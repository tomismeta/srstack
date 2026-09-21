# srstack

**Standard Reserve expertise, analysis and user-directed workflows for AI agents.**

srstack explains protocol mechanics, investigates current and historical state, models scenarios and helps with requested research workflows. It is one independent [Agent Skill](https://agentskills.io/specification), not an official Standard Reserve product. It does not sign wallet messages/transactions or submit transactions, directly or through delegated tools.

**Version 0.2.2 · dogfood candidate on `feature/v0.2.2`.** Removes skill-imposed limits on requested modelling, forecasting, strategy comparisons, private-data analysis, authenticated research, exports, monitoring and nonbroadcast simulation. Bundled catalogs and helpers describe convenient implementations, not a capability allowlist. Normal host permissions, evidence integrity and credential protection remain. The `v0.2.2` tag is not yet published; use the full reviewed candidate commit below, not the version or moving branch alone.

**Helper continuity:** the retired `scripts/scenario.py` and fictional fixture are not restored. Requested models and workflows may use existing host tools or inspectable locally authored code; “no bundled simulator” is not a reason to refuse analysis. The verifier has no `--offline` flag: its default is offline integrity verification. Install a clean runtime export rather than overlaying old files.

**Read coverage retained:** compact charter summaries, original HTTP-denial diagnostics, bounded auction/buyback history, auction controller/pending ownership, queued CentralBank policy/recycling, and treasury routing/controls with approval-gated selected-asset raw holdings. No new cataloged contract identities or claimed Second Mandate deployment. Prior release audit results do not cover edited bytes.

## What you can ask

| Question | What srstack provides |
|---|---|
| “How do charter withdrawals work?” | Branch retirement, credit release, fees and unresolved mechanics |
| “What are the current issuance rate and buy/sell taxes?” | Fresh block-scoped protocol observations, not stored launch values |
| “How much supply was permanently removed, and why?” | Separate liquid-token burns from retired ledger value; totals do not attribute individual burn causes |
| “Are launch holding limits or the Pool Manager gate active?” | Fresh enabled/active flags and cap values; not a guarantee that a transaction will succeed |
| “Are expansion licenses available at a usable price?” | Fresh auction status and inventory; no purchasable quote when unavailable |
| “How did past license or charter auctions go?” | [Supported bounded history scans](references/auction-history.md), with an optional auction-day filter, quantity-weighted prices, evidenced timing and explicit coverage gaps; no stored auction results |
| “What are the current treasury shares and team liability?” | Current/queued FeeSplitter state and vault controls, not holder yield |
| “What does the vault hold of this public reserve asset?” | Approval-gated raw holdings/pool metadata for that asset, not portfolio enumeration |
| “How much did buybacks spend and burn in this block window?” | Checked `BuybackExecuted` event totals with explicit coverage, not aggregate burn attribution or transfer reconciliation |
| “Show the branches and pending balance of this public charter.” | A charter-ID-specific snapshot; no wallet connection or claim that you own it |
| “What is STANDARD trading at, or what is this amount worth?” | Latest reported canonical-pool USD/ETH prices and a gross indicative valuation |
| “Which contracts are listed, and is their source verified?” | Publisher-listed identities and explorer links; verification status requires a fresh explorer check |
| “What has the team announced?” | Fresh official-post research where the host can retrieve it; no bundled recap |
| “What does the Second Mandate mean, and are its market positions real?” | Source-linked manifesto explanation; sample illustrations are not observed positions, revenue or yield offers |

One skill, useful starting routes:

- **Research:** source-linked explanations, documented parameters and evidence gaps.
- **Inspect:** on-demand protocol, auction and public-charter snapshots, bounded auction history, prices and supplemental evidence. No wallet signing or transaction submission.
- **Analyse:** conditional accrual/time-to-target estimates, auction/fee models, forecasts, comparisons and plans with explicit inputs and assumptions.
- **Workflows:** requested reports, local/private-data analysis, exports, caches, monitoring, authenticated research and nonbroadcast simulations using host-permitted capabilities. These examples are not an exhaustive list.

Common questions have [direct inspection paths](references/inspection.md#common-question-paths). Default charter JSON contains only charter facts and its supported rate equivalent; explicitly select `--detail full` when combined charter, burn or launch-restriction context is requested at one block. Explanation-only questions go straight to packaged sources without an RPC call or financial questionnaire. STANDARD amounts do not trigger a price lookup unless monetary valuation is requested.

Research topics: [protocol](references/protocol.md) · [charters](references/charters.md) · [reserves](references/reserves.md) · [contracts](references/contracts.md) · [updates](references/updates.md) · [documents](references/documents.md) · [risks](references/risks.md).

These are routing instructions within one skill, not separately installed commands. `Use srstack` returns the two-route menu. `/srstack` works where the host registers an installed skill command; other command syntax varies by host.

## Requirements

| Capability | Host requirements | Network access |
|---|---|---|
| Explain packaged rules | Read the skill and its selected resources | None |
| Research announcements or explorer status | Permitted public web retrieval | Relevant official pages or explorer |
| Inspect current state | Trusted package and permitted Python 3.10+ execution | Fixed public Robinhood Chain RPC |
| Inspect auction history | Trusted package and permitted Python 3.10+ execution; bounded block scope | Fixed public Robinhood Chain RPC |
| Read market price or gross balance value | Trusted package and permitted Python 3.10+ execution | Fixed public DEX Screener/GeckoTerminal pool endpoints; charter balances additionally use RPC |

All four fixed entrypoints—`snapshot.py`, `price.py`, `history.py` and `verify.py`—use only Python's standard library: no pip dependencies, wallet connector or provider credentials. They require the filesystem protections described in [execution](references/execution.md); unsupported hosts fail closed for those helpers. Other host-permitted tools may provide the requested capability. Dependency installation and reviewed maintenance require the ordinary approval flow, not permission bypass; missing capability means identify the prerequisite, not invent results.

## Install a reviewed release

Package version `0.2.2` is not a revision pin; the **full source commit SHA** resolved below identifies the exact candidate you review and install. These dogfood commands select `feature/v0.2.2`; the `v0.2.2` release tag is not yet available. Compare the resolved SHA with the full commit supplied in the dogfood handoff. Installation prints that SHA and retains it outside the hashed runtime; never embed the package's own commit in hashed files.

These are deliberate maintenance commands for a user or an agent explicitly asked to install/update the skill, subject to normal host approval—not authorization for unsolicited self-updates or guard bypass. Use Git and Python 3.10+ on a supported POSIX host. Review the selected commit, including `maintenance/package.py`, [SKILL.md](SKILL.md), the runtime scripts and [safety](references/safety.md), **before executing package code**. The bundled verifier checks integrity, not publisher authenticity; running it is already executing the package.

### 1. Select paths and pin the candidate commit

Installing while Telegram/Hermes or another host is running is supported; a running host is not installation failure. Stop other installers and coordinate a pause in srstack invocations for replacement and final verification. Stopping the host, if convenient, is only an optional precaution. In one shell, select its **actual configured skill root** and an existing stable working directory outside it. Use absolute paths. Hermes' default is `$HOME/.hermes/skills`; OpenClaw commonly uses the intended workspace's `skills` directory. Named profiles may differ. For dogfooding, prefer an isolated profile/workspace.

Set `SRSTACK_BACKUPS` outside **every** skill-discovery root, on the same filesystem as `SKILL_PARENT`. It will retain the review clone, staging and any previous installation. Do not use another discovered skill directory as a backup, or leave a shadowing same-name installation in another root. Keep customizations for review; do not merge them into the reviewed runtime.

```sh
# Select these paths for your host before continuing:
SKILL_PARENT="$HOME/.hermes/skills"
SRSTACK_BACKUPS="$HOME/srstack-backups"

cd "$HOME" &&
mkdir -p "$SKILL_PARENT" "$SRSTACK_BACKUPS" &&
WORK="$(mktemp -d "$SRSTACK_BACKUPS/srstack-release.XXXXXXXX")" &&
REVIEW_ROOT="$WORK/source" &&
git clone --single-branch --branch feature/v0.2.2 \
  https://github.com/tomismeta/srstack.git "$REVIEW_ROOT" &&
git -C "$REVIEW_ROOT" fetch origin refs/heads/feature/v0.2.2 &&
REVIEWED_COMMIT="$(git -C "$REVIEW_ROOT" rev-parse --verify 'FETCH_HEAD^{commit}')" &&
git -C "$REVIEW_ROOT" checkout --detach "$REVIEWED_COMMIT" &&
printf '%s\n' "$REVIEWED_COMMIT" > "$WORK/reviewed-commit.txt" &&
printf 'Review source: %s\nFull source commit: %s\nRecovery directory: %s\n' \
  "$REVIEW_ROOT" "$REVIEWED_COMMIT" "$WORK"
```

Stop on any error. Review this detached revision before the next step; do not fetch again and silently change the pin. The clone is the **repository**, not an installable runtime. It contains maintenance tools and tests that must not enter the host's discovered skill. Do not run unreviewed local modifications to the exporter.

### 2. Export the reviewed runtime

Continue in the same shell, only after review and any required execution approval:

```sh
python3 -B -I "${REVIEW_ROOT:?Complete the review checkout first}/maintenance/package.py" export \
  --commit "${REVIEWED_COMMIT:?Resolve and review the full commit first}" \
  --destination "${WORK:?Select the recovery directory first}/staged-runtime"
```

`staged-runtime` must **not exist**; its parent already exists. The exporter checks that the full commit equals checkout `HEAD`, reads committed bytes rather than working-tree runtime edits, and verifies runtime membership, hashes and aggregate digest before creating the export. It excludes `.git`, `maintenance`, tests, `.github`, `dist` and caches. A failed export must be resolved before proceeding.

### 3. Clean-replace, verify and retain rollback

The following small replacement step verifies staging before touching the old installation, then moves whole directories—never overlays files. **Pause srstack invocations across the two directory moves and final verification.** Each rename is a whole-root move, but the pair is not atomic: the target is briefly absent between them. The host may remain running. The script checks separation from the selected root; you must also ensure the recovery directory is outside any **other** configured discovery root. Run from the stable directory selected above, not from the installation being moved.

```sh
python3 -B -I - "${SKILL_PARENT:?Select the actual host root}" "${WORK:?Export first}" <<'PY'
import subprocess
import sys
from pathlib import Path

parent = Path(sys.argv[1]).resolve(strict=True)
work = Path(sys.argv[2]).resolve(strict=True)
if parent == work or parent in work.parents or work in parent.parents:
    raise SystemExit("Skill and recovery directories must be separate")
if parent.stat().st_dev != work.stat().st_dev:
    raise SystemExit("Recovery directory must be on the skill root's filesystem")
staged, target, old = work / "staged-runtime", parent / "srstack", work / "previous-install"
failed = work / "failed-install"
if old.exists() or old.is_symlink() or failed.exists() or failed.is_symlink():
    raise SystemExit("Recovery paths already exist; do not overwrite a previous attempt")
if target.is_symlink() or (target.exists() and not target.is_dir()):
    raise SystemExit("Refusing a symlink or non-directory installation")
if staged.is_symlink() or not staged.is_dir():
    raise SystemExit("Expected a complete staged runtime directory")
reviewed_commit = (work / "reviewed-commit.txt").read_text(encoding="ascii").strip()
if len(reviewed_commit) != 40 or any(c not in "0123456789abcdef" for c in reviewed_commit):
    raise SystemExit("Expected the full reviewed commit SHA in the external recovery record")

def verify(root):
    subprocess.run([sys.executable, "-B", "-I", str(root / "scripts/verify.py")],
                   cwd=root, check=True, timeout=30)

print("Recovery directory:", work, flush=True)
verify(staged)
moved_old = installed_new = False
try:
    if target.exists():
        target.rename(old)
        moved_old = True
    staged.rename(target)
    installed_new = True
    verify(target)
except BaseException:
    if installed_new:
        target.rename(failed)
    if moved_old:
        old.rename(target)
        print("Restored previous installation:", target, file=sys.stderr)
    raise
print("Installed and verified:", target)
print("Full reviewed commit SHA:", reviewed_commit)
print("Keep recovery files and full source pin:", work)
PY
```

No files are deleted. On final verification failure, the new root is retained as `failed-install` and the previous root is restored (or the destination is left absent for a first install). If restoration itself fails, keep srstack invocations paused and recover from the printed directory; never use a missing or inconsistent skill root. Telegram/Hermes need not shut down. Whole-root replacement removes obsolete scenario/fixture files from the active runtime without deleting your backup. Keep it until the loaded path and reviewed runtime behavior are confirmed; never discover it as a second skill. A process interruption or filesystem failure may require manual recovery from those same directories before srstack use resumes.

After success, refresh skill discovery if needed and confirm the loaded path is `SKILL_PARENT/srstack`, package version is `0.2.2`, and the printed full SHA matches `WORK/reviewed-commit.txt`. Resume srstack invocations only against the verified root. **Existing chats retain their loaded context:** start a fresh `/new` in each Telegram/Hermes chat that will use the revision (or the host's equivalent new conversation). Installing in one chat cannot restart or refresh the other chats. Restarting the host is optional, not an acceptance criterion; package version alone cannot identify the exact installed revision.

**Hermes installation:** use the complete-bundle instructions above. URL discovery depends on configured sources; importing raw `SKILL.md` does not necessarily import its references, assets and scripts.

**Host approvals:** trusted skill files and requested public reads do not bypass execution approval. If a one-shot session cannot obtain it, continue in an approval-capable session for the exact helper command rather than trying wrappers, PTYs or `--yolo`. Explicit CLI modes remove the need for stdin but still require normal permission. See [input transport and approvals](references/execution.md#input-transport-and-host-approvals).

Other harnesses can use their Agent Skills loader or explicitly read [SKILL.md](SKILL.md) and selected resources. Resource paths resolve against the loaded skill directory. See [host setup](references/installation.md). Installation and configuration changes require an explicit maintenance request and normal host approval; the skill does not initiate them itself.

### Quick test after installation

In a fresh host conversation, `Use srstack` should show **research / inspect / analyse / workflows**, without unsolicited reads. Packaged explanations should work offline without Python. Ask: “Assume 3,384 STANDARD pending, a fixed 15,179 target and 500 STANDARD/day net accrual: how long to the target?” Expect the 11,795 gap and a conditional 23.59-day estimate, not a forecasting refusal or a claim about actual future rates. Ask the [Second Mandate questions](#second-mandate-research): samples must not become holdings, reserve fees must not become holder entitlements, and proposals must not become deployed facts. Requested hypothetical models remain allowed. Signing/submitting must be declined without invoking a wallet.

From the reviewed, verified **installed root**, the default diagnostic is offline integrity verification. There is no `--offline` flag:

```sh
cd "${SKILL_PARENT:?Select the installed host root}/srstack" &&
python3 -B -I scripts/verify.py
```

Only if live access is intended and permitted, select a diagnostic:

```sh
python3 -B -I scripts/verify.py --price
python3 -B -I scripts/verify.py --charter 1 --price
```

Replace example ID `1` with the intended public charter ID. These diagnostics report **stage status and timing, not a price or monetary valuation**. They verify the entire package before running selected helpers; bare verification starts no child and makes no network request. Exit 0 means all selected stages are `ok`; partial, failed or skipped live stages exit 5. See [diagnostic statuses and exits](references/execution.md#package-and-smoke-diagnostic).

For actual live results, ask “Use srstack inspect protocol” or “Use srstack inspect charter 1”: expect a fresh block-scoped snapshot or a precise unavailable/partial result. For a charter's gross USD value, use its successful snapshot's `charter_pending` quantity unchanged with `scripts/price.py --amount-standard DECIMAL`, not the verifier's status. The [snapshot commands](#live-protocol-auction-and-charter-reads) and [price commands](#current-price-and-gross-accrued-balance-value) below exercise the real output paths. Offline operation never waives host execution approval.

Stage elapsed times measure local verification/helper execution, not host startup, model reasoning, discovery, tool-approval waits or answer rendering. Live network latency varies; no end-to-end runtime is promised. A successful local smoke does not certify host approvals, isolation, authenticity or financial correctness.

A live HTTP 401/403 identifies denial of that original request at its endpoint, not global chain/provider unavailability or failed installation. Preserve the helper's bounded original-response diagnostics. Do not evade that endpoint's access controls or a host denial. Independent public RPCs, explorers or APIs may supply fresh evidence under their own access rules; identify the new source and re-establish chain, block, interface and coverage as relevant. This is separate research, not an automatic helper fallback or proof that the original request succeeded. See [safety](references/safety.md#public-retrieval-and-calls).

## Examples

### Conversation starters

```text
Use srstack.
```

Expected: the research/inspect/analyse/workflows menu, without fetching live data.

```text
Use srstack to explain charter withdrawals.
Use only the packaged references and cite the source links.
```

Expected: a sourced explanation, including fees and evidence gaps.

### Second Mandate research

```text
Use srstack to explain the Second Mandate using packaged sources.
Are the manifesto's market positions actual holdings or sample illustrations?
Does the announced fee reinvestment establish revenue rights for charter holders?
```

Expected: distinguish announced strategy from deployed mechanics, identify sample positions, and explain that reserve-level fee reinvestment does not establish holder entitlements. If asked to model future returns or proposal effects, use labelled assumptions and formulas rather than treating samples as actual holdings or declining numerical analysis.

### Live protocol, auction and charter reads

```text
Use srstack inspect protocol. Show current issuance and buy/sell taxes.
Use srstack inspect protocol. Split permanent supply removal into token burns and retired ledger value, and show launch restrictions.
Use srstack inspect auctions. Are licenses available, and what price is actually usable?
Use srstack inspect charter <public charter ID>. Show its branches and pending balance.
```

The reader checks the chain, block, code, module bindings and scalar decoding. Sold-out or disabled auctions do not produce purchasable quotes. A specific charter request also needs its public charter ID; it never needs a wallet connection.

Replace `<public charter ID>` with the ID to inspect.

| View | Selected observations |
|---|---|
| `protocol` | Issuance and epoch context, branch count, supply and permanent-burn decomposition, token restriction/launch flags, counter-based remaining budget, buy/sell tax and pool/emissions state |
| `auctions` | License and daily-charter activation, pause state, inventory, duration and available current prices |
| `treasury` | Current/queued fee allocation, team ETH liability, vault authority/pause, buyback controls; optional approved-asset raw holdings and pool key |
| `charter` | Default: public owner, branches, pending and supported current-rate equivalent. Explicit `--detail full`: additional protocol context and raw evidence |

Each invocation uses one checked block. Separate example invocations are not one atomic combined snapshot; do not combine their values as if they share a block. Failed fields remain missing with errors; fatal failures return no snapshot. Results are not saved or reused as a fallback. These are selected publisher-ABI reads, not a complete contract audit.

Advanced users can request the same protocol snapshot from the reviewed installed root:

```sh
python3 -B -I scripts/snapshot.py protocol
python3 -B -I scripts/snapshot.py auctions --detail full
python3 -B -I scripts/snapshot.py charter --id 1
python3 -B -I scripts/snapshot.py treasury
```

The charter command requires an unsigned uint256 ID; replace `1` with the intended public ID. **Summary is compact in the helper's JSON output**, not just agent-side formatting; `--detail full` opts into raw evidence. No-argument JSON stdin is equally supported, for example `{"schema_version":1,"view":"charter","charter_id":1}`. Default answers show useful values first, with at most one short note such as **“RPC snapshot; publisher ABI.”**

### Bounded auction history

Prefer the supported `history.py` helper for license or charter event history when it covers the question; supplemental read-only RPC tools or locally authored request code are also permitted. For the helper, select `license` or `charter`, optionally filter by `--day N`, and choose either an anchored lookback (`--anchor-block B --lookback-blocks N`, with the anchor defaulting to a fresh head) or an explicit `--from-block A --to-block B` range. `--chunk-blocks N` and `--max-chunks N` bound scanning; defaults, hard limits and evidence semantics live in the [auction-history contract](references/auction-history.md). Supplemental scans must likewise bound resources and establish coverage.

```sh
python3 -B -I scripts/history.py license --lookback-blocks 1000000
python3 -B -I scripts/history.py charter --day 1 --from-block 1 --to-block 1000000
```

Choose the day and block scope for the question; the examples do not assert where a round occurred. An auction day is a filter, not a 24-hour block estimate. Report scanned coverage and partial results, not complete-all-history. A last observed purchase alone does not prove sellout. Results go to stdout and are never saved as runtime observations.

For buybacks use `python3 -B -I scripts/history.py buybacks --lookback-blocks 1000000`. There is no auction-day filter. ETH spent and STANDARD burned are event-accounted within checked coverage, not reconciled transfers or complete-all-history. Treasury optionally accepts `--asset ADDRESS` only as a fixed vault-call argument; approval false/unavailable omits holdings and pool details. Token holdings and internal streamed counters with unestablished decimals remain raw units; queued policy is never substituted for current settings.

### Current price and gross accrued-balance value

```text
Use srstack inspect price. Show STANDARD in USD and ETH.
What is 1000 STANDARD worth at the latest reported market price?
What is the accrued balance of public charter <public charter ID> worth in USD now?
Use srstack inspect price. Cross-check DEX Screener against GeckoTerminal.
Use GeckoTerminal for the current STANDARD price.
```

Current-value questions use the shared price reader automatically; there is no prerequisite `inspect price` step. A charter USD question needs **one charter snapshot and one price-helper invocation**, not an extra protocol snapshot or default cross-check. Pass the successful `charter_pending` quantity unchanged to `scripts/price.py --amount-standard DECIMAL`; report its `valuation.gross_usd`, or that USD is unavailable. Ask only for a missing public ID, not a wallet. This is a gross market mark of a STANDARD-denominated ledger balance—not wallet tokens, net withdrawal proceeds or a branch/NFT resale price. It does not value future earning capacity.

By default, the reader queries DEX Screener for the exact canonical ETH/STANDARD pool. If that source is unavailable, it can use GeckoTerminal and explicitly label the fallback and reason. Identity/schema violations and host/provider access denials do not trigger fallback. A valid partial response stays with its provider rather than filling a missing currency from another source. Chain, token, quote asset and pool identity are checked for both providers; any amount valuation is local and never sent to them.

An explicit provider choice disables automatic fallback. A requested cross-check fetches the other fixed provider and reports its separate prices, evidence and percentage differences; it does not average prices, pick the higher value or change the selected valuation source. Each invocation makes at most two requests. Ordinary price questions do not fetch both providers unnecessarily.

These provider and arithmetic rules describe the bundled helper, not the limits of research. Other sources, market discovery, currencies, cross-source statistics, conditional calculations and user-supplied inputs are permitted with explicit identities, units, times, formulas and assumptions. Public addresses can be inspected without proof of ownership. Private files, authenticated sessions and outputs follow the user's scope and host permissions; see [safety](references/safety.md) and [supplemental reads](references/inspection.md#supplemental-public-reads).

From the reviewed installed root:

```sh
python3 -B -I scripts/price.py --quote
python3 -B -I scripts/price.py --amount-standard 1000
python3 -B -I scripts/price.py --quote --cross-check
python3 -B -I scripts/price.py --source geckoterminal --amount-standard 1000
```

`source` is `auto` (default), `dexscreener` or `geckoterminal`; `cross_check` is an optional boolean, defaulting to false. The optional amount is an unsigned decimal **string**, not a JSON number. Quotes and gross values are decimal strings. Failed fields remain missing, and a labelled fallback never becomes a cached or invented value.

The snapshot and price helpers also accept no-argument JSON stdin; `--help` and the [execution contract](references/execution.md) describe strict input handling. CLI mode does not read stdin or relax approval/integrity checks. Use `--amount-standard` alone for a valuation, not together with `--quote`. Amounts in CLI arguments may appear in process listings or host logs; stdin does not promise transcript privacy.

These are **provider-reported indicative prices**. Neither consumed pool API supplies a quote-observation timestamp: retrieval/cache age is not quote age, and pool creation time is not price freshness. Charter state, the selected price and any cross-check have separate observation boundaries, not one atomic snapshot. Gross values exclude withdrawal fees, trading taxes, LP fees, slippage and gas.

## Contract coverage

The [contract catalog](assets/entities/robinhood.json) contains **14 publisher-listed identities on Robinhood Chain (4663)**. The fixed [publisher read interface](assets/interfaces/robinhood-reads.json) supports selected live getter reads from **nine**:

| Contract | Questions supported by fresh reads |
|---|---|
| **$STANDARD** | What are total supply, ceiling, permanent token burns and retired ledger value? Are launch holding limits and the Pool Manager gate enabled/active? `totalSupply()` is not necessarily circulating supply. |
| **Central Bank** | What are the issuance rate, multiplier, stream rate, branch count and epoch? What budget remains according to the issuance counters? |
| **Charter NFT** | Who owns public charter X? Combined with Central Bank reads, how many branches and pending credits does it have? |
| **Trading Hook** | What are current buy/sell taxes? Is an override or launch schedule active? Is the pool initialized, and is an ownership handoff pending? |
| **Expansion License Auction** | Is it started or paused? How much inventory remains? Is there a usable current price, and what is the auction duration? |
| **Charter Auction** | Are daily charter sales enabled? Is inventory available, and what is the usable ETH price and auction duration? |
| **Fee Splitter** | What are current/queued team and POL shares, team ETH liability, wallet and pending ownership? |
| **Expansion Vault** | Is it paused, who controls it, and is the requested reserve asset approved? If approved, what are its raw holdings and pool key? |
| **Contraction Vault** | What are the timing, configured/effective pool and TWAP limits, configured vault percentage and ETH depth? Bounded history separately accounts for `BuybackExecuted` events. |

The other five have **no direct getter profile**: Founding Sale, Liquidity Manager, Address Registry, Uniswap v4 Pool Manager and Multicall. Registry and Pool Manager identities/code also participate in the treasury authentication graph. Their addresses and explorer links are cataloged; this does not establish complete holdings, permissions or implementation correspondence.

**The catalogs describe bundled coverage, not an inspection allowlist.** Research relevant contracts, networks, sources, interfaces, historical state and events beyond bundled coverage. Prefer fixed helpers where they fit; otherwise use [supplemental tools](references/inspection.md#supplemental-public-reads) or inspectable locally authored code under normal host permissions. Independently authenticate observations and label simulation/assumption boundaries. No catalog edit is needed just to investigate. No wallet signing or transaction submission is permitted.

**Publisher-listed addresses and publisher ABIs do not establish source correspondence.** Selected STANDARD and Trading Hook interfaces and accounting/restriction semantics have additional source-review provenance; that review does not verify the other modules or establish current deployment state. The package bundles no contract source and stores no current explorer verdicts. Current verification status requires fresh retrieval. Getter observations do not establish complete administrator powers, upgradeability, audit correspondence or exploit resistance. Source dates identify reference provenance, not live-state freshness.

## Coverage and footprint

The package covers the 16-section whitepaper, contract identities, publisher ABI definitions and the [Second Mandate manifesto](references/updates.md#second-mandate-liquidity-for-tokenized-stocks) as announced strategic direction. It stores no changing-state snapshots, recap metrics or explorer verification verdicts. Current balances, rates, supply, inventory, prices, activation, verification status and latest announcements require fresh retrieval; unavailable data stays unavailable.

For current protocol questions, request only the relevant [inspection](references/inspection.md). Current stream rates, remaining-budget accounting, sale taxes, LP fees and unavailable auctions have different meanings; none establishes future earnings or executable net proceeds.

The package uses selected references and indexed records rather than loading the whole corpus for every question. The reference indexes own current inventory counts; disk size is not per-question token cost, and selective loading depends on the host.

Packaged research needs a resource reader. Bundled readers use **Python 3.10+ and its standard library**, fixed RPC/provider paths and supported filesystem primitives. Other host-permitted tools, reviewed dependencies and custom code can support additional requested workflows without modifying these helpers. No wallet signer, telemetry, scheduler or self-update process is bundled; host capabilities must actually exist before claiming an operation was performed.

## Safety and verification limits

Answers lead with content. Estimates get a short label; observations get a brief source note where needed. Detailed provenance and assumptions are available on request, not repeated as small print.

The four bundled helpers retain their fixed input schemas, identities, decoding, finite budgets and integrity checks; they write no files and make no financial transactions. Their partial results and errors remain honest, not silently repaired. Supplemental analysis, user-authorized artifacts/monitoring, authenticated research, unsigned preparation and nonbroadcast simulations are permitted through appropriate tools. Do not sign wallet messages/transactions, invoke signing prompts or submit/broadcast transactions, including through delegated tools. Host permissions, access controls and secret protection remain binding. See [safety](references/safety.md) and [execution](references/execution.md).

The readers do **not themselves** implement liquidity-depth analysis, amount-specific withdrawal quotes, gas estimation or strategy/settlement models. Use appropriate supplemental tools or explicit calculations for those requests, preserving evidence and assumptions. No result is guaranteed sale proceeds. A helper's missing feature is not a skill-wide prohibition.

Skill instructions do not enforce host isolation, and estimates are not guaranteed returns.

## Repository validation

These commands run from the **repository root**, not the installed skill folder:

```sh
python3 -B maintenance/package.py verify
python3 -B maintenance/check-snapshot.py
python3 -B maintenance/check-price.py
python3 -B maintenance/check-history.py
python3 -B maintenance/check-verify.py
python3 -B maintenance/check-package.py
python3 -B maintenance/package.py archive
```

The checks use Python's standard library and local Git; they do not call explorers, connect wallets or use model/API credentials. CI runs them on Python 3.10 and 3.14, with read-only repository permissions and commit-pinned Actions. GitHub checkout and Python provisioning require network access; the validation commands themselves are offline. CI verifies the committed manifest rather than regenerating it, and checks deterministic ZIP output. It does not upload artifacts, tag, publish releases or monitor contracts.

After deliberate runtime changes, regenerate the manifest with `python3 -B maintenance/package.py build`, then run the checks above. The archive `dist/srstack-0.2.2.zip` contains only the runtime package; building it does not publish a release or certify it. Maintenance tooling and CI files are repository-only; their execution requires a deliberate maintenance request, trusted code and normal host permissions.

## Feedback and license

Report reproducible problems through [GitHub issues](https://github.com/tomismeta/srstack/issues), including the host/version, package commit, actual loaded path and redacted reproduction. Never upload wallet credentials, private RPC URLs or private conversation history.

Original srstack code, summaries and instructions are [MIT-licensed](LICENSE). Third-party documents, posts, media, trademarks and protocol code retain their owners' rights and are excluded from that grant. Source links and quotations do not transfer those rights or imply affiliation.
