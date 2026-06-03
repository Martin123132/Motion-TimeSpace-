# Cosmology Parent-Bridge Audit

## 1. Purpose

This file follows:

```text
20-empirical-pillar-test-queue.md
```

The question is:

```text
Can the cosmology variables be mapped onto the parent-action skeleton before
any long robustness run?
```

Short answer:

```text
yes, they can be mapped; no, the cosmology branch is not parent-derived yet.
No long cosmology run is authorized from this file.
```

## 2. Machine Run

Implemented:

```text
scripts/cosmology_parent_bridge_audit.py
```

Successful run:

```text
runs/20260530-234037-cosmology-parent-bridge-audit/status.json
```

Readout:

```text
cosmology_parent_bridge_mapped_not_derived_no_long_run
```

Next target:

```text
22-cosmology-bridge-run-manifest.md
```

## 3. Source Files Checked

The audit uses current main-workbench evidence:

```text
176-C0-radflat-demotion-decision.md
178-parent-amplitude-theorem-attempt.md
157-minimal-smooth-memory-growth-CMB-test-contract.md
174-bmem-parent-boundary-law.md
04-variable-audit.csv
07-unification-spine.md
```

All are read-only sources for this bridge. No main-workbench file was edited.

## 4. Variable Bridge

Key mapping:

```text
C(t):
maps to C(x) / S_load.
Status: target, not derived.

M_cosmo_or_memory:
maps to S_cosmo_memory.
Status: placeholder, not action-derived.

Omega_Gamma(z):
maps to memory trace projection.
Status: closure variable.

b_mem:
maps to integrated memory-source budget.
Status: meaning/source identity derived; magnitude phenomenological.

F(N):
maps to memory transition shape.
Status: shape closure.

S_Gamma(N):
maps to memory source.
Status: identity derived given F(N).

alpha_act, nu_act, A_act:
map to transition scale/shape/amplitude.
Status: fitted/phenomenological unless parent-derived.

c_s,Gamma^2, pi_Gamma, Q_m^nu:
map to perturbation sector.
Status: fixed closure in C0 growth/CMB contract.
```

## 5. Branch Status

The current cosmology branches are:

```text
C0_minimal_smooth_memory:
closure benchmark only.

M6_or_activation_shape:
fragile phenomenology until shape/amplitude are parent-derived and edge rules
are locked.

growth_CMB_holdout:
contract locked, but not yet a fit authorization.

full_joint_radflat:
near-competitive diagnostic, but closure-only because b_mem shifts strongly.

strict_future_branch:
needed if we want fewer amplitude freedoms or a parent-predeclared shape.
```

## 6. Robustness Rules

Before any long cosmology run:

```text
1. every parameter must be labeled:
derived / postulated / closure / phenomenological / fitted nuisance.

2. LCDM, wCDM, CPL, C0, and any strict branch must get same-test treatment.

3. prior-edge branches cannot count as evidence.

4. growth/CMB holdout split must be respected.

5. closure success cannot be called parent derivation.

6. no long run before a bridge run manifest is locked.
```

## 7. Gate Verdict

Passes:

```text
source 20 complete;
main cosmology status files exist;
variables mapped to parent hooks.
```

Fails:

```text
parent-derived cosmology available;
long run allowed now;
empirical claim allowed.
```

Status:

```text
cosmology bridge mapped;
not derived;
no long run yet.
```

## 8. Critical Open Items

Open:

```text
derive_b_mem_magnitude;
derive_F_N_or_activation_shape;
derive_FLRW_memory_equations;
derive_perturbation_sector;
lock_same-test_robustness_manifest.
```

## 9. Next Target

Create:

```text
22-cosmology-bridge-run-manifest.md
```

Purpose:

```text
turn this bridge audit into an exact dry-run/run manifest: models, parameters,
labels, priors, edge flags, baselines, data splits, outputs, and claim limits
before any long cosmology robustness job.
```
