# 3635 Y5 R2FR source-readout descent zero or JX residual row

**Status:** 3635 derives the source/readout coupling law. If measured source data M_obs descends through q, then partial_Z M_obs=0 and the source part of J_Z dies. If not, the source current is exactly the chain-rule pullback of partial_Z M_obs into the source action, and the J_X/J_Z residual row is active. This turns the coupling worry into a concrete theorem-or-coefficient branch.

**Claim ceiling:** no source-zero, local-GR, R10/R11, WEP, Newton, or PPN claim is allowed from 3635.

## Main result

The coupling question now has a clean theorem-or-coefficient split:

```text
M_obs = M_bar(q(Phi))  =>  partial_Z M_obs = 0
J_Z_source = Pi_M^*[(delta L_source/delta G_obs) partial_Z G_obs
                     + (delta L_source/delta M_obs) partial_Z M_obs
                     + boundary/projector terms].
```

So if the measured source block descends through `q`, source coupling dies. If it does not, the theory has a real `J_X/J_Z` residual current to normalize and test. This is the coupling fork, sharpened.

## Source register

| source_id | path | exists | needle_found | role |
| --- | --- | --- | --- | --- |
| handoff_3634 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3634_NEXT_TARGET.csv | True | True | 3634 handoff selecting source/readout descent as highest-pressure coupling target. |
| dqz_component_3634 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3634_DQZ_COMPONENT_EVALUATION.csv | True | True | source/readout component was identified as the main DqZ bottleneck. |
| filled_dqz_3634 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3634_FILLED_DQZ_ROW.csv | True | True | exact Dq_Z norm formula that this checkpoint refines. |
| coupling_law_3629 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3629_RESPONSE_DOUBLET_COUPLING_LAW.csv | True | True | linearized source-current obstruction for response doublet. |
| jz_coefficients_3629 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3629_JZ_COEFFICIENT_ROWS.csv | True | True | source/Newton residual row already waiting for a J_Z source profile. |
| parent_action_3630 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3630_PARENT_ACTION_CLAUSE.csv | True | True | sufficient source-normalization descent clause from the parent action contract. |
| retained_dq_1667 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1667_RETAINED_DQ_LEAK_ROWS.csv | True | True | retained source/readout leakage row. |
| x_residual_669 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_669_R10_R11_RESIDUAL_VECTOR.csv | True | True | existing X-sector source current row to refine if descent fails. |

## Source-readout descent theorem

| theorem_id | statement | identity | derivation | status | blocks_if_missing |
| --- | --- | --- | --- | --- | --- |
| SDT3635_0_source_quotient_setup | Let M_obs be the measured source/readout block: rest mass, GM calibration, Hamiltonian/source charge, and orbit/readout maps. | M_obs = M_bar(q(Phi)) is the source-readout descent condition | For any fibre direction v_Z in ker(Dq), partial_Z M_obs = DM_bar[Dq(v_Z)] = 0. | CONDITIONAL_THEOREM | if M_obs uses Z directly, the source current J_Z is physical or must be bounded |
| SDT3635_1_source_action_zero | If both geometry and source/readout descend through q, the source action has no linear Z current. | delta_Z S_source = (delta S_source/delta G_obs) partial_Z G_obs + (delta S_source/delta M_obs) partial_Z M_obs = 0 | 3634 supplies the component split; source descent kills the M_obs term and geometry descent kills the G_obs term. | CONDITIONAL_THEOREM | geometry-only descent is insufficient because the M_obs derivative can source Z |
| SDT3635_2_point_particle_source | For a compact source represented by a point-particle/readout action, the Z source has a clean split into geometry and mass-readout parts. | delta_Z S_pp = -int c ds_obs partial_Z mu_obs - 1/2 int mu_obs u^mu u^nu partial_Z g_obs_mn d tau + readout/projector terms | If partial_Z g_obs=0, the leading source current is controlled by partial_Z mu_obs and readout/projector derivatives. | DERIVED_SOURCE_CURRENT_FORM | source mass/readout derivative remains the live coupling row |
| SDT3635_3_orbit_GM_calibration | Newtonian/orbital observables see the combination GM_obs; hiding Z-dependence in measured GM is not a GR reduction. | partial_Z(GM_obs)=G_obs partial_Z M_obs + M_obs partial_Z G_obs + calibration/projector terms | With geometry/G fixed, a nonzero partial_Z M_obs becomes a source-normalization residual feeding R1/R10/R11. | DERIVED_GM_READOUT_GUARD | GM calibration can absorb a fifth-force-looking coupling unless reported as a residual |
| SDT3635_4_verdict | The source-readout theorem is exact, but the live corpus does not sign M_obs=M_bar(q(Phi)). | partial_Z M_obs=0 is sufficient for source silence; not currently proven | This converts the coupling gap into a single branch: prove source descent or score J_X/J_Z. | THEOREM_SOUND_NOT_PARENT_SIGNED | open J_X/source-charge residual row |

## Source current law

| law_id | quantity | formula | meaning | zero_condition | status |
| --- | --- | --- | --- | --- | --- |
| SCL3635_0_general_chain_rule | J_Z_source | J_Z_source = Pi_M^*[(delta L_source/delta G_obs) partial_Z G_obs + (delta L_source/delta M_obs) partial_Z M_obs + (delta L_source/delta B_obs) partial_Z B_obs] | the source current is the chain-rule image of every Z-visible readout component | partial_Z G_obs=partial_Z M_obs=partial_Z B_obs=0 | EXACT_CHAIN_RULE_FORM |
| SCL3635_1_geometry_zero_limit | J_Z_source\|geometry_zero | J_Z_source = Pi_M^*[(delta L_source/delta M_obs) partial_Z M_obs + projector/boundary terms] | even a perfect metric/coframe quotient leaves a source current if measured source mass/readout depends on Z | partial_Z M_obs=0 plus projector/boundary silence | COUPLING_BOTTLENECK_EXPOSED |
| SCL3635_2_positive_operator_profile | Z_profile_from_source | Z^A(x)=-(L^{-1})^{AB}J_B_source + boundary Green terms + O(J^2) | if source descent fails, the local branch produces a residual profile that must be bounded, not waved away | J_B_source=0 and boundary source=0 | PROFILE_ROUTE_FROM_3629_RETAINED |
| SCL3635_3_R10_R11_projection | alpha_or_operator_residual | R_source ~ P_R[L^{-1} Pi_M^*((delta L_source/delta M_obs) partial_Z M_obs)] | this is the bridge from source-readout leakage to R1/R10/R11 residual rows | partial_Z M_obs=0 or projection P_R kills the source theoremically | EXECUTABLE_SYMBOLIC_BRIDGE |

## Source component gate

| component_id | component | required_zero | current_evidence | status | if_nonzero |
| --- | --- | --- | --- | --- | --- |
| SRC3635_0_rest_mass | partial_Z mu_obs | measured rest/source mass is q-owned or fixed external label | 3630 source-normalization clause is sufficient but not parent-signed | OPEN | species/source charge row opens; WEP/source charge and R10/R11 affected |
| SRC3635_1_GM_calibration | partial_Z(GM_obs) | Newtonian calibration uses only EH/source quotient variables or reports residual separately | 3629 Newton/source row missing source mass and range profile | OPEN | delta_Newton_MTS and alpha(lambda) rows become live |
| SRC3635_2_Hamiltonian_source | partial_Z H_source or Pi_M J_H | Hamiltonian/source projector Pi_M is q-owned and orthogonal to extra charge | 3630 PAC3630_4 calls this charge-current orthogonality not parent-derived | OPEN | source normalization and hidden Hamiltonian charge drive J_X/J_Z |
| SRC3635_3_orbit_readout | partial_Z orbit/readout map | orbit and ephemeris readouts are functions of observed metric/source quotient only | retained Dsource_readout_Dq_leak exists | OPEN | orbital residuals and PPN/source projection rows must be scored |
| SRC3635_4_verdict | partial_Z M_obs | all source/readout subcomponents vanish componentwise | no subcomponent zero is parent-signed | SOURCE_DESCENT_NOT_CLAIMED | use J_X source residual row below |

## JX/JZ residual row

| row_id | symbol | value_or_formula | geometry_zero_reduction | units | feeds | zero_condition | fill_level | score_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| JX3635_0_source_readout_residual | J_X_source_or_J_Z_source | Pi_M^*[(delta L_source/delta M_obs) partial_X M_obs + (delta L_source/delta G_obs) partial_X G_obs + boundary/projector terms] | Pi_M^*[(delta L_source/delta M_obs) partial_X M_obs + boundary/projector terms] | source action density per normalized X/Z field; must be fixed by parent field normalization | R1_WEP_source_charge;R10_fifth_force;R11_EH_operator_ledger;orbital_source_projection | M_obs=M_bar(q), G_obs=G_bar(q), and boundary/projector silence | symbolic_executable_law_not_numeric | not_scoreable_until_field_normalization_projection_and_units |

## Decisions

| decision_id | decision | status | next_action |
| --- | --- | --- | --- |
| DEC3635_0_theorem | Source/readout descent is sufficient: M_obs=M_bar(q) implies partial_Z M_obs=0 and kills the source part of J_Z when geometry/boundary also descend. | CONDITIONAL_SOURCE_ZERO_THEOREM | try to parent-sign M_obs as quotient data rather than merely closure-label it |
| DEC3635_1_live_gap | The live corpus does not sign source/readout descent; rest mass, GM calibration, Hamiltonian source, and orbit readout remain open componentwise. | SOURCE_DESCENT_NOT_CLAIMED | keep J_X/J_Z source residual row active |
| DEC3635_2_progress | The coupling gap is now an explicit chain-rule current, not a vague missing coupling. | JX_SYMBOLIC_ROW_FILLED | next checkpoint should choose either parent-sign source mass as q-data or normalize the J_X row for scoring |

## Next target

| target_doc | target_script | objective | success_gate |
| --- | --- | --- | --- |
| 3636-Y5-R2FR-source-mass-quotient-signature-or-JX-normalization.md | scripts/Y5_R2FR_3636_source_mass_quotient_signature_or_JX_normalization.py | attempt to parent-sign measured source mass/GM/Hamiltonian readout as q-data; if that fails, define the field normalization and units needed to make J_X_source scoreable | either M_obs=M_bar(q) is parent-signed for rest mass, GM, Hamiltonian source, and orbit readout, or J_X_source gains explicit normalization, units, and first comparator channel |
