import importlib.util, os
spec = importlib.util.spec_from_file_location(
    "codigos_sii", os.path.join(os.path.dirname(__file__), "..", "scripts", "codigos_sii.py"))
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

def test_codigos_f22_con_fuente():
    for cod in ("122", "123", "101", "843", "645", "646", "305"):
        assert cod in m.F22, cod
        assert m.F22[cod]["glosa"] and m.F22[cod]["fuente"], cod

def test_codigos_f29_con_fuente():
    for cod in ("538", "537", "077", "089", "547", "048", "092", "093", "094"):
        assert cod in m.F29, cod
        assert m.F29[cod]["glosa"] and m.F29[cod]["fuente"], cod

def test_fuentes_sin_placeholder_sin_rellenar():
    # Ninguna fuente debe quedar con un marcador de página sin rellenar.
    # No se acepta '<X>', 'p.<X>' ni ningún '<...>' sin rellenar.
    for tabla in (m.F22, m.F29):
        for cod, info in tabla.items():
            assert "<" not in info["fuente"], f"fuente sin rellenar en {cod}: {info['fuente']}"

def test_aliases_no_vacios():
    # Toda entrada (F22 y F29) debe declarar aliases no vacío.
    for tabla in (m.F22, m.F29):
        for cod, info in tabla.items():
            assert info.get("aliases"), f"aliases vacío o ausente en {cod}"
            assert cod in info["aliases"], f"{cod} debe estar en sus propios aliases"

def test_aliases_cero_inicial_f29():
    # Los códigos con cero inicial aceptan ambas formas textuales.
    assert set(m.F29["092"]["aliases"]) >= {"92", "092"}
    for cod, sin_cero in (("048", "48"), ("077", "77"), ("089", "89"),
                          ("093", "93"), ("094", "94")):
        assert sin_cero in m.F29[cod]["aliases"], cod
        assert cod in m.F29[cod]["aliases"], cod
