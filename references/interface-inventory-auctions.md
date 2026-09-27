# Auction interface discovery

[Inventory scope](interface-inventory.md) · [Capability map](capabilities.md) · [Question-driven auction inputs](interface-guide.md#auction-state)

## Separate families and generations

| Family / generation | Full publisher definition | Key distinction |
| --- | --- | --- |
| Branch-license / original | [license-auction-original](../assets/interfaces/license-auction-original.json) | `AUCTION_DAY()`, per-charter/day cap and usage |
| Branch-license / v1.1 | [license-auction-v1-1](../assets/interfaces/license-auction-v1-1.json) | Explicit `jc` filtering plus window declarations; constructor intentionally absent |
| Branch-license / v1.2 | [license-auction-v1-2](../assets/interfaces/license-auction-v1-2.json) | Window allowance plus charter-keyed bid entrypoints/events |
| New-charter / original | [charter-auction-original](../assets/interfaces/charter-auction-original.json) | Independent ETH-priced charter sale, original duration getter |
| New-charter / v1.2 | [charter-auction-v1-2](../assets/interfaces/charter-auction-v1-2.json) | Independent `auctionPeriod()` and constructor argument |

The reviewed v1.1 mapping identifies no separate charter replacement. Historical records retain original charter evidence rather than inventing a v1.1 address. `DECAY_HALF_LIFE_MAX()` is removed from newer auction definitions; no guessed replacement is supplied.

Branch licenses expand existing charters using publisher STANDARD18 ledger denomination. Charter auctions acquire new charters with publisher ETH-wei prices. Authenticate each family's target, generation, schedule, capacity, floor, multiplier, funds, inventory and permissions independently. Matching getter names never merge their economics.

## Reads and scoped absences

Current/stored round inputs include `auctionAnchor()`, period, `currentDay()`, `dayStartPrice()`, `dayFloorPrice()`, `dayHalfLife()`, `dayCap()`, `soldToday()`, `remainingToday()`, `lastSaleDay()` and `lastSalePrice()`. Price output or `quote(uint256)` does not prove buyable inventory. The `Day` spelling is not a 24-hour guarantee.

Original `purchasedOnDay(uint256 charterId,uint256 day)` and newer `purchasedInWindow(uint256 charterId,uint256 window)` are **available keyed usage reads**. They do not supply aggregate auction price/volume history; historical retention and reset behavior are unverified. License `capWindow()` is separate from auction period, and charter allowance is distinct from global inventory and bank branch capacity.

The five complete reviewed publisher auction definitions contain no `daySold(uint256)`, `dayPrice(uint256)` or `dayAnchorTime()`, no declared historical period-policy getter, and no event named `SoldOut` or `AuctionEnded`. These are bounded publisher-definition absences, not claims about every deployed capability. For aggregate history, combine authenticated purchase/configuration/roll logs with coverage-qualified historical state and effective settings; never substitute latest for unavailable old-block state.

## Orders and event decoding

Only v1.2 license declares `openBidCount()`, `openBids(uint256,uint256)`, `bids(uint256)`, `fillable(uint256)`, placement/cancellation/fill/pruning methods and bid events. `openBids` returns dynamic raw IDs. `bids`/`fillable` explicitly take charterId; the raw-page join, ordering, pagination stability, escrow/refunds, expiry and priority remain unestablished. No separate orderbook deployment is invented.

Use the full `abi` or explicit indexed `declaration`, not the canonical signature alone:

```solidity
event LicensesPurchased(uint256 indexed charterId, uint256 indexed day, uint256 count, uint256 unitPrice)
event CharterPurchased(uint256 indexed charterId, address indexed buyer, uint256 indexed day, uint256 price)
event DayRolled(uint256 indexed day, uint256 startPrice, uint256 floorPrice, uint256 cap)
```

License consideration is reported count × unitPrice; charter price is a separate ETH sale field. Neither submitted limits nor transaction value necessarily equal settled consideration. `DayRolled` has no timestamp, duration or end reason. Bid/core supporting logs in the same receipt are not extra purchases. Family, chain, emitter and round jointly identify history.
