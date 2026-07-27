# 3208 - Htau One-Form Exactness Or First DeltaH Curl Bound Under AX1090

Private checkpoint. This is not a local-GR claim, Newtonian-limit claim, PPN pass, R10 pass, clock pass, orbital pass, Bobs residual score, `H_tau` exactness claim, `M_H_ref` claim, or public-facing result.

## Result

3208 derives the exact curl criterion and adds the finite-curl escape hatch.

The useful advance is not that `H_tau` is now proved exact. It is not. The advance is:

```text
alpha_tau(delta Phi) = int_S(delta Q_tau^MTS - i_tau Theta_MTS(delta Phi)) - delta H_ref
d_F alpha_tau(delta1,delta2) = - int_S i_tau omega_MTS(delta1,delta2)
                              + C_tau + C_S + C_ref

if d_F alpha_tau = 0, H_tau is path-independent.
if not, |Delta H_tau(path1)-Delta H_tau(path2)| <= int_BF |d_F alpha_tau|.
```

So nonzero curl is not automatically hand-waving death. It can become a bounded residual:

```text
epsilon_Htau_curl = Delta_H_curl_bound / (G_ref M_EH)
```

and then feed the `epsilon_abs` denominator lower-bound route from 3207.

Current verdict:

```text
H_tau exactness: not proved.
Delta_H_curl finite value: not sourced.
Bobs/local-GR/Newton scoring: still refused.
New route: source or theorem-zero the X-sector omega term and reference-curl term first.
```

## Curl Law

| law_id | object | formula | derivation | claim_status | missing_for_claim | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| HCL3208_0_one_form | alpha_tau | alpha_tau(delta Phi)=int_S(delta Q_tau^MTS - i_tau Theta_MTS(delta Phi)) - delta H_ref | definition of the Hamiltonian variation one-form on a fixed branch | conditional_definition | parent Theta_MTS;Q_tau_MTS;tau_id;surface_pair;fixed_H_ref | false |
| HCL3208_1_field_space_curl_fixed_branch | d_F alpha_tau | d_F alpha_tau(delta1,delta2) = - int_S i_tau omega_MTS(delta1,delta2) when tau,S,H_ref are fixed branch data | d_F(delta Q_tau)=0 and omega_MTS=d_F Theta_MTS; sign is irrelevant for absolute bounds | derived_identity | omega_MTS by sector; fixed branch certificate; boundary pullback units | false |
| HCL3208_2_moving_branch_corrections | C_tau+C_S+C_ref | d_F alpha_tau = -int_S i_tau omega_MTS + C_tau + C_S + C_ref if tau, surface class, or reference selector varies | field-dependent generator/surface/reference add explicit curl terms rather than being hidden in H_tau | derived_accounting_rule | delta_tau;delta_surface;reference_selector_derivative source rows | false |
| HCL3208_3_exact_route | H_tau exactness | H_tau exists as a state function if d_F alpha_tau=0 on the allowed local branch | closed one-form criterion | not_satisfied_current_corpus | all curl components theorem-zero in one parent branch | false |
| HCL3208_4_bound_route | Delta_H_curl | if two field-space paths enclose B_F, |Delta H_tau(path1)-Delta H_tau(path2)| <= int_{B_F}|d_F alpha_tau| <= A_F sup_{B_F}|d_F alpha_tau| | field-space Stokes bound; nonzero curl becomes a no-cancellation denominator residual | new_bound_route_derived_no_values | field-space area A_F; component sup bounds; norm convention; source paths | false |
| HCL3208_5_epsilon_feed | epsilon_Htau_curl | epsilon_Htau_curl := Delta_H_curl_bound/(G_ref M_EH) feeds epsilon_abs from 3207 | normalizes path-dependence by the same non-orbital comparator used for the denominator lower-bound law | feed_schema_only | Delta_H_curl_bound;G_ref;M_EH | false |

## Curl Components

| component_id | component | definition | zero_or_bound_condition | current_status | feeds | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| HCURL3208_0_EH_stationary | I_EH_stationary_boundary | abs(int_S i_tau omega_EH(delta1,delta2)) | fixed stationary EH exterior branch with standard boundary conditions | CONDITIONAL_REFERENCE_ONLY_NOT_MTS_PROOF | Delta_H_curl_bound | false |
| HCURL3208_1_X_sector | I_X_symplectic | abs(int_S i_tau omega_X(delta1,delta2)) | L_X/Theta_X/omega_X parent-owned and boundary pullback zero/exact/bounded | MISSING_LX_THETA_OMEGA_OWNER | Delta_H_curl_bound;epsilon_abs | false |
| HCURL3208_2_boundary_flux | I_boundary_corner_edge | abs(boundary/corner/edge contribution to d_F alpha_tau) | boundary class exact/proper/no-hair or source-backed finite flux | MISSING_BOUNDARY_EXACTNESS_OR_BOUND | Delta_H_curl_bound;Bobs boundary/corner rows | false |
| HCURL3208_3_projector_domain | I_projector_domain_stress | abs(delta Pi_M, P_loc, domain, normal, Hodge/Green variation contribution) | projector/domain is parent-fixed or finite commutator/stress bound is sourced | MISSING_PROJECTOR_STRESS_MAP | Delta_H_curl_bound;Bobs projector row | false |
| HCURL3208_4_reference | I_ref | abs(C_ref) from moving H_ref/reference selector or reference curl | H_ref fixed before source/readout and derivative-silent, or explicit reference-curl bound | MISSING_FIXED_REFERENCE_LOCK_OR_BOUND | Delta_H_curl_bound;Delta_ref | false |
| HCURL3208_5_tau_surface | I_tau_surface | abs(C_tau+C_S) from tau generator or linking surface variation | same tau and surface homology class are fixed before readout or finite mismatch bound is sourced | MISSING_TAU_SURFACE_VARIATION_LOCK | Delta_H_curl_bound;tau_ref_surface_mismatch | false |
| HCURL3208_6_observed_source_flux | I_observed_source_measure | abs(P_loc B_source/B_boundary/B_bulk contribution to d_F alpha_tau) | observed reduced Ward/no-flux theorem or componentwise source-backed Bobs rows | MISSING_OBSERVED_REDUCED_FLUX_ZERO_OR_BOUND | Delta_H_curl_bound;Bobs source/bulk rows | false |
| HCURL3208_7_total | Delta_H_curl_bound | A_F times the absolute sum/supremum of all live curl components; no cancellation credit | every component theorem-zero or source-backed finite in shared units and norm | NOT_COMPUTED_COMPONENTS_MISSING | epsilon_Htau_curl;epsilon_abs;M_H_ref lower-bound route | false |

## Field-Space Path Bound

| row_id | route | required_statement | output_if_passes | current_value | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| PB3208_0_exact_zero | exact_integrability | d_F alpha_tau=0 for all allowed field variations on the branch | Delta_H_curl_bound=0 and H_tau is path-independent | MISSING_EXACT_ZERO_CERTIFICATE | false |
| PB3208_1_finite_bound | bounded_nonintegrability | Delta_H_curl_bound <= integral_BF |d_F alpha_tau| | finite path-dependence residual can feed epsilon_abs without pretending H_tau is exact | MISSING_COMPONENT_BOUNDS_AND_FIELD_SPACE_AREA | false |
| PB3208_2_first_fill | first_component_acquisition | source the reference-curl and X-sector omega terms first because they block both exactness and finite bound routes | first nonzero piece of Delta_H_curl_bound becomes evaluable | SOURCE_READY_NONCLAIM_TEMPLATE | false |

## Exactness Or Bound Gates

| gate_id | gate | pass | status | valid_for_claim |
| --- | --- | --- | --- | --- |
| G3208_0_parent_current | Theta_MTS and Q_tau_MTS come from one parent variation | false | MISSING_PARENT_THETA_QTAU | false |
| G3208_1_fixed_branch | tau, surface pair, source worldtube, and reference are fixed before readout | false | MISSING_FIXED_BRANCH_CERTIFICATE | false |
| G3208_2_curl_identity | field-space curl identity is written with all correction terms explicit | true | DERIVED_IDENTITY_PRESENT | false |
| G3208_3_exact_zero | d_F alpha_tau theorem-zero is proved | false | ZERO_NOT_PROVED | false |
| G3208_4_finite_bound | Delta_H_curl_bound has finite source-backed value | false | BOUND_ROWS_MISSING | false |
| G3208_5_no_cancellation | no cancellation between curl/reference/projector/boundary components is used | true | NO_CANCELLATION_POLICY_ACTIVE | false |
| G3208_6_epsilon_feed | epsilon_Htau_curl can feed epsilon_abs | false | FEED_SCHEMA_ONLY_VALUES_MISSING | false |
| G3208_7_claim_status | H_tau/M_H_ref/Bobs/local-GR branch can score | false | CLAIM_BLOCKED_CURRENT_CORPUS | false |

## Epsilon Feed

| feed_id | epsilon_abs_component | definition | current_status | feeds | claim_effect | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| EF3208_0_Delta_H_curl | epsilon_Htau_curl | Delta_H_curl_bound/(G_ref*M_EH) | MISSING_VALUES | LAW3207_3_positive_lower_bound | if finite and small, contributes to denominator lower-bound instead of blocking by wording alone | false |
| EF3208_1_exact_zero_case | epsilon_Htau_curl | 0 if d_F alpha_tau=0 theorem is parent-signed | ZERO_CASE_NOT_PROVED | exact M_H_ref route | H_tau becomes a legal state function but positivity still needs M_H_ref/G_ref/source rows | false |

## Decision

`HTAU_CURL_IDENTITY_AND_STOKES_BOUND_DERIVED_NO_VALUES`.

Claim status: `NO_HTAU_EXACTNESS_NO_MHREF_NO_BOBS_SCORE_NO_LOCAL_GR_CLAIM`.

Best next route: derive/source HCURL3208_1_X_sector omega bound or HCURL3208_4_reference fixed-reference curl bound first.

Next target:

```text
3209-Y5-R2FR-X-sector-Theta-omega-owner-or-reference-curl-bound-first-row-under-AX1090
```

## Generated Evidence

- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3208_INPUTS.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3208_HTAU_ONE_FORM_CURL_LAW.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3208_CURL_COMPONENT_ENVELOPE.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3208_FIELD_SPACE_PATH_BOUND_TEMPLATE.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3208_EXACTNESS_OR_BOUND_GATES.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3208_EPSILON_ABS_FEED.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3208_DECISION.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3208_VALIDATION.csv`

## Validation

| check_id | pass | detail |
| --- | --- | --- |
| VAL3208_00_inputs_exist | true | inputs=10 |
| VAL3208_01_curl_identity | true | d_F alpha_tau = -int_S i_tau omega_MTS for fixed branch |
| VAL3208_02_stokes_bound | true | path ambiguity bounded by integral of |d_F alpha_tau| |
| VAL3208_03_component_envelope | true | component_rows=8 |
| VAL3208_04_claims_blocked | true | no exact-zero or finite bound rows are sourced |
| VAL3208_05_no_cancellation | true | component bounds must be absolute, not cancelling |
| VAL3208_06_epsilon_feed_nonclaim | true | epsilon_feed_rows=2 |
| VAL3208_07_next_target | true | 3209-Y5-R2FR-X-sector-Theta-omega-owner-or-reference-curl-bound-first-row-under-AX1090 |
| VAL3208_08_no_formalization_workbench_edit | true | no formalization-workbench paths are output targets |
| VAL3208_09_csv_parse | true | P8_Y5_R2FR_3208_INPUTS.csv;P8_Y5_R2FR_3208_HTAU_ONE_FORM_CURL_LAW.csv;P8_Y5_R2FR_3208_CURL_COMPONENT_ENVELOPE.csv;P8_Y5_R2FR_3208_FIELD_SPACE_PATH_BOUND_TEMPLATE.csv;P8_Y5_R2FR_3208_EXACTNESS_OR_BOUND_GATES.csv;P8_Y5_R2FR_3208_EPSILON_ABS_FEED.csv;P8_Y5_R2FR_3208_DECISION.csv |

All generated rows remain `valid_for_claim=false`.
