# Stage49 — reconnecting condensate language to the retained MTS parent

6 October 2026. Private continuation of Stage48. Earlier work is preserved.

## What this actually adds

There is a precise route from the **old real motion field and its existing real bath fields** to a phase/amplitude description. It does not require replacing them by another fundamental complex scalar. A positive quadratic bath subfamily also admits a slow cosmological mode and fast matter-like modes in the same action, with a derived matching condition that preserves the slow pole.

This is a conditional construction within the retained architecture, not a numerical selection of its bath spectrum or initial population. The price of identifying appreciable amounts of the original motion variable with a much faster mode is quantified below. A phase-space redefinition alone cannot change a measured timescale.

The finite-charge, fractional-plus-quartic complex candidate studied in Stages1–48 is **not** identified with this construction. Its exact internal charge, isolated-body solutions, surface response and pulse results do not automatically transfer. No original files or parameters are replaced here.

## 1. Ownership, conventions and approximation

Read the original owners:

- `../../4873-Y5-R2FR-covariant-open-parent-action-and-connected-covariance-kernel-to-unit-flow-Kubo-coefficients-or-final-EFT-freeze.md`: real closed bath and its open-system reduction.
- `../../4916-Y5-R2FR-covariantization-map-from-microscopic-motion-action-to-integrated-H-parent-and-no-direct-flow-charge-or-primitive-freeze.md`: common metric and real-linear interaction.
- `../../4938-Y5-R2FR-motion-scale-to-Newton-scale-parent-identity-or-explicit-two-scale-theory-gate.md`: one universal physical motion gap, not independently refitted by arena.
- `../../5192-Y5-R2FR-parent-motion-FLRW-branch-memory-separation-and-mass-gap-cosmology-gate.md`: regular low-energy mass germ and directly integrated cosmology.
- `../../4897-Y5-R2FR-cosmology-without-bath-source-metric-only-baseline-and-derived-extension-reentry-gate.md`: retired bath-driven cosmology is not being revived.
- `../cosmology-reconnection-20261006/results/comparison/status.json`: actual data fits used below.

Use signature(-,+,+,+), c=hbar=1 unless restored, and positive canonical kinetic terms. In a normalized discrete bath subfamily the retained quadratic architecture is

\[
 S_{\psi X}=\int\sqrt{-g}\left[-\tfrac12(\nabla\psi)^2-\tfrac12m_b^2\psi^2
 -\sum_j\tfrac12\{(\nabla X_j)^2+\Omega_j^2X_j^2\}
 +\sum_j g_j\psi X_j\right].
\]

Here m_b is a matching coefficient before bath diagonalization; it is **not** the already calibrated physical gap mu. Couplings g_j have mass dimension2, scalar fields dimension1. The positive quadratic subfamily is an explicit specialization, not a claim that every bath or the full interacting MTS action is Gaussian. Nonlinear and higher-derivative terms require their own inherited matching; Gaussian elimination by itself only generates a quadratic nonlocal kernel, not an independent stabilizing quartic.

S_H and ordinary matter retain the same metric and original normalization. Nothing here derives a new Newton constant or alters their coupling. Bath spectral masses, couplings and a populated state remain physical model inputs; a coherent classical wave is not automatically a thermodynamic Bose–Einstein condensate.

## 2. Exact phase-space map; where averaging enters

For a flat FLRW metric, set chi=a^(3/2)psi and Y_j=a^(3/2)X_j. For a comoving Fourier mode k,

\[
 \ddot\chi+[m_b^2+k^2/a^2-U_H]\chi-\sum_j g_jY_j=0,
 \qquad U_H=\tfrac32\dot H+\tfrac94H^2.
\]

For any fixed positive reference frequency omega, define

\[
 A={e^{i\omega t}\over\sqrt{2\omega}}(\omega\chi+i\dot\chi),
 \quad\chi={Ae^{-i\omega t}+A^*e^{i\omega t}\over\sqrt{2\omega}},
 \quad\dot\chi=-i\sqrt{\omega/2}(Ae^{-i\omega t}-A^*e^{i\omega t}).
\]

After the usual time-dependent boundary transformation for chi, its momentum is dot chi and {A,A*}=-i. This is an invertible map of two real initial data to two real initial data. It does **not** impose a slow-envelope approximation. Define B_j analogously with the same reference frequency. Differentiating the map gives the exact equation

\[
 i\dot A={m_b^2+k^2/a^2-U_H-\omega^2\over2\omega}
 (A+e^{2i\omega t}A^*)
 -\sum_j{g_j\over2\omega}(B_j+e^{2i\omega t}B_j^*).
\]

The conjugate, fast terms must not be silently discarded. A first-order Schrödinger approximation follows only with slow expansion, small gradients/detunings and weak resonant coupling relative to the carrier, or after diagonalizing and using a separate suitable carrier for each mode. A common slow carrier is unsuitable for a light/heavy hierarchy of many orders of magnitude.

For one decoupled mass M the leading envelope satisfies

\[
 i\dot A=-{\nabla^2A\over2Ma^2}-{U_H\over2M}A,
 \qquad H/M,\ |\dot H|/M^2,\ k/(aM)\ll1.
\]

The spatially uniform U_H term shifts the phase. The resulting approximate particle-number symmetry is not the exact local electric U(1) of electromagnetism, nor the exact internal charge of the separate complex candidate. The SK response/average fields are also not two independent physical scalars.

This general real-field/envelope method is established, not claimed as new MTS mathematics: [Namjoo, Guth and Kaiser, 2018](https://arxiv.org/abs/1712.00445), DOI10.1103/PhysRevD.98.016011; curved-background extensions: [Heyen and Floerchinger, 2020](https://arxiv.org/abs/2005.11359), DOI10.1103/PhysRevD.102.036024. The local canonical map and FLRW equation displayed here are differentiated directly in this checkpoint rather than imported as a black box.

## 3. A constructive old-bath completion, not a second motion field

Keep one existing bath mode X with Omega>mu>0. The quadratic mass matrix is

\[
 {\cal M}^2=\begin{pmatrix}m_b^2&-g\\-g&\Omega^2\end{pmatrix}.
\]

Demand that the physical light pole remain the same mu which owns the parent cosmological equation. Its Schur complement gives

\[
 D(s)=m_b^2-s-{g^2\over\Omega^2-s},\qquad
 \boxed{m_b^2=\mu^2+{g^2\over\Omega^2-\mu^2}}.
\]

Put d=Omega^2-mu^2 and eta=g/d. The constant orthogonal transformation

\[
 \begin{pmatrix}\psi\\X\end{pmatrix}
 ={1\over\sqrt{1+\eta^2}}
 \begin{pmatrix}1&-\eta\\\eta&1\end{pmatrix}
 \begin{pmatrix}\ell\\h\end{pmatrix}
\]

gives canonical, decoupled quadratic modes of mass

\[
 \boxed{m_\ell^2=\mu^2,\qquad M_h^2=\Omega^2+\eta^2d.}
\]

Both eigenvalues are positive. The field content has not increased: two old real fields become two normal coordinates. The light mode can follow the old thawing solution while a fast heavy mode admits the cold envelope description. This construction proves compatibility of that quadratic subfamily; it does not show that a particular heavy bath peak or its abundance has already been derived by MTS. Merely adding a bath while setting m_b=mu without matching can move or destabilize the cosmological pole.

The map is constant and metric-independent. Consequently the **full quadratic action**, kinetic stress, potential stress and Hilbert metric variation agree in both coordinates on any background metric. For a homogeneous state,

\[
 \rho=\tfrac12(\dot\psi^2+\dot X^2)
 +\tfrac12m_b^2\psi^2+\tfrac12\Omega^2X^2-g\psi X
 =\tfrac12(\dot\ell^2+\mu^2\ell^2)+\tfrac12(\dot h^2+M_h^2h^2),
\]
\[
 p=\tfrac12(\dot\psi^2+\dot X^2)-V_{\rm total},\qquad
 \dot\rho+3H(\rho+p)=0.
\]

Compute stress from the original covariant action, not from a time-rescaled Hamiltonian mistaken for physical energy. For example a^(3)rho contains (dot chi-3Hchi/2)^2/2, not simply dot chi^2/2. Counting both original fields and their envelopes as separate sources would duplicate the energy.

Existing nonlinear terms rotate too. For example, if an inherited regular germ contains lambda4 psi^4/24, its l^2 h^2 coefficient is lambda4 eta^2/[4(1+eta^2)^2]. This illustrates how a physical cross-coupling would be derived, not a supplied numerical value of lambda4. Nonzero nonlinearities can spoil exact decoupling and must be included before claiming the full interacting cosmology is preserved.

## 4. General positive-bath bound and the quantitative cost

For finitely many normalized bath modes with Omega_j>mu, the same derivation yields

\[
 m_b^2=\mu^2+I_1,\quad
 I_1=\sum_j{g_j^2\over\Omega_j^2-\mu^2},\quad
 Z_\ell={1\over1+I_2},\quad
 I_2=\sum_j{g_j^2\over(\Omega_j^2-\mu^2)^2}.
\]

Z_l is the light pole's squared overlap with the original canonical psi. The orthogonal heavy modes carry total overlap r=1-Z_l, not automatically the same fraction of cosmological energy. Completing the potential square proves positivity because

\[
 m_b^2-\sum_j g_j^2/\Omega_j^2
 =\mu^2+\sum_j{\mu^2g_j^2\over\Omega_j^2(\Omega_j^2-\mu^2)}>0.
\]

For a gapped positive bath, Omega_j>=Omega_min>mu,

\[
 \boxed{\Delta:={m_b^2-\mu^2\over\mu^2}
 \ge\left({\Omega_{\min}^2\over\mu^2}-1\right){r\over1-r}.}
\]

The one-mode result saturates the inequality. Positive convergent spectral integrals obey the same bound with the appropriately normalized positive measure. A gapless dissipative bath at the light frequency is a different case: the undamped-pole construction cannot simply be applied to it. This is not the retired Ohmic cosmology re-entering through a relabeling.

Delta is a **matching cancellation in the original canonical basis**, not a basis-independent or computed quantum-naturalness probability. A symmetry or nonlinear state could protect a hierarchy; neither is supplied by this quadratic exercise.

The actual Stage48 parent fits give mu/H0=0.880676 without Lambda and1.894696 with Lambda. Thus H0/mu=1.13549 or0.527789: their present cosmological modes are not rapidly oscillating cold condensates. These are best-fit points, not a mass posterior; in the zero-amplitude Lambda-containing limit a mass may be unidentifiable.

For an explicitly illustrative galactic scale R=10kpc and v=200km/s, requiring reduced de Broglie wavelength c^2/(M v)<=R gives

\[
 M\gtrsim1.45633\,10^{-9}\ {\rm s}^{-1},\qquad M/H_0\gtrsim6.41968\,10^8
\]

at the inherited fiducial H0=70km/s/Mpc. M is angular frequency and no2pi is included. This is a localization scale estimate, **not a galaxy-data fit or observational confidence limit**. It implies a separation of about3.39e8 to7.29e8 from the fitted slow mode. High-k excitation of the light mass alone would instead be relativistic, not cold galactic material.

For an example bath frequency at that scale and r=1% motion overlap, Delta is approximately1.16e15 (Lambda allowed) or5.37e15 (zero Lambda). If one merely imposes the diagnostic Delta<=1, the allowed overlap is at most8.71e-18 or1.88e-18. That diagnostic is not a law. It shows why a nearly independent heavy bath component is easy, while a strongly motion-owned unified explanation needs an actual hierarchy mechanism. The heavy-mode mass is slightly above Omega for nonzero mixing; the example uses the bath frequency as its stated reference, not an optimized mass bound.

## 5. Back to the universe: what survives, and what must distinguish it

At leading cold order, rho_h proportional a^(-3). Replace a share of the existing dust budget, do not add another dust budget:

\[
 \Omega_m=\Omega_{\rm other}+\Omega_h,\qquad
 E^2=E_{\ell,\Lambda,r}^2+(\Omega_{\rm other}+\Omega_h)a^{-3}.
\]

The share is not determined by the background expansion; ordinary/baryonic abundance still requires its own data. Replayed shares0,25%,75% against the original full-covariance1624 Pantheon+ light-curve rows and13 DESI BAO elements reproduce

| Original parent retained | chi2 |
|---|---:|
| Lambda allowed |1465.101906754732|
| Lambda zero |1465.130710709530|

The largest split/replay difference is2.3e-13. This is **leading-order background degeneracy**, not six independent detections, extra goodness of fit, a finite-mass two-field fit or a new preference over LCDM. H0 and the sound horizon are not independently predicted by this shape-only likelihood. Incorrectly adding75% more dust instead of replacing it gives chi2=1649.76 or1650.32 in an intentionally invalid negative control.

Finite-mass corrections exist. On a prescribed matter-dominated a proportional t^(2/3) background the exact homogeneous solution is h=C cos(Mt+phi)/t. Averaging over a uniform phase at fixed t gives

\[
 \langle\rho_h\rangle={C^2M^2\over2t^2}+{C^2\over4t^4},\quad
 \langle p_h\rangle={C^2\over4t^4},\quad
 {\rho_h-\rho_{\rm dust}\over\rho_{\rm dust}}={9H^2\over8M^2}.
\]

These averaged expressions conserve energy exactly on that prescribed background. They are not a self-consistent finite-mass fit to the actual expansion history, or justification for averaging the slow light mode.

There is also a derived observable discriminator. Restoring weak Newtonian potential Phi_N, the heavy-envelope equation is

\[
 i\dot A=-{\nabla^2 A\over2M a^2}+M\Phi_N A
\]

up to a uniform phase, inherited interactions and higher-order relativistic terms. Write A=sqrt(n)exp(iS), rho_h=M n/a^3, v=grad(S)/(Ma). Its continuity and Euler equations give, after linearization in a subhorizon, nonrelativistic regime,

\[
 \ddot\delta_h+2H\dot\delta_h+{k^4\over4M^2a^4}\delta_h
 =4\pi G(\bar\rho_h\delta_h+\bar\rho_{\rm other}\delta_{\rm other}).
\]

In these natural units the densities are mass/energy densities. This uses the inherited weak-field gravitational coupling, not a new derivation of G. For an isolated self-gravitating heavy component the physical Jeans wavenumber obeys k_J^4=16piG rho_h M^2. Quantum/wave pressure therefore distinguishes this matter route from pressureless dust in structure and galaxies, even when late-time distances do not. A rotation curve, galaxy population, linear-growth transfer function and preparation of the state are not computed here.

## 6. Decision and immediate next physical step

Retain the original parent cosmology. The real phase-space map is usable now. The positive old-bath construction is a candidate **completion with explicit matching cost**, not an identified numerical condensate or a claim to replace the Standard Model. Weak mixing without a sourced spectral/formation mechanism would be a generic scalar dark-matter completion, not evidence for a distinct MTS explanation.

Next use the derived density/current/Poisson system to calculate an actual matter-response prediction: a bounded linear-growth/Jeans transfer scan with the old cosmological background held fixed and identical cold-matter controls, then connect its admissible masses to the galaxy evidence read-only. Keep mass, occupation and mixing as visibly separate inputs; do not fit away the hierarchy or manufacture a spectrum. If this route only supplies ordinary dark matter with no MTS-specific relation, say so and retain the established original galaxy mechanism rather than supplanting it.

The exact algebra, independent real-coordinate ODE replay and inherited observational replay are stored in `results/derivation/status.json` and `results/replay/status.json`. Preservation and independent checks are recorded in `results/validation/status.json` and `results/stage-integrity.json`.
