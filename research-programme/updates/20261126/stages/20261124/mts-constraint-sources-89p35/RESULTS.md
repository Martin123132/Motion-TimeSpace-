> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# What breaks the metric-rate check near 89.35 Mpc

**24 November 2026 · local source-isolation test · retained mode k = 0.3368801156243423 Mpc⁻¹.** The leading discrepancy is in the flux-squared part of the quadratic geometry source, not the photon scattering solver. Reconstructing that term from the heavy field's **momentum and enthalpy together** takes the matched calculation below its unchanged 0.5% metric-rate limit for both saved launches and both gravity steps. Restoring heavy pressure alone fails. This is a wave-informed diagnostic: it still uses the resolved heavy perturbation after the switch.

## A controlled reversal

These are maximum errors over the complete 89.1485038–89.6 interval, normalized to the maximum momentum-constraint rate on that branch. The spatial interpolation rule, clocks, 77-bin recoupling, initial conditions and 0.5% gate are unchanged. Seed 0 supplies the photon readout.

| Calculation, seed 0 | p16 error | p32 error |
|---|---:|---:|
| Matched surrounding sources, unchanged | 1.3424% | 1.3425% |
| Explicit-wave surroundings, same one-sided stencil | 0.3619% | 0.3619% |
| Matched, replacing only U by the wave value | 0.3914% | 0.3915% |
| Reverse: wave surroundings, replacing only U by the matched value | 1.3564% | 1.3566% |
| Matched, reconstruct only the heavy pressure part of the flux change | 0.9597% | 0.9602% |
| Matched, reconstruct the heavy synchronous momentum and enthalpy pair | **0.4580%** | **0.4582%** |
| Reverse: remove that pair's wave contribution inside the flux square | 1.3989% | 1.3989% |

The paired reconstruction passes on seed 1 as well (0.3134% on p32). It transfers the heavy contribution only inside the squared flux: this is not a global replacement of the native gravity solver. The reverse failure and the negative pressure-only control matter more for attribution than a small improvement on one run. [Absolute constraints by seed](evidence-001.zip) (archive member: `absolute-constraints.csv`) · [two-way U test](evidence-001.zip) (archive member: `test-waveUinMatched-p32.csv`) · [paired test](evidence-001.zip) (archive member: `test-pairInMatched-p32.csv`).

## Where the excess comes from

The energy-constraint derivative was decomposed independently of the momentum constraint, including the full metric denominator, curvature slip, quadratic forcing and all retained species. At the saved p32 peak (89.3525390625), U contributes **101.07%** of the signed matched-minus-wave residual on seed 0. Photon-state response cancels 2.85%; the cold density trace adds 1.29%. Across the full window the U share is 102.02%. These are projections of complex differences, not fractions of total energy. On replacing U, just 7.09% of the original window RMS discrepancy relative to the wave control remains on seed 0. [Peak decomposition](evidence-001.zip) (archive member: `rank-p32.csv`) · [window decomposition](evidence-001.zip) (archive member: `window-p32.csv`).

Recomputing U from the native mode pairs gives the stored source to better than 1.1e-15 in peak-relative error on each branch. The term proportional to the convolution of F with itself accounts for 103.09% of the signed U difference at the peak and 100.38% across the window. Within U the background pressure times the synchronous gauge shift supplies +116.69% at the peak; the independently changing synchronous momentum supplies −13.63%. They cannot be treated as two independent positive contributions. [Exact finite-product decomposition](evidence-001.zip) (archive member: `upstream-p32.csv`).

The native field equations explain the pairing: the resolved scalar has enthalpy v² and synchronous momentum k v δb. After the native switch, heavy enthalpy becomes the dust density and the corresponding momentum is the saved fluid current. Both enter the common-slice metric flux. Using these expressions on the same 782 input-mode rows predicts the total flux difference with 0.00722% peak-relative error and the resulting squared-flux difference with **0.01853%** error, without fitting a coefficient or using the donor U as an input. The synchronous wave momentum itself agrees with the separate native diagnostic to 4.8e-8 relatively. [Equations, normalizations and replay](DERIVATION.md) · independent reconstruction (not bundled here).

## What reaches the photons

The cold history and the photon launch normalization were kept fixed. For the paired diagnostic the joint correction is **0.00362484% / 0.00362483% of the original joint launch** (p16 / p32) using the momentum-constraint drive. Independently differentiating the metric gives 0.00365848% / 0.00365045%. Both remain far below 0.163%. Time, angle and gravity-step checks pass; the two rate routes differ by 0.935% / 0.710% relative to the small correction vector, so that separate 0.5% precision gate still fails. Passing the absolute metric-rate gate is not passing every photon precision check. No driving beyond 89.6 was added. [Readouts](evidence-001.zip) (archive member: `photon-readouts.csv`) · [checks](evidence-001.zip) (archive member: `photon-checks.csv`) · [verdict](evidence-001.zip) (archive member: `verdict.json`).

**Next:** attempt to predict the paired flux correction from phase and stress information available at the switch. Freeze that prediction before comparing with the next saved cycle, and do not provide the predictor with the later microscopic wave or a donor metric table. Recheck the absolute metric rate and the two photon rate routes unchanged. That would distinguish a usable coarse-field prediction from the retrospective reconstruction established here. No authoritative averaged restart or public update was made.
