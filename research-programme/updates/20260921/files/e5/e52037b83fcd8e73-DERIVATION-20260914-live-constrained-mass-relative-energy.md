# Live constrained-mass relative energy: gravity feedback without inverse-grid constants

Private derivation, 14 September 2026. This replaces neither the parent action nor any sealed calculation. It constructs a comparison functional from the radial constraint already being evolved.

## 1. Result and scope

For the stationary-source, regular-annulus candidate of the preceding checkpoint, the **live gravitational error terms can be controlled together**. The useful energy is a Bregman remainder of the full-support constrained mass, not the earlier purely quadratic error energy.

The resulting estimate has constants independent of the spacing h and collar width h/2. It uses the actual state-dependent lapse and the normalization at the internal physical cut R=6. No metric is frozen; no extra MTS smoothness axiom is inserted.

There are two different conclusions:

1. A **conditional live relative-energy estimate** reduces convergence to regularity/consistency of the nearest-neighbour reference solution.
2. An explicit, very conservative **uniform short-time stability bound**, while the solutions exist, follows for the compact initial preparation. Its reference-tangent comparison time is approximately 0.00083458 in pilot time, NOT seconds. This does not cover the full previous numerical interval 0.06.

This is **not** a full GR/Newton limit, a continuum existence theorem, a moving-source result, a horizon theorem, or an observational claim. In particular, a spacing-independent bound is not the same as a bound that tends to zero with spacing.

## 2. Fixed source leaf and notation

Use the previous annulus, canonical scalar data, factor matrices, positive node/layer weights and outer clock. The source obeys D=v=a=0, E=0.003. Its clock still advances and its reaction still enforces the fixed scalar endpoint, but it supplies no work. Variations here hold that reservoir and source preparation fixed. The irrelevant clock coordinates are not varied in the reduced scalar phase space.

Let Y=(chi,pi), pi=Omega p, with the fixed right-end scalar/momentum omitted. Integrals over z include the normalized nonnegative W(z). The constant symplectic operator J includes the canonical node/layer pairing; it is not the spacing-dependent stiffness matrix.

Let e_0(Y;R) be the nonnegative nearest-neighbour quadratic density and e_G(Y;R) the extra Gram density, both including their collar pushforward to radius. Define

    E_0(Y) = integral e_0(Y;R) dR,
    E_G(Y) = integral e_G(Y;R) dR,
    e_1(Y) = e_0(Y)+e_G(Y).

The Gram energy of a phase direction V uses only its scalar component. For the reference tangent V=Y_0', this is E_G[q_0], where q_0 is the actual reference scalar velocity.

Write a_h and B_h for the lower and upper full-support edges. B_h=6+h/4; the clock normalization is at b=6, not at B_h. Extend zero densities through any needed vacuum intervals when using common bounds r=4.9 and R<=6.1.

## 3. Constrained mass owns the Hamiltonian gradient

For a general nonnegative density e and the fixed source sigma,

    m_R = kappa[(1-2m/R)e + sqrt(1-2m/R) sigma],
    (log N)_R = m/(R^2 F)+kappa e/R,
    F=1-2m/R, U=sqrt(F), m(a_h)=0.8,
    (N/U)(b)=1, integral sigma dR=S=0.003.

Define H[e]=m(B_h)/kappa. The fixed seed contributes only a constant. A signed density variation d produces u=delta m satisfying

    u_R + a_e u = kappa F d,
    a_e = kappa[2e/R + sigma/(R U)], u(a_h)=0.

Consequently

    DH[e] d = integral w_e(R) d(R) dR,
    w_e(R) = F(R) exp[-integral_R^B_h a_e(s) ds].

Subtracting the radial equations gives

    (log(N/U))_R=a_e,
    (log(NU))_R=2m/(R^2 F)-kappa sigma/(R U).

In particular, the bulk density cancels from the second equation. Defining

    g[e]=(N/U)(B_h)=exp[integral_b^B_h a_e dR],

we obtain the exact identity

    w_e=NU/g[e].

Therefore H_j(Y)=H[e_j(Y)] generates the actual phase flow as

    Y_j' = g_j J DH_j(Y_j).

This is conformally Hamiltonian in the prescribed physical-cut time, not a claim that g_j=1. It implies H_j'=0. It also explains why the full-support mass, rather than the mass at b, is the correct functional. Source potential energy can extend beyond b.

## 4. Density derivative bounds, including the thin source collar

Assume 0<F<=1, F>=f>0, R>=r, sigma>=0, integral sigma=S, e>=0. All connecting densities below will meet these conditions. Norms of density directions are L1 in physical radius.

The damped first variation gives

    ||u||_infinity <= kappa ||d||_1.

For two directions d_1,d_2, the mixed second mass variation obeys

    v_R+a_e v
      = -(2kappa/R)(u_1 d_2+u_2 d_1)
        -kappa sigma u_1 u_2/(R^2 U^3).

Thus the second derivative of H is bounded by

    |D^2 H[d_1,d_2]| <= L_2 ||d_1||_1 ||d_2||_1,
    L_2 = 4kappa/r + kappa^2 S/(r^2 f^(3/2)).

Differentiating again, the three mixed terms of each type yield

    |D^3 H[d_1,d_2,d_3]| <= L_3 product_i ||d_i||_1,
    L_3 = 6kappa L_2/r
          +3kappa^2 S L_2/(r^2 f^(3/2))
          +3kappa^3 S/(r^3 f^(5/2)).

No supremum norm or derivative of sigma occurs. In particular, sigma=O(1/h) inside its shrinking collar does not introduce a 1/h constant here.

For the clock factor,

    D log g[d] = kappa integral_b^B_h
                   [2d/R + sigma u/(R^2 U^3)] dR,
    |D log g[d]| <= L_g ||d||_1,
    L_g=2kappa/r+kappa^2 S/(r^2 f^(3/2)).

If integral e<=E_bar, set

    A_bar=kappa[2E_bar/r+S/(r sqrt(f))],
    w_*=f exp(-A_bar), G=exp(A_bar).

Then w_*<=w_e<=1 and 1<=g<=G. These bounds also cover signed variations along nonnegative connecting density paths.

## 5. Coercivity is checked, not postulated

The predecessor's positive-energy/mass argument supplies, while exact solutions exist and mass is conserved,

    M_* = 0.9292469107643997,
    f_actual = 0.6207155466267756,
    E_bar=(M_*-0.8)/(kappa f_actual)=2.08222448216064.

Every density connection needed here has integral <=E_bar. This includes e_0(Y_s) for Y_s=(1-s)Y_0+sY_1, the path e_0(Y_1)+s e_G(Y_1), and the straight connection between the total endpoint densities. Quadratic positivity bounds the first path pointwise by the convex endpoint mixture.

For these paths, m<=0.8+kappa(E_bar+S), so

    F>=0.5883581844016066 > f=0.5.

Thus the convenient common f=0.5 is justified for connecting states, not just for the observed endpoints.

Quadratic densities give

    ||De_0(Y)[V]||_1 <= 2 sqrt(E_0(Y) E_0(V)),
    ||D^2e_0[V,W]||_1 <= 2 sqrt(E_0(V) E_0(W)).

It follows that

    D^2 H_0(Y)[V,V] >= 2mu E_0(V),
    mu = w_*-2 L_2 E_bar = 0.11925180874784208 >0.

Also define

    C_2=2+4 L_2 E_bar,
    C_3=8 L_3 E_bar^(3/2)+12 L_2 sqrt(E_bar).

Then

    |D^2 H_0[V,W]| <= C_2 sqrt(E_0(V)E_0(W)),
    |D^3 H_0[V,V,W]| <= C_3 E_0(V) sqrt(E_0(W)).

The cubic bound follows from the density chain rule: one D^3H term and three D^2H terms. Its coefficients are 8 and 12, respectively.

Define the new modulated mass

    R = H_1(Y_1)-H_0(Y_0)-DH_0(Y_0)[delta Y],
    delta Y=Y_1-Y_0.

Taylor's formula for H_0 and positive density interpolation for the extra term imply

    mu E_0(delta Y)+w_* E_G(Y_1)
       <= R
       <= (1+2L_2 E_bar)E_0(delta Y)+E_G(Y_1).

Hence R controls the trajectory error AND the extra Gram energy, with genuine uniform positive constants.

## 6. Exact live relative balance and uniform bound

Put V=Y_0' and rho=g_1/g_0. Conservation of both constrained masses and antisymmetry of J give

    R' = rho [DH_1(Y_1)-DH_0(Y_0)][V]
         -D^2H_0(Y_0)[V,delta Y].

No derivative of the MTS metric has been dropped. Decompose this identity into

    R' = rho(T+P)+(rho-1) D^2H_0(Y_0)[V,delta Y],

where

    T = [DH_0(Y_1)-DH_0(Y_0)-D^2H_0(Y_0)delta Y][V],
    P = [DH_1(Y_1)-DH_0(Y_1)][V].

The reference Taylor remainder satisfies

    |T| <= (C_3/2) E_0(delta Y) sqrt(E_0(V)).

For P, vary the density weight from e_0(Y_1) to e_1(Y_1) and retain the explicit Gram derivative:

    |P| <= 2L_2 sqrt(E_bar E_0(V)) E_G(Y_1)
           +2 sqrt(E_G(Y_1) E_G(V)).

Finally,

    |rho-1| <= G L_g [E_G(Y_1)+2sqrt(E_bar E_0(delta Y))].

Use E_0(delta Y)<=4E_bar in the clock term. Define

    A_delta = G[C_3/2+2L_g C_2 sqrt(E_bar)],
    A_G     = G[2L_2 sqrt(E_bar)+2L_g C_2 sqrt(E_bar)],
    C       = max(A_delta/mu,A_G/w_*),
    D       = G/sqrt(w_*).

Then the actual evolving system satisfies

    |R'| <= C sqrt(E_0(V)) R
            +2D sqrt(R) sqrt(E_G(V)).

For this preparation,

    w_*=0.45922154366171203, G=1.0887990925101885,
    C=10.432859744122617, D=1.6067067682852492.

With I(t)=integral_0^t sqrt(E_0(V(s))) ds, the regularized square-root comparison gives

    sqrt(R(t)) <= exp(C I(t)/2) [
        sqrt(R(0))
        +D integral_0^t exp(-C I(s)/2) sqrt(E_G(V(s))) ds ].

This is the desired live bound: no assumed uniform MTS eta, no separate MTS H3 theorem, no inverse-grid operator norm, and no frozen clock.

For matched initial scalar data, R(0)<=E_G(Y_initial). Therefore uniform bounded I(t), together with integral sqrt(E_G[q_0])=O(h^2) and initial E_G=O(h^4), would yield

    R=O(h^4), E_0(delta Y)=O(h^4), E_G(Y_1)=O(h^4).

The predecessor's actual-trajectory density-to-geometry inequality would then give a conservative O(h^2) mass/lapse difference, not automatically O(h^4).

## 7. Reference tangent control: an actual local derivation

The I(t) hypothesis is not left wholly as an unsupported input. On the reference branch define

    T_ref = (1/2) D^2H_0(Y_0)[V,V], V=Y_0'.

Differentiating Y_0'=g_0 J DH_0 and cancelling the antisymmetric Hessian pairing gives exactly

    T_ref' = (1/2)D^3H_0[V,V,V]
             +2 Dlog g_0[V] T_ref.

Since mu E_0(V)<=T_ref, we obtain

    |T_ref'| <= C_T T_ref^(3/2),
    C_T = C_3/(2mu^(3/2))+4 L_g sqrt(E_bar/mu)
        =20.763310118477733.

Consequently

    sqrt(T_ref(t)) <= sqrt(T_ref(0)) /
                    [1-C_T sqrt(T_ref(0)) t/2]

until the denominator vanishes, conditional on solution existence in the stated leaf/chart.

### Uniform initial bound, not a three-grid extrapolation

For b(R)=exp(1-1/(1-y^2)), y=(R-5.5)/0.3, inside its support and zero elsewhere,

    |b'| <= 8/(0.3 e),
    |b''| <= [1024/e^3+216/e^2+8/e]/0.3^2.

These follow by bounding s^n exp(1-s) for s=1/(1-y^2)>=1; endpoint flatness extends the bounds globally. With chi=0.02b and p=0.004R^2b, the reference velocity is q=0.004 NU b.

The support and its initial incident nearest-neighbour stencil stay away from the source collar and endpoints for every h<=1/32. There sigma=0 and the exact cancellation in section 3 gives

    |(NU)_R| <= 2M_*/(r^2 f_actual).

Also N<=1 in this inner region and U<=1. Writing L=NU, C_R=d(R^2 L)/dR, we may use

    |q_R| <= 0.004 [8/(0.3e)+2M_*/(r^2 f_actual)],
    |C_R| <= 2R_max+R_max^2 [2M_*/(r^2 f_actual)],
    |p_i'| <= R_max^2 (0.02 ||b''||_infinity)
              +||C_R||_infinity (0.02 ||b'||_infinity).

The latter is the nearest-neighbour divergence difference, using interior omega=h. The half-weight endpoint is initially identically silent because the preparation and its incident stencil vanish there; it is not silently assigned interior weight. This initial-bound proof uses the exact analytic layer preparation. Finite-degree interpolation is its numerical approximation; checking the saved initial energies against this coarse bound is not a rigorous interpolation enclosure for every future grid.

Summing the positive weights yields the explicit coarse bounds

    E_0(V(0)) <= 9941.20585498272,
    T_ref(0) <= 13320.914974225407,
    t_* = 2/[C_T sqrt(13320.914974225407)]
        =0.0008345769328864052.

Thus I(t) has a derived h-independent bound on every t<t_*. This is a coarse comparison lifespan, NOT an estimated breakdown time. The actual saved reference tangent energies are around 4.4--6.2, vastly below that worst-case initial bound. Neither these samples nor this Riccati estimate prove a uniform theorem to t=0.06.

For arbitrary phase directions, the already sourced Gram factor norm and third/first-difference relation also imply

    E_G(V) <= (2 R_max^2/r^2) E_0(V).

Combining this with the tangent estimate proves spacing-uniform short-time stability while solutions exist. It does **not** prove consistency as h tends to zero: this last inequality does not force E_G(V) to vanish.

## 8. Numerical replay and independent differentiation

The exact algebra concerns the underlying finite-h, continuous-layer system. The saved trajectories use polynomial layer/radial approximations to that system; floating-point agreement is a consistency test, not a certified continuum proof or a formal theorem-assistant proof.

Main replay: nine saved count/time pairs (33,65,129 at 0,0.03,0.06), 93 checks. It checks the full-support mass gradient, strict modulated coercivity, the exact live rate, nonlinear remainder and Gram feedback bounds, the complete rate inequality, and the initial/reference tangent estimates.

The final modulated masses are

| nodes | R(0.06) |
|---:|---:|
| 33 | 4.2970318730441056e-4 |
| 65 | 9.894016652380105e-5 |
| 129 | 7.672565013603889e-6 |

Maximum main live-rate replay discrepancy: 1.462e-16. Omitting the factor 1/g from the mass gradient gives a resolved discrepancy up to about 2.5281e-6. The physical-cut versus full-support normalization is therefore genuinely retained, not numerically irrelevant by assertion.

Independent verification solves the radial first, second and third mass-variation ODEs with a different adaptive integrator. For a straight phase direction, let d=De[V] and e_V=e(V). Its equations are

    u'+a_e u = kappa F d,
    v'+a_e v = 2kappa F e_V
                -4kappa u d/R-kappa sigma u^2/(R^2 U^3),
    z'+a_e z = -6kappa(v d+2u e_V)/R
                -3kappa sigma u v/(R^2 U^3)
                -3kappa sigma u^3/(R^3 U^5).

They are compared with complex-step Hessians and real centred differences. The derivative of log g is integrated only from b to B_h. A separate accelerated tangent perturbation checks the live T_ref identity; layer quadrature is also refined. All 30 independent checks pass. Maximum first/second radial derivative discrepancies are 2.967e-14 and 4.539e-12; the third derivative agrees with centred differences within 4.569e-10, and the live tangent-energy rate within 2.285e-10. These are numerical differentiation errors, not observational precision. Final authority is the independent status plus the final integrity file, not this prose alone.

## 9. What this closes, and the best next calculation

**Closed at the stated analytic level:** the live gravity terms are no longer an unsigned requirement to bound an MTS metric derivative. Constrained mass coercivity and its third derivative give an explicit uniform relative-energy inequality. A nonzero uniform short-time reference tangent interval is also derived.

**Not closed:** the vanishing reference forcing integral sqrt(E_G[q_0]) at the actual boundaries. Merely citing energy conservation would repeat the previously disproved inference that bounded energy removes oscillatory Gram energy.

The next calculation should exploit the nearest-neighbour reference equation to derive sufficient spatial/time regularity of q_0, including the free-end and stationary-source conditions, or establish a weaker vanishing-consistency estimate. It should also sharpen/continue reference tangent control toward the tested interval. Do not return to the discarded need for a separate arbitrary MTS C3 coefficient bound; this functional bypasses it.

No full-GR, local-GR, horizon, physical-unit, or observational-pass flag is promoted. No files in the protected original workbench are edited. No GitHub action, new parameters, external claims or subagents are involved.

## 10. Sources and reproducibility

- Predecessor derivation: `DERIVATION-20260914-boundary-compatible-h-evolution.md`.
- Prior Gram and radial geometry bounds: `DERIVATION-20260914-Gram-bound-to-radial-geometry.md`.
- Original live geometry/clock equations: `scripts/annular_horizontal_clock_evolution_20260913.py`.
- Existing factor ownership: `scripts/annular_covariant_scalar_action_20260912.py` and `scripts/annular_gram_joint_action_20260909.py`.
- Matching evolving preparation: `scripts/annular_compatible_h_evolution_20260914.py`.
- New mathematical helper: `scripts/annular_constrained_mass_relative_energy_20260914.py`.
- Main replay: `scripts/derive_annular_constrained_mass_relative_energy_20260914.py`.
- Independent radial derivative replay: `scripts/verify_annular_constrained_mass_relative_energy_20260914.py`.
- Main evidence: `source-intake/navier-stokes/20260914/annular-constrained-mass-relative-energy-attempt01/status.json`.
- Independent evidence: `source-intake/navier-stokes/20260914/annular-constrained-mass-relative-energy-independent-attempt01/status.json`.
- Predecessor seal: `source-intake/navier-stokes/20260914/annular-compatible-h-evolution-final-integrity.json`.

All numerical jobs use one low-priority single-core worker, no fresh long trajectories. Executed scripts and previous evidence remain immutable. The mutable resume records safe continuation.
