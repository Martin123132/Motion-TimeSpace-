# 3159 - Projection-Coefficient Derivation for J2 and Tide under AX1090

Private checkpoint. This follows 3158 by replacing symbolic `C2` and `Ctide` with explicit weak-field metric projection coefficients.

The target was:

```text
derive C2 and Ctide from the actual metric/source projection convention,
or bound them tightly enough that the 3158 reverse caps become a real gate.
```

## Projection Convention

3159 uses the local weak-field metric projection:

```text
g00 = -(1 + 2 Phi/c^2) + O(Phi^2)
gij =  (1 - 2 Phi/c^2) delta_ij + O(Phi^2)
```

This is used only as a public metric-component projection convention. It is not promoted to an MTS local-GR proof.

Because the AX1090 gate is a metric-component product gate, the metric perturbation amplitude carries the factor:

```text
2 Phi/c^2.
```

Using a potential-only norm would halve the coefficients and would mix conventions.

## J2 Coefficient

For the exterior Earth quadrupole:

```text
Phi_J2 = (GM/R) J2 (R_body/R)^2 P2(cos theta).
```

The metric perturbation amplitude is:

```text
|h_J2| = 2 epsilon_G |J2| (R_body/R)^2 |P2(cos theta)|.
```

Therefore:

```text
C2_full_shell = 2 max|P2| = 2.
```

For a local equatorial readout:

```text
P2(0) = -1/2,
```

so:

```text
C2_equatorial = 2 |P2(0)| = 1.
```

## Tide Coefficient

For an external Newtonian/electric-Weyl tide:

```text
Phi_tide = -1/2 E_ij x^i x^j.
```

Then:

```text
h00_tide = 2 Phi_tide/c^2 = -E_ij x^i x^j/c^2.
```

If `||E||` is the spectral norm/radial eigenvalue magnitude, then on a radius `R` domain:

```text
|h00_tide| <= ||E|| R^2/c^2.
```

Therefore:

```text
Ctide_spectral = 1.
```

## Updated Numeric Gate

Using 3158 source rows:

```text
epsilon_G |J2| = 7.528092708775573e-13.
```

The conservative full-shell metric projection gives:

```text
B_J2_full_shell = 2 epsilon_G |J2| = 1.505618541755115e-12.
```

So the AX1090 reverse ceiling becomes:

```text
L_Wphys_Lambda <= 3.965788037202410e8      single cap
L_Wphys_Lambda <= 6.609646728670684e7      equal cap
```

The local equatorial readout gives:

```text
B_J2_equatorial = epsilon_G |J2| = 7.528092708775573e-13.
```

So:

```text
L_Wphys_Lambda <= 7.931576074404820e8      single cap
L_Wphys_Lambda <= 1.321929345734137e8      equal cap
```

For the combined Sun+Moon radial tide smoke:

```text
B_tide = 1.140243262621331e-16.
```

So:

```text
L_Wphys_Lambda <= 5.236570297951847e12     single cap
L_Wphys_Lambda <= 8.727617163253077e11     equal cap
```

## Meaning

3159 removes one fake uncertainty.

`C2` and `Ctide` are not arbitrary coupling knobs under the selected public metric convention:

```text
C2 = 1 local equatorial point,
C2 = 2 conservative full shell,
Ctide = 1 spectral/radial tide norm.
```

This means the first sourced local domain is still not numerically fatal. The tightest conservative first-domain row is Earth J2 full-shell, and it still permits:

```text
L_Wphys_Lambda <= 3.97e8
```

under the single AX1090 cap.

But this is not a local-GR proof. The remaining missing object is now sharper:

```text
derive or bound L_Wphys_Lambda itself in the same parent-owned norm/projection convention.
```

## Claim State

No claim is promoted.

3159 does not claim:

- local closure;
- local-GR recovery;
- WEP;
- R10;
- PPN safety;
- clock safety;
- orbital safety;
- Maxwell recovery;
- Newtonian recovery.

Every generated row remains:

```text
valid_for_claim=false.
```

## Runner Artifacts

| artifact | path |
|---|---|
| runner | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\scripts\Y5_R2FR_3159_projection_coefficient_derivation_for_J2_and_tide.py` |
| inputs | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3159_INPUTS.csv` |
| derivation | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3159_PROJECTION_COEFFICIENT_DERIVATION.csv` |
| numeric reverse caps | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3159_NUMERIC_REVERSE_CAP_WITH_DERIVED_COEFFICIENTS.csv` |
| gates | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3159_GATE_STATUS.csv` |
| decision | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3159_DECISION.csv` |
| validation | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3159_VALIDATION.csv` |

## Decision

3159 promotes the next target to:

```text
3160-Y5-R2FR-LWphysLambda-parent-product-bound-or-zero-theorem-under-AX1090.
```

The next target should not ask again whether `C2` or `Ctide` are missing. They are now convention-derived for this first domain.

The next target is:

```text
derive L_Wphys_Lambda = 0,
or derive a parent Hodge/Wbar bound on L_Wphys_Lambda,
or prove the local branch must carry it as an explicit closure parameter.
```
