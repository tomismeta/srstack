# Planning inputs: schema 1

Agent-facing translation reference, not a user questionnaire. Collect and confirm assumptions through the [guided planning workflow](planning.md), then construct or repair JSON internally. Do not dump this table or require users to know field names. Already complete requests need no schema read. Answer first; label calculated results as estimates rather than opening every intake reply with a warning.

The root must be an object with every field below, except optional `detail` and `include_history`. No other root or scenario keys are accepted. Numeric fields accept JSON numbers or numeric strings; strings are preferable for exact decimal entry. All bounds are inclusive. Integer fields require integral values, not booleans or non-integral numbers. Decimal arithmetic uses 50-digit precision; economic output amounts are decimal strings, and counts are integers. This is not exact EVM arithmetic.

### Required run and position fields

| Field | Type / allowed range | Meaning |
| --- | --- | --- |
| `schema_version` | integer, `1` | Input contract version. |
| `mode` | string, `documented` or `stress` | Explicit checked-rule behavior; required with no default. |
| `assumptions_acknowledged` | boolean, `true` | Explicit acknowledgment that the calculation is hypothetical. |
| `days` | integer, 1–365 | Whole-day horizon. |
| `initial_branches` | integer, 1–100 | Own starting branches, shared by all strategies. |
| `initial_credits` | decimal, 0–1e12 | Starting issuance credits; not counted as new accrual. |
| `other_branches` | integer, 0–1e9 | Starting external branch count. |
| `max_branches` | integer, 1–100; at least `initial_branches` | Own expansion cap. |
| `daily_license_limit` | integer, 0–100 | Maximum licenses bought per day. |
| `base_daily_issuance` | decimal, 0–1e12 | Hypothetical global daily issuance before the scenario multiplier. |
| `remaining_issuance_budget` | decimal, 0–1e15 | Gross global issuance budget remaining at day 1. |
| `initial_token_price_eth` | decimal, 0–1000 | Day-1 ETH per token; hypothetical, not an executable quote. |

### Required costs, funding, and exits

| Field | Type / allowed range | Meaning |
| --- | --- | --- |
| `entry_cost_eth` | decimal, 0–1e6 | Explicit initial position cash cost, not inferred from branches or token price. |
| `entry_gas_eth` | decimal, 0–100 | Explicit entry gas assumption. |
| `license_cost_tokens` | decimal, 0–1e12 | Token cost per expansion license. |
| `license_gas_eth` | decimal, 0–100 | External ETH gas cost per successful license purchase. |
| `expansion_budget_eth` | decimal, 0–1e6 | Expansion cash cap, including license gas; excludes entry and exit costs. |
| `buy_cost_markup_pct` | decimal, 0–10000 | Markup on external token acquisition for licenses. |
| `sale_fee_pct` | decimal, 0–100 | Regular terminal sale fee assumption. |
| `sale_slippage_pct` | decimal, 0–100 | Terminal sale slippage assumption. |
| `exit_gas_eth` | decimal, 0–100 | One terminal exit gas charge when any branch is retired. |
| `funding` | string, `external` or `credits` | External token purchase plus gas, or existing credits plus external gas. |
| `selective_target` | integer, `initial_branches`–`max_branches` | Selective strategy's target branch count. |
| `selective_interval_days` | integer, 1–365 | Selective attempts occur on interval + 1, twice interval + 1, and so on. |
| `exit_mode` | string, `all`, `one`, or `none` | Retire all, one, or zero branches at the horizon. |
| `scenarios` | array, 1–9 objects | Independently specified sensitivity cases, each with the exact fields below. |

### Required fields of each scenario

| Field | Type / allowed range | Meaning |
| --- | --- | --- |
| `id` | unique string matching `[a-z0-9-]{1,40}` | Stable case identifier. |
| `name` | plain string, 1–80 characters; no control characters | Display label, never code. |
| `multiplier` | decimal, 0–100 | Constant hypothetical multiplier of base issuance. |
| `other_branch_growth_pct` | decimal, −20–20 | Daily compounded change in external branches. |
| `price_growth_pct` | decimal, −20–20 | Daily compounded change in token price. |
| `resolution_fee_pct` | decimal, 0–100 | Hypothetical fee on credits released at exit. |
| `sale_tax_pct` | decimal, 0–100 | Hypothetical first haircut on gross sale ETH. |

`detail` is optional: `"summary"` (default) or `"full"`. `include_history` is optional: boolean, default `false`; `true` requires `detail: "full"`, otherwise input validation fails with exit 2. These controls affect output only, not economics. There are no economic defaults.

The numeric ranges in these schema tables are **computational bounds**, not claims about publisher or deployed limits. Documented mode also applies the checks in [planning-conformance](planning-conformance.md); stress mode retains the computational bounds while allowing disclosed canonical conflicts.

Validation rejects missing or unknown keys, duplicate JSON keys, invalid enum values, booleans used as numbers, non-finite numbers (`NaN`/`Infinity`), out-of-range values, invalid labels, excessive decimal magnitude/precision, and input exceeding 64 KiB (65,536 bytes). Numeric strings use JSON-number syntax with no surrounding whitespace or leading `+`. Numeric representations are limited to 80 characters, a Decimal coefficient of at most 30 digits, and a Decimal exponent from −18 through 18, before applying the field bounds. Input nesting is limited to eight levels; labels reject Unicode control, format, and surrogate characters.

## Sensitivity and example

For sensitivity analysis, specify one scenario per cell, or up to nine cells in a single `scenarios` array with unique IDs. The five economic scenario fields are explicit for each cell; they do not inherit missing values. Root assumptions remain shared within that invocation. Varying funding, horizon, entry cost, or another root assumption requires a separate explicitly specified invocation. Do not assign probabilities, select a winner, or turn a modeled comparison into financial advice.

The complete [fictional example](../assets/examples/planning.json) is for explicit example/tutorial requests only. It selects schema 1, documented mode and summary detail; none of its numbers is a default, recommendation, live value or parameter authority.

## Current protocol inputs

Prepare a partial assumption sheet from fresh reads, not a stored launch preset. Use `protocol` and `auctions`; use `charter` only when the user supplies a public charter ID. Read the result's status and material errors before proposing values.

| Proposed input | Fresh source and approval boundary |
|---|---|
| Base issuance and multiplier | Use `base_issuance_per_day` and `multiplier`; holding either constant requires approval. A documented ceiling is not the current rate. |
| Position | Use the selected charter's observed branches and pending balance, or the user's explicit hypothetical position. Do not infer ownership or balances. |
| Network and budget | Use same-block branch counts and the counter-based budget difference with their stated meanings. Do not substitute original supply or launch totals. |
| License cost | Only an available auction price can inform a current purchase assumption. Sold-out, paused or unstarted means unavailable—not a last-sale quote or free license. |
| Taxes, fees and gas | Current taxes are observations, not future guarantees. LP fee, slippage and gas remain distinct inputs. Any unsupported amount requires the user's explicit assumption. |
| Strategy and limits | Use documented bounds as constraints and ask for the user's budget, target, cadence, horizon and endpoint. Constraints do not prove current inventory or affordability. |

If live access fails, state the missing input and ask whether the user wants a clearly hypothetical scenario. Do not backfill it from stored observations, launch settings, recap figures or the fictional example. Show only useful proposals and the next questions; obtain approval of complete economic inputs before running the model.

## Deployment-evidence handoff

Use only when the user requests contract-informed planning or provides relevant observations. Read the selected [Robinhood identity records](../assets/entities/robinhood.json) with their shared limits and `sr-protocol-conditions` in [deployment sources](../assets/sources/deployments.json). An ordinary scenario does not require loading these resources or fetching live data.

The packaged `scripts/snapshot.py` offers bounded public reads of fixed Robinhood targets using the publisher-authenticated interface in `assets/interfaces/robinhood-reads.json` (`sr-publisher-read-interface`). This is a **publisher ABI**, not verified source/bytecode correspondence. Use the integrity, chain, code, binding, decoding and common-block checks in [inspection](inspection.md) and [execution](planning-execution.md); do not borrow cross-chain ABIs or treat a selector match as proof. Otherwise keep website values attributed and dated. No automatic refresh, persistence or extra parameters injected into the engine.

| Planning need | Relevant evidence and mapping boundary |
|---|---|
| Starting branches and credits | `charter` view requires the selected public charter ID. `charter_branches`, `charter_pending` and `charter_owner` provide block-scoped state, not proof that the user owns it. Map compatible branches/pending credits to `initial_branches`/`initial_credits` only after approval. No personal position or acquisition cost is packaged; a failed owner read is not a zero balance. |
| External branch count | `total_branches` is global, not `other_branches`. Subtract `charter_branches` only for an existing included charter at the same snapshot; do not subtract a hypothetical new position. One observation supplies no growth rate. |
| Base issuance and multiplier | `base_issuance_per_day` is the unscaled base → proposed `base_daily_issuance`; `multiplier` → proposed scenario multiplier. Multiply once. The frontend's policy-scaled rate and `stream_rate_per_second` (which includes recycling) are not substitutes. Emissions status and owner-configured values are observations, not guaranteed future issuance. |
| Remaining issuance budget | `remaining_gross_budget` is the counter-based difference `ISSUANCE_BUDGET() - cumulativeIssued()` using the publisher's mapping. Require successful compatible readings and a nonnegative result; do not claim it includes every pending/unsettled accrual. It may be proposed as an initial budget estimate with approval. `permanent_removed` is `HARD_CAP() - maxSupply()`, not remaining issuance; supply and pending balances are different quantities. |
| Entry and license cost | `auctions` view supplies daily auction states, inventory, price, floor and last sale observations; founding entry is a separate route outside this reader. A `currentPrice()` value can keep decaying after sellout: it is not a purchasable quote when inactive, paused, sold out or status is unknown. The last sale is historical, not a new quote. Never replace existing acquisition cost with a current auction or whitelist price. |
| Token price, sale fees and tax | `buy_tax_percent` uses `currentTaxBps(true)` and `sell_tax_percent` uses `false`, with basis points divided by 100 for percent. A current sell tax may inform an approved future `sale_tax_pct`, not the separate LP-fee assumption. `pool_initialized` is not a token-price or liquidity guarantee; this reader supplies no token market quote. |
| Withdrawal fee | `zero_amount_withdrawal_fee_percent` is a zero-amount preview, not an amount-specific exit quote or a fixed future resolution fee. The published curve and envelope remain context; user approval is required for any scenario proxy. Missing pressure inputs, timing or availability are not zero. |
| Gas | Addresses do not supply transaction gas usage or network fee assumptions. Use the guided workflow's approved estimates, sensitivity or explicitly labelled exclusions; no state-changing simulation or wallet connection. |

Offer a small **observation → proposed assumption** sheet only for useful compatible values, with material gaps. Obtain approval before mapping them into JSON, especially for any value held constant into the future. Keep URLs, retrieval times, block anchors, derivations and classifications internally beside the input, not as unsupported keys or a mandatory trace dump. A short “RPC snapshot; publisher ABI.” note distinguishes observations from verified-source claims.

For current planning, use requested fresh observations rather than carrying forward an old pre-launch snapshot. Report the actual emissions, pool and auction status; unknown availability stays unknown. A future-active what-if requires explicit approval. Epoch settlement pauses, recycling, dynamic policy/fees, owner configuration changes, liquidity and auction availability are not simulated by the fixed daily engine. Owner addresses or configuration getters establish only what was returned at the block, not immutability, authority completeness or safe governance.
