# Supply, flow and issuance policy

Publisher design: `sr-whitepaper-v1` §§3–5,12,15; [source index](../assets/sources.json). Exact settings and provenance: [monetary parameters](../assets/parameters/monetary.json); removal shares: [participation](../assets/parameters/participation.json) and [reserves](../assets/parameters/reserves.json).

## Currency and supply — §3

Canonical settings: `hard-cap`, `token-decimals`, `genesis-liquidity`, `issuance-budget`. Genesis is the only pre-mint: protocol-owned liquidity single-sided above the owner-set launch price, with no upper price ceiling and described as non-withdrawable. The original issuance budget is not a measured remaining balance. On exhausting cumulative issuance budget, base issuance stops permanently; the publisher describes closed-loop recycling thereafter. Burns do not reopen that cumulative budget. [sr-whitepaper-v1: currency, reserves]

Issuance first credits internal ledger balances; actual tokens are minted on withdrawal. Permanent value removals differ from conversions:

- License payments and the burned halves of resolution/revocation fees remove ledger value that is never minted.
- Open-market buybacks and the protocol position's token-side fees permanently burn wallet/pool tokens.
- Deposits destroy tokens but credit the ledger one-for-one; that value remains re-mintable on withdrawal. A deposit conversion is not a permanent economic burn.

With G = `genesis-liquidity`, H = `hard-cap`, M(t) cumulative withdrawal mints, B(t) permanent token burns, C(t) deposit conversions and R(t) permanent ledger removals, the published identities are:

- S_circ(t) = G + M(t) − B(t) − C(t).
- S_max(t) = H − B(t) − R(t).

The publisher calls the first quantity circulating supply, including genesis pool tokens. It says public burns and ledger removals lower the mintable ceiling, while the CentralBank deposit-conversion path is exempt; minted supply plus outstanding bank obligations must fit under that ceiling. These are source claims, not authenticated getter semantics or a substitute for implementation accounting. [sr-whitepaper-v1: currency equations 3.1–3.2]

Canonical accounting records: `circulating-supply-formula`, `mintable-ceiling-formula`, `deposit-ledger-conversion`. Formula strings describe the source, not verified callable code.

## Flow signal and policy — §§4–5

F_n = gross ETH entering through buys − gross ETH leaving through sells in epoch n. Issuance policy uses the trailing `signal-lookback` completed epochs; fee routing uses the sign of current F_n. Positive current flow means expansion; negative or zero means contraction. A current contraction-routing regime does not itself establish a negative trailing policy signal. The claim that capital-based measurement resists manipulation is an argument, not a demonstrated security result. [sr-whitepaper-v1: net-flow, policy]

The documented launch base (`base-issuance`) is **700,000 STANDARD/day before the multiplier**, not an already-scaled rate. The owner may lower it for the next epoch but never raise it back. For d days, base rate r and multiplier m_n, epoch issuance is I_n = r × d × m_n. A branch's daily-equivalent share is r × m / N while total branches N and other inputs stay fixed. Accrual streams second by second; a new branch earns from opening. [sr-whitepaper-v1: policy equations 5.1–5.2, branches]

`base-issuance-owner-policy` records the ratchet and effective-epoch claim. `time-to-full-issue` means opening at the full base rate, not time to exhaust the original issuance budget.

The source now publishes `multiplier-floor`, `multiplier-ceiling`, `multiplier-launch`, `epoch-length`, `rate-cut`, `rate-raise` and `multiplier-update-rule`: a negative trailing signal cuts toward the floor; a positive signal sustained for the qualifying consecutive epochs raises toward the ceiling; otherwise the multiplier holds. The rate changes are additive multiplier steps, not percentage changes. Timing/dilution illustrations (`time-to-full-issue`, `time-to-multiplier-ceiling`, `time-ceiling-to-floor`, `ceiling-to-floor-dilution-cut`) retain their source meanings and limits rather than becoming forecasts. The frontend's `frontend-policy-range` remains a separate earlier presentation. [sr-whitepaper-v1: policy; sr-protocol]

These published formulas do not establish code correspondence, epoch-boundary rounding or future pool flows. A future multiplier path remains a scenario assumption; no executable dynamic-policy algorithm is authorized by this overview alone. [Risks](risks.md) covers bounded owner controls; [contracts](contracts.md) covers implementation limits.
