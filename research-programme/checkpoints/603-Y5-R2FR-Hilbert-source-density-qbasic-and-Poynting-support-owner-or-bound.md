# 4587 - Hilbert source density q-basic and Poynting support owner or bound

Marker: `PPC4161_HILBERT_SOURCE_DENSITY_QBASIC_AND_POYNTING_SUPPORT_OWNER_OR_BOUND_4587`  
Branch: `MTS_R2FR_Y5_HILBERT_SOURCE_DENSITY_QBASIC_AND_POYNTING_SUPPORT_OWNER_OR_BOUND_4587`  
Decision: `HILBERT_SOURCE_DENSITY_QBASIC_THEOREM_AND_POYNTING_ONCE_ONLY_LOCK_DERIVED_RESIDUAL_VECTOR_RETAINED_NONCLAIM`  
Private/public status: private nonclaim; no GitHub action.

## Result

4587 attacks the first 4586 source-worldtube component directly.

The active source density is:

```text
rho_H dV_H := c^-2 T_total(n,n) dV_eobs.
```

If the source sector is a single q-basic Hilbert functor before variation,

```text
S_src = Sbar_src[q(Phi), Psi, A, theta],
D_v theta=0,
v in ker(Dq),
```

then:

```text
D_v(rho_H dV_H)=0,
E_rho_qbasic=0.
```

The Poynting rule is once-only:

```text
public Maxwell-Hodge T_EM included in T_total  =>  no extra Poynting source coefficient,
c_Poynt_extra=0.
```

Radiative or hidden-Hodge leakage is not erased:

```text
E_EM_flux >= |int_boundary T_EM(tau,n_boundary) dSigma dt| / |M_H_ref|.
```

So this is genuine progress, but still private/nonclaim: parent adoption, regular support, reference normalization and readout masks still gate local GR.

## Density q-basic theorem

| checkpoint | theorem_id | claim | derivation | consequence | status | generated_utc | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 4587 | DQT4587_0_density_definition | The active source density is the Hilbert density measure, not bare rest mass. | rho_H dV_H := c^-2 T_total(n,n) dV_eobs, where T_total is obtained from the same observed-metric Hilbert source action used by the parent source current. | Binding, pressure, EM stress, Poynting bookkeeping and boundary/reference dressing cannot be omitted from the active source. | SOURCE_DENSITY_OBJECT_DEFINED | 2026-07-06T12:58:12.153936+00:00 | False |
| 4587 | DQT4587_1_qbasic_density_zero | If the matter+EM source functor descends through q before variation, then D_v(rho_H dV_H)=0 for v in ker(Dq). | S_src=Sbar_src[q(Phi),Psi,A,theta] with D_v theta=0 gives D_v g_obs=D_v n=D_v dV=0 and D_v T_total=0 on the source functor. Therefore D_v(c^-2 T_total(n,n)dV_eobs)=0. | E_rho_qbasic=0 in the compact private source-functor branch. | CONDITIONAL_ZERO_THEOREM_DERIVED_NOT_GLOBAL_PARENT_SIGNED | 2026-07-06T12:58:12.153936+00:00 | False |
| 4587 | DQT4587_2_profile_support_handoff | Density q-basicness is the first input to source-support descent, not the whole local-GR proof. | 3560 still requires compact regular support, fixed tau/e_obs, M_H_ref source-blindness and no readout mask. Density zero removes E_rho_qbasic only on the strict branch. | The next obstruction becomes regular source-support boundary/Reynolds shell control. | PARTIAL_KERNEL_COMPONENT_ZERO_ROUTE | 2026-07-06T12:58:12.153936+00:00 | False |

## Poynting owner lock

| checkpoint | row_id | case | formula | result | status | claim_allowed | valid_for_claim | generated_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4587 | POY4587_0_public_Maxwell_Hodge | EM action uses the public observed Hodge/coframe | S_EM=-1/(4 mu0) int sqrt(-g_obs) F^2; T_EM^{mu nu}=Hilbert variation | rho_EM=T_EM(n,n)/c^2 and S_EM^i=-T_EM(n,e_i) are components of the same Hilbert stress. | POYNTING_INSIDE_HILBERT_SOURCE_CONDITIONAL | False | False | 2026-07-06T12:58:12.153936+00:00 |
| 4587 | POY4587_1_once_only | attempt to add an extra background/Poynting source after T_EM is already in T_total | T_total includes T_EM and c_Poynt_extra int_boundary S dot n would double-count | c_Poynt_extra=0 in the single source functional branch. | ONCE_ONLY_LOCK_DERIVED | False | False | 2026-07-06T12:58:12.153936+00:00 |
| 4587 | POY4587_2_flux_boundary | radiative or nonminimal EM flux crosses the local source collar | E_EM_flux >= |int_{partial W} T_EM(tau,n_boundary) dSigma dt| / |M_H_ref| | radiative Poynting is not erased; it is boundary/Hamiltonian flux or an explicit source-worldtube residual. | BOUND_ROW_RETAINED_VALUES_MISSING | False | False | 2026-07-06T12:58:12.153936+00:00 |

## Residual vector

| checkpoint | component_id | symbol | definition | zero_condition | bound_formula | status | numeric_value_present | claim_allowed | valid_for_claim | generated_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4587 | DRV4587_0_E_action_vertical | E_action_vertical | explicit vertical field/source dependence in S_src not mediated by q | zero if S_src=Sbar_src[q(Phi),Psi,A,theta] and D_v theta=0 | E_rho_qbasic[E_action_vertical] <= N_density * E_action_vertical | ZERO_CONDITION_DEFINED_VALUE_MISSING | False | False | False | 2026-07-06T12:58:12.153936+00:00 |
| 4587 | DRV4587_1_E_constant_marker | E_constant_marker | hidden vertical dependence of masses, alpha_EM, source normalization or material/source labels | zero if theta, m_A, alpha_EM and source scale are q-owned/fixed | E_rho_qbasic[E_constant_marker] <= N_density * E_constant_marker | ZERO_CONDITION_DEFINED_VALUE_MISSING | False | False | False | 2026-07-06T12:58:12.153936+00:00 |
| 4587 | DRV4587_2_E_matter_lift | E_matter_lift | matter field lift changes physical Hilbert density rather than representative variables | zero if source probe is vertical/gauge or on-shell quotient silent | E_rho_qbasic[E_matter_lift] <= N_density * E_matter_lift | ZERO_CONDITION_DEFINED_VALUE_MISSING | False | False | False | 2026-07-06T12:58:12.153936+00:00 |
| 4587 | DRV4587_3_E_Hodge_EM | E_Hodge_EM | EM Hodge/constitutive relation uses hidden or second frame structure | zero in public Maxwell-Hodge branch | E_rho_qbasic[E_Hodge_EM] <= N_density * E_Hodge_EM | ZERO_CONDITION_DEFINED_VALUE_MISSING | False | False | False | 2026-07-06T12:58:12.153936+00:00 |
| 4587 | DRV4587_4_E_Poynting_boundary | E_Poynting_boundary | EM flux through the source collar not already in stationary H_tau | zero only with no-flux/stationary collar; otherwise finite boundary row | E_rho_qbasic[E_Poynting_boundary] <= N_density * E_Poynting_boundary | ZERO_CONDITION_DEFINED_VALUE_MISSING | False | False | False | 2026-07-06T12:58:12.153936+00:00 |
| 4587 | DRV4587_5_E_nonminimal_EM | E_nonminimal_EM | nonminimal EM/current coupling creates independent source weight | zero if unique Maxwell block and no extra F^2/source multiplier | E_rho_qbasic[E_nonminimal_EM] <= N_density * E_nonminimal_EM | ZERO_CONDITION_DEFINED_VALUE_MISSING | False | False | False | 2026-07-06T12:58:12.153936+00:00 |
| 4587 | DRV4587_6_E_distributional_shell | E_distributional_shell | density/support boundary has source shell or birth/death layer | not solved here; pass to 4588 regular support target | E_rho_qbasic[E_distributional_shell] <= N_density * E_distributional_shell | ZERO_CONDITION_DEFINED_VALUE_MISSING | False | False | False | 2026-07-06T12:58:12.153936+00:00 |
| 4587 | DRV4587_7_E_readout_state | E_readout_state | state/readout mask selected after local residual is inspected | zero only for fixed q-basic domain certificate | E_rho_qbasic[E_readout_state] <= N_density * E_readout_state | ZERO_CONDITION_DEFINED_VALUE_MISSING | False | False | False | 2026-07-06T12:58:12.153936+00:00 |
| 4587 | DRV4587_8_total | E_rho_qbasic_open | open-branch Hilbert density q-basicness failure | all DRV4587_0..7 components zero in one parent branch | E_rho_qbasic <= N_density*(E_action_vertical+E_constant_marker+E_matter_lift+E_Hodge_EM+E_Poynting_boundary+E_nonminimal_EM+E_distributional_shell+E_readout_state) | RESIDUAL_VECTOR_READY_VALUES_MISSING | False | False | False | 2026-07-06T12:58:12.153936+00:00 |

## Reduction rows

| checkpoint | row_id | target | formula | branch_condition | status | generated_utc | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 4587 | DRR4587_0_Erho_zero | E_rho_qbasic | E_rho_qbasic=0 | single q-basic matter+EM Hilbert source functor; fixed constants/source normalization; no hidden EM Hodge; no post-fit readout mask | CONDITIONAL_ZERO_NOT_PUBLIC_CLAIM | 2026-07-06T12:58:12.153936+00:00 | False |
| 4587 | DRR4587_1_EEM_zero_or_bound | E_EM_flux | E_EM_flux=0 for stationary public-Hodge no-flux collar; otherwise E_EM_flux >= |int_boundary T_EM(tau,n)dSigma dt|/|M_H_ref| | public Maxwell-Hodge stress plus stationary/no-flux boundary, or explicit radiative boundary row | POYNTING_ONCE_ONLY_ZERO_OR_BOUND | 2026-07-06T12:58:12.153936+00:00 | False |
| 4587 | DRR4587_2_CKsource_strict_update | C_K_source_worldtube | strict branch removes E_rho_qbasic and E_EM_flux from the 4586 vector; remaining blockers start with E_boundary_birth and support regularity | 4587 density/Poynting zero branch plus 4586 source-worldtube factorisation | PARTIAL_REDUCTION_DERIVED | 2026-07-06T12:58:12.153936+00:00 | False |
| 4587 | DRR4587_3_next_regular_support | E_boundary_birth | prove compact regular support/no Reynolds shell birth, or bound the boundary source layer | next obstruction after density/Poynting placement | SELECTED_NEXT_DERIVATION_TARGET | 2026-07-06T12:58:12.153936+00:00 | False |

## Controls

| checkpoint | control_id | case | expected_result | status | generated_utc | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 4587 | CTRL4587_public_Hilbert_EM | public Maxwell-Hodge EM inside T_total | Poynting is Hilbert flux, not extra source | SYMBOLIC_CONTROL_PASS | 2026-07-06T12:58:12.153936+00:00 | False | False |
| 4587 | CTRL4587_double_count | add Poynting source after including T_EM | reject; c_Poynt_extra=0 | COUNTERMODEL_CAUGHT | 2026-07-06T12:58:12.153936+00:00 | False | False |
| 4587 | CTRL4587_hidden_Hodge | EM Hodge/constitutive law uses hidden frame | retain E_Hodge_EM/E_EM_flux | FIREWALL_PASS | 2026-07-06T12:58:12.153936+00:00 | False | False |
| 4587 | CTRL4587_bare_mass | bare rest mass used as active source | reject; use rho_H/H_tau dressed source | COUNTERMODEL_CAUGHT | 2026-07-06T12:58:12.153936+00:00 | False | False |
| 4587 | CTRL4587_radiative_flux | nonzero EM flux exits collar | retain boundary flux row | FIREWALL_PASS | 2026-07-06T12:58:12.153936+00:00 | False | False |
| 4587 | CTRL4587_no_claim | conditional density theorem exists | no R10/PPN/local-GR claim | FIREWALL_PASS | 2026-07-06T12:58:12.153936+00:00 | False | False |

## Promotion gates

| checkpoint | gate_id | gate | status | generated_utc | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| 4587 | PROM4587_0_density_object | Hilbert density object defined as dressed T_total(n,n)dV/c^2. | PASSED | 2026-07-06T12:58:12.153936+00:00 | False | False |
| 4587 | PROM4587_1_qbasic_theorem | q-basic density zero theorem derived conditionally. | PASSED_CONDITIONAL | 2026-07-06T12:58:12.153936+00:00 | False | False |
| 4587 | PROM4587_2_poynting_once_only | Poynting/Maxwell stress is inside Hilbert source or explicit flux bound. | PASSED_FIREWALL | 2026-07-06T12:58:12.153936+00:00 | False | False |
| 4587 | PROM4587_3_residual_vector | Open branch residual vector emitted. | PASSED | 2026-07-06T12:58:12.153936+00:00 | False | False |
| 4587 | PROM4587_4_parent_adoption | One global parent branch signs all density/Poynting clauses. | BLOCKED | 2026-07-06T12:58:12.153936+00:00 | False | False |
| 4587 | PROM4587_5_no_local_claim | No local-GR/R10/PPN claim from 4587 alone. | PASSED_FIREWALL | 2026-07-06T12:58:12.153936+00:00 | False | False |

## Decision

| checkpoint | branch | generated_utc | decision | plain_english | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| 4587 | MTS_R2FR_Y5_HILBERT_SOURCE_DENSITY_QBASIC_AND_POYNTING_SUPPORT_OWNER_OR_BOUND_4587 | 2026-07-06T12:58:12.153936+00:00 | HILBERT_SOURCE_DENSITY_QBASIC_THEOREM_AND_POYNTING_ONCE_ONLY_LOCK_DERIVED_RESIDUAL_VECTOR_RETAINED_NONCLAIM | 4587 derives the density leg instead of just labelling it missing: if the source action is one q-basic matter+EM Hilbert functor before variation, then rho_H dV_H is vertically silent. Poynting is handled once: public Maxwell-Hodge stress puts it inside T_total/H_tau; radiative or hidden-Hodge flux remains E_EM_flux. The open branch is an explicit residual vector, not a closure assumption. | False | False |

## Next target

| checkpoint | branch | generated_utc | next_target | reason | derive_first | fallback | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 4587 | MTS_R2FR_Y5_HILBERT_SOURCE_DENSITY_QBASIC_AND_POYNTING_SUPPORT_OWNER_OR_BOUND_4587 | 2026-07-06T12:58:12.153936+00:00 | 4588-Y5-R2FR-regular-source-support-boundary-zero-or-Reynolds-shell-bound.md | After density/Poynting ownership, the next source-worldtube obstruction is whether the support boundary is regular and vertically fixed. | prove no source-support birth/death/Reynolds shell term for compact ordinary sources in the same Hilbert worldtube | emit finite E_boundary_birth row with boundary measure, collar normal, density jump/shell strength, M_H_ref normalization and arena links | False |

## Source register

| checkpoint | source_id | path | path_exists | needle | needle_found | role | generated_utc | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4587 | SRC4587_00_4586_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\4586-Y5-R2FR-source-worldtube-kernel-zero-certificate-or-first-operator-norm.md | True | 4587-Y5-R2FR-Hilbert-source-density-qbasic-and-Poynting-support-owner-or-bound.md | True | 4586 selected density/Poynting target | 2026-07-06T12:58:12.153936+00:00 | False |
| 4587 | SRC4587_01_4586_operator | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4586_SOURCE_WORLDTUBE_OPERATOR_VECTOR.csv | True | CKSW4586_0_E_rho_qbasic | True | 4586 E_rho_qbasic source-kernel component | 2026-07-06T12:58:12.153936+00:00 | False |
| 4587 | SRC4587_02_4586_next | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4586_NEXT_TARGET.csv | True | 4587-Y5-R2FR-Hilbert-source-density-qbasic-and-Poynting-support-owner-or-bound.md | True | 4586 next target csv | 2026-07-06T12:58:12.153936+00:00 | False |
| 4587 | SRC4587_03_3560_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3560-Y5-R2FR-source-support-qbasic-worldtube-descent-or-bound-vector.md | True | D_X(rho_H dV_H)=0 | True | 3560 density q-basic implication | 2026-07-06T12:58:12.153936+00:00 | False |
| 4587 | SRC4587_04_3560_bound | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3560_BOUND_VECTOR.csv | True | BF3560_6_E_EM_flux | True | 3560 E_rho/E_EM failure vector | 2026-07-06T12:58:12.153936+00:00 | False |
| 4587 | SRC4587_05_191_Maxwell | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\191-PPC4161-Maxwell-Hodge-Poynting-stress-owner-theorem.md | True | Poynting vector is not a separate background field | True | Maxwell-Hodge/Poynting stress theorem | 2026-07-06T12:58:12.153936+00:00 | False |
| 4587 | SRC4587_06_193_quotient | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\193-PPC4161-quotient-naturality-vertical-silence-theorem.md | True | S_matter = Sbar_m | True | quotient naturality matter descent | 2026-07-06T12:58:12.153936+00:00 | False |
| 4587 | SRC4587_07_223_once_only | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\223-PPC4161-EM-Poynting-Hodge-source-owner-lock.md | True | c_Poynt_extra = 0 | True | Poynting once-only source lock | 2026-07-06T12:58:12.153936+00:00 | False |
| 4587 | SRC4587_08_3375_policy | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3375-Y5-R2FR-worldtube-source-measure-selector-or-Rworldtube-bound-under-AX1090.md | True | POY3375_2_theory_policy | True | Poynting must be included or bounded | 2026-07-06T12:58:12.153936+00:00 | False |
| 4587 | SRC4587_09_3496_poynting | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3496-Y5-R2FR-source-worldtube-hypermomentum-zero-or-kernel-fill.md | True | DER3496_4_poynting_not_optional | True | Poynting not optional precedent | 2026-07-06T12:58:12.153936+00:00 | False |
| 4587 | SRC4587_10_4170_identity | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4170_SAME_OBJECT_IDENTITY.csv | True | SO4170_1_identity | True | same Hilbert/Hamiltonian charge object | 2026-07-06T12:58:12.153936+00:00 | False |
| 4587 | SRC4587_11_4580_domain | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4580_PI_READOUT_DOMAIN_CERTIFICATE.csv | True | PDC4580_1_fixed_qbasic_domain | True | fixed q-basic domain certificate | 2026-07-06T12:58:12.153936+00:00 | False |
| 4587 | SRC4587_12_claim_428 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\02-claims-register.csv | True | L-428 | True | prior claim register handoff | 2026-07-06T12:58:12.153936+00:00 | False |
