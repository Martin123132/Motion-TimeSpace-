# 4178 - Y5 R2FR Calibrated Source Coupling Kappa-GN Normalization Or Measured-G Envelope

Branch: `MTS_R2FR_Y5_CALIBRATED_SOURCE_COUPLING_4178`  
Decision: `KAPPA_TO_GN_CALIBRATED_SOURCE_COUPLING_DERIVED_NUMERIC_G_NOT_PREDICTED_PRIVATE_SELECTOR`  
Status: private selector theorem; numerical `G_N` is not predicted.

## Result
The local branch derives the source-coupling form:

```text
G_mu_nu[g_obs] = kappa_eff T_H_mu_nu,
kappa_eff = kappa_* Z_0,
G_cal = c^4 kappa_eff/(8*pi).
```

With `D_A ln kappa_* = 0` and `delta_ZH = 0`:

```text
D_A ln G_cal = 0.
```

The weak-field readout gives:

```text
nabla^2 Phi_N = 4*pi G_cal rho_H,
a_r = -G_cal M_H^dress/r^2.
```

## Meaning
This is the honest GR-like situation: the form of the coupling and Newtonian source law are derived inside the private selector, while the numerical value of `G_cal` is calibrated unless a future parent scale law derives `kappa_*`.

## Anti-Circularity
The mass is `M_H^dress = H_tau[S_link]-H_ref`, not fitted orbital `GM`. The constant `G_cal` is one calibrated constant across local tests, not a hiding place for species, clocks, material labels, ranges, frames, source normalization or boundary flux.

## Output Files
- `formalization-workbench/194-PPC4161-calibrated-source-coupling-kappa-to-GN-law.md`
- `formalization-workbench/02-claims-register.csv` row `L-019`
- `formalization-workbench/180-PPC4161-private-local-packet-integration.md` marker `PPC4161_PACKET_CALIBRATED_SOURCE_COUPLING_4178`
- `formalization-workbench/07-unification-spine.md` marker `PPC4161_CALIBRATED_SOURCE_COUPLING_4178`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_4178_SOURCE_REGISTER.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_4178_COUPLING_DERIVATION_CHAIN.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_4178_ANTI_CIRCULARITY_GUARDS.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_4178_MEASURED_G_ENVELOPE.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_4178_REACTIVATION_LEDGER.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_4178_BRANCH_DECISION.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_4178_CLAIM_FIREWALL.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_4178_STATUS.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_4178_NEXT_TARGET.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_BRR545_4178_VALIDATION.csv`

## Next Target
`4179-Y5-R2FR-local-GR-private-closure-summary-and-global-parent-adoption-burden-map.md`
