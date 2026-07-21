# 4745 Y5 R2FR: Adjoint Principal Symbol UCP Ellipticity Gate Or CzeroMode Bound Runner

Generated: `2026-07-08T00:19:28+00:00`

## Summary

- Work is local-only and private.
- This checkpoint derives the minimal TFRI adjoint principal-symbol spine and blocks a common mistake.
- Static local tests may use an elliptic spatial/UCP/gap route **only** if that static reduction is parent-specified before scoring.
- Full Lorentzian dynamics is not uniformly elliptic because of the null cone, so it needs a hyperbolic energy route or a finite residual bound.
- Full owner ellipticity still needs the missing `sigma_TT` and `sigma_quar` parent components.

## Minimal TFRI Principal Symbol

```text
E_R[m] = rho_{mu nu} + eta g_{mu nu} - sym_0(nabla_mu lambda_nu) + lower
E_Gamma[m] = -nabla_nu lambda^nu + lower
E_phi[m] = H_T^dagger rho
         = nabla_mu nabla_nu rho^{mu nu} - (1/4)Box tr(rho) + lower

sigma_R(k)m = rho + eta g - i sym_0(k tensor lambda)
sigma_Gamma(k)m = -i k.lambda
sigma_phi(k)m = (k_mu k_nu - (1/4)g_mn k^2)rho^{mn}
```

Because this is mixed order, the correct test is Douglis-Nirenberg symbol injectivity on the admissible multiplier space.

## Symbol Rows

- `SYM4745_0_multiplier_vector`: m=(lambda_nu,eta,rho_mn,xi_nu,chi_nu)
- `SYM4745_1_R_block`: E_R[m] = rho_{mu nu}+eta g_{mu nu}-sym_0(nabla_mu lambda_nu)+lower
- `SYM4745_2_Gamma_block`: E_Gamma[m] = -nabla_nu lambda^nu + lower
- `SYM4745_3_phi_block`: E_phi[m] = H_T^dagger rho = nabla_mu nabla_nu rho^{mu nu}-(1/4)Box tr(rho)+lower
- `SYM4745_4_principal_symbols`: sigma_R(k)m = rho+eta g-i sym_0(k tensor lambda); sigma_Gamma(k)m=-i k.lambda; sigma_phi(k)m=(k_mu k_nu-(1/4)g_mn k^2)rho^{mn}
- `SYM4745_5_DN_weights`: Use Douglis-Nirenberg weights so algebraic rho/eta terms and first/second derivative blocks are judged together.
- `SYM4745_6_missing_full_owner_symbol`: sigma_TT(k;xi) and sigma_quar(k;chi) are MISSING_PARENT_COMPONENTS

## DN Ellipticity / UCP Gate

- `DN4745_0_static_slice`: STATIC_PPN_ELLIPTIC_SLICE_ONLY
- `DN4745_1_symbol_injectivity`: ker sigma_DN(D_adj)(x,k) cap M_adm = {0} for every spatial k != 0
- `DN4745_2_complementing_boundary`: H^1_0 or strong compact-support boundary data satisfy the complementing condition for the chosen static operator
- `DN4745_3_UCP`: DN ellipticity + regular coefficients + connected collar => UCP(D_adj,W_loc^space)
- `DN4745_4_gap`: compact W_loc^space + elliptic self-adjoint L_adj + kernel projected out => lambda_1^adj>0
- `DN4745_5_full_owner_gate`: TFRI block plus sigma_TT plus sigma_quar must all pass symbol injectivity

## Lorentzian Caution Audit

- `LOR4745_0_null_cone`: g^{mu nu}k_mu k_nu=0 has nonzero real k on a Lorentzian collar
- `LOR4745_1_no_gap_claim`: Do not infer lambda_1^adj>0 from a Lorentzian wave-type operator without converting to an elliptic/static or hyperbolic energy problem.
- `LOR4745_2_hyperbolic_route`: Use energy estimate on a time slab: E_m(t2) <= E_m(t1)+int source+boundary flux
- `LOR4745_3_static_tests`: PPN/R10/clock/orbital static limits may use the elliptic spatial branch if the parent specifies the reduction before scoring.

## Physical Kernel Audit

- `PK4745_0_tracefree_algebraic`: rho+eta g algebraic kernel
- `PK4745_1_lambda_killing`: lambda Killing/vector kernel
- `PK4745_2_harmonic_tracefree`: rho harmonic tracefree kernel
- `PK4745_3_TT_owner`: xi TT/superpotential kernel
- `PK4745_4_quarantine_owner`: chi quarantine kernel
- `PK4745_5_physical_bound`: C_phys_kernel

## CzeroMode Bound Runner

- `CZG4745_0_static_exact_case`: if STATIC_PPN_ELLIPTIC_SLICE_ONLY and DN gate passes and C_phys_kernel=0 then C_zeroMode=0
- `CZG4745_1_full_dynamic_case`: if Lorentzian branch only then C_zeroMode_dynamic is bounded by hyperbolic energy data, not set to zero
- `CZG4745_2_finite_runner`: C_zeroMode <= C_static_fail + C_phys_kernel + C_TT_kernel + C_quar_kernel + C_hyp_energy
- `CZG4745_3_amplitude_insert`: A_m <= sqrt(C_zeroMode^2 + (C_Dadj^2 + C_boundary)/lambda_1^adj)

## Route Matrix

- `ROUTE4745_0_static_PPN_gap`: derive static spatial elliptic operator and lambda_1^adj lower bound
- `ROUTE4745_1_full_owner_symbol`: write sigma_TT and sigma_quar parent components
- `ROUTE4745_2_hyperbolic_energy`: derive Lorentzian time-slab energy bound
- `ROUTE4745_3_score_now`: score local tests now

## Promotion Gates

- `GATE4745_0_sources`: pass_internal
- `GATE4745_1_symbol_spine`: conditional_pass
- `GATE4745_2_static_branch`: conditional_open
- `GATE4745_3_lorentzian_branch`: closed_unsigned
- `GATE4745_4_full_owner_symbol`: closed_unsigned
- `GATE4745_5_CzeroMode`: closed_unsigned
- `GATE4745_6_no_claim`: closed_firewall

## Decision

`ADJOINT_PRINCIPAL_SYMBOL_GATE_DERIVED_STATIC_ELLIPTIC_ROUTE_CONDITIONAL_LORENTZIAN_UCP_NOT_CLAIMED_CZEROMODE_BOUND_STAGED`

## Next Target

`4746-Y5-R2FR-static-PPN-elliptic-slice-gap-proof-or-lorentzian-energy-bound.md`
