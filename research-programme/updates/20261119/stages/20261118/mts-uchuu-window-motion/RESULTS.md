# Does the velocity correction survive the survey window?

**Answer:** the close-pair term remains measurable, but it does not uniformly improve the full monopole and quadrupole. At the two primary wavenumbers it helps the North slightly and hurts the South slightly. A field-level diagnostic identifies the useful target: the *spatially varying* signed residual velocity current and its second moment, not another global dispersion. The first boost-invariant candidate for those two inputs is derived, calibrated on low-z mock 0 and saved for a separate transfer test.

## Measurement

The same 176,826 southern and 393,919 northern selected **cone-1** galaxies were evaluated at their real and redshift-space positions, with original weights. This includes satellites lacking a unique host. Subtracting the published COMB random window uses 7,349,655 South and 16,157,158 North random points in 0.2≤z_obs<0.5. This experiment isolates displacements at fixed sample membership; it does not model galaxies entering or leaving selection. [Uchuu release](https://skun.iaa.es/SUsimulations/UchuuDR2/Uchuu_GLAM_BOSS-eBOSS/Uchuu/) and [simulation methods](https://arxiv.org/html/2311.14456v2).

For each local line of sight n define F_ℓ=Σgal w L_ℓ(khat·n)exp(−ik·s)−αΣran w_r L_ℓ exp(−ik·s_r), following the [endpoint power estimator](https://arxiv.org/abs/1505.05341). For disjoint random halves A,B use 2(2ℓ+1)Re(F₀A F*ℓB+F₀B F*ℓA)/Σgal w². This unit is the sample weighted shot scale, not (Mpc/h)³. One half never pairs a galaxy row with itself. Hence replacing each satellite by a probability distribution calculates the expected cross-power for independent draws without a spurious self term; a conventional whole-catalogue auto difference is a separate check. Fixed α per half, same actual sky window in every branch. Local-only ducc0 nonuniform Fourier transforms, one thread, all shell modes and full randoms, no periodic replication of survey galaxies.

| Cone 1, true shift | k=0.025 | k=0.050 |
|---|---:|---:|
| South Δmonopole | 2.8513 | 1.8620 |
| South Δquadrupole | 5.0361 | 3.7620 |
| North Δmonopole | 2.7655 | 1.6806 |
| North Δquadrupole | 5.0561 | 3.3293 |

Centers in h/Mpc, each ±0.0025. Two stress bands at 0.075/0.10 are in paired-multipoles.csv. All cells, caps, cone-0 calibration controls, ordinary equal-mode averages and auto results are retained. Positively reweighted cubic-symmetric mode shells integrate the angular polynomials of the transfer through quartic order; individual mode weights are 0.924–1.085 times the shell mean. Primary cross and conventional auto do not have identical finite-sample noise.

## Frozen forecasts

Use each actual mock central's velocity, retain the 3D central projection for matched satellites, and use an eight-central radial-flow proxy for missing hosts. The measured missing-satellite proxy residual RMS is 6.07/6.13 h⁻¹ Mpc, South/North. Exact coincident other-family positions in this first proxy use the finite inverse-square interpolation limit, not a division by zero. Keeping unresolved satellites at real radius while moving everything else changes the low-k quadrupole by 0.289/0.305 at k=0.025: omitting them would not have answered the question.

| Cone-1 mean absolute error over ℓ=0,2 and k=0.025,0.05 | South | North |
|---|---:|---:|
| Host/proxy alone | 0.07206 | 0.03629 |
| Independent internal motions, measured in cone 0 | 0.01274 | 0.04250 |
| Independent + angular close-pair correction | 0.01332 | 0.04029 |
| One-body mean linear in absolute host displacement | 0.17284 | 0.21094 |

No coefficients were fitted to these spectra. The last branch is **worse in both caps**; a one-body correlation with absolute host speed is not a good substitute for relative flow. The previous 77–90% improvement concerned a conditional close-pair cosine, not these full multipoles. These are correlated ΛCDM mocks with central velocities given, not a BOSS fit or a choice between MTS and cold matter.

For a true real-space pair within 10 h⁻¹ Mpc, let s be its shifted separation and Q=3[(n_i·s)²+(n_j·s)²]/2−s². Through k⁴ its orientation-averaged response has coefficients (−s²/6,s⁴/120) for ℓ=0 and (−Q/6,Q s²/84) for ℓ=2. Subtract the independent distribution before averaging. The difference is taken on cone 0 by shell, endpoint types (including proxy satellites), and family equality; evaluation supplies only real-pair composition to the correction. The four-node integration is exact for all the needed polynomial moments including the sixth-order error bound; its finite-Bessel output is a control, not labelled exact for the full distribution. Unsupported calibration cells account for 0.186%/0.00073% of the corresponding cross-pair weight South/North. They add no estimated correction; this is not evidence that their physical correction vanishes.

## Where the remaining error comes from

At k=0.025 the southern quadrupole discrepancy actual-minus-independent is +0.00322. It contains a **−0.51507 data–random** contribution, +0.00164 from galaxy pairs within 10, and +0.51665 from larger separations up to the close Taylor remainder (bounded by 0.000036). North gives +0.08085 = −0.63212 + 0.00081 + 0.71216, to rounding and the 0.000047 remainder. These are signed terms in one estimator, not independent pieces of evidence. Removing the random window or attaching a multiplicative constant to the short-pair result would miss the cancellation.

At the field level, keep the host and real-space phases and the random window **unexpanded**. With t=k·n, true residual D and cone-0 satellite law φ, expand only exp(−itD)−φ(t). The first source is −it(D−〈D〉); the second is −t²(D²−〈D²〉)/2. The sums are weighted by the actual tracers and evaluated at host/proxy positions, including the endpoint Legendre factors. This is an application of the [density-weighted velocity moment expansion](https://arxiv.org/abs/1109.1888); the matched mock test and error decomposition are the new work.

| Diagnostic using actual cone-1 residual fields | South error | North error |
|---|---:|---:|
| Original independent prediction | 0.01274 | 0.04250 |
| Add measured first moment only | 0.00817 | 0.01038 |
| Add measured second moment only | 0.01211 | 0.05235 |
| Add both measured fields | **0.00135** | **0.00073** |

This last row **uses the evaluation velocities**. It localizes the missing physics, not an independent predictive gain: the two moments remove about 89%/98% of the primary error when supplied. These are number-weighted tracer moments, not automatically the fundamental conserved MTS stress. At k=0.10 the residual quadrupole errors with both moments are −0.00147/−0.01653, so do not extrapolate two terms arbitrarily.

## A specific, testable next prediction

SLIP-CONTRACT.md and boost-safe-seed.json define a candidate using only central radial velocities around each target, never satellite test speeds. Weighted local vector projection supplies a surrounding flow: adding the same space velocity to all neighbours shifts the predicted radial speed by exactly n·U. The **difference** between host and surrounding velocity, and the scatter around the local streaming velocity, are unchanged. This supplies an invariant argument for both source moments. Four training scatter bands and the regression/velocity laws are empirical tracer inputs, not derived parent constants.

Calibration on cone 0: slopes for matched satellites −0.698 South/−0.655 North; for locally reconstructed missing hosts −1.362/−1.235. Uniform-boost check <3.6×10⁻¹¹ km/s. The eight-neighbour reconstruction has a North worst-case noise amplification of 14.9 (99th percentile 1.46); carry those ill-conditioned geometries into the transfer gate rather than clipping them after scoring. The baseline in that gate must use the same host/proxy definition as the candidate to separate geometry from response. **Next test:** freeze the mean-only and mean-plus-local-scatter sources against that matched baseline, propagate them into the 0.5≤z_obs<0.6 monopole and quadrupole using the actual higher-z random window, and report errors separately for both caps. No upper-z power was calculated in this stage. Only after this input is under control compare to the native parent/cold/ΛCDM coherent fields with the same estimator.

## Reproduction

New private directory only. In a fresh copy next to the sealed preceding stage: window_sources.py; dependency.py (pinned local wheel, no global install); fourier.py S N; run.py train; run.py S0 N0 S1 N1; diagnose.py; current.py; verify.py; slip_seed.py. Python 3.13 with -B, NumPy, SciPy, h5py. Outputs are exclusive-create. Verified direct signed data/random pair test 1.15×10⁻¹⁰ absolute; discrete shell angular identity <4×10⁻¹⁵; end-to-end direct-mode checks <2.5×10⁻¹⁰ in their RMS-weight units; whole-interval characteristic error bound <1.1×10⁻¹². Saved 224 response rows plus individual-mode residuals, input receipts and checksums. BRANCH=mock-conditioned tracer response only; no observed-data re-fit, public upload or background worker.
