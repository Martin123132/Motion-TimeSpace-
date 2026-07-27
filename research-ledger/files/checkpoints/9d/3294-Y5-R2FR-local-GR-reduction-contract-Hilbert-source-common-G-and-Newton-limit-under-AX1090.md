# 3294 - Local GR reduction contract: Hilbert source, common G, and Newton limit under AX1090

**Run UTC:** 2026-06-27T17:44:22.327382+00:00

3294 turns the recent coupling work into a local-GR spine contract. The point is not to claim GR yet. The point is to state exactly what MTS must derive or bound to reduce to GR/Newton/Maxwell in the local regime:

`G_mu_nu + Lambda g_mu_nu = (8*pi*G_cal/c^4) T_H_mu_nu + R_mu_nu^MTS`.

Here `G_cal` may be empirical at first pass, exactly as in GR, but it must be a single common silent coupling. Relative source weights, hidden drift, range/time/frame dependence, and non-Hilbert source selectors remain forbidden residuals unless derived/bounded.

## Source Register

| source_id | path | exists | parse_ok | role | evidence_hits | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| SRC3294_0 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3293-Y5-R2FR-parent-Hilbert-source-and-canonical-quantum-normalization-signature-under-AX1090.md | true | true | Hilbert source/common G handoff | L24:## Hilbert-Source Signature Theorem \| L28:\| HSSIG3293_0_target \| parent Hilbert-source signature \| There is one descended matter functional S_m[q(Phi),Psi,theta] and local source tensors/currents are defined only by its variational derivatives: T_mu_nu=-2/sqrt(-g) delta S_m/delta g^mu_nu and J_Q=1/sqrt(-g) delta S_m/delta A_Q. \| TARGET_SHARP \| source strength is no l... \| L31:\| HSSIG3293_3_parent_gap \| why not promoted \| The corpus still has to show that the MTS parent action actually descends to this single Hilbert-source signature; writing the signature is not the same as deriving the parent action. \| NOT_PARENT_SIGNED \| cleanly names the remaining local-GR matter coupling requirement. \| false \| \| L32:\| HSSIG3293_4_verdict \| signature status \| 3293 proves the exact local theorem: Hilbert-source signature excludes source-only scalars. It does not prove MTS owns the signature yet. \| CONDITIONAL_DERIVATION_NOT_PROMOTED \| the coupling problem is now a parent-action descent problem, not a beta_source_alpha fitting problem. \| fa... \| L65:\| RES3293_0_Hilbert_signature_zero_conditional \| formal_local_GR_coupling \| beta_source_only_label \| 0 if parent Hilbert-source signature and canonical readout are signed \| PASS_SYMBOLIC_NONCLAIM \| PARENT_ACTION_DESCENT;CANONICAL_QUANTUM_READOUT;EFFECTIVE_ACTION_GUARD \| false \| | false |
| SRC3294_1 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3293_NEXT_TARGET.csv | true | true | 3293 next target | L2:NEXT3293_0_3294,3294-Y5-R2FR-local-GR-reduction-contract-Hilbert-source-common-G-and-Newton-limit-under-AX1090.md,scripts/Y5_R2FR_3294_local_GR_reduction_contract_Hilbert_source_common_G_and_Newton_limit.py,"assemble the local GR reduction contract: single public metric/coframe, Einstein-like kinetic term or equivalent field ... | false |
| SRC3294_2 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3293_HILBERT_SOURCE_SIGNATURE_THEOREM.csv | true | true | Hilbert source theorem | L3:HSSIG3293_1_source_only_exclusion,ban post-variation source selectors,"If all source terms entering the local field equations are Hilbert/Noether variations of S_m, then T_source=sum_A kappa_A T_A introduced after variation is not allowed unless kappa_A already belongs to S_m and readout.",EXACT_CONDITIONAL_THEOREM,the source... \| L6:HSSIG3293_4_verdict,signature status,3293 proves the exact local theorem: Hilbert-source signature excludes source-only scalars. It does not prove MTS owns the signature yet.,CONDITIONAL_DERIVATION_NOT_PROMOTED,"the coupling problem is now a parent-action descent problem, not a beta_source_alpha fitting problem.",false | false |
| SRC3294_3 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3293_LOCAL_GR_MATTER_COUPLING_REDUCTION.csv | true | true | local GR matter coupling inputs | L3:LGR3293_1_common_G,Newton/G calibration,one universal common coupling constant kappa_G multiplying the total Hilbert source,common kappa_G can be calibrated as measured G; relative w_A cannot be hidden in G,CALIBRATION_ALLOWED_NOT_PREDICTIVE,false \| L5:LGR3293_3_Maxwell_stress,EM stress contribution,Hodge/Maxwell action from same public metric and same T_Q current owner,EM stress enters Hilbert source consistently with Poynting/Hodge branch,CONDITIONAL_ON_3286_3288_AND_TQ_SIGNATURE,false | false |
| SRC3294_4 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_3293_VALIDATION.csv | true | true | 3293 validation | L2:VAL3293_0_sources_exist,all cited source paths exist,true, \| L3:VAL3293_1_sources_parse,all cited source paths parse,true, \| L4:VAL3293_2_outputs_parse,all 3293 non-validation output CSVs parse,true, \| L5:VAL3293_3_signature_theorem_present,Hilbert-source theorem includes variational definitions and source-only exclusion,true, \| L6:VAL3293_4_canonical_readout_requirements_present,"canonical requirements include field normalization, action scale, measured readout, and effective action guard",true, | false |
| SRC3294_5 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3286-Y5-R2FR-Hodge-Poynting-factor-owner-or-first-CH-CS-slope-row-under-AX1090.md | true | true | Hodge/Poynting EM stress owner | L1:# 3286 - Hodge/Poynting factor owner or first C_H/C_S slope row under AX1090 \| L5:3286 gets past the loose-coupling stage: the Hodge/impedance slope `C_H` and the Poynting-flux slope `C_S` are not treated as independent mystery knobs. They collapse to one owner problem: \| L27:## Hodge/Poynting Owner Theorem \| L30:\| HP3286_0_premetric_owner \| one constitutive owner for Hodge and Poynting \| DEFINITION_AND_BRANCH_COMPRESSION \| C_H and C_S are not independent leaks once chi is owned. \| \| L31:\| HP3286_1_metric_Hodge_branch \| metric Hodge specialization \| STANDARD_CONDITIONAL_REDUCTION \| finite Hodge drift is reduced to Z_Q, g_pub, and any nonmetric Delta_chi. \| | false |
| SRC3294_6 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3287-Y5-R2FR-chi-to-metric-Hodge-premise-proof-or-DeltaChi-slope-source-row-under-AX1090.md | true | true | chi to metric Hodge reconstruction | L31:\| CHR3287_2_closure_to_metric_Hodge \| closure relation gives metric Hodge shape \| DERIVED_CONDITIONAL \| Hodge shape is no longer arbitrary; it follows from reciprocal nonbirefringent closure. \| \| L33:\| CHR3287_4_axion_and_impedance_residual \| Hodge shape does not fix scalar coupling or axion/readout drift \| DERIVED_OBSTRUCTION \| the missing coupling is specifically scalar impedance/gauge norm/readout ownership, not the whole Hodge tensor. \| \| L78:\| GATE3287_0_hodge_shape_conditional \| true \| false \| reciprocal nonbirefringent closure derives metric-Hodge shape up to scalar/axion/same-metric/readout clauses. \| \| L96:\| NEXT3287_0_3288 \| 3288-Y5-R2FR-same-public-metric-or-ZQ-impedance-owner-split-under-AX1090.md \| Use the 3287 split to attack the two remaining gates separately: prove g_EM=g_pub from cross-sector coframe/equivalence/Ward ownership, and prove or demote q-basic Z_Q from gauge norm/no-extra-F2/readout closure; if either fails,... \| L104:\| VAL3287_3_reconstruction_theorem_present \| reconstruction theorem includes Fresnel closure and Hodge shape \| true \| \| | false |
| SRC3294_7 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3288-Y5-R2FR-same-public-metric-or-ZQ-impedance-owner-split-under-AX1090.md | true | true | same public metric and calibrated Z_Q standard | L14:`[g_EM]=[g_pub]` plus shared observed coframe `e_obs` for matter, clocks, rods, source current, and EM stress. \| L46:\| LGR3288_0_value_vs_silence \| must MTS derive the numerical value of Z_Q immediately? \| no for local GR/Maxwell reduction; yes eventually for a stronger unification/prediction claim \| GR uses empirical G, but local tests require constants to be universal and not hidden/environment drifting. \| FAIR_CLAIM_STANDARD \| | false |
| SRC3294_8 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1100-Y5-R10-parent-TQ-owner-fixed-charge-lattice-and-gauge-norm-signature.md | true | true | T_Q/current and alpha normalization open clauses | L31:\| TQS1100_3_unique_curvature_norm \| observed F_Q^2 is the only allowed Maxwell kinetic subblock \| S_parent contains -C_P/4 int <F,F>_P and the Q subblock gives -C_P N_Q/4 int F_Q^2 with no independent lambda_A F_Q^2 or f_X F_Q^2 \| FAIL_CURRENT_CORPUS_COUNTERTERM_LEGAL \| 1057 and 1099 retain lambda_A and f_X F_Q^2 as legal unl... \| L32:\| TQS1100_4_same_current_owner \| matter current normalization is the Noether current of the same T_Q owner \| S_int=sum_A n_A int A_Q J_A, with J_Q=delta S_m/delta A_Q and no q_A(Xhat) or c_A current weights \| NOT_PARENT_SIGNED \| 765 current owner and 990 EM-lock both keep current normalization unsigned \| source/test alpha cha... \| L42:\| TQT1100_3_lambda_countermodel \| fixed norm alone is still insufficient without domain exhaustion \| Even if C_P N_Q exists, S -> S - lambda_A/4 int F_Q^2 gives Z_A=C_P N_Q+lambda_A unless the parent visible-operator domain forbids independent F_Q^2. \| COUNTEREXAMPLE_RETAINED \| operator-domain exhaustion/no-extra-F2 not deriv... \| L63:\| Z1100_4_total \| Z_A = C_P N_Q + lambda_A + f_X + delta_lambda_rad + readout \| honest current alpha normalization ledger \| FINITE_BRANCH_RETAINED \| b_alpha not theorem-zero unless all nonparent terms vanish and parent piece fixed \| \| L98:\| V1100_5_ZA_decomposition_retained \| pass \| honest Z_A decomposition retains finite branch \| | false |

## Local GR Reduction Contract

| contract_id | piece | required_statement | derived_if_signed | current_status | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| LGC3294_0_single_public_metric | public geometry | one observed metric/coframe g_pub/e_obs is shared by matter, clocks, rods, source current, Maxwell stress, and local gravitational field equation | no bimetric source split; EM stress and matter stress live in the same tensor equation | CONDITIONAL_FROM_3288_NOT_PARENT_SIGNED | false |
| LGC3294_1_Einstein_like_kinetic | gravitational left-hand side | the parent local metric equation reduces to G_mu_nu + Lambda g_mu_nu plus bounded higher-derivative/extra-field residuals | left-hand side is GR in the local weak-field regime | MAJOR_OPEN_THEOREM_LOVELOCK_ROUTE_NEXT | false |
| LGC3294_2_Hilbert_source | matter source | source is T_H_mu_nu=-2/sqrt(-g) delta S_m/delta g^mu_nu from one descended matter action | source-only species weights vanish by 3293 | EXACT_CONDITIONAL_NOT_PARENT_SIGNED | false |
| LGC3294_3_common_calibrated_G | coupling constant | one universal common constant kappa_G=8*pi*G_cal/c^4 couples the total Hilbert source | G can be empirically calibrated like GR; no relative species/source weights may hide in it | FAIR_ALLOWED_CALIBRATION_NOT_PREDICTION | false |
| LGC3294_4_Maxwell_stress | EM contribution | public Maxwell/Hodge action on g_pub supplies T_EM^mu_nu with no Poynting/background double count | EM stress enters the same Hilbert source consistently with 3286-3288 | CONDITIONAL_HODGE_BRANCH_NOT_FULLY_SIGNED | false |
| LGC3294_5_Newton_limit | Newtonian mechanics | weak-field slow-motion limit gives g_00=-(1+2Phi/c^2)+O(c^-4) and nabla^2 Phi=4*pi*G_cal*rho_total plus residuals | Newtonian mechanics follows as GR limit with calibrated G | CONDITIONAL_ON_LGC3294_0_TO_3_AND_SMALL_RESIDUALS | false |
| LGC3294_6_PPN_residual_gate | local tests | all extra-field, metric-split, source-weight, G-drift, and constitutive residuals are zero by theorem or bounded below PPN/WEP/orbital limits | local-GR claim can be promoted only after residual vector closes | BOUNDING_STAGE_REQUIRED | false |

## Conditional Local GR Theorem

| theorem_id | statement | status | not_a_claim_because | valid_for_claim |
| --- | --- | --- | --- | --- |
| LGT3294_0_conditional_GR_equation | If LGC3294_0..4 are parent-signed, the local MTS field equation reduces to G_mu_nu + Lambda g_mu_nu = (8*pi*G_cal/c^4) T_H_mu_nu + R_mu_nu^MTS with R_mu_nu^MTS=0 or bounded. | EXACT_CONDITIONAL_REDUCTION | Einstein-like kinetic term, same public metric, and Hilbert source are not all parent-signed. | false |
| LGT3294_1_common_G_fairness | A common constant G_cal is acceptable for first local-GR reduction just as GR uses measured G; the required derivation is universality/silence, not the numerical value. | FAIR_STANDARD_FORMALIZED | G drift and relative source weights remain residual gates. | false |
| LGT3294_2_Newton_limit | Under weak-field slow-motion assumptions and small residuals, the 00 equation gives nabla^2 Phi=4*pi*G_cal*rho_total plus explicit residual source terms. | STANDARD_GR_LIMIT_CONDITIONAL | the parent equation has not yet been proven Einstein-like. | false |
| LGT3294_3_no_Bianchi_smuggling | Bianchi identity supports consistency after the source is Hilbert-owned; it is not used as a standalone proof of universal coupling. | RED_TEAM_GUARD | constant relative source weights can evade simple divergence checks. | false |

## Newton Limit And Common G Calibration

| row_id | quantity | rule | forbidden_escape | status | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| NGC3294_0_common_G_allowed | G_cal | may be empirical/calibrated in first-pass local limit | species-dependent G_A, range-dependent G(r), time-drifting G(t), frame-dependent G_frame, or hidden-variable G(I_hid) | ALLOWED_COMMON_ONLY | false |
| NGC3294_1_Newton_Poisson | nabla^2 Phi | equals 4*pi*G_cal*rho_total when LGC3294 contract and weak-field limit are signed | rho_total reweighted by w_A or extra hidden source density without residual accounting | CONDITIONAL | false |
| NGC3294_2_orbital_PPN_bridge | PPN/orbital residual vector | score deviations only after deriving projection from R_mu_nu^MTS into gamma,beta,alpha_i,Gdot,Yukawa/source terms | declaring GR reduction because one sector is quiet | PROJECTION_REQUIRED | false |

## PPN/Newton/Maxwell Residual Vector

| residual_id | symbol | meaning | required_zero_or_bound | current_status | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| RV3294_0_metric_split | R_metric | g_EM, g_matter, g_clock, or source frame not the same public metric/coframe | same-public-metric theorem or optical/source-frame bounds | OPEN_FROM_3288 | false |
| RV3294_1_non_Einstein_kinetic | R_kin | left-hand side differs from Einstein tensor by higher derivative, scalar, vector, torsion, or memory terms | Lovelock/second-order metric theorem or PPN/orbital bounds | NEXT_TARGET | false |
| RV3294_2_non_Hilbert_source | R_source | source-only species weights or non-Hilbert source selector survives | 3293 parent Hilbert-source signature or WEP/PPN/R10 source-product bounds | CONDITIONAL_ZERO_NOT_PARENT_SIGNED | false |
| RV3294_3_G_drift | R_G | common coupling is not actually common/constant; hidden, time, range, or frame drift | q-basic G_cal or Gdot/range/fifth-force bounds | OPEN | false |
| RV3294_4_EM_constitutive | R_EM | Delta_chi, impedance drift, Poynting double count, or nonmetric Hodge stress | 3286-3288 Hodge/public metric/Z_Q gates or Delta_chi bounds | CONDITIONAL_ZERO_WITH_LIVE_DELTA_CHI | false |
| RV3294_5_readout_boundary | R_readout | radiative/readout/boundary terms reintroduce couplings after tree-level reduction | effective-action/readout closure or source-backed product bounds | OPEN | false |

## Nonclaim Runner

| run_id | check | observed_status | expectation_match | claim_allowed |
| --- | --- | --- | --- | --- |
| RUN3294_0_contract_shape | local GR contract has all named pieces | PASS_SYMBOLIC_NONCLAIM | true | false |
| RUN3294_1_common_G | common G allowed only as universal calibration | PASS_SYMBOLIC_NONCLAIM | true | false |
| RUN3294_2_Newton_limit | Newton limit conditional on Einstein kinetic + Hilbert source | PASS_SYMBOLIC_NONCLAIM | true | false |
| RUN3294_3_residual_vector | claim refused until residual vector zero/bounded | REFUSE_CLAIM_NONCLAIM | true | false |

## Promotion Gates

| gate_id | gate | passed | claim_allowed | detail |
| --- | --- | --- | --- | --- |
| GATE3294_0_contract_complete | local GR reduction contract names all required pieces | true | false | this is a structured contract, not a proof. |
| GATE3294_1_Einstein_kinetic_signed | Einstein-like kinetic term parent-signed | false | false | next target is Lovelock/metric kinetic theorem. |
| GATE3294_2_Hilbert_source_signed | Hilbert-source signature parent-signed | false | false | 3293 gives conditional theorem only. |
| GATE3294_3_residual_vector_closed | PPN/Newton/Maxwell residual vector zero or bounded | false | false | residual projection/bounds remain open. |

## Decision Ledger

| decision_id | finding | consequence | claim_allowed |
| --- | --- | --- | --- |
| DEC3294_0_spine_progress | The local-GR route now has a precise contract: single public metric, Einstein-like kinetic term, Hilbert source, common calibrated G, Maxwell stress, Newton limit, and residual vector. | future work can attack one contract piece at a time rather than circling generic coupling concerns. | false |
| DEC3294_1_G_policy | Deriving numerical G is not required before local-GR reduction; proving common universality/no drift is required. | this matches the fair GR standard while still blocking source-weight cheats. | false |
| DEC3294_2_best_next | The biggest remaining local-GR gap is the gravitational left-hand side. | next target should use the Lovelock/second-order metric route: derive Einstein tensor plus Lambda or explicitly parameterize R_kin. | false |

## Next Target

| next_id | target_doc | target_script | objective | guardrails | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| NEXT3294_0_3295 | 3295-Y5-R2FR-Lovelock-metric-kinetic-owner-or-non-Einstein-residual-vector-under-AX1090.md | scripts/Y5_R2FR_3295_Lovelock_metric_kinetic_owner_or_non_Einstein_residual_vector.py | derive or reject the Einstein-like gravitational left-hand side from locality, diffeomorphism invariance, single metric, second-order field equations, and no extra propagating local fields; if rejected, parameterize R_kin for PPN/Newton/orbital tests. | do not assume GR kinetic term by taste; do not use Bianchi alone; do not claim local GR until R_kin and the residual vector are zero or bounded. | false |

## Validation

| check_id | check | passed | detail |
| --- | --- | --- | --- |
| VAL3294_0_sources_exist | all cited source paths exist | true |  |
| VAL3294_1_sources_parse | all cited source paths parse | true |  |
| VAL3294_2_outputs_parse | all 3294 non-validation output CSVs parse | true |  |
| VAL3294_3_contract_pieces_complete | contract includes geometry, kinetic, Hilbert source, common G, Maxwell stress, Newton limit, and residual gate | true |  |
| VAL3294_4_GR_equation_and_no_Bianchi_smuggling | theorem states conditional GR equation and no Bianchi smuggling | true |  |
| VAL3294_5_Newton_and_G_policy_present | Newton/G table allows common G and forbids species/range/time/frame drift | true |  |
| VAL3294_6_residual_vector_complete | residual vector includes metric, kinetic, source, G, EM, and readout terms | true |  |
| VAL3294_7_runner_expectations | runner expectations all match | true | RUN3294_0_contract_shape=PASS_SYMBOLIC_NONCLAIM;RUN3294_1_common_G=PASS_SYMBOLIC_NONCLAIM;RUN3294_2_Newton_limit=PASS_SYMBOLIC_NONCLAIM;RUN3294_3_residual_vector=REFUSE_CLAIM_NONCLAIM |
| VAL3294_8_claim_gates_false | no 3294 gate allows local GR claim | true |  |
| VAL3294_9_next_target_Lovelock | next target focuses Lovelock/metric kinetic owner or non-Einstein residual | true |  |
| VAL3294_10_decision_records_spine_progress | decision ledger records local-GR spine and G policy | true |  |
| VAL3294_11_formalization_untouched | formalization-workbench modified-file count remains zero by this script | true | formalization_changed_count=0 |
| VAL3294_12_overall | 3294 validation overall | true | all required checks passed |
