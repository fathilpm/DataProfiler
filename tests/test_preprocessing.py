import numpy as np
import pandas as pd
import pytest

from profiler.preprocessing import (
    ColumnDropper, RowDropperNA, TypeConverter, SimpleImputer,
    MinMaxScaler, StandardScaler, RobustScaler, OneHotEncoder,
    LabelEncoder, OutlierCapper, AutoPreprocessor
)

@pytest.fixture
def base_df():
    return pd.DataFrame({
        "a": [1, 2, np.nan, 4, 5],
        "b": ["cat", "dog", "cat", None, "dog"],
        "c": [10.0, 20.0, 30.0, 40.0, 100.0],  # 100 is an outlier (Q1=20, Q3=40, IQR=20, Upper=70)
        "d": ["1", "2", "3", "4", "5"],
        "const": [1, 1, 1, 1, 1]
    })

def test_column_dropper(base_df):
    dropper = ColumnDropper(columns=["const", "non_existent"])
    res = dropper.fit_transform(base_df)
    assert "const" not in res.columns
    assert "a" in res.columns
    assert res.shape == (5, 4)

def test_row_dropper_na(base_df):
    dropper = RowDropperNA(column="a")
    res = dropper.fit_transform(base_df)
    assert res.shape[0] == 4
    assert not res["a"].isnull().any()

def test_type_converter(base_df):
    converter = TypeConverter(column="d", target_type="numeric")
    res = converter.fit_transform(base_df)
    assert pd.api.types.is_numeric_dtype(res["d"])

    converter_str = TypeConverter(column="a", target_type="string")
    res_str = converter_str.fit_transform(base_df)
    assert pd.api.types.is_string_dtype(res_str["a"]) or res_str["a"].dtype == object

def test_simple_imputer_numeric(base_df):
    imputer = SimpleImputer(column="a", strategy="mean")
    res = imputer.fit_transform(base_df)
    assert not res["a"].isnull().any()
    assert res["a"].iloc[2] == 3.0  # Mean of [1, 2, 4, 5] is 3.0

    imputer_median = SimpleImputer(column="a", strategy="median")
    res_median = imputer_median.fit_transform(base_df)
    assert not res_median["a"].isnull().any()
    assert res_median["a"].iloc[2] == 3.0  # Median of [1, 2, 4, 5] is 3.0

def test_simple_imputer_categorical(base_df):
    imputer = SimpleImputer(column="b", strategy="mode")
    res = imputer.fit_transform(base_df)
    assert not res["b"].isnull().any()
    assert res["b"].iloc[3] in ["cat", "dog"]

    imputer_const = SimpleImputer(column="b", strategy="constant", fill_value="missing")
    res_const = imputer_const.fit_transform(base_df)
    assert res_const["b"].iloc[3] == "missing"

def test_min_max_scaler(base_df):
    scaler = MinMaxScaler(column="c")
    res = scaler.fit_transform(base_df)
    assert res["c"].min() == pytest.approx(0.0)
    assert res["c"].max() == pytest.approx(1.0)
    assert res["c"].iloc[1] == pytest.approx(10.0 / 90.0)

def test_standard_scaler(base_df):
    scaler = StandardScaler(column="c")
    res = scaler.fit_transform(base_df)
    assert res["c"].mean() == pytest.approx(0.0, abs=1e-7)
    assert res["c"].std() == pytest.approx(1.0, abs=1e-7)

def test_robust_scaler(base_df):
    scaler = RobustScaler(column="c")
    res = scaler.fit_transform(base_df)
    assert res["c"].median() == pytest.approx(0.0)

def test_label_encoder(base_df):
    df_clean = base_df.dropna(subset=["b"])
    encoder = LabelEncoder(column="b")
    res = encoder.fit_transform(df_clean)
    assert set(res["b"].unique()) == {0, 1}

def test_one_hot_encoder(base_df):
    df_clean = base_df.dropna(subset=["b"])
    encoder = OneHotEncoder(column="b")
    res = encoder.fit_transform(df_clean)
    assert "b_cat" in res.columns
    assert "b_dog" in res.columns
    assert "b" not in res.columns
    assert res["b_cat"].iloc[0] == 1

def test_outlier_capper(base_df):
    capper = OutlierCapper(column="c", factor=1.5)
    res = capper.fit_transform(base_df)
    # q1 = 20, q3 = 40, iqr = 20. lower = -10, upper = 70.
    assert res["c"].max() == pytest.approx(70.0)
    assert res["c"].iloc[4] == pytest.approx(70.0)

def test_auto_preprocessor(base_df):
    # a has null, b has null, c has outlier, const is constant
    preprocessor = AutoPreprocessor(missing_threshold=0.8, onehot_threshold=5, outlier_factor=1.5)
    res = preprocessor.fit_transform(base_df)
    assert "const" not in res.columns
    assert not res["a"].isnull().any()
    assert "b" not in res.columns
    assert "b_cat" in res.columns
    assert res["c"].max() == pytest.approx(70.0)
