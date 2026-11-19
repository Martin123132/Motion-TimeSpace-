# Forest gravity: dropping the wave pressure fails, retaining its leading term works

**Answer.** At redshift 99 we gave both evolutions *exactly the same active field state and velocities*. Ordinary pressureless evolution is adequate on the larger tested scales but can almost double the forest-era gravitational force at 5/Mpc. Keeping the mass-derived dispersive term instead reproduces that force to **1.72×10⁻⁷ fractional** in the full linear hierarchy across the 24 tested modes and four forest epochs. It needs no new fitted coupling. This gives us a practical gravity input for a forest calculation; the gas-to-absorption calculation is separate.

## How big is the effect?

Worst fractional amplitude change from turning pressure off, expressed as percentages over z=5.4, 5, 4.6 and 4.2. U_b is the gas velocity convergence, F=−k²Ψ. Numerics used the original 2×10⁻⁵ check; 1% and 5% are separate physical approximation budgets.

| k (Mpc⁻¹) | Baryon density | U_b | Gravity F |
|---:|---:|---:|---:|
| 0.3425 | 0.0105% | 0.0151% | 0.0173% |
| 0.708505 (forest pivot) | 0.182% | 0.264% | 0.303% |
| 1.000 | 0.685% | 1.001% | 1.153% |
| 1.98096 | 6.635% | 10.456% | 12.465% |
| 5.000 | 30.959% | 64.650% | 93.790% |

Among the original sampled modes, all three channels pass 1% through 0.83536/Mpc, but not at the next mode, 1/Mpc; they pass 5% through 1.21881/Mpc, but not at 1.51247/Mpc. These bracket transitions on this history, not universal sharp cutoffs. Power errors are not amplitude errors: for example at 5/Mpc the largest squared-transfer change is +275.55%. The independently prepared all-cold arm shows **bit-identical outputs** on and off. It is not used as the initial state of the switched heavy arm.

## Why the force changes

Removing pressure changes the heavy current, then its density, then the potential felt by ordinary baryons. DERIVATION.md gives the causal current integral and CDM-relative density identity. Independent source integration closes to 2.28×10⁻¹³ and 1.57×10⁻⁷ respectively on the stated mode normalizations. Integrating the **metric acceleration** recovers the freely falling cold velocity to 1.17×10⁻⁷ fractional or better across the five arms. The remaining gas impulse is not mislabeled a gravity error. Clustered matter alone reconstructs the force to about 0.0444% in the worst forest case; restoring independently accessible radiation, massive-neutrino density, slow-field and photon shear sources reduces the largest remaining fraction to 1.07×10⁻⁶. This checks the same metric both as a source equation and as the acceleration of a test species, on these perturbations.

The alternative solver retains k²/(4a²m_h²) in the rest-pressure coefficient rather than setting pressure to zero. The coefficient differs from the full one by at most 5.57×10⁻⁶ after the switch. In the full hierarchy baryon density and velocity agree to 1.05×10⁻⁷ and 1.24×10⁻⁷ respectively. A wave-envelope momentum flux derived without dividing by density also passes independent periodic 3D momentum and expanding-energy checks, including exact interference nodes (worst normalized momentum residual 5.27×10⁻¹³). This tests the nonlinear **operator**, not a nonlinear forest spectrum.

## A forecast made before the second intervention

A stand-alone clustered-sector model took only the switch state, mass, density fractions and expansion, without future perturbation histories. We locked its predictions before computing the new z=49 pressure-off counterfactual. At 5/Mpc and z=4.2 it predicted a dust/wave force ratio **1.5677214**; the full hierarchy returned **1.5677343**. Across all three channels and four epochs, the largest absolute error in this predicted ratio was 0.0000358 for the z=49 start; the largest fractional error in an individual wave/dust field was 0.0670%. At z=99 those errors were 0.0000677 and 0.0748%. This is percent-level success, **not** universal 2×10⁻⁵ accuracy for a clustered-only solver. The known pressure-on history was not a blind observation; the new dust intervention was the withheld numerical outcome. A correction about the supplied dust history, tested separately, recovers all three wave fields to 0.0128% (z=99) or 0.0063% (z=49).

## Which actual forest scales are covered?

Used only the instrument labels, redshifts and k_v coordinates from the pinned [Hooper et al. likelihood](https://arxiv.org/abs/2206.08188). Before propagating any new radial mode, derived its initial matching data directly from the field. Of 49 HIRES/MIKE entries, 42 have radial minima within the trusted domain (24 distinct z,k pairs, not 42 independent theoretical modes). For those, only **14/42** radial entries pass the 1% pressureless approximation in all three channels; **21/42** pass 5%. Seven entries at the highest k_v start beyond 5/Mpc and were left unscored for *both* models. The corresponding four actual k_parallel are 7.0523, 7.3052, 7.5513 and 7.7909/Mpc. We have exact early-event packets at all four now: the earliest phase-switch variant fails the original 2×10⁻⁶ pressure check at three; the fourth passes all five local checks but is still beyond the qualified band. A later switch passing one of these checks is not by itself a reason to discard the earlier failure.

For the 42 supported entries we also integrated the **truncated linear density/velocity** response through k=5, including transverse modes. At z=4.2, k_v=0.0199526 s/km, the pressureless/wave power ratio of this proxy is 1.269–1.274 as the common nonnegative density/velocity weighting changes. This is **not a flux-power prediction**. Sampling variation reaches 1.97% across the 168 control matrices (154 exceed 2×10⁻⁵); within-panel quadrature alone is at machine precision. Missing transverse power, nonlinear gas, temperature/ionization, thermal broadening and biases still matter. No measured absorption powers entered this calculation and no observational score is issued.

**Next:** use forest-radial-inputs.npz to derive why the earliest phase switch misses the pressure at those four high-k modes. Predict the residual from the exact oscillating field and check at a separate matching epoch, then propagate the admitted modes to the gas and gravity. Extending the transverse range with qualified initial data matters more now than refining a dust model already known to fail. Keep the pressureless control and use the verified leading wave force for a paired nonlinear gas/absorption calculation once the inputs support it.

