> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# Restoring the through-64 photon history reverses the marginal result

24 November 2026 · Local · Retained mode (4,2,1), k = 0.3368801156243423 per comoving Mpc.

Adding the third source interval (76.8–83.2 conformal Mpc) **reduces the full-window joint MTS-minus-baseline RMS by 14.93%** when both models include their fixed through-64 photon histories. The same interval **increased** the isolated post-64 contrast by 8.70%. These are two comparisons with different starting histories, not conflicting numerical runs.

| Paired window RMS, p32 | Through 64 | With first two (through 76.8) | With all three (through 83.2) | Third versus first two, including history |
|---|---:|---:|---:|---:|
| Photon energy | 3.99436% | 3.97838% | 3.38072% | −15.0225% |
| Photon current | 2.11397% | 2.12706% | 1.81618% | −14.6152% |
| Joint | 4.51927% | 4.51130% | 3.83768% | −14.9318% |

The first three numeric columns are percent of the original joint launch contrast (1.8923589891767267e-12); the last is a change relative to the through-76.8 value. All three intervals together reduce the joint contrast **15.0817%** relative to through 64. This is a partial-history diagnostic for one Fourier mode, not a percent change of the observed CMB.

| Joint RMS with fixed earlier photons | Through 64 | Through 76.8 | Through 83.2 | Third interval change, p16 / p32 |
|---|---:|---:|---:|---:|
| Cold baseline | 4.14708% | 4.25656% | 4.27521% | +0.43812% / +0.43812% |
| Heavy MTS | 4.14041% | 4.26669% | 4.29588% | +0.68425% / +0.68425% |
| MTS minus baseline | 4.51927% | 4.51130% | 3.83768% | −14.93118% / −14.93182% |

Each row uses its own original joint launch norm. Both branch magnitudes rise slightly but their **complex difference**, formed before squaring, shrinks. The separate branch percentages must not be subtracted to obtain the paired percentage.

**What flips the sign.** In squared percent-of-launch units, the third interval adds +3.33555 of its own joint power. Its cross term with the first two contributes −1.81694, leaving +1.51862 in isolation. Its additional cross term with the **through-64** photons is −7.14266. The resulting joint power change is −5.62404. This identifies interference with the earlier history, not a change in the source or a retuned amplitude. [Power balance](evidence-001.zip) (archive member: `third-power-balance.csv`).

**Method and checks.** The fixed history is the sealed native complex `new_partial` in the primary through-64 transfer for each branch (final pre-64 interval at p8). It is already propagated across the emission window and contains earlier photons, regular driving and earlier particular forcing. It is not a state at recombination initialized from a single value, and it was not recomputed at p16 or p32. Added histories used the saved physical photon scattering, original 77-bin matter inputs, both post-64 gravity steps, and the original common baseline visibility weight over 750 ≤ z ≤ 1500. Addition and heavy-minus-cold subtraction precede the weighted RMS, at equal scale factor. The joint RMS is the square root of the sum of the two component powers.

The calculation reproduces the archived through-64 RMS, the old isolated ratios, and the previous accumulated complex peak for each preparation and step. All **288 numerical comparisons** pass at the unchanged 0.5% tolerance, including complex-history changes with gravity, photon time and angular settings, quadrature doubling, and the smaller signed changes themselves. The two post-64 gravity steps differ by **0.00456%** in the accumulated paired joint complex history over the window. Error estimates here condition on the same earlier history. [Full readouts](evidence-001.zip) (archive member: `window-readouts.csv`) · [Checks](evidence-001.zip) (archive member: `checks.csv`) · Hashed inputs (not bundled here) · [Isolated control](../mts-photon-visibility-window-post64-three/RESULTS.md).

**Next:** take the existing 83.2 Mpc physical matter restarts to 89.6 Mpc at both accepted gravity steps, and test the new contribution against these saved accumulated photon histories. The drop here cannot be used to assume later gravitational driving is negligible. No further matter interval was run for this comparison.
