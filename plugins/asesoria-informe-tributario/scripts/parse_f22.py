import re, sys, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from codigos_sii import F22

def _monto(s): return int(s.replace(".", "").replace("$", "").strip())

def _buscar_codigo(texto, formas):
    """Localiza cualquiera de las 'formas' del código (aliases con/sin cero inicial).
    F22 trae el valor ANTES de la glosa Y DESPUÉS del código (ejemplo ilustrativo
    sintético: "122 1.000.000Total del Activo"). El texto extraído de un PDF real
    puede concatenar varios códigos por línea sin separador (ejemplo ilustrativo
    sintético: "102 500.000Capital 122 1.000.000Total del Activo"), así que solo se
    mira lo que sigue al código (no lo que lo precede) para no capturar el valor del código
    anterior en la misma línea."""
    patron = re.compile(r"\b(?:" + "|".join(re.escape(f) for f in formas) + r")\b")
    for line in texto.splitlines():
        m = patron.search(line)
        if m:
            resto = line[m.end():]
            nums = [n for n in re.findall(r"-?[\d\.]+", resto) if any(c.isdigit() for c in n)]
            if nums:
                return _monto(nums[0]), line.strip()
    return None

def parse_f22_text(texto, archivo, pagina=1):
    codigos = {}
    for cod in F22:
        hit = _buscar_codigo(texto, F22[cod].get("aliases", [cod]))
        codigos[cod] = None if hit is None else {
            "valor": hit[0], "archivo": archivo, "pagina": pagina, "texto_cercano": hit[1]}
    anio = None
    ma = re.search(r"A[ÑN]O\s+TRIBUTARIO\s+(\d{4})", texto)
    if ma: anio = int(ma.group(1))
    def v(c): return codigos[c]["valor"] if codigos.get(c) else None
    pe = (v("122") - v("843")) if v("122") is not None and v("843") is not None else None
    res = (v("122") - v("123")) if v("122") is not None and v("123") is not None else None
    return {"anio": anio, "codigos": codigos,
            "derivados": {"pasivo_exigible": pe, "resultado_ejercicio": res},
            "validaciones": []}

def parse_f22_file(path):
    from pypdf import PdfReader
    r = PdfReader(path)
    texto = "".join((p.extract_text() or "") for p in r.pages)
    return parse_f22_text(texto, Path(path).name, 1)

if __name__ == "__main__":
    print(json.dumps(parse_f22_file(sys.argv[1]), ensure_ascii=False, indent=2))
