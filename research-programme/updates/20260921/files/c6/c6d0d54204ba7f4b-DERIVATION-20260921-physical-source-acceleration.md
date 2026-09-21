# Physical source acceleration from the live canonical model

## Aim

Convert the resolved coupled evolution into the same physical acceleration observable in the reference and both MTS branches. This is a calculation of the candidate's response, not another identification of missing inputs. The initial phase point and the fine-integration sixteen-step endpoint at T=1e-5 are both tested. Coordinates retain their inherited normalization; numerical time is not assigned SI seconds.

The preceding accepted time/integration evidence is `DERIVATION-20260921-eight-sixteen-step-time-refinement.md` and `source-intake/navier-stokes/20260914/annular-candidate-finer-time-final-integrity.json`. Its two failed coarser momentum comparisons remain recorded unchanged.

## 1. Derive acceleration by differentiating the full inverse

Let p=P(q,v) be the full momentum map after solving the candidate's radial gravity equations, and f the corresponding canonical coordinate covector. On a differentiable, locally invertible branch,

    q_dot=v, p_dot=f,
    P_v*a + P_q*v = f,
    a = P_v^(-1) (f-P_q*v).

The saved mass matrix is not P_v. It is only a preconditioner for solving the full nonlinear map, with the evolving metric retained. Forming every dense column is unnecessary: define the straight canonical tangent path

    q(epsilon)=q+epsilon*v,
    p(epsilon)=p+epsilon*f,
    w(epsilon)=P^(-1)(q(epsilon),p(epsilon)).

Differentiating its defining equation at zero gives w'(0)=a. The path is a directional probe, not an extra time-integrated trajectory. This construction retains all16,425 components and the full gravitational response; it is not a source-only inversion or a projection onto selected modes.

At each of six phase points we solve plus/minus probes at epsilon=1e-5,5e-6,2.5e-6, using reference/material integration orders16/48. Each root uses the existing5e-12 weighted residual and2e-12 maximum preconditioned-correction gates. The central derivative D_h=(w(h)-w(-h))/(2h) and its two fourth-order Richardson estimates are compared. These are numerical derivative estimates, not certified error enclosures or a global invertibility theorem.

Independent forward evaluations test the result: compute P_q*v and P_v*a by separate centered coordinate/velocity perturbations, and compare their sum with f. A joint perturbation (q+delta*v,v+delta*a) supplies a further chain-rule check at delta=1.25e-6. These evaluations do not prescribe their momenta to equal p+delta*f, so the residual is not zero by construction.

Derivative acceptance is declared in advance as a difference below1e-8+0.002*the corresponding acceleration scale. Weighted momentum-tangent residuals must be below0.002 relative to f. A failed scientific gate is recorded, not removed or retuned. The absolute tolerance is in inherited acceleration units.

After the first run passes its derivative gates, all three endpoint cases are repeated with probe sizes ten times larger (1e-4,5e-5,2.5e-5). This addresses the observed small difference between the two derivative estimates before treating a geodesic residual as physical. The base phase points, equations, roots and tolerances stay fixed. Both probe families are retained, including any sign changes in their residuals; the smaller residual is not selected as evidence of agreement. The cross-family proper-acceleration comparison uses the same1e-8+0.002*scale acceptance rule.

## 2. Keep the clock and moving metric in the observable

For a fixed material label z, let b(t,z) be the physical radial coordinate, V=db/dt, F=1-2*mu/b and N=exp(ell). Its proper-clock rate is

    s=d(tau)/dt=sqrt(N^2-V^2/F).

The radial-coordinate acceleration parametrized by proper time is

    A_tau=d^2b/d(tau)^2=a_b/s^2 - V*s_dot/s^3,
    s_dot=[N*N_dot - V*a_b/F + V^2*F_dot/(2*F^2)]/s.

N_dot and F_dot are total derivatives sampled on that moving material label, including the metric response to all field/source changes. A second evaluation differentiates the observable U=V/s directly along the canonical tangent path and divides its derivative by the base s. Agreement with the explicit chain rule tests the conversion independently of rearranging its terms.

This is not the invariant norm of four-acceleration: a geodesic has zero covariant four-acceleration but can have nonzero d^2b/d(tau)^2. This distinction is essential for the GR/Newton comparison.

Samples include48 positive-weight material quadrature points, the15 material interpolation nodes, and the center. Report both central values and weighted residual norms; extrema at zero-density material edges must not substitute for a mass-weighted comparison.

## 3. Derive a reference comparator for the same observable

For the polar metric ds^2=-N(t,r)^2 dt^2+dr^2/F(t,r)+r^2 dOmega^2, the radial connections are

    Gamma^r_tt=F*N*N_r,
    Gamma^r_tr=-F_t/(2F),
    Gamma^r_rr=-F_r/(2F).

Consequently the radial geodesic comparator on the same sampled geometry is

    A_geo=[-F*N*N_r + V*F_t/F + V^2*F_r/(2F)]/s^2,
    F_t=F_dot-V*F_r.

The computation derives this independently from the test-dust action L=-m*sqrt(N^2-V^2/F), retaining explicit time dependence in the Euler-Lagrange derivative. The symbolic expressions agree. Its physical comparison with the full finite-source, wave-coupled candidate is then a measurement: equality is not imposed as an acceptance rule.

In a prescribed static Schwarzschild metric, N^2=F=1-2*mu/r, this reduces exactly to

    A_tau=-mu/r^2,
    d^2r/dt^2=-(mu/r^2)*(F-3*V^2/F).

The slow-motion, weak-field coordinate acceleration tends to -mu/r^2. The proper-time radial identity itself is exact in this test-source limit. These are symbolic baseline controls, not a derivation of the parent coupling's SI normalization or a claim that the finite material candidate already equals this special case. The separately recorded -mu/r^2 on a general evolving metric is explicitly a Newton-like proxy, not its general geodesic prediction.

Omitting the proper-clock response or the metric time derivative is retained as a diagnostic comparison. The physical geodesic residual is A_tau-A_geo using the same units, geometry, label and time point, rather than recycling differently normalized earlier force percentages.

## 4. Measured results

The main run completes111 implementation checks in3478.13seconds: six phase points,36 full inverse probes and132 inverse iterations. All30 derivative-consistency and18 independent momentum-tangent comparisons pass. The wider endpoint repeat completes69 checks in1869.37seconds:18 inverse probes and72 inverse iterations. All15 derivative and nine tangent comparisons pass there too. No equations, root tolerances or modes are changed between the families.

This totals54 inverse probes,204 inverse iterations, nine base evaluations and54 independent forward-tangent evaluations:267 live evaluations, about1hour29minutes of numerical work on one restrained worker. There are six distinct physical phase points; repeating their three endpoints with a different probe scale does not create three new evolved states.

The source center's proper acceleration is approximately-0.019313 in the inherited units. The geodesic comparator is approximately-0.0193127. Narrow-probe endpoint residuals are-3.467e-7(reference),-3.232e-7(primary) and-3.239e-7(alternative). The wider reference and primary residuals are-3.710e-7 and-3.476e-7. Thus their common small residual is not discarded as zero, and the wider repeat does not magically remove it. Both families are published side by side in the local evidence.

The independently reconstructed tables, weighted profiles, derivative-estimate sensitivities and moving-anchor traction comparison are in `source-intake/navier-stokes/20260914/annular-candidate-source-acceleration-v3-computed-results.md`. Exact source-linked values take precedence over the rounded figures in this narrative. Their paired MTS/reference comparisons retain branch-specific geometry and measure derivative-scale sensitivity; they do not assign physical significance without spatial and parent-action control.

The substantive advance is an evaluated all-component source-acceleration map, the proper-clock conversion, exact test-source GR/Newton controls, and the explicit projected reaction identity below. The next question is now the origin and limit of a quantified non-dust reaction, not an unspecified missing coupling coefficient.

## 4a. The derived coupling/reaction identity

There is a more informative comparison than simply demanding every coupled source follow a free geodesic. For a material label define the dust momentum and coordinate covector

    p_d=m*V/(F*s),
    f_d=-m*[N*N_r+V^2*F_r/(2*F^2)]/s.

Differentiating p_d with the total metric and clock derivatives, and substituting the same A_geo as above, gives exactly

    d(p_d)/dt-f_d = (m*s/F)*(A_tau-A_geo).

After material projection, the total canonical source equation therefore implies

    integral w*L_a*(m*s/F)*(A_tau-A_geo) dz
      = f_a_non-dust - d(P_a_non-dust)/dt.

The checker independently reconstructs dust momentum derivatives from the saved inverse probes, the explicit dust covector from metric gradients, and the remaining field/Gram force and momentum channels. This tests the projected identity and exposes the cancellation between field force and field-carried momentum. A small total source covector divided by a bare mass is not the physical acceleration. Vanishing15-component projected residual also does not imply pointwise vanishing across all material labels.

### Differentiate the inverse residual too

The first postflight fails a further raw reaction-closure check at the reference endpoint:2.02219e-6 relative to the dust-force norm exceeds its2e-6 threshold. Its executed script, failed seal and initial traction output are preserved. This does not retroactively change the45 acceleration derivative or27 forward-tangent gates. Diagnosing the saved probes gives a specific cause, rather than treating that failure as a physics verdict.

Write the computed canonical momentum as P_computed=P_target+e, where P_target=p+epsilon*f. With non-dust momentum P_nd=P_computed-P_d, the raw reconstructed reaction obeys

    R_raw=f_nd-d(P_nd)/dt,
    R_raw-(d(P_d)/dt-f_d)=-d(e)/dt.

All nine cases satisfy this decomposition to roughly2.3e-16 of the dust-force norm. The directly differentiated dust momentum independently agrees with the projected geodesic residual to better than2e-10 on that scale. Therefore the raw mismatch is explained by differentiation of the small nonzero inverse-root error, not by a new force term. Root-corrected R_raw+d(e)/dt and target-owned non-dust momentum are recorded separately; their cancellation is an accounting identity, not independent proof of physical agreement or an error bound on the recovered acceleration.

The same raw2e-6 closure gate remains failed for all three narrow-probe endpoints. The wider probes lower the raw mismatch to approximately3.91e-9 in all three branches, about517times smaller, and pass the unchanged gate. Both probe families, every raw failure and every correction term remain in the tables. There is no threshold relaxation, replacement of computed momentum by target momentum without disclosure, or selection of a smaller geodesic residual. Their residual force and pointwise acceleration profiles still need the spatial/boundary decomposition below.

### The moving internal anchor must be included

The saved spatial basis explicitly removes the field value at the moving source anchor: the two adjacent elements use a zero value there. The checker verifies this against their actual index lists. This is a boundary condition of the present numerical candidate; its parent physical-versus-gauge interpretation must not be silently assumed.

For a continuum wave with L=alpha*phi_t^2/2-beta*phi_r^2/2 on either side of a moving Dirichlet interface b(t), phi(b(t),t)=0 implies phi_t=-V*phi_r at each side. Moving-boundary variation gives

    T_left = L - phi_r*(L_phi_r-V*L_phi_t)
           = (beta-alpha*V^2)*phi_r_left^2/2,
    T_right = -(beta-alpha*V^2)*phi_r_right^2/2.

With alpha=r^2/(N*sqrt(F)), beta=r^2*N*sqrt(F), the resulting bulk-wave source traction is

    T_wave = r^2*sqrt(F)*s^2/(2*N)
             *[phi_r_left^2-phi_r_right^2].

This sign corresponds to a wave on the left pushing the interface outward. The formula is symbolically checked and evaluated using high-precision one-sided P2 derivatives of the saved states. It is a bulk-wave comparator, not a fitted cancellation term. Any remainder includes the unseparated finite-element field-equation residual and the explicit Gram/source contributions. The actual total non-dust reaction, not this continuum traction alone, enters the preceding exact projected identity.

Thus a nonzero A_tau-A_geo can represent a legitimate reaction to the imposed moving field boundary, rather than automatically a failure of gravity or an integration bug. Conversely, the pin cannot be promoted to a physical interaction just because a boundary formula exists. The next derivation must account for that boundary and its remaining field-equation/Gram terms from the parent action. This is a concrete coupling question now attached to measured quantities.

### Measured boundary comparison and next derivation

At the wider-probe endpoints the independently evaluated boundary traction and raw non-dust reaction are:

| Branch | Bulk traction norm | Non-dust reaction norm | Vector remainder / reaction norm |
| --- | ---: | ---: | ---: |
| Reference | 4.60598e-9 | 4.54915e-9 | 0.01254 |
| MTS primary | 4.35365e-9 | 4.26533e-9 | 0.02082 |
| MTS alternative | 4.32416e-9 | 4.27403e-9 | 0.01193 |

The last column is the norm of the VECTOR difference, not a subtraction of norms. Thus this derived boundary force matches the small additional source reaction to about1.2-2.1percent in the present candidate, with no fitted scaling. The inverse-root derivative is around0.02percent of that raw reaction at these wider endpoints. These finite-basis covector norms are diagnostics in the fixed material basis, not invariant SI forces or certified error bounds. Initially the boundary traction is approximately6.35e-18 while the inferred small reaction is differentiation-sensitive, so endpoint agreement cannot be extrapolated to arbitrary states.

The next calculation should split the remaining1.2-2.1percent using the actual action: cellwise field Euler-Lagrange terms, internal flux jumps from the piecewise-polynomial field, and the explicit Gram/source force. This gives a testable decomposition rather than assigning the remainder a name. Then derive the conditions under which the full reaction vanishes or decouples, recovering geodesic source motion without changing the gravitational comparator or discarding the field sector. The same-action radial mass-current check follows that source balance.

## 5. Reproduction and integrity

- Calculation helpers: `scripts/annular_candidate_source_acceleration_20260921.py`.
- All-component inverse and independent-tangent runner: `scripts/run_annular_candidate_source_acceleration_20260921.py`.
- Endpoint parameter-scale control: `scripts/run_annular_candidate_source_acceleration_wide_probes_20260921.py`.
- Numerical execution: `source-intake/navier-stokes/20260914/annular-candidate-source-acceleration-attempt01/status.json`.
- Wider endpoint execution: `source-intake/navier-stokes/20260914/annular-candidate-source-acceleration-wide-probes-attempt01/status.json`.
- First postflight (preserved failed): `scripts/seal_annular_candidate_source_acceleration_20260921.py` and `source-intake/navier-stokes/20260914/annular-candidate-source-acceleration-final-integrity.json`.
- Second postflight (preserved failed after all nine case reconstructions): `scripts/seal_annular_candidate_source_acceleration_v2_20260921.py` and `source-intake/navier-stokes/20260914/annular-candidate-source-acceleration-v2-final-integrity.json`. A path-indexing typo stopped the cross-family section; no equations or numerical tolerances changed for the repair.
- Residual-aware independent reconstruction: `scripts/seal_annular_candidate_source_acceleration_v3_20260921.py`.
- Authoritative integrity record: `source-intake/navier-stokes/20260914/annular-candidate-source-acceleration-v3-final-integrity.json`.

Every solved probe saves its full phase point, recovered rates, momentum residual, radial state, sampled metric and clock. The independent reconstruction checks canonical-path identities, both inverse gates, material interpolation, derivative estimates, proper-clock and Christoffel conversion, tangent residuals, and every physical sample row. Closed-form test-source inversions check the same observable for inward, outward and momentarily static motion.

Private, local-only work; no GitHub changes, subagents, galaxy edits or sibling-workbench edits. One single-core BelowNormal worker with BLAS threads limited to one. Turn baseline2026-09-21T14:47:07Z and check-in18:47UTC; numerical budget9,000seconds leaves validation time. Protected-workbench verification is an mtime scan from that baseline, not a whole-tree pre-turn hash snapshot. Executed scripts and sealed results are immutable.
