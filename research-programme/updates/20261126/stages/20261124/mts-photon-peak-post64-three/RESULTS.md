> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# The matter reversal reaches the photons, but not as a uniform increase

**24 November 2026 · private.** At the common visibility peak (\(z=1089.17\); baseline conformal time 277.89763 Mpc), adding the measured 76.8–83.2 Mpc interval **cuts the magnitude of the MTS-minus-baseline photon energy response by 55.66%** and **makes the photon current response 14.05 times larger** than the response from the first two post-64 intervals alone. Their joint magnitude falls **34.09%**. The preceding matter-target pivot at 273.33 Mpc is not the photon scoring time. No new matter interval or observational fit was run.

### Isolated peak contributions from the three intervals

Percentages below use the same original two-component **signed launch norm** for the paired difference (\(1.8923589892\times10^{-12}\)). Magnitudes are taken **after** addition of complex responses, not before.

| MTS minus baseline, finest gravity step | Photon energy | Photon current | Joint magnitude |
|---|---:|---:|---:|
| 64–70.4 alone | 0.97833% | 0.37044% | 1.04612% |
| 70.4–76.8 alone | 0.37481% | 0.34403% | 0.50876% |
| First two, signed sum | 1.35307% | 0.04701% | 1.35389% |
| 76.8–83.2 reversal alone | 0.75701% | 0.68413% | 1.02034% |
| All three, signed sum | **0.59996%** | **0.66049%** | **0.89230%** |

The reversal energy points almost opposite the first-two energy (alignment −0.99772). The 14-fold current change has a different cause: two earlier current magnitudes near 0.35% each had already largely canceled. The third interval dominates the small remainder; the current alignment with that remainder is −0.52852, not positive amplification of its original phase. Overall 34.65% of the sum of the three separate paired vector magnitudes survives. The result is for the retained Fourier mode \(k=0.3368801156\ {\rm Mpc}^{-1}\), not a percentage change in the sky.

| Physical scattering, p32 | Final energy / first-two energy | Final current / first-two current | All-three joint / corresponding launch |
|---|---:|---:|---:|
| Cold baseline | 0.36276 | 4.52662 | 0.08917% |
| Heavy MTS | 0.30102 | 4.34448 | 0.08084% |
| Signed MTS minus baseline | 0.44340 | 14.04973 | 0.89230% |

The last column uses the appropriate branch or paired launch norm, so the branch percentages must not be subtracted to obtain the paired percentage. The physical total before 64 is not included in these isolated readouts. For context only, **holding the archived through-64 complex photon state fixed**, adding these three contributions changes its joint paired peak magnitude from 1.48105% to 1.58214% of launch. This is not a fully p32-recomputed prehistory. [Complex readouts](evidence-001.zip) (archive member: `readouts.csv`) · [signed interference and both step sizes](evidence-001.zip) (archive member: `signed-reversal.csv`) · [frozen-history reference](evidence-001.zip) (archive member: `frozen-prehistory-context.csv`).

### What scattering changes

For a matched comparison in photon units, we switched off only Thomson opacity, retaining both source histories, free streaming, expansion and the same physical readout epoch. **For the reversal interval alone**, the physical energy magnitude is **80.74%** of its transparent counterpart, current is **86.90%**, and the joint magnitude is **83.34%** (joint alignment +0.99932). These are amplitude ratios for this isolated forced response, not probabilities or a fraction of a gravitational potential converted to light.

That factor cannot be applied to all intervals. Without scattering the reversal and the first-two joint response are nearly opposite (alignment −0.99858); only 4.12% of the sum of the three magnitudes remains. Physical scattering changes those phases (alignment −0.75209 between the reversal and first two), so the all-three joint difference is **6.24 times** the transparent all-three difference even though scattering reduces the isolated reversal. [Opacity control](evidence-001.zip) (archive member: `opacity-counterfactual.csv`).

### Construction and checks

The original forcing terms are \(4\Phi'\) into the photon energy equation and \(4k\Psi/3\) into the coupled baryon and photon momentum equations. The matter inputs are the constraint rate and lapse, **not** the transported cancellation targets. Both forcing channels can reach both photon outputs. We projected on one common fine photon time mesh per model, with each model's own opacity, loading and expansion. We used each block's own source spline, including distinct one-sided endpoint values; forcing is zero outside the block **only to isolate its linear contribution**, not to claim the later physical matter vanishes. All sources are compared before any modulus is taken. An independent direct integration retained separate real and imaginary energy/momentum drives for all three blocks and both gravity steps; it evaluated the output at the peak using cubic interpolation rather than the transposed readout.

For the independent zero-opacity check the scalar free-streaming hierarchy sends a unit initial monopole into \((j_0,j_1)\) and a unit dipole into \(3(j'_0,j'_1)\), with argument \(k(\eta_{\rm peak}-\eta)\). Integrating these responses against the same sources tests the no-scattering result without the numerical photon hierarchy or adjoint solve. No visibility function is inferred for the transparent toy universe.

- Both gravity steps give the same reversal: p16 vs p32 leaves 44.3385% vs 44.3404% of the earlier energy magnitude, and 14.0504 vs 14.0497 times the earlier current. Relative differences of the actual complex three-block outputs are **0.00337% energy, 0.00904% current, 0.00706% joint**.
- All 1,620 component, channel and joint comparisons in [sensitivity](evidence-001.zip) (archive member: `sensitivity.csv`) passed the unchanged 0.5% criterion. They include gravity-step, photon-time and angular controls, and forward vs adjoint in the physical medium. Worst physical relative change: 0.0266%; worst opacity-zero relative change: 0.0680%. Largest forward/adjoint difference: \(1.02\times10^{-11}\) relative.
- All 36 historical closure comparisons, 225 combined-forcing scattering-ratio comparisons, and 540 independent free-streaming and quadrature comparisons passed. [Validation and source hashes](evidence-001.zip) (archive member: `validation.json`) · [analytic free-streaming checks](evidence-001.zip) (archive member: `streaming-analytic-check.csv`). Results are local; original matter coverage still ends at 83.2 Mpc.

**Next:** test the same three isolated contributions over the *finite width* of last scattering: first take the signed sum at each common scale, then calculate the original visibility-weighted energy/current readouts. Compare peak against window and both gravity steps before extending the matter history. This distinguishes a phase cancellation specific to one time from a feature that persists over the emission window.
