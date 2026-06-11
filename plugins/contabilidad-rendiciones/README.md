# contabilidad-rendiciones

Plugin de procesamiento de rendiciones de caja chica (PDF) para el equipo Taxtic.

## ⚠️ Privacidad

Este plugin usa **Claude visión**: los PDFs se envían a Claude para leerlos. Pueden contener datos
tributarios reales (RUT, montos, proveedores). Su procesamiento está permitido según la configuración
corporativa vigente de Taxtic. Para compartir resultados **fuera de la organización**, anonimiza
primero con `/anonimizar` (plugin `comun-anonimizacion`).

## Componentes

- **Skill `/extractor-rendiciones`** — PDFs de caja chica → `resumen-rendiciones.csv` + `.xlsx`.
  Salta las hojas resumen y las usa como control de totales.
- **Agent `auditor-rendiciones`** — audita el CSV: resumen global + hallazgos CRÍTICO/ADVERTENCIA/INFO.

## Instalación

```
/plugin install contabilidad-rendiciones@plugins-taxtic
```

## Uso

```
/extractor-rendiciones
[indicar carpeta con PDFs, ej: ./rendiciones/]
```

Genera `resumen-rendiciones.csv` y `resumen-rendiciones.xlsx` en la carpeta indicada. Luego, para
auditar:

```
[invocar al agente auditor-rendiciones sobre resumen-rendiciones.csv]
```

## Columnas del CSV/Excel

`Archivo, Pagina, Rendicion, Fecha, TipoDocumento, NumeroDocumento, Proveedor, RutProveedor,
Descripcion, CentroCosto, Neto, IVA, Total, Observacion`.

## Dependencias

- Python 3.10+ con `pypdf` (fallback si `Read` no puede con el PDF).
- `openpyxl` para generar el Excel (`pip install openpyxl`). Sin él, se genera solo el CSV.

## Versión

0.1.0
