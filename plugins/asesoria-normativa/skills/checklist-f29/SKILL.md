---
name: checklist-f29
description: Genera un checklist de revisión pre-envío del Formulario 29 (IVA y retenciones mensual) según el giro y características del cliente. Útil para evitar errores comunes en cierres mensuales.
---

# Checklist F29

Cuando el usuario invoca este skill (palabras gatillo: "checklist F29", "qué reviso antes de declarar F29", "F29 cierre mensual"), genera un checklist contextualizado.

## Inputs

Información del cliente:
- Giro (comercio, servicios, construcción, agricultura, etc.).
- Régimen tributario (ProPyme General, ProPyme Transparente, 14A semi-integrado, etc.).
- Características especiales (exportador, retenedor de honorarios, gran contribuyente, etc.).

Si el usuario no especifica, pedirle estos datos antes de generar el checklist.

## Flujo

Genera un checklist en formato Markdown con las siguientes secciones:

```markdown
# Checklist F29 — <Cliente> — período <YYYY-MM>

**Giro:** ...
**Régimen:** ...

## Ventas (débito fiscal)
- [ ] Suma de facturas electrónicas emitidas cuadra con libro ventas
- [ ] Boletas electrónicas registradas en RVD/RES
- [ ] Notas de crédito aplicadas correctamente
- [ ] Exportaciones declaradas en código correcto (si aplica)
- [ ] Ventas exentas separadas

## Compras (crédito fiscal)
- [ ] Suma de facturas recibidas cuadra con libro compras
- [ ] Crédito fiscal solo de facturas relacionadas al giro
- [ ] Facturas de bienes uso (depreciable) registradas
- [ ] Notas de crédito recibidas
- [ ] Facturas de retención emitidas (si retenedor)

## Honorarios (si aplica)
- [ ] Total boletas de honorarios recibidas
- [ ] Retención 13.75% (2026) aplicada
- [ ] PPM honorarios (10% trabajadores independientes propios)

## PPM y otros
- [ ] PPM calculado según tasa vigente
- [ ] PPM ProPyme (0.25% o 0.5% según régimen)

## Ajustes finales
- [ ] Remanente crédito fiscal mes anterior aplicado
- [ ] Saldo a favor o a pagar coherente con libro
- [ ] Firma electrónica vigente

## Específico al giro <giro>
[Items adicionales según giro]
```

Ajusta los items según el giro y régimen.

## Limitaciones

- Checklist genérico. Cliente con casos especiales (zonas francas, IFC, etc.) requiere ampliación manual.
