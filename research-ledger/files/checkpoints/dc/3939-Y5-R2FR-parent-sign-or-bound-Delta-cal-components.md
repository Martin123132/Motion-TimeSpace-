# 3939 - Parent-Sign or Bound Delta_cal Components

Timestamp: `2026-07-01T12:27:03+00:00`

## Result

Built the first `Delta_cal` closure reducer.

The 3938 runner had 11 active component blockers. 3939 reduces them to six parent clauses:

1. same-parent source Hamiltonian and charge equality;
2. same-frame EH weak-field Poisson plus Gauss flux;
3. minimal slow-body readout of the same potential;
4. no extra mass-channel monopole;
5. constant universal coupling plus closed projected source flux;
6. second-order PPN source/operator stability.

If those six clauses are parent-signed in one branch, then `Delta_cal_abs=0`. If any clause fails, the affected components stay in the no-cancellation fallback score.

## Closure Attempt

The conditional reducer theorem is now explicit:

`PC0 ∧ PC1 ∧ PC2 ∧ PC3 ∧ PC4 ∧ PC5 => Delta_charge = Delta_Poisson = Delta_Gauss = Delta_orbit = mu_extra = Delta_G = Delta_flux = partial_r ln mu_obs = dln_Geff_dt_plus_dln_Meff_dt = Delta_frame_species_range = Delta_PPN_source = 0`.

Therefore:

`Delta_cal_abs = 0`

inside that private branch.

## Current Verdict

- Reducer: built.
- Public claim: blocked.
- Reason: PC0-PC5 are not parent-signed as a single current MTS parent branch.
- Best next attack: PC0, because it anchors source charge, Poisson source ownership, WEP/R10 source charges, and PPN source normalization.

## Source Register

- Source rows found: `15/15`
- Register: `source-intake\mts_residuals\P8_Y5_R2FR_3939_SOURCE_REGISTER.csv`
- Validation: `source-intake\mts_residuals\P8_Y5_BRR545_3939_VALIDATION.csv`

## Generated Tables

- `source-intake\mts_residuals\P8_Y5_R2FR_3939_PARENT_CLAUSE_STACK.csv`
- `source-intake\mts_residuals\P8_Y5_R2FR_3939_DELTA_CAL_COMPONENT_REDUCTION_MAP.csv`
- `source-intake\mts_residuals\P8_Y5_R2FR_3939_DELTA_CAL_CLOSURE_ATTEMPT.csv`
- `source-intake\mts_residuals\P8_Y5_R2FR_3939_COMPONENT_BOUND_ROUTE_MATRIX.csv`
- `source-intake\mts_residuals\P8_Y5_R2FR_3939_REDUCED_DELTA_CAL_RUNNER.csv`
- `source-intake\mts_residuals\P8_Y5_R2FR_3939_CLAIM_GATE.csv`
- `source-intake\mts_residuals\P8_Y5_R2FR_3939_NEXT_TARGET.csv`

## Next Target

`3940-Y5-R2FR-source-charge-Hamiltonian-equality-or-bound.md`
