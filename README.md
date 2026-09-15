# srstack

**Standard Reserve research, guided scenario planning and live read-only inspection for AI agents.**

srstack explains documented protocol mechanics, reads current public state and compares expansion strategies using assumptions you approve. It is one independent [Agent Skill](https://agentskills.io/specification), not an official Standard Reserve product, trading bot or wallet toolkit.

**0.1.1 candidate · planner schema/model 1.** This README describes the candidate, including shared market pricing and gross valuation. Export an exact reviewed commit to try it; published versions and their separate audit evidence remain on the [releases page](https://github.com/tomismeta/srstack/releases). No 0.1.1 release is published yet.

## What you can ask

| Question | What srstack provides |
|---|---|
| “How do charter withdrawals work?” | Branch retirement, credit release, fees and unresolved mechanics |
| “What are the current issuance rate and buy/sell taxes?” | Fresh block-scoped protocol observations, not stored launch values |
| “Compare expansion strategies using these assumptions.” | Keep/selective/aggressive calculations with explicit costs and limitations |
| “Which assumptions depart from the documentation?” | Documented-rule conflicts and unresolved semantics |
| “Are expansion licenses available at a usable price?” | Fresh auction status and inventory; no purchasable quote when unavailable |
| “Show the branches and pending balance of this public charter.” | A charter-ID-specific snapshot; no wallet connection or claim that you own it |
| “What is STANDARD trading at, or what is this amount worth?” | Latest reported canonical-pool USD/ETH prices and a gross indicative valuation |
| “Which contracts are listed, and is their source verified?” | Publisher-listed identities and explorer links; verification status requires a fresh explorer check |
| “What has the team announced?” | Fresh official-post research where the host can retrieve it; no bundled recap |

One skill, three routes:

- **Research:** source-linked explanations, documented parameters and evidence gaps.
- **Plan:** a guided conversation: describe your position, budget and goal; choose current, hypothetical or both price cases; review an assumption sheet; then approve a local comparison. Explicit prices take precedence. Documented mode blocks known conflicts; stress mode reports approved departures. No silent economic defaults.
- **Inspect:** on-demand protocol, auction and public-charter snapshots through the fixed RPC helper, plus a separate canonical-pool price reader for current price and gross balance-value questions. No wallet access.

Research topics: [protocol](references/protocol.md) · [charters](references/charters.md) · [reserves](references/reserves.md) · [contracts](references/contracts.md) · [updates](references/updates.md) · [documents](references/documents.md) · [risks](references/risks.md).

These are routing instructions within one skill, not separately installed commands. `Use srstack` returns the three-route menu. `/srstack` works where the host registers an installed skill command; other command syntax varies by host.

## Requirements

| Capability | Host requirements | Network access |
|---|---|---|
| Explain packaged rules | Read the skill and its selected resources | None |
| Research announcements or explorer status | Permitted public web retrieval | Relevant official pages or explorer |
| Run approved scenarios | Trusted package, permitted Python 3.10+ execution and safe JSON input | None; the planner is offline |
| Inspect current state | Trusted package and permitted Python 3.10+ execution | Fixed public Robinhood Chain RPC |
| Read market price or gross balance value | Trusted package and permitted Python 3.10+ execution | Fixed public DEX Screener canonical-pool endpoint; charter balances additionally use RPC |

All three helpers use only Python's standard library: no pip dependencies, wallet connector or provider credentials. Execution also requires the filesystem protections described in [execution](references/planning-execution.md); unsupported hosts fail closed. Missing execution or retrieval capability produces an explanation, not invented results. The skill does not install dependencies or change host permissions.

## Quick start

This candidate is available through the reviewed-commit export below. For a tagged release instead, follow that release's documentation and verify its attached runtime ZIP against `SHA256SUMS`.

**Install a runtime export or attached runtime ZIP—not a full repository, GitHub's automatic “Source code” archive or an audit archive.** Audit evidence is not an installable skill or a smart-contract security certification.

### Export an exact reviewed commit

The export machine needs Git and Python 3.10+. The installed host needs only the capabilities for the routes you use.

1. Review [SKILL.md](SKILL.md), the [safety boundary](references/safety.md) and the complete package. Select a full immutable commit SHA you trust and have reviewed, not the moving `main` branch.
2. From your chosen working directory (the intended workspace for OpenClaw workspace installation), clone a review copy and select that revision:

   ```sh
   REVIEWED_COMMIT=REVIEWED_COMMIT_SHA
   git clone https://github.com/tomismeta/srstack.git srstack-review &&
   git -C srstack-review checkout --detach "$REVIEWED_COMMIT"
   ```

   Replace `REVIEWED_COMMIT_SHA` with the full 40-character commit SHA you reviewed; it is a placeholder, not a release identifier. Stop on any error. The export command below independently checks that the selected commit matches the checkout, so a failed checkout cannot silently install the default branch.

3. Choose **one** installation parent. For Hermes' default profile:

   ```sh
   SKILL_PARENT="$HOME/.hermes/skills"
   ```

   Or, for OpenClaw in the workspace where you ran the clone:

   ```sh
   SKILL_PARENT="$PWD/skills"
   ```

   Named profiles and managed installations may use different roots; use the intended host's configured location. Export the reviewed commit's manifest-listed runtime files into a new skill folder:

   ```sh
   mkdir -p "$SKILL_PARENT" &&
   python3 -B srstack-review/maintenance/package.py export \
     --commit "$REVIEWED_COMMIT" \
     --destination "$SKILL_PARENT/srstack"
   ```

   The destination must not already exist. Export validates the selected commit's runtime membership, per-file hashes and aggregate digest before creating it. It reads committed content, not uncommitted runtime edits, and excludes Git metadata, maintenance tools, tests, CI configuration and local build/cache artifacts. Failed exports clean up the new destination. Review the helper itself as part of the selected commit; do not run unreviewed local modifications.

   For updates, preserve customizations outside all skill-discovery roots, then remove the old active installation before exporting into the now-absent destination. Keep the review clone outside those roots too. Do not overlay files, use `cp -a` on the repository or leave a shadowing same-name copy. Start or refresh the host only after export succeeds. A full repository may load in a host, but it is not the supported runtime installation.

4. Have the host verify the installed files against `release-manifest.json`: `content_files` maps relative paths to SHA-256 hashes, and `digest_convention` specifies the aggregate `content_sha256`. Confirm the actual loaded path and revision, and that repository-only `.git`, `maintenance`, `.github` and `dist` directories are absent. Matching listed hashes alone does not detect extra files or establish trust in an otherwise unreviewed package.
5. Start a fresh conversation and try a packaged-knowledge question from the examples below.

**Hermes installation:** use the complete-bundle instructions above. URL discovery depends on configured sources; importing raw `SKILL.md` does not necessarily import its references, assets and scripts.

Other harnesses can use their Agent Skills loader or explicitly read [SKILL.md](SKILL.md) and selected resources. Resource paths resolve against the loaded skill directory. See [host setup](references/installation.md); this package never installs itself or changes host permissions.

## Examples

### Conversation starters

```text
Use srstack.
```

Expected: the research/plan/inspect menu, without fetching live data.

```text
Use srstack to explain charter withdrawals.
Use only the packaged references and cite the source links.
```

Expected: a sourced explanation, including fees and evidence gaps.

### Guided planning

```text
Use srstack to help me compare keeping my branches versus expanding.
I have 2 branches and 100 credits, can spend another 0.25 ETH,
and want to compare a full exit after 30 days. Walk me through the assumptions.
```

The agent asks only for missing decisions in small groups, explains unfamiliar inputs and proposes a plain-language assumption sheet. Approve it or change individual items; you do not need to supply JSON. Missing data stays missing rather than becoming a made-up number. If gas is unknown, you may explicitly approve a preliminary comparison excluding specified gas costs; those results must be labelled before the excluded costs, not all-in.

No numerical comparison runs until all economic assumptions and the mode are explicit and approved. A complete, already acknowledged input can still use the direct path without another questionnaire. See the [planning workflow](references/planning.md).

To start from current protocol observations:

```text
Use srstack plan. Read the current protocol and auction settings.
Show the proposed assumptions, then ask me only for what's still missing.
```

The agent proposes supported fresh observations for approval, then asks for missing assumptions. Documented ceilings are constraints, not current rates or balances. Failed reads are not filled from launch defaults, recap figures or fictional examples. Holding current settings constant into the future requires approval; the scenario model does not reproduce dynamic contract execution.

For projections, choose **use the latest market price**, **supply a hypothetical price**, or **compare both**. The agent asks for that choice before fetching an unspecified projection price. “Use current prices” already authorizes the lookup; holding that observation constant or applying growth into the future still requires explicit assumptions. Supplied prices take precedence, and complete offline or fictional scenarios do not trigger a price lookup.

### Runnable fictional planner demonstration

```text
Use srstack plan in documented mode with the installed assets/examples/planning.json.
These are fictional demonstration inputs, not my holdings or market expectations.
Verify the trusted package, use the JSON unchanged, and compare all three strategies.
Do not refresh sources or persist anything.
```

With permitted Python execution and a trusted package, expect a concise estimated comparison in `documented` mode with keep/selective/aggressive results. Missing prerequisites produce a short explanation, not invented results. The fixture's values are not recommendations or economic defaults.

For a direct engine smoke test, run **from the reviewed installed skill root**:

```sh
python3 -B -I scripts/scenario.py < assets/examples/planning.json
```

Expected: exit 0 and JSON containing the warning, the three strategies and their conformance report. This tests the engine, not host discovery or sandbox isolation. `scripts/scenario.py` is the only intended planner executable; do not substitute model-generated formulas or downloaded helpers. CLI output is JSON and may be verbose even in summary mode; agents should summarize it for users. Request `detail: "full"` for detailed accounting and purchase schedules. History requires full detail.

### Live protocol, auction and charter reads

```text
Use srstack inspect protocol. Show current issuance and buy/sell taxes.
Use srstack inspect auctions. Are licenses available, and what price is actually usable?
Use srstack inspect charter <public charter ID>. Show its branches and pending balance.
```

The reader checks the chain, block, code, module bindings and scalar decoding. Sold-out or disabled auctions do not produce purchasable quotes. A specific charter request also needs its public charter ID; it never needs a wallet connection.

Replace `<public charter ID>` with the ID to inspect.

| View | Selected observations |
|---|---|
| `protocol` | Issuance and epoch context, branch count, token supply, counter-based remaining budget, buy/sell tax and pool/emissions state |
| `auctions` | License and daily-charter activation, pause state, inventory, duration and available current prices |
| `charter` | Public owner, branch count, pending balance and related issuance context |

Each invocation uses one checked block. Separate example invocations are not one atomic combined snapshot; do not combine their values as if they share a block. Failed fields remain missing with errors; fatal failures return no snapshot. Results are not saved or reused as a fallback. These are selected publisher-ABI reads, not a complete contract audit.

Advanced users can request the same protocol snapshot from the reviewed installed root:

```sh
printf '%s' '{"schema_version":1,"view":"protocol"}' | python3 -B -I scripts/snapshot.py
```

Views are `protocol`, `auctions` and `charter`; the last requires integer `charter_id`. `detail: "full"` adds raw responses and call mappings. Default answers show useful values first, with at most one short note such as **“RPC snapshot; publisher ABI.”**

### Current price and gross accrued-balance value

```text
Use srstack inspect price. Show STANDARD in USD and ETH.
What is 1000 STANDARD worth at the latest reported market price?
What is the accrued balance of public charter <public charter ID> worth now?
```

Current-value questions use the shared price reader automatically; there is no prerequisite `inspect price` step. A charter valuation reads that charter's balance, then passes the successful `charter_pending` quantity to `scripts/price.py`. This is a gross market mark of a STANDARD-denominated ledger balance—not wallet tokens, net withdrawal proceeds or a branch/NFT resale price. It does not value future earning capacity.

The reader makes one fixed public request for the exact canonical ETH/STANDARD pool. It validates chain, token, quote asset and pool identity, and computes any amount valuation locally without sending the amount to the provider. No ticker search, first-pair selection, arbitrary endpoint or saved-price fallback is used.

From the reviewed installed root:

```sh
printf '%s' '{"schema_version":1}' | python3 -B -I scripts/price.py
printf '%s' '{"schema_version":1,"standard_amount":"1000"}' | python3 -B -I scripts/price.py
```

The optional amount is an unsigned decimal **string**, not a JSON number. Usable prices and gross values are decimal strings. A failed denomination remains missing; if no usable price is available, the helper fails without a fallback value.

These are **provider-reported indicative prices**. The API does not supply a quote-observation timestamp: retrieval time is not quote age, and pool creation time is not price freshness. A charter block and a price retrieval are separate observations, not an atomic combined snapshot. Gross values exclude withdrawal fees, trading taxes, LP fees, slippage and gas.

## Contract coverage

The [contract catalog](assets/entities/robinhood.json) contains **14 publisher-listed identities on Robinhood Chain (4663)**. The fixed [publisher read interface](assets/interfaces/robinhood-reads.json) supports selected live reads from **six**:

| Contract | Questions supported by fresh reads |
|---|---|
| **$STANDARD** | What are total token supply, maximum supply and hard cap? `totalSupply()` is not necessarily circulating supply. |
| **Central Bank** | What are the issuance rate, multiplier, stream rate, branch count and epoch? What budget remains according to the issuance counters? |
| **Charter NFT** | Who owns public charter X? Combined with Central Bank reads, how many branches and pending credits does it have? |
| **Trading Hook** | What are current buy/sell taxes? Is an override active? Is the pool initialized? |
| **Expansion License Auction** | Is it started or paused? How much inventory remains? Is there a usable current price, and what is the auction duration? |
| **Charter Auction** | Are daily charter sales enabled? Is inventory available, and what is the usable ETH price and auction duration? |

The other eight have **identity and documented-role coverage, not fixed-helper live-read support**: Founding Sale, Expansion Vault, Contraction Vault, Liquidity Manager, Fee Splitter, Address Registry, Uniswap v4 Pool Manager and Multicall. Their addresses and explorer links are in the catalog; current holdings, permissions and implementation details require separate fresh research.

**Publisher-listed addresses and publisher ABIs are not independently verified Solidity source code.** The package bundles no independently verified contract source and stores no explorer verification verdicts. Current verification status requires a fresh explorer check. Getter observations do not establish complete administrator powers, upgradeability, audit correspondence or exploit resistance. Source dates identify reference provenance, not live-state freshness.

## Coverage and footprint

The package covers the 16-section whitepaper, contract identities and publisher ABI definitions. It stores no changing-state snapshots, recap metrics or explorer verification verdicts. Current balances, rates, supply, inventory, prices, activation, verification status and announcements require fresh retrieval; unavailable data stays unavailable.

For evidence-assisted planning, ask: **“Use srstack plan. Read the current protocol and auction settings, propose inputs, then ask me for what is missing.”** The [handoff](references/planning-inputs.md#deployment-evidence-handoff) keeps observations separate from approved future assumptions. It distinguishes current stream rates, remaining-budget accounting, sale taxes, LP fees and unavailable auctions. No financial execution is added.

The package uses selected references and indexed records rather than loading the whole corpus for every question. The reference indexes own current inventory counts; disk size is not per-question token cost, and selective loading depends on the host.

Packaged research needs a resource reader. Calculations and public readers use **Python 3.10+ and its standard library**, with no pip dependencies. Chain reads use the fixed Robinhood RPC; market prices use the fixed DEX Screener pool endpoint. No wallet connector, telemetry or self-update process is bundled.

## Safety and verification limits

Answers lead with content. Estimates get a short label; observations get a brief source note where needed. Detailed provenance and assumptions are available on request, not repeated as small print.

The scenario engine is offline. The snapshot helper reads two fixed catalogs and permits only its pinned view/pure calls on the configured Robinhood addresses. The price helper reads only the fixed identity catalog and makes a fixed-host canonical-pool GET; optional quantity multiplication is local. All three reject unsupported inputs and write no files. No wallets, credentials, signatures, transaction payloads or state-changing simulations. See [safety](references/safety.md) and [execution](references/planning-execution.md) for the full boundary.

The readers do **not** supply liquidity-depth analysis, an amount-specific withdrawal quote, transaction gas estimates or guaranteed sale proceeds. The planner does **not** reproduce changing policy, auction competition or contract execution; it compares explicit hypothetical inputs rather than forecasting returns. Source verification and announcements use separate fresh web research.

Skill instructions do not enforce host isolation, and estimates are not guaranteed returns.

## Repository validation

These commands run from the **repository root**, not the installed skill folder:

```sh
python3 -B maintenance/package.py verify
python3 -B maintenance/check-planner.py
python3 -B maintenance/check-snapshot.py
python3 -B maintenance/check-price.py
python3 -B maintenance/check-package.py
python3 -B maintenance/package.py archive
```

The checks use Python's standard library and local Git; they do not call explorers, connect wallets or use model/API credentials. CI runs them on Python 3.10 and 3.14, with read-only repository permissions and commit-pinned Actions. GitHub checkout and Python provisioning require network access; the validation commands themselves are offline. CI verifies the committed manifest rather than regenerating it, and checks deterministic ZIP output. It does not upload artifacts, tag, publish releases or monitor contracts.

After deliberate runtime changes, regenerate the manifest with `python3 -B maintenance/package.py build`, then run the checks above. `dist/srstack-0.1.1.zip` contains only the candidate runtime package. Maintenance tooling and CI files are repository-only and never authorize an installed skill to execute them.

## Feedback and license

Report reproducible problems through [GitHub issues](https://github.com/tomismeta/srstack/issues), including the host/version, package commit, actual loaded path and redacted reproduction. Never upload wallet credentials, private RPC URLs or private conversation history.

Original srstack code, summaries and instructions are [MIT-licensed](LICENSE). Third-party documents, posts, media, trademarks and protocol code retain their owners' rights and are excluded from that grant. Source links and quotations do not transfer those rights or imply affiliation.
