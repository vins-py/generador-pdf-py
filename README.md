# Generador de PDF Automático con Python

Este proyecto genera automáticamente un reporte de ventas en formato PDF usando Python.

El programa toma datos desde un archivo CSV, calcula subtotales, IVA, total vendido, ventas por producto, ventas por día y genera un PDF listo para entregar o enviar.

## Funciones principales

- Lee datos desde un archivo CSV.
- Calcula subtotal, IVA y total.
- Genera resumen general de ventas.
- Agrupa ventas por producto.
- Agrupa ventas por día.
- Crea un PDF automático.
- Incluye detalle de ventas.
- Genera datos de prueba si no existe el CSV.

## Archivos principales

- `generar_pdf.py`: programa principal que genera el PDF.
- `datos_ventas.csv`: archivo de datos de entrada.
- `reporte_ventas.pdf`: archivo PDF generado.

## Tecnologías usadas

- Python
- Pandas
- FPDF2
- CSV

## Objetivo del proyecto

Este proyecto fue creado para practicar generación automática de reportes en PDF con Python, útil para ventas, negocios, administración y automatización de documentos.