> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# The pre-switch state predicts the spatial correction to U

**24 November 2026 · local saved-history test.** A forecast frozen at the 89.148503803 Mpc switch predicts the change in the Laplacian term to **0.2882%** peak-relative error and the sum of all three spatial terms to **0.2878%** through 89.6 Mpc. The spatial terms supplied the improvement previously seen only by inserting the resolved wave. Here the later wave was masked in all 38 native input packets; later background knots and the centered fluid projection table were withheld. The old flux prediction reproduced exactly, and was kept fixed across all three spatial tests. This is a forward prediction on a previously studied simulation, not a new observation.

| Primary: wave-minus-matched quantity | First stress cycle: value / rate error | Through 89.6: value / rate error |
|---|---:|---:|
| Common-slice potential difference across the input modes | 0.2574% / 0.6723% | 0.2574% / 0.6698% |
| Potential–Laplacian correction | 0.2882% / 0.7659% | 0.2882% / 0.7659% |
| Sum of all three spatial corrections | 0.2878% / 0.7628% | 0.2878% / 0.7628% |
| Full geometric source correction (including the locked flux) | 0.0433% / 0.1093% | 0.0416% / 0.1037% |

Errors are relative to each native *correction*, not the large native source. Without the new spatial terms the spatial value error is 100%. The shorter preparation gives 0.2282% spatial value error over the full window, the alternative algebraic prediction 0.4583%; neither replaces the designated primary result.

**The rate miss is localized.** On the unchanged derivative-of-saved-knots test, 0.7628% is over 0.5%. Its worst point is the first saved knot, 89.15 Mpc. Every subsequent knot is within 0.3920% on this spatial-sum metric, using the original peak normalization. An independent diagnostic using the native field equations, rather than differentiating the stored source, agrees with the forward spatial rate to better than 0.002% at the tested differentiation steps. Halving the model differentiation step changes the rate by 0.000570% of peak; integrating native equation rates back over two cells agrees with the saved source changes within 0.172%. At the first knot the native spline rate differs from the native equation rate by 0.894% of peak. This supports a boundary-sensitive numerical readout, not a wholesale error in the physical rate; the original gate is still recorded as failed.

## What reaches the photons?

| Full-window result | Coarse gravity | Fine gravity |
|---|---:|---:|
| Matched residual with frozen flux only, % of previous small correction | 0.64501% | 0.64501% |
| Matched residual with forecast flux and spatial terms, same units | **0.53932%** | **0.53932%** |
| Matched residual with full resolved U supplied, same units | 0.53942% | 0.53942% |
| Complete two-route photon gap, % of this run's own small correction | 0.82686% | 0.60662% |
| Supplied-U complete gap, % of its own small correction | 0.82696% | 0.60673% |
| Joint photon correction, % of original launch, momentum / differentiated route | 0.0036270% / 0.0036568% | 0.0036270% / 0.0036488% |

The distance between the forecast and supplied-U **complex route-gap vectors** is 0.130% of the distance the flux-only result originally had to cover, on both steps. This measures reproduction of a specific controlled change, not a 99.87% agreement with the sky. Both metric launches pass their own 0.5% criterion (fine: 0.39076%, 0.29375%). Both photon routes remain well inside 0.163% of launch. Time, angular and gravity controls on the momentum readout pass; the independent route precision still misses 0.5%. The fixed cold baseline and the earlier companion stress were reused; no later interval or authoritative new restart.

**Next:** leave this forecast for U fixed. Use the saved branches to isolate the other two geometric inputs: the source for the difference between the metric potentials (Q) and the source in the momentum-rate equation (Fq), separately and together. Test their signed effects on both photon components before deciding whether either is worth deriving from entry; if neither moves the remaining discrepancy, go to the coupled matter/companion balance rather than tuning U.

[Equations and assumptions](DERIVATION.md) · [frozen protocol](PROTOCOL.md) · [numeric freeze](evidence-001.zip) (archive member: `frozen.json`) · [source scores](evidence-001.zip) (archive member: `source-scores.csv`) · [modal errors](evidence-001.zip) (archive member: `modal-error-budget.csv`) · [direct rate check](evidence-001.zip) (archive member: `rate-diagnostic.csv`) · [donor and reference comparison](evidence-001.zip) (archive member: `donor-comparison.csv`) · [photon readouts](evidence-001.zip) (archive member: `photon-scores.csv`) · [precision controls](evidence-001.zip) (archive member: `photon-controls.csv`).
