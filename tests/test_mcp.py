#!/usr/bin/env python3
"""Runnable check for the MCP server.

Drives a real stdio session — handshake, tool listing, a real call, and every
failure path — against a freshly created household repository.

The last group is the one that matters most: it asserts that NO tool can order
or pay for anything. That absence is the product's safety property, and a test
is the only thing that stops a future commit from quietly removing it.

    python3 tests/test_mcp.py
"""

import json
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
AFERIDOR = ROOT / "bin" / "aferidor"
MCP = ROOT / "bin" / "aferidor-mcp"

falhas = []


def check(rotulo, got, want):
    if got != want:
        falhas.append(f"{rotulo}: got {got!r}, want {want!r}")


def session(casa, messages):
    """Send newline-delimited JSON-RPC, collect the responses."""
    payload = "".join(json.dumps(m) + "\n" if isinstance(m, dict) else m + "\n" for m in messages)
    p = subprocess.run(
        [sys.executable, str(MCP)],
        input=payload, capture_output=True, text=True, timeout=120, cwd=str(casa),
    )
    if p.returncode != 0:
        falhas.append(f"server exited {p.returncode}: {p.stderr[:300]}")
        return []
    return [json.loads(line) for line in p.stdout.splitlines() if line.strip()]


with tempfile.TemporaryDirectory() as tmp:
    subprocess.run([sys.executable, str(AFERIDOR), "init", tmp],
                   capture_output=True, text=True, check=True)

    out = session(tmp, [
        {"jsonrpc": "2.0", "id": 1, "method": "initialize",
         "params": {"protocolVersion": "2025-06-18", "capabilities": {}}},
        {"jsonrpc": "2.0", "method": "notifications/initialized"},
        {"jsonrpc": "2.0", "id": 2, "method": "tools/list"},
        {"jsonrpc": "2.0", "id": 3, "method": "tools/call",
         "params": {"name": "comparar_preco", "arguments": {"sku": "oleo-de-soja"}}},
        {"jsonrpc": "2.0", "id": 4, "method": "tools/call",
         "params": {"name": "nao_existe", "arguments": {}}},
        {"jsonrpc": "2.0", "id": 5, "method": "tools/call",
         "params": {"name": "comparar_preco", "arguments": {}}},
        {"jsonrpc": "2.0", "id": 6, "method": "metodo/inventado"},
        "isto nao e json",
        {"jsonrpc": "2.0", "id": 7, "method": "tools/call",
         "params": {"name": "ler_doutrina", "arguments": {}}},
    ])

    by_id = {m.get("id"): m for m in out}

    # A notification must not produce a response; a bad line must not end the session.
    check("one response per request (notification silent)", len(out), 8)

    init = by_id.get(1, {}).get("result", {})
    check("handshake echoes the requested protocol", init.get("protocolVersion"), "2025-06-18")
    check("server identifies itself", init.get("serverInfo", {}).get("name"), "aferidor")
    check("tools capability advertised", "tools" in init.get("capabilities", {}), True)
    if len(init.get("instructions", "")) < 200:
        falhas.append("instructions are missing or too short to steer a model")

    tools = by_id.get(2, {}).get("result", {}).get("tools", [])
    names = {t["name"] for t in tools}
    check("every tool is exposed", len(tools), 11)
    for required in ("aconselhar", "comparar_preco", "listar_itens", "ler_doutrina",
                     "ver_historico", "o_que_falta", "escrever_mensagem"):
        if required not in names:
            falhas.append(f"tool missing from tools/list: {required}")
    for t in tools:
        if not t.get("description") or len(t["description"]) < 40:
            falhas.append(f"tool {t['name']!r} has no usable description")
        if t.get("inputSchema", {}).get("type") != "object":
            falhas.append(f"tool {t['name']!r} has no object inputSchema")

    # A real call returns real, parseable data.
    call = by_id.get(3, {}).get("result", {})
    check("comparar_preco succeeded", call.get("isError"), False)
    try:
        data = json.loads(call["content"][0]["text"])
        check("comparison normalised to litres", data["base"], "L")
        check("both merchants present", len(data["mercados"]), 2)
    except (KeyError, IndexError, ValueError) as exc:
        falhas.append(f"comparar_preco payload not usable: {exc}")

    # Failures are reported as tool errors, never as crashes.
    check("unknown tool is a tool error", by_id.get(4, {}).get("result", {}).get("isError"), True)
    check("missing argument is a tool error", by_id.get(5, {}).get("result", {}).get("isError"), True)
    check("unknown method is JSON-RPC error", by_id.get(6, {}).get("error", {}).get("code"), -32601)
    check("bad JSON is a parse error", by_id.get(None, {}).get("error", {}).get("code"), -32700)
    # …and the session kept going after all of them.
    check("session survived every failure", by_id.get(7, {}).get("result", {}).get("isError"), False)

    # ---------------------------------------------------------------------
    # THE SAFETY PROPERTY: no tool can order or pay.
    #
    # Payment is completed by a person, by hand, in the merchant's app. There
    # is deliberately no capability here for a model to be talked into using.
    # If this group fails, someone added a tool that spends money — that is the
    # one change this project does not make.
    # ---------------------------------------------------------------------
    PROIBIDO = ("pag", "pedido", "comprar", "checkout", "order", "pay", "fone",
                "telefone", "celular", "tocar", "cart", "carrinho", "finalizar")
    for name in names:
        for word in PROIBIDO:
            if word in name.casefold():
                falhas.append(f"SAFETY: tool {name!r} looks like it can order or pay")

    blob = json.dumps(tools, ensure_ascii=False).casefold()
    for word in ("adb", "aferidor-fone", "android"):
        if word in blob:
            falhas.append(f"SAFETY: the tool surface mentions {word!r} — the phone must not be reachable")

    # Writing a message to a shop is allowed; sending it is not. The tool that
    # drafts one has to say so in its own description, because that description
    # is the only thing a model reads before deciding what it may do.
    escrever = next((t for t in tools if t["name"] == "escrever_mensagem"), None)
    if escrever is None:
        falhas.append("SAFETY: escrever_mensagem is missing")
    else:
        desc = escrever["description"].casefold()
        check("the drafting tool declares it cannot send",
              ("não envia" in desc) and ("não tem como enviar" in desc), True)

    # The server source must not be able to reach the phone driver at all.
    # Tokenise and drop comments and string literals first: the docstrings here
    # discuss `aferidor-fone` at length on purpose, and a naive text search flags
    # the very prose that explains the boundary.
    import io
    import tokenize

    code_only = []
    with MCP.open("rb") as fh:
        for tok in tokenize.tokenize(fh.readline):
            if tok.type not in (tokenize.COMMENT, tokenize.STRING):
                code_only.append(tok.string)
    code = " ".join(code_only)
    for needle in ("aferidor-fone", "aferidor_fone", "adb"):
        if needle in code:
            falhas.append(f"SAFETY: executable code references {needle!r} — the phone must not be reachable")

if falhas:
    print(f"FAIL — {len(falhas)} checks did not hold:\n")
    for f in falhas:
        print(f"  {f}")
    sys.exit(1)
print("ok — MCP handshake, 11 tools, failures contained, and no tool can order or pay")
