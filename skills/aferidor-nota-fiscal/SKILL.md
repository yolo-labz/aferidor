---
name: aferidor-nota-fiscal
description: >-
  Reads Brazilian electronic consumer receipts (NFC-e, model 65) and folds the
  prices actually paid into the household price history. Handles "importa essa
  nota", "lê o cupom fiscal", "quanto foi a compra do mês passado", "puxa as
  notas do SEFAZ", "parse this receipt XML". Works on authorised NFC-e XML files
  the user already downloaded from their own state tax portal using their own
  CPF. Receipt prices are ground truth — they record what was paid, after
  discounts, unlike a listed price on a website.
when_to_use:
  - "User has NFC-e / cupom fiscal XML files and wants them read or imported"
  - "User asks what a past shopping trip actually cost, item by item"
  - "User wants to reconcile a delivery against what was charged"
  - "User asks how to get their receipts out of the state tax portal"
when_NOT_to_use:
  - "User wants to compare merchants → use `aferidor-precos`"
  - "User has a paper receipt or a photo, not an XML — this skill parses XML only; offer manual `aferidor record` instead"
  - "User asks you to log into a government portal on their behalf without them present — never do this; see the human gate below"
requires:
  - "python3"
  - "NFC-e XML files the user has already downloaded (this skill never fetches them)"
---

# aferidor-nota-fiscal

Brazilian NFC-e receipts into price history.

## Why receipts beat scraping

A price on a store page is a claim. A price on an NFC-e is a fact: it is the
amount that cleared, after the promotion, after the club discount, after the
item that turned out to be a different size than the page said. It carries a
timestamp, a CNPJ and a 44-digit access key, so it is auditable.

Every Brazilian retail sale to a consumer generates one. Most people never look
at theirs. That corpus is the single most valuable asset in this whole method,
and it costs nothing.

## Getting the files — the human does this part

The XML comes from the user's own state tax portal (in Pernambuco: SEFAZ-PE
e-fisco), authenticated with their own gov.br account and their own CPF.

**You do not do this step.** It requires an interactive government login with
two-factor authentication. Walk the user through it, wait, and pick up once
files exist on disk:

1. User logs in to their state's SEFAZ portal with gov.br.
2. User finds the "download de notas" / "consulta NFC-e" area, enters a date
   range and their CPF, and downloads the ZIP.
3. User unzips it somewhere, e.g. `notas/2026-08/`.
4. You take over.

A per-state walkthrough is in `referencia/sefaz-por-estado.md`. Portals differ
by state and change without notice; if the walkthrough is stale, say so rather
than improvising instructions for a government website.

The 44-digit key on the bottom of a paper receipt (or its QR code) also resolves
to the same document on the state portal, one at a time — the fallback when
bulk download is not available.

## Workflow

### 1. Look before importing

```bash
aferidor nfce notas/2026-08/            # human-readable dump, changes nothing
aferidor nfce notas/2026-08/ --json     # structured, for computing on
```

Read the output back to the user: date, merchant, total, item count. This is
also the moment to catch the wrong file — a model-55 NF-e (a business invoice)
will parse but is not a grocery receipt.

### 2. Import

```bash
aferidor nfce notas/2026-08/ --importar
```

This appends one observation per line item. It is append-only and idempotent
only by your care — **importing the same directory twice duplicates every
row.** Check `dados/observacoes.csv` for the receipt key (the `observacao`
column holds the first 12 digits) before re-importing.

### 3. Merge the SKUs — the part that actually takes time

Receipts name things the way the retailer's cash register does:

```
ARROZ T JOAO T1 1KG
ARR TIO JOAO TP1 PC 1KG
ARROZ BCO TIO JOAO 1KG
```

Three names, one product, three useless slugs. Until they are merged, the
comparison sees three items with one observation each and correctly refuses to
say anything.

Do the merge deliberately, not eagerly:

1. `cut -d, -f2 dados/observacoes.csv | sort | uniq -c | sort -rn` to see the
   spread.
2. Group by hand. **Ask the user before merging anything ambiguous** — "arroz
   branco" and "arroz integral" are different products and merging them
   silently poisons the history in a way that is very hard to notice later.
3. Rewrite the `sku` column for the group to the canonical slug.
4. Create `itens/<slug>.md` with the front matter.

Prefer the EAN (barcode) when the receipt carries one — it is the only truly
stable key. Many receipts emit `SEM GTIN`, which is why this is manual work.

The full procedure, including a worked example, is in
`referencia/casar-skus.md`.

## Privacy — read this before you touch the files

An NFC-e XML contains the buyer's **CPF**, the merchant's CNPJ and address, and
a complete itemised record of what the household consumes. That last one is more
revealing than people expect: it shows medication, alcohol, baby formula,
pregnancy tests.

Rules:

- **Never commit raw XML to a shared or public repository.** The template's
  `.gitignore` excludes `notas/` for this reason. Do not "helpfully" remove that
  line.
- Derived observations (date, sku, merchant, price) are safe to keep — they
  carry no CPF.
- If the user asks to publish or share any of this, treat it as an irreversible,
  outward-facing action: show exactly what would be exposed, and wait for an
  explicit yes.
- If a receipt carries a CPF that is not the user's, stop and ask. It happens
  when someone pays for a relative.

## Degrading gracefully

- **No XML, only a photo or paper** → parse nothing. Read the items to the user
  and record the important ones with `aferidor record --fonte loja`. Say that a
  photo is not a substitute, because the useful thing about the XML is that it
  is machine-checkable.
- **Portal is down or the login fails** → this is a government website; it
  happens. Do not retry in a loop. Say so and offer the single-key lookup.
- **XML parses but has no items** → it is probably a cancellation or an
  `evento` file, not a sale. Skip it and say which file.
