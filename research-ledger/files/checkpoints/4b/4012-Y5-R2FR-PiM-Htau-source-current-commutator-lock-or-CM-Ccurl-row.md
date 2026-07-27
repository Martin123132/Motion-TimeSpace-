# 4012 - Pi_M/H_tau Source-Current Commutator Lock Or C_M/C_curl Row

- Timestamp: `2026-07-01T20:46:09+00:00`
- Status: `private_nonclaim_checkpoint`
- Scope: `post-checkpoint-work` only; no `formalization-workbench` edits.

## Result

The clean route is now a parent constraint-map theorem, not an empirical `GM` definition:

`Pi_M^C := D_N[C_tau]|_{J_H[tau]}`

`Delta_charge := M_H[Pi_M^C J_H] - (H_tau[S_outer]-H_ref)`.

If `Pi_M^C` is parent-selected, fixed as a chain map, `H_tau` is exact, `M_H_ref` is q-basic, the constraint map has no homogeneous mass kernel, and exact/boundary/EM terms have owned zero-flux accounting, then `C_M=0`, `C_curl=0`, `[d,Pi_M]J_H=0`, and `R_eq=0`.

This is a genuine derivation path to calibrated source coupling. It is still not a public Newton/local-GR claim, because the parent signatures are not all adopted and the EM/Poynting source term remains live.

## Charge-Glue Vector

If the theorem branch is not adopted, the retained vector is

`epsilon_charge_4012 <= |C_M|+|C_curl|+|I_commutator|+|R_eq|+|C_ref|+|C_frame|+|C_units|+|R_kernel|+|R_extra|+|R_symp|+|R_boundary|+|R_EM_flux|+|epsilon_G_norm|+|epsilon_PPN_source|`.

No fitted orbital `GM` is allowed to define the charge it is supposed to test.

## Evaluator Results

- `CASE4012_0_full_charge_lock_signed`: charge=`CONDITIONAL_PIM_HTAU_SOURCE_CHARGE_LOCK`, commutator=`C_M_C_curl_I_commutator_R_eq_ZERO_IF_PARENT_BRANCH_SIGNED`, local_GR=`NEWTON_SOURCE_CHARGE_CONDITIONAL_NOT_FULL_PPN_CLAIM`, next=`move to Maxwell/Poynting once-only Hilbert stress and then second-order PPN source stability`
- `CASE4012_1_constraint_map_open`: charge=`CHARGE_LOCK_BLOCKED`, commutator=`R_kernel+R_extra`, local_GR=`NO_LOCAL_GR_PROMOTION`, next=`retain R_kernel+R_extra as finite nonclaim rows`
- `CASE4012_2_chainmap_open`: charge=`CHARGE_LOCK_BLOCKED`, commutator=`I_commutator`, local_GR=`NO_LOCAL_GR_PROMOTION`, next=`retain I_commutator as finite nonclaim rows`
- `CASE4012_3_Htau_curl_open`: charge=`CHARGE_LOCK_BLOCKED`, commutator=`C_curl`, local_GR=`NO_LOCAL_GR_PROMOTION`, next=`retain C_curl as finite nonclaim rows`
- `CASE4012_4_MHref_qbasic_open`: charge=`CHARGE_LOCK_BLOCKED`, commutator=`C_M+C_units`, local_GR=`NO_LOCAL_GR_PROMOTION`, next=`retain C_M+C_units as finite nonclaim rows`
- `CASE4012_5_same_charge_open`: charge=`CHARGE_LOCK_BLOCKED`, commutator=`R_eq`, local_GR=`NO_LOCAL_GR_PROMOTION`, next=`retain R_eq as finite nonclaim rows`
- `CASE4012_6_EM_once_open`: charge=`CHARGE_LOCK_BLOCKED`, commutator=`R_EM_flux`, local_GR=`NO_LOCAL_GR_PROMOTION`, next=`retain R_EM_flux as finite nonclaim rows`
- `CASE4012_7_G_PPN_open`: charge=`CHARGE_LOCK_BLOCKED`, commutator=`epsilon_G_norm+epsilon_PPN_source`, local_GR=`NO_LOCAL_GR_PROMOTION`, next=`retain epsilon_G_norm+epsilon_PPN_source as finite nonclaim rows`
- `CASE4012_8_numeric_pack`: charge=`FINITE_CHARGE_GLUE_PACK_NONCLAIM`, commutator=`C_M+C_curl+I_commutator+R_eq+EM_G_PPN_VECTOR_REQUIRED`, local_GR=`NO_LOCAL_GR_PROMOTION`, next=`fill source-backed charge, curl, commutator, EM-flux, G-normalization and PPN-stability rows`

## Verdict

4012 moves the coupling problem forward: the source mass can be made the same object as the Hamiltonian charge only through a parent constraint-map lock. The live physics bottleneck is now concrete: EM/Poynting/binding energy must enter the Hilbert source exactly once.

## Next Target

- `4013-Y5-R2FR-Maxwell-Poynting-Hilbert-stress-once-only-lock-or-IEM-row.md`
- `scripts/Y5_R2FR_4013_Maxwell_Poynting_Hilbert_stress_once_only_lock_or_IEM_row.py`

## Source Count

- source needles found: `43/43`
