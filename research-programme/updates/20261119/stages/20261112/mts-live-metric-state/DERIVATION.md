# Live metric/field subsystem and external-source response

## Retained equations, not a new branch

Use the native flat constraint and metric equation already verified in the previous stage:

    z=[D_total/(2k)+eta_k]/H,     eta_k'=Q_total/2.

Primes denote the same conformal Mpc clock. The background splines, masses, normalization and original scale-factor clock are retained. In particular r=a'/a and H are not silently identified in derivative calculations. Let M=(am_h)², b,v the retained heavy background, u,w its perturbation with u'=w. The heavy density and current are D_h=vw+Mbu and Q_h=kvu. Define D_o,Q_o by excluding this component only. Then

    u'=w,
    w'=-(M+k²+vMb/(2H))u-(2H+v²/(2H))w
         -(kv/H)eta_k-vD_o/(2H),
    eta_k'=kvu/2+Q_o/2.

All metric feedback of the subsystem is now live. The H(t) denominator is evaluated directly from the original background rather than Taylor-expanded. The large H'' and heavy-current terms that dominated the preceding rest-curvature representation are not deleted: their effects are represented by this exact denominator and the evolved eta_k.

Baseline CDM uses R_c=grhoc/a and its zero current:

    delta_c'=-R_c delta_c/(2H)-k eta_k/H-D_o/(2H),
    eta_k'=Q_o/2.

The remaining sectors include baryons, photons, massive/massless neutrinos and the slow scalar; baseline and MTS exclude different own-subsystem densities but otherwise follow the same construction.

## Prepared sources and tests

Each of the original 902 signed preparation nodes supplies its own u,w,eta_k (or delta_c,eta_k), D_o,D_o',D_o'',Q_o,Q_o'. These come from the saved coupled-equation readouts. No later target is used to choose a coefficient. The three continuations were declared before integration:

1. Primary: D_o=D0+s D1, Q_o=Q0+s Q1.
2. Constant control: D0,Q0.
3. Density-curvature diagnostic: D0+s D1+s²D2/2, Q0+s Q1. This is not a post-selected primary.

These are approximations to other-sector evolution, not new physical laws or exact closures. Initial first and second state derivatives match the retained native derivatives under the unchanged 1e-10 algebra gate for the primary. Constant-coefficient matrix-exponential controls independently test the solver representation. The original source functional and signed increment matching remain unchanged:

    Ybar(s)=Ybar_saved(0)+sum_i weight_i [Y_i(s)-Y_i(0)].

Solver: DOP853 rtol1e-10, normalized atol1e-12, maximum steps duration/32 and /64. The heavy pair keeps its previous phase-amplitude normalization. The extra eta scale is a positive quadratic sum of initial eta, density-constraint contributions and known duration times initial eta derivative; this changes numerical units only, not initial state, physical equations or tolerances.

## Derivation of the remaining error budget

Write X'=A(s)X+B_D(s)D_o(s)+B_Q(s)Q_o(s). For MTS X=(u,w,eta_k):

    B_D=(0,-v/(2H),0)^T,    B_Q=(0,0,1/2)^T.

For baseline X=(delta_c,eta_k):

    B_D=(-1/(2H),0)^T,      B_Q=(0,1/2)^T.

For a terminal density/current/pressure row L_j, lambda_j'=-A^T lambda_j and lambda_j(T)=L_j(T)^T. With identical initial state and background, the exact linear response to external-source errors is

    delta Ybar_j = sum_i weight_i integral_0^T
        [lambda_ij^T B_Di delta D_oi + lambda_ij^T B_Qi delta Q_oi] ds.

If independently established uniform bounds satisfy |D_oi''|<=K_D and |Q_oi''|<=K_Q on every relevant trajectory, the primary's Taylor remainders obey

    |delta Ybar_j| <= G_Dj K_D + G_Qj K_Q,
    G_aj=sum_i |weight_i| integral_0^T |lambda_ij^T B_ai| s²/2 ds.

The two gains are calculated at the final original report using the same backgrounds; signed gains are checked by separate forward forcing integrations, with32/64 refinement. They are numerical, not certified interval enclosures. This identity also predicts the known density-quadratic-minus-linear change without refitting; the prediction agrees with the independently evolved change within the stated numerical allowance.

For final MTS pressure, including the measured gain-refinement allowance:

    9.662590567957012e-6 K_D + 1.1984110932221908e-7 K_Q
        <= 4.753907854071907e-9.

The right-hand side is the remaining original numerical gate margin after the primary residual and existing working allowance. D_o,Q_o have native Mpc^-2 units and their second derivatives Mpc^-4; pressure output retains the original a/R0 normalization. The individual intercepts are K_D=.000491991026696 when K_Q=0, and K_Q=.0396684233061 when K_D=0. They cannot both be saturated together, and neither zero assumption is made.

The largest saved initial |D_o''| is1.0350072939591864e-5 for MTS (baseline1.0328142646639162e-5). These are samples, not uniform trajectory bounds. Q_o'' has not been derived/read out here. Consequently the inequality is a concrete conditional requirement, not a completed uniform certificate. All eight intervals are directly scored, but this gain calculation applies only to the final epoch.

## Reference paths

Retained readouts and previous derivation: ../mts-derived-rest-curvature-20261112/{cold,heavy}-rest-readout.npz and DERIVATION.md.

Original coherent source functional and prepared histories: ../mts-coherent-primitive-20261112/primitive_math.py and {cold,heavy}-initial-state.npz.

Retained background reconstruction: ../mts-integrated-defect-20261112/integrated_math.py and {cold,heavy}-native-clock.npz; original field tables under ../condensate-origin-20261003/native-two-field-transfer-20261007/runs/backgrounds.

Targets are the already-exposed corrected readouts and their working budgets in ../mts-boundary-midpoint-check-20261112. This stage is a short-window numerical validation, not an independent observational comparison or a galactic state-preparation prescription.
