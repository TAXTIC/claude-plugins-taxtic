---
name: conciliacion-bancaria
description: Compara una cartola bancaria (CSV) con un libro mayor o auxiliar (CSV) y reporta movimientos sin match, diferencias de monto y posibles duplicados. Útil para cierre mensual.
---

# Conciliación bancaria

Cuando el usuario invoca este skill (palabras gatillo: "concilia cartola", "conciliación bancaria", "matchea cartola y libro"), aplica el siguiente flujo.

## Inputs

- Cartola bancaria CSV con al menos: `fecha`, `descripcion`, `monto` (positivo = abono, negativo = cargo).
- Libro contable CSV con al menos: `fecha`, `glosa`, `debe`, `haber` (o un único `monto` con signo).
- Tolerancia de fechas en días (default 3) y de montos en CLP (default 100).

## Flujo

1. Leer ambos CSV con tool `Read`.
2. Para cada movimiento de cartola, buscar coincidencia en libro:
   - Match si: monto coincide (dentro de tolerancia) Y fecha dentro de ventana ±N días.
   - Marcar como `MATCH`, `MATCH_PARCIAL` (monto OK, fecha fuera) o `SIN_MATCH`.
3. Para cada movimiento de libro sin contraparte en cartola: marcar `SOLO_LIBRO`.
4. Generar reporte CSV `conciliacion-<fecha>.csv` con columnas:
   - `origen` (CARTOLA o LIBRO)
   - `fecha`, `monto`, `descripcion`/`glosa`
   - `estado` (MATCH, MATCH_PARCIAL, SIN_MATCH, SOLO_LIBRO)
   - `fila_relacionada` (índice de la fila contraparte si aplica)
5. Reportar al usuario:
   - Total movimientos cartola / libro
   - Total matches
   - Total sin match (acción requerida)
   - Suma de diferencias

## Privacidad

Los CSVs contienen información financiera sensible. No compartir fuera de la organización.

## Limitaciones

- Match es heurístico (monto + fecha). No interpreta descripciones.
- Para casos complejos (un movimiento bancario = varios en libro): marcar y pedir revisión manual.
