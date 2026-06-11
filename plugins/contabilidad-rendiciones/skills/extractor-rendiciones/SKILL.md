---
name: extractor-rendiciones
description: Extrae gastos de PDFs de rendiciones de caja chica chilenas (boletas, facturas y comprobantes, escaneados o digitales) a CSV + Excel. Detecta página, fecha, tipo de documento, número, proveedor, RUT, descripción, centro de costo, neto, IVA y total por gasto. Salta las hojas resumen y las usa como control de totales. Útil para rendiciones de caja chica, ingreso masivo y conciliación.
---

**Idioma de respuesta:** siempre en español chileno. Terminología contable/tributaria local. Todo el output (resúmenes, validaciones, mensajes de error, comentarios) en español. Solo cambiar de idioma si el usuario lo solicita explícitamente.

# Extraer rendiciones a CSV + Excel

Cuando el usuario invoca este skill (palabras gatillo: "extrae rendiciones", "rendiciones a csv", "procesa estos PDF de caja chica", "leeme las rendiciones de esta carpeta"), realiza el siguiente flujo.

## Privacidad (leer primero)

Este skill usa Claude visión: los PDFs se envían a Claude para leerlos. Pueden contener datos
tributarios reales (RUT, montos, proveedores). Procesarlos está permitido según la configuración
corporativa vigente de Taxtic. Para compartir el resultado fuera de la organización, anonimizar antes
con el skill `/anonimizar` del plugin `comun-anonimizacion`.

## Regla central — NUNCA inventar datos

- Campo inexistente → dejarlo **vacío**.
- Campo dudoso o ilegible → marcar `REVISAR` en la columna `Observacion`.
- Nunca completar un dato por intuición o por el patrón esperado. En contabilidad, un dato
  plausible-pero-falso es peor que uno ausente.

## Inputs aceptados

- Una carpeta con archivos `.pdf` (ej: `rendiciones/`).
- Una lista explícita de rutas `.pdf`.
- Un único PDF.

Si no se especifica, asumir la carpeta actual.

## Flujo

1. **Listar PDFs**: usar `Glob` con patrón `**/*.pdf` (o el path dado) y mostrar cuántos se procesarán.
   Pedir confirmación si son >50.

2. **Leer cada PDF**: usar `Read` con el PDF (lectura visual, lee impreso y manuscrito). Si `Read`
   falla por tamaño, intentar fallback de texto:
   `python -c "from pypdf import PdfReader; r=PdfReader('<path>'); print('\n'.join((p.extract_text() or '') for p in r.pages))"`.

3. **PDF no procesable**: si la lectura visual falla y el fallback `pypdf` no entrega texto útil, NO
   adivinar. Emitir una sola fila para ese archivo con `Observacion = NO_PROCESADO` y el resto de
   columnas vacías, e indicar al usuario que ese PDF debe dividirse, comprimirse o revisarse a mano.

4. **Recorrer páginas de cada PDF**:
   - **Hoja resumen "Rendición Caja Chica"** (tabla que agrupa gastos, suele ser manuscrita): NO
     emitir como gasto. Leerla como **control**: capturar el identificador de la rendición
     (número/nombre/periodo) y, si es legible, el **total rendido declarado**. Si el total no se lee,
     no inventarlo.
   - **Boleta / factura / comprobante**: extraer un gasto con su número de `Pagina`.

5. **Extraer por gasto** los campos, en este orden exacto:
   - `Archivo` — nombre del PDF.
   - `Pagina` — número de página (entero) de donde sale el gasto.
   - `Rendicion` — si se detectó identificador en la hoja resumen, usarlo; si no, el nombre base del PDF.
   - `Fecha` — formato `DD-MM-YYYY`. Convertir desde otros formatos. Si no se lee, vacío.
   - `TipoDocumento` — uno de: `FACTURA`, `FACTURA_EXENTA`, `BOLETA`, `COMPROBANTE`, o vacío.
   - `NumeroDocumento` — número del documento (string).
   - `Proveedor` — razón social/emisor tal cual aparece.
   - `RutProveedor` — formato `12345678-9` (sin puntos, con guión).
   - `Descripcion` — glosa/detalle del gasto.
   - `CentroCosto` — si aparece (centro de costo / obra / área); si no, vacío.
   - `Neto` — entero CLP, sin separadores.
   - `IVA` — entero CLP. Documento exento → `0`.
   - `Total` — entero CLP.
   - `Observacion` — observaciones de validación + `REVISAR` cuando aplique.

6. **Validar coherencia** por gasto (acumular en `Observacion`, NO descartar la fila):
   - `Total == Neto + IVA` (±1 CLP por redondeo).
   - `RutProveedor` válido por módulo 11.
   - `IVA` ≈ 19% del `Neto` cuando es afecto; si `TipoDocumento = FACTURA_EXENTA`, `IVA` debe ser 0.
   - `Fecha` no futura; si el usuario indicó periodo de la rendición, dentro de ese periodo.
   - `Total > 0`.
   - `NumeroDocumento` presente en boleta/factura.
   - **Duplicados**: misma combinación `NumeroDocumento + Proveedor + Total` en otra fila.
   - Cualquier campo dudoso/ilegible → `REVISAR`.

7. **Control vs hoja resumen** (best-effort): si se capturó un total rendido legible, comparar contra
   la suma de `Total` de los gastos extraídos de esa rendición. Si difieren, reportarlo como
   advertencia global (no bloquea, no descarta nada).

8. **Generar salida** en la carpeta de los PDFs (o el path indicado):
   - `resumen-rendiciones.csv` — UTF-8 con BOM, encabezado + una fila por gasto. Usar `Write`.
   - `resumen-rendiciones.xlsx` — generarlo desde el CSV con Python + openpyxl:
     ```
     python -c "import csv; from openpyxl import Workbook; wb=Workbook(); ws=wb.active; ws.title='Rendicion'; rows=list(csv.reader(open('resumen-rendiciones.csv', encoding='utf-8-sig'))); [ws.append(r) for r in rows]; wb.save('resumen-rendiciones.xlsx')"
     ```
     Si `openpyxl` no está instalado (ImportError), generar solo el CSV y avisar al usuario:
     "Excel omitido: instala openpyxl con `pip install openpyxl` y reintenta".

9. **Reportar resumen** al usuario:
   - N gastos extraídos.
   - Suma de Neto, suma de IVA, suma de Total.
   - Cantidad de filas con observación / `REVISAR`.
   - Hojas resumen usadas como control y diferencia vs total rendido (si se pudo comparar).
   - Archivos `NO_PROCESADO`.

## Formato CSV

```
Archivo,Pagina,Rendicion,Fecha,TipoDocumento,NumeroDocumento,Proveedor,RutProveedor,Descripcion,CentroCosto,Neto,IVA,Total,Observacion
RENDICION 283.pdf,3,283,07-04-2026,FACTURA,358,Comercial Los Andes Ltda,76086428-5,Aridos para obra,Vizcaya,1000000,190000,1190000,
RENDICION 283.pdf,4,283,09-04-2026,BOLETA,9912,Minimarket El Sol,77654321-2,Insumos oficina,Oficina,5000,950,5950,
documento-ilegible.pdf,,,,,,,,,,,,,NO_PROCESADO
```

Encoding UTF-8 con BOM (compatibilidad Excel chileno).

## Limitaciones

- La precisión depende de la calidad del escaneo. Lo dudoso queda `REVISAR` para revisión humana.
- El total de la hoja resumen suele ser manuscrito: la comparación es referencial, no un bloqueo.
- No reemplaza el criterio del contador; revisar antes de contabilizar.
