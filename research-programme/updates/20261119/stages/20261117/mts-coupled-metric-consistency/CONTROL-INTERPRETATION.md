# Control interpretation: preserve the weak baseline pressure test

The original metric-result.json has metric_stage_passed=false. Its physical raw residual, refinement, algebra and source-array reproduction checks pass in BOTH cases. Its extra all-controls conjunction fails because deleting baseline pressure from the trace equation gives a normalized residual 1.1674e-5, smaller than the unchanged broad physical allowance 2e-5.

This is a sensitivity limitation of that baseline negative control, not a new failure of the correct baseline equation. Do not change the broad tolerance, rescale the norm, claim the omitted term was detected by that test, or erase the failed aggregate flag.

The frozen test design already separately requires agreement with independently derived species contacts at the algebra tolerance 1e-10. check_negative_controls.py adds an explicitly POST-RESULT supplemental test: subtract the independent predicted trace/shear contacts, then delete pressure or anisotropic stress. The correct identities should still pass 1e-10; the omitted versions should fail it. This measures equation-accounting sensitivity rather than physical closeness to the full equation.

Both diagnostics use the same cached packets, original934-state norms, and original1e-10/2e-5 thresholds. There is no new evolution and no adjustment to the theory, bank or grids. Report the supplement separately, not as an originally preregistered universal negative-control success.

Consequently:
- Raw common-metric compatibility can pass in the tested interval.
- The baseline pressure-omission control can simultaneously be inconclusive at the broad physical budget.
- The stricter contact identity can detect that omission without changing either threshold.
- The original strict aggregate and earlier baseline tiny-response failures remain false and visible.

