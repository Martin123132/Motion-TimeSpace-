# 4746 Y5 R2FR: Static PPN Elliptic Slice Gap Proof Or Lorentzian Energy Bound

Generated: `2026-07-08T00:24:12+00:00`

## Summary

- Work is local-only and private.
- This checkpoint turns the 4745 fork into two explicit proof/bound routes.
- Static local-test route:

```text
STATIC_PPN_ELLIPTIC_SLICE_ONLY
D_stat := spatial/static reduction of D_adj
L_stat := D_stat^* D_stat
lambda_1^stat >= c_DN/(C_P L_loc^2)
```

- Lorentzian dynamical route:

```text
E_m[t2] <= C_hyp(E_m[t1]+int ||D_adj m||^2 dt + Flux_boundary + Curv_coeff)
C_hyp_energy := sqrt(E_m[t2])/a_ref
```

- Static PPN/R10/clock/orbital arenas may pursue the gap law.
- Full Lorentzian local-GR dynamics keeps the energy bound.
- No local-test or local-GR claim is made until constants, projections, owner symbols and kernels are sourced.

## Static Operator Setup

- `STATOP4746_0_static_reduction`: STATIC_PPN_ELLIPTIC_SLICE_ONLY: W_loc -> Sigma_loc with Riemannian h_ij and parent-fixed lapse/shift/background fields
- `STATOP4746_1_domain`: M_adm^stat=H^1_0(Sigma_loc,E_m) cap Q_perp cap M_phys_allowed
- `STATOP4746_2_operator`: D_stat := spatial/static reduction of D_adj with time derivatives removed or algebraically constrained before scoring
- `STATOP4746_3_principal_symbol`: sigma_DN(D_stat)(x,p) = spatial part of sigma_DN(D_adj)(x,k) with p_i != 0
- `STATOP4746_4_laplacian`: L_stat := D_stat^*D_stat on M_adm^stat

## Static Gap Proof

- `SGP4746_0_DN_elliptic_assumption`: ker sigma_DN(D_stat)(x,p) cap M_adm^stat = {0} for every p != 0
- `SGP4746_1_Garding`: ||m||_{H^s}^2 <= C_G(||D_stat m||_{L2}^2 + ||m||_{L2}^2) on Sigma_loc
- `SGP4746_2_Poincare`: ||m||_{L2}^2 <= C_P L_loc^2 ||nabla_h m||_{L2}^2 for m in H^1_0
- `SGP4746_3_gap_bound`: lambda_1^stat >= c_DN/(C_P L_loc^2)
- `SGP4746_4_zero_kernel`: D_stat m=0 and gamma_boundary m=0 and C_phys_kernel=0 => m=0
- `SGP4746_5_static_amplitude`: A_m^stat <= sqrt(C_zeroMode_stat^2 + (C_Dstat^2 + C_boundary_stat)/lambda_1^stat)

## Static Test Arena Mapping

- `ARENA4746_0_PPN`: PPN/static weak-field metric response
- `ARENA4746_1_R10`: short-range inverse-square/fifth-force local response
- `ARENA4746_2_clock`: clock/redshift quasi-static local response
- `ARENA4746_3_orbital`: quasi-static orbital weak-field response
- `ARENA4746_4_GW_dynamic`: gravitational-wave/dynamical local response
- `ARENA4746_5_EM_dynamic`: time-dependent EM/stress coupling response

## Lorentzian Energy Bound

- `HYP4746_0_energy_definition`: E_m[t]=||partial_t m||_{L2(Sigma_t)}^2+||nabla_h m||_{L2(Sigma_t)}^2+||m||_{L2(Sigma_t)}^2
- `HYP4746_1_energy_bound`: E_m[t2] <= C_hyp(E_m[t1]+int_{t1}^{t2}||D_adj m||^2 dt + Flux_boundary + Curv_coeff)
- `HYP4746_2_zero_dynamic_case`: If E_m[t1]=0, D_adj m=0, Flux_boundary=0, Curv_coeff controlled, then E_m[t2]=0
- `HYP4746_3_finite_residual`: C_hyp_energy := sqrt(E_m[t2])/a_ref
- `HYP4746_4_no_static_claim`: Do not replace C_hyp_energy by lambda_1^stat^{-1} terms

## Owner Symbol Completion Ledger

- `OWN4746_0_TFRI`: sigma_R/sigma_Gamma/sigma_phi
- `OWN4746_1_TT`: sigma_TT(k;xi)
- `OWN4746_2_quarantine`: sigma_quar(k;chi)
- `OWN4746_3_boundary`: boundary complementing symbol
- `OWN4746_4_physical_kernel`: C_phys_kernel or Pi_phys Pi_0 m=0
- `OWN4746_5_gap_constants`: c_DN, C_P, L_loc

## Residual Bound Law

- `RB4746_0_static`: C_res_static <= Pi_owner^stat sqrt(CzeroMode_stat^2 + (C_Dstat^2+C_boundary_stat)/lambda_1^stat)
- `RB4746_1_gap_insert`: lambda_1^stat >= c_DN/(C_P L_loc^2)
- `RB4746_2_lorentzian`: C_res_dyn <= Pi_owner^dyn(C_hyp_energy+C_TT_kernel+C_quar_kernel+C_boundary_dyn)
- `RB4746_3_score_gate`: score_ready=false until c_DN,C_P,L_loc,Pi_owner,C_phys_kernel,sigma_TT,sigma_quar are sourced

## Route Matrix

- `ROUTE4746_0_static_constants`: source c_DN, C_P, L_loc and boundary complementing data
- `ROUTE4746_1_owner_symbols`: write sigma_TT and sigma_quar parent components
- `ROUTE4746_2_lorentzian_energy`: turn schematic hyperbolic energy bound into sourced C_hyp_energy
- `ROUTE4746_3_claim_now`: claim local PPN/local-GR pass

## Promotion Gates

- `GATE4746_0_sources`: pass_internal
- `GATE4746_1_static_gap_law`: conditional_pass
- `GATE4746_2_static_scope`: conditional_open
- `GATE4746_3_lorentzian_energy`: conditional_open
- `GATE4746_4_owner_symbols`: closed_unsigned
- `GATE4746_5_numeric_constants`: closed_unsigned
- `GATE4746_6_no_claim`: closed_firewall

## Decision

`STATIC_LOCAL_TEST_GAP_BOUND_DERIVED_CONDITIONALLY_LORENTZIAN_ENERGY_BOUND_STAGED_FULL_OWNER_SYMBOLS_STILL_UNSIGNED`

## Next Target

`4747-Y5-R2FR-static-gap-constant-source-and-owner-symbol-completion.md`
