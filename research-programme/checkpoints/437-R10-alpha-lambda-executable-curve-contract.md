# 437 - R10 Alpha-Lambda Executable Curve Contract

Private R10/fifth-force checkpoint. This is not a public fifth-force, PPN, Einstein-Hilbert, Newtonian-limit, local-GR, cosmology, or unified-field claim.

## 1. Purpose

Checkpoint 436 routed several retained local branches into R10: bulk X tails, coarse-graining gradients, source-normalization flux, radial hair, boundary/domain hair, and non-EH operator remnants. This checkpoint removes the last loose language around R10: either a branch proves theorem-zero for finite-range forces, or it supplies an executable `alpha(lambda)` curve/envelope that can be compared to the external bound curve.

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/R10_alpha_lambda_executable_curve_contract.py` |
| Run directory | `runs/20260602-124500-R10-alpha-lambda-executable-curve-contract` |
| Status | `R10_alpha_lambda_executable_curve_contract_written_theorem_zero_or_curve_required_no_R10_pass_no_local_GR_pass` |
| Claim ceiling | `R10_alpha_lambda_curve_contract_only_no_fifth_force_PPN_EH_Newton_or_local_GR_pass` |
| Template | `source-intake\mts_residuals\R10_alpha_lambda_curve_TEMPLATE.csv` |
| Next target | `438-R11-nonEH-coefficient-vector-contract.md` |

## 3. Source Register

| source_file | exists | role |
| --- | --- | --- |
| 380-bulk-X-mass-gap-source-normalized-force-law.md | True | bulk X Yukawa force-law options and alpha_X(lambda_X) debt |
| 403-boundary-domain-flux-nohair-numeric-contract.md | True | boundary/domain/flux no-hair gates and fifth-force hair branch |
| 425-EH-operator-retained-ledger-and-source-normalization-test-plan.md | True | local-bound test matrix requiring verified alpha(lambda) curve for R10 |
| 428-MTS-local-residual-vector-input-contract.md | True | R10 residual vector input contract and symbolic curve comparison rule |
| 431-MTS-local-residual-vector-evaluator.md | True | local residual evaluator that blocks missing R10 curve files |
| 434-measured-GM-mu-extra-zero-route.md | True | measured mu decomposition showing finite-range/radial hair channels |
| 435-exterior-extra-source-nohair-owner-gate.md | True | exterior extra-source owners and bulk X theorem-zero fork |
| 436-auxiliary-projector-local-Euler-equation-ledger.md | True | C1 Euler ledger routing A0/A6/A7/A8 into R10 |
| source-intake/local_bounds/local_bound_claims.csv | True | R10 empirical row declaring alpha(lambda) symbolic and unscored |
| source-intake/mts_residuals/MTS_local_residual_predictions_TEMPLATE.csv | True | MTS residual template requiring curve_or_vector_file for R10 |
| runs/20260602-004500-bulk-X-mass-gap-source-normalized-force-law/results/bulk_X_operator_routes.csv | True | machine-readable bulk X operator route table |
| runs/20260602-004500-bulk-X-mass-gap-source-normalized-force-law/results/source_normalized_force_law.csv | True | source-normalized Yukawa alpha/lambda force-law ledger |
| runs/20260602-004500-bulk-X-mass-gap-source-normalized-force-law/results/gate_results.csv | True | bulk X force-law gates showing alpha(lambda) not parent-derived |
| runs/20260602-085500-EH-operator-retained-ledger-and-source-normalization-test-plan/results/local_bound_test_matrix.csv | True | local bound matrix row requiring R10 curve |
| runs/20260602-094500-MTS-local-residual-vector-input-contract/results/residual_components.csv | True | R10 residual component contract |
| runs/20260602-105000-MTS-local-residual-vector-evaluator/results/gate_results.csv | True | evaluator symbolic-file missing gate for R10 |
| runs/20260602-120000-measured-GM-mu-extra-zero-route/results/mu_extra_decomposition.csv | True | mu_extra channels that can induce radial/fifth-force residuals |
| runs/20260602-123000-auxiliary-projector-local-Euler-equation-ledger/results/Euler_ledger_rows.csv | True | A0/A6/A7/A8 Euler rows feeding R10 |

## 4. R10 Contract Chain

| step | contract | required_object | current_status | failure_if_missing |
| --- | --- | --- | --- | --- |
| 1 | R10 is a range-dependent inverse-square/fifth-force test, not a scalar local residual. | alpha(lambda) curve or theorem-zero derivation | symbolic_curve_required | no_R10_pass |
| 2 | The accepted Yukawa convention must be explicit before comparison. | V(r)=-G m1 m2/r [1+alpha(lambda) exp(-r/lambda)] | convention_written | formula_ambiguous |
| 3 | The acceleration residual must use the same convention as the bound curve. | a_extra/a_GR = alpha(lambda) (1+r/lambda) exp(-r/lambda) | convention_written | curve_not_comparable |
| 4 | A non-Yukawa retained force must be conservatively mapped to a Yukawa-equivalent envelope. | alpha_envelope(lambda) over the declared comparison range | contract_only_no_envelope_supplied | non_yukawa_symbolic_block |
| 5 | Theorem-zero can replace a curve only if the finite-range source is absent, gauge/topological, screened, or no-haired by a parent proof. | source-free positive operator/gauge identity/screening/no-hair derivation | not_derived | theorem_zero_not_available |
| 6 | A constant universal monopole may be absorbed into measured GM only if it is range/species/time independent. | source-normalized calibration proof | conditional_not_supplied | GM_absorption_not_allowed |
| 7 | Every curve row must carry derivation status, source path, formula reference, assumptions, and valid_for_claim flag. | executable CSV with declared columns | template_written_only | curve_file_invalid |
| 8 | Until a theorem-zero proof or real curve exists, R10 remains symbolic and blocks fifth-force/local-GR promotion. | no promotion from placeholders | enforced | false_local_GR_pass |

Core rule:

```text
R10 passes only if one of these exists:

1. theorem-zero:
   alpha(lambda) = 0 by parent-derived absence/gauge/topology/screening/no-hair/calibration proof;

2. executable curve:
   for each lambda_i, supply alpha_predicted(lambda_i), alpha_bound(lambda_i),
   units, force-law convention, source normalization, formula source, assumptions,
   and valid_for_claim=true after validation.

Anything else remains symbolic and blocks R10 promotion.
```

## 5. Accepted Force-Law Forms

| form_id | mathematical_form | alpha_meaning | lambda_meaning | accepted_for_R10 | notes |
| --- | --- | --- | --- | --- | --- |
| Yukawa_potential | V(r) = -G m1 m2/r [1 + alpha(lambda) exp(-r/lambda)] | dimensionless strength relative to Newtonian gravity at the same source/test normalization | finite interaction range | True | directly comparable when alpha_bound(lambda) uses the same convention |
| Yukawa_acceleration_ratio | a_extra/a_GR = alpha(lambda) (1 + r/lambda) exp(-r/lambda) | same alpha as potential convention | finite interaction range | True | needed when MTS branch predicts acceleration rather than potential |
| bulk_X_static_green_function | (-Delta + m_X^2) X = q_X rho_source; X(r)=Q_X exp(-r/lambda_X)/(4 pi r); lambda_X=1/m_X | source-normalized product of source and test charges relative to measured G | inverse positive mass gap | True | accepted only if q_X, Q_X, test charge, sign, and normalization are derived |
| non_yukawa_envelope | alpha_envelope(lambda) >= max_range |a_extra/a_GR mapped to Yukawa-equivalent bound convention| | conservative executable envelope | comparison scale used by external alpha(lambda) bound | True | allowed only as an explicit conservative map; symbolic text does not pass |

## 6. Alpha-Lambda Curve Schema

| column | meaning | required | example |
| --- | --- | --- | --- |
| model_id | MTS model/family label | True | MTS_branch_name |
| branch_id | specific derivation or parameter branch | True | fill_branch_id |
| curve_id | unique curve identifier for R10 | True | R10_alpha_lambda_curve |
| lambda_value | interaction range value | True | fill_numeric_lambda |
| lambda_units | units for lambda_value | True | m |
| alpha_predicted | dimensionless predicted or envelope fifth-force strength | True | fill_numeric_alpha_predicted |
| alpha_bound | dimensionless external upper bound at matching lambda | True | fill_numeric_alpha_bound |
| alpha_bound_source | reference path or URL for bound curve | True | Adelberger_Heckel_Nelson_2003_ISL_curve |
| force_law_form | Yukawa_potential, Yukawa_acceleration_ratio, bulk_X_static_green_function, or non_yukawa_envelope | True | Yukawa_potential |
| derivation_status | derived_zero, derived_bound, fitted, phenomenological, closure_assumed, or speculative | True | fill_derivation_status |
| formula_reference | file or equation source for alpha_predicted(lambda) | True | fill_formula_reference |
| source_file | source derivation or run artifact supplying the row | True | fill_source_file |
| assumptions | source normalization, exterior, matter-frame, and range assumptions | True | fill_assumptions |
| valid_for_claim | true only after the row is real data, not a placeholder | True | false |
| notes | comparison caveats and interpolation notes | False | no scalar placeholder pass |

## 7. Curve Comparison Rules

| rule_id | rule | pass_condition | current_status |
| --- | --- | --- | --- |
| C10_1_units | Convert every lambda_value into the bound-curve units before interpolation. | lambda units declared and conversion unambiguous | template_only |
| C10_2_bound_match | Compare alpha_predicted(lambda) against alpha_bound(lambda) at every supplied row. | abs(alpha_predicted) <= alpha_bound for all rows unless signed bounds are explicitly supplied | no_real_curve_supplied |
| C10_3_interpolation | Use conservative interpolation or a denser supplied curve across the declared lambda range. | no unsampled peak can exceed the bound between rows | not_yet_applicable |
| C10_4_non_yukawa | For non-Yukawa forces, compare only after a conservative alpha_envelope(lambda) map is supplied. | envelope is executable and source-normalized | not_supplied |
| C10_5_claim_flag | Rows with valid_for_claim=false are documentation templates only. | scorer ignores templates and placeholders | enforced |

## 8. Theorem-Zero Routes

| route_id | required_derivation | allowed_result | current_status |
| --- | --- | --- | --- |
| R10_Z0_absent_source | show the finite-range field/source coupling is exactly absent in compact ordinary local exteriors | alpha(lambda)=0 | not_derived |
| R10_Z1_positive_mass_gap_nohair | positive elliptic massive operator with source-free exterior, regular boundary data, and decaying solution | no local Yukawa tail outside calibrated source | operator_sign_and_sources_open |
| R10_Z2_gauge_topological | finite-range-looking variable is pure gauge/topological and has no local stress or matter charge | no physical fifth-force residual | not_derived |
| R10_Z3_screened_local_branch | screening solution with no composition/time/range leakage and no hidden preferred frame | alpha(lambda) below bound across the local test range | not_supplied |
| R10_Z4_universal_GM_calibration | constant universal source-normalized monopole independent of range, species, and time | absorbed into measured GM, not counted as finite-range R10 | conditional_not_proven |

## 9. Invalid R10 Inputs

| input_type | why_invalid | required_repair |
| --- | --- | --- |
| single_delta_G_scalar | R10 is range-dependent; a scalar cannot represent alpha(lambda) | supply curve rows over lambda or theorem-zero proof |
| symbolic_alpha_lambda_text | a formula without numeric/evaluable rows cannot be scored against a bound curve | emit executable curve or dense sampled envelope |
| mass_gap_without_source_normalization | lambda alone does not set alpha; source/test charges and measured-G normalization are required | derive q_source, q_test, Q_X, sign, and alpha normalization |
| negative_or_tachyonic_operator_called_screened | tachyonic or wrong-sign operators do not give the accepted local no-hair route | derive stable positive operator or retain explicit curve |
| boundary_or_domain_hair_absorbed_into_GM | radial/range/time/species dependent hair is not a constant universal calibration | prove constant universality or score as alpha(lambda) |
| template_row_valid_for_claim | placeholder rows are scaffolding, not evidence | replace placeholders and set valid_for_claim only after validation |

## 10. Template Rows

The reusable template has been written to `source-intake\mts_residuals\R10_alpha_lambda_curve_TEMPLATE.csv`.

| model_id | branch_id | curve_id | lambda_value | lambda_units | alpha_predicted | alpha_bound | alpha_bound_source | force_law_form | derivation_status | formula_reference | source_file | assumptions | valid_for_claim | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MTS_branch_name | fill_branch_id | R10_alpha_lambda_curve | fill_numeric_lambda | m | fill_numeric_alpha_predicted | fill_numeric_alpha_bound | fill_bound_curve_reference_or_file | Yukawa_potential | fill: derived_zero/derived_bound/fitted/phenomenological/closure_assumed/speculative | fill_formula_reference | fill_derivation_or_run_path | fill_same_frame_source_normalization_exterior_matter_range_assumptions | false | template row only; no scalar placeholder pass |
| MTS_branch_name | fill_branch_id | R10_alpha_lambda_curve | fill_numeric_lambda | m | fill_numeric_alpha_predicted | fill_numeric_alpha_bound | fill_bound_curve_reference_or_file | non_yukawa_envelope | fill: derived_bound/phenomenological/closure_assumed/speculative | fill_envelope_mapping_reference | fill_derivation_or_run_path | fill_conservative_envelope_range_and_normalization_assumptions | false | use only after non-Yukawa force is mapped to executable alpha_envelope(lambda) |

## 11. Gate Results

| gate | status | evidence |
| --- | --- | --- |
| source_paths_exist | pass | all cited source paths exist |
| template_schema_matches_contract | pass | template columns match alpha_lambda_curve_schema |
| R10_contract_chain_written | pass | 8-step theorem-zero-or-curve chain recorded |
| force_law_conventions_written | pass | Yukawa potential, acceleration ratio, bulk X Green function, and non-Yukawa envelope conventions recorded |
| alpha_lambda_schema_written | pass | 15-column executable curve schema recorded |
| R10_template_written | pass | source-intake\mts_residuals\R10_alpha_lambda_curve_TEMPLATE.csv |
| actual_alpha_lambda_curve_supplied | fail | template only; no real alpha_predicted(lambda) branch data supplied |
| R10_theorem_zero_derived | fail | no absent-source, positive no-hair, gauge/topological, screened, or universal-GM proof supplied |
| scalar_placeholder_allowed | fail | single scalar delta_G cannot pass R10 |
| R10_promoted | fail | R10 remains symbolic until theorem-zero or executable curve is supplied |
| local_GR_promoted | fail | fifth-force gate only; no PPN/EH/Newton/local-GR pass |
| claim_ceiling_enforced | pass | R10_alpha_lambda_curve_contract_only_no_fifth_force_PPN_EH_Newton_or_local_GR_pass |

## 12. Decision

R10 is now converted from a vague symbolic fifth-force debt into an executable contract. A branch may pass R10 only by deriving theorem-zero for every finite-range source, or by supplying an alpha(lambda) curve/envelope with explicit units, force-law convention, source normalization, bound source, assumptions, and valid_for_claim=true after validation. The current state is template-only: no theorem-zero proof and no real curve are supplied, so R10 remains symbolic and blocks fifth-force and local-GR promotion.

Practical read: this is a clean engineering gate. If MTS has no fifth-force locally, prove the no-force theorem. If it has a tiny one, draw the curve. If it cannot draw the curve, it has not beaten the local inverse-square tests yet. No shame, but no free pass.

## 13. Next Queue

| rank | target | why_next |
| --- | --- | --- |
| 1 | 438-R11-nonEH-coefficient-vector-contract.md | R11 is the sister symbolic row; non-EH operator families need EH-only theorem-zero or executable coefficient vectors |
| 2 | filled R10 alpha(lambda) curve | bulk X, L_cg, flux, or domain branches need real curve data before R10 can be scored |
| 3 | local residual scorer curve mode | 431 can block missing files; next scorer upgrade should parse and evaluate supplied alpha(lambda) rows |
