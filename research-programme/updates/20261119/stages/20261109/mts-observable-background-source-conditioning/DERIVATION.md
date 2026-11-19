# Observable-coordinate source conditioning

For the retained map T=S^-1 F P and the original adjoint lambda, set

    x=T y_c,   a=T^-T lambda=S^T F^-T P^-T lambda.
    g=lambda^T T^-1(r_ref-r_ret)=a^T(r_ref-r_ret),
    r_ref=F_ref x,   r_ret=F_ret x.

F in the coordinate map is distinct from the native generators F_ref,F_ret. The paired native rates, maps, phases and original adjoints are already saved at all257 points/model. Both rates already use their own background's conformal H. No new physical operator, clock or phase is introduced.

## Three different numerical questions

1. **Represented subtraction and reduction.** Treat saved rates and the computed covector as exact floating-point inputs. Error-free TwoDiff gives hi+lo for their exact difference under ordinary finite IEEE arithmetic. Fused multiply-add residuals and an accurately summed expansion evaluate a dot(hi+lo) without discarding the subtraction low part. Exact rational spot checks test selected full contractions. This diagnoses arithmetic on the stored packets; it cannot restore errors already present when the rates were generated.
2. **Conditioning with respect to the rate inputs.** If independent relative perturbations of both rate vectors are bounded by epsilon, then |delta g| <= epsilon sum_i |a_i|(|r_ref,i|+|r_ret,i|), with a held fixed. Integrating the positive quadrature weights gives a source-budget-relative sensitivity. Reporting it for epsilon=u (binary64 unit roundoff) is a benchmark, NOT a bound on the actual native generator error. No operation count for the native generator is assumed.
3. **Phase integration.** On each block of four fine subintervals, compare its two fine Simpson panels against the coarse Simpson panel using the same endpoints and middle point. The sum of these signed local differences equals the original257-versus129 difference. Their absolute sum and concentration identify cancellation and phase regions demanding attention. The analogous129-versus65 calculation is retained. These are refinement diagnostics, not rigorous quadrature remainders.

The usual gamma_n=n u/(1-n u) bound applies to specified arithmetic on fixed inputs, not to the full physics automatically. For the post-subtraction dot product, the conservative gamma_(2D+1) sum |a_i hi_i| estimate is reported separately from the explicitly recovered lo contribution. Underflow terms are recorded and exact rational spot checks are retained; no claim of an exact continuous physical source follows from finite-packet precision checks.

All ratios also retain the old reference scale. A tiny physical baseline residual is not set to zero merely because its relative condition is poor. A large worst-case sensitivity is not evidence that the worst perturbation actually occurred. Current histories, source phase, bank, physical grids, numerical tolerances and the model are unchanged.
