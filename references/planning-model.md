# Planning model and result detail

Model `"1"`, schema `1`. Return to [planning workflow](planning.md) for execution and its mandatory visible warning; [inputs](planning-inputs.md) defines the computational bounds. Arithmetic uses 50-digit Decimal precision, not exact EVM arithmetic.

## Published mechanics versus fixed proxies

The refreshed whitepaper publishes the unscaled **700,000 STANDARD/day launch base**, an owner-only downward base-rate ratchet, the multiplier epoch policy (0.2–1.25, launch 1, launch epoch 3 days), and a quadratic withdrawal-fee curve driven by system-wide trailing-seven-day withdrawals and remaining bank balances. These are publisher statements, not verified source-code/ABI correspondence or live configuration. Earlier redacted evidence remains dated history; those publications are no longer described as unavailable.

Model `"1"` still uses explicit fixed base issuance, multiplier, license cost and resolution-fee inputs. It does not execute the published dynamic policy, auction equations or withdrawal settlement. No economic defaults are introduced; holding a launch value constant is itself a future assumption. The reviewed [partial conformance checks](planning-conformance.md) enforce the documented base-rate ceiling, multiplier bounds and resolution-fee envelope, not a live rate, dynamic path or particular withdrawal fee; projection arithmetic is unchanged.

The whitepaper's launch tax statements conflict (§12 90%/90% versus §15 20%/40%, toward 2%/3%), as do the license auction's geometric-to-floor equation (§7) and four-hour gap-halving prose (§§7–8). No executable interpretation is chosen. The published multiplier equation's zero-signal hold versus the regime table's zero-flow contraction description also needs implementation correspondence. Source formulas remain evidence strings, not runnable algorithms.

## Model order and accounting

Each case runs three independent counterfactual strategies from the same initial branches and credits:

- **keep** buys no licenses.
- **selective** attempts one license on days `selective_interval_days + 1`, `2 * selective_interval_days + 1`, and so on until its target, subject to the daily limit and cap.
- **aggressive** attempts up to the daily license limit each day until the maximum branch count.

Day 1 starts at the supplied token price and external branch count. At the **start of each day**, attempts use that day's price, existing credits, and remaining expansion cash budget. Successful purchases add whole own branches before that day's accrual. An unaffordable discrete attempt is skipped: no partial branch, debit, or gas charge. Caps and targets still apply.

For external funding, each license costs `license_cost_tokens * start_price * (1 + buy_cost_markup_pct / 100)` in token-purchase ETH, plus `license_gas_eth`. For credits funding, a license consumes `license_cost_tokens` of already available credits and the external ETH gas charge; it never tops up missing credits by buying tokens. Initial credits are available on day 1, but a day's later accrual cannot fund a start-of-day purchase. This **credits-only funding path is a model hypothesis**, not a claim that deployed contracts accept credits for licenses. Its ETH budget still covers gas; markup does not convert credits spending into cash spending.

Next, gross global issuance is `min(base_daily_issuance * multiplier, budget_remaining)`. The supplied base is **unscaled**; the multiplier is applied once, not to an already-scaled daily rate. Own accrual is that amount times `own_branches / (other_branches + own_branches)`, after purchases. This denominator includes the strategy's own expansion: additional own branches dilute its per-branch share as well as increasing its total share. Gross global budget depletes once per day along the common exogenous path, not once per strategy and not merely by the user's allocation. Credit spending, burns, and cancellations do not refill it. The documented 900M original issuance budget is not an observed remaining balance.

At day end, external branches and token price compound by their respective daily growth percentages. External branches may become fractional as an aggregate approximation; own branches remain whole. All strategies use the same exogenous price, external-branch, and gross-budget paths; they are not competing participants in one run. The terminal price is the price after the final day's compounding, also reported in that day's end-state history.

### Terminal exit and cash comparison

For pre-exit branches `b` and retired branches `k`, `all` sets `k = b`, `one` sets `k = 1`, and `none` sets `k = 0`. Gross released credits are `credits_before_exit * k / b`; the rest remain credits on the retained position. The supplied fixed resolution fee is applied to released credits, and `wallet_tokens_before_sale` is released credits minus that fee. Full exit closes all branches and leaves zero credits; partial or no exit retains branches and credits explicitly. This pro-rata model does not compute the published pressure curve or establish real commit timing, ledger/mint ordering, fee redistribution or settlement success.

The model assumes **all released wallet tokens are sold** at the terminal price. Haircuts are sequential:

1. `gross_sale_eth = wallet_tokens_before_sale * final_token_price_eth`.
2. `sale_tax_eth = gross_sale_eth * sale_tax_pct / 100`.
3. `sale_fee_eth = (gross_sale_eth - sale_tax_eth) * sale_fee_pct / 100`.
4. `sale_slippage_eth = (gross_sale_eth - sale_tax_eth - sale_fee_eth) * sale_slippage_pct / 100`.
5. Estimated recovered ETH is the remainder.

This ordering and fee basis are **model assumptions**, not an authenticated protocol tax formula, a trading simulation, or a guarantee of liquidity or executable price. Published directional trading rates do not establish an additional separate charge; callers must explain fee-versus-tax assumptions rather than automatically counting the same charge twice. Exit gas is charged once only when `k > 0`. Total cash outlay is entry cost + entry gas + expansion cash (including license gas) + charged exit gas. `net_cash_eth` is recovered ETH minus that outlay. `delta_vs_keep_eth` compares this cash result with keep under the same scenario and exit mode.

There is **no liquidation or residual price valuation** for a retained charter, retained branches, or retained credits. Partial/no-exit cash P&L is not total return, and a negative cash result does not price the retained position. Entry cost must be explicit even for an existing position; choosing sunk-cost exclusion is a stated cash-accounting assumption, not an automatically inferred zero.

`break_even_price_eth` is available only for `exit_mode: "all"` with a positive denominator:

`total_outlay_eth / (wallet_tokens_before_sale * (1 - sale_tax_pct/100) * (1 - sale_fee_pct/100) * (1 - sale_slippage_pct/100))`.

Otherwise it is `null`, including partial/no exit. It is a terminal-price threshold holding the modeled purchases, accrual, costs, and haircuts fixed—not a forecast, a path-consistent rerun, or a net branch price. Changing the price path can change purchase affordability and invalidate those fixed quantities.

## Output selection

Top level: `schema_version: 1`, `model_version: "1"`, `detail`, `mode`, `classification: "hypothetical"`, `warning`, normalized `assumptions`, `conformance`, `limitations`, and `scenarios`. Economic decimals are normalized decimal strings, counts are integers; the engine does not authenticate provenance. Every scenario retains `id`, `name`, `warning`, `final_token_price_eth`, and three `results`; every strategy retains the exact warning too. JSON warnings never replace the first visible warning line.

`detail: "summary"` is the default. Normalized inputs appear once in root `assumptions`; [compact conformance](planning-conformance.md) shares canonical evidence by parameter ID. Each strategy retains exactly:

- `strategy`, `warning`;
- `branches_before_exit`, `branches_retired`, `branches_after_exit`, `charter_retained`;
- `credits_accrued`, `credits_spent`, `credits_retained`, `wallet_tokens_before_sale`;
- `expansion_eth_spent`, `total_outlay_eth`, `estimated_eth_recovered`, `net_cash_eth`, `delta_vs_keep_eth`, `break_even_price_eth`;
- `licenses_bought`, `skipped_attempts`.

Summary omits purchase records, daily history and per-fee drilldown, not conformance or evidence boundaries. Top-level limitations retain partial checks; published mechanics versus fixed proxies; unresolved fee application, dynamic policy, auction conflicts and credits-payment feasibility; absent residual valuation; and the lack of quotes or contract verification.

`detail: "full"` returns full conformance and strategy accounting: credits before exit/released, resolution fee, license tokens purchased, token-purchase ETH, license gas and each sequential sale deduction, alongside the summary fields. `purchases` records each purchase day's `day`, `branches_added`, `license_tokens_spent`, and `external_eth_spent`; a credits-funded purchase is not an external token purchase.

Credit accounting is `initial_credits + credits_accrued - credits_spent = credits_released + credits_retained`, subject to finite decimal precision. Released credits are before the resolution fee, not identical to wallet tokens. Initial credits are not newly accrued yield.

`include_history: true` requires `detail: "full"` (otherwise exit 2), adding each strategy's bounded daily end-state `history`: `day`, `branches`, `other_branches`, `credits`, `token_price_eth`, and cumulative `expansion_eth_spent`. At most nine cases × three strategies × 365 days. History is a hypothetical path, not observed activity or realized return. Neither detail nor history changes economics.

## Reporting

Start with the exact workflow warning. State whether the packaged engine ran; separate publisher claims, observations with provenance, future assumptions and calculated hypothetical outputs. Report explicit mode, checked scope/conflicts and unresolved semantics alongside comparisons, not just a cap match. Keep cash-versus-retained accounting visible. A documented blocked run has no numerical strategy results. These are counterfactual strategies, not investment recommendations; do not assign probabilities or select a winner. No financial action, source refresh, persistence or monitoring is implied.
