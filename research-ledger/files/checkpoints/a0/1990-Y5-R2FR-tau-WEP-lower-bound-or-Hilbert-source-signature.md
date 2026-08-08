# 1990 Y5 R2FR: Tau WEP Lower Bound Or Hilbert Source Signature

Private checkpoint. This tries the 1989 fork honestly: can `tau_WEP` or `P_WEP` be bounded away from zero, or must the branch lean harder on the parent Hilbert-source zero theorem?

Verdict: the symbolic `tau_WEP` functional is retained, but no lower bound is derived. The obstruction is mathematical, not cosmetic: `tau_WEP` is an orbit/readout/source/material inner product, and such a projection can vanish by orthogonality or mask cancellation even when every named factor is nonzero.

Therefore the finite WEP route needs a real nondegeneracy certificate: official/readout-equivalent `K_eta`, Earth/source worldtube, Ti/Pt material tensor, product normalization, sign convention, and an alignment floor. The clean GR/Newton route remains the parent Hilbert-source theorem: if ordinary matter has one universal Hilbert source and no species/source-weight slot, then `DeltaW_TiPt=0` and tau lower bounds are unnecessary for the WEP zero.

No WEP, local-GR, Newton, R10, PPN, clock, orbital, or public claim follows from 1990.

## Source Register

| branch_id | valid_for_claim | claim_allowed | generated_utc | source_id | source_path | needed_for | needles | exists | anchor_found | missing_needles | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | false | false | 2026-06-20T02:36:02.379592+00:00 | 1989_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1989-Y5-R2FR-WEP-source-weight-projection-denominator-or-Hilbert-signature.md | 1990 tau_WEP lower-bound or Hilbert-source signature gate | NEXT1989_0_primary;DEN1989_2_tau_lower_bound | True | True |  | EXISTS_NEEDLES_CONFIRMED |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | false | false | 2026-06-20T02:36:02.379592+00:00 | 1989_validation | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_1989_VALIDATION.csv | 1990 tau_WEP lower-bound or Hilbert-source signature gate | VAL1989_OVERALL;PASS | True | True |  | EXISTS_NEEDLES_CONFIRMED |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | false | false | 2026-06-20T02:36:02.379592+00:00 | 1225_tau_contract | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1225-Y5-R10-tau-WEP-source-worldtube-readout-projection.md | 1990 tau_WEP lower-bound or Hilbert-source signature gate | FORM1225_0_tau_WEP_functional;TAU1225_6_verdict | True | True |  | EXISTS_NEEDLES_CONFIRMED |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | false | false | 2026-06-20T02:36:02.379592+00:00 | 1596_tau_lower | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1596-Y5-R2FR-tau-WEP-source-projection-or-action-measure-owner-last-gate.md | 1990 tau_WEP lower-bound or Hilbert-source signature gate | TCL1596_3_tau_null_escape;TSA1596_3_tau_min | True | True |  | EXISTS_NEEDLES_CONFIRMED |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | false | false | 2026-06-20T02:36:02.379592+00:00 | 1437_pwep_refusal | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1437-Y5-R10-RAB-P-WEP-first-row-or-source-input-acquisition-ledger.md | 1990 tau_WEP lower-bound or Hilbert-source signature gate | PWA1437_0_first_row;REFUSED_FIRST_ROW_MISSING_INPUTS | True | True |  | EXISTS_NEEDLES_CONFIRMED |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | false | false | 2026-06-20T02:36:02.379592+00:00 | 1936_hilbert | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1936-Y5-R2FR-source-weight-universality-theorem-or-TiPt-material-charge-ledger.md | 1990 tau_WEP lower-bound or Hilbert-source signature gate | UNIV1936_1_hilbert_source_theorem;UNIVERSALITY_NOT_DERIVED | True | True |  | EXISTS_NEEDLES_CONFIRMED |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | false | false | 2026-06-20T02:36:02.379592+00:00 | 1988_hilbert | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1988-Y5-R2FR-action-weight-source-beta-theorem-or-finite-row-fill.md | 1990 tau_WEP lower-bound or Hilbert-source signature gate | THM1988_0_parent_form;THEOREM_NOT_CLOSED_CURRENT_CORPUS | True | True |  | EXISTS_NEEDLES_CONFIRMED |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | false | false | 2026-06-20T02:36:02.379592+00:00 | 1935_eta | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1935-Y5-R2FR-MTS-WEP-eta-projection-map-or-material-charge-ledger.md | 1990 tau_WEP lower-bound or Hilbert-source signature gate | ETA1935_4_mts_source_weight_form;CON1935_3_transfer_factor | True | True |  | EXISTS_NEEDLES_CONFIRMED |

## Tau Lower-Bound Theorem Attempt

| branch_id | valid_for_claim | claim_allowed | generated_utc | attempt_id | statement | formula | result | claim_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | false | false | 2026-06-20T02:36:02.379592+00:00 | TAU1990_0_functional_shape | tau_WEP is a dimensionless source-worldtube/orbit/readout/material functional, not a convention-free unity factor. | tau_WEP = N_eta^{-1}<K_eta[e_obs,orbit,masks] · Integral_Earth K_source(x;orbit) R_source(x) dV · R_material(TiPt)>_orbit | SYMBOLIC_FUNCTIONAL_CONFIRMED | NONCLAIM |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | false | false | 2026-06-20T02:36:02.379592+00:00 | TAU1990_1_upper_bound_easy | norm data can give an upper envelope on |tau_WEP| | |tau| <= |N_eta|^{-1} ||K_eta|| ||K_source R_source|| ||R_material|| | UPPER_BOUND_SHAPE_ONLY | NOT_ENOUGH_FOR_DELTAW_BOUND |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | false | false | 2026-06-20T02:36:02.379592+00:00 | TAU1990_2_lower_bound_hard | a lower bound needs nonzero aligned projection, not merely nonzero ingredients | |tau_WEP| >= tau_min>0 requires sign/alignment/coercivity or official arrays proving nonzero orbit-readout projection | LOWER_BOUND_NOT_DERIVED | CURRENT_CORPUS_HAS_NO_TAU_MIN |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | false | false | 2026-06-20T02:36:02.379592+00:00 | TAU1990_3_current_verdict | Does current MTS derive |P_WEP|>=P_min>0 or |tau_WEP|>=tau_min>0? | P_WEP=tau_WEP*S_Earth; need |tau_WEP*S_Earth|>=P_min | FAIL_CURRENT_PROOF | P_MIN_NOT_DERIVED_OR_SOURCED |

## Tau Nonzero No-Go Ledger

| branch_id | valid_for_claim | claim_allowed | generated_utc | no_go_id | premise | counterexample | consequence | lesson |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | false | false | 2026-06-20T02:36:02.379592+00:00 | NG1990_0_orthogonality | K_eta and source/material response are each nonzero | choose K_eta orthogonal to the source/material response over the orbit average | tau_WEP=0 even though every named factor is nonzero | nonzero factors do not imply nonzero projected transfer |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | false | false | 2026-06-20T02:36:02.379592+00:00 | NG1990_1_mask_cancellation | source response has positive and negative orbit segments or readout masks | equal weighted positive/negative segments cancel in the reported eta channel | tau_WEP can vanish by averaging without a source-weight theorem | official readout/orbit convention is required for any lower bound |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | false | false | 2026-06-20T02:36:02.379592+00:00 | NG1990_2_common_mode | source coupling is universal/common but not composition-differential | common response enters SigmaW or measured calibration but not DeltaW_TiPt | P_WEP for the differential channel can be zero while common source response exists | measured-G/common-mode strength is not a WEP differential lower bound |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | false | false | 2026-06-20T02:36:02.379592+00:00 | NG1990_3_normalization | symbolic tau functional exists | without N_eta/product convention, rescale tau and DeltaW inversely | tau_min is convention-dependent unless normalization is fixed | tau_WEP=1 is a forbidden gauge choice, not a derivation |

## Nondegeneracy Certificate Contract

| branch_id | valid_for_claim | claim_allowed | generated_utc | cert_id | required_clause | acceptance | current_status | if_missing |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | false | false | 2026-06-20T02:36:02.379592+00:00 | CERT1990_0_official_readout | official or exactly equivalent MICROSCOPE readout/orbit kernel K_eta | source path, units, masks, body order, sensitive-axis sign, and reproducible extraction | OFFICIAL_ARRAYS_NOT_IMPORTED | no tau numeric value or tau_min |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | false | false | 2026-06-20T02:36:02.379592+00:00 | CERT1990_1_source_worldtube | Earth/source worldtube vector in same parent basis | finite-size/source profile, orbit weighting, basis convention, and uncertainty/source path | MISSING_SOURCE_PROFILE_WEIGHTING | source side of P_WEP is not evaluable |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | false | false | 2026-06-20T02:36:02.379592+00:00 | CERT1990_2_material_tensor | TA6V-minus-PtRh10 material response tensor in same basis | composition/model/source path and no double-counting rule | MATERIAL_PAIR_ONLY_OR_PARTIAL_SMOKE | DeltaW_TiPt cannot be linked to the readout product |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | false | false | 2026-06-20T02:36:02.379592+00:00 | CERT1990_3_alignment_floor | nonzero aligned projection certificate | explicit positive floor I_min for the orbit/readout/source/material inner product, or theorem ruling out orthogonality | MISSING_ALIGNMENT_COERCIVITY | tau_WEP may vanish by orthogonality/cancellation |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | false | false | 2026-06-20T02:36:02.379592+00:00 | CERT1990_4_normalization_floor | eta product normalization N_eta and bounded convention | N_eta nonzero with source path and sign/units convention | NORMALIZATION_NOT_FILLED | tau_min is convention-dependent |

## U Denominator Envelope Contract

| branch_id | valid_for_claim | claim_allowed | generated_utc | u_id | quantity | needed_for | current_status | required_input |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | false | false | 2026-06-20T02:36:02.379592+00:00 | U1990_0_definition | U=P_WEP*SigmaW_TiPt | denominator control in eta=2D/(2+U) | SYMBOL_DEFINED_VALUES_MISSING | P_WEP envelope and SigmaW_TiPt envelope or theorem U=0 |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | false | false | 2026-06-20T02:36:02.379592+00:00 | U1990_1_zero_route | U | linear product bound with u_max=0 | CONDITIONAL_ONLY | parent Hilbert source universality or common-mode cancellation theorem |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | false | false | 2026-06-20T02:36:02.379592+00:00 | U1990_2_finite_route | u_max | |D| <= eta_bound_abs*(1+u_max/2) | MISSING_U_MAX | upper bounds for |P_WEP| and |SigmaW_TiPt| in same convention |

## Hilbert Source Signature Gate

| branch_id | valid_for_claim | claim_allowed | generated_utc | route_id | target | if_success | current_status | remaining_gap |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | false | false | 2026-06-20T02:36:02.379592+00:00 | HIL1990_0_strong_route | parent-signed universal Hilbert source coupling | DeltaW_TiPt=0 and beta_w=0, so WEP source-weight residual vanishes without tau_min | CONDITIONAL_THEOREM_EXACT_PARENT_UNSIGNED | no-source-weight object-language clause, common measure/current owner, and readout preservation |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | false | false | 2026-06-20T02:36:02.379592+00:00 | HIL1990_1_finite_route | tau/P nondegeneracy and denominator finite envelopes | finite nonclaim WEP product comparison becomes scoreable | SOURCE_READOUT_NONDEGENERACY_MISSING | official MICROSCOPE/readout/source/material/sign rows and alignment floor |

## Runner Dryrun

| branch_id | valid_for_claim | claim_allowed | generated_utc | run_id | check | result | reason |
| --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | false | false | 2026-06-20T02:36:02.379592+00:00 | RUN1990_0_tau_functional | tau_WEP functional shape | PASS_SYMBOLIC | 1225 formula gives the source-worldtube/orbit/readout/material functional shape |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | false | false | 2026-06-20T02:36:02.379592+00:00 | RUN1990_1_tau_lower_bound | derive tau_min>0 from current corpus | FAIL_ORTHOGONALITY_COUNTEREXAMPLE | nonzero factors can project to zero without an alignment/coercivity certificate |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | false | false | 2026-06-20T02:36:02.379592+00:00 | RUN1990_2_u_envelope | derive u_max for denominator control | FAIL_VALUES_MISSING | P_WEP and SigmaW_TiPt envelopes are not sourced/derived |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | false | false | 2026-06-20T02:36:02.379592+00:00 | RUN1990_3_hilbert_signature | close DeltaW_TiPt=0 by parent Hilbert source signature | FAIL_PARENT_SIGNATURE_UNSIGNED | conditional theorem exists but parent object language still permits countermodels unless signed |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | false | false | 2026-06-20T02:36:02.379592+00:00 | RUN1990_4_verdict | 1990 tau/Hilbert fork | TAU_LOWER_BOUND_NOT_DERIVED_CERTIFICATE_CONTRACT_WRITTEN | progress is the exact nondegeneracy certificate contract, not a WEP/local-GR score |

## Claim Gate

| branch_id | valid_for_claim | claim_allowed | generated_utc | gate_id | claim | status | reason |
| --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | false | false | 2026-06-20T02:36:02.379592+00:00 | CG1990_0_symbolic_tau | tau_WEP functional shape is defined | PASS_NONCLAIM_SYMBOLIC | functional shape is inherited from 1225 and kept nonclaim |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | false | false | 2026-06-20T02:36:02.379592+00:00 | CG1990_1_tau_min | |tau_WEP|>=tau_min>0 | FAIL_BLOCKED | no alignment/coercivity/readout certificate; orthogonality counterexample survives |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | false | false | 2026-06-20T02:36:02.379592+00:00 | CG1990_2_P_min | |P_WEP|>=P_min>0 | FAIL_BLOCKED | tau_min and source-environment floor missing |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | false | false | 2026-06-20T02:36:02.379592+00:00 | CG1990_3_u_max | denominator envelope u_max is known | FAIL_BLOCKED | P_WEP and SigmaW_TiPt envelopes missing |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | false | false | 2026-06-20T02:36:02.379592+00:00 | CG1990_4_hilbert_zero | DeltaW_TiPt=0 parent-signed | FAIL_BLOCKED | Hilbert source route remains conditional |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | false | false | 2026-06-20T02:36:02.379592+00:00 | CG1990_5_local_GR_Newton | local GR/Newton source universality derived | FAIL_BLOCKED | neither tau finite route nor Hilbert zero route is closed |

## Decision Ledger

| branch_id | valid_for_claim | claim_allowed | generated_utc | decision_id | decision | because | next_action |
| --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | false | false | 2026-06-20T02:36:02.379592+00:00 | DEC1990_0_tau_result | TAU_MIN_NOT_DERIVED | tau_WEP is an inner-product/readout functional; current corpus lacks the alignment certificate needed to rule out zero projection | build nondegeneracy certificate or source official readout arrays |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | false | false | 2026-06-20T02:36:02.379592+00:00 | DEC1990_1_hilbert_status | HILBERT_ZERO_ROUTE_REMAINS_BEST_CLEAN_GR_ROUTE | if universal Hilbert source coupling is parent-signed, DeltaW_TiPt=0 and tau_min becomes unnecessary for WEP zero | try to close source-signature/readout-preservation theorem in parallel with finite data route |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | false | false | 2026-06-20T02:36:02.379592+00:00 | DEC1990_2_best_next | NONDEGENERACY_CERTIFICATE_OR_HILBERT_OWNER_NEXT | the finite route needs official readout/source/material alignment; the derivation route needs no-source-weight parent ownership | 1991-Y5-R2FR-WEP-nondegeneracy-certificate-or-parent-Hilbert-owner.md |

## Next Target

| branch_id | valid_for_claim | claim_allowed | generated_utc | next_id | selection_status | target_doc | target_script | task | success_condition | do_not |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428 | false | false | 2026-06-20T02:36:02.379592+00:00 | NEXT1990_0_primary | selected | 1991-Y5-R2FR-WEP-nondegeneracy-certificate-or-parent-Hilbert-owner.md | scripts/Y5_R2FR_WEP_nondegeneracy_certificate_or_parent_Hilbert_owner_1991.py | either construct a nonzero WEP projection certificate from readout/source/material alignment, or close the parent Hilbert source owner/no-species-weight theorem | tau/P lower-bound certificate with source paths, or parent-signed DeltaW_TiPt=0; otherwise retain finite nonclaim route | do not set tau_WEP=1, use nonzero factors as nonzero projection, assume U=0, invent material/source rows, claim WEP/local-GR pass, or modify formalization-workbench |

## Validation

| validation_id | status | detail | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- |
| VAL1990_00_sources | PASS | all source paths exist and needles found | false | false |
| VAL1990_01_tau_attempt | PASS | tau functional retained; lower bound not promoted | false | false |
| VAL1990_02_no_go | PASS | orthogonality/cancellation no-go recorded | false | false |
| VAL1990_03_certificate_contract | PASS | alignment/coercivity certificate required | false | false |
| VAL1990_04_u_envelope | PASS | U denominator envelope remains explicit and missing | false | false |
| VAL1990_05_runner_blocks | PASS | runner blocks tau-min and Hilbert-zero claims | false | false |
| VAL1990_06_claim_gates | PASS | claim gates safe; symbolic tau only | false | false |
| VAL1990_07_next_target | PASS | 1991 nondegeneracy/Hilbert owner target selected | false | false |
| VAL1990_08_claim_flags_safe | PASS | claim flags all false | false | false |
| VAL1990_09_csv_parse | PASS | all generated CSVs parse with rows | false | false |
| VAL1990_10_pycache_absent | PASS | scripts __pycache__ absent | false | false |
| VAL1990_11_formalization_untouched | PASS | formalization_1990_artifact_count=0 | false | false |
| VAL1990_OVERALL | PASS | 1990 tau WEP lower-bound or Hilbert source signature gate | false | false |
