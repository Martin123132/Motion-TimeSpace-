# Stage147 — the small cubic correction survives time-step refinement

16 October 2026. Private/local continuation of Stage146. Frequency grid and
repaired physical sources remain fixed; no new event or virtual-loop work.

## Controlled test

Reused the saved 1024-step response and ran 2048 and 4096 steps in each of the
active and transfer phases, for heavy/cold backgrounds and both profile joins.
All runs use the same 96 modes, collision/emission banks, initial states,
source interpolation and unchanged integrator. Both phases are refined
together. Comparisons use exactly shared epochs, not temporal interpolation.

The small colder-point increment is evolved as its own column. Its convergence
is measured against its OWN signal, never against the much larger baseline.
The physical baseline and old-window readout are reused unchanged and receive
the same temperature/mu/y/residual decomposition as MTS and baseline+MTS.
This does not claim a new refinement of the baseline's inner history.

## Result: all predeclared convergence gates pass

Largest relative changes in the isolated correction between 2048 and 4096
steps, across the tested histories and joins:

| Quantity | Finest step change |
|---|---:|
| Final mu amplitude | 0.00011511% |
| Final y amplitude | 0.00027291% |
| Final photon response, mass norm | 0.00019818% |
| Photon trajectory, normalized by its own peak | 0.00305138% |
| Final gas response, normalized by its own peak | 0.000096764% |
| Gas trajectory, normalized by its own peak | 0.000575371% |

The predeclared target was 1%, including the small increment itself. The
original and revised MTS responses and old-window control also pass the
same finest-grid convergence checks. Zero-extra-source columns remain zero.

The mu step differences contract by factors 0.250157--0.250163 and y by
0.250625--0.250626: approximately fourfold smaller when the step is halved.
Their observed convergence orders are 1.9991 and 1.9964 respectively.
Photon trajectory differences also shrink, with observed orders about
1.84--1.89; they are not falsely described as exactly second order.
None of the isolated-increment contraction passes relies on the numerical-
floor exception. These are observed step differences, not rigorous bounds
on the continuum solution or on the physical event quadrature.

## Physical readout remains stable

At the saved final epoch a=1e-5, the 4096-step isolated contribution has:

- mu: +3.27742e-19 to +3.28068e-19;
- y: -1.18523e-20 to -1.18361e-20.

Relative to the original combined MTS windows, the correction remains about
-0.001407% to -0.001411% in mu and -0.014133% to -0.014162% in y. Mu is
negative for that combined response, so its magnitude decreases slightly.
Combined y remains positive, about 8.36830e-17--8.37352e-17.

As an additional scale check, the original new-window response's own final
mu/y changes from 2048 to 4096 are less than 0.34% / 0.096% of the small
correction, respectively. Thus this result is not obtained by hiding a
larger total-response step shift underneath the small correction.
The source for these ratios is the saved spectral_comparisons table:
abs(original.signed_changes[1])/abs(increment.amplitudes[2]).

## Consistency and preservation

All 414 scientific checks and 61 validation checks pass, with no new failures.
The maximum energy-plus-expansion-work residual is 1.654e-13 relative.
The maximum source rewrite stays below 2.693e-11 against the unchanged
1e-10 gate. Original photon/gas equations, photon-number accounting, direct
superposition and independent per-column spectral decompositions pass.

All 285 consumed or immediate-parent files were rehashed. Six scripts compile
without bytecode. The protected workbench has modification-time change count
zero. All prior forecasts, failures and source repairs remain sealed and
unchanged. No GitHub action, subagents, installs or galaxy changes occurred.
Only two single-core below-normal workers were used for the response runs;
all owned computation is finished before sealing.

## Next

Extend the physical source into the next colder temperature interval using
the already evaluated endpoint. Keep this interval and its convergence
evidence fixed rather than repeatedly refitting these temperatures.
The new interval's inner-history feedback and event-quadrature uncertainty
remain separate questions; this checkpoint isolates response time stepping.
