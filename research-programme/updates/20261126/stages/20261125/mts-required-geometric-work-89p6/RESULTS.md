> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# How much must U change to satisfy the two constraints?

25 November 2026 · retained matched mean-current state · 89.148503803–89.6 conformal Mpc · original photon launch. **The predicted U increments have the wrong time dependence to supply all the work required on this trajectory.** The discrepancy is about 6.47% of the frozen source's rate variation on either gravity step, although signed cancellations reduce the end-to-end discrepancy to about 0.88% of the net U increment.

| Full interval; four substeps per saved gravity cell | Coarse gravity | Fine gravity |
|---|---:|---:|
| Time-weighted RMS rate mismatch / frozen RMS rate | 6.4701% | 6.4737% |
| Largest local difference / that cell's own frozen increment | 19.6058% | 19.6296% |
| Original cells differing by more than 0.5% of their own increment | 1,152 / 1,156 | 2,305 / 2,312 |
| Minimum RMS rate mismatch under **any constant complex rescaling** of the frozen increments | 6.4118% | 6.4154% |
| Photon-weighted matched discrepancy / original small photon correction | 0.538991% | 0.538995% |
| Same minus the unchanged explicit reference wave | 0.826861% | 0.606614% |

The source-rate and photon percentages have **different denominators**. On the fine step, the two projected contributions from supplied and required increments have norms of 61.2734% and 61.2380% on the small photon scale. We subtract their complex vectors, not these norms. The resulting matched discrepancy agrees with the preceding independent matter calculation to 0.000125% of its joint vector norm. After subtracting the unchanged reference, the fine photon energy and current discrepancies are 0.606848% and 0.605804%. Neither step passes the original 0.5% precision gate; both total routes remain below the 0.163%-of-launch size limit. Time and angular controls pass. The matched vector changes by only 0.00082% of its fine value on gravity refinement; the comparison that includes the reference remains gravity-step sensitive. [Coarse source checks](evidence-001.zip) (archive member: `local-p16.csv`) · [fine source checks](evidence-001.zip) (archive member: `local-p32.csv`) · [photon gates](evidence-001.zip) (archive member: `photon-gates.csv`) · [signed projections](evidence-001.zip) (archive member: `work-projections.csv`) · [controls](evidence-001.zip) (archive member: `controls.csv`).

## How the requirement was obtained without supplying U

In the retained normalization, the energy constraint and momentum rate are

    U = D Φ + E/2 + 3 H J/(2 k²)
    Φ′ = J/(2 k²) − H Ψ + Fq,       Ψ = Φ + (shear − Q)/k².

Only the original left matter state and potential of each gravity cell are supplied. We evolve twelve matter variables and Φ together; Φ is advanced from momentum, not reconstructed from U. The photon–baryon state current is combined as eγ W before assembling total J, retaining both the heat and external momentum exchange. E and J include material and prescribed source terms. The background, surrounding quadrupoles, Q, Fq, 77-bin stress and external drives are the saved ones. No U values are passed into the integration or work equations. The state continues across internal substeps, with splits at the original source corners, and resets to the retained left state at the next original cell.

The required work per substep is obtained independently of the measured U increment:

    ΔU_req = D_R ∫Φ′ dη + Φ_L ΔD + ΔE/2 + 3 Δ(HJ)/(2 k²).

We use the finite product identity Δ(Ax)=mean(A)Δx+mean(x)ΔA to separate state evolution, changing weights, and external work. Direct endpoint reconstruction checks the sum. Both gravity steps and both substep resolutions were frozen and hashed before the scoring phase. The read-once input loader authenticates the old geometry; the prediction interface drops U. A separate verification replaces that channel with nonfinite values at every predictor evaluation and checks that the required increments and all terms are bit-identical. This tests data flow, not whether the prior research was historically blind. The left states and imported surroundings still come from that research. No inferred value is supplied to MTS.

For scoring we use (ΔU_frozen−ΔU_req)/D_R as the potential-equivalent impulse. This is a **diagnostic on fixed inputs**, not the output of a modified self-consistent evolution. It independently recovers the old matched discrepancy. We use the same two-stage photon transfer with within-step weights and recover the half-/quarter-cell results and the archived control on both clocks. [Frozen protocol](PROTOCOL.md) · [required-work derivation and implementation](evidence-001.zip) (archive member: `required_u.py`) · [freeze manifest](evidence-001.zip) (archive member: `frozen.json`) · [transport checks](evidence-001.zip) (archive member: `photon-comparisons.csv`).

## What this rules out

- **One coefficient cannot repair the waveform on this trajectory.** Projecting required-minus-frozen increments orthogonally to the frozen increments in the rate RMS norm gives a lower bound for *every* constant amplitude and phase. It leaves 99.10% of the fine mismatch norm. No coefficient was fed back into the calculation. [Shape bound](evidence-001.zip) (archive member: `shape-bound.csv`).
- **The known forecast error in the spatial-plus-flux correction is too small.** We independently compared the saved native wave-minus-matched geometric correction with the frozen forecast, using its original log-time interpolation. The native adjustment is 0.259% of the missing-work RMS norm on the fine step; after photon weighting it is only 0.0259% of the matched discrepancy norm. Its signed effect slightly enlarges the mismatch at fixed states. The original interpolation extrapolates from its first native knot at 89.15 back to the switch; the source bound also holds using only original cells fully inside the native coverage. This is not a test of *all* possible geometric terms or a rerun replacing the wave.
- The result identifies a quantitative constraint between geometry and matter. It **does not uniquely assign the error to U**: a missing matter-work term, a background approximation or the matching procedure could also change the requirement.

**Next discriminating test:** repeat the blind balance requirement on the **unaveraged explicit wave with its own background, scalar stress and source U**, then compare the two signed work errors on common cells and photon weights. The saved wave packet contains its potential/rate histories, stress clock and final 91-variable state, but not every internal matter state; first reconstruct and verify that trajectory against the wave's own saved readouts. This control distinguishes a shared constraint mismatch from one introduced by matching. Do not insert the U required here into either branch.
