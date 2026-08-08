# 5307 — N04 secondary-peak adaptive refinement

## Repair

The 5306 order discrepancy was isolated to one N04 panel. A local
E0025 scan resolves a second narrow peak and the panel is replaced by
nested 1e-5, 2e-6, and 4e-7 angular spacing around that peak.
The thirty converged parent integral rows are reused unchanged; only
the ten N04 regulator/order shards are recomputed.

- secondary peak: `0.425456729868914`;
- refined panels: `881`;
- completed refined shards: `10/10`;
- N04 maximum order change: `0.000107888359207`;
- maximum final Richardson change: `0.000168346416487`;
- maximum model-intercept change: `0.000139738947771`;

| node | energy | zero-regulator estimate | stable |
|---|---:|---:|:---:|
| N01_TWO_BRANCH_MID | 0.0785830741606 | 538.94193 -2.91941995e-07 i | yes |
| N02_ANGULAR_CUTOFF | 0.0795445844332 | 842.044317 -4.55904547e-07 i | yes |
| N03_5302_WITNESS | 0.110081677847 | 114.384446 -142.540078 i | yes |
| N04_INNER_HIGH_MID | 0.16697438223 | 215.178935 -95.30929 i | yes |

Decision: **FOUR_SELECTED_ENERGY_REGULATOR_ZERO_LIMITS_RESOLVED__TEST_ENERGY_INTERPOLATION_AND_CUBATURE**.

Validation: **PASS**.

## Claim boundary

This controls four selected fixed-decay energy slices. It does not
yet establish continuous energy interpolation, the energy integral,
the decay-angle integral, the full phase-space coefficient, local
GR, or the full MTS theory.
