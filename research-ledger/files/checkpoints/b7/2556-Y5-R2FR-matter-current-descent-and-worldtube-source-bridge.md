# 2556 Y5 R2FR Matter-current Descent And Worldtube Source Bridge

**Result:** source bridge sharpened, not closed. The best route is not an arbitrary vertical charge and definitely not fitted orbital GM. The least-circular current is a Hilbert/energy current, `J_M^nu = ell_J T_matter^{nu rho} tau_rho`, because it uses the same stress-energy object that GR already treats as source.

**Important shift:** this makes the Newton-source problem more concrete. Instead of asking for a mysterious `J_M`, the contract is now: derive/fix `ell_J`, prove the clock-compatible conservation identity, and make the worldtube integral surface-independent. If those close, `q_loc=P_loc J_M` has a real shot at giving source-free local vacuum outside matter without a plateau axiom.

## Source Register
| source_id | source_path | exists | missing_needles | source_pass | role |
| --- | --- | --- | --- | --- | --- |
| SRC2556_00_2555_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\2555-Y5-R2FR-vertical-generator-current-law-variation-and-source-audit.md | true |  | true | active handoff selecting source-current descent |
| SRC2556_01_2555_source_descent | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_NO_SHADOW_2555_SOURCE_CURRENT_DESCENT.csv | true |  | true | machine-readable source-current missing clauses |
| SRC2556_02_2555_dimension | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_NO_SHADOW_2555_DIMENSION_AUDIT.csv | true |  | true | dimension branch and parent-scale warning |
| SRC2556_03_2555_stress | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_NO_SHADOW_2555_STRESS_TENSOR_EXPOSURE.csv | true |  | true | stress/WEP local-GR blockers |
| SRC2556_04_2554_candidate | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_NO_SHADOW_2554_CANDIDATE_ACTIONS.csv | true |  | true | parent action needing J_M source bridge |
| SRC2556_05_symbol_map | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_MTS_SYMBOL_TO_LOCAL_GR_ACTION_MAP.csv | true |  | true | local-GR source/action placement warning |

## Current Candidates
| candidate_id | candidate_name | candidate_law | definition | strength | status | main_risk |
| --- | --- | --- | --- | --- | --- | --- |
| CUR2556_A_Hilbert_energy_current | Hilbert/energy current | J_M^nu = ell_J T_matter^{nu rho} tau_rho | T_matter from metric variation; tau is local clock/coframe direction; ell_J supplies one inverse mass scale | best universality route because all matter couples through stress-energy | SELECTED_PRIMARY_CONTRACT | needs parent scale ell_J, clock compatibility, and conservation identity |
| CUR2556_B_vertical_Noether_current | vertical Noether current | J_M^nu = c_A pi_Psi^nu R_M Psi | matter has vertical generator R_M and A_mu enters D_mu^A Psi=D_mu Psi+A_mu R_M Psi | directly matches vertical-generator language | SECONDARY_CANDIDATE | risks species-dependent charge and WEP failure unless R_M is universal/geometric |
| CUR2556_C_rest_mass_current | rest-mass/baryonic current | J_M^nu proportional to rho_0 u^nu | phenomenological matter current | useful for smoke tests only | DEMOTE_TO_PHENOMENOLOGY | not fundamental enough for GR reduction and likely fails pressure/radiation regimes |
| CUR2556_D_orbital_GM_current | fitted orbital GM current | J_M chosen so worldtube integral equals observed GM | post-readout fitted source | would make Newton limit circular | REJECTED | forbidden shortcut |

## Hilbert Current Descent
| hilbert_id | clause | basis | result | status |
| --- | --- | --- | --- | --- |
| HIL2556_0_define_T | T_matter^{mu nu}:=-(2/sqrt(-g)) delta S_matter/delta g_mu_nu | standard Hilbert stress from matter action | universal source object exists if matter action is metric-coupled | PASS_AS_CONTRACT |
| HIL2556_1_define_current | J_M^nu:=ell_J T_matter^{nu rho} tau_rho | clock/coframe tau selects local energy current; ell_J fixes dimension to M^3 branch | matches 2555 viable branch with [A]=M and [Gamma_eff]=M^2 | PASS_AS_CANDIDATE_CONTRACT |
| HIL2556_2_parent_scale | ell_J must be parent-derived and fixed before tests | otherwise J_M normalization becomes a hidden fitted mass scale | source bridge remains nonclaim until ell_J source exists | MISSING_PARENT_SCALE |
| HIL2556_3_clock_compatibility | tau_rho must be parent-owned and locally compatible with conservation | nabla_nu(T^{nu rho} tau_rho)=T^{nu rho} nabla_nu tau_rho on matter shell | exact conservation needs tau Killing/covariantly constant locally or a controlled exchange term | MISSING_CLOCK_CONSERVATION_CLAUSE |
| HIL2556_4_matter_A_coupling | If A also couples directly to matter, its source must reduce to the Hilbert current branch or be demoted. | prevents double-counting Hilbert and vertical charge currents | A_nu J_M^nu should be universal source coupling, not species charge tuning | MISSING_UNIFICATION_OF_COUPLINGS |

## Conservation Audit
| conservation_id | statement | basis | result | status |
| --- | --- | --- | --- | --- |
| CON2556_0_matter_shell | If matter equations and diffeomorphism invariance give nabla_mu T^{mu nu}=0, then divergence of J_M is ell_J T^{mu nu} nabla_mu tau_nu plus scale-gradient terms. | Hilbert current branch | conserved only under clock compatibility or controlled exchange | CONDITIONAL_NOT_CLOSED |
| CON2556_1_local_inertial_limit | In a local inertial vacuum collar with tau approximately covariantly constant and no matter support, J_M=0 and nabla.J_M=0. | local lab/PPN collar approximation | supports conditional q_loc zero exterior | PASS_AS_LOCAL_LIMIT_CONTRACT |
| CON2556_2_exact_identity_needed | Exact local-GR theorem needs an identity: nabla_mu J_M^mu + I_GK = 0, with I_GK supplied by Gamma/Khat/tau equations if tau is not Killing. | integrability of A equation | exchange term must be parent-derived, not added by hand | MISSING_EXACT_IDENTITY |
| CON2556_3_Noether_alternative | Vertical Noether current can be exactly conserved if R_M is a genuine symmetry and A/Gamma sector has compatible transformation. | secondary branch | possible but WEP/composition risk is higher than Hilbert branch | CANDIDATE_ONLY |
| CON2556_4_distributional_source | Worldtube boundary requires distributional conservation including surface layer flux. | compact source with boundary | needed before deriving Newton source mass | MISSING_JUMP_IDENTITY |

## Worldtube Bridge
| worldtube_id | clause | role | condition | status |
| --- | --- | --- | --- | --- |
| WT2556_0_charge_integral | Q_M[W,Sigma]:=int_{Sigma cap W} J_M^mu dSigma_mu | source charge from current flux through parent-defined hypersurface | valid only if J_M is conserved including boundary layers | CONDITIONAL_CONTRACT |
| WT2556_1_mass_readout | M_source[W]:=Q_M/ell_J for Hilbert branch, equivalently int T^{mu nu} tau_nu dSigma_mu | mass/energy source readout before orbital fitting | requires ell_J fixed by parent convention and tau normalized | CONDITIONAL_CONTRACT |
| WT2556_2_surface_independence | Q_M[Sigma_1]=Q_M[Sigma_2] if nabla_mu J_M^mu=0 and no flux leaks through side boundary | Gauss law | not proved until conservation/jump conditions close | MISSING_CONSERVATION_PROOF |
| WT2556_3_external_vacuum | Outside W, J_M=0 so q_loc=P_loc J_M=0 up to bounded boundary tails | local vacuum law | requires compact support/falloff theorem | MISSING_SUPPORT_THEOREM |
| WT2556_4_no_orbital_GM | Do not define M_source by observed GM or fitted orbital acceleration. | anti-circularity guardrail | passes as explicit forbidden route | PASS_GUARDRAIL |

## WEP And Composition Guardrail
| wep_id | statement | status | required_fix |
| --- | --- | --- | --- |
| WEP2556_0_hilbert_universal | Hilbert current branch is naturally universal because all matter contributes through T_matter. | SUPPORTS_WEP_ROUTE | still needs proof that A coupling does not add species charge |
| WEP2556_1_noether_species_risk | Vertical Noether branch may couple differently to different matter fields. | RISK_OPEN | requires universal R_M or geometric descent |
| WEP2556_2_pressure_radiation | Newton source cannot be only baryonic rest mass; relativistic pressure/radiation regimes must be handled. | HILBERT_BRANCH_PREFERRED | T_matter route is safer than rho_0 u^mu route |
| WEP2556_3_composition_bound | Any residual species-dependent component must be zero or bounded before WEP/PPN claims. | BLOCKS_CLAIM | future local tests need eta/WEP projection if branch survives |
| WEP2556_4_coupling_unification | A_nu J_M^nu should be the same source object that appears in metric stress equations. | REQUIRED | prevents duplicate source definitions |

## External Vacuum Support
| vacuum_id | condition | effect | status |
| --- | --- | --- | --- |
| VAC2556_0_exact_vacuum | If T_matter=0 outside W and tau is regular, then Hilbert J_M=0 outside W. | q_loc=P_loc J_M gives local vacuum zero in source-free exterior | CONDITIONAL |
| VAC2556_1_tail_bound | If matter has tails, require \|\|J_M\|\|_collar <= epsilon_J and boundary flux <= epsilon_B. | Delta m/m bound inherits epsilon_J+epsilon_B | BOUND_FORM_ONLY |
| VAC2556_2_clock_leak | If tau varies across collar, conservation leaks through T^{mu nu} nabla_mu tau_nu. | clock compatibility needed for exact source silence | MISSING_CLOCK_BOUND |
| VAC2556_3_surface_layer | Distributional worldtube surface terms must be included in J_M or boundary flux ledger. | prevents hiding source at boundary | MISSING_JUMP_LEDGER |

## Promotion Verdict
| verdict_id | question | result | evidence | effect |
| --- | --- | --- | --- | --- |
| PV2556_0_best_current | Which source current route is best? | HILBERT_ENERGY_CURRENT | universal stress-energy source is least circular and most GR-compatible | select for next derivation |
| PV2556_1_source_bridge | Is J_M fully derived? | NO | ell_J, tau conservation, exact identity and worldtube jump conditions are missing | source bridge remains nonclaim |
| PV2556_2_Newton_source | Is Newton source mass derived? | NO_BUT_CONTRACT_WRITTEN | M_source=int T tau dSigma is the right-looking target but not yet parent-closed | no Newton claim |
| PV2556_3_WEP | Does source branch avoid WEP risk? | PARTIALLY | Hilbert route is universal, but A coupling and any Noether supplement must not add composition charge | WEP gate remains blocked |
| PV2556_4_overall | Overall 2556 verdict | SOURCE_BRIDGE_SHARPENED_NOT_CLOSED | best source route identified; theorem blocked by scale, clock conservation and worldtube support | next target is exact conservation/scale gate |

## Claim Gates
| gate_id | claim | gate_status | reason | gate_pass | claim_allowed |
| --- | --- | --- | --- | --- | --- |
| GATE2556_0_hilbert_route | Hilbert current is selected as best source-current route. | PASS_AS_CONTRACT | least circular and most universal | true | false |
| GATE2556_1_parent_scale | ell_J is parent-derived. | BLOCKED | no source for parent scale yet | false | false |
| GATE2556_2_conservation | J_M conservation identity is exact. | BLOCKED | tau compatibility/exchange identity missing | false | false |
| GATE2556_3_worldtube | worldtube source mass is parent-derived and surface-independent. | BLOCKED | jump/support conditions missing | false | false |
| GATE2556_4_WEP_PPN | WEP/PPN safe source coupling is proven. | BLOCKED | composition guardrail not closed | false | false |
| GATE2556_5_local_GR_Newton | local GR/Newton branch passes. | BLOCKED | source bridge not closed and stress gate still open | false | false |
| GATE2556_6_no_GitHub | No public/GitHub update. | PASS_GUARDRAIL | private derivation checkpoint only | true | false |

## Decision Ledger
| decision_id | decision | reason | effect |
| --- | --- | --- | --- |
| DEC2556_0_select_hilbert | Select Hilbert/energy current as primary source bridge. | it best matches GR source structure and avoids species tuning | use J_M=ell_J T_matter tau as working contract |
| DEC2556_1_demote_orbital_GM | Reject fitted orbital GM source definition. | would make Newton limit circular | keeps derivation honest |
| DEC2556_2_keep_noether_secondary | Keep vertical Noether current only as secondary route. | it may map to vertical-generator intuition but has WEP risk | do not use as primary local-GR source |
| DEC2556_3_next_conservation_scale | Next derive clock-compatible conservation and parent scale. | Hilbert branch cannot close without ell_J and nabla.J identity | 2557 target selected |
| DEC2556_4_no_claim | No local-GR/Newton claim. | source bridge sharpened but not closed | private nonclaim status retained |

## Next Target
| route_id | selection_status | target_file | target_script | task | acceptance_target | guardrails |
| --- | --- | --- | --- | --- | --- | --- |
| NEXT2556_0_selected | selected | 2557-Y5-R2FR-Hilbert-current-conservation-scale-and-clock-compatibility-gate.md | scripts/Y5_R2FR_Hilbert_current_conservation_scale_and_clock_compatibility_gate_2557.py | derive or reject the exact conservation identity for J_M=ell_J T_matter tau, identify the parent scale ell_J, and decide whether the Hilbert source bridge can close | clock compatibility equation, parent scale options, exchange-current identity, worldtube surface-independence gate, and demotion if ell_J is only fitted | no local-GR claim; no fitted GM; no M_H_ref reuse; no plateau axiom; no GitHub |

## Branch Copies
| copy_id | source_path | target_path | source_exists | target_exists |
| --- | --- | --- | --- | --- |
| hilbert_current_contract | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_NO_SHADOW_2556_HILBERT_CURRENT_DESCENT.csv | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\rab-sector\acquisition-queue\JR2556_HILBERT_CURRENT_SOURCE_BRIDGE_CONTRACT_NONCLAIM.csv | true | true |
| worldtube_contract | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_NO_SHADOW_2556_WORLDTUBE_BRIDGE.csv | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\local_bounds\Worldtube_source_bridge_2556_NONCLAIM.csv | true | true |

## Validation
| check_id | status | notes | detail |
| --- | --- | --- | --- |
| VAL2556_00_sources_exist | PASS | all cited source paths exist and needles are present |  |
| VAL2556_01_hilbert_selected | PASS | Hilbert current selected as primary contract |  |
| VAL2556_02_hilbert_contract | PASS | Hilbert source current contract written |  |
| VAL2556_03_scale_missing | PASS | parent scale blocker retained |  |
| VAL2556_04_conservation_not_closed | PASS | exact conservation blocker retained |  |
| VAL2556_05_worldtube_guardrail | PASS | orbital-GM source definition rejected |  |
| VAL2556_06_wep_guardrail | PASS | WEP/composition gate blocks claim |  |
| VAL2556_07_vacuum_conditional | PASS | external vacuum condition recorded as conditional |  |
| VAL2556_08_overall_nonclaim | PASS | overall source bridge verdict is nonclaim |  |
| VAL2556_09_claim_gates_safe | PASS | no claim gate allows local-GR/Newton claim |  |
| VAL2556_10_next_target_written | PASS | 2557 conservation/scale gate selected |  |
| VAL2556_11_branch_copies | PASS | nonclaim branch copies exist |  |
| VAL2556_12_no_formalization_artifacts | PASS | no 2556 artifacts were written to formalization-workbench |  |
| VAL2556_13_all_outputs_inside_post_checkpoint | PASS | all 2556 outputs stay inside post-checkpoint-work |  |
| VAL2556_14_pycache_absent | PASS | scripts __pycache__ absent after cleanup |  |
| VAL2556_CSV_P8_Y5_NO_SHADOW_2556_SOURCE_REGISTER | PASS | CSV parses with 6 rows | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_NO_SHADOW_2556_SOURCE_REGISTER.csv |
| VAL2556_CSV_P8_Y5_NO_SHADOW_2556_CURRENT_CANDIDATES | PASS | CSV parses with 4 rows | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_NO_SHADOW_2556_CURRENT_CANDIDATES.csv |
| VAL2556_CSV_P8_Y5_NO_SHADOW_2556_HILBERT_CURRENT_DESCENT | PASS | CSV parses with 5 rows | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_NO_SHADOW_2556_HILBERT_CURRENT_DESCENT.csv |
| VAL2556_CSV_P8_Y5_NO_SHADOW_2556_CONSERVATION_AUDIT | PASS | CSV parses with 5 rows | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_NO_SHADOW_2556_CONSERVATION_AUDIT.csv |
| VAL2556_CSV_P8_Y5_NO_SHADOW_2556_WORLDTUBE_BRIDGE | PASS | CSV parses with 5 rows | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_NO_SHADOW_2556_WORLDTUBE_BRIDGE.csv |
| VAL2556_CSV_P8_Y5_NO_SHADOW_2556_WEP_COMPOSITION_GUARDRAIL | PASS | CSV parses with 5 rows | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_NO_SHADOW_2556_WEP_COMPOSITION_GUARDRAIL.csv |
| VAL2556_CSV_P8_Y5_NO_SHADOW_2556_EXTERNAL_VACUUM_SUPPORT | PASS | CSV parses with 4 rows | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_NO_SHADOW_2556_EXTERNAL_VACUUM_SUPPORT.csv |
| VAL2556_CSV_P8_Y5_NO_SHADOW_2556_PROMOTION_VERDICT | PASS | CSV parses with 5 rows | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_NO_SHADOW_2556_PROMOTION_VERDICT.csv |
| VAL2556_CSV_P8_Y5_NO_SHADOW_2556_CLAIM_GATES | PASS | CSV parses with 7 rows | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_NO_SHADOW_2556_CLAIM_GATES.csv |
| VAL2556_CSV_P8_Y5_NO_SHADOW_2556_DECISION_LEDGER | PASS | CSV parses with 5 rows | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_NO_SHADOW_2556_DECISION_LEDGER.csv |
| VAL2556_CSV_P8_Y5_NO_SHADOW_2556_NEXT_TARGET | PASS | CSV parses with 1 rows | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_NO_SHADOW_2556_NEXT_TARGET.csv |
| VAL2556_CSV_P8_Y5_NO_SHADOW_2556_BRANCH_COPIES | PASS | CSV parses with 2 rows | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_NO_SHADOW_2556_BRANCH_COPIES.csv |
| VAL2556_COPY_CSV_hilbert_current_contract | PASS | copy CSV parses with 5 rows | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\rab-sector\acquisition-queue\JR2556_HILBERT_CURRENT_SOURCE_BRIDGE_CONTRACT_NONCLAIM.csv |
| VAL2556_COPY_CSV_worldtube_contract | PASS | copy CSV parses with 5 rows | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\local_bounds\Worldtube_source_bridge_2556_NONCLAIM.csv |
| VAL2556_OVERALL | PASS | 2556 selects a Hilbert-current source bridge but blocks theorem claims on parent scale, conservation and worldtube support |  |
