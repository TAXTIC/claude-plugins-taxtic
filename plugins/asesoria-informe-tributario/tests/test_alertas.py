import importlib.util, os
def _load(name):
    spec = importlib.util.spec_from_file_location(name,
        os.path.join(os.path.dirname(__file__), "..", "scripts", name + ".py"))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
al = _load("alertas")

def _f29(periodo, c94=0, c077=0):
    cod = {}
    if c94: cod["094"] = {"valor": c94}
    if c077: cod["077"] = {"valor": c077}
    return {"periodo": periodo, "codigos": cod}

def test_recargo_gatilla_por_094():
    datos = {"f29": [_f29("2025-08", c94=5000)], "f22": [], "balance": {}}
    a = al.alertas_deterministas(datos)
    assert any(x["codigo"] == "F29_RECARGO" and x["periodo"] == "2025-08" for x in a)

def test_sin_recargo_no_gatilla():
    datos = {"f29": [_f29("2025-08", c94=0)], "f22": [], "balance": {}}
    assert not any(x["codigo"] == "F29_RECARGO" for x in al.alertas_deterministas(datos))

def test_cpt_negativo():
    datos = {"f29": [], "f22": [{"codigos": {"646": {"valor": 100}}}], "balance": {}}
    assert any(x["codigo"] == "CPT_NEGATIVO" for x in al.alertas_deterministas(datos))

def test_remanente_creciente():
    datos = {"f29": [_f29("2025-06", c077=100), _f29("2025-07", c077=200),
                     _f29("2025-08", c077=300)], "f22": [], "balance": {}}
    assert any(x["codigo"] == "REMANENTE_CRECIENTE" for x in al.alertas_deterministas(datos))

def test_ppm_devolucion_por_resultado_liquidacion_negativo():
    datos = {"f29": [], "f22": [{"codigos": {"305": {"valor": -742806}}}], "balance": {}}
    a = al.alertas_deterministas(datos)
    op = [x for x in a if x["codigo"] == "PPM_DEVOLUCION"]
    assert op and op[0]["nivel"] == "OPORTUNIDAD"

def test_ppm_sin_devolucion_si_resultado_positivo():
    datos = {"f29": [], "f22": [{"codigos": {"305": {"valor": 500000}}}], "balance": {}}
    assert not any(x["codigo"] == "PPM_DEVOLUCION" for x in al.alertas_deterministas(datos))
