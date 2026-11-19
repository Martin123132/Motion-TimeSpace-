# Longer coupled interval without changing the action

This stage uses the retained shared-distribution background, direct late hierarchy and canonical four-coordinate heavy field. The mathematical equations and coupling coefficients are those derived and checked in mts-shared-moment-perturbation-20261110/DERIVATION.md. No new force law is introduced to improve this control.

## What extending the interval requires

The short-window interpolation is not extrapolated. Reintegrate the same background equations, starting from the identical scalar field, velocity and Friedmann normalization:

    d phi/dN = u/H;
    d u/dN = -2u - a^2 m_s^2 phi/H;
    d H/dN = -(R+3P)/(6H);
    d tau/dN = 1/H,

where N=ln(a/a_start), a_start=1/11, 0<=N<=0.01, and the shared shell-distribution neutrino density and pressure enter R,P. Generate both32/64momentum backgrounds. Reuse the actual masses and thermal amplitude; do not refit H0 or infer a new mass from a different normalization rule. Reuse the existing differential Taylor-jet construction for the canonical carrier and pressure clock.

Thermal opacity and baryon sound speed remain functions ofa from the retained native thermal solution. Evaluate them over the new interval and check interpolation at independent midpoints. Seventeen native captures verify that the same regime signature applies across the interval: no tight coupling, the same photon/massless-neutrino streaming approximation, no new thermal perturbation coordinates, no massive-neutrino fluid switch, and unchanged angular cutoff16. This checks regime compatibility, not accuracy of every approximation.

## Exact seed and source continuity

Before evolution, compare all full matrix rows and physical source rows on the old overlap. The longer reference must reproduce the previously tested equations there. Compare fresh live-D0 preparations with the saved states, then reuse the saved states byte for byte. The choice Theta=1e-6 remains a controlled perturbation, not a new fitted parameter or formation law.

The same eight-step restart and fourth-order exponential solver is used at128/256time steps. Canonical fast coordinates remain in the evolution. Readouts at common scale-factor points are reached by a short exponential substep, never by interpolation of oscillating state coordinates.

The shared-neutrino source identities remain

    D_nu' + H(D_nu+3P_nu) + kQ_nu + kz(R_nu+Pbar_nu)=0;
    Q_nu' + 2HQ_nu - kP_nu + 2kPi_nu/3=0.

Test these as full coefficient rows using the actual longer operator and independently computed background density-plus-pressure, not only on one chosen trajectory. This carries the derived coupling consistency into the enlarged window.

## Tests that must not be conflated

1. Time-step refinement of the state and each physical source.
2.32/64momentum-rule refinement at common scale factors.
3. Independently differentiated Phi'+H Psi-Q/(2k), Hamiltonian constraint, source budget and scalar energy/current equations.
4. Sampled source ordering: source derivatives divided by k times the history's peak source density, and pressure divided by that same source density. Peak normalization avoids fictitious divergences at a zero source crossing; it is a sampled diagnostic, not a pointwise or uniform expansion bound.
5. Angular-tail occupancy at l15/l16. Momentum and time-step convergence do not establish angular convergence. A high tail calls for a larger hierarchy or a characteristic/line-of-sight reference, not an adjusted tolerance.

The retained late angular closure uses the absolute conformal clock. For a deliberately prepared late perturbation, a new free-streaming front can populate high multipoles even though the original primordial history's high multipoles were small. Testing this is a physical check on the retained approximation, not merely on arithmetic.

## Scope

This still tests the explicit controlled late initial-value problem and existing approximations. Extending its interval is not replacing the saved primordial history, deriving a galactic occupation, modifying data, or importing a constructive-QFT theorem. Physical claims about cosmological history require the retained early/matching regimes and derived initial data. The work stays within the retained action and provides evidence on when its coupled numerical realization is trustworthy.
