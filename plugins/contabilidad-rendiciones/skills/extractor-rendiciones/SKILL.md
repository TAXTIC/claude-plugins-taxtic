---
name: extractor-rendiciones
description: Extrae gastos de PDFs de rendiciones de caja chica chilenas (boletas, facturas y comprobantes, escaneados o digitales) a CSV + Excel. Orquesta un agente por PDF para no saturar el contexto con escaneos pesados. Detecta página, fecha, tipo de documento, número, proveedor, RUT, descripción, centro de costo, neto, IVA y total por gasto. Útil para rendiciones de caja chica, ingreso masivo y conciliación.
---

**Idioma de respuesta:** siempre en español chileno. Terminología contable/tributaria local. Todo el output (resúmenes, validaciones, mensajes de error, comentarios) en español. Solo cambiar de idioma si el usuario lo solicita explícitamente.

# Extraer rendiciones a CSV + Excel (orquestador)

Cuando el usuario invoca este skill (palabras gatillo: "extrae rendiciones", "rendiciones a csv", "procesa estos PDF de caja chica", "leeme las rendiciones de esta carpeta"), orquestas la extracción.

**Importante:** este skill NO lee los PDFs directamente. Los escaneos de rendición son pesados
(5–17 MB) y leerlos todos en este contexto lo satura y puede superar el límite de ~32 MB por request.
Por eso delegas cada PDF a un agente que lo procesa en su propio contexto y te devuelve solo las filas.

## Privacidad (leer primero)

El procesamiento usa Claude visión: los PDFs se envían a Claude. Pueden contener datos tributarios
reales (RUT, montos, proveedores). Procesarlos está permitido según la configuración corporativa
vigente de Taxtic. Para compartir el resultado fuera de la organización, anonimizar antes con
`/anonimizar` (plugin `comun-anonimizacion`).

## Inputs aceptados

- Una carpeta con archivos `.pdf` (ej: `rendiciones/`).
- Una lista explícita de rutas `.pdf`.
- Un único PDF.

Si no se especifica, asumir la carpeta actual.

## Flujo (orquestación)

1. **Listar PDFs**: usar `Glob` con patrón `**/*.pdf` (o el path dado). Mostrar cuántos se procesarán y
   pedir confirmación si son >50.

2. **Por cada PDF, despachar el agente `extractor-rendicion-pdf`** con la tool `Task`, pasándole la
   ruta del PDF. Procesar **de a uno** (no leas tú el PDF en este contexto). El agente devuelve un
   JSON con esta forma:
   ```json
   { "rendicion": "283", "total_resumen": 430874, "filas": [ { ...campos... } ], "no_procesado": false }
   ```

3. **Acumular** las `filas` de cada agente. Tu contexto solo crece con texto (filas), nunca con
   imágenes de PDF. Si un agente devuelve `no_procesado: true`, registrar una fila con
   `Observacion = NO_PROCESADO` para ese archivo.

4. **Generar salida** en la carpeta de los PDFs (o el path indicado):
   - `resumen-rendiciones.csv` — UTF-8 con BOM, encabezado + una fila por gasto. Usar `Write`.
   - `resumen-rendiciones.xlsx` — desde el CSV con Python + openpyxl:
     ```
     python -c "import csv; from openpyxl import Workbook; wb=Workbook(); ws=wb.active; ws.title='Rendicion'; rows=list(csv.reader(open('resumen-rendiciones.csv', encoding='utf-8-sig'))); [ws.append(r) for r in rows]; wb.save('resumen-rendiciones.xlsx')"
     ```
     Si `openpyxl` no está instalado (ImportError), generar solo el CSV y avisar:
     "Excel omitido: instala openpyxl con `pip install openpyxl` y reintenta".

5. **Control vs hoja resumen** (best-effort): si algún agente reportó `total_resumen` legible,
   comparar contra la suma de `Total` de los gastos de esa rendición y reportar la diferencia como
   advertencia global. No bloquea ni descarta nada.

6. **Reportar resumen** al usuario:
   - N gastos extraídos.
   - Suma de Neto, suma de IVA, suma de Total.
   - Cantidad de filas con observación / `REVISAR`.
   - Hojas resumen usadas como control y diferencia vs total rendido (si se pudo comparar).
   - Archivos `NO_PROCESADO`.

## Formato CSV (orden exacto de columnas)

```
Archivo,Pagina,Rendicion,Fecha,TipoDocumento,NumeroDocumento,Proveedor,RutProveedor,Descripcion,CentroCosto,Neto,IVA,Total,Observacion
RENDICION 283.pdf,3,283,07-04-2026,FACTURA,358,Comercial Los Andes Ltda,76086428-5,Aridos para obra,Vizcaya,1000000,190000,1190000,
RENDICION 283.pdf,4,283,09-04-2026,BOLETA,9912,Minimarket El Sol,77654321-2,Insumos oficina,Oficina,5000,950,5950,
documento-ilegible.pdf,,,,,,,,,,,,,NO_PROCESADO
```

Encoding UTF-8 con BOM (compatibilidad Excel chileno). El agente `extractor-rendicion-pdf` define y
valida los campos de cada fila.

## Auditoría

Tras generar el CSV, ofrecer al usuario auditar con el agente `auditor-rendiciones`
(resumen global + hallazgos CRÍTICO/ADVERTENCIA/INFO).

## Limitaciones

- La precisión depende de la calidad del escaneo. Lo dudoso queda `REVISAR` para revisión humana.
- Para lotes muy grandes de escaneos pesados, la latencia/costo suben (un agente por PDF). La app
  Python con OCR sigue siendo la alternativa liviana para volumen.
