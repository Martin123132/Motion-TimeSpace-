# Coupled background response calculated and checked
16 November 2026. Private, manual continuation; the persistent goal stays paused.

## Actual advance

We have evolved one coherent background correction rather than replacing
pressure alone. The scale factor, both populated scalar modes and the
Friedmann response evolve together, with the retained ordinary
matter/radiation/massive-neutrino density. The baseline contains its own
slow mode. No masses, populations, normalizations or couplings were fitted.

Each case starts at ONE earliest common saved anchor and is followed
continuously across the overlapping preparation/history domain. Both
32/64 step choices are sampled at the original33x902 physical queries,
through report2924. No reset is made at the902 individual preparation times.
The independent control evolves the absolute background equations, without
defect subtraction, from exactly the same initial values.

The accepted background representation is in segmented-response.
Use its exact nonlinear correction. All old checkpoints and the first
attempt in this folder are preserved.

## What passed

The MTS background passes all68 frozen checks:
- Analytic Jacobian tests at three clocks and both original stencil steps.
- Absolute-state versus defect-response agreement, worst normalized
  difference5.487781195e-12 against1e-10.
-32/64 correction-relative refinement, worst1.590921658e-7 against2e-5.
- Linear versus nonlinear response, worst1.657688970e-5 against2e-5.
  This is close enough to the gate that the nonlinear background should
  remain authoritative, not be replaced by the linear approximation.
- Shared-anchor and finite-domain checks.

Maximum MTS relative scale correction is2.153552946e-11. The heavy field
and velocity corrections reach7.802527663e-7 and7.463650153e-7 of their
original phase amplitudes. These are background-representation corrections,
not measured cosmological fit improvements.

The source-interface check passes38 baseline and52 MTS checks. It uses
stable algebraic source differences, independent80-digit direct arithmetic
at selected nodes, original source-map recovery, and full-state/source
refinement controls. Cached source reports and arrays replay exactly.
The full ODE trajectories were independently computed at two step sizes;
they were not rerun merely to obtain an exact-bit trajectory replay.

## Baseline limitation retained, not waived

Baseline absolute-state/control, source-interface and linear/nonlinear
checks pass. Four correction-relative entries still fail: scale and slow
velocity, each in linear and nonlinear form. Thus the combined flag
all_background_checks_passed remains FALSE even though the MTS response
passes and the source interface passes for both.

The baseline relative scale correction is4.245845672e-16; its32/64
difference is7.269274423e-19, giving relative0.00171209 versus2e-5.
The slow velocity correction is3.629484443e-26; its refinement difference
is1.079679413e-30, giving2.97475e-5 versus2e-5. Such small corrections
are numerically delicate; a claim of correction-relative convergence is
not justified. Their small absolute sizes and source-scale checks answer
different questions and do not erase these failures.

The normalized cold source is unchanged when its perturbation is frozen,
as required by the retained CDM readout. This does not imply zero change
in the bare gravitational density or in a future evolved cold perturbation.

## Numerical repair, with the failed run preserved

The first unsplit, original-phase-normalized response failed heavy
absolute agreement and refinement. At the fine step its heavy
field/velocity disagreement was about1.93e-10, above1e-10.

Before testing the repair, we froze two numerical changes for BOTH cases:
1. Split integration at the original clock and field-spline boundaries:
   298 baseline segments and733 MTS segments.
2. Express the correction in units1e-7 times the original phase units.
   Solver rtol1e-10 and normalized atol1e-12 stay fixed; this makes the
   requested PHYSICAL absolute accuracy stricter, not more permissive.

Original physical maximum steps, query grids, spline coefficients, source
bank, weights, physical parameters and acceptance gates remain unchanged.
The first failure and its source-interface replay remain at the root;
the repaired results and replay are in segmented-response.

## Source sensitivity, not a substituted prediction

At frozen saved perturbations, the stable MTS source increments are:

| Channel | Maximum absolute increment | Increment/original source scale |32/64 error/increment scale |
|---|---:|---:|---:|
| Density |1.18480994544e-8 |2.51889673107e-7 |2.23253331315e-8 |
| Current |1.08746648034e-10 |3.14921302444e-9 |8.24725508297e-8 |
| Pressure |1.41449939947e-10 |5.57310536160e-7 |1.76683367962e-7 |

The fixed-state source increments and their refinement tests fit the
unchanged2e-5 source gate. Final pressure increment is8.053746414e-11
in the retained native source units. The readout changes density and
current as well as pressure; metric forcing is not silently frozen.

This is not the previous derivative-substitution diagnostic, and it is
not a completed corrected spectrum. No zero environmental response has
been imposed on the theory. Changes to the perturbations, surrounding
species and matched preparation still need their own coupled evolution.
The previous Hilbert-readout pressure failure remains recorded; it is
not relabelled as passed because this different partial calculation is small.
Quantum-measure questions remain separate.

## Reproduction and authority

- protocol.json, DERIVATION.md: frozen first-attempt equations and settings.
- run_response.py, cold/heavy-result.json: preserved first attempt.
- segmented-response/protocol.json and DERIVATION.md: frozen repair.
- segmented-response/cold-result.json and heavy-result.json: background results.
- segmented-response/interface-result.json and interface-replay.json:
  stable source checks and exact cached replay.
- verification.json: consolidated consistency checks, separate from scientific
  acceptance flags; verification-replay.json checks exact report replay.
- CLEANUP-VERIFIED.json and closeout.json: worker exit and artifact receipts.
- NEXT.md: the bounded physical continuation.

Python3.13, NumPy, SciPy, mpmath and psutil plus the frozen retained
modules are required. Run each response case once in a fresh stage
directory; outputs refuse overwrite. check_interface.py --replay reads
the saved results without redoing the background integrations.

The next step is to carry the accepted common background through the
existing matter/metric/environment preparation and exchange equations.
Do not add epochs, fit a new source coefficient or substitute a new theory.

