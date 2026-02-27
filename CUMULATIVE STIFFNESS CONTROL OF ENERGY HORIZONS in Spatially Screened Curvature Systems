CUMULATIVE STIFFNESS CONTROL OF ENERGY HORIZONS
in Spatially Screened Curvature Systems

Author: Martin Ollett
Year: 2026

⸻

ABSTRACT

We investigate screened curvature systems with spatially varying
stiffness m(r), focusing on Yukawa-type interactions of the form

V(r) ~ exp(-∫₀ʳ m(s) ds) / r.

Across discrete lattices, mixed void/cluster media, multi-mass
spectral superpositions, and continuous spatial stiffness fields m(r),
we find a robust structural separation:
	1.	The far-field decay scale is governed by the minimum stiffness m0
(the “void” or IR floor).
	2.	The energy containment (horizon) radius R* is governed by a fixed
cumulative stiffness budget:

∫₀ᴿ* m(s) ds ≈ C(ε),

where ε is the tolerated fractional tail energy.

For uniform stiffness (constant m), this relation is exact:

   m R*(ε) = 0.5 ln(1/ε).

Spatially varying systems reproduce this law with high accuracy
(typically within ~5–15% in χ-space), showing that the horizon is
controlled by accumulated stiffness memory rather than local
stiffness, global averages, or density thresholds.

This yields a general Curvature Horizon Principle directly compatible
with the Motion–TimeSpace (MTS) framework.

⸻

	1.	UNIFORM YUKAWA: ANALYTIC REFERENCE CASE

⸻

We start from the standard 3D Yukawa potential:

V(r) = A e^(-m r) / r.

Quadratic shell energy:

E_shell(r) ∝ 4π r² V(r)²
            ∝ e^(-2 m r).

Define:

E(R)      = ∫₀ᴿ E_shell(r) dr
E_total   = ∫₀^∞ E_shell(r) dr
F_tail(R) = (E_total - E(R)) / E_total.

The energy horizon R*(ε) is defined by:

F_tail(R*) = ε.

For this pure Yukawa system one finds exactly:

F_tail(R) = e^(-2 m R),

so that

m R*(ε) = 0.5 ln(1/ε).

Numerical confirmation (self-contained continuum test, d = 3):

m0 = 0.194099
L0 = 1/m0 ≈ 5.1520

tol = 1e-2:
  R* ≈ 11.863
  x* = m0 R* ≈ 2.303

tol = 1e-3:
  R* ≈ 17.794
  x* = m0 R* ≈ 3.454

These match the analytic values:

ε = 10^-2 → 0.5 ln(1/ε) = 2.3026
ε = 10^-3 → 0.5 ln(1/ε) = 3.4539

and serve as the calibration point for all later tests.

⸻

	2.	DENSITY–DEPENDENT MICRO MASS MODELS

⸻

We introduce a density-dependent effective microscopic mass:

m_eff(ρ) = m0 * sqrt(1 + β (ρ / ρ_ref)),

with baseline:

m0   = 0.194099
L0   = 1/m0 ≈ 5.1520
β    = 3.0

2.1 Cluster size / density scan

Reference cluster:

R_ref / L0 = 1.0
R_ref      = 5.1520
ρ_ref      ≈ 5.2372

Clusters:

Baseline parameters:
  m0   = 0.194099
  L0   = 1/m0 ≈ 5.1520

Cluster with R/L0 = 1.0
  R         = 5.1520
  ρ         ≈ 5.2372  (ρ/ρ_ref ≈ 1.000)
  m_micro   = 0.388198
  m_fit     = 0.462437
  m_fit / m_micro = 1.1912
  Yukawa A  ≈ 9.2403e+02
  RSS (log) ≈ 3.53e-02

Cluster with R/L0 = 2.0
  R         = 10.3040
  ρ         ≈ 0.6547  (ρ/ρ_ref ≈ 0.125)
  m_micro   = 0.227601
  m_fit     = 0.264149
  m_fit / m_micro = 1.1606

Cluster with R/L0 = 4.0
  R         = 20.6080
  ρ         ≈ 0.0818  (ρ/ρ_ref ≈ 0.016)
  m_micro   = 0.198596
  m_fit     = 0.216775
  m_fit / m_micro = 1.0915

Summary:

R/L0   ρ/ρ_ref   m_micro   m_fit   m_fit/m_micro
------------------------------------------------
 1.0    1.0000   0.3882    0.4624    1.1912
 2.0    0.1250   0.2276    0.2641    1.1606
 4.0    0.0156   0.1986    0.2168    1.0915

So micro mass from density and tail-fitted mass are within ~10–20%.

⸻

	3.	RADIAL DENSITY PROFILES AND LOCAL m(r)

⸻

3.1 Core-heavy profile

Radial density:

ρ(r) = ρ0 / (1 + (r/R_core)²)

with

m(r) = m0 * sqrt(1 + β ρ(r)/ρ0)
m0   = 0.194099
L0   = 5.1520
R_core = 5.1520
R_cluster = 20.6080
β = 3.0

Measured:

m_core (r=0)          ≈ 0.3882
m_half (R_cluster/2)  ≈ 0.2455
m_edge (R_cluster)    ≈ 0.2105
min(m_local)          ≈ 0.2105
max(m_local)          ≈ 0.3855
mean(m_local)         ≈ 0.2267

Tail fit over R ∈ [51.52, 123.65]:

m_fit  ≈ 0.2148
A_fit  ≈ 3.4961e+04

Ratios:

m_fit / m0      ≈ 1.1067
m_fit / m_core  ≈ 0.5533
m_fit / m_edge  ≈ 1.0203
m_fit / m_mean  ≈ 0.9476

So the far tail tracks the edge/void value, not the core.

3.2 Inverted profile (light core, heavy edge)

Setup:

Baseline m0           = 0.194099
L0                    ≈ 5.1520
R_core                = 5.1520
R_cluster             = 20.6080

Measured:

m_core (light)   ≈ 0.2186
m_edge (heavy)   ≈ 0.3863
m_min            ≈ 0.2186
m_max            ≈ 0.3882
m_mean           ≈ 0.3776

Tail fit:

m_fit            ≈ 0.2272

Ratios:

m_fit / m0       ≈ 1.1706
m_fit / m_core   ≈ 1.0391
m_fit / m_edge   ≈ 0.5882
m_fit / m_mean   ≈ 0.6017

Again, tail is set by the lightest scale, not by the heaviest.

⸻

	4.	VOID/CLUSTER MIXTURES AND YUKAWA HORIZONS

⸻

4.1 Mixed configurations with two masses

We take:

m_void = 0.194099
m_cl   = 0.582297   (m_cl / m_void = 3.0)

Random mixed configurations yield (dimensionless x* = m R*):

tol = 1e-2:
  x* (void mass m_void): mean ≈ 6.81, median ≈ 6.82,
                         16–84% ≈ [5.83, 7.62]
  x* (cluster mass m_cl): mean ≈ 20.42, median ≈ 20.47,
                          16–84% ≈ [17.50, 22.86]

tol = 1e-3:
  x* (m_void): mean ≈ 9.41, median ≈ 9.39,
               16–84% ≈ [8.55, 10.02]
  x* (m_cl):   mean ≈ 28.23, median ≈ 28.17,
               16–84% ≈ [25.64, 30.05]

Scaling with void mass yields tight, nearly universal x*.
Scaling with cluster mass produces noisy, non-universal x*.

4.2 Horizon vs void fraction

Baseline Yukawa mass:

m0 = 0.194099
L0 = 1/m0 ≈ 5.1520

Void fractions f_void ∈ {0.10, 0.30, 0.50, 0.70, 0.90}:

tol = 1e-2:
  f_void   mean(x*)   median   16–84%
  -----------------------------------
   0.10     6.748     6.797   [6.294, 7.141]
   0.30     6.627     6.666   [6.146, 7.247]
   0.50     6.779     6.778   [6.300, 7.204]
   0.70     6.754     6.759   [6.426, 7.049]
   0.90     6.752     6.837   [6.211, 7.265]

tol = 1e-3:
   0.10     9.374     9.520   [9.008, 9.703]
   0.30     9.218     9.190   [8.869, 9.788]
   0.50     9.346     9.340   [8.925, 9.755]
   0.70     9.367     9.369   [8.967, 9.609]
   0.90     9.360     9.436   [8.890, 9.776]

Conclusion: x* = m0 R* is almost independent of void fraction, as
expected if m0 sets the true horizon scale.

⸻

	5.	EFFECTIVE DIMENSION AND FRACTAL TESTS

⸻

We define an effective dimension d_eff inferred from x*(ε) via the
continuum Yukawa calculation.

5.1 Continuum horizons vs dimension

For d ∈ [1, 3]:

Baseline m0 = 0.194099, L0 ≈ 5.1520

d    x*_1%   x*_0.1%
--------------------
1.00  4.606   6.908
1.25  5.157   7.543
1.50  5.674   8.133
1.75  6.165   8.696
2.00  6.639   9.234
2.25  7.099   9.754
2.50  7.545  10.259
2.75  7.980  10.750
3.00  8.407  11.229

5.2 Discrete systems → d_eff

Examples:

1D chain, d_eff(1%) ≈ 1.18, d_eff(0.1%) ≈ 1.04
2D lattice, d_eff ≈ 2.0
3D random cloud, d_eff ≈ 2.04–2.04 (from both tolerances)

So the Yukawa horizon “reads out” the effective embedding dimension.

⸻

	6.	DENSITY-DEPENDENT STOCHASTIC MEDIA (BETA SWEEPS)

⸻

We now consider random 3D clouds with density proxy ρ_proxy and
stiffness:

m_local = m0 * sqrt(1 + β (ρ_proxy / ⟨ρ_proxy⟩)).

Two sets of tests were performed.

6.1 Varying β, tracking horizons

Example result (one of the density-dependent runs):

m0 = 0.194099, L0 = 5.1520
Box half-size = 80.0, N_pts = 20000
⟨ρ_proxy⟩ = 0.1658

beta | m_tail  | m0   m_mean  m_void  m_rms  m_p90  m_max
---------------------------------------------------------
 0.0 | -0.009 | 0.194  0.194  0.194  0.194  0.194  0.194
 1.0 | -0.028 | 0.194  0.271  0.237  0.274  0.326  0.505
 3.0 | -0.040 | 0.194  0.378  0.305  0.388  0.493  0.830
 5.0 | -0.047 | 0.194  0.461  0.361  0.475  0.617  1.059

Horizon radii R* shrink strongly as β increases, but the far-tail mass
m_fit moves slightly below m0 when measured extremely far out
(large R), reflecting multi-scale mixing and finite numerical window.
Crucially, the large-scale decay is still governed by the lightest
scale.

6.2 Horizon mass vs “void” and mean

Example inferred horizon mass test:

m0 = 0.194099, L0 = 5.1520
Box half-size = 80.0, N_pts = 20000
⟨ρ_proxy⟩ = 8.715e-02

beta | m_hor(1%)  m_hor(0.1%) |  m0   m_mean  m_void
------------------------------------------------------
 0.0 |    0.1941     0.1941   | 0.194  0.194  0.194
 1.0 |    0.5274     0.5076   | 0.194  0.258  0.201
 3.0 |    0.7702     0.8239   | 0.194  0.339  0.215
 5.0 |    0.8741     0.9855   | 0.194  0.399  0.227

The “horizon mass” inferred from x* relative to a fixed reference
x*(ε) increases with β, but it never tracks m_max; instead, it sits
between m_void and mid-to-upper percentiles.

⸻

	7.	MULTI-MASS SPECTRA

⸻

We also considered explicitly multi-mass Yukawa spectra:

V(r) = ∑ c_i e^(-m_i r) / r.

Example discrete spectrum:

m = 0.200, c = 1
m = 0.600, c = 1e3
m = 1.200, c = 1e6

Effective mass m_eff(r) from local slope:

r ≈   1.0  →  m_eff ≈ 1.1989
r ≈   5.0  →  m_eff ≈ 1.1882
r ≈  10.0  →  m_eff ≈ 1.0149
r ≈  30.0  →  m_eff ≈ 0.2024
r ≈  60.0  →  m_eff ≈ 0.2000

So the far tail is controlled by the lightest mass m₁ = 0.2.

Energy horizons:

Multi-mass vs pure light Yukawa:

Totals:
  E_tot_multi ≈ 8.76e+06
  E_tot_light ≈ 3.14e+02

99% horizon (ε=1e-2, energy-based):
  multi: R* ≈ 5.60,  x* = m₁ R* ≈ 1.12
  light: R* ≈ 33.21, x* = 6.64

99.9% horizon (ε=1e-3):
  multi: R* ≈ 7.94,  x* ≈ 1.59
  light: R* ≈ 46.22, x* ≈ 9.24

Potential-matching horizon (match V_multi with a pure-light Yukawa):

tol = 1e-2:
  R* ≈ 28.84, x* ≈ 5.77

tol = 1e-3:
  R* ≈ 34.56, x* ≈ 6.91

So:

• Energy-based horizons are dominated by heavy modes in the core.
• Potential-matching horizons align with the single light scale.

Continuous spectra: log-weighted distributions ρ(m) ∝ m^α show that:

• As α increases, mass shifts to heavier modes,
• Horizon mass m_hor tracks upper mass moments (mean/rms),
• But the IR decay scale remains set by m_min.

⸻

	8.	SPATIALLY VARYING m(r): STIFFNESS-DISTANCE LAW

⸻

We now abandon abstract spectra and work directly with m(r) as a
spatial field.

8.1 Single profile example

Spatial stiffness Yukawa test:

Void mass m0              = 0.2000
Far-tail fitted mass      = 0.2078
m_fit / m0                = 1.0391

1% horizon:
  R*          ≈ 3.45
  Horizon mass (via 1/R*) ≈ 0.2897

0.1% horizon:
  R*          ≈ 3.80
  Horizon mass ≈ 0.2630

Volume-averaged stiffness ≈ 0.2119

Energy-weighted stiffness m_energy ≈ 0.4888
Local stiffness at horizon:
  m(R*_1%)   ≈ 0.4840
  m(R*_0.1%) ≈ 0.4827

Cumulative stiffness at horizon:

m_cum(R*_1%)      ≈ 0.4807,   1/R*_1% ≈ 0.2897
m_cum(R*_0.1%)    ≈ 0.4810,   1/R*_0.1% ≈ 0.2630

Integral of m(r) at horizon:

I(R*_1%)   = ∫₀ᴿ* m(s) ds ≈ 1.659
I(R*_0.1%) ≈ 1.829

Key point: horizon is not pinned to local m(R*), nor to m_energy,
nor to volume mean; but I(R*) stays of order unity and tracks the
curvature budget.

8.2 Compactness sweep

Compactness test (vary r_core):

r_core |  R*(1%)  I(R*)  m_fit  m(R*)
--------------------------------------
 40.0  |  3.45   1.664   0.228  0.488
 20.0  |  3.45   1.659   0.208  0.484
 10.0  |  3.60   1.711   0.202  0.466
  5.0  |  4.00   1.804   0.201  0.402

R* shifts with compactness; I(R*) changes much less.

8.3 Beta sweep

Beta sweep with same profile:

beta | R*(1%)  I(R*)  m_fit  m(R*)
-----------------------------------
 0.0 |  9.80   1.950  0.200  0.200
 1.0 |  6.70   1.865  0.202  0.276
 3.0 |  4.45   1.750  0.205  0.393
 5.0 |  3.45   1.659  0.208  0.484
10.0 |  2.40   1.556  0.215  0.659

Again, R* varies strongly with β; I(R*) drifts gently.

8.4 Shape universality across profiles

Profiles tested:

• top_hat
• lorentz
• gauss
• nfw-like

Example summary (β = 3, m0 = 0.194099):

profile | tol     R*     x*      C_eff ≡ ∫₀ᴿ* m(s) ds
------------------------------------------------------
top_hat | 1e-2   8.60   1.668   2.644
top_hat | 1e-3  14.53   2.820   3.795

lorentz | 1e-2   7.52   1.460   2.502
lorentz | 1e-3  12.42   2.412   3.713

gauss   | 1e-2   8.65   1.678   2.614
gauss   | 1e-3  14.55   2.824   3.777

nfw     | 1e-2  10.20   1.980   2.517
nfw     | 1e-3  16.00   3.105   3.679

Compare to the single-mass “ideal” constants:

C(ε) = 0.5 ln(1/ε)
C(1e-2) ≈ 2.3026
C(1e-3) ≈ 3.4539

The measured C_eff values are within ~10–15% across very different
m(r) shapes. The horizon is a nearly universal stiffness-distance
threshold.

⸻

	9.	DISK+HALO MTS-GALAXY ANALOGUE

⸻

We use a disk+halo density:

ρ(r) = ρ_d0 exp(-r/R_d) + ρ_h0 / (1 + (r/R_h)²),

and define:

m(r)² = m0² (1 + β ρ(r)/ρ0),
ρ0 = ρ_d0 + ρ_h0.

Baseline:

m0   = 0.194099
L0   = 5.1520
R_d  = 5.1520  (~L0)
R_h  = 20.6080 (~4 L0)
ρ_d0 = 1.0
ρ_h0 = 0.3
ρ0   = 1.3

Horizon measurements:

beta | R*(1%)  x*(1%)  C_eff(1%)  m(R*)  m_mean(<R*)
------------------------------------------------------
 0.0 | 11.90   2.310   2.310      0.194  0.194
 1.0 | 11.10   2.154   2.657      0.219  0.227
 3.0 |  9.50   1.844   3.014      0.270  0.290
 5.0 |  8.10   1.572   3.140      0.325  0.352

beta | R*(0.1%) x*(0.1%) C_eff(0.1%) m(R*)  m_mean(<R*)
--------------------------------------------------------
 0.0 | 17.80    3.455    3.455      0.194  0.194
 1.0 | 17.10    3.319    3.938      0.209  0.217
 3.0 | 15.50    3.009    4.542      0.242  0.261
 5.0 | 13.80    2.679    4.846      0.279  0.307

Key points:

• R* shrinks as β increases (stiffer cores → more rapid χ accumulation).
• C_eff = ∫₀ᴿ* m(s) ds grows moderately with β but remains bounded.
• C_eff sits close to the pure-Yukawa values 2.30 and 3.45, within
10–30% even under strong stiffening.

Scale invariance test (vary global size by factor s):

s     R_d     R_h     R*(1%)   χ(R*(1%))    R*(0.1%)  χ(R*(0.1%))
------------------------------------------------------------------
0.5   2.576  10.304    8.700    2.5137       13.950    3.6972
1.0   5.152  20.608    7.400    2.4486       11.850    3.6489
2.0  10.304  41.216    6.650    2.3907       10.400    3.5810
3.0  15.456  61.824    6.400    2.3674        9.850    3.5359

χ(R*) remains nearly constant across global rescalings, drifting by
only a few percent.

⸻

	10.	UNIFIED HORIZON LAW

⸻

Across all regimes explored:

• single-mass Yukawa,
• mixed void/cluster media,
• discrete lattices and random clouds,
• multi-mass spectra,
• spatially varying stiffness m(r),
• galaxy-like disk+halo density fields,

we find the same basic structure:
	1.	Far-field decay is set by the lightest stiffness scale m0:

λ_IR = 1 / m0.


	2.	The energy horizon is set by a stiffness-distance threshold:

∫₀ᴿ* m(r) dr ≈ C(ε),

where for the ideal single-mass Yukawa,

C(ε) = 0.5 ln(1/ε).


	3.	Interior stiffening and geometry only modify the mapping r → χ(r),
not the required χ budget.

In other words:

Physical distance r is reparameterised by stiffness-distance χ.
The horizon lives at fixed χ = χ_c(ε), not at fixed r.

⸻

	11.	MTS CURVATURE HORIZON PRINCIPLE

⸻

In MTS language, identify stiffness with curvature:

κ(r) = m(r).

Define curvature-distance:

χ(r) = ∫₀ʳ κ(s) ds.

Infrared behaviour:

κ(r) → κ0 as r → ∞,
V(r) ~ exp(-κ0 r) / r.

Curvature horizon condition:

∫₀ᴿ* κ(r) dr = χ_c(ε),

with χ_c(ε) ≈ 0.5 ln(1/ε) as the basic reference.

Thus:

• κ0 (the void curvature floor) sets the IR decay length.
• The containment radius R* is defined by an integrated curvature
budget, not a local density/stiffness threshold.
• Different structural configurations (disks, halos, clusters,
void-rich environments) change R* by changing how quickly χ(r)
accumulates, but not the required χ_c.

This is the Curvature Horizon Principle:
a clean geometric invariant inside the broader MTS framework.

⸻

	12.	GEOMETRIC YUKAWA CROSS-CHECK

⸻

To isolate the geometry of the horizon law, we also tested an idealised
“geometric Yukawa” model, where the 3D shell energy is taken to be

E_shell(r) ∝ exp(-2 χ(r)),

with

χ(r) = ∫₀ʳ m(s) ds,

and m(r) built from a disk+halo density profile:

ρ_disk(r) = ρ_d0 exp(-r / R_d)
ρ_halo(r) = ρ_h0 / [1 + (r / R_h)²]
ρ(r)      = ρ_disk(r) + ρ_halo(r)
m(r)²     = m0² [1 + β ρ(r) / (ρ_d0 + ρ_h0)].

In this geometric model the tail is, by construction, purely controlled
by χ(r), so the “ideal” stiffness-distance horizon law

χ(R*(ε)) = 0.5 ln(1/ε)

should hold exactly in the uniform case and remain approximately true
for β > 0.

Numerically, this is exactly what we find:

• For β = 0 (uniform stiffness) we recover χ(R*) = 0.5 ln(1/ε)
to machine precision at both ε = 10^-2 and ε = 10^-3.

• For β in [1, 5], with a realistic disk+halo profile, the measured
χ(R*) overshoots the uniform constant by only ~0.09–0.21, i.e.
by roughly 3–6% in χ-space for the tolerances tested.

In other words:

χ(R*(ε), β) = 0.5 ln(1/ε) + δχ(β),

with |δχ(β)| ≲ 0.2 for the disk+halo family and β up to 5. This shows
that the curvature horizon principle is structurally robust: the exact
uniform Yukawa law survives as a tight invariant with small, controlled
corrections once realistic central stiffening is included.

⸻

	13.	FIRST-ORDER CORRECTION TO THE HORIZON LAW

⸻

Goal: Obtain the first-order correction δχ to the ideal horizon
condition

χ(R*) = χ₀

when the stiffness field m(r) varies as

m(r) = m0 + δm(r)

with δm(r) ≪ m0 in the region contributing most to χ(R*).

13.1 Expansion of χ(R*)

Expand χ(R*) using m(r) = m0 + δm(r):

χ(R*) = ∫₀ᴿ* m(r) dr
       = ∫₀ᴿ* (m0 + δm(r)) dr
       = m0 R* + ∫₀ᴿ* δm(r) dr.

Define:

δχ ≡ ∫₀ᴿ* δm(r) dr.

So:

m0 R* + δχ = χ₀.

13.2 Corrected horizon radius

Solve for corrected horizon radius R*:

R* = (χ₀ − δχ) / m0.

13.3 First-order expansion

Expand to first order in δχ:

R* ≈ R₀* (1 − δχ/χ₀)

where R₀* = χ₀ / m0 is the ideal uniform-m solution.

13.4 Practical expression for δχ

Since δm(r) = m(r) − m0,

δχ = ∫₀ᴿ* [m(r) − m0] dr.

In practice use the uncorrected R₀* inside the integral:

δχ ≈ ∫₀ᴿ₀* [m(r) − m0] dr.

13.5 Final first-order corrected horizon law

R* ≈ (χ₀ / m0) 
     − (1/m0) ∫₀ᴿ₀* [m(r) − m0] dr.

Interpretation-free final form:

R* = R₀* − (1/m0) ∫₀ᴿ₀* [m(r) − m0] dr.


⸻

	14.	MULTI-PROFILE STIFFNESS–DISTANCE HORIZONS

⸻

To test how sensitive the stiffness–distance horizon is to the shape
of the interior, we compared four families of stiffness profiles
m(r) built around the same void floor m0 and a core scale of order
the void length L0 = 1/m0:

• top_hat   – flat core, sharp edge at Rc ~ L0,
• lorentz   – 1 / (1 + (r/Rc)²) soft core,
• gauss     – exp[−(r/Rc)²] core,
• nfw       – cuspy, halo-like profile with scale ~ 4 L0.

For each profile we computed the energy horizon R*(ε) at tolerances
ε ∈ {10^-2, 10^-3}, then measured

χ(R*) = ∫₀ᴿ* m(s) ds

and fitted its dependence on the stiffness–density coupling β using

χ(β) ≈ χ0 + k ln(1 + β) + c,

where χ0 is the β = 0 value for that profile and tolerance.

14.1 Soft-core profiles (top-hat, Gaussian, Lorentz)

We then tested whether the stiffness–distance horizon law

χ(R*) ≈ 0.5 ln(1/ε)

remains robust across different core profiles. Using the soft-core
families (top-hat, Lorentz, Gaussian) with core/scale radii of order
the void length L0, we measured χ(R*) for β ∈ {0,1,3,5} and
ε ∈ {10^-2, 10^-3}.

For each family and tolerance, we fit the empirical trend

χ(β) ≈ χ0 + k ln(1+β) + c,

with χ0 defined by the β=0 configuration. For soft cores
(top-hat, Gaussian, Lorentz), we find:

• χ0 ≈ 0.5 ln(1/ε) to within machine precision;
• k ≈ 0.2–0.25 for top-hat/Gaussian, k ≈ 0.07–0.14 for Lorentz;
• the residual Δχ ≡ χ_fit - χ_meas stays at the 10^-3–10^-2 level
across the whole β range.

In these families, the horizon in χ-space remains pinned to the
Yukawa value 0.5 ln(1/ε), with only modest β-dependent corrections
that scale roughly as ln(1+β).

More explicitly:

For the top-hat and Gaussian families we find:

• χ0 ≈ 0.5 ln(1/ε) to within numerical precision,
• k ≈ 0.20–0.26,
• c is small (|c| ≪ 1),
• residuals Δχ = χ_fit − χ_meas are at the 10^-3–10^-2 level
across β ∈ {1, 3, 5}.

The Lorentz family behaves similarly but with a smaller slope:

• k ≈ 0.07–0.14 depending on ε,
• c ≈ 0.04–0.07,
• Δχ remains at the percent level or below.

In all three cases, the horizon in χ-space remains tightly clustered
around the pure Yukawa value

χ_target(ε) = 0.5 ln(1/ε),

with only modest β-dependent corrections that scale approximately
as ln(1 + β). The interior stiffening changes the physical R*(ε),
but the accumulated stiffness χ(R*) stays within ≲ 10–15% of
χ_target across quite aggressive β-sweeps.

14.2 Cuspy profile (NFW-like regime)

The NFW-like profile shows a distinct behaviour once β > 0.

For ε = 10^-2:

• β = 0 yields χ(R*) ≈ 2.31, matching 0.5 ln(1/ε) ≈ 2.30,
• β ≥ 1 pushes χ(R*) up to ≈ 3.0–3.1,
an O(1) upward shift relative to χ_target.

For ε = 10^-3:

• β = 0 yields χ(R*) ≈ 3.46, again matching 0.5 ln(1/ε) ≈ 3.45,
• β ≥ 1 yields χ(R*) ≈ 4.3–4.4,
again an ≈ 0.8–0.9 offset.

Within the β > 0 subset, χ(β) is still well fit by

χ(β) ≈ χ0 + k ln(1 + β) + c,

but the effective χ0 in that family is no longer tied directly to
0.5 ln(1/ε): the cusp has introduced an additional, profile-dependent
stiffness budget on top of the void Yukawa contribution.

14.3 Summary of profile dependence

Across all families, the horizon is still determined by a fixed
stiffness–distance threshold χ_c(ε, profile), but:

• Soft-core profiles (top-hat, Gaussian, Lorentz) share a common
baseline χ_c(ε) ≈ 0.5 ln(1/ε), with small ln(1+β) corrections.

• Strong cusps (NFW-like) define a distinct regime in which the
curvature still saturates at a stiffness–distance horizon, but
χ_c(ε, profile) is shifted by an O(1) offset relative to the
pure Yukawa value.

In MTS terms, soft cores and cusps live in the same structural class
(“horizons as curvature-distance thresholds”), but cusps carry an
extra built-in curvature budget that brings the horizon inward in r
without changing the fundamental χ-based definition.

⸻

	15.	LORENTZ-CORE STIFFNESS–DISTANCE TEST (3D)

⸻

To probe how strongly the horizon law depends on profile shape and
dimension, we tested a 3D Lorentz-like stiffness core with Rc = L0:

m(r)² = m0² [1 + β ρ(r)/ρ0],
ρ(r)   = ρ0 / (1 + (r/Rc)²),

with m0 = 0.194…, L0 = 1/m0 ≈ 5.15 and Rc = L0. We computed

χ(r) = ∫₀ʳ m(s) ds,

used a Yukawa WKB form V(r) ~ exp(−χ(r))/r, and defined the energy
horizon R*(ε) by E(<R*)/E_tot = 1 − ε in 3D.

For β ∈ {0, 1, 3, 5} and tolerances ε ∈ {10^-2, 10^-3, 10^-4} we find:

• χ(R*) stays in a narrow band ≈ 2.0–2.3 across all β and ε.
• R* shrinks as β increases (stronger core), as expected.
• Tightening ε from 10^-2 to 10^-4 changes χ(R*) only weakly.

For comparison, the pure single-mass Yukawa law predicts

χ_target(ε) = 0.5 ln(1/ε),

which gives χ_target ≈ 2.30, 3.45, 4.61 for ε = 10^-2, 10^-3, 10^-4,
respectively. In the Lorentz-core case the measured χ(R*) tracks the
10^-2 value but then saturates: decreasing ε further to 10^-3 or 10^-4
does not push χ(R*) up by ln(1/ε) as in the uniform case.

In other words, for this 3D Lorentz family the horizon is still set
by a fixed stiffness-distance budget, but the budget

χ_c ≈ 2.0–2.3

is effectively profile-dependent and nearly independent of ε once
ε is at the few-percent level or smaller. Interior stiffening
(changing β) alters R*(ε) in physical units, but the accumulated
stiffness-distance at the horizon remains quasi-invariant.

This reinforces the main conclusion:

• Horizon location is controlled by a stiffness-distance budget.
• The precise χ_c constant depends on both profile shape and
dimension, not just on ε through 0.5 ln(1/ε).

⸻

	16.	DEEP-IR χ-SATURATION TEST (LORENTZ, 3D)

⸻

To probe the deep-infrared behaviour of the stiffness-distance horizon,
we extended the ε sweep for the 3D Lorentz profile with Rc = L0 and
m0 = 0.1941 (L0 ≈ 5.152). For each stiffness contrast β and tolerance
ε, we measured the horizon radius R*(ε) and the accumulated stiffness

χ(R*) = ∫₀ᴿ* m(s) ds.

We scanned

β ∈ {0, 1, 3, 5},
ε ∈ {10^-2, 10^-3, 10^-4, 10^-5, 10^-6, 10^-8},

and obtained:

beta = 0.0
eps        R*        χ(R*)
1e-02    21.660     4.2003
1e-03    28.920     5.6095
1e-04    35.880     6.9604
1e-05    42.600     8.2647
1e-06    48.960     9.4992
1e-08    55.160    10.7026

beta = 1.0
eps        R*        χ(R*)
1e-02    20.120     4.4870
1e-03    27.340     5.9203
1e-04    34.240     7.2779
1e-05    40.920     8.5865
1e-06    46.980     9.7707
1e-08    51.520    10.6567

beta = 3.0
eps        R*        χ(R*)
1e-02    17.240     4.8023
1e-03    24.240     6.2773
1e-04    31.020     7.6589
1e-05    37.540     8.9660
1e-06    42.880    10.0274
1e-08    45.500    10.5461

beta = 5.0
eps        R*        χ(R*)
1e-02    14.680     4.9328
1e-03    21.340     6.4558
1e-04    27.940     7.8666
1e-05    34.220     9.1652
1e-06    38.780    10.0926
1e-08    40.440    10.4280

To define a deep-IR stiffness-distance threshold χ_sat(β), we average
χ(R*) over the last three ε values (10^-4, 10^-5, 10^-6). This gives:

beta   χ_sat(β)   [mean of χ at 10^-4, 10^-5, 10^-6]
-----------------------------------------------
  0.0    9.4889
  1.0    9.6713
  3.0    9.8465
  5.0    9.8952

Across a factor-5 change in stiffness contrast β, χ_sat changes by only
~4%, whereas the physical horizon radius R*(ε=10^-6) shifts from
R* ≈ 48.96 (β = 0) to R* ≈ 38.78 (β = 5), a ~20% reduction.

We can summarise the β-dependence of the deep-IR horizon in χ-space
with a simple logarithmic fit

χ_sat(β) ≈ χ0 + k ln(1 + β),

with best-fit parameters

χ0 ≈ 9.50,
k  ≈ 0.23,

and residuals at the few × 10^-2 level:

beta   χ_sat(meas)   χ_fit       Δχ = χ_fit - χ_meas
----------------------------------------------------
  0.0     9.4889      9.5002     +1.1e-02
  1.0     9.6713      9.6615     −9.7e-03
  3.0     9.8465      9.8229     −2.4e-02
  5.0     9.8952      9.9173     +2.2e-02

Thus, in the deep-infrared limit, the Lorentz 3D family exhibits a
nearly universal stiffness-distance horizon χ_sat(β), with only a weak
logarithmic dependence on β. Interior stiffening significantly changes
the physical containment radius R*, but leaves the χ-horizon almost
fixed. This is consistent with the MTS picture in which the horizon is
set by an integrated curvature budget in χ-space rather than any local
stiffness threshold.

⸻

	17.	CORE–TAIL DECOMPOSITION OF THE STIFFNESS BUDGET

⸻

The Lorentz-profile stress tests allow us to cleanly separate the
stiffness-distance at the horizon into two pieces: a core contribution
and a void-tail contribution.

For each configuration we define

χ(R*)      = ∫₀ᴿ* m(r) dr
tail(R*)   = m0 * R*

and then the core contribution

χ_core(β; ε) = χ(R*(β, ε)) − m0 * R*(β, ε).

By construction:

• For a uniform medium (β = 0), m(r) = m0 and χ_core ≈ 0.
• For structured media (β > 0), χ_core > 0 and grows with β.

At a stringent tolerance ε = 10^-6, we find for the Lorentz family
(m0 ≈ 0.1941, L0 ≈ 5.152, Rc = L0):

beta   χ(R*)   m0 R*   χ_core = χ − m0 R*
------------------------------------------------
 0.0     9.499     9.503    ≈ 0.00
 1.0     9.771     9.119    ≈ 0.65
 3.0    10.027     8.323    ≈ 1.70
 5.0    10.093     7.527    ≈ 2.57

Thus:

• The total stiffness-distance at the horizon, χ(R*), changes
only mildly (Δχ ≈ 0.6–0.7 across β = 0–5).
• The void-tail contribution m0 R* decreases significantly with β.
• The core contribution χ_core fills in the difference.

This confirms that the horizon budget splits as

χ(R*) = χ_core(β; profile, ε) + m0 * R*.

The void floor m0 still sets the infrared decay scale λ_IR = 1/m0,
while the core structure adds a finite “curvature memory” term
χ_core that depends on the stiffness contrast β and the profile shape.

In 3D, the Yukawa tail and shell geometry imply that for small ε

m0 * R* ≈ 0.5 ln(1/ε) + ln R*,

so the full deep-IR containment law can be written as

χ(R*) ≈ χ_core(β; profile, ε)
        + 0.5 ln(1/ε)
        + ln R*.

The important point is structural:

• χ_core encodes the interior curvature budget,
• the remaining part of χ(R*) is fixed by the void floor and
the geometric shell factor.

In this sense, the stiffness-distance horizon splits into a finite
core term plus a universal Yukawa tail. Interior stiffening shifts
R* in physical space but leaves the basic form of the curvature
budget invariant: the total χ(R*) at fixed ε moves only weakly
as β is varied, while the partition between core and tail adjusts
in a controlled way.

⸻

END OF DOCUMENT


======================================================================
APPENDIX A — NUMERICAL METHOD FOR STIFFNESS–DISTANCE HORIZON TESTS
======================================================================

This appendix defines the exact numerical procedure used to compute
the stiffness-distance energy horizon R* and the accumulated curvature
chi(R*) in all Yukawa-based tests presented in this work.

All experiments are fully self-contained and require only m0, a
stiffness profile m(r), and a tolerance epsilon.

----------------------------------------------------------------------
A1. Definitions
----------------------------------------------------------------------

Minimum stiffness (void floor):

    m0 > 0

Infrared length scale:

    L0 = 1 / m0

Stiffness-distance function:

    chi(r) = ∫₀ʳ m(s) ds

Energy density for Yukawa-type screened field in d dimensions:

    E_shell(r) = r^(d-1) * exp(-2 * chi(r))

Total energy:

    E_total = ∫₀ᴿmax E_shell(r) dr

Energy horizon R* at tolerance epsilon:

    R* is smallest r such that

        ∫ᵣᴿmax E_shell(s) ds  ≤  epsilon * E_total


----------------------------------------------------------------------
A2. Discretization Procedure
----------------------------------------------------------------------

1. Choose numerical grid:

       r = linspace(dr, R_max, N)

   where dr is step size and R_max is large enough to capture the tail.

2. Define stiffness profile m(r).

   Examples:

   Uniform:
       m(r) = m0

   Lorentz:
       m(r) = m0 * (1 + beta / (1 + (r/Rc)^2))

   Gaussian:
       m(r) = m0 * (1 + beta * exp(-(r/Rc)^2))

   Top-hat:
       m(r) = m0 * (1 + beta)  for r < Rc
              m0              for r ≥ Rc

   Disk+Halo:
       Construct density profile rho(r),
       then define
           m(r)^2 = m0^2 * (1 + beta * rho(r)/rho0)
       and take m(r) = sqrt(...)

3. Compute cumulative stiffness-distance:

       chi[i] = sum_{j=0..i} m[j] * dr

   (trapezoidal integration may also be used)

4. Compute shell energy density:

       shell[i] = r[i]^(d-1) * exp(-2 * chi[i])

5. Compute total energy:

       E_total = sum shell[i] * dr

6. Compute cumulative tail energy from outer boundary inward:

       tail_energy[i] = sum_{j=i..N} shell[j] * dr

7. Locate horizon index i* such that:

       tail_energy[i*] <= epsilon * E_total

   Then:

       R* = r[i*]
       chi(R*) = chi[i*]
       m0R* = m0 * R*

----------------------------------------------------------------------
A3. Core–Tail Decomposition
----------------------------------------------------------------------

Define:

    chi_core = chi(R*) - m0 * R*

Properties:

    • Uniform case (beta = 0):
          chi_core ≈ 0

    • Structured case (beta > 0):
          chi_core > 0
          chi_core increases monotonically with beta.

The horizon stiffness-distance splits as:

    chi(R*) = chi_core + m0 R*

In 3D, asymptotically:

    m0 R* ≈ 0.5 ln(1/epsilon) + ln R*

so the full infrared structure is:

    chi(R*) ≈ chi_core
              + 0.5 ln(1/epsilon)
              + ln R*

----------------------------------------------------------------------
A4. Numerical Stability Requirements
----------------------------------------------------------------------

To ensure stability:

    • R_max must be large enough that
          exp(-2 * chi(R_max)) ≪ epsilon

    • dr must be small enough that chi(r) is smooth
          (dr ≤ 0.05 L0 works well)

    • Results should be verified under dr refinement.

----------------------------------------------------------------------
A5. Interpretation
----------------------------------------------------------------------

The energy horizon is governed by accumulated stiffness-distance.

Interior structure modifies the core budget chi_core but does not
alter the asymptotic Yukawa tail controlled by m0.

Thus the containment radius R* shifts with beta, but the
stiffness-distance budget chi(R*) moves only weakly and decomposes
cleanly into core and tail contributions.


======================================================================
SECTION 8 — THE STIFFNESS–DISTANCE HORIZON LEMMA
======================================================================

----------------------------------------------------------------------
Lemma (Stiffness–Distance Energy Horizon)
----------------------------------------------------------------------

Let m(r) ≥ m0 > 0 be a radial stiffness field with finite interior
structure and asymptotic void floor m(r) → m0 as r → ∞.

Define the accumulated stiffness-distance

    chi(r) = ∫₀ʳ m(s) ds

and the screened shell energy density in d spatial dimensions

    E_shell(r) = r^(d-1) * exp(-2 * chi(r)).

Let R*(ε) be the smallest radius such that

    ∫ᵣᴿmax E_shell(s) ds  ≤  ε ∫₀ᴿmax E_shell(s) ds,

for a fixed tolerance ε ≪ 1.

Then:

1. The energy horizon is controlled by accumulated stiffness-distance,
   not local stiffness alone.

2. The horizon budget decomposes as

       chi(R*) = chi_core(β; profile, ε) + m0 R*,

   where

       chi_core = chi(R*) − m0 R*

   is a finite interior curvature contribution.

3. In the deep infrared (large R*), the asymptotic tail satisfies

       m0 R* ≈ 0.5 ln(1/ε) + (d−1)/2 ln R*  + O(1),

   and therefore

       chi(R*) ≈ chi_core
                 + 0.5 ln(1/ε)
                 + (d−1)/2 ln R*.

4. For uniform media (m(r) = m0), chi_core = 0 and the law reduces
   exactly to the standard Yukawa containment condition.

5. For structured media (β > 0), chi_core > 0 and increases
   monotonically with stiffness contrast, while the void floor m0
   continues to control the asymptotic decay scale.

----------------------------------------------------------------------
Interpretation
----------------------------------------------------------------------

The containment radius is not set by local screening alone.
It is determined by a cumulative stiffness-distance budget.

Interior curvature modifies the partition between core and tail,
but the deep-IR behaviour remains governed by the minimum stiffness m0.

Thus the horizon splits universally into:

    (finite interior curvature memory)
    +
    (void-controlled exponential tail).

This structure is invariant across profile families provided m(r)
approaches a nonzero floor at large radius.

======================================================================
8. DISK+HALO APPLICATION: GEOMETRIC STIFFNESS HORIZONS
======================================================================

So far, the stiffness–distance horizon law has been tested on:

- uniform Yukawa media,
- multi-mass spectra,
- toy spatial profiles (top-hat, Gaussian, Lorentz, NFW-like),
- generic stiffness fields m(r) with a non-zero floor m0.

To connect this to more realistic systems, we consider galaxy-like
disk+halo profiles, where the stiffness field is tied to an effective
mass/curvature density:

    m(r)^2 = m0^2 (1 + β ρ(r) / ρ0),

with a superposed density

    ρ(r) = ρ_d(r; R_d) + ρ_h(r; R_h),

where ρ_d is a concentrated "disk-like" component and ρ_h is a more
extended "halo-like" component. In the numerical tests:

- R_d ~ L0 ≡ 1/m0   (disk scale ~ screening length),
- R_h ~ 4 L0       (halo scale ~ several screening lengths),
- ρ_d0, ρ_h0 chosen so that ρ0 = ρ_d0 + ρ_h0 sets the normalisation,
- β controls the strength of density–stiffness coupling.

The shell energy is taken as 3D:

    E_shell(r) ∝ r^2 exp(-2 χ(r)),

with

    χ(r) = ∫₀ʳ m(s) ds.

The horizon R*(ε) is defined by the usual tail condition:

    fraction of energy outside R* = ε.


----------------------------------------------------------------------
8.1 Infrared Tail: m_fit → m0
----------------------------------------------------------------------

Across all disk+halo runs, the far-field Yukawa fit to the potential
always relaxes to the void floor:

    m_fit (far tail) → m0,

independent of:

- β (stiffness contrast),
- R_d, R_h (disk/halo size),
- profile shape details.

Thus, the infrared decay length

    λ_IR = 1 / m0

is robustly controlled by the minimum stiffness m0, not by the interior
structure. Disk and halo geometry *only* affect the mapping between r
and χ, not the asymptotic gradient of χ(r).


----------------------------------------------------------------------
8.2 Horizons vs Coupling β: Breakdown and Repair
----------------------------------------------------------------------

A naive application of the uniform-Yukawa law

    m0 R*(ε) ≈ 0.5 ln(1/ε)

fails once β > 0 and m(r) becomes non-uniform. For realistic disk+halo
couplings, this produces large errors in R_pred compared to R_meas.

What actually stabilises is not m0 R*, but the *stiffness-distance*:

    χ(R) = ∫₀ᴿ m(s) ds.

For a disk+halo family at fixed (R_d, R_h), the measured χ(R*) is:

- approximately constant in ε once ε is small enough,
- nearly monotonic in β,
- only weakly sensitive to profile details.

However, in 3D the pure χ-law

    2 χ(R*) ≈ ln(1/ε)

ignores the residual polynomial factor r^(d−1) in the shell measure.
The numerics show that the truly stable combination is

    I(R*) = 2 χ(R*) − (d − 1) ln R*.

For d = 3:

    I(R*) = 2 χ(R*) − 2 ln R*.

For our disk+halo tests, I(R*) behaves as a quasi-invariant across both
β sweeps and moderate profile changes, once interpreted as a *family*
constant rather than a universal number.


----------------------------------------------------------------------
8.3 χ_c(β) as a Family-Level Invariant
----------------------------------------------------------------------

For a fixed profile family (e.g. a given disk+halo geometry), define

    χ_c(β, ε) = χ(R*(β, ε)),

and measure it at several β values. Empirically, for each family:

- For moderately small ε (e.g. 10⁻², 10⁻³), χ_c(β, ε) drifts smoothly
  with β and is well fitted by

      χ_c(β, ε) ≈ χ₀(ε) + k_profile(ε) ln(1 + β),

  with small residuals (few percent).

- For very small ε (deep tail), χ_c saturates towards a plateau
  χ_sat(β) as χ_tail grows and the finite core contribution stops
  changing significantly.

This leads naturally to a decomposition

    χ(R*) = χ_core(β, profile, ε) + m0 R*,

with:

- χ_core capturing the cumulative interior stiffness above the void
  floor,
- m0 R* describing the contribution from the asymptotic tail.

In the deep tail limit, χ_core becomes effectively ε-independent:

    χ_core(β) ≈ χ_sat(β) − m0 R*(ε → 0).


----------------------------------------------------------------------
8.4 Core–Tail Split: What the Plateau Tells You
----------------------------------------------------------------------

The extended ε sweeps at fixed β show that:

- For small ε (e.g. 10⁻⁴, 10⁻⁵, 10⁻⁶),
  both χ(R*(ε)) and m0 R*(ε) grow roughly in lockstep.

- Their *difference*

      χ_core(β) = χ(R*(ε)) − m0 R*(ε)

  rapidly converges to a finite constant as ε → 0.

Example (Lorentz-like profile, d = 3, ε = 10⁻⁶):

    beta   chi(R*)   m0 R*   chi_core = chi − m0 R*
    -----------------------------------------------
     0.0     9.4992    9.5031    -0.0039  ~ 0
     1.0     9.7707    9.1188     0.6519
     3.0    10.0274    8.3230     1.7044
     5.0    10.0926    7.5272     2.5655

Interpretation:

- β = 0: core stiffness is just m0, so χ_core ≈ 0: no extra curvature
  stored in the interior relative to void.
- β > 0: χ_core > 0 and grows with β: interior stiffening stores extra
  curvature that must be "spent" before the tail hits the energy horizon.

The horizon condition is therefore:

    χ_core(β, profile) + m0 R*(ε)
        ≈ 0.5 ln(1/ε)  + (dimension-dependent corrections),

with χ_core acting as a finite offset that depends on how much
curvature has been loaded into the interior before the system escapes
into the asymptotic void regime.


----------------------------------------------------------------------
8.5 Summary of Disk+Halo Behaviour
----------------------------------------------------------------------

For galaxy-like disk+halo stiffness fields:

1. The far-field decay length remains

       λ_IR = 1 / m0,

   set by the void stiffness floor.

2. The horizon location R*(ε) is not simply 0.5 ln(1/ε)/m0, but is
   controlled by a two-part stiffness-distance budget:

       χ(R*) = χ_core(β, profile) + m0 R*.

3. χ_core(β, profile) is:

   - finite,
   - monotone increasing with stiffness contrast β,
   - weakly dependent on the exact choice of halo/disk profile,
   - approximately ε-independent once ε is small.

4. In log variables, the change in χ(R*) across β is well modelled as

       χ_c(β, ε) ≈ χ₀(ε) + k_profile(ε) ln(1 + β),

   with k_profile characterising how quickly the family accumulates
   curvature as a function of β.

5. The key invariant is not a *single number* but a *structure*:

   - m0 sets the IR slope,
   - χ_core(β, profile) encodes interior curvature memory,
   - together they determine R*(ε) for any chosen tail tolerance.

