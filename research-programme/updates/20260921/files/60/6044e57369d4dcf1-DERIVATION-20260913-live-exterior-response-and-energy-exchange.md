# Live exterior response and energy exchange

Private continuation, 2026-09-13. Conditional regular-annulus dynamics of the existing finite-width candidate. No new parent coefficient, external actuator, public upload, black-hole result or general GR-limit claim.

## 1. Actual advance and unchanged baseline

The preceding stage evolved the enlarged closed system and found that its deliberately affine inner mass history does not persist in either branch. This stage does not repair that mismatch by fitting another initial exterior mode. It derives the exterior response of that same live system and tests it against its coupled trajectories.

The nonlinear exterior reduction, its time-dependent linear memory and its initial-state term are explicit. The mass-flow response keeps the changing metric multiplier, and the existing source apparatus pays its own energy exchange. GR-control and MTS metric-Gram receive the same interval, tolerances, perturbations, negative controls and independent verification.

Here “GR-control” means the existing control branch of this candidate apparatus/regulator calculation. It does not mean that the complete physical GR initial-boundary problem, let alone the MTS-to-GR limit, has been proved.

Predecessor and action owners:

- `DERIVATION-20260913-horizontal-clock-live-evolution-and-boundary-history.md`
- `DERIVATION-20260912-covariant-full-scalar-action-and-initial-constraint.md`
- `DERIVATION-20260912-nonlinear-history-Euler-equations.md`
- `DERIVATION-20260913-proper-clock-source-action-and-live-initial-backreaction.md`

The saved exterior amplitudes, lower enlarged-support mass seed, source trajectory D(theta), source profile, clock convention and physical pilot parameters are unchanged. The two branch preparations have different previously recorded microscopic exterior states; this is not an identical-microscopic-initial-data comparison.

## 2. Exact nonlinear reduction: what the input really is

In the horizontal regular chart write the finite collocation equations as

    y_tau = f(tau,y),       y=(x,e).

Take e to be chi_0(z) and p_0(z) at the negative translation nodes z<0: the left scalar half-band outside the old inner observation cut. At layer degree16, e has32 entries and x has1091. The z=0 state is retained in x, together with the adjacent scalar fields, source proper clocks, source energies and the inner proper-clock readout.

For a retained history x(tau) and initial exterior state e0, define

    e_tau = f_e(tau,x(tau),e),       e(0)=e0,
    o(tau) = o(tau,x(tau),e(tau)).

All mass and lapse constraints inside f_e are reconstructed from the combined state. Nothing in this definition holds the geometry fixed.

This is exact elimination within the smooth finite-dimensional constrained chart, on an interval where the reduced ODE exists. It is NOT an existence theorem for the continuum theory and NOT a response driven only by a single physical boundary trace. An arbitrary supplied x history need not satisfy the retained equations; a closed solution must also obey x_tau=f_x(tau,x,e).

The nonlinear replay therefore uses retained histories from actual coupled trajectories, including a genuinely perturbed trajectory, and checks the retained-equation discrepancy after reconstruction. Such replay checks the implementation of elimination; it is not an independent prediction of the whole coupled trajectory.

## 3. Derive the live linear memory

Along an unperturbed coupled trajectory, let the derivatives include the full mass/lapse solve and source reaction:

    delta x_tau = A_xx(tau) delta x + A_xe(tau) delta e,
    delta e_tau = A_ex(tau) delta x + A_ee(tau) delta e.

Let the two-time transition matrix satisfy

    partial_tau U_e(tau,s)=A_ee(tau) U_e(tau,s),
    U_e(s,s)=I.

Variation of constants gives

    delta e(tau)
      = U_e(tau,0) delta e0
        + integral_0^tau U_e(tau,s) A_ex(s) delta x(s) ds,

and for any differentiable recorded output,

    delta o(tau)
      = o_x(tau) delta x(tau)
        + o_e(tau) U_e(tau,0) delta e0
        + integral_0^tau o_e(tau) U_e(tau,s) A_ex(s) delta x(s) ds.

The first term is direct retained-state dependence; the second is the initial exterior state; the third is driven memory. None can generally be deleted. Because the coefficients depend on the live trajectory, the kernel is not generally a function of tau-s and need not be a convolution.

Substitution into the retained equation constructs a coupled linear Volterra equation for delta x, with kernel A_xe(tau) U_e(tau,s) A_ex(s) and the corresponding initial exterior term. This is the closed linear response formulation mathematically. The current computation evaluates A_ex on three actual retained tangent histories; it does not assemble or independently solve the full1091-dimensional retained Volterra operator. Do not report that larger solve as done.

The response is retarded in this chosen regular time chart. That alone is not a relativistic finite-propagation theorem: the spatially constrained metric solve and finite-range action still require their own continuum/causality analysis.

## 4. Explicit finite-factor interface, not a black box

The action exposes a smaller family of scalar and geometric inputs. At a fixed negative translation z, write the actual factor arrays as

    A_f = B_f0 chi_0 + a_f,
    a_f = sum_(j != 0) B_fj chi_j,
    D_f = sum_i S_fi C_i,       C_i=R_i^2 N_i U_i.

The existing canonical pair is (chi_0,omega_0 p_0), with no new coupling. The exact exterior scalar equations become

    chi_0,tau = c_0 p_0,              c_0=C_0/R_0^4,
    p_0,tau = -k_0 chi_0 + d_0,

    k_0 = sum_f B_f0^2 D_f/(omega_0 h),
    d_0 = -sum_f B_f0 D_f a_f/(omega_0 h).

These are driven oscillators only CONDITIONAL on the LIVE geometric and neighboring scalar histories. Their coefficients are not constants. C_i depends on the exterior as well as the retained state, so this representation does not remove gravitational backreaction. The full Jacobian A_ee in section3 contains those geometric derivatives; it is not simply the block oscillator matrix obtained by holding C_i and a_f externally fixed.

The output current must keep whole crossing factors:

    q_i = chi_i,tau,
    A_f,tau = sum_j B_fj q_j,
    I_fi = A_f [S_fi C_i A_f,tau - B_fi q_i D_f]/h,
    K_L = integral dz W(z) sum_(crossing pairs) orientation_fi I_fi.

Keep metric-sampling pairs even when B_f0=0. A force-support list alone need not own the current. The implementation records separate force factors, crossing factors, scalar-node support and metric-node support. It supplies the z=0 trace for the negative-half polynomial reconstruction and checks that the positive half contains no omitted crossings.

The independent verification replays these explicit oscillator equations using geometric/interface traces sampled from the coupled trajectory, and independently integrates the whole-factor crossing current. This is an explicit conditional finite-factor response, NOT yet an autonomous one-point boundary action or a replacement for the radial constraints.

A useful exact mechanical bookkeeping identity follows. With the explicitly time-dependent coefficients above, choose

    H_osc = omega_0 [c_0 p_0^2/2 + k_0 chi_0^2/2 - d_0 chi_0].

Hamilton's equations give those same two scalar equations, and along them

    dH_osc/dtau
      = omega_0 [c_0,tau p_0^2/2 + k_0,tau chi_0^2/2 - d_0,tau chi_0].

The state-derivative terms cancel. This identifies metric/interior driving work rather than making it disappear. H_osc omits retained-only potential terms and gravitational energy, is not a unique partition of a crossing factor, and is not asserted positive or equal to the exterior quasilocal mass. The full mass/source ledger below remains the relevant ledger within this candidate.

## 5. Energy exchange with the metric weight retained

At the fixed old inner cut, define w_L=U_L/N_L, distinct from the translation-layer measure W(z). The inherited live mass law is

    M_L,tau = -kappa w_L K_L.

With the lower enlarged-support seed fixed, the change of exterior quasilocal storage (M_L-M_seed)/kappa is therefore -w_L K_L, not -K_L. Linearization requires

    delta M_L,tau
      = -kappa [w_L delta K_L + K_L delta w_L].

The second term is metric work in this response. Omitting it fails the derivative ledger even though it is small in these pilot units. For an oriented gravitational canonical work trace, the existing relation is instead

    n N_L M_L,tau/(kappa U_L) = -n K_L.

These are compatible but differently weighted quantities; calling both “the power” without their convention would lose a lapse factor.

The proper-clock source retains

    D(theta)=D0+V0 theta+aProper theta^2/2,
    theta_tau=N_right,
    E_tau=-rho D'(theta),

with rho derived from the same constrained endpoint acceleration and scalar force. The layer-integrated source storage obeys

    d/dtau integral W(z) E(tau,z) dz
      = -integral W(z) rho(tau,z) D'(theta(tau,z)) dz.

Source E enters the radial geometry at each evaluation. The lower and upper enlarged-support currents vanish, and the full-support enclosed mass remains conserved. Source energy loss need not equal inner-cut mass gain: geometry weights and the other scalar stores also participate.

No extra source is introduced to restore the original affine inner history. Its failed interval test is unchanged.

## 6. Tests and measured results

The interval is tau=0..0.004 in PILOT units, not SI seconds. The degree16 state has1123 components; the geometry solve uses radial degree40. Main and independent scripts use a single below-normal, single-core worker.

The live constrained Jacobian is evaluated by complex-step differentiation through the complete geometry/source calculation. The full32x32 exterior block and7x32 output block are saved at17 temporal Chebyshev nodes. A nested9-node control tests interpolation. A full1123x3 tangent system supplies a separate reference; transition integration and separate Duhamel quadrature reconstruct its exterior and output derivatives.

| Main result | GR-control | MTS metric-Gram |
|---|---:|---:|
| Exterior tangent reconstruction max absolute error | 1.343e-15 | 6.343e-15 |
| Output tangent reconstruction max absolute error | 2.169e-18 | 8.457e-18 |
| Temporal operator refinement,9 versus17 nodes | 1.735e-17 | 1.540e-16 |
| Separate Duhamel state quadrature error | 3.123e-17 | 2.776e-17 |
| Current error if initial exterior term is omitted, exterior probe | 8.210e-4 | 8.093e-4 |
| Current error if driven memory is omitted, interior probe | 3.873e-5 | 4.653e-5 |
| Current response error with exterior/output operators frozen | 5.579e-5 | 9.831e-5 |
| Integrated inner mass balance error | 2.567e-16 | 1.153e-16 |
| Integrated source energy balance error | 1.830e-19 | 1.898e-19 |
| Inner mass change | +1.3384244e-6 | +1.3360579e-6 |
| Layer-integrated source energy change | -4.4605485e-5 | -4.4056644e-5 |
| Full-support total mass change | +3.109e-15 | +1.333e-15 |

These errors are numerical consistency measurements in the saved coordinate/variable units. They are not observational errors, certified continuum error bounds or evidence that MTS is closer to nature than GR. Tiny shared-solver replay errors in particular should not be advertised as independent accuracy.

Three perturbation directions validate the derivative, with both signs and amplitudes0.001 and0.0005 in both branches:

1. Existing exterior p0 mode b0(z)=256^2 z^4(z+1/2)^4 for z<0, zero otherwise.
2. Adjacent interior momentum p1 perturbed by1-4z^2.
3. Existing source energy perturbed in the direction delta E=0.001.

There are24 nonlinear perturbed trajectories. They are derivative-validation initial states, NOT replacement preparations and NOT claims of preserving the original matched boundary two-jet. Initial mass/source-energy changes are explicitly recorded. Every tested perturbation conserves its own full-support mass to the declared tolerance and retains positive source E at the saved observation times. This is not a global energy-positivity theorem.

The independent verifier additionally uses off-node real centered finite differences, a second complex-step size, a separate RK4 propagator with refinement, transition composition, reloaded finite-trajectory derivatives, finite-factor replay and independent crossing-current quadrature. Its results and actual completion state are authoritative in the final integrity file; do not infer their completion merely from this test description.

## 7. Scope, next mathematical step and stopping point

What is supplied: an explicit live exterior response, its initial-state and driven-memory terms, a finite-factor scalar/interface formulation, and the correctly weighted mass/source energy ledger. This replaces the earlier frozen-response stand-in for the tested regular-annulus system.

What is not supplied: a unique parent regulator, physical apparatus support stresses, an autonomous one-point port action, arbitrary-history well-posedness, nonlinear stability, horizon crossing, black-hole regularity, or a general physical GR/Newton limit.

The best next calculation is not another fit to a higher boundary Taylor coefficient. Close the actual interface formulation with the radial constraint reconstruction and retained dynamics. Specifically, derive a matrix-free Schur/Volterra retained response and test a NEW source-history perturbation, not one used to sample the three current probe contractions, against an independently evolved coupled solution. Keep source and geometric work in that calculation. If a prescribed affine inner history is later required, its actuator and budget must be action-owned, not silently imposed.

Preserve the current naturally generated history and all executed artifacts as the checkpoint.

## 8. Reproduction and evidence

- Main helper: `scripts/annular_live_exterior_response_20260913.py`
- Main runner: `scripts/derive_annular_live_exterior_response_20260913.py`
- Explicit factor helper: `scripts/annular_live_factor_response_20260913.py`
- Independent verifier: `scripts/verify_annular_live_exterior_response_20260913.py`
- Main result: `source-intake/navier-stokes/20260913/annular-live-exterior-response-attempt01/status.json`
- Saved GR operator: `source-intake/navier-stokes/20260913/annular-live-exterior-response-attempt01/GR_live_operator.npz`
- Saved MTS operator: `source-intake/navier-stokes/20260913/annular-live-exterior-response-attempt01/metric_Gram_live_operator.npz`
- Independent final authority: `source-intake/navier-stokes/20260913/annular-live-exterior-response-final-integrity.json`

The operator files include all sampled blocks/contractions, full baseline and tangent states, propagators and term-separated outputs. The24 perturbation files retain initial states, trajectories and outputs. The independent-attempt directory holds factor histories and RK4 controls. Inherited inputs, executed scripts, note and resume snapshot are hashed by the final verifier. A subsequent completion line in the mutable resume intentionally postdates its immutable snapshot.

Private-only scope: no GitHub, no subagents, no old-workbench edits. The protected-workbench check is an mtime scan since2026-09-13T21:27:19Z, not a pre-turn content-hash comparison.

