# Supply, flow and issuance policy

Publisher design: [core source records](../assets/sources/website-core.json), `sr-whitepaper` §§3–5. Exact settings: [monetary parameters](../assets/parameters/monetary.json); burn shares: [participation](../assets/parameters/participation.json) and [reserves](../assets/parameters/reserves.json).

## Currency and supply — §3

Canonical settings: `hard-cap`, `token-decimals`, `genesis-liquidity`, `issuance-budget`. The genesis liquidity allocation is the only stated pre-mint, placed full-range in a protocol-owned position described as non-withdrawable. Subsequent issuance first increases internal ledger balances; actual tokens are minted at withdrawal. On exhausting cumulative issuance budget, base issuance stops permanently; the publisher describes subsequent operation as closed-loop recycling of fees. Burned supply does not reopen that stated cumulative budget. [sr-whitepaper: currency]

Using G = `genesis-liquidity`, C = `hard-cap`, M(t) = cumulative withdrawal mints and B(t) = cumulative burns, the published accounting is:

- S_circ(t) = G + M(t) − B(t).
- S_max(t) = C − B(t).

The publisher calls the first quantity circulating supply, including genesis pool tokens. Do not silently replace that definition with a data provider's free-float measure. Internal accrued balances are not already wallet token supply. Burn mechanisms are license payments, purchased buybacks and the burned component of resolution fees; canonical shares are `license-burn-share`, `buyback-burn-share`, `resolution-burn-share`. Exact implementation accounting requires authenticated contracts, not just these identities. [sr-whitepaper: currency; see contracts.md via the link below]

## Flow signal and policy — §§4–5

The hook measures F_n = gross ETH entering from buys − gross ETH leaving from sells during epoch n. Policy uses the sum of F over the trailing `signal-lookback` completed epochs; fee routing instead uses the sign of current F_n. Expansion means positive current net flow; negative **or zero** means contraction. This separates a lagged issuance decision from current-regime routing. The whitepaper's assertion that capital must move to affect the signal is a design argument, not a demonstrated manipulation-resistance result. Its claim that trading is the only entry/exit point concerns the pool signal, not all protocol receipts: charter auctions also bring ETH. [sr-whitepaper: net-flow, policy]

Symbolically, issuance for an epoch of d days is I_n = r × d × m_n, with r = `base-issuance`. A branch in a system of N branches has instantaneous daily-equivalent share r × m / N while those inputs stay fixed. Accrual streams second by second and starts when a branch opens; changing branch counts or multiplier require interval-by-interval accounting, not a fixed-yield quote. [sr-whitepaper: policy, branches]

The publisher describes immediate cuts and earned/slower raises, a license floor that scales with the rate, reserve buying in expansion, and buyback defense in contraction. Missing policy settings include `multiplier-floor`, `multiplier-ceiling`, `multiplier-launch`, `epoch-length`, `rate-cut`, `rate-raise`, `multiplier-update-rule`, `time-to-full-issue`, `time-to-multiplier-ceiling`, `time-ceiling-to-floor`, and `ceiling-to-floor-dilution-cut`. The qualitative story is visible; its quantitative transition rule is not. [sr-whitepaper: policy]

The separate frontend range is `frontend-policy-range` in monetary parameters; it does not unredact the whitepaper recurrence or establish an onchain multiplier. [sr-protocol]

See [protocol](protocol.md) for system flows and [contracts](contracts.md) for identity limits.
