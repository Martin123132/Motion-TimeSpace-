# 5043 — Theorem-first coarse `E040` multilevel gate

**Status: QUARANTINED AND SUPERSEDED BY CHECKPOINT 5049.**

The broad theorem guard used here admitted 1299 exact-zero rows, while only 98
were inside the later proved-family audit. The figures below are retained as a
historical diagnostic and must not be used as the current estimator verdict.
Checkpoint 5049 reruns the complete matrix with the restricted theorem.

## Purpose

Test whether the strong retrospective correlation between the Richardson
observable

`Y = 2 R(E020_primary24) - R(E040_primary24)`

and an `E040` low-fidelity observable can reduce cost without bias.

The future estimator would be

`mu_hat = mean_H(Y - beta X) + beta mean_L(X)`,

with fixed coefficients and independent high/correction and low-only samples.
No known value of `E[X]` is assumed, so low-fidelity bias cancels exactly.

## Theorem-first evaluator

The 5041 additive-source theorem is applied before numerical local-residue
evaluation. A cross-source collision is set to exact zero only when every 5041
guard passes. Remaining same-source rows retain the shrinking-radius numerical
rule. Same-source stereographic chart-origin coalescences without a tracked
crossing are filtered under the existing chart certificate.

The sole finite endpoint obstruction, `S503403_N0000/A14`, reuses the promoted
5037 source contract. Its two contour floors prove zero double residue,
two-sided continuous limits agree, and the primary/audit repaired kernels agree
with zero recorded relative residual. The coarse run used that continuous
extension twice; it did not insert a fitted value.

## Matrix result

- Dry-run coverage: `120/120` exact event/argument topologies and primary
  comparators exist.
- Benchmark winner: fixed `coarse12` profile (`12` relative/global nodes,
  adaptive tolerance `5e-4`).
- Matrix: `120/120` converged, zero failed and zero unconverged.
- Kernel wall time: `5352.99 s` (`89.2 min`).
- Exact theorem-zero rows: `1299`.
- Numerically evaluated residue rows: `1960`.
- Chart-origin exclusions: `300`.
- Maximum adaptive residual: `4.94e-4`.
- Formalization-workbench digest remains
  `b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758`.

## Statistical gate

Uniformly coarse `E040` is cheaper but not useful enough:

- future low/high event-cost ratio, including fresh topology: `0.326`;
- cross-fitted channels improved: `3/10`;
- worst cross-fitted SD ratio: `1.884`;
- target-margin-normalized equal-cost score ratio: `1.370`.

A ratio above one is worse than high-only sampling. The fixed `coarse12`
multilevel pilot is therefore rejected and no fresh kernels are authorized.
The approximately `6.8%` one-job coarse offset is not itself a failure—the
multilevel identity removes mean bias—but the measured correlation loss is.

## Evidence

- Runner: `scripts/Y5_R2FR_5043_theorem_first_coarse_E040_multilevel_gate.py`
- Benchmark: `source-intake/functional_rg/5043/coarse_profile_benchmark.json`
- Matrix status: `source-intake/functional_rg/5043/runs/coarse12/status.json`
- Result: `source-intake/functional_rg/5043/multilevel_coarse_E040_gate.json`
- Components: `source-intake/functional_rg/5043/multilevel_component_gate.csv`
- Rejected lock: `source-intake/functional_rg/5043/locked_multilevel_pilot_contract.json`
- Validation: `source-intake/mts_residuals/P8_Y5_BRR545_5043_VALIDATION.csv`

This closes the uniformly coarse route only. It is not a production amplitude
or MTS physics claim.
