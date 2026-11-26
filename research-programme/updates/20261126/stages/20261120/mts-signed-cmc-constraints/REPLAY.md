> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# Reproduce the conditional constraints

Use the retained 64-bit Python with NumPy, SciPy, SymPy, and the earlier formation code and saved native outputs. No compilation, downloads, GPU or service. Use one process at a time; scripts set numerical libraries to one thread. Nothing here alters the original histories. From this folder:

1. For each pair MODEL ∈ {heavy,cold}, RATE ∈ {4,5}, run `python -B run_slices.py MODEL RATE`, then `python -B differential.py MODEL RATE` and `python -B proper_probe.py MODEL RATE`. The rate is the archived number of elements per comoving Mpc; it does not select a different physical model. Each file is created once; repeats compare results without overwriting.
2. `python -B controls.py` tests a manufactured nonlinear CMC dust solution whose energy/current and analytic tide are fixed independently of the grid, and the compact free tensor's divergence. `python -B quadratures.py` compares the stress lift against a discrete real-carrier phase integral. `python -B compare.py` forms all same-background and same-ruler differences.
3. `python -B verify.py` checks source hashes, the matched cold null, GR linear recovery, constraint residuals, independently assembled differences, signed proper-distance comparisons, known resolution failures, and the stage inventory against the seal. The native input spectra, domain, pressure on/off switch and accepted/rejected parent artifacts are identified by the parent seal (not bundled here). The real nonlinear source fields come from the transmitted-tide seal (not bundled here). Each is checked before use. No public repository action.

The reference NPZ packets store spherical and quadrupolar metric, vector potential, and independent shear components, on both archived meshes. CSVs retain the alternate free data, failed relative checks and proper-distance diagnostics. Multiplying a comoving curvature in Mpc⁻² by (c/(a Mpc))² gives s⁻². No local observational score or new fit is part of this checkpoint.
