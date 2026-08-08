# 3967 - Second Order PPN Source Stability Or Delta PPN Bound

Timestamp: `2026-07-01T15:36:24+00:00`

## Result

3967 pushes the Newton bridge into the real local-GR danger zone: second-order PPN source stability.

The useful derived piece is not a claim of local GR. It is the fixed-`GM` bookkeeping:

```text
U := G_obs M_obs/r = A_source W
g_00 = -1 + 2 A_source W/c^2 - 2 B_source W^2/c^4 + O(c^-6)
beta_eff = B_source/A_source^2
delta_beta_source = B_source/A_source^2 - 1
```

So a Newtonian fit only fixes the first-order amplitude. It does **not** fix `beta`.
The clean route is now sharp: prove `B_source = A_source^2` from the parent/source coupling, or keep a finite beta residual.

## PPN Vector

The source-stability vector is now:

```text
Delta_PPN_source =
  (delta_gamma_source,
   delta_beta_source,
   delta_beta_operator,
   delta_beta_q_loc,
   delta_beta_boundary_domain,
   delta_beta_readout,
   alpha1_source,
   alpha2_source,
   alpha3_source,
   xi_source,
   zeta1_source,
   zeta2_source,
   zeta3_source,
   zeta4_source)
```

with the no-cancellation envelope:

```text
Delta_PPN_abs =
 |delta_gamma| + |delta_beta_total| + |alpha1| + |alpha2| + |alpha3| + |xi| + sum_i |zeta_i|
```

## Comparator Status

- Gamma, beta, alpha1, alpha2, alpha3, and xi comparator rows are imported from existing local PPN ledgers.
- Zeta comparator rows are explicitly marked acquisition-required.
- No generated row is valid for public/local-GR claim.

## Source Intake

Source needles found: `27/27`.

## Outputs

- `source-intake/mts_residuals/P8_Y5_R2FR_3967_PPN_STABILITY_THEOREM_OR_BOUND.csv`
- `source-intake/mts_residuals/P8_Y5_R2FR_3967_PPN_RESIDUAL_VECTOR.csv`
- `source-intake/mts_residuals/P8_Y5_R2FR_3967_BETA_AB_LAW_ROLLED_FORWARD.csv`
- `source-intake/mts_residuals/P8_Y5_R2FR_3967_EMPIRICAL_BOUND_INTERFACE.csv`
- `source-intake/mts_residuals/P8_Y5_R2FR_3967_LOCAL_GR_GATE_FEED_UPDATE.csv`
- `source-intake/mts_residuals/P8_Y5_BRR545_3967_VALIDATION.csv`

## Decision

The best next attack is not another broad audit. It is the hard derivation:

```text
B_source = A_source^2
```

If that parent/source-coupling square law closes, the local GR route gets substantially stronger.
If it fails, the beta branch becomes a finite residual vector and must be tested.
