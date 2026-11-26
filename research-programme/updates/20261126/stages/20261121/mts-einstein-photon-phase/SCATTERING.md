> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# The Einstein pole and a finite polarization comparison

Work in the weak flat vacuum of the retained calibrated metric (not bundled here) and use the matched massive electron trace (not bundled here). Both the Einstein control and the MTS calculation contain the **same** minimally coupled neutral scalar of mass m, ordinary electron, calibrated Newton constant and asymptotic states. We compute the elastic photon–scalar intermediate state at first absorptive order, to first order in the separately transverse electron spin-zero amplitude. Real higher-derivative amplitudes, other loop/tensor channels and unresolved radiation are not set to zero in a physical likelihood. The Born tensor and its low-energy light-bending limit have a standard GR counterpart ([Bjerrum-Bohr et al.](https://arxiv.org/abs/1609.07477)); the subtraction and readout below use the retained normalization.

## From the shared metric to its angular eigenvalues

Use v for the CM energy squared, ρ=1−m²/v, D=(v−m²)²/v=4p², r=(1−cosθ)/2, t=−Dr, and G₀=v/M_R². M_R⁻²=8πG. The photon stress is traceless and both sources are conserved. In the previous all-incoming phase convention the Einstein numerator is −2 times the contraction p₃ T_EM p₄, divided by M_R²t; the contact amplitude is +λ times the same contraction. For photon helicity preserved the contraction is vD(1−r)/2; for flipped helicity it is zero. Thus

    P_E = G₀(1−r)/r,      P_contact/P_E = −λ M_R² t/2 = ζr,
    ζ = λ M_R² D/2,       P/G₀ = p(r) = (1−r)(1/r + ζ).

The unpolarized minimal low-energy differential cross section tends to G²m² cot⁴(θ/2) for a heavy target, i.e. 16G²m²/θ⁴ in the forward limit, consistent with the small-angle deflection 4Gm/b. Spin here refers to photon polarization, not an internal electric charge on the scalar. [Covariant controls](evidence-001.zip) (archive member: `controls.py`) check the helicities, both stress Ward identities, the Maxwell trace and photon gauge representatives before any angular projection.

Use M=16πΣ(2J+1)t_J d^J, with d^J₊₊=(1−r)P^(0,2)_{J−1}(1−2r) and d^J₋₊=r P^(2,0)_{J−1}(1−2r). The divergence is the same in every diagonal wave. For a common angular regulator, t^P_J=G₀/(16π) times

    L_reg + h_J + (ζ/3)δ_J1,      h_J=−H_(J−1)−H_(J+1), J≥1.

For example h₁=−3/2, h₂=−17/6. To derive this, integrate r^(a−1)(1−r)²P^(0,2)_n(1−2r) from zero to one. Jacobi's derivative formula and n integrations by parts give (1−a)_n B(a,n+3)/n!, by continuation from Re(a)>n. The pole is 1/a and the displayed h_J is the constant. Cutting r<ε, or replacing 1/r by 1/(r+ε), has L=ln(1/ε) to the accuracy of the limit. A finite change in that convention shifts every h_J by the same constant if L is redefined. Neither an isolated finite h₁ nor a raw absorptive wave is an absolute measurement. This is a forward-exchange phase, not a new graviton mass; see [Weinberg's IR analysis](https://journals.aps.org/pr/abstract/10.1103/PhysRev.140.B516).

## Keep both helicities of the same outgoing photon

Let F be the tree flip due to the massive electron **trace** exchange. In units a_e D², with signed a_e and f=F₁(t)/F₁(0) as matched previously, write

    f_B(r)=−r(2m²/D−r)f(−Dr)/2=Σ B_J d^J₋₊.

At leading heavy-electron order f=1, B₁=−(2m²/D−3/4)/2 and B₂=−1/8; there are no higher waves at this order. The exact finite spacelike form determines the higher B_J by orthogonality. No direct charge curvature is used. Prepare incident + helicity; analyse the two outgoing helicities with axes tied to the scattering plane. Define the signed phase-sensitive Stokes combination S=2 Im(P*F)/(|P|²+|F|²) in that basis. It is accessible in principle by comparing orthogonal linear-analyser orientations after preparing circular polarization. Unlike an angle-to-angle ratio of complex amplitudes it cannot change if the entire final state at *one angle* is rephased.

The normalized absorptive flip from t t† is 2L f_B + j, with
j=2Σ h_J B_J d^J₋₊ + 2ζ B₁r/3. Both time orderings enter. The diagonal elastic iteration must be included too: its normalized result is 2L p + k. Here

    k=p₀ h_E(r)+(1−r)(2ζh₁+ζ²/3),          p₀=(1−r)/r,
    h_E(r)=r/(1−r) + [1+1/(1−r)²] ln r.

A derivation of the nontrivial diagonal convolution: choose incident spinor (1,0), final spinor (c,s)=(√(1−r),√r), intermediate spinor (√(1−u),exp(iφ)√u). For E×E the numerator is N=[c(1−u)+s√(u(1−u))exp(iφ)]². The denominators are the angular distances u and w from the two directions. Subtract c² from N, since it is the residue at both poles; the remainder is absolutely integrable. Azimuthal averaging of N/w gives c²/|u−r| at u<r and (1−u)²/[c²|u−r|] at u>r. The subtracted remainder with the other 1/u has integral [1−r+(2−r)ln r]/(1−r). For the omitted scalar integral, Feynman combination of the two screened poles gives ∫₀¹ dx/[ε(1+ε)+r x(1−x)] = (2/r) ln(r/ε)+o(1). Reinstating c² yields 2L p₀+p₀ h_E. The mixed and double-contact diagonal convolutions follow by J=1 orthogonality. Dropping this diagonal iteration would leave a spurious forward infinity in the polarization.

Inserting both absorptive parts, the common phase cancels **at the same finite angle**:

    S_elastic,trace = [ρ a_e D²/(8π)] [j − f_B k/p]/p .

This retains terms linear in a_e; take the ζ derivative at zero for a consistently linear stress-contact excess. Keeping ζ exactly gives the elastic iteration of the *two specified trees*, not an all-orders EFT. The formula is for 0<r<1, away from zeros of p. At the leading trace Born null r*=2m²/D between zero and one, the dimensionless GR bracket divided by p is r*²(3−4r*)/[3(1−r*)]; no division by F occurs. At m→0 it becomes r²[2/r−17/3−h_E(r)]/(2p₀). At r=1/2 it is +0.09988365; there is an interior zero at r≈0.583997 for this projected channel. These are signs relative to a_e and the specified analyser, not zero or negative total cross sections.

**Independent check.** Directly sew both two-helicity trees on the sphere, rotating the polarization basis at the intermediate direction. Integrate the two hemispherical Voronoi regions about the separated poles, including the azimuthal phases. Repeat with a sharp removed cone and a smooth screened denominator down to ε=10⁻¹⁰. The calculation never inserts h_J, h_E or their Wigner sum into that sphere integrand. Results (not bundled here) cover a finite-mass vertex zero, GR, nonzero stress contact and a synthetic D/m_e²=0.5 resolving the electron shape. An explicit finite common-phase change cancels as well. The stored 1 meV rows use the leading heavy electron; evaluating the exact trace at those angles changes the normalized answer by less than 6×10⁻¹³ in the numerical comparison. This is removal of the forward regulator in a specified elastic interference term, not an all-channel inclusive calculation or a claim that the electron trace dominates measured polarization.

## A simpler rate test does not need the tiny electron phase

At fixed v the preserved Born helicity has dσ/dr=v p₀²(1+ζr)²/(16πM_R⁴). For bins A=[1/4,1/2], B=[1/2,3/4], take (N_B/N_A)/(N_B/N_A)_Einstein for the same incoming state and controlled angular efficiencies. Common flux cancels; the rate scale does not become larger. The first log derivative is 2(〈r〉_B−〈r〉_A)=0.502998 per ζ with weight p₀². At 1 meV the old strict-EFT one-percent corridor allows |ζ| up to 0.00069444 |Zψ/K₀|. For kinetic ratio one the illustrative edges give 0.999651 and 1.000349, not a measured interval. The Einstein bin cross sections are only 1.90×10⁻¹³¹ and 2.33×10⁻¹³² m². The incoming scalar flux/occupation is not calibrated here. The ratio isolates the displayed tree contribution, not all new matter or higher operators. A GR EFT with the same λ has the identical contact response. [Physical scales](evidence-001.zip) (archive member: `summary.json`).
