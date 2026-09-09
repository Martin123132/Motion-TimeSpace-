# 5496: D4 parent-v58 adaptive stable-edge T2 resume handoff

## Locked source position

- Checkpoint-5484 frontier: `178/8/0` accepted/pending/unresolved, SHA-256 `3f485d18bb2a55d3fda317091e58c0330166a7b5ae7e2185a82ab46602e23faa`.
- Target: `R_E0S_E0S_E0S_E1S` in `E07__U051__RIGHT_CONNECTOR__CUBOID__6df3d70a73e4618b`.
- Parent v57 supplies the exact scoped collision-Jacobian certificate but the complete target reaches `away_arc_left_K5:s1:c0:left1:edge_2_1_3:stable_edge`.

## What checkpoint 5495 rejected

The first parent-v58 candidate replaced only the checkpoint-5494 failed leaf `X1:T0` by two exact t children. Both children and the next 127 complete-amplitude leaves pass, giving 129 passing final leaves. The same stable-edge class then occurs at `X2:T0`. The hard-coded one-location rule is therefore rejected; its 129 positive leaves are retained as source-locked evidence.

## Derived parent-v58 rule

On the exact `X4 x T64` complete-amplitude cover, evaluate every base leaf unchanged. If and only if that leaf raises the identical `edge_2_1_3:stable_edge` interval singularity, replace it by its two exact t halves and require both unchanged complete amplitudes to pass. Any other failure class, or either failed child, rejects the rule. This changes finite-cover composition only.

## Certified result

- All `256/256` base cells resolve.
- Final complete-amplitude cover: `259` leaves.
- Exact T2 replacements: `X1:T0`, `X2:T0`, `X3:T0`; `X0:T0` passes without replacement.
- Replaced t interval: `[0.0002,0.015821875]` in each affected x strip.
- Exact parameter-area error: `0.0`.
- Integrated regular-path upper: `4.286134854559046e+18`.
- Amplitude-denominator lower: `8.369218233636728e-09`.
- Relative-root lower: `0.9413782923495447`.
- Selected-global-root lower: `0.3098121936985199`.
- Collision-Jacobian lower: `0.915559101588387`.
- Complete parent-v58 target passes; certificate application count is one.
- The untriggered parent-v57/parent-v58 control is exactly identical; control application count is zero.
- All `13/13` checkpoint-5496 validation gates pass.

The parent-v58 target/control gate is certified. The active frontier has not yet been migrated, so the active cuboid and every broader GR/MTS claim remain open.

## Exact checkpoint-5497 migration contract

Create a hash-locked copy of the checkpoint-5484 state and install the unchanged `v52 -> v53 -> v54 -> v55 -> v56 -> v57 -> v58` parent chain. For target `R_E0S_E0S_E0S_E1S`:

1. verify the checkpoint-5496 runner, work state, certificate, result and validation hashes;
2. verify the five pending target descendants form an exact partition of the target, with volume error `0.0`;
3. verify there are zero accepted target descendants;
4. remove exactly those five pending descendants;
5. add exactly one accepted coarse target row using the certified parent-v58 result;
6. retain the four prior refinement failures as historical, explicitly superseded witnesses;
7. preserve every unrelated accepted, pending, unresolved and audit row exactly;
8. require the migrated frontier to be `179/3/0` and its accepted volume to be `5.96085317405059e-07` before any further node evaluation.

After status-only migration, resume the next pending frontier node atomically under parent v58. Do not claim the complete active cuboid, full outer enclosure, event-local or combined `W3`, the regulator limit, all-operator local GR or full MTS.

## Immutable evidence

- Runner: `scripts/Y5_R2FR_5496_D4_parent_v58_adaptive_stable_edge_T2_gate.py`
- Work state: `source-intake/functional_rg/5496/work-v1/parent_v58_adaptive_stable_edge_T2_state.json`
- Certificate: `source-intake/functional_rg/5496/D4_parent_v58_adaptive_complete_amplitude_certificate.json`
- Result: `source-intake/functional_rg/5496/D4_parent_v58_adaptive_stable_edge_T2_result.json`
- Validation: `source-intake/functional_rg/5496/P8_Y5_BRR5495_5496_VALIDATION.csv`
- Runner SHA-256: `8709e97da3fdd0a0d8453c6ead0299c6024ca82e3214f5e2d045b8fca6239537`
- Work-state SHA-256: `63745c8d0ac00efc0809a77696206f2ee049b4ef35c1bd60d1e712085fb68b95`
- Certificate SHA-256: `27dc7fce1f83b424e9d9341778a392b83ed7c8659d12e05afd561338782fc708`
- Result SHA-256: `615ba9da7bef062fbfeb5ea0b5fe33d537715e2c46527c49416d18d4b629ed9a`
- Validation SHA-256: `ae0ef0a2c5fba86a3b1b667a55aeefc212aad2193bd1c5528ef4a73510d954e4`
- Source-register SHA-256: `18b614194e4a221648a94ab4fcb4385621acc306427e3792718760706df676fc`

