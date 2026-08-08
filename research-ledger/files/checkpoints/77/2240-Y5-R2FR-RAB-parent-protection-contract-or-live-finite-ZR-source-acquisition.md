# 2240 - Y5/R2FR R_AB Parent Protection Contract or Live Finite Z_R Source Acquisition

## Verdict
- 2240 imports the old `1567` parent-protection/source-acquisition checkpoint into the current R2FR chain after `2239` installed the hard finite-residual validator.
- The single parent-protection contract is now explicit: typed parent sorts, action-image exhaustion, matter descent, boundary descent, readout closure, and operator exclusion must close together.
- If that contract is parent-signed, the second-class route kills `J_R`, `B_R`, `readout_regen`, and `Z_R` without a plateau axiom.
- It is not signed from MTS primitives yet, so no `Z_R=0`, `q_R=0`, local GR/Newton, R10, PPN, WEP, clock, or orbital claim is made.
- The fallback is live but nonclaim: internal coefficient targets are separated from external arena-bound sources, with no raw/accepted score row ready.

## Source Register
| source_id | source_path | path_exists | validation_overall_pass | role |
| --- | --- | --- | --- | --- |
| SRC2240_0_2239_doc | 2239-Y5-R2FR-RAB-source-boundary-readout-protection-or-finite-ZR-validator.md | True |  | current R2FR protection validator handoff |
| SRC2240_1_2239_validation | source-intake/mts_residuals/P8_Y5_BRR545_2239_VALIDATION.csv | True | True | current R2FR protection validator handoff |
| SRC2240_2_2239_decision | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2239_DECISION_LEDGER.csv | True |  | current R2FR protection validator handoff |
| SRC2240_3_2239_protection | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2239_PROTECTION_PROOF_AUDIT.csv | True |  | current R2FR protection validator handoff |
| SRC2240_4_2239_joint | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2239_JB_READOUT_OPERATOR_JOINT_GATE.csv | True |  | current R2FR protection validator handoff |
| SRC2240_5_2239_validator | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2239_FINITE_ZR_VALIDATOR_SUMMARY.csv | True |  | current R2FR protection validator handoff |
| SRC2240_6_1567_doc | 1567-Y5-RAB-parent-protection-contract-or-live-finite-ZR-source-acquisition.md | True |  | older parent-contract/source-acquisition evidence |
| SRC2240_7_1567_validation | source-intake/mts_residuals/P8_Y5_BRR545_1567_VALIDATION.csv | True | True | older parent-contract/source-acquisition evidence |
| SRC2240_8_1567_source | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1567_SOURCE_REGISTER.csv | True |  | older parent-contract/source-acquisition evidence |
| SRC2240_9_1567_web | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1567_WEB_SOURCE_REGISTER.csv | True |  | older parent-contract/source-acquisition evidence |
| SRC2240_10_1567_contract | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1567_PARENT_PROTECTION_CONTRACT.csv | True |  | older parent-contract/source-acquisition evidence |
| SRC2240_11_1567_audit | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1567_CONTRACT_PROOF_AUDIT.csv | True |  | older parent-contract/source-acquisition evidence |
| SRC2240_12_1567_theorem | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1567_CONDITIONAL_THEOREM.csv | True |  | older parent-contract/source-acquisition evidence |
| SRC2240_13_1567_acquisition | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1567_LIVE_SOURCE_ACQUISITION_QUEUE.csv | True |  | older parent-contract/source-acquisition evidence |
| SRC2240_14_1567_runner | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1567_RUNNER_NONCLAIM.csv | True |  | older parent-contract/source-acquisition evidence |
| SRC2240_15_1567_claim | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1567_CLAIM_GATE.csv | True |  | older parent-contract/source-acquisition evidence |
| SRC2240_16_1567_decision | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1567_DECISION.csv | True |  | older parent-contract/source-acquisition evidence |
| SRC2240_17_1567_next | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1567_NEXT_TARGET.csv | True |  | older parent-contract/source-acquisition evidence |

## External Arena Source Queue
| source_id | arena | url | description | use_for | local_copy_path | row_status |
| --- | --- | --- | --- | --- | --- | --- |
| WEB2240_R10_EOTWASH_PRL_2021 | R10 | https://link.aps.org/doi/10.1103/PhysRevLett.126.211101 | Combined short-range inverse-square-law/Yukawa alpha(lambda) bound source for 5-500 mm. | external alpha(lambda) bound acquisition only; not an MTS coefficient source | NOT_DOWNLOADED_THIS_CHECKPOINT | EXTERNAL_ARENA_SOURCE_CANDIDATE_NONCLAIM |
| WEB2240_PPN_WILL_LRR_2014 | PPN | https://link.springer.com/article/10.12942/lrr-2014-4 | Living Reviews PPN/solar-system test framework source. | external PPN residual comparator conventions only | NOT_DOWNLOADED_THIS_CHECKPOINT | EXTERNAL_ARENA_SOURCE_CANDIDATE_NONCLAIM |
| WEB2240_WEP_MICROSCOPE_PRL_2022 | WEP | https://link.aps.org/doi/10.1103/PhysRevLett.129.121102 | MICROSCOPE final equivalence-principle result. | external WEP/source-composition residual bound only | NOT_DOWNLOADED_THIS_CHECKPOINT | EXTERNAL_ARENA_SOURCE_CANDIDATE_NONCLAIM |
| WEB2240_CLOCK_NATURE_2023 | clock | https://www.nature.com/articles/s41467-023-40629-8 | Laboratory gravitational-redshift/clock-gradient test source. | external clock/readout residual bound only | NOT_DOWNLOADED_THIS_CHECKPOINT | EXTERNAL_ARENA_SOURCE_CANDIDATE_NONCLAIM |

## Parent Protection Contract
| contract_id | contract_clause | effect_if_signed | current_status | missing_for_claim |
| --- | --- | --- | --- | --- |
| CON2240_0_parent_sorts | Parent fields are typed into public quotient observables Q, auxiliary compatibility variables A_R=(R_AB,Lambda_R), matter/readout fields Psi, fixed markers theta, and boundary data B. | R_AB cannot be simultaneously a physical scalar and an auxiliary compatibility coordinate. | SCHEMA_VALID_NOT_PARENT_DERIVED | derive the typed field list from MTS primitives, not from the local failure mode |
| CON2240_1_action_image | S_parent belongs to Image(ParentGenerate[Q,theta,top,Psi]) plus algebraic Lambda_R(R_AB-C_AB[Q,theta,top]). | No direct R_AB matter source, no independent R_AB kinetic term, and no R_AB boundary functional are generated. | SCHEMA_VALID_NOT_PARENT_DERIVED | prove ParentGenerate exhaustion and no extension markers |
| CON2240_2_matter_functor | S_matter descends through Q and Psi only: delta S_matter/delta R_AB=0. | Kills J_R in E_R. | UNSIGNED_MATTER_DESCENT | prove no material constants, EM labels, clocks, masses, or hidden markers depend on R_AB |
| CON2240_3_boundary_functor | Boundary/corner terms descend through Q-boundary data only: delta B/delta R_AB=0 and Q_R=0. | Kills B_R/Pi_Rn leakage. | UNSIGNED_BOUNDARY_SILENCE | prove source-worldtube and corner terms cannot carry R_AB hair |
| CON2240_4_readout_closure | Readout/effective reduction preserves Image(ParentGenerate) and cannot generate R_AB derivative or transfer operators. | Kills readout_regen and tau leakage. | UNSIGNED_READOUT_STABILITY | prove radiative/readout closure rather than assume tree-level silence survives |
| CON2240_5_operator_exclusion | No D R_AB, D Lambda_R, G_vert, nabla_vert, or Sobolev norm constructor exists for A_R. | Kills Z_R and M_R^2 derivative residuals at parent level. | BLOCKED_EXACT_CONDITIONAL | 1236/1269 provide certificate shape but not primitive derivation |
| CON2240_6_joint_contract | CON2240_0 through CON2240_5 are a single indivisible protection contract. | If all parent-signed, then J_R=B_R=readout_regen=Z_R=0 and the second-class route closes. | CONTRACT_WRITTEN_NOT_SIGNED | current corpus lacks one parent-owned theorem binding all clauses |

## Contract Proof Audit
| audit_id | target_zero | required_contract_clause | current_status | fallback |
| --- | --- | --- | --- | --- |
| AUD2240_0_JR | J_R=0 | CON2240_2_matter_functor | UNSIGNED | finite J_R row remains required if not derived |
| AUD2240_1_BR | B_R=Pi_Rn=0 | CON2240_3_boundary_functor | UNSIGNED | finite boundary row remains required if not derived |
| AUD2240_2_readout | readout_regen=tau_residual=0 | CON2240_4_readout_closure | UNSIGNED | finite tau rows remain required if not derived |
| AUD2240_3_ZR | Z_R=0 and no derivative R_AB residual | CON2240_5_operator_exclusion | BLOCKED_EXACT_CONDITIONAL | finite Z_R/M_R2 rows remain required if not derived |
| AUD2240_4_joint | local second-class protection package | CON2240_0 through CON2240_5 | FAILED_CURRENT_PARENT_PROOF | cannot spend local-GR credit from separate unsigned clauses |

## Conditional Theorem
| theorem_id | statement | calculation_or_role | status | why_not_claimed |
| --- | --- | --- | --- | --- |
| THM2240_0_statement | If the parent protection contract CON2240_0-5 is parent-signed, then the R_AB sector is algebraically eliminated before readout with J_R=B_R=readout_regen=Z_R=0. | conditional theorem | EXACT_IF_CONTRACT_PARENT_SIGNED | not a claim because the contract is not derived from MTS primitives |
| THM2240_1_variation | E_Lambda: R_AB=C_AB[Q,theta,top]; E_R: Lambda_R + J_R + delta B/delta R_AB + readout_regen = 0. | with J_R=B_R=readout_regen=0, Lambda_R=0 | FORMAL_PASS_WITHIN_CONTRACT | requires all source/boundary/readout clauses together |
| THM2240_2_operator | ParentGenerate has no R_AB derivative constructor, so Z_R \|D R_AB\|^2 is not in the parent image. | operator is syntactically excluded | EXACT_IF_TYPED_GRAMMAR_PARENT_SIGNED | 1236/1269 are schema-valid but not parent-derived |
| THM2240_3_verdict | The theorem is a useful target, not an achieved local-GR reduction. | current branch remains conditional/fallback | NOT_CLAIMABLE | needs parent proof or finite source rows |

## Live Source Acquisition Queue
| acquisition_id | source_class | target | needed_evidence | preferred_source_kind | arena_projection | current_status | ready_for_raw | ready_for_accepted |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ACQ2240_0_parent_contract | internal_theory | parent_protection_contract | derive typed ParentGenerate grammar from MTS primitives so CON2240_0-5 are not post-hoc closure rules | MTS parent action / primitive object-language derivation | all | MISSING_PARENT_PROTECTION_DERIVATION | False | False |
| ACQ2240_1_ZR | internal_theory | Z_R | theorem-zero from operator exclusion or finite coefficient with units and normalization | MTS parent action second variation/operator grammar | R10;PPN;clock;orbital | MISSING_ZR_THEOREM_OR_COEFFICIENT | False | False |
| ACQ2240_2_MR2 | internal_theory | M_R^2 | mass-gap/Hessian or range scale tied to same R_AB normalization | MTS parent Hessian or sourced residual model | R10;PPN;clock;orbital | MISSING_MR2_SOURCE | False | False |
| ACQ2240_3_JR | internal_theory | J_R | matter-source zero theorem or finite source coupling | MTS matter descent proof or explicit source-current derivation | WEP;R10;PPN;clock | MISSING_JR_SOURCE_OR_ZERO | False | False |
| ACQ2240_4_BR | internal_theory | B_R_or_Pi_Rn | boundary/corner zero theorem or finite boundary momentum bound | MTS boundary variational grammar | R10;PPN;orbital | MISSING_BR_SOURCE_OR_ZERO | False | False |
| ACQ2240_5_tau_R10 | mixed_internal_external | tau_R10 | projection from finite R_AB residual to alpha(lambda), paired with external R10 bound source | internal kernel plus Eot-Wash/short-range alpha(lambda) source | R10 | MISSING_TAU_R10_PROJECTION | False | False |
| ACQ2240_6_tau_PPN | mixed_internal_external | tau_PPN | projection from finite R_AB residual to gamma/beta residual vector | internal metric projection plus PPN convention source | PPN | MISSING_TAU_PPN_PROJECTION | False | False |
| ACQ2240_7_tau_clock | mixed_internal_external | tau_clock | projection from finite R_AB residual to fractional clock/readout observable | internal readout map plus clock/redshift source | clock | MISSING_TAU_CLOCK_PROJECTION | False | False |
| ACQ2240_8_tau_orbital | mixed_internal_external | tau_orbital | projection from finite R_AB residual to acceleration/timing observable | internal force map plus orbital/PPN source | orbital | MISSING_TAU_ORBITAL_PROJECTION | False | False |

## Runner
| runner_id | test | current_status | detail |
| --- | --- | --- | --- |
| RUN2240_0_sources | load 1567 parent-protection evidence chain | PASS | 1566, 1565, 1236, 1265, 1268, 1269, and 1023 evidence loaded |
| RUN2240_1_contract | write single parent protection contract | PASS_CONTRACT_WRITTEN | contract clauses are precise and jointly sufficient if parent-signed |
| RUN2240_2_parent_signature | prove contract from MTS primitives | FAILED_CURRENT_PARENT_PROOF | typed object language, matter descent, boundary silence, readout closure, and operator exclusion remain unsigned |
| RUN2240_3_conditional_theorem | derive theorem under contract | PASS_EXACT_CONDITIONAL | if contract is signed then J_R=B_R=readout_regen=Z_R=0 |
| RUN2240_4_acquisition | start live finite residual acquisition | PASS_NONCLAIM_QUEUE_READY | internal coefficient targets and external arena sources are separated |
| RUN2240_5_raw_accepted | raw/accepted finite rows | NO_LIVE_SCORE_ROWS | raw_rows=0; accepted_rows=0 |
| RUN2240_6_claim | local GR/Newton claim | BLOCKED_NO_CLAIM | contract is not parent-signed and no finite residual row is source-ready |

## Claim Gate
| gate_id | claim_gate | status | reason |
| --- | --- | --- | --- |
| GATE2240_0_contract | parent protection contract | BLOCKED_NO_CLAIM | contract written but not derived from MTS primitives |
| GATE2240_1_JR_BR_readout_ZR | J_R=B_R=readout_regen=Z_R=0 | BLOCKED_NO_CLAIM | zero theorem is conditional on unsigned contract |
| GATE2240_2_finite_rows | finite residual source rows | BLOCKED_NO_CLAIM | only acquisition queue and blueprint exist; raw/accepted rows remain empty |
| GATE2240_3_external_bounds | external arena bounds | PASS_SOURCE_QUEUE_NONCLAIM | R10/PPN/WEP/clock source URLs queued, but not connected to MTS coefficients |
| GATE2240_4_local_GR | derived local GR/Newton/PPN safety | BLOCKED_NO_CLAIM | neither theorem-zero nor finite-residual route is claim-ready |

## Decision Ledger
| decision_id | decision | result | reason |
| --- | --- | --- | --- |
| DEC2240_0_contract | parent protection contract | CONTRACT_WRITTEN_NOT_PARENT_SIGNED | the contract is jointly sufficient but still a schema, not a derivation from motion/time/space primitives |
| DEC2240_1_theorem | conditional theorem | EXACT_IF_CONTRACT_SIGNED | if signed, the second-class route kills J_R, B_R, readout_regen, and Z_R together |
| DEC2240_2_acquisition | finite residual workflow | LIVE_ACQUISITION_QUEUE_STARTED_NONCLAIM | internal coefficient targets and external arena sources are now separated before raw/accepted intake |
| DEC2240_3_next | next target | NEXT_2241_PARENT_CONTRACT_DERIVATION_FROM_MTS_PRIMITIVES_OR_FIRST_LIVE_ZR_ROW | either derive the contract from primitives or fill the first source-backed finite row without scoring it |

## Next Target
| next_id | next_target | script | objective | do_not |
| --- | --- | --- | --- | --- |
| NEXT2240_0_1568 | 2241-Y5-R2FR-RAB-parent-contract-derivation-from-MTS-primitives-or-first-live-ZR-row.md | scripts/Y5_R2FR_RAB_parent_contract_derivation_from_MTS_primitives_or_first_live_ZR_row_2241.py | attempt to derive the typed parent protection contract from motion/time/space primitives; if not derivable, fill the first nonclaim source-backed finite row or explicit theorem-zero row using the 1567 acquisition queue | do not promote the contract schema to local-GR evidence; do not move rows to accepted until source path, anchor, units, normalization, and arena projection are real; do not edit formalization-workbench |

## Branch Copies
| copy_id | source_path | target_path | copied | parse_ok |
| --- | --- | --- | --- | --- |
| queue | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2240_LIVE_SOURCE_ACQUISITION_QUEUE.csv | source-intake/rab-sector/acquisition-queue/JR2240_PARENT_CONTRACT_OR_SOURCE_ACQ_NONCLAIM.csv | True | True |
| branch_wep | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2240_LIVE_SOURCE_ACQUISITION_QUEUE.csv | source-intake/microscope/branch_locked_wep/residuals/parent_contract_or_source_acq_nonclaim_2240.csv | True | True |
| beta_docs | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2240_LIVE_SOURCE_ACQUISITION_QUEUE.csv | source-intake/beta-source/docs/PARENT_CONTRACT_OR_SOURCE_ACQ_2240_NONCLAIM.csv | True | True |

## Validation
| check_id | result | detail |
| --- | --- | --- |
| VAL2240_00_sources_exist | PASS | all direct and registered 2240 source paths exist |
| VAL2240_01_prior_validations | PASS | 2239 and 1567 validations pass overall |
| VAL2240_02_web_sources_queued | PASS | external arena source URLs queued nonclaim and not treated as downloaded evidence |
| VAL2240_03_contract_written | PASS | joint parent protection contract is written but unsigned |
| VAL2240_04_audit_failed_parent_proof | PASS | contract audit refuses parent proof |
| VAL2240_05_conditional_theorem | PASS | conditional theorem is explicit |
| VAL2240_06_acquisition_queue | PASS | live acquisition queue exists but is not raw/accepted-ready |
| VAL2240_07_runner_blocks_claim | PASS | runner blocks local claim |
| VAL2240_08_claim_gates | PASS | claim gates remain closed except nonclaim source queue |
| VAL2240_09_path_fields | PASS | source path fields resolve locally |
| VAL2240_10_decision_next | PASS | decision selects parent derivation or first live finite row |
| VAL2240_11_next_target | PASS | next target is current-numbered parent contract derivation or first live row |
| VAL2240_12_csv_parse | PASS | all generated 2240 CSVs parse cleanly |
| VAL2240_13_claim_flags_false | PASS | all generated prediction/claim flags remain false |
| VAL2240_14_branch_copies | PASS | branch/quarantine nonclaim copies written |
| VAL2240_15_pycache_absent | PASS | scripts __pycache__ absent after run |
| VAL2240_16_formalization_no_2240 | PASS | formalization-workbench has no non-venv 2240 artifacts |
| VAL2240_17_formalization_untouched | PASS | formalization-workbench untouched during 2240 run |
| VAL2240_OVERALL | PASS | 2240 writes the parent protection contract, keeps the exact theorem conditional, starts nonclaim finite-source acquisition, and selects primitive derivation or first live row next |

## Working Interpretation

This is a clean fork in the road, not a failure. The theorem route now has a single contract to derive from motion/time/space primitives. The empirical fallback now has a source acquisition queue that refuses to score placeholders. Next we either derive the contract from primitives or fill the first source-backed finite/theorem-zero row without moving it to accepted.

