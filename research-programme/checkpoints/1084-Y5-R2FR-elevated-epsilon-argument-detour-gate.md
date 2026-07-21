# 5068 - elevated-epsilon argument-detour gate

Marker: `MTS_5068_ELEVATED_EPSILON_ARGUMENT_DETOUR_GATE`.

An explicitly predeclared higher-epsilon detour was tested as a way to recover
straight-path fallback edges. Nine candidate zero-detour signatures appear,
but two are false negatives against the full target and none can be adopted.
The detour also costs `10.07 s` more per event on average.

Decision: reject the elevated-epsilon hierarchy and retain the straight
certified chain. This negative result prevents a cheaper but unsound route from
entering the runner.

## Evidence

- Result: `source-intake/functional_rg/5068/elevated_epsilon_argument_detour_gate.json`
- Rows: `source-intake/functional_rg/5068/argument_detour_rows.csv`
- Generator: `scripts/Y5_R2FR_5068_elevated_epsilon_argument_detour_gate.py`
- Validation: `source-intake/mts_residuals/P8_Y5_BRR545_5068_VALIDATION.csv`

No detour transport or fresh kernel is authorized.
