# 5088 - exact same-source double-zero collision certificate

Marker: `MTS_5088_EXACT_SAME_SOURCE_DOUBLE_ZERO_COLLISION_CERTIFICATE`.

The `direct:g2:plus_u/plus_v` obstruction at `E020/A07` is not a genuine
pinch. Write the global contour form and its pair-regularized numerator as

`G(q,w)=I(q,w)/w`,

`H(q,w)=(w-u(q))(w-v(q))G(q,w)`.

At

`q0 = -0.001018098889384383 + 0.002734237261662615 i`,

the two roots meet at

`w0 = -23.0774857152861 + 1.5313685545231042 i`.

The collision residual is `3.45e-14`, the equivalent kinematic condition
`n_z=z` holds to `9.65e-15`, and the analytically differentiated root split is

`u'(q0)-v'(q0) = -331.52617953425755 + 66.95595517555924 i`,

with nonzero magnitude `338.2199101916566`.

Three local Cauchy radii and two node orders show that `H` has no constant or
linear local term. The worst constant/quadratic, linear/quadratic, and local
residue ratios are respectively `2.71e-7`, `5.55e-8`, and `5.55e-8`; the
quadratic coefficient and finite Cauchy center agree to `4.26e-15`.

Both adjacent chamber choices were then tested independently. Their selected
residues obey

`Res_plus_u = (30.5926080832 + 25.9110158273 i)(q-q0) + O((q-q0)^2)`,

`Res_plus_v = (-49.8516470676 - 30.6377257090 i)(q-q0) + O((q-q0)^2)`.

The coefficient spreads are `9.73e-4` and `1.00e-3`; half-step contraction
errors are below `2.60e-4`. Therefore each uniquely owned residue has exact
collision limit zero. No principal value, half residue, or fitted plateau is
inserted. The certified treatment removes only this silent pair at `q0` and
retains every other global residue.

The formerly blocked fixed-event gate then converges with residual
`6.66736793604562e-6`, all residues stable, and two adjacent-chamber guard
calls.

## Evidence

- Certificate: `source-intake/functional_rg/5088/exact_same_source_double_zero_collision_certificate.json`
- Recomputed gate: `source-intake/functional_rg/5088/E020_A07_primary24_exact_collision_gate.json`
- Generator: `scripts/Y5_R2FR_5088_exact_same_source_double_zero_collision_certificate.py`
- Validation: `source-intake/mts_residuals/P8_Y5_BRR545_5088_VALIDATION.csv`

This is a row-local contour theorem and does not establish a production `hhh`,
GR, Newton, or full-MTS result.
