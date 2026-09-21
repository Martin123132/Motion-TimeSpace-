# Computed source-acceleration comparisons

All values retain the candidate normalization. These are not assigned SI accelerations.
The same phase points and action are retained in the wider-probe repeat. Both estimates remain visible.

| Branch | Phase / probes | Center proper acceleration | Center geodesic comparator | Weighted relative residual |
| --- | --- | ---: | ---: | ---: |
| reference | initial | -0.0193127320859 | -0.0193127264795 | 2.5748e-06 |
| reference | endpoint | -0.0193130712838 | -0.0193127245662 | 1.84939e-05 |
| primary | initial | -0.0193127132602 | -0.0193127264796 | 2.66144e-06 |
| primary | endpoint | -0.0193130477837 | -0.0193127245647 | 1.72826e-05 |
| alternative | initial | -0.0193127132592 | -0.0193127264796 | 2.66149e-06 |
| alternative | endpoint | -0.0193130485013 | -0.0193127245647 | 1.732e-05 |
| reference | endpoint-wide | -0.0193130956087 | -0.0193127245657 | 1.97691e-05 |
| primary | endpoint-wide | -0.0193130721161 | -0.0193127245656 | 1.85465e-05 |
| alternative | endpoint-wide | -0.0193130728265 | -0.0193127245656 | 1.85843e-05 |

## Derivative sensitivity

| Branch | Phase / probes | Weighted geodesic residual | Weighted derivative-estimate change |
| --- | --- | ---: | ---: |
| reference | initial | 4.97264e-08 | 5.70417e-08 |
| reference | endpoint | 3.57167e-07 | 5.7748e-08 |
| primary | initial | 5.13997e-08 | 5.7041e-08 |
| primary | endpoint | 3.33775e-07 | 5.7748e-08 |
| alternative | initial | 5.14006e-08 | 5.70423e-08 |
| alternative | endpoint | 3.34496e-07 | 5.77472e-08 |
| reference | endpoint-wide | 3.81796e-07 | 5.28831e-13 |
| primary | endpoint-wide | 3.58184e-07 | 3.89671e-13 |
| alternative | endpoint-wide | 3.58914e-07 | 4.34581e-13 |

Derivative-estimate changes are observed numerical diagnostics, not rigorous error bounds.
A numerical residual is not by itself a physical deviation from GR.

## Source reaction and moving-anchor traction

Norms below are for the same15-component material covector basis, not invariant physical-force norms.
The bulk traction comparison leaves Gram and finite-element field-equation terms unseparated.

| Branch | Phase / probes | Non-dust reaction / dust-force norm | Reaction minus bulk traction / dust-force norm | Remainder / raw reaction |
| --- | --- | ---: | ---: | ---: |
| reference | initial | 1.64912e-06 | 1.64912e-06 | 1 |
| reference | endpoint | 1.95002e-05 | 2.44559e-07 | 0.0125414 |
| primary | initial | 6.78496e-07 | 6.78496e-07 | 1 |
| primary | endpoint | 1.82835e-05 | 3.80839e-07 | 0.0208297 |
| alternative | initial | 6.78514e-07 | 6.78514e-07 | 1 |
| alternative | endpoint | 1.83208e-05 | 2.18701e-07 | 0.0119373 |
| reference | endpoint-wide | 1.95002e-05 | 2.44522e-07 | 0.0125395 |
| primary | endpoint-wide | 1.82836e-05 | 3.8075e-07 | 0.0208247 |
| alternative | endpoint-wide | 1.83209e-05 | 2.18653e-07 | 0.0119346 |

## Inverse-root differentiation audit

The first postflight failed the original raw2e-6 dust-force-normalized closure gate at the reference endpoint.
That failure and the same raw gate are preserved for every branch. The discrepancy is reconstructed from
the derivative of computed minus target canonical momentum, not removed by loosening a threshold.
Root-corrected and target-owned reactions are accounting identities, not independent evidence of physical agreement.
The wider-probe raw comparison passes the original gate for all three endpoint branches.

| Branch | Phase / probes | Raw closure / dust force | Root derivative / dust force | Original raw gate |
| --- | --- | ---: | ---: | --- |
| reference | initial | 1.99857e-06 | 1.99857e-06 | True |
| reference | endpoint | 2.02219e-06 | 2.02219e-06 | False |
| primary | initial | 1.99854e-06 | 1.99854e-06 | True |
| primary | endpoint | 2.02214e-06 | 2.02214e-06 | False |
| alternative | initial | 1.99856e-06 | 1.99856e-06 | True |
| alternative | endpoint | 2.02216e-06 | 2.02216e-06 | False |
| reference | endpoint-wide | 3.91482e-09 | 3.91482e-09 | True |
| primary | endpoint-wide | 3.91141e-09 | 3.91141e-09 | True |
| alternative | endpoint-wide | 3.9119e-09 | 3.9119e-09 | True |

Source: the final integrity manifest and its source-linked CSV tables. The parent derivation states assumptions and equations.
