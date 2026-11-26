> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# The continuity equation predicts the heavy-density mismatch from the switch

**On the retained 89.148503803–89.6 conformal-Mpc window, the later matched heavy densities were not needed to predict their difference from the wave's trailing-cycle average.** Starting once at the switch and advancing with the momentum equation gives complex RMS errors of **0.000517% (coarse) and 0.000699% (fine)** relative to that difference, not relative to the much larger density. Holding the entry mismatch fixed misses by about 100%; holding the physical density fixed misses by more than 400%. The result comes from evolution, not a constant offset.

| Primary test | Coarse gravity | Fine gravity |
|---|---:|---:|
| Density mismatch: RMS prediction error | 0.000517% | 0.000699% |
| Density mismatch: maximum absolute error / peak actual mismatch | 0.000710% | 0.001107% |
| Density-only forecast: joint photon gap, % of original small momentum-route correction | 0.577971% | 0.577981% |
| Saved joint photon gap, same scale | 0.577973% | 0.577985% |
| Signed joint photon error relative to **the saved gap itself** | 0.000513% | 0.000737% |
| Signed photon error with predicted density **and** current, same denominator | 0.000265% | 0.000442% |

**What the prediction uses.** Let A be the trailing phase average of the native energy perturbation, e the matched perturbation, Φ the metric potential and j the matched current. Define g = e−3Φ−A. In the conventions of the retained branch:

    g′ = −j − 3H p + S_e − A′
    j′ = −Hj + k²(p+Ψ) + S_j
    p  = c_s²(g+A+3Φ+3Hj/k²) + p_res
    predicted mismatch = A−e = −g−3Φ.

A′ is the phase speed times the difference between the entering and leaving native samples, divided by π. Before the first full cycle the leaving sample is held at the switch. Integrating this endpoint formula also recovers the numerical average's excursion to better than 6×10⁻¹² relative. The source and pressure closure are the retained **native-wave-derived** companion inputs, not parameters inferred here.

We propagated the unaveraged pre-switch solution from 89 Mpc, matched its normal energy and current, and solved the constraint at the switch for the entry potential. The primary calculation then propagated Φ from momentum. The independent numerical route through the same model recomputed Φ from the energy constraint with the frozen supplied U. On the fine grid the latter's RMS mismatch error is 0.000297%; its density-only photon forecast misses the signed saved gap by 0.000373%. There was no restart of the density, current, ordinary lower moments or potential between switch and endpoint. The saved quadrupoles and prescribed stress/forcing are inputs. The matched history reader exposed only I2 and N2 before the density freeze; no later matched heavy fields, metric or lower ordinary fields were supplied to either density evolution.

**Resolution and controls.** The coarse-to-fine RMS change of the predicted mismatch is 0.132% and the peak change 0.229%; corresponding figures for the saved mismatch are 0.133% and 0.230%. These are below 0.5%, but larger than the within-grid prediction errors. The small within-grid errors are not continuum error bars. All source-subdivision, photon-time, angle, gravity-step and filtered-control photon comparisons pass. The unchanged filtered-only control still misses the signed fine-step photon gap by 95.415%.

**What the gap means.** The later photon test used exactly the preceding stage's per-cell metric and ordinary left states; they were released only after freezing the density. The density-only test leaves the earlier filtered current untouched. The predicted fine-step photon energy and current gaps are **0.578203% and 0.577210%** of the original small correction. Both agree closely with their saved counterparts and both remain above the physical 0.5% threshold. The separate 0.163%-of-original-launch size check passes. This identifies the density preparation error in this saved-history experiment; it does not make the physical gap disappear.

**Next:** carry the ordinary fields and metric continuously from the switch into the photon work calculation too. Freeze that single-launch result before comparing it with the existing per-cell result and the archived photon reference. That tests how much of the residual belongs to continuous constraint evolution rather than the repeated choice of saved left states. No change of averaging rule, bank, amplitude, fit or tolerance; no new interval or promoted restart.

[Protocol](PROTOCOL.md) · density freeze (not bundled here) · source freeze (not bundled here) · photon freeze (not bundled here) · [density scores](evidence-001.zip) (archive member: `density-scores.csv`) · [null and cross-grid checks](evidence-001.zip) (archive member: `density-controls.csv`) · [signed photon comparison](evidence-001.zip) (archive member: `photon-scores.csv`) · [physical gates](evidence-001.zip) (archive member: `physical-gates.csv`) · [numerical checks](evidence-001.zip) (archive member: `photon-controls.csv`).
