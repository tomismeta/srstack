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

The installed skill contains instructions, concise topic references, dated source/policy records, a license and an integrity manifest. **No executable runtime, pinned contract addresses, bundled ABI catalogs, selectors, bytecode allowlists, embedded rates, wallet connector or background service.** Historical source citations may name past deployments or interfaces; they are provenance, not current execution bindings.

- **Contract reads first where useful:** authenticated getters and bounded enumeration for current state or efficient discovery, not a log reconstruction of an available balance.
- **History from execution evidence:** discover all relevant generations, use bounded index/log retrieval, deduplicate and verify events, and report the actual coverage. Exhausted pagination, receipt matching and canonical verification are separate results.
- **Accrual pace from the contract:** establish the applicable rate, eligible quantity, scale and epoch/pause/expiry conditions. A method name alone does not establish an earning rate or spendability.
- **Earned-only scenarios:** verified unspent earned accrual plus projected new accrual, minus commitments and simulated purchases. Exclude deposits, wallet funds and unattributed balances. Future prices and persistent rates remain explicit assumptions; gas and conversion funding are separate.
- **Token/RPC economy:** load only relevant sections, reuse authenticated context and same-block observations, batch independent calls, fetch each receipt/header once, and stop when the question is answered. A thin skill does not itself guarantee fewer RPCs; host capability and evidence selection matter.

The agent may use inspectable local calculation code when needed under host permissions. That is not a bundled protocol client or permission to execute downloaded code. No Python dependency is required to load the skill; live access and exact arithmetic depend on actual host capabilities.

## Install a reviewed release

The development branch is `feature/v0.3.0`; do not assume a `v0.3.0` release tag exists. Follow [reviewed installation](references/installation.md#reviewed-installation): resolve a full commit before review, export only its runtime files and clean-replace the old skill root. Do not overlay an older installation and leave retired scripts behind.

Maintenance verification runs from the reviewed repository outside the installed skill. Keep the source pin and recovery record outside the hashed runtime. Host loading and session refresh are host-dependent; no forced restart or automatic update is included.

### Quick test after installation

Check the actual loaded path and reviewed revision, then ask a real question. A bare invocation should invite a question, not run network calls or return a mandatory menu.

Suggested acceptance questions:
- Explain a packaged policy without live access.
- Inspect a public position using dynamically authenticated evidence; do not use a cached rate as current.
- Ask for all historical auction generations; disclose omitted contracts, ranges or verification stages rather than substitute a current-only table.
- Model earned-accrual buying; use the contract-derived starting pace, subtract costs and respect epoch boundaries.
- Repeat a calculation from the same evidence, then change one assumption. Check identical numerical outcomes for identical inputs and appropriate sensitivity without refetching unchanged data.

Record what the host actually read, calculated and answered. A package integrity check or synthetic calculation is not proof of live-provider access or host isolation. Repository-only acceptance cases (`maintenance/agent-acceptance.json`) are available in the source checkout, not the installed runtime.

For dogfooding, judge correctness, coverage, observed RPC cost and repeatability—not tool choice or a prescribed sequence. Count RPC methods separately from batch requests and index pages when the host exposes them; unknown counts stay unknown. Keep review records outside the skill. Missing live access is a blocked live check, not a failed installation.

**Deterministic results, flexible agents:** nontrivial arithmetic should use inspectable exact calculations with relevant reconciliation checks. Agents remain free to choose or write tools, investigate beyond the references and answer conditional questions without an execution facility. No required language, script, question menu, fixed call budget or permanent output artifact. Identical evidence and assumptions should reproduce identical numbers, not identical wording or tool calls.

## Safety and evidence

[Safety](references/safety.md) governs every host tool and delegated action. No signing, signature requests or transaction submission. Ready-to-sign calldata, deep links and filled unsigned objects require an explicit preparation request; a question about buying does not authorize preparation or execution.

Use host-managed credentials without exposing them to prompts, installed files or output. Preserve denials; do not evade access controls or silently repair failed evidence through another provider. Save reports or resumable collection checkpoints only as authorized, outside the installed skill, without credentials.

Dates describe reference provenance, not live freshness. Published policy, authenticated interfaces, source/implementation correspondence, observed state and modeled outcomes are different evidence levels. Forecasts are permitted with explicit assumptions; unsupported factual claims are not.

## Maintenance

From a reviewed source checkout with Python 3.10+:

```sh
python3 -B maintenance/package.py verify
python3 -B maintenance/check-package.py
```

After deliberate content changes, regenerate the manifest with `python3 -B maintenance/package.py build`. The maintenance tool also exports reviewed commits and creates deterministic archives. These tools are not installed with the skill. Update source provenance and affected references together; ordinary research never rewrites the package.

This host-native cutover removes the previous fixed snapshot, price, history and diagnostic clients and their execution catalogs. There are no compatibility commands or retired helper aliases. Existing host-native research tools replace them; any automatic discovery, checkpointing or batching must actually be supported or implemented by the host agent before being claimed.

Cutover verification: 19 packaging regression tests passed; an isolated reviewed-commit export and the documented clean-replacement procedure passed external byte verification and retained the previous root. Two tool-free model exercises loaded the exported instructions and correctly handled synthetic earned-only reinvestment/epoch boundaries and incomplete cross-contract auction history. These are package and instruction-behavior checks, **not** a live RPC run, tool-enabled host replay or proof of host isolation.

Calculation-readiness verification additionally exercised exact reservation-to-fill accounting, delayed activation, pauses, epoch assumptions, purchase-price sensitivity, integers above binary floating-point's exact range, and shuffled/duplicate historical executions. A separate tool-free model exercise matched the executed synthetic projection outcomes without demanding a workflow. These checks prepare the skill for real-host dogfooding; they do not establish live deployment semantics or measured production RPC efficiency.

## License

Original code, summaries and instructions are [MIT-licensed](LICENSE). Third-party documents, media, trademarks and protocol code retain their owners' rights and are excluded from that grant. Source links do not imply affiliation or transfer those rights.
