# 5350: D4 E0025 read-only affine holdout preregistration

## Purpose

Checkpoint 5350 freezes the `epsilon = 0.0025` coefficient as a read-only
holdout before any accepted `E0025` all-eight coefficient exists. It tests the
finite-rung affine relation found at checkpoint 5349 without fitting that
relation to the holdout.

## Frozen predictions

The three prediction disks are written to
`source-intake/functional_rg/5350/E0025/D4_E0025_affine_holdout_predictions.csv`:

| Prediction | Centre | Radius |
|---|---:|---:|
| `WIDE_BRACKET_2H_8H` | `0.0007552290705173516 + 0.47073642746553424 i` | `2.382240221513515e-06` |
| `SMALL_EXTRAPOLATION_H_2H` | `0.0007629069471950874 + 0.4707367913879382 i` | `1.7675221898366594e-05` |
| `OUTER_BRACKET_H_8H` | `0.0007530353914665701 + 0.47073632348770456 i` | `3.2049883047184277e-06` |

The frozen acceptance rule is

```text
abs(A_E0025 - A_prediction)
    <= r_E0025 + r_prediction
```

for all three predictions. No prediction may be changed after observing the
`E0025` coefficient.

## Provenance boundary

The current E0025 event, candidate, contract, pole, scan and fixed-rung source
files are independently revalidated and source-current. A recursive historical
sweep also exposes three older defects rather than concealing them:

```text
stale scripts/Y5_R2FR_5297_order8_exact_component_singularity_atlas.py;
stale source-intake/functional_rg/5297/order8_exact_component_atlas_result.json;
malformed source-intake/functional_rg/5224/frozen_replacement_config.json.
```

Therefore this checkpoint uses the current revalidated event chain, not the
broken deep historical chain. It does not claim complete historical provenance.

## Claim boundary

True:

```text
valid_for_D4_outer_E0025_event_geometry;
valid_for_D4_E0025_affine_holdout_preregistration.
```

False:

```text
valid_for_D4_four_regulator_affine_endpoint_coefficient_holdout;
valid_for_D4_endpoint_coefficient_regulator_zero_limit;
valid_for_D4_outer_regulator_zero_limit;
valid_for_decay_angle_integral;
valid_for_full_angular_convergence;
valid_for_full_phase_space_coefficient;
valid_for_numeric_UV_claim;
valid_for_local_GR_claim;
valid_for_full_MTS_claim.
```

No GitHub action is taken.
