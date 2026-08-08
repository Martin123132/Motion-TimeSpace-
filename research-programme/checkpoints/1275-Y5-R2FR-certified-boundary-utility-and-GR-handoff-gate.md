# 5259 — Certified boundary utility and GR-handoff gate

## Purpose

Checkpoint 5258 proves a continuous residue envelope over all four active
transition brackets. This checkpoint asks the next question: is that
certificate already tight enough to preserve the outer coefficient and pass
the result toward the GR-linked reconstruction?

The answer is **no**. The theorem gate is closed, but the present enclosure is
too conservative for the numerical stopping gate.

## Inputs

The gate compares:

- the certified checkpoint-5258 half-residue envelope and boundary-location
  error;
- the checkpoint-5256 equal per-boundary budget
  \(B_{\rm eq}=0.6052369604865984\);
- the earlier sampled envelope, used only to measure interval inflation.

For a certified envelope \(E_C\), the target bracket width is

\[
\Delta x_{\rm target}
=\frac{B_{\rm eq}}{(1/4)E_C}.
\]

If the enclosure is held fixed, the additional binary bisections are

\[
n_{\rm bisect}
=\left\lceil
\log_2\frac{\Delta x_{\rm current}}{\Delta x_{\rm target}}
\right\rceil.
\]

## Utility result

| transition | certified/sample ratio | error/budget ratio | target width | fixed-envelope bisections |
|---|---:|---:|---:|---:|
| I01_T00 | 110.922 | 2,582.481 | \(5.2200\times10^{-6}\) | 12 |
| I01_T01 | 48.383 | 1,891.083 | \(7.1285\times10^{-6}\) | 11 |
| I06_T00 | 133.418 | 7,611.048 | \(1.7712\times10^{-6}\) | 13 |
| I06_T01 | 110.922 | 2,582.482 | \(5.2200\times10^{-6}\) | 12 |

The former sampled estimate suggested five or six more bisection generations.
Using the present certified supremum without tightening would require eleven
to thirteen. That is mathematically safe but computationally wasteful.

The reflected I01_T00/I06_T01 certified envelopes agree with relative
difference

\[
4.8622707552\times10^{-7},
\]

so the inflation is not evidence of a broken reflection or a random branch
selection. It is dominated by interval dependency and chart conditioning.

## Decision

`HOLD_GR_HANDOFF__TIGHTEN_CERTIFIED_ENVELOPE_BEFORE_MORE_TOPOLOGY_GENERATIONS`

The next route is:

1. derive centered/Taylor interval forms for the regularized amplitude in the
   outer coordinate;
2. target the largest inflation first, especially I06_T00;
3. rerun the utility gate;
4. use additional topology bisections only after the certified envelope is
   near the sampled scale.

This avoids spending eleven to thirteen expensive topology generations merely
to compensate for a loose interval representation.

## What is now certain

- The exact quadratic branch is simple and separated on every retained box.
- The lower-point regularized amplitude matches the parent expression.
- The non-active global roots remain outside a certified Cauchy disk.
- A finite continuous residue supremum exists for every transition and both
  regulators.
- The D01A/D06B reflection survives interval certification.

## What is not yet established

- The certified boundary error is not within the outer budget.
- The outer coefficient is not yet numerically locked.
- The numeric UV coefficient is not claimable.
- No local-GR or full-MTS claim follows from these checkpoints.

This is not a return to the old “missing envelope” loop. The envelope is now
derived and certified. The remaining problem is quantitative sharpness, with
a measured inflation factor and a selected repair route.

## Machine-readable evidence

- `source-intake/functional_rg/5259/certified_boundary_utility_gate.csv`
- `source-intake/functional_rg/5259/certified_boundary_utility_validation.csv`
- `source-intake/functional_rg/5259/certified_boundary_utility_result.json`
- `scripts/Y5_R2FR_5259_certified_boundary_utility_and_GR_handoff_gate.py`
