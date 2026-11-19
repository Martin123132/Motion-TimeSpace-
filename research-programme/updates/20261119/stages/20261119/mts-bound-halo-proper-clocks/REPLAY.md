# Private replay

Use the retained Python 3.13, NumPy and SciPy with bytecode disabled; one numerical thread per job. The neighboring predecessor directories and the retained EPTA calendar are dependencies. Preserve all prior checkpoints; no observational downloads, Git operations, other chats or long-lived services required.

**Verify in place:** run `python -B verify_halo.py`. It checks the phase-specific freezes, parent and earlier seals, inherited files, every finite output against its receipt and the stationary solves, rebuilds the numerical tables from saved arrays including original misses, checks local input code and hashes the entire stage. No recalculation of the two time-dependent histories is needed for ordinary verification. The hash manifest is a local integrity check, not external timestamp attestation.

**Full reproduction:** in a fresh copy beside the unchanged predecessor stages, start with just stage code and Markdown, not the outputs. Set OPENBLAS_NUM_THREADS, OMP_NUM_THREADS, MKL_NUM_THREADS and NUMEXPR_NUM_THREADS to 1 before the interpreter. In order:
1. `python -B halo_mean.py create`, then `python -B bound_cycle.py init`.
2. For each PHASE in turn, kinetic: `python -B bound_cycle.py forecast PHASE 128 256`, then `python -B bound_cycle.py freeze PHASE`, only then `python -B bound_cycle.py finite PHASE 128 256`.
3. `python -B read_run.py create`. Run `python -B radial_readout.py PHASE` for each phase; each must match the original sampled mass at every output time before a corrected readout is retained. Then `python -B radial_readout.py create`.
4. Separately run `python -B SCRIPT create` for milkyway.py, free_ray.py, occupation_envelope.py, outer_speed.py and quarter_prediction.py. These are appendices and a prospective linear prediction, not inputs to the original time-dependent freeze.
5. `python -B verify_halo.py seal` and `python -B verify_halo.py`. For independent reproductions compare numerical arrays, not just container bytes across software versions. CSV units are given in column labels or in DERIVATION.md. External density/mass inputs are transcribed in milkyway.py; the measured outer speed and error in outer_speed.py come from Feng et al. Table 1, not from the NFW fit.

Radial archive order: delta mass, total flux times r², pressure, displacement, velocity, spatial mass constraint. Clock diagnostics in read_run.py: one-way and echo frequency, then one-way and echo delay. Compare like with like: shifted launch reference for held-clock waveforms; common proper reception dates for calendar checks; free-endpoint weak-field ray separately. The calendar has 5,011 retained times of arrival on 2,055 distinct observing days spanning 8,935 days; no timing residual file or observed pulsed amplitude was used.
