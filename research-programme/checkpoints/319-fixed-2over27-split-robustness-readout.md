# 319 — Fixed `2/27` Split-Robustness Readout

## Status

This is a stronger private diagnostic for the locked late-time branch, not a public evidence claim.

- Runner: `scripts/fixed_2over27_split_robustness_matrix.py`
- Run: `runs/20260601-125900-fixed-2over27-split-robustness-matrix`
- Status: `fixed_2over27_split_robustness_survives_first_pass_diagnostic_only`
- Claim ceiling: `late_time_background_split_diagnostic_only_no_parent_CMB_or_local_GR_promotion`

## What was tested

The fixed branch was tested symmetrically against the same baselines, same data cuts, same nuisance treatment, and same no-SH0ES calibration policy.

Models:

- `LCDM`
- `wCDM`
- `CPL`
- `MTS_fixed_2over27_no_clock`
- `MTS_Bmem_zero`

Scenarios:

- DESI DR2 full-cov no-SH0ES and DESI DR1 full-cov no-SH0ES.
- Full reference runs.
- SN low/high-redshift half splits with all BAO retained.
- BAO observable-class leave-outs: without `DH_over_rs`, without `DM_over_rs`, without `DV_over_rs`.
- BAO low/high-redshift half splits with all SN retained.

Total: 16 split scenarios and 80 model fits.

## Result

This is a good result for the fixed branch, but it is still not a derivation.

Against `LCDM`:

- Raw chi-square wins: 15/16.
- AIC wins: 15/16.
- BIC wins: 15/16.
- Median `Delta_BIC`: `-3.48951687710678`.
- Worst `Delta_BIC`: `+0.5301498792798611`, a close-round loss in `DESI_DR1_fullcov_noSH0ES / BAO_high_z_half_plus_all_SN`.
- Best `Delta_BIC`: `-5.865248582431946`.

Against `wCDM`:

- Raw chi-square wins: 8/16.
- AIC wins: 16/16.
- BIC wins: 16/16.
- Median `Delta_BIC`: `-7.229301587645864`.
- Worst `Delta_BIC`: `-5.6799468992114726`.

Against `CPL`:

- Raw chi-square wins: 0/16, as expected for a more flexible baseline.
- AIC wins: 14/16.
- BIC wins: 16/16.
- Median `Delta_BIC`: `-13.69695791201832`.
- Worst `Delta_BIC`: `-8.258680237312205`.

The boxing readout is: the fixed branch is not knocking the baselines out by miles, but it is staying in the ring cleanly. It wins most of the simple rounds against `LCDM`, and it wins the information-criterion cards against the more flexible baselines because it is not buying its fit with extra freedom.

## Fairness notes

- `MTS_Bmem_zero` tracks `LCDM` in every split, so the memory term is the actual moving part.
- All models converged.
- The strict fixed branch has no fitted prior-edge flags.
- One baseline edge flag occurs: `CPL` hits `Omega_m = 0.05` in `DESI_DR1_fullcov_noSH0ES / BAO_low_z_half_plus_all_SN`.
- That baseline edge is reported, but it should not be counted as a fixed-branch failure.

## Derivation consequence

This result raises the value of the `B_mem = 2/27` target, but it does not derive it.

The current derivation ladder is:

1. FLRW projection gives the shape conditionally: `F(N) = 1 - exp[-(N/u3)^3]`.
2. The background limit is clean: `B_mem -> 0` exactly returns `LCDM`.
3. The empirical branch now prefers the locked value `B_mem = 2/27` across DR1/DR2 and first split stress.
4. The parent action still must explain why the amplitude is exactly `2/27`.

The most plausible amplitude route remains:

```text
B_mem = kappa_mem * rank(P_active) / dim(V_cell)
```

with the required locks:

```text
rank(P_active) = 2
dim(V_cell) = 27
kappa_mem = 1
```

The Ward/conservation route cannot fix `kappa_mem = 1` by itself because it is homogeneous under rescaling of the memory action. Therefore the missing theorem must be a non-homogeneous normalization theorem: an index, trace, flux-quantization, boundary-charge, or measure-normalization condition.

## Current verdict

Not grim. The local-GR branch is still hard, and the CMB bridge is still unresolved, but the late-time fixed branch just passed a fairer split test than the earlier smoke runs.

The honest position is:

- `B_mem = 2/27` is no longer just numerology-level interesting.
- It is still not parent-derived.
- The next serious theory move is to either derive the `2/27` amplitude from the parent cell/action structure or explicitly demote it to a locked empirical closure.

## Next step

Attempt the parent amplitude theorem directly:

1. Define the cell vector space whose natural dimension is `27`.
2. Derive why the active FLRW memory projector has rank `2`.
3. Find or reject a non-homogeneous condition that fixes `kappa_mem = 1`.
4. If any one of those fails, keep the late-time branch as a closure and move the derivation pressure to external `Hz`, growth, CMB bridge, and local-GR compatibility tests.
