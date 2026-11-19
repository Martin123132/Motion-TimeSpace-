# One bounded manual step: fixed-lag historical readout

2026-11-12. The app goal stays paused. No automatic research, new handover, fit, downloads, publication, changed bank or added physical parameters. Reuse the completed eight-interval live baseline/MTS runs. One numerical worker/thread, with the retained guard and exact identity receipts.

Freeze before evaluation:
- Original902 weights and original native historical epochs. Each branch uses its OWN native conformal clock at the same original scale-factor indices; no shift of the center or replacement of physical lags by index offsets.
- Primary past interpolation: local degree5 polynomial using6 original knots. Compare degree7/8knots; degree3/4knots is a separately labelled sensitivity diagnostic. No extrapolation beyond the available past. Historical knots reproduce exactly.
- Current source continuation: local cubic Hermite interpolation using saved source values and equation-owned derivatives, with only the available prefix through the readout epoch. No future native samples are passed to the prediction.
- Independent native endpoint source series are a comparison only. Use the saved32/64 integrations to separate ODE sensitivity; odd current nodes held out from Hermite interpolation are an interpolation check.
- Historical odd nodes are held out from the polynomial check (endpoints kept), with no fitting. Degree5/7 discrepancies at the actual queries are also propagated with absolute weights to expose cancellation. This is a numerical discrepancy envelope, NOT a certified mathematical error bound.
- Numerical tolerance2e-5, algebra tolerance1e-10, per-source normalization (D,Q,P). Exactly-zero dust current/pressure must remain zero; no arbitrary floors. Include the old nonzero MTS initial memory.
- Report separately: exact initial readout, historical withheld-node checks, current withheld-node checks, degree5/7 weighted and absolute-weight discrepancies, source-map/normalization continuity, paired ODE difference and same-interpolation native comparison. Preserve failed checks without adjusting the tolerance.

Explicit history is tested first. A compressed memory model is not built unless this readout is reliable. Existing source derivatives and full native continuations are inputs, not rederived or rerun here.
