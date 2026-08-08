# 5269 - Joint angular energy-first topology preflight

## Question

Checkpoint 5268 supplies the endpoint-completed energy rule at one angular
event. The next operation must transport that rule over both angular variables
without assuming that the two angular homotopies commute.

## Transport construction

For every one of the six material components and both regulators, two paths are
constructed from the sourced event:

1. `source -> decay_cosine -> soft_cosine`;
2. `source -> soft_cosine -> decay_cosine`.

Each leg transports the unordered reciprocal root pair on `CP1`. The closure
metric is the bottleneck chordal distance between the two endpoint pair sets,
with limit `1.0e-07`. At every joint node the accepted angular
anchor is then transported over
`1.0e-04 <= x <= 0.9999` and audited at
eight energy witnesses.

The exact measure remains

`du_soft du_decay = (d c_soft/2)(d c_decay/2)`,

so the eventual angular Jacobian is `1/4`.

## Atlas result

- Joint angular nodes: `16`.
- Material component/regulator jobs: `12`.
- First-leg tracks: `24`.
- Second-leg tracks: `96`.
- Path-closure rows: `192`.
- Path-order failures: `0`.
- Maximum closure distance: `0`.
- Energy tracks: `192`.
- Maximum energy pair-set step: `0.0499499829477`.
- Maximum energy reciprocal residual: `5.15000290401e-12`.
- Cycle-state rows: `1536`.
- Angular cycle-transition edges: `582`.
- Canonical regulator-independent transition edges: `291`.
- E040/E020 cycle-state mismatches: `0`.

## Angular signatures

The six-bit signatures list active component cycles in sorted component order.

| regulator | energy | angular signature count | signatures |
|---|---:|---:|---|
| E020 | 0.0001 | 4 | `101000|101101|111010|111111` |
| E020 | 0.01 | 4 | `101000|101101|111010|111111` |
| E020 | 0.1 | 4 | `101000|101101|111010|111111` |
| E020 | 0.263057 | 4 | `101000|101101|111010|111111` |
| E020 | 0.5 | 5 | `011111|101000|101101|111010|111111` |
| E020 | 0.9 | 7 | `010100|010111|011101|100101|110010|111010|111111` |
| E020 | 0.99 | 7 | `010100|010101|010111|011101|110010|111010|111111` |
| E020 | 0.9999 | 9 | `010100|010101|010110|010111|011111|111010|111101|111110|111111` |
| E040 | 0.0001 | 4 | `101000|101101|111010|111111` |
| E040 | 0.01 | 4 | `101000|101101|111010|111111` |
| E040 | 0.1 | 4 | `101000|101101|111010|111111` |
| E040 | 0.263057 | 4 | `101000|101101|111010|111111` |
| E040 | 0.5 | 5 | `011111|101000|101101|111010|111111` |
| E040 | 0.9 | 7 | `010100|010111|011101|100101|110010|111010|111111` |
| E040 | 0.99 | 7 | `010100|010101|010111|011101|110010|111010|111111` |
| E040 | 0.9999 | 9 | `010100|010101|010110|010111|011111|111010|111101|111110|111111` |

## Decision

`ADOPT_SHARED_PIECEWISE_JOINT_ANGULAR_CHAMBERS__LOCALIZE_TRANSITION_SURFACES_BEFORE_CUBATURE`

Validation passed: `true`.

This is a real topology preflight rather than an angular integral. A global
transport is accepted only if both path order and cycle signatures are
single-valued on the tested grid. Otherwise the transition cells must be
localized and integrated chamber by chamber. No phase-space coefficient,
numeric UV value, local GR, or full MTS claim follows.

The reciprocal root transport itself is path-independent on all tested cells.
The piecewise structure comes from causal cycle occupation, not from an
ambiguous root branch. The E040 and E020 occupation atlases agree exactly on
the complete preflight grid, so one shared transition geometry can be
localized before evaluating regulator-dependent amplitudes.

## Next derivation

If transition cells are present, bisect their exact reciprocal-pair boundaries
in the relevant angular coordinate at fixed energy witnesses, continue those
boundaries over energy, and construct topology-uniform angular panels. If no
transition cells are present, evaluate nested angular orders 3 and 5 with the
checkpoint-5268 energy rule before raising quadrature order.

## Artifacts

- Runner: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\scripts\Y5_R2FR_5269_joint_angular_energy_first_topology_preflight.py`
- Result: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\functional_rg\5269\joint_angular_energy_first_preflight_result.json`
- Angular nodes: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\functional_rg\5269\joint_angular_nodes.csv`
- Path closure: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\functional_rg\5269\angular_path_closure.csv`
- Energy tracks: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\functional_rg\5269\energy_track_atlas.csv`
- Cycle states: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\functional_rg\5269\energy_cycle_state_atlas.csv`
- Transition atlas: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\functional_rg\5269\angular_transition_edges.csv`
- Validation: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\functional_rg\5269\joint_angular_energy_first_validation.csv`
