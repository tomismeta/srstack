# Planning conformance and evidence

Return to [planning workflow](planning.md) for execution and the required visible first warning. Checks are partial publisher-statement comparisons, never contract or position verification.

## Mode choice and checked-rule scope

Use these three safeguards together:

1. **Documented-rules mode:** require `mode: "documented"` for a comparison intended to stay within the supported packaged statements. Known conflicts block calculation before any numerical strategy result. Passing these partial checks does not establish protocol feasibility.
2. **Explicit stress mode:** departures require the user's explicit `mode: "stress"`. Known conflicts remain prominently reported, but calculation may proceed within the same computational bounds. Never silently switch modes, alter conflicting inputs, or suggest stress removes missing-input requirements.
3. **Assumption/conformance report:** accompany every computed comparison with its fresh report, conflicts, unresolved semantics, provenance, and model limitations. On a documented conflict, show the blocked report instead of numerical results. No mode, report category, or package hash certifies a contract or actual position.


Schema 1 requires an explicit mode. Both modes load and validate the same fixed canonical data; package-data failure blocks both with no unconstrained fallback.

The engine resolves supported rules by canonical parameter ID, not economic constants copied into this guide or Python. The following are the complete **supported checks**, not a complete protocol rulebook:

| Input path | Relation | Canonical parameter ID | Documented unit / evidence boundary |
| --- | --- | --- | --- |
| `initial_branches`, `max_branches`, `selective_target` | each ≤ cap | `maximum-branches` | `branches per charter`; publisher design statement, not position verification. |
| `daily_license_limit` | ≤ cap | `licenses-per-charter-per-day` | `licenses per charter per day`; not global auction availability. |
| `remaining_issuance_budget` | ≤ total | `issuance-budget` | `STANDARD cumulative issuance`; an upper bound, not an observed remaining balance. |
| `scenarios.<index>.multiplier` | ≥ floor; ≤ ceiling (two checks) | `multiplier-floor`, `multiplier-ceiling` | `multiplier`; documented whitepaper policy bounds, not verified deployed configuration or a future path. |
| `base_daily_issuance` | ≤ launch ceiling | `base-issuance` | `STANDARD per day`; unscaled launch ceiling, not a current rate or constant future path. |
| `scenarios.<index>.resolution_fee_pct` | ≥ floor; ≤ ceiling (two checks) | `resolution-fee-floor`, `resolution-fee-ceiling` | `percent`; published fee envelope, not execution of the pressure curve or verification of a particular withdrawal fee. |

The current multiplier checks use the documented whitepaper bounds, not the earlier `frontend-policy-range` publication. That frontend record remains packaged historical context and is validated as data, but does not supply active conformance bounds. Each active bound retains its canonical value, unit, status, source IDs and locator. Known constraint values must be finite and nonnegative; caps must be integral, the branch maximum positive, and each multiplier or resolution-fee floor no greater than its ceiling. Active numeric bounds require `documented-visible` status and the exact units above; percentage bounds must not exceed 100. Missing, null or malformed required bounds fail closed in both modes; they never fall back to the frontend or caller assumptions.

Source publication and executable applicability are separate:

- `base_daily_issuance` (`base-issuance`): the whitepaper documents **700,000 STANDARD/day unscaled at launch**, with an owner-decreasable rate that cannot be raised back. This supports an upper-envelope check, not authentication of the current rate. The engine multiplies the supplied base by the supplied multiplier once. Holding either constant over the future horizon is still an explicit assumption; neither is auto-filled or authenticated as current.
- Scenario `multiplier` (`multiplier-update-rule`): the whitepaper publishes the epoch rule, 0.2–1.25 bounds, launch multiplier 1, and launch epoch length 3 days. A fixed scenario multiplier is not execution of that dynamic policy, even inside the bounds. The equation's zero-signal hold and the regime prose's zero-flow contraction language require implementation correspondence, not an invented transition.
- Scenario `resolution_fee_pct` (`resolution-fee-formula`): the source publishes the quadratic withdrawal curve and system-wide trailing-seven-day pressure basis. The documented 2%–60% envelope is checked, but an in-range fixed fee remains a proxy; no authenticated pressure observations, commit timing or settlement ordering are supplied by this model.
- `license_cost_tokens` (`license-floor-formula`): the published floor is not a fixed executable auction quote. Section 7's geometric-to-floor equation and sections 7–8's four-hour gap-halving prose conflict. Neither becomes a numerical auction implementation here.
- `sale_fee_pct` (`trading-fee`) and scenario `sale_tax_pct` (`launch-trading-tax-curve`): steady-state directional rates are published, but launch tax claims conflict (§12: 90%/90%; §15: 20%/40%, both toward 2%/3%). A separate fee haircut must not silently double-count a source-described trading tax. Timing, basis, composition and executable application remain unchecked; no conflicting launch schedule is selected.
- Credits funding remains unresolved payment feasibility, not a verified way to buy licenses. `entry_cost_eth` remains an unresolved acquisition-context assumption: `whitelist-liquidity-fee` is context for a specific mint route, not a universal entry price or an enforced generic cost.

These unresolved classifications identify **future assumptions or unverified model application**, not missing published rates, missing user inputs, or a claim that the withdrawal curve is redacted.

Nullable or otherwise unknown source records remain unknown; do not replace supplied assumptions with null, infer an executable fee or policy rule, or automatically apply newly populated formulas without an explicitly reviewed mapping. Formula strings are evidence, never evaluated code. Other branch growth and global auction inventory, continuous accrual approximated by daily steps, fee redistribution, dormancy, credit-payment feasibility, fee/tax bases, sequential haircuts, and absent residual valuation remain explicit unchecked model assumptions. The existing 900M original issuance budget is an upper bound only, never an inferred remaining balance. Passing the supported checks does not establish that any or all scenarios are protocol-feasible.

## Report shape

Both details contain `mode`, `status` (`within_checked_rules`, `conflicts_allowed_in_stress`, or `blocked`), `scope: "partial checks against packaged publisher statements, not contract verification"`, `contract_verified: false`, `counts` (`checked`, `conflicts`, `unresolved`), `constraints`, `conflicts`, `inputs`, `unresolved`, and `parameter_files`. Stress without conflicts may be `within_checked_rules`; that is not a validity certificate. Input cannot override the freshly generated report.

Each `parameter_files` entry identifies one fixed `path`, `sha256` of raw bytes, and packaged `reviewed_at`. Hashes/dates identify the records used, not source refresh or live verification.

### Summary (default)

- `constraints` and `conflicts`: compact rows `{input_path, provided_value, relation, parameter_id, conforms}`.
- `inputs`: `{path, classification}` for every economic, position and decision field and scenario numeric field (for example `scenarios.0.multiplier`). Values live once in root normalized `assumptions`; all origins are `user_supplied`. Version, acknowledgment, output controls, IDs and labels are not classified inputs.
- `unresolved`: `{path, explanation, parameter_ids}`.
- `evidence`: keyed by canonical parameter ID, with `{documented_value, unit, status, source_ids, locator, source_kind, source_limits}`. Constraints and unresolved rows reference this shared evidence without duplicating it.

No nested conformance assumptions or limitations duplicate root data. Even imported observations are user-supplied model inputs; preserve their independent provenance outside strict JSON.

### Full

Each constraint/conflict includes its canonical documented value, unit, source status, source IDs, locator and source kind alongside the compact fields. Inputs include `path`, `value`, `origin: "user_supplied"`, classification, explanation and relevant constraint evidence. Unresolved entries retain their detailed source evidence; conformance also includes its complete `assumptions` and `limitations`. Full output adds detail, not additional checks or stronger authenticity.

### Classifications

| Classification | What it does and does not mean |
| --- | --- |
| `source_backed` | Only `max_branches` or `daily_license_limit` exactly matching the corresponding documented cap. This means **matches a publisher cap only**, not that the actual position or live contract configuration was verified. |
| `user_selected` | A supplied decision or assumption, including lower chosen caps, initial position, and remaining issuance budget even when equal to a documented bound; other economic fields fall here unless unresolved or inconsistent. |
| `unresolved` | The user supplied a value, but relevant source semantics, model application, or feasibility remain unresolved, including the fee, policy, funding, and entry-context cases above. It does not mean the user's value is missing or null. |
| `inconsistent` | A known checked-rule conflict; this classification takes precedence over all others. Documented mode blocks; explicit stress mode reports and permits the conflict within computational bounds. |

Show unresolved/proxy assumptions alongside cap matches rather than calling the whole input “source-backed.” In particular, checking a multiplier against a published range does not resolve its future policy behavior. Conformance is partial even when there are no known conflicts.

## Blocked and malformed requests

A documented conflict exits `3` (`ConformanceError`, `error.type: "documented_rule_conflict"`), with `warning`, selected `detail`, normalized `assumptions` and the selected-detail blocked `conformance` on stderr. There is no stdout and no numerical strategy result. Show conflicts and unresolved semantics without silently changing inputs or switching mode.

Malformed input exits `2` (`InputError`, `invalid_input`); malformed fixed references exit `4` (`PackageDataError`, `package_data_error`) in either mode. Errors carry warning and JSON on stderr, never fallback numbers. `simulate(config)` uses the same schema/detail and raises corresponding errors. Neither an error nor missing output is a zero-valued scenario.
