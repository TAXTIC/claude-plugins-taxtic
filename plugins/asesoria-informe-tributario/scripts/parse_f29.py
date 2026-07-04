import re, sys, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from codigos_sii import F29

def _monto(s):
    return int(s.replace(".", "").replace("$", "").strip())

def _buscar_codigo(texto, formas):
    """Localiza cualquiera de las 'formas' del código (aliases: con/sin cero inicial,
    p.ej. '048' y '48') y captura el número asociado. Devuelve (valor, texto_cercano) o None."""
    patron = re.compile(r"\b(?:" + "|".join(re.escape(f) for f in formas) + r")\b")
    for line in texto.splitlines():
        m = patron.search(line)
        if m:
            resto = line[:m.start()] + line[m.end():]   # quitar solo la ocurrencia del código
            nums = [n for n in re.findall(r"-?[\d\.]+", resto) if any(c.isdigit() for c in n)]
            if nums:
                return _monto(nums[-1]), line.strip()
    return None

def parse_f29_text(texto, archivo, pagina=1):
    codigos = {}
    for cod in F29:
        hit = _buscar_codigo(texto, F29[cod].get("aliases", [cod]))
        codigos[cod] = None if hit is None else {
            "valor": hit[0], "archivo": archivo, "pagina": pagina, "texto_cercano": hit[1]}
    periodo = None
    mp = re.search(r"PERIODO\s*\[15\]\s*(\d{4})(\d{2})", texto)
    if mp: periodo = f"{mp.group(1)}-{mp.group(2)}"
    folio = None
    mf = re.search(r"FOLIO\s*\[07\]\s*(\d+)", texto)
    if mf: folio = mf.group(1)
    fecha = None
    mfe = re.search(r"Presentaci[oó]n\s*(\d{2}/\d{2}/\d{4})", texto)
    if mfe: fecha = mfe.group(1)
    validaciones = []
    # 547 total determinado NO es IVA — validación separada, no descarta
    if codigos.get("547") and codigos.get("089") and \
       codigos["547"]["valor"] == codigos["089"]["valor"] and codigos["089"]["valor"] != 0:
        validaciones.append("REVISAR: 547 == 089 inesperado (547 debería incluir retenciones)")
    total_pagado = codigos["547"]["valor"] if codigos.get("547") else None
    return {"periodo": periodo, "folio": folio, "codigos": codigos,
            "total_pagado": total_pagado, "fecha_presentacion": fecha,
            "validaciones": validaciones}

def parse_f29_file(path):
    from pypdf import PdfReader
    r = PdfReader(path)
    texto = "".join((p.extract_text() or "") for p in r.pages)
    return parse_f29_text(texto, Path(path).name, 1)

if __name__ == "__main__":
    print(json.dumps(parse_f29_file(sys.argv[1]), ensure_ascii=False, indent=2))
