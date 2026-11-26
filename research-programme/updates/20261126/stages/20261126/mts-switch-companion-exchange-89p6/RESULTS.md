> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# The incoming pressure history predicts the switch correction at fixed curvature

**Result.** The retained phase-average preparation predicts a complementary current with the correct sign and a **0.25954% complex-amplitude error relative to the entire required switch correction** on both gravity grids. The density increment was fixed to its saved initial value of zero; neither it nor curvature was adjusted. The pressure and initial rate of density change are also recovered at the original 0.5% tolerance. These are tests of the initial condition for one Fourier mode and one prepared perturbation, not of the subsequent gravity rate.

## Derivation from incoming work

Use the saved current variable j = J_h/ρ, where ρ = ρ₀/a in the code’s conformal normalization, and the pressure p in the same normalization. A prime denotes conformal time; H is the conformal expansion rate. The saved exchange equation is j′ = −Hj + k²p + k²Ψ + s_j. The split is the retained one, not a decomposition into independently observable forces. The current mean is over one **stress** period, π in background phase. At the switch θ=0, averaging j(θ)−j(0) and exchanging the order of integration gives

    j_c = mean(j) − j(0)
        = − ∫[-π,0] [(θ+π)/π] [−Hj + k²p + k²Ψ + s_j]/θ′ dθ.

All four work terms were formed from the saved incoming field, its derivative, the background oscillator and the prescribed force functions. For the supplied source we used the saved expression involving hJ′, hJ, hfield, henergy, htrace and the lapse, not a residual inferred from the joint metric. Only prefix samples enter the primary integral; the original known switch oscillator fixes the background phase. The last incoming stress period was 89.055305821–89.148503803 conformal Mpc. We did not infer a phase, amplitude or coefficient from the needed compensation.

On the preparation’s common reference metric, subtracting the instantaneous current equation from the mean-current equation with the same supplied exchange gives

    j_c′ = θ′[j(0)−j(−π)]/π − j′(0),
    p_c = (j_c′ + H j_c)/k²,
    e_c(0) = 0,     e_c′(0) = −j_c − 3H p_c.

Here e_c is the additional normalized density for this preparation; zero is its *prescription*, not a universal boundary condition. The prediction in the fixed-curvature constraint is C = ρ e_c/2 + 3Hρ j_c/(2k²). Pressure affects the constraint through its prior work on the current, not by inserting a pressure term into the instantaneous density constraint. The test target was −R_wave, taken after freezing both forecasts from the previous sealed *full* metric readout, including ordinary matter and all 77 bins. The small density difference of that readout was not subtracted from the target.

## Signed tests

| Test (percent; original gate 0.5%) | Coarse p16 | Fine p32 |
|---|---:|---:|
| Complex error / full compensation required | 0.259540 | 0.259539 |
| Current error / required change in heavy current | 0.041326 | 0.041326 |
| Pressure error / saved complementary pressure | 0.244132 | 0.244131 |
| Initial density-rate error / right derivative of saved density | 0.239103 | 0.239138 |
| Offset left after accounting, as % of launch scale | 0.00088937 | 0.00088934 |

On p32 the predicted C was (−1.6820695 + 2.6155840 i) × 10⁻¹⁶; the required C was (−1.6819056 + 2.6236708 i) × 10⁻¹⁶ in the saved constraint units. The prediction supplies **99.78438% along the required complex direction**. The initial offset was 0.342660% of the launch scale. The two subdivision readouts on each grid agree at the switch; they are not independent histories.

The projected work contributions on p32, as percentages of the **required** correction, are pressure +99.80919%, drag −0.00259%, lapse +0.00990%, and supplied exchange −0.03212%. Omitting pressure gives 100.025% error; keeping the exchange term alone gives 100.032%. Reversing the prediction’s sign gives 199.784%; predicting zero gives 100%. The relevant signal is a pressure-driven memory of the incoming oscillation. A smooth instantaneous transfer into another sector is not indicated: integrating the supplied exchange over the final 0.001, 0.0005 and 0.00025 conformal Mpc gives only 0.0201%, 0.0110% and 0.00576% of the required current magnitude, tending to zero for a bounded source.

## Independent numerical checks and limits

The two primary forecasts differ by 0.0005901% of the fine forecast; 48 vs 96 integration nodes changes either forecast by less than 0.00000060%. Integrating the reconstructed current itself rather than its momentum equation reproduces the primary integral to within 0.000000019%. A separate post-score calculation used the older archived wave kernel and its interpolation rather than the one-sided reconstruction: it predicts the entire switch correction to 0.24450% on both grids and attributes 99.798% along the required direction to pressure. That comparison reuses the same underlying data; it is not an independent observation. Two right-sided stencils for the saved density-rate comparison agree within 0.000017%.

This derives the **stress complementary to the resolved wave in the retained averaged preparation**. It is not a new matter species, a surface impulse, or evidence that a fully microscopic parent must choose this preparation. Adding it again to the already averaged fluid would count it twice. The incoming microscopic force bank remains an input. No prior state, gravity integration, photon readout or tolerance was changed.

**Next test:** propagate the derived complementary current, pressure and density through the first stress period with continuous curvature. Couple their stress exactly once to the total metric on the resolved-wave side, and subtract any part already in the supplied matched closure. Freeze both gravity-route rate predictions before comparison with the saved 0.5% rate test. The switch result justifies testing that evolution; it does not by itself fix the earlier 0.770% window-wide rate discrepancy.

[Protocol](PROTOCOL.md) · [Frozen predictions](evidence-001.zip) (archive member: `forecast.json`) · [Signed comparisons](evidence-001.zip) (archive member: `scores.json`) · [Archive and density-rate controls](evidence-001.zip) (archive member: `crosscheck.json`) · [Previous joint switch result](../mts-matched-joint-77-switch-89p6/RESULTS.md). The score wrapper evaluates the mathematical zero-prediction control as exactly 100% after checking the original floating-point result within 3×10⁻¹⁴ percentage points; the frozen predictor, physical scores and tolerances were unchanged. Reproduce locally with Python 3.13, NumPy/SciPy, one numerical thread and -B: junction.py freeze, score_switch.py, crosscheck.py, verify_switch.py (as separate Python invocations).
