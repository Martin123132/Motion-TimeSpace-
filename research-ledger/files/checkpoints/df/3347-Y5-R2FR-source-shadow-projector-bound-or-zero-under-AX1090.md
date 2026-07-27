# 3347 — Source-Shadow Projector Bound Or Zero Under AX1090

Generated: `2026-06-28T03:01:36.001262+00:00`

## Summary
- This checkpoint attacks the source-shadow/projector gap directly, not merely by naming it.
- The clean theorem is: if the parent action admits no post-variation source map, then `T_active=T_H`; any universal common mode is absorbed into measured `G_N`.
- Any nonidentity source map is forced into a trichotomy: real variational action content, boundary/improvement silence, separately conserved residual block, or observable relative projector.
- Current MTS still cannot claim `epsilon_source_shadow=0`, but it now has a finite nonclaim MICROSCOPE Ti/Pt smoke bound and a precise next derivation target: the material response basis `R_AB`.

## Source-Shadow Normal Form
| form_id | object | mathematical_form | interpretation | effect_after_G_calibration | status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| SSF3347_0_identity | identity source map | T_active = T_H := (-2/sqrt(-g_obs)) delta(S_matter+S_EM)/delta g_obs | the active local source is exactly the Hilbert/Noether source of the same action that defines ordinary dynamics | ordinary Newtonian source normalization is one measured constant G_N | EXACT_CONDITIONAL_IF_PARENT_ARGS_SIGNED | false |
| SSF3347_1_projector_decomposition | candidate source projector | P_src = I + C_0 I + Pi_rel, so T_active=(1+C_0)T_H + Pi_rel(T_H) | C_0 is a universal common mode; Pi_rel is the dangerous composition/source-shadow part | C_0 is absorbed into measured G_N; Pi_rel survives as WEP/source-composition residual | DERIVED_LOCAL_DECOMPOSITION | false |
| SSF3347_2_epsilon_definition | epsilon_source_shadow | epsilon_source_shadow := \|\|Pi_rel(T_H)\|\|_arena / \|\|T_H\|\|_arena | finite residual measuring nonidentity source projector leakage after common-mode calibration | bounded by differential acceleration/source-composition channels, not by a single Cavendish G value | BOUND_INTERFACE_DEFINED | false |

## Zero Theorem Attempt
| theorem_id | claim | derivation | proof_status | blocker | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| Z3347_0_statement | epsilon_source_shadow = 0 | If Args(S_parent) admits only q-visible geometry, ordinary fields, public EM/current, fixed constants, and classified boundary terms, then no post-variation P_src or F_shadow is typed. | EXACT_CONDITIONAL_THEOREM | 3346 normal form is a candidate inventory, not a parent-signed field-by-field syntax certificate | false |
| Z3347_1_variational_case | a variational shadow is not hidden | If DeltaT_shadow = (-2/sqrt(-g)) delta(DeltaS)/delta g_obs, then DeltaS is a real parent action term and must be listed as matter, EM, geometry, or boundary/improvement content. | DERIVED_RECLASSIFICATION | requires field-by-field parent action inventory to show no such DeltaS remains unlisted | false |
| Z3347_2_nonvariational_case | a nonvariational shadow is rejected or bounded | Bianchi/Noether gives nabla_mu E^{mu nu}=0 and matter EOM give nabla_mu T_H^{mu nu}=0, so an inserted J_shadow must be conserved by itself; then it is boundary/improvement silence or a separately conserved residual block. | DERIVED_FILTER | decoupled conserved blocks and boundary falloff are not fully arena-signed | false |
| Z3347_3_common_mode | a universal source rescaling is not a local-GR residual | T_active=(1+C_0)T_H gives kappa_eff=kappa(1+C_0); Newtonian calibration measures G_N proportional to kappa_eff, so C_0 disappears from local differential/source-shape tests. | DERIVED_ABSORPTION | only the relative projector Pi_rel is bounded here; global/cosmological calibration is a separate branch | false |
| Z3347_4_current_verdict | current MTS source-shadow zero | The no-projector theorem is strong enough as a parent-action contract, but current files do not yet sign every no-shadow/no-boundary/no-decoupled-block clause. | NOT_PROMOTED_TO_MTS_ZERO | carry epsilon_source_shadow as explicit finite residual until 3347/3347b clauses close | false |

## Shadow Trichotomy Decision
| case_id | candidate | classification | action | survives_as_residual | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| TRI3347_0_identity | P_src = I + C_0 I | identity plus measured-G common mode | absorb C_0 into G_N; no WEP/source-composition residual | false | false |
| TRI3347_1_variational | P_src(T_H)-T_H = delta DeltaS/delta g_obs | real action content | move DeltaS into parent action inventory or forbid it by Args(S_parent) | true_until_parent_inventory_closes | false |
| TRI3347_2_boundary | J_shadow = nabla_alpha U^{alpha mu nu} | boundary/improvement | zero under signed local falloff/no-flux condition, otherwise bound boundary contact residual | true_until_boundary_signed | false |
| TRI3347_3_nonvariational | J_shadow inserted into RHS without DeltaS | Bianchi-inconsistent unless separately conserved | reject as parent field theory or classify as decoupled residual block | true_if_separately_conserved_block_exists | false |
| TRI3347_4_relative_projector | Pi_rel(T_H) labelled by material/species/source composition | observable source-shadow leakage | bound epsilon_source_shadow using WEP/source-composition tests with no-cancellation guard | true_until_zero_or_bound_promoted | false |

## Local Newtonian Projection
| projection_id | weak_field_form | source_shadow_form | after_calibration | observable_residual | status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| NEW3347_0_field_equation | nabla^2 Phi_N = 4 pi G_* [rho_H + rho_shadow] | rho_shadow = C_0 rho_H + Pi_rel(rho_H) | G_N = G_*(1+C_0) for a universal common mode | Pi_rel only | DERIVED_PROJECTION | false |
| NEW3347_1_eotvos_channel | eta_AB ~= epsilon_source_shadow * R_AB for a differential material response R_AB | R_AB is the response of the test/source materials to Pi_rel | common Earth/source acceleration and common G_N cancel in eta_AB | \|epsilon_source_shadow\| <= \|eta_AB\|/\|R_AB\| | BOUND_FORMULA_DERIVED | false |
| NEW3347_2_no_cancellation | epsilon_budget >= sum_i \|epsilon_i R_i\| unless parent theorem proves cancellations | absolute component accounting | do not hide opposite signs across material channels | conservative private bound rows | NO_CANCELLATION_GUARD | false |

## Epsilon Source-Shadow Bound Rows
| bound_id | symbol | observable | bound_formula | response_factor | epsilon_bound | units | source_path | source_url | arena | extraction_method | valid_for_component_bound | valid_for_claim | claim_blocker |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BND3347_0_MICROSCOPE_TiPt_unit_response | epsilon_source_shadow | eta_TiPt | \|epsilon_source_shadow\| <= \|eta_TiPt\| / \|R_TiPt\| | 1.000000e+00 | 4.245906e-15 | dimensionless_projector_fraction | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3342_WEP_BOUND_ROWS.csv | https://link.aps.org/doi/10.1103/PhysRevLett.129.121102 | WEP_TiPt_MICROSCOPE | inherited from 3342 eta_species MICROSCOPE component row; unit response smoke only | true | false | R_TiPt is not derived from MTS source-shadow basis; only one WEP material channel is staged |
| BND3347_1_common_mode_absorbed | C_0 | measured_G_N | G_N = G_* (1+C_0) | universal | absorbed_not_WEP_bound | dimensionless_common_mode | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3339_MEASURED_G_ABSORPTION_THEOREM.csv | local_corpus | local_Newtonian_calibration | derived common-mode calibration identity | true | false | common source normalization is not a local differential residual but may matter for global calibration branches |

## Promotion Gates
| gate_id | claim | passed | reason | valid_for_claim |
| --- | --- | --- | --- | --- |
| GATE3347_0_zero_theorem_shape | source-shadow/projector zero theorem has an exact conditional proof | true | identity-source, variational reclassification, Bianchi filter, and common-mode absorption are explicit | false |
| GATE3347_1_parent_signed_zero | epsilon_source_shadow=0 is parent-signed for current MTS | false | 3346 normal form is not a closed field-by-field parent action certificate | false |
| GATE3347_2_finite_bound_staged | finite epsilon_source_shadow component bound is staged | true | MICROSCOPE Ti/Pt unit-response smoke row gives a dimensionless nonclaim component bound | false |
| GATE3347_3_local_GR_claim | local GR/Newton calibrated source-coupling branch is claim-ready | false | source-shadow zero is not parent-signed and material response basis is not derived | false |

## Decision Ledger
| decision_id | question | answer | reason | next_action | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| DEC3347_0 | Did 3347 prove away source projectors for current MTS? | no | the theorem is exact as a parent-action contract, but current MTS has not signed the no-projector/no-boundary/no-decoupled-block clauses | derive the material/source response basis R_AB or close the parent inventory clauses directly | false |
| DEC3347_1 | Did 3347 move the source-coupling problem forward? | yes | it reduces source-shadow freedom to identity/common-mode, variational parent content, boundary/improvement, decoupled block, or a bounded relative projector | attack R_AB/material charge basis before adding more empirical channels | false |

## Next Target
| target_id | target_script | objective | why_next | valid_for_claim |
| --- | --- | --- | --- | --- |
| 3348-Y5-R2FR-source-shadow-response-basis-or-zero-under-AX1090.md | scripts/Y5_R2FR_3348_source_shadow_response_basis_or_zero.py | derive the material/source response basis R_AB for epsilon_source_shadow from Hilbert/Noether matter content, or prove R_AB has no independent ordinary slot | the finite WEP bound exists but cannot become a serious local-GR bound until R_AB is derived rather than set to unit smoke response | false |
| 3347b-Y5-R2FR-coefficient-domain-field-by-field-certificate.md | scripts/Y5_R2FR_3347b_coefficient_domain_field_by_field_certificate.py | parallel route: field-by-field certificate for epsilon_coeff_domain and hidden coefficients | prevents hidden coefficient maps from recreating the source-shadow response through clocks, charges, masses, or frames | false |
