# Host installation and capabilities

Install/update only when requested and under normal host approval. Use Git and Python 3.10+ on a supported POSIX host. Review the exporter, runtime and [safety rules](safety.md) before executing package code; integrity verification is not publisher authentication.

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

No files are deleted. Failed verification retains the candidate as `failed-install` and restores the previous root. If interruption or restoration fails, keep skill use paused and recover from the printed directory. Keep backups outside discovery roots until the new installation is confirmed; never merge old customizations into the reviewed runtime.

After success, verify the loaded path and the printed SHA against `WORK/reviewed-commit.txt`, then refresh discovery/reload as described below. Resume invocations only against the verified root.

**Transport compatibility:** user-reported direct-TLS `WRONG_VERSION_NUMBER` failures were endpoint-independent in an intercepted sandbox; urllib+Alchemy worked there. Snapshot/history now use proxy-aware `urllib.request`. That evidence does not establish public-RPC access or universal host compatibility. Test the intended provider and retain honest denial diagnostics.

## Host loading and sessions

- **Hermes:** find the actual profile root (commonly `~/.hermes/skills`). Use `skills_list`/`skill_view` and literal relative resource paths. `/srstack` or “Use srstack inspect” invokes the selected installation. [Host docs](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills/).
- **OpenClaw:** use the intended workspace's `skills/srstack/` or configured managed root; avoid shadowing duplicates. Resources and Python must exist in the execution environment. [Host docs](https://docs.openclaw.ai/tools/skills).
- **Other hosts:** load the complete Agent Skills runtime and selected relative resources, not `SKILL.md` alone. Packaged explanations can work without Python; live helpers need permitted execution/network access.

After replacement, refresh discovery and reload the skill in the main session if the host supports it. Existing loaded context may remain stale: report that limitation rather than claiming reload succeeded. A fresh `/new` is a host-dependent way to load the new revision, not an automatic installation step or a requirement to restart Telegram. One chat cannot refresh all other chats.

Keep the maintainer working directory outside any tree being moved. A missing cwd requires selecting an existing directory, not reinstalling the host. If interruption or rollback fails, pause skill use and recover the complete root from the printed recovery directory.

## Acceptance and distribution

Run the [post-install checks](../README.md#quick-test-after-installation). Offline integrity, host routing and live RPC access are separate results. HTTP 401/403 means the original request was denied, not that installation failed. The helper's env-only configuration hint is informational; see [provider guidance](execution.md#rpc-provider-guidance).

Use [safety](safety.md) for external access, explicit unsigned-artifact preparation and host approvals. Do not use wrappers or broaden permissions to evade a denial. ClawHub/Skills Hub publication and guard acceptance are separate from a local install and require their own authorization.
