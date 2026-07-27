# 5083 - owned g2 local Cauchy zero certificate

Marker: `MTS_5083_OWNED_G2_LOCAL_CAUCHY_ZERO_CERTIFICATE`.

The first failed fresh-pilot row is resolved locally rather than by restoring
the overbroad checkpoint-5041 theorem. For `S507602_N0000`, `E040_A00`,
chamber 0, the collision is between owned `direct:g2:minus_v` and unowned
`subtraction:decay:plus_v` at a nonzero relative root.

Write the finite-plus integrand as `I=D+S`. A local global-variable cycle can
be chosen around only the transported `direct:g2` pole cluster. The
subtraction term is holomorphic on that cycle, while the audited separation
from every other direct pole keeps the direct residue `R_D(q)` holomorphic
through the cross-source collision. Because the collision point satisfies
`q0 != 0`,

`Res_q[R_D(q)/q] = 0`.

A 70-digit independent Cauchy witness suppresses the measured iterated
residue from approximately `1.435e-19` to `2.190e-24` when the local radius
is halved; the ratio follows the expected `2^16` scaling and is insensitive
to the enclosing global radius. The topology constructor is therefore not
the source of this row's instability.

## Evidence

- Certificate: `source-intake/functional_rg/5083/owned_g2_local_cauchy_zero_certificate.json`
- Witness: `source-intake/functional_rg/5083/owned_g2_arbitrary_precision_witness.json`
- Generator: `scripts/Y5_R2FR_5083_owned_g2_local_cauchy_zero_certificate.py`
- Validation: `source-intake/mts_residuals/P8_Y5_BRR545_5083_VALIDATION.csv`

This is an event-local zero certificate. It neither reinstates the broad 5041
claim nor establishes a general `g2`, production-`hhh`, local-GR, or MTS
result.
