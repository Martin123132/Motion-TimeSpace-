# Full-bank coupled gravity and the explicit wave-stress photon test

The prediction was generated for all 782 original modes. Each of the four runs contains the same 38 mode blocks and 273 time samples, including incoming derivative support. Cold is the retained cold comparator, not the resolved MTS wave. Original and cold pilot packets remain byte-identical to the previous controls. Tables below use percentages, not fractions.

## Gravity at first order: per-mode change, not absolute level

| Run | Worst error (%) | Mode (k per Mpc) | Fails / 782 | Worst on target triangle (%) | Failed incoming matches | Worst pressure-free work (%) |
|---|---:|---|---:|---:|---:|---:|
| cold | 0.0187952 | 222 (1.2345) | 0 | 0.00935562 | n/a | 0.0187951 |
| fine | 0.108309 | 37 (0.564666) | 0 | 0.108309 | 0 | 0.10902 |
| original | 1.12641 | 37 (0.564666) | 1 | 1.12641 | n/a | 1.13234 |
| primary | 0.0994957 | 37 (0.564666) | 0 | 0.0994957 | 0 | 0.0998161 |

The two corrected tables are primary (phase spacing at most 0.04) and fine (0.02). All misses and their tiny-denominator scales are kept in mode-scores.csv, including whether each enters the first output triangle. On the common original normalization, the worst corrected errors are 0.0999009%, 0.108764%. No mode is dropped. The maximum error in reproducing the signed integrated discrepancy from the separate work terms is 2.07919e-08 percentage points. The maximum cubic/quintic diagnostic spread is 1.60334e-07 percentage points.

## Separate scalar energy and current exchange

| Model, scalar | Worst energy / current error (%) | Failed modes (energy / current) | Median energy error with metric work omitted (%) |
|---|---:|---:|---:|
| original, heavy | 0.13417 / 4.0224e-05 | 0 / 0 | 416.923 |
| original, slow | 0.140399 / 0.0528278 | 0 / 0 | 1505.14 |
| primary, heavy | 0.0122938 / 3.67267e-05 | 0 / 0 | 416.887 |
| primary, slow | 0.140384 / 0.0528284 | 0 / 0 | 1505.14 |
| fine, heavy | 0.0130446 / 3.68674e-05 | 0 / 0 | 416.887 |
| fine, slow | 0.140385 / 0.0528284 | 0 / 0 | 1505.14 |
| cold, slow | 1.1868e-08 / 1.41892e-09 | 0 / 0 | 191967 |

The common metric does work on the scalar. Incoming stress is carried rather than reset. The two laws use the actual scalar pressure; see EXCHANGE.md for equations and exchange.json for error and quadrature controls. Ordinary massive-species pressure was not separately measured by this test.

## Radiation and quadratic source predictions

| Model | Largest photon energy / current readout change (%) | Number outside 0.5% |
|---|---:|---:|
| original | 2.98489e-05 / 0.00205544 | 0 / 0 |
| primary | 1.73614e-06 / 0.000107802 | 0 / 0 |
| fine | 1.93005e-06 / 0.000118136 | 0 / 0 |
| cold | 4.08464e-07 / 3.15056e-05 | 0 / 0 |

The radiation table changes only the gravity readout on a fixed linear solution. Its volume-density identity cancels to 1.31792e-14% of the level. It is not a residual against a measured sky spectrum.

All five spatial outputs, ordered as in driving-scores.json, were retained for the real preparation. For the original wave the maximum replay errors over all 15 driving channels and 121 forward reference samples are 6.2987e-05% of level and 0.00067614% of change. The cold control has only 17 published-to-workspace incoming samples in this source chain through the join; its nine channels replay to 0.000110275% of change on those samples. A complete late cold solution has been generated here without a second late cold archive to compare against.

At the target (4,2,1), changing from the original to the fine wave alters explicit quadratic heavy energy/current by 0.00326432 / 0.000137592% of their original changes. The primary/fine spread is 5.54095e-05 / 1.38849e-06%. Using integrated shear in place of algebraic shear on the *same* fine solution alters them by 0.000415129 / 1.68766e-06% of their changes. These are distinct effects. For explicit heavy pressure and its density-constraint numerator the fine-minus-original changes are 5.74403e-05 / 0.00302429%. The driven field and compensator also contribute to total stress.

## What reaches the visibility distribution

Hold the resolved state, its metric denominator, the matched branch and all other forces fixed. Insert the *difference* in three explicit resolved heavy stress channels into the two-route transfer. The following test measures the direct term only, not a rerun of the 77-bin state. Gap units are percent of the original small photon correction, not percent of the CMB.

| Grid / table | Prior joint gap | Direct term norm | Signed contribution (points) | Conditional gap with entry | Conditional gap without entry |
|---|---:|---:|---:|---:|---:|
| p16 / primary | 0.659717 | 0.0807347 | -0.00787927 | 0.656771 | 0.656664 |
| p16 / fine | 0.659717 | 0.0821687 | -0.00885345 | 0.65597 | 0.655875 |
| p32 / primary | 0.659708 | 0.0807348 | -0.00786056 | 0.656781 | 0.656674 |
| p32 / fine | 0.659708 | 0.0821688 | -0.00883443 | 0.655981 | 0.655886 |

The independent transfer of the saved interval reproduces its photon vector to 1.16573e-12 percentage points. The norm above bounds the improvement available from **these terms alone with other fields held fixed**. It does not bound responding matter, metric force, perturbed wave, phase preparation or feedback.

## Reproduction and limits

Use the retained Python 3.13 native environment with numerical libraries restricted to one thread. generate_bank.py reuses the four sealed pilot packets. After all-forecast.json: score_bank.py, exchange.py, project.py, driving.py, photon_probe.py, report.py then verify_bank.py. The stage uses write-once data and separate forecast/score receipts. The raw native numerical warnings are preserved in native-run.log. This is a numerical field-equation test on the retained preparation, not a fit. No changes to GitHub or old checkpoints by this stage.

Run entry_correction.py after photon_probe.py and before report.py: it restores the complex boundary impulse omitted by a real cast in the first transfer. The corrected forecast in photon-complex.npz keeps every interior vector unchanged. Its independent real/imaginary controls are in entry-check.json. The largest reported quadrature spread for the fine heavy energy/current conservation errors is 0.000983227 / 0.000325804 percentage points; interpret very small residuals with this numerical floor. Six native Romberg warnings are retained: the largest stated integration error is 1.46e-13, versus 8.32e-14 requested, for an integral near 192.58.

## What is worth propagating next

By the reverse triangle inequality, the smallest joint gap obtainable even by perfectly aligning the *measured norm* of the direct correction against the old gap is 0.57754% on p32. Thus these three explicit stress terms cannot reach 0.5% on their own at this size. Their actual signed projection is only -0.00883443 percentage points; most of the vector does not cancel the discrepancy. Following the direct change, at least 0.155981 further points of appropriately directed response are needed on the original small-signal scale.
Next propagate the corrected force packet, not a tuned rotation of that vector: keep the separate resolved and matched states at 89.65, change the resolved metric and scalar forcing together, evolve ordinary matter, gravity and the 77 momentum bins, and compare the resulting photon vector on p16/p32 to its direct-only prediction. In particular U and Qf/Qw may change the later state even when direct energy/current cannot close the gap. Keep any source not yet supplied identical and label it; do not silently apply the resolved physical orientation to the phase-averaged matched branch.
