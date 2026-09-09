# Spatial clock control and the actual inner flux: two inputs are now derived

Date: 2026-09-09. Private canonical annular continuation.

## 1. Result, scope and the remaining gap

Within the existing canonical configuration box, this step derives:

- a pointwise bound on the background lapse gradient N_R, hence on p_R;
- an L2 bound on the lapse-rate gradient N_tR and clock-rate gradient theta_R;
- an L2 bound on the PAIRED flux remainder, without removing its defects;
- a mesh-uniform bound on the ACTUAL full shift velocity, including its inner
  trace and the candidate's metric-link Gram current.

The spatial coefficient Lipschitz bound and inner shift trace no longer
have to be supplied as independent measured inputs to the first-response
estimate. The scalar graph energy and prescribed boundary histories remain.
All statements are conditional on the canonical box and the retained
constraint residuals. They do NOT show that an evolved solution stays there.

Important norm distinction: theta_R is controlled in L2, NOT pointwise.
The preceding scalar transport proof used a pointwise coefficient gradient.
We must derive an H1-coefficient version of that energy argument before
calling the evolution estimate closed. An L2 bound cannot simply be
substituted into a formula requiring an infinity norm.

No nonlinear P(X), full shift/DAE compatibility, horizon crossing, black-hole
regularity, observational pass or complete MTS-to-GR limit is claimed.

## 2. Owners, results and reproducibility

Previous response theorem:
`DERIVATION-20260909-first-metric-source-and-pointwise-lapse-bound.md`.
Inverse and exact staggered geometry:
`DERIVATION-20260909-metric-Schur-inverse-and-projection-remainder.md`.
Flux identity and physical mismatch definitions:
`DERIVATION-20260909-metric-flux-cancellation-and-exact-constraint-jets.md`.
Owned action/geometry:
`scripts/annular_released_hermite_action_20260909.py`,
`scripts/annular_metric_link_quadratic_20260909.py`,
`scripts/annular_gram_joint_action_20260909.py`,
`scripts/sbp4_compatible_second_operator_20260909.py`.

New spatial helper and runner:
`scripts/annular_clock_spatial_bound_20260909.py` and
`scripts/derive_annular_clock_spatial_bound_20260909.py` (derive phase).
Inner-shift certificate and COMBINED FINAL SEAL OWNER:
`scripts/certify_annular_inner_shift_trace_20260909.py` (derive/seal).
Results:
`source-intake/navier-stokes/20260909/annular-clock-spatial-gradient-derived/status.json`
and
`source-intake/navier-stokes/20260909/annular-inner-shift-trace-certified/status.json`.
Combined integrity:
`source-intake/navier-stokes/20260909/annular-clock-spatial-and-inner-shift-final-integrity.json`.

The first result still labels the inner flux as an input; the companion
then derives and substitutes an upper bound for that input in the ESTIMATE.
It does not replace the physical boundary data or trajectory. Use the
combined seal, not the spatial runner's unused standalone seal option.

## 3. Exact differentiated overlap, not an inverse h estimate

Keep the old box: [a,b]=[47/8,49/8], kappa=1/10,
13/20<=F<=17/25, 4/5<=N<=21/25, |q|<=1/50,
|chi_R|<=3/100, |mu_R|<=1/500, n>=17, ell=b-a and h=ell/(n-1).
Write F0,F1,N0,N1,Q0,W0,U0 for these bounds and A0=aF0.

Let H be the exact mass-cell/lapse-node overlap matrix and omega_i the
mass-cell widths divided by h. Define the cell-average matrix
A=diag(omega_i^-1)H. Because A preserves constants, there is an exact
commuting relation

    diff(A n)/h = G diff(n)/h.

The first five rows of G, restricted to the first six columns, are

    [925/1416, 49/354, 0, 0, 0, 0]
    [961/5664, 1940/2537, 529/4128, 0, 0, 0]
    [0, 25/258, 37369/50568, 6/49, 0, 0]
    [0, 0, 625/4704, 295/392, 1/8, 0]
    [0, 0, 0, 1/8, 3/4, 1/8].

The interior row repeats (1/8,3/4,1/8); the right boundary is reflected.
These disjoint templates cover every supported grid. The exact strict gaps
are g_row=18951/40592 and g_column=12085/25284.
Thus ||G^-1||_infinity<=1/g_row and
||G^-1||_2<=1/sqrt(g_row g_column), with sqrt(g_row g_column)>=47/100.

Let sigma=F^-1/2, sigma0=123/100 and delta_sigma=1/50.
For the positive actual cell quadrature, differences of neighboring cell
means are positive averages of the spatial derivative. Their kernel row
integrals are <=omega_max=59/48 and the weighted column sum is <=1.
Consequently their infinity and L2 bounds are omega_max and sqrt(omega_max).
This holds for continuous piecewise H1 functions, not only polynomials.

Apply this to (sigma-sigma0)n. The derivative contains
(sigma-sigma0)n_R+sigma_R n. Absorbing the first term is valid because

    sigma0*g_row-delta_sigma*omega_max >1/2,
    sigma0*(47/100)-delta_sigma*(9/8) >1/2,
    sqrt(omega_max)<=9/8.

All constant comparisons are exact rational certificates. The remaining
sigma_R n term is bounded explicitly, not set to zero.

## 4. The cumulative mass equation and its nonzero residual

Set E_clock=N/sqrt(F). Write the actual mass covector as

    C_mu=P_R^T Q[E_clock/kappa]+P^T Q[V]+P_node^T z
          -c_b e_b/kappa,
    V=N mu_R/(kappa R F^(3/2))+R q^2/(2N F^(3/2))
          +R N w^2/(2sqrt(F)),
    z_j=rho_j R_j N_j/sqrt(F_j) [Gram only].

The free mass test primitive for cell i is its clipped linear ramp psi_i.
Dividing its equation by the mass-cell width gives the EXACT identity

    average_i(E_clock)+kappa Q[psi_i V]+kappa sum_j psi_i(R_j)z_j
       =c_b+kappa sum_(free mass nodes k>=i) r_k,

where r is the actual mass covector residual. This includes the natural
outer equation. Differentiating in space cancels the constant c_b, but its
amplitude and time derivative remain in the preceding response theorem.

The positive source hats J_i=(psi_i-psi_(i+1))/h have integral <=omega_max
and sum_i h J_i<=1. For nodal atoms they obey h sum_j J_i(R_j)<=3 and
sum_i h J_i(R_j)<=1. The nodal factor 3 follows from the bounded support
over at most three uniform scalar nodes. Therefore

    ||source_bulk_difference||_infinity<=omega_max ||V||_infinity,
    ||source_bulk_difference||_(h l2)<=sqrt(omega_max)||V||_Q2,
    ||source_atom_difference||_infinity<=3||z/h||_infinity,
    ||source_atom_difference||_(h l2)<=sqrt(3)||z||_(h^-1 l2).

The residual contributes the interior mass-face values r/h, NOT the fixed
inner reaction. At first time order it contributes r_t/h. These are physical
residual-density norms; fixed absolute solver tolerances do not by themselves
bound them as h tends to zero. They vanish on the exact constraint manifold.
Every sampled nonzero residual is retained in the numerical estimates.

## 5. Background spatial coefficient is derived

From F_R=(1-F-2mu_R)/R,

    L_F=(1-F0+2U0)/a >= ||F_R||_infinity,
    L_sigma=L_F/(2F0^(3/2)).

The mass density satisfies

    V0=N1 U0/(kappa a F0^(3/2))
       +b Q0^2/(2N0 F0^(3/2))+b N1 W0^2/(2sqrt(F0)),
    Z0=2 I_G W0^2 p_+/A0 >= ||z/h||_infinity,

where I_G is one for Gram and zero for GR. The static mass row and the
inverse margin in section 3 imply

    L_N=2[kappa(omega_max V0+3Z0+||r_interior/h||_infinity)
              +omega_max L_sigma N1] >= ||N_R||_infinity.

Hence the spatial input to the previous first-source theorem is now

    L_p=2b N1 sqrt(F1)+b^2 L_N sqrt(F1)
          +b^2 N1 L_F/(2sqrt(F0)) >= ||p_R||_infinity.

It is derived from the box and the mass equation, not measured from N_R.
On the saved roots it is about 13.4212 for GR and 13.6510 for Gram, compared
with sampled |p_R| around 10.2501. This estimate is reasonably informative.

## 6. Differentiated source gives a spatial clock-rate L2 bound

Use the preceding graph-energy/source theorem with the DERIVED L_p.
Denote its bounds by R_m for ||mu_tR||_2 and ||N_t||_(h l2), M_t for
||mu_t||_infinity, N_t^max for ||N_t||_infinity, Q1 for ||q_R||_2,
R_scalar for the scalar stiffness-force mass norm, and Theta0 for
||theta||_infinity, theta=partial_t log(N sqrt(F)).

The actual differentiated Legendre equation gives

    q_t=(I-Pi)eta-r_scalar+Pi(theta q)+scalar_residual,
    ||q_t||_2 <= [sqrt(m_+)||eta||_2+R_scalar
                  +sqrt(m_+)Q0 sqrt(ell)Theta0+epsilon_v]/sqrt(m_-).

Pi is the free weighted scalar projection and eta is the unchanged affine
endpoint-acceleration lift. epsilon_v is the actual free scalar equation
residual in its mass-dual norm. Metric Schur solve residuals are also added
to the response bound in their proper dual norm; neither residual is erased.

Differentiating V in section 4 requires only N_t,mu_t,mu_tR,q_t and q_R:

    V_t=(N_t mu_R+N mu_tR)/(kappa R F^(3/2))
       +3N mu_R mu_t/(kappa R^2 F^(5/2))
       +R q q_t/(N F^(3/2))-R q^2 N_t/(2N^2 F^(3/2))
       +3q^2 mu_t/(2N F^(5/2))
       +R N_t w^2/(2sqrt(F))+R N w q_R/sqrt(F)
       +N w^2 mu_t/(2F^(3/2)).

Every undifferentiated factor is bounded by the box; the remaining factors
are controlled in L2 or infinity by the just-derived response. The helper
records their explicit positive majorant V1. No unknown N_tR is in V1.

The Gram atom derivative is

    z_t=rho_t R N/sqrt(F)+rho[R N_t/sqrt(F)+N mu_t/F^(3/2)].

The preceding ||rho_t||_(h^-1 l2)<=sqrt(8)W0 Q1 gives an explicit bound Z1
for ||z_t||_(h^-1 l2); the second term uses rho<=2hW0^2 and the response.

The additional differentiated coefficient is lambda=sigma_t N=N mu_t/(R F^(3/2)).
Define

    J0=N1/(a F0^(3/2)),
    J_R=L_N/(a F0^(3/2))+N1/(a^2 F0^(3/2))
          +3N1 L_F/(2a F0^(5/2)),
    Lambda1=J0 R_m+J_R sqrt(ell) M_t >= ||lambda_R||_2.

The differentiated actual mass row now yields

    N_tR_bound=2[kappa(sqrt(omega_max)V1+sqrt(3)Z1+||r_t,interior/h||_(h l2))
                    +sqrt(omega_max)(Lambda1+L_sigma R_m)].

Finally, since theta=N_t/N-mu_t/(RF),

    ||theta_R||_2 <= N_tR_bound/N0
       +N_t^max sqrt(ell)L_N/N0^2+R_m/A0
       +M_t sqrt(ell)(1+2U0)/A0^2.

This is a genuine spatial H1 estimate for the clock rate, with mesh-uniform
constants and explicit residual norms. It is not a pointwise derivative bound.

## 7. The paired physical flux remainder stays intact

The previous off-shell identity was

    theta_R=2s/(RF)^2 + [Delta-2(D/(RF))_R],
    s=kappa R^2 F q w,
    D=mu_t-s=P d+(P s_shift-s).

The independently derived bound on theta_R now implies

    ||Delta-2(D/(RF))_R||_2
       <= theta_R_bound+2kappa Q0 W0 sqrt(ell)/F0.

The Gram current/projection difference in D is still present. This result
does not set the physical mismatch d, D, Delta or their derivatives to zero.
All old physical d, d_t and complete shift covectors are preserved.

## 8. The physical inner flux is also bounded by its own equation

The full shift equation has the positive mass pairing

    M_shift=Q[W phi_i phi_j], W=1/(kappa N F^(3/2)),
    M_shift s_shift = Q[W phi_i s]+Gram_shift.

For a mass node with adjacent-cell total length H_i, positivity and exact
quadratic integration give

    M_ii-sum_(j!=i)|M_ij| >= H_i(2W_- -W_+)/6.

The common box admits exact rational W_-=2500/119, W_+=625/26 and
2W_- -W_+=55625/3094>0. This includes BOTH endpoint rows of the shift solve.

The canonical local derivative of the Gram coefficient with respect to
shift is exactly zero. Its metric-LINK current is not zero and is retained.
For each owned factor f let T1_f=sum|t_fj| and
D_f=sum|t_fj||j-anchor_f|. Zero factor row sum and |chi_R|<=W0 give
|Tchi_f|<=hW0 D_f; |Tq_f|<=Q0 T1_f. Thus each link current is bounded by

    |J_fj|<=p_+Q0W0 D_f(s_fj T1_f+|t_fj|).

All links lie within their factor's support. The three factor families
(single third differences, adjacent pairs, and the two boundary extra
pairs) have respective bounds on 2D_f T1_f of 12,3,9/4, and at most
4,5,2 active factors at a point. Hence their sum is at most

    4*12+5*3+2*(9/4)=135/2 <68.

This follows from the owned rational coefficient bounds and finite supports,
not from a fitted current. Link quadrature has positive weights along each
orientation and exactly integrates the mass hat after taking the bounded
inverse clock outside. With I0=1/(N0^2F0),

    |Gram_shift_i| <= (H_i/2) I0*68*p_+Q0W0.

Maximum-component diagonal dominance therefore proves

    ||s_shift||_infinity <=
       3[W_+ kappa b^2 F1 Q0W0+I_G I0*68*p_+Q0W0]/(2W_- -W_+)
       +6 max_i|shift_residual_i/H_i|/(2W_- -W_+).

The zero-residual rational bounds are

    GR:   43715007/7120000000 = approximately 0.00613975,
    Gram: 3103765497/7120000000 = approximately 0.43592212.

They also bound the actual inner trace u_a=s_shift(a). The companion
substitutes these bounds into the ESTIMATE from section 6 without replacing
the actual u_a in the tangent or prescribing a favorable flux.
The Gram bound is very loose because all link cancellations were discarded.
It is a finite control constant, not a physical prediction of a large flux.

## 9. Checks, sizes, and honest interpretation

520/520 spatial checks and 175/175 inner-shift checks pass. The same 18 saved
states are used, with GR and Gram treated alike. Eight manufactured spatial
controls include deliberately off-shell oscillatory lapse profiles: their
residual-density term is essential, and dropping it would give a false bound.
No new evolution was launched. These are algebra/code checks, not new
observations or independent experiments.

Final relative time 0.01:

| Grid | Branch | measured ||theta_R||_Q2 | measured paired remainder Q2 | derived theta_R L2 bound, using derived inner flux |
|---|---|---:|---:|---:|
| N16 | GR | 0.00030057 | 0.00029778 | 1.170662 |
| N16 | Gram | 0.00030210 | 0.00029917 | 3.597248 |
| N32 | GR | 0.00015241 | 0.00014710 | 1.171551 |
| N32 | Gram | 0.00015246 | 0.00014731 | 3.596875 |
| N64 | GR | 0.00008383 | 0.00007362 | 1.171954 |
| N64 | Gram | 0.00008401 | 0.00007369 | 3.597484 |

The measured clock/paired norms use the existing quadrature and are not
outward-rounded integral certificates. The analytic inequalities control
continuous L2 norms using the proven coefficient/polynomial majorants.
The displayed bounds are conservative, not tight predictions. Sampled
decrease of the paired discrepancy is encouraging numerical behavior but
not a convergence theorem or a proof that physical shift compatibility holds.

## 10. Next derivation

Rework the canonical scalar graph-energy transport with the H1 clock
coefficient now available: in one spatial dimension, products can use
L2 coefficient gradients with appropriate scalar Sobolev control, but
the ACTUAL weighted free Hermite projection and Gram commutators must be
bounded explicitly. Do not silently reuse an infinity-gradient theorem.

The target is a coupled differential energy inequality with derived spatial
and inner-flux coefficients, followed by persistence of the configuration
box. Derive the second effective source if that energy hierarchy requires
it, using the owned second jets rather than another finite-difference fit.
Do not redo the now-derived spatial coefficient or inner-shift input audit.

Protected workbench verification is an mtime scan since 2026-09-09T21:11:00Z,
not a full pre-turn hash baseline. All work remains local and private.
