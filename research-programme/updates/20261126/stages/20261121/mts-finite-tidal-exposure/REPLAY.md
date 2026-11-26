# Verification

Use the retained Python 3.13 interpreter with NumPy, SciPy and SymPy, one numerical thread. Run from this folder with `python -B`; assertions must be enabled. No external data or service is required for the calculations. The link to the two source papers in OPTICAL-MATCH.md is for reviewing the normalization conventions.

- Quick check: `python -B verify.py`. The manifest pins the previous 114-file stage, inputs, forecasts and raw signed readings. Existing tables and JSON are compared byte-for-byte, not overwritten.
- Full sequence: `forecast.py`; `retarded.py 16 6`, `retarded.py 24 6`, `retarded.py 24 10`, `retarded.py 32 10`; `design_aperture.py`, `timing_forecast.py`; `geometry_check.py 24 8`, `geometry_check.py 32 10`; `assessment.py`, `optics.py`, then `verify.py`.
- Historical order matters: geometry adjustments were derived **after** the fixed-aperture readings, but before testing those new sizes and centres; timing forecasts preceded the perturbed-duration tests. A repeat is a reproducibility test, not a new prospective test. The optical comparison uses previously known papers, not blinded observations.
- The initial `verify.py --seal` creates the manifest once. All subsequent verifications check it. Existing stages, the LMC work and the public repository were not altered.
