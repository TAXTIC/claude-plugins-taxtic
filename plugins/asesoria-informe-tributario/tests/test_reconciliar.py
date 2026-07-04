import importlib.util, os
def _load(name):
    spec = importlib.util.spec_from_file_location(name,
        os.path.join(os.path.dirname(__file__), "..", "scripts", name + ".py"))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
rc = _load("reconciliar")

def _bal(**kw):
    base = {"total_activo_sii": 1000, "total_pasivo_columna_sii_sin_utilidad_ejercicio": 700,
            "patrimonio_financiero": 900, "saldo_caja": 50}
    base.update(kw); return base
def _f22(a=1000, p=700, pf=900, caja=50):
    return {"codigos": {"122": {"valor": a}, "123": {"valor": p},
                        "843": {"valor": pf}, "101": {"valor": caja}}}

def test_todo_cuadra():
    res = rc.reconciliar(_bal(), _f22())
    assert all(r["cuadra"] for r in res)
    assert len(res) == 4

def test_discrepancia_marca_no_cuadra():
    res = rc.reconciliar(_bal(total_activo_sii=999), _f22())
    r122 = next(r for r in res if "122" in r["regla"])
    assert r122["cuadra"] is False

def test_fallback_omite_cruce_si_balance_none():
    res = rc.reconciliar(_bal(patrimonio_financiero=None), _f22())
    assert not any("843" in r["regla"] for r in res)  # omitido, no falso positivo
