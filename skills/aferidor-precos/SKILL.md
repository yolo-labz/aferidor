---
name: aferidor-precos
description: >-
  Compares grocery prices across merchants and decides whether to switch, using
  the household's own recorded price history rather than a live search. Handles
  "onde está mais barato", "vale a pena comprar no atacarejo", "quanto custava o
  arroz", "compara o preço do X", "where should I buy Y", "is this a good
  price", "did this get more expensive". Normalises every price to R$ per
  kg/L/unit before comparing, so a 900 ml bottle never beats a 1 L bottle on the
  sticker alone. Applies the household's migration rule (minimum delta AND
  minimum sample count) instead of naively recommending the cheapest observed
  price. Requires only a `aferidor` household repository — no phone, no browser,
  no store account.
when_to_use:
  - "User asks where an item is cheapest, or whether a price they were quoted is good"
  - "User asks whether to change where the household buys something"
  - "User asks what an item used to cost, or whether it went up"
  - "User just came back from shopping / got a receipt and wants the prices recorded"
  - "User asks for a review of the whole basket ('o que dá para economizar?')"
when_NOT_to_use:
  - "User wants to build this week's shopping list → use `aferidor-lista`"
  - "User wants to import a Brazilian NFC-e receipt XML → use `aferidor-nota-fiscal`"
  - "User wants to actually place and pay for an order → use `aferidor-pedido`"
  - "User is asking about a product the household has never bought and has no history for — say so plainly and offer to start recording, do not search the web and present a stranger's price as the household's baseline"
requires:
  - "python3 (3.11+ preferred; 3.9+ works with default thresholds)"
  - "a aferidor household repository (a directory containing aferidor.toml)"
---

# aferidor-precos

Price comparison from the household's own observations.

## The one thing to get right

**Never compare sticker prices.** Compare price per base unit. The `aferidor` CLI
does this for you — the whole reason it exists is that the human eye reads
"R$ 7,49" as cheaper than "R$ 7,90" and does not read "900 ml" as 11% less
product.

Do not do this arithmetic yourself in prose. You will be inconsistent across a
conversation and no one will be able to check your work. Run the command.

## Workflow

### 1. Locate the repository

```bash
cd <the household repo>   # the directory holding aferidor.toml
aferidor check               # confirms it parses; prints counts
```

If `aferidor` is not on PATH, it lives at `~/.local/share/aferidor/bin/aferidor`.
If there is no repository at all, stop and offer `aferidor init <dir>` — do not
invent one.

### 2. Answer the question with the right command

| The user asks | Run |
|---|---|
| "onde o arroz está mais barato?" | `aferidor compare arroz-tio-joao-1kg` |
| "o que dá pra economizar?" / basket review | `aferidor advise` |
| "quanto eu paguei da última vez?" | `aferidor compare <sku>` and read the `última` column |
| "anota que o feijão tava 8,90 no atacarejo" | `aferidor record <sku> <mercado> 8.90 -e '1kg'` |

Add `--json` when you need to compute on the result rather than show it.

### 3. Report the verdict, not just the table

`aferidor compare` returns one of four verdicts. Relay it faithfully:

- **MANTER** — stay. Say *why* it is not worth moving, including the number.
  "O atacarejo está 5% abaixo, e a regra da casa é 8%" is a useful answer.
  "Fique onde está" alone is not.
- **MIGRAR** — move, with the delta and the sample count.
- **ADOTAR** — no incumbent is defined yet; pick the qualified cheapest.
- **COLETAR** — not enough data. **Say this plainly and do not guess.** This is
  the verdict users most want you to override. Do not override it. Offer to
  record more observations instead.

### 4. Persist what you learned

If the user told you a price during the conversation, record it before the
conversation ends — an unrecorded observation is a lost one:

```bash
aferidor record oleo-de-soja atacarejo-online 7.90 -e '1L' -m Soya --fonte site
```

Then note *decisions* (not prices) in `DIARIO.md`, appending a new dated
section. Never edit an old one.

## Recording prices correctly

The `-e/--embalagem` flag carries the whole comparison. Get it right:

| Real world | Write |
|---|---|
| pacote de 1 kg | `1kg` |
| garrafa 900 ml | `900ml` |
| fardo com 6 de 350 ml | `6x350ml` |
| papel higiênico com 16 rolos | `c/16` |
| caixa 12 × 1 L | `12x1L` |
| bandeja avulsa, sem peso | leave empty (counts as 1 unit) |

If the user says "levei 3 pacotes de 1 kg por R$ 20", that is
`-q 3 -e '1kg'` with `preco 20` — quantity times package content, total price.
**Not** R$ 20 per package.

Use `--fonte` honestly: `nfce` (from a receipt — the price actually paid),
`site`/`app` (a listed price, which may not survive checkout), `manual`, `loja`.
A receipt price is worth more than a listed price and the source column is how
anyone can tell them apart later.

## When the data is thin

Three observations per merchant is the floor, and most households start with
zero. That is normal and worth saying out loud: the first three weeks of this
method produce no recommendations at all, only data. A tool that recommends
confidently on week one is lying.

Offer the useful thing instead: record what is known, and name exactly which
item/merchant pairs need one more sample to unlock a verdict.

## Degrading gracefully

- **No `aferidor` on PATH** → the CSV is still readable. Say so, show the user
  `dados/observacoes.csv`, and do the comparison by hand *showing the division*
  (`7.49 / 0.9 = 8.32/L`), flagged as a manual calculation.
- **No repository** → offer `aferidor init`. Do not fabricate a baseline.
- **Item not found** → check for a near-miss slug first
  (`ls itens/ | grep -i <word>`); users type `arroz` for `arroz-tio-joao-1kg`.

## Reference

- `referencia/regra-de-migracao.md` — why 8% and 3 samples, and when to change them
- `referencia/unidades.md` — every package string the normaliser understands
