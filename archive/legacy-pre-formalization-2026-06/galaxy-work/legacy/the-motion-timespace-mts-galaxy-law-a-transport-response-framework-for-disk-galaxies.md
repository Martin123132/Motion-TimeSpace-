TITLE
The Motion–Timespace (MTS) Galaxy Law: A Transport–Response Framework for Disk Galaxies

ABSTRACT
We present a transport-based derivation of galaxy rotation curves within the Motion–Timespace (MTS) framework. A curvature–exchange field, emerging from a coarse-grained microscopic scalar field, drives a support field whose radial transport produces a closed-form rotation law. The resulting background law is cosmologically normalised and contains no free parameters on a clean subset of disk galaxies. First-order corrections arise from structural deviations, specifically bulge concentration and gas depletion. Using photometric scale lengths and raw rotation curve reconstructions, we show that (i) the background law accurately describes bulgeless gas-rich disks, (ii) a saturating gas correction improves gas-poor systems, and (iii) bulge effects are present but sub-dominant in late-type galaxies. Early-type galaxies are not described by the same response family. The framework therefore defines a transport-driven law for disk galaxies with controlled structural corrections rather than a universal galaxy model.

------------------------------------------------------------

1. INTRODUCTION

Galaxy rotation curves exhibit systematic deviations from baryonic expectations. Existing approaches either introduce additional matter components or modify gravitational dynamics. In contrast, the MTS framework treats galaxy dynamics as a macroscopic transport response to a cosmological curvature–motion background.

The goal of this work is to derive the galaxy law from first principles within this framework and test it directly against raw rotation curve data. The emphasis is on:

- deriving the background law without free parameters,
- identifying the minimal correction sector required by data,
- distinguishing what is genuinely derived from what remains empirical.

------------------------------------------------------------

2. THE MTS FRAMEWORK

2.1 Emergent geometry

We consider a scalar field ψ defined over spacetime. The macroscopic metric arises from coarse-grained gradient covariance:

g_μν = η_μν + ⟨∂_μ ψ, ∂_ν ψ⟩

This defines spacetime as an emergent statistical structure of underlying microscopic motion.

2.2 Curvature–exchange field

A scalar field Γ = F[ψ, g] encodes curvature–motion exchange at the macroscopic level. It acts as an effective source term in the emergent geometry.

2.3 Action

The system is governed by an action containing:

- Einstein–Hilbert term with Γ contribution
- kinetic and potential terms for Γ and ψ
- a constraint linking Γ to ψ
- matter sector
- transport sector

The transport sector introduces a support field χ responsible for deviations from baryonic rotation.

------------------------------------------------------------

3. TRANSPORT EQUATION AND BACKGROUND LAW

3.1 Transport closure

At lowest isotropic order, the support tensor takes the form:

Σ_μν = (Γ/4) g_μν

This fixes the projection factor of 1/4.

The resulting transport equation is:

u^μ ∇_μ χ + χ/τ_Γ = Γ/4

3.2 Galaxy limit

In the stationary outer-disk regime:

u^μ ∇_μ → v_Γ d/dr

giving:

v_Γ dχ/dr + χ/τ_Γ = Γ₀/4

Defining the transport scale:

L = v_Γ τ_Γ

the solution is:

χ(r) = (Γ₀/4) L (1 − e^(−r/L))

3.3 Observable mapping

Identifying:

χ(r) = V²(r) − V_bar²(r)

gives the background galaxy law:

V²(r) = V_bar²(r) + (Γ₀/4) L (1 − e^(−r/L))

3.4 Scale closure

A resonance argument yields:

L = k (j_bar / V_bar,char)

with k ≈ 0.9 on disk galaxies.

3.5 Cosmological normalisation

Coarse-graining gives:

Γ₀ = ν c H₀

with ν ≈ 1/(2π), so:

Γ_drive = cH₀ / (8π)

3.6 Zero-parameter law

The resulting background law is:

V²(r) = V_bar²(r)
+ (cH₀ / 8π)
  (k j_bar / V_bar,char)
  [1 − exp(−r V_bar,char / (k j_bar))]

------------------------------------------------------------

4. SHAPE CORRECTION

A simple exponential turn-on does not describe all disk galaxies equally well. Replacing the radial response with:

1 − exp[−(r/L)^q]

improves fits.

For late-type galaxies (LTGs), the preferred value is:

q ≈ 1.3

This defines the LTG response kernel.

------------------------------------------------------------

5. LINEARISED CORRECTION SECTOR

5.1 Perturbation equation

Writing:

Γ = Γ_bg + δΓ

the perturbation obeys a screened equation:

(∇² − ℓ_Γ⁻²) δΓ = −δS_Γ / Z_Γ

5.2 Source channels

Two dominant structural sources emerge:

- bulge concentration
- gas depletion and disk evolution

These define the first-order correction sector.

------------------------------------------------------------

6. BULGE CORRECTION

6.1 Compactness scaling

For a compact source of size r_bul:

δΓ_b ~ Q_b / (Z_Γ r_bul)

so the screened field alone gives a linear compactness enhancement.

6.2 Gradient-sensitive closure

Including radial gradient sensitivity in the transport projection:

Σ → Γ/4 + ℓ_Γ ∂_r Γ

yields:

α_b ∝ (r_disk / r_bul)²

Thus the square-law scaling arises from:

- screened compactness enhancement
- transport sensitivity to radial gradients

6.3 Empirical LTG form

For LTGs, the preferred bulge term is mild:

1 + A_b b_frac

with A_b ≈ 0.46 (peak definition) or ≈ 3.2 (integral definition)

These are consistent normalisations of the same underlying physics.

------------------------------------------------------------

7. GAS CORRECTION

7.1 Transport memory

The time-dependent transport equation:

dχ/dt + χ/τ_Γ = Γ_drive(t)/4

implies exponential memory of past forcing.

7.2 Structural proxy

A simple gas fraction term (1 − f_gas) is insufficient. Including photometric structure yields:

z = (1 − f_gas) |ln(h/L)|

where h is the stellar exponential scale length.

7.3 Saturation form

The preferred functional form is:

1 − exp(−λ z)

with λ ≈ 0.4

This reflects a saturating build-up of depletion-induced mismatch.

7.4 Interpretation

- (1 − f_gas): primary driver
- |ln(h/L)|: secondary structural modulation

------------------------------------------------------------

8. FULL LTG LAW

The current best LTG law is:

V²(r) = V_bar²(r)
+ (cH₀ / 8π)
  [1
   + 0.4566 b_frac
   + 1.0709 (1 − exp(−0.4 (1 − f_gas) |ln(h/L)|))
  ]
  (0.9 j_bar / V_bar,char)
  [1 − exp(−(rV_bar,char / (0.9 j_bar))^1.3)]

------------------------------------------------------------

9. RESULTS

Validation was performed using raw rotation curve reconstructions.

9.1 Clean branch (bulgeless gas-rich LTGs)
- RMSE ≈ 8–10 km/s
- Correct normalisation within a few percent

9.2 Full LTG sample
- Zero-parameter law: ≈ 19.1 km/s
- Corrected law: ≈ 17.1–15.8 km/s

9.3 Gas-poor LTGs
- Significant improvement under correction sector

9.4 Performance ceiling
- ≈ 10.2 km/s
- Residual gap due to baryonic uncertainties and structure

9.5 ETGs
- RMSE ≳ 49 km/s
- Not described by the LTG response family

------------------------------------------------------------

10. INTERPRETATION

The results support a hierarchical structure:

Level 1:
Clean disk galaxies follow the background transport law.

Level 2:
Gas depletion introduces a saturating correction.

Level 3:
Bulge concentration introduces a secondary correction.

Level 4:
Early-type galaxies require a different response family.

------------------------------------------------------------

11. DERIVED VS EMPIRICAL COMPONENTS

Derived:
- Transport equation and exponential response
- Scale law L ~ j/V
- Cosmological normalisation cH₀/(8π)
- Saturation form of gas correction

Derived with closure assumption:
- Bulge square-law scaling via gradient-sensitive transport

Empirical:
- Amplitudes A_b, A_g
- Exact proxy for z
- Shape parameter q

------------------------------------------------------------

12. CONCLUSION

The MTS framework produces a cosmologically normalised transport-response law for disk galaxies. The clean branch provides the strongest evidence, while first-order corrections account for gas depletion and structural variation.

This is not a universal galaxy law. It is a controlled, physically motivated description of late-type galaxies, with early-type systems requiring a separate response model.

------------------------------------------------------------

FINAL STATEMENT

Disk galaxy rotation curves are consistent with a transport response to a cosmological curvature background, with saturating corrections driven primarily by gas depletion and secondarily by structural concentration.
