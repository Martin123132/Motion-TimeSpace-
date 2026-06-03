# 118 - Locked 2/27 Joint Late-CMB Calibration Contract

Private checkpoint. This is not a public claim.

## 1. Trigger

Checkpoint 117 found:

```text
late SN+BAO Omega_m0 -> CMB with only h profiled fails.
```

The primary late locked branch used:

```text
Omega_m0 = 0.3032827426766658
B_mem = 2/27
p = 3
u3 = 1/4
```

The CMB-only compressed-distance fit preferred:

```text
Omega_m0 about 0.330-0.331
h about 0.666-0.667
```

The simple transfer therefore exposed a real map tension:

```text
Delta Omega_m0 about -0.026 to -0.028.
```

This checkpoint defines the next fair test:

```text
one joint late+CMB calibration map.
```

## 2. Short Verdict

```text
joint_calibration_contract_status =
declared_score_not_yet_run
```

```text
theory_promotion_allowed =
false
```

```text
absolute_calibration_claim_allowed =
false_until_joint_score_passes
```

Plain English:

```text
The next score must stop giving late SN+BAO and CMB separate calibration
freedoms. h, r_d, SN offset, BAO scale, Omega_m0, and B_mem must live in one
shared parameter map.
```

Boxing-score version:

```text
No more winning separate sparring rounds. Now it has to fight a proper combined
round with the same stance all the way through.
```

## 3. What Counts as Joint

A genuine joint late+CMB test must use one shared set:

```text
Omega_m0
h
r_d
late-time background parameters
CMB distance parameters
SN offset nuisance
```

For the locked MTS branch:

```text
B_mem = 2/27
p = 3
u3 = 1/4
DeltaR = 2/9
```

are frozen.

Not allowed:

```text
late SN+BAO fits Omega_m0 independently;
CMB fits Omega_m0 independently;
BAO uses a free alpha unrelated to h and r_d;
MTS gets a private calibration parameter not given to LCDM/wCDM/CPL.
```

## 4. Data Branch

Primary joint score uses the same data as the primary late branch plus the compressed CMB distance prior:

| Sector | Data | Treatment |
|---|---|---|
| SN | Pantheon+ `mb-corr` no-SH0ES | full covariance, calibrators excluded |
| BAO | DESI DR2 primary | full covariance |
| CMB | Planck 2018 compressed distance prior | `wCDM` and `LCDM` prior tables |

Primary score modes:

```text
strict_full4 = R, l_A, Omega_b_h2, n_s
marginal_R_lA = R, l_A
```

The `wCDM` compressed table remains the continuity/default table.

The `LCDM` compressed table is mandatory sensitivity.

## 5. Joint Parameter Map

Shared parameters for every branch:

| Parameter | Meaning | Bounds | Counts in k |
|---|---|---:|---:|
| `Omega_m0` | present matter fraction in E(z) and CMB shift parameter | `[0.05, 0.60]` | yes |
| `h` | `H0/100` used in CMB and BAO absolute scale | `[0.45, 0.90]` | yes |
| `r_d` | BAO drag scale in Mpc | `[80, 200]` | yes |
| `SN_offset` | Pantheon+ absolute nuisance offset | analytic/profiled | yes |

Branch-specific parameters:

| Branch | Extra parameters | Frozen quantities |
|---|---|---|
| `LCDM` | none | flat LCDM form |
| `wCDM` | `w` | constant-w form |
| `CPL` | `w0`, `wa` | CPL form |
| `MTS_locked_2over27` | none | `B_mem=2/27`, `p=3`, `u3=1/4`, `DeltaR=2/9` |
| `MTS_Bmem_zero` | none | `B_mem=0`, `p=3`, `u3=1/4` |

Diagnostic only:

```text
MTS_fitted_Bmem_diagnostic
```

It may be reported, but it is not the holdout branch.

## 6. BAO Calibration Rule

The old BAO-only and SN+BAO runners used an analytic free scale:

```text
alpha_BAO
```

The joint test must replace that with:

```text
alpha_BAO = c / (100 h r_d)
```

with:

```text
c = 299792.458 km/s
H0 = 100 h km/s/Mpc
r_d in Mpc
```

Predictions:

```text
D_M(z)/r_d = alpha_BAO integral[0,z] dz'/E(z')
D_H(z)/r_d = alpha_BAO / E(z)
D_V(z)/r_d = alpha_BAO [z (integral[0,z] dz'/E)^2 / E(z)]^(1/3)
```

This is the key fairness move:

```text
BAO alpha is no longer a private free nuisance; it is the same h-r_d calibration
seen by the CMB side of the fit.
```

## 7. SN Calibration Rule

The primary no-SH0ES score does not use Cepheid/local-H0 calibration.

Therefore:

```text
SN_offset remains an analytic/profiled nuisance common to all branches.
```

It absorbs the absolute magnitude/H0 degeneracy in the SN-only distance modulus.

It must count in the information criteria:

```text
k_SN_offset = 1
```

Not allowed in the primary branch:

```text
local-H0 prior;
SH0ES calibrator rows;
different SN offset treatment for MTS and baselines.
```

SH0ES/local-H0 pressure may be a later sensitivity branch only.

## 8. CMB Calibration Rule

Use the same repaired CMB convention as checkpoints 115-116:

```text
N_eff = 3.046
Omega_gamma0 = 2.469e-5 / h^2
Omega_r0 = Omega_gamma0 (1 + 0.22710731766 N_eff)
```

Use:

```text
E_CMB^2(z) = E_late^2(z) + Omega_r0 (1+z)^4
```

Use the repaired scale-factor quadrature:

```text
D_M(z_star) = (c/H0) integral[a_star,1] da / [a^2 E(a)]
r_s(z_star) = (c/H0) integral[0,a_star] c_s(a) da / [a^2 E(a)]
```

with the same `z_star` fitting formula used in checkpoint 116.

Primary strict treatment:

```text
Omega_b_h2 and n_s fixed to the mean values of the compressed prior table.
```

Mandatory sensitivity:

```text
R,l_A only.
```

## 9. Drag-Horizon Rule

Primary joint calibration treats:

```text
r_d
```

as a shared late-CMB calibration nuisance, not as a derived parent-theory prediction.

Reason:

```text
the current parent action has not derived the baryon-drag sound horizon or an
MTS-specific early-universe transfer function.
```

Guardrails:

| Rule | Requirement |
|---|---|
| broad bound | `80 <= r_d <= 200` Mpc |
| physical warning band | report if `r_d < 130` or `r_d > 160` Mpc |
| edge flag | fail promotion if `r_d` sits within 1 percent of the prior edge |
| no private rescue | same `r_d` freedom for LCDM, wCDM, CPL, MTS locked, and zero-memory control |

Optional later branch:

```text
derived_drag_horizon_control
```

using a declared `z_drag` and sound-horizon integral.

That optional branch cannot be used to promote MTS until the same early-sector assumptions are applied to baselines.

## 10. Parameter Counts

Primary dynamic parameter counts:

| Branch | Parameters counted | k |
|---|---|---:|
| `LCDM` | `Omega_m0`, `h`, `r_d`, `SN_offset` | 4 |
| `wCDM` | `Omega_m0`, `h`, `r_d`, `w`, `SN_offset` | 5 |
| `CPL` | `Omega_m0`, `h`, `r_d`, `w0`, `wa`, `SN_offset` | 6 |
| `MTS_locked_2over27` | `Omega_m0`, `h`, `r_d`, `SN_offset` | 4 |
| `MTS_Bmem_zero` | `Omega_m0`, `h`, `r_d`, `SN_offset` | 4 |
| `MTS_fitted_Bmem_diagnostic` | `Omega_m0`, `h`, `r_d`, `B_mem`, `SN_offset` | 5 |

Use:

```text
AIC = chi2 + 2k
BIC = chi2 + k ln(n)
```

where:

```text
n = N_SN + N_BAO + N_CMB
```

for each score mode.

## 11. Required Controls

The joint runner must produce these controls before interpretation:

| Control | Purpose | Required result |
|---|---|---|
| `alpha_free_late_control` | reproduce T7 late score with free BAO alpha | confirms no regression in late runner |
| `CMB_only_control` | reproduce checkpoint 116 CMB-only draw | confirms no regression in CMB machinery |
| `late_to_CMB_transfer_control` | reproduce checkpoint 117 simple transfer fail | confirms the tension is still visible |
| `joint_h_rd_score` | main test with `alpha=c/(100hr_d)` | real discriminator |
| `r_d_prior_sensitivity` | repeat broad and physical-warning bands | checks whether result relies on weird drag scale |

If any control fails, the joint score is not interpretable.

## 12. Acceptance Gates

For `MTS_locked_2over27` to survive the joint gate:

| Gate | Pass condition |
|---|---|
| convergence | all required branches converge or are explicitly marked failed |
| edge flags | locked branch has no `Omega_m0`, `h`, or `r_d` edge hit |
| late degradation | SN+BAO chi2 penalty versus T7 locked branch is `<= 2` for clean pass, `<= 6` for soft pass |
| CMB degradation | CMB chi2 penalty versus CMB-only locked branch is `<= 2` for clean pass, `<= 6` for soft pass |
| joint IC | locked branch is at least a competitive draw versus LCDM by BIC, or the loss is explicitly narrow |
| zero-memory control | locked branch improves over `MTS_Bmem_zero` in chi2/AIC or the memory branch is demoted |
| flexible baselines | comparisons to `wCDM` and `CPL` reported symmetrically |
| r_d plausibility | `r_d` not edge-hit; physical-warning band reported |

Boxing scorecard:

| Result | Condition |
|---|---|
| clean win | beats LCDM BIC and passes late/CMB degradation gates |
| points win | beats LCDM AIC or draws BIC within 2 |
| competitive draw | `abs(Delta BIC) <= 2` and no edge flags |
| narrow loss | `2 < Delta BIC <= 6` with degradation gates not catastrophic |
| hard loss | `Delta BIC > 6`, edge-dependent, or late/CMB degradation `> 6` |

## 13. Failure Interpretation

If the locked branch fails the joint gate, the allowed conclusion is:

```text
locked 2/27 remains a strong late-time empirical closure but has unresolved
late-CMB calibration transfer.
```

Forbidden conclusion:

```text
MTS is dead.
```

Reason:

```text
the parent action still has not derived the absolute calibration map, baryon
drag scale, or perturbation-level CMB sector.
```

But the branch must not be promoted if this fails.

## 14. Required Machine Outputs

Next runner:

```text
scripts/locked_2over27_joint_late_CMB_calibration_runner.py
```

Dry-run command:

```text
python scripts/locked_2over27_joint_late_CMB_calibration_runner.py --dry-run
```

Score command:

```text
python scripts/locked_2over27_joint_late_CMB_calibration_runner.py --score
```

Required outputs:

```text
source_register.csv
data_schema_report.csv
model_register.csv
parameter_map_register.csv
control_reproduction.csv
fit_summary.csv
sector_chi2_breakdown.csv
prior_edge_table.csv
rd_plausibility_table.csv
baseline_comparisons.csv
joint_gates.csv
decision.csv
status.json
```

The runner must not write into:

```text
formalization-workbench
```

## 15. Claim Ceiling

Allowed after this checkpoint:

```text
The fair joint late+CMB calibration contract is declared.
```

Allowed only after a future passing score:

```text
The locked 2/27 branch survives a joint compressed-background late+CMB
calibration stress test.
```

Still forbidden:

```text
MTS passes CMB.
MTS predicts the CMB spectrum.
MTS derives r_d.
MTS is a complete unified field theory.
```

## 16. Decision

Status:

```text
joint_late_CMB_calibration_contract_declared_score_next
```

Next target:

```text
119-locked-2over27-joint-late-CMB-calibration-runner.md
```

with:

```text
scripts/locked_2over27_joint_late_CMB_calibration_runner.py
```

This is the right next fight:

```text
not another separate arena score,
but one shared calibration map across SN, BAO, and compressed CMB distance.
```
