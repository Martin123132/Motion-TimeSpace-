# Coherent projection and derived pressure/phase transport — 2026-11-10

This stage keeps the retained action and physical state. It finishes the saved
phase-projection calculation, derives its gauge/metric product corrections,
then constructs and tests a nonsingular first-order phase-stress representation
when a second-derivative pressure prediction proves poorly conditioned.

## 1. Original extraction retained

The original a225-w6-d8 k1 density/current/pressure and mode norm are reproduced
before repaired histories are examined. All902 selected epochs,29 basis
columns and weights are frozen. There are429 negative weights; sum|w|=1.70244.
This is the same signed secular extraction, not a newly chosen positive
ensemble. The original mode norm is5.5516538582214014, pressure gate2e-6.

The repaired heavy pressure is-0.0002250062405401436 in the original normalized
units. The retained algebraic pressure law gives-0.00022465306046513095.
Their discrepancy is3.53180e-7 absolute,6.36171e-8 of the original mode norm,
so the OLD gate still passes. Pressure-relative error is0.156965%; do not
substitute the mode-normalized error for pressure-relative precision.

## 2. Gauge/metric product corrections derived and verified

Projecting products is not multiplying projected factors. The exact correction
to the heavy gauge-transformed projected pressure is-6.14315e-9, or2.73018e-5
of that small pressure. Density/current corrections are8.89015e-11 and
8.10383e-10 in the original normalized units. Applying the derived covariance
terms reproduces direct coherent-source projection at the1e-10 algebra gate.

The total metric-potential correction from the H*Q product is-1.02726e-12,
about1.21908e-9 of the projected MTS potential. The cold-control term is
5.21815e-20, at floating cancellation scale relative to its potential.
These are representation/projection terms, NOT new forces or fitted stress.

The pressure's removed2theta harmonic has peak5.65576, versus its secular
magnitude0.000225006. This explains why retaining phase information matters.
The large oscillatory amplitude is not itself an observational exclusion:
its time-integrated dynamical effect requires the corresponding equations.

## 3. An informative failed representation

From the KG equations, Z=a*b*us obeys

    2a*Ps=Z''+(k^2-H^2-H')Z+a*k*z*b*v-(source-defect terms).

Fitting only Z to the already-frozen basis, not fitting pressure, predicts
heavy pressure with1.18653e-7 absolute error:0.0527332% pressure-relative,
2.13725e-8 in the historical mode norm. The clock-resolution sensitivity is
9.34148e-11 absolute. This heavy prediction passes the original pressure gate.

However, the SAME calculation on the slow field fails in BOTH controls.
Cold absolute error8.33523e-18 versus actual pressure1.65156e-24; MTS slow
error3.67605e-18 versus7.93281e-25. Terms hundreds of trillions of times larger
than the result are subtracted. A small displacement-fit residual is not a
bound on this pressure. Those failures remain saved, not promoted as passes.

## 4. Derived first-order repair: carry phase/stress, not a cancellation

PHASE-MEMORY-TRANSPORT.md derives M=B U^T, with
B=(b,v/omega), U=(us,ws/omega), omega=sqrt(k^2+mu^2). The physical rank/direction
constraints keep this equivalent to ONE coherent real scalar. The state is
initialized directly from saved native fields/velocities, with no free phase,
pressure fit, effective sound-speed fit or additional populated quadrature.

Its matrix evolution follows by differentiating the outer product. The
retained background interpolation defects enter only the representation's
background derivative; neither the action nor native perturbation force is
altered. The pressure readout uses the actual kinetic/potential products,
avoiding the huge displacement/metric subtraction that failed above.

Six fine2/fine4/coarse4 runs pass history, step, source, recovered-field and
physical-subspace tests at UNCHANGED tolerances on the902 frozen epochs.
These are FORCED-HISTORY representation tests against the saved coupled
native solution; no new self-consistent metric evolution is claimed here.

| MTS heavy run | Worst source/field history error | Projected pressure absolute error | Pressure-relative error |
|---|---:|---:|---:|
| fine2 | 1.89527e-6 | 1.67728e-10 | 7.45436e-7 |
| fine4 | 1.18681e-7 | 1.35235e-11 | 6.01028e-8 |
| coarse4 history | 1.18614e-7 | 5.47880e-11 | 2.43495e-7 |

The fine4 heavy pressure error is2.43594e-12 of the unchanged historical mode
norm. Baseline slow fine4 pressure-relative error2.89147e-15; MTS slow
fine4 error3.33964e-12. These are numerical representation comparisons to a
common reference, not claims of cosmological accuracy to that many digits.
The stronger per-entry physical-subspace check also passes; worst heavy
deviation1.54918e-6(fine2),9.66372e-8(fine4),9.90900e-8(coarse4).

## 5. Verification and preserved failures

Thirteen symbolic identities derive the virial/defect relation, matrix
transport, source readouts, invertible recovery and product commutator.
The verifier recomputes137 comparisons, checks3391 source hashes and compiles
all local scripts without bytecode. It separately records:

- fixed_projection_reproduced=true;
- gauge_metric_commutators_validated=true;
- heavy_virial_pressure_gate_passed=true;
- paired_virial_prediction_passed=false;
- paired_phase_transport_passed=true;
- forced_history=true; new_coupled_phase_transport=false.

The first validation caught a mismatched coarse/native algebra input. Its
code and failed receipt remain. The diagnosis and corrected same-state check
are in VALIDATOR-REPAIR.md; no evolution or tolerance changed. Use
verify_projection_consistent.py for validation/seal verification, not an
identical retry of the initial verifier. All task-owned worker exits and seal
integrity are checked separately. No native rebuild, downloads, GitHub,
Galaxy edits, relay, timer, browser, subagent, process kill or shared-service
change. The coherent state and original external initial conditions remain
inherited; this stage does not select a galactic population.
