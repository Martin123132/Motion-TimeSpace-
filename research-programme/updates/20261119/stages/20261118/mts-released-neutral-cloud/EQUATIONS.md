# From a source and emitted field to the displacement of neutral probes

## Experiment and order counting
Use the retained local classical common metric and minimally coupled matter, scalar and Maxwell sectors. Let ε multiply the existing material counterrotation. Time τ is each freely falling centre's proper time. We calculate the coefficient of ε² in the sky-averaged log volume relative to the unspun preparation, and the coefficient of ε in a signed directional arm signal. This fixes what is held equal when two experiments have different clocks. To this order the fractional-volume and log-volume corrections coincide because there is no first-order trace. Release is from rest, with the connecting vectors initially orthonormal and initially covariantly stationary; no independent even-parity wave was seeded. It is inappropriate to equate these conditions with holding a detector at a prescribed radius. Physical length/time scales follow the parent nondimensionalization; no astrophysical spin amplitude is fitted.

Write f=1−2m/r, F=α/√f, B=Ff, and W²=1+fp² for canonical radial momentum p. Along a zero-axial-momentum centre the horizontal geodesic equations are

    t'=W/(F√f),   r'=fp,   p'=−W² F_r/F−(1+2fp²)f_r/(2f).

A prime here and below is d/dτ except for explicitly radial subscripts. Differentiate all three with respect to ε² with zero perturbation to initial coordinates and momentum. The perturbation of any field at common τ includes its Eulerian change plus δt·∂t+δr·∂r. The mass/lapse come from the earlier conserved-energy solution, including loss from the source. For the matched-mass, nonemitting ordinary control only, remove the wave and retain the initial ADM increment.

## Physical tidal matrix
For spherical scalar h and Π=h_t/B outside material, U h=W√f Π+fp h_r. The radial section and the Ricci trace in the absence of spin are
    E_R=−2m/r³+2Q²/r⁴+f(Π²−h_r²),    R_UU=2(U h)²−h²+Q²/r⁴,
    E_T=(R_UU−E_R)/2.
Compute their total ε² variation, including the varied clock, radius and boost. The additional explicit mean photon contributions, for n=2/3, P=A_t/B and X=A_r, are
    δE_R|photon=4n A²/r⁴,
    δR_UU|photon=n[f{(WP+√f p X)²+(WX+√f p P)²}/r²+2A²/r⁴].
These are physical stresses; do not add the axial effective stress a second time. The mean takes the products of the axial l=1 fields *before* projection. An independent second-order axisymmetric l=2 term is linear at this order and integrates to zero on an unperturbed sphere; it does not vanish for a particular viewing angle.

Let S be the outward spatial radial direction, eφ the normalized azimuthal Killing field, and λ=r sinθ. Metric compatibility, the Killing equation and dK♭(U,S)=λ²C/F give ∇_U eφ=Ω S, ∇_U S=−Ω eφ at first order, where Ω=ε sinθ·o and o=rC/(2F)=2(QA−I)/r³. The constraint is the same one used for the electromagnetic source, not a force fit. Here I is the material integral of the signed specific angular momentum; it vanishes in the exterior of the balanced source, not for a general Kerr body. The Killing Jacobi field λeφ has radial second derivative proportional to 2r'o+r o', so the radial-frame E_Rφ/(ε sinθ)=−o'−2r'o/r ≡ u. For the parallel frame integrate γ'=o, γ(0)=0. Its off-diagonal section per ε sinθ is k=u+γ(E_T−E_R). The mean radial second-order diagonal acquires c=n[2γu+γ²(E_T−E_R)], the transverse sum loses c. This is why evaluating only the trace of the metric perturbation gives the wrong volume in a spinning vacuum.

## Two independent propagations
In the parallel frame J''=−EJ, J(0)=1, J'(0)=0. If j_R,j_T are the spherical stretches, x,y the Rφ,φR entries per ε sinθ, and d_R,d_A the mean quadratic radial and summed transverse entries, then
    x''=−E_R x−k j_T,   y''=−E_T y−k j_R,
    d_R''=−E_R d_R−(δE_R+c)j_R−nk y,
    d_A''=−E_T d_A−(δR_UU−δE_R−c)j_T−nk x,
    δlog V=d_R/j_R+d_A/j_T−n xy/(j_R j_T).
The quadratic determinant term cannot be removed by choosing different axes.

Independently, use the vorticity-free optical equation (the trace is [Raychaudhuri’s equation](https://journals.aps.org/pr/abstract/10.1103/PhysRev.98.1123)). With b_R=j_R'/j_R and b_T=j_T'/j_T and s the shear divided by ε sinθ, in the rotating radial basis it gives
    (s−o)' +(b_R+b_T)(s−o)=2(r'/r−b_T)o,
    δb_R'+2b_R δb_R=−δE_R−n(s²+2os),
    δΘ'+2b_T δΘ=−δR_UU−2(b_R−b_T)δb_R−2n s²,     δlog V=∫δΘ dτ.
The two methods use the same source but different evolution equations, frames and integrators. The parallel matrix passes in a stationary spinning reference with o(0)≠0 only if the launch shear is set to zero, not to the local frame rotation.

## Source readout, limits, independent checks
For spherical radial release the orbital Killing vector enforces j_T=r/r₀ exactly. Hence s=o−o(0)/(j_R j_T). The initially untwisted exterior obeys s=o: in the physical optical equations the square and radial cross terms precisely cancel the explicit horizontal-versus-4D curvature difference. This justifies a third *volume* test from varying the launch radius in the horizontal metric, while the observable signed shear is nonzero. See QUOTIENT-FORECAST.md, KILLING-READOUT.md and DIAGONAL-ARM-PREDICTION.md for the resulting measurements; see EXACT-CLOUD-FORECAST.md for the different normal-release test in the full [Newman et al. metric](https://doi.org/10.1063/1.1704351).

Before signal arrival, initial symmetry makes the quadratic-spin volume correction start at τ⁴. Let h₂=(spatial Laplacian)h−h at launch, with δh₂=δf h_rr+(2δf/r+δf_r/2)h_r. Then δr''=−δm/r²−rδf h_r²/2, and the coefficient is
    −[(8h₂−2h)δh₂−4Q²δr''/r⁵+4(E_R−E_T)δE_R]/24.
In the spherical neutral vacuum control the radial Jacobi sections are −2M/r³ and +M/r³. Radial free fall parametrized by proper time obeys r''=−M/r², so the prepared cloud has the same radial and transverse stretches as the Newtonian inverse-square solution down to its first caustic. EARLY-PREDICTION.md gives the closed form, evaluated independently at 42 digits. This is a derived observable within a retained GR sector, not a derivation of G, a claim about all geodesics or a bound on every MTS sector.

