# 2975 — Gamma/Khat Sign Convention and Metric-Response Certificate, or Delta_K Bound Row

Status: `Y5_R2FR_2975_q_loc_positive_sign_locked_Khat_metric_response_not_derived_DeltaK_rows_written_nonclaim`

Claim ceiling: `no_Khat_equals_Kmetric_no_DeltaK_zero_no_q_loc_zero_no_local_GR_no_Newton_no_R10_no_PPN_no_clock_no_orbital_no_WEP_no_public_claim`

## Summary

- The canonical branch sign is now fixed: `T_q^{mu nu} := Gamma_eff g^{mu nu} - K_hat^{mu nu}`, so `nabla_mu T_q^{mu nu}` is exactly the unprojected `q_loc` expression.
- The older `2206` sign is not a contradiction; it is the negative-stress convention and is translated rather than used for scoring.
- `K_hat = K_metric[Gamma_eff]` is still not derived: the corpus has a formal metric-response route and a component list, not a source-backed component certificate.
- `Delta_K^{mu nu} := K_hat^{mu nu} - K_metric^{mu nu}` is now the retained nonclaim residual feeding `eps_q_loc_component`.
- Next target is `Gamma_eff` scalar-density ownership and the first `K_vol`/`DeltaK_vol` component.

## Generated Outputs

| output | path | exists |
| --- | --- | --- |
| sources | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_2975_SOURCE_REGISTER.csv | True |
| sign | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_2975_GAMMAKHAT_SIGN_CONVENTION_LOCK.csv | True |
| metric | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_2975_METRIC_RESPONSE_CERTIFICATE_AUDIT.csv | True |
| deltak | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_2975_DELTAK_COMPONENT_BOUND_ROWS_NONCLAIM.csv | True |
| rollforward | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_2975_QLOC_BOUND_ROLLFORWARD_NONCLAIM.csv | True |
| claims | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_2975_CLAIM_GATES.csv | True |
| decision | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_2975_DECISION_LEDGER.csv | True |
| next | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_2975_NEXT_TARGET.csv | True |
| branches | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_2975_BRANCH_COPIES.csv | True |

## Branch Copies

| copy | path | exists |
| --- | --- | --- |
| metric_copy | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\parent-action\GammaKhat_sign_metric_response_2975_NOT_DERIVED.csv | True |
| deltak_copy | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\local_bounds\DeltaK_component_bound_rows_2975_NONCLAIM.csv | True |
| next_copy | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\rab-sector\acquisition-queue\JR2975_Gamma_eff_scalar_density_owner_next_NONCLAIM.csv | True |

## Sign Convention Lock

| sign_id | object | definition | q_loc_relation | status | convention_selected | parent_theorem |
| --- | --- | --- | --- | --- | --- | --- |
| SIGN2975_0_canonical | canonical q_loc-positive stress | T_q^{mu nu}:=Gamma_eff g^{mu nu}-K_hat^{mu nu} | nabla_mu T_q^{mu nu}=nabla^nu Gamma_eff-nabla_mu K_hat^{mu nu} | SELECTED_BOOKKEEPING_CONVENTION | True | False |
| SIGN2975_1_metric | metric-response stress | T_metric^{mu nu}:=Gamma_eff g^{mu nu}-K_metric^{mu nu}[Gamma_eff] | if K_hat=K_metric then q_loc^nu=P_loc nabla_mu T_metric^{mu nu} | SELECTED_FOR_DELTAK_ACCOUNTING | True | False |
| SIGN2975_2_DeltaK | Delta_K convention | Delta_K^{mu nu}:=K_hat^{mu nu}-K_metric^{mu nu} | q_loc^nu=P_loc(nabla_mu T_metric^{mu nu})-P_loc(nabla_mu Delta_K^{mu nu}) plus projector/connection terms | LOCKED_NONCLAIM_RESIDUAL_CONVENTION | True | False |
| SIGN2975_3_2206_translate | opposite sign row translation | T_2206^{mu nu}:=K_hat^{mu nu}-Gamma_eff g^{mu nu}=-T_q^{mu nu} | Ward zero is sign-equivalent, but scoring must use the canonical q_loc-positive T_q | TRANSLATED_NOT_USED_FOR_SCORING | False | False |
| SIGN2975_4_guard | sign/volume guard | all Delta_K rows inherit the canonical T_q, K_metric and Delta_K definitions | no mixed-sign cancellation or measured-G absorption allowed | GUARD_ACTIVE | True | False |

## Metric-Response Certificate Audit

| metric_audit_id | object | required_statement | status | parent_signed | component_value_present |
| --- | --- | --- | --- | --- | --- |
| MR2975_0_Gamma_density | Gamma_eff scalar density | explicit local scalar density Gamma_eff(g,Phi,nabla Phi,D,...) with field content, units and metric dependence | MISSING_GAMMA_EFF_COMPONENT_FORMULA | False | False |
| MR2975_1_variation | K_metric formula | K_metric^{mu nu}:=2/sqrt(-g) delta[sqrt(-g)Gamma_eff]/delta g_{mu nu} with derivative/boundary conventions | FORMAL_DEFINITION_ONLY | False | False |
| MR2975_2_components | K_metric component split | K_metric=K_vol+K_deltaM+K_deltaZ+K_deriv+K_boundary | COMPONENTS_LISTED_VALUES_MISSING | False | False |
| MR2975_3_Khat_match | K_hat equals K_metric | source path showing current K_hat is defined as the same metric response under the same sign/volume/boundary convention | MISSING_COMPONENT_BY_COMPONENT_CERTIFICATE | False | False |
| MR2975_4_tracefree_route | trace-free Khat birth | trace-free improvement channel exists as a candidate but live Khat adoption, boundary/projector and amplitude response remain unsigned | CANDIDATE_NOT_LIVE_CERTIFICATE | False | False |
| MR2975_5_Helmholtz | Helmholtz symmetry | second variation of sqrt(-g)T_metric is symmetric up to allowed boundary terms | MISSING_HELMHOLTZ_CERTIFICATE | False | False |
| MR2975_6_verdict | K_hat=K_metric[Gamma_eff] | all metric-response rows close with source/equation paths | NOT_DERIVED_DELTAK_RETAINED | False | False |

## Delta_K Component Bound Rows

| deltak_id | symbol | definition_or_bound | units | status | required_input | upper_bound | accepted_for_scoring |
| --- | --- | --- | --- | --- | --- | --- | --- |
| DK2975_0_definition | Delta_K^{mu nu} | K_hat^{mu nu}-K_metric^{mu nu}[Gamma_eff] | stress | DEFINITION_LOCKED_NONCLAIM | source-backed K_hat/K_metric components | MISSING_SOURCE_BACKED_UPPER_BOUND | False |
| DK2975_1_Kvol | DeltaK_vol | K_hat_vol-K_vol where K_vol is the Gamma_eff g^{mu nu} volume/sign term | stress | MISSING_KVOL_VALUE | Gamma_eff density and volume convention | MISSING_SOURCE_BACKED_UPPER_BOUND | False |
| DK2975_2_KdeltaM | DeltaK_deltaM | K_hat_deltaM-K_deltaM from metric variation of M_AB | stress | MISSING_DELTA_MAB_VALUE | M_AB metric dependence | MISSING_SOURCE_BACKED_UPPER_BOUND | False |
| DK2975_3_KdeltaZ | DeltaK_deltaZ | K_hat_deltaZ-K_deltaZ from metric variation of Z basis | stress | MISSING_DELTA_Z_VALUE | Z^A metric/coframe dependence | MISSING_SOURCE_BACKED_UPPER_BOUND | False |
| DK2975_4_Kderiv | DeltaK_deriv | K_hat_deriv-K_deriv from derivative/principal-symbol/domain/CDB dependence | stress | MISSING_DERIVATIVE_TERMS | derivative order and integration-by-parts convention | MISSING_SOURCE_BACKED_UPPER_BOUND | False |
| DK2975_5_Kboundary | DeltaK_boundary | K_hat_boundary-K_boundary from boundary primitive, corners, P_loc, source worldtubes and support variation | stress | MISSING_BOUNDARY_TERMS | proper boundary/no-flux theorem or retained value | MISSING_SOURCE_BACKED_UPPER_BOUND | False |
| DK2975_6_DDelta | D_Delta | C_t\|\|partial_t Delta_K^{0nu}\|\|+C_r\|\|partial_r Delta_K^{rnu}\|\|+C_ang\|\|partial_ang Delta_K\|\|+C_conn\|\|Gamma_conn\|\|\|\|Delta_K\|\| | force-density norm | MISSING_COMPONENT_DERIVATIVE_VALUES | Delta_K component profiles and derivative constants | MISSING_SOURCE_BACKED_UPPER_BOUND | False |
| DK2975_7_projector_constants | C_Ploc,C_comm | \|\|q_DeltaK\|\| <= C_Ploc D_Delta + (C_comm_parallel+C_comm_domain+C_comm_boundary)\|\|Delta_K\|\| | operator/bound constants | MISSING_PROJECTOR_CONSTANTS | orthogonal projector theorem or source-backed constants | MISSING_SOURCE_BACKED_UPPER_BOUND | False |
| DK2975_8_score_gate | eps_DeltaK | eps_DeltaK <= q_*^{-1}(C_Ploc D_Delta + C_comm\|\|Delta_K\|\|) | dimensionless after q_* | NOT_SCORE_READY | q_*, Delta_K components, C_Ploc/C_comm and arena projections | MISSING_SOURCE_BACKED_UPPER_BOUND | False |

## q_loc Bound Rollforward

| rollforward_id | quantity | formula | meaning | accepted_for_scoring |
| --- | --- | --- | --- | --- |
| RF2975_0_master_q_loc | eps_q_loc_component | \|\|Z_q\|\| <= q_*^{-1}(eps_Ward + eps_DeltaK + eps_Ploc_comm + eps_boundary) | 2974 master bound preserved under canonical sign | False |
| RF2975_1_DeltaK_insert | eps_DeltaK | eps_DeltaK <= q_*^{-1}(C_Ploc D_Delta + C_comm\|\|Delta_K\|\|) | first Delta_K insertion after sign lock | False |
| RF2975_2_zero_branch | Delta_K zero route | if K_hat=K_metric and P_loc is covariantly fixed then eps_DeltaK=0 | conditional branch not claimed | False |
| RF2975_3_no_cancellation | absolute envelope | Ward, Delta_K, P_loc commutator and boundary rows are summed in absolute value unless a parent identity proves cancellation | guard remains active | False |

## Claim Gates

| claim_gate_id | claim | condition_passed | status | claim_allowed |
| --- | --- | --- | --- | --- |
| CG2975_0_sign | single q_loc-positive sign convention selected | True | BOOKKEEPING_CONVENTION_LOCKED_NOT_THEOREM | False |
| CG2975_1_Gamma_density | Gamma_eff scalar density source-backed | False | MISSING_GAMMA_EFF_FORMULA | False |
| CG2975_2_Kmetric | K_metric components computed | False | KMETRIC_COMPONENTS_MISSING_VALUES | False |
| CG2975_3_Khat_match | K_hat=K_metric | False | METRIC_RESPONSE_CERTIFICATE_MISSING | False |
| CG2975_4_DeltaK_zero | Delta_K=0 | False | DELTAK_RETAINED | False |
| CG2975_5_q_loc_zero | q_loc zero theorem | False | QLOC_ZERO_NOT_PARENT_SIGNED | False |
| CG2975_6_local_GR | local GR/Newton reduction | False | LOCAL_GR_NOT_DERIVED | False |
| CG2975_7_arena_claims | R10/PPN/clock/orbital/WEP claims | False | NO_ARENA_CLAIM_ALLOWED | False |

## Decision Ledger

| decision_id | decision | because | next_action |
| --- | --- | --- | --- |
| DEC2975_0_sign | Use the 2808-compatible q_loc-positive convention. | T_q=Gamma_eff g-K_hat makes nabla_mu T_q exactly the unprojected q_loc expression. | all future Delta_K rows use Delta_K=K_hat-K_metric |
| DEC2975_1_2206 | Treat 2206 as the negative-stress convention. | the Ward zero route is sign-equivalent, but mixed signs would corrupt bounds. | do not score with the 2206 sign |
| DEC2975_2_metric | K_hat=K_metric is not proved. | the corpus has a formal route and component list, not a source-backed component certificate. | retain Delta_K |
| DEC2975_3_next | The next derivation target is Gamma_eff scalar density ownership. | without the full scalar density and metric dependence, K_metric components cannot be computed. | run 2976 on Gamma_eff/K_vol first |

## Next Target

| next_id | priority | next_doc | next_script | objective | exclude |
| --- | --- | --- | --- | --- | --- |
| NEXT2975_0_2976 | selected_primary | 2976-Y5-R2FR-Gamma-eff-scalar-density-owner-and-Kmetric-volume-component-or-DeltaK-first-bound-under-AX1090.md | scripts/Y5_R2FR_Gamma_eff_scalar_density_owner_and_Kmetric_volume_component_or_DeltaK_first_bound_under_AX1090_2976.py | Source or construct the explicit Gamma_eff scalar density, field content, units and metric dependence needed to compute the K_vol component of K_metric; if not, emit the first DeltaK_vol bound/input row. | plateau axiom;bookkeeping stress claim;full K_metric certificate;full Z-basis scoring;Y5/Y6/PPN closure;R10 alpha claim;PPN claim;clock/orbital claim;local-GR claim;GitHub action;formalization-workbench edits |

## Validation

| validation_id | passed | check | required |
| --- | --- | --- | --- |
| VAL2975_0_sources_exist | True | all cited local source paths exist | True |
| VAL2975_1_anchors_found | True | all cited source anchors found | True |
| VAL2975_2_canonical_sign_selected | True | canonical q_loc-positive sign convention selected | True |
| VAL2975_3_2206_translated | True | opposite 2206 sign translated and excluded from scoring | True |
| VAL2975_4_metric_not_derived | True | K_hat=K_metric remains unproved | True |
| VAL2975_5_deltak_rows_nonclaim | True | Delta_K rows exist and remain nonclaim | True |
| VAL2975_6_claims_blocked_except_convention | True | all physics claim gates remain blocked except bookkeeping convention | True |
| VAL2975_7_next_target_written | True | 2976 Gamma_eff scalar density next target selected | True |
| VAL2975_8_branches_exist | True | branch copy files exist | True |
| VAL2975_9_csvs_parse | True | all generated CSV files parse | True |
| VAL2975_10_outputs_under_post_checkpoint | True | all generated outputs are under post-checkpoint-work | True |
| VAL2975_11_formalization_clean | True | no 2975 outputs were written to formalization-workbench | True |
| VAL2975_12_doc_written | True | 2975 markdown checkpoint exists | True |
| VAL2975_OVERALL | True | 2975 validation overall | True |

Validation overall: `True`.
