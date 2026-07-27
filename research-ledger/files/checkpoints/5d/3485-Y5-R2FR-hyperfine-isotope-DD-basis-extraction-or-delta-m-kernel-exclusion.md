# 3485: Hyperfine/Isotope DD-Basis Extraction Or Delta-m Kernel Exclusion

## Current Verdict
- **Good news:** sourced hyperfine/isotope sensitivity rows can algebraically close the 3483 one-dimensional blind direction.
- **Important honesty guard:** these rows are average light-quark `X_q=m_q/Lambda_QCD` rows, not direct `D_delta_m_eff` rows.
- **Mechanism:** closure happens indirectly because the Earth DD source proxy has a small nonzero `Q_delta_m_Earth` component.
- **Risk:** the closure is ill-conditioned and remains nonclaim until `Q_delta_m_Earth` is parent-owned or a kernel-exclusion theorem is derived.
- **No claim:** no local-GR, WEP, Newton, source-coupling, or EM pass is claimed here.

## Basis Map Audit
| map_id | source_quantity | dd_basis_mapping | not_mapped_to | reason | claim_status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| MAP3485_0_Xq_to_D_hatm | X_q = m_q/Lambda_QCD | D_hatm_eff | D_delta_m_eff | X_q is the average light-quark mass over the QCD scale; D_delta_m_eff is the isospin-breaking up/down mass-difference channel. | SOURCE_BACKED_CONCEPTUAL_MAP_NONCLAIM_PARENT_MTS_MAP_MISSING | False |
| MAP3485_1_hyperfine_ratio | hyperfine ratio A/B from Dinh Table II | row = (Delta k_Xq, 0, 0, Delta Krel_alpha) | D_delta_m_eff; D_me_eff for same-class hyperfine ratios | the table gives alpha and average-quark-mass sensitivities; same hyperfine-class ratios cancel common electron/proton mass factor at this level. | SENSITIVITY_ROW_ONLY_NONCLAIM | False |
| MAP3485_2_isotope_ratio | same-element isotope hyperfine comparison | row = (Delta kappa_Xq, 0, 0, 0) | D_delta_m_eff | electron relativistic and alpha factors cancel for same element; source discusses average quark mass sensitivity of nuclear magnetic moments. | SENSITIVITY_ROW_ONLY_NONCLAIM | False |
| MAP3485_3_indirect_delta_closure | rank closure through Q_Earth | possible only because Q_delta_m_Earth != 0 in the bulk DD proxy | a direct hyperfine D_delta_m coefficient | new D_hatm rows separate average-quark direction from the tiny Earth Q_delta_m component, but the conditioning is poor and the parent Earth source map is not signed. | CONDITIONAL_NUMERIC_RANK_CLOSURE_NONCLAIM | False |

## Extracted Sensitivity Rows
| candidate_id | observable | extraction | D_hatm_eff | D_delta_m_eff | D_me_eff | D_e_eff | basis_status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DINH3485_0_Rb_over_Cs_hyperfine | 87Rb/133Cs hyperfine ratio | DeltaKrel=0.34-0.83=-0.49; Deltak=(-0.019)-0.002=-0.021 | -0.021 | 0.0 | 0.0 | -0.49 | AVERAGE_LIGHT_QUARK_MASS_Xq_ROW_NOT_ISOSPIN_DELTA_M | False |
| DINH3485_1_Yb_over_Cs_hyperfine | 171Yb+/133Cs hyperfine ratio | DeltaKrel=1.50-0.83=0.67; Deltak=(-0.099)-0.002=-0.101 | -0.101 | 0.0 | 0.0 | 0.67 | AVERAGE_LIGHT_QUARK_MASS_Xq_ROW_NOT_ISOSPIN_DELTA_M | False |
| DINH3485_2_Hg_over_Cs_hyperfine | 199Hg+/133Cs hyperfine ratio | DeltaKrel=2.28-0.83=1.45; Deltak=(-0.111)-0.002=-0.113 | -0.113 | 0.0 | 0.0 | 1.45 | AVERAGE_LIGHT_QUARK_MASS_Xq_ROW_NOT_ISOSPIN_DELTA_M | False |
| DINH3485_3_Cd_over_Cs_hyperfine | 111Cd+/133Cs hyperfine ratio | DeltaKrel=0.60-0.83=-0.23; Deltak=0.120-0.002=0.118 | 0.118 | 0.0 | 0.0 | -0.23 | AVERAGE_LIGHT_QUARK_MASS_Xq_ROW_NOT_ISOSPIN_DELTA_M | False |
| BFK3485_4_Yb_isotope_delta_kappa | 161Yb/169Yb hyperfine isotope comparison | same-element isotope comparison sensitivity quoted as delta kappa = 0.924 | 0.924 | 0.0 | 0.0 | 0.0 | ISOTOPE_AVERAGE_LIGHT_QUARK_MASS_ROW_NOT_ISOSPIN_DELTA_M | False |
| FT3485_5_Rb_over_Cs_continuity | 87Rb/133Cs hyperfine ratio continuity row | DeltaKrel=0.34-0.83=-0.49; Deltakappa=(-0.016)-0.009=-0.025 | -0.025 | 0.0 | 0.0 | -0.49 | OLDER_CONTINUITY_Xq_ROW_NOT_ISOSPIN_DELTA_M | False |

## Rank And Conditioning Ledger
| candidate_id | rank_if_added | closes_rank | projection_on_3483_blind | min_singular_value_after | condition_number_after | condition_flag | closure_mechanism | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DINH3485_0_Rb_over_Cs_hyperfine | 4 | True | 2.356652993841e-05 | 1.116083931040e-05 | 6.726186776036e+05 | ILL_CONDITIONED_PROXY_CLOSURE | indirect via nonzero Q_delta_m_Earth in Earth DD proxy | False |
| DINH3485_1_Yb_over_Cs_hyperfine | 4 | True | 8.204236198579e-05 | 3.466946324442e-05 | 2.169291603591e+05 | ILL_CONDITIONED_PROXY_CLOSURE | indirect via nonzero Q_delta_m_Earth in Earth DD proxy | False |
| DINH3485_2_Hg_over_Cs_hyperfine | 4 | True | 4.276284016226e-05 | 3.591773104593e-05 | 2.124210263680e+05 | ILL_CONDITIONED_PROXY_CLOSURE | indirect via nonzero Q_delta_m_Earth in Earth DD proxy | False |
| DINH3485_3_Cd_over_Cs_hyperfine | 4 | True | -2.512387788448e-04 | 3.669425974501e-05 | 2.042424341644e+05 | ILL_CONDITIONED_PROXY_CLOSURE | indirect via nonzero Q_delta_m_Earth in Earth DD proxy | False |
| BFK3485_4_Yb_isotope_delta_kappa | 4 | True | -5.503904639594e-04 | 4.431522265308e-05 | 1.690393478510e+05 | ILL_CONDITIONED_PROXY_CLOSURE | indirect via nonzero Q_delta_m_Earth in Earth DD proxy | False |
| FT3485_5_Rb_over_Cs_continuity | 4 | True | 2.804466855682e-05 | 1.311560457022e-05 | 5.723708658008e+05 | ILL_CONDITIONED_PROXY_CLOSURE | indirect via nonzero Q_delta_m_Earth in Earth DD proxy | False |

## Theorems
| theorem_id | statement | proof | result | valid_for_claim |
| --- | --- | --- | --- | --- |
| THM3485_0_Xq_rows_do_not_directly_probe_D_delta_m | The acquired hyperfine/isotope rows constrain average light-quark sensitivity X_q, not the isospin-breaking D_delta_m_eff channel directly. | Their source quantity is m_q/Lambda_QCD with m_q=(m_u+m_d)/2; no sourced coefficient for (m_d-m_u)/Lambda_QCD is present in these rows. | D_delta_m_eff entries are kept exactly zero for honest basis mapping. | False |
| THM3485_1_indirect_kernel_closure | Despite zero direct D_delta_m_eff coefficient, X_q rows can close the 3483 rank algebraically through the Earth source vector. | Q_Earth has a small nonzero Q_delta_m component; adding an independent D_hatm/X_q row separates the Earth source mixture from the clock rows. | closing candidates=6; best_condition_number=1.690393478510e+05 | False |
| THM3485_2_conditioning_guard | This is not yet a local-GR/source-coupling claim because the closure is condition-sensitive and depends on the parent status of Q_delta_m_Earth. | The smallest singular values are controlled by the tiny Q_delta_m_Earth component in a bulk DD proxy, not a parent-derived MTS source theorem. | next target must stabilize/source Q_delta_m_Earth or derive a parent lower-bound/kernel-exclusion theorem. | False |

## Decisions
| decision_id | decision | rationale | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- |
| DEC3485_0_basis_honesty | Do not relabel average quark-mass sensitivity as D_delta_m_eff. | that would be a basis error; all extracted rows have D_delta_m_eff=0. | False | False |
| DEC3485_1_kernel_status | The 3483 blind direction is algebraically closable, but only as a conditional proxy closure. | 6 sourced sensitivity rows close rank, but the closure uses nonzero Q_delta_m_Earth from the nonclaim Earth DD proxy. | False | False |
| DEC3485_2_best_next_attack | Stabilize the closure by deriving/sourcing the Earth Q_delta_m component and its uncertainty, or prove a parent kernel-exclusion theorem. | without that, the condition number can make the apparent closure fragile. | False | False |

## Next Target
| next_doc | next_script | objective | success_gate | forbidden_shortcuts | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| 3486-Y5-R2FR-earth-Qdelta-source-stability-or-parent-kernel-exclusion.md | scripts/Y5_R2FR_3486_earth_Qdelta_source_stability_or_parent_kernel_exclusion.py | Test whether the nonzero Earth Q_delta_m component is stable/source-owned enough to support the 3485 rank closure, or derive a parent theorem excluding the D_delta_m-like kernel. | Q_delta_m_Earth has source-backed uncertainty and parent transport status, or the parent action forbids Q_Earth dot C=0 along the 3483 blind vector | claiming local GR from ill-conditioned proxy rank; relabelling X_q as D_delta_m; using WEP linearly in the same-vector branch | False | False |

## Validation
| check_id | passed | detail | valid_for_claim |
| --- | --- | --- | --- |
| VAL3485_0_sources_exist | True | all local sources and PDFs exist | False |
| VAL3485_1_csv_parse | True | source_register:8; pdf_audit:3; basis_map:4; extracted_rows:6; rank_ledger:6; theorems:3; decisions:3; next_target:1 | False |
| VAL3485_2_basis_honesty | True | all extracted Xq rows keep D_delta_m_eff=0 | False |
| VAL3485_3_algebraic_rank_closure_exists | True | closing_rows=6 | False |
| VAL3485_4_condition_guard_present | True | rank closure is condition-guarded | False |
| VAL3485_5_no_claim | True | all generated rows valid_for_claim=false | False |
| VAL3485_6_no_formalization_outputs | True | outputs are under post-checkpoint-work/source-intake only | False |
| VAL3485_SUMMARY | True | PASS | False |

_Generated: 2026-06-29T04:16:11.897296+00:00_
