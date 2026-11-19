# Derived history terms carry the sources across the averaging window

Private continuation, 10 November2026. This builds on the verified live phase-stress coupling without changing the retained theory, weights, data bank, backgrounds or tolerance gates.

## New result

The original temporal extraction has an exact source-transfer rule:

    S*endpoint = original_projection + integral(cumulative_weights * physical_source_rate).

Its memory terms are now derived from the retained scalar/dust equations and evaluated, not chosen to cancel an observed mismatch. They recover endpoint density, current and scalar pressure for baseline and MTS on the original902-node support. Pressure work, gravitational work and current transport remain explicit.

The wider capture uses original indices1991..2892. All original4253 observations are reproduced unchanged; its902-node source/metric subset matches the saved history exactly. The full native restart over that wider fixed-regime interval passes. No new native build or data download was needed. The new phase representation is evaluated against this native reference; this stage does not claim a new full902-node phase-only reintegration.

## Numerical checks

Original output nodes, action, mass, G, source normalization and weights stay fixed. Internal Gaussian orders4/8 and retained-history strides1/2 test quadrature and interpolation sensitivity. The numerical acceptance remains2e-5 and the algebra acceptance1e-10.

| Case/history/integration | Worst endpoint relative difference | Worst interval-increment relative difference |
|---|---:|---:|
| Baseline/full/order8 | 4.67418e-15 | 6.42697e-11 |
| Baseline/stride2/order8 | 4.67418e-15 | 6.42156e-11 |
| MTS/full/order8 | 7.84090e-7 | 3.78601e-7 |
| MTS/stride2/order8 | 1.14594e-5 | 7.41644e-7 |

All eight baseline/MTS quadrature-history combinations pass, as do the differences between resolutions. The coarsened MTS history has less margin; this is measured numerical sensitivity, not a certified continuum error bound. No tolerance was widened.

## Why the boundary memory matters

Replacing only a source at the right endpoint by its untransported temporal average would change the instantaneous metric while leaving the other fields fixed. The derived memory transports that source before comparison:

| Replacement diagnostic | Potential mismatch without memory | With source-equation memory |
|---|---:|---:|
| Baseline CDM | 4.18784e-3 | 3.80982e-16 |
| MTS heavy scalar | 1.71170e-3 | 3.59369e-11 |

These are dimensionless fractions of the existing endpoint potential, NOT observed cosmological fit errors. The baseline has the same temporal-handoff problem; this is not an MTS-only hurdle or an exclusion of an otherwise consistent coarse-grained model. A coarse-grained metric and an instantaneous native metric are distinct descriptions and cannot be mixed silently.

Removing only heavy-scalar pressure work from the transfer gives a0.3154% endpoint density error; removing gravitational work gives7.1872%; removing current transport gives4.5562%. Each fails the unchanged numerical gate. Corresponding slow-scalar ablations fail too, but the absolute slow-scalar contribution to this metric is tiny and is not advertised as an observable anomaly.

`transfer-analysis.json` contains the signed term ledger, endpoint values, refinement comparisons, metric consequences and ablations. `*-source-readout.npz` and the eight quadrature packets retain the numerical inputs. Seven symbolic checks establish the endpoint telescoping rule, scaled source equations and scalar self-gravity elimination.

## What follows from this, and what does not

This supplies a derived, source-complete finite-history transfer in a known-history test. It is not an independent holdout prediction or a fitted local pressure law. The boundary memory remembers actual evolution; it is not a new force or stress parameter.

DERIVATION.md also obtains the retarded scalar response operator including its own density contribution to gravity. That yields a concrete next calculation: evaluate the original projection's response matrix and test whether it can recover the coherent state and predict pressure with the supplied driving history. The rank and conditioning must be measured; two projected numbers should neither be assumed sufficient nor dismissed automatically.

The retarded fundamental matrix, its full coupled reduced evolution and the coherent-to-positive-ensemble population choice are not supplied by this finite-support test. They remain separate from galactic formation/occupation. Full project scope is retained and the goal stays active.

Everything remains local. No Galaxy files, public repository, shared services or other chats were changed. Worker identities, source hashes and cleanup accompany the checkpoint.
