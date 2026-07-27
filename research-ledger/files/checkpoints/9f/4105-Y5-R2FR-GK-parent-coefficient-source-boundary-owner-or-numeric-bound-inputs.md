# 4105 - GK parent coefficient/source/boundary owner or numeric bound inputs

## Verdict
4105 is deliberately not another spin around the same GK missing-input roundabout. It audits the GK input gate, imports the older resolved trail, and moves the live route forward.

The result is sharp:

- `lambda_GK` has an exact conditional lower-bound formula, but the signs/domain/cross/stability/observable-lock package is not parent-signed.
- The coercive `1/lambda_GK` no-hair route is therefore blocked.
- The noncoercive finite branch exists: `a_GK=C_Poincare_GK J_GK_norm + C_trace_GK |Phi_boundary_GK| + C_top_GK |Q_top_GK|`, `X_GK<=0.5*(a_GK+sqrt(a_GK^2+4F_outer_GK_abs))`, and `epsilon_GK_hair_nc<=K_GK X_GK`.
- The absorption law also exists: from `X_GK^2 <= a_GK X_GK + F0_GK_abs + eta_GK X_GK^2`, `eta_GK<1` gives the exact absorbed root.
- Because `eta_GK<1`, `F0_GK_abs`, and `K_GK` remain unsigned, GK hair is now carried as `X_GK_residual`, not endlessly refilled.

Decision: `GK_INPUTS_AUDITED_LAMBDA_UNSIGNED_NONCOERCIVE_AND_ABSORPTION_ROUTES_IMPORTED_SOURCE_COUPLING_PIVOT_SELECTED`

## Practical consequence
The best next attack is source coupling: prove the `Pi_M J_H` to Hamiltonian/Hilbert mass-charge equality, or build the first source-ready `epsilon_mu` input pack. That is the path from an EH/weak-field branch to actual Newtonian measured `GM`.

## Outputs
- `P8_Y5_R2FR_4105_SOURCE_REGISTER.csv`
- `P8_Y5_R2FR_4105_GK_INPUT_OWNER_MATRIX.csv`
- `P8_Y5_R2FR_4105_LAMBDA_GK_POSITIVITY_AUDIT.csv`
- `P8_Y5_R2FR_4105_NONCOERCIVE_INPUT_PACK_IMPORT.csv`
- `P8_Y5_R2FR_4105_ABSORPTION_RESIDUAL_CONTRACT.csv`
- `P8_Y5_R2FR_4105_SOURCE_COUPLING_PIVOT.csv`
- `P8_Y5_R2FR_4105_DECISION_GATE.csv`
- `P8_Y5_R2FR_4105_CLAIM_GATE.csv`
- `P8_Y5_R2FR_4105_NEXT_TARGET.csv`
- `P8_Y5_R2FR_4105_STATUS.csv`
- `P8_Y5_BRR545_4105_VALIDATION.csv`

## Next target
- `4106-Y5-R2FR-PiM-Hilbert-charge-equality-or-epsilon-mu-input-pack.md`
- Objective: derive `B_xi/G_ref=M_H[Pi_M J_H]` with projector variation handled, or construct source/unit/input rows for `epsilon_mu` without claiming Newton/PPN.
