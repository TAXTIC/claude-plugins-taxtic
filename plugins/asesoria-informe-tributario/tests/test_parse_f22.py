import importlib.util, os
def _load(name):
    spec = importlib.util.spec_from_file_location(name,
        os.path.join(os.path.dirname(__file__), "..", "scripts", name + ".py"))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
pf = _load("parse_f22")

TEXTO = """FORM. 22 AÑO TRIBUTARIO 2026
122 1.000.000 Total del Activo
123 700.000 Total del Pasivo
843 900.000 Patrimonio financiero
101 50.000 Saldo de caja
646 0 CPT negativo final
"""

def test_extrae_codigos():
    r = pf.parse_f22_text(TEXTO, "F22_fake.pdf")
    assert r["anio"] == 2026
    assert r["codigos"]["122"]["valor"] == 1000000
    assert r["codigos"]["843"]["valor"] == 900000

def test_derivados():
    r = pf.parse_f22_text(TEXTO, "F22_fake.pdf")
    assert r["derivados"]["pasivo_exigible"] == 100000     # 122 - 843
    assert r["derivados"]["resultado_ejercicio"] == 300000 # 122 - 123

# Layout real: el PDF concatena varios pares código/valor sin separador en una
# línea. El valor de un código es el número que le SIGUE, no el del código previo.
# Regresión de la desviación `line[m.end():]` (datos FALSOS).
TEXTO_CONCATENADO = "102 3.276.111.486Capital 122 1.000.000Total del Activo"

def test_valor_por_codigo_no_toma_el_del_codigo_anterior():
    r = pf.parse_f22_text(TEXTO_CONCATENADO, "F22_fake.pdf")
    assert r["codigos"]["122"]["valor"] == 1000000  # NO 3276111486 del código previo

# Montos negativos (ej. cód. 305 resultado liquidación) deben preservar el signo.
TEXTO_NEGATIVO = "305 -742.806Resultado liquidacion"

def test_preserva_signo_negativo():
    r = pf.parse_f22_text(TEXTO_NEGATIVO, "F22_fake.pdf")
    assert r["codigos"]["305"]["valor"] == -742806
