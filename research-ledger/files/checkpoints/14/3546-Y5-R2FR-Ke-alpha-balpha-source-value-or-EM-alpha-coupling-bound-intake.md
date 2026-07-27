# 3546 — Ke-alpha b-alpha source value or EM alpha-coupling bound intake

## Verdict

- **No sourced numeric `K_e_alpha*b_alpha` value exists yet.** The corpus has an exact alpha identity and usable empirical ceilings, but not the parent-owned product value.
- **The actual law is now pinned down:** `b_alpha = D_X ln alpha_eff = 2 z_g - z_lambda`, with `alpha_eff proportional to g_J^2/lambda_A` after canonical normalization.
- **Finite nonclaim gate:** in the DD-like e basis, any future isolated alpha product must satisfy `|K_e_alpha*b_alpha| <= 1.372549e-12`; in the older alpha-Coulomb convention the ceiling is `1.407170e-12`.
- **Baseline route:** calibrated local alpha may be held fixed as a measured constant for Maxwell stress/local-GR bookkeeping, but that is not a derived parent theorem.

## Exact identity

| identity_id | object | mathematical_form | result | zero_or_bound_role |
| --- | --- | --- | --- | --- |
| KAB3546_0_EM_action_start | local EM normalization | S_EM[X] = -1/4 lambda_A(X) int F^2 + g_J(X) int A_mu J^mu | the raw Maxwell kinetic coefficient and current coupling are separately convention-dependent | sets the exact variables whose mismatch becomes b_alpha |
| KAB3546_1_canonical_charge | canonical local charge | A_c = sqrt(lambda_A) A; g_eff = g_J/sqrt(lambda_A); alpha_eff proportional to g_J^2/lambda_A | a field rescaling can move coefficients but cannot remove the invariant ratio | prevents false alpha-zero claims by convention |
| KAB3546_2_balpha_law | alpha vertical residual | b_alpha := D_X ln alpha_eff = 2 z_g - z_lambda | K_e_alpha*b_alpha is zero only if alpha is calibrated constant or parent proves 2 z_g = z_lambda | exact law for the EM/source coupling target |
| KAB3546_3_WEP_projection | alpha-only WEP channel | eta_TiPt^(alpha) = DeltaQ_e(TiPt) * (K_e_alpha*b_alpha) + R_nonalpha | under an isolated no-cancellation alpha branch, \|K_e_alpha*b_alpha\| <= 1.372549019608e-12 | finite branch bound if parent zero does not close |

## Zero-proof clauses

| clause_id | claim | mathematical_condition | effect_on_product | status | remaining_gap |
| --- | --- | --- | --- | --- | --- |
| ZKAB3546_0_calibrated_baseline | baseline local branch may set alpha_EM=alpha_0 as measured universal constant | D_X ln alpha_eff = 0 | K_e_alpha*b_alpha = 0 if K_e_alpha is finite | CLOSURE_BASELINE_ALLOWED_NOT_DERIVED | calibration is not a parent derivation of alpha or C_XF2=0 |
| ZKAB3546_1_parent_same_owner | parent quotient owner ties current normalization to Maxwell kinetic normalization | 2 z_g - z_lambda = 0 | b_alpha=0 without using calibration closure | DERIVATION_ROUTE_OPEN_UNSIGNED | fixed representation/current owner and unique F2/fibre norm must be proved in one parent object-language |
| ZKAB3546_2_no_source_marker | alpha channel carries no material/source marker after Hilbert source reduction | partial_A mu_obs(alpha marker)=0 and beta_source_alpha=0 | prevents K_e_alpha from becoming species/source-dependent even when b_alpha is present | SOURCE_MARKER_ZERO_UNSIGNED | pre-variation weights and non-Hilbert bypass remain legal until action grammar closes |
| ZKAB3546_3_readout_radiative_stability | loops, clocks, material binding and readout maps do not regenerate alpha dependence | R_readout_alpha = R_rad_alpha = 0 | keeps calibrated alpha from re-entering as an effective WEP/source coefficient | READOUT_STABILITY_UNSIGNED | radiative/readout closure not parent-signed |
| ZKAB3546_4_factorized_source_leg | K_e_alpha is a real source/material projection, not a hidden fitted number | K_e_alpha = K[Earth source, Ti/Pt material tensor, readout convention, q normalization] | lets a nonzero b_alpha be scored against MICROSCOPE instead of being a placeholder | FINITE_BOUND_ROUTE_INPUTS_MISSING | Earth/source leg, alloy policy, q units and sign convention |

## Product bounds

| bound_id | target | arena | formula | bound_value | units | mts_value_ready | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| B3546_0_DD_e_basis | K_e_alpha*b_alpha | MICROSCOPE alpha/source WEP, DD-like e basis | abs(K_e_alpha*b_alpha) <= eta_bound / abs(DeltaQ_e) | 1.372549019608e-12 | dimensionless effective source-coupling product | False | False |
| B3546_1_alpha_Coulomb_basis | D_e_eff(alpha-only) | MICROSCOPE alpha-only Coulomb-material convention | abs(D_e_eff) <= eta_bound / abs(DeltaQ_alpha_Coulomb) | 1.407170315973e-12 | dimensionless effective alpha source coefficient | False | False |
| B3546_2_convention_bridge_spread | basis reconciliation | DD e basis versus alpha-only Coulomb basis | abs(B_DD_e - B_alpha_Coulomb)/B_DD_e | 2.522408735197e-02 | fractional spread | False | False |
| B3546_3_clock_product_quarantine | b_alpha*tau_clock_time | atomic clock alpha drift | abs(P_clock_alpha) <= 2.1e-18 yr^-1 | 2.100000000000e-18 | yr^-1 | False | False |

## Input contract

| input_id | target | must_supply | acceptance_gate | current_status |
| --- | --- | --- | --- | --- |
| IN3546_0_balpha_parent_value_or_zero | b_alpha | parent theorem for 2 z_g = z_lambda, or numeric b_alpha with source path and units | no field-rescaling-only argument; current and Maxwell kinetic owners must be tracked together | MISSING_PARENT_VALUE_OR_ZERO |
| IN3546_1_Ke_alpha_factorized | K_e_alpha | Earth/source leg, Ti/Pt material tensor, alpha/Coulomb sensitivity convention, readout/sign/q normalization | one convention maps to either DD e basis or alpha-Coulomb basis without mixing them | MISSING_FACTORIZED_SOURCE_LEG |
| IN3546_2_no_nonalpha_cancellation | residual isolation | mass/shadow/projector/readout terms are zero-owned or separately bounded with no cancellation credit | alpha-only pass cannot hide non-alpha residuals | MISSING_FULL_RESIDUAL_ENVELOPE |
| IN3546_3_readout_radiative_reentry | effective alpha branch | proof or finite row for clock/material/readout/radiative regeneration of alpha dependence | calibrated alpha baseline cannot be reused as a theorem-zero for loop/readout terms | MISSING_READOUT_STABILITY_PROOF |
| IN3546_4_public_claim_policy | claim hygiene | numeric parent value or theorem-zero plus sourced K_e_alpha projection and validation rows | valid_for_claim remains False until all rows are parent-owned and source-backed | CLAIM_BLOCK_RETAINED |

## Decisions

| decision_id | question | decision | basis | next_action |
| --- | --- | --- | --- | --- |
| DEC3546_0_value_found | Did 3546 find a sourced numeric K_e_alpha*b_alpha value? | NO | current corpus supplies exact alpha identities and numeric WEP ceilings, but no parent-owned b_alpha or factorized K_e_alpha | attempt parent same-owner zero proof for b_alpha, then source K_e_alpha if the proof fails |
| DEC3546_1_zero_route | Can the baseline set K_e_alpha*b_alpha=0? | YES_AS_CALIBRATED_BASELINE_ONLY | 3528 permits alpha_EM=alpha_0 as a calibrated local constant, like GR uses measured G_N | keep active nonzero alpha branches quarantined behind 3546 bound rows |
| DEC3546_2_finite_bound | Is there now a finite test gate for a future nonzero alpha product? | YES | DD e-basis gate is 1.372549e-12; alpha-Coulomb convention gate is 1.407170e-12 | do not merge the two conventions until alloy/material tensor policy is sourced |

## Validation

| validation_id | passes | status | detail |
| --- | --- | --- | --- |
| VAL3546_0_sources_exist | True | PASS | all source paths cited by the 3546 source register exist |
| VAL3546_1_generated_csvs_parse | True | PASS | 9 generated CSV files parse with DictReader |
| VAL3546_2_numeric_bounds_positive | True | PASS | all finite alpha product bound rows have positive numeric values |
| VAL3546_3_bounds_nonclaim | True | PASS | all alpha product bounds remain claim_allowed=False and valid_for_claim=False |
| VAL3546_4_formalization_workbench_untouched | True | PASS | 3546 generated outputs only inside post-checkpoint-work |
| VAL3546_5_claim_block_retained | True | PASS | no local-GR/WEP/alpha-source claim is made by this checkpoint |

## Next target

Move to `3547-Y5-R2FR-parent-EM-same-owner-zero-or-Ke-alpha-source-leg.md`: prove `2 z_g = z_lambda` from a single parent EM/current owner if possible; otherwise build the factorized `K_e_alpha` source leg so a future nonzero `b_alpha` can be scored rather than waved around.

Generated UTC: 2026-06-29T10:59:28.971970+00:00