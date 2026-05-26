---
name: clasificar-cuentas
description: Sugiere cuenta contable según el Plan Único de Cuentas chileno (PUC) para cada factura o glosa. Acepta CSV de facturas o lista de glosas. Devuelve sugerencia con código de cuenta y confianza.
---

**Idioma de respuesta:** siempre en español chileno. Terminología contable/tributaria local. Todo el output (resúmenes, validaciones, mensajes de error, comentarios) en español. Solo cambiar de idioma si el usuario lo solicita explícitamente.

# Clasificar facturas a cuenta contable

Cuando el usuario invoca este skill (palabras gatillo: "clasifica estas facturas", "qué cuenta uso", "sugiere cuenta contable"), aplica el siguiente flujo.

## Inputs aceptados

- Un CSV generado por `/extractor-facturas` (con columna `razon_social` y opcionalmente `glosa`).
- Una lista de glosas en texto plano.
- Una sola glosa.

## Catálogo de cuentas mínimo (Plan Único de Cuentas chileno)

Usar este catálogo como base. Si el usuario tiene un PUC propio, pedirlo y usarlo en su lugar.

| Código | Cuenta | Categoría sugerida (palabras clave) |
|---|---|---|
| 4101 | Compras de mercaderías | mercadería, producto reventa |
| 5101 | Sueldos y salarios | nómina, sueldo, remuneración |
| 5102 | Honorarios | boleta honorarios, consultor independiente |
| 5201 | Arriendos | arriendo, alquiler, leasing |
| 5301 | Servicios básicos | electricidad, agua, gas, internet |
| 5302 | Telefonía | telefono, móvil, celular, plan datos |
| 5401 | Combustibles | bencina, diesel, petróleo |
| 5501 | Material de oficina | papelería, oficina, suministros |
| 5601 | Mantención vehículos | taller, repuesto auto, mantención flota |
| 5701 | Asesorías profesionales | abogado, contador externo, consultoría |
| 5801 | Publicidad | marketing, publicidad, redes sociales |
| 5901 | Gastos bancarios | comisión banco, interés |

## Flujo

1. Para cada factura/glosa, evaluar la `razon_social` y `glosa` (si existe) contra las palabras clave del catálogo.
2. Sugerir la cuenta con mayor match. Confianza: alta (>2 keywords match), media (1 keyword), baja (sin match — sugerir "manual").
3. Si es CSV, devolver el mismo CSV con dos columnas adicionales: `cuenta_sugerida`, `confianza`.
4. Si son glosas sueltas, devolver tabla.

## Privacidad

Misma advertencia del skill `/extractor-facturas`.

## Limitaciones

- Catálogo mínimo, no reemplaza criterio del contador.
- Marcar siempre las sugerencias para revisión humana antes de contabilizar.
