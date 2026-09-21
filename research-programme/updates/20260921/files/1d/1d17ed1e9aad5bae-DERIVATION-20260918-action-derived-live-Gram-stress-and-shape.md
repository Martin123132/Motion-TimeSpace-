# Action-derived live Gram stress and source shape response

18 September 2026. Private continuation of `DERIVATION-20260918-live-metric-response-and-moving-mass-hessian.md`.

## 1. Result and its scope

The specific retained MTS Gram term DOES preserve the preceding scalar radial cancellation. This follows by varying its actual lapse and radial-metric dependence, not by assigning it a convenient equation of state:

    rho_Gram = p_radial,Gram = F g_Gram >= 0.

Consequently the radial constraint equations use e_total=e_wave+R^2 g_Gram and have the same characteristic-speed identity as before. The term gravitates and exerts a nonzero source shape force; neither effect is discarded. Both its source transport and spatial-Jacobian variation are essential.

This note also derives a grid-independent shape-force bound, a quadratic field-to-density estimate, and a fixed-width source-map sensitivity estimate with explicit label-regularity requirements. Numerical checks use the existing locally refined P2 action, including all its Gram rows, rather than transferring a P1 result without checking.

Scope is the specified finite Gram extension in the conditional spherical/polar branch. A unique covariant parent extension, full off-diagonal stress/current, the coupled finite canonical inverse and full live P2 force convergence are NOT established. The older scalar/Gram mesh-refinement limit is still not a physical parent-coupling decoupling theorem.

## 2. The action that is actually being varied

The source files are:

- `scripts/annular_quadratic_source_fitted_action_20260915.py`
- `scripts/annular_locally_refined_source_action_20260916.py`
- `scripts/annular_source_fitted_action_20260915.py`
- `scripts/annular_moving_collar_sparse_20260914.py`
- `scripts/derive_annular_source_fitted_live_pullback_20260915.py`

The first two implement the P2 family and eight-fold source-adjacent subdivision used here. The positive sampling matrix is denoted S_sample, the retained source-lifted factor matrix L, the original Gram spacing h_G, and the field coefficients a(z). Neither the reference anchor nor L changes when physical source position b changes. In particular, the source lift must not be differentiated as though its reference anchor were the moving physical source.

Set

    r_f(z) = (L a(z))_f,
    gamma_i(z) = sum_f (S_sample)_(fi) r_f(z)^2/(2h_G) >= 0.

The matrices retain every original row. The implementation may skip structurally zero nodal sampling columns when assembling densities, but it does not discard small factors or source-adjacent factors.

Let k(r) be the existing piecewise-affine global source displacement shape: k=1 at the reference source anchor bstar and k=0 at the outer endpoints. For physical material width epsilon and label z in [-1/2,1/2],

    R(r,z) = r + k(r)[b(z)-bstar] + [1-k(r)] epsilon z,
    J(r,z) = partial_r R = 1 + k_r(r)[b(z)-bstar-epsilon z],
    j(r,z) = partial_z R = epsilon + k(r)[b_z(z)-epsilon].

Assume J,j>0. Write R_i=R(r_i,z), J_i=J(r_i,z), j_i=j(r_i,z), C(R)=R^2 N(R)U(R). The exact Gram part of the retained action is

    L_G = - integral w(z) sum_i gamma_i(z) C(R_i(z))/J_i(z) dz,
    w(z)=6(z+1/2)(1/2-z).

This is exactly the sampled coefficient `S_sample @ (C/J)` in the existing action, rearranged by transposition. It has no velocity dependence, hence no separate Gram contribution to the kinetic source/field momentum. The rest of the action still has its nonzero field-source momentum shift.

## 3. Independent lapse and radial-metric variations

For the diagonal metric ds^2=-N^2 dt^2+U^-2 dR^2+R^2 dOmega^2, the reduced stress convention is

    delta L = - integral [R^2 rho/U delta N
                          + N R^2 p_radial/U^2 delta U] dR.

The angular normalization is absorbed as in the preceding branch equations. Hold the matter coefficients and source map fixed during metric variation. The pushforward density is

    g_G(R) = sum_i [w(z_i) gamma_i(z_i)/(J_i(z_i) j_i(z_i))],
    R_i(z_i)=R,

where only in-range inverse labels contribute. Because J_i,j_i and gamma_i do not depend on N or U in this fixed matter chart,

    delta_N L_G = - integral R^2 U g_G delta N dR,
    delta_U L_G = - integral R^2 N g_G delta U dR.

Comparison with the stress definition yields

    rho_G = U^2 g_G = p_radial,G.

The equality is an identity for arbitrary independent smooth lapse/root test variations, also as a weak measure before continuous-label spreading. It is not an empirical cancellation between fitted parameters. A potential-like term would instead have different U dependence; the previous negative-control counterexample remains valid and is not contradicted.

Only the diagonal response of this specified radial action is being derived. This does not infer its full four-dimensional covariance, angular stress, off-diagonal shift current, or a unique extension of the original MTS corpus.

## 4. The live radial equations retain the cancellation

Use the same source rest mass S0, material momentum p, source density d and coupling kappa as the preceding note, and q=sqrt(F(S0^2+F p^2)), F=U^2=1-2m/R. With

    e_total = e_wave + e_G,    e_G=R^2 g_G,

the varied equations are

    m_R = kappa [F e_total + q d],
    (log N)_R = m/(R^2 F) + kappa e_total/R
                + kappa d F p^2/(R q).

Therefore, for s=NU,

    (log s)_R = 2m/(R^2 F) - kappa S0^2 d/(R q).

There is no direct local e_G term in this last equation, but the Gram changes m and N through the first two equations. On the preceding fixed-source loading set, replacing e_wave by e_total gives the same proven finite-difference bounds

    ||delta m||infinity <= kappa ||delta e_total||L1,
    ||delta s||infinity <= C0 ||delta e_total||L1,
    ||delta s_R||infinity <= C1 ||delta e_total||L1,

where C0=.11563843793783894 and C1=.05144223534787455 for that declared set. The cap is now on TOTAL canonical loading, not just the scalar part. The controls below remain below .004138 against the .05 cap.

Here s is the metric coefficient of the local scalar bulk operator. It is not the complete dispersion relation of the finite nonlocal Gram operator. Its controlled radial response does not by itself prove high-frequency stability or identical propagation speeds for every MTS mode.

The proof uses F>=f>0 and fixed positive material thickness. It does not extend through a trapped-surface coordinate singularity or to zero collar width.

## 5. Source shape force from the same action

Let delta b(z)=v(z) while holding reference field coefficients and the Eulerian metric fixed. Then delta R_i=k_i v, delta J_i=k'_i v, and delta gamma_i=0. The exact shape covector per weighted material label is

    F_G(z) = -sum_i gamma_i [k_i C_R(R_i)/J_i
                            - C(R_i) k'_i/J_i^2].

Its pairing is delta_b L_G=integral w F_G v dz. The two terms represent atom transport and spatial-Jacobian dilation. The source-fitted lift and all source-adjacent rows are retained; there is no additional derivative of the fixed matrix L with respect to physical b.

For a general field variation,

    delta_a L_G = - integral w [L delta a]^T
                        diag(S_sample(C/J)/h_G) [L a] dz.

Together these formulas are the complete Gram coordinate covectors in this chart. They are not the whole material force: the scalar kinetic source momentum, ordinary scalar spatial term and material proper-time action remain separate.

### A shape-force bound without inverse scalar-grid factors

Since C=R^2 s,

    C_R/C = 2/R + A_g,    A_g=(log s)_R.

For |k|<=1, |k'|<=K1, J>=Jmin, R>=r and |A_g|<=Amax,

    |integral w F_G v dz|
      <= ||v||infinity [2/r + Amax + K1/Jmin] V_G,
    V_G = integral w sum_i gamma_i C(R_i)/J_i dz >= 0.

The shape-force estimate contains no scalar mesh h. Its constants depend on the source map and gravitational loading set. This is more informative than simply announcing that a source derivative is missing.

At fixed a,b, the effect of a change of reconstructed metric obeys

    |delta_metric <F_G,v>|
      <= ||v||infinity E_G [(2/r+K1/Jmin)||delta s||infinity
                            +||delta s_R||infinity],
    E_G=integral e_G dR.

Combining with section4 gives a Lipschitz metric contribution to this Gram shape force. When comparing a scalar baseline to the same loads plus a fixed Gram component, ||delta e_total||1=E_G and this particular force-response bound is O(E_G^2). That is not a claim that the entire MTS force or trajectory difference is quadratic.

## 6. Weak source variation and transport

Define the atom mass a_i(z)=w(z)gamma_i(z)/J_i(z). At fixed nodal field,

    delta g_G = sum_i push_i[-w gamma_i k'_i v/J_i^2]
               - partial_R sum_i push_i[a_i k_i v],

where push_i[f](R)=f(z_i)/j_i(z_i). Against any smooth test psi,

    integral psi delta g_G dR
      = integral w sum_i gamma_i v
          [k_i psi_R(R_i)/J_i - k'_i psi(R_i)/J_i^2] dz.

The variation of j_i in the physical density is encoded by the divergence term; it must not be separately omitted or counted twice. In particular j_i is not generally epsilon. Tests with a curved material map detect a 5.06% to 9.78% weak-moment error from substituting epsilon for j_i.

For time-dependent a,b, let V=b_t. Then

    partial_t g_G + partial_R sum_i push_i[a_i k_i V]
      = sum_i push_i[w gamma_i_dot/J_i
                     -w gamma_i k'_i V/J_i^2],
    gamma_i_dot = sum_f S_sample_(fi) (L a)_f (L a_dot)_f/h_G.

The factor-work term is present even when geometry is fixed. This weak identity is exact bookkeeping for the transported Gram measure. It is not yet the full Einstein mass-current equation: that also uses scalar/source Euler equations, the correct canonical inverse and the action's shift variation. A density transport identity alone must not be marketed as a complete Bianchi/conservation proof.

## 7. Quantitative field and source-map sensitivity

### Field changes on a common map

For fixed b, use the positive Gram seminorm

    ||a||_G^2 = integral w sum_f [S_sample(R_i^2/J_i)]_f
                              (L a)_f^2/h_G dz = 2E_G(a).

Difference of squares, positivity of S_sample, and Cauchy-Schwarz give

    ||e_G(a)-e_G(c)||L1
       <= (||a||_G+||c||_G)||a-c||_G/2.

The seminorm is allowed to have a kernel; the ordinary wave term supplies its usual additional control. On an ordered map with bounded radius/J, this seminorm is uniformly comparable to its fixed-reference Gram counterpart. There is no need to estimate each small atom separately with an inverse inequality.

In the canonical-DENSITY functional of the preceding note, append the positive Gram features to the wave feature vector y. Then e_total=|y_augmented|^2/2 and the same fixed-position wave/material-momentum Hessian bound applies on the same TOTAL loading set. This is a restriction of a positive quadratic-feature estimate, not an assertion that the finite nodal momentum inverse is already identical to the continuum pointwise inverse.

### Source-map changes require label control, not just weighted energy

Let

    G0=integral sum_i gamma_i dz,
    G1=integral sum_i |partial_z gamma_i| dz,
    W0=||w||infinity, W1=||w_z||infinity,
    D0=||v||infinity, D1=||v_z||infinity,
    |J_z|<=Jzmax, |b_zz|<=B2, J>=Jmin, j>=jmin>0.

Define

    A0 = W0 G0/Jmin,
    A1 = (W1 G0+W0 G1)/Jmin + W0 Jzmax G0/Jmin^2.

The weak source formula and differentiation of a_i k_i v/j_i give

    ||delta_b g_G||L1 <= W0 K1 G0 D0/Jmin^2
        + D0 A1/jmin + A0 D1/jmin + A0 B2 D0/jmin^2,
    ||delta_b e_G||L1 <= B^2 ||delta_b g_G||L1,

where B is a common outer-radius bound. Zero endpoint values of w remove endpoint delta masses. No h appears, but jmin tracks the physical width. Integrating along a common ordered-map segment gives a finite-difference bound.

The extra hypotheses are visible: w vanishes at the label endpoints, so weighted conserved energy alone does not control G0 or G1. Positive sampling and factorization give a sufficient condition in terms of unweighted label norms of L a and L a_z. For row-normalized sampling,

    G0 = ||L a||_(L2_z)^2/(2h_G),
    G1 <= ||L a||_(L2_z) ||L a_z||_(L2_z)/h_G.

These are assumptions to propagate in a live label-regularity argument, not an unproved consequence of scalar mesh refinement. The controlled polynomial label profiles here satisfy them. No uniform-in-label-degree or shell-crossing theorem is claimed.

## 8. Qualification: action, measure and live constraints

New implementation/evidence:

- `scripts/annular_live_gram_stress_20260918.py`
- `scripts/qualify_annular_live_gram_stress_20260918.py`
- `scripts/qualify_annular_live_gram_radial_20260918.py`
- `scripts/qualify_annular_Gram_shape_L1_bound_20260918.py`
- `source-intake/navier-stokes/20260914/annular-live-P2-Gram-stress-attempt01/status.json`
- `source-intake/navier-stokes/20260914/annular-live-P2-Gram-radial-attempt01/status.json`
- `source-intake/navier-stokes/20260914/annular-Gram-shape-L1-bound-attempt01/status.json`

**186 successful implementation checks:**114 action/stress/transport checks,42 constraint-response checks,30 source-map L1 checks. No new failed attempt. The inherited31 failures and four old full-horizon flat-force failures stay preserved and are not reclassified.

The action tests independently subtract the existing reference action from the existing MTS action on the SAME P2 chart, then vary N, U, the scalar coefficients and b. They include original smooth-profile controls and nontrivial oscillatory controls normalized to E_G=.002, on base grids33,129,257 with eight source subdivisions. This normalization is solely a numerical control; it is not a physical rescaling of the programme's original data or action.

The strongest checks are:

| Check | Observed discrepancy |
| --- | --- |
| Existing-action independent lapse/root variations vs derived Gram covectors | <=1.10e-18 |
| Pulled label integral vs independently inverted physical density moments | relative <=8.38e-15 |
| Physical density source-shape differences vs weak analytic derivative | scaled <=2.46e-9 |
| Wrong constant-width label Jacobian | detected5.06%-9.78% error |
| Dropped whole-atom transport | detected in every profile/grid case |

The radial tests hash-verify and reconstruct the saved degree64 scalar initial snapshot, using the same positive density adapter as the preceding note. They add the exact retained Gram density with the actual affine initial material map, keep its scalar canonical density and material momentum fixed, and re-solve the nonlinear radial constraints. These are OFF-SHELL constraint comparisons, not evolved solutions or a qualification of the complete finite P2 canonical state.

For the fixed E_G=.002 controls:

| Base grid | Max change in m | Max change in s | Max change in s_R |
| --- | --- | --- | --- |
| 33 | .0001531700 | .0000501176 | .00000692769 |
| 129 | .0001533117 | .0000495413 | .00000668803 |
| 257 | .0001534339 | .0000504677 | .00000731233 |
| Analytic common bound | .0002 | .0002312769 | .0001028845 |

Every control retains the derived cancellation and lies in the loading set. A second radial integrator checks the nontrivial129-grid case. The Gram source-force metric change is also below its derived bound. Very small smooth-profile responses can lie below the numerical control's absolute allowance, so those rows alone are not evidence for high-relative-precision asymptotics; the fixed-energy controls avoid that false comfort.

The source-shape L1 controls use a nonaffine map with Jmin=.9 and jmin=.017. At fixed E_G=.002 their measured canonical-density derivative norms are about .028-.070, against conservative bounds .775-.795. These are deliberately non-sharp bounds derived from the displayed regularity constants, not constants fitted to the samples. The two difference steps are recorded; no convergence rate is inferred from them.

An inherited SciPy sparse-construction FutureWarning appears during these tests. It does not cause a numerical failure; the old sealed constructor was not modified merely to suppress it.

## 9. The remaining concrete interface

The previous question, "does the actual retained Gram add an uncontrolled rho-pr term?", is answered: **no, not for this action in this radial chart**. The action-derived shape force and measure sensitivities are now explicit. Repeating that missing-stress question or another held-flat mesh pair is not the next step.

Next derive and qualify the finite moving-source kinetic inverse WITH the reconstructed metric: the nodal mass matrix and global field-source momentum shift depend on the metric, whereas the continuum shorthand Pi=R^2 phi_t/(NU) is pointwise. A finite projection must not be silently replaced by that shorthand. Use the actual P2 banded mass/cross blocks, retain the timelike material term and field Schur complement, then differentiate the constraint/canonical solve and test its energy/current residual. The Gram calculations here provide its spatial and source-shape contributions.

The label regularity assumptions in section7 still need propagation; a complete nonlinear live trajectory/convergence theorem remains beyond this checkpoint. Nothing here resolves unrestricted spacetime covariance, empirical parameters, black-hole regularity or the full MTS-to-GR limit.

Final seal: `source-intake/navier-stokes/20260914/annular-live-Gram-stress-final-integrity.json`. Its state must be complete before treating this checkpoint as immutable verified evidence. No GitHub action or publication is authorized by this local step.
