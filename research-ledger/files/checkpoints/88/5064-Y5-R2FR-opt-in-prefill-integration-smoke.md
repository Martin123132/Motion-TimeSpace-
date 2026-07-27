# 5064 - opt-in prefill integration smoke

Marker: `MTS_5064_OPT_IN_PREFILL_INTEGRATION_SMOKE`.

A scratch copy of the 5036 run was populated with one safe `E040` source and
one known transition source. With transport disabled, no target is written.
With the explicit flag enabled, the safe `S503401_N0000/A00` target is written
and matches the full signature/class, while `S503402_N0000/A06` remains absent
for full-homotopy fallback.

A second enabled call preserves the generated file byte-for-byte. The existing
5034 `obtain_topology` path accepts it with zero homotopy runtime, proving that
the acceleration can be inserted without changing the kernel runner.

## Evidence

- Result: `source-intake/functional_rg/5064/opt_in_prefill_integration_smoke.json`
- Scratch run: `source-intake/functional_rg/5064/scratch_run/`
- Generator: `scripts/Y5_R2FR_5064_opt_in_prefill_integration_smoke.py`
- Validation: `source-intake/mts_residuals/P8_Y5_BRR545_5064_VALIDATION.csv`

The integration is default-off, idempotent, and preserves full-homotopy
fallback. No fresh science kernel is authorized here.
