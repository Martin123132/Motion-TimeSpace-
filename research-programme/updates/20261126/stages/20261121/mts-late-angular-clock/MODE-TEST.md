# Can gravity alone carry the measured clock error?

This is an additional local transfer test, not a fit to the final centre. It has two inputs: (i) the independently injected smooth angular curvature, and (ii) the actual difference between native and half-step gravitational fields **before** the last 64 ticks. The second test is retrospective; no amplitudes or phases are optimized.

On a flat slice write the four metric coefficients as (L,u,m,β), where u=L+2b is the metric trace combination; write the four extrinsic/momentum coefficients as (k,s,π,τ). These are evolution-chart variables, not observables. Retaining the radial and angular derivatives of the actual action-derived geometric equations while omitting matter variation, expansion and curved-background terms gives, in the stored proper time,

    L′=−k/3−s,    u′=−k,   m′=π,             β′=τ,
    k′=H,         s′=−X−H/3,  π′=−r D_fH/2,   τ′=−H/2,
    H=−2[D_b(r m)−6β]/r²,
    X=r⁻⁶D_b(r_f⁶D_f L)+[2D_b(r m)−D_b D_f(r²u)]/r².

In face terms m and π have their original regular face completion. The twelfth-order derivatives and their centre parities are unchanged. Differentiating H gives the separately solved flat scalar wave in the [pulse derivation](DERIVATION.md); agreement checks more than just a period or final amplitude. To predict what the second, cell-based geometric momentum reader would see, also reconstruct the physical cross velocity

    V_f=[π−2r_f D_f(−k/3+s/2)−3I_f s]/3,
    τ_cell=τ−r [D_old I_c V_f−D_even V_f]/2.

The two derivative chains are fixed by the two saved implementations; there is no adjustable transfer coefficient. This is a prediction of their **difference**, not permission to subtract it from an adverse measured residual. Compare both forecasts to the actual signed pulses in the curved runs; the scalar Hamiltonian on a curved slice is not identical to this flat principal part.

For the unforced trajectories let Y_A be the last-quarter half-step readout, Y_B the half-step result restarted at native tick 960, and Y_C the unbroken native result. The identity Y_A−Y_C=(Y_A−Y_B)+(Y_B−Y_C) separates what was already different at tick 960 and subsequently evolved under identical clock steps from what changed solely by taking shorter steps after tick 960. It is exact for a scalar readout, even on nonlinear trajectories. Ratios of norms of these terms are not additive fractions. A separate three-clock comparison always uses the identical tick-960 state.

Propagate all eight signed angular field differences A−B from tick 960 through the flat system at the same half step; a finer time integration is a separate sensitivity check. Compare predicted geometric τ and τ_cell to the held-forward **curved** values of P+J and P_ind+J_ind, respectively, rather than confusing a matter change with a geometric one. In addition, take only the initial L,L′ with u=m=β=π=τ=k=0. Its source-free angular equation is L″=r⁻⁶D_b(r_f⁶D_f L). Subtract this solution from the full flat one to identify the remaining forced part of that decomposition. This does not decompose the full curved theory into independent physical species. The same grid and input differences are used for wave and cold controls. The input is a numerical difference, not a new physical matter state.
