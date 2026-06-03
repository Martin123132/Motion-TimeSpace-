# 216 - Load Morphology Sidecar Galaxy Test Plan

Private test-planning checkpoint. This is not a public local-GR, galaxy, SPARC,
ETG, BAO, CMB, or field-theory completion claim.

## 1. Trigger

Checkpoint 215 found the honest owner split:

```text
matter support -> s_80, r_99, A_I
Q -> anisotropy/routing sidecar
J_rel -> missing edge-current owner
```

The parent theorem is still missing.

But the closure is sharp enough to precommit a future sidecar test plan before
touching any galaxy pipeline.

## 2. Machine Artifact

Script:

```text
scripts/load_morphology_sidecar_galaxy_test_plan.py
```

Run:

```text
runs/20260601-000033-load-morphology-sidecar-galaxy-test-plan
```

Command:

```text
python scripts/load_morphology_sidecar_galaxy_test_plan.py --timestamp 20260601-000033
```

Status:

```text
load_morphology_sidecar_plan_locked_no_fit_no_galaxy_repo_touch
```

Claim ceiling:

```text
sidecar_plan_only_no_galaxy_local_or_field_theory_promotion
```

## 3. Frozen Sidecar Rule

The sidecar rule is locked as:

```text
E_L = s_80 (1 + A_I)/2 + F_edge.
```

Classification:

| class | frozen rule |
|---|---|
| `compact_vacuum_shell` | `vacuum_collar_fraction > 0.5` and `E_L < 0.25` |
| `extended_load` | `E_L > 0.40` or `F_edge > 0.05` |
| `ambiguous` | neither compact nor extended |

These are not fit parameters.

They must not be changed after seeing residuals.

## 4. Required Input Schema

Future sidecar rows require:

| column | meaning |
|---|---|
| `object_id` | join key |
| `domain_radius_kpc` | predeclared domain/shell radius |
| `s80_r80_over_RD` | 80% support radius divided by domain radius |
| `s99_r99_over_RD` | 99% support radius divided by domain radius |
| `A_I` | support inertia/load anisotropy |
| `F_edge` | outer-collar load/current proxy |
| `quality_flag` | complete, extrapolated, missing profile, or ambiguous domain |

Forbidden input:

```text
rotation residuals,
fit residuals,
post-hoc galaxy success labels.
```

## 5. No-Fit Policy

The sidecar must obey:

| rule | reason |
|---|---|
| compute sidecar before reading residuals | prevents post-hoc selection |
| thresholds frozen from checkpoint 214 | prevents hidden tuning |
| ambiguous means ambiguous | prevents cherry-picking |
| galaxy repo read-only | keeps this thread separate from galaxy work |
| split baselines fairly | avoids guilty-until-proven-innocent asymmetry |

This matters because the sidecar is only scientifically useful if it is
precommitted.

## 6. Future Galaxy Test Plan

Future phases:

| phase | action |
|---|---|
| `G0` | schema dry-run on a tiny manifest |
| `G1` | read-only join to existing galaxy result tables |
| `G2` | stratified residual audit by compact/extended/ambiguous class |
| `G3` | fair baseline split/jackknife where baselines can meaningfully run |

No result from this plan should be called galaxy evidence until:

```text
the sidecar is computed independently of residuals,
the galaxy outputs are unchanged,
and baselines receive comparable splits.
```

## 7. Future Local Test Plan

Future local phases:

| phase | action |
|---|---|
| `L0` | compact shell manifest for Sun/Earth cases |
| `L1` | combine compact class with fixed `G_K` to estimate `q_loc` residual vector |
| `L2` | compare with GR/control local observables |

No local-GR promotion is allowed from the sidecar alone.

It only prepares the branch for a fair `q_loc`/PPN test.

## 8. Gate Results

| gate | result |
|---|---|
| all cited sources exist | pass |
| sidecar formula frozen | pass |
| no galaxy repo mutation | pass |
| input schema specified | pass |
| actual SPARC/ETG data run | not run |
| local `q_loc`/PPN residual run | not run |
| sidecar promoted as parent theory | fail |

## 9. Decision

Decision:

```text
load_morphology_sidecar_plan_locked_no_fit_no_galaxy_repo_touch
```

Meaning:

```text
the load-morphology invariant is now ready as a disciplined future sidecar
contract, not as evidence.
```

The sidecar is useful because it prevents a dirty move:

```text
choosing local/galaxy domains after seeing what scores well.
```

## 10. Next Target

Next target:

```text
217-load-morphology-sidecar-builder-dryrun.md
```

The exact next question:

```text
Can we build a tiny schema validator/sidecar builder dry-run inside
post-checkpoint-work, without touching galaxy-work or fitting anything?
```
