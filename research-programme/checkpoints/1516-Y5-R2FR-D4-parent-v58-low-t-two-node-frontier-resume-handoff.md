# 5500: D4 parent-v58 low-t two-node frontier resume handoff

## Result

- Source: checkpoint-5499 `179/6/0`, state SHA-256 `c63cc94f32504abba2bf9adb5fa95e981505fd7d2a6260af8170ac60b47bd994`.
- Coarse low-t node: `REFINED_X2` after `482.9852973999223` seconds.
- Low-x child: `ACCEPTED` after `3746.5417996000033` seconds.
- Accepted amplitude-denominator lower: `1.81500376319531e-07`.
- Accepted relative-root lower: `0.944053322390594`.
- Accepted selected-global-root lower: `0.310163185511982`.
- Accepted collision-Jacobian lower: `0.459458903598766`.
- Accepted regular-path upper: `2.39898040133638e+15`.
- Enclosure: `V55_EXACT_UNIFORM_XT_LEAF_UNION_SUM`.
- Frontier: `180/6/0`; witnesses: `63`; exact partition error: `0.0`.
- New v58 applications: `0`; validation: `17/17`; current sources: `57/57`.

## Next target

Evaluate `R_E0S_E0S_E1S_X0S_X0S_T0S_X1S`, epsilon `[0.0025,0.005]`,
x `[0.8570588830266272,0.8571076493072545]`, t `[0.0002,0.5]`. It is the
exact high-x sibling of the newly accepted leaf. A pass closes their low-t
parent by an exact two-leaf union. A failure permits only the inherited
source-width split; it does not erase the accepted low-x certificate.

## Immutable evidence

- Runner: `scripts/Y5_R2FR_5500_D4_parent_v58_low_t_two_node_frontier_runner.py`
- State: `source-intake/functional_rg/5500/work-v1/E07__U051__RIGHT_CONNECTOR__CUBOID__6df3d70a73e4618b.json`
- Result: `source-intake/functional_rg/5500/D4_parent_v58_low_t_two_node_result.json`
- Validation: `source-intake/functional_rg/5500/P8_Y5_BRR5499_5500_VALIDATION.csv`
- Source register: `source-intake/functional_rg/5500/source_register.csv`
- Node audit: `source-intake/functional_rg/5500/D4_parent_v58_low_t_two_node_audit.csv`
- Runner SHA-256: `730d3e3f13b8302d323ea488eca6513c0e7c29a37e3f29f6ab1458ef88f98f94`
- State SHA-256: `b916d268ac3c6466c46b53d9fa597feab86ae37d8d8584731c6c3fd248d05e8e`
- Result SHA-256: `823765b7974953217d80244db8a39ee9bc4b1a04d525496457a9f828f7df82ac`
- Validation SHA-256: `c0a11f710f2d2437de7206ecee43b334b76451e44fbfc9ddc72fd96ab10c3ac7`
- Source-register SHA-256: `daf9497593c5b2b789db2d60902c9b226654f714d145f6b61be5f406d098cbca`
- Node-audit SHA-256: `4e8f59a1308b873e61475a7d2e94e588470f1aea606db2771efd2801f28a1701`

## Claim boundary

Checkpoint 5500 certifies one accepted finite-cover leaf and its coarse parent
refinement. It does not certify the complete active cuboid, full outer,
event-local/combined `W3`, regulator limit, all-operator local GR or full MTS.
