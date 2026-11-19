# Saved midpoint is a conformal-time midpoint

The first normalization extractor recovered identical mass/amplitude from
the native initialization and saved source coefficients, but its midpoint
scale gate failed. It mistakenly treated the saved probe fraction as a
fraction of log scale factor. The retained port samples linearly between
conformal times; these midpoints are not the same physical epoch.

Keep normalization-result.json and normalization-end.json unchanged.
check_clock.py reuses those recovered numbers, maps the probe through the
saved background's conformal clock and checks the original 1e-10 gate.
No mass, amplitude, tolerance or native background initialization is rerun
or adjusted. normalization-clock-result.json records the corrected gate.
