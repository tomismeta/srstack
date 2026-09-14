# Ongoing charter and license auctions

Sources: [website core](../assets/sources/website-core.json), `sr-whitepaper` §§6–8. Exact settings: [participation parameters](../assets/parameters/participation.json). These are daily post-genesis mechanics, not the [genesis auction](launch-mint.md).

## Ongoing auctions — §§7–8

The documented daily auctions execute immediately at the current falling price, first come first served, with no bids, escrow or refunds. The day closes on sellout or `auction-duration`; unsold capacity does not roll over. Unpurchased charters are never minted. The last sold price becomes the reference for the next open. [sr-whitepaper: auctions]

- **License:** $STANDARD payment is burned. Initial daily supply is `licenses-per-day`; charter daily purchase cap is `licenses-per-charter-per-day`. Opening price is `license-open-multiple` times the previous closing sale, or that multiple of the floor if nothing sold.
- **Post-genesis charter:** ETH payment enters the ongoing fee engine; the NFT and its first branch arrive in the purchase transaction. Opening multiple is `charter-open-multiple`; the floor is an admin-set reserve price with no visible numeric value (`charter-reserve-price`). Daily supply starts at `initial-daily-charter-count` and is policy-controlled (`charter-count-policy`).

For this daily mechanism, P(t) = P_start × (P_floor / P_start)^(t/T), T = `auction-duration`, with t and T in matching units. The license floor is described approximately by `license-floor-yield-days`, but its exact issuance/branch-count formula is hidden (`license-floor-formula`). The §7 table also hides its decay setting (`license-decay-setting`) even though the exponential interpolation is visible. Do not reconstruct the concealed rule from the approximate yield description. [sr-whitepaper: branches equation 7.1; auctions]

The publisher explains early purchase as paying more for allocation certainty versus waiting and risking sellout. It describes license prices ratcheting upward under sustained demand by the opening multiple, and charter prices repricing faster because of their different multiple. The illustrative `license-repricing-week-multiple` is not a guaranteed gain or market outcome. §8 reveals several values whose §7 entries remain redacted; that uneven disclosure is retained in the parameter limits. Five after-genesis redacted spans in §6 have no visible labels (`post-genesis-charter-redactions`), so their individual meanings cannot be assigned. [sr-whitepaper: charters, branches, auctions]

Credit-versus-wallet-token spending/burn accounting remains unresolved: [conflicts](risk-conflicts.md).
