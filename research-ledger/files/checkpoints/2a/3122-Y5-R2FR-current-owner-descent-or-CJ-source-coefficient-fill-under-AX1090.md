# 3122 - Current-Owner Descent or `C_J` Source-Coefficient Fill under AX1090

Private checkpoint. This follows 3121 by trying the theorem-zero route first, then filling the first conservative `C_J` coefficient from existing material/Coulomb rows without promoting it to a claim.

## Verdict

The exact descent result remains conditional:

```text
T_Q owner + fixed charge labels n_A + q-basic J_Q + public Hodge/Z_EM
+ variation-before-readout + radiative closure
=> C_J,S^ADM = 0
=> Delta(GM)_S/GM_S = 0 from delta_J.
```

The current corpus does not sign every clause. In particular, 1100/3119 still leave the same-current owner, no-source-weight, no-extra-`F^2`, and readout/radiative guards unsigned. So 3122 does not claim the zero theorem.

Instead it fills the first finite coefficient bridge using the existing Coulomb/material rows:

```text
C_J,A ~= 2 tau_EM,A Q_alpha,A + C_relax,A.
```

In the conservative smoke convention:

```text
tau_EM,A = 1,
C_relax,A = 0,
C_J,A ~= 2 Q_alpha,A.
```

This is not a full source-mass coefficient. It is a first executable material coefficient in the same current-normalization bridge. It tells us what the `delta_J` branch would look like if it reappears as an EM Coulomb/binding response.

## Source Register

| source_id | path | role |
|---|---|---|
| 1100 | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1100-Y5-R10-parent-TQ-owner-fixed-charge-lattice-and-gauge-norm-signature.md` | parent `T_Q`, gauge norm and current owner gaps |
| 3119 | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3119-Y5-R2FR-same-current-owner-or-deltaJ-source-test-residual-priority-under-AX1090.md` | same-current theorem attempt |
| 3121 | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3121-Y5-R2FR-deltaJ-source-calibration-DeltaGM-bridge-under-AX1090.md` | `DeltaGM_J` bridge law |
| WCM1053 | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1053_WEP_COMPOSITION_CHARGE_MATRIX.csv` | existing `Q_alpha` Coulomb material rows |
| MCON1061 | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1061_WEP_MATERIAL_CONVENTION.csv` | material-pair convention and `eta` target |
| local-bounds | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\local_bounds\local_bound_claims.csv` | MICROSCOPE WEP anchor |
| 3122-input | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3122_CJ_COEFFICIENT_FILL_INPUTS.csv` | coefficient fill inputs |
| 3122-runner | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\scripts\Y5_R2FR_3122_CJ_coefficient_fill_runner.py` | executable coefficient evaluator |

## Derivation

3121 showed:

```text
J_Q -> c_J J_Q
F_Q -> c_J F_Q
T_EM -> c_J^2 T_EM
Lie_v T_EM = 2 delta_J T_EM.
```

For a bound material body whose mass response to EM/Coulomb energy is represented by a material sensitivity:

```text
Q_alpha,A := partial ln m_A / partial ln alpha_EM
```

and current normalization changes the effective Coulomb piece as:

```text
alpha_EM -> c_J^2 alpha_EM
```

then:

```text
partial ln m_A / partial ln c_J
= 2 Q_alpha,A.
```

Allowing a nonuniform source weighting and relaxation tail gives:

```text
C_J,A = 2 tau_EM,A Q_alpha,A + C_relax,A.
```

This is the same law as 3121:

```text
C_J,S^ADM = 2 tau_EM,S f_EM,S^ADM + C_relax,S
```

but in a material-response convention where the existing `Q_alpha` rows play the role of the EM mass-fraction sensitivity.

## First Filled Rows

Using the existing WCM1053 smoke rows:

```text
Q_alpha(PtRh10) = 3.996544904717e-03,
Q_alpha(TA6V)   = 2.006736017892e-03.
```

With:

```text
tau_EM = 1,
C_relax = 0,
```

the runner computes:

```text
C_J(PtRh10) = 7.993089809434e-03,
C_J(TA6V)   = 4.013472035784e-03,
Delta C_J(TA6V-PtRh10) = -3.979617773650e-03.
```

This gives a one-channel, no-cancellation smoke implication:

```text
|delta_J| <= eta_bound / |Delta C_J|
```

with `eta_bound=2.8e-15`, so:

```text
|delta_J| <= 7.035851579866e-13
```

under the deliberately narrow assumptions:

```text
same source branch,
no other WEP channels,
tau_EM=1,
C_relax=0,
DD Coulomb smoke convention,
MICROSCOPE Ti/Pt pair convention,
no cancellation with mass/surface/direct/source-shadow/projector tails.
```

That bound is **not** an MTS claim. It is a useful scale: if `delta_J` is finite and lands in a Coulomb-like material channel, it is brutally constrained unless current-owner descent kills it.

## Why This Helps

3122 converts the coupling gap from:

```text
source coefficient missing
```

into:

```text
either derive current-owner descent,
or keep delta_J below a ~7e-13 one-channel Ti/Pt Coulomb smoke envelope,
or explain why the delta_J branch does not project into that material response.
```

That is real pressure on the theory. It also shows why your intuition that "the coupling is the key" was not noise: the whole local-GR/Newton/WEP bridge depends on whether the current normalization is parent-owned, universal/calibrated away, or leaks into material/source coefficients.

## Claim Status

No WEP, local-GR, Newtonian, PPN, orbital, source-`GM`, derived-`G`, or unification claim follows from 3122.

The internal advance is:

```text
current-owner zero route is restated exactly;
the first finite C_J material coefficient is computed from existing source rows;
a concrete delta_J smoke envelope is produced;
the source-GM route and WEP material route remain separated.
```

## Next Target

Write:

```text
3123-Y5-R2FR-current-owner-action-variation-or-deltaJ-projection-exclusion-under-AX1090.md
```

Direct target:

1. try to prove the same-current owner from action variation, not Ward conservation alone;
2. if that fails, classify whether `delta_J` projects into material Coulomb response, source `GM`, both, or neither;
3. if it projects into neither, state the parent projection reason explicitly rather than hiding it as calibration.
