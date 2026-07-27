# 3263 - Source-profile channel projection or parent-domain lock under AX1090

Private derivation/checkpoint. This does not claim local GR, Newton, Maxwell, WEP, R10, PPN, clock, orbital, material-response, or public source-coupling success.

## Verdict
- `3263` closes the experimental EP-channel projection for the **eta-level** convention: MICROSCOPE fits `delta_x g_x` and identifies final `eta` with `delta_x` in practice.
- Therefore, if `B_alpha` is defined by `eta_AB^EM = DeltaQe_AB B_alpha^eta`, do **not** multiply by an extra `tau_channel_projection`.
- The conservative eta-level bound remains `|B_alpha^eta| <= 1.389797711688e-12` after the 0.98 readout factor.
- The parent-source convention is still open: projecting an upstream MTS source residual into eta still needs the source-charge/force-map theorem.

## Source Register
| source_id | exists | parse_ok | role | evidence_hits | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| SRC3263_3262_handoff | true | true | 3262 selected source-profile/channel projection or parent domain lock | L7:- This does **not** close full `tau_WEP`; it splits it into `tau_readout_X * tau_source_profile * tau_channel_projection`. \| L8:- Using the sourced lower bound `tau_readout_X >= 0.98`, the remaining product obeys `\|beta_source_alpha*b_alpha_EM*tau_source_profile*tau_channel_projection\| <= 1.389797711688e-12`. \| L33:\| TAU3262_0_decomposition \| tau_WEP \| tau_WEP = tau_readout_X * tau_source_profile * tau_channel_projection \| DECOMPOSITION_DEFINED \| tau_readout_X bounded; source_profile/channel_projection missing \| false \| \| L35:\| TAU3262_2_source_profile \| tau_source_profile \| projection of MTS source residual onto Earth/orbit/source-worldtube profile \| WIP1899_1/2/5 remain missing \| MISSING \| false \| | false |
| SRC3263_3262_tau | true | true | tau_WEP factorization with sourced readout subfactor | L3:TAU3262_1_readout_X,tau_readout_X,tau_readout_X = tilde(a)_c11,MICROSCOPE_SOURCE_BACKED,9.800000000000e-01 <= tau_readout_X <= 1.020000000000e+00,false \| L5:TAU3262_3_channel_projection,tau_channel_projection,projection of selected EM/DD residual onto the MICROSCOPE fitted EP channel after nuisance/correction model,official arrays or exact parent reduction still required,MISSING,false | false |
| SRC3263_3262_bound | true | true | readout-reduced product bound | L4:RB3262_2_remaining_product_worst,\|beta_source_alpha*b_alpha_EM*tau_source_profile*tau_channel_projection\|,B_bound/min(\|tau_readout_X\|),1.389797711688e-12,READOUT_REDUCED_PRODUCT_BOUND,false | false |
| SRC3263_MICROSCOPE_tex | true | true | MICROSCOPE fitted EP channel equations | L102:The space mission MICROSCOPE dedicated to the test of the Equivalence Principle (EP) operated from April 25, 2016 {until} the deactivation of the satellite on October 16, 2018. {In this analysis we compare the free-fall accelerations ($a_{\rm A}$ and $a_{\rm B}$) of two test mass \| L152:higher and higher precision.} Tests of the WEP are usually presented in terms of the E\"otv\"os ratio $\eta$ \cite{eotvos22}, defined as the normalised difference of accelerations (or equivalently, as the normalised difference of gravitational-to-inertial {mass ratios}) of two te \| L154:%\eta = 2 \frac{a_2-a_1}{a_2+a_1} = 2 \frac{m_{g,2}/m_{i,2} - m_{,g1}/m_{i,1}}{m_{g,2}/m_{i,2} + m_{g,1}/m_{i,1}} \| L155:\eta(2,1) = 2 \frac{a_2-a_1}{a_2+a_1} = 2 \frac{m_{G2}/m_{I2} - m_{G1}/m_{I1}}{m_{G2}/m_{I2} + m_{G1}/m_{I1}} | false |
| SRC3263_1899_pack | true | true | remaining parent-source profile inputs | L3:WIP1899_1_source_worldtube_profile,source_worldtube,P_WEP_R_source_Earth_worldtube.csv,"Earth/source stress or mass-density profile in observed local frame, or parent theorem reducing to calibrated point source with error bound",MISSING,MISSING_SOURCE_PROFILE_WEIGHTING,SI density \| L7:WIP1899_5_force_map,observed_force_map,P_WEP_force_map_eta_convention.md,"source residual to differential acceleration map in same observed coframe, with eta sign/normalization and common-mode guard",MISSING,MISSING_FORCE_READOUT_MAP,m s^-2 internally; dimensionless eta after nor | false |
| SRC3263_1397_unique_F2 | true | true | parent domain no-counterterm status | L4:UMF1397_2_operator_basis_uniqueness,no independent Maxwell quadratic invariant,"the parent operator basis forbids every observed-only F_Q^2 term not inherited from <F,F>_P","Allowed_2der(parent, U(1)_Q) = {<F,F>_P subblock} and not {<F,F>_P, F_Q^2}",RCE765_0 and ELA989_1 keep Del \| L9:UMF1397_7_current_verdict,unique Maxwell F2 proof status,promote Z_unique_F2 only if the lambda_A counterterm is forbidden by parent structure,Z_unique_F2 = false while DeltaS_lambda is allowed,"lambda_A F_Q^2 remains gauge invariant, diffeomorphism invariant, and not excluded by | false |

## MICROSCOPE EP Channel Evidence
| evidence_id | line_number | text_excerpt | role | valid_for_claim |
| --- | --- | --- | --- | --- |
| MCH3263_0_force_model | 342 | \vv\gamma^{(d)} = \delta(2,1) \vv{g}(O_{\rm sat}) + ([{\rm T}] - [{\rm In}]) \vv{\Delta} + \vv{b_1}^{(d)}, | raw differential acceleration contains the Eotvos/mass-ratio parameter multiplying satellite gravity. | false |
| MCH3263_1_g_source | 347 | \item $\vv{g}(O_{\rm sat}) $ is the gravity acceleration computed at the centre of the satellite, | experimental source signal is computed Earth gravity at satellite centre. | false |
| MCH3263_2_corrected_channel | 371 | \Gamma^{(d)}_{x, {\rm corr}}=\tilde{b}_x^{'(d)}+\delta_x g_x+\delta_z g_z+\Delta'_{x} S_{xx} +\Delta'_{z} S_{xz}+ n_x^{(d)}, | corrected fitted X channel carries delta_x times g_x. | false |
| MCH3263_3_uncorrelated_signals | 392 | As a consequence, these signals are almost uncorrelated. | the EP channel is separated by frequency/signature from nuisance terms in the model. | false |
| MCH3263_4_parameters_estimated | 384 | \item The parameters $\delta_x$, $\delta_z$, $\Delta'_{x}$ and $\Delta'_{z}$ are estimated. | delta_x is a fitted parameter, not a hidden hand-assigned projection. | false |
| MCH3263_5_eta_identification | 926 | {Putting all together, and remembering that the conventional E\"otv\"os parameter $\eta$ {can be practically identified} to the parameter $\delta_{x}$ measured in this experiment, we end up for SUREF with} | paper identifies final eta with delta_x in practice. | false |

## Eta-Level vs Parent-Source Convention Split
| convention_id | definition | tau_status | bound_use | what_remains | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| CONV3263_ETA_LEVEL | Define B_alpha^eta by eta_AB^EM = DeltaQe_AB * B_alpha^eta + residual. | experimental EP-channel projection is already absorbed into the published eta fit; only readout calibration uncertainty remains | use 3260 bound directly, or 3262 conservative readout-corrected version | no-cancellation/full-channel control and parent interpretation of B_alpha^eta | false |
| CONV3263_PARENT_SOURCE | Define upstream B_alpha^parent before source/readout projection. | requires tau_source_profile and tau_channel_projection from parent source profile or official/equivalent arrays | only product B_alpha^parent*tau_source_profile*tau_channel_projection is bounded | source worldtube/profile, force map, and parent source-charge normalization | false |

## Channel Projection Result
| projection_id | projection | result | formula | claim_effect | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| PROJ3263_0_observed_eta_channel | eta_AB -> MICROSCOPE fitted delta_x | SOURCE_BACKED | delta_x = tilde(a)_c11 eta_AB with \|tilde(a)_c11-1\|<2e-2 and final eta practically identified with delta_x | the experimental channel projection is not a remaining blocker for eta-level bounds | false |
| PROJ3263_1_parent_source_channel | MTS parent source residual -> eta_AB | NOT_CLOSED | eta_AB^MTS = source/force/readout contraction of parent residual | still requires parent source-charge theorem or source_profile/force_map inputs | false |
| PROJ3263_2_no_double_tau | avoid multiplying by tau twice | GUARD_ACTIVE | if B_alpha is eta-level, do not also include tau_channel_projection; if B_alpha is parent-source-level, include tau factors explicitly | prevents over-suppressing the residual by convention confusion | false |

## Convention Bound Output
| bound_id | convention | quantity | formula | value | status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| CB3263_0_eta_level_reported | CONV3263_ETA_LEVEL | \|B_alpha^eta\| | 2.7e-15/\|DeltaQe_DD\| | 1.362001757454e-12 | OBSERVED_ETA_LEVEL_BOUND | false |
| CB3263_1_eta_level_readout_conservative | CONV3263_ETA_LEVEL | \|B_alpha^eta\| with tau_readout_X>=0.98 | (2.7e-15/\|DeltaQe_DD\|)/0.98 | 1.389797711688e-12 | CONSERVATIVE_READOUT_CORRECTED_BOUND | false |
| CB3263_2_parent_source_product | CONV3263_PARENT_SOURCE | \|B_alpha^parent*tau_source_profile*tau_channel_projection\| | (2.7e-15/\|DeltaQe_DD\|)/0.98 | 1.389797711688e-12 | UPSTREAM_PRODUCT_ONLY | false |

## Remaining Parent-Source Inputs
| remaining_id | missing_piece | current_best | needed_next | valid_for_claim |
| --- | --- | --- | --- | --- |
| REM3263_0_beta_source_interpretation | parent meaning of beta_source_alpha | eta-level product bound is usable empirically, but parent source-charge interpretation remains open | same-owner Hamiltonian/source theorem or force-map input | false |
| REM3263_1_source_profile_only_for_upstream | tau_source_profile | not needed for eta-level bound; needed only if B_alpha is defined upstream of the observed Eotvos parameter | Earth/source worldtube profile or theorem reducing parent residual to eta | false |
| REM3263_2_multi_channel_control | no-cancellation/full-channel fit | isolated EM/DD branch bound is hard but not full MTS WEP pass | include light-quark/surface/readout channels or parent no-cancellation theorem | false |

## Parent Domain Lock Audit
| domain_id | question | answer | current_status | valid_for_claim |
| --- | --- | --- | --- | --- |
| DOM3263_0_eta_route_vs_zero_route | Should we prioritize parent-domain lock or eta-level empirical bound? | both are now cleanly separated: eta-level bound constrains fallback; parent-domain lock would remove the branch by b_alpha_EM=0 | BOUND_ROUTE_EXECUTABLE_ZERO_ROUTE_CONDITIONAL | false |
| DOM3263_1_counterterm_block | What blocks fixed EM zero? | UMF1397 still retains lambda_A while quotient-only/independent F_Q^2 counterterm is not forbidden by a signed parent domain | NO_COUNTERTERM_NOT_SIGNED | false |

## Claim Gates
| gate_id | gate | passed | reason | claim_allowed |
| --- | --- | --- | --- | --- |
| CG3263_0_eta_channel_projection | MICROSCOPE eta-level channel projection sourced | true | measurement model fits delta_x g_x and identifies eta with delta_x in practice | false |
| CG3263_1_parent_source_projection | MTS parent source residual projected to eta | false | same-owner source theorem or source_profile/force-map still missing | false |
| CG3263_2_parent_domain_lock | parent domain forbids lambda_A counterterm | false | no-counterterm theorem remains conditional | false |
| CG3263_3_local_GR | local GR/Newton/Maxwell promotion | false | eta-level bound is not a full parent-source/local-GR derivation | false |

## Decision
| decision_id | verdict | what_moved | best_next | fallback_next | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| DEC3263_0 | ETA_CHANNEL_PROJECTION_SOURCED_PARENT_SOURCE_STILL_OPEN | the experimental channel projection is closed for eta-level bounds, avoiding a false tau blocker | attack parent source-charge meaning of beta_source_alpha or the parent no-counterterm domain | add other composition channels to prevent EM-only cancellation mistakes | false |

## Next Target
| next_id | selected | target_doc | target_script | objective | guardrail | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| NEXT3263_0_3264 | primary | 3264-Y5-R2FR-parent-source-charge-meaning-or-multichannel-WEP-vector-under-AX1090.md | scripts/Y5_R2FR_3264_parent_source_charge_meaning_or_multichannel_WEP_vector.py | Either derive the parent source-charge meaning of beta_source_alpha in the eta-level branch, or add the non-EM DD/material channels so the WEP comparison is not EM-only. | Do not reintroduce tau_channel_projection for eta-level B_alpha; use it only for upstream parent-source convention. | false |

## Validation
| check_id | check | passed | detail |
| --- | --- | --- | --- |
| VAL3263_0_sources_exist | all cited source paths exist | true |  |
| VAL3263_1_sources_parse | all cited source CSV/MD/TEX paths parse | true |  |
| VAL3263_2_channel_lines_found | MICROSCOPE channel evidence lines are found | true | MCH3263_0_force_model:342;MCH3263_1_g_source:347;MCH3263_2_corrected_channel:371;MCH3263_3_uncorrelated_signals:392;MCH3263_4_parameters_estimated:384;MCH3263_5_eta_identification:926 |
| VAL3263_3_outputs_parse | all 3263 output CSVs parse | true |  |
| VAL3263_4_conservative_bound_matches | conservative eta-level bound equals direct/0.98 | true | 1.389797711688e-12 |
| VAL3263_5_claim_gates_false | no 3263 claim gate allows local-GR/WEP/Maxwell promotion | true | all claim_allowed=false |
| VAL3263_6_formalization_untouched | formalization-workbench modified-file count remains zero by this script | true | formalization_changed_count=0 |
| VAL3263_7_overall | 3263 validation overall | true | all required checks passed |

Generated UTC: 2026-06-27T06:04:25.256142+00:00
