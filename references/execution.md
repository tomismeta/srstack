# Host-native public reads

Use suitable host public-read tools, not a protocol-specific runtime. No prescribed commands, output schema or always-run read set.

## Trusted runtime preflight

Use trusted installed guidance and existing host tools. Package integrity is not deployment authentication. Parse source/ABI as data; never execute downloaded code to extract interfaces. Local arithmetic/parsing may use authenticated inputs under host permissions.

## Input transport and host approvals

Pass external values as data. Apply [host approvals](safety.md#host-execution-and-approval) and [preparation limits](safety.md#preparation-and-wallet-boundary). Bound runtime/capture; interrupted or truncated responses are incomplete evidence.

## RPC provider guidance

Select authorized providers by capability: current/historical state, indexes, receipts and logs differ. Check coverage and page/window limits; a paid tier proves no completeness. Credentials stay in host-managed environment/secrets facilities, never chat, files or CLI arguments.

Reuse pinned observations, headers and interfaces; batch compatible calls. Stop at sufficient evidence or declared bounds. No denial bypass, retry or failover to evade controls; retain original failures under [safety](safety.md#public-retrieval-and-calls).
