---
name: validar-planilla
description: Valida una planilla de remuneraciones CSV o Excel. Revisa totales, descuentos legales chilenos (AFP, salud, seguro cesantía, impuesto único de segunda categoría), formato Previred, y completitud de campos obligatorios.
---

**Idioma de respuesta:** siempre en español chileno. Terminología contable/tributaria local. Todo el output (resúmenes, validaciones, mensajes de error, comentarios) en español. Solo cambiar de idioma si el usuario lo solicita explícitamente.

# Validar planilla de remuneraciones

Cuando el usuario invoca este skill (palabras gatillo: "valida planilla", "revisa nómina", "chequea remuneraciones"), aplica el siguiente flujo.

## Inputs

Archivo CSV o Excel con al menos las siguientes columnas (acepta variantes de nombre):
- `rut` (trabajador)
- `nombre`
- `sueldo_base`
- `gratificacion` (opcional)
- `total_haberes`
- `afp` (descuento)
- `salud` (descuento)
- `seguro_cesantia` (descuento, opcional)
- `impuesto_unico` (opcional)
- `total_descuentos`
- `liquido_pagar`

## Flujo

1. Leer el archivo con tool `Read`.
2. Para cada trabajador, validar:

### Validaciones

**ESTRUCTURA:**
- Todas las columnas obligatorias presentes.
- RUT válido (módulo 11).
- Sin filas duplicadas (mismo RUT).

**ARITMÉTICA:**
- `total_haberes` = suma de haberes individuales (±1 CLP por redondeo).
- `total_descuentos` = suma de descuentos individuales.
- `liquido_pagar` = `total_haberes` - `total_descuentos`.

**LEGAL (rangos típicos 2026, ajustables):**
- AFP entre 10% y 12.5% del imponible (varía por administradora, considerar como sensor de alerta no de bloqueo).
- Salud ≥ 7% del imponible (Fonasa) o monto pactado Isapre.
- Seguro cesantía 0.6% trabajador + 2.4% empleador (validar solo trabajador en planilla).
- Tope imponible AFP: 87.8 UF (2026) — alertar si imponible > tope.

**TOPE NO IMPONIBLE:**
- Asignación colación, movilización: alertar si sospechosamente alto (>20% del sueldo base).

3. Generar reporte Markdown estructurado:

```markdown
# Reporte validación planilla — <archivo>

Trabajadores: N

## Errores estructurales (X)
- Fila 5: RUT inválido (10.123.456-9 no pasa módulo 11).

## Errores aritméticos (Y)
- Fila 3 (RUT 11.111.111-1): total_haberes declarado $1.200.000, suma individual $1.180.000 (diferencia $20.000).

## Alertas legales (Z)
- Fila 8: AFP 8% (esperado 10-12.5%).

## OK

Trabajadores sin observaciones: M / N.
```

4. Guardar reporte y resumir al usuario.

## Privacidad

Planillas contienen sueldos identificables. NO compartir fuera del equipo RRHH.

## Limitaciones

- Tasas legales son referenciales 2026. Para producción, configurar tabla actualizada.
- No reemplaza revisión humana del encargado RRHH.
