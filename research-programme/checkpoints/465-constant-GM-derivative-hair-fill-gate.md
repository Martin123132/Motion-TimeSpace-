# 465 - Constant-GM Derivative-Hair Fill Gate

Private source-normalization checkpoint. This is not a public measured-GM, Newtonian-limit, PPN, local-GR, cosmology, EM, or unified-field claim.

## 1. Question

Checkpoint 464 identified `source_normalization_operator` as the highest-priority R11 row because it decides whether measured Newtonian `GM` is a constant source charge or a place where hidden boundary/bulk/domain/range/source hair can hide.

This checkpoint asks the sharper question:

Can `mu_obs` be constant in time, radius, species, range, frame, and domain from the parent theory, or must every surviving derivative become an explicit residual row?

## 2. Run Metadata

| Field | Value |
| --- | --- |
| Script | `scripts/constant_GM_derivative_hair_fill_gate.py` |
| Run directory | `runs\20260602-211500-constant-GM-derivative-hair-fill-gate` |
| Status | `constant_GM_derivative_hair_fill_gate_written_exact_log_derivative_identity_derived_all_hair_channels_retained_unfilled_no_Newton_or_local_GR_pass` |
| Claim ceiling | `constant_GM_derivative_hair_gate_only_no_constant_GM_Newton_PPN_or_local_GR_pass` |
| Derivative gate CSV | `source-intake\mts_residuals\P8_CONSTANT_GM_DERIVATIVE_HAIR_GATE.csv` |
| Fill queue CSV | `source-intake\mts_residuals\P8_CONSTANT_GM_DERIVATIVE_HAIR_FILL_QUEUE.csv` |
| R11 derivative vector CSV | `source-intake\mts_residuals\R11_SOURCE_NORMALIZATION_DERIVATIVE_HAIR_VECTOR.csv` |
| Next target | `466-constant-GM-zero-theorem-or-local-residual-runner.md` |

## 3. Source Register

| path | exists | role |
| --- | --- | --- |
| 434-measured-GM-mu-extra-zero-route.md | True | mu_obs = G_eff M_eff + mu_extra decomposition and mu_extra zero route |
| 460-source-normalized-Newton-branch-theorem-stack.md | True | source-normalized Newton theorem stack and SN closure dependencies |
| 461-PG-residual-input-derive-or-fill-gate.md | True | P8 derivative/source-normalization residual rows |
| 462-charge-current-equality-direct-derivation-attempt.md | True | charge-current residual decomposition feeding measured-source closure |
| 463-EH-only-or-R11-executable-vector-gate.md | True | EH-only failure and R11 vector branch decision |
| 464-R11-executable-vector-minimum-fill-skeleton.md | True | source_normalization_operator chosen as highest-priority R11 family |
| source-intake\mts_residuals\P8_PG_residual_input_DERIVE_OR_FILL_GATE.csv | True | machine-readable P8 derive/fill rows |
| source-intake\mts_residuals\P8_PG_residual_input_STATUS.csv | True | machine-readable P8 no-claim status rows |
| source-intake\mts_residuals\R11_MTS_MINIMUM_EXECUTABLE_VECTOR_SKELETON.csv | True | minimum executable R11 skeleton with source_normalization_operator row |
| source-intake\mts_residuals\R11_P8_source_normalization_rows_TEMPLATE.csv | True | source-normalization operator template rows |
| runs\20260602-120000-measured-GM-mu-extra-zero-route\results\mu_extra_decomposition.csv | True | mu_extra channel decomposition from checkpoint 434 |

## 4. Exact Law

Start from the measured-source decomposition already isolated in the P8 route:

```text
mu_obs = G_eff M_eff + mu_extra.
```

Define the dimensionless source-normalization hair

```text
epsilon_mu := mu_extra / (G_eff M_eff).
```

Then

```text
mu_obs = G_eff M_eff (1 + epsilon_mu).
```

For any local derivative/readout channel

```text
X in {t, r, species A, range lambda, frame, domain},
```

the exact log-derivative law is

```text
D_X ln mu_obs
  = D_X ln G_eff
  + D_X ln M_eff
  + D_X ln(1 + epsilon_mu).
```

So constant measured `GM` is not a vibe; it is the finite checklist

```text
D_X ln mu_obs = 0 for every X.
```

A row can pass only if the terms are theorem-zero, numerically bounded below the relevant lock, or cancelled by a parent-derived identity. Tuned cancellation does not count.

## 5. Derivative-Hair Gate

The derivative-hair gate has been written to `source-intake\mts_residuals\P8_CONSTANT_GM_DERIVATIVE_HAIR_GATE.csv`.

| channel_id | derivative_channel | exact_identity | zero_condition | mapped_P8_component | mapped_symbol | affected_rows | current_evidence | evidence_required | minimum_fill_artifact | cancellation_policy | current_decision | valid_for_Newton_claim | valid_for_local_GR_claim | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CGM0_master_identity | any channel X in {t,r,A,lambda,frame,domain} | epsilon_mu := mu_extra/(G_eff M_eff); mu_obs = G_eff M_eff(1+epsilon_mu); D_X ln mu_obs = D_X ln G_eff + D_X ln M_eff + D_X ln(1+epsilon_mu) | D_X ln G_eff = 0, D_X ln M_eff = 0, and D_X epsilon_mu = 0, or their cancellation is a parent-derived identity | all_P8_source_normalization_rows | D_X_ln_mu_obs | R1;R4;R9;R10;R11 | exact algebraic identity derived from the existing mu_obs decomposition | for a pass, each derivative channel must be theorem-zero or numerically filled below its lock | this gate plus one channel-specific residual/theorem artifact per active derivative channel | not allowed as a tuning; only a Ward/superselection/source identity may cancel terms for claim credit | derived_identity_only_no_zero_claim | false | false | this is the useful law; it converts vague measured-GM language into a row-by-row derivative scorecard |
| CGM1_time_drift | D_t | d ln mu_obs/dt = d ln G_eff/dt + d ln M_eff/dt + d ln(1+epsilon_mu)/dt | dln_Geff_dt = 0; dln_Meff_dt = 0; partial_t epsilon_mu = 0, or parent-owned exact cancellation | P8_Geff_time_drift;P8_Meff_conservation;P8_boundary_bulk_domain_mu_extra | dln_Geff_dt;dln_Meff_dt;partial_t_epsilon_mu | R4;R9;R11 | 461 retains dln_Geff_dt and dln_Meff_dt unfilled; 462 leaves Delta_flux/Delta_G/Delta_extra active | parent superselection plus calibrated Pi_M flux conservation, or numeric local drift residual | P8_time_drift_residual_or_zero.csv with units yr^-1 and separate G_eff/M_eff/mu_extra terms | time cancellation must be an identity, not a fitted epoch-by-epoch balance | retained_unfilled_no_claim | false | false | this is the local Gdot lock; cosmology memory activity cannot be imported as local drift silence |
| CGM2_radial_hair | D_r | partial_r ln mu_obs = partial_r ln G_eff + partial_r ln M_eff + partial_r ln(1+epsilon_mu) | no radial G_eff profile, no radial M_eff leakage, and no radial mu_extra outside compact support | P8_radial_source_hair;P8_boundary_bulk_domain_mu_extra;P8_range_dependence | partial_r_ln_mu_obs;partial_r_epsilon_mu;alpha(lambda) | R4;R10;R11 | 461 retains partial_r_ln_mu_obs unfilled; 434 identifies radial mu_extra as a failure channel | Gauss/no-hair theorem or radial profile envelope relative to measured GM | P8_radial_mu_profile_or_zero.csv with radius units and bound source | radial cancellation must hold for every exterior radius, not only at an orbital calibration point | retained_unfilled_no_claim | false | false | if this survives, Newton becomes range/radius-dependent rather than clean inverse-square source normalization |
| CGM3_species_source_charge | D_A or Delta_AB across source/test species | Delta_AB ln mu_obs = Delta_AB ln G_eff + Delta_AB ln M_eff + Delta_AB ln(1+epsilon_mu) | source action is selector-blind and mu_obs is composition/species independent | P8_species_source_charge;P8_frame_calibration_split | eta_source_AB;partial_A_ln_mu_obs | R1;R11 | 461 separates source-charge WEP from direct coframe WEP and retains eta_source_AB unfilled | no-species source-charge theorem or eta_source_AB residual below the source lock | P8_species_source_charge_residual_or_zero.csv with material/source assumptions | species cancellation must be universal over allowed sources, not tuned per material | retained_unfilled_no_claim | false | false | direct WEP geometry is helpful but does not alone prove source-current universality |
| CGM4_range_dependence | D_lambda or finite-range branch scan | D_lambda ln mu_obs = D_lambda ln G_eff + D_lambda ln M_eff + D_lambda ln(1+epsilon_mu); a nonzero finite-range term maps to alpha(lambda) | alpha(lambda)=0 by theorem, or an executable alpha(lambda) curve stays below bounds for every relevant lambda | P8_range_dependence;R11_EH_operator_ledger | alpha(lambda);D_lambda_ln_mu_obs | R10;R11 | 461 and 464 both mark the R10 alpha(lambda) link required but missing | no-range theorem or R10 alpha(lambda) curve with predicted and bound columns | R10_alpha_lambda_curve_MTS_source_normalization.csv or theorem-zero source path | range cancellation must be functional in lambda, not a single-scale calibration | retained_unfilled_no_claim | false | false | symbolic fifth-force silence is not enough; this row needs a curve or a proof |
| CGM5_frame_domain_split | Delta_frame or D_domain | Delta_frame ln mu_obs = Delta_frame ln G_eff + Delta_frame ln M_eff + Delta_frame ln(1+epsilon_mu) | one observed coframe/source frame/domain readout is parent-selected for source variation and matter motion | P8_frame_calibration_split | delta_frame_source | R0;R2;R11 | 461 reports only partial conditional same-frame evidence; source variation remains not parent-derived | parent frame theorem or frame/source calibration residual below WEP and clock locks | P8_frame_source_split_residual_or_zero.csv with same-frame assumptions | frame cancellation must be a single parent pullback, not post-hoc coordinate relabeling | retained_unfilled_no_claim | false | false | this keeps the source-side frame issue attached to the variational source, not just the geodesic readout |
| CGM6_mu_extra_amplitude | epsilon_mu amplitude and all D_X epsilon_mu | epsilon_mu = mu_extra/(G_eff M_eff); D_X ln(1+epsilon_mu) = (D_X epsilon_mu)/(1+epsilon_mu) | epsilon_mu = 0, or epsilon_mu is a universal constant calibration and every derivative D_X epsilon_mu vanishes | P8_boundary_bulk_domain_mu_extra;R11_EH_operator_ledger | mu_extra_boundary_bulk_domain/(G_eff M_eff);D_X_epsilon_mu | R3;R4;R7;R8;R9;R11 | 434 decomposes mu_extra channels; 461 retains the central mu_extra row unfilled; 464 leaves source_normalization_operator unfilled | mu_extra=0 theorem or coefficient/residual map for every boundary, bulk, domain, memory, and non-EH channel | P8_mu_extra_over_Geff_Meff_vector.csv with channel coefficients and derivative tags | constant universal calibration may be absorbed; radial/time/species/range/frame variation may not | retained_unfilled_no_claim | false | false | this is the main hair vector: even if its amplitude is tiny, it must be sourced or bounded |
| CGM7_second_order_beta_residue | second-order source-normalized weak field | after first-order mu_obs is fixed, delta_beta_source is the remaining U^2 source-normalization residue | delta_beta_source=0 and gamma-1=0 after measured-GM normalization | P8_nonlinear_beta_source_residue;R11_EH_operator_ledger | delta_beta_source;beta_minus_1;gamma_minus_1 | R3;R4;R11 | 461 marks beta residue not required for first-order only but blocking for local-GR promotion | second-order weak-field theorem-zero or numeric PPN residual vector after constant-GM rows are owned | P8_second_order_source_normalized_PPN_vector.csv | beta cancellation cannot be inferred from first-order Poisson/Gauss | deferred_until_first_order_source_rows_owned | not_required_for_first_order_only | false | kept in the gate so nobody accidentally upgrades Newton to GR on first-order evidence |

## 6. Minimum Fill Queue

The minimum fill queue has been written to `source-intake\mts_residuals\P8_CONSTANT_GM_DERIVATIVE_HAIR_FILL_QUEUE.csv`.

| priority | target_row | symbol | minimum_acceptance | artifact_required | blocks | claim_if_missing | next_action |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | CGM6_mu_extra_amplitude | mu_extra_boundary_bulk_domain/(G_eff M_eff) | mu_extra=0 theorem or explicit coefficient vector with units/normalization/source paths | P8_mu_extra_over_Geff_Meff_vector.csv | constant_GM;Newton;R11_source_normalization_operator | no measured-GM absorption claim | try parent no-hair/Ward owner zero; otherwise fill coefficients |
| 2 | CGM1_time_drift | dln_Geff_dt;dln_Meff_dt;partial_t_epsilon_mu | separate drift terms in yr^-1 or parent superselection/flux-conservation theorem-zero | P8_time_drift_residual_or_zero.csv | Gdot_over_G;local_GR | no local Gdot silence | derive global-coupling superselection and Pi_M conservation or load drift bound |
| 3 | CGM2_radial_hair | partial_r_ln_mu_obs | radial no-hair theorem or profile envelope relative to measured GM | P8_radial_mu_profile_or_zero.csv | inverse_square_Newton;R10 | no radius-independent GM claim | derive Gauss/no-hair exterior or fill radial profile |
| 4 | CGM4_range_dependence | alpha(lambda) | theorem-zero or executable alpha(lambda) curve | R10_alpha_lambda_curve_MTS_source_normalization.csv | fifth_force;R10;R11 | no finite-range silence claim | build source-normalization alpha(lambda) curve or no-range theorem |
| 5 | CGM3_species_source_charge | eta_source_AB | source-charge theorem-zero or residual below source lock | P8_species_source_charge_residual_or_zero.csv | R1_source_charge;WEP_full | direct WEP only; source WEP retained | prove selector-blind source action or fill eta_source_AB |
| 6 | CGM5_frame_domain_split | delta_frame_source | same parent pullback for source variation and matter readout or residual bound | P8_frame_source_split_residual_or_zero.csv | same_frame_Newton;clock_link | no same-frame source-normalization claim | attach frame theorem to source variation, not only matter motion |
| 7 | CGM7_second_order_beta_residue | delta_beta_source | second-order source-normalized PPN vector after first-order rows are closed | P8_second_order_source_normalized_PPN_vector.csv | local_GR;PPN_beta_gamma | Newton may remain first-order only; local GR cannot pass | defer until CGM1-CGM6 are theorem-zero or numerically scored |

## 7. R11 Source-Normalization Vector

The derivative-specialized R11 vector has been written to `source-intake\mts_residuals\R11_SOURCE_NORMALIZATION_DERIVATIVE_HAIR_VECTOR.csv`.

| model_id | branch_id | vector_id | operator_family | coefficient_symbol | coefficient_value | coefficient_units | normalization | operator_form | weak_field_map | affected_rows | induced_observable | predicted_residual_or_bound_source | derivation_status | formula_reference | source_file | assumptions | valid_for_claim | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_source_normalized_Newton_branch | constant_GM_derivative_hair_gate | R11_source_normalization_derivative_hair_vector | source_normalization_operator | epsilon_mu_vector | MISSING_DERIVED_ZERO_OR_NUMERIC_BOUND | dimensionless | epsilon_mu=mu_extra/(G_eff M_eff) | mu_obs = G_eff M_eff(1+epsilon_mu) | CGM0_master_identity;CGM6_mu_extra_amplitude | R1;R4;R9;R10;R11 | eta_source_AB;beta_minus_1;Gdot_over_G;alpha(lambda);operator_ledger | MISSING_P8_MU_EXTRA_VECTOR_OR_ZERO_THEOREM | retained_unfilled | 465-constant-GM-derivative-hair-fill-gate.md | source-intake\mts_residuals\P8_CONSTANT_GM_DERIVATIVE_HAIR_GATE.csv | same-frame weak-field branch; source-normalization decomposition from checkpoint 434 | false | exact epsilon definition supplied, but no zero/bound coefficient supplied |
| MTS_source_normalized_Newton_branch | constant_GM_derivative_hair_gate | R11_source_normalization_derivative_hair_vector | time_drift_source_memory | dln_mu_obs_dt_vector | MISSING_DERIVED_ZERO_OR_NUMERIC_DRIFT | yr^-1 | d ln mu_obs/dt = dln_Geff_dt + dln_Meff_dt + dln(1+epsilon_mu)/dt | local time drift of measured source strength | CGM1_time_drift | R4;R9;R11 | Gdot_over_G;beta_minus_1;operator_ledger | MISSING_P8_TIME_DRIFT_RESIDUAL_OR_ZERO_THEOREM | retained_unfilled | 465-constant-GM-derivative-hair-fill-gate.md | source-intake\mts_residuals\P8_CONSTANT_GM_DERIVATIVE_HAIR_GATE.csv | local compact exterior, no imported cosmological drift cancellation | false | must report G_eff, M_eff, and epsilon_mu contributions separately |
| MTS_source_normalized_Newton_branch | constant_GM_derivative_hair_gate | R11_source_normalization_derivative_hair_vector | radial_range_source_hair | partial_r_ln_mu_obs_and_alpha_lambda | MISSING_DERIVED_ZERO_PROFILE_OR_ALPHA_CURVE | 1/length_or_range_dependent | partial_r ln mu_obs and alpha(lambda) relative to measured GM | radial/range-dependent measured-source strength | CGM2_radial_hair;CGM4_range_dependence | R4;R10;R11 | alpha(lambda);perihelion;operator_ledger | MISSING_RADIAL_PROFILE_OR_R10_ALPHA_LAMBDA_CURVE | retained_unfilled | 465-constant-GM-derivative-hair-fill-gate.md | source-intake\mts_residuals\P8_CONSTANT_GM_DERIVATIVE_HAIR_GATE.csv | radius and range silence must be functional, not single-calibration | false | this row prevents hiding finite-range hair inside measured GM |
| MTS_source_normalized_Newton_branch | constant_GM_derivative_hair_gate | R11_source_normalization_derivative_hair_vector | species_source_charge | eta_source_AB_or_partial_A_ln_mu_obs | MISSING_DERIVED_ZERO_OR_NUMERIC_SOURCE_CHARGE | dimensionless | eta_source_AB from source-side mu_obs composition dependence | species/material/source marker coupling in measured source strength | CGM3_species_source_charge | R1;R11 | eta_source_AB;operator_ledger | MISSING_SOURCE_CHARGE_RESIDUAL_OR_ZERO_THEOREM | retained_unfilled | 465-constant-GM-derivative-hair-fill-gate.md | source-intake\mts_residuals\P8_CONSTANT_GM_DERIVATIVE_HAIR_GATE.csv | source action is selector-blind across allowed materials | false | direct WEP geometry does not auto-fill this source-side row |
| MTS_source_normalized_Newton_branch | constant_GM_derivative_hair_gate | R11_source_normalization_derivative_hair_vector | frame_calibration_source_split | delta_frame_source | MISSING_DERIVED_ZERO_OR_NUMERIC_FRAME_SPLIT | dimensionless | Delta_frame ln mu_obs in observed matter/source frame | frame/source calibration mismatch in measured-source strength | CGM5_frame_domain_split | R0;R2;R11 | eta_WEP_direct_geometry;clock_redshift;operator_ledger | MISSING_FRAME_SOURCE_SPLIT_RESIDUAL_OR_ZERO_THEOREM | retained_unfilled | 465-constant-GM-derivative-hair-fill-gate.md | source-intake\mts_residuals\P8_CONSTANT_GM_DERIVATIVE_HAIR_GATE.csv | one parent pullback for source variation and matter readout | false | source variation must live in the same observed frame as the orbital readout |
| MTS_source_normalized_Newton_branch | constant_GM_derivative_hair_gate | R11_source_normalization_derivative_hair_vector | second_order_source_normalization | delta_beta_source | MISSING_SECOND_ORDER_PPN_SOURCE_VECTOR | dimensionless | source-normalized U^2 coefficient after first-order measured GM is fixed | second-order source-normalization residue | CGM7_second_order_beta_residue | R3;R4;R11 | gamma_minus_1;beta_minus_1;operator_ledger | MISSING_SECOND_ORDER_PPN_VECTOR_OR_ZERO_THEOREM | deferred_retained_unfilled | 465-constant-GM-derivative-hair-fill-gate.md | source-intake\mts_residuals\P8_CONSTANT_GM_DERIVATIVE_HAIR_GATE.csv | first-order CGM rows are already theorem-zero or numerically scored | false | blocks local-GR promotion even if first-order Newton later passes |

## 8. Gate Results

| gate | status | evidence | claim_credit |
| --- | --- | --- | --- |
| CGMV0_source_paths | pass | missing source paths = 0 | audit_only |
| CGMV1_P8_rows_loaded | pass | P8 PG rows loaded = 9 | schema_only |
| CGMV2_R11_source_norm_loaded | pass | R11 skeleton rows = 10; source_normalization_operator rows = 1 | schema_only |
| CGMV3_derivative_identity | pass | mu_obs = G_eff M_eff(1+epsilon_mu) implies exact D_X ln mu_obs identity | identity_only |
| CGMV4_zero_conditions_parent_derived | fail | all derivative channels retain missing theorem-zero or numeric residual artifacts | none |
| CGMV5_R11_vector_executable | fail | missing markers in derivative R11 vector = 12; generic output placeholders = 0 | none |
| CGMV6_constant_GM_promoted | fail | constant measured GM requires CGM1-CGM6 theorem-zero or numeric scoring | none |

## 9. Theorem Status

| claim | status | evidence |
| --- | --- | --- |
| exact constant-GM derivative law derived | pass_identity | D_X ln mu_obs identity follows algebraically from mu_obs = G_eff M_eff + mu_extra |
| source-normalization derivative hair is zero | fail | no parent-zero theorem or numeric residual vector supplied for CGM1-CGM6 |
| constant measured GM is parent-derived | fail | G_eff, M_eff, epsilon_mu, source, range, radial, and frame derivatives remain retained |
| Newtonian reduction promoted | fail | constant measured GM and R11 source-normalization vector are not executable |
| local GR promoted | fail | second-order beta/gamma source-normalized vector remains deferred and unfilled |

## 10. Decision

The exact derivative law lands. That is real progress: measured `GM` now has a clean algebraic spine instead of a loose calibration phrase.

But the zero theorem does not land yet. The law exposes the debt:

```text
constant GM requires
D_X ln G_eff = 0,
D_X ln M_eff = 0,
D_X epsilon_mu = 0
for every local channel X,
or a parent identity that cancels them exactly.
```

Current corpus state: P8 rows loaded = `9`, P8 source-normalization template rows = `6`, R11 source-normalization skeleton rows = `1`, derivative-vector `MISSING_` markers = `12`, generic output `fill_` placeholders = `0`.

So the round is scored like this: we landed the jab cleanly, but we do not raise the belt. Exact identity: yes. Constant-GM theorem: no. Newton/local-GR promotion: no.

## 11. Next Queue

| Priority | Target | Reason |
| --- | --- | --- |
| 1 | `466-constant-GM-zero-theorem-or-local-residual-runner.md` | either prove `epsilon_mu`, `G_eff`, and `M_eff` are derivative-silent, or start loading actual local residual/bound rows |
| 2 | `R10_alpha_lambda_curve_MTS_source_normalization.csv` | range dependence cannot pass with symbolic `alpha(lambda)` language |
| 3 | `P8_second_order_source_normalized_PPN_vector.csv` | local GR needs beta/gamma after first-order source normalization |
