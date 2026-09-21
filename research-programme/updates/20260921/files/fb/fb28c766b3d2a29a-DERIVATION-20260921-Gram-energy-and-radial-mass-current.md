# Same-action Gram energy transport and radial mass-current test

Private derivation, September 21, 2026. Numerical run complete; the final integrity record determines independent-reconstruction status. This extends `DERIVATION-20260921-cell-flux-and-Gram-reaction-balance.md`; its source-force identity and saved phase points are unchanged.

## 1. Derive the actual discrete transport, rather than name a flux

At each material label z the saved action has a fixed reference-space factor D and sampling map S. Set y=D u, gamma_i=beta(r_i)/J_i, A=S gamma, beta=r^2 N sqrt(F). Its Gram potential is

    E_G = 1/2 sum_k A_k y_k^2,
    h_i = gamma_i/2 sum_k S_ki y_k^2,
    F_i = -sum_k D_ki A_k y_k.

The nodal allocation h is exactly the allocation used by the existing radial mass constraint. D is NOT recomputed from physical node positions. Use all saved rows, including compensation tails. Reference u_t=v is not the physical phi_t when the mesh moves.

Define C_ij=sum_k gamma_i S_ki y_k D_kj v_j and the antisymmetric outgoing bond current J_ij=C_ji-C_ij. Direct differentiation gives the off-shell identity

    hdot_i + v_i F_i + sum_j J_ij = Q_i,
    Q_i = gamma_dot_i/2 sum_k S_ki y_k^2.

For any cut into left/right nodes this gives a computable current without constructing a dense bond matrix:

    J_G(cut) = sum_k y_k [ A_k (D v_left)_k - (S gamma_left)_k (D v)_k ]
             = sum_(i left) [ -v_i F_i - gamma_i (S^T(y*ydot))_i ].

These formulae are exact algebra for any D,S with time-independent entries, not an on-shell or continuum approximation. Reversing every bond orientation reverses the reported current. Different nodal allocations could change local routing; we fix the allocation already used by the candidate.

## 2. Mesh motion and explicit geometry exchange

Node radius is r_i=chi(x_i,b,z), velocity W_i=chi_b V. In physical radius the energy measure sum_i h_i delta(r-r_i) carries advective flux sum_i W_i h_i delta(r-r_i), in addition to the cut current. Integrating over material labels converts the delta by the positive label Jacobian; omit neither that Jacobian nor the spatial J in gamma.

The coefficient derivative splits as

    gamma_dot = gamma_b V + gamma (N_t/N + F_t/(2F)) at fixed physical r,
    F_G,b = -1/2 sum_i gamma_b,i sum_k S_ki y_k^2.

Consequently the total Gram power identity is

    dE_G/dt + sum_i v_i F_i + V F_G,b
      = 1/2 sum_i gamma_i [N_t/N+F_t/(2F)] sum_k S_ki y_k^2.

The right side is metric exchange, not a failure of autonomous total-system conservation. Coupling this identity with the already derived cellwise wave identity and dust/source work is the energy-accounting bridge. Numerical residuals include archived tangent/inverse and differentiation errors.

## 3. The gravitational test is separate

For ds^2=-N^2 dt^2+F^(-1)dr^2+r^2 dOmega^2 and F=1-2mu/r, direct Christoffel/Ricci calculation gives G^r_t=-F_t/r=2mu_t/r^2. With the existing spherical normalization, the minimal scalar and dust mixed equation would require

    mu_t + J_wave + J_dust = 0,
    J_wave = -kappa r^2 F <phi_t phi_r>,
    J_dust = V mu_r,dust,
    mu_r,dust = kappa m rho_label sqrt(F) N/s,
    s^2=N^2-V^2/F.

The wave sign gives decreasing enclosed mass for an outgoing wave. Test this on the reference as well as BOTH MTS variants; the finite-element reference is not automatically an exact pointwise continuum solution.

The Gram contribution to the radial constraint has nodal mass m_i=a_i h_i, a_i=kappa sqrt(F_i)/N_i. This does not by itself prove that a(R) times its cut energy current is the mixed Einstein source. Indeed, defining the symmetric bond-weighted mass current J^m_ij=(a_i+a_j)J_ij/2 gives exactly

    mdot_i + a_i v_i F_i + sum_j J^m_ij
      = a_i Q_i + adot_i h_i + 1/2 sum_j (a_j-a_i) J_ij.

Thus spatial redshift variation produces a bond exchange term. A general shift/covariant completion must account for it. We evaluate a(R)*(J_G+advection) only as a clearly labelled candidate diagnostic, never as a derived stress tensor or fitted correction. A success would motivate the completion, not replace it; a failure cannot by itself reject every such completion.

## 4. Numerical experiment, fixed in advance

- Reuse six qualified phase points, 42 archived radial solutions, all16,425 canonical components. No new trajectory, cutoffs, fit coefficients or mode deletion.
- Same257 initial/258 endpoint physical cuts in allthree branches:129 across the annulus and129 across/near the source, with duplicates removed. Domain endpoints are excluded.
- Differentiate mu at FIXED physical radius, not at a material label. Reconstruct the mass excess from radial primitives before differencing; compare ordinary subtraction as a roundoff diagnostic.
- Three archived central steps, two Richardson estimates; these are directional phase-space probes, not an independently integrated time series.
- Wave integrals split material labels where P2 cells cross each radius, orders28/48. Gram cut integration uses nodewise label primitives, degrees32/64, and clips each primitive at the inverse node map. This avoids sampling discontinuous cut masks on one unsplit label grid. Check degree sensitivity; it is not a rigorous quadrature enclosure.
- Predeclared profile tolerance1e-10+1e-3*maximum mass-current scale. Apply equally to reference and MTS; retain failures without altering the threshold. Global Gram power cancellation has an absolute plus summed-work-scaled floating-point gate, not a fitted physical tolerance.
- Local coordinate units and kappa=.1 are inherited test normalizations, not measured SI parameters. No empirical GR-precision claim follows from the residuals.

## 5. Evidence

Runner: `scripts/run_annular_candidate_energy_current_20260921.py`.
Helper: `scripts/annular_candidate_energy_current_20260921.py`.
Prior seal: `source-intake/navier-stokes/20260914/annular-candidate-reaction-balance-final-integrity.json`.
New evidence: `source-intake/navier-stokes/20260914/annular-candidate-energy-current-attempt01/status.json`.

## 6. Numerical result and what it actually resolves

Allsix cases complete in83.72seconds, reusing the expensive prior geometry rather than solving it again. All119 implementation checks and36 predeclared smoke comparisons pass. The latter thresholds are intentionally loose; inspect the residuals themselves, not just green flags.

For the MTS branches, the Gram energy current has maximum~2.55e-10, comprising graph transfer~2.53e-10 and mesh advection~3.67e-12 (their maxima occur at different radii and do not simply add). Explicit metric exchange is retained. Global Gram power cancellation error is at most1.38e-22; direct finite-difference energy-rate discrepancy at most4.23e-21 and geometry-exchange balance discrepancy at most1.14e-20. These are numerical checks of a derived discrete identity, not measured physical accuracy.

At the wider endpoint, max|mu_t+J| is1.375e-11 in the reference,5.223e-11 in MTS with wave/dust only, and3.667e-11 with the explicitly conditional Gram current added. The global current scale is~.00593, dominated by the source. Outside the source the wave scale is~2.82e-5, so the conditional MTS remainder is~1.30e-6 of that smaller scale, not merely a few parts in a billion. The new current accounts for some, not all, of the smaller discrepancy without any fit. Both MTS variants give essentially the same profile in this experiment.

The initial max mass-derivative change is~1.34e-10 and larger than the total mass-current remainder there; do not claim its small residual is resolved. Wider endpoint change~5.73e-12 is smaller but remains material to the remaining wave-region discrepancy. Degree32/64 Gram-current changes, after candidate conversion, are below5.44e-24; wave order28/48 changes are below9e-19. These observed sensitivities are not full error enclosures. The same reference treatment matters: its endpoint remainder1.375e-11 is nonzero too.

## 7. A derived route from local stress balance to the mixed Einstein equation

This is the next useful analytical bridge, not a new axiom. Write the existing two radial constraints in stress notation:

    mu_r = kappa r^2 rho,
    (log N)_r = mu/(r^2 F) + kappa r p_r/F,
    F=1-2mu/r.

Then A=(log(N/sqrt(F)))_r=kappa r(rho+p_r)/F. Let J=-kappa r^2 T^r_t, rho=-T^t_t, p_r=T^r_r, and define the stress-divergence defect H=div_mu T^mu_t. For a symmetric spherically symmetric stress tensor, direct evaluation of that divergence gives

    H = -rho_t - [J_r+A J]/(kappa r^2) + (rho+p_r)F_t/(2F).

Differentiate the mass constraint, use F_t=-2mu_t/r, and define R=mu_t+J. Without imposing the mixed Einstein equation one obtains

    R_r + A R = -kappa r^2 H,
    [N R/sqrt(F)]_r = -kappa r^2 N H/sqrt(F).

Hence the exact annular propagation formula is

    R(r) = sqrt(F(r))/N(r) * {
        N(r_in) R(r_in)/sqrt(F(r_in))
        - kappa integral_(r_in)^r x^2 N(x) H(x)/sqrt(F(x)) dx }.

Local stress conservation plus compatible inner current implies R=0 throughout this untrapped chart. More generally the absolute value is bounded by the same positive prefactor times the absolute inner term plus kappa times the integral with |H|. This is a conditional derived conservation/GR link, not a claim that H has already vanished for the discretized candidate. Its assumptions are N>0,F>0, consistent normalization, radial constraints and sufficient regularity (or a justified measure-valued face treatment). It is not a horizon-crossing argument.

For the minimal scalar alone, H_scalar=phi_t E/(r^2 N/sqrt(F)) with E=-partial_t(alpha phi_t)+partial_r(beta phi_r). Thus the weighted propagation source is precisely -kappa phi_t E. At moving internal P2 faces, E has flux-jump contributions and phi_t can jump; multiplying a delta by one arbitrarily chosen trace is not legitimate. The energy jump identity supplies the appropriate averaged traces. Dust/source work and Gram metric variation must be included consistently. Weak FE equations annihilate allowed test functions, not arbitrary radius-truncated energy tests.

This identifies a concrete next calculation: reconstruct the wave/kinetic discrete current, its cell/face work and the Gram metric/shift contribution, then use the propagation formula to explain or bound the remaining R. Merely defining H from the measured R would be a tautology; H must be obtained independently from the action/EL quantities. Do not fit a multiplier to the Gram energy current or replace this step with another list of missing inputs.
