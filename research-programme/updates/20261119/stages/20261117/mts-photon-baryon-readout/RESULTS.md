# Photon/baryon predictions extracted from the coupled repair

Completed2026-11-17, private and local. No evolution rerun, fit, new collision source, bank/grid change or tolerance change. This stage uses the previous coherent histories rather than starting a replacement model. Read readout-result.json, native-transfer-result.json, velocity-attribution-result.json, verification.json and TRANSFER-CONVENTIONS.md.

## Actual advance

The corrected source's effects on photons, baryons and gravitational potentials are now calculated from their ALREADY coupled states. Standard frame transformations are checked against the retained CAMB symbolic implementation. Relative-density and photon/baryon drag equations are derived from the actual native hierarchy and tested against saved derivatives.

This is a single retained Fourier mode k=5 Mpc^-1 over a=0.0002233978..0.0002267397, around redshift4409..4475. Values retain the original native initial-mode normalization. They are transfer readouts, not measured sky amplitudes or a comparison to DES/BAO data.

## MTS output changes

Change is the coherent-repair minus interpolated-reference result. Normalized maximum changes use each ORIGINAL934-state observable amplitude, frozen before corrected evaluation. They are not percentages at every time or near a zero crossing.

| Quantity | Maximum absolute change | Representative interpretation |
|---|---:|---|
| Synchronous photon density contrast | 4.15132e-10 | Below old2e-5 output envelope |
| Newton-frame photon temperature-like monopole | 1.22081e-10 | Below old output envelope |
| Newton-frame baryon density contrast | 3.95091e-10 | Below old output envelope |
| Relative baryon/photon density S_bg | 3.12052e-11 | Resolved in retained numerical comparison |
| Photon/baryon velocity slip | 8.96724e-12 | Full outputs converge; tiny RESPONSE remains unresolved at2e-5 relative precision |
| Actual native Weyl potential | 7.96695e-13 | 1.22895e-8 of its reference amplitude |
| Actual native Newtonian baryon-velocity transfer | 3.08819e-7 | 4.46118e-5 of reference amplitude:0.00446118%, outside old2e-5 envelope |

The baryon-velocity change is small but exceeds the OLD numerical envelope by about2.23 times. It is a reproducible change caused by repairing an inconsistent history, not a fit improvement or a failure of the corrected solver. Future use of that transfer must carry the corrected value rather than claim the old prediction is unchanged.

All full-output32/64 refinements pass the unchanged2e-5 gate, for both baseline and MTS. Most MTS changes also resolve relative to their own small size. All tiny baseline response-relative tests remain unresolved, including background temperature/opacity; their absolute output refinements pass. Do not turn a numerical floor into an exact-zero or convergence claim.

## Derived velocity attribution

For the actual exported velocity V=-k(v_b+sigma)/H, the exact finite response is
```
Delta V=-k Delta(v_b)/H_star-k Delta(sigma)/H_star
        -V_old Delta(H)/H_star.
```
At the final physical query the MTS contributions are:
- Fluid velocity: +1.31296593e-7.
- Metric shear: -2.32528708e-7.
- H normalization: -4.91202854e-11.
- Total: -1.01281235e-7.

These are signed cancelling contributions, not probabilities or independent positive error bars. The metric response dominates this endpoint change, with a partial fluid counter-response; it is not mainly a background normalization effect. Both cases pass the unchanged algebra gate and reproduce this attribution exactly on replay.

## Important potential convention

The first result's column weyl is the KINEMATIC potential obtained from the actual sigma derivative. It changes by1.57264e-7 for MTS, mostly because the old geometry did not obey the spatial-pressure equation. That is NOT the size of the change in the solver's historical exported Weyl transfer.

The native code exports k^2 times the STRESS-derived Weyl potential, W_native=-(D+3HQ/k+Pi)/(2k^2). Saved observer values verify this definition without another run. Derived exact bridge:
```
W_kin-W_native=R_shear/(2k)-C00/k.
```
The old MTS discrepancy is1.57257e-7; the coherent discrepancy is8.29793e-12, or1.28000e-7 of the native Weyl scale. The corrected native Weyl output itself changes only7.96695e-13.

That residual implementation difference is larger than the tiny native-Weyl repair response. Therefore numerical reproducibility of the latter is NOT proof of a physically resolved lensing signal at1e-8 precision. Both versions and the failed old kinematic envelopes remain recorded; no result is replaced to obtain a better score.

## Gas and radiation scope

Homogeneous gas temperature follows the retained RECFAST branch T_m=T_CMB/a: final MTS fractional change=-2.13576348e-11, opacity change=-4.27152696e-11. Both satisfy the derived map and refinement test. There is no independent gas-temperature perturbation in this retained branch.

These are frequency-integrated photon moments. No mu/y spectrum or frequency-resolved distortion has been produced here. The historical signed902-node projection is retained only as a preparation diagnostic, not mislabelled as an observational kernel. Source correction is transmitted through the common metric, not injected as an invented Compton/emission term.

The earlier full preparation-pressure budget remains87.5966% of its cap, unchanged. That is a SOURCE budget, not automatically a complete uncertainty bound on every photon/baryon observable. This stage's readout allowances cover measured step changes and a stated working arithmetic envelope, not all parent, discretization, initial-state or astrophysical uncertainty.

## Verification and preservation

Twelve symbolic/interface checks,128 readout/arithmetic controls across the paired cases,36 native-convention/bridge checks, two velocity-attribution checks and41 consolidated checks pass. Original-state norms and all cached arrays/reports/CSV replay exactly. All492 frozen paths and the previous472 sealed artifacts remain unchanged. The original metric-stage weak-control flag and inherited tiny-baseline failures are retained.

Eight numerical/checking worker identities verified exited; foreground verification also completed. No bytecode, live worker, server, browser, subagent, GitHub, relay, scheduler action or changes to another chat. The main goal remains active. These readouts are still not complete corrected native-state restarts.

Next: use the derived Newton-frame baryon force balance to check how the velocity correction accumulates, with pressure, photon drag and exact metric endpoint work separated. NEXT.md supplies the equation and a cancellation-safe integral form; do not rerun the same readout stage.

