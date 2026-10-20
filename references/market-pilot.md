# King of the Markets: points, season and rewards

King of the Markets is a publisher-run market competition: a team score and a wallet's offchain points are not wallet tokens, charter branches or a settled reward entitlement. The October 19, 2026 review covers published rules, application bindings and dated indexer/rendered observations, not an independently reconciled payout ledger. Use existing [identity guidance](contracts.md) and [read-only safety boundaries](safety.md#preparation-and-wallet-boundary); a points question does not require connecting a wallet.

Evidence: [market-pilot source records](../assets/sources/market-pilot.json), [launchpad sources](../assets/sources/launchpad.json), the [official rules](https://www.standardreserve.xyz/docs/king-of-the-markets/) and [rewards page](https://www.standardreserve.xyz/liquidity/rewards/). The acquired root-linked rules module and retained October 19 rendered page have different evidence scopes; neither turns a displayed total into audited accounting. Current scores, balances and marked pot values stay outside this reference.

| Question | Minimum relevant evidence and interpretation |
| --- | --- |
| Which team and season does this activity count toward? | Season identifier, source-specific time bounds and authenticated market/token route; use the [capability planning map](capabilities.md#planning-map) and [stock/market inventory](interface-inventory-stock-markets.md). A ticker or country label alone is not a factory/market identity. |
| What points are supported for this wallet? | Publisher wallet/team records with as-of metadata, pagination and unresolved activity, plus relevant trade/referral evidence where available. The `market-pilot-entitlement` capability distinguishes these observations from entitlement; [launchpad interfaces](interface-inventory-launchpad.md) supply only their actual reviewed onchain scope. |
| What would those points pay, and is the pot funded? | Applicable allocation rules, final scoring scope, assets/prices, custody, liabilities and attributable distribution receipts. Follow `market-pilot-entitlement` in the [planning map](capabilities.md#planning-map); a reward Safe or fee getter is not a rewards-distributor ABI. |

## Teams and season

The reviewed publisher rules name four teams: **US/SPCX, China/BABA, South Korea/SKHY and ETH/WETH**. Stock-route trades score for the stock's country; WETH-paired launch tokens score for ETH from the launchpad's trades. A wallet can score for more than one team. Trader, token deployer and referrer are distinct roles, not interchangeable ownership rights. Token generations still coexist; see [launchpad generation and controls](launchpad.md).

The [October 12 announcement](https://x.com/standard_rsv/article/2109652523502248183) proposed an October 14 launch and 14-day competition. The [October 19 developer announcement](https://x.com/0xbeans/status/2112221543929713122) extended it by another week and announced an additional “100k”; that post alone establishes neither its currency nor receipt of funding. The October 19 docs/application and rendered reward page give **November 4, 2026, 13:00 America/New_York = 18:00 UTC**, after the daylight-saving transition. This is a dated published deadline, not a hardwired current season. Retain the start-time conflict below rather than silently choosing an event boundary.

## Points are not payouts

The reviewed docs describe regular-hours stock trades as 1 point per dollar and launch-token trades as approximately 4.3 points per dollar (the application constant is 13/3). They say points follow paid fees, count qualifying Reserve-market legs including multihop routes, and count buys and sells. These are published scoring descriptions, **not a current fee schedule**: the docs' 0.3% stock-fee illustration must not override later stock-pool configuration. See [effective stock fees and indexer coverage](liquidity-markets.md).

The docs describe referrals as 5% and deployer points as 10%, deducted from the trader rather than created on top; own-token trades score in full and self-referrals are dropped. Onchain trade/referral events can establish observed activity, but points and rewards are computed offchain. An event does not prove the indexer's classification, final points or settlement.

Report useful supported points and coverage even when payout rules remain unresolved. Preserve source, season/team/wallet scope, `asOfBlock`, `asOfTime`, `stale`, page/cursor coverage and unresolved swaps/volume. Missing metadata is unknown; `stale:false` does not certify correct accounting, and a failed request is not an empty ledger. Only summary and token inventory endpoints were exercised in the catch-up; other endpoint shapes are discovery leads described in [public market evidence](liquidity-markets.md#public-market-evidence).

A user-supplied rule can support a clearly labelled conditional calculation using stated inputs and denominators. Do not present that scenario as an exact entitlement or build an estimator from incompatible sources. Missing payout evidence blocks the dependent payout calculation, not every observation or explanation.

## Conflicting published rules

These are October 19 source observations, not fallback configuration. The API fields were observed in the publisher's `/v1/pilot/summary`; their names alone do not establish how accounting was applied.

| Issue | Docs/application or announcement | Other publisher evidence and unresolved boundary |
| --- | --- | --- |
| Launch-token points | Approximately 4.3 points/$ (13/3 constant) | API `tokenMultiplier:5`; do not equate a named multiplier with an independently proved points/$ formula. |
| Referral share | 5% of trader points | API `referrerBps:1000`; October 14 launch graphic also advertised 10%. API `traderBonusBps:500` is not automatically the docs' referral rule. |
| Contribution to pot | 20% of the launchpad's 1% base fee | Rendered rewards page says the protocol's share goes into the pot; its displayed examples imply approximately 0.7% of trade value. These are different assessment bases/accounting descriptions, not interchangeable rates. |
| Start | October 14, 2026, 17:00 UTC (13:00 Eastern daylight time) | API start was October 14, 16:45 UTC. Do not silently move the eligibility window. |
| Duration/end | Original announcement: 14 days | October 19: another week; docs/rendered deadline November 4 at 13:00 New York/18:00 UTC, also the observed API endpoint. Preserve the original duration as historical, not current. |

Do not average these rules, choose a winner without evidence, or infer reconciliation from field names. A later explicit revision or applied-accounting evidence may resolve a conflict; retain which source and period it resolves. A condensed answer using already collected evidence must retain material conflicts without refreshing merely to reformat it.

## Funding and distribution evidence

The October 19 rendered page describes an **opening $1.1 million pot comprising USDG, stock tokens and STANDARD**. It is a mixed-asset dollar valuation, not necessarily $1.1 million of USDG cash. The older October 12 article's “1M+ USDG” pool and “1M USDG” jackpot wording is separately dated promotional evidence, not a reconciliation of that later composition.

The reviewed docs/page describe **65% incentives shared by points across teams and 35% jackpot for the winning team's participants**. This is a published distribution rule, not proof that any wallet has been allocated or paid that fraction. Keep opening pot, subsequently marked reward value, custody, liabilities, final reward allocation and settled receipts separate. For a mixed pot, asset balances, token scales, valuation sources and timing are all necessary to compare like amounts; displayed growth need not be a cash inflow.

The publisher's reward address is identified in dated research as a **Safe proxy**, not a dedicated automated distributor. Its address, threshold or any one asset balance cannot prove complete custody, funding provenance, solvency, insolvency or payout automation. In particular, a zero USDG observation at one address cannot establish that no mixed-asset rewards exist. The [stock/market inventory](interface-inventory-stock-markets.md) records actual interface coverage and gaps; launchpad fee/configuration reads do not supply a missing settlement interface.

A funding conclusion needs scoped transfer provenance and holdings; an entitlement needs applicable beneficiary/rule/allocation evidence; a payment conclusion needs successful canonical receipts and attributable asset movements. None confers charter revenue rights or changes [reserve routing](reserves.md). No reward calculator, bundled indexer client or wallet action is implied by this reference.
