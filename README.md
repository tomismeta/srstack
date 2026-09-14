# srstack

Independent **Standard Reserve research, scenario planning and public inspection** in one Agent Skill. Initial version **0.1.0**; planner schema/model **1**. Not an official Standard Reserve product.

## Use

```text
Use srstack.
Use srstack to explain charter withdrawals.
Use srstack plan in documented mode to compare expansion strategies.
Use srstack plan in stress mode to explore departures from documented limits.
Use srstack inspect to investigate a public charter.
```

- **Research:** source-linked mechanics, announcements, documented parameters and explicit unknowns.
- **Plan:** deterministic local calculations with explicit assumptions. Documented mode blocks known conflicts; stress mode reports departures. Compact output is the default; request `detail: "full"` for accounting and purchase schedules.
- **Inspect:** on-demand public evidence after authenticating identities and read interfaces. No fabricated contract adapter, background monitor or wallet connection.

Every planning answer begins with:

> **Hypothetical scenario—not contract-verified. Based on our interpretation of the whitepaper and official announcements, plus your assumptions. Not a forecast or executable quote.**

No-conflict status covers only checked packaged statements, not complete protocol feasibility. Unknown mechanics and user assumptions remain visible. There are no economic defaults or inferred executable prices.

## Install or try

This repository root is the skill. Keep `SKILL.md`, `references/`, `assets/`, `scripts/`, `LICENSE` and `release-manifest.json` together. There are no published tags or releases; pin a reviewed commit for a reproducible installation.

- **Hermes:** place the complete skill in the intended profile's `skills/srstack/`, or use a configured external skill directory. An installed skill can be invoked with `/srstack`.
- **OpenClaw:** place it in `<workspace>/skills/srstack/` or the appropriate managed skill location. Confirm no older same-name copy takes precedence.
- **Other harnesses:** use their Agent Skills loader or explicitly load [SKILL.md](SKILL.md). Relative resource paths are based at this directory.

See [host setup](references/installation.md). Replace installed copies cleanly rather than overlaying files; exclude `.git` metadata from copied runtime bundles. Nothing here installs itself or changes host permissions.

## Requirements and boundaries

Research needs a way to read packaged resources. Current inspection also needs permitted public retrieval and, where relevant, authenticated read-only chain methods. Planning needs permitted Python 3.10+ execution and safe descriptor-relative reads of the fixed bundled parameter files; unsupported backends fail closed. Python's standard library is sufficient—no pip dependencies.

The planner performs no network or environment lookup, accepts no user file paths, and writes no files. The skill prohibits credentials, wallet connections, signatures, approvals, executable financial payloads and state-changing EVM simulations. A skill prompt is not a sandbox; actual host controls still matter.

## Evidence

Start with [documents](references/documents.md) and [updates](references/updates.md). Source, parameter and entity indexes route to bounded records. Source dates distinguish publisher claims from observations; the package does not invent unknown contract identities or treat a snapshot as live state. A source-matching parameter is not contract verification.

Original code and summaries are [MIT-licensed](LICENSE). Third-party documents, posts, media, trademarks and protocol code retain their owners' rights. No safety or profitability guarantee is implied.
