# Host-native public reads

Choose suitable host public-read tools, existing clients or locally authored analysis code under normal permissions. The skill bundles no protocol client and requires no particular tool, command, output schema or always-run read set. Efficiency guidance is not a ceiling on requested deeper research.

## Trusted runtime preflight

Use trusted installed guidance and existing host tools. Check the needed capabilities, not the host brand: authorized public RPC/read transport; ABI encoding/decoding and Ethereum Keccak-256 when selectors/topics are needed; exact integer/decimal calculation; and relevant index, log and receipt coverage for historical claims. Archive state is needed only for questions requiring past state, not automatically for receipt history. No particular language, bundled helper, paid plan or provider is required.

Keep package integrity, the actually loaded revision, host capabilities, provider coverage, reasoning correctness and the end result separate. An intact install is not proof of deployment authentication or live access; a successful state call is not proof of history coverage or earned-fund attribution. Parse source/ABI as data; never execute downloaded code to extract interfaces. Use the dated [interface guide](interface-guide.md) as leads, authenticate the question's deployment and semantics, and calculate under ordinary host permissions.

Resolve auction family from the question and context before applying its interface or economics: buying a new charter is not expanding an existing charter with branch licenses. Authenticate each family's role, generation, schedule, inventory, price, payment asset and event semantics independently; do not borrow a 12-hour period, 2×/3× rule, floor or cap from the other. Ask a focused clarification only when context cannot disambiguate.

## Input transport and host approvals

Pass external values as data. Apply [host approvals](safety.md#host-execution-and-approval) and [preparation limits](safety.md#preparation-and-wallet-boundary). Bound runtime/capture; interrupted or truncated responses are incomplete evidence.

## RPC provider guidance

Select authorized providers by the question's needed capability: current/historical state, event indexes, logs, transactions and receipts differ. Record relevant chain, provider/plan, observation date and finite coverage/page/window bounds; do not promote one endpoint's limit to a universal protocol rule. A paid tier, API key or working receipt lookup proves neither a usable event index nor completeness. Credentials stay in host-managed environment/secrets facilities, never chat, runtime files or CLI arguments.

Provider limits are evidence to record, not package defaults. A reported **10-block Alchemy log-range cap** is only a dated observation for the particular host, chain, endpoint/product and plan that returned it; retain those details and the original diagnostic, and leave missing details unknown. This guidance does not claim to have measured current provider limits. Use relevant published capabilities or an authorized bounded observation where needed, without re-probing an already established limit. No external workshop or host-specific RPC document is required to use the skill.

Reuse pinned observations, headers and interfaces; batch compatible calls when useful. Stop at sufficient evidence or declared bounds. After failure, distinguish authorization denial, provider access denial, transport failure, method/range/index/archive limitations and a remaining evidence gap under [safety](safety.md#public-retrieval-and-calls). A user/host prohibition ends that action across routes. Do not evade provider controls; an ordinary independently authorized source may still answer a permitted question. Make source changes explicit, retain the original diagnostic and set a justified finite bound before retrying or changing the retrieval plan. Do not silently fail over, probe the same known limit repeatedly or claim unobserved coverage.

For multi-read work, use the [shared collection recipe](collection-efficiency.md): resolve dependencies, deduplicate requests, batch supported independent reads and match responses by ID before reconciliation. Avoid one CLI subprocess per item when an authorized batch facility exists. This applies to bill/position reads, quote alternatives and receipt/header verification; it introduces no bundled transport or mandatory client.

Capture complete `eth_getLogs` identity/order fields at ingestion when available; receipt matching, transaction-success checks and header canonicality remain distinct verification. Preserve partial source observations rather than fabricating missing fields. Existing authorized external evidence may be reused incrementally: fill coverage gaps, reconcile overlap/reorg replacements, refresh a declared provisional boundary and perform a scoped cross-check on provider transition. See [canonicality triggers and reuse](auction-history.md#optional-incremental-evidence-reuse); neither repeated full scans nor never-refetch rules are required.
