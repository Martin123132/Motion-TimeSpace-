# 5044 — Symmetric hybrid-fidelity reserve gate

**Status: QUARANTINED AND SUPERSEDED BY CHECKPOINT 5050.**

This split was selected from the quarantined 5043 coarse matrix. Its figures
below are historical only. The restricted-scope reaudit in 5050 selects no
exterior promotion and rejects the old hybrid lock.

## Question

Did uniform coarsening fail everywhere, or only where the cyclic observable
uses exterior crossed arguments?

The test is restricted to nine nested, reflection-symmetric thresholds. It is
not an unrestricted subset fit. Each step promotes the next `(+z,-z)` argument
pair from `coarse12` to `primary24`; the centre is promoted last. Selection uses
leave-one-scramble-out correction variance, measured future topology/kernel
cost, and the fixed target-error margins. Target central values are not fitted.

## Result

The minimum occurs at the physically simple split

- `primary24` for `|argument| >= 1.5`:
  `A00–A04` and `A10–A14`;
- `coarse12` for the physical band `|argument| <= 0.6`:
  `A05–A09`.

Measured retrospective diagnostics are:

- low/high event-cost ratio: `0.469`;
- optimal low/high sample ratio: `11.17`;
- equal-cost target-normalized score ratio: `0.735`;
- channels improved cross-fitted: `7/10`;
- worst cross-fitted SD ratio: `1.492`.

The neighboring exterior thresholds also score below `0.8`, so the result is
not a one-grid-point minimum. This supports a real conclusion: the coarse error
that destroys correlation is concentrated in the exterior crossed region.

## Cost decision

The design is statistically locked only as a future reserve. Four high units
and the locked low/high allocation require at least `45` low units, with a
measured projected runtime of `46.29 h`. This exceeds the user's four-hour
per-turn execution cap by more than an order of magnitude.

Therefore:

- do not run the pilot now;
- do not call the retrospective score evidence;
- retain the fixed split, coefficients, and estimator so it cannot be retuned
  after new data;
- first derive a cheaper topology-conditioned, analytic, or exterior-only
  control that attacks the same measured source of variance.

## Evidence

- Generator: `scripts/Y5_R2FR_5044_symmetric_hybrid_fidelity_gate.py`
- Result: `source-intake/functional_rg/5044/symmetric_hybrid_fidelity_gate.json`
- Threshold family: `source-intake/functional_rg/5044/symmetric_threshold_family.csv`
- Components: `source-intake/functional_rg/5044/selected_component_gate.csv`
- Reserve lock: `source-intake/functional_rg/5044/locked_reserve_multilevel_pilot.json`
- Validation: `source-intake/mts_residuals/P8_Y5_BRR545_5044_VALIDATION.csv`

No production `hhh`, local-GR, Newton, Maxwell, or full-MTS claim follows from
this estimator-design checkpoint.
