import importlib.util, os
def _load(name):
    spec = importlib.util.spec_from_file_location(name,
        os.path.join(os.path.dirname(__file__), "..", "scripts", name + ".py"))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
pf = _load("parse_f29")

# Texto sintético con la forma del F29 real (RUT y montos FALSOS).
TEXTO = """FORMULARIO 29
RUT [03] 11.111.111-1
PERIODO [15] 202605
537 TOTAL CREDITOS 500.000
077 REMANENTE DE CREDITO FISC. 500.000
089 IMP. DETERM. IVA 0
048 RET. IMP. UNICO TRAB. ART. 74 N 1 LIR 300.000
547 TOTAL DETERMINADO 300.000
094 TOTAL A PAGAR CON RECARGO 0
Fecha de Presentacion 15/06/2026
"""

def test_extrae_codigos_como_datos_trazados():
    r = pf.parse_f29_text(TEXTO, "F29_fake.pdf", 1)
    assert r["codigos"]["537"]["valor"] == 500000
    assert r["codigos"]["537"]["archivo"] == "F29_fake.pdf"
    assert "500.000" in r["codigos"]["537"]["texto_cercano"]
    assert r["periodo"] == "2026-05"

def test_codigo_ausente_es_none_no_error():
    r = pf.parse_f29_text(TEXTO, "F29_fake.pdf", 1)
    assert r["codigos"]["538"] is None   # sin débitos ese mes

def test_547_no_se_confunde_con_iva():
    r = pf.parse_f29_text(TEXTO, "F29_fake.pdf", 1)
    assert r["codigos"]["547"]["valor"] == 300000   # total determinado
    assert r["codigos"]["089"]["valor"] == 0        # IVA real

def test_recargo_cero_no_marca():
    r = pf.parse_f29_text(TEXTO, "F29_fake.pdf", 1)
    assert r["codigos"]["094"]["valor"] == 0
