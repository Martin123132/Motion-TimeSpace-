# Joint boundary–geometry closure for the regular-annulus candidate

Private continuation, local date2026-09-14. Start2026-09-13T23:06:13Z. No GitHub action, no changes to the original workbench, no new parent coefficient fitted.

## 1. What gap this closes

The preceding response calculation supplied a retained-state or metric history from an already solved coupled trajectory. It demonstrated a conditional exterior response but did not predict the changed retained history itself.

This stage solves that missing feedback loop. Retained fields, exterior fields, source clocks, apparatus energy and radial geometry respond together to a new source protocol. The predicted perturbed fields are saved BEFORE the fresh coupled comparison trajectories are computed. No perturbed retained or metric histories enter the prediction.

The initial unperturbed trajectory is still used to linearize the equations and initialize the nonlinear solver. That is legitimate background data for a response calculation, not an independently predicted background. Every nonlinear residual evaluation reconstructs geometry from its current trial fields rather than prescribing geometry from the background.

The main calculation completes the joint linear response and eight nonlinear joint solutions: four source-protocol parameters in each of the GR-control and MTS metric-Gram branches. It does not establish the full physical MTS-to-GR limit, a one-point boundary action, continuum regularity or a black-hole result.

Owners:

- `DERIVATION-20260913-live-exterior-response-and-energy-exchange.md`
- `DERIVATION-20260913-horizontal-clock-live-evolution-and-boundary-history.md`
- `DERIVATION-20260913-proper-clock-source-action-and-live-initial-backreaction.md`
- `DERIVATION-20260912-covariant-full-scalar-action-and-initial-constraint.md`

“GR-control” denotes the existing control branch within this candidate apparatus and regulator calculation, not a complete physical GR initial-boundary value theorem.

## 2. Geometry is a derived functional of the fields

Use the inherited regular chart F=U^2=1-2M/R>0, with fixed enlarged lower mass seed and the unchanged outer clock convention. Separate the radial densities as

    epsilon = epsilon_fixed + k_source/F,
    sigma = source reservoir density,

    M_R = kappa [F epsilon_fixed + k_source + U sigma],
    (ln N)_R = M/(R^2 F) + kappa [epsilon_fixed+k_source/F]/R.

Here epsilon_fixed contains the factor potential and the free scalar kinetic density. In the right source layer only,

    k_source = W(z) omega_right R^2 v^2/(2 width),
    sigma = W(z) E/width,
    v = D_eta'(theta).

These densities are functions of the trial scalar/source state, not of a supplied metric history. The source kinetic term was separated because p_right=R^2 v/U is constrained: treating its kinetic density as metric-independent would give the wrong linear constraint.

For given regular matter data, the mass equation is an ordinary radial initial-value equation. Its right-hand side is locally Lipschitz in M away from F=0. The lapse follows by radial integration and normalization

    N(R_outer)=C_clock(tau) U(R_outer).

Thus, on a regular interval where the radial solution exists, these conditions define a unique radial geometry functional G[y;eta]. They do not provide a horizon-crossing solution or a uniform continuum existence bound.

The numerical radial collocation is an approximation to these equations. Its source-layer algebraic solve must still remain nonsingular and accurate; uniqueness of the continuous radial IVP must not be used to assert global uniqueness of every discretized root.

### Explicit linear geometry response

At fixed radii, parameter and state variations obey

    delta M_R + a_R delta M = b_R,

    a_R = kappa [2 epsilon_fixed/R + sigma/(R U)],
    b_R = kappa [F delta epsilon_fixed + delta k_source + U delta sigma],
    delta M(R_lower)=0.

The integrating-factor representation is

    I(R)=exp(integral_(R_lower)^R a_R(s) ds),
    delta M(R)=I(R)^(-1) integral_(R_lower)^R I(s) b_R(s) ds.

The subscript R on a_R and b_R labels radial coefficients, not a further derivative. With ell=ln N,

    delta ell_R
      = [(1+2 kappa k_source)/(R^2 F^2)] delta M
        + (kappa/R) [delta epsilon_fixed+delta k_source/F],

    delta ell(R_outer)
      = -delta M(R_outer)/(R_outer F_outer),

    delta U=-delta M/(R U),       delta N=N delta ell.

The outer clock is unvaried in this experiment. If it were varied, delta ln C_clock would enter the normalization explicitly.

For the source variation,

    delta chi_right = v delta theta + theta^3 delta eta/6,
    delta v = (aProper+eta theta) delta theta + theta^2 delta eta/2,
    delta k_source = (W/width) omega_right R^2 v delta v,
    delta sigma = (W/width) delta E.

Factor-potential variations and free-momentum variations provide delta epsilon_fixed. These equations close the previously supplied geometric response using the evolving state and the declared source parameter.

An independent verifier integrates these derived radial variation equations, including vacuum gaps, and compares them with differentiation through the original nonlinear radial reconstruction. Both mixed field/protocol perturbations and a source-protocol-only variation are included.

## 3. New source history, unchanged initial preparation

Keep the existing proper-clock apparatus action and deform only its prescribed trajectory:

    D_eta(theta)=D0+V0 theta+aProper theta^2/2+eta theta^3/6,
    v_eta(theta)=V0+aProper theta+eta theta^2/2,
    a_eta(theta)=aProper+eta theta.

eta is an explicitly declared apparatus protocol parameter, with units of scalar displacement per proper-clock-time cubed. It is not a fitted MTS coupling or an observationally inferred parameter. Values eta=-1,-1/2,+1/2,+1 are fixed pilot-unit probes, not optimized fits.

At theta=0, D, D' and D'' are unchanged. The complete saved initial state, initial geometry, source energy and initial RHS are unchanged. This does NOT mean every higher derivative of the coupled fields or apparatus energy is unchanged: the source jerk and ensuing reaction derivatives are supposed to change.

Re-deriving the source reaction gives

    theta_tau=N_right,
    p_right=R^2 v_eta/U,
    p_right,tau
      = R^2 a_eta N/U + R v_eta M_tau/U^3,
    rho=omega_right p_right,tau-Gchi_right,
    E_tau=-rho v_eta.

The cubic source history must appear consistently in the source displacement, velocity, acceleration, radial kinetic density, scalar factors, reaction and energy drain. Changing only the endpoint force would not be this action-owned protocol.

No actuator is added at the inner observation cut, no exterior initial amplitude is refitted, and the original deliberately affine inner-history condition is not restored by fiat.

## 4. Close the exterior memory through a retained Schur solve

Write the fully reconstructed finite-state equations as

    y_tau=f(tau,y;eta),       y=(x,e),

with32 exterior and1091 retained components. At eta=0 the derivative satisfies

    delta x_tau=A_xx delta x+A_xe delta e+b_x,
    delta e_tau=A_ex delta x+A_ee delta e+b_e,
    b=partial_eta f,          delta y(0)=0.

Every block contains the derived metric response. It is not differentiated at fixed lapse or mass.

The continuous exterior elimination is

    delta e(t)=U_e(t,0) delta e0
              + integral_0^t U_e(t,s)[A_ex(s)delta x(s)+b_e(s)] ds.

Substitute it into the retained equation. The retained history is now an unknown of the resulting Volterra equation, not an input imported from a solved perturbation.

For temporal collocation, let W_t be the time-integration matrix and let A blocks act diagonally at the time nodes. For a general linear right-hand side r,

    E_op = I-W_t A_ee,

    S_op = I-W_t A_xx-W_t A_xe E_op^(-1) W_t A_ex,

    S_op delta x = r_x+W_t A_xe E_op^(-1) r_e,
    delta e = E_op^(-1)[r_e+W_t A_ex delta x].

The source-history experiment uses r=W_t b. Nonzero initial data enter r as repeated initial-value rows; the independent verifier checks that case separately.

The32 exterior columns of the full Jacobian are evaluated directly, supplying A_ee and A_xe. The retained action is matrix-free: actual trial retained directions are differentiated through the full reconstructed RHS to obtain A_xx delta x and A_ex delta x. This is no longer limited to the three supplied tangent histories of the preceding stage.

The small exterior block is factored once per temporal grid; the retained Schur operator is solved iteratively. Numerical invertibility and converged residuals on these grids are not a regulator-uniform operator bound.

## 5. Nonlinear closure, not only a linear replay

For the full time-node state Y, solve

    R(Y;eta)=Y-1*y_initial-W_t f(t_nodes,Y;eta)=0.

The linear prediction Y0+eta delta Y initializes this solve. Chord-Newton corrections use the unperturbed Schur factorization, but R is evaluated with the ACTUAL nonlinear source and freshly reconstructed geometry at every iteration.

Reusing a background Jacobian as a solver preconditioner is not freezing the physical geometry. The fixed Jacobian determines the correction step; convergence is assessed against the nonlinear equations, including their changing metric.

Both the linear and nonlinear predictions are stored before any perturbed reference evolution is run. Only afterward are new DOP853 coupled trajectories and a new full variational trajectory generated for comparison.

The independent verifier additionally integrates the full nonlinear equations with RK4 at64 and128 steps, without taking the predicted time-node history as an input.

## 6. Results and what the small numbers do not prove

Same interval tau=0..0.004 in PILOT units, not seconds; layer degree16, radial degree40. Temporal degree8 and16 correspond to9 and17 time nodes. There are18547 retained time-node unknowns on the finer grid and544 exterior time-node unknowns.

| Main result | GR-control | MTS metric-Gram |
|---|---:|---:|
| Schur iterations for new linear source response | 5 | 5 |
| Full linear collocation residual | 2.497e-17 | 8.151e-17 |
| Temporal9-versus17-node response refinement | 1.606e-17 | 1.568e-16 |
| Predicted tangent versus fresh full tangent | 9.442e-16 | 5.442e-15 |
| Predicted output tangent versus fresh full tangent | 1.997e-16 | 6.287e-16 |
| Largest nonlinear residual before correction | 5.226e-12 | 5.230e-12 |
| Largest nonlinear residual after correction | 3.678e-16 | 4.450e-16 |
| Largest nonlinear state error versus fresh evolution | 2.526e-15 | 4.247e-15 |
| Largest nonlinear output error versus fresh evolution | 7.373e-18 | 1.041e-17 |
| Largest full-support mass drift in finite runs | 6.440e-15 | 5.108e-15 |
| Minimum source energy at saved times | 0.00095086324 | 0.00095145296 |

Each of the eight nonlinear solutions needed one chord correction; its inner Schur correction took2 iterations for GR and3 for MTS. The nonlinear correction is small because this is a short, weak source perturbation, not because arbitrary large changes have been solved. Its approximate eta^2 scaling is visible between eta=1 and1/2.

The saved baseline is recovered without refitting. Mass-flow and source-energy balances hold to the recorded tolerances. Both signed finite-difference amplitudes reproduce the predicted response. The main runner completes44 checks.

These are consistency and numerical closure results for this candidate system, not independent experimental evidence, certified error bounds, observational precision or proof that MTS beats GR.

### Honest negative-control limitation

Deleting the exterior feedback from the retained solve changes the internal tangent state by about2.80e-12 in GR and3.33e-12 in MTS. Those are resolved against the corresponding full-tangent comparison errors.

For this particular short source perturbation, however, the resulting output-vector differences are only1.42e-15 and2.20e-15. They do NOT pass the deliberately conservative100-times-reference-error output-resolution criterion. The main records therefore retain one_way_feedback_effect_resolved=false for the output test in BOTH branches. Do not claim a large new observable feedback signal.

The independent verifier also solves a nonzero exterior initial-state response with no retained history supplied. It compares with the previously saved full tangent as a separate validation case and reports whether that stronger internal feedback control is resolved.

## 7. What is closed; what remains

Closed at the tested finite-regulator, regular-annulus level:

- Radial mass/lapse response is derived from the state and source variations rather than supplied as a perturbed metric history.
- The retained–exterior linear response is solved jointly through the actual Schur/Volterra feedback.
- Full nonlinear time-node solutions respond to a new source history with fresh geometry in every residual.
- Source reaction, reservoir energy and the mass-flow ledger stay attached to the same apparatus action.

Still not established:

- A one-point local boundary action, without the resolved collar/state variables.
- Regulator-independent convergence or a controlled continuum/local GR limit.
- Long-time nonlinear stability, horizon crossing or global causal well-posedness.
- Physical apparatus support stresses/microphysics, or a derivation of its chosen source protocol from fundamental MTS.
- Restoration of the former affine inner history; it is not imposed here.

The next substantive test should widen the regime rather than rewrite the same missing-input ledger: continue this closed solver to longer pilot intervals and refine its spatial regulator without retuning the initial amplitudes. Track when source energy, chart regularity, coupling feedback, numerical convergence or continuum comparisons fail. Only then use a controlled regulator/coupling limit to assess the GR connection.

This checkpoint closes a particular computational/derivational dependence, not the entire research programme.

## 8. Evidence and final authority

- Joint source/Schur helper: `scripts/annular_joint_boundary_geometry_20260914.py`
- Main prediction runner: `scripts/derive_annular_joint_boundary_geometry_20260914.py`
- Independent radial response: `scripts/annular_radial_response_20260914.py`
- Independent verifier: `scripts/verify_annular_joint_boundary_geometry_20260914.py`
- Main status: `source-intake/navier-stokes/20260914/annular-joint-boundary-geometry-attempt01/status.json`
- GR pre-reference prediction: `source-intake/navier-stokes/20260914/annular-joint-boundary-geometry-attempt01/GR_predicted_response_before_reference.npz`
- MTS pre-reference prediction: `source-intake/navier-stokes/20260914/annular-joint-boundary-geometry-attempt01/metric_Gram_predicted_response_before_reference.npz`
- Final verification authority: `source-intake/navier-stokes/20260914/annular-joint-boundary-geometry-final-integrity.json`

Independent results and completion are determined by that final file, not inferred from the planned-test descriptions in this note. The note, executed scripts, inherited sources and resume snapshot are hashed there. The later completion line in the mutable resume intentionally postdates its snapshot.

Only one below-normal single-core worker is used. The protected-workbench check is an mtime scan since2026-09-13T23:06:13Z, not a pre-turn full-content snapshot.

