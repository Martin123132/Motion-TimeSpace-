# Separate the independent checker step from the physical metric step

Restoring the missing map derivative factor removes the large chain failure. The corrected heavy preflight still stops at a density-coordinate independent finite-difference error of 2.09699e-5 versus the fixed 2e-5 gate. The remaining failed attempt and its native-release receipt stay unchanged. No heavy evolution has yet been performed.

A separate paired cold/heavy diagnostic evaluates the same independent derivative at eight step sizes. The physical current-metric derivative remains span/8192 throughout; no physical equation or integrator is run or altered in this diagnostic. Heavy density-chain normalized errors are:

| Checker divisor | Error |
|---|---:|
| 256 | 6.17774e-4 |
| 512 | 3.17833e-5 |
| 768 | 4.65921e-6 |
| 1024 | 5.47696e-6 |
| 1536 | 3.54916e-5 |
| 2048 | 2.09699e-5 |
| 4096 | 2.22459e-5 |
| 8192 | 1.45983e-4 |

The heavy current coordinate is also within tolerance at both768 and1024. All cold checks pass. The observed fall at initially smaller steps and rise/irregularity at very small steps are consistent with a truncation/evaluation-noise balance in the independent subtraction-based checker, not a failure that can be repaired by arbitrarily halving its step. These observations are not a rigorous rounding-error certificate.

Before the first heavy evolution, run_balanced_live_memory.py freezes checker divisors768 and1024, requires BOTH paired diagnostic results to pass, and retests BOTH against the two retained physical metric steps. This is an explicitly diagnostic-informed selection, not a claim that these checker steps were preregistered before the scan. The tolerance stays2e-5; physical metric steps stay span/4096 and span/8192; physical integration remains span/128 and span/256 with unchanged solver tolerances. All eight diagnostic outcomes and both original failed preflights remain available.

The correction to the physical map derivative is independently the exact product rule documented in MAPPING-DERIVATIVE-REPAIR.md; it is not determined by choosing a checker step. This balanced check does not change the candidate equation, source coupling, seeds, bank or output grid. Successful future evolution must still meet native-state, actual-derivative, source, cache, residual and numerical refinement gates.
