# 121 - Shared Calibration Relation Derivation Attempt

Private checkpoint. This is not a public claim.

## 1. Trigger

Checkpoint 120 said the only hard joint late+CMB failure looked mostly like:

```text
BAO absolute-calibration tension after alpha_BAO was tied to c/(100 h r_d).
```

This checkpoint tests that statement directly.

Question:

```text
Can a shared calibration relation among h, r_d, alpha_BAO, SN offset, and
Omega_m0 repair the failed gate, or is the real problem somewhere else?
```

## 2. Machine Artifact

Script:

```text
research-programme\scripts\shared_calibration_relation_attempt.py
```

Run:

```text
research-programme\runs\20260531-171500-shared-calibration-relation-attempt
```

Generated:

```text
source_register.csv
t7_free_alpha_target.csv
calibration_target_rows.csv
aggregate_targets.csv
relation_candidate_audit.csv
decision.csv
status.json
```

Status:

```text
shared_calibration_relation_target_quantified_not_derived
```

Claim ceiling:

```text
internal_derivation_audit_not_public_evidence
```

## 3. T7 Late-Only Target Reproduced

The locked late-only branch is reproduced exactly:

| Quantity | Value |
|---|---:|
| `Omega_m0` | `0.3032827426766658` |
| `B_mem` | `0.07407407407407407` |
| `p` | `3.0` |
| `u3` | `0.25` |
| free BAO `alpha` | `30.012562164133616` |
| `chi2_SN` | `1457.0988304105056` |
| `chi2_BAO` | `8.169575390292101` |
| `chi2_late` | `1465.2684058007976` |
| recomputation difference | `0.0` |

So the target is clean:

```text
late-only T7 wants Omega_m0 ~= 0.30328 and alpha_BAO ~= 30.01256.
```

## 4. The Important Surprise

The suspected repair lever was:

```text
alpha_BAO = c / (100 h r_d)
```

But the audit says:

```text
this is not where the hard failure lives.
```

For each joint row, the tied value:

```text
alpha_BAO = c / (100 h r_d)
```

is already essentially equal to the free-alpha optimum at that same joint
`Omega_m0`.

Aggregate result:

| Quantity | Value | Meaning |
|---|---:|---|
| mean same-shape `xi_alpha` required | `1.000000039490485` | multiplier needed to make tied alpha equal the free-alpha optimum |
| max same-shape `xi_alpha` spread | `8.629146552863176e-08` | scatter across four joint gates |
| mean tied-alpha BAO penalty | `3.3278224620403307e-10` | effectively zero |
| mean free-alpha BAO shape penalty | `3.1697527095124576` | actual remaining BAO cost |
| mean `Omega_m0` shift vs T7 | `0.01647749874764233` | CMB bridge pushes `Omega_m0` upward |

So the previous phrase:

```text
BAO absolute-calibration tension
```

was too broad. The sharper diagnosis is:

```text
BAO shape tension caused by the CMB-driven upward shift in Omega_m0.
```

## 5. Failed Gate Anatomy

The failed row is:

```text
prior_table = LCDM
score_mode = strict_full4
gate = hard_loss_sector_degradation
```

Exact numbers:

| Quantity | Value |
|---|---:|
| joint `Omega_m0` | `0.32404493506253196` |
| T7 late-only `Omega_m0` | `0.3032827426766658` |
| `Omega_m0` shift | `+0.020762192385866185` |
| tied `alpha_BAO` | `30.47091750027696` |
| same-shape free `alpha_BAO` | `30.470918292570904` |
| same-shape `xi_alpha` required | `1.0000000260016437` |
| tied-alpha BAO penalty | `8.814460272787983e-11` |
| BAO shape penalty after freeing alpha | `4.841090529899786` |

Readout:

```text
The alpha relation is not hurting us at fixed joint shape.
The CMB-compatible Omega_m0 is what moves the BAO shape away from the late-only
sweet spot.
```

Boxing-score version:

```text
We thought the judge took the round because our glove tape was wrong.
The tape is fine. The issue is the angle: the CMB corner is making us stand at
Omega_m0 ~= 0.324 while late SN+BAO wants Omega_m0 ~= 0.303.
```

## 6. Relation Candidates

| Candidate | Status | Verdict |
|---|---|---|
| pure metric calibration `alpha_BAO = c/(100 h r_d)` | already encoded | mixed result remains |
| common alpha multiplier `xi_alpha` | quantified but not useful | not the repair lever |
| effective late sound horizon `r_d_eff` | algebraically equivalent to alpha shift | not enough at fixed joint shape |
| SN offset / H0 lock | not primary | does not repair BAO residuals in no-SH0ES branch |
| MTS-specific BAO deformation | possible only after early-sector derivation | forbidden as an ad hoc rescue |
| early-to-late `Omega_m0` / CMB map | live theorem target | main unresolved bridge |

## 7. Derivation Attempt

Start from the joint BAO prediction:

```text
D_BAO^model(z) = alpha_BAO F_BAO[z; E(z; Omega_m0, B_mem, p, u3)]
```

with:

```text
alpha_BAO = c / (100 h r_d).
```

For fixed joint `Omega_m0`, the free-alpha optimum is:

```text
alpha_free =
(F^T C_BAO^{-1} D_obs) / (F^T C_BAO^{-1} F).
```

The audit finds:

```text
alpha_free / alpha_BAO = 1 + O(10^-8)
```

for the mandatory joint rows.

Therefore a scalar calibration multiplier:

```text
alpha_BAO -> xi_alpha alpha_BAO
```

cannot be the physical missing term unless it also changes the background shape
`F_BAO[z; E(z)]`.

But changing `F_BAO` means changing:

```text
E(z), D_M(z), D_H(z), D_V(z),
```

or the mapping between the CMB-inferred matter parameter and the late-time
BAO/SN matter parameter.

So the required parent-action contract is not:

```text
derive xi_alpha.
```

It is:

```text
derive a lawful early-to-late Omega_m0 map, or derive a memory-sector BAO-shape
correction that reduces to the GR identity in the zero-memory limit.
```

## 8. Exact Contract for a Future Parent Action

A future parent action may repair this gate only if it supplies a relation:

```text
Omega_m0^late = M_Omega(Omega_m0^CMB, B_mem, p, u3, ...),
```

or an equivalent shape relation:

```text
F_BAO^MTS(z) = F_BAO^metric(z) + delta F_memory(z),
```

with all of the following conditions:

1. It reduces to the identity when the memory sector is turned off:

```text
B_mem -> 0  implies  Omega_m0^late = Omega_m0^CMB
```

or:

```text
delta F_memory -> 0.
```

2. It is derived before being fitted.

3. It is not applied privately to MTS while baselines keep a stricter ruler map.

4. It preserves the existing successful late-only branch:

```text
Omega_m0^late ~= 0.30328.
```

5. It makes the compressed CMB bridge tolerate that late value, or predicts a
specific BAO shape correction.

6. It does not break the local-GR/PPN route.

7. It does not turn `B_mem=2/27` back into a hidden fitted amplitude.

Required scale:

```text
mean Omega_m0 shift to account for ~= 0.01648
failed strict-LCDM shift to account for ~= 0.02076
```

## 9. Decision

Allowed statement:

```text
The joint late+CMB failure is now sharper: it is not an alpha/r_d calibration
failure at fixed joint shape, but a BAO-shape penalty induced by the CMB-driven
Omega_m0 shift.
```

Allowed statement:

```text
The locked branch remains close and not dead, but the promotion target has
moved from alpha calibration to an early-to-late Omega_m0/CMB-map derivation.
```

Forbidden statement:

```text
The calibration relation is derived.
```

Forbidden statement:

```text
MTS passes joint late+CMB cosmology.
```

Current status:

```text
closure-only unless the Omega_m0 bridge or BAO-shape correction is derived.
```

## 10. Next Target

The next checkpoint should be:

```text
122-early-late-Omega-map-theorem-attempt.md
```

Task:

```text
Try to derive a memory-sector map between CMB-inferred Omega_m0 and late-time
BAO/SN Omega_m0. If it cannot be derived cleanly, demote the joint CMB bridge
to an explicit empirical closure and move testing to observables that do not
depend on compressed CMB background priors.
```

