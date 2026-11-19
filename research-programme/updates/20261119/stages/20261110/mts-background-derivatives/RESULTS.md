# The changing background is derived, evolved and checked

2026-11-10. This extends the retained forced state map using the actual
cosmological background equations. It does not restart the theory, refit a
coupling, or replace the late matching prescription.

## Physical result

The conformal derivatives H',H'',H''' are now explicit functions of total
background stress and its species equations. Scalar, dust, radiation and
massive-neutrino contributions are retained. No float32 metric derivative
is used as their source. Substitution gives a particularly simple carrier
frequency correction:

    W20=mu+3P/(8mu),    P=a^2 p_total/M_Pl^2.

Thus this correction is pressure-sourced. Exact dust makes it vanish;
radiation and a rolling field contribute with their physical pressure signs.
The finite-k formula and a cancellation-safe beat-frequency expression are
derived in PRESSURE-BRIDGE.md. The existing flat Einstein sector is used;
this is not a new derivation of G or of that sector from a deeper unknown action.

In the saved z=10 interval, H'/H^2 runs from about-0.4983353 to-0.4983249.
The homogeneous correction is only0.33294%-0.33503% of the earlier frozen-H
test value. That is a correction to a specific small frequency term, not a
300-fold observational improvement. Both models have almost the same late
homogeneous expansion here, as expected from their retained matter budgets.

## Real saved background, independently evolved

The interval is ln(a/a_center) in[0,.001], a_center=1/11, using the existing
matched-heavy and cold tables. The slow field, conformal expansion and
elapsed conformal time were evolved from the initial slice with the derived
Raychaudhuri equation, not reanchored to later saved H values.

| Check | Heavy | Cold |
|---|---:|---:|
| Friedmann constraint discrepancy | 6.67e-16 | 6.67e-16 |
| Saved slow-field state, fixed initial scales | 4.601e-13 | 4.604e-13 |
| Reconstructed versus native H,399x7rows | 2.23e-16 | 2.23e-16 |
| Saved conformal interval | 7.25e-14 | 6.91e-14 |
| Background solver-tolerance comparison | 1.139e-15 | 5.695e-16 |

The solver runs each used62evaluations, so the small tolerance difference
alone is not evidence of convergence order. Independent constraints, native
clock/state comparisons and derivative checks provide separate controls.
Finite-difference spot checks of the independently evolved trajectory test
H',H'',H''' at three positions and two spacings; they are validation only,
not the derivative source. All checks satisfy the unchanged gates.

The massive-neutrino derivatives use the original StandardSpecies smooth
background interpolation. Its native generation and parameters are reused;
no perturbation spectrum or shooting fit was rerun. Its kinetic/tabulation
accuracy is inherited, not newly proven. There are no neutrino spline knots
inside this particular interval, although future intervals must check them.

## Prepared physical history

For each model, heavy-history.npz/cold-history.npz preserve all399modes
at seven surrounding original knots. All2793raw rows per model match the
original source packets byte-for-byte as numerical arrays. Fields include
the distinct potentials, physical density/current, actual and requested
scales, original conformal times, and their existing transfer-rounding radii.
No missing fast phase or full late-hierarchy restart is invented.

The metric is genuinely changing: maximum endpoint Phi/Psi changes on the
fixed window-amplitude norm are about2.444e-4 for heavy and5.704e-6 for cold.
These are saved transfer-history changes, not observational gains. The packet
is ready for a changing-source propagation rather than a frozen-metric probe.

## Residual diagnostic and its limits

The general W2 residual was symbolically cancelled to a91-term rational
numerator retaining H',H'',H'''. At33fixed positions and all399wave numbers,
the largest heavy sampled |R_W|/W is1.491e-28 inverse Mpc. Nine60-digit
controls per model agree with the stable binary64 expression on the declared
fourth-order scale; maximum heavy discrepancy there is1.723e-15.

This is a sampled diagnostic, NOT a certified integral enclosure. The
constant-H certificate does not apply to this background. The cold WKB
numbers are a same-test-mass geometric diagnostic only: no heavy scalar
or quantum pressure has been inserted into cold matter.

There are14exact identities. The142preparation check entries include packet
coverage/clock checks as well as physical tests; they are not142independent
physical discoveries. The independent validator also checks raw-array
preservation and the pressure reformulation. No failed attempt was discarded.

## Next

Derive a true variable-background residual enclosure and carry the saved
changing Phi/Psi through the existing canonical source action. Compare
physical field evolution and the retained source readout on this same real
interval, with the cold Euler control and input-precision allowances. Keep
the prepared packet, rather than regenerating the full cosmology. The current
stage has evolved the background, not yet the forced perturbations.
