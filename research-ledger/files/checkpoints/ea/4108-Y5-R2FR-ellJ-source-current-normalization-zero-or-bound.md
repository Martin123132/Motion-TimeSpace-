# 4108 - ellJ source-current normalization zero or bound

## Verdict
4108 makes `ell_J` a real source-current theorem gate instead of a hidden normalization denominator.

`z_ellJ = R_md + R_Ward + R_PiM + R_Htau + R_ref + R_W + R_frame + R_units`.

The core is now sharper again:

`R_PiM + R_Htau = C_M + C_shape + C_curl + C_domain + C_ref + C_frame + C_units`.

The best non-cheat route is the chain-rule mechanism: if `Y=(M_H_ref,sigma^a)` descends through the parent quotient and the residual direction is truly vertical, then `A_X=dYbar(Dq(v_X))=0`, so `C_M=C_shape=0` before any measured-GM calibration.

Decision: `ELLJ_DECOMPOSITION_IMPORTED_PIM_HTAU_SUBDENOMINATOR_CONDITIONAL_ZERO_ROUTE_ACTIVE_QBASIC_SOURCE_COORDINATE_GATE_NEXT`

## Concrete Advances
- `ell_J` is decomposed into named source-current owner residuals.
- `R_PiM+R_Htau` is identified as the algebraic heart of the denominator.
- `C_M` and `C_shape` get a real derivation route through q-basicity and verticality.
- Measured-orbital `GM` is explicitly forbidden as the definition of `ell_J`, `M_H_ref`, `H_ref`, source units, or source shape.

## Still Not Claimed
- `ell_J` source silence.
- Constant measured `G_eff`.
- Newton/local-GR/PPN promotion.

## Outputs
- `P8_Y5_R2FR_4108_SOURCE_REGISTER.csv`
- `P8_Y5_R2FR_4108_ELLJ_DECOMPOSITION.csv`
- `P8_Y5_R2FR_4108_PIM_HTAU_SUBDENOMINATOR.csv`
- `P8_Y5_R2FR_4108_BOUND_INPUTS.csv`
- `P8_Y5_R2FR_4108_PROMOTION_GATES.csv`
- `P8_Y5_R2FR_4108_DECISION_GATE.csv`
- `P8_Y5_R2FR_4108_NEXT_TARGET.csv`
- `P8_Y5_R2FR_4108_STATUS.csv`
- `P8_Y5_BRR545_4108_VALIDATION.csv`

## Next target
- `4109-Y5-R2FR-source-coordinate-qbasicity-or-AX-connection-bound.md`
- Objective: prove `Y=(M_H_ref,sigma^a)` is q-basic and `Dq(v_X)=0`, or retain `A_X` source-connection bound rows.
