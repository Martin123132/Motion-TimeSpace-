# 3851 - Fill First R_AB Gamma Projection Row Or Prove Phi-Floor Neutrality

Private checkpoint. This fills the first actual denominator/budget row for the 3850 `R_AB -> gamma` response, using the Cassini near-limb geometry as a nonclaim scalar proxy.

Generated: `2026-07-01T04:09:11+00:00`

## Result

Using the Cassini 2002 conjunction near-limb geometry:

`b_min = 1.6 R_sun_N = 1.113120000000000e+09 m`.

With IAU nominal `GM_sun_N`, IAU nominal `R_sun_N`, and exact SI `c`:

`phi_b=GM_sun_N/(c^2*b_min), b_min=1.6*R_sun_N = 1.326564106340848e-06`.

The local branch value is:

`T2_b = 1 - 2 phi_b = 9.999973468717873e-01`.

If all other gauge/domain/readout/kernel terms were zero, the Cassini `theta_gamma=2.3e-5` row would require:

`B_RAB_budget_zero_other=ln(1+2*phi_b*T2_b*theta_gamma) = 6.102178699076298e-11`.

So the practical message is sharp: finite `R_AB` hair is under roughly `6.1e-11` pressure in this near-limb gamma lane before any other residuals are paid. That makes the parent neutrality/no-hair proof the clean route; the finite-hair route now has a real number to beat.

This is not a claim. It is a sourced budget scout. A public or internal pass still needs real `B_RAB`, a full Cassini path-integrated Shapiro/radio kernel, and gauge/domain/normalization/no-slip/readout residual rows.

## Source Register

| source_id | source_type | path_or_url | exists_or_url_recorded | needle_found | role |
| --- | --- | --- | --- | --- | --- |
| SRC3851_L0_3850_response | local | source-intake\mts_residuals\P8_Y5_R2FR_3850_RAB_TO_GAMMA_RESPONSE_DERIVATION.csv | True | True | input_for_first_RAB_gamma_projection_row |
| SRC3851_L1_3850_contract | local | source-intake\mts_residuals\P8_Y5_R2FR_3850_GAMMA_BOUND_CONTRACT.csv | True | True | input_for_first_RAB_gamma_projection_row |
| SRC3851_L2_3850_input | local | source-intake\mts_residuals\P8_Y5_R2FR_3850_PPN_PROJECTION_INPUT_ROW.csv | True | True | input_for_first_RAB_gamma_projection_row |
| SRC3851_L3_3850_validation | local | source-intake\mts_residuals\P8_Y5_BRR545_3850_VALIDATION.csv | True | True | input_for_first_RAB_gamma_projection_row |
| SRC3851_L4_3849_hair | local | source-intake\mts_residuals\P8_Y5_R2FR_3849_RAB_HAIR_SOURCE_ROW.csv | True | True | input_for_first_RAB_gamma_projection_row |
| SRC3851_L5_3849_neutrality | local | source-intake\mts_residuals\P8_Y5_R2FR_3849_RECIPROCAL_NEUTRALITY_THEOREM.csv | True | True | input_for_first_RAB_gamma_projection_row |
| SRC3851_L6_local_gamma_bound | local | source-intake\local_bounds\local_bound_claims.csv | True | True | input_for_first_RAB_gamma_projection_row |
| SRC3851_W0_Cassini_bmin | web | https://pds-geosciences.wustl.edu/radiosciencedocs/urn-nasa-pds-radiosci_documentation/DOCUMENT/asmar.2014.pdf | True | True | external_provenance_for_constants_or_Cassini_geometry |
| SRC3851_W1_Cassini_gamma | web | https://www.nature.com/articles/nature01997 | True | True | external_provenance_for_constants_or_Cassini_geometry |
| SRC3851_W2_IAU_2015_B3 | web | https://www.iau.org/common/Uploaded%20files/IAUGA2015-Resolution-B3-recommended-nominal-conversion.pdf | True | True | external_provenance_for_constants_or_Cassini_geometry |
| SRC3851_W3_BIPM_c | web | https://www.bipm.org/documents/20126/41483022/SI-Brochure-9-EN.pdf | True | True | external_provenance_for_constants_or_Cassini_geometry |

## Geometry Constants

| constant_id | symbol | value | units | formula | status |
| --- | --- | --- | --- | --- | --- |
| CGC3851_0_bmin_factor | b_min/R_sun_N | 1.6 | dimensionless | Cassini 2002 conjunction minimum impact parameter | SOURCE_BACKED_CASSINI_GEOMETRY_INPUT |
| CGC3851_1_Rsun_nominal | R_sun_N | 6.957000000000000e+08 | m | IAU nominal solar radius | SOURCE_BACKED_NOMINAL_CONVERSION_CONSTANT |
| CGC3851_2_mu_sun_nominal | GM_sun_N | 1.327124400000000e+20 | m^3 s^-2 | IAU nominal solar mass parameter | SOURCE_BACKED_NOMINAL_CONVERSION_CONSTANT |
| CGC3851_3_c | c | 299792458 | m s^-1 | SI exact speed of light | SOURCE_BACKED_EXACT_SI_CONSTANT |
| CGC3851_4_bmin_m | b_min | 1.113120000000000e+09 | m | b_min=1.6*R_sun_N | DERIVED_GEOMETRY_INPUT |
| CGC3851_5_phi_b | phi_b | 1.326564106340848e-06 | dimensionless | phi_b=GM_sun_N/(c^2*b_min), b_min=1.6*R_sun_N | DERIVED_NEAR_LIMB_DENOMINATOR_INPUT |
| CGC3851_6_T2_b | T2_b | 9.999973468717873e-01 | dimensionless | T2_b=1-2*phi_b | DERIVED_NEAR_LIMB_BRANCH_INPUT |

## First Projection Rows

| projection_id | arena | phi_floor | T2_floor | B_RAB_budget_if_B_other_zero | status |
| --- | --- | --- | --- | --- | --- |
| PPR3851_0_Cassini_near_limb_RAB_row | Cassini_Shapiro_gamma_2003_near_limb_scalar_proxy | 1.326564106340848e-06 | 9.999973468717873e-01 | 6.102178699076298e-11 | PARTIAL_NUMERIC_DENOMINATOR_FILLED_B_RAB_AND_KERNEL_MISSING |
| PPR3851_1_parent_neutrality_zero_route | local_exterior_neutrality_branch | not_needed_if_B_RAB_zero | 9.999973468717873e-01 | 0 contribution if Pi_R=J_R=Pi_R_ct=Delta_R_boundary=Delta_W=0 | BEST_ROUTE_BUT_PARENT_SIGNATURE_UNSIGNED |

## R_AB Budget

| budget_id | formula | input_phi_b | input_T2_b | exact_log_bound | status |
| --- | --- | --- | --- | --- | --- |
| RBC3851_0_near_limb_scalar_budget | B_RAB_budget_zero_other=ln(1+2*phi_b*T2_b*theta_gamma) | 1.326564106340848e-06 | 9.999973468717873e-01 | 6.102178699076298e-11 | NUMERIC_PRESSURE_RESULT_NONCLAIM |
| RBC3851_1_with_other_terms | B_RAB <= ln(1+2*phi_b*T2_b*(theta_gamma-B_other)) | 1.326564106340848e-06 | 9.999973468717873e-01 | requires theta_gamma>B_other | STRICTER_IF_OTHER_TERMS_NONZERO |

## Neutrality Versus Finite Hair

| decision_id | route | required_new_input | current_status | route_score |
| --- | --- | --- | --- | --- |
| NFD3851_0_finite_hair_pressure | finite R_AB hair | source-backed B_RAB <= 6.102178699076298e-11 plus full Cassini kernel/gauge/domain terms | NOT_FILLED | hard_but_now_quantified |
| NFD3851_1_neutrality_zero_pressure | parent reciprocal neutrality | prove Pi_R=J_R=Pi_R_ct=Delta_R_boundary=Delta_W=0 on the exterior source branch | UNSIGNED_BUT_BEST_ROUTE | mathematically_preferred_after_6e-11_budget |

## Claim Gates

| gate_id | status | claim_allowed | reason |
| --- | --- | --- | --- |
| GATE3851_0_geometry_constants | PASS_SOURCE_STRINGS_AND_DERIVED_VALUES_RECORDED | False | b_min, R_sun_N, GM_sun_N, c, phi_b, and T2_b are recorded with provenance |
| GATE3851_1_numeric_RAB_budget | PASS_NONCLAIM_NUMERIC_PRESSURE_ROW | False | zero-other-term near-limb budget is about 6.1e-11 |
| GATE3851_2_B_RAB_source | BLOCKED_MISSING_B_RAB_OR_PARENT_NEUTRALITY | False | 3849 hair row still has no source-backed numeric B_RAB and no parent zero signature |
| GATE3851_3_Cassini_kernel | BLOCKED_NEAR_LIMB_PROXY_NOT_FULL_KERNEL | False | a claim needs the path-integrated Shapiro/radio observable, not only a near-limb scalar denominator |
| GATE3851_4_scope_guard | BLOCKED_GAMMA_COMPONENT_ONLY | False | Newton/source normalization, beta, no-slip/readout, and EM/source coupling remain separate gates |

## Decisions

| decision_id | decision | consequence |
| --- | --- | --- |
| DEC3851_0 | finite R_AB hair is numerically under severe Cassini pressure | without a theorem zero, the source row must deliver B_RAB at roughly 1e-10 or below before other residuals |
| DEC3851_1 | the best physics route is now the parent neutrality/no-hair proof | trying to carry finite reciprocal hair through PPN is possible but likely ugly and very constrained |
| DEC3851_2 | do not overclaim the numeric row | near-limb scalar denominator is a budget scout; full Cassini kernel projection remains a later empirical gate |

## Bottom Line

This checkpoint stops the circling and puts a number on the local gamma throat. If MTS keeps finite reciprocal hair, it must be tiny in the solar-system lane. The better route is to derive the `R_AB=0` exterior neutrality result from the parent action, then use finite rows only as fallback.

Next target: `3852-Y5-R2FR-parent-neutrality-signature-for-RAB-zero-or-finite-hair-source-row.md`.
