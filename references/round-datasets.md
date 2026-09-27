# Curated round datasets and projection evidence

Consult the **latest relevant curated dataset before deriving a policy opening or forecasting a close**. A policy-derived opening, a current inventory-conditional curve quote, an observed last sale and an authenticated current floor are four different quantities. The expected next market last-sold price is not automatically the next opening. This projection leaves the future floor unknown; do not carry today's floor forward as a fact.

The installed `assets/schemas/round-dataset-v1.json` defines the version `"1"` summary shape. It is strict about names, types and raw integer encoding, but preserves incomplete economic observations with explicit `null` fields. Shape validation does not authenticate sources, establish completeness, resolve conflicting evidence or admit a row to a projection. The broader [research evidence interchange](research-tools.md#optional-external-evidence-interchange) remains suitable for raw logs, headers, receipts, coverage gaps and conflicts that cannot yet support a curated round.

## Durable storage and finding the latest cohort

Live research belongs in an **explicitly selected, durable research store outside the installed runtime skill**. Record the chosen location and dataset identity in the host's research context so the next session can find it. There is no implicit home-directory cache, bundled live history, network discovery command or automatic persistence requirement for ordinary questions. Do not write live observations into installed `assets/`, `references/` or scripts.

For source review, `research/datasets/` relative to the source skill root is a suitable explicit location: for this repository, `skills/srstack/research/datasets/`. The existing package boundary excludes `research/`, so this source-only store is **not** installed or exported as runtime content. An authorized external research directory is equally suitable and survives replacing an installed skill. Keep public source identities, referenced evidence and migration notes with the selected store; never persist credentials, provider keys, secret URL parameters, wallet material or token inventories. Contract addresses, generation identifiers and arbitrary price-unit metadata are evidence identities, not a maintained asset list.

Before using a saved dataset:

1. Identify the requested chain, auction family, contract/generation cohort and exact payment denomination/scale. Locate the saved dataset and supporting evidence using the chosen research context, rather than assuming an installed example is live.
2. Inspect its curation time **and** its pinned observation head, head timestamp/hash, coverage horizon, source revisions and generation discovery scope. Compare the head and known round/settings boundaries with the question's relevant observation anchor. File modification time, a recent copy or a newly written `curated_at` is not freshness evidence.
3. Account for newly opened or completed rounds, capacity or schedule changes, pricing/floor changes, redeployments, source/index lag and provisional/reorg-sensitive ranges since that horizon. Reconcile required new scope and overlap under existing host permissions. A later head does not heal an earlier coverage gap; an older complete dataset is not necessarily current.
4. Separate comparable generations and units, retain incomplete/no-sale rounds, and state excluded rows and the exact trailing sample. Do not quietly skip a newer uncertain round to make an old cohort look like the latest closed sample.
5. Only then derive a policy opening from an evidenced qualified close and an **explicit, scoped policy multiplier**, and present any close projection as conditional. If current relevant data is absent, stale or insufficient, provide the formula, known evidence and missing prerequisite; do not invent a numeric close forecast or silently substitute the fictional fixture.

The offline helpers make no network requests, inspect no wall clock and discover no datasets. Freshness, source authentication and cross-generation comparability are caller/curator responsibilities, not effects of passing a Python function a JSON object. Dataset retention does not grant additional transport, signing or submission authority; see [safety](safety.md).

## Schema, identity and units

The schema applies to a **dataset object**, not an arbitrary wrapper. Its required top-level fields are:

- `schema_version: "1"`, canonical integer-string `chain_id`, `auction_family: "license" | "charter"`, and `synthetic` boolean. Real chain identity must be authenticated and positive; no chain or address is built into the schema.
- `price_unit: {"label": <nonempty identity>, "decimals": <integer string>}`. The label is arbitrary and must identify an authenticated denomination, not a ticker casually treated as USD. Every raw price in this dataset uses the same exact scale `10**decimals`.
- `curated_at`: ISO 8601 UTC with `Z`; and `rounds`: an array of the records below. Optional `sources` identify public original sources or durable evidence artifacts; optional `notes` retain qualifications. These are evidence metadata, not asset inventories.

All raw prices, sold/capacity quantities, day IDs, block heights, timestamps and decimal counts are **canonical nonnegative integer strings**: `"0"` or digits with no leading zero. They are not JSON numbers, signed strings, exponential notation, formatted currency or binary floats. UTC `curated_at`/`reconstructed_at` are human-readable curation times; Unix `ts` and `head_timestamp` are integer seconds on the chain clock. Decimal display is a presentation step; retain raw integers for calculations. Enable JSON Schema `date-time` format checking in validators: some implementations treat `format` as annotation only.

Each round requires these slots:

| Field | Meaning and partial-data treatment |
| --- | --- |
| `generation`, `contract`, `day` | Composite identity is **chain + family + generation + contract + day**. Contract is a 20-byte hex address; normalize address case when checking duplicates. Day IDs may reset and are not calendar dates. |
| `scheduled_window.start_unix`, `.end_unix` | Effective scheduled interval, normally `[start,end)`, in Unix seconds; each may be `null` when unavailable. Derive from the authenticated effective anchor/period, not a guessed duration. |
| `start_price_raw` | Historical policy opening; `null` when unknown. Not a market-close prediction. |
| `last_sale_price_raw` | Last observed executed unit price; `null` for unavailable price/no observed sale, distinguished in notes/evidence. A last print is not automatically a closing sale. |
| `floor_price_raw` | Authenticated historical floor; `null` if missing. A minimum observed trade is not necessarily the floor. |
| `sold`, `round_cap` | Purchased quantity and effective round capacity in the same selling units. Nullable; partial quantity remains a partial subtotal. Sold is not a count of purchase logs. |
| `sellout` | `true`, `false` or `null` for evidenced exhaustion, evidenced non-sellout or unknown. Zero allocation alone is not demand-driven sellout. |
| `first_sale`, `last_sale` | Each is `null` or `{ "block": <integer string>, "ts": <integer string>, "block_hash": <optional 32-byte hash> }`. Null distinguishes unavailable anchor/no observed sale in notes. Preserve an incomplete anchor in supporting evidence rather than filling its missing part. |
| `provenance` | Reconstruction method, observation horizon, coverage and timestamp basis, described below. Optional record `notes` preserve exceptions. |

`null` never means zero. An empty purchase response does not prove a no-sale round without adequate discovery and coverage. A no-sale or partial row remains useful historical context even though it cannot supply a close/open ratio. Keep conflicting observations and their provenance in supporting evidence; mark the summary partial/unknown until reconciled. Do not discard rows just to make a clean sold-out series.

`provenance` requires `method: "events" | "archive-reads" | "mixed"`, `head_block`, `head_timestamp`, `reconstructed_at`, `coverage: "complete" | "partial" | "unknown"` and `timestamp_basis: "block_headers" | "unknown"`. Optional `head_block_hash`, `source_refs`, `evidence_refs`, nonempty `sellout_basis` and `notes` support the claims. Pin the head hash here or in referenced evidence. Source records have required `id` and `identity`; optional kind, retrieval/observation UTC times (or null), digest and notes. Resolve references against the retained evidence; a present reference or a nonempty basis string alone proves nothing.

There are no free-form extension objects in this round schema: misspelled fields and unrecognized payloads fail shape validation. Retain richer or incompatible source material in the separate evidence store, not by silently dropping it. Required provenance fields must not be invented to make a source fit; evidence lacking a usable observation head belongs in precursor research evidence until that head can be established.

## Reconstructing rounds: events first, archive state when needed

Prefer authenticated purchase events for executed quantity, executed unit price, execution order and first/last sale identity. Preserve raw log identity and decode with the actual generation's ABI and price/quantity semantics. Deduplicate a derived canonical ledger only after reconciling chain, emitter, block/transaction hashes, transaction index and block-global log index; retain removed logs, conflicts and reorg alternatives separately. Supporting events or cumulative counters are cross-checks, not another set of purchases to add. A receipt-matched execution does not prove that discovery found every execution.

Use historical/archive reads at the **round-end evidence anchor**, or the evidenced exhaustion anchor plus the required subsequent coverage, to recover state that events do not establish: effective opening, floor, capacity, remaining inventory, schedule/settings and any reopening. Do not read today's mutable values and assign them to every historical day. A historical getter that reports only the current round cannot necessarily reconstruct a past round even when called at a recent block. When a purchase event omits unit price, use an authenticated generation-specific reconstruction or a corroborating execution trace/state path; a curve value sampled at a block timestamp is not automatically that transaction's executed price. If price remains unavailable, preserve `null`.

Identify the exact archive block and hash and document why that block represents the relevant boundary. At a rollover boundary, the first block after the timestamp may already expose the next round's state; a block-level poststate may also include later transactions in the same block. Cross-check event order and the contract's transition semantics rather than assuming any nearby height is an end-of-round snapshot. Retain archive limitations or pruned/unavailable state as gaps, not zeros. Use `mixed` when event and archive evidence both contribute.

**Fetch actual node block headers** for first and last purchases and the observation head. `first_sale.ts`/`last_sale.ts` must come from their containing headers for real timed claims. Never derive elapsed time from `(last_block − first_block) × average_block_time`, an index's retrieval time, browser time or the curation timestamp. Reuse header evidence by chain/hash, and reconcile canonicality when reorgs, removed logs, competing hashes or provisional boundaries require it. If the timestamp source is not established, use `timestamp_basis: "unknown"` and keep the record out of timed projection admission.

Distinguish first-to-last **observed selling span**, scheduled-opening-to-last-observed-sale, and evidenced sellout duration. They answer different questions. A receipt-verified last print becomes a qualified exhausted close only with complete ordered purchase coverage through the relevant endpoint and authenticated exhaustion, including capacity changes/reopenings. Complete event scan coverage, receipt checks, header canonicality, economic semantics and exhaustion evidence are separate claims.

A scheduled window uses the effective anchor/period. Its next boundary is a candidate schedule, not promised inventory or a guaranteed fill. The scoped 2026-09-27 observations of continued curve decay after zero inventory and an unchanged current day until the scheduled boundary do not certify every generation's implementation. Preserve the `remainingToday == 0` tripwire: a residual mathematical curve price then is phantom/not buyable, not another sale or forecast input. Positive inventory alone does not establish every purchase constraint. See [auction guidance](auctions.md).

## Chronology, compatibility and projection admission

Curate chronological order using authenticated scheduled starts and actual sale anchors, not file arrival order, lexical day strings or raw day IDs across generation resets. Check scheduled bounds, first/last ordering, head bounds, duplicate composite identities, overlaps and gaps. Resolve ambiguous ties and conflicts before calling a sequence comparable. Do not count overlapping exports twice. A dataset can span generations only after documenting compatible denomination, quantity, economic-price meaning, lifecycle and policy scope; the presence of a shared schema or the same label does not establish compatibility. Split incompatible cohorts. If an exact unit conversion is justified, retain the original amounts, conversion evidence and exact scale; never invent missing decimals or silently relabel one asset as another.

The [calculation helpers](calculations.md) distinguish schema storage from stricter projection selection. A qualified sellout record needs `sellout is true`, `coverage == "complete"`, `timestamp_basis == "block_headers"`, a nonempty `sellout_basis`, known ordered first/last block-and-timestamp anchors, known last-sale price, positive opening and `sold == round_cap > 0`. These are admission checks over supplied assertions, **not independent verification**. The helper does not resolve source/evidence references or authenticate a basis string; the curator must do that work.

Sale anchors must not exceed the supplied observation-head block or timestamp. Qualified sellouts require both head fields; contradictory future observations are excluded rather than fitted as known closes.

Helpers use scheduled start when available, otherwise first-sale time, otherwise last-sale time for chronological selection, and reject duplicate `(generation, normalized contract, day)` identities within the supplied chain/family. Historical leaf summaries can exclude unqualified rows with reasons. The composed next-close procedure rejects an unorderable record or an unqualified latest supplied round instead of silently projecting past a newer unknown observation. Merely giving it rows in array order or passing an old but internally consistent sample does not establish latest-cohort freshness.

Choose `trailing`, precision and the policy multiplier explicitly. At least two admitted observations are needed for sample standard deviation or a close trend. State the selected identities/count and all excluded partial, unknown or no-sale observations; never hide a ratio, sample count or multiplier as a live default. An ordinal fit uses `x = 0..N−1` in the selected chronological sample; it is not a regression against elapsed time or resettable day IDs. Report generation transitions and gaps that make a per-selected-round trend economically inappropriate.

Show the last observed print separately from any qualified close. Present trend and structural projections together with exact ratio statistics and assumptions; a mean ± one sample standard deviation band is descriptive dispersion, not a confidence interval or contractual price range. Retain a negative trend result as an implausible scenario outcome rather than clipping it into an apparently credible price. Missing historical floors stay missing and `future_floor_raw` stays null. A policy opening is explicitly **not the expected transaction price**, and a next-close forecast remains conditional on the selected sellout behavior continuing.

## Coverage, sample verification and migration

For a real-source import or refresh, retain the original artifact unchanged in the selected research store, its public origin/retrieval context and a digest or equivalent stable identity. Record which original rows map to each composite round identity, all transformations, omissions and unresolved conflicts. Review scope and numerical fields before describing a migrated dataset as authoritative.

- Map only evidenced fields. Convert known display prices to raw integers with exact decimal/rational arithmetic and an authenticated scale; reject or retain separately a value that cannot be represented exactly. Do not round a feedback decimal into a purported historic execution.
- Preserve every source round, including no-sale, partial and unknown entries, without manufacturing prices, timestamps, capacity or sellout. Keep legacy raw material in supporting evidence when required provenance is unavailable. Reconcile generation resets, unit changes, overlaps and duplicate identities before ordering the cohort.
- Verify a disclosed sample against actual node-backed evidence: include first/last cohort endpoints, generation transitions, capacity or pricing changes, and ambiguous/outlier rows rather than only convenient successes. Check event ordering and executed price/quantity, actual first/last header timestamps, historical opening/floor/capacity and exhaustion at the relevant archive anchor. Record the selected identities, source anchors, results and unavailable/mismatched checks. Sample verification is not proof of the unexamined rounds or complete discovery.
- Preserve separate evidence for discovery scope, requested/scanned/failed/unsearched ranges, index caps/pagination, receipt matching, historical state and header canonicality. `coverage: "complete"` requires a justified claim-specific horizon and accounting for gaps/settings changes; counts and a final page alone are insufficient.
- Validate the resulting shape and review cross-field invariants/chronology/units separately. Recheck affected observations on reorg evidence, inconsistent overlap, source corrections, a generation/settings change or a freshness extension crossing a provisional boundary. Incremental reuse is allowed; neither blind append nor automatic full rescan is a correctness rule.

The user-mentioned **19-round `license-auction-history.json`** is not reconstructed from remembered averages, reported decimals or the six-round example. If its source is unavailable, the missing prerequisite is the original artifact (or an equivalent authenticated source export) **plus node-backed sample evidence sufficient to verify its round identities, prices, coverage and timestamps**. State what is unavailable; do not substitute a differently scoped partial dataset and call it the 19-round seed. Missing source evidence does not prevent using the schema or explaining a conditional model, but does prevent claiming that live seed has been migrated and verified.

## Installed synthetic scenario

`assets/examples/projection-evidence-v1.json` is an explicitly fictional wrapper with `schema_version`, `synthetic`, `description`, `dataset`, `projection_request` and `phantom_request`. Validate **its `dataset` member** against `assets/schemas/round-dataset-v1.json`; the wrapper is not itself a round dataset. It is separate from `assets/examples/research-evidence-v1.json`, which demonstrates the broader raw-evidence interchange. Neither example is a live forecast default.

The six-round scenario uses chain `999999`, contract `0x1111111111111111111111111111111111111111`, generation `fictional-v1`, license family, and arbitrary `FICTIONAL_PAYMENT` with two decimals. Every identity, hash, timestamp and economic observation is invented. `complete` coverage, header-shaped anchors and sellout are **stipulated fictional inputs**, not actual node/receipt verification. This exception is always visible through `synthetic: true` and source notes; never mark fabricated real observations as header-backed evidence.

| Day | Opening, display units | Last sold, display units | Floor, display units |
| --- | ---: | ---: | ---: |
| 0 | 17598 | 8400 | 5334 |
| 1 | 16800 | 8001 | 5068 |
| 2 | 16002 | 7602 | 4802 |
| 3 | 15204 | 7203 | 4536 |
| 4 | 14406 | 6804 | 4270 |
| 5 | 13608 | 6405 | 4004 |

The file stores each table price as an integer string multiplied by 100. The fictional preceding close is 8799 display units; each opening is exactly twice the preceding close. Each floor is `(4 × close − opening) / 3`. Each round stipulates 40 sold from a positive cap of 40 without reopening. Day `i` has scheduled start `1000 + 1000i`, end `2000 + 1000i`, first sale at start + 100/block `100 + 10i`, and last sale at start + 800/block `109 + 10i`. Head block 200 has timestamp 6900; curation time is the matching synthetic `1970-01-01T01:55:00Z`.

The projection request uses six rounds, explicit multiplier `"2"` and precision 32. The phantom request uses the last opening/floor, half-life 400 seconds, elapsed 900 seconds and remaining inventory `"0"`. Under this deliberately assumed curve, the last sale at elapsed 800 seconds is an exact quarter-gap above the floor; the later residual curve has no buyable price. This illustrates a scheduled window still in progress after fictional exhaustion, not an early round rollover or a universal deployed pricing law.

The request inputs are separated from expected answers: use the installed pure helpers described in [calculations](calculations.md) for the offline scenario. No model-prompt answer key, live numerical default, asset inventory, router target or network client is included.
