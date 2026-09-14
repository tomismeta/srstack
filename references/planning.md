# Plan: guided workflow and execution index

Every planning answer starts with this exact short line, including intake, assumption approval, blocked runs and unavailable execution:

Hypothetical—not contract-verified or a forecast.

## Conversation first; JSON is internal

Help the user build a scenario in ordinary language. Do not open with a JSON template, schema field list or a demand for schema-1 input. Read [input definitions](planning-inputs.md) when translating or repairing assumptions; the agent owns that translation. Show raw JSON only when requested. Use plain-language questions in the response, not a blocking interactive tool in one-shot hosts.

Reuse information already supplied. Ask only the next missing decisions, grouped into at most three short questions per turn. Do not ask for wallet access, private identifiers or a complete financial history. A hypothetical position needs no public address.

### 1. Establish the comparison

For an underspecified request, start with:

- **Goal and position:** what does the user want to compare, and are they exploring a new position, an existing position or a fictional illustration? Collect starting branches/credits when relevant; do not infer balances.
- **Spending:** what additional ETH budget may expansion use? Keep this separate from initial position cost, entry gas and terminal exit costs.
- **Time and endpoint:** how long should the comparison run, and should it end in full exit, partial exit or continued holding?

Adapt these questions to the supplied context rather than repeating the checklist. Suggest documented mode for ordinary comparisons; explain that stress is an explicit choice to explore departures. Offer a 30-day/full-exit illustration only as a proposed scenario, never as a recommendation or an accepted default. No calculation is required during intake.

### 2. Fill gaps without inventing economics

After the essentials, collect the remaining assumptions in small groups. Explain unfamiliar concepts before asking for values. Distinguish user inputs, dated sourced observations, proposed hypotheses and unresolved gaps. A current observation is not a future constant or an executable quote.

| Kind | Treatment |
|---|---|
| Schema version, case IDs/names, summary detail, history off | Set internally; these do not change economics. IDs and labels must remain valid plain data. |
| Mode, horizon, exit choice, selective target/cadence | Propose a suitable comparison setup, but obtain approval before execution. No silent documented-to-stress switch. |
| Flat price, unchanged external branches, constant issuance multiplier | May propose as clearly labelled illustrative hypotheses, not neutral forecasts or low-risk economic facts. Approval is required. |
| Holdings, initial cost, network size, issuance/budget, token/license price, protocol fees, acquisition markup, sale slippage/tax | Ask for values or explain the evidence gap. Do not guess, substitute zero or borrow fixture values. Fresh public research is a separate user-authorized step, not an automatic lookup. |
| Gas | Ask for an ETH estimate for entry, each successful expansion purchase and terminal exit. No universal gas constant. An estimate needs a stated basis; network gas price alone is insufficient without chain and transaction-cost information. |

If a user cannot estimate gas, offer **explicit gas exclusion for a preliminary comparison**, or ask them to approve specific hypothetical values/ranges. Only after approval may exclusion be encoded as zero for the agreed gas fields; label the result **before the excluded gas costs**, never all-in. Entry, per-purchase and terminal gas are different charges. Do not exclude protocol fees, slippage or other costs merely because gas was excluded.

When exporting JSON on request, include any exclusion notes alongside it, not as unsupported schema keys. Zero-valued inputs alone do not distinguish excluded costs from assumed free execution.

If a user supplies an acceptable gas range, a sensitivity comparison can show whether strategy rankings change. Gas fields are root assumptions: use separate approved invocations, not scenario-level overrides. Do not manufacture a plausible range or calculate gas from unauthenticated contracts.

When material information remains unknown, offer a qualitative explanation, a user-approved hypothetical assumption, or an explicitly requested fictional tutorial. An ordinary planning request is not permission to load the example. A tutorial request may use the complete [fictional fixture](../assets/examples/planning.json), identified as unrelated to the user's holdings and market expectations; do not mix its values into a personal scenario.

### 3. Present an assumption sheet and obtain approval

Before a newly assembled run, show a compact plain-language table: **item · value/unit · basis or status**. Group related quantities, but keep every economically meaningful input visible. Translate the schema rather than showing its keys. Include:

- Mode, horizon, starting branches/credits and initial position cost.
- Expansion budget, funding source, branch cap, daily purchase limit, selective target and interval.
- External branch count, base daily issuance and remaining gross issuance budget.
- Initial ETH/token price, license token cost and token-buy markup.
- Entry/per-purchase/terminal gas, exit choice, resolution fee, sale tax, sale fee and slippage.
- Each case's issuance multiplier and daily price/external-branch growth assumptions.

Mark **provided**, **sourced observation**, **proposed** or **missing**; retain source dates, units and relevant block/quote anchors outside engine input. Group shared assumptions once. Highlight exclusions and unresolved mechanics. Don't pretend a partially completed table is runnable.

Ask: **“Approve these hypothetical assumptions, or tell me what to change.”** If values are still missing, ask for those instead of inviting blanket approval. “Use sensible defaults” or “looks good” does not supply an omitted value. Approval applies only to the shown complete values and mode; it acknowledges the hypothetical scenario, not contract feasibility. Economic edits require approval of the changes before rerunning. Do not repeat intake or demand another confirmation when the user has already explicitly approved a complete hypothetical configuration.

### 4. Translate, execute and explain

Build schema-1 JSON internally from the approved assumptions, with explicit mode and `assumptions_acknowledged: true`. Read the input definitions to check mappings, units and bounds. No economic defaults; mode differs from `exit_mode`. Never fill gaps from examples, calculator defaults, quotes or differently scoped publisher values.

Read [safety](safety.md) and [execution](planning-execution.md). Verify the trusted installed manifest/script/three fixed parameter-file hashes, then use permitted Python 3.10+, the fixed planner and separate JSON stdin. Missing runtime, verification or safe transport means a stated gap—not installed tools, broader access or invented results. The only intended calculator is `scripts/scenario.py`; do not substitute agent arithmetic or generated model code.

Lead with the comparison relevant to the user's goal, then a small keep/selective/aggressive table and the important assumptions/evidence gaps. Report actual execution, mode, conflicts and unresolved semantics. Documented conflicts block numerical results; explain the conflict and offer an input correction or explicitly approved stress rerun, never silently change either. Both modes require valid packaged rules. Separate hypothetical cash from unvalued retained positions; no forecasts, investment recommendations, contract verification or executable quotes. Retain any approved cost-exclusion labels in every affected comparison, including sensitivity runs.

Offer a focused next adjustment rather than another schema dump. No automatic inspection, refresh, persistence or monitoring.

## Complete-input fast path

An already complete, explicitly acknowledged JSON request can go directly through safety/integrity verification and execution. Do not force it through a questionnaire or load schema/model/catalogs/script bodies unnecessarily. Complete approved natural-language inputs need translation, not repeated approval. Hashes identify bytes, not source authenticity or model validity.

| Need | Load only then |
|---|---|
| Construct/repair input, bounds, sensitivity | [planning-inputs](planning-inputs.md) |
| Mechanics, exits, summary/full fields | [planning-model](planning-model.md) |
| Rules, classifications, report evidence | [planning-conformance](planning-conformance.md) |
| Explicit tutorial/example only | [fictional JSON](../assets/examples/planning.json); never defaults |

`detail`: `summary` default or `full`. `include_history`: false default; true requires full. Neither changes economics.

CLI: `0` JSON stdout; `2` invalid input; `3` documented conflict with selected-detail blocked conformance/assumptions, no strategy numbers; `4` invalid fixed references in either mode. Errors: warning/JSON stderr, no stdout/fallback. Missing output is not zero. `simulate(config)` follows schema/detail and raises corresponding errors.
