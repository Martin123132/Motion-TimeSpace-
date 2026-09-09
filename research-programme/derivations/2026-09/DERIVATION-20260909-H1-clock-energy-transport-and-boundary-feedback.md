# Energy transport with an H1 clock, including the actual Gram and boundary terms

Date: 2026-09-09. Private canonical annular continuation.

## 1. The advance and its limit

The previous step controlled theta_R in L2, whereas the old scalar energy
argument required it in infinity norm. That mismatch is now resolved for
the ACTUAL weighted free Hermite projection and both bulk/Gram stiffness
transport operators. The proof does not replace L2 by a stronger norm.

The resulting boundary-adapted energy inequality is explicit and uniform
in mesh spacing, conditional on its coefficient/source inputs. The change
from raw graph energy to boundary-adapted energy also has a derived
absorption gate, satisfied on all 18 saved states with feedback about
0.03364 for GR and 0.08354 for Gram at the final saved time.

One temporal input remains unclosed: T2=||theta_t||_Q, the L2 norm in the
actual positive quadrature. It enters the second derivative of the mass
coefficient in the unchanged boundary driving. This step evaluates T2
from the owned exact second jets; it does NOT derive a uniform time bound
on T2. Nor does it propagate the configuration box or full shift constraints.

The constants are extremely conservative. This is a structural energy
estimate, NOT a useful certified evolution interval yet, and not evidence
of physical growth, instability, horizon regularity or complete MTS-to-GR recovery.

## 2. Source owners and reproduction

Previous spatial/inner-flux bounds:
`DERIVATION-20260909-clock-spatial-gradient-and-derived-coefficient-input.md`.
Raw/adapted energy and physical boundary histories:
`DERIVATION-20260909-first-derivative-graph-energy-and-boundary-forcing.md`,
`scripts/annular_first_derivative_energy_20260909.py`,
`scripts/annular_boundary_adapted_energy_20260909.py`.
Existing elliptic comparison and H2 bound:
`DERIVATION-20260909-mesh-uniform-coefficient-and-boundary-source-bounds.md`,
`DERIVATION-20260909-metric-flux-cancellation-and-exact-constraint-jets.md`.
Exact second jets:
`scripts/annular_metric_flux_jets_20260909.py`.

New helper and runner:
`scripts/annular_H1_clock_energy_20260909.py`,
`scripts/derive_annular_H1_clock_energy_20260909.py` (derive/seal).
Results:
`source-intake/navier-stokes/20260909/annular-H1-clock-energy-derived/status.json`.
Final integrity:
`source-intake/navier-stokes/20260909/annular-H1-clock-energy-final-integrity.json`.

The runner uses one single-core BelowNormal process, python -B, the same
18 saved canonical states, and 16 manufactured operator tests. No new
trajectory, boundary condition, action term or physical residual replacement
is introduced. Old d, d_t and full shift covectors are retained.

## 3. Assumptions and spaces

Use the same canonical branch b2=b3=m_chi=Lambda=0 on the old positive box.
V_h is the actual C1 cubic Hermite space with zero scalar endpoint values;
all slope coordinates remain free. Q is the owned positive composite Gauss4
rule, exact for unweighted cubic products, but not assumed exact for
arbitrary weighted products. The scalar matrices are

    M(v,w)=Q[m v w],
    K(v,w)=Q[p v_R w_R]+G_h(v,w),
    M_t(v,w)=-Q[m theta v w],
    K_t(v,w)=Q[p theta v_R w_R]+G_h,p*theta(v,w).

Here m=R^2/(N sqrt(F)), p=R^2 N sqrt(F), theta=partial_t log(N sqrt(F)).
Assume positive coefficient bounds m_-,m_+,p_-,p_+, spatial Lipschitz
constant L_p, and theta in H1. Let eta=theta-theta0, delta>=||eta||_infinity,
H>=||theta_R||_2 and Theta=|theta0|+delta. The previous step supplies the
spatial and inner-flux inputs within the canonical configuration box.

## 4. A constructive H1-stable weighted projection

For any f in H1 with zero endpoint values define J_h f from its nodal
values, with derivative ZERO at every node. On a cell its formula is

    J_h f=f_left+(f_right-f_left)(3t^2-2t^3),  t=(R-R_left)/h.

It belongs to the SAME free cubic space; zero slopes here specify an
auxiliary interpolant, not new physical boundary or evolution conditions.
Since integral_0^1 [6t(1-t)]^2 dt=6/5,

    ||(J_h f)_R||_2 <=2||f_R||_2.

An H1 function and this convex nodal interpolant each differ from the
left-endpoint value by at most sqrt(h)||f_R||_cell. Consequently

    ||f-J_h f||_Q <=2h||f_R||_2.

Let Pi_m be the ACTUAL Q[m . .] orthogonal projection onto V_h.
Contractivity, positivity and the exact polynomial inverse16 bound give

    ||[Pi_m f-J_h f]_R||_2
       <=32 sqrt(m_+/m_-)||f_R||_2,
    ||[Pi_m f]_R||_2<=C_Pi||f_R||_2,
    C_Pi=2+32sqrt(m_+/m_-).

Only after an approximation error proportional to h exists is an inverse
h used. The resulting constant contains no inverse mesh power and requires
no pointwise bound on f_R.

Since ||u||_infinity<=sqrt(ell)||u_R||_2 for u in V_h,

    ||(eta u)_R||_2<=(delta+sqrt(ell)H)||u_R||_2.

With G0=2p_+ for Gram and zero for GR, coercivity gives

    ||M^-1 M_t||_(K->K) <= B_A,
    B_A=|theta0|+sqrt((p_++G0)/p_-) C_Pi (delta+sqrt(ell)H).

This is a full operator bound, not just a sampled symmetric growth rate.
When theta is spatially constant, splitting off theta0 recovers exactly
B_A=|theta0| rather than charging for an artificial interpolation error.

## 5. H2 elliptic control turns stiffness transport into an L2 source

For u=K^-1 M g, reuse the prior quadrature-plus-Gram elliptic comparison.
Writing C1=ell/p_-, C2=(1+L_p C1)/p_-,

    C_I=C1+2ell C2,
    C_e=[2p_+ C2+2L_p C_I+(G0/sqrt(3))C2]/p_-,
    D1=sqrt(m_+)ell/p_-,
    D2=(m_+/sqrt(m_-))(4C2+16C_e),
    D_infinity=D1/sqrt(ell)+sqrt(ell)D2,

the established estimates imply

    ||u_R||_2<=D1||g||_M,
    ||u_RR||_2<=D2||g||_M,
    ||u_R||_infinity<=D_infinity||g||_M.

No third spatial derivative is assumed. The H2 bound uses the continuous
elliptic comparison only as an estimate device; the finite action is unchanged.

For a continuous H1 flux k and cubic test v, subtract a cell constant from
k before estimating the quadrature error. Each quadrature/integral error
is <=h||k_R||_cell||v_R||_cell. Integration by parts and inverse16 then give

    |Q[k v_R]| <=(1+2*16)||k_R||_2||v||_2 =33||k_R||_2||v||_2.

Boundary terms vanish because the test values vanish at both endpoints.
Apply this with k=p eta u_R, for which

    ||k_R||_2 <= delta(L_p D1+p_+ D2)||g||_M
                     +p_+ H D_infinity||g||_M.

This is the decisive H1 product estimate: eta_R is paired with u_R in
infinity norm, which is supplied by elliptic H2 control, not assumed.

## 6. The actual Gram transport does not require a pointwise clock gradient

The owned factorization has ||R_template||_2<1/8. Its existing difference
estimates give

    ||T u|| <=sqrt(2/3) h^(3/2)||u_RR||_2,
    ||T v|| <=sqrt(2h)||v_R||_2.

Convex coefficient sampling and |p eta|<=p_+ delta imply

    |G_h,p*eta(u,v)|
       <=(2/sqrt(3)) p_+ delta h ||u_RR||_2||v_R||_2
       <=(32/sqrt(3)) p_+ delta ||u_RR||_2||v||_2.

Thus no unbounded nodal multiplier derivative or discarded Gram term is
hidden in the stiffness transport. Combining sections 5-6 yields

    ||M^-1 K_t K^-1 M||_(M->M) <= B_L,
    B_L=|theta0|+[33{delta(L_p D1+p_+D2)+p_+H D_infinity}
                       +I_G(32/sqrt(3))p_+delta D2]/sqrt(m_-).

Here I_G is one for Gram and zero for GR. Constant clock rescalings again
give B_L=|theta0| exactly. The bound is otherwise intentionally conservative.

## 7. Boundary-adapted energy and the remaining time input

Use the unchanged affine physical endpoint lift l(t), with l_t and l_tt
fixed by the existing quadratic histories. Let v=chi-l, z=v_t,

    F_b=-(M_full l_tt+M_full,t l_t+K_full l)_free,
    g_hat=M^-1(Kv-F_b),
    E_hat=one_half[z^T K z+g_hat^T M g_hat].

Differentiating the exact energy and rearranging Kv=M g_hat+F_b gives

    E_hat' <= G E_hat+sqrt(2E_hat)(B_L F0+F1+R_graph),
    G=max(2B_A+Theta,2B_L+Theta).

R_graph is the retained scalar-equation/nonlinear residual force in its
K-graph norm, not a favorable subtraction. The canonical exact scalar
equations make it zero; the runner retains its actual floating residual.

Explicit boundary bounds are, with all unmarked norms continuous L2,

    F0=sqrt(m_+)(||l_tt||+Theta||l_t||)
                            +33 L_p||l_R||/sqrt(m_-),
    F1=2sqrt(m_+)Theta||l_tt||
       +(m_+/sqrt(m_-))[Theta^2||l_t||+||l_t||_infinity T2]
       +(33/sqrt(m_-))[(L_p Theta+p_+H/sqrt(ell))||l_R||
                                      +L_p||l_tR||].

They bound ||F_b||_M* and ||F_b,t||_M*. The Gram parts annihilate the
affine lift even with variable time coefficients. The formula uses l_ttt=0,
which is the actual prescribed history, not an altered boundary condition.

The unresolved input is T2=||theta_t||_Q. It appears because

    m_tt=m(theta^2-theta_t),
    theta_t=N_tt/N-(N_t/N)^2-mu_tt/(RF)-2mu_t^2/(RF)^2.

The norm is explicitly the ACTUAL quadrature norm: no continuous L2 bound
on an arbitrary sampled function is silently assumed. A future second-metric
estimate can control it through the owned finite reconstructions. Here it
is only evaluated from the exact second jets, without finite differences.

## 8. Raw/adapted energy conversion is not assumed

The earlier metric bounds use the raw graph radius s=sqrt(2E_raw), whereas
this energy inequality evolves E_hat. Triangle inequality gives

    s <= sqrt(2E_hat)+||F_b||_M*.

The earlier positive source majorants admit
Theta<=Theta_offset+Theta_slope*s and
H<=H_offset+H_slope*s. These coefficients come from the explicit homogeneous
parts of the bound, not a fit to selected energy values. Norm subadditivity
justifies the affine majorants for every s>=0. Auxiliary zero boundary
arguments are used only to extract bound coefficients; physical data stay fixed.

Substitution in F0 gives F0<=a+b*s, where

    b=sqrt(m_+)||l_t|| Theta_slope,
    a=sqrt(m_+)||l_tt||+33L_p||l_R||/sqrt(m_-)
                                     +sqrt(m_+)||l_t||Theta_offset.

If b<1, then

    s <= [sqrt(2E_hat)+a]/(1-b).

This closes the conversion needed to express B_A and B_L in terms of the
adapted energy and known data. The gate is checked, not assumed universally:
all saved states pass, with final b=0.0336404 (GR), 0.0835445 (Gram).
The proof is conditional on this gate and the canonical box, not all
possible boundary histories. Linear-solve roundoff is tested numerically;
these results are not outward-rounded interval certificates for the roots.

## 9. Validation and size of the bounds

388/388 implementation/algebra checks pass: 18 unchanged canonical states
and 16 manufactured operator cases. The tests compare FULL matrix operator
norms, independently check the interpolant and weighted projection, verify
the inherited H2 constant, preserve the exact energy identity and retain
the actual boundary source and physical shift discrepancies.

The manufactured clock spike has nodal height sqrt(h) and width two cells.
Its derivative L2 norm is exactly sqrt(2), while its pointwise gradient
grows like h^(-1/2). It passes the new H1 estimates through N128 without
treating the growing pointwise derivative as uniformly bounded. Constant
rescaling controls reproduce both transport norms exactly as 0.003.

At final time on N64:

| Branch | B_A | B_L | T2, evaluated only | actual adapted energy rate | conditional rate upper bound |
|---|---:|---:|---:|---:|---:|
| GR | 101.591 | 7513.088 | 0.0016072 | 0.0307089 | 4690.691 |
| Gram | 634.136 | 51467.590 | 0.0015426 | 0.0307142 | 36214.086 |

These rate bounds are far too loose to certify the existing evolution span
as a practical stability result. They establish absence of an inverse-mesh
loss in this argument, not useful precision. In particular the larger Gram
majorant is not an observed instability or an empirical defeat of MTS.
Conversely, the finite observed energy rates do not prove a time-uniform
theorem or validate the full physical framework.

## 10. Next derivation

Derive a uniform bound on T2 from the actual second constraint/source
equations, retaining the physical inner-flux derivative, natural clock
boundary and Gram terms. Use the existing exact second jets as the equation
owner, not as a substitute for a bound. Prefer the weakest norm sufficient
for T2; do not demand pointwise control of every second derivative merely
because the old route did so.

Then insert that bound into the adapted-energy inequality, sharpen the
overconservative constants where needed, and prove persistence of the
configuration domain. If controlling T2 needs a higher scalar energy, derive
that hierarchy explicitly rather than importing an unstated regularity axiom.
Do not redo the now-derived H1 projection, Gram transport or energy conversion.

No GitHub action. Protected workbench check: mtime scan since
2026-09-09T21:36:00Z, not a full pre-turn hash baseline.
