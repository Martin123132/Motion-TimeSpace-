
⸻

MTS-Gradient Cosmology

Benchmark Tests Against Standard Late-Time Expansion Probes

Author: Martin Ollett
Year: 2026

⸻

Abstract

We investigate the observational behaviour of the MTS-Gradient cosmological background by comparing it with the standard ΛCDM model across a set of commonly used late-time probes. The analysis uses Pantheon+ Type Ia supernovae, DESI DR1 baryon acoustic oscillation measurements, cosmic chronometer expansion-rate data, and large-scale structure growth observations.

The MTS-Gradient background modifies the matter contribution to the expansion history through a redshift-dependent gradient function while retaining a spatially flat geometry. Using identical datasets and likelihood constructions for both models, we evaluate the resulting expansion histories, distance measures, and growth predictions.

Across several probes the MTS-Gradient background yields fits comparable to the ΛCDM baseline under the likelihood assumptions adopted here. The results presented in this work provide a reproducible benchmark of the MTS-Gradient cosmological background against standard observational tests.

⸻

1 Introduction

The ΛCDM model provides the current standard description of the large-scale expansion history of the Universe. In this framework the cosmic expansion rate is governed by a combination of matter, radiation, and a cosmological constant.

Despite its success in describing a wide range of observations, alternative phenomenological descriptions of the expansion history remain of interest, particularly when exploring how different background dynamics reproduce late-time cosmological datasets.

In this work we examine the MTS-Gradient cosmological background, a modified expansion history characterised by a redshift-dependent gradient function applied to the matter term of the Friedmann equation. The goal of this paper is to evaluate how this background performs across a set of widely used observational probes.

Throughout the analysis ΛCDM is used as the baseline reference model, and all datasets and likelihood constructions are applied identically to both models.

⸻

2 Model Definitions

2.1 ΛCDM Expansion History

For a spatially flat Universe without radiation the ΛCDM expansion rate is

H(z) = H_0 \sqrt{\Omega_m (1+z)^3 + (1-\Omega_m)}

When radiation is included the expansion rate becomes

H(z) =
H_0 \sqrt{\Omega_r(1+z)^4 + \Omega_m(1+z)^3 + \Omega_\Lambda}

⸻

2.2 MTS-Gradient Expansion History

The MTS-Gradient background modifies the matter contribution through a gradient function g(z):

H(z) =
H_0 \sqrt{\Omega_m (1+z)^3 g(z) + (1-\Omega_m)}

with

g(z)=1-\exp\left[-\left(\frac{z}{z_s x_0}\right)^\nu\right]

The fixed parameters used throughout this analysis are

x0_fixed = 0.966
nu_fixed = 0.942

The free parameters of the model are

H0
Ωm
z_s
r_d


⸻

3 Cosmological Observables

Distances and expansion observables are computed using standard definitions.

Comoving distance

D_C(z) = \int_0^z \frac{c}{H(z')} dz'

Luminosity distance

D_L(z) = (1+z)D_C(z)

Distance modulus

\mu(z) = 5\log_{10}(D_L / \text{Mpc}) + 25 + \mu_{shift}

BAO distance measures

D_H = \frac{c}{H(z)}

D_V = \left[z D_M^2 \frac{c}{H(z)}\right]^{1/3}

Alcock–Paczyński parameter

F_{AP} = \frac{D_M H}{c}

CMB acoustic scale

\ell_A = \pi \frac{D_M(z_*)}{r_d}

CMB shift parameter

R = \sqrt{\Omega_m} \frac{H_0 D_M(z_*)}{c}

⸻

4 Observational Datasets

The following observational datasets are used in the analysis.

Pantheon+ Supernova Sample

1701 Type Ia supernovae using the SH0ES-calibrated Pantheon+ compilation.

Columns used:

zCMB
MU_SH0ES
MU_SH0ES_ERR_DIAG


⸻

DESI DR1 BAO

Anisotropic BAO measurements:

z = [0.510, 0.706, 0.930, 1.317, 1.491]

Observables:

DM / rd
DH / rd

Isotropic BGS measurement:

z = 0.295
DV / rd


⸻

Cosmic Chronometers

Direct expansion-rate measurements:

29 H(z) points
0.07 < z < 1.965


⸻

Growth of Structure

Growth data using the compilation of fσ8 measurements:

Gold-2017 dataset

Growth predictions are computed by solving the GR growth equation for each background expansion history.

⸻

5 Numerical Methods

Likelihood functions are constructed separately for each observational probe.

Supernova likelihood

A nuisance magnitude offset \mu_{shift} is analytically profiled.

Growth likelihood

The amplitude parameter \sigma_8 is profiled analytically.

BAO likelihood

DESI DR1 measurements of

DM / rd
DH / rd
DV / rd

are used with diagonal covariance.

CMB geometry

The acoustic scale and shift parameter are evaluated using

ℓ_A
R

with sound horizon

r_s = \int c_s/H \, dz

⸻

6 Results

Benchmark Comparison

Dataset	ΛCDM χ²	MTS χ²	Δχ²
SN + CC + DESI	828.77	823.66	−5.11
SN + CC + DESI + CMB	842.69	825.29	−17.40
SN + BOSS DR12	817.32	816.05	−1.26
SN + BOSS + CMB	838.68	816.02	−22.66
SN + DESI DR1	834.07	820.98	−13.09
Cosmic Chronometers	54.13	32.42	−21.71
Alcock-Paczyński (DESI)	9.19	8.20	−0.98
BAO DV/rd	5.38	1.36	−4.01
Joint Fit	895.82	861.85	−33.96

Negative Δχ² indicates a lower χ² value for the MTS background for that dataset.

⸻

7 Best-Fit Parameters

Test	Model	H0	Ωm	z_s	r_d
SN+CC+DESI	ΛCDM	66.00	0.365	–	147.71
SN+CC+DESI	MTS	77.77	0.218	0.205	140.93
SN+BOSS+CMB	ΛCDM	68.62	0.306	–	144.21
SN+BOSS+CMB	MTS	76.20	0.236	0.259	146.22
Joint Fit	ΛCDM	68.79	0.329	–	144.75
Joint Fit	MTS	74.57	0.269	0.174	144.19


⸻

8 Discussion

Across several late-time probes the MTS-Gradient background produces fits comparable to the ΛCDM reference model under the likelihood assumptions used in this analysis.

For some datasets the two models yield nearly indistinguishable predictions within observational uncertainties, while in other cases one model produces a slightly lower χ² value than the other.

The purpose of this work is to document these behaviours using identical datasets and likelihood constructions.

⸻

9 Reproducibility

All numerical tests in this work are implemented using a fully reproducible analysis pipeline.

Key constants:

c = 299792.458 km/s
x0_fixed = 0.966
nu_fixed = 0.942

Datasets are loaded directly from publicly available releases including Pantheon+ and DESI DR1.

The full analysis scripts and data links are available in the associated GitHub repository.

⸻

10 Conclusion

We have presented a benchmark comparison between the ΛCDM cosmological background and the MTS-Gradient expansion model using a set of widely used late-time observational probes.

Using identical likelihood constructions for both models, the MTS-Gradient background produces observational fits comparable to the ΛCDM baseline across several datasets considered here.

These results provide a reproducible reference point for further investigation of the MTS-Gradient cosmological background.

⸻

