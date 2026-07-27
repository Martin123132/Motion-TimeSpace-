# 3625 Y5 R2FR Bianchi residual closure or first PPN envelope runner

**Status:** 3625 derives the conditional Noether/Bianchi residual closure law and builds a first nonclaim PPN/Newton envelope schema; local-GR remains unclaimed because parent action/Euler/boundary signatures and numeric component rows are missing.

**Claim ceiling:** no local-GR, Newton, PPN, WEP, R10/R11, Maxwell-source, or conservation pass is claimed from 3625.

## Core result

The Bianchi route is real but conditional:

```text
single diffeomorphism-invariant parent action
  -> parent Noether identity
  -> residual closure law
  -> nabla_m[DeltaE_MTS^{mn} - kappa_eff DeltaT_MTS^{mn}] = C_B^n
```

`C_B^n=0` only follows when the actual parent Euler equations, source current, and boundary/no-flux terms are signed. Even then, closure is necessary but not sufficient: a conserved nonzero residual can still fail `gamma`, `beta`, preferred-frame, Newton/source, clock, or orbital tests.

## Source register

| source_id | path | exists | needle_found | role |
| --- | --- | --- | --- | --- |
| handoff_3624 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3624_NEXT_TARGET.csv | True | True | 3624 handoff selecting Bianchi/residual envelope. |
| contract_3624 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3624_MINIMAL_LOCAL_GR_CONTRACT.csv | True | True | minimal local-GR contract containing conservation gate. |
| residual_vector_3624 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3624_EXPLICIT_MTS_RESIDUAL_VECTOR.csv | True | True | explicit residual vector to close or bound. |
| newton_ppn_3624 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3624_NEWTON_PPN_COMPLETION_GATES.csv | True | True | Newton/PPN completion gates. |
| claim_gates_3624 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3624_CLAIM_GATES.csv | True | True | nonclaim guard from 3624. |
| ppn_interface_2636 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_GENERATOR_EFFECTIVE_PACK_2636_PPN_INTERFACE_MAP.csv | True | True | PPN interface map for fallback envelope. |
| operator_pack_2619 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_GR_LEFT_HAND_GATE_2619_OPERATOR_RESIDUAL_PACK.csv | True | True | operator residual pack and nonclaim lock. |
| einstein_lhs_2619 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_GR_LEFT_HAND_GATE_2619_EINSTEIN_LEFT_HAND_LIMIT_ATTEMPT.csv | True | True | prior Bianchi/Noether compatibility gate. |
| newton_2619 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_GR_LEFT_HAND_GATE_2619_NEWTON_POISSON_WEAK_FIELD_ATTEMPT.csv | True | True | Newton/Poisson conditional bridge. |
| eh_envelope_2579 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_EH_DESCENT_COUPLING_PIM_2579_LOCAL_GR_RESIDUAL_ENVELOPE.csv | True | True | absolute local-GR residual envelope precedent. |
| q_loc_2581 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_GAMMAKHAT_QLOC_2581_LOCAL_TEST_MAP.csv | True | True | q_loc local test projection map. |
| gk_stress_2469 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_GK_STRESS_2469_LOCAL_METRIC_EQUATION_GATE.csv | True | True | GK stress/local metric equation gate. |
| maxwell_3463 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3463_MAXWELL_POYNTING_STRESS_LEDGER.csv | True | True | Maxwell stress exchange and Poynting source ledger. |
| wem_phi_3623 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3623_WEM_PHI_SOURCE_THEOREM.csv | True | True | EM source-weight/boundary theorem split. |

## Bianchi / Noether derivation

| derivation_id | step | formula | derived_effect | current_status |
| --- | --- | --- | --- | --- |
| BND3625_0_parent_action | parent diffeomorphism-invariant action | S_parent[g,psi,A,Phi]=S_EH+S_matter+S_EM+S_MTS_extra+S_boundary | sets the stage for a Noether identity over the whole retained system | CONDITIONAL_PARENT_ACTION_NOT_SIGNED |
| BND3625_1_noether_identity | diffeomorphism variation | 0=delta_xi S=int sqrt(-g)[E_g^{mn} L_xi g_mn+E_A L_xi Phi^A+E_psi L_xi psi]+boundary | nabla_m(2E_g^{mn}) + E_A nabla^n Phi^A + E_psi D^n psi + B_boundary^n = 0 | EXACT_CONDITIONAL_IDENTITY |
| BND3625_2_on_shell_reduction | on-shell retained fields | E_A=0; E_psi=0; B_boundary^n=0 => nabla_m E_g^{mn}=0 | Bianchi closure follows from the parent action rather than a separate plateau axiom | CONDITIONAL_REQUIRES_PARENT_EULER_AND_BOUNDARY |
| BND3625_3_residual_closure_law | residual field equation | G^{mn}+Lambda g^{mn}=kappa_eff(T_matter^{mn}+T_EM^{mn})+DeltaE_MTS^{mn}; nabla_m[DeltaE_MTS^{mn}-kappa_eff DeltaT_MTS^{mn}]=C_B^n | C_B^n must be zero by parent Noether identity or carried as an observable conservation/preferred-frame residual | EXACT_CONDITIONAL_CLOSURE_LAW |
| BND3625_4_variable_coupling_warning | calibrated constants consistency | nabla_m[kappa_eff T^{mn}] = (nabla_m kappa_eff)T^{mn}+kappa_eff nabla_m T^{mn} | G_eff/alpha_eff calibration is safe; Gdot/alpha_dot drift is not silently ignorable | CONSERVATION_WARNING_WRITTEN |
| BND3625_5_necessary_not_sufficient | closure limit | nabla_m DeltaR^{mn}=0 does not imply DeltaR^{mn}=0 | if closure is conditional, fallback must be a no-cancellation PPN/Newton envelope | NO_SMUGGLING_GUARD |

## Residual closure audit

| audit_id | residual_symbol | closure_condition | failure_mode | current_status |
| --- | --- | --- | --- | --- |
| RCA3625_0_DeltaE | DeltaE_MTS_mn | DeltaE_MTS must be the metric variation of a retained parent sector or a fixed boundary term. | arbitrary dropped/kept DeltaE breaks Bianchi identity or hides a force term | CONDITIONAL_NOT_PARENT_SIGNED |
| RCA3625_1_source_weight | DeltaT_source; w_EM; kappa_J; delta_ellJ | source weights must come from the same Hilbert/Noether current used in the field equation. | test/source current rescaling creates nonconservation or WEP/GM drift | CONDITIONAL_CURRENT_OWNER_NOT_SIGNED |
| RCA3625_2_coupling_drift | delta_kappa; b_alpha; lambda_F2 | calibrated constants must be locally constant or their gradients must be represented as residual fields. | Gdot/alpha_dot terms sneak into conservation and clock/GM observables | DRIFT_BOUND_REQUIRED |
| RCA3625_3_q_loc | q_loc^nu | q_loc must appear as a Ward-balanced force/current term or be zero in the local vacuum branch. | q_loc=0 alone may not kill homogeneous stress; q_loc nonzero maps to PPN/R10/clock/orbit residuals | WARD_ZERO_OR_PROJECTION_REQUIRED |
| RCA3625_4_GK_stress | T_GK_mn; T_tau/P_mn | extra-sector stress must be zero, pure gauge, exponentially suppressed, or explicitly bounded. | conserved but nonzero stress can still change gamma/beta/orbits | BIANCHI_CLOSURE_NOT_ENOUGH |
| RCA3625_5_boundary_PiM | delta_PiM; Phi_EM_boundary; Q_boundary | boundary and readout terms must be fixed before readout and included in the Noether charge balance. | mass/GM can be laundered through the boundary/reference subtraction | BOUNDARY_FLUX_OR_ZERO_REQUIRED |
| RCA3625_6_Delta_PPN_abs | Delta_PPN_abs | each PPN/Newton residual component must be independently zeroed or bounded; no cancellation-only pass. | a conserved residual vector can pass divergence but fail a component bound | SCHEMA_READY_VALUES_MISSING |

## PPN / Newton envelope schema

| envelope_id | observable_component | prediction_formula_template | current_status |
| --- | --- | --- | --- |
| ENV3625_0_gamma | gamma_minus_1 | gamma_minus_1 = K_gamma_DeltaE*Pi_gamma(DeltaE_MTS)+K_gamma_readout*epsilon_readout+K_gamma_q*q_loc_projection | MISSING_COMPONENT_VALUES_AND_BOUND |
| ENV3625_1_beta | beta_minus_1 | beta_minus_1 = sum_abs(beta_source + beta_operator + beta_readout + beta_boundary) | MISSING_SECOND_ORDER_COMPONENT_VALUES_AND_BOUND |
| ENV3625_2_preferred_frame | alpha_i; xi | Delta_PF_abs = |alpha1|+|alpha2|+|alpha3|+|xi| from projected residual basis | MISSING_PROJECTION_MATRIX_AND_BOUNDS |
| ENV3625_3_conservation | zeta_i; Bianchi leakage | Delta_cons_abs = |Pi_zeta(C_B)| + |Pi_orbit(C_B)| | MISSING_C_B_VALUE_AND_PROJECTION |
| ENV3625_4_Newton_Poisson | delta_Newton_MTS | nabla^2 Phi - 4*pi*G_eff*rho_H = Pi_00(DeltaE_MTS)-4*pi*G_eff*delta_rho_source+boundary | MISSING_SOURCE_MASS_CLOSURE_AND_BOUND |
| ENV3625_5_EM_source | w_EM; Phi_EM_boundary | Delta_EM_source_abs = |w_EM|*f_EM + |Phi_EM_boundary|/M_H_ref | MISSING_EM_FRACTION_OR_FLUX_NORMALIZATION |
| ENV3625_6_total | Delta_local_GR_total_abs | Delta_total_abs = sum_abs(ENV3625_0..ENV3625_5); pass only if each component has theorem-zero or numeric bound pass | RUNNER_SCHEMA_READY_INPUTS_MISSING |

## Nonclaim smoke rows

| smoke_id | envelope_id | predicted_value | bound_value | runner_verdict | reason |
| --- | --- | --- | --- | --- | --- |
| SMOKE3625_0 | ENV3625_0_gamma | MISSING_COMPONENT_VALUE | MISSING_BOUND_VALUE | BLOCKED_NOT_SCORED | MISSING_COMPONENT_VALUES_AND_BOUND |
| SMOKE3625_1 | ENV3625_1_beta | MISSING_COMPONENT_VALUE | MISSING_BOUND_VALUE | BLOCKED_NOT_SCORED | MISSING_SECOND_ORDER_COMPONENT_VALUES_AND_BOUND |
| SMOKE3625_2 | ENV3625_2_preferred_frame | MISSING_COMPONENT_VALUE | MISSING_BOUND_VALUE | BLOCKED_NOT_SCORED | MISSING_PROJECTION_MATRIX_AND_BOUNDS |
| SMOKE3625_3 | ENV3625_3_conservation | MISSING_COMPONENT_VALUE | MISSING_BOUND_VALUE | BLOCKED_NOT_SCORED | MISSING_C_B_VALUE_AND_PROJECTION |
| SMOKE3625_4 | ENV3625_4_Newton_Poisson | MISSING_COMPONENT_VALUE | MISSING_BOUND_VALUE | BLOCKED_NOT_SCORED | MISSING_SOURCE_MASS_CLOSURE_AND_BOUND |
| SMOKE3625_5 | ENV3625_5_EM_source | MISSING_COMPONENT_VALUE | MISSING_BOUND_VALUE | BLOCKED_NOT_SCORED | MISSING_EM_FRACTION_OR_FLUX_NORMALIZATION |
| SMOKE3625_6 | ENV3625_6_total | MISSING_COMPONENT_VALUE | MISSING_BOUND_VALUE | BLOCKED_NOT_SCORED | RUNNER_SCHEMA_READY_INPUTS_MISSING |

## Decisions

| decision_id | decision | status | next_action |
| --- | --- | --- | --- |
| DEC3625_0_bianchi_result | Bianchi closure has an exact conditional derivation from a single diffeomorphism-invariant parent action, but current MTS has not signed the parent action/Euler/boundary package. | CONDITIONAL_DERIVATION_NOT_CLAIM | derive actual local parent residual Lagrangian inventory or keep C_B^nu as a bounded residual |
| DEC3625_1_closure_not_silence | A divergence-closed residual is not necessarily zero; local-GR still requires PPN/Newton component silence or bounds. | NO_SMUGGLING_GUARD | do not treat Bianchi closure as a local-GR pass |
| DEC3625_2_envelope_result | The first PPN/Newton envelope schema and smoke rows now exist, but all numeric/source inputs remain missing and nonclaim. | SCHEMA_READY_VALUES_MISSING | fill component rows in the least-scrutiny order: Bianchi C_B, beta, gamma/readout, Newton source mass, EM source/boundary |
| DEC3625_3_next_target | Next checkpoint should attempt the parent local residual Lagrangian inventory, because it can close Bianchi and populate residual components from one source. | NEXT_TARGET_SELECTED | 3626-Y5-R2FR-local-residual-Lagrangian-inventory-or-PPN-component-fill.md |

## Next target

| target_doc | target_script | objective | success_gate |
| --- | --- | --- | --- |
| 3626-Y5-R2FR-local-residual-Lagrangian-inventory-or-PPN-component-fill.md | scripts/Y5_R2FR_3626_local_residual_Lagrangian_inventory_or_PPN_component_fill.py | construct the actual retained local residual Lagrangian/source inventory that would make the Bianchi identity concrete, or fill the first PPN/Newton component rows with source-backed values/bounds | each residual in RV3624 has a parent Lagrangian/Euler/boundary owner or a component-level nonclaim PPN/Newton row with value, units, bound, source path, and no-cancellation guard |
