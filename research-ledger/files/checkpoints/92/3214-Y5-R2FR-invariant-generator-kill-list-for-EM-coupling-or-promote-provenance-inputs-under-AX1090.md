# 3214 - Invariant Generator Kill List For EM Coupling Or Provenance Promotion under AX1090

Private checkpoint. This is not a local-GR claim, Maxwell derivation claim, Newtonian-limit claim, WEP pass, R10 pass, clock pass, `b_alpha=0` claim, or public-facing result.

## Result

3214 makes a real narrowing move.

The target is not now "kill every hidden invariant or give up." The exact condition is sharper:

```text
For hidden generators I_a and visible coefficient vector
C_vis = (ln Z_A, Theta_A, g_obs, C_boundary, C_readout, m_A, kappa_A),

L_X C_vis =
    sum_a (partial C_vis / partial I_a) L_X I_a
    + explicit_hidden_slot.
```

Therefore hidden-visible coupling is killed if the visible coefficient Jacobian annihilates the vertical generator velocity:

```text
J_C(I) . L_X I = 0
```

This can happen by full invariant-algebra triviality, but it can also happen by a weaker typed/coefficient-kernel theorem. That is a useful escape hatch: MTS does not have to erase every possible label; it has to prove those labels cannot move the visible EM/matter/source coefficients on the local branch.

The useful win:

```text
fixed discrete/spectral/domain labels
    -> dI = 0 on a connected no-wall local branch
    -> no smooth bulk EM source from those labels
```

The bad news, kept honest:

```text
continuous memory/class scalars,
readout/radiative scalar slots,
boundary/Poynting flux weights,
and species source-weight constants
still survive unless separately derived or bounded.
```

## Invariant Coupling Criterion

| criterion_id | claim_piece | formal_statement | derivation_status | consequence | required_for_claim | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| CRIT3214_0_vertical_derivative_decomposition | exact generator projection of hidden-visible coupling | For hidden generators I_a and visible coefficient vector C_vis=(ln Z_A,Theta_A,g_obs,C_boundary,C_readout,m_A,kappa_A), L_X C_vis = sum_a (partial C_vis/partial I_a) L_X I_a + explicit_hidden_slot. | EXACT_CHAIN_RULE_IDENTITY | EM/local source silence does not require all hidden invariants to be absent; it requires the visible coefficient Jacobian to annihilate the vertical generator velocity. | parent-owned list of I_a, coefficient target grammar, and proof that no explicit hidden slot exists | false |
| CRIT3214_1_zero_condition | minimal zero condition for EM coupling | J_X^EM=0 for bulk EM if for every generator I_a either L_X I_a=0 or partial_Ia(ln Z_A,Theta_A,g_obs/readout)=0, and if boundary/readout flux maps have the same annihilation property. | CONDITIONAL_THEOREM | This is weaker than full invariant algebra triviality and stronger than hand-waving sequester: it gives a checkable kernel condition. | same-branch proof for all bulk, boundary, and radiative/readout coefficient maps | false |
| CRIT3214_2_bulk_discrete_generator_result | discrete generators cannot create local bulk derivative inside a connected fixed branch | If I_a takes values in a discrete set and the local branch is connected with no wall crossing, then dI_a=0 and L_X I_a=0 on that branch. | EXACT_TOPOLOGICAL_CONDITIONAL | finite-cell spectrum, fixed domain class, and branch labels can be removed from the differential EM bulk source but may remain as fixed constants, jump data, or boundary/selection debt. | connected fixed-branch theorem and explicit no-wall/no-selector clause | false |
| CRIT3214_3_continuous_generator_result | continuous scalar generators remain dangerous | If I_a is smooth, nonconstant, and partial_Ia C_vis is not parent-forbidden, then L_X C_vis can be nonzero and the 3213 countertheorem survives. | COUNTERTHEOREM_RETAINED | memory/class scalar and radiative/readout scalar slots remain the real bulk-coupling enemies. | positive nohair, exact shift/product typing, or finite empirical coefficient bound | false |
| CRIT3214_4_finite_fallback_condition | if zero proof fails, source becomes bounded not claimed absent | \|J_X^EM\| <= sum_a \|L_X I_a\| \|partial_Ia C_vis\| \|O_vis\| + boundary/readout flux terms. | ABSOLUTE_VALUE_BOUND | surviving generators can feed 3210 amplitude law as a finite source rather than forcing a dead end. | numeric/source-backed generator amplitudes, coefficient derivatives, field norms, support surfaces, and units | false |

## Generator Kill List

| generator_id | generator | type | bulk_EM_derivative_status | proof_move | what_remains | next_requirement | survives_as_bulk_EM_source | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| GK3214_0_finite_cell_spectrum | finite_cell_fibre_spectrum | discrete_or_spectral_label | conditionally_killed_on_connected_fixed_branch | discrete locally constant theorem: no wall crossing gives L_X I=0 | fixed-sector constants, thresholds, or branch jumps can still affect source normalization and WEP/local bounds | write connected fixed-cell branch clause or keep finite-cell jumps as boundary/source priors | false_if_branch_signed_else_unknown | false |
| GK3214_1_relative_domain_class | relative_boundary_domain_class | discrete_topological_domain_label | conditionally_killed_in_domain_interior | fixed topological class has zero local derivative; variations changing class are boundary/domain-wall events, not smooth bulk X | boundary functor and domain-wall flux can still feed C_Poynting or local projection leakage | separate smooth local interior from boundary/domain transition sector | false_if_interior_branch_signed_else_boundary_survives | false |
| GK3214_2_domain_selector | domain_selector_chi_D | idempotent_projector | killed_only_if_selector_is_fixed_before_variation | chi_D^2=chi_D implies values are discrete; connected branch gives d chi_D=0, but post-variation selector is a readout/projection source | if selector acts after variation it re-enters as reduced-action/readout debt | parent variation-before-readout theorem plus no post-readout EFT backreaction | unknown_until_readout_order_signed | false |
| GK3214_3_memory_class_scalar | memory_or_class_scalar | continuous_scalar | survives | cannot be killed by connectedness; needs positive nohair/source-silence or exact typed coefficient exclusion | can feed b_alpha, clock drift, Hodge coefficient drift, gamma shift, or finite fifth-force source | derive local memory nohair equation with signed mass/source/boundary terms, or promote b_memory_to_alpha finite bound | true_until_nohair_or_typing_signed | false |
| GK3214_4_orientation_time_arrow | orientation_time_arrow | discrete_orientation_or_continuous_clock_marker | split | if it is only time orientation/coframe sign, it is fixed discrete structure; if it is a continuous clock-arrow scalar, it survives | preferred-frame, parity/time-asymmetry, clock, or FstarF channel | classify as coframe-owned discrete orientation versus continuous hidden scalar | false_for_fixed_orientation_true_for_clock_scalar | false |
| GK3214_5_species_constants | species_charge_constants | constant_sector_label | not_a_vertical_derivative_source_if_constant | L_X kappa_A=0 if species constants are truly constant and not hidden-coordinate functions | nonuniversal constants still violate WEP/source coupling even when they do not generate b_alpha source | universal Hilbert source theorem or explicit source-coupling bound rows | false_as_derivative_true_as_WEP_source_debt | false |
| GK3214_6_readout_projector | readout_projector | procedure_or_reduced_action_projector | not_killed_by_geometry_alone | if readout happens after parent variation and is not fed back into S_eff, no source; if it is varied as reduced action, source re-enters | alpha/clock/readout coefficients can be manufactured after the bare product theorem | readout-after-variation theorem plus radiative closure | unknown_until_readout_closure_signed | false |
| GK3214_7_boundary_flux_weight | boundary_or_worldtube_flux_weight | boundary_functional | not_bulk_but_survives_boundary | bulk F2 silence does not control surface term delta_X int_boundary C(I)n_i T_EM^0i | Poynting/worldtube leakage feeds the 3210 b_X source term | boundary nohair/proper-exact cancellation or sourced Poynting flux bound | not_bulk_survives_as_boundary_source | false |

## EM Bulk Survivor Reduction

| reduction_id | statement | effect | reduction_status | remaining_active_terms | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| RED3214_0_bulk_source_formula | J_X^EM,bulk = sum_a (L_X I_a)[1/4 partial_Ia Z_A F^2 + 1/4 partial_Ia Theta_A FstarF - 1/2 T_EM^{mu nu} partial_Ia g_obs,mu nu + partial_Ia C_readout O_readout] | bulk source is a generator-velocity times coefficient-Jacobian problem | derived_formula | memory_or_class_scalar; continuous clock-arrow if present; readout/radiative scalar slot | false |
| RED3214_1_discrete_bulk_pruning | fixed finite-cell, fixed domain class, and fixed selector labels have L_X I=0 inside a connected smooth local branch | they are pruned from smooth bulk EM source, but not from boundary jumps or source normalization | conditional_pruning_not_claim | domain-wall/boundary flux; nonuniversal constants; readout selector if varied after reduction | false |
| RED3214_2_real_enemy_list | The shortest route to local EM silence is not killing every label; it is killing the continuous memory/readout coefficient projection and separately bounding boundary Poynting flux. | next derivation should target memory scalar nohair/coefficient typing before more broad audits | route_narrowed | memory scalar; readout/radiative closure; boundary flux; universal source-coupling constants | false |

## Provenance Promotion Rows

| row_id | source_generator | coefficient | zero_route | finite_route_inputs | feeds | current_status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| PROM3214_0_memory_to_balpha | memory_or_class_scalar | b_alpha_memory = partial_memory ln Z_A | exact typed exclusion of memory from visible gauge coefficient or positive memory nohair with L_X memory=0 | memory amplitude/gradient; partial_memory ln Z_A bound; EM F2 norm; source path; units | 3212 FEB3212_0_balpha;3210 source amplitude law | MISSING_MEMORY_NOHAIR_OR_NUMERIC_BOUND | false |
| PROM3214_1_memory_to_hodge | memory_or_class_scalar | C_Hodge_memory = partial_memory g_obs or partial_memory star_obs | observed coframe/Hodge star factors only through q and memory is vertical-invisible | C_Hodge_memory bound; EM stress norm; local support; source path; units | 3212 FEB3212_3_Hodge;PPN/clock/local stress rows | MISSING_HODGE_FACTORING_OR_NUMERIC_BOUND | false |
| PROM3214_2_readout_to_alpha_clock | readout_projector | C_readout_alpha_clock | readout-after-variation plus no readout feedback into S_eff | readout coefficient derivative; clock/alpha observable norm; source path; units | clock drift; alpha drift; R10 transfer gates | MISSING_READOUT_CLOSURE_OR_NUMERIC_BOUND | false |
| PROM3214_3_boundary_poynting | boundary_or_worldtube_flux_weight | C_Poynting_boundary | boundary functor exact/proper/orthogonal or depends only on q-visible flux | C_Poynting; integral \|n_i T_EM^0i\| dSdt; worldtube rule; orientation; source path; units | 3212 FEB3212_4_Poynting;3210 boundary leakage b_X | MISSING_BOUNDARY_NOHAIR_OR_FLUX_BOUND | false |
| PROM3214_4_species_kappa | species_charge_constants | Delta kappa_A or source weight nonuniversality | universal Hilbert source theorem with one kappa and all species stress entering same metric variation | species source-weight differences; WEP/local source bounds; material composition; source path; units | WEP;PPN;Newtonian source coupling | MISSING_UNIVERSAL_SOURCE_THEOREM_OR_BOUND | false |

## Decision

`COUPLING_JACOBIAN_GATE_DERIVED_DISCRETE_BULK_GENERATORS_PRUNED_MEMORY_READOUT_BOUNDARY_SURVIVE`.

Claim status: `NO_LOCAL_GR_NO_EM_SILENCE_NO_BALPHA_ZERO_CLAIM`.

Best next route: derive the memory scalar nohair/coefficient-typing theorem first, because it is the main continuous bulk EM coupling survivor; handle boundary Poynting and source universality as separate finite/proof branches.

Next target:

```text
3215-Y5-R2FR-memory-scalar-nohair-or-coefficient-typing-theorem-for-balpha-Hodge-under-AX1090
```

## Generated Evidence

- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3214_INPUTS.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3214_INVARIANT_COUPLING_CRITERION.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3214_GENERATOR_KILL_LIST.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3214_EM_BULK_SURVIVOR_REDUCTION.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3214_PROVENANCE_PROMOTION_ROWS.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3214_DECISION.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3214_VALIDATION.csv`

## Validation

| check_id | pass | detail |
| --- | --- | --- |
| VAL3214_00_inputs_exist | true | inputs=9 |
| VAL3214_01_chain_rule_gate | true | L_X C_vis = sum partial_I C_vis L_X I plus explicit slot |
| VAL3214_02_discrete_pruning | true | discrete generators have dI=0 on connected no-wall branch |
| VAL3214_03_generator_coverage | true | GK3214_0_finite_cell_spectrum;GK3214_1_relative_domain_class;GK3214_2_domain_selector;GK3214_3_memory_class_scalar;GK3214_4_orientation_time_arrow;GK3214_5_species_constants;GK3214_6_readout_projector;GK3214_7_boundary_flux_weight |
| VAL3214_04_memory_survives | true | continuous memory/class scalar remains the main bulk-coupling target |
| VAL3214_05_provenance_rows | true | PROM3214_0_memory_to_balpha;PROM3214_1_memory_to_hodge;PROM3214_2_readout_to_alpha_clock;PROM3214_3_boundary_poynting;PROM3214_4_species_kappa |
| VAL3214_06_claims_blocked | true | claim_rows_true=0 |
| VAL3214_07_no_formalization_workbench_edit | true | no formalization-workbench paths are output targets |
| VAL3214_08_csv_parse | true | P8_Y5_R2FR_3214_INPUTS.csv;P8_Y5_R2FR_3214_INVARIANT_COUPLING_CRITERION.csv;P8_Y5_R2FR_3214_GENERATOR_KILL_LIST.csv;P8_Y5_R2FR_3214_EM_BULK_SURVIVOR_REDUCTION.csv;P8_Y5_R2FR_3214_PROVENANCE_PROMOTION_ROWS.csv;P8_Y5_R2FR_3214_DECISION.csv |
| VAL3214_09_next_target | true | 3215-Y5-R2FR-memory-scalar-nohair-or-coefficient-typing-theorem-for-balpha-Hodge-under-AX1090 |

All generated rows remain `valid_for_claim=false`.
