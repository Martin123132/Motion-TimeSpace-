# A controlled scalar-to-ordinary limit of a physical launch tide
This is about the coupled retained constraint and a matched round release, not about all subsequent times or the existence of a full quantum theory. Keep conserved material D and charge Q=ηN fixed, keep the same smooth balanced specific angular momentum ℓ(N), set the neutral scalar to h=A H(r) with fixed smooth compact H, vanishing normal velocity and no independently imposed even wave. Vary A, not ℓ or G. The ordinary comparison is the *same* charged Einstein–Maxwell–dust solution at A=0. The conformal-label preparation is used here; shell preparation has a different scalar Eulerian perturbation.

**The background dependence is controlled, not assumed negligible.** Write μ=m+Q²/(2r), b²=1−2μ/r+Q²/r². The spherical Hamiltonian is
    μ'=r²[D b+(b² h'²+h²)/2]+ηr D Q.
Subtract the two equations, using b₀−b_A=2(μ_A−μ₀)/[r(b_A+b₀)]:
    (Δμ)'+[2rD/(b_A+b₀)]Δμ = (A²/2)r²[b_A² H'²+H²],    Δμ(0)=0.
The integrating factor is positive. So 0≤Δμ≤A² E_H(r), E_H(r)=½∫₀ʳ s²[b₀²H'²+H²]ds, and b_A≤b₀. Let b₀≥β₀>0. If β²=β₀²−2A² sup(E_H/r)>0, continuation from the regular centre gives b_A≥β without first assuming that the perturbed geometry stays outside a horizon. A useful explicit ordinary lower bound for the present D≤D₀, total M and |η|≤1 is β₀²≥1−2m*−η²m*² where m*=(D₀M²/3)^(1/3): use m₀'=r²D b₀+Q²/(2r²), m₀≥0, b₀≤1 and N/r≤m*. Thus d=‖b_A−b₀‖∞≤A² sup(E_H/r)/β and dᵢ=‖1/b_A−1/b₀‖∞≤d/β². The estimates are finite for fixed regular compact H.

**What cancels from the even source.** The positive elliptic form has coefficients p_A=r²b_A and
    q_A=r²D+(6+Q²/r²−r²h²)/b_A.
The forcing in divergence form is F_A=Dℓ²/6+2J²/(3r⁴b_A), J=∫ℓdN. The matter kinetic part of the forcing is *identical* between branches, as is the r²D term in q. Let the flat energy norm be ‖v‖²=∫(r²v'²+6v²)dr. A positive coercivity constant is κ_A=min(inf b_A,inf q_A/6), and Λ_A=max(sup b_A,sup q_A/6) bounds the form from above. For sufficiently small A, κ_A remains positive. A form-difference constant is
    δ=max(d, [(6+‖Q/r‖∞²)dᵢ+‖rh‖∞²/β]/6)=O(A²).
These bounds do not assume the two numerical metrics or transfer functions are identical.

**Two different strengths of result.** At launch the P₂ coefficient of Ric(n,n) is 4Ru_A h h' on the matched sphere. In the ordinary branch it is zero. The positive Green diagonal argument from ANY-BALANCED-CURRENT gives |u_A(R)|≤C_A W/(5R κ_A), R≥S, with C_A=1/2+D₀ S²/(5β). Thus the *pole-minus-equator* trace difference, or minus the initial acceleration of directional log-volume, satisfies
    |Δ Ric(n,n)| ≤ 6 C_A W |h(R)h'(R)|/(5κ_A).
This is a uniform O(A² W) bound for arbitrary smooth balanced rotations of bounded proper kinetic energy. It vanishes exactly at a zero or extremum of h, even when there is a traceless tide. The shell-prepared result has zero initial trace contrast for a different reason (δh on the matched shells vanishes); do not translate either statement into an absence of all later signals.

For the radial sectional tide distinguish a fixed smooth rotation from an arbitrary sequence concentrating its energy at the origin. Flat evaluation gives |v(r)|≤‖v‖/√(5r). Define
    N₀=∫ F₀/√(5r) dr,   D_F=(2dᵢ/3)∫ J²/(r⁴√(5r)) dr.
Both moments exist for a regular fixed current. Subtract the two weak elliptic equations: the right side contains ΔF and the difference of forms acting on u₀. Coercivity gives
    |u_A(R)−u₀(R)| ≤ UΔ=(D_F+δ N₀/κ₀)/(κ_A√(5R)).
This is O(A²) at fixed current, uniformly for families with those moments bounded; this estimate alone does **not** claim a W-only uniform radial convergence rate. For source-free R≥S let d_R=−u'/u=γ_R/(R²b_R). The exterior variational characterization yields |γ_A−γ₀|≤δγ₀/κ₀, γ₀≤3RΛ₀. Hence d_{R,A}≤3Λ_A/(Rβ) and |Δd_R|≤3Λ₀[δ/(κ₀β)+dᵢ]/R.

On the matched sphere E₂=(C−4f d_R/R)u, where C=−12/R²−4m/R³+2Q²/R⁴+2h²+(6f+2Rf')h'²+4R f h'h''. The fixed-current pole-minus-equator radial difference is bounded by
    (3/2){ (|C_A(section)|+4f_A d_max/R) UΔ
           +[|ΔC|+4(|Δf|d_max+f₀ |Δd_R|)/R] |u₀(R)| }.
Here d_max=3Λ_A/(Rβ); C_A(section) is the local radial coefficient, not the earlier source-integral bound. ΔC and Δf are O(A²) by the spherical result and regularity of H,H',H''. Thus the *physical radial launch response*, not only a parameter in the action, tends to its ordinary value as A→0. This argument uses the retained Einstein kinetic term and minimal matter coupling. It provides a controlled local observable limit and identifies explicitly the preparation and norm assumptions on which it rests.
