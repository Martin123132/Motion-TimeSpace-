# Extending the saved source-history test without resetting it

## Same preparation, later endpoint

The retained mode is k=5 in the native inverse-Mpc convention. The original902 signed preparation nodes and initial matching state remain fixed. Report indices2892..2900 are retained unchanged; the new block is2901..2908. Elapsed duration increases from about0.009864 to0.019727 in the native conformal-time units. This is still a short numerical history test, not a late cosmological epoch or an observational fit.

For each prepared node the retained system is

    X_i'=A(t_i+s)X_i+B(t_i+s)F_i(s),
    F_i(s)=F_i(0)+s F'_i(0)+s^2 K_i(0)/2+R_i(s),
    R_i(s)=integral_0^s (s-v)[Khat(t_i+v)-K_i(0)]dv.

The same vectorized local-cell integral and physical normalization are reused. Old curvature cells are concatenated byte-for-byte with the missing new cells; no old polynomial is refitted, and no polynomial is extrapolated outside its domain.

The source-history, frozen-quadratic and resolved difference equations restart separately from their saved32/64 endpoint states. Crucially, the quadratic source is still expanded about the original preparation times, not restarted with newly chosen coefficients. Likewise DeltaX is carried forward, not reset to zero:

    DeltaX'=A DeltaX+B R_i, DeltaX(T_old)=saved DeltaX(T_old).

All old report rows are copied unchanged. Maximum physical integration steps remain T_old/32 and T_old/64, with rtol1e-10 and normalized atol1e-12. The saved difference-state conditioning is reused, not recalibrated against the new residual.

## New source cells and one-sided control

Only eight original source intervals are added:11 polynomial cells for baseline and13 for MTS after splitting at background corners. Native quarter/midpoint values construct the new cells. One-sided points use resolvable offsets, and the native thermal interpolation-cell ID confirms their side. The true sample coordinate enters the polynomial; it is not falsely treated as exactly on the corner.

Frozen predictions are then tested at22 new baseline and26 new MTS one-sixth/five-sixths points. The physical native evolution keeps its original complete requested clock and modes; diagnostic probes evolve copies. All910 previously retained main packets are byte-identical, and all918 extended main packets agree between the two probe schedules. No dynamical/native source files or DLL are changed.

## A reference for the new block, not extrapolated old uncertainty

The old explicit-history reference and its uncertainty only cover the original nine reports. For each of the eight new reports, obtain the native own-field readout at all902 shifted times t_i+s. This supplies7,216 node/epoch evaluations per case. The signed projection uses the same saved initial matching anchor:

    O_ref(s)=O_ref(0)+sum_i weight_i [S_native(t_i+s)-S_native(t_i)].

O_ref(0) is the old saved initial reference; it is not fitted to the new block. The native initial node readout agrees with the retained initial source representation at the unchanged algebra gate. The prior reference rows and their numerical budget are preserved for their own interval.

Two native probe/restart schedules evaluate the new query set. The second includes extra midpoint stops and the fresh source validation points. Absolute-weighted differences supply a query-path working uncertainty. A separate floating-arithmetic term uses absolute kinetic/potential contributions and absolute weights. Neither estimate proves absence of a common native-solver error. This direct numerical reference must not be called a new observational holdout or a fully independent physical theory.

The original D/Q/P reference scales are retained for2e-5 comparisons, including the new block. They are not enlarged to make an extending signal easier to pass. The new-tail budget keeps query-path sensitivity, reference arithmetic, saved initial recapture, new32/64 evolution differences and projection arithmetic distinct. No old future uncertainty is extrapolated.

## Extended response inequality

The old final-time gain cannot bound a later endpoint. Recompute forward and adjoint response gains through T_new, using64/128 full-horizon step ceilings so their maximum physical step is no larger than the old32/64 setting. The same forward/adjoint duality and refinement gates apply.

For each node/channel let V_i bound the represented curvature change Khat(t)-K_i over its now-longer interval. Use the same clipped-cell Bernstein enclosure, and include the absolute nodewise gain-refinement difference:

    E_c = sum_i |weight_i| sum_channel (G_fine+|G_fine-G_coarse|)_i,c,channel V_i,channel.

The independently evolved final DeltaO must lie inside E plus its difference-solve uncertainty. Fresh source-reconstruction discrepancy is tracked separately through the new gains. Finite source tests and numerical gains are not an interval-certified continuum theorem.

## Time-growth clue, not a fitted law

Doubling the short duration increases the resolved baseline density correction by15.9972 and MTS pressure by16.1771; MTS current increases32.5551. On a smooth one-sided cell, a cubic source remainder gives DeltaX=O(T^4), with an extra integration for the displacement/current channel giving O(T^5). The observed factors are compatible with that local-order picture, but they do not prove a global power law across all corners. Deriving the coefficients and limitations of that estimate is a useful next target before choosing a much longer test window.
