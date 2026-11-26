> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# Fixed stress: the averaged gravity agrees; the directly evolved heavy current does not

Over 89.1485038031–89.6 conformal Mpc we prescribed exactly the same physical change in the saved 77-bin stress to the averaged and phase-resolved branches. The averaged lapse and wave-momentum forecasts were sealed before evaluating the native responses. On the primary input, removing the common imposed shear leaves **0.00783% relative error in the gravity the system generates**. The unchanged acceptance limit was 0.5%. This is an internal perturbation comparison, not a fit to data or a new photon readout.

| Full window; fine gravity, four subdivisions; time-weighted complex RMS error relative to native change | Frozen fine stress | Independent replay using frozen coarse stress* |
|---|---:|---:|
| Curvature potential Φ | 0.007816% | 0.009632% |
| Lapse Ψ including common shear | 0.000006774% | 0.000006226% |
| Induced lapse with common shear removed | **0.007827%** | **0.009647%** |
| Heavy momentum from projecting the averaged geometry through the switch-launched wave | 0.00002520% | 0.00002524% |
| Same wave projection from induced geometry alone | **0.009906%** | **0.012790%** |
| Heavy current evolved directly as an averaged fluid variable | **49.930%** | **49.444%** |
| Heavy current contribution integrated in the curvature equation | 11.450% | 12.184% |

*The two stress histories are controls, not independent observational samples or uncertainty limits. Treating the two different stresses as if they were the same produced the previous 186% comparison. Giving both models either one tests their responses, not which absolute stress is correct.

**Why the distinction matters.** The primary native induced lapse RMS is 7.7771 × 10⁻³², only about 0.087% of the full lapse change (8.9851 × 10⁻²⁹, retained units). A total-lapse pass alone would therefore be weak evidence. We tested this smaller part on its own, as well as the corresponding induced wave momentum. Both pass on the first cycle, on the remaining window and on the whole window on all four numerical grids for both inputs. The largest errors over those comparisons are 0.00965% and 0.01280% respectively. The phase-blind fluid current does not pass: its error is over 136% in the first cycle for both sources. Omitting the kinetic tangent in a separate control gives 50.09% full-window fluid-current error for fine stress: that tangent is not the missing current closure. Near-agreement of the two metric forecasts does not identify the tangent uniquely.

**What the curvature budget says.** We accumulated Φ′ = (J_heavy + J_other + J_fixed)/(2k²) − H Ψ along each evolution. On the fine input, the heavy integral projects to 100.28% of the small curvature error, the lapse integral to −0.28%, the fixed current to zero. These are signed projections, not fractions of physical energy. The heavy integral itself is small on this window, so a large *relative current* error can coexist with good curvature. The curvature, rather than the responsive shears, accounts for nearly all of the lapse mismatch.

**One-way diagnostic, after scoring, not a second blind test.** Hold the averaged other currents and shear fixed, and replace only its heavy current with that obtained from the already frozen phase-resolved wave probe on averaged gravity. The predicted curvature change relative to the original averaged solution satisfies ΔΦ′ + H_avg ΔΦ = (J_probe − J_fluid)/(2k²), starting from zero. The integrating-factor solution reduces the fine-source curvature error from 0.007816% to 0.0009231% (88.19% reduction in its RMS); the coarse-source error falls from 0.009632% to 0.0012294% (87.24%). A trapezoidal cross-check differs by at most 0.00148% of the correction across all runs. **This is not a recoupled solution:** the probe does not see its own corrected metric, and the density/energy equation is not replaced by this diagnostic.

**Checks.** All 126 fixed-input clock comparisons pass (largest difference below 3.4 × 10⁻⁹%); all 12 comparisons to the archived native currents or geometry pass. The cold acceleration and integrated curvature checks pass, both shear components sum correctly, and all zero-stress controls give exactly zero. The matched forecast uses the oscillator launched at the switch, not the subsequent native wave background. The two physical input histories and all primary forecast choices were frozen. No gravity or frequency grid, threshold, stress bank, production history or paper was changed.

**Next:** close the loop at the same switch and on these same inputs: replace the averaged heavy current, do not add a second copy, propagate the phase-resolved current on the resulting metric, and check its associated heavy density/energy balance independently. Compare with the one-way result and native wave on both gravity steps before extending the window.

[Protocol](PROTOCOL.md) · Frozen forecasts (not bundled here) · [Native controls](evidence-001.zip) (archive member: `native-replay.csv`) · [All windows and branches](evidence-001.zip) (archive member: `frozen-comparisons.csv`) · [Fixed-input refinement](evidence-001.zip) (archive member: `clock-tests.csv`) · [Curvature and momentum attribution](evidence-001.zip) (archive member: `signed-error-shares.csv`) · [One-way diagnostic](evidence-001.zip) (archive member: `one-way-current-budget.csv`).

Reproduction with the same sealed parents in a fresh sibling directory: lapse_stage.py, identical_input.py, respond.py averaged, project_wave.py averaged, respond.py native, project_wave.py native, judge.py, current_budget.py, verify_lapse.py. Use Python with -B and one numerical thread.
