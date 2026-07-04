"""Fuente de verdad de códigos SII. Cada 'fuente' cita el instructivo o el
formulario oficial del SII del que sale la semántica, para que la regla sea
auditable y no dependa de la memoria del que la escribió.

Las citas apuntan al formulario oficial y a las instrucciones oficiales
publicadas en sii.cl (Formulario 22 AT2026 y Formulario 29), que son las
fuentes primarias para la semántica de estos códigos.

Estructura de cada entrada:
  - "glosa":   descripción del código.
  - "fuente":  cita auditable (formulario/instructivo oficial + recuadro/línea).
  - "aliases": formas textuales aceptadas del código. El formulario oficial
               muestra 48/77/89/92/93/94 SIN cero inicial; el módulo acepta
               ambas formas (con y sin cero inicial) vía aliases, para que
               los consumidores no tengan que normalizar el texto de entrada.
  - "aplica":  (opcional) regímenes tributarios en que el código es válido.
"""

F22 = {
    "122": {"glosa": "Total del Activo (columna activo del balance)",
            "fuente": "SII Formulario 22 AT 2026, recuadro Datos de Balance "
                       "(formulario oficial sii.cl/ayudas/formularios/f22_at2026.pdf, p.2)",
            "aliases": ["122"]},
    "123": {"glosa": "Total columna Pasivo del balance, sin utilidad del ejercicio",
            "fuente": "SII F22 AT2026, Recuadro N°6 Datos de Balance, p.2; e Instrucciones "
                       "oficiales SII código 123 (total pasivo sin considerar utilidad del ejercicio)",
            "aliases": ["123"]},
    "101": {"glosa": "Saldo de caja según balance y arqueo",
            "fuente": "SII Formulario 22 AT 2026, recuadro Datos de Balance, glosa "
                       "'Saldo de caja (sólo dinero en efectivo y documentos al día, según arqueo)' "
                       "(formulario oficial sii.cl/ayudas/formularios/f22_at2026.pdf, p.2)",
            "aliases": ["101"]},
    "843": {"glosa": "Patrimonio financiero (residual de activos deducidos pasivos exigibles)",
            "fuente": "SII Formulario 22 AT 2026, recuadro Datos de Balance, glosa "
                       "'Patrimonio financiero' (formulario oficial sii.cl/ayudas/formularios/f22_at2026.pdf, p.2)",
            "aliases": ["843"]},
    # 645/646 (CPT positivo/negativo final) son válidos SOLO para los regímenes
    # 14A y 14G. NO generalizar a 14D N°3 ni 14D N°8: esos regímenes tienen sus
    # propios recuadros de CPTS (Capital Propio Tributario Simplificado).
    "645": {"glosa": "CPT positivo final",
            "fuente": "SII F22 AT2026, Recuadro N°14 Razonabilidad Capital Propio Tributario, p.6",
            "aliases": ["645"],
            "aplica": ["14A", "14G"]},
    "646": {"glosa": "CPT negativo final",
            "fuente": "SII F22 AT2026, Recuadro N°14 Razonabilidad Capital Propio Tributario, p.6",
            "aliases": ["646"],
            "aplica": ["14A", "14G"]},
    # NOTA: 305 es dato de resultado de la liquidación anual del impuesto a la
    # renta. NO se usa en reconciliaciones de balance; solo alimenta la alerta
    # PPM_DEVOLUCION (resultado negativo = saldo a favor / devolución).
    "305": {"glosa": "Resultado liquidación anual impuesto a la renta (negativo = saldo a favor / devolución)",
            "fuente": "SII Formulario 22 AT 2026 (anverso), recuadro Resultado Liquidación Anual Impuesto a la Renta "
                       "(formulario oficial sii.cl/ayudas/formularios/f22_at2026.pdf, p.15)",
            "aliases": ["305"]},
}

F29 = {
    "538": {"glosa": "Total débitos",
            "fuente": "SII Formulario 29, línea 23, Cód.538 "
                       "(Instrucciones oficiales F29, sii.cl/servicios_online/instrucciones_f29_20241112.pdf)",
            "aliases": ["538"]},
    "537": {"glosa": "Total créditos",
            "fuente": "SII Formulario 29, línea 49, Cód.537 "
                       "(Instrucciones oficiales F29, sii.cl/servicios_online/instrucciones_f29_20241112.pdf)",
            "aliases": ["537"]},
    "077": {"glosa": "Remanente de crédito fiscal",
            "fuente": "SII Formulario 29, línea 50, Cód.77 (remanente para el mes siguiente) "
                       "(Instrucciones oficiales F29, sii.cl/servicios_online/instrucciones_f29_20241112.pdf)",
            "aliases": ["077", "77"]},
    "089": {"glosa": "IVA determinado",
            "fuente": "SII Formulario 29, línea 50, Cód.89 (impuesto IVA determinado) "
                       "(Instrucciones oficiales F29, sii.cl/servicios_online/instrucciones_f29_20241112.pdf)",
            "aliases": ["089", "89"]},
    "547": {"glosa": "Total determinado (incluye retenciones art.74, NO es IVA)",
            "fuente": "SII Formulario 29, línea 134, Cód.547 (suma líneas 80 a 133, columna Impuesto Determinado) "
                       "(Instrucciones oficiales F29, sii.cl/servicios_online/instrucciones_f29_20241112.pdf)",
            "aliases": ["547"]},
    "048": {"glosa": "Retención impuesto único trabajadores art.74",
            "fuente": "SII Formulario 29, línea 60, Cód.48, glosa 'Retención Impuesto Único a los Trabajadores, "
                       "según Art. 74 N°1 LIR' (Instrucciones oficiales F29, "
                       "sii.cl/servicios_online/instrucciones_f29_20241112.pdf)",
            "aliases": ["048", "48"]},
    "092": {"glosa": "Más IPC",
            "fuente": "SII Formulario 29, línea 142, Cód.92, glosa 'Más IPC' "
                       "(formulario oficial sii.cl/formularios/imagen/F29.pdf, p.3)",
            "aliases": ["092", "92"]},
    "093": {"glosa": "Más interés y multas",
            "fuente": "SII Formulario 29, línea 143, Cód.93, glosa 'Más Intereses y multas' "
                       "(formulario oficial sii.cl/formularios/imagen/F29.pdf, p.3)",
            "aliases": ["093", "93"]},
    "094": {"glosa": "Total a pagar con recargo",
            "fuente": "SII Formulario 29, línea 144, Cód.94, glosa 'TOTAL A PAGAR CON RECARGO' "
                       "(formulario oficial sii.cl/formularios/imagen/F29.pdf, p.3)",
            "aliases": ["094", "94"]},
}
