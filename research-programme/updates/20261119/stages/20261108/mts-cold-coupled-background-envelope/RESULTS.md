# Complete cold coupled-source envelope — verified 2026-11-08

## Scientific advance

The inherited background and clock uncertainty is now propagated through the COMPLETE physical coupled generator, including the exact metric/map derivatives and their mixed background derivatives. The bound covers the entire saved cold interval and all phases, rather than just the saved start/midpoint/end probes. The existing source, action-derived branch, bank, grids and initial preparation are retained.

This includes every retained G192 massive hierarchy level, both saved models, all three original wave numbers and both GR/spatial-Poisson branches. Sparse evaluation is exactly the same coupled algebra as the previously qualified dense pullback; its remote tail rows are verified to remain the original free source, not truncated away.

Two useful structures are derived and kept separate:

1. The full coefficient-replacement error, which can affect phase and amplitude.
2. Its symmetric part, which bounds the change in physical logarithmic norm and hence amplitude growth. Exact skew streaming is cancelled before interval estimation, rather than counted as instability.

The source replacement is also carried through the normalized phase-clock measure. This avoids silently assuming that a change of background leaves the time-weighted phase average unchanged.

## Uniform bounds

The following MTS bounds include the continuous phase-mean weighting correction. Values shown round upward and cover both retained gravity branches.

| Inherited k family | Full mean-generator replacement | Symmetric mean-generator replacement |
| --- | ---: | ---: |
| half | 2.444700e-3 | 1.312014e-4 |
| balanced | 5.555940e-3 | 1.082047e-4 |
| double | 1.111181e-2 | 1.082047e-4 |

These are conservative operator bounds per unit ln(a), NOT fractional observational errors, fitted discrepancies, or the total transfer error. The saved entrywise bounds are available for a sharper calculation on the actual prepared perturbation. The symmetric bound constrains a change in growth rate, not the entire growth rate. The earlier midpoint logarithmic norm must not be substituted for a whole-path value.

The baseline's heavy-averaging replacement radii are zero; its saved result is only the outward float floor, approximately5e-324. This does not claim zero baseline solver, source or observational uncertainty.

The uniform phase frequency lies in [2.1365961619765922e8,3.7068497677637297e8]. Its inherited replacement error is bounded by428.1599907299166. Normalizing the phase probability density gives an L1 weight change <=1.406866e-14, so the additional full-generator mean uncertainty is at most1.353566e-10; the symmetric addition is at most4.853628e-13. A large accumulated unaveraged phase error is not ruled out by these small changes of normalized measure.

## Evidence and unchanged gates

- 108 sparse/direct branch comparisons: largest absolute difference1.110224e-16. Remote full G192 source rows are checked explicitly.
- 72 independent structured-symmetric comparisons: largest absolute difference8.253459e-13, below ALGEBRA=1e-10.
- Twelve complete model/wave/gravity envelopes use50-digit outward interval differentiation over the inherited tube. No sampled maximum is used as a supremum.
- 1,356,618 independent70-digit complex-derivative entry checks cover the complete source and symmetric part. Two complex steps are compared; worst relative refinement difference2.410530e-45.
- 90 actual background/clock fixtures remain inside the frozen entry/Frobenius bounds. Largest fixture/Frobenius-bound ratio0.340187; largest derivative/bound ratio0.9999999999999999.
- Three exact symbolic identities cover the normalized phase-clock derivative, its uniform majorant and the exceptional massive streaming pair. Independent high-precision period integrals and normalized-weight derivatives check the implementation.

ALGEBRA=1e-10 and GATE=2e-5 are unchanged. The interval theorem is conditional on the already retained finite source coefficients and inherited background tube; global integration, native representation and thermal-continuum uncertainty remain their own error channels. DERIVATION.md states the precise scope and arithmetic-validation floors.

## Numerical precision repair

The first clock-weight validator stopped at its unchanged1e-55 relative arithmetic criterion. The normalized phase density is almost constant; at theta=0 its derivative is of order mu^-3. mpmath's default differentiation guard precision gave a worst relative error2.816495e-55. Diagnostic calculations identified this subtraction loss while confirming the working precision remained70 digits.

The separately named `mean_weight_bound_v2.py` adds80 guard bits only inside the independent numerical derivative. The exact formula, interval bound, physical source and tolerances are unchanged. `mean-weight-02` is accepted; the first script, failed receipt and partial freeze directory are preserved. No theory repair was needed for this issue.

## Files and next physical step

Accepted implementation: `background_jet.py`, `factored_sparse.py`, `symmetric_source.py`, `enclose_coupled.py`, `validate_envelope.py`, `mean_weight_bound_v2.py`, `audit_envelope_v2.py`.

Evidence: each wave family's `envelope-01` and `validation-01`, plus `sparse-validation`, `symmetric-validation`, `mean-weight-02` and `audit/result.json`. All consumed parent artifacts are checked against their seals. Cleanup and final inventory are recorded separately in CLEANUP.json and closeout.json.

Next, apply the saved entrywise error and physical growth structure to the ORIGINAL prepared perturbation, verify its preparation-to-cold matching, and carry both endpoint maps and the averaging remainder into the transport calculation. TRANSPORT-CONTRACT.md derives the relevant variation-of-constants bound. Do not initialize an arbitrary late mode or equate a worst-case coefficient bound with an actual transfer residual.

All work remains local. No GitHub action, new dataset, fitted cutoff, altered source bank or changed tolerance.
