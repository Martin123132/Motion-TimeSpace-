# 3199 - Poynting Source Coupling Domain Map Candidate Or Local Residual Bound Under AX1090

Private checkpoint. This is not a local-GR claim, Newtonian-limit claim, PPN pass, Maxwell derivation, EM unification claim, R10 pass, clock pass, orbital pass, or public-facing result.

## Result

3199 takes the constructive route rather than only circling missing inputs.

The candidate parent-domain map is:

```text
C^nu = n_mu(T_MTS^{mu nu} - tau_m T_matter^{mu nu} - tau_EM T_EM^{mu nu})|_layer.
```

This is the right shape because parent-owned local gluing should be a normal stress-flux balance. In that language the Poynting vector is not decorative: it is the EM energy-flux/momentum-density part of `T_EM^{mu nu}`.

Tiny goblin verdict: useful route, not closed.

## What This Derives

If a parent action supplies `T_MTS`, matter/EM descent, source couplings, and the layer variation, then the 3197 stiffness theorem can be fed by a flux map:

```text
J_Aa = partial C_A / partial z^a,
K0 = J^T G_flux J.
```

This is a real derivation target, not a vibes target.

## Why Poynting Helps But Does Not Save The Branch Alone

- `PMG3199_00`: `open` - Poynting may be used as a target structure, not a derived MTS object
- `PMG3199_01`: `open` - without this, EM flux can only be a phenomenological/pre-Maxwell residual channel
- `PMG3199_02`: `open` - tau_EM cannot be claimed parent-owned
- `PMG3199_03`: `partial_open` - can define a source-ready bound row, not a Maxwell derivation claim

A large unsuppressed local Poynting flux would hurt the local-GR branch, not rescue it. In quiet/static local tests the EM flux contribution must either theorem-zero or enter the residual-bound ledger.

## Hard Gates

- `RPG3199_00`: C^nu is obtained by varying a parent action with an interface/layer domain, not imposed as an external junction rule Status: `unproven`.
- `RPG3199_01`: rank(J)=4 for z=(Delta F_L, Delta F'_L, Delta F_R, Delta F'_R) Status: `unproven`.
- `RPG3199_02`: positive normal metric on flux codomain comes from parent hyperbolic energy or observer-split positive energy norm Status: `unproven`.
- `RPG3199_03`: source coupling coefficients are fixed by parent normalization/units rather than tuned owner couplings Status: `unproven`.

## Residual Bound Fallback

If the flux map is not parent-derived, the honest fallback is to bound each absolute component without cancellation credit.

- `BR3199_00`: `B_obs_EM_Poynting_over_MH` - abs(P_loc n_mu tau_EM T_EM^{mu nu})/M_H_ref
- `BR3199_01`: `B_obs_matter_source_flux_over_MH` - abs(P_loc n_mu tau_m T_matter^{mu nu})/M_H_ref
- `BR3199_02`: `B_obs_MTS_stress_flux_over_MH` - abs(P_loc n_mu T_MTS^{mu nu})/M_H_ref
- `BR3199_03`: `B_obs_total_flux_no_cancellation_over_MH` - sum of BR3199_00..BR3199_02 absolute components with no cancellation credit

## Decision

`STRESS_FLUX_DOMAIN_MAP_CANDIDATE_BUILT_NOT_CLOSED`.

Claim status: `NO_LOCAL_GR_MAXWELL_OR_PPN_CLAIM`.

Decision: Poynting/source flux is a legitimate candidate ingredient only through stress-energy; current corpus lacks Maxwell descent, parent-owned couplings, positive flux metric, and rank-four Jacobian

Best next route: derive or source the four response coefficients J_Aa for C^nu, starting with whether quiet local Poynting flux is theorem-zero or finite-bounded

Next target:

```text
3200-Y5-R2FR-stress-flux-rank-coefficient-extractor-or-Poynting-residual-bound-runner-under-AX1090
```

## Generated Evidence

- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3199_INPUTS.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3199_STRESS_FLUX_DOMAIN_CANDIDATE.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3199_POYNTING_MAXWELL_DESCENT_AUDIT.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3199_RANK_POSITIVITY_AND_COUPLING_GATE.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3199_LOCAL_RESIDUAL_BOUND_SCHEMA.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3199_DECISION.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3199_VALIDATION.csv`

## Validation

- `VAL3199_00_inputs_exist`: `true` - inputs=11
- `VAL3199_01_candidate_equation_recorded`: `true` - C^nu normal stress-flux map present
- `VAL3199_02_poynting_not_overclaimed`: `true` - PMG3199_00=open;PMG3199_01=open;PMG3199_02=open;PMG3199_03=partial_open
- `VAL3199_03_rank_and_positive_metric_unproven`: `true` - rank(J), positive G_flux, parent variation, and tau ownership remain open
- `VAL3199_04_residual_schema_has_poynting_component`: `true` - Poynting bound schema staged without numeric claim
- `VAL3199_05_no_claim_leak`: `true` - no local-GR, Maxwell, PPN, or coupling claim
- `VAL3199_06_decision_names_extractor`: `true` - 3200-Y5-R2FR-stress-flux-rank-coefficient-extractor-or-Poynting-residual-bound-runner-under-AX1090
- `VAL3199_07_csv_parse`: `true` - P8_Y5_R2FR_3199_INPUTS.csv;P8_Y5_R2FR_3199_STRESS_FLUX_DOMAIN_CANDIDATE.csv;P8_Y5_R2FR_3199_POYNTING_MAXWELL_DESCENT_AUDIT.csv;P8_Y5_R2FR_3199_RANK_POSITIVITY_AND_COUPLING_GATE.csv;P8_Y5_R2FR_3199_LOCAL_RESIDUAL_BOUND_SCHEMA.csv;P8_Y5_R2FR_3199_DECISION.csv

All generated rows remain `valid_for_claim=false`.
