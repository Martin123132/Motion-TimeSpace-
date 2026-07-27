# 3790 - Charge Unit Superselection or beta_q Bound

## Status

`QSTAR_SUPERSELECTION_EXACT_IF_PARENT_SIGNED_CURRENT_CORPUS_UNSIGNED_BETAQ_ROWS_RETAINED`.

3790 proves the exact conditional q_* route: a parent-signed compact charge lattice makes beta_q,A=0 and d beta_q,A=0, which zeroes eps_qA, eps_betaqF, and eps_dbetaqA. The current corpus still has q_* unsigned, so finite beta_q bound rows remain. This does not derive alpha_EM or Z_EM.

## Result In Plain Terms

3790 takes a real conditional win without cheating. If `q_*` is a fixed compact U(1) charge-lattice/superselection datum in the parent branch, then `Lie_EA q_*=0`, so `beta_q,A=0` and `d beta_q,A=0`. That kills `eps_qA`, `eps_betaqF`, and `eps_dbetaqA` in the local `R_A/dR_A` response. But the current corpus has not yet signed the parent U(1) bundle/generator/lattice owner, so finite `beta_q` rows stay live in current-corpus mode. Also: this does not derive `alpha_EM`, `Z_EM`, or the Maxwell kinetic coefficient.

## Compact Result

`beta_q,A := Lie_EA ln q_*`.

If `q_*` is quotient-owned or compact charge-lattice superselected, then `beta_q,A=0` and `d beta_q,A=0`.

Then `eps_qA=0`, `eps_betaqF=0`, and `eps_dbetaqA=0`.

With the `U_good` chart-zero from 3789, the local response reduces conditionally to `RA_normed <= eps_BQ_descent_A` and `dRA_normed <= eps_dBQ_A`.

The remaining hard blockers are `B_Q` owner/descent, `Z_EM`, `lambda_A`, same-current descent, defects, and source/Hilbert stress ownership.

## q_* Superselection Theorem
- `QST3790_0_constant_superselection_template` `vertical silence of a constant/charge unit`: mathematical_form: If q_*(Phi)=qbar_*(q_obs(Phi)) or q_* is discrete/topological representation data, then Dq_obs[E_A]=0 implies Lie_EA q_*=0.; proof_status: EXACT_CONDITIONAL_THEOREM; missing_for_current_claim: parent classification that q_* is quotient-owned or topological charge-lattice data; if_unsigned: retain beta_q,A
- `QST3790_1_compact_lattice_route` `q_* as compact U(1) charge-lattice period`: mathematical_form: For a fixed compact U(1) parent bundle, charges are representation/lattice labels n in Z and q_* is the global lattice scale; admissible local vertical variations preserve the lattice, so Lie_EA ln q_*=0.; proof_status: EXACT_IF_PARENT_U1_LATTICE_SIGNED; missing_for_current_claim: parent-signed P_Q, fixed charge lattice/generator, and nonrescalable normalization; if_unsigned: beta_q,A remains a finite residual row
- `QST3790_2_betaq_derivative` `d beta_q,A`: mathematical_form: If beta_q,A:=Lie_EA ln q_*=0 as a superselection identity on U_good, then d beta_q,A=0 on U_good.; proof_status: EXACT_CONDITIONAL_COROLLARY; missing_for_current_claim: same parent-signed q_* superselection as QST3790_1; if_unsigned: eps_dbetaqA remains a finite residual row
- `QST3790_3_not_alpha_owner` `q_* silence does not imply alpha_EM or Z_EM silence`: mathematical_form: Compactness fixes charge labels/connection periods, but Z_EM, N_Q, lambda_A, current normalization, and readout descent can still vary.; proof_status: ACTIVE_OVERCLAIM_GUARD; missing_for_current_claim: unique Maxwell F^2 normalization, fixed generator norm, same-current owner, and readout descent; if_unsigned: retain beta_Z,A, lambda_A, epsilon_J_Q, and alpha/readout residuals

## Current Corpus Signature Audit
- `AUD3790_0_3783_qstar`: source_signal: 3783 marks qstar_superselected as false/missing charge-unit owner; current_result: CURRENT_CORPUS_UNSIGNED; impact: cannot promote beta_q,A=0 as a current derived MTS result
- `AUD3790_1_3784_action_clause`: source_signal: 3784 includes q_* in the minimal parent U(1) field space and names charge-unit zero as a required zero condition; current_result: PARENT_EXTENSION_ROUTE_AVAILABLE; impact: q_* can be signed as a clean parent-extension clause without changing the RA/dRA algebra
- `AUD3790_2_1047_constant_theorem`: source_signal: 1047 proves the exact conditional criterion: quotient-descended or topological constants are vertical-silent; current_result: THEOREM_TEMPLATE_AVAILABLE; impact: q_* silence is mathematically justified if q_* is classified as charge-lattice/topological data
- `AUD3790_3_1056_alpha_guard`: source_signal: 1056 says compact U1 fixes charge lattice/periods but not continuous Maxwell kinetic coefficient; current_result: NO_ALPHA_PROMOTION; impact: zeroing beta_q,A does not zero beta_Z,A or derive alpha_EM
- `AUD3790_4_current_verdict`: source_signal: all relevant sources support a conditional q_* theorem but do not parent-sign the current corpus; current_result: CONDITIONAL_ZERO_EXTENSION_OR_FINITE_BOUND_FALLBACK; impact: emit both the exact zero branch and nonclaim beta_q bound rows

## beta_q Zero or Bound Components
- `BQ3790_0_beta_qA` `beta_q,A`: definition: Lie_EA ln q_*; zero_if: q_* is quotient-owned or compact charge-lattice/superselection data and E_A preserves the parent bundle/lattice; conditional_value: 0; fallback_value: MISSING_BETA_QA_OR_PARENT_ZERO_THEOREM; feeds: eps_qA;eps_betaqF;alpha_source_leakage;Gdot_source_rate; status: CONDITIONAL_ZERO_CURRENTLY_UNSIGNED
- `BQ3790_1_d_beta_qA` `d beta_q,A`: definition: exterior derivative on U_good of beta_q,A; zero_if: beta_q,A=0 as a superselection identity or beta_q,A is constant on U_good; conditional_value: 0; fallback_value: MISSING_DBETA_QA_PROFILE_OR_BOUND; feeds: eps_dbetaqA; status: CONDITIONAL_ZERO_CURRENTLY_UNSIGNED
- `BQ3790_2_eps_qA` `eps_qA`: definition: |beta_q,A| ||A_obs||_A/A_ref; zero_if: beta_q,A=0; conditional_value: 0; fallback_value: |beta_q,A| ||A_obs||_A/A_ref; feeds: RA_normed; status: ZERO_IN_QSTAR_EXTENSION_BRANCH_ELSE_BOUND_ROW
- `BQ3790_3_eps_betaqF` `eps_betaqF`: definition: |beta_q,A| ||F_obs||_F/F_ref; zero_if: beta_q,A=0; conditional_value: 0; fallback_value: |beta_q,A| ||F_obs||_F/F_ref; feeds: dRA_normed; status: ZERO_IN_QSTAR_EXTENSION_BRANCH_ELSE_BOUND_ROW
- `BQ3790_4_eps_dbetaqA` `eps_dbetaqA`: definition: ||d beta_q,A wedge A_obs||_F/F_ref; zero_if: d beta_q,A=0 or A_obs wedge d beta_q,A=0 by source-backed profile; conditional_value: 0; fallback_value: ||d beta_q,A wedge A_obs||_F/F_ref; feeds: dRA_normed; status: ZERO_IN_QSTAR_EXTENSION_BRANCH_ELSE_BOUND_ROW

## R_A/dR_A Update
- `RDU3790_0_full_3789_nonclaim` `finite_current_corpus`: formula: RA_normed <= eps_BQ_descent_A + eps_BQ_chart_A + eps_qA; conditions: no q_* superselection claim; chart may or may not be local-zero; status: RETAINED_BOUND_FORM
- `RDU3790_1_qstar_zero` `qstar_superselected_parent_extension`: formula: RA_normed <= eps_BQ_descent_A + eps_BQ_chart_A; conditions: Lie_EA q_*=0 from parent-signed compact charge lattice; status: CONDITIONAL_SIMPLIFICATION
- `RDU3790_2_qstar_and_Ugood_zero` `qstar_superselected_on_Ugood`: formula: RA_normed <= eps_BQ_descent_A; conditions: q_* superselected plus U_good chart/Wilson zero; status: CONDITIONAL_LOCAL_SIMPLIFICATION
- `RDU3790_3_dRA_qstar_zero` `qstar_superselected_parent_extension`: formula: dRA_normed <= eps_dBQ_A + eps_dchart_A; conditions: beta_q,A=0 and d beta_q,A=0 from parent-signed charge lattice; status: CONDITIONAL_SIMPLIFICATION
- `RDU3790_4_dRA_qstar_and_Ugood_zero` `qstar_superselected_on_Ugood`: formula: dRA_normed <= eps_dBQ_A; conditions: q_* superselected plus U_good chart/Wilson zero; status: CONDITIONAL_LOCAL_SIMPLIFICATION
- `RDU3790_5_hard_remainder` `local_EM_GR_remainder`: formula: local EM closure now reduces to B_Q descent/owner/rank/Z_EM/current/lambda/defect clauses after q_* is signed; conditions: does not prove B_Q owner, Z_EM owner, same-source current, or unique Maxwell kinetic normalization; status: REMAINDER_EXPLICIT

## Alpha/Z_EM Overclaim Guard
- `AG3790_0_charge_lattice_not_alpha`: rule: Do not infer beta_Z,A=0 or b_alpha=0 from beta_q,A=0.; because: compact U(1) fixes charge labels/periods, while Maxwell kinetic normalization and readout can vary independently; retained_rows: beta_Z,A;lambda_A;N_Q;Z_EM;epsilon_J_Q;b_alpha
- `AG3790_1_no_generator_rescale_cheat`: rule: A fixed charge lattice must include a nonrescalable parent generator/norm; otherwise q_* can be conventionally rescaled with A_Q/current labels.; because: 1056 rescaling ledger keeps generator/current normalization unsigned; retained_rows: N_Q;current normalization;readout descent
- `AG3790_2_parent_extension_flag`: rule: The q_* zero is a valid parent-extension clause, not yet a derivation from the current real-scalar MTS corpus.; because: 3783/3784 explicitly say the parent U(1) bundle and primitive Pi_Q remain unsigned; retained_rows: P_Q;Pi_Q;B_Q owner;D_Q defects

## Claim Gates
- `CG3790_0_sources`: pass: True; claim_allowed: False; details: all cited source paths resolve
- `CG3790_1_qstar_theorem_shape`: pass: True; claim_allowed: False; details: exact conditional q_* superselection theorem emitted
- `CG3790_2_current_qstar_signed`: pass: False; claim_allowed: False; details: current corpus still lacks parent-signed U(1) bundle/generator/lattice owner
- `CG3790_3_extension_branch_zeroes_betaq`: pass: True; claim_allowed: False; details: if q_* is accepted as parent-superselected charge-lattice data, beta_q,A and d beta_q,A vanish
- `CG3790_4_no_alpha_overclaim`: pass: True; claim_allowed: False; details: Z_EM/alpha/current/readout rows remain live despite q_* zero branch
- `CG3790_5_numeric_bound_ready`: pass: False; claim_allowed: False; details: finite fallback still lacks numeric beta_q,A or d beta_q,A bound/profile
- `CG3790_6_local_GR_EM_claim`: pass: False; claim_allowed: False; details: no local-GR/EM claim; q_* theorem only removes one charge-unit residual branch conditionally

## Decisions
- `DEC3790_0_take_conditional_win`: decision: q_* superselection is an exact conditional theorem and should be used in the parent U(1) extension branch.; action: Mark beta_q,A, eps_qA, eps_betaqF, and eps_dbetaqA as zero only under the signed charge-lattice clause.
- `DEC3790_1_keep_current_corpus_honest`: decision: The current real-scalar corpus still has not derived the parent U(1) bundle or q_* owner.; action: Retain beta_q finite-bound rows for current-corpus mode.
- `DEC3790_2_no_alpha_jump`: decision: Charge-unit silence does not own alpha_EM.; action: Keep beta_Z,A, lambda_A, N_Q/Z_EM, current normalization, and readout descent as separate gates.
- `DEC3790_3_next`: decision: After q_* zero, the next cheap exact target is Z_EM/Maxwell normalization or same-current owner; the hardest remaining target is still B_Q owner.; action: Attempt Z_EM fixed-normalization/no-independent-F2 gate in the R2FR local EM branch.

## Next Target
- `3791-Y5-R2FR-ZEM-fixed-normalization-or-betaZ-bound.md`: target_script: scripts/Y5_R2FR_3791_ZEM_fixed_normalization_or_betaZ_bound.py; objective: Try to prove beta_Z,A=0 from fixed parent generator norm/unique Maxwell kinetic normalization/no independent F^2 operator in the local EM branch; if it fails, emit source-ready beta_Z/lambda_A bound rows without claiming alpha_EM ownership.

## Validation
- `sources_exist` `PASS`: detail: every cited source path exists
- `csv_outputs_parse` `PASS`: detail: all generated CSV outputs exist and parse
- `doc_written` `PASS`: detail: 3790 markdown document written
- `qstar_theorem` `PASS`: detail: compact charge-lattice q_* theorem emitted
- `current_unsigned` `PASS`: detail: current corpus unsigned status retained
- `zero_components` `PASS`: detail: conditional zero rows emitted for beta_q branch
- `alpha_guard` `PASS`: detail: alpha/Z_EM overclaim guard emitted
- `claim_gate_closed` `PASS`: detail: local GR/EM claim remains closed
- `next_target` `PASS`: detail: 3791 Z_EM target emitted
- `formalization_clean` `PASS`: detail: no 3790 files written under formalization-workbench
