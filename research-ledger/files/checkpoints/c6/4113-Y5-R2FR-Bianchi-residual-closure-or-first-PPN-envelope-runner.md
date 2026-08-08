# 4113 - Bianchi residual closure or first PPN envelope runner

## Verdict
4113 imports the useful `3625-3626` work into the active `411x` spine: Bianchi closure is now an exact conditional Noether law, the first PPN/Newton envelope exists, and every local residual has a candidate owner inventory.

This is still not a local-GR claim. The key guard is that Bianchi closure is necessary, not sufficient: a conserved residual can still fail `gamma`, `beta`, preferred-frame, Newton/source, clock, or orbital tests.

## Strongest Current Result
- `BIANCHI_CONDITIONAL_LAW_AND_RESIDUAL_OWNER_INVENTORY_IMPORTED_GK_ORPHAN_NEXT`
- 4113 imports the conditional Noether/Bianchi residual closure law, the first PPN/Newton no-cancellation envelope schema, and the local residual owner inventory into the active 411x spine.
- The local-GR path now has a consistency law plus a component test scaffold; the bottleneck is no longer vague conservation but the hard orphan S_GK/q_loc/T_GK and the parallel Pi_M/H_tau source denominator.

## Bianchi / Noether Closure Law
| law_id | piece | formula | effect | status |
| --- | --- | --- | --- | --- |
| BLC4113_0_parent_action | single diffeomorphism-invariant parent action | delta_xi S_parent=0 | Noether identity applies only to the whole retained system, not to selected convenient pieces. | CONDITIONAL_PARENT_ACTION_NOT_SIGNED |
| BLC4113_1_noether_identity | diffeomorphism Noether identity | nabla_m(2E_g^{mn}) + E_A nabla^n Phi^A + E_psi D^n psi + B_boundary^n = 0 | Bianchi closure must come from parent symmetry plus Euler/boundary terms. | EXACT_CONDITIONAL_IDENTITY_IMPORTED |
| BLC4113_2_residual_closure | local residual closure law | nabla_m[DeltaE_MTS^{mn}-kappa_eff DeltaT_MTS^{mn}]=C_B^n | C_B^n is zero only when parent Euler/source/boundary package closes; otherwise it is an observable residual. | EXACT_CONDITIONAL_CLOSURE_LAW_IMPORTED |
| BLC4113_3_not_sufficient | closure is not local-GR silence | nabla_m DeltaR^{mn}=0 does not imply DeltaR^{mn}=0 | A conserved residual can still fail gamma, beta, preferred-frame, Newton/source, clock or orbital tests. | NO_SMUGGLING_GUARD |
| BLC4113_4_calibrated_drift | calibrated constants consistency | nabla_m[kappa_eff T^{mn}]=(nabla_m kappa_eff)T^{mn}+kappa_eff nabla_m T^{mn} | Measured G_eff/alpha_eff are allowed, but local drift must be zeroed or bounded. | DRIFT_WARNING_RETAINED |

## PPN / Newton Envelope
| envelope_id | observable_component | prediction_formula_template | current_status | runner_verdict |
| --- | --- | --- | --- | --- |
| ENV4113_0_gamma | gamma_minus_1 | gamma_minus_1=K_gamma_DeltaE*Pi_gamma(DeltaE_MTS)+K_gamma_readout*epsilon_readout+K_gamma_q*q_loc_projection | MISSING_COMPONENT_VALUES_AND_BOUND | BLOCKED_NOT_SCORED |
| ENV4113_1_beta | beta_minus_1 | beta_minus_1=sum_abs(beta_source+beta_operator+beta_readout+beta_boundary) | MISSING_SECOND_ORDER_COMPONENT_VALUES_AND_BOUND | BLOCKED_NOT_SCORED |
| ENV4113_2_preferred_frame | alpha_i;xi | Delta_PF_abs=|alpha1|+|alpha2|+|alpha3|+|xi| from projected residual basis | MISSING_PROJECTION_MATRIX_AND_BOUNDS | BLOCKED_NOT_SCORED |
| ENV4113_3_conservation | zeta_i;Bianchi leakage | Delta_cons_abs=|Pi_zeta(C_B)|+|Pi_orbit(C_B)| | MISSING_C_B_VALUE_AND_PROJECTION | BLOCKED_NOT_SCORED |
| ENV4113_4_Newton_Poisson | delta_Newton_MTS | nabla^2 Phi-4*pi*G_eff*rho_H=Pi_00(DeltaE_MTS)-4*pi*G_eff*delta_rho_source+boundary | MISSING_SOURCE_MASS_CLOSURE_AND_BOUND | BLOCKED_NOT_SCORED |
| ENV4113_5_EM_source | w_EM;Phi_EM_boundary | Delta_EM_source_abs=|w_EM|*f_EM+|Phi_EM_boundary|/M_H_ref | MISSING_EM_FRACTION_OR_FLUX_NORMALIZATION | BLOCKED_NOT_SCORED |
| ENV4113_6_total | Delta_local_GR_total_abs | Delta_total_abs=sum_abs(ENV4113_0..ENV4113_5); pass only if each component has theorem-zero or numeric bound pass | RUNNER_SCHEMA_READY_INPUTS_MISSING | BLOCKED_NOT_SCORED |

## Residual Owner Inventory
| inventory_id | residual_symbol | candidate_owner | current_status | blocks |
| --- | --- | --- | --- | --- |
| INV4113_0_DeltaE | DeltaE_MTS_mn | S_EH plus retained S_GK/S_selector/S_boundary/S_readout variations | OWNER_DECOMPOSITION_AVAILABLE_NOT_SIGNED | EH dominance and retained residual coefficient map missing |
| INV4113_1_source_weight | DeltaT_source;w_EM;kappa_J;delta_ellJ | S_matter[e_obs,psi]+S_EM[g_obs,A,J] with same Hilbert/Noether source current | CONDITIONAL_CURRENT_OWNER_NOT_SIGNED | Pi_M/H_tau denominator and same-frame readout unsigned |
| INV4113_2_coupling_drift | delta_kappa;b_alpha;lambda_F2 | topological kappa sector plus parent EM level/fibre metric and unique F_Q^2 domain | PARTIAL_KAPPA_CANDIDATE_ALPHA_LEVEL_UNSIGNED | parent EM level/Q_* certificate missing |
| INV4113_3_q_loc | q_loc^nu | S_GK[g,Phi] or response-doublet action whose Ward identity yields q_loc | ACTION_EXISTENCE_AND_HELMHOLTZ_NOT_PROVED | Gamma/Khat stress may be non-variational bookkeeping |
| INV4113_4_GK_stress | T_GK_mn;T_tau/P_mn | positive auxiliary/response-doublet sector or topological exact sector | CANDIDATE_NOT_MATCHED_TO_EXISTING_MTS_SYMBOLS | positive operator/no-hair and physical residual lock not derived |
| INV4113_5_PiM_boundary | delta_PiM;Phi_EM_boundary;Q_boundary | parent boundary symplectic metric, fixed Pi_M, Hamiltonian H_tau and fixed reference/boundary terms | PROJECTOR_VARIATION_AND_DENOMINATOR_NOT_PARENT_DERIVED | source mass can still be laundered through Pi_M/H_tau/reference |
| INV4113_6_PPN_total | Delta_PPN_abs | derived weak-field/readout solution from the full owned local action | AGGREGATE_SCHEMA_READY_COMPONENT_VALUES_MISSING | beta, preferred-frame, source, boundary and q_loc projection coefficients missing |

## Orphan Scorecard
| score_id | sector | ownership_level | main_gap | next_priority |
| --- | --- | --- | --- | --- |
| OSC4113_0_EH_matter_EM | EH/matter/visible EM | CONDITIONAL_STANDARD_OWNER | parent descent of observed fields and source current/readout closure | medium |
| OSC4113_1_GK_q_loc | Gamma/Khat/q_loc/GK stress | HARD_ORPHAN | S_GK variational owner or response-doublet physical lock | highest |
| OSC4113_2_PiM_source_denominator | Pi_M/H_tau/source mass boundary denominator | HARD_ORPHAN | M_H_ref / Pi_M J_H / H_tau reference lock | highest_parallel |
| OSC4113_3_PPN_component_vector | PPN/Newton component rows | RUNNER_SCHEMA_ONLY | weak-field projection from action-owned residuals | after_owner_attempt_or_parallel_data_fill |

## Decisions
| decision_id | decision | status | next_action |
| --- | --- | --- | --- |
| DEC4113_0_bianchi | Bianchi closure is derived as an exact conditional Noether law, not an axiom. | CONDITIONAL_DERIVATION_IMPORTED | do not claim closure until parent action/Euler/boundary package signs C_B^nu=0 |
| DEC4113_1_envelope | The first PPN/Newton envelope is explicit and refuses to score missing component values. | RUNNER_SCHEMA_READY_BLOCKED_CORRECTLY | fill component rows only from owner theorem or source-backed data |
| DEC4113_2_inventory | Every local residual now has a candidate owner; the true hard orphan is GK/q_loc/T_GK, with Pi_M/H_tau parallel. | OWNER_INVENTORY_IMPORTED | attack highest-leverage orphan instead of recircling the full vector |
| DEC4113_3_claim_guard | No local-GR/Newton/PPN/conservation claim follows. | CLAIM_BLOCKED_NOT_WORK_BLOCKED | Bianchi closure is necessary but not sufficient for local tests |
| DEC4113_4_next | Next current-chain target is Gamma/Khat response-action Helmholtz or q_loc/T_GK bound rows. | NEXT_TARGET_SELECTED | 4114-Y5-R2FR-Gamma-Khat-response-action-Helmholtz-or-qloc-TGK-bound.md |

## Next Target
| target_doc | target_script | objective | success_gate |
| --- | --- | --- | --- |
| 4114-Y5-R2FR-Gamma-Khat-response-action-Helmholtz-or-qloc-TGK-bound.md | scripts/Y5_R2FR_4114_Gamma_Khat_response_action_Helmholtz_or_qloc_TGK_bound.py | test whether Gamma_eff/K_hat/q_loc/T_GK are generated by a legitimate variational S_GK via Helmholtz, metric-response, Euler, double-zero and boundary clauses; if not, fill q_loc/T_GK PPN/Newton component-bound rows as nonclaim | either S_GK passes action-existence, Euler closure, double-zero and boundary no-flux gates, or q_loc/T_GK receive component-level nonclaim coefficient rows with value/unit/bound/source placeholders explicit |

## Claim Ceiling
- No local-GR, Newton, PPN, WEP, R10/R11, Maxwell-source, or conservation pass is claimed.
- The next proof target is the hard orphan: `S_GK/q_loc/T_GK` variational ownership.
- `Pi_M/H_tau/source denominator` remains a parallel pressure point for Newton/source mass.
