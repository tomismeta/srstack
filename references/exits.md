# Exits, dormancy and transfers

Sources: [website core](../assets/sources/website-core.json), `sr-whitepaper` §§9–10,12. Exact values and explicit unknowns: [participation parameters](../assets/parameters/participation.json).

## Earning, withdrawal and resolution fees — §9

For accrued balance A and b branches held before retirement, retiring k branches releases A × k/b before the resolution fee, with corresponding earning capacity removed. Wallet tokens are minted on withdrawal, net of the fee. This pro-rata relation is a design description; implementation rounding is not given. [sr-whitepaper: exits]

Exit pressure uses W, system-wide tokens withdrawn over `exit-lookback`, and D, balances still held at the bank: P = W / max(D + W, E), where E = `exit-pressure-denominator-floor` is redacted. The fee is described as quadratic between `resolution-fee-floor` and `resolution-fee-ceiling`, saturating at `exit-saturation-pressure`; `resolution-fee-formula` and the quiet/elevated/heavy/bank-run pressure/fee pairs remain redacted. Without them no exact withdrawal quote is supported. [sr-whitepaper: exits equation 9.1]

The publisher says the fee rate locks at commitment and withdrawals are never paused or queued. The resolution fee itself—not the gross released balance—is split by `resolution-burn-share` and `resolution-redistribution-share` between burn and remaining bankers. Commitment mechanics and redistribution implementation are not specified. This is the claimed incentive response to crowded exits, not proof that remaining is profitable or that withdrawals always work in deployed code. [sr-whitepaper: exits]

## Dormancy and transferability — §§10,12

Anyone may report a wallet inactive for `dormancy-period`. The informant bounty is `dormancy-bounty-share`, capped by `dormancy-bounty-cap`. Revocation charges `dormancy-revocation-fee`; the stated remainder (`dormancy-remainder-share`) goes to the dormant wallet. The fee burns/redistributes according to `dormancy-fee-burn-share` and `dormancy-fee-redistribution-share`; branches close and the NFT burns. The source does not specify how the bounty is funded or its deduction order relative to that fee/remainder split. [sr-whitepaper: dormancy]

The publisher says any interaction resets inactivity and a zero-cost check-in exists (`check-in-protocol-cost`); this does not establish free network gas. Exact qualifying interactions require implementation evidence. [sr-whitepaper: dormancy]

A future one-way switch is described as enabling NFT transfers, moving branches and balance together. The publisher characterizes such a seat sale as an exit without directly selling $STANDARD. Transfers are not stated to be active at launch, and controller/date are unknown (`transfer-enablement`). No secondary-market availability or price is established. [sr-whitepaper: transfers]

See [reserves](reserves.md) for proceeds ownership and [risks](risks.md) for source and implementation limits.
