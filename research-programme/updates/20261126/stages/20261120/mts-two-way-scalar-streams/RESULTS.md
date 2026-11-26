# Both material coordinates and the slow field gravitate on the same spherical solution

Local continuation of the canonical-stream checkpoint, separate from the fixed-occupation LMC comparison. No galaxy data, fitted couplings or catalogue changes. The background, core, positive material labels, endpoints, seven sites and original four signed spans are inherited. All reported errors use actual uncorrected fields; no predicted error was subtracted to obtain a pass.

## Two independent changes

Use a common radial material chart `X=Q+D(Q,t)`, `J=1+D_Q`, `p=s(Q,t)+π/J`. Position and momentum are physical coordinates on the left, material coordinates on the right. The transformation has unit phase-space determinant. Differentiation along a characteristic of physical speed v and force F gives

    Qdot = (v-D_t)/J
    πdot = J(F-s_t-s_Q Qdot) + (π/J)(D_tQ+D_QQ Qdot).

Thus a moving chart with its momentum kick can carry the physical velocity and the physical force even when neither is affine inside an original material element. A finite Galerkin projection error is still possible. The evolving density uses the actual Jacobian, the original positive label weights and the restored physical momentum; the time reconstruction splits pressure quadrature at streams crossing the moving chart image of a fixed physical site.

The canonical slow scalar is evolved with the density, momentum and stresses of the same Hilbert tensor. With local spatial scale ℓ and normal derivative W, its energy is `(W² + φ_r²/ℓ² + m²φ²)/2`, covariant momentum `−Wφ_r`, anisotropy `φ_r²/ℓ²` and radial pressure `(W²+φ_r²/ℓ²−m²φ²)/2`. The constraints receive energy above background, momentum and anisotropy; pressure is tested in the independent trace equation. The source-off control evolves the slow field but does not let it gravitate. Both trials use the same moving chart.

## Outcomes on the original finite interval

At the later slice, with eight outer steps and the uniform slow preparation, switching on feedback reduces the worst four-span trace error from 93.08 to 1.14 ppm (cold) and 141.08 to 3.15 ppm (wave). The corresponding worst on-case kinematic metric errors are 1.85 and 0.31 ppm or smaller. The earlier uniform slice gives at most 3.58 and 14.67 ppm for the four trace differences. These are finite signed differences on fixed scales, not absolute errors at every point.

More discriminatingly, before these integrations the separately propagated tracer predicted the signed change in the trace residual. Against the observed late feedback-on minus feedback-off differences, its maximum error on the small forecast's own scale is 3.47 ppm for cold and 11.45 ppm for the wave (four spans each). The isolated momentum prediction is less accurate: its worst wave span differs by 53.43 ppm on its own scale. A correct overall balance does not make that separate 20 ppm comparison pass.

Embedding the same 99-mode linear formation selection at each actual epoch gives nearly identical span decisions to uniform initial normal data. This conditional embedding is not an integration through the intervening nonlinear formation history. The saved single-precision velocity can cause up to 2.89% uncertainty relative to the reconstructed late cold field perturbation, although its estimated contribution relative to the normal-rate perturbation is below 4×10⁻⁸ there. Do not use small differences between those two preparations as a resolved physical observable. The probe source provided for native double precision is not itself a validated precision repair.

At the original eight steps the worst absolute-site trace errors are 20.51/37.46 ppm or smaller at the late cold/wave slice and 59.42/122.55 ppm or smaller at the early slices. The absolute 20 ppm gate is not passed by the four-span success. The outer FLRW match, remaining radiation/neutrino sources, regularized core, and finite evolution remain explicit conditions. A useful next calculation is to budget these absolute terms from the matched sources without inserting a free spatial offset.

Doubling the late time resolution keeps the worst signed-span trace and metric errors under 3.15 ppm and 1.85 ppm, respectively, across the two branches. Doubling the position-chart resolution instead gives 3.16 ppm and 3.74 ppm. Neither resolves the absolute-site trace discrepancy. The exact transformation passes the symbolic chain-rule and symplectic tests, the finite characteristic comparison agrees to 2.23×10⁻¹⁶, and direct contraction of the stress tensor agrees to 4.17×10⁻¹⁷ on the independent fixture. No fixed-position-chart null was included in this batch: source feedback is isolated by the on/off pair, whereas comparison to the previous material scheme also changes the representation.

## Reuse

Each run keeps its metric, pressure-crossing events, signed scores and final restart. Cases beginning `heavy` also retain the wave charge/energy budget. The final per-run table and both feedback forecasts are machine-readable in the sealed manifest. `finish_batch.py` checks all original input seals and every completed case, then verifies that the local files match that manifest. The initial abandoned subdivision method is documented in RESOURCE-AND-METHOD.md; it generated no result. These spherical field tests are not part of the Milky Way/LMC force-band scores.
