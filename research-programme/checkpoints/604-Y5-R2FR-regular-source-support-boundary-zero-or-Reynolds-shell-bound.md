# 4588 - Regular source-support boundary zero or Reynolds shell bound

Marker: `PPC4161_REGULAR_SOURCE_SUPPORT_BOUNDARY_ZERO_OR_REYNOLDS_SHELL_BOUND_4588`  
Branch: `MTS_R2FR_Y5_REGULAR_SOURCE_SUPPORT_BOUNDARY_ZERO_OR_REYNOLDS_SHELL_BOUND_4588`  
Decision: `REGULAR_ZERO_TRACE_SUPPORT_KILLS_REYNOLDS_BOUNDARY_BIRTH_CONDITIONAL_SHELL_NORM_RETAINED_NONCLAIM`  
Private/public status: private nonclaim; no GitHub action.

## Result

4588 derives the support-boundary term instead of leaving it as a missing regularity phrase.

For any bounded arena/source test `phi`:

```text
I_phi(t)=int_W(t) phi rho_H dV.
```

The Reynolds transport split is:

```text
dI_phi/dt =
int_W d_t(phi rho_H dV)
+ int_partialW phi rho_H^tr V_n dSigma
+ <phi,mu_birth>.
```

The first term is the 4587 density q-basic object.  The live 4588 term is:

```text
E_boundary_birth ~ int_partialW phi rho_H^tr V_n dSigma + <phi,mu_birth>.
```

So the strict zero route is:

```text
rho_H^tr|partialW=0,  mu_birth=0,  fixed q-basic collar
=> E_boundary_birth=0.
```

If not signed, the finite bound is:

```text
E_boundary_birth <= Phi_A*(rho_H_trace_norm*V_n_bound + mu_birth_TV)/|M_H_ref|.
```

This is still not a local-GR claim.  It converts another source-worldtube blocker into either a theorem clause or sourceable shell norm.

## Reynolds theorem

| checkpoint | theorem_id | claim | derivation | consequence | status | generated_utc | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 4588 | RST4588_0_Reynolds_identity | The support-boundary term is exactly the Reynolds transport term for moments over W_H. | For I_phi(t)=int_{W_t} phi rho_H dV, dI_phi/dt=int_{W_t} d_t(phi rho_H dV)+int_{partial W_t} phi rho_H^tr V_n dSigma + <phi,mu_birth>. The first term was attacked by 4587; the second/third are E_boundary_birth. | The support-boundary problem is no longer vague: zero trace/no shell kills it, otherwise a boundary measure norm is required. | REYNOLDS_IDENTITY_DERIVED | 2026-07-06T13:04:10.899761+00:00 | False |
| 4588 | RST4588_1_zero_trace_support | If the Hilbert source density has compact regular support with zero trace and no birth/death shell, then E_boundary_birth=0. | On a fixed q-basic collar, if rho_H^tr|partial W_H=0, V_n is finite, and mu_birth=0, the Reynolds boundary contribution int_partialW phi rho_H^tr V_n dSigma + <phi,mu_birth> vanishes for every bounded shape/readout test phi. | Regular zero-trace ordinary sources have E_boundary_birth=0 and do not create an active source-worldtube kernel by boundary motion. | CONDITIONAL_ZERO_THEOREM_DERIVED_NOT_GLOBAL_PARENT_SIGNED | 2026-07-06T13:04:10.899761+00:00 | False |
| 4588 | RST4588_2_shell_bound | If zero trace or no-shell regularity is not signed, the fallback is a finite Reynolds shell norm. | For |phi|<=Phi_A on the declared arena, |D_v I_phi|/M_H_ref <= Phi_A*(int_partialW |rho_H^tr| |V_n| dSigma + ||mu_birth||_TV)/|M_H_ref| plus any q-basic bulk failures retained from 4587. | E_boundary_birth receives sourceable inputs: boundary trace density, normal support velocity, shell measure, arena test ceiling and M_H_ref. | BOUND_FORMULA_DERIVED_VALUES_MISSING | 2026-07-06T13:04:10.899761+00:00 | False |

## Zero clauses

| checkpoint | clause_id | clause | zero_condition | current_status | zero_certificate_signed | claim_allowed | valid_for_claim | generated_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4588 | ZSR4588_0_fixed_qbasic_collar | The source worldtube/collar is selected before variation and descends through q. | D_v collar=0 except support motion induced by the Hilbert density itself | CONDITIONAL_4580_284_ROUTE | Conditional | False | False | 2026-07-06T13:04:10.899761+00:00 |
| 4588 | ZSR4588_1_compact_regular_support | W_H has compact regular finite-perimeter boundary. | partial W_H has finite area and a well-defined normal trace | UNSIGNED_REGULARITY_PREMISE | False | False | False | 2026-07-06T13:04:10.899761+00:00 |
| 4588 | ZSR4588_2_zero_density_trace | The Hilbert density has zero boundary trace on the support edge. | rho_H^tr|partial W_H=0 | UNSIGNED_ZERO_TRACE_PREMISE | False | False | False | 2026-07-06T13:04:10.899761+00:00 |
| 4588 | ZSR4588_3_no_birth_death_shell | No new source layer is born or killed under the vertical probe. | mu_birth=0 | UNSIGNED_NO_SHELL_PREMISE | False | False | False | 2026-07-06T13:04:10.899761+00:00 |
| 4588 | ZSR4588_4_no_threshold_mask | The support is not a fitted threshold/readout mask. | W_H=closure(supp rho_H dV_H), not {rho>rho_cut from residual} | ANTI_CIRCULARITY_GUARD_REQUIRED | False | False | False | 2026-07-06T13:04:10.899761+00:00 |
| 4588 | ZSR4588_5_no_flux_sidewall | Sidewall/radiative flux is zero or routed as boundary Hamiltonian charge. | F_side[tau]=0; F_rad routed, not hidden bulk | CONDITIONAL_4176_ROUTE | Conditional | False | False | 2026-07-06T13:04:10.899761+00:00 |
| 4588 | ZSR4588_6_bounded_test_functions | Arena kernels have declared bounded test functions on the source boundary. | sup_partialW |phi_A|=Phi_A<infty | BOUND_SCHEMA_REQUIRED | False | False | False | 2026-07-06T13:04:10.899761+00:00 |

## Shell bound rows

| checkpoint | bound_id | symbol | definition | meaning | bound_formula | current_status | numeric_value_present | claim_allowed | valid_for_claim | generated_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4588 | RSB4588_0_trace_density | rho_H_trace_norm | int_partialW |rho_H^tr| dSigma | boundary trace of Hilbert source density | int_partialW |rho_H^tr| dSigma | MISSING_ZERO_TRACE_CERTIFICATE_OR_VALUE | False | False | False | 2026-07-06T13:04:10.899761+00:00 |
| 4588 | RSB4588_1_support_velocity | V_n_bound | sup_partialW |V_n| | normal velocity of support boundary under source probe | sup_partialW |V_n| | MISSING_SUPPORT_VARIATION_BOUND | False | False | False | 2026-07-06T13:04:10.899761+00:00 |
| 4588 | RSB4588_2_birth_measure | mu_birth_TV | ||mu_birth||_TV | distributional source shell/birth-death measure | ||mu_birth||_TV | MISSING_NO_SHELL_CERTIFICATE_OR_VALUE | False | False | False | 2026-07-06T13:04:10.899761+00:00 |
| 4588 | RSB4588_3_test_ceiling | Phi_A | sup_partialW |phi_A| | arena test/readout ceiling for source moment | sup_partialW |phi_A| | MISSING_ARENA_TEST_BOUND | False | False | False | 2026-07-06T13:04:10.899761+00:00 |
| 4588 | RSB4588_4_denominator | M_H_ref | |M_H_ref| | same-frame positive Hilbert source normalization | |M_H_ref| | MISSING_POSITIVE_MHREF_OR_VALUE | False | False | False | 2026-07-06T13:04:10.899761+00:00 |
| 4588 | RSB4588_5_total | E_boundary_birth | Phi_A*(rho_H_trace_norm*V_n_bound + mu_birth_TV)/|M_H_ref| | total Reynolds shell boundary birth envelope | Phi_A*(rho_H_trace_norm*V_n_bound + mu_birth_TV)/|M_H_ref| | FORMULA_READY_VALUES_MISSING | False | False | False | 2026-07-06T13:04:10.899761+00:00 |

## Reduction rows

| checkpoint | row_id | target | formula | branch_condition | status | generated_utc | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 4588 | RSR4588_0_Eboundary_zero | E_boundary_birth | E_boundary_birth=0 | fixed q-basic collar, compact regular support, rho_H^tr=0, mu_birth=0, no threshold mask, sidewall flux zero/routed | CONDITIONAL_ZERO_NOT_PUBLIC_CLAIM | 2026-07-06T13:04:10.899761+00:00 | False |
| 4588 | RSR4588_1_Eboundary_bound | E_boundary_birth | E_boundary_birth <= Phi_A*(rho_H_trace_norm*V_n_bound + mu_birth_TV)/|M_H_ref| | any regular support/zero-trace/no-shell clause unsigned | REYNOLDS_SHELL_BOUND_READY_VALUES_MISSING | 2026-07-06T13:04:10.899761+00:00 | False |
| 4588 | RSR4588_2_CKsource_update | C_K_source_worldtube | strict 4587+4588 branch removes E_rho_qbasic, E_EM_flux and E_boundary_birth; remaining blockers are E_Dq_source+E_tau_eobs+E_Href+E_readout_mask | density/Poynting zero branch plus regular support zero branch | PARTIAL_SOURCE_KERNEL_REDUCTION_DERIVED | 2026-07-06T13:04:10.899761+00:00 | False |
| 4588 | RSR4588_3_next_MHref | E_Href and M_H_ref | prove H_ref/M_H_ref source-blind q-basic positive normalization, or bound D_v H_ref and denominator drift | next most central denominator/coupling obstruction | SELECTED_NEXT_DERIVATION_TARGET | 2026-07-06T13:04:10.899761+00:00 | False |

## Controls

| checkpoint | control_id | case | expected_result | status | generated_utc | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 4588 | CTRL4588_smooth_zero_trace | smooth compact source with rho trace zero and no shell | E_boundary_birth=0 | SYMBOLIC_CONTROL_PASS | 2026-07-06T13:04:10.899761+00:00 | False | False |
| 4588 | CTRL4588_hard_surface_jump | sharp boundary with nonzero trace density or shell layer | retain Reynolds shell bound | COUNTERMODEL_CAUGHT | 2026-07-06T13:04:10.899761+00:00 | False | False |
| 4588 | CTRL4588_threshold_mask | support defined by fitted cutoff after residual inspection | reject zero; retain mask/shell row | FIREWALL_PASS | 2026-07-06T13:04:10.899761+00:00 | False | False |
| 4588 | CTRL4588_radiative_sidewall | nonzero sidewall/radiative flux through collar | route as boundary flux, not hidden bulk zero | FIREWALL_PASS | 2026-07-06T13:04:10.899761+00:00 | False | False |
| 4588 | CTRL4588_unbounded_test | arena test function unbounded at boundary | bound not score-ready | COUNTERMODEL_CAUGHT | 2026-07-06T13:04:10.899761+00:00 | False | False |
| 4588 | CTRL4588_no_claim | Reynolds theorem exists but values/signatures missing | no local-GR/R10/PPN claim | FIREWALL_PASS | 2026-07-06T13:04:10.899761+00:00 | False | False |

## Promotion gates

| checkpoint | gate_id | gate | status | generated_utc | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| 4588 | PROM4588_0_Reynolds_identity | Reynolds transport identity for source support emitted. | PASSED | 2026-07-06T13:04:10.899761+00:00 | False | False |
| 4588 | PROM4588_1_zero_trace | Zero-trace/no-shell support theorem derived conditionally. | PASSED_CONDITIONAL | 2026-07-06T13:04:10.899761+00:00 | False | False |
| 4588 | PROM4588_2_shell_bound | Finite shell norm fallback emitted. | PASSED | 2026-07-06T13:04:10.899761+00:00 | False | False |
| 4588 | PROM4588_3_firewalls | Threshold mask, hard shell and radiative sidewall traps are blocked. | PASSED_FIREWALL | 2026-07-06T13:04:10.899761+00:00 | False | False |
| 4588 | PROM4588_4_values | Regular support clauses or numeric shell values are source-backed. | BLOCKED | 2026-07-06T13:04:10.899761+00:00 | False | False |
| 4588 | PROM4588_5_no_local_claim | No local-GR/R10/PPN claim from 4588 alone. | PASSED_FIREWALL | 2026-07-06T13:04:10.899761+00:00 | False | False |

## Decision

| checkpoint | branch | generated_utc | decision | plain_english | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| 4588 | MTS_R2FR_Y5_REGULAR_SOURCE_SUPPORT_BOUNDARY_ZERO_OR_REYNOLDS_SHELL_BOUND_4588 | 2026-07-06T13:04:10.899761+00:00 | REGULAR_ZERO_TRACE_SUPPORT_KILLS_REYNOLDS_BOUNDARY_BIRTH_CONDITIONAL_SHELL_NORM_RETAINED_NONCLAIM | 4588 derives the Reynolds support-boundary law. If the Hilbert source support is compact regular, zero-trace and no-shell on a fixed q-basic collar, the boundary birth term vanishes. If not, the open branch is a finite shell norm with explicit trace-density, support-velocity, shell-measure, arena-test and M_H_ref inputs. This removes another source-worldtube ambiguity without claiming local GR. | False | False |

## Next target

| checkpoint | branch | generated_utc | next_target | reason | derive_first | fallback | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 4588 | MTS_R2FR_Y5_REGULAR_SOURCE_SUPPORT_BOUNDARY_ZERO_OR_REYNOLDS_SHELL_BOUND_4588 | 2026-07-06T13:04:10.899761+00:00 | 4589-Y5-R2FR-MHref-source-blind-reference-and-Htau-normalization-zero-or-bound.md | After density/Poynting and support-boundary components, the source-worldtube denominator and reference lock are the next central coupling obstruction. | prove M_H_ref and H_ref are q-basic, source-blind, positive and fixed before readout in the same tau/e_obs branch | emit finite E_Href and denominator drift rows with H_tau/H_ref/M_H_ref units and no fitted-G absorption | False |

## Source register

| checkpoint | source_id | path | path_exists | needle | needle_found | role | generated_utc | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4588 | SRC4588_00_4587_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\4587-Y5-R2FR-Hilbert-source-density-qbasic-and-Poynting-support-owner-or-bound.md | True | 4588-Y5-R2FR-regular-source-support-boundary-zero-or-Reynolds-shell-bound.md | True | 4587 selected regular support target | 2026-07-06T13:04:10.899761+00:00 | False |
| 4588 | SRC4588_01_4587_reduction | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4587_SOURCE_KERNEL_REDUCTION_UPDATE.csv | True | DRR4587_3_next_regular_support | True | 4587 next support-boundary reduction | 2026-07-06T13:04:10.899761+00:00 | False |
| 4588 | SRC4588_02_4587_residual | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4587_DENSITY_POYNTING_RESIDUAL_VECTOR.csv | True | E_distributional_shell | True | 4587 distributional shell residual | 2026-07-06T13:04:10.899761+00:00 | False |
| 4588 | SRC4588_03_4586_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\4586-Y5-R2FR-source-worldtube-kernel-zero-certificate-or-first-operator-norm.md | True | E_boundary_birth | True | 4586 source-worldtube vector | 2026-07-06T13:04:10.899761+00:00 | False |
| 4588 | SRC4588_04_3560_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3560-Y5-R2FR-source-support-qbasic-worldtube-descent-or-bound-vector.md | True | Reynolds transport | True | 3560 Reynolds support handoff | 2026-07-06T13:04:10.899761+00:00 | False |
| 4588 | SRC4588_05_3560_bound | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3560_BOUND_VECTOR.csv | True | BF3560_1_E_boundary_birth | True | 3560 boundary birth bound row | 2026-07-06T13:04:10.899761+00:00 | False |
| 4588 | SRC4588_06_192_no_flux | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\192-PPC4161-local-boundary-no-flux-sector-interface-theorem.md | True | F_side[tau] = 0 | True | local boundary no-flux theorem | 2026-07-06T13:04:10.899761+00:00 | False |
| 4588 | SRC4588_07_4176_no_flux_csv | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4176_NO_FLUX_THEOREM.csv | True | NFT4176_1_support | True | compact support no-flux selector | 2026-07-06T13:04:10.899761+00:00 | False |
| 4588 | SRC4588_08_324_trace | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\324-PPC4161-smooth-Hilbert-volume-domain-parent-signature-or-worldtube-flux-profile-row.md | True | mu_tr := weak-lim | True | smooth-to-exterior trace defect precedent | 2026-07-06T13:04:10.899761+00:00 | False |
| 4588 | SRC4588_09_284_fixed_collar | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\284-PPC4161-Dq-boundary-projector-fixed-collar-or-boundary-residual-bound.md | True | fixed collar | True | fixed q-basic collar/domain precedent | 2026-07-06T13:04:10.899761+00:00 | False |
| 4588 | SRC4588_10_4580_domain | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4580_PI_READOUT_DOMAIN_CERTIFICATE.csv | True | PDC4580_1_fixed_qbasic_domain | True | fixed q-basic readout domain certificate | 2026-07-06T13:04:10.899761+00:00 | False |
| 4588 | SRC4588_11_claim_429 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\02-claims-register.csv | True | L-429 | True | prior claim register handoff | 2026-07-06T13:04:10.899761+00:00 | False |
