# 3727 — U_H Local Unit Map Schema or Symbolic Operator Lock

## Status
- `UH_SCHEMA_READY_CURRENT_UNIT_MAP_SYMBOLIC`
- `U_H` is now an explicit finite matrix/singular-value schema from Fisher/response Hessian units to local `m^-2` operator units.
- Current runner status: `BLOCKED_SYMBOLIC_UH` because template map rows are placeholders.
- `Xi_loc` remains unscoreable until `u_min` and `R_U` are source-owned.

## Main Result
- `U_H` must map the abstract mean-branch Hessian into the observed local operator basis.
- Finite matrix law: `u_min=sqrt(lambda_min(U_H^T U_H))`.
- The corrected local gap uses `u_min^2` and subtracts a unit-map remainder `R_U`.
- Without `U_H`, a positive Fisher/response gap is not yet a local GR/Newton/R10 gap.

## Theorem Rows
- `THM3727_0_map_definition` `SCHEMA`: U_H: H_Fisher -> H_local maps abstract Hessian directions into local m^-2/operator units. | defines the missing local-unit object
- `THM3727_1_coercivity` `COERCIVITY_REQUIREMENT`: ||U_H v||_local >= u_min ||v||_Fisher for all active v. | gives the u_min^2 multiplier in Xi_loc
- `THM3727_2_remainder` `REMAINDER_REQUIREMENT`: R_U bounds projection, basis, non-isometry, and omitted-local-channel errors. | keeps unit conversion losses explicit
- `THM3727_3_matrix_runner` `DERIVED_SCHEMA`: For finite U matrix, u_min=sqrt(lambda_min(U^T U)). | makes U_H a singular-value problem
- `THM3727_4_refusal` `ANTI_SMUGGLING_GUARD`: If U entries, bases, units, or coercivity are missing, Xi_loc cannot be scored. | prevents abstract gap from becoming local-GR claim

## Runner Status
- `RUN3727_0_UH` `BLOCKED_SYMBOLIC_UH`: executable=False missing=`L0:F0;L0:F1;L1:F0;L1:F1` u_min=``

## Decisions
- `DEC3727_0_schema_ready` `UH_SCHEMA_READY` | U_H is now an explicit finite matrix/singular-value schema rather than a hidden unit conversion.
- `DEC3727_1_current_blocked` `CURRENT_UH_LOCKED_SYMBOLIC` | Template map rows are placeholders, so u_min/R_U remain missing and Xi_loc cannot be scored.
- `DEC3727_2_next` `ADVANCE_TO_COMBINED_XILOC_RUNNER` | With Fisher window and U_H schemas installed, next target can combine both and refuse scoring until all inputs are real.

## Claim Gates
- `CG3727_0_domain_basis` `BLOCKED` | Fisher/response Hessian basis parent-owned
- `CG3727_1_local_basis` `BLOCKED` | local operator m^-2 basis parent-owned
- `CG3727_2_units` `BLOCKED` | domain and codomain units matched
- `CG3727_3_matrix` `BLOCKED` | U_H matrix entries numeric and parent-owned
- `CG3727_4_coercivity` `BLOCKED` | u_min>0 and R_U finite
- `CG3727_5_Xi` `BLOCKED` | Xi_loc score can use U_H
- `CG3727_6_claim` `BLOCKED` | local operator/local-GR claim allowed

## Next Target
- `3728-Y5-R2FR-combined-Xiloc-runner-and-refusal-gates.md`
- Objective: combine Fisher window, `U_H`, scale, mismatch, and losses into one refusal-safe `Xi_loc` runner.
