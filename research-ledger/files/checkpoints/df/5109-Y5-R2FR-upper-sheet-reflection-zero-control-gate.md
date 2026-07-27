# 5109 - upper-sheet reflection zero-control gate

The proposed zero-mean imaginary control is rejected for the locked upper-Feynman-sheet observable. This is a proof-level contour result, not a failed search.

For the reflected event

`(x,s,d,r,w,c) -> (x,-s,-d,conj(r),conj(w),-conj(c))`,

the directions obey `n_R=diag(1,-1,-1)conj(n)`, and the finite-plus integrand obeys

`F_R(-conj(c),conj(r),conj(w))=conj(F(c,r,w))`.

Across all 16 locked events and all 15 locked arguments, the maximum normalized integrand residual is `1.9915401814800678e-12`. The target pole map is also exact to `4.217831194788777e-14`: `plus_u <-> plus_v` and `minus_u <-> minus_v`.

The obstruction is the owned contour. Reflection maps the anchor `+0.3` to `-0.3`, where that same target permutation is exact. The implemented upper-sheet prescription instead reanchors every reflected event at `+0.3`; at that common anchor the permutation is `plus_u <-> minus_v` and `plus_v <-> minus_u`. Both identities have zero mismatches, but the two ownership maps disagree in 408 of 1280 locked event/chamber comparisons.

A fixed-relative cyclic counterexample separates algebra from contour ownership. The true reflection-image cycle satisfies the expected conjugate/reversal relation to `5.9215582170490347e-14`. The prescribed upper-sheet cycle misses it by `1.3467511476339342`, so the difference is macroscopic and residue-carrying rather than quadrature noise.

Therefore `E[Im R]=0` cannot be imposed. The imaginary component is an upper/lower-sheet absorptive discontinuity, not a reflection-forced zero. Checkpoint 5037 was correct to keep its reflection row diagnostic-only.

This rejects only the zero-control construction. The next estimator route is an exact complex multilevel identity or a nonzero discontinuity control; no additional kernels should be spent on the rejected symmetry.

Outputs:

- `scripts/Y5_R2FR_5109_upper_sheet_reflection_zero_control_gate.py`
- `source-intake/functional_rg/5109/upper_sheet_reflection_zero_control_gate.json`
- `source-intake/mts_residuals/P8_Y5_BRR545_5109_VALIDATION.csv`

No MTS physics, fixed-point, local-GR, or full-theory claim follows from this estimator theorem.
