# 2557 Y5 R2FR Hilbert-current Conservation Scale And Clock Compatibility Gate

**Status:** derivation sharpened, theorem not promoted. The exact divergence of `J_M^mu=ell_J T_matter^{mu nu}tau_nu` is now explicit: it is controlled by parent-scale gradients, matter stress conservation, and symmetric clock strain. A stationary/Killing local collar can close conditionally, but the generic dynamic branch still needs a parent-derived exchange current.

**Main result:** the Hilbert route survives, but only honestly. The stationary compact-source route is a real theorem target; the full dynamic MTS/time route is blocked until `I_GK` and `ell_J` come from the parent action rather than being patched in. No Newton, local-GR, PPN, WEP, or R10 pass is claimed here.

## Source Register

| source_id | source_path | exists | missing_needles | source_pass | role |
| --- | --- | --- | --- | --- | --- |
| SRC2557_00_2556_doc | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\2556-Y5-R2FR-matter-current-descent-and-worldtube-source-bridge.md | true |  | true | active handoff selecting exact Hilbert-current conservation and scale gate |
| SRC2557_01_2556_hilbert_descent | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_NO_SHADOW_2556_HILBERT_CURRENT_DESCENT.csv | true |  | true | machine-readable Hilbert current and parent-scale blocker |
| SRC2557_02_2556_conservation | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_NO_SHADOW_2556_CONSERVATION_AUDIT.csv | true |  | true | machine-readable conservation identity gap |
| SRC2557_03_2556_worldtube | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_NO_SHADOW_2556_WORLDTUBE_BRIDGE.csv | true |  | true | worldtube surface-independence and anti-circularity guardrail |
| SRC2557_04_2556_wep | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_NO_SHADOW_2556_WEP_COMPOSITION_GUARDRAIL.csv | true |  | true | universality support and residual composition blocker |
| SRC2557_05_2556_vacuum | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_NO_SHADOW_2556_EXTERNAL_VACUUM_SUPPORT.csv | true |  | true | external vacuum conditional and clock-leak blocker |
| SRC2557_06_2467_precedent | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\2467-Y5-R2FR-Hilbert-current-conservation-scale-and-clock-compatibility-gate.md | true |  | true | earlier same-gate derivation precedent, now re-run against sharper 2556 bridge |

## Divergence Identity

| divergence_id | identity_or_condition | basis | result | status |
| --- | --- | --- | --- | --- |
| DIV2557_0_define_current | J_M^mu := ell_J T_matter^{mu nu} tau_nu | 2556 Hilbert-current source bridge | source current is universal if matter action is metric-coupled and tau is parent-owned | PASS_AS_INPUT |
| DIV2557_1_full_product_rule | nabla_mu J_M^mu = (nabla_mu ell_J) T^{mu nu} tau_nu + ell_J (nabla_mu T^{mu nu}) tau_nu + ell_J T^{mu nu} nabla_mu tau_nu | Leibniz rule for a scalar ell_J, symmetric Hilbert stress, and clock one-form tau | exact algebraic identity before using matter equations | PASS_DERIVED |
| DIV2557_2_matter_shell_constant_scale | if nabla_mu T^{mu nu}=0 and nabla_mu ell_J=0, then nabla_mu J_M^mu = ell_J T^{mu nu} nabla_mu tau_nu | matter equations plus fixed parent scale | clock strain is the only remaining leakage | PASS_DERIVED_CONDITIONAL |
| DIV2557_3_symmetric_clock_strain | for symmetric T, T^{mu nu} nabla_mu tau_nu = T^{mu nu} nabla_(mu tau_nu) | Hilbert stress symmetry | antisymmetric clock vorticity cannot source the divergence | PASS_DERIVED |
| DIV2557_4_Killing_or_covariantly_constant_clock | if nabla_(mu tau_nu)=0 in the collar, nabla_mu J_M^mu=0 on shell with fixed ell_J | stationary local clock condition | stationary compact-source route can close conditionally | CONDITIONAL_CLOSES |
| DIV2557_5_generic_clock_obstruction | for generic tau, nabla_mu J_M^mu is nonzero unless a parent exchange term cancels the clock-strain leak | dynamic MTS/time sector | Hilbert current alone does not prove exact conservation | BLOCKED_CURRENT_THEOREM |
| DIV2557_6_variable_scale_obstruction | if nabla_mu ell_J != 0, the term (nabla_mu ell_J)T^{mu nu}tau_nu is an extra source leak | scale as field or local fitted normalisation | ell_J must be parent-fixed, constant in the local collar, or supplied with its own exchange identity | BLOCKED_IF_SCALE_FLOATS |

## Clock Compatibility Gate

| clock_id | gate | condition | effect | status |
| --- | --- | --- | --- | --- |
| CLK2557_0_stationary_gate | stationary/Killing collar | nabla_(mu tau_nu)=0 across the local source collar | kills the Hilbert-current leakage term exactly on matter shell | CONDITIONAL_PASS |
| CLK2557_1_local_inertial_point_gate | pointwise local inertial frame | nabla_(mu tau_nu)=0 only at one event or to finite-order approximation | good for local expansion bookkeeping, not enough for finite worldtube conservation | APPROXIMATION_NOT_THEOREM |
| CLK2557_2_dynamic_clock_gate | generic evolving MTS clock | nabla_(mu tau_nu) generally nonzero | requires parent-derived exchange current or a dynamical clock equation with signed cancellation | BLOCKED |
| CLK2557_3_FLRW_split | cosmology/time activation | cosmological memory may deliberately have nonzero clock strain | local GR route must split local stationary collars from cosmological activation | REQUIRED_SPLIT |
| CLK2557_4_parent_clock_origin | tau parent-owned | tau must descend from the parent action/coframe rather than be chosen to fit a source | clock compatibility cannot be imposed as an after-the-fact gauge patch | MISSING_PARENT_CLOCK_EQUATION |
| CLK2557_5_clock_leak_bound | finite local bound | epsilon_tau(W)=int_W \|ell_J T^{mu nu}nabla_(mu tau_nu)\| dV | if exact closure fails, this becomes the residual PPN/local-GR bound to source | BOUND_FORM_ONLY |

## Parent Scale Options

| scale_id | scale_clause | reason | status |
| --- | --- | --- | --- |
| SCL2557_0_dimension | [ell_J]=M^-1=L if [J_M]=M^3, [T]=M^4, and tau is dimensionless | fits the 2555 viable branch where A has mass dimension one and Gamma_eff has mass dimension two | PASS_DERIVED_DIMENSION |
| SCL2557_1_parent_length_candidate | ell_J could be a universal parent length ell_* | acceptable only if fixed by the parent action before any local/cosmology fits | CANDIDATE_ONLY |
| SCL2557_2_gap_candidate | ell_J could be inverse parent gap 1/m_* | acceptable only if m_* is an independently derived spectrum/action scale | CANDIDATE_ONLY |
| SCL2557_3_clock_normalisation_candidate | ell_J could be absorbed into parent normalisation of tau | acceptable only if tau normalisation is universal and not source-fitted | CANDIDATE_ONLY |
| SCL2557_4_forbidden_fit | ell_J cannot be chosen from observed GM, orbital acceleration, H0 pressure, or M_H_ref denominator reuse | would make the Newton/local-GR bridge circular | REJECTED_GUARDRAIL |
| SCL2557_5_current_status | current corpus has no signed parent derivation of ell_J | source-current normalisation remains blocked for theorem claims | MISSING_PARENT_SCALE |
| SCL2557_6_variable_scale_warning | if ell_J is dynamical, nabla_mu ell_J must be included in the exchange identity | otherwise the scale field injects an untracked source leak | MISSING_SCALE_EXCHANGE_CLAUSE |

## Exchange Current Identity

| exchange_id | identity | basis | result | status |
| --- | --- | --- | --- | --- |
| EXC2557_0_required_identity | nabla_mu J_M^mu + I_GK = 0 | integrability of the A/current equation and surface independence of Q_M | required for a general dynamic source theorem | REQUIRED_NOT_DERIVED |
| EXC2557_1_minimal_on_shell_form | I_GK = -ell_J T^{mu nu}nabla_(mu tau_nu) | after nabla_mu T^{mu nu}=0 and fixed ell_J | exact form of the needed clock-exchange cancellation is identified | FORM_DERIVED_SOURCE_MISSING |
| EXC2557_2_full_scale_form | I_GK = -[(nabla_mu ell_J)T^{mu nu}tau_nu + ell_J(nabla_mu T^{mu nu})tau_nu + ell_J T^{mu nu}nabla_mu tau_nu] | before matter-shell and fixed-scale reductions | full cancellation target known, but not yet produced by parent variation | FORM_DERIVED_SOURCE_MISSING |
| EXC2557_3_parent_source_requirement | I_GK must be obtained from Gamma/Khat/tau equations or a Noether identity | parent action consistency | cannot be manually appended without losing the derivation route | MISSING_PARENT_DERIVATION |
| EXC2557_4_stationary_silence | in stationary collars I_GK=0 because the clock-strain source is zero | Killing/covariantly constant tau branch | gives a narrow local theorem path without dynamic exchange machinery | CONDITIONAL_CLOSES |
| EXC2557_5_boundary_silence | boundary/local projection terms must vanish or be included in I_GK | worldtube and local projection consistency | uncontrolled boundary leakage blocks promotion | MISSING_BOUNDARY_IDENTITY |

## Worldtube Surface Gate

| worldtube_id | clause | basis | result | status |
| --- | --- | --- | --- | --- |
| WTG2557_0_surface_difference | Q_M[Sigma_2]-Q_M[Sigma_1]=int_V nabla_mu J_M^mu dV + side_flux | Gauss theorem for the worldtube slab | surface independence needs exact conservation and controlled side flux | PASS_DERIVED |
| WTG2557_1_stationary_surface | if T has compact support, ell_J is fixed, tau is Killing, and side flux vanishes, Q_M is surface-independent | DIV2557_4 plus compact-support collar | stationary local source theorem can be attempted | CONDITIONAL_CLOSES |
| WTG2557_2_dynamic_surface | if tau is dynamic, surface drift equals int_V[-I_GK]dV plus side flux once exchange identity is known | EXC2557_0 dynamic branch | blocked until parent exchange current is derived | BLOCKED |
| WTG2557_3_distributional_surface | surface layers need jump terms in J_M or an explicit boundary flux ledger | compact source with boundary | prevents hiding source at the matter boundary | MISSING_JUMP_IDENTITY |
| WTG2557_4_no_orbital_GM | do not force Q_M/ell_J to equal observed GM | anti-circularity guardrail from 2556 | Newton limit remains derivation-first | PASS_GUARDRAIL |
| WTG2557_5_external_q_zero | outside compact matter support J_M=0, so q_loc=P_loc J_M=0 only after projection/support/boundary clauses are signed | source-free exterior | useful local-vacuum route, but still conditional | CONDITIONAL_NOT_CLAIM |

## Promotion Verdict

| verdict_id | question | result | evidence | effect |
| --- | --- | --- | --- | --- |
| PV2557_0_conservation_identity | Is the Hilbert current exactly conserved? | ONLY_IF_STATIONARY_OR_PARENT_EXCHANGE_DERIVED | product-rule divergence leaves clock strain and possible scale-gradient leakage | not a general theorem yet |
| PV2557_1_parent_scale | Is ell_J parent-derived? | NO | dimension and candidate routes are identified, but no action-normalised source exists | scale gate remains blocked |
| PV2557_2_clock_compatibility | Does local clock compatibility close? | CONDITIONALLY | Killing/stationary local collar closes; generic MTS time requires exchange current | split local and cosmological/dynamic branches |
| PV2557_3_worldtube | Is worldtube source mass surface-independent? | CONDITIONAL_NOT_GENERAL | surface independence follows only under conservation plus no side/boundary leakage | need jump/support theorem |
| PV2557_4_Newton_local_GR | Does 2557 prove Newton/local GR? | NO | source normalisation, dynamic exchange, and boundary support remain unsigned | no local-GR claim |
| PV2557_5_overall | Overall 2557 verdict | DERIVATION_SHARPENED_NOT_PROMOTED | exact leakage terms are now explicit; branch survives as a narrow stationary theorem plus dynamic exchange target | next target should derive I_GK or prove the stationary theorem cleanly |

## Claim Gates

| gate_id | claim | gate_status | reason | gate_pass | claim_promoted |
| --- | --- | --- | --- | --- | --- |
| GATE2557_0_product_rule | Full divergence identity is derived. | PASS | DIV2557_1 records exact product rule | true | false |
| GATE2557_1_stationary_contract | Stationary compact-source Hilbert current is conserved. | PASS_AS_CONDITIONAL_CONTRACT | requires fixed ell_J, conserved T, Killing tau, compact support, and no side flux | true | false |
| GATE2557_2_dynamic_exchange | Generic dynamic MTS source current is conserved. | BLOCKED | I_GK form is known but not parent-derived | false | false |
| GATE2557_3_parent_scale | ell_J is parent-derived and not fitted. | BLOCKED | no signed parent scale in corpus | false | false |
| GATE2557_4_worldtube | Q_M is surface-independent for physical bounded sources. | BLOCKED | dynamic exchange, jump terms, and side flux ledger missing | false | false |
| GATE2557_5_local_GR_Newton | Local GR/Newton branch passes. | BLOCKED | 2557 is a source-bridge gate, not a full metric-limit theorem | false | false |

## Decision Ledger

| decision_id | decision | reason | effect |
| --- | --- | --- | --- |
| DEC2557_0_keep_hilbert | Keep Hilbert/energy current as the primary matter source route. | it matches GR source structure and avoids species-tuned charges | continue this branch |
| DEC2557_1_no_fake_scale | Do not promote ell_J or derive it from observed GM. | that would make the Newton bridge circular | parent scale remains a blocker |
| DEC2557_2_split_clock_routes | Split stationary local collars from dynamic/cosmological clock activation. | stationary collars can close conditionally; dynamic clocks need I_GK | prevents local GR and cosmology from fighting each other |
| DEC2557_3_next_target | Next attempt parent derivation of the exchange current or prove the stationary source theorem. | the exact obstruction is now I_GK plus ell_J and boundary support | 2558 selected |

## Next Target

| route_id | selection_status | target_file | target_script | task | acceptance_target | guardrails |
| --- | --- | --- | --- | --- | --- | --- |
| NEXT2557_0_selected | selected | 2558-Y5-R2FR-parent-clock-exchange-current-or-stationary-source-theorem.md | scripts/Y5_R2FR_parent_clock_exchange_current_or_stationary_source_theorem_2558.py | try to derive I_GK from the parent tau/Gamma/Khat equations; if that fails, prove the narrower stationary compact-source theorem and demote dynamic closure | parent exchange-current derivation attempt, stationary theorem hypotheses, ell_J status, boundary/jump ledger, and no local-GR claim unless all gates close | no fitted GM; no M_H_ref reuse; no plateau axiom; no local-GR claim from conditional stationary contract; no GitHub |

## Branch Copies

| copy_id | source_path | target_path | source_exists | target_exists |
| --- | --- | --- | --- | --- |
| clock_gate_contract | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_NO_SHADOW_2557_CLOCK_COMPATIBILITY_GATE.csv | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\rab-sector\acquisition-queue\JR2557_CLOCK_COMPATIBILITY_GATE_NONCLAIM.csv | true | true |
| scale_gate_contract | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_NO_SHADOW_2557_PARENT_SCALE_OPTIONS.csv | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\rab-sector\acquisition-queue\JR2557_PARENT_SCALE_OPTIONS_NONCLAIM.csv | true | true |
| worldtube_gate_contract | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_NO_SHADOW_2557_WORLDTUBE_SURFACE_GATE.csv | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\local_bounds\Worldtube_surface_gate_2557_NONCLAIM.csv | true | true |

## Validation

| check_id | status | notes | detail |
| --- | --- | --- | --- |
| VAL2557_00_sources_exist | PASS | all cited source paths exist and needles are present |  |
| VAL2557_01_full_product_rule | PASS | full divergence identity derived |  |
| VAL2557_02_symmetric_clock_strain | PASS | antisymmetric clock vorticity drops out for symmetric stress |  |
| VAL2557_03_generic_clock_block | PASS | generic dynamic clock obstruction retained |  |
| VAL2557_04_stationary_gate | PASS | stationary/Killing clock gate recorded |  |
| VAL2557_05_clock_bound_form | PASS | clock-leak residual bound form recorded |  |
| VAL2557_06_parent_scale_blocked | PASS | parent scale remains blocked |  |
| VAL2557_07_no_forbidden_scale_fit | PASS | GM/H0/M_H_ref fitted scale routes rejected |  |
| VAL2557_08_exchange_identity_required | PASS | dynamic exchange identity remains required and unsigned |  |
| VAL2557_09_exchange_form_derived | PASS | minimal on-shell exchange form derived but not parent-sourced |  |
| VAL2557_10_worldtube_guardrail | PASS | orbital-GM source definition remains forbidden |  |
| VAL2557_11_no_local_gr_claim | PASS | local GR/Newton claim remains blocked |  |
| VAL2557_12_overall_verdict_nonclaim | PASS | overall verdict is sharpened nonclaim |  |
| VAL2557_13_next_target_selected | PASS | 2558 next target selected |  |
| VAL2557_14_branch_copies | PASS | nonclaim branch copies exist |  |
| VAL2557_15_all_outputs_inside_post_checkpoint | PASS | all 2557 outputs stay inside post-checkpoint-work |  |
| VAL2557_16_formalization_workbench_not_targeted | PASS | declared 2557 outputs do not target formalization-workbench | declared_2557_paths_outside_formalization=17/17 |
| VAL2557_OUTPUT_source_register | PASS | source_register output exists and has rows | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_NO_SHADOW_2557_SOURCE_REGISTER.csv |
| VAL2557_OUTPUT_divergence_identity | PASS | divergence_identity output exists and has rows | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_NO_SHADOW_2557_DIVERGENCE_IDENTITY.csv |
| VAL2557_OUTPUT_clock_gate | PASS | clock_gate output exists and has rows | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_NO_SHADOW_2557_CLOCK_COMPATIBILITY_GATE.csv |
| VAL2557_OUTPUT_scale_gate | PASS | scale_gate output exists and has rows | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_NO_SHADOW_2557_PARENT_SCALE_OPTIONS.csv |
| VAL2557_OUTPUT_exchange_identity | PASS | exchange_identity output exists and has rows | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_NO_SHADOW_2557_EXCHANGE_CURRENT_IDENTITY.csv |
| VAL2557_OUTPUT_worldtube_gate | PASS | worldtube_gate output exists and has rows | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_NO_SHADOW_2557_WORLDTUBE_SURFACE_GATE.csv |
| VAL2557_OUTPUT_promotion_verdict | PASS | promotion_verdict output exists and has rows | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_NO_SHADOW_2557_PROMOTION_VERDICT.csv |
| VAL2557_OUTPUT_claim_gates | PASS | claim_gates output exists and has rows | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_NO_SHADOW_2557_CLAIM_GATES.csv |
| VAL2557_OUTPUT_decision_ledger | PASS | decision_ledger output exists and has rows | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_NO_SHADOW_2557_DECISION_LEDGER.csv |
| VAL2557_OUTPUT_next_target | PASS | next_target output exists and has rows | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_NO_SHADOW_2557_NEXT_TARGET.csv |
| VAL2557_OUTPUT_branch_copies | PASS | branch_copies output exists and has rows | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_NO_SHADOW_2557_BRANCH_COPIES.csv |
| VAL2557_COPY_clock_gate_contract | PASS | clock_gate_contract copy exists and has rows | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\rab-sector\acquisition-queue\JR2557_CLOCK_COMPATIBILITY_GATE_NONCLAIM.csv |
| VAL2557_COPY_scale_gate_contract | PASS | scale_gate_contract copy exists and has rows | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\rab-sector\acquisition-queue\JR2557_PARENT_SCALE_OPTIONS_NONCLAIM.csv |
| VAL2557_COPY_worldtube_gate_contract | PASS | worldtube_gate_contract copy exists and has rows | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\local_bounds\Worldtube_surface_gate_2557_NONCLAIM.csv |
| VAL2557_OVERALL | PASS | 2557 derives the Hilbert-current leakage identity, blocks theorem claims on parent scale/exchange/boundary support, and selects 2558 |  |

