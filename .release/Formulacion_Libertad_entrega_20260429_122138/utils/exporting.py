from io import BytesIO
from pathlib import Path

from django.http import HttpResponse
from django.utils import timezone
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


BASE_DIR = Path(__file__).resolve().parent.parent
LOGO_PATH = BASE_DIR / "static" / "img" / "logo-istul.png"


def build_pdf_response(
    filename,
    title,
    headers,
    rows,
    subtitle=None,
    page_orientation="landscape",
    generated_by=None,
    generated_at=None,
):
    buffer = BytesIO()
    pagesize = landscape(A4) if page_orientation == "landscape" else A4
    doc = SimpleDocTemplate(buffer, pagesize=pagesize, leftMargin=24, rightMargin=24, topMargin=24, bottomMargin=24)
    styles = getSampleStyleSheet()
    generated_at = generated_at or timezone.localtime()
    generated_at_text = generated_at.strftime("%d/%m/%Y %H:%M")
    generated_by_text = generated_by or "Sistema"
    title_style = ParagraphStyle(
        "InstitutionTitle",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=18,
        leading=22,
        textColor=colors.HexColor("#0e3a5a"),
        spaceAfter=6,
    )
    subtitle_style = ParagraphStyle(
        "InstitutionSubtitle",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#486170"),
        spaceAfter=6,
    )
    header_meta_style = ParagraphStyle(
        "HeaderMeta",
        parent=styles["BodyText"],
        fontName="Helvetica-Bold",
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#0e3a5a"),
    )
    info_style = ParagraphStyle(
        "HeaderInfo",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#5a7281"),
        spaceAfter=2,
    )

    story = []
    if LOGO_PATH.exists():
        logo = Image(str(LOGO_PATH))
        logo.drawHeight = 20 * mm
        logo.drawWidth = 50 * mm
        story.append(logo)
        story.append(Spacer(1, 6))

    story.append(Paragraph("Instituto Superior Tecnologico Universitario Libertad", header_meta_style))
    story.append(Paragraph("Sistema de Formulacion Magistral - Reporte institucional", subtitle_style))
    story.append(Spacer(1, 6))
    story.append(Paragraph(title, title_style))
    if subtitle:
        story.append(Paragraph(subtitle, subtitle_style))
    story.append(Paragraph(f"Fecha de emision: {generated_at_text}", info_style))
    story.append(Paragraph(f"Generado por: {generated_by_text}", info_style))
    story.append(Spacer(1, 12))

    data = [headers] + [[str(cell) for cell in row] for row in rows]
    table = Table(data, repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0e3a5a")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#d0dde6")),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f5f8fb")]),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("LEADING", (0, 0), (-1, -1), 11),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
                ("TOPPADDING", (0, 0), (-1, 0), 8),
            ]
        )
    )
    story.append(table)

    def draw_footer(canvas, pdf_doc):
        canvas.saveState()
        footer_y = 12 * mm
        canvas.setStrokeColor(colors.HexColor("#d0dde6"))
        canvas.line(pdf_doc.leftMargin, footer_y + 5, pdf_doc.pagesize[0] - pdf_doc.rightMargin, footer_y + 5)
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(colors.HexColor("#5a7281"))
        canvas.drawString(pdf_doc.leftMargin, footer_y - 2, "Instituto Superior Tecnologico Universitario Libertad")
        canvas.drawRightString(
            pdf_doc.pagesize[0] - pdf_doc.rightMargin,
            footer_y - 2,
            f"Pagina {canvas.getPageNumber()}",
        )
        canvas.restoreState()

    doc.build(story, onFirstPage=draw_footer, onLaterPages=draw_footer)
    pdf = buffer.getvalue()
    buffer.close()

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    response.write(pdf)
    return response
