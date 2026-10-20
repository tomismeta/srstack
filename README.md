# srstack

**Question-driven Standard Reserve research and analysis for AI agents.**

Ask about protocol mechanics, positions, auctions, stock-pool fees, launchpad controls or rewards. The agent selects the evidence and calculations the question needs using its existing host-authorized tools. No topic command, calculator wizard or fixed sequence is required.

Independent [Agent Skill](https://agentskills.io/specification), not an official Standard Reserve product. **Version 0.5.0.** Follow [reviewed installation](references/installation.md) for the `v0.5.0` release or an explicitly supplied full commit.

## What you can ask

| Topic | Example questions |
| --- | --- |
| [Charters and branches](references/charters.md) | How are my branches doing? Do I need to check in? What changes if I buy more? |
| [Auctions and forecasts](references/auctions.md) | What sold in earlier rounds? What could earned accrual afford next? How do limit orders work? |
| [S-Bills](references/sbills.md) | What would this deposit quote? Which bills mature that day, and is the discovery complete? |
| [Policy and reserves](references/protocol.md) | What does the Second Mandate say versus what is deployed? Where do buybacks and fees go? |
| [Stock liquidity](references/liquidity-markets.md) | What fees apply to these pools, and what could an LP actually earn? |
| [Launchpad tokens](references/launchpad.md) | Which generation created this token? What can its creator change, and what does URC5 enforce? |
| [Charter distributions](references/charter-distributions.md) | How do stimulus, burn compensation and launch-token drops differ? Can I claim or spend an allocation? |
| [Market pilot](references/market-pilot.md) | What do points and the advertised reward pot establish, and which published rules conflict? |

## New in 0.5.0

- Native coverage of stock liquidity, both coexisting launchpad generations, creator controls/URC5, market-pilot rules and charter distributions.
- The complete 93-declaration SessionFeeHook ABI within its retained explorer-reader representation, with dated identity/provenance and exact layouts. Fee reads no longer require reacquiring that ABI from an explorer; current identity and state still require authorized evidence.
- Question-driven navigation and a broader skill description, without a second product-specific assistant or mandatory workflow.
- Optional `SRSTACK_WORK` for predictable installation recovery paths, with pre-clone separation/filesystem checks, exclusive creation and retained rollback.

Current quantities require fresh evidence. Packaged knowledge can answer explanations offline. Unknown positions, inaccessible evidence and hypothetical inputs remain distinct; missing information is not zero.

## Minimal architecture

The installed skill contains [capability planning](references/capabilities.md), [dated contract identities](references/contracts.md), [reviewed interface inventories](references/interface-inventory.md), topic/source references and an integrity manifest. The [object map](references/object-map.md) separates economic objects, contracts, ownership, funding and control; [role discovery](references/contracts.md#discover-a-role-without-prior-session-context) authenticates the identity relevant to a question.

**No RPC transport, active deployment router, bytecode allowlist, embedded live rates, wallet connector or background service.** Reviewed interfaces supply encoding and decoding knowledge, not permission, current state, complete deployed correspondence or successful execution. The inventory is neither an allowlist nor a mandatory read sequence.

The [research workflow](references/research-workflow.md) and [collection guidance](references/collection-efficiency.md) cover scoped discovery, pinned evidence, batching and reuse. Core distinctions remain explicit: earned accrual versus deposits/unattributed balances; availability versus affordability; quotes versus execution; points/allocations versus spendable receipts; and observed history versus conditional forecasts. Missing evidence limits the dependent claim, not every useful answer.

Optional [offline research aids](references/research-tools.md) include exact calculations, the thin `scripts/research.py` CLI, schemas and explicitly fictional examples. Python 3.10+ and its standard library are needed only when choosing those helpers—not to load the skill. Agents may use another language or inspectable tool. Regression machinery stays source-only; installation grants no execution permission and downloads no code automatically.

[Projection recipes](references/calculations.md) start from relevant [curated round history](references/round-datasets.md), not an assumed policy opening. Live observations and research stores remain outside the installed runtime. No latency, token-saving or universal RPC-efficiency guarantee is claimed.

Live support depends on actual host capabilities: authorized public reads, applicable ABI/Keccak encoding/decoding and exact calculation; history additionally needs adequate archive/event/index/receipt coverage. Dated explanations and conditional reasoning remain useful without those capabilities. No particular language, client or provider is required.

## Agent compatibility

srstack uses the Agent Skills format rather than a host-specific client. Install the complete runtime, not only `SKILL.md`; live research and optional calculations use the host's authorized capabilities.

| Host / evidence | Recorded scope |
| --- | --- |
| **Muse — owner-supplied October20 0.5.0 dogfood reports** | Exact primary installation, separately verified catalog-mirror transformation, fresh-session discovery, bundled-ABI live stock-fee reads and targeted regressions passed. Host connector setup remains outside srstack. |
| **Second dogfood host — owner-supplied October20 reports** | Exact installation, fresh-session path/version/digest verification, public-RPC stock-fee reads without explorer retrieval, installation guard exercises and targeted regressions passed. No blanket host-brand certification is inferred. |
| **Local OMP — maintainer-exercised 0.5.0 candidate** | Explicit standalone loading and native synthetic ABI-byte decoding passed. Separate pinned Alchemy reads verified the packaged hook interface and pool identities; these were driver-executed, not an unassisted host-discovery run. |
| **Hermes — pinned-source 0.5.0 checks** | Native imported installation/loading, exact resource bytes and default preprocessing passed; four medium guard warnings retained. The separate create-new-skill validator rejects the 220-character description against its 60-character budget; imported installation does not use that authoring gate, and the host may truncate index descriptions. |
| **OpenClaw — pinned-source 0.5.0 checks** | Native-source loading, eligibility, format validation and packaging passed with exact resource bytes. The supported JavaScript filesystem fallback was exercised; the optional native addon was unavailable. Not interactive-agent acceptance. |

These are scoped observations for tested candidates, not the full pristine-profile acceptance matrix or universal live-access/safety guarantees. A host-managed mirror must be checked for correspondence separately from primary runtime byte identity. See [host loading and sessions](references/installation.md#host-loading-and-sessions); detailed provenance and historical limits remain in source-only `maintenance/review-history.md`.

## Install a reviewed release

The reviewed release tag is `v0.5.0`. Follow [reviewed installation](references/installation.md#reviewed-installation): resolve the tag or supplied full commit before review, export only its runtime files and clean-replace the old skill root. Do not overlay an older installation and leave retired scripts behind.

For a separately reviewed candidate, supply its full commit as `SRSTACK_COMMIT`. A branch name is not an immutable pin. The explicit-commit procedure never silently substitutes the default release tag for the requested revision.

Detect the actual discovery roots, preserve rollback outside all of them and verify runtime integrity before and after replacement. Optional `SRSTACK_WORK` selects a new absolute recovery path; rejected paths may leave an empty directory, but no clone is created before separation/device checks pass. Use real, resolved directory paths: the verifier rejects symlinked roots/ancestors, and replacement refuses a symlink installation target.

Maintenance verification runs from the reviewed source checkout outside discovery. Keep source pins and recovery records outside the hashed runtime. A fresh session must confirm the actual loaded path and content; installation alone does not prove loading. No forced restart or automatic update is included.

### Quick test after installation

Check the actual loaded path and reviewed revision, then ask a real question. A bare invocation should invite a question, not run network calls or return a mandatory menu.

Suggested acceptance questions:
- Explain a packaged policy without live access.
- Read stock-pool fees with the packaged ABI, pinned identity/state, callback-sender scope, units, pauses and overrides; do not substitute a historical schedule when access fails.
- Distinguish charter ETH funding from branch-ledger funding, both launchpad generations and creator controls, and pilot points from payable rewards.
- Ask for cross-generation auction history and earned-only scenarios; retain omitted ranges, attribution gaps, inventory and epoch boundaries rather than claim unsupported completeness.
- Repeat a calculation from unchanged evidence, then change one assumption. Reuse collected evidence for a summary without refreshing it.

Record what the host actually read, calculated and answered. A package integrity check or synthetic calculation is not proof of live-provider access or host isolation. Repository-only acceptance cases (`maintenance/agent-acceptance.json`) are available in the source checkout, not the installed runtime.

For dogfooding, judge correctness, coverage, observed RPC cost and repeatability—not tool choice or a prescribed sequence. Count RPC methods separately from batch requests and index pages when the host exposes them; unknown counts stay unknown. Keep review records outside the skill. Missing live access is a blocked live check, not a failed installation.

### Release acceptance and bounded release scope

The 0.5.0 dogfood evidence supports **bounded installation/loading, packaged-interface live reads and targeted reasoning regressions**. Both reported hosts exercised the updated stock hook without explorer ABI retrieval. Maintainer verification also covered exact exports, offline regressions, synthetic native decoding and pinned live reads. No current fee table is installed from those observations.

The full source-only acceptance suite (`maintenance/agent-acceptance.json` in the repository) was **not run in a pristine isolated profile across every mandatory scenario**. Its cases cover direct state, purchase events/receipts, inventory/order/allowance interpretation, earned-only attribution, epoch boundaries, cross-generation history, reuse and error classification. A correct unknown passes uncertainty handling, not the unavailable numerical or completeness gate. The suite is a release-review contract, not an intake wizard for ordinary users.

Deployed accrual/lazy-roll/reset mechanics, independent source/compiler correspondence, attributable earned-only funding, refund/internal-flow attribution and complete canonical history remain uncertified. A real attributable earned-only 24-hour scenario remains blocked. S-Bill security-review completion is attributed to developer confirmation, not independently mapped reports or deployment correspondence. [Source conflicts](references/updates.md), including pilot accounting and integrator-fee descriptions, remain qualified rather than silently reconciled.

The October20 stock-hook evidence fingerprints a retained reader-parsed explorer representation, canonical ABI and decoded source strings—not original HTTP bytes. Matching explorer-returned deployed bytes at one observed block does not establish an independent recompilation or whole-contract audit. Fee getters do not certify swap success, backing, custody or LP income.

October20 0.5.0 release-readiness checks covered exact runtime packaging, offline regressions, isolated static/behavioral and secret scans, dependency audits and local host-source compatibility. File-count/deep-reference advisories, maintenance execution diagnostics and public-identifier false positives remain recorded; results were not raw-clean or proof of complete recursive coverage. The owner authorized a bounded repository/runtime release with these limits retained. Final-input evidence and artifact identities accompany the release. Local scanner/reviewer results are not hosted approval or host-isolation guarantees; ClawHub publication, hosted approval and terms acceptance remain separate decisions.

Record pass/fail/blocked/not-run per claim, with actual loaded revision, provider coverage and evidence. The bounded 0.5.0 release decision does not turn failed, blocked or unexercised claims into passes or authorize later releases. Detailed decisions and evidence attributions belong in source-only `maintenance/review-history.md`, not the installed runtime.

**Deterministic results, flexible agents:** identical evidence and assumptions should reproduce identical numbers—not identical wording or tool calls. Nontrivial arithmetic needs inspectable exact calculation and relevant reconciliation, without prescribing a language, helper, fixed call budget or permanent output artifact.

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

The optional calculation toolkit does not restore the retired snapshot/price/history clients, execution catalogs or compatibility aliases. Specialized references own accounting and history rules. Host-maintainer cleanup of stale prompts, mirrors or other skills remains outside this repository; installing srstack does not rewrite credentials or global instructions.

## License

Original code, summaries and instructions are [MIT-licensed](LICENSE). Third-party documents, media, trademarks and protocol code retain their owners' rights and are excluded from that grant. Source links do not imply affiliation or transfer those rights.
