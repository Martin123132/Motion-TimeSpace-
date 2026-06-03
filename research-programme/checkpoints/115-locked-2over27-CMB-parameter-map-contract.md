# 115 - Locked 2/27 CMB Parameter-Map Contract

Private checkpoint. This is not a public claim.

## 1. Trigger

Checkpoint 114 passed the CMB distance-prior data dry-run:

```text
locked_2over27_CMB_distance_dryrun_pass_score_blocked_pending_parameter_map
```

The live problem is no longer whether the Planck distance-prior files load.

The live problem is:

```text
what exact parameter map is fair for scoring the locked 2/27 branch against
CMB distance priors?
```

This checkpoint declares that map.

## 2. Short Verdict

```text
CMB_parameter_map_status =
contract_declared_guarded_score_allowed
```

```text
theory_promotion_allowed =
false
```

```text
CMB_public_claim_allowed =
false
```

Plain English:

```text
The next CMB distance score is now allowed, but only under this symmetric
contract.
```

No hidden CMB calibration rescue is allowed for MTS.

No hidden baseline privilege is allowed for LCDM, wCDM, or CPL.

Boxing-score version:

```text
Now we have the rules of the round. Same ring, same gloves, same judges.
```

## 3. Branches to Score

Required score set:

| Branch | Role | Free dynamical parameters | Fixed quantities |
|---|---|---|---|
| `LCDM` | baseline | `Omega_m0`, `h` | flat late-time LCDM shape |
| `wCDM` | flexible baseline | `Omega_m0`, `h`, `w` | constant `w` shape |
| `CPL` | flexible baseline | `Omega_m0`, `h`, `w0`, `wa` | CPL shape |
| `MTS_locked_2over27` | predeclared branch | `Omega_m0`, `h` | `p=3`, `u3=1/4`, `DeltaR=2/9`, `B_mem=2/27` |
| `MTS_Bmem_zero` | negative control | `Omega_m0`, `h` | `p=3`, `u3=1/4`, `B_mem=0` |

Allowed diagnostic only:

```text
MTS_fitted_Bmem_diagnostic
```

but it must never be treated as the holdout branch.

## 4. Parameter Bounds

The same optimizer priors apply to every branch where the parameter exists:

| Parameter | Bounds | Edge flag |
|---|---:|---|
| `Omega_m0` | `[0.05, 0.60]` | within 1 percent of interval edge |
| `h` | `[0.45, 0.90]` | within 1 percent of interval edge |
| `w` | `[-2.0, -0.2]` | within 1 percent of interval edge |
| `w0` | `[-2.0, -0.2]` | within 1 percent of interval edge |
| `wa` | `[-2.0, 2.0]` | within 1 percent of interval edge |

If a branch wins only by sitting on a prior edge, it does not win.

If a baseline sits on an edge, it can be reported but not used as a clean kill-shot against MTS.

## 5. H0/h Rule

Primary rule:

```text
h is fitted from the CMB distance prior for every branch.
```

No branch imports `h` from SH0ES.

No branch imports `h` from a previous SN+BAO fit.

No branch receives a private Planck-H0 prior.

Reason:

```text
BAO-only scoring used an alpha calibration and does not determine the absolute
CMB sound-horizon scale. CMB distance scoring must therefore fit h symmetrically.
```

Parameter count:

```text
h counts as one fitted dynamical parameter for every branch.
```

## 6. Omega_m0 Rule

Primary rule:

```text
Omega_m0 is fitted from the CMB distance prior for every branch.
```

No branch imports `Omega_m0` from BAO-only, SN+BAO, or growth.

Reason:

```text
This is a CMB-distance-only stress test, not yet a joint late+CMB fit.
```

Parameter count:

```text
Omega_m0 counts as one fitted dynamical parameter for every branch.
```

## 7. Baryon and Spectral-Index Rule

The compressed prior vector is:

```text
R, l_A, Omega_b_h2, n_s
```

Primary strict score:

```text
Omega_b_h2 and n_s are fixed to the mean values of the compressed prior table
being scored.
```

This gives residuals:

```text
Delta Omega_b_h2 = 0
Delta n_s = 0
```

Reason:

```text
the current locked MTS branch is a late-time background closure, not a
primordial-baryon or primordial-spectrum theory.
```

Fairness rule:

```text
the same fixed Omega_b_h2 and n_s treatment is used for LCDM, wCDM, CPL,
MTS_locked_2over27, and MTS_Bmem_zero.
```

Parameter count:

```text
Omega_b_h2 and n_s do not count as fitted dynamical parameters in the primary
strict score.
```

Required sensitivity:

```text
also report a two-dimensional marginalized distance-only control using only
R and l_A.
```

If MTS survives only one of these two treatments, the readout is:

```text
CMB_distance_result_sensitive_to_nuisance_treatment
```

not support.

## 8. Radiation and Recombination Rule

Use the repaired CMB-distance convention from checkpoint 30:

```text
N_eff = 3.046
Omega_gamma0 = 2.469e-5 / h^2
Omega_r0 = Omega_gamma0 * (1 + 0.22710731766 N_eff)
```

The CMB scoring branch uses:

```text
E_CMB^2(z) = E_late^2(z) + Omega_r0 (1+z)^4
```

without changing the late-time closure normalization between branches.

The recombination redshift uses the existing Hu/Sugiyama-style fitting formula:

```text
z_star =
1048 [1 + 0.00124 (Omega_b h^2)^(-0.738)]
[1 + g1 (Omega_m h^2)^g2]
```

where:

```text
g1 = 0.0783 (Omega_b h^2)^(-0.238) /
     [1 + 39.5 (Omega_b h^2)^0.763]
g2 = 0.560 / [1 + 21.1 (Omega_b h^2)^1.81]
```

Sensitivity rule:

```text
do not introduce a radiation-renormalized convention in the primary score.
```

If a radiation-normalized variant is later tested, it must be labelled a sensitivity control and applied to all branches.

## 9. Distance Observable Rule

Use the repaired scale-factor quadrature:

```text
D_M(z_star) = (c/H0) integral[a_star, 1] da / [a^2 E(a)]
```

```text
r_s(z_star) = (c/H0) integral[0, a_star] c_s(a) da / [a^2 E(a)]
```

with:

```text
c_s(a) = 1 / sqrt[3(1 + R_b)]
R_b = 31500 Omega_b h^2 a
```

Predicted CMB distance-prior entries:

```text
R = sqrt(Omega_m0) H0 D_M(z_star) / c
l_A = pi D_M(z_star) / r_s(z_star)
```

The finite redshift-grid sound-horizon method is banned for this branch.

## 10. MTS Locked E(z) Rule

The locked branch late-time background is:

```text
E_MTS^2(z) =
Omega_m0 (1+z)^3
+ 1 - Omega_m0
+ B_mem [1 - exp(-(ln(1+z)/u3)^p)]
```

with:

```text
p = 3
u3 = 1/4
B_mem = 2/27
```

No CMB-specific change to `B_mem`, `p`, `u3`, `DeltaR`, `eta`, or `a_F` is allowed.

The direct high-redshift memory contribution is already bounded at recombination, but the line-of-sight distance effect remains testable.

## 11. Compressed-Prior Table Rule

Primary tables:

```text
wCDM compressed prior table
LCDM compressed prior table
```

The `wCDM` table is the local default for C0/MTS continuity.

The `LCDM` table is mandatory because it is the baseline compressed prior most favourable to a strict standard comparison.

Optional context tables:

```text
LCDM_Omega_k
LCDM_A_L
```

Decision rule:

```text
MTS cannot claim CMB-distance survival if it survives only by choosing one
compressed-prior table and fails the other primary table badly.
```

## 12. Information-Criterion Rule

Report against each baseline:

```text
Delta chi2
Delta AIC
Delta BIC
```

Parameter counts:

| Branch | Primary dynamic k |
|---|---:|
| `LCDM` | 2 |
| `wCDM` | 3 |
| `CPL` | 4 |
| `MTS_locked_2over27` | 2 |
| `MTS_Bmem_zero` | 2 |
| `MTS_fitted_Bmem_diagnostic` | 3 |

Use:

```text
AIC = chi2 + 2k
BIC = chi2 + k ln(n)
```

where:

```text
n = 4 for the strict full-vector score
n = 2 for the R,l_A marginalized control
```

The fitted-Bmem diagnostic may be shown but cannot be used to promote the locked branch.

## 13. Boxing Scorecard Gate

This is the fair readout scale:

| Result | Condition | Meaning |
|---|---|---|
| clean win | `Delta BIC < -2` vs LCDM and no edge flags | locked branch wins the round |
| points win | `-2 <= Delta BIC < 0` vs LCDM and no edge flags | small but useful win |
| competitive draw | `abs(Delta BIC) <= 2` and no edge flags | viable enough to keep moving |
| narrow loss | `2 < Delta BIC <= 6` and no edge flags | not fatal, inspect physics/contract |
| hard loss | `Delta BIC > 6` or edge-dependent | CMB distance branch fails this gate |

This is not a knockout-only standard.

If MTS scores a draw while using fewer phenomenological knobs than the flexible baselines, that is scientifically useful.

If MTS loses badly to plain LCDM under the same rules, that is a real branch problem.

## 14. Required Outputs for the Score Script

The next guarded score script must write:

```text
source_register.csv
prior_table_register.csv
model_register.csv
parameter_map_register.csv
fit_summary.csv
prior_edge_table.csv
distance_prior_residuals.csv
baseline_comparisons.csv
scorecard_gates.csv
decision.csv
status.json
```

Required script:

```text
scripts/locked_2over27_CMB_distance_score.py
```

Required first command:

```text
python scripts/locked_2over27_CMB_distance_score.py --dry-run
```

Scoring command is allowed only after the dry-run confirms this contract is encoded:

```text
python scripts/locked_2over27_CMB_distance_score.py --score
```

## 15. Claim Ceiling

Allowed statement after this checkpoint:

```text
The locked 2/27 branch has a declared fair CMB distance-prior scoring contract.
```

Allowed statement after a future score, if it survives:

```text
The locked 2/27 branch survives a compressed CMB distance-prior background
stress test under a symmetric parameter map.
```

Forbidden statement:

```text
MTS passes CMB.
```

Forbidden statement:

```text
MTS predicts the CMB spectrum.
```

Forbidden statement:

```text
The parent field theory is CMB-derived.
```

## 16. Decision

The score gate is now open, but only under the contract above.

Status:

```text
contract_declared_guarded_score_allowed
```

Next target:

```text
116-locked-2over27-CMB-distance-score.md
```

with:

```text
scripts/locked_2over27_CMB_distance_score.py
```

The score will be meaningful only if it reports the boring details:

```text
edge flags, prior-table sensitivity, nuisance-treatment sensitivity, and
LCDM/wCDM/CPL comparisons.
```
