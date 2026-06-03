# Cosmology Bridge Run Manifest

## 1. Purpose

This file follows:

```text
21-cosmology-parent-bridge-audit.md
```

The question is:

```text
What exact manifest must be locked before any long cosmology robustness run?
```

Short answer:

```text
the manifest is locked for safe preflight only. Long runs remain blocked until
models, labels, splits, and outputs are obeyed explicitly.
```

## 2. Machine Run

Implemented:

```text
scripts/cosmology_bridge_run_manifest.py
```

Successful run:

```text
runs/20260530-234358-cosmology-bridge-run-manifest/status.json
```

Readout:

```text
cosmology_bridge_run_manifest_locked_preflight_only
```

Next target:

```text
23-strict-cosmology-branch-contract.md
```

## 3. Models

Allowed model classes:

```text
LCDM:
baseline only.

wCDM:
baseline only.

CPL:
baseline only.

C0_minimal_smooth_memory:
MTS closure benchmark only.

C0_frozen_background_holdout:
primary holdout candidate; no growth/CMB refit.

M6_or_shape_free_activation:
dry-run only unless shape/amplitude are predeclared and edge-safe.

strict_future_MTS_branch:
not existing yet; must be defined before use.
```

## 4. Data Splits

Locked splits:

```text
background_training:
SN/BAO background comparison.

no_SH0ES_background:
Pantheon+ shape with nuisance offset, BAO unchanged.

growth_CMB_holdout:
primary C0 holdout; no growth/CMB refit.

Hz_direct_stress:
diagnostic only until covariance handling is locked.

full_joint_robustness:
secondary refit only; cannot overwrite the primary holdout verdict.
```

## 5. Parameter Labels

Required labels:

```text
b_mem:
meaning derived, magnitude phenomenological.

F(N):
closure shape.

alpha_act, nu_act, A_act:
phenomenological/fitted unless parent-derived.

c_s,Gamma^2:
fixed closure = 1.

pi_Gamma:
fixed closure = 0.

Q_m^nu:
fixed closure = 0.

H0, Omega_m, rd, sigma8:
fitted nuisance or dataset calibration.
```

No result may relabel these as derived without a new parent-action derivation.

## 6. Commands

Allowed now:

```text
bridge_manifest_only
data_source_audit
parser_smoke
likelihood_preflight
```

Blocked long/score runs:

```text
first_scoring_run
full_joint_radflat
cosmology_likelihood_smoke
```

Those require explicit next approval and must obey this manifest.

## 7. Output Contract

Any later scoring run must write:

```text
status.json
model_scores.csv
parameter_labels.csv
residuals_by_dataset.csv
robustness_diagnostics.csv
claim_ladder_verdict.csv
```

The outputs must include:

```text
prior_edge_flags;
baseline_same_test_done;
delta_AIC_vs_best_baseline;
delta_BIC_vs_best_baseline;
dominant point/dataset diagnostics;
maximum allowed claim level.
```

## 8. Gate Verdict

Passes:

```text
source 21 complete;
models and labels locked;
data splits locked;
output contract locked.
```

Fails:

```text
long run allowed now;
empirical claim allowed;
main workbench mutation allowed.
```

Status:

```text
safe for preflight only;
not safe for long scoring runs yet.
```

## 9. Next Target

Create:

```text
23-strict-cosmology-branch-contract.md
```

Purpose:

```text
define a stricter MTS cosmology branch with fewer amplitude/shape freedoms, or
explicitly choose a preflight-only path before any costly robustness run.
```
