# Closure-Deviation PPN Sensitivity

## 1. Purpose

This file follows:

```text
13-local-closure-PPN-benchmark.md
```

The question is:

```text
If the local closure leaks, which observable sees it first and how should the
leak be parameterized?
```

Short answer:

```text
q_R, beta drift, clock drift, and matter-coupling drift can now be treated as
an internal deviation budget. This is not yet tied to current literature bounds.
```

## 2. Machine Run

Implemented:

```text
scripts/closure_deviation_ppn_sensitivity.py
```

Successful run:

```text
runs/20260530-231601-closure-deviation-PPN-sensitivity/status.json
```

Readout:

```text
closure_deviation_ppn_sensitivity_internal_budget_complete
```

Next target:

```text
15-local-observables-data-map.md
```

## 3. Perturbation Dictionary

Use these closure-leak parameters:

```text
q_R:
reciprocal hair coefficient in R_AB approximately q_R L.
Maps to gamma - 1 approximately q_R.

delta_beta:
nonlinear completion drift beta - 1.

alpha_clock:
clock/load redshift anomaly.

epsilon_matter:
matter-sector coupling spread away from universal coframe coupling.

Q_R:
conserved reciprocal charge from a kinetic/current route.
Must vanish under the closure.
```

## 4. Linear Sensitivities

The internal linear coefficients are:

```text
solar light bending vs q_R:
0.8756216406841224 arcsec per unit q_R

solar Shapiro vs q_R:
59.7375179242781 microseconds per unit q_R

Mercury perihelion vs q_R:
28.65467507274745 arcsec/century per unit q_R

Mercury perihelion vs delta_beta:
-14.327337536373726 arcsec/century per unit delta_beta

GPS gravitational redshift vs alpha_clock:
45.718449825926655 microseconds/day per unit alpha_clock

Eotvos proxy vs epsilon_matter:
1 dimensionless proxy per unit coupling spread
```

These numbers are not observational constraints. They are the conversion
factors needed before comparing to real data.

## 5. Main Warning

The dangerous local leaks are:

```text
q_R:
immediately appears as a gamma-like residual.

epsilon_matter:
breaks universal matter coupling and therefore threatens equivalence-principle
consistency.
```

Beta drift is also important, but it mainly enters nonlinear orbital dynamics:

```text
Mercury shift factor = (2 q_R - delta_beta)/3.
```

So perihelion tests alone can contain degeneracy between `q_R` and `delta_beta`.

Light bending and Shapiro isolate the gamma-like side more directly.

## 6. Gate Verdict

Passes:

```text
source 13 complete;
q_R sensitivity quantified;
beta sensitivity quantified;
clock/matter sensitivity separated.
```

Fails:

```text
uses real literature bounds;
closure promoted to derivation.
```

Status:

```text
usable internal deviation budget;
not an empirical claim yet.
```

## 7. Practical Interpretation

The closure benchmark is now falsifiable in shape:

```text
R_AB=0 and universal coframe coupling define the null lane.
q_R, delta_beta, alpha_clock, and epsilon_matter define the leakage channels.
```

Any future local-data test should report:

```text
best-fit q_R;
best-fit delta_beta;
clock anomaly alpha_clock;
matter coupling spread epsilon_matter;
whether the result is a real MTS signal or just GR-equivalent closure.
```

## 8. Next Target

Create:

```text
15-local-observables-data-map.md
```

Purpose:

```text
map the internal deviation parameters to real observational sources and
published bounds before using the local branch as empirical evidence.
```
