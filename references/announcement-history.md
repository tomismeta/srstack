# Publisher history and review boundary

Announcement review cutoff: 2026-09-14T16:40:35Z; this archive was not re-scraped during the later website refresh. [Participation history](../assets/sources/history-participation.json) preserves superseded genesis terms, allocations, whitepaper release and early messaging; [audit history](../assets/sources/history-audits.json) preserves audit promises; [mechanics history](../assets/sources/history-mechanics.json) preserves the complete recovered four-post policy thread. [Attributed context](../assets/sources/announcements-context.json) is not protocol evidence.

## Dated status and superseded promise

The official profile displayed **“No token or NFT set is live yet”** at the earlier review (`sr-x-profile`). The recovered launch thread plans September 14; neither that date nor an accessible app proves launch happened. The later whitepaper/companion observations and separately added deployment evidence are mapped in [documents](documents.md); they do not silently refresh the profile's timestamp.

**The free-genesis description is superseded.** The earlier whitepaper §6, observed September 11, described free founding charters, no genesis sale/proceeds, and team-seeded liquidity (`sr-whitepaper-historical-free`; publication date unknown). The [Mint Details reply](https://x.com/standard_rsv/status/2098969964283846751) says **“liquidity fee”** for whitelist entry and a descending public auction for remaining spots, attributing the change to expected liquidity needs. That rationale is the publisher's claim, not independently measured demand. Both the earlier paid-model snapshot (`sr-whitepaper`) and current `sr-whitepaper-v1` reflect paid entry. Use `whitelist-liquidity-fee` and `genesis-charters` in [launch parameters](../assets/parameters/launch.json), not historical free wording.

The same reply assigns all founding proceeds to liquidity/vaults, none to the team. Current `sr-whitepaper-v1` §11 now supplies the founding floor-bid/remainder allocation and explicitly separates it from ongoing fees. Preserve the earlier announcement as history, not an unknown current split; see [reserves](reserves.md).

The current whitepaper was captured at 2026-09-14T22:15:13.789Z: sixteen sections including Immutables, published policy/exit/founding settings and unresolved internal launch-tax/auction-curve conflicts. The earlier fifteen-section/redacted `sr-whitepaper` remains dated evidence. These are publisher-document changes, not package release history, authenticated deployment events or code verification. [Documents](documents.md) and [source conflicts](risk-conflicts.md) carry the current interpretation.

## Earlier material changes

| Publication date | Publisher announcement | What it establishes, and what it does not |
|---|---|---|
| September 10 | [Launch and audit update](https://x.com/standard_rsv/status/2098183945926119589) | Claims both audits found **zero critical vulnerabilities** and promises reports before launch. Not zero findings, a reviewed report, remediation evidence or proof of safety. |
| September 8 | [Second allocations](https://x.com/standard_rsv/status/2097126276998013081) | Announces another allocation round and participant-selection rationale. No wallet eligibility or allocation list independently checked. |
| September 2 | [Second audit round](https://x.com/standard_rsv/status/2095171541604639094) | Says the second round is about to begin and credits Uniswap Foundation with audit funding/support. This is the project's attribution, not foundation corroboration or endorsement. |
| August 28 | [First allocations](https://x.com/standard_rsv/status/2093328953931116590) | Announces a first wave for active DeFi/NFT wallets, educators and early supporters, with more wallets planned. |
| August 26 | [First audit round](https://x.com/standard_rsv/status/2092602073011695793) | Announces audits and solicits security firms. Its contract-count claim does not identify an inspected suite. |
| August 23 | [Whitepaper release](https://x.com/standard_rsv/status/2091510125051969891) | Announces the paper and no token/NFT live then; links the project homepage, not an immutable implementation release. |
| August 20 | [Monetary-policy thread](https://x.com/standard_rsv/status/2090446255084188133) | Describes inflow-driven expansion/reserve accumulation and outflow-driven contraction. Replies are indexed individually; defensive outcomes remain publisher claims, not observed performance. Consult `sr-whitepaper-v1` and [protocol](protocol.md) for current design, retaining `sr-whitepaper` as earlier evidence. |

## Scope, media and missing release evidence

The recovered set covers August 17–September 13: the visible official profile, the launch and monetary-policy threads, an RSS sample, selected individual posts and nine reviewed images. All recovered identified posts have records, including routine teasers/reminders and third-party replies excluded from protocol facts. The reposted `@0xbeans` opinion retains its original author and URL; a repost does not establish a project role or contract attribution. Mirror-rendered replies without exposed canonical IDs were not adopted as sources.

RSS omitted official continuations that the browser recovered. Replies/media/repost navigation did not expose a complete unauthenticated archive. The August 18 post's video text was read, but playback, audio and transcript were not reviewed. Unreviewed ordinary attachments are identified in source limits. **This is not an entire-account guarantee**, and mirror delivery is not independent corroboration.

No new public contract address, source repository, named auditor or audit-report link was found in these reviewed announcement surfaces and selected images. The known homepage/whitepaper link was recovered, but no new immutable release was authenticated. This is a bounded non-discovery, not a claim that these materials do not exist elsewhere. Audit scope, code revision, findings across severities, remediation and deployed-bytecode correspondence remain unestablished. See [risks](risks.md) and [research workflow](research-workflow.md).

The bounded announcement non-discovery above is unchanged by the later `sr-contract-directory` and `sr-protocol-conditions` website additions. Those new deployment/condition records remain available through [contracts](contracts.md); do not erase them or mistake an announcement-only search boundary for a current site-wide absence of addresses.
