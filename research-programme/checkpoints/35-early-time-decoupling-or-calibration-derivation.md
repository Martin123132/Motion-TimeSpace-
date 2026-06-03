# Early-Time Decoupling or Calibration Derivation

## 1. Purpose

This file follows:

```text
34-CMB-compatible-MTS-limit-contract.md
```

The question is:

```text
Can the locked MTS/C0 memory branch be made CMB-compatible because the memory
term decouples at recombination, or is the CMB-calibrated branch still only
phenomenological closure?
```

Short answer:

```text
the direct recombination/plasma contribution is safely bounded, but the CMB
distance branch is not derived. The memory term is tiny against matter+radiation
at z_star, yet D_M(z_star) still samples the late-time expansion where b_mem
matters. So the CMB-calibrated branch remains closure-only until a parent
H0/Omega_m0/b_mem calibration map is derived.
```

## 2. Machine Run

Implemented:

```text
scripts/early_time_decoupling_or_calibration_derivation.py
```

Successful run:

```text
runs/20260531-004152-early-time-decoupling-or-calibration-derivation/status.json
```

Readout:

```text
early_time_memory_bound_passes_CMB_distance_calibration_remains_closure_only
```

## 3. Exact M6 Memory Form

The frozen branch uses:

```text
E_M6^2(z) = Omega_m0 (1+z)^3 + 1 - Omega_m0 + b_mem F(N)
N = ln(1+z)
F(N) = 1 - exp[-(N/u_s)^nu]
u_s = alpha_act ln((1-Omega_m0)/Omega_m0)/3
```

Locked values:

```text
h0 = 67.91792167906756
Omega_m0 = 0.3009916276432578
b_mem = 0.0880607293391193
alpha_act = 1.0543379145228584
nu_act = 1.7500073382761008
z_star = 1091.5182931260854
```

At recombination:

```text
F(z_star) = 1 to machine precision
log10(1-F) = -109.96017933412008
b_mem dF/dN = 6.11264537727496e-110
```

So the transition source has effectively switched off by recombination.

## 4. Recombination Bound

The direct fractional memory contribution to H^2 at recombination is:

```text
|b_mem F(z_star)| /
[Omega_m0(1+z_star)^3 + Omega_r0(1+z_star)^4 + 1 - Omega_m0]
= 1.6885841317095195e-10
```

Worst-case saturated bound:

```text
|b_mem| /
[Omega_m0(1+z_star)^3 + Omega_r0(1+z_star)^4 + 1 - Omega_m0]
= 1.6885841317095195e-10
```

Therefore:

```text
delta H/H <= 8.442920658547598e-11
```

This passes the high-redshift background decoupling test for recombination and
sound-horizon source physics.

## 5. Why This Does Not Rescue CMB Yet

At fixed `h0` and `Omega_m0`, turning off only `b_mem` gives:

```text
D_M(z_star) fractional shift = -0.00527378720955813
l_A fractional shift = -0.00527378719497626
R fractional shift = -0.0052737872095580925
r_s(z_star) fractional shift = -1.4659164316786716e-11
```

Interpretation:

```text
the sound horizon is basically unaffected by direct early-time memory, but the
angular-diameter/shift distance is affected through the low-redshift line of
sight. That is exactly where the parent calibration map is missing.
```

So the CMB issue is not:

```text
memory ruining recombination physics.
```

It is:

```text
how H0, Omega_m0, and b_mem are jointly calibrated between late-time SN/BAO,
growth, and CMB distance observables.
```

## 6. Gate Result

Passed:

```text
exact M6 memory formula identified;
direct recombination H^2 bound;
activation source switched off by recombination.
```

Failed:

```text
CMB line-of-sight distance decoupling;
parent calibration map derivation;
CMB support claim;
C0 death claim.
```

## 7. Decision

Allowed language:

```text
the locked M6 memory term is safely negligible for direct recombination
background physics, but CMB distance compatibility remains a calibration-map
problem.
```

Forbidden language:

```text
MTS is supported by CMB;
MTS is ruled out by CMB;
the CMB-calibrated branch is derived;
the fixed CMB tension kills the parent theory.
```

## 8. Next Target

Create:

```text
36-parent-CMB-calibration-map-attempt.md
```

Purpose:

```text
attempt to derive the parent map that tells us whether H0, Omega_m0, and b_mem
are one shared physical parameter set across SN/BAO/growth/CMB, or whether the
CMB-calibrated branch must stay permanently secondary.
```
