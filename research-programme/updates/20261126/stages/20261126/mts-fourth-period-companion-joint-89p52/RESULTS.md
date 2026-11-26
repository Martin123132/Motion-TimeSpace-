> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# Fourth oscillation: the rate error falls on both gravity routes

Both gravity routes pass the unchanged 0.5% rate test on both grids during the fourth oscillation and over all four complete oscillations. The fine momentum-route error fell from 0.206564% in period three to 0.195818% in period four. The fine density-route error fell from 0.206526% to 0.195810%. Thus the rise in error seen through period three did not continue in period four. The maximum sampled fourth-period corrected error across both clocks and subdivisions was 0.312857% of the corresponding RMS momentum rate or less.

| Gravity clock / route | Period four, no correction | Period four, corrected | Four periods, no correction | Four periods, corrected |
|---|---:|---:|---:|---:|
| Coarse / momentum | 0.757378% | 0.195820% | 0.761156% | 0.198689% |
| Coarse / density | 0.185172% | 0.195812% | 0.190085% | 0.198657% |
| Fine / momentum | 0.757374% | 0.195818% | 0.761151% | 0.198687% |
| Fine / density | 0.185170% | 0.195810% | 0.190083% | 0.198655% |

Four subdivisions shown; both two-subdivision runs give the same verdict. “No correction” disables only the complementary contribution to gravity; the underlying matter and wave still evolve. The correction again brings the failing momentum route below threshold, at a small cost on the already passing density route. These are internal consistency results for the retained prepared mode.

## Restart and checks

We evolved the interval 89.4274304581–89.5201848111 conformal Mpc. For each route the entering matter/field state, integrated curvature, 77×69 bin states, spectral shape, running mean and complementary density exactly matched its sealed third-period endpoint. The integrated and algebraic curvatures showed no jump at this join. Neither the curvature nor the averaging memory was reset. There was no refit, change to the source bank, or tolerance adjustment.

The running mean used instantaneous wave current from that trajectory at its own delayed phase. On the fine grid only the first 2.46×10⁻⁹ conformal Mpc of period four drew on the tail of period two. We split there rather than rounding phase or reusing another route’s history. The remaining delayed values came from that route’s third period. Only the complementary density and the difference between mean and instantaneous current gravitated in addition to the resolved wave; its instantaneous current was not added twice.

The rate score is the time-integrated complex RMS difference between the energy-derived curvature rate and the momentum-equation rate, normalized to the RMS momentum rate on the same trajectory. The cumulative score combines squared-error and squared-rate integrals across periods before normalization; it is not an average of percentages. The first three periods reproduce their previously saved cumulative score. On the fine grid, the four-period curvature drift since launch was 0.012822% of actual curvature motion on the momentum route and 0.013313% on the density route.

Controls checked history ownership at the delayed join, independent integration of the mean, pressure and density balance, single current addition, independent momentum integration, and disabled-control reproduction of the original solver. The original solver was interpolated inside its own domain at the two off-grid endpoints. The largest control discrepancy was less than 0.00000043%. At four subdivisions, the corrected period-four rate-residual histories differed by less than 0.000240% of the fine residual between gravity clocks.

**Restart:** the four fourth-period packets hold the final states, mean, complementary density and route-specific current histories. Next advance from this endpoint to **89.6**, using period four for each delayed current as it enters that history, and the tail of period three until then. Score the partial interval on its own before combining it with the four complete periods. Only that last test makes the corrected result directly comparable with the original full-window rate discrepancy. No partial-cycle or photon calculation was run here.

[All scores and controls](evidence-001.zip) (archive member: `results.json`) · [Frozen protocol](PROTOCOL.md) · [Period-three restart](../mts-third-period-companion-joint-89p43/RESULTS.md). Reproduction in a fresh sibling stage with the same pinned parents: run fourth.py init, fourth.py run, score_fourth.py, then verify_fourth.py, with -B and one numerical thread. Input and output checksums are recorded in seal.json.
