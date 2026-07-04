import sys, json

def _val(cod_dict, cod):
    d = cod_dict.get(cod)
    return d["valor"] if d else 0

def alertas_deterministas(datos):
    out = []
    # F29 recargo — señal primaria autoritativa (092/093/094 > 0)
    for f in datos.get("f29", []):
        cod = f.get("codigos", {})
        if any(_val(cod, c) > 0 for c in ("092", "093", "094")):
            out.append({"nivel": "ADVERTENCIA", "codigo": "F29_RECARGO",
                        "periodo": f.get("periodo"), "origen": "cod092/093/094>0",
                        "detalle": "El formulario declara recargo (IPC/interés/multa)."})
    # CPT negativo (646 > 0)
    for f in datos.get("f22", []):
        if _val(f.get("codigos", {}), "646") > 0:
            out.append({"nivel": "ADVERTENCIA", "codigo": "CPT_NEGATIVO",
                        "periodo": None, "origen": "F22[646]>0",
                        "detalle": "CPT negativo final declarado en F22."})
    # PPM / devolución — resultado liquidación anual (305) < 0 = saldo a favor / devolución
    for f in datos.get("f22", []):
        r305 = f.get("codigos", {}).get("305")
        if r305 is not None and r305.get("valor") is not None and r305["valor"] < 0:
            out.append({"nivel": "OPORTUNIDAD", "codigo": "PPM_DEVOLUCION",
                        "periodo": None, "origen": "F22[305]<0",
                        "detalle": "Resultado de liquidación anual negativo: PPM acumulado con "
                                   "potencial saldo a favor / devolución (confirmar en liquidación)."})
    # Patrimonio financiero negativo
    bal = datos.get("balance", {})
    pf = bal.get("patrimonio_financiero")
    if pf is not None and pf < 0:
        out.append({"nivel": "ADVERTENCIA", "codigo": "PATRIMONIO_NEGATIVO",
                    "periodo": None, "origen": "balance.patrimonio_financiero<0",
                    "detalle": "Patrimonio financiero negativo."})
    # Remanente 077 creciente sostenido (>= 3 periodos monótonos)
    f29 = sorted(datos.get("f29", []), key=lambda x: x.get("periodo") or "")
    rem = [(_val(f.get("codigos", {}), "077"), f.get("periodo")) for f in f29]
    rem = [r for r in rem if r[0] > 0]
    if len(rem) >= 3 and all(rem[i][0] < rem[i + 1][0] for i in range(len(rem) - 1)):
        out.append({"nivel": "ADVERTENCIA", "codigo": "REMANENTE_CRECIENTE",
                    "periodo": rem[-1][1], "origen": "F29[077] monótono creciente",
                    "detalle": "Remanente de crédito IVA creciente sostenido; posible acumulación."})
    return out

if __name__ == "__main__":
    print(json.dumps(alertas_deterministas(json.load(open(sys.argv[1], encoding="utf-8"))),
                     ensure_ascii=False, indent=2))
