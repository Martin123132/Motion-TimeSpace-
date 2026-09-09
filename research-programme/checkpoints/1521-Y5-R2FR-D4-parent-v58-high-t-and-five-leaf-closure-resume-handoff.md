# 5505: D4 parent-v58 high-t and five-leaf closure resume handoff

## Certified result

- Source: checkpoint-5504 frontier `183/4/0`, SHA-256 `74ed505b52d668d1719e99f8c992e255b6c94dd6edf266afe265f90bbb63f02d`.
- Evaluated: `R_E0S_E0S_E1S_X0S_X1S_T1S`.
- Outcome: `ACCEPTED` after `74.8370785999577` seconds.
- Node regular-path upper: `16303607776.8527`.
- Node amplitude-denominator lower: `0.000104947314549855`.
- Node relative-root lower: `0.954077168887397`.
- Node selected-global-root lower: `0.309973207177995`.
- Node collision-Jacobian lower: `0.891060030375242`.
- Node enclosure: `V53_EXACT_UNIFORM_T_LEAF_UNION_SUM`.

The high-t child and checkpoint-5504 low-t child exactly close failed parent
`R_E0S_E0S_E1S_X0S_X1S`. Their two-leaf union has denominator lower
`2.95404190746998e-08`, collision-Jacobian lower `0.731510745407076`,
regular-path upper `2.01250649936794e+17` and exact rational volume error
`0.0`.

Those two leaves and checkpoint 5502's immutable three-leaf union exactly
close `R_E0S_E0S_E1S_X0S`. The five-leaf union has denominator lower
`1.8910427091829266e-08`, collision-Jacobian lower `0.4594589035987657`,
regular-path upper `4.63038443217942e+17` and exact rational volume error
`0.0`.

- Frontier: `184/3/0`; witnesses: `64`.
- New v58 applications: `0`.
- Validation: `18/18`; current source rows: `87/87`.

## Next target

Before resuming broad node `R_E0S_E0S_E1S_X1S`, use the now-complete real
subdivision tree to integration-test the theorem in
`D4-general-proof-carrying-adaptive-cover-theorem-draft.md`. Select the cheapest
real parent-v58 stable-edge target whose exact children already pass, require a
complete target replay and an exactly unchanged untriggered control, and only
then consider parent v59. If no cheap real target exists, retain v58 and advance
the frontier without promoting the draft.

## Immutable evidence

- Runner: `scripts/Y5_R2FR_5505_D4_parent_v58_high_t_and_five_leaf_closure_gate.py`
- State: `source-intake/functional_rg/5505/work-v1/E07__U051__RIGHT_CONNECTOR__CUBOID__6df3d70a73e4618b.json`
- Result: `source-intake/functional_rg/5505/D4_parent_v58_high_t_and_five_leaf_closure_result.json`
- Validation: `source-intake/functional_rg/5505/P8_Y5_BRR5504_5505_VALIDATION.csv`
- Source register: `source-intake/functional_rg/5505/source_register.csv`
- Node audit: `source-intake/functional_rg/5505/D4_parent_v58_high_t_child_audit.csv`
- Union audit: `source-intake/functional_rg/5505/D4_parent_v58_two_and_five_leaf_union_audit.csv`
- Runner SHA-256: `f83530455d165f3decf730e3a7a3cfc316cb511be708577ec7b1920d3df2e733`
- State SHA-256: `df67524e5d8f81d9642cd04514c1f22e325fa0dedf1f466dcf7a74de3c940a8b`
- Result SHA-256: `2ec5aad038be98e747b53a753ca2f0bfeb5fa55f878f9e3601be616cbebbe171`
- Validation SHA-256: `82bf0aeaf125ca333ca2897e9924110e9d8c9c48466343125fdf12bd59fd25cd`
- Source-register SHA-256: `5cc54ff2ff25a83d5de40737766f666f81d618b6f4f2975bbd2e8d428349b423`
- Node-audit SHA-256: `d22c570a90eeb8b4762844bbae8b9c2e5ecbc79c98df4073c2749558b942a095`
- Union-audit SHA-256: `2326dd6e1da6e25cae8349218a31450f59f0841cfd4c64a61eb7aab06d112973`

## Claim boundary

Checkpoint 5505 certifies two nested exact finite unions inside one active
positive-epsilon branch. It does not certify the full active cuboid, full
outer, event-local/combined `W3`, regulator limit, all-operator local GR or
full MTS.
