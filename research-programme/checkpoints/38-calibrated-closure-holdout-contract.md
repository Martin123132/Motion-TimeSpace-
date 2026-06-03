# Calibrated Closure Holdout Contract

## 1. Purpose

This file follows:

```text
37-CMB-calibrated-joint-growth-stress.md
```

The question is:

```text
What are the no-rescue rules before the native CMB-calibrated C0 closure row is
tested again?
```

Short answer:

```text
freeze the calibrated row exactly. The row may be used only as a closure
candidate. No parameter rescue, no CMB-prior model-selection claim, and no
public support language are allowed.
```

## 2. Machine Run

Implemented:

```text
scripts/calibrated_closure_holdout_contract.py
```

Successful run:

```text
runs/20260531-005438-calibrated-closure-holdout-contract/status.json
```

Readout:

```text
calibrated_closure_holdout_contract_frozen_no_rescue
```

## 3. Frozen Row

The frozen branch is:

```text
C0_native_bmem_CMB_calibrated_shape_frozen
```

Locked parameters:

```text
h0 = 67.71676410614398
Omega_m0 = 0.31988262346779694
b_mem = 0.027085159773612907
alpha_act = 1.0543379145228584
nu_act = 1.7500073382761008
rd = 147.29909165793796
```

Growth nuisance:

```text
sigma8_0 = 0.8738706429542475
```

`sigma8_0` may vary only if every baseline gets the exact same predeclared
one-parameter treatment.

## 4. Already Consumed Data

Not independent anymore:

```text
Planck 2018 compressed distance prior;
SDSS/eBOSS DR16 BAO-plus growth;
SDSS/eBOSS DR16 full-shape growth.
```

Available as a guardrail, not evidence:

```text
Pantheon+/DESI late-background backreaction stress.
```

Reason:

```text
the original C0 shape came from late-background work, but the CMB-calibrated
row changed H0/Omega_m0/b_mem. We can test whether that calibration wrecks
late-background consistency, but it is not a fresh discovery claim.
```

## 5. No-Rescue Rules

Forbidden after this point:

```text
move h0;
move Omega_m0;
move b_mem;
move alpha_act or nu_act;
change covariance/data cuts only for C0;
reuse the compressed CMB prior as independent evidence;
add perturbation knobs without parent derivation;
use public support/falsification language.
```

If any of these are violated:

```text
the branch restarts as a new training branch and the old holdout is invalid.
```

## 6. Holdout Route Register

Priority 1:

```text
late_background_backreaction_guardrail
```

Purpose:

```text
score the frozen CMB-calibrated row on the no-SH0ES SN/BAO background path and
ask whether CMB calibration catastrophically worsens late-background consistency.
```

Priority 2:

```text
fresh_growth_or_RSD_holdout
```

Priority 3:

```text
official_CMB_spectra_lensing_fixed_params
```

Priority 4:

```text
parent_calibration_map_repair
```

## 7. Gate Result

Passed:

```text
source 37 complete;
native calibrated row frozen;
no-rescue rules declared;
available next guardrail exists.
```

Failed by design:

```text
independent support claim;
public claim.
```

## 8. Decision

Allowed language:

```text
the native CMB-calibrated C0 row is a frozen closure candidate worth one
no-rescue guardrail pass.
```

Forbidden language:

```text
the calibrated row is evidence;
the calibrated row beats LCDM/wCDM/CPL;
the CMB prior supports MTS;
the parent map is derived.
```

## 9. Next Target

Create:

```text
39-calibrated-background-backreaction-guardrail.md
```

Purpose:

```text
with the calibrated row frozen, test whether it ruins late-background SN/BAO
consistency. This is a guardrail, not a proof.
```
