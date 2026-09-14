# Fees, reserves and defense

Publisher accounting, not observed holdings or deployed restrictions. Current source: [v1 sources](../assets/sources/website-v1.json), `sr-whitepaper-v1` §§3,6,11–12,15. Exact settings: [reserve parameters](../assets/parameters/reserves.json), [launch parameters](../assets/parameters/launch.json).

## Founding funding is not the ongoing fee split

Founding proceeds escrow until finalization. The owner sets launch price; finalization launches the pool and starts the tax clock and epoch-one emissions in one described atomic transaction. The genesis token allocation is single-sided above launch price with no upper price ceiling. The first 25 ETH of accepted proceeds forms a floor bid below that price; the remaining proceeds split 60% to a protocol-held POL pairing reserve, 20% to contraction and 20% to expansion. There is no founding team share. Canonical records: `genesis-liquidity-vault-split`, `genesis-protocol-proceeds-share`, `genesis-team-proceeds-share`. [sr-whitepaper-v1: currency, charters, reserves, parameters]

Allocation components: `founding-floor-bid`, `founding-pol-remainder-share`, `founding-contraction-remainder-share`, `founding-expansion-remainder-share`. The remainder percentages must not be applied to gross receipts.

Current §11 now expressly separates this founding allocation from steady-state trading/charter-auction receipts. The earlier §6/§11 blanket-routing wording tension belongs to dated `sr-whitepaper`, not an unresolved absence of the founding split today. Do not use the ongoing fee percentages for founding proceeds. [sr-whitepaper: charters, reserves; sr-whitepaper-v1: reserves]

## Ongoing ETH routing — §11

Current net flow selects the active vault: expansion when positive, contraction otherwise. Shares are `ongoing-active-vault-share`, `ongoing-pol-share`, `ongoing-team-share`. Of the POL allocation, `pol-swap-share` is swapped to STANDARD, paired with remaining ETH and added as permanent liquidity. “No insider allocation” in About is not a claim that the team receives no ongoing fees. §12 also allows bounded owner changes to fee splits. [sr-whitepaper-v1: policy, reserves, immutables; sr-about; sr-app-about]

The current whitepaper publishes steady buy/sell taxes, but contradicts itself on launch opening rates; [launch trading](launch-trading.md) preserves the distinction. The canonical pool's LP fee and tick spacing are separate from protocol taxes. The token companion explicitly says taxes apply **on top of** the LP fee; it does not establish the precise computation order or fee base. The protocol position's fees earned in STANDARD are burned (`standard-trading-fee-burn-share`). ETH diagrams do not supersede that token-side statement. [sr-whitepaper-v1: currency, reserves, parameters; sr-token-page-v1]

## Reserve assets and ownership

Expansion accumulates ETH and purchases tokenized gold and comparable assets. Reserves are protocol property and are not redeemable by charter holders. Sources do not authenticate reserve issuers, custody/redemption terms, balances, valuation policy or purchase venues. Reserve accumulation is neither evidence of holdings nor a fixed peg or guaranteed price floor. ExpansionVault reserve purchases remain owner-only even if the separate execution switch is opened. [sr-whitepaper-v1: reserves, immutables, disclaimer]

Genesis liquidity and subsequent POL additions are described as permanent/non-withdrawable. Those restrictions are not verified deployed permissions or a guarantee of ETH exit value. A banker withdrawing tokens is not withdrawing the protocol's LP position. [sr-whitepaper-v1: currency, reserves]

Authoritative ownership/authority records: `reserve-redemption-policy`, `pol-withdrawal-policy`, `expansion-reserve-purchase-policy`.

## Contraction execution

Contraction buys STANDARD on-market and burns all purchases (`buyback-burn-share`). For vault balance V and pool reserves R, the published rule is:

spend_tick = min(a × V, b × R)

Here a = `buyback-vault-fraction`, b = `buyback-pool-fraction`, and cadence = `buyback-tick`. Commensurate denominations and the exact measurement of R still need implementation evidence. `buyback-daily-depth-bound` is an approximate source description, not a fixed daily budget. Unspent balance rolls forward and the vault is described as unable to sell. [sr-whitepaper-v1: reserves equation 11.1]

`buyback-spend-formula` stores this source-only formula; `vault-execution-enablement` separately records who may execute it.

Contraction-buyback/POL-pairing execution starts owner-cranked; the owner can make it permissionless through a one-way switch. Optional guardian pauses cover auctions and vault purchases, not withdrawals. Non-upgradeability does not imply autonomous execution or absent operational controls. [sr-whitepaper-v1: immutables]

## Accounting boundaries

Keep founding proceeds, ongoing auction receipts, LP fees, protocol taxes, accrued issuance, wallet mints, deposit conversions, ledger removals, redistribution, reserve holdings and buyback spend separate. A reserve purchase is not banker income; a deposit conversion is not a permanent burn; an announced allocation is not an observed transfer. [Contracts](contracts.md) retains the separately added deployment/condition evidence and implementation limits; [conflicts](risk-conflicts.md) identifies unresolved source discrepancies.
