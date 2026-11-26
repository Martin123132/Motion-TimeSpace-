> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# A finite-time wave-current test at 89.1485038 Mpc

**24 November 2026 · saved histories only · k = 0.3368801156243423 Mpc⁻¹.** The oscillating part of the measured momentum does not die at the switch. Its phase winds and its signed contributions largely cancel over a stress period. Following the mean, the raw current and their difference with the momentum equation reconstructs all three histories at both gravity steps. All tested photon corrections remain below the unchanged **0.163% of the original joint launch**. This is a threshold result for the tested histories, not a unique physical damping law or a new cosmological fit.

## What the wave actually does

The first full post-switch stress cycle takes 0.0930865 conformal Mpc. Four complete pre-switch and four complete post-switch cycles fit inside the saved overlap used here. From the last pre-switch cycle to the fourth post-switch cycle, the within-cycle oscillating RMS on p32 rises from 1.79400e-11 to 1.79882e-11 (0.27%) on the photon launch; on the other seed it rises by 0.24%. This is not evidence of damping. On the first post-switch cycle of the photon launch, the real and imaginary mean momenta are −6.394e-12 and −1.003e-11. The four signed contributions to the **change** over that cycle, in units of 1e-15, are expansion (+7.64,+12.00), pressure (−0.38,−7.62), lapse (−4.64,−6.89) and remaining source work (−5.58,−8.43). They sum as vectors, not as powers.

For a trailing one-cycle readout starting with the instantaneous entry value, the mean's conformal-time derivative is the phase speed times the difference between incoming and outgoing momentum samples, divided by π. Independently integrating the force terms gives the same rate. Over the entire post-switch interval the independent reconstruction of the oscillating remainder misses by at most **0.0078% of its excursion** over the two seeds and two steps. No period, phase shift, decay time or amplitude was fitted. [Derivation and conventions](DERIVATION.md) · [p32 cycles](evidence-001.zip) (archive member: `cycles-p32.csv`) · [signed impulses](evidence-001.zip) (archive member: `impulses-p32.csv`) · [integrated checks](evidence-001.zip) (archive member: `integrated-current-checks.csv`).

## What reaches the photons

Full visibility-window RMS of the complex energy/current correction relative to the explicit-wave history, as percent of the original joint launch. The baseline stays fixed. The primary gravity drive uses the momentum constraint; the last column checks it by independently differentiating the curvature at the finer step.

| MTS stress used with matched surroundings | p16 | p32 | p32 differentiated |
|---|---:|---:|---:|
| One trailing cycle, continuously initialized | 0.00364770 | 0.00364773 | 0.00122345 |
| Two trailing cycles | 0.00621210 | 0.00621216 | 0.00283419 |
| One cycle with progressive start | 0.00346808 | 0.00343977 | 0.00121130 |
| Fully resolved wave current | 0.00003017 | 0.00003016 | 0.00003384 |
| One-cycle current with pressure and energy from balance | 0.00362576 | 0.00362576 | 0.00365679 |

The largest joint correction over the tested readouts, steps and transfer variants is **0.00621216%**, a factor of 26.2 below the threshold. That margin is not being used to waive any precision test. In the balance-derived case, the p32 full MTS-minus-baseline RMS is 3.67483864% versus 3.67464838% for the explicit control at 89.6 and 3.83768420% entering at 83.2; the earlier cancellation survives. The original 77 momentum bins, amplitudes, opacity, visibility, both gravity steps, numerical tolerance and endpoint were retained. [Photon readouts](evidence-001.zip) (archive member: `photon-window.csv`) · [independent scoring](evidence-001.zip) (archive member: `independent-readouts.csv`).

## Why the pressure check matters

Simply filtering all heavy stresses gives a **46.11%** disagreement between the two local metric rates at the switch for the one-cycle readout. This persists under step refinement. Instead, preserving the resolved external work and shear and prescribing just the measured coarse current fixes the pressure and density changes from conservation. This reduces the maximum metric-rate discrepancy to **1.342%** at both steps, still above the **0.5%** gate. The required pressure is not the directly averaged wave pressure. The resolved wave with those same matched surroundings already gives a 1.057% discrepancy; subtracting that control leaves a peak excess of 0.0424% of the resolved full rate. That subtraction is diagnostic, not an absolute pass.

On the same explicit-wave surrounding sources, the control gives 0.2884% (resolved) and 0.3619% (balance-derived) absolute metric-rate discrepancies, both passing. Keeping the one-sided interpolation rule while using the explicit-wave sources gives 0.3619% again at p32. Thus changing the surrounding inputs matters; this is not just a one-sided interpolation artifact. Those controls do not identify which of the surrounding source terms is responsible. The two photon-rate routes still differ by 0.868% of the small balance-derived correction vector at p32 with matched inputs (1.084% at p16); the correction is not measured to 0.5% relative precision.

Other retained failures: coarse fully resolved source-energy check on both seeds; gravity-step checks on the progressive and resolved small photon correction vectors. The independently computed adjoint photon transfer agrees with the forward transfer to 2.5e-14 relatively at the peak. Full individual gates, including the different normalizations, are in [verdict.json](evidence-001.zip) (archive member: `verdict.json`), [metric diagnostics](evidence-001.zip) (archive member: `metric-rate-diagnostics.csv`), and [wave-surroundings photon controls](evidence-001.zip) (archive member: `null-readouts.csv`).

**Next:** at the saved time of maximum residual near 89.35 Mpc, decompose the two metric constraints by species and quadratic source, comparing matched and wave surroundings on the same interpolation stencil. Determine which term breaks the total balance before extending the interval. No physical endpoint restart was promoted; all previous stages are intact.
