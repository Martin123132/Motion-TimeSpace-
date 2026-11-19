# Preparation-owned phase-corrected initialization

This composes the retained general-k code with the ORIGINAL k=5 saved coherent field, original normalization and 902-node signed projection. It does not invert two averaged fluid numbers, select a phase, fit pressure or reinterpret the signed weights as a positive ensemble. The preceding fixed-center moment construction is a separate source-compatible representative and a useful failed shortcut test, not a replacement for this carrier.

Let L[f]=sum_i w_i f_i be the frozen a225-w6-d8 extraction. The native b_i,v_i,u_i,wfield_i,H_i and a_i come from the original preparation. beta_i=a_i/R0, mu_i=a_i*m, k=5/Mpc. Write the previous stage's exact primitive-to-normal map as M_i and its physical density/current/pressure readout as R_i. The retained zero-mean micromotion gives P_i=I+K_i, using the actual phase atan2(-v_i/mu_i,b_i) and E_i=beta_i*(v_i^2+mu_i^2*b_i^2)/2.

The native force separates as

    zeta_i = z_i - Dnative_i/(2*k*H_i),
    x_i = (M_i*(u_i,wfield_i), zeta_i),
    y_i = inverse(P_i)*x_i.

zeta is the existing rest-species metric readout, not a new field or population. Its reconstruction uses the saved growth identity documented in DERIVATION.md. The third row of P is the identity. No separately fitted force is added.

Define the matching carrier and its retained unresolved preparation by

    y0 = L[y],  delta_y_i = y_i-y0,
    T_i = R_i * first_two_rows(P_i),  T0 = L[T_i].

Because L[1]=1, L[delta_y]=0, but generally L[T*delta_y] is NOT zero. The exact physical matching sources are

    Y0 = T0*y0 + C0,
    C0 = L[T_i*delta_y_i] = L[(T_i-T0)*delta_y_i].

This is a constructive initialization: both y0 and the entire delta_y packet are recovered from saved preparation, and C0 follows from their product rather than from a pressure discrepancy fit. A representative simultaneous multi-field state is neither required nor inferred. This memory is a history/projection correlation; it is not an independently observed galaxy occupation or a claim of extra fundamental degrees of freedom.

The normalized canonical source triplet additionally contains the known gauge readout

    g_i = beta_i*(-3*eta_i*v_i^2,
                   k*alpha_i*v_i^2,
                  -3*eta_i*v_i^2-2*alpha_i*mu_i^2*b_i*v_i),
    Ycanonical_0 = T0*y0 + C0 + L[g].

This is the canonical Dstar, Q, Pstar triplet. It is not the full Newtonian-gauge physical density/pressure, whose existing metric additions remain as in the prior stage. Gauge conversion is evaluated before averaging; no products are silently commuted.

## Computed state in retained units

    a0 = 0.00022501566262210325
    R0 = 2.479342985570997e-08  [native density normalization]
    y0 = (-0.047032046604023284,
           0.03434319348000285,
          -0.03441290465105713)

The last component is zeta. The normal source pair is dimensionless in the original rescaled perturbation convention. All times, H, mu and k retain the native conformal/Mpc convention. No observational amplitude has been refitted. The maximum micromotion matrix condition number is 1.0770523490645536.

    T0*y0 = (-0.047033501485096094,
              0.03453240449162986,
             -0.00025472265505696975)

    C0 = ( 1.3105681969083294e-08,
          -1.031989837643703e-06,
           9.145341456793352e-07)

    Y0 = (-0.04703348837941416,
           0.03453137250179223,
          -0.00025380812091127926)

All three Y0 components reproduce the historical matching sources; the largest component-relative difference is 6.002e-14 (pressure). Keeping only y0 would discard C0: current then differs by 2.9885e-5 and pressure by 3.5903e-3 using the unchanged max-magnitude relative comparison. Both exceed 2e-5. This is why zero-memory matching is not a valid substitute for the saved preparation.

## What is now initialized, and what still requires transport

carrier-initial-state.npz retains the phase-corrected 902-node preparation, y0, delta_y, T_i, C0 and canonical gauge offsets, with original indices/weights. matching-state.npz separately retains the moment representative and exact projected-rate remainder. The cold baseline uses its own saved dust normalization and identity source chart; it receives no scalar phase or pressure.

The initialization fixes the omitted source contribution at this matching boundary. It does not supply its future values by fiat. In particular neither C(t)=C0 nor delta_y=0 is justified. One must transport the recovered initial memory through the current-state equations, or derive a controlled memory kernel, before replacing the late native heavy block. A late restart at z10 cannot be obtained just by copying these a0 values across the intervening expansion.

The bare moment-rate failure in DERIVATION.md/RESULTS.md tests a simpler local representative; it does not test or reject the retained phase-corrected memory law. The latter is the route to carry forward.
