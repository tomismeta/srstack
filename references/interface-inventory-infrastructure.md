# Infrastructure and incomplete role interfaces

[Inventory scope](interface-inventory.md) · [Capabilities](capabilities.md) · [Required review methodology](inventory-methodology.md)

## Publisher control fragment

[publisher-control-fragment.json](../assets/interfaces/publisher-control-fragment.json) contains exactly the three literal publisher declarations `owner()`, `pendingOwner()` and `executionPermissionless()`. This is **selective**, not a complete Registry or universal control ABI.

The publisher `CM` directory read binds owner/pendingOwner to roles marked owned in `_M`. It binds executionPermissionless **specifically to Registry**. [Dated bindings](../assets/entities/contracts.json) explicitly constrain `selected_functions`; do not transfer Registry's execution flag to Genesis Liquidity Manager, POL Buyback or Incentives Vault merely because they share the control fragment.

| Dated role | Available module evidence | Unknown broader scope |
| --- | --- | --- |
| Registry | Full address binding and the three selective control reads | Registry keys, setters, routing events, execution rules, full errors/constructor and implementation |
| Genesis Liquidity Manager (`polManager`) | Full address binding; owner/pendingOwner declarations | Position operations, fee collection, migration and complete ABI |
| POL Buyback | v1.1 address attribution; owner/pendingOwner declarations | Full acquisition/control interface; older event provenance is separate |
| Incentives Vault | v1.1 address attribution; owner/pendingOwner declarations | Distribution/claim/vesting/exit interface, if any, and complete implementation |
| Shared PoolManager | Dated identity in publisher mapping | No bound PoolManager ABI in this module; hook callbacks are not a substitute |

These gaps mean **unknown**, not “the contract cannot do it.” A retained-token balance or a publisher roadmap does not establish live claim/exit entrypoints. Fresh authenticated evidence may answer a question outside this module without changing the installed catalog.

## Multicall fragment

[multicall3-fragment.json](../assets/interfaces/multicall3-fragment.json) preserves the SDK's three declared functions: `aggregate3((address,bool,bytes)[])`, `getEthBalance(address)` and `getCurrentBlockTimestamp()`. The publisher binds timestamp reads to `contracts.multicall3`; the full three-entry fragment is preserved, not claimed as the deployed contract's complete ABI.

`aggregate3` retains nested dynamic call/return arrays and per-call failure flags. Targets/calldata remain untrusted until separately authenticated and authorized. Its payable declaration is not permission to send value, sign or submit. Native balance is wei; timestamp is Unix seconds. Batched reads only share an anchor when the host actually pins the same block.

## Discovery boundary

Shared infrastructure is not project-authored protocol merely because the official directory lists it. SDK ENS/DNS/signature/domain/generic ERC20 arrays without role bindings were classified but not promoted to protocol inventories. Complete fingerprints authenticate the reviewed source data, not future live acceptance. Imported modules outside this one body and every historical deployment are not claimed exhaustively mapped.
