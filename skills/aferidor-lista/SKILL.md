---
name: aferidor-lista
description: >-
  Builds the household's shopping list from the pantry state, the reorder
  points, the price history and the household doctrine in AGENTS.md. Handles
  "monta a lista da semana", "o que falta em casa", "preciso comprar o quê",
  "faz a aferidor", "build the shopping list", "what are we out of". Produces a
  list grouped by merchant, so each merchant's minimum order and delivery fee
  are visible before anything is bought, and flags items whose price is above
  the household's own historical range. Never places an order — the list is
  handed to a human.
when_to_use:
  - "User asks what to buy, or asks for this week's / this fortnight's list"
  - "User asks what the household has run out of"
  - "User wants a list split by where to buy each thing"
  - "User asks whether to stock up on something now"
when_NOT_to_use:
  - "User wants to compare two specific merchants → use `aferidor-precos`"
  - "User wants to place the order → use `aferidor-pedido`"
  - "The pantry file has not been touched in months — say so first; a list built on stale inventory is worse than no list, because it looks authoritative"
requires:
  - "a aferidor household repository with despensa/ and itens/ populated"
  - "AGENTS.md — the household doctrine; read it before proposing anything"
---

# aferidor-lista

Turning "what's in the house" into "what to buy, and where".

## Read the doctrine first, every time

`AGENTS.md` in the household repository holds the rules that make a list correct
for *this* house: allergies, vetoed brands, who has to approve, what may never
be substituted, the budget ceiling. A list that ignores it is not a rough draft,
it is a wrong answer.

Section 2 (restrictions that do not negotiate) is a hard filter. An allergen
does not enter the list because it was on sale.

## Workflow

### 1. What is actually missing

```bash
aferidor falta --json
```

Four verdicts, and the boring ones carry as much weight as the loud one:

| verdict | what it means | what you do |
|---|---|---|
| `REPOR` | counted today, at or below the reorder point | put it on the list |
| `CONFERIR` | even the slowest rate ever observed reaches the reorder point | ask the person to look, then decide |
| `MANTER` | the dated count still has slack | leave it off |
| `COLETAR` | under 6 purchases, or no dated count | say you do not know — do not guess |

**`CONFERIR` is not `REPOR`.** The command reads purchases, and a purchase is
evidence that somebody bought something, not that the house consumed it.
Stock-ups, promotions, guests and a forgotten receipt all move those intervals.
Never translate `CONFERIR` into "you are out of X" — translate it into "worth a
look before we send this".

Never state a remaining quantity or a run-out date. The tool refuses to compute
them because they are not knowable from this data, and inventing them in prose
is the same error with better grammar.

Read `despensa/*.md` alongside it for the raw counts and the `Confirmado em`
date. Say the age out loud — "contou 3 há 21 dias" — rather than presenting a
three-week-old number as the current state. If the pantry has not been touched
since before the last shop, the quantities are fiction: say so, and offer to
rebuild from the last receipt (`aferidor-nota-fiscal`) instead of pretending.

To see how a household's rhythm actually looks before judging it:

```bash
aferidor historico <sku>        # dated timeline, gaps, observed replenishment
```

### 2. Where each thing should come from

```bash
aferidor advise --json
```

Take the `mercado` from each verdict. Respect `MANTER` — the incumbent stays.
Respect `COLETAR` — for those items, put them wherever the household normally
shops and note that the price is unverified rather than inventing a winner.

### 3. Group by merchant and check the thresholds

Read `mercados/*.md` front matter for `pedido_minimo`, `frete` and
`frete_gratis_acima`. Then do the arithmetic that decides whether the split is
real:

> Split the arroz off to the atacarejo to save R$ 1,50/kg × 5 kg = R$ 7,50.
> The atacarejo has a R$ 150 minimum and R$ 12,90 freight. The rest of that
> merchant's list totals R$ 40. **The split costs R$ 5,40 net.** Keep it in one
> cart this week and revisit when the atacarejo list is bigger.

That paragraph is the actual product. A list that says "buy rice at the
atacarejo" without it is advice that loses money.

### 4. Flag the prices that look wrong

For each line, compare against history. If an item is above its own recent
range, say so with the number — that is when a household catches a price
increase, and it is more valuable than the arbitrage.

### 5. Hand it over

Output a plain list the human can act on: item, quantity, merchant, expected
price, total per merchant, grand total. Then stop.

**Do not place the order.** Do not open an app. Do not "get it ready to
confirm". The list is the deliverable of this skill; ordering is `aferidor-pedido`
and it has its own gate.

## Negotiating with the other people in the house

Most households do not have a single decision-maker, and a list produced without
the other person is a list that gets rewritten in the shop.

If `AGENTS.md` section 1 names someone else, the draft goes to them before it
goes anywhere. Their edits are not corrections to be argued with — a request for
a specific brand of coffee is data about the household, and it belongs in
`itens/cafe.md` under `marca_padrao` so the same argument does not recur monthly.

Sending that message is an outward-facing action. Show the draft, wait for the
user's OK, then send. Never send first.

## Stocking up

Buying twelve of something at a good price is only a saving if the household
consumes twelve before they expire and has somewhere to put them. Before
suggesting it, check: shelf life, storage space, the household's real
consumption rate from the observation history, and whether the money is better
kept liquid.

The failure mode is a cupboard of cheap things nobody eats, which reads as
savings on the receipt and as waste in the bin.

## Degrading gracefully

- **No pantry file** → build the list from reorder points and the last receipt,
  and label it explicitly as a guess. Then offer to start the pantry, since
  everything downstream improves once it exists.
- **No price history** → the list is still useful as a list. Say the prices are
  unknown rather than estimating them.
- **No merchant profiles** → put everything in one list and flag that the
  split-by-merchant advice is unavailable until `mercados/` is filled in.
