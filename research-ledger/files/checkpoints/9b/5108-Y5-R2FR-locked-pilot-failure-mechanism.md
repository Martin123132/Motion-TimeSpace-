# 5108 — locked pilot failure mechanism

The pilot passes matrix completion and runtime, but fails the efficiency score for a structural reason.

The high-only precision bottleneck is `imag_z-0.3`. The locked design sets all imaginary control coefficients to zero, so this channel keeps its high-only variance while paying the positive paired/independent low-bank cost. Its unavoidable score is

`sqrt((C_correction+3 C_low)/C_high)=1.3474894142500562`,

exactly the observed global score and already above the predeclared `0.8` threshold. Two active real channels also miss the threshold, but they do not set the global maximum.

Therefore adding more samples under this same low-only design cannot cure its primary efficiency gate. The next derivation is to prove or reject an exact conjugation/reflection-symmetric imaginary control. If that route fails, the low-only bank should remain rejected and future sampling should use a separately predeclared high-only or genuinely complex-control design.

This is an estimator diagnosis, not a theory verdict.

Outputs:

- `scripts/Y5_R2FR_5108_locked_pilot_failure_mechanism.py`
- `source-intake/functional_rg/5108/locked_pilot_failure_mechanism.json`
- `source-intake/mts_residuals/P8_Y5_BRR545_5108_VALIDATION.csv`
