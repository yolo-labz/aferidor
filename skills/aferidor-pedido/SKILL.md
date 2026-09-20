---
name: aferidor-pedido
description: >-
  Governs the last mile — turning an approved shopping list into a placed order.
  Handles "faz o pedido", "compra isso", "coloca no carrinho", "place the
  order", "finaliza a compra". This skill's primary job is to enforce the human
  payment gate and to hand the list back to a person when automation is
  unavailable, which is the normal case. Automated order placement requires a
  dedicated Android device wired for adb; without one, this skill produces a
  copy-pasteable list and stops. It NEVER pays for anything without an explicit,
  in-the-moment human confirmation.
when_to_use:
  - "User has an approved list and wants to order"
  - "User asks whether the household can automate ordering, or what that needs"
  - "User asks to resolve out-of-stock substitutions on an order in progress"
  - "An order was delivered and needs reconciling against what was charged"
when_NOT_to_use:
  - "The list has not been approved by the household yet → use `aferidor-lista` first"
  - "User wants price research → use `aferidor-precos`"
  - "User asks you to save, store or reuse card details — refuse; see below"
requires:
  - "TIER 3 (automated placement): a dedicated Android device with USB debugging, adb, and the merchant app logged in. THIS IS OPTIONAL AND USUALLY ABSENT."
  - "TIER 1 (default): nothing. A human orders from the list."
---

# aferidor-pedido

The last mile, and the gate in front of it.

## Default assumption: there is no phone

**Automated ordering is the exception, not the baseline.** It needs a dedicated
Android device — a spare handset, in developer mode, with adb reachable, the
merchant app installed and logged in, and nothing else competing for the
foreground.

Most households setting this up do not have one, and should not buy one to try.
That is fine, and it is not a degraded experience: everything valuable in this
method — the price history, the normalisation, the migration rule, the
merchant thresholds, the list — happens before the order. The order itself is
five minutes of tapping that a human does perfectly well.

So the default path is:

1. Produce the final list, grouped by merchant, with expected prices.
2. Format it so it can be pasted into the merchant's search box one line at a
   time, or read aloud in a shop.
3. **Stop.** The human orders and pays.
4. When the receipt arrives, come back with `aferidor-nota-fiscal` and record what
   was actually charged.

Say this plainly when a user asks why it will not just buy the groceries. Do not
apologise for it and do not offer workarounds that route around the gate.

## The gate — non-negotiable

**The person finalises and pays, by hand, in the merchant's own app.** That is
the decision (25/08/2026), and it is the whole safety model. The software may
build the cart; the last step belongs to a human.

So: **the software never completes a payment on its own**, at any tier.

Before any irreversible step — placing an order, confirming a cart, accepting a
substitution on a restricted item, sending a message to a merchant — show the
human exactly what is about to happen and wait for an explicit yes.

- Consent is per-action and per-occasion. "You approved this yesterday" is not
  approval for today.
- Show the final total, the merchant, the payment instrument and the delivery
  address before asking.
- A silent failure is better than a silent purchase. If you cannot confirm what
  state the cart is in, stop and describe what you see.

This is not caution theatre. An unattended agent that orders the wrong thing
once destroys more value in trust than the method generates in a year, and under
Brazilian consumer law the household — not the software — owns the resulting
dispute.

Note how little is actually given up. Everything valuable happens *before* the
button: deciding what to buy, where, and when to change nothing. Tapping
"finalizar" is thirty seconds of human time, and it is the cheapest insurance
the method has.

## Cards and credentials

- **Never** write a card number, CVV, password or session token into any file in
  the repository, into a commit, into a log, or into your own output.
- Credentials come from the user's own password manager at the moment of use and
  go nowhere else.
- Never store them "to speed up next time". There is no next time worth that.
- If the user pastes a card number into the conversation, tell them, and do not
  echo it back.

## Tier 3: when a dedicated device does exist

The setup, the adb invocations and the substitution-modal handling are in
`referencia/tier-3-android.md`, kept separate because almost nobody needs it.
The load-bearing points:

- **Pin the device.** `ANDROID_SERIAL` must be set explicitly. A second device
  on the network silently absorbs every command and returns empty dumps, which
  looks exactly like a broken script.
- **Never tap raw coordinates from an old screen dump.** Re-read the UI, resolve
  the element, then tap. Coordinates go stale the instant the app re-lays out,
  and a stale tap in a checkout flow is how you buy the wrong thing.
- **Out-of-stock modals are the hard part**, not the happy path. The choice
  between "substitute" and "refund" is a household policy decision (`AGENTS.md`
  section 3), not a UI puzzle to solve as fast as possible. Items the doctrine
  marks "never substitute" get refunded, always, even when the substitute is
  obviously fine.
- **Expect it to break.** App layouts change without warning. When a step does
  not match what the reference describes, stop and hand back to the human —
  do not improvise taps in a payment flow.
- Leave the device as you found it: no lingering display-geometry overrides, no
  disabled packages.

## Reconciling the delivery

The order is not done when it is placed. When it arrives:

- Compare charged against expected, line by line.
- Record what was substituted, what was missing, and what was refunded.
- Import the receipt (`aferidor-nota-fiscal`) so the *paid* prices, not the listed
  ones, enter the history.
- Append a dated entry to `DIARIO.md` covering anything surprising — a refused
  card, an antifraud block, a substitution the household hated. Six months later
  that entry is the only reason anyone remembers why a rule exists.

## Degrading gracefully

Every one of these is a normal outcome, not an error:

- **No Android device** → produce the list, stop. This is the default.
- **Device present but adb unreachable** → say so once, produce the list, stop.
  Do not troubleshoot a phone for twenty minutes when the fallback takes five.
- **App layout does not match the reference** → stop, screenshot, describe, hand
  back.
- **Payment declined** → do not retry, and do not try a second card. A decline
  is frequently an antifraud rule that a retry escalates. Report it, note the
  time, and let the human decide.
