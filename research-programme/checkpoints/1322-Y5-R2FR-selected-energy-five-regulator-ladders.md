# 5306 — Selected-energy five-regulator ladders

## Result

The exact activation/cancellation support from 5305 was integrated at
four representative fixed-decay energy nodes. Each node uses all five
regulators, order-4/order-8 angular quadrature, and a resumable shard
per regulator/order pair.

- completed shards: `40/40`;
- maximum order change: `0.911412084064`;
- maximum final Richardson change: `0.0344339181603`;
- maximum model-intercept change: `0.0222280849031`;

| node | energy | zero-regulator estimate | stable |
|---|---:|---:|:---:|
| N01_TWO_BRANCH_MID | 0.0785830741606 | 538.94193 -2.91941995e-07 i | yes |
| N02_ANGULAR_CUTOFF | 0.0795445844332 | 842.044317 -4.55904547e-07 i | yes |
| N03_5302_WITNESS | 0.110081677847 | 114.384446 -142.540078 i | yes |
| N04_INNER_HIGH_MID | 0.16697438223 | 406.79027 -1.77386536 i | no |

Decision: **SELECTED_ENERGY_REGULATOR_LADDERS_REQUIRE_REFINEMENT**.

Validation: **FAIL**.

## Claim boundary

These are four selected fixed-decay slices. They do not yet prove
energy interpolation, the energy integral, the decay-angle integral,
the phase-space coefficient, local GR, or the full MTS theory.

## Saved refinement point

The first three energy nodes pass both angular quadrature and regulator-zero
stability. Only `N04_INNER_HIGH_MID` fails. Its order-4/order-8 discrepancy is
localized almost entirely to panel `489`,
`|s| in [0.420812351994717, 0.428317665198399]`. A direct 501-point E0025
scan finds the missed narrow peak at approximately
`|s|=0.425450635554592`, with magnitude `2.45122739708e8` before the physical
multiplier. The next run should split that panel around this second peak and
rerun only the ten N04 regulator/order shards; the other thirty saved shards
remain converged evidence and should not be repeated.
