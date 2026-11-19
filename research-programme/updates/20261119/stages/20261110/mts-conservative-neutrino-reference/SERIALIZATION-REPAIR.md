# Retained first attempt and serialization-only repair

The first reference worker (PID 33532, creation time in reference-start.json)
exited with a TypeError while encoding a NumPy boolean as JSON. Its terminal
receipt records failure. No completed reference-result.json existed.

check_reference_attempt1.py retains that implementation. The repaired reader
casts the occupation-bound boolean to Python bool and uses new worker receipts.
It verifies and reuses the existing shell-rules.npz without rewriting it.
All formulas, masses, nodes, weights, tolerances and continuum integrations
are unchanged. This is not a retry of a rejected physical hypothesis.

Reference evaluations are recomputed after that saving failure; saved
trajectories and any production background/evolution are not rerun.
