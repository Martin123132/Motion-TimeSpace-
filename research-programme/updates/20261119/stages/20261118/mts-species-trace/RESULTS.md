# What actually drives the shared metric?

Private MTS parent calculation, 18 November 2026. Baseline is the retained cold preparation; MTS includes the heavy bath. Same k=5 Mpc⁻¹, bank and 2×10⁻⁵ comparison tolerance, no fits or native CAMB reruns. These are numerical cosmologies, not observations.

**The archive contained a real inconsistency in how its background sources the Einstein trace. Evolving the background fields and their velocities together removes its dominant cause.** The physical effect is highly channel-dependent: the metric is little changed on the tested interval, but the MTS slow-field pressure is not interchangeable with its archived value.

## Which stress supplies gravity?

Seven species slots reproduce the directly saved density, current and derivatives. CDM supplies most of the trace: its MTS RMS contribution is 6.22×10⁻⁵, versus 2.14×10⁻⁶ from the heavy scalar. The unadjusted density-plus-three-pressure trace passes all 2,262 baseline clocks but only 6/2,262 MTS clocks. Differentiating the Hamiltonian constraint with the actual tabulated background and separately derived species-continuity terms recovers **2,262/2,262 on each**. MTS uncorrected RMS defect is 2.36×10⁻⁷; the background term alone has RMS 2.36×10⁻⁷. The two largest contributions are the homogeneous heavy-field acceleration and field–velocity interpolation defects. This diagnosis does **not** promote that defect to a new source of gravity. Equations and per-species data: EQUATIONS.md, cold-direct.json, heavy-direct.json.

## Inside the old gap (1834–1835)

With plasma and slow fields initialized at 1833 and collisionless/metric/heavy variables fixed independently at 1991, neither endpoint of the gap supplies targets to the solve. The MTS slow displacement and velocity recover both held-out endpoints to better than 1×10⁻⁷ relative; heavy displacement to 4.44×10⁻⁶. The weakest MTS endpoint is the small photon density (up to 0.443% relative); it is not relabelled a pass. On the nearby 1991–3040 control, 1,048 interior trace values withheld per branch give maximum absolute error below 1.85×10⁻¹² for both. Raw right-hand sides are cross-checked separately in 100 complete states per branch.

The revised MTS trace differs from the prior nominal history by 2.05×10⁻⁷ RMS, **above** the old sufficient worst-case criterion of 1.29×10⁻⁷. Its *signed* projection, calculated from the resolved shape, is −7.42×10⁻²⁴: **0.172% of the allowed error** on the physical MTS displacement, but about **661 times** the allowed error on the far smaller archive-emulation discrepancy. The baseline uses a much tighter physical target (~5.53×10⁻¹³ RMS); the signed revision reaches 116% of its allowance. Do not infer a baseline pass. The physical MTS result benefits from the sign/shape of the forcing, not from dropping the difficult epochs. Integrating the stress and integrating the metric drive by parts agree within 3.1×10⁻³⁰ for MTS after resolving interpolation knots. The tested MTS boundary/mesh spread plus maximum control error is 3.40×10⁻¹² in trace units, not a theorem covering arbitrary hidden initial photon moments. Details: both mixed and projection JSON records.

## A physical check, separate from reproducing the archive

From **one complete saved state** at 1991, advance the background, matter, and radiation forward to 3038 without later pressure/metric input. Run twice: the metric is sourced by the Hamiltonian density constraint or by the independent pressure trace equation. Half-step refinements, a raw five-node quadrature control and the retained enthalpy correction are saved. The old archived-background Hamiltonian run reproduces the saved MTS slow pressure to 9.1×10⁻¹¹ of its peak, so the new difference is not a failure to implement the old calculation.

| Test over the window | Baseline | MTS |
|---|---:|---:|
| Peak metric-drive difference between the two physical Einstein evolutions / peak drive | 7.30×10⁻¹⁴ | 3.42×10⁻¹² |
| Peak slow-pressure difference between those evolutions / peak physical slow pressure | 1.45×10⁻¹² | 2.52×10⁻¹¹ |
| Largest fractional change in background ℋ from enforcing field evolution | 2.03×10⁻¹⁴ | 2.10×10⁻⁸ |
| Peak change in physical slow pressure / peak archived slow pressure | 4.68×10⁻⁸ | **1.1212** |

The pressure is a very small signed scalar channel, not the total pressure of the universe. Its MTS peak change is +1.26×10⁻²⁹ in native stress units. The exact product decomposition assigns 98.76% of that change at its peak to the **evolved perturbation velocity**, 0.82% to the homogeneous velocity in the instantaneous stress, and 0.42% to perturbation displacement. A change of background therefore affects the accumulated perturbation response, not just the last conversion into pressure. The baseline shows why the MTS pressure cannot simply be assumed robust. There is no sky fit here.

**Resume:** cold-epoch3038-restart.npz and heavy-epoch3038-restart.npz hold the new forward states, including both metric evolutions and physical homogeneous data; the previous epoch4252 restarts remain untouched. Next: carry the self-consistent Cauchy states from 3038 to the previously saved endpoint, compare the pressure and photon stress to the independent earlier physical preparation, and separate preparation memory from locally regenerated pressure. Reuse the archive as a control, not as a required physical answer. The single-cell inverse problem is only conditionally resolved; do not spend the next stage fitting its hidden angular tail.
