# Frozen-prediction report selector repair

test-half-01 stopped before opening a native context or evaluating a held-out point: its report selector still pointed to prediction-01/result.json, whereas the repaired paired report is prediction-02/result.json. The original partial report path was not fabricated. test_time_v3.py reads the correct already-frozen report and writes test-02, preserving the failed attempt and its empty output. Predictions, inputs, equations, target epochs and gates are unchanged. This is a selector repair, not a numerical failed-test retry.
