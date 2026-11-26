> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# A single complementary stress brings both gravity rates inside 0.5% for the first oscillation

From 89.1485038031 to 89.2415903205 conformal Mpc, adding the part of the current and density carried by the phase average reduces the fine momentum-route rate error from **0.757584% to 0.193725%**. The density-route error increases from **0.183397% to 0.193730%**, still well within tolerance. The improved momentum result survives both gravity clocks and both step subdivisions. The previously reported 0.769540% was for the longer interval ending at 89.6, not the uncorrected first-period score.

| First-period RMS rate error | Coarse, unchanged | Coarse, with stress | Fine, unchanged | Fine, with stress |
|---|---:|---:|---:|---:|
| Momentum-driven gravity | 0.757588% | 0.193726% | 0.757584% | 0.193725% |
| Density-driven gravity | 0.183398% | 0.193731% | 0.183397% | 0.193730% |

Four subdivisions shown. Each error compares the derivative of curvature inferred from energy with the rate from the momentum equation on the **same** trajectory, normalized to the RMS momentum rate. The maximum sampled corrected discrepancy across all eight trajectory/grid/subdivision combinations was 0.30812% of this rate scale. Fine momentum-route curvature drift since launch fell from 0.51318% to 0.02725% of the actual curvature motion. Fine density-route drift went from 0.01850% to 0.02791%. Full-curvature discrepancies are 0.000917% and 0.000919%, respectively. These are internal consistency tests of one prepared mode.

## What was evolved, and why it counts only once

On each trajectory, j is the instantaneous heavy current divided by ρ = ρ₀/a, including the supplied microscopic current. Let m be the trailing current mean and θ the background phase in radians, zero at the switch. Over the first period the outgoing end of the average always samples the **incoming** history. We evaluated the pre-switch field and forcing without using later wave data, and evolved

    m′ = (θ′/π)[j_live − j_incoming(θ−π)],     j_c = m − j_live,
    p_c = (m′ − j_live′ + H j_c)/k²,          e_c′ = −j_c − 3H p_c.

The derivative of the live current comes from the oscillator, live field equation, normalization and supplied current derivative. The initial e_c is zero and the initial j_c is the preceding stage’s frozen prediction on each grid. The complementary pressure and energy follow the retained common-metric exchange equations, with no new background component, shear, density fit or independent external force.

The solver still uses the explicit heavy wave, not the old averaged-fluid evolution slots. It receives just ρ e_c in the energy constraint and ρ j_c in the current constraint and momentum evolution. Thus the heavy current that gravitates is ρ[j_live + (m−j_live)] = ρ m, not ρ(j_live+m). The inherited geometric and microscopic forcing and shear were left in place. Ordinary matter and the 77 momentum bins respond to each trajectory's own gravity at every integration substep. Both momentum integrations start at the original saved curvature. The density-driven route evaluates its algebraic constraint; its separate momentum integration is never reset. The slight 0.000889% initial constraint offset is retained, not forced to zero.

## Controls and restart

- With the extra source switched off, the same code reproduces the earlier saved first-period trajectories, including the left limit at the first source corner. The four predicted packets were frozen before scoring them against that control.
- We independently checked current addition, the phase integral, the pressure from the derivative of j_c, and density with the derivative-free balance [e_c+3Hj_c/k²]′ = [−1+3(H′−H²)/k²]j_c. The worst numerical control across all runs was 0.00000133%. The coarse/fine corrected rate residuals differ by 0.000237% or less of the fine residual at four subdivisions.
- The launch pressure on the live histories is within 0.245% of the independently predicted pressure from the preceding period. At the saved end, the live mean differs from the direct integral of the newly completed period by 0.05871% or less. The small inherited initial mean offset and the tiny difference between the saved corner and exactly π account for this; neither was removed or used for tuning.
- Each sealed period packet contains the end matter states, both gravity histories, all final bin and shape states, complementary density and mean, and each route’s phase-labelled instantaneous current across the period. Start from the last states, not the last readout alone. The tiny phase interval just before zero, if required at the next launch, still belongs to the incoming prefix. No state was propagated past the first source corner.

**Next:** advance through the second period. The delayed side of the mean must now remove samples from each route’s own first-period current instead of reusing the pre-switch wave. Keep the inherited mean and density, evaluate the correct side of the source corner, and check the second-period and cumulative rate errors before moving farther toward 89.6.

[Protocol](PROTOCOL.md) · [All rates, controls and refinements](evidence-001.zip) (archive member: `results.json`) · [Endpoint check](evidence-001.zip) (archive member: `endpoint.json`) · [Input switch derivation](../mts-switch-companion-exchange-89p6/RESULTS.md). Local only, with no photon fit or published update. To reproduce in a fresh stage copy with the same parent stages and environment: run period.py init, launch.py, score.py, endpoint.py and verify_period.py with Python 3.13, -B and one numerical thread. The launch wrapper points the inherited write guard at the new stage rather than the sealed parent; the initial guard stopped before any evolution and the original protocol did not change.
