> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# Fixed occupation: what the LMC changes, and what the chosen background already supplies

20 November 2026 • local MTS parent research • no new observations, sky fits, or publication.

**The wave moves mass inward without gaining particles. On the two original Milky Way preparations that does not put another radial or polar component into its observed band.** A separate comparison on the six simulations' own ordinary-matter backgrounds gives a materially different score, but it is already there before the satellite response is switched on.

## Same signed radial and polar bands

The independent original retarded replay (not bundled here) was rerun read-only this stage. It reproduced all 12 original preparation/history combinations, final density multipoles, and all 192 signed wave/control rows within unchanged tolerances. The force in the original comparison is its saved subtotal **plus** the newly isolated m=0 term (the earlier direct satellite and retained m=2 subtotal are not counted again). The separate [extended-bar m=0 calculation](../mts-extended-bar-fixed-occupation/RESULTS.md) also gives 2/8 without any rotating-wave term.

| Background and test | MTS | Matched static NFW | Native collisionless halo |
|---|---:|---:|---:|
| Original two Milky Way preparations, six saved histories | 2/8 | 2/8 | Not a common-background control here |
| Simulation's ordinary disk and bulge, initial outer normalization matched, m=0 only | 6/8 | 4/8 | Frozen: 4/8; evolved: 4–5/8 |

On the original grounds, 1.67–3.48 × 10⁸ solar masses move inside the 6.185 kpc sphere and are compensated by a loss outside it. The satellite closes only 1.08–2.44% of the earlier inner radial deficit; its northern inner polar contribution has the opposite sign to the needed increment. Only the two outer polar components pass. The time history matters: instantaneous equilibrium gives the opposite sign for the inner northern polar change. The original domain-refinement check varies the very small induced polar term by up to 0.2264%, above the original 0.002% precision target, but does not flip any band decision. High replay agreement is not the same as high absolute physical accuracy.

For the simulation-background comparison, each of two representations of each of six hosts supplies its stationary ordinary foreground. One initial dark force at 17.58 kpc sets the wave normalization; it is then held fixed. No inner datum or final-time response selects it. Wave masses are 1.502–1.512 × 10¹¹ solar masses. No additional stellar bar is inserted here. This controls one initial force and the environment, not the complete initial shape or phase-space state. It is a sensitivity test, not a new preferred Milky Way mass model.

| Northern site, z=1.5 kpc | m=0 LMC force alone | MTS total | Static NFW total | Original band |
|---|---:|---:|---:|---:|
| R=6 kpc, radial | −0.00880 to −0.00426 | −2.339 to −2.326 | −2.608 to −2.597 | −2.552 to −2.230 |
| R=6 kpc, polar | −0.000448 to −0.000235 | +0.6362 to +0.6433 | +0.6284 to +0.6356 | +0.5734 to +0.7690 |
| R=8.3 kpc, radial | −0.00896 to −0.00435 | −1.851 to −1.837 | −1.941 to −1.930 | −2.200 to −1.959 |
| R=8.3 kpc, polar | −0.000422 to −0.000236 | +0.3425 to +0.3497 | +0.3373 to +0.3446 | +0.2375 to +0.3648 |

Units: 10⁻¹⁰ m/s². Rows show zero-start waves and the simulation's accelerating frame, both field representations; positive polar follows the saved spherical convention. The south is evaluated directly with signed bands. The wave on these backgrounds misses both *outer radial* components. Turning off the induced wave entirely still gives **6/8**. Adding m=2 keeps **6/8**. Both start prescriptions and both frame checks preserve these scores. The matched static NFW is actually closer to the missed outer radial target. There are not twelve independent observational samples here: six alternative satellite histories, each with two representations. No detection, independent fit or model probability follows from counting bands.

Applied the same Poisson force kernel to the reconstructed m=0 density, and independently used the modal force rows. Agreement ≤1.4 × 10⁻¹⁷ in the table units; maximum first-order fractional number change ≤3.51 × 10⁻¹⁸. Half-time-grid change ≤2.08 × 10⁻⁶ relative; two 64→88 basis spot checks ≤2.73 × 10⁻⁶ (target 2 × 10⁻⁵). These are numerical checks on the discrete solver, not uncertainty in the galaxy. See matched-axis-only-*-k64.csv (all signed components), matched-axis-density-*-k64.npz (signed density multipoles), and [checks.json](evidence-001.zip) (archive member: `checks.json`).

## Separate prediction: the three-ring tangential force

On the two previously prepared extended-bar backgrounds the LMC-driven m=2 wave **reverses** the original positive bar-only forecast. With the ring weights, phase, and occupation frozen, the predicted contrast after subtracting the direct LMC is **−8.07 to −5.40 × 10⁻¹³ m/s²**, versus zero for the static spherical dark control. This is not a measurement of tangential acceleration; none of the eight radial/polar bands measures it.

- In units of the table above, the bar alone gives +0.001323 to +0.001346. The satellite wave gives −0.009420 to −0.006724. Including the direct satellite, raw MTS is −0.010353 to −0.006531 versus −0.002279 to −0.001129 for the static control. All six histories reverse the sign on both backgrounds. The alternative start does too.
- The uniform part of the external tide contributes **nothing directly** to the weighted statistic, but deforms the wave enough to contribute −0.011329 to −0.007734. Its spatially nonuniform remainder offsets part of this. A full sparse static inverse gives −7.229 and −7.207 kpc for the ratio of induced contrast to the local uniform tidal gradient. This is a model-dependent response, not an adjustable scale. Basis, time and source refinements lie within 2 × 10⁻⁵ for this contrast. Increasing the radial box changes it by up to 2.49 × 10⁻⁴ relative (absolute ≤2.27 × 10⁻⁶ in table units); this exceeds formal precision but is far smaller than the sign change.
- Matched wave changes, final minus initial, on the simulation foreground are −0.00589 to −0.00432; the native collisionless halo changes cover −0.01321 to +0.00083. The ranges overlap. A static spherical halo is a useful zero, not a stand-in for a live halo. The simulation's full evolution is not guaranteed to be solely the satellite wake.
- A freely chosen m=2 initial disturbance could erase the sign: a minimum of 5.73–7.57% of the forced energy in the unrestricted optimal shape, or 13.62–17.98% while preserving all four independent meridian force readouts. But a wave initially unexcited and driven solely by a one-way pre-archive turn-on of the first saved spatial forcing shape cannot do it: the required energy exceeds the rigorous linear discrete one-way ceiling by a factor of at least 604 (1,437 with the meridian constraint). No upper bound on unrelated earlier formation perturbations has been assumed.

Signed ring outputs (not bundled here) • [matched live changes](evidence-001.zip) (archive member: `matched-comparison.csv`) • [free-state thresholds](evidence-001.zip) (archive member: `free-state-gate.csv`) • [derivation](DERIVATION.md) • [replay](REPLAY.md).

**Next local test:** separate the change in ordinary disk/bulge force from the change in the stationary wave normalization between the two preparations; constrain those choices using light or stellar-mass information independent of these eight bands. The decisive discrepancy is the outer radial force on the simulation foreground, not the sign of a tiny tilt in its polar force. Do not tune occupation or select the foreground by maximizing the pass count.
