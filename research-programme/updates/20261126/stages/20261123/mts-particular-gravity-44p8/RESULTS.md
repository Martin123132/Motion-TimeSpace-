> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# 38.4–44.8: the new gravity contribution reduces the photon contrast at the peak and across the window

23 November 2026. Private continuation from the two sealed 38.4 conformal-Mpc states. Longest frozen wave (4,2,1), k = 0.3368801156243423 per comoving Mpc. Both backgrounds, the 77 momenta, angular grids, early amplitudes, visibility window and 0.5% tolerance were retained. Only the particular gravitational force in the new interval is added. No phases, amplitudes or comparisons were fitted.

| MTS minus cold baseline | Last-scattering window RMS | At the common visibility peak |
|---|---:|---:|
| Previous history through 38.4 | 4.3884% | 2.0307% |
| New interval in isolation | 1.3456% | 0.3954% |
| Signed sum through 44.8 | **3.8467%** | **1.8714%** |
| Net change (percentage points) | **−0.5417** | **−0.1593** |

The percentages are relative to the *original joint energy/current launch contrast* (1.8923589891767267e-12). The two branches are compared at common scale factors using the normalized baseline visibility and conformal-time weighting, 750 ≤ z ≤ 1500. This is a numerical prediction for one Fourier wave, not a measurement or a sky power spectrum.

**Why both readings decrease.** The new complex photon response is partly opposed to the accumulated one: normalized alignment −0.531 across the window and −0.484 at its peak. Energy and current RMS from this interval alone are 1.1817% and 0.6436% of launch, combined in quadrature. The *individual* RMS readings actually rise: cold 4.1959% → 4.2611% and MTS 4.1987% → 4.2785%, each relative to its own launch. It is the difference between the fields that falls.

**Similar size does not mean the same history.** The accumulated contrast now has nearly the same RMS size as the freely propagated photons (3.8467% vs 3.8354%). As a follow-up diagnostic, subtracting the free history *before* taking the norm gives **2.4306% of launch** for the net response to the retained gravitational drivers. Taking the difference of RMS sizes instead would obscure this response.

## Numerics

- Continued the 77 incident states for each background. The joins agree to better than 2e-16 relative; direct independent checks on slow, middle and fast bins agree below 1e-15. Native material samples were newly obtained except for the 17 reused overlap times. Copied values are not counted as independent confirmations.
- Before any photon scoring, compared inner steps 0.0015625 and 0.003125 conformal Mpc with the returned stress held fixed. The signed potential, lapse and potential-derivative changes were 0.1202%, 0.1145% and 0.0222% of their own peaks. Independently differentiating the potential agreed with the signed constraint derivative to 0.0492%. All passed the original 0.5% gate. Both branches used identical numerical settings; neither needed a retuned restart.
- All 27 transfer comparisons and six end-to-end fixed-stress step comparisons passed for baseline, MTS and their difference (window and peak). The new interval contributes exactly zero before it starts; the verification checks that the preceding history is included exactly once.
- Reassembled all three source intervals coherently using each numerical setting in turn, keeping launch and regular drive fixed. Even the largest tested shift in the final signed history was only 0.0938% across the window and 0.1116% at the peak. All five settings give a fall in both readings: −0.54170 to −0.54122 percentage points across the window; −0.15929 to −0.15927 points at peak (outward-rounded). This controls the numerical comparison, not the size of uncomputed later forcing.

[By branch and contribution](evidence-001.zip) (archive member: `results-p4.csv`) · [pre-transfer gravity check](evidence-001.zip) (archive member: `pre-transport-gate.json`) · [time-step comparisons](evidence-001.zip) (archive member: `matched-step-check.csv`) · [signed interference](evidence-001.zip) (archive member: `interference-p4.csv`) · [all three intervals](evidence-001.zip) (archive member: `all-three-blocks-control.csv`) · [direction under paired controls](evidence-001.zip) (archive member: `direction-under-paired-controls.csv`) · [full minus free](evidence-001.zip) (archive member: `net-drive-versus-free.csv`) · [transport controls](evidence-001.zip) (archive member: `controls-p4.csv`) · [propagated step test](evidence-001.zip) (archive member: `frozen-stress-step-propagated.csv`).

**Next manual test:** isolate 44.8–51.2 from particular-cold-p4.npz and particular-heavy-p4.npz and the accompanying common and 77 finite-momentum endpoints for each model. Keep testing the isolated response as well as its coherent sum; closeness to the free RMS is not a stopping rule for the forcing. Scope and tolerance are recorded in [the protocol](PROTOCOL.md). Use verify44.py with bytecode disabled to recheck the seal.
