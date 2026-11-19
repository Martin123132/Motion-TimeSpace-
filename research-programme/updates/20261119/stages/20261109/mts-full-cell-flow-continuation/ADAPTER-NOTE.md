# Continuation-only adapter

The source evaluation and flow projection functions are imported unchanged from the sealed full-cell parent. The authoritative full freeze stays in that parent; no fresh node selection is made.

continuation_audit.py differs from the executed parent full_cell_audit_v2.py only in collecting batch receipts from INHERITED_BATCH_STAGES plus this stage. all_source_projection.py changes the same catalogue collection and imports that identical integration helper. common.py changes ownership, cutoff, inherited seal/hold checks and module routing. New probe is frozen ordinal40 rather than already completed ordinal1.

This prevents an omission of the first40completed segments when auditing a new output directory. Existing inherited duplicate checks remain active. Parent baseline data and all1e-10/2e-5 gates stay unchanged. The bounded campaign starts at batch05 and uses segment40as its reusable probe; no previous worker or source point is restarted.

