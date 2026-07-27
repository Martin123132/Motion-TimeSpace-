# 3120 - `delta_J` Product-Bound Runner or Current-Owner Source Intake under AX1090

Private checkpoint. This follows 3119 by turning the hidden current-normalization residual into an executable intake/runner rather than another informal missing-input note.

## Verdict

The useful zero theorem remains:

```text
same parent charge generator + fixed charge lattice + q-basic matter currents
+ no source-only weights + variation-before-readout + radiative closure
=> delta_J = 0.
```

But that theorem is still unsigned at parent level. Therefore 3120 implements the finite branch:

```text
delta_J is retained as a sourced product residual until the current-owner theorem closes.
```

The new runner does not claim a pass. It forces the missing pieces to be concrete:

```text
beta_source_J, beta_test_J, tau_WEP, tau_R10, K_X(lambda),
material charge convention, delta_GM_J bridge, PPN projection kernel,
and source paths.
```

## Source Register

| source_id | path | role |
|---|---|---|
| 00-heuristics | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\00-martin-fork-heuristics-private.md` | fork discipline: do not reject a route merely because one time/readout sign looks GR-opposite before checking variable split and tested limit |
| 3116 | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3116-Y5-R2FR-public-Hodge-Maxwell-stress-lock-or-constitutive-residual-vector-under-AX1090.md` | Maxwell stress/Poynting/source residual vector |
| 3118 | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3118-Y5-R2FR-no-hidden-visible-coefficient-hom-for-local-EM-or-balpha-product-bound-runner-under-AX1090.md` | `b_alpha` runner pattern copied for `delta_J` |
| 3119 | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3119-Y5-R2FR-same-current-owner-or-deltaJ-source-test-residual-priority-under-AX1090.md` | same-current owner theorem attempt and `delta_J` projections |
| 3119-gate | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3119_SAME_CURRENT_OWNER_DELTAJ_GATE.csv` | current-owner gate rows used by this runner |
| WEP1052 | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1052_ALPHA_WEP_PROJECTION_LEDGER.csv` | WEP projection anchor; not a direct `delta_J` product value |
| R10-1052 | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1052_ALPHA_R10_PROJECTION_LEDGER.csv` | R10 product-law anchor; not a direct scoreable bound |
| local-bounds | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\local_bounds\local_bound_claims.csv` | PPN/WEP empirical anchors; not yet a `delta_J` projection kernel |

## Implemented Files

| artifact | path |
|---|---|
| input template | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3120_DELTAJ_PRODUCT_INPUTS_TEMPLATE.csv` |
| runner | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\scripts\Y5_R2FR_3120_deltaJ_product_bound_runner.py` |
| runner output | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3120_DELTAJ_PRODUCT_BOUND_RUNNER_OUTPUT.csv` |
| validation | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3120_VALIDATION.csv` |
| gate | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3120_CURRENT_OWNER_SOURCE_INTAKE_GATE.csv` |

## Product Rows

| product_id | arena | product being tested | current status |
|---|---|---|---|
| DJP3120_0 | theorem-zero | `delta_J = 0` | blocked until same-current owner theorem is parent-signed |
| DJP3120_1 | WEP | `K_WEP Delta Q_J beta_source_J delta_J tau_WEP` | blocked by missing MTS product and material charge convention |
| DJP3120_2 | R10 | `K_X^R10 beta_s^J beta_t^J + epsilon_tail_J` | blocked by missing current legs, profile kernel, tail and valid bound curve |
| DJP3120_3 | source calibration | `Delta_GM_J / GM` | blocked by missing EM-current-to-source-mass bridge |
| DJP3120_4 | PPN bridge | `Delta gamma_J` or `Delta beta_J` | blocked by missing source-mass-to-PPN projection kernel |
| DJP3120_5 | standalone current | `abs(delta_J)` | blocked by missing current normalization source or theorem zero |

## Claim Logic

A row can only become claim-valid if all of the following hold:

```text
1. product_value is finite numeric;
2. valid_for_claim=true on the input row;
3. product value has no MISSING/PLACEHOLDER marker;
4. material charge convention is sourced and has no MISSING marker;
5. source file and source row resolve;
6. source bound is numeric or the theorem-zero row is parent-signed;
7. bound status is direct for the selected arena;
8. abs(product_value) <= source_bound.
```

The present template deliberately fails this gate. That is correct: the achievement is executable structure, not a physics claim.

## Result

The runner converts the 3119 branch into a testable product interface.

Current output:

```text
all rows: claim_allowed=false
reason: current-owner theorem unsigned and finite products missing
```

This is a sharper situation than "something is missing." We now know the exact files and row-level quantities required to move the branch:

```text
same-current theorem route:
  sign T_Q / n_A / q-basic current / no c_A(y) / readout closure

finite residual route:
  source beta_source_J, beta_test_J, tau_WEP/R10, K_X(lambda),
  material charge maps, Delta_GM_J bridge, and PPN kernels
```

## Fork Discipline

Use the private 00 heuristic here. If a future `delta_J` or source-time branch appears to move opposite to a familiar GR wording, do not discard it instantly. First split:

```text
local clock/proper time
public readout time
field/source current normalization
background traversal or flow parameter
```

Then require the branch to reproduce measured GR/Newton/Maxwell limits or become a bounded residual. This keeps the work derivation-first without turning intuition into an unsupported claim.

## Claim Status

No public EM current, WEP, R10, PPN, source-calibration, local-GR, Maxwell, derived-`G`, or unification claim follows from 3120.

The internal advance is:

```text
delta_J now has a product-bound smoke runner;
the exact missing MTS inputs are machine-readable;
the current-owner zero route and finite-bound route are separated cleanly.
```

## Next Target

Write:

```text
3121-Y5-R2FR-deltaJ-source-calibration-DeltaGM-bridge-under-AX1090.md
```

Direct target:

1. attempt the derivation route first: show that current-owner descent makes `Delta_GM_J=0`;
2. if not, derive the leading bridge from `J_Q(y)` to `Delta T_EM^J`, then to `Delta_GM_J/GM`;
3. only after that project the result into WEP/PPN/orbital bounds.
