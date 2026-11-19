# Surrounding-current curvature from the retained equations

## Scope and conventions

Native conformal time is measured in Mpc with c=1; D and Q have native Mpc^-2 units, and their second derivatives have Mpc^-4 units. Retain r=a'/a separately from the native conformal H. The heavy field/CDM subsystem and eta_k already evolve together. Q_o excludes the heavy scalar for MTS and CDM for baseline, not the other species.

Authority: ../mts-derived-rest-curvature-20261112/native/fortran/equations.f90, results.f90, massive_neutrinos.f90 and MTSTwoField.f90, with the original160-column packets. A private read-only export supplies only missing current derivatives. All original160 columns at all910 rows match byte-for-byte for both cases; no evolution equation or original file changes.

The actual captured regime is non-tight-coupled photons with delta_p_b=cs2 delta_b at every row for both cases. All910 rows have both tightcoupling=false and Evolve_baryon_cs=false. Unsupported branches are rejected rather than evaluated with these formulas. Massive neutrino momentum bins are retained; the relativistic-tail implementation is preserved, though the captured window has zero tail bins. No massless-neutrino substitution is made.

## General weighted-current identity

For Q_j=R_j q_j with R_j proportional to a^(-p):

    Q_j''=R_j[q_j''-2p r q_j'+(p²r²-p r')q_j].

p=1 for baryons, p=2 for photons and neutrinos' prefactor. CDM current remains identically zero. Differentiation uses actual background derivatives, not a conservation identity that would erase interpolation defects.

## Baryons and photons: preserve collision cancellation

Let C=R_gamma/R_b (so C'=-rC), kappa the native opacity, P=delta_p_b=cs2 delta_b, S=4v_b/3-q_gamma, and c1=EV%denlk(1), c2=EV%denlk2(1). The retained non-tight-coupled equations are

    v_b'=-Hv_b+kP-C kappa S,
    q_gamma'=c1 delta_gamma-c2 pi_gamma+kappa S.

The native implementation computes the second line through its momentum-conserving equivalent (-v_b'-Hv_b+kP)/C+c1 delta_gamma-c2 pi_gamma. Both forms are checked. Differentiate:

    P'=cs2' delta_b+cs2 delta_b',
    v_b''=-H'v_b-Hv_b'+kP'
           -C(kappa'-r kappa)S-C kappa(4v_b'/3-q_gamma'),
    q_gamma''=c1 delta_gamma'-c2 pi_gamma'
              +kappa'S+kappa(4v_b'/3-q_gamma').

To avoid losing collision cancellation, combine the weighted first derivatives before differentiating:

    (Q_b+Q_gamma)' = R_b[-(H+r)v_b+kP]
                    +R_gamma[c1 delta_gamma-c2 pi_gamma-2r q_gamma].

Hence the stable paired curvature is

    (Q_b+Q_gamma)'' =
      R_b[-(H'+r')v_b-(H+r)v_b'+kP'
          +r(H+r)v_b-rkP]
      +R_gamma[c1 delta_gamma'-c2 pi_gamma'-2r' q_gamma-2r q_gamma'
          -2r(c1 delta_gamma-c2 pi_gamma-2r q_gamma)].

Explicit kappa and kappa' cancel from this combined expression; the retained collision physics remains in the actual v_b',q_gamma'. This is not deletion of scattering. The separately differentiated baryon/photon curvatures agree with this stable sum under the unchanged1e-10 algebra gate.

cs2' and kappa' are derivatives of the actual Hermite interpolants: for x=ln(tau/tauminn)/dlntau and cell polynomial f=f0+d(s0+d(A+dB)), f'=[s0+2Ad+3Bd²]/(tau dlntau). Do not replace this with the separately interpolated legacy opacity derivative. Their maximum absolute differences are3.51383e-12 baseline and2.14252e-8 MTS in native derivative units; the legacy interpolation itself is untouched. The paired-current formula removes explicit sensitivity to that derivative representation.

## Neutrinos

Massless dipole: q_r'=c1 delta_r-c2 pi_r, so q_r''=c1 delta_r'-c2 pi_r'. Use native pi_r', retaining its actual hierarchy closure.

For a resolved massive-neutrino momentum, v_q=[1+(am/q)²]^(-1/2), v_q'=-r v_q(1-v_q²):

    F1'=v_q(c1 F0-c2 F2),
    F1''=v_q'(c1 F0-c2 F2)+v_q(c1 F0'-c2 F2').

The momentum-current weight is A kernel with A=grhormass/a², without a density-like1/v_q factor. Its curvature contribution is

    A kernel [F1''-4rF1'+(4r²-2r')F1].

For the retained relativistic tail, F1=q_r+c q_corr, c=(m/q)²/2. Differentiate the native correction equation

    q_corr'=-a²(c1 delta_r-c2 pi_r)+c1 delta_corr-c2 pi_corr,
    q_corr''=-a²[2r(c1 delta_r-c2 pi_r)+c1 delta_r'-c2 pi_r']
              +c1 delta_corr'-c2 pi_corr'.

That path is checked by an independent synthetic identity, not advertised as a nonzero-tail numerical test of this window.

## Scalars

For each retained scalar, Q=kvu, u'=w, u''=w':

    Q''=k(v''u+2v'w+vw').

v'=r v_N and v''=r'v_N+r²v_NN use the actual saved background splines. The slow scalar is retained in Q_o for both cases; the heavy scalar is excluded only from the MTS surrounding source because it already feeds live eta_k. Both scalar curvatures are exported and independently reconstructed.

## Frozen continuation and budget

Use Q_o(s)=Q0+sQ1+s²Q2/2 alongside the already-derived quadratic D_o(s). Each of902 coefficients Q2 is frozen before scoring. The only additional live-system forcing is eta_k' += s²Q2/4, since eta_k' includes Q_o/2. Preserve the same normalized states, backgrounds, weights, reports and solver tolerances. Reuse the previous linear and density-quadratic results rather than recomputing them.

From the saved two-channel signed adjoint gains:

    Delta Ybar_j=sum_i weight_i [g_Dij D2_i+g_Qij Q2_i].

This independently predicts the complete quadratic-minus-linear correction and the current-only increment. Both comparisons pass with the explicit numerical/refinement/rounding allowance. A conservative envelope for this FROZEN quadratic forcing is

    E_j=(G_Dj+delta G_Dj) max_i |D2_i|
         +(G_Qj+delta G_Qj) max_i |Q2_i|.

MTS initial maxima: K_D_sample=1.0350072939591864e-5, K_Q_sample=1.0272002367743577e-5. E_pressure uses .02129606387632497 of the saved linear pressure margin, about2.13%. Baseline density uses1.001329088340777e-7 of its corresponding margin. This is a test of the actual frozen correction and its response, not evidence that these sampled maxima bound the uncomputed continuous histories.

## Remaining continuous remainder: correct mathematical form

No current-curvature coefficient is missing at the prepared nodes now. The outstanding issue is its variation between saved epochs, and the analogous density remainder. For the quadratic continuation the exact integral remainder is

    e_Q(s)=integral_0^s (s-t)[Q_o''(t)-Q_o''(0)] dt,
    e_D(s)=integral_0^s (s-t)[D_o''(t)-D_o''(0)] dt.

This form remains useful across the retained piecewise interpolation cells. Do not assume a globally smooth third derivative across thermal interpolation corners. Bound or directly validate these variations with the relevant cell boundaries included, then propagate them through the saved two-channel response. The earlier linear-source sufficient inequality remains available if a coarse genuine uniform bound on full D_o'',Q_o'' is easier. Sample maxima alone establish neither bound. Gains currently cover only the final epoch; final-source comparisons cover all eight intervals.

## Readout layout

The first160 packet columns are unchanged. The new64-column block (Python packet[:,160:]) has:0:7 component Q'' in CDM,baryon,photon,massless-neutrino,massive-neutrino,slow,heavy order;7 stable baryon+photon Q'';8 Q_o'';9 totalQ'';10/11 regime flags;12/13 cs2,cs2';14:17 opacity,exact opacity',legacy opacity';17:23 velocity/current first and second derivatives;23 P';24/25 native c1,c2;26/27 photon shear and derivative;28/29 massive-dipole RHS error/scale;30 thermal-clock difference;31 tail-bin count;32/33 baryon/photon RHS reconstructions;34 independent differentiated native photon equation;35 massless RHS;39 supported-regime flag. Other slots are unused zeros.
