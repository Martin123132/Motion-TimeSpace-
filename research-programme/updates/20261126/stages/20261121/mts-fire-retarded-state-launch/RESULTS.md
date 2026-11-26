> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# Carrying the wave forward changes the Galactic shell correction

**Private research · 21 November 2026.** We evolved the first relativistic state correction from FIRE snapshot 590 to 600 (22.190427 Myr) rather than choosing it at the endpoint. The leading waves and total occupation are unchanged. On both archived time grids the evolved wave increases the matched time-potential correction and **reverses the sign of the spatial correction**. The largest term is the coupling between kinetic energy and the wave's own Newtonian potential, not the free dispersion term. The strongest unresolved input for this test is the part of the clock potential that *differs* between histories.

### The two computations being compared

Same spherical three-radius force combination as the [previous stage](../mts-fire-normal-energy-shell/RESULTS.md); units m/s², self-gravitating inherited wave **minus** self-gravitating reset. These are force corrections on simulation-informed histories, not proper accelerations measured at any single location.

| Quantity | Canonical correction zero **at 600** | Started zero **at 590**, 9 steps | Started zero **at 590**, 18 steps |
|---|---:|---:|---:|
| Wave-history contribution | 0 by construction | +2.030e−19 | +2.042e−19 |
| Total conditional spatial correction | −5.016e−20 (fine) | +1.528e−19 | +1.540e−19 |
| Total conditional time correction | +3.530e−20 (fine) | +2.383e−19 | +2.395e−19 |
| Spatial minus time | −8.546e−20 (fine) | −8.555e−20 | −8.546e−20 |

The new term enters both metric potentials equally: it is the induced rest-density perturbation. The calculation includes its self-gravity during evolution. Of the net +2.042e−19, the kinetic/self-potential term supplies +1.520e−19 (74.5%); ordinary-potential/kinetic and free dispersion supply +4.152e−20 and +3.588e−20. The three local potential-product terms collectively subtract 2.527e−20. The single arms' state contributions are −1.146e−17 and −1.126e−17, so the matched result is a difference of larger values. Reconstructing normalized endpoint waves after removing the arbitrary global phase confirms the linear density readout at physical amplitude. Drive breakdown (not bundled here) · fine history (not bundled here) · finite-state check (not bundled here)

**Condition on this number:** we set the still-unsupplied part of the lapse drive to zero when transporting the correction, not when evaluating the endpoint constraints. In particular, gravity sourced by the induced wave density is included exactly once to this order. Common ordinary densitized matter and stress are held as in the earlier shell test. The initial zero is a conditional preparation 22 Myr earlier, not the entire formation history. This calculation is not new data evidence for MTS versus another model.

### A bound on the missing clock potential, not a fitted clock potential

The reverse calculation gives the signed response to a lapse perturbation at every time, radius and angular node. It distinguishes a potential shared by both arms from a potential *difference*, with exact finite-grid bounds for restrictions on its value or on its radial force. For example, the minimum maximum radial acceleration of the omitted lapse whose **effect on wave evolution alone** could equal the fine conditional time correction in magnitude is:

| Allowed radial field | Same in both histories | Coupled minus reset, with the mean held fixed |
|---|---:|---:|
| Static | 2.758e−15 m/s² | 1.727e−17 m/s² |
| Can vary during interval | 1.877e−15 m/s² | 1.158e−17 m/s² |

Thus the matched test is about **160 times more sensitive to a static radial difference** than to the same static radial perturbation shared between histories. These are worst-case signed gradient profiles on the grid, not measurements or claims about what gravity actually supplies. The differential column does not include a separate *direct* endpoint force from an externally imposed metric. The static differential threshold was 1.732e−17 on the coarser run. In contrast, the fully unrestricted shared space-time gain changes from 1.29e−20 to 1.90e−20 m/s² per dimensionless unit half-range when time resolution is doubled: **do not treat that bound as continuum-converged**. The known retarded contribution changes by 0.57%. Gradient and amplitude bounds (not bundled here) · transfer between grids (not bundled here)

Holding the missing lapse fixed, the fine backward calculation also finds that a different, freely chosen number-preserving preparation of the *coupled* wave alone at 590 could cancel the conditional time correction at first order for a fractional wave-amplitude change of 1.259e−9 in its most effective direction. The earlier state is not thereby determined or adjusted. The saved initial gradients and both lapse kernels can be used directly with a physically specified earlier state and source, without optimizing to the answer.

### Checks that discriminate between error sources

- Both leading endpoint waves reproduce the original archives (phase-aligned normalized error ≤2.7e−12); number derivatives tested separately. Forward evolution and the backward response agree for all three drives. A smooth radial and a time-varying angular test were prescribed before the comparison.
- At 600 the direct short-step response tends to the independent native shell-current prediction +2.339e−21 m/s² per Myr (fine). Carrying tiny wave increments separately before the fourth derivative lowers the final relative discrepancy to 1.57e−7; the continuum surface vs native-current difference previously measured (~0.059%) remains. The launch **rate** is not extrapolated over the whole interval.
- Direct signed nonlinear runs on the fine time grid hit subtraction noise as the imposed test lapse gets small. Evolving the same finite positive/negative perturbations as even/odd waves resolves the discrepancy: the matched derivative error decreases from 1.14e−6 to 4.48e−9, and the original raw comparison remains saved. This tests an actual independent nonlinear spatial perturbation, not the whole PN Hamiltonian at finite coupling.
- The largest native kinetic eigenvalue has εK ≈ 24: a low-velocity series is not uniform on this grid. Less than 1.7e−20 of saved wave norm has εK>0.01 at the sampled step endpoints. More importantly, replacing just the quartic dispersion drive by the exact free positive-frequency dispersion difference changes the full matched state contribution by 1.26e−7 relative on the fine grid (2.42e−7 coarse). The much shorter instantaneous dispersive current is more sensitive; this isolated check is not a bound on every relativistic correction.

**Next derivation:** calculate the *differential radial lapse* along this interval from the matter and geometric terms of the same two Einstein constraints, starting with the traceable monopole. Contract it with the saved differential kernel. Preserve any unresolved interior/exterior modes, nonspherical sources, ordinary stresses and preparation as explicit terms or bounds; do not replace them with an endpoint-fit amplitude. This tests whether the sign change survives the wave's own clock-potential response.

[Equations and discrete adjoint](DERIVATION.md) · [frozen protocol](PROTOCOL.md) · checks (not bundled here) · file hashes (not bundled here). Local replay: with the same Python, NumPy/SciPy and the predecessor archives, run each with the -B option and no save argument. For each of 32 and 64, run evolve.py, launch_checks.py, paired_control.py, kinetic_check.py and increment_onset.py with that number. Then run lapse_bounds.py, paired_susceptibility.py, finite_state.py and verify.py without a number. Outputs are compared, not overwritten. No prior research bank or public repository was changed.
