# Pre-execution adapter correction

The inherited-node assembly in full_cell_audit.py supplied index both explicitly and through an inherited mapping. That path has not run; it would raise a duplicate-keyword error while building the completed-coverage audit. full_cell_audit_v2.py uses dict(mapping,index=global_index), leaving all mathematical checks and tolerances identical. The original file is retained because probe sources already record its hash. The probe path is unaffected. No failed physical calculation or input replacement occurred.

Campaign launch additionally requires every new probe segment/branch/channel numerical comparison to pass, not merely the audit's structural passed field. This condition is checked explicitly by bounded_campaign.ps1 before any production batch is launched.

