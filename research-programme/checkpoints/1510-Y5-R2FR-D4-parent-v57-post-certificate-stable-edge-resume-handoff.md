# 5494: D4 parent-v57 post-certificate stable-edge resume handoff

## Locked position

- The source checkpoint-5484 frontier remains `178/8/0` accepted/pending/unresolved at SHA-256 `3f485d18bb2a55d3fda317091e58c0330166a7b5ae7e2185a82ab46602e23faa`.
- Checkpoint 5493 binds the checkpoint-5492 `E16 x X32 x T128` collision-Jacobian certificate to its exact local geometric-factor domain. It applies once and removes the collision obstruction, but the unchanged complete parent amplitude then reaches `away_arc_left_K5:s1:c0:left1:edge_2_1_3:stable_edge`.
- The untriggered checkpoint-5493 parent-v56/parent-v57 control is exactly identical. Parent v57 is therefore scoped correctly but is not accepted as a complete target pass.

## Checkpoint-5494 constructive result

The inherited parent-v55 schedule fails at `X2 x T32`, `X4 x T32` and `X4 x T64`. The finest first failed leaf is

- x: `[0.8570968199513506,0.8571564165685354]`;
- t: `[0.0002,0.015821875]`;
- schedule position: `X4:T64`, leaf `1:0`.

Complete parent-v54 child amplitudes were evaluated with the scoped parent-v57 collision certificate still installed. Epsilon-real and epsilon-imaginary subdivisions through 32 fail on their first child. X subdivisions through 16 fail on their first child; at X32, child zero passes and child one fails. One exact t bisection is sufficient:

- child 0: `[0.0002,0.0080109375]`;
- child 1: `[0.0080109375,0.015821875]`;
- both complete amplitudes pass;
- minimum amplitude-denominator lower: `1.7041112393221877e-08`;
- minimum collision-Jacobian lower: `1.902438820174668`;
- exact t-coverage error: `0.0`.

This identifies a local interval dependency rather than a new action term. It is a parent-v58 candidate only.

## Exact next implementation contract

Build a parent-v58 target/control integration gate. Preserve the parent chain and every physical threshold. On the demonstrated stable-edge exception, inside the exact source-bounded failed leaf and only after the scoped parent-v57 certificate is active, replace that one complete-amplitude call by the two exact t children above. Require:

1. parent v57 reproduces the post-certificate stable-edge failure;
2. parent v58 invokes the t-bisection exactly once;
3. both unchanged complete child amplitudes pass;
4. their domains form the parent leaf exactly, with no gap or overlap;
5. the complete target returns finite with positive denominator and collision-Jacobian lowers;
6. an untriggered parent-v57/parent-v58 control is exactly identical;
7. no action, contour, chart, selector, residue, threshold or source frontier changes.

Only after all seven clauses pass may parent v58 be migrated into the checkpoint-5484 frontier. Full outer enclosure, event-local or combined `W3`, the regulator limit, all-operator local GR and full MTS remain open.

## Immutable evidence

- Runner: `scripts/Y5_R2FR_5494_D4_parent_v57_post_certificate_stable_edge_axis_probe.py`
- Result: `source-intake/functional_rg/5494/D4_parent_v57_post_certificate_stable_edge_axis_result.json`
- Axis audit: `source-intake/functional_rg/5494/D4_parent_v57_post_certificate_stable_edge_axis_ablation.csv`
- Validation: `source-intake/functional_rg/5494/P8_Y5_BRR5493_5494_VALIDATION.csv`
- Runner SHA-256: `bcaadd40a0096fdc70fad4c881ca037826c6000df74a10647f12c1206325dff0`
- Result SHA-256: `bb624b0ce3d54699212723526ff109305a7400b34f54d9f8588095bc2c9710bd`
- Axis-audit SHA-256: `8b7f0208048a6bc3ff334f678124a3fac36b3cd54050cb091bfb1caabc570145`
- Validation SHA-256: `2d0f750871ecce8e66a5411ec30bb4684b7b0aba7a516982b04a6bacc32cfa61`

