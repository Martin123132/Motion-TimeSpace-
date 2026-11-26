# Private replay and sources

Use the same installed Python 3.13, NumPy and SciPy, one worker, with bytecode disabled. From this directory run the scripts in this order with python -B:

1. prediction.py — fixed 104-site geometry, Gauss resolution, symmetry, ordinary controls and frozen prediction digests. Sources include the previously sealed launch.npz, occupation, finite-volume positive source and stellar field code; no survey results are read here apart from the already exposed saved solar comparison.
2. gd1.py and crossing.py — direct GD-1 evaluation on the same fields and the angular window around the foreground crossing. [Stream data, v1, equations 2–4](https://arxiv.org/html/2504.07187v1); [stellar and conventional controls, table 1 and equations 7–9](https://arxiv.org/html/1611.07979).
3. native_map.py — original finite-element reconstruction, matching both saved 590 states; writes the map and native units, not a new long evolution. formation_forces.py and origin_trace.py map the already archived waves; provenance is pinned to the November 20 and 22 manifests.
4. virial.py — weak field/analytic Gaussian, global self-energy, wall term, true shell current acceleration and independent fixed-grid check. state_angle.py and native_bound.py — Rayleigh bounds in the continuous norm and the actual native norm.
5. drive_floor.py and action_replay.py — source constraints and actual prior measured effective-action integrals. verify_result.py checks files and numerical controls; with an existing seal it verifies exact contents. Use --seal only when first sealing a complete equivalent copy.

No code here fits GD-1. Source paths are relative to this stage's parent and checked before use. Writers validate existing output bytes rather than overwrite. Earlier artifacts are read-only; no network required for replay. Source-search leads such as the [RR Lyrae Jeans analysis](https://doi.org/10.1093/mnras/stz572) have not supplied additional data points or independent likelihood terms.
