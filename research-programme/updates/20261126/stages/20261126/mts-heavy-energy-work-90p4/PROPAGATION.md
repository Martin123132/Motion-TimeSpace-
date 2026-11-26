# Constraint propagation after cancelling the common metric work

This is a follow-up to the frozen explicit-energy attribution. It changes variables, not trajectories or the tolerances. A large projected term is not a missing force if the constraint already carries its opposite.

**Total identity.** Split the coefficient of the energy constraint into D=κ+Σd_s. On these histories the contributions are (4eγ+3eb)/2 for the coupled photon–baryon variables; 3ec/2 for cold matter; 3v_s²/2 for the light scalar; 3v²/2 for the explicit heavy scalar; zero for its companion; and (4er+νE)/2 for the remaining relativistic population. The prefactors use the retained code's rescaled energies, not unrescaled physical densities. Define A=κ−D+3(H²−H′). For each component define

    S_s = −E_s′−HE_s−J_s−3H(J_s′+2HJ_s)/κ
          −2(d_s′+Hd_s)Φ + 2Hd_s Ψ.

Using the energy constraint, Σ[E_s+2d_sΦ+3HJ_s/κ]=2(U−κΦ). Split DHΨ into κHΨ+Σd_s HΨ. Substitution directly into D(Φ_E′−P_J) gives

    D R = U′ + H U + κH(Ψ−Φ) − D Fq + A J/(2κ) + ½ Σ S_s.

No individual S_s is required to vanish in an interacting, externally driven perturbation. Only their balance with the displayed geometric sources tests propagation of this particular constraint on this trajectory. Writing an identity is not evidence the two routes agree.

**Scalar simplification.** J_h=κv f+q_J and d_h=3v²/2. In −E_h′−2d_h′Φ the rapid terms −6BvΦ and −6vv′Φ combine to (12Hv²−6v r_v)Φ. Substituting the independent f′,w′ in S_h then cancels the remaining common lapse, gradient and homogeneous scalar work. What is left is

    S_h = (2H M²−(M²)′) b f − M² r_b f − r_v(w+3Hf+6vΦ)
          −(B+3Hv)q_f − v q_w − (q_E′+H q_E)
          − q_J − 3H(q_J′+2Hq_J)/κ.

No inverse power of v or division by a wave zero occurs. For the companion the prior exchange law gives independently

    S_comp = (a′/a−H)(δE+3HδJ/κ).

These two predictions use the input histories and field variables, not the total measured constraint residual. The total balance test uses the retained other sectors' equation-derived rates, calculates d_s and its derivatives from the source bank, and compares the resulting signed photons to the prior density residual. For a separate control compute each S_s without the scalar simplification, and retain both branches before taking the difference. No term is removed from the current theory.
