> Public reading copy. Machine-specific or private operational passages are omitted; original and public SHA-256 values are recorded separately.

# Finite-time derived carrier test: saved outcome, 10 November 2026

The first derived phase/background-drift correction has now been propagated from the frozen initial states, rather than merely compared with rates evaluated on a saved solution. The actual cold/CDM baseline and the retained MTS heavy branch were checked on both the 65-node live-history interval and the original 902-node extraction window. Original physical parameters, bank, output grids, signed weights and tolerances are unchanged.

This stage prescribes the saved homogeneous background and rest-species source history. Heavy self-gravity is included in the conditional exact equation. The reduced forward channels receive neither the comparator's heavy perturbations nor its diagnostic defect response. This is a conditional propagation test, not the completed all-species feedback implementation. Twelve channel-independence mutation checks pass.

## Physical result

Errors below are dimensionless history-peak-normalized errors, not observational percentages or per-epoch relative errors at zero crossings. The physical comparison tolerance is 2e-5. Live results use dense-step2; extraction uses dense-step2-segmented after the numerical diagnostic repair described below.

| MTS comparison | 65-node interval | 902-node extraction |
|---|---:|---:|
| Reduced primitive field | 4.61053e-7 | 5.29593e-7 |
| Reduced primitive velocity | 3.63761e-7 | 4.24078e-7 |
| Reduced density source | 2.69333e-6 | 2.98469e-6 |
| Reduced current source | 3.20951e-7 | 3.65513e-7 |
| Reduced pressure source | 3.73025e-7 | 4.36837e-7 |

All these comparisons pass the unchanged physical tolerance. The corresponding exact conditional reference agrees with the saved native solutions well inside that tolerance. The actual cold baseline passes both windows; its selected extraction state error is approximately 6.46e-15.

The original signed extraction is more discriminating for the small pressure integral:

| Projected source | Native reference | Reduced prediction | Relative discrepancy | Gate |
|---|---:|---:|---:|---|
| Density | -1.0259226340481824 | -1.0259212725869302 | 1.32706e-6 | pass |
| Current | 0.08228092934536191 | 0.08228095388109785 | 2.98195e-7 | pass |
| Pressure | -0.00022500624054024466 | -0.0002246665572221522 | 0.00150966176 | fail |

The pressure discrepancy is 0.150966%, with absolute error 3.39683318e-7 in the retained source normalization. It remains above this stage's unchanged relative gate of 2e-5. Its historical mode-normalized error is 6.11860e-8, below that older 2e-6 gate; that different normalization is context only and does not replace the failed test here. The small signed projection involves cancellation, so passing the larger instantaneous pressure scale does not establish accuracy of its integral. No model or old late-time selector is replaced/promoted.

## Numerical diagnostic repair, not a physical retuning

Original validation.json remains false. All three original heavy extraction configurations failed only the stricter accumulated density-coordinate defect identity (tolerance 1e-10); their physical reference and step/history refinement comparisons passed. The diagnostic identity sums the reduced solution with a separately integrated exact-reference-driven error channel. That diagnostic channel is never added to the forward prediction.

A separately frozen check forced the integrator to stop at the existing cubic-Hermite source knots, carrying the same state through the same original output times. It changed no physical history, initial value, grid, solver tolerance, maximum integration step or coefficient. Both cold and heavy segmented calculations completed. The heavy diagnostic identity now closes at 6.97e-15 and 7.03e-15 in its two coordinates. Physical reduced/reference outputs remain consistent with the global-step runs at the unchanged tolerance, and the pressure projection still fails. This supports integration across the source interpolation knots as the cause of the accumulated diagnostic error; it is not a general guarantee about arbitrary interpolation or integrators.

selected-route-validation.json records 152 passing numerical/reference/readout/refinement comparisons and the separately retained failed projected-pressure gate. The original three failed diagnostic rows are preserved and identified explicitly. The selected route uses the repaired extraction packet and the already passing live packets; it does not relabel the original validation as passing.

## Error envelopes and provenance

The numerically integrated componentwise envelopes enclose the sampled measured errors. Their values are not converged at 2e-5 under the saved refinements. They are a posteriori diagnostics, not certified continuum bounds, independent predictions or observational error bars. independence.json records this limitation.

PROTOCOL.md has a prose error: it calls the saved memory derivative degree5. The frozen implementation actually reads the hash-locked fine8 packets through memory_path(...,'fine8'); the heavy live case uses saved native metric_rates. The implementation and those input packets were not changed for this result. Use the frozen paths/hashes, not that incorrect prose label, for reproduction.

The intentionally interrupted cold worker and its completed reusable packet are retained in ADMINISTRATIVE-PAUSE.md. Its failed receipt is not removed. Subsequent extraction configurations ran one at a time with bounded hold-check overhead. All final process identities and exits are recorded separately in CLEANUP-VERIFIED.json. No Galaxy files, public repository, original bank or earlier scientific checkpoint was edited.

## Actual next derivation

PREDICTIVE-MEMORY-CORRECTION.md derives an explicit first memory response driven by the approximate solution and current operator/forcing remainder, not by the exact trajectory. Its remaining error source is R*delta1. Test that forward correction against the retained pressure projection before making a more ambitious feedback claim. LIVE-FEEDBACK-LIFT.md supplies the separate current-rest-state interface needed afterwards. These follow-ons are derived interfaces, not already completed integrations.

[Operational or machine-specific passage omitted from public reading copy.]