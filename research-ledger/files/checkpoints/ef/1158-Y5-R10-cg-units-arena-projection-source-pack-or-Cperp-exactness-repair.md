# 1158 - Y5/R10 c_g Units/Arena Projection Source Pack or Cperp Exactness Repair

**Current verdict:** the `c_g` problem is now sharper, but not solved. A finite branch needs sourced `A_g`, `Xhat`, `c_g`, `K_X`, `Qbar_XH`, `lambda_X`, and separate arena projections. The zero branch needs a parent-signed `Cperp` exactness repair with boundary primitive silence.

**Main progress:** the coupling is no longer a foggy "something is missing" problem. It is now an explicit source-pack: define the observed common frame, normalize `Xhat`, then fill or zero `c_g`, then map it separately into R10, PPN, clocks, WEP, and orbital systems.

**Key guard:** `c_g=d ln A_g/dXhat` is dimensionless only if `Xhat` is dimensionless. Earlier dimensionless placeholders are not enough.

**Best next attack:** either source a first nonclaim finite `c_g` prior/projection bundle, or try the cleaner derivation route: prove the `Cperp` boundary primitive is zero so the quotient-null route can actually bite.

**No claim:** no R10, PPN, WEP, clock, orbital, local-GR, Newton, GitHub, or public claim follows from 1158.

## Source Register
| source_id | relative_path | exists | needle | needle_found | role |
| --- | --- | --- | --- | --- | --- |
| SRC1158_0_1157_next | source-intake/mts_residuals/P8_Y5_R10_1157_NEXT_TARGET.csv | true | NEXT1157_0_1158 | true | handoff selecting c_g units/projection source pack or Cperp exactness repair. |
| SRC1158_1_1157_cg_first | source-intake/mts_residuals/P8_Y5_R10_1157_CG_BOUND_FIRST_FILL_ROWS.csv | true | CG1157_0_cg_first_fill | true | first explicit c_g source row and required column contract. |
| SRC1158_2_1157_exactness | source-intake/mts_residuals/P8_Y5_R10_1157_QMAP_NULL_GENERATOR_PROOF_AUDIT.csv | true | QMAP1157_2_exactness | true | Cperp exactness and boundary primitive silence burden. |
| SRC1158_3_1156_frame_leak | source-intake/mts_residuals/P8_Y5_R10_1156_FRAME_LEAK_BOUND_FILL_ROWS.csv | true | FLB1156_1_c_g | true | prior frame-leak bound row requiring c_g sourcing. |
| SRC1158_4_626_template | source-intake/mts_residuals/P8_Y5_R10_626_CG_BOUND_INPUT_TEMPLATE.csv | true | CGB626_1_cg_value | true | early c_g, tau_R10, tau_PPN, tau_clock, tau_orbital input template. |
| SRC1158_5_944_pack | source-intake/mts_residuals/P8_Y5_R10_944_FRAME_LEAK_BOUND_PACK.csv | true | FLB944_0_cg_weyl | true | frame leak source pack identifying c_g as a Weyl/common-frame derivative. |
| SRC1158_6_945_rows | source-intake/mts_residuals/P8_Y5_R10_945_FIRST_FRAME_LEAK_BOUND_ROWS.csv | true | BND945_0_cg_value | true | first c_g/tau bound rows showing the same missing-source pattern. |
| SRC1158_7_1033_tau_R10 | source-intake/mts_residuals/P8_Y5_R10_1033_TAU_R10_DERIVATION_AUDIT.csv | true | TAUR1033_6_verdict | true | R10 projection audit: tau_R10 and companion factors not derived. |
| SRC1158_8_1052_clock | source-intake/mts_residuals/P8_Y5_R10_1052_TAU_CLOCK_XHAT_NORMALIZATION_AUDIT.csv | true | TCN1052_4_verdict | true | clock/Xhat normalization audit: standalone clock coupling not claim-ready. |
| SRC1158_9_1068_wep | source-intake/mts_residuals/P8_Y5_R10_1068_TAU_WEP_ACQUISITION_PACK.csv | true | TAP1068_5_Xhat_normalization | true | WEP tau acquisition pack: Xhat normalization and force/readout map missing. |
| SRC1158_10_272_Cperp | 272-quotient-configuration-principle-from-topological-projector.md | true | Cperp exactness for the C-sector | true | older quotient principle file naming Cperp exactness as a missing parent derivation. |
| SRC1158_11_720_kinetic_guard | source-intake/mts_residuals/P8_Y5_R10_720_KINETIC_NULL_THEOREM_AUDIT.csv | true | KNT720_8_no_mode_theorem | true | kinetic/null guard preventing missing kinetic terms from being treated as zero proof. |

## c_g Units / Arena Projection Audit
| audit_id | claim_piece | required_form | current_status | missing_for_claim | risk_if_missing | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| CGUP1158_0_Ag_definition | common observed-frame conformal factor | g_obs = A_g(Xhat)^2 g_ref plus explicitly separated disformal/tail terms | SCHEMA_READY_NOT_PARENT_DEFINED | parent source path defining A_g, observed frame, and whether disformal terms are absent or retained | c_g is only a label, not a measurable coefficient | false |
| CGUP1158_1_Xhat_normalization | Xhat normalization | Xhat must be dimensionless or assigned explicit units and a parent normalization | MISSING_SHARED_NORMALIZATION | shared clock/R10/WEP/PPN/orbital Xhat convention or explicitly separated branch convention | c_g units and cross-arena comparisons drift | false |
| CGUP1158_2_cg_units | units of c_g | c_g = d ln A_g / dXhat; dimensionless only if Xhat is dimensionless | DIMENSIONAL_CONVENTION_UNSIGNED | A_g source plus Xhat normalization source | dimensionless c_g can be accidentally smuggled in | false |
| CGUP1158_3_R10_projection | tau_R10 and R10 alpha projection | alpha_R10(lambda)=K_X(lambda) Qbar_XH(source,lambda) [tau_R10(test,lambda)c_g + tails] | DEFINITION_ONLY_NOT_NUMERIC | K_X, Qbar_XH, tau_R10, c_g, finite-source profile, bound curve, and tail envelope | R10 alpha rows remain placeholders | false |
| CGUP1158_4_PPN_projection | tau_PPN weak-field projection | gauge-fixed weak-field map from common-frame response to gamma/beta/preferred-frame residuals | MISSING_ARENA_PROJECTION | PPN gauge convention, observable residual vector, and source-normalized coefficient map | local-GR reduction can be claimed only by words | false |
| CGUP1158_5_clock_WEP_orbital_projection | tau_clock, tau_WEP, tau_orbital | separate arena projections with shared Xhat normalization or direct product observables | MISSING_ARENA_PROJECTIONS | clock time map, WEP material/force readout, orbital source/orbit kernel | finite c_g cannot be compared across local arenas | false |
| CGUP1158_6_zero_theorem_link | Z_cg zero theorem | q object, v_X in ker(Dq), matter functor descent, boundary primitive silence, and no edge/source tail | ZERO_THEOREM_NOT_SIGNED | Cperp exactness repair and parent matter descent in the same local domain | c_g=0 cannot be used as a local-GR proof | false |
| CGUP1158_7_verdict | current c_g source-pack readiness | A_g, Xhat, c_g, tau_R10, tau_PPN, tau_clock, tau_WEP, tau_orbital all sourced or theorem-zeroed | SOURCE_PACK_READY_CLAIM_BLOCKED | all numeric/theorem-zero parent inputs remain missing | no R10, PPN, WEP, clock, orbital, local-GR, or Newton promotion | false |

## c_g Source Pack Rows
| row_id | item | symbol | arena | definition | required_source | unit_convention | current_value | source_path | status | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CGSRC1158_0_Ag_definition | A_g_definition | A_g(Xhat) | all_local_arenas | observed-frame common Weyl/conformal matter coupling, separated from disformal and boundary tails | parent action/frame clause defining g_obs and matter coupling | dimensionless A_g | MISSING_PARENT_Ag_DEFINITION | MISSING_PARENT_SOURCE | BLOCKED | false | false |
| CGSRC1158_1_Xhat_normalization | Xhat_normalization | Xhat | R10;PPN;clock;WEP;orbital | normalized local generator coordinate used by c_g and all arena tau projections | shared parent normalization or explicit branch-separated normalization | dimensionless_or_declared_units | MISSING_SHARED_XHAT_NORMALIZATION | MISSING_PARENT_SOURCE | BLOCKED | false | false |
| CGSRC1158_2_cg_value | c_g_value_or_zero_theorem | c_g=d ln A_g/dXhat | R10;PPN;clock;WEP;orbital | finite common-frame coefficient or parent-signed zero theorem | numeric coefficient source row or Z_cg theorem path with q/null/boundary/matter descent proof | 1/[Xhat_units]; dimensionless only if Xhat dimensionless | MISSING_PARENT_NUMERIC_CG_OR_ZERO_THEOREM | MISSING_PARENT_SOURCE | BLOCKED | false | false |
| CGSRC1158_3_tau_R10 | R10 projection | tau_R10(lambda) | R10 | normalized short-range material/test/readout projection multiplying c_g in the Yukawa alpha convention | test material projection, profile integral, finite-source correction, and alpha(lambda) convention | dimensionless_after_declared_normalization | MISSING_R10_ARENA_PROJECTION | source-intake/mts_residuals/P8_Y5_R10_1033_TAU_R10_DERIVATION_AUDIT.csv | BLOCKED_DEFINITION_ONLY | false | false |
| CGSRC1158_4_KX_Qbar_lambda | R10 companion factors | K_X(lambda);Qbar_XH;lambda_X | R10 | Green-kernel normalization, source charge, and range/profile relation required before alpha_R10 can score | parent kinetic normalization, source worldtube, measured-G comparison, and lambda_X relation | declared_by_kernel_and_source_normalization | MISSING_R10_COMPANION_FACTORS | source-intake/mts_residuals/P8_Y5_R10_1033_TAU_R10_DERIVATION_AUDIT.csv | BLOCKED | false | false |
| CGSRC1158_5_tau_PPN | PPN projection | tau_PPN | PPN | weak-field projection of common-frame response into PPN residual vector | gauge-fixed weak-field map and residual-vector formula | dimensionless_after_gauge_convention | MISSING_PPN_ARENA_PROJECTION | MISSING_PPN_SOURCE | BLOCKED | false | false |
| CGSRC1158_6_tau_clock | clock projection | tau_clock | clock | time/readout projection converting local generator motion into clock observable products | local time map, chi_X/Xhat normalization, and clock sensitivity product rule | time^-1 or dimensionless per declared clock convention | MISSING_CLOCK_ARENA_PROJECTION | source-intake/mts_residuals/P8_Y5_R10_1052_TAU_CLOCK_XHAT_NORMALIZATION_AUDIT.csv | BLOCKED_PRODUCT_ONLY | false | false |
| CGSRC1158_7_tau_WEP | WEP/material projection | tau_WEP | WEP | material/source/readout projection converting common-frame coupling into differential acceleration observable | source worldtube, orbit average, material response, force map, and shared Xhat normalization | dimensionless_or_direct_product | MISSING_WEP_ARENA_PROJECTION | source-intake/mts_residuals/P8_Y5_R10_1068_TAU_WEP_ACQUISITION_PACK.csv | BLOCKED_ACQUISITION_PACK_ONLY | false | false |
| CGSRC1158_8_tau_orbital | orbital projection | tau_orbital | orbital | source/orbit/readout projection of common-frame response into perihelion, range, or timing residuals | orbital source body, orbit averaging kernel, calibration convention, and PPN/source-normalization link | dimensionless_or_declared_by_residual_vector | MISSING_ORBITAL_ARENA_PROJECTION | MISSING_ORBITAL_SOURCE | BLOCKED | false | false |
| CGSRC1158_9_epsilon_cg_score | score envelope | epsilon_cg | all_local_arenas | absolute projected residual envelope from c_g and arena tau factors | all component coefficients, units, source paths, no-cancellation rule, and observed-frame residual map | dimensionless_residual_or_declared_observable_units | MISSING_COMPONENT_INPUTS | MISSING_COMPONENT_SOURCE_PACK | BLOCKED | false | false |

## Cperp Exactness Repair Audit
| repair_id | target | required_statement | current_status | missing_for_proof | effect_if_closed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| CPE1158_0_exactness_target | Cperp exactness | C_perp is relative-exact or variationally trivial in the local domain | OPEN_TARGET | parent C-sector form, differential, allowed boundary class, and local domain | candidate presymplectic null direction becomes credible | false |
| CPE1158_1_boundary_primitive | boundary primitive zero | the exact primitive has zero compact/local boundary readout and no hidden edge charge | NOT_PROVED | boundary condition, edge-mode exclusion, and source support silence | prevents exactness from reappearing as boundary hair | false |
| CPE1158_2_presymplectic_kernel | Omega(v_X,delta)=0 | the Xhat/frame direction lies in the presymplectic kernel after exact/boundary pieces are removed | CONDITIONAL_ONLY | Theta/Omega calculation with the actual parent local branch | supports v_X in ker(Dq) | false |
| CPE1158_3_vX_identification | local generator identification | the c_g-carrying direction is exactly the quotient null generator, not a retained physical field | NOT_IDENTIFIED | map from Xhat/frame variation to parent null orbit | c_g can move from finite bound row toward zero theorem | false |
| CPE1158_4_matter_descent | matter action descends through q | S_matter factors through the quotient and cannot depend on representative A_g(Xhat) | NOT_SIGNED | same-domain matter functor, observed coframe, constants, and source measure descent | blocks common-frame matter coupling | false |
| CPE1158_5_kinetic_rank_guard | no physical retained X mode | rank/signature/source-orthogonality classify X as null or constrained, not merely omitted | OPEN_GUARD | kinetic/Hessian/range/source-rank audit in the same branch | prevents hidden scalar-force leakage | false |
| CPE1158_6_verdict | Cperp exactness repair closes Z_cg | CPE1158_0 through CPE1158_5 all parent-signed | NOT_CLOSED_CURRENT_CORPUS | exactness, boundary primitive zero, vX identification, matter descent, and kinetic-rank guard | only then can c_g=0 be considered for local-GR branch promotion | false |

## No-Cheat Guards
| guard_id | guard | status | reason | valid_for_claim |
| --- | --- | --- | --- | --- |
| GUARD1158_0_no_dimensionless_cg_shortcut | c_g is dimensionless only after Xhat is dimensionless or explicitly normalized | ACTIVE | units cannot be inherited from earlier placeholder rows | false |
| GUARD1158_1_no_placeholder_source_pack_claim | a row with MISSING_* or NOT_DERIVED status cannot be used in a score | ACTIVE | source pack rows are acquisition targets, not evidence | false |
| GUARD1158_2_no_tau_reuse_across_arenas | tau_R10, tau_PPN, tau_clock, tau_WEP, and tau_orbital are separate projections unless parent-linked | ACTIVE | same symbol cannot silently do five different experiments | false |
| GUARD1158_3_no_Cperp_slogan_proof | Cperp exactness must include boundary primitive zero and matter descent | ACTIVE | exact bulk terms can still carry boundary/source hair | false |
| GUARD1158_4_no_local_GR_promotion | local-GR/Newton/R10/PPN/WEP/clock/orbital claims remain blocked | ACTIVE | neither finite c_g source pack nor Z_cg proof is complete | false |

## Claim Gates
| gate_id | rule | gate_pass | reason | valid_for_claim |
| --- | --- | --- | --- | --- |
| G1158_0_sources_exist | all cited local source paths and needles exist | true_nonclaim | source register validates the audit trail | false |
| G1158_1_cg_pack_complete | source pack covers A_g, Xhat, c_g, R10, PPN, clock, WEP, orbital, and score envelope | true_nonclaim | all required rows are emitted as blocked acquisition rows | false |
| G1158_2_finite_cg_score_ready | finite c_g branch has numeric/theorem-zero value and arena projections | false | A_g, Xhat, c_g, tau projections, and companion factors remain missing | false |
| G1158_3_Cperp_zero_ready | Cperp exactness repair proves Z_cg | false | boundary primitive zero, vX identification, matter descent, and kinetic guard are not parent-signed | false |
| G1158_4_claim_promotion | R10/PPN/WEP/clock/orbital/local-GR claim allowed | false | both finite-bound and theorem-zero c_g routes remain incomplete | false |

## Decision Ledger
| decision_id | decision | reason | next_action | valid_for_claim |
| --- | --- | --- | --- | --- |
| D1158_0_units | separate c_g units from c_g value | d ln A_g/dXhat is dimensionless only under a dimensionless Xhat normalization | require A_g and Xhat source rows before any c_g scoring | false |
| D1158_1_projection_pack | treat every local arena as its own projection | R10, PPN, clocks, WEP, and orbital tests measure different readout maps | fill tau_R10/tau_PPN/tau_clock/tau_WEP/tau_orbital separately or derive a parent link | false |
| D1158_2_derivation_route | keep Cperp exactness as the clean zero route | a true presymplectic-null quotient would be cleaner than fitting finite c_g bounds | attack boundary primitive zero and vX identification, not q by declaration | false |
| D1158_3_best_next | target first numeric prior or boundary primitive zero proof | 1158 has converted the coupling problem into exact missing rows and one derivation repair burden | 1159 c_g first numeric prior or Cperp boundary primitive zero proof | false |

## Validation
| check_id | result | detail | valid_for_claim |
| --- | --- | --- | --- |
| V1158_0_sources_exist | pass | all cited local source paths exist and needles are found | false |
| V1158_1_units_unsigned | pass | c_g units remain gated by Xhat normalization instead of assumed dimensionless | false |
| V1158_2_pack_rows_complete | pass | c_g source pack covers A_g, Xhat, c_g, all projections, companion factors, and score envelope | false |
| V1158_3_pack_rows_nonclaim_missing | pass | all c_g source-pack rows remain missing/nonclaim until sourced | false |
| V1158_4_Cperp_not_closed | pass | Cperp exactness repair remains open rather than claimed | false |
| V1158_5_guards_active | pass | all c_g source-pack and Cperp no-cheat guards are active | false |
| V1158_6_claim_gates_blocked | pass | finite c_g, Z_cg, and local claim gates remain blocked | false |
| V1158_7_no_claim_rows | pass | all generated rows remain nonclaim | false |
| V1158_8_next_target | pass | 1159 handoff targets first numeric prior or Cperp boundary primitive zero proof | false |
| V1158_9_generated_under_post_checkpoint | pass | all generated outputs are under post-checkpoint-work | false |
| V1158_10_csv_parse | pass | all 1158 CSV outputs parse cleanly | false |
| V1158_11_formalization_untouched | pass | generator writes no outputs under formalization-workbench | false |
| V1158_SUMMARY | pass | 1158 makes c_g source requirements exact, blocks finite/local claims, and preserves Cperp exactness as the clean zero route | false |

## Next Target
| next_id | next_target | objective | include | exclude | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- | --- | --- |
| NEXT1158_0_1159 | 1159-Y5-R10-cg-first-numeric-prior-or-Cperp-boundary-primitive-zero-proof.md | either source a first nonclaim finite c_g prior/projection bundle or prove the Cperp boundary primitive is zero in the local branch | A_g source; Xhat normalization; finite c_g prior; tau_R10/tau_PPN/tau_clock/tau_WEP/tau_orbital; boundary primitive B_C=0 proof attempt | dimensionless c_g shortcut; tau reuse; q by declaration; local-GR/Newton claim; GitHub; formalization edits | false | false |
