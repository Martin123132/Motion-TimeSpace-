# Where the prepared wave and the averaged gravity calculation part company

**Do not promote the raw source substitution.** Densities and currents from a single coherent prepared wave reconstruct its microscopic state well, but inserting the resulting stress directly into the existing oscillation-averaged model makes its two gravity predictions agree **less** well. The cause can be localized: most of the new photon discrepancy enters through the heavy energy source between the switch at **89.1485038031** and the first subsequent native sample at **89.15 conformal Mpc**. The momentum prediction is nearly unchanged. The former model and the negative result are both retained.

## Frozen photon test

Only the heavy quadratic forcing was replaced. The common incoming energy/current, field state, 77-bin perturbations, pre-switch memory, two gravity grids, subdivisions, other metric and matter sources, scattering medium and original cold baseline were reused. Both the resolved and matched heavy histories were propagated on their respective metrics. Momentum and energy constraints give separate trajectories, not duplicate fits. All gravity outputs and both signed photon channels were frozen before scoring the full visibility distribution. The cold baseline was not recomputed or renamed as the resolved wave.

| Grid, primary transfer, four subdivisions | Previous cumulative joint gap | New cumulative energy | New cumulative current | New cumulative joint | New 89.65–90.4 joint alone |
|---|---:|---:|---:|---:|---:|
| p16 | 0.659717% | 35.227240% | 35.420007% | 35.270392% | 5.250161% |
| p32 | 0.659708% | 35.222129% | 35.414989% | 35.265302% | 5.250167% |

These are percentages of the **original small photon correction**, not of the CMB and not a sky-data residual. The pass threshold is 0.5%. On p32 the substitution changes the cumulative momentum-route vector by **0.00212%** of that reference and the density-route vector by **35.82063%**. The two corrections separately remain 0.018391% and 0.019526% of the full joint launch, below the separate 0.163% cap. Turning the companion stress off gives 501.72% cumulative joint discrepancy on p32; that is a control, not an alternative preferred model. Numerical controls: **144/144** pass on the prescribed reference, worst 0.17545%; across all 12 compensated settings the cumulative joint gap is 35.259–35.429%. Refining the original grids cannot account for this miss.

## What drives it

On the compensated branch the wave current plus its compensating stress is exactly ρw+ρ(m−w)=ρm. At fixed state the raw current cancels immediately, though it still changes future memory. A direct heavy energy change acts on the energy-route potential as δΦ=−δq_E/(2D); it does not appear directly in the independent momentum equation. This division follows from the retained equations, not a fit to the output. The first-period **equation** checks verify energy, field and momentum forcing, shear-induced lapse and curvature rate on both branches/grids to 5.6e−8% or better of the change. The actual propagated run uses the full bundle together. The resolved source has six slots; the matched host originally had only five dynamical heavy sources. We provide the sixth as its trace diagnostic, not as a second energy or pressure force.

We propagated the direct energy term, remaining forcing and state response through the original scattering operator. Signed contributions below project onto the **new** full joint photon difference in percentage points of the original small reference; these are not separately positive norms. Timing splits preserve the boundary state and do not inject a kick when switching integration bins.

| Contribution, p32 | Signed points |
|---|---:|
| Previous model's entire gap projected on the new difference | −0.55393 |
| New direct energy, switch to first subsequent knot | +32.49761 |
| New direct energy, rest of first period | +0.13993 |
| New direct energy, later periods to 89.6 | +1.03753 |
| New direct energy, 89.6–89.65 | +0.11277 |
| Other forcing and state changes through 89.65 | −0.09844 |
| New direct energy, 89.65–90.4 | +2.41845 |
| Late direct current and shear | +0.00113 and −0.00006 |
| Late response of the changed state | −0.28970 |
| **Total** | **+35.26530** |

On p16 the first cell contributes +32.50421 points. The full signed increment and its two photon channels reconstruct to below 1e−10% of the reference. This attribution holds with the existing frozen other forcings and histories: the residual category includes the effect of the changed trajectory and is not an independently derived new force.

**An endpoint test distinguishes a source mismatch from the shape of an interpolation curve.** The real incoming photon kick change is exactly zero. At 89.15 the conditional matched quadratic energy differs from the old source by −5.42434e−18 + 3.98249e−17 i in native units, versus +9.26820e−20 − 3.65149e−19 i in the resolved control. The resulting paired direct potential change is +2.41541e−17 − 1.75957e−16 i. We separately propagated just this potential change across the exact 0.001496197-Mpc cell. A straight ramp between the same endpoints reproduces its joint photon vector to **0.0393% / 0.0198%** on p16/p32. Treating the integrated energy drive as a single impulse at the right endpoint gives **0.0477% / 0.0340%**. Errors here are on the cell contribution's own norm. These are diagnostics, not boundary impulses inserted into the physical run. A different smoothing polynomial between the same sources is not the indicated repair.

## Independent controls, scope and next test

The resolved-wave gravity outputs reproduce all 14 archived channels on both routes through the three windows to at worst 0.001201% of the respective channel peak. The exact shared entry is reused on both branches. At the native knots the source-rate derivative agrees with the independently derived current equation within 0.00019% (wave) and 0.00213% (matched) of the peak rate. The reduced compensation identity in CURRENT-TRANSFER.md independently reproduces the *change* in the earned energy/current combination to 0.261% or better on all tested blocks/routes. All 120 late pieces retain exact predecessor hashes. The largest readout seam is below 1.7e−12%; no curvature resets or new phase preparation.

**Next physical calculation: derive the stress matching on the switch hypersurface rather than tuning the energy jump away.** Evaluate one-sided first-order field, normal momentum, induced metric, time slicing and their quadratic energy on the same clock; distinguish a genuine incoming/outgoing preparation change from a change of gauge or from averaging products versus multiplying averages. If Φ is continuous on the identified common slicing, the retained Hamiltonian constraint requires [E]+3[ℋJ]/κ=2[U]−2[D]Φ at the surface. Derive and test those terms separately before proposing a compensating energy or a new photon forecast. Do not enforce the identity by defining an offset from the failed readout. Keep the 0.5% gate, same episode, resolved control and the preceding 0.65971% branch as the reference.

## Reproduction and readout

The predecessor checksums are in source_pair.py. Use separate single-thread Python processes with the retained NumPy/SciPy environment: prefix_run.py; continuation.py bridge then late; photon_run.py bridge then late then score; verify_transfer.py; source_injection.py; diagnosis.py; direct_transfer.py; early_energy.py; cell_endpoint.py; finish.py. There were no fits or data downloads. The first source-routing preflight failed before any field step because it expected a dynamical trace slot on the matched host; prefix/method.json is its historical receipt, not an active freeze. The corrected run is bound to prefix/method-v2.json. The parent files were not rewritten. See late/paired-forecast.json for the pre-score receipt, late/scores.json and late/intervention.json for the comparison, late/substitution-work.json and late/early-direct-work.json for the signed decomposition, late/first-cell-check.json for the independent endpoint control, validation.json for verification and late/restart90.json for signed restart paths. This is a conditional perturbation test at the retained output k=0.3368801 Mpc⁻¹, not observational evidence for or against the full MTS framework.
