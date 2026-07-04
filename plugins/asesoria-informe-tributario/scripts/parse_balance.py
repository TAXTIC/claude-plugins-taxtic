import re, sys, json

class DependenciaFaltante(Exception): ...

def _n(f, col): return f.get(col, 0) or 0

def _hojas(filas):
    """Filas de detalle: excluye subtotales (código padre, prefijo de otro código) y
    filas sin código (líneas de total/patrimonio/resultado). Evita doble conteo."""
    codigos = [f.get("codigo") or "" for f in filas]
    out = []
    for f in filas:
        c = f.get("codigo") or ""
        if not c:
            continue
        if any(o != c and o.startswith(c + ".") for o in codigos):  # es padre/subtotal
            continue
        out.append(f)
    return out

def _fila_por_desc(filas, *keys):
    for f in filas:
        d = (f.get("descripcion") or "").upper()
        if all(k in d for k in keys):
            return f
    return None

def compute_balance_totals(filas):
    hojas = _hojas(filas)
    total_activo = sum(_n(f, "activo") for f in hojas)
    total_pasivo = sum(_n(f, "pasivo") for f in hojas)
    saldo_caja = sum(_n(f, "activo") for f in hojas if "CAJA" in (f.get("descripcion") or "").upper())
    # patrimonio_financiero: SOLO desde una fila explícita "PATRIMONIO" del balance (idealmente
    # "TOTAL PATRIMONIO"). Si el balance no la expone, queda None → la reconciliación contra
    # F22[843] se OMITE (no se inventa ni se deriva por clasificación de cuentas 3.x, que
    # depende del plan de cuentas y no está confirmada).
    fp = _fila_por_desc(filas, "TOTAL", "PATRIMONIO")  # SOLO línea total explícita; header no fabrica 0
    patrimonio = _n(fp, "pasivo") if fp else None
    # resultado_ejercicio_balance: SOLO desde fila explícita; si no, None.
    fr = _fila_por_desc(filas, "RESULTADO", "EJERCICIO")
    resultado = (_n(fr, "pasivo") - _n(fr, "activo")) if fr else None
    return {
        "total_activo_sii": total_activo,
        "total_pasivo_columna_sii_sin_utilidad_ejercicio": total_pasivo,
        "patrimonio_financiero": patrimonio,
        "saldo_caja": saldo_caja,
        "resultado_ejercicio_balance": resultado,
    }

def extract_balance_rows(path):
    try:
        import pdfplumber
    except ImportError:
        raise DependenciaFaltante("pdfplumber no instalado: pip install pdfplumber")
    def num(x):
        x = (x or "").replace(".", "").replace(" ", "").strip()
        return int(x) if x.lstrip("-").isdigit() else 0
    filas = []
    with pdfplumber.open(path) as pdf:
        for pg in pdf.pages:
            for row in (pg.extract_table() or []):
                # columnas esperadas: Cuenta, Descripcion, Debe, Haber, Deudor, Acreedor, Activo, Pasivo, Perdida, Ganancia
                if not row: continue
                cod = (row[0] or "").strip()
                desc = (row[1] or "").strip() if len(row) > 1 else ""
                # detalle (código numérico) O líneas explícitas de patrimonio/resultado (sin código).
                keep = re.match(r"\d", cod) or any(k in desc.upper() for k in ("PATRIMONIO", "RESULTADO DEL EJERCICIO"))
                if not keep: continue
                filas.append({"codigo": cod, "descripcion": desc,
                              "activo": num(row[6]) if len(row) > 6 else 0,
                              "pasivo": num(row[7]) if len(row) > 7 else 0})
    return filas

def parse_balance_file(path):
    filas = extract_balance_rows(path)
    out = compute_balance_totals(filas)
    out["fecha"] = None
    out["cuentas"] = filas          # para la hoja "Balance Cuentas" del anexo .xlsx
    out["_n_cuentas"] = len(filas)
    return out

if __name__ == "__main__":
    print(json.dumps(parse_balance_file(sys.argv[1]), ensure_ascii=False, indent=2))
