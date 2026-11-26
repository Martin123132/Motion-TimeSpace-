> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# The two prepared histories pass the switch and the joint 77-bin evolution

**No sampled time crosses the unchanged 0.5% threshold between 89.1485038031 and 89.6 conformal Mpc.** There is a small difference in the rates already at the switch; it does not grow into a constraint failure on this window. The two histories here are the momentum-evolved explicit heavy wave and the archived density-constraint particular solution whose difference drove the earlier packet. They are two gravity routes for the same prepared parent mode, not two cosmological models.

| Fine gravity clock, four subdivisions | Momentum-driven history | Density-driven history |
|---|---:|---:|
| Switch density-constraint mismatch / saved curvature | 1.76 × 10⁻⁹% | 1.76 × 10⁻⁹% |
| Switch rate mismatch from the left state / actual launch rate | about 0.05% | about 0.05% |
| Full-window RMS difference of density and momentum curvature / RMS momentum curvature | 0.00004355% | 0.00004367% |
| Accumulated discrepancy after subtracting entry offset / RMS curvature change since switch | 0.00550% | 0.00551% |
| RMS disagreement of the two curvature rates / RMS momentum rate | 0.11317% | 0.11317% |
| Largest sampled rate disagreement / RMS momentum rate | 0.20081% | 0.20094% |
| Time of largest sampled rate disagreement (conformal Mpc) | 89.5351074 | 89.5351074 |

**Where does it start?** At launch both preparations have the same nonzero curvature (fine |Φ| = 7.953 × 10⁻¹³). Their energy constraints agree with it to the precision in the table. The stored archive derivative and the momentum rate differ by 0.05061% on the fine grid. A separate calculation using the switch state, its ordinary and 77-bin rates, and the time dependence of its supplied coefficients gives about 0.053%; its two coefficient-derivative refinements differ by 0.0036 percentage points on the rate scale. This supports a small *existing slope difference*, not an initial jump in curvature or a precisely determined extra term. The largest disagreement later is near 89.5351 on both gravity clocks. It partly cancels on integration; the largest elapsed-time drift divided by elapsed time times the RMS rate is 0.1292% or less. There is no threshold-crossing time to quote for either route or either clock. These are sampled tests; they are not an analytic bound between samples.

## What was evolved

- Restored all 77 complex momentum-bin hierarchies through angular order 68 from their saved nonzero 83.2 restart, not from an empty perturbation. The spectral shape and the 77 separate microscopic sources come from the same sealed bank. The switch ordinary and angular variables for the two routes were recovered independently; no potential or source was adjusted to pass the entry check.
- At every integration substage each history recomputes its energy, longitudinal current, shear and mass trace from its own bins. Matter, the heavy and light wave perturbations, and the metric then supply the same substage's normal multipoles and lapse back to those bins. Both histories use the same background and externally supplied U, Q, Fq and microscopic forcing. None of the original 11 saved stress knots is used to drive the post-switch evolution.
- For the momentum route, the independent test is the potential inferred from total energy and momentum, Φ_E=(U−E/2−3HJ/(2k²))/B. For the density route, Φ_E drives the evolution; an auxiliary curvature independently integrates J/(2k²)−HΨ+Fq from the saved curvature without being reset. The reported check compares these two quantities, **not** an imposed algebraic identity with itself.
- Incoming-population replay on the archived driver reproduces every individual terminal bin to within 0.0000048%; the four stress moments at the original knots replay to within 0.0000013% on their channel scales. The switch stress from actual bins differs from the archived moment spline by at most 0.000041%. Both 2/4 subdivision tests and the p16/p32 gravity-clock tests pass, including the small curvature residual on its own RMS scale (largest refinement discrepancy 0.0955%). The maximum terminal-bin discrepancy against the archive in the new joint evolution is below 0.0000048%.

## What changed from the previous conclusion?

The isolated feedback packet failed when its density from an earlier ordinary driving history was inserted alongside a later incremental metric. That result stands on its own normalization. When the *two full nonzero histories* and the returning stress are evolved at the same step, the independent equations agree inside tolerance. This is not merely the effect of dividing by a large background curvature: the change since launch and the rate also pass. It does not turn the previous packet into a self-contained solution or establish accuracy on that isolated packet's extremely small scale. No visibility-peak photon result or observational fit was recalculated.

**Next:** apply this same joint-bin test to the recoupled **matched** MTS preparation. Use its own switch density, current and phase, rather than copying the explicit wave's launch; verify those physical inputs map to a well-conditioned wave perturbation at the switch. Compare its constraint and its difference from this resolved control before carrying the result to the saved photon readout.

[Protocol](PROTOCOL.md) · [Restored populations](evidence-001.zip) (archive member: `preparation-controls.csv`) · [Switch constraints](evidence-001.zip) (archive member: `switch-checks.csv`) · [Full-window and onset tests](evidence-001.zip) (archive member: `onset.csv`) · [Independent entry rate and peak timing](evidence-001.zip) (archive member: `switch-rate.csv`) · [Archive and shadow controls](evidence-001.zip) (archive member: `independent-controls.csv`) · [Refinements](evidence-001.zip) (archive member: `refinement.csv`) · [Two-history comparison](evidence-001.zip) (archive member: `paired-readout.csv`).

Reproduction in a fresh sibling directory with the same sealed parents, Python -B and one numerical thread: joint77_stage.py, joint77_prepare.py, joint77_evolve.py, joint77_score.py, switch_rate.py, then joint77_score.py --seal. All work is local; no older archive, paper or repository was changed.
