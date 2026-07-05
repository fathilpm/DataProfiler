from __future__ import annotations

from pathlib import Path

from profiler.config.profile_config import ProfileConfig
from profiler.engine.profiler_engine import ProfilerEngine
from profiler.readers.factory import ReaderFactory
from profiler.report.console_reporter import ConsoleReporter
from profiler.report.html_reporter import HTMLReporter
from profiler.report.json_reporter import JSONReporter
from profiler.report.markdown_reporter import MarkdownReporter


def main() -> None:

    file_path = Path("examples/test_dataset.csv")

    # Load
    reader = ReaderFactory.get_reader(file_path)
    dataset = reader.read(file_path)

    # Configure — enable all modules
    config = ProfileConfig(
        run_statistics=True,
        run_quality=True,
        export_html=True,
        export_json=True,
        export_markdown=True,
    )

    # Profile
    profile = ProfilerEngine.profile(dataset, config=config)

    # Console output
    reporter = ConsoleReporter()
    reporter.display(profile)

    # File exports
    if config.export_html:
        path = HTMLReporter().export(profile)
        print(f"\n  HTML report saved -> {path}")

    if config.export_json:
        path = JSONReporter().export(profile)
        print(f"  JSON export saved -> {path}")

    if config.export_markdown:
        path = MarkdownReporter().export(profile)
        print(f"  Markdown report saved -> {path}")

    print()


if __name__ == "__main__":
    main()