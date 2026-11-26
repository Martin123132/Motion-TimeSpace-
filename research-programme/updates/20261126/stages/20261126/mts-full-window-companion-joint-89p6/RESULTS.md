> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# The complementary stress clears the original full-window gravity-rate threshold

The final partial oscillation ran from 89.5201848111 to **89.6 conformal Mpc**, covering 0.861448 of a stress period. The original window starting at 89.1485038031 is now covered continuously. No cycle was extrapolated to an integer period, no curvature or memory was reset, and no parameters were fitted.

**Direct result:** on the original fine clock the full-window momentum-route rate error falls from **0.769540% to 0.198912%** (74.15% smaller). The density-route error rises from **0.190707% to 0.198893%**. The corrected routes pass the unchanged 0.5% RMS criterion both on the final partial interval alone and on the complete window. Both coarse settings give the same verdict. This resolves the earlier failed momentum-rate check for this prepared mode and supplied source bank; it is not a photon or observational score.

| Grid / gravity route | Partial: correction off | Partial: correction on | Full: original archive | Full: correction on, original ticks |
|---|---:|---:|---:|---:|
| Coarse / momentum | 0.808371% | 0.199966% | 0.769544% | 0.198914% |
| Coarse / density | 0.193658% | 0.200002% | 0.190709% | 0.198895% |
| Fine / momentum | 0.808367% | 0.199963% | 0.769540% | 0.198912% |
| Fine / density | 0.193656% | 0.200000% | 0.190707% | 0.198893% |

Values shown for four subdivisions; [full-window comparisons for all settings](evidence-001.zip) (archive member: `full-comparison.json`) and [partial scores, quadratures and controls](evidence-001.zip) (archive member: `results.json`) include two subdivisions as well. “Off” disables only the complementary contribution; the explicit wave, other matter and gravity are present. No corrected saved sample exceeded 0.5% of its route's RMS momentum rate: the largest partial-cycle peak over all settings was 0.355938%, and the largest full-window peak on the original grid was 0.365639%. These are sampled peaks, not continuum bounds.

## Why the comparison is like for like

1. Each of the four trajectories (corrected and disabled, momentum- and density-driven) restarted with the exact matched fourth endpoint on each grid and subdivision, including field/matter state, integrated curvature, 77×69 bins, spectral shape, mean and complementary density. On the fine grid only the first 3.01×10⁻⁹ conformal Mpc of the partial interval drew its delayed current from the end of period three; after that the delayed current came from the same trajectory’s period-four history. The stress equations, treatment of shear and microscopic forcing were unchanged. Only the complement was added, not a second copy of the live heavy current.
2. We froze the partial trajectories before scoring. The first full-window calculation adds the time-integrated squared complex rate residual and reference rate from the actual partial interval to the four saved complete periods. Percentages are not averaged. We also verified the four-period cumulative inputs against the preceding sealed results.
3. For the direct comparison, we selected the original gravity time samples exactly, dropping only the two extra off-grid cycle endpoints. We preserved separate left/right readouts at the original two source corners and differentiated within each of the original three smooth intervals. The archived trajectories reproduce the original signed-off rate table to better than 10⁻¹¹ percentage points. The new disabled replays match those original RMS rates to within 1.7×10⁻⁹ percentage points; the corrected segmented and original-grid scoring conventions differ by at most 8.3×10⁻⁸ percentage points. This makes the improvement distinguishable from a change in sampling or normalization.
4. The pressure/density balance, current ownership, direct phase integral, single inclusion of the heavy current and independent momentum integration were checked. The largest partial-run numerical control was below 0.0000012%. Fine full-window curvature drift since launch was 0.012116% of actual curvature motion on the corrected momentum trajectory and 0.012603% on the corrected density trajectory. The density route's slight loss of rate accuracy is retained in the result.

## Saved handoff

The four partial packets contain final physical states and branch-owned phase/current histories. The four full-grid packets include potential, lapse, momentum rate, other named readouts, route labels, original clocks and both sides of each source corner. They are readouts for subsequent comparisons, not a replacement matter restart or a changed production bank.

**Next test:** use these saved metric histories with the already fixed photon transfer and original photon baselines. Freeze the corrected photon energy/current predictions before comparing them to the previous readout, keeping the original photon-specific tolerances and normalization separate from the 0.5% gravity-rate criterion. No new photon projection, fit or publication was done here.

[Protocol](PROTOCOL.md) · [Exact comparison](evidence-001.zip) (archive member: `full-comparison.json`) · [Restart from the fourth oscillation](../mts-fourth-period-companion-joint-89p52/RESULTS.md) · [Original failed rate test](../mts-matched-joint-77-switch-89p6/RESULTS.md). To replay in a fresh sibling stage with the pinned parents: run partial.py init, partial.py run, score_partial.py, compare_full.py, then verify_full.py with Python 3.13, -B and one numerical thread. Inputs and outputs are covered by seal.json.
