# Mesh-independent regular transport with retained clock jumps and Gram terms

Private continuation, 2026-09-10 (Europe/London). No GitHub action.

## 1. Result and exact scope

The regular configuration transport D0 now has a DERIVED mesh-independent
bound, conditional on the stated positive coefficient, clock Lipschitz and
broken curvature/jump bounds. Together with the existing endpoint normal
form, this supplies a conditional mesh-independent HOMOGENEOUS moving-energy
estimate. The previous dependence on a measured finite-mesh growth rate is
no longer necessary for that estimate.

The decisive new estimate is ||E||_(M to M)<=h C_E for the actual weak
commutator. Its factor h cancels the inverse h when estimating its energy
norm. A second lemma bounds the mass projection of functions with INTERNAL
VALUE jumps; those jumps are retained rather than calling the function H1.
The actual Gram coefficient-sampling/product commutator is included.

This does not prove the parent equations propagate these coefficient bounds,
control the external source history, preserve the positive annulus, or close
local GR/the horizon/nonlinear DAE problem. In particular, our explicit
constants are extremely loose: at the final N64 states the new homogeneous
upper rates are about 671 GR and 2326 Gram, versus measured rates about
.000236 and .000339. Removing inverse mesh factors is meaningful, but it is
NOT the same as a quantitatively useful long-time estimate.

Validation: 886 passing checks; 18 unchanged saved states, 32 manufactured
coefficient controls and 32 projection/function controls. These validate
algebra, constants and numerical inequalities, not physical correctness.

## 2. Hypotheses and inherited notation

Use the SAME canonical b2=b3=m_chi=Lambda=0 annulus, composite positive
Gauss4 quadrature and C1 cubic Hermite space V_h. Only endpoint scalar VALUES
are fixed; every slope remains free. The scalar mesh is uniform with n>=17
nodes; its union with the owned staggered mass faces has at most one interior
mass face per scalar cell. The verified SBP boundary face geometry is retained.
All quantities use the inherited dimensionless conventions.

Let 0<m_min<=m<=m_max, 0<p_min<=p<=p_max and |p_R|<=L_p. Put

    c=N sqrt(F), m=R^2/c, p=R^2 c, theta=c_t/c,
    M=(.,.)_(Qm), K=a_bulk+a_Gram, L=M^-1 K, U=L^-1,
    A=M^-1 M_t=-Pi(theta .), C=M^-1 K_t U,
    D_g=C-A, D_h=C-A-L A U,
    T=-diag(c(e)^2 theta_R(e)) E_R U, D0=D_g-BT.

Pi is the ACTUAL weighted quadrature projection, B=Pi ell_map, and e denotes
the two endpoints. No projection or boundary condition is changed here.

For the continuous, piecewise-H2 clock on the union partition define

    L_theta=||theta_R||_infinity,
    H_theta=||theta_R||_L2,
    Q_theta=||theta_RR||_(broken L2),
    J_theta^2=sum_internal |[theta_R]|^2/h,
    R_theta=Q_theta+sqrt(6)J_theta.

The derivative may jump. No globally C2 clock is assumed. Conditional
mesh-uniformity means all coefficient and displayed regularity bounds are
uniform in h on the time interval in question; this is NOT inferred from
three saved time samples. The inherited elliptic bounds give, for u=U g,

    ||u_R||<=D1||g||_M, ||u_RR||<=D2||g||_M,
    ||u_R||_infinity<=Dinf||g||_M.

Sources and constants:

- `DERIVATION-20260910-released-slope-feedback-and-boundary-normal-form.md`
- `DERIVATION-20260910-endpoint-commutator-bound-with-parent-clock-jumps.md`
- `DERIVATION-20260909-H1-clock-energy-transport-and-boundary-feedback.md`
- `scripts/annular_H1_clock_energy_20260909.py`
- `scripts/annular_uniform_energy_bounds_20260909.py`

## 3. Exact weak remainder, not a pointwise endpoint substitution

Write zeta_g=-c^2 theta_R u_R and

    E=C+A-Pi zeta_map,
    D0g=-2Ag+Pi(zeta_g-ell_map Tg)+Eg.

We do NOT replace the strong reconstruction -(p u_R)_R/m by g at endpoints.
For any test v in V_h define W_theta v by nodal values theta_i v_i and nodal
physical slopes theta_i v_R,i. W_theta is only an auxiliary test-space map.
It need not match the derivative of the product theta v. It is the existing
nodal multiplier map in the uniform-energy helper and preserves zero endpoint
values. Set e_v=theta v-W_theta v. The weak elliptic equation for W_theta v
gives the EXACT quadrature identity

    (v,Eg)_M = Q[p u_R e_v,R]-Q[m g e_v]
                 +a_Gram,t(u,v)-a_Gram(u,W_theta v).

The new runner reconstructs the entire operator E from these three terms and
checks it against C+A-Pi zeta_map. In particular, the mass-load and Gram terms
are not omitted and no integration error is declared zero without justification.

## 4. Local multiplication estimates and quadrature remainder

On a scalar cell of length h, let theta_i be its left value and R_i v the
right-endpoint Hermite lift: right nodal value and slope of v, zero left data.
The inherited exact polynomial certificates prove

    ||R_i v||<=2||v||, ||(R_i v)_R||<=13||v||/h,
    ||v_R||<=16||v||/h.

All polynomial L2 norms equal their composite Gauss4 norms. Since

    W_theta v=theta_i v+(theta_(i+1)-theta_i)R_i v,

positivity and |theta-theta_i|<=h L_theta give

    ||e_v||_Q <=3h L_theta||v||,
    ||e_v,R||_Q <=30 L_theta||v||.

Let k=p u_R, a continuous H1 flux. Subtract k at the left endpoint of each
scalar cell. The nonconstant part obeys

    |Q[(k-k_i)e_v,R]|<=30h L_theta||k_R||_cell||v||_cell.

For the constant part, e_v vanishes at both cell endpoints, hence the true
integral of e_v,R is zero, including the interior partition knot. Its
QUADRATURE integral need not vanish. The polynomial W_theta derivative is
integrated exactly, leaving (Q-integral)(theta v)_R.

On a union subcell of length delta<=h, approximate theta by its one-sided
affine Taylor polynomial. The product of this affine function with cubic v
has derivative of degree at most three, integrated exactly by Gauss4. For
the remainder r_theta, the fundamental theorem and Cauchy-Schwarz give

    ||r_theta,R||_infinity<=sqrt(delta)||theta_RR||_subcell,
    ||r_theta||_infinity<=delta^(3/2)||theta_RR||_subcell.

Cubic/quadratic evaluation estimates give

    ||v||_infinity<=4||v||_cell/sqrt(h),
    ||v_R||_infinity<=48||v||_cell/h^(3/2).

These follow from degree<=3 Legendre suprema and the inverse16 estimate;
the low-degree Legendre suprema are checked symbolically. Bounding both the
positive quadrature and the integral by the supremum yields

    |(Q-integral)(r_theta v)_R|
       <=104 delta^(3/2)||theta_RR||_subcell||v||_cell/sqrt(h).

Summing subcells uses sum(delta^3)<=h^3, not a lower bound on their widths.
Then summing scalar cells proves the retained quadrature estimate

    |Q[k e_v,R]|
       <=h[30 L_theta||k_R||+104||k||_infinity Q_theta]||v||.

Clock-gradient jumps cause no unaccounted delta term here: theta v and e_v
are continuous, and their derivatives are integrated piecewise. Only the
second derivative inside open subcells enters the Taylor remainder.

Also |Q[m g e_v]|<=3h m_max L_theta||g||_L2||v||_L2.

## 5. Gram commutator: its factor h is also derived

The owned Gram form is

    a_Gram(u,v)=h^-1 sum_r a_r (F u)_r(F v)_r,
    a_r=(sampling p)_r, a_r,t=(sampling(p theta))_r.

F=H Delta^3 is the existing factorization, not a replacement stencil. The
source-backed exact template row bounds imply ||abs(H)||_2<=1/sqrt(8), hence
||abs(F)||_2<=sqrt(8). Every factor and its convex coefficient-sampling nodes
lie within a stencil of diameter at most 5h, including boundary extra rows.
These assertions follow from the template formulas for arbitrary n>=17;
the runner additionally checks them on all four manufactured grids.

For a factor row, the difference in its clock factors is bounded by

    |a_r,t(Fv)_r-a_r(F(theta_nodes v_nodes))_r|
       <=5h p_max L_theta (abs(F) abs(v_nodes))_r.

Cubic nodal evaluation gives
||v_nodes||_l2<=4sqrt(2)||v||_L2/sqrt(h). The existing H2 third-difference
bound gives ||F u||_l2<=sqrt(2/3)h^(3/2)||u_RR||. Thus

    |a_Gram,t(u,v)-a_Gram(u,W_theta v)|
       <=80sqrt(2/3)h p_max L_theta||u_RR||||v||
       <=128h p_max L_theta||u_RR||||v||.

The last rounding is deliberately conservative and checked exactly. This
is why a bare norm bound on K_Gram,t, which would lose the cancellation, is
not substituted for the actual product commutator.

## 6. The weak commutator gains exactly the needed mesh factor

Using ||k_R||<=L_p D1||g||_M+p_max D2||g||_M and
||k||_infinity<=p_max Dinf||g||_M, define

    C_E=[30 L_theta(L_p D1+p_max D2)
            +104p_max Dinf Q_theta
            +3m_max L_theta/sqrt(m_min)
            +I_Gram 128p_max L_theta D2]/sqrt(m_min).

Section 3 and duality in the actual M inner product prove

    ||Eg||_M<=h C_E||g||_M.

Let G0=2p_max in Gram and zero in GR. The inherited cubic inverse and Gram
gradient inequalities give, for any free coefficient vector,

    ||v||_K<=16 sqrt((p_max+G0)/m_min)||v||_M/h.

Therefore

    ||Eg||_K<=E_star||g||_M,
    E_star=16sqrt((p_max+G0)/m_min) C_E.

There is no hidden inverse h in E_star. The exact spatially constant-clock
case has C_E=0 and E=0, consistent with C=theta I and A=-theta I.

## 7. Projection lemma for internal VALUE jumps

For a piecewise-H1 function f on the union partition with zero one-sided
endpoint values, define

    J_h(f)^2=sum_internal |[f]|^2/h,
    R1_h(f)=||f_R||_(broken L2)+sqrt(6)J_h(f).

The function is NOT called globally H1 when it has nonzero jumps. Construct
I_h f from arithmetic means of the two nodal traces, one-sided endpoint
values, and zero physical nodal slopes. This auxiliary interpolant does not
change any physical field or impose a slope condition on it.

On each scalar cell set T_cell=||f_R||_cell+h^-1/2 sum_relevant |[f]|,
including its internal face and its two scalar-node ends. The variation
bound and the convex zero-slope cubic shape give

    ||f-I_hf||_(Q,cell)<=2h T_cell,
    ||(I_hf)_R||_cell<=2T_cell.

At most three jumps occur in this accounting, with each internal scalar-node
jump counted at most twice. Thus ||T_cell||_l2<=R1_h(f). Projection contraction
and inverse16 then prove

    ||(Pi f)_R||<=P R1_h(f), P=2+32sqrt(m_max/m_min),
    ||Pi f||_K<=sqrt(p_max+G0) P R1_h(f).

This supplies the missing discontinuous-input version of the previous
zero-trace projection lemma; it does not weaken its endpoint requirement.

## 8. Apply it to the real clock-gradient term

Write C2>=sup(c^2), C2_R>=sup|(c^2)_R|. These are sourced from the original
positive metric coefficient envelopes, not free fit parameters. Since u and
u_R are continuous,

    [zeta_g]=-c^2 u_R[theta_R],
    (zeta_g)_R=-[(c^2)_R theta_R+c^2 theta_RR]u_R-c^2 theta_R u_RR.

Let t_star=Dinf |c(e)^2 theta_R(e)|_2, as in the normal-form checkpoint. The
affine lift of Tg has derivative norm at most sqrt(2/length)t_star||g||_M.
For f=zeta_g-ell_map Tg, consequently

    R1_h(f)<=Z_star||g||_M,
    Z_star=Dinf[C2_R H_theta+C2 R_theta]
              +C2 L_theta D2+sqrt(2/length)t_star,
    ||Pi f||_K<=Z_K||g||_M,
    Z_K=sqrt(p_max+G0)P Z_star.

This includes the actual value jumps and the actual endpoint trace. No
endpoint u_RR condition or extra time derivative is needed.

## 9. Complete conditional regular and normal-form growth bounds

Choose a spatial constant theta0 and radius delta with |theta-theta0|<=delta.
Let eta=theta-theta0. The existing transport helper evaluated with center
zero supplies A_eta_star>=||A_eta||_(K to K) and
C_eta_star>=||C_eta||_(M to M). Set rho=length sqrt(m_max/p_min). Sections 6-8
give the new bound

    ||D0-2theta0 I||_(K to K)<=B0,
    B0=2 A_eta_star+rho(Z_K+E_star).

For the velocity block, retain the already proved graph-projection lemma
with constants C1,C2graph and use

    P1=D1(delta+sqrt(length)H_theta),
    P2=sqrt(length)D1 R_theta+2Dinf H_theta+delta D2,
    ||D_h-3theta0 I||_(M to M)<=Bh,
    Bh=C_eta_star+delta+C1 P1+C2graph P2.

Here D_h=3theta0 I+C_eta-A_eta+L Pi(eta U). Keeping the signs of the spatial
constant part in K_t and M_t yields

    Gamma0=max(0, 5theta0+delta+2max(B0,Bh)).

This bounds the paired regular forms involving D0 and D_h. Unlike the
previous checkpoint's finite-mesh Gamma0, it is an explicit conditional
mesh-independent expression. It gives exactly max(0,5theta0) for a purely
constant clock, including the negative-clock controls.

The previous derived normal form w=h+B T g has

    g_t=w+D0g+b,
    w_t=-Lg+(D_h+BT)w+H g+r+BTb,
    H=F_B T+B S-BTBT.

With the already sourced b_star, t_star, s_star, f_star,

    H_star=f_star t_star+b_star s_star+b_star^2 t_star^2,
    Gamma_N=Gamma0+2b_star t_star+rho H_star,

and the full energy inequality is

    E_N'<=Gamma_N E_N
           +sqrt(2E_N)sqrt(||b||_K^2+||r+BTb||_M^2).

Gamma_N is mesh-uniform IF the displayed coefficient/jet bounds are uniform.
The S bound retains the original second metric time jets and theta_tR. This
does not establish their uniform time propagation. Nor does it establish
mesh-uniformity of the external source norm ||b||_K, whose nonzero endpoint
piece was precisely why the memory correction was introduced.

## 10. Connection back to the external boundary-memory argument

There is no need to discard the earlier memory construction. Let A_N be the
normal-form block generator and J(t) beta=(0,B(t)beta). For the external
source b=B beta, the transformed forcing is (B beta,BTB beta), not (B beta,0).
Direct block multiplication gives the exact identity

    (B,BTB)=A_N J-J_t+(0,F_B).

The BTB terms cancel from the integration-by-parts defect; the same already
bounded F_B remains. If V(t,s) is the homogeneous normal-form propagator, the
zero-initial external response therefore has the conditional BV representation

    Y_beta(t)=V(t,0)J(0)beta(0)-J(t)beta(t)
        +integral_0^t V(t,s)(0,F_B(s)beta(s)) ds
        +integral_(0,t] V(t,s)J(s) d beta(s).

For a continuous coefficient path and right-continuous BV beta, let
P(t,s)=exp(integral_s^t Gamma_N/2). In the moving energy norm this implies

    ||Y_beta(t)|| <= P(t,0)b_star(0)|beta(0)|+b_star(t)|beta(t)|
       +integral_0^t P(t,s)f_star(s)|beta(s)| ds
       +integral_(0,t] P(t,s)b_star(s) d|beta|(s).

This algebraic corollary uses the retained transformed source from the
preceding checkpoint, not a new integration run. Beta's actual uniform BV
bound is STILL unproved. Three samples give neither its total-variation
upper bound nor a reason to set its time derivative to zero. The present
result closes the missing homogeneous-propagator input to this argument,
conditional on the coefficient/jet hypotheses; it does not close its source
or parent-persistence inputs.

## 11. Validation, useful evidence and limitations

The exact inequalities above, rather than a fit to refinements, supply the
mesh-independent statements. Tests check the original weak matrix identity,
the 3h/30 multiplication estimates, Gram product commutator, value-jump
projection, centered transport norms and the completed conditional growth
formula. Original trajectories are unchanged.

For the spatially linear manufactured clock .001(R-6), actual measured values:

|Intervals|GR ||E||M/h|Gram ||E||M/h|GR ||E||M-to-K|Gram ||E||M-to-K|
|---|---:|---:|---:|---:|
|16|.000110405|.000458200|.000460828|.00119964|
|32|.000109886|.000465957|.000460631|.00121309|
|64|.000109853|.000469061|.000460586|.00121885|
|128|.000109836|.000469811|.000460564|.00122148|

These are consistent with the derived h scaling; four meshes alone are not
its proof. The manufactured positive and negative constant-clock cases
recover exactly .005 and 0 for the nonnegative growth bound in both branches.

Projection controls include a smooth quadratic, a fixed value jump at a
scalar node, a fixed value jump at a mass face, and a mesh-scaled sawtooth.
For a fixed jump J_h grows as h^-1/2, as it SHOULD. For the sawtooth with h-sized
jumps at every internal scalar node, J_h=sqrt(length-h) is uniformly bounded.
No discontinuity was silently treated as continuous input.

Actual final saved states:

|Intervals/branch|Measured normal growth|Derived conditional upper|
|---|---:|---:|
|16 GR|.000165270|679.035|
|16 Gram|.000261683|2357.668|
|32 GR|.000218391|672.914|
|32 Gram|.000292720|2331.485|
|64 GR|.000235703|670.829|
|64 Gram|.000338923|2325.572|

The huge slack is retained openly. These conservative floating-point
evaluations are not interval-certified numerical enclosures. They must NOT
be used as evidence for fast physical growth, nor replaced by the measured
small rates in a future rigorous persistence argument. Sharper constants or
a more direct bound on the projected product will be needed for useful
quantitative evolution estimates.

## 12. Next target and reproducibility

The next derivation should address the ACTUAL external beta variation, with
its original source formula, released-slope law, Gram/quadrature remainder
and endpoint histories. Derive any needed higher parent jet from the equations
rather than supplying an arbitrary smoothness assumption or using sampled
variation as an upper bound. Parent coefficient/clock-jet propagation and
quantitative box persistence also remain necessary. The new D0 estimate and
normal-form construction need not be rediscovered or relabeled missing.

Authoritative new files:

- `scripts/annular_regular_transport_bound_20260910.py`
- `scripts/derive_annular_regular_transport_bound_20260910.py`
- `source-intake/navier-stokes/20260910/annular-regular-transport-bound-attempt02/status.json`
- `source-intake/navier-stokes/20260910/annular-regular-transport-bound-final-integrity.json`

The successful derive phase finished at 2026-09-10T01:54:47Z. Use attempt02
for the seal phase. It owns all inherited hashes, the new note and a resume
snapshot. Completed evidence must not be overwritten on rerun.

The first attempt stopped on a JSON serialization defect in an inherited
SymPy BooleanTrue certificate. Its source, first artifact and stale status
are preserved, with an explicit failure note; no worker remains active there:
`source-intake/navier-stokes/20260910/annular-regular-transport-bound-derived/FAILED-NOTE.md`.
The correction converts certificate truth values to Python bool. It did not
alter a mathematical inequality or an input trajectory.

All scripts compile without bytecode caches. One single-core BelowNormal
Python worker at a time, BLAS/OMP threads set to one, no subagents, shared
process shutdowns, Git action or new physical evolution. Protected workbench
verification is an mtime scan since 2026-09-10T01:42:00Z, not a full pre-turn
hash baseline.
