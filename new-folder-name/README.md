# Curvature–Memory Theory (MTS Framework)

### A Unified Description of Galactic Dynamics and Cosmological Growth

**Author:** Martin Ollett
**Year:** 2026

---

## Overview

This repository contains a structured research programme developing a **curvature–memory field theory** in which gravitational response is governed not purely by instantaneous mass distribution, but by a dynamically evolving scalar field ( M ) coupled to matter.

The framework aims to provide a **single, continuous description** across:

* Galactic rotation curves
* Intermediate-scale transport behaviour
* Cosmological background evolution
* Linear perturbations and structure growth

The central objective is to test whether observed phenomena typically attributed to additional matter components can instead emerge from **field–matter coupling and cumulative response dynamics**.

---

## Core Idea

The theory introduces a scalar field ( M(x) ) governed by the action:

```
S = ∫ d^4x √(-g) [

        R/(16πG)
      - 1/2 (∇M)^2
      - a M^4 / 4
      + b T M^2
      + L_b

    ]
```

Where:

* ( M ): curvature–memory field
* ( a ): self-interaction strength
* ( b ): coupling to matter trace
* ( T ): trace of baryonic stress-energy

For pressureless matter:

```
T = -ρ_b
```

This induces an **effective potential**:

```
V_eff(M) = a M^4/4 + b ρ_b M^2
```

---

## Physical Structure of the Theory

The framework naturally separates into three regimes:

### 1. Cosmological Background

* Field evolves under FRW expansion:

  ```
  M̈ + 3H Ṁ + a M^3 + 2 b ρ_b M = 0
  ```

* For the physically relevant branch:

  ```
  b < 0
  ```

* The field sits in a **matter-supported minimum**:

  ```
  M_*^2 = 2 |b| ρ_b / a
  ```

* This produces a **slowly evolving background field**:

  ```
  M_* ∝ a^(-3/2)
  ```

---

### 2. Linear Cosmological Perturbations

Perturbations around the minimum:

```
M = M_* + χ
```

* Fluctuation mass:

```
m_*^2 = 4 |b| ρ_b
```

* Quasi-static response:

```
χ ≈ [ m_*^2 / (k^2/A^2 + m_*^2) ] δM_*
```

* Leads to a modified Poisson equation:

```
(k^2/A^2) Φ = 4πG [1 + β_*(k,a)] δρ_b
```

* Effective gravitational strength:

```
G_eff = G [1 + β_*(k,a)]
```

With leading-order form:

```
β_*(k,a)
  ≈ - (8 |b|^3 / a)
      ρ_b^2
      / (k^2/A^2 + 4 |b| ρ_b)
```

Key properties:

* β_* < 0 → suppressed growth
* Scale dependence (Yukawa-type)
* GR recovered on small scales

---

### 3. Galaxy Regime (Nonlinear Transport)

At galactic scales, the field departs from the cosmological minimum and enters a nonlinear transport regime:

```
M^3 ∝ g_b g_obs
```

This produces:

* Emergent rotation curve behaviour
* Linearisation in cumulative stiffness coordinate
* Direct connection to observed scaling relations

---

## Unified Chain

The theory forms a continuous pipeline:

```
Cosmological background M̄(a)
        ↓
Linear growth modification G_eff(k,a)
        ↓
Nonlinear galaxy response
        ↓
Observed rotation curves
```

---

## Repository Structure

Suggested organisation:

```
/papers
    01_galaxy_cumulative_stiffness.txt
    02_transport_theorem.txt
    03_effective_field_equation.txt
    04_covariant_invariant.txt
    05_frw_background.txt
    06_growth_equation.txt
    07_analytic_solutions.txt
    08_sign_of_b.txt
    09_minimum_branch_perturbations.txt
    10_cosmology_branch.txt

/code
    growth_solver.py
    background_evolution.py

/data
    sparc/
    growth_data/

/results
    plots/
    fits/
```

---

## Key Results

From the current derivations:

* A **matter-supported scalar field background** emerges naturally
* Linear perturbations produce a **scale-dependent modification of growth**
* The modification has the sign:

```
G_eff < G
```

→ Suppressed clustering

* The theory predicts:

```
γ > 0.55
```

with scale dependence

* Galaxy dynamics emerge from a **nonlinear transport relation**, not a fixed force law

---

## Scientific Status

This repository contains:

* Fully specified action
* Background evolution equations
* Linear perturbation system
* Closed-form approximation for growth modification
* Analytic solutions in key regimes

Not yet included:

* Full numerical integration of growth across datasets
* Joint cosmology + galaxy parameter constraints
* High-precision likelihood comparisons

---

## Next Steps

The immediate testable pipeline is:

1. Choose background expansion ( H(a) )
2. Solve growth equation:

```
δ'' + [2 + d ln H/dN] δ'
  = (3/2) Ω_b(a) [1 + β_*(k,a)] δ
```

3. Compute:

```
f(a,k) = δ'/δ
fσ8(z)
```

4. Compare against:

* DESI growth measurements
* Gold-2017 dataset
* Weak lensing constraints

---

## Interpretation Boundaries

This repository:

* Derives equations directly from the action
* Keeps comparisons at the level of **measurable quantities**
* Avoids introducing external phenomenological corrections

This does **not** claim:

* Final cosmological model completeness
* Resolution of all observational tensions
* Replacement of existing frameworks without empirical validation

---

## Purpose

The aim of this work is to establish a **testable, internally consistent framework** linking:

* matter distribution
* dynamical field response
* gravitational behaviour across scales

All conclusions should be evaluated through direct comparison with data.

---

## License

MIT License (recommended)

---

## Contact / Attribution

Martin Ollett
Independent Researcher

---
