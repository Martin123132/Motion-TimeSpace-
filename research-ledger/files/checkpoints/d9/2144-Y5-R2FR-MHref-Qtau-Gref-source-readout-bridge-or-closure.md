# 2144 - Y5/R2FR M_H_ref, Q_tau, G_ref Source-Readout Bridge Or Closure

## Current Verdict

2144 does **not** close the measured-source bridge. The equality `mu=G_ref M_H_ref/c^2=GM_orbital/c^2` is still not parent-signed, because the Hamiltonian source-measure mismatch `Delta_Hsrc` remains unresolved.

But this is useful progress, not circling. The vague 2143 quantity `epsilon_mu` is now decomposed into an explicit no-cancellation source object: `epsilon_mu <= epsilon_Gref + epsilon_Hsrc_abs + epsilon_Gauss + epsilon_PPN + epsilon_readout`, with `epsilon_Hsrc_abs` inherited from the 1795 `Delta_Hsrc` component pack.

So the 2143 local K-channel bound becomes `2.000000E-122*(2*(epsilon_Gref+epsilon_Hsrc_abs+epsilon_Gauss+epsilon_PPN+epsilon_readout)+6*epsilon_r+epsilon_frame)`. That is not a claim, but it tells us exactly where the remaining local-GR/Newton source-normalization debt lives.

## Source Register

| source_id | source_path | path_exists | needles_found | role | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| SRC2144_00_2143_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\2143-Y5-R2FR-local-curvature-operator-norm-and-source-bridge-bound.md | true | true | 2143 reduces deltaK to source/readout fractions and selects the bridge as the bottleneck. | false |
| SRC2144_01_2143_validation | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_2143_VALIDATION.csv | true | true | 2143 validation confirms the previous checkpoint. | false |
| SRC2144_02_2143_next | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2143_NEXT_TARGET.csv | true | true | 2143 handoff requires the M_H_ref/Q_tau/G_ref source-readout bridge. | false |
| SRC2144_03_2143_runner | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2143_OPERATOR_BOUND_RUNNER.csv | true | true | machine-readable operator bound to be updated by 2144. | false |
| SRC2144_04_1339_source_GM | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1339-Y5-R10-RAB-source-closure-to-EH-left-hand-local-GR-reduction-gate.md | true | true | 1339 blocks source-GM transfer and measured Newtonian calibration. | false |
| SRC2144_05_1008_Qtau_MHref | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1008-Y5-R10-parent-theta-Qtau-extraction-or-charge-decomposition-runner.md | true | true | 1008 blocks parent Q_tau extraction and M_H_ref denominator promotion. | false |
| SRC2144_06_1793_source_owner | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1793-Y5-R2FR-Y5-source-charge-owner-and-Y6-extra-stress-gate-or-finite-coupling-pack.md | true | true | 1793 writes the exact source owner chain and keeps it inactive. | false |
| SRC2144_07_1794_PiM_tau | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1794-Y5-R2FR-parent-PiM-observed-time-generator-or-finite-Y5-pack.md | true | true | 1794 identifies Hamiltonian Pi_M and observed-time normalization as the cleanest route. | false |
| SRC2144_08_1795_Delta_Hsrc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1795-Y5-R2FR-Hamiltonian-PiM-adoption-or-Delta-Hsrc-component-pack.md | true | true | 1795 stages Delta_Hsrc as the central source-measure mismatch and component envelope. | false |


## Source Anchors

| anchor_id | source_path | line_number | snippet | role | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| ANCH2144_0_2143_bridge | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\2143-Y5-R2FR-local-curvature-operator-norm-and-source-bridge-bound.md | 7 | Using the 2142 coefficient, the K-channel action residual becomes `2.000000E-122*(2 eps_mu + 6 eps_r + eps_frame)`. This is much sharper than the previous `MISSING_DELTAK_NORM`, but it is still not a PPN/Newton claim because `mu=G_ref M_H_ref/c^2=GM_orbital/c^2` is not parent-signed. | 2143 bridge equation | false |
| ANCH2144_1_2143_bound | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\2143-Y5-R2FR-local-curvature-operator-norm-and-source-bridge-bound.md | 7 | Using the 2142 coefficient, the K-channel action residual becomes `2.000000E-122*(2 eps_mu + 6 eps_r + eps_frame)`. This is much sharper than the previous `MISSING_DELTAK_NORM`, but it is still not a PPN/Newton claim because `mu=G_ref M_H_ref/c^2=GM_orbital/c^2` is not parent-signed. | 2143 K-channel bound | false |
| ANCH2144_2_1339_GM_transfer | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1339-Y5-R10-RAB-source-closure-to-EH-left-hand-local-GR-reduction-gate.md | 44 | \| EHGate1339_6_source_GM_transfer \| EH mass parameter equals Hilbert/worldtube source charge and measured orbital GM \| mu_EH = G_ref M_H[worldtube] = GM_orbital/c^2 \| NOT_DERIVED \| Newtonian mechanics reduction can be attempted \| Poisson-looking algebra cannot be identified with measured Newtonian gravity \| True \| False \| False \| | source-GM blocker | false |
| ANCH2144_3_1008_MHref | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1008-Y5-R10-parent-theta-Qtau-extraction-or-charge-decomposition-runner.md | 101 | \| CG1008_5_MHref \| M_H_ref denominator can pass \| false \| positive same-frame denominator depends on integrable fixed-reference H_tau \| false \| false \| | M_H_ref blocker | false |
| ANCH2144_4_1793_source_chain | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1793-Y5-R2FR-Y5-source-charge-owner-and-Y6-extra-stress-gate-or-finite-coupling-pack.md | 33 | \| Y5SC1793_0_observable_split \| observed local source strength is split into parent source charge plus explicit extra source-normalization channels \| mu_obs = G_eff M_H[Pi_M J_H] + mu_extra = G_eff M_H(1 + epsilon_mu) \| Y5 cannot hide as fitted GM; deviations are theorem-zero or finite residual rows \| DEFINITION_WRITTEN_NOT_PARENT_DERIVED \| False \| | source-normalization chain | false |
| ANCH2144_5_1794_PiMH | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1794-Y5-R2FR-parent-PiM-observed-time-generator-or-finite-Y5-pack.md | 5 | 1794 narrows the source-normalized Newton route to the actual parent objects. The mass projector cannot be a post-readout mask: it must be `Pi_M^H`, a Hamiltonian/covariant-phase-space mass charge map, or the old/topological `Pi_M` must be proven equivalent to it. The observed time generator `tau_obs` must also be selected and normalized by parent boundary/clock data before orbital/source readout. | Hamiltonian Pi_M route | false |
| ANCH2144_6_1795_Delta_Hsrc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1795-Y5-R2FR-Hamiltonian-PiM-adoption-or-Delta-Hsrc-component-pack.md | 9 | `Delta_Hsrc := G_ref^-1 int_S Q_tau^MTS - H_ref - M_eff[Pi_M^H J_H^dress]`. | central source mismatch | false |
| ANCH2144_7_1795_component_pack | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1795-Y5-R2FR-Hamiltonian-PiM-adoption-or-Delta-Hsrc-component-pack.md | 62 | \| DHC1795_7_total_abs_envelope \| epsilon_Hsrc_abs \| strict no-cancellation Delta_Hsrc absolute envelope \| sum_abs(DHC1795_0..DHC1795_6) \| all component rows theorem-zero or source-backed; no cancellation credit \| REJECT_CURRENT_DELTA_HSRC_PACK \| False \| False \| False \| | no-cancellation component envelope | false |
| ANCH2144_8_1795_MHref_gate | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1795-Y5-R2FR-Hamiltonian-PiM-adoption-or-Delta-Hsrc-component-pack.md | 71 | \| AEG1795_4_MHref \| same-frame Hilbert mass reference \| positive M_H_ref with units/source path in observed coframe \| MISSING_M_H_REF \| False \| | M_H_ref source gate | false |


## Bridge Clauses

| clause_id | object | exact_contract | current_status | blocker | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| BRIDGE2144_0_mu_target | measured exterior mass parameter | mu_obs/c^0 = G_ref*M_H_ref/c^2 = GM_orbital/c^2 in the same observed frame | TARGET_WRITTEN_NOT_SIGNED | source charge and orbital readout are not yet proved equal | false |
| BRIDGE2144_1_Qtau_to_MHref | Q_tau^MTS to source mass | M_H_ref = G_ref^-1 int_S Q_tau^MTS - H_ref for a fixed integrable reference and selected tau_obs | BLOCKED_BY_DELTA_HSRC | 1795 keeps Delta_Hsrc nonzero/noncomputed | false |
| BRIDGE2144_2_PiMH_source_measure | Hamiltonian Pi_M^H source readout | G_ref^-1 int_S Q_tau^MTS-H_ref = M_eff[Pi_M^H J_H^dress] | CONDITIONAL_LEMMA_ONLY | Pi_M adoption/equivalence, source functor, commutator, boundary and extra-charge silence are unsigned | false |
| BRIDGE2144_3_Gref | G_ref normalization | G_ref is fixed before local/orbital residual readout and not fitted to absorb Delta_Hsrc | UNSIGNED | no parent normalization certificate tied to source charge yet | false |
| BRIDGE2144_4_radius_frame | radius/readout frame | r_obs, tau_obs, coframe and orbital/clock/photon readout use the same parent-selected observed representative | UNSIGNED | same-frame and pre-readout selection remain gate conditions | false |
| BRIDGE2144_5_no_shortcut | Newtonian calibration guardrail | Poisson/Gauss shape cannot prove measured GM; it can only be downstream after source-measure equality | POLICY_RETAINED | prevents circular proof by orbital fitting | false |
| BRIDGE2144_6_verdict | source-readout bridge | all clauses above close in one parent action before local GR/Newton claim | SOURCE_READOUT_BRIDGE_NOT_CLOSED | Delta_Hsrc, G_ref, tau_obs/r_obs and PPN followthrough remain open | false |


## Epsilon Closure Rows

| epsilon_id | symbol | definition | closure_law | current_status | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| EPS2144_0_epsilon_mu_definition | epsilon_mu | fractional uncertainty/residual in the source mass parameter entering K=48mu^2/r^6 | epsilon_mu := \|delta ln mu_obs\| <= epsilon_Gref + epsilon_Hsrc_abs + epsilon_Gauss + epsilon_PPN + epsilon_readout | STRICT_ABSOLUTE_ENVELOPE_NONCLAIM | false |
| EPS2144_1_epsilon_Hsrc_abs | epsilon_Hsrc_abs | Hamiltonian source-measure mismatch from 1795 | epsilon_Hsrc_abs=(\|Delta_integrability\|+\|R_eq\|+\|I_commutator\|+\|B_ref\|+\|Delta_extra_charge\|+\|Delta_tau_MHref\|+\|Delta_Gauss_PPN\|)/M_H_ref | IMPORT_FROM_1795_COMPONENTS_MISSING | false |
| EPS2144_2_epsilon_r | epsilon_r | fractional radius/readout residual in Schwarzschild reference K | epsilon_r <= epsilon_radius_obs + epsilon_tau_obs + epsilon_coframe + epsilon_orbit_model + epsilon_boundary_frame | SOURCE_BACKED_VALUES_MISSING | false |
| EPS2144_3_epsilon_frame | epsilon_frame | projector/coframe/representative mismatch in the deltaK/K conversion | epsilon_frame <= epsilon_same_frame + epsilon_pre_readout + epsilon_Dq_kernel + epsilon_projector_shadow | SOURCE_BACKED_VALUES_MISSING | false |
| EPS2144_4_eps_combo_substitution | eps_combo_2144 | 2143 source/readout combo after source-bridge decomposition | 2*epsilon_mu + 6*epsilon_r + epsilon_frame <= 2*(epsilon_Gref + epsilon_Hsrc_abs + epsilon_Gauss + epsilon_PPN + epsilon_readout)+6*epsilon_r+epsilon_frame | BOUND_REWRITTEN_NOT_NUMERIC | false |
| EPS2144_5_verdict | epsilon closure | the epsilons are named and decomposed but not proved small | local K-channel remains a symbolic nonclaim bound until each component is theorem-zero or source-backed | CLOSURE_ROWS_STAGED_NONCLAIM | false |


## Delta_Hsrc Component Rows

| component_id | component | formula | required_input | current_status | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| DHSRC2144_0_definition | Delta_Hsrc | Delta_Hsrc := G_ref^-1 int_S Q_tau^MTS - H_ref - M_eff[Pi_M^H J_H^dress] | parent Q_tau, fixed H_ref, Pi_M^H, dressed source current, units | IDENTITY_IMPORTED_NONCLAIM | false |
| DHSRC2144_1_integrability | Delta_integrability | failure of Q_tau to be integrable with fixed reference | Hamiltonian charge integrability/reference certificate or finite residual row | MISSING_INTEGRABILITY_REFERENCE_LOCK | false |
| DHSRC2144_2_R_eq | R_eq | Hilbert/source/topological equality residual | same-worldtube equality theorem or source-backed mismatch over M_H_ref | MISSING_SOURCE_EQUALITY_INPUT | false |
| DHSRC2144_3_I_commutator | I_commutator | M_H_ref^-1 int_A [d,Pi_M]J_H | fixed-chainmap theorem or finite annulus/profile row | MISSING_COMMUTATOR_ZERO_OR_PROFILE | false |
| DHSRC2144_4_boundary_reference | B_ref | boundary/reference/improvement offset in source charge | exact boundary flux theorem or finite reference convention row | MISSING_BOUNDARY_REFERENCE_INPUT | false |
| DHSRC2144_5_extra_charge | Delta_extra_charge | sum of independent non-EH/domain/memory/range/frame Hamiltonian mass channels | channelwise silence theorem or source-backed absolute envelope | MISSING_EXTRA_CHARGE_CHANNEL_INPUT | false |
| DHSRC2144_6_tau_MHref_readout | Delta_tau_MHref | tau_obs, M_H_ref denominator and same-frame readout mismatch | tau_obs lock, positive M_H_ref, observed coframe/radius/source paths | MISSING_TAU_MHREF_READOUT_INPUT | false |
| DHSRC2144_7_Gauss_PPN | Delta_Gauss_PPN | downstream orbital Gauss and PPN source-stability mismatch | GM_orbit, PPN vector, alpha(lambda), partial_r ln mu_obs | MISSING_GAUSS_PPN_INPUT | false |
| DHSRC2144_8_total | epsilon_Hsrc_abs | strict no-cancellation sum of components divided by M_H_ref | all components theorem-zero or source-backed with units | REJECT_CURRENT_DELTA_HSRC_PACK_NONCLAIM | false |


## Operator Bound Update

| bound_id | object | expression | current_status | valid_for_claim |
| --- | --- | --- | --- | --- |
| BOUND2144_0_2143_import | 2143 K-channel action residual | \|D_S^K deltaK\| <= 2.000000E-122*(2 epsilon_mu + 6 epsilon_r + epsilon_frame) | IMPORTED_FROM_2143 | false |
| BOUND2144_1_substitute_epsilon_mu | source-decomposed bound | \|D_S^K deltaK\| <= 2.000000E-122*(2*(epsilon_Gref+epsilon_Hsrc_abs+epsilon_Gauss+epsilon_PPN+epsilon_readout)+6*epsilon_r+epsilon_frame) | SYMBOLIC_SUBSTITUTION_NONCLAIM | false |
| BOUND2144_2_if_zero_theorem | ideal theorem branch | if Delta_Hsrc=0 and G_ref/tau_obs/r_obs/frame gates close, the K-channel residual becomes controlled by downstream readout/PPN residuals only | CONDITIONAL_ROUTE_ONLY | false |
| BOUND2144_3_if_finite_pack | finite residual branch | if Delta_Hsrc components are source-backed, epsilon_mu can be bounded by epsilon_Gref+epsilon_Hsrc_abs+epsilon_Gauss+epsilon_PPN+epsilon_readout | FINITE_PACK_NOT_SCOREABLE | false |
| BOUND2144_4_verdict | local curvature bridge | 2144 closes no claim, but replaces vague epsilon_mu with Delta_Hsrc and readout component rows | BRIDGE_SHARPENED_NOT_CLOSED | false |


## Claim Gates

| gate_id | gate | gate_pass | rationale | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| GATE2144_0_sources | 2143/1339/1008/1793/1794/1795 evidence validates | true | all source paths and needles are checked | false | false |
| GATE2144_1_bridge_contract_written | exact source-readout bridge contract written | true | mu, Q_tau, M_H_ref, G_ref and frame requirements are explicit | false | false |
| GATE2144_2_epsilon_decomposition | epsilon_mu/r/frame decomposition staged | true | 2143 eps_combo is rewritten through Delta_Hsrc/readout rows | false | false |
| GATE2144_3_bridge_closed | mu=G_ref*M_H_ref/c^2=GM_orbital/c^2 derived | false | Delta_Hsrc, G_ref and readout-frame clauses remain unsigned | false | false |
| GATE2144_4_Delta_Hsrc_zero | Delta_Hsrc=0 theorem | false | 1795 retains integrability, R_eq, commutator, boundary, extra charge and M_H_ref blockers | false | false |
| GATE2144_5_finite_score | finite epsilon_mu score allowed | false | component rows have no source-backed values/units yet | false | false |
| GATE2144_6_local_GR_Newton_claim | local GR/Newton claim allowed | false | source-normalized Newton remains blocked by Delta_Hsrc and PPN/source stability gates | false | false |


## Decision Ledger

| decision_id | decision | because | next_action | valid_for_claim |
| --- | --- | --- | --- | --- |
| DEC2144_0 | BRIDGE_NOT_CLOSED | no parent action signs Q_tau/M_H_ref/G_ref/readout equality in one chain | do not claim local GR/Newton | false |
| DEC2144_1 | EPSILON_MU_NOW_HAS_OWNER | epsilon_mu is no longer a vague fudge factor; it is controlled by epsilon_Gref plus Delta_Hsrc/readout pieces | attack Delta_Hsrc components | false |
| DEC2144_2 | DELTA_HSRC_IS_PRIMARY_SOURCE_BLOCKER | 1795 supplies the exact mismatch object and no-cancellation component envelope | try integrability/reference lock first | false |
| DEC2144_3 | NEXT_1796_STYLE_INTEGRABILITY_OR_FIRST_COMPONENT_ROW | the least circular path is to sign Q_tau integrability/reference before orbital calibration | 2145 imports 1795/2144 and targets Delta_integrability or Pi_M^H adoption theorem | false |


## Next Target

| route_id | next_target | script | objective | forbidden_shortcuts | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| NEXT2144_0_2145 | 2145-Y5-R2FR-Delta-Hsrc-integrability-reference-lock-or-first-source-row.md | scripts/Y5_R2FR_Delta_Hsrc_integrability_reference_lock_or_first_source_row_2145.py | Try to prove Q_tau integrability and fixed-reference silence for the Hamiltonian mass functional used in Delta_Hsrc; if it fails, emit the first strict source-backed/nonclaim Delta_integrability residual row. | orbital GM fitting as proof; importing EH mass as MTS mass; cancellation credit among Delta_Hsrc components; local GR/Newton/PPN/R10 claim; formalization-workbench edits; GitHub action | false |


## Branch Copies

| copy_id | destination | path_exists | row_count | parse_ok | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| COPY2144_0_source_weight_docs | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\source-weight\docs\AFRAME_MHREF_QTAU_GREF_BRIDGE_2144_NONCLAIM.csv | true | 18 | true | false |
| COPY2144_1_branch_locked_wep | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope\branch_locked_wep\residuals\P8_Y5_PARENT_QLOC_2144_EPSILON_SOURCE_BRIDGE_NONCLAIM.csv | true | 11 | true | false |
| COPY2144_2_acquisition_queue | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\rab-sector\acquisition-queue\JR2144_DELTA_HSRC_COMPONENT_QUEUE.csv | true | 10 | true | false |


## Validation

| check_id | status | detail | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- |
| VAL2144_00_sources | PASS | 2143/1339/1008/1793/1794/1795 sources validate | false | false |
| VAL2144_01_anchors | PASS | line anchors for bridge, bound, Q_tau, M_H_ref and Delta_Hsrc exist | false | false |
| VAL2144_02_bridge_not_closed | PASS | source-readout bridge is explicitly not closed | false | false |
| VAL2144_03_epsilon_decomposition | PASS | epsilon_mu/r/frame closure rows staged | false | false |
| VAL2144_04_Delta_Hsrc_pack | PASS | Delta_Hsrc component pack imported and rejected nonclaim | false | false |
| VAL2144_05_operator_update | PASS | 2143 operator bound rewritten through source components | false | false |
| VAL2144_06_claim_gates | PASS | epsilon decomposition gate passes while local claim gate fails | false | false |
| VAL2144_07_decisions | PASS | decision ledger selects integrability/reference or first component row | false | false |
| VAL2144_08_next | PASS | next target is 2145 | false | false |
| VAL2144_09_branch_copies | PASS | branch copies exist and parse | false | false |
| VAL2144_10_csv_parse | PASS | all generated CSVs parse cleanly | false | false |
| VAL2144_11_no_claim_flags | PASS | no generated row allows a claim | false | false |
| VAL2144_12_formalization_clean | PASS | formalization-workbench untouched by 2144 | false | false |
| VAL2144_13_no_pycache | PASS | scripts __pycache__ removed | false | false |
| VAL2144_OVERALL | PASS | 2144 rewrites the measured-source bridge through Delta_Hsrc/epsilon closure rows but keeps local GR/Newton nonclaim. | false | false |
