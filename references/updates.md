# Current updates

For the current recap, use [latest summary evidence](../assets/sources/live-interface.json), especially `sr-latest-summary`, `sr-recap-trading`, `sr-recap-bootstrapping` and `sr-recap-licenses`.

The [official September 15 recap](https://x.com/standard_rsv/status/2099915418010046574) reports a sold-out founding launch, broad charter ownership, token-holder growth, liquidity and vault bootstrapping. Attribute recap numbers to the team; they are not live counters. Keep the answer short and link the post rather than printing a provenance table.

The team says **12-hour auctions are being considered**. That is not an implemented duration. Use `scripts/snapshot.py` with the `auctions` view to read the current auction-day length, availability and prices. Sold-out closing prices and current price-function outputs are not interchangeable purchase quotes.

For current issuance, taxes and supply, use the `protocol` snapshot. For a selected public charter, use the `charter` view with its ID. The helper reads a fixed publisher ABI at one block; it does not execute trades or reproduce the entire implementation.

Use [documents](documents.md) for current written rules, [contracts](contracts.md) for identities, and [planning](planning.md) to turn selected observations into approved assumptions. No automatic monitoring or source updates.
