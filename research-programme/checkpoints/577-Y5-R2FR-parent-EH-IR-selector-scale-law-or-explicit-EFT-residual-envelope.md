# 4561 - parent EH/IR selector scale law or explicit EFT residual envelope

Generated: `2026-07-06T10:13:25.168250+00:00`  
Marker: `PPC4161_PARENT_EH_IR_SELECTOR_SCALE_LAW_OR_EXPLICIT_EFT_RESIDUAL_ENVELOPE_4561`  
Decision: `CONDITIONAL_EH_IR_SELECTOR_REDERIVED_PARENT_SIGNATURE_FAILS_RESIDUAL_EFT_ENVELOPE_RETAINED`  
Claim: `L-403` remains private, conditional and nonclaim.

## What Moved

4561 takes the selected 4560 root target seriously: the private local branch is clean, but public parent derivation needs the EH/IR principal block.

The best theorem currently available is conditional:

```text
A_MF
+ local parity-even covariant four-form
+ two-derivative / one-curvature IR order
+ no extra light local modes
+ same-coframe matter/EM
+ routed boundary
=> EC/Palatini principal block
=> S_EH[g_obs] + boundary when torsion/nonmetricity are silent.
```

That is mathematically useful, but it is not yet an MTS parent derivation. The current corpus still lacks:

- parent origin of `A_MF`;
- parent scale law selecting two-derivative IR order;
- parent proof that extra light torsion/scalar/vector/disformal/memory modes are zero, heavy or bounded.

So the disciplined result is:

```text
conditional EH/IR selector = written
current parent EH derivation = false
residual EFT envelope = retained
```

## Conditional EH Selector Theorem

| theorem_id | clause | statement | derived_status | failure_if_unsigned | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| TH4561_0_variables | motion-frame Cartan variables | If A_MF is parent-owned, e^A=D_omega X^A+B^A and omega^AB are parent-covariant variables, with g_obs=eta_AB e^A e^B. | conditional_on_A_MF_parent_signature | coframe and connection remain effective GR infrastructure, not MTS-derived variables | False |
| TH4561_1_local_covariant_classification | local parity-even covariant four-form classification | At leading two-derivative / one-curvature IR order, the unsuppressed parity-even Cartan geometry term is EC/Palatini plus vacuum term. | conditional_selector_theorem | higher-curvature, torsion-square, disformal and memory terms remain residual coefficients | False |
| TH4561_2_scale_law | parent IR scale separation | A parent scale law must rank two-derivative EC/Palatini terms above R^2, torsion kinetic, disformal and memory terms in the local <=2PN branch. | not_parent_derived_currently | EH is an effective leading ansatz rather than a parent-selected principal block | False |
| TH4561_3_no_extra_light_modes | no unscreened extra local modes | No light torsion, scalar, vector, disformal, R^2 or memory pole can survive below the local PPN/R10/clock scale unless it is bounded by an explicit residual row. | not_parent_derived_currently | gamma/beta/R10/clock/PPN compatibility remains branch-conditional | False |
| TH4561_4_Palatini_to_EH | torsion/nonmetricity resolution | If torsion/nonmetricity are algebraic and zero or bounded in the compact spinless local branch, S_EC reduces to S_EH[g_obs] plus routed boundary. | conditional_reduction | torsion/nonmetricity residuals reopen preferred-frame, WEP, spin and source-coupling rows | False |
| TH4561_5_verdict | EH/IR parent selector | A clean conditional theorem exists, but the current corpus does not derive the parent EH/IR selector because A_MF parent ownership, IR scale law and no-extra-light-mode clauses remain unsigned. | conditional_true_current_parent_claim_false | use explicit residual EFT envelope and effective-GR branch language | False |


## Parent Scale-Law Audit

| audit_id | required_parent_input | current_evidence | verdict | repair_route | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| PA4561_0_A_MF_parent_origin | A_MF motion-frame gauge redundancy owned by parent action | 4182 says A_MF parent signature is not found; 4183 treats it as adoption-ready candidate | FAIL_PARENT_SIGNATURE | derive A_MF from motion/time/space primitives or freeze it as an explicit axiom | False |
| PA4561_1_IR_order_scale_law | parent scale hierarchy selecting two-derivative / one-curvature local IR order | 4184 uses IR order as selector assumption; 4185 maps c_R2/M_R as residual | FAIL_PARENT_SCALE_LAW | derive M_* suppression or source c_R2/M_R bounds in PPN/R10/orbital arenas | False |
| PA4561_2_no_extra_light_modes | no light torsion/scalar/vector/disformal/memory modes in local branch | 4181 extra-mode gates require zero_or_bound; 4184 residual ledger keeps c_T,c_R2,c_D,c_Gamma,c_bdy,delta_kappa | FAIL_UNTIL_ZERO_OR_BOUND | prove each coefficient zero/heavy or fill finite residual source rows | False |
| PA4561_3_same_coframe_source | matter and Maxwell-Hodge see the same observed coframe | private selector clause exists, global parent adoption still open | PRIVATE_NOT_GLOBAL | derive parent same-coframe functor or retain c_D/WEP/clock/EM propagation bounds | False |
| PA4561_4_boundary_routing | boundary/topological terms fixed, exact or Hamiltonian-routed | private boundary route exists, global boundary/no-flux remains unsigned | PRIVATE_NOT_GLOBAL | derive global compact-collar support/no-flux theorem or retain c_bdy bounds | False |


## Residual EFT Envelope Refresh

| residual_id | coefficient | meaning | test_arena | current_value | envelope_rule | next_action | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RE4561_0_cT | c_T | torsion-square / spin-torsion coefficient | PPN preferred-frame; spin coupling; R10/contact | MISSING_PARENT_ZERO_OR_NUMERIC_BOUND | zero_or_heavy_or_explicit_bound_required_before_public_local_GR_claim | derive torsion silence or source c_T bound | False |
| RE4561_1_cR2 | c_R2/M_R | curvature-square massive scalar/tensor pole | R10 alpha(lambda); orbital precession; beta/gamma | MISSING_PARENT_ZERO_OR_NUMERIC_BOUND | zero_or_heavy_or_explicit_bound_required_before_public_local_GR_claim | derive parent scale gap M_R or source full R10/orbital bound | False |
| RE4561_2_cD | c_D | disformal/second metric/source coframe split | WEP; clocks; EM propagation; Poynting stress | MISSING_PARENT_ZERO_OR_NUMERIC_BOUND | zero_or_heavy_or_explicit_bound_required_before_public_local_GR_claim | derive same-coframe parent functor or source WEP/clock bounds | False |
| RE4561_3_cGamma | c_Gamma | local memory support/projector residual | PPN; clocks; R10; local G variation | MISSING_PARENT_ZERO_OR_NUMERIC_BOUND | zero_or_heavy_or_explicit_bound_required_before_public_local_GR_claim | derive memory support silence or source c_Gamma profile coefficients | False |
| RE4561_4_cbdy | c_bdy | unrouted boundary/edge charge | Hamiltonian mass leakage; radiation/transition current; R10 edge | MISSING_PARENT_ZERO_OR_NUMERIC_BOUND | zero_or_heavy_or_explicit_bound_required_before_public_local_GR_claim | derive boundary primitive/no-flux or source edge-bound rows | False |
| RE4561_5_deltaKappa | delta_kappa | source-coupling drift / kappa normalization residual | Newton coefficient; orbital GM; clock/local G variation | MISSING_PARENT_ZERO_OR_NUMERIC_BOUND | zero_or_heavy_or_explicit_bound_required_before_public_local_GR_claim | derive parent kappa scale law or keep G_cal calibrated only | False |


## Promotion Gates

| gate_id | requirement | status | claim_effect | valid_for_claim |
| --- | --- | --- | --- | --- |
| PG4561_0_conditional_theorem | conditional EC/Palatini->EH selector theorem written | PASS_CONDITIONAL | usable theorem route, not parent proof | False |
| PG4561_1_parent_signature | A_MF, IR scale law and no-extra-light-mode clauses parent-derived | FAIL_UNSIGNED | public local-GR derivation remains blocked | False |
| PG4561_2_residual_EFT | every excluded invariant has parent-zero/heavy proof or numeric bound | FAIL_RESIDUALS_OPEN | residual EFT envelope retained | False |
| PG4561_3_next_target | next derivation target attacks first missing parent input | PASS_NEXT_SELECTED | next target = A_MF origin from motion/time/space or explicit axiom freeze | False |


## Decision

| decision_id | decision | summary | claim_id | valid_for_claim |
| --- | --- | --- | --- | --- |
| DEC4561_0 | CONDITIONAL_EH_IR_SELECTOR_REDERIVED_PARENT_SIGNATURE_FAILS_RESIDUAL_EFT_ENVELOPE_RETAINED | 4561 rederives the conditional EH/IR selector: A_MF plus local parity-even two-derivative IR order, no extra light modes, same-coframe matter/EM and routed boundary selects EC/Palatini and reduces to EH when torsion/nonmetricity are silent. Current MTS still fails parent promotion because A_MF parent origin, IR scale law and no-extra-light-mode proofs are unsigned. The explicit EFT residual envelope is retained. | L-403 | False |


## Next Target

| next_target | route | why | success_condition | valid_for_claim |
| --- | --- | --- | --- | --- |
| 4562-Y5-R2FR-A-MF-parent-origin-from-motion-time-space-or-effective-axiom-freeze.md | best_forward_route | A_MF parent ownership is the first gate in the EH/IR selector chain; without it, coframe and connection are effective GR inputs rather than MTS-derived variables. | Derive A_MF from motion/time/space parent primitives, or freeze it explicitly as an adopted axiom and move residual EFT bounds forward without claiming parent derivation. | False |


## Source Register

| source_id | label | source_path | exists | needle | needle_found | role | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SRC4561_00_4560_next | 4560 selected EH/IR root | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\576-PPC4161-local-scorecard-closure-to-parent-signature-gap-map.md | True | next target is EH/IR selector scale law | True | 4561 parent EH/IR selector theorem attempt | False |
| SRC4561_01_4181_doc | 4181 EH origin demotion | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\4181-Y5-R2FR-EH-local-metric-principal-block-origin-or-effective-GR-demotion.md | True | strong formal candidate, not a completed derivation | True | 4561 parent EH/IR selector theorem attempt | False |
| SRC4561_02_4182_doc | 4182 A_MF parent signature missing | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\4182-Y5-R2FR-motion-frame-symmetry-parent-signature-or-effective-GR-label.md | True | does not yet parent-sign the axiom `A_MF` | True | 4561 parent EH/IR selector theorem attempt | False |
| SRC4561_03_4183_doc | 4183 A_MF consequences | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\4183-Y5-R2FR-motion-frame-axiom-adoption-consequences-or-effective-GR-test-contract.md | True | does not by itself derive the Einstein-Cartan/Palatini action | True | 4561 parent EH/IR selector theorem attempt | False |
| SRC4561_04_4184_doc | 4184 conditional Palatini selector | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\4184-Y5-R2FR-Palatini-IR-normal-form-selector-under-AMF-or-residual-EFT-bound.md | True | selector assumptions are not yet fully parent-derived | True | 4561 parent EH/IR selector theorem attempt | False |
| SRC4561_05_4185_doc | 4185 residual coefficient map | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\4185-Y5-R2FR-extra-invariant-residual-coefficient-map-to-PPN-R10-clocks-or-parent-scale-law.md | True | c_D, delta_kappa, c_Gamma, c_T, c_R2/M_R, c_bdy | True | 4561 parent EH/IR selector theorem attempt | False |
| SRC4561_06_4181_chain | 4181 EH theorem chain | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4181_EH_ORIGIN_THEOREM_CHAIN.csv | True | EHO4181_2_two_derivative_normal_form | True | 4561 parent EH/IR selector theorem attempt | False |
| SRC4561_07_4181_extra | 4181 extra mode gates | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4181_EXTRA_MODE_SILENCE_GATES.csv | True | XMG4181_3_higher_curvature | True | 4561 parent EH/IR selector theorem attempt | False |
| SRC4561_08_4184_axioms | 4184 selector axiom set | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4184_IR_SELECTOR_AXIOM_SET.csv | True | SEL4184_2_IR_order | True | 4561 parent EH/IR selector theorem attempt | False |
| SRC4561_09_4184_theorem | 4184 Palatini theorem chain | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4184_PALATINI_REDUCTION_THEOREM_CHAIN.csv | True | TH4184_1_classification | True | 4561 parent EH/IR selector theorem attempt | False |
| SRC4561_10_4184_residuals | 4184 residual EFT ledger | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4184_RESIDUAL_EFT_BOUND_LEDGER.csv | True | RB4184_1_cR2 | True | 4561 parent EH/IR selector theorem attempt | False |
| SRC4561_11_4185_status | 4185 residual status | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4185_STATUS.csv | True | all_coefficients_numeric_or_parent_zero | True | 4561 parent EH/IR selector theorem attempt | False |


## Validation

| validation_id | check | status | details |
| --- | --- | --- | --- |
| VAL4561_0_sources | all cited source paths exist and needles are found | PASS | 12/12 sources verified |
| VAL4561_1_theorem | conditional EH/IR selector theorem includes A_MF, EC/Palatini, IR order and EH reduction | PASS | 6 theorem rows checked |
| VAL4561_2_parent_audit | parent audit blocks current EH derivation on explicit unsigned inputs | PASS | 5 audit rows checked |
| VAL4561_3_residuals | residual EFT envelope contains all open coefficients and keeps them unclaimed | PASS | 6 residual rows checked |
| VAL4561_4_gates | promotion gates pass conditional theorem but block parent claim and select next target | PASS | promotion gates checked |
| VAL4561_5_docs | post and formal docs exist during validation | PASS | post=True formal=True |
| VAL4561_OVERALL | 4561 checkpoint validation | PASS | CONDITIONAL_EH_IR_SELECTOR_REDERIVED_PARENT_SIGNATURE_FAILS_RESIDUAL_EFT_ENVELOPE_RETAINED |

