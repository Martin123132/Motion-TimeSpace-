# 114 - Locked 2/27 CMB Distance-Prior Dry-Run

Private checkpoint. This is not a public claim.

## 1. Trigger

Checkpoint 112 predeclared:

```text
canonical_R_2over27_locked_amplitude
```

with:

```text
p = 3
u3 = 1/4
DeltaR = 2/9
B_mem = 2/27
eta = 1
a_F = 1
```

Checkpoint 113 then showed that the locked branch survives the BAO-only DR1/DR2 release stress test.

This checkpoint moves to the next external stress target:

```text
CMB distance-prior dry-run.
```

Important:

```text
no CMB chi2 is generated here.
```

The purpose is to verify that the Planck distance-prior tables and row locks are usable, then explicitly block scoring until the locked branch has a fair CMB parameter-map contract.

## 2. Short Verdict

```text
CMB_distance_dryrun_status =
locked_2over27_CMB_distance_dryrun_pass_score_blocked_pending_parameter_map
```

```text
score_ran =
false
```

```text
theory_promotion_allowed =
false
```

Plain English:

```text
The CMB distance-prior data gate passes, but the actual score is intentionally blocked.
```

Reason:

```text
CMB distance priors require a declared map for H0/h, Omega_m0, Omega_b h^2,
n_s, radiation, z_star, and the repaired sound-horizon integral.
```

Without that map, a CMB chi2 would mostly measure hidden convention choices rather than the locked MTS branch.

Boxing-score version:

```text
This is not a round on the cards yet. It is the referee checking the gloves before we let CMB throw punches.
```

## 3. Machine Artifact

Script:

```text
research-programme\scripts\locked_2over27_CMB_distance_dryrun.py
```

Dry-run:

```text
research-programme\runs\20260531-155808-locked-2over27-CMB-distance-dryrun
```

Generated:

```text
source_register.csv
distance_prior_vector_report.csv
distance_prior_covariance_report.csv
prior_model_register.csv
locked_branch_register.csv
cmb_parameter_map_contract.csv
dryrun_gates.csv
score_blockers.csv
command_templates.csv
decision.csv
status.json
```

## 4. Data Source Gate

Distance-prior source:

```text
Planck2018_distance_priors_Chen_Huang_Wang
```

Machine files checked:

```text
planck2018_distance_prior_vector.csv
planck2018_distance_prior_covariance.csv
covariance_validation.csv
row_lock_manifest.json
```

Source files checked:

```text
1808.05724-abs.html
1808.05724-eprint.tar.gz
1808.05724.pdf
```

Source gate:

| Gate | Result |
|---|---:|
| Missing source files | 0 |
| Vector rows checked | 16 |
| Covariance models checked | 4 |
| Failed vector rows | 0 |
| Failed covariance reconstructions | 0 |

## 5. Prior Tables

The row-lock manifest reports:

| Prior table | Parameters | Covariance | Default for C0/MTS | Status |
|---|---|---|---|---|
| `LCDM` | `R,l_A,Omega_b_h2,n_s` | 4x4 | false | pass |
| `wCDM` | `R,l_A,Omega_b_h2,n_s` | 4x4 | true | pass |
| `LCDM_Omega_k` | `R,l_A,Omega_b_h2,n_s` | 4x4 | false | pass |
| `LCDM_A_L` | `R,l_A,Omega_b_h2,n_s` | 4x4 | false | pass |

The default available compressed table is:

```text
wCDM
```

This is acceptable for an internal stress test only. It is not enough for a public CMB claim because compressed distance priors are model-dependent summaries.

## 6. Covariance Reconstruction

All four covariance matrices reconstruct as finite, symmetric, positive-definite matrices.

| Prior table | Rows seen | Cholesky | Minimum eigenvalue | Status |
|---|---:|---|---:|---|
| `LCDM` | 16 | pass | 1.263158117956702e-08 | pass |
| `wCDM` | 16 | pass | 1.2617393277352042e-08 | pass |
| `LCDM_Omega_k` | 16 | pass | 1.2626285080244737e-08 | pass |
| `LCDM_A_L` | 16 | pass | 1.3860406327571146e-08 | pass |

This means the data machinery is ready.

It does not mean the locked branch is ready to be scored.

## 7. Locked Branch Register

The dry-run freezes:

| Quantity | Value | Status |
|---|---:|---|
| `p` | 3 | frozen |
| `u3` | 0.25 | frozen |
| `DeltaR` | 0.2222222222222222 | frozen |
| `B_mem` | 0.07407407407407407 | frozen |
| `eta` | 1 | frozen |
| `a_F` | 1 | frozen |

No CMB-specific retuning is allowed.

## 8. Dry-Run Gates

| Gate | Status | Evidence |
|---|---|---|
| source files exist | pass | missing_count = 0 |
| distance-prior vector parses | pass | 16 rows, 0 failures |
| distance-prior covariance reconstructs | pass | 4 models, 0 failures |
| default wCDM prior available | pass | default_model = wCDM |
| locked 2/27 constants frozen | pass | p=3, u3=1/4, DeltaR=2/9, B_mem=2/27 |
| repaired sound-horizon method required | pass | future score must use scale-factor quadrature |
| compressed-prior model dependence | warning | score must check LCDM and wCDM prior tables |
| locked-branch CMB parameter map | blocked | H0/h, Omega_m0, Omega_b h2, n_s, radiation, z_star undeclared |
| CMB distance score execution | blocked | no chi2 generated |

Readout:

```text
data gate passes;
physics scoring gate remains closed.
```

That is the correct conservative move.

## 9. Score Blockers

The next CMB score cannot be run honestly until these are declared:

| Blocker | Severity | Required resolution |
|---|---|---|
| H0/h treatment undeclared | blocking | fixed, fitted, imported, or jointly optimized rule shared with baselines |
| Omega_m0 treatment undeclared | blocking | CMB-only, BAO-imported, or joint-optimized protocol |
| Omega_b h2 and n_s nuisance treatment undeclared | blocking | fixed means or covariance-fitted nuisance handling |
| early radiation and z_star convention undeclared | blocking | lock Tcmb, N_eff, radiation density, z_star, and scale-factor quadrature |
| compressed-prior table sensitivity not yet run | warning after map | score at least LCDM and wCDM prior tables |
| no perturbation closure | claim ceiling | report only as background-distance stress |

## 10. Interpretation

Allowed statement:

```text
The locked B_mem=2/27 branch now has a validated CMB distance-prior dry-run gate:
the Planck compressed-prior tables load, reconstruct, and pass covariance checks.
```

Allowed statement:

```text
The CMB score is blocked for good scientific reasons until a symmetric parameter-map
contract is written for the locked branch and baselines.
```

Forbidden statement:

```text
MTS passes CMB.
```

Forbidden statement:

```text
The locked 2/27 branch predicts the CMB distance priors.
```

## 11. Decision

The CMB distance-prior machinery is not the problem anymore.

The live problem is:

```text
What exactly is the fair parameter map from the locked branch to CMB observables?
```

That map must be written before scoring.

## 12. Next Target

Create:

```text
115-locked-2over27-CMB-parameter-map-contract.md
```

Purpose:

```text
declare the exact local rules for H0/h, Omega_m0, Omega_b h2, n_s, radiation,
z_star, sound horizon, compressed-prior table sensitivity, and fair baseline
symmetry before any CMB chi2 is allowed.
```

If that contract passes, the next machine step is a guarded score script:

```text
scripts/locked_2over27_CMB_distance_score.py
```

If it does not pass, the CMB branch remains:

```text
dry-run-ready but score-blocked.
```
