# Exact real-series evaluation and longer original-mode transport

2026-11-08. Accepted numerical audit: audit/result.json (audit_continuation.py). Broad MTS objective remains active. Previous completed stage: ../mts-contiguous-mode-extension-20261108, seal8593146437412d04d2a1ee90806f85090580a809fb16fc9b60974335f4374f3d.

## Verified advance

The original prepared perturbation now reaches approximately .07 e-fold from its original N=-8.518454909126145 start. This packet adds .03999929425968496 e-fold for MTS and .03998083501090122 for the baseline. New final epochs are MTS N=-8.448462527230577 and baseline N=-8.448509640165089, using their unchanged original grids.

All120 channel comparisons pass the unchanged2e-5 gate: three wavenumbers, baseline/MTS, GR/spatial-Poisson, ten original channels over five frozen probes. Each branch is compared with its OWN saved full-equation reference; this is not a claim that GR and Poisson coincide with one another, nor an observational fit.

No reference-state reset, new physical preparation, fitted residual, discarded phase coefficient, changed bank/hierarchy or relaxed tolerance was used. The inherited candidate's corrected mean state and physical phase are retained. The NEW response alone starts from zero.

## Exact computational improvement

DERIVATION.md proves the real-coordinate representation of the SAME finite Fourier polynomial, including the FFT's negative Nyquist mode and arbitrary non-Hermitian rounding. real_series.py applies it before the same cubic interpolation and evaluates a real matrix-vector product. Normal-form and coordinate-map responses stay separate. No harmonic cutoff or approximate low-rank compression is introduced.

- Synthetic complex-polynomial tests (1,2,8,256modes, unconstrained complex coefficients) agree within9.523e-16 relative.
- Saved physical source tests cover both models/all three wavenumbers and frozen phase/time probes; maximum relative difference2.4099467277975546e-15.
- The preceding full half-wavenumber interval was rerun at its ORIGINAL1024-step limit before new propagation: separate MTS response components agree within3.2305938304721857e-15 relative; baseline within1.2202391849650275e-16.
- Repeated MTS evolution takes264.385seconds versus the retained635.744seconds, approximately2.40x faster for this numerical integration (not a claim of identical speedup for every workload). Polynomial-only saved-source benchmarks show2.71–2.81x for MTS.

The new longer interval doubles maximum-step counts so maximum physical step size is retained: leading512/256, response2048/1024, phase1024/512. The phase256/128 controls,33source epochs,17mean nodes,9/5forcing nodes and fullG192 hierarchy remain.

## Paired results

Channel error is maximum absolute discrepancy across the five probes divided by the maximum reference magnitude of that channel across those probes. Full-state error uses the retained native-unit normalized state norm. Interval normalizations differ from the preceding packet, so ratios of maxima are NOT propagator-gain bounds.

| Wavenumber family | Model | Branch | Worst channel | Largest channel discrepancy | Full-state discrepancy |
| --- | --- | --- | --- | ---: | ---: |
| half | MTS | gr | Q | 8.5392722789e-8 | 5.570597e-9 |
| half | MTS | poisson-spatial | Q | 8.5451681690e-8 | 5.705308e-9 |
| half | baseline | gr | Q | 5.5621122190e-12 | 9.949420e-11 |
| half | baseline | poisson-spatial | Q | 5.5773467538e-12 | 8.923010e-11 |
| balanced | MTS | gr | Q | 1.7106342039e-7 | 7.022888e-9 |
| balanced | MTS | poisson-spatial | Q | 1.7105778555e-7 | 7.052579e-9 |
| balanced | baseline | gr | Pi | 2.2729538002e-11 | 2.668239e-10 |
| balanced | baseline | poisson-spatial | delta_b | 2.3763988164e-11 | 4.966465e-10 |
| double | MTS | gr | Q | 2.5586284572e-7 | 4.131102e-9 |
| double | MTS | poisson-spatial | Q | 2.5586294549e-7 | 4.133488e-9 |
| double | baseline | gr | delta_b | 6.8687903674e-11 | 3.424530e-10 |
| double | baseline | poisson-spatial | delta_b | 4.0204258337e-10 | 1.538023e-9 |

Largest MTS discrepancy2.558629454886972e-7 is in Q (double,spatial-Poisson), below2e-5 by a factor~78.2. Baseline maximum4.02042583371576e-10 is in delta_b (double,spatial-Poisson). The accumulated MTS discrepancy has grown; it is recorded, not removed by resetting or renormalizing the physical initial state.

## Numerical and derived-source controls

| Control | Maximum |
| --- | ---: |
| Full normal-form chain identity | 8.960770645998741e-14 |
| Slow primitive closure (boundary qualification inherited) | 1.165183067175154e-13 |
| Phase128/256 forcing refinement | 2.0275444587011466e-12 |
| Independent fixed-phase primitive derivative | 6.579178800920423e-9 |
| Independent complex-direction generator derivative | 1.6013847618082417e-15 |
| Native physical-map value check | 7.942653662333677e-12 |
| Leading mean source/time refinement, state norm | 1.624171305308965e-13 |
| New response source refinement, original-state norm | 1.272350116496786e-12 |
| New response time refinement, original-state norm | 3.5056287662245804e-19 |
| Source refinement relative to small MTS correction | 0.000005671374788863766 |
| Time refinement relative to small MTS correction | 1.0865002627164263e-12 |
| New response source control in physical observables | 8.71947913012782e-11 |
| New response time control in physical observables | 7.641304520247585e-19 |

Source/time readout controls concern the NEW response on the retained leading solution, not all inherited error. Initial state normalization round trips are independently reproduced exactly; their maximum relative effect is1.0742878539743763e-16. Preparation packets preserve inherited input bytes, and corrected first outputs equal the first leading outputs exactly. Joining physical readouts differ by at most2.051e-16; phase/background state match exactly.

## Error interpretation and next move

The new response source/time controls are much smaller than the accumulated Q discrepancy. That does not certify a complete continuum error budget: inherited errors, omitted R*delta, invariant drift, slow-background and clock/source mismatches remain separate. The Duhamel error identity in DERIVATION.md carries the old error explicitly; no uniform gain bound is asserted without deriving it.

Next advance: qualify a further contiguous~.08 e-fold on the same original trajectory, with frozen probes and doubled step counts, subject to the original source/refinement gates and a four-hour safe cutoff. This aims toward completing the available saved early-reference segment rather than producing more audit-only stages. After that finite segment, source-conditioned averaging/gain bounds and cold-endpoint matching are the route to the cold regime; do not substitute an arbitrary new cold initial mode or extrapolate this finite numerical check into a whole-history theorem.

Everything remains local. One numerical worker/thread at a time; no subagents, GitHub operations, compilers, apps, previews or servers. No failed calculation attempts occurred in this stage. CLEANUP.json/closeout.json provide exact worker identities, exits and artifact readback hashes.

