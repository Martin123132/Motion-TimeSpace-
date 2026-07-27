# 3212 - EM Source Channel: No-Extra-F2 Or Poynting Bound Input under AX1090

Private checkpoint. This is not a local-GR claim, Newtonian-limit claim, Maxwell derivation claim, PPN pass, R10 pass, WEP pass, clock pass, `b_alpha=0` claim, `J_EM=0` claim, `J_X=0` claim, or public-facing result.

## Result

3212 derives the actual EM source law feeding the `3211` coupling equation:

```text
S_EM = -1/4 int mu Z_A(X) F^2
       -1/4 int mu Theta_A(X) F*F
       + S_Hodge[g_obs(X),A]
       + S_boundary_flux.
```

Therefore:

```text
J_X^EM = 1/4 Z_A'(X) F^2
       + 1/4 Theta_A'(X) F*F
       - 1/2 T_EM^(mu nu) partial_X g_obs,mu nu
       + J_readout/radiative.
```

and the finite no-cancellation envelope is:

```text
||J_EM||_2 <= 1/4 Z_A0 |b_alpha| ||F^2||_2
            + 1/4 |Theta_A'| ||F*F||_2
            + 1/2 ||C_Hodge T_EM||_2
            + ||J_readout/radiative||_2.
```

Poynting remains a boundary/worldtube flux:

```text
|Phi_Poynting| <= C_Poynting int_boundary |n_i T_EM^(0i)| dS dt.
```

Clean zero route:

```text
fixed T_Q/gauge norm
+ no independent lambda_A F^2 or f_X(X)F^2
+ no radiative/readout alpha re-entry
+ Hodge/metric descent
+ Poynting boundary silence
=> J_EM = 0 and Phi_Poynting = 0.
```

Current verdict: that theorem is not signed in the present corpus. The EM channel is therefore not dead, but it is now a finite source/bound problem rather than a foggy coupling problem.

## EM Variation Law

| law_id | object | formula | derived_result | status | missing_for_claim | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| EMV3212_0_parent_decomposition | S_EM[X,A,g] | S_EM = -1/4 int mu Z_A(X) F^2 - 1/4 int mu Theta_A(X) F*F + S_Hodge[g_obs(X),A] + S_boundary_flux | this is the minimal EM source decomposition: gauge-kinetic scalar, dual/topological scalar, metric/Hodge stress, and boundary/Poynting flux | decomposition_derived_not_parent_selected | parent EM action domain;Z_A owner;Theta_A owner;Hodge descent;boundary flux rule | false |
| EMV3212_1_bulk_variation | J_X^EM_bulk | J_X^EM = (1/4)Z_A'(X)F^2 + (1/4)Theta_A'(X)F*F - (1/2)T_EM^{mu nu} partial_X g_obs,mu nu + J_readout/radiative | bulk EM source is zero only if every derivative term is theorem-zero or the relevant field invariant vanishes on support | source_formula_derived | b_alpha=0;Theta_A'=0;Hodge/metric descent;readout closure;field support norms | false |
| EMV3212_2_F2_bound | J_F2_bound | \|\|J_F2\|\|_2 <= (1/4) Z_A0 \|b_alpha\| \|\|F^2\|\|_2, where b_alpha=partial_X ln Z_A at the local branch | finite b_alpha immediately becomes a source norm input for the 3210 amplitude law | bound_formula_derived_values_missing | Z_A0;b_alpha;F2_norm;support;units;source_path | false |
| EMV3212_3_dual_bound | J_FstarF_bound | \|\|J_dual\|\|_2 <= (1/4)\|Theta_A'\| \|\|F*F\|\|_2 | CP/topological EM invariant must be absent, constant, or bounded; it cannot be hidden inside F2 silence | bound_formula_derived_values_missing | Theta_A' theorem-zero or numeric bound;FstarF_norm;topological sector rule | false |
| EMV3212_4_Hodge_bound | J_Hodge_bound | \|\|J_Hodge\|\|_2 <= (1/2)\|\|C_Hodge T_EM\|\|_2 with C_Hodge := partial_X g_obs or partial_X star_obs in the EM sector | if the observed Hodge star descends through q, this term is zero; otherwise it is an EM stress-source coefficient | bound_formula_derived_values_missing | Hodge descent theorem or C_Hodge bound;EM stress norm | false |
| EMV3212_5_total_EM_bound | J_EM_bound_abs | \|\|J_EM\|\|_2 <= \|\|J_F2\|\|_2 + \|\|J_dual\|\|_2 + \|\|J_Hodge\|\|_2 + \|\|J_readout/radiative\|\|_2 | the EM contribution to J_X is now a no-cancellation absolute envelope | envelope_derived_values_missing | all component values or theorem-zero certificates | false |

## No-Extra-F2 Theorem Gates

| gate_id | gate | required_condition | current_status | if_pass | if_fail | pass | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| F2G3212_0_fixed_TQ_norm | parent T_Q and gauge norm fixed | T_Q, charge lattice, C_P, and <T_Q,T_Q>_P are parent-owned and nonrescalable | not_parent_signed_by_1100_1101 | parent contribution to Z_A is X-silent | b_alpha remains a finite coefficient | false | false |
| F2G3212_1_no_independent_F2 | no lambda_A F^2 or f_X(X)F^2 operator | operator-domain exhaustion, product/sequester functor, exact shift symmetry, or equivalent parent ban | failed_current_claim_by_1099_1048_1109 | Z_A'(X)=0 at tree level | J_F2=(1/4)Z_A0 b_alpha F^2 is live | false | false |
| F2G3212_2_radiative_readout | no radiative/readout alpha re-entry | effective/readout alpha remains a function only of q plus fixed representation data | unsigned_by_1099_1100 | tree-level silence survives clocks/spectra | J_readout/radiative and b_alpha product rows remain live | false | false |
| F2G3212_3_Hodge_descent | EM Hodge star/metric descends through q | partial_X g_obs=0 or partial_X star_obs=0 on EM support, including disformal/stress channels | not_signed_in_current_chain | J_Hodge=0 and Maxwell trace silence applies to pure conformal channel | EM stress/Hodge source must be bounded | false | false |
| F2G3212_4_boundary_Poynting_silence | Poynting/worldtube flux silent | closed stationary surface, no radiative energy flux, exact/proper boundary term, or projector orthogonality | new_gate_values_missing | Phi_Poynting=0 | Phi_Poynting bound feeds 3210 b_X | false | false |
| F2G3212_5_total_EM_zero | J_EM=0 and Phi_Poynting=0 | F2G3212_0 through F2G3212_4 all pass on the same parent branch | not_claim_ready | EM channel no longer sources local X amplitude | use finite EM source and flux bound rows | false | false |

## Finite EM Bound Inputs

| row_id | quantity | definition | required_value_or_bound | current_value | feeds | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| FEB3212_0_balpha | b_alpha | partial_X ln Z_A or vertical derivative of ln alpha_EM in the EM gauge-kinetic channel | 0 by no-extra-F2 theorem or finite sourced bound | MISSING_B_ALPHA_OR_PARENT_ZERO_THEOREM | J_F2_bound;clock/WEP/R10 alpha rows | false |
| FEB3212_1_F2_norm | \|\|F^2\|\|_2 | L2 norm of the Maxwell invariant on the local EM support used by the X branch | finite norm with surface/worldtube/support and units | MISSING_F2_SUPPORT_NORM | J_F2_bound | false |
| FEB3212_2_dual | Theta_A_prime and \|\|F*F\|\|_2 | dual/topological EM invariant source slot | theorem-zero or finite bound | MISSING_DUAL_CHANNEL_POLICY | J_dual_bound | false |
| FEB3212_3_Hodge | C_Hodge and \|\|T_EM\|\|_2 | EM stress/Hodge source coefficient and stress norm | Hodge descent theorem or finite stress-coupling bound | MISSING_HODGE_STRESS_BOUND | J_Hodge_bound | false |
| FEB3212_4_Poynting | C_Poynting and flux_integral | boundary/worldtube energy-flow coupling and integral of \|n_i T_EM^{0i}\| | zero by stationary/no-flux theorem or finite sourced bound | MISSING_POYNTING_BOUND_INPUTS | Phi_boundary;3210 b_X | false |
| FEB3212_5_total | J_EM_bound_abs | absolute no-cancellation EM contribution to \|\|J_X\|\|_2 | sum of FEB3212_0 through FEB3212_3, plus readout/radiative if open | NOT_COMPUTED_COMPONENTS_MISSING | 3211 J_norm_bound_abs;3210 a_X | false |

## Poynting Case Split

| case_id | case | F2_status | Poynting_status | lesson | claim_status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| POY3212_0_static_Coulomb | static electrostatic source | F^2 generally nonzero | T_EM^{0i}=0 if B=0 and fields stationary | static fields are F2-active but Poynting-silent | case_split_only_not_source_data | false |
| POY3212_1_null_wave | ideal null EM wave | F^2=0 and F*F=0 | T_EM^{0i} nonzero | radiation can be F2-silent but boundary/stress active | case_split_only_not_source_data | false |
| POY3212_2_stationary_closed_exterior | closed stationary local exterior with no radiative flux crossing boundary | depends on local Coulomb/magnetic field support | Phi_Poynting=0 if n_i T_EM^{0i}=0 on boundary and boundary rule is proper/exact | this is the clean zero route for Poynting, but it needs a parent boundary/domain rule | conditional_zero_route_unsigned | false |
| POY3212_3_general_lab_wave | lab/radiative EM configuration | may be zero or nonzero depending on polarization/near fields | finite flux must be bounded by C_Poynting int \|n_i T_EM^{0i}\| | do not use F2=0 to claim no EM source unless boundary/stress channel is also silent | finite_bound_route_values_missing | false |

## Feed To 3211/3210

| feed_id | target | feed_formula | current_status | claim_effect | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| EF3212_0_to_3211_Jnorm | FJB3211_0_abs_J_norm | replace EM term by J_EM_bound_abs = J_F2_bound + J_dual_bound + J_Hodge_bound + J_readout/radiative_bound | formula_ready_values_missing | EM source contribution becomes finite and absolute if inputs are sourced | false |
| EF3212_1_to_3211_Phi | FJB3211_1_abs_Phi_Poynting | Phi_Poynting_bound_abs = C_Poynting int_boundary \|n_i T_EM^{0i}\| dS dt | formula_ready_values_missing | Poynting becomes a boundary amplitude input, not a loose analogy | false |
| EF3212_2_to_3210_zero | AMP3210_5_zero_limit | if J_EM_bound_abs=0 and Phi_Poynting_bound_abs=0 by parent theorem, EM does not obstruct X=0 | conditional_zero_route_not_signed | would remove the EM source contribution from the local no-hair gate | false |
| EF3212_3_to_empirical | clock/WEP/R10/PPN EM rows | if b_alpha or Hodge/Poynting coefficients are finite, map them to alpha/source/readout residual rows with no cancellation | finite_residual_route_selected_if_zero_fails | empirical route requires coefficient provenance and field/support norms | false |

## Decision

`EM_SOURCE_VARIATION_AND_POYNTING_BOUND_DERIVED_NO_EXTRA_F2_NOT_PROVED`.

Claim status: `NO_B_ALPHA_ZERO_NO_JEM_ZERO_NO_LOCAL_GR_CLAIM`.

Best next route: try the strongest derivation left: product/sequester or exact-shift theorem for hidden-visible coefficient maps; if it fails, build coefficient provenance for b_alpha and Hodge/Poynting bounds.

Next target:

```text
3213-Y5-R2FR-hidden-visible-product-sequester-or-balpha-Hodge-Poynting-provenance-pack-under-AX1090
```

## Generated Evidence

- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3212_INPUTS.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3212_EM_SOURCE_VARIATION_LAW.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3212_NO_EXTRA_F2_THEOREM_GATES.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3212_FINITE_EM_BOUND_INPUT_ROWS.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3212_POYNTING_CASE_SPLIT.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3212_SOURCE_FEED_TO_3211_3210.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3212_DECISION.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3212_VALIDATION.csv`

## Validation

| check_id | pass | detail |
| --- | --- | --- |
| VAL3212_00_inputs_exist | true | inputs=10 |
| VAL3212_01_variation_law | true | J_EM includes F2, F*F, Hodge/stress, readout/radiative |
| VAL3212_02_no_extra_F2_gates | true | TQ norm;no independent F2;radiative;Hodge;Poynting;total |
| VAL3212_03_finite_inputs | true | b_alpha;F2;dual;Hodge;Poynting;total |
| VAL3212_04_poynting_cases | true | static;null wave;closed exterior;general wave |
| VAL3212_05_feeds_3211_3210 | true | J_EM_bound_abs and Phi_Poynting feed rows exist |
| VAL3212_06_claims_blocked | true | claim_rows_true=0 |
| VAL3212_07_no_formalization_workbench_edit | true | no formalization-workbench paths are output targets |
| VAL3212_08_csv_parse | true | P8_Y5_R2FR_3212_INPUTS.csv;P8_Y5_R2FR_3212_EM_SOURCE_VARIATION_LAW.csv;P8_Y5_R2FR_3212_NO_EXTRA_F2_THEOREM_GATES.csv;P8_Y5_R2FR_3212_FINITE_EM_BOUND_INPUT_ROWS.csv;P8_Y5_R2FR_3212_POYNTING_CASE_SPLIT.csv;P8_Y5_R2FR_3212_SOURCE_FEED_TO_3211_3210.csv;P8_Y5_R2FR_3212_DECISION.csv |

All generated rows remain `valid_for_claim=false`.
