# 198 - BAO Radial Drift and Alpha Owner Gate

Private theory checkpoint. This is not a public BAO claim.

## 1. Trigger

Checkpoint 197 wrote the conditional BAO ratio theorem:

```text
tilde_D_X / tilde_r_d = D_X / r_d
```

provided that:

```text
D_X and r_d share the same late conformal matter unit.
```

The remaining weak point was radial BAO:

```text
tilde_D_H = exp(C_obs/2) D_H / (1 + dot_C/(2H)).
```

So this checkpoint asks:

```text
How much dot_C/H can DESI DR2 tolerate, and is the tiny H0-bridge residual safe?
```

It also classifies `alpha`:

```text
shared nuisance, MTS-only rescue, or parent-owned calibration.
```

## 2. Machine Artifact

Script:

```text
scripts/BAO_radial_drift_and_alpha_owner_gate.py
```

Run:

```text
runs/20260601-000015-BAO-radial-drift-and-alpha-owner-gate
```

Command:

```text
python scripts/BAO_radial_drift_and_alpha_owner_gate.py --timestamp 20260601-000015
```

Status:

```text
BAO_radial_drift_bound_safe_for_H0_residual_alpha_owner_still_closure
```

Claim ceiling:

```text
BAO_radial_drift_bound_internal_only_alpha_not_parent_owned_no_support_claim
```

## 3. Radial Drift Model

Define:

```text
epsilon = dot_C / (2H).
```

Then the BAO ratio factors are:

| observable | factor |
|---|---|
| `D_M/r_d` | `1` |
| `D_H/r_d` | `1/(1+epsilon)` |
| `D_V/r_d` | `(1/(1+epsilon))^(1/3)` |

This is the anisotropic drift mode that can spoil the common-mode theorem.

## 4. DESI DR2 Drift Tolerance

Using the DESI DR2 primary BAO covariance:

| alpha mode | `Delta chi2` | max `|dot_C/H|` |
|---|---:|---:|
| fixed `alpha=1` | `1` | `0.011285628250379043` |
| fixed `alpha=1` | `4` | `0.022697688743796407` |
| fixed `alpha=1` | `9` | `0.03423829798375011` |
| fixed `alpha=1` | `25` | `0.057713865824317034` |
| best shared `alpha` | `1` | `0.018079450186889945` |
| best shared `alpha` | `4` | `0.03636283824103148` |
| best shared `alpha` | `9` | `0.05485394049212666` |
| best shared `alpha` | `25` | `0.09247485669130451` |

So DESI DR2 is less brutal against radial-only drift than against global BAO
ratio leakage, but it still rejects a full unscreened memory-scale drift.

## 5. Representative Cases

| case | `dot_C/H` | fixed-alpha chi2 | best shared alpha | best-alpha residual chi2 |
|---|---:|---:|---:|---:|
| zero drift | `0.0` | `0.0` | `1.0` | `0.0` |
| H0-bridge residual drift | `-0.0004084189185673548` | `0.0013248316775037391` | `0.9999212407694936` | `0.0005161835652659898` |
| same magnitude opposite sign | `0.0004084189185673548` | `0.0013237636837480859` | `1.0000787323271187` | `0.0005158396722879871` |
| one-percent drift | `0.01` | `0.7861344592216811` | `1.0019200270818829` | `0.30617591914896544` |
| full memory-scale drift | `0.07407407407407407` | `40.543585695707606` | `1.0138504368582386` | `16.220798155176727` |

This is the useful readout:

```text
the tiny dot_C/H residual needed by the H0 bridge is BAO-safe.
```

But:

```text
an unscreened live C field drifting at memory scale is not BAO-safe.
```

Therefore the parent theory still needs a saturation/silence mechanism.

## 6. Alpha Policy

| alpha route | empirical fairness | parent-owner status | verdict |
|---|---|---|---|
| shared observational nuisance | fair if identical for all baselines | not parent-owned | closure-only |
| MTS-only alpha rescue | unfair | not parent-owned | rejected |
| parent observer-map alpha | fair if predeclared | candidate, not derived | theorem target |
| no-alpha strict shape | fair | strongest if survived | strict diagnostic |

This matters because previous BAO empirical scores can be fair without being a
field-theory prediction.

Allowed:

```text
shared alpha is an empirical nuisance used symmetrically.
```

Forbidden:

```text
alpha proves MTS predicted BAO.
```

## 7. Theory Contract

To promote the BAO route, the parent framework must provide:

| contract | current status |
|---|---|
| saturated BAO readout with small `dot_C/H` | safe for H0 residual, not parent-derived |
| reject full unscreened memory-scale drift | numerically required |
| shared alpha policy | fair empirically, closure-only |
| radial/transverse no-leakage | bounded, not derived |

The key survival condition is now:

```text
BAO readout must occur in a saturated/silent clock-map regime.
```

That is consistent with the endpoint route, but not yet derived from the parent
action.

## 8. Claim Gates

| gate | result |
|---|---|
| all cited sources exist | pass |
| H0-residual radial drift BAO-safe | pass |
| full memory-scale radial drift rejected | pass |
| radial drift parent-derived | fail |
| alpha parent-owned | fail |
| BAO support claim allowed | fail |

## 9. Decision

Decision:

```text
BAO_radial_drift_bound_safe_for_H0_residual_alpha_owner_still_closure
```

Meaning:

```text
The H0-bridge residual dot_C/H is tiny enough to be safe for DESI DR2 BAO.
But the theory must still derive why BAO readout is saturated/silent, and alpha
remains closure-level unless parent-owned.
```

Current theory status:

```text
BAO no longer looks like an immediate killer for the endpoint-clock route;
full unscreened radial drift is rejected;
shared alpha remains empirical discipline, not theory promotion.
```

Next target:

```text
199-BAO-alpha-parent-or-shared-nuisance-policy.md
```
