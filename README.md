# srstack

**Question-driven Standard Reserve research and analysis for AI agents.**

Ask about protocol mechanics, live positions, historical auctions or what earned accrual could buy. The agent chooses the evidence and calculations the question needs, using its existing host-authorized tools. No topic command, calculator wizard or fixed sequence is required.

Independent [Agent Skill](https://agentskills.io/specification), not an official Standard Reserve product. **0.3.0 remains unreleased.**

## What you can ask

- “How are my charter's branches doing?”
- “Do I need to check in?”
- “Show every auction round across contracts, with opening, first, average and last sale prices.”
- “Based only on earned accrual, what could I afford in the next auctions?”
- “What changes if I buy more branches, and when would they affect accrual?”
- “What does the Second Mandate say, and what is actually deployed?”

Current quantities require fresh evidence. Packaged knowledge can answer explanations offline. Unknown positions, inaccessible evidence and hypothetical inputs remain distinct; missing information is not zero.

## Minimal architecture

The installed skill contains a [question-to-capability guide](references/capabilities.md), [dated contract inventory](references/contracts.md), [complete inventories of explicitly reviewed interfaces](references/interface-inventory.md), selected [decoding guidance](references/interface-guide.md), topic/source/policy references, optional offline calculation code and schema, a [synthetic worked example](references/research-example.md), a license and an integrity manifest. **No RPC transport, active deployment router, bytecode allowlist, embedded live rates, wallet connector or background service.** This deliberately expands the earlier catalog exclusion into reviewed planning knowledge, not an execution client. Dated identities are leads; ABI layout, economic meaning and deployed correspondence remain separate claims.

The [object and contract map](references/object-map.md) defines economic objects separately from contracts and makes ownership, recorded state, funding, routing and control relationships explicit. [Role discovery](references/contracts.md#discover-a-role-without-prior-session-context) connects a natural question to dated identity evidence and fresh publisher/onchain corroboration without requiring old chats or backups.

- **Capabilities before needless reconstruction:** prefer the planning guide and relevant reviewed interface to repeating discovery or indexing. Direct getters, archive-state corroboration and event history answer different questions. The inventory is neither an allowlist nor a mandatory workflow; scoped negative and unknown entries do not prohibit independent research.
- **History from execution evidence:** discover relevant generations and deployment/round bounds, estimate the retrieval work against actual provider limits, then use an appropriate authorized index/log path. Do not default to genesis or a runaway tiny-chunk/429 retry loop. Event discovery, pagination, receipt matching and canonical verification are separate results.
- **Accrual and conditional pace:** certify a contract-derived rate only with its applicable quantity, scale and epoch/pause/expiry mechanics. Separately, exact changes between pinned pending observations can support a labelled empirical ledger pace and explicit bounded scenarios. Neither a getter name nor a quiet interval proves earned origin or spendability.
- **Earned-only scenarios:** verified unspent earned accrual plus projected new accrual, minus commitments and simulated purchases. Exclude deposits, wallet funds and unattributed balances. Future prices and persistent rates remain explicit assumptions; gas and conversion funding are separate.
- **Availability before affordability:** effective zero inventory means not buyable now; a residual price getter is not an ask. A next scheduled window is a candidate opportunity. Keep opening-policy assumptions, executed-history comparators and conditional unsold-curve crossings separate.
- **Token/RPC economy:** load relevant sections, reuse authenticated observations with their coverage/canonicality limits, batch independent calls and deduplicate receipt/header reads. Recheck on material conflicts, reorg evidence or provisional-boundary changes rather than blindly appending or universally refetching. A thin skill does not itself guarantee fewer RPCs; host capability and evidence selection matter.
- **Claim-level results:** exact sale consideration, independently evidenced refunds, gas, origin attribution, discovery coverage and implementation-based forecasts have separate statuses. A successful receipt or correct pending disclaimer does not make the whole financial answer pass.

The agent may use inspectable local calculation code when needed under host permissions. That is not a bundled protocol client or permission to execute downloaded code. No Python dependency is required to load the skill; live access and exact arithmetic depend on actual host capabilities.

The installed [optional offline research aids](references/research-tools.md) provide `scripts/calculations.py`, the thin `scripts/research.py` CLI and `assets/schemas/research-evidence-v1.json`. Python 3.10+ and its standard library are needed only when choosing these helpers. Regression machinery stays source-only; the explicitly fictional installed [example](references/research-example.md) is instructional data reused by tests, not a live dataset. Agents may use, adapt or ignore these aids, choose another language/store, or write an independent solution. No helper, schema or checkout is required for an answer. Installation does not run code or grant execution permission; no transport, default deployment or automatic code download is added.

For next-round price questions, the [projection guidance](references/auctions.md) starts from the latest relevant [curated round history](references/round-datasets.md), not the policy opening. Six [offline recipes](references/calculations.md), a round-dataset schema and a separate fictional projection example distinguish empirical close forecasts, policy openings, inventory-conditional quotes, last sold and floors. Live research stays outside the installed runtime.

Live support is capability-based, not a blanket host-brand promise: the host needs authorized public reads, applicable ABI/Keccak encoding/decoding and exact calculation; historical questions additionally need adequate event/index/receipt coverage. Below that baseline, dated explanations and conditional reasoning remain useful, but blocked live checks cannot be counted as successful live acceptance. No particular language, client or RPC provider is required.

## Install a reviewed release

The development branch is `feature/v0.3.0`; do not assume a `v0.3.0` release tag exists. Follow [reviewed installation](references/installation.md#reviewed-installation): resolve a full commit before review, export only its runtime files and clean-replace the old skill root. Do not overlay an older installation and leave retired scripts behind.

Maintenance verification runs from the reviewed repository outside the installed skill. Keep the source pin and recovery record outside the hashed runtime. Host loading and session refresh are host-dependent; no forced restart or automatic update is included.

### Quick test after installation

Check the actual loaded path and reviewed revision, then ask a real question. A bare invocation should invite a question, not run network calls or return a mandatory menu.

Suggested acceptance questions:
- Explain a packaged policy without live access.
- Inspect a public position using dynamically authenticated evidence; do not use a cached rate as current.
- Ask for all historical auction generations; disclose omitted contracts, ranges or verification stages rather than substitute a current-only table.
- Model earned-accrual buying with attributed funds and established mechanics; separately exercise empirical pending pace and explicitly assumed all-ledger/dilution scenarios. Unknown earned origin must neither become earned funding nor suppress useful conditional calculations. Respect reservations, inventory and epoch boundaries.
- Repeat a calculation from the same evidence, then change one assumption. Check identical numerical outcomes for identical inputs and appropriate sensitivity without refetching unchanged data.

Record what the host actually read, calculated and answered. A package integrity check or synthetic calculation is not proof of live-provider access or host isolation. Repository-only acceptance cases (`maintenance/agent-acceptance.json`) are available in the source checkout, not the installed runtime.

For dogfooding, judge correctness, coverage, observed RPC cost and repeatability—not tool choice or a prescribed sequence. Count RPC methods separately from batch requests and index pages when the host exposes them; unknown counts stay unknown. Keep review records outside the skill. Missing live access is a blocked live check, not a failed installation.

### Mandatory release acceptance

A release candidate must be exercised in a fresh session using only its exported runtime—not a previous install, retired catalog/helper or stale workshop prompt. Record installation/loading, authorized host capability, provider/evidence coverage, reasoning/decoding and final answer separately as pass, fail, blocked or not run.

Required capabilities: direct pinned state; exact purchase-event/receipt verification; auction inventory/order/allowance interpretation; source-grounded accrual and an attributable real earned-only scenario; fixed-window/epoch boundaries; cross-generation history; evidence reuse; and correct failure classification. Include adverse cases for mixed-origin funds, precision, dynamic arrays and internally invoked purchases missed by direct-transaction discovery. A correct unknown passes uncertainty handling, not the unavailable numerical or completeness gate. The source-checkout acceptance file defines the detailed cases; these are publication checks, not an intake wizard for ordinary users.

**Deterministic results, flexible agents:** nontrivial arithmetic should use inspectable exact calculations with relevant reconciliation checks. Agents remain free to choose or write tools, investigate beyond the references and answer conditional questions without an execution facility. No required language, script, question menu, fixed call budget or permanent output artifact. Identical evidence and assumptions should reproduce identical numbers, not identical wording or tool calls.

## Safety and evidence

[Safety](references/safety.md) governs every host tool and delegated action. No signing, signature requests or transaction submission. Ready-to-sign calldata, deep links and filled unsigned objects require an explicit preparation request; a question about buying does not authorize preparation or execution.

Use host-managed credentials without exposing them to prompts, installed files or output. An underlying user/host authorization denial stops that action. Provider access refusal, transport failure, method/range capability and incomplete evidence require distinct handling: no evasion or silent source substitution, but independently authorized research is not globally forbidden by one failed endpoint. Save authorized evidence outside the skill, without credentials.

Dates describe reference provenance, not live freshness. Published policy, authenticated interfaces, source/implementation correspondence, observed state and modeled outcomes are different evidence levels. Forecasts are permitted with explicit assumptions; unsupported factual claims are not.

## Maintenance

From a reviewed source checkout with Python 3.10+:

```sh
python3 -B maintenance/package.py verify
python3 -B maintenance/check-package.py
python3 -B maintenance/check-inventory.py
python3 -B research/check-research.py
```

After deliberate content changes, regenerate the manifest with `python3 -B maintenance/package.py build`. The maintenance tool also exports reviewed commits and creates deterministic archives. These tools are not installed with the skill. Update source provenance and affected references together; ordinary research never rewrites the package.

Every future contract, generation or interface addition follows the [inventory methodology](references/inventory-methodology.md): shared immutable review provenance, complete enumeration of the stated source scope, exact indexed layouts, qualified explanations/units, dated role bindings, and corresponding positive/negative/unknown capability entries. Packaging invokes the source-only inventory consistency validator; CI also exercises its semantic regressions. These checks maintain the package, not a runtime permission gate.

CI installs `jsonschema==4.25.1` only to validate the instructional examples against Draft 2020-12. Local research regressions explicitly skip those optional checks if it is unavailable; use a separate maintenance environment to include them. Loading, using and exporting the skill remain standard-library-only and never install dependencies automatically.

This host-native cutover removes the previous fixed snapshot, price, history and diagnostic clients and their execution catalogs. There are no compatibility commands or retired helper aliases. Existing host-native research tools replace them; any automatic discovery, checkpointing or batching must actually be supported or implemented by the host agent before being claimed.

The installed optional calculation toolkit does not restore the retired protocol clients. Specialized references own exact accounting, round dating, allowance windows, order-ID caveats and history coverage. Stale host workshop/install prompts need explicit host-maintainer cleanup outside this repository; package installation does not rewrite other skills, credentials or global instructions.

### History-first projection correction (0.3.0, unreleased)

Next-close forecasts now report both a trailing last-sold linear trend and a structural estimate from the policy opening times recent sellout close/open ratios, with a descriptive ±1 sample-standard-deviation band. Policy is the mechanism, not a market-close prediction. Continued sellout and comparable cohorts are explicit assumptions; the future floor remains unknown. Four price shapes and the scheduled round lifecycle remain distinct, including the `remainingToday == 0` phantom-price tripwire.

Six standard-library helpers retain exact rational fits/statistics and bounded Decimal evaluation where roots or decay are generally irrational. A strict round-dataset schema preserves partial observations, actual header timestamps, coverage and provenance; curation guidance covers durable external storage, events/archive reconstruction, freshness and sample verification. Six new derived-analysis capability records bring the inventory to 25 without inventing forecast getters or new ABI reviews. The six-round installed fixture is fictional, not a live seed.

Review-clone checks passed all 20 package, 14 inventory and 29 existing research regressions plus 12 projection regressions, including both optional schema validations. All six documented recipes executed from a standalone 72-file runtime without changing its bytes. Packaging now distinguishes fenced code from Markdown links, so executable recipes do not create false missing-link errors. Three new source-only fresh-session gates cover next-close forecasting, sold-out current price and ambiguous price requests; passing these synthetic gates does not establish live history completeness.

The reported 19-round `license-auction-history.json` was not available for migration or node-backed sample verification. No seed was invented or replaced with a differently scoped history. **0.3.0 remains on hold**, with prior live-evidence blockers unchanged. This correction adds no runtime dependency, RPC client, endpoint, token inventory, router, wallet authority or transport-policy change.

### Release-readiness acceptance (unreleased, 2026-09-27)

The frozen `df4174500928e724b6aa67c1337e37d5dfae3a7a` runtime was exercised through fresh OMP 18.3.1 sessions using the observed `opencode-go/gpt-6-luna` model. All 20 scenarios and 88 required criteria were assessed: nine scenarios passed, three failed, and eight remained blocked. Runtime loading was observed with automatic discovery disabled and instruction-scoped isolation—not an OS sandbox or a claim about other host profiles. A separate real-host exercise clean-replaced the previous 39-file runtime, loaded the 68-file candidate, and restored the previous bytes exactly; no primary installation was changed.

The three failures were an unauthenticated cross-role getter probe and incomplete request-bound/checkpoint plans. The correction makes exact selected-interface authentication explicit before encoding, requires concrete question-scoped retry limits, and requires populated checkpoint values rather than a field checklist. Fresh runs of the same three natural questions against that uncommitted correction passed all 16 affected criteria; the original failures remain in external evidence. No router, fixed call budget, provider dependency, mandatory tool sequence or wallet authority was added.

**Release remains on hold.** Corresponding deployed accrual/lazy-roll/reset paths, attributable earned funding, required historical state and complete canonical history/flow coverage remain unestablished. Saved-public-evidence replays reproduced exact receipt accounting and 13 observed history rows, but assisted arithmetic is not unassisted discovery or complete live acceptance. Provider/client denials, unsupported tracing and throttling are recorded separately. Results, raw observations and transcripts remain outside the installed runtime; no live values become package defaults. The focused correction does not constitute a fresh complete acceptance pass for a later release pin.

### Reviewed capabilities and worked evidence (unreleased)

The current revision adds 19 dated contract bindings, 19 provenance-scoped capability records, and 15 interface inventories: 13 complete reviewed publisher definitions/adaptations and two explicit selective fragments. Their 905 ABI entries include 522 functions, 133 events, 234 errors, 12 constructors and four receive entries. Every entry retains exact layouts, indexed fields where applicable, generation/review context and qualified explanations/units. Registry and other incompletely exposed roles remain explicit gaps, not negative capability claims. Complete publisher-interface coverage is not complete deployed behavior.

The smaller entrypoint points into the capability guide before needless discovery/indexing, without requiring that workflow. Keyed charter/day and charter/window usage reads remain available; negative aggregate-history claims are narrower. Future additions follow the documented inventory methodology and source-only consistency checks. The collection guidance separates log identity from receipt verification, makes canonicality/reuse triggers concrete, explains schema-versus-summary admission, and prevents rounded-average reconstruction. A single installed synthetic ten-observation example demonstrates raw indexed logs, conflicts, reorg alternatives, removal, deferred identity and exact table/duration formatting. No transport client, new input mode or wallet authority was added.

Verification passed 14 inventory regressions, 20 packaging/export regressions and 29 research/example regressions, including the optional Draft 2020-12 check in a disposable maintenance environment. Independent PyCryptodome 3.23.0 verification matched all 889 function/error selectors and event topics and eight Keccak padding cases. All inventory source byte ranges/hashes and parsed ABI entries matched the retained complete publisher data. The package contains 68 runtime files; its installed example produced exact raw average `706/7`, remainder `6`, and `2m7s`, retaining conflicts, disputed, removed and deferred observations.

Direct CLI/library and capability/event lookups ran from a standalone runtime candidate in another working directory with checkout reads and network access denied by a Python audit hook. The documented decoder and table recipes also ran from that installed tree; installed bytes remained unchanged. This is scoped offline execution, source-layout and packaging evidence, not a production sandbox, fresh isolated host acceptance, live financial observation, source/bytecode correspondence or all-generation history PASS.

### Bundled research execution (unreleased)

The earlier bundled-execution revision installed the optional offline library, five-command JSON CLI (`weighted-price`, `rounds`, `pace`, `workload`, `curve`) and evidence-v1 schema, with exact JSON serialization and no source-checkout dependency. At that revision tests and fictional fixtures stayed outside the runtime; the current revision deliberately adds one labelled instructional example. No transport, protocol defaults, automatic execution, dependency installation or wallet capability was added.

Verification passed 23 calculation/CLI regressions and 20 packaging/export regressions, including execution after deleting the isolated source-checkout fixture and unchanged installed bytes afterward. All five documented CLI examples, file-input reconstruction and a direct library import ran from a standalone 39-file runtime candidate in another working directory, with checkout reads and network access denied by a Python audit hook. Exact rational values and unknown timestamps remained intact. This is offline execution and packaging evidence, not live-provider acceptance, a production sandbox or a claim that every release gate passed. The dated results below describe earlier revisions.

### Earlier interface-revision verification

Interface-revision verification: 19 packaging regression tests passed, and a clean isolated export passed exact runtime byte verification. Every published selector/topic was independently checked with Ethereum Keccak: 84 function signatures and 31 unique event signatures. Live canonical-block reads exercised scalar, flat-tuple and dynamic-array decoding, including separate charter and branch-license prices. The public provider served current pinned state and historical logs/receipts but later reported an older state unavailable; these are different capabilities.

A bounded license-history investigation reconciled emitter logs against successful receipts and canonical block headers, including an internally invoked purchase whose transaction destination was not the auction. Direct-to-auction transaction discovery would omit that purchase. Executed exact-arithmetic checks covered mixed-origin bounds, reservation replacement, precision beyond binary floating-point integers, price sensitivity, rounding-order counterexamples, fixed-window prior use/reset and epoch stopping. Synthetic mechanics are labelled scenarios, not proof of deployed Solidity behavior.

Two fresh tool-enabled dogfood sessions loaded only an isolated exported runtime and public evidence, without retired resources; isolation was instruction-scoped, not an OS sandbox. They exercised pinned public state, exact accounting replay, dynamic order-page decoding, charter consideration/refund/gas separation, and a bounded three-generation license-history query with 89 purchase events and 92 successful receipts including supporting creation/start/charter transactions. The history session needed an explicitly supplied, already-established permitted browser transport context after another client was denied; this is recorded host assistance, not unassisted transport discovery. A focused instruction replay additionally checked scoped-client access, broader host denial, prohibited spoofing and unavailable historical state.

### Feedback-revision verification (2026-09-27)

The updated package passed 19 packaging regression tests and exact-byte verification of a clean 35-file runtime export. The repository acceptance specification now has 20 scenarios; this is a definition of release gates, not a claim that all 20 passed.

Two new tool-enabled agents loaded only that exported runtime, without source-checkout context, prior sessions, retired helpers or backups. Isolation was instruction-scoped, not an OS sandbox. One freshly discovered publisher-declared roles, corroborated code and dependencies at a pinned block, discovered token identity dynamically, calculated exact pending-ledger pace from two actual headers, queried a bounded contamination interval and correctly stopped the live buying answer at zero effective inventory. Current Registry authorization, complete internal-flow coverage and earned origin were not proved. Its established permitted browser transport was supplied as host capability, not protocol addresses or expected answers.

The other exercised an explicitly fictional packet: sold-out/next-window reasoning, conditional opening and unsold-curve affordability, epoch clipping, bounded dilution, cross-generation quantity-weighted prices, exact receipt amounts with unproved refund/net cost, and stopping an infeasible tiny-range/429 scan. Independent exact calculations reconciled the numerical results. These are conditional/replay checks, not live history completeness, deployed formula verification or proof of a future fill. Observations and worked financial values remain outside the installed package.

Source reconciliation reread seven website page bodies and ten known social posts, recording fourteen full-body website/module fingerprints. It established no complete social-timeline interval. The current charter guide's 12-hour wording still conflicts with the whitepaper's daily/24-hour wording; S-Bill design copy and an inert sample UI do not authenticate a launch. Coverage and unresolved conflicts are recorded in the source records and [updates](references/updates.md), not summarized as universal synchronization.

Matching source/compiler correspondence and complete accrual/ledger-origin semantics remain unestablished. Bounded runtime-path research was retained outside the package and was not promoted into new certified onchain semantics. A real attributable earned-only 24-hour scenario remains blocked; empirical and explicitly assumed calculations have their own successful, narrower evidence. This unreleased development revision does not claim every mandatory release gate passed.

### Earlier source-only research-aids revision (2026-09-27)

This historical entry records the pre-bundling distribution and its verification; the current installed membership is described above.

Added source-only exact weighted accounting, observed round reconstruction, signed pending-delta pace, inclusive-range workload estimates and a separately named, fully parameterized gap-to-floor mathematical scenario. The optional version1 evidence schema retains raw observations, hash-keyed headers/timestamps, separate receipt checks and coverage gaps. Only the guidance and fictional worked explanation enter the installed skill; library, schema, tests and synthetic fixtures remain excluded. No transport, live dataset, protocol defaults or new wallet capability was added.

Verification passed 20 offline research regressions and 19 packaging/export regressions, including exclusion of the entire research directory from installs. The documented reconstruction example ran against the fictional fixture: exact weighted totals retained their remainder, missing timestamps stayed unknown and partial receipt coverage stayed partial. Competing transaction/log slots, active/removed variants and unresolved reorg alternatives were exercised without inflating uncontested totals. A temporary standards-based Draft2020-12 validator accepted the schema, fixture and partial/extended evidence; it is not a library or runtime dependency. An independent JavaScript BigInt calculation with a different input format reproduced the accounting result without the helper or schema.

Fresh official publication and bounded same-block core/auction code, dependency and getter checks are recorded by `sr-offline-research-evidence-2026-09-27` in [interface provenance](assets/sources/live-interface.json). Dynamic inputs remain external, not defaults. The complete publisher module measured860946UTF-8bytes versus860338JavaScript string units with the same prior SHA-256; mixed length measures were not source drift. Fingerprints identify reviewed evidence, not allowed future deployments or sources. No new matching compiler/source correspondence or full release acceptance is claimed.

Agent freedom is explicit in the entrypoint and research guidance: use, adapt or ignore these aids, choose another language, dependencies, evidence format or independent solution under existing host permissions. Missing tooling or schema nonconformance is not an answer gate. Arithmetic argument checks belong only to the selected function; they do not prescribe the research process. Existing wallet/signing/submission boundaries are unchanged.

## License

Original code, summaries and instructions are [MIT-licensed](LICENSE). Third-party documents, media, trademarks and protocol code retain their owners' rights and are excluded from that grant. Source links do not imply affiliation or transfer those rights.
