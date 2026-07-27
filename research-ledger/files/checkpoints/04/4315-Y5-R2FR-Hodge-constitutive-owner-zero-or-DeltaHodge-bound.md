# 4315 - Hodge constitutive owner zero or DeltaHodge bound

## Verdict
- Derived the exact same-Hodge zero contract for `Delta_Hodge_EM`.
- Retained the constitutive countermodel: `chi_EM != chi(g_obs)` is a real residual, not killed by gauge covariance.
- Wrote the no-cancellation envelope for principal, skewon, axion-gradient, hidden-Hodge, readout-Hodge and orientation terms.
- Fed `Delta_Hodge_EM` into `R_EM_Poynting`, `Eta_H`, and `S_U`.
- Preserved the scale guard: no alpha, charge, source-mass or `G_N` derivation from Hodge closure.

## Source Register
| source_id | source_path | exists | needle_found | purpose |
| --- | --- | --- | --- | --- |
| SRC4315_00_4314_next | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4314_NEXT_TARGET.csv | True | True | 4314 handoff selecting Hodge/constitutive owner or Delta_Hodge_EM bound. |
| SRC4315_01_4314_status | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4314_STATUS.csv | True | True | 4314 status marks Delta_Hodge_EM as the next open EM gate. |
| SRC4315_02_4260_formal | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\276-PPC4161-Delta-Hodge-EM-closure-or-bound.md | True | True | 4260 Hodge uniqueness lemma and unsigned parent-action clauses. |
| SRC4315_03_4208_formal | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\224-PPC4161-Hodge-deformation-zero-or-constitutive-bound.md | True | True | 4208 constitutive countermodel and no-cancellation envelope. |
| SRC4315_04_4261_action_domain | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\277-PPC4161-visible-EM-action-domain-fork-or-constitutive-bound.md | True | True | 4261 signs the visible EM action domain only inside the calibrated branch. |
| SRC4315_05_4262_readout | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\278-PPC4161-visible-EM-readout-guard-or-charge-normalization-bound.md | True | True | 4262 readout-after-variation guard for calibrated visible branch. |
| SRC4315_06_3504_flow | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_EM_Hodge_flow_rule_bound_or_zero.csv | True | True | component-level Hodge flow rule bound/zero ledger. |
| SRC4315_07_3506_runner | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_EM_first_constitutive_bound_runner_results.csv | True | True | first constitutive bound runner showing missing coefficients/bounds. |
| SRC4315_08_4312_bound | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4312_COLLAR_EM_RESIDUAL_BOUND.csv | True | True | 4312 residual bound where Hodge defects feed R_EM_Poynting and Eta_H. |
| SRC4315_09_4314_flux | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\330-PPC4161-radiative-Poynting-no-flux-or-boundary-flux-row.md | True | True | 4314 radiative row separated from Hodge/constitutive defects. |
| SRC4315_10_precision | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\309-PPC4161-epsilon-mu-tr-shared-local-bound-runner-WEP-R10-PPN-clocks-orbital.md | True | True | local precision guard for Hodge/constitutive leakage. |
| SRC4315_11_newton_guard | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1714-Y5-R2FR-Y5-worldtube-Hilbert-source-equality-or-Req-Icommutator-fill.md | True | True | source-to-Newton equality gate remains open. |

## Same-Hodge Theorem
| theorem_id | clause | statement | result | status |
| --- | --- | --- | --- | --- |
| HT4315_0_unique_hodge | observed Hodge uniqueness | fixed e_obs, g_obs, orientation and volume determine *_obs by alpha wedge *_obs beta = <alpha,beta>_g_obs vol_obs | mathematical uniqueness lemma | EXACT_MATH_LEMMA |
| HT4315_1_same_action | same-Hodge Maxwell action | S_EM = -(4 mu0)^-1 int F wedge *_obs F with no independent chi_EM | Delta_Hodge_EM=0 inside the calibrated same-Hodge visible branch | EXACT_ZERO_IF_PARENT_BRANCH_SIGNED |
| HT4315_2_action_domain | visible action-domain branch | DeltaS_MTS_visible=0 before variation and S_Maxwell-Hodge uses g_obs and *_obs | visible EM action-domain contribution to Delta_Hodge_EM is zero only in this branch | CONDITIONAL_BRANCH_ZERO |
| HT4315_3_readout_guard | readout Hodge guard | readout is pure postprocessing with no argument slot in parent/effective action | C_Hodge_readout=0 only under readout-after-variation discipline | CONDITIONAL_BRANCH_ZERO |
| HT4315_4_countermodel | constitutive countermodel | S_EM = -1/4 int F_ab chi_EM^abcd F_cd vol_obs with chi_EM != chi(g_obs) | gauge covariance alone does not imply Delta_Hodge_EM=0 | COUNTERMODEL_RETAINED |
| HT4315_5_zero_contract | full Hodge zero contract | same Hodge action, no principal/skewon/axion-gradient/hidden/readout/orientation residuals | Delta_Hodge_EM=0 and Hodge term drops from R_EM_Poynting/Eta_H/S_U | EXACT_ZERO_IF_ALL_CLAUSES_SIGNED |

## Constitutive Residual Envelope
| residual_id | symbol | meaning | envelope_term | observable_links | status | next_action |
| --- | --- | --- | --- | --- | --- | --- |
| CR4315_0_Delta_chi_principal | Delta_chi_principal | principal constitutive tensor changes EM cone/anisotropy/birefringence | \|\|Delta_chi_principal\|\| | vacuum_birefringence; light_cone; Shapiro/lensing consistency | EXPLICIT_BOUND_ROW_VALUE_MISSING | parent-sign zero or fill sourced coefficient and observational bound |
| CR4315_1_Delta_chi_skewon | Delta_chi_skewon | skewon/nonreciprocal/dissipative constitutive piece | \|\|Delta_chi_skewon\|\| | polarization; dispersion; Poynting flux nonconservation | EXPLICIT_BOUND_ROW_VALUE_MISSING | parent-sign zero or fill sourced coefficient and observational bound |
| CR4315_2_dtheta_EM | dtheta_EM | active axion-gradient or pseudoscalar bulk response | L\|\|d theta_EM\|\| | polarization rotation; parity-odd EM propagation | EXPLICIT_BOUND_ROW_VALUE_MISSING | parent-sign zero or fill sourced coefficient and observational bound |
| CR4315_3_C_Hodge_hidden | C_Hodge_hidden | hidden/motion/time field defines a disformal or medium-like EM Hodge star | \|C_Hodge_hidden\| | preferred frame; light-speed anisotropy; clock | EXPLICIT_BOUND_ROW_VALUE_MISSING | parent-sign zero or fill sourced coefficient and observational bound |
| CR4315_4_C_Hodge_readout | C_Hodge_readout | post-solution readout/clock/spectroscopy map regenerates Hodge or alpha response | \|C_Hodge_readout\| | clock; spectroscopy; alpha_EM; binding response | EXPLICIT_BOUND_ROW_VALUE_MISSING | parent-sign zero or fill sourced coefficient and observational bound |
| CR4315_5_Delta_orientation_flux | Delta_orientation_flux | orientation/time-orientation or boundary normal differs between EM and source charge | \|Delta_orientation_flux\| | Poynting sign; boundary source orientation | EXPLICIT_BOUND_ROW_VALUE_MISSING | parent-sign zero or fill sourced coefficient and observational bound |

## Bound Update
| bound_id | symbol | law | role | status | next_action |
| --- | --- | --- | --- | --- | --- |
| HB4315_0_envelope | Delta_Hodge_EM | \|\|Delta_Hodge_EM\|\| <= \|\|Delta_chi_principal\|\| + \|\|Delta_chi_skewon\|\| + L\|\|dtheta_EM\|\| + \|C_Hodge_hidden\| + \|C_Hodge_readout\| + \|Delta_orientation_flux\| | no-cancellation constitutive envelope | BOUND_DERIVED_VALUES_MISSING | prove same-Hodge zero or source every term in the no-cancellation envelope |
| HB4315_1_zero | Delta_Hodge_EM_zero | all constitutive residual components zero in same-Hodge parent-visible branch | Delta_Hodge_EM=0 | CONDITIONAL_ZERO_NOT_GLOBAL | prove same-Hodge zero or source every term in the no-cancellation envelope |
| HB4315_2_R_EM_update | R_EM_Poynting | R_EM_Poynting <= R_EM_noHodge + C_H \|\|Delta_Hodge_EM\|\| \|\|F\|\|^2 | 4312 EM residual with Hodge mismatch explicit | FORMULA_READY_VALUES_MISSING | prove same-Hodge zero or source every term in the no-cancellation envelope |
| HB4315_3_EtaH_update | Eta_H | Eta_H >= Eta_H_noHodge + C_Eta_Hodge \|\|Delta_Hodge_EM\|\| \|\|F\|\|^2 | lambda-floor correction if Hodge mismatch survives | FORMULA_READY_VALUES_MISSING | prove same-Hodge zero or source every term in the no-cancellation envelope |
| HB4315_4_SU_update | S_U | S_U <= S_U_noHodge + N_Hodge_EM | collar residual numerator receives constitutive mismatch as named term | FORMULA_READY_VALUES_MISSING | prove same-Hodge zero or source every term in the no-cancellation envelope |

## Scale Guard
| guard_id | item | rule | implication | status |
| --- | --- | --- | --- | --- |
| SG4315_0_alpha | alpha_EM | not derived by Hodge matching | requires Maxwell normalization/current-scale gate | ACTIVE |
| SG4315_1_mu0 | mu0/Z_Q | not derived by two-form Hodge uniqueness | requires EM normalization/action-scale input | ACTIVE |
| SG4315_2_charge | charge normalization | not derived by constitutive cone matching | requires current lattice/source normalization | ACTIVE |
| SG4315_3_GN | G_N/source mass | not derived by EM Hodge closure | requires Hilbert/Newton source calibration | ACTIVE |
| SG4315_4_conformal | conformal scale | two-form Hodge star in 4D is conformally invariant | prevents smuggling scale constants into Hodge theorem | ACTIVE |

## Runner
| runner_id | case | result | reason | next_action |
| --- | --- | --- | --- | --- |
| RUN4315_0_current_corpus | current corpus | CONDITIONAL_ZERO_OR_BOUND | same-Hodge zero branch exists for calibrated visible branch; global MTS EM constitutive ownership remains unproved | keep Delta_Hodge_EM zero only branch-local and retain bound rows |
| RUN4315_1_same_hodge | same observed Hodge owner with no independent constitutive terms | ALLOW_DELTA_HODGE_ZERO_CONDITIONAL | Delta_Hodge_EM drops from R_EM_Poynting, Eta_H and S_U | still requires lambda/source-equality/non-EM residual gates |
| RUN4315_2_constitutive_deformation | principal/skewon/axion/hidden/readout/orientation residual survives | KEEP_CONSTITUTIVE_BOUND | Hodge mismatch enters local precision via explicit no-cancellation envelope | source coefficients and bounds before scoring local arenas |
| RUN4315_3_scale_claim | derive alpha_EM, G_N or source mass from Hodge closure | REJECT | four-dimensional two-form Hodge closure does not fix coupling scale | route scale constants to separate normalization gates |
| RUN4315_4_local_claim | claim local GR/Newton/R10/PPN now | REJECT | lambda components, non-EM residuals, source equality, I_commutator and projection gates remain open | continue derivation chain |

## Claim Firewall
| firewall_id | rule | status |
| --- | --- | --- |
| FW4315_0 | Do not claim Delta_Hodge_EM=0 from Hodge uniqueness unless the parent EM action uses the observed Hodge star only. | ACTIVE |
| FW4315_1 | Do not cancel principal, skewon, axion-gradient, hidden-Hodge and readout-Hodge terms against each other. | ACTIVE |
| FW4315_2 | Do not derive alpha_EM, mu0, charge normalization, source mass or G_N from Hodge closure. | ACTIVE |
| FW4315_3 | Do not treat the calibrated visible EM branch as global MTS electromagnetism. | ACTIVE |
| FW4315_4 | Do not claim local GR/Newton/R10/PPN from the Hodge gate alone. | ACTIVE |

## Decision
| decision_id | result | reason | next_action |
| --- | --- | --- | --- |
| DEC4315_0_zero | SAME_HODGE_ZERO_ROUTE_IS_CLEAN | Observed Hodge uniqueness plus same-Hodge Maxwell action can set Delta_Hodge_EM=0 in the calibrated branch. | use only inside the branch with all constitutive counterterms forbidden |
| DEC4315_1_bound | CONSTITUTIVE_COUNTERMODEL_RETAINED | Gauge covariance does not forbid chi_EM != chi(g_obs); the no-cancellation envelope is required. | feed Delta_Hodge_EM into R_EM_Poynting, Eta_H and S_U if any term survives |
| DEC4315_2_scale | HODGE_MATCHING_IS_NOT_SCALE_DERIVATION | Two-form Hodge closure does not derive alpha_EM, charge scale, G_N or source mass. | keep normalization/source calibration gates separate |
| DEC4315_3_frontier | VISIBLE_HILBERT_SOURCE_SILENCE_INTEGRATION_NEXT | EM residuals are now mostly zero-or-bound; next useful step is integrating visible Hilbert silence with remaining non-EM residual budget. | 4316-Y5-R2FR-visible-Hilbert-source-silence-integration-or-nonEM-residual-budget.md |
| DEC4315_4_claim | NO_LOCAL_CLAIM | 4315 improves the EM source-coupling ladder but does not complete the local GR/Newton route. | keep all claim flags false |

## Status
| status_id | item | status | note |
| --- | --- | --- | --- |
| STAT4315_0_math | Hodge uniqueness | EXACT_MATH | fixed observed metric/coframe/orientation determines *_obs |
| STAT4315_1_zero | Delta_Hodge_EM | ZERO_OR_BOUND | zero only in same-Hodge calibrated branch |
| STAT4315_2_envelope | constitutive envelope | EXPLICIT | principal/skewon/axion/hidden/readout/orientation rows named |
| STAT4315_3_scale | alpha/G/source scale | SEPARATE_GATE | not derived here |
| STAT4315_4_next | visible Hilbert silence | NEXT_OPEN_GATE | integrate EM zero-or-bound with non-EM residual budget |
| STAT4315_5_local | local GR/Newton | BLOCKED | source coupling sharper, full reduction still open |

## Next Target
| next_target_id | next_target | target_question | preferred_route | fallback_route |
| --- | --- | --- | --- | --- |
| NT4315_0 | 4316-Y5-R2FR-visible-Hilbert-source-silence-integration-or-nonEM-residual-budget.md | Can visible Hilbert source silence be integrated with the EM zero-or-bound ledger to produce a reduced non-EM residual budget? | combine same-Hodge/current/radiative zero branches with 4303 visible Hilbert source silence | stage the remaining non-EM residual budget rows feeding S_U, Eta_H and the lambda-floor test |
