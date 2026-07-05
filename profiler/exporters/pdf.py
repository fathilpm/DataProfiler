from __future__ import annotations

from pathlib import Path

from profiler.models.profile import ColumnProfile, DatasetProfile
from profiler.utils.size_formatter import SizeFormatter

try:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import cm
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    )
    _REPORTLAB_AVAILABLE = True
except ImportError:
    _REPORTLAB_AVAILABLE = False


def _check_reportlab() -> None:
    if not _REPORTLAB_AVAILABLE:
        raise ImportError(
            "reportlab is required for PDF export. "
            "Install it with: pip install reportlab"
        )


class PDFExporter:
    """Exports a DatasetProfile to a PDF report file using reportlab."""

    @staticmethod
    def export(profile: DatasetProfile, output_path: Path) -> Path:
        """
        Writes a formatted PDF report.

        Parameters
        ----------
        profile : DatasetProfile
            The profile to render.
        output_path : Path
            Destination .pdf file.

        Returns
        -------
        Path
            Path to the written file.
        """
        _check_reportlab()

        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        doc = SimpleDocTemplate(
            str(output_path),
            pagesize=A4,
            rightMargin=2 * cm,
            leftMargin=2 * cm,
            topMargin=2 * cm,
            bottomMargin=2 * cm,
        )

        styles = getSampleStyleSheet()
        story = []

        # ── Accent colors ─────────────────────────────────────────────────
        ACCENT = colors.HexColor("#6366f1")
        BG_HEADER = colors.HexColor("#1a1a2e")
        TEXT_MUTED = colors.HexColor("#94a3b8")

        # ── Title ─────────────────────────────────────────────────────────
        title_style = ParagraphStyle(
            "Title", parent=styles["Title"],
            textColor=ACCENT, fontSize=20, spaceAfter=4,
        )
        story.append(Paragraph("DataProfiler Report", title_style))
        sub_style = ParagraphStyle(
            "Sub", parent=styles["Normal"],
            textColor=TEXT_MUTED, fontSize=10, spaceAfter=16,
        )
        story.append(Paragraph(f"Dataset: {profile.dataset_name}", sub_style))

        # ── Overview Table ────────────────────────────────────────────────
        h2_style = ParagraphStyle(
            "H2", parent=styles["Heading2"],
            textColor=ACCENT, fontSize=12, spaceBefore=14, spaceAfter=6,
        )
        story.append(Paragraph("Overview", h2_style))

        c = profile.completeness
        hs_score = (
            f"{profile.health_score.score} / 100 (Grade {profile.health_score.grade})"
            if profile.health_score else "N/A"
        )
        overview_data = [
            ["Property", "Value"],
            ["Rows", f"{profile.rows:,}"],
            ["Columns", str(profile.columns)],
            ["Memory Usage", SizeFormatter.format(profile.memory_usage)],
            ["Duplicate Rows", str(profile.duplicate_rows)],
            ["Completeness", f"{c.completeness_percentage:.2f}%"],
            ["Missing Cells", f"{c.missing_cells:,}"],
            ["Health Score", hs_score],
        ]

        overview_table = Table(overview_data, colWidths=[8 * cm, 8 * cm])
        overview_table.setStyle(PDFExporter._table_style(ACCENT, BG_HEADER))
        story.append(overview_table)
        story.append(Spacer(1, 0.5 * cm))

        # ── Column Summary Table ──────────────────────────────────────────
        story.append(Paragraph("Column Summary", h2_style))

        col_headers = ["#", "Column", "Type", "Nullable", "Missing", "Unique", "Memory"]
        col_data = [col_headers]
        for i, col in enumerate(profile.column_profiles, 1):
            missing = f"{col.missing_count} ({col.missing_percentage:.1f}%)"
            unique = f"{col.unique_count} ({col.unique_percentage:.1f}%)"
            col_data.append([
                str(i), col.name, col.dtype,
                "Yes" if col.nullable else "No",
                missing, unique,
                SizeFormatter.format(col.memory_usage),
            ])

        col_table = Table(col_data, repeatRows=1)
        col_table.setStyle(PDFExporter._table_style(ACCENT, BG_HEADER))
        story.append(col_table)
        story.append(Spacer(1, 0.5 * cm))

        # ── Quality Report ────────────────────────────────────────────────
        if profile.quality_report:
            qr = profile.quality_report
            story.append(Paragraph("Data Quality", h2_style))
            quality_data = [
                ["Check", "Result"],
                ["Constant Columns", ", ".join(qr.constant_columns) or "None"],
                ["High Cardinality Columns", ", ".join(qr.high_cardinality_columns) or "None"],
                ["Columns with Outliers", ", ".join(qr.outlier_columns) or "None"],
                ["Duplicate Rows", str(qr.duplicate_rows)],
            ]
            quality_table = Table(quality_data, colWidths=[8 * cm, 8 * cm])
            quality_table.setStyle(PDFExporter._table_style(ACCENT, BG_HEADER))
            story.append(quality_table)

            if qr.warnings:
                story.append(Spacer(1, 0.3 * cm))
                story.append(Paragraph("Warnings", h2_style))
                warn_style = ParagraphStyle(
                    "warn", parent=styles["Normal"],
                    textColor=colors.HexColor("#f59e0b"),
                    fontSize=9, spaceAfter=4,
                )
                for w in qr.warnings:
                    story.append(Paragraph(f"⚠ {w}", warn_style))

        doc.build(story)
        return output_path

    @staticmethod
    def _table_style(accent, bg_header) -> TableStyle:
        return TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), bg_header),
            ("TEXTCOLOR", (0, 0), (-1, 0), accent),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 9),
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ("FONTSIZE", (0, 1), (-1, -1), 8),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [
                colors.HexColor("#0f0f1a"),
                colors.HexColor("#1a1a2e"),
            ]),
            ("TEXTCOLOR", (0, 1), (-1, -1), colors.HexColor("#e2e8f0")),
            ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#2d2d50")),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ])
