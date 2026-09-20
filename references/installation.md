# Host installation and capabilities

For users/maintainers—not permission for an agent to install itself or change configuration. The **0.2.0 research/inspect candidate is not a published release**. Its package version is separate from the full source commit identifying the reviewed revision. The complete runtime contains `SKILL.md`, exactly three scripts (`snapshot.py`, `price.py`, `verify.py`), references, assets, license and manifest. A manifest comparison establishes byte integrity, not authenticity or economic validity.

Use the single [candidate installation workflow](../README.md#install-the-020-candidate): clone/fetch the named `feature/v0.2.0` branch, resolve and review its full commit, then use that checkout's `maintenance/package.py export` with the full pin and an absent staging destination. Review the exporter and runtime before executing them; a bundled self-verifier cannot bootstrap trust. The repository, GitHub's automatic source archive and audit evidence are not installable runtimes.

Select the actual host/profile root. Keep the review clone, staging and unique backups outside **every** discovery root, with recovery files on the installation's filesystem. The documented replacement verifies staging, preserves the entire old root and customizations, moves the complete new root into the absent destination, and verifies again before discovery. It restores the previous root if final verification fails. Never overlay, silently merge customizations or retain a shadowing same-name copy. The runtime excludes `.git`, `maintenance`, tests, `.github` and `dist`; maintenance tools and CI are not skill actions. Keep the full commit record outside the hashed runtime and confirm the actual loaded path/version in a fresh conversation.

Before moving/removing an old installation or deleting a temporary checkout, change the maintainer shell/tool working directory to an existing stable directory outside that tree. Start subsequent commands there, then select the verified installed root explicitly for helper execution. If a command reports that its current directory no longer exists, restore a valid cwd; do not reinstall the host or treat it as a skill-load failure.

## Hermes

Primary root: `~/.hermes/skills/`; named profiles may use another Hermes home. Put the package at that profile's `skills/srstack/`, or in an explicitly configured external skill directory containing `srstack/`. Do not duplicate across roots.

Hermes uses `skills_list` for discovery and `skill_view` for progressive resources. Request literal paths relative to the returned skill directory, such as `references/inspection.md`; use native resource loading rather than assuming a general filesystem reader is necessary. Resolve execution paths against the same loaded directory, not unrelated working directories.

Invoke `/srstack` or natural-language “Use srstack inspect”. Confirm the selected path and `0.2.0` package version in a fresh conversation against the retained full source pin. Local loading differs from Skills Hub community-install guard acceptance; do not bypass guards to claim compatibility.

Use the Python supported by the installed Hermes release; all three entrypoints need only standard-library Python 3.10+ and the containment primitives described in [execution](execution.md). Live state/price readers additionally require existing permitted public network access; default package verification stays offline.

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
- **Inspect:** trusted package, permitted Python execution and the fixed [snapshot/price helper interfaces](execution.md). A current-value request authorizes only the necessary read within existing host permissions, not a wallet connection or arbitrary provider. For a charter value, read its pending STANDARD balance and pass the successful quantity unchanged to `price.py --amount-standard DECIMAL`; diagnostic status is not monetary output.
- **Diagnose:** `verify.py` alone checks complete package membership/hashes without a child or network request. `--charter ID` and `--price` explicitly request live checks and may combine; do not add `--offline`. Each diagnostic verifies the package first, and normal execution approvals still apply. Status/timing output is not financial output, proof of sandboxing or a host-discovery test. See [the diagnostic contract](execution.md#package-and-smoke-diagnostic).

For candidate acceptance, follow the [post-install checks](../README.md#quick-test-after-installation): research/inspect menu, offline packaged research, no planner, and the Second Mandate boundaries (sample is not holdings, fees are not holder yield, manifesto is not deployment). Live helper checks are optional and require permission.

ClawHub is a separate distribution service: local directory/archive preparation does not establish hosted acceptance, ownership, name availability, moderation or registry clearance. Hosted publication/scanning needs separately scoped permission; never upload merely to check a local package.

No prompt, metadata, loader or scanner enforces isolation or universally certifies compatibility. Apply [safety](safety.md) and actual host policy.
