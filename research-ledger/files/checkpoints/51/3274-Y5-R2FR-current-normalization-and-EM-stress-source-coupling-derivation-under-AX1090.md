# 3274 - Current normalization and EM stress/source coupling derivation under AX1090

## Summary

3274 pushes the coupling problem forward into a concrete source law. Starting from the explicit low-energy block

`S[A,J;g,X]=int mu_obs[-Z_Q(X)F_Q^2/4 + s_J kappa_J(X) A_Q_mu J_Q^mu]`,

variation gives

`nabla_mu(Z_Q F_Q^{mu nu}) = -s_J kappa_J J_Q^nu`,

and therefore

`nabla_mu(kappa_J J_Q^mu)=0`.

So `C_J=L_X ln kappa_J` is not a free fudge factor. If `J_Q` is separately the parent Noether current, then `J_Q^mu nabla_mu ln kappa_J=0`; if ordinary currents are rich enough and there is no compensator/source-shadow current, this forces `C_J=0`. The current corpus does not yet sign those escape-route exclusions, so no local-GR/Maxwell claim is promoted.

## Action Variation
| derivation_id | formula | status | derivation |
| --- | --- | --- | --- |
| AV3274_0_action_block | S[A,J;g,X]=int mu_obs[-Z_Q(X)F_Q^2/4 + s_J kappa_J(X) A_Q_mu J_Q^mu] + S_matter + S_owner[X] | EXACT_STARTING_BLOCK_FOR_CJ_AUDIT | Use one explicit sign flag s_J so the source normalization question is not hidden in conventions. |
| AV3274_1_Maxwell_equation | nabla_mu(Z_Q F_Q^{mu nu}) = -s_J kappa_J J_Q^nu | DERIVED_FROM_ASSUMED_BLOCK | Integrate -Z_Q F^{mu nu} nabla_mu(delta A_nu) by parts and combine with s_J kappa_J J^nu delta A_nu. |
| AV3274_2_weighted_current_conservation | 0 = nabla_nu nabla_mu(Z_Q F_Q^{mu nu}) = -s_J nabla_nu(kappa_J J_Q^nu) | EXACT_CURRENT_CONSTRAINT | antisymmetry of F_Q makes the double divergence vanish, so the source entering Maxwell is the weighted current kappa_J J_Q. |
| AV3274_3_CJ_definition | C_J := L_X ln kappa_J | DEFINED_AS_FINITE_COUPLING_TARGET | This is the 3273 alpha decomposition component that controls Maxwell source normalization and Lorentz/Poynting transfer. |
| AV3274_4_if_J_Noether_conserved | if nabla_mu J_Q^mu=0 then J_Q^mu nabla_mu ln kappa_J=0 | GAUGE_CURRENT_LOCK_LEMMA | Substitute separate Noether conservation into nabla_mu(kappa_J J_Q^mu)=0. |

## Gauge/Current Lock
| lemma_id | mathematical_statement | consequence | status |
| --- | --- | --- | --- |
| GL3274_0_statement | Gauge invariance and the Maxwell equation require nabla_mu(kappa_J J_Q^mu)=0. If J_Q is already the parent Noether current with nabla_mu J_Q^mu=0, then J_Q^mu nabla_mu ln kappa_... | A spatial/time/material variation in kappa_J is not free; it must either vanish on all allowed currents or be carried by an extra compensating current. | EXACT_CONDITIONAL_LEMMA |
| GL3274_1_arbitrary_current_corollary | If the ordinary matter sector permits enough local current directions through each lab point, J_Q^mu nabla_mu ln kappa_J=0 for all such J_Q implies nabla_mu kappa_J=0 and hence ... | This is the clean route to source-normalization zero: not a fitted parameter, but a gauge-current consistency result. | VALID_IF_CURRENT_OWNER_AND_CURRENT_RICHNESS_SIGNED |
| GL3274_2_countermodel_compensator | nabla_mu(kappa_J J_Q^mu + J_comp^mu)=0 can hold with variable kappa_J if an extra parent current J_comp carries the mismatch. | Current MTS cannot promote C_J=0 unless it excludes compensator/source-shadow/non-Hilbert EM charge currents. | COUNTERMODEL_RETAINED |
| GL3274_3_relation_to_3273 | With C_Z=C_R=0, the 3273 law gives C_e=2C_J, so \|C_J\| <= \|C_e\|_bound/2. | The pure-alpha DD envelope can bound current normalization only under the explicit Maxwell/readout-zero side conditions. | CONDITIONAL_BOUND_ROUTE |

## EM Stress and Poynting Exchange
| law_id | formula | status | derivation |
| --- | --- | --- | --- |
| SP3274_0_stress_tensor | T_EM^{mu nu}=Z_Q(F_Q^{mu rho}F_Q^nu_rho - 1/4 g_obs^{mu nu}F_Q^2) up to the fixed metric-sign convention | DERIVED_FROM_ASSUMED_BLOCK | Metric variation of the Maxwell kinetic block with Z_Q treated as the parent-owned scalar coefficient. |
| SP3274_1_stress_exchange | nabla_mu T_EM^{mu nu} = s_J kappa_J F_Q^nu_mu J_Q^mu + Q_Z^nu, with Q_Z^nu proportional to F_Q^2 nabla^nu Z_Q and owner-sector Euler terms | EXACT_CONDITIONAL_EXCHANGE_LAW | Use the Maxwell equation plus the Bianchi identity; Z_Q gradients are not EM stress conservation, they are exchange with the parent owner of Z_Q. |
| SP3274_2_matter_exchange | nabla_mu(T_matter^{mu nu}+T_EM^{mu nu}+T_owner^{mu nu})=0; if Q_Z^nu=0 then nabla_mu T_matter^{mu nu}=-s_J kappa_J F_Q^nu_mu J_Q^mu | SOURCE_COUPLING_CONTRACT_DERIVED | Diffeomorphism Ward identity for the combined parent block fixes the equal-and-opposite force law. |
| SP3274_3_Poynting_readout | u_EM=Z_Q(E^2+B^2)/2, S_EM^i=Z_Q(E x B)^i, and partial_t u_EM + div S_EM = -s_J kappa_J E.J + Z_Q/readout-gradient exchange terms | POYNTING_BACKGROUND_FIELD_ROUTE_MADE_EXPLICIT | 3+1 split of SP3274_1 in the observed coframe. |
| SP3274_4_q_loc_link | unowned EM/source exchange contributes to the same kind of projected Ward residual as q_loc^nu=P_loc nabla_mu T_extra^{mu nu} | LOCAL_RESIDUAL_MAPPING_READY | Imports the 513 stress rewrite: failed owner terms must be stress-exchange residuals, not silent closure assumptions. |

## C_J Owner Audit
| audit_id | needed_signature | status | blocks_CJ_zero |
| --- | --- | --- | --- |
| CJA3274_0_weighted_current_owned | J_Q is the parent Noether/representation current and the Maxwell source is exactly kappa_J J_Q. | CONDITIONAL_NOT_PARENT_SIGNED | true |
| CJA3274_1_no_current_rescale | No q_A(X), c_A(X), kappa_A(X), source-shadow, or hidden current rescaling survives in S_int. | UNSIGNED_COUNTERMODEL_RETAINED | true |
| CJA3274_2_no_compensator_current | No extra J_comp current carries nabla(kappa_J J_Q) mismatch. | UNSIGNED | true |
| CJA3274_3_current_richness | ordinary lab matter supplies enough local current directions that J.nabla ln kappa_J=0 forces nabla kappa_J=0. | MATHEMATICALLY_CLEAN_BUT_NOT_PARENT_SIGNED | true |
| CJA3274_4_CJ_zero_verdict | CJA3274_0 through CJA3274_3 all pass under the same local generator. | CJ_ZERO_NOT_PARENT_SIGNED | true |

## Conditional C_J Bound
| bound_id | coefficient | side_conditions | bound_value | status |
| --- | --- | --- | --- | --- |
| CJB3274_0_conditional_CJ_from_alpha | C_J=L_X ln kappa_J | C_Z=0 and C_R=0, same local generator X, same observed coframe/readout | 6.948988557475e-13 | CONDITIONAL_BOUND_ONLY_NONCLAIM |
| CJB3274_1_general_CJ_unbounded_by_alpha_alone | C_J=L_X ln kappa_J | C_Z and C_R not both fixed zero | MISSING_STANDALONE_GENERAL_CJ_BOUND | REFUSE_STANDALONE_CJ_CLAIM |

## C_J Runner
| case_id | C_J_prediction | C_Z_zero_assumed | C_R_zero_assumed | prediction_over_bound | result | expectation_met | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CJR3274_0_missing_CJ | MISSING | true | true | MISSING | REFUSE_OR_FAIL | true | false |
| CJR3274_1_CJ_zero_conditional | 0 | true | true | 0.000000000000e+00 | PASS_NUMERIC_NONCLAIM | true | false |
| CJR3274_2_half_conditional_bound | 3.474494278738e-13 | true | true | 5.000000000001e-01 | PASS_NUMERIC_NONCLAIM | true | false |
| CJR3274_3_at_conditional_bound | 6.948988557475e-13 | true | true | 1.000000000000e+00 | PASS_NUMERIC_NONCLAIM | true | false |
| CJR3274_4_twice_conditional_bound | 1.389797711495e-12 | true | true | 2.000000000000e+00 | FAIL_BOUND | true | false |
| CJR3274_5_general_without_CZ_CR | 3.474494278738e-13 | false | false | 5.000000000001e-01 | REFUSE_OR_FAIL | true | false |

## Promotion Gates
| gate_id | passed | claim_allowed | detail |
| --- | --- | --- | --- |
| GATE3274_0_variation_derivation | true | false | This is a derived low-energy contract, not a parent action signature by itself. |
| GATE3274_1_gauge_current_lock | true | false | C_J=0 follows only if current owner, no compensator, and current-richness clauses are signed. |
| GATE3274_2_Poynting_exchange | true | false | EM flow is now mapped to stress exchange and q_loc-style residuals. |
| GATE3274_3_CJ_zero_parent_signed | false | false | current rescale/source-shadow/compensator exclusions remain unsigned. |
| GATE3274_4_CJ_runner_disciplined | true | false | conditional runner works only under C_Z=C_R=0 side conditions. |

## Decisions
| decision_id | decision | why_it_moves_forward | claim_allowed |
| --- | --- | --- | --- |
| DEC3274_0_real_progress | C_J is now tied to a weighted-current conservation law, not left as a free symbol. | Maxwell variation gives nabla_mu(kappa_J J_Q^mu)=0 and therefore a sharp gauge-current route to C_J=0. | false |
| DEC3274_1_poynting_route | Poynting/EM stress flow is explicitly in the source-coupling stack. | S_EM=Z_Q E x B and stress exchange show where a background-field/flow interpretation must live without breaking conservation. | false |
| DEC3274_2_CJ_status | C_J=0 is plausible as a theorem route but not parent-signed. | the remaining proof debt is no compensator/source-shadow/current-rescale plus ordinary-current richness, not an undefined coupling mystery. | false |
| DEC3274_3_bound_status | \|C_J\| <= 6.948988557475e-13 is available only if C_Z=C_R=0. | future numeric or theorem-zero C_J rows can be scored immediately, but alpha data cannot bound general C_J alone. | false |

## Next Target
| next_id | target_doc | objective | guardrail |
| --- | --- | --- | --- |
| NEXT3274_0_3275 | 3275-Y5-R2FR-no-compensator-current-and-source-shadow-ban-or-finite-CJ-row-under-AX1090.md | Try to prove the no-compensator/source-shadow clause for kappa_J: show the only gauge current entering Maxwell is the parent Noether current, or emit the first source-backed fin... | Do not re-prove Maxwell variation; start from 3274 weighted-current law and attack the remaining escape routes. |

## Validation
| check_id | check | passed | detail |
| --- | --- | --- | --- |
| VAL3274_0_sources_exist | all cited source paths exist | true |  |
| VAL3274_1_sources_parse | all cited source paths parse | true |  |
| VAL3274_2_outputs_parse | all 3274 output CSVs parse | true | non-validation outputs parsed before validation write |
| VAL3274_3_variation_law_present | Maxwell and weighted-current equations are present | true | nabla_mu(kappa_J J_Q^mu)=0 |
| VAL3274_4_poynting_law_present | Poynting/stress exchange law is present | true | S_EM=Z_Q(E x B) |
| VAL3274_5_CJ_bound_positive | conditional C_J bound is positive numeric | true | 6.948988557475e-13 |
| VAL3274_6_CJ_zero_not_falsely_signed | C_J zero remains conditional rather than promoted | true | CJ_ZERO_NOT_PARENT_SIGNED |
| VAL3274_7_runner_expectations | C_J runner expectations all match | true | CJR3274_0_missing_CJ=REFUSE_OR_FAIL;CJR3274_1_CJ_zero_conditional=PASS_NUMERIC_NONCLAIM;CJR3274_2_half_conditional_bound=PASS_NUMERIC_NONCLAIM;CJR3274_3_at_conditional_bound=PAS... |
| VAL3274_8_claim_gates_false | no 3274 gate allows local-GR/WEP/Maxwell claim | true | all claim_allowed=false |
| VAL3274_9_formalization_untouched | formalization-workbench modified-file count remains zero by this script | true | formalization_changed_count=0 |
| VAL3274_10_overall | 3274 validation overall | true | all required checks passed |

Generated UTC: 2026-06-27T14:46:40.222661+00:00
