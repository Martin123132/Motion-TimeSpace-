# Mesh-uniform canonical coefficient and boundary-source bounds

Date: 2026-09-09. Private local continuation. No new evolution, public upload,
boundary adjustment, physical residual subtraction, or changed action.

## 1. What has actually advanced

The preceding energy construction left alpha_A and alpha_L as finite-matrix
spectral quantities. Stable values on three grids did not bound a refinement
family. Here both are bounded analytically by **metric coefficient envelopes,
not matrix condition numbers or inverse powers of the mesh spacing**.

The difficult step is alpha_L: compare the actual quadrature-plus-Gram elliptic
solve with a continuous one-dimensional elliptic problem. Its interpolation
and consistency error supplies the factor h that cancels the inverse estimate.
The Gram term is included, not silently dropped in this comparison.

The same full operator bound controls the boundary-adapted source. Thus there
is a conditional, mesh-uniform canonical energy estimate. It is conditional
on positive metric bounds and bounded metric jets over the time interval.
Those hypotheses are NOT yet consequences of the full coupled MTS equations.
The nonlinear P(X) closure, full shift/DAE closure, and horizon remain open.

## 2. Exact scope and source owners

Previous energy identity and unchanged affine lift:
`DERIVATION-20260909-first-derivative-graph-energy-and-boundary-forcing.md`.

Action matrices and energy rate definitions:
`scripts/annular_first_derivative_energy_20260909.py`.
Adapted source and saved numerical metric accelerations:
`scripts/annular_boundary_adapted_energy_20260909.py`.
Actual released C1 cubic Hermite space and positive composite Gauss4 rule:
`scripts/annular_adm_mixed_action_20260909.py`.
Actual finite Gram template:
`scripts/annular_gram_joint_action_20260909.py` and
`scripts/sbp4_compatible_second_operator_20260909.py`.

New constructive constants and coefficient/boundary formulas:
`scripts/annular_uniform_energy_bounds_20260909.py`.
Reproducible runner:
`scripts/derive_annular_uniform_energy_bounds_20260909.py`.
Results:
`source-intake/navier-stokes/20260909/annular-uniform-energy-bounds-derived/status.json`.
Final integrity:
`source-intake/navier-stokes/20260909/annular-uniform-energy-bounds-final-integrity.json`.

General methodological background: [Patrick Farrell, Finite Element Methods
for PDEs, sections 7.5 and 11.4](https://people.maths.ox.ac.uk/farrellp/femvideos/notes.pdf),
checked 2026-09-09, explains the roles of interpolation and elliptic regularity
in finite-element error estimates. The explicit one-dimensional estimates,
quadrature treatment, and MTS Gram constants below are derived here; that
reference does not prove this particular MTS bound. An alternative Oxford
notes URL returned 403; recorded in the result, not used as evidence.

The theorem here covers b2=b3=m_chi=Lambda=0, on a fixed annulus [a,b] with
0<a<b, length ell=b-a, uniform scalar spacing h, and at least 17 scalar nodes.
Mass faces may have the existing nonuniform boundary spacing. All scalar
slopes are dynamical/free; only scalar endpoint values are prescribed.
After lifting them, the scalar space V_h has zero endpoint values.
No claim is made at F=0, lapse collapse, or for the nonlinear fixture.

## 3. Coefficients, quadrature, and basic assumptions

Write Q for the actual positive composite Gauss4 quadrature and set

    F=1-2mu/R, c=N sqrt(F), m=R^2/c, p=R^2 c,
    theta=c_t/c=N_t/N-mu_t/(R F).

Then m_t=-m theta and p_t=p theta. Assume over the annulus

    0<m_-<=m<=m_+, 0<p_-<=p<=p_+,
    ||p_R||_infty<=L_p, theta_-<=theta<=theta_+,
    ||theta_R||_infty<=L_theta.

p and theta are continuous, piecewise W^(1,infty); jumps in their spatial
derivatives are allowed. These are envelopes of the reconstructed metric,
not assumed smooth nodal interpolants with their kinks erased.

On V_h the exact discrete bilinear forms are

    M(v,w)=Q[m v w],
    K(v,w)=Q[p v_R w_R]+G_h(v,w),
    K_t(v,w)=Q[p theta v_R w_R]+G_{h,t}(v,w).

For GR, G_h=0. For the candidate it is the positive Gram term already in the
action, with nodal coefficient p and rate p theta. Q integrates unweighted
products of cubic polynomials exactly on every scalar cell, even when split
by mass faces. Weighted products are NOT assumed exactly integrated.

Let theta_0=(theta_++theta_-)/2, delta=(theta_+-theta_-)/2, and
Theta=max(abs(theta_-),abs(theta_+)). Splitting off theta_0 avoids penalizing
a spatially constant time rescaling with artificial coefficient ratios.

## 4. Universal local estimates, with exact certificates

For any cubic on a scalar cell,

    ||v_R|| <= (16/h)||v||.

On the unit cell define the right-endpoint reconstruction

    R_right v = v(1)(3x^2-2x^3)+v'(1)(x^3-x^2).

Its L2 norm is <=2||v|| and its derivative norm is <=13||v||.
The runner proves these three constants by exact rational Sylvester minors
of 256 H-D, 4 H-R^T H R, and 169 H-R^T D R, where H is the monomial L2
Gram matrix and D the derivative Gram matrix. No sampled eigenvalue is used
to select the constants.

For u in H2 in one dimension, ordinary nodal cubic Hermite interpolation
satisfies ||(I_h u-u)_R||<=2h||u_RR||. Subtract the affine Taylor polynomial
at each left endpoint. The remaining endpoint value is bounded by
h^(3/2)||u_RR||/sqrt(3), its endpoint derivative by sqrt(h)||u_RR||,
and its derivative in the cell by h||u_RR||. The two right Hermite basis
derivative norms are sqrt(6/5) and sqrt(2/15). Consequently the interpolation
constant is at most 1+sqrt(2/5)+sqrt(2/15)<2. The final strict inequality has
the exact squared margin 1/225. This requires H2, NOT a uniform third derivative.

The elementary endpoint Poincare bound ||v||<=ell||v_R|| is sufficient here.
We deliberately use loose constants rather than optimize a spectral fit.

## 5. Gram bounds valid for every allowed grid

Let D3 be the unscaled nodal third difference. The template has
T^T T=D3^T R_template D3. Its four distinct row types are the three left
boundary types and the interior; the right boundary is their reflection.
Exact source rationals give positive diagonal-dominance margins and

    ||R_template||_2 <= max(row absolute sums) < 1/8.

The boundary closures are disjoint for n>=17, so this is not an inference
from checking a finite list of sizes. Convex sampling of positive p gives

    G_h(v,v) <= (p_+/(8h)) ||D3 v_nodes||^2.

Factor D3 as a second difference of the first difference. The second-
difference convolution has l1 norm 4. Also
sum |v_{j+1}-v_j|^2 <= h||v_R||^2. Therefore

    G_h(v,v) <= G ||v_R||^2,  G=2p_+  (candidate), G=0 (GR).

For an H2 function, the second nodal difference is its second derivative
paired with a triangular kernel of squared norm 2h^3/3. Those kernels
overlap at most twice; taking one further difference costs at most 2 in
l2 norm. Thus

    ||D3 u_nodes||^2 <= (16/3)h^3||u_RR||^2,
    G_h(I_hu,I_hu) <= (G/3)h^2||u_RR||^2,
    |G_h(v,I_hu)| <= (G/sqrt(3))h||v_R|| ||u_RR||.

The same absolute estimates apply to G_{h,t}-theta_0 G_h with the additional
factor delta: each coefficient is p(theta-theta_0). Convex sampling ensures
this coefficient bound even though a sampled ratio need not equal theta
at the sampling center. Third differences of any affine lift vanish exactly.

It follows that p_-||v_R||^2<=K(v,v)<=(p_++G)||v_R||^2.

## 6. alpha_A: constructive weighted mass projection

Let Pi_m denote projection onto V_h in the discrete Q[m . .] inner product.
Then M^-1 M_t w=-Pi_m(theta w) exactly, including quadrature.
For a multiplier eta=theta-theta_0 define J_h(eta w) by nodal values
eta_j w_j and nodal derivatives eta_j w'_j, deliberately without eta'_j w_j.
This is a valid C1 cubic field, and its endpoint values remain zero.
On a cell,

    J_h(eta w)=eta_left w+(eta_right-eta_left)R_right(w).

Consequently

    ||J_h(eta w)-eta w||_Q <= 3h L_theta ||w||,
    ||[J_h(eta w)]_R|| <= delta||w_R||+13 L_theta||w||.

Projection contractivity and the inverse estimate give

    ||[Pi_m(eta w)-J_h(eta w)]_R||
        <=48 sqrt(m_+/m_-) L_theta ||w||.

The argument uses exact quadrature norms only for polynomials; eta w itself
is controlled pointwise at the positive quadrature nodes. It does not
replace the actual mass matrix by an exactly integrated alternative.

Set C_J=13+48 sqrt(m_+/m_-). Then

    alpha_A <= B_A
      =abs(theta_0)+sqrt((p_++G)/p_-)(delta+C_J ell L_theta).

This bounds the FULL K-operator norm of M^-1 M_t, hence also the symmetric
quadratic growth rate used in the energy identity.

## 7. alpha_L: elliptic comparison cancels the inverse-grid factor

Given a_h in V_h, let u_h=K^-1 M a_h. There exists a broken cellwise cubic
f_h such that (f_h,v)=Q[m a_h v] for all broken cubics, with
||f_h||<=m_+||a_h||. This is the cellwise unweighted L2 Riesz representative;
positivity and exactness of Q[v^2] prove the bound.

Solve the AUXILIARY continuous Dirichlet equation

    -(p U_R)_R=f_h,  U(a)=U(b)=0.

This is an estimate device, not a replacement physical field equation.
Positive Lipschitz p gives, directly by testing with U and differentiating
the flux,

    ||U_R||<=C1||f_h||, C1=ell/p_-,
    ||U_RR||<=C2||f_h||, C2=(1+L_p C1)/p_-.

In particular U is H2 despite coefficient-derivative kinks. Set

    C_I=C1+2ell C2,
    C_cons=2p_+ C2+2L_p C_I+(G/sqrt(3))C2,
    C_e=C_cons/p_-.

To see the quadrature term: subtract any cellwise constant from p in
Q[p v_R (I_hU)_R]-integral[p v_R (I_hU)_R]. Exactness cancels that constant;
the remainder is <=2h L_p||v_R|| ||(I_hU)_R||. Add the Hermite interpolation
error and the smooth Gram bound of section 5. Coercivity then gives

    ||(u_h-I_hU)_R||<=h C_e||f_h||.

Now replace theta by eta=theta-theta_0 and set

    L_r=L_p delta+p_+ L_theta,
    C_r=2p_+ delta C2+2L_r C_I+(delta G/sqrt(3))C2.

The continuous comparison has the exact integration-by-parts identity

    integral[p eta v_R U_R]
      =integral[v(eta f_h-p eta_R U_R)].

Thus its norm is bounded by (delta+p_+ L_theta C1)||v|| ||f_h||.
The interpolation/quadrature/Gram discrepancy contributes h C_r||v_R||||f_h||;
the u_h-I_hU error contributes h delta(p_++G)C_e||v_R||||f_h||.
Use ||v_R||<=16||v||/h ONLY here, after the factor h is present. Define

    C_L2=delta+p_+ L_theta C1+16[delta(p_++G)C_e+C_r],
    B_L=abs(theta_0)+(m_+/m_-)C_L2.

We have proved

    ||M^-1 K_t K^-1 M||_(M->M) <= B_L,
    alpha_L <= B_L.

Equivalently ||K_t K^-1 f||_(M^-1)<=B_L||f||_(M^-1), for an arbitrary
free covector f. This last statement is stronger than a bound on the
symmetric energy form and is needed for boundary-source control.

Finally alpha_M<=Theta and alpha_K<=Theta follow immediately from positive
mass/bulk/Gram weights. Therefore the old energy coefficient obeys

    C<=C_star=max(2B_A+Theta, 2B_L+Theta).

All constants are independent of h. If theta is spatially constant, delta
and L_theta vanish and all four bounds equal abs(theta), exactly. A frozen
metric gives zero rates. These limiting cases were independently tested.

## 8. Uniform boundary-source bound, with unchanged physical data

For the existing affine scalar-value lift l(R,t), whose endpoint histories
are quadratic in time, l_ttt=0. All norms here are continuous unweighted L2
norms of that affine function, hence exactly computable from endpoint data.
Define D_q=1+2*16=33 and T_theta>=||theta_t||_infty. Since

    m_tt/m=theta^2-theta_t,
    f_b=-[M_full l_tt+M_full,t l_t+K_full l]_free,
    f_b,t=-[2M_full,t l_tt+M_full,tt l_t+K_full,t l+K_full l_t]_free,

integration by parts plus the same quadrature cancellation yields

    F_b = [m_+(||l_tt||+Theta||l_t||)+D_q L_p||l_R||]/sqrt(m_-),
    F_bt = [2m_+Theta||l_tt||+m_+(Theta^2+T_theta)||l_t||
             +D_q{(L_p Theta+p_+L_theta)||l_R||+L_p||l_tR||}]/sqrt(m_-),
    ||f_b||_(M^-1)<=F_b, ||f_b,t||_(M^-1)<=F_bt,
    ||h_b||_(M^-1)<=H_b=B_L F_b+F_bt,
    h_b=K_t K^-1 f_b-f_b,t.

There is no Gram lift contribution: T l_nodes=0, including for l_t and
for differentiated Gram coefficients. There is also no new slope boundary
condition, fitted counterterm, or subtraction of a physical mass offset.
The large factor 33 is a conservative quadrature bound, not a new coupling.

## 9. The resulting conditional energy/commutator theorem

For the already-derived Ehat=(w^T K w+b^T M b)/2, b=M^-1(Ku-f_b),

    Ehat_t <= C_star Ehat+sqrt(2Ehat)(H_b+||M^-1g||_K).

For the exact canonical free scalar equation g=0; if a numerical Euler
residual is retained it stays in g. The nonlinear acceleration-dependent
P(X) correction cannot be declared bounded by invoking this canonical result.

Let Y=sqrt(2Ehat). With finite time-dependent coefficient/source envelopes,

    Y(t)<=exp(A(t))[Y(0)+integral_0^t exp(-A(s))(H_b(s)+G_source(s)) ds],
    A(t)=one_half integral_0^t C_star(s) ds,
    G_source=||M^-1g||_K.

This follows by regularization also at Ehat=0. For constant upper envelopes
it becomes Y<=exp(C_star t/2)Y0+2(H_b+G_source)(exp(C_star t/2)-1)/C_star,
with the usual linear limit when C_star=0.

Then ||q_R||<=Y/sqrt(p_-)+||l_tR||. Inserting this into the previous
H1-only scalar commutator estimate in
`DERIVATION-20260909-mass-trace-control-and-bulk-commutator-bound.md` supplies
the previously missing conditional uniform H1 bound, rather than assuming
a uniform third derivative. In particular its h^2 and h prefactors survive
for a family with uniform coefficient/time/source envelopes and initial Y.
This is not yet a proof that the coupled physical family has those envelopes.

## 10. How envelopes are obtained from the actual saved metric

For this canonical Lambda=0 case, mu, N, mu_t, N_t are their actual continuous
piecewise affine reconstructions. On each union cell, F=1-2mu/R is monotone,
and N_t/N and mu_t/(R-2mu) are linear-fractional functions with positive
denominators. Endpoint interval bounds therefore control them throughout
the cell. Their derivative numerators are constant within the cell.
This bounds theta and its Lipschitz seminorm without ignoring mass-face or
lapse-node kinks. Product envelopes give m_-,m_+,p_-,p_+,L_p.

For second time derivatives use the exact coefficient identity

    theta_t=N_tt/N-(N_t/N)^2-mu_tt/(R F)-2mu_t^2/(R F)^2.

The stored local ODE directional accelerations give numerical evaluations
of a triangle-inequality bound on this expression. They are not new exact
solutions or outward-rounded interval certificates.

For the coupled closure write the unaltered mass-rate mismatch as

    d=mu_t-s_mu,  mu_t=s_mu+d,
    ||mu_t||<=||s_mu||+||d||,
    Lip(mu_t)<=Lip(s_mu)+Lip(d),
    mu_tt=(s_mu)_t+d_t.

s_mu is the mass rate predicted by the full shift equation. The nonzero
d arrays and full shift covectors are carried forward and checked unchanged.
Neither d nor its space/time derivatives have been set to zero. A small
sampled d alone does NOT control Lip(d) or d_t. This is a genuine remaining
metric-jet problem, not another need to derive the same scalar energy identity.

## 11. Verification and numerical meaning

608/608 implementation checks pass. These include exact polynomial/template
certificates, 24 manufactured cases (N16/32/64/128; variable, constant-theta,
and frozen profiles; each with GR and Gram), and 18 unchanged canonical
saved states (initial/middle/final on N16/32/64 in both branches).
The manufactured variable metric contains coefficient-derivative kinks.
F=0 is explicitly rejected. The full nonsymmetric operator norm, not merely
its symmetric part, is checked against B_L. Old matrices, physical mismatch,
and full shift residuals are checked unchanged. All nonlinear old evidence
is preserved but is outside this theorem's scope.

Final-time values, in the existing normalized fixture units:

| Grid | Branch | measured C | analytic C_star | measured ||h_b|| | analytic H_b |
|---|---|---:|---:|---:|---:|
| N16 | GR | 0.00068055 | 0.520456 | 0.0734535 | 2.726535 |
| N16 | Gram | 0.00067004 | 0.565904 | 0.0734525 | 2.736728 |
| N32 | GR | 0.00066594 | 0.509277 | 0.0736204 | 2.724233 |
| N32 | Gram | 0.00066588 | 0.529361 | 0.0736175 | 2.728724 |
| N64 | GR | 0.00066058 | 0.506411 | 0.0737037 | 2.723696 |
| N64 | Gram | 0.00066091 | 0.514844 | 0.0737049 | 2.725557 |

The analytic bounds are very loose: roughly 10^3 above measured C and
about 37 times measured source norms. They prove no hidden h^-1 factor
under the stated assumptions; they are not sharp predictions and are not
evidence that MTS beats GR. Finite sample maxima do not establish envelopes
for all times or all finer-grid evolved solutions. Floating evaluations of
the analytic envelopes use ordinary arithmetic, not outward interval rounding.

Sources compile without bytecode. The runner verifies inherited evidence
hashes and writes no old results. The final seal checks the frozen workbench
by mtime since 2026-09-09T16:43:00Z, not by a full pre-turn hash baseline.
No worker is left running after this short single-core calculation.

## 12. Next derivation, not another scalar-bound inventory

The canonical scalar operator bounds and affine boundary source formulas
are now derived. Do not rerun a search for these same missing estimates.

Next differentiate the actual constraint/clock/shift relations to obtain
bounds on N, mu, N_t, mu_t and the required second time/spatial-mixed jets.
Carry the full physical shift mismatch and its derivatives through that
calculation. Seek a coupled bootstrap that preserves p_->0 and m_->0 and
makes the section 9 time integrals finite for the same family of solutions.
If an inverse constraint map or a boundary compatibility term is needed,
derive it from the existing action rather than setting its residual to zero.

Only after that canonical closure is controlled should the P(X) kinetic
correction be absorbed or symmetrized. This turn does not solve black-hole
regularity, derive a complete local-GR limit, or close the nonlinear parent.
