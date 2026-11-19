# How the common-metric contact changes both the source and its clocks

**Input and scope.** Take the two total-stress operators in the retained reduced 4964 basis, in the sign and unit conventions of the sealed predecessor's EM-AND-SOURCE.md. Write their additions to the matter Lagrangian as γ₁(T:T)/4 + γ₂(Tr T)²/4. Here T is the leading stress of the charged dust, electric field and real massive scalar on the same metric. The ideal clocks/light are test probes, not another contribution to the evolved source. Keep only first order in either γ. This is not an assumption that the matter operators, or the local wave occupation, have been measured.

**From action to source.** Use spherical synchronous coordinates with radial proper length a dx and areal radius R. In code units 4πG=1, scalar mass=1. Let Π=p_h/(aR²), s=∂ₓh/a, n=N/(aR²) be the Eulerian dust *number* density, w=p_d/a, Γ=√(1+w²), D=Q/R². In the local radial orthonormal frame the leading energy, two principal pressures and outward momentum are

    e=(Π²+s²+h²+D²)/2+nΓ,      p=(Π²+s²−h²−D²)/2+nw²/Γ,
    t=(Π²−s²−h²+D²)/2,          j=nw−Πs.

The Legendre transform at fixed canonical momenta inserts minus the first Lagrangian variation. Hence the change in Hamiltonian per proper volume is Z₁=−(e²+p²+2t²−2j²)/4 or Z₂=−(−e+p+2t)²/4. Squaring the *total* stress generates the mixed terms, including the contractions with the electric field; adding only the scalar self-pressure would not do this. At fixed canonical variables the sources are

    δe=Z,   δp=−Z+Π Z_Π+s Z_s+n Z_n+w Z_w,
    δt=−Z+Π Z_Π+n Z_n+D Z_D,      δj_explicit=0.

These follow by varying aR² Z w.r.t. a and R separately at fixed canonical momenta and charge. They do not hold local velocities fixed. Rather, proper field rate, material speed and electric field are Π+γZ_Π, w/Γ+γ Z_w/n, and D+γZ_D. This resolves the apparent discrepancy with the predecessor's covariant fixed-velocity stress variation. The boost identity Γ Z_w + n(w/Γ) Z_n − s Z_Π − Π Z_s=0 holds identically for both choices: flux and canonical momentum agree to first order, not just on a static fixture. action_checks.py independently differentiates the invariants and varies both physical scale factors.

**Evolution and matching.** With H=e+γZ, J=aR², Kᵣ=−ȧ/a, Kₜ=−Ṙ/R and η=0.8, the matter equations are

    ḣ=H_Π,      (JΠ)·=∂ₓ(R² H_s)−J H_h,
    Ṅ=−∂ₓ(R² H_w),   Q̇=−η R² H_w,    ṗ_d=−∂ₓ H_n+η a H_D.

The ∂ₓ H_n is the total spatial derivative evaluated on the solution. Outside dust support Z_w/n denotes its regular analytic continuation; no new particles are placed there. Einstein gives ṁ=−R²(p_tot Ṙ+jRₓ/a), mₓ=R²(e_tot Rₓ+ajṘ). With k=−ȧ the useful clock equation is k̇=a(e_tot−p_tot+2t_tot−2m/R³). Both radial and angular geometry evolve. The two local weak balances are ∂τ(Je_tot)+∂ₓ(R²j)=J(p_tot Kᵣ+2t_tot Kₜ) and ∂τ(Jaj)+∂ₓ(Jp_tot)=J(p_tot aₓ/a+2t_tot Rₓ/R). In a finite numerical excursion the chosen truncated Hamiltonian has an O(γ²) boost defect; those excursions are derivative controls, not a nonlinear completion.

At launch the density and charge preparations, normal field kick and vanishing material velocity are specified, not fitted canonical momenta. Solve the Hamiltonian shell constraint for U=m+Q²/(2r), adjusting both momenta to realize the same velocities. Determine the compact field coefficient c from ΔU(5.5;c,γ)=0, where Δ means event minus quiet at the same γ. Then dc/dγ=−∂γΔU/∂cΔU. Beyond support, the two initial geometries obey the identical exterior ODE with identical mass and charge; the root residual is measured before identifying the two exteriors. The comparison between independent fixed-c derivatives and the continued root is in action-checks.json.

**What the clocks read.** In synchronous source coordinates unperturbed radial light has dτ/dℓ=a, and d ln(νᵣ/νₑ)/dℓ=k along the ray, with positive distance dℓ in either direction. The varying common metric changes both integrands and both arrival times. In addition, expanding the stress square once with a test stress gives δg_probe=γ₁ T+γ₂ Tr(T)g. Apply the saved endpoint/proper-time and null variation to this *total* leading source. The radial background electric stress has e+p=0 and produces no direct radial cone shift, but moves rulers. For a transverse radial electromagnetic perturbation on this radial electric background, the linearized electromagnetic mixed stress has equal-magnitude time–angular and radial–angular entries on the null cone; its square vanishes there. This is the ideal geometric-optics, neutral free-fall readout. The term must not be counted again in an unreduced curvature action. Compose echo legs at the perturbed reflection time.

**An analytic Newton/clock prediction, independently of the transient solver.** In the ordinary exterior only D=Q/r² remains. At fixed conserved Q, e_EM=D²/2−γ₁D⁴/4 and p_r=−e_EM. The trace operator vanishes there. Integrating m'=r²e yields

    f(r)=1−2M/r+Q²/r²−γ₁Q⁴/(10r⁶),  M=U(24)−γ₁Q⁴/(20·24⁵).

Here M is the ADM mass of each preparation, not necessarily unchanged by the interior interaction. On this branch g is the static metric (−f,1/f,r²). For a neutral test clock the time–radial block multiplies by C=1−γ₁Q²/(2r⁴), and the angular block by 1+γ₁Q²/(2r⁴). Thus radial light still uses dr*/dr=1/f but clocks use A=Cf. For a clock released from rest at r₀, E²=A(r₀), v=dr/dτ, and v̇=−A'/(2C²)−C'v²/C. Along it d(t−σr*)/dτ=1/(E+σCv). This gives an independent two-clock readout computed without the evolution grid.

Expressed in the *clock metric's areal radius* S=r[1+γ₁Q²/(4r⁴)], its redshift coefficient at fixed measured M and Q is

    −g_clock,tt(S) = 1−2M/S+Q²/S²
                   + γ₁[−Q²/(2S⁴)+MQ²/(2S⁵)−Q⁴/(10S⁶)] + O(γ²).

Consequently these operators do not shift the leading Newtonian 1/S coefficient independently of the measured mass. The first charge-dependent clock contact in this coefficient falls as 1/S⁴, whereas the geometric metric alone first deviates from Reissner–Nordström as 1/r⁶. For Q=0 both exterior terms disappear; for the trace operator any ordinary exterior response here comes from changed interior ADM mass. This distinguishes an operational prediction from a redefinition of M. It pertains to the specified common-metric, order-reduced subfamily; no universal statement about other parent operators is needed.

**A second prediction: which combination can separate the massive and light fronts?** This is a local short-wavelength characteristic, not a velocity assigned to a finite massive pulse. In the dust-free radial sector the electric Gauss constraint fixes longitudinal displacement. The tensor mixed Hamiltonian is exactly −D²(Π²−s²)/4 and the trace mixed Hamiltonian is zero: the electric field does not split the two radial characteristic speeds at first order. This cancellation does not eliminate electric stress from the gravitational source or clock rate.

In the leading local orthonormal frame the actual scalar characteristic speeds are −H_Πs ± √(H_ΠΠ H_ss). The ideal tensor-coupled radial photon has first variation j−σ(e+p)/2 for direction σ=±1; its trace variation vanishes. Taking the scalar Hessian and subtracting the photon speed gives

    v_scalar,σ − v_light,σ = −σ (γ₁+2γ₂)(Π+σs)²/2 + O(γ²).

Thus γ₁=−2γ₂ is a genuine radial relative-cone null direction even though the individual operators need not vanish and clocks may still move. In the imported 4964 normalization the measured combination would be 16(a_R+a_C/3)(m_h/M_R)². This is not a measured value or a constraint from arrival times. The two characteristic families and their ordinary zero-field control are checked in wave-cone.json. Finite-frequency dispersion from the scalar mass, changing source histories, nonradial propagation and other matter operators are distinct effects.

For scalar and photon fronts emitted together, the common metric, launch rebalancing and clock perturbation cancel at first order in their **difference**. The coefficient of their one-leg difference in flight time obeys dD/dℓ=a_t D+a(Π+σs)²/2, with D(0)=0. The echo composes this D at the actual unperturbed reflection. An independent calculation reproduces the previously saved scalar tensor photon *path-only* transfer, now for a different, derived physical meaning. The dilute calculation evolves the scalar and geometry at the pre-existing reference density before applying this formula.

**A sign test from the material sector.** On an exactly cold, ordinary pressureless continuum with density n in the leading observer frame, both stress squares equal n²/Γ². Put g=γ₁+γ₂. The truncated local canonical Hamiltonian is nΓ−g n²/(4Γ²). At rest H_nn=−g/2, H_ww=n+g n²/2 and H_nw=0. The slow principal squared speed is H_nn H_ww=−g n/2+O(g²). The same result follows from the rest-frame relation e=n−g n²/4, p=n e'−e and c²=dp/de. This is independent of the scalar–photon combination γ₁+2γ₂. In the 4964 variables g=8(a_R+4a_C/3)(m_h/M_R)².

For g>0 ideal cold matter has a negative short-wavelength gradient coefficient. For g<0 it has a positive one at weak coupling; g=0 is the ordinary pressureless degeneracy, not strictly positive sound speed. The sign test concerns real characteristics, not necessarily how much growth fits inside a finite experiment. Gravity and constrained longitudinal electric charge can add finite-frequency Jeans or plasma terms; they do not change that leading local k² coefficient. The separate four-variable principal matrix for (Π,s,n,w) is the Hessian of H premultiplied by the constant off-diagonal canonical pairs (−1 for the scalar pair and +1 for dust). Its sampled eigenvalues, not just the pure-fluid analogy, are retained in mixed-characteristics.json.

One cannot fix this by quietly inserting pressure. For an independently known isentropic rest energy ρ(n), p=nρ'−ρ, the two covariant perfect-fluid invariants are I₁=ρ²+3p² and I₂=(−ρ+3p)². The corresponding first-order rest-frame energy is e_eff=ρ−(γ₁I₁+γ₂I₂)/4. Both e_eff'>0 and n e_eff''/e_eff'≥0 are directly testable material conditions. In microscopic matter a renormalized stress product need not equal the square of a coarse-grained stress; connected stresses and velocity dispersion require matching. Neither a numerical pressure floor nor assuming a sign from the experimental failure accomplishes that matching.

