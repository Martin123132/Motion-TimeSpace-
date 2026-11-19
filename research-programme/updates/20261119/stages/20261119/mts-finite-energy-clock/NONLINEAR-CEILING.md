# A necessary upper bound beyond the quadratic ellipse

Restrict to the two saved profiles, the conditional dilute background, regular untrapped configurations, and positive excitation E no larger than the originally proposed 1.70e−11. This is not an energy theorem for arbitrary gravitational matter.

Use the exact mass-difference kernel W of SOURCE-ENERGY-LIMIT.md. Define W₀ by setting v=0 and F_e=F_q in its exponent. With F_q and W₀ held fixed define K_ij and ℓ_i by integrating the perturbation profiles against each other and against the quiet scalar, respectively, and G by the positive proper-volume norm. This uses the **full quiet** constraint, not the earlier ordinary-background ellipse. If |W/W₀−1|≤δ then a necessary condition for zero mass difference is

    [λ_min(K,G)−δ] E ≤ √E [√(2 ℓᵀ G⁻¹ ℓ)+2δ√E_q,raw].

Proof: the fixed-kernel quadratic term is ≥λ_min E; the fixed-kernel linear term is bounded by the dual Gram norm times √(2E). The error from replacing W by W₀ is at most δ(E+2√(E E_q,raw)), using Cauchy–Schwarz and W₀≤1. The inequality is one-sided for *every* direction on the energy shell.

For a known upper energy, use the two interval bounds of SOURCE-ENERGY-LIMIT.md to bound |v|≤v₀ and |v'|≤v₁. Since W≤1 at each radius, |Δm(r)|/r ≤ r²[(v₀²+v₁²)/2+sup|h|v₀+sup|h'|v₁]/3 ≤ B_m. Thus F_e≥F_min−2B_m. Rationalizing the difference of the baryon terms in the two exponents gives a uniform exponent-change bound

    B = (9/2)[2 sup|h'| v₁+v₁²+2 n B_m/{√F_min (√F_min+√(F_min−2B_m))²}].

Use δ=expm1(B). The right-hand side of the first inequality supplies an improved upper energy whenever its denominator is positive; iterating strengthens rather than assumes the cap. A single near-saturating source on the nonlinear constraint gives an existence lower bracket on the supremum, not a lower bound on an arbitrary event's energy. Computed Gram matrices and norms are evaluated twice (1,024 and 2,048 initial radial samples per length), with outward 1e−6 relative margins on the two projected coefficients. These are reproducible numerical evaluations of an analytic inequality, not machine-verified interval arithmetic. The separate looser direct exclusion does not use those Gram eigenvalues.
