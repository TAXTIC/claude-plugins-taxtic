# contabilidad-facturas

Plugin de procesamiento de facturas PDF para el equipo Taxtic.

## Componentes

- **Skill `/extractor-facturas`** — PDFs de facturas → CSV estructurado.
- **Skill `/clasificar-cuentas`** — sugiere cuenta contable (PUC chileno) para cada factura.
- **Agent `auditor-facturas`** — revisa coherencia de un CSV de facturas ya extraído.

## Instalación

```
/plugin install contabilidad-facturas@plugins-taxtic
```

## Uso

```
/extractor-facturas
[indicar carpeta con PDFs, ej: ./facturas-octubre/]
```

Genera `resumen-facturas.csv` en la carpeta indicada.

## Dependencias

- Python 3.10+ con `pypdf` instalado (fallback si `Read` no puede con el PDF).

## Versión

0.1.0
