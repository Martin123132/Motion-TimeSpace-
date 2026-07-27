# 3266 - Source convention lock or two-channel bound promotion under AX1090

Private derivation/checkpoint. This does not claim local GR, Newton, Maxwell, WEP, R10, PPN, clock, orbital, material-response, or public source-coupling success.

## Verdict
- `3266` converts the remaining two-channel WEP issue into an exact residual-inclusive theorem: `eta = A D + epsilon`.
- Since `3265` proved `A` is rank two, the algebra is no longer the blocker; the exact law is `D=A^-1(eta-epsilon)`.
- This gives a clean no-smuggling contract: sign one common parent `D_hatm,D_e` source map and supply residual budgets `epsilon_k`, or do not promote the branch.
- The strongest honest statement is now: cancellation is killed by the second vector **if** the parent source convention is locked.

## Source Register
| source_id | exists | parse_ok | role | evidence_hits | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| SRC3266_3265_handoff | true | true | 3265 rank-two conditional inversion result | L7:- The two-row matrix `[(TA6V-PtRh10),(Be-Ti)]` is rank two in `(Q'_hatm,Q'_e)`, so the pure algebraic cancellation escape is broken **conditionally**. \| L59:\| NCT3265_1_same_coupling_coordinates \| MICROSCOPE and Eot-Wash must project onto the same parent D_hatm/D_e coordinates. \| UNSIGNED_PARENT_CONVENTION \| Both are Earth-field WEP arenas, but the MTS parent source map has not signed equality of calibration coordinates. \| derive/sou \| L74:\| DEC3265_0 \| SECOND_VECTOR_FOUND_RANK_TWO_BUT_PARENT_LOCK_UNSIGNED \| det(A)=-8.926159003891e-06; conditional CB3265_1_D_hatm_component_bound=8.549427862687e-11; CB3265_2_D_e_component_bound=1.443549691533e-10 \| derive/source the common parent source-convention lock so MICROSCOPE \| L89:\| VAL3265_5_delta_matrix_rank_two \| two-arena DD matrix is rank two \| true \| determinant=-8.926159003891e-06; sin_angle_abs=3.178915482438e-01; condition=7.457960818153e+00 \| | false |
| SRC3266_DD_two_channel | true | true | DD two-channel body-charge convention | L1063:{\alpha}_A \simeq d_g^* + \left[ (d_{\hat m} - d_g) Q'_{\hat m} + d_e Q'_e \right]_A \| L1071:Q'_{\hat m} = -\frac{0.036}{A^{1/3}} - 1.4 \times 10^{-4} \, \frac{Z(Z-1)}{A^{4/3}} \| L1075:Q'_{e} = + 7.7 \times 10^{-4} \frac{Z(Z-1)}{A^{4/3}} . \| L1090:{\rm Material} &$A$ &$Z$ &$-Q'_{\hat m}$ &$Q'_e$ \\ \\ | false |
| SRC3266_EOTWASH_BeTi | true | true | Eot-Wash Be/Ti arena source and eta row | L37:We used a continuously rotating torsion balance instrument to measure the acceleration difference of beryllium and titanium test bodies towards sources at a variety of distances. Our result $\Delta a_{N,Be-Ti}=(0.6\pm 3.1)\times 10^{-15}\;\ms$ improves limits on equivalence-princ \| L141:\eta(\mbox{Be}-\mbox{Ti})= \frac{\Delta a_{N}}{a_{\perp}^g}= (0.3\pm 1.8)\times 10^{-13}. \| L147:interaction (Eq.~1) as a function of range $\lambda$. To establish these limits we used the mass density and charge content of the environment surrounding the torsion balance to create a source model. For $\lambda= 1-100$~m the source is dominated by a hill sloping towards the Ea | false |
| SRC3266_delta_matrix | true | true | Two-row DD delta matrix from 3265 | L2:DM3265_0_MICROSCOPE_TA6V_minus_PtRh10,MICROSCOPE_TIPT_EARTH_FIELD,TA6V_minus_PtRh10,-3.314967641189e-03,-1.982376296945e-03,2.755102040816e-15,MICROSCOPE final eta divided by tau_readout_min=0.98 from 3264,D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal  \| L3:DM3265_1_EOTWASH_Be_minus_Ti,EOTWASH_BETI_EARTH_FIELD,Be_minus_Ti,-7.101658786830e-03,-1.554163298639e-03,3.828000000000e-13,\|0.3e-13\| + 1.96*1.8e-13 from Eot-Wash eta(Be-Ti),D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motio | false |
| SRC3266_rank | true | true | Rank and conditioning result from 3265 | L2:RANK3265_0_two_arena_DD_matrix,"[(TA6V-PtRh10),(Be-Ti)] in (Q'_hatm,Q'_e)",-8.926159003891e-06,3.862489643328e-03,7.269730468415e-03,9.481270819649e-01,3.178915482438e-01,7.457960818153e+00,true,The Eot-Wash Be/Ti vector is not parallel to the MICROSCOPE Ti/Pt vector; cancellatio | false |

## Residual-Inclusive Inversion Theorem
| theorem_id | statement | proof | determinant | result | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| THM3266_0_residual_inclusive_two_arena_inversion | For eta = A D + epsilon with A rank two, D=A^{-1}(eta-epsilon). Therefore \|D_j\| is bounded by the absolute inverse row applied to \|eta\|+\|epsilon\|. | A is a 2x2 matrix of DD material-charge differences. det(A) != 0 by 3265. Left-multiply by A^{-1}; take componentwise absolute values and the triangle inequality. | -8.926159003891e-06 | \|D_hatm\| <= \|inv00\|(b1+e1)+\|inv01\|(b2+e2); \|D_e\| <= \|inv10\|(b1+e1)+\|inv11\|(b2+e2) | false |
| THM3266_1_zero_residual_special_case | If epsilon_1=epsilon_2=0 and the two arenas share the same parent D coordinates, 3265's finite two-channel bounds follow exactly. | Set e1=e2=0 in THM3266_0. | -8.926159003891e-06 | absolute inverse = [[1.741133334015e+02,-2.220861510624e+02],[-7.956007487357e+02,3.713767186697e+02]] | false |
| THM3266_2_no_unbounded_cancellation | A cancellation direction for one material row is not a cancellation direction for the other unless D=0, up to residual budgets. | The nullspaces of two nonparallel rows in R^2 intersect trivially because det(A) != 0. | -8.926159003891e-06 | single-row cancellation becomes a bounded parallelogram once residual budgets are supplied | false |

## Matrix Inverse and Residual Gains
| gain_id | scenario | determinant | inv00_Dhatm_from_MICROSCOPE | inv01_Dhatm_from_EOTWASH | inv10_De_from_MICROSCOPE | inv11_De_from_EOTWASH | epsilon_MICROSCOPE | epsilon_EOTWASH | Dhatm_bound | De_bound | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| GAIN3266_0_inverse_coefficients | matrix_inverse | -8.926159003891e-06 | 1.741133334015e+02 | -2.220861510624e+02 | -7.956007487357e+02 | 3.713767186697e+02 |  |  |  |  | false |
| GAIN3266_1_zero_residual | zero_residual | -8.926159003891e-06 | 1.741133334015e+02 | -2.220861510624e+02 | -7.956007487357e+02 | 3.713767186697e+02 | 0.000000000000e+00 | 0.000000000000e+00 | 8.549427862687e-11 | 1.443549691533e-10 | false |
| GAIN3266_2_ten_percent_eta_residual | ten_percent_eta_residual | -8.926159003891e-06 | 1.741133334015e+02 | -2.220861510624e+02 | -7.956007487357e+02 | 3.713767186697e+02 | 2.755102040816e-16 | 3.828000000000e-14 | 9.404370648955e-11 | 1.587904660686e-10 | false |
| GAIN3266_3_eta_sized_residual | eta_sized_residual | -8.926159003891e-06 | 1.741133334015e+02 | -2.220861510624e+02 | -7.956007487357e+02 | 3.713767186697e+02 | 2.755102040816e-15 | 3.828000000000e-13 | 1.709885572537e-10 | 2.887099383065e-10 | false |

## Source Convention Lock Clauses
| clause_id | required_clause | mathematical_form | status | if_missing | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| LOCK3266_0_common_field | Both arenas must couple to the same parent MTS residual/source field, not two arena-specific fields. | D_i is arena-independent: D_i^MICROSCOPE = D_i^EOTWASH = D_i | UNSIGNED_PARENT_ACTION_CLAUSE | matrix inversion bounds the wrong variables: D_i^1 and D_i^2 rather than one common D_i | false |
| LOCK3266_1_common_DD_basis | MTS parent source charge must reduce to the same DD basis Q'_hatm,Q'_e used in both material rows. | alpha_A-alpha_B = DeltaQ_hatm D_hatm + DeltaQ_e D_e + residual | CONDITIONALLY_DERIVED_FROM_DD_NOT_PARENT_SIGNED | Be/Ti and Ti/Pt rows may be calibration coordinates only | false |
| LOCK3266_2_source_normalization | Earth/source normalization and eta readout must be absorbed into the same D_i convention or explicit residual epsilons. | eta_k = row_k dot D + epsilon_k, with no hidden scale s_k of unknown sign | PARTIAL_SOURCE_BACKING_NOT_PARENT_LOCKED | unknown s_k rescales rows and can fake or erase bounds | false |
| LOCK3266_3_residual_budget | All omitted channels must be bounded as epsilon_MICROSCOPE and epsilon_EOTWASH. | \|epsilon_k\| <= e_k supplied before promotion | EXACT_BOUND_LAW_DERIVED_BUT_NUMERIC_EPSILONS_MISSING | finite zero-residual bounds remain smoke only | false |

## Promotion Contract
| contract_id | deliverable | must_supply | acceptance_test | current_status | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| CON3266_0_parent_action_signature | parent action/source map clause | variation showing one local parent source current projects to Q'_hatm and Q'_e with arena-independent D_hatm,D_e | LOCK3266_0 and LOCK3266_1 become signed without adding experiment-specific coefficients | missing | false |
| CON3266_1_residual_rows | epsilon_MICROSCOPE and epsilon_EOTWASH budgets | numeric or theorem-zero bounds on readout, source-profile, omitted DD channels, material tensor errors | THM3266_0 computes promoted bounds with explicit e1,e2 instead of zero-residual assumptions | law derived; numeric epsilons missing | false |
| CON3266_2_promotion_gate | two-channel WEP promotion row | all source lock clauses signed and residual budgets smaller than chosen tolerance | claim_allowed may become true only after validation proves no unsigned clauses remain | blocked for claim, not blocked for derivation | false |

## Claim Gates
| gate_id | gate | passed | reason | claim_allowed |
| --- | --- | --- | --- | --- |
| CG3266_0_exact_residual_law | residual-inclusive inversion theorem derived | true | A^{-1} propagation law is exact for two rows and explicit epsilons | false |
| CG3266_1_parent_source_lock | same parent D coordinates across arenas | false | requires parent action/source-map signature, not merely external DD phenomenology | false |
| CG3266_2_residual_budget | numeric residual budgets supplied | false | epsilon_MICROSCOPE and epsilon_EOTWASH are variables in the theorem, not sourced numbers yet | false |
| CG3266_3_local_GR | local GR/Newton/Maxwell promotion | false | WEP source-coupling lock is a local-sector gate, not the full local GR derivation | false |

## Decision
| decision_id | verdict | what_moved | best_next | fallback_next | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| DEC3266_0 | EXACT_PROMOTION_CONTRACT_DERIVED_NOT_SIGNED | The vague blocker became eta=A D+epsilon with exact A^{-1} residual propagation; cancellation is no longer hand-wavy. | try to derive CON3266_0 parent action/source-map signature directly from the MTS local matter action grammar | source numeric epsilon budgets and keep the result as a bounded two-channel WEP smoke branch | false |

## Next Target
| next_id | selected | target_doc | target_script | objective | guardrail | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| NEXT3266_0_3267 | primary | 3267-Y5-R2FR-parent-source-map-signature-for-DD-coordinates-under-AX1090.md | scripts/Y5_R2FR_3267_parent_source_map_signature_for_DD_coordinates.py | Attempt the actual derivation of the parent source map that makes D_hatm and D_e arena-independent MTS coordinates. | If the parent map introduces arena-specific scale factors, keep them explicit and do not promote the WEP branch. | false |

## Validation
| check_id | check | passed | detail |
| --- | --- | --- | --- |
| VAL3266_0_sources_exist | all cited source paths exist | true |  |
| VAL3266_1_sources_parse | all cited source paths parse | true |  |
| VAL3266_2_rank_input_true | 3265 rank-two input is true | true | rank_two=True |
| VAL3266_3_inverse_finite | inverse coefficients and residual gains are finite | true | all inverse coefficients finite |
| VAL3266_4_outputs_parse | all 3266 output CSVs parse | true |  |
| VAL3266_5_no_claim_promotion | no claim gate allows WEP/local-GR promotion | true | all claim_allowed=false |
| VAL3266_6_formalization_untouched | formalization-workbench modified-file count remains zero by this script | true | formalization_changed_count=0 |
| VAL3266_7_overall | 3266 validation overall | true | all required checks passed |

Generated UTC: 2026-06-27T06:25:18.848570+00:00
