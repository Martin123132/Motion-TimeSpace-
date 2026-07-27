# 5080 - locked fresh-pilot analysis

Marker: `MTS_5080_LOCKED_FRESH_PILOT_ANALYSIS`.

Before the 5079 matrix is complete, the v6 analysis code and decision rule are
hash-locked. The estimator is

`mean[H-BL_paired] + B mean[L_independent]`,

with `H=P[2R_primary(E020)-R_primary(E040)]`, fixed `B=1` on the five real
channels, and fixed `B=0` on the five imaginary channels. No coefficient or
target central value is fit from the fresh data.

The predeclared numerical pass requires all 360 kernels to converge, recorded
runtime no greater than ten hours, and a realized-cost target-normalized score
ratio below `0.8`. Delete-one-high and delete-one-low shifts are diagnostics,
not post-hoc gates.

## Evidence

- Lock: `source-intake/functional_rg/5080/fresh_pilot_analysis_lock_v6.json`
- Locked script: `scripts/Y5_R2FR_5080_locked_fresh_pilot_analysis.py`

The lock binds configuration digest
`4b3cf7f08d232f26aeed21618068707b3b7e1e5362fd5f5dc160fedba207f2af`.
The v6 pilot is currently blocked at `112/360`, so result, channel, event-cost,
jackknife, and validation files are not authorized. Passing this numerical
gate would still not establish the full MTS theory.
