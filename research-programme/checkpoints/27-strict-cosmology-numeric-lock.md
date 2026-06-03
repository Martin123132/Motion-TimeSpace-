# Strict Cosmology Numeric Lock

## 1. Purpose

This file follows:

```text
26-isolated-likelihood-preflight-wrapper.md
```

The question is:

```text
Before any growth/CMB score, what exact background and MTS numbers are frozen?
```

Short answer:

```text
the no-SH0ES background-fit values are locked as inputs for the first strict
growth/CMB holdout. No score was run.
```

## 2. Machine Run

Implemented:

```text
scripts/strict_cosmology_numeric_lock.py
```

Successful run:

```text
runs/20260531-000551-strict-cosmology-numeric-lock/status.json
```

Readout:

```text
strict_cosmology_numeric_lock_ready_for_scoring_manifest_no_score
```

## 3. Locked MTS Values

For:

```text
MTS_C0_minimal_smooth_memory
```

the locked first-holdout values are:

```text
h0 = 67.91792167906756
omega_m0 = 0.3009916276432578
rd = 147.29909165793796
b_mem = 0.0880607293391193
alpha_act = 1.0543379145228584
nu_act = 1.7500073382761008
c_s2_Gamma = 1
pi_Gamma = 0
Q_m_nu = 0
```

These are frozen inputs, not derivations.

## 4. Baseline Lock

The same source file locks the no-SH0ES background rows for:

```text
LCDM;
wCDM;
CPL;
MTS_C0_minimal_smooth_memory.
```

The first growth/CMB holdout must use these locked rows and the same growth/CMB
data/covariance treatment for every model.

## 5. Policy Lock

Hard rules:

```text
primary branch:
no-SH0ES background fit, then growth/CMB holdout.

b_mem sign:
positive from the locked no-SH0ES fit; no sign-free rescue in first score.

activation:
alpha_act and nu_act frozen; A_act excluded.

growth normalization:
one sigma8_0 normalization fitted symmetrically per model on primary growth rows.

claim limit:
L0 now; at most L2/L3 after same-test score and robustness.
```

## 6. Gate Verdict

Passes:

```text
source 26 complete;
background rows locked;
frozen shape source locked;
no score run here.
```

Fails/blocks:

```text
MTS growth/CMB refit allowed;
isolated scoring runner available;
empirical claim allowed now.
```

Status:

```text
numeric inputs are ready for a scoring manifest;
scoring itself remains blocked until the isolated runner is created.
```

## 7. Next Target

Create:

```text
28-isolated-growth-CMB-first-score-runner.md
```

Purpose:

```text
make a post-checkpoint first-score runner that consumes this numeric lock and
the isolated preflight wrapper, instead of using the legacy main-workbench
source-163 gate.
```
