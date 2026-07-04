import importlib.util, os
def _load(name):
    spec = importlib.util.spec_from_file_location(name,
        os.path.join(os.path.dirname(__file__), "..", "scripts", name + ".py"))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
pb = _load("parse_balance")

FILAS = [
    {"codigo": "1.1.1010.10.01", "descripcion": "CAJA", "activo": 50000, "pasivo": 0},
    {"codigo": "2.1.0001", "descripcion": "PROVEEDORES", "activo": 0, "pasivo": 100000},
    {"codigo": "3.1.0001", "descripcion": "CAPITAL", "activo": 0, "pasivo": 600000},
]

# Con subtotales: los códigos padre "1" y "2" son prefijo de sus hijos → NO deben sumarse
# (sumar ciego duplicaría). Además una fila explícita TOTAL PATRIMONIO sin código.
FILAS_SUB = [
    {"codigo": "1", "descripcion": "TOTAL ACTIVO", "activo": 50000, "pasivo": 0},
    {"codigo": "1.1.1010.10.01", "descripcion": "CAJA", "activo": 50000, "pasivo": 0},
    {"codigo": "2", "descripcion": "TOTAL PASIVO", "activo": 0, "pasivo": 700000},
    {"codigo": "2.1.0001", "descripcion": "PROVEEDORES", "activo": 0, "pasivo": 100000},
    {"codigo": "3.1.0001", "descripcion": "CAPITAL", "activo": 0, "pasivo": 600000},
    {"codigo": "", "descripcion": "TOTAL PATRIMONIO", "activo": 0, "pasivo": 600000},
]

def test_totales_columnas():
    t = pb.compute_balance_totals(FILAS)
    assert t["total_activo_sii"] == 50000
    assert t["total_pasivo_columna_sii_sin_utilidad_ejercicio"] == 700000
    assert t["saldo_caja"] == 50000

def test_no_doble_conteo_subtotales():
    t = pb.compute_balance_totals(FILAS_SUB)
    assert t["total_activo_sii"] == 50000                                   # padre "1" excluido
    assert t["total_pasivo_columna_sii_sin_utilidad_ejercicio"] == 700000   # padre "2" excluido
    assert t["patrimonio_financiero"] == 600000                             # fila explícita

def test_patrimonio_y_resultado_none_si_no_explicitos():
    t = pb.compute_balance_totals(FILAS)
    assert t["patrimonio_financiero"] is None       # sin fila explícita → None (no se inventa)
    assert t["resultado_ejercicio_balance"] is None

# Header "PATRIMONIO" (pasivo=0) SIN línea "TOTAL PATRIMONIO": no debe fabricar 0 → None.
FILAS_HEADER_PATRIMONIO = [
    {"codigo": "1.1.1010.10.01", "descripcion": "CAJA", "activo": 50000, "pasivo": 0},
    {"codigo": "", "descripcion": "PATRIMONIO", "activo": 0, "pasivo": 0},  # solo header
    {"codigo": "3.1.0001", "descripcion": "CAPITAL", "activo": 0, "pasivo": 600000},
]

def test_patrimonio_none_si_solo_header_sin_total():
    t = pb.compute_balance_totals(FILAS_HEADER_PATRIMONIO)
    assert t["patrimonio_financiero"] is None       # header con pasivo=0 NO debe devolver 0

def test_parse_balance_file_emite_cuentas(monkeypatch):
    # El anexo .xlsx (hoja "Balance Cuentas") lee balance["cuentas"] → parse_balance_file
    # debe exponer la lista de filas extraídas. Reemplazamos el shell IO por filas FALSAS.
    filas_falsas = [
        {"codigo": "1.1.1010.10.01", "descripcion": "CAJA", "activo": 50000, "pasivo": 0},
        {"codigo": "2.1.0001", "descripcion": "PROVEEDORES", "activo": 0, "pasivo": 100000},
    ]
    monkeypatch.setattr(pb, "extract_balance_rows", lambda p: filas_falsas)
    out = pb.parse_balance_file("ruta_ignorada.pdf")
    assert out["cuentas"] == filas_falsas
    assert len(out["cuentas"]) == 2
    assert all(set(c) >= {"codigo", "descripcion", "activo", "pasivo"} for c in out["cuentas"])
    assert out["_n_cuentas"] == 2
    assert out["total_activo_sii"] == 50000
