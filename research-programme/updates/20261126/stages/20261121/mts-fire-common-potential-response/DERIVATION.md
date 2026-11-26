> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# A causal test of the parent wave's Newtonian coupling

## What is changed

The parent action note (not bundled here) supplies a positive real heavy mode, its canonical Hilbert stress and the Newtonian envelope coupled to the same metric as ordinary matter. The time-averaged nonrelativistic mass-amplitude convention here is ρ=|a|². The experiment uses the [original formation preparation](../../20261120/mts-pre572-wave-preparation/RESULTS.md) and previous two-wave balance (not bundled here), including their conditional occupation and foreground. No dark-matter sector or adjustable Poisson coefficient was added. All zero potentials at the outer boundary and the chemical rotating frame are inherited.

In native units write H[b]=K+Vₒ+P[|b|²], with P the existing real linear Poisson map (including angular projection). For the reset wave b evolve i ḃ=H[b]b. For the active inherited wave a, evolve i ȧ=H[a]a. The intervention uses t(572)=a(572) but i ṫ=H[b]t. The passive wave is **not additional mass** alongside b. Its applied metric is the reset metric. Postprocessing P[|t|²] gives the force its density *would* source, so P[|a|²−|t|²] tests how responding to its own changed density reshapes the inherited force. Ordinary gravity and the reset self-gravity stay in play. Since t and b obey the same Hermitian Hamiltonian, both norms and their complex overlap are preserved. Repeat on both original time grids.

## Predict the fully coupled response without using the changed solution

Rotate a's initial global phase to align its number inner product with b, normalize to the same archived norm N, and use a unit-sphere arc a₀(s)=b₀ cos(sθ)+t₀ sin(sθ), with ⟨b₀,t₀⟩=0, ‖t₀‖²=N. Set θ from the initial overlap (use atan2 for small angles). s selects a **controlled initial state**, not a new coupling. Only s=1 is the archived early preparation. With a(s)=b+s h+s² j+O(s³), define

    L = P[2 Re(b* h)],      Q = P[2 Re(b* j) + |h|²].
    i ḣ = H[b] h + L b,     i j̇ = H[b] j + L h + Q b.
    h₀=θ t₀,                  j₀=−θ² b₀/2.

First and second order here refer to powers of s. The second derivative is twice j. Differentiating norm gives 2 Re⟨b,h⟩=0 and 2 Re⟨b,j⟩+‖h‖²=0 throughout. The response of the Newtonian force uses the same density coefficients as L,Q but applies the gradient of P at the actual probes. In the discrete calculation, average each **endpoint density variation** before solving Poisson, multiply each potential by the relevant midpoint wave, and solve implicitly. This differentiates the *actual* native update; density of midpoint is not average endpoint density. The passive tangent instead solves only i ḣ_pass=H[b]h_pass and gives the exact passive arc at every time. The numerical predictions were sealed at both resolutions before evolving the new nonlinear half-strength and reversed states. The full positive endpoint was already exposed. No astronomical holdout or parameter fit is claimed.

## Exact retarded source and its angular structure

With d=a−t, the same common potential gives i ḋ=H[b]d + (P[|a|²]−P[|b|²])a and d₀=0. Project the difference potential into its spherical average and the remaining angular part at each radius using the original angular quadrature. Transport each source separately with H[b]; the resulting fields sum to d. This is an identity evaluated using the actual changed density, **not** a first-principles forecast based on an unmeasured density. At readout, for each transported piece dᵢ the contribution to the density is 2 Re[((a+t)/2)* dᵢ]. The sum gives |a|²−|t|² exactly and splits the quadratic interference evenly.

Re-expand that final density in Legendre degrees 0 through 68 and integrate both interior and exterior Newton multipoles. A spherical *potential drive* can act on a flattened wave and produce a degree-two *density response*; there is no conflict with the vanishing polar derivative of a spherical density's own Newton potential. The monopole's direct exterior radial force and either side's monopole polar force vanish. The summed angular readout is checked against a separate evaluation of the entire density difference.

## Source coupling and energy, not just curve agreement

The normalized Newton interaction is reciprocal: ∫ρ₁ P[ρ₂]=∫ρ₂ P[ρ₁] with the retained boundary. For a self-gravitating wave the native energy is ⟨K+Vₒ⟩+½∫ρP[ρ]. In the reset metric the passive energy is ⟨K+Vₒ+P[ρ_b]⟩_t: *no* half on a prescribed potential. Its change includes not only ordinary work but ∫ρ_t ∂ₜP[ρ_b]. On each conservative midpoint step, replace the instantaneous work by the mean endpoint density times the endpoint potential change. Check reciprocal metric work also as ∫(ρ_b⁺−ρ_b⁻)(P[ρ_t⁺]+P[ρ_t⁻])/2. At a single time the exact difference between the active energy functional contrast and that in a prescribed reset potential is ½∫(ρ_t−ρ_b)P[ρ_t−ρ_b]≤0. These identities distinguish the diagnostic transport from a closed self-gravitating two-species proposal. They do not derive the numerical value of G.

## Replay

In the retained single-threaded Python 3.13 environment run `python -B predict.py 32`, then 64, followed by `physical_test.py` at 32 and 64 with the same interpreter options; then `compare.py`, `angular_readout.py`, `metric_stress.py` and `verify.py`. No-save mode compares retained bytes. Stage output does not alter any prior archive. Newly generated trajectories represent only the original time-dependent external interpolation and finite wave space. See [stress constraint and its ordering](METRIC-STRESS.md) for the separate metric test.
