# Host installation and capabilities

For users/maintainers—not permission for an agent to install itself or change configuration. The v0.2.0 research/inspect candidate contains `SKILL.md`, exactly three runtime scripts (`snapshot.py`, `price.py`, `verify.py`), references, assets, license and manifest together. Avoid same-name stale copies. Select a trusted pinned release or reviewed commit; a manifest checksum comparison establishes byte integrity, not source authenticity or economic validity.

The candidate is not published: the normal installer remains the [pinned v0.1.3 ZIP commands](../README.md#normal-pinned-release-install), for the existing published package rather than this candidate. Select Hermes or OpenClaw's actual root, check only the runtime ZIP's exact `SHA256SUMS` entry, safely stage the archive, and run staged membership/hash verification before changing an old install. Downloaded checksums and a self-verifier cannot bootstrap trust; review/pin the release and trust its outer ZIP checksum first. The audit archive and GitHub automatic source archive are not runtime packages.

For isolated review or source export, use the [reviewed-commit workflow](../README.md#reviewed-commit-export-or-isolated-review-install) and a separate test profile/workspace. The repository's maintenance tools and CI are not runtime resources or skill actions. For any update, back up the complete old installation and its customizations outside every discovery root without overwriting another backup; install into an absent destination, never overlay. Verify the final root with `python3 -B -I scripts/verify.py` before discovery; restore the backup if final verification fails. Membership must exclude `.git`, `maintenance`, `.github` and `dist`. Keep the review clone, staging and backups outside discovery roots too.

Before moving/removing an old installation or deleting a temporary checkout, change the maintainer shell/tool working directory to an existing stable directory outside that tree. Start subsequent commands there, then select the verified installed root explicitly for helper execution. If a command reports that its current directory no longer exists, restore a valid cwd; do not reinstall the host or treat it as a skill-load failure.

## Hermes

Primary root: `~/.hermes/skills/`; named profiles may use another Hermes home. Put the package at that profile's `skills/srstack/`, or in an explicitly configured external skill directory containing `srstack/`. Do not duplicate across roots.

Hermes uses `skills_list` for discovery and `skill_view` for progressive resources. Request literal paths relative to the returned skill directory, such as `references/inspection.md`; use native resource loading rather than assuming a general filesystem reader is necessary. Resolve execution paths against the same loaded directory, not unrelated working directories.

Invoke `/srstack` or natural-language “Use srstack inspect”. Confirm the selected description/revision in a fresh conversation. Local loading differs from Skills Hub community-install guard acceptance; do not bypass guards to claim compatibility.

The new-skill authoring validator has a shorter description budget than the existing-skill loader. Keep description short and metadata version a string; no nested host metadata merely to repeat requirements. Use the Python supported by the installed Hermes release; all three entrypoints need only standard-library Python 3.10+ and the containment primitives described in [execution](execution.md). Live state/price readers additionally require existing permitted public network access; default package verification stays offline.

One-shot Hermes sessions may be unable to complete a normal tool-approval prompt. Select a [permitted CLI or stdin path](execution.md#input-transport-and-host-approvals) before running a helper; `verify.py` requires no stdin and performs integrity-only verification by default. If execution still requires approval, stop and request an approval-capable session for that exact command. Do not hunt for a PTY/wrapper that avoids the check or require `--yolo`. Successful execution with approvals bypassed establishes helper behavior only, not ordinary approval-flow compatibility.

[Official Hermes Skills System](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills/).

## OpenClaw

Place the complete package at `<workspace>/skills/srstack/` or the managed skills directory for the intended state/profile. Skill-root precedence can shadow a package; use a fresh session or explicitly refresh the selected revision.

The catalog points to `SKILL.md`; resources resolve against its directory. Invoke natural-language “Use srstack” or the installed host/channel's explicit reference/command; slash and `$` syntax vary. In sandbox/node setups, resources and Python must exist in the actual execution environment, not just the main host.

No global Python eligibility gate: offline research remains useful without execution. No installer declaration, secret/environment requirement or tool-dispatch command is supplied.

[Official OpenClaw Skills](https://docs.openclaw.ai/tools/skills).

## Other harnesses and distribution

Use common Agent Skills frontmatter (name, description, license, string metadata), discovery/explicit SKILL loading and relative-resource delivery without truncating required content. Recover omissions via documented host mechanisms, not invented selectors/permissions.

- **Research:** packaged topic/source resources; public retrieval only where needed.
- **Inspect:** trusted package, existing permitted Python with fixed CLI arguments or safe JSON stdin for `snapshot.py` RPC and `price.py` canonical-pool API reads, or existing permitted authenticated read-only facilities for other supported research. Verify snapshot's script plus entity/interface catalogs; verify price's script plus entity catalog only. Price uses DEX Screener by default with labelled GeckoTerminal availability fallback, explicit provider selection and cross-check only on request; each target still needs existing host permission, and access denial never authorizes switching. A current-value request already calls for the needed price read; no wallet, arbitrary providers or package-created provider/account.
- **Diagnose:** `verify.py` alone checks complete package membership/hashes without a child or network request. `--charter ID` and `--price` explicitly request live checks and may combine with each other; the removed `--offline` flag is invalid. Every smoke verifies the package first, and normal execution approvals still apply. Status/timing output is not full financial output, proof of sandboxing or a host-discovery test. See [the diagnostic contract](execution.md#package-and-smoke-diagnostic).

ClawHub is a separate distribution service: local directory/archive preparation does not establish hosted acceptance, ownership, name availability, moderation or registry clearance. Hosted publication/scanning needs separately scoped permission; never upload merely to check a local package.

No prompt, metadata, loader or scanner enforces isolation or universally certifies compatibility. Apply [safety](safety.md) and actual host policy.
