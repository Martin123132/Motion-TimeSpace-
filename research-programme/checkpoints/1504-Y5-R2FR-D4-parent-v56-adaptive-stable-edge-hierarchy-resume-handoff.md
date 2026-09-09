# 5488: D4 parent-v56 adaptive stable-edge hierarchy resume handoff

Checkpoint 5484 performs six atomic evaluations from the checkpoint-5487 state. Three nodes pass and three coarse boxes reproduce the already-derived connector stable-edge enclosure class. Every parent-v56 collision-Jacobian union remains positive; no new algebraic obstruction appears and no parent-v57 term is introduced.

## Accepted nodes

1. `R_E0S_E0S_E0S_E0S_X0S_X0S_T1S`, x `[0.8570372233341658,0.8571076493072545]`, t `[0.5,1.0]`, passes the v53 exact t cover with amplitude-denominator lower `8.443946350403823e-05` and collision-Jacobian lower `0.8847253192374765`.
2. `R_E0S_E0S_E0S_E0S_X0S_X1S_T0S`, x `[0.8571076493072545,0.8571564165685353]`, t `[0.0002,0.5]`, passes the v55 exact x/t cover with amplitude-denominator lower `3.115762383787817e-08` and collision-Jacobian lower `0.8152489575954128`.
3. `R_E0S_E0S_E0S_E0S_X0S_X1S_T1S`, over the same x interval and t `[0.5,1.0]`, passes the v53 exact t cover with amplitude-denominator lower `0.00010730682756010485` and collision-Jacobian lower `0.8924459752149636`.

## Exact adaptive refinement

The three failed coarse boxes all carry the same signed witness:

`interval denominator reaches zero: away_arc_left_K5:s1:c0:left1:edge_2_1_3:stable_edge`.

Their v56 Jacobian unions are not the problem. The three new `16 x 128` rows all pass, with minimum leaf-union lower `246.78642183189933`, minimum rectangular-hull lower `244.90338631483147`, minimum chart-denominator lower `6.32556660893073e-05` and exact-cover error `0.0`.

The runner therefore uses exact source-aligned x/t bisection rather than adding a broader fallback. This is the existing adaptive finite-cover theorem, not a closure assumption.

## Current frontier

- State: `source-intake/functional_rg/5484/work-v1/E07__U051__RIGHT_CONNECTOR__CUBOID__6df3d70a73e4618b.json`.
- SHA-256: `4a3bf787cf8e435d6eca06010ed3ac4db45345d8bc18c6f52cb82059f5fc66e6`.
- Accepted/pending/unresolved: `174/7/0`.
- Parent-v56 node evaluations: `9`.
- Parent-v56 accepted nodes: `6`.
- Parent-v56 refinement witnesses: `3`.

## Exact next calculation

Resume checkpoint 5484 for one atomic node at
`R_E0S_E0S_E0S_E0S_X1S_X0S_T0S`, x
`[0.8571564165685353,0.8572051848104696]`, t `[0.0002,0.5]`.
Keep one BelowNormal core. If this child passes, preserve it; if the same
stable-edge class persists, retain the exact split hierarchy rather than
inventing parent v57 without a distinct obstruction.

Full active-cuboid, full outer, event-local/combined `W3`, regulator-limit,
all-operator local-GR and full-MTS claims remain false. No GitHub action and no
`formalization-workbench` edit belongs to this checkpoint.

**PARENT_V56_ADAPTIVE_STABLE_EDGE_HIERARCHY_CONTINUES__NO_V57_REQUIRED**
