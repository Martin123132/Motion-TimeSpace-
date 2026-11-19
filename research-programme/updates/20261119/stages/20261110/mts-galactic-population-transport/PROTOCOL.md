# Galactic occupation transport: frozen derivation and checks

2026-11-10. Previous goal turn made verified progress: the saved third-cell calculation is sealed, not left running. This stage answers the next parent handoff without changing the retained action or touching galaxy files.

## Physical target

Derive the map from specified formation initial data to local/bound heavy population in the existing positive quadratic bath. Do not fit a halo mass, add a baryonic scalar coupling, infer local abundance from cosmic fraction alone, or import the old single-light-mode mass benchmark as the current heavy bath mass.

Build on the existing covariance, gauge-seed, stress and weak-field results. The new deliverable is the bound-subspace transport equation, its capture-rate bound, and a precise account of the initial/environmental information that the retained calculation already owns.

The retained example is m_h c^2 = 9.585761787277403e-25 eV, not a derived universal bath spectrum. The existing finite-band seed and empirical primordial spectrum are explicit inputs, not a new state-selection theorem.

## Equations to check before interpreting results

For one realization/common-metric NR evolution, i hbar Gamma_dot=[H,Gamma].
For a differentiable spectral projector P_B of H, [P_B,H]=0 and
N_B=Tr(P_B Gamma), N_B_dot=Tr(P_B_dot Gamma).
With Q=I-P_B, r=||Q P_B_dot P_B||,
|N_B_dot| <= 2 r sqrt(N_B (N-N_B)).
For a separated bound/unbound spectrum with gap Delta>0,
r <= ||Q H_dot P_B||/Delta.
For fixed N, |d arcsin sqrt(N_B/N)/dt|<=r in the open interval.
This assumes a fixed-rank smooth spectral subspace. Threshold crossings, tides without a global escape threshold and relativistic pair sources must be handled separately.

The local aperture count follows a different law:
d integral_Omega n /dt = -integral_boundary (J - n v_boundary).normal.
A bound spectral count and a count inside a chosen spatial aperture are not interchangeable.

## Frozen controls

- Original algebra gate1e-10 and numerical comparison gate2e-5 retained.
- Finite-dimensional Hermitian/projector identities, positivity and exact-rank controls.
- Thirty seeded positive covariance/Hamiltonian pairs; analytic projector derivative versus independent centered differences at two steps.
- Two-level rotating well H=R(theta t/T) diag(-Delta/2,Delta/2) R^T, Delta=2, theta=pi/3, T=.5 and4. Same initial/final operator and initial unbound state. Independently integrate the ODE and compare the prederived transition probability:
  p=theta^2/[theta^2+(Delta T/2)^2] sin^2(sqrt(theta^2+(Delta T/2)^2)).
- Check unitary transport, energy change versus external work and the instantaneous capture-rate bound. A static operator has no spectral capture; a zero initial covariance stays zero.
- Show that deleting off-diagonal coherence falsely removes instantaneous transfer in a specified test state. No phase randomization is introduced in the actual computation.
- Verify moving-aperture flux from an analytic interfering plane-wave solution.
- Verify inherited seed and gauge CSV hashes, count and finite k support. Do not evolve an averaged primordial metric as if it were a realization, extrapolate the k band, or pretend the superhorizon seed is an isolated halo.
- The finite-dimensional controls test transport algebra, not galactic formation, binding stability or observed rotation curves. No baseline-versus-MTS fit claim will be inferred.

## Execution

One Python3.13 worker, -B, BLAS1, below-normal on CPU4, at most600seconds; owner holds checked. No native rebuild, large bank scan, subagent, new catalogue, browser relay, GitHub operation or unrelated process action. Record exact own PID, creation time and command, all input hashes, outputs and completion; verify exit before final reply.
