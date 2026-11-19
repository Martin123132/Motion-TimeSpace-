# Local replay and source integrity

Run with the retained Python 3.13 and -B, from this directory. Numpy and SciPy plus the historical, sealed compact-lens dependency chain are required. No event photometry is needed. The retained EROS static-magnitude catalog is real stellar photometry, not simulated counts.

First acquisition only: fetch_inputs.py pins the arXiv source tarball and reads only named TeX/EPS members without extracting paths or executing paper code. fetch_catalog.py downloads and hashes the II/390 archive ReadMe, catlist and compressed image list (62.27 MB for the image list). pilot.py obtains one bounded public position query only when its retained catalog extract is missing. Compare all locally recovered hashes against seal.json; all materials remain private and carry their original attribution. The dated VizieR response header is not evidence of reprojection; store distinct source records and query parameters instead. No overwrite on replay.

Offline, sequentially:
- python -B register_points.py
- python -B seasons.py
- python -B pilot.py
- python -B sky_bounds.py
- python -B pilot_depth.py 8, then python -B pilot_depth.py 14
- python -B distance_witness.py 8, then python -B distance_witness.py 14
- python -B verify_stage.py seal

These steps were replayed against the saved bytes. The comparison of the two numerical orders has maximum relative change 1.36e−7 for the pilot outputs and 2.20e−8 for the exact-moment witnesses. Signs of all three witness differences reverse; both assignments use exactly the same per-cell multiset. Historical compact-lens files are read-only and rechecked against their 48-file seal. No persistent process or automatic acquisition. Summary: verification.json. The active resume note is outside this stage's seal; append future results elsewhere.
