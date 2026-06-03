# Local Observables Data Map

## 1. Purpose

This file follows:

```text
14-closure-deviation-PPN-sensitivity.md
```

The question is:

```text
Which real local-gravity observables should be used to screen q_R, delta_beta,
alpha_clock, epsilon_matter, and Q_R before making any empirical claim?
```

Short answer:

```text
the local branch is now screening-ready against published bounds, but it is not
a raw-data fit and it is not empirical evidence for MTS.
```

## 2. Machine Run

Implemented:

```text
scripts/local_observables_data_map.py
```

Successful run:

```text
runs/20260530-232024-local-observables-data-map/status.json
```

Readout:

```text
local_observables_data_map_screening_ready_not_fit
```

Next target:

```text
16-local-bounds-gate-runner.md
```

## 3. Adopted Screening Gates

This stage uses published bounds only:

```text
q_R:
2.3e-5 from the Cassini gamma uncertainty.

delta_beta:
7.16e-5 from INPOP20a conservative beta-1 interval.

alpha_clock:
2.48e-5 from the Galileo eccentric-satellite redshift test.

epsilon_matter:
2.745906043549196e-15 from MICROSCOPE stat/systematic quadrature proxy.

Q_R:
0 by closure definition.
```

These are screening gates, not fitted MTS posteriors.

## 4. Source Map

The current source map is:

```text
Cassini radio science:
gamma = 1 + (2.1 +/- 2.3)e-5.
Mapped to q_R.

INPOP20a planetary ephemerides:
conservative intervals beta-1 about 7.16e-5 and gamma-1 about 7.49e-5.
Mapped to delta_beta and cross-check q_R.

Galileo eccentric satellites:
redshift fractional deviation (+0.19 +/- 2.48)e-5.
Mapped to alpha_clock.

MICROSCOPE final WEP result:
eta(Ti,Pt) = [-1.5 +/- 2.3(stat) +/- 1.5(syst)]e-15.
Mapped to epsilon_matter.
```

The script stores URLs in:

```text
runs/20260530-232024-local-observables-data-map/results/published_bound_sources.csv
```

## 5. Observable Translation

The stage also translates gates through the stage-14 linear coefficients.

Examples:

```text
q_R gate -> solar light-bending screening shift:
0.8756216406841224 * 2.3e-5 arcsec.

q_R gate -> Mercury gamma-side screening shift:
28.65467507274745 * 2.3e-5 arcsec/century.

delta_beta gate -> Mercury beta-side screening shift:
-14.327337536373726 * 7.16e-5 arcsec/century.

alpha_clock gate -> GPS-like redshift screening shift:
45.718449825926655 * 2.48e-5 microseconds/day.
```

These translations tell us the scale at which the closure begins to leak into
local observables.

## 6. Priority Channels

Priority order:

```text
1. Cassini / radio-science Shapiro:
primary q_R gate.

2. Planetary ephemerides / perihelia:
delta_beta and q_R mixed gate.

3. Galileo redshift:
alpha_clock gate.

4. MICROSCOPE:
epsilon_matter / universal coupling gate.

5. VLBI/Gaia light deflection:
later independent q_R check after current data curation.
```

## 7. Gate Verdict

Passes:

```text
source 14 complete;
published bounds mapped;
parameter degeneracies flagged;
next test plan defined.
```

Fails:

```text
raw data likelihoods available;
empirical claim allowed.
```

Status:

```text
screening-ready;
not a data fit;
no empirical MTS signal claimed.
```

## 8. Next Target

Create:

```text
16-local-bounds-gate-runner.md
```

Purpose:

```text
turn the screening gates into a simple pass/fail runner for candidate local
branches, starting with closure, q_R leakage, beta drift, clock drift, and
matter-coupling drift.
```
