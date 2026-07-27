# 3153 - Source-Support Level-Set Split or Physical Drift Bound under AX1090

Private checkpoint. This follows 3152:

```text
prove d_S z_S=0 from local vacuum/source support,
or prove D_z Wbar annihilates Im(d_S z_S) from quotient symmetry,
or source L_W, B_z, ||Lambda|| and Poynting flux below the caps.
```

## Result

3153 tries the boundary-level-set route directly.

The important result is:

```text
source support is useful, but it does not generically prove d_S z_S = 0.
```

It only removes the parts of the boundary data that are truly compact-support current or pure gauge/label drift. The remaining metric, reference, readout, multipole, tidal, EM, and constitutive drift is physical unless another theorem removes it.

So the full shortcut:

```text
supp(J) cap S = empty
=> d_S z_S = 0
```

is rejected as a generic theorem.

## Drift Split

Start from the 3152 chain rule:

```text
d_S W = (D_z Wbar) o d_S z_S.
```

3153 decomposes:

```text
d_S z_S =
  d_S z_const
  + d_S z_gauge
  + d_S z_support
  + d_S z_phys.
```

The pieces are:

| piece | meaning | status |
|---|---|---|
| `d_S z_const` | fixed labels/constants/calibration identifiers | zero as declared data |
| `d_S z_gauge` | tangential reparametrization, frame, and U(1) gauge drift | zero only if `Wbar` is boundary-basic |
| `d_S z_support` | ordinary matter/source current crossing `S` | zero only if source support misses `S` |
| `d_S z_phys` | metric/coframe multipoles, reference/readout, EM flux, constitutive drift | retained |

The reduced derivative route is therefore:

```text
d_S W = D_z Wbar[P_phys d_S z_S].
```

and the reduced finite bound is:

```text
||d_S W|| ||Lambda|| <= L_W_phys B_phys ||Lambda||.
```

where:

```text
L_W_phys := ||D_z Wbar P_phys||_op
B_phys   := ||P_phys d_S z_S||_*.
```

## What Source Support Actually Gives

If the compact matter/source worldtube is strictly inside the integration surface:

```text
supp(J_matter) cap S = empty
```

then:

```text
n . J_matter|S = 0.
```

That is useful. It removes ordinary matter-current leakage through a vacuum collar.

But it does not imply:

```text
d_S(g_pub, e_pub, mu_obs, reference, lambda, epsilon) = 0.
```

Vacuum exterior fields can still carry:

- multipoles and tidal gradients;
- stationary binding geometry;
- reference/readout convention drift;
- harmonic/corner boundary data;
- EM radiation or Poynting flux;
- constitutive/Hodge/alpha/current-normalization residuals.

So the theory cannot use local vacuum as a magic sponge. It has to either prove symmetry/annihilator conditions or bound the surviving physical drift.

## Reduced Bound Contract

The old 3152 finite target was:

```text
L_W B_z ||Lambda||_*.
```

3153 improves this to:

```text
L_W_phys B_phys ||Lambda||_*.
```

The single-survivor cap remains:

```text
L_W_phys B_phys ||Lambda||_* <= 5.970964001482571e-04
```

with eta cap:

```text
4.201081650315690e-16.
```

The six-way diagnostic cap remains:

```text
L_W_phys B_phys ||Lambda||_* <= 9.951606669137618e-05
```

with eta cap:

```text
7.001802750526150e-17.
```

The Poynting branch remains:

```text
|Int_partialW S_EM . dA dt| / M_H <= 5.970964001482571e-04
```

or:

```text
<= 9.951606669137618e-05
```

under equal diagnostic splitting.

## Gate Status

| gate | status | reason |
|---|---|---|
| fixed constants/labels have `d_S=0` | `pass_nonclaim` | only declared labels are removed |
| `Wbar` basic under boundary gauge/reparametrization | `not_claim_ready` | quotient owner not signed |
| compact source current misses `S` | `not_claim_ready` | source worldtube/profile is still an acquisition row |
| full `d_S z_S=0` from source support | `fail_for_claim` | false generically |
| reduced physical drift bound | `fail_for_claim` | `L_W_phys`, `B_phys`, and `||Lambda||` are missing |

## Decision

3153 does not promote local closure, local-GR recovery, WEP, R10, PPN, clock, orbital, Maxwell, or Newton claims.

It does move the derivation forward by replacing a false broad theorem:

```text
local vacuum => d_S z_S = 0
```

with a true reduced structure:

```text
local vacuum/source support removes compact current leakage,
gauge-basicness can remove pure boundary gauge drift,
physical multipole/reference/EM drift remains as B_phys.
```

So the next best attack is:

```text
3154:
prove Wbar is boundary-basic under tangential reparametrization/frame/U(1) gauge,
or fill the first B_phys component:
B_metric_multipole, B_reference_readout, or B_EM_flux_constitutive.
```

## Runner Artifacts

| artifact | path |
|---|---|
| inputs | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3153_INPUTS.csv` |
| source-support split | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3153_SOURCE_SUPPORT_DRIFT_SPLIT.csv` |
| level-set gates | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3153_LEVELSET_GATE_STATUS.csv` |
| physical drift components | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3153_PHYSICAL_DRIFT_COMPONENTS.csv` |
| reduced bound contract | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3153_REDUCED_BOUND_CONTRACT.csv` |
| score impact | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3153_SCORE_IMPACT.csv` |
| decision | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3153_DECISION.csv` |
| validation | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3153_VALIDATION.csv` |
| runner | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\scripts\Y5_R2FR_3153_source_support_levelset_split_or_physical_drift_bound.py` |
