# 5374 - D4 E020 source-silent multipole Laurent repair

## Decision

`D4_E020_SOURCE_SILENT_MULTIPOLE_REPAIR_ACCEPTED__RUN_FROZEN_HOLDOUT_COMPARISON`

The completed E020 run localized four failed inner nodes to residue-classification gates. This repair transfers the parent normalized double-Laurent pole-refinement method to every unresolved pole in a node, preserving all existing residual, scale-change, second-order, masked-identity, inner-quadrature, and global error thresholds.

The v1 diagnostic resolved six of seven poles. Its last pole stopped after four refinement iterations with a residual double-pole ratio of 1.0589550643390497e-4, while its fourth pole correction remained 1.0991090150822313e-11 against the unchanged 1e-11 convergence tolerance. Version 2 therefore tests the deterministic refinement-count ladder 4, 5, 6 before increasing background degree; it does not relax a gate.

Candidate selection uses only local pole-fit and topology diagnostics. It does not read the frozen E020 prediction, perform the holdout comparison, or optimize the measured finite-rung central value.

No regulator-zero, angular, UV, local-GR, or full-MTS claim is made by the repair contract.
