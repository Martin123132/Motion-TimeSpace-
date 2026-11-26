> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# Private reproducibility and limits

Use retained Python 3.13 and the NumPy/SciPy and inherited FIRE dependencies already used by the preceding checkpoint. All sampling is local. Each numerical worker is limited to one library thread. From this directory, verify the checked-in packets without downloading or running the mechanical evolution:

    python -B verify_material.py

Full replay if needed (run sequentially; j denotes 0 and then 1):

    python -B gas_inputs.py
    python -B material_evolution.py j base
    python -B material_evolution.py j controls
    python -B material_evolution.py j fine
    python -B resolve_faces.py j 4 8
    python -B early_time.py j
    python -B interface_euler.py
    python -B interface_gravity.py
    python -B coupling_reciprocity.py
    python -B numerical_checks.py
    python -B verify_material.py

Replace j with the actual integer. Primary state packets contain both reset and coupled displacements, both material choices, original triangles, mass and tag. Source files use the previously hash-verified launch selection and its full compact gas support radius, no network queries. The public simulation source and conditional pressure assumptions are documented in the predecessor replay (not bundled here). Two 57×57 sample grids per probe are stored as one packet with both radial reconstructions of the 3D gas kernel. Per-triangle cubature uses the interpolated axisymmetric density, not velocities or data inferred from the clock. Axisymmetry is an imposed reduction, not the original 3D hydrodynamics.

Every mechanical endpoint is computed independently; padding augments the material outside the fixed core. The pressure work uses the variational nodal masses and pressure-force gradient; the clock integrates the uniform-per-reference-volume *material inside* each triangle rather than putting its mass at the corners. This makes the isolated clock an observable of the chosen model, not the derivative conjugate to the nodal gravity force. The paired pressure alternative changes both the gas dynamics and where the original source is sampled; its fourth-order coefficient is thus not equal to the pressure-only coefficient of the earlier work.

The cold, matched starts, adiabatic model, fixed outer displacements and frozen wave potentials isolate the pressure transaction. No shock capturing is claimed for these 2D energy-variational triangles. The independent one-dimensional front control uses an entropy shock/rarefaction solution and, separately, a first-order conservative local Lax–Friedrichs evolution. The planar slab field is calculated analytically with open conditions on the *field difference*. It is not substituted into the three-dimensional wave evolution. In the aperture-wide source alternative, the external host mass and the wave's previous formation are not changed by the new static calculation. Do not promote different host profiles into observations or fit a new gravitational constant to their difference.
