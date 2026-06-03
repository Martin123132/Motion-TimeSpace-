# Memory Scalar Reconstruction Gate

## 1. Purpose

This file follows:

```text
44-minimal-CMB-perturbation-closure-attempt.md
```

The question is:

```text
Can the effective memory background be reconstructed as an action-like scalar,
or is it only imported quintessence clothing?
```

Short answer:

```text
the scalar proxy is reconstructable on the past branch, but it is nonanalytic
at the present endpoint and is not parent-derived. So it remains a closure
benchmark, not a fundamental MTS scalar.
```

This is a useful result because it finds the exact mathematical snag rather
than just saying "perturbations missing".

## 2. Machine Run

Implemented:

```text
scripts/memory_scalar_reconstruction_gate.py
```

Successful run:

```text
runs/20260531-013422-memory-scalar-reconstruction-gate/status.json
```

Readout:

```text
memory_scalar_proxy_reconstructable_but_nonanalytic_and_not_parent_derived
```

Generated:

```text
runs/20260531-013422-memory-scalar-reconstruction-gate/results/source_checkpoint_register.csv
runs/20260531-013422-memory-scalar-reconstruction-gate/results/scalar_reconstruction_grid_sample.csv
runs/20260531-013422-memory-scalar-reconstruction-gate/results/scalar_potential_features.csv
runs/20260531-013422-memory-scalar-reconstruction-gate/results/endpoint_regularities.csv
runs/20260531-013422-memory-scalar-reconstruction-gate/results/parent_compatibility_tests.csv
runs/20260531-013422-memory-scalar-reconstruction-gate/results/scalar_reconstruction_gates.csv
runs/20260531-013422-memory-scalar-reconstruction-gate/results/repair_options.csv
runs/20260531-013422-memory-scalar-reconstruction-gate/results/decision.csv
```

## 3. What Reconstructs

The checkpoint-38 frozen background can be written as:

```text
rho_X/H0^2 = 1 - Omega_m0 + b_mem F(N)
```

If treated as a separately conserved effective dark sector:

```text
w_X(N) = -1 + [b_mem dF/dN] / [3(1 - Omega_m0 + b_mem F)]
```

Then a canonical scalar proxy can be reconstructed:

```text
K/(3 M_Pl^2 H0^2) = 0.5(1+w_X)rho_X/H0^2
V/(3 M_Pl^2 H0^2) = 0.5(1-w_X)rho_X/H0^2
```

This is mathematically useful, but it is still reverse-engineered from the
fitted background.

## 4. Numerical Features

Key values:

```text
nu_act = 1.7500073382761008
total scalar proxy excursion = 0.1067102512617318 M_Pl
V_today = 0.680117376532203
V_min = 0.6725002186470456
V_recombination = 0.707202536305816
V_recombination - V_today = 0.02708515977361292
```

The potential is single-valued because `phi` is monotone on the reconstructed
past branch, but the potential is not monotone:

```text
it dips near z = 0.08917898104010302, then climbs to the high-z plateau.
```

That is not automatically fatal. A non-monotone potential is allowed if a parent
action derives it. But here it is fitted backwards from `F(N)`.

## 5. Endpoint Regularity Problem

The serious snag is the fitted activation exponent.

The C0/M6 memory shape is:

```text
F(N) = 1 - exp[-(N/u_s)^nu]
```

For the frozen row:

```text
u_s = 0.26509965674554914
nu = 1.7500073382761008
```

Near today:

```text
F(N) ~ (N/u_s)^nu
dF/dN ~ N^(nu-1)
d2F/dN2 ~ N^(nu-2)
```

Since:

```text
nu - 2 = -0.24999266172389922
```

the second derivative diverges at `N -> 0+`.

For the canonical scalar reconstruction:

```text
phi - phi0 ~ N^((nu+1)/2)
V(phi) - V0 ~ -C phi^[2(nu-1)/(nu+1)]
```

The fitted row gives:

```text
2(nu-1)/(nu+1) = 0.5454584268464233
```

That means the canonical `V(phi)` has a cusp/infinite slope at the present
endpoint. A finite `dV/dphi` in this reconstruction requires roughly:

```text
nu >= 3
```

The current fitted value is below that.

## 6. Parent Compatibility

Failed parent-compatibility tests:

```text
phi_mem is reconstructed from H(a), not identified with psi, Gamma, C, or S_memory;
V(phi) is reverse-engineered from fitted F(N);
nu_act and alpha_act are frozen closure values;
b_mem is a frozen calibrated amplitude;
c_s^2 = 1 comes from imported canonical scalar closure;
the cosmological scalar proxy is not connected to local R_AB/q_loc suppression.
```

Conditional pass:

```text
w_X follows if the effective dark sector is separately conserved.
```

But that conservation law is not yet parent-derived.

## 7. Gate Result

Passed:

```text
canonical energy reconstruction, conditional;
single-valued V(phi) on the past branch;
official CMB kill-screen remains possible with clear labels.
```

Failed:

```text
activation C2 endpoint regularity;
smooth canonical parent action;
parent identity and variation;
support-capable CMB perturbations.
```

So the result is:

```text
reconstructed proxy, not parent action.
```

## 8. What This Means

Good news:

```text
the background is not impossible to cast in field-theory language.
```

Bad news:

```text
the current fitted activation law is not yet a clean fundamental scalar action.
```

This is exactly the sort of pressure a serious theory should feel. The empirical
shape is giving us something useful, but the field-theory regularity gate is
now biting.

## 9. Repair Routes

Possible routes:

```text
smooth_activation_replacement:
    replace the fractional Weibull onset by a C2/C1-action-safe load function;
    must be predeclared and retested.

noncanonical_k_essence_parent:
    use a kinetic structure that absorbs the cusp;
    risky because it adds functional freedom.

direct_Gamma_memory_action:
    make Gamma or S_memory the varied field and derive F(N) as a solution;
    preferred if derivable.

keep_quintessence_proxy_only:
    safe as a diagnostic closure benchmark;
    cannot become fundamental-theory evidence.
```

## 10. Decision

Decision:

```text
memory_scalar_proxy_reconstructable_but_nonanalytic_and_not_parent_derived
```

Meaning:

```text
the scalar bridge is useful;
the parent bridge is not solved;
the fitted activation exponent is now the mathematical bottleneck.
```

The cleanest statement:

```text
we can reconstruct the costume, but not yet the creature.
```

## 11. Next Target

Create:

```text
46-activation-regularity-repair-gate.md
```

Purpose:

```text
define what a parent-safe activation law must satisfy before any support-capable
CMB or scalar-action claim: real time-domain extension, C2 endpoint regularity,
finite dV/dphi, no new rescue knobs, and a same-test empirical retest plan.
```

This next step attacks the bottleneck directly instead of hiding it under more
likelihood machinery.
