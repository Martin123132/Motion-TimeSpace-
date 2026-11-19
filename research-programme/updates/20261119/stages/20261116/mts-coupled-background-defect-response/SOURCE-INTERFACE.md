# Stable source interface and unchanged acceptance gates

The original background integration and its results are frozen. This separate
checker does not rerun or alter the state, grids, bank, parameters or tolerances.
It tests the resulting source map, using the saved full perturbation history.

For alpha=delta a/a, B=delta b, V=delta v, M=(am)^2, beta=a/R0,
let dM=M alpha(2+alpha). At fixed perturbations u,w and comoving k,

    K=v w, U=M b u, dK=V w,
    dU=(dM b+M B+dM B)u,
    S=(K+U,k v u,K-U), dS=(dK+dU,k V u,dK-dU),
    delta Y=beta[dS+alpha(S+dS)].

This exact difference avoids subtracting two nearly equal source values.
The cold CDM normalized source is unchanged at fixed density contrast,
but its bare constraint density changes by -D alpha/(1+alpha).
Zero fixed-state cold source response is not zero evolved response.

The checker compares this algebra with 80-digit direct arithmetic at the
anchor, late/worst-clock examples and maximum-change nodes. All original
33x902 sources are independently reconstructed from the retained readout.
Fine/coarse and linear/nonlinear background effects are propagated through
the same fixed-state source map. Signed weights and matched initial-epoch
subtraction are unchanged. The physical gate remains2e-5 on the saved source
scales; algebra checks remain1e-10. Correction-relative diagnostics are
also retained, including any failures: a tiny correction is not made
converged by changing its denominator.

In particular the cold run has four failed correction-relative refinements.
Its largest relative scale correction is4.24e-16 and the scale difference
between refinements is2.31e-18. The slow velocity correction differs by
1.72e-30. Their small absolute sizes do not override the failed tests.
Full-state agreement and source-error checks answer different questions
and are reported separately, not substituted for the original acceptance.

No environment, prepared-state or metric-perturbation response is set to
zero in the physical theory. This is an interface/sensitivity calculation,
not a repaired cosmological prediction or closure of the prior pressure
readout discrepancy. The quantum measure is not part of this stage.
