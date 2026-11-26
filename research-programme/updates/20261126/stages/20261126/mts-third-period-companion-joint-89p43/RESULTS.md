> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# The complementary stress passes the third-period and three-period gravity-rate tests

The third oscillation ran from 89.3345657494 to 89.4274304581 conformal Mpc. Both corrected routes passed the unchanged 0.5% rate tolerance on both gravity clocks and both time subdivisions. The fine momentum-route error rose from 0.198416% in period two to 0.206564% in period three. The fine density-route error rose from 0.198334% to 0.206526%. The largest sampled third-period error on either corrected route, measured against its period RMS momentum rate, was 0.365568%. No curvature reset or fitted adjustment was made.

| Grid / gravity route | Third: no correction | Third: with correction | Three periods: no correction | Three periods: with correction |
|---|---:|---:|---:|---:|
| Coarse / momentum | 0.763959% | 0.206566% | 0.762404% | 0.199630% |
| Coarse / density | 0.200204% | 0.206528% | 0.191685% | 0.199592% |
| Fine / momentum | 0.763955% | 0.206564% | 0.762399% | 0.199628% |
| Fine / density | 0.200202% | 0.206526% | 0.191684% | 0.199589% |

Four subdivisions shown; all settings and precision are in [results.json](evidence-001.zip) (archive member: `results.json`). The disabled copies have the original wave and matter stresses but not the complementary stress in their gravity. The gain is specific to the momentum route; the already passing density route is slightly less accurate with the correction. This is a test of the saved prepared perturbation, not an observational fit.

## Restart, delay and independent checks

- Before advancing we verified the period-two packet hashes. Each route restarted from its own exact endpoint: matter, explicit wave, integrated curvature, all 77×69 bin states, spectral shape, mean and complementary density. Neither energy-derived curvature nor integrated curvature showed a jump at the join.
- The leaving current was evaluated at θ−π in the same trajectory’s phase-labelled instantaneous history. On the fine clock, only the first 2.99×10⁻⁹ conformal Mpc used the tail of period one. The integral was split at the actual phase crossing; the rest used period two. No history was extrapolated or periodically copied. The original interior output times were preserved, with the saved third phase crossing added as an endpoint.
- Only ρ(mean − instantaneous current) and complementary density were added to the resolved wave in the enabled routes. Direct phase integration of the mean, pressure and density balance checks, total current accounting, trajectory ownership, momentum integration and replays with the complementary stress disabled give numerical errors below 0.00000026%. The disabled control at the final off-grid crossing was compared with an interpolation of the original uncorrected trajectory inside its saved domain. The coarse/fine corrected rate-residual histories differed by less than 0.000223% of the fine residual.
- Cumulative rates use the sum of time-integrated squared errors divided by the sum of time-integrated squared reference rates, followed by the square root. We differentiated only within smooth source intervals and checked the two-period inputs against their saved score. On the fine grid the three-period curvature drift since the original launch is 0.014173% of the actual curvature motion on the momentum route and 0.014684% on the density route.

**Next:** continue from the sealed third endpoint through the fourth complete oscillation. Carry each trajectory's mean, complementary density and its own recorded current; use the tail of period two where the delayed phase requires it. The partial cycle ending at 89.6 remains separate. No fourth period, photon propagation or publication occurred here.

[Protocol](PROTOCOL.md) · [Scores, controls and refinement](evidence-001.zip) (archive member: `results.json`) · [Period-two restart](../mts-second-period-companion-joint-89p33/RESULTS.md). The four third-period packets contain complete endpoint states, their entering states and phase-labelled histories. For an offline replay, run third.py init, third.py run, score_third.py and verify_third.py sequentially in a fresh sibling stage with the pinned parents, single-threaded Python 3.13 and -B. The stage manifest is seal.json.
