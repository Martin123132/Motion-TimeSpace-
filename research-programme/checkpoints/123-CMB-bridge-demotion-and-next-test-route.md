# 123 - CMB Bridge Demotion and Next Test Route

Private checkpoint. This is not a public claim.

## 1. Trigger

Checkpoint 122 rejected the clean early-to-late `Omega_m0` theorem under the
current assumptions:

```text
single metric + separately conserved dust -> identity Omega_m0 map.
```

A nontrivial map needs:

```text
matter-memory exchange Q^nu,
```

or:

```text
a memory-sector BAO/acoustic shape correction.
```

Neither is derived yet.

So this checkpoint stops the compressed CMB background-prior branch from
quietly pretending to be a theory result.

## 2. Machine Artifact

Script:

```text
research-programme\scripts\CMB_bridge_demotion_and_next_test_route.py
```

Run:

```text
research-programme\runs\20260531-173000-CMB-bridge-demotion-and-next-test-route
```

Generated:

```text
source_register.csv
previous_gate_summary.csv
route_scorecard.csv
acceptance_gates.csv
decision.csv
status.json
```

Status:

```text
compressed_CMB_bridge_demoted_next_route_BAO_shape_residuals
```

Claim ceiling:

```text
routing_gate_not_public_evidence
```

## 3. Decision

The compressed CMB bridge is demoted to:

```text
empirical closure only.
```

It is still useful as a stress test, but not as promotion evidence.

Allowed:

```text
MTS survives compressed CMB distance-prior stress in a mixed/closure-only way.
```

Forbidden:

```text
MTS passes CMB.
```

Forbidden:

```text
MTS derives the early-to-late Omega_m0 map.
```

## 4. Route Scorecard

| Route | Decision | Reason |
|---|---|---|
| continue compressed CMB background priors | do not use for promotion | mixed/draw information only; map is not derived |
| BAO-shape residual decomposition | run next | directly targets the current failure with existing data |
| growth or `H(z)` non-CMB stress test | queue after BAO shape | reduces dependence on compressed CMB priors |
| full CMB perturbation/acoustic contract | write contract before running | correct high-value route, but expensive |
| local-GR/PPN derivation | keep parallel | mandatory for unified theory, not this cosmology residual |
| matter-memory exchange `Q^nu` theorem | do not fit until derived | would be powerful but high-risk and easy to abuse |

The practical next move is:

```text
BAO-shape residual decomposition.
```

Not because it is the grandest route, but because it is the cleanest next
punch: it tests the exact body shot that hurt us.

## 5. Acceptance Gates for the Next Test

The BAO-shape pass must obey:

1. Same BAO rows and covariance for every model.

```text
LCDM, wCDM, CPL, MTS_locked_2over27, MTS_Bmem_zero
```

2. Decompose by observable:

```text
DM/rs, DH/rs, DV/rs.
```

3. Decompose by redshift row.

4. Compare:

```text
late-only free-alpha T7
joint tied-alpha rows
CMB-compatible rows
```

5. Do not add any MTS-only BAO deformation.

6. If a residual pattern appears, write it as a theorem target, not a fitted
repair.

7. Keep the claim ceiling:

```text
diagnostic residual map only.
```

## 6. Why This Is the Right Next Step

Checkpoint 121 found:

```text
alpha_BAO is not the problem at fixed joint shape.
```

Checkpoint 122 found:

```text
B_mem DeltaR = 4/243 almost perfectly centers the joint compromise, but it is
not a full CMB-to-late theorem.
```

So the next useful question is:

```text
Which BAO observable and redshift rows actually create the shape penalty when
Omega_m0 is pushed upward?
```

That tells us whether the missing theorem should aim at:

```text
D_M(z), D_H(z), D_V(z), acoustic ruler physics, or the Omega_m0 inference map.
```

## 7. Boxing Readout

This is not us running away from CMB.

It is us refusing to let a dodgy judge decide the round from a compressed
scorecard.

The current honest card is:

```text
late SN+BAO: alive and interesting
BAO-only: alive and interesting
compressed CMB background: mixed closure stress, not promotion
joint late+CMB: close but not passed
next punch: identify the BAO-shape residual row by row
```

That is a respectable position.

It is not a title belt yet.

## 8. Next Target

Next checkpoint:

```text
124-BAO-shape-residual-decomposition.md
```

Script:

```text
scripts\BAO_shape_residual_decomposition.py
```

Task:

```text
For each model and branch, compute BAO residual contributions by observable
type and redshift row, then identify whether the MTS joint penalty is driven by
D_M, D_H, D_V, a redshift subset, or a broad shape mismatch.
```

Promotion rule:

```text
No promotion. This is a diagnostic map for the next derivation target.
```

