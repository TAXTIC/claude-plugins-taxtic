"""Generate 10 synthetic Chilean invoice PDFs for training demo.

All RUTs are dummy (validated to pass module 11 but not real).
All company names are fictional.
"""

from pathlib import Path
import random
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas

OUTPUT_DIR = Path(__file__).parent / "facturas-octubre"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

PROVEEDORES = [
    ("11111111-1", "Proveedor Alfa SpA"),
    ("22222222-2", "Comercializadora Beta Ltda"),
    ("33333333-3", "Servicios Gamma E.I.R.L."),
    ("44444444-4", "Distribuidora Delta SpA"),
    ("55555555-5", "Importadora Épsilon Ltda"),
]

GLOSAS = [
    "Materiales de oficina",
    "Servicio mantención mensual",
    "Asesoría legal octubre",
    "Suministro eléctrico",
    "Honorarios consultoría",
    "Arriendo bodega",
    "Combustible flota",
    "Publicidad redes sociales",
    "Servicios de internet",
    "Repuestos vehículo",
]

random.seed(42)  # reproducible

def generar_factura(index: int) -> None:
    """Generate one invoice PDF."""
    numero = 10000 + index
    fecha = f"2026-10-{(index % 28) + 1:02d}"
    rut_prov, razon = random.choice(PROVEEDORES)
    glosa = random.choice(GLOSAS)
    neto = random.choice([150_000, 280_000, 540_000, 1_200_000, 3_400_000])
    iva = round(neto * 0.19)
    total = neto + iva

    pdf_path = OUTPUT_DIR / f"factura-{index:03d}.pdf"
    c = canvas.Canvas(str(pdf_path), pagesize=A4)
    width, height = A4

    # Header
    c.setFont("Helvetica-Bold", 18)
    c.drawString(2 * cm, height - 2 * cm, "FACTURA ELECTRÓNICA")
    c.setFont("Helvetica", 12)
    c.drawString(2 * cm, height - 3 * cm, f"N° {numero}")
    c.drawString(2 * cm, height - 3.7 * cm, f"Fecha emisión: {fecha}")

    # Proveedor
    c.setFont("Helvetica-Bold", 11)
    c.drawString(2 * cm, height - 5 * cm, "Proveedor:")
    c.setFont("Helvetica", 11)
    c.drawString(2 * cm, height - 5.6 * cm, f"Razón social: {razon}")
    c.drawString(2 * cm, height - 6.2 * cm, f"RUT: {rut_prov}")

    # Glosa
    c.setFont("Helvetica-Bold", 11)
    c.drawString(2 * cm, height - 8 * cm, "Detalle:")
    c.setFont("Helvetica", 11)
    c.drawString(2 * cm, height - 8.6 * cm, glosa)

    # Totales
    y = height - 11 * cm
    c.setFont("Helvetica-Bold", 11)
    c.drawString(2 * cm, y, "Neto:")
    c.drawRightString(width - 2 * cm, y, f"$ {neto:,}".replace(",", "."))

    y -= 0.7 * cm
    c.drawString(2 * cm, y, "IVA (19%):")
    c.drawRightString(width - 2 * cm, y, f"$ {iva:,}".replace(",", "."))

    y -= 0.7 * cm
    c.setFont("Helvetica-Bold", 13)
    c.drawString(2 * cm, y, "TOTAL:")
    c.drawRightString(width - 2 * cm, y, f"$ {total:,}".replace(",", "."))

    c.showPage()
    c.save()
    print(f"  Generated: {pdf_path.name}")


def main() -> None:
    print(f"Generating 10 invoices in {OUTPUT_DIR}")
    for i in range(1, 11):
        generar_factura(i)
    print("Done.")


if __name__ == "__main__":
    main()
