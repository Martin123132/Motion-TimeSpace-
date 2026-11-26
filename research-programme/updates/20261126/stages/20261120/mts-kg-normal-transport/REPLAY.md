> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# Replay this local calculation

Dependencies used: 64-bit Python 3.13.13, NumPy 2.4.6, SciPy 1.17.1, mpmath 1.3.0, the existing serial native cosmology library and the saved host, native-spectrum and metric archives. Run one worker at a time, with bytecode writing disabled. No installation, GPU, download, fitting or change to a parent release is required. The native observer configuration is the one imported by [native_trace.py](evidence-001.zip) (archive member: `native_trace.py`).

From this folder, in order:

1. Run `python -B native_trace.py 0`, then `python -B native_trace.py 1`. They first compare the original time array's full overlap, then save the endpoint and the forward pressure stencils. Run `python -B pressure.py`.
2. Run `python -B history_check.py 4` then repeat with `5`. These rates are the saved number of elements per comoving Mpc, not tunable coefficients.
3. Run `python -B coupled_readout.py 4` then repeat with `5`. Both ordinary and incremental solves and source-sector controls are saved; deliberately amplified diagnostics are separately labelled. No rerun of a failed amplified solve is used to replace it.
4. Run `python -B graph_accuracy.py 4` and repeat with `5`, then `python -B phase_integral.py`, `python -B temporal_modes.py` and `python -B compare_lifts.py`. These validate distinct pieces: exact finite changes of the nonlinear constraint tensor, the frozen spatial expansion, exact real phase averaging, homogeneous *time-dependent* mode evolution, and the host-only proper-radius comparison.
5. Run `python -B verify_transport.py`. It validates the numerical products and parent seal, and writes or compares the inventory with SHA-256 checksums. Repeated runs compare bytes, not just an “OK” string. The prior signed-slice packet and the ordinary cold controls are here (not bundled here). The job does not run indefinitely, and no server or detached worker is needed.

The numerical claim is conditional on the initial normal graph, background/spectator prescription, boundary and two signed matter preparations. Multiplying the conformal tide in Mpc⁻² by (c/(a Mpc))² converts it to s⁻². Terms in the error diagnostics are not new observational error bars.
