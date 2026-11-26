> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# Replaying this private stage

Use the same Python 3.13, NumPy/SciPy and inherited local FIRE inputs as the 70-file predecessor (not bundled here). From this directory run **python -B verify_directional.py** for a read-only verification. It reads the prior manifest, verifies the saved files and identities and checks the trial's own seal; it does not redo the evolutions. Nothing needs downloading. For fresh numerical work use a new sibling directory with the same parent paths, and keep one numerical thread per worker.

Computational order (replace each listed argument literally):

1. 'python -B directional.py 4 volume', then '8 volume' and '8 radius'. These produce the coordinate/rod clocks and multipoles. 'python -B split_tensor.py 8 volume' and '8 radius' separately recover the transverse components. 'python -B controls.py' and 'python -B rod_replay.py' give analytic Hodge and finite rod-root controls.
2. 'python -B light_link.py 4 volume 3', '8 volume 4', '8 radius 4' produce the analytic light-flight predictions. The earlier 'current-volume-4-3.csv' is a preserved pre-trace diagnostic; the completed script additionally writes the trace test as a separate file. 'python -B null_controls.py' checks formulas by integrating exact null pulses on manufactured fields.
3. Only **after** saving the predictions: 'python -B flight_evolution.py N ARM SOURCE', once per N = 8,16, ARM = reset,coupled, and SOURCE = raw,represented. An existing evolution packet is protected against restart/replacement. Use 'python -B flight_evolution.py reduce N' after each complete set, then 'python -B finite_checks.py'. Run 'python -B bandwidth.py' to compare the same angular clock kernel with the preceding stage's acceleration. The finite wave readout is the original capped native-grid readout, not a silent change to the evolution's angular/grid conventions.
4. 'python -B normal_products.py' independently recomputes the angular normal constraint with exact factorial weights. 'python -B verify_directional.py --seal' is for initial creation only; use the read-only mode on later visits. The larger per-arm receipts are NumPy arrays loadable without pickle; dimensions, times and unchanged launch states are checked across hosts and refinements. No sessions need to be kept alive after verification.

[Derivations](DERIVATION.md) · [Results and remaining assumptions](RESULTS.md) · angular split (not bundled here) · independent trace/current agreement (not bundled here) · finite flight (not bundled here).
