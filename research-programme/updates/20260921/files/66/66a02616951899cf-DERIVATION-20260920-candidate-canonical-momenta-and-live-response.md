# Candidate canonical momenta and live gravitational velocity response

Private checkpoint, 20 September 2026. This extends the coherent initial metric in `DERIVATION-20260920-candidate-radial-constraint-and-initial-metric.md`, not the earlier mixed-time frozen pilot.

## 1. The actual advance sought

Compute momenta from the continuous-material candidate action, retaining the material interpolation weights, on its own solved initial geometry. Differentiate the radial constraints with respect to motion and include that gravitational response in the momentum derivative. Test reference and both MTS extensions on equal terms.

This is a polar, zero-shift, untrapped initial-state calculation. The inherited gravity action and supplied normalized coupling are unchanged. No new evolution or full GR limit is claimed.

Source seal: `source-intake/navier-stokes/20260914/annular-candidate-radial-metric-final-integrity.json`. The same full t=0 physical fields and velocities, common 1094 field coordinates per material label, and 15 material labels are retained. Canonical momenta are newly computed, not copied from the old action.

## 2. Momentum must carry the material basis

Let q_aj and v_aj be field coordinates and velocities on material interpolation nodes a; b_a,V_a are source coordinates and velocities. Write L_a(z) for the cardinal material polynomials, phi_j(z,r) for the moving physical P2 basis, and

\[
 W(z,r)=\sum_{a,j}L_a(z)\phi_j(z,r)v_{aj}+m(z,r)V(z),
 \qquad m(z,r)=-d(z,r)\chi_r(z,r),\qquad
 V(z)=\sum_a L_a(z)V_a.
\]

Here d is the source-map displacement, not an adjustable coupling. At fixed coordinates, the velocity variation is

\[
 \delta W=\sum_{a,j}L_a\phi_j\delta v_{aj}+m\sum_a L_a\delta V_a.
\]

With F=1-2 mu/r, N=exp(ell), k=r^2/(N sqrt(F)), s=sqrt(N^2-V^2/F), and the same w,sigma as in the preceding report, the canonical momenta are

\[
 p_{aj}=\int dr\int dz\,w(z)L_a(z)\,k(r)W(z,r)\phi_j(z,r),
\]
\[
 P_a=\int dr\int dz\,w(z)L_a(z)\,k(r)W(z,r)m(z,r)
       +\int dr\,\sigma(r)L_a(z_b)\frac{m_sV(r)}{F(r)s(r)}.
\]

These are action derivatives with respect to the material nodal velocities, not unweighted pointwise momentum samples. The distinction matters: the earlier label-collocation momenta cannot simply be relabeled as the canonical variables of the continuously averaged action. The independent center-label reference check below compares pointwise quantities only after the common-field covector is pulled back to the native field space.

The candidate Gram term has no velocity dependence at fixed coordinates and metric. It affects these momenta through the candidate metric; it must not be inserted as a spurious direct kinetic term.

## 3. Derived gravitational response to velocity

At fixed coordinates, B,g,sigma are unchanged, while

\[
 \delta A(r)=2\int dz\,wW\delta W,\qquad \delta V(r)=\delta V(z_b).
\]

The finite perturbation of A is exactly quadratic:

\[
 A(v+\epsilon\delta v)=A+\epsilon\delta A+
 \epsilon^2\int dz\,w(\delta W)^2.
\]

For the preceding radial RHS f=(f_mu,f_ell), its explicit velocity forcing at fixed geometry is

\[
 \delta_v f_\mu=\frac{\kappa r^2}{2N^2}\delta A
 +a\,\frac{V}{Fs^2}\delta V,
 \qquad a=\frac{\kappa m_s\sigma N\sqrt F}{s},
\]
\[
 \delta_v f_\ell=\frac{\kappa r}{2N^2F}\delta A
 +\frac{\kappa m_s\sigma}{rNF^{3/2}}
   \left(\frac{2V}{s}+\frac{V^3}{Fs^3}\right)\delta V.
\]

The local metric Jacobian is inherited from the independently varied radial action. The linearized integral constraints solve

\[
 R_y\,\delta y=-R_v\,\delta v,\qquad y=(\mu,\ell),
\]

including delta mu_inner=0 and

\[
 \delta\ell_{\rm out}=-\frac{\delta\mu_{\rm out}}{r_{\rm out}F_{\rm out}}.
\]

The response is not just an interior radial derivative with a fixed outer lapse. A separate complex-perturbed nonlinear solve uses the exact quadratic A(v+epsilon delta v) and perturbed source velocity, keeps the outer clock condition, and checks the analytic response.

## 4. Momentum derivative and reduced inertia

The gravitational coefficient variation is

\[
 \delta k=k\left(\frac{\delta\mu}{rF}-\delta\ell\right).
\]

Thus every wave momentum derivative uses k[delta W+W(delta mu/(rF)-delta ell)] in place of k W in section 2. For source proper-clock momentum p_s=m_s V/(F s), exact partial derivatives are

\[
 (p_s)_V=\frac{m_sN^2}{Fs^3},\quad
 (p_s)_\mu=p_s\left(\frac2{rF}+\frac{V^2}{rF^2s^2}\right),\quad
 (p_s)_\ell=-p_s\frac{N^2}{s^2}.
\]

Combining these with the solved metric response gives

\[
 \delta p=M_{\rm eff}\delta v,\qquad
 M_{\rm eff}=p_v-p_yR_y^{-1}R_v.
\]

The extra term is evaluated here rather than set to zero. At fixed metric the second velocity variation is a positive kinetic integral plus the positive timelike dust term. That fixed-metric argument does not establish positivity of the full metric-eliminated operator.

Four linearly independent probes are used: smooth field motion, source motion, an alternating common-field nodal direction, and mixed material-dependent field/source motion. Full momentum vectors and their responses to those four directions are retained. The resulting four-by-four matrix is a restriction to that probe span, not the full 16425-by-16425 reduced inertia. No mode is removed from the action; checking four directions does not certify all its modes.

## 5. Independent action and reference checks

Two complementary action tests are used:

1. At fixed metric, contract the assembled full momentum vector with each velocity direction and compare it to direct differentiation of the averaged kinetic and proper-clock actions.
2. Re-solve the metric at complex-perturbed velocity and differentiate the total gravity+wave+dust+outer-boundary action. Compare this on-shell derivative with the same momentum contraction.

The latter is a numerical check of the stationary-action envelope identity, not an assumption that arbitrary metric substitution is allowed. The action retains -mu_out/kappa; the inner multiplier term vanishes because inner mass is fixed. The calculation substitutes mu_r from the solved radial equation to evaluate the on-shell gravitational term. Equality is checked numerically with the sampled radial/material quadratures, not asserted as an exact discrete variational theorem for the old collocation evolution.

The implementation also compares every component of the analytic full momentum response with a separate complex-perturbed momentum evaluation, tests reciprocity of the four-probe reduced matrix, and increases radial degree/material quadrature together. An independent common-element, center-label momentum integral is pulled back through the exact-source embedding and compared with the original reference momentum.

## 6. Numerical outcome

The run in `source-intake/navier-stokes/20260914/annular-candidate-live-momenta-attempt01/status.json` completed with **155 implementation/control checks**, no failed execution, and approximately 346 seconds of single-core worker time. This is reproducible numerical evidence about the specified candidate, not experimental validation.

Six cases were evaluated: reference and both MTS extensions at (radial degree, material quadrature)=(18,20) and (22,28). Each case contains all **16425 action-owned momentum components** (15 times 1094 field variables plus 15 source variables), their four full directional derivatives, the solved metric responses, and the independent complex-perturbed results.

| Check across the six cases | Measured maximum |
|---|---:|
| Common-representation metric change from preceding initial solve | 1.12e-16 |
| Radial integral residual | 5.60e-17 |
| Explicit velocity-forcing discrepancy | 1.22e-17 |
| Linearized radial response residual | 2.99e-19 |
| Analytic vs independently re-solved metric response, relative | 2.93e-15 |
| Full momentum-response component comparison, relative | 2.19e-16 |
| Four-probe reciprocity error, relative | 2.96e-17 |
| Weighted momentum vs fixed-metric action derivative, relative | 9.72e-15 |
| Weighted momentum vs on-shell total-action derivative, relative | 6.85e-14 |
| Joint quadrature refinement of full momentum vector, relative | 3.58e-14 |
| Joint quadrature refinement of four-probe live inertia, relative | 8.51e-15 |

The independent center-label reference momentum integral, after common-to-native covector pullback, differs from the original reference momentum by at most 7.44e-15. The analogous MTS change from the old initial momentum is about 3.882e-13; those old momenta were not constraints on this new solve.

Every four-probe reduced-inertia matrix is symmetric to the recorded tolerance and has positive eigenvalues. Its smallest eigenvalue is approximately 0.00234851577848 in these supplied normalized probe coordinates. The fixed-metric counterpart is approximately 0.00234851577609. These numbers are basis-dependent and are not a bound on all modes of the full system.

The gravitational response changes the four-probe inertia by about **7.1301e-7 in relative Frobenius norm**, in the specified unwhitened probe coordinates. It is small but nonzero here; the frozen-background approximation is therefore not literally the derived live response. This ratio must not be promoted to a universal error bound for the full operator, other initial data, or evolved motion.

Both MTS extensions give the same reported results at this initial state. Their preceding evolved diagnostic differences remain unresolved; agreement on this slice neither selects an extension nor proves them equivalent.

The general-shift/current, force-convergence, and full-GR claim flags stay false. All new CSV rows retain valid_for_claim=false. No numerical gate was relaxed, no historical file was overwritten, and all 55 earlier failed executions remain in the inherited evidence chain.

## 7. Scope and next substantive step

No time integration, all-mode reduced-inertia positivity theorem, complete canonical inverse, or general-shift/current derivation is supplied here. The original physical-force discrepancies and field spatial-convergence obligations remain unchanged. Joint radial/material quadrature refinement is not field-mesh convergence.

The next calculation is a **full, weighted canonical inverse at fixed coordinates with the candidate metric solved simultaneously**. Use the action-owned momenta as targets; do not transplant the original unweighted collocation momenta. Recover the known initial velocities from perturbed starting guesses, check the complete momentum and radial residuals, and compare reference and both extensions. A matrix-free derivative is preferable to a dense 16425-square matrix. Any conditioning or null direction must be measured rather than removed silently. Only after qualification should a short coupled evolution be attempted.

A practical candidate preconditioner follows from the action's support: the fixed-metric field mass couples only P2 nodes sharing an element, while it couples the 15 material coefficients densely. With field-node-major ordering this gives a narrow block band; the 15 source variables can be handled by a Schur complement. That structure does not apply to the generally nonlocal gravitational response itself. Assembly, conditioning, preconditioning, and the full inverse have **not** yet been implemented or qualified.

Implementation: `scripts/annular_candidate_canonical_response_20260920.py` and `scripts/derive_annular_candidate_canonical_response_20260920.py`. All evidence is private, within post-checkpoint-work, with no GitHub, sibling-workbench, or subagent action.
