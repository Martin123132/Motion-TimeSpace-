# 199 - BAO Alpha Parent or Shared Nuisance Policy

Private theory checkpoint. This is not a public BAO claim.

## 1. Trigger

Checkpoint 198 showed:

```text
the tiny H0-bridge dot_C/H residual is BAO-safe,
but BAO alpha is not parent-owned.
```

This checkpoint decides how alpha is allowed to be used:

```text
fair empirical nuisance,
MTS-only rescue,
or parent-owned prediction.
```

## 2. Machine Artifact

Script:

```text
scripts/BAO_alpha_parent_or_shared_nuisance_policy.py
```

Run:

```text
runs/20260601-000016-BAO-alpha-parent-or-shared-nuisance-policy
```

Command:

```text
python scripts/BAO_alpha_parent_or_shared_nuisance_policy.py --timestamp 20260601-000016
```

Status:

```text
BAO_alpha_shared_nuisance_fair_parent_owner_missing
```

Claim ceiling:

```text
BAO_alpha_policy_internal_only_shared_nuisance_not_prediction
```

## 3. What Alpha Is in the Runner

The BAO prediction code uses:

```text
D_M/r_d = alpha * integral dz/E(z),
D_H/r_d = alpha / E(z),
D_V/r_d = alpha * [z D_M^2/E(z)]^(1/3).
```

So, physically:

```text
alpha ~ c / (H0 r_d).
```

It is a global BAO scale calibration.

In the current BAO-only runner, alpha is not MTS-only:

| model | fitted |
|---|---|
| `LCDM` | `Omega_m; BAO alpha` |
| `wCDM` | `Omega_m; w; BAO alpha` |
| `CPL` | `Omega_m; w0; wa; BAO alpha` |
| `MTS_locked_2over27` | `Omega_m; BAO alpha` |
| `MTS_Bmem_zero` | `Omega_m; BAO alpha` |
| `MTS_fitted_Bmem_diagnostic` | `Omega_m; B_mem; BAO alpha` |

Therefore:

```text
alpha is fair for empirical comparison because every branch gets it.
```

But:

```text
alpha is not a field-theory prediction.
```

## 4. Fitted Alpha Readback

Using:

```text
rdrag = 147.10139220381296
```

the locked 2/27 BAO-only fits read back:

| release | locked alpha | effective H0 if `rdrag` fixed |
|---|---:|---:|
| DESI DR2 | `30.02925466330115` | `67.86711171776678` |
| DESI DR1 | `29.937985423791293` | `68.07401206815871` |

This is useful because it tells us what parent alpha would have to own:

```text
roughly H0*r_d corresponding to H0 ~ 67.9-68.1 for fixed rdrag.
```

## 5. Candidate Parent Alpha Branches

Compare candidate H0 branches against the DESI DR2 locked alpha:

| candidate | alpha | delta vs DR2 locked alpha | status |
|---|---:|---:|---|
| late-reference H0 with `rdrag` | `29.785829426978175` | `-0.24342523632297386` | candidate, not selected |
| same-density CMB-profile H0 with `rdrag` | `30.916005439216264` | `0.8867507759151145` | candidate, not selected |
| half-memory H0 with `rdrag` | `30.909692098462312` | `0.8804374351611628` | candidate, not selected |
| DR2 locked fit readback | `30.029254663301153` | `~0` | readback |
| DR1 locked fit readback | `29.937985423791297` | `-0.09126923950985244` | readback |

None of the current parent candidates is allowed to become the BAO alpha owner
yet, because the parent theory has not derived:

```text
which H0 branch BAO should use,
which r_d calibration BAO should use,
and why that product is fixed.
```

## 6. Policy Decision

| policy | verdict |
|---|---|
| shared empirical nuisance | allowed for fair scorecards |
| MTS-only alpha rescue | rejected |
| parent alpha prediction | theorem target, missing |
| strict no-alpha shape | future stress test |

Allowed statement:

```text
The locked 2/27 branch survives BAO-only stress tests with the same alpha
nuisance treatment as the baselines.
```

Forbidden statement:

```text
MTS predicts the BAO absolute scale.
```

## 7. Parent Contract

To promote alpha from nuisance to theory, the parent framework must derive:

| contract | needed |
|---|---|
| H0 branch owner | decide whether BAO uses late H0, CMB-profile H0, half-memory H0, or another derived branch |
| `r_d` owner | derive sound horizon/ruler calibration in the same matter-unit frame used by BAO |
| alpha nuisance policy | predeclare shared nuisance vs fixed prediction before scoring |
| no double-counting | do not use alpha to absorb a scale already claimed as predicted |

Until then:

```text
alpha is empirical discipline, not physics promotion.
```

## 8. Claim Gates

| gate | result |
|---|---|
| all cited sources exist | pass |
| alpha shared across BAO-only models | pass |
| MTS-only alpha rescue | rejected |
| parent alpha predicted | fail |
| BAO empirical score remains usable | pass |
| BAO support claim allowed | fail |

## 9. Decision

Decision:

```text
BAO_alpha_shared_nuisance_fair_parent_owner_missing
```

Meaning:

```text
BAO alpha is currently a fair shared empirical nuisance, not an MTS prediction.
Parent promotion requires deriving H0 branch ownership, r_d calibration, and
alpha = c/(H0 r_d) before alpha is fixed or claimed.
```

Current theory status:

```text
BAO empirical cards remain usable;
BAO alpha cannot be used as proof;
strict fixed-alpha/no-alpha stress should be the next empirical discipline gate.
```

Next target:

```text
200-BAO-strict-alpha-shape-stress-or-parent-H0-rd-contract.md
```
