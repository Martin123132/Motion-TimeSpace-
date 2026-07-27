# 5091 - E040/A11 coarse multi-double-zero certificate

Marker: `MTS_5091_E040_A11_COARSE_MULTI_DOUBLE_ZERO_CERTIFICATE`.

The v7 pilot stopped at `E040__S507603_N0000__A11__coarse12` because the
5085 multidirection limit returned convergence `7.25e-7` and direction spread
`3.09e-7`, above the unchanged `1e-7` gate. This was not resolved by widening
that gate.

The `direct:g2:plus_u/plus_v` equation has two algebraic collision roots:

- `q0=-0.0491433095245+0.000157896170678 i`, with root-split magnitude
  `11384.8059913`;
- `q1=-20.34843983-0.0653790060033 i`, with root-split magnitude
  `0.00495187532458`.

Their collision residuals are `3.34e-13` and `1.23e-14`. At each root the
pair-regularized form `H=(w-u)(w-v)I/w` has vanishing constant and linear
terms, a stable quadratic term, and zero local Cauchy residue. Both possible
owned residues obey `Res=C_j(q-q_j)+O((q-q_j)^2)`.

The residue audit uses a smaller asymptotic ladder
`(2e-4,1e-4,5e-5)` and `192/384` nodes. This changes the sampled distance and
resolution, not any acceptance tolerance. Both roots and both ownerships pass.

The exact multi-root guard recomputes the formerly blocked coarse event with
six calls at `q1`, no 5085 numerical fallback, stable residues, and residual
`4.6686866473304254e-4`. The actual v8 runner replay also converges, with
residual `4.219245118548192e-4`.

## Evidence

- Certificate: `source-intake/functional_rg/5091/E040_A11_coarse_multi_double_zero_certificate.json`
- Standalone gate: `source-intake/functional_rg/5091/E040_A11_coarse12_exact_collision_gate.json`
- Generator and reusable guard: `scripts/Y5_R2FR_5091_E040_A11_coarse_multi_double_zero_certificate.py`
- Validation: `source-intake/mts_residuals/P8_Y5_BRR545_5091_VALIDATION.csv`
- Production replay: `source-intake/functional_rg/5079/runs/bounded_central_anchor_pilot_v8/jobs/E040__S507603_N0000__A11__coarse12.json`

This is a row-local contour result. It is not a production `hhh`, GR, Newton,
or full-MTS claim.
