# CMB-Calibrated Joint Growth Stress

## 1. Purpose

This file follows:

```text
36-parent-CMB-calibration-map-attempt.md
```

The question is:

```text
If we take the CMB-calibrated C0 frozen-shape row seriously as a closure
diagnostic, does the same parameter row wreck the growth diagnostic?
```

Short answer:

```text
no. The native CMB-calibrated frozen-shape row keeps growth close to the locked
C0 row while fitting the compressed CMB distance prior. This preserves it as an
interesting closure diagnostic, but it is still not evidence because the row
was calibrated on the CMB prior and the parent map is missing.
```

## 2. Machine Run

Implemented:

```text
scripts/CMB_calibrated_joint_growth_stress.py
```

Successful run:

```text
runs/20260531-005015-CMB-calibrated-joint-growth-stress/status.json
```

Readout:

```text
CMB_calibrated_closure_retained_growth_near_locked_not_evidence
```

## 3. Main Stress Result

Fixed no-SH0ES locked C0:

```text
chi2_growth_primary = 14.930776159766813
chi2_growth_full_shape_only = 15.294371129697419
chi2_CMB_repaired = 295.0481129416254
```

Native C0 CMB-calibrated frozen-shape row:

```text
chi2_growth_primary = 15.320425017819245
chi2_growth_full_shape_only = 16.28288410248863
chi2_CMB_repaired = 3.4632081390356074e-10
```

Growth deltas versus locked C0:

```text
primary growth delta = 0.389648858052432
full-shape growth delta = 0.9885129727912112
```

This passes the closure stress gate:

```text
the CMB-calibrated row does not destroy the growth signal.
```

## 4. Baseline Context

Fixed baselines:

```text
LCDM growth primary = 15.682412358967213
wCDM growth primary = 14.463332089064483
CPL growth primary = 17.110842020618023
```

Native C0 CMB-calibrated row:

```text
growth delta versus best fixed baseline = 0.8570929287547617
```

So growth remains near the normal baseline pack.

## 5. The Trap

The total score looks excellent:

```text
native C0 calibrated chi2_growth + chi2_CMB = 15.320425018165565
delta total versus best fixed baseline = -37.1482278157956
```

But this number is not a valid model-selection claim because:

```text
the C0 calibrated rows were trained on the same compressed CMB distance prior.
```

So the only allowed conclusion is:

```text
same-parameter closure stress passed.
```

Not:

```text
C0 beats LCDM/wCDM/CPL.
```

## 6. Gate Result

Passed:

```text
source 36 complete;
native calibrated primary growth not worse than locked C0 by 2 chi2;
native calibrated full-shape growth not worse than locked C0 by 2 chi2;
native calibrated CMB distance chi2 near exact.
```

Failed:

```text
joint model-selection claim;
CMB-calibrated support claim;
public claim.
```

## 7. Decision

Allowed language:

```text
the native CMB-calibrated C0 closure row remains empirically interesting because
it fixes the compressed CMB-distance residual without wrecking growth.
```

Forbidden language:

```text
MTS beats LCDM;
CMB supports MTS;
the calibrated branch is derived;
this is an independent holdout result.
```

## 8. Next Target

Create:

```text
38-calibrated-closure-holdout-contract.md
```

Purpose:

```text
predeclare what would make this CMB-calibrated closure row meaningful: freeze
the calibrated row, choose an independent holdout or stronger likelihood route,
and forbid further parameter rescue.
```
