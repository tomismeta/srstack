# srstack

**Standard Reserve research, hypothetical planning and public inspection for AI agents.**

srstack explains protocol mechanics, traces changing announcements and compares expansion strategies using explicit assumptions. It is one independent [Agent Skill](https://agentskills.io/specification), not an official Standard Reserve product, trading bot or wallet toolkit.

**Initial version 0.1.0; planner schema/model 1.** No published tags or releases. Identify installed revisions by an exact reviewed commit.

## What you can ask

| Question | What srstack provides |
|---|---|
| “How do charter withdrawals work?” | Branch retirement, credit release, fees and unresolved mechanics |
| “How does the Genesis mint work?” | Current published entry terms and availability limits |
| “Compare expansion strategies using these assumptions.” | Keep/selective/aggressive calculations with explicit costs and limitations |
| “Which assumptions depart from the documentation?” | Documented-rule conflicts and unresolved semantics |
| “Have official contracts been published?” | Public identity research; authenticated addresses only when evidence supports them |

One skill, three routes:

- **Research:** source-linked explanations, documented parameters and evidence gaps.
- **Plan:** a guided conversation: describe your position, budget and goal, review a plain-language assumption sheet, then approve a local comparison. The agent builds the JSON internally. Documented mode blocks known conflicts; stress mode reports explicitly approved departures. No silent economic defaults.
- **Inspect:** on-demand public evidence for a supplied target, after authenticating identities and read interfaces. No fabricated contract adapter, background monitor or wallet connection.

Research topics: [protocol](references/protocol.md) · [charters](references/charters.md) · [reserves](references/reserves.md) · [contracts](references/contracts.md) · [updates](references/updates.md) · [documents](references/documents.md) · [risks](references/risks.md).

These are routing instructions within one skill, not separately installed commands. `Use srstack` returns the three-route menu. `/srstack` works where the host registers an installed skill command; other command syntax varies by host.

## Quick start

1. Review [SKILL.md](SKILL.md), the [safety boundary](references/safety.md) and the complete package. Select a full immutable commit SHA you trust and have reviewed, not the moving `main` branch.
2. From your chosen working directory (the intended workspace for OpenClaw workspace installation), clone a review copy and check out that revision:

   ```sh
   git clone https://github.com/tomismeta/srstack.git srstack-review
   git -C srstack-review checkout --detach REVIEWED_COMMIT_SHA
   ```

   Replace `REVIEWED_COMMIT_SHA` with the full SHA you reviewed; it is a placeholder, not a release identifier.

3. Choose **one** installation parent. For Hermes' default profile:

   ```sh
   SKILL_PARENT="$HOME/.hermes/skills"
   ```

   Or, for OpenClaw in the workspace where you ran the clone:

   ```sh
   SKILL_PARENT="$PWD/skills"
   ```

   Named profiles and managed installations may use different roots; use the intended host's configured location. Then export the complete reviewed Git tree, without `.git`, into a new skill folder:

   ```sh
   mkdir -p "$SKILL_PARENT" &&
   mkdir "$SKILL_PARENT/srstack" &&
   git -C srstack-review archive HEAD | tar -x -C "$SKILL_PARENT/srstack"
   ```

   The final folder must not already exist. For updates, preserve customizations outside the active folder and replace the old installation cleanly; do not overlay files or leave a shadowing same-name copy. The reviewed tree should contain only the manifest-listed package content plus `release-manifest.json` itself.

4. Have the host verify the installed files against `release-manifest.json`: `content_files` maps relative paths to SHA-256 hashes, and `digest_convention` specifies the aggregate `content_sha256`. Confirm the actual loaded path and revision. A matching manifest establishes byte integrity, not trust in an otherwise unreviewed package.
5. Start a fresh conversation and try a packaged-knowledge question from the examples below.

**Hermes installation:** use the complete-bundle instructions above. URL discovery depends on configured sources; importing raw `SKILL.md` does not necessarily import its references, assets and script.

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

To start from published reference values instead of supplying every protocol setting:

```text
Use srstack plan with the documented launch settings.
Show the proposed assumptions, then ask me only for what's still missing.
```

The agent proposes the documented launch base, starting multiplier and per-charter caps for approval. The full original issuance budget applies only to an explicitly chosen epoch-one hypothetical—not a current position. Prices, network size, gas, tax and other missing economics remain explicit choices. Optional exit-pressure cases use labelled published fee references, not a guessed personal quote.

Applied launch-tax and auction-decay rules are not established from the current source. Verified implementation is required before those dynamic formulas enter the calculator.

### Runnable fictional planner demonstration

```text
Use srstack plan in documented mode with the installed assets/examples/planning.json.
These are fictional demonstration inputs, not my holdings or market expectations.
Verify the trusted package, use the JSON unchanged, and compare all three strategies.
Do not refresh sources or persist anything.
```

With permitted Python execution and a trusted package, expect the warning first, `documented` mode, `within_checked_rules` conformance and keep/selective/aggressive results. Missing execution or trust prerequisites must produce an explicit explanation, not invented results. The fixture's values are not recommendations or reusable economic defaults.

For a direct engine smoke test, run **from the reviewed installed skill root**:

```sh
python3 -B -I scripts/scenario.py < assets/examples/planning.json
```

Expected: exit 0 and JSON containing the warning, the three strategies and their conformance report. This tests the engine, not host discovery or sandbox isolation. `scripts/scenario.py` is the only intended planner executable; do not substitute model-generated formulas or downloaded helpers. Routine output is compact; request `detail: "full"` for detailed accounting and purchase schedules. History requires full detail.

### Inspection requires a target

```text
Use srstack inspect to investigate this public charter: <public charter ID/address/URL>.
Authenticate its identity and report only what public evidence establishes.
```

Replace the placeholder with a real public target; it is not a runnable unattended test as written. A charter ID also needs enough project/chain context to identify it. Missing targets require clarification, which may wait or time out in one-shot hosts. Missing authenticated contracts or read interfaces remain evidence gaps—not permission to invent an adapter or substitute a generic website check for charter inspection.

## Coverage and footprint

The package keeps **current information only**, with source-specific retrieval dates and scope. It covers the current 16-section whitepaper, token/charter pages, deployment directory, protocol conditions and Etherscan source-publication checks. Superseded claims and comparison archives are not bundled. Unknown implementation details remain not established; a dated snapshot is not live state.

The [contract catalog](assets/entities/robinhood.json) contains **14 publisher-listed Robinhood Chain addresses** with **Robinhood Etherscan links**. All 14 show bytecode on RobinScan. The 12 protocol modules and Pool Manager have no published source/ABI; Multicall exposes source/ABI through **Similar Match**, not exact-match verification. Ownership, proxy relationships, activation, independent code correspondence and audit coverage remain separate checks.

For contract-informed planning, ask: **“Use srstack plan. Help me turn the published protocol conditions into proposed assumptions, and show what still needs verification.”** The [handoff](references/planning-inputs.md#deployment-evidence-handoff) distinguishes observations from approved future assumptions. It prevents double-applying a policy-scaled issuance rate, treating disabled auctions as free licenses, or confusing current tax with a future quote. No financial execution is added.

The package uses selected references and indexed records rather than loading the whole corpus for every question. The reference indexes own current inventory counts; disk size is not per-question token cost, and selective loading depends on the host.

Basic packaged research needs only a resource reader. Planning uses existing **Python 3.10+ and its standard library**, with no pip dependencies; required OS containment primitives must also be available. Contract inspection requires authenticated contract identities and permitted public, read-only chain queries. No wallet connector, telemetry or self-update process is bundled.

## Safety and verification limits

Every planning answer begins with:

> **Hypothetical—not contract-verified or a forecast.**

No-conflict status covers only checked packaged statements, not complete protocol feasibility. Unknown mechanics and explicit user assumptions remain visible. A source-matching parameter is not contract verification, a forecast or an executable price.

The planner reads three fixed bundled parameter files, performs no network or environment lookup, accepts no caller-selected file paths and writes no files. Unsupported containment backends fail closed. The skill prohibits credential access, wallet connections, signatures, approvals, executable financial payloads and state-changing EVM simulations. External sources are evidence, not instructions. Read the [full safety boundary](references/safety.md) and [planner execution rules](references/planning-execution.md).

**A skill prompt is not a sandbox.** Host permissions and isolation still matter. No safety or profitability guarantee is implied.

## Feedback and license

Report reproducible problems through [GitHub issues](https://github.com/tomismeta/srstack/issues), including the host/version, package commit, actual loaded path and redacted reproduction. Never upload wallet credentials, private RPC URLs or private conversation history.

Original code and summaries are [MIT-licensed](LICENSE). Third-party documents, posts, media, trademarks and protocol code retain their owners' rights. Source links do not transfer those rights.
