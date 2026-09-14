# Exits, dormancy and transfers

Publisher design: [v1 sources](../assets/sources/website-v1.json), `sr-whitepaper-v1` §§9–10,12–13. Exact settings and limits: [participation parameters](../assets/parameters/participation.json).

## Earning, withdrawal and resolution fees — §9

For accrued balance A and b branches before retirement, retiring k branches releases A × k/b before the resolution fee and removes that earning capacity. Tokens are minted to the wallet net of the fee. Retiring every branch burns the charter. This pro-rata relation is a source description, not an implementation rounding/settlement algorithm. [sr-whitepaper-v1: exits]

The published pressure and fee formulas are now visible. W is system-wide tokens withdrawn over `exit-lookback`, D is everything still held at the bank, and E is `exit-pressure-denominator-floor`:

P = W / max(D + W, E)

fee = 0.02 + 0.58 × min(P / 0.10, 1)^2

The authoritative records are `resolution-fee-formula`, `resolution-fee-floor`, `resolution-fee-ceiling` and `exit-saturation-pressure`; the quiet/elevated/heavy/bank-run examples retain their approximate source status. The denominator floor is a STANDARD amount, not a branch count. These formulas alone do not establish when the current withdrawal enters W, which balance enters D, commitment sequencing, integer rounding or exact deployed payout. Do not turn them into an implementation-verified withdrawal algorithm. [sr-whitepaper-v1: exits equation 9.1]

The publisher says the rate locks at commitment. The fee—not gross released balance—is split by `resolution-burn-share` and `resolution-redistribution-share`; the burned part is permanently removed from the ledger, and the other part goes to remaining bankers. It says the contract exposes no withdrawal pause or queue at any fee level, while explicitly warning that independent settlement dependencies can still make a Bank call revert. These are source claims, not a guarantee of continuous withdrawal availability. [sr-whitepaper-v1: currency, exits]

## Dormancy — §10

Anyone may report a wallet inactive for `dormancy-period`. The bounty is `dormancy-bounty-share`, capped by `dormancy-bounty-cap`. Revocation charges `dormancy-revocation-fee`, split by `dormancy-fee-burn-share` and `dormancy-fee-redistribution-share`; the stated `dormancy-remainder-share` goes to the dormant wallet. Branches close and the NFT burns. Bounty funding and deduction order relative to that fee/remainder remain unspecified; no exact net-payout formula follows. [sr-whitepaper-v1: dormancy]

Qualifying wallet-clock resets are explicitly listed: creating a charter, buying a license, depositing, withdrawing, successfully reporting another dormant charter, and zero-cost check-in (`check-in-protocol-cost`). Zero protocol charge does not mean zero network gas. Sending or receiving a charter does **not** refresh either wallet; the transferred charter carries its own timestamp and receives a full dormancy-period grace window. Do not replace these distinctions with “any interaction resets inactivity.” [sr-whitepaper-v1: dormancy]

`dormancy-clock-reset-actions` and `dormancy-transfer-grace` preserve those separate rules. `withdrawal-retirement-rule` and `withdrawal-availability` record the withdrawal claims without supplying a verified settlement algorithm.

## Transferability — §§12–13

The owner may enable initially disabled charter transfers through a one-way switch (`transfer-enablement`). Thereafter the seat moves with branches and balance intact. The publisher calls a seat sale an exit without directly selling $STANDARD; no secondary-market availability or price is established. The whitepaper describes authority, not an observed enablement transaction. An optional guardian may pause auctions and vault purchases, **not withdrawals**; see [risks](risks.md). [sr-whitepaper-v1: immutables, transfers]
