# Energy-unit adapter

Review before handing the helper to a physical solver found an interface limitation:
the original normalized implementation used an absolute 1e-12 spectral guard.
Its completed controls use order-one energies, so those results stand, but
applying that guard unchanged to SI energies would incorrectly reject a
well-separated tiny-energy Hamiltonian.

energy_units.py explicitly centers on the declared escape threshold and scales
the matrix by its maximum absolute entry before eigendecomposition. It scales
H_dot and hbar consistently, and returns the gap in the caller's energy units.
The projector and its rate do not depend on this positive energy rescaling.
The numerical threshold guard is now relative to the centered operator. This
is not a new physical gap criterion or a fitted energy floor. A uniform
threshold shift changes neither the projector nor its derivative when the
escape reference is shifted with it.

Preserve population_transport.py, its original receipts and result.json.
The supported dimensional interface is energy_units.py; it reuses the
verified normalized kernel. The additional validation reruns the same checks,
plus energy-unit rescalings1e-80,1,1e80, a common potential/escape-level offset,
and a negative control confirming the original raw tiny-energy call is refused.
No physical coefficient, occupation, gate or earlier result is modified.
