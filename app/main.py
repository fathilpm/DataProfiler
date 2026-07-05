from __future__ import annotations

from pathlib import Path

from profiler.engine.profiler_engine import ProfilerEngine
from profiler.readers.factory import ReaderFactory
from profiler.report.console_reporter import ConsoleReporter


def main() -> None:

    file_path = Path("examples/sample.csv")

    reader = ReaderFactory.get_reader(file_path)

    dataset = reader.read(file_path)

    profile = ProfilerEngine.profile(dataset)

    reporter = ConsoleReporter()

    reporter.display(profile)


if __name__ == "__main__":
    main()