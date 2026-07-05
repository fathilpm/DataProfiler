from __future__ import annotations


class Formatter:
    """Common formatting utilities for reporters."""

    @staticmethod
    def title(text: str) -> str:
        line = "=" * 60
        return f"\n{line}\n{text.center(60)}\n{line}"

    @staticmethod
    def separator() -> str:
        return "-" * 60