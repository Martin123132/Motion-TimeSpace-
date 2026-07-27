# 4147 - Jordan-frame `G_eff` calibration or second-order source closure

## Decision
- Decision: `GEFF_CALIBRATION_CONDITIONS_DERIVED_LOCAL_CONSTANT_F_REQUIRED_SECOND_ORDER_SOURCE_BOUNDS_EMITTED`.
- The useful theorem is now exact: constant local `F(phi)=M_eff(phi)^2` is the condition for a one-time Newton coupling.
- Current corpus status: conditional theorem only; no Newton/local-GR/PPN claim.

## Coupling theorem
Take the Jordan-frame route from 4146:

`S_grav=(1/2)int sqrt|g| F(phi) R`, with `F(phi)=M_eff(phi)^2=M0^2+2 c_I phi`.

Metric variation gives

`F G_mn = T_mn + nabla_m nabla_n F - g_mn Box F + T_phi_mn`.

If

`F=F_*+O(v^6)`, `nabla F=O(v^6)`, and `T_phi_mn=O(v^6)`,

then through Newton and beta order

`G_mn=F_*^-1 T_mn+O(v^6)`,

so the measured local coupling is fixed once:

`G_ref=1/(8 pi F_*)`.

This is the clean answer to the Newton-constant question inside the MTS route: GR also takes `G` as a measured coupling, but here the Jordan parent route says exactly what object must be constant for MTS to inherit the same local coupling without smuggling.

## Drift law
If `F` varies, the variation is observable:

`delta G_ref/G_ref = - delta F/F_* + O((delta F/F_*)^2)`.

Equivalently:

`partial_a ln G_ref = - partial_a ln F`.

So time, radial, source, species, range, or frame dependence cannot be hidden inside measured `GM`; it becomes `Gdot`, source-charge, fifth-force/R10, WEP, or PPN residual debt.

## Second-order source closure
First-order Newton calibration is not enough. Variable `F` feeds beta order through

`S_beta^F=Pi_00^PPN[(nabla_0 nabla_0 F-g_00 Box F)+T_phi_00+T_phi_ii-deltaF F_*^-1 T_m]_[U^2]`.

Using the 4139 projector:

`delta_beta_source^F=-1/(2N_U2)<L_00^-1 S_beta^F,U^2>`.

Therefore `beta=1` follows only if `S_beta^F=0` by theorem, or if the bound row is numerically below the beta gate after Newtonian `G_ref` is fixed.

## Current verdict
| Gate | Result | Meaning |
|---|---|---|
| constant `F` theorem | CONDITIONAL_DERIVED | exact condition identified |
| local phi freeze/no scalar charge | MISSING | no live parent certificate yet |
| phi owner stress silence | UNSIGNED | staged, not adopted |
| live `Khat` adoption | UNSIGNED | still must use same parent response |
| beta source closure | BOUND_ROW_ONLY | no `beta=1` claim |

## Outputs
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4147_SOURCE_REGISTER.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4147_GEFF_CALIBRATION_THEOREM.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4147_CONSTANT_F_AUDIT.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4147_SECOND_ORDER_SOURCE_CLOSURE.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4147_COUPLING_BOUND_ROWS.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4147_DECISION_GATES.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4147_STATUS.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4147_NEXT_TARGET.csv`

## Next Target
- `4148-Y5-R2FR-local-phi-freeze-no-scalar-charge-or-coupling-drift-bound.md`
- Try to derive `delta_phi=0` through Newton/PPN order from the phi owner, mass gap, boundary data, or quotient/superselection rule; otherwise keep `Q_phi`, `dlnG_eff`, `D_deltaF_gradient`, and `delta_beta_source` as explicit nonclaim bounds.
