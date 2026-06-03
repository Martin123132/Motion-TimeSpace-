# 124 - BAO Shape Residual Decomposition

Private checkpoint. This is not a public claim.

## 1. Trigger

Checkpoint 123 demoted compressed CMB background priors to closure-only and
selected the next fair empirical move:

```text
decompose the BAO shape residual row by row.
```

The aim is not to rescue the branch. The aim is to locate the exact residual
pattern that a future theorem would have to explain.

## 2. Machine Artifact

Script:

```text
research-programme\scripts\BAO_shape_residual_decomposition.py
```

Run:

```text
research-programme\runs\20260531-173800-BAO-shape-residual-decomposition
```

Generated:

```text
source_register.csv
branch_chi2_summary.csv
bao_row_residuals.csv
observable_group_summary.csv
redshift_group_summary.csv
mts_delta_vs_T7_by_row.csv
mts_delta_vs_T7_by_observable.csv
mts_delta_vs_T7_by_redshift.csv
primary_failed_gate_drivers.csv
decision.csv
status.json
```

Status:

```text
BAO_shape_residual_decomposition_complete
```

Claim ceiling:

```text
diagnostic_residual_map_only
```

## 3. Method

Same BAO data for all branches:

```text
DESI DR2 primary BAO, 13 rows, full covariance.
```

Branches scored:

```text
46 branches
598 row residuals
```

Included branch families:

```text
late_T1_free_alpha
late_T7_locked_2over27_free_alpha
joint_tied_alpha
CMB_only_free_alpha_shape
```

The decomposition uses covariance-signed row contributions:

```text
contribution_i = residual_i (C_BAO^-1 residual)_i.
```

These contributions sum to total BAO chi2, but individual rows can be negative
because the BAO covariance is correlated. So this is a diagnostic influence
map, not a set of independent chi2 bins.

## 4. Primary Failed Gate

The branch under the microscope is:

```text
joint_tied_alpha__LCDM__strict_full4__MTS_locked_2over27
```

This was the one hard-loss joint gate from checkpoint 119/120.

BAO comparison against the late-only locked T7 branch:

| Quantity | Value |
|---|---:|
| T7 locked late-only BAO chi2 | `8.169575390292101` |
| failed joint gate BAO chi2 | `13.010665920280031` |
| BAO delta vs T7 | `4.84109052998793` |

Readout:

```text
the hard gate is now localized to a 4.84109 BAO shape penalty.
```

## 5. Observable Decomposition

For the failed gate, the MTS delta against T7 by observable is:

| Observable | Rows | Signed delta | Positive delta | Negative delta |
|---|---:|---:|---:|---:|
| `DH_over_rs` | 6 | `3.7171698689088206` | `3.8756384884099426` | `-0.158468619501122` |
| `DM_over_rs` | 6 | `0.22469316626669691` | `2.3309382872803153` | `-2.1062451210136186` |
| `DV_over_rs` | 1 | `0.8992274948124139` | `0.8992274948124139` | `0` |

Dominant observable:

```text
DH_over_rs.
```

Interpretation:

```text
The main penalty is radial-expansion shape, not simply transverse distance.
```

`DM_over_rs` has substantial movement, but it partly cancels because the
`z=0.51` transverse row improves relative to T7.

## 6. Redshift Decomposition

For the failed gate, the redshift groups are:

| z | Rows | Signed delta | Positive delta | Negative delta |
|---:|---:|---:|---:|---:|
| `0.934` | 2 | `1.7190551718646399` | `1.7190551718646399` | `0` |
| `2.33` | 2 | `1.3343207789010494` | `1.3343207789010494` | `0` |
| `0.706` | 2 | `1.082624620054263` | `1.241093239555385` | `-0.158468619501122` |
| `1.321` | 2 | `1.104704604638844` | `1.166828473964046` | `-0.062123869325202065` |
| `0.295` | 1 | `0.8992274948124139` | `0.8992274948124139` | `0` |
| `0.51` | 2 | `-1.5468401437109258` | `0.4972811079774906` | `-2.0441212516884164` |
| `1.484` | 2 | `0.24799800342764705` | `0.24799800342764705` | `0` |

Dominant redshift group:

```text
z = 0.934.
```

But the pattern is not a single rogue point. The positive penalty is spread
across:

```text
z = 0.706, 0.934, 1.321, 2.33
```

plus the low-redshift `DV/rs` point at:

```text
z = 0.295.
```

## 7. Top Row Drivers

Largest positive penalty rows:

| Rank | z | Observable | Delta vs T7 |
|---:|---:|---|---:|
| 1 | `0.706` | `DM_over_rs` | `1.241093239555385` |
| 2 | `1.321` | `DH_over_rs` | `1.166828473964046` |
| 3 | `0.934` | `DH_over_rs` | `1.1481403472705145` |
| 4 | `2.33` | `DH_over_rs` | `0.9225971051639887` |
| 5 | `0.295` | `DV_over_rs` | `0.8992274948124139` |
| 6 | `0.934` | `DM_over_rs` | `0.5709148245941253` |
| 7 | `0.51` | `DH_over_rs` | `0.4972811079774906` |
| 8 | `2.33` | `DM_over_rs` | `0.41172367373706065` |

Largest offsets/improvements:

| Rank | z | Observable | Delta vs T7 |
|---:|---:|---|---:|
| 1 | `0.51` | `DM_over_rs` | `-2.0441212516884164` |
| 2 | `0.706` | `DH_over_rs` | `-0.158468619501122` |
| 3 | `1.321` | `DM_over_rs` | `-0.062123869325202065` |

Readout:

```text
The failed joint branch pays mostly radial DH/rs penalties, while one
transverse row at z=0.51 improves enough to hide part of the transverse cost.
```

## 8. CMB-Compatible Shape Probe

The CMB-only locked shape, confronted with BAO using free alpha, is worse than
the joint compromise:

| Prior table | Mode | `Omega_m0` | BAO chi2 | Delta vs T7 |
|---|---|---:|---:|---:|
| `wCDM` | `strict_full4` | `0.3295740146787432` | `15.907365531657566` | `7.7377901413654655` |
| `wCDM` | `marginal_R_lA` | `0.32957399350906025` | `15.907353266120026` | `7.737777875827925` |
| `LCDM` | `strict_full4` | `0.331286732138333` | `16.928380426631904` | `8.758805036339803` |
| `LCDM` | `marginal_R_lA` | `0.3312867941619584` | `16.928418433525465` | `8.758843043233364` |

So:

```text
CMB-only Omega_m0 is even less BAO-shape friendly than the joint compromise.
```

This supports checkpoint 122:

```text
the issue is the CMB-driven upward Omega_m0 pressure, not alpha calibration.
```

## 9. Theory Target

The next theorem target is no longer vague.

A future derivation would need to explain why the memory sector modifies, or
does not modify, primarily:

```text
D_H(z) / r_s
```

across roughly:

```text
0.7 <= z <= 2.33,
```

without wrecking:

```text
D_M(z) / r_s at z = 0.51,
```

which currently improves relative to T7 in the failed joint branch.

In physical terms:

```text
the target is radial expansion H(z), not just a distance-ladder calibration.
```

## 10. Decision

Allowed statement:

```text
The joint BAO shape penalty is now localized: it is dominated by DH/rs and a
spread of redshift rows, especially z = 0.934, 1.321, 2.33, and 0.706.
```

Allowed statement:

```text
This is a diagnostic theorem target for H(z)-like radial expansion behaviour.
```

Forbidden statement:

```text
MTS has a BAO-shape correction.
```

Forbidden statement:

```text
MTS passes joint late+CMB cosmology.
```

Current status:

```text
diagnostic map complete; no promotion; no rescue term added.
```

## 11. Next Target

Next checkpoint:

```text
125-BAO-shape-theorem-target-or-non-CMB-stress-route.md
```

Recommended move:

```text
Build an H(z)/radial-expansion stress route before attempting a full CMB
perturbation machine.
```

Reason:

```text
The residual is radial-expansion dominated, so the fairest next empirical
question is whether independent H(z)-like data agree with the BAO radial
pressure or expose it as a DESI/compressed-bridge artefact.
```

