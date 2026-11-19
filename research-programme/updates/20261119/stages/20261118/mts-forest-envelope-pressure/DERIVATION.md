# The high-frequency pressure as a response of the parent field
This is a finite-window linear operator for the **existing positive quadratic heavy mode in the common metric**, not a fit or a new coupling. The mass, fraction, adiabatic state, homogeneous solutions and all standard species come from the retained example. Conformal time τ in Mpc; k, m, and Hc=a'/a in Mpc⁻¹; a dimensionless; c=ℏ=1. Field normalization is exactly that of the native MTSTwoField equations. The density and pressure perturbations denoted d and p below include 8πG a² in native units; they are not Newtonian masses.

## Two different ways of returning gravity
In synchronous CDM-comoving gauge put f=δφ_h, J=δ_c'=-kZ. Then the exact quadratic field and its stress obey

    f'' + 2Hc f' + (k²+a²m²)f = φ' J
    d_h = φ'f' + a²m²φf,    p_h = φ'f' − a²m²φf,    q_h = kφ'f.

In flat space the Einstein energy constraint reads J=−[k etak+(d_other+d_h)/2]/Hc, where etak=kη is native synchronous curvature. Simply substituting live d_h while borrowing etak and d_other from the averaged branch is NOT the whole metric response. It specifies curvature externally as the field stress changes. A second test supplies J entirely from the averaged branch via CDM/baryon continuity (growth accounts for their density-weighted derivative and the baryon peculiar velocity); it is a prescribed-force control, not the self-gravitating result.

A better return is the spatial trace combined with the time-time constraint: h_metric''+Hc h_metric'=−(d_total+3p_total), with J=−h_metric'/2. Therefore

    J' + Hc J = (d_other+3p_other)/2 − a²m²φ f + 2φ'f'.

Seed J from the full energy constraint, not from a fit. Its early response to the instantaneous field *includes the kinetic and potential pressure*, without prescribing the later etak. On the right we supply only the other species from the separately evolved a200 averaged model on the same scale-factor surfaces. This neglects their additional response to the returned fast metric; all-heavy-backreaction and full Einstein/species feedback are not synonymous. The held-out comparison quantifies that approximation on this trajectory. Removing only 3p_h changes the last two coefficients to +a²m²φ/2 and φ'/2. It does not turn off ordinary matter gravity.

The supplied trace contains baryon, CDM, photon, both neutrino sectors and rolling-scalar density and pressure. A readout-only private build exports baryon pressure and the massive-neutrino momentum integral (or evolved pressure moment on its late asymptotic chart). The two replaced diagnostic columns are not cosmological transfer observables in that build. Unmodified columns and homogeneous histories were byte-compared to the normal build on the source run. Late observations always use the unmodified build. Independently, quadrature of (aJ)'=a(d_total+3p_total)/2 is compared to the unmodified energy constraint on the exact trajectory and both cold controls. These are two different ways of calculating the metric expansion.

## Eliminate the hidden field quadratures
On a finite interval the above f,f',J system is linear and affine. Solve two homogeneous initial field quadratures and one driven solution. In each column initialize J by its constraint, including its field-dependent part. These are response basis vectors, **not** three fitted physical modes. Apply the original phase projection to a(d_h,q_h,p_h)/ρ⋆; retain the zero-harmonic polynomial intercept in the presence of the second and fourth carrier harmonics. Each center has

    [D,Q]ᵀ=M v + b,       P=c v + p_0,
    P=(c M⁻¹)[D,Q]ᵀ + p_0−c M⁻¹b.

Here v is the two-component initial field quadrature, not a velocity observable. This gives a conditional pressure law from two averaged moments plus a sourced environmental history. For an independent **time prediction**, infer v only once from the saved D,Q at a200 and use it unchanged at all later centers. Never use later measured D,Q when reporting those forecasts. The code also tests the conditional law separately. None of these operations calibrates P from target pressures. The centered windows at independent epochs are separated from the input window. Numerical solver: conformal time, fourth-stage Gauss–Legendre collocation (order eight), with the step doubled as a control. The incoming density is nonzero at the chosen background switch; normalization uses the same fixed comoving heavy density as the earlier release. No time or frequency tolerances were changed.

The cheap formula P₀=c²(D+3Hc Q/k), c²=[u/(1+√(1+u²))]², u=k/(am), omits both a change in the projected current coefficient and a driven offset. Writing C_D,C_Q,b_P for the response coefficients, the signed correction at fixed D,Q is (C_D−c²)D + (C_Q−3Hc c²/k)Q + b_P. Individual terms can cancel. This split depends on the chosen synchronous variables, not three separately observable forces. pressure-origin.csv contains signed terms, not just their absolute sum. Related literature on the distinction between an oscillating field and an approximate fluid: [Passaglia & Hu (2022)](https://arxiv.org/abs/2201.10238); no numerical coefficient or fit was taken from it.

## Operational switch
Test the predicted defect |P−P₀| on the actual state, divided by the original mode norm, plus a step-refinement allowance. Use the ordinary late fluid only on a continuous-density background interface where this is below 2×10⁻⁶ and where the field density/current time forecast already passed 2×10⁻⁵. The step allowance is an empirical check, not a rigorous uniform bound. Earlier failed simple-fluid interfaces remain explicit failures. The exact field or returned trace bridges them; do not simply change the redshift to conceal them. Repeat the late solution from a second accepted interface to measure ambiguity in the actual gravity, gas and velocity transfers. A local pressure test does not guarantee a global transfer or astronomical flux result.

