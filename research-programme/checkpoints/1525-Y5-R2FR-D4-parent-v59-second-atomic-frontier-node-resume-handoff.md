# 5509: D4 parent-v59 second atomic frontier node resume handoff

## Certified result

- Source: checkpoint-5508 frontier `185/2/0`, witnesses `64`.
- Evaluated: `R_E0S_E1S`, epsilon `[0.005,0.01]`, x `[0.8570372233341658,0.857275609802905]`, t `[0.0002,1.0]`.
- Outcome: `REFINED_EPSILON2` after `857.1189352000365` seconds.
- Precise failure: global-contour collision-Jacobian interval lower `0.0`.
- Nonfailing geometric lowers: relative root `0.9971775297668853`; selected global root `3.221645284809934`.
- Children: `R_E0S_E1S_E0S` on epsilon `[0.005,0.0075]` and `R_E0S_E1S_E1S` on epsilon `[0.0075,0.01]`.
- Parent-v59 events: zero triggers, zero internal splits, zero cache hits and zero aggregates.
- Frontier: `185/3/0`; witnesses: `65`.
- Exact partition error: `0.0`.
- Validation: `18/18`; current source rows: `115/115`.

The v59 wrapper correctly remains silent because this is a collision-Jacobian
enclosure failure, not the uniquely authorized stable-edge denominator failure.
The inherited outer source-width rule responds with one exact epsilon split.
No action, amplitude, contour, chart, selector, residue or v59 trigger class is
changed.

## Next target

Evaluate low-epsilon child `R_E0S_E1S_E0S` under unchanged parent v59. If it
passes, test the matching high-epsilon child and require exact two-child closure
of the checkpoint-5509 parent. If collision-Jacobian zero persists after the
source-scale refinement, isolate its first exact x/t leaf before deriving any
new certificate.

## Immutable evidence

- Runner: `scripts/Y5_R2FR_5509_D4_parent_v59_second_atomic_frontier_node.py`
- State: `source-intake/functional_rg/5509/work-v1/E07__U051__RIGHT_CONNECTOR__CUBOID__6df3d70a73e4618b.json`
- Result: `source-intake/functional_rg/5509/D4_parent_v59_second_atomic_frontier_node_result.json`
- Validation: `source-intake/functional_rg/5509/P8_Y5_BRR5508_5509_VALIDATION.csv`
- Source register: `source-intake/functional_rg/5509/source_register.csv`
- Node audit: `source-intake/functional_rg/5509/D4_parent_v59_second_frontier_node_audit.csv`
- V59 audit: `source-intake/functional_rg/5509/D4_parent_v59_second_frontier_adaptive_xt_audit.csv`
- Runner SHA-256: `bb9370c44d38d136b2bb895f999945b3dfab6047b7c28d6009b249af62e20004`
- State SHA-256: `ac63042facd73b3662b5cb1924eaeb17ddb2fb30fe15aa3ec93902b2f0e38cdc`
- Result SHA-256: `17d3380624c1d2eb57565afb0b29bd5ccb78277cb686f8007b4f9790d9351f0f`
- Validation SHA-256: `e4bf3c2285d1b2abec3a4b3c30ad2975e8522ea8083c6aa787799231b5ac0abc`
- Source-register SHA-256: `b3e1d1cb181f6cbd7ebce4aa331054bb2ca41aa8efc95c4cc89718228ff8cf49`
- Node-audit SHA-256: `2d48a5ac625ea0be7491bb67e8a7f29b061def5dfe7acb6f583c5ad7a51f33ad`
- V59-audit SHA-256: `136d8886ce5a8b5a9568d4962f1d2756acb73d8a58bc45ede7536a6dae0c8d31`

## Claim boundary

Checkpoint 5509 certifies a sound exact refinement, not an accepted parent.
The active cuboid, full outer cover, event-local/combined `W3`, regulator limit,
all-operator local GR and full MTS remain unclaimed.
