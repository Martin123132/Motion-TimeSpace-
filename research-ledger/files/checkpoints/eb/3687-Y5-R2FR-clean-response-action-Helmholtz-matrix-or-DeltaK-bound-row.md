# 3687 - Clean response action Helmholtz matrix or DeltaK bound row

**Status:** CLEAN_BULK_HELMHOLTZ_DERIVED_LIVE_KHAT_MATCH_NOT_CLAIMED_DELTAK_COMPONENT_VECTOR_STAGED

This checkpoint does the promised Helmholtz/`Delta_K` test. It closes the formal bulk Helmholtz problem for the clean response action under explicit symmetry/self-adjointness clauses, then separates that theorem from the still-unmatched live `K_hat` symbols.

## Main result

Clean bulk Euler operator:

`E_A = -D_mu(G_AB D^mu Y^B) + M_AB Y^B + O(Y^3) - J_A - B_A`.

Helmholtz matrix:

`H_AB := delta E_A/delta Y^B - (delta E_B/delta Y^A)^dagger`.

Bulk theorem:

`H_AB^clean_bulk=0` if `G_AB=G_BA`, `M_AB=M_BA`, `D_mu` is compatible with the internal pairing, constraints/gauge modes are removed, and boundary adjoint terms vanish.

Metric response obstruction:

`H_K^{mu nu|alpha beta}:=delta(sqrt(-g)K_hat^{mu nu})/delta g_alpha_beta - delta(sqrt(-g)K_hat^{alpha beta})/delta g_mu_nu` is zero automatically only for an action-defined `K_metric`, not for the old/live `K_hat` symbols unless they are matched.

DeltaK split:

`Delta_K^{mu nu} := K_hat_live^{mu nu} - K_metric^{mu nu}[Gamma_eff]`.

`R_DeltaK = R_DeltaK_grad+R_DeltaK_coeff+R_DeltaK_projector+R_DeltaK_boundary+R_DeltaK_flux`.

Reduced residual:

`abs(R_Helmholtz)/N_H <= (|R_H_live_symbol|+|R_H_conn|+|R_H_boundary|)/N_H`.

## Helmholtz matrix rows
- `HMX3687_0_clean_bulk_operator`: BULK_HELMHOLTZ_DERIVED_CONDITIONALLY - field Euler operator -> This is genuine progress: integrability is automatic for the clean action, not a new empirical axiom.
- `HMX3687_1_mass_matrix`: ZERO_IF_SYMMETRIC_MASS_MATRIX - zeroth-order Helmholtz block -> A parent even response sector must choose a symmetric/coercive M_AB.
- `HMX3687_2_kinetic_matrix`: ZERO_IF_SYMMETRIC_COMPATIBLE_KINETIC_PAIRING - second-order Helmholtz block -> This is the exact mathematical condition under the 'motion field' language: the response medium must have a self-adjoint local stiffness.
- `HMX3687_3_connection_projector`: OPEN_LIVE_PROJECTOR_INPUT - connection/readout Helmholtz block -> The clean action can absorb a connection only if the connection is part of the parent geometry, not a fitted readout.
- `HMX3687_4_metric_Helmholtz`: CLOSED_FOR_ACTION_DEFINED_KMETRIC_NOT_FOR_LIVE_KHAT - metric response integrability -> This separates the theorem branch from the old-symbol branch.
- `HMX3687_5_boundary`: OPEN_BOUNDARY_CONVENTION - boundary adjoint block -> Bulk Helmholtz closure does not silence linked-surface mass/force leakage.
- `HMX3687_6_verdict`: BULK_THEOREM_PROGRESS_LIVE_CLAIM_BLOCKED - Helmholtz status -> 3687 closes the formal bulk Helmholtz rung but does not close the live local-GR branch.

## DeltaK decomposition
- `DK3687_0_definition`: DEFINITION_READY - total Delta_K -> `Delta_K must vanish in the same convention used by T_GK=Gamma_eff g-K_metric`
- `DK3687_1_gradient_piece`: OPEN_COMPONENT_MATCH - gradient/elastic piece -> `R_DeltaK_grad`
- `DK3687_2_coefficient_response`: OPEN_COEFFICIENT_RESPONSE - metric-dependent coefficients -> `R_DeltaK_coeff`
- `DK3687_3_projector_readout`: OPEN_PROJECTOR_OWNER - projector/readout piece -> `R_DeltaK_projector`
- `DK3687_4_boundary`: OPEN_BOUNDARY_NO_FLUX - boundary/improvement piece -> `R_DeltaK_boundary`
- `DK3687_5_flux`: SEPARATE_EM_BRANCH_NOT_LOCAL_ZERO_PROOF - physical EM/Poynting/wave flux piece -> `R_DeltaK_flux`
- `DK3687_6_live_verdict`: DELTAK_ZERO_NOT_CLAIMED_COMPONENT_VECTOR_STAGED - live symbol match -> `R_DeltaK = R_DeltaK_grad+R_DeltaK_coeff+R_DeltaK_projector+R_DeltaK_boundary+R_DeltaK_flux`

## Live symbol match audit
- `LMA3687_0_clean_bulk`: pass_now=True - bulk clean response action -> not enough to claim live K_hat
- `LMA3687_1_formal_Kmetric`: pass_now=True - formal K_metric formula -> compare to live K_hat
- `LMA3687_2_live_Khat_identity`: pass_now=False - live K_hat=K_metric -> R_DeltaK
- `LMA3687_3_live_Helmholtz`: pass_now=False - live K_hat Helmholtz test -> R_H_live_symbol
- `LMA3687_4_boundary_projector`: pass_now=False - boundary/projector compatibility -> R_H_conn+R_H_boundary+R_DeltaK_projector
- `LMA3687_5_source_coupling`: pass_now=False - J_A local source silence -> R_linear_source
- `LMA3687_6_verdict`: pass_now=False - live local-GR branch -> local-GR/Newton claim remains blocked

## Residual bound rows
- `RHB3687_0_Helmholtz_reduced`: BULK_HELMHOLTZ_ZERO_CLEAN_BRANCH_LIVE_INPUTS_MISSING - `abs(R_Helmholtz)/N_H` -> `(|R_H_live_symbol|+|R_H_conn|+|R_H_boundary|)/N_H`; clean bulk Helmholtz is no longer the gap; live symbol, connection/projector and boundary pieces remain
- `RHB3687_1_DeltaK_total`: FORMULA_READY_COMPONENT_INPUTS_MISSING - `abs(R_DeltaK)/N_H` -> `(|R_DeltaK_grad|+|R_DeltaK_coeff|+|R_DeltaK_projector|+|R_DeltaK_boundary|+|R_DeltaK_flux|)/N_H`; explicit tensor mismatch vector replacing the vague Khat-match blocker
- `RHB3687_2_q_loc_profile`: WARD_PROFILE_READY_NUMERIC_INPUTS_MISSING - `q_loc^nu` -> `q_loc^nu = P_loc^nu_rho(E_A R_A^rho + B_GK^rho - nabla_mu Delta_K^{mu rho})`; testing can proceed once E_A/J_A, B_GK, Delta_K and P_loc coefficients are sourced
- `RHB3687_3_live_tensor_input`: MISSING_SOURCE_INPUT - `K_hat_live component table` -> `MISSING_KHAT_LIVE_COMPONENT_ROWS`; the next work must build a component map, not another free-form prose audit
- `RHB3687_4_coupling_input`: MISSING_COUPLING_INPUT - `J_A source coupling coefficient` -> `MISSING_J_A_ZERO_THEOREM_OR_BOUND`; the coupling suspicion is now a concrete Euler-source row

## Decisions
- `DEC3687_0_result`: BULK_HELMHOLTZ_CLOSED_CONDITIONALLY - the clean response action passes the bulk Helmholtz test under explicit symmetry/self-adjointness clauses -> stop treating Helmholtz as mystical; the live problem is Khat matching and source/boundary leakage
- `DEC3687_1_DeltaK`: DELTAK_VECTOR_STAGED - Khat mismatch is decomposed into gradient, coefficient, projector, boundary and flux components -> next build the live component map and try to collapse pieces
- `DEC3687_2_coupling`: COUPLING_REMAINS_CORE - J_A enters q_loc through the derived Euler source law -> later target J_A=0 theorem or finite source-backed coefficient
- `DEC3687_3_EM`: POYNTING_VECTOR_ALLOWED_AS_PHYSICAL_STRESS - flux can live in K_flux only as explicit EM/wave stress -> do not use Poynting stress as hidden local-GR closure
- `DEC3687_4_next`: NEXT_BEST_TARGET - live Gamma/Khat component map is now the route with least ambiguity -> run 3688 Khat component map to clean response or Delta_K component bound
- `DEC3687_5_private`: PRIVATE_NONCLAIM - no local-GR/Newton/public claim follows yet -> continue derivation privately

## Claim gates
- `CG3687_0_Helmholtz_live`: BLOCKED_LIVE_COMPONENTS - claim live Gamma/Khat variational integrability because bulk clean branch passes, but live Khat components are not source-matched
- `CG3687_1_DeltaK_zero`: BLOCKED_COMPONENT_MATCH - claim Delta_K=0 because gradient/coefficient/projector/boundary/flux pieces are not matched under one convention
- `CG3687_2_q_loc_zero`: BLOCKED_DELTAK_JA_BOUNDARY_PLOC - claim local q_loc^nu=0 because Ward profile still contains E_A/J_A, boundary and Delta_K terms
- `CG3687_3_Newton_GR`: BLOCKED_LOCAL_BRANCH - claim derived Newton/local-GR limit because Khat match and source coupling are not closed
- `CG3687_4_public_or_github`: BLOCKED_PRIVATE - public/GitHub promotion because private checkpoint only

## Next target
`3688-Y5-R2FR-live-Gamma-Khat-component-map-to-clean-response-or-DeltaK-component-bound.md` via `scripts/Y5_R2FR_3688_live_Gamma_Khat_component_map_to_clean_response_or_DeltaK_component_bound.py`.

## Sources
- `handoff_3686`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3686_NEXT_TARGET.csv` exists=True needle_found=True
- `candidate_3686`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3686_RESPONSE_ACTION_CANDIDATE_ROWS.csv` exists=True needle_found=True
- `gate_3686`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3686_HELMHOLTZ_GATE_ROWS.csv` exists=True needle_found=True
- `bound_3686`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3686_RGK_ACTION_BOUND_ROWS.csv` exists=True needle_found=True
- `metric_3627`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3627_GAMMA_KHAT_METRIC_RESPONSE_DERIVATION.csv` exists=True needle_found=True
- `helmholtz_3627`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3627_SGK_HELMHOLTZ_ACTION_GATE.csv` exists=True needle_found=True
- `audit_3432`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3432_GAMMA_KHAT_OWNER_AUDIT.csv` exists=True needle_found=True
- `match_2807`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_2807_GAMMA_KHAT_METRIC_RESPONSE_MATCH.csv` exists=True needle_found=True
- `match_audit`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_GK_METRIC_RESPONSE_MATCH_AUDIT.csv` exists=True needle_found=True
- `response_variation`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_RESPONSE_DOUBLET_ACTION_VARIATION.csv` exists=True needle_found=True
- `response_metric`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_RESPONSE_DOUBLET_METRIC_RESPONSE_LEDGER.csv` exists=True needle_found=True
- `khat_2409`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2409_KHAT_METRIC_RESPONSE_MATCH_AUDIT.csv` exists=True needle_found=True
- `helmholtz_3419`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3419_HELMHOLTZ_AUDIT.csv` exists=True needle_found=True
- `coupling_3629`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3629_RESPONSE_DOUBLET_COUPLING_LAW.csv` exists=True needle_found=True
