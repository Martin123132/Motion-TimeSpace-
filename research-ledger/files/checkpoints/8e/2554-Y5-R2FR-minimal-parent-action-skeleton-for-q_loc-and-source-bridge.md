# 2554 Y5 R2FR Minimal Parent Action Skeleton For q_loc And Source Bridge

**Result:** constructive route opened, not claimed. The best candidate is a vertical-generator current-law action where `A_nu` is the varied object and `K_hat^{mu nu}:=partial L_K/partial(nabla_mu A_nu)`. This gives the desired `q_loc` equation as an Euler equation rather than a plateau axiom, but it is new parent material and the source bridge is still unsigned.

**Core sketch:** take

`S_GK = int sqrt(-g)[L_K(g,tau,nabla A)+A_nu nabla^nu Gamma_eff-A_nu J_M^nu+L_Gamma(Gamma_eff,g,tau)]`

with `K_hat^{mu nu}:=partial L_K/partial(nabla_mu A_nu)`. Varying `A_nu` gives

`nabla^nu Gamma_eff - nabla_mu K_hat^{mu nu} - J_M^nu = 0`,

so `q_loc^nu=P_loc^nu_rho J_M^rho`. In a source-free local collar with boundary silence this gives the desired local vacuum zero. The sting in the tail: `A_nu`, `L_K`, `L_Gamma`, `J_M`, `P_loc`, and boundary/source descent must be sourced from a parent theory before this counts.

## Source Register
| source_id | source_path | exists | missing_needles | source_pass | role |
| --- | --- | --- | --- | --- | --- |
| SRC2554_00_2553_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\2553-Y5-R2FR-local-GR-route-triage-after-Hamiltonian-denominator-block.md | true |  | true | active handoff selecting constructive parent-action skeleton |
| SRC2554_01_2553_route_triage | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_NO_SHADOW_2553_LOCAL_GR_ROUTE_TRIAGE.csv | true |  | true | machine-readable route selection |
| SRC2554_02_2553_prereqs | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_NO_SHADOW_2553_PREREQUISITE_MATRIX.csv | true |  | true | missing prerequisites to attack |
| SRC2554_03_2552_reopen_material | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_NO_SHADOW_2552_REOPEN_MATERIAL_SPEC.csv | true |  | true | parent-action reopen material requirements |
| SRC2554_04_1010_gk_residual | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1010-Y5-R10-Gamma-Khat-action-existence-Helmholtz-or-q_loc-residual-retention.md | true |  | true | Gamma/Khat/q_loc hard block and exact route-to-proof |
| SRC2554_05_symbol_map | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_MTS_SYMBOL_TO_LOCAL_GR_ACTION_MAP.csv | true |  | true | symbol/action placement map |
| SRC2554_06_variation_gates | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_MTS_SYMBOL_FIRST_VARIATION_GATES.csv | true |  | true | first-variation fail gate to improve |

## Field Inventory
| field_id | symbol | meaning | status | role_in_skeleton | current_evidence | 2554_treatment |
| --- | --- | --- | --- | --- | --- | --- |
| FLD2554_0_metric | g_mu_nu | spacetime metric | fundamental_or_background_parent | needed for covariance, covariant derivatives, stress variation | EH anchor exists but not full parent | included_in_skeleton |
| FLD2554_1_clock | tau_mu / coframe | local clock/coframe sector | candidate_parent_field | needed for local frame, P_loc and same-frame source readout | not fully parent-owned | included_as_conditional |
| FLD2554_2_vertical_generator | A_nu | vertical/local generator | new_auxiliary_candidate | variation with respect to A_nu can own q_loc equation | not currently sourced in corpus | new_material_required |
| FLD2554_3_connection_scalar | Gamma_eff | effective scalar connection/compression | candidate_parent_field | appears through grad^nu Gamma_eff in q_loc | hard block in q_loc map | included_as_conditional |
| FLD2554_4_displacement_tensor | K_hat^{mu nu} | response/displacement tensor | derived_or_auxiliary | defined as partial L_K / partial(nabla_mu A_nu) | not currently variationally derived | included_as_derived_definition |
| FLD2554_5_source_current | J_M^nu | matter/source worldtube current | must_be_parent_derived | right side of q_loc equation and Newton source bridge | Pi_M/worldtube source bridge missing | included_but_unsigned |
| FLD2554_6_projector | P_loc^nu_rho | local projector/selector | candidate_parent_or_frame_structure | physical residual is P_loc applied to Euler current | selector stress and boundary closure missing | included_as_conditional |
| FLD2554_7_reference | beta_ref/H_ref | reference/counterterm data | late_boundary_data_only | must not set source normalization | 2552 forbids denominator reuse | not_used_in_skeleton |

## Candidate Actions
| candidate_id | candidate_name | action_skeleton | key_definition | variation_target | risk | verdict | promote_now |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ACT2554_A_vertical_generator_current_law | vertical generator current-law action | S_GK=int sqrt(-g)[L_K(g,tau,nabla A)+A_nu nabla^nu Gamma_eff-A_nu J_M^nu+L_Gamma(Gamma_eff,g,tau)] | K_hat^{mu nu}:=partial L_K/partial(nabla_mu A_nu) | delta_A S gives nabla^nu Gamma_eff-nabla_mu K_hat^{mu nu}-J_M^nu=0 | A_nu, L_K, L_Gamma, J_M and P_loc are new parent material; coupling may be tautological unless symmetry/source descent is supplied | BEST_CONSTRUCTIVE_CANDIDATE_BUT_NONCLAIM | false |
| ACT2554_B_multiplier_constraint | direct multiplier constraint | S_constraint=int sqrt(-g) lambda_nu P_loc(nabla^nu Gamma_eff-nabla_mu K_hat^{mu nu}-J_M^nu) | lambda_nu enforces q_loc=P_loc J_M | delta_lambda S gives q_loc=P_loc J_M directly | high closure-risk unless lambda arises from gauge/symmetry reduction | DEMOTE_UNLESS_SYMMETRY_DERIVED | false |
| ACT2554_C_quadratic_penalty | quadratic residual penalty | S_penalty=int sqrt(-g)[-1/2 Z_q q_loc_nu q_loc^nu + source terms] | q_loc treated as costly residual rather than exact constraint | variation produces differential equations for q_loc but not automatic q_loc=0 | gives finite bounds rather than exact GR reduction; may introduce local fifth-force tails | BOUND_FALLBACK_NOT_GR_PROOF | false |
| ACT2554_D_reference_cancellation | reference/counterterm cancellation | choose H_ref/B_ref so local q_loc readout cancels | reference data absorbs local residual | none before readout | smuggles local GR through boundary bookkeeping | REJECTED | false |

## Variation Ownership
| variation_id | varied_object | formal_euler_output | ownership_status | closure_status | remaining_issue |
| --- | --- | --- | --- | --- | --- |
| VAR2554_0_delta_A | A_nu | nabla^nu Gamma_eff - nabla_mu K_hat^{mu nu} - J_M^nu = 0 | owned by ACT2554_A if K_hat=partial L_K/partial(nabla A) | FORMALLY_CLOSES_QLOC_EULER_EQUATION | still needs source descent and dimensions |
| VAR2554_1_delta_Gamma | Gamma_eff | -nabla_nu A^nu + partial L_Gamma/partial Gamma_eff = 0 plus boundary | owned by ACT2554_A | CLOSES_COMPANION_EQUATION_CONDITIONAL | must not force unphysical gauge or nonlocal clock behaviour |
| VAR2554_2_delta_matter | Psi | matter Euler equations plus source current J_M^nu | not owned until L_m and source map are specified | MISSING_SOURCE_BRIDGE | Newton limit blocked until J_M is physical source current |
| VAR2554_3_delta_metric | g_mu_nu | Einstein/EH stress plus GK stress plus matter stress | not owned by minimal GK skeleton alone | MISSING_FULL_PARENT_STRESS | local GR pass requires stress either zero, bounded, or absorbed consistently |
| VAR2554_4_delta_projector | P_loc | selector stress/boundary terms | not owned | MISSING_SELECTOR_VARIATION | physical projection may leak residual if not parent-defined |
| VAR2554_5_boundary | boundary data | n_mu K_hat^{mu nu} delta A_nu and Gamma/A surface terms | not fixed by skeleton | MISSING_BOUNDARY_SILENCE | local vacuum law needs boundary flux condition |

## q_loc Derivation Attempt
| derivation_id | step | assumption | result | status |
| --- | --- | --- | --- | --- |
| QDER2554_0_define_displacement | Define K_hat^{mu nu}:=partial L_K/partial(nabla_mu A_nu). | definition from candidate L_K | turns divergence of K_hat into the Euler divergence term | PASS_AS_CANDIDATE_DEFINITION |
| QDER2554_1_vary_A | delta_A S_GK=int sqrt(-g)[-nabla_mu K_hat^{mu nu}+nabla^nu Gamma_eff-J_M^nu]delta A_nu + boundary. | integration by parts with fixed delta A or boundary term cancelled | gives the exact unprojected q equation | PASS_AS_FORMAL_VARIATION |
| QDER2554_2_project_local | Apply P_loc: q_loc^nu=P_loc^nu_rho(nabla^rho Gamma_eff-nabla_mu K_hat^{mu rho})=P_loc^nu_rho J_M^rho. | P_loc is fixed or parent-owned and commutes only as specified | physical q_loc is source current projection | CONDITIONAL_ON_PROJECTOR |
| QDER2554_3_vacuum_zero | If J_M^nu=0 and boundary flux is silent in the local vacuum collar, then q_loc^nu=0. | source-free local exterior and boundary silence | F1=0 follows because the residual itself is zero to all local perturbative orders allowed by the Euler equation | CONDITIONAL_ZERO_NOT_CURRENT_CLAIM |
| QDER2554_4_not_promoted | The derivation is not promoted for current MTS. | A_nu/L_K/L_Gamma/J_M/P_loc are not sourced from the corpus as a parent action | 2554 is a constructive contract, not evidence of local-GR pass | NONCLAIM |

## Source Bridge Contract
| bridge_id | required_clause | why_needed | current_status |
| --- | --- | --- | --- |
| SRCBR2554_0_current_origin | J_M^nu must be Noether/Hilbert matter current from L_matter, not a fitted mass current. | prevents orbital-GM smuggling | MISSING |
| SRCBR2554_1_worldtube_integral | M_source[W] or charge_source[W] must equal integral of J_M over a parent-defined worldtube/linking surface. | needed for Newton source | MISSING |
| SRCBR2554_2_conservation | nabla_nu J_M^nu=0 or controlled exchange with GK sector must follow from matter equations/diffeomorphism invariance. | needed for stable local source readout | MISSING |
| SRCBR2554_3_external_vacuum | Outside the worldtube, J_M^nu=0 except distributional boundary layer terms explicitly bounded. | needed for q_loc zero exterior | MISSING |
| SRCBR2554_4_universality | same J_M coupling must apply across local tests without species-dependent hand tuning. | needed for WEP/PPN safety | MISSING |

## Local Vacuum And Amplitude Law
| law_id | quantity | law | conditions | consequence | claim_status |
| --- | --- | --- | --- | --- | --- |
| LAW2554_0_exact_conditional_zero | q_loc^nu | q_loc^nu=P_loc^nu_rho J_M^rho | ACT2554_A is valid, P_loc is parent-owned/fixed, source-free local collar J_M=0, boundary flux silent | q_loc^nu -> 0 exactly in local vacuum | CONDITIONAL_CONTRACT_ONLY |
| LAW2554_1_F1_zero | F1 | F1=0 because the first local residual coefficient is proportional to the Euler-source residual J_M plus boundary leakage | same as LAW2554_0 plus smooth weak-field expansion | no linear local fifth-force term in the vacuum collar | CONDITIONAL_CONTRACT_ONLY |
| LAW2554_2_Delta_m_bound | Delta m / m | abs(Delta m/m) <= C_P[\|\|P_loc J_M\|\|_collar + \|\|boundary_flux\|\|]/M_source | source bridge supplies M_source and norm convention | mass/readout leakage is bounded by source leakage and boundary flux, not arbitrary plateau | BOUND_FORM_ONLY |
| LAW2554_3_transition_length | ell_tr/L_cg | ell_tr/L_cg = 1/(m_tr L_cg) if L_Gamma or L_K supplies a parent mass/gap m_tr | operator has a real positive gap and cosmological gradient scale L_cg is independently defined | transition scale can be derived from parent coefficients rather than fitted as a local patch | PARAMETRIC_ONLY |
| LAW2554_4_current_limit | local GR/Newton/PPN | not claimed | current corpus lacks ACT2554_A source adoption and source bridge | 2554 improves route clarity but does not pass local GR | NONCLAIM |

## Claim Gates
| gate_id | claim | gate_status | reason | gate_pass | claim_allowed |
| --- | --- | --- | --- | --- | --- |
| GATE2554_0_formal_variation | ACT2554_A formally produces the q_loc Euler equation. | PASS_AS_CANDIDATE | delta_A derivation closes algebraically once K_hat is a displacement tensor | true | false |
| GATE2554_1_parent_source_adoption | Current MTS adopts ACT2554_A as a sourced parent action. | BLOCKED | A_nu, L_K, L_Gamma, J_M and P_loc are new material | false | false |
| GATE2554_2_source_bridge | J_M source bridge is parent-derived. | BLOCKED | Pi_M/worldtube/source current remains missing | false | false |
| GATE2554_3_local_vacuum_zero | q_loc^nu -> 0 in local vacuum is derived for current MTS. | CONDITIONAL_ONLY | follows from candidate action only if source and boundary clauses are supplied | false | false |
| GATE2554_4_local_GR_Newton_PPN | local GR/Newton/PPN branch passes. | BLOCKED | candidate action is not yet full parent action and stress/source/projector terms are not closed | false | false |
| GATE2554_5_no_GitHub | No public/GitHub update from this checkpoint. | PASS_GUARDRAIL | private derivation checkpoint only | true | false |

## Decision Ledger
| decision_id | decision | reason | effect |
| --- | --- | --- | --- |
| DEC2554_0_best_candidate | Keep ACT2554_A as the best constructive candidate. | it derives the q_loc equation as an Euler equation for A_nu rather than imposing a plateau | next work should vary and dimension-check this candidate harder |
| DEC2554_1_not_promoted | Do not promote ACT2554_A to current MTS theorem. | its fields and source current are not sourced parent material yet | local-GR claim remains blocked |
| DEC2554_2_multiplier_demoted | Demote direct multiplier constraint. | it can force q_loc=0 too cheaply and would look like closure by notation | only revisit if multiplier is symmetry-derived |
| DEC2554_3_source_bridge_is_key | Treat J_M/Pi_M/worldtube as equally important as q_loc. | without source bridge, Newton limit can be smuggled through fitted GM | next checkpoint must own current and source integral |
| DEC2554_4_next_target | Move to variation/dimension/source audit of ACT2554_A. | the route is now constructive enough to test rather than merely discuss | 2555 should try to break the candidate |

## Next Target
| route_id | selection_status | target_file | target_script | task | acceptance_target | guardrails |
| --- | --- | --- | --- | --- | --- | --- |
| NEXT2554_0_selected | selected | 2555-Y5-R2FR-vertical-generator-current-law-variation-and-source-audit.md | scripts/Y5_R2FR_vertical_generator_current_law_variation_and_source_audit_2555.py | stress-test ACT2554_A by doing the variation, dimensional bookkeeping, boundary terms, stress tensor exposure, and J_M source-current descent clauses | either promote the candidate to a sharper parent-action contract or demote it as tautological/inconsistent | no local-GR claim; no M_H_ref reuse; no orbital-GM source definition; no plateau axiom; no GitHub |

## Branch Copies
| copy_id | source_path | target_path | source_exists | target_exists |
| --- | --- | --- | --- | --- |
| candidate_action_nonclaim | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_NO_SHADOW_2554_CANDIDATE_ACTIONS.csv | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\rab-sector\acquisition-queue\JR2554_PARENT_ACTION_SKELETON_CANDIDATES_NONCLAIM.csv | true | true |
| qloc_law_nonclaim | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_NO_SHADOW_2554_LOCAL_VACUUM_AMPLITUDE_LAW.csv | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\local_bounds\Qloc_local_vacuum_law_2554_NONCLAIM.csv | true | true |

## Validation
| check_id | status | notes | detail |
| --- | --- | --- | --- |
| VAL2554_00_sources_exist | PASS | all cited source paths exist and needles are present |  |
| VAL2554_01_fields_written | PASS | field inventory covers metric, clock, vertical generator, Gamma, Khat, source, projector and reference |  |
| VAL2554_02_candidate_actions_written | PASS | candidate action options written |  |
| VAL2554_03_best_candidate_nonclaim | PASS | best candidate exists but is nonclaim |  |
| VAL2554_04_variation_attempt_written | PASS | delta_A ownership row written |  |
| VAL2554_05_q_loc_derivation_contract | PASS | formal q_loc variation route written |  |
| VAL2554_06_source_bridge_missing | PASS | source bridge remains explicitly missing |  |
| VAL2554_07_laws_nonclaim | PASS | local vacuum/amplitude laws are nonclaim |  |
| VAL2554_08_claim_gates_safe | PASS | no local-GR claim allowed |  |
| VAL2554_09_next_target_written | PASS | 2555 variation/source audit selected |  |
| VAL2554_10_branch_copies | PASS | nonclaim branch copies exist |  |
| VAL2554_11_no_formalization_artifacts | PASS | no 2554 artifacts were written to formalization-workbench |  |
| VAL2554_12_all_outputs_inside_post_checkpoint | PASS | all 2554 outputs stay inside post-checkpoint-work |  |
| VAL2554_13_pycache_absent | PASS | scripts __pycache__ absent after cleanup |  |
| VAL2554_CSV_P8_Y5_NO_SHADOW_2554_SOURCE_REGISTER | PASS | CSV parses with 7 rows | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_NO_SHADOW_2554_SOURCE_REGISTER.csv |
| VAL2554_CSV_P8_Y5_NO_SHADOW_2554_FIELD_INVENTORY | PASS | CSV parses with 8 rows | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_NO_SHADOW_2554_FIELD_INVENTORY.csv |
| VAL2554_CSV_P8_Y5_NO_SHADOW_2554_CANDIDATE_ACTIONS | PASS | CSV parses with 4 rows | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_NO_SHADOW_2554_CANDIDATE_ACTIONS.csv |
| VAL2554_CSV_P8_Y5_NO_SHADOW_2554_VARIATION_OWNERSHIP | PASS | CSV parses with 6 rows | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_NO_SHADOW_2554_VARIATION_OWNERSHIP.csv |
| VAL2554_CSV_P8_Y5_NO_SHADOW_2554_QLOC_DERIVATION_ATTEMPT | PASS | CSV parses with 5 rows | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_NO_SHADOW_2554_QLOC_DERIVATION_ATTEMPT.csv |
| VAL2554_CSV_P8_Y5_NO_SHADOW_2554_SOURCE_BRIDGE_CONTRACT | PASS | CSV parses with 5 rows | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_NO_SHADOW_2554_SOURCE_BRIDGE_CONTRACT.csv |
| VAL2554_CSV_P8_Y5_NO_SHADOW_2554_LOCAL_VACUUM_AMPLITUDE_LAW | PASS | CSV parses with 5 rows | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_NO_SHADOW_2554_LOCAL_VACUUM_AMPLITUDE_LAW.csv |
| VAL2554_CSV_P8_Y5_NO_SHADOW_2554_CLAIM_GATES | PASS | CSV parses with 6 rows | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_NO_SHADOW_2554_CLAIM_GATES.csv |
| VAL2554_CSV_P8_Y5_NO_SHADOW_2554_DECISION_LEDGER | PASS | CSV parses with 5 rows | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_NO_SHADOW_2554_DECISION_LEDGER.csv |
| VAL2554_CSV_P8_Y5_NO_SHADOW_2554_NEXT_TARGET | PASS | CSV parses with 1 rows | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_NO_SHADOW_2554_NEXT_TARGET.csv |
| VAL2554_CSV_P8_Y5_NO_SHADOW_2554_BRANCH_COPIES | PASS | CSV parses with 2 rows | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_NO_SHADOW_2554_BRANCH_COPIES.csv |
| VAL2554_COPY_CSV_candidate_action_nonclaim | PASS | copy CSV parses with 4 rows | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\rab-sector\acquisition-queue\JR2554_PARENT_ACTION_SKELETON_CANDIDATES_NONCLAIM.csv |
| VAL2554_COPY_CSV_qloc_law_nonclaim | PASS | copy CSV parses with 5 rows | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\local_bounds\Qloc_local_vacuum_law_2554_NONCLAIM.csv |
| VAL2554_OVERALL | PASS | 2554 constructs a promising q_loc parent-action skeleton but keeps source bridge/local-GR claims blocked |  |
