# 5110 - E020-primary complex-control derivation

Checkpoint 5109 rejects the upper-sheet imaginary-zero route, but zero mean was never required for a valid complex multilevel control.

Let

- `A = R_primary(E020)`,
- `B = R_primary(E040)`,
- `H = 2A-B`,
- `C = A`.

With fixed `beta=1` in every real and imaginary channel,

`E[H-C] + E[C] = E[A-B] + E[A] = E[2A-B] = E[H]`.

This identity is componentwise over the complex numbers, has numerical residual `7.105427357601002e-15`, and needs neither reflection symmetry nor `E[Im C]=0`.

Using the four completed high events only as design data, the fixed ratio `N_low/N_high=3` gives a projected cost-normalized score `0.7462906810169911`, below the old `0.8` gate. The bottleneck remains `imag_z-0.3`. Four high plus twelve E020-primary controls project to `9.94395049986113 h`, of which `5.021066679416702 h` is new work.

The route is promising but borderline: deleting one high event gives a maximum design score `0.8000294913775439`. A ratio near `3.81` is more leave-one-out stable (`0.7580201125618966`) but exceeds the ten-hour budget at current control cost. Therefore this is a design-conditioned continuation, not an independent efficiency result.

The design lock fixes `beta_real=beta_imag=1`, ratio `3`, the existing four high seeds, the twelve locked low seeds, the `<0.8` score gate, and the ten-hour total cap. It authorizes implementation of a restartable control-only runner, but not numerical execution until that runner passes a dry-run and enforces the four-hour per-invocation cap.

Outputs:

- `scripts/Y5_R2FR_5110_E020_primary_complex_control_derivation.py`
- `source-intake/functional_rg/5110/E020_primary_complex_control_feasibility.json`
- `source-intake/functional_rg/5110/E020_primary_complex_control_design_lock.json`
- `source-intake/functional_rg/5110/E020_primary_complex_control_channels.csv`
- `source-intake/functional_rg/5110/E020_primary_complex_control_allocation_sensitivity.csv`
- `source-intake/mts_residuals/P8_Y5_BRR545_5110_VALIDATION.csv`

No fixed-point or MTS physics claim follows from this estimator design.
