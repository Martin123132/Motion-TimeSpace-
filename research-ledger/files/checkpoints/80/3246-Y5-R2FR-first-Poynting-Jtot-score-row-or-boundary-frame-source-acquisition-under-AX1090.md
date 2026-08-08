# 3246 - First Poynting Jtot Score Row or Boundary/Frame Source Acquisition under AX1090

Generated: `2026-06-27T04:03:54.705998+00:00`

Status: `Y5_R2FR_3246_first_Poynting_Jtot_score_row_schema_written_boundary_frame_flux_inputs_missing_nonclaim`

Claim ceiling: `score_schema_only_no_numeric_Poynting_component_no_Poynting_zero_no_Jtot_score_no_amplitude_score_no_local_GR_claim`

## Summary

- `3246` attempts the first concrete `J_tot` score row, using the Poynting/collar flux component selected in `3245`.

- The formula is now executable in shape: `|J_A^Poynting| <= ||e_A||_B(C_flux||S_EM dot n||_B+B_corner_flux)+||e_A||_coll C_coll||T_EM(u,n)||_collar`.

- It is not numeric yet because the boundary/collar label, observed frame `u,n`, constants `C_flux/C_coll`, flux norms, response-basis norms, units and source path are not present.

- The quiet-static zero route is also separated from the finite-flux route: Poynting can be zero in a quiet electrostatic limit, but that does not zero Maxwell stress, EM self-energy, Coulomb coupling, or full `J_tot`.

- Next target is therefore not another theorem: it is the parent-owned boundary/frame certificate, or a specific arena source row.

## First Poynting Jtot Score Row

| score_id | component_id | boundary_id | surface_class | field_regime | frame_u | normal_n | C_flux | C_coll | S_normal_norm_B | T_EM_un_norm_collar | eA_norm_B | eA_norm_collar | B_corner_flux | units | source_path | computed_J_Poynting_bound | zero_certificate | status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PJS3246_0_first_component | JTC3245_0_selected | MISSING_PARENT_BOUNDARY_ID | MISSING_BOUNDARY_COLLAR_WORLDTUBE_CLASS | UNCLASSIFIED_REQUIRES_QUIET_STATIC_OR_FINITE_FLUX | MISSING_OBSERVED_FRAME_U | MISSING_BOUNDARY_NORMAL_N | MISSING_C_FLUX | MISSING_C_COLL | MISSING_NORM_S_EM_DOT_N_ON_B | MISSING_NORM_T_EM_U_N_ON_COLLAR | MISSING_RESPONSE_BASIS_NORM_ON_B | MISSING_RESPONSE_BASIS_NORM_ON_COLLAR | MISSING_CORNER_WORLDTUBE_REMAINDER | MISSING_COMMON_JTOT_UNITS | MISSING_SOURCE_PATH_FOR_NUMERIC_INPUTS | NOT_COMPUTED_MISSING_INPUTS | false | FILLABLE_SCORE_ROW_NONCLAIM | false |

## Boundary/Frame/Flux Acquisition Ledger

| acq_id | field | needed_input | derivation_or_source_route | claim_if_missing | priority |
| --- | --- | --- | --- | --- | --- |
| ACQ3246_0_boundary | boundary_id;surface_class | parent-owned local boundary/collar/worldtube label and support class | derive from local test-domain definition or source from existing local arena runner | cannot choose the boundary after seeing flux | 1 |
| ACQ3246_1_frame | frame_u;normal_n | observed tetrad/frame u and outward normal n | derive from observed coframe/public metric branch; must match T_EM readout | Poynting flux is frame/surface ambiguous | 2 |
| ACQ3246_2_flux_constants | C_flux;C_coll | operator constants mapping boundary/collar flux norms into Jtot units | dual norm of response test function and collar embedding constant | no numerical Jtot component can be computed | 3 |
| ACQ3246_3_flux_norms | S_normal_norm_B;T_EM_un_norm_collar | EM stress flux norms on the selected boundary/collar | quiet-static zero certificate, measured/source-backed EM field bounds, or finite arena model | component remains formula-only | 4 |
| ACQ3246_4_response_norm | eA_norm_B;eA_norm_collar | response basis norm under the same Z normalization used by M_AB | M_AB/Z basis owner ledger and boundary trace inequality | cannot connect flux to response amplitude denominator | 5 |
| ACQ3246_5_units | units;source_path | common action-density/Jtot units and source provenance | same unit convention as 3244/3245 amplitude transfer | row cannot be valid_for_claim | 6 |

## Poynting Regime Zero Or Bound Classifier

| regime_id | field_regime | zero_condition | finite_bound | caveat | current_status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| REG3246_0_quiet_static | quiet_static_no_radiation_no_normal_magnetic_flux | H_radiative=0 and n dot(E x H_static)=0 on the parent-owned boundary | J_Poynting_bound=0 for this subchannel only | does not zero EM energy density, spatial stress, Coulomb coupling or full Jtot | CERTIFICATE_MISSING | false |
| REG3246_1_electrostatic | electrostatic_bound_field | S_EM dot n=0 can hold while EM stress/energy remains nonzero | Poynting component may be zero; EM source-coupling still lives elsewhere | do not confuse Poynting silence with Maxwell/EM stress silence | CLASSIFIER_READY_NOT_SELECTED | false |
| REG3246_2_crossed_fields | static_crossed_or_circulating_field_momentum | normal projection vanishes by owned geometry or averaging | \|n dot S\| <= \|E\|\|H\| and Phi <= C_flux\|\|S_EM dot n\|\| | requires sourced field bounds and boundary geometry | FINITE_BOUND_ROUTE | false |
| REG3246_3_radiative | radiative_or_time_dependent_EM | none unless no-flux support is explicitly proven | J_Poynting_bound <= C_coll\|\|T_EM(u,n)\|\|_collar | using radiation flux to rescue static local GR is the wrong limit unless the test arena is radiative | LIVE_BOUND_REQUIRED | false |

## Score Row Dry Run

| dry_run_id | check | passed | evidence | claim_effect |
| --- | --- | --- | --- | --- |
| DRY3246_0_schema | required columns present | true | score_id;component_id;boundary_id;surface_class;field_regime;frame_u;normal_n;C_flux;C_coll;S_normal_norm_B;T_EM_un_norm_collar;eA_norm_B;eA_norm_collar;B_corner_flux;units;source_path;computed_J_Poynting_bound;zero_certificate;status;valid_for_claim | schema ready only |
| DRY3246_1_missing | missing inputs detected | true | boundary_id;surface_class;field_regime;frame_u;normal_n;C_flux;C_coll;S_normal_norm_B;T_EM_un_norm_collar;eA_norm_B;eA_norm_collar;B_corner_flux;units;source_path;computed_J_Poynting_bound | blocks numeric promotion |
| DRY3246_2_valid_flag | valid_for_claim remains false | true | false | no empirical/local-GR claim |
| DRY3246_3_zero | zero certificate not asserted | true | false | no Poynting-zero shortcut |

## Jtot/Amplitude Transfer Update

| transfer_id | target | formula | current_status | valid_for_claim |
| --- | --- | --- | --- | --- |
| XFER3246_0_component_bound | Poynting contribution to Jtot | \|J_A^Poynting\| <= \|\|e_A\|\|_B(C_flux\|\|S_EM dot n\|\|_B+B_corner_flux)+\|\|e_A\|\|_coll C_coll\|\|T_EM(u,n)\|\|_coll | FORMULA_READY_INPUTS_MISSING | false |
| XFER3246_1_Jtot | Jtot total bound | \|\|Jtot\|\| <= \|\|J_bulk\|\| + \|J_A^Poynting\| + \|\|B_other\|\| + \|\|J_oddGamma\|\| | PARTIAL_COMPONENT_INTERFACE_ONLY | false |
| XFER3246_2_amplitude | response amplitude | \|\|Z_*\|\| <= m0^{-1}\|\|Jtot\|\| after M_AB coercivity is sourced | WAITING_ON_M0_AND_NUMERIC_COMPONENTS | false |

## Claim Gates

| claim_gate_id | claim | condition_passed | status | claim_allowed |
| --- | --- | --- | --- | --- |
| CG3246_0_score_schema | first Poynting Jtot score-row schema exists | true | fillable row written | false |
| CG3246_1_numeric_component | first Poynting Jtot component is numeric/source-backed | false | boundary/frame/constants/flux norms/units missing | false |
| CG3246_2_zero_component | Poynting component is zero | false | quiet/static or exact no-flux certificate missing | false |
| CG3246_3_amplitude_score | Jtot amplitude score can be computed | false | needs numeric component plus m0 coercivity | false |
| CG3246_4_local_GR | local GR/Newton/PPN reduction | false | no numeric qloc/amplitude residual | false |

## Decision Ledger

| decision_id | decision | because | next_action |
| --- | --- | --- | --- |
| DEC3246_0_real_fill_attempt | The first Poynting Jtot score row is created but not promoted. | Existing files supply the formula, not the boundary/frame/flux constants needed for a number. | Acquire boundary/frame inputs or derive a quiet-static zero certificate. |
| DEC3246_1_no_F2_shortcut | Reject F^2=0 as a Poynting score substitute. | Earlier guards show null radiation can have nonzero stress/Poynting flux. | Keep stress-flux norm separate from scalar EM_F2 rows. |
| DEC3246_2_best_next | Next target should choose the actual local arena boundary and frame. | That is the first field in the score row; without it all later numbers are floating. | Build the parent-owned boundary/frame certificate or a nonclaim arena source row. |

## Next Target

| next_id | priority | next_doc | next_script | objective | exclude | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| NEXT3246_0_3247 | selected_primary | 3247-Y5-R2FR-parent-owned-boundary-frame-certificate-or-Poynting-arena-source-row-under-AX1090.md | scripts/Y5_R2FR_3247_parent_owned_boundary_frame_certificate_or_Poynting_arena_source_row.py | Try to derive or source the parent-owned boundary/collar/worldtube and observed frame u,n for the first Poynting Jtot score row; if unavailable, write the first arena-specific nonclaim source row. | do not choose boundary after seeing flux; do not claim Poynting zero from F2; do not edit formalization-workbench | false |

## Source Register

| source_id | source_path | exists | parse_ok | role | evidence_hits | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| SRC3246_3245 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3245-Y5-R2FR-MAB-coercivity-and-first-Jtot-component-bound-under-AX1090.md | true | true | immediate handoff: first Poynting Jtot component | L5:Status: `Y5_R2FR_3245_MAB_Rayleigh_coercivity_certificate_written_first_Poynting_Jtot_component_interface_added_nonclaim` \| L17:- The first concrete `J_tot` component interface is selected: the Poynting/collar boundary flux from `3234`, because it already has a finite bound functional and is directly tied to EM stress coupling. \| L45:\| JTC3245_0_selected \| boundary/Poynting flux contribution to B_A subset J_A^tot \| 3234 finite Poynting/collar flux functional \| \\|J_A^Poynting\\| <= \\|\\|e_A\\|\\|_B (C_flux \\|\\|S_EM dot n\\|\\|_B + B_corner_flux) + \\|\\|e_A\\| \| L46:\| JTC3245_1_zero_condition \| Poynting no-flux zero special case \| 3234 boundary silence audit \| J_A^Poynting=0 only if S_EM dot n=0 on parent-owned boundary/collar or flux is exact/proper and annihilated \| boundary frame | false |
| SRC3246_3234_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3234-Y5-R2FR-Poynting-boundary-flux-silence-or-finite-bound-under-AX1090.md | true | true | finite Poynting flux derivation | L12:Phi_Poynting[v_perp] \| L13::= int_B w_perp T_EM(u,n) dSigma \| L20:\|Phi_Poynting[v_perp]\| \| L22::= C_flux \|\|S_EM dot n\|\|_B + B_corner_flux. | false |
| SRC3246_3234_functional | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3234_POYNTING_FLUX_FUNCTIONAL.csv | true | true | machine Poynting functional rows | L2:PF3234_0_functional,Poynting boundary/collar/worldtube flux functional,"Phi_Poynting[v_perp] := int_B w_perp T_EM(u,n) dSigma ~= int_B w_perp (S_EM dot n) dSigma","transverse variation tests the EM stress/energy flux thr \| L3:PF3234_1_stress_form,stress tensor equivalent,"S_EM dot n = T_EM(u,n) after choosing observed frame u and boundary normal n",keeps the channel covariant; Poynting is the frame expression of the Maxwell stress flux,"obser \| L4:PF3234_2_collar_bulk,collar leakage source,"J_Poynting_bound <= C_coll \|\|T_EM(u,n)\|\|_collar","if flux is represented as a collar/worldtube source rather than a pure boundary term, it still enters only through a finite st \| L5:PF3234_3_F2_guard,F2 shortcut guard,"F_mu_nu F^mu_nu=0 does not imply T_EM(u,n)=0 or S_EM dot n=0",null radiation can have vanishing scalar invariant and nonzero energy flux,none; must separately prove stress/flux silenc | false |
| SRC3246_3234_bound | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3234_FINITE_FLUX_BOUND.csv | true | true | machine finite flux bound rows | L2:PB3234_0_boundary_flux,Phi_Poynting_bound,Phi_Poynting_bound := C_flux \|\|S_EM dot n\|\|_B + B_corner_flux,"C_flux; boundary/collar/worldtube B; observed u,n; flux norm; corner/worldtube remainder; units",FINITE_BOUND_FORMU \| L3:PB3234_1_collar_source,J_Poynting_bound,"J_Poynting_bound := C_coll \|\|T_EM(u,n)\|\|_collar",C_coll; collar support; stress-flux norm; projector norm; units,FINITE_BOUND_FORMULA_READY_INPUTS_MISSING,false,2026-06-26T22:50:5 \| L4:PB3234_2_total_phi,Phi_perp_bound update,\|Phi_perp^tau\| <= Phi_other_bound + Phi_EM_F2_boundary + C_flux \|\|S_EM dot n\|\|_B + B_corner_flux,Phi_other_bound; Phi_EM_F2_boundary; C_flux; flux norm; corner flux,FEEDS_LOCAL_RE \| L5:PB3234_3_total_jperp,J_perp_bound update,"\|\|J_perp^tau\|\|_2 <= J_other_bound + (1/4) C_F2_perp \|\|F^2\|\|_2 + C_coll \|\|T_EM(u,n)\|\|_collar",J_other_bound; C_F2_perp; F2 norm; C_coll; collar stress flux norm,FEEDS_TRANSVERSE_A | false |
| SRC3246_3200_schema | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3200_POYNTING_BOUND_RUNNER_SCHEMA.csv | true | true | older runner schema for Poynting residual rows | L1:bound_id,quantity,inequality,input_columns,output_column,claim_use,current_status,valid_for_claim,generated_utc \| L2:PBR3200_00,normal_Poynting_flux_density,\|n dot S\| <= \|E\| \|H\|,system_id;surface_id;E_bound;H_bound;normal_projection_bound;units;source_path;valid_for_claim,S_normal_bound,finite residual input only,schema_only_no_numeric \| L3:PBR3200_01,dimensionless_EM_flux_residual,B_EM <= \|tau_EM\| S_normal_bound / M_H_ref,tau_EM;S_normal_bound;M_H_ref;units;source_path;valid_for_claim,B_obs_EM_Poynting_over_MH_bound,local residual bound only after tau_EM a \| L4:PBR3200_02,quiet_zero_certificate,if H_radiative=0 and n dot(E x H_static)=0 then B_obs_EM_Poynting_over_MH=0 for the Poynting subchannel,system_id;surface_id;field_regime;H_radiative_zero_certificate;normal_cross_flux_z | false |
| SRC3246_3200_cases | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3200_POYNTING_ZERO_OR_BOUND_THEOREM.csv | true | true | quiet/static/radiative regime classifier | L1:case_id,local_regime,assumptions,standard_target_statement,MTS_status,J_EM_rank_contribution,important_caveat,valid_for_claim,generated_utc \| L2:PZT3200_00,quiet_static_no_radiation_no_magnetic_flux,observer split exists; fields stationary; H=0 or E cross H has zero normal projection; no radiation through local surface,"S = E x H gives n dot S = 0, so T_EM^{0i} c \| L4:PZT3200_02,static_crossed_fields_or_circulating_field_momentum,E cross H nonzero but controlled; normal projection may vanish by geometry or averaging,\|n dot S\| <= \|E\|\|H\| supplies a finite residual bound,finite_bound_rou \| L5:PZT3200_03,radiative_or_time_dependent_EM,radiation or time-dependent fields cross the local surface,Poynting flux is live and must be source-backed/bounded,residual_bound_required,not_claimed,using radiation flux to rep | false |
| SRC3246_3142_stress | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3142_POYNTING_STRESS_READOUT.csv | true | true | conditional EM stress and Poynting readout | L1:readout_id,object,formula,requires,status,valid_for_claim,generated_utc \| L3:EMS3142_1_stress,Hilbert EM stress tensor,T_EM^{mu nu}=Z_Q(F^{mu rho}F^nu_rho - 1/4 g_obs^{mu nu}F^2),same observed coframe and q-basic Z_Q,conditional_derived,false,2026-06-26T08:02:42.158025+00:00 \| L4:EMS3142_2_poynting,Poynting flux,S^i=-T_EM^i_0 in an observed tetrad; equivalent to observed E x H with the same Z_Q convention,observed tetrad e_obs and owned Maxwell stress,conditional_derived,false,2026-06-26T08:02:42 | false |
| SRC3246_3199_descent | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3199_POYNTING_MAXWELL_DESCENT_AUDIT.csv | true | true | Maxwell descent/open gate guard | L1:gate_id,gate,required_for,current_status,source_path,evidence,effect_on_3199,valid_for_claim,generated_utc \| L4:PMG3199_02,conserved_current_and_charge,source coupling tau_EM and Coulomb/radiation-pressure consistency,open,formalization-workbench/29-em-maxwell-gate-audit.md,audit lists Coulomb force and radiation pressure as faile \| L5:PMG3199_03,standard_or_parent_derived_T_EM,normal flux C^nu_EM = n_mu T_EM^{mu nu},partial_open,formalization-workbench/29-em-maxwell-gate-audit.md,energy diagnostics exist but are not yet Maxwell T_EM,"can define a sour | false |
| SRC3246_3222_guards | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3222_STRESS_POYNTING_AND_READOUT_GUARDS.csv | true | true | stress/readout guards | L2:SPG3222_0_null_wave_guard,null EM radiation,F_Q^2=0 while T_EM and Poynting vector can be nonzero,stress/Hodge/current residual R_T or finite T_EM projection bound,NOT_CLOSED,false,2026-06-26T21:41:11.234884+00:00 \| L4:SPG3222_2_current_normalization,source/current coupling,J_Q normalization can float even if Maxwell kinetic coefficient is locally stationary,same T_Q/Ward owner for kinetic coefficient and matter current,NOT_CLOSED,fals \| L5:SPG3222_3_local_GR_boundary,local GR/Newton/PPN transfer,"EM defect norm does not prove EH source normalization, Poisson-Gauss, or PPN values",separate local GR/Newton source-charge and PPN derivations,NO_TRANSFER_CLAIM, | false |
| SRC3246_3232_audit | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3232_POYNTING_FLUX_ZERO_OR_BOUND_AUDIT.csv | true | true | Poynting zero-or-bound audit | L2:PY3232_0_definition,Poynting/collar/worldtube flux,"Phi_Poynting <= C_flux \|\|S_EM . n\|\|_B, equivalently a stress flux norm built from T_EM^{mu nu} n_mu","no EM flux through boundary/collar/worldtube, or flux form is exac \| L3:PY3232_1_F2_nonimplication,F2 versus stress,F^2=0 does not imply T_EM^{mu nu}=0 or S_EM=0,must separately prove stress/flux silence,retain Poynting/stress norm even when scalar F2 channel is zero,SEPARATE_CHANNEL_GUARD,b \| L5:PY3232_3_no_flux_support,support silence,S_EM . n = 0 on the selected boundary/collar/worldtube,boundary chosen or derived so physical flux through it is zero,"if flux is nonzero, bound by measured/sourced field flux sup | false |

## Validation

| validation_id | passed | requirement | evidence |
| --- | --- | --- | --- |
| VAL3246_0_sources_exist | true | all cited source paths exist | True |
| VAL3246_1_source_hits | true | source evidence hits are present | True |
| VAL3246_2_csvs_parse | true | all generated CSV files parse | True |
| VAL3246_3_outputs_under_post_checkpoint | true | all outputs are under post-checkpoint-work | True |
| VAL3246_4_formalization_clean | true | no 3246 outputs in formalization-workbench | formalization_3246_count=0 |
| VAL3246_5_required_columns | true | score row has all required columns | True |
| VAL3246_6_missing_detected | true | score row exposes missing inputs | True |
| VAL3246_7_score_nonclaim | true | score row remains nonclaim | True |
| VAL3246_8_zero_not_claimed | true | Poynting zero not asserted | True |
| VAL3246_9_claims_blocked | true | all claim gates remain nonclaim | True |
| VAL3246_10_next_written | true | 3247 next target written | True |
| VAL3246_11_doc_written | true | 3246 markdown checkpoint exists | True |
| VAL3246_OVERALL | true | 3246 validation overall | all required validation rows passed |

## Generated Evidence

- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3246_SOURCE_REGISTER.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3246_FIRST_POYNTING_JTOT_SCORE_ROW_NONCLAIM.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3246_BOUNDARY_FRAME_FLUX_ACQUISITION_LEDGER.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3246_POYNTING_REGIME_ZERO_OR_BOUND_CLASSIFIER.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3246_SCORE_ROW_DRY_RUN.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3246_JTOT_AMPLITUDE_TRANSFER_UPDATE.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3246_CLAIM_GATES.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3246_DECISION_LEDGER.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3246_NEXT_TARGET.csv`
- `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3246_VALIDATION.csv`