# srstack

**Standard Reserve research and live read-only inspection for AI agents.**

srstack explains documented protocol mechanics and announcements, reads current public state and reports indicative prices and gross balance values. It is one independent [Agent Skill](https://agentskills.io/specification), not an official Standard Reserve product, trading bot or wallet toolkit.

**Version 0.2.0 · research and inspect.** Retires the pre-release strategy simulator and its assumption-intake workflow. Includes the Second Mandate's tokenized-stock liquidity vision, intended market funding and fee flows, and explicit boundaries between announced strategy, sample positions and deployed mechanics. Canonical protocol facts and live-reader targets are preserved. This branch is a dogfood candidate, not a published release; prior release audit results do not cover these bytes.

**Breaking changes:** the `plan` route, `scripts/scenario.py`, fictional fixture and verifier `--offline` flag are removed. Use the default `scripts/verify.py` command for offline integrity checks. Future-return and strategy questions receive qualitative research, not a replacement simulator. Install a clean runtime export; do not overlay an older installation containing removed files.

## What you can ask

| Question | What srstack provides |
|---|---|
| “How do charter withdrawals work?” | Branch retirement, credit release, fees and unresolved mechanics |
| “What are the current issuance rate and buy/sell taxes?” | Fresh block-scoped protocol observations, not stored launch values |
| “How much supply was permanently removed, and why?” | Separate liquid-token burns from retired ledger value; totals do not attribute individual burn causes |
| “Are launch holding limits or the Pool Manager gate active?” | Fresh enabled/active flags and cap values; not a guarantee that a transaction will succeed |
| “Are expansion licenses available at a usable price?” | Fresh auction status and inventory; no purchasable quote when unavailable |
| “Show the branches and pending balance of this public charter.” | A charter-ID-specific snapshot; no wallet connection or claim that you own it |
| “What is STANDARD trading at, or what is this amount worth?” | Latest reported canonical-pool USD/ETH prices and a gross indicative valuation |
| “Which contracts are listed, and is their source verified?” | Publisher-listed identities and explorer links; verification status requires a fresh explorer check |
| “What has the team announced?” | Fresh official-post research where the host can retrieve it; no bundled recap |
| “What does the Second Mandate mean, and are its market positions real?” | Source-linked manifesto explanation; sample illustrations are not observed positions, revenue or yield offers |

One skill, two routes:

- **Research:** source-linked explanations, documented parameters and evidence gaps.
- **Inspect:** on-demand protocol, auction and public-charter snapshots through the fixed RPC helper, plus a separate canonical-pool price reader for current price and gross balance-value questions. No wallet access.

Common questions have [direct inspection paths](references/inspection.md#common-question-paths): a charter snapshot already includes burn and launch-restriction context, so combined questions need no duplicate protocol read. Explanation-only questions go straight to relevant packaged sources without an RPC call or financial questionnaire. STANDARD amounts do not trigger a market-price lookup unless a monetary valuation is requested.

Research topics: [protocol](references/protocol.md) · [charters](references/charters.md) · [reserves](references/reserves.md) · [contracts](references/contracts.md) · [updates](references/updates.md) · [documents](references/documents.md) · [risks](references/risks.md).

These are routing instructions within one skill, not separately installed commands. `Use srstack` returns the two-route menu. `/srstack` works where the host registers an installed skill command; other command syntax varies by host.

## Requirements

| Capability | Host requirements | Network access |
|---|---|---|
| Explain packaged rules | Read the skill and its selected resources | None |
| Research announcements or explorer status | Permitted public web retrieval | Relevant official pages or explorer |
| Inspect current state | Trusted package and permitted Python 3.10+ execution | Fixed public Robinhood Chain RPC |
| Read market price or gross balance value | Trusted package and permitted Python 3.10+ execution | Fixed public DEX Screener/GeckoTerminal pool endpoints; charter balances additionally use RPC |

All three fixed entrypoints use only Python's standard library: no pip dependencies, wallet connector or provider credentials. Execution also requires the filesystem protections described in [execution](references/execution.md); unsupported hosts fail closed. Missing execution or retrieval capability produces an explanation, not invented results. The skill does not install dependencies or change host permissions.

## Quick start

For the published release, use the attached **`srstack-0.1.3.zip`** and **`SHA256SUMS`** from [srstack v0.1.3](https://github.com/tomismeta/srstack/releases/tag/v0.1.3), not a moving branch. The pinned installation below installs **0.1.3**, not this **0.2.0 candidate**. For dogfooding, use a complete candidate runtime ZIP or local runtime export in an isolated host profile; never install the full repository.

**Install a runtime export or attached runtime ZIP—not a full repository, GitHub's automatic “Source code” archive or an audit archive.** Audit evidence is not an installable skill or a smart-contract security certification.

### Normal pinned-release install

These are **user/maintainer installation commands**, not permission for an installed agent to download code, install itself or bypass host guards. Review the pinned release, [SKILL.md](SKILL.md) and [safety](references/safety.md) first. A checksum downloaded beside a ZIP detects disagreement, not a compromised publisher; trust comes from your review/pin and trusted outer ZIP checksum. Running the bundled verifier is already executing that package, so self-verification cannot bootstrap trust.

Use Python 3.10+ on a supported POSIX host. Stop the host/other installers while replacing its skill. Choose **one** root explicitly:

```sh
# Hermes default profile:
SKILL_PARENT="$HOME/.hermes/skills"
# OR OpenClaw: run this instead from the intended workspace:
# SKILL_PARENT="$PWD/skills"
```

For named profiles, use their actual configured root. Choose a backup/staging directory **outside every skill-discovery root**, on the same filesystem as `SKILL_PARENT`. Keep local customizations there; never merge them silently into the new release. The unique backup below is never overwritten. Move the shell to a stable directory before installation:

```sh
SRSTACK_BACKUPS="$HOME/srstack-backups"
cd "$HOME" && python3 -B -I - "${SKILL_PARENT:?Choose a skill root first}" "$SRSTACK_BACKUPS" <<'PY'
import hashlib, re, stat, subprocess, sys, tempfile, urllib.request, zipfile
from pathlib import Path

parent = Path(sys.argv[1]).resolve()
backups = Path(sys.argv[2]).resolve()
if parent == backups or parent in backups.parents or backups in parent.parents:
    raise SystemExit("Skill and backup roots must be separate")
parent.mkdir(parents=True, exist_ok=True)
backups.mkdir(parents=True, exist_ok=True)
if parent.stat().st_dev != backups.stat().st_dev:
    raise SystemExit("Choose a backup directory on the skill root's filesystem")
work = Path(tempfile.mkdtemp(prefix="srstack-0.1.3-", dir=backups))
print("Retained staging/backup directory:", work, flush=True)
base = "https://github.com/tomismeta/srstack/releases/download/v0.1.3/"
archive = "srstack-0.1.3.zip"
for name, limit in ((archive, 16 * 1024 * 1024), ("SHA256SUMS", 65536)):
    with urllib.request.urlopen(base + name, timeout=30) as response:
        data = response.read(limit + 1)
    if len(data) > limit:
        raise SystemExit("Release download exceeds bound")
    (work / name).write_bytes(data)
entries = re.findall(r"^([0-9a-fA-F]{64}) [ *]" + re.escape(archive) + r"$",
                     (work / "SHA256SUMS").read_text(), re.MULTILINE)
if len(entries) != 1 or hashlib.sha256((work / archive).read_bytes()).hexdigest() != entries[0].lower():
    raise SystemExit("Runtime ZIP checksum missing, duplicated or mismatched")
with zipfile.ZipFile(work / archive) as bundle:
    members = bundle.infolist()
    if len(members) > 1024 or sum(m.file_size for m in members) > 16 * 1024 * 1024:
        raise SystemExit("Archive exceeds extraction bounds")
    seen = set()
    for m in members:
        parts = m.filename.split("/")
        if (m.filename in seen or len(parts) < 2 or parts[0] != "srstack"
                or any(p in ("", ".", "..") for p in parts) or "\\" in m.filename
                or stat.S_IFMT(m.external_attr >> 16) != stat.S_IFREG):
            raise SystemExit("Archive contains unsafe or unexpected members")
        seen.add(m.filename)
    bundle.extractall(work)  # Only checked regular files under the fresh srstack/ root.
staged, target, old = work / "srstack", parent / "srstack", work / "previous-install"
def verify(root):
    subprocess.run([sys.executable, "-B", "-I", str(root / "scripts/verify.py")],
                   cwd=root, check=True, timeout=30)
verify(staged)  # Entire membership + hashes, before touching the old installation.
if target.is_symlink() or (target.exists() and not target.is_dir()):
    raise SystemExit("Refusing a symlink or non-directory installation")
moved_old = installed_new = False
try:
    if target.exists():
        target.rename(old)
        moved_old = True
    staged.rename(target)  # Whole root; no overlay.
    installed_new = True
    verify(target)
except BaseException:
    if installed_new:
        target.rename(work / "failed-install")
    if moved_old:
        old.rename(target)
        print("Restored previous installation:", target, file=sys.stderr)
    print("Installation failed; retained recovery files:", work, file=sys.stderr)
    raise
print("Installed and verified:", target)
print("Previous installation (if any) and downloads retained:", work)
PY
```

This checks **only the exact runtime ZIP entry** in `SHA256SUMS`; it does not require the separate audit ZIP. Unsafe archive members, extra/missing runtime files or mismatched hashes stop installation. No files are deleted. If final verification fails, the new root is retained as `failed-install` and the old root is restored; if restoration itself errors, stop and recover from the printed directory before restarting discovery. Keep that backup until you have reviewed any customizations and confirmed the actual loaded path/version in a fresh host conversation. Do not install the backup as a second discoverable skill.

### Reviewed-commit export or isolated review install

The export machine needs Git and Python 3.10+. The installed host needs only the capabilities for the routes you use.

1. Review [SKILL.md](SKILL.md), the [safety boundary](references/safety.md) and the complete package. Select a full immutable commit SHA you trust and have reviewed, not the moving `main` branch.
2. From a stable working directory outside skill-discovery roots, clone a review copy and select that revision:

   ```sh
   REVIEWED_COMMIT=REVIEWED_COMMIT_SHA
   REVIEW_ROOT="$PWD/srstack-review"
   git clone https://github.com/tomismeta/srstack.git "$REVIEW_ROOT" &&
   git -C "$REVIEW_ROOT" checkout --detach "$REVIEWED_COMMIT"
   ```

   Replace `REVIEWED_COMMIT_SHA` with the full 40-character commit SHA you reviewed; it is a placeholder, not a release identifier. Stop on any error. The export command below independently checks that the selected commit matches the checkout, so a failed checkout cannot silently install the default branch.

3. Choose **one** installation parent. For an isolated review, use the test profile/workspace's skill root instead of your active root. For Hermes' default profile:

   ```sh
   SKILL_PARENT="$HOME/.hermes/skills"
   ```

   Or, for OpenClaw, run this from the intended workspace:

   ```sh
   SKILL_PARENT="$PWD/skills"
   ```

   Named profiles and managed installations may use different roots; use the intended host's configured location. Export the reviewed commit's manifest-listed runtime files into a new skill folder:

   ```sh
   mkdir -p "$SKILL_PARENT" &&
   python3 -B "$REVIEW_ROOT/maintenance/package.py" export \
     --commit "$REVIEWED_COMMIT" \
     --destination "$SKILL_PARENT/srstack"
   ```

   The destination must not already exist. Export validates the selected commit's runtime membership, per-file hashes and aggregate digest before creating it. It reads committed content, not uncommitted runtime edits, and excludes Git metadata, maintenance tools, tests, CI configuration and local build/cache artifacts. Failed exports clean up the new destination. Review the helper itself as part of the selected commit; do not run unreviewed local modifications.

   For updates, first export into a fresh staging directory outside discovery roots and run its `scripts/verify.py` before touching the active installation. Preserve the entire old installation in a unique backup outside all discovery roots, then move the complete verified root into the absent destination and verify it again. Restore the backup if final verification fails. Do not overlay files, use `cp -a` on the repository or leave a shadowing same-name copy. Keep the review clone outside discovery roots; start or refresh the host only after installation succeeds.

   Before removing an old installation or temporary checkout, move your shell/tool working directory outside that tree to an existing stable directory. A deleted cwd can break later host commands even when the installation is correct.

4. From the installed root, run `python3 -B -I scripts/verify.py` for complete runtime membership, per-file hashes and aggregate digest verification. Confirm the actual loaded path and revision, and that repository-only `.git`, `maintenance`, `.github` and `dist` directories are absent. A matching self-supplied manifest does not establish trust in an unreviewed package.
5. Start a fresh conversation and try a packaged-knowledge question from the examples below.

**Hermes installation:** use the complete-bundle instructions above. URL discovery depends on configured sources; importing raw `SKILL.md` does not necessarily import its references, assets and scripts.

**Host approvals:** trusted skill files and requested public reads do not bypass execution approval. If a one-shot session cannot obtain it, continue in an approval-capable session for the exact helper command rather than trying wrappers, PTYs or `--yolo`. Explicit CLI modes remove the need for stdin but still require normal permission. See [input transport and approvals](references/execution.md#input-transport-and-host-approvals).

Other harnesses can use their Agent Skills loader or explicitly read [SKILL.md](SKILL.md) and selected resources. Resource paths resolve against the loaded skill directory. See [host setup](references/installation.md); this package never installs itself or changes host permissions.

### Quick test after installation

In a fresh host conversation, `Use srstack` should show **research / inspect**, with no live read. “Explain charter withdrawals using only packaged references” should work offline without Python. “Offline” means no live retrieval, not that host execution approval is waived.

For live post-install checks, ask “Use srstack inspect protocol” or “Use srstack inspect charter 1” (replace `1` with your intended public ID). Expect a block-anchored snapshot, or a precise unavailable/partial result—not stored values. [Direct snapshot commands](#live-protocol-auction-and-charter-reads) and [price commands](#current-price-and-gross-accrued-balance-value) exercise these paths without model routing; do not run live checks unless intended and permitted.

From the reviewed, verified installed root, choose only the diagnostics you intend:

```sh
python3 -B -I scripts/verify.py                 # Membership and hashes only; no child/network.
python3 -B -I scripts/verify.py --price         # Explicit live indicative quote.
python3 -B -I scripts/verify.py --charter 1 --price  # One live charter + gross balance mark.
```

Replace example ID `1` with the public charter ID you intend to read. `--charter` and `--price` may combine. A bare diagnostic never silently fetches live data. Every smoke first checks the entire manifest/membership and blocks child execution on failure. Output is compact stage status/timing, not financial results; use the helpers below for results. Exit 0 means all selected stages are `ok`; partial, failed or skipped smoke stages exit 5. See [diagnostic statuses and exits](references/execution.md#package-and-smoke-diagnostic).

Stage elapsed times measure local verification/helper execution, not host startup, model reasoning, discovery, tool-approval waits or answer rendering. Live network latency varies; no end-to-end runtime is promised. A successful local smoke does not certify host approvals, isolation, authenticity or financial correctness.

## Examples

### Conversation starters

```text
Use srstack.
```

Expected: the research/inspect menu, without fetching live data.

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

Expected: distinguish announced liquidity strategy from deployed mechanics, identify the explicitly sample panel and explain that reserve-level fee reinvestment does not establish holder revenue entitlements. Requests for future returns get a qualitative explanation of mechanics, risks and missing evidence—not projected cash flows.

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
| `charter` | Public owner, branch count, pending balance and related issuance, supply and restriction context |

Each invocation uses one checked block. Separate example invocations are not one atomic combined snapshot; do not combine their values as if they share a block. Failed fields remain missing with errors; fatal failures return no snapshot. Results are not saved or reused as a fallback. These are selected publisher-ABI reads, not a complete contract audit.

Advanced users can request the same protocol snapshot from the reviewed installed root:

```sh
python3 -B -I scripts/snapshot.py protocol
python3 -B -I scripts/snapshot.py auctions --detail full
python3 -B -I scripts/snapshot.py charter --id 1
```

The charter command requires an unsigned uint256 ID; replace `1` with the intended public ID. `--detail full` adds raw evidence; summary is the default. No-argument JSON stdin is equally supported, for example `{"schema_version":1,"view":"charter","charter_id":1}`. Default answers show useful values first, with at most one short note such as **“RPC snapshot; publisher ABI.”**

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

From the reviewed installed root:

```sh
python3 -B -I scripts/price.py --quote
python3 -B -I scripts/price.py --amount-standard 1000
python3 -B -I scripts/price.py --quote --cross-check
python3 -B -I scripts/price.py --source geckoterminal --amount-standard 1000
```

`source` is `auto` (default), `dexscreener` or `geckoterminal`; `cross_check` is an optional boolean, defaulting to false. The optional amount is an unsigned decimal **string**, not a JSON number. Quotes and gross values are decimal strings. Failed fields remain missing, and a labelled fallback never becomes a cached or invented value.

Both data helpers retain no-argument JSON stdin; `--help` documents both interfaces. Any non-help CLI arguments select explicit CLI mode and never read or merge stdin. Use exact separate flag/value tokens, not `--flag=value`; snapshot's view comes first. Unknown, repeated, abbreviated or conflicting options are rejected before network access. `--quote` conflicts with `--amount-standard`; use the latter alone for gross valuation. Amount arguments can appear in process listings or host logs; stdin remains available, without promising transcript privacy. CLI conveniences use the same validators/readers and do not relax approval or integrity checks.

These are **provider-reported indicative prices**. Neither consumed pool API supplies a quote-observation timestamp: retrieval/cache age is not quote age, and pool creation time is not price freshness. Charter state, the selected price and any cross-check have separate observation boundaries, not one atomic snapshot. Gross values exclude withdrawal fees, trading taxes, LP fees, slippage and gas.

## Contract coverage

The [contract catalog](assets/entities/robinhood.json) contains **14 publisher-listed identities on Robinhood Chain (4663)**. The fixed [publisher read interface](assets/interfaces/robinhood-reads.json) supports selected live reads from **six**:

| Contract | Questions supported by fresh reads |
|---|---|
| **$STANDARD** | What are total supply, ceiling, permanent token burns and retired ledger value? Are launch holding limits and the Pool Manager gate enabled/active? `totalSupply()` is not necessarily circulating supply. |
| **Central Bank** | What are the issuance rate, multiplier, stream rate, branch count and epoch? What budget remains according to the issuance counters? |
| **Charter NFT** | Who owns public charter X? Combined with Central Bank reads, how many branches and pending credits does it have? |
| **Trading Hook** | What are current buy/sell taxes? Is an override or launch schedule active? Is the pool initialized, and is an ownership handoff pending? |
| **Expansion License Auction** | Is it started or paused? How much inventory remains? Is there a usable current price, and what is the auction duration? |
| **Charter Auction** | Are daily charter sales enabled? Is inventory available, and what is the usable ETH price and auction duration? |

The other eight have **identity and documented-role coverage, not fixed-helper live-read support**: Founding Sale, Expansion Vault, Contraction Vault, Liquidity Manager, Fee Splitter, Address Registry, Uniswap v4 Pool Manager and Multicall. Their addresses and explorer links are in the catalog; current holdings, permissions and implementation details require separate fresh research.

**Publisher-listed addresses and publisher ABIs do not establish source correspondence.** Selected STANDARD and Trading Hook interfaces and accounting/restriction semantics have additional source-review provenance; that review does not verify the other modules or establish current deployment state. The package bundles no contract source and stores no current explorer verdicts. Current verification status requires fresh retrieval. Getter observations do not establish complete administrator powers, upgradeability, audit correspondence or exploit resistance. Source dates identify reference provenance, not live-state freshness.

## Coverage and footprint

The package covers the 16-section whitepaper, contract identities, publisher ABI definitions and the [Second Mandate manifesto](references/updates.md#second-mandate-liquidity-for-tokenized-stocks) as announced strategic direction. It stores no changing-state snapshots, recap metrics or explorer verification verdicts. Current balances, rates, supply, inventory, prices, activation, verification status and latest announcements require fresh retrieval; unavailable data stays unavailable.

For current protocol questions, request only the relevant [inspection](references/inspection.md). Current stream rates, remaining-budget accounting, sale taxes, LP fees and unavailable auctions have different meanings; none establishes future earnings or executable net proceeds.

The package uses selected references and indexed records rather than loading the whole corpus for every question. The reference indexes own current inventory counts; disk size is not per-question token cost, and selective loading depends on the host.

Packaged research needs a resource reader. Calculations and public readers use **Python 3.10+ and its standard library**, with no pip dependencies. Chain reads use the fixed Robinhood RPC; market prices use only the fixed DEX Screener/GeckoTerminal pool endpoints. No wallet connector, telemetry or self-update process is bundled.

## Safety and verification limits

Answers lead with content. Estimates get a short label; observations get a brief source note where needed. Detailed provenance and assumptions are available on request, not repeated as small print.

The snapshot helper reads two fixed catalogs and permits only its pinned view/pure calls on configured Robinhood addresses. The price helper reads only the fixed identity catalog and makes bounded canonical-pool GETs to two allowlisted providers; optional quantity multiplication is local and uses one selected provider. The third entrypoint, `verify.py`, checks the package and invokes only explicitly selected fixed data helpers with bounded execution/output; it has no network of its own. All three reject unsupported inputs and write no files. No wallets, credentials, signatures, transaction payloads or state-changing simulations. See [safety](references/safety.md) and [execution](references/execution.md) for the full boundary.

The readers do **not** supply liquidity-depth analysis, an amount-specific withdrawal quote, transaction gas estimates or guaranteed sale proceeds. No strategy, future-return or settlement simulator is bundled. Source verification and latest announcements use separate fresh web research.

Skill instructions do not enforce host isolation, and estimates are not guaranteed returns.

## Repository validation

These commands run from the **repository root**, not the installed skill folder:

```sh
python3 -B maintenance/package.py verify
python3 -B maintenance/check-snapshot.py
python3 -B maintenance/check-price.py
python3 -B maintenance/check-verify.py
python3 -B maintenance/check-package.py
python3 -B maintenance/package.py archive
```

The checks use Python's standard library and local Git; they do not call explorers, connect wallets or use model/API credentials. CI runs them on Python 3.10 and 3.14, with read-only repository permissions and commit-pinned Actions. GitHub checkout and Python provisioning require network access; the validation commands themselves are offline. CI verifies the committed manifest rather than regenerating it, and checks deterministic ZIP output. It does not upload artifacts, tag, publish releases or monitor contracts.

After deliberate runtime changes, regenerate the manifest with `python3 -B maintenance/package.py build`, then run the checks above. The candidate archive `dist/srstack-0.2.0.zip` contains only the runtime package; building it does not publish a release or certify it. Maintenance tooling and CI files are repository-only and never authorize an installed skill to execute them.

## Feedback and license

Report reproducible problems through [GitHub issues](https://github.com/tomismeta/srstack/issues), including the host/version, package commit, actual loaded path and redacted reproduction. Never upload wallet credentials, private RPC URLs or private conversation history.

Original srstack code, summaries and instructions are [MIT-licensed](LICENSE). Third-party documents, posts, media, trademarks and protocol code retain their owners' rights and are excluded from that grant. Source links and quotations do not transfer those rights or imply affiliation.
