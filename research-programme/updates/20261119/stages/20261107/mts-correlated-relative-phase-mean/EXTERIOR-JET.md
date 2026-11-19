# Exterior enthalpy jet from the retained thermal source

The accepted half-family refinement follows two preserved failures.
`drift-half-01` fails the derivative-width gate before the exact scalar-row
repair. `stable-half-01` removes the cancellation noise but the Poisson
width comparison remains2.0603152414e-5, just above2e-5. This is still
a failure; the gate is not rounded or relaxed.

`refined-half-01` adds ONLY the four new +/-0.0005 directional phase
families and reuses the larger offsets. Its Poisson drift comparison is
1.4433940525e-6, a reduction by14.27; GR is7.6750670797e-10. The
absolute Poisson remainder change is2.0621487380e-10. Phase refinement
and all other required checks pass. These are coefficient diagnostics,
not a new history grid or physical parameter adjustment.

## Deriving a smoother physical background jet for the next cold step

Let R_ext be the parent's conformally rescaled density excluding both
explicit scalar fields. Its conservation equation implies

    W_ext = (2 R_ext - R_ext,N)/3,
    W_ext,N = (2 R_ext,N - R_ext,NN)/3.

No equation of state is fitted here. The retained
`../mts-cold-background-extension-20261107/thermal_candidate.py` already
evaluates R_ext and both derivatives from its fixed matter/radiation
normalizations and Fermi-Dirac integral. For a massive momentum element
with speed squared v^2, its density integrand obeys

    R_N = -(1+v^2) R,
    R_NN = (1+4v^2-v^4) R,
    W_N = -(1+2v^2-v^4/3) R.

Cold matter gives W_N=-R; massless radiation gives W_N=-8R/3. These
identities provide the required exterior jet without subtracting a
rapid scalar derivative from a fitted total-gravity spline.

`half/external-jet-01` checks this source against the native baseline and
MTS at11 frozen offsets. Parent thermal orders48 and64 agree to at most
2.20e-16 in the three density quantities. Integral versus native values:

| Comparison | MTS | Baseline |
|---|---:|---:|
| Exterior density |3.14e-11|2.38e-11|
| Exterior enthalpy |1.68e-11|1.33e-11|
| Inherited enthalpy derivative |1.31e-8|5.86e-11|

Independently differencing the smooth native exterior enthalpy at four
widths agrees with the integral derivative within4.37e-11 for MTS and
3.79e-11 for baseline. The larger inherited MTS derivative discrepancy
is consistent with subtracting the fast scalar derivative from the
total-gravity interpolant. This is a numerical diagnosis, not a new
thermal anomaly or proof of the cause of every derivative discrepancy.

The source is **not switched in this stage's accepted phase packets**.
They retain the original operator, including its finite-quadrature
enthalpy defect, and pass after controlled refinement. For the next cold
coefficient construction, use this derived jet with an explicit native
comparison and replacement-error budget; do not silently set the defect
or its derivative to zero. Configuration ownership is recorded in
`half/external-jet-01/freeze.json` and `result.json`.
