# Local replay

All inputs are existing MTS preparations. Run in this directory with the retained 64-bit Python 3.13 environment (NumPy, SciPy and the original upstream dependencies). Do not move or edit the sealed input stages. Each script is single-worker, writes only locally, and checks existing result bytes instead of replacing them. No downloads, service or GitHub action.

- `python -B clock_tide.py heavy 5 normal 8 --shells`: native-matched interval and exterior terms for both signs. Also run `cold 5 normal 4` for the all-cold control. The full set is both models × grids 4,5 × histories archive,normal,longitudinal with 4 steps; heavy grid 5 all histories with 8 steps; heavy grid 5 archive with 2 steps. Add `--shells` for heavy 4 normal 4 and heavy 5 normal 8 only.
- `python -B launch_flux.py 5` and repeat with 4: reconstruct both launch currents and all sources out to 120 Mpc.
- `python -B analytic.py` and `python -B subsidiary.py check`: analytic Newtonian and ADM controls. `python -B compare.py`: matched branch and precision tables.
- `python -B constraint_rate.py 80 192 1` and repeat with final argument 0: separate local scalar-curvature rate versus the previously archived GR readouts. `python -B subsidiary.py 80 192 1` and repeat with 120 instead of 80: momentum-divergence prediction.
- `python -B diagnostics.py`, then `python -B verify.py` to verify the complete saved set, previously archived checksums and explicitly retained failures. These readouts concern the conditional signed-cloud calculation, not the separate LMC band test.

[Derivation](DERIVATION.md) · [results](RESULTS.md). The ADM starting convention follows [Gourgoulhon's 3+1 lecture notes](https://arxiv.org/abs/gr-qc/0703035); the modified constraint transport, numerical tests and comparisons in this directory are specific to this study.
