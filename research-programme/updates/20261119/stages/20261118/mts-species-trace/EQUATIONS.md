# When can the Hamiltonian constraint and the Einstein trace both hold?

Use the flat retained synchronous scalar chart, x=kτ, k=5 Mpc⁻¹, h=ℋ/k, C=δ_c, u=δφ, β=φ_τ/k, w=u_x, μ=am/k and J=μ²φ. Use D=8πGa²δρ/k², P=8πGa²δp/k², W=8πGa²(ρ+p)/k², and the correspondingly normalized current Q=2η_x, with η=etak/k. The native code's z is −C_x. Do not confuse its derivative with a radiation-streaming approximation. All comparisons are for a single perturbation mode.

The cold+baryon contribution to (D+3P)/2 is half the weighted density contrast; for photons and the massless hierarchy it is the full weighted density contrast. For the massive hierarchy it is Aν Σ w_i (1/v_i+v_i) F₀ᵢ/2, where Aν is the massless reference density in these units, and v_i=[1+(amν/q_i)²]⁻¹ᐟ². There is no baryon pressure term in the original retained Einstein trace; its small sound-speed term is retained in the baryon Euler equation. For each canonical scalar, D=βw+Ju, P=βw−Ju, Q=βu and W=β²: the scalar forcing is 2βw−Ju, not density alone. These are the original metric couplings. No source coefficient is fitted here.

## Defect of the archive, not a new pressure

Differentiate h C_x=−η−D/2, substitute η_x=Q/2, and **keep** every background and stress residual. Define εᵢ=Dᵢ,x+h(Dᵢ+3Pᵢ)−Wᵢ C_x+Qᵢ and B=h_x−h²+ΣWᵢ/2. Then

    C_xx+h C_x = Σ(Dᵢ+3Pᵢ)/2 − Σεᵢ/(2h) − B C_x/h.

Write r=(ln a)_x, which need not equal h in a pretabulated clock. For dust and radiation, εᵢ=(h−r)(Dᵢ+3Pᵢ). For the five-node native massive closure add [Aν(4/3)Σw_i/v_i−Wν] C_x. For scalars u_x=w and w_x=−2hw−(1+μ²)u+β C_x, hence ε_s=(β_x+2hβ+J)w + (J_x−2hJ−βμ²)u. These formulas predict the packet-derived residuals independently; no target pressure is fed into the gap solver.

Friedmann gives 6hB=Σ[ρ̄ᵢ,x+h(ρ̄ᵢ+3p̄ᵢ)], with bars denoting the normalized background densities. For a scalar the summand splits into β(β_x+2hβ+J)+J(φ_x−β)+(r−h)μ²φ². Thus interpolation of the homogeneous field and its velocity as **separate curves** need not respect the energy equation even when interpolated H itself is very close. RMS contributions need not add, since terms have phase. See the individual species entries in the direct JSON records.

## Two independent ways to drive perturbations

At the same complete starting state, evolve log(a)_x=h, φ_x=β, β_x=−2hβ−μ²φ for all active fields; compute h from total density. Compare driving by the algebraic Hamiltonian constraint to integrating C_xx=Σ(D+3P)/2−h C_x. Never replace the evolved C_x of the latter with the algebraic value. η_x=Q/2 evolves in both. Both versions include the full photon, polarisation, baryon, massive and massless hierarchies on this chart. To retain background enthalpy in the **discrete** massive-neutrino monopole metric source, its existing finite-quadrature factor must be Wν/[Aν(4/3)Σw_i/v_i]; the dipole transport coefficient stays −v_i. This is a quadrature consistency correction, not a gravitational coupling. The original raw native five-node calculation is retained and tested separately. Thermal background series, opacity and baryon sound speed are inherited; the latter two remain fixed vs conformal time, not a new recombination solution. This is a conditional Cauchy test of a sector in the retained action, not a new cosmological population prescription.

## Resolving a sparsely sampled source

Take the archived clock and fields (not the newly evolved physical background) for the inverse comparison. Propagate plasma/slow variables from the left and collisionless/heavy variables from the right; keep all 85 massive perturbation moments. The only communication between these two systems is gravity: plasma density and flux one way, C_x and shear the other. This determines a trace history for specified boundary data without inventing native observations in the gap. Unobserved higher photon moments at the left remain a boundary uncertainty. Tests move the boundaries, add a nonzero angular tail, withhold archived interior states, and refine the time integration.

For the previous stage's orthogonally projected kernel K⊥, a force revision d=C_x(new)−C_x(old) has signed residual

    ∫ K⊥ (d_x+h₀ d) dx = [K⊥ d] − ∫ (K⊥,x−h₀ K⊥) d dx.

Here h₀ is the one used to construct the original kernel. The small change from actual h to h₀ is retained. Endpoint constraints have already been projected out: this is the source shape **remaining after** endpoint information, not the total unconstrained error. Compare the species-trace integral and the independent derivative-free drive integral. Split quadrature at thermal, field and nominal-source knots: uniform samples interpolate the metric derivative poorly. No angular-tail assumption or observed calibration is hidden in an unconditional L² bound.

Source map (relative to post-checkpoint-work): the native equations are in mts-coupled-metric-consistency-20261117/native/fortran/{equations.f90,massive_neutrinos.f90,mts_curvature_hook.inc}; clock/field interpolation is in mts-integrated-defect-20261112/integrated_math.py. The retained finite-moment correction is in mts-neutrino-switch-20261118/{switch.c,branches.inc}; projected tolerances are in mts-retarded-displacement-20261118/{TRACE-BOUND.md,cold-trace-bound.json,heavy-trace-bound.json}.
