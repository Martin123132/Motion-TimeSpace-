# When the inherited field displacement is made

Private parent calculation, 18 November. Starts with the 309-file sealed neutrino-switch stage, not a new action. Baseline = the retained cold preparation; MTS = the retained heavy-bath preparation. The references and growth rates here are **saved numerical cosmologies**, not galaxy surveys or sky measurements. No parameter was fitted.

## Answer at epoch 1999

The MTS discrepancy that later shows up as a velocity error is not made at one instant. For k=5 Mpc⁻¹ the largest signed contribution to the **archived-velocity diagnostic displacement** is from epochs **1836–1991: 45.41%** (47.33% on baseline). The maximum combined tested spread in that contribution is about 0.07 percentage points of the final MTS discrepancy. Epochs 448–625 and 625–1827 contribute 25.83% and 25.49%; the nine longer intervals 1827–1836 contribute 3.14% net. Some velocity contributions cancel by large factors: displacement percentages are not velocity or energy fractions. These shares use both measured field endpoints and the derived retarded propagator: they locate the net effect without assuming the force is known inside those intervals.

For the much larger **physical** MTS displacement, there is also an independent forward calculation. On the supplied physical metric the new and archived homogeneous velocities give a *known* differential force, (φ′_phys−φ′_archive) C,x/5, starting from equal perturbations. With no post-initial native scalar input, its retarded integral predicts the physical-minus-native displacement to **2.59×10⁻⁶ relative**, with tested spread **1.89×10⁻⁷**. This passes 2×10⁻⁵. The velocity is close but misses the same gate: 1.16×10⁻⁵ discrepancy plus 1.10×10⁻⁵ spread. On baseline the background-velocity term is tiny and explains neither total discrepancy; this is a useful contrast, not a baseline win on observational data. On MTS, 41.62% of the integrated physical displacement contribution comes from 1836–1991 and about 19.70% from 1827–1836. These latter shares use the actual switched trajectory between the sparse **native** knots. They do not recover native substeps there.

## An independent metric source, tested across scales

The native growth number is for baryons plus CDM, not all gravitating matter. Combining its definition with the two continuity equations gives **C,x=(H/k)g D_cb+f_b v_b** in x=kτ. The source uses no differentiation of a rounded density. On all 2,262 directly captured metric derivatives in **each** cosmology, the directly tabulated D_cb version agrees within 4.15×10⁻⁸ relative and inside the predicted transfer-rounding bin. Using the actual unrounded captured matter state also reproduces the double-precision identity. This is a sampled force readout, not a measurement of universal matter growth between outputs.

We then predicted the pressure channel from this common drive, with **one initialization per contiguous sampling block**, using the archived backgrounds. All pressure values after initialization were excluded from forward forcing. Like-for-like counts are for k=0.03, 0.1, 1 and 5 Mpc⁻¹, at the same 2×10⁻⁵ tolerance, including integration, source-sampling and stored-value sensitivities. Each entry is a mode–epoch comparison, not a statistically independent observation.

| Calculated pressure | Dense intervals: passes / 15,140 | Sparse: passes / 1,868 | Zero-drive control, dense (even before uncertainty) |
|---|---:|---:|---:|
| Baseline slow | 14,965 | 918 | 0 |
| MTS slow | 14,008 | 726 | 0 |
| MTS heavy | 14,998 | 625 | 57 |

On the additional 15 disjoint high-k MTS modes: slow pressure passes **52,654/56,775** dense targets and heavy pressure **56,743/56,775**; sparse passes are **474/7,005** and **476/7,005**. The conditional pressure coupling transfers across scales when the metric input is resolved. It does not supply its own metric prediction in a long unsampled gap. See MULTISCALE.md, the five multiscale packets and verification.json. The four-mode comparison uses each source chunk's own background and avoids counting its k=5 mode twice.

## What can be bounded inside the gap?

Using the heavy perturbation as a second detector of the same metric force does **not** uniquely reconstruct the small slow-field residual. For epochs 1834–1835 (width 4.6366 in kτ), a smooth within-cell change in metric drive preserves the growth endpoints, CDM increment and both final heavy-field coordinates yet moves the terminal slow displacement. Independent quadrature checks the normalized heavy/dust nulls to below 5×10⁻¹¹ and its nonzero slow response to 10⁻¹² relative. This is non-uniqueness of an inverse calculation, **not** a second self-consistent solution of the complete field theory. The attempted heavy correction failed its small-residual forecast; it was not tuned.

The retained Einstein trace gives a sharper target than another interpolation choice. At fixed metric coefficients the hidden drive d obeys d′+h d=r, where r is the residual in half the normalized density-plus-three-pressure source. A varying background also contributes −Δh C′_S. After imposing the known endpoint constraints, the sharp L² gain from r in this cell to the terminal MTS displacement is **1.55403×10⁻¹⁴** in the saved normalization. An independent forward trace-plus-two-field solve reproduces the extremal response to 1.85×10⁻⁹ relative. The kernel-refinement spread is 3.90×10⁻⁶. The inferred sufficient single-cell rms limits are:

| Target at 1999, error ≤2×10⁻⁵ of that target | Baseline | MTS |
|---|---:|---:|
| Tiny archived-velocity displacement discrepancy | 5.52×10⁻¹³ | 3.35×10⁻¹³ |
| Physical-minus-native displacement | 5.53×10⁻¹³ | 1.29×10⁻⁷ |

These are requirements on **unexplained trace stress**, not observations that it is that small. They assume known endpoint constraints and concern one interval only. They also show why uncertainty in the tiny archive mismatch should not be mistaken for uncertainty of the same size in the physical MTS prediction. See TRACE-BOUND.md and the trace-bound receipts.

## Energy and numerical controls

For forcing error δF on a fixed expanding metric, the derived oscillator norm satisfies E(R)≤E(L)+∫|δF|/ω dx, E²=δu²+(δu,x/ω)². Its conversion to a scaled pressure bound is in MULTISCALE.md and SCALAR-WORK.md. The signed work − damping + changing-restoring-energy identity on the **difference mode** closes at the terminal epoch for both models. On MTS the difference from the independently saved terminal quadratic energy is 4.44×10⁻¹² relative (quadrature spread 4.01×10⁻⁸). The sign-blind pressure envelope at the endpoint is conservative by a factor of about 1,397 on MTS, 2,531 on baseline.

Four early samples (rows 2–5) lie outside the numerical quadrature envelope before refinement. This is larger than the final stored-state subtraction ulps alone. Passively reading the actual six solver stages and halving the step on the first eight intervals puts all eight inside the endpoint-sampled envelope in both models. The tiny early pressure itself still varies beyond tolerance between the finest levels; it is not used as evidence. The original sparse-source forecasts and their failures remain in the stage.

**Next physics test:** reconstruct the trace source from independently saved matter and radiation stresses and evolved parent fields. First validate its normalization and direct metric response where the derivative is recorded; then use the derived kernel to bound its effect across 1834–1835. Keep the slow response out of its own source test. If a species' pressure or the force between two knots is not independently bounded, isolate its allowed projected contribution rather than substituting a smooth curve. This goes after the stress that makes geometry respond, not another fit of the terminal pressure.
