# Original perturbation reaches ~.15 e-fold without reset

2026-11-08. Accepted audit: audit/result.json from audit_continuation_v3.py. Parent: ../mts-original-mode-real-series-extension-20261108, seal3ba22a5d39071a0c83c07c1cc8802472c5898c5dd1fd443475a1221ccce9a720. Broad MTS goal remains active.

## Verified advance and remaining reference

This packet extends the SAME corrected candidate and its own phase by~.08 e-fold. All120 channel comparisons pass unchanged2e-5: three original wavenumbers, baseline/MTS, GR/spatial-Poisson and ten original channels assessed at five frozen probes. Each branch is compared to its own original full-equation reference. This is internal propagation validation, not an observational likelihood or proof that the two gravity branches coincide.

| Model | Original start N | Candidate endpoint N | Accumulated span | Original reference endpoint N | Remaining span |
| --- | ---: | ---: | ---: | ---: | ---: |
| MTS | -8.518454909126145 | -8.368470146125201 | 0.1499847630009441 | -8.293202925182642 | 0.07526722094255867 |
| baseline | -8.518454909064344 | -8.368566039228474 | 0.1498888698358698 | -8.293202925162689 | 0.07536311406578555 |

These horizons were read from hash-verified original TIME arrays, not inferred from notes. The paired model-specific grids are retained. The early-reference segment is not yet complete and is not the whole path to the cold entrance.

## Paired physical results

Channel error is maximum absolute discrepancy across five probes divided by the maximum reference magnitude of that channel across those probes. Full-state error uses original native-unit normalization. Ratios to earlier interval maxima are bookkeeping only: interval/channel normalization differs, so these ratios are not propagator gains.

| Wavenumber | Model | Gravity branch | Worst channel | Largest channel discrepancy | Full-state discrepancy |
| --- | --- | --- | --- | ---: | ---: |
| half | MTS | gr | Q | 4.4300947890e-7 | 8.360682e-9 |
| half | MTS | poisson-spatial | Q | 4.4325209841e-7 | 8.173893e-9 |
| half | baseline | gr | Pi | 3.1166478823e-11 | 5.739788e-11 |
| half | baseline | poisson-spatial | Pi | 3.0783542027e-11 | 5.869181e-11 |
| balanced | MTS | gr | Q | 1.1920713047e-6 | 7.083641e-9 |
| balanced | MTS | poisson-spatial | Q | 1.1921115334e-6 | 7.072696e-9 |
| balanced | baseline | gr | delta_b | 3.0423688096e-10 | 5.813233e-10 |
| balanced | baseline | poisson-spatial | delta_b | 2.0584832047e-10 | 3.691537e-10 |
| double | MTS | gr | Q | 8.1730127117e-7 | 1.466926e-8 |
| double | MTS | poisson-spatial | Q | 8.1730526496e-7 | 1.467095e-8 |
| double | baseline | gr | delta_massless | 1.0433291896e-10 | 4.526214e-11 |
| double | baseline | poisson-spatial | delta_b | 5.3181767612e-10 | 3.177349e-10 |

The largest MTS channel discrepancy is1.1921115333797518e-6 in Q (balanced,spatial-Poisson), versus the fixed2e-5 gate. Baseline maximum is5.318176761240433e-10 (double,spatial-Poisson,delta_b). Error remains accumulated from the original preparation; no reference reset, fitted residual or changed coupling is used.

## Retained mathematics and implementation

The accepted full finite real Fourier evaluator is byte-for-byte identical to its qualified parent. Its representation and end-to-end regression evidence are inherited, not redundantly recomputed. No phase harmonic, imaginary Nyquist contribution, source field or G192 tail was dropped. Global invariant normalization and slow/clock backgrounds remain unchanged.

New y0 begins at the parent's corrected y_b; only the NEW response increment starts atzero. Full boundary C,C_N and remote streaming derivatives are reused on the new incoming state. The previous approximation discrepancy and leading/response controls remain in the inherited-error ledgers. DERIVATION.md records the first-response equation and Duhamel error identity, keeping higher response and true-background mismatch separate.

Longer-interval step counts are doubled while retaining the preceding maximum physical step: phase2048/1024,leading1024/512,response4096/2048. Source grids,phase256/128,17mean nodes,9/5forcing nodes,thermal tables and ALGEBRA1e-10/GATE2e-5 remain unchanged. Boundary normalization round trips are independently reproduced exactly; their largest relative effect is5.1206306690628936e-17. Joining physical readouts differ by at most1.899e-16, with exact phase/background-state continuity.

## Controls and their scope

| Control | Maximum |
| --- | ---: |
| Full normal-form chain identity | 5.428189469435656e-14 |
| Slow primitive closure | 1.0227201047664698e-13 |
| Phase forcing refinement | 1.213611177279753e-12 |
| Independent fixed-phase derivative difference | 1.2233793289045119e-8 |
| Independent complex-direction source derivative | 2.1817117249752027e-15 |
| Native physical-map check | 1.1495300296857785e-11 |
| Leading mean source/time refinement, state norm | 4.5145708024345306e-11 |
| New response source refinement, original-state norm | 2.102672490307216e-11 |
| New response time refinement, original-state norm | 5.770808058709605e-19 |
| Source refinement relative to SMALL MTS correction | 0.00008705556432141609 |
| Time refinement relative to SMALL MTS correction | 2.530719495577604e-12 |
| New response source control, physical observables | 1.08174728027128e-9 |
| New response time control, physical observables | 1.6426240542507811e-18 |

Important: the small-correction source diagnostic is8.705556432141609e-5. The inherited acceptance gate applies to the original physical-state/observable normalization, not a separately imposed2e-5 relative-to-small-correction condition. Do not claim the small correction is independently resolved to2e-5 relative accuracy; do not hide this diagnostic. Its propagated physical-source control is1.08174728027128e-9, smaller than the accumulated MTS channel discrepancy. The table does not replace inherited numerical/background errors or establish a uniform continuum/gain bound.

## Preserved operational events

- preflight-01 rejected a copied evaluator containing one extra trailing newline. The unqualified copy is preserved, the exact original bytes restored, and preflight-02 passes the SAME hash requirement. No scientific calculation ran in the failed preflight; see PREFLIGHT-REPAIR.md.
- The generic55minute dispatcher declined to start the last evolution with3268seconds left. A measured reserve using the slowest completed identical-step run plus120seconds (3183seconds) fitted the remaining3233seconds. The first launch then completed at15:07:41Z, before the unchanged15:30Z cutoff. No numerical retry, accuracy-gate change or deadline extension occurred; see SCHEDULER-RESUME.md and scheduler-resume.json. The original not-started receipt remains.

## Next actual calculation

Finish the remaining original reference:~.07527e-fold MTS and~.07536baseline, with candidate endpoints fixed to the ORIGINAL last time entries. This is slightly shorter than the present packet; retain the present step counts rather than doubling again. Preserve all source/physical controls, inherited error and frozen probes. Watch the source-relative-to-small-correction diagnostic if a later conclusion depends on resolving that small term.

After completing the available early reference, derive or bound the remaining source-conditioned averaging/gain and original-mode matching to the cold regime. Do not extrapolate this finite numerical result into a whole-history theorem or introduce a new cold initial mode.

Local only. One numerical worker/thread, no GitHub/subagents/apps/servers/compilers or unrelated-process changes. Exact process exits and artifact integrity are recorded in CLEANUP.json/closeout.json.

