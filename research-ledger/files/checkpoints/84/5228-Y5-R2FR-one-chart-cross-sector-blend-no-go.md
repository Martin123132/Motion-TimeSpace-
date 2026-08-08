# 5228 - One-chart cross-sector blend no-go

## Result

Checkpoint 5227 did not merely find an unlucky coefficient. It exposed a
soft-boundary obstruction to the whole constant-mixture shortcut.

Decision:
`REJECT_NONZERO_CONSTANT_CROSS_SECTOR_MIXTURES_IN_ONE_SOFT_CHART`.

## Derivation

Take the slot-1 soft boundary `E1=lambda->0` while `E2,E3=O(1)`. For

`wi = Ei^-2 / sum_j Ej^-2`,

the weights obey

`w1=1+O(lambda^2)`, `w3=lambda^2/E3^2+O(lambda^4)`.

The crossed `hhh` reduced product has the gravitational soft scaling
`A_hhh=O(lambda^-2)`. The original slot-3 sector factor therefore gives

`3 w3 A_hhh = O(1)`.

For the constant mixture

`W_beta=3[(1-beta)w3+beta w1]`,

every constant `beta != 0` instead gives

`W_beta A_hhh = O(lambda^-2)`.

Since the massless phase-space measure contains `lambda d lambda`, its
absolute mean has the logarithmic boundary `d lambda/lambda`, and its
second moment is stronger still, `d lambda/lambda^3`. A native slot-1
subtraction/chart can regulate that sector; inserting it into the slot-3
one-soft chart cannot.

## Machine check

On a fixed physical geometry, fitting the smallest four `lambda` values
gave:

- `A_hhh` slope: `-2.00241126`;
- original `3 w3 A_hhh` slope: `-0.00107864031`;
- paired `3(w3+w1)A_hhh/2` slope: `-2.0024137`;
- `lambda^2 |A_hhh|` plateau ratio: `1.00853761`.

This explains the checkpoint-5227 variance ratios of
`4.05545962` at A00
and `1.88662303`
after local projection.

## Consequence

The full-S3 pointwise shortcut `w1+w2+w3=1` is also excluded in this
one-soft chart: algebraic cancellation of the partition denominator would
simultaneously remove the off-sector soft suppression.

The admissible route is now narrower and clearer:

1. preserve each sector's native `O(lambda^2)` suppression;
2. use independent native-chart stratification for immediate variance
   reduction; or
3. build the full correlated `T13` pullback, including transformed outer
   coordinates, relative azimuth, Jacobian and every plus-boundary term,
   before transporting complex topology.

This closes a shortcut class; it does not close the ultraviolet coefficient.

## Claim boundary

No numerical UV coefficient, local-GR result, galaxy result, or full-MTS
claim follows. The result is an estimator-admissibility theorem.

## Evidence

- Scaling rows: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\functional_rg\5228\cross_sector_soft_boundary_scaling.csv`
- Result: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\functional_rg\5228\one_chart_cross_sector_blend_no_go.json`
- Validation: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_5228_VALIDATION.csv`
