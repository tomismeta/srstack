# Plan: workflow and index

Every planning answer starts with this exact paragraph, including missing inputs, blocked runs and unavailable execution:

Hypothetical scenario—not contract-verified. Based on our interpretation of the whitepaper and official announcements, plus your assumptions. Not a forecast or executable quote.

1. Require schema `1`, explicit `documented`/`stress` mode, acknowledgment and all economic inputs. No economic defaults; mode differs from `exit_mode`. Never fill gaps from examples, calculator defaults, quotes or differently scoped publisher values.
2. Complete JSON: read [safety](safety.md) and [execution](planning-execution.md), verify trusted installed manifest/script/fixed-resource hashes using host utilities, then execute. Do **not** load schema, model, catalogs or script body unless needed; engine output supplies canonical checks/evidence. Hashes identify bytes, not protocol validity.
3. Existing permitted Python 3.10+: fixed `python3 -B -I scripts/scenario.py` at the verified root, JSON separately on stdin. Safety defines transport alternatives/containment. Missing runtime, verification or safe transport means a stated gap—not installed tools, broader access or invented results.
4. Report actual execution, mode, inputs/provenance, conformance conflicts/unresolved semantics and relevant keep/selective/aggressive comparisons. Documented conflicts block numbers; only explicit stress permits disclosed departures. Both require valid packaged rules. Separate hypothetical cash from unvalued retained positions; no forecasts, recommendations, contract verification or executable quotes.

| Need | Load only then |
|---|---|
| Construct/repair input, bounds, sensitivity | [planning-inputs](planning-inputs.md) |
| Mechanics, exits, summary/full fields | [planning-model](planning-model.md) |
| Rules, classifications, report evidence | [planning-conformance](planning-conformance.md) |
| Explicit tutorial/example only | [fictional JSON](../assets/examples/planning.json); never defaults |

`detail`: `summary` default or `full`. `include_history`: false default; true requires full. Neither changes economics. Preserve imported observations' sources, units, block/quote and retrieval times outside input; future flat prices/constants require explicit assumptions. No automatic inspection, source refresh or persistence.

CLI: `0` JSON stdout; `2` invalid input; `3` documented conflict with selected-detail blocked conformance/assumptions, no strategy numbers; `4` invalid fixed references in either mode. Errors: warning/JSON stderr, no stdout/fallback. Missing output is not zero. `simulate(config)` follows schema/detail and raises corresponding errors.
