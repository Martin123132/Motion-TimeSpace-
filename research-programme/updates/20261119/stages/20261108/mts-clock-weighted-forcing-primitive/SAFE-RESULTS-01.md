# Verified progress: clock-weighted forcing transformation

2026-11-08. This is a SAFE PARTIAL checkpoint, not completion of the planned three-family control matrix. The broader MTS objective remains active. Accepted closed physical parent: ../mts-original-mode-reference-completion-20261108, seal cca27f5d3d015605ec05fbf07cde372dfcfe2c73c7035da915761ee021473b12.

## Derived, not fitted

For the complete retained source f=sum B_j F_j, derive clock-weighted scalar kernels K_j with
    Omega partial_theta K_j=B_j-mu_j,   mean_clock K_j=0.
Then J=sum K_j F_j and the exact transformed response is
    eta_N=M eta+fbar+M J-J_N,   delta=eta+J.
The incoming condition eta=-J preserves the original zero local increment and hence the unchanged inherited physical mode. Both the kernel derivative and complete source-history derivative are retained.

The moving physical clock adds a nonzero correction to the mean drive:
    mean_clock(M J-J_N)=-mean_clock((Omega_N/Omega)J).
This follows by differentiating the primitive's clock-weighted normalization; it is not a fitted coefficient. DERIVATION.md and MOVING-CLOCK-MEAN.md give the derivation and scope.

## Verified evidence

- All three wavenumbers pass paired source/derivative identity checks for MTS and baseline.
- Fixed-N all-phase clock bound is positive; the smallest bound at the 65 tested nodes is 2765.526062747708. Invariant-map bound is at most .0005423546437212156 within the retained .02 box, and contraction bound at most .00006291610055696879.
- Primitive/clock-normalization identities are at the 1.58e-15 level. Independent phase quadrature and fixed-phase derivative checks pass.
- The COMPLETE original finite real forcing is retained, including both Nyquist terms. Auxiliary scalar kernels use 65 versus33 N nodes and513 versus1025 phase quadrature; the original physical/source banks, thermal histories and grids are untouched.
- Fourteen of18 response jobs are complete. Half and balanced wavelengths have ALL paired fine/time/kernel controls plus physical readouts and residual diagnosis. Double wavelength has its paired fine runs complete; four control runs and postprocessing remain.
- Fine MTS corrections agree with their saved direct response to at worst 7.718329358746032e-13 relative. Baseline fine and auxiliary-source-control responses reproduce the saved fine result exactly in the tested arrays.
- Worst correction-relative regression among completed fine/coarse jobs is 2.2405678407495415e-12. All unchanged numerical gates pass. The completed physical comparisons remain at the same errors against the original full-equation references (worst2.072881286154049e-6); no claim of improved observational fit is made.

| Wavenumber | Gravity branch | Fine correction-relative regression |
|---|---|---:|
| half | gr | 7.171989407e-13 |
| half | poisson-spatial | 6.125922427e-14 |
| balanced | gr | 7.035690215e-13 |
| balanced | poisson-spatial | 2.468853856e-13 |
| double | gr | 7.608197074e-13 |
| double | poisson-spatial | 7.718329359e-13 |

## Does it help the fast forcing?

At the three diagnosed epochs in each COMPLETED half/balanced case, compare clock-weighted RMS after removing the corresponding mean. The remaining-to-original oscillatory ratios are:
- GR normal-form source: .00843117–.02701633, approximately97–99percent reduction.
- Spatial-Poisson normal-form source: .07895928–.17365413, approximately83–92percent reduction.
- Coordinate-map source: .000660497–.000806435, more than99.9percent reduction.

The derived moving-clock mean identity passes independently through these physical vectors (worst5.9615e-16, normalized to the residual scale). Every remaining oscillatory term is still INCLUDED in the response evolution. These measurements concern finite saved source directions and epochs, not a uniform operator/gain bound.

No runtime speedup is claimed: this check deliberately keeps the original time-step caps while evaluating additional kernels. The purpose is to validate the derived transformation before justifying any longer or faster slow evolution.

## Evidence and boundaries

progress-audit-01/result.json independently checks provenance, every completed direct-response regression and completed physical-channel result; it explicitly sets full_planned_stage_complete=false and lists pending jobs. Individual result/freeze files preserve source hashes, parameters and predictions before comparison. SAFE-CHECKPOINT-01.json/SAFE-CLEANUP-01.json provide final readback and process-exit receipts; closeout.json is intentionally absent.

f_N here is the exact derivative of the accepted retained forcing interpolant, not a new independent microscopic R_N derivation. The original nine-node source interpolation uncertainty, first-response truncation R delta and reconstructed-background mismatch remain inherited. The positive clock proof is uniform in phase at the queried N, not an asserted enclosure of every unsampled N. No fitted parameter, new initial mode, physical bank, tolerance or public repository was changed.

The dispatcher stopped BEFORE launching the next job because the remaining reserve did not fit the four-hour session. This is a deliberate safe handover, not a scientific failure or failed-run retry. All29 tracked Python invocations finished successfully; no numerical worker remains. Earlier research and the original ladder remain intact.
