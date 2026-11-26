> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# A particle inventory, an exterior condition, and a causal thermal stress

## Where an absolute error can enter

Use conformal time η and the saved shear-free spherical ADM metric, with lapse α=a exp U and radial scale ℓ=a exp(−V). The normal expansion is h=H at the fixed outer matching radius L=24 comoving Mpc. Write Einstein-normalized stress variables (8πG times the physical density, flux and pressure, c=1); j is the covariant radial momentum. The radial momentum constraint then reads h′=j/2. The radial momentum balance of an independently conserved stress is

    ∂η j + 3 (∂η ln ℓ) j = −α [∂r P_r + U′(E+P_r) + 2(1/r−V′)(P_r−P_t)].

For a species treated only in the expanding background the spatial stress gradient/current response is omitted. Integration from L **to the site**, not from an adjustable zero point, gives the predicted source of the old measured-minus-trace error: +½ ∫ a (E+p) [exp U(r)−1] dη. This is exact for the corresponding homogeneous omitted-force term; it is not the prediction of a whole nonlinear solution. The finite boundary adds an independent term. At U=V=0, h=H and original U′=V′, the geometry term of the trace reduces to −V′²/(2a). Thus the box defect (measured minus predicted) is +½∫[a δP_r(L)+V′²/a]dη. The pulse also has material discretization and possible kinematic residuals; the absolute-site test does not assume these vanish. See the preceding radial identity (not bundled here), edge derivation (not bundled here) and the [3+1 Einstein conventions](https://arxiv.org/abs/gr-qc/0703035).

Native CAMB returns D=a⁴ E. Photons and relativistic neutrinos have E+p=4E/3. For the massive neutrino use the native dimensionless mass M=m/Tν0 and the actual thermal distribution: ε=(q²+a²M²)½, v=q/ε, E∝a⁻⁴∫q²ε f dq and p∝a⁻⁴∫q⁴ f/(3ε) dq. Normalize to the native E at the starting scale factor, not the size of any measured residual. Independently check E+p against −(1/3)dE/d ln a. Compare this physical inventory with the effective residual −2 Hdot−E_dust−E_wave,rest−W_s². The wave's tiny background interference about the rest approximation is not identified as a new hot species. Hdot comes from differentiating the originally used log-linear interpolant; agreement of H values is not a guarantee of agreement of this subdominant difference of derivatives.

## Thermal transport without a fictitious cold neutrino

Set δf=−(∂f₀/∂ln q) Θ for an initially unperturbed, isotropic distribution in the local orthonormal frame. The linear collisionless Boltzmann equation in conformal Newtonian gauge, with the present signs, is

    (∂η + v n·∇) Θ = ∂η V − n·∇U/v.

This is the local real-space form of the standard kinetic equation; see [Ma & Bertschinger, 1995](https://arxiv.org/abs/astro-ph/9506072). The trajectory uses the true v(q,a), not a fluid sound speed. We neglect collisions and terms nonlinear in metric perturbations in this thermal transport. Cold material, both scalar sectors and the constraint solver retain their existing equations. The finite thermal initial state is a control choice; prior formation could supply additional incoming multipoles.

The source at time t reaches x by free streaming over signed distance s=∫v dη. At radius r, μ=n·x̂ and u=|x−sn|, so n·∇U=(rμ−s)U′(u)/u. These expressions work unchanged for the negative elapsed-time test. Write W=q²ε(−∂lnq f₀) times the native normalization and a⁻⁴. Then δE=∫W〈Θ〉, j=ℓ∫W v〈μΘ〉, δP_r=∫W v²〈μ²Θ〉 and Π=P_r−P_t=∫W v²〈P₂(μ)Θ〉. For massless particles the weight integrates to 4E. Each null beam has trace-free stress, and the angular average can carry a nonzero radial current or anisotropy even when its background pressure is isotropic. This uses the geometric-optics stress of radiation; it is not a derivation of charge or a quantum measure.

## Reducing a whole radial integral to the two causal neighborhoods

For a radial function f, let S_s f(x)=〈f(x−sn)〉 on a sphere and B_s f(x)=∫₀¹3y² S_sy f(x) dy in its ball. Define A_s=S_s−2B_s/3. The divergence theorem gives 〈n f(x−sn)〉=−(s/3)∇B_s f, and ∂s(s B_s/3)=A_s. Thus the integral from r to L of the dipole of the kinetic drive is just the difference between the two endpoint values of

    (s/3) B_s (∂η V) + A_s U/v.

For the trace we also need a pressure combination P*(r)=δP_r(r)−2∫_r^L Π(x)dx/x. For the angular distribution f(x−sn), the derivative with respect to r of 〈μ² f〉+the integrated anisotropy contribution is ∂r〈μ² f〉+2〈P₂ f〉/r. This is the radial divergence of 〈n_i n_j f〉; since ∂s〈n_i f〉=−∂j〈n_i n_j f〉, it equals ∂r A_s f. Therefore P*(r) for a single translated scalar is A_s f(r)−A_s f(L)+〈μ² f(L−sn)〉, with the last notation evaluated at the outer location. Apply this formula to ∂ηV and to ∂s U/v separately. No integral crosses unobserved radii and guesses an arbitrary pressure there: in this linear identity the interior integrals cancel analytically. It still depends on the state and field in neighborhoods of both endpoints. Signed backward travel and the two distinct derivatives (source time versus propagation distance) matter.

In the test-field calculation put J=−½∫_r^L j dx, using ℓ=a to first order. The independently evaluated moments must obey

    ΔJ + ∫[3aH J + a(P*(r)−δP_r(L))/2]dη = −½ ∫a(E+p)[U(r)−U(L)]dη.

The right side is fixed before sampling any perturbed particle. On the left, the pressure/anisotropy and momentum are actual kinetic solutions, evaluated by the causal integrals. The test also includes a polynomial with independent closed-form radial integrals and a monochromatic spherical mode with independently differentiated Bessel functions. A potential constant in space cancels as a physical drive. The finite live solver does not use this endpoint identity or its target to manufacture a current: it transports angles and momenta, measures each local stress, solves the constraints, and measures radial flux and pressure from that separate representation.
