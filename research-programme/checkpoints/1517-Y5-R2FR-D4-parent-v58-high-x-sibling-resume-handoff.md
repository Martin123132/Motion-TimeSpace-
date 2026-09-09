# 5501: D4 parent-v58 high-x sibling resume handoff

## Certified result

- Source: checkpoint-5500 frontier `180/6/0`, SHA-256 `b916d268ac3c6466c46b53d9fa597feab86ae37d8d8584731c6c3fd248d05e8e`.
- Evaluated sibling: `R_E0S_E0S_E1S_X0S_X0S_T0S_X1S`.
- Outcome: `ACCEPTED` after `16175.45627720002` seconds.
- Amplitude-denominator lower: `1.8910427091829266e-08`.
- Relative-root lower: `0.958525846226203`.
- Selected-global-root lower: `0.310103465517881`.
- Collision-Jacobian lower: `0.682313809192487`.
- Regular-path upper: `2.59388355022642e+17`.
- Enclosure: `V55_EXACT_UNIFORM_XT_LEAF_UNION_SUM`.

The high-x leaf and checkpoint-5500 low-x leaf are interior-disjoint and have
exactly the rational volume of parent
`R_E0S_E0S_E1S_X0S_X0S_T0S`. The certified union lower bounds are
`1.8910427091829266e-08` for the amplitude denominator and
`0.4594589035987657` for the collision Jacobian.

- Frontier: `181/5/0`; witnesses: `63`; exact partition error: `0.0`.
- New v58 applications: `0`.
- Validation: `16/16`; current source rows: `63/63`.

## Next target

Evaluate `R_E0S_E0S_E1S_X0S_X0S_T1S`, epsilon `[0.0025,0.005]`, x
`[0.8570372233341658,0.8571076493072545]`, t `[0.5,1.0]`. It is the exact
high-t sibling of the now-certified low-t region. Use one core, BelowNormal
priority and an atomic evaluate-before-commit transaction. Do not revisit the
low-t cover unless an independent validation contradiction is found.

## Immutable evidence

- Runner: `scripts/Y5_R2FR_5501_D4_parent_v58_high_x_sibling_gate.py`
- State: `source-intake/functional_rg/5501/work-v1/E07__U051__RIGHT_CONNECTOR__CUBOID__6df3d70a73e4618b.json`
- Result: `source-intake/functional_rg/5501/D4_parent_v58_high_x_sibling_result.json`
- Validation: `source-intake/functional_rg/5501/P8_Y5_BRR5500_5501_VALIDATION.csv`
- Source register: `source-intake/functional_rg/5501/source_register.csv`
- Node audit: `source-intake/functional_rg/5501/D4_parent_v58_high_x_sibling_audit.csv`
- Runner SHA-256: `8df999ce2084911004a8ae7b393bf4ba7e359d61e16595c17392e237360bdef5`
- State SHA-256: `83831a5709eed87c5d82804db3c4b87f3a8d4a8ce3184ca591cf95984dac4015`
- Result SHA-256: `4f0203641f8c2adf0d3f79c21df73da4c950b2be14bfa9897edc5c2aecfb8ab5`
- Validation SHA-256: `5b617411755acc445a0c2408f1abdc503c560bde86cb8680a5aff97ae676f640`
- Source-register SHA-256: `97907c3ce965077ae40803e5f64e55611f71cde615eee8d902aebee003841a03`
- Node-audit SHA-256: `3bc0b591e4fcb5c0532fd62eb4475c4e72fc57e1c6df9ff090e626664e54ba60`

## Claim boundary

Checkpoint 5501 certifies the exact low-t X2 union inside one positive-epsilon
frontier branch. It does not certify the full active cuboid, full outer,
event-local/combined `W3`, regulator limit, all-operator local GR or full MTS.
