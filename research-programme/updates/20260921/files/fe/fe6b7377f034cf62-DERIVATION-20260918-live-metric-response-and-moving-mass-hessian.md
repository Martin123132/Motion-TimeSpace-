# Live radial metric response and moving-matter mass Hessian

Private working derivation, 18 September 2026. Internal argument with independent numerical implementation controls; not independently reviewed proof and not a full GR/MTS limit claim.

## What is actually advanced

The preceding full-interval argument was for prescribed-flat, source-fitted P2 semidiscrete systems. Here gravity is reconstructed from the radial constraints, including nonzero material momentum. Three previously unavailable pieces are derived for the existing conditional spherical scalar-plus-layer sector:

1. The moving-source first and second variations of constrained exterior mass, with the correct wave, source-velocity and proper-clock adjoints.
2. A wave-density L1 to wave-speed W1,infinity estimate with constants independent of scalar grid spacing and of the concentration width of that wave-density perturbation.
3. A positive joint wave/material-momentum Hessian lower bound on an explicit weak-field loading set, at fixed material positions/density.

The extra live-metric contribution to the canonical bulk wave residual then has no inverse-grid loss on a regular comparison field. This closes a specific part of the live-geometry extension; it does not complete the moving-source canonical chart, the finite P2 constrained action, or its force convergence.

The stress cancellation is NOT valid for arbitrary extra MTS stress. A general-stress identity and a counterexample identify precisely what must be checked next instead of concealing that distinction.

## 1. Existing equations, not a new fitted model

Source equations and provenance:

- `DERIVATION-20260915-independent-live-continuum-GR-oracle.md`
- `DERIVATION-20260915-repaired-live-canonical-geometry-and-current.md`
- `DERIVATION-20260914-live-constrained-mass-relative-energy.md`
- `DERIVATION-20260918-full-interval-force-comparison-path.md`
- `scripts/annular_live_continuum_characteristics_20260915.py`
- `scripts/annular_live_barycentric_20260915.py`
- `scripts/derive_annular_source_fitted_live_pullback_20260915.py`

Use the existing branch's dimensionless radial normalization, not laboratory units or newly derived parent coefficients. On A <= R <= B:

    ds^2 = -N^2 dt^2 + F^-1 dR^2 + R^2 dOmega^2,
    F = 1 - 2m/R = U^2 > 0,    s = NU,
    P = phi_t/s,    H = phi_R,    Pi = R^2 P,
    e = R^2 <P^2 + H^2>/2,
    d = w(z(R))/b_z(z(R)),    p = p_material(z(R)),
    E = sqrt(S^2 + F p^2),    q = U E = sqrt(F(S^2+F p^2)),
    m_R = kappa (F e + q d),
    (log N)_R = m/(R^2 F) + kappa e/R + kappa d F p^2/(R q).

The brackets mean the existing weighted material-label average where multiple scalar layers occupy a radius. The source density d is nonnegative with fixed positive physical thickness and an ordered label map. S > 0 is rest mass. Crucially p is material momentum, not the finite source-fitted canonical P_b that contains a field-momentum shift.

Boundary normalization is m(A)=m_in fixed and N(B)=sqrt(F(B)), at the FULL outer boundary of this branch. Then H_ADM=m(B)/kappa. Changing to the earlier inner-clock normalization introduces its state-dependent clock factor; that factor has not been silently dropped from that earlier model.

This audit varies fixed Eulerian canonical densities, not fixed coordinate velocities. Reconstructing N after changing a velocity load without changing its canonical interpretation would be a different operation.

## 2. Moving constrained-mass variations

Partial derivatives below hold R fixed and use F_m=-2/R:

    q_m  = -(S^2+2F p^2)/(R q),
    q_p  = F^2 p/q,
    q_S  = F S/q,
    q_mm = -S^4/(R^2 q^3),
    q_mp = -F^2 p(3S^2+2F p^2)/(R q^3),
    q_pp = F^3 S^2/q^3.

Let a=kappa(2e/R-d q_m) >= 0 and eta(R)=exp(-integral_R^B a). The two radial equations imply

    (log(N/U))_R = a,    eta = N/U.

For independent straight-line perturbations de, dd, dp, the first mass variation u=delta m solves

    u_R + a u = kappa [F de + q dd + d q_p dp],    u(A)=0.

Variation of constants gives the exact functional derivative

    D H_ADM = integral eta [F de + q dd + d q_p dp] dR.

Allowing rest-mass variation adds integral eta d q_S dS. Its coefficients reduce to

    eta F   = NU = s,
    eta q_p = N F p/E = source coordinate velocity,
    eta q_S = N S/E   = source proper-clock rate.

These are identities, not calibration choices. A global S variation measures the density-weighted integral of clock rate; a label-dependent variation gives the corresponding local coefficient.

The second mass variation v along the same straight loading path obeys

    v_R + a v = kappa [
        -4 u de/R
        + d(q_mm u^2 + 2q_mp u dp + q_pp dp^2)
        + 2dd(q_m u + q_p dp)],    v(A)=0.

For a nonlinear loading path add F d2e + q d2d + d q_p d2p to the bracket. In particular, canonical field variations make e quadratic, and that positive second-density term must not be omitted.

An independently implemented lapse tangent l=delta log N has

    l_R = g_m u + kappa de/R + g_d dd + g_p dp,
    l(B) = -u(B)/(B F(B)),
    g_m = 1/(R^2 F^2) - kappa d F S^2 p^2/(R^2 q^3),
    g_d = kappa F p^2/(R q),
    g_p = kappa d F^2 p(2S^2+F p^2)/(R q^3).

Both the moving first variation and second variation are checked by re-solving the nonlinear radial problem at perturbed loads, not only by comparing two rearrangements of the same formula.

## 3. Source translation: the gravitational part, not the whole force

Translate the material profile, so dd=-d_R db and dp=-p_R db for constant db, while holding Eulerian scalar density e fixed. Since d vanishes at the collar endpoints, integration by parts gives

    D_b H_ADM = integral d [partial_R(NE)]_(p fixed) dR,

    [partial_R(NE)]_(p fixed)
      = N [E(log N)_R + (p^2/E)(m/R^2-m_R/R)]
      = N m/R^2 (E/F+p^2/E) + kappa N S^2 e/(R E).

Explicit d terms cancel, but the source's gravitational mass remains inside m and N. This is not absence of self-gravity. The canonical force has a minus sign relative to the energy gradient. Radiation traction, moving scalar domains and the source field-momentum shift are additional terms: this held-e translation is not falsely identified with the whole source equation.

## 4. An explicit untrapped loading set

Assume nonnegative e,d, R>=r>0, integral e<=Ebar, integral d<=D1, ||d||infinity<=Dinf, |p|<=pstar, and fixed S,kappa,m_in>0. While F>0, monotonicity gives 0<F<=1 and

    m <= Mbar = m_in + kappa[Ebar + sqrt(S^2+pstar^2) D1].

If 1-2Mbar/r >= f>0, continuation of the radial equation cannot first reach F=0. This establishes a common metric floor from total loading, rather than from a few sampled minima. The same loading bounds apply along convex interpolations of nonnegative e with d,p fixed.

For the controls below:

    r=5.19, m_in=.7, kappa=.1, S=.03,
    Ebar=.05, D1=1, Dinf=75, pstar=.005,
    Mbar=.708041381265149,
    1-2Mbar/r=.7271516835201738 > f=.5.

The saved source's Chebyshev-coefficient l1 bound gives |p|<=.0013405733595306473, not just a sampled momentum maximum. Its frozen scalar loading integrates to .0021379670373143853; all positive spike controls add only .002. Source width stays .02. These are branch-normalized mathematical bounds, not observed astrophysical limits.

## 5. Wave-density to metric bound with no inverse-grid factor

First fix d and p, and vary only e. From the nonnegative integrating factor,

    ||u||infinity <= kappa ||de||L1.

Since |q_mm|<=S/(r^2 f^(3/2)),

    ||delta log eta||infinity <= Leta ||de||L1,
    Leta = 2kappa/r + kappa^2 S D1/(r^2 f^(3/2)).

Now s=F eta, so

    delta log s = -2u/(RF) + delta log eta,
    ||delta s||infinity <= C0 ||de||L1,
    C0 = 2kappa/(r f) + Leta,

using 0<s<=1. The crucial radial identity is

    s_R/s = A_g = 2m/(R^2 F) - kappa S^2 d/(R q).

The local scalar density e has canceled from A_g. It still sources m and N; its gravitational effect has not been set to zero. Differentiating A_g at fixed d,p,

    (A_g)_m = 2/(R^2 F^2)
              - kappa S^2 d(S^2+2F p^2)/(R^2 q^3).

Safe bounds are

    Amax = 2Mbar/(r^2 f) + kappa S Dinf/(r sqrt(f)),
    Bmax = 2/(r^2 f^2)
           + kappa Dinf(S^2+2pstar^2)/(r^2 S f^(3/2)),
    ||delta s_R||infinity <= C1 ||de||L1,
    C1 = kappa Bmax + Amax C0.

Integrate these derivative estimates along the nonnegative loading segment to obtain finite-difference estimates. For the declared loading set:

    C0=.11563843793783894,
    C1=.05144223534787455.

Neither contains the scalar mesh h or the width of a wave-energy concentration. They do depend on the physical source collar through Dinf. This is NOT a zero-thickness theorem.

### Moving source inputs can be separated explicitly

For general loading variations write Qmax=sqrt(S^2+pstar^2), Qp=pstar/S,
Qm=(S^2+2pstar^2)/(r sqrt(f) S), Qmm=S/(r^2 f^(3/2)),
Qmp=pstar(3S^2+2pstar^2)/(r S^3). Then

    Uvar = kappa[||de||1 + Qmax||dd||1 + D1 Qp||dp||infinity],
    ||u||infinity <= Uvar,
    Lvar = 2Uvar/(r f) + 2kappa||de||1/r
           + kappa[D1 Qmm Uvar + Qm||dd||1 + D1 Qmp||dp||infinity],
    ||delta s||infinity <= Lvar,
    ||delta s_R||infinity <= Amax Lvar + Bmax Uvar
        + kappa S||dd||infinity/(r sqrt(f))
        + kappa Dinf pstar||dp||infinity/(r S).

Thus the scalar input still needs only L1 control, but the source-density input genuinely needs stronger control. For ordered C2 material maps with b_z>=jmin>0, fixed Lipschitz weight w vanishing at its endpoints, first variations at fixed R satisfy

    delta z = -delta b/b_z,
    delta d = (w_z/b_z - w b_zz/b_z^2) delta z
              - w delta b_z/b_z^2,
    delta p_Eulerian = delta p_label + p_z delta z.

Consequently C1 control of b and suitable label regularity bound the displayed source terms, with constants depending on jmin and label derivatives. The zero extension across collar edges is Lipschitz, not globally C3. These formulas do not supply a uniform high-label-degree theorem or allow shell crossing.

## 6. Joint wave/momentum coercivity at fixed material positions

Set y=R(P,H), with the appropriate weighted label norm, so e=|y|^2/2. For a canonical field direction xi and a material momentum direction zeta, holding d fixed,

    de = y dot xi,    d2e=|xi|^2,
    H_ADM'' = integral eta [F|xi|^2 + d q_pp zeta^2
        -4u(y dot xi)/R + d(q_mm u^2+2q_mp u zeta)].

The last terms are gravitational binding terms and need not be positive. They are retained in the estimate and tests.

Let x=||xi||L2, z=||zeta||L2(d), Y=sqrt(2Ebar), c=(pstar/S)sqrt(D1). Define

    abar = kappa[2Ebar/r + D1(S^2+2pstar^2)/(r sqrt(f) S)],
    eta_min=exp(-abar),
    Dpositive=diag(f eta_min,
        eta_min f^(3/2) S^2/(S^2+pstar^2)^(3/2)).

The source equation gives ||u||infinity <= kappa(Y x+c z). Hence

    H_ADM'' >= (x,z) [Dpositive - Bbinding] (x,z)^T,

where the symmetric binding matrix has entries

    B11=4kappa Y^2/r + Qmm D1 kappa^2 Y^2,
    B12=2kappa Yc/r + Qmm D1 kappa^2 Yc
        + Qmp sqrt(D1) kappa Y,
    B22=Qmm D1 kappa^2 c^2 + 2Qmp sqrt(D1) kappa c.

For the same declared loading set the lower matrix is

    [ .490896833771175    -.00513559424933957 ]
    [ -.00513559424933957  11.2758006972862   ],

with smallest eigenvalue .490894388286019>0 in these branch-normalized variables. Thus the constrained mass is uniformly strongly convex in these fixed-position wave/material-momentum directions on this loading set. The matrix estimate is analytic; three sampled directions only check its implementation.

This is NOT a lower bound in every moving-source canonical coordinate. Moving b, the finite field-momentum shift, boundary traces and the metric-constrained finite mass matrix remain to be incorporated. Nor does it prove a uniform third derivative for arbitrary L2 material-momentum directions: cubic label products require additional control. Those qualifications matter for applying the earlier relative-energy argument.

## 7. The additional canonical bulk residual is explicit

For a fixed reference canonical field (phi,Pi), compare two reconstructed metrics in the same physical chart. With delta s=s1-s0,

    delta phi_dot = delta s P,
    delta Pi_dot = partial_R(R^2 delta s H),
    partial_R(delta phi_dot) = delta s_R P + delta s P_R,
    delta Pi_dot/R^2 = delta s_R H + delta s(H_R+2H/R).

On smooth pieces of the reference field, its wave-energy norm is therefore bounded by a reference H1 constant times ||delta s||infinity+||delta s_R||infinity. Also

    ||e(y1)-e(y0)||L1
      <= (||y1||L2+||y0||L2)||y1-y0||L2/2.

Combining these estimates yields locally Lipschitz gravitational feedback with no extra h^-1 or h^-1/2 loss in this BULK comparison term. Interfaces, source traction, changing material charts, and irregular reference fronts require their separate estimates; the displayed piecewise calculation does not hide distributional interface terms.

## 8. Precisely when the cancellation fails

In the same radial normalization, for general energy density rho and radial pressure pr,

    m_R = kappa R^2 rho,
    (log N)_R = m/(R^2 F) + kappa R pr/F,
    (log s)_R = 2m/(R^2 F) - kappa R(rho-pr)/F.

The massless radial scalar has rho=pr. The moving material sector contributes

    rho_source = q d/R^2,
    pr_source = F^2 p^2 d/(R^2 q),
    rho_source-pr_source = F S^2 d/(R^2 q),

which gives exactly A_g above. An additional stress sector contributes

    extra (log s)_R = -kappa R (rho_extra-pr_extra)/F.

Therefore positivity of extra energy alone is insufficient. For example a prescribed potential-like loading has rho_extra=V, pr_extra=-V, leaving -2kappa R V/F. At fixed integral R^2 V, a narrow positive bump makes this local contribution grow inversely with its width. This is an instantaneous constraint-loading counterexample, not a newly conserved matter theory or an identification of the MTS Gram with a potential.

The next MTS-specific calculation must vary the actual source-fitted moving Gram action with respect to lapse and radial metric, and determine rho_Gram-pr_Gram including source/measure dependence. It may vanish, admit its own estimate, or leave an additional term. It cannot be deleted by relabeling all positive energy as scalar wave energy.

## 9. Qualification and numerical honesty

Implementation:

- `scripts/annular_live_radial_response_20260918.py`
- `scripts/annular_live_radial_response_v2_20260918.py`
- `scripts/qualify_annular_live_radial_response_20260918.py`
- `scripts/qualify_annular_live_radial_response_v2_20260918.py`
- `scripts/qualify_annular_live_mass_hessian_20260918.py`
- `scripts/qualify_annular_live_stress_response_20260918.py`

Source-backed state is the hash-verified degree64 initial state in `source-intake/navier-stokes/20260914/annular-live-continuum-snapshot-attempt01/status.json`. The density adapter samples the existing scalar reconstruction, interpolates its square root by PCHIP, then squares it. It is a positive FROZEN canonical-density approximation, not an exact replacement of the original continuum data or a new time trajectory. It includes nonzero source momentum prepared at velocity .03.

The first radial-difference test failed: a wave adjoint mismatch of 1.50575e-7 exceeded the declared 2e-8 tolerance. That executed attempt is retained in `source-intake/navier-stokes/20260914/annular-live-radial-response-attempt01/status.json`. Its adaptive integrator did not split at the density-interpolation knots. The immutable second version explicitly makes those knots integration boundaries, with the same tolerance and unchanged equations/data. The wave adjoint mismatch becomes 4.73e-12; the largest of the five wave/density/momentum/rest-mass/translation adjoint errors is 3.96e-10.

`source-intake/navier-stokes/20260914/annular-live-radial-response-attempt02/status.json` completes 46 checks. Independent RK45 versus DOP853 mass/lapse/speed errors are below 1.9e-15 on this smooth segmented control. Full moving tangent-profile errors are below 6.9e-12. The combined second-mass difference differs by 4.52e-7. The frozen-density reconstructed lapse/root differ from the original snapshot by less than 2.0e-10. These are implementation controls, not rigorously rounded error certificates.

At added integrated wave density .002:

| Bump half-width | Peak added e | Max change in (log N)_R | Max change in s_R |
| --- | --- | --- | --- |
| .04 | .046875 | .00084130 | .0000094288 |
| .01 | .1875 | .00335247 | .0000095256 |
| .0025 | .75 | .01339711 | .0000095506 |
| .000625 | 3 | .05357568 | .0000095569 |

The derived s_R bound is .00010288447 for every row, not fitted to these measurements. The lapse gradient genuinely grows; the characteristic speed gradient does not inherit that direct density spike.

`source-intake/navier-stokes/20260914/annular-live-mass-hessian-attempt01/status.json` completes 11 checks. Field-only, momentum-only and mixed Hessians are .00291585934, 22.3483632944 and 22.3512699389 respectively. Gravitational binding contributions are retained and negative. Independent second differences agree within 2.41e-6 absolute against a predeclared 3e-5 absolute numerical control. This is not a high-relative-precision certification of the small field-only Hessian.

`source-intake/navier-stokes/20260914/annular-live-stress-response-attempt01/status.json` completes 12 checks. At the same integrated potential loading .002, narrowing the prescribed potential-like bump from .04 to .000625 increases the maximum wave-speed gradient change from .00166668 to .10706862 (about 64.24 times). The exact general-stress identity agrees within 2.1e-17. This deliberately fails the proposed extension to arbitrary positive stress; it is a successful negative control, not a failure of the scalar bound and not evidence against an uncomputed MTS stress.

Total current qualification: 69 successful implementation checks across the three completed suites. One new failed integration-control attempt is retained, making 31 retained failed attempts in the inherited integrity chain. The four old full-horizon flat-force failures remain failures. Final integrity evidence is `source-intake/navier-stokes/20260914/annular-live-radial-response-final-integrity.json`; its state must be complete before this checkpoint is treated as sealed. No numerical check is promoted into a physical pass.

## 10. What stays open and what to do next

The original action/data, old failed force gates and existing parent-claim flags are untouched. No full live force convergence, useful asymptotic grid threshold, time-integration certificate, black-hole regularity theorem, parent-owned numeric coupling, or full GR limit is claimed. The earlier flat reference/MTS argument and the older live P1/cut-cell implementation remain distinct from a yet-to-be-qualified live P2/source-fitted finite family.

Next concrete derivation: compute the live source-fitted Gram's lapse/radial-metric stress difference and its source shape derivative from that actual action. Carry its surviving terms, not a scalar-stress substitution, into the moving-source canonical residual. The fixed-position coercivity and scalar bulk metric bound above are now available ingredients; do not re-run the same flat grid comparison in their place.
