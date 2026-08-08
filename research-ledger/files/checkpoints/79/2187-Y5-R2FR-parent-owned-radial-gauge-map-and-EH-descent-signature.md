# 2187 - Y5/R2FR Parent-Owned Radial Gauge Map And EH Descent Signature

## Current Verdict

2187 turns the 2PN gauge fix into a rule, not a vibe.

The local branch now has two allowed readout branches:

1. **Areal reciprocal branch.** The parent readout defines `R_areal=sqrt(Area(S^2)/(4*pi))`, uses angular area coframe `R dOmega`, and the Schwarzschild/EH fixed-point form

`A=exp(v)=1-2GM/(c^2 R)`,

`B=exp(-v)=A^-1`.

2. **Isotropic PPN branch.** The parent readout defines `r_iso` by conformal-flat spatial PPN gauge, uses `A_iso=((1-x/2)/(1+x/2))^2`, and scores beta/gamma in that gauge.

The required map is:

`R=r_iso(1+x/2)^2`,

`y=GM/(c^2 R)=x/(1+x/2)^2`.

This means the old `+1/2*x^2` row is not a physical local-GR failure if the parent owns the areal/isotropic transform. It is a forbidden mixed-gauge residual: isotropic lapse plus reciprocal spatial readout in the same coordinate.

But the parent ownership is still not derived. 2187 gives the contract:

- do not mix gauges;
- label `kappa_v` by gauge;
- use areal reciprocal readout internally if that is the MTS branch;
- transform to isotropic/PPN gauge before beta/gamma scoring;
- derive or residualize the angular coframe and radial coordinate map.

So local-GR is healthier, but still nonclaim.

## Source Register

| source_id | source_path | path_exists | needles_found | role | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| 2186_handoff | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\2186-Y5-R2FR-MTS-EH-fixed-point-descent-and-2PN-readout-residual-gate.md | True | True | 2186 selects parent-owned radial gauge map and EH descent signatures as the next gate. | False |
| 2186_validation | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_2186_VALIDATION.csv | True | True | 2186 validation passed before 2187 continues the chain. | False |
| 2186_gauge_calc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2186_2PN_READOUT_GAUGE_CALCULATION.csv | True | True | 2186 provides the gauge calculation this checkpoint turns into a parent-owned readout contract. | False |
| 2186_readout_owner | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2186_RADIAL_READOUT_OWNER_GATE.csv | True | True | 2186 records that radial and angular coframe ownership are the live readout debts. | False |
| 2177_v_readout | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\2177-Y5-R2FR-v-only-visible-quotient-readout-owner-or-current-readout-lock.md | True | True | 2177 supplies the v-only reciprocal coframe after u=0 and its source/readout caveats. | False |
| descent_gate | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2186_MTS_EH_DESCENT_GATE.csv | True | True | 2186 records descent, PiM, and readout-gauge debts. | False |
| local_gr_blocks | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_MIN_PARENT_LOCAL_GR_ACTION_BLOCKS.csv | True | True | local-GR blocks identify EH core, boundary reference, and readout/PiM double-zero structure. | False |
| fixed_point_conditions | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_MIN_PARENT_LOCAL_GR_FIXED_POINT_CONDITIONS.csv | True | True | fixed-point conditions define the remaining local descent and transition-control requirements. | False |

## Parent Radial Gauge Contract

| contract_id | contract | statement | status | implication | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| RGC2187_0_parent_object | radial coordinate is an observable functional | The parent readout must define either R_areal := sqrt(Area(S^2)/(4*pi)) from the angular coframe, or r_iso by conformal-flat spatial PPN gauge. | PARENT_GAUGE_OBJECT_DEFINED_AS_CONTRACT | radial gauge is no longer allowed to float silently between calculations. | False |
| RGC2187_1_areal_branch | areal reciprocal branch | If R=R_areal, the local EH fixed-point line element may use A=exp(v)=1-2GM/(c^2 R), B=exp(-v)=A^-1, and angular area R^2 dOmega^2. | AREAL_RECIPROCAL_BRANCH_ALLOWED_CONDITIONAL | the reciprocal branch is legitimate in Schwarzschild/areal gauge. | False |
| RGC2187_2_isotropic_branch | isotropic PPN branch | If r=r_iso, then A=A_iso and spatial factor B_iso=(1+x/2)^4; PPN beta/gamma are scored in this gauge. | ISOTROPIC_PPN_BRANCH_ALLOWED_CONDITIONAL | kappa_v=0 and beta=1 belong to the isotropic lapse expansion. | False |
| RGC2187_3_transform | required transform | The parent map must carry R=r_iso(1+x/2)^2 and y=x/(1+x/2)^2 between branches before comparing 2PN coefficients. | AREAL_ISOTROPIC_TRANSFORM_REQUIRED | mixing A_iso with B=1/A_iso in the same coordinate is forbidden. | False |
| RGC2187_4_angular_coframe | angular coframe owner | Areal gauge requires the angular area coframe theta_angular=R dOmega; isotropic gauge requires a conformal spatial factor for both radial and angular legs. | ANGULAR_COFAME_REQUIRED | radial leg alone is insufficient for full local-GR/PPN scoring. | False |
| RGC2187_5_order | constraint before gauge readout | The u=0/v-only reduction must be imposed before the radial gauge functional is scored against clocks, rods, light, orbit endpoints, and source mass. | CONSTRAINT_BEFORE_READOUT_RETAINED | this keeps the 2177 readout-order guard active. | False |
| RGC2187_6_current_status | current parent ownership status | This is a parent-readout contract, not a proof that MTS already supplies the angular/radial gauge functional. | RADIAL_GAUGE_CONTRACT_WRITTEN_NOT_PARENT_SIGNED | local-GR claim remains blocked until the contract is derived from the parent action/readout. | False |

## Areal/Isotropic Branch Rules

| rule_id | rule | statement | status | implication | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| BR2187_0_no_mixing | no mixed-gauge scoring | Do not use isotropic lapse A_iso and reciprocal spatial factor B=1/A_iso in the same coordinate for 2PN scoring. | FORBIDDEN_MIXED_GAUGE | this is exactly the source of the +1/2 warning. | False |
| BR2187_1_areal_scoring | areal internal branch | Areal reciprocal branch may be used for internal Schwarzschild/EH descent checks, with R fixed by sphere area and B=A^-1. | CONDITIONAL_PASS_IF_AREAL_OWNER | valid only if the angular area coframe is parent-owned. | False |
| BR2187_2_ppn_scoring | PPN scoring branch | For PPN beta/gamma reporting, transform to isotropic/PPN gauge and use A_iso plus conformal spatial factor B_iso. | PPN_GAUGE_REQUIRED_FOR_BETA_GAMMA | beta=1 comes from isotropic lapse, not areal kappa_v. | False |
| BR2187_3_kappa_label | kappa_v label discipline | kappa_v must carry a gauge label: kappa_v_isotropic=0, kappa_v_areal=-2 for Schwarzschild expansions. | GAUGE_LABEL_REQUIRED | unlabelled kappa_v claims are not admissible beyond leading order. | False |
| BR2187_4_residual_rule | residual activation | If no parent radial/angle owner is supplied, activate epsilon_radial_gauge_owner and retain the 2PN residual row as nonclaim. | RESIDUAL_ROW_IF_OWNER_MISSING | conditional gauge resolution cannot be treated as local-GR evidence without ownership. | False |

## EH Descent Signature Matrix

| signature_id | signature | statement | status | implication | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| EDS2187_0_EH_core | EH operator core | S_parent local compact branch contains S_EH[e_obs,kappa_eff] with locally constant kappa_eff. | CONDITIONAL_SOURCE_EXISTS_NOT_FULLY_SIGNED | required for coefficient inheritance rather than GR import. | False |
| EDS2187_1_extra_double_zero | extra-sector double zero | For all local non-EH couplings C_i: C_i(Phi0)=0 and partial_A C_i(Phi0)=0 with positive source-free operator. | REQUIRED_NOT_PROVED | main fifth-force/PPN/source-normalization descent debt. | False |
| EDS2187_2_universal_matter | universal observed coframe | All matter species couple to g_obs/e_obs at leading local order and define the same Hilbert source current. | OPEN_SOURCE_FRAME_DEBT | WEP/source measure still needs proof. | False |
| EDS2187_3_PiM_lock | PiM Hamiltonian lock | Pi_M(Phi0)=Pi_EH and partial_A Pi_M(Phi0)=0. | PIM_LOCK_OPEN | mass projector calibration remains a live residual. | False |
| EDS2187_4_boundary_zero | boundary/reference zero | GHY/reference/exact/topological boundary terms carry no extra compact local mass flux. | BOUNDARY_ZERO_OPEN | source-measure equality can still shift by boundary bookkeeping. | False |
| EDS2187_5_readout_gauge | radial/angle readout owner | Parent readout chooses areal reciprocal branch plus PPN transform or isotropic PPN branch plus non-reciprocal spatial factor. | READOUT_GAUGE_CONTRACT_WRITTEN_NOT_DERIVED | 2187 closes the contract shape, not the parent derivation. | False |
| EDS2187_6_transition | local/cosmology transition control | Same action must suppress MTS extra sectors in compact local systems while allowing cosmological/galaxy behaviour through a derived activation scale. | TRANSITION_CONTROL_OPEN | avoid hand switching between GR local branch and MTS large-scale branch. | False |
| EDS2187_7_verdict | descent signature status | The typed EH descent signature matrix is now explicit, but only the gauge contract is sharpened; extra/PiM/boundary/source signatures remain unsigned. | SIGNATURE_MATRIX_WRITTEN_CURRENT_CLAIM_FAILS | next work should attack extra double zeros and PiM lock. | False |

## Residual Rows

| row_id | symbol | definition | value | status | units | observable_link | source_path | score_ready | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| RGR2187_0_radial_owner | epsilon_radial_gauge_owner | parent ownership failure for areal/isotropic radial coordinate and transform | MISSING_PARENT_RADIAL_GAUGE_OWNER | MISSING_RADIAL_GAUGE_OWNER | dimensionless_or_declared | 2PN;PPN;local_GR | MISSING_SOURCE_PATH | False | False |
| RGR2187_1_angular_owner | epsilon_angular_coframe_owner | parent ownership failure for angular area coframe or conformal isotropic spatial factor | MISSING_PARENT_ANGULAR_COFAME_OWNER | MISSING_ANGULAR_COFAME_OWNER | dimensionless_or_declared | 2PN;light_time;orbital | MISSING_SOURCE_PATH | False | False |
| RGR2187_2_mixed | sigma_spatial_2PN_mixed_forbidden | residual if isotropic lapse and reciprocal spatial factor are scored in same coordinate | 1/2 | FORBIDDEN_MIXED_GAUGE_RESIDUAL | dimensionless_2PN_coefficient | 2PN;PPN | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\2187-Y5-R2FR-parent-owned-radial-gauge-map-and-EH-descent-signature.md | False | False |
| RGR2187_3_areal | sigma_spatial_2PN_areal_owned | spatial residual in parent-owned areal reciprocal gauge | 0 | ZERO_IF_AREAL_GAUGE_PARENT_OWNED | dimensionless_2PN_coefficient | 2PN;local_GR | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\2187-Y5-R2FR-parent-owned-radial-gauge-map-and-EH-descent-signature.md | False | False |
| RGR2187_4_kappa_iso | kappa_v_isotropic | PPN-gauge lapse quadratic coefficient | 0 | ZERO_IN_ISOTROPIC_PPN_GAUGE_CONDITIONAL | dimensionless | PPN_beta | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\2187-Y5-R2FR-parent-owned-radial-gauge-map-and-EH-descent-signature.md | False | False |
| RGR2187_5_kappa_areal | kappa_v_areal | areal-gauge lapse quadratic coefficient | -2 | GAUGE_LABEL_REQUIRED_NOT_BETA_FAILURE | dimensionless | coordinate_gauge | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\2187-Y5-R2FR-parent-owned-radial-gauge-map-and-EH-descent-signature.md | False | False |
| RGR2187_6_descent | epsilon_EH_descent_signature | failure to parent-sign EH core plus extra-sector double zeros | MISSING_PARENT_DESCENT_SIGNATURE | MISSING_EH_DESCENT_SIGNATURE | dimensionless_or_declared | local_GR;WEP;PPN | MISSING_SOURCE_PATH | False | False |
| RGR2187_7_PiM | epsilon_PiM_lock | failure to prove Pi_M(Phi0)=Pi_EH and derivative silence | MISSING_PARENT_PIM_LOCK | MISSING_PIM_LOCK_PROOF | dimensionless_or_GM_flux | Newton;R10;R11;PPN | MISSING_SOURCE_PATH | False | False |
| RGR2187_8_boundary | epsilon_boundary_reference_zero | failure to prove zero compact boundary/reference mass flux | MISSING_BOUNDARY_ZERO_PROOF | MISSING_BOUNDARY_ZERO | dimensionless_or_GM_flux | Newton;local_GR | MISSING_SOURCE_PATH | False | False |
| RGR2187_9_total | Delta_local_GR_readout_descent_abs | absolute envelope of radial, angular, descent, PiM and boundary residuals | MISSING_COMPONENT_INPUTS | MISSING_COMPONENT_INPUTS | dimensionless | local_GR;PPN;Newton | MISSING_SOURCE_PATH | False | False |

## Claim Gate

| gate_id | gate | status | implication | valid_for_claim |
| --- | --- | --- | --- | --- |
| CG2187_0_contract | parent radial gauge contract shape is written | PASS_GUARDRAIL | areal/isotropic branches and transform are explicit | False |
| CG2187_1_mixed_gauge | mixed isotropic/reciprocal 2PN scoring is forbidden | PASS_GUARDRAIL | the +1/2 row is now a guardrail residual, not a physical claim | False |
| CG2187_2_radial_owner | parent owns radial/angle gauge map | BLOCKED_NONCLAIM | contract written but not derived from parent action/readout | False |
| CG2187_3_EH_descent | EH descent signatures are parent-signed | BLOCKED_NONCLAIM | extra double-zero, PiM, source and boundary signatures remain open | False |
| CG2187_4_local_GR | full local-GR reduction can be claimed | BLOCKED_NONCLAIM | requires gauge owner plus EH descent signatures | False |
| CG2187_5_GitHub | public/github update is triggered | BLOCKED_NONCLAIM | private work only; no GitHub action | False |

## Decision Ledger

| decision_id | decision | rationale | selection_status | valid_for_claim |
| --- | --- | --- | --- | --- |
| DEC2187_0_gain | RADIAL_GAUGE_CONTRACT_WRITTEN | Areal reciprocal and isotropic PPN branches are now separated with a required transform and gauge labels. | selected | False |
| DEC2187_1_gain_guard | MIXED_GAUGE_SCORING_FORBIDDEN | The previous +1/2 2PN warning becomes a guardrail against using two gauges at once. | selected | False |
| DEC2187_2_limit | PARENT_OWNERSHIP_AND_EH_DESCENT_STILL_UNSIGNED | Radial/angle map, extra double zeros, PiM lock, universal source and boundary zero are not parent-signed. | selected | False |
| DEC2187_3_next | EXTRA_DOUBLE_ZERO_AND_PIM_LOCK_SIGNATURE_NEXT | The next best route is to attack the two hardest remaining descent signatures: extra-sector double zeros and Hamiltonian PiM lock. | selected | False |

## Next Target

| route_id | selection_status | target_file | target_script | objective | success_condition | do_not_do | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NEXT2187_0_2188 | selected | 2188-Y5-R2FR-extra-sector-double-zero-and-PiM-lock-signature-or-residual-fill.md | scripts/Y5_R2FR_extra_sector_double_zero_and_PiM_lock_signature_or_residual_fill_2188.py | derive or audit the extra-sector double-zero conditions and Hamiltonian PiM lock needed for MTS to own the EH fixed-point local branch | for each local extra coupling C_i, C_i(Phi0)=0 and partial_A C_i(Phi0)=0 or a finite residual exists; Pi_M(Phi0)=Pi_EH and derivative silence are parent-signed or residualized | do not claim local GR from radial gauge contract alone, do not absorb PiM residual into G, do not use GitHub action | False |
| NEXT2187_1_empirical_parallel | held_parallel | 2188b-Y5-R2FR-readout-gauge-2PN-bound-source-acquisition.md | scripts/Y5_R2FR_readout_gauge_2PN_bound_source_acquisition_2188b.py | if derivation stalls, acquire source-backed PPN/2PN bounds for retained radial/angle readout residuals | at least one residual row has source path, units, normalization, arena projection and valid_for_claim=false | do not score placeholders or unsourced 2PN bounds | False |

## Branch Copies

| copy_id | source_path | target_path | copied | valid_for_claim |
| --- | --- | --- | --- | --- |
| queue | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2187_RESIDUAL_ROWS.csv | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\rab-sector\acquisition-queue\JR2187_RADIAL_GAUGE_EH_DESCENT_RESIDUAL_ROWS_NONCLAIM.csv | True | False |
| branch_wep | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2187_PARENT_RADIAL_GAUGE_CONTRACT.csv | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope\branch_locked_wep\residuals\P8_Y5_PARENT_QLOC_2187_RADIAL_GAUGE_CONTRACT_NONCLAIM.csv | True | False |
| source_weight | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2187_EH_DESCENT_SIGNATURE_MATRIX.csv | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\beta-source\docs\PARENT_RADIAL_GAUGE_EH_DESCENT_2187_NONCLAIM.csv | True | False |

## Validation

| validation_id | status | detail | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- |
| VAL2187_00_sources_exist | PASS | 8/8 sources exist | False | False |
| VAL2187_01_needles_found | PASS | 8/8 source needle sets found | False | False |
| VAL2187_02_gauge_contract | PASS | areal/isotropic branch contract and transform are explicit | False | False |
| VAL2187_03_branch_rules | PASS | mixed-gauge scoring forbidden and kappa labels required | False | False |
| VAL2187_04_descent_signature | PASS | EH descent signature matrix is explicit and nonclaim | False | False |
| VAL2187_05_residual_rows | PASS | mixed warning, owned-areal zero, and missing descent rows represented; rows=10 | False | False |
| VAL2187_06_claim_gate | PASS | claim gate keeps local-GR and GitHub blocked | False | False |
| VAL2187_07_decision | PASS | decision selects extra double-zero and PiM lock next | False | False |
| VAL2187_08_next_target | PASS | 2188 double-zero/PiM target selected | False | False |
| VAL2187_09_claim_flags_false | PASS | all generated rows keep valid_for_claim=false and claim_allowed=false | False | False |
| VAL2187_10_csv_parse | PASS | P8_Y5_PARENT_QLOC_2187_SOURCE_REGISTER.csv:8; P8_Y5_PARENT_QLOC_2187_PARENT_RADIAL_GAUGE_CONTRACT.csv:7; P8_Y5_PARENT_QLOC_2187_AREAL_ISOTROPIC_BRANCH_RULES.csv:5; P8_Y5_PARENT_QLOC_2187_EH_DESCENT_SIGNATURE_MATRIX.csv:8; P8_Y5_PARENT_QLOC_2187_RESIDUAL_ROWS.csv:10; P8_Y5_PARENT_QLOC_2187_CLAIM_GATE.csv:6; P8_Y5_PARENT_QLOC_2187_DECISION_LEDGER.csv:4; P8_Y5_PARENT_QLOC_2187_NEXT_TARGET.csv:2; P8_Y5_PARENT_QLOC_2187_BRANCH_COPIES.csv:3 | False | False |
| VAL2187_11_branch_copies | PASS | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\rab-sector\acquisition-queue\JR2187_RADIAL_GAUGE_EH_DESCENT_RESIDUAL_ROWS_NONCLAIM.csv;D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope\branch_locked_wep\residuals\P8_Y5_PARENT_QLOC_2187_RADIAL_GAUGE_CONTRACT_NONCLAIM.csv;D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\beta-source\docs\PARENT_RADIAL_GAUGE_EH_DESCENT_2187_NONCLAIM.csv | False | False |
| VAL2187_12_formalization_clean | PASS | formalization-workbench has no 2187 artifacts | False | False |
| VAL2187_13_pycache_absent | PASS | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\scripts\__pycache__ | False | False |
| VAL2187_OVERALL | PASS | 2187 writes parent radial gauge/readout contract and keeps EH descent/local-GR nonclaim | False | False |

## Working Interpretation

This is exactly the kind of discipline the framework needed. The reciprocal branch survives, but only as a parent-owned areal readout or with a declared transform to PPN gauge.

That means the next bottleneck is not the 2PN gauge scare. It is the true descent theorem:

`MTS parent action -> EH fixed point -> extra-sector double zeros -> PiM lock -> source/boundary silence -> parent-owned readout gauge`.

The most valuable next attack is therefore the double-zero/PiM lock signature.
