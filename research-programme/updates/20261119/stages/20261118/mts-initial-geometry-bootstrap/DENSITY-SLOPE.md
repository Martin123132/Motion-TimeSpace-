# Closing the weighted ordinary-density slope without differentiating the metric twice in time

Work in the same spherical dust + canonical scalar model. All derivatives below specify their frame. At fixed dust proper time set L=χ∂χ and Z=UJ. Let n be the outward radial unit vector orthogonal to the dust velocity U. In comoving synchronous coordinates ∂χ|τ=a₀ J n: orthogonality to U is initially true and preserved by geodesic motion. In polar coordinates n=W(v/α,1/a). Thus L_R=L R/R=a₀JW/(aA). Its upper bound is 1.07705, with |L_R−1|<0.07705 throughout the trial box. Neither statement treats an equal-coordinate-time derivative as an equal-proper-time derivative.

The crucial cancellation is
    L(M/R³)=L_R[e−v j−3M/R³].
It uses both M_t=−r²Bj and M_r=r²e. There is **no spatial derivative of e** on the right. For Q=(Π²−X²)/a²,
    LQ=L_R[r Q_r+(v/B)r Q_t].
Only the dust interior r≤5.1 is needed to bound its density gradient (outside the surface ρ=0). The wave evolution gives rΠ_t/B=r X_r+2X+r(B_r/B)X−r a²h, rX_t/B=rΠ_r+r(B_r/B)Π. On this domain, |r a_r/a|≤a_*²5.1²(4E/3), |r a_t/(aB)|≤a_*²5.1²E, |rB_r/B|≤a_*²5.1² sup|K|. With the field bounds in WAVE-AND-GEOMETRY.md this gives the two quantities qr, qt_over_b in the executable calculation, upper bounds on |rQ_r|, |rQ_t/B|. In particular the derivative of the field stress is controlled without requiring another unweighted derivative of the dust source.

Differentiate the exact Jacobi equation at fixed label/proper time. Since [U,L]=0,
    U²(LJ)=(2M/R³−Q)LJ + L(2M/R³−Q)J
           −(Lρ₀)/A² + (2ρ₀/A²)(L_R−1).
Initial LJ=U(LJ)=0: the chosen whole initial slice has J=1 and UJ=0, not just at the two probes. Initially ρ₀=D√(1−2M/r); differentiating and using M_r=r²e gives |Lρ₀|≤2(5/6)^5 Dmax + Dmax a_*5²(4E/3). Here max |rD'| is from the actual polynomial dust profile. The wave term in L(2M/R³−Q) is bounded by L_R,max(qr+vmax qt_over_b); the mass term by 2 L_R,max[(1+vmax)E+E]. With k_J=2E/3+2ε and total forcing F_J as evaluated in bootstrap.py, Volterra comparison yields |LJ|≤F_J[cosh(√k_J T)−1]/k_J<0.09279. No dust velocity-gradient closure was inserted.

For ρ=ρ₀/(JA²), use
    |Lρ|≤ |Lρ₀|/(Jmin Amin²)+ρmax[|LJ|/Jmin+2|L_R−1|],
    |Uρ|≤ρmax[|Z|/Jmin+2|UR/R|],
    rρ_r=aW[(A/(a₀J))Lρ−r v Uρ].
The last identity uses the inverse boost and is evaluated at fixed polar time. The resulting **strict** bound is |rρ_r|<0.000903 against the proposed 0.003. Combined with the other strict margins and N(0)exp(kT)<0.001, continuity rules out a first exit at or before T. At the initial slice these bounds follow directly from the constraints, the maximum initial norm, ρ₀, and rest initial data; the regular centre is obtained by parity. Replacing the weighted derivative by an unrestricted numerical V_r maximum was neither necessary nor used.

