# 539 - Y5 PiM as Hamiltonian Charge Map or Topological Demotion

Generated: 2026-06-04T10:32:08.271503+00:00  
Run: `runs/20260605-044500-Y5-PiM-as-Hamiltonian-charge-map-or-topological-demotion`  
Status: `Y5_PiM_Hamiltonian_charge_map_candidate_written_topological_PiM_demoted_as_independent_proof`  
Claim ceiling: `PiM_Hamiltonian_charge_map_candidate_only_no_epsilon_charge_measured_GM_Newton_PPN_or_local_GR_pass`

## 1. Verdict

The clean repair is available as a candidate, but it is not a promotion.

The move is:

```text
Do not let Pi_M be an independent topological/readout selector.
Define Pi_M^H from the parent Hamiltonian surface charge itself.
Then the measured mass channel is tied to Q_tau by construction at charge level.
```

That repairs the "wrong conserved object" risk only if MTS adopts this Hamiltonian branch and then proves integrability, source-measure glue, zero residuals, and PPN readout.

The old topological `Pi_M` route is demoted as an independent proof unless it is shown to equal this Hamiltonian charge map.

## 2. Hamiltonian PiM Branch Definition

| branch_id | definition | mathematical_form | what_this_fixes | what_remains_open | status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| PH539_0_charge_functional | define the mass functional from the parent Hamiltonian/covariant-phase-space surface charge | ell_H[J_H;tau,S] := 4*pi*G_ref int_S Q_tau[J_H] | the mass readout is tied to the parent action charge rather than a post-fit Pi_M mask | integrability, reference subtraction, source measure, and PPN readout | candidate_definition_not_claim | false |
| PH539_1_charge_representative | represent the Hamiltonian mass charge as a parent-fixed mass cohomology representative | Pi_M^H J_H := ell_H[J_H;tau,S] omega_M^H with int_S omega_M^H=1 | Pi_M becomes a charge-map representative, not an independent conserved object | pointwise equality to the old topological current is not proved | cohomology_level_repair_candidate | false |
| PH539_2_DAT537_4_repair_scope | repair DAT537_4 only at charge/integral level unless stronger equality is proved | (4*pi*G_ref)^-1 int_S Pi_M^H J_H = int_S Q_tau by construction | avoids the conserved-wrong-object failure for measured source charge | does not prove d(Pi_M J_H)=0 off shell or old Pi_M topological equality | repair_candidate_not_promotion | false |
| PH539_3_no_independent_topological_credit | old topological Pi_M earns no derivation credit unless it is shown to equal Pi_M^H | Pi_M^top J_H - Pi_M^H J_H = R_Htop + dB_Htop | prevents the topological current from being counted as measured mass by name alone | R_Htop and boundary flux must be zero or bounded | topological_route_demoted_until_equality | false |
| PH539_4_residual_branch_preserved | if Hamiltonian Pi_M cannot be adopted non-circularly, use residual fill rows | epsilon_PiM_total_abs = \|R_eq\|/M_H + \|I_commutator\|/M_H + \|B_zero_flux\|/M_H + \|T_PiM_beta\| | keeps failure testable rather than rhetorical | source-backed numeric or theorem rows are still missing | fallback_ready_not_filled | false |

## 3. Gate Results

| gate_id | gate | current_result | why_it_matters | valid_for_claim |
| --- | --- | --- | --- | --- |
| HG539_0_parent_charge_integrability | Hamiltonian surface charge Q_tau is integrable with fixed reference and boundary terms | not_yet_derived_for_current_MTS | without integrability, ell_H is not a stable mass functional | false |
| HG539_1_same_source_frame | J_H is the observed matter/source current of the same frame used by clocks/orbits | open_from_537 | otherwise Hamiltonian charge and source mass can describe different frames | false |
| HG539_2_cohomology_representative_fixed | omega_M^H is fixed by parent topology/reference before readout | conditional_standard_branch_only | otherwise Pi_M^H can still become a readout mask | false |
| HG539_3_old_PiM_equivalence | old/topological Pi_M equals the Hamiltonian Pi_M^H up to exact zero-flux terms | not_derived | without this, old Pi_M is demoted as independent proof | false |
| HG539_4_commutator_zero | [d,Pi_M^H]J_H = 0 or its residual is source-backed and below locks | not_derived | charge-map definition does not automatically remove projector/boundary residuals | false |
| HG539_5_source_measure_glue | worldtube source measure equals the Hamiltonian charge before orbital fitting | not_derived | measured GM needs source-measure glue, not only a surface charge definition | false |
| HG539_6_Gauss_PPN_readout | the same charge controls the 1/r metric coefficient and second-order PPN vector | not_reached | local GR requires readout through PPN order | false |

## 4. Topological PiM Demotion Ledger

| old_route | old_claim_risk | new_status | repair_condition | fallback | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| Pi_M^top as independent topological mass current | closed topological current may be a conserved wrong object | demoted_unless_equivalent_to_PiM_H | Pi_M^top J_H = Pi_M^H J_H + dB_zero with zero boundary flux | retain R_Htop/R_eq and commutator residual rows | false |
| Pi_M algebra idempotence | Pi_M^2=Pi_M can be mistaken for d(Pi_M J_H)=0 | algebra_only_no_flux_closure | derive Ward/Euler closure of the Hamiltonian mass channel | source-backed I_commutator or radial mass-drift residual | false |
| Hodge/metric projector representative | metric-dependent projector variation can create hidden stress | retained_variation_debt | delta Pi_M stress is zero/topological or mapped below local locks | projector_stress_beta_equiv row | false |
| late equality multiplier | imposes source normalization by hand | forbidden_as_derivation | multiplier sector must have independent gauge/topological origin and zero stress | closure-only label | false |

## 5. DAT537 Repair Status

| dat537_id | before_539 | after_539 | remaining_blocker | claim_status |
| --- | --- | --- | --- | --- |
| DAT537_4_PiM_Hilbert_identification | fail_for_current_MTS | candidate_repair_if_PiM_redefined_as_Hamiltonian_charge_map | adoption/integrability/source-measure/readout gates HG539_0 through HG539_6 | false |
| DAT537_5_local_readout | not_reached | still_not_reached | requires HG539_5 source-measure glue and HG539_6 Gauss/PPN readout | false |

## 6. Decision

| decision_id | status | meaning | claim_status | next_action |
| --- | --- | --- | --- | --- |
| D539_0_Hamiltonian_PiM_candidate | PiM_Hamiltonian_charge_map_candidate_written | the clean repair is to make Pi_M the parent Hamiltonian charge representative rather than an independent selector | candidate_only | 540-Y5-Hamiltonian-PiM-source-measure-and-PPN-readout-test.md |
| D539_1_topological_PiM_demoted | topological_PiM_not_independent_proof | old Pi_M/topological current must equal the Hamiltonian charge map or remain a residual branch | no_epsilon_charge_credit | 540-Y5-Hamiltonian-PiM-source-measure-and-PPN-readout-test.md |
| D539_2_DAT537_4_not_closed_for_claim | DAT537_4_candidate_repair_not_claim | charge-level identity can be made by definition only if the branch is adopted and downstream gates pass | local_GR_false | 540-Y5-Hamiltonian-PiM-source-measure-and-PPN-readout-test.md |
| D539_3_next_is_source_measure_and_PPN | source_measure_Gauss_PPN_still_required | even the repaired Pi_M branch must still prove measured GM and local readout | Newton_false | 540-Y5-Hamiltonian-PiM-source-measure-and-PPN-readout-test.md |
| D539_4_private_no_push | private_no_github | no public/GitHub action is performed | safe_private_work | continue_private_derivation |

## 7. Source Register

| source_file | role | exists |
| --- | --- | --- |
| 538-Y5-minimal-parent-action-Euler-Ward-test-or-closure-demotion.md | isolates DAT537_4 Pi_M/Hilbert/Hamiltonian identification as blocker | True |
| 537-Y5-Hilbert-worldtube-parent-action-contract-or-PiM-input-fill.md | parent-action contract and DAT537 chain | True |
| 534-Y5-PiM-topological-equality-certificate-or-commutator-bound.md | topological Pi_M equality certificate and wrong-conserved-object warning | True |
| 501-topological-Hilbert-current-equality-or-radial-bound-runner.md | topological-Hilbert equality attempt and Hamiltonian dictionary route | True |
| 454-PiM-parent-symplectic-projector-algebra-attempt.md | conditional Pi_M projector algebra and variation debt | True |
| 510-worldtube-source-measure-glue-or-Meff-residual-runner.md | dressed source charge and EH-style worldtube glue | True |
| 505-parent-Noether-mass-charge-closure-theorem-or-closure-demotion.md | conditional Noether mass-charge closure theorem | True |
| source-intake/mts_residuals/P8_Y5_DAT537_GATE_RESULTS.csv | 538 DAT537 gate results | True |
| source-intake/mts_residuals/P8_Y5_PIM_REPAIR_OR_DEMOTION_OPTIONS.csv | 538 Pi_M repair/demotion options | True |
| source-intake/mts_residuals/P8_Y5_PIM_INPUT_FILL_TEMPLATE.csv | 537 residual input fill branch | True |
| source-intake/mts_residuals/P8_TOPOLOGICAL_HILBERT_EQUALITY_ATTEMPT.csv | 501 topological-Hilbert equality rows | True |
| source-intake/mts_residuals/P8_PiM_parent_symplectic_projector_algebra_CONTRACT.csv | 454 Pi_M symplectic projector algebra contract | True |
| scripts/Y5_PiM_as_Hamiltonian_charge_map_or_topological_demotion.py | this checkpoint generator | True |

## 8. Validation

| check_id | result | detail |
| --- | --- | --- |
| V539_0_source_paths_exist | pass | missing=0 |
| V539_1_prior_538_loaded | pass | dat537_rows=6;repair_option_rows=4 |
| V539_2_old_topological_evidence_loaded | pass | topological_rows=6;projector_contract_rows=9 |
| V539_3_branch_definition_complete | pass | branch_rows=5 |
| V539_4_gate_results_complete | pass | gate_rows=7 |
| V539_5_topological_demotion_explicit | pass | demotion_rows=4 |
| V539_6_no_claim_rows | pass | claim_branch_rows=0;claim_gate_rows=0;claim_demotion_rows=0 |
| V539_7_no_overclaim | pass | PiM_Hamiltonian_branch_adopted=false; epsilon_charge_filled=false; measured_GM=false; Newton=false; PPN=false; local_GR=false |

## 9. Route Update

| route_id | previous_status | new_status | accepted_for_claim | next_target |
| --- | --- | --- | --- | --- |
| PIM_AS_SOURCE_CHARGE | hard_blocker_now_isolated | Hamiltonian_charge_map_candidate_written | false | 540-Y5-Hamiltonian-PiM-source-measure-and-PPN-readout-test.md |
| TOPOLOGICAL_PIM | wrong_conserved_object_risk | demoted_unless_equivalent_to_Hamiltonian_PiM | false | 540-Y5-Hamiltonian-PiM-source-measure-and-PPN-readout-test.md |
| DAT537_4 | fail_for_current_MTS | candidate_repair_not_claim | false | 540-Y5-Hamiltonian-PiM-source-measure-and-PPN-readout-test.md |
| SOURCE_NORMALIZED_NEWTON | still_blocked_by_DAT537_4 | still_blocked_source_measure_and_Gauss_readout | false | 540-Y5-Hamiltonian-PiM-source-measure-and-PPN-readout-test.md |
| LOCAL_GR | still_blocked_PiM_charge_map_and_PPN_not_reached | still_blocked_PPN_readout_not_reached | false | 540-Y5-Hamiltonian-PiM-source-measure-and-PPN-readout-test.md |

## 10. Claim Ceiling

Allowed:

```text
MTS has a candidate Hamiltonian-charge-map definition of Pi_M.
The old topological Pi_M route is demoted unless it equals the Hamiltonian charge map.
DAT537_4 has a candidate repair path, not a completed proof.
```

Forbidden:

```text
MTS has adopted/proved the Hamiltonian Pi_M branch.
MTS has filled epsilon_charge.
MTS has derived measured GM, source-normalized Newton, beta, PPN, or local GR.
```

## 11. Practical Read

This is probably the right conceptual pivot. In GR-like mathematics the mass charge is not a free selector; it is the Hamiltonian/Noether charge. If MTS wants derived local GR, `Pi_M` should become that parent charge map. Any separate topological current can still be useful, but only as a representation of the same charge or as a bounded residual.

## 12. Next Target

`540-Y5-Hamiltonian-PiM-source-measure-and-PPN-readout-test.md`

Next: test the Hamiltonian `Pi_M^H` branch against source-measure glue and weak-field/PPN readout. If it cannot produce measured GM and the PPN vector, the repair remains only a cleaner notation.
