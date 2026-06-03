# Minimal CMB Perturbation Closure Attempt

## 1. Purpose

This file follows:

```text
43-official-CMB-perturbation-contract.md
```

The question is:

```text
Can the frozen calibrated C0 background be given a minimal scalar/lensing
perturbation closure, or does official CMB remain a kill-screen only?
```

Short answer:

```text
a conditional effective-fluid/scalar closure exists mathematically, but it is
not parent-derived. Therefore official CMB can be used as a kill-screen, not as
support.
```

This is not a failure. It is a useful middle result: the branch is not obviously
unclosable, but the closure currently has to be borrowed.

## 2. Machine Run

Implemented:

```text
scripts/minimal_CMB_perturbation_closure_attempt.py
```

Successful run:

```text
runs/20260531-012747-minimal-CMB-perturbation-closure-attempt/status.json
```

Readout:

```text
conditional_effective_fluid_closure_found_parent_perturbation_derivation_still_missing
```

Generated:

```text
runs/20260531-012747-minimal-CMB-perturbation-closure-attempt/results/source_checkpoint_register.csv
runs/20260531-012747-minimal-CMB-perturbation-closure-attempt/results/effective_dark_sector_background.csv
runs/20260531-012747-minimal-CMB-perturbation-closure-attempt/results/scalar_reconstruction_summary.csv
runs/20260531-012747-minimal-CMB-perturbation-closure-attempt/results/perturbation_closure_candidates.csv
runs/20260531-012747-minimal-CMB-perturbation-closure-attempt/results/perturbation_equation_contract.csv
runs/20260531-012747-minimal-CMB-perturbation-closure-attempt/results/minimal_closure_consistency_gates.csv
runs/20260531-012747-minimal-CMB-perturbation-closure-attempt/results/official_CMB_implementation_manifest.csv
runs/20260531-012747-minimal-CMB-perturbation-closure-attempt/results/decision.csv
```

## 3. Effective Dark Sector Identity

For the frozen calibrated M6/C0 row:

```text
E^2(z) = Omega_m0(1+z)^3 + 1 - Omega_m0 + b_mem F(N)
N = ln(1+z)
```

Define the effective dark/memory sector:

```text
rho_X/H0^2 = 1 - Omega_m0 + b_mem F(N)
```

If that sector is separately conserved, its equation of state is fixed:

```text
w_X(N) = -1 + [b_mem dF/dN] / [3(1 - Omega_m0 + b_mem F)]
```

So the background does not need an arbitrary CMB perturbation equation of state.
It supplies one once conservation is assumed.

## 4. Numerical Readout

Key diagnostics:

```text
min(1 + w_X) = 0.0
max(w_X) = -0.9608350693324875
w_X at recombination = -1.0
Omega_X fraction at recombination = 1.2930917531205805e-09
proxy scalar field excursion from z=0 to z_star = 0.10671025121589944 M_Pl
```

Interpretation:

```text
the effective sector stays non-phantom;
it is dynamically tiny at recombination;
it has a small canonical-scalar proxy excursion;
its main CMB danger is late-time ISW/lensing, not primary plasma physics.
```

That is fairly good news. It means the branch is not immediately killed by
trying to write a minimal perturbation closure.

## 5. Candidate Closures

Three options were locked:

```text
homogeneous_smooth_memory:
    useful as a rough smooth-DE limit;
    not gauge-complete unless a parent constraint suppresses perturbations.

GR_effective_scalar_fluid:
    use w_X(a), c_s^2 = 1, sigma_X = 0, Phi = Psi under GR constraints;
    mathematically well-posed if treated as an imported effective closure;
    not parent-derived MTS.

parent_memory_field:
    derive delta Gamma_eff, delta q_mem, constraints, conservation, and lensing;
    required for support-capable official CMB;
    still missing.
```

Current best closure:

```text
GR_effective_scalar_fluid
```

Current honest label:

```text
borrowed effective-field closure; kill-screen only.
```

## 6. Scalar Proxy

Because the frozen row stays non-phantom, a canonical scalar proxy can be
written at the background level:

```text
K/(3 M_Pl^2 H0^2) = 0.5(1+w_X) rho_X/H0^2
V/(3 M_Pl^2 H0^2) = 0.5(1-w_X) rho_X/H0^2
```

This matters because it gives a narrow field-theory-shaped bridge:

```text
background memory -> effective scalar energy -> standard perturbation closure.
```

But the bridge is imported unless the scalar/action is derived from MTS parent
variables. So this is promising structure, not a solved derivation.

## 7. Consistency Gates

Passed conditionally:

```text
effective background conservation identity;
canonical scalar proxy exists;
early dark-sector fraction is small;
official CMB kill-screen is possible.
```

Failed:

```text
metric/lensing parent derivation;
support-capable official CMB readiness.
```

The failure is precise:

```text
Phi/Psi constraints and lensing response are still GR-imported unless the
parent action supplies them.
```

## 8. What This Allows

Allowed:

```text
run an official CMB background-plus-effective-fluid kill-screen with fixed
checkpoint-38 parameters, if the setup is labelled non-support.
```

Forbidden:

```text
claim official CMB support;
claim MTS derives CMB perturbations;
claim the scalar proxy is the parent field;
add A_L, mu(k,a), Sigma(k,a), or other rescue knobs.
```

## 9. Decision

Decision:

```text
conditional_effective_fluid_closure_found_not_parent_derivation
```

Meaning:

```text
the branch can be tested more seriously;
it still cannot be promoted;
the next derivation target is action/scalar reconstruction.
```

The useful way to say it:

```text
we found a clean borrowed bridge, not the parent bridge.
```

## 10. Next Target

Create:

```text
45-memory-scalar-reconstruction-gate.md
```

Purpose:

```text
try to reconstruct an action-like memory scalar from the effective rho_X and
w_X. If it can be tied to parent MTS variables, the CMB branch moves closer to
a real field-theory spine. If it is only imported quintessence, it remains a
closure benchmark.
```

This is the right next step because it attacks the exact gap instead of merely
adding more data pressure.
