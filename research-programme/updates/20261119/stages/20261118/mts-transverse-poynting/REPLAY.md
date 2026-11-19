# Private local replay

Read-only verification from this folder: `python -B verify.py`, using the retained Windows Python 3.13 with NumPy, SciPy, SymPy and psutil. It checks previous seals/inputs, reconstructs results from the saved packets, and evaluates the action, stationary rotating control and energy identities independently. It does not start a new evolution. Distinguish algebra, evolution tests, numerical resolution, and the supplied physical assumptions in the other notes.

For a new replay, use an empty sibling directory with just this stage's Python and Markdown files, keeping the signed parent tree intact. Use the same interpreter, one numerical worker, exclusively created result files. Run in order:
1. background.py — extracts exterior radial constraints and their time derivatives. Six final states can be compared bitwise to an existing charged-stage archive. The two neutral full-strength histories did not have matching archives in that parent stage; they use the same original preparation, labelled as new runs.
2. pulse.py and measure.py — baseline, retained scalar, static analytic control, fixed-metric versus coupled dipoles, clock and energy comparisons.
3. rotation.py and crosschecks.py — distinct staggered evolution with explicit angular momentum, neutral and reversed-charge controls, and independent reading of the receiver clocks.
4. mixed_precision.py — replay only the two charged amplitudes on each mesh, assert equality of all final states, and audit the mixed work using both quadrature rules.
5. field_calibration.py — two-sphere relation from field and earlier Gauss-charge measurements. After copying the original closeout only into a byte-identical replay directory, verify.py checks it. A library change may affect file bytes; compare science scores separately; do not override the originals.

All reported time and length numbers share the parent pole units. In all flux and energy series the common factor 2/3 and the infinitesimal pulse amplitude squared have been divided out. The paired small-scalar rows carry an additional 1/λ²; rotational differences carry 1/(4Q²) and the mixed work carries both. Reported arrival shifts in arrivals.csv under proper_arrival_shift are NOT divided by λ². Local radiation and constrained metric rotation are different observables. There are no telescope data, fitted parameters, remote jobs, or ongoing workers for this stage.

