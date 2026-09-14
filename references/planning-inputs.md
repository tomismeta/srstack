# Planning inputs: schema 1

Load to construct or repair input, not before executing an already complete request. Return to [planning workflow](planning.md); all planning answers require its visible first warning.

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
