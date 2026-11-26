> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# Compatible radial transport, finite detectors and a weak-field source prediction

Inputs: prepared GR clouds and clock (not bundled here), the unchanged Newtonian evolution and ADM constraint identity (not bundled here). Work on the same minimally coupled, positive quadratic heavy branch. The two real field quadratures are the saved phase preparation, not a new complex fundamental particle. Same on/off states, signed hosts, native surrounding pressure and anisotropy, local conservation of surrounding energy/momentum, mass, angular truncation and 273.43 proper years. The current residual is in a conditional GR-versus-Newton calculation at z=86.11, not a present-day Galactic constraint.

## A spatial operator test, not a change to the action

On cell centres the archived sixth-order first and second derivatives are independent approximations. The radial part of the momentum budget differentiates twice by composition; the curvature instead uses its separate second derivative. We tested (i) the archived method; (ii) composing the first derivative with itself on all fields; (iii) also differencing the properly weighted radial fluxes in dust continuity, the spatial wave operator, surrounding energy and constraint transport, with sixth- and eighth-order alternatives where stated. For example, write n for orthonormal radial flux, t₂ for the angular flux coefficient, N=exp ℓ and b for the log of the angular radius divided by r. Then

    div J = [r² exp(ℓ+2b)]⁻¹ ∂r[r² exp(2b) n]
            −(6/r) [exp(−b₀) t₂ − v₂ exp(−ℓ₀) n₀] P₂.

Here v₂ is the radial-surface angular shift, not a matter velocity. The radial centre derivative itself is a difference of shared face fluxes: (1,−8,37,37,−8,1)/60 is the six-point face interpolant whose difference gives the archived centre gradient. Using the same centre derivative twice also annihilates an alternating grid perturbation. Such a mode should have a large second derivative, not zero. Hence we separately tested **staggered** derivatives with
Gf at face i+½ = Σ wⱼ(fᵢ₊ⱼ₊₁−fᵢ₋ⱼ)/h, w=(75/64,−25/384,3/640), and the matching face-to-centre D. In the interior D=−Gᵀ. The Laplacian's principal part is DG, not (centre gradient)²; its positive high-frequency eigenvalue in units h⁻² is 4(Σ(−1)ʲwⱼ)². Matter phase gradients and radial number fluxes live at faces, as does the radial momentum defect used in the independent transport prediction. Other first derivatives interpolate face gradients to centres; angular terms and the existing exterior buffer are explicit. This is not a claim of a fully constraint-preserving discretization or exact product rules. [Operators](evidence-001.zip) (archive member: `scheme.py`) · [staggered method](evidence-001.zip) (archive member: `stagger.py`) · [face balance](evidence-001.zip) (archive member: `face-balance.csv`) · adjoint and checkerboard test (not bundled here).

Tests include a non-polynomial, deliberately off-constraint profile on a nonuniform, intrinsically flat metric: areal coordinate R=r(1+0.065 exp[−(r/1.74)²]), Gaussian in R² centred near the physical aperture, widths 0.20, 0.08, 0.04 Mpc. For k=k₀(R)+k₂(R)P₂ and diagonal spherical shear σ(R), the exact source is −2 div M=−2(σ″+5σ′/R+3σ/R²)+4∆k/3; the projected/free trace transport is (2k/3+pσ/2)H_c−2 div M. Check the direct differentiated scalar as well as the divergence against the analytic values. Also repeat the independently known evolving, nonlinearly reparametrized dust spacetime in both radial evolution choices. No threshold or initial data was altered to make the pointwise GR remainder pass.

## Proper-length measurement and independent weak transport

Keep the original point measurements. Add two distinct, prospectively specified finite detectors, centred at the original middle proper radius, with half-widths 15% and 30% of that distance. These are compact averaging kernels for ideal tidal measurements, not data, inferred instrumental beams or replacements for the point test. [Frozen definition](windows.md). If y=∫N₀ dr is the proper radial distance in launch units, V=∫N₂ dr and W(y) the normalized window, the fixed-y quadrupole coefficient of a scalar is T₂−(V/N₀)T₀′. Integrate in y and integrate once by parts:

    average = ∫ [A T₂+B T₀] dr,
    A=W N₀,   B=W′ N₀ V+W N₂.

No boundary term survives: the weight and its low derivatives vanish at both ends. Its proper-time derivative includes both tensors' time dependence AND the time derivatives of A and B. The measurement has no spatial derivative of the tidal scalar left in it. This matters when the subtraction of two very similar tidal histories would otherwise differentiate spatial noise. We evaluate within each resolved radial cell, not by smoothing the three old point results.

For the independently predicted subsidiary equation there is an additional integration by parts. Let J₀=r² exp(ℓ₀+2b₀), J₂/J₀=ℓ₂+2b₂, F=r² exp(2b) M_n. Set P=A/J₀ and Q=(B−A J₂/J₀)/J₀. The integral of minus twice the momentum-defect divergence is

    2 ∫(P′F₂+Q′F₀) dr + 12 ∫ A [e^(−b₀) M_θ − v₂ e^(−ℓ₀) M_n₀] dr/r.

The P′,Q′ are derived from the actual proper metric and compact weight; neither uses the measured Hamiltonian time derivative. Compare separately against face-divergence sampling and the direct derivative of H_c. By the predecessor's identity, ∆H_c/6 equals the split in the two tidal readouts on identical geometry. Error relative to the *small defect* and relative to the *whole tidal change* must not be interchanged. [Proper ruler code](evidence-001.zip) (archive member: `window.py`) · [moving-metric and weak-flux control](evidence-001.zip) (archive member: `proper-window-controls.csv`).

## What part of the excess can the weak-field equations predict?

For the radial TF tide the Gauss expression on this branch is

    T_G = S_nn^TF − E/3 + X/2 + k²/9 − kσ/3 + σ²/4,
    X = R_surface − κ²/2.

Split E into conserved rest/area number times mass per proper volume, energy in excess of that rest value, and the surrounding species. For dust, E_extra=ρ_ref n(Γ−1)/√q and S_nn^TF=(2/3)ρ_ref n p_hat²/(√q Γ). Compute Γ−1 as p_hat²/(Γ+1). Only one quadrupolar order is retained: the tangential speed is first order and its square is second order. For the real wave quadratures write L=log U and z=W_slow/U−k/(2µ) in the preceding normal-clock convention. Define A_h=ρ_ref exp(2 Re L), ∂n=exp(−ℓ)∂r. Exactly on this phase ensemble at this angular order:

    E_rest = A_h(1−Im z)
    E_extra = A_h[(Re z+k/(2µ))²+(Im z)²+|∂n L|²/µ²]/2
    S_nn^TF = (2/3) A_h |∂n L|²/µ².

Consequently the spatial-gradient term in S_nn^TF is **−4 times** its term in −E_extra/3. The net spatial coefficient is +1/2, not a fitted force coefficient. Normal-amplitude/frequency energy contributes separately with coefficient −1/6. Split the spatial term into log-amplitude and phase-gradient squares, then differentiate each and transport the same proper ruler. On the dust-off branch the heavy species has only its dust term. The spatial positivity of the underlying square does not require that its quadrupole or its temporal switch has positive sign.

At leading nonrelativistic order the Newtonian motion-phase gradient gives v_r=∂r V_matter, and the wave amplitude gives ∂n Re L/µ=(∂r ln n)/(2am). Everything on this right-hand side is available from the archived wide Newtonian evolution, without a relativistic tide or a new coefficient. The prediction is the time change of

    ½ Σ ρ_ref (a★/a)³ n [v_rel,r² + (∂r ln n)²/(4a²m²) for the wave only],

where all species carry the velocity term and only the pressure-on wave carries the amplitude-gradient term. For example the first quadrupole of n(∂r ln n)² is 2 n₀′ n₂′/n₀−n₂(n₀′/n₀)². Evaluate the endpoints on a fixed proper-length distribution: quadrature radii in comoving coordinates shrink as a★/a. The original Newton equations and incident source were evolved, not a fitted history of the excess. Freely falling comparison normals start at rest in the normal-initialized flat chart. Their leading peculiar speed at the endpoint is −∫d ln a (a/a_end)∇Φ/ℋ, using the direct native potential and mass-sourced excess potential, including the spherical host. This is evaluated along the fixed final comoving labels to leading order in normal displacement (largest estimated displacement ~1.3e−12 comoving Mpc). An Eulerian comparison omits that subtraction. This is a short-time Newtonian frame prescription, not an exact nonlinear gauge transformation. [Formula recorded before calculating its predictions](stress-forecast.md) · [weak-field calculation](evidence-001.zip) (archive member: `stress_forecast.py`) · [independent microscopic readout](evidence-001.zip) (archive member: `source_budget.py`).

The **remaining** excess should not be equated to a new coupling. The local proper rest-mass term must be compared with the Newtonian local term −exp(−3x) S(r)/3 including its own dilution and ruler motion; compare the rest of the Newtonian kernel to the intrinsic and extrinsic geometry together. This reveals large terms of opposite sign. Their net, not either term alone, is the next quantity to derive from the mass and momentum constraints.
