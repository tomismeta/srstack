# Inspect: public state, price and gross value

Use the smallest sufficient set of host public reads. These topics are not a required sequence. Apply [safety](safety.md#public-retrieval-and-calls).

## Common question paths

Prefer authenticated state for balances, ownership, supply, permissions, positions, treasury and current auctions; events for executions/flows, markets for prices, documents for design. A current balance needs no history scan; an explanation needs no unrelated refresh.

A known ID needs only relevant state/dependencies; a supplied amount needs no balance lookup. Fetch prices for requested valuation, not every STANDARD amount. Ask only for missing user choices.

### Branch scope and earnings

For a charter, report requested branches, whole-charter accrued ledger balance and as-of time. Add pace only with established deployed calculation and inputs, not a method-name inference. Daily equivalent is not earned today or guaranteed income. See [accrual models](research-workflow.md#earned-only-projections-and-reinvestment).

For an address, use ownership enumeration or a bounded index accounting for transfers/burns; verify candidates at the anchor. Incomplete discovery means identified positions, not all positions. Ownership is not user authentication. Historical earnings need [flow accounting](research-workflow.md#flows-principal-income-and-fees), not pending differences. S-Bills need actual position evidence, not charter balances or preview samples.

### Supplemental public reads

Discover runtime deployments/interfaces through publisher evidence, explorers, registries and authenticated relationships; no fixed allowlist. Packaged evidence is dated, not current configuration. Use [host tools](execution.md); keep installed resources unchanged.

## Authenticate before ABI reads

Establish chain, full address, role and generation. Pin code, relationships and state to a block number/hash/time; retain retrieval time. Authenticate the interface by deployment/source correspondence or independently retrieved publisher ABI linked to that chain/address. Parse ABI as data, never execute downloaded code.

Establish types, strict decoding, scales and relevant proxy/module relationships. Code, names or selectors alone prove neither semantics nor source equivalence. Authenticate material dependencies; unresolved evidence blocks only dependent conclusions.

## Read the scoped state

Reuse anchored observations; batch compatible reads and bound pages/calls/bytes/time. Never substitute latest for unavailable history. Failures and incomplete enumeration are unknown, not zero. Order IDs need authenticated mapping to charters; bids/fillability are not purchases.

### Units and financial interpretation

Preserve raw scales; use [exact accounting](research-workflow.md#compute-with-explicit-units). Ledger credits, wallet tokens, branches and gas funds differ. Pending is whole-charter, not proof all funds were earned. Its mark is gross before withdrawal/trading costs, not net proceeds, resale value or earning capacity. Zero-amount previews do not establish amount-specific fees.

### Supply, restrictions and control context

Distinguish burns, ledger retirement, conversion, cap reduction, issuance budget and headroom under deployed semantics; none alone attributes buybacks. Retained tokens are not burns or holder income. Enabled/effective restrictions, configured/effective limits, queued/active policy and pending/completed ownership differ. Addresses prove neither complete authority nor transaction success.

## Anchor any price separately

Authenticate asset/market identity, units and methodology. Retain provider/retrieval time; quote time stays unknown unless supplied. Cache/trade/creation timestamps are not quote times. State and prices need not be atomic. Missing denominations remain unavailable; conversions need evidenced rates or labelled assumptions. Indicative price is not executable proceeds.

### Auction interpretation

Interpret start, pause, inventory and price together; a post-sellout curve value is not purchasable. Distinguish stored rounds, elapsed schedule and effective getter logic; cadence versus cap windows; last-sale storage versus history. Lazy-roll time is not scheduled opening. Do not use stale counters as effective inventory or unchanged state as empty rounds. See [history](auction-history.md).

## Report observations and gaps

Lead with the result or gap, units, short as-of anchor and material limitations. Keep raw evidence/derivations for requested detail. Partial success is not complete history or a future guarantee.

### Original HTTP failure evidence

Preserve bounded safe original-response diagnostics, not a new probe. Denial identifies that request, not an unconfirmed cause or global outage. See [access boundaries](safety.md#public-retrieval-and-calls).

## Requested analysis beyond inspection

Separate current state, history and forecasts. See [models](research-workflow.md) for earned budgets, effective purchase timing, costs and epoch boundaries, and [safety](safety.md#preparation-and-wallet-boundary) for preparation limits.
