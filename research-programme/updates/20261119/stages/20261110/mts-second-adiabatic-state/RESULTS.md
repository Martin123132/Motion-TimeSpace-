# Second-adiabatic state/source map: verified results

2026-11-10. Continues the retained averaged-action work. No live native
closure, original cosmology, galaxy model or data bank was replaced.

## What is now derived

From the original canonical scalar oscillator, not from a pressure fit:

    W2 = omega - H^2(3mu^4+12mu^2 k^2+4k^4)/(8omega^5)

for the preserved constant-conformal-H probe. The general expression with
H' is recorded in DERIVATION.md. The second-order frequency, field/source
map, nonzero background pressure and canonical symplectic weight are carried
together. An arbitrary compensating source is not added.

The exact source-coordinate identities now connect any conservation
remainder directly to the underlying oscillator residual. This follows
the scalar field's stress-divergence identity, not an assumption that
a numerically stable reduced equation automatically conserves its sources.

## A bound against the original field equation

The real template has unit Wronskian. Variation of constants gives a
coefficient-generator norm |R_W|/W and an error bound exp(B)-1, where
B=integral |R_W|/W d tau. This includes mixing of the two quadratures.

An exact-rational enclosure covers the entire frozen probe rectangle,
including the homogeneous carrier and all399saved heavy modes, not merely
a sampled maximum. Both model parameter boxes were verified from the saved
rows. The conservative coefficient-norm bounds are:

| Template | Rationally enclosed propagation error |
|---|---:|
| Old W=omega | <=9.565e-10, safely rounded upward to1e-9 |
| Derived W2 | <=1.256e-21, safely rounded upward to2e-21 |

This applies to the specified unforced constant-H oscillator over
Delta ln a=.001, with the SAME exact initial q and q'. It is not a claimed
precision of the full cosmology, an observational uncertainty, or the accuracy
of ordinary floating-point output.

Independent80-digit Bessel solutions test the original constant-H equation.
At the three preselected probes k=0,1e-5,.000982171889188 inverseMpc:

- Old-template coefficient-norm errors are approximately3.259e-10.
- W2 errors are approximately3.225e-22, within the analytic enclosure.
- W2 quadrature-mixing errors are approximately2.709e-25.
- Exact-reference Wronskian checks are at or below2.11e-81.

The three controls do not establish coverage of the whole rectangle by
themselves; the polynomial/rational proof provides that coverage.

## Source conservation is tied to the same remainder

Three exact off-shell identities connect the background, density-energy
and phase/current conservation remainders to R0 and Rk. They retain the
nonzero second-order background pressure and the distinction between
momentum/rho and the physical velocity potential.

The rational enclosure gives instantaneous e-fold source-remainder bounds

    energy continuity: <=5.093e-18 N,
    phase/current:     <=2.545e-18 N,

where N=max(|R|,|I|,|delta|,|S|) in the explicitly defined carrier/source
coordinates. These are not terminal relative-error bounds for a tiny
individual stress component. Read SOURCE-CONSERVATION.md for the exact
identities, assumptions and conditioning.

## Matched transport using the saved state packet

All399heavy and399cold initial rows at a=.01 were reused. No new primordial
realization, mass adjustment or local occupation was selected.

| Saved comparison | Maximum normalized state difference |
|---|---:|
| Independent old-template replay | 1.059e-15 |
| Full old template versus derived W2 map | 2.360e-14 |
| Retained original closure versus W2 map | 3.644e-10 |
| Previous first-order completion versus W2 map | 5.677e-9 |
| Cold analytic continuation versus saved control | 4.059e-16 |

These fix initial physical delta and S. Different reduction orders can map
them to different microscopic initial data; those comparisons therefore
are interface/branch differences, not automatically errors for one fixed
microscopic initial state. The separate Bessel/operator controls use the
same exact equation and canonical initial-data rule.

The full old template already retained important higher-order kinematic
terms. The derived W2 transport is close to it, whereas the earlier
first-order-only completion is still farther away. Do not claim that adding
only g improved the saved model, or that W2 yields a new galaxy-fit gain.

All8/16/32point beat-phase integrations produce final double-precision states
that agree to their stored precision. That equality is not a21-digit
numerical certificate. Independent80-digit evaluations of the source/frame
formulas show relative rounding discrepancies below6.15e-16 for the tested
coefficients. Stable factorization avoids subtracting nearly equal carriers.

## Scientific scope

The frequency and canonical-state truncation are now controlled against the
original oscillator on a specified domain. Its source identity is also
derived. This is concrete progress toward a correctly normalized parent
formation state; it is not a completed halo formation calculation.

The next step is action-derived Phi/Psi forcing with these same normalizations,
and then the explicit variable-H terms before using the certificate on an
actual evolving cosmological history. Spatial geometry, nonlinear realization
and environment are still required before the galaxy solver can predict
local occupation. The existing global amplitude does not choose that state.

Standard WKB mathematics is credited in DERIVATION.md. No interacting-QFT
existence or mass-gap theorem is imported into this classical reduction.
No new observation was scored, and no original result was overwritten.

## Evidence owners

- proof.json: exact polynomial and rational solution-error enclosure.
- exact-controls.json: independent original-equation Bessel controls.
- conservation.json: source identities and rational residual enclosure.
- transport-result.json and transport.npz: all paired saved-state comparisons.
- validation.json: independent high-precision residual and implementation checks.
- closeout.json: source/output manifest and worker cleanup.

The original1e-10 algebra and2e-5 numerical gates remain unchanged.
