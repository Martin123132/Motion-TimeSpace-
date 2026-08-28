# 5354: D4 E0025 four-regulator affine holdout gate

## Purpose

Checkpoint 5354 compares the accepted E0025 coefficient with all three
checkpoint-5350 predictions. The E0025 value is not used to refit any
prediction, weight or uncertainty.

## Holdout result

For each prediction the contrast disk has centre
`A_E0025 - A_prediction` and radius `r_E0025 + r_prediction`.

| Prediction | Contrast magnitude | Disk radius | Ratio | Margin | Contains zero |
|---|---:|---:|---:|---:|---:|
| `WIDE_BRACKET_2H_8H` | `1.7329102226267593e-06` | `3.1701841262065464e-06` | `0.5466276259165949` | `1.4372739035797871e-06` | yes |
| `SMALL_EXTRAPOLATION_H_2H` | `9.364828628887781e-06` | `1.8463165803059625e-05` | `0.5072168407508905` | `9.098337174171845e-06` | yes |
| `OUTER_BRACKET_H_8H` | `7.123907252266061e-07` | `3.9929322094114596e-06` | `0.17841292760930927` | `3.2805414841848534e-06` | yes |

All three preregistered contrast disks contain zero. The maximum radius ratio
is `0.5466276259165949`, so none is a marginal boundary contact.

## What this establishes

The independent fourth coefficient is compatible with the finite-regulator
affine relation inferred from `E000625`, `E00125` and `E005`. This is a genuine
read-only holdout pass and strengthens the evidence that the leading E0025
coefficient is regulator-stable over the sampled range.

It does not prove that `epsilon -> 0` exists, that the affine law continues
outside the four sampled rungs, or that the endpoint coefficient has its
claimed physical normalization.

## Provenance boundary

The current baseline, preregistration, branch refinement and all-eight source
chains are hash-current. The three older historical E0025 defects recorded at
checkpoint 5350 remain disclosed; this result relies on the independently
revalidated current event contracts rather than pretending those historical
files are current.

## Claim boundary and next gate

The only new true claim is

```text
valid_for_D4_four_regulator_affine_endpoint_coefficient_holdout.
```

The regulator-zero, decay-angle, full phase-space, numerical UV, local-GR and
full-MTS claims remain false. The next admissible regulator-zero route is

```text
SOURCE_DERIVED_REMAINDER_BOUND_OR_TWO_ADDITIONAL_REGULATOR_RUNGS
```

because four finite rungs alone do not supply a uniform remainder theorem.

No GitHub action is taken.
