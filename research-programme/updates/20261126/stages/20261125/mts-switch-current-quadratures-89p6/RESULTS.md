> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# A cycle of incoming current fixes the field at a velocity turning point

**The switch does determine the two components of the perturbed field in this preparation.** The missing information is carried by the preceding oscillation of current, not by dividing the instantaneous momentum by the tiny background velocity. With the retained microscopic forcing supplied, the reconstructed oscillating momentum accounts for the earlier large energy-work mismatch on fixed histories. The much smaller change relative to the original preparation does not pass.

## Which measurements determine the state?

Write the switch state in equally scaled variables (f,u/ω), with f the field perturbation, u its canonical velocity and ω=am. With the supplied energy, potential and current terms removed, the instantaneous observables are proportional to v u + ω² b f and k² v f. Near v=0 their instantaneous inversion loses a direction. The retained switch instead fixes instantaneous energy and a current corrected by the saved trailing half field oscillation (one full kinetic period). The two launches use the same historical calibration correction; the historical and live instantaneous seam values were not silently equated.

Propagating two basis solutions and an inhomogeneous solution backwards through the incoming metric, and integrating current per unit background phase, gives the following dimensionless observation matrices on the fine clock. The row scales are ω²A/ρ and k²ωA/ρ with A²=b²+(v/ω)²:
    
    instantaneous            retained energy + trailing current
    [-1.000000, 0.000308]     [-1.000000, 0.000308]
    [ 0.000308, 0.000000]     [ 0.000575, 0.500262]

The condition number drops from 10,567,267 to 1.999 on both clocks. At an exact harmonic turning point with b=−A, the second row tends to (0,1/2): it measures the velocity component that the density alone cannot see. No fitted prior or post-switch phase enters this inversion. The earlier saved interval used here is 89.05530582–89.14850380 conformal Mpc. Refining the inverse calculation changes the inferred live switch state by less than 0.000000028%. Compared directly to the unaveraged switch state, field and scaled-velocity errors are 0.000214% and 0.001272% on the fine clock.

## Direct tests through 89.6 conformal Mpc

We first froze both switch states, then the prediction for the difference in heavy momentum on the already frozen, different metric histories. Common supplied microscopic forcing cancels from these difference equations. We separately froze an absolute prediction using three prescribed input-bank columns (field source, momentum source, supplied current); these are available in the canonical microscopic bank but **not** in the averaged-fluid bank. Neither prediction uses the later field perturbation to fix its phase or amplitude. We then opened the reference wave. The updated wave replay reproduces its saved cycle-boundary states at stored precision.

| Full-window RMS error against own reference | Coarse gravity | Fine gravity |
|---|---:|---:|
| Conditional total heavy momentum | 0.000715% | 0.000714% |
| Conditional field momentum alone, without supplied current | 0.001141% | 0.001140% |
| Predicted change from original preparation | 2,450% | 19,265% |
| Error in that change, as % of total heavy momentum | 0.000445% | 0.000432% |

Why these results differ: on the fine clock the reference change has RMS 5.35×10⁻²³, only 0.00000224% of total current. The predicted change has magnitude 0.00043021% of total current, almost all metric driven. As complex time histories the frozen predictions change by 0.027% between gravity grids, but the **reference difference changes by 709%** relative to its fine value. The latter is not a continuum-resolved target; neither grid passes the 0.5% test for the difference. On each fixed grid cubic versus quintic interpolation of the original field contributes under 0.019% of that small target over the full window. Dropping the three noncoincident coarse time samples gives the same cross-grid verdict. An accurate total therefore cannot certify the incremental law.

## Link back to the energy-work problem

A diagnostic after scoring asks a different question: how well does the conditional calculation recover **wave minus averaged-fluid current**, the term implicated in the preceding stage? This is not wave minus the original microscopic preparation. The missing current is 83.48% of total wave current in RMS. The signed current waveform is reconstructed to 0.00086% relative on each clock. Inserting it only in the momentum readout, Δ(3Φ′)=3(J_reconstructed−J_averaged)/(2k²), reduces the gross kinetic energy-work error from 32.961% to 0.13015% on **both** clocks. All other histories are unchanged in this diagnostic. It is not a re-evolution of the metric, a new photon result, or an independent prediction of the three microscopic forcing inputs. The small prepared-subtracted energy-work signal still misses.

**Next:** make a numerically matched reference for the small momentum change. Launch two unaveraged evolutions from the same state with the same microscopic forcing, clocks and integration scheme; vary only the intended metric/stress history, evolve their difference directly, and require a zero-change null and gravity-step convergence before judging it. Keep the already-frozen prediction as the comparator, not a source. This distinguishes a physical response from the error of subtracting two different numerical histories. The reviewed paper and the production restart are unchanged.

[Derivation and frozen protocol](PROTOCOL.md) · [Conditioning](evidence-001.zip) (archive member: `conditioning.csv`) · [Switch validation](evidence-001.zip) (archive member: `switch-states.csv`) · [Direct field and momentum tests](evidence-001.zip) (archive member: `direct-tests.csv`) · [Clock sensitivity](evidence-001.zip) (archive member: `grid-comparison.csv`) · [Size of the small signal](evidence-001.zip) (archive member: `signal-scales.csv`) · [Fixed-history energy work](evidence-001.zip) (archive member: `fixed-history-current-readout.csv`).

Reproduction order in a fresh stage directory alongside the sealed parents: run infer_current.py, run_forecast.py delta, run_forecast.py conditional, release_current.py, momentum_readout.py and verify_current.py. The forecast adapter converts a returned metric pair to a numerical array; the release wrapper evaluates clocks on common support rather than assuming identical interior knots. These were interface fixes, not changes to the equations, forecasts or tolerances. For external background on the distinction between an oscillating scalar and its effective fluid, see [Passaglia and Hu](https://arxiv.org/abs/2201.10238); no external coefficient is adopted here.
