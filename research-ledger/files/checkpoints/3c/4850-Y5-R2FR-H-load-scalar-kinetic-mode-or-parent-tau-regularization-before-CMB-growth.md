# 4850 Y5 R2FR H-load scalar kinetic mode and complete flow constraint

**Status:** The 4849 scalar/vector question is now resolved for the action actually varied in 4847. The apparent negative scalar coefficient obtained from an ADM trace-only reduction is not a physical ghost eigenvalue: that reduction omits the unit-flow Euler equation (D_mu G_	heta=0). Keeping the complete constraint set gives a local Legendre transform to a cuscuton-type action with no extra propagating scalar. The fitted positive branch also has the correct longitudinal elliptic sign, (-G_{	heta	heta}>0), while its homogeneous constraint remains invertible for (f_K<1). The SH0ES edge is still a real approach to a constraint degeneracy and remains nonclaim.

**Decision:** `POSITIVE_H_LOAD_MINIMAL_FLOW_CUSCUTON_EQUIVALENCE_DERIVED_NO_EXTRA_SCALAR_LONGITUDINAL_ELLIPTIC_SIGN_PASSES_FITTED_BRANCH_EDGE_DEPENDENCE_AND_SHARED_PARENT_TAU_MATRIX_REMAIN_PRIVATE_NONCLAIM`.

## 1. Do not drop the flow Euler equation

The 4847 action is

\[
S_{\rm mem}=-\frac1\kappa\int d^4x\sqrt{-g}
\left[G(\theta)+\lambda_u(u^\mu u_\mu+1)\right],
\qquad
\theta=\nabla_\mu u^\mu.
\]

Define

\[
\phi:=G_\theta.
\]

Variation of the unit flow gives

\[
\boxed{\nabla_\mu\phi=2\lambda_u u_\mu},
\qquad
\boxed{D_\mu\phi=0}.
\]

This is a local constraint, not an optional background equation. A calculation that substitutes (u) as a foliation normal, eliminates the shift, and omits this equation changes the theory.

## 2. Exact Legendre/cuscuton equivalence

On a patch where

\[
g:=G_{\theta\theta}\ne0,
\]

define the Legendre transform

\[
U(\phi)=\phi\theta-G(\theta).
\]

Then

\[
U_\phi=\theta,
\qquad
U_{\phi\phi}=\frac1{G_{\theta\theta}}=\frac1g.
\]

Up to a boundary term, the memory action is exactly

\[
S_{\rm mem}=\frac1\kappa\int d^4x\sqrt{-g}
\left[u^\mu\nabla_\mu\phi+U(\phi)
-\lambda_u(u^2+1)\right].
\]

When (\nabla_\mu\phi) is timelike, the (u) equation aligns the flow with it:

\[
u_\mu=\sigma\frac{\nabla_\mu\phi}
{\sqrt{-\nabla_\alpha\phi\nabla^\alpha\phi}},
\qquad \sigma=\pm1.
\]

Eliminating (u) gives

\[
\boxed{
S_{\rm mem}=\frac1\kappa\int d^4x\sqrt{-g}
\left[\sigma\sqrt{-\nabla_\mu\phi\nabla^\mu\phi}+U(\phi)\right]
}
\]

on that orientation branch. This is the cuscuton kinetic form. It imposes a mean-curvature constraint and carries no independent propagating scalar on a cosmological background. The general no-extra-mode property of this kinetic form and the necessity of treating its perturbations through the full constraints are documented in [Quintin and Yoshida, *Cuscuton gravity as a classically stable limiting curvature theory*](https://arxiv.org/abs/1911.06040/).

## 3. Why the naive ADM ghost test is wrong

If (u) is prematurely replaced by a hypersurface normal and its Euler equation is discarded, the trace Hessian gives

\[
Q_{\rm naive}=\frac{2(2+3g)}g.
\]

Using 4849,

\[
g=-\frac23f_K,
\]

so (Q_{\rm naive}<0) for (0<f_K<1). This is not a physical eigenvalue. It is the Schur complement after eliminating the shift while leaving out the lapse/(\phi)/flow constraints that remove the memory scalar.

The quickest consistency check is the Legendre form. In unitary gauge for (\phi), the square-root term is linear in the lapse cancellation and has no quadratic (\dot{\delta\phi}^{,2}) term. The (\phi) equation is elliptic/constraint-like rather than a second propagating wave equation. Therefore

\[
\boxed{N_{\rm scalar}^{\rm memory}=0}
\]

for the minimal independently varied unit-flow branch.

This does not automatically certify a different branch in which a propagating parent coframe/time field contributes its own kinetic Hessian. That shared-parent branch must be diagonalized as a combined system.

## 4. Principal longitudinal sign

On a local inertial patch, hold the metric background fixed and perturb the spatial flow. At linear order,

\[
\delta\theta=\partial_i\delta u^i.
\]

The quadratic memory density is

\[
\boxed{
\mathcal L^{(2)}_{\rm mem}
=-\frac{g}{2\kappa}
(\partial_i\delta u^i)^2.
}
\]

The longitudinal constraint is coercive when

\[
\boxed{-g>0}.
\]

For the positive kinetic-fraction branch,

\[
-g=\frac23f_K>0.
\]

Thus every nonzero fitted positive-(H)-load row has the correct isolated longitudinal elliptic sign at (z=0). The memory term has no transverse-vector wave and does not alter the tensor principal block:

\[
Q_T=1,
\qquad
c_T^2=1.
\]

## 5. Constraint margin of the fitted branch

The homogeneous background Jacobian remains

\[
\mathcal K_0=6+9g=6(1-f_K).
\]

Therefore the fitted branch simultaneously has

\[
0<f_K<1
\Longrightarrow
-g>0,
\qquad
\mathcal K_0>0.
\]

All twelve fitted rows pass these two principal conditions at (z=0). This does not make the SH0ES signal stable evidence:

- broad SH0ES still selects (f_K=0.95), leaving only (5\%) of the homogeneous margin;
- strict SH0ES still selects (f_K=0.80);
- no-SH0ES still does not select the model after AIC/BIC;
- matter-coupled lapse, shift and cuscuton constraints have not yet been reduced into a growth kernel.

The correct reading is now sharper: the edge is a constraint-conditioning problem, not a demonstrated propagating ghost.

## 6. Local endpoint and patching

At the stationary local fixed point,

\[
G=G_\theta=G_{\theta\theta}=0.
\]

The Legendre map is singular there because (g=0). This does not invalidate the original action. It means the cuscuton chart is a cosmological (g\ne0) chart, while the local branch must be described in the original (u,Q,\Lambda) variables. In those variables the memory stress and tau force vanish exactly, and the parent EH/coframe sector owns local propagation.

The remaining global burden is to show that the original-variable local branch and the cosmological Legendre patch belong to one regular parent solution without a strong-coupling transition.

## 7. Branch decision

The positive (H)-load is **not** demoted by the scalar principal calculation. Instead:

1. retain the minimal independently varied unit-flow branch as a cuscuton-equivalent, no-extra-scalar private candidate;
2. retain the 4849 SH0ES result only as an edge-dependent empirical lead;
3. forbid the incomplete (Q_{\rm naive}) ghost diagnosis;
4. keep any propagating shared-parent tau/coframe completion as a separate branch needing its own matrix;
5. derive the matter-coupled scalar constraints and effective growth/Poisson kernel before CMB or growth likelihoods.

This is real forward movement: the parent (u)-equation supplies the missing mechanism rather than an added closure term.

## 8. Machine evidence

- `P8_Y5_R2FR_4850_ADM_KINETIC_MATRIX.csv`
- `P8_Y5_R2FR_4850_FIT_STABILITY.csv`
- `P8_Y5_R2FR_4850_REGULARIZER_GATE.csv`
- `P8_Y5_BRR545_4850_VALIDATION.csv`

All rows remain `valid_for_claim=false` until the matter-coupled perturbation system, patch transition and same-frame parent ownership close.

## 9. Next target

`4851-Y5-R2FR-H-load-cuscuton-matter-perturbation-constraint-and-growth-kernel.md`
