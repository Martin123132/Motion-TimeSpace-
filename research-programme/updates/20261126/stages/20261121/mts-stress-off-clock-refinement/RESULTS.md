> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# The clock is not driving the tide; what the source test really distinguishes

**Local result, 21 November 2026.** On the two signed 960-cell/Mpc formations the unmodified parent tide meets the original Newton-plus-propagating-stress band on **32/32** readouts. Newton alone meets it on **8/32**. Restoring the stress and its conservation equations shifts the final temporal tide by about 92–94 ppm of the matched Newton magnitude; an independently evaluated mechanical forecast predicts that *change* to within 0.045 ppm on every readout. No gravitational coefficient was fitted. A common density/stress normalization works, but the density and propagating terms track one another so closely here that these runs cannot calibrate them independently.

### What changed when the clock was refined?

Two prepared host signs, the wave and its cold control, the same zero-host differences, same exterior bank, 3 Mpc domain, 960 cells/Mpc, both original proper apertures, four original observation times and both tidal readouts. No discarded centre cells. The native final-quarter restart reproduced all four saved endpoint fields bit for bit, before either clock refinement. On that quarter the largest half-step shift was 0.08690 ppm and the largest thirds-minus-halves difference was 0.06963 ppm. The thirds matter: native and half steps both sample a simple fast harmonic at identical phases, whereas thirds do not. See the [phase derivation](CLOCK-LIMIT.md).

Halving from formation instead changed any of the 32 **stress-withdrawn** readings by at most 0.05113 ppm; all stayed in the 20 ppm band. Final temporal residuals against the compensated Newton source were −10.0941/−8.2975 ppm on the negative host and +3.0574/+3.8837 ppm on the positive host (narrow/wide). The negative narrow case is diagnostic: −0.08690 ppm entered in the last quarter, and +0.03897 ppm was inherited, giving a net −0.04793 ppm. The observed 10 ppm offset did not disappear; nor does cancellation on this pair of clocks bound the continuum solution. The independent first-cell momentum defect divided by current at the full-half endpoint is 3.73/12.98 on the negative formation and 0.38/10.22 on the positive one (wave/cold). Aperture agreement is not pointwise constraint convergence. Clock budget (not bundled here) · [all clocks](evidence-001.zip) (archive member: `full-time-scores.csv`) · unmasked constraints (not bundled here).

### What changed when the physical stress was restored?

After the noncommensurate late-clock gate passed, the **unmodified** parent was evolved from the same initial state for each sign and matter branch. At all sixteen saved native physical states both spherical fields match the withdrawn evolution bit for bit. The additional effect is angular. The forecast was taken from the earlier independently integrated conserved density and current (not bundled here) and the retained retarded stress, frozen before the physical half-step runs. This is an additional numerical resolution on previously studied preparations, **not** a blind new formation or sky observation.

All entries below are signed ppm of |matched Newton|. P is the induced density tide. T is the propagating stress plus moving contact for the *difference*; the original absolute Newton-plus-stress benchmark does not add that contact.

| Host, aperture | Physical minus withdrawn | P | T | Measured − (P+T) | Physical − (Newton+propagating) |
|---|---:|---:|---:|---:|---:|
| negative, narrow | +92.101 | +33.664 | +58.474 | −0.037 | −10.131 |
| negative, wide | +93.759 | +33.959 | +59.837 | −0.037 | −8.336 |
| positive, narrow | −92.681 | −34.667 | −57.978 | −0.035 | +3.024 |
| positive, wide | −94.467 | −35.022 | −59.479 | +0.034 | +3.921 |

For the change, **no response: 0/32; density with its supplied normalization: 8/32; full prediction: 32/32**. These are correlated clocks/readers on two synthetic formations. The 0.045 ppm discrepancy is agreement of these computed differences, not an absolute accuracy assignment or a measured coupling. Frozen forecast (not bundled here) · all physical comparisons (not bundled here).

### Does this pin down two couplings?

No. Keeping the density coefficient at one, the measured remaining response divided by T ranges from 0.99768 to 1.00067. But the intersection allowed by the **actual 20 ppm** bands is 0.6651–1.3336, not that narrow measured spread. Allowing a single common scale on P+T gives 0.7880–1.2113. Allow both coefficients to move independently, and even density alone at 2.1720–3.2503 times its supplied value, or stress alone at 1.2537–1.9011 times its supplied value, can meet every band. Those alternatives are **not** authorized recalibrations of the parent; they show what these fixtures cannot discriminate. Two unrestricted directions have a singular-value ratio of 0.00893. We used 60-digit decimal strip intersections and an independent unbounded linear programme for the extrema, without fitting the physical prediction. [Definitions](SOURCE-NORMALIZATION.md) · feasible intervals (not bundled here).

### A physically different source rather than a better fit

We constructed two finite source-free electromagnetic preparations whose **energy densities are identical everywhere and at all times**, but whose cross-polarized stress and tidal fields differ. Their longitudinal current contrast vanishes. This removes the scalar-density degeneracy by source construction, not subtraction of a fitted template. On the Fourier mode kL=1 the normalized tidal acceleration is +0.2500 at launch, +0.6309 at t/L=0.75, and **−0.4139** at t/L=2, when the normalized instantaneous stress is still **+0.3668**: propagation can reverse the sign of the tide. This is a consequence of the leading common Einstein–Maxwell terms, not a distinctive observed MTS signal. The packet energies independently fix the stress normalization. Direct time integration and the closed retarded convolution differ by at most 1.56 × 10⁻¹⁵ in the recorded dimensionless metric. In the off-axis spatial reconstruction order 18 failed the 10⁻¹² null (worst 4.90 × 10⁻⁸); orders 24, 28 and 32 pass unchanged, all retained in the table. [Source, calibration and detector](MAXWELL-STRESS-SOURCE.md) · tensor history (not bundled here) · failed and passing orders (not bundled here).

There is also a **different** pair of exactly dual packets. Its entire canonical stress cancels in the difference, leaving a readout for the retained Weyl–photon coefficient after a scalar-curvature control. At fixed pulse energy and fixed detector-width/packet-width ratio, doubling the packet length divides that conditional signal by 32. This does not determine the coefficient from gravity or exclude ordinary QED matching. [Derivation](MAXWELL-DUAL-PACKET.md) · energy scaling (not bundled here).

**Next gravity test.** Inject the finite Maxwell stress and momentum into an independent, *unprojected* linearized common-metric evolution, not another calculation that begins by imposing the TT equation. Use identical differential gravitational constraint data at launch. The signed time curve, zero scalar-density difference, longitudinal constraint and cross-tidal readout are now predictions. The oblique toroidal momentum begins cubically with [a derived coefficient and sign](OBLIQUE-CURRENT.md); do not set it to zero by assumption. Keep the native matter-source check on the curved formations separate. No Galactic refit or Git action.

[Inputs, runs and verification](REPLAY.md).
