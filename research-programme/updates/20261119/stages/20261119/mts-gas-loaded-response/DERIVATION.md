# Gas gravity, wave response, and the common-metric interaction

## Newton source and the thin-disk split

For each component in [McMillan, Eq. 4 & Table 1](https://arxiv.org/pdf/1608.00971), the surface law is S(R)=S0 exp(−Rm/R−R/Rd) and rho=S(R) sech²(z/2h)/(4h). Its total mass is 4π S0 Rd Rm K₂(2√(Rm/Rd)), by integrating 2πR S dR. Parameters, helium convention and source URL come from the sealed predecessor. Neutral-associated gas beyond R=30 kpc alone has 1.068 billion solar masses; imposing the stellar truncation on the gas is not justified.

To avoid resolving a very thin positive disk solely with angular harmonics, define H(z)=h log cosh(z/2h), H′=tanh(z/2h)/2, H″=p(z). With r the spherical radius, split Φ=4πG S(r)H(z)+Φ_res. The exact Poisson source for the residual field divided by 4πG is

    [S(R)−S(r)]p(z) − [S″(r)+2S′(r)/r]H(z) − 2 S′(r)(z/r)H′(z).

The auxiliary potential decays at infinity; no plane-sheet or halo mass is added. Expand the signed residual in even Legendre multipoles, integrate inner and exterior moments, and restore the auxiliary field with its analytic derivatives. Use only potential and radial work from this expansion in the Hamiltonian; independent singularity-resolved elliptic 3D ring integrations supply direct observational forces. The ring program includes physically signed radial forces; it makes no spherical mass shortcut. Verify exterior behavior, monopole, annulus volume vs flux, the saved three gas forces and three numerical source grids. The small disagreement in the initial outer radial control at R=40 was resolved by one extra ring order, not a wider tolerance. All force component truncation errors are retained separately.

## On-shell response and source reciprocity

In the retained stationary Schrödinger–Poisson reduction, let u be the real coefficients, N=⟨u,u⟩, B the constrained linearization of the stationary equation, and b_j the projected drive Φ_j u from one gas source. For t_j infinitesimal, δu_j=−B_perp⁻¹ P b_j at fixed N. The induced Newton source is 2u δu_j in physical density units. On the branch also calibrated to R_a g_in,a=V_a², add ∂u/∂lnN times

    d ln N/dt_j = −(g_gas,j + δg_wave,j)_in,a / (∂g_wave/∂lnN)_in,a.

An NFW amplitude receives its corresponding one-constraint shift without an intrinsic shape response. The finite calculations solve the nonlinear equation, not this first derivative. In output, direct-only holds the original wave fixed, fixed holds its occupation but re-solves the wave, and matched re-solves both the wave and its normalization. The two original stars-only calibrated preparations are the controls; changing a stellar density normalization is not equivalent to changing gas.

At fixed N the envelope derivative of the *full* stationary energy with respect to t_j is ∫rho_w Φ_j dV. At variable N add μ dN/dt_j in consistent units. For the two gas components the fixed-occupation curvature matrix in the code's real-field normalization is 2⟨b_i,δu_j⟩ (converted to physical energy per original wave mass). Its symmetry follows from the self-adjoint constrained linearization, and it is negative semidefinite if B_perp is positive on the driven subspace. We evaluate the full symmetric 2×2 matrix; negative eigenvalues in this subspace are not a general stability theorem. Total-gas derivatives also have independent small nonlinear perturbation checks. The original wave mode rearranges in response to the gas on this branch; no independent gravitational charge is fitted.

## Independent common-source energy and stress checks

Write Φ_w and Φ_g for physical Newton potentials with the same G. Integrating by parts with their decaying exterior fields gives U_wg=∫rho_w Φ_g dV=∫rho_g Φ_w dV. There is no additional half factor in the cross term: each self-energy contributes a half, while the two equal cross contributions give one. We integrate the first in spherical coordinates using the saved wave coefficients, and the second in cylindrical coordinates through the gas with newly reconstructed wave multipoles, neither using a force fit.

The cross stress from the two Newton potentials is

    t_ij = (Φ_w,i Φ_g,j + Φ_g,i Φ_w,j − δ_ij ∇Φ_w·∇Φ_g)/(4πG).

Its divergence equals rho_g ∂iΦ_w + rho_w ∂iΦ_g, the negative of the total mutual force density. A whole-space force test would vanish trivially by symmetry. Instead integrate over z>0. The vertical gradients vanish on the midplane, so its downward mutual weight equals

    ∫_(z>0) (rho_w ∂zΦ_g + rho_g ∂zΦ_w) dV
      = (1/2G) ∫_0^∞ R ∂RΦ_w(R,0) ∂RΦ_g(R,0) dR.

We compute all three terms independently, retaining the exterior multipole traction tail to infinity. The wave mass density is fixed by its already-used Poisson field: v_unit² |wave|²/(4πG L²). In the retained physical units the old solar-mass label uses G_SI × 1.98847×10³⁰ kg, while the external Galactic field constant corresponds to the nominal solar GM=1.3271244×10²⁰ m³/s². The inversion independently identifies their 1.000030239893 conversion. Apply it once when comparing absolute wave masses or absolute energies in one solar convention. Dimensionless occupations, energy per original mass, forces, and rotation speeds do not change. The raw unconverted failure remains in the tables. This is the Newtonian cross term of an already specified weak-field reduction, not a general spacetime perturbation identity or a change of G.

## Sky coordinate, sign, and coverage

At z>0 let g_in be positive toward the Galactic axis and g_z positive upward. At a given cylindrical (R,z), spherical components are a_r=(−R g_in+z g_z)/r and a_θ=(−z g_in−R g_z)/r=−(R/r)T, with r=hypot(R,z), θ measured from Galactic north, and T=g_z+(z/R)g_in. Reflection changes the sign of a_θ but not a_r inside these models. Spherical gravity has zero a_θ. A north–south difference in actual data is not a second independent measurement of the same model residual. The model can be compared directly to a_θ; it is not necessary to reconstruct two independent observed accelerations for that one comparison.

[Lim et al., Fig. 9 and §3.2](https://arxiv.org/html/2305.13358v3) use 3D accelerations inferred from stellar phase space with an approximate equilibrium assumption. The upper-left and middle-left panels are radial traces at z=±1.5 kpc. Evaluate at the frozen *spherical* radii for R=6 and 8.3; the R=12 site is outside the stated volume and is not scored. Extract central strokes plus both uncertainty envelopes from the pinned vector PDF, validate affine axes with actual ticks and the centerline identities against rendered colors. These are graph readings, not underlying raw stars or a joint likelihood. The precision of observed numbers is limited by the graph itself. No raw point outside its panel's visible limits is used. For a prospective multiradius test use a component/position covariance, include baryon and geometric nuisance terms, and do not assume independent pointwise bands. No raw northern/southern force values were used to set the underlying stellar or gas templates.

## Census consistency is a separate investigation

For fixed gas and any spherical halo, the uniform stellar scale needed by a given polar angle is η=(−r a_θ/R−T_g)/T_star. It is independent of the halo's mass profile. Compare intervals from the plotted bands to a scale obtained separately from the [McKee et al. local star census, Table 1](https://arxiv.org/pdf/1509.05334), not by fitting a rotation or polar force. The census reports components including brown dwarfs and remnants, excluding halo stars at large |z|; the APOGEE-to-mass conversion is not an identical population inventory. A subtraction of the brown-dwarf central entries is only a sensitivity case, not a newly calibrated uncertainty. The two census columns and midplane entry are correlated summaries.

The optional post-comparison deformation rho′(R,z)=η rho(R,z/b)/b keeps surface density shape vs R and changes vertical heights by b; the physical finite height bound scales to 10b. Given the census's total column and its fraction inside |z|=1.1 kpc, positivity makes the predicted fraction monotone in b across the relevant domain and fixes a unique b within this restricted deformation. No angular measurement sets η or b in that forward experiment. Check the unused midplane density and reverse the construction (total + midplane → 1.1-kpc column). The data do not specify that the same compression applies throughout the Galaxy. As a separate consistency inequality for an *untruncated* positive mixture of exponentials, Jensen gives f(<H)≤1−exp(−2H rho0/Σ), with all quantities in consistent length units. The census central columns then require rho0≥0.0413 solar masses/pc³, compatible with their 0.043. This inequality is not used as a rejection of the truncated model.
