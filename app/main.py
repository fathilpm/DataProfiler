from pathlib import Path

from profiler.engine.profiler_engine import ProfilerEngine
from profiler.readers.factory import ReaderFactory


def main() -> None:

    file_path = Path("examples/sample.csv")

    reader = ReaderFactory.get_reader(file_path)

    dataframe = reader.read(file_path)

    profile = ProfilerEngine.profile(
        dataframe,
        dataset_name=file_path.name,
    )

    print("=" * 50)
    print("DATASET PROFILE")
    print("=" * 50)

    print(f"Dataset : {profile.dataset_name}")
    print(f"Rows    : {profile.rows}")
    print(f"Columns : {profile.columns}")
    print(f"Memory  : {profile.memory_usage} bytes")
    print(f"Duplicates : {profile.duplicate_rows}")

    print("\nColumns")

    for column in profile.column_profiles:

        print("-" * 40)

        print(f"Name       : {column.name}")
        print(f"Type       : {column.dtype}")
        print(f"Missing    : {column.missing_count}")
        print(f"Missing %  : {column.missing_percentage:.2f}")
        print(f"Unique     : {column.unique_count}")

if __name__ == "__main__":
    main()