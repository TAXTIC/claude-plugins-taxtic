---
name: anonimizar
description: Anonimiza datos sensibles chilenos en texto, archivos o snippets - RUTs (con o sin guión, con o sin DV), nombres de personas o empresas, y montos. Útil ANTES de pegar contenido en chats, prompts o documentos compartidos.
---

# Anonimizar datos sensibles

Cuando el usuario invoca este skill (palabras gatillo: "anonimiza", "anonimizar", "limpia datos", "saca el RUT", "tapa nombres"), aplica las siguientes transformaciones al texto, archivo o snippet entregado.

## Reglas de reemplazo

1. **RUTs chilenos** — patrón regex: `\b\d{1,2}\.?\d{3}\.?\d{3}-?[\dkK]\b` o `\b\d{7,8}-?[\dkK]\b`.
   - Reemplazar por `11111111-1` (primer RUT) → `22222222-2` (segundo distinto) → `33333333-3` (tercero distinto), etc.
   - Mantener mapeo consistente: el mismo RUT original mapea siempre al mismo dummy en la misma operación.

2. **Nombres propios de personas** — detectar por contexto (capitalización, palabras como "don", "doña", "Sr.", "Sra.", "el cliente", o asociadas a RUT).
   - Reemplazar por `Cliente A`, `Cliente B`, `Cliente C`, etc., también con mapeo consistente.
   - NO reemplazar nombres de meses, días, lugares públicos.

3. **Nombres de empresas** — detectar por contexto (terminaciones SpA, S.A., Ltda., E.I.R.L.).
   - Reemplazar por `Empresa Alfa`, `Empresa Beta`, `Empresa Gamma`, etc.

4. **Montos** — números > 10.000 con o sin separador de miles, opcionalmente con `$` o `CLP`.
   - Reemplazar por rangos: `$X` (X = orden de magnitud, ej: `$~100K`, `$~1M`, `$~10M`).
   - No anonimizar porcentajes ni números pequeños (IVA 19%, cuotas, etc.).

5. **Direcciones, teléfonos, emails** — si el usuario los menciona, también reemplazarlos por `<dirección>`, `<teléfono>`, `<email>`.

## Formato de salida

Devuelve el texto anonimizado en un bloque de código, seguido de una tabla resumen del mapeo aplicado (original → dummy) en formato compacto. Cierra con un recordatorio: "Verifica el resultado antes de usar."

## Ejemplo

Input del usuario:
```
El cliente Juan Pérez Soto, RUT 12.345.678-9, de Constructora Andes SpA, debe pagar $4.500.000 antes del 30.
```

Output esperado:
```
El cliente Cliente A, RUT 11111111-1, de Empresa Alfa, debe pagar $~5M antes del 30.

Mapeo aplicado:
- Juan Pérez Soto → Cliente A
- 12.345.678-9 → 11111111-1
- Constructora Andes SpA → Empresa Alfa
- $4.500.000 → $~5M

Verifica el resultado antes de usar.
```
