> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# The saved preceding wave cycle changes the photon signal, but not the disagreement

Replacing the missing part of the first trailing average with the actual preceding wave history increases the fine-grid joint photon gap from **0.5763610063% to 0.5763616532%**. The comparison is signed before the norm, with no fit or phase adjustment. Both gravity steps tell the same story: constant padding did not cause the 0.5% miss in this window.

| Primary readout | Coarse | Fine |
|---|---:|---:|
| Old joint gap, % of original small momentum-route correction | 0.5763499845 | 0.5763610063 |
| Revised joint gap, same units | 0.5763506314 | 0.5763616532 |
| Revised energy gap, % | 0.57657174 | 0.57658244 |
| Revised current gap, % | 0.57558126 | 0.57559339 |
| Revised momentum route, % of original **launch** | 0.01901927 | 0.01901930 |
| Revised differentiated route, % of original **launch** | 0.01904000 | 0.01904003 |

**The initialization matters for a different quantity.** On the fine clock, the magnitude of the change in the entry current is 68.84% of the old entry-current magnitude. Holding physical heavy energy continuous changes the constrained starting potential by 0.34237% of its old magnitude. Transporting that common entry kick, the changed potential rate and the lapse moves the differentiated-route size from 0.003648% to 0.019040% of the original launch. Both physical routes remain below their separate 0.163% size limit. A large common shift is not a large change in the disagreement between routes.

**Where the disagreement accumulates.** The first full stress cycle ends at 89.24159032 conformal Mpc. On the fine grid, sources before that point contribute **12.11%** of the final signed joint gap along its direction; later sources contribute **87.89%**. The old padding control gives the same split to two decimal places. Transported alone, the *later* contribution has norm **0.509730%** on the original common scale, already above 0.5%; the coarse result is 0.509720%. These are source-time slices of a continuous trajectory, not a claim that a late-time cause is independent of earlier states. The original simulation interval still ends at 89.6 Mpc.

**Checks.** The signed correction was frozen before opening the control photon histories. All **87** numerical comparisons passed the original 0.5% tolerance, including reconstruction of the previous photon result, signed sums, substeps, two independent ways to compute the current-window rate, and photon-time, angle and gravity controls. The coarse/fine difference is 0.000605% of the small correction vector and 0.00214% of the revised joint gap. All 12 independent launch-channel projection checks agree to better than 3.3×10⁻¹⁴ relative. The physical 0.5% gap gate still misses for energy, current and joint in all six grid/settings combinations. This is a conditional calculation on saved histories, not an observation or a reason to promote a new restart.

**Next discriminator:** keep the initialization fixed. Over the remaining complete stress cycles after 89.24159032 Mpc, separate the net change of the constraint per cycle from the oscillation within that cycle. Carry each through the same signed photon weighting; retain the final incomplete cycle explicitly. This can distinguish accumulated cycle-to-cycle drift from oscillations that fail to cancel in the readout, without fitting a parameter or running a new cosmological interval.

[Derivation](DERIVATION.md) · [Protocol](PROTOCOL.md) · Frozen sources (not bundled here) · Frozen photons (not bundled here) · Control (not bundled here) · [Gates](evidence-001.zip) (archive member: `gates.csv`) · [When the photon work occurs](evidence-001.zip) (archive member: `windows.csv`) · [Numerical checks](evidence-001.zip) (archive member: `checks.csv`).
