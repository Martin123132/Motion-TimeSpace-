# Reference-wave decoupling with the actual endpoint fluxes

Private derivation, 14 September 2026. No new field, fitted coefficient, source protocol or frozen metric is introduced.

## 1. Main conclusion — distinguish the three limits

A weaker estimate than uniform spatial H3 is sufficient. For the same stationary-source candidate, the nearest-neighbour reference equation gives

    E_G[q_0(t)] <= C_F h Q_ref(t),

where Q_ref is a derived higher-time-derivative energy and C_F is independent of the spacing h and source collar width h/2. The source is allowed to retain its sharp collar; it is not replaced by a flat boundary coefficient.

Q_ref has a spacing-independent differential bound and a finite, explicitly bounded initial value for the exact compact analytic preparation. Combined with the preceding live gravitational relative-energy estimate, this yields, on each fixed short interval below the previously derived comparison time and while the exact solutions exist,

    R_h(t) = O(h),
    E_0(Y_1-Y_0)(t) = O(h),
    E_G[Y_1(t)] = O(h).

The existing density-to-geometry bound then gives conservative mass/lapse differences O(sqrt(h)). This is slower than the smooth fourth-order target but **does tend to zero**, unlike a mere energy-conservation bound.

Be precise about what this proves:

- It is a short-time **relative decoupling estimate between the two existing finite-h branches** in the fixed stationary-source regular-annulus model.
- It does not identify the reference branch's h->0 limit with the complete Einstein equations, prove existence of that continuum limit, or cover other MTS sectors.
- The classical-solution/existence qualification remains. No global-in-time, horizon, moving-source, observational, physical-unit, or full-GR claim follows.
- The analytic time window is still t<0.0008345769328864052 in pilot units. The saved numerical interval 0.06 is longer. Numerical checks at 0.06 do not extend the proven window.

The constants are deliberately very conservative. The resulting asymptotic theorem is not a useful numerical error bar at the presently tested h; the distinction matters.

## 2. Inherited system and notation

All definitions and hypotheses of `DERIVATION-20260914-live-constrained-mass-relative-energy.md` remain in force: Y=(chi,pi), pi=Omega p; fixed source D=v=a=0, E=0.003; positive layer measure W; regular annulus; lower seed 0.8; physical-cut normalization at b=6 and full support B_h=6+h/4.

Write H=H_0 for the reference constrained mass, g=(N/U)(B_h), and J for the fixed canonical antisymmetric operator. The actual reference evolution is

    Y'=g J DH(Y).

Let

    V=Y', A=Y'', v=sqrt(E_0(V)), a=sqrt(E_0(A)),
    B=D^2H, C_3tensor=D^3H, C_4tensor=D^4H,
    T=(1/2)B[V,V].

Distinguish the third-derivative tensor C_3tensor from its scalar bound C_3. The inherited bounds are

    B[V,V]>=2mu E_0(V), |B[V,W]|<=C_2 sqrt(E_0(V)E_0(W)),
    |D^3H[V,V,W]|<=C_3 E_0(V)sqrt(E_0(W)),
    |T'|<=C_T T^(3/2),

with mu=0.11925180874784208, C_2=2.67993946982774, C_3=1.6539159684347136 and C_T=20.763310118477733.

## 3. A fourth derivative without a source-density supremum

Continue the radial density-variation argument of the predecessor. For H[e]=m(B_h)/kappa, the density fourth derivative satisfies

    |D^4H[d_1,d_2,d_3,d_4]| <= L_4 product ||d_i||_1,

    L_4 = 8kappa L_3/r
          +kappa^2 S(4L_3+3L_2^2)/(r^2 f^(3/2))
          +18kappa^3 S L_2/(r^3 f^(5/2))
          +15kappa^4 S/(r^4 f^(7/2)).

The terms correspond to the four density/third-mass pairings, the four 1+3 and three 2+2 mass partitions, the six 2+1+1 partitions, and the fourth derivative of sqrt(F), respectively. The latter contributes -15/(R^4 U^7). No derivative of sigma and no ||sigma||_infinity appears.

Since e(Y) is quadratic, the phase fourth-derivative bound is

    |D^4H[V_1,V_2,V_3,V_4]| <= C_4 product sqrt(E_0(V_i)),
    C_4=16 L_4 E_bar^2+48 L_3 E_bar+12 L_2
       =2.0921247295614114.

For the clock, differentiating the same fixed-source integral gives

    |D^2 log g[d_1,d_2]| <= L_g2 ||d_1||_1 ||d_2||_1,
    L_g2=kappa^2 S L_2/(r^2 f^(3/2))
          +3kappa^3 S/(r^3 f^(5/2)).

Hence, with gamma_1=2L_g sqrt(E_bar) and gamma_2=4L_g2 E_bar+2L_g,

    |Dlog g[V]|<=gamma_1 v,
    |D^2log g[V,V]|<=gamma_2 v^2.

Here gamma_1=0.11780542410110965, gamma_2=0.08164572839750167. These are phase-energy bounds, not a claim of spatially uniform high derivatives at the source.

## 4. Derive the higher energy rather than assume acceleration regularity

Set s=Dlog g[V] and t=D^2log g[V,V]+Dlog g[A]-s^2. Differentiating the actual equation twice gives

    A' = g J B A + g J C_3tensor[V,V] + 2s A + t V.

The naive energy (1/2)B[A,A] has a derivative containing g B[A,J C_3tensor[V,V]]. Estimating that vector field by an inverse-grid operator norm would lose the uniform bound.

Instead add the exact cancelling cross term:

    Q = (1/2)B[A,A] + C_3tensor[V,V,A] + Lambda T^2,
    Lambda = (C_3^2/(2mu)+1)/mu^2 =876.814094955144.

Young's inequality and T>=mu v^2 give

    Q >= (mu/2) a^2 + v^4.

Differentiate the cross term. Its C_3tensor[V,V,A'] contribution cancels g B[A,J C_3tensor[V,V]] by antisymmetry of J. The exact remaining identity is

    Q' = (5/2)C_3tensor[V,A,A] + C_4tensor[V,V,V,A]
         +2s C_3tensor[V,V,A] +t C_3tensor[V,V,V]
         +2s B[A,A] +t B[A,V] +2Lambda T T'.

Thus all derivatives are scalar energy-bounded tensors. The state-dependent clock terms remain; they are not silently set to zero.

With gamma_b=gamma_2+gamma_1^2 and beta=C_2/2, let

    P_a=(5/2)C_3+3gamma_1 C_2,
    P_cross=C_4+3gamma_1 C_3+gamma_b C_2,
    P_v=gamma_b C_3+2Lambda C_T beta^(5/2).

Using |t|<=gamma_b v^2+gamma_1 a,

    |Q'| <= P_a v a^2 +P_cross v^3 a +P_v v^5
           <= C_Q v Q,

    C_Q=2P_a/mu+P_cross(1/mu+1/2)+P_v
       =75789.78383782142.

Consequently, for I(t)=integral_0^t v(s)ds,

    Q(t)<=Q(0)exp(C_Q I(t)).

This constant is large, but has no h in it. It is a genuine local uniform acceleration-energy estimate once the analytic initial bound below and the predecessor's T estimate are used, not an assumed reference H3 bound.

## 5. Bound the initial acceleration independently of h

The exact initial analytic bump satisfies the predecessor's first/second derivative bounds and

    ||b'''||_infinity <=
       [8*6^6/e^5+48*5^5/e^4+60*4^4/e^3+24*3^3/e^2]/0.3^3
       =226470.28549972211.

For y=(R-5.5)/0.3 and u=1/(1-y^2), its dimensionless third derivative is

    b[-8y^3u^6+48y^3u^5-48y^3u^4+12yu^4-24yu^3].

The expression is checked symbolically; the bound follows termwise from u^n exp(1-u). Flatness extends it across the support boundary.

Initially the relevant stencil, including the extra differences required for A, lies away from the stationary source for h<=1/32. Write L=NU and C=R^2L. In this source-free region,

    (log L)_R=2m/(R^2F).

The initial density has the pointwise bound

    e_0 <= (3/2)R_max^2[(0.02||b'||)^2+0.004^2],

because W<=3/2, width=h/2, nearest-neighbour differences are O(h), and omega<=h. Thus m_R<=kappa e_0, with no inverse h. This bounds L_RR and C_RR as well as their first derivatives.

In particular, put L_1=2M_*/(r^2 f_actual) and

    L_2sp = L_1^2 +2(m_R)_max/(r^2 f_actual^2)
            +4M_*/(r^3 f_actual)+4M_*^2/(r^4 f_actual^2),
    C_1=2R_max+R_max^2 L_1,
    C_2sp=2+4R_max L_1+R_max^2 L_2sp.

The initial nearest-neighbour momentum rate and its continuous shifted-grid extension satisfy

    ||p'|| <= R_max^2(0.02||b''||)+C_1(0.02||b'||),
    ||partial_R p'|| <= R_max^2(0.02||b'''||)
                         +2C_1(0.02||b''||)+C_2sp(0.02||b'||).

This is a differentiated flux difference, not a 1/h operator-norm estimate. The initial free-end half-weight has zero incident data, so no interior-weight substitution occurs.

For time-dependent coefficients, the radial variation bounds give uniform initial L_t and

    |(L_t)_R| <= |L_t| L_1 +2||m_t||_infinity/(r^2 f_actual^2),
    ||m_t||_infinity<=2kappa sqrt(E_bar E_0(V)).

Using q=0.004 L b, derive

    q_t=0.004 L_t b + (L/R^2)p',
    p''=-Omega^-1[K q+K_t chi].

The bounds on q_RR, C_t, (C_t)_R and the displayed p' derivative control the gradient of q_t and the weighted L2 norm of p''. Explicit conservative substitution gives

    E_0(A(0)) <= 950260089.973602,
    Q(0) <= 157367997192.5084.

These extremely loose bounds use analytic initial data, not a fit or extrapolation of three numerical grids. The helper records every constant used. Finite polynomial layer approximations are tested separately and are not rigorous all-h interpolation enclosures.

Combining with the predecessor's Riccati comparison yields a finite h-independent Q bound on every fixed T<t_*=0.0008345769328864052, while the exact solutions exist. Its exponential can be enormous: retain it symbolically or logarithmically, rather than representing overflow as failure of the dynamics.

## 6. The physical boundary flux, not an invented smooth boundary

Work layer by layer. For the nearest-neighbour reference define edge coefficients

    c_i=(R_i^2 L_i+R_(i+1)^2 L_(i+1))/2 >0,
    F_i=c_i(chi_(i+1)-chi_i)/h.

The actual free-node equation is

    omega_i p_i'=F_i-F_(i-1), F_(-1)=0.

The left node uses omega_0=h/2. The right node is the fixed source; it is not included in this free sum. Therefore

    F_i=sum_(j=0)^i omega_j p_j',
    F_i'=sum_(j=0)^i omega_j p_j''.

Differentiating the flux, including c_i', gives exactly

    a_i := (q_(i+1)-q_i)/h
          =F_i'/c_i-(c_i'/c_i^2)F_i.

This includes the edge ending at the fixed source, where q_source=0. It does not require q or chi to remain compactly supported at positive times. Nor does it set the source reaction to zero.

For each layer, both the supremum and node-total-variation of F are bounded by
R_max sqrt(2E_0(V;z)); the analogous bounds for F' use E_0(A;z). This follows from the exact partial sums and Cauchy-Schwarz with sum omega_free<=1.

## 7. Use bounded total variation, allowing the shrinking collar

Let ell=partial_t log L. The actual radial identities imply

    partial_R log L=2m/(R^2F)-kappa sigma/(R U),
    partial_R ell=2m_t/(R^2F^2)-kappa sigma m_t/(R^2 U^3).

Fixed sigma is essential here. Only its L1 integral S is used. Both the coefficient's total variation and its time derivative's total variation are bounded, even though pointwise derivatives in the source collar can grow.

With r=4.9, R_max=6.1, length=R_max-r, choose

    c_*=r^2 w_*, c^*=R_max^2 G,
    V_c=c^*[2log(R_max/r)+2M_* length/(r^2 f)+kappa S/(r sqrt(f))].

Let

    ell_0=[2kappa/(rf)+2L_g]2sqrt(E_bar),
    ell_V=2kappa sqrt(E_bar)[2length/(r^2 f^2)+kappa S/(r^2 f^(3/2))],
    V_ct=c^* ell_V+ell_0 V_c.

Then

    c_*<=c_i<=c^*, TV(c_i)<=V_c,
    ||c_i'||<=c^* ell_0 v, TV(c_i')<=V_ct v.

Sampling/averaging at any fixed layer cannot increase the radial total variation. Thus

    ||1/c||<=1/c_*, TV(1/c)<=V_c/c_*^2,
    ||c'/c^2||<=c^*ell_0 v/c_*^2,
    TV(c'/c^2)<= [V_ct/c_*^2+2c^*ell_0 V_c/c_*^3]v.

Apply these bounds to the exact a_i in section 6. Taking the weighted layer L2 norm after the per-layer variation bound gives

    ||TV(a)||_L2(W dz) <= A_f a+B_f v^2,

    A_f=sqrt(2)R_max[1/c_*+V_c/c_*^2]
       =2.576244630375354,
    B_f=sqrt(2)R_max[
        c^*ell_0/c_*^2+V_ct/c_*^2+2c^*ell_0 V_c/c_*^3]
       =8.743432407736655.

No supremum over layer-dependent matter gradients is inserted. The global geometry bounds and integrated layer energies are sufficient.

## 8. The missing forcing now vanishes

The sourced Gram matrix bound is Q_Gram<=1/8. For any nodal q,

    E_G[q] <= R_max^2/(16h) integral W sum |Delta^3 q|^2 dz
             <=R_max^2/(4h) integral W sum |Delta^2 q|^2 dz.

Since Delta^2q=h Delta a and sum |Delta a|^2<=(TV a)^2,

    E_G[q_0] <= (R_max^2 h/4)(A_f a+B_f v^2)^2
              <= C_F h Q,

    C_F=(R_max^2/4)[A_f sqrt(2/mu)+B_f]^2
       =3462.879910571655.

This is the crucial h factor. It comes from the actual flux representation plus bounded variation, not an unsupported spatial H3 assumption or energy conservation alone.

For fixed T<t_* with common exact solutions,

    integral_0^T sqrt(E_G[q_0])dt
       <= sqrt(C_F h) integral_0^T sqrt(Q(t))dt
       =O(sqrt(h)).

The exact initial bump gives E_G(Y_initial)=O(h^4). Insert both results into the preceding live relative-energy inequality to obtain the O(h) relative-energy conclusion in section 1, and the O(sqrt(h)) conservative geometry bound.

The proof does not certify the stronger O(h^4) error or a sharp finite-h prediction. A synthetic positive-coefficient boundary-corner example in the verifier shows E_G proportional to h under bounded variation, so that stronger rate cannot be inferred from these hypotheses alone. That example is a bound-sharpness control, not a newly sourced MTS trajectory.

## 9. Validation and limits of the numerical evidence

Main replay uses existing trajectories at 33,65,129 nodes and t=0,0.03,0.06. No long production trajectories are repeated. It verifies:

- free-end cumulative flux, differentiated flux with actual changing metric, and all Gram/BV inequalities;
- coercivity of Q and the fourth/mixed mass-derivative bounds;
- the higher-energy rate inequality and the analytic initial bounds.

There are 108 main checks. Saved final values are:

| nodes | E_0(A) | Q | E_G[q_0] |
|---:|---:|---:|---:|
| 33 | 2980.06490 | 19124.47591 | 0.48963923 |
| 65 | 7842.46587 | 34024.57873 | 0.17645975 |
| 129 | 12066.18464 | 42174.61878 | 0.02810491 |

The fact that E_0(A) and Q rise on these grids does not establish divergence or a plateau; the uniform estimate is analytic and much looser. Maximum main flux and differentiated-flux residuals are approximately 6.76e-12 and 1.09e-11.

Independent verification uses a separately implemented radial cubic-variation solver to check fourth derivatives by real centred differences, plus fresh very short forward/backward trajectories to differentiate Q. These small derivative probes are not a long-time rerun or a new physical prediction.

One attempted verifier failed a real quadrature gate: the 32/48-node estimates of the total-variation norm differed by 5.7956e-7 against a 1e-7 tolerance. The absolute values introduce interior corners. The failed attempt and executed code are preserved. The replacement splits the layer integral at the real roots of the exact polynomial second differences, then uses 12/16-point quadrature on each smooth segment, retaining the tolerance. It does not weaken the physics gate or relabel the failed attempt as passed.

A manufactured endpoint excitation checks that replacing the left half-weight by an interior weight causes a resolved wrong answer. It is labelled separately from the original compact preparation. An exact rational Hamiltonian control with a deliberately changing multiplier checks the higher-energy clock terms outside the nearly clock-stationary saved pulse.

All 32 replacement-verifier checks and all 5 exact-algebra checks pass. The independent fourth mass derivatives agree within 4.623e-9; fresh short-trajectory differentiation of Q agrees within 2.058e-5. Root-split 12/16-point variation norms agree within 1.777e-15 for the represented polynomials, whereas the unresolved coarse 32/48 differences reach 2.242e-5. The BV boundary-corner control has successive energy orders 0.96549, 0.98283 and 0.99143, approaching one rather than four. The generic changing-clock control has exact rational identity residual zero and dropping its clock terms changes the rate by about 0.01700. These figures measure checks of algebra and numerical methods, not physical accuracy.

The analysis addresses the underlying finite-h continuous-layer system. Polynomial discretizations, floating-point differentiation, root finding and numerical quadrature are consistency tests, not interval-certified proofs or theorem-assistant verification.

## 10. Best next step

The earlier specific obstruction — deriving a vanishing reference forcing rather than assuming it — now has a short-time route including both endpoints.

Next, identify and control the **nearest-neighbour reference continuum problem** with its actual source-collar matching, and improve or continue the excessively conservative time/constant bounds. Relative agreement between two regulated branches must not be renamed “full GR recovered.” In particular, track the finite source reservoir and internal clock through the limit instead of deleting them.

No moving-source, horizon, global existence, full GR/Newton, or observational-pass flag is promoted. No GitHub action; the protected workbench remains untouched.

## 11. Sources and reproduction

- Predecessor: `DERIVATION-20260914-live-constrained-mass-relative-energy.md`.
- Underlying source-compatible evolution: `scripts/annular_compatible_h_evolution_20260914.py`.
- Actual geometry and endpoint dynamics: `scripts/annular_horizontal_clock_evolution_20260913.py`.
- Gram norm: `scripts/annular_gram_smooth_limit_20260914.py`.
- New proof constants, bivariate radial derivatives, and flux reconstruction: `scripts/annular_reference_wave_decoupling_20260914.py`.
- Main replay: `scripts/derive_annular_reference_wave_decoupling_20260914.py`.
- Preserved first verifier: `scripts/verify_annular_reference_wave_decoupling_20260914.py`.
- Root-split verifier: `scripts/verify_annular_reference_wave_decoupling_v2_20260914.py`.
- Root-split integration: `scripts/annular_reference_wave_quadrature_20260914.py`.
- Independent cubic radial equations: `scripts/verify_annular_constrained_mass_relative_energy_20260914.py`.
- Exact clock/algebra control: `scripts/check_annular_higher_energy_algebra_20260914.py`.
- Main evidence: `source-intake/navier-stokes/20260914/annular-reference-wave-decoupling-attempt01/status.json`.
- Preserved failed verifier: `source-intake/navier-stokes/20260914/annular-reference-wave-decoupling-independent-attempt01/status.json`.
- Replacement verifier: `source-intake/navier-stokes/20260914/annular-reference-wave-decoupling-independent-attempt02/status.json`.
- Exact algebra evidence: `source-intake/navier-stokes/20260914/annular-higher-energy-exact-algebra-attempt01/status.json`.

The final integrity seal, not a running status or this narrative alone, is the completion authority. Executed code and prior evidence are immutable. All calculations are local, single-core and below normal priority; no subagents are used.
