TITLE
The Motion–Timespace (MTS) Galaxy Law: A Transport–Response Framework for Disk Galaxies

ABSTRACT
We present a transport-based derivation of galaxy rotation curves within the Motion–Timespace (MTS) framework. A curvature–exchange field, emerging from a coarse-grained microscopic scalar field, drives a support field whose radial transport produces a closed-form rotation law. The resulting background law is cosmologically normalised and contains no free parameters on a clean subset of disk galaxies. First-order corrections arise from structural deviations, specifically bulge concentration and gas depletion. Using photometric scale lengths and raw rotation curve reconstructions, we show that (i) the background law accurately describes bulgeless gas-rich disks, (ii) a saturating gas correction improves gas-poor systems, and (iii) bulge effects are present but sub-dominant in late-type galaxies. A zero-free-parameter gas benchmark derived directly from the transport equation recovers a substantial fraction of the correction signal. Early-type galaxies are not described by the same response family. The framework therefore defines a transport-driven law for disk galaxies with controlled structural corrections rather than a universal galaxy model.

------------------------------------------------------------

1. INTRODUCTION

Galaxy rotation curves exhibit systematic deviations from baryonic expectations. Existing approaches either introduce additional matter components or modify gravitational dynamics. In contrast, the MTS framework treats galaxy dynamics as a macroscopic transport response to a cosmological curvature–motion background.

The aim of this work is to derive the galaxy law within this framework and test it directly against raw rotation curve data. The emphasis is on separating derived structure from empirical closure and identifying the minimal correction sector required by observations.

------------------------------------------------------------

2. THE MTS FRAMEWORK

2.1 Emergent geometry

A scalar field ψ defines an emergent metric via coarse-grained gradient covariance:

g_μν = η_μν + ⟨∂_μ ψ, ∂_ν ψ⟩

2.2 Curvature–exchange field

A scalar Γ = F[ψ, g] encodes curvature–motion exchange.

2.3 Action

The system includes gravitational, scalar, constraint, matter, and transport sectors. The transport sector introduces a support field χ governing deviations from baryonic rotation.

------------------------------------------------------------

3. TRANSPORT EQUATION AND BACKGROUND LAW

The transport equation is:

u^μ ∇_μ χ + χ/τ_Γ = Γ/4

In the stationary disk limit:

v_Γ dχ/dr + χ/τ_Γ = Γ₀/4

Defining L = v_Γ τ_Γ:

χ(r) = (Γ₀/4) L (1 − e^(−r/L))

Mapping to observables:

V²(r) = V_bar²(r) + (Γ₀/4) L (1 − e^(−r/L))

Using:

L = k (j_bar / V_bar,char),   k ≈ 0.9

and:

Γ_drive = cH₀ / (8π)

gives the zero-parameter galaxy law.

------------------------------------------------------------

4. SHAPE CORRECTION

Replacing the exponential kernel with:

1 − exp[−(r/L)^q]

improves disk fits, with:

q ≈ 1.3 (LTGs)

------------------------------------------------------------

5. LINEARISED CORRECTION SECTOR

Perturbations satisfy a screened equation:

(∇² − ℓ_Γ⁻²) δΓ = −δS_Γ / Z_Γ

Two dominant source channels emerge:

- bulge concentration
- gas-driven disk evolution

------------------------------------------------------------

6. BULGE CORRECTION

Screened compactness gives linear enhancement. Including gradient-sensitive transport closure yields:

α_b ∝ (r_disk / r_bul)²

In LTGs, this appears observationally as:

1 + A_b b_frac

with:

A_b ≈ 0.46 (peak definition)
A_b ≈ 3.2 (integral definition)

These represent consistent normalisations of the same physics.

------------------------------------------------------------

7. GAS CORRECTION

7.1 Transport memory

dχ/dt + χ/τ_Γ = Γ_drive(t)/4

implies exponential memory of past forcing.

7.2 Observable proxy

Using photometric data:

z = (1 − f_gas) |ln(h/L)|

7.3 Saturation form

1 − exp(−λ z),   λ ≈ 0.4

Gas fraction is the primary driver, with structural mismatch providing secondary modulation.

------------------------------------------------------------

8. FULL LTG LAW

V²(r) = V_bar²(r)
+ (cH₀ / 8π)
  [1
   + 0.4566 b_frac
   + 1.0709 (1 − exp(−0.4 (1 − f_gas)|ln(h/L)|))
  ]
  (0.9 j_bar / V_bar,char)
  [1 − exp(−(rV_bar,char / (0.9 j_bar))^1.3)]

------------------------------------------------------------

9. RESULTS

Clean LTGs:
RMSE ≈ 8–10 km/s

Full LTG sample:
≈19.1 → ≈17.1–15.8 km/s

Gas-poor LTGs:
significant improvement

Performance ceiling:
≈10.2 km/s

ETGs:
RMSE ≳ 49 km/s (not described by LTG law)

------------------------------------------------------------

10. DERIVED GAS-SECTOR BENCHMARK

10.1 Derived form

From the transport equation, the gas correction is:

A_g ~ (L_past − L_now) / L_now × (1 − e^(−n))

Using L ~ j/V:

A_g ~ (j_past − j_now) / j_now × (1 − e^(−n))

This identifies the gas term as a fractional loss of transport scale filtered by finite-memory build-up.

10.2 Observable closure

Since j_past is not directly observable, we use:

z = (1 − f_gas) |ln(h/L)|

giving the zero-free-parameter benchmark:

A_g^(0) = 1 − exp[−(1 − f_gas)|ln(h/L)|]

10.3 Performance

All LTGs (median RMSE):
- zero: ~29.5 km/s
- simple gas: ~28.1 km/s
- mismatch benchmark: ~27.2 km/s

Gas-poor LTGs:
- zero: ~29.9 km/s
- mismatch: ~27.6 km/s

10.4 Interpretation

The derived benchmark recovers a substantial fraction of the gas correction signal without fitted amplitudes. The remaining discrepancy arises from observable proxy limitations and baryonic uncertainties.

------------------------------------------------------------

11. INTERPRETATION

The system exhibits a hierarchical structure:

Level 1:
Clean disks follow the background law

Level 2:
Gas depletion introduces a saturating correction

Level 3:
Bulge concentration introduces a secondary correction

Level 4:
ETGs require a different response family

------------------------------------------------------------

12. DERIVED VS EMPIRICAL COMPONENTS

Derived:
- transport law
- exponential kernel
- L ~ j/V
- cosmological normalisation
- saturation structure

Derived with closure assumption:
- bulge square-law scaling

Partially derived:
- gas correction amplitude (now constrained)

Empirical:
- observable proxy mapping
- coefficients A_b, A_g
- shape parameter q

------------------------------------------------------------

13. CONCLUSION

The MTS framework yields a cosmologically normalised transport-response law for disk galaxies. The background law is strongly supported on clean disk systems, while a derived saturation correction accounts for gas depletion effects. A zero-free-parameter benchmark confirms that the correction sector largely follows from the same transport physics.

The model is therefore not a purely empirical fit, but a structured physical law for late-type galaxies. Early-type systems remain outside the present response family.

------------------------------------------------------------

FINAL STATEMENT

Disk galaxy rotation curves are consistent with a transport response to a cosmological curvature background, with saturating corrections driven primarily by gas depletion and secondarily by structural concentration.
