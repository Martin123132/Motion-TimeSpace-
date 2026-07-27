# 3523 - Source Label Forgetting Functor And EM Hodge Owner Or Marker Kernel Bound

## Summary
- **Coupling result:** the clean route is now explicit. MTS gets universal source coupling only if a parent functor forgets source/representative labels before Hilbert variation.
- **Matter theorem target:** `F_src` must map labelled matter/source bundles to public matter fields plus fixed representation constants, with no `w_A(X)`, `c_A(X)`, source masks or shadow frames.
- **EM theorem target:** `F_EM` must own Hodge star, gauge normalization `Z_EM`, charge generator/lattice and current normalization through `q(Phi)` or fixed representation data.
- **Poynting placement:** Poynting is not an extra hidden force in the local branch; when `F_EM` closes it is the flux of Maxwell Hilbert stress. If Hodge or `Z_EM` leaks, Poynting becomes a residual channel.
- **Current verdict:** exact conditional route, not live claim. The missing object is now shared observed-stack plus charge/gauge owner, not another broad mystery.

## Core Contract
The parent action must have the local quotient-coupled form

`S_parent = S_geom[Phi] + sum_A S_A[psi_A; Q_pub(Phi), theta_A] - 1/4 int mu_g(Q_pub) Z_EM(Q_pub,theta_Q) F^2 + S_boundary[Q_pub]`

where `Q_pub=q(Phi)` owns the metric/coframe, derivative, clock, source scale, Hodge star and EM normalization before readout. Source labels may appear only as fixed representation constants `theta_A`, not as source-dependent bulk weights or current rescalings.

## Source Register
| source_id | path | exists | role | valid_for_claim |
| --- | --- | --- | --- | --- |
| script_3523 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\scripts\Y5_R2FR_3523_source_label_forgetting_functor_and_EM_Hodge_owner_or_marker_kernel_bound.py | True | 3523 generator | False |
| doc_3522 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3522-Y5-R2FR-representative-identity-vs-global-symmetry-or-active-marker-bound.md | True | representative identity vs symmetry handoff | False |
| next_3522 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3522_NEXT_TARGET.csv | True | 3522-selected source-label/EM-Hodge target | False |
| status_3522 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_EM_representative_identity_status.csv | True | canonical representative identity status | False |
| matter_2587 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\2587-Y5-R2FR-minimal-parent-matter-coupling-action-or-domain-motion-input.md | True | minimal parent matter action, single observed stack, no-source-slot contract | False |
| matter_contract_2587 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_MIN_PARENT_MATTER_2587_ACTION_CONTRACT.csv | True | 2587 matter action contract rows | False |
| sort_constructor_2688 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\2688-Y5-R2FR-parent-sort-constructor-from-MTS-primitives-or-delta-w-component-values.md | True | source-label forgetting and Delta_w constructor blocker | False |
| vertical_poynting_3115 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3115-Y5-R2FR-local-vertical-Noether-generator-certificate-under-AX1090.md | True | EM/Hodge/Poynting readout and Hilbert-stress route | False |
| em_owner_1099 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1099-Y5-R10-unique-EM-kinetic-owner-no-extra-F2-theorem-or-alpha-coefficient-source-row.md | True | no-extra-F2/gauge-normalization owner and alpha residual guard | False |
| em_theorem_1099 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1099_EM_KINETIC_OWNER_THEOREM_ATTEMPT.csv | True | 1099 EM kinetic owner theorem attempt | False |
| alpha_rows_1099 | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1099_ALPHA_COEFFICIENT_SOURCE_ROWS_NONCLAIM.csv | True | 1099 alpha coefficient source rows | False |

## Toy Kernel Runner
| test_id | channel | toy_quantity | state_value | relabelled_value | residual | expected_result | meaning | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TK3523_0_common_source_weight | matter_source_weight | sum_A w_common h_A^2 | 30 | 30 | 0 | zero_if_common_mode | common source normalization forgets labels in the toy model | False |
| TK3523_1_source_label_weight | matter_source_weight | sum_A w_A h_A^2 with fixed source weights | 32.5 | 30.1 | 2.4 | nonzero_if_fixed_source_label_survives | source-label coefficients reopen representative dependence | False |
| TK3523_2_EM_gauge_norm_marker | EM_gauge_normalization | delta log Z_EM = beta deltaX | 0 | 0.006 | 0.006 | nonzero_if_hidden_EM_marker_survives | a hidden marker in Z_EM creates alpha/Hodge/Poynting residual pressure | False |
| TK3523_3_public_Poynting_Hilbert_route | EM_Hilbert_stress | S^a=-h^a_mu T_EM^{mu nu} u_nu | defined_from_T_EM | same_if_T_EM_q_owned | 0_if_Hodge_ZEM_q_owned_else_epsilon_EM | Poynting_is_not_extra_source | Poynting belongs to public Maxwell Hilbert stress when Hodge and Z_EM descend through q | False |

## Functor Contract
| clause_id | object | required_statement | derivation_if_signed | current_status | blocks_if_missing | source_path | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| FC3523_0_parent_observed_stack | Q_pub=q(Phi) | The observed stack used by matter and EM is Q_pub=(g_pub/e_obs,D_obs,A_obs,tau,ell_J,Hodge) and is parent-owned before readout/fitting. | All ordinary matter and EM actions can be written on public quotient objects rather than representative labels. | CONTRACT_AVAILABLE_NOT_PARENT_SIGNED | q_stack, tau/ell_J, Hodge and current normalization residuals | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\2587-Y5-R2FR-minimal-parent-matter-coupling-action-or-domain-motion-input.md | False |
| FC3523_1_source_label_forgetting_functor | F_src: Matter_parent -> Matter_public | F_src maps labelled source/matter bundles to public matter fields plus fixed representation constants theta_A; no spacetime/source-dependent label weight survives. | S_matter=sum_A S_A[psi_A;Q_pub,theta_A] has one Hilbert variation and J_H=q^*Jbar_H. | FUNCTOR_OWNER_NOT_DERIVED | Delta_w_label, c_A current rescale, shadow source frame | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\2688-Y5-R2FR-parent-sort-constructor-from-MTS-primitives-or-delta-w-component-values.md | False |
| FC3523_2_no_source_only_slot | forbidden morphisms | Hom_parent(SourceLabel/Marker/Readout, Coeff_active_source)=empty_or_common_mode before variation. | w_A(X), c_A(X), source masks and shadow frames are not legal bulk parent terms. | NOHOM_EXACT_CONDITIONAL_ONLY | source-dependent Newton/WEP/PPN/clock/orbital residuals | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\2587-Y5-R2FR-minimal-parent-matter-coupling-action-or-domain-motion-input.md | False |
| FC3523_3_EM_Hodge_owner_functor | F_EM: Q_pub -> (*_q,Z_EM,T_Q) | The Hodge star, gauge norm Z_EM, charge generator/lattice and current normalization are functions of q(Phi) or fixed representation data, not hidden/private labels. | S_EM=-1/4 int mu_g Z_EM F^2 gives Maxwell Hilbert stress and no standalone alpha/Hodge/Poynting marker. | EM_OWNER_NOT_SIGNED | b_alpha, delta_Hodge, constitutive tensor, Poynting/source residual | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\1099-Y5-R10-unique-EM-kinetic-owner-no-extra-F2-theorem-or-alpha-coefficient-source-row.md | False |
| FC3523_4_variation_before_readout | Hilbert/Maxwell variation order | Functional derivatives are taken on the parent/public quotient action before support fitting, local calibration, arena projection or material readout. | prevents fitted GM, post-readout current changes and external Poynting masks from manufacturing source coupling. | WORKFLOW_CONTRACT_NOT_PARENT_THEOREM | domain-motion, support, boundary and calibration residuals | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\2587-Y5-R2FR-minimal-parent-matter-coupling-action-or-domain-motion-input.md | False |

## Derivations And Counterterms
| derivation_id | statement | derivation | consequence | current_status | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| DER3523_0_matter_source_descent | If FC3523_0 through FC3523_2 and FC3523_4 hold, then source labels are forgotten before Hilbert variation. | With S_matter=sum_A S_A[psi_A;Q_pub,theta_A], variation gives T_H=sum_A delta S_A/delta Q_pub. Because label A appears only as fixed representation data theta_A and not as w_A(X), c_A(X) or a shadow frame, no vertical representative/source-label derivative contributes except common-mode normalization. | J_H=q^*Jbar_H conditionally; Delta_w_label and epsilon_source_slot theorem-zero if the parent functor is signed. | EXACT_CONDITIONAL_NOT_LIVE_CLAIM | False |
| DER3523_1_source_label_counterterm | If a fixed source weight survives, representative identity fails in the source sector. | A term sum_A w_A(X)S_A is invariant only under simultaneous transformation of the physical source weights. With fixed labelled weights, relabelling the representative changes the source action by Delta S=sum_A w_A(S_A(pi.h)-S_A(h)), as TK3523_1 demonstrates. | Delta_w_label must be zero by theorem or carried into WEP/R10/PPN/clock/orbital kernels. | COUNTERTERM_RETAINED_AS_NONCLAIM_BOUND | False |
| DER3523_2_public_Maxwell_Poynting_lock | If FC3523_3 holds, Poynting flux is part of public Maxwell Hilbert stress, not an extra source coupling. | For S_EM=-1/4 int mu_g Z_EM F_{mu nu}F^{mu nu}, metric variation gives T_EM^{mu nu}=Z_EM(F^mu_alpha F^{nu alpha}-1/4 g_pub^{mu nu}F^2). An observer Poynting vector is S^a=-h^a_mu T_EM^{mu nu}u_nu. Thus Poynting is already in the Hilbert source when g_pub, Hodge star and Z_EM are q-owned. | EM source coupling can reduce to GR Hilbert stress if Hodge/Z_EM/current normalization are quotient-owned. | EXACT_PUBLIC_ROUTE_CONDITIONAL | False |
| DER3523_3_EM_hidden_marker_counterterm | Gauge invariance alone does not kill hidden EM markers. | A term f_X(X_private)F^2 is covariant and U(1)-gauge invariant. Unless f_X is constant, sequestered, or q-owned, L_v log Z_EM produces alpha/clock/WEP/R10 and Poynting/source residuals. | No-extra-F2 or parent T_Q/gauge-norm owner must be signed; otherwise b_alpha and epsilon_EM remain finite. | COUNTERTERM_RETAINED_AS_NONCLAIM_BOUND | False |

## Promotion Gates
| gate_id | gate | pass_condition | current_evidence | passed | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| G3523_0_Qpub_owner | single observed stack owner | q(Phi), e_obs/g_pub, D_obs, A_obs, tau, ell_J and Hodge are parent-owned before readout | 2587 writes the contract; parent signature remains missing | False | False |
| G3523_1_Fsrc_owner | source-label forgetting functor | F_src exists and excludes source-only weights/current rescalings/shadow frames | 2688 identifies this as missing hinge | False | False |
| G3523_2_EM_owner | EM Hodge/gauge norm owner | Hodge star, Z_EM, T_Q/charge lattice and current normalization are q-owned or fixed representation data | 1099 no-extra-F2 theorem is conditional; 3115 Poynting route is conditional | False | False |
| G3523_3_variation_order | variation before readout/calibration | Hilbert and Maxwell variation occur before support fitting, arena kernels, local GM calibration or Poynting readout | workflow contract exists in 2587 but is not parent theorem | False | False |
| G3523_4_total | coupling owner closes | G3523_0 through G3523_3 pass together | no source signs all matter and EM owner clauses | False | False |

## Marker Kernel Bounds
| kernel_id | channel | symbol | formula | needed_inputs | units | source_path | current_status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| KB3523_0_Delta_w_label | matter/source-label | Delta_w_label | Delta_w_label = P_perp w_source or 0 from signed F_src | source composition vector, common-mode projector, parent source-label forgetting theorem, arena kernels | dimensionless | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\2688-Y5-R2FR-parent-sort-constructor-from-MTS-primitives-or-delta-w-component-values.md | MISSING_Fsrc_OR_NUMERIC_VALUES | False |
| KB3523_1_epsilon_J | Hilbert current normalization | epsilon_J | epsilon_J <= \|\|c_A-c_common\|\| \|\|J_A\|\| + support/boundary/jump terms | ell_J owner, current normalization theorem, support/jump ledger, source map | source_current_norm | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\2587-Y5-R2FR-minimal-parent-matter-coupling-action-or-domain-motion-input.md | MISSING_CURRENT_OWNER_OR_BOUND | False |
| KB3523_2_b_alpha | EM gauge normalization | b_alpha | b_alpha = L_v log Z_EM or 0 from no-extra-F2/T_Q owner | T_Q owner, charge lattice, gauge norm, radiative/readout alpha map | dimensionless vertical derivative | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R10_1099_ALPHA_COEFFICIENT_SOURCE_ROWS_NONCLAIM.csv | MISSING_EM_OWNER_OR_STANDALONE_BOUND | False |
| KB3523_3_delta_Hodge_constitutive | EM Hodge/constitutive readout | delta_star_chi | \|\|L_v *g\|\| + \|\|L_v chi_constitutive\|\| | public metric/Hodge owner, constitutive tensor owner, clock/spectral projection | operator_norm | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3115-Y5-R2FR-local-vertical-Noether-generator-certificate-under-AX1090.md | MISSING_HODGE_CONSTITUTIVE_OWNER | False |
| KB3523_4_Poynting_source_projection | Poynting/Hilbert source projection | epsilon_Poynting | epsilon_Poynting = \|\|D[-h T_EM u][v]\|\| with T_EM from q-owned Maxwell action, else finite kernel | observer field, source support, EM stress map, Hodge/Z_EM owner, arena projection | stress_flux_norm | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\3115-Y5-R2FR-local-vertical-Noether-generator-certificate-under-AX1090.md | MISSING_POYNTING_PROJECTION_KERNEL | False |

## Canonical Status
| status_id | quantity | value | meaning | claim_effect | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| STAT3523_0_matter_functor_route | source_label_forgetting_functor | exact_conditional_contract | a signed F_src would remove source labels before Hilbert variation and conditionally produce universal source current | route to GR/Newton source coupling sharpened | False |
| STAT3523_1_EM_Poynting_route | Poynting_as_Maxwell_Hilbert_stress | exact_conditional_derivation | Poynting is not an extra source if Hodge/Z_EM/current normalization are q-owned | Maxwell/EM route tied to GR source stress | False |
| STAT3523_2_live_coupling_owner | coupling_owner_parent_signed_by_current_MTS | False | Q_pub owner, F_src, EM Hodge/gauge owner and variation-order theorem are not signed together | no local-GR/Newton/Maxwell/source-coupling claim | False |
| STAT3523_3_next_best | next_best_attack | observed_stack_and_charge_lattice_owner | the next smallest parent object is the shared observed stack plus EM charge/gauge norm owner | try to turn conditional matter/EM contract into a parent theorem | False |

## Decision Ledger
| decision_id | decision | rationale | effect | claim_allowed |
| --- | --- | --- | --- | --- |
| DEC3523_0_coupling_route | keep F_src as exact theorem target | source-label forgetting before Hilbert variation is the cleanest way to avoid fitted source coupling | local GR/Newton source universality has a concrete owner to derive | False |
| DEC3523_1_Poynting_route | fold Poynting into Maxwell Hilbert stress when EM owner closes | Poynting flux is derived from T_EM, so it belongs in public source stress if Hodge/Z_EM descend through q | your Poynting intuition is useful, but it becomes a quotient-ownership test | False |
| DEC3523_2_no_promotion | do not promote live coupling owner | the current corpus has contracts and conditional derivations, not a signed shared owner | retain marker kernels and attack observed-stack/charge-lattice ownership next | False |

## Next Target
| next_doc | next_script | objective | success_gate | why_next | claim_allowed |
| --- | --- | --- | --- | --- | --- |
| 3524-Y5-R2FR-observed-stack-and-charge-lattice-parent-owner-or-local-source-kernel-values.md | scripts/Y5_R2FR_3524_observed_stack_and_charge_lattice_parent_owner_or_local_source_kernel_values.py | Try to parent-sign the shared observed stack q(Phi)->g/e/tau/ell_J/Hodge and the EM charge-lattice/gauge-norm owner; if it fails, fill local source-kernel value requirements for Delta_w, epsilon_J, b_alpha, delta_Hodge and Poynting projection. | Either the shared observed stack plus charge/gauge owner is derived from MTS primitives, or each coupling residual has explicit source/unit/projection requirements and remains nonclaim. | 3523 reduces the coupling problem to a shared parent owner rather than another broad audit. | False |

## Validation
| check_id | passed | detail | valid_for_claim |
| --- | --- | --- | --- |
| VAL3523_0_sources_exist | True | all cited local source paths exist | False |
| VAL3523_1_toy_kernels_execute | True | common source mode is silent; source-label and EM markers leak; Poynting routes through T_EM | False |
| VAL3523_2_functor_contract_covers_matter_and_EM | True | F_src and F_EM clauses written | False |
| VAL3523_3_derives_Poynting_Hilbert_route | True | Poynting is derived as Maxwell Hilbert-stress route conditionally | False |
| VAL3523_4_live_coupling_not_promoted | True | current MTS coupling owner remains unclaimed | False |
| VAL3523_5_kernel_bounds_nonclaim | True | source-label, current, alpha, Hodge and Poynting kernels remain nonclaim | False |
| VAL3523_6_no_claim_flags_true | True | no local-GR/Newton/Maxwell/source-coupling claim is promoted | False |
| VAL3523_7_next_target_selected | True | 3524 observed stack and charge lattice owner target selected | False |
| VAL3523_8_csvs_parse | True | source_register; toy_kernels; functor_contract; derivations; promotion_gates; kernel_bounds; status; canonical_status; decision_ledger; next_target | False |
| VAL3523_9_outputs_stay_in_post_checkpoint_work | True | root=D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work | False |
| VAL3523_10_formalization_workbench_not_targeted | True | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench | False |
| VAL3523_SUMMARY | True | PASS | False |
