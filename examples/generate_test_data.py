"""Generates a rich test dataset that exercises all DataProfiler features."""
import pandas as pd
import numpy as np
from pathlib import Path

np.random.seed(42)
n = 200

df = pd.DataFrame({
    # Integer — primary-key-like, high cardinality
    "customer_id": range(1, n + 1),

    # String — categorical with realistic distribution
    "country": np.random.choice(
        ["India", "USA", "UK", "Germany", "France"],
        size=n,
        p=[0.40, 0.25, 0.15, 0.12, 0.08],
    ),

    # String — high cardinality (almost unique names)
    "name": [f"Customer_{i}" for i in range(1, n + 1)],

    # Float — with outliers injected
    "revenue": np.concatenate([
        np.random.normal(5000, 1200, n - 5),
        [95000, 87000, 110000, 78000, 92000],  # outliers
    ]),

    # Integer — age with realistic range
    "age": np.random.randint(18, 65, size=n),

    # Boolean
    "is_active": np.random.choice([True, False], size=n, p=[0.75, 0.25]),

    # DateTime
    "joined_date": pd.date_range("2018-01-01", periods=n, freq="3D"),

    # Constant column — should be flagged
    "version": ["v1"] * n,

    # Float — with missing values (15%)
    "score": np.where(
        np.random.rand(n) < 0.15,
        np.nan,
        np.random.uniform(0, 100, n),
    ),

    # Category
    "plan": np.random.choice(["Free", "Basic", "Pro", "Enterprise"], size=n),
})

# Inject 8 duplicate rows
duplicates = df.iloc[10:18].copy()
df = pd.concat([df, duplicates], ignore_index=True)

# Inject mixed types in one column (object dtype)
df["notes"] = pd.Series(["OK"] * len(df), dtype="object")
df.loc[5:10, "notes"] = 123  # inject integers into object column

output = Path("examples/test_dataset.csv")
df.to_csv(output, index=False)
print(f"Generated {len(df)} rows x {len(df.columns)} columns -> {output}")
print(f"Columns: {list(df.columns)}")
print(f"\nFeatures exercised:")
print(f"  Outliers        : revenue (5 extreme values)")
print(f"  Missing values  : score (~15% null)")
print(f"  Duplicates      : 8 duplicate rows injected")
print(f"  Constant column : version")
print(f"  Mixed types     : notes (str + int mixed)")
print(f"  Boolean         : is_active")
print(f"  DateTime        : joined_date")
print(f"  Categorical     : country, plan")
print(f"  Numeric         : revenue, age, score")
