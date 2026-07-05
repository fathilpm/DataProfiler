from __future__ import annotations


class SizeFormatter:
    """Formats byte values into human-readable units."""

    UNITS = ("B", "KB", "MB", "GB", "TB")

    @staticmethod
    def format(size: int) -> str:
        value = float(size)

        for unit in SizeFormatter.UNITS:
            if value < 1024 or unit == SizeFormatter.UNITS[-1]:
                if unit == "B":
                    return f"{int(value)} {unit}"
                return f"{value:.2f} {unit}"

            value /= 1024