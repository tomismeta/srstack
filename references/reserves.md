# Fees, reserves and defense

Scope: publisher-design accounting and announcements, not observed treasury holdings or deployed restrictions. Sources: [website core](../assets/sources/website-core.json), [About context](../assets/sources/website-context.json), [mint announcement](../assets/sources/launch-mint.json). Exact settings: [reserve parameters](../assets/parameters/reserves.json); genesis proceeds: [launch parameters](../assets/parameters/launch.json).

## Genesis funding is not the ongoing fee split

Current whitepaper §6 and the mint-details announcement allocate genesis mint proceeds to initial liquidity and protocol vaults, with no team share: `genesis-protocol-proceeds-share`, `genesis-team-proceeds-share`. The whitelist entry charge is `whitelist-liquidity-fee`; public-genesis auction economics are separate in [charters](charters.md). The division between genesis liquidity and the vaults is not disclosed (`genesis-liquidity-vault-split`). [sr-whitepaper: charters; sr-mint; sr-post-2098969964283846751]

Whitepaper §11 uses broader wording, “all protocol ETH,” including trading fees and charter auctions, for an active-vault/POL/team split. Preserve that wording tension: the current specific genesis destination must not silently be replaced by the ongoing fee-engine split. Post-genesis auction ETH is explicitly described as entering the fee engine. [sr-whitepaper: charters, reserves]

## Ongoing ETH routing — §11

Each epoch's active vault is chosen from the sign of current net flow: expansion when positive, contraction otherwise. Canonical shares are `ongoing-active-vault-share`, `ongoing-pol-share`, `ongoing-team-share`. The POL allocation is partly swapped to $STANDARD (`pol-swap-share`), paired with the remaining ETH and added to liquidity described as permanent. The team receives its ongoing share; “no insider allocation” on About is not a claim of no fee revenue. [sr-whitepaper: policy, reserves; sr-about; sr-app-about]

Both buy and sell activity are described as producing ETH fees, but the regular `trading-fee` setting is redacted. The whitepaper separately says trading fees earned in $STANDARD are burned (`standard-trading-fee-burn-share`). That statement should not be discarded because the simplified flow diagrams show ETH fees; exact hook accounting and token-denominated fee handling need implementation evidence. [sr-whitepaper: entities, reserves, parameters]

## Reserve assets and ownership

The expansion vault accumulates ETH and purchases tokenized gold and comparable hard assets. The bank, not the charter holder, is described as holding these reserves. The sources do not identify authenticated reserve assets, issuers, custody/redemption terms, current balances, valuation policy, purchase venues or an individual charter redemption right against reserves. Reserve accumulation is a stated mechanism, not proof of holdings, a fixed exchange-rate peg or a guaranteed token-price floor. [sr-whitepaper: reserves]

Genesis liquidity is described as full-range and protocol-owned, with the position never withdrawable; later POL additions are described as permanent. These are ownership/constraint claims, not verified deployed permissions or a guarantee of a particular ETH exit value. Token withdrawal by a banker is distinct from withdrawing the protocol's LP position. [sr-whitepaper: currency, reserves]

## Contraction execution

The contraction vault buys $STANDARD on the market and burns the purchase (`buyback-burn-share`). For vault balance V and pool reserves R, the published tick rule is:

spend_tick = min(a × V, b × R)

Here a = `buyback-vault-fraction`, b = `buyback-pool-fraction`, and cadence = `buyback-tick`. Use commensurate denominations; the overview does not fully define the reserve measurement R. The prose's near-daily-depth figure is `buyback-daily-depth-bound`, an approximate description, not a constant daily budget. Unspent balance rolls forward and the vault is described as unable to sell. The publisher says rate-limited steps avoid a single baitable execution; that safety claim is not independently tested here. [sr-whitepaper: reserves equation 11.1]

## Temporary launch tax

[Launch trading](launch-trading.md) preserves the announced tax, body/image half-life tension and unspecified allocation/fee basis. Do not infer launch-tax routing from either genesis proceeds or the regular ETH split.

## Accounting boundaries

Keep swap fees, genesis receipts, post-genesis auction receipts, internal accrued issuance, wallet token mints, fee redistribution, reserve holdings, buyback spend and burns separate. A reserve purchase is not banker income; a token burn is not ETH proceeds; an announced allocation is not an observed transfer. Current holdings, burn totals and earned fees need authenticated identities, explicit time/block anchors and complete relevant event coverage. Use [contracts](contracts.md) and [research workflow](research-workflow.md); unresolved claims are in [risks](risks.md).
