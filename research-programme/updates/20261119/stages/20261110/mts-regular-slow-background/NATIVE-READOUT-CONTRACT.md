# Bounded coupled native check after the background passes

The background-check-result is passed: original seeds, full original grid,
no refit, self-consistent slow energy, fixed rest density, step/interpolation
and independent integral controls. Only now use the existing ORIGINAL early
native engine and existing double-precision observer. No rebuild or edits
to either library/source are authorized by this step.

Run old and candidate tables for each of cold/heavy at k=1/Mpc, the same
original4253requested scale factors, retained accuracy2.5/background8/start
factor.5/perturbation IntTolBoost6/lAccuracyBoost4. Derive each table's own
conformal clock at those scales. Evolve the full native species from its
regular perturbation initialization, not by supplying a late thermal seed.
No phase averaging event is allowed in this early schedule.

Reuse the source_func observer from mts-metric-feedback-20261107: it exports
sigma, sigma', eta, eta', Weyl, D/Q/Pi and native background quantities
directly as real*8, including delta_cdm64. These are not casts of the old
float32 transfer columns. Freeze all relevant code, DLL, observer, candidate
and schedule hashes before each worker begins native evolution.

The separately retained late frozen-operator capture explicitly rejects
TightCoupling. Do not enable it or remove its guard to obtain an apparent
early restart. This step obtains a complete native evolution with physical
readouts, NOT a saved full-state restart. A separate supported early capture
still has to retain its regime, hierarchy and tight-coupling caches.

Recover Newtonian scalar variables using alpha=sigma/k, Phi=eta-H*alpha,
Psi=Phi-Pi/k^2; compare the resulting Weyl with the independent native Weyl.
The original local interval indices2292--2591 and original numerical gates
remain fixed. Old-table comparisons retain the known on-shell defect;
candidate comparisons use the actually evolved repaired source table.
Do not compare differing clock values as if they were the same scale factor.

All workers are sequential, one numerical thread, CPU4below-normal,
Python-B and900second bounds. Native failures are preserved, not retried
automatically. No publishing, unrelated process changes or new dependencies.
