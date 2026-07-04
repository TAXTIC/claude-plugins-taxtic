import sys, json

# (regla, campo balance, código F22)
CRUCES = [
    ("balance.total_activo_sii == F22[122]", "total_activo_sii", "122"),
    ("balance.total_pasivo_columna_sii_sin_utilidad_ejercicio == F22[123]",
     "total_pasivo_columna_sii_sin_utilidad_ejercicio", "123"),
    ("balance.patrimonio_financiero == F22[843]", "patrimonio_financiero", "843"),
    ("balance.saldo_caja == F22[101]", "saldo_caja", "101"),
]

def _f22val(f22, cod):
    d = f22.get("codigos", {}).get(cod)
    return d["valor"] if d else None

def reconciliar(balance, f22):
    res = []
    for regla, campo, cod in CRUCES:
        bval = balance.get(campo)
        fval = _f22val(f22, cod)
        if bval is None or fval is None:   # fallback: dato ausente → omitir (no cruzar mal)
            continue
        res.append({"regla": regla, "esperado": fval, "obtenido": bval,
                    "cuadra": bval == fval})
    return res

if __name__ == "__main__":
    data = json.load(open(sys.argv[1], encoding="utf-8"))
    print(json.dumps(reconciliar(data["balance"], data["f22"][0]), ensure_ascii=False, indent=2))
