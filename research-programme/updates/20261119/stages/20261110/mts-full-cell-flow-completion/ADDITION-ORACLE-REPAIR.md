# Exact addition-oracle repair; source calculation unchanged

The first accumulation attempt stopped before writing either model's accumulated packet. Its independent addition checker demanded bitwise equality between binary64 addition and a 90-significant-digit decimal sum converted back to binary64.

Read-only diagnosis found exact halfway sums where the finite decimal intermediate moves to one side of the binary midpoint, producing a one-ULP double-rounding discrepancy. Fraction.from_float reconstructs the exact rational value of each binary input; their exact rational sum rounds to the existing NumPy result. The fault is the finite-decimal bitwise oracle, not the production sum or the physical source.

audit_addition_oracle.py checks every scalar addition used by the cumulative step for both MTS and baseline. For every decimal disagreement it additionally requires adjacent binary64 results and proves that the exact rational sum equals their midpoint. It records all such cases and unchanged input hashes.

accumulate_complete_cells_v2.py keeps the numerical arrays, arithmetic, physical inputs, grids and tolerances unchanged. Only its independent addition oracle changes to exact rational arithmetic. It writes a separate accumulation-02 output and requires the oracle audit to pass first. The failed accumulate-01 attempt, source file, logs, empty output directory and terminal receipt remain preserved. This is an inspected repair, not an automatic failed-run retry.
