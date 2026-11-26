> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# Initial data in the retained Einstein limit: what is solved, and what is not assumed

## Geometry

Use the sign convention Kᵢⱼ = −(1/2)ℒ_n γᵢⱼ, zero shift, γᵢⱼ = a² b⁴ δᵢⱼ, N=exp(U), V=−2 ln b and Kⁱⱼ=−h δⁱⱼ. These are shear-free normals on the chosen spherical chart; this is not a coordinate-independent identification of all possible spherical solutions. The FLRW background has h=H. Energy E, ADM current jᵢ=−T(n,∂ᵢ), and principal pressures are normal-observer projections. Use c=1, comoving Mpc, and the retained G. The starting Hamiltonian, momentum and spatial evolution equations are the standard [Einstein 3+1 equations](https://arxiv.org/abs/gr-qc/0703035), not a new derivation of Einstein's action. No lapse follows from the two constraints alone.

The observed sign of the momentum term matters. The Hamiltonian and radial momentum constraints reduce to

    (r² b')' = a² r² b⁵ [ 3(h²−H²)/4 − (8πG)(E−E_bg)/4 ],
    h' = 4πG j_r,       8πG E_bg = 3 H².

A prime denotes a comoving radial derivative. This follows from R^(3)=−8∇²b/(a²b⁵) and Dⱼ(Kʲᵢ−δʲᵢK)=2∂ᵢh. In particular constant mean curvature would require j_r=0. Set h(L)=H from the saved expansion table and regular mass flux r²b'→0 for the explicitly regularised core. Compare b(L)=1 in two boxes and the exterior harmonic monopole alternative b(L)−1=−L b'(L). The latter is an outer matching *trial*, not an assertion that the whole cosmological exterior is vacuum. The untracked homogeneous energy is 3H²/(8πG) minus the homogeneous energy assigned to the stored species. It carries no imposed local current or anisotropy here; an arbitrary dynamical continuation or equation of state for it is not inferred.

Independently impose the condition that the anisotropic part of Kᵢⱼ remain zero. With Π=P_r−P_t this gives a linear ODE for the lapse itself:

    N'' + (2V'−1/r)N' = N [V''−V'/r+V'²−8πG a² b⁴ Π].

We solve for N−1 and N'/r, inserting V'' from the spatial constraint rather than differencing a noisy potential. The primary match is U(L)=V(L), U'(L)=V'(L). We also vary the relative slope explicitly. As a conditioning and sign check, independently integrate the flux of F=exp(U−V), without forming a difference of nearby potentials; the exact nonlinear identity and the previous leading, frozen prediction are in the preceding derivation (not bundled here). Directly sample V−U at the three radii and form the contrast. No previous predicted value enters the solver.

There is an independent physical mass test. Define areal radius R=a b²r and Γ=1+2r b'/b. Then nR=hR. The geometrical excess Misner–Sharp mass, subtracting homogeneous mass at the *same areal radius*, is

    G δM = R [(h²−H²)R²−(Γ²−1)]/2.
    (G δM)' = 4πG R² [(E−E_bg)R' + j_r hR].

The latter follows by differentiating the former and using both constraints; it can also be interpreted as the radial energy balance of the sphere. An oriented energy flux matters even for an integral over a single slice. We integrate the material side independently and compare it to the geometrical mass, also relative to the much smaller current term. This is an internal consistency test, not a measurement of the mass.

## Actual stress, independent of the fitted force bands

For species s take the positive saved shell measure dM_s, normalized so homogeneous matter has dM_s=r²dr. Store its initial canonical radial momentum p with sign reversed on negative oriented X. At a given radius multiple distinct streams may be present. Write D₀=ρ̄_s dM_s/(r²dr); the conserved rest mass per normal spatial volume is D=D₀ b⁻⁶. The physical orthonormal momentum per unit rest mass is v_*=p/(a b²), γ=sqrt(1+v_*²), and the physical speed is v_*/γ, not v_*:

    E=D γ,       j_r=D p,      Π=D v_*²/γ  (radial streams).

We sum streams before solving the metric but never replace them with one mean speed. The code splits each oriented label element at its radial endpoints and uses its exact q² weight and affine X(q),p(q) for evaluation. For the sources it keeps dust coordinates and canonical momenta from the saved state fixed under metric iteration; keeping proper density fixed as well would count the volume variation incorrectly.

For the retained minimally coupled oscillating real scalar, parameterize two quadratures as field sqrt(2ρ̄)/m Re(z exp(−iθ)) and normal derivative sqrt(2ρ̄) Re(−i w exp(−iθ)). Fast-phase averaging the actual Hilbert stress gives

    E/ρ̄=(|w|²+|z|²+|∂r z|²/(m²a²b⁴))/2,
    j_r/ρ̄=Im(w*∂r z)/m,       Π/ρ̄=|∂r z|²/(m²a²b⁴).

Primary lift z=w=b⁻³ ψ; alternative z=ψ, w=b⁻⁶ ψ. Both preserve the saved densitized phase occupation b⁶Re(z*w)=|ψ|² and give the same densitized radial current. They differ in gradient stress and beyond-leading energy. They are phase-averaged Cauchy-data prescriptions, not a proof of unique relativistic positive-frequency preparation or of exact real-field evolution. The previous theory's nonrelativistic mass and norm are unchanged. There is no electromagnetic field in these formation data. Charged exterior controls separately test the sign and relative normalization of the Maxwell stress.

## Why the raw dust cannot simply be declared regular

A material element that actually crosses X=0 with nonvanishing dM/dq and X' produces two contributions to dM/dr as r→0. Its coefficient is 2(dM/dq)/|X'| at the crossing, strictly positive. Thus the radial normal-frame dust density of the unmodified folded field diverges at least as 1/r² for a finite, regular spatial metric. A regular center with bounded curvature and bounded h cannot solve the Hamiltonian constraint for these positive masses. This is a limitation of the cold, exactly radial stream preparation after crossing, not a universal singularity theorem for MTS.

For the numerical core controls only, redistribute *exactly the same* signed stream momenta and rest masses found inside r_c over the core's coordinate volume. Mix a radial population of fraction (r/r_c)² with a population of isotropically oriented momenta of the same magnitude for the remaining fraction. This retains energy for a given conformal factor, makes the center regular, and allows net radial momentum and anisotropy away from it. The core prescription is **not derived** and is not the source of the frozen exterior prediction. Compare r_c=1.5625, 3.125, 6.25 and 12.5 comoving kpc. There is no claim that taking r_c→0 yields a smooth limit. The coherent radial wave has different regularity: the sine variable u=rψ obeys u(0)=0, so its physically represented smooth limit is ψ(0)=u'(0), not an additional independent data item.

## Independent dynamical check

Kᵢⱼ=−hγᵢⱼ also implies ∂ηV=a[H−exp(U)h] on fixed comoving worldlines, where dη=dt/a. This relation is *not* used to obtain time sequences of V: we first record its prediction at a saved epoch, then propagate the original matter and wave to adjacent epochs and solve the constraints again. Compare potential contrasts (not arbitrary central potential offsets) and normalize the time-derivative difference to the largest of the predicted/measured rate and the Hubble-times-span term. Separate numerical/reconstruction errors seen in Newtonian V from corrections in the relativistic lift. A correct instantaneous constraint solution need not be a spacetime solution if its reconstructed time derivative fails this test.

