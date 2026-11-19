# The conservative reference now drives a paired background

The retained cold and MTS-heavy short backgrounds were actually evolved
with shared neutrino density, pressure and derivatives. Their slow fields,
expansion rate, elapsed conformal time and heavy scalar carrier now use
one consistent reference. No mass or abundance was retuned.

## Results at unchanged gates

| Check | Cold | Heavy |
|---|---:|---:|
| Solver-tolerance difference, normalized state | 7.59e-16 | 9.49e-16 |
| 32-to-64-node reference state difference | 1.86106e-10 | 1.86107e-10 |
| Reference-grid jet difference | 5.40870e-10 | 5.40870e-10 |
| Propagated Friedmann error | 6.66e-16 | 4.44e-16 |
| Pressure/metric clock jet error | 6.70e-16 | 5.20e-16 |

Numerical comparison gate remains2e-5; algebra/constraint gate remains1e-10.
Solver comparisons this small are rounding-limited, not certified precision.
Both branches retain the same33sample positions in Delta ln a=.001.

Expansion differs from the old saved background by about2.029e-8 on the
stored normalization, and elapsed conformal time by about2.030e-8.
These are numerical representation changes, not a predicted observational
signal. Slow-field changes are smaller. Both branches' background changes
are almost identical because their late matter partitions nearly coincide.

## Independent checks

- Native mass/thermal normalization agrees with saved source coefficients
  to<=6.67e-16. Actual native mass/temperature356.5935334924326 and
  amplitude1.902191136579917e-12 Mpc^-2 are unchanged.
- Three exact identities cover scalar energy, propagated Friedmann
  constraint and the pressure/metric clock.
- Independent60decimal differentiation checks30case/position/degree
  combinations through fourth N derivative; largest scaled error2.790e-12.
- Independent60decimal carrier checks agree to<=2.03e-16 at three epochs.
  The pressure piece is retained separately, about-1.67e-14 Mpc^-1,
  and the k5beat is about9.17e-4 Mpc^-1.
- Two finite-difference spacings check background conformal derivatives;
  largest normalized error4.69e-11, below the unchanged numerical gate.

An old-pressure/new-density mixed diagnostic is also recorded. Its residual
is nonzero but only about1.66e-12 of total density in this window: it is NOT
reported as failing a1e-10 aggregate gate. Exact consistency and sampled
numerical detectability are different questions.

## Retained failure and preservation

The initial normalization worker failed a mistaken midpoint-coordinate
check. Its numbers and receipt remain unchanged. The saved midpoint is
conformal-time midpoint, not log-scale-factor midpoint. A separate reader
uses the already saved clock, passes1e-10 and performs no new native run.

All inherited files remain hash-verified. No production action, table,
bank, grid, original native library or Galaxy artifact was edited.
No fits, new coupling, relay/timer, GitHub action or new perturbation
evolution occurred. Background reference outputs are separate and reusable.

Next is the matched perturbation interface and one paired coupled control,
then increased interval/mode coverage—not further refinement of this
already-passing background. See NEXT.md.
