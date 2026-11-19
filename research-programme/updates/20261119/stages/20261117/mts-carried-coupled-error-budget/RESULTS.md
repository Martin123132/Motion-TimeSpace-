# Continued to3042 with inherited error and correction memory

Private/local, 2026-11-17. This stage makes verified progress toward accountable
derived dynamics; it does not replace the retained parent formulation.
Read CONTRACT.md and science-score.json for the frozen definitions and scores.

## Physical continuation

Baseline direct32/64 and MTS coupled32/64 continue original3041..3042. Each
starts from its OWN saved32 or64 state, so earlier numerical differences are
propagated rather than erased by a shared fine restart. MTS retains the full
parent, approximation, live homogeneous background, K1/K2, defect work and
transported error. Matching of physical fields remains at3040; K and error
are not reset. The error split is referenced to3041.

The interval spans0.9813381224690829 conformal Mpc for MTS, with630 diagnostic
samples; baseline spans0.9813379823532671 with244 samples. Original bank,
parameters, native binary, grids,934 seed/norms and1e-10/2e-5 gates are unchanged.
All1052 owner capture rows are exact. No supplied future metric/source history
drives the solution; retained background/thermodynamic tables remain inputs.
No new data, fit, coupling or quantum-measure assumption is introduced.

## New derived error budget

Evolving h'=A h from the earlier error, alongside f'=A f-r from zero, gives
e=h+f. The full retained operator includes metric and surrounding-species
feedback. For each linear value observable, its signed error is C+F and the
exact triangle bound is |C|+|F|. This separates error inherited from the first
window from newly generated error instead of allowing their cancellation to
hide either contribution. Numerical refinement, primitive rounding, signed
control and physical trajectory allowances are included in the WORKING envelope.

The split is independently evolved, not obtained by subtracting one stored
component from the other. Maximum normalized state/RHS identity residuals are
6.1017607e-13 and2.0586920e-12, below1e-10. Source/readout split identities have
maximum relative residual4.0608814e-15. These numerical estimates are not a
certified interval-arithmetic enclosure or a global nonlinear stability proof.

Coherent-branch results (native/source units, not SI observables or fit gains):

| Quantity | Carry amplitude | New amplitude | Max triangle | Envelope/original norm |
|---|---:|---:|---:|---:|
| Weighted density |1.62715e-9|2.10121e-9|3.60268e-9|7.57518e-8|
| Weighted momentum current |1.55273e-10|1.56183e-10|2.38911e-10|3.36615e-9|
| Weighted pressure |1.63021e-9|2.00062e-9|3.03422e-9|6.36163e-9|
| Native velocity readout |2.82575e-10|8.96860e-10|1.17335e-9|1.69689e-7|

Individual amplitudes need not peak at the same time. Every source/readout
working envelope passes2e-5 of its original norm and covers the corresponding
observed parent/approximation discrepancy. The largest normalized envelope is
1.6968885e-7, about118 times below that gate for this tested interval.

Cancellation is measurable: the velocity triangle is1.453 times its signed
error amplitude; photon density1.724 and velocity slip1.836. At the endpoint,
the coherent velocity contribution from earlier error is+2.55823e-10 and the
new contribution is-8.68738e-10. The budget retains BOTH magnitudes instead of
reporting only their smaller sum. This is why the carried split is useful.

## Independent validation and retained failures

The prospective contract uses the validated signed-control measurement, not
the unresolved tiny difference of two large physical trajectories. Four
independent probes, both signs at16384 and65536, start from the separately
checked3041 error and evolve through the same live linear operator. They are
numerical controls, not alternative physical MTS models. Initial reconstruction
is checked; they do not supply a force to the unamplified physical solution.

All signed source/readout precision checks pass. Largest error-relative budget
1.6936295e-6; cross-amplitude agreement2.0923591e-6; center recovery of the
independent parent3.2926443e-10 on the original full norms. The old subtraction
gate remains false in the previous immutable stage, and the new subtraction
diagnostics still do not resolve all tiny errors. Neither failure is relabelled
as a pass. The replacement measurement was frozen before this NEW interval.

All raw physical/exchange/pressure/metric and original-native endpoint controls
pass for baseline, full MTS parent and MTS approximation. Largest raw main
budgets are4.24124e-8 baseline,4.31465e-8 full parent and1.15200e-7 approximation.
Actual approximate metric derivatives include the retained residual correction;
defect-accounted exchange is supplementary and also passes, not a substitute
for the raw gates. Maximum coefficient inverse-bound diagnostic0.0611199546<1.

The small coherent-minus-original native-velocity response is~3.02403e-7 for
parent and approximation. Their separate step/rounding precision budgets are
5.24743e-6 and5.25674e-6 of that amplitude and pass2e-5. Baseline's tiny response
~7.26164e-14 remains unresolved against3.48108e-12 (relative47.94, FAIL). Do not
interpret full-scale baseline agreement as a resolved tiny baseline signal.
No observation or generalization gain is claimed. Independent-native,
slow-sector and earlier projected-source uncertainty remain separate.

## Restart, verification and cleanup

The authoritative new full-parent states are `cold-64-terminal.npz` and
`heavy-64-parent-terminal.npz`. The matched approximation is
`heavy-64-approximate-terminal.npz`. Use `heavy-64-terminal.npz` to continue
the COMPLETE experiment: it retains total transported error, carry/fresh split,
K memory, defect work, parent, physical approximation and signed controls with
the ACTUAL RHS. `heavy-64-transport-terminal.npz` is the verified physical/core
subset. Do not confuse direct-control native checkpoint RHS with actual
residual-modified RHS. Retain matching32 files for cumulative refinement.

The next continuation should carry the COMPLETE state, including the current
split and probes. Keep the split anchor3041 and original matching3040; do not
create a new zero-error history at every report epoch.

All175 technical checks pass, including score replay, original unit/layout
continuity, actual metric derivative checks, nonzero inherited memory and
fresh-owner BITWISE final full/core RHS plus parent/approximate source restore.
Cold8/heavy34 initial checks pass. Closeout verifies all frozen inputs and exact
owned process exits. Seven native owners are released, including the final
fresh-owner check. No browser, subagent, server, native rebuild, downloads,
GitHub, scheduler or other-chat process changes. Only this private stage and
the current resume note are changed. Whole MTS goal remains active/unfinished.
