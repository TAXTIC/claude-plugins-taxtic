---
name: resumen-circular-sii
description: Genera un resumen estructurado de una circular, resolución o documento normativo del SII (Servicio de Impuestos Internos chileno) en formato PDF o URL pública. Extrae - tema, alcance, fecha vigencia, principales obligaciones, impactos prácticos para contadores, contribuyentes afectados, plazos clave.
---

**Idioma de respuesta:** siempre en español chileno. Terminología contable/tributaria local. Todo el output (resúmenes, validaciones, mensajes de error, comentarios) en español. Solo cambiar de idioma si el usuario lo solicita explícitamente.

# Resumen circular SII

Cuando el usuario invoca este skill (palabras gatillo: "resume esta circular SII", "qué dice esta resolución", "impacto de esta normativa"), aplica el siguiente flujo.

## Inputs

- Path a PDF local del documento.
- URL pública del SII (ej: https://www.sii.cl/normativa_legislacion/...).
- Texto pegado directamente.

## Flujo

1. Si es PDF: leer con tool `Read`. Si falla por tamaño, usar `python -c "from pypdf import PdfReader; r = PdfReader('...'); print(...)"`.
2. Si es URL: usar tool `WebFetch` para obtener contenido.
3. Si es texto: usar directamente.

4. Estructurar el resumen en este formato exacto:

```markdown
# Resumen — <Título o número de circular>

**Fuente:** [path o URL]
**Fecha publicación:** [si está disponible]
**Vigencia:** [fecha desde / hasta si está]

## Tema central

[1-2 oraciones]

## Alcance

[Quiénes son afectados: contribuyentes, retenedores, agentes, etc.]

## Principales obligaciones

1. ...
2. ...
3. ...

## Impactos prácticos para contadores Taxtic

- **Asesoría:** [acciones recomendadas]
- **Contabilidad:** [ajustes operativos]
- **RRHH:** [si aplica]

## Plazos clave

| Plazo | Acción |
|---|---|
| ... | ... |

## Riesgos / sanciones

[Multas o consecuencias por incumplimiento]

## Recomendación general

[1-2 oraciones accionables]
```

5. Guardar como `resumen-circular-<numero>.md`.

## Limitaciones

- La interpretación normativa es referencial. Para casos específicos, validar con abogado tributario.
- El SII publica modificaciones; verifica que la circular esté vigente.
