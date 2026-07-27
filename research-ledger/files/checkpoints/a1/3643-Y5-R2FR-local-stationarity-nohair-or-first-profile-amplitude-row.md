# 3643 Y5 R2FR local stationarity nohair or first profile amplitude row

**Status:** 3643 attempts the local stationarity/no-hair proof. The coercive energy identity gives an exact theorem-zero route, but the live corpus does not parent-sign operator ownership, coercivity, source silence, boundary no-flux, projector silence, stationarity, and topology. Therefore the branch now carries explicit A_X, ell_X, Q_X, dot_A_X, dot_ell_X, and dot_X_inf rows into Gdot, radial/orbital, PPN, and R10 bounds.

**Claim ceiling:** no local-GR/Newton, no-hair, Gdot, radial, PPN, or R10 pass is allowed from 3643.

## Theorem attempt

The clean no-hair route is real but conditional: if `L_X=(-D_X Delta_h+M_X^2)` is parent-owned and coercive, `J_X^eff=0`, boundary flux is zero, projector/calibration stress is silent, and there is no topological mode, then the energy identity forces `delta X_N=0`. That gives `A_X=Q_X=0`. Time silence additionally needs stationarity of the operator, source, boundary, and projector data.

## Live result

Those premises are not all parent-signed in the current corpus, so the branch cannot claim local no-hair. The fallback is now explicit: `A_X=A_src+A_bdy+A_top+A_proj+A_shell`, `ell_X=sqrt(D_X/M_X^2)`, and time coefficients `dot_A_X`, `dot_ell_X`, `dot_X_inf` feed the Gdot/radial/PPN/R10 bound rows.

## No-hair rows

- `NH3643_0_operator_contract`: CONDITIONAL_OPERATOR_FORM — L_X delta X_N := (-D_X Delta_h + M_X^2) delta X_N = J_X^eff on exterior domain Omega_ext, with D_X>0 and M_X^2>=0
- `NH3643_1_energy_identity`: EXACT_CONDITIONAL_ENERGY_IDENTITY — int_Omega D_X |grad delta X_N|^2 + M_X^2 delta X_N^2 = int_Omega J_X^eff delta X_N + int_boundary delta X_N n.D_X grad delta X_N
- `NH3643_2_zero_hair_branch`: THEOREM_ZERO_CONDITIONAL_NOT_PARENT_SIGNED — J_X^eff=0, boundary_flux=0, harmonic/topological sector=0, M_X^2>=0, D_X>0 => delta X_N=0 => A_X=Q_X=0
- `NH3643_3_time_stationarity_branch`: TIME_ZERO_CONDITIONAL_NOT_PARENT_SIGNED — partial_t L_X=0, partial_t J_X^eff=0, partial_t boundary_flux=0, partial_t projector=0 => partial_t delta X_N=0
- `NH3643_4_finite_amplitude_branch`: AMPLITUDE_ROW_REQUIRED — A_X = A_src + A_bdy + A_top + A_proj + A_shell, ell_X=1/sqrt(M_X^2/D_X) when M_X^2>0

## Premise audit

- `P3643_0_operator_owner`: MISSING_PARENT_OPERATOR_OWNERSHIP — L_X, D_X, M_X^2 are parent-owned with units
- `P3643_1_coercivity`: MISSING_COERCIVITY_SIGNATURE — D_X>0 and M_X^2>=0, plus cross terms bounded by eta<1
- `P3643_2_source_silence`: MISSING_SOURCE_SILENCE — J_X^eff=0 outside compact source and no residual source tail
- `P3643_3_boundary_no_flux`: MISSING_BOUNDARY_NOFLUX — boundary flux and relative cohomology class vanish
- `P3643_4_projector_silence`: MISSING_PROJECTOR_SILENCE — projector/readout/calibration carries no local profile source
- `P3643_5_stationarity`: MISSING_LOCAL_STATIONARITY — partial_t L_X=partial_t J_X=partial_t boundary=partial_t projector=0
- `P3643_6_topology`: MISSING_TOPOLOGY_CERTIFICATE — no harmonic/topological exterior mode

## Amplitude rows

- `AMP3643_0_master_profile`: delta X_N(r,t)=A_X(t) exp(-r/ell_X(t))/r + Q_X(t)/r + X_inf(t) | A_X=A_src+A_bdy+A_top+A_proj+A_shell | FIRST_PROFILE_AMPLITUDE_ROW_FILLED_NONCLAIM
- `AMP3643_1_source_component`: A_src | A_src ~ (1/(4*pi*D_X)) int_source e^{r'/ell_X} J_X^eff d^3x in spherical Green approximation | MISSING_SOURCE_CURRENT_VALUE
- `AMP3643_2_boundary_component`: A_bdy | A_bdy set by exterior boundary flux n.D_X grad(delta X_N) and relative cohomology class | MISSING_BOUNDARY_FLUX_VALUE
- `AMP3643_3_time_component`: dot_A_X;dot_ell_X;dot_X_inf | Xdot_N=dot_A_X exp(-r/ell_X)/r + A_X exp(-r/ell_X) dot_ell_X/ell_X^2 + dot_X_inf + projector/source-motion terms | MISSING_TIME_PROFILE_VALUES

## Bound updates

- `BU3643_0_gdot`: Gdot_clock — `|beta_common| <= (9.0e-13 yr^-1 + |explicit_t residuals|)/|dot_A_X e^{-r/ell_X}/r + A_X e^{-r/ell_X} dot_ell_X/ell_X^2 + dot_X_inf + projector/source-motion|`.
- `BU3643_1_radial`: orbital_radial — `partial_r X_N=-(1/r+1/ell_X) A_X e^{-r/ell_X}/r - Q_X/r^2; plug into beta_common radial hair bound`.
- `BU3643_2_ppn`: PPN_local_GR — `gamma-1 = C_qgamma[S_beta(A_X,Q_X,ell_X)] beta_common^2 + C_grad partial_r X_N + retained channels`.
- `BU3643_3_r10`: R10_short_range — `ell_X is the candidate lambda_X; A_X controls support/profile factor in alpha_common(lambda)`.

## Claim gates

- `G3643_0_nohair_promotion`: ENFORCED — No local no-hair/stationarity claim unless every premise is parent-signed.
- `G3643_1_amplitude_required`: ENFORCED — If any premise is unsigned, carry A_X/ell_X/Q_X and time-profile coefficients explicitly.
- `G3643_2_no_single_radius_calibration`: ENFORCED — A single calibrated GM/radius cannot erase radial profile hair.

## Next target

`3644-Y5-R2FR-profile-source-owner-or-first-amplitude-prior.md` via `scripts/Y5_R2FR_3644_profile_source_owner_or_first_amplitude_prior.py`.

## Sources

- `next_3642`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3642_NEXT_TARGET.csv` exists=True needle_found=True
- `profile_derivation_3642`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3642_LOCAL_XN_PROFILE_DERIVATION.csv` exists=True needle_found=True
- `profile_candidates_3642`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3642_XN_PROFILE_CANDIDATES.csv` exists=True needle_found=True
- `bound_updates_3642`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3642_BETA_BOUND_UPDATE_ROWS.csv` exists=True needle_found=True
- `elliptic_rebase_2606`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_KINETIC_ELLIPTIC_REBASE_2606_BOUNDARY_AMPLITUDE_THEOREM.csv` exists=True needle_found=True
- `gk_nohair_2470`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_GK_NOHAIR_2470_NOHAIR_PROOF_ATTEMPT.csv` exists=True needle_found=True
- `gk_positivity_2470`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_GK_NOHAIR_2470_POSITIVITY_CLAUSES.csv` exists=True needle_found=True
- `boundary_obstructions_549`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_BOUNDARY_COHOMOLOGY_NOHAIR_OBSTRUCTION_LEDGER.csv` exists=True needle_found=True
- `time_drift_row`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_time_drift_residual_or_zero.csv` exists=True needle_found=True
- `radial_mu_row`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_radial_mu_profile_or_zero.csv` exists=True needle_found=True
- `constant_gm_gate`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_CONSTANT_GM_DERIVATIVE_HAIR_GATE.csv` exists=True needle_found=True
