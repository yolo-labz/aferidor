#!/usr/bin/env python3
"""Runnable check for aferidor-fone's guardrails.

Only the pure logic is exercised here — no phone required, and deliberately so:
this must be verifiable on a machine with no device attached, because it is the
code that stands between an agent and someone's money.

    python3 tests/test_fone.py
"""

import importlib.machinery
import importlib.util
import pathlib
import sys

# The executable has no .py suffix, so it needs an explicit source loader.
FONE = pathlib.Path(__file__).resolve().parent.parent / "bin" / "aferidor-fone"

spec = importlib.util.spec_from_loader(
    "aferidor_fone", importlib.machinery.SourceFileLoader("aferidor_fone", str(FONE))
)
fone = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fone)

falhas = []


def check(rotulo, got, want):
    if got != want:
        falhas.append(f"{rotulo}: got {got!r}, want {want!r}")


# --- the payment gate ------------------------------------------------------
# A false negative here is an unattended purchase, so the list is checked in
# both languages and in the casing the apps actually render.

for label in [
    "Pagar", "PAGAR R$ 288,46", "Finalizar pedido", "Finalizar Compra",
    "Confirmar pagamento", "Place order", "PLACE ORDER", "Comprar agora",
    "Adicionar cartão", "Enviar", "Fazer pedido",
]:
    if fone.is_dangerous(label) is None:
        falhas.append(f"payment gate MISSED a dangerous label: {label!r}")

for label in [
    "Adicionar ao carrinho", "Buscar", "Ver mais", "Arroz Tio João 1kg",
    "Voltar", "Continuar comprando", "Filtrar",
]:
    if fone.is_dangerous(label) is not None:
        falhas.append(f"payment gate blocked a harmless label: {label!r}")


# --- element matching ------------------------------------------------------

nodes = [
    {"text": "Adicionar ao carrinho", "desc": "", "enabled": True, "clickable": True,
     "area": 40_000, "center": {"x": 500, "y": 900}},
    # The card containing the button. Same text, far larger — must lose.
    {"text": "Arroz Tio João 1kg Adicionar ao carrinho", "desc": "", "enabled": True,
     "clickable": True, "area": 400_000, "center": {"x": 500, "y": 800}},
    {"text": "Indisponível", "desc": "", "enabled": False, "clickable": True,
     "area": 30_000, "center": {"x": 500, "y": 1100}},
    {"text": "", "desc": "Buscar produtos", "enabled": True, "clickable": True,
     "area": 20_000, "center": {"x": 300, "y": 120}},
]

hits = fone.match(nodes, "adicionar ao carrinho")
check("case-insensitive match finds both", len(hits), 2)
check("tightest element wins over its card", hits[0]["area"], 40_000)

check("disabled elements are skipped", fone.match(nodes, "Indisponível"), [])
check("content-desc is searched too", len(fone.match(nodes, "buscar")), 1)
check("no match is empty, not an error", fone.match(nodes, "não existe"), [])

# A non-clickable label is findable but not tappable.
nodes.append({"text": "Total", "desc": "", "enabled": True, "clickable": False,
              "area": 10_000, "center": {"x": 100, "y": 1400}})
check("non-clickable excluded by default", fone.match(nodes, "Total"), [])
check("non-clickable included on request", len(fone.match(nodes, "Total", only_clickable=False)), 1)


# --- bounds parsing --------------------------------------------------------

check("PERIGO list is non-empty", len(fone.PERIGO) > 0, True)
check("bounds regex", bool(fone.BOUNDS.fullmatch("[0,100][540,200]")), True)
check("bounds regex rejects junk", bool(fone.BOUNDS.fullmatch("0,100,540,200")), False)

if falhas:
    print(f"FAIL — {len(falhas)} checks did not hold:\n")
    for f in falhas:
        print(f"  {f}")
    sys.exit(1)
print("ok — payment gate catches every dangerous label, matcher prefers the tightest element")
