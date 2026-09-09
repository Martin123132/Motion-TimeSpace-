# Preserve selected terminal integrals, not every attempted refinement

Private implementation companion, 2026-09-08. This extends the saved E06
calculation without editing the frozen parent, core runner, old geometry
seed wrapper, completed batch1, or historical source certificates.

## The exact ownership issue

An adaptive parent may try a partition, successfully evaluate some children,
then abandon that partition after another child fails and try a different
one. A list of all successful calls is therefore not a disjoint integration
cover. Nor does a final `V53/V54/V55...SUM` label retain the terminal
integration methods by itself.

The new observer records both the call graph and the actual rows supplied
to each successful aggregation. It preserves object identities through
forwarding wrappers and records which returned object each aggregator used.
Traversing only those selected edges recovers the terminal contributions;
abandoned trials remain in the trace but are not counted as selected leaves.

For a genuine selected disjoint partition D=union D_j, if every terminal
bound is an absolute-integral bound U_abs(D_j), their sum bounds the absolute
integral on D. The same upper bound is safe on an arbitrary subset of D.
No division by area or leaf count is authorized. If a terminal integration
method has not been classified, the observer records it as unresolved
instead of turning its signed-integral bound into a pointwise bound.
Exact domain coverage and the numerical bound's arithmetic still remain
with the frozen parent and its validation; a trace is not their replacement.

## Implementation and controls

`scripts/D4_E06_terminal_trace_20260908.py` wraps the existing evaluation and
aggregation functions in memory. Each invocation calls its original function
exactly once and returns the same object or rethrows the same exception.
It changes neither amplitudes, chart schedules, source inputs nor thresholds.

Each atomic record gets one append-only, flushed JSONL trace and one summary
under its existing batch directory. Calls retain implementation path/hash,
source binding, full input arguments, binary64 coordinate values, and full
parent results before the existing compact frontier representation is saved.
The original parent records remain authoritative for numerical outcomes.
The observer's completion status separately reports trace validation.

The control suite passed **15/15**, including deliberately abandoned successful
trials, unclassified primitive methods, exact return/exception identity,
single invocation, missing-origin rejection and bytecode/source preservation.
This validates observer behavior on explicit controls, not the physics.
The full source/parent strict dry run passed **17/17**, with no numerical
parent evaluations and no modification of the saved frontier.

Frozen observer SHA:
`e22f9795d45b540b1db258afde973e760b291fab0e38dea6b690312261132ee4`.
Control outputs: `source-intake/functional_rg/5515/terminal-trace-selftest-initial/`.
Preflight: `source-intake/functional_rg/5515/geometry-seeded/trace-preflight1/`.

## Current bounded run

The fresh tag is `trace-batch2`, with at most 8 nodes and a 1800-second budget
checked BETWEEN nodes. An in-flight atomic node is saved before stopping.
It resumes the existing 9-accepted/209-pending frontier, initially SHA
`f8df1c114720fcbebac129c90dcebef4047a7fcdc27b475411f28f05b11315f7`.
No E07 numerical certificate is copied. One BelowNormal numerical worker
uses one logical core. Inspect the live process command and exit marker
before any continuation; a lock alone is not evidence of a live worker.

Launcher: `source-intake/functional_rg/5515/geometry-seeded/launch-terminal-trace-20260908.ps1`.
It requires an explicit fresh tag and expected saved-state hash, preserves
existing output paths, and starts a hidden supervisor/worker.

Global W3, the complete matched MTS coefficient, all-operator local GR and
full unification are still unclaimed. No GitHub operation is performed.

## Completed execution and interruption recovery

The execution connection reset during trace-batch2. The worker and supervisor
were subsequently confirmed absent, with no completed record 10. Its partial
trace and checked dead-worker lock were preserved rather than deleted.
Trace-batch3 resumed only the unfinished node from the same saved frontier.

Trace-batch3 finished at 02:57:03 BST, exit 0. Records 10 and 11 both passed,
in 1400.920 and 1270.445 seconds respectively. Total frontier is now
**11 accepted / 207 pending / 0 unresolved**. All 21 core validation checks
passed; both trace summaries passed their five observer checks.

Each new record selects 98 actual `POINTWISE_SUPREMUM` terminals through seven
aggregations. Thus their aggregate labels no longer hide the integration
type. This is not retroactively assigned to the older untraced records.

`scripts/D4_E06_trace_verify_20260908.py` compiled and passed **47/47** checks
after the worker exited. It independently checks the call graph, selected
source identities, exact binary-rational rectangle covers and terminal types,
with gap/overlap/outside/empty-cover controls. It also reproduces all **144**
completed returns from the interrupted trace by exact call binding and
implementation identity; no mismatches occur. The partial trace thereby
supplies a reproducibility control, not an extra completed parent node.

The verifier records upward-rounded sums of the selected recorded terminal
bounds. These sums are conditional on the terminal bounds themselves; they
do not silently replace the proof of the terminal arithmetic or the global
event integral.

Saved state SHA:
`1a5960f1521b21bdd3d8c02a6fafc7425a4d450a3a5bae697a0c7944f8d05187`.
Independent verification: `source-intake/functional_rg/5515/geometry-seeded/trace-batch3/independent-trace-verification.json`,
SHA `1462b64d720c152e4a22415fb0bd9e0117c70c492e3550feea272aa55e4b50dd`.
No successor worker was launched at this handoff.
