# 3256 - Material EM binding projection or toy charged-shell smoke input under AX1090

Generated: `2026-06-27T05:20:42.587068+00:00`

Private derivation checkpoint. This does not claim local GR, Newton, Maxwell, WEP, R10, PPN, clock, orbital, material-response, or public source-coupling success.

## Summary
- `3256` converts the `3255` Coulomb-shell toy parameter into material EM-binding language.
- Key bridge: match the shell energy to internal EM binding, `U_EM_shell = E_EM,A = f_EM,A M_A c^2`.
- This gives `Q_eff^2 = 8*pi*epsilon0*E_EM,A/(R_in^-1-R_out^-1)` and removes fake external net-charge dependence.
- The material surrogate self-entry is now `G_J[EM,EM]_A = C_frame^2/(20*pi)*(f_EM,A M_A c^2)^2*K_shell(R_in,R_out)`.
- `K_shell=(R_in^-5-R_out^-5)/(R_in^-1-R_out^-1)^2`.
- This is still nonclaim: accepted `f_EM,A`, material mass, profile/cutoffs, tau/source kernel, and no-double-count basis are missing.

## Material EM Binding Projection

| projection_id | object | formula | derivation | required_inputs | current_status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| MEP3256_0_material_energy_split | material EM binding energy | E_EM,A := f_EM,A M_A c^2 | use the existing component-fraction basis: EM/Coulomb is an internal material energy fraction, not an external net charge | f_EM,A;M_A;c;basis convention;source path | PROJECTION_FORMULA_READY_VALUES_MISSING | false |
| MEP3256_1_alpha_response | material EM response | gamma_EM,A := partial ln M_A / partial ln alpha_EM = (alpha_EM/M_A c^2) partial_alpha E_EM,A | if E_EM,A scales linearly with alpha in the chosen convention, gamma_EM,A approx f_EM,A; otherwise retain gamma_EM,A as sourced derivative | alpha-scaling convention or sourced derivative;no double-counting with nuclear surface/binding rows | CONDITIONAL_APPROX_OR_DERIVATIVE_ROW_REQUIRED | false |
| MEP3256_2_differential_material_projection | Ti/Pt or body-pair EM projection | DeltaR_AB^EM = gamma_EM,A - gamma_EM,B | inherits the 1910 response law DeltaR_AB^X=sum_c(f_Ac-f_Bc)gamma_cX when EM is the selected component | gamma_EM or f_EM rows for both bodies;material alloy/isotope convention;tau/source kernel | PAIR_FORMULA_READY_VALUES_MISSING | false |
| MEP3256_3_no_external_neutrality_shortcut | neutral material handling | Q_net,A=0 does not imply E_EM,A=0 or f_EM,A=0 | internal Coulomb/binding stress remains a material response even if the external field is screened | material binding projection rather than external Q_eff alone | GUARDRAIL_ACTIVE | false |

## Coulomb Shell Energy Match

| match_id | object | formula | result | derivation | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| CSM3256_0_energy_match | replace Q_eff by E_EM,A | U_EM_shell = Q_eff^2/(8*pi*epsilon0)*(1/R_in-1/R_out) = E_EM,A | Q_eff^2 = 8*pi*epsilon0*E_EM,A/(R_in^-1-R_out^-1) | solve the 3255 shell energy formula for Q_eff^2 | false |
| CSM3256_1_material_Gram_self | G_J[EM,EM]_A material shell surrogate | G_J[EM,EM]_A = C_frame^2/(20*pi) * E_EM,A^2 * (R_in^-5-R_out^-5)/(R_in^-1-R_out^-1)^2 | substitute CSM3256_0 into the 3255 Q_eff^4 shell Gram formula | epsilon0 cancels; the remaining dependence is material EM energy squared times shell-shape factor | false |
| CSM3256_2_fraction_form | G_J[EM,EM]_A in component fraction variables | G_J[EM,EM]_A = C_frame^2/(20*pi) * (f_EM,A M_A c^2)^2 * K_shell(R_in,R_out) | K_shell := (R_in^-5-R_out^-5)/(R_in^-1-R_out^-1)^2 | use E_EM,A=f_EM,A M_A c^2 | false |
| CSM3256_3_distribution_generalization | non-shell material distribution | G_J[EM,EM]_A = integral_A w_J u_EM,A(x)^2 dV_eobs | shell formula is a surrogate when u_EM,A(x) is replaced by an energy-matched shell profile | keeps the true target as a stress-current norm, not a forced spherical model | false |

## Toy Charged Shell Smoke Input

| toy_id | allowed_use | material_id | Q_eff | R_in | R_out | C_frame | formula_target | forbidden_use | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TOY3256_0_charged_shell_schema | code/schema smoke only | toy_charged_shell | MISSING_TOY_VALUE | MISSING_TOY_VALUE | MISSING_TOY_VALUE | MISSING_TOY_VALUE | G_J[EM,EM]_shell = C_frame^2 Q_eff^4/(1280*pi^3*epsilon0^2)*(R_in^-5-R_out^-5) | FORBIDDEN_FOR_CLAIM: real neutral matter, WEP, local-GR, Maxwell, or source-coupling evidence | false |
| TOY3256_1_material_surrogate_schema | debug material projection algebra only | toy_material_EM_fraction | derived_from_E_EM_not_external_charge | MISSING_TOY_VALUE | MISSING_TOY_VALUE | MISSING_TOY_VALUE | G_J[EM,EM]_A = C_frame^2/(20*pi)*(f_EM,A M_A c^2)^2*K_shell | FORBIDDEN_FOR_CLAIM: claim-grade material response unless f_EM,A, M_A, cutoffs, and source/readout kernel are sourced | false |

## Material Acceptance Gates

| gate_id | required_object | acceptance_rule | current_status | valid_for_claim |
| --- | --- | --- | --- | --- |
| ACC3256_0_component_fraction | f_EM,A | must be finite numeric with uncertainty, basis convention, source path/URL/DOI, and extraction method matching the 1233 schema | MISSING_ACCEPTED_EM_FRACTION_ROWS | false |
| ACC3256_1_material_mass | M_A or mass density profile | must match the same material body, isotope/alloy convention, and source-worldtube used by the tau/readout kernel | MISSING_SAME_ARENA_MATERIAL_MASS | false |
| ACC3256_2_shape_cutoffs | R_in/R_out or u_EM(x) | either source a real EM energy-density distribution u_EM(x), or declare shell cutoffs as a toy/surrogate envelope | MISSING_SHAPE_PROFILE_OR_TOY_LABEL | false |
| ACC3256_3_no_double_count | component basis map | EM_Coulomb fraction must not double-count nuclear surface/asymmetry, QCD/gluon binding, electron rest mass, or readout rows | BASIS_CONVENTION_REQUIRED | false |
| ACC3256_4_tau_source_kernel | tau/source/readout kernel | material Gram row cannot be inserted into WEP/PPN/local-GR until the same tau/e_obs/source-worldtube convention is declared | MISSING_TAU_SOURCE_KERNEL | false |

## GJ EM EM Material Update

| update_id | target | previous_symbolic_value | new_symbolic_value | gain | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| GJU3256_0_Qeff_to_material | G_J[EM,EM] | C_frame^2 Q_eff^4/(1280*pi^3*epsilon0^2)*(R_in^-5-R_out^-5) | C_frame^2/(20*pi)*(f_EM,A M_A c^2)^2*K_shell(R_in,R_out) | external charge parameter is replaced by internal material EM binding energy | false |
| GJU3256_1_material_pair | material-pair EM response | MISSING_SCREENING_OR_BINDING_SOURCE | DeltaR_AB^EM = gamma_EM,A - gamma_EM,B, with gamma_EM,A approx f_EM,A only under sourced linear-alpha convention | connects C_Tw EM row to WEP/source coupling material-response language | false |
| GJU3256_2_CTw_status | C_Tw matrix | first diagonal EM shell formula only | first diagonal material-surrogate formula only; cross entries and accepted material rows still required | makes next missing objects precise rather than broad | false |

## Neutrality And Double Count Guards

| guard_id | statement | blocks_bad_move | required_safe_move | valid_for_claim |
| --- | --- | --- | --- | --- |
| NG3256_0_external_neutrality | External Q_net=0 does not imply internal EM_Coulomb binding fraction f_EM,A=0. | using neutral material as an EM stress zero theorem | use f_EM,A or gamma_EM,A from material binding/source rows | false |
| NG3256_1_shell_surrogate | The shell energy match is a surrogate profile unless a real u_EM,A(x) distribution is sourced. | treating R_in/R_out as physical without source-worldtube geometry | label toy shell rows or source actual material/profile geometry | false |
| NG3256_2_double_count | EM_Coulomb, nuclear surface/asymmetry, QCD binding, electron rest mass, and readout fractions must be basis-disjoint. | counting the same binding energy in multiple source components | declare basis convention and no-double-count map before score | false |
| NG3256_3_DD_external_comparator | Damour-Donoghue style material charges may guide extraction but do not become parent MTS coefficients by copy-paste. | claiming MTS source coupling from external phenomenological charges alone | record external basis as comparator or derive parent basis map | false |

## Claim Gates

| claim_gate_id | claim | gate_pass | reason | claim_allowed |
| --- | --- | --- | --- | --- |
| CG3256_0_energy_match_derivation | Coulomb shell energy matching to material EM binding is algebraically derived | true | CSM3256_0 through CSM3256_2 eliminate Q_eff in favour of E_EM,A=f_EM,A M_A c^2 | false |
| CG3256_1_material_projection_shape | material projection formula is structurally ready | true | MEP3256 rows define f_EM,A/gamma_EM,A and DeltaR_AB^EM gates | false |
| CG3256_2_material_numeric | material EM binding projection is numeric/source-backed | false | accepted f_EM,A, M_A, profile/cutoffs, tau/source kernel, and basis map are missing | false |
| CG3256_3_toy_smoke_claim | toy charged shell is evidence for real material/source coupling | false | toy rows are schema/debug only and explicitly forbidden for claims | false |
| CG3256_4_local_GR_Newton_Maxwell | local GR/Newton/Maxwell source branch is derived or bounded enough to claim | false | only symbolic material projection is derived; numeric rows/cross terms/theorem-zero branch remain open | false |

## Decisions

| decision_id | decision | because | next_action | valid_for_claim |
| --- | --- | --- | --- | --- |
| DEC3256_0_progress | Use energy matching to turn Q_eff shell language into material EM binding language | this removes the most misleading toy parameter and connects the Gram row to real material fractions | source accepted f_EM,A rows or build an explicitly toy charged-shell smoke input | false |
| DEC3256_1_best_next | Prioritize accepted EM_Coulomb fraction rows over numeric toy shell values | real local-GR/source coupling needs neutral material binding, not external net charge | fill 1233-style rows for TA6V/PtRh10 or an Earth/source material with basis/source/provenance | false |
| DEC3256_2_no_claim | Keep all outputs private nonclaim | deriving the bridge equation is progress but not evidence until inputs are sourced | carry no-claim gates to 3257 | false |

## Next Target

| next_id | selection | next_checkpoint | next_script | objective | guardrail | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| NEXT3256_0_3257 | selected_primary | 3257-Y5-R2FR-first-accepted-EM-Coulomb-fraction-row-or-toy-shell-runner-dryrun-under-AX1090.md | scripts/Y5_R2FR_3257_first_accepted_EM_Coulomb_fraction_row_or_toy_shell_runner_dryrun.py | Either fill the first 1233-schema EM_Coulomb material fraction row with source/provenance, or run a clearly labelled toy-shell dry-run that cannot be mistaken for evidence. | No local-GR/Newton/Maxwell/WEP claim from toy rows or unsourced material fractions. | false |

## Source Register

| source_id | source_path | exists | parse_ok | role | evidence_hits | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| SRC3256_3255_handoff | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3255-Y5-R2FR-EM-Gram-row-input-pack-or-static-Coulomb-stress-envelope-under-AX1090.md | true | true | 3255 selected material EM binding projection or toy shell smoke input | L5:Private derivation checkpoint. This does not claim local GR, Newton, Maxwell, WEP, R10, PPN, clock, orbital, material binding, or public source-coupling success. \| L12:- The diagonal Gram self-entry is now symbolic: `G_J[EM,EM]_shell=C_frame^2 Q_eff^4/(1280*pi^3*epsilon0^2)*(R_in^-5-R_out^-5)`. \| L20:\| ARENA3255_1_current_norm \| L2 energy-current norm \| G_J[EM,EM] := integral_Aext u_EM(r)^2 dV_eobs for tau=unit static observer and J_EM=tau-energy-current \| matches the 3253 Gram/eigenvalue requirement while giving an analytic Coulomb she \| L31:\| CSE3255_3_L2_energy_current_shell \| G_J[EM,EM] shell envelope \| G_J[EM,EM]_shell = integral u_EM^2 dV = Q_eff^4/(1280*pi^3*epsilon0^2)*(R_in^-5 - R_out^-5) \| integrate [Q_eff^2/(32*pi^2*epsilon0*r^4)]^2 * 4*pi*r^2 dr \| same current norm;Q | false |
| SRC3256_3255_envelope | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3255_STATIC_COULOMB_STRESS_ENVELOPE.csv | true | true | static Coulomb shell energy and Gram formula | L4:CSE3255_2_L1_energy_shell,\|\|J_EM\|\|_L1 shell envelope,U_EM_shell = integral u_EM dV = Q_eff^2/(8*pi*epsilon0)*(1/R_in - 1/R_out),"integrate u_EM(r)*4*pi*r^2 dr over [R_in,R_out]",Q_eff;epsilon0;R_in>0;R_out>R_in,false \| L5:CSE3255_3_L2_energy_current_shell,"G_J[EM,EM] shell envelope","G_J[EM,EM]_shell = integral u_EM^2 dV = Q_eff^4/(1280*pi^3*epsilon0^2)*(R_in^-5 - R_out^-5)",integrate [Q_eff^2/(32*pi^2*epsilon0*r^4)]^2 * 4*pi*r^2 dr,same current norm;Q_eff;e | false |
| SRC3256_3255_inputs | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3255_GJ_EM_EM_INPUT_REQUIREMENTS.csv | true | true | Q_eff/cutoff/screening input requirements | L2:IN3255_0_Q_eff,Q_eff,effective charge or EM binding/source envelope feeding the Coulomb shell,CSE3255_0 through CSE3255_4,MISSING_Q_EFF_OR_MATERIAL_BINDING_MAP,"source profile, material EM binding model, or explicit neutralization/screening \| L7:IN3255_5_screening_neutrality,screening/neutralization/material map,map from real material EM binding to the idealized Q_eff shell envelope,applying the envelope to WEP/local matter rather than a toy charged shell,MISSING_SCREENING_OR_BINDI | false |
| SRC3256_1232_formula | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1232_COMPONENT_FRACTION_FORMULA_LEDGER.csv | true | true | component-fraction formula ledger | L2:FORM1232_0_alloy_average,component fraction in material B,"F_{B,c}=sum_{elements E in B} x_{B,E} sum_i p_{E,i} F_{E,i,c}",alloy mass fractions x; isotope fractions p; isotope component fractions F,FORMULA_READY_INPUTS_MISSING,False,False \| L4:FORM1232_2_delta_w_prediction,Delta_w_TiPt,"Delta_w_TiPt=sum_c DeltaF_{TiPt,c} delta w_c + DeltaK_TiPt",DeltaF rows; component priors; readout/measure residual,NONCLAIM_TEMPLATE_ONLY,False,False | false |
| SRC3256_1233_schema | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1233_COMPONENT_FRACTION_SCHEMA.csv | true | true | component fraction acceptance schema | L4:component_id,True,must map to DCW1231 component basis,electron;light_quark;QCD_gluon;EM_Coulomb;nuclear_surface;measure_readout,True,False,False \| L5:fraction_value,True,finite numeric >=0 unless signed residual explicitly justified,dimensionless energy/mass fraction,True,False,False | false |
| SRC3256_1328_routes | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1328_COMPONENT_SOURCE_ROUTE_MATRIX.csv | true | true | source routes for EM_Coulomb material fraction | L8:ROUTE1328_TA6V_EM_Coulomb,TA6V,EM_Coulomb,PSRC1328_5_Damour_Donoghue_dilaton_charges;PSRC1328_6_Damour_Donoghue_DOI,external DD Coulomb/electromagnetic binding charge or SEMF Coulomb term after isotope/alloy averaging,MTS EM owner and alpha \| L9:ROUTE1328_PtRh10_EM_Coulomb,PtRh10,EM_Coulomb,PSRC1328_5_Damour_Donoghue_dilaton_charges;PSRC1328_6_Damour_Donoghue_DOI,external DD Coulomb/electromagnetic binding charge or SEMF Coulomb term after isotope/alloy averaging,MTS EM owner and a | false |
| SRC3256_1394_composition | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1394_BULK_MATERIAL_COMPOSITION_MAP.csv | true | true | bulk material composition and binding interface | L3:MCM1394_1_source_nuclear,source,nuclear_binding,"f_nuc,S",beta_nuc,"f_nuc,S*beta_nuc",source nuclear binding fraction and nuclear beta row or theorem-zero,MISSING,MISSING_SOURCE_NUCLEAR_FRACTION_OR_BETA,False,False \| L4:MCM1394_2_source_EM,source,EM_binding,"f_EM,S",beta_EM,"f_EM,S*beta_EM",source EM binding/charge fraction and EM beta row or theorem-zero,MISSING,MISSING_SOURCE_EM_FRACTION_OR_BETA,False,False \| L6:MCM1394_4_test_nuclear,test,nuclear_binding,"f_nuc,T",beta_nuc,"f_nuc,T*beta_nuc",test nuclear binding fraction and nuclear beta row or theorem-zero,MISSING,MISSING_TEST_NUCLEAR_FRACTION_OR_BETA,False,False \| L7:MCM1394_5_test_EM,test,EM_binding,"f_EM,T",beta_EM,"f_EM,T*beta_EM",test EM binding/charge fraction and EM beta row or theorem-zero,MISSING,MISSING_TEST_EM_FRACTION_OR_BETA,False,False | false |
| SRC3256_1395_binding_pack | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1395_BINDING_SECTOR_BETA_SOURCE_PACK.csv | true | true | binding sector beta source pack | L2:SBP1395_0_beta_e,beta_e,electronic_atomic,canonical phi_c derivative of electronic/atomic contribution to observed bulk mass and clock standards,"beta_bind,A via f_e,A beta_e; clocks/constants; WEP material contrast; R10 material leg","elec \| L3:SBP1395_1_beta_nuc,beta_nuc,nuclear_binding,canonical phi_c derivative of nuclear binding/composite rest-mass contribution,"beta_bind,A via f_nuc,A beta_nuc; WEP material contrast; orbital/self-energy residuals; R10 material leg",nuclear/QC \| L4:SBP1395_2_beta_EM,beta_EM,EM_binding,canonical phi_c derivative of EM binding/charge/fine-structure contribution,"beta_bind,A via f_EM,A beta_EM; alpha_EM/clock; Coulomb WEP; R10 material leg","EM-lock theorem, alpha_EM readout descent, no- \| L5:SBP1395_3_beta_other_guard,beta_other,other_binding_or_readout,placeholder guard for any binding/readout sector not covered by e/nuc/EM,"beta_bind,A residual envelope if sector inventory is incomplete",proof sector inventory is complete or  | false |
| SRC3256_1909_blockers | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1909_MATERIAL_BINDING_PROJECTION_BLOCKER_LEDGER_NONCLAIM.csv | true | true | Ti/Pt material binding projection blockers | L3:BB1909_1_atomic_nuclear_mass_convention,atomic-to-nuclear mass and electron subtraction convention,electron rest-mass fraction proxy from 1330,atomic masses include electrons and chemical/nuclear conventions; WEP response tensor needs one n \| L4:BB1909_2_EM_Coulomb_binding_owner,EM/Coulomb binding response under MTS parent generator,DD-style smoke components and rough coulomb_formula_proxy,external Damour-Donoghue or liquid-drop proxies cannot be imported as MTS parent coefficients \| L5:BB1909_3_nuclear_binding_decomposition,nuclear volume/surface/asymmetry/pairing/QCD split,surface/binding smoke contrast only,one scalar surface proxy cannot stand in for a source-basis tensor unless the parent basis selects it,exact mass-d \| L6:BB1909_4_lattice_impurity_and_shape,"alloy lattice/chemical binding, impurities, coatings, and test-body geometry convention",bulk mass-fraction alloy labels only,flight test bodies are not abstract elemental mixtures; local source response | false |
| SRC3256_1910_contract | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_PARENT_QLOC_1910_EXACT_MASS_DEFECT_TENSOR_CONTRACT_NONCLAIM.csv | true | true | exact mass-defect tensor contract | L2:MDT1910_0_common_mode,universal_common_mode_mass_energy,DeltaR_AB^U = 0 if V_U M_A = sigma_U M_A for all ordinary A,not needed if theorem signed,parent-signed universal minimal-coupling/common-mode theorem,one matter action/current/source o \| L3:MDT1910_1_electron_rest,electron,DeltaR_AB^e = f_Ae - f_Be if V_e rescales electron rest energy only,3.129116287420e-05,CODATA/NIST electron fraction plus parent owner for electron rest-mass generator,V_e and C_e derived or theorem-zero in  \| L4:MDT1910_2_nucleon_or_light_quark_rest,light_quark_or_nucleon_rest,DeltaR_AB^q = sum_isotopes Deltaf_isotope partial ln M_isotope/partial ln m_q in the declared parent basis,Z_over_A=5.677745651272e-02; N_over_A=-5.677745651272e-02,AME/nucle \| L5:MDT1910_3_EM_Coulomb_binding,EM_Coulomb,DeltaR_AB^alpha = partial_alpha ln M_A - partial_alpha ln M_B with EM binding owned by the parent EM generator,WCM1053_4 DD alpha/Coulomb smoke; AP1909 coulomb_formula_proxy=-2.574514671000e+00,parent | false |
| SRC3256_3129_binding_pressure | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3129-Y5-R2FR-Earth-source-calibration-smoke-and-binding-pressure-channel-under-AX1090.md | true | true | binding pressure/source channel guard | L1:# 3129 - Earth Source-Calibration Smoke and Binding Pressure Channel under AX1090 \| L79:## Binding Pressure Channel \| L84:Q_surface_binding_Earth = -0.01211918219995745. \| L90:\|Q_surface_binding_Earth delta_J\| = 8.526876722826009e-15. | false |
| SRC3256_3130_boundary_suppression | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3130-Y5-R2FR-binding-boundary-suppression-or-profile-fill-under-AX1090.md | true | true | boundary suppression/profile fork | L36:If the surface/binding term is an exact boundary partition term: \| L58:If the surface/binding channel survives with residual factor `rho_surf`, then: \| L61:DeltaC_Scal,surf = rho_surf Q_surface_binding_Earth. \| L67:\|rho_surf\| <= 0.3283734585378189. | false |

## Validation

| validation_id | passed | requirement | evidence |
| --- | --- | --- | --- |
| VAL3256_0_sources_exist_parse_hit | true | every cited source exists, parses, and has evidence hits | True |
| VAL3256_1_output_csvs_parse | true | all 3256 output CSVs parse before validation write | True |
| VAL3256_2_material_energy_split | true | material EM binding energy split exists | True |
| VAL3256_3_shell_match | true | Q_eff elimination and material GJ formula are present | q=True material=True |
| VAL3256_4_toy_quarantined | true | toy shell rows are nonclaim and forbidden for evidence | True |
| VAL3256_5_acceptance_missing | true | acceptance gates preserve missing/required status | True |
| VAL3256_6_gram_material_update | true | GJ EM self-entry updated to material binding variables | True |
| VAL3256_7_guards_present | true | neutrality and double-count guards are present | True |
| VAL3256_8_nonclaim_claims_blocked | true | all rows nonclaim and local-GR/Newton/Maxwell gate blocked | nonclaim=True claims=True |
| VAL3256_9_output_scope | true | all generated files stay in post-checkpoint-work | True |
| VAL3256_10_formalization_untouched | true | no 3256 files are written under formalization-workbench | file_count=0 |
| VAL3256_11_next_target | true | 3257 next target is selected | True |
| VAL3256_OVERALL | true | 3256 validation overall | all required validation rows passed |

## Working Verdict
`3256` is a useful leap because the EM Gram row is no longer tied to an unphysical external `Q_eff` for neutral matter. It now has a bridge to the real material quantity: internal EM/Coulomb binding energy fraction. The next practical move is to fill one accepted `EM_Coulomb` fraction row, or run a toy shell only as a labelled code smoke.
