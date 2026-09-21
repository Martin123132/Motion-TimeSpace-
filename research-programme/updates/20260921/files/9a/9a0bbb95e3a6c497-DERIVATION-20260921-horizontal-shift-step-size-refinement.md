# Refinement of the finite-shift probe: preserve the coarse failures

The first horizontal-shift run found failures in the separately evaluated MTS Gram derivative for the constant-connection profile. The observed primary case at label0 has raw derivative7.08334759e-11 versus the first Richardson estimate7.08257317e-11. This is a failed original comparison, not a reason to relax its tolerance or rewrite its evidence.

The two centered estimates at h=.001 and h=.0005 are approximately4.51842e-11 and6.44153e-11. They have not yet reached the small Gram derivative even though the action itself is evaluated consistently. Test step dependence before blaming or endorsing the action variation.

For S(epsilon)=sum_n s_n epsilon^n, a centered derivative is

    D_h=s_1+s_3*h^2+s_5*h^4+O(h^6),
    (4*D_(h/2)-D_h)/3=s_1-s_5*h^4/4+O(h^6).

Thus a factor16 reduction under step halving is a diagnostic of the leading Richardson truncation term, not a fitted correction to the physical current.

The separate, fresh step-scan copies the original finite-action evaluator unchanged except that it accepts the predeclared grid

    h=[.001,.0005,.00025,.000125,.0000625,.00003125].

It tests the same constant-connection profile at the same3 material labels in reference and both MTS branches. All original coarser estimates are reproduced and retained. Require the finest estimate to meet the ORIGINAL sector tolerance: absolute2e-12 for wave/dust,2e-18 for Gram, plus2e-7 times the raw derivative magnitude. For each nonzero MTS Gram sector, record the error-halving ratios; require the first two ratios to lie between8 and32 as a finite-range fourth-order diagnostic. Zero reference Gram terms are not assigned an artificial convergence rate. No new coefficient, action, background, state, stencil, or trajectory is used.

This is an explicitly post-failure numerical-resolution investigation. A successful refined check qualifies the derivative at the finer steps; it does not retroactively pass the first run's coarse gate. If refinement fails, retain the discrepancy as unresolved.
