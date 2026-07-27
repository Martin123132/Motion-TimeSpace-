# 3697 - Direct leakage penalty from coarse-graining Onsager or closure

Private checkpoint. No GitHub action. No local-GR/Newton/R10/PPN/EM claim.

## Status
- `DIRECT_LEAKAGE_PENALTY_THEOREM_SHAPED_BUT_PARENT_ENTROPY_ONSAGER_OBJECT_MISSING_CLOSURE_ONLY`
- A coarse-grained entropy/free-energy maximum plus Onsager/open-system dynamics would derive U_Z=u_1 s_L, but the corpus does not yet own S_cg, T_eff, C_AB~G_AB, FDT/noise, units, source silence, or one environment law. Therefore u_1 remains closure-only/nonclaim for local mass-gap screening.

## Main Result
- A real derivation of `U_Z=u_1 s_L` is possible in form, but not yet supplied by the corpus.
- Entropy/free-energy route: if `S_cg=S_0-0.5 C_AB z^A z^B+O(z^4)`, then `F_cg=-T_eff S_cg` gives `U_Z=0.5 T_eff C_AB z^A z^B`.
- To recover the 3695 mass-gap law, the Hessian must align with the leakage metric: `C_AB=2u_1 T_eff^{-1}G_AB+C_perp`, with `C_perp` zero or bounded.
- Onsager route supplies dynamics, `dot z=-L partial F_cg`, but it does not supply `u_1` unless `F_cg/S_cg` is parent-derived.

## Verdict
- The theorem shape is good.
- The parent object is missing.
- Therefore `u_1` is closure-only/nonclaim until a parent entropy/free-energy/Onsager object is built.

## Entropy Derivation Rows
- `EDR3697_0_state`: coarse-grained local state | `STATE_SPACE_CANDIDATE_NOT_PARENT_COMPLETE` | X=(X_L,z^A), z=0 is the local fixed point, s_L=G_AB z^A z^B
- `EDR3697_1_entropy_maximum`: entropy/free-energy maximum | `THEOREM_FORM_DERIVED_ENTROPY_FUNCTIONAL_MISSING` | S_cg(X_L,z)=S_0(X_L)-0.5 C_AB(X_L) z^A z^B+O(z^4), C_AB>=0
- `EDR3697_2_free_energy`: free-energy penalty | `FORMAL_ROUTE_READY_TEFF_AND_CAB_MISSING` | F_cg=-T_eff S_cg => U_Z=0.5 T_eff C_AB z^A z^B+O(z^4)
- `EDR3697_3_metric_alignment`: alignment with G_AB | `ALIGNMENT_CONDITION_DERIVED_NOT_SIGNED` | C_AB=2u_1 T_eff^{-1} G_AB + C_perp, with ||C_perp|| bounded or symmetry-forbidden
- `EDR3697_4_units`: units and normalization | `UNITS_NORMALIZATION_MISSING` | [u_1] is fixed by the action density convention; T_eff C_AB/2 must match the response-action mass term units
- `EDR3697_5_verdict`: entropy route verdict | `ENTROPY_ROUTE_CONDITIONAL_CLOSURE_IF_UNSIGNED` | entropy maximum would derive U_Z=u_1 s_L if S_cg, T_eff, C_AB~G_AB and units are parent-owned

## Onsager Rows
- `ONR3697_0_gradient_flow`: Onsager gradient flow | `FORMAL_OPEN_SYSTEM_ROUTE_READY_PARENT_L_MISSING` | dot z^A = -L^{AB} partial_B F_cg + noise/source terms
- `ONR3697_1_OM_action`: Onsager-Machlup/doubled action | `FORMAL_DOUBLED_ACTION_ROUTE_NOT_PARENT_BUILT` | S_OM ~ int (dot z + L C z)^T (4L)^{-1} (dot z + L C z)
- `ONR3697_2_static_limit`: static local gap | `STATIC_REDUCTION_REQUIRED` | omega_H ~ eigen(L C), mu_H^2 ~ eigen(G_H^{-1} T_eff C) after static/elliptic reduction
- `ONR3697_3_noise_FDT`: fluctuation-dissipation consistency | `FDT_OR_NOISE_NORMALIZATION_MISSING` | noise covariance ~ 2 L T_eff if the open system is thermal/effective-equilibrium
- `ONR3697_4_verdict`: Onsager route verdict | `ONSAGER_ROUTE_CONTRACT_ONLY` | Onsager can justify the dynamics around U_Z but does not by itself supply u_1 unless F_cg/S_cg is parent-derived

## Closure Classifier
- `CLC3697_0_claim_branch`: claim-eligible direct penalty | `NOT_AVAILABLE_CURRENTLY` | S_cg/T_eff/C_AB/G_AB/u_1/source silence/environment dependence all parent-owned
- `CLC3697_1_closure_branch`: disciplined closure | `AVAILABLE_NONCLAIM` | declare U_Z=u_1 s_L and pass u_1 to Yukawa runner with valid_for_claim=false
- `CLC3697_2_no_penalty_branch`: no local mass-gap branch | `AVAILABLE_BUT_STRICT` | u_1=0 or not introduced; local safety must come from exact projection/metric-null/vertical theorem only
- `CLC3697_3_phenomenology_branch`: Yukawa phenomenology | `AVAILABLE_NONCLAIM` | lambda_H and alpha_A fitted/sourced per shared closure parameters, then tested against R10/PPN/clocks/WEP/EM/orbits

## Source-Silence Gates
- `SS3697_0_matter`: ordinary matter silence | `UNSIGNED` | partial_z S_matter=0 at fixed q/Psi/theta and no z-dependent species masses
- `SS3697_1_EM`: EM charge/stress silence | `UNSIGNED` | partial_z Z_EM=0 and partial_z alpha_fs=0 unless quotient-owned
- `SS3697_2_Newton`: Newton normalization silence | `UNSIGNED` | partial_z G_N^obs=0 after fixed-point calibration, or residual alpha/lambda row must be scored
- `SS3697_3_environment`: environment dependence guard | `UNSIGNED` | u_1(local), u_1(galaxy), u_1(cosmic) come from one function of X_B, not per-arena selection

## Decisions
- `DEC3697_0`: `FORMAL_ROUTE_IDENTIFIED` - A parent entropy/free-energy maximum can derive U_Z=u_1 s_L and an Onsager action can supply dynamics.
- `DEC3697_1`: `CLAIM_BLOCKED` - The corpus does not yet supply S_cg, T_eff, C_AB~G_AB, units, FDT/noise, or source silence.
- `DEC3697_2`: `CLOSURE_ONLY_FOR_NOW` - Until the parent object is derived, u_1 must be treated as closure/nonclaim and scored through the Yukawa runner.

## Claim Gates
- `CG3697_0_entropy`: `BLOCKED` - parent S_cg/free-energy functional missing
- `CG3697_1_alignment`: `BLOCKED` - entropy Hessian C_AB~G_AB not derived
- `CG3697_2_units`: `BLOCKED` - T_eff/action normalization and units missing
- `CG3697_3_onsager`: `BLOCKED` - doubled/open-system Onsager action not built
- `CG3697_4_source_silence`: `BLOCKED` - ordinary matter/EM/Newton source silence not signed
- `CG3697_5_environment`: `BLOCKED` - single u_1(X_B) environment law not derived
- `CG3697_6_local_GR`: `BLOCKED` - local GR mass-gap screening is closure-only until above gates pass
- `CG3697_7_public`: `BLOCKED` - private checkpoint only; no public/GitHub claim

## Source Register
- `handoff_3696`: exists=True, needle_found=True, path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3696_NEXT_TARGET.csv`
- `contract_3696`: exists=True, needle_found=True, path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3696_DIRECT_PENALTY_CONTRACT_ROWS.csv`
- `u1_origin_3696`: exists=True, needle_found=True, path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3696_U1_ORIGIN_ROWS.csv`
- `coarse_XB_85`: exists=True, needle_found=True, path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\85-coarse-graining-invariants-XB.md`
- `DL_silence_122`: exists=True, needle_found=True, path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\122-parent-DL-fixed-point-silence.md`
- `fixed_point_124`: exists=True, needle_found=True, path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\124-fixed-point-extremality-origin.md`
- `red_team_06`: exists=True, needle_found=True, path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\06-consistency-red-team.md`
- `equations_05`: exists=True, needle_found=True, path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\05-equation-register.md`
- `metric_null_138`: exists=True, needle_found=True, path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\138-metric-null-action-block-contract.md`
- `scalar_evenness_126`: exists=True, needle_found=True, path=`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\126-scalar-evenness-origin.md`

## Next Target
- `3698-Y5-R2FR-parent-entropy-free-energy-object-or-u1-closure-runner.md`
- Objective: attempt to construct the parent S_cg/F_cg object with Hessian C_AB aligned to G_AB and source-silence gates; if absent, write explicit u1 closure runner rows for local Yukawa tests
