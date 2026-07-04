# asesoria-informe-tributario

Plugin para generar el informe tributario anual de un cliente (F29, F22, balance, ficha, malla)
en Word + Excel, con marca Taxtic, para el equipo Taxtic.

## ⚠️ Privacidad

Los documentos de entrada traen datos tributarios reales (RUT, montos, razón social). Su
procesamiento está permitido según la configuración corporativa vigente de Taxtic. Para compartir
el informe generado **fuera de la organización**, anonimiza primero con `/anonimizar` (plugin
`comun-anonimizacion`).

## Qué hace

- **Skill `/informe-tributario`** (orquestador, dos fases):
  1. **Extracción determinista**: parsers Python leen los PDF/Excel del cliente y arman un
     `datos.json` con cifras exactas — ningún número lo escribe la IA a mano.
  2. **Síntesis**: se redacta la prosa del informe usando **placeholders** (`{{token}}`) que
     apuntan a las cifras extraídas. La generación final del `.docx`/`.xlsx` corre por CLI y
     **aborta** si detecta un monto tecleado literal o un token inexistente — es la garantía
     anti-alucinación: ninguna cifra del informe puede haber sido inventada por el modelo.
- Reconciliaciones automáticas (ej. balance ↔ F22), alertas deterministas sobre inconsistencias, y
  trazabilidad: cada cifra del informe queda vinculada al archivo/página de origen.

## Instalación

```
/plugin install asesoria-informe-tributario@plugins-taxtic
```

## Requisitos

Python 3.12 y las dependencias del plugin:

```
pip install -r requirements.txt
```

(`pypdf`, `pdfplumber`, `openpyxl`, `python-docx`, `pytest`).

## Uso

Ubicate en (o indicá) la carpeta con los documentos del cliente — F29 mensuales, F22 anuales,
balance en PDF, ficha (`Datos*.xlsx`) y malla (`Malla*.xlsx`) — e invocá:

```
/informe-tributario
[indicar carpeta del cliente si no es la actual, ej: ./clientes/acme-spa/]
```

Si la carpeta tiene documentos de más de un cliente, el skill pregunta a cuál referirse antes de
procesar. Si algún archivo no se puede parsear, se marca `NO_PROCESADO` y se sigue con el resto;
al final se informa qué se procesó y qué no.

## Qué genera

En la carpeta del cliente:

- `informe.docx` — informe tributario redactado por secciones (ficha, malla, F22 comparativo,
  cadena IVA F29, PPM/retenciones/recargos, balance + conciliación, inconsistencias, alertas y
  oportunidades, resumen ejecutivo).
- `anexo.xlsx` — detalle tabular de las cifras que respaldan el informe.
- `datos.json` — extracción intermedia (útil para auditar de dónde salió cada cifra).

## Limitaciones (v1)

- No procesa escritura societaria (documentos extensos, ~100 páginas) ni la Consulta Integral SII
  en formato imagen (PNG) — quedan fuera del alcance de esta versión; se planea soporte con
  agentes de visión más adelante.
- No incluye cruces aproximados que requieren juicio contable (ej. F29↔F22 de ingresos, malla↔
  escritura); esos se dejan para revisión manual.

## Versión

0.1.0
