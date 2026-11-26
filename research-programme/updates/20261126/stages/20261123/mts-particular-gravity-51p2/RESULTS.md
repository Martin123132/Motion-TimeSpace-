> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# 44.8–51.2 conformal Mpc: cancellation continues, especially at the peak

23 November 2026 · Private · Longest frozen wave (4,2,1), k = 0.3368801156243423 per comoving Mpc. The new matter-sourced gravitational interval is **not weaker in isolation** than the previous one across the visibility window (1.3769% versus 1.3456% of launch). Nevertheless, its phase reduces the accumulated difference between the MTS and cold-baseline photon histories.

| Joint MTS-minus-cold photon energy and current | Window RMS | Common visibility peak |
|---|---:|---:|
| Previous signed sum, source through 44.8 | 3.8467% | 1.8714% |
| New interval alone | 1.3769% | 0.8591% |
| New signed sum, source through 51.2 | **3.4519%** | **1.2727%** |
| Change in the signed sum (percentage points) | **−0.3948** | **−0.5987** |

All percentages in the table use the fixed launch-difference norm 1.8923589891767267e-12. The comparison is at matched scale factors with the saved cold visibility and conformal-time weighting at 750 ≤ z ≤ 1500. Source coverage ends at early conformal time 51.2; photons are still propagated through the same last-scattering readout. These are single-mode field predictions, not percentages of the observed microwave background.

## What cancels

The new interval's signed alignment with the whole earlier photon signal is −0.451 across the window and −0.815 at the peak; the stronger opposition at peak explains the larger drop there. Its window energy and current components are 1.2151% and 0.6475% of launch and combine in quadrature.

Independently of the earlier launched photons and regular drive, the four particular-source intervals from 25.6 to 51.2 have individual window magnitudes summing to 5.1908% of launch. Their actual coherent sum is 1.9580%: **37.72% of that sum of magnitudes**. At peak the corresponding figures are 2.6327%, 0.6644% and **25.23%**. This is an amplitude comparison, not an energy-loss fraction. It was checked both from all pairwise products and by subtracting the pre-interval history from the accumulated history. Subtracting freely propagated photons instead, which retains the regular drive too, gives a net driven contrast of 1.9216% RMS (1.1030% at peak).

## How well it is resolved

- Continued both sealed -p4 states, common sources and 154 finite-momentum endpoints on the original bank. All joins were consistent (worst incident-source relative mismatch below 2.3e-16). The 17 overlapping native time samples are reused values, not independent checks. The direct incident solver and angular projection checks agreed within 5e-16 on the three test bins per model.
- Before scoring photons, doubled the inner time step at fixed converged stress. The signed potential, lapse and curvature-derivative histories shifted by at most 0.2370%, 0.2278% and 0.0485% of their corresponding peaks. The independently differentiated potential agreed with the signed constraint derivative to 0.1116%. All are below the unchanged 0.5% threshold. The potential check is larger than the previous interval's 0.1202%; carry that check forward.
- All 27 propagation comparisons and six further fixed-stress propagation comparisons passed at window and peak. Assembling all four blocks with the same variant throughout, all five settings gave decreases of 0.3948–0.3957 percentage points across the window and 0.5987–0.5995 points at peak (rounded). For the cumulative signed history the largest tested shift was 0.0714% RMS and 0.0940% at peak. The new force was zero before its interval, and earlier blocks were included exactly once. These are numerical controls at the retained bank and grids, not observational uncertainties.

[Per-model results](evidence-001.zip) (archive member: `results-p4.csv`) · [source-window alignment](evidence-001.zip) (archive member: `interference-p4.csv`) · [four-interval coherence](evidence-001.zip) (archive member: `four-interval-coherence.csv`) · [net driven vs freely transported](evidence-001.zip) (archive member: `net-drive-versus-free.csv`) · [paired signs](evidence-001.zip) (archive member: `direction-under-paired-controls.csv`) · [cumulative sensitivity](evidence-001.zip) (archive member: `all-four-blocks-control.csv`) · [pre-transport check](evidence-001.zip) (archive member: `pre-transport-gate.json`) · [propagation checks](evidence-001.zip) (archive member: `controls-p4.csv`) · [propagated time step](evidence-001.zip) (archive member: `frozen-stress-step-propagated.csv`) · [protocol](PROTOCOL.md).

**Next:** continue 51.2–57.6 from particular-cold-p4.npz and particular-heavy-p4.npz and both sets of common and finite-momentum endpoints. Test the signed time step before reading the photons. The isolated interval has not become small, so do not treat cancellation as a bound on future forcing. Use verify51.py with bytecode disabled to verify the sealed local files.
