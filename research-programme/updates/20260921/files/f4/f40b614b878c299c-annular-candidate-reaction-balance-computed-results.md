# Full source-reaction decomposition

All values use the inherited normalization and the same15-component material covector basis.
Norms of separate contributions do not add; the vector sum is evaluated before its norm.
Initial small reactions remain derivative-sensitive. Endpoint rows use wider probes.

| Branch | Phase | Order | Boundary-only remainder / reaction | Full remainder / reaction |
| --- | --- | ---: | ---: | ---: |
| reference | initial | 16 | 1 | 0.0001271383 |
| reference | initial | 32 | 1 | 0.0001271442 |
| reference | endpoint-wide | 16 | 0.01253948 | 4.290392e-07 |
| reference | endpoint-wide | 32 | 0.01253948 | 4.291093e-07 |
| primary | initial | 16 | 1 | 0.0003233393 |
| primary | initial | 32 | 1 | 0.0003233328 |
| primary | endpoint-wide | 16 | 0.02082471 | 9.629216e-07 |
| primary | endpoint-wide | 32 | 0.02082471 | 9.629711e-07 |
| alternative | initial | 16 | 1 | 0.000331589 |
| alternative | initial | 32 | 1 | 0.0003316108 |
| alternative | endpoint-wide | 16 | 0.01193464 | 8.56885e-07 |
| alternative | endpoint-wide | 32 | 0.01193464 | 8.568684e-07 |

## Contributions at reference order32

| Branch | Phase | Anchor norm | Internal jump norm | Cell field EL norm | Gram source norm | Full remainder |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| reference | initial | 5.366912e-18 | 1.447661e-08 | 1.409211e-08 | 0 | 4.89147e-14 |
| reference | endpoint-wide | 4.605984e-09 | 1.457048e-08 | 1.46274e-08 | 0 | 1.952084e-15 |
| primary | initial | 5.393919e-18 | 1.447661e-08 | 1.432654e-08 | 7.721648e-12 | 5.117868e-14 |
| primary | endpoint-wide | 4.353647e-09 | 1.436034e-08 | 1.445655e-08 | 7.721144e-12 | 4.107389e-15 |
| alternative | initial | 5.393919e-18 | 1.447661e-08 | 1.432654e-08 | 7.721648e-12 | 5.249034e-14 |
| alternative | endpoint-wide | 4.324159e-09 | 1.438212e-08 | 1.444016e-08 | 7.721144e-12 | 3.662281e-15 |

Scientific gates passed: 66/66.
The exact identity and finite-grid numerical validation are distinct from a continuum convergence or parent-action existence theorem.

## Derived force-to-acceleration projection

The positive material metric G integrates m*s/F times the cardinal basis products.
The reconstructed covector includes the separately recorded inverse-root derivative correction.
The last two columns are measured finite-quadrature errors relative to the weighted acceleration-residual norm.

| Branch | Phase | Corrected reconstruction error / residual | Unresolved material projection / residual |
| --- | --- | ---: | ---: |
| reference | initial | 8.640541e-05 | 5.388418e-05 |
| reference | endpoint-wide | 4.883084e-07 | 1.919886e-07 |
| primary | initial | 6.141335e-05 | 5.479764e-05 |
| primary | endpoint-wide | 1.202163e-06 | 2.443695e-07 |
| alternative | initial | 7.716498e-05 | 5.479796e-05 |
| alternative | endpoint-wide | 1.049016e-06 | 2.438658e-07 |
