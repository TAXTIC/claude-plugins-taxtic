import sys, json, argparse
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from parse_f29 import parse_f29_file
from parse_f22 import parse_f22_file
from parse_balance import parse_balance_file
from read_ficha import read_ficha_file
from read_malla import read_malla_file
from reconciliar import reconciliar
from alertas import alertas_deterministas

# Campos escalares del balance que se exponen como token plano. patrimonio_financiero
# puede venir None (el balance no siempre trae la fila "TOTAL PATRIMONIO" explícita) y
# en ese caso NO se genera el token — mejor omitir que fabricar un dato.
_CAMPOS_BALANCE = ("total_activo_sii", "saldo_caja",
                   "total_pasivo_columna_sii_sin_utilidad_ejercicio", "patrimonio_financiero")


def construir_tokens(datos):
    """Arma el bloque plano `tokens` que la prosa referencia vía {{token}}.

    Los valores SIEMPRE se copian tal cual del output de los parsers (parse_f29,
    parse_f22, parse_balance) — nunca se recalculan ni se teclean acá. Esta función
    es pura: no toca disco, no corre parsers, solo reorganiza datos ya extraídos.
    """
    tokens = {}

    for f22 in datos.get("f22") or []:
        anio = f22.get("anio")
        for cod, dato in (f22.get("codigos") or {}).items():
            if dato is not None:
                tokens[f"f22.{anio}.{cod}"] = dato
        derivados = f22.get("derivados") or {}
        pe = derivados.get("pasivo_exigible")
        if pe is not None:
            tokens[f"f22.{anio}.pasivo_exigible"] = {
                "valor": pe, "archivo": f"F22 {anio}", "pagina": 0,
                "texto_cercano": "derivado: 122 - 843 (pasivo exigible)"}
        rej = derivados.get("resultado_ejercicio")
        if rej is not None:
            tokens[f"f22.{anio}.resultado_ejercicio"] = {
                "valor": rej, "archivo": f"F22 {anio}", "pagina": 0,
                "texto_cercano": "derivado: 122 - 123 (resultado del ejercicio)"}

    balance = datos.get("balance") or {}
    for campo in _CAMPOS_BALANCE:
        valor = balance.get(campo)
        if valor is not None:
            tokens[f"balance.{campo}"] = {
                "valor": valor, "archivo": "balance", "pagina": 0, "texto_cercano": campo}

    for f29 in datos.get("f29") or []:
        periodo = f29.get("periodo")
        for cod, dato in (f29.get("codigos") or {}).items():
            if dato is not None:
                tokens[f"f29.{periodo}.{cod}"] = dato

    return tokens


def _descubrir(carpeta, patron):
    return sorted(Path(carpeta).glob(patron), key=lambda p: p.name)


def ensamblar(carpeta):
    """Descubre los documentos del cliente en `carpeta`, corre todos los parsers
    deterministas y arma `datos` (incluido el bloque `tokens`). Ningún LLM
    transcribe cifras: todo el número sale de un parser Python.

    Si un archivo no se puede parsear, se registra en `no_procesados` y se sigue
    con el resto (no se aborta el ensamblado completo por un archivo).
    """
    no_procesados = []

    f29 = []
    for p in _descubrir(carpeta, "F29*.pdf"):
        try:
            f29.append(parse_f29_file(str(p)))
        except Exception as e:
            no_procesados.append({"archivo": p.name, "error": str(e)})

    f22 = []
    for p in _descubrir(carpeta, "F22*.pdf"):
        try:
            f22.append(parse_f22_file(str(p)))
        except Exception as e:
            no_procesados.append({"archivo": p.name, "error": str(e)})

    balance = {}
    for p in _descubrir(carpeta, "Balance*.pdf"):
        try:
            balance = parse_balance_file(str(p))
            break  # se espera un único balance por cliente
        except Exception as e:
            no_procesados.append({"archivo": p.name, "error": str(e)})

    cliente = {}
    for p in _descubrir(carpeta, "Datos*.xlsx"):
        try:
            cliente = read_ficha_file(str(p))
            break
        except Exception as e:
            no_procesados.append({"archivo": p.name, "error": str(e)})

    malla = {}
    for p in _descubrir(carpeta, "Malla*.xlsx"):
        try:
            malla = read_malla_file(str(p))
            break
        except Exception as e:
            no_procesados.append({"archivo": p.name, "error": str(e)})

    f22_mas_reciente = max((f for f in f22 if f.get("anio") is not None),
                           key=lambda f: f["anio"], default={})
    reconciliaciones = reconciliar(balance, f22_mas_reciente)

    datos = {
        "cliente": cliente,
        "malla": malla,
        "f29": f29,
        "f22": f22,
        "balance": balance,
        "reconciliaciones": reconciliaciones,
        "no_procesados": no_procesados,
    }
    datos["alertas_deterministas"] = alertas_deterministas(datos)
    datos["tokens"] = construir_tokens(datos)
    return datos


if __name__ == "__main__":
    ap = argparse.ArgumentParser(
        description="Ensambla datos.json determinista desde la carpeta de documentos del cliente "
                     "(descubre F29/F22/Balance/Datos/Malla, corre los parsers, arma tokens). "
                     "Ningún LLM transcribe cifras en esta fase.")
    ap.add_argument("carpeta", help="carpeta con los documentos del cliente")
    ap.add_argument("--out", default="datos.json", help="ruta de salida del datos.json")
    args = ap.parse_args()

    datos = ensamblar(args.carpeta)
    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(datos, fh, ensure_ascii=False, indent=2)

    cuadran = sum(1 for r in datos["reconciliaciones"] if r["cuadra"])
    resumen = {
        "f29": len(datos["f29"]),
        "f22": len(datos["f22"]),
        "reconciliaciones": f"{cuadran}/{len(datos['reconciliaciones'])} cuadran",
        "alertas": len(datos["alertas_deterministas"]),
        "no_procesados": len(datos["no_procesados"]),
        "salida": args.out,
    }
    print(json.dumps(resumen, ensure_ascii=False, indent=2))
