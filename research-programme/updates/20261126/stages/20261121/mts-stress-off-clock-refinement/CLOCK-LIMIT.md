> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# Why the third clock is informative

In the retained step map (not bundled here) the massive wave has a fast eigenvalue +2iµ; the cold control does not. This linear part is propagated exponentially, not with an ordinary explicit update. Stage values of the other terms still enter a slow component with the zero-eigenvalue weights 1/6, 1/3, 1/3, 1/6 at nodes 0, 1/2, 1/2, 1. The native interval is h=4π/µ, hence the first carrier harmonic advances by 8π. Exact evolution of the free carrier is **not** sufficient to prove exact integration of its forcing of the slow metric.

For a manufactured slow variable driven *only* by exp(iωt), let θ=ωh/d for d equal substeps. The discrete drive, divided by h, is

    [(1+4 exp(iθ/2)+exp(iθ))/6] × [Σ_{k=0}^{d−1} exp(ikθ)/d].

The exact integral of every nonconstant integer carrier harmonic is zero over h. For the first harmonic the native and half steps both return one instead of zero: even their midpoint samples see the same phase. Thirds cancel it, but its third harmonic still aliases. Moreover a changing envelope does not cancel like a constant. With linear envelope t/h the exact response divided by h is 1/(iωh). Differentiating the finite sampling sum gives the corresponding discrete moment; where exp(iθ)≠1 and the full interval closes, it is −(1+4 exp(iθ/2)+exp(iθ))/(6d[1−exp(iθ)]). The [control program](evidence-001.zip) (archive member: `clock_phase.py`) compares these expressions to actual slow-stage weights and directly sampled constant and linear envelopes.

These are constructed counterexamples to a numerical inference, not amplitudes inferred for the physical source. The actual two-sign, wave/cold comparisons must be made on the evolved histories. Close agreement at three finite subdivisions on a shared restart is encouraging but not a rigorous upper bound on a full-formation continuum solution.
