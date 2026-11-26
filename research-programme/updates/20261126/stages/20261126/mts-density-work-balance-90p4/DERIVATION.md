# A constraint-work identity for the oscillation-averaged stress

**Fields and normalization.** Conformal time is η; a prime denotes d/dη, H is the saved conformal Hubble rate, κ=k², and D is the density-constraint denominator as retained (not a background identity substituted for it). Write E,J for energy and scalar current in the normalization of the archived Einstein constraints. On a density-route trajectory the independently calculable residual is

    Φ_E = (U − E/2 − 3HJ/(2κ))/D,    P_J = J/(2κ) − HΨ + Fq,
    R = Φ_E′ − P_J
      = U′/D − D′Φ_E/D + HΨ − Fq + Σ_s W_s,
    W_s = −E_s′/(2D) − 3(H′J_s+HJ_s′)/(2κD) − J_s/(2κ).

For a species whose energy or current is c(η)·Y(η), its rate is c′·Y+c·Y′. This calculation gets Y′ from the retained equations, including the 77 massive angular populations and their shared spectral shape, not by differentiating Φ_E. Constant and externally driven terms are additional time-dependent coefficients acting on the constant state 1. The split is an identity in these variables; a bare term need not be observable. In particular the mixed baryon/photon momentum should not be attributed to photons alone.

**Why fast current derivatives cancel.** For the activated companion, let ρ=ρ₀/a, r=a′/a, j be its physical instantaneous heavy current divided by ρ, m its carried mean and d=m−j. Let e be the compensating energy variable. The retained current/pressure equations imply

    δJ=ρd,     δE=ρe,     P=(d′+Hd)/κ,     e′=−d−3HP.
    δE′=−rδE−δJ−3Hρ(d′+Hd)/κ,
    δJ′=ρd′−rδJ.

Substituting these last two equations in W_s cancels the terms proportional to ρd′ exactly. The remaining companion contribution is

    W_comp = r[δE + 3HδJ/κ]/(2D)
           + [κ−D+3(H²−H′)]δJ/(2κD).

Thus it is the weighted *energy plus current* and the independently testable background combination that can leave work here, not an uncancelled rapid derivative of the phase mean. The code tests the two sides on the matched history without setting the bracket to zero or imposing r=H. On the resolved wave there is no companion. Also J_explicit+δJ=ρm on the matched branch: the direct wave current is not counted twice. This identity only treats the direct companion term in R; the companion still changes the evolved trajectories and their metric. It is not a license to switch off the compensation or declare the total residual zero.

**Native U check.** The previously measured signed error in the frozen restoration supplies δU, not a parameter to optimize. At fixed matter state and fixed other forcings, the direct change of the density potential and lapse is δΦ=δΨ=δU/D. The interval contribution to photon forcing is therefore (δU′/D−D′δU/D², δU/D). This computation deliberately has zero incoming diagnostic photon state, no added boundary impulse, and no matter backreaction. It is a sensitivity, not a rerun of the physical model.

**Independent target for the next stage.** Write the explicit heavy perturbation energy as E_h=v w+M² b f+E_ext, where b,v are background field and conformal velocity, f,w the two evolving perturbations, and M²=(am_h)². Define S_f=f′−w and S_w=w′+2Hw+M²f; the next test must compute these from the metric and physical source terms, *not* infer them by subtracting the target energy rate. If b′=v and v′=−2Hv−M²b, the two terms in M²bw and the two in M²vf cancel, giving

    E_h′ = −4H v w + (M²)′ b f + v S_w + M² b S_f + E_ext′.

For independently interpolated background tables retain the additional terms (v′+2Hv+M²b)w + M²(b′−v)f; do not silently set them to zero. This is an algebraic prediction of the retained equations. Its decomposition into expansion, metric work and external-source work has not yet been tested on the two trajectories; the measured target is their energy-rate contribution to the photons.
