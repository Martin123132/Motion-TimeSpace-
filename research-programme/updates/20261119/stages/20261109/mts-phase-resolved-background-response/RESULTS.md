# First-cell phase-resolved background response

## Result

The first original cell now has a directly evaluated background-source contribution to the existing final saved epoch. This replaces the previously rejected wide-cell time cubic with evaluations of the original native equations at frozen phase-resolved points. Baseline and MTS use the same preparation, bank, hierarchy, physical grids and numerical gates. This is the balanced wave family, both GR and spatial-Poisson metric branches; it does not silently cover the other families or remaining cells.

The recovered coarse batch, nested129/257-point extensions, two response projections and independent audit are saved. The crash did not require repeating a completed source point. Audit-02 passes all structural, algebraic, provenance and reproduction checks. Numerical convergence flags below are separate from that audit pass.

## What was calculated

The source is E_bg y_c, with E_bg=T^-1(F_ref-F_ret)T and y_c the saved mean-plus-slow-plus-periodic-plus-feedback approximation. The difference is WITHIN each model, comparing its reference and retained backgrounds. It is not MTS-minus-baseline and not an observational fit.

The final-output contribution is integral_cell lambda^T E_bg y_c dN, using the existing source-independent adjoint. MTS integrates in physical phase; baseline stays in N because it has no heavy phase. Native rates use each background's own conformal H. Source evaluations reconstruct the original256-angle endpoint, not a fitted time interpolant. The same-state final output-map difference remains a separate term.

Four dense current histories reproduce the saved original modes to about1.8e-15 of their initial-state scale. Frozen257-point panels reuse the65/129-point subsets. The514 final source points and514 paired phase controls retain both metric branches and the full hierarchy. The exact current/phase comparison includes all three terms E_f Delta y, Delta E y_f, Delta E Delta y.

## Quantitative outcome

All fractions below use the pre-existing per-channel reference scales stored in the accepted feedback comparison; they are not a percent change in a new cosmological observable or a new data-fit score.

| Quantity | MTS | Baseline |
|---|---:|---:|
| Largest absolute signed contribution / reference scale | 2.633902171154364e-7 | 5.167006642406829e-14 |
| Largest numerical Cauchy budget / reference scale | 2.635115885832027e-7 | 5.207520785467507e-14 |
| Fine numerical passes, out of20 branch/channel cases | 10 | 0 |
| Maximum129-to257 signed integration change / component budget | 8.927172429438069e-5 | 8.711999036701208e-2 |
| Maximum129-to257 budget change / component budget | 1.383024104751297e-4 | 7.337216218032036e-2 |
| Largest measured signed integration change / reference scale | 1.305801116367674e-12 | 1.478631181400251e-16 |

The MTS dominant contribution is approximately0.26339ppm of its existing reference scale. Phi, Psi, D, Q and theta_c pass every defined control in both metric branches at the unchanged2e-5 gate. Pi, delta_c, delta_b, delta_gamma and delta_massless retain integration/budget-refinement flags in both branches. The middle panel had8/20 MTS passes; the finer panel has10/20. Refinement is not yet a demonstrated asymptotic convergence law for all channels.

The baseline contribution is tiny on the original physical scales, but its source-relative integration controls remain unresolved. We neither set it to zero nor relax its acceptance rule. Measured refinement changes are diagnostics, not rigorous error enclosures.

## Separate controls

All current-history, source-phase, cross-term, adjoint-interpolation, adjoint-step and clock-measure controls pass for both models. The largest MTS source-phase change / component budget is2.245087971334982e-6; current-history control is3.187606762129537e-15; adjoint interpolation is3.362323262142451e-11. The largest phase-control change on the inherited physical scale is3.171308624145088e-15. This directs the next effort toward the source integral, rather than another blind current-history timestep reduction.

The saved MTS phase polynomial is strictly monotone: exact rational Bernstein checks on all555 stored pieces bound its derivative between2773.536004045926 and2824.828226171617 perN. The baseline741 pieces have exactly zero phase derivative and are not inverted. This certifies the represented polynomial, not the continuous physical solution. Physical-clock versus stored-polynomial rate differences at the sampled nodes are at most8.056e-13 relatively; the measured phase-volume error is2.756e-11.

The independent audit reconstructs the moving-map and source identities from saved matrices and native rates. Maximum relative residuals are6.113e-16 for the fine source and6.172e-16 for its phase control, below the unchanged1e-10 algebra gate. Original primitive refinement and closure diagnostics are at most4.091e-13 and2.517e-13. All saved adjoint projections reproduce exactly in the audit. Counts:4 histories,514 source points,514 phase controls,80 projection rows across the middle/fine comparisons.

## Interpretation and retained terms

This is a calculated first-cell contribution, not merely a missing-input list. The dominant gravitational outputs now have a numerically qualified source integral. Smaller channels still retain explicit strict-integration flags. A Cauchy expression evaluated by quadrature is a conditional numerical budget, not a certified continuous-time bound.

The rest of the original interval, other wavelength families, final output-map mismatch, D_bridge, E_bg v, R v, inherited errors and older source-interpolation uncertainty must remain in the total response. No full-trajectory correction is manufactured by adding this first-cell number alone. No new fit, coupling or observational data were introduced.

## Evidence and recovery

Authoritative local files: balanced/projection-fine-02/result.json, balanced/projection-middle-02/result.json, balanced/points-01/fine-02-result.json, audit-02/result.json, DERIVATION.md, NEXT.md and closeout.json after sealing. These paths are relative to this document's directory. Source paths and hashes are in their manifests.

The first audit exposed an audit-only compact-layout padding mistake; AUDIT-REPAIR.md preserves the diagnosis. The original source calculations were not rerun or modified. audit-01 failed; audit-02 is the accepted independent verifier. RECOVERY.md preserves the app-crash recovery receipt. Final process cleanup and all artifact hashes are recorded by the sealer. Everything remains local.
