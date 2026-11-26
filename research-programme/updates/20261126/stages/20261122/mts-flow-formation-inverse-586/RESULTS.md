> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# Which earlier formation produces the frozen flow?

**The archived formation histories produce forward flow in both preparations. Neither produces the reversed flow under the same ordinary drive.** Reversal is dynamically admissible: we recovered its required earlier state and advanced it back to the target. That earlier state is distinct even from the best complex linear combination of the two saved 586 preparations. This conclusion is about these initial conditions in this simulated host, not an observational identification of the Galactic current.

## From snapshot 590 back to 586 — 88.968349 Myr
We used all four frozen 590 targets (reset and inherited, each forward and conjugated), not four separately fitted configurations. At native resolution the original 586 states propagated directly to the saved forward launch states with zero array-norm discrepancy. The inverse forward states agreed with the archived formations to within 5e-13 of the wave norm after a constant phase alignment. The reversed trajectories also round-trip; it is *formation compatibility*, not existence of the inverse, that differentiates the signs.

| At 586 (280 steps, identical 590 targets) | Reset reverse | Inherited reverse |
|---|---:|---:|
| Norm mismatch from its own archive, global phase removed | 0.7441% | 0.4470% |
| Smallest norm mismatch allowing any normalized complex blend of the two archives | 0.4058% | 0.4345% |
| Fraction of the required pure state's norm-squared outside that span | 0.001647% | 0.001888% |
| Coordinate-space mass total variation from its own archive | 0.2837% | 0.2082% |

The small percentages are important: these are resolved requirements for an alternative preparation, not enormous changes that can be dismissed astrophysically. In the same finest-grid comparison, the ordinary forward solutions miss the native archive by only 0.00031% in wave norm. The last time-step change in the reversed state is at most 0.024% **of the orthogonal gap**, not of the full wave. The complex-span comparison is an additional exact geometric minimization at 586; it does not exclude the nonlinear descendants of other earlier preparations, which need not lie in that span.

## What changes in the gravitational source?
At the launch itself conjugation changes no enclosed mass. At 586, however, the wave mass enclosed by 8.43445 kpc would need to be **317.25 million solar masses lower** for reversed reset, or **248.08 million higher** for reversed inherited, each relative to its own reconstructed forward solution. These are −0.639% and +0.504% of the forward enclosed **wave** mass. The inner two faces change in the same direction within each preparation. These are spherically averaged source tests; the sign need not be the sign of the change in every local force component.

The same Newton coefficient converts those outer mass changes to −19.18 and +15.00 (km/s)²/kpc in the wave's mean inward radial force. No change to G, ordinary matter, wave mass, or metric coupling. Integrating the wave density inside the three spheres at 590 reproduces the saved flux-law mass vector within 2.2e-15 relative; computing current directly from the wave amplitudes reproduces its mass-rate vector within 7.8e-11. The earlier gravitational contrast thus uses a readout independently checked against the frozen prediction.

## Energy and a necessary condition for changing the sign
The endpoint energies at 590 are identical for each sign pair. The earlier reverse-minus-forward specific energies are −0.43963 (reset) and +0.61036 (inherited) in (km/s)²; the differences in work by the common time-dependent ordinary field have the opposite signs. The work differs because the two histories place mass differently in that field. The finest paired energy/work discrepancies are below 8e-9 (km/s)².

An alternative scenario would keep the **same** 586 state but change the subsequent generator. Projecting the relative evolution perpendicular to the wave derives a lower bound on the time-averaged spatially varying **total** potential contrast needed to turn the forward endpoint into its reverse: 154.48 (reset) or 91.24 (inherited) in (km/s)² over this interval. These are [projective evolution-speed](https://doi.org/10.1103/PhysRevLett.65.1697) bounds evaluated at the retained physical scales, not new fitted couplings, energy penalties, or external-only requirements. The relevant variance is in the second evolving state; use the total change including wave self-gravity. A spatially constant shift cannot perform the task. A large enough variance by itself does not establish that a proposed source produces the right current.

## Decision and continuation
- The shadow of the actual prior formation is detectable in the earlier wave source. Do not count the extra 88.97 Myr as independent stream evidence or claim Pal 5 now determines the sign.
- Next: start both forward preparations at the **archived 586 state** and test the missing time structure of the *ordinary* source, not another arbitrary wave mixture. The saved 587, 588 and 589 stellar-plus-cold-gas potentials permit an endpoint-preserving variation about the joint interpolation. Use only their departure from their own interpolated endpoints; do not replace the full all-gas source by the cold component. Compare distance to the forward/reversed targets **and actual shell currents** at 590. If this changes the decision, the all-phase intermediate source must be checked independently. This is a test of formation uncertainty upstream of the Newtonian prediction, not a search for a better-fit force law.

[Predeclared checks](PROTOCOL.md) · [derivations and units](DERIVATION.md) · closest coherent blend (not bundled here) · [gravitational source changes](evidence-001.zip) (archive member: `newton-source-contrast.csv`) · [work balance](evidence-001.zip) (archive member: `work-contrast.csv`) · [same-start necessary bound](evidence-001.zip) (archive member: `same-start-drive-bound.csv`) · numerical refinement (not bundled here). Kept native, twice and four times as many steps (70/140/280), fixed 590 inputs, 1e-9 normalization/round-trip and 0.005 relative refinement ceiling. Finite-element and angular discretization and the formation archive itself are held fixed; this is not a continuum or astrophysical error bar.

Local replay, single numerical thread: run `python -B inverse.py 1`, then `2` and `4` as the factor, followed by `python -B formation_bounds.py` and `python -B verify.py`. Conflicting results are not overwritten. No fit, external handoff, publication or change to prior source files.
