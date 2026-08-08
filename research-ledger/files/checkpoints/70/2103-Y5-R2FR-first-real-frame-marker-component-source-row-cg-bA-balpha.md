# 2103 - Y5/R2FR First Real Frame-Marker Component Source Row: c_g, b_A, b_alpha

## Current Verdict

2103 moves us past the abstract coupling fog. It records real experimental anchors for the first three live frame/marker components: `c_g` via PPN/Cassini and short-range gravity, `b_A` via MICROSCOPE/WEP composition sensitivity, and `b_alpha` via optical-clock fine-structure constraints.

This is **not** a local-GR, R10, WEP or clock claim. These sources bound observable residuals, not raw MTS variables. The missing object is now the projection matrix from MTS components into each arena.

The best next derivation is `c_g -> PPN gamma`: either derive the coefficient mapping common-frame coupling into the Cassini/Shapiro residual, or prove it is an exact measured-frame degeneracy with no observable PPN residue.

## Local Source Register
| source_id | source_path | path_exists | needle_found | use_in_2103 | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| SRC2103_00_2102_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\2102-Y5-R2FR-frame-marker-coupling-bound-input-pack-or-no-marker-theorem.md | true | true | 2102 selects first real frame/marker component source rows rather than another no-marker loop. | false |
| SRC2103_01_2102_bound_rows | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2102_BOUND_INPUT_ROWS.csv | true | true | 2102 bound input rows define c_g, b_A and b_alpha as live nonclaim components. | false |
| SRC2103_02_2102_components | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2102_SURVIVING_COUPLING_COMPONENTS.csv | true | true | 2102 surviving components identify the three first source targets. | false |
| SRC2103_03_2102_arenas | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2102_ARENA_RESIDUAL_MAP.csv | true | true | 2102 arena rows map c_g/b_A/b_alpha to PPN, WEP and EM/clock tests. | false |
| SRC2103_04_2102_decision | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2102_DECISION_LEDGER.csv | true | true | 2102 decision says the non-looping route is a first component source row. | false |
| SRC2103_05_2102_next | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2102_NEXT_TARGET.csv | true | true | 2102 next target points exactly at this source table. | false |
| SRC2103_06_2102_validation | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_2102_VALIDATION.csv | true | true | 2102 validation is clean and nonclaim. | false |

## External Source Anchors
| external_id | source_title | citation | doi_url | source_url | observable | source_bound_or_measurement | candidate_mts_components | mts_mapping_status | score_ready | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EXT2103_0_cassini_ppn_gamma | Cassini radio-link test of GR | Bertotti, Iess, Tortora, Nature 425, 374-376 (2003) | https://doi.org/10.1038/nature01997 | https://pubmed.ncbi.nlm.nih.gov/14508481/ | PPN gamma / Shapiro delay | gamma = 1 + (2.1 +/- 2.3) x 10^-5 | c_g;b_dis;q_nonH | MTS_PPN_PROJECTION_MISSING | false | false |
| EXT2103_1_microscope_wep | MICROSCOPE final WEP result | Touboul et al., Phys. Rev. Lett. 129, 121102 (2022) | https://doi.org/10.1103/PhysRevLett.129.121102 | https://arxiv.org/abs/2209.15487 | Eotvos ratio eta(Ti,Pt) | eta(Ti,Pt) = [-1.5 +/- 2.3(stat) +/- 1.5(syst)] x 10^-15 | b_A;b_marker;delta_kappa_A;q_domain | MTS_COMPOSITION_PROJECTION_MISSING | false | false |
| EXT2103_2_eotwash_short_range | Eot-Wash inverse-square law anchor | New Test of the Gravitational 1/r^2 Law at Separations down to 52 um, Phys. Rev. Lett. 124, 101101 (2020) | https://doi.org/10.1103/PhysRevLett.124.101101 | https://www.npl.washington.edu/eotwash/node/1 | short-range Yukawa alpha(lambda) | separations down to 52 um; full alpha(lambda) curve still needs digitization/table | c_g;b_A;delta_kappa_A;q_boundary | MTS_R10_ALPHA_CURVE_AND_PROJECTION_MISSING | false | false |
| EXT2103_3_rosenband_alpha_clock | Al+/Hg+ optical-clock alpha variation | Rosenband et al., Science 319, 1808-1812 (2008) | https://doi.org/10.1126/science.1154622 | https://pubmed.ncbi.nlm.nih.gov/18323415/ | present-era fine-structure variation | dot(alpha)/alpha = (-1.6 +/- 2.3) x 10^-17 yr^-1 | b_alpha;b_A;b_marker;c_g | MTS_CLOCK_ALPHA_PROJECTION_MISSING | false | false |

## Component Source Rows
| row_id | symbol | source_arena | external_source_id | mts_projection_formula | source_tolerance_anchor | current_blocker | score_ready | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CSR2103_0_cg_ppn | c_g | PPN gamma | EXT2103_0_cassini_ppn_gamma | Delta_gamma_MTS = Pi_gamma_cg*c_g + Pi_gamma_dis*b_dis + Pi_gamma_nonH*q_nonH | tau_gamma ~= O(10^-5) from Cassini source anchor | MISSING_Pi_gamma_cg_AND_FRAME_LOCK | false | false |
| CSR2103_1_cg_r10 | c_g | short-range Yukawa alpha(lambda) | EXT2103_2_eotwash_short_range | alpha_MTS(lambda)=K_X(lambda)*Qbar_XH(lambda)*qbar_XT(c_g,...) | source anchor exists, but no digitized alpha(lambda) curve in this row | MISSING_K_X_Qbar_XH_AND_DIGITIZED_CURVE | false | false |
| CSR2103_2_bA_wep | b_A | MICROSCOPE eta(Ti,Pt) | EXT2103_1_microscope_wep | eta_TiPt_MTS = Pi_eta_bA*(b_A^Ti-b_A^Pt)+Pi_eta_marker*b_marker+Pi_eta_kappa*delta_kappa_A | tau_eta ~= O(10^-15) from MICROSCOPE source anchor | MISSING_COMPOSITION_CHARGE_MAP_AND_Pi_eta_bA | false | false |
| CSR2103_3_balpha_clock | b_alpha | clock alpha variation | EXT2103_3_rosenband_alpha_clock | clock_residual_MTS = Pi_clock_alpha*b_alpha + Pi_clock_A*b_A + Pi_clock_cg*c_g | tau_alpha_dot ~= O(10^-17 yr^-1) source anchor | MISSING_CLOCK_SENSITIVITY_AND_LOCAL_SPATIAL_PROJECTION | false | false |
| CSR2103_4_abs_vector_gate | qbar_XT_bound_abs | all local arenas | EXT2103_0;EXT2103_1;EXT2103_2;EXT2103_3 | \|\|r_local\|\| <= \|Pi_cg c_g\|+\|Pi_bA b_A\|+\|Pi_balpha b_alpha\|+other unsigned components | no cancellation allowed; source anchors only bound projected residuals after Pi rows exist | MISSING_PROJECTION_MATRIX_AND_COMPONENT_VALUES | false | false |

## Missing Projection Inputs
| missing_id | required_quantity | definition | how_to_get | blocks | status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| MPR2103_0_Pi_gamma_cg | Pi_gamma_cg | coefficient mapping c_g into PPN gamma/Shapiro delay residual | derive from local weak-field action or parent matter-frame transformation | blocks c_g->Cassini score | MISSING_REQUIRED_PROJECTION_INPUT | false |
| MPR2103_1_frame_lock | frame_lock | proof that operational rods/clocks use the same frame that enters PPN comparison | derive readout-frame lock or include frame degeneracy parameter | blocks measured-G/calibration absorption shortcut | MISSING_REQUIRED_PROJECTION_INPUT | false |
| MPR2103_2_R10_kernel | K_X Qbar_XH | R10 source/test kernel for finite-range component exchange | derive kernel or source from existing R10 runner inputs | blocks alpha(lambda) comparator | MISSING_REQUIRED_PROJECTION_INPUT | false |
| MPR2103_3_composition_charges | Delta q_A(Ti,Pt) | composition sensitivity of b_A/b_marker/delta_kappa_A for MICROSCOPE materials | derive material charge vector or source conservative sensitivity coefficients | blocks WEP score | MISSING_REQUIRED_PROJECTION_INPUT | false |
| MPR2103_4_clock_sensitivity | Pi_clock_alpha | clock transition sensitivity to b_alpha and readout frame | source K_alpha for Al+/Hg+ or use clock-comparison sensitivity table | blocks EM/clock score | MISSING_REQUIRED_PROJECTION_INPUT | false |
| MPR2103_5_abs_norm | local residual norm | common absolute norm joining PPN, WEP, R10 and clock rows without cancellations | define vector norm and acceptance rules | blocks any combined local-GR pass | MISSING_REQUIRED_PROJECTION_INPUT | false |

## Claim Gates
| gate_id | gate | gate_pass | reason | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| GATE2103_0_sources | external source anchors exist | true | Cassini, MICROSCOPE, Eot-Wash and clock anchors are recorded | false | false |
| GATE2103_1_projection | MTS projection matrix exists | false | Pi_gamma_cg, R10 kernel, composition charges and clock sensitivities are missing | false | false |
| GATE2103_2_component_values | component values or zero theorems exist | false | c_g, b_A and b_alpha remain unsigned | false | false |
| GATE2103_3_abs_envelope | absolute no-cancellation residual envelope exists | false | rule exists but norm/projection rows are missing | false | false |
| GATE2103_4_local_GR | derived local GR/Newton limit can be claimed | false | requires projection matrix plus component zeros/bounds below all source anchors | false | false |

## Decision Ledger
| decision_id | decision | because | next_action | valid_for_claim |
| --- | --- | --- | --- | --- |
| DEC2103_0_source_result | REAL_SOURCE_ANCHORS_STAGED_NONCLAIM | The project now has real PPN/WEP/R10/clock anchors for c_g, b_A and b_alpha, but they are not MTS scores. | keep them as source-backed projection targets only | false |
| DEC2103_1_best_first_derivation | CG_TO_PPN_PROJECTION_MATRIX_NEXT | c_g to PPN gamma is the cleanest GR/Newton-facing derivation because it attacks the universal-frame coupling before composition complications. | derive Pi_gamma_cg or prove common-frame degeneracy/readout absorption explicitly | false |
| DEC2103_2_no_claim | NO_LOCAL_GR_OR_R10_CLAIM_FROM_SOURCE_ANCHORS | Experimental bounds constrain projected residuals, not raw MTS components, until projection coefficients are derived. | do not compare raw c_g/b_A/b_alpha to external tolerances | false |

## Next Target
| route_id | next_target | script | objective | forbidden_shortcuts | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| NEXT2103_0_2104 | 2104-Y5-R2FR-cg-to-PPN-projection-matrix-or-measured-frame-degeneracy.md | scripts/Y5_R2FR_cg_to_PPN_projection_matrix_or_measured_frame_degeneracy_2104.py | Derive the coefficient mapping common frame coupling c_g into PPN gamma/Shapiro residual, or prove it is exactly a measured-frame degeneracy with no observable PPN residue. | raw c_g compared directly to gamma; measured-G handwave; cancellation against b_dis/q_nonH; local-GR claim without projection matrix | false |

## Branch Copies
| copy_id | destination | path_exists | row_count | parse_ok | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| COPY2103_0_source_weight_docs | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\source-weight\docs\AFRAME_FIRST_FRAME_MARKER_SOURCE_2103_NONCLAIM.csv | true | 12 | true | false |
| COPY2103_1_branch_locked_wep | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope\branch_locked_wep\residuals\P8_Y5_PARENT_QLOC_2103_CG_BA_BALPHA_SOURCE_STATUS_NONCLAIM.csv | true | 11 | true | false |
| COPY2103_2_acquisition_queue | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\rab-sector\acquisition-queue\JR2103_CG_PPN_PROJECTION_OR_FRAME_DEGENERACY_QUEUE.csv | true | 7 | true | false |

## Validation
| check_id | status | detail | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- |
| VAL2103_00_local_sources | PASS | 2102 handoff files exist and contain required needles | false | false |
| VAL2103_01_external_sources | PASS | real PPN/WEP/R10/clock source anchors recorded with URLs | false | false |
| VAL2103_02_component_rows | PASS | c_g/b_A/b_alpha rows are source-backed but projection-incomplete | false | false |
| VAL2103_03_missing_projection | PASS | projection matrix and sensitivity inputs remain explicit blockers | false | false |
| VAL2103_04_claim_gates | PASS | claim gates block local-GR/Newton promotion | false | false |
| VAL2103_05_decision | PASS | decision selects c_g to PPN projection as next derivation | false | false |
| VAL2103_06_next | PASS | next target is 2104 c_g to PPN projection or frame degeneracy | false | false |
| VAL2103_07_branch_copies | PASS | branch copies exist and parse | false | false |
| VAL2103_08_csv_parse | PASS | all generated CSVs parse cleanly | false | false |
| VAL2103_09_no_claim_flags | PASS | no generated row allows a claim or score | false | false |
| VAL2103_10_formalization_clean | PASS | formalization-workbench untouched by 2103 | false | false |
| VAL2103_11_no_pycache | PASS | scripts __pycache__ removed | false | false |
| VAL2103_OVERALL | PASS | 2103 stages real source anchors for c_g/b_A/b_alpha, blocks claims, and selects c_g->PPN projection next | false | false |
