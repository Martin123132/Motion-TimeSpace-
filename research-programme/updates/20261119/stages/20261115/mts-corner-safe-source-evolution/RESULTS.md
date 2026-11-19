# Corner-safe source evolution — 2026-11-15

Authoritative outputs: `result.json`, `cold-result.json`, `heavy-result.json`, and the corresponding `*-comparison.npz` files. Runs: `cold/heavy-source-history-32.npz` and `cold/heavy-source-history-64.npz` (separate files with those prefixes). All requested paired checks pass.

## Completed advance

Propagated the frozen, tested source variation through the retained coupled own-field/metric equations. Reused the successful quadratic runs as the control; no native replay/rebuild, scattering-bank change, physical-grid change, new observation or fit. Original902 signed preparation nodes, nine report epochs, parameters, normalization and tolerances stay fixed.

Twenty-one preparation/algebra checks pass. Full and independent difference evolutions were each run at32/64 subdivisions for both cases. Both pass all eight later reports, all native boundary-state/metric checks, both external source-channel checks, difference refinement and full/difference superposition.

## Comparison with saved references

Maximum relative residual including the existing numerical working allowance:

| Case | Density | Current | Pressure | Unchanged gate |
|---|---:|---:|---:|---:|
| Baseline | 1.01786750e-9 | identically zero | identically zero | 2e-5 |
| MTS | 1.02648454e-9 | 9.32197964e-10 | 1.19075113e-6 | 2e-5 |

MTS raw pressure residual is5.75079490e-8. The previous quadratic value was5.462021998e-8: the more complete source does not improve every residual, and it is not selected to do so. Both remain within the same tolerance. Most of the pressure working allowance still comes from the saved target uncertainty, not this source variation or current time-step error.

The boundary metric-force relative errors are2.22634e-15 baseline and2.62328e-15 MTS. These are consistency checks against the retained numerical history, not precision claims about nature. The earlier baseline external-density mismatch is also resolved by the source integral, with the same result as the previous source-only check.

## Actual changes versus the precomputed allowance

Changes are in the retained normalized source-output units:

| Output | Independently evolved final change | Earlier absolute envelope | Fraction of envelope used |
|---|---:|---:|---:|
| Baseline density | -1.2083599331e-12 | 6.6221003670e-12 | 18.25% |
| MTS density | -7.3154999693e-13 | 3.6794896818e-12 | 19.88% |
| MTS current | -7.1819725835e-15 | 4.4861807512e-14 | 16.01% |
| MTS pressure | -7.3292709685e-13 | 3.7005856490e-12 | 19.81% |

The actual MTS pressure change consumes about0.01535% of the previously remaining pressure margin; the conservative source-variation estimate allowed0.07750%. The difference-equation32/64 pressure refinement is3.48e-9 relative to this small correction, versus the unchanged2e-5 gate.

MTS full-state subtraction agrees with its separately evolved corrections; the largest weighted pressure discrepancy between those routes is8.72e-18, within the tracked allowance. Baseline density's correction is smaller than the conservative subtraction uncertainty, so the independently evolved difference equation is the resolved diagnostic there. Baseline current and pressure remain zero.

## Boundaries of this result

The tested source history is conditional on the retained native surrounding solution. No newly measured universe-facing improvement is claimed. The finite source checks and numerical gain calculation are not an interval-certified continuum theorem. There is now a direct propagation test of the previously estimated source-variation effect, rather than only an estimated budget.

Private local stage only. Previous325 artifacts and frozen inputs are checked unchanged; no GitHub, browser/coordinator message, subagent or unrelated process action. See `validation.json`, `closeout.json` and `CLEANUP-VERIFIED.json` for the saved audit and exact worker exits. The persistent goal remains paused for manual continuation.
