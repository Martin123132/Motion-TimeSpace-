# 4115 - S_GK explicit scalar-density construction or bound runner

## Verdict
4115 imports the `3628` scalar-density construction into the active `411x` spine. This is a genuine derivation advance: the even response-doublet action supplies a mathematical reason for `F_1=0` by parity, not by plateau assertion.

No local-GR, PPN, Newton, R10/R11, `q_loc=0`, `K_hat=K_metric`, or source-coupling-zero claim follows yet.

## Strongest Current Result
- `EVEN_RESPONSE_SCALAR_DENSITY_IMPORTED_F1_ZERO_FOUND_JZ_COUPLING_NEXT`
- 4115 imports the explicit scalar-density construction into the active spine. The even response-doublet action gives a real F_1=0 mechanism by parity, and K_metric formulas are now available for potential, gradient, response-doublet, boundary and flux branches.
- The local plateau/double-zero route is no longer a plateau axiom: it has a candidate action mechanism. The remaining bottleneck is whether Z is the actual physical residual and whether J_Z/source coupling vanishes or is bounded.

## Scalar-Density Candidates
| candidate_id | ansatz | metric_response_formula | current_status | interpretation |
| --- | --- | --- | --- | --- |
| GSD4115_0_potential_background | S_GK=-int sqrt(-g)[Gamma_0+V(Phi)] | K_metric^{mu nu}=0 if V has no explicit metric dependence | MATHEMATICALLY_VALID_TOO_WEAK_FOR_GENERAL_KHAT | use only for pure background/potential branch |
| GSD4115_1_gradient_elastic | S_GK=-int sqrt(-g)[V(Phi)+1/2 G_AB g^{rho sigma} nabla_rho Phi^A nabla_sigma Phi^B] | K_metric^{mu nu}=G_AB nabla^mu Phi^A nabla^nu Phi^B plus coefficient metric-response terms | PROMISING_TEMPLATE_SYMBOL_MATCH_MISSING | requires K_hat decomposition into gradient/elastic anisotropic stress |
| GSD4115_2_even_response_doublet | S_GK=-int sqrt(-g)[Gamma_0+1/2 M_AB Z^A Z^B+1/2 H_AB g^{rho sigma}nabla_rho Z^A nabla_sigma Z^B+O(Z^4)] | K_metric^{mu nu}=H_AB nabla^mu Z^A nabla^nu Z^B plus metric/coefficient response terms | BEST_CONDITIONAL_ROUTE_F1_ZERO_BY_EVENNESS_PARENT_MAPPING_MISSING | Z=0 and nabla Z=0 gives T_GK=0 after background subtraction; parity gives partial_A T_GK|0=0 |
| GSD4115_3_exact_boundary | S_GK=int dB_GK or topological density | bulk K_metric is zero or improvement tensor | BOUNDARY_FLUX_RISK_OPEN_NONCLAIM | viable only with no-flux or Hamiltonian handoff rows |
| GSD4115_4_wave_flux | S_flux=-int sqrt(-g)[1/4 W_AB F^A_{rho sigma}F^{B rho sigma}] | K_metric^{mu nu}=W_AB F^{A mu rho}F^B{}^{nu}{}_{rho} | USEFUL_EM_STRESS_TEMPLATE_NOT_QLOC_ZERO_PROOF | Poynting/wave flux is legitimate physical stress branch, not hidden local-GR silence |
| GSD4115_5_composite_spine | S_GK=S_even_response_doublet+S_exact_boundary+S_physical_flux_if_present | K_metric=K_Z+K_boundary_improvement+K_flux | SELECTED_CONDITIONAL_SPINE_NOT_PARENT_SIGNED | best current spine, with each unmatched remainder retained as residual |

## K_metric / K_hat Comparison
| comparison_id | target_piece | computed_from_candidate | residual_if_unmatched | status |
| --- | --- | --- | --- | --- |
| KMC4115_0_convention | stress convention | T_GK^{mu nu}=Gamma_eff g^{mu nu}-K_metric^{mu nu} | R_K^{mu nu}:=K_hat^{mu nu}-K_metric^{mu nu} | CONVENTION_DECLARED_NOT_GLOBAL_PARENT_LOCKED |
| KMC4115_1_potential | potential/background scalar | K_metric=0 | R_K=K_hat | TOO_WEAK_FOR_CURRENT_KHAT_MATCH |
| KMC4115_2_gradient_elastic | gradient/elastic anisotropic stress | K_metric=G_AB nabla Phi nabla Phi plus coefficient response | R_K=K_hat-G_AB nabla Phi nabla Phi-coefficient_response | MATCH_MISSING_RESIDUAL_RETAINED |
| KMC4115_3_even_response_doublet | response doublet metric stress | K_metric=H_AB nabla Z nabla Z plus metric/coefficient terms; mass potential contributes to Gamma g | R_K=K_hat-K_Z and R_Z=physical_residual_vector-Z | BEST_ROUTE_BUT_PARENT_MAP_UNSIGNED |
| KMC4115_4_wave_flux | Poynting/Maxwell-like stress | K_metric=W_AB F^A F^B stress response | R_flux=unowned Poynting/current stress contribution | VALID_ACTION_SHAPE_RETAINED_FOR_EM_BRANCH_NOT_LOCAL_GR_CLAIM |
| KMC4115_5_verdict | K_hat=K_metric claim | candidate K_metric formulas exist | R_K^{mu nu} remains a scored local residual if no exact decomposition | KMETRIC_CONSTRUCTED_KHAT_MATCH_NOT_CLAIMED |

## Double-Zero Mechanism
| gate_id | condition | effect_if_true | status |
| --- | --- | --- | --- |
| FPG4115_0_fixed_point | Z^A=0, nabla Z^A=0, Phi^A=Phi0 stationary | T_GK zeroth-order local residual can be zero/background | CONSTRUCTED_AS_CANDIDATE_NOT_PARENT_SELECTED |
| FPG4115_1_background | Gamma_eff(Phi0) absorbed into Lambda_eff or reference Hamiltonian | constant scalar value does not act as local force | STANDARD_ROUTE_WRITTEN_NOT_PARENT_LOCKED |
| FPG4115_2_F1_zero | partial_A T_GK^{mu nu}|0=0 by Z-parity and Gamma_0 subtraction | linear fifth-force/PPN/source-normalization leakage removed for even template | F1_ZERO_DERIVED_FOR_EVEN_RESPONSE_TEMPLATE_ONLY |
| FPG4115_3_positive_operator | M_AB positive and H_AB elliptic/self-adjoint after constraints/gauge removal | source-free compact exterior gives Z=0 or exponentially bounded hair | FORMAL_REQUIREMENT_WRITTEN_NUMERIC_OR_PARENT_PROOF_MISSING |
| FPG4115_4_source_coupling | J_Z=0 or source-backed coupling coefficient below local bounds | Euler equations do not re-source Z around ordinary matter | HARD_BLOCK_REMAINS_COUPLING_NOT_DERIVED |
| FPG4115_5_boundary | boundary terms have zero/fixed linked-surface force and Hamiltonian mass handoff retained | bulk q_loc silence does not leak through alpha3/source-normalization channels | OPEN_BOUNDARY_HANDOFF_REQUIRED |
| FPG4115_6_verdict | all fixed point, K_hat=K_metric, Z map, J_Z=0, positive operator and boundary gates pass | would turn q_loc/T_GK from closure into derived local-GR silence mechanism | DOUBLE_ZERO_MECHANISM_FOUND_PARENT_OWNERSHIP_MISSING_NO_CLAIM |

## Bound Runner Rows
| row_id | quantity | new_reduction | missing_input | fallback_bound |
| --- | --- | --- | --- | --- |
| QBR4115_0_RK | R_K^{mu nu}=K_hat^{mu nu}-K_metric^{mu nu} | explicit K_metric formulas now available | MISSING_KHAT_TENSOR_DECOMPOSITION_AND_SYMBOL_MATCH | score ||R_K|| through PPN/Newton/source-normalization envelope if not zero |
| QBR4115_1_RZ | R_Z^A=physical local residual vector-Z^A | even response doublet gives F1=0 only for actual residual coordinates | MISSING_Z_TO_QLOC_PPN_NEWTON_SOURCE_MAP | retain q_loc, alpha3, gamma, beta, xi, Gdot and source-mass rows |
| QBR4115_2_JZ | J_Z source/coupling coefficient | coupling is now isolated as next hard variable | MISSING_PARENT_COUPLING_ZERO_OR_NUMERIC_COEFFICIENT | derive J_Z=0 from quotient/current symmetry or fill numeric coefficient |
| QBR4115_3_flux | Poynting/wave flux stress | Maxwell-like scalar density gives legitimate stress-action branch | MISSING_F_W_J_BOUNDARY_OWNER | route to EM/charge branch or count as ordinary physical stress |
| QBR4115_4_boundary | boundary/symplectic flux | exact/topological route viable only with no-flux or Hamiltonian handoff | MISSING_BOUNDARY_NO_FLUX_OR_MHREF_HANDOFF | fill boundary alpha3/source-normalization coefficient products if no theorem-zero |

## Decisions
| decision_id | decision | status | next_action |
| --- | --- | --- | --- |
| DEC4115_0_real_progress | A real scalar-density mechanism is now in the active spine: an even response-doublet action makes F_1=0 by symmetry, not assertion. | DERIVATION_PROGRESS_CONDITIONAL | map Z^A to actual q_loc/PPN/Newton/source residual coordinates |
| DEC4115_1_current_ceiling | Do not claim local GR or q_loc silence: K_hat=K_metric, Z=physical residual, J_Z=0, positive operator and boundary no-flux remain unsigned. | NO_CLAIM | retain R_K, R_Z, J_Z and boundary rows |
| DEC4115_2_poynting | Poynting/wave intuition is retained as a Maxwell-like action branch where flux is physical stress/current. | EM_FLUX_BRANCH_RETAINED | use later for EM/charge/radiation stress mapping, not local-GR zero proof unless flux/current vanish |
| DEC4115_3_next | The next best target is source coupling: prove J_Z=0 or produce coefficient rows. | NEXT_TARGET_SELECTED | 4116-Y5-R2FR-response-doublet-source-coupling-zero-or-coefficient.md |

## Next Target
| target_doc | target_script | objective | success_gate |
| --- | --- | --- | --- |
| 4116-Y5-R2FR-response-doublet-source-coupling-zero-or-coefficient.md | scripts/Y5_R2FR_4116_response_doublet_source_coupling_zero_or_coefficient.py | attempt to parent-own the response doublet by mapping Z^A to the actual local residual vector and proving J_Z=0; if not, create source-ready coupling coefficient rows for PPN/Newton/R10/clock/orbital bounds | Z^A equals q_loc/PPN/Newton/source residual coordinates, K_hat=K_metric has no remainder or retained R_K row, J_Z is theorem-zero or numeric/source-backed, and boundary flux remains explicit |
