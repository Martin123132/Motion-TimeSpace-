# 5502: D4 parent-v58 high-t sibling resume handoff

## Certified result

- Source: checkpoint-5501 frontier `181/5/0`, SHA-256 `83831a5709eed87c5d82804db3c4b87f3a8d4a8ce3184ca591cf95984dac4015`.
- Evaluated: `R_E0S_E0S_E1S_X0S_X0S_T1S`.
- Outcome: `ACCEPTED` after `74.65516149997711` seconds.
- High-t denominator lower: `8.20397988265475e-05`.
- High-t relative-root lower: `0.953396548588503`.
- High-t selected-global-root lower: `0.309986868592539`.
- High-t collision-Jacobian lower: `0.883337496611847`.
- High-t regular-path upper: `457857169302.248`.
- Enclosure: `V53_EXACT_UNIFORM_T_LEAF_UNION_SUM`.

The high-t leaf plus the two certified low-t x leaves exactly close parent
`R_E0S_E0S_E1S_X0S_X0S`. Their union has rational volume error `0.0`,
regular-path upper `2.61787793281148e+17`, amplitude-denominator lower
`1.8910427091829266e-08` and collision-Jacobian lower
`0.4594589035987657`.

- Frontier: `182/4/0`; witnesses: `63`.
- New v58 applications: `0`.
- Validation: `16/16`; current source rows: `69/69`.

## Next target

Evaluate `R_E0S_E0S_E1S_X0S_X1S`, epsilon `[0.0025,0.005]`, x
`[0.8571076493072545,0.8571564165685353]`, t `[0.0002,1.0]`. Use one core,
BelowNormal priority and evaluate-before-commit atomicity. Do not recompute or
weaken the checkpoint-5502 three-leaf union.

## Immutable evidence

- Runner: `scripts/Y5_R2FR_5502_D4_parent_v58_high_t_sibling_gate.py`
- State: `source-intake/functional_rg/5502/work-v1/E07__U051__RIGHT_CONNECTOR__CUBOID__6df3d70a73e4618b.json`
- Result: `source-intake/functional_rg/5502/D4_parent_v58_high_t_sibling_result.json`
- Validation: `source-intake/functional_rg/5502/P8_Y5_BRR5501_5502_VALIDATION.csv`
- Source register: `source-intake/functional_rg/5502/source_register.csv`
- Node audit: `source-intake/functional_rg/5502/D4_parent_v58_high_t_sibling_audit.csv`
- Runner SHA-256: `7fe7833197b124ed9c228492f82cda8ba3810278b38c026ce7042fee9405a4d8`
- State SHA-256: `fa7e401c5981d83c12dffdbb9e4cc8b9e9d1847fe4393f3509fcde883fca892c`
- Result SHA-256: `8e40ee678a76a58e99706054c640388e94918d56b8b7214f865d39e9a0129623`
- Validation SHA-256: `98918d686f8669f971aec5730851a32a68c8adcb34ea53a64cacfdb8329aa6bd`
- Source-register SHA-256: `305b96cdbc48740f5ccb200dd583604e42eef640af4aae9d7f0555e5f38d0894`
- Node-audit SHA-256: `642e62b6a1e94490fabb4641b82373db2cf8349f142e2bcce94e0d0d60b025ad`

## Claim boundary

Checkpoint 5502 certifies one exact three-leaf finite union inside the active
positive-epsilon branch. It does not certify the full active cuboid, full outer,
event-local/combined `W3`, regulator limit, all-operator local GR or full MTS.
