# A conditional local initial state, not a new equation of state

The resolved cosmology already stores the canonical slow scalar's field, conformal derivative and mass on both branches. Before a local response is computed, our prediction is: its positive background enthalpy (φ'_s/a)² in 8πG units will supply an inward momentum change and/or a signed pressure difference balancing **its own** part of the missing-source forecast in SMOOTH-SOURCE.md. It need not equal the entire untracked enthalpy (radiation, massive neutrinos, tabulated expansion accuracy). Record its fraction, both signed pieces and the residual. Do not infer that a uniform-density comoving fluid is a canonical scalar.

Use the existing minimally coupled quadratic action and the *already evolved* metric. In units in which φ includes √(8πG), the canonical density per comoving r² is π=ℓ³ ∂ηφ/α. Then φ'=απ/ℓ³ and π'=r⁻² ∂r(r² αℓ ∂rφ)−αℓ³m²φ, where primes on field variables here denote conformal time. Define q=φ−φ_b and d=π−a³W_b, W_b=φ'_b/a. Initialize exactly q=0, W=W_b, so d=a³W_b[exp(−3V)−1]. This is conditional homogeneous *normal-velocity* preparation at the beginning of each short window; a growing mode extrapolated from formation could start differently. The matched scalar background evolves with the same table of scale factors, ∂η(a³W_b)=−a⁴m²φ_b. Splitting off that exact evolution gives

    ∂η q = e^(U+3V)d/a² + a W_b expm1(U+3V),
    ∂η d = a²/r² ∂r[r² e^(U−V) ∂r q]
           − a⁴m² [e^(U−3V)q + φ_b expm1(U−3V)].

Initially j_r=−W ∂r q=0 but ∂η j_r=−W_b²∂rα. For an ordinary cosmological constant this term instead vanishes. At finite time set ΔJ=½∫dr Δj_r and B=½∫dη [α (P_r−P_b)]_lo^hi. Independently compute the homogeneous drive S=½∫dη a W_b² [N]_lo^hi. Momentum balance predicts ΔJ+B+S+small=0, with

    small = ½∫dη dr [3(∂η ln ℓ)j_r + α U' (E−E_b) + 2α(1/r−V')Π].

Test both actual finite-time terms, not just an instantaneous identity. Control: nested uniform time and radial steps, alternate edge condition with the whole test region outside the edges' light cones, zero metric perturbation (q=d=0), repeated initial signs and normalization. Compare on the unchanged original trace scale, and also against the much smaller slow-field drive so the large material terms cannot hide a bad scalar test. The scalar evolves here **on** the nonlinear history; it is not fed back into the recorded metric or used to rewrite the old results. A coupled solution must also account for δE, j_r, δP_r when solving the constraints and evolving the other fields; the momentum balance of this individual field is a separate test. No free pressure or smoothing amplitude is introduced.

Independent wave control: set a=1, m=0, W_b=1, V=0 and U=ε j₀(kr), j₀(s)=sin(s)/s. To first order in ε, δφ has zero initial value and initial time derivative U. The spherical wave equation gives q=U sin(kη)/k, d=U[cos(kη)−1]. Thus with A=ε[j₀(k hi)−j₀(k lo)]/2 the three independent finite-interval targets are ΔJ=−A sin(kT)/k, B=A[sin(kT)/k−T], S=AT. The implementation evolves the exponential lapse, not this series. Use ε=10⁻⁷, k=32 Mpc⁻¹ and test each piece on |AT|, not their already vanishing sum.
