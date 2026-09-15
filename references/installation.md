# Host installation and capabilities

For users/maintainers—not permission for an agent to install itself or change configuration. Install the complete reviewed package root containing `SKILL.md`, script, references, assets, license and manifest together. Avoid same-name stale copies. Select a trusted reviewed commit; a manifest checksum comparison establishes byte integrity, not source authenticity or model validity.

The repository also contains maintenance tools and CI configuration that are not runtime resources. Follow the [reviewed-commit export steps](../README.md#quick-start) to produce only manifest-listed content plus the manifest. Do not install the entire repository, run maintenance commands as skill actions, or start discovery before export succeeds.

## Hermes

Primary root: `~/.hermes/skills/`; named profiles may use another Hermes home. Put the package at that profile's `skills/srstack/`, or in an explicitly configured external skill directory containing `srstack/`. Do not duplicate across roots.

Hermes uses `skills_list` for discovery and `skill_view` for progressive resources. Request literal paths relative to the returned skill directory, such as `references/planning.md`; use native resource loading rather than assuming a general filesystem reader is necessary. Resolve execution paths against the same loaded directory, not unrelated working directories.

Invoke `/srstack` or natural-language “Use srstack plan”. Confirm the selected description/revision in a fresh conversation. Local loading differs from Skills Hub community-install guard acceptance; do not bypass guards to claim compatibility.

The new-skill authoring validator has a shorter description budget than the existing-skill loader. Keep description short and metadata version a string; no nested host metadata merely to repeat requirements. Use the Python supported by the installed Hermes release; the planner needs only standard library Python 3.10+ and the containment primitives described in [safety](safety.md).

[Official Hermes Skills System](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills/).

## OpenClaw

Place the complete package at `<workspace>/skills/srstack/` or the managed skills directory for the intended state/profile. Skill-root precedence can shadow a package; use a fresh session or explicitly refresh the selected revision.

The catalog points to `SKILL.md`; resources resolve against its directory. Invoke natural-language “Use srstack” or the installed host/channel's explicit reference/command; slash and `$` syntax vary. In sandbox/node setups, resources and Python must exist in the actual execution environment, not just the main host.

No global Python eligibility gate: offline research remains useful without execution. No installer declaration, secret/environment requirement or tool-dispatch command is supplied.

[Official OpenClaw Skills](https://docs.openclaw.ai/tools/skills).

## Other harnesses and distribution

Use common Agent Skills frontmatter (name, description, license, string metadata), discovery/explicit SKILL loading and relative-resource delivery without truncating required content. Recover omissions via documented host mechanisms, not invented selectors/permissions.

- **Research:** packaged topic/source resources; public retrieval only where needed.
- **Inspect:** existing permitted readers and authenticated read-only chain methods. No package-created provider/account/wallet.
- **Plan:** trusted package, existing permitted Python and safe JSON stdin transport. Host read/hash utilities or minimal fixed launcher can check manifest/script/three fixed resource hashes and return a compact result; do not dump source bodies merely to verify integrity. Missing capability means explanation/gap, not claimed calculation output.

ClawHub is a separate distribution service: local directory/archive preparation does not establish hosted acceptance, ownership, name availability, moderation or registry clearance. Hosted publication/scanning needs separately scoped permission; never upload merely to check a local package.

No prompt, metadata, loader or scanner enforces isolation or universally certifies compatibility. Apply [safety](safety.md) and actual host policy.
