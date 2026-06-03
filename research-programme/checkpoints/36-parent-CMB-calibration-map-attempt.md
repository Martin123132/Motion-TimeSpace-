# Parent CMB Calibration Map Attempt

## 1. Purpose

This file follows:

```text
35-early-time-decoupling-or-calibration-derivation.md
```

The question is:

```text
Can the parent theory derive the shared H0/Omega_m0/b_mem map needed to turn
the CMB-calibrated branch from closure into physics?
```

Short answer:

```text
not yet. H0 and Omega_m0 are still algebraic/Friedmann bookkeeping variables,
while b_mem has a plausible parent amplitude corridor but no predicted
magnitude. The CMB-calibrated branch therefore remains secondary closure.
```

## 2. Machine Run

Implemented:

```text
scripts/parent_CMB_calibration_map_attempt.py
```

Successful run:

```text
runs/20260531-004705-parent-CMB-calibration-map-attempt/status.json
```

Readout:

```text
parent_CMB_calibration_map_not_derived_bmem_corridor_only
```

## 3. Candidate Parent Map

Current possible maps:

```text
H0 = c / L_H
Omega_m0 = kappa_eff rho_m0 / (3 H0^2)
b_mem = a_F DeltaR / [3 (H0 L_cg / c)^2]
u_s = alpha_act ln[(1-Omega_m0)/Omega_m0] / 3
```

What derives:

```text
Omega_m0 bookkeeping identity;
b_mem corridor identity;
sign route for b_mem if a_F > 0 and DeltaR >= 0.
```

What does not derive:

```text
L_H;
rho_m0 definition with/without absorbed memory;
L_cg;
a_F;
DeltaR;
alpha_act;
nu_act.
```

So this is a map skeleton, not a parent prediction.

## 4. Calibration Shift

The native C0 CMB-calibrated frozen-shape row changes the locked no-SH0ES
branch as follows:

```text
h0:       67.91792167906756 -> 67.71676410614398    fractional shift = -0.0029617745648064264
Omega_m0: 0.3009916276432578 -> 0.31988262346779694 fractional shift =  0.06276252921868368
b_mem:    0.0880607293391193 -> 0.027085159773612907 fractional shift = -0.692426351940503
```

This is too large to treat as a harmless convention switch.

It means:

```text
the CMB-calibrated branch is a different closure row unless the parent theory
derives why b_mem, H0, and Omega_m0 should move together this way.
```

## 5. b_mem Corridor

Using:

```text
eta = H0 L_cg / c
a_F DeltaR = 3 b_mem eta^2
```

the locked no-SH0ES branch requires:

```text
eta = 0.1 -> a_F DeltaR = 0.0026418218801735798
eta = 1.0 -> a_F DeltaR = 0.26418218801735793
eta = 3.0 -> a_F DeltaR = 2.3776396921562215
```

The native CMB-calibrated row requires:

```text
eta = 0.1 -> a_F DeltaR = 0.0008125547932083873
eta = 1.0 -> a_F DeltaR = 0.08125547932083872
eta = 3.0 -> a_F DeltaR = 0.7312993138875485
```

Interpretation:

```text
both rows can sit inside an order-one parent amplitude corridor for eta near
unity, but that is plausibility only. It does not select either row.
```

## 6. Gate Result

Passed:

```text
source 35 complete;
high-z recombination memory safety already bounded;
CMB-calibrated row has no optimizer edge flags;
closure-only empirical stress is allowed.
```

Failed:

```text
H0 parent map;
Omega_m0 parent map;
b_mem magnitude derivation;
CMB support claim;
parent-predicted calibrated row.
```

## 7. Decision

Allowed language:

```text
the CMB-calibrated branch is a useful closure stress test, and its b_mem value
is not obviously absurd in the parent amplitude corridor.
```

Forbidden language:

```text
the calibrated CMB branch is derived;
CMB now supports MTS;
the CMB-calibrated parameter shift is just a harmless convention;
the fixed CMB tension kills the parent theory.
```

## 8. Next Target

Create:

```text
37-CMB-calibrated-joint-growth-stress.md
```

Purpose:

```text
take the native CMB-calibrated frozen-shape row and test whether the same
parameter set keeps the growth diagnostic near-competitive, with no support
claim and no parent-derivation claim.
```
