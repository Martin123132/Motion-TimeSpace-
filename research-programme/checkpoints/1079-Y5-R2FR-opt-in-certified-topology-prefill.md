# 5063 - opt-in certified topology prefill

Marker: `MTS_5063_OPT_IN_CERTIFIED_TOPOLOGY_PREFILL`.

The validated certificate and constructor are exposed as a default-off prefill
runner. It reads an existing run configuration and source-epsilon topology,
requires converged 8/16 segment signatures and projective steps below `0.1`,
and writes a target topology only when no transition is present.

Transitions, unconverged certificates, missing source topologies, and existing
target files are never overwritten. A generated target carries the live config
digest and argument identity so the existing 5034 runner can reuse it normally.
The explicit enable flag is `--enable-certified-transport`; omitting it performs
no topology writes.

## Evidence

- Runner: `scripts/Y5_R2FR_5063_opt_in_certified_topology_prefill.py`
- Integration result: `source-intake/functional_rg/5064/opt_in_prefill_integration_smoke.json`

The runner never authorizes a kernel or physics claim by itself.
