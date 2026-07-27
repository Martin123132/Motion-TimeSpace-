# 4104 - No homogeneous exterior mode or extra-hair epsilon row

## Verdict
4104 does not pretend to prove full no-hair. It does something more useful: it makes the exterior-hair problem channel-by-channel and imports the first concrete field-specific channel, `Gamma/Khat`.

The homogeneous exterior split is now `delta Phi_hom = h_TT^rad + X_coercive + X_cross + X_top_boundary + X_projector + X_nonEH`. Radiative EH modes are killed only by a zero-news/no-radiation boundary. Coercive extra modes are killed only by a positive self-adjoint energy identity with zero source charge, zero boundary/topological flux and fixed gauge/projector kernel.

For `Gamma/Khat`, the nonzero route is explicit: `epsilon_GK_hair = K_GK * [(J_GK_norm + sqrt(J_GK_norm^2 + 4 lambda_GK |Phi_boundary_GK+Q_top_GK|))/(2 lambda_GK)]`. That is a real bound contract, not a placeholder.

Decision: `NO_HOMOGENEOUS_MODE_CHANNELIZED_GK_COERCIVE_BOUND_IMPORTED_ZERO_THEOREMS_CONDITIONAL_EXTRA_HAIR_RETAINED`

## What Advanced
- `epsilon_hom_mode` is decomposed into physical channels rather than one vague row.
- EH radiative hair has a zero-news/no-radiation theorem route.
- Coercive extra hair has an energy-identity zero theorem route.
- `Gamma/Khat` is now a concrete theorem-or-bound channel with `lambda_GK`, `J_GK_norm`, `Phi_boundary_GK`, and `Q_top_GK` inputs.

## What Remains Live
- `lambda_GK`, source charge, boundary flux, topology and projector/gauge kernel are not parent-signed.
- Topological/boundary hair, projector-hidden hair, cross terms and non-EH operators remain explicit residual channels.
- No local GR/Newton/Maxwell/PPN claim follows.

## Outputs
- `P8_Y5_R2FR_4104_SOURCE_REGISTER.csv`
- `P8_Y5_R2FR_4104_NO_HOMOGENEOUS_MODE_THEOREM.csv`
- `P8_Y5_R2FR_4104_HAIR_CHANNEL_AUDIT.csv`
- `P8_Y5_R2FR_4104_GK_BOUND_INPUT_ROWS.csv`
- `P8_Y5_R2FR_4104_EPSILON_HAIR_ROWS.csv`
- `P8_Y5_R2FR_4104_ACTIVATION_GATES.csv`
- `P8_Y5_R2FR_4104_DECISION_GATE.csv`
- `P8_Y5_R2FR_4104_CLAIM_GATE.csv`
- `P8_Y5_R2FR_4104_NEXT_TARGET.csv`
- `P8_Y5_R2FR_4104_STATUS.csv`
- `P8_Y5_BRR545_4104_VALIDATION.csv`

## Next target
- `4105-Y5-R2FR-GK-parent-coefficient-source-boundary-owner-or-numeric-bound-inputs.md`
- Objective: source/sign `lambda_GK`, `J_GK_norm`, `Phi_boundary_GK`, and `Q_top_GK`, or fill them as finite nonclaim rows with units.
