# Neutrino shear, the metric, and slow-field pressure

Private calculation, November 18. We changed a single numerical prescription after a matched state, not the MTS action, the primordial state, the scalar mass, or a fit parameter. The empirical question here is **not** whether MTS beats a cosmological dataset: the reference is a prior numerical implementation at k=5 Mpc⁻¹. “Crossed pressure” uses the old homogeneous slow velocity for both forcing and readout, on the newly evolved geometry. “Physical pressure” uses the independently evolved background. Keep the two distinct.

## Which change explains the remaining discrepancy?

The retained flat calculation switches at x=kτ=52 (τ=10.4 Mpc). This follows from its configured massless L=56 and max(20,L−4)/k rule; it is not a fitted transition time or a direct timestamped callback. Both continuations started from the exact same complete saved state of their own model at that clock. Density, flux, shear, metric, fields and photon/baryon state were unchanged. One copy kept the full hierarchy. The other copied the lowest three massless moments and changed only their subsequent shear equation. Two more arms independently switched the massive hierarchy to its native l=16 boundary, alone and together with the massless switch. Perturbations continued to gravitate in every arm.

| Crossed pressure error at the material event | Baseline | MTS |
|---|---:|---:|
| Continue free streaming | −0.01161% | −0.01372% |
| Massless fluid only | +0.000394% | +0.000716% |
| Massive cutoff only | −0.01193% | −0.01483% |
| Both changes | +0.0000745% | −0.000395% |

The massless switch alone removes slightly more than the original residual in both models; the massive cutoff partly offsets that improvement. The two changes are not interchangeable. Neither explains away the original **physical** MTS pressure difference: using the independently evolved slow velocity still gives about 57.72% less slow pressure than the old implementation, consistent with the preceding stage's velocity attribution. Reproducing the archive is a diagnostic, not a reason to substitute the archived velocity into the physical prediction.

The massive five-node source was checked against all 2,262 captured RHS rows in **both** models. Evaluating the original Fortran default-real literals before conversion reproduces the dipole and l=16 boundary derivatives at floating-point precision. Decimal and literal, balanced and raw finite-quadrature, and higher-momentum cases are kept separate. The pre-switch histories are physical restarts: this is not presented as an exact reconstruction of every earlier tight-coupling and massive-node activation in the native code.

## Why the pressure responds

The switch changes the **derivative** of the massless shear immediately (J = −0.0003071344 baseline, −0.0003286597 MTS), but not the shear itself. Flux and density cannot jump. A cancellation then matters: the cubic-order curvature and half-density changes have opposite signs in the Einstein constraint. The resulting CDM forcing starts at fourth order in elapsed x, not third. Integrating the scalar equation once more makes its scaled pressure response start at **fifth** order:

    ΔP(t) = (φ′*)² f_r J t⁵/(60 g*²) + O(t⁶),   t = k(τ−τ*).

This coefficient uses only the state at the switch. The independently forced difference equations measure the physical coefficients −6.47762×10⁻⁴² (baseline) and −6.93054×10⁻⁴² (MTS) in the sense that the measured/derived ratios extrapolate to 0.999999967 in both. The observed numerical spreads are about 6.0×10⁻⁷, below 2×10⁻⁵. At t=2 the independently driven crossed-pressure changes agree with subtracting the two full runs to 2.6×10⁻⁸ and 1.6×10⁻⁸ relative. No imposed source returns exactly zero, and the opposite source reverses the result. See ONSET-LAW.md and the two direct-onset packets.

At the later material event this is no longer just a short-time power law. Splitting the CDM forcing into the curvature and species densities and evolving a separate linear scalar response for each recovers the net change. For example, in the MTS joint switch the curvature contributes about −10.10 times the net pressure change; the massless and massive density contributions are +5.85 and +5.51 times the net, and CDM contributes −0.259. Photons, baryons and the parent fields complete the balance. These are signed terms in one gauge, not independently measurable energy fractions. Quoting a single positive neutrino term would give the wrong answer.

The hierarchy approximation is taken from the retained Fortran; [Blas, Lesgourgues & Tram](https://arxiv.org/abs/1104.2933) give its scientific context. The pressure propagation and switched comparisons above are local calculations. No public files, older bank, or native executable were changed.

## Radiation stress: a coefficient from the equations

On a matched initial state with no extra density or flux, an imposed radiation shear starting as A tⁿ gives a leading scaled slow-field pressure of **2 A n!/(n+4)! × (φ′*)² f/g*² × tⁿ⁺⁴**. Here f is the corresponding relativistic background fraction, t is elapsed kτ and g* is the retained dimensionless background scale. The four integrations and cancellation are derived in SHEAR-KERNEL.md. Independent unit-shear histories on both backgrounds pass for n=0,1,2,3 (pressure powers 4–7), across a change of hierarchy, metric equation and numerical step. This is a short-time response on this linear branch and these matching conditions, not a universal scattering law.

With this normalization a photon **intensity** quadrupole gives 2.169778907 times the leading pressure response of the same massless-neutrino quadrupole; the independently predicted background fraction ratio is 2.169778907 in both models. A pure initial **linear polarization** quadrupole instead starts at fifth order: polarization feeds intensity shear at 0.6 opacity/k. Removing only that mixing leaves polarization present and gives an exactly zero linear intensity/metric response in this test. At one baryon–photon relaxation time the intensity and polarization pressure amplitudes are already about 0.4% below their leading laws. Do not use those asymptotes as a finite-time fit. See PHOTON-STRESS.md and the photon-probe files.

## What survives to epoch 4252?

The material gate (nine of nine pressures in each model including trial spreads; tolerance 2×10⁻⁵) permitted forward propagation. No field was rematched after 1999. The following counts include **all 2,253 new epochs** (2000–4252; conformal time about 88.60–102.72 Mpc), using each target's own absolute magnitude and including numerical sensitivities.

| Joint-switch channel compared to archive | Baseline passes | MTS passes |
|---|---:|---:|
| Slow pressure, archived homogeneous velocity diagnostic | 2,253 | 1,996 |
| Slow pressure, independently evolved physical background | 2,253 | 0 |
| CDM forcing; metric shear (each) | 2,253 | 2,253 |
| Massless neutrino density | 2,091 | 2,124 |
| Massive neutrino density | 0 | 0 |

For the archived-velocity pressure, uninterrupted free streaming instead gives 567/2,253 baseline and 177/2,253 MTS. After the joint switch the MTS diagnostic reproduces all six pressure sign changes; the maximum shift of the linearly interpolated crossings is 9.96×10⁻⁶ in kτ. All epochs pass **on the peak scale**, but this does not supersede the 257 misses on their own scale. The first miss is epoch 2117. At 4252 the diagnostic differs from the archive by +0.000341%, whereas the independently evolved physical slow pressure differs by −64.31%. The heavy-field pressure has a distinct error budget (420/2,253 own-scale passes); reproducing the metric does not reproduce every stress.

Across **all 257 misses**, the slow perturbation's **velocity**, rather than its field value or stress-readout weights, is the largest component of the crossed-pressure error. We also derived the forcing-history split in VELOCITY-MEMORY.md. The first uninterrupted region with fine native source sampling ends at 3038. At its 137 misses the largest propagated contribution is consistently the **field displacement already present at 1999**, which the oscillator converts to a velocity error. At the first miss this contributes about +4.76 times the net error; the subsequent metric drive offsets it by about −4.23 times. The component ordering survives the replay/interpolation budget at all 137; the signed shares are not known to 2×10⁻⁵ relative to the small *discrepancy*. No such pressure failure occurs in the baseline control. This identifies a causal input to investigate before 1999, not a reason to retune the late pressure. The attribution has not been extended across the large gaps to the other 120 misses.

## Integrated radiation on the same expansion interval

On the common interval a=0.0002234303391–0.0002618009551, the joint-switch MTS history has **90.5168% less dipole-slip drag integral** and **8.17189% less angular collision integral** than the baseline. These are quadratic one-mode diagnostics, not gas heat or a predicted sky spectrum. The same comparison with free streaming gives −90.5166% and −8.16396%, respectively.

The sparse original output rates fail as independent quadrature: several gaps exceed five units in kτ. Recording the rates passively at all **29,703** accepted fine-scheme steps per replay preserved all 53 original outputs at all 2,254 clocks and each terminal state bit for bit. Dense independent quadrature and model controls bound the measured numerical sensitivity of the two joint-switch contrasts at 3.57×10⁻⁹ and 2.62×10⁻⁶ relative, respectively, against the unchanged 2×10⁻⁵ threshold. The archived comparison has no corresponding dense record here: its staggered-sampling spreads are 0.80% and 72.3% of its respective contrasts. Do not transfer our internal precision to it. RADIATION-WINDOW.md, DENSE-READOUT.md and both sparse and dense results preserve this distinction.

**Next:** propagate the field-displacement and velocity response kernels *up to* 1999 and isolate when the inherited displacement is generated. Use the same perturbation equations, physical and archived-velocity branches, and shared metric controls. Test on the baseline as well; where the native driving history is undersampled, report the unresolved interval rather than differentiating rounded CDM densities or fitting the pressure zeros. Keep the physical epoch4252 restart and all unsuccessful archive comparisons.
