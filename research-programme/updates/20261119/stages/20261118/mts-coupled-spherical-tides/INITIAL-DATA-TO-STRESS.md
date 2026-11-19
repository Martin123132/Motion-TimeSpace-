# Deriving the needed stress envelope from scalar initial data

The comparison bound need not presuppose small scalar stress on *every later* slice. Here are two ways of obtaining it from initial data. Both need a regularity class for the **metric**, uniform in the small-scalar family; neither prescribes a time history for the scalar density. They concern classical regular solutions over a finite pre-crossing interval. No global existence or all-environment bound is asserted.

Let u=r h and p=rΠ, B=α/a, V=αa m²+B_r/r. The exact radial KG system becomes
    u_t=Bp,     p_t=(B u_r)_r−V u .
At a regular origin u,p are odd, B,V even. The seemingly singular B_r/r equals αa[2M/r³+s−e] by the radial Einstein constraints; at r=0 use M/r³→e(0)/3. Thus V=αa[m²+2M/r³+s−e]. This does not assume a flat background.

**Local characteristic option.** For w_±=p±u_r, (∂t∓B∂r)w_±=±B_r w_±−Vu. On a backward cone with no unknown incoming data, bound the initial absolute values of w_± and ωu by A₀, ω>0. The maximum along characteristics is ≤A₀ exp(kt), with k=max(sup|B_r|+sup|V|/ω,ω sup B). Only low-order regularity is needed. On r≥R_* and a≥1, e_h ≤ A₀² exp(2kt)[1+(1+1/(ωR_*))²+(m/ω)²]/(2R_*²). Extend oddly at the origin; otherwise include true inflow data. This is a sufficient finite-time estimate, not exponential growth of a physical massive mode.

**Energy option, avoiding exponential growth at the free carrier frequency.** Use all material support with regular parity and vanishing outer energy flux, or the entire isolated line restricted to r≥0. For V_min>0, B_min>0 introduce a fixed length L and
    H₀ = ½∫ [B(p²+u_r²)+Vu²] dr ,
    H₁ = ½∫ [B(p_r²+u_rr²)+V u_r²] dr ,    H=H₀+L²H₁ .
Integration by parts gives H₀,t=½∫[B_t(p²+u_r²)+V_tu²] dr. Differentiating the field equations once in r and applying the same calculation gives, in addition to the coefficient-time derivatives in H₁,
    ∫ [ B B_rr p_r u_r + 2B B_r p_r u_rr −B V_r p_r u
       + B B_rr u_rr p + V B_r u_r p ] dr .
The boundary terms vanish at the regular centre and in exterior vacuum outside the signal. Applying 2|xy|≤x²+y² with the energy weights gives |H_t|≤C(t)H with the sufficient coefficient
    C=max(sup|B_t/B|,sup|V_t/V|)
      +2sup|B_r|+sup(|B_rr|√(B/V))+L sup|B_rr|
      +L sup(|V_r|√(B/V))+L sup(|B_r|√(V/B)).
All suprema are over the specified radial domain. Importantly C=0 for a constant flat massive operator. Then H≤H(0) exp(∫C dt), not H(0) exp(2mt). These are regularity constants, not additional fitted couplings.

For a compact or decaying function g on the half-line, |g(r)|²≤2||g||₂||g_r||₂ by integrating to infinity. It also applies to even u_r, which need not vanish at the centre. Consequently p²,u_r²≤P²=2H_bound/(L B_min), u²≤U²=2H_bound/(L V_min). Using Π=p/r, h_r=(u_r−u/r)/r gives the **initial-data-derived** bound
    e_h ≤ [3P²+(m²+2/R_*²)U²]/(2R_*²) ,   r≥R_* .
For the initial enclosed energy μ use its actual constraint integral or upper-bound it from the proper initial field/gradient/velocity. Do not apply the last annular pointwise inequality at r=0. Use coordinate duration t≤W_* T/α_min when converting an observer's proper-time interval. The positive gradient term in H₁ controls concentration; a small total scalar mass alone would not control pointwise curvature.

There is also an exact identity for the enclosed-mass input. Integrate the cross terms in B u_r² with u=rh: the extra B(rh²)' cancels the integral of (B_r/r)u², up to the vanishing endpoint term. Therefore H₀=∫αa r² e_h dr. In an isolated regular solution with a≥1, αa=B a²≥B_min, so μ≤H₀(0)/B_min≤H(0)/B_min. A separate bound on the central point density is unnecessary.

For a family with fixed bounded metric regularity, lower positive B,V and fixed finite duration, H(0)→0 now implies both stress and enclosed-mass budgets tend to zero and both comoving separations recover GR uniformly. For a fixed smooth packet scaled by amplitude λ, H(0)=O(λ²), so the error is O(λ²), allowing nonzero phase and free gradients. This is a conditional finite-time local GR recovery from **initial scalar fields**, not an assumption of later suppression. The sample histories can measure constants and check inequalities; maxima on a discrete grid do not prove uniform continuum regularity. An independently certified uniform regular metric tube or a coupled small-data bootstrap remains necessary to make the estimate unconditional in a proposed environment. A spatially infinite homogeneous cosmological carrier does not have a finite isolated energy H; it needs a localized domain/inflow or an appropriate background-subtracted theorem.

