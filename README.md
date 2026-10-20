# srstack

**Question-driven Standard Reserve research and analysis for AI agents.**

Ask about protocol mechanics, live positions, historical auctions or what earned accrual could buy. The agent chooses the evidence and calculations the question needs, using its existing host-authorized tools. No topic command, calculator wizard or fixed sequence is required.

Independent [Agent Skill](https://agentskills.io/specification), not an official Standard Reserve product. **Version 0.5.0 — unreleased dogfood candidate.** [Installation](references/installation.md) still defaults to the reviewed `v0.4.1` release; use an explicit full candidate commit for 0.5.0 dogfooding.

## What you can ask

- “How are my charter's branches doing?”
- “Do I need to check in?”
- “Show every auction round across contracts, with opening, first, average and last sale prices.”
- “Based only on earned accrual, what could I afford in the next auctions?”
- “What changes if I buy more branches, and when would they affect accrual?”
- “What does the Second Mandate say, and what is actually deployed?”
- “What changed in the v1.1/v1.2 auctions, and how do limit orders work?”
- “What is the S-Bill rate, what would this deposit quote, and which of my bills mature on a given day?”
- “How much S-Bill principal matures protocol-wide that day, and is the discovery complete?”
- “Where do POL buybacks go, and what actually gets burned?”
- “What does recent sellout history suggest for the next auction close?”
- “What fees apply to the Reserve's stock pools, and what could an LP actually earn?”
- “Which launchpad generation created this token, and what can its creator change?”
- “How do charter distributions and market-pilot points differ from spendable rewards?”

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

## Agent compatibility

srstack uses the Agent Skills format rather than a host-specific client. Install the complete runtime, not only `SKILL.md`; live research and optional calculations use the host's authorized capabilities.

| Agent | Recorded compatibility |
| --- | --- |
| **Hermes** | Pinned native loading, resource-byte, guard, default-preprocessing and temporary-install checks passed during the 0.4.1 review; four medium guard warnings retained. |
| **OpenClaw** | Pinned native-source loader, eligibility, official validation and packaging checks passed during the 0.4.1 review. |
| **Muse** | User-reported v0.2.2 installation and integrity checks passed. End-to-end network helper execution was unavailable in that sandbox; no v0.4.1 Muse verification is claimed. |
| **Other Agent Skills hosts** | Use the complete runtime and verify loading, resource access and the capabilities needed for the question. Compatibility is not assumed from the format alone. |

See [host installation and capabilities](references/installation.md#host-loading-and-sessions). These checks are scoped evidence, not fresh-session acceptance or universal live-access/safety guarantees; Muse support remains recorded at its reported version.

## Install a reviewed release

The reviewed release tag is `v0.4.1`. Follow [reviewed installation](references/installation.md#reviewed-installation): resolve the tag or supplied full commit before review, export only its runtime files and clean-replace the old skill root. Do not overlay an older installation and leave retired scripts behind.

For the unreleased **0.5.0** candidate, select a full commit from `feature/0.5.0-ecosystem-dogfood` and set `SRSTACK_COMMIT` before following that procedure. A branch name is not an immutable installation pin. This candidate includes the post-0.4.1 navigation and ecosystem integration work; it has no release tag and does not inherit the historical 0.4.1 release approval.

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

### Release acceptance and bounded release scope

A release candidate must be exercised in a fresh session using only its exported runtime—not a previous install, retired catalog/helper or stale workshop prompt. Record installation/loading, authorized host capability, provider/evidence coverage, reasoning/decoding and final answer separately as pass, fail, blocked or not run.

The acceptance suite covers direct pinned state; exact purchase-event/receipt verification; auction inventory/order/allowance interpretation; source-grounded accrual and an attributable real earned-only scenario; fixed-window/epoch boundaries; cross-generation history; evidence reuse; and correct failure classification. Include adverse cases for mixed-origin funds, precision, dynamic arrays and internally invoked purchases missed by direct-transaction discovery. A correct unknown passes uncertainty handling, not the unavailable numerical or completeness gate. The source-checkout acceptance file defines the detailed cases; these are review checks, not an intake wizard for ordinary users.

Version **0.4.1** has an owner-approved bounded repository/runtime release, not blanket fresh-session acceptance. Shared profiles, incomplete artifact/timing retention and unsupported recovery interpretations limit the native-host evidence; later diagnostic guidance was checked offline, not proved to improve live-agent compliance. Collector timings are not end-to-end latency or a universal speed guarantee. Failed, blocked, wrong-pin, incomplete and unexercised claims remain unpassed; not all mandatory scenario/profile combinations are established.

Deployed accrual/lazy-roll/reset mechanics, source/compiler correspondence, attributable earned-only funding, refund/internal-flow attribution and complete canonical history remain uncertified; a real attributable earned-only 24-hour scenario remains blocked. Reviewed interfaces are not the full deployed surface. Historical sample/archive checks do not close purchase-event anchor or interior-discovery gaps, and assisted replays do not prove unassisted live acceptance. S-Bill security-review completion is attributed to user-reported developer confirmation, not independently mapped public reports or deployment correspondence. Source coverage/conflicts remain qualified in [updates](references/updates.md), not universal synchronization.

Scanner advisories and adjudicated public-identifier false positives remain disclosed; local reviews are not hosted approval or host isolation guarantees. ClawHub publication, hosted approval and terms acceptance remain deferred; MIT and wallet/host boundaries are unchanged. Detailed release decisions, evidence attributions and retained historical limitations are in the source checkout at `maintenance/review-history.md` (not installed).

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

## License

Original code, summaries and instructions are [MIT-licensed](LICENSE). Third-party documents, media, trademarks and protocol code retain their owners' rights and are excluded from that grant. Source links do not imply affiliation or transfer those rights.
