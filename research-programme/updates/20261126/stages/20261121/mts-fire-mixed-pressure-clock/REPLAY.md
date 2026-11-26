> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# Reproduce without downloading or fitting

Start in this directory with the retained Python 3.13, NumPy and SciPy; the ancestor imports also use h5py and requests. Use one numerical thread per job and no bytecode (the scripts set the library thread limits). The preceding [live-feedback checkpoint](../mts-fire-live-poisson-feedback/RESULTS.md) and the original relative paths in the private archive are prerequisites. Start with the cheap integrity check:

    python -B verify_stage.py

The eight local support/boundary packets suffice for the entire numerical stage. The four main pieces retain 2,620,700 native records; the four outer buffers retain 25,708 **additional**, non-overlapping records. Each selection reconciled internal energy on all 57,075,281 native records back to the prior energy bank. Both acquisitions together read 1,094,940,706 network bytes. The public FIRE-2 release describes the snapshot conventions in [Wetzel et al., section 4.2](https://arxiv.org/pdf/2202.06969); the exact shard URLs, server identities, hashes, conversion factors and selection counts are in the eight per-shard JSON receipts. The [published run configuration](https://users.flatironinstitute.org/~mgrudic/fire2_public_release/core/m12i_res7100/gizmo_config.h) uses meshless finite-mass hydro. The two positive continuum reconstructions in this stage are explicit alternatives, not the simulation's detailed thermodynamics. No catalogue, rotation-curve or clock data were fitted.

Optional full numerical replay, sequentially:

    python -B finite_volume.py
    python -B gas_clouds.py
    python -B cloud_volume.py 640 0 1 2 3 --all-arms
    python -B cloud_volume.py 640 1 2 3
    python -B cloud_volume.py 960 0
    python -B trace_resolution.py
    python -B scalar_pressure_test.py
    python -B normal_energy.py --cells
    python -B normal_energy.py 1200 0
    python -B normal_energy.py 2000 1
    python -B verify_stage.py

The script excludes the two clock radii from unsplit bulk quadrature, checks signs against analytic controls and verifies seed-matched paired subtractions. Four angular draws are not a statistical sample of Milky Ways. For internal-energy gravity the two refinements change both numerical interpolation and draw; the difference is not an isolated order-of-convergence estimate. Machine-precision file replay assumes the same numerical environment. Default verification compares all files and does not regenerate expensive calculations or overwrite a mismatch. The original per-shard acquisition script is retained for provenance only; the launcher requires an explicit UTC deadline on a fresh acquisition. No re-fetch is part of validation.
