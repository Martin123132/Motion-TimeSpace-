# Official CMB Perturbation Contract

## 1. Purpose

This file follows:

```text
42-calibrated-closure-candidate-ledger.md
```

The question is:

```text
What must be true before the frozen calibrated C0 closure candidate can be
tested against official CMB spectra/lensing without cheating?
```

Short answer:

```text
the official CMB route is not ready for a support-capable run. It is blocked by
missing perturbation, conservation, initial-condition, and lensing closures.
```

Important distinction:

```text
official CMB likelihood tooling can be used as a kill-screen before the parent
perturbation theory is complete, but not as support.
```

That sounds annoying, but it is actually useful: it stops us mistaking borrowed
GR perturbations on an MTS background for a parent-derived MTS prediction.

## 2. Machine Run

Implemented:

```text
scripts/official_CMB_perturbation_contract.py
```

Successful run:

```text
runs/20260531-012227-official-CMB-perturbation-contract/status.json
```

Readout:

```text
official_CMB_contract_written_perturbation_closure_missing_no_support_run_yet
```

Generated:

```text
runs/20260531-012227-official-CMB-perturbation-contract/results/source_checkpoint_register.csv
runs/20260531-012227-official-CMB-perturbation-contract/results/frozen_background_manifest.csv
runs/20260531-012227-official-CMB-perturbation-contract/results/perturbation_variable_contract.csv
runs/20260531-012227-official-CMB-perturbation-contract/results/standard_parameter_policy.csv
runs/20260531-012227-official-CMB-perturbation-contract/results/CMB_observable_contract.csv
runs/20260531-012227-official-CMB-perturbation-contract/results/no_new_knob_policy.csv
runs/20260531-012227-official-CMB-perturbation-contract/results/official_CMB_run_mode_register.csv
runs/20260531-012227-official-CMB-perturbation-contract/results/official_CMB_pass_fail_gates.csv
runs/20260531-012227-official-CMB-perturbation-contract/results/official_CMB_setup_manifest.csv
runs/20260531-012227-official-CMB-perturbation-contract/results/decision.csv
```

## 3. Frozen Background Row

The official CMB stress must keep the checkpoint-38 frozen row:

```text
h0 = 67.71676410614398
Omega_m0 = 0.31988262346779694
b_mem = 0.027085159773612907
alpha_act = 1.0543379145228584
nu_act = 1.7500073382761008
rd = 147.29909165793796
```

These cannot move inside the official CMB test.

If they move, the result is not a fixed-row stress test. It becomes parameter
rescue.

## 4. Mandatory Perturbation Contract

The generated contract has eight perturbation blocks:

```text
metric variables: Phi/Psi or h/eta;
standard species: delta_i, theta_i, sigma_i for photons, baryons, CDM, neutrinos;
memory background: F(N), b_mem, alpha_act, nu_act;
memory perturbations: delta F, delta b_mem, delta Gamma_eff, delta q_mem;
constraint equations: Poisson, slip, momentum, anisotropic stress;
conservation: Bianchi-compatible source or no-source law;
initial conditions: superhorizon adiabatic/isocurvature modes;
lensing: W_lens, Phi + Psi, growth response.
```

Current count:

```text
perturbation rows = 8
mandatory missing rows = 7
```

This is the core result of this checkpoint.

Without these rows, an official spectra/lensing run can still be informative
as a failure screen, but cannot support the theory.

## 5. Standard Parameter Policy

Official spectra need more than the late-background closure row:

```text
A_s, n_s, tau_reio;
omega_b h^2;
T_CMB;
N_eff;
Y_p;
sum_mnu;
foreground and instrument nuisance parameters.
```

Policy:

```text
lock them to a chosen baseline/reference or marginalize identically across all
branches.
```

Forbidden:

```text
tuning these only for MTS;
using A_L as a lensing rescue;
adding arbitrary mu(k,a) or Sigma(k,a);
moving h0/Omega_m0/b_mem/alpha/nu after seeing spectra.
```

## 6. Observable Contract

A support-capable official CMB route must cover:

```text
C_l^TT;
C_l^TE;
C_l^EE;
CMB lensing phi-phi or convergence likelihood;
theta_star, r_s, D_M(z_star);
late ISW and low-ell response.
```

The compressed distance prior only probes the last background-distance corner.
It does not replace the spectra/lensing contract.

## 7. Allowed Run Modes

Allowed but not support:

```text
compressed_CMB_distance;
official_background_only_GR_perturbation_stress;
official_lensing_fixed_parameter_stress if labelled as background-only kill-screen.
```

Not ready:

```text
official_parent_perturbation_CMB_stress.
```

Reason:

```text
the parent perturbation closure is missing.
```

This is the honest boundary.

## 8. Predeclared Gates

Locked gates:

```text
source_42_complete: pass;
perturbation_contract_complete: fail now;
baseline_reproduction: not run;
fixed_row_no_rescue: contract locked;
official_CMB_delta_chi2_band: predeclared, not run;
evidence_language: forbidden now.
```

Predeclared CMB score bands:

```text
Delta chi2 <= 10:
    retain for further tests only, not support by itself;

10 < Delta chi2 <= 25:
    serious CMB tension;

Delta chi2 > 25:
    demote the CMB-calibrated branch.
```

These thresholds are intentionally blunt. The point is to prevent after-the-fact
storytelling once a real likelihood number exists.

## 9. Practical Setup Contract

Before any long official run:

```text
write baseline and MTS configs side by side;
record exact data paths, versions, hashes, and likelihood choices;
prove baseline reproduction before evaluating MTS;
write runs/<timestamp>/log.txt, status.json, configs, copied manifests, and DONE.txt;
do not sit watching an hour-long run inside Codex.
```

Official route references remain:

```text
Planck 2018 likelihood code;
Cobaya likelihood framework;
ACT DR6 lensing likelihood;
ACT DR6 data products.
```

They are setup targets, not completed evidence.

## 10. Decision

Decision:

```text
official_CMB_contract_written_run_not_ready
```

Meaning:

```text
the frozen calibrated row has earned a serious CMB contract;
the parent perturbation theory has not yet earned a serious CMB support run;
background-only official CMB can kill the branch but cannot crown it.
```

This is the cleanest line so far:

```text
to make CMB useful, derive the perturbations first.
```

## 11. Next Target

Create:

```text
44-minimal-CMB-perturbation-closure-attempt.md
```

Purpose:

```text
attempt the minimal scalar/lensing perturbation closure for the frozen C0
background: metric potentials, memory perturbation response, conservation law,
initial conditions, and lensing projection. If that cannot be derived, official
CMB remains a kill-screen only.
```

This is not narrowing the theory into CMB-only work. It is forcing the
cosmology pillar to speak field-theory language.
