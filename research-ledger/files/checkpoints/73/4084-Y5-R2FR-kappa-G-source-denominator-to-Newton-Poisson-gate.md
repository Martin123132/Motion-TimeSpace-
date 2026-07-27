# 4084 - Kappa/G Source Denominator To Newton Poisson Gate

- Timestamp: `2026-07-02T03:38:12+00:00`
- Status: `private_nonclaim_checkpoint`
- Decision: `NEWTON_POISSON_GATE_DERIVED_CONDITIONAL_WITH_CALIBRATED_G_SOURCE_DENOMINATOR_STILL_PARENT_UNSIGNED`
- Public local-GR/Newton claim: `false`
- GitHub action: `false`

## Result

This checkpoint locks the first-order Newton bridge in the clean form:

```text
S_EH[g_obs; kappa_ref] + S_matter[e_obs, visible matter]
kappa_ref = 8 pi G_ref / c^4
g_00 = -(1 + 2 Phi_N/c^2)
T_00^H = rho_H c^2
```

Then:

```text
G_00^(1) = 2 nabla^2 Phi_N/c^2
G_00^(1) = kappa_ref T_00^H
nabla^2 Phi_N = 4 pi G_ref rho_H
```

So the Poisson coefficient is derived conditionally from EH plus a calibrated universal `G_ref`.

## No Fitted-GM Laundering

The source denominator is now explicitly:

```text
M_H = int rho_H dV_obs
```

from the parent Hilbert/Hamiltonian source branch. It is not:

```text
M_H := GM_orb / G_ref
```

Orbital `GM` is an output comparison:

```text
Delta_orb = GM_orb - G_ref M_H
```

That matters. It stops the Newtonian limit from being won by definition.

## Calibrated G/Kappa Rows

```text
G_ref = 6.67430000e-11 m^3 kg^-1 s^-2
relative G calibration scale = 2.200e-05
kappa_ref = 2.076647442845e-43
4 pi G_ref = 8.387172739142e-10
Gdot/G residual scale = 1.300e-12 yr^-1
```

This is exactly like GR in one important sense: the local reduction may use a calibrated `G`, but it must not pretend to derive the numerical value of `G`.

## What Improved

4083 lets calibrated visible EM sit inside the Hilbert stress. That means the Newton source can include ordinary matter plus bound EM/Poynting stress once, without the alpha loop blocking the branch.

## What Remains Unsigned

```text
EH/EC parent reduction to observed metric operator
q/e_obs same-frame source functor
Pi_M/H_tau/Hilbert source denominator equality
closed exterior Gauss boundary
slow-geodesic orbital readout with no fifth force
PPN gamma/beta/preferred-frame/conservation stability
```

## Decision

```text
Newton/Poisson coefficient = exact conditional
G numerical value = calibrated, not predicted
source denominator anti-laundering = locked
local GR claim = still false
next gate = source-stable PPN vector
```

## Sources

- NIST/CODATA, Newtonian constant of gravitation, 2022 value.
- Williams, Turyshev and Boggs, lunar laser ranging `Gdot/G` bound.

## Next

```text
4085-Y5-R2FR-source-stable-PPN-vector-gamma-beta-preferred-frame-gate.md
```

If 4085 works, that is where this starts to look genuinely dangerous in the good way: not just Newton, but GR-shaped local tests.
