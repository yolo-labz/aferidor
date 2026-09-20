#!/usr/bin/env python3
"""Runnable check for reading old receipts and reasoning about what ran low.

Drives the real CLI against a real household repository built from the shipped
template, with a real NFC-e XML written to disk.

The check that matters most is the second one: importing the same receipt twice
must not double the history. Everything the tool says downstream is a median
over these rows, so a silent duplicate does not fail loudly — it just quietly
shifts every price and every replenishment rate, and nobody finds out.

    python3 tests/test_historico.py
"""

import json
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
AFERIDOR = ROOT / "bin" / "aferidor"

falhas = []


def check(rotulo, got, want):
    if got != want:
        falhas.append(f"{rotulo}: got {got!r}, want {want!r}")


def aferidor(casa, *args, esperar_ok=True):
    p = subprocess.run(
        [sys.executable, str(AFERIDOR), *args],
        capture_output=True, text=True, timeout=120, cwd=str(casa),
    )
    if esperar_ok and p.returncode != 0:
        falhas.append(f"aferidor {' '.join(args)} exited {p.returncode}: {p.stderr[:300]}")
    return p


# A minimal but real NFC-e (model 65) authorised XML: the shape SEFAZ hands back.
NFCE = """<?xml version="1.0" encoding="UTF-8"?>
<nfeProc xmlns="http://www.portalfiscal.inf.br/nfe" versao="4.00">
  <NFe><infNFe Id="NFe26260812345678000199650010000000011000000017" versao="4.00">
    <ide><cUF>26</cUF><mod>65</mod><nNF>1</nNF><dhEmi>2026-08-14T19:20:31-03:00</dhEmi></ide>
    <emit><CNPJ>12345678000199</CNPJ><xNome>SUPERMERCADO EXEMPLO LTDA</xNome>
      <xFant>Mercado Exemplo</xFant>
      <enderEmit><xMun>Recife</xMun><UF>PE</UF></enderEmit></emit>
    <det nItem="1"><prod><cProd>7891</cProd><cEAN>7891000100103</cEAN>
      <xProd>OLEO SOJA LIZA 900ML</xProd><uCom>UN</uCom>
      <qCom>2.0000</qCom><vUnCom>7.4900</vUnCom><vProd>14.98</vProd></prod></det>
    <det nItem="2"><prod><cProd>7892</cProd><cEAN>7891000100110</cEAN>
      <xProd>ARROZ TIO JOAO 1KG</xProd><uCom>UN</uCom>
      <qCom>1.0000</qCom><vUnCom>6.9900</vUnCom><vProd>6.99</vProd></prod></det>
    <total><ICMSTot><vNF>21.97</vNF><vDesc>0.00</vDesc></ICMSTot></total>
  </infNFe></NFe>
</nfeProc>
"""


def linhas_nfce(casa):
    texto = (casa / "dados" / "observacoes.csv").read_text(encoding="utf-8")
    return [ln for ln in texto.splitlines() if ",nfce," in ln]


with tempfile.TemporaryDirectory() as tmp:
    casa = pathlib.Path(tmp) / "casa"
    subprocess.run([sys.executable, str(AFERIDOR), "init", str(casa)],
                   capture_output=True, text=True, check=True)

    notas = casa / "notas"
    notas.mkdir()
    (notas / "agosto.xml").write_text(NFCE, encoding="utf-8")

    # -- reading an old receipt --------------------------------------------
    lido = aferidor(casa, "nfce", "notas", "--json")
    recibos = json.loads(lido.stdout)
    check("one receipt parsed", len(recibos), 1)
    check("merchant name", recibos[0]["emitente"], "Mercado Exemplo")
    check("date from dhEmi", recibos[0]["data"], "2026-08-14")
    check("both items", len(recibos[0]["itens"]), 2)
    check("quantity parsed", recibos[0]["itens"][0]["quantidade"], 2.0)
    check("total parsed", recibos[0]["total"], 21.97)

    # A directory argument must find the XML inside it, not require the file.
    check("directory recursed", "OLEO SOJA LIZA 900ML" in lido.stdout, True)

    # -- importing, twice ---------------------------------------------------
    primeira = aferidor(casa, "nfce", "notas", "--importar")
    check("first import writes both items", len(linhas_nfce(casa)), 2)
    check("first import says so", "imported 2 observations" in primeira.stdout, True)

    segunda = aferidor(casa, "nfce", "notas", "--importar")
    check("second import writes nothing", len(linhas_nfce(casa)), 2)
    check("second import says it skipped", "skipped 1 receipt" in segunda.stdout, True)
    check("and imports zero", "imported 0 observations" in segunda.stdout, True)

    # The access key is what makes that possible, so it must be stored whole:
    # the first 12 chars are UF + year-month + part of the CNPJ, which every
    # receipt from one shop in one month shares.
    chave = "26260812345678000199650010000000011000000017"
    check("access key stored in full", chave in linhas_nfce(casa)[0], True)

    # The same receipt reaching one batch twice — a copied file, or a folder
    # passed alongside a file inside it — is still the same receipt.
    (notas / "copia.xml").write_text(NFCE, encoding="utf-8")
    aferidor(casa, "nfce", "notas/agosto.xml", "notas/copia.xml", "--importar")
    check("a repeat inside one batch is caught too", len(linhas_nfce(casa)), 2)

    # A history imported by the old truncated-key version cannot be matched.
    # Guessing would be worse than saying so, so it must say so.
    legado = casa / "dados" / "observacoes.csv"
    legado.write_text(
        legado.read_text(encoding="utf-8").replace(chave, chave[:12]), encoding="utf-8")
    aviso = aferidor(casa, "nfce", "notas", "--importar")
    check("legacy truncated keys are disclosed",
          "truncated key" in aviso.stdout, True)

    # -- history by date ----------------------------------------------------
    hist = aferidor(casa, "historico", "--json")
    meses = json.loads(hist.stdout)["meses"]
    check("august is present", "2026-08" in meses, True)
    check("august spend includes the receipt",
          round(meses["2026-08"]["gasto"], 2) >= 21.97, True)

    filtrado = aferidor(casa, "historico", "--desde", "2099-01-01", esperar_ok=False)
    check("an empty window is an error, not an empty table", filtrado.returncode, 1)

    item = json.loads(aferidor(casa, "historico", "oleo-de-soja", "--json").stdout)["item"]
    check("item timeline is dated and ordered",
          item["compras"] == sorted(item["compras"], key=lambda c: c["data"]), True)
    check("cycles counted", item["ciclos"] >= 1, True)

    # -- what ran low -------------------------------------------------------
    falta = json.loads(aferidor(casa, "falta", "--json").stdout)
    check("every verdict group exists",
          sorted(falta), ["coletar", "conferir", "manter", "repor"])
    todos = [v["sku"] for grupo in falta.values() for v in grupo]
    check("no sku is judged twice", len(todos), len(set(todos)))

    # The template ships two purchases of toilet paper on purpose. Under six,
    # the tool must decline rather than guess.
    coletar = [v["sku"] for v in falta["coletar"]]
    check("under-sampled item refuses to guess", "papel-higienico-30m" in coletar, True)

    # Interleaved 1 kg top-ups and 5 kg sacks are two rhythms in one series. The
    # honest answer is that it cannot separate them, not an invented average.
    razoes = {v["sku"]: v["razao"] for v in falta["coletar"]}
    check("a lumpy rhythm is admitted, not averaged",
          "irregular" in razoes.get("arroz-tio-joao-1kg", ""), True)

    # A spreadsheet that rewrote every date is the realistic pt-BR disaster.
    # The tool must say it could not read them, never just "0 compras".
    csv_path = casa / "dados" / "observacoes.csv"
    guardado = csv_path.read_text(encoding="utf-8")
    linhas = guardado.splitlines()
    quebrado = [linhas[0]] + [ln.replace(ln.split(",")[0], "31/31/2026", 1)
                              for ln in linhas[1:] if ln.strip()]
    csv_path.write_text("\n".join(quebrado) + "\n", encoding="utf-8")
    ilegivel = aferidor(casa, "falta").stdout
    check("unreadable dates are disclosed, not silently zero",
          "não foram lidas" in ilegivel, True)
    csv_path.write_text(guardado, encoding="utf-8")

    texto = aferidor(casa, "falta").stdout
    for proibido in ["acabou", "está sem", "vai acabar", "% de chance", "compre agora"]:
        check(f"never says {proibido!r}", proibido in texto.lower(), False)
    check("says plainly that it reads purchases, not the cupboard",
          "não o armário" in texto, True)

    # -- the seller message -------------------------------------------------
    zap = aferidor(casa, "zap")
    check("writes a message", "Oi!" in zap.stdout, True)
    check("points at wa", "github.com/yolo-labz/wa" in zap.stdout, True)
    check("shows the allowlist step first", "wa allow add" in zap.stdout, True)
    check("says it does not send", "não envia mensagem" in zap.stdout, True)
    # $'...' is what keeps the line breaks; a plain '...' would deliver "\n".
    check("quotes the body so newlines survive", "--body $'" in zap.stdout, True)

    antes = (casa / "dados" / "observacoes.csv").read_text(encoding="utf-8")
    aferidor(casa, "zap", "oleo-de-soja")
    check("asking about an item changes nothing on disk",
          (casa / "dados" / "observacoes.csv").read_text(encoding="utf-8"), antes)

# ---------------------------------------------------------------------------
# A household created before the 20/09/2026 rename still has `feira.toml`.
#
# Reading only the new name would not fail loudly: the file would simply be
# ignored, the shipping defaults would load, and a household that had raised its
# migration threshold to 20% would start seeing 9% migrations recommended with
# no warning anywhere. Silent configuration loss is the failure mode worth a
# test, so this asserts the old file is *read*, and that the new name wins when
# both exist.
with tempfile.TemporaryDirectory() as tmp:
    legada = pathlib.Path(tmp) / "casa-legada"
    subprocess.run([sys.executable, str(AFERIDOR), "init", str(legada)],
                   capture_output=True, text=True, check=True)

    config = (legada / "aferidor.toml").read_text(encoding="utf-8")
    (legada / "feira.toml").write_text(
        config.replace("delta_minimo_pct = 8.0", "delta_minimo_pct = 90.0"),
        encoding="utf-8")
    (legada / "aferidor.toml").unlink()

    achou = aferidor(legada, "advise")
    check("a household keeping the old config name is still a household",
          achou.returncode, 0)
    antigo = json.loads(aferidor(legada, "compare", "oleo-de-soja", "--json").stdout)
    check("the threshold in feira.toml is the one in force",
          "limite 90%" in antigo["veredito"]["razao"], True)

    (legada / "aferidor.toml").write_text(config, encoding="utf-8")
    novo = json.loads(aferidor(legada, "compare", "oleo-de-soja", "--json").stdout)
    check("with both present, aferidor.toml wins",
          "limite 8%" in novo["veredito"]["razao"], True)

if falhas:
    print(f"FAIL — {len(falhas)} check(s) did not hold:\n")
    for f in falhas:
        print(f"  {f}")
    sys.exit(1)
print("ok — receipts import once, history reads by date, low stock is a suggestion, "
      "and a pre-rename household keeps its own thresholds")
