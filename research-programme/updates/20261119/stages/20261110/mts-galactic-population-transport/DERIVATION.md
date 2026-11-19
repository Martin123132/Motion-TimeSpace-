# From retained preparation to galactic occupation: transport, capture and boundary

10 November 2026. This builds on the retained real-bath action, covariance and weak-field equations. It does not restart MTS or replace the empirical galaxy model.

## 1. Answer to the galaxy handoff

The parent owns a concrete heavy-field equation and its metric coupling. It also owns a benchmark cosmological preparation and finite-band perturbation seed. It does **not** currently specify the initial realization and formation/environmental history of NGC3521 or the other pilot galaxies. A unique numerical local population is therefore not supplied.

There is a more useful next step than assigning another normalization: the equations determine a transport functional for the population, given that preparation and history. The derivation below supplies it, a rate bound and a boundary-flux check. They allow a formation calculation to predict occupation rather than set it from Vobs.

A dynamical action need not uniquely determine all initial conditions, in MTS or in GR. A shared, explicitly calibrated primordial preparation can support a fair conditional prediction. What would be circular is selecting a separate initial state for each galaxy using its rotation curve and calling the resulting normalization derived.

## 2. Source ownership and what is already specified

Paths in this section are relative to the parent post-checkpoint-work directory; frozen-inputs.json and result.json record exact absolute paths and hashes.

- MTS-HEAVY-BATH-COUNTERFLOW-AND-GALACTIC-STRESS.md: the quadratic heavy subfamily, inherited gravitational coefficient, stationary states, force tests and the stated example mass.
- condensate-origin-20261003/motion-bath-matching-20261006/49-real-motion-envelope-and-existing-bath-matching.md: exact real phase-space map and positive bath diagonalization. The pole and matching conditions do not select abundance.
- condensate-origin-20261003/heavy-interaction-and-condensate-bridge-20261007/52-heavy-mode-interactions-and-condensate-coherence.md: inherited interaction vertices; these are not permission to insert an arbitrary relaxation law.
- MTS-COVARIANCE-TO-GRAVITATING-STATE.md and mts-covariance-dynamics-20261107/: normal/anomalous covariance, Hilbert stress, common-metric versus realization-specific gravity, 1,197 sourced seed rows and subsequent gauge interface.
- MTS-RETAINED-HIERARCHY-AND-RETARDED-COUPLING.md and mts-independent-poisson-evolution-20261107/DERIVATION.md: self-consistent retained linear hierarchy and the owned gauge/weak-field map. A later linear source calculation is not automatically a nonlinear formation simulation.
- condensate-origin-20261003/radiation-and-slow-field-transfer-20261007/radiation_common.py: the benchmark H0=70 km/s/Mpc, A_s=2.1e-9 and n_s=0.9653; the present example uses the retained half-matter heavy share, replacing rather than adding to the matter budget.
- 5152-Y5-R2FR-primordial-motion-occupation-dust-limit-Jeans-window-and-formation-source-arbitration.md: a historical primordial-state construction, explicitly leaving its abundance input. Its older single-motion-mode masses are **not** substituted for the later heavy bath example.

The retained example m_h c^2=9.585761787277403e-25 eV corresponds to kappa=hbar/m_h approximately2000 kpc km/s. This remains an illustrative bath mass, not a uniquely derived physical spectrum. Keep heavy overlap in the original motion coordinate, global matter fraction, local mass and largest coherent occupation as distinct quantities.

The saved seed spans399 modes per epoch, 1e-5<=k<=5 Mpc^-1, at a=.0002,.000225,.00025. Its relative envelope and anomalous covariance retain correlated density/phase data; independent thermal phases would change the preparation. The original seed is in a specified synchronous representation. The subsequent gauge-seed.csv supplies Newtonian metric/source mappings, with its recorded rounding and unresolved direct-derivative qualification. Later integral/physical replays do not erase that qualification.

This is useful initial-state evidence, not a complete catalogue of halo realizations. A power spectrum alone also does not select Gaussian higher moments; if Gaussian statistics are adopted, label that preparation assumption. The mean field, anomalous correlations and the declared normalization are not replaced by the diagonal excess covariance.

## 3. Restoring a cosmological preparation instead of an isolated wall

In the leading number-conserving, nonrelativistic weak-field limit let A=a^(3/2) psi_phys be the comoving envelope, with weights absorbed into factors A_alpha. For comoving coordinates x in length units and cosmic time t,

    i hbar d_t A_alpha = H A_alpha,
    H = -hbar^2 laplacian_x/(2m_h a^2) + m_h Phi,
    Gamma(x,y) = sum_alpha A_alpha(x) A_alpha*(y),
    n_c(x) = Gamma(x,x),  rho_h = m_h n_c/a^3,
    laplacian_x Phi = 4pi G a^2 [rho_h+rho_b+rho_other - rho_bar_total].

Other sources are the retained ones within the specified Newtonian reduction; relativistic species cannot be arbitrarily relabelled cold. The homogeneous background controls a(t), rather than being included again in the periodic peculiar Poisson source. In a local isolated patch take a=1 and use its asymptotic/environmental potential instead of the cosmological mean subtraction.

The spatially uniform FLRW phase term in Stage49 can be removed without changing density/current. A physical reference for escape energy is still required before "negative energy" can mean gravitational binding. Setting a periodic potential's spatial mean to zero does not supply an escape surface.

The quadratic number symmetry is approximate with respect to the original real relativistic action. All assertions about constant N below refer to this declared NR system. Expansion, gradients, interactions and pairing terms need their retained error control before it becomes a precision galaxy model.

## 4. Population in an aperture comes from flux

Differentiate Gamma using the envelope equation. Potential terms cancel on the diagonal:

    d_t n_c + div_x J_c = 0,
    J_c = hbar/(2 i m_h a^2)
          [(grad_x-grad_y)Gamma(x,y)]_(y=x).

For a moving comoving aperture Omega(t), with boundary velocity w,

    d_t N_Omega = -integral_boundary [J_c - n_c w].normal dS,
    N_Omega = integral_Omega n_c d^3x.

Multiplying by m_h gives the mass balance. The w term matters if a fixed proper aperture is described in expanding coordinates. An isolated zero-flux wall would impose a different preparation; it is not derivable from a SPARC radial table.

In the parent GR description the corresponding approximate current is integrated with the physical hypersurface volume and normal. The displayed formula is its leading weak-field/comoving reduction, not a claim that metric-volume corrections vanish exactly.

## 5. Occupation in a bound spectral subspace: the new transport law

On one specified realization trajectory, or in the explicitly common-metric Hartree approximation already described by the parent,

    i hbar Gamma_dot = [H[Gamma,t], Gamma].
    Gamma(t) = U(t,t_i;Gamma_i) Gamma_i U_dagger(t,t_i;Gamma_i).

The propagator is unitary along that trajectory even when the potential is self-consistent. It depends on the initial state through the potential. An ensemble of separate classical universes has separate propagators; its average cannot in general be evolved with one average potential.

Choose a smooth, fixed-rank spectral projector P_B(t) of H, using a physically specified escape threshold and a spectral gap. Then

    [P_B,H]=0,
    N_B(t)=Tr(P_B Gamma),
    boxed: N_B_dot = Tr(P_B_dot Gamma).

This follows directly by differentiating the trace and using cyclicity. It is not an imposed source term. It gives the final population functional

    boxed: N_B(t_f)=Tr[U_dagger P_B(t_f) U Gamma_i].

In an initial mode basis with covariance C_i this is Tr(K_B C_i), where
(K_B)_ab=<u_a|U_dagger P_B U|u_b>. The capture operator obeys0<=K_B<=I.
No new force coefficient or halo mass enters K_B. The baryonic and exterior histories determine it through the same Hamiltonian.

For isolated instantaneous eigenstates b in the selected subspace and u outside it, differentiating H|b>=E_b|b> yields

    <u|P_B_dot|b> = <u|H_dot|b>/(E_b-E_u).

Only off-diagonal subspace coherence contributes to the instantaneous trace. Replacing Gamma by a newly dephased diagonal matrix at every time would delete that response. Conversely, a static H gives P_B_dot=0 and no change in its bound spectral count, even if density inside an aperture moves.

Self-gravity does not invalidate the identity: H_dot then includes the evolving wave density. Gravitational rearrangement and radiation of unbound waves can alter a core's population while conserving global N. The identity therefore does not exclude gravitational cooling or nonlinear collapse.

## 6. A rigorous rate bound within that approximation

Let Q=I-P_B, N=Tr Gamma, N_U=Tr(Q Gamma), and r=||Q P_B_dot P_B||.
Differentiating P_B^2=P_B gives P_B P_B_dot P_B=Q P_B_dot Q=0.
Writing the positive covariance as a sum of rank-one factors and using
Cauchy--Schwarz on their bound/unbound parts gives

    boxed: |N_B_dot| <= 2 r sqrt(N_B N_U).

For a fixed total N>0 and0<N_B<N,

    |d_t arcsin sqrt(N_B/N)| <= r.

The integrated inequality extends to endpoints by continuity. It bounds the
possible change; it is not a positive lower bound on capture.

If every selected energy lies below every unselected energy with gap Delta,
the off-diagonal projector derivative solves a separated Sylvester equation.
Its integral representation by two decaying semigroups gives

    r <= ||Q H_dot P_B||/Delta.

For a local fixed-a mass-constant Hamiltonian, H_dot=m_h Phi_dot; in an expanding
patch the kinetic derivative -2Hubble*T must also be retained. For a
self-consistent potential this is a conditional bound on the actual
formation history, not a way to replace that history by an observed speed.

No gap is asserted at the birth/disappearance of a bound state or a continuum
threshold. The projector derivative formula and gap bound must not be used
there; continue the full wave initial-value problem and define the final
observable, or use a declared spatial aperture. A tidally open evolving halo
need not admit a globally conserved bound/unbound split.

## 7. Why global number conservation does not freeze the galaxy

A rotating two-level Hamiltonian supplies an exact control, not a galaxy fit:

    H(t)=R(theta t/T) diag(-Delta/2,+Delta/2) R^T(theta t/T).

Start in the unbound state. In the rotating frame the constant operator is
D-i hbar (theta/T)J, where J=[[0,-1],[1,0]]. At hbar=1 its exponential gives

    p_B(T) = theta^2/[theta^2+(Delta T/2)^2]
             sin^2(sqrt(theta^2+(Delta T/2)^2)).

Fixing theta and Delta fixes the initial and final Hamiltonians. Different
durations nevertheless give different final bound occupation: the history
matters, not merely the final stationary equation. The test uses Delta=2,
theta=pi/3,T=.5and4, before looking at numerical results. All work done by
the prescribed time-dependent potential is checked through
d< H >/dt=< H_dot >. It is not an unexplained gain/loss of energy.

This example also shows why optimizing a stationary solution at a chosen
N is not a derivation of N or proof that the system selects its ground state.

## 8. Beyond conserved NR number

For a genuinely extra source C in Gamma_dot, the general equation is

    N_B_dot=Tr(P_B_dot Gamma)+Tr(P_B C).

The parent already derives normal/anomalous covariance coupling before the
NR averaging:
i hbar Gamma_dot=[A,Gamma]+B Sigma_dagger-Sigma B_dagger.
Thus pairing supplies C=-(i/hbar)(B Sigma_dagger-Sigma B_dagger).
It cannot be set to zero outside its controlled averaging regime. Likewise,
the classical-ensemble metric-correlation term is a distinct contribution,
not a freely tuned capture/damping coefficient.

The available finite-band covariance can initialize a specified preparation.
It does not provide a numerical universal rate for these terms, an independent
formation history, or an ultraviolet completion of the spectrum.

## 9. What now needs to be supplied once, not refitted galaxy by galaxy

A formation experiment can freeze the following input bundle before looking
at rotation-curve targets:

1. The retained heavy spectrum/share and cosmological background, with their
   fitted, illustrative or derived status recorded.
2. A physical initial slice with real field/normal-time-derivative data (or
   their controlled envelope/covariance), common primordial realization,
   baryonic/other-species data, coordinate/gauge and volume conventions.
3. Independent baryonic formation data or a declared baryonic evolution
   model, plus large-scale tidal/inflow conditions on the simulated patch.
4. A boundary treatment and final mass observable: spatial aperture,
   asymptotically bound projector, or another explicitly defined halo finder.
5. Spatial/temporal convergence and domain/initial-band checks. The saved
   k<=5Mpc^-1 band may seed later small scales through collapse, but omitted
   initial modes cannot be silently set to zero and called irrelevant.

For one such bundle, evolve each realization with its own metric. N_B or
N_Omega is then an output. A local stationary solver can be compared with the
result; it is not used to choose the population retrospectively.

This supplies a derivable route without requiring a parameter-free origin of
all initial conditions. The same preparation discipline must be applied to
the cold baseline. No galaxy RMSE or success against a null follows from the
transport tests.

## 10. Implementation and external-method provenance

population_transport.py operates in an orthonormal finite basis. Grid
quadrature weights must be absorbed into the basis/factors before use;
a raw cylindrical matrix with volume weights is not automatically Hermitian
in the Euclidean inner product. It includes fixed-rank threshold guards,
the explicit pairing/other-source slot, and the positive capture operator.
It is a small interface/check implementation, not a replacement galaxy solver.

The field-to-envelope reduction is established methodology:
[Namjoo, Guth and Kaiser](https://arxiv.org/abs/1712.00445),
[Heyen and Floerchinger](https://arxiv.org/abs/2005.11359).
[Hui, Ostriker, Tremaine and Witten](https://arxiv.org/abs/1610.08297)
discuss gravitational wave-halo structure and relaxation; their phenomenological
halo relations are not imported as a state-selection law here.
The projector identities and bounds above are derived explicitly here within
the stated mathematical assumptions; no claim of new general spectral theory
or of a quantum Yang--Mills mass gap is made.
