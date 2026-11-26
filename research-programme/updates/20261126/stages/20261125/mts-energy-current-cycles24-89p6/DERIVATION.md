# Heavy work without differentiating two cancelling field products separately

Write K=k², H for the conformal Hubble rate, Φ for curvature, Ψ for lapse and T=J_all/(2K)+Fq=Φ′+HΨ from the metric momentum equation. A prime denotes conformal-time differentiation. In the retained sign convention the raw constraint change is ΔC=ΔU−ΔW_h−Δ(BΦ)−ΔW_o. For both branches W_h=E/2+3HJ/(2K), and B=K+[3(e_c+e_b+s_v²)+4(e_γ+e_r)+ν_E]/2. B is evaluated on each branch's background; equality of sampled numerical values between branches is not assumed.

**Matched.** E=ρe, J=ρj, e=h_f+3Φ, j=h_w, and ρ=ρ₀/a. The retained equations give e′=3Φ′−j−3Hp+S_e and j′=−Hj+K(p+Ψ)+S_j. Consequently

    W_h′ = [ρ′e+ρ(−j+S_e)]/2 + 3ρT/2
           + 3[(ρ′H+ρH′−ρH²)j+ρH S_j]/(2K).

The two instantaneous pressure terms cancel identically for any p. Pressure still enters the propagated states. Use ρ′=−ρa′/a for the interpolated background.

**Native wave.** Let f,w be the heavy perturbation and its retained momentum coordinate; b,v the heavy background field and velocity; M=(am)², P=Mb. The actual physical heavy energy and current include the externally supplied source work:

    E = vw + P f + 3v²Φ + q_E,        J = K v f + q_J.
    f′ = w + v(Ψ+3Φ) + q_f,
    w′ = −2Hw − (K+M)f + P(3Φ−Ψ) + q_w.

Introduce g=v′+2Hv+P and s=b′−v, evaluated from the retained background splines. These are **not** assumed to vanish. Substituting the two field equations into W_h′, collecting like terms, and using Φ′+HΨ=T gives the following rate *excluding* the separately supplied derivative of q_E/2+3Hq_J/(2K):

    (g−Hv)w/2
    + { [M′b+Ms−Kv]/2 + 3[H(g−2Hv−P)+H′v]/2 } f
    + (3vg−3Hv²/2)Φ + 3v²T/2
    + v q_w/2 + (P/2+3Hv/2) q_f.

For example P′−Mv=M′b+Ms and v′+P=g−2Hv. This cancels the rapid mass terms algebraically rather than integrating a large positive field derivative and a large negative coefficient derivative and subtracting afterwards. It never divides by v or fits an oscillation phase. Add the exact increment of the explicitly supplied source work after integration.

**Pairing and check.** Integrate the heavy rate and (BΦ)′=BΦ′+B′Φ together on the same RK stages. Keep the signed pair, its two components, U and ordinary work. An independent primitive formed only from *forecast* endpoint states is ΔE/2+3Δ(HJ)/(2K)+Δ(BΦ). To score, use the saved raw drift as an archive target, and an independent replay in the old field-variable basis for the corresponding heavy and metric partitions. These are conditional tests with shared inputs; they are not observational predictions.
