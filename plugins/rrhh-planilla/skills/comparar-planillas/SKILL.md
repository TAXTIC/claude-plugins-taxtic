---
name: comparar-planillas
description: Compara dos planillas de remuneraciones (mes anterior vs mes actual) y reporta variaciones significativas - trabajadores nuevos, bajas, variaciones de sueldo > umbral configurable (default 5%), variaciones en descuentos y cambios de AFP/salud.
---

# Comparar planillas

Cuando el usuario invoca este skill (palabras gatillo: "compara planillas", "diferencias mes a mes", "qué cambió en la planilla"), aplica el siguiente flujo.

## Inputs

- Path a planilla mes anterior (CSV o Excel).
- Path a planilla mes actual.
- Umbral de variación en % (default 5).

Ambas con columnas mínimas: `rut`, `nombre`, `total_haberes`, `total_descuentos`, `liquido_pagar`.

## Flujo

1. Leer ambos archivos.
2. Match por `rut`.
3. Categorizar:

### Categorías

**NUEVOS:** presentes en actual, ausentes en anterior.
**BAJAS:** presentes en anterior, ausentes en actual.
**VARIACIÓN ALTA:** match, diferencia `liquido_pagar` > umbral%.
**SIN CAMBIO:** match, diferencia ≤ umbral%.

4. Generar reporte:

```markdown
# Comparación planilla — <mes_actual> vs <mes_anterior>

## Nuevos ingresos (X)
- 11.111.111-1 — Cliente A — líquido $980.000

## Bajas (Y)
- 22.222.222-2 — Cliente B — último líquido $1.200.000

## Variaciones > 5% (Z)
- 33.333.333-3 — Cliente C — anterior $850.000, actual $1.050.000 (+23.5%).

## Sin cambios (W)
[resumen numérico, no listado]
```

5. Guardar como `comparacion-<mes_actual>.md`.

## Privacidad

Mismas advertencias que `/validar-planilla`.
