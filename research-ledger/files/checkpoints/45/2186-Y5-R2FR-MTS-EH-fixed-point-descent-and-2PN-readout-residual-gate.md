# 2186 - Y5/R2FR MTS EH Fixed-Point Descent And 2PN Readout Residual Gate

## Current Verdict

2186 improves the situation again: the `+1/2*x^2` 2PN warning from 2185 is **not automatically a physical failure**.

It is a mixed-gauge warning.

In isotropic radius `x=GM/(c^2 r_iso)`:

`A_iso=((1-x/2)/(1+x/2))^2`,

`B_iso=(1+x/2)^4`,

and if we force the reciprocal branch in that same isotropic coordinate,

`B_recip=1/A_iso`,

then:

`B_recip-B_iso=+1/2*x^2+O(x^3)`.

But Schwarzschild's areal radius is

`R=r_iso(1+x/2)^2`,

with

`y=GM/(c^2 R)=x/(1+x/2)^2`.

In that areal gauge:

`A=1-2y`,

`B=(1-2y)^-1`,

and the transformed isotropic radial coefficient is exactly the same `B`. So the reciprocal branch `B=exp(-v)=1/A` is not killed; it is the natural Schwarzschild areal-gauge readout.

The catch is equally important:

`kappa_v=0` is the isotropic/PPN-gauge lapse statement, while in areal gauge

`v=log(1-2y)=-2y-2y^2+O(y^3)`.

So `kappa_v` is gauge/readout dependent unless the radial coordinate is parent-owned.

That means the next real blocker is not "2PN mismatch = death". It is:

**does MTS parent-own the radial/angle readout map and EH fixed-point descent?**

Current answer: not yet.

## Source Register

| source_id | source_path | path_exists | needles_found | role | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| 2185_handoff | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\2185-Y5-R2FR-EH-fixed-point-to-v-action-coefficient-extraction-or-GR-import-demotion.md | True | True | 2185 selects MTS EH fixed-point descent and 2PN readout residual resolution as next gate. | False |
| 2185_validation | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_BRR545_2185_VALIDATION.csv | True | True | 2185 validation passed before 2186 continues the chain. | False |
| 2177_readout_shape | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\2177-Y5-R2FR-v-only-visible-quotient-readout-owner-or-current-readout-lock.md | True | True | 2177 supplies the reciprocal radial coframe/readout branch and its order guard. | False |
| 2185_residuals | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2185_RESIDUAL_ROWS.csv | True | True | 2185 records the mixed isotropic/reciprocal 2PN warning. | False |
| local_gr_blocks | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_MIN_PARENT_LOCAL_GR_ACTION_BLOCKS.csv | True | True | local-GR blocks define EH core, boundary reference, and readout/PiM double-zero requirements. | False |
| fixed_point_conditions | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_MIN_PARENT_LOCAL_GR_FIXED_POINT_CONDITIONS.csv | True | True | fixed-point conditions define extra-sector double zero, PiM lock, and local/cosmology transition guard. | False |
| derived_chain | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_MIN_PARENT_LOCAL_GR_DERIVED_CHAIN.csv | True | True | derived chain records conditional EH metric equation, Hamiltonian charge, and readout steps. | False |
| hamiltonian_source | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_HAMILTONIAN_SOURCE_MEASURE_CONTRACT.csv | True | True | Hamiltonian source contract carries PiM adoption, observed source worldtube, and extra-source silence debts. | False |

## 2PN Readout Gauge Calculation

| calc_id | calculation | equation | status | implication | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| RGC2186_0_mixed_warning | mixed isotropic/reciprocal comparison | In isotropic radius x=GM/(c^2 r_iso), A_iso=((1-x/2)/(1+x/2))^2 and B_iso=(1+x/2)^4, while imposing B_recip=1/A_iso gives B_recip-B_iso=+1/2*x^2+O(x^3). | MIXED_GAUGE_2PN_WARNING_REPRODUCED | the 2185 warning is real as a same-coordinate isotropic comparison. | False |
| RGC2186_1_areal_map | isotropic to areal radius map | R=r_iso(1+x/2)^2, y=GM/(c^2 R)=x/(1+x/2)^2, so x=y+y^2+5*y^3/4+O(y^4). | EXACT_RADIUS_MAP_SERIES | the same Schwarzschild geometry uses different weak-field expansion variables in isotropic and areal gauges. | False |
| RGC2186_2_A_areal | lapse in areal radius | A_iso expressed in y is exactly A_areal=1-2y. | AREAL_LAPSE_MATCH_EXACT | the reciprocal branch belongs naturally to areal Schwarzschild gauge. | False |
| RGC2186_3_B_areal | reciprocal spatial radial coefficient | B_areal=(1-2y)^-1=1+2y+4y^2+8y^3+O(y^4), and transformed isotropic g_RR equals B_areal. | AREAL_GAUGE_RESOLVES_2PN_SPATIAL_RESIDUAL | the +1/2 isotropic residual vanishes after the proper radial gauge transformation. | False |
| RGC2186_4_kappa_gauge | kappa_v is radial-gauge dependent | In isotropic x, v=log(A_iso)=-2x+0*x^2+O(x^3), but in areal y, v=log(1-2y)=-2y-2y^2+O(y^3). | KAPPA_V_GAUGE_DEPENDENT | kappa_v=0 is the isotropic/PPN-gauge statement; reciprocal readout is the areal-gauge statement. | False |
| RGC2186_5_resolution | 2PN status | The 2PN issue is demoted from physical failure to radial-gauge/readout-owner debt if MTS parent-owns the areal-isotropic map and the angular coframe. | GAUGE_RESOLUTION_CONDITIONAL_NOT_PARENT_SIGNED | without a parent radial gauge owner, keep finite readout residual rows. | False |

## MTS EH Descent Gate

| gate_id | gate | statement | status | implication | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| DEG2186_0_EH_core | EH core descent | S_parent local compact branch must reduce to S_EH[e_obs,kappa_eff] plus locally silent sectors. | CONDITIONAL_FROM_A511_0_NOT_CURRENTLY_SIGNED | coefficient extraction remains GR import unless this is parent-derived. | False |
| DEG2186_1_kappa | constant kappa/G | d kappa_eff=0 on connected compact local domains from topological/superselection sector. | CONDITIONAL_FROM_A511_1 | local G drift is not the active blocker if the kappa sector is adopted, but still needs parent signoff. | False |
| DEG2186_2_extra_double_zero | extra-sector double zeros | For each non-EH MTS coupling C_i, require C_i(Phi0)=0 and partial_A C_i(Phi0)=0 with positive source-free operator. | REQUIRED_NOT_PROVED | this is the main no-fifth-force/local-GR descent debt. | False |
| DEG2186_3_universal_coframe | universal observed coframe | All matter species, clocks, and orbital readout use the same g_obs/e_obs at leading local order. | OPEN_SOURCE_FRAME_DEBT | WEP/source-measure closure remains live. | False |
| DEG2186_4_PiM_lock | Hamiltonian PiM lock | Pi_M(Phi0)=Pi_EH and partial_A Pi_M(Phi0)=0 at the fixed point. | PIM_LOCK_OPEN | mass projector calibration freedom remains live. | False |
| DEG2186_5_boundary | boundary/reference zero | GHY/reference/exact/topological boundary terms must produce no extra compact local mass flux. | BOUNDARY_ZERO_OPEN | source-measure equality can still shift by boundary bookkeeping. | False |
| DEG2186_6_readout | metric/readout descent | g_readout=g_obs+O((Phi-Phi0)^2), plus parent-owned radial gauge map chooses areal or isotropic coordinates before PPN scoring. | READOUT_GAUGE_OWNER_OPEN | 1PN survives conditionally; full readout requires coordinate/gauge ownership. | False |
| DEG2186_7_verdict | MTS EH descent status | 2186 resolves the 2PN warning as a gauge debt, but does not prove the MTS EH fixed-point descent. | DESCENT_GATE_CURRENT_CLAIM_FAILS | local-GR claim remains blocked; route is now sharper. | False |

## Radial Readout Owner Gate

| owner_id | owner_gate | statement | status | implication | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| ROG2186_0_radial_leg | radial coframe leg | 2177 gives theta_1=exp(-v/2)dr after u=0, but it does not by itself identify dr as areal, isotropic, or another parent-owned radial coordinate. | RADIAL_COORDINATE_OWNER_MISSING | this is why the 2PN comparison can be mixed-gauge. | False |
| ROG2186_1_angular_leg | angular coframe/area radius | Areal Schwarzschild gauge requires angular area element R^2 dOmega^2 while reciprocal radial leg has B=(1-2GM/(c^2R))^-1. | ANGULAR_COFAME_OWNER_MISSING | MTS must state whether r is area radius or supply the isotropic-to-areal map. | False |
| ROG2186_2_PPN_gauge | PPN isotropic gauge | PPN beta/gamma are normally read in isotropic-like coordinates; kappa_v=0 belongs to that lapse gauge. | PPN_GAUGE_CONTRACT_REQUIRED | beta=1 cannot be inferred from an areal-coordinate x^2 coefficient without transforming gauge. | False |
| ROG2186_3_reciprocal_gauge | reciprocal branch gauge | B=exp(-v)=1/A is exact Schwarzschild radial gauge when r is areal and A=1-2GM/(c^2r). | RECIPROCAL_BRANCH_AREAL_GAUGE_CONDITIONAL_PASS | the reciprocal branch is not killed by the isotropic 2PN warning. | False |
| ROG2186_4_parent_choice | parent readout choice | The parent action/readout must choose either: areal reciprocal gauge plus PPN transform, or isotropic gauge with non-reciprocal spatial factor. | READOUT_BRANCH_FORK_EXPLICIT | choosing both in the same coordinate causes the +1/2 residual. | False |

## Residual Rows

| row_id | symbol | definition | value | status | units | observable_link | source_path | score_ready | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| RES2186_0_sigma_mixed | sigma_spatial_2PN_mixed_isotropic | same-coordinate residual B_recip(A_iso)-B_iso in isotropic radius | 1/2 | FINITE_MIXED_GAUGE_WARNING | dimensionless_2PN_coefficient | 2PN;light_time;perihelion | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\2186-Y5-R2FR-MTS-EH-fixed-point-descent-and-2PN-readout-residual-gate.md | False | False |
| RES2186_1_sigma_areal | sigma_spatial_2PN_areal_gauge | residual after transforming isotropic Schwarzschild to areal radius | 0 | ZERO_IN_AREAL_GAUGE_CONDITIONAL | dimensionless_2PN_coefficient | 2PN;local_GR | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\2186-Y5-R2FR-MTS-EH-fixed-point-descent-and-2PN-readout-residual-gate.md | False | False |
| RES2186_2_kappa_iso | kappa_v_isotropic | x^2 coefficient in v=log(A_iso) with x=GM/(c^2 r_iso) | 0 | ZERO_IN_ISOTROPIC_PPN_GAUGE_CONDITIONAL | dimensionless | PPN_beta | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\2186-Y5-R2FR-MTS-EH-fixed-point-descent-and-2PN-readout-residual-gate.md | False | False |
| RES2186_3_kappa_areal | kappa_v_areal | y^2 coefficient in v=log(1-2y) with y=GM/(c^2 R_areal) | -2 | GAUGE_DEPENDENT_NOT_BETA_FAILURE | dimensionless | PPN_beta;coordinate_gauge | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\2186-Y5-R2FR-MTS-EH-fixed-point-descent-and-2PN-readout-residual-gate.md | False | False |
| RES2186_4_radius_owner | epsilon_radial_gauge_owner | failure to parent-own areal/isotropic radial coordinate and angular coframe | MISSING_PARENT_RADIAL_GAUGE_MAP | MISSING_RADIAL_GAUGE_OWNER | dimensionless_or_declared | 2PN;PPN;local_GR | MISSING_SOURCE_PATH | False | False |
| RES2186_5_EH_descent | epsilon_EH_fixed_point_descent | failure to parent-derive EH fixed point and extra-sector double zeros | MISSING_PARENT_DESCENT_PROOF | MISSING_MTS_EH_DESCENT | dimensionless_or_declared | local_GR;WEP;PPN | MISSING_SOURCE_PATH | False | False |
| RES2186_6_PiM | epsilon_PiM_lock | failure of Pi_M(Phi0)=Pi_EH and partial_A Pi_M(Phi0)=0 | MISSING_PARENT_PIM_LOCK | MISSING_PIM_LOCK_PROOF | dimensionless_or_GM_flux | Newton;R10;R11;PPN | MISSING_SOURCE_PATH | False | False |
| RES2186_7_boundary | epsilon_boundary_flux | unresolved GHY/reference/exact/topological compact local boundary flux | MISSING_BOUNDARY_ZERO_PROOF | MISSING_BOUNDARY_ZERO | dimensionless_or_GM_flux | Newton;local_GR;R11 | MISSING_SOURCE_PATH | False | False |
| RES2186_8_extra | epsilon_extra_mass_charge | non-EH MTS extra-sector mass charge at compact local fixed point | MISSING_EXTRA_DOUBLE_ZERO_OR_BOUND | MISSING_EXTRA_SECTOR_ZERO | dimensionless_or_GM_flux | WEP;PPN;local_GR | MISSING_SOURCE_PATH | False | False |
| RES2186_9_total | Delta_local_GR_descent_abs | absolute envelope of descent, PiM, boundary, extra-sector, and radial-gauge residuals | MISSING_COMPONENT_INPUTS | MISSING_COMPONENT_INPUTS | dimensionless | local_GR;PPN;Newton | MISSING_SOURCE_PATH | False | False |

## Claim Gate

| gate_id | gate | status | implication | valid_for_claim |
| --- | --- | --- | --- | --- |
| CG2186_0_2PN_gauge | 2PN reciprocal/isotropic warning is gauge-resolved conditionally | CONDITIONAL_PASS | areal gauge map removes the +1/2 residual if parent-owned | False |
| CG2186_1_radial_owner | parent owns radial/areal/isotropic readout map | BLOCKED_NONCLAIM | 2177 supplies radial coframe but not full radial/angular gauge ownership | False |
| CG2186_2_EH_descent | MTS parent derives EH fixed point and extra double zeros | BLOCKED_NONCLAIM | fixed-point descent remains not parent-signed | False |
| CG2186_3_PiM_source | PiM lock and same Hilbert/Hamiltonian source measure are proved | BLOCKED_NONCLAIM | Hamiltonian PiM adoption and source glue remain open | False |
| CG2186_4_boundary | compact boundary/reference flux is zero | BLOCKED_NONCLAIM | boundary flux remains open | False |
| CG2186_5_local_GR | full local-GR reduction can be claimed | BLOCKED_NONCLAIM | needs descent, PiM/source, boundary, and radial gauge ownership | False |
| CG2186_6_guardrail | no mixed-gauge or GR-import promotion | PASS_GUARDRAIL | 2186 labels the win as conditional and keeps all claims false | False |

## Decision Ledger

| decision_id | decision | rationale | selection_status | valid_for_claim |
| --- | --- | --- | --- | --- |
| DEC2186_0_gain | TWO_PN_WARNING_IS_GAUGE_CONDITIONAL | The +1/2 isotropic residual is a mixed-gauge comparison; in areal Schwarzschild gauge reciprocal B=exp(-v) is exact. | selected | False |
| DEC2186_1_caution | RADIAL_READOUT_OWNER_NOW_CRITICAL | MTS must parent-own whether r is areal, isotropic, or mapped before PPN scoring; otherwise the same branch can be misread. | selected | False |
| DEC2186_2_limit | MTS_EH_DESCENT_STILL_UNSIGNED | The coefficient and 2PN gauge pieces look promising, but EH fixed-point descent/PiM/source/boundary clauses remain open. | selected | False |
| DEC2186_3_next | PARENT_RADIAL_GAUGE_AND_EH_DESCENT_SIGNATURE_NEXT | Next target should construct the parent readout gauge map and tie it to EH descent/PiM/source signatures. | selected | False |

## Next Target

| route_id | selection_status | target_file | target_script | objective | success_condition | do_not_do | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NEXT2186_0_2187 | selected | 2187-Y5-R2FR-parent-owned-radial-gauge-map-and-EH-descent-signature.md | scripts/Y5_R2FR_parent_owned_radial_gauge_map_and_EH_descent_signature_2187.py | derive or specify the parent-owned radial gauge/readout map linking reciprocal areal branch, isotropic PPN gauge, angular coframe, PiM lock, and EH fixed-point descent signatures | parent action/readout owns r_areal or r_iso plus transform, angular area coframe, PiM(Phi0)=Pi_EH, same source measure, zero boundary flux, and extra-sector double zeros; otherwise residual rows remain nonclaim | do not mix isotropic lapse with reciprocal spatial readout in the same coordinate, do not claim local GR from gauge equivalence alone, do not use GitHub action | False |
| NEXT2186_1_empirical_parallel | held_parallel | 2187b-Y5-R2FR-radial-gauge-2PN-bound-acquisition.md | scripts/Y5_R2FR_radial_gauge_2PN_bound_acquisition_2187b.py | if derivation stalls, acquire source-backed 2PN/readout/orbital bounds for any retained radial-gauge residual | at least one 2PN/readout residual has source path, units, normalization, arena projection, and valid_for_claim=false | do not score placeholders or unsourced PPN bounds | False |

## Branch Copies

| copy_id | source_path | target_path | copied | valid_for_claim |
| --- | --- | --- | --- | --- |
| queue | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2186_RESIDUAL_ROWS.csv | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\rab-sector\acquisition-queue\JR2186_MTS_EH_DESCENT_2PN_RESIDUAL_ROWS_NONCLAIM.csv | True | False |
| branch_wep | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2186_2PN_READOUT_GAUGE_CALCULATION.csv | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope\branch_locked_wep\residuals\P8_Y5_PARENT_QLOC_2186_2PN_GAUGE_AUDIT_NONCLAIM.csv | True | False |
| source_weight | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_2186_MTS_EH_DESCENT_GATE.csv | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\beta-source\docs\MTS_EH_DESCENT_2PN_READOUT_GATE_2186_NONCLAIM.csv | True | False |

## Validation

| validation_id | status | detail | valid_for_claim | claim_allowed |
| --- | --- | --- | --- | --- |
| VAL2186_00_sources_exist | PASS | 8/8 sources exist | False | False |
| VAL2186_01_needles_found | PASS | 8/8 source needle sets found | False | False |
| VAL2186_02_gauge_calculation | PASS | 2PN warning reproduced, areal gauge resolution and kappa gauge dependence recorded | False | False |
| VAL2186_03_descent_gate | PASS | MTS EH descent debts remain explicit and nonclaim | False | False |
| VAL2186_04_readout_owner | PASS | radial/angular readout ownership gate written | False | False |
| VAL2186_05_residual_rows | PASS | mixed warning, areal zero and missing descent rows represented; rows=10 | False | False |
| VAL2186_06_claim_gate | PASS | claim gate separates conditional gauge pass from blocked local-GR claim | False | False |
| VAL2186_07_decision | PASS | decision selects parent radial gauge and EH descent signature next | False | False |
| VAL2186_08_next_target | PASS | 2187 radial gauge/EH descent target selected | False | False |
| VAL2186_09_claim_flags_false | PASS | all generated rows keep valid_for_claim=false and claim_allowed=false | False | False |
| VAL2186_10_csv_parse | PASS | P8_Y5_PARENT_QLOC_2186_SOURCE_REGISTER.csv:8; P8_Y5_PARENT_QLOC_2186_2PN_READOUT_GAUGE_CALCULATION.csv:6; P8_Y5_PARENT_QLOC_2186_MTS_EH_DESCENT_GATE.csv:8; P8_Y5_PARENT_QLOC_2186_RADIAL_READOUT_OWNER_GATE.csv:5; P8_Y5_PARENT_QLOC_2186_RESIDUAL_ROWS.csv:10; P8_Y5_PARENT_QLOC_2186_CLAIM_GATE.csv:7; P8_Y5_PARENT_QLOC_2186_DECISION_LEDGER.csv:4; P8_Y5_PARENT_QLOC_2186_NEXT_TARGET.csv:2; P8_Y5_PARENT_QLOC_2186_BRANCH_COPIES.csv:3 | False | False |
| VAL2186_11_branch_copies | PASS | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\rab-sector\acquisition-queue\JR2186_MTS_EH_DESCENT_2PN_RESIDUAL_ROWS_NONCLAIM.csv;D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\microscope\branch_locked_wep\residuals\P8_Y5_PARENT_QLOC_2186_2PN_GAUGE_AUDIT_NONCLAIM.csv;D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\beta-source\docs\MTS_EH_DESCENT_2PN_READOUT_GATE_2186_NONCLAIM.csv | False | False |
| VAL2186_12_formalization_clean | PASS | formalization-workbench has no 2186 artifacts | False | False |
| VAL2186_13_pycache_absent | PASS | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\scripts\__pycache__ | False | False |
| VAL2186_OVERALL | PASS | 2186 demotes 2PN warning to parent radial-gauge debt while keeping MTS EH descent/local-GR nonclaim | False | False |

## Working Interpretation

This is a good result. The local branch is not dead at 2PN just because the isotropic comparison gave `+1/2`.

The sharper statement is:

`reciprocal v-readout + areal radius = Schwarzschild radial gauge`,

while

`kappa_v=0 + beta=1 = isotropic/PPN lapse gauge`.

Those are connected by a coordinate/readout map. MTS now needs to own that map instead of letting us switch gauges by hand.

So the project position is:

1. EH fixed point gives the right `K_v`, `C_v`, beta and gamma conditionally.
2. The 2PN reciprocal warning is gauge-resolvable conditionally.
3. Full local-GR still requires parent-owned EH descent, radial/angle readout ownership, PiM lock, source measure glue, and zero boundary flux.
