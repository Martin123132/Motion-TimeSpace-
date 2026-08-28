# 5361 - D4 E005 frozen holdout and three-rung curvature gate

## Decision

`D4_E005_FROZEN_HOLDOUT_COMPATIBLE__ACQUIRE_E010_FOR_COMPLETE_FIXED_A_FAMILY`

## Blind comparison

Checkpoint 5360 froze the E005 prediction using only E00125 and E0025. This checkpoint reads E005 only after its independent eight-event integration and validation pass.

- frozen prediction: `5.7283434974085274 +6.4823353306222407 i`, disk `0.11125673393041546`;
- measured E005: `5.7284929273339813 +6.481579111780122 i`, disk `0.026118049481747969`;
- centre separation: `0.00077084125460199907`;
- combined disk radius: `0.13737478341216344`;
- compatibility: `True`.

## Derived curvature combination

For dyadic regulators `(h,2h,4h)` with `h=0.00125`, define `J=I-A epsilon Log(epsilon/0.0025)`. The preregistered affine residual is exactly

`Delta3 = J(4h)+2J(h)-3J(2h)`.

For the complete second-order normal form this obeys

`Delta3/h^2 = 14 Log(2) C + 6 D + [R3(4h)+2R3(h)-3R3(2h)]/h^2`.

The measured composite curvature is `95.635152290469705 -483.98005895592178 i` with conservative disk `87919.861383784606`.

## Claim boundary

This is a genuine frozen leading-family holdout and one measured composite curvature combination. Three rungs cannot separate `C` from `D`, cannot numerically upper-bound `R3`, and cannot establish the regulator-zero limit. More accepted rungs remain mandatory.
