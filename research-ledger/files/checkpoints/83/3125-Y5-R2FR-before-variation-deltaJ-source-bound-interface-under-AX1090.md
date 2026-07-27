# 3125 - Before-Variation `delta_J` Source-Bound Interface under AX1090

Private checkpoint. This is the first strict bound interface after 3124 selected the finite before-variation branch:

```text
FINITE_BEFORE_VARIATION_PROJECTS_BOTH
```

The aim is not to make a public claim. The aim is to stop circling the coupling gap and turn the current live branch into a scoreable structure: one finite nonclaim `delta_J` envelope from material WEP, with source-GM, `Gdot`, R10, calibration, and readout kept as separate gates rather than mixed into a fake pass.

## Verdict

The strictest available numeric interface is:

```text
|delta_J| <= 7.035851579866459e-13
```

from the 3122 one-channel WEP smoke branch:

```text
Delta C_J(TA6V - PtRh10) = -0.003979617773650001
eta_bound = 2.8e-15
|delta_J| <= eta_bound / |Delta C_J|
```

This is useful, but not claimable:

```text
claim_allowed = false
```

because the coefficient is still a Coulomb-only smoke value with `tau_EM=1`, `C_relax=0`, and no parent-owned material/source current tensor.

## Bound Interface

For the selected before-variation insertion, write the differential material/WEP channel as:

```text
eta_AB ~ |Delta C_J^AB delta_J|
```

so the no-cancellation envelope is:

```text
|delta_J| <= eta_AB / |Delta C_J^AB|.
```

3122 provides a finite smoke value for:

```text
Delta C_J^TA6V-PtRh10 = C_J^TA6V - C_J^PtRh10.
```

The runner imports that row directly and tags it as:

```text
usable_for_rollup = true
claim_allowed = false
```

That distinction matters. It means the number can guide the next derivation, but it is not yet MTS evidence.

## Source-GM Separation

The source-GM bridge remains:

```text
Delta(GM)_S / (GM)_S = [C_J,S^ADM - C_J,cal^ADM] delta_J
```

with:

```text
C_J,S^ADM = 2 tau_EM,S f_EM,S^ADM + C_relax,S.
```

3125 does not import the WEP material coefficient into source-GM. That would be the wrong move. Source-GM needs:

```text
tau_EM_source,
f_EM_ADM_source,
C_relax_source,
calibration_reference.
```

Until those exist, the source-GM lane is blocked but structurally ready.

## R10 Separation

The R10 lane remains formula-only:

```text
alpha_X(lambda)
  = K_X^R10(lambda) beta_s_J(lambda) beta_t_J(lambda)
    + epsilon_tail_J(lambda).
```

This is not a numeric `delta_J` bound until the source/test current maps, kernel, tail, range, and real bound curve are filled.

## Calibration and Readout Guards

3125 keeps two traps out of the scoring path:

```text
universal current-unit rescaling -> calibration, not source-GM evidence
post-variation readout selector -> observed charge/material readout, not Hilbert EM stress/source GM
```

This protects the derivation from both overclaiming and false rejection.

## Runner Artifacts

| artifact | path |
|---|---|
| input rows | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3125_DELTAJ_BOUND_INTERFACE_INPUTS.csv` |
| output rows | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3125_DELTAJ_BOUND_INTERFACE_OUTPUT.csv` |
| validation | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3125_VALIDATION.csv` |
| gate | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3125_BOUND_INTERFACE_GATE.csv` |
| runner | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\scripts\Y5_R2FR_3125_deltaJ_bound_interface.py` |

## Current Gate

3125 moves the work forward by producing a real finite interface number while refusing to pretend it is a theorem:

```text
strict_rollup = 7.035851579866459e-13
claim_allowed = false
```

The next derivation should not be another broad missing-input sweep. It should attack the coupling directly:

```text
derive parent-owned C_J tensor/source-current map
```

or close the alternative:

```text
prove no-c_A/current-owner zero.
```

Either route would move the local GR/Newton/EM reduction spine more than another symbolic ledger.
