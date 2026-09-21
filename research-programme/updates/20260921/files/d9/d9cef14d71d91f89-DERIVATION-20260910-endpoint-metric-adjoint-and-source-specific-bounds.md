# Endpoint metric adjoint and source-specific bounds

Private continuation, 2026-09-10 (Europe/London). No GitHub action.

## 1. What changed

The third parent jet is already sourced. This continuation eliminates the
scalar-velocity block EXACTLY and solves for the particular endpoint metric
functional entering theta_tt. It does not replace the parent equations or
assume that the large scalar derivatives vanish.

This substantially improves the pointwise parent-derived source-rate bound.
At final N64 the earlier whole-parent upper 2272.027 GR / 2509.240 Gram becomes
0.232662 / 0.376102 using the reduced-source componentwise estimate. A separate
weighted-norm estimate gives 0.249266 / 0.404813. Both retain the original
third-jet forcing, including the fixed inner shift rate and Gram terms.

New model-specific identity: the lapse-lapse block of the metric Schur
complement is a POSITIVE projection-residual Gram matrix. It is not generally
zero: prescribed endpoint velocities and the actual quadrature projection
must remain. This identity also supplies a conditional mesh-independent bound
for that block; it does not imply positivity of the full metric Schur matrix.

The calculations do NOT certify the physical time interval or all-mesh parent
invertibility. They establish exact reduction identities, finite-state bounds,
and a conditional response-neighborhood theorem. Numerical spectral values
are ordinary floating-point evaluations, not outward-rounded certificates.

Validation: 603/603 checks on 18 unchanged states, including 36 adversarial
reduced-source box controls and 36 manufactured response-neighborhood controls.
These controls are algebraic, not additional physical trajectories or tests
of MTS against nature. No new evolution, fit, public action, or local-GR claim.

## 2. Owned setup and notation

Keep the canonical Lambda=m_chi=b2=b3=0 annulus, the original C1 Hermite scalar
space and positive Gauss4 quadrature, positive N and F=1-2mu/R, all free scalar
slopes, quadratic prescribed endpoint values, and the original affine outer
clock history. GR and metric-Gram are treated by the SAME method.

The previous note owns y3, the third packed parent jet, k3, and the fixed
third jet. The free parent equation is

    J_ff y3_f=f,  f=-(k3+J y3_fixed)_f.

The fixed vector is zero on free entries and contains the original prescribed
inner mass third rate and endpoint velocity third rates. In particular the
Gram metric-link shift current in that inner rate is retained. The earlier
saved interior shift mismatch is neither changed nor asserted zero.

Split free parent coordinates into metric a=(mu_free,N) and scalar velocities
v=(nodal velocities excluding the prescribed endpoints, all slope velocities).
Here a and v label BLOCKS, not new dynamical fields. All numbers use inherited
dimensionless coordinates.

Sources:

- `DERIVATION-20260910-parent-third-jet-and-boundary-source-variation.md`
- `DERIVATION-20260910-mesh-independent-regular-transport-with-clock-jumps.md`
- `scripts/annular_released_hermite_action_20260909.py`
- `scripts/annular_constraint_routhian_20260909.py`
- `scripts/annular_metric_flux_jets_20260909.py`
- `scripts/annular_boundary_source_variation_20260910.py`
- `scripts/annular_endpoint_metric_adjoint_20260910.py`
- `scripts/derive_annular_endpoint_metric_adjoint_20260910.py`

## 3. Exact elimination, not removal of scalar feedback

The symmetric free parent Jacobian has blocks

    J_ff = [ H  C ],
           [ C' M ].

In this canonical branch the scalar-velocity block is exactly the same
positive scalar mass matrix M used by the earlier energy argument. The Gram
coefficient is independent of velocity in this branch, so there is no omitted
Gram kinetic block. The runner checks M independently against the original
saved matrix and its positive quadrature construction.

Define the metric Schur matrix and reduced forcing

    S=H-C M^-1 C',       r=f_a-C M^-1 f_v.

Then, whenever S is invertible,

    y3_a=S^-1 r,
    y3_v=M^-1(f_v-C' y3_a).

Both reconstructed blocks agree with the prior saved third jet. Thus a large
scalar third derivative is not simply discarded: its coupling and its forcing
remain in C M^-1 C' and C M^-1 f_v respectively. All fixed-row contributions
remain inside f.

## 4. The endpoint functional actually needed

For either endpoint e define a row ell_e on the FULL packed vector by

    ell_e y3 = N3(e)/N(e)-mu3(e)/(R_e-2mu(e)).

Use the original linear face/node reconstruction for both metric evaluations.
The row has zero entries on scalar velocities. The known lower-jet term is

    l_e=-3N1 N2/N^2+2(N1/N)^3
                       -6mu1 mu2/(R-2mu)^2-8(mu1/(R-2mu))^3.

Let t_e be ell_e restricted to free metric entries, and
o_e=l_e+ell_e y3_fixed. The endpoint quantity is exactly

    theta_tt(e)=o_e+t_e S^-1 r.

Solve just the target adjoint equations

    S' z_e=t_e',
    theta_tt(e)=o_e+z_e' r.

The corresponding FULL parent adjoint is

    alpha_e=(z_e,-M^-1 C' z_e).

Its full-Jacobian solve and its response to f are independently checked. The
new reconstruction also agrees with the old direct theta_tt formula. This is
not a bound obtained by treating measured theta_tt itself as an unknown input.

Two componentwise bounds follow immediately:

    |theta_tt(e)| <= |o_e|+sum_i |z_e,i| |r_i| = U_S,e,
    |theta_tt(e)| <= |o_e|+sum_i |alpha_e,i| |f_i| = U_J,e.

U_S uses the ACTUAL reduced forcing, including its exact signed elimination.
It is valid at the sourced state; an interval application must bound that
reduced forcing throughout the interval. It is not legitimate to carry its
saved component values unchanged into a later time.

For the independent box |r_i|<=rbar_i and fixed o,z, the first inequality is
sharp: choose r_i=sign(o) sign(z_i) rbar_i, with either sign when o=0. The
runner checks this worst-case alignment by solving S against the manufactured
forcing. Those box forcings are not advertised as realizable parent states.

## 5. Natural metric norm, without the raw scalar inverse scaling

Choose a fixed analysis weight W, the block-diagonal unweighted quadrature
L2 mass matrices of the free linear mass reconstruction and linear lapse
reconstruction. W is an ANALYSIS norm, not a new physical mass term.
Let W=R'R be its Cholesky factorization and define

    Shat=R^-T S R^-1,
    rhat=R^-T r,    that_e=t_e R^-1,    zhat_e=R z_e.

Then Shat' zhat_e=that_e' and

    |theta_tt(e)| <= |o_e|+||zhat_e||2 ||rhat||2 = U_W,e.

Because Shat is symmetric, its inverse norm is

    kappa_S=1/min_j |lambda_j(Shat)|.

This is an absolute spectral gap for a SADDLE system, not a claim that its
eigenvalues are all positive. At the final states the inertia is (17,17),
(33,33), (65,65) negative/positive on N=16,32,64 in both branches.

The measured inverse norm stays near .0148689 and the endpoint adjoint norms
near (.0511,.0200). This contrasts with the raw mixed parent inverse infinity
norm ~404,808,1617. The norms are different; their numerical sizes are NOT a
direct comparison of equivalent operator bounds. The source-rate estimates
in section 9 are directly comparable bounds for the SAME endpoint quantity.

Three meshes and saved times do not prove mesh-uniformity. In particular a
uniform endpoint response requires control of the target adjoint, not only
the ordinary inverse norm: point evaluation itself can have mesh scaling.

## 6. Derived lapse Schur identity

This provides information about the actual parent structure, beyond the
general Schur-complement identity. Let q_h be the original reconstructed
scalar velocity, eta_h a linear lapse variation, and

    A_eta=q_h eta_h/N,      m=R^2/(N sqrt(F)).

Let Pi_0 denote the actual Qm-orthogonal projection onto FREE scalar velocity
tests. Both prescribed endpoint scalar velocities are excluded from that
test space; all slope degrees remain included.

The canonical bulk kinetic density is m q_h^2/2. Gravity, the canonical
spatial scalar term and the Gram coefficient are affine in N for fixed mass,
configuration and scalar velocity. Therefore their second lapse variations
vanish. Direct differentiation gives

    eta' H_NN eta = ||A_eta||Qm^2,
    C_N' eta = -(free scalar load of A_eta).

Consequently the lapse-lapse Schur block obeys the exact polarization identity

    eta' S_NN xi
       = ((I-Pi_0)A_eta,(I-Pi_0)A_xi)_Qm.

The runner reconstructs this block from the projection-error functions,
independently of subtracting C M^-1 C' from H. The two agree in both branches.
It follows that S_NN is positive semidefinite. It need not vanish: the product
need not belong to the free test space, particularly at its endpoints.

Projection contraction also proves, for W_N the lapse L2 mass matrix,

    0 <= eta' S_NN eta
       <= Q[m(q_h/N)^2 eta_h^2]
       <= sup_Q[m(q_h/N)^2] eta' W_N eta
       <= mmax (Qsup/Nmin)^2 eta' W_N eta,

where Qsup is a genuine upper bound for |q_h| at all quadrature points (or
everywhere). This last inequality is an analytic consequence of the identity,
not a separate counted numerical control. It has no explicit inverse mesh
factor, conditional on the displayed coefficient/velocity bounds.

This does NOT bound the other Schur blocks or their inverse. A positive small
S_NN block by itself cannot prove an indefinite saddle system is invertible.
That coupling question must be addressed, not concealed by the good numerical
spectral gap at the saved states.

## 7. Conditional neighborhood theorem

The analysis weight W depends only on the fixed basis and quadrature, so use
the SAME normalization throughout a prospective coefficient neighborhood.
At a base state denote Shat_0, zhat_0, rhat_0, that_0 and o_0 as above. Suppose
actual perturbations satisfy

    ||Delta Shat||2<=dS, ||Delta that||2<=dt,
    ||Delta rhat||2<=dr, |Delta o|<=do,
    eta=kappa_S dS<1.

The inverse perturbation identity gives

    ||Shat^-1||2 <= kappa_S/(1-eta),
    ||Delta zhat||2 <= kappa_S/(1-eta)
                                (dt+dS ||zhat_0||2) = dz.

Indeed (Shat_0+Delta Shat)' Delta zhat =
Delta that'-(Delta Shat)' zhat_0. Expanding the changed response then proves

    |Delta theta_tt| <= do+||zhat_0||2 dr
                                      +dz (||rhat_0||2+dr).

The implementation rejects negative/nonfinite majorants and makes NO inverse
persistence conclusion when eta>=1. It checks the formula under manufactured
symmetric matrix perturbations with eta=.2, perturbed targets, forcing and
offsets, using independent perturbed solves for both endpoints at all states.

These perturbations validate the algebra, not physical reachability. We have
NOT yet supplied dS,dt,dr,do enclosing the actual parent evolution. A numerical
base-state inverse norm also needs a rigorous enclosure before the theorem
becomes a computer-assisted interval certificate.

## 8. Transfer to the unchanged boundary-source rate

The previous exact repacking remains

    b=B beta_red,end+b_red,reg.

The source derivative formula contains -theta_tt ell_t. All other terms have
the earlier sourced conditional upper, denoted R_no3,e. Substituting any of
U_S,e, U_J,e or U_W,e yields

    |beta_red,t(e)| <= R_no3,e+U_e |ell_t(e)|.

No source term, regular remainder, endpoint work or Gram contribution is
dropped. The earlier complete source arrays and derivative arrays remain
unchanged and their hashes are inherited. A time-integrable majorant would
then bound the total variation needed by the boundary-memory argument.
It is still wrong to integrate just three saved rate values and call that a
certified upper on the whole interval.

## 9. Results on the original final states

Final t=.01, dimensionless R2 source-rate upper bounds:

| Cells | Branch | Previous whole-parent | New reduced-box | New weighted-norm | Earlier direct endpoint |
| --- | --- | ---: | ---: | ---: | ---: |
| 16 | GR | 355.035 | .305041 | .315302 | .295719 |
| 16 | metric-Gram | 514.779 | .397930 | .416012 | .389234 |
| 32 | GR | 1277.132 | .274741 | .287597 | .264446 |
| 32 | metric-Gram | 1961.535 | .367337 | .385574 | .354739 |
| 64 | GR | 2272.027 | .232662 | .249266 | .221951 |
| 64 | metric-Gram | 2509.240 | .376102 | .404813 | .362525 |

The earlier direct-endpoint column uses the computed theta_tt value rather
than a bound on the parent response. It is shown for context, not promoted
to a response bound over other states. The new columns bound that response
from the sourced parent forcing and adjoint instead.

At N64 the componentwise theta_tt uppers are (.57511,.55981) GR and
(.74366,.72143) Gram. They enclose the prior directly reconstructed endpoint
values, with no need to use the raw maximum of every third jet.

| Cells | Branch | max metric third jet | max scalar-velocity third jet | kappa_S |
| --- | --- | ---: | ---: | ---: |
| 16 | GR | .20353 | 1143.79 | .01486888 |
| 16 | metric-Gram | .28521 | 2490.57 | .01486888 |
| 32 | GR | .20271 | 2172.90 | .01486887 |
| 32 | metric-Gram | .24708 | 4968.58 | .01486887 |
| 64 | GR | .20356 | 3236.00 | .01486887 |
| 64 | metric-Gram | .24414 | 6102.28 | .01486887 |

The earlier large packed maximum was indeed dominated by scalar-velocity
derivatives at these states. This does not prove those scalar derivatives
are harmless for other estimates or have a continuum limit. It shows why
assigning their worst bound to the endpoint metric response was wasteful.

The weighted reduced-forcing norms increase across these saved meshes
(GR about 32.53,37.85,43.33; Gram 42.93,56.58,70.50). We retain this warning:
uniform control of the response source has NOT been established merely
because the saved adjoint norms and metric spectral gap look stable.

## 10. Next derivation, without another global derivative shortcut

Construct a PARENT-OWNED positive-coefficient neighborhood that bounds the
normalized metric matrix, endpoint target and reduced third-jet forcing.
The lapse projection-residual identity gives one explicit controlled block;
the mass-lapse saddle coupling and remaining metric block must supply the
inverse estimate. Use the actual block equations and their coefficient
variation, not a new assumption that the good sampled eigenvalue persists.

Then connect that neighborhood to time using the parent evolution and the
already sourced jets. The response-neighborhood formula states exactly which
majorants are needed and avoids treating every scalar/metric component by
one maximum. Regular-source jumps, affine quadrature and positive-annulus
persistence still have to close. No horizon or full-theory conclusion follows
from this canonical annulus calculation alone.

## 11. Reproducibility and preservation

- `source-intake/navier-stokes/20260910/annular-endpoint-metric-adjoint-derived/status.json`
- `source-intake/navier-stokes/20260910/annular-boundary-source-variation-final-integrity.json`
- `source-intake/navier-stokes/20260910/annular-endpoint-metric-adjoint-final-integrity.json`

The additive runner records the Schur matrices, both reconstructed third-jet
blocks, full and reduced adjoints, source bounds, normalized spectra, lapse
projection residuals, manufactured-control diagnostics, and every inherited
source hash. The seal checks cited paths and hashes and saves a resume snapshot.
No prior completed evidence is overwritten.

One single-core BelowNormal Python worker was used; no evolution or other
agent was launched. The protected formalization-workbench check is an mtime
scan since 2026-09-10T10:42:12Z, not a full pre-turn content-hash baseline.
No galaxy files, prior public publication, or shared processes were changed.
