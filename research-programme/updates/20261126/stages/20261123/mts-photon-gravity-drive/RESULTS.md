> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# Longest photon wave: separate carried and regenerated signals
23 November 2026. Local continuation of the sealed 77-bin photon test. The gravitational drive from the **regular primordial curvature component** raises the joint MTS-minus-cold amplitude slightly across the last-scattering window, but lowers it at the peak. The part driven by the quadratic matter and radiation sources has not been extrapolated.

| Fraction of this same wave's launch contrast, expressed as percent | RMS over z=1500–750 | At peak visibility |
|---|---:|---:|
| Launch photon energy/current propagated freely through the scattering plasma | 3.83543% | 1.40429% |
| Post-launch regular gravitational drive, zero additional initial photons/baryon velocity | 0.46820% | 0.50440% |
| Both, with phases kept | **3.92974%** | **1.31838%** |

These are joint amplitudes of energy and current for the (4,2,1) Fourier probe, k=0.3368801156243423/Mpc. The denominator is the previously frozen two-component contrast at the common launch scale, not the cold signal or the observed sky. Subtract MTS minus cold at equal scale **before** taking a norm. The regular drive changes the RMS by +0.09431 percentage points, not +0.46820 points: its signed projection onto the freely propagated pattern is only weakly positive (weighted alignment 0.143). Its response is mainly energy, and the phases partly cancel at the visibility peak.

## How the drive was identified

The saved field family is affine in initial curvature: metric = particular + c (unit-curvature solution − particular). The basis difference agrees with the independent regular native metric multiplied by the saved primordial pair. Over 65 overlapping early times, worst Phi/Psi discrepancy is 0.000030% for cold and 0.00393% for MTS (normalized to each channel's peak). Only the basis difference was continued with the regular native solver. Each branch kept its early coefficient c, convolution pair, normalization and phase. This is not a new linear mode of arbitrary amplitude added at recombination.

The MTS phase table did not contain the actual k. Its nearest row, 0.3375/Mpc, was **not** substituted. We evolved the exact heavy-field oscillations at the requested k, used the original six-cycle, degree-eight phase projection, and replayed the neighboring tabulated control. Target pressure-closure residual: 1.51e-7 of the inherited mode norm (gate 2e-6); neighboring density and momentum rows recovered to 2.05e-15 of that norm or better. The extra row was inserted only into the in-memory matching table for these runs. All archived tables are unchanged.

In the same longitudinal convention as the inherited photon equations, post-launch gravity supplies 4 Phi' to D', and 4 k Psi/3 to both J' and U' (U=4 v_b/3). The latter common acceleration does not directly source photon–baryon slip. Phi=etak/k−Hc sigma/k and Psi=2 Weyl−Phi. Phi' is recovered from total momentum, and separately from differentiating the native shear and curvature variables using the background acceleration. A second transport uses D−4(Phi−Phi_launch) and the potentials rather than their derivatives. This yields the same physical energy after reconstructing D. We evolved the free, driven and coherent sums separately, and tested a native-state replay against independent native photon energy and current. The tagged primary drive starts at zero so it does not count any of the saved photon launch twice.

## What the checks caught

The first sampling grid missed some fast MTS gravitational oscillations before the heavy-field matching surface. Comparing two forms of the drive on the *contrast* moved the window amplitude vector by 0.5145%, above the unchanged 0.5% threshold, although either branch alone passed. We kept that failure. With 32 samples per old early grid interval through the matching region, and corresponding refined time integration, all 42 final comparisons pass for both RMS and peak. They include time, angular order, source sampling, native hierarchy accuracy, an independent drive equation and native-plasma replay. Worst final relative movement is 0.0113% in the window and 0.0109% at peak. These are numerical checks, not an observational uncertainty. No new amplitude fits.

## The part that still matters

The 77-bin run also contains a **particular** potential caused by the interacting matter and radiation. It is measured through 25.6 conformal Mpc but the inspected regular-start run does not carry it to recombination. The same-k saved interval near 87–89 Mpc has a different initialization; the longer two-wave recombination calculation is a different experiment. Neither was spliced onto this history. At launch the particular energy-driving source |4 Phi'| is about 23 times the regular source in **both** branches; its acceleration |4 k Psi/3| is about 14.5 times the regular source in cold and 17.0 times in MTS. Those are instantaneous source ratios within branches, not ratios of the late contrast. They do not determine either its sign or its later size.

**Restart:** advance the curvature-zero, matter-sourced gravitating solution from the actual 77-bin restart across a short first post-launch block (suggested endpoint 32 conformal Mpc); check Phi' from the constraint and independently from the derivative of Phi on both backgrounds. Feed that verified block into the same retarded scattering response, leaving later unsourced blocks separate. The regular drive and launch photon terms here can be reused unchanged.

[Component results](evidence-001.zip) (archive member: `results.csv`) · [complex markers](evidence-001.zip) (archive member: `signed-markers.csv`) · source coverage (not bundled here) · [launch drives](evidence-001.zip) (archive member: `seam-forcing.csv`) · [numerical tests including rejected coarse result](evidence-001.zip) (archive member: `checks.csv`) · [verification](evidence-001.zip) (archive member: `verification.json`). The drive-*-resolved archives retain the separate complex histories. Run verify_drive.py for a read-only replay of the seal. No new data, fitting, external publication or continuing worker.
