# Source/bound revision receipt

The half-family worker imported the initial analytic_math.py before its clock-mean ratio bound was corrected on disk.
analytic_math_initial.py retains that exact imported source (hash checked against the initial freeze).
The correction changes only reported truncation bounds: the sampled clock denominator must also be bounded, and integrating sampled forcing needs its own alias bound.
It does not change source construction, operator evaluation, inputs, grids or tolerances.
The final independent audit must recompute ALL bound reports from the completed coefficient packets using the corrected analytic_math.py; those audit results, not the initial per-case bounds, are authoritative.
The half worker remains a single uninterrupted calculation, not a rerun. Its source-freeze metadata is supplemented by this explicit imported-source receipt.
