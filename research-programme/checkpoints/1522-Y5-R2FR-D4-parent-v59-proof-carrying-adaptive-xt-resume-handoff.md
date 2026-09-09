# 5506: D4 parent-v59 proof-carrying adaptive x/t resume handoff

## Certified candidate

- Source frontier: checkpoint 5505, `184/3/0`, SHA-256 `df67524e5d8f81d9642cd04514c1f22e325fa0dedf1f466dcf7a74de3c940a8b`.
- Real triggered target: `R_E0S_E0S_E1S_X0S_X1S`.
- Live parent-v58 trigger: exactly one
  `edge_2_1_3:stable_edge` `IntervalSingularity`.
- Derived split: t at exact source boundary `0.5`.
- Terminal evidence: exactly two immutable parent-v58 exact-binding
  certificates, bindings
  `30a28e5e93272a50abd5...` and `dd807ddd421fa4b092ed...`.
- Target runtime: `1037.1593281000387` seconds.
- Target aggregate exactly equals the independently assembled child union.
- Target denominator lower: `2.95404190746998e-08`.
- Target collision-Jacobian lower: `0.731510745407076`.
- Untriggered control: `R_E0S_E0S_E1S_X0S_X1S_T1S`.
- Control runtime: `63.1520964000374` seconds.
- Control trigger count: `0`; all physics fields exactly match its parent-v58
  source certificate.
- Parent-v58 bound-certificate applications: `0`.
- Validation: `19/19`; source register: `95/95` current.

The candidate changes only enclosure composition. It evaluates the root under
the unchanged parent, triggers only on the precise stable-edge exception,
selects an exact inherited x/t source split, and accepts only if every terminal
leaf is a live or immutable exact-binding complete-parent certificate.

## Next target

Perform a status-only migration of checkpoint 5505's frontier from parent v58
to parent v59. The accepted, pending, unresolved and witness ledgers must be
byte-equivalent under canonical hashing; no numerical node may be evaluated.
After migration, evaluate pending `R_E0S_E0S_E1S_X1S` with the general wrapper.

## Immutable evidence

- Runner: `scripts/Y5_R2FR_5506_D4_parent_v59_proof_carrying_adaptive_xt_integration_gate.py`
- Result: `source-intake/functional_rg/5506/D4_parent_v59_proof_carrying_adaptive_xt_result.json`
- Validation: `source-intake/functional_rg/5506/P8_Y5_BRR5505_5506_VALIDATION.csv`
- Source register: `source-intake/functional_rg/5506/source_register.csv`
- Application audit: `source-intake/functional_rg/5506/D4_parent_v59_adaptive_xt_application_audit.csv`
- Proof cache: `source-intake/functional_rg/5506/D4_parent_v59_exact_binding_proof_cache.csv`
- Comparison: `source-intake/functional_rg/5506/D4_parent_v59_target_control_comparison.csv`
- Runner SHA-256: `e29f4bc38eab7c9834512dd7c3020bc10a3207dc63486ca27d1e282dfe894fa0`
- Result SHA-256: `f519605a65d2947c8a2866f5e4e929816e47c5f684ffe380f1bd0891d025f2f9`
- Validation SHA-256: `423ece3372279b98df7a763b1f7442af64bff159bdf014a7b7b47f2ca02c7184`
- Source-register SHA-256: `a40668f99d394e400394d31bb257c2d04a91124e148c4711368a1e6971ca3efa`
- Application-audit SHA-256: `0d47a2798846f0e3c7d4ddc2d0051e3baa4365fdf7f2512bc415f423c00dfc27`
- Proof-cache SHA-256: `981da19698a0db9195038b15aba849647deec80e2ea277b725419f8047a5aaba`
- Comparison SHA-256: `54e65b04ed5dc25271eec5324bb184c1cda722c424b175b28a923f3b8b7717cf`

## Claim boundary

Checkpoint 5506 certifies a parent-v59 candidate and one real target/control
pair. It has not yet migrated the active frontier and does not certify the
complete active cuboid, full outer, event-local/combined `W3`, regulator limit,
all-operator local GR or full MTS.
