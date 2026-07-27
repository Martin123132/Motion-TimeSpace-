# 3628 Y5 R2FR S_GK explicit scalar-density construction or bound runner

**Status:** 3628 constructs explicit scalar-density candidates for S_GK, identifies the even response-doublet action as the best derivation route because F_1=0 follows by parity, and retains Poynting/Maxwell-like flux as a legitimate action branch; the framework still cannot claim local GR because K_hat=K_metric, Z=physical residual, J_Z=0, positive operator, and boundary no-flux are not parent-signed.

**Claim ceiling:** no local-GR, PPN, Newton, R10/R11, q_loc=0, K_hat=K_metric, or source-coupling-zero claim is allowed from 3628.

## Core result

The useful move is no longer just another missing-input ledger. 3628 writes an explicit variational shape that can make the local first variation vanish for a real mathematical reason:

```text
S_GK = -int sqrt(-g)[Gamma_0 + 1/2 M_AB Z^A Z^B + 1/2 H_AB g^{rho sigma} nabla_rho Z^A nabla_sigma Z^B + O(Z^4)]
T_GK^{mu nu}=Gamma_eff g^{mu nu}-K_metric^{mu nu}
K_metric^{mu nu}=H_AB nabla^mu Z^A nabla^nu Z^B + metric/coefficient response terms
```

At `Z=0`, `nabla Z=0`, with `Gamma_0` background-subtracted, this gives `T_GK=0` and `partial_A T_GK|0=0` by evenness. That is the cleanest route so far to the double-zero/local plateau mechanism. It still does not prove local GR, because the parent map `Z^A = physical q_loc/PPN/Newton/source residual`, the match `K_hat=K_metric`, source-coupling silence `J_Z=0`, positivity, and boundary no-flux remain unsigned.

## Source register

| source_id | path | exists | needle_found | role |
| --- | --- | --- | --- | --- |
| handoff_3627 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3627_NEXT_TARGET.csv | True | True | 3627 selected explicit scalar-density and K_metric comparison as the next real derivation target. |
| metric_response_3627 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3627_GAMMA_KHAT_METRIC_RESPONSE_DERIVATION.csv | True | True | 3627 wrote the conditional metric-response formula to be made explicit here. |
| helmholtz_gate_3627 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3627_SGK_HELMHOLTZ_ACTION_GATE.csv | True | True | 3627 identifies candidate A as the least-scrutiny route. |
| double_zero_3627 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3627_EULER_DOUBLE_ZERO_BOUNDARY_GATE.csv | True | True | fixed-point and first-variation gates inherited from 3627. |
| gk_candidates | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_GK_STRESS_ACTION_CANDIDATES.csv | True | True | older scalar-density, positive auxiliary, topological, and residual branch candidates. |
| metric_contract | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_GK_METRIC_RESPONSE_CONTRACT.csv | True | True | requirements for Gamma_eff scalar density, K_hat metric response, Ward identity, and double zero. |
| metric_match_audit | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_GK_METRIC_RESPONSE_MATCH_AUDIT.csv | True | True | prior audit showing K_hat was not matched to a metric response in the current corpus. |
| response_doublet_contract | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_RESPONSE_DOUBLET_ACTION_CONTRACT.csv | True | True | response-doublet route with even scalar density, metric response, positive operator, and source-coupling gates. |
| stress_rewrite | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_GAMMA_KHAT_QLOC_STRESS_REWRITE.csv | True | True | q_loc/T_GK algebraic rewrite that all scalar-density candidates must own or bound. |
| residual_demotion | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_GAMMA_KHAT_QLOC_RESIDUAL_OR_DEMOTION.csv | True | True | fallback if scalar-density ownership fails. |
| bound_rows_3627 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3627_QLOC_TGK_BOUND_ROWS.csv | True | True | nonclaim q_loc/T_GK bound rows inherited from 3627. |
| ppn_component_rows_3626 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3626_PPN_COMPONENT_FILL_ROWS.csv | True | True | PPN/Newton local residual rows that remain blocked until q_loc/T_GK is owned or bounded. |

## Explicit scalar-density candidates

| candidate_id | ansatz | metric_response_formula | khat_match_requirement | fixed_point_zero_gate | current_status |
| --- | --- | --- | --- | --- | --- |
| GSD3628_0_potential_background | S_GK=-int sqrt(-g)[Gamma_0+V(Phi)] | K_metric^{mu nu}=0 if V has no explicit metric dependence; T_GK^{mu nu}=[Gamma_0+V]g^{mu nu} | K_hat must be zero/pure background in this sector | Gamma_0+V(Phi0) must be background-subtracted and partial_A V(Phi0)=0 | MATHEMATICALLY_VALID_TOO_WEAK_FOR_GENERAL_KHAT |
| GSD3628_1_gradient_elastic | S_GK=-int sqrt(-g)[V(Phi)+1/2 G_AB(Phi) g^{rho sigma} nabla_rho Phi^A nabla_sigma Phi^B] | K_metric^{mu nu}=G_AB nabla^mu Phi^A nabla^nu Phi^B plus metric-dependence terms from G_AB | K_hat must equal the gradient/elastic anisotropic response tensor under the same convention | nabla Phi0=0, V(Phi0) subtracted, partial_A V(Phi0)=0, positive Hessian/gap | PROMISING_TEMPLATE_SYMBOL_MATCH_MISSING |
| GSD3628_2_even_response_doublet | S_GK=-int sqrt(-g)[Gamma_0+1/2 M_AB Z^A Z^B+1/2 H_AB g^{rho sigma} nabla_rho Z^A nabla_sigma Z^B+O(Z^4)] | K_metric^{mu nu}=H_AB nabla^mu Z^A nabla^nu Z^B plus metric/coefficient response terms | K_hat must be identified with this K_metric and Z^A must be the physical q_loc/PPN residual vector, not a bookkeeping shadow | Z=0 and nabla Z=0 gives T_GK=0 after Gamma_0 subtraction; evenness gives partial_A T_GK\|0=0 | BEST_CONDITIONAL_ROUTE_F1_ZERO_BY_EVENNESS_PARENT_MAPPING_MISSING |
| GSD3628_3_exact_topological_or_improvement | S_GK=int dB_GK or int topological_density | bulk K_metric is zero or an improvement tensor; all physical content moves to boundary/symplectic terms | K_hat must be an exact/improvement stress and all linked-surface flux must be zero or fixed-reference | bulk q_loc can vanish, but source mass and alpha3 channels still require no-flux/handoff proof | BOUNDARY_FLUX_RISK_OPEN_NONCLAIM |
| GSD3628_4_wave_flux_Poynting_Maxwell_like | S_flux=-int sqrt(-g)[1/4 W_AB F^A_{rho sigma}F^{B rho sigma}] | K_metric^{mu nu}=W_AB F^{A mu rho}F^B{}^{nu}{}_{rho}; T_flux^{mu nu}=Gamma_flux g^{mu nu}-K_metric^{mu nu} | K_hat may contain this stress only if the MTS EM/wave sector declares F, W, current J, and boundary flux | local gravitational-vacuum silence requires F=0 or a separately conserved physical EM/radiation stress already present in T_matter | USEFUL_EM_STRESS_TEMPLATE_NOT_QLOC_ZERO_PROOF |
| GSD3628_5_composite_minimal_spine | S_GK=S_even_response_doublet+S_exact_boundary+S_physical_flux_if_present | K_metric=K_Z+K_boundary_improvement+K_flux; T_GK=Gamma_total g-K_metric | existing K_hat must decompose into exactly these pieces with no residual knob | Z branch gives F1=0; boundary branch no-flux; flux branch either absent or counted as ordinary physical stress | SELECTED_CONDITIONAL_SPINE_NOT_PARENT_SIGNED |

## K_metric / K_hat comparison

| comparison_id | target_piece | computed_from_candidate | required_existing_match | residual_if_unmatched | status |
| --- | --- | --- | --- | --- | --- |
| KMC3628_0_convention | stress convention | For S_GK=-int sqrt(-g) Gamma_eff, use T_GK^{mu nu}=Gamma_eff g^{mu nu}-K_metric^{mu nu}, K_metric^{mu nu}:=-2 E_g^{mu nu}[Gamma_eff] with derivative/boundary terms included. | all existing Gamma_eff/K_hat appearances must use this one sign and volume convention | R_K^{mu nu}:=K_hat^{mu nu}-K_metric^{mu nu} | CONVENTION_DECLARED_FOR_3628_NOT_GLOBAL_PARENT_LOCKED |
| KMC3628_1_potential | potential/background scalar | K_metric=0, so T_GK=[Gamma_0+V]g after background subtraction | K_hat=0 in this sector and V_A(Phi0)=0 | R_K=K_hat | TOO_WEAK_FOR_CURRENT_KHAT_MATCH |
| KMC3628_2_gradient_elastic | gradient/elastic anisotropic stress | K_metric^{mu nu}=G_AB nabla^mu Phi^A nabla^nu Phi^B plus coefficient metric-response terms | K_hat must decompose as G_AB nabla Phi nabla Phi plus declared coefficient terms | R_K=K_hat-G_AB nabla Phi nabla Phi-coefficient_response | MATCH_MISSING_RESIDUAL_RETAINED |
| KMC3628_3_even_response_doublet | response doublet metric stress | K_metric^{mu nu}=H_AB nabla^mu Z^A nabla^nu Z^B plus metric/coefficient terms; mass potential contributes to Gamma g, not anisotropic K | Z^A must be the actual local residual/PPN vector and K_hat must equal this metric response | R_K=K_hat-K_Z and R_Z=physical_residual_vector-Z | BEST_ROUTE_BUT_PARENT_MAP_UNSIGNED |
| KMC3628_4_wave_flux | Poynting/Maxwell-like stress | K_metric^{mu nu}=W_AB F^{A mu rho}F^B{}^{nu}{}_{rho}; Ward residual becomes a current/flux exchange term, not a free zero | F, W, J, and boundary flux must be explicit; physical EM/radiation stress must not be double-counted or hidden | R_flux=unowned Poynting/current stress contribution | VALID_ACTION_SHAPE_RETAINED_FOR_EM_BRANCH_NOT_LOCAL_GR_CLAIM |
| KMC3628_5_verdict | K_hat=K_metric claim | candidate K_metric formulas exist for potential, gradient, even doublet, exact boundary, and flux branches | existing MTS K_hat must be one of these formulas or a declared sum with no remainder | R_K^{mu nu} remains a scored local residual | KMETRIC_CONSTRUCTED_KHAT_MATCH_NOT_CLAIMED |

## Fixed-point and coupling gates

| gate_id | condition | exact_requirement | derivation_status | effect_if_true |
| --- | --- | --- | --- | --- |
| FPG3628_0_fixed_point_definition | local compact vacuum fixed point | Z^A=0, nabla Z^A=0, Phi^A=Phi0 stationary, unforced physical flux absent or counted as T_matter, boundary reference fixed | CONSTRUCTED_AS_CANDIDATE_NOT_PARENT_SELECTED | T_GK zeroth-order local residual can be zero/background only |
| FPG3628_1_background_subtraction | Gamma_0 and V(Phi0) subtraction | Gamma_eff(Phi0) is absorbed into Lambda_eff or reference Hamiltonian before local PPN/source readout | STANDARD_ROUTE_WRITTEN_NOT_PARENT_LOCKED | constant scalar value does not act as a local force |
| FPG3628_2_F1_zero | first variation zero | partial_A T_GK^{mu nu}\|0=0; in the even Z action this follows from Z-parity and Gamma_0 subtraction | F1_ZERO_DERIVED_FOR_EVEN_RESPONSE_TEMPLATE_ONLY | linear fifth-force/PPN/source-normalization leakage is removed for that template |
| FPG3628_3_positive_operator | local no-hair/mass gap | M_AB positive and H_AB elliptic/self-adjoint after constraints/gauge removal | FORMAL_REQUIREMENT_WRITTEN_NUMERIC_OR_PARENT_PROOF_MISSING | source-free compact exterior gives Z=0 or exponentially bounded hair |
| FPG3628_4_source_coupling_zero | coupling/source silence | J_Z=0 for compact local vacuum, or the coupling coefficient is source-backed and below local bounds | HARD_BLOCK_REMAINS_COUPLING_NOT_DERIVED | Euler equations do not re-source Z around ordinary matter |
| FPG3628_5_boundary_no_flux | boundary/symplectic no flux | boundary terms from variation of S_GK have zero/fixed linked-surface force and Hamiltonian mass handoff is retained | OPEN_BOUNDARY_HANDOFF_REQUIRED | bulk q_loc silence does not leak through alpha3/source-normalization channels |
| FPG3628_6_verdict | local-GR reduction from S_GK | all fixed point, K_hat=K_metric, Z=physical residual, J_Z=0, positive operator, and boundary gates pass | DOUBLE_ZERO_MECHANISM_FOUND_PARENT_OWNERSHIP_MISSING_NO_CLAIM | would turn q_loc/T_GK from closure into a derived local-GR silence mechanism |

## q_loc / T_GK bound runner rows

| row_id | quantity | new_reduction | missing_input | fallback_bound | status |
| --- | --- | --- | --- | --- | --- |
| QBR3628_0_RK_residual | R_K^{mu nu}=K_hat^{mu nu}-K_metric^{mu nu} | explicit K_metric formulas are now available for candidate action classes | MISSING_KHAT_TENSOR_DECOMPOSITION_AND_SYMBOL_MATCH | score \|\|R_K\|\| through PPN/Newton/source-normalization envelope if not zero | BLOCKED_NONCLAIM |
| QBR3628_1_RZ_map | R_Z^A=physical local residual vector - Z^A | even response doublet gives automatic F1=0 only for variables that are the actual residual coordinates | MISSING_Z_TO_QLOC_PPN_NEWTON_SOURCE_MAP | retain q_loc, alpha3, gamma, beta, xi, Gdot and source-mass residual rows | BLOCKED_NONCLAIM |
| QBR3628_2_JZ_coupling | J_Z source/coupling coefficient | the coupling is now isolated as the next hard variable: local source can regenerate Z even when the action is even | MISSING_PARENT_COUPLING_ZERO_OR_NUMERIC_COEFFICIENT | derive J_Z=0 from quotient/current symmetry or fill numeric coefficient against local bounds | NEXT_HARD_TARGET_BLOCKED_NONCLAIM |
| QBR3628_3_flux_branch | Poynting/wave flux stress | Maxwell-like scalar density gives a legitimate stress-action shape rather than vibes | MISSING_F_W_J_BOUNDARY_OWNER_IN_CURRENT_MTS_LOCAL_GR_BRANCH | route to EM/charge branch or count as ordinary physical stress, not local-GR residual silence | EM_BRANCH_RETAINED_NONCLAIM |
| QBR3628_4_boundary | boundary/symplectic flux | exact/topological route remains viable only with no-flux or Hamiltonian handoff rows | MISSING_BOUNDARY_NO_FLUX_OR_MHREF_HANDOFF | fill boundary alpha3/source-normalization coefficient products if no theorem-zero | BOUNDARY_BLOCKED_NONCLAIM |

## Decisions

| decision_id | decision | status | next_action |
| --- | --- | --- | --- |
| DEC3628_0_real_progress | A real scalar-density mechanism now exists on paper: an even response-doublet action makes F_1=0 by symmetry, not by assertion. | DERIVATION_PROGRESS_CONDITIONAL | map Z^A to the actual q_loc/PPN/Newton/source residual vector and prove or bound its coupling J_Z |
| DEC3628_1_current_ceiling | Do not claim local GR or q_loc silence: K_hat=K_metric, Z=physical residual, J_Z=0, positive operator, and boundary no-flux are still unsigned. | NO_CLAIM | carry residual rows R_K, R_Z, J_Z, boundary flux and score them if derivation fails |
| DEC3628_2_poynting_vector | The Poynting/wave intuition is not discarded; it is put into an explicit Maxwell-like action branch where flux is physical stress/current, not a hidden plateau. | EM_FLUX_BRANCH_RETAINED | use it later for EM/charge or radiation stress mapping, not as a local-GR zero proof unless F/J/boundary vanish |
| DEC3628_3_next_target | The next best target is the source coupling: prove J_Z=0 from parent quotient/current symmetry or fill a coefficient row. | NEXT_TARGET_SELECTED | 3629-Y5-R2FR-response-doublet-source-coupling-zero-or-coefficient.md |

## Next target

| target_doc | target_script | objective | success_gate |
| --- | --- | --- | --- |
| 3629-Y5-R2FR-response-doublet-source-coupling-zero-or-coefficient.md | scripts/Y5_R2FR_3629_response_doublet_source_coupling_zero_or_coefficient.py | attempt to parent-own the response doublet by mapping Z^A to the actual local residual vector and proving J_Z=0; if not, create source-ready coupling coefficient rows for PPN/Newton/R10/clock/orbital bounds | Z^A equals q_loc/PPN/Newton/source residual coordinates, K_hat=K_metric has no remainder or retained R_K row, J_Z is theorem-zero or numeric/source-backed, and boundary flux remains explicit |
