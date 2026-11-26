> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# The photon discrepancy is in the saved potential increments

24 November 2026 | 89.148503803–89.6 conformal Mpc | photon launch | saved 77-bin solutions. We compared the observed endpoint change of the potential, Φ(right)−Φ(left), with the time integral of the independently saved momentum-constraint rate P. For the wave we used its native clock, including its pre-switch samples for interpolation at entry. The matched control retains forecast U, original Q/Fq and the one-cycle current; the restored-current comparison retains its original pressure, density and source terms. No fit, new evolution or change of gates.

## What the actual steps say

There are 1,156 coarse and 2,312 fine intervals per history, including the short first one. Below, local error is the magnitude of the complex increment difference divided by the magnitude of that cell's own predicted increment. **No cell in any of the three histories exceeds 0.5%.** This is not the photon criterion: photon energy and current measure a much smaller signed difference of two histories, with a different denominator.

| Branch | Worst local increment error, coarse / fine | Photon-weighted branch discrepancy, coarse / fine |
|---|---:|---:|
| Matched, one-cycle current | 0.40410% / 0.40451% | 0.538994% / 0.538996% |
| Matched, resolved current | 0.44457% / 0.44562% | 0.538986% / 0.538995% |
| Explicit reference wave | 0.28480% / 0.26962% | 0.297453% / 0.084913% |
| Matched mean **minus** wave | — | **0.826864% / 0.606615%** |
| Matched restored **minus** wave | — | **0.826856% / 0.606614%** |

Right column: joint photon norm on the original small momentum-route correction at the corresponding gravity step. The signed complex branch histories are subtracted **before** taking this norm; magnitudes do not subtract as scalars. The fine mean-current run's energy and current gaps are 0.606848% and 0.605804% on their own component scales. None of the full runs pass the original 0.5% component agreement test; the restored run in particular has a nearly vanishing own normalization. The separate 0.163%-of-launch size limit still passes. The previous coarse restored-wave energy-rate failure remains recorded and is not overridden here. [Per-step summaries](evidence-001.zip) (archive member: `endpoint-statistics.csv`) · [all gates and denominators](evidence-001.zip) (archive member: `gates.csv`) · [separate photon components](evidence-001.zip) (archive member: `branch-projection.csv`).

## Why testing endpoints changes the diagnosis

For each cell of width h, define m=[ΔΦ−∫P]/h. We transported (i) that mean, (ii) the remaining Φ′−P−m, which integrates to zero on the cell but can drive the photons if their weighting varies, and (iii) the difference from the archived derivative readout. We integrated on the union of native and photon knots; no endpoints were discarded. In each photon step we project the source onto the two retained Radau stages by integrating each linear nodal weight times the source, divided by its quadrature weight. This preserves constant and linear source moments and the existing linear photon response without replacing a varying kernel by a midpoint. Four- and six-point integrals agree. Separately replaying the original stage sampling recovers the archived energy and current, including the reference sign, at all three transport settings.

For the mean-current run the within-cell part has joint norm **1.81×10⁻⁸ / 6.27×10⁻⁹ of the saved gap** (coarse / fine). The change from interpolating the derivative samples and the difference from the original stage sampling are also negligible on that scale. The means alone reproduce 0.826864% / 0.606615%. Thus replacing the derivative readout does not fix the discrepancy: it already exists between actual saved endpoints and the integral of the saved rate. This identifies an inconsistency of the saved histories at the precision needed for this small photon signal; it does not establish which evolution equation is responsible. [Signed contributions](evidence-001.zip) (archive member: `signed-terms.csv`) · [independent archive replay](evidence-001.zip) (archive member: `replay.csv`) · [step controls](evidence-001.zip) (archive member: `controls.csv`).

## Where the gravity-step sensitivity enters

Every pair of fine cells has exactly the same outer endpoints as its coarse cell. For coarse minus fine we separated the change in ΔΦ from the negative change in ∫P. We propagated these differences with the original photon operator, keeping the within-cell weight. On the explicit reference wave, **86.38% of the signed change along the joint difference vector comes from the potential history, 13.62% from the momentum prediction**. The split is unchanged to displayed precision on the photon time and angular controls. These are projections of the coarse-to-fine change, not fractions of the full residual. On the matched mean-current history the two changes strongly cancel; its net photon residual vector changes by only 0.00081% of its fine value. The full gap vector changes by 43.28%. Two steps do not establish a continuum limit. [Paired-cell closures](evidence-001.zip) (archive member: `paired-stats.csv`) · [gravity-step attribution](evidence-001.zip) (archive member: `gravity-attribution.csv`).

**Next test:** use the stable matched history first. Write its saved energy constraint as DΦ=N. On each cell the exact identity ΔN=mean(D)ΔΦ+mean(Φ)ΔD holds with arithmetic endpoint means. Independently build ΔN from the retained energy- and current-balance equations, including external work and the frozen geometric source. Compare this with mean(D)∫P+mean(Φ)ΔD and project the signed difference to the photons. This tests which balance contributes to the stable 0.539%, rather than trying another photon derivative or treating the reference's coarse-to-fine change as the explanation for it.

[Fixed protocol](PROTOCOL.md) · [cell calculation](evidence-001.zip) (archive member: `cell89.py`) · [photon moments and propagation](evidence-001.zip) (archive member: `photons89.py`) · [comparison](evidence-001.zip) (archive member: `score_cell_balance89.py`) · [paired-gravity calculation](evidence-001.zip) (archive member: `step89.py`).
