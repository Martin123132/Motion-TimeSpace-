# Direct background-source response

## Physical meaning

Each background difference is computed WITHIN one retained model. It is not MTS minus baseline and not a new observational fit. The source measures how the original native perturbation generator changes when its reference background replaces its retained approximation in one common coordinate frame. Both native generators already use their own conformal H to express rates per N=ln a.

The current approximation is y_c=y_0+eta_normal+eta_map+J_normal+J_map+z_normal+z_map. Dense evaluation now solves the same original mean, slow-source and feedback equations over the first original cell. Their initial states and source normalizations are preserved. DOP853 dense polynomials are saved verbatim in bounded chunks, checked against the original solver evaluator and the previously saved mode values. No simple time cubic is substituted for the oscillatory current.

## Derived driven response and saved adjoints

For E=T^-1(F_ref-F_ret)T,
    v_N=M v+E y_c, v(N_0)=0.
For a terminal row ell and lambda_N=-M^T lambda with lambda(N_f)=ell,
    ell v(N_f)=integral_cell lambda(N)^T E(N)y_c(N)dN.
The adjoint is the existing source-independent mean propagator to the final saved epoch, not a refit to the new source. Its65 endpoint values and equation-derived first/second derivatives provide the already tested quintic interpolation;32-endpoint and coarse-step adjoint controls remain separate.

MTS quadrature follows the heavy-field phase:
    theta_N=Omega=a m_h/H_ret-(3/2)sin(2theta),
    integral_cell=lambda^T E y_c/Omega integrated over theta.
Baseline has no heavy phase and stays in N. Reference and retained physical phases are not identified. The encoded carrier remains common, as in the previous source stage.

At every new quadrature point the original256-angle parent construction supplies the full periodic endpoint P=I+C. The physical and metric maps supply T=S^-1 F P. This does not interpolate a rapidly oscillating source between the failed time-derivative endpoints.

## Exact decomposition of the evolution controls

At the SAME physical N, let E_f,y_f use the fine phase/current history and E_c,y_c use the coarse phase/current history. Then
    E_c y_c-E_f y_f
       =E_f Delta y + Delta E y_f + Delta E Delta y.
All three contributions are retained. The first comes from a direct native evaluation on Delta y; the other two use the same derived phase profile at the coarse phase, with its physical and metric maps recomputed. No profile coefficients or original quadrature points are changed. When the baseline phase degree of freedom is absent, Delta E from this phase-only control is exactly zero; this does not set the baseline background forcing to zero.

## Integration and conditional bounds

For each projected source g=lambda^T E y_f on a cell of N-length L,
    abs(integral g dN) <= sqrt(L integral g^2 dN).
Composite Simpson estimates the signed contribution and this conditional Cauchy budget on nested257/129/65 points. The same controls are reported on the original physical-output scales and on the conditional source budget. Budget-relative checks are not substituted for a whole-theory comparison or an all-time certificate.

The inverse phase grid comes from the saved fine DOP853 phase polynomial. clock_domain.py converts the derivative of each stored polynomial to Bernstein coefficients using exact rational arithmetic on its floating-point input coefficients. An expanded local interval contains the exact represented endpoints. Positive coefficients certify monotonicity of that STORED polynomial throughout the cell. This is not a continuum certificate for the physical ODE. The difference between the polynomial inverse-clock Jacobian and the physical Omega Jacobian is integrated as a separate measure control.

## What remains outside this contribution

This is one original cell and initially the balanced wave family, projected to the existing final epoch. Other cells and wave families remain to be calculated. The final physical output-map difference, response feedback E v and R v, finite pullback discrepancy, inherited initial errors and older source-interpolation uncertainty remain separate. The new source contribution is not added to a full trajectory and declared successful before those terms are accounted for. No parameter, action term, physical input grid, preparation or tolerance is retuned.

