# Fixed-lag source history: one verified short advance

Manual step,2026-11-12. Goal remains paused. Reused the saved baseline/MTS preparation and completed eight-interval coupled continuations; no new evolution, fit, downloads, handover or publication. Original weights, banks, masses, normalization, output grids and2e-5 numerical/1e-10 algebra tolerances retained.

## What now works

The original902-node source history advances by actual conformal-time delays, with new source values supplied only by the current coupled solution. At the nine saved readout epochs,0..8 nodes respectively draw on the new continuation. Every other node still uses the available past. Each branch retains its own native clock at the same scale-factor indices.

54 per-source checks pass: initial readout, history/current join, same-interpolation native comparison,32/64 ODE comparison, interpolation refinement, cancellation-sensitive absolute-weight discrepancies, and withheld historical/current nodes. Fifteen independent controls pass, including polynomial reproduction, no extrapolation, exact cubic delay transport and a mutation test proving later continuation values cannot change earlier readouts. Six combined numerical-budget component checks pass; zero cold current/pressure remain exactly zero.

| Normalized historical source | Initial MTS | Final MTS |
|---|---:|---:|
| Density | -0.04703348837941416 | -0.04703686065518735 |
| Current | 0.03453137250179223 | 0.03451448074085888 |
| Pressure | -0.00025380812091127926 | -0.00025376283098371233 |

Cold historical density advances93.50727097122366 to93.51350205023556 under its own retained normalization. These branch-specific amplitudes are not observational fit scores or a direct superiority comparison.

The heavy pressure readout differs from the native-comparison readout by5.27e-11 relative and between32/64 saved evolutions by4.21e-10. Those comparisons SHARE the past interpolation; they are not independent validation of the entire historical curve. Separate withheld-node and interpolation-refinement tests address that limitation numerically.

## The remaining tight spot

The combined WORKING discrepancy budget for heavy pressure is4.34474e-9 absolute, or1.71182e-5 relative, against2e-5. It passes with limited margin (about86% of the allowed error). The recent-boundary Hermite interpolation allowance supplies4.05718e-9 of this budget; the old-history degree5/7 discrepancy supplies2.87413e-10. ODE-step and seam differences are much smaller. Tightening the ODE alone is therefore not the best next use of computation.

This is a discrepancy budget supported by withheld and refinement tests, NOT a certified bound on all numerical error. It does not cover common systematic errors shared by interpolation methods. Do not call its small native-comparison residual a complete error estimate or certify a compressed memory model from it.

## Useful negative controls

- Freezing the history fails the density check in both branches, and all three MTS source checks. The historical source genuinely changes over this short interval.
- Shifting saved row indices instead of preserving time delays passes cold and MTS-density checks, but misses MTS current by3.1238e-5 and pressure by0.0419948 (about4.20%). The nonuniform-time distinction matters; not every negative-control component fails.
- Degree3 versus7 readout still passes here. This is an interpolation sensitivity result, not permission to ignore the cancellation-aware budget.

## Physical and numerical scope

For source history S(t,ell)=Y(t-ell), partial_t S+partial_ell S=0 with boundary S(t,0)=Y_live(t). The implemented readout is sum_i w_i S(t,lag_i), lag_i fixed and nonnegative. This is a causal history of one solution, not902 physical fields. The original signed weights and full prepared source history retain the initial nonzero memory; the old averaged pressure is never inserted as an instantaneous field source.

This supplies a tested explicit-history reference over the saved eight early-time intervals. It does not yet reduce that history to a compact carrier/memory equation. Next, improve the recent-boundary interpolation check before testing such a reduction.

All files stay in this new private folder except the additive current-resume bookmark. No original checkpoints modified. Cleanup and hashes are recorded in closeout.json and CLEANUP-VERIFIED.json.
