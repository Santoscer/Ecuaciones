"""Preparación de archivos descargables."""
from io import BytesIO
import pandas as pd

def csv_bytes(curvas: pd.DataFrame) -> bytes:
    return curvas.to_csv(index=False, float_format="%.5f").encode("utf-8-sig")

def pdf_bytes(curvas: pd.DataFrame, resumen: pd.DataFrame, T0: float, Ta: float) -> bytes:
    """Crea informe breve con ReportLab, dependencia opcional."""
    try:
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import letter
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
        from reportlab.lib.styles import getSampleStyleSheet
    except ImportError as exc:
        raise RuntimeError("La exportación PDF requiere instalar reportlab.") from exc
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    filas = [list(resumen.columns)] + resumen.fillna("No alcanzado").astype(str).values.tolist()
    tabla = Table(filas, repeatRows=1)
    tabla.setStyle(TableStyle([("BACKGROUND", (0,0),(-1,0),colors.HexColor("#12304a")),
        ("TEXTCOLOR",(0,0),(-1,0),colors.white),("GRID",(0,0),(-1,-1),.4,colors.grey),
        ("FONTSIZE",(0,0),(-1,-1),8),("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.white,colors.whitesmoke])]))
    doc.build([Paragraph("Simulación de enfriamiento de CPU", styles["Title"]),
               Paragraph(f"Ley de Newton · T₀={T0:g} °C · Tₐ={Ta:g} °C · tiempo en minutos", styles["BodyText"]),
               Spacer(1, 14), tabla])
    return buffer.getvalue()
