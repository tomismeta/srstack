# TaxHook interface discovery

[Inventory scope](interface-inventory.md) · [Capabilities](capabilities.md) · [Restriction distinctions](interface-guide.md#restrictions)

[tax-hook.json](../assets/interfaces/tax-hook.json) preserves all 80 publisher declarations, including constructor schedule tuple, payable receive, callback tuple inputs, flow/oracle reads, setters, events and errors. This is the Trading Hook role, not a complete ABI for shared PoolManager infrastructure.

## Taxes and restrictions

`currentTaxBps(bool isBuy)` is called with true for buy and false for sell by the publisher. `buyTaxBps()`/`sellTaxBps()`, decay-start/floor rates, `taxHalfLife()`, `taxDecayStart()`, `taxDecayDuration()` and `taxOverridden()` are separate fields. Do not infer a schedule's active state from the current rate alone.

`launchScheduleActive()` has separately reviewed dated source semantics: override deactivates the schedule; otherwise start zero is active, and a started schedule is active before start plus duration. Authenticate deployment correspondence before applying this. STANDARD's holding-cap enabled flag, resolved active result and PoolManager gate remain independent.

## Pool, flow and oracle fields

`poolKey()` and `canonicalPoolKey()` preserve currency0/currency1, raw uint24 fee, signed tick spacing and hooks. A shared PoolManager address is not a unique pool. Currency order and fee flags require their own interpretation; do not assign all uint24 values basis-point units.

`epochNetFlow`, `settledNetFlow`, `settledTaxes`, `epochBoundary`, window-start checkpoints and signed tick cumulatives are raw research inputs, not token balances or a proved bank earnings formula. `currentTick`, `lastTick`, `lastTickTime`, `twapTick` and `withinDeviation` do not themselves establish oracle freshness, resistance to manipulation or swap/buyback success.

`takeEpochNetFlow` is state-changing: its getter-like name must not turn it into an assumed public read. `openEpochWindow`, `forwardTaxes` and setters likewise retain exact mutability in the data. Flow-consumption and tax-forwarding events are distinct accounting observations.

## Callbacks and dynamic data

Before/after liquidity and swap callbacks preserve complete nested pool/action tuples and signed delta types. These are callback entrypoints, not user-facing read methods. Caller constraints, currency order, delta signs, settlement and return flags require implementation evidence. `unlockCallback(bytes)` is a dynamic bytes input/output, not a single fixed data word.

The full event layouts distinguish indexed sender/recipient addresses from data. `EpochWindowClosed` is a hook measurement-window event, not an auction-end event; `LpTaxCollected` separates ETH and token amounts. ABI completeness here does not authenticate every transfer, implementation branch, dependency or currently authorized caller.
