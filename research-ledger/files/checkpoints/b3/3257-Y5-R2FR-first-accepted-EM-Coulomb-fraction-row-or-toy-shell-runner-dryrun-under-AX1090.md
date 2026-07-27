# 3257 - First accepted EM Coulomb fraction row or toy-shell runner dryrun under AX1090

Private derivation/checkpoint. This does not claim local GR, Newton, Maxwell, WEP, R10, PPN, clock, orbital, material-response, or public source-coupling success.

## Verdict
- `3257` does **not** accept a real `EM_Coulomb` material fraction row.
- It does make a concrete leap: the 1909 alloy Coulomb shape is now connected to `f_EM,A = k_C q_C,A`, and that fraction contract is executable in the 3256 `G_J[EM,EM]` material shell formula.
- The toy SEMF-scale coefficient branch runs and produces finite positive `G_J` rows, but every such row is quarantined as nonclaim.
- The next real fork is sharp: source `k_C=a_C/(m_u c^2)` plus uncertainty/convention, or derive the parent-owned alpha/EM response map so the coefficient is not external smoke.

## Source Register
| source_id | exists | parse_ok | role | evidence_hits | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| SRC3257_3256_handoff | true | true | 3256 material EM binding projection handoff | L9:- Key bridge: match the shell energy to internal EM binding, `U_EM_shell = E_EM,A = f_EM,A M_A c^2`. \| L11:- The material surrogate self-entry is now `G_J[EM,EM]_A = C_frame^2/(20*pi)*(f_EM,A M_A c^2)^2*K_shell(R_in,R_out)`. \| L13:- This is still nonclaim: accepted `f_EM,A`, material mass, profile/cutoffs, tau/source kernel, and no-double-count basis are missing. \| L19:\| MEP3256_0_material_energy_split \| material EM binding energy \| E_EM,A := f_EM,A M_A c^2 \| use the existing component-fraction basis: EM/Coulomb is an internal material energy fraction, not an external net charge \| f_EM,A;M_A;c;basis convention;source path \|  | false |
| SRC3257_3256_projection | true | true | material EM binding projection formulas | L2:MEP3256_0_material_energy_split,material EM binding energy,"E_EM,A := f_EM,A M_A c^2","use the existing component-fraction basis: EM/Coulomb is an internal material energy fraction, not an external net charge","f_EM,A;M_A;c;basis convention;source path",PROJEC \| L3:MEP3256_1_alpha_response,material EM response,"gamma_EM,A := partial ln M_A / partial ln alpha_EM = (alpha_EM/M_A c^2) partial_alpha E_EM,A","if E_EM,A scales linearly with alpha in the chosen convention, gamma_EM,A approx f_EM,A; otherwise retain gamma_EM,A a \| L5:MEP3256_3_no_external_neutrality_shortcut,neutral material handling,"Q_net,A=0 does not imply E_EM,A=0 or f_EM,A=0",internal Coulomb/binding stress remains a material response even if the external field is screened,material binding projection rather than exter | false |
| SRC3257_3256_match | true | true | Coulomb shell energy match and material Gram formula | L4:CSM3256_2_fraction_form,"G_J[EM,EM]_A in component fraction variables","G_J[EM,EM]_A = C_frame^2/(20*pi) * (f_EM,A M_A c^2)^2 * K_shell(R_in,R_out)",K_shell := (R_in^-5-R_out^-5)/(R_in^-1-R_out^-1)^2,"use E_EM,A=f_EM,A M_A c^2",false | false |
| SRC3257_1233_schema | true | true | component-fraction acceptance schema | L5:fraction_value,True,finite numeric >=0 unless signed residual explicitly justified,dimensionless energy/mass fraction,True,False,False \| L6:fraction_uncertainty,True,finite numeric >=0 or sourced upper-bound convention,dimensionless,True,False,False \| L7:basis_convention,True,names parent/MTS basis or external phenomenological basis,MTS_parent_basis;external_DD;external_mass_budget;other_with_source,True,False,False | false |
| SRC3257_1328_routes | true | true | EM_Coulomb source acquisition routes | L8:ROUTE1328_TA6V_EM_Coulomb,TA6V,EM_Coulomb,PSRC1328_5_Damour_Donoghue_dilaton_charges;PSRC1328_6_Damour_Donoghue_DOI,external DD Coulomb/electromagnetic binding charge or SEMF Coulomb term after isotope/alloy averaging,MTS EM owner and alpha/Coulomb map remain  \| L9:ROUTE1328_PtRh10_EM_Coulomb,PtRh10,EM_Coulomb,PSRC1328_5_Damour_Donoghue_dilaton_charges;PSRC1328_6_Damour_Donoghue_DOI,external DD Coulomb/electromagnetic binding charge or SEMF Coulomb term after isotope/alloy averaging,MTS EM owner and alpha/Coulomb map rem | false |
| SRC3257_1909_composition | true | true | TA6V/PtRh10 alloy composition context | L2:AC1909_PtRh10_Pt,PtRh10,Pt,0.900000000000,195.1,78,WEB983_0_MICROSCOPE_CQG_COMPOSITION,D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P \| L4:AC1909_TA6V_Ti,TA6V,Ti,0.900000000000,47.9,22,WEB983_0_MICROSCOPE_CQG_COMPOSITION,D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_ | false |
| SRC3257_1909_proxy | true | true | dimensionless Coulomb shape proxy already computed for alloys | L1:proxy_id,material_id,left_minus_right,mass_fraction_sum,Z_over_A_proxy,N_over_A_proxy,neutron_excess_proxy,electron_rest_mass_fraction,coulomb_formula_proxy,A_bar_proxy,basis_convention,source_anchor,usable_level,missing_for_claim,source_backed_composition_con \| L4:AP1909_TA6V_minus_PtRh10,TA6V_minus_PtRh10,TA6V_minus_PtRh10,not_applicable,5.677745651272e-02,-5.677745651272e-02,-1.135549130254e-01,3.129116287420e-05,-2.574514671000e+00,-1.391140000000e+02,same sign as MCON1061_0_test_pair and 1481 context pack,P8_Y5_R10_ | false |
| SRC3257_1910_tensor_contract | true | true | exact EM mass-defect tensor contract | L5:MDT1910_3_EM_Coulomb_binding,EM_Coulomb,DeltaR_AB^alpha = partial_alpha ln M_A - partial_alpha ln M_B with EM binding owned by the parent EM generator,WCM1053_4 DD alpha/Coulomb smoke; AP1909 coulomb_formula_proxy=-2.574514671000e+00,parent EM edge owner plus  | false |
| SRC3257_3129_dd_comparator | true | true | external DD alpha/Coulomb comparator, not an MTS fraction source | L3:ESC3129_1,Earth_bulk_Coulomb_alpha_smoke,"DeltaC_Earth_bulk_alpha_smoke=2*Q_alpha_Coulomb_Earth with tau_EM=1,zeta_Q=0,C_relax=0,C_cal=0",0.003382521373501744,7.035851579866459e-13,2.379891834968431e-15,0.003979617773650001,0.0005970964001482571,2.8e-15,4.2010 | false |

## EM Coulomb Fraction Formula Contract
| formula_id | object | formula | derivation | inputs | status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| FEM3257_0_Coulomb_shape | dimensionless alloy Coulomb shape | q_C,B = sum_E x_B,E Z_E(Z_E-1)/A_E^(4/3) | SEMF Coulomb energy E_C~a_C Z(Z-1) A^(-1/3); divide by A m_u c^2 to obtain a fractional shape times k_C=a_C/(m_u c^2) | mass fractions x_B,E; element Z; A_context; no isotope-level refinement yet | SHAPE_FORMULA_READY_FROM_1909_PROXY | false |
| FEM3257_1_fraction_from_shape | material EM/Coulomb fraction | f_EM,B = k_C q_C,B, k_C := a_C/(m_u c^2) | converts the dimensionless Coulomb shape into an approximate EM binding fraction only after a sourced Coulomb coefficient and mass convention are selected | source-backed a_C; m_u c^2; isotope/alloy convention; uncertainty | COEFFICIENT_AND_UNCERTAINTY_MISSING_FOR_CLAIM | false |
| FEM3257_2_pair_difference | TA6V_minus_PtRh10 EM difference | Delta f_EM = k_C (q_C,TA6V - q_C,PtRh10) | uses the 1910 response law for the EM selected component once gamma_EM is tied to alpha scaling | both material rows; source-backed k_C; parent EM/alpha map | DIFFERENTIAL_SHAPE_READY_PARENT_ALPHA_MAP_UNSIGNED | false |
| FEM3257_3_alpha_response_guard | alpha/material response | gamma_EM,B = partial ln M_B / partial ln alpha, gamma_EM,B≈f_EM,B only if the retained Coulomb term is alpha-linear in the declared basis | prevents a coefficient smoke row from being treated as the full material response tensor | alpha scaling convention; no-double-count decomposition against nuclear surface/binding rows | CONDITIONAL_RESPONSE_NOT_PROMOTED | false |

## Numeric Shape Rows
| shape_id | material_id | shape_value_q_C | fraction_formula | coefficient_status | status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| SHAPE3257_PtRh10 | PtRh10 | 5.187582949000e+00 | f_EM,B=k_C*q_C,B | MISSING_SOURCE_BACKED_k_C | SHAPE_NUMERIC_FRACTION_NOT_ACCEPTED | false |
| SHAPE3257_TA6V | TA6V | 2.613068278000e+00 | f_EM,B=k_C*q_C,B | MISSING_SOURCE_BACKED_k_C | SHAPE_NUMERIC_FRACTION_NOT_ACCEPTED | false |
| SHAPE3257_TA6V_minus_PtRh10 | TA6V_minus_PtRh10 | -2.574514671000e+00 | f_EM,B=k_C*q_C,B | MISSING_SOURCE_BACKED_k_C | SHAPE_NUMERIC_FRACTION_NOT_ACCEPTED | false |

## Raw Candidate Rows
| row_id | material_id | component_id | fraction_value | fraction_uncertainty | basis_convention | acceptance_status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CFI3257_PtRh10_EM_Coulomb_candidate | PtRh10 | EM_Coulomb | MISSING_k_C_TIMES_5.187582949000e+00 | MISSING_COEFFICIENT_UNCERTAINTY | SEMF_Coulomb_shape_from_1909_proxy;fraction_requires_k_C=a_C/(m_u c^2) | REJECTED_BY_1233_NUMERIC_FRACTION_GATE | false |
| CFI3257_TA6V_EM_Coulomb_candidate | TA6V | EM_Coulomb | MISSING_k_C_TIMES_2.613068278000e+00 | MISSING_COEFFICIENT_UNCERTAINTY | SEMF_Coulomb_shape_from_1909_proxy;fraction_requires_k_C=a_C/(m_u c^2) | REJECTED_BY_1233_NUMERIC_FRACTION_GATE | false |

## Acceptance Audit
| audit_id | requirement | status | evidence | accepts_real_fraction | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| ACCEPT3257_0_schema_present | 1233 component-fraction schema exists and parses | PASS_SCHEMA_PRESENT | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1233_COMPONENT_FRACTION_SCHEMA.csv | false | false |
| ACCEPT3257_1_routes_present | TA6V and PtRh10 EM_Coulomb acquisition routes exist | PASS_ROUTE_PRESENT | ROUTE1328_TA6V_EM_Coulomb;ROUTE1328_PtRh10_EM_Coulomb | false | false |
| ACCEPT3257_2_shape_proxy_present | numeric alloy Coulomb shape proxy exists for both materials | PASS_SHAPE_PRESENT | SHAPE3257_PtRh10;SHAPE3257_TA6V;SHAPE3257_TA6V_minus_PtRh10 | false | false |
| ACCEPT3257_3_claim_fraction_rejected | fraction_value must be finite numeric with uncertainty, basis, and source | REJECTED_MISSING_SOURCE_BACKED_k_C_AND_UNCERTAINTY | CFI3257_PtRh10_EM_Coulomb_candidate;CFI3257_TA6V_EM_Coulomb_candidate | false | false |
| ACCEPT3257_4_parent_alpha_map_unsigned | MTS parent EM/alpha map must turn Coulomb fraction into parent-owned response | BLOCKED_PARENT_ALPHA_MAP_UNSIGNED | 1910 exact tensor contract remains nonclaim; 1328 routes remain external-basis-only | false | false |
| ACCEPT3257_5_toy_runner_executes | toy shell runner evaluates finite positive G_J values without evidence promotion | PASS_TOY_DRYRUN_ONLY | TOYSHELL_OUT3257_PtRh10;TOYSHELL_OUT3257_TA6V | false | false |

## Toy SEMF-Coefficient Fraction Dryrun
| toy_fraction_id | material_id | q_C_shape | toy_k_C | toy_fraction_value | toy_coefficient_meaning | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| TOYF3257_PtRh10 | PtRh10 | 5.187582949000e+00 | 7.700000000000e-04 | 3.994438870730e-03 | placeholder SEMF-scale k_C for code smoke only; not a sourced accepted coefficient | false |
| TOYF3257_TA6V | TA6V | 2.613068278000e+00 | 7.700000000000e-04 | 2.012062574060e-03 | placeholder SEMF-scale k_C for code smoke only; not a sourced accepted coefficient | false |
| TOYF3257_TA6V_minus_PtRh10 | TA6V_minus_PtRh10 | -2.574514671000e+00 | 7.700000000000e-04 | -1.982376296670e-03 | placeholder SEMF-scale k_C for code smoke only; not a sourced accepted coefficient | false |

## Toy Shell Output
| toy_output_id | material_id | E_EM_A_J | K_shell_m_minus3 | G_J_EM_EM_toy | finite_positive | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| TOYSHELL_OUT3257_PtRh10 | PtRh10 | 3.994438870730e-03 | 3.875000000000e+00 | 9.840188027058e-07 | true | false |
| TOYSHELL_OUT3257_TA6V | TA6V | 2.012062574060e-03 | 3.875000000000e+00 | 2.496748538447e-07 | true | false |

## Gram Update
| update_id | target | previous_formula | new_input_contract | runner_status | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| GJU3257_0_fraction_shape_to_material_Gram | G_J[EM,EM]_A | C_frame^2/(20*pi)*(f_EM,A M_A c^2)^2*K_shell | f_EM,A may be supplied by source-backed k_C q_C,A; currently only q_C,A is numeric and k_C is nonclaim/toy | TOY_NUMERIC_PATH_EXECUTES_REAL_CLAIM_PATH_REJECTED | false |
| GJU3257_1_pair_delta_shape | DeltaR_TA6V_PtRh10^EM | DeltaR_AB^EM=gamma_EM,A-gamma_EM,B | Delta q_C= q_C,TA6V - q_C,PtRh10 is present; Delta f_EM=k_C Delta q_C needs sourced k_C and alpha-response convention | DIFFERENTIAL_SHAPE_PRESENT_PARENT_RESPONSE_UNSIGNED | false |

## Claim Gates
| gate_id | gate | passed | reason | claim_allowed |
| --- | --- | --- | --- | --- |
| CG3257_0_real_fraction_row | at least one real EM_Coulomb fraction row accepted under 1233 | false | numeric q_C shape exists but source-backed k_C, uncertainty, isotope convention, and parent map are absent | false |
| CG3257_1_toy_runner | toy shell branch evaluates finite numbers | true | runner computes toy f_EM and G_J without promoting them as evidence | false |
| CG3257_2_local_GR | local GR/Newton/Maxwell/source-coupling claim | false | parent EM owner/alpha map, source kernel, and accepted material fractions remain unsigned | false |

## Decision
| decision_id | verdict | what_moved | what_remains | selected_next | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| DEC3257_0 | NO_REAL_ACCEPTED_FRACTION_ROW_BUT_TOY_DRYRUN_CLOSED | q_C alloy shape now feeds a concrete f_EM=k_C q_C contract and a runnable G_J[EM,EM] dry-run | source-backed k_C/a_C, uncertainty, isotope convention, no-double-count basis, parent EM/alpha response map, source/readout kernel | source-backed EM Coulomb coefficient or parent alpha-map owner | false |

## Next Target
| next_id | selected | target_doc | target_script | objective | guardrail | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| NEXT3257_0_3258 | primary | 3258-Y5-R2FR-source-backed-EM-Coulomb-coefficient-or-parent-alpha-map-owner-under-AX1090.md | scripts/Y5_R2FR_3258_source_backed_EM_Coulomb_coefficient_or_parent_alpha_map_owner.py | Either source a claim-grade Coulomb coefficient/mass convention for f_EM=k_C q_C, or derive the parent alpha-map owner that makes gamma_EM parent-owned rather than external SEMF smoke. | No local-GR/WEP/Maxwell claim unless accepted fraction rows, response map, and source kernel all pass. | false |

## Validation
| check_id | check | passed | detail |
| --- | --- | --- | --- |
| VAL3257_0_sources_exist | all required source paths exist | true |  |
| VAL3257_1_sources_parse | all required source CSV/MD paths parse | true |  |
| VAL3257_2_outputs_parse | all 3257 output CSVs parse | true |  |
| VAL3257_3_shape_numeric | TA6V and PtRh10 q_C shape values are finite numeric | true | 5.187582949;2.613068278 |
| VAL3257_4_raw_candidates_nonclaim | all raw candidate fraction rows remain valid_for_claim=false | true | CFI3257_PtRh10_EM_Coulomb_candidate;CFI3257_TA6V_EM_Coulomb_candidate |
| VAL3257_5_toy_outputs_finite_positive | toy shell G_J outputs are finite positive | true | TOYSHELL_OUT3257_PtRh10;TOYSHELL_OUT3257_TA6V |
| VAL3257_6_no_claim_gate_promoted | no 3257 claim gate allows a local-GR/WEP/Maxwell claim | true | all claim_allowed=false |
| VAL3257_7_formalization_untouched | formalization-workbench modified-file count remains zero by this script | true | formalization_changed_count=0 |
| VAL3257_8_overall | 3257 validation overall | true | all required checks passed |

Generated UTC: 2026-06-27T05:30:01.437120+00:00
