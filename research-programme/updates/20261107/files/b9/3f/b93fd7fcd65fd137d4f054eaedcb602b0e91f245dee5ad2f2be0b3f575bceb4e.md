# Stage128 — temperature/source interpolation attribution

Preregistered14October2026 before new response calculations.
Previous turn is progress:Stage127 completed the integration matrix and
showed its tested errors are much smaller than the source-time sensitivity.

Reuse all33 saved first-interval states and existing endpoint/interior q32
operators. No new temperature integrals,no fitting,no new physical histories.
Keep evolution grid5265,inner40960,response2048,modes96,initial conditions,
DC/BR,overlap,and every other interval unchanged. Both backgrounds/windows
and baseline/both MTS joins receive identical tests.

Derive and evaluate exact product-interpolation decomposition into operator,
state and mixed terms. Split the operator term again using its positive
analytic energy moment m(theta),not a fitted normalization. Compare direct
operators with m(theta) times the linearly interpolated normalized shape.

Require source identity/analytic moment residuals<=1e-10,unchanged inputs,
zero diagnostic DC/BR/outside-interval forcing,and response superposition
closure<=1e-7 using operand-peak scales. Retain all raw response gas1e-7
failures;all other response checks retain their old gates. Diagnostic
signed pieces need not be positive collision kernels or separate theories.

Do not prescribe that moment normalization succeeds. Report signed
endpoint contributions,absolute differences,denominators and cancellation.
Its energy moment must be exact within1e-10 whether spectral/gas accuracy
improves or not. The1percent candidate comparison is a sensitivity gate,
not proof of a globally controlled approximation.

Independently reconstruct saved source identities,source changes,response
closures and moment agreement;rehash parent and consumed files;compile and
seal only after validation. No outside-child edits except mutable resume
heads. No GitHub,subagents,installation or protected-workbench changes.
One below-normal single-core worker;check in by13:39:15UTC.
