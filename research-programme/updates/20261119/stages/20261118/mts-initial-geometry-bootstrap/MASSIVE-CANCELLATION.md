# Keeping the mass oscillation cancels enough error to certify the actual 1/160 packet

The simple characteristic absolute-value estimate loses a factor exp(T) even for a free massive wave. It misses the previously saved test state. The following repair uses the *same* classical equations, profile, first-exit box, proper times and tolerance. Nothing is adjusted to its measured trajectory.

On the regular half-line in reduced Compton units put
    Y₀²=∫(p²+u_r²+u²)dr,   Y₁²=∫(p_r²+u_rr²+u_r²)dr,   Eᵢ=Yᵢ²/2.
These are flat-weight energies used to **estimate** the curved-metric solution; they do not replace its field equation with the flat one. Integration by parts (all boundary terms vanish by regular parity and isolation) gives
    E₀,t=∫[B_r p u_r+(B−V)u p]dr,
    E₁,t=∫[3B_r p_r u_rr+(B−V)p_r u_r+B_rr(p_r u_r+u_rr p)−V_r p_r u+B_r u_r p]dr.
The carrier term cancels in both identities on the exact flat massive operator B=V=1. In a weak curved metric it costs |B−V|≤2M/r+|K| rather than order unity. There are *no* B_t,V_t coefficients to obtain from an evolved history.

Let b,b₂,d,g,k denote respectively upper bounds for |B_r|, |B_rr|, |B−V|, |F_r|(1+sup|K|), and |rK_r| on the low-order first-exit box. From V=F(1+K), F≤1, the potentially singular term involving K_r is bounded by k||p_r||₂||u/r||₂≤2k||p_r||₂||u_r||₂ using Hardy on the half-line (integrate (u²/r)' and apply Cauchy-Schwarz; u(0)=0). Thus
    Y₀'≤a₀Y₀,  a₀=(b+d)/2,
    Y₁'≤a₁Y₁+cY₀,   a₁=(3b+d+b₂+2k)/2,  c=b₂+g+b.
Use continuity when either norm vanishes. For all t≤T take X₀=exp(a₀T)Y₀(0), X₁=exp(a₁T)[Y₁(0)+cTX₀]. In particular |u|≤X₀, |u_r|≤X₁ and |p|≤√(2X₀X₁) by one-dimensional Sobolev; |u/r|≤X₁ by regularity. If W=√(2X₀X₁)+X₁, the *differentiated characteristics only* now give
    |z±|≤exp(2bT){N(0)+T[b₂W+(1+sup|K|+k)X₁+gX₀]}.
Unlike a total-energy smallness assumption, this actually controls central gradients. This last bound at λ=1/160 is **0.000960432 < 0.001**; X₀ and W are smaller. The density, compactness, lapse, speed and shell bounds already improve on this box. Therefore the simultaneous first exit cannot occur. No simulation extrema, no source-amplitude reduction from 1/160 and no bound on the old integrated metric-growth coefficient are required.

**Initial data provenance.** With the prescribed dust source, the Newtonian potential is polynomial inside its radius and −M_b/r outside. Hence r times the normalized prepared correction is polynomial on every interval delimited by 0, 5, 10, 15, 16, 26. initial_polynomial.py constructs it from the two Poisson integrals, not from the simulated initial energy, and integrates squared derivatives as exact rationals. This gives Y₀(0)=0.00026796707 and Y₁(0)=0.00005208104 for the saved packet; massive_budget.py uses only initial profiles and first-exit algebra. The finite-grid parent uses numerical radial integration for that prescription. These are a continuum bound and a separately discretized check, not bitwise identity of two representations.

**Off-centre rulers.** On r≥R* the same norms give ε=[2X₀X₁+2X₁²+(1+2/R*²)X₀²]/(2R*²). Do not use that annular bound for matter at the centre: the initial enclosed scalar mass is independently ≤E₀(0), since a≥1 and ∫r² h_r²=∫u_r² for this isolated packet. Insert these two inputs into the previous stage's comoving comparison. For the 1/160 state, the radial/angular ceilings are 4.474e-6 / 2.042e-6 at 2.5 and 3.484e-7 / 1.681e-7 at 6 (rounded upward). All four are below 2e-5. The direct 1/160 measurements are ~9e-11, so the new bound is safe, not tight. The unrestricted full-strength packet does not satisfy the sufficient first-exit test; its simulated small effect is still a separate result. In particular the mathematical amplitude range is not an astrophysical population prediction.

