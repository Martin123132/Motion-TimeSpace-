# 5448: D4 event-local remainder analyticity bridge

## Decision

**THE EVENT-LOCAL OWNER IS NOT A NEW NONANALYTIC OBSTRUCTION: AFTER THE CERTIFIED `H log + G` PRIMITIVE IS REMOVED, ALL EIGHT REMAINDERS ARE HOLOMORPHIC ON THE COMMON REGULATOR STRIP. A FINITE SUPREMUM STILL HAS TO BE ENCLOSED.**

## Exact local split

For each fixed mapped event tube `T_e`, subtract every selected material principal part before integration and write

```text
I_tube,e(epsilon)
 = integral_Te [f-sum_b rho_b/(E-p_b)] dE dx
 + sum_b integral_Xe rho_b[Log(E_U-p_b)-Log(E_L-p_b)] dx.
```

At the colliding endpoint, checkpoint 5392 proves `v=epsilon h`, with `epsilon_ref z0/epsilon=2 i epsilon_ref u h` nonzero in one fixed half-plane. Its exact primitive is

```text
-Phi(z0)=H_e(epsilon) Log(epsilon/epsilon_ref)+G_e(epsilon).
```

Define

```text
R_e(epsilon)=I_tube,e(epsilon)-H_e(epsilon) Log(epsilon/epsilon_ref)-G_e(epsilon).
```

The patched Krawczyk branch makes the event coordinates holomorphic through zero. The fixed-half-plane gap makes the chosen logarithm single-valued. The full pole-catalog and nested-contour certificates isolate the selected pole and keep every other denominator nonzero. Checkpoint 5388 fixes the subtraction pole order. Holomorphic parameter integration over the fixed 5393 event cells therefore makes `R_e` holomorphic.

## Eight-event audit

| event | type | mapped cells | ratio boxes | half-plane | min other-root separation | analytic remainder |
|---|---|---:|---:|---|---:|---:|
| `E01` | `SUPPORT_ENTRY` | 3 | 10 | `UPPER` | 0.12474861292412141 | `true` |
| `E02` | `SUPPORT_ENTRY` | 3 | 10 | `LOWER` | 0.033684221192054054 | `true` |
| `E03` | `SUPPORT_ENTRY` | 2 | 10 | `LOWER` | 0.041236447737984447 | `true` |
| `E04` | `BRANCH_DEATH` | 2 | 10 | `UPPER` | 6.8590489890063674e-05 | `true` |
| `E05` | `BRANCH_DEATH` | 2 | 10 | `LOWER` | 7.1741890250848927e-05 | `true` |
| `E06` | `BRANCH_DEATH` | 2 | 10 | `LOWER` | 7.1700639711740104e-05 | `true` |
| `E07` | `BRANCH_DEATH` | 2 | 10 | `LOWER` | 6.8460688902406304e-05 | `true` |
| `E08` | `SUPPORT_EXIT` | 3 | 10 | `LOWER` | 0.17617930430994963 | `true` |

## What this closes

This closes the logical analyticity gap behind the phrase `desingularized coordinates exist`. The local `epsilon log epsilon` term is fully assigned to `H log + G`; it cannot leak back into `R_e`. A finite Cauchy estimate is therefore legitimate once a complex-strip supremum of the two retained analytic pieces is obtained.

The next bound is

```text
W3_event <= sum_e 6 sup_|zeta-epsilon|=r |R_e(zeta)| / r^3.
```

The remaining numerical owner is now concrete: bound the regularized two-dimensional integral on the `19` mapped event cells and the nonsingular upper/cutoff primitive. No new local-state, coupling or galaxy axiom is involved.

## Claim boundary

Analyticity does not supply the missing supremum. `valid_for_D4_event_local_W3_bound`, combined `W3`, the D4 regulator limit, all-operator local GR and full MTS remain false.
