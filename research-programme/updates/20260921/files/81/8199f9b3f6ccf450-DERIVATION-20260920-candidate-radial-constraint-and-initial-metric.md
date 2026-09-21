# Candidate-owned radial gravity and coherent initial metric

Private derivation and numerical checkpoint, 20 September 2026. No GitHub action.

**Result:** the two common-space MTS candidates now have radial metric equations derived from their own field action, the inherited polar gravity action, proper-clock source action, and retained boundary action. Both have a solved, coherent initial metric at physical time zero. This is an initial-data result on the untrapped, zero-shift spherical branch, not a coupled evolution or a full GR limit.

The successful derivation/control run has 59 checks; the successful initial-metric run has 68. These are implementation checks, not independent experimental confirmations. Three failed executions are retained and explained below.

## 1. Inputs and scope

This extends `DERIVATION-20260920-joint-candidate-spatial-refinement.md` and `DERIVATION-20260920-complete-frozen-candidate-and-source-response.md`. The preceding immutable seal is `source-intake/navier-stokes/20260914/annular-joint-candidate-refinement-final-integrity.json`.

Gravity and radial boundary terms are inherited from `DERIVATION-20260913-cross-cut-source-action-and-driven-initial-boundaries.md`; the continuous material collar and velocity-owned radial equations are documented in `DERIVATION-20260915-repaired-live-canonical-geometry-and-current.md`. The present calculation does not derive these assumptions from a completed covariant MTS parent theory.

Retained controls: kappa=0.1, source mass=0.03, inner mass=0.7, material width=0.02, and the original 15 material labels with degree-14 interpolation. These are normalized model inputs, not measured SI parameters or a derivation of Newton's constant. The field is represented exactly on the common 1094-DOF P2 space for this initial-data calculation. Both Gram extensions remain in play; neither is chosen because of a nicer-looking force.

## 2. Continuous material density, including both Jacobians

Write F=1-2 mu/r, U=sqrt(F), N=exp(ell), with F>0. At fixed physical radius define

\[
 A(r)=\int w(z)\chi_t(z,r)^2\,dz,\qquad
 B(r)=\int w(z)\chi_r(z,r)^2\,dz,\qquad
 w(z)=6(z+1/2)(1/2-z).
\]

The time derivative here is physical, including moving-coordinate transport, not merely the reference-nodal time derivative.

Let R_i(z)=R(xi_i,z) be the physical position of candidate reference knot xi_i, J_i=partial R/partial xi and Z_i=partial R_i/partial z. On the ordered maps tested here J_i,Z_i>0. For either candidate let

\[
 a_i(z)=\tfrac12\sum_f P_{fi}[H u(z)]_f^2,\qquad
 g(r)=\sum_{i:\,r\in R_i([-1/2,1/2])}
 \frac{w(z_i)a_i(z_i)}{J_i(z_i)Z_i(z_i)},\qquad z_i=R_i^{-1}(r).
\]

H and P are the preceding candidate's derivative factor and positive sampler; u denotes its field coordinates here, not the physical velocity. Their normalization is already included; no additional 1/h is inserted. The nodal action is therefore

\[
 -\int dz\,w(z)\sum_i \frac{r_i^2 N_iU_i}{J_i(z)}a_i(z)
 =-\int dr\,r^2NU\,g(r).
\]

The first Jacobian belongs to the physical spatial derivative/action coefficient; the second converts material-label integration into radial density. Losing either changes the action.

The code prepares the cancellation-sensitive H u factors with 64-digit decimal arithmetic before conversion to binary64 and material interpolation. It evaluates positive weighted squares without clipping. Bulk A,B are evaluated from the original P2 representation of the same fixed physical field, while its old Gram contribution is disabled and replaced by candidate g. No new motion is evolved using the old field operator.

For ordered source b(z), write sigma(r)=w(z_b)/b_z(z_b), z_b=b^{-1}(r), V(r)=b_t(z_b), and s=sqrt(N^2-V^2/F). Source terms vanish outside the collar. Physical fields and velocities, hence A,B,g,sigma,V, are held fixed in the following metric variations.

## 3. Action variation and radial constraints

With the inherited normalization the radial Lagrangian is

\[
 L=\frac{N\mu_r}{\kappa U}
   +\frac{r^2 A}{2NU}
   -NUr^2\left(\frac B2+g\right)-m_s\sigma s.
\]

Set

\[
 D=\frac{A}{2N^2F}+\frac B2+g,\quad
 a=\kappa m_s\sigma\,\frac{UN}{s},\quad
 b=\frac{\kappa m_s\sigma V^2}{rNF^{3/2}s}.
\]

Direct variation gives

\[
 \boxed{\mu_r=f_\mu=\kappa r^2FD+a},\qquad
 \boxed{\ell_r=f_\ell=\frac{\mu}{r^2F}+\kappa rD+b}.
\]

The independent symbolic calculation verifies the full Euler expressions:

\[
 E_N=\frac{\mu_r-f_\mu}{\kappa U},\qquad
 E_\mu=\frac{N}{\kappa U}\left(f_\ell-\frac{N_r}{N}\right).
\]

Removing all matter gives mu_r=0 and ell_r=mu/(r^2 F). Removing only g removes exactly kappa r^2 F g from the mass equation and kappa r g from the lapse equation. The complete expression agrees with the original radial RHS when supplied the same density inputs. This is reference reduction within the inherited polar action, not derivation of full GR from MTS.

### Boundary action is part of the calculation

Gravity variation supplies [N delta mu/(kappa U)] from inner to outer boundary. The inherited boundary action is

\[
 S_{\partial}=\int dt\left[-\frac{\mu_{\rm out}}{\kappa}
 +\lambda_{\rm in}(\mu_{\rm in}-m_{\rm in})\right],
\]

so

\[
 \mu_{\rm in}=m_{\rm in},\qquad
 N_{\rm out}=U_{\rm out},\qquad
 \lambda_{\rm in}=\frac{N_{\rm in}}{\kappa U_{\rm in}}.
\]

Outer clock normalization is enforced inside the simultaneous solve. With physical velocities fixed, lapse-dependent matter loading forbids solving first and rescaling N afterward.

## 4. Derived local and integral Jacobians

For metric coordinates (mu,ell), at fixed physical fields and velocities,

\[
 D_\mu=\frac{A}{N^2rF^2},\quad D_\ell=-\frac{A}{N^2F},\quad
 h=\frac{V^2}{rF^2s^2}.
\]

The local Jacobian is

\[
 \partial_\mu f_\mu=\kappa r^2(FD_\mu-2D/r)+a[-1/(rF)+h],
\]
\[
 \partial_\ell f_\mu=\kappa r^2FD_\ell+a[1-N^2/s^2],
\]
\[
 \partial_\mu f_\ell=\frac1{r^2F}+\frac{2\mu}{r^3F^2}
                     +\kappa rD_\mu+b[3/(rF)+h],
\]
\[
 \partial_\ell f_\ell=\kappa rD_\ell+b[-1-N^2/s^2].
\]

For I f(r)=integral from inner radius to r, the actual integral residual is

\[
 {\cal R}_\mu=\mu-m_{\rm in}-If_\mu,\qquad
 {\cal R}_\ell=\ell-\tfrac12\log F_{\rm out}-If_\ell+(If_\ell)_{\rm out}.
\]

Consequently

\[
 \delta{\cal R}_\mu=\delta\mu-I\delta f_\mu,\qquad
 \delta{\cal R}_\ell=\delta\ell+
 \frac{\delta\mu_{\rm out}}{r_{\rm out}F_{\rm out}}
 -I\delta f_\ell+(I\delta f_\ell)_{\rm out}.
\]

The outer-boundary derivative cannot be omitted. These formulas are independently compared with complex-step differentiation of the implemented residual.

## 5. Independent controls and actual initial state

`source-intake/navier-stokes/20260914/annular-candidate-radial-derivation-attempt03/status.json` records:

- Exact symbolic gravity/field/dust variations, vacuum/Gram reductions, boundary cancellation and an omitted-boundary negative control.
- Local Jacobians checked symbolically and by complex differentiation at zero, positive, and negative source velocities. Maximum symbolic difference: 1.39e-17; original-RHS difference: 3.47e-18.
- Twelve manufactured nonaffine material-map checks comparing label and radial Gram integrals, including lapse and mass metric-covector directions. Maximum relative discrepancy: 2.79e-14. Separate omission tests detect each Jacobian. These are manufactured controls, not parent observational data.

### A caught time-slice mismatch matters

Earlier frozen pilots combined initial scalar data with a prescribed later metric/source background. That is a restricted frozen diagnostic, not a coherent whole-system initial state. The first attempt at this new solve accidentally took the complete later state while checking it against the initial scalar Gram profile. The consistency check rejected it.

The successful calculation instead reads the complete t=0 state:

- `source-intake/navier-stokes/20260914/annular-P2-joint-refinement-257-cap2e-05-attempt01/reference-initial.npz`
- `source-intake/navier-stokes/20260914/annular-P2-joint-refinement-257-cap2e-05-attempt01/MTS-initial.npz`

Original velocities are obtained from that original canonical state. The center field and velocity are independently checked against:

- `source-intake/navier-stokes/20260914/annular-moving-duhamel-trajectory-attempt01/reference-point032.npz`
- `source-intake/navier-stokes/20260914/annular-moving-duhamel-trajectory-attempt01/MTS-point032.npz`

These reverse-indexed trajectory files have physical_time=0. Candidate center Gram factors match exactly; material interpolation of prepared factors differs relatively by at most 6.65e-16.

**The new solve fixes physical fields and velocities, not the old canonical momenta.** The latter are preserved only as provenance. New candidate momenta have not yet been computed.

## 6. Actual self-consistent initial metric

`source-intake/navier-stokes/20260914/annular-candidate-initial-metric-attempt02/status.json` records six solves: reference and both MTS extensions at (radial degree,label quadrature)=(18,20) and (22,28).

Every native field edge and candidate Gram-knot band endpoint is included: 2182 radial segments, 41458/50186 collocation nodes. Each solution starts from a vacuum metric and converges in five simultaneous iterations; the original metric is a comparison, not the candidate answer. Two independent interior Gauss points per segment, with label order 32, test the differential equations away from collocation nodes.

| Quantity across the six cases | Measured maximum |
|---|---:|
| Integral constraint residual | 5.60e-17 |
| Full integral Jacobian discrepancy | 1.39e-17 |
| Off-grid mass-equation residual | 2.64e-14 |
| Off-grid log-lapse-equation residual | 4.17e-17 |
| Boundary residual | 2.78e-17 |
| Joint radial/label refinement: mass change at probes | 1.12e-16 |
| Joint radial/label refinement: log-lapse change at probes | 2.78e-17 |

Reference reproduces its original t=0 metric to binary64 roundoff: mass difference <=1.12e-16 and log-lapse difference <=1.39e-16. Both MTS extensions differ from the original MTS t=0 metric by at most 5.41051315e-10 in mu and 2.32366960e-10 in log N at the recorded probes.

Outer mass is 0.7027941941750363 for reference and 0.7027941941801547 for each candidate. Minimum F is approximately 0.73025048 and the largest |V|/(NU) is about 0.03911585, safely inside this calculation's untrapped/timelike chart. These are normalized control numbers, not observational constraints.

Both candidates give identical reported metric values at binary64 on these initial probes. This does not prove their actions identical, select an extension, or establish uniqueness. Their different responses in preceding evolution diagnostics remain relevant.

These are sampled numerical checks, not interval-certified global error bounds. Radial degree and label quadrature were increased together; the test does not separately attribute their errors. No common-field spatial refinement or coupled-force convergence is established by this initial-metric comparison.

## 7. Failures retained, not overwritten

1. `source-intake/navier-stokes/20260914/annular-candidate-radial-derivation-attempt01/status.json`: symbolic simplify left an exact-zero expression unevaluated. Rational combination and factorization prove the unchanged expression zero in the corrected version.
2. `source-intake/navier-stokes/20260914/annular-candidate-radial-derivation-attempt02/status.json`: incorrect substitution API syntax raised an exception; corrected with a substitution dictionary.
3. `source-intake/navier-stokes/20260914/annular-candidate-initial-metric-attempt01/status.json`: later-state versus initial-profile mismatch, detected at 6.96966446e-11 in the center Gram factor. Its two preliminary reference results remain failed-run evidence, not promoted results.

There was no relaxation of the successful center-factor or radial numerical gates. Executed versions and outputs remain immutable.

Implementation: `scripts/annular_candidate_radial_constraint_20260920.py`, `scripts/derive_annular_candidate_radial_constraint_v3_20260920.py`, and `scripts/solve_annular_candidate_initial_metric_v2_20260920.py`.

## 8. What this closes, and the next derivation

Closed within the stated candidate polar branch: action-owned radial loading, the two collar Jacobians, radial boundary work, local/global metric Jacobians, and a coherent candidate-owned initial metric. This advances beyond imposing the old metric as a background.

Still open: candidate canonical inversion and evolution, general-shift/temporal-current variation for this candidate, a qualified coupled force comparison, material and spatial convergence, parent uniqueness, and the full GR/Newton limit. The old 12.5718% impulse, 13.5770% fine/continuum endpoint, and 32.5535% coarse/fine endpoint discrepancies are not repaired. The preceding final spatial diagnostic changes (0.588% reference, 1.228% primary, 1.093% alternative) and non-clean MTS phase convergence are unchanged.

The next calculation is **candidate momenta and the metric-eliminated velocity response**, followed by qualified canonical inversion before any short coupled step. Fixed-background positive Schur inertia is not automatically live-gravity inertia.

To specify that calculation without adding a closure, let q,v collect source/field variables, y=(mu,ell), and R(y,q,v)=0 include radial and boundary equations. Assuming a differentiable solution and invertible R_y,

\[
 y_v=-R_y^{-1}R_v,\qquad y_q=-R_y^{-1}R_q.
\]

If this elimination is stationary for the retained gravity+matter+boundary action, and the polar reduced action has no remaining independent metric velocity, the envelope identity gives p=L_v evaluated at y. This condition must not be silently extended to a general-shift action. Differentiation then yields

\[
 M_{\rm eff}=p_v-p_yR_y^{-1}R_v,\qquad
 \dot p=(p_q-p_yR_y^{-1}R_q)v+M_{\rm eff}\dot v
\]

for the autonomous case (add explicit time derivatives when present). All partial derivatives on the right precede metric elimination. Continuous-collar momenta are densities carrying material weight; discrete-action momenta must carry the corresponding quadrature weights. Existing collocation is not thereby certified as an exact finite-label Galerkin action.

These identities identify a response term; they do not certify invertibility or positivity. Neither R_v nor candidate momenta nor reduced inertia have been evaluated here. Five converged radial iterations are not proof of those properties. Test these derivatives independently, retain the outer clock response, compare reference on equal terms, and only then attempt the new canonical evolution.

All new numerical rows remain valid_for_claim=false. Work is private and restricted to post-checkpoint-work; no publication or sibling-workbench change is part of this stage.

