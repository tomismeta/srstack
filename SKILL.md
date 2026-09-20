---
name: srstack
description: Standard Reserve research and live read-only public inspection.
license: MIT
compatibility: Python 3.10+ for fixed helpers; network access for live public RPC, indicative prices and web research. Packaged research works offline.
metadata:
  version: "0.2.0"
---

# srstack

Independent Standard Reserve research and bounded public reads. Use existing host permissions; no wallet or transaction actions, strategy simulator or numerical return projections.

## Answer style

Lead with the answer, useful numbers or next question—not a disclaimer. For a simple question use a short paragraph or small table, not both repeating the same facts. Default to roughly 3–6 useful lines; expand only when needed.

Use at most one short caveat when it changes interpretation, such as “RPC snapshot using publisher ABI” or “Gross indicative value before withdrawal and trading costs.” Mark missing values directly. Do not repeat generic warnings, long limitations or provenance tables.

Normally cite one or two useful source links. A short observation time is enough when freshness matters; omit block numbers/hashes unless requested. Keep raw responses, call mappings and detailed evidence available on request. Never call publisher-ABI reads source-verified or present current-rate equivalents as promised earnings.

## Bare invocation

For only `srstack`, `Use srstack` or a host equivalent, print this menu without reads or requests:

- **research** — Source-grounded explanations and evidence gaps.
- **inspect** — On-demand public protocol, auction or charter snapshot, current STANDARD price or gross accrued-balance value; no wallet or monitoring.

Research topics: **protocol · charters · reserves · contracts · updates · documents · risks**.

Invite a route or question. These are intents, not registered tools.

## Load only what answers the question

Specific intent precedes broad topic. Do not preload indexes or related guides.

Changing facts—balances, prices, rates, supply, inventory, ownership, activation, source verification and latest announcements—require a fresh read. Never answer them from packaged snapshots or recap figures. If the read is unavailable, say so; do not fall back to a launch reference. Packaged rules, identities and ABI definitions are reference configuration, not live state.

| Intent | First resource |
|---|---|
| Explain the Second Mandate, manifesto, tokenized-stock liquidity vision or sample market positions | [Second Mandate](references/updates.md#second-mandate-liquidity-for-tokenized-stocks) |
| Explain burn versus ledger retirement/deposits or epoch rollover; no requested live values | [Supply and epoch policy](references/protocol-policy.md) |
| Explain successor migration versus code upgradeability | [Source-reviewed mechanics and ABI leads](references/contracts.md#source-reviewed-mechanics-versus-publisher-abi-leads) |
| Explain cap/gate mechanics or transaction-success limits; no requested live state | [Launch restrictions](references/launch-trading.md#enabled-versus-active-restrictions) |
| Current burns, holding cap, Pool Manager gate, Hook owner/pending owner, price/value, charter worth, current state or availability | [Inspection](references/inspection.md) |
| Identity, address, chain, deployment, ownership | [Contracts](references/contracts.md) |
| Supply, holdings, income, flows, LP fees, reconciliation | [Research workflow](references/research-workflow.md) |
| Setup or host loading | [Installation](references/installation.md) |
| Protocol / charters / reserves | [Protocol](references/protocol.md) / [charters](references/charters.md) / [reserves](references/reserves.md) |
| Current updates / documents / risks | [Updates](references/updates.md) / [documents](references/documents.md) / [risks](references/risks.md) |

Generic research: choose the relevant topic; use documents for source discovery. Follow direct topic links to needed records. Only when an ID's file is unknown, use the [source index](assets/sources.json) or [parameter index](assets/parameters.json). Never load all groups. Recover truncated resources through documented host mechanisms before claiming coverage.

Explanation-only questions use packaged rule/source context without a live refresh or financial questionnaire. Questions requesting current numbers or flags use inspection instead. For several supported metrics, use the narrowest snapshot view containing them all; a charter snapshot already includes burn and launch-restriction context. Do not add a protocol snapshot or price lookup merely because those topics appear together. Preserve all trust checks; summarize only requested fields.

For planning, what-if or investment-comparison requests, explain relevant mechanics, risks and missing evidence qualitatively. Offer relevant current inspection if useful; do not collect an economic assumption sheet, rank strategies, fabricate future cash flows, run a retired simulator or replace it with agent-generated arithmetic. The skill does not model branch expansion, future exits, stock-market liquidity returns or holder fee entitlements.

Use current evidence and preserve its units and scope. Distinguish documented facts, announced direction, sample illustrations, RPC observations and website-reported values. Missing or failed reads are unknown, never zero. Source details are expandable on request.

Current price and gross-value questions use the fixed `scripts/price.py` reader; a current-value request already authorizes its needed fresh price read under existing host permissions. For charter worth, ask only for a missing public charter ID, read its fresh `charter_pending`, then pass that exact amount to the price helper. This is gross accrued ledger value, not wallet tokens, net proceeds, charter resale value or earning capacity. STANDARD amounts alone do not trigger a lookup unless monetary valuation is requested. Preserve supplied units; never treat USD as ETH or assume stablecoins equal USD.

Price reads default to DEX Screener, with a disclosed GeckoTerminal fallback only for availability failures—not access denial, invalid data or identity mismatch. Honour explicit provider selection; cross-check the other provider only when requested. Keep selected-provider quotes and gross values together; do not average, choose the higher quote or fill missing denominations across providers. Show fallback and material cross-check differences; each provider's retrieval time is separate and quote age remains unknown. See the [price contract](references/execution.md#price-helper).

For Robinhood Chain (4663), use `https://robin.etherscan.io/` for contract navigation and new explorer checks. Read each record's source-publication status: bytecode, ABI availability, Similar Match and exact verification are different. Access failures are gaps, not a verdict or permission to silently switch providers.

## Action boundary

Read [safety](references/safety.md) before external retrieval or execution. Use only `scripts/snapshot.py` for supported public state reads and `scripts/price.py` for canonical-pool indicative prices and optional gross amount valuation. Publisher-supplied interfaces require fixed targets, declared view/pure methods, decoding/binding checks and block context; they do not imply verified source code. Provider prices have retrieval times, not independently assured freshness or a shared chain block. No wallets, credentials, signatures, transaction/authorization payloads, state changes or state-changing simulations—even delegated or agent-owned. No downloaded code execution, dependency installation or persistence of observations/personal holdings.

The third fixed entrypoint, `scripts/verify.py`, is a compact package diagnostic: no flags verifies only membership/hashes without network or child execution; `--charter ID` and `--price` explicitly select live helper checks. Every smoke verifies the complete package first. It does not certify authenticity, sandboxing or economic correctness. Snapshot/price CLI flags avoid stdin; no-argument JSON stdin remains supported by those two readers. Follow [execution](references/execution.md) for commands and approval boundaries.

Host execution approval remains separate from a requested public read. If approval cannot be obtained, stop promptly; do not retry through wrappers/PTYs or recommend disabling guards. Use the [input and approval guidance](references/execution.md#input-transport-and-host-approvals).
