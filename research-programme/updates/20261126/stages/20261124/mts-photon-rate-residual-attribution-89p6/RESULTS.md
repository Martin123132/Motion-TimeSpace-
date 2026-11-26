> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# The photon rate gap builds up inside the saved interval

**24 November 2026 · retained mode and photon launch · 89.148503803–89.6 conformal Mpc.** The one-sided derivative at the switch is not responsible for the discrepancy. Around 89–90% of the signed gap comes from after the first stress cycle. Almost all of the **change** on refining gravity is in the resolved-wave reference, while the **remaining** matched contribution is nearly unchanged and on its own exceeds the 0.5% precision threshold.

| Joint photon result | p16 | p32 |
|---|---:|---:|
| Difference of rate routes, % of small momentum-route correction | 0.934810 | 0.710336 |
| Matched residual alone, same units (magnitude) | 0.645007 | 0.645009 |
| Subtracted resolved-wave residual alone (magnitude) | 0.297631 | 0.084964 |
| Signed fraction of gap from matched minus reference, by branch | +68.74% / +31.26% | +90.51% / +9.49% |
| First four coarse knots, signed share | −1.89% | −2.24% |
| After first cycle, signed share | +88.80% | +90.42% |
| Gap with the identical post-switch derivative stencil, % of small correction | 0.934810 | 0.710336 |
| Actual gap as % of original joint launch | 0.00003389 | 0.00002575 |

The two branch **magnitudes need not add**. Their signed shares add to 100%. The first four knots end at 89.15 Mpc; excluding those sources *increases* the remaining gap to 0.9525% / 0.7265%. Two- and eight-knot definitions also yield a negative opening share. The cycle cut is the first shared coarse knot at or after the physical cycle endpoint: 89.241796875 Mpc. The last four coarse steps have small negative shares as well. These are contributions to the full visibility-weighted signal, not simply areas under a local time plot.

**Two different questions.** On the fine step the matched residual accounts for 90.51% of the signed gap. In contrast, the subtracted explicit-wave residual accounts for 99.9996% of the signed fine-minus-coarse *change*. The two matched complex photon vectors differ by only 0.00000434% of the fine small correction. Even setting the reference residual identically to zero would leave about 0.645% on these histories. Two steps do not establish the continuum limit or identify a defective matter equation.

## Calculation and controls

At matched knots let \(R_m=D_{\rm post}\Phi_m-\dot\Phi_{M,m}\), where the dotted rate is from the momentum constraint. Independently form \(R_w=D_{\rm native}\Phi_w-\dot\Phi_{M,w}\) from the sealed explicit-wave potential and rate, retaining its samples before entry. The difference of the two archived photon routes is exactly the linear transport of \(R_m-R_w\): common initial kick, lapse and cold baseline cancel. The separation here is **matched MTS minus explicit-wave MTS** inside a comparison with a fixed cold photon history, not a new independent baseline evolution.

For a separate end-stencil test, resample the explicit potential to precisely the matched clock. The gap source can also be written
\[
 [D_{\rm post}(\Phi_m-\Phi_w)-(\dot\Phi_{M,m}-\dot\Phi_{M,w})]
 + [D_{\rm post}\Phi_w-D_{\rm native}\Phi_w].
\]
The second bracket measures the change from the asymmetric treatment of the reference; it contributes only 0.0000000211% / 0.0000000068% of the small photon correction. This does not assume the matched potential has a smooth physical continuation through the switch. The signed time partitions give an independent check that the early source is not driving the gap.

Each already-interpolated rate is split on transport step boundaries. Both collocation stages of a step stay with that step, including its right endpoint. Each piece propagates to the same visibility window, with zero artificial kick and the original time/angular settings. Signed share of term \(v_i\) is \(\operatorname{Re}\langle g,v_i\rangle/\langle g,g\rangle\), where \(g\) is the archived complex energy/current gap and the inner product uses the original visibility weights. Adding the signed branches recovers the two archived photon components to better than \(4\times10^{-12}\) relative RMS at all three transport settings. Photon time and angular controls pass on the gap; changing the gravity step changes the gap vector by 36.98% of the fine gap, so we do not claim convergence of the gap. Both total correction routes stay below the fixed 0.163%-of-launch threshold.

[Input protocol](PROTOCOL.md) · [windows](evidence-001.zip) (archive member: `time-cuts.json`) · [source identities](evidence-001.zip) (archive member: `source-checks.json`) · [signed contributions](evidence-001.zip) (archive member: `signed-attribution.csv`) · [two-step attribution](evidence-001.zip) (archive member: `gravity-step-change.csv`) · [absolute and relative gates](evidence-001.zip) (archive member: `rate-gates.csv`) · [full-vector replays](evidence-001.zip) (archive member: `vector-replay.csv`) · [numerical controls](evidence-001.zip) (archive member: `numerical-controls.csv`).

**Next:** use the saved matched constraint ledger to transport its signed matter, radiation and geometric residuals, first over the post-first-cycle interior and then over the whole window. Require their sum to reproduce the stable 0.645% matched vector at both steps before assigning a cause; separately keep the explicit-wave reference contribution. No new interval, fitted amplitudes or adjusted tolerances are needed.
