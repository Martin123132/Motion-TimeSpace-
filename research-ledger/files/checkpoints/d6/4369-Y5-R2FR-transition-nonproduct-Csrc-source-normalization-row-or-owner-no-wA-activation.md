# 4369: non-product C_src source-normalization row or owner/no-wA activation

Marker: `PPC4161_TRANSITION_NONPRODUCT_CSRC_SOURCE_NORMALIZATION_ROW_OR_OWNER_NO_WA_ACTIVATION_4369`

## What changed

- Installed the non-product Newton/source-normalization projection row `Pi_Gsrc^C=[0,0,0,1]`.
- Defined `epsilon_Gsrc` as the fractional defect in `G_cal rho_H`.
- Derived the exact Poisson/Green transfer and compact-source bound.
- Split common calibration mode from the physical shape residual `epsilon_Gsrc_perp`.
- Kept the zero route conditional because parent source-measure/source-mass/owner graph signatures are still not globally signed.

## Decision row

| decision_id | decision | summary | next_target |
| --- | --- | --- | --- |
| DEC4369_0 | NONPRODUCT_EPSILON_GSRC_NEWTON_GREEN_TRANSFER_DERIVED_OWNER_ZERO_NOT_PARENT_ACTIVATED_NONCLAIM | 4369 advances the non-product source-coupling route by defining epsilon_Gsrc as the fractional defect in G_cal rho_H, installing the Newton/source-normalization projection row [0,0,0,1], deriving the exact Poisson/Green transfer and compact-source bound, and splitting off the common monopole calibration mode. The useful physical residual is epsilon_Gsrc_perp. It is not zeroed yet: source-measure leaks, source-mass ownership, owner/no-wA graph signatures, Xi_open, T_open and transition hair remain unsigned/open. No local-GR/Newton/PPN claim fires. | 4370-Y5-R2FR-transition-epsilon-Gsrc-coefficient-bound-or-Xi-owner-edge-proof.md |

## Next target

| next_id | target | question | preferred_route | alternate_zero_route | avoid |
| --- | --- | --- | --- | --- | --- |
| NT4369_0 | 4370-Y5-R2FR-transition-epsilon-Gsrc-coefficient-bound-or-Xi-owner-edge-proof.md | Can epsilon_Gsrc_perp be bounded with a source/worldtube coefficient, or can one parent owner/no-wA edge be signed enough to zero it? | derive/source a compact-support coefficient bound for epsilon_Gsrc_perp in Newton/source-normalization | parent-sign one concrete measure/source-mass/no-reentry edge that forces epsilon_Gsrc_perp=0 | claiming local GR from the symbolic projection row alone |
