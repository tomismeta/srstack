# Host installation and capabilities

Install/update only when requested and under normal host approval. Repository maintenance uses Git and Python 3.10+ on a supported POSIX host. Neither is needed to load the skill; Python 3.10+ is needed only if choosing its optional standard-library calculation helpers. Review the exporter, runtime and [safety rules](safety.md) before executing code; integrity verification is not publisher authentication.

**Identity:** `0.3.0` is the unreleased development line. The full reviewed commit identifies the installed package; retain it outside the hashed runtime, never inside its own files. Installation and bug reports need the loaded path and recorded SHA. Ordinary charter/auction answers do not need revision ceremony.

## Reviewed installation

The default below resolves the available `feature/v0.3.0` branch to a detached full commit **before review**. For a supplied pin, set `SRSTACK_COMMIT` to that full 40-hex SHA first; never replace a requested pin with the branch tip. No release tag is assumed.

### 1. Select paths and pin the commit

Select the actual configured skill root and a stable working directory outside it. The host may remain running; coordinate other installers and pause srstack invocations during replacement. Use absolute paths. An isolated profile/workspace is useful for dogfooding, not required.

Set `SRSTACK_BACKUPS` outside **every** skill-discovery root, on the same filesystem as `SKILL_PARENT`. It will retain the review clone, staging and any previous installation. Do not use another discovered skill directory as a backup, or leave a shadowing same-name installation in another root. Keep customizations for review; do not merge them into the reviewed runtime.

```sh
# Select these paths for your host before continuing:
SKILL_PARENT="$HOME/.hermes/skills"
SRSTACK_BACKUPS="$HOME/srstack-backups"

cd "$HOME" &&
mkdir -p "$SKILL_PARENT" "$SRSTACK_BACKUPS" &&
WORK="$(mktemp -d "$SRSTACK_BACKUPS/srstack-release.XXXXXXXX")" &&
REVIEW_ROOT="$WORK/source" &&
git clone --single-branch --branch feature/v0.3.0 \
  https://github.com/tomismeta/srstack.git "$REVIEW_ROOT" &&
REVIEWED_COMMIT="$(git -C "$REVIEW_ROOT" rev-parse --verify --end-of-options "${SRSTACK_COMMIT:-HEAD}^{commit}")" &&
{ test -z "${SRSTACK_COMMIT:-}" || test "$SRSTACK_COMMIT" = "$REVIEWED_COMMIT"; } &&
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

`staged-runtime` must **not exist**; its parent already exists. The exporter checks that the full commit equals checkout `HEAD`, reads committed bytes rather than working-tree runtime edits, and verifies exact runtime membership, hashes and aggregate digest before creating the export. The runtime includes `SKILL.md`, `README.md`, `LICENSE`, `release-manifest.json`, reference documents, the source/parameter corpus, `scripts/calculations.py`, `scripts/research.py` and `assets/schemas/research-evidence-v1.json`. The library, CLI and schema are installed and covered by the manifest; use needs no source checkout. It excludes retired protocol clients, deployment registries, exhaustive ABI catalogs, `.git`, `maintenance`, source-only `research/` tests/fixtures, `.github`, `dist` and caches. A failed export must be resolved before proceeding.

The hashed references include a bounded, dated Markdown [method/event guide](interface-guide.md): question-oriented canonical signatures, argument/return/event layouts, indexed fields, evidenced units, generation applicability and source/review provenance. It is not a complete ABI, current-address router, allowlist or executable client. Its entries are leads for deployment-specific authentication, not evidence that a dated binding or mechanic still applies. Installation bundles optional offline calculation code but does not execute it, install dependencies, provide transport or grant permissions. Host-native tools, other languages and independent calculations remain valid.

### 3. Clean-replace, verify and retain rollback

The following small replacement step verifies staging before touching the old installation, then moves whole directories—never overlays files. Verification runs the reviewed repository's maintenance tool **outside discovery**, comparing the candidate and installed bytes with the reviewed commit; it never executes code from either runtime. **Pause srstack invocations across the two directory moves and final verification.** Each rename is a whole-root move, but the pair is not atomic: the target is briefly absent between them. The host may remain running. The script checks separation from the selected root; you must also ensure the recovery directory is outside any **other** configured discovery root. Run from the stable directory selected above, not from the installation being moved.

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
verifier = work / "source" / "maintenance" / "package.py"

def verify(root):
    subprocess.run([sys.executable, "-B", "-I", str(verifier), "verify",
                    "--root", str(root), "--commit", reviewed_commit],
                   cwd=work, check=True, timeout=30)

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

No files are deleted. Failed verification retains the candidate as `failed-install` and restores the previous root. If interruption or restoration fails, keep skill use paused and recover from the printed directory. Keep backups outside discovery roots until the new installation is confirmed; never merge old customizations into the reviewed runtime.

After success, verify the loaded path and the printed SHA against `WORK/reviewed-commit.txt`, then refresh discovery/reload as described below. Resume invocations only against the verified root.

To recheck installed bytes later, retain the reviewed repository outside discovery and run `python3 -B -I "$REVIEW_ROOT/maintenance/package.py" verify --root "$SKILL_PARENT/srstack" --commit "$REVIEWED_COMMIT"`. The full commit must still equal that checkout's `HEAD`. This checks membership and bytes, not host loading or public-source access.

## Host loading and sessions

- **Hermes:** find the actual profile root (commonly `~/.hermes/skills`). Use `skills_list`/`skill_view` and literal relative resource paths. `/srstack` or a natural question asking to use srstack invokes the selected installation. [Host docs](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills/).
- **OpenClaw:** use the intended workspace's `skills/srstack/` or configured managed root; avoid shadowing duplicates. The reference/corpus files must be available to the host. [Host docs](https://docs.openclaw.ai/tools/skills).
- **Other hosts:** load the complete Agent Skills runtime and selected relative resources, not `SKILL.md` alone. Questions use the host's permitted public-read tools; the installed optional helpers only calculate supplied inputs, without network transport. Explanation-only requests do not require network access.

After replacement, refresh discovery and reload the skill in the main session if the host supports it. Existing loaded context may remain stale: report that limitation rather than claiming reload succeeded. A fresh `/new` is a host-dependent way to load the new revision, not an automatic installation step or a requirement to restart Telegram. One chat cannot refresh all other chats.

Keep the maintainer working directory outside any tree being moved. A missing cwd requires selecting an existing directory, not reinstalling the host. If interruption or rollback fails, pause skill use and recover the complete root from the printed recovery directory.

### Stale host instructions

Only the host maintainer, under an explicit maintenance request, should inspect and correct obsolete workshop/installer instructions that invoke removed srstack helpers or catalogs. Review the actual configured host files and loaded revision first; do not assume installing this package updates external workshops or other chats. This procedure does not perform that cleanup. Never automatically mutate another skill, migrate its configuration or reuse its credentials. Keep any retained old srstack installation outside every discovery root and inaccessible to an isolated acceptance session.

## Capability baseline

Select tools by capability, not host or provider brand. Explanation-only questions need no network. Live numerical and historical release gates need the applicable rows below, under ordinary host authorization; the skill supplies none of these tools.

| Capability | What must be demonstrated for the question |
| --- | --- |
| Public RPC/read transport | Authorized access to the relevant chain and source evidence, with block/time identity; one blocked transport does not establish that all independent public access is unavailable. |
| ABI and Ethereum Keccak-256 | Authenticate and encode/decode the needed methods/events, including indexed fields and dynamic layouts; NIST SHA3 is not Ethereum Keccak. |
| Exact calculation | Preserve raw integers and scales through threshold, rounding, time-window and ledger calculations; format only afterward. |
| Index, logs and receipts | Discover the relevant records with stated finite coverage, verify successful receipts and canonical blocks, and expose omissions; receipt lookup alone is not a complete event index. |
| Historical state, when needed | Demonstrate archive coverage for the requested state anchors; working current state or historical receipts does not prove it. |

Record actual capability and provider coverage independently. A configured key or paid tier proves neither chain support nor adequate history. Missing history can block an earned-only result while basic state reads still succeed.

For live acceptance, record the host's established ordinary authorized access contexts and their limits, not merely that an HTTP client or browser is installed. Supplying a tested transport capability is host setup, not an expected protocol answer; record any coordinator assistance separately from unassisted discovery. Do not probe a known-denied route or invent a browser/header workaround when a permitted path has already been established. Apply the actual denial scope under [safety](safety.md#public-retrieval-and-calls).

## Acceptance and distribution

The [post-install checks](../README.md#quick-test-after-installation) are a smoke check, not release acceptance. The repository-only `maintenance/agent-acceptance.json` defines **mandatory release gates** using natural questions in a fresh isolated session with no prior installation, catalog or stale workshop access. It prescribes evidence and outcomes, not a fixed tool sequence, language, query budget or question whitelist. Cross-generation history must pass if that capability is claimed; a correct uncertainty response does not pass a blocked numerical gate.

Keep external result records for each stage: package integrity, actual loaded revision/isolation, host capability, provider coverage, reasoning and end-to-end result. Mark each **pass**, **fail**, **blocked** or **not_run**, with the real transcript, exact calculation/evidence anchors and reason. Do not store results or live balances/prices as defaults in the runtime. Reading the gate file, parsing JSON or verifying bytes is not a model replay or completed live acceptance; this guide claims no host cleanup or acceptance run.

Use [safety](safety.md) for failure classification, external access, explicit unsigned-artifact preparation and host approvals. A user/host authorization denial stops the action across routes; preserve provider denials and do not evade their controls. Transport failures, provider method/range/index/archive limits and evidence gaps are different outcomes, not installation failures. An independent ordinary authorized public source is not automatically a bypass for otherwise permitted research; disclose source changes, never silently fail over or retry without a finite bound. Credentials belong only in host-managed configuration. ClawHub/Skills Hub publication and guard acceptance remain separate authorized actions.
