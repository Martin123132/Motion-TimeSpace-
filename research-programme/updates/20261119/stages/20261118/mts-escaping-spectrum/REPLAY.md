# Local replay and audit

Run verify.py with the retained local Python 3.13, -B, one BLAS/OMP thread. It checks the sealed upstream files, archived gates, reprojects the independent time-domain comparison, and reconstructs the receipt rather than just trusting a green flag. No internet, new observations or live worker required. The reference is the sibling mts-driven-current-20261118. Code uses NumPy, SciPy and psutil. All Python processes in this stage are short-lived. No change to the stored geometry or to the matter action.

For a full re-creation, copy this stage's Python and Markdown sources to a fresh sibling directory while preserving the parent's relative location. Run, in order:
1. outgoing.py checks, outgoing.py fine, outgoing.py checkgrid (three serial invocations). Each creates a new packet exclusively. The fine and coarse grids use 1536 and 768 frequency nodes; independent soft and exterior-start probes are separate.
2. diagnostics.py, soft_flux.py, finite_transfer.py, radiative_metric.py, signed_readout.py (five serial invocations).
3. verify.py --seal once, then verify.py separately. Do not rerun --seal into an existing receipt. Copy no data into an existing stage.
4. Compare numerical outputs on the stated tolerances across environments. There is no requirement for bitwise portability across different math libraries.

spectrum.csv is the angular-frequency quadrature with weights, complex outgoing news and the ideal flat comparator. retarded_signal.csv is the null-time waveform and cumulative energy in units with the angular factor divided out. escape_energy.csv compares spectral, time-domain and source energies. detector_comparisons.csv contains each frozen near-detector test. The full-field independent comparisons are stored in closeout.json. finite_transport.csv and transfer_mesh.csv test the time-dependent arms; finite_traces.csv retains launch, retarded arrivals, receiver and no-barrier control. soft_flux_repair.csv keeps both evaluations including failed raw soft-current checks. signed_tail.csv is the distinct finite-time magnetic-moment diagnostic. bondi_loss.csv and null_metric_memory.csv restore the actual solid-angle normalization. See EQUATIONS.md and GRAVITY-AT-INFINITY.md for derivations and source attribution.

