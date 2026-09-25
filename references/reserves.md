# Fees, reserves and defense

Published accounting and v1.1 policy, not saved holdings or verified privileges. Sources: `sr-whitepaper-v1` §§3,6,11–12,15 and `sr-protocol-v1-1-announcement` via the [source index](../assets/sources.json). Exact reference scopes: [reserve parameters](../assets/parameters/reserves.json), [launch parameters](../assets/parameters/launch.json). Current balances, owners and routing require live reads.

## Founding funding is not the ongoing fee split

Founding proceeds escrow until finalization and fund liquidity and protocol vaults, with no team share. The current publication does not specify the exact split. Genesis token liquidity is described in the currency section; do not substitute ongoing fee-allocation percentages for founding receipts. [sr-whitepaper-v1: currency, charters]


The founding allocation is separate from steady-state trading/charter-auction receipts. Do not use ongoing fee percentages for founding proceeds. [sr-whitepaper-v1: reserves]

## Ongoing ETH routing — §11

The whitepaper uses current net flow to select the active vault: expansion when positive, contraction otherwise. Reference shares are `ongoing-active-vault-share`, `ongoing-pol-share` and `ongoing-team-share`; §11 now explicitly routes the POL share to buybacks held in the Incentives Vault. Section15 retains historical “POL liquidity” launch wording; use the specific current §11 explanation for the documented destination. Section12 allows bounded tuning, so current percentages require live reads. [sr-whitepaper-v1: policy, reserves, immutables, parameters]

The published launch rule in `launch-trading-tax-curve` describes opening taxes decaying to the steady buy/sell floors. Read fresh tax getters rather than treating launch values as current fees; unavailable reads leave current fees unknown. The canonical pool's LP fee is separate; transaction-specific fee bases and computation order require separate evidence. Protocol-position STANDARD fees are burned under the published design. [sr-whitepaper-v1: currency, reserves, parameters]

Outside liquidity opens after the launch schedule reaches its floors. The publisher says withdrawn ETH principal is taxed at the sell rate and STANDARD principal at the buy rate; accrued LP fees are untaxed. See `outside-liquidity-tax-policy`. Requested liquidity-return calculations may use these rules with stated fee, price and liquidity assumptions under [modeling boundaries](risks.md#what-economics-alone-cannot-establish), not as guaranteed proceeds. [sr-whitepaper-v1: reserves]

**Official v1.1 policy:** [the announcement](updates.md#protocol-v11-announced-changes) confirms bid-side-only incremental POL. The publisher **POL Buyback** purchases tokens on-market and sends them to the **Incentives Vault**, where they remain unburned for future distribution (`pol-routing-policy`). The old frontend `polManager` is now **Genesis Liquidity Manager**, not the asserted current Registry `POL_MANAGER` destination; historical registry evidence separately routes that key to the new buyback. Refresh current routing rather than treating that event as perpetual state. The earlier proposed 50/50 branch-payment burn/incentive split and incentive allocation restrictions are **not confirmed**; do not apply them to license payments, Contraction Vault buybacks or exit fees.

## Reserve assets and ownership

Expansion accumulates ETH and purchases tokenized gold and comparable assets. Reserves are protocol property and are not redeemable by charter holders. Sources do not authenticate reserve issuers, custody/redemption terms, balances, valuation policy or purchase venues. Reserve accumulation is neither evidence of holdings nor a fixed peg or guaranteed price floor. ExpansionVault reserve purchases remain owner-only even if the separate execution switch is opened. [sr-whitepaper-v1: reserves, immutables, disclaimer]

The whitepaper describes genesis liquidity as non-withdrawable and says those positions remain in place, no longer receiving new liquidity from the POL share; the original manager continues collecting LP fees. These are publisher custody/continuity claims, not independently verified positions or permissions, and do not establish equivalent restrictions over bought-back Incentives Vault tokens. A banker withdrawing tokens is not withdrawing the protocol's LP position; historical idle-asset movement is not proof that every LP position migrated. [sr-whitepaper-v1: currency, reserves; sr-v1-1-deployment-evidence]

Authoritative ownership/authority records: `reserve-redemption-policy`, `pol-withdrawal-policy`, `expansion-reserve-purchase-policy`.

For current routing/liability and vault observations use `snapshot.py treasury`. An explicitly specified `--asset ADDRESS` is checked with `isReserveAsset` before Expansion Vault holdings/pool calls; approved holdings remain raw token units without independently authenticated decimals, not a complete portfolio. The fixed authenticated STANDARD `balanceOf(incentivesVault)` provides the separately requested token balance, while generic owner/pending-owner reads provide bounded control context. These do not invent complete POL Buyback/Incentives Vault ABIs or establish incentive distribution privileges. Every balance and owner is read live, never filled from review snapshots.

`history.py buybacks` reports Contraction Vault `BuybackExecuted(uint256,uint256)` ETH/ STANDARD burned-token event accounting. **`history.py pol-buybacks` is separate**: POL Buyback `BuybackExecuted(uint256,uint256,address)` reports ETH input, raw `tokensOut` and destination. The POL event alone does not authenticate token identity/decimals, burn accounting or wallet movements, so no guessed token-binding getter or normalized token amount is added. Neither mode is aggregate burn history or independent receipt/transfer reconciliation. [Inspection](inspection.md#common-question-paths) and [history](auction-history.md) retain those boundaries.

The publisher-linked ABIs contain successor holdings-migration entries for both vaults and FeeSplitter. Asset movement to a successor is distinct from changing deployed code; whitepaper non-upgradeability language is not a blanket proof that holdings can never move between components. The ABI alone establishes neither deployment correspondence nor who can move what, registry replacement rules or present authority. Keep these as implementation questions, not custody assurances; requested migration explanations or unsigned preparation follow [safety](safety.md), without signing or submission. [sr-contract-directory; contracts](contracts.md)

The [Second Mandate](updates.md#second-mandate-liquidity-for-tokenized-stocks) proposes seeding tokenized-stock markets, coordinating external capital and returning trading fees to the Reserve for further markets. It establishes neither a new ongoing ETH split nor deployed positions or holder revenue rights. Its reserve-position panel is explicitly sample content; the separate “as of today” graphic uses fixed values in the reviewed component, not live observations. Fresh retrieval alone does not establish holdings. Keep this strategy separate from whitepaper accounting and the specific official v1.1 POL change. [sr-second-mandate-manifesto]

## Contraction execution

The **Contraction Vault**, distinct from POL Buyback, buys STANDARD on-market and burns purchases under the whitepaper rule (`buyback-burn-share`). Retained Incentives Vault tokens must never be counted as these burns. For vault balance V and pool reserves R, the whitepaper rule is:

spend_tick = min(a × V, b × R)

Here a = `buyback-vault-fraction`, b = `buyback-pool-fraction`, and cadence = `buyback-tick`. Commensurate denominations and the exact measurement of R still need implementation evidence for deployed calculations; a source-rule model may instead state its denomination and pool-depth assumptions. `buyback-daily-depth-bound` is an approximate source description, not a fixed daily budget. Unspent balance rolls forward and the vault is described as unable to sell. [sr-whitepaper-v1: reserves equation 11.1]

`buyback-spend-formula` stores this source-only formula; `vault-execution-enablement` separately records who may execute it.

The current whitepaper describes contraction-buyback and POL-buyback execution as initially owner-cranked, with a one-way permissionless switch, and an optional guardian pausing auctions/vault purchases rather than withdrawals. These are publisher rules, not a complete source-reviewed permission model for POL Buyback or the Incentives Vault. An administrative SafeProxy dependency, component replacement or successor asset movement does not prove proxy-upgradeable monetary modules; non-upgradeability likewise does not eliminate privileged controls. [sr-whitepaper-v1: immutables; sr-protocol-control-dependencies]

## Accounting boundaries

Keep founding proceeds, ongoing auction receipts, LP fees, protocol taxes, accrued issuance, wallet mints, deposit conversions, ledger removals, redistribution, reserve holdings and buyback spend separate. A reserve purchase is not banker income; a deposit conversion is not a permanent burn; a documented allocation is not an observed transfer. [Contracts](contracts.md) routes identity provenance and fresh verification; [risks](risks.md) identifies evidence boundaries.

The official conditions page's Treasury & controls section reports native ETH vault balances and explicitly does not index reserve-token holdings. Its fee-routing direction is provisional until settlement and uses a different window from issuance policy. Neither a partial ETH display nor the combined “Burned forever” cap-reduction label proves a complete reserve portfolio or cumulative buyback spend. [sr-protocol-conditions; inspection](inspection.md#supply-restrictions-and-control-context)
