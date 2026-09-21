# Coupled live P2 canonical inverse and constrained-energy gradient

Private working derivation, 18 September 2026. Continuation of `DERIVATION-20260918-action-derived-live-Gram-stress-and-shape.md`.

## 1. Actual advance

The finite source-fitted P2 field/source momentum map is now inverted jointly with a reconstructed radial metric. It is not replaced by the pointwise continuum relation Pi=R^2 phi_t/(NU). Eight nonzero-wave snapshots cover paired reference/MTS branches, scalar and material refinement, and a nonaffine ordered source map. The same acceptance criteria apply to both branches.

The mathematical additions are:

1. A unique finite momentum inverse at each prescribed positive/timelike metric, using the exact field projection remainder.
2. Its implicit metric tangent and a bound in the natural kinetic norm without an inverse scalar-mesh factor.
3. A conditional constrained-mass Hamiltonian variation identity that retains the global field/source momentum shift.

There are61 successful implementation checks:40 coupled snapshot/tangent checks,8 partition-error diagnosis checks,13 constrained-energy/refinement checks. One failed numerical partition attempt is retained, making32 inherited/current failed attempts in the integrity chain. All four older full-horizon flat-force failures remain unchanged.

This is not a time evolution, a proof of global uniqueness of the nonlinear coupled metric solve, a label-uniform convergence theorem, or the full MTS-to-GR limit.

## 2. Exact finite kinetic blocks

Use the existing source-fitted P2 spatial ansatz, eight source-adjacent subdivisions, reference coefficients a, physical source position b, coefficient rate u=a_dot and source rate V=b_dot. On a label z, let B be the P2 value basis, D the reference derivative basis, and

    R = r + k(r)(b-bstar) + (1-k(r)) epsilon z,
    J = partial_r R > 0,
    H = D a/J,
    f = -k H,
    W = B u + f V,
    s = NU,    A = J R^2/s.

Here f is a scalar sampled function, not a new physical field. W is the Eulerian field time derivative. Integrals below can mean exact spatial integrals, or the same positive quadrature rule used consistently in all kinetic blocks. With spatial measure included,

    M = integral A B^T B,
    d = integral A B^T f,
    I = integral A f^2,
    T_wave = (u^T M u + 2V d^T u + I V^2)/2.

M is the actual five-band P2 mass matrix, not a diagonal replacement. Positivity of A, sufficient positive quadrature and linear independence of the source-constrained basis make M positive definite. The retained Gram contributes potential energy only and does not alter these fixed-metric kinetic blocks.

For source rest mass S0>0 and ell=sqrt(N_b^2-V^2/U_b^2), the per-unit-label momenta are

    pi = M u + d V,
    p_b = d^T u + I V + p_material,
    p_material = S0 V/(U_b^2 ell).

The actual canonical label densities are w(z)pi and w(z)p_b. The material weight is fixed, so the displayed unweighted equations apply in its positive interior; endpoint collocation uses continuous extension, not division by zero weight.

The metric-dependent source field momentum d^T u+I V is retained. It is not identical to a continuum pointwise momentum substitution at finite resolution.

## 3. Unique fixed-metric inverse and a stable Schur complement

Let c=M^-1 d and define

    sigma = I - d^T M^-1 d
          = integral A (f-Bc)^2 >= 0.

The second expression proves nonnegativity and evaluates it without subtracting nearly equal positive numbers. The subtraction formula is separately checked rather than silently clipped to zero. Eliminating u gives

    u = M^-1 pi - c V,
    p_b - d^T M^-1 pi = sigma V + S0 V/(U_b^2 ell).

The right side has derivative

    D_V = sigma + S0 N_b^2/(U_b^2 ell^3) > 0.

As V approaches the two ends of (-N_b U_b,N_b U_b), the source term tends to the corresponding infinities. Hence every finite target momentum has exactly one timelike solution at fixed positive metric. This is a derived inverse, not a guessed source velocity.

The velocity Hessian is

    K = [ M    d                  ],
        [ d^T  I + p_material,V  ],

whose positive Schur complement is D_V. In the principal controls, sigma is about9.159e-6 and the proper source inertia about.044746. Both contributions remain in the equations.

This fixed-metric uniqueness statement does not imply uniqueness of the combined canonical/radial fixed point. That separate nonlinear coupling is numerically checked below, not promoted to a global theorem.

## 4. Implicit metric tangent: no pointwise shortcut

At fixed a,b and canonical momenta, vary the metric by n=delta log N and v=delta log U. Then l=n+v=delta log s, and

    delta M = -integral A l B^T B,
    delta d = -integral A l B^T f,
    delta I = -integral A l f^2.

At fixed source velocity,

    delta_g p_material
      = p_material[-2v_b
          -(N_b^2 n_b + V^2 v_b/U_b^2)/ell^2].

The full velocity tangent solves

    K [delta u, delta V]^T = [F, G]^T,
    F = -delta M u - delta d V,
    G = -delta d^T u - delta I V - delta_g p_material.

The implementation solves the same banded mass equations and scalar Schur equation as the inverse. It does not hold either d or M fixed while changing gravity.

For the natural velocity norm

    ||(xi,zeta)||_K^2
      = integral A(B xi+f zeta)^2 + p_material,V zeta^2,

Cauchy-Schwarz applied to the forcing gives

    ||(delta u,delta V)||_K
       <= ||delta log s||infinity sqrt(2T_wave)
          + |delta_g p_material|/sqrt(p_material,V).

There is no h^-1 in this bound. The constants still require a positive metric and a source separated from its null velocity. This is weighted kinetic/L2 control, not a spatial-derivative, boundary-trace or complete canonical-vector-field estimate. It does not alone transfer the old flat force-convergence proof.

The preceding radial response estimates can bound the metric inputs on their declared loading set. A uniform contraction estimate for the entire feedback map, and propagation of the required label regularity, remain distinct tasks.

## 5. Continuous-label P2 densities and actual coupled solve

Implementation sources:

- `scripts/annular_live_P2_canonical_20260918.py` (executed original, including retained partition failure)
- `scripts/annular_live_P2_canonical_v2_20260918.py` (roundoff-partition correction)
- `scripts/annular_quadratic_source_fitted_action_20260915.py`
- `scripts/annular_locally_refined_source_action_20260916.py`
- `scripts/annular_repaired_live_geometry_20260915.py`

The new layer class reuses the original P2 action and its actual mass/cross/Gram blocks, with the correct label-dependent source-fitted map and an independently reconstructed metric. No old source or evidence file is modified.

At each physical radius, label quadrature is split at crossings of every P2 element edge and the source. The correct inverse node map gives the two Jacobians

    J_i = partial_r R_i,
    j_i = partial_z R_i = (1-k_i)epsilon+k_i b_z.

The Gram density is sum_i w gamma_i/(J_i j_i), as derived in the preceding note. Scalar gradients, Eulerian time derivatives and source rates are continuously averaged BEFORE the nonlinear metric equations are solved.

Writing A_W=<W^2>, A_H=<H^2>, g_G for the Gram density, and d_b=w/b_z on source support,

    D = [A_W/(N^2 U^2)+A_H]/2 + g_G,
    m_R = kappa[R^2 U^2 D + U S0 N d_b/ell],
    (log N)_R = m/(R^2 U^2)+kappa R D
               +kappa S0 V_b^2 d_b/(R N U^3 ell).

The source velocity in these formulas is reconstructed from the current canonical inverse, not frozen to the preparation. Boundary data remain fixed inner mass and N(B)=U(B). Lapse normalization is imposed INSIDE the nonlinear solve; velocities make it invalid to solve at an arbitrary lapse and rescale afterward.

The outer iteration starts from zero rates with a reconstructed rest/potential-loaded metric, alternates the finite inverse with radial reconstruction, and stops only when the rate fixed point meets the declared tolerance. Every perturbation used in the reduced-energy tests repeats this coupled solve from that cold start.

Material coefficients and rates are interpolated by Chebyshev label collocation. This is still not an exact finite-label Galerkin action: off-grid canonical residuals and label refinement are tested and reported. Polynomial extrema, rather than a fixed101-point probe, check positivity of the source and spatial map for these represented polynomials; the calculation is floating point, not interval certification.

The numerical spatial action uses20-point positive quadrature per P2 element; a32-point action/16-point label/higher-radial-order control checks the same canonical states. These are quadrature qualifications of the specified spatial action, not changes to its matter terms.

### Initial rates must belong to the source-fitted chart

The inherited physical profile is phi=.01(R-b) times the same compact envelope and V=.03. At the initial affine map, the coefficient rate is

    a_dot = phi_t + k V phi_R = -(1-k)V phi_R,

not the old fixed-grid rate -V phi_R. The new preparation applies this coordinate conversion explicitly. The nonaffine controls deform the represented source map and label amplitudes without modifying the original stored benchmark data.

## 6. Constrained-mass Hamiltonian variation

This derivation is conditional on a differentiable, ordered, timelike branch of the constraint/canonical solution, continuous label equations and consistent exact spatial integration. It does not assume that finite label collocation is exactly variational.

Let H_red=m(B)/kappa, eta=N/U, e=e_wave+e_G, d the Eulerian material density and p the physical material momentum. The preceding mass-adjoint calculation gives

    delta H_red = integral [s delta e + NE delta d + d V delta p] dR,
    E=sqrt(S0^2+U^2 p^2),    V=N U^2 p/E.

This formula includes the implicit changes of the metric inside the physical loads. It is not obtained by keeping velocities fixed after varying canonical momentum.

For a source displacement xi and label-following momentum variation delta p_label,

    delta d = -partial_R(d xi),
    delta p = delta p_label - p_R xi.

Integration by parts, with the zero endpoint weight, turns the material terms into

    integral w [V delta p_label + partial_R(NE)|_p xi] dz.

The identity partial_R(NE)|_p = -partial_b L_source|_(V,metric)
is the moving-matter gravitational derivative from the preceding note. Thus this is precisely the source Legendre variation, not a new prescribed gravitational force.

For the complete wave-plus-Gram part, the full field/source Legendre transform is

    E_wave = integral w [u dot pi_wave + V p_b,wave - L_wave] dz
           = integral s e dR.

At fixed coordinates/rates, metric variation satisfies delta_g L_wave=-integral e delta s. Differentiating the Legendre identity in two ways, the integral e delta s terms cancel, leaving

    integral s delta e
      = integral w [u dot delta pi_wave + V delta p_b,wave
                    -L_wave,a dot delta a -L_wave,b delta b] dz.

Adding the material contribution yields the conditional reduced identity

    delta H_red = integral w [u dot delta pi + V delta p_b
                              -L_matter,a dot delta a
                              -L_matter,b delta b] dz.

All coordinate covectors on the right hold the Eulerian metric fixed during matter variation, retaining its spatial gradients at moving quadrature/source positions. All metric feedback on the LEFT is re-solved. The global source field momentum is required for this identity; discarding it breaks the calculation.

Under the exact conditional canonical equations this identity has the formal Hamiltonian energy-conservation consequence. It is NOT an independent local Einstein mass-current proof, an evolved numerical conservation result, or an unrestricted covariance theorem. The tests here check eight independent directional variations of H_red against the canonical pairing. Their success is evidence of implementation consistency, not a proof inferred from samples.

## 7. Controls and results

Evidence:

- `scripts/qualify_annular_live_P2_canonical_20260918.py`
- `scripts/qualify_annular_live_P2_canonical_v2_20260918.py`
- `scripts/diagnose_annular_live_P2_edges_20260918.py`
- `scripts/qualify_annular_live_P2_reduced_energy_20260918.py`
- `source-intake/navier-stokes/20260914/annular-live-P2-canonical-attempt01/status.json` (failed; retained)
- `source-intake/navier-stokes/20260914/annular-live-P2-canonical-attempt02/status.json`
- `source-intake/navier-stokes/20260914/annular-live-P2-edge-diagnosis-attempt01/status.json`
- `source-intake/navier-stokes/20260914/annular-live-P2-reduced-energy-attempt01/status.json`

The shared cases are base17/label4/radial12, base17/label8/radial12, nonaffine base17/label6/radial18, and base33/label4/radial14, each for reference and MTS. The actual P2 free scalar counts are62 and94 respectively. Source width=.02, central mass=.7, rest mass=.03 and coupling=.1 stay unchanged. They are branch-normalized controls, not fitted physical constants.

| Diagnostic | Result |
| --- | --- |
| Cold-start coupled velocity round trip | <=1.74e-17 |
| Nodal canonical momentum residual | <=2.61e-18 |
| Independent off-grid radial mass residual | <=5.18e-11 |
| Affine label4 to label8 off-grid momentum residual | about4.95e-10 to7.16e-11 |
| Nonaffine off-grid momentum residual | about3.16e-10 |
| Coupled outer iterations | 3 affine,4 nonaffine |
| Metric inverse tangent vs independent perturbed inversions | <=3.20e-14 |
| Fixed-metric finite Legendre envelope check | <=8.36e-15 |
| Constrained-mass gradients vs canonical velocity/force pairing | <=2.69e-12 |

The observed affine label residual improves but does not disappear at finite degree. No uniform label-refinement rate is inferred. Numerical tolerances are not rigorous rounding-error bounds.

Two negative controls matter physically for this calculation:

- Dropping the field source momentum predicts source speed about.032361 instead of.030000 in BOTH branches. It is a7.87% error in this control, not a negligible convention.
- Holding the inverse metric at the central Schwarzschild background leaves canonical momentum residuals around2.50e-6 after live loading is restored; this shortcut is detected.

The zero-wave reference/MTS arrays agree exactly in the saved control calculation. Setting coupling to zero recovers the same central Schwarzschild metric, not flat space. These baseline controls are not replaced by an MTS-only criterion.

### Retained partition failure and diagnosed correction

Attempt01 passed the first paired snapshots, then failed the reference label8 off-grid radial check: mass/lapse derivative errors6.45/1.46. The cause was a duplicate physical band boundary represented1.77636e-15 apart at R=6.02875. Dividing a tiny polynomial interpolation error by this machine-width interval created a spurious large derivative.

The new immutable implementation merges only coincident endpoints within32 scaled machine epsilons (4.839e-14 here). Its smallest remaining interval is.00125. It changes no action, state, radial equation or acceptance threshold.

An independent paired diagnosis reproduces the same issue in MTS, with old residuals5.17/1.28, then checks both corrections. The largest mass/lapse profile change is4.45e-16 and canonical momenta change by less than6.51e-19; new radial residuals are below8.47e-12 in those diagnosis cases. Thus this was a shared partition-roundoff defect, not an MTS inconsistency. The failed executed attempt and its source remain immutable.

The inherited sparse-construction FutureWarning remains visible; old sealed code was not modified merely to suppress it.

## 8. What is now available, and the next calculation

The programme now has a checked finite P2 canonical/geometry snapshot map and its metric tangent, rather than only a prescribed geometry inverse or an independently varied density. The constrained-energy gradient checks include both fields and source, both coordinates and momenta, and both branches. These are concrete ingredients for the next live evolution step.

Next derive the independent moving-source P2 temporal mass current from the actual action/transport terms, then run a short paired live evolution with that current and unprojected constrained-energy checks. Do not use a finite difference of the radial mass as the DEFINITION of the supposedly independent current. Do not substitute the older P1 current formula without carrying the source-fitted field momentum, moving Gram atoms and measure terms through the derivation.

Still separate: global coupled-solve existence/uniqueness, high-frequency stability and boundary traces, propagation of label regularity, long-time force convergence, parent-owned couplings, full four-dimensional covariance and the full GR limit. No old finite-grid physics gate is upgraded by this checkpoint.

Final integrity ledger: `source-intake/navier-stokes/20260914/annular-live-P2-canonical-final-integrity.json`. Require state complete before treating this note and its evidence as sealed. All work is local; no GitHub action.
