# Predictive memory now evolves with current rest-species feedback

10 November 2026. Previous goal turn: verified progress on conditional predictive memory. This turn implements the retained current-state coupling and executes the short live test. It is no longer driven by a saved future rest-perturbation history.

## Completed calculation

Eight integrations completed: actual cold/CDM and heavy/MTS, three reconstructed-initial step/metric configurations plus a captured-initial fine control for each. All use the original65 output epochs2892..2956, k=1, physical bank, source coupling, parameters and 2e-5/1e-10 gates. DOP853 tolerances remain1e-10/initial-scaled1e-12. The parent homogeneous background tables remain unchanged.

The MTS carrier has187 coordinates (rest plus two heavy carrier coordinates), replacing the189-coordinate redundant native phase representation without removing physical perturbations; the original active native state has185 entries. Both Z0 and the zero-initial full correction Delta evolve. Their sum alone is the candidate. Its exact native comparator supplies no source values to the forward calculation.

## Accepted fine results

The following are maximum componentwise history-peak-normalized errors against the retained native solution, not observational errors or precision claims about cosmology:

| Comparison | Actual CDM | MTS live memory |
|---|---:|---:|
| Native state | 1.47462e-14 | 2.13405e-11 |
| Source/observer readouts | 1.21063e-13 | 1.18075e-10 |
| Actual physical evolution derivative | 3.42761e-12 | 6.54478e-9 |
| Coordinate equation residual | 0 | 2.10683e-9 |
| Active native cache differences | 0 | 0 |

All pass the unchanged numerical gate. Reducing the integration step lowers the MTS actual-derivative error from1.66063e-8 to6.54068e-9; refining the physical metric derivative gives6.54478e-9. The independently captured-initial fine control also passes. The actual cold correction remains exactly zero throughout, as required by its unchanged exact dust/slow-field operator.

The MTS correction to the rest coordinates is nonzero, with maximum absolute magnitude4.29126e-10 in the retained mixed-coordinate convention. This is evidence that the implementation actually evolves the coupled correction, not a dimensionless observational effect or a fitted population. The fine heavy density/pressure/current source errors change from2.69216e-6/3.72940e-7/3.20869e-7 in the uncorrected control to1.18075e-10/1.75705e-11/1.17138e-11 with predictive memory.

## Numerical checks and retained failures

The native initialization preserves the original full-history output parity and releases its owner. Current-state roundtrip, zero/superposition, bidirectional source response and comparator-mutation checks pass. The corrected heavy preflight contains211 checks. Final validation recomputes10,190 component comparisons across the saved runs, source/actual-derivative readouts, retained-coordinate derivative decoding and refinements. These are checks on eight integrations, not10,190 independent physical experiments.

Two original heavy preflights remain failed and are preserved:

1. The first adapter omitted a background-field factor in one map derivative. The independent chain check caught it before any heavy evolution. An exact product-rule correction restores the previously derived formula.
2. With that correction, a small-step subtraction-based independent checker gave2.09699e-5 against the fixed2e-5 gate. The separate eight-step paired diagnostic identifies a usable band at divisors768 and1024, with heavy density errors4.65921e-6 and5.47696e-6. Both are retested with the original physical metric steps. All scan outcomes, failed receipts and the diagnostic-informed selection are explicit; no tolerance was relaxed.

Read MAPPING-DERIVATIVE-REPAIR.md and CHAIN-PRECISION-DIAGNOSIS.md. The physical metric-step comparison remains7.07430e-9 for H' and1.63410e-8 for the rest-source derivative. Physical integrator settings, bank, grid, initial data and theory coefficients are unchanged. Reuse checked_live_memory_model.py, whose corrected class is verified identical to the accepted one; the frozen erroneous base file remains only with this explicit warning and its failure evidence.

## Meaning and next physical test

This establishes a working current-state implementation of the derived memory/source coupling on the retained short live branch. The candidate evolves using present rest species, not a prescribed future rest forcing, and its actual evolution derivatives are tested rather than merely evaluating native equations at a nearby state. It does not introduce a new background-averaging prescription or change the old late selector.

The earlier902-node signed-pressure success remains conditional until this live construction is tested on that original window. The saved next-window inspection confirms both branches have902 matching source/capture nodes, contiguous original native indices1991..2892, and one capture signature. Those inputs are ready for the next bounded live test; they have not been rerun here.

All changes remain private in this new stage and the resume bookmark. No Galaxy files, GitHub, browser, relay, shared service or unrelated process was changed. Exact exits and the two documented failed preflights are recorded in CLEANUP-VERIFIED.json; no continuing task-owned job is authorized.
