# Live phase-aware fields coupled to the common metric

Completed 2026-11-17. This is a new self-consistent continuation of the retained
model, not a new field law, fit, or replacement for the earlier work.

## What changed

The regular matched-density/relative-phase variables now evolve together with
the background correction, metric and full surrounding hierarchy from original
epoch 3039 to 3040. Their physical density, current and pressure are decoded
before the live metric and field equations are evaluated. No future perturbation,
source or metric history drives the calculation. The retained original
background/thermodynamic tables remain model inputs, not independently predicted
quantities. DERIVATION.md states the exact old/change transformation and its
derivative; no pressure endpoint or phase coordinate is discarded.

Both baseline and MTS keep the original bank, native binary, parameters, report
clocks, original 934-row normalization/seed, and numerical gates. A new native
capture has 1050 rows; its known 1049-row prefix is exact. Six evolutions compare
32/64 step caps: cold direct, heavy direct, and heavy phase-aware. This extends
about 0.96306 conformal Mpc, with 244 baseline and 614 MTS diagnostic samples.
The samples are existing background-table boundaries, not additional original
report epochs. No parameter was fitted.

## Results under the frozen numerical tests

All ratios below use the original frozen component norms unless stated otherwise.
The numerical gate is 2e-5; algebra/preflight checks retain 1e-10.

| Check | Baseline direct | MTS direct | MTS phase-aware |
|---|---:|---:|---:|
| Largest main residual/refinement budget | 4.36291e-8 | 4.47526e-8 | 4.47526e-8 |
| Coherent density-exchange budget | 6.13849e-14 | 3.85542e-11 | 8.30368e-13 |
| Coherent current-exchange budget | exact owned zero | 8.89067e-12 | 1.80282e-11 |
| Largest independent-native full-output budget | 7.98386e-9 | 2.66246e-6 | 2.66246e-6 |

Phase-aware versus direct physical readouts and sources pass. The largest
reported normalized equivalence budget is 4.88961e-10. Source equivalence entries
are differences plus rounding, with step-refinement checked separately for each
implementation, not a separately combined source-error enclosure. The maximum
sampled regularity ratio |kappa|/mu is 0.0005506504, well below one; regularity is
also required during every transformed RHS evaluation.

The MTS coherent-minus-original velocity response has maximum magnitude
2.88188472e-7, ending at -4.54156598e-8 in the phase-aware run. Its paired-step
plus primitive-rounding budget is 5.40855e-6 of that amplitude; direct integration
gives 5.41809e-6. The cross-implementation small-response budget is 8.17027e-6.
These pass the unchanged 2e-5 gate. This response is NOT MTS minus LambdaCDM or
an observed signal.

## Limits retained explicitly

- The baseline response amplitude is only 6.62820e-14 versus a working absolute
  precision budget of 3.40940e-12. Its response-relative gate FAILS (ratio 51.44).
  This does not fail its separately normalized full-source/metric tests. It also
  does not resolve that correction or prove it is zero.
- Independent native controls are evaluated at the two original report times,
  not all intermediate diagnostic points. The MTS original-velocity discrepancy
  already present at the initial endpoint is 1.11891245e-8, about 3.88% of this
  interval's maximum small response. Passing paired refinements or coordinate
  equivalence is not a bound on all inherited modelling/numerical error.
- Numerical budgets are working refinement/rounding estimates, not rigorous
  continuum enclosures. Transform and direct paths share native equations,
  initial data and tables: they are independent coordinate implementations,
  not independent physical models.
- Earlier slow-sector self-normalized identity failures remain. The previous
  conditional slow-stress bound covers 3038..3039 only and is NOT automatically
  extended to 3040. The earlier 87.5966% projected source uncertainty also remains
  separate. No new sky/source projection or quantum-measure result is inferred.
- Cold runs required about 1.17 million RHS evaluations each versus 81,557 in
  each heavy 64-step run. The cause has not been isolated; this is not a physical
  verdict or a reason to drop the baseline/change tolerances.

## Verification and restart

422 verification checks pass, including exact score replay, finite outputs,
unchanged native units, complete restart consistency and cumulative checkpoint
prefixes. Both preflights pass; heavy coefficients/differences and actual
external-density derivatives also pass independent 80-digit controls.
science-score.json deliberately retains all_precision_checks_pass=false.

Complete decoded restarts: cold-direct-64-terminal.npz and
heavy-phase-64-terminal.npz. The latter has the matching exact encoded state and
encoded RHS in heavy-phase-64-phase-terminal.npz. Keep heavy-direct-64-terminal.npz
as the coordinate control. For a future native owner, verify the full known
1050-row prefix while retaining the original 934-row seed/normalization.

The inherited protocol fields strides, quadrature_orders and wording about
phase-root/off-grid work quadrature describe earlier stages; they are not new
tests performed here. This stage's operative tests are CONTRACT.md, score_live.py
and verify_live.py. The frozen protocol is preserved rather than silently edited.
Cleanup and artifact hashes are recorded in cleanup.json and closeout.json.
All work remains private; no publishing, other-chat process changes or new
browser/server is part of this stage.
