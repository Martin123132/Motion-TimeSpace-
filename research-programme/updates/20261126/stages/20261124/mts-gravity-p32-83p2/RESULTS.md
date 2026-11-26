> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# 76.8–83.2 Mpc: the reversal survives a stricter gravity calculation

**Outcome (24 November 2026, private).** The previous interval had reduced both paired targets. The new interval reverses that trend. Relative to the work still needed at 76.8, the magnitude of the signed MTS-minus-baseline cancellation needed at the fixed 273.33232 Mpc target **increases by 93.55% for the effective current and 75.37% for the lapse**. The earlier (p16) run gave +93.55% and +75.37% to the same precision. These are changes in the remaining source-work targets, *not* percentage changes in an observed spectrum. Physical matter coverage ends at 83.2.

**The original numerical failure mattered.** We retained the [failed p8/p16 comparison](../mts-physical-impulses-83p2/RESULTS.md) and halved the step again instead of changing the tolerance. Each model was rebuilt from the same sealed 57.6 joint state across **all four intervals**, using exactly the same common and 77 finite-momentum sources and the same angular, material and stress rules. The new gravity step is 0.0001953125 Mpc.

| Shift between the two compared solutions, in the original one-term peak allowances | p8 vs p16 | p16 vs p32 |
|---|---:|---:|
| Paired current, at 83.2 | 0.00518 | **0.000647** |
| Paired lapse, at 83.2 | **1.39785 (fail)** | **0.17497 (pass)** |
| Paired lapse, largest sampled inside 76.8–83.2 | **1.66786 (fail)** | **0.20875 (pass)** |

The largest refined sampled lapse displacement occurs near 83.16894. These are resolution checks at fixed physical input, not rigorous continuum-error bounds. The one-term allowances were unchanged: \(5.506091776945591\,10^{-18}\ {\rm Mpc}^{-1}\) (current) and \(3.043355946343286\,10^{-17}\) (lapse). [Absolute checks](evidence-001.zip) (archive member: `absolute-test.csv`) · [center progression at 64, 70.4, 76.8 and 83.2](evidence-001.zip) (archive member: `cut-centers.csv`).

### Why separate model magnitudes do not tell the story

| Finest resolution | Current target remaining vs its value at 76.8 | Lapse target remaining vs its value at 76.8 |
|---|---:|---:|
| Cold baseline | 13.61% | 34.14% |
| Heavy MTS | 52.80% | 28.50% |
| Signed paired comparison | **193.55%** | **175.37%** |

Both individual magnitudes fell, but they did not change together in the complex plane. The paired result is computed at the same scale factor, with the clock mismatch explicit; it is not the subtraction of these percentages. The new impulses have negative alignment with the entering cancellation directions (−0.369 for current, −0.488 for lapse). The paired lapse target briefly falls to **21.13%** of its entering magnitude near 83.14156 Mpc before ending at 175.37%. The extrema are sampled numerical values, checked against a doubled readout grid; they are not bounds between nodes. Relative to the cut at 64, 140.97% of the original current target and 116.72% of the original lapse target remain. This reverses more than the preceding gain; extrapolating a monotone trend would have given the wrong answer. [Sampled paths and extrema](evidence-001.zip) (archive member: `inside-block.csv`).

### Physical work and numerical checks

At the peak pivot the transported work generated solely in 76.8–83.2 is \((-4.17285+3.47811i)10^{-16}\ {\rm Mpc}^{-1}\) for current and \((-1.64849+1.26158i)10^{-13}\) for lapse. The latter is dominated by current work; shear contributes \((1.95310-1.99971i)10^{-16}\) and clock mismatch \((3.87937+9.59087i)10^{-20}\). The new centers for the uncomputed subsequent work are \((2.89920-7.36315i)10^{-16}\ {\rm Mpc}^{-1}\) and \((1.36084-3.25004i)10^{-13}\). The actual photon response is a separate integral over the history; a larger cancellation target alone does not establish a larger observed photon signal. [Signed work, both branches and both resolutions](evidence-001.zip) (archive member: `physical-work.csv`).

The fine paired curvature-rate discrepancy contributes 0.03199 of a lapse allowance, versus 0.09019 at p16 for this block. Along the total control shift the inherited launch contributes +0.08379 allowance, the change in that discrepancy +0.07505 and physical longitudinal work +0.01615. The discrepancy is between differentiating the saved potential and reading its rate from the constraint. It is not subtracted as a physical source correction. [Defect cross-checks](evidence-001.zip) (archive member: `rate-checks.csv`) · [sensitivity attribution](evidence-001.zip) (archive member: `lapse-attribution.csv`).

All **264 relative checks** passed (96 trajectory, 132 integration/reconstruction, 36 resolution comparisons) at the original 0.5% tolerance. All **26** additional replay, rate, kernel and profile checks passed, along with both endpoint and within-block allowance tests. The eight rebuilt model/block restarts and their parent hashes are recorded in [validation](evidence-001.zip) (archive member: `validation.json`). p32 matter and phase-space states for continuing start in `to83/`; p16 controls and the common and 77 individual incident endpoints remain in the sealed initial 83.2 directory. No fitting, observations, publication or GitHub changes.

**Recommended next test:** before buying another physical interval, use the saved photon transport and the three measured post-64 source blocks (64–70.4, 70.4–76.8, 76.8–83.2). Compare their *signed* contribution to photon energy and current at the visibility peak for baseline and MTS with both gravity steps. This tests whether the source reversal survives scattering or largely cancels in what reaches the photons; it does not assume zero later forcing.
