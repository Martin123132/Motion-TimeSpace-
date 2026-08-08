# 3552 - H_tau q-basic charge extraction or D_X H_tau bound pack

## Verdict

- **The exact route is now written:** `H_tau` is q-basic if the parent current chain `L_parent -> theta_MTS -> J_tau -> Q_tau^MTS -> H_tau` is built only from the same visible `q/e_obs/tau` branch and is integrable.
- **The local zero is exact but not live:** if `H_tau=Hbar_tau(q(Phi))` and `Dq(v_X)=0`, then `D_X H_tau=0`.
- **No EH shortcut:** the GR/EH charge is a comparison template only until MTS extracts or bounds boundary, extra, projector, matter/source and constraint pieces.
- **Bound fallback installed:** if the theorem is unsigned, use an explicit no-cancellation leakage vector for `D_X H_tau` and `partial_M D_X H_tau`.

## H_tau Theorem

| theorem_id | claim_piece | statement | current_status |
| --- | --- | --- | --- |
| HTD3552_0_covariant_phase_space_charge | H_tau definition | delta H_tau = integral_S(delta Q_tau^MTS - i_tau theta_MTS) plus explicit constraint/bulk terms that must vanish or be retained. | FORMAL_SHAPE_NOT_PARENT_OWNED |
| HTD3552_1_qbasic_charge_theorem | H_tau q-basicness | If L_parent, tau_obs, theta_MTS, Q_tau^MTS, boundary/reference data, and the integration surface all factor through the same q/e_obs/tau branch, then H_tau=Hbar_tau(q(Phi)). | EXACT_CONDITIONAL_THEOREM_UNSIGNED |
| HTD3552_2_vertical_zero | D_X H_tau zero | If H_tau=Hbar_tau(q(Phi)) and Dq(v_X)=0, then D_X H_tau=0. | EXACT_COROLLARY_NOT_LIVE |
| HTD3552_3_integrability_gate | path independence | H_tau is a scalar charge only if curl(delta H_tau)=0 or every curl/boundary term is retained with units. | BLOCKED_BY_2667 |
| HTD3552_4_EH_import_guard | GR charge comparison | Q_tau^EH can be used as a template only; it proves MTS H_tau only after MTS residual, boundary, projector, matter/source and extra-sector pieces are extracted, zeroed or bounded. | GUARD_ACTIVE |

## Parent Charge Chain

| chain_id | object | required_identity | status | if_signed |
| --- | --- | --- | --- | --- |
| CCA3552_0_parent_action | L_parent | delta L_parent = E_A delta Phi^A + d theta_MTS(delta Phi) | MISSING_EXPLICIT_CURRENT_CHAIN | theta_MTS becomes evaluable rather than a placeholder |
| CCA3552_1_tau_action | tau_obs | L_tau Phi^A is defined for metric, matter, representative, projector, boundary and reference fields before readout | MISSING_PARENT_SELECTED_TAU_LOCK | tau-choice ambiguity leaves D_X H_tau |
| CCA3552_2_theta_MTS | theta_MTS | theta_MTS = theta_EH + theta_boundary + theta_extra + theta_projector + theta_matter/source | MISSING_THETA_EXTRACTION | delta H_tau can be formed from parent variables |
| CCA3552_3_Qtau_split | Q_tau^MTS | J_tau=dQ_tau^MTS+C_tau with Q_EH, Q_boundary, Q_extra, Q_projector and Q_matter/source pieces extracted | PIECE_SPLIT_NOT_PROMOTED | total Q_tau becomes candidate physical Hamiltonian mass charge |
| CCA3552_4_constraints | C_tau | all retained bulk/source/projector/boundary constraints vanish by EOM or are bounded with source rows | OWNERSHIP_NOT_ZERO_THEOREM | bulk-to-boundary reduction becomes honest |
| CCA3552_5_boundary_reference | boundary/reference | B_ref/H_ref and improvement ambiguity are fixed before source/orbit/clock readout | REFERENCE_AND_IMPROVEMENT_UNSIGNED | H_tau cannot absorb source normalization by counterterm choice |
| CCA3552_6_integrability | curl(delta H_tau) | curl(delta H_tau)=0 or every curl/boundary/projector-stress term is explicitly retained | HTAU_INTEGRABILITY_CURL_NOT_CLAIM_READY | H_tau becomes path-independent on the selected branch |

## D_X H_tau Bound Pack

| bound_id | quantity | formula | current_value | arena |
| --- | --- | --- | --- | --- |
| DXH3552_0_total | D_X H_tau | D_X H_tau = E_tau + E_theta + E_QEH + E_Qboundary + E_Qextra + E_Qprojector + E_Qmatter + E_constraint + E_curl + E_surface + E_units | MISSING_DX_HTAU_COMPONENT_VECTOR | M_H_ref; Newton source denominator; local GR; PPN; R10 |
| DXH3552_1_tau_generator | E_tau | variation from tau_obs not being the same q-basic source/charge/clock/orbit/boundary generator | MISSING_PARENT_SELECTED_TAU_LOCK | clocks; orbital GM; H_tau integrability |
| DXH3552_2_theta | E_theta | variation from missing theta_MTS sector extraction | MISSING_THETA_MTS_SOURCE | H_tau charge extraction |
| DXH3552_3_EH_import | E_QEH | EH reference charge mismatch if Q_tau^EH is treated as total MTS charge | MISSING_MTS_PARENT_REDUCTION_GUARD | GR/Newton comparison baseline |
| DXH3552_4_boundary | E_Qboundary | boundary/reference/improvement contribution to Q_tau | MISSING_FIXED_BEFORE_READOUT_COUNTERTERM_POLICY | H_ref; M_H_ref; local boundary terms |
| DXH3552_5_extra_sector | E_Qextra | motion/time/domain/memory/range charge leakage | MISSING_Q_TAU_EXTRA_SOURCE | cosmology/local split; local GR residuals |
| DXH3552_6_projector | E_Qprojector | projector/Pi_M variation and [d,Pi_M]J_H contribution | MISSING_Q_TAU_PROJECTOR_SOURCE | C_M; source denominator; PPN source profile |
| DXH3552_7_matter_source | E_Qmatter | matter/source constraint and worldtube glue contribution | MISSING_Q_TAU_MATTER_SOURCE | Newton source mass; WEP; local source coupling |
| DXH3552_8_constraints_curl_surface | E_constraint + E_curl + E_surface | bulk constraint, field-space curl and surface/domain mismatch contributions | MISSING_CONSTRAINT_CURL_SURFACE_VECTOR | H_tau integrability; local GR; Newton source |

## partial_M D_X H_tau Rows

| row_id | quantity | formula | current_value | feeds |
| --- | --- | --- | --- | --- |
| PMDX3552_0_total | partial_M D_X H_tau | partial_M D_X H_tau = sum_i partial_M E_i | MISSING_PARTIAL_M_DX_HTAU_COMPONENT_VECTOR | C_M via partial_M A_X^M |
| PMDX3552_1_projector_matter | partial_M(E_Qprojector + E_Qmatter) | source-sensitive charge leakage through Pi_M and Hilbert-current glue | MISSING_SOURCE_SENSITIVE_CHARGE_DERIVATIVE | C_M; Newton source normalization |
| PMDX3552_2_boundary_extra | partial_M(E_Qboundary + E_Qextra) | mass dependence of boundary/reference and extra-sector charge leakage | MISSING_BOUNDARY_EXTRA_MASS_DERIVATIVE | C_M; H_ref separation; local GR residual |
| PMDX3552_3_integrability | partial_M(E_curl + E_surface) | mass dependence of H_tau curl and surface branch mismatch | MISSING_CURL_SURFACE_MASS_DERIVATIVE | C_M; M_H_ref positivity and path independence |

## Decisions

| decision_id | question | decision | consequence |
| --- | --- | --- | --- |
| D3552_0_theorem_verdict | Did 3552 make H_tau live? | No live claim. It proves the exact q-basic charge theorem, but the parent theta/Q_tau chain is not extracted. | H_tau is now a component charge-extraction problem, not a vague denominator problem. |
| D3552_1_EH_guard | Can the EH/GR Hamiltonian charge be used? | Only as a comparison template. | No GR/Newton reduction claim from EH import alone. |
| D3552_2_next_target | What is the least-cheatable next step? | Build the parent sector current-chain contract for theta_MTS. | Move to 3553: sector action variation/theta source pack. |

## Validation

| validation_id | passes | status | detail |
| --- | --- | --- | --- |
| VAL3552_0_sources_exist | True | PASS | 21/21 cited source paths exist |
| VAL3552_1_generated_csvs_parse | True | PASS | 9 generated CSV files parse with DictReader |
| VAL3552_2_qbasic_charge_theorem_present | True | PASS | H_tau q-basic charge theorem is present |
| VAL3552_3_charge_chain_covered | True | PASS | parent action, theta_MTS, Q_tau split and integrability gates are covered |
| VAL3552_4_all_rows_nonclaim | True | PASS | all theorem/audit/bound/decision rows keep claims disabled |
| VAL3552_5_leakage_vector_non_cancellation | True | PASS | D_X H_tau and partial_M D_X H_tau rows expose missing inputs and use no-cancellation bounds |
| VAL3552_6_formalization_workbench_untouched | True | PASS | 3552 generated outputs only inside post-checkpoint-work |

## Next target

Move to `3553-Y5-R2FR-parent-sector-current-chain-theta-source-pack.md`: build the sector-by-sector `theta_MTS` source pack, because it is the first missing object in the `H_tau` theorem.

Generated UTC: 2026-06-29T11:42:43.703213+00:00