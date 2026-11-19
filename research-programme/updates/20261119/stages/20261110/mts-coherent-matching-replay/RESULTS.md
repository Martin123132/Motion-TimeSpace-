# A dynamical test exposed and locally repaired a background inconsistency

10 November 2026. Continuation of the retained MTS scalar action and saved
early calculation; no new fit, coupling, field, population or release law.

## Original test: preserve the mixed result

The interval is frozen at saved indices2292--2591:299intervals, phase1424.35497
to1436.87945 about the original a225center. There are316guarded input samples
and160coarse-history samples. Each case retains its own actual clock and a.
Six runs finished: baseline/MTS x fine2/fine4/coarse4. The metric is externally
supplied from the original history; this is not a new coupled cosmology.

- The heavy-field physical readouts pass: the largest fine4 normalized
  discrepancy is2.11262e-6 (compensated density), against2e-5.
- The cold-fluid control passes in both cases, max1.18152e-7.
- The baseline slow field/current miss the unchanged gate: field7.23557e-5,
  absolute1.18262e-21. Its other saved source readouts pass.
- The MTS slow field fails substantially: field0.19538443, momentum0.12095905;
  density0.11681449 and current0.19453041. Its absolute field difference is
  1.54634e-16 and absolute density difference4.11022e-30Mpc^-2.
- Time-step refinement is<=1.019e-14baseline and5.681e-8MTS. Changing the
  driver-history sampling gives<=2.147e-7baseline and1.722e-7MTS; withheld
  metric sample discrepancies<=2.915e-7. These do not explain the large
  MTS slow-field discrepancy. Do not mark the original paired replay passed.

## Derived diagnosis, not a guessed patch

The heavy-case slow velocity table has a background-equation defect with
peak6.17309e-15Mpc^-2, or0.510027 of its peak equation-component sum. The
baseline's corresponding normalized defect is1.51546e-10. The old background
builder used a common1e-13absolute tolerance on field and tiny dimensionless
velocity, with max_step=.04 in ln(a), through an oscillatory heavy background.
Its H/flatness checks did not test this tiny velocity's on-shell accuracy.

Differentiating the actual gauge map derives the background defect ports.
With NO fitted coefficients, their response reduces the MTS slow field
discrepancy to2.20837e-6 and momentum to8.62822e-7. This identifies the
dominant numerical problem. Those ports are error diagnostics, not new
physical forces to be inserted into the action.

The previous early-state recovery remains a faithful extraction of the
saved real field/velocity and an algebraic source check. Its interpretation
as true canonical momentum assumed an on-shell background; this stage
finds that assumption numerically inaccurate for this old slow table.
The conditional derivation is not discarded, and the previous files are
not rewritten to hide the discovery.

The saved metric-transfer columns are confirmed float32-origin. The small
baseline discrepancy lies within a documented, non-certified rounding
estimate; this cannot explain the much larger MTS defect. The noisy
derivative-based metric diagnostic is retained, not accepted as a repair.
See PRECISION-NOTE.md for the assumptions and limits of that estimate.

## Tested local repair from the same action

Use J=a^2*b' and a separately represented tiny field offset:

    J'=-a^4*m_s^2*b,    (b-b_start)'=J/a^2.

This removes the tiny-velocity absolute-tolerance problem without changing
the mass or field normalization. An independently implemented synchronous
momentum W_s=w_s-v*delta_c removes the need to differentiate noisy metric
columns. Its transformation back to Newtonian canonical coordinates is
derived explicitly, not fitted to the original trajectory.

Four local runs (two/four substeps in each case) pass the unchanged numerical
gate. At four substeps, the independent coordinate/source implementations
agree to4.571e-11baseline and7.403e-11MTS; direct time-refinement differences
are<=9.877e-15. The local MTS slow velocity changes by1.05245% of the old
window's velocity peak; the largest induced homogeneous energy change is
2.668e-25 of3H^2 (baseline7.930e-27). This supports a fixed-metric local
bridge control, not a full regenerated early universe.

The new local repair inherits the saved starting velocity, so it does not
establish that velocity's primordial accuracy. It is deliberately not scored
as reproducing the old off-shell history. Original failures remain false;
the separate local repair and gauge-control result is true.

## Ownership and continuation

All original banks, actions, parameters, grids and tolerances remain intact.
No native rebuild, new data, fit, Galaxy edit/relay, GitHub action, subagent,
browser, timer or other-worker intervention occurred. Only the new private
folder and resume bookmark change. Worker exit receipts and hashes accompany
the closeout; an implementation-validation pass must not be mistaken for
passing the original paired physics comparison.

NEXT.md targets a stable early-initial-condition repair and full-precision
native state/readout before the self-consistent coupled handoff.
