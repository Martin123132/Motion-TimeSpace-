# Read-only verification and numerical replay

Default from this directory: `python -B verify.py`. This checks the full previous 232-file stage, frozen designs, signed results and acknowledged raw failures, finite apertures, numeric packets and the current stage manifest. The first seal was made with `python -B verify.py --seal`. Existing scientific outputs are compared, never overwritten, by the replay writers. Use Python 3.13 with NumPy, SciPy and SymPy on the retained local environment, one numerical thread; do not use optimized Python (-O disables assertions). The frozen forecast cannot be regenerated as a new blind test on already observed data.

To repeat the full prior evolution sequentially, run the following from this directory with `python -B` before each script name:

1. `scope.py`, `width_forecast.py`, `null_forecast.py`.
2. `photons.py coarse fine wide narrow critical`, then `spacetime.py coarse fine wide narrow critical`.
3. Replay old raw tables with `python -B -c "import measure; measure.algebra(); measure.sources(); measure.metrics()"`. Running the raw `measure.py` acceptance is **expected to fail** for the preserved interpolation result. The historical dust-index table is kept for audit, not accepted as the dust solution.
4. `local_jets.py coarse fine wide narrow critical`, `signed_tests.py`, `wilson.py`, `exact_vertices.py`, `critical_check.py`.
5. `action_forecast.py`, `action_metric.py coarse fine`, `finite_detector.py`, `finite_null.py`, `transfer.py`, `verify.py`.

The two independent numerical routes are described in [the original design](DESIGN.md), [action matching](ACTION-MATCHING.md), and [finite-aperture prescription](FINITE-NULL-DESIGN.md). The latest stress and LMC results in the parent directory are separate, unchanged inputs or comparisons. No network service or background worker is required.
