> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# Private offline replay

Use the retained Python with NumPy and SciPy; run from this folder with bytecode disabled (Python -B). The launch code checks pinned upstream artifact hashes and stop flags, and numerical libraries use one thread. Writers validate existing results byte for byte; work in a private copy if changing an algorithm rather than overwriting evidence. No web downloads or catalogue fits are required.

1. Run freeze.py, geometry_terms.py and budget.py. These recover the original launch response, source split and joint sensitivity. The launch prediction's digest is fixed in EVOLUTION.md and assess.py.
2. For the native finite-volume solver run evolve.py with arguments LEVEL DT STEPS MODELS STATES. For "both all" use (2,0.002,4), (2,0.001,8), (2,0.0005,16), (3,0.001,8), (2,0.000064,2), (2,0.000032,4), (3,0.000032,4). The two single controls are (1,0.002,4,Pouliasis_I,reset_forward) and (2,0.000032,4,equal,reset_forward). Use the default retained constants; times are Myr.
3. Run stress.py, gaussian.py, interfaces.py, dual_mesh.py, weak_flux.py, angular_control.py, weak_commutator.py and initial_current.py. These include expected failures of the old mesh, two exact free packets, the independent first-derivative commutator and the signed current forecast.
4. Run smooth_grid.py with no arguments for static controls. For finite histories use smooth_grid.py with (2,0.001,8,both,all), (3,0.001,8,both,all), (3,0.0005,16,both,all), (4,0.001,8,Pouliasis_II,all). Level 4 is the additional full spatial refinement of the smaller differential signal; level 3 with halved time step supplies the common fine tabulation. The time and space checks are at fixed space and time respectively, not a simultaneous retuning.
5. Run assess.py, current_budget.py, observable_budget.py, ordinary_degeneracy.py and angular_discriminator.py. Verify with verify_stage.py. The existing seal is checked rather than replaced. The local resume index is outside the seal. For a newly produced equivalent copy, verify_stage.py --seal records the full set of local artifacts after the checks.

Read [results](RESULTS.md), [weak-stress derivation](WEAK-STRESS.md), [observational degeneracy proof](IDENTIFIABILITY.md) and finite verdicts (not bundled here). Reported optimal discrepancy is a coordinate-wise feasibility scale, not a Gaussian significance. No jobs need to persist for replay.
