# 4114 - Gamma/Khat response action Helmholtz or q_loc/T_GK bound

## Verdict
4114 imports the `3627` GK/q_loc action-existence work into the active `411x` spine. The route is mathematically clean but not yet signed: `q_loc` is a Ward residual only if `Gamma_eff` is an owned scalar-density action and `K_hat` is its metric response.

No `S_GK`, `q_loc=0`, `T_GK=0`, PPN, Newton, R10/R11, source-normalization, or local-GR claim follows.

## Strongest Current Result
- `GK_QLOC_STRESS_IDENTITY_AND_CONDITIONAL_SGK_ROUTE_IMPORTED_SCALAR_DENSITY_NEXT`
- 4114 imports the exact GK/q_loc stress identity and the conditional variational S_GK route into the active spine. q_loc can be a Ward residual if Gamma_eff is an owned scalar-density action and K_hat is its metric response, but the action/Helmholtz/double-zero/boundary gates are not signed.
- The hard orphan is no longer vague: either construct Gamma_eff as an explicit covariant scalar density and compute K_metric, or demote q_loc/T_GK to component-bound rows.

## GK / q_loc Stress Identity
| identity_id | object | formula | meaning | status |
| --- | --- | --- | --- | --- |
| ID4114_0_TGK | T_GK^{mn} | T_GK^{mn}:=Gamma_eff g^{mn}-K_hat^{mn} | algebraic stress rewrite available | PASS_IDENTITY_NOT_ACTION_PROOF |
| ID4114_1_qloc | q_loc^n | q_loc^n:=P_loc nabla_m T_GK^{mn} | q_loc is the projected divergence of the retained GK stress | PASS_IDENTITY_NOT_ZERO_PROOF |
| ID4114_2_ward | Ward residual route | if T_GK=-(2/sqrt(-g))delta S_GK/delta g then nabla_m T_GK^{mn}=sum_A E_A nabla^n Phi^A + boundary | local q_loc silence is derived only if Euler and boundary terms vanish | EXACT_CONDITIONAL_NOT_SIGNED |
| ID4114_3_claim_guard | closure guard | q_loc=0 cannot be asserted from the stress rewrite alone | requires S_GK action, Helmholtz, double-zero and no-flux gates | NO_SMUGGLING_GUARD |

## Helmholtz / Action Gate
| gate_id | test | requirement | current_status |
| --- | --- | --- | --- |
| HAG4114_0_action_existence | local scalar action exists | there exists S_GK[g,Phi] with T_GK^{mn}=-(2/sqrt(-g))delta S_GK/delta g_mn | NOT_SUPPLIED_CURRENT_CORPUS |
| HAG4114_1_Helmholtz | variational Helmholtz symmetry | delta(sqrt(-g)T_GK^{mn})/delta g_ab is symmetric as second variation up to boundary terms | NOT_CHECKED_CURRENT_MTS |
| HAG4114_2_metric_response | Gamma scalar-density response | Gamma_eff is covariant scalar density and K_hat equals its metric response under one fixed convention | BEST_CANDIDATE_NOT_MATCHED_TO_EXISTING_MTS |
| HAG4114_3_positive_auxiliary | positive auxiliary/no-hair action | positive source-free operator matches Gamma/Khat pieces and suppresses local hair | CONDITIONAL_CANDIDATE_NEEDS_SYMBOL_MATCH |
| HAG4114_4_topological | exact/topological sector | S_GK=int dB_GK or topological density gives zero bulk stress and fixed/no-flux boundary charge | BOUNDARY_FLUX_RISK_OPEN |
| HAG4114_5_verdict | current S_GK proof status | action-existence, Helmholtz, metric-response, Euler, double-zero, projector and boundary gates all pass | SGK_NOT_CLAIMED_BOUND_BRANCH_REQUIRED |

## Metric-Response Route
| response_id | formula | condition_or_use | current_status |
| --- | --- | --- | --- |
| MR4114_0_candidate_action | S_GK=-int d^4x sqrt(-g) Gamma_eff(g,Phi,nabla Phi,D,...) | Gamma_eff must be covariant, local, unit-declared and fixed before readout | FORMULA_WRITTEN_NOT_PARENT_MATCHED |
| MR4114_1_response_tensor | K_metric^{mn}:=-2 delta Gamma_eff/delta g_mn - convention_terms | one fixed sign/volume convention and derivative/boundary terms must be included | MATCH_MISSING_CURRENT_CORPUS |
| MR4114_2_comparison | DeltaK^{mn}:=K_hat^{mn}-K_metric^{mn} | DeltaK must be zero, pure boundary/topological, or retained as coefficient row | NEXT_COMPUTATION_TARGET |
| MR4114_3_obstruction | delta(sqrt(-g)(Gamma g-Khat)^{mn})/delta g_ab != symmetric second variation => no S_GK | if Helmholtz fails, demote q_loc/T_GK to finite bound rows | OBSTRUCTION_NOT_RESOLVED |

## Double-Zero / Boundary Gate
| zero_id | required_condition | effect | current_status |
| --- | --- | --- | --- |
| DZ4114_0_background | Gamma_eff(Phi0) constant and absorbed into Lambda_eff/background subtraction | no local force from fixed-point value | CONDITIONAL_STANDARD_NOT_PARENT_MATCHED |
| DZ4114_1_stress_value | T_GK^{mn}(Phi0)=0 or pure background | no zeroth-order local metric/source residual | NOT_MATCHED_CURRENT_CORPUS |
| DZ4114_2_first_variation | partial_A T_GK^{mn}(Phi0)=0 | linear PPN/fifth-force/source-normalization leakage absent | F1_NOT_PROVED |
| DZ4114_3_positive_operator | extra-field operator has positive Hessian/gap and no source term | compact local exterior gives zero/exponentially bounded hair | POSITIVE_OPERATOR_NOT_DERIVED |
| DZ4114_4_boundary | S_GK boundary/symplectic terms have zero or fixed topological flux | bulk q_loc zero cannot leak through source mass or radial force | BOUNDARY_OPEN |

## q_loc / T_GK Bound Branch
| bound_id | quantity | candidate_value | units | status |
| --- | --- | --- | --- | --- |
| QTB4114_0_compact_proxy | max |P_loc d_rel J_rel| or q_loc leakage proxy | 7.432631961576971e-06 | dimensionless_proxy | RETAINED_ANCHOR_PROXY_NONCLAIM |
| QTB4114_1_alpha3 | q_loc preferred-frame alpha3 channel | MISSING_QLOC_TO_ALPHA3_COEFFICIENT | dimensionless | MAPPING_MISSING_BLOCKED |
| QTB4114_2_PPN_metric_tail | T_GK/q_loc contribution to gamma,beta,xi | MISSING_WEAK_FIELD_METRIC_SOLUTION | dimensionless_vector | PPN_MAPPING_MISSING_BLOCKED |
| QTB4114_3_Newton_source | T_GK/q_loc contribution to delta_Newton_MTS | MISSING_PI00_DELTAE_OR_SOURCE_PROFILE | dimensionless_or_acceleration_profile | SOURCE_MASS_CLOSURE_MISSING |
| QTB4114_4_TGK_stress_norm | ||T_GK|| local exterior stress norm | MISSING_TGK_STRESS_NORM_OR_ZERO_THEOREM | stress_or_metric_response_units | STRESS_NORM_MISSING_BLOCKED |
| QTB4114_5_boundary_flux | S_GK boundary/symplectic flux | MISSING_BOUNDARY_FLUX_OR_NO_FLUX_THEOREM | flux_over_MH_or_declared_boundary_units | BOUNDARY_NO_FLUX_MISSING |

## Decisions
| decision_id | decision | status | next_action |
| --- | --- | --- | --- |
| DEC4114_0_identity | q_loc is exactly the projected divergence of T_GK once T_GK=Gamma_eff g-K_hat is defined. | ALGEBRAIC_PROGRESS_IMPORTED | use this as residual definition whether or not S_GK exists |
| DEC4114_1_action_route | Least-scrutiny derivation route is Gamma_eff as covariant scalar density and K_hat as its metric response. | BEST_ROUTE_SELECTED_NOT_CLOSED | construct explicit Gamma_eff scalar density and compute K_metric |
| DEC4114_2_claim_guard | Current corpus does not prove S_GK action-existence, Helmholtz symmetry, metric-response match, double-zero, or boundary no-flux. | SGK_NOT_CLAIMED | do not claim local q_loc/T_GK silence |
| DEC4114_3_bound_branch | q_loc/T_GK component-bound rows are staged and remain nonclaim. | BOUND_BRANCH_STAGED_NOT_SCORED | fill weak-field projection, stress norm and source-backed bounds if action route fails |
| DEC4114_4_next | Next current-chain target is explicit Gamma_eff scalar-density construction or bound runner. | NEXT_TARGET_SELECTED | 4115-Y5-R2FR-SGK-explicit-scalar-density-construction-or-bound-runner.md |

## Next Target
| target_doc | target_script | objective | success_gate |
| --- | --- | --- | --- |
| 4115-Y5-R2FR-SGK-explicit-scalar-density-construction-or-bound-runner.md | scripts/Y5_R2FR_4115_SGK_explicit_scalar_density_construction_or_bound_runner.py | attempt an explicit Gamma_eff scalar-density construction, compute the corresponding K_metric response, compare it to K_hat, and either sign the metric-response owner or demote q_loc/T_GK to the nonclaim bound runner | Gamma_eff has declared fields, units and covariance; K_metric is computed with boundary terms; K_hat-K_metric is zero or retained as coefficient row; F1/double-zero and boundary gates are evaluated |
