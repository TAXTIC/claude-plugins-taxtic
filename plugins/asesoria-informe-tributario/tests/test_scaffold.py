import json, os
BASE = os.path.join(os.path.dirname(__file__), "..")

def test_plugin_json_valido():
    with open(os.path.join(BASE, ".claude-plugin", "plugin.json"), encoding="utf-8") as f:
        meta = json.load(f)
    assert meta["name"] == "asesoria-informe-tributario"
    assert meta["version"] == "0.1.0"

def test_assets_presentes():
    for a in ("imagotipo-principal-negro.png", "isologo-naranjo.png", "marca.md"):
        assert os.path.exists(os.path.join(BASE, "assets", a)), a

def test_requirements_presente():
    req = os.path.join(BASE, "requirements.txt")
    assert os.path.exists(req)
    txt = open(req, encoding="utf-8").read()
    for dep in ("pypdf", "pdfplumber", "openpyxl", "python-docx", "pytest"):
        assert dep in txt, dep
