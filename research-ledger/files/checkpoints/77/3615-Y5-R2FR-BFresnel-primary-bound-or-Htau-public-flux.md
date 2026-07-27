# 3615 Y5 R2FR: B_Fresnel primary bound or H_tau public flux

## Verdict
- Primary-source observational analogue data were acquired for the `B_Fresnel` / principal-Hodge birefringence arena.
- The acquired rows are **not** an MTS pass: they constrain a published dimensionless LIV birefringence parameter `xi`, not a parent-owned MTS coefficient.
- The live next target is now a real derivation step: map `Delta_chi_principal_MTS` into the GRB polarization/Fresnel arena via a sourced `K_Fresnel` and norm, or move to the `H_tau` public-flux fallback.

## Source acquired
- Source: Jun-Jie Wei, *New Constraints on Lorentz Invariance Violation with Polarized Gamma-Ray Bursts*, arXiv:1905.03413.
- URL: https://arxiv.org/abs/1905.03413
- Local extracted source: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\external\arxiv_1905_03413\ms.tex`
- Model anchor: circular-polarization dispersion uses a dimensionless `xi` and predicts energy-dependent polarization rotation.
- Bound anchors: GRB 061122 gives `xi < 5.2e-17`; GRB 140206A gives `xi < 1.0e-16`, both at 68% C.L. in the source table.

## Bound rows
- `P8_Y5_R2FR_3615_BFRESNEL_PRIMARY_BOUND_ACQUISITION.csv` records two positive numeric dimensionless bound rows.
- Every bound row is marked `valid_for_claim=false`, `claim_allowed=false`, and `score_ready=false`.
- This is source plumbing, not a local-GR/R10/EM claim.

## MTS translation gate
- Current MTS target from 3614: `B_Fresnel := ||G_chi(k)-rho(g_EM^{ab}k_a k_b)^2||_arena`.
- Required bridge: `B_Fresnel_MTS <= K_Fresnel |Delta_chi_principal_MTS|`.
- Missing parent-owned inputs: `K_Fresnel`, the projection norm, energy/redshift arena matching, and a sourced MTS parent coefficient.
- Until those exist, the bound is a useful external boxing ring, not a scorecard win.

## H_tau fallback staged
- Fallback is not activated because a real `B_Fresnel` source was acquired.
- If projection stalls, the staged fallback is `I_EH_stationary_boundary` or `I_matter_EM_flux` inside the `C_curl`/`H_tau` denominator route.

## Next target
- `3616-Y5-R2FR-BFresnel-projection-runner-or-Htau-flux-reduction.md`.
- First attempt: derive/source the `K_Fresnel` projection law.
- Backup attempt: theorem-zero or source-bound the public EH/matter-EM Hamiltonian flux term.

## Claim status
- `NO_CLAIM`: the new rows are private robustness scaffolding.
- A claim only becomes possible after a parent-owned projection maps MTS variables into the acquired observational bound arena.
