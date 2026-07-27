# 3151 - Boundary-Class Fixedness or Derivative Input Contract under AX1090

Private checkpoint. This follows 3150:

```text
derive boundary-class fixedness before readout,
or fill/source the first numeric derivative-bound input:
||d_S(W)|| and ||Lambda||.
```

## Result

3151 sharpens the closed-weight route instead of simply circling the missing term.

The boundary class has to be a parent-owned object:

```text
B_class := [S, orientation, corner_policy, cohomology_sector, reference_counterterm, readout_convention].
```

The clean fixedness theorem shape is:

```text
D_source B_class = 0,
D_readout B_class = 0,
D_reference B_class = 0,
D_source(lambda, epsilon, xi) = 0
=> D_source W|S = 0.
```

This is useful, but it is not yet enough.

Boundary-class fixedness removes source/readout drift of `W`, but full surface closedness still needs:

```text
d_S Wbar(B_class, lambda, epsilon, xi, reference) = 0
```

or a sourced norm bound. In short:

```text
D_source W|S = 0 does not by itself imply d_S(W)=0.
```

That is the important refinement from this step.

## Current Blockers

The boundary-fixed route is still not claimable because:

| gate | status | reason |
|---|---|---|
| parent fixes `B_class` before readout | `fail_for_claim` | 3089 keeps the boundary class unsigned |
| reference/counterterm silence | `fail_for_claim` | reference remains an allocator head |
| readout no-re-entry | `fail_for_claim` | `J_direct`, `J_spurion`, and `C_Obs_e` remain active |
| kernel closed on `S` | `not_claim_ready` | fixed labels do not prove `d_S(W)=0` |
| derivative input contract | `pass_nonclaim` | caps are staged, inputs are still missing |

## Derivative Input Contract

If the theorem route does not close, the first finite input is now explicit:

```text
|Q_deriv| <= ||d_S(W)||_* ||Lambda||_*.
```

The single-survivor cap is:

```text
||d_S(W)||_* ||Lambda||_* <= 5.970964001482571e-04
```

with current eta cap:

```text
4.201081650315690e-16.
```

The equal six-way diagnostic cap is:

```text
||d_S(W)||_* ||Lambda||_* <= 9.951606669137618e-05
```

with current eta cap:

```text
7.001802750526150e-17.
```

The same coefficient caps are staged for the Poynting/EM flux branch:

```text
|Int_partialW S_EM . dA dt| / M_H <= 5.970964001482571e-04
```

if it is the only survivor, or:

```text
<= 9.951606669137618e-05
```

under equal diagnostic splitting.

No numeric `||d_S(W)||`, `||Lambda||`, or Poynting flux value is claimed here.

## Research Fork Rule

I also recorded the working heuristic from Martin's note:

```text
A branch is not rejected merely because its coordinate-time story appears opposite to GR.
Reject only after invariant observables, weak-field GR/Newton limits,
conservation/covariance, or calibration tests fail.
```

This is not a physics claim. It is a search rule: when a fork looks strange, push once for a derivation or sourced finite bound before demoting it to closure.

## What This Means

3151 does move the branch forward:

1. It separates source/readout fixedness from surface closedness.
2. It prevents the bad shortcut `B_class fixed => d_S(W)=0`.
3. It gives exact source-ready rows for `||d_S(W)||`, `||Lambda||`, and Poynting flux.
4. It keeps the active local obstruction honestly alive until the missing inputs are filled.

So the next mathematical leap is narrower:

```text
prove d_S Wbar = 0 on S from the parent kernel geometry,
or acquire/source a real norm bound for ||d_S(W)||_* ||Lambda||_*.
```

## Runner Artifacts

| artifact | path |
|---|---|
| inputs | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3151_INPUTS.csv` |
| theorem | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3151_BOUNDARY_CLASS_FIXEDNESS_THEOREM.csv` |
| gates | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3151_GATE_STATUS.csv` |
| derivative contract | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3151_DERIVATIVE_INPUT_CONTRACT.csv` |
| score impact | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3151_SCORE_IMPACT.csv` |
| fork rules | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3151_RESEARCH_FORK_RULES.csv` |
| decision | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3151_DECISION.csv` |
| validation | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3151_VALIDATION.csv` |
| runner | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\scripts\Y5_R2FR_3151_boundary_class_fixedness_or_derivative_input_contract.py` |

## Decision

3151 does not promote local closure or local-GR recovery.

It promotes the next target from vague to exact:

```text
3152:
derive d_S Wbar = 0 under fixed B_class and parent kernel geometry,
or source the first real derivative/Poynting norm rows below the caps.
```
