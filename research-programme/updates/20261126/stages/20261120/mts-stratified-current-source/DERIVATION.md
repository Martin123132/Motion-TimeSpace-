# The source of gravity from opposing currents on a nonuniform host

**Domain.** Work inside the retained weak-field nonrelativistic branch, before stream crossing, with smooth positive background densities n_s(r) (in units of the corresponding homogeneous densities), radial velocities U_s, fixed coefficients C_s and a common metric potential. Length and conformal time η are comoving Mpc (c=1); m is inverse Mpc. We test a linear velocity perturbation W_s(r)P₂(cosθ) initially, with no initial change in any density, gravitational potential or exterior tide. The heavy wave and its pressure-disabled *perturbation* control have exactly the same spherical foreground. The separate cold preparation has CDM and baryons and no wave stress at all. Standard scalar wave pressure is imported dynamics, not a new MTS coupling; see e.g. [Hui et al.](https://arxiv.org/abs/1610.08297). The results below are derived consequences for these specific preparations and their compact generalization.

## Ordinary streaming first, wave dispersion separately

Let S=Σ C_s d_s be the quadrupolar Eulerian density source and 2a L₂Φ=S, where L₂f=f″+2f′/r−6f/r² (spatial primes here only). Set M_T=∫r² T S dr, omitting the same angular factor on both sides. The reported smooth aperture moments divide this by ∫r²T dr. Projection on a compact T inside the box also gives M_T/(2a)=∫r²[T_r g_r−6TΦ/r²]dr for g_r=−∂rΦ. This reads the **radial and angular gravitational force** via integration by parts; neither is individually equal to a local force measurement. All time derivatives below are conformal.

Initially δJ_r=Σ C_s n_s W_s,r and δJ_angular=Σ C_s n_s W_s/r (coefficient of ∇ΩP₂). With overdots denoting conformal-time derivatives:

    Ṁ_T = Σ C_s∫ r² n_s(T_r W_s,r+6T W_s/r²) dr,
    M̈_T+ℋ Ṁ_T = Σ C_s∫ r² n_s U_s[2 T_rr W_s,r +12(T_r/r−T/r²)W_s/r] dr.

The second line follows from ∂ηδJ+ℋδJ=−div δΠ initially, δΠ=Σ C_s n_s(U_s⊗δu_s+δu_s⊗U_s). Both changed gravity and changed density pressure are zero at this instant, not set to zero for the subsequent evolution. Integrating div div δΠ against T gives the radial and mixed angular Hessian terms above. In a weakly balanced preparation Ṁ_T is tiny, but the stress on the right need not be: different spherical streams weight the same opposite currents differently. In particular, absence of a net initial current source does not imply absence of an ordinary gravitational response at the next order.

For the heavy species define K_n f=L₂ f+(∂r ln n) ∂r f. Let Δ denote enabling wave pressure only in the perturbation versus disabling it on the **same** evolving spherical background. At launch ḋ_h=−n K_n W. Linearized wave enthalpy is Q[d]=(4a²m²)⁻¹ K_n(d/n). The first additional quadrupolar velocity-potential acceleration is Δẅ_h=Q[ḋ_h], so ΔS, ΔṠ and ΔS̈ are zero, while

    ΔM⃛_T = − C_h/(4a_i²m²) ∫ r² n [(K_n T)_r(K_n W)_r + 6(K_n T)(K_n W)/r²] dr.

Three integrations/operators are involved, not a fitted exponent. Compact support or vanishing surface terms are needed. The result is independent of the compensator's chosen initial velocity and of the radial background flow at this order; it is not independent of the density profile. For homogeneous n it recovers Fourier scaling −C_h n k⁶ W/(4a²m²) for the density, hence +C_h n k⁴ W/(8a³m²) for the potential. A useful launch scale is η_*≈3|M̈_T/ΔM⃛_T| when Ṁ_T is negligible; even exact derivatives do not make this finite-time crossing formula exact.

## What can be invisible?

For any smooth compact real quadrupolar W supported inside R_* with n>0, use T=W. Then −ΔM⃛_W is positive unless W=0. In the n-weighted norm, writing the positive operator A=−K_n, its value is C_h/(4a_i²m²) times ⟨AW,A(AW)⟩_n. Both W and AW are compact/regular. The angular term gives ⟨f,Af⟩_n≥(6/R_*²)‖f‖²_n; Cauchy–Schwarz first gives ‖AW‖_n≥(6/R_*²)‖W‖_n. Therefore

    −ΔM⃛_W ≥ C_h (6/R_*²)³ ‖W‖²_n/(4a_i²m²).

This rules out a nonzero compact l=2 phase whose wave correction is invisible to **every interior probe** at cubic order. It does not make every individual probe respond and does not rule out cancellation of the *total* field with other inputs. The bound is on a weighted overlap with the source, not a model-independent lower bound on a distant acceleration. The possible presence of nodes (n=0), a different boundary, strong gravity, relativistic stresses or a noncompact state requires a new argument.

Outside a compact density perturbation the Newtonian quadrupole potential is Φ₂(r)=−Q₂/(10a r³), Q₂=∫r⁴ S dr. At launch the above bilinear form also applies to T=r² when W and its relevant derivatives are compact. Here K_n(r²)=2r ∂r ln n. **A homogeneous host has no exterior wave-only quadrupole at cubic order for any such W**, despite its nonzero interior response. In a stratified host the exterior coefficient is just one signed linear functional of W. On the three chosen compact probes we computed its maximizing direction in the fixed weighted norm and an independent direction in its kernel; no force data enter. Preserving the same mass occupation does not select either one. For the dipole-free axisymmetric quadrupole, g_r=−3Q₂P₂/(10ar⁴) and g_θ=Q₂(dP₂/dθ)/(10ar⁴) outside. This is the isolated *difference* between two solutions with the same imposed exterior; it is not a vacuum cosmology or an isolated real Milky Way.

## Does the exterior cancellation persist?

In operator notation for the heavy perturbation, write ḋ=A d+B w and ẇ=D w+E[d_all]+Q d. Here A advects density in the spherical flow, B=−div(n∇), D=−ℋ−U∂r, E is common gravity, and Q is the varied dispersive enthalpy. Let h=B W, j=A h+ḂW+B D W. Then h=ḋ_h and j=d̈_h initially. Differentiating the two evolutions on the identical moving background gives

    Δd⃛_h = B Q h,
    Δd⁽⁴⁾_h = A BQh + 3 Ḃ Qh + B[D Qh + 2 Q̇h + Qj].

No changed common potential or other-species response enters this expression before this order: all Δd_s and their first two derivatives start at zero. They are included during the actual evolution. A common potential formed from ΔS/(2a) has fourth source derivative proportional to ΔS⁽⁴⁾−4ℋ ΔS⃛ at launch. In the homogeneous case ΔS⁽⁴⁾=−6ℋ ΔS⃛ as in the predecessor. In a stratified host ṅ and U enter separately. A cubic zero of the exterior functional need not be a quartic zero. The prediction uses the initial spherical equation (including the retained reference lift) for ṅ, not a derivative taken from the later force data.
