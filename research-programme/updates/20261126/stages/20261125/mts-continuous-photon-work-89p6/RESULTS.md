> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# The photon gap survives continuous matter and gravity evolution

**Removing all the gravity-cell resets changes the joint photon gap from 0.577985% to 0.576361% on the fine clock.** The coarse result is 0.576350%. The photon prediction was frozen at both gravity steps, with time and angular controls, before opening the archived photon comparison. The reset was not the cause of the 0.5% crossing on this saved window.

| Joint visibility-weighted result | Coarse gravity | Fine gravity |
|---|---:|---:|
| Archived per-cell reference | 0.577973% | 0.577985% |
| Continuous, one launch per branch | **0.576350%** | **0.576361%** |
| Continuous, direct change of energy-vs-momentum potential on the same matter | 0.576419% | 0.576430% |
| Signed vector change vs per-cell reference, % of the reference itself | 0.283681% | 0.283800% |

The first three rows are percentages of the original small momentum-route correction, not of the photon launch. Complex energy and current histories are subtracted before taking visibility-weighted norms. The fine continuous components are **0.576582% energy** and **0.575593% current**, both above the unchanged 0.5% gate. The separate original-launch size is **0.003648%** after the correction, within its unchanged 0.163% limit. Agreement with the old reference and passing the physical component gate are different questions.

**What was actually continuous.** At 89.148503803 conformal Mpc, we took the matched physical launch archived by the previous continuity test and the native wave interpolant at that same initial instant, as in the per-cell comparison. On each branch all 12 lower matter variables plus the potential were propagated to 89.6 Mpc. Each state fed the next update, including across the source corners. Φ was advanced only by the momentum equation; we did not project it back onto the energy constraint. After launch the native saved-state/potential evaluators were explicitly disabled. The matched driver loaded only the prescribed quadrupoles, stress and external coefficients, not a history of ordinary or heavy initial values. This is conditional on the same upper multipoles, 77-bin stress/forcing and closure; it is not a new fully autonomous Boltzmann hierarchy or an observational fit.

**Independent accounting.** For each route let C = U − DΦ − E/2 − 3HJ/(2k²) in the retained variables. We evaluate the source-work impulse ΔC/D_right using the integrated state increments and changing weights, not by setting C to zero or subtracting a known total to determine the metric. Independently evaluating C at endpoints gives

    ΔC/D_right = Δ(C/D) + C_left (1/D_left − 1/D_right).

Here C/D is what the energy constraint would add to the momentum-evolved potential on the *same* matter. It is not a second evolution with constraint feedback. The conventional and direct-potential photon vectors differ by only **0.01527% of the continuous work vector** on the fine step; the normalizing weight is not the reason the gap survives. The fine matched branch alone is 0.537487% and the native branch 0.082399% on the original common scale. In the *change on removing resets*, 90.33% of the signed projection lies along the matched-branch change and 9.67% along the subtracted native-branch change; these are shares of the small reset effect, not of the whole discrepancy.

**Accuracy.** The coarse-to-fine signed joint difference is 0.00214% of the continuous result. On the fine clock halving the source substep changes the vector by 0.00120%; the photon-time control changes it by 0.000016%, and the angular control gives no change at stored precision. These are refinement checks, not formal continuum error bounds. The continuous matched density and current independently reproduce the previous switch-launched continuity solution. All 36 trajectory and 96 photon controls pass the retained tolerances. No input, launch, fit or published result was replaced.

**Next test:** release the prescribed photon and collisionless quadrupoles from their saved histories and evolve their angular moments from the switch on both branches, retaining the same external forcing and 77-bin stress as controls. Freeze the coupled-minus-prescribed prediction before scoring the photon energy and current. This tests another physical assumption instead of subdividing the same interval again.

[Protocol](PROTOCOL.md) · source freeze (not bundled here) · photon freeze (not bundled here) · [unchanged gates](evidence-001.zip) (archive member: `gates.csv`) · [signed comparisons](evidence-001.zip) (archive member: `signed-comparisons.csv`) · [where the reset effect enters](evidence-001.zip) (archive member: `reset-attribution.csv`) · [trajectory checks](evidence-001.zip) (archive member: `trajectory-controls.csv`) · [photon checks](evidence-001.zip) (archive member: `photon-controls.csv`).
