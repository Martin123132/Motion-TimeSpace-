# Replay

Use the existing Python 3.13 environment with NumPy, SciPy, SymPy and psutil; run with -B and one numerical thread. No downloads or changes to the saved scattering, radiation or matter banks. All Python workers are short-lived, serial within their groups, below-normal priority and pinned to one available core by the inherited guard. Replaying verify.py is read-only once sealed.

For a fresh calculation use a fresh sibling directory with these Python/Markdown sources, so that no numerical packets need to be overwritten. Sequence:
1. exterior.py, then local_curvature.py and identities.py.
2. matter_tangent.py group, matter_tangent.py repair, then matter_tangent.py higher. Each command calculates both original grids, the extremal control and the three matched eta=0.8 configurations. The variations use an infinitesimal imaginary coefficient for the coupled differential, not an imaginary physical spin. The real parts are compared to the existing independently saved final spherical state. The exact static velocity null is checked in absolute machine-scale units; its previously stored value is at roundoff.
3. matter_tangent.py 1920 0 0 0 --higher for the neutral no-radiation control.
4. rulers.py, rulers.py higher, trace_channels.py, proper_scalar.py, near_far.py, exact_exterior.py.
5. verify.py --seal once in a fresh stage, then verify.py again in a new process.

Reading order: RESULTS.md, CONSTRAINTS.md, then the two prospective prediction notes. static_checks.csv and local_curvature.csv include the raw curvature miss and its local repair. mass_audit.csv tracks the first two source schemes; higher_mass_audit.csv, higher_paired_controls.csv and higher_ruler_mesh.csv are the accepted mass/clock comparisons. All proper-time samples are in higher_ruler_series.csv. proper_scalar.csv retains the failed mixed-interpolator subtraction as well as the independent proper-clock scalar test (combine equal-frequency/clock terms before interpolating). The real initial data for every arm and its frozen first-order dipole are inherited, not fitted. Full disk, finite-radius quadrupole and microscopic charge are not inferred from these fixtures.

In all coupled NPZ files the delta/base labels are embedded, including the scalar, its momentum and the metric factor. delta_final row 2 is δD in the direct-density scheme, and δN/r³ in the conserved and higher schemes. The saved scalar perturbation and its clock correction can be reused directly. The initial area-sphere mass differs from initial ADM on a scalar background; the exterior mass arrays report changes about the correct initial local value. The geometric 4D control reads the previously specified Kerr–Newman metric independently, not just the proposed effective stress.

Do not interpret published error ratios below a raw finite-difference or interpolation floor as observational precision. A near-zero control is labelled separately; a failed whole-interior readout is not replaced by a renormalized source mass.

