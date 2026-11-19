# Verified galactic occupation-transport interface

2026-11-10. Local work only.

## Physical result

The retained heavy-mode equations now have an explicit bound-population readout:

    N_B(t_f) = Tr[U_dagger P_B(t_f) U Gamma_i].

For a smooth, gapped instantaneous bound projector, the derived local law is

    N_B_dot = Tr(P_B_dot Gamma),
    |N_B_dot| <= 2 ||Q P_B_dot P_B|| sqrt(N_B (N-N_B)).

A separate moving-aperture flux law tracks matter entering/leaving an environmental volume. These are different mass observables and must not be interchanged. The same inherited metric coupling determines the propagation; neither expression adds a galaxy force parameter.

The final stationary equation does not by itself choose occupation. In the frozen exact two-level control, the same initial state and initial/final Hamiltonians give:
- T=.5: analytic bound fraction0.6847469466226259; integrated0.6847469466225296.
- T=4: analytic bound fraction0.04502067390940435; integrated0.04502067390943863.

The energy changes equal the work of the changing potential to within1.65e-13 in the chosen dimensionless units. These are mathematical transport controls, not percentages predicted for real galaxies. Slow rearrangement, finite-time capture, and changing spatial-aperture counts are no longer conflated.

## Validation

- Original normalized test suite:308 checks pass.
- Supported energy-unit interface:333 checks pass, INCLUDING those308; not641 independent checks.
- Thirty positive-covariance/Hermitian controls check projector identities, independent finite-difference derivatives, the capture bound and spectral-gap bound.
- Maximum original finite-difference projector error is2.6205273236801423e-6 at the coarser step, below the unchanged2e-5 gate; the finer comparison improves for every case.
- Static spectral populations remain fixed; an empty covariance stays empty; explicit extra sources are not discarded.
- Removing coherence in a specified control changes a nonzero instantaneous transfer to zero. That negative control rejects automatic dephasing, not mixed states in general.
- Analytic moving-boundary flux tests include the boundary-velocity term.
- The supported energy_units.py wrapper is invariant under energy rescalings1e-80,1,1e80 and common potential/escape-threshold shifts. The original normalized kernel's absolute guard is not suitable for direct SI-energy calls; the original successful controls and code are preserved. See UNIT-SCALE-NOTE.md.

No empirical gate or arithmetic tolerance was loosened. The two-level and matrix controls do not establish a nonlinear galaxy formation solution or stability theorem. The gap estimate is not applied at threshold crossings.

## Retained preparation recovered, not invented

All41 recorded inherited seed/source dependencies were checked. The1197 primordial rows and gauge table match their saved hashes. There are399 modes at each of a=.0002,.000225,.00025, spanning1e-5through5Mpc^-1; A_s=2.1e-9 and n_s=.9653 remain unchanged.

The saved mass149896.229Mpc^-1 converts, with current library constants, to9.585761788018772e-25eV and kappa=2000kpc km/s. Its7.7341e-11relative difference from the retained quoted9.585761787277403e-25eV is a unit-constant precision difference within the1e-10 algebra gate, not a new mass fit.

These are a global benchmark and finite-band seed, not a unique halo preparation. The original synchronous/gauge conventions, source rounding and unresolved direct gauge-derivative check remain recorded. No raw superhorizon seed is relabelled an isolated Newtonian halo. No ultraviolet modes, independent thermal phases or new local occupation were manufactured.

## What Galaxy Lab can use

The stationary solver already solves the force/state shape problem at a supplied population. DERIVATION.md now specifies how a time-dependent formation calculation can instead produce that population. Independent baryonic geometry and environmental evolution are needed, together with the source-complete initial preparation.

For actual physical energy units use energy_units.py, not the raw normalized helper. Work in an orthonormal basis with grid weights correctly included. The current implementation tests the occupation readout and derivative; it does not replace Galaxy Lab's Poisson solver or propagate an entire cosmological galaxy.

The parent reply is staged in ../MTS-GALACTIC-POPULATION-HANDOFF-20261110.md. It is not automatically sent. The incoming handoff remains attributed to the galaxy agent, and none of its tests are counted as independently verified parent results.

## Next scientific step

Construct the physical initial-state bundle from the retained gauge/real-field data, preserving correlated field and momentum and the anomalous covariance. Quantify which slice/band permits the desired NR accuracy before evolving a finite formation patch. Use the same primordial realization and environmental assumptions for the cold control. Do not default to thermal weights, a spherical ground state, or the old single-light-mode mass. The original full-cell radiation/gravity calculation remains sealed and available; no result has been discarded.
