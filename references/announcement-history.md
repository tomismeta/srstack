# Publisher history and review boundary

Review cutoff: 2026-09-14T16:40:35Z. [Participation history](../assets/sources/history-participation.json) preserves superseded genesis terms, allocations, release and early messaging; [audit history](../assets/sources/history-audits.json) preserves audit promises; [mechanics history](../assets/sources/history-mechanics.json) preserves the complete recovered four-post policy thread. [Attributed context](../assets/sources/announcements-context.json) is not protocol evidence.

## Current status and superseded promise

The official profile still displayed **“No token or NFT set is live yet”** at review (`sr-x-profile`). The latest recovered launch thread plans September 14; neither the date nor an accessible app proves that launch happened. The mint and whitepaper observations are covered in [documents](documents.md) and [charters](charters.md).

**The free-genesis description is superseded.** The earlier whitepaper §6, observed September 11, described free founding charters, no genesis sale/proceeds, and team-seeded liquidity (`sr-whitepaper-historical-free`; its publication date is unknown). The new [Mint Details reply](https://x.com/standard_rsv/status/2098969964283846751) explicitly says **“liquidity fee”** for the whitelist mint and a descending public auction for remaining spots. It attributes the change to greater expected liquidity needs; that rationale is the publisher's claim, not independently measured demand. The current whitepaper also reflects the paid model (`sr-whitepaper`). Use `whitelist-liquidity-fee` and `genesis-charters` in [launch parameters](../assets/parameters/launch.json) for current settings, not the historical free wording.

The same reply says all genesis mint proceeds go to initial liquidity and protocol vaults, with none to the team. **Genesis routing is not the ongoing fee split.** Do not overwrite the continuing fee-engine design described by `sr-whitepaper`; see [reserves](reserves.md) and the canonical parameter records.

## Earlier material changes

| Publication date | Publisher announcement | What it establishes, and what it does not |
|---|---|---|
| September 10 | [Launch and audit update](https://x.com/standard_rsv/status/2098183945926119589) | Claims both audits found **zero critical vulnerabilities** and promises reports before launch. Not zero findings, a reviewed report, remediation evidence or proof of safety. |
| September 8 | [Second allocations](https://x.com/standard_rsv/status/2097126276998013081) | Announces another allocation round and participant-selection rationale. No wallet eligibility or allocation list independently checked. |
| September 2 | [Second audit round](https://x.com/standard_rsv/status/2095171541604639094) | Says the second round is about to begin and credits Uniswap Foundation with audit funding/support. This is the project's attribution, not foundation corroboration or endorsement. |
| August 28 | [First allocations](https://x.com/standard_rsv/status/2093328953931116590) | Announces a first wave for active DeFi/NFT wallets, educators and early supporters, with more wallets planned. |
| August 26 | [First audit round](https://x.com/standard_rsv/status/2092602073011695793) | Announces audits and solicits security firms. Its contract-count claim does not identify an inspected suite. |
| August 23 | [Whitepaper release](https://x.com/standard_rsv/status/2091510125051969891) | Announces the paper and no token/NFT live then; links the project homepage, not an immutable implementation release. |
| August 20 | [Monetary-policy thread](https://x.com/standard_rsv/status/2090446255084188133) | Describes inflow-driven expansion/reserve accumulation and outflow-driven contraction. Replies are indexed individually; defensive outcomes remain publisher claims, not observed market performance. Consult `sr-whitepaper` and [protocol](protocol.md) for the fuller design. |

## Scope, media and missing release evidence

The recovered set covers August 17–September 13: the visible official profile, the launch and monetary-policy threads, an RSS sample, selected individual posts and nine reviewed images. All recovered identified posts have records, including routine teasers/reminders and third-party replies excluded from protocol facts. The reposted `@0xbeans` opinion retains its original author and URL; a repost does not establish a project role or contract attribution. Mirror-rendered replies without exposed canonical IDs were not adopted as sources.

RSS omitted official continuations that the browser recovered. Replies/media/repost navigation did not expose a complete unauthenticated archive. The August 18 post's video text was read, but playback, audio and transcript were not reviewed. Unreviewed ordinary attachments are identified in source limits. **This is not an entire-account guarantee**, and mirror delivery is not independent corroboration.

No new public contract address, source repository, named auditor or audit-report link was found in these reviewed announcement surfaces and selected images. The known homepage/whitepaper link was recovered, but no new immutable release was authenticated. This is a bounded non-discovery, not a claim that these materials do not exist elsewhere. Audit scope, code revision, findings across severities, remediation and deployed-bytecode correspondence remain unestablished. See [risks](risks.md) and [research workflow](research-workflow.md).
