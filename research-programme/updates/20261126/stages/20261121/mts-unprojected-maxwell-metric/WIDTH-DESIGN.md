# An unfitted change of preparation, frozen before running the two new widths

Keep the toroidal pulse at L_a=L, A=1. Set the poloidal width to b L for b=3/2 and b=2/3. Reduce or increase its amplitude to B=b^(−3/2), keeping **each component's integrated energy** unchanged, not just their sum. The unit fields at launch are those of the parent with the appropriate component length. No force or clock reading is used to select an occupation or coupling. These are prospective internal test cases, not new observations.

Put K=kL=(K_perp,0,Kz) in the rotated plane of an oblique mode. Let v=b²/(1+b²), F_b=(2πv)^(3/2)L³ exp(−v|K|²/2), F_1=π^(3/2)L³ exp(−|K|²/4). The normalized launch spatial stress components xy, zy divided by iABF_b are

    X = −2v³ K_perp² Kz / b²,
    Z =  2v K_perp [2−4v/b²+v² K_perp²/b²].

Derivation: the cross stress is −2(E_a E_p + E_p E_a) at launch; its real-space xy shape is −2AB z(x²−y²) f_a f_b/b², and zy is −2AB x(2−s²/b²) f_a f_b (positions in L). The Fourier moments of the Gaussian product follow by differentiating F_b. Conservation then fixes the initial momentum growth:

    d[ΔJ̃_az/(ABF_b)]/d(t/L) = K_perp X + Kz Z
                            = 4v (b²−1)/(b²+1) K_perp Kz.

The matched-width case is exceptional: that slope vanishes and the saved cubic law takes over. At K_perp=Kz=1/√2 the widened case has slope +90/169 and the narrowed case −40/169. The genuine transverse shear is (−Kz X+K_perp Z)/|K|. The launch is also a test of the vector tide: its normalization equals the longitudinal-transverse shear in the same projection. Density contrast remains zero and no artificial current is supplied.

**Testing plan.** First freeze the stress, physical current, retarded tensor tide and Newton-normalized cross tide at the seven original nonzero modes and nine original times. Integrate the independently propagated free Maxwell spectrum about p=vK, q=K−p, with Gaussian covariance 1/(1+b²); do not read the new real-space source bank or any new metrics. A cross check of the time-zero polynomial and two momentum quadratures is required. Use both independent real-space metric gauges, both signs and the equal-density dust controls for the eventual measurements. Record the early slope, not just sign agreement; the finite-time slope is compared with its own finite-time prediction. Keep 2e-8 absolute on curvature, 5e-8 on source, 1e-12 on differential density in the original F_1 normalization; use 2e-5 relative for nonzero early oblique geometric currents. The independent full metric must not consume these forecasts as a source. Retain any failed predictions.

**Calibrate only once.** The individual dust ruler has inward longitudinal tidal amplitude κρ₀/2. In units of F_1 the initial density equals one half of [A² S(K) + B² b³ exp(−(b²−1)|K|²/4) (4−4S(bK)+S(bK)Z_g(bK)+Q(bK))], with S(q)=1−q_perp²/4, Z_g(q)=1/2−q_z²/4 and Q(q)=2−q_perp²+q_perp⁴/16. This follows by transforming the squared launch fields, not by observing the gravitational response. Thus the signed Fourier cross-tide over the Newton ruler predicts a dimensionless ratio independent of κ. It is a ratio of resolved Fourier amplitudes, not of two forces at one point. At b=1, K=(1,0,0), launch gives 16/51. Keep the signed denominator; do not floor a small Fourier density to improve the score.
