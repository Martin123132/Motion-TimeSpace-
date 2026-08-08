# 5318 - Regulator-specific squared-event outer repair

## Method

Each regulator derives its own support-entry, support-exit, and shared-branch
death coordinates. Panel 9 is partitioned exactly at those events. The
logarithmic endpoint collars use `|x-x_event|=t^2`, while smooth pieces use
ordinary Gauss-Legendre coordinates. No E0025 event coordinate is assumed
to transfer to another regulator.

The normalized Laurent basis `r^2/(E-p)^2`, `r/(E-p)`, and powers of the
dimensionless fit coordinate removes pole-location conditioning artifacts.
Independent interlaced holdout points remain mandatory.

Panel 2 is retained under the same global conservative budget used for the
validated E0025 baseline; imposing a new local-only gate on the four added
regulators would be an asymmetric test.

## Result

- derived regulator events: `12`;
- completed outer nodes: `720`;
- failed outer inner nodes: `0`;
- accepted added regulators: `4` / 4;
- all five finite regulators accepted: `True`;
- decision: **FIVE_FINITE_REGULATORS_CONVERGED__FIT_REGULATOR_ZERO_LIMIT**;
- validation: **PASS**.

| regulator | leaves | panel-9 error | full error | accepted |
|---|---:|---:|---:|---:|
| E005 | 7 | 0.00105785 | 0.00178553 | True |
| E010 | 7 | 0.00101469 | 0.00176554 | True |
| E020 | 7 | 0.000962525 | 0.00174136 | True |
| E040 | 7 | 0.000913507 | 0.0017185 | True |

## Claim boundary

Even if all five rows pass, this is one fixed decay angle at finite
regulators. No regulator-zero, decay-angle, phase-space, UV, local-GR,
or full-MTS claim follows until those later gates are run.
