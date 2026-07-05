from __future__ import annotations


class Formatter:
    """Common formatting utilities for reporters."""

    WIDTH = 72

    @staticmethod
    def title(text: str) -> str:
        line = "=" * Formatter.WIDTH
        return f"\n{line}\n{text.center(Formatter.WIDTH)}\n{line}"

    @staticmethod
    def section(text: str) -> str:
        return f"\n{text.upper()}\n{Formatter.separator()}"

    @staticmethod
    def separator() -> str:
        return "-" * Formatter.WIDTH

    @staticmethod
    def table(
        headers: list[str],
        rows: list[list[str]],
        min_col_width: int = 8,
    ) -> str:
        """
        Renders a dynamic-width text table.

        Column widths are automatically sized to fit the widest value
        in each column (header or data).
        """
        # Compute column widths
        col_widths = [
            max(min_col_width, len(h))
            for h in headers
        ]
        for row in rows:
            for i, cell in enumerate(row):
                if i < len(col_widths):
                    col_widths[i] = max(col_widths[i], len(str(cell)))

        # Add padding
        col_widths = [w + 2 for w in col_widths]

        sep = Formatter.separator()

        # Header row
        header_line = "".join(
            h.ljust(col_widths[i]) for i, h in enumerate(headers)
        )

        lines = [sep, header_line, sep]

        # Data rows
        for row in rows:
            line = "".join(
                str(cell).ljust(col_widths[i]) for i, cell in enumerate(row)
            )
            lines.append(line)

        lines.append(sep)
        return "\n".join(lines)

    @staticmethod
    def kv(label: str, value: str, label_width: int = 18) -> str:
        """Renders a key-value line: 'Label          : value'"""
        return f"{label:<{label_width}}: {value}"