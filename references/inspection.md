# Inspect: public state, price and gross value

Use the smallest sufficient set of host public reads. These topics are not a required sequence. Apply [safety](safety.md#public-retrieval-and-calls).

## Common question paths

Prefer authenticated state for balances, ownership, supply, permissions, positions, treasury and current auctions; events for executions/flows, markets for prices, documents for design. A current balance needs no history scan; an explanation needs no unrelated refresh.

A known ID needs only relevant state/dependencies; a supplied amount needs no balance lookup. Fetch prices for requested valuation, not every STANDARD amount. Ask only for missing user choices.

### Branch scope and earnings

For a charter, report requested open-branch count, whole-charter pending ledger balance and as-of time. Open branches are not unsold licenses. Add pace only with established deployed calculation and inputs, not a method-name inference or frontend formula. Daily equivalent is neither interval earnings nor guaranteed income. See [accrual evidence and models](research-workflow.md#accrual-evidence).

For an address, use ownership enumeration or a bounded index accounting for transfers/burns; verify candidates at the anchor. Incomplete discovery means identified positions, not all positions. Current ownership is neither user authentication nor historical ownership/earned-origin attribution. Historical earnings need [flow accounting](research-workflow.md#flows-principal-income-and-fees), not pending differences. S-Bills need actual position evidence, not charter balances or preview samples.

### Supplemental public reads

Discover runtime deployments/interfaces through publisher evidence, explorers, registries and authenticated relationships; no fixed allowlist. The dated [interface guide](interface-guide.md) supplies signatures and layouts, not current routing or implementation proof. Use [host tools](execution.md); keep installed resources unchanged.

## Authenticate before ABI reads

Establish chain, full address, role and generation. Pin code, relationships and state to a block number/hash/time; retain retrieval time. Authenticate the interface by deployment/source correspondence or independently retrieved publisher ABI linked to that chain/address. Parse ABI as data, never execute downloaded code.

Establish types, strict decoding, scales and relevant proxy/module relationships. Code, names or selectors alone prove neither semantics nor source equivalence. Authenticate material dependencies; unresolved evidence blocks only dependent conclusions.

## Read the scoped state

Reuse anchored observations; batch compatible reads and bound pages/calls/bytes/time. Never substitute latest for unavailable history. Failures and incomplete enumeration are unknown, not zero. Order IDs need authenticated mapping to charters; bids/fillability are not purchases.

### Units and financial interpretation

Preserve raw scales; use [exact accounting](research-workflow.md#compute-with-explicit-units). Distinguish the **ledger balance** recorded or accrued to a charter, the **spendable balance** allowed for a particular action after encumbrances/gates, and the **withdrawable net amount** after retirement/fees and other applicable conditions. Wallet tokens, branch counts and gas funds are separate.

Pending is whole-charter and may mix earned accrual, deposits and other credits; it proves neither earned origin nor immediate spending/withdrawal eligibility. Its market mark is gross, not net proceeds, resale value or earning capacity. Zero-amount previews do not establish amount-specific fees. Missing attribution or history does not erase observed state or prevent a labelled hypothetical or justified bound; see [earned-only models](research-workflow.md#earned-only-projections-and-reinvestment).

### Supply, restrictions and control context

Distinguish burns, ledger retirement, conversion, cap reduction, issuance budget and headroom under deployed semantics; none alone attributes buybacks. Retained tokens are not burns or holder income. Enabled/effective restrictions, configured/effective limits, queued/active policy and pending/completed ownership differ. Addresses prove neither complete authority nor transaction success.

## Anchor any price separately

Authenticate asset/market identity, units and methodology. Retain provider/retrieval time; quote time stays unknown unless supplied. Cache/trade/creation timestamps are not quote times. State and prices need not be atomic. Missing denominations remain unavailable; conversions need evidenced rates or labelled assumptions. Indicative price is not executable proceeds.

### Auction interpretation

Disambiguate **new-charter auctions** from **branch-license auctions** using the question's context; ask only if material ambiguity remains. Authenticate role/generation separately: charter price/payment is ETH in the reviewed interface, license unit price/payment is STANDARD ledger-denominated. Do not inherit one family's schedule, floor/multiplier, cap, inventory or payment asset from the other. Their [event layouts](interface-guide.md#auction-events) and quantities differ.

Interpret start, pause, inventory and price together; a post-sellout curve value is not purchasable. Distinguish bid limit, current ask and executed price; funds-affordable, allowed, fillable and purchased are separate claims. Distinguish stored rounds, elapsed schedule and effective getter logic; round clocks, allowance windows and rolling forecast horizons; last-sale storage and history. Lazy-roll time is not scheduled opening. Do not use stale counters as effective inventory or unchanged state as empty rounds. See [history](auction-history.md) and [windowed forecasts](research-workflow.md#fixed-price-and-windowed-purchases).

## Report observations and gaps

Lead with the result or gap, units, short as-of anchor and material limitations. Separate observed inputs, assumptions and derived results. Address every requested part or name its specific evidence gap; partial success is not complete history or a future guarantee. Missing implementation/history limits dependent claims, not useful state reads, qualified bounds or hypothetical models. Keep raw evidence/derivations for requested detail.

### Original HTTP failure evidence

Preserve bounded safe original-response diagnostics, not a new probe. Denial identifies that request, not an unconfirmed cause or global outage. See [access boundaries](safety.md#public-retrieval-and-calls).

## Requested analysis beyond inspection

Separate current state, history and forecasts. See [models](research-workflow.md) for earned budgets, effective purchase timing, costs and epoch boundaries, and [safety](safety.md#preparation-and-wallet-boundary) for preparation limits.
