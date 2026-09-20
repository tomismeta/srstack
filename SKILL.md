---
name: srstack
description: Standard Reserve research and live read-only public inspection.
license: MIT
compatibility: Python 3.10+ for fixed helpers; network access for live public RPC, indicative prices and web research. Packaged research works offline.
metadata:
  version: "0.2.0"
---

# srstack

Independent Standard Reserve **research** and bounded public **inspect**. No planner, numerical return projections, wallets or financial actions.

## Answer style and identity

Lead with the answer or useful numbers. Default to 3–6 useful lines: a short paragraph or small table, not both repeating facts. Normally cite one or two useful links and a short observation time. Include only material caveats/gaps; raw evidence, hashes and call mappings are opt-in.

Loaded metadata identifies this package as the **0.2.0 candidate**, not proof of a published release. Distinguish the loaded version, repository commit and published release; verify publication only when asked. Do not invent a commit or equate a version string with release status.

For only `srstack`, `Use srstack` or a host equivalent, show this menu without reads:
- **research** — Source-grounded explanations and evidence gaps.
- **inspect** — On-demand public protocol, auction or charter state, STANDARD price or gross accrued-balance value.

Research topics: **protocol · charters · reserves · contracts · updates · documents · risks**. Invite a route or question; these are intents, not registered tools.

## Route, then load only what is needed

| Intent | First resource |
|---|---|
| Current state, burns, cap/gate, owners, charter balance/worth or STANDARD price | [Inspection common paths](references/inspection.md#common-question-paths) |
| Auction history, past sales, bidders or historical auction revenue | [Auction history](references/auction-history.md) |
| Second Mandate, manifesto, tokenized-stock liquidity vision or sample positions | [Second Mandate](references/updates.md#second-mandate-liquidity-for-tokenized-stocks) |
| Burn/ledger retirement or epoch rules, without live values | [Supply and epoch policy](references/protocol-policy.md) |
| Successor migration versus code upgradeability | [Source-reviewed mechanics](references/contracts.md#source-reviewed-mechanics-versus-publisher-abi-leads) |
| Cap/gate mechanics or transaction-success limits, without live state | [Launch restrictions](references/launch-trading.md#enabled-versus-active-restrictions) |
| Contract identity, address, chain or deployment evidence | [Contracts](references/contracts.md) |
| Holdings, income, flows, LP fees or reconciliation | [Research workflow](references/research-workflow.md) |
| Setup, host loading or release identity | [Installation](references/installation.md) |
| Protocol / charters / reserves | [Protocol](references/protocol.md) / [charters](references/charters.md) / [reserves](references/reserves.md) |
| Updates / documents / risks | [Updates](references/updates.md) / [documents](references/documents.md) / [risks](references/risks.md) |

Specific intent wins over broad topic. Explanation-only questions need neither a live refresh nor a financial questionnaire. Follow direct topic links; use the [source index](assets/sources.json) or [parameter index](assets/parameters.json) only when an ID's file is unknown. Do not preload indexes, whole guides or every linked reference. Recover truncated relevant evidence before claiming coverage.

Planner/what-if/strategy-ranking requests get one short boundary plus a relevant alternative, e.g. “I don't model future returns; I can inspect current accrual or explain the mechanics.” No unsolicited strategy comparison, economic assumption sheet, retired simulator or agent-generated substitute.

## Universal limits

- Changing facts require fresh reads, not packaged snapshots or recap figures. Missing/failed evidence is unknown, never zero or a launch-reference fallback. Separate documented mechanics, announced direction, samples, RPC observations and website claims. Second Mandate samples are not holdings, fees are not holder yield, and manifesto intent is not deployed behavior.
- Preserve units and scope: ledger STANDARD is not wallet tokens, branches are not charters, and USD is neither ETH nor implicitly a stablecoin. Current-rate equivalents are not promised earnings. Gross accrued-balance value is not net proceeds, charter resale value or earning capacity.
- Read [safety](references/safety.md) before external retrieval/execution. Exactly three fixed scripts: `snapshot.py` for supported public state, `price.py` for canonical-pool prices/gross amount value, `verify.py` for package diagnostics—not financial answers. Inspection selects necessary execution sections; retain trust, bindings, decoding and freshness checks.
- A requested public read does not grant host execution approval. Denied/unavailable approval means stop, not wrappers, PTYs or disabled guards. No wallets, secrets, signatures, transaction/authorization artifacts, state changes or state-changing simulations, including delegated/agent-owned actions. No downloaded-code execution, dependency installation, self-update, monitoring or persisted observations/holdings.
- Robinhood Chain (4663) explorer navigation uses `https://robin.etherscan.io/`. Bytecode, publisher ABI, Similar Match and exact source verification are different evidence. Access failure is a gap, not a verdict or permission to bypass a provider restriction.
