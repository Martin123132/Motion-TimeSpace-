# 5492: D4 parent-v57 uniform E16/X32/T128 candidate resume handoff

Checkpoint 5492 executes the full exact cover prescribed by checkpoint 5491. It is resumable by epsilon slab and commits each completed slab atomically. The candidate is complete and positive; it deliberately stops before parent acceptance.

## Exact cover result

The unchanged outer target node is `R_E0S_E0S_E0S_E1S`. The certificate itself belongs to its first triggered local geometric-factor domain, not to the node's full x/t box: epsilon-real `[1e-6,0.0025]`, epsilon-imaginary `[-1e-6,1e-6]`, x `[0.8570372233341658,0.8571564165685354]` and t `[0.0002,0.0011763671875000001]`.

The `E16 x X16 x T128` base partition contains `32,768` leaves. Every base leaf has zero collision-Jacobian interval lower bound. Checkpoint 5491 proved on the first such leaf that one exact x bisection is the resolving axis, so checkpoint 5492 applies that operation to every and only every zero leaf.

All `65,536` x-half children pass. Because every base leaf required the same exact bisection, the final proof object is equivalently the uniform exact `E16 x X32 x T128` finite union.

- Collision-Jacobian leaf-union lower: `172.32019740285685`.
- Rectangular-hull diagnostic lower: `172.32019740285685`.
- Minimum projective chart-denominator lower: `6.33623189561967e-05`.
- Original and covered parameter volume: `2.9082453116316825e-10`.
- Parameter-volume coverage error: `0.0`.
- Unresolved replacement leaves: `0`.

The minimum is attained at `E15:X15:T127`, x-child 1. Its two child lowers are `172.4269559911032` and `172.32019740285685`.

## Proof ownership

- Source frontier SHA-256: `3f485d18bb2a55d3fda317091e58c0330166a7b5ae7e2185a82ab46602e23faa`.
- Work-state SHA-256: `351b27598779707c199746bdc64f498b9a035dd4ef2e66bec9cfafe122a10881`.
- Leaf-audit SHA-256: `4ea6f7369a6928cb4975d409e4db1cd876bb6ac1f10c764fb4c775665acacaee`.
- Result SHA-256: `6a02d818cb0155f2e54d942fbcb0789f8d7a2cfeb7fb5ae5385898a5051e381e`.
- Validation gates: `13/13` pass.

No action, contour, chart candidate, residue, threshold or source region changes. The exact finite-union theorem is the only inference: every final leaf excludes zero, so the union excludes zero by the minimum certified leaf distance.

## Exact next calculation

Build checkpoint 5493 as the complete-amplitude parent-v57 target/control integration gate:

1. Reproduce the target failure under parent v56.
2. Bind the immutable `E16 x X32 x T128` certificate to the exact target cell, configuration fingerprint, connector segment and contained epsilon/x/t domain.
3. Evaluate the unchanged complete target amplitude under parent v57 and require positive amplitude-denominator, roots and collision-Jacobian bounds.
4. Evaluate an untriggered passing control under parent v56 and v57 and require exact equality.
5. Keep parent-v57 migration false unless every source hash, scope predicate, complete-amplitude check and control gate passes.

Checkpoint 5492 is a local geometric-factor candidate, not a certificate for the full outer target node and not a parent-v57 pass. The complete-amplitude gate must establish whether this local certificate resolves the target without exposing another context. The active frontier remains `178/8/0`, and full active-cuboid, full outer, event-local/combined `W3`, regulator-limit, all-operator local-GR and full-MTS claims remain false. No GitHub action and no `formalization-workbench` edit belongs to this checkpoint.

**UNIFORM_E16_X32_T128_CANDIDATE_CERTIFIED__BUILD_COMPLETE_AMPLITUDE_TARGET_CONTROL_GATE**
