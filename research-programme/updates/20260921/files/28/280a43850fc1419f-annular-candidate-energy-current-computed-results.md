# Gram energy transport and radial mass-current results

Private same-action directional test; inherited coordinate units. Gram-to-mass conversion is a candidate diagnostic.
Global residual ratios use the larger dust-dominated scale; outside-source rows prevent that scale hiding the smaller wave residual.
Observed derivative and quadrature sensitivities are not rigorous error bounds.

| Branch | Phase | Region | Current scale | Bare residual max | Candidate-corrected max | Relative corrected | Derivative sensitivity |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| reference | initial | all | 0.0059258633 | 1.0874041e-10 | 1.0874041e-10 | 1.8350139e-08 | 1.3431819e-10 |
| reference | initial | outside_source | 2.8203076e-05 | 1.9715751e-11 | 1.9715751e-11 | 6.9906384e-07 | 1.0393885e-11 |
| reference | initial | source | 0.0059258633 | 1.0874041e-10 | 1.0874041e-10 | 1.8350139e-08 | 1.3431819e-10 |
| reference | endpoint-wide | all | 0.0059258336 | 1.3749768e-11 | 1.3749768e-11 | 2.3203095e-09 | 5.7303693e-12 |
| reference | endpoint-wide | outside_source | 2.8205047e-05 | 1.3749768e-11 | 1.3749768e-11 | 4.8749318e-07 | 1.3769368e-12 |
| reference | endpoint-wide | source | 0.0059258336 | 9.2663733e-12 | 9.2663733e-12 | 1.5637249e-09 | 5.7303693e-12 |
| primary | initial | all | 0.0059258633 | 1.0862727e-10 | 1.0862727e-10 | 1.8331046e-08 | 1.3443746e-10 |
| primary | initial | outside_source | 2.8203117e-05 | 6.3543424e-11 | 3.8069997e-11 | 1.3498507e-06 | 1.0444481e-11 |
| primary | initial | source | 0.0059258633 | 1.0862727e-10 | 1.0862727e-10 | 1.8331046e-08 | 1.3443746e-10 |
| primary | endpoint-wide | all | 0.0059258336 | 5.2230399e-11 | 3.6665802e-11 | 6.1874506e-09 | 5.7130221e-12 |
| primary | endpoint-wide | outside_source | 2.8205093e-05 | 5.2230399e-11 | 3.6665802e-11 | 1.299971e-06 | 1.3776596e-12 |
| primary | endpoint-wide | source | 0.0059258336 | 8.7412516e-12 | 8.7412517e-12 | 1.4751092e-09 | 5.7130221e-12 |
| alternative | initial | all | 0.0059258633 | 1.0862727e-10 | 1.0862727e-10 | 1.8331046e-08 | 1.3443746e-10 |
| alternative | initial | outside_source | 2.8203117e-05 | 6.3543424e-11 | 3.8069997e-11 | 1.3498507e-06 | 1.0444481e-11 |
| alternative | initial | source | 0.0059258633 | 1.0862727e-10 | 1.0862727e-10 | 1.8331046e-08 | 1.3443746e-10 |
| alternative | endpoint-wide | all | 0.0059258336 | 5.2228953e-11 | 3.6665802e-11 | 6.1874506e-09 | 5.7137454e-12 |
| alternative | endpoint-wide | outside_source | 2.8205093e-05 | 5.2228953e-11 | 3.6665802e-11 | 1.299971e-06 | 1.376214e-12 |
| alternative | endpoint-wide | source | 0.0059258336 | 8.7419785e-12 | 8.7419786e-12 | 1.4752319e-09 | 5.7137454e-12 |

## Same-action Gram power

| Branch | Phase | Global power cancellation | Direct derivative discrepancy | Metric-exchange balance discrepancy |
| --- | --- | ---: | ---: | ---: |
| reference | initial | 0 | 0 | 0 |
| reference | endpoint-wide | 0 | 0 | 0 |
| primary | initial | 8.7267555e-23 | 4.225342e-21 | 1.1397211e-20 |
| primary | endpoint-wide | 1.3710519e-22 | 3.7429923e-22 | 2.3556331e-21 |
| alternative | initial | 8.7060759e-23 | 4.225342e-21 | 1.1397005e-20 |
| alternative | endpoint-wide | 7.6721002e-23 | 4.2847956e-22 | 2.3488862e-21 |

## Matched-grid MTS minus reference diagnostic

| Branch | Phase | Bare contrast max | Candidate-corrected contrast max | Bare RMS | Corrected RMS |
| --- | --- | ---: | ---: | ---: | ---: |
| primary | initial | 4.4423414e-11 | 2.2564072e-11 | 8.1951053e-12 | 4.2549658e-12 |
| alternative | initial | 4.4423414e-11 | 2.2564072e-11 | 8.1951164e-12 | 4.254977e-12 |
| primary | endpoint-wide | 4.4387553e-11 | 2.2916034e-11 | 8.1958684e-12 | 4.2682426e-12 |
| alternative | endpoint-wide | 4.4386107e-11 | 2.2916034e-11 | 8.1961571e-12 | 4.268526e-12 |

All36 predeclared smoke comparisons pass. Passing these loose absolute/relative smoke gates is distinct from resolving the smaller current defect.
The next derivation should construct the discrete wave-energy current and its weak-EL/interface contributions, and the metric/shift variation of the same Gram action, rather than fit a multiple of its energy flux.
