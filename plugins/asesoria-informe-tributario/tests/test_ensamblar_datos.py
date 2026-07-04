import importlib.util, os
def _load(name):
    spec = importlib.util.spec_from_file_location(name,
        os.path.join(os.path.dirname(__file__), "..", "scripts", name + ".py"))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
ea = _load("ensamblar_datos")

# Todos los datos de este archivo son SINTÉTICOS (repo público, cero data real de cliente).

def _f22_falso(anio=2099, pe=100, rej=300):
    return {
        "anio": anio,
        "codigos": {
            "843": {"valor": 900, "archivo": "F22_fake.pdf", "pagina": 1,
                     "texto_cercano": "843 900 Patrimonio financiero"},
            "122": {"valor": 1000, "archivo": "F22_fake.pdf", "pagina": 1,
                     "texto_cercano": "122 1.000 Total del Activo"},
        },
        "derivados": {"pasivo_exigible": pe, "resultado_ejercicio": rej},
    }

def _balance_falso(patrimonio=850):
    return {
        "total_activo_sii": 1000,
        "total_pasivo_columna_sii_sin_utilidad_ejercicio": 700,
        "patrimonio_financiero": patrimonio,
        "saldo_caja": 50,
    }

def _f29_falso(periodo="2099-01", valor=500):
    return {
        "periodo": periodo,
        "codigos": {"077": {"valor": valor, "archivo": "F29_fake.pdf", "pagina": 1,
                             "texto_cercano": "077 500 Remanente"}},
    }


def test_tokens_f22_codigos_y_derivados():
    f22 = _f22_falso()
    tokens = ea.construir_tokens({"f22": [f22], "f29": [], "balance": {}})
    assert tokens["f22.2099.843"]["valor"] == 900
    assert tokens["f22.2099.122"]["valor"] == 1000
    assert tokens["f22.2099.pasivo_exigible"]["valor"] == 100
    assert tokens["f22.2099.resultado_ejercicio"]["valor"] == 300

def test_tokens_balance_escalares():
    tokens = ea.construir_tokens({"f22": [], "f29": [], "balance": _balance_falso()})
    assert tokens["balance.saldo_caja"]["valor"] == 50
    assert tokens["balance.total_activo_sii"]["valor"] == 1000
    assert tokens["balance.total_pasivo_columna_sii_sin_utilidad_ejercicio"]["valor"] == 700
    assert tokens["balance.patrimonio_financiero"]["valor"] == 850

def test_tokens_balance_patrimonio_none_no_genera_token():
    tokens = ea.construir_tokens({"f22": [], "f29": [], "balance": _balance_falso(patrimonio=None)})
    assert "balance.patrimonio_financiero" not in tokens

def test_tokens_f29_codigos():
    tokens = ea.construir_tokens({"f22": [], "f29": [_f29_falso()], "balance": {}})
    assert tokens["f29.2099-01.077"]["valor"] == 500

def test_tokens_valores_no_recalculados_mismo_objeto():
    f22 = _f22_falso()
    tokens = ea.construir_tokens({"f22": [f22], "f29": [], "balance": {}})
    # mismo objeto del parser, no una copia recalculada
    assert tokens["f22.2099.843"] is f22["codigos"]["843"]
    assert tokens["f22.2099.122"] is f22["codigos"]["122"]

def test_tokens_codigo_ausente_none_no_genera_token():
    f22 = _f22_falso()
    f22["codigos"]["101"] = None
    tokens = ea.construir_tokens({"f22": [f22], "f29": [], "balance": {}})
    assert "f22.2099.101" not in tokens
