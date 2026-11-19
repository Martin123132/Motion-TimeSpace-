# Original prepared trajectory: complete saved reference interval

Status: verified progress, 2026-11-08. Local only; no GitHub, subagents or new fits. Parent: ../mts-original-mode-next-reference-packet-20261108 (seal ad51bff1451898d45a30ef05561aff0e43761e5c45ef616cbfac5b2f1b16ea75).

## Physical result

The same original perturbation now reaches the exact end of its retained early-time numerical reference. The corrected state, own physical phase and global background normalization are carried across every boundary, never replaced by a new cold unit mode or reset to the reference.

- MTS: N=-8.518454909126145 to -8.293202925182642, span 0.22525198394350276.
- Baseline: N=-8.518454909064344 to -8.293202925162689, span 0.22525198390165535.
- Three wavenumbers; both GR and spatial-Poisson branches; ten physical channels per branch.
- This last interval adds 120 per-channel comparisons. The complete five-interval audit checks 600 per-interval channel results using their original local normalizations.
- Each model/wavenumber has 21 distinct frozen physical readout epochs and 81 saved corrected mean-state epochs. Boundary duplicates are removed only after verifying the joins.
- All original channel gates pass at 2e-5 (0.002%). The worst MTS discrepancy over the whole chain is 2.072881286154049e-6 (0.0002072881%), in Q for the half-wavenumber GR branch. Worst baseline channel discrepancy over the chain is 5.318176761240433e-10, in the preceding interval.
- Actual original native initial states agree within 8.409343557629646e-13 in their original unit-normalized norm. Every intervening preparation carries the preceding corrected state byte-for-byte. Solver normalization round trips are reproduced exactly. Maximum physical readout join is 2.0509838866397855e-16; maximum encoded join is 3.6916235235797475e-16. Phase and background joins are exact.

## Final interval by branch

| Wavenumber | Model | Gravity branch | Largest channel | Relative discrepancy |
|---|---|---|---|---:|
| half | MTS | gr | Q | 2.072881286e-6 |
| half | MTS | poisson-spatial | Q | 2.067230749e-6 |
| half | baseline | gr | delta_b | 2.240378848e-10 |
| half | baseline | poisson-spatial | delta_b | 9.873638169e-11 |
| balanced | MTS | gr | Q | 1.712649190e-6 |
| balanced | MTS | poisson-spatial | Q | 1.712770921e-6 |
| balanced | baseline | gr | Pi | 9.721170556e-11 |
| balanced | baseline | poisson-spatial | delta_b | 1.986519536e-10 |
| double | MTS | gr | Q | 2.029036021e-6 |
| double | MTS | poisson-spatial | Q | 2.028980655e-6 |
| double | baseline | gr | delta_massless | 2.572527442e-10 |
| double | baseline | poisson-spatial | delta_massless | 2.573121764e-10 |

Each row compares its own branch against its own original full-equation numerical reference, not against the other gravity branch. These are finite sampled numerical consistency comparisons, not fresh observational evidence or 600 independent experiments. Inherited reference uncertainty is not eliminated by agreement; shared inputs can cancel errors.

## Unchanged accuracy controls

- Algebra gate 1e-10; physical numerical gate 2e-5.
- Original G192 hierarchy, thermal/source inputs, phase grid, couplings and physical grids retained. Qualified full real Fourier representation reused without dropping harmonics.
- Last-interval chain identity: 9.107983366975003e-14; slow primitive closure: 8.960982062273571e-14.
- Phase-forcing refinement: 7.228736572058467e-13; independent fixed-phase derivative difference: 9.314789739939734e-9.
- Complex derivative check: 3.2055762808987163e-15; native physical-map check: 1.8186120959119685e-11.
- Response source refinement relative to physical state: 1.597488826131125e-11; time refinement: 6.712466865861788e-19.
- Propagated physical-observable source control: 9.695536244922908e-10; time control: 1.659992627755649e-18.
- Relative to the much smaller MTS correction itself, source refinement is 7.994981534981198e-5 and time refinement 3.35014609020382e-12. The source diagnostic does not meet 2e-5 relative accuracy on that tiny increment; this is disclosed, not silently promoted to such a claim. The original physical-state/readout acceptance normalization remains unchanged.
- First-response truncation, true-background/source differences and long-time gain still need controlled estimates before extrapolation. The observed discrepancy has grown in parts of this trajectory; completion does not license unlimited extension with the same approximation.

## Evidence and reproducibility

- audit/result.json: final acceptance, individual channel results, controls and consumed-file hashes.
- chain-audit-01/result.json: complete five-interval path, 600 recomputed channel checks, exact reference ownership, original initial state and endpoint checks.
- chain-audit-01/{half,balanced,double}-{heavy,cold}-joined.npz: joined predictions, original reference values, phases, native encodings and corrected states; these reuse existing results rather than refit them.
- join-diagnosis-01/result.json: final boundary round-trip and original horizon checks.
- DERIVATION.md: unchanged first-response equation and inherited-error identity.
- SLOW-TRANSPORT-HANDOFF.md: next exact change of variables, with explicit outstanding validation.
- Source and receipt files preserve all executed versions; no numerical failures or automatic retries occurred.

All numerical work used one below-normal, single-thread worker at a time. All 37 tracked Python invocations finished successfully. CLEANUP.json and closeout.json provide final process-exit verification and artifact readback. No original bank, sealed upstream checkpoint or formalization-workbench file was edited. All planned stages in PLAN.md are complete.
