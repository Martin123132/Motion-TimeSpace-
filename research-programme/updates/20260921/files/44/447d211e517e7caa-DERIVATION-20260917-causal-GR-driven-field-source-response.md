# Independent causal GR-driven field/source response

Private continuation of `DERIVATION-20260916-GR-projection-and-coupled-consistency-force.md`.
Scope: the unchanged513/8 finite action, prescribed flat background, original
compact-quintic initial state and T=.4. This is not the full GR limit. The
benchmark is already known: input isolation is not a claim of statistical
blinding or a new experiment.

## 1. Build the response, rather than insert its measured value

The preceding checkpoint decomposed the actual force error using the known
finite trajectory. Here the predictor is forbidden from reading that
trajectory. Its inputs are the independently computed GR projection, its
derivative, the original action and original initial data only.

For a differentiable reconstructed GR path z(t), evolve

\[
 \dot\eta=DF_h(z)\eta+F_h(z)-\dot z,
 \qquad \eta(0)=y_h(0)-z(0),\qquad w=z+\eta.
\]

No observed force discrepancy, future finite state, fitted coefficient or
discarded Gram row is an input. The field, source position, field rate,
source velocity and proper clock all evolve in this coupled prediction.

The matrix-free implementation evaluates the already qualified original flow
at z+i*epsilon*eta: its real part supplies F_h(z) and its imaginary part divided
by epsilon supplies DF_h(z)eta. No dense full Jacobian is formed at every step.
An independent analytic full Jacobian and force derivative check this operation
on a smaller instance of the same action before any production integration.

## 2. Reconstruction must have its own derivative

Use cubic Hermite reconstruction of the isolated GR states and derivatives.
Its derivative in the forcing term is the exact derivative of that chosen
polynomial, not a separately interpolated derivative mislabeled as identical.
The integrator restarts at every reconstruction knot. All81 original output
times are retained, even for the control using only41 reconstruction knots.
Any kinematic mismatch between reconstructed scalar velocity and its coordinate
derivative is therefore part of the actual forcing, not silently removed.

For this chosen z, the identity

\[
 \dot w=F_h(z)+DF_h(z)\eta,
 \quad N_h=F_h(w)-\dot w
       =F_h(z+\eta)-F_h(z)-DF_h(z)\eta
\]

is exact up to the numerical tangent/integration implementation. It holds for
any differentiable reconstruction, even one that does not exactly satisfy
the GR equations. Reconstruction quality affects eta, the nonlinear remainder,
and ultimately the prediction, so it still requires independent controls.
No uniform-in-time bound follows merely from small sampled values of N_h.

For E=y_h-w, the remaining error satisfies

\[
 \dot E=DF_h(w)E+N_h+
 [F_h(w+E)-F_h(w)-DF_h(w)E],\qquad E(0)=0.
\]

This identifies the omitted drive without assuming that stability or the
nonlinear remainder is automatically harmless.

## 3. Two output rules fixed before validation

Both are reported; neither is selected afterward to hide a failure:

1. Linearized force: F_force(z)+DF_force(z)eta.
2. Original, nonlinear force evaluated on the reconstructed state: F_force(w).

The latter retains the force's known finite-amplitude rational dependence;
it does not restore the nonlinear dynamical terms omitted from eta's equation.
Their difference and the actual nonlinear dynamical remainder are saved.
Neither rule changes the original physical action or subtracts a fitted error.

## 4. Controls and input isolation

Prespecified runs, each on BOTH branches through the originalT=.4:

|Run|Reference degree|Reconstruction knots|Maximum-step multiplier|
|---|---:|---:|---:|
|standard|768|81|1|
|tighter time|768|81|1/2|
|coarser reconstruction|768|41|1|
|reference control|512|81|1|
|reference control|384|81|1|

Standard correction tolerances are2e-10/2e-14; tighter2e-12/2e-16. Step caps
come from the original coupled stiffness diagnostic, not a presumed reduction
in mode count. The frozen frequency estimate is not a nonlinear stability proof.

An isolated input pack contains only GR times/states/derivatives/forces and
the original initial vector. A runtime audit hook rejects array reads outside
that pack and the predictor's own outputs; rejection of the known future
finite-trajectory path is tested before integration. All prediction files and
their hashes are frozen before the separate validator opens finite trajectories.

Force prediction accuracy against the finite trajectory is tested at2e-7.
Independent time/reconstruction/reference changes are separately tested at2e-8.
The original GR force criterion remains2e-7, but these are different questions:
accurately predicting a finite-action GR discrepancy does not remove it.
Raw errors, signed values atT=.21, component errors and failed acceptance
flags remain visible even if the implementation checks succeed.

## 5. Implementation and results

- `scripts/annular_GR_causal_predictor_20260917.py`
- `scripts/prepare_annular_GR_causal_predictor_20260917.py`
- `scripts/run_annular_GR_causal_predictor_20260917.py`
- `scripts/validate_annular_GR_causal_predictor_20260917.py`

All five paired runs completed. Input/tangent qualification has19 checks,
the five production runs have45, and the frozen-prediction comparison has39:
103 successful implementation checks. These counts are not independent
physical observations or evidence for the complete theory.

Predictions were frozen at2026-09-17T03:19:48.980108Z; the separate future-state
read phase began at03:19:49.000588Z. Both timestamps are stored with the local
+01:00 offset in the evidence. All10 prediction arrays were complete and hashed
before that comparison. No numerical attempt failed in this continuation.

Primary comparison:
`source-intake/navier-stokes/20260914/annular-GR-causal-validation-attempt01/status.json`.
Frozen manifest:
`source-intake/navier-stokes/20260914/annular-GR-causal-validation-attempt01/frozen-predictions-before-finite-comparison.json`.
Input qualification:
`source-intake/navier-stokes/20260914/annular-GR-causal-inputs-attempt01/status.json`.

### Prediction accuracy on the81 original sample times

Maximum absolute force error against the original finite trajectory, in the
existing normalized benchmark units (not a new SI-force calibration):

|Configuration|Reference, original force on w|MTS, original force on w|MTS, linearized force|
|---|---:|---:|---:|
|768/81 standard|1.30319e-13|6.64582e-10|2.10370e-8|
|768/81 tighter time|1.20168e-13|6.61663e-10|2.10381e-8|
|768/41 reconstruction|5.45660e-13|6.63395e-10|2.10454e-8|
|512/81 reference|1.20526e-13|6.64046e-10|2.10243e-8|
|384/81 reference|3.55141e-13|6.70557e-10|2.11928e-8|

Both prespecified output rules pass the2e-7 prediction gate for every
configuration on both branches. Reference linearized-force errors are at most
4.19363e-10 over these configurations. This is sampled prediction accuracy;
the integration coversT=.4, but no between-sample supremum is certified.

The standard MTS maximum source-position, velocity and clock prediction errors
are respectively2.44859e-9,2.57370e-8 and1.38339e-10. The field and field-rate
errors are1.64200e-11 and6.52924e-10. These are separate component norms in the
benchmark's normalization, not one dimensionally interchangeable error norm.
Original source/velocity/clock comparison gates pass for all10 predictions.

### Independent controls

Maximum changes of the predicted finite force relative to768/81 standard:

|Control|Reference, original force on w|MTS, original force on w|MTS, linearized force|
|---|---:|---:|---:|
|Tighter time|4.33239e-14|3.62575e-12|3.62547e-12|
|41 reconstruction knots|5.61447e-13|9.14582e-12|1.54762e-9|
|Reference degree512|6.34783e-14|1.62351e-12|1.93854e-10|
|Reference degree384|3.62159e-13|6.21094e-12|5.29992e-10|

All controls pass2e-8 for both force rules. They compare the predicted finite
force itself, not differences against changing GR reference forces. Individual
projected consistency terms can still be reference-sensitive. Their cancellation
through the coupled response is what these tests now check independently.

### What has and has not closed

For degree768, the original finite-to-GR peak force discrepancies remain
5.48205187e-7 (reference) and3.67184258e-6 (MTS). The independently reconstructed
predictions give5.48205252e-7 and3.67250716e-6. All original GR-force gates
remain false; neither branch's trajectory or action was changed.

AtT=.21 the actual MTS discrepancy is+3.43633319e-6; the independent prediction
is+3.43625510e-6, differing by-7.80948e-11. The earlier retrospective field/source
response is therefore no longer merely a term filled using the known finite
solution. It has been produced causally from the GR path and original initial
state and checked on this finite benchmark.

This construction is a first linear defect-correction/Newton step for the
finite initial-value problem around a prescribed GR path. It uses the same
finite action as the target trajectory. Its successful reconstruction is an
internal numerical/mathematical result, not independent experimental support,
not a new fundamental coupling, and not a cheaper solver: all finite modes and
their original stiffness were retained. It does not establish spatial
convergence, a uniform nonlinear stability bound, live-metric backreaction,
or the full parent-action GR limit.

## 6. Derived force-response representation for the spatial step

Write A_h(t)=DF_h(z(t)), r_h(t)=F_h(z(t))-z_dot(t), and let P_h(t,s)
be the fundamental matrix of eta_dot=A_h eta. On a fixed finite grid, while
the reference and flow stay in their smooth admissible domain, variation of
constants gives exactly

\[
 \eta(t)=P_h(t,0)\eta(0)+\int_0^t P_h(t,s)r_h(s)\,ds.
\]

Let f_h be the source-force observable, g_h(t)=Df_h(z(t)) its row derivative,
and c_h(t)=f_h(z(t))-f_{GR}(t). The linear force discrepancy is therefore

\[
 \delta f_{h,\mathrm{lin}}(t)=c_h(t)+g_h(t)P_h(t,0)\eta(0)
       +\int_0^t g_h(t)P_h(t,s)r_h(s)\,ds.
\]

This exposes both the initial projection and the accumulated coupled residual;
the local consistency force alone is not the error law. Equivalently, for a
fixed terminal time t, the adjoint p_t(s) obeys

\[
 -\partial_s p_t=A_h(s)^T p_t,\qquad p_t(t)=g_h(t)^T,
 \qquad
 \delta f_{h,\mathrm{lin}}(t)=c_h(t)+p_t(0)^T\eta(0)
          +\int_0^t p_t(s)^Tr_h(s)\,ds.
\]

The adjoint has not yet been implemented here; its formula is a direct
consequence of differentiating p_t(s)^T eta(s). It offers a force-weighted
way to separate field, source-cell and moving-geometry residuals rather than
compare unweighted components with different units.

The exact nonlinear finite force adds

\[
 \mathcal R_f=[f_h(w)-f_h(z)-Df_h(z)\eta]+[f_h(y_h)-f_h(w)].
\]

Both terms are retained in this checkpoint: the first is the saved difference
between the two prespecified observables, and the second is the independent
prediction error. Small sampled values do not prove either term vanishes as
h tends to zero. A uniform spatial estimate must control the propagator or its
force-weighted adjoint, the projected residual, the initial projection, and
this nonlinear remainder together. No such uniform bound is silently assumed.

## 7. Next concrete target

Use this qualified response construction to derive the leading source-trace
and spatial-refinement contribution, starting from the exact force-response
representation above. Check that prediction on the already qualified1025/8
benchmark with both branches and the originalT=.4; reuse its existing finite
trajectories and completed tighter-time controls rather than repeat them.
Preserve the independent prediction/input separation for any new grid run.

Do not subtract the predicted error from the physical force, change the action,
or call a reconstructed discrepancy a repair. The target is an actual
refinement/stability argument that drives the unmodified discrepancy to zero,
or a demonstrable obstruction if it does not. Only after the prescribed-flat
control is resolved should this be promoted to the coupled live-metric test.
