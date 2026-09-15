# Current updates

On an update request, freshly read the [official account](https://x.com/standard_rsv), then open the latest relevant official posts. Answer the requested update first, with a post link and publication time. Attribute reported metrics and distinguish proposals from implemented changes. If fresh retrieval is unavailable or incomplete, say so; do not substitute a stored recap.

For current auction-day length, availability and prices, use `scripts/snapshot.py` with the `auctions` view. Sold-out closing prices and current price-function outputs are not interchangeable purchase quotes. Read current state rather than inferring implementation from an announcement.

For current issuance, taxes and supply, use the `protocol` snapshot. For a selected public charter, use the `charter` view with its ID. The helper reads a fixed publisher ABI at one block; it does not execute trades or reproduce the entire implementation.

Use [documents](documents.md) for published rules, [contracts](contracts.md) for identities, and [planning](planning.md) to turn freshly read observations into approved assumptions. Unavailable state remains unknown. No automatic monitoring or saved-state/source updates.
