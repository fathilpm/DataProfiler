from pathlib import Path

from profiler.readers.factory import ReaderFactory


def main() -> None:
    file_path = Path("examples/sample.csv")

    reader = ReaderFactory.get_reader(file_path)

    dataframe = reader.read(file_path)

    print(dataframe.head())


if __name__ == "__main__":
    main()