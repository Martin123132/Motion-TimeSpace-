# Reproducing the signed-cloud evolution

Use the retained local 64-bit Python 3.13 environment with NumPy, SciPy, SymPy and the native cosmology implementation used by the predecessor. Keep this folder beside the original normal-transport and signed-constraint checkpoints. Input identities are checked before reuse. No observations, additional epochs or new fit are required.

- `python -B replay_cloud.py representative` repeats ten groups serially, including both signs of the cloud, analytic controls, a cold branch, transport, conserved surroundings and the tidal-rate integral. This set was replayed successfully against the saved outputs.
- `python -B verify_cloud.py` checks input hashes, the saved switches, wave, conservation and precision gates, numerical tables and file inventory. It writes the seal on first success and compares it on subsequent runs. Passing includes reproducing the explicitly recorded precision failures; it does not promote a failed tolerance.
- `python -B replay_cloud.py all` is the longer reconstruction, also serial, including both cold traces, preparation refinements and the deliberately rejected amplified diagnostic. It is not needed to read the results. The representative subset, not this whole sequence, was rerun after generation.

See [results](RESULTS.md) and [derivation](DERIVATION.md) for the pressure and clock preparations, force sign and proper ruler. All runs are finite commands; no service or scheduler is needed.
