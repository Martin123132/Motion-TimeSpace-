> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# Quark and gluon stress in the parent photon–curvature readout

21 November 2026 · Local derivation and tests for checkpoint 4946. No new empirical fits.

**Result:** The previously calibrated readout now operates on a finite noncommuting gauge-field measure with charged sea quarks. A direct change to the partition function confirms the full response, and exposes which terms a simpler calculation loses. We also found and removed a false curvature signal in the ordinary Maxwell control.

| Test | Result | What it establishes |
|---|---:|---|
| Two independent constructions, 3 color histories × 4 momentum choices | max 1.40×10⁻⁷ absolute difference per site | Matrix-trace formula agrees with directly changing all three sources, original 2×10⁻⁷ gate |
| Both frozen weighted combinations | 6.52×10⁻⁹ and 1.09×10⁻⁸ absolute differences | Response survives the actual retained projection |
| Explicit real-source, translated log partition | differences <8.37×10⁻⁹ for both quadratures | Normalized-measure check independent of the complex closed-momentum shortcut |
| Gauge cancellation, every history/mode, either or both photons longitudinal | max 5.47×10⁻¹⁶; dropping contacts gives up to 0.00644 | Pure-gauge sources really cancel, rather than the whole test being insensitive |
| Two one-current loops in three-light-flavor test | exact mass-difference factor checked to 6.48×10⁻¹⁶ on source traces | Distinct from the stress/two-current covariance that does **not** vanish at equal masses |
| Change gluon stress interpolation in coupled action | predicted two weighted shifts agree with direct changes to <1.55×10⁻¹¹ | A calculable regulator change, not a retuned physical coupling |

The coarser finite difference **missed the original gate in all twelve cases** (worst 2.74×10⁻⁵). Keeping those outputs, we halved the step twice and used two independent overlapping three-size extrapolations; each and their difference passes the same gate. Small errors above compare evaluations of one specified finite action, not systematic errors on QCD.

Omitting the change of statistical weight misses the two dimensionless readouts by 0.04731 and 0.01105. Omitting all but the triangle misses them by 0.07388 and 0.03676. These are absolute differences in the test, not fractional contributions in real matter. See all seven pieces (not bundled here), direct checks (not bundled here), [all gauge controls](evidence-001.zip) (archive member: `all-ward-controls.csv`).

**What transfers to the physical calculation.** The common response formula includes gluon stress even when the external photons couple only to quarks. In the three-flavor isospin limit the contributions with currents on *separate* loops factor out (m_s−m_l)²; the stress–two-current covariance does not. This lets a future calculation preserve an exact cancellation rather than estimate two large terms separately. [Derivation and independent four-dimensional check](DERIVATION.md).

Ordinary Maxwell theory on the plaquette grid puts an apparent +Zγ a²/96 into **both** previous readouts for a corner-averaged metric. We derived a local shear sampling rule, ⅔ corner average + ⅓ center, that cancels this artifact at leading order in both banks and **exactly** at every momentum in the first. The second has a known finite-momentum remainder. Direct coordinate tests and an independent two-point calibration check this without comparing numbers to the desired QCD result. [Derivation, finite-momentum identity, and injection tests](MAXWELL.md).

**Next actual data target.** The [CLS / ILDG D450r010 ensemble record](https://www-zeuthen.desy.de/ape-cgi-bin/ildg-mdc.cgi?action=show&collection=ensemble&grid=ldg&id=mc://ldg/cls/nf21/D450r010) specifies a 128×64³ SU(3) chain, 2+1 Wilson-clover flavors, β=3.46, c_SW=1.915595, gauge plaquette and rectangle coefficients 5/3 and −1/12, and per-configuration reweighting. This is a concrete production action, not the simple Wilson/plaquette fixture above. For matched physical momentum units on this elongated lattice use temporal harmonics +4,−2,−2 against spatial 0,+n,−n. Check the run's actual propagator boundary convention and determinant weights before any reading. Do not assume all CLS chains have periodic time: the [ensemble paper](https://arxiv.org/abs/1411.3982) describes the open-boundary construction too.

The useful next calculation is the rectangle and clover contribution to the shear/current variation for that action, tested against independent action changes, flat current two-point contacts, and the nonforward stress Ward identity. Distinguish electromagnetic gauging of the chosen clover improvement from the underlying color clover; a prescription that agrees only at zero external field does not fix finite source contacts. Curved-source stress normalization/mixing and the finite same-Weyl subtraction convention must be documented. Reuse compact saved correlators if available; no gauge configuration, reweighting file or measured TJJ correlator was downloaded here. One double-precision uncompressed four-link color field on this geometry is ~18 GiB before working space, so do not start a bulk download or naive dense solve on this laptop. No inference about a mass gap or a physical QCD contribution to the pulsar lag from these finite measures.

[Replay and file validation](REPLAY.md) · [previous continuum and scalar-lattice calibration](../mts-mixed-current-weyl-extractor/RESULTS.md).
