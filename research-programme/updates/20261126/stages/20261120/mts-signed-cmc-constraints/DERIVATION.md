> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# From a prepared mass flow to a measurable tide on one relativistic slice

This is a conditional initial-data construction in the retained minimally coupled Einstein branch. The archival ground and perturbation histories are unchanged. No new gravity coefficient is chosen. Use signature −+++, Kᵢⱼ=−(Lieₙγ)ᵢⱼ/2, c=1, conformal H=a'/a and comoving Mpc; energies below include 8πGa². Standard ADM and conformal identities are from [Gourgoulhon, 3+1 Formalism](https://arxiv.org/abs/gr-qc/0703035). The real heavy mode, its quadratic action, and the scope of its complex envelope are specified in the parent action note (not bundled here). This does not replace a real scalar with a new fundamental complex field.

## Fix the slice and calibrate its scalar limit

Choose γᵢⱼ=a²u⁴δᵢⱼ, aKⁱⱼ=−Hδⁱⱼ+u⁻⁶Bⁱⱼ, trace B=0. The trace of K is uniform (CMC). Write E=8πGa² Tₙₙ and jᶜᵢ=u⁶8πGa(−Tₙᵢ) for the Eulerian energy and the rescaled covariant momentum density. Flat Cartesian indices on B and jᶜ refer to the conformal reference space. On one slice the **two constraints** reduce to

    div B = jᶜ,             −∆u = u⁵(E−3H²)/4 + B:B/(8u⁷).

Thus the momentum solve supplies a tensor entering the energy constraint; E itself depends on u and its gradient. In this choice of material variables jᶜ can be prescribed without knowing u: a triangular solve is the exact coupling for these data, not an iteration that drops the shear. A homogeneous FRW slice has u=1,B=0,E=3H².

First take the actual 99-mode scalar solution on the retained heavy or cold background. Transform the Newtonian clock by τ_C=τ_N+T. The spatial potential becomes Φ_C=Φ+HT, the normal-frame velocity potential becomes V_C=V_N+T. A tilted slice has aδK_C=3(Φ'+HΨ)+(∆−3S/2)T, S=8πGa²(ρ+p). Using the native constraints checked previously (not bundled here),

    T = 3Q_N/[2k(k²+3S/2)],    Φ_C=−D*/(2k²+3S),   δu=−Φ_C/2.
    Bᵢⱼ=(∂ᵢ∂ⱼ−δᵢⱼ∆/3)T,     Wᵢ=∂ᵢT/2  for B=LW.

Here L is the flat trace-free symmetrized gradient. The scalar density variable d=δ_N−3Φ for a dust background is invariant under this linear change of time coordinate. The saved matter species supply d and V; total density, current and anisotropic stress supply the other species without treating the archive's compensated density as a proper volume density. On a flat unsourced host the momentum and Hamiltonian solves have to reproduce the native geometry throughout the interior, not simply on the prescribed boundary. The native *lapse* is never a boundary value of our elliptic solve. The noncompact incident tide is from the pressure-on or pressure-off full hierarchy, as appropriate. The archived *localized excess* from the earlier nonlinear matter evolution is added to that reference; this is not a new full nonlinear CAMB history.

## What matter has actually been put on the new slice?

Use n for number per reference coordinate volume divided by its homogeneous value, and pᵢ for covariant specific spatial momentum divided by a (pᵢ=∂ᵢV at preparation). For a dust stream with R=8πGa²ρ̄,

    W=sqrt(1+p²/u⁴),  E=R nW/u⁶,  jᶜ=Rn p,  Ŝᵢⱼ=Rn pᵢpⱼ/(u¹⁰W).

Ŝ here is spatial stress in an orthonormal frame including 8πGa²; only its trace-free part is used. For the wave, specify real Cauchy data h=A cos θ, ∇ₙh=m A sin θ, ∂ᵢθ=am pᵢ, m²A²/2=ρ̄ n/u⁶. Average over the fast phase. This **specific normal momentum** amounts to a leading carrier-frequency quadrature with no independent slow normal-amplitude drift. It is a preparation, not a derivation that every evolved real field chooses it. Averaging the canonical Hilbert tensor gives, with gᵢ=∂ᵢ ln n−6∂ᵢ ln u and ε=1/[4(am)²],

    E=Rn/u⁶ + Rn(p²+ε g²)/(2u¹⁰),   jᶜ=Rn p,
    Ŝᵢⱼ^TF=Rn[pᵢpⱼ+ε gᵢgⱼ]^TF/u¹⁰.

The gradient of the conformal factor is part of the proper amplitude gradient, not an optional extra force. This average is a source prescription for gravity on slow scales; we do not solve the Einstein equations for each microscopic phase and commute that solve with the average. Nor is adiabatic wave occupation an exact U(1) charge of the original real scalar. The other species use their linear native CMC Eulerian energy and stress and prescribed rescaled current; their nonlinear host response is not known. An explicit alternative keeps their compensated density fixed and adds −6S_other ln u to their energy. Both prescriptions recover the same native scalar limit; extrapolating the latter logarithm is not a measured nonlinear equation of state.

For the primary data, transplant the archived host excess coordinate number and canonical phase onto this slice. In the **linear-clock alternative** derive an additional CMC shift for the host by solving (−∆+3S/2)T_ex=−3ΣR V_ex/2, with decaying modified-spherical-Bessel exterior and exterior monopole phase zero. Boost the material covectors by ∂T_ex and the spectator current by S_other ∂T_ex; for fixed Eulerian spectators include their 3HS_other T_ex density shift. This retains the required first-order excess clock terms. It does **not** purport to time-translate the entire finite nonlinear movie; a finite-contrast slice change also moves matter across the slice and changes the spatial geometry. Both lifts are explicitly selectable initial data.

## Solve on a finite ball, without setting the tidal field by hand inside it

Spherical variables remain nonlinear. Retain the first variation in the saved axisymmetric quadrupole amplitude λ: n=n₀+λDP₂, V=V₀+λvP₂. Products n₀v' and DV₀' both enter radial current; the tangential current is proportional to n₀v/r. The monopole conformal shear is Bᵣᵣ=b₀=r⁻³∫₀ʳs³jᶜ₀(s)ds. For Bᵣᵣ=bP₂, Bᵣₐ=cDₐP₂, write the angular block as −bP₂Ωₐᵦ/2 + d(DₐDᵦ+3Ωₐᵦ)P₂. The two quadrupole momentum equations are

    b'+(3b−6c)/r=jᶜᵣ,      c'+(3c−b/2−2d)/r=jᶜₜ.

The variational operator for W=(WᵣP₂,Wₜ∇ΩP₂) is half the integral of LW:LV. Its local coefficients are b=4(Wᵣ'−Wᵣ/r)/3+4Wₜ/r, c=Wₜ'+(Wᵣ−Wₜ)/r and d=2Wₜ/r. Smooth origin, W at the outer boundary from the incident native CMC solution. First solve the spherical u₀. Then linearize the full Hamiltonian about u₀, including both the physical energy and the 3b₀b cross term in B:B; solve for u₂. Positive radial stiffness, sixth-order elements, two independent archived grids. Subtract the homogeneous Friedmann source before assembling the stiffness RHS. Integration of the scalar Green kernel and interior pointwise divergence tests are independent readouts of the weak solves.

Primary outer radius 120 Mpc. Monopole excess uses u₀−1 decaying as 1/r at the boundary; quadrupole excess uses u₂ decaying as 1/r³ *relative to the native incident field*. These Robin conditions describe one exterior prescription, not a theorem about the complete cosmological exterior. Also solve with zero excess Dirichlet data on the same wall and with a 96-Mpc matching radius. Independently add a globally smooth compact TT shear at quadrupole order: b=A f(r), c=(rb'+3b)/6, d=(rc'+3c−b/2)/2. Here f=1 within 12 Mpc and tapers with four vanishing endpoint derivatives to zero by 36 Mpc. Both divergences vanish. A=2Σwₖ k²Tₖ/15 is the original *heavy* native axial CMC shear at the origin; the same ±A is used for both seeds, cosmologies and pressure switches. It tests allowed free gravitational data, not a measured tensor wave or a prior on one.

## Read the geometry, using the same ruler

Let Gᵢⱼ=a²[³Rᵢⱼ+KKᵢⱼ−KᵢₖKᵏⱼ] in the physical orthonormal triad. The Gauss and Einstein equations give

    a²(−Rᵢₙⱼₙ)^TF=−Gᵢⱼ^TF+Ŝᵢⱼ^TF,   a²(−Cᵢₙⱼₙ)=−Gᵢⱼ^TF+Ŝᵢⱼ^TF/2.
    G^TF=[−2u⁻⁵ Hess u + 6u⁻⁶ ∇u∇u − H u⁻⁶B − u⁻¹² B²]^TF.

No imposed present-time lapse or boundary value for the desired force is needed. Axial rr and meridional rθ have separate signed readouts. The principal radial second derivative uses the solved Hamiltonian; differentiating the element polynomial independently records where numerical cancellation matters. Compare the *physical* normal-observer tide, not ∂ᵣΦ/r. In the scalar homogeneous limit the two positive-acceleration conventions must give −HessᵀᶠΨ and −Hessᵀᶠ[(Φ+Ψ)/2].

Coordinate radii need not correspond to the same distance when there is a host. The symmetry axis is a spatial geodesic. Fix a proper axial length a·r_lab from the origin. Its spherical endpoint r₀ satisfies ∫₀ʳ⁰u₀²ds=r_lab. At first order r shifts by δr=−2∫₀ʳ⁰u₀u₂ds/u₀²(r₀); the local measured quadrupole becomes T₂(r₀)+δr T₀'(r₀). This term is measurable in the numerical budget. It fixes the spatial ruler, not an unobserved galaxy formation state or a unique cosmological clock. Divide all tabulated tides by a² and multiply by (c/Mpc)² for s⁻².

## A cancellation with a stated domain

For *identical spherical data, lift and boundary operator*, the first-variation constraint and tide are linear in the quadrupolar matter inputs, boundary data and free TT perturbation. Subtract the on/off branches: an identical freely added TT field cancels, including the perturbation that it induces in the Hamiltonian and in the proper ruler. This also follows by directly evolving no background difference: put the archived third channel of excess D and V, and the native on-minus-off quantities, through a single solve. This is a conditional first-order identity; it does not remove free data that differ between the branches, and matter stress prescriptions that change the spherical operator cannot be subtracted this way. The run separates (a) density/phase response at identical wave lift, (b) changing the final matter stress lift, and (c) removing the unperturbed incident response to isolate the additional effect of the host. A cold switch must give identically zero on every control. No global error bound or uniqueness of all possible CMC data follows.
