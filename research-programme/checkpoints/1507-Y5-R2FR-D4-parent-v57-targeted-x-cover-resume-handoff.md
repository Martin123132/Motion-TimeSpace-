# 5491: D4 parent-v57 targeted-x-cover resume handoff

Checkpoint 5484 advances four atomic nodes beyond checkpoint 5489. The first positive-epsilon source box and three exact descendants retain positive relative-root and selected-global-root bounds but fail the parent-v56 collision-Jacobian enclosure. The current state remains unresolved-free at `178/8/0`; these are exact refinements, not accepted failures.

## Checkpoint 5490: epsilon-real cover rejected

The broad target is `R_E0S_E0S_E0S_E1S`, epsilon-real `[1e-6,0.0025]`, x `[0.8570372233341658,0.857275609802905]`, t `[0.0002,1.0]`. Parent v56's exact `X16 x T128` union has zero lower bound while the chart-denominator lower is `6.334463380684113e-05`.

Checkpoint 5490 adds the missing epsilon-real axis without changing the parent action or threshold. Exact `E2`, `E4`, `E8` and `E16` by `X16 x T128` covers all retain zero. Their chart-denominator lowers remain positive and increase to `6.335985000065282e-05`; parameter-volume error is zero. Epsilon-real refinement alone is therefore rejected as the repair.

## Checkpoint 5491: dependency isolated

The first exact `E16/X16/T128` zero leaf is index `E0:X0:T0`; it is encountered on the first tested leaf. Its bounds are:

- epsilon-real `[1e-6,0.0001571875]`;
- epsilon-imaginary `[-1e-6,1e-6]`;
- x `[0.8570372233341658,0.8570446729113139]`;
- t `[0.0002,0.00020762786865234376]`.

Its selected alternate chart has denominator lower `6.37627693274237e-05`, but the interval Jacobian contains zero. Single-axis exact ablations give:

- epsilon-real counts `2,4,8,16,32`: all zero;
- epsilon-imaginary counts `2,4,8,16,32`: all zero;
- t counts `2,4,8,16,32`: all zero;
- x count `2`: pass, leaf-union lower `242.40838294805386`, chart-denominator lower `6.376523592885644e-05`, exact-cover error `0.0`.

The 81 corner/midpoint point samples have minimum selected lower `267.04436705001797`. This is diagnostic only, but it agrees with the interval proof that the demonstrated zero is an x-hull dependency rather than evidence for a sampled pointwise zero.

## Current state

- Frontier state: `source-intake/functional_rg/5484/work-v1/E07__U051__RIGHT_CONNECTOR__CUBOID__6df3d70a73e4618b.json`.
- SHA-256: `3f485d18bb2a55d3fda317091e58c0330166a7b5ae7e2185a82ab46602e23faa`.
- Accepted/pending/unresolved: `178/8/0`.
- Parent-v56 evaluations/accepted/witnesses: `18/10/8`.
- Checkpoint 5490 validation: `11/11` pass.
- Checkpoint 5491 validation: `11/11` pass.

## Exact next calculation

Build checkpoint 5492 as a candidate-only adaptive finite union on the unchanged broad target:

1. Partition exactly into `E16 x X16 x T128` leaves.
2. Retain every leaf whose selected collision-Jacobian lower is positive.
3. For each and only each zero leaf, bisect x exactly once and require both children to have positive Jacobian and chart-denominator lowers.
4. Take the global lower as the minimum over retained leaves and replacement children, and prove exact parameter-volume coverage.
5. Stop before parent acceptance. If the adaptive candidate is positive, build a complete-amplitude target/control integration gate before any parent-v57 migration.

This is a derived response to the measured dependency; it does not add a closure assumption. Full active-cuboid, full outer, event-local/combined `W3`, regulator-limit, all-operator local-GR and full-MTS claims remain false. No GitHub action and no `formalization-workbench` edit belongs to this checkpoint.

**X_HULL_DEPENDENCY_ISOLATED__BUILD_EXACT_ADAPTIVE_X_REPLACEMENT_COVER**
