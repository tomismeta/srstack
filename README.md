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

The installed skill contains instructions, topic references, a bounded [dated interface guide](references/interface-guide.md), source/policy records, an optional offline calculation library/CLI and evidence schema, a license and an integrity manifest. **No RPC transport, active deployment router, broad ABI catalog, bytecode allowlist, embedded rates, wallet connector or background service.** The guide restores selected signatures/selectors, event layouts and evidenced units as generation-scoped discovery aids. Historical addresses are provenance, not current execution bindings; interface decoding is not implementation verification.

The [object and contract map](references/object-map.md) defines economic objects separately from contracts and makes ownership, recorded state, funding, routing and control relationships explicit. [Role discovery](references/contracts.md#discover-a-role-without-prior-session-context) connects a natural question to dated identity evidence and fresh publisher/onchain corroboration without requiring old chats or backups.

- **Contract reads first where useful:** authenticated getters and bounded enumeration for current state or efficient discovery, not a log reconstruction of an available balance.
- **History from execution evidence:** discover relevant generations and deployment/round bounds, estimate the retrieval work against actual provider limits, then use an appropriate authorized index/log path. Do not default to genesis or a runaway tiny-chunk/429 retry loop. Event discovery, pagination, receipt matching and canonical verification are separate results.
- **Accrual and conditional pace:** certify a contract-derived rate only with its applicable quantity, scale and epoch/pause/expiry mechanics. Separately, exact changes between pinned pending observations can support a labelled empirical ledger pace and explicit bounded scenarios. Neither a getter name nor a quiet interval proves earned origin or spendability.
- **Earned-only scenarios:** verified unspent earned accrual plus projected new accrual, minus commitments and simulated purchases. Exclude deposits, wallet funds and unattributed balances. Future prices and persistent rates remain explicit assumptions; gas and conversion funding are separate.
- **Availability before affordability:** effective zero inventory means not buyable now; a residual price getter is not an ask. A next scheduled window is a candidate opportunity. Keep opening-policy assumptions, executed-history comparators and conditional unsold-curve crossings separate.
- **Token/RPC economy:** load only relevant sections, reuse authenticated context and same-block observations, batch independent calls, fetch each receipt/header once, and stop when the question is answered. A thin skill does not itself guarantee fewer RPCs; host capability and evidence selection matter.
- **Claim-level results:** exact sale consideration, independently evidenced refunds, gas, origin attribution, discovery coverage and implementation-based forecasts have separate statuses. A successful receipt or correct pending disclaimer does not make the whole financial answer pass.

The agent may use inspectable local calculation code when needed under host permissions. That is not a bundled protocol client or permission to execute downloaded code. No Python dependency is required to load the skill; live access and exact arithmetic depend on actual host capabilities.

The installed [optional offline research aids](references/research-tools.md) provide `scripts/calculations.py`, the thin `scripts/research.py` CLI and `assets/schemas/research-evidence-v1.json`. Python 3.10+ and its standard library are needed only when choosing these helpers; tests and synthetic fixtures remain source-only under `research/`. Agents may use, adapt or ignore them, choose another language/store, or write a different solution. No helper invocation, dataset format or checkout is a prerequisite for answering; arithmetic input checks are not agent workflow controls. Installation does not run the helpers or grant execution permission. There is no transport client, live-data bundle, default deployment or automatic code download.

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
python3 -B research/check-research.py
```

After deliberate content changes, regenerate the manifest with `python3 -B maintenance/package.py build`. The maintenance tool also exports reviewed commits and creates deterministic archives. These tools are not installed with the skill. Update source provenance and affected references together; ordinary research never rewrites the package.

This host-native cutover removes the previous fixed snapshot, price, history and diagnostic clients and their execution catalogs. There are no compatibility commands or retired helper aliases. Existing host-native research tools replace them; any automatic discovery, checkpointing or batching must actually be supported or implemented by the host agent before being claimed.

The installed optional calculation toolkit does not restore the retired protocol clients. Specialized references own exact accounting, round dating, allowance windows, order-ID caveats and history coverage. Stale host workshop/install prompts need explicit host-maintainer cleanup outside this repository; package installation does not rewrite other skills, credentials or global instructions.

### Bundled research execution (unreleased)

The current revision installs the optional offline library, five-command JSON CLI (`weighted-price`, `rounds`, `pace`, `workload`, `curve`) and evidence-v1 schema, with exact JSON serialization and no source-checkout dependency. Tests and fictional fixtures stay outside the runtime. No transport, protocol defaults, automatic execution, dependency installation or wallet capability is added.

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
