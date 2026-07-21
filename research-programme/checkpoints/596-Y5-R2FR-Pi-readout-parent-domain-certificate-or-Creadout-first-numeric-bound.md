# 4580 - Pi_readout parent-domain certificate or Creadout first numeric bound

Generated: `2026-07-06T12:03:48.895018+00:00`  
Branch: `MTS_R2FR_Y5_PI_READOUT_PARENT_DOMAIN_CERTIFICATE_OR_CREADOUT_FIRST_NUMERIC_BOUND_4580`  
Decision: `FIXED_QBASIC_READOUT_DOMAIN_CERTIFICATE_DERIVES_CDOMAIN_CSUPPORT_ZERO_ACTIVE_PROJECTOR_BRANCH_RETAINED_NONCLAIM`  
Claim status: private nonclaim checkpoint.

## Result

4580 takes the 4579 readout commutator split and actually deletes a chunk of it in the fixed local branch.

From 4579:

```text
||rho_readout_shift||_TV/M_H_ref <= C_readout
C_readout <= C_domain + C_support + C_frame + C_material + C_kernel + C_EFT + C_tau
```

The fixed q-basic no-flux readout-domain certificate gives:

```text
C_domain = 0
C_support = 0
C_tau_protocol = 0
```

under a pre-variation protocol:

```text
P_loc={Dbar,W_loc,Sigma_in,Sigma_out,C_side,C_rad,tau_obs,e_obs,orientation,units,Pi_loc}
Pi_readout = Pi_post o Pi_protocol[P_loc]
```

with fixed/q-basic domain, compact no-flux support, and observed tau selected before the probe.  Therefore the reduced private branch is:

```text
C_readout <= C_frame + C_material + C_kernel + C_EFT + C_tau_residual
```

This is not a local-GR claim.  It is a real narrowing: the domain/support part is no longer allowed to float as a vague missing coupling in the fixed-collar branch.  Active Hodge/Green/moving-domain projectors and physical Poynting/apparatus/tail flux are explicitly retained as separate bound branches.

## Pi_readout domain certificate

| checkpoint | branch | generated_utc | certificate_id | clause | statement | formula | effect_on_Creadout | status | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4580 | MTS_R2FR_Y5_PI_READOUT_PARENT_DOMAIN_CERTIFICATE_OR_CREADOUT_FIRST_NUMERIC_BOUND_4580 | 2026-07-06T12:03:48.895018+00:00 | PDC4580_0_protocol_object | pre-variation readout protocol | Define the local readout protocol before source variation: P_loc={Dbar,W_loc,Sigma_in,Sigma_out,C_side,C_rad,tau_obs,e_obs,orientation,units,Pi_loc}. | Pi_readout = Pi_post o Pi_protocol[P_loc] | O_f Pi_protocol=0 if P_loc is fixed or q-basic and held fixed during the compact lapse source probe. | CERTIFICATE_CLAUSE_DEFINED | False | False |
| 4580 | MTS_R2FR_Y5_PI_READOUT_PARENT_DOMAIN_CERTIFICATE_OR_CREADOUT_FIRST_NUMERIC_BOUND_4580 | 2026-07-06T12:03:48.895018+00:00 | PDC4580_1_fixed_qbasic_domain | fixed q-basic domain and support | For D_loc=q_src^{-1}(Dbar), source-silent compact probes and no source crossing, the support/domain projector is not varied by the readout operation. | O_f Pi_domain=0 and O_f Pi_support=0 on the fixed compact no-flux collar | C_domain=0 and C_support=0 | CONDITIONAL_THEOREM_ZERO_DERIVED_FROM_3928_3929_4268_4326 | False | False |
| 4580 | MTS_R2FR_Y5_PI_READOUT_PARENT_DOMAIN_CERTIFICATE_OR_CREADOUT_FIRST_NUMERIC_BOUND_4580 | 2026-07-06T12:03:48.895018+00:00 | PDC4580_2_qbasic_tau_protocol | q-basic observed tau used across readout roles | If tau_obs=tau_bar(q) is selected before variation and the same tau is used for source, charge, clock, orbit, PPN and readout, the tau protocol does not create a readout commutator. | O_f Pi_tau=0 inside the fixed observed-tau protocol; tau residuals are routed if roles split | C_tau_protocol=0, while R_tau_split and related residuals remain outside this certificate | CONDITIONAL_PROTOCOL_ZERO_DERIVED_FROM_4269 | False | False |
| 4580 | MTS_R2FR_Y5_PI_READOUT_PARENT_DOMAIN_CERTIFICATE_OR_CREADOUT_FIRST_NUMERIC_BOUND_4580 | 2026-07-06T12:03:48.895018+00:00 | PDC4580_3_active_projector_rejection | active Hodge/Green/moving-domain projector | If Pi_readout is a dynamic Green/Hodge/domain selector, product-rule terms survive and must be bounded. | delta(Pi J)=Pi delta J+(delta Pi)J with delta Pi != 0 generically | Use active branch rows, not zero certificate | ZERO_REJECTED_FOR_ACTIVE_BRANCH | False | False |
| 4580 | MTS_R2FR_Y5_PI_READOUT_PARENT_DOMAIN_CERTIFICATE_OR_CREADOUT_FIRST_NUMERIC_BOUND_4580 | 2026-07-06T12:03:48.895018+00:00 | PDC4580_4_readout_certificate_result | Pi_readout domain certificate result | The fixed q-basic no-flux readout-domain part of C_readout is theorem-zero; remaining material/frame/kernel/EFT/tau-residual channels are not zeroed here. | C_readout <= C_frame + C_material + C_kernel + C_EFT + C_tau_residual after C_domain=C_support=C_tau_protocol=0 | Creadout is reduced rather than merely relabelled as missing | PARTIAL_CREADOUT_REDUCTION_DERIVED_NONCLAIM | False | False |


## Creadout reduction rows

| checkpoint | branch | generated_utc | row_id | quantity | value_or_bound | proof_source | source_path | status | score_ready | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4580 | MTS_R2FR_Y5_PI_READOUT_PARENT_DOMAIN_CERTIFICATE_OR_CREADOUT_FIRST_NUMERIC_BOUND_4580 | 2026-07-06T12:03:48.895018+00:00 | CRV4580_0_C_domain | C_domain | 0 | fixed q-basic local domain D_loc=q_src^{-1}(Dbar), source-silent compact probes, no moving-domain readout | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3929_PROJECTOR_PARENT_SIGNATURE.csv | THEOREM_ZERO_IN_PRIVATE_FIXED_COLLAR_BRANCH | True | False | False |
| 4580 | MTS_R2FR_Y5_PI_READOUT_PARENT_DOMAIN_CERTIFICATE_OR_CREADOUT_FIRST_NUMERIC_BOUND_4580 | 2026-07-06T12:03:48.895018+00:00 | CRV4580_1_C_support | C_support | 0 | compact source support remains inside W_loc and no source-crossing/radiative pullback enters the collar | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\284-PPC4161-Dq-boundary-projector-fixed-collar-or-boundary-residual-bound.md | THEOREM_ZERO_IN_PRIVATE_NOFLUX_COLLAR_BRANCH | True | False | False |
| 4580 | MTS_R2FR_Y5_PI_READOUT_PARENT_DOMAIN_CERTIFICATE_OR_CREADOUT_FIRST_NUMERIC_BOUND_4580 | 2026-07-06T12:03:48.895018+00:00 | CRV4580_2_C_tau_protocol | C_tau_protocol | 0 | tau_obs=tau_bar(q), same tau roles, fixed reference/surfaces/orientation/units before readout | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4269_TAU_LOCK_THEOREM.csv | THEOREM_ZERO_FOR_QBASIC_OBSERVED_TAU_PROTOCOL | True | False | False |
| 4580 | MTS_R2FR_Y5_PI_READOUT_PARENT_DOMAIN_CERTIFICATE_OR_CREADOUT_FIRST_NUMERIC_BOUND_4580 | 2026-07-06T12:03:48.895018+00:00 | CRV4580_3_C_projector_abs_bridge | C_projector_abs | 0 in fixed q-basic/topological readout branch; otherwise use BRR545 absolute bound | 3929 zero result removes epsilon_domain_projector_abs only for the private fixed branch | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3929_PROJECTOR_DOMAIN_ZERO_RESULT.csv | BRANCH_ZERO_ACTIVE_PROJECTOR_FALLBACK_RETAINED | True | False | False |
| 4580 | MTS_R2FR_Y5_PI_READOUT_PARENT_DOMAIN_CERTIFICATE_OR_CREADOUT_FIRST_NUMERIC_BOUND_4580 | 2026-07-06T12:03:48.895018+00:00 | CRV4580_4_Creadout_reduced | C_readout | C_readout <= C_frame + C_material + C_kernel + C_EFT + C_tau_residual | insert CRV4580_0..3 into the 4579 Creadout split | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4579_PROJECTOR_DERIVATIVE_BOUND.csv | REDUCED_BOUND_DERIVED_VALUES_REMAIN | False | False | False |


## Active branch bound rows

| checkpoint | branch | generated_utc | bound_id | when_active | formula | required_input | current_status | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4580 | MTS_R2FR_Y5_PI_READOUT_PARENT_DOMAIN_CERTIFICATE_OR_CREADOUT_FIRST_NUMERIC_BOUND_4580 | 2026-07-06T12:03:48.895018+00:00 | AB4580_0_active_Hodge_Green | Pi_readout is a dynamic Hodge/Green/constraint projector rather than a fixed readout protocol | C_active_projector <= abs(int_A [d,Pi_M^C]J_H)/M_H_ref + operator_norm(delta Pi_M^C/delta g) | PB3941_2_commutator and PB3941_3_projector_stress values or theorem-zero rows | MISSING_COMMUTATOR_AND_PROJECTOR_STRESS_VALUES | False | False |
| 4580 | MTS_R2FR_Y5_PI_READOUT_PARENT_DOMAIN_CERTIFICATE_OR_CREADOUT_FIRST_NUMERIC_BOUND_4580 | 2026-07-06T12:03:48.895018+00:00 | AB4580_1_moving_domain_tau | worldtube/linking surface or tau frame moves under the source/readout probe | C_domain_tau_active <= abs(D_domain Pi_M^C J_H + delta_tau J_H)/M_H_ref | PB3941_5_domain_tau or 4269 tau residual values | MISSING_DOMAIN_AND_TAU_LOCK_IF_BRANCH_REOPENED | False | False |
| 4580 | MTS_R2FR_Y5_PI_READOUT_PARENT_DOMAIN_CERTIFICATE_OR_CREADOUT_FIRST_NUMERIC_BOUND_4580 | 2026-07-06T12:03:48.895018+00:00 | AB4580_2_radiative_boundary | radiative EM/gravity/Poynting flux crosses the compact collar | C_rad_flux <= abs(int_boundary S_rad dot dA dt)/M_H_ref | PB3941_7_em_flux and DOM3946_5_Poynting values or no-flux theorem | MISSING_POYNTING_OR_EM_FLUX_ZERO_OR_VALUE | False | False |


## Closed-domain guards

| checkpoint | branch | generated_utc | guard_id | guard | meaning | status | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4580 | MTS_R2FR_Y5_PI_READOUT_PARENT_DOMAIN_CERTIFICATE_OR_CREADOUT_FIRST_NUMERIC_BOUND_4580 | 2026-07-06T12:03:48.895018+00:00 | CDG4580_0_stationary_tau | stationary/Killing tau for conserved mass current | not supplied by the readout-domain zero itself | MISSING_STATIONARY_TAU_CERTIFICATE | False | False |
| 4580 | MTS_R2FR_Y5_PI_READOUT_PARENT_DOMAIN_CERTIFICATE_OR_CREADOUT_FIRST_NUMERIC_BOUND_4580 | 2026-07-06T12:03:48.895018+00:00 | CDG4580_1_Poynting | EM/Poynting normal wall flux | fixed support does not erase physical flux | MISSING_POYNTING_FLUX_BOUND | False | False |
| 4580 | MTS_R2FR_Y5_PI_READOUT_PARENT_DOMAIN_CERTIFICATE_OR_CREADOUT_FIRST_NUMERIC_BOUND_4580 | 2026-07-06T12:03:48.895018+00:00 | CDG4580_2_apparatus | apparatus/readout support | apparatus must be included in source or excluded with a bound | MISSING_APPARATUS_DOMAIN_DECLARATION | False | False |
| 4580 | MTS_R2FR_Y5_PI_READOUT_PARENT_DOMAIN_CERTIFICATE_OR_CREADOUT_FIRST_NUMERIC_BOUND_4580 | 2026-07-06T12:03:48.895018+00:00 | CDG4580_3_EM_tail | near/tail EM energy ownership | Maxwell stress/Poynting must be Hilbert-owned or bounded | MISSING_EM_TAIL_ENERGY_MODEL_OR_BOUND | False | False |
| 4580 | MTS_R2FR_Y5_PI_READOUT_PARENT_DOMAIN_CERTIFICATE_OR_CREADOUT_FIRST_NUMERIC_BOUND_4580 | 2026-07-06T12:03:48.895018+00:00 | CDG4580_4_theta_source | theta/source normalization descent | no second source normalization is allowed | MISSING_THETA_SOURCE_NORMALIZATION_DESCENT_OR_BOUND | False | False |


## Audit

| checkpoint | branch | generated_utc | audit_id | finding | status | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 4580 | MTS_R2FR_Y5_PI_READOUT_PARENT_DOMAIN_CERTIFICATE_OR_CREADOUT_FIRST_NUMERIC_BOUND_4580 | 2026-07-06T12:03:48.895018+00:00 | AUD4580_0_forward_progress | C_domain and C_support are no longer generic missing rows | ZERO_VALUES_DERIVED_FOR_FIXED_QBASIC_COLLAR | False | False |
| 4580 | MTS_R2FR_Y5_PI_READOUT_PARENT_DOMAIN_CERTIFICATE_OR_CREADOUT_FIRST_NUMERIC_BOUND_4580 | 2026-07-06T12:03:48.895018+00:00 | AUD4580_1_tau_protocol | observed-tau readout protocol can be zeroed, but stationary mass-current tau remains a separate guard | TAU_READOUT_ZERO_NOT_GLOBAL_STATIONARITY | False | False |
| 4580 | MTS_R2FR_Y5_PI_READOUT_PARENT_DOMAIN_CERTIFICATE_OR_CREADOUT_FIRST_NUMERIC_BOUND_4580 | 2026-07-06T12:03:48.895018+00:00 | AUD4580_2_active_projectors | dynamic Hodge/Green/moving-domain projectors are explicitly rejected from the zero branch | ACTIVE_BRANCH_RETAINED | False | False |
| 4580 | MTS_R2FR_Y5_PI_READOUT_PARENT_DOMAIN_CERTIFICATE_OR_CREADOUT_FIRST_NUMERIC_BOUND_4580 | 2026-07-06T12:03:48.895018+00:00 | AUD4580_3_no_public_claim | valid_for_claim remains false because the full local-GR stack still needs frame/material/kernel/EFT/Poynting/tau-source guards | CLAIM_FIREWALL_ACTIVE | False | False |
| 4580 | MTS_R2FR_Y5_PI_READOUT_PARENT_DOMAIN_CERTIFICATE_OR_CREADOUT_FIRST_NUMERIC_BOUND_4580 | 2026-07-06T12:03:48.895018+00:00 | AUD4580_4_verdict | fixed q-basic readout-domain certificate gives first theorem-zero Creadout component values | PARTIAL_CERTIFICATE_COMPLETE_NONCLAIM | False | False |


## Controls

| checkpoint | branch | generated_utc | control_id | input_case | expected | verdict | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4580 | MTS_R2FR_Y5_PI_READOUT_PARENT_DOMAIN_CERTIFICATE_OR_CREADOUT_FIRST_NUMERIC_BOUND_4580 | 2026-07-06T12:03:48.895018+00:00 | CTRL4580_fixed_qbasic | fixed q-basic domain, no source crossing, pure readout protocol | C_domain=C_support=0 | CONTROL_PASS | False | False |
| 4580 | MTS_R2FR_Y5_PI_READOUT_PARENT_DOMAIN_CERTIFICATE_OR_CREADOUT_FIRST_NUMERIC_BOUND_4580 | 2026-07-06T12:03:48.895018+00:00 | CTRL4580_moving_domain | domain chosen by residual or moved by source probe | zero certificate rejected; active bound row used | COUNTERMODEL_CAUGHT | False | False |
| 4580 | MTS_R2FR_Y5_PI_READOUT_PARENT_DOMAIN_CERTIFICATE_OR_CREADOUT_FIRST_NUMERIC_BOUND_4580 | 2026-07-06T12:03:48.895018+00:00 | CTRL4580_flux_crossing | Poynting/radiative flux crosses collar while domain is fixed | domain zero does not erase flux guard | FIREWALL_PASS | False | False |
| 4580 | MTS_R2FR_Y5_PI_READOUT_PARENT_DOMAIN_CERTIFICATE_OR_CREADOUT_FIRST_NUMERIC_BOUND_4580 | 2026-07-06T12:03:48.895018+00:00 | CTRL4580_tau_split | clock/orbit/source/readout use different tau choices | C_tau_protocol zero rejected; tau residual row used | FIREWALL_PASS | False | False |


## Promotion gates

| checkpoint | branch | generated_utc | gate_id | gate | status | required_for_claim | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 4580 | MTS_R2FR_Y5_PI_READOUT_PARENT_DOMAIN_CERTIFICATE_OR_CREADOUT_FIRST_NUMERIC_BOUND_4580 | 2026-07-06T12:03:48.895018+00:00 | PROM4580_0_fixed_domain | Fixed q-basic no-flux domain/support certificate for C_domain and C_support. | PASSED_PRIVATE_BRANCH | True | False |
| 4580 | MTS_R2FR_Y5_PI_READOUT_PARENT_DOMAIN_CERTIFICATE_OR_CREADOUT_FIRST_NUMERIC_BOUND_4580 | 2026-07-06T12:03:48.895018+00:00 | PROM4580_1_tau_protocol | Observed tau readout protocol selected before variation and role-locked. | PASSED_CONDITIONAL_BRANCH | True | False |
| 4580 | MTS_R2FR_Y5_PI_READOUT_PARENT_DOMAIN_CERTIFICATE_OR_CREADOUT_FIRST_NUMERIC_BOUND_4580 | 2026-07-06T12:03:48.895018+00:00 | PROM4580_2_remaining_Creadout | Frame/material/kernel/EFT/tau-residual components theorem-zero or source-bounded. | BLOCKED | True | False |
| 4580 | MTS_R2FR_Y5_PI_READOUT_PARENT_DOMAIN_CERTIFICATE_OR_CREADOUT_FIRST_NUMERIC_BOUND_4580 | 2026-07-06T12:03:48.895018+00:00 | PROM4580_3_closed_domain | Stationary tau, Poynting, apparatus, EM tail and theta/source guards closed. | BLOCKED | True | False |
| 4580 | MTS_R2FR_Y5_PI_READOUT_PARENT_DOMAIN_CERTIFICATE_OR_CREADOUT_FIRST_NUMERIC_BOUND_4580 | 2026-07-06T12:03:48.895018+00:00 | PROM4580_4_no_active_projector_mix | Do not mix fixed collar zero with active Green/Hodge/moving-domain branch. | PASSED_FIREWALL | True | False |


## Source register

| source_id | label | source_path | exists | needle | needle_found | role | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SRC4580_00_4579_doc | 4579 readout commutator checkpoint | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\4579-Y5-R2FR-readout-commutator-zero-or-rho-readout-shift-bound-value.md | True | C_readout | True | Pi_readout parent-domain certificate and first C_readout theorem-zero values | False |
| SRC4580_01_4579_next | 4579 selected 4580 target | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4579_NEXT_TARGET.csv | True | Pi-readout-parent-domain-certificate-or-Creadout-first-numeric-bound | True | Pi_readout parent-domain certificate and first C_readout theorem-zero values | False |
| SRC4580_02_4579_theorem | 4579 product-rule identity | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4579_READOUT_COMMUTATOR_THEOREM.csv | True | RCT4579_3_rho_shift_bound | True | Pi_readout parent-domain certificate and first C_readout theorem-zero values | False |
| SRC4580_03_4579_projector | 4579 Creadout split | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4579_PROJECTOR_DERIVATIVE_BOUND.csv | True | PDB4579_0_Creadout_split | True | Pi_readout parent-domain certificate and first C_readout theorem-zero values | False |
| SRC4580_04_4579_bound | 4579 operator bound row | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4579_RHO_READOUT_SHIFT_BOUND_VALUE_ROWS.csv | True | RVB4579_1_operator_bound | True | Pi_readout parent-domain certificate and first C_readout theorem-zero values | False |
| SRC4580_05_3928_fixed_domain | 3928 fixed domain zero | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3928_PROJECTOR_DOMAIN_CERTIFICATE_AUDIT.csv | True | PDC3928_3_fixed_domain_zero | True | Pi_readout parent-domain certificate and first C_readout theorem-zero values | False |
| SRC4580_06_3928_active_no_go | 3928 active branch no-go | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3928_PROJECTOR_DOMAIN_CERTIFICATE_AUDIT.csv | True | PDC3928_7_active_branch_no_go | True | Pi_readout parent-domain certificate and first C_readout theorem-zero values | False |
| SRC4580_07_3928_contract | 3928 topological/readout zero contract | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3928_TOPOLOGICAL_READOUT_ZERO_CONTRACT.csv | True | ZPD3928_0_readout_route | True | Pi_readout parent-domain certificate and first C_readout theorem-zero values | False |
| SRC4580_08_3929_signature | 3929 q-basic projector signature | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3929_PROJECTOR_PARENT_SIGNATURE.csv | True | SIG3929_6_signature_verdict | True | Pi_readout parent-domain certificate and first C_readout theorem-zero values | False |
| SRC4580_09_3929_zero | 3929 projector/domain zero result | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3929_PROJECTOR_DOMAIN_ZERO_RESULT.csv | True | PDZ3929_4_epsilon_domain_projector_abs | True | Pi_readout parent-domain certificate and first C_readout theorem-zero values | False |
| SRC4580_10_3941_map | 3941 PiM/Htau residual split | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3941_PIM_HTAU_MAP_DERIVATION.csv | True | MAP3941_3_exact_split | True | Pi_readout parent-domain certificate and first C_readout theorem-zero values | False |
| SRC4580_11_3941_bounds | 3941 domain/tau bound row | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3941_PIM_COMMUTATOR_BOUND_ROWS.csv | True | PB3941_5_domain_tau | True | Pi_readout parent-domain certificate and first C_readout theorem-zero values | False |
| SRC4580_12_3946_domain | 3946 closed-domain blockers | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3946_TOTAL_SOURCE_DOMAIN_CERTIFICATE.csv | True | DOM3946_8_result | True | Pi_readout parent-domain certificate and first C_readout theorem-zero values | False |
| SRC4580_13_4269_tau | 4269 q-basic observed tau theorem | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4269_TAU_LOCK_THEOREM.csv | True | TAU4269_1_qbasic_observed_tau | True | Pi_readout parent-domain certificate and first C_readout theorem-zero values | False |
| SRC4580_14_4269_adoption | 4269 Dq tau adoption | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4269_DQ_TAU_ADOPTION.csv | True | ADOPT4269_Dq_tau | True | Pi_readout parent-domain certificate and first C_readout theorem-zero values | False |
| SRC4580_15_4269_residuals | 4269 tau residual fallback | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4269_TAU_RESIDUAL_SPLIT_ROWS.csv | True | TRES4269_0_tau_split | True | Pi_readout parent-domain certificate and first C_readout theorem-zero values | False |
| SRC4580_16_2598_stationary_guard | 2598 stationary tau not derived guard | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_STATIONARY_TAU_2598_THEOREM_ATTEMPT.csv | True | STA2598_7_verdict | True | Pi_readout parent-domain certificate and first C_readout theorem-zero values | False |
| SRC4580_17_formal_284 | 4268 fixed noflux collar theorem | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\284-PPC4161-Dq-boundary-projector-fixed-collar-or-boundary-residual-bound.md | True | Dq_boundary_projector = 0 | True | Pi_readout parent-domain certificate and first C_readout theorem-zero values | False |
| SRC4580_18_formal_342 | 4326 Hperp boundary/projector zero | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\342-PPC4161-Dq-boundary-projector-Hperp-zero-or-domain-tail-bound.md | True | Dq_boundary_projector[Hperp]=0 | True | Pi_readout parent-domain certificate and first C_readout theorem-zero values | False |
| SRC4580_19_claim_421 | prior claim register row | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\02-claims-register.csv | True | L-421 | True | Pi_readout parent-domain certificate and first C_readout theorem-zero values | False |


## Next target

`4581-Y5-R2FR-remaining-Creadout-frame-material-kernel-EFT-tau-residual-bound-or-zero.md`

Reason: after removing the fixed domain/support branch, attack the remaining `C_readout` terms directly.
