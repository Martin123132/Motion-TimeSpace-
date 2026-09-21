# Exact finite-width curvature and coupled energy

2026-09-17. Private continuation of
`DERIVATION-20260917-source-trace-law-and-causal-refinement.md`.

## 1. Outcome and scope

The failed endpoint-jet approximation is replaced by an independently qualified
finite-width curvature identity. It reproduces the original source-row Gram
force, including its sign. Nothing in the action or original force is changed.

The same calculation also gives a weaker sufficient spatial regularity
condition: piecewise C2 with a uniform curvature modulus is enough for
instantaneous extra-Gram force consistency. Uniform C3/C5 is unnecessary for
that particular statement.

For the coupled dynamics, a positive shifted Jacobi energy and its exact
off-solution evolution are derived. The principal Hamiltonian stiffness cancels.
A conditional uniform linear estimate follows from stated reference-path
regularity and nondegeneracy conditions. Those conditions have NOT been proved
for the full parent theory or an evolving continuum solution.

The nonlinear energy-only Taylor shortcut is unsuitable for a uniform limit:
its mixed source-position/field derivative loses a spatial derivative. This
occurs in the reference branch as well as MTS. It is not a physical instability
test or a rejection of either branch.

This is a prescribed-flat-background spherical finite-action calculation,
not the full GR limit. No empirical pass, local-GR recovery, complete parent
action, or solved black-hole problem follows. The previous physical GR-force
gates remain false. No future finite trajectories were needed for this stage.

## 2. Exact curvature functional, including rounded coordinates

Let x_i = xi_i-anchor be the actual free nodal coordinates. For one row a_i
of the unchanged lifted Gram factor, define

    m_- = sum_{x_i<0} a_i x_i,     m_+ = sum_{x_i>0} a_i x_i,
    K_-(s) = sum_{x_i<=s<=0} a_i(s-x_i),
    K_+(s) = sum_{0<=s<=x_i} a_i(x_i-s).

For U(0)=0, twice integrating separately on each side gives EXACTLY

    sum_i a_i U(x_i)
      = m_- U'_-(0) + m_+ U'_+(0)
        + integral_{s<0} K_-(s) U''_-(s) ds
        + integral_{s>0} K_+(s) U''_+(s) ds.                 (1)

The formula also holds for one-sided W2,1 functions with derivative traces.
The ideal stencil annihilates the two linear slopes, but actual floating
coordinates leave tiny m_-/m_+. They are retained, not silently set to zero.
No pointwise third or fifth derivative enters (1).

K is piecewise affine. Its absolute integral is computed exactly on each
segment, splitting at a sign change analytically. Thus

    |q_row| <= |m_- U'_-| + |m_+ U'_+|
               + ||K_-||_1 ||U''_-||_infinity
               + ||K_+||_1 ||U''_+||_infinity.             (2)

The implementation uses actual row coefficients and coordinates, not a
handwritten ideal stencil. Independent checks use piecewise quintics and
rapid trigonometric oscillations. For the saved GR reference, curvature is
obtained by differentiating the characteristic Chebyshev expansion once;
Gauss-Legendre quadrature integrates it against K, interval by interval.
The comparison target uses the independently saved nodal primitive projection.
Orders degree/2+1 and degree/2+9 integrate the polynomial product exactly in
exact arithmetic. Floating results are not interval certificates.

### Results on the already completed GR references

Degrees512/768, grids257/513/1025, all81 saved times, seven source rows each:

- largest absolute row-factor discrepancy:2.94610e-17;
- largest independent quadrature-order change:1.69407e-21;
- largest source-force discrepancy:7.65381e-13;
- no original force has been replaced by this reconstructed diagnostic.

At degree768, grid1025, T=.21:

|Calculation|Source-row Gram force|
|---|---:|
|Original action|+9.46518143618e-6|
|Finite-width curvature identity|+9.46518129099e-6|
|Previously rejected constant-curvature shortcut|-9.05950314566e-6|

The sign problem belonged to the endpoint truncation, not to this exact
representation. This is internal identity verification, not new experimental
evidence. Absolute curvature bounds still overestimate the signed result.
For example the fine degree768 largest row factor is2.97689e-9 versus a
curvature-only absolute bound3.39864e-7.

## 3. Spatial consistency needs less smoothness

This section concerns ideal arithmetic and the previous shape-regular dyadic
family: each source-adjacent element length ell_- and ell_+ lies in [h/40,h/10].
Assume U is one-sided C2, U(0)=0, uniformly bounded slopes and curvatures,
and a common curvature modulus omega(delta) -> 0 within each side.
Curvature may jump at the source.

The right P2 endpoint derivative has curvature kernel

    k_ell(s) = 1-3s/ell       for 0 <= s <= ell/2,
             = s/ell-1       for ell/2 <= s <= ell.

Its integral is zero and its absolute integral is ell/3. Reflection gives
the left counterpart. Consequently

    |J_h U - (U'_+ - U'_-)|
      <= [ell_- omega(ell_-) + ell_+ omega(ell_+)]/3.      (3)

For a bulk third difference not crossing the source,

    D3 U(x) = integral_0^h integral_0^h
                  [U''(x+h+s+t)-U''(x+s+t)] ds dt,

so |D3 U| <= h^2 omega(h). For each of the finitely many crossing rows,
subtract the exact linear hinge and bound the remaining nodal values by
M2 |x|^2/2. Their third differences are O(h^2 M2).

Using the already derived ||T|| <= 1/sqrt(8), G=T D3, ||G x_+||=O(h),
and (3), the entire lifted factor satisfies

    Q_h = ||Gtilde U||_2
         <= C1 h^(3/2) omega(h) + C2 h^2 M2
               + C3 h^2 omega(h).                        (4)

Constants include the fixed domain length and cut-phase bounds, not h.
The previously derived mass and kinetic-Cauchy estimates then give

    |F_Gram| <= C [h^(-3/2) Q_h + h^(-1) Q_h^2]
              <= C' [omega(h)+sqrt(h)+h^2 omega(h)^2+h^3]
              -> 0.                                     (5)

This is same-state, instantaneous extra-force consistency. It is NOT a
bound on evolved force discrepancies or a regularity/existence theorem.
For a fixed one-sided C2 function on compact intervals, a modulus exists;
for a sequence of reference polynomials, a COMMON modulus still needs proof.
Finite polynomial fits do not supply it automatically.

The new manufactured test includes a |x+.247|^(5/2) term. Its curvature is
Holder1/2 and its third derivative is unbounded at the interior cusp. All
seven grids33..2049 satisfy the explicit (4) bound. Measured Q_h/h^2 ranges
from.09319 to.10994. This exercises a case not covered by a uniform C3
hypothesis, without asserting that the physical reference has this regularity.
Floating tests allow3e-13 arithmetic slack; they do not prove arbitrary
machine-precision refinement. Formula (1) retains floating slope moments.

## 4. Coupled Legendre transform from the actual action

Write configuration X=(U,b), velocity W=(v,V), c=A(b)U, and

    L = v^T M v/2 + V v^T A U + V^2 U^T B U/2
        - U^T K U/2 - m sqrt(1-V^2),
    K = K_bulk + Gtilde^T D_h Gtilde.

All matrices and source-map derivatives are those of the unchanged action.
Let H=L_WW, C=L_WX, D=L_XX. Here H is the kinetic Hessian; the Hamiltonian
is denoted mathcal-H below to avoid confusing these two objects.

    H = [[M,c],[c^T, mu+U^T B U]],  mu=m/(1-V^2)^(3/2),
    s_H = mu+U^T B U-c^T M^-1 c >= mu > 0.

The inequality is kinetic Cauchy-Schwarz. The Legendre map
Tmap(X,W)=(X,L_W) has derivative

    T = [[I,0],[C,H]],
    Q = Hessian(mathcal-H)
      = [[-D+C^T H^-1 C, -C^T H^-1],[-H^-1 C,H^-1]].     (6)

No representative-dependent term or source mode is discarded. Source speed
is kept timelike. Q itself need not be positive in the free position b.
For constant beta, let e select the canonical b coordinate and set

    Wc = Q + beta e e^T,
    T^T Wc T = diag(P,H),  P=-D+beta e_b e_b^T.           (7)

This is the shifted Jacobi energy, not a new potential in the physical action.
The shift appears only in the comparison norm.

Its field block is

    P_UU = K - V^2 B >= (1-V^2) K_bulk + Gtilde^T D_h Gtilde.

The inequality follows from |source-map displacement|<=1 in the flat chart.
The anchor Dirichlet condition removes the constant field mode on each side.
P is positive precisely when, in addition to P_UU>0,

    beta > D_bb + D_bU P_UU^-1 D_Ub.                     (8)

H is already positive. Thus (7)-(8) give an explicit, testable coupled norm.
The numerical qualification fixes beta=1 throughout; it does not tune beta
per time sample or omit a beta-dot term from a varying shift.

## 5. Off-solution reference correction and stiff cancellation

Let z(t) be the reconstructed reference path in velocity coordinates,
F the original finite-action flow, r=F(z)-zdot, and A=DF(z).
The independent causal predictor uses eta'=A eta+r.
Because z is NOT an exact finite-action solution, its Legendre-transformed
perturbation xi=T(z)eta satisfies

    xi' = Ac xi + T r,
    Ac = J Q - B_r,
    B_r = (DT(z)[r]) T^-1.                              (9)

This follows by differentiating T F = J grad(mathcal-H) with respect to z.
Using Ac=JQ alone would be wrong off solution. The reference derivative is
the actual derivative of the chosen path, not substituted by F(z).
The passive clock is separated because it does not feed back into F.

For E=xi^T Wc xi/2,

    E' = xi^T S xi/2 + xi^T Wc T r,
    S = Qdot + beta(ee^T JQ-QJee^T) - Wc B_r-B_r^T Wc.   (10)

The dangerous QJQ contribution cancels EXACTLY. One need not estimate the
large wave frequency by an absolute norm of DF.

With lambda=max eig(S,Wc) and R=sqrt(2E),

    R' <= lambda R/2 + ||T r||_Wc.                       (11)

For continuous valid coefficients, integrating (11) gives the usual
exponential weighted forcing integral. Three sampled times are NOT an
integral bound or a supremum over the full time interval.

An independent velocity-coordinate form is useful. For any matrix-valued
function B(z), write B_F=DB[F(z)], B_zdot=DB[zdot]. Then

    T^T S T = [[-D_zdot, beta E_b-C_F^T],
               [beta E_b-C_F, H_zdot-2 H_F]].            (12)

Here E_b is the configuration-space source projector. This formula contains
all moving-geometry terms and is qualified against (10), not postulated.

### Conditional uniform linear lemma

A sufficient set of hypotheses on a family of reference paths is:

1. Source-map Jacobians bounded above/below, positive inner radius, and
   |V| <= Vstar < 1 uniformly; fixed m>0 and fixed cut-phase bounds.
2. U, v, and the reference derivative of U have uniformly bounded one-sided
   H1 norms; the reference derivative of v has a uniform mass-L2 norm.
   Reference bdot and Vdot are bounded.
3. F(z)'s field acceleration has a uniform mass-L2 norm, and its source
   acceleration is bounded. These are explicit regularity hypotheses, not
   assumed consequences of a small pointwise force error.
4. One constant beta gives a positive margin in (8), uniformly.

Under these hypotheses, (12) is bounded by a constant times (7), with that
constant independent of h. Reason: the weights and their source-position
derivatives through third order have uniform relative bounds. The Gram
form is H1-bounded uniformly: original vertex differences are integrals of
U_x; the lifted trace uses ||g||=O(h) and the P2 inverse endpoint estimate
|J_h U| <= C h^(-1/2)||U_x||. With the D_h=O(1/h) weight these factors cancel.
All mixed terms in C_F involve at most an L2 field acceleration paired with
one H1 variation, or one bounded source acceleration. Terms in D_zdot and
H_zdot use exactly the reference norms listed above. Cauchy-Schwarz and the
positive margins in (7)-(8) therefore bound every block of (12).

Coercivity of H also has a uniform quantitative route: completing its square,

    deltaW^T H deltaW
      = ||delta v+M^-1 c delta V||_M^2+s_H(delta V)^2.

If c^T M^-1 c<=C_U, then
||delta v||_M^2+(delta V)^2 is at most
max(2,(2C_U+1)/m) times this quadratic form. P follows similarly by its
field/source Schur complement. No h-dependent Euclidean coercivity is used.

Thus a conditional linear stability result is derived, rather than replacing
it by ||DF||=O(h^-2). This does not establish the hypotheses for a continuum
solution, a nonlinear perturbed solution, or a full MTS-to-GR limit.

## 6. Nonlinear remainder: retained, and the crude route rejected

For an exact solution y and delta=y-z, the transformed difference xi=T(z)delta
obeys (9) with the additional term T N, where

    N=F(z+delta)-F(z)-DF(z)delta.

Equations (10)-(11) hold with the additional ||T N||_Wc. At each fixed finite
mesh, a local Hessian bound could give ||T N||_Wc <= L_h R^2/2. It is NOT
legitimate to suppose L_h is uniform in the basic energy norm.

At the zero-field, stationary-source state, the mixed source-position/field
derivative of field acceleration is exactly

    D_b D_U F_v[1,u]
      = M^-1 M_b M^-1 K u - M^-1 K_b u.                 (13)

For a highest-frequency mode normalized by u^T K u=1, (13) grows with its
wave frequency. The same principal effect is already present in the continuum
wave operator: differentiating sigma(b)^-2 partial_x^2 with respect to b
maps an H1-normalized high-frequency wave to an L2 norm proportional to its
frequency. Therefore the elementary energy-only second-derivative argument
loses a spatial derivative. This is a limitation of that argument, not a
demonstration that the energy grows uncontrollably.

|Grid|Reference mixed norm|MTS mixed norm|
|---|---:|---:|
|33|7.84942e3|7.20826e3|
|65|2.91254e4|3.94434e4|
|129|2.91280e4|2.66667e4|
|257|1.25580e5|1.72261e5|

Both direction norms are one. Mixed-norm/frequency stays about2.04..2.60;
independent central-source/complex-field derivative checks agree within
1.36e-9 relative error. Changing cut phase explains nonmonotonic intermediate
entries; four meshes are not an asymptotic proof. The continuum principal
operator explains why a uniform naive quadratic bound is the wrong target.

The appropriate nonlinear continuation is a relative/quasilinear energy that
keeps the changing principal operator inside the energy, or a justified
stronger regularity estimate. Merely increasing the scalar L_h is not a
uniform convergence proof. A completed relative-energy theorem is NOT claimed
in this checkpoint.

## 7. Output duality and the exact Gram adjoint forcing

For force f, its linear energy-dual norm is

    ||Df||_{diag(P,H)^-1}.

It is finite on each grid but does not have a demonstrated uniform bound.
At T=.21 the reference/MTS values are:

|Grid|Reference|MTS|
|---|---:|---:|
|33|2.91205|7.26757|
|65|4.88193|19.53438|
|129|5.73120|14.10022|
|257|10.24466|40.84654|

Clock-rate dual norms remain about.33644. Clock is a passive integral with
delta clock'=sqrt(1-V_y^2)-sqrt(1-V_z^2); on |V|<=Vstar its absolute rate
difference is at most Vstar/sqrt(1-Vstar^2) times |delta V|.
No full-interval clock error certificate is claimed from the table.

There is a useful exact simplification for the force adjoint. Reference and
MTS have the SAME kinetic Legendre map. At the same state, their canonical
flow difference is just the extra potential covector:

    T(F_MTS-F_reference)
      = (0_configuration, -Gtilde^T D_h q, -q^T D_h,b q/2),
    q=Gtilde U.                                          (14)

Hence for any canonical adjoint p,

    p^T T(F_MTS-F_reference)
      = -(Gtilde p_PU)^T D_h q - p_Pb q^T D_h,b q/2.       (15)

This removes the artificial mass-inverse amplification from the forcing
pairing. It does not delete any Gram row. Inserting (1) gives an explicit
finite-width curvature forcing for the adjoint, retaining signs and phase.
An absolute instantaneous bound is the product of the corresponding weighted
Gram norms plus the source quadratic term, but may be much looser than the
signed time integral.

For a backward adjoint -p'=Ac^T p with terminal condition Df T^-1, the linear
response is its initial-error pairing plus integral p^T T r. Formula (15)
is one exact contribution to that integral. Changing branch ALSO changes
Ac, the terminal output, and any initial error; (15) alone is NOT the whole
difference between evolved branch predictions.

## 8. Qualification results and limits

Energy checks use GR degree768, grids33/65/129/257, both branches and times
0,.21,.4. All24 shifted metrics are positive at fixed beta=1. Growth rates
in (11), for squared energy before dividing by2, range6.22037..7.41847.
At T=.21 the values are:

|Grid|Reference lambda|MTS lambda|Reference forcing norm|MTS forcing norm|
|---|---:|---:|---:|---:|
|33|6.44776|6.72517|.0126894|.402827|
|65|6.44957|7.41847|.00491381|.954579|
|129|6.44963|6.53034|.00162639|.228292|
|257|6.44965|6.63560|.000581844|.415179|

These moderate sampled rates support trying the energy route; they are not
uniform-in-time or uniform-in-mesh certificates. MTS absolute forcing is
nonmonotonic and much larger than reference here. Its signed response can be
small without its absolute norm being small. Do not turn (11) with three
samples into a claimed force-error bound.

Smooth perturbation remainder ratios under amplitude halving are near1/4.
That checks the finite-mesh Taylor implementation only; section6 deliberately
tests the high-frequency directions that this benign probe misses.

Implementation and evidence:

- `scripts/annular_finite_width_curvature_20260917.py`
- `scripts/qualify_annular_curvature_kernel_20260917.py`
- `scripts/annular_canonical_energy_20260917.py`
- `scripts/qualify_annular_canonical_energy_20260917.py`
- `scripts/qualify_annular_energy_duality_20260917.py`
- `scripts/qualify_annular_energy_remainder_scaling_20260917.py`
- `source-intake/navier-stokes/20260914/annular-curvature-kernel-attempt01/status.json`
- `source-intake/navier-stokes/20260914/annular-canonical-energy-attempt01/status.json`
- `source-intake/navier-stokes/20260914/annular-energy-duality-attempt01/status.json`
- `source-intake/navier-stokes/20260914/annular-energy-remainder-scaling-attempt01/status.json`

54 kernel checks,193 energy checks,41 duality/regularity checks,16 mixed
derivative checks:304 successful implementation checks. They are not304
physics passes. No failed executed attempt was added in this stage. Earlier
25 failed attempts and original GR-force failures remain preserved.

## 9. Next concrete calculation

Use (14)-(15) to implement the full time-dependent force adjoint on a small
already-qualified grid first. Verify its signed residual and initial-error
integrals against the existing forward causal response, using BOTH branches.
Keep the off-solution B_r term, moving geometry and all Gram rows. This is a
duality test, not a fitted force subtraction or a new physical prediction.

In parallel mathematically, derive the nonlinear relative energy with the
source-dependent principal operator inside the comparison energy, rather than
using the now-rejected uniform basic-energy Taylor remainder. Require the
result to control source motion, field gradients and output traces; retain
the actual continuum regularity obligations. No full-time adjoint has yet
been run, and no additional expensive trajectory grid is called for.
