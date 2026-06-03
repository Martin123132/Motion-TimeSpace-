# Strict Cosmology Branch Contract

## 1. Purpose

This file follows:

```text
22-cosmology-bridge-run-manifest.md
```

The question is:

```text
Can we define a stricter MTS cosmology branch before scoring, so any future
data hit is not just a shape-free or amplitude-rescue fit?
```

Short answer:

```text
yes as a contract, not yet as a derived cosmology. The strict branch is now a
disciplined test object, but scoring and empirical claims remain blocked.
```

## 2. Machine Run

Implemented:

```text
scripts/strict_cosmology_branch_contract.py
```

Successful run:

```text
runs/20260530-235043-strict-cosmology-branch-contract/status.json
```

Readout:

```text
strict_cosmology_branch_contract_locked_no_scoring_yet
```

Next target:

```text
24-cosmology-preflight-execution-plan.md
```

## 3. Strict Branch Rule

The admissible strict memory candidate is:

```text
Omega_Gamma(N) = b_mem_pre F_pre(N)
S_Gamma(N) = b_mem_pre dF_pre/dN
```

with:

```text
b_mem_pre locked before scoring;
F_pre(N) locked before scoring;
c_s,Gamma^2 = 1;
pi_Gamma = 0;
Q_m^nu = 0.
```

This is still closure-level unless the parent action derives the amplitude,
shape, and perturbation sector.

## 4. Branch Status

Locked branches:

```text
strict_C0_frozen_holdout:
primary strict control; background frozen before growth/CMB holdout.

strict_memory_predeclared:
candidate strict MTS branch; b_mem_pre and F_pre must be chosen before scoring.

strict_activation_predeclared:
secondary candidate only; alpha_act, nu_act, A_act require predeclared rules.

shape_free_M6:
diagnostic only; not positive support.

phenomenology_full_joint:
secondary diagnostic only; cannot override the frozen holdout.
```

## 5. Parameter Contract

Hard rules:

```text
b_mem_pre:
predeclared or absent; never an after-the-fact rescue amplitude.

F_pre(N):
predeclared or absent; never a shape sweep after residuals are known.

alpha_act, nu_act, A_act:
fixed-rule/predeclared branches only; edge hits block support.

H0, Omega_m, rd, sigma8:
baseline-symmetric nuisance parameters only.
```

No nuisance shift counts as a theory derivation.

## 6. Data Split Contract

Primary order:

```text
background_training:
can lock background values; not support by itself.

no_SH0ES_background:
tests whether local-H0 calibration pressure is doing the work.

growth_CMB_holdout:
primary frozen-direction test; no refit rescue.

Hz_direct_stress:
diagnostic only until source/covariance handling is locked.

full_joint_robustness:
secondary same-test refit only.
```

## 7. Gate Verdict

Passes:

```text
source 22 complete;
strict branch contract defined;
shape-free support blocked;
same-baseline requirement locked;
preflight allowed now.
```

Fails:

```text
parent-derived amplitude available;
parent-derived shape available;
parent-derived perturbation sector available;
scoring run allowed now;
empirical claim allowed now.
```

Status:

```text
safe for preflight planning;
not safe for scoring or claims yet.
```

## 8. Claim Ladder

Current maximum:

```text
L0_control
```

Future upgrades require:

```text
L2_fit:
same-test scoring against LCDM/wCDM/CPL.

L3_robust:
holdout survival plus AIC/BIC against the best baseline without edge dependence.

L4_derived:
parent action derives amplitude, shape, and perturbation sector.
```

## 9. Next Target

Create:

```text
24-cosmology-preflight-execution-plan.md
```

Purpose:

```text
turn this strict contract into dry-run command generation and data-shape checks,
without starting a long scoring run or making a cosmology claim.
```
