# 3154 - Wbar-Basic Quotient Theorem or Bphys First Component Bound under AX1090

Private checkpoint. This follows 3153:

```text
prove Wbar is boundary-basic under tangential reparametrization/frame/U(1) gauge,
or fill the first B_phys component:
B_metric_multipole, B_reference_readout, or B_EM_flux_constitutive.
```

## Result

3154 proves the clean conditional theorem for the gauge part:

```text
Wbar = Wtilde o pi_G
=> D_z Wbar[V_G] = 0.
```

Here:

```text
G_S := Diff(S) semidirect SO(1,3)_S semidirect U(1)_S
V_G := ker(D pi_G).
```

So if the parent action supplies a boundary quotient map:

```text
pi_G : z_S -> [z_S] / G_S
```

and `Wbar` is really a function of that quotient class, then pure tangential reparametrization, frame-gauge, and U(1)-gauge drift cannot enter `d_S W`.

This is a real annihilator theorem, not a closure axiom.

## Proof

Take a curve in the boundary-gauge orbit:

```text
z(t) = g(t).z
```

with tangent:

```text
V_G = d z(t)/dt |_{t=0}.
```

If `Wbar` descends to the quotient:

```text
Wbar(z) = Wtilde(pi_G(z)),
```

then along the gauge orbit:

```text
pi_G(z(t)) = pi_G(z).
```

Therefore:

```text
d/dt Wbar(z(t)) |_{t=0}
= D_z Wbar[V_G]
= 0.
```

So:

```text
D_z Wbar[d_S z_gauge] = 0
```

whenever `d_S z_gauge` is a genuine boundary-gauge tangent.

## Reduced Derivative

Starting from:

```text
d_S W = (D_z Wbar) o d_S z_S
```

and the 3153 split:

```text
d_S z_S =
  d_S z_const
  + d_S z_gauge
  + d_S z_support
  + d_S z_phys,
```

the best reduction is:

```text
d_S W = D_z Wbar[P_phys d_S z_S].
```

But this reduction is valid only when:

1. fixed labels/constants are genuinely fixed;
2. `Wbar` is parent-signed as boundary-basic;
3. compact source support removes ordinary matter-current crossing;
4. physical drift is not falsely reclassified as gauge.

## What Cannot Be Quotiented Away

3154 explicitly blocks the bad shortcut:

```text
physical drift = gauge drift.
```

The following remain physical until separately zeroed or bounded:

| component | meaning | zero route |
|---|---|---|
| `B_metric_multipole_tidal` | public metric/coframe/measure drift from multipoles, tides, binding fields, non-spherical source structure | exact stationary spherical monopole and symmetry surface |
| `B_reference_readout` | reference subtraction, projector/readout, calibration-surface drift | fixed quotient scalar reference chosen before comparison |
| `B_EM_flux_constitutive` | Poynting flux, hidden Hodge/constitutive drift, alpha/current normalization | public stationary Maxwell no-flux and metric-Hodge lock |
| `B_harmonic_corner` | cohomology, corner, residual surface data | parent-signed harmonic-free/corner-free boundary class |

Thus:

```text
B_phys <=
  B_metric_multipole_tidal
  + B_reference_readout
  + B_EM_flux_constitutive
  + B_harmonic_corner.
```

## Current Caps

For a single surviving derivative component:

```text
L_W_phys B_phys ||Lambda||_* <= 5.970964001482571e-04.
```

Under equal diagnostic splitting:

```text
L_W_phys B_phys ||Lambda||_* <= 9.951606669137618e-05.
```

For the Poynting component specifically:

```text
B_EM_flux_constitutive <= 5.970964001482571e-04
```

if it is the only survivor, or:

```text
<= 9.951606669137618e-05
```

under equal diagnostic splitting.

No component value is filled here.

## Gate Status

| gate | status | reason |
|---|---|---|
| boundary gauge group declared | `pass_nonclaim` | `G_S` and `V_G` are defined |
| basicness theorem | `pass_conditional_math` | quotient-basic functions annihilate quotient-vertical tangents |
| parent `Wbar` owner | `fail_for_claim` | `Wbar`, `pi_G`, and tangent domain are not sourced |
| no physical gauge overreach | `pass_nonclaim` | metric/reference/EM/harmonic drift remain physical |
| first `B_phys` component rows | `pass_nonclaim` | component contracts are staged |

## Meaning

This checkpoint removes a real piece of the fog.

Before:

```text
d_S z_gauge might contaminate d_S W.
```

After:

```text
if Wbar is boundary-basic, d_S z_gauge is harmless.
```

But the theorem does not touch physical geometry/flux/readout drift. So local closure is now narrowed to:

```text
L_W_phys B_phys ||Lambda||_*.
```

## Runner Artifacts

| artifact | path |
|---|---|
| inputs | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3154_INPUTS.csv` |
| theorem | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3154_WBAR_BASIC_QUOTIENT_THEOREM.csv` |
| gates | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3154_BASICNESS_GATE_STATUS.csv` |
| component rows | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3154_BPHYS_COMPONENT_BOUND_ROWS.csv` |
| scorecard | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3154_REDUCED_SCORECARD.csv` |
| decision | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3154_DECISION.csv` |
| validation | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3154_VALIDATION.csv` |
| runner | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\scripts\Y5_R2FR_3154_Wbar_basic_quotient_theorem_or_Bphys_first_component_bound.py` |

## Decision

3154 does not promote local closure, local-GR recovery, WEP, R10, PPN, clock, orbital, Maxwell, or Newton claims.

It does promote the next target to:

```text
3155:
derive exact monopole/symmetry zero for B_metric_multipole_tidal,
or source the first finite multipole/tidal boundary-drift row.
```

The reason to attack the metric component first is simple: if local Newton/PPN is the main bridge to GR, the first physical boundary drift to control is the public metric/coframe multipole/tidal drift.
