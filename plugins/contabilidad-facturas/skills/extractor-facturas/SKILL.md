---
name: extractor-facturas
description: Extrae datos estructurados de uno o varios PDFs de facturas chilenas (electrónicas o impresas escaneadas) a CSV. Detecta número, fecha de emisión, RUT proveedor, razón social, neto, IVA y total. Útil para ingreso masivo, declaración F29, conciliación con libro de compras.
---

# Extraer facturas a CSV

Cuando el usuario invoca este skill (palabras gatillo: "extrae facturas", "facturas a csv", "procesa estos PDFs", "leeme las facturas de esta carpeta"), realiza el siguiente flujo.

## Inputs aceptados

- Una carpeta con archivos `.pdf` (ej: `facturas-octubre/`).
- Una lista explícita de rutas `.pdf`.
- Un único PDF.

Si no se especifica, asume la carpeta actual.

## Flujo

1. **Listar PDFs**: usar el tool `Glob` con patrón `**/*.pdf` (o el path dado) y mostrar al usuario cuántos se procesarán. Pedir confirmación si son >50.

2. **Leer cada PDF**: usar el tool `Read` con cada PDF. Si Read falla por tamaño, usar Bash con `python -c "from pypdf import PdfReader; r = PdfReader('<path>'); print(''.join(p.extract_text() for p in r.pages))"`.

3. **Extraer por factura** los siguientes campos (en este orden exacto):
   - `numero_factura` — número de la factura/boleta (string, ej: "12345").
   - `fecha_emision` — formato `YYYY-MM-DD`. Si la fecha viene como DD/MM/YYYY, convertir.
   - `rut_proveedor` — formato `12345678-9` (sin puntos, con guión).
   - `razon_social` — nombre del proveedor tal cual aparece.
   - `neto` — número entero (CLP), sin separadores.
   - `iva` — número entero (CLP). Si no aparece, calcular como `round(neto * 0.19)`.
   - `total` — número entero (CLP).

4. **Validar coherencia mínima** por cada factura:
   - `total == neto + iva` (±1 por redondeo).
   - `iva` entre 18% y 20% del neto.
   - Si alguna validación falla, agregar columna `_observacion` con el problema, pero NO descartar la fila.

5. **Generar CSV** con encabezado y una fila por factura. Usar tool `Write` para guardar como `resumen-facturas.csv` en la misma carpeta de los PDFs (o el path que indique el usuario).

6. **Reportar resumen** al usuario:
   - N facturas procesadas
   - Suma de netos
   - Suma de IVA
   - Suma de totales
   - Cantidad de filas con observación

## Formato CSV

```
numero_factura,fecha_emision,rut_proveedor,razon_social,neto,iva,total,_observacion
12345,2026-05-12,76543210-1,Proveedor Alfa SpA,1000000,190000,1190000,
12346,2026-05-13,77654321-2,Proveedor Beta Ltda,500000,95000,595000,
```

Encoding UTF-8 con BOM (compatibilidad Excel chileno).

## Privacidad

Los datos extraídos contienen RUTs de proveedores reales. NO compartir el CSV en chats fuera de la organización sin anonimizar primero (ver skill `/anonimizar` del plugin `comun-anonimizacion`).
