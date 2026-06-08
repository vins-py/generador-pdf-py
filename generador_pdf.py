import pandas as pd
from pathlib import Path
from fpdf import FPDF
from datetime import datetime


ARCHIVO_DATOS = Path("datos_ventas.csv")
ARCHIVO_PDF = Path("reporte_ventas.pdf")


def crear_datos_prueba():
    if ARCHIVO_DATOS.exists():
        return

    datos = {
        "fecha": [
            "2026-06-01", "2026-06-01", "2026-06-02",
            "2026-06-02", "2026-06-03", "2026-06-03",
            "2026-06-04", "2026-06-04"
        ],
        "producto": [
            "Aceite", "Filtro", "Aceite", "Llanta",
            "Bujia", "Filtro", "Llanta", "Aceite"
        ],
        "cantidad": [3, 2, 4, 2, 8, 3, 1, 6],
        "precio": [180, 120, 180, 950, 80, 120, 950, 180]
    }

    ventas = pd.DataFrame(datos)
    ventas["subtotal"] = ventas["cantidad"] * ventas["precio"]
    ventas["iva"] = ventas["subtotal"] * 0.16
    ventas["total"] = ventas["subtotal"] + ventas["iva"]

    ventas.to_csv(ARCHIVO_DATOS, index=False, encoding="utf-8")

    print(f"Archivo creado: {ARCHIVO_DATOS}")


def dinero(valor):
    return f"${valor:,.2f}"


def generar_pdf():
    crear_datos_prueba()

    ventas = pd.read_csv(ARCHIVO_DATOS)

    total_vendido = ventas["total"].sum()
    subtotal_general = ventas["subtotal"].sum()
    iva_general = ventas["iva"].sum()
    cantidad_total = ventas["cantidad"].sum()

    ventas_por_producto = (
        ventas.groupby("producto", as_index=False)
        .agg({
            "cantidad": "sum",
            "total": "sum"
        })
        .sort_values("total", ascending=False)
    )

    ventas_por_dia = (
        ventas.groupby("fecha", as_index=False)
        .agg({
            "cantidad": "sum",
            "total": "sum"
        })
    )

    producto_mas_vendido = ventas.groupby("producto")["cantidad"].sum().idxmax()
    producto_mayor_ingreso = ventas.groupby("producto")["total"].sum().idxmax()

    fecha_reporte = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.set_font("Helvetica", "B", 18)
    pdf.cell(0, 10, "Reporte Automatico de Ventas", ln=True, align="C")

    pdf.set_font("Helvetica", "", 10)
    pdf.cell(0, 8, f"Fecha de generacion: {fecha_reporte}", ln=True, align="C")

    pdf.ln(8)

    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 8, "Resumen general", ln=True)

    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 7, f"Subtotal general: {dinero(subtotal_general)}", ln=True)
    pdf.cell(0, 7, f"IVA general: {dinero(iva_general)}", ln=True)
    pdf.cell(0, 7, f"Total vendido: {dinero(total_vendido)}", ln=True)
    pdf.cell(0, 7, f"Cantidad total vendida: {cantidad_total}", ln=True)
    pdf.cell(0, 7, f"Producto mas vendido: {producto_mas_vendido}", ln=True)
    pdf.cell(0, 7, f"Producto con mayor ingreso: {producto_mayor_ingreso}", ln=True)

    pdf.ln(8)

    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 8, "Ventas por producto", ln=True)

    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(60, 8, "Producto", border=1)
    pdf.cell(40, 8, "Cantidad", border=1, align="C")
    pdf.cell(50, 8, "Total", border=1, align="R")
    pdf.ln()

    pdf.set_font("Helvetica", "", 10)

    for _, fila in ventas_por_producto.iterrows():
        pdf.cell(60, 8, str(fila["producto"]), border=1)
        pdf.cell(40, 8, str(int(fila["cantidad"])), border=1, align="C")
        pdf.cell(50, 8, dinero(fila["total"]), border=1, align="R")
        pdf.ln()

    pdf.ln(8)

    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 8, "Ventas por dia", ln=True)

    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(60, 8, "Fecha", border=1)
    pdf.cell(40, 8, "Cantidad", border=1, align="C")
    pdf.cell(50, 8, "Total", border=1, align="R")
    pdf.ln()

    pdf.set_font("Helvetica", "", 10)

    for _, fila in ventas_por_dia.iterrows():
        pdf.cell(60, 8, str(fila["fecha"]), border=1)
        pdf.cell(40, 8, str(int(fila["cantidad"])), border=1, align="C")
        pdf.cell(50, 8, dinero(fila["total"]), border=1, align="R")
        pdf.ln()

    pdf.ln(8)

    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 8, "Detalle de ventas", ln=True)

    pdf.set_font("Helvetica", "B", 9)
    pdf.cell(28, 8, "Fecha", border=1)
    pdf.cell(38, 8, "Producto", border=1)
    pdf.cell(25, 8, "Cant.", border=1, align="C")
    pdf.cell(30, 8, "Precio", border=1, align="R")
    pdf.cell(30, 8, "Total", border=1, align="R")
    pdf.ln()

    pdf.set_font("Helvetica", "", 9)

    for _, fila in ventas.iterrows():
        pdf.cell(28, 8, str(fila["fecha"]), border=1)
        pdf.cell(38, 8, str(fila["producto"]), border=1)
        pdf.cell(25, 8, str(int(fila["cantidad"])), border=1, align="C")
        pdf.cell(30, 8, dinero(fila["precio"]), border=1, align="R")
        pdf.cell(30, 8, dinero(fila["total"]), border=1, align="R")
        pdf.ln()

    pdf.output(ARCHIVO_PDF)

    print("PDF creado correctamente.")
    print(f"Archivo generado: {ARCHIVO_PDF}")
    print("-------------------------")
    print(f"Total vendido: {dinero(total_vendido)}")
    print(f"Producto mas vendido: {producto_mas_vendido}")


generar_pdf()