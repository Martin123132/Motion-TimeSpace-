# Checkpoint 1192 Paired-Ensemble Snapshot

This directory is the compact public snapshot of private checkpoint `5176`. It is published after confirmatory seed 1 and before seeds 2-12. The earlier seed `517500409` is an excluded pilot.

## Frozen Identifiers

- Protocol SHA-256: `64529978cc452b302a5f09f52fff4be7af2ae8ef5cd64f29a8352005925fb7e7`.
- Protocol file SHA-256: `b804d6ff999c45efe1f5a554ca60a234df0ccfa402c007c720db712b5c38f605`.
- Schedule file SHA-256: `c690a052c7144aa15b6e68d0219d064d9900d67ab15fa6ac3ee87b0a98d7d3fd`.
- Runner SHA-256: `c15616bf4eedd9fae55c11c67a5f9064c88f6af0321ec89697f167d228ac8303`.
- Source-provenance SHA-256: `b146f03f1e247d490ef1a957804ccd2830962142867528d416f30f9b94e26ca1`.
- Seed-1 result SHA-256: `4ee9b21df70901a441e3d0e3f9860093fa3593b63f12c1c569a777616b0be4af`.

## Contents

- `ensemble_protocol.json` and `predeclared_seed_schedule.csv` contain the locked settings and seed order.
- `runner_freeze.json` records the expected hashes and read-only source identities.
- `source_provenance.csv` records the parent source paths and hashes used locally.
- `paired_seed_scores.csv`, `paired_ensemble_statistics.csv`, `seed_execution_status.csv`, `route_decision.csv`, and `paired_ensemble_results.json` record the 1-of-12 aggregate state.
- `seeds/seed_01_3240854344/` contains the compact seed-level result, diagnostics, scores, status, and completion marker. The run log and numerical caches are intentionally excluded.

## Claim Boundary

Every current result is nonclaim. The frozen rule permits a preference decision only after all 12 confirmatory seeds complete. Even then, any result applies only to the locked UGC09133 formation gate, not to MTS as a whole.

Run `python tools/verify_checkpoint_1192_snapshot.py` from the repository root to verify the five frozen hashes, seed schedule, nonclaim state, and checkpoint validation table using only the compact public snapshot.
