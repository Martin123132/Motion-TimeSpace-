# 1601 - R2/fR EP-Template Alignment Lemma Or CMSM Browser Capture

## Verdict
- 1601 derives the conditional EP-template alignment lemma: if `|C_EP| ||K_EP|| ||T_EP|| > |<K_EP,V_corr>|`, then the MICROSCOPE EP-template projection is nonzero.
- The lemma is not claimable: `C_EP`, official template norm, and correction bound are not parent-signed or sourced.
- Three countermodels remain live: common-mode-only response, quadrature/orthogonal phase, and correction/window cancellation.
- The smallest next theoretical object is now `C_EP`, the parent EP-template source coefficient.
- No WEP, local-GR, Newton, PPN, R10, clock, orbital, beta/coupling, or public claim is made.

## Source Register

| source_id | source_path | exists | needle_found | needles |
| --- | --- | --- | --- | --- |
| SRC1601_0_1600_doc | 1600-Y5-R2FR-MICROSCOPE-HAR-intake-or-parent-K-vector-proof.md | True | True | NEXT_1601_EP_TEMPLATE_ALIGNMENT_LEMMA_OR_CMSM_BROWSER_CAPTURE; EP-template alignment |
| SRC1601_1_1600_validation | source-intake/mts_residuals/P8_Y5_BRR545_1600_VALIDATION.csv | True | True | VAL1600_OVERALL; PASS |
| SRC1601_2_1600_K_proof | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1600_PARENT_K_VECTOR_PROOF_ATTEMPT.csv | True | True | KVP1600_1_EP_template_alignment; NO_EP_TEMPLATE_ALIGNMENT_PROOF |
| SRC1601_3_1600_K_components | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1600_K_COMPONENT_CONTRACT.csv | True | True | KCC1600_0_K_EP; SYMBOLIC_ONLY_NO_ARRAYS |
| SRC1601_4_1600_alignment | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1600_ALIGNMENT_GATE.csv | True | True | ALG1600_2_combined_verdict; ALIGNMENT_REMAINS_MISSING |
| SRC1601_5_1600_next | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1600_NEXT_TARGET.csv | True | True | 1601-Y5-R2FR-EP-template-alignment-lemma-or-CMSM-browser-capture; EP-template alignment |
| SRC1601_6_1599_symbolic_k | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1599_SYMBOLIC_K_BRIDGE.csv | True | True | SKB1599_0_EP_signal_template; K_EP_gravity_dot_V_MTS_source_material |
| SRC1601_7_1599_filelist | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1599_CMSM_PARSED_FILELIST_CANDIDATE.csv | True | True | PFL1599_0_no_filelist_rows; NO_PARSEABLE_OFFICIAL_FILELIST |
| SRC1601_8_1598_kernel | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1598_MEASUREMENT_KERNEL_STATUS.csv | True | True | MKS1598_0_published_measurement_equation; SYMBOLIC_KERNEL_STRUCTURE_AVAILABLE |

## EP-Template Alignment Lemma

| lemma_id | statement | condition | status | result |
| --- | --- | --- | --- | --- |
| EPA1601_0_decomposition | decompose the branch source-material readout vector as V_MTS = C_EP T_EP + V_perp + V_corr | T_EP is the MICROSCOPE Earth-gravity EP template; <K_EP,V_perp>=0 by definition; V_corr contains corrections/windowing errors | CONDITIONAL_DECOMPOSITION_DEFINED | PROOF_REDUCED_TO_C_EP_AND_CORRECTION_BOUND |
| EPA1601_1_alignment_condition | if |C_EP| ||K_EP|| ||T_EP|| > |<K_EP,V_corr>| then <K_EP,V_MTS> != 0 | requires nonzero C_EP, nonzero template norm, and signed/absolute bound on correction projection | CONDITIONAL_ALIGNMENT_LEMMA_DERIVED | EP_ALIGNMENT_SUFFICIENT_CONDITION |
| EPA1601_2_parent_source_coefficient | C_EP must be supplied by parent MTS source coupling, not fitted from the MICROSCOPE bound | parent action/source map gives nonzero differential source coefficient in the observed Earth-gravity EP channel | MISSING_PARENT_C_EP | NO_PARENT_SIGNED_EP_COMPONENT |
| EPA1601_3_verdict | the EP-template alignment lemma is derived conditionally but not closed by current corpus evidence | C_EP and correction bound remain unsourced; CMSM browser/HAR evidence absent | EP_TEMPLATE_ALIGNMENT_NOT_PROVEN | LEMMA_ROUTE_BLOCKED_NONCLAIM |

## EP-Template Countermodels

| countermodel_id | construction | math_result | blocked_claim | escape_condition |
| --- | --- | --- | --- | --- |
| EPC1601_0_common_mode_only | parent source response shifts only the common-mode/gravitational normalization and leaves no differential EP-template component | C_EP=0 while a source response exists | source response implies EP-template alignment | derive nonzero differential source coefficient before measured-G/common-mode absorption |
| EPC1601_1_quadrature_phase | MTS residual is in a quadrature/orthogonal orbital phase relative to the EP template | <K_EP,V_MTS>=0 despite nonzero residual norm | nonzero residual norm implies MICROSCOPE EP-channel projection | source parent phase/observed coframe theorem or official template projection |
| EPC1601_2_correction_cancellation | correction/window terms cancel the EP-template projection within the observed channel | C_EP template projection can be canceled without a signed correction bound | symbolic EP template alone proves nonzero readout | official CMSM correction arrays or parent no-cancellation theorem |

## Alignment Amplitude Contract

| contract_id | quantity | needed_form | current_status | why_needed |
| --- | --- | --- | --- | --- |
| EAC1601_0_C_EP | C_EP | nonzero parent source coefficient for the MICROSCOPE EP-template channel | MISSING_PARENT_C_EP | sets the leading alignment amplitude |
| EAC1601_1_template_norm | ||K_EP|| ||T_EP|| | positive sourced norm from official template/readout arrays or exact symbolic normalization | MISSING_NUMERIC_TEMPLATE_NORM | turns nonzero C_EP into lower bound |
| EAC1601_2_correction_bound | |<K_EP,V_corr>| | upper bound from official corrections/windowing or parent theorem | MISSING_CORRECTION_BOUND | prevents correction cancellation |
| EAC1601_3_alignment_margin | M_EP = |C_EP| ||K_EP|| ||T_EP|| - |<K_EP,V_corr>| | strictly positive margin | NOT_EVALUATED | M_EP>0 proves EP-template alignment |

## CMSM Browser Capture Status

| capture_id | route | current_status | filelist_acquired | claim_impact |
| --- | --- | --- | --- | --- |
| CAP1601_0_CMSM_input_folder | source-intake/microscope/quarantine/1599/input | NO_INPUT_FILES_PRESENT | False | rerun 1599 parser if input appears; current 1601 uses theory route only |
| CAP1601_1_browser_capture_route | CMSM browser/HAR capture | AVAILABLE_AS_FALLBACK_NOT_EXECUTED | False | data route remains parked until authenticated evidence is available |

## Runner Refusal

| runner_id | acceptance_rule | input_state | runner_result | effect |
| --- | --- | --- | --- | --- |
| RUN1601_0_conditional_lemma | record conditional EP-template alignment lemma | mathematical inequality derived; C_EP/corrections unsourced | ACCEPT_CONDITIONAL_LEMMA_ONLY | proof target sharpened |
| RUN1601_1_proof_claim | parent-signed C_EP and correction bound required | C_EP missing; correction bound missing | REJECT_EP_ALIGNMENT_CLAIM | no tau_min or WEP score |
| RUN1601_2_CMSM_capture | reviewed HAR/filelist evidence required | no input files present | NO_CMSM_CAPTURE_INGESTED | data route remains fallback |

## Claim Gates

| gate_id | claim | status | reason |
| --- | --- | --- | --- |
| CG1601_0_EP_alignment | EP-template alignment proven | BLOCKED | C_EP and correction bound are missing |
| CG1601_1_tau | tau_WEP lower bound exists | BLOCKED | EP alignment margin not positive/sourced |
| CG1601_2_CMSM | CMSM browser/HAR evidence ingested | BLOCKED | no input files present |
| CG1601_3_WEP | MTS passes MICROSCOPE/WEP | BLOCKED | product anchor only |
| CG1601_4_local_GR | derived local GR branch | BLOCKED | readout/coupling residual remains open |

## Decision

| decision_id | decision | reason | next_action |
| --- | --- | --- | --- |
| DEC1601_0_progress | CONDITIONAL_EP_ALIGNMENT_LEMMA_DERIVED | the proof now reduces to a nonzero parent EP coefficient and a correction-cancellation bound | hunt C_EP in parent source/matter action |
| DEC1601_1_blocker | EP_TEMPLATE_ALIGNMENT_NOT_PROVEN | common-mode-only, quadrature, and correction-cancellation countermodels remain live | try C_EP source-coefficient theorem or use CMSM data route |
| DEC1601_2_next | NEXT_1602_CEP_SOURCE_COEFFICIENT_OR_COMMON_MODE_ZERO_THEOREM | C_EP is now the smallest unsourced theoretical object | derive nonzero C_EP from parent source coupling or prove source response is common-mode zero for WEP |

## Next Target

| next_target | script | objective | success_condition | do_not |
| --- | --- | --- | --- | --- |
| 1602-Y5-R2FR-C_EP-source-coefficient-or-common-mode-zero-theorem.md | scripts/Y5_R2FR_C_EP_source_coefficient_or_common_mode_zero_theorem.py | derive a parent-signed nonzero EP-template source coefficient C_EP, or prove the finite branch is purely common-mode/zero in WEP | C_EP source coefficient with sign/units and correction contract, or theorem that WEP finite branch is common-mode only and cannot violate WEP | do not fit C_EP from the MICROSCOPE bound, do not claim WEP/local GR, do not use tau_WEP=1 |

## Validation

| check_id | result | detail |
| --- | --- | --- |
| VAL1601_0_sources_exist | PASS | all cited 1601 local source paths exist |
| VAL1601_1_needles_found | PASS | all required 1601 source needles found |
| VAL1601_2_conditional_lemma | PASS | conditional EP-template alignment lemma recorded |
| VAL1601_3_lemma_not_claimed | PASS | EP-template alignment remains unproven |
| VAL1601_4_countermodels | PASS | countermodels recorded |
| VAL1601_5_CEP_contract | PASS | C_EP source coefficient contract recorded |
| VAL1601_6_capture_status | PASS | CMSM capture fallback status recorded |
| VAL1601_7_runner_rejects_claim | PASS | runner rejects EP alignment claim |
| VAL1601_8_claim_gates_closed | PASS | all 1601 claim gates remain closed |
| VAL1601_9_decision_next | PASS | decision selects 1602 C_EP source coefficient or common-mode zero theorem |
| VAL1601_10_csv_parse | PASS | all generated 1601 CSVs parse |
| VAL1601_11_claim_safety_flags | PASS | no generated 1601 rows are score-ready, prediction rows, or claim-allowed |
| VAL1601_12_branch_copies | PASS | branch/quarantine nonclaim copies exist |
| VAL1601_13_pycache_absent | PASS | scripts __pycache__ absent |
| VAL1601_14_formalization_untouched | PASS | no 1601 outputs found under formalization-workbench |
| VAL1601_OVERALL | PASS | 1601 EP-template alignment lemma or CMSM capture validation |
