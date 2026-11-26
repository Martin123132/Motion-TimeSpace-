> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# Private replay guide

From this directory use the existing Python 3.13 environment with NumPy, SciPy and the archived FIRE dependencies. The short integrity check reads local files and starts no worker:

    python -B verify_matched.py

This verifies the two upstream manifests and their listed files, compiles local source in memory, compares the represented wave and clock with their sealed endpoints, checks the new numerical comparisons, and verifies the contents of this stage against its manifest. It does not regenerate the expensive histories. Do not use Python optimization (-O) for checking. The full calculation used one numerical thread per worker. No downloads or new catalogues are needed.

## Self-contained order of operations given the archived inputs

1. Read [the frozen protocol](PROTOCOL.md) and [the inherited reciprocal run](../mts-fire-live-poisson-feedback/RESULTS.md). The initial states, source map, and remaining host field are inherited, not reconstructed from clock readouts.
2. For each radial layout S = 0 and 2, run 'python -B matched_evolution.py predict S 1' before evolving. Layout 0 places each bin at its saved radius; 2 splits at probe and wave nodes and uses two radial integration nodes in each subinterval. Both use one angular parcel per original bin in the evolution.
3. For each arm A = reset and coupled run 'python -B matched_evolution.py live 0 1 A raw 4 8 16' and 'python -B matched_evolution.py live 0 1 A represented 16'. For radial layout 2 replace 0 by 2 and use step counts '4 8' for raw and '8' for represented. The last argument is a step count over the same 0.24 Myr, not an epoch selector.
4. Run 'python -B source_path_law.py 0 1 16', then 'python -B source_path_law.py 2 1 8'. For each arm A run 'python -B local_exchange.py A'. This last script writes the corrected endpoint test; the two local-exchange CSVs are retained **pre-repair diagnostics**, not a competing result.
5. Run 'python -B ordinary_metric.py', then 'python -B summarise_hosts.py'. They split the live/fixed and crossed-host readouts. The tag-only trajectory check uses common parcel indices and small displacement differences.
6. Run 'python -B crossed_metric.py', 'python -B shell_clock.py', 'python -B continuum_response.py', and 'python -B area_replay.py'. The last uses finite-amplitude area roots independently of the expansion formula, but the same underlying fields. Doubling radial/angular quadrature and changing the assumed within-bin mass law are separate checks, not observation-based error bars.
7. The published-to-self seal was made once with 'python -B verify_matched.py --seal'; use the read-only invocation above for subsequent verification. Retain byte-for-byte upstream data. For exploratory reruns use a separate sibling directory with the same relative upstream paths; do not replace saved receipts after numerical-library changes.

## Main result files

Newtonian budget (not bundled here) · direct tagged trajectories (not bundled here) · continuum acceleration (not bundled here) · spatial/time constraints (not bundled here) · shell clocks and isolated tail (not bundled here) · nonlinear geometry replay (not bundled here) · [properly matched shell exchange, reset](evidence-001.zip) (archive member: `boundary-matched-exchange-reset.csv`) and [inherited](evidence-001.zip) (archive member: `boundary-matched-exchange-coupled.csv`). Host and transition units are specified in [the derivation](DERIVATION.md) and [results](RESULTS.md).
