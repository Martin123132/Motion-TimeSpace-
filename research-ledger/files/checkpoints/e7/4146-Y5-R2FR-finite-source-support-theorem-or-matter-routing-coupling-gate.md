# 4146 - Finite-source support theorem or matter-routing coupling gate

## Decision
- Decision: `SUPPORT_ONLY_THEOREM_REJECTED_MATTER_ROUTING_CONSTRUCTED_NOT_LIVE_SIGNED_FINITE_SOURCE_BOUND_ROWS_EMITTED`.
- Support-only route: rejected.
- Matter-routing route: constructed, but not live-signed.
- Claim ceiling: no local-GR, Newton, PPN, R10, WEP, clock, orbital, or public evidence claim follows from 4146.

## Why exterior readout is not enough
4145 showed `phi G_TF=0` on a genuine vacuum annulus. That is useful, but PPN beta is not only a pointwise exterior tensor test; it is a Green-solved metric coefficient.

For the finite-source curvature channel,

`delta_beta_phiG=-1/(2N_U2)<L_00^-1 S_phiG,U^2 W_out>_Omega_out`.

Introduce the adjoint readout field:

`L_00^dagger chi_out=U^2 W_out`.

Then

`delta_beta_phiG=-1/(2N_U2)<S_phiG,chi_out>_B + boundary/support terms`.

So an exterior readout window still carries an interior body weight

`chi_out(x')=int_Omega_out G_00(x,x') U(x)^2 W_out(x)d^3x`.

That is generically nonzero for source points `x'` inside the body. Therefore vacuum support alone does not prove finite-source beta safety.

## Matter-routing route
The better route is not to delete `2 phi G_TF`. It is to stop treating it as a stray RHS force.

Adopt a Jordan-frame parent gravitational term:

`S_grav=(1/2)int sqrt|g| M_eff(phi)^2 R`, with `M_eff(phi)^2=M0^2+2 c_I phi`.

Then the `phi G_mn` term is part of `M_eff(phi)^2 G_mn`, i.e. part of the gravitational coupling/Planck-mass side. The finite-source term is routed into the same source-normalization ledger that defines measured `G_ref`, not hidden as a separate force.

This is only legal if the live theory supplies:
- one observed frame for matter, clocks, rods and EH/source variation;
- `G_ref=1/(8 pi M_eff(phi_*)^2)` with no time, range, species, frame, or source dependence;
- live `Khat_current^TF` adoption of the parent response;
- phi owner stress and zero-mode accounting;
- second-order PPN source closure so beta is not spoiled after Newtonian calibration.

## Updated residual
After 4145:

`D_TF=2 phi G_TF + D_owner + D_adoption`.

The support-only route gives:

`delta_beta_phiG=-1/(2N_U2)<Pi_00[16 pi G phi T_TF],chi_out>_B + boundary/support terms`.

The constructed Jordan route gives:

`D_TF -> D_owner + D_adoption + D_Geff_mismatch + D_deltaF_gradient + D_second_order_source`.

So the hard problem has moved from "why is finite-source `phi G_TF` zero?" to "can MTS derive one constant universal coupling and second-order source closure?"

## Outputs
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4146_SOURCE_REGISTER.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4146_SUPPORT_THEOREM_ATTEMPT.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4146_MATTER_ROUTING_CONTRACT.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4146_FINITE_SOURCE_BOUND_ROWS.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4146_RESIDUAL_UPDATE.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4146_DECISION_GATES.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4146_STATUS.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4146_NEXT_TARGET.csv`

## Next Target
- `4147-Y5-R2FR-Jordan-frame-Geff-calibration-or-second-order-source-closure.md`
- Try to derive the live constant-universal `G_eff` calibration for the `M_eff(phi)^2 R` route and show beta-order source stability; otherwise emit `D_Geff_mismatch` and `delta_beta_source` bounds.
