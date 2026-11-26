> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# Initial gravitational feedback: the vector, its boundary, and what enters the stellar work

At the launch, the two ordinary potentials (source-resolved minus represented) define a difference U and acceleration d=−grad U. The initial wave states and their first density derivatives are matched. In the inertial frame, continuity and momentum therefore give δρ''=−div(ρ d). The self-field a=−4πG grad Δ⁻¹ρ has fixed-position curvature 4πG P(ρd), P=grad Δ⁻¹div. For two frames initially at the same position and velocity but accelerated by their respective ordinary fields, add (d(X)·grad)a=−4πG Hess(Δ⁻¹ρ)d(X). This is not a free local subtraction from the gravitational law. Use the same units throughout the calculation: U in (km/s)², lengths in kpc, ρ in solar masses/kpc³. The final factor 4πG times the squared km/s→kpc/Myr conversion gives force curvature in (km/s)²/kpc/Myr².

**Which force enters stellar work?** If the comparison is between an updated wave and the old saved wave *both sampled along the same corrected ordinary-matter trajectory*, only the fixed-position wave difference belongs in the new term. The translation of the old wave was already present when changing the trajectory. Both wave fields and their first derivatives coincide initially at every fixed point; evaluating their difference on the same path adds no second-order advection term. For star and centre at x,X, with initial relative velocity v, the leading extra specific work from updating just the wave is
`W(t) = [v·(δa_fix''(x)−δa_fix''(X))] t³/6 + higher orders`.
Uniform common acceleration cancels. Opposite initial velocities must give opposite coefficients in the same positions. A zero average over paired velocities cannot rule out work on individual stars, nor can an initial coefficient determine a long-term escape rate. Comparing *two different frame histories* instead produces the moving-frame readout; do not add this term to the fixed-position live correction a second time.

## Whole-wave calculation
Use the exact product decomposition ρd=−grad(ρU)+U grad ρ, so P(ρd)=ρd−U grad ρ+P(U grad ρ). This leaves the sharp local acceleration in an independently evaluated Newton field, not in a low-degree angular fit. U is gauged to zero at the launch centre. An additive constant cancels because P(grad ρ)=grad ρ for the isolated compact wave.

Use spherical coordinates about the Galaxy and μ=cos θ. Expand the radial component of B=U grad ρ in a_l(r)P_l(μ) and its polar component in b_l(r)∂θ P_l(μ). Integration by parts in the isolated Green integral (no derivative of a noisy source) gives
```
I_l(r) = ∫_0^r (s/r)^(l+1) a_l+(l+1)b_l (not bundled here) ds
E_l(r) = ∫_r^∞ (r/s)^l a_l−l b_l (not bundled here) ds
u_l    = [l I_l−(l+1) E_l]/(2l+1)
u'_l   = a_l−l(l+1)(I_l+E_l)/[(2l+1)r].
```
Then P(B)=grad u. The local a_l term cancels −U∂rρ in the radial component. Keep −U∂θρ/r in the polar component. For projection of ρ itself use the isolated scalar Green solution to compute the three-dimensional Hessian including the azimuthal and translation components. The latter need not be axisymmetric about the Galaxy's axis.

The ordinary source is the retained positive prescription over its cylinder, both mass-redistribution components included, not a zero continuation of the Pal 5 patch. Multipoles extend outside the source with isolated decay. The wave integral covers its actual finite-element domain, ending at 388.41 kpc. Volume integrals include all occupied elements, not only the two intersecting the cluster. Only the readout of U and d in the explicit local term uses the local chart or the direct isolated Newton integral. Angular truncation of U at L gives modes up to L+68 in B (ρ comes from an amplitude with degree at most 34). Cutoff, quadrature and independent source comparisons are empirical convergence checks, not infinite-series enclosures. They apply to this retained model source, not to a measured Milky Way density.

## An independent check and a local solution for weak angular signals
Now use spheres **centred on the cluster**, not the Galaxy. Let h=P_l(n·axis), angular brackets denote sphere mean, and F=ρ[d(x)−d(X)] in common time units. Define radial mode g_r=(2l+1)⟨g·n h⟩, polar-gradient mode g_t=(2l+1)⟨g·∇Ω h⟩/[l(l+1)], for outward g including the moving-frame correction. All sources exterior to a given sphere contribute harmonics proportional to r^l inside it; hence they cancel exactly in D=g_r−l g_t. The remaining interior combination follows directly from δρ''=−div F integrated against s^l h:
```
D(r) = 4πG(2l+1) [ ⟨h F_n⟩_r
    − ∫₀¹ v^(l+1) ⟨(l h n+∇Ω h)·F⟩_(vr) dv ].
```
For l=0 this is the original Gauss check (positive outward). For l>0 it measures a directional component with no unknown exterior. It does **not** say exterior gravity vanishes.

A complete interior angular mode follows from the same I,E integrals using the projected F in the local spheres. At boundary B fix E(B) from the whole-domain potential coefficient (g_t) or independently the radial force there combined with D(B). Integrate inwards with the actual F on r<s<B. The exterior mass contribution itself is g_t,out(r)=(r/B)^(l−1)[g_t(B)+D(B)/(2l+1)], g_r,out=l g_t,out. This decomposition separates the true exterior density source, not a fictitious interface sheet from abruptly truncating F. Move B to test matching; no fitted exterior constant. Reconciling D by construction is not an independent validation of the entire interior field: use the other boundary condition, boundary radius, source integration and raw whole-domain readouts as checks.
