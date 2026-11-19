# Preserved implementation attempts

All source/numerical gates stay unchanged. The retained physics code was not changed after execution.

- `independent-validation-01` stopped in the validation harness: the installed mpmath matrix constructor does not accept a dimensions-plus-callback initializer. The intended comparison matrices were silently zero. The original script, failed receipts and freeze file are retained.
- `diagnose-validation-01` then stopped while serializing mpmath scalar objects into JSON. Its partial JSON file is intentionally preserved as a failed diagnostic artifact, not accepted evidence.
- `diagnose-validation-02` converts the diagnostic scalars to ordinary floats and explicitly confirms the zero-matrix constructor behaviour.
- `validate_exact_jets_v2.py` replaces only the two comparison matrix initializers with explicit nested lists, and writes to a new output directory. It preserves the original 70-digit arithmetic criteria, physical gates, source formulas, histories and references. `independent-validation-02` is the accepted independent calculation.

The collector, exact source laws and stable generator did not require a physics repair. No failed output is used in the mean/primitive calculation. Original source versions and both failure receipts remain part of the final artifact seal.
