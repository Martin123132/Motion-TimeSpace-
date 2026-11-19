# Coupled memory closes; a reversible source state follows

Private retained-MTS checkpoint,10 November2026. This finishes the saved combined pressure/kinetic memory calculation and derives an explicit next state map rather than merely listing missing coefficients.

## The actual source-budget calculation

Both the65-node live continuation and the original902-node signed extraction are evaluated for baseline and MTS, in all four frozen quadrature/history/metric representations. All16 variants pass the unchanged2e-5 numerical and1e-10 algebra checks. No native evolution, data download, fit, bank change, new action or physical grid change was required.

The cold CDM control carries its actual normalization and needs no heavy correction; its endpoint agreement is about6e-16 or better. For MTS:

| Fine order8 boundary/history transfer | Live continuation | Original extraction |
|---|---:|---:|
| Endpoint density relative discrepancy |3.7714e-11|1.9826e-10|
| Endpoint current relative discrepancy |1.9899e-11|7.4451e-9|
| Combined density correction |0.0006030627|0.0031991281|
| Combined current correction |0.0227952659|-0.0819771685|
| Density history left after boundary terms |-8.8272e-7|1.1230e-7|
| Current history left after boundary terms |1.9940e-5|-1.1983e-5|

Corrections use the original normalized source units. A large percentage of a small endpoint current is not an observational exclusion. The independent direct field-equation integrals also pass; their more cancellation-sensitive original-extraction current discrepancy is7.90e-7 fine and1.15e-5 with coarsened history. The boundary decomposition improves the numerical cancellation without changing the equations or tolerance.

The metric derivative comes from differentiated Hamiltonian/Friedmann constraints plus native eta', with numerical derivatives of retained source history. Degree5/7 and stride1/2 checks compare against direct metric interpolant derivatives; worst discrepancy across variants is2.21e-6. No exact native derivative port or independent future forecast is claimed by this postprocessing.

## What cannot be dropped

The no-remainder and pressure-only controls fail for MTS. For example, on the original extraction, pressure-only endpoint errors are6.09e-5 in density and8.34e-5 in current, beyond the same2e-5 gate. Including only the analytic boundary still leaves a current-history contribution which cannot be neglected at that tolerance. The baseline does not develop an invented discrepancy.

The derived conditional energy bounds enclose the calculated memory, but do not certify a zero-remainder approximation: source bounds are approximately(0.01014,0.16593) for the live window and(0.01394,0.22716) for the extraction. They use absolute signed-weight contributions and are deliberately conservative. These are numerically evaluated analytic conditional bounds, not uniform continuum or observational error bars.

## The constructive step

Rather than erase the endpoint phase, carry it in

    WD=YD+(3H*S+k*z*J)/2, WQ=YQ-k*S/2,
    J=beta*b*v, S=beta*(b*w+v*u).

Their exact equations retain the smaller remaining history/source terms. An explicit inverse to the original(u,w) is derived with metric self-feedback included. Under the stated flat positive-energy conditions, mu>9H/4 is sufficient for regularity at every phase, including v=0. This is an algebraic sufficient condition, not a claim about all possible MTS backgrounds.

On both saved heavy windows, the forward/inverse maps pass1e-10. Maximum energy-scaled condition is1.00058; minimum sampled sufficient margin is0.99913. The source coordinates reproduce the original field state to roughly1.4e-15 or better under the stated peak normalization. No coefficient was fitted. These are reversible coordinates of the retained parent, not a new field, new population, or an assertion that the old averaged law already uses them.

464 recorded comparison checks plus8 exact symbolic identities pass; the coordinate-map checks are separately retained. Checks are numerical/algebraic evidence, not independent observational predictions. Full results, every negative control, signed weights and packets are saved in analysis.json and the paired result files.

Next: implement and test this derived source state with LIVE gravity and present-state/background derivatives, keeping the exact remaining terms. Then assess a controlled reduction into the actual late averaged carrier and its background. Do not run another identical memory budget or reinterpret the passing known-history reconstruction as a new galaxy/cosmology fit.

Everything stays local; older work, Galaxy files and public repositories are unchanged. Exact worker cleanup accompanies the seal. Full goal remains active.
