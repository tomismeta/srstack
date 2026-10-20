# Launchpad role interfaces

**Reviewed 2026-10-19.** The two independently deployed generations coexist: `launch-2026-10-14` and `urc5-2026-10-19`. Each primary role array is preserved completely; two supplemental association interfaces retain one exact declaration apiece. All have **partial contract coverage**: `source_definition_complete: false` and `deployed_implementation_complete: false`. No factory/router/hook/curve union or auction-style adaptation is used. See [launchpad mechanics](launchpad.md), [capabilities](capabilities.md), [identity authentication](contracts.md#authenticate-the-requested-role), [dated bindings](../assets/entities/contracts.json) and [wallet boundaries](safety.md#preparation-and-wallet-boundary).

## Role and source coverage

[Review `publisher-ecosystem-2026-10-19`](../assets/interfaces/reviews.json) preserves the root → `mountApp-RNywHOZ_.js` → `LaunchpadDoc-j28NPSkX.js` chain in [launchpad sources](../assets/sources/launchpad.json). The main body is 1139855 UTF-8 bytes, SHA-256 `6f614bf7a6b1e51260100315752ac5a0ff31b272f7ecc696190e1d53d1d68b91`. Each JSON records the exact zero-based half-open declaration range, fragment hash, parent hash, role-use object and enclosing-function fingerprints. Static template/identifier/spread dependencies were resolved as data, never executed. Default nonindexed/nonanonymous ABI flags and empty unnamed parameters are made explicit without changing encoding.

All forty fresh explorer metadata/ABI requests were denied and stopped. Consequently there is no explorer ABI review. Factory/deployer/curve-implementation dependencies and creation observations retained from October19 research are explicitly attributed, not represented as freshly fetched explorer responses. A curve implementation address is **not a child curve’s storage**: authenticate the actual token/factory/child relationship and proxy target before applying a curve layout.

| Role / generation | Selected array and exact main-body range | Coverage |
| --- | --- | --- |
| [launch-factory-2026-10-19](../assets/interfaces/launch-factory-2026-10-19.json) | `zo` / `[613317,613813)` | 12 entries: 2 functions, 1 events, 9 errors; selected only |
| [launch-router-2026-10-19](../assets/interfaces/launch-router-2026-10-19.json) | `q2` / `[624060,624488)` | 26 entries: 2 functions, 0 events, 24 errors; selected only |
| [launch-hook-2026-10-19](../assets/interfaces/launch-hook-2026-10-19.json) | `qa` / `[615961,616570)` | 23 entries: 8 functions, 0 events, 15 errors; selected only |
| [launch-factory-2026-10-14](../assets/interfaces/launch-factory-2026-10-14.json) | `Wr` / `[632735,633775)` | 29 entries: 3 functions, 2 events, 24 errors; selected only |
| [launch-factory-association-2026-10-14](../assets/interfaces/launch-factory-association-2026-10-14.json) | Single `ps` declaration / `[621837,621898)` | 1 view function; bound only to the earlier factory generation |
| [launch-factory-association-2026-10-19](../assets/interfaces/launch-factory-association-2026-10-19.json) | Same single declaration / `[621837,621898)` | 1 view function; separately bound to the newer factory generation |
| [launch-router-2026-10-14](../assets/interfaces/launch-router-2026-10-14.json) | `q2` / `[624060,624488)` | 26 entries: 2 functions, 0 events, 24 errors; selected only |
| [launch-config-2026-10-19](../assets/interfaces/launch-config-2026-10-19.json) | `L2` / `[615033,615369)` | 2 entries: 2 functions, 0 events, 0 errors; selected only |
| [creator-fee-escrow-2026-10-19](../assets/interfaces/creator-fee-escrow-2026-10-19.json) | `dR` / `[624496,624619)` | 26 entries: 2 functions, 0 events, 24 errors; selected only |
| [bonding-curve-2026-10-19](../assets/interfaces/bonding-curve-2026-10-19.json) | `Ah` / `[614080,614306)` | 5 entries: 5 functions, 0 events, 0 errors; selected only |
| [bonding-curve-2026-10-14](../assets/interfaces/bonding-curve-2026-10-14.json) | `ui` / `[622757,623436)` | 38 entries: 14 functions, 0 events, 24 errors; selected only |
| [creator-fee-escrow-2026-10-14](../assets/interfaces/creator-fee-escrow-2026-10-14.json) | `dR` / `[624496,624619)` | 26 entries: 2 functions, 0 events, 24 errors; selected only |
| `launch-hook-2026-10-14` | No acquired role ABI | Identity-only binding; callbacks, fees and authority remain unknown |
| `launch-token-deployer-2026-10-14` and `launch-token-deployer-2026-10-19` | No acquired role ABI | Identity-only bindings; no token ABI or module deployment is inferred |

Both [charter-drop interfaces](interface-inventory-charter-distributions.md) have their own role files. The stock SessionFeeHook has a separate October20 full-ABI review in the [stock-market inventory](interface-inventory-stock-markets.md); it is not one of these launch hooks. The reward Safe remains identity-only, not a reviewed reward-distributor interface.

## Primary arrays are not every frontend call

The common `ps` array at `[621644,622749)` includes `curveOfToken(address)`, `feeEscrow()` and `pairAsset(address)`, but its legacy launch/event/config tuples differ from primary `Wr` and `zo`. Only the exact `curveOfToken(address token) view returns (address)` declaration is installed as two supplemental generation-bound interfaces. The retained `FR(e)` fingerprint shows use across `di()` factories; the `OR(q)`/`di()` fingerprint includes current and `earlierLaunchpads` enumeration. This authenticates a point-read layout without merging the full common array or supplying an unobserved `isCurve` declaration. Refresh dated factory identity, query relevant generations, and corroborate child code/proxy relationships. Log-based discovery remains separately bounded; it is not required merely to encode this point read.

Likewise common `ui` is used for curve reads across generations, while the new-only primary `Ah` is retained separately here. The common/earlier `fn` drop array and new `D2` disagree on `drops(address)` output arity. They must never be combined by selector or function name. The publisher’s selected arrays provide no complete quote engine: retained router buy/sell functions are transactions, and local curve approximations are not deployed integer arithmetic. Obtain an independently authenticated quote interface or labelled simulation where needed; lifecycle reads and receipt evidence remain useful without an exact quote.

## Functions, layouts and units

Exact recursive tuple components, widths, mutability and selectors are in each JSON. The following is the full selected function inventory, not an action menu. Only `view`/`pure` entries are direct getters; listing a payable/nonpayable entry does not authorize transaction preparation.

### Supplemental factory association fragments

Both generation-bound fragments expose `curveOfToken(address)` (`view`, selector `0x923f533f`): one input token address and one returned curve-address ABI word. Zero means no association in that factory under the publisher callsite, not proof that no other generation knows the token. The declaration fingerprint is `55abd542344ae7d913cffa1e1e53ffb1bc5e869ab792c45feed983dfea9b1c82`; each file retains parent, callsite and generation-dispatch fingerprints. No other `ps` entry is included.

### `launch-factory-2026-10-19`

| Signature | Mutability / bounded interpretation |
| --- | --- |
| `config()` | `view` — Read the configured Config address; this is not evidence that the factory can replace its immutable Config address or that Config contents are immutable. |
| `launch((address,string,string,string,bool,address,uint16,uint8,address,bool),(address,uint256,uint256,uint256))` | `payable` — Document the generation-specific payable creation call and returned token/curve/bought amount; this is not an authorized launch or proof of actual cost/refund. |

### `launch-router-2026-10-19`

| Signature | Mutability / bounded interpretation |
| --- | --- |
| `buyExactIn(address,address,uint256,uint256,uint256,address,address,(address,uint16))` | `payable` — Document router buy inputs, protection minima, recipients, referral and integrator fee tuple; returned tokens are not a read-only cost/refund quote. |
| `sellExactIn(address,uint256,address,uint256,address,address,(address,uint16))` | `nonpayable` — Document router sell inputs, payout protection and integrator fee tuple; no automatic execution or guaranteed fill follows. |

### `launch-hook-2026-10-19`

| Signature | Mutability / bounded interpretation |
| --- | --- |
| `setModule(bytes32,address)` | `nonpayable` — Document hook module assignment for a pool; actual caller authorization and protocol disable controls remain separate. |
| `clearModule(bytes32)` | `nonpayable` — Document hook module removal for a pool; do not infer identical controls for the older hook. |
| `poolOf(address)` | `view` — Read the pool identifier associated with a module; the identifier is not a complete LP position. |
| `moduleOf(bytes32)` | `view` — Read the module associated with a pool identifier; refresh disable and configuration evidence separately. |
| `disabled(address)` | `view` — Read the hook’s module-disabled flag; it does not certify safe behavior or all possible trading outcomes. |
| `swapIndex(bytes32)` | `view` — Read the pool’s reported swap counter; not offchain pilot points or proof of complete trade-volume history. |
| `pools(bytes32)` | `view` — Read the hook’s pool association tuple including curve, token, pair asset, direction, policy flag, graduation time and Config address. |
| `checkModule(address,bytes32,address,address)` | `nonpayable` — Document the nonpayable module-check entry; it is not a view getter or independent certification of module behavior. |

### `launch-factory-2026-10-14`

| Signature | Mutability / bounded interpretation |
| --- | --- |
| `charterDrop()` | `view` — Read the factory-linked drop contract address; authenticate that role separately. |
| `launchConfig()` | `view` — Read this generation’s launch configuration tuple; differing generation and common-array tuple layouts must not be substituted. |
| `launch((address,string,string,string,uint16,bool,address,uint16),(address,uint256,uint256,uint256))` | `payable` — Document the generation-specific payable creation call and returned token/curve/bought amount; this is not an authorized launch or proof of actual cost/refund. |

### `launch-router-2026-10-14`

| Signature | Mutability / bounded interpretation |
| --- | --- |
| `buyExactIn(address,address,uint256,uint256,uint256,address,address,(address,uint16))` | `payable` — Document router buy inputs, protection minima, recipients, referral and integrator fee tuple; returned tokens are not a read-only cost/refund quote. |
| `sellExactIn(address,uint256,address,uint256,address,address,(address,uint16))` | `nonpayable` — Document router sell inputs, payout protection and integrator fee tuple; no automatic execution or guaranteed fill follows. |

### `launch-config-2026-10-19`

| Signature | Mutability / bounded interpretation |
| --- | --- |
| `get()` | `view` — Read the Config configuration and supply tuples in their distinct declared order; current fields are not immutable published defaults. |
| `hookConfig()` | `view` — Read the hook-facing Config tuple, not the larger get() result or a stock SessionFeeHook fee table. |

### `creator-fee-escrow-2026-10-19`

| Signature | Mutability / bounded interpretation |
| --- | --- |
| `balanceOf(address)` | `view` — Read creator escrow accounting for the supplied curve, not a holder token balance or Safe reward reserve. |
| `claim(address)` | `nonpayable` — Document the role-specific explicit claim transaction; a preview or successful simulation is not settled transfer evidence. |

### `bonding-curve-2026-10-19`

| Signature | Mutability / bounded interpretation |
| --- | --- |
| `config()` | `view` — Read the configured Config address; this is not evidence that the factory can replace its immutable Config address or that Config contents are immutable. |
| `module()` | `view` — Read the curve’s configured module address; an address does not establish full powers, tier or deployed source. |
| `dropMode()` | `view` — Read the curve’s encoded charter-drop mode; authenticate enum semantics rather than equating every nonzero value with at-exit payout. |
| `enforced()` | `view` — Read the curve’s recorded venue-policy flag, not universal router enforcement or a token permission result. |
| `charterDropAmount()` | `view` — Read the curve’s recorded launched-token drop amount; allocation does not imply presently spendable tokens. |

### `bonding-curve-2026-10-14`

| Signature | Mutability / bounded interpretation |
| --- | --- |
| `graduated()` | `view` — Read the curve lifecycle flag for an authenticated child curve; implementation-template storage is not a launched token’s state. |
| `stock()` | `view` — Read the curve’s pair-asset address; the name stock does not prove legal equity backing or exclude other pair-asset types. |
| `virtualStock()` | `view` — Read the curve virtual pair-asset reserve input, not a withdrawable balance. |
| `virtualTokens()` | `view` — Read the virtual launched-token reserve input, not circulating supply. |
| `endVirtualTokens()` | `view` — Read the curve terminal virtual-token input; deployed curve rounding and exact execution arithmetic remain unproved. |
| `phantomReserve()` | `view` — Read the curve phantom pair-asset reserve parameter, not owned backing or available liquidity. |
| `creatorTaxBps()` | `view` — Read the older curve’s creator extra-fee input, distinct from its base fee. |
| `baseFeeBps()` | `view` — Read the curve’s base-fee input; do not import new-generation published rates into the old generation. |
| `launchTime()` | `view` — Read the child curve’s launch timestamp used to contextualize schedules. |
| `currentSnipeTaxBps()` | `view` — Read the reported current curve-buy snipe fee; timing/sender/path and actual receipts remain separate. |
| `snipeSchedule()` | `view` — Read the ordered curve snipe-fee schedule; array position alone does not establish timing buckets. |
| `feeRecipient()` | `view` — Read the designated fee/control recipient, not all token holders or a proof of accepted ownership. |
| `setFeeRecipient(address)` | `nonpayable` — Document the fee-recipient change transaction; effective control and treatment of unclaimed fees require the generation’s source/receipt evidence. |
| `poolKey()` | `view` — Read all five PoolKey components; PoolManager address alone cannot identify this pool or an LP position. |

### `creator-fee-escrow-2026-10-14`

| Signature | Mutability / bounded interpretation |
| --- | --- |
| `balanceOf(address)` | `view` — Read creator escrow accounting for the supplied curve, not a holder token balance or Safe reward reserve. |
| `claim(address)` | `nonpayable` — Document the role-specific explicit claim transaction; a preview or successful simulation is not settled transfer evidence. |

Trading-rate BPS use `10000 = 100%`, not hook hundredths-of-bp. However, **a field name does not establish its scale**: `creatorShareOfBaseBps` concerns a share of the base fee, not trade value, but its raw denominator remains unestablished by this selected ABI. Do not automatically divide that raw field by10000 or equate it to a published percentage; authenticate source arithmetic or publisher usage first. Creator-buy/drop caps concern supply. Pair-asset, launched-token, native ETH and WETH quantities remain distinct; corroborate decimals. An ordinary PoolKey fee uses hundredths-of-bp, while dynamic-fee flags are not numeric rates. Tick spacing is signed ticks. Times are seconds; byte/gas bounds and enum/bitset fields are neither token amounts nor rates. WAD-labelled curve inputs do not prove a deployed formula, rounding or gross/net assessment order.

`get()` returns separate `c` and `s` tuples; `c` contains dynamic `snipeScheduleBps`, so offsets require recursive ABI decoding. `hookConfig()` has a different static tuple. Older `launchConfig()` has its own dynamic tuple and must not use either decoder. New factory `config()` exposes the immutable Config **address**; mutable Config contents are separate. Escrow `balanceOf(address curve)` is curve-keyed fee accounting in the pair asset, not ERC20 holder balance.

## Events and errors

Both selected factories expose `Launched`: token, curve and creator occupy topics1/2/3, while the generation-specific `info` tuple is in ABI data. It contains strings and arrays; data-parameter position is not a fixed word offset. **Different info tuple layouts produce different signatures/topics.** The older selected factory additionally exposes `Graduated`: token/curve/poolId are indexed; the info tuple is data. The newer primary array does not supply that event, which is incomplete coverage, not proof graduation emits nothing. Inspect JSON `event_layout` and preserve emitter, canonical log identity, receipt and asset-flow evidence.

Every selected error is retained with its exact signature/selector and any arguments. Shared error declarations are parsing dependencies, not evidence that every error is reachable on every role. Name-derived guards such as `BlockedByModule`, `ModuleFailed`, `Tier2Disabled`, `NotFeeRecipient`, `CurveGraduated` or `InsufficientOutput` do not establish all authority, failure behavior or safety. No selected constructor/receive/fallback is present in these arrays; broader deployed coverage remains unknown. The reference URC5 token spec is not installed as a deployed token ABI, and a hook policy flag is not a complete inbound/outbound token-permission interface.
