# Live pressure-work transport: fixed3044..3046 test

Private/local. Previous goal turn derived and tested accumulating work from
saved histories; it made verified progress. Keep the full MTS goal active.
This stage advances the retained physical model, not a replacement theory.

Restore the COMPLETE two-epoch stage3044 baseline/MTS32/64 states. Never
encode/rematch or reset K,error,h/f,work,parent,probes. Matching3040 and split3041
remain. Preserve original bank,binary,parameters,934 seed/norms,physical grids,
rtol1e-10/normalized-atol1e-12 and1e-10/2e-5 science gates.

Use original source epochs3045 then3046; the first cumulative physical AND
pressure-work gate must pass before any3046 run. One numerical worker/thread,
below-normal CPU4, cutoff14:05UTC. Save complete physical and diagnostic state
every32 original source boundaries and at each original epoch. Stop safely
on a hold/failure; no automatic retry. No GitHub or other-chat process changes.

## Non-invasive dense-output route

Use the SAME DOP853 physical right-hand side and error controller. Test both
cases/resolutions over the first source segment with dense output disabled
and enabled: accepted clocks and physical states must be bitwise identical.
Verify initial RHS/source restore and dense endpoint agreement. A mismatch
blocks this route; do not silently change solver tolerances or physical law.

For MTS, evaluate derived pressure-work rates on the accepted solver steps'
dense output. All original background/source knots remain outer boundaries.
Gaussian orders3,5,7 are frozen; evaluate shared nodes once. Diagnostic work
does not enter the physical adaptive error norm or feed back into the fields.
Baseline owned pressure/error-work is exactly zero; it gets the same physical
evolution and dense-control preflight, not an invented heavy-field sector.

The linear error transport and pressure law are unchanged:

    J_h'=-3 H B_P h, J_f'=-3 H B_P f, J_e'=-3 H B_P e,
    P[z]=beta*(V*z_g-mu^2*Phi*z_f).

Compute physical old/coherent and stable branch-change forms with all deltaH
cross terms. Accumulate the non-cancelling absolute integrals separately.
Also integrate the actual numerical split residual e-h-f independently;
do not define it from differences of integrated answers.

## Inherited history and uncertainty

All three NEW quadrature-order accumulators start from their respective
32/64 previous stride1/order7/nodes4 fifteen-component final work vectors.
This retains3041..3044 work. No artificial zero at3044. Preserve the previous
failed raw/offline diagnostics and unresolved tiny-error precision.

Carry a conservative WORKING inherited allowance: previous stride1-versus2,
stride2-versus4,degree5-versus7,order7-versus5,order5-versus3 differences and
primitive rounding. Keep32/64 trajectory differences separate to avoid
discarding or hiding them. New quadrature allowances SUM absolute local
order differences over accepted steps, not merely their cancellation at the
final endpoint. Also accumulate local primitive-rounding estimates. These are
numerical uncertainty estimates, not a certified global/continuum bound.

At new epochs compare J_h+J_f against independently integrated pressure work
relative to the retained3041 anchor. Require the full coupled raw physics,
actual metric/pressure/exchange, signed controls, source/readout error envelope
and physical-response work budgets. The tiny approximation error's own
relative resolution is separately reported, not substituted for physical
response precision. Dense quadrature does not erase inherited uncertainty.

Reuse complete earlier histories for cumulative checks and stable velocity-slip
readout. No external data fitting, quantum-measure inference or new coupling.
