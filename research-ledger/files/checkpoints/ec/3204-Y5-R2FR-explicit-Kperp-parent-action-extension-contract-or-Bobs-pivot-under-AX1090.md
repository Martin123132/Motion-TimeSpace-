# 3204 - Explicit Kperp Parent Action Extension Contract Or Bobs Pivot Under AX1090

Private checkpoint. This is not a local-GR claim, Newtonian-limit claim, PPN pass, parent-action promotion, rank-four proof, R10 pass, clock pass, orbital pass, or public-facing result.

## Result

3204 writes the explicit extension in a form that is respectable enough to keep testing privately:

```text
S_ext = (1/(2 kappa_GR)) int sqrt(-g) eta_T ell_T^2 <D_T K_perp, D_T K_perp> d^4x
D_T = Pi_perp (1 - ell_T^2 Delta_perp) Pi_perp
K_perp = Pi_perp[K_hat],
D_T^dagger D_T K_perp = Sigma_perp.
```

The important restriction is that `Delta_perp` is elliptic/spatial/domain-normal in the local static coarse-grained sector. A covariant fourth-time-derivative `Box^2` promotion is rejected unless a separate ghost-free construction exists.

## Action Extension

- `EXT3204_00_action`: `Kperp local-static extension action` -> `PRIVATE_EXTENSION_CANDIDATE_NOT_PARENT_PROMOTION`
- `EXT3204_01_source`: `optional projected tensor source` -> `CONDITIONAL_SOURCE_CHANNEL`
- `EXT3204_02_projection`: `transverse/traceless local projection` -> `OPEN_PARENT_PROJECTOR`
- `EXT3204_03_trace`: `C1 trace map` -> `OPEN_PARENT_TRACE_MAP`
- `EXT3204_04_scope`: `no-ghost scope restriction` -> `MANDATORY_SAFETY_RESTRICTION`

## Dimension Audit

- `DIM3204_00_Kperp`: `K_perp` has `L^-2` -> `source_backed_dimension`
- `DIM3204_01_ellT`: `ell_T` has `L^1` -> `new_parameter_needs_parent_or_empirical_bound`
- `DIM3204_02_DT`: `D_T = 1 - ell_T^2 Delta_perp` has `L^0` -> `dimensionally_consistent`
- `DIM3204_03_action_bracket`: `eta_T ell_T^2 <D_T K_perp,D_T K_perp>` has `L^-2` -> `dimensionally_consistent`
- `DIM3204_04_sigma`: `Sigma_perp` has `L^-2` -> `dimensionally_consistent_but_unsourced`
- `DIM3204_05_eta`: `eta_T` has `L^0` -> `new_parameter_needs_parent_normalization`

## Normal Variation

- `NM3204_00_define_Y`: S_normal = (eta_T ell_T^2/2) int Y^2 d rho -> `local_static_normal_reduction`
- `NM3204_01_bulk`: eta_T ell_T^2 int (Y - ell_T^2 Y'') delta K d rho = eta_T ell_T^2 int D_T^dagger D_T K delta K d rho -> `derives_fourth_order_operator`
- `NM3204_02_Pi1`: Pi_1 = - eta_T ell_T^4 Y -> `C1_boundary_momentum_present`
- `NM3204_03_Pi0`: Pi_0 = eta_T ell_T^4 Y' -> `C1_boundary_momentum_present`
- `NM3204_04_source`: D_T^dagger D_T K_perp = Sigma_perp -> `conditional_on_source_descent`

## Safety Gates

- `SAFE3204_00_no_ghost`: `elliptic_not_fourth_time_dynamics` -> `passes_as_contract_restriction_not_parent_proof`; fail action: if promoted to covariant Box^2 without ghost-free construction, reject extension and pivot to Bobs
- `SAFE3204_01_parent_frame`: `parent-owned observer/environment frame` -> `open`; fail action: projector/frame leakage becomes Bobs_projector_commutator component
- `SAFE3204_02_positive_eta`: `positive stiffness weight` -> `contract_pass_unsourced`; fail action: negative/indefinite sector rejected as ghost/instability
- `SAFE3204_03_no_zero_modes`: `zero modes fixed` -> `open`; fail action: rank map nonunique; pivot to Bobs or add explicit zero-mode ledger
- `SAFE3204_04_local_suppression`: `local safety` -> `open`; fail action: extension may exist but only as residual component, not local-GR proof
- `SAFE3204_05_no_tuned_rank`: `no tuned trace map` -> `open`; fail action: rank-four owner remains closure-only

## Pivot Logic

- `PIV3204_00_continue_extension`: `continue Kperp extension` -> `PASS_AS_PRIVATE_EXTENSION_CANDIDATE_ONLY`
- `PIV3204_01_demote_to_Bobs`: `Bobs residual acquisition` -> `STAGED_NOT_TRIGGERED_THIS_CHECKPOINT`
- `PIV3204_02_public_claim`: `public/local-GR claim` -> `FORBIDDEN`

## Decision

`KPERP_EXTENSION_ADMISSIBLE_AS_PRIVATE_CANDIDATE_ONLY`.

Claim status: `NO_PARENT_PROMOTION_LOCAL_GR_NEWTON_OR_PPN_CLAIM`.

Decision: the explicit Kperp action extension is dimensionally consistent and derives the L4/C1-boundary mechanism, but it remains a private candidate because parent frame, projector, zero modes, trace map, and local suppression are not closed

Best next route: run a hard safety screen on frame/projector/zero-mode/trace/local-suppression gates; if any fail without repair, pivot to Bobs residual acquisition

Next target:

```text
3205-Y5-R2FR-Kperp-extension-safety-screen-or-Bobs-pivot-under-AX1090
```

## Generated Evidence

- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3204_INPUTS.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3204_EXPLICIT_ACTION_EXTENSION.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3204_DIMENSION_AND_NORMALIZATION_AUDIT.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3204_NORMAL_VARIATION_MOMENTA.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3204_EXTENSION_SAFETY_GATES.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3204_EXTENSION_OR_BOBS_PIVOT.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3204_DECISION.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3204_VALIDATION.csv`

## Validation

- `VAL3204_00_inputs_exist`: `true` - inputs=8
- `VAL3204_01_action_explicit`: `true` - action_rows=5
- `VAL3204_02_dimensions_consistent`: `true` - K_perp=source_backed_dimension;ell_T=new_parameter_needs_parent_or_empirical_bound;D_T = 1 - ell_T^2 Delta_perp=dimensionally_consistent;eta_T ell_T^2 <D_T K_perp,D_T K_perp>=dimensionally_consistent;Sigma_perp=dimensionally_consistent_but_unsourced;eta_T=new_parameter_needs_parent_normalization
- `VAL3204_03_variation_has_C1_momenta`: `true` - NM3204_00_define_Y;NM3204_01_bulk;NM3204_02_Pi1;NM3204_03_Pi0;NM3204_04_source
- `VAL3204_04_safety_open_not_claimed`: `true` - elliptic_not_fourth_time_dynamics=passes_as_contract_restriction_not_parent_proof;parent-owned observer/environment frame=open;positive stiffness weight=contract_pass_unsourced;zero modes fixed=open;local safety=open;no tuned trace map=open
- `VAL3204_05_pivot_logic`: `true` - continue Kperp extension=PASS_AS_PRIVATE_EXTENSION_CANDIDATE_ONLY;Bobs residual acquisition=STAGED_NOT_TRIGGERED_THIS_CHECKPOINT;public/local-GR claim=FORBIDDEN
- `VAL3204_06_decision_nonclaim`: `true` - 3205-Y5-R2FR-Kperp-extension-safety-screen-or-Bobs-pivot-under-AX1090
- `VAL3204_07_no_claim_leak`: `true` - no parent promotion, local-GR, Newton, PPN, or rank-four claim
- `VAL3204_08_csv_parse`: `true` - P8_Y5_R2FR_3204_INPUTS.csv;P8_Y5_R2FR_3204_EXPLICIT_ACTION_EXTENSION.csv;P8_Y5_R2FR_3204_DIMENSION_AND_NORMALIZATION_AUDIT.csv;P8_Y5_R2FR_3204_NORMAL_VARIATION_MOMENTA.csv;P8_Y5_R2FR_3204_EXTENSION_SAFETY_GATES.csv;P8_Y5_R2FR_3204_EXTENSION_OR_BOBS_PIVOT.csv;P8_Y5_R2FR_3204_DECISION.csv

All generated rows remain `valid_for_claim=false`.
