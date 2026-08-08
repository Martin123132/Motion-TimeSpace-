# 3287 - Chi-to-metric-Hodge premise proof or DeltaChi slope source row under AX1090

## Summary

3287 makes a real derivation step instead of circling the whole `chi` problem.

The Hodge **shape** is conditionally derivable:

1. A local bilinear EM action gives a reciprocal principal constitutive tensor and routes skewon/non-Lagrangian response into a residual.
2. If the reciprocal principal constitutive tensor has a repeated-quadratic Fresnel polynomial, equivalently a closure relation `kappa^2=-lambda^2 I` on 2-forms, it reconstructs a conformal EM metric class `[g_EM]`.
3. With positive energy/time orientation, the principal constitutive law becomes

`chi_principal = Z_Q *_(g_EM)`.

That is a useful partial win: the public Hodge form is not just inserted by hand.

But two hard gates remain:

- `g_EM` still has to be proven equal to the matter/clock/source public metric `g_pub`.
- `Z_Q` still has to be parent-owned/q-basic, or the scalar coupling/alpha/readout branch stays live.

So the honest residual is no longer a vague `Delta_chi`. It decomposes into skewon, birefringent principal, axion-gradient, impedance drift, metric-split, and radiative/readout pieces. Under the selected 3286 envelope:

`|C_R^(Delta chi)| <= 1.389797711495e-12`.

## Chi-To-Hodge Reconstruction Theorem
| theorem_id | claim_piece | status | payoff |
| --- | --- | --- | --- |
| CHR3287_0_action_to_reciprocal_chi | local bilinear EM action gives reciprocal principal chi | DERIVED_CONDITIONAL | CHS3106_1 and CHS3106_2 collapse into one parent Lagrangian-owner clause. |
| CHR3287_1_fresnel_to_conformal_metric | nonbirefringence reconstructs conformal metric | DERIVED_CONDITIONAL | CHS3106_3 derives the light-cone/conformal part of the public Hodge candidate. |
| CHR3287_2_closure_to_metric_Hodge | closure relation gives metric Hodge shape | DERIVED_CONDITIONAL | Hodge shape is no longer arbitrary; it follows from reciprocal nonbirefringent closure. |
| CHR3287_3_positivity_to_sign | positive energy fixes branch sign | DERIVED_CONDITIONAL | CHS3106_4 is a physical branch selector, not a new free function. |
| CHR3287_4_axion_and_impedance_residual | Hodge shape does not fix scalar coupling or axion/readout drift | DERIVED_OBSTRUCTION | the missing coupling is specifically scalar impedance/gauge norm/readout ownership, not the whole Hodge tensor. |
| CHR3287_5_same_metric_obstruction | EM metric is not automatically matter/clock metric | DERIVED_OBSTRUCTION | local GR needs same-metric identification, not merely EM nonbirefringence. |
| CHR3287_6_vertical_zero_after_reconstruction | q-basic reconstructed Hodge gives vertical silence | EXACT_CONDITIONAL_NOT_PARENT_SIGNED | C_H=C_S=0 becomes a conditional theorem after the remaining scalar/same-metric/readout clauses are signed. |

## Premise Collapse Matrix
| collapse_id | old_premises | new_gate | derived_here | remaining_gap | blocks_claim |
| --- | --- | --- | --- | --- | --- |
| PCM3287_0_lagrangian_owner | CHS3106_0_local_linear + CHS3106_1_reciprocal + CHS3106_2_no_skewon | parent EM sector is a local bilinear action coefficient before readout | partly | parent action must actually supply this coefficient and exclude non-Lagrangian/skewon medium response. | true |
| PCM3287_1_fresnel_closure | CHS3106_3_nonbirefringent | reciprocal principal chi has repeated-quadratic Fresnel polynomial or closure kappa^2=-lambda^2 I | theorem_form | MTS parent variables must force this closure rather than fit it after observation. | true |
| PCM3287_2_energy_branch | CHS3106_4_positive_energy | choose positive Z_Q/time orientation branch | branch_selector | source sign and local observer convention must match matter/coframe sector. | true |
| PCM3287_3_scalar_impedance_owner | CHS3106_5_impedance_owner | Z_Q is q-basic/fixed parent gauge norm, not a hidden scalar or independent F^2 counterterm | not_derived | 1100/1056 retain gauge norm, no-extra-F2, current owner, and readout/radiative guard as unsigned. | true |
| PCM3287_4_same_public_metric | CHS3106_6_same_public_metric | g_EM reconstructed from light equals the matter/clock/source public metric | not_derived_by_EM_alone | requires cross-sector equivalence/coframe action-domain theorem. | true |
| PCM3287_5_readout_radiative_guard | CHS3106_7_radiative_readout | effective/readout reductions preserve q-basic Z_Q, Hodge star, hbar*c, and no independent f(Xhat)F^2 | not_derived | readout functor and radiative operator-domain closure remain needed. | true |

## Delta Chi Residual Decomposition
| residual_id | term | effect | repair_or_bound | status |
| --- | --- | --- | --- | --- |
| DCR3287_0_skewon | Delta_chi_skewon | dissipation, preferred-frame leakage, non-Hilbert stress | derive parent local bilinear action or bound skewon response | ROUTED_TO_LAGRANGIAN_GATE |
| DCR3287_1_birefringent_principal | Delta_chi_biref | polarization/lightcone split and nonmetric Hodge failure | prove closure kappa^2=-lambda^2 I or source birefringence bound | ROUTED_TO_FRESNEL_GATE |
| DCR3287_2_axion_gradient | Delta_chi_axion | magnetoelectric rotation/source exchange without setting ordinary stress scale | prove constant/q-basic axion or source axion-gradient bound | LIVE_FINITE_RESIDUAL |
| DCR3287_3_impedance_drift | Delta_Z_Q *F | alpha/clock/WEP/source-coupling branch reopens | derive q-basic gauge norm/no-extra-F2/readout guard or keep finite alpha product route | LIVE_COUPLING_BOTTLENECK |
| DCR3287_4_metric_split | Z_Q(*_{g_EM}-*_{g_pub})F | local GR same-source limit fails or becomes bimetric | prove same-public-metric theorem or route to optical-metric residual tests | LIVE_LOCAL_GR_BOTTLENECK |
| DCR3287_5_radiative_readout | Delta_chi_rad/readout | tree-level Hodge silence does not survive measured alpha/EM standards | derive public readout functor/radiative closure or keep readout residual | LIVE_READOUT_BOTTLENECK |

## Delta Chi Slope Rows
| row_id | prediction | abs_bound | source_status | result | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| DCS3287_0_reconstruction_zero_conditional | 0 | 1.389797711495e-12 | THEOREM_CONDITIONAL_AFTER_REMAINING_GATES | PASS_NUMERIC_NONCLAIM | false |
| DCS3287_1_skewon_biref_residual | Pi_SB[L_v(Delta_chi_skewon+Delta_chi_biref)]/N_SB | 1.389797711495e-12 | MISSING_NUMERIC_SKEWON_BIREF_PROJECTION | REFUSE_MISSING_SOURCE_NONCLAIM | false |
| DCS3287_2_impedance_metric_readout_residual | n_Z*L_v ln Z_Q + Pi_g[L_v(g_EM-g_pub)]/N_g + Pi_rad[L_v Delta_chi_rad]/N_rad | 1.389797711495e-12 | MISSING_NUMERIC_ZQ_METRIC_READOUT_PROJECTION | REFUSE_MISSING_SOURCE_NONCLAIM | false |
| DCS3287_3_half_bound_smoke | 6.948988557475e-13 | 1.389797711495e-12 | SMOKE_ONLY | SMOKE | false |
| DCS3287_4_twice_bound_smoke | 2.779595422990e-12 | 1.389797711495e-12 | SMOKE_ONLY | SMOKE | false |

## Delta Chi Bound Runner
| row_id | prediction | prediction_over_bound | result | expectation_met | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| DCS3287_0_reconstruction_zero_conditional | 0 | 0.000000000000e+00 | PASS_NUMERIC_NONCLAIM | true | false |
| DCS3287_1_skewon_biref_residual | Pi_SB[L_v(Delta_chi_skewon+Delta_chi_biref)]/N_SB | N/A | REFUSE_MISSING_SOURCE_NONCLAIM | true | false |
| DCS3287_2_impedance_metric_readout_residual | n_Z*L_v ln Z_Q + Pi_g[L_v(g_EM-g_pub)]/N_g + Pi_rad[L_v Delta_chi_rad]/N_rad | N/A | REFUSE_MISSING_SOURCE_NONCLAIM | true | false |
| DCS3287_3_half_bound_smoke | 6.948988557475e-13 | 5.000000000000e-01 | PASS_NUMERIC_NONCLAIM | true | false |
| DCS3287_4_twice_bound_smoke | 2.779595422990e-12 | 2.000000000000e+00 | FAIL_BOUND | true | false |

## Promotion Gates
| gate_id | passed | claim_allowed | detail |
| --- | --- | --- | --- |
| GATE3287_0_hodge_shape_conditional | true | false | reciprocal nonbirefringent closure derives metric-Hodge shape up to scalar/axion/same-metric/readout clauses. |
| GATE3287_1_premises_collapsed | true | false | CHS3106_0..7 collapse into fewer sharper gates: Lagrangian owner, Fresnel closure, positive branch, scalar owner, same metric, readout guard. |
| GATE3287_2_scalar_impedance_signed | false | false | Z_Q/gauge norm/no-extra-F2/readout closure remain unsigned in 1100/1056. |
| GATE3287_3_same_public_metric_signed | false | false | EM Fresnel metric is not yet proven identical to matter/clock/source public metric. |
| GATE3287_4_numeric_residual_sourced | false | false | no source-backed Delta_chi projection row exists for skewon, birefringence, impedance, metric split, or readout. |
| GATE3287_5_no_claim | true | false | no local-GR/Maxwell/alpha/PPN/clock claim is allowed from this checkpoint. |

## Decisions
| decision_id | decision | why_it_moves_forward | claim_allowed |
| --- | --- | --- | --- |
| DEC3287_0_partial_win | The Hodge tensor shape is conditionally derivable from local reciprocal nonbirefringent EM closure. | this removes much of the vague Hodge gap and turns it into standard closure geometry rather than a guessed motion-field insert. | false |
| DEC3287_1_coupling_bottleneck | The continuous coupling/impedance Z_Q is still the live missing owner. | it matches the user's coupling instinct: the shape can be derived, but the scalar normalization and readout descent still decide alpha/source coupling. | false |
| DEC3287_2_same_metric_bottleneck | EM nonbirefringence gives g_EM, not automatically the matter/clock/source g_pub. | local GR requires same-source stress in one public metric, so the next proof cannot hide behind light cones alone. | false |
| DEC3287_3_next_work | Next attack should split scalar Z_Q ownership from same-public-metric identification and try the least costly proof first. | the remaining route is now two explicit gates instead of a blob called chi. | false |

## Next Target
| next_id | target_doc | objective | guardrail |
| --- | --- | --- | --- |
| NEXT3287_0_3288 | 3288-Y5-R2FR-same-public-metric-or-ZQ-impedance-owner-split-under-AX1090.md | Use the 3287 split to attack the two remaining gates separately: prove g_EM=g_pub from cross-sector coframe/equivalence/Ward ownership, and prove or demote q-basic Z_Q from gauge norm/no-extra-F2/readout closure; if either fails, produce finite residual rows rather than a closure claim. | Do not claim Maxwell/local-GR or alpha silence from Hodge shape alone; do not mix scalar impedance with metric identification; no Poynting double-counting. |

## Validation
| check_id | check | passed | detail |
| --- | --- | --- | --- |
| VAL3287_0_sources_exist | all cited source paths exist | true |  |
| VAL3287_1_sources_parse | all cited source paths parse | true |  |
| VAL3287_2_outputs_parse | all 3287 non-validation output CSVs parse | true | non-validation outputs parsed before validation write |
| VAL3287_3_reconstruction_theorem_present | reconstruction theorem includes Fresnel closure and Hodge shape | true |  |
| VAL3287_4_coupling_obstruction_present | scalar impedance and same-metric obstructions are explicit | true |  |
| VAL3287_5_premise_collapse_sharpens_stack | CHS premise stack is collapsed into sharper gates | true |  |
| VAL3287_6_residual_decomposition_complete | Delta_chi residuals cover skewon, birefringence, axion, impedance, metric split, and readout | true |  |
| VAL3287_7_runner_expectations | Delta_chi runner expectations all match | true | DCS3287_0_reconstruction_zero_conditional=PASS_NUMERIC_NONCLAIM;DCS3287_1_skewon_biref_residual=REFUSE_MISSING_SOURCE_NONCLAIM;DCS3287_2_impedance_metric_readout_residual=REFUSE_MISSING_SOURCE_NONCLAIM;DCS3287_3_half_bound_smoke=PASS_NUMERIC_NONCLAIM;DCS3287_4_twice_bound_smoke=FAIL_BOUND |
| VAL3287_8_claim_gates_false | no 3287 gate allows local-GR/alpha/Maxwell claim | true |  |
| VAL3287_9_next_target_focused | next target splits same metric and Z_Q owner | true |  |
| VAL3287_10_formalization_untouched | formalization-workbench modified-file count remains zero by this script | true | formalization_changed_count=0 |
| VAL3287_11_overall | 3287 validation overall | true | all required checks passed |

Generated UTC: 2026-06-27T16:40:25.782148+00:00
