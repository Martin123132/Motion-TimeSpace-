# 3551 - M_H_ref q-basic descent or H_tau/H_ref bound pack

## Verdict

- **The derivation attempt succeeds conditionally:** `M_H_ref = H_tau - H_ref` is q-basic if `H_tau` and `H_ref` are q-basic on the same `q/e_obs/tau/surface` branch.
- **The local zero mechanism is exact:** for vertical `v_X`, `D_X M_H_ref = dMbar_H_ref(Dq(v_X)) = 0`; then `A_X^M=0`, `partial_M A_X^M=0`, and `C_M=0`.
- **It is not live yet:** current source rows still mark `H_tau`, `H_ref`, positive `M_H_ref`, theta/Q_tau ownership, H_tau curl, and same-tau normalization as unsigned.
- **No cancellation is allowed:** if the theorem does not fire, use `|D_X M_H_ref| <= |D_X H_tau| + |D_X H_ref|`; do not tune the reference against the physical charge.

## Descent Theorem

| theorem_id | claim_piece | statement | proof_step | current_status |
| --- | --- | --- | --- | --- |
| MHD3551_0_definition | mass coordinate | M_H_ref(Phi) := H_tau[S_outer;Phi] - H_ref[Phi] | This defines the source mass coordinate used by the source-branch connection A_X^M. | DEFINITION_ONLY_NONCLAIM |
| MHD3551_1_sum_difference_descent | q-basic difference theorem | If H_tau=Hbar_tau(q(Phi)) and H_ref=Hbar_ref(q(Phi)), then M_H_ref=Mbar_H_ref(q(Phi)). | Mbar_H_ref(q):=Hbar_tau(q)-Hbar_ref(q), so a difference of two q-basic scalars is q-basic. | EXACT_THEOREM_CONDITIONAL |
| MHD3551_2_vertical_zero | A_X^M zero | If M_H_ref=Mbar_H_ref(q(Phi)) and Dq(v_X)=0, then A_X^M=D_X M_H_ref=0. | D_X M_H_ref=dMbar_H_ref(Dq(v_X))=0. | EXACT_THEOREM_CONDITIONAL |
| MHD3551_3_mass_flat_corollary | C_M zero | If A_X^M vanishes identically on the source branch, then partial_M A_X^M=0 and C_M=0. | C_M = -(partial_M A_X^M) partial_M(H_tau-H_ref)/(Pi_M H_tau), so the first factor is zero. | EXACT_COROLLARY_NOT_PROMOTED |
| MHD3551_4_no_cancellation_rule | leakage discipline | Without signed q-basicness, D_X M_H_ref must be bounded as D_X H_tau - D_X H_ref without relying on cancellation. | \|D_X M_H_ref\| <= \|D_X H_tau\| + \|D_X H_ref\| by the triangle inequality. | BOUND_ROUTE_REQUIRED_IF_THEOREM_UNSIGNED |

## Required Signatures

| clause_id | object | required_signature | status | failure_residual |
| --- | --- | --- | --- | --- |
| HHD3551_0_actual_q_branch | q branch | single visible q/e_obs/tau branch used by H_tau, H_ref, clocks, R10 and orbital readout | CANDIDATE_UNSIGNED | E_Dq |
| HHD3551_1_vertical_basis | v_X | Dq(v_X)=0 for the actual residual direction used in source coupling | UNSIGNED | E_vertical |
| HHD3551_2_Htau_qbasic | H_tau | integrable parent Hamiltonian charge for tau_obs, built from theta/Q_tau with every retained sector extracted, zeroed or bounded | UNSIGNED | E_Htau |
| HHD3551_3_Href_qbasic | H_ref | source-blind reference/counterterm selected by boundary/topology/stationarity/asymptotic coframe before source readout | UNSIGNED | E_Href |
| HHD3551_4_same_tau_surface_frame | same branch | tau_source=tau_charge=tau_clock=tau_orbit=tau_boundary and the same surface/coframe branch is used | UNSIGNED | E_frame_tau |
| HHD3551_5_positive_denominator | M_H_ref | finite positive same-frame M_H_ref with units, not imported from orbital GM | UNSIGNED | E_denominator |

## Leakage Bound Pack

| bound_id | quantity | formula | non_cancellation_bound | current_value | status |
| --- | --- | --- | --- | --- | --- |
| LB3551_0_A_M_identity | A_X^M | A_X^M = D_X M_H_ref = D_X H_tau - D_X H_ref | \|A_X^M\| <= \|D_X H_tau\| + \|D_X H_ref\| | MISSING_DX_HTAU_AND_DX_HREF | EXACT_IDENTITY_BOUND_INPUTS_MISSING |
| LB3551_1_Htau_leak | D_X H_tau | D_X H_tau = E_theta + E_Qtau + E_curl + E_surface + E_sector + E_boundary | \|D_X H_tau\| <= \|E_theta\| + \|E_Qtau\| + \|E_curl\| + \|E_surface\| + \|E_sector\| + \|E_boundary\| | MISSING_PARENT_HTAU_DERIVATIVE | NONCLAIM_BOUND_ROW |
| LB3551_2_Href_leak | D_X H_ref | D_X H_ref = E_ref_selector + E_ref_boundary + E_ref_frame + E_ref_readout | \|D_X H_ref\| <= \|E_ref_selector\| + \|E_ref_boundary\| + \|E_ref_frame\| + \|E_ref_readout\| | MISSING_SOURCE_BLIND_HREF_DERIVATIVE | NONCLAIM_BOUND_ROW |
| LB3551_3_normalized_mass_leak | epsilon_MHref | epsilon_MHref := \|D_X M_H_ref\|/\|M_H_ref\| | epsilon_MHref <= (\|D_X H_tau\|+\|D_X H_ref\|)/\|M_H_ref\| | MISSING_POSITIVE_SAME_FRAME_MHREF | NONCLAIM_DENOMINATOR_GUARD |
| LB3551_4_C_M_derivative | partial_M A_X^M | partial_M A_X^M = partial_M(D_X H_tau - D_X H_ref) | \|partial_M A_X^M\| <= \|partial_M D_X H_tau\| + \|partial_M D_X H_ref\| | MISSING_PARTIAL_M_DX_HTAU_AND_HREF | NONCLAIM_CM_INPUT_ROW |

## Decisions

| decision_id | question | decision | consequence |
| --- | --- | --- | --- |
| D3551_0_theorem_verdict | Does 3551 prove live M_H_ref q-basic descent? | No live claim. The theorem is exact, but H_tau and H_ref are not parent-signed q-basic scalars yet. | A_X^M and C_M remain nonclaim, but their leakage is now an explicit two-owner bound problem. |
| D3551_1_no_cancellation | Can H_tau and H_ref leakage cancel? | No. Treat them as independently zeroed or independently bounded. | Use \|D_X H_tau\|+\|D_X H_ref\| and never a signed difference as evidence. |
| D3551_2_next_target | Which owner should be attacked next? | Attack H_tau q-basic charge extraction before H_ref polish. | Move to 3552: H_tau q-basic charge extraction or D_X H_tau bound pack. |

## Validation

| validation_id | passes | status | detail |
| --- | --- | --- | --- |
| VAL3551_0_sources_exist | True | PASS | 19/19 cited source paths exist |
| VAL3551_1_generated_csvs_parse | True | PASS | 8 generated CSV files parse with DictReader |
| VAL3551_2_exact_descent_theorem_present | True | PASS | difference-of-q-basic-scalars theorem is present |
| VAL3551_3_required_descent_clauses_covered | True | PASS | H_tau, H_ref and positive M_H_ref denominator clauses are present |
| VAL3551_4_all_rows_nonclaim | True | PASS | theorem, clause, leakage and decision rows do not promote a claim |
| VAL3551_5_no_cancellation_bound_pack | True | PASS | leakage rows use triangle-bound discipline and expose missing parent inputs |
| VAL3551_6_formalization_workbench_untouched | True | PASS | 3551 generated outputs only inside post-checkpoint-work |

## Next target

Move to `3552-Y5-R2FR-Htau-qbasic-charge-extraction-or-DXHtau-bound-pack.md`: extract or bound `H_tau` itself, because it is the larger missing owner inside the mass coordinate.

Generated UTC: 2026-06-29T11:35:01.683459+00:00