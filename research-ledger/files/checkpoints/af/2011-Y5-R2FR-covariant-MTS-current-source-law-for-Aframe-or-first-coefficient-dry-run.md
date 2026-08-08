# 2011 Y5 R2FR: Covariant MTS Current Source Law For A-Frame Or First Coefficient Dry-Run

Private checkpoint. This attacks the least-circular route left by 2010: derive a covariant MTS moment/current that sources `A^a_MTS`, or turn the A-frame residual into coefficient rows that refuse placeholders.

## Current Verdict

The covariant source-law route is **not derived yet**. A plausible scaffold can be written:

`E_A^a_mu = delta S_A/delta A^a_mu = kappa_A J_MTS^a_mu`, with `A^a_mu(x)=kappa_A integral G_A(x,y)J_MTS^a_mu(y)dV_y`.

But this is not yet a parent theorem. The parent action `S_A`, the current `J_MTS`, the Green kernel, the rank/domain certificate, and the boundary no-hair theorem are all missing. Most importantly, ordinary current conservation is explicitly not enough: it can leave an exterior A-charge/hair, just like the earlier reciprocal-cell current obstruction.

The practical win is that the first coefficient dry-run now exists and refuses fake numbers. `C_A`, `lambda_A`, `f_A(r)`, `alpha_A(lambda_A)`, PPN, clock/orbital, and `q_loc` handoff slots are named, but all remain nonclaim until sourced or theorem-zeroed.

No local-GR/Newton/WEP/R10 claim is promoted.

## Source Register
| source_id | source_path | status | needles | note |
| --- | --- | --- | --- | --- |
| SRC2011_00_2010_handoff | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\2010-Y5-R2FR-Aframe-parent-source-map-rank-certificate-or-residual-coefficient-source-pack.md | EXISTS_NEEDLES_CONFIRMED | NEXT2010_0_2011;DEC2010_1_best_derivation_route;VAL2010_OVERALL | 2010 selected covariant MTS current/source law or first coefficient dry-run. |
| SRC2011_01_2009_kernel | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\2009-Y5-R2FR-Aframe-no-extra-mode-theorem-or-first-residual-response-kernel.md | EXISTS_NEEDLES_CONFIRMED | KER2009_5_R10_yukawa_projection;KER2009_7_total_response_vector;VAL2009_OVERALL | symbolic A-frame residual kernel to feed if source-law derivation fails. |
| SRC2011_02_cell_current_warning | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\11-cell-current-origin-attempt.md | EXISTS_NEEDLES_CONFIRMED | cell_current_origin_no_charge_obstruction;Q_R = constant.;ordinary cell-current conservation does not close | ordinary conserved current leaves hair unless a no-charge theorem is supplied. |
| SRC2011_03_parent_current_chain | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1009-Y5-R10-parent-current-chain-action-contract-or-sector-variation-runner.md | EXISTS_NEEDLES_CONFIRMED | PCS1009_4_Gamma_Khat_extra;DEC1009_1_root_hard_block;V1009_SUMMARY | parent current-chain action contract and Gamma/Khat/q_loc action-existence blocker. |
| SRC2011_04_source_hunt_warning | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1266-Y5-R10-RAB-primitive-auxiliary-grammar-source-hunt-or-finite-ZR-intake-review.md | EXISTS_NEEDLES_CONFIRMED | HUNT1266_7_cell_current;DEC1266_1_best_derivation_route;VAL1266_3_source_hunt_nonclaim | source-hunt warning that ordinary current conservation gives hair unless a constraint already exists. |
| SRC2011_05_local_residuals | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\790-Y5-R10-MTS-exchange-stress-decomposition-and-local-suppression-gates.md | EXISTS_NEEDLES_CONFIRMED | LSG790_0_Ward_compatible_split;LSG790_3_anisotropic_PPN_suppression;D790_1_Q_first | Bianchi-compatible residual split and PPN suppression gates. |
| SRC2011_06_q_loc_split | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\791-Y5-R10-Ward-compatible-exchange-current-q-loc-zero-or-bound.md | EXISTS_NEEDLES_CONFIRMED | ECT791_1_q_loc_geometric;WZG791_3_geometric_q_loc_zero;D791_1_q_loc_still_open | ordinary matter Ward zero does not automatically kill geometric q_loc. |


## Covariant Current Source-Law Attempt
| current_id | object | status | missing_before_claim | parent_signed |
| --- | --- | --- | --- | --- |
| CSA2011_0_target | J_MTS^a_mu -> A^a_MTS | TARGET_EXACT | needs parent action, covariance, split-gauge compatibility, rank/domain certificate, and no-hair/no-spurion clauses | false |
| CSA2011_1_ordinary_conserved_current | D_mu J_MTS^{a mu}=0 | REJECTED_AS_ZERO_THEOREM | it can make A source conserved, but does not prove the A charge/amplitude is zero or small | false |
| CSA2011_2_Ward_Noether_current | J_MTS from diffeo/local-Lorentz Noether identity | WARD_COMPATIBLE_NOT_SOURCE_MAP | requires a parent action and boundary charge theorem before it becomes ownership | false |
| CSA2011_3_moment_current_candidate | J_MTS^a_mu = P^a_rho D_nu M_MTS^{rho nu}{}_mu or covariant projection of coarse-grained motion moments | PROMISING_FORMAL_CANDIDATE | the moment tensor, projector, evolution equation, and projection to Lorentz-vector one-form are not parent-derived | false |
| CSA2011_4_action_equation_candidate | E_A^a_mu := delta S_A/delta A^a_mu = kappa_A J_MTS^a_mu | FORMAL_EQUATION_ONLY | no S_A, Helmholtz-compatible E_A, theta_A, or Q_tau contribution is sourced | false |
| CSA2011_5_green_function_candidate | A^a_mu(x)=kappa_A integral G_A(x,y) J_MTS^a_mu(y) dV_y | TESTABLE_RESIDUAL_ROUTE | it is a finite residual/source model unless kappa_A, G_A, and J_MTS are parent-derived | false |
| CSA2011_6_rank_domain | rank(delta A/delta J_MTS * delta J_MTS/delta Phi_MTS) | MISSING_RANK_DOMAIN_CERTIFICATE | no current map is available to certify rank or local Lorentzian domain | false |
| CSA2011_7_verdict | covariant MTS current source law | CURRENT_SOURCE_LAW_NOT_DERIVED | move to A-current no-hair/source-neutrality theorem or keep coefficient dry-run as fallback | false |


## Covariance And No-Spurion Guards
| guard_id | clause | why_needed | status |
| --- | --- | --- | --- |
| COV2011_0_diffeomorphism | J_MTS^a_mu is a covariant one-form density or one-form with measure fixed by e | required so A equation has tensor meaning and total Ward identity can close | UNSIGNED |
| COV2011_1_local_Lorentz | J_MTS^a_mu transforms as an internal Lorentz vector and has no preferred-frame spurion | required so the completed tetrad does not carry hidden species/readout frame labels | UNSIGNED |
| COV2011_2_split_gauge | source law depends on e=dX+A or split-gauge invariant combinations, not X and A separately in observable sectors | protects the no-extra-mode closure theorem from 2009 | UNSIGNED |
| COV2011_3_Bianchi | D_mu E_A^{a mu}=D_mu(kappa_A J_MTS^{a mu}) is compatible with total stress conservation | prevents an A source from becoming an unbalanced q_loc or non-geodesic force | UNSIGNED |
| COV2011_4_boundary_nohair | surface charge Q_A=integral_boundary *J_A or conjugate Pi_A^n vanishes or is bounded | ordinary current conservation alone leaves charge hair | MISSING_NOHAIR_THEOREM |
| COV2011_5_matter_blindness | ordinary matter couples to e, omega[e], and owned gauge fields only | needed for Ward matter-zero and WEP/clock safety | UNSIGNED |
| COV2011_6_guard_verdict | all covariance guards | the source-current route is meaningful but cannot be promoted without these guards | GUARDS_NOT_PARENT_SIGNED |


## First Coefficient Dry-Run
| dry_id | symbol | meaning | formula_or_rule | missing_input | dry_run_status | note |
| --- | --- | --- | --- | --- | --- | --- |
| DRY2011_0_C_A | C_A | overall A-source coupling/amplitude | A response amplitude from A=kappa_A G_A*J_MTS | MISSING_PARENT_COEFFICIENT | REFUSED_PLACEHOLDER | required before Newton/PPN/clock/R10 scoring |
| DRY2011_1_lambda_A | lambda_A | range/correlation length or inverse mass of A residual | lambda_A from Green kernel pole or screening profile | MISSING_RANGE_OR_SCREENING_MAP | REFUSED_PLACEHOLDER | required before R10/orbital profile scoring |
| DRY2011_2_f_A | f_A(r) | normalized local source profile | h_A00(r)=2 C_A f_A(r) in weak-field normalization after gauge fixing | MISSING_PROFILE | REFUSED_PLACEHOLDER | required before acceleration/clock/orbital integrals |
| DRY2011_3_alpha_A | alpha_A(lambda_A) | Yukawa-equivalent R10 amplitude | if h_A00=2 G M alpha_A exp(-r/lambda_A)/(c^2 r), compare \|alpha_A\| to bound(lambda_A) | MISSING_C_A_LAMBDA_PROFILE_AND_FULL_BOUND_CURVE | REFUSED_PLACEHOLDER | anchor-only rows remain smoke-only |
| DRY2011_4_PPN_vector | delta_PPN_A | PPN residual vector | J_PPN[A] dot (C_A,lambda_A,profile parameters) | MISSING_PPN_RESPONSE_MATRIX | REFUSED_PLACEHOLDER | do not score gamma/beta/alpha_i without weak-field projection |
| DRY2011_5_clock_orbit | delta_clock_A, delta_orbit_A | clock and orbital residuals | integrate h_A along clock sites or orbital/light-time kernels | MISSING_SOURCE_PROFILE_AND_BOUNDS | REFUSED_PLACEHOLDER | do not claim local pass from symbolic kernel |
| DRY2011_6_q_loc_handoff | h_Q_mu_nu | metric response to geometric q_loc carrier | solve div T_Q=-q_loc and apply linearized response | MISSING_GAMMA_EFF_KHAT_EQUATIONS | REFUSED_PLACEHOLDER | keeps q_loc separate from ordinary matter Ward zero |
| DRY2011_7_dry_run_verdict | first coefficient dry-run | dry-run schema is executable but every numeric coefficient is missing | claim false until all inputs are sourced or theorem-zero | ALL_NUMERIC_INPUTS_MISSING | DRY_RUN_PASS_REFUSAL | this is good plumbing, not evidence |


## Claim Gates
| gate_id | gate | status | reason | passed_for_claim |
| --- | --- | --- | --- | --- |
| CG2011_0_current_scaffold | covariant current source scaffold written | PASS_NONCLAIM | formal source-law rows exist | false |
| CG2011_1_current_derivation | J_MTS -> A parent-derived | FAIL_BLOCKED | no parent S_A/E_A/J_MTS derivation or variation certificate | false |
| CG2011_2_ordinary_current_zero | ordinary current conservation proves A charge zero | FAIL_REJECTED | conservation leaves exterior charge/hair unless no-hair theorem is added | false |
| CG2011_3_covariance_guards | diffeo/Lorentz/split-gauge/Bianchi guards signed | FAIL_BLOCKED | guards are requirements, not parent-signed results | false |
| CG2011_4_coeff_dry_run | first coefficient dry-run refuses placeholders | PASS_NONCLAIM | C_A, lambda_A, alpha_A slots are explicit but missing | false |
| CG2011_5_R10_PPN_clock_orbit | local arenas score-ready | FAIL_BLOCKED | no coefficients, full bound curves, or response matrices | false |
| CG2011_6_local_GR_Newton | local GR/Newton derived | FAIL_BLOCKED | A ownership, nohair, q_loc, R11, and matter silence remain open | false |


## Decision Ledger
| decision_id | verdict | rationale | next_action |
| --- | --- | --- | --- |
| DEC2011_0_result | COVARIANT_CURRENT_SOURCE_LAW_NOT_DERIVED | A credible J_MTS -> A scaffold can be written, but the parent action, source current, and boundary no-hair theorem are missing. | do not claim A ownership; attack the A-current no-hair/source-neutrality theorem next |
| DEC2011_1_current_warning | ORDINARY_CURRENT_CONSERVATION_IS_NOT_ENOUGH | The project has seen this trap before: a conserved current can leave Q_A/Q_R hair, which is exactly a finite local residual. | require Q_A=0 from gauge/topology/boundary silence or keep finite coefficient rows |
| DEC2011_2_testing_plumbing | FIRST_C_A_LAMBDA_ALPHA_DRY_RUN_READY_BUT_EMPTY | The R10/PPN/clock/orbital plumbing now refuses placeholders while preserving the exact coefficient slots we need. | fill coefficients only from parent derivation or source-backed bounds/profiles |


## Branch Copies
| copy_id | copy_path | exists | note |
| --- | --- | --- | --- |
| COPY2011_0 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\source-weight\docs\COVARIANT_MTS_CURRENT_AFRAME_2011_NONCLAIM.csv | True | covariant MTS current A-frame attempt nonclaim copy |
| COPY2011_1 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope\branch_locked_wep\residuals\P8_Y5_PARENT_QLOC_2011_CURRENT_SOURCE_STATUS_NONCLAIM.csv | True | A-frame current covariance/no-spurion guard status nonclaim copy |
| COPY2011_2 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\rab-sector\acquisition-queue\JR2011_AFRAME_COEFFICIENT_DRY_RUN_QUEUE.csv | True | A-frame coefficient dry-run queue |


## Next Target
| target_id | next_doc | objective | include | exclude |
| --- | --- | --- | --- | --- |
| NEXT2011_0_2012 | 2012-Y5-R2FR-Aframe-current-nohair-source-neutrality-theorem-or-finite-QA-row.md | try to prove the A-current charge Q_A vanishes by gauge/topology/source-neutrality/boundary silence; if not, create finite Q_A/C_A/lambda_A residual rows for the A-frame kernel | Q_A definition; boundary momentum Pi_A^n; nohair theorem clauses; split-gauge and matter silence; finite residual coefficient rows; R10/PPN/clock/orbital routing | ordinary current conservation as zero proof; scalar exact-gradient retry; unlabelled tetrad insertion; local-GR claim; GitHub; formalization-workbench edits |


## Validation
| check_id | status | detail |
| --- | --- | --- |
| VAL2011_00_sources | PASS | all cited source paths exist and needles are found |
| VAL2011_01_current_not_promoted | PASS | current source law not falsely promoted |
| VAL2011_02_ordinary_current_rejected | PASS | ordinary current conservation rejected as zero theorem |
| VAL2011_03_covariance_guards_unsigned | PASS | covariance/no-spurion guards remain unsigned |
| VAL2011_04_dry_run_refuses_placeholders | PASS | coefficient dry-run rows remain missing/nonclaim |
| VAL2011_05_dry_run_covers_core_slots | PASS | dry-run covers C_A/lambda_A/alpha_A/PPN/q_loc |
| VAL2011_06_claim_gates_blocked | PASS | all claim gates remain blocked |
| VAL2011_07_csv_parse | PASS | all generated CSV outputs parse cleanly |
| VAL2011_08_branch_copies | PASS | branch-copy CSVs exist |
| VAL2011_09_no_formalization_edits | PASS | formalization-workbench modified-file count remains 0 for this run |
| VAL2011_10_output_scope | PASS | all outputs are under post-checkpoint-work |
| VAL2011_OVERALL | PASS | 2011 covariant MTS current source law for A-frame or first coefficient dry-run |

