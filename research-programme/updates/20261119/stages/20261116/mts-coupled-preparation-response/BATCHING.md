# Bounded integration batches

The full native comparison is larger than the earlier subsystem check.
The initial cold worker started both32/64 solves in one1500-second slot.
To preserve completed work rather than let its second solve hit that guard,
the supervisor requests an intentional local hold only AFTER the32-step
archive appears. Archive writing finishes before the next guard call.
The worker's finally block releases its native owner; only then is this
task-owned hold removed. The first capture and completed32-step solve
are retained, not relaunched.

run_sized.py uses the identical Coupled implementation but runs one step
choice per bounded worker. The native live context is re-established and
verified against the exact saved full state; this is not a new preparation
choice. Source equations, integration steps, numerical units, output grids
and tolerances do not change. Existing archives refuse overwrite.

Any original failure receipt reading this task-owned checkpoint hold is
an intentional handover, not a failed scientific test or a retry license.
Do not remove an owner-created or different stop request.
