# A positive collision balance for the photon angular hierarchy

Use the coupled intensity F and polarization E from the kinetic restart, not the archived shortcut E₂=π/4. Normalize inner-product weights so the photon dipole F₁=4v_γ/3 carries v_γ²/2. Antisymmetry of adjacent streaming terms then fixes w_F(l)=3(2l+1)/16. Symmetry of the Thomson quadrupole matrix in that inner product fixes w_E(2)=6 w_F(2); for l≥2 the streaming recurrence fixes w_E(l+1)/w_E(l)=(l+3)(l−1)(2l+3)/[(l+1)²(2l+1)]. There is no fitted weight.

Let A be half the weighted sum of squares of all l≥2 moments. The zero-high-moment boundary makes internal streaming cancel. In x units, the exact finite-hierarchy identity is

    A_x = w_F(2) (8/15) F₂ (v_γ+σ_metric) − D₂ − D_high,
    D₂ = w_F(2)/L [3 F₂²/4 + 12(E₂−F₂/4)²/5],
    D_high = sum_{l≥3} [w_F(l)F_l²+w_E(l)E_l²]/L.

This positive quadratic dissipation is an angular **norm** of linear photon brightness and polarization relative to isotropy, in a dipole-matched normalization. Do not equate it with heat deposited in baryons, a y distortion, or total second-order covariant stress-energy. Its separation from S²/L is necessary before trying to make that physical identification.

Use the same common x window as the work test. For every solved state evaluate A_x separately from the differential hierarchy. Integrate the signed source, positive terms and dipole drag on the saved trajectory. Use degree-seven local interpolation as a sampled-data quadrature with lower degrees and removal of alternate knots as controls; check baseline, MTS, both differential solvers and the erased startup. Do not omit zero crossings or substitute the positive integrand for the signed net storage. Test on the stored-energy change as well as on the scale of the injected norm. The higher-order polynomial here is offline quadrature, not a modification of any source history.
