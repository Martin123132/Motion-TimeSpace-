# Initial preparation versus accumulated motion: a force-specific response calculation

Private continuation of `DERIVATION-20260916-anchored-moving-reduction-and-gap-envelope.md`. The earlier original-action and GR-oracle results are unchanged. This checkpoint concerns the short T=.005 reduced/full finite-action comparison, not a full GR limit.

## 1. Target and controls

The preceding moving test passed its sampled numerical reduction-force budget, but a small unweighted omitted-mode norm alone did not explain the force error. The present target is constructive: calculate the endpoint force sensitivity, carry the initial projection error, separate physical omission from interpolation/integration residuals, and measure the nonlinear remainder.

Both original reference and MTS branches use the same method. There is no fit, force subtraction, damping, altered physical threshold, new parent coefficient, or new empirical claim. The saved tight trajectories remain immutable. Replays generate denser data separately and must reproduce the saved force observations before being used.

## 2. Full coupled equations and their derivative

Start from the same finite action

    L=udot^T M(b) udot/2+V udot^T A(b)u
      +V^2 u^T B(b)u/2-u^T K(b)u/2+Lm(b,V).

Let v=udot, V=bdot, D=M_b+A-A^T, E=A_b-B. The original, unreduced equations are

    [M  c] [u_ddot] = [r_u],   c=A u,
    [cT h] [b_ddot]   [r_b],   h=Lm_VV+u^T B u,

    r_u=-V D v-Ku-V^2 E u,
    r_b=v^T(M_b/2-A)v-2V v^T B u
        -V^2 u^T B_b u/2-u^T K_b u/2+Lm_b-V Lm_Vb.

The Schur solve retains the complete field/source velocity Hessian. The material force observable is

    h_force(z)=Lm_VV b_ddot+Lm_Vb V,

not pressure alone. The complete state z=(u,b,v,V,clock) includes the clock equation. For this autonomous prescribed metric the clock does not feed back into the force; the corresponding adjoint component is proved and checked to remain zero, rather than silently dropping the clock state.

For any state perturbation dz, differentiation of Hkin*a=r gives

    da=Hkin^-1 (dr-(dHkin)*a).

This supplies the full Jacobian without nested finite differences of a complex-step solver. In particular the source-position column needs M_bb,A_bb,B_bb,K_bb; the source-speed column differentiates the relativistic material inertia as well as r. Omitting either would corrupt the force sensitivity.

Implementation uses the existing analytic first/second matrix derivatives, a banded field-mass solve, and the same coupled Schur complement. Independent comparisons with the old variational acceleration and complex-step directional derivatives qualify the full Jacobian, force gradient, and transpose action on both branches, two backgrounds, and moved/unmoved states. This is a finite prescribed-background result, not variation of live geometry.

## 3. Independent nonlinear counterfactual

There is an independently interpretable split which does not use a linearization:

    F_full(raw initial state)-F_reduced
       =[F_full(raw)-F_full(prepared)]
        +[F_full(prepared)-F_reduced].

The prepared full model starts from the exact lifted reduced initial position/rate/clock state, then evolves with the unchanged FULL equations. It is a diagnostic counterfactual, not a replacement for the original full initial data.

The first bracket is the evolved effect of initial preparation under the full dynamics. The second is the effect of imposing the reduction after that preparation. The second includes the direct same-state omission force as well as its accumulated trajectory effect; it need not vanish at t=0 even though the prepared and reduced initial states agree. This is an exact algebraic split but, like nonlinear counterfactual attributions generally, it depends on the explicitly chosen intermediate trajectory. It is not a unique causal partition of all possible descriptions.

## 4. Adjoint identity, including numerical-path defects

Let F(z) be the original first-order vector field, z_f(t) the reconstructed full path and z_r(t) the reconstructed lifted reduced path. These paths use separately saved states and their actual ODE derivatives. They are not declared exact solutions merely because their endpoints passed a check.

Define

    e=z_f-z_r,  J=DF(z_r),
    d_r=F(z_r)-z_r_dot,
    d_f=F(z_f)-z_f_dot,
    R_F=F(z_f)-F(z_r)-J e.

Then the exact reconstruction-level equation is

    e_dot=J e+d_r-d_f+R_F.

The subtraction of d_f is essential. Neglecting full-path interpolation/integration error while attributing the reduced-path defect to omitted physics would give a misleading answer.

Set ell=Dh_force(z_r(T)) and solve backwards

    -psi_dot=J^T psi,  psi(T)=ell^T.

Differentiating psi^T e gives

    F_full(T)-F_reduced(T)
      =DeltaF_same(T)+psi(0)^T e(0)
       +integral psi^T(d_r-d_f)dt
       +integral psi^T R_F dt+R_h,

    R_h=h_force(z_f(T))-h_force(z_r(T))-ell e(T).

The direct term DeltaF_same is obtained from the original full acceleration evaluated at the lifted reduced endpoint minus the reduced material force. It is not a fitted correction. The initial term is not omitted.

At saved replay nodes the exact lifted reduced derivative is known, so the physical moving omission defect is computed independently as

    d_motion=F(lift(y_red))-D(lift)*F_red(y_red).

It has acceleration components only. The analysis interpolates these independently calculated samples, and splits d_r into that interpolated omission plus the remaining reconstruction defect. The four integrated scalars are therefore

    I_motion = integral psi^T d_motion,interpolated dt,
    I_red,recon = integral psi^T(d_r-d_motion,interpolated)dt,
    I_full,recon = -integral psi^T d_f dt,
    I_nonlinear = integral psi^T R_F dt.

Both reconstruction contributions are retained individually and as a net sum; a cancellation must not be hidden. Their refinement test is needed before interpreting I_motion as a resolved physical omission contribution. The small nonlinear remainder, if observed, is a measured diagnostic along these paths, NOT a uniform state-tube bound.

An independent forward tangent calculation tests the transpose propagation and integral signs:

    eta_initial_dot=J eta_initial,       eta_initial(0)=e(0),
    eta_motion_dot=J eta_motion+d_motion,interpolated, eta_motion(0)=0,
    eta_all_dot=J eta_all+d_r-d_f,        eta_all(0)=e(0).

Their endpoint contractions with ell must match the corresponding backward adjoint contributions. Neither full nor reduced force observations are used to choose these sensitivities.

## 5. Numerical protocol

- The full state dimension is575 (286 field coordinates, source position, their rates, and clock). Original reduced dimensions remain273/reference and278/MTS.
- Replay the same T=.005 interval and same initial states at321 saved nodes. Use the old tight tolerances2e-12/2e-14 and half-frequency maximum-step caps. Reproduce the old41 force observations to2e-10.
- Reconstruct entire physical state vectors using cubic Hermite interpolation of value and actual derivative; subtract the initial offset before interpolation. This avoids artificial large-coordinate cancellation. The reconstruction's position derivative need not exactly equal its independently interpolated velocity, so ALL components of its defect are kept.
- Compare161-node and321-node reconstructed paths. Interpolated actual omission uses a separate cubic spline. Both are numerical reconstructions, not continuum certificates.
- Backward adjoint and forward tangent use the full coupled Jacobian. Standard adjoint tolerances2e-10/2e-12, integral absolute tolerance1e-15. A further control uses100-fold tighter tolerances and half the maximum step.
- Prespecified identity and attribution tolerances2e-10 are numerical controls within the existing2e-7 reduction budget; they do not alter any GR-oracle gate. Failure of an attribution flag must stay visible.

## 6. Results

The full Jacobian qualification completes60 checks; the acceleration and full-Jacobian directional relative errors are below1e-12 at the finest mesh. Denser trajectory replay and independent nonlinear counterfactual complete18 checks. They reproduce the old41 force observations to9.19e-16/reference and2.224e-12/MTS.

Exact nonlinear endpoint partition at T=.005:

| Contribution | Reference | MTS |
| --- | ---: | ---: |
| Initial preparation: full(raw)-full(prepared) |-4.6061169143e-9|-5.0325642195e-9|
| Moving reduction: full(prepared)-reduced |-1.7666880552e-9|+3.0016590367e-8|
| Total reduced/full force difference |-6.3728049695e-9|+2.4984026147e-8|
| Direct same-state omission |-6.7212685501e-9|-2.5218168888e-10|

For MTS at this endpoint, the moving-reduction contribution is larger than the initial-preparation effect and has the opposite sign. Its direct same-state term is comparatively small; accumulated trajectory response matters. For reference, both nonlinear counterfactual brackets have the same sign, but the accumulated response partly cancels its negative direct same-state contribution. These endpoint statements must not be generalized to every time or every physical regime.

With321 observations the maximum sampled total force difference is3.3163858203e-8/reference and4.0863457690e-8/MTS; both remain below the unchanged2e-7 numerical reduction budget. The denser MTS sampling reveals a slightly larger maximum than the previous41-point result. It is recorded, not hidden or described as identical.

Tight backward-adjoint endpoint attribution:

| Derived term | Reference | MTS |
| --- | ---: | ---: |
| Initial preparation response psi(0)^T e(0) |-4.6060319861e-9|-5.0325080051e-9|
| Accumulated physical omission response |+4.9546426872e-9|+3.0268687967e-8|
| Direct same-state omission |-6.7212685501e-9|-2.5218168888e-10|
| Sum: physical linear prediction |-6.3726578491e-9|+2.4983998273e-8|
| Observed total |-6.3728049695e-9|+2.4984026147e-8|
| Net reconstruction contribution |-6.7664e-14|+3.8084e-14|
| Sum of absolute reconstruction contributions |6.7664e-14|5.1326e-13|
| Measured dynamical plus observable nonlinear remainder |-9.7337e-14|+2.1568e-13|
| Complete identity closure discrepancy |1.7881e-14|2.2589e-13|

The bare physical prediction happens to differ from the observed totals by1.4712e-13/reference and2.7874e-14/MTS. Do NOT advertise those tiny cancellation-dependent differences as certified accuracy: the complete identity closure, nonlinear subtraction, reconstruction components and the independent replay precision set a more cautious numerical resolution. The MTS complete-identity error is larger than its bare prediction difference. All are still much smaller than the prespecified2e-10 attribution control and2e-7 reduction-force budget.

The adjoint initial term agrees with the independently evolved nonlinear initial-preparation effect within8.50e-14 on both branches. Its accumulated term plus direct same-state omission agrees with the nonlinear moving-reduction effect within8.41e-14. This is a non-fitted consistency check of the attribution, not an additional empirical physics test. Clock adjoint components remain exactly zero as the full equations predict.

Final controls pass on both branches. Changing161 to321 path nodes shifts the physical accumulated-response term by2.18e-14/reference and1.13e-14/MTS. Tightening adjoint integration changes the physical prediction by1.61e-16/reference and7.63e-18/MTS. Independent forward tangents agree with their backward-adjoint contractions within3.56e-13.

An important numerical caveat is preserved: the standard321-node MTS reconstruction contributions individually reach approximately+1.17e-10 and-1.17e-10 while their sum is only1.58e-13. The tighter run reduces their absolute sum from2.3382e-10 to5.1326e-13. We therefore checked the individual terms as well as their net sum; the largest componentwise change under path/time refinement is1.3870e-10, below the2e-10 numerical-control tolerance, but clearly not a10^-13-level certification of those individual standard-run terms. The physical initial/motion attribution is much more stable and independently matches the nonlinear counterfactual. Do not hide this cancellation or infer certified accuracy from the small net residual.

All computations complete:117 successful current algebra/implementation checks (Jacobian60, dense paths18, standard adjoint plus independent tangents18, tighter adjoints8, refinement/counterfactual controls13). No new failed attempt. These are implementation and short-trajectory tests, not117 independent confirmations of a physical theory.

## 7. Reproducible files

- `scripts/annular_full_force_linearization_20260916.py`
- `scripts/verify_annular_full_force_linearization_20260916.py`
- `scripts/run_annular_force_response_paths_20260916.py`
- `scripts/annular_force_adjoint_response_20260916.py`
- `scripts/run_annular_force_adjoint_response_20260916.py`
- `scripts/verify_annular_force_response_controls_20260916.py`
- `source-intake/navier-stokes/20260914/annular-full-force-linearization-attempt01/status.json`
- `source-intake/navier-stokes/20260914/annular-force-response-paths-attempt01/status.json`
- `source-intake/navier-stokes/20260914/annular-force-adjoint-tight-attempt01/status.json`
- `source-intake/navier-stokes/20260914/annular-force-adjoint-response-attempt01/status.json`
- `source-intake/navier-stokes/20260914/annular-force-response-controls-attempt01/status.json`

## 8. What would and would not follow

An accurate force-specific attribution would explain the observed short finite reduction error and tell us whether initial preparation, accumulated omission, or a numerical artifact dominates. That is more useful than only recording a small total difference. It would not prove that the reduction works at T=.4, that its nonlinear remainder is uniformly bounded, that the original trace-domain/continuum problem has disappeared, or that full GR follows from the parent theory.

The nonlinear counterfactual already indicates that MTS at this endpoint needs its accumulated motion response, not initial preparation alone. A concrete next construction is the causal FULL-STATE defect response

    eta_dot=DF(z_r) eta+[F(z_r)-z_r_dot],
    eta(0)=z_full(0)-z_r(0),
    z_corrected=z_r+eta.

It uses the original vector field, its derived Jacobian, the reduced path and the original initial state; no future full trajectory or observed force difference is an input. Direct substitution gives

    F(z_corrected)-z_corrected_dot
       =F(z_r+eta)-F(z_r)-DF(z_r)eta.

Thus the first-order dynamical defect is removed and the remaining defect is exactly nonlinear. The initial state is corrected in all channels, not silently reset on the full comparison side. Position/rate consistency follows from the original kinematic rows. Clock and source corrections stay coupled to the field.

This is a derived numerical correction of the entire approximate state, NOT permission to subtract a fitted force from the reduced equations. Its force must be evaluated consistently from the original action at the corrected state, with the remaining dynamical residual measured separately. It is not yet implemented/tested here; a uniform nonlinear remainder or long-time guarantee would still require additional control.

Next implement that causal response on both saved short reduced paths, predict the corrected field/source/clock and force WITHOUT full future-state input, then use the held-out full trajectories only for validation. Retain the signed initial/moving contributions. Only after that should the time window be extended under cluster/window control. No old force failure is upgraded by this analysis.

Use a predictor input pack containing only the reduced path, its derivatives, original initial state and fixed model specification; write its predictions before opening full future-state validation data. This makes the absence of force fitting inspectable. A successful correction would reconstruct the original finite action more accurately, not cure that action's inherited GR-oracle discrepancies. Once this numerical error is controlled, return to the actual GR-oracle/joint-refinement question rather than indefinitely polishing internal agreement.
