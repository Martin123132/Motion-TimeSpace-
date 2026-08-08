# 3404 - Y5/R2FR source-calibrated EH parent ownership audit under AX1090

## Verdict

- The useful result is not a local-GR claim. The useful result is a precise contract for when MTS would own the source-calibrated EH/no-hair branch instead of importing GR.
- The conditional bridge is now explicit: q-basic observed metric, EH selector, Levi-Civita connection, one Hilbert source, one mass parameter, fixed boundary/readout, common G_ref, and q_loc vector silence imply the beta/local metric core route.
- The current corpus does not yet sign the central EH selector. Generic covariance still permits R^2/f(R), Weyl/Ricci-squared, scalar/vector, torsion/nonmetricity, nonlocal, projector/domain and boundary families.
- Newton's constant does not need to be numerically derived for local-GR reduction, but the same G_ref must be owned by the field equation, source charge and readout before fitting.

## Parent Ownership Clauses
| clause_id | parent_clause | mathematical_content | needed_to_derive | current_status | closes | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| EHO3404_0_q_basic_metric | one q-basic observed metric/coframe owns matter, clocks, photons, source variation and PPN readout through O(U^2) | g_obs=g_matter=g_source=g_readout; Lie_vertical g_obs=0; no representative-dependent readout | PPN coefficients refer to one physical metric rather than a stitched readout | PARTIAL_SUPPORT_NOT_OU2_PARENT_SIGNED | readout lane; source/current scale drift; observed-branch ambiguity | False |
| EHO3404_1_metric_second_order_selector | compact exterior quotient equations are local, four-dimensional, metric-only and second-order at the PPN order being claimed | Fields_ext={g_obs}; E_mn[g] contains at most second derivatives; c_R2=c_fR=c_Weyl=c_scalar=c_vector=c_X=0 or silent | Lovelock activation: E_mn=a G_mn+b g_mn instead of importing the EH operator | NOT_PARENT_SIGNED_R11_OPERATORS_RETAINED | operator lane; eta/source square route; EH-only exterior | False |
| EHO3404_2_levi_civita_connection | the observed connection is Levi-Civita or independent connection modes are pure gauge/source-silent | Gamma=LC(g_obs); T^lambda_mn=0; Q_lambda_mn=0; hypermomentum/readout connection residual=0 | Palatini/metric compatibility step and removal of torsion/nonmetricity PPN leakage | NOT_PARENT_SIGNED_CONNECTION_ROW_RETAINED | torsion/nonmetricity R11 family; clock/light/source connection residual | False |
| EHO3404_3_same_Hilbert_source | ordinary matter and EM source tensors come from one descended Hilbert action before calibration | T_total^mn=(-2/sqrt(-g)) delta(S_matter+S_EM)/delta g_mn; J^mn=kappa_* T_total^mn | universal source coupling and Ward/Bianchi balance | STRONG_CONDITIONAL_THEOREM_NOT_PARENT_SIGNED | delta_ellJ; species/tensor/EM source-selector residuals | False |
| EHO3404_4_single_mass_nohair | ordinary compact exteriors have one Hamiltonian/Pi_M mass parameter and no independent scalar/vector/domain/memory/boundary hair | g_ext=g_Schwarzschild_or_SdS(mu)+background; d hair_i=0; hair_i=0 by constraint/boundary condition | B_source=A_source^2 and no hidden O(U^2) beta source response | CONDITIONAL_EH_MATH_NOT_MTS_OWNED | source_quad; operator hair; boundary/domain leakage | False |
| EHO3404_5_fixed_boundary_reference | annulus, primitive/reference and boundary charge are parent-fixed and source-blind | B_zero_flux=0; Delta_symp=0; delta_g H_ref=0; no physical Poynting/Hilbert flux hidden in boundary fit | boundary terms cannot act as post-readout mass/beta selectors | CONDITIONAL_STOKES_ROUTE_NOT_PARENT_SIGNED | boundary lane; PiM mass drift; calibration feedback | False |
| EHO3404_6_measured_mu_lock | the exterior EH mass parameter equals the measured orbital source and the Hilbert/Pi_M charge in the same branch | mu_EH=G_ref M_H[Pi_M J_H]=mu_obs; U=mu_EH/r; kappa_MTS=8 pi G_ref/c^4 | Newtonian limit and source calibration without circular GM backfill | FIRST_ORDER_STAGED_SECOND_ORDER_UNSIGNED | delta_kappa; epsilon_Gref_match; epsilon_M; source normalization | False |
| EHO3404_7_fixed_PPN_readout | the isotropic/PPN expansion is read by one fixed post-smoothing projector in one local patch | P_PPN fixed; nabla P_PPN=0; smoothing before readout; no adaptive ray/frame fit through O(U^2) | beta/gamma are metric coefficients, not artefacts of a changing readout frame | CONDITIONAL_READOUT_THEOREM_NOT_PARENT_SIGNED | readout lane; coframe/gauge drift; beta dictionary ambiguity | False |
| EHO3404_8_q_loc_vector_silence | q_loc has either a Ward-zero compact exterior profile or separately safe beta and preferred-frame/location projections | P_loc(nabla Gamma_eff - nabla Khat)=0 through O(U^2), or beta/alpha_i/xi projections satisfy locks without cancellation | full local PPN, not just beta-only safety | OPEN_ALPHA_VECTOR_GUARD | q_loc beta guard; alpha_i/alpha3/xi guard | False |

## Conditional EH Ownership Theorem
| step_id | statement | derivation | result | claim_status | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| THM3404_0_descent | If the observed metric/coframe is q-basic and matter/EM descend through it, parent variation projects to a quotient local field equation plus vertical residuals. | delta S_parent = <E_Phi,delta Phi>; q-basic variations split into Dq^dagger E_obs plus vertical terms. EHO3404_0 and EHO3404_3 silence the vertical/source-selector terms. | one observed source-coupled field equation is eligible for EH selection | EXACT_CONDITIONAL | False |
| THM3404_1_lovelock | If the compact exterior quotient equation is local, 4D, metric-only, diffeomorphism covariant and second-order, it has EH form. | Lovelock-style uniqueness gives E_mn=a G_mn+b g_mn; background subtraction or local asymptotics fixes b/Lambda for the branch. | operator core is EH rather than a fitted GR import | MATHEMATICALLY_CLEAN_IF_EHO3404_1_SIGNED | False |
| THM3404_2_connection | If the parent connection is Palatini-EH with no hypermomentum or all independent connection modes are gauge/source-silent, the observed connection reduces to Levi-Civita. | delta_Gamma S_EH gives metric compatibility up to projective gauge; torsion/nonmetricity terms are zero or matter/readout silent by EHO3404_2. | no torsion/nonmetricity PPN or clock/light residual survives | EXACT_CONDITIONAL_NOT_CURRENTLY_SIGNED | False |
| THM3404_3_source | If the same Hilbert source owns matter and EM, the source side is common-mode calibrated by one kappa_*. | Diffeomorphism invariance gives the Ward identity; the same action variation defines T_total, J_H, M_H and source density before calibration. | delta_ellJ=0 and noncommon source weights are excluded | EXACT_CONDITIONAL_FROM_3340_3399 | False |
| THM3404_4_mass_family | If the exterior is EH-only and one-mass/no-hair, the metric family has one mass parameter mu locked to the Hilbert/Pi_M source. | Birkhoff/Schwarzschild-family mathematics supplies the exterior; EHO3404_4 through EHO3404_6 identify mu with G_ref M_H rather than an after-the-fact orbital fit. | U=mu/r is the same U in Newton, PPN, H_tau and Pi_M | CONDITIONAL_EH_MATH_WITH_MTS_OWNERSHIP_OPEN | False |
| THM3404_5_beta_square | The one-parameter EH family gives the source-square law needed for beta=1 after measured-U normalization. | With U=A_source W and one mu controlling both terms, B_source=A_source^2; the log-lapse expansion has no U^2 term in v. | kappa_eta=0 and kappa_source_quad=0 if EHO3404 clauses are signed | EXACT_CONDITIONAL_FROM_3402 | False |
| THM3404_6_retained_lanes | If PiM, boundary, readout, operator, coupling and q_loc ownership clauses are signed, every retained 3403 beta lane zeroes. | Substitute EHO3404_1..8 into the 3403 zero-route table and the 3401 kappa_v component ledger. | kappa_v=0, hence beta=1 in the local metric core | EXACT_CONDITIONAL_NOT_CLAIM_LEVEL | False |
| THM3404_7_local_GR_bridge | If the above also kills gamma, alpha_i, zeta_i and xi residuals, the MTS local branch reduces to GR/PPN at tested orders. | beta alone is insufficient; the same operator/source/readout clauses must silence the full PPN residual vector without cancellation. | local-GR route exists as a precise parent-ownership contract, not yet as a claim | CONDITIONAL_BRIDGE_WRITTEN_FULL_VECTOR_OPEN | False |

## EH Import Obstruction Theorem
| obstruction_id | statement | counter_family | why_it_matters | required_fix | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| OBS3404_0_covariance_not_enough | Diffeomorphism covariance, locality and an observed metric do not by themselves select EH. | sqrt(-g)(aR+b+c1 R^2+c2 R_mn R^mn+c3 C_mnrs C^mnrs)+scalar/vector/connection/boundary terms | these terms can preserve a Newtonian-looking first order while shifting beta, gamma, finite-range, clock, WEP or preferred-frame rows | derive a parent normal-form selector, a double-zero coefficient law, or a sourced finite residual bound | False |
| OBS3404_1_EH_import_test | Using Schwarzschild/SdS before proving EHO3404_1..6 is an EH import, not an MTS derivation. | f(R) or scalar-tensor exterior with the same leading GM/r but extra scalar charge or range | the 3402 beta-square theorem is exact only after the EH/no-hair family is parent-owned | make EH-only/no-hair a theorem of the parent quotient branch | False |
| OBS3404_2_connection_gap | A metric field does not automatically imply the observed connection is Levi-Civita. | metric-affine/projective/torsion/nonmetricity modes with weak source or readout couplings | connection modes can leak into clocks, spin, light propagation, WEP and PPN readout | prove Palatini compatibility/source silence or carry the connection residual vector | False |
| OBS3404_3_G_derivation_not_required_but_G_ownership_is | Local-GR reduction does not require deriving the dimensionful number G from nothing, but it does require one common G_ref across field, source and readout. | separate kappa_field, kappa_source, G_orbit or post-readout GM calibration | GR itself calibrates Newton's constant; the non-negotiable MTS task is common-branch ownership, not numerology | sign kappa_MTS=8 pi G_ref/c^4 and mu=G_ref M_H[Pi_M J_H] before readout | False |

## Premise Scorecard
| score_id | source_rung | required_identity | current_status | parent_owned_now | why_not_owned | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| PS3404_0_observed_metric_branch | SCEH529_0_observed_metric_branch | one observed metric/coframe is used by matter, clocks, photons, source variation, and PPN readout | conditional_not_derived_through_O_U2 | False | current source row is conditional/not-derived/not-run; 3404 treats it as a clause to prove, not a permission to claim | False |
| PS3404_1_EH_only_exterior | SCEH529_1_EH_only_exterior | compact exterior field equation is EH plus harmless Lambda/background subtraction | not_derived_R11_template_only | False | current source row is conditional/not-derived/not-run; 3404 treats it as a clause to prove, not a permission to claim | False |
| PS3404_2_one_parameter_nohair_family | SCEH529_2_one_parameter_nohair_family | ordinary compact exterior is a one-parameter mass family with no scalar/vector/domain/memory/boundary hair | not_derived_extra_sectors_retained | False | current source row is conditional/not-derived/not-run; 3404 treats it as a clause to prove, not a permission to claim | False |
| PS3404_3_measured_mu_calibration | SCEH529_3_measured_mu_calibration | the EH mass parameter equals measured orbital GM and the Hilbert/projected source charge | not_derived_523_scorecard_unfilled | False | current source row is conditional/not-derived/not-run; 3404 treats it as a clause to prove, not a permission to claim | False |
| PS3404_4_constant_source_normalization | SCEH529_4_constant_source_normalization | mu_EH has no time/radius/species/range/frame/domain derivative and no mu_extra channel | not_derived_extra_mass_channels_unfilled | False | current source row is conditional/not-derived/not-run; 3404 treats it as a clause to prove, not a permission to claim | False |
| PS3404_5_isotropic_PPN_expansion | SCEH529_5_isotropic_PPN_expansion | the EH family is expanded in the observed isotropic/PPN readout coordinate | conditional_on_prior_rungs | False | current source row is conditional/not-derived/not-run; 3404 treats it as a clause to prove, not a permission to claim | False |
| PS3404_6_no_quadratic_leakage | SCEH529_6_no_quadratic_leakage | R11, q_loc, boundary/domain, and readout sectors contribute no independent O(U^2) term | not_derived_components_unfilled | False | current source row is conditional/not-derived/not-run; 3404 treats it as a clause to prove, not a permission to claim | False |
| PS3404_7_beta_local_GR_gate | SCEH529_7_beta_local_GR_gate | beta residual envelope and full PPN vector are zero or below locks without cancellation | not_run | False | current source row is conditional/not-derived/not-run; 3404 treats it as a clause to prove, not a permission to claim | False |

## Non-EH Operator Survival Law
| operator_id | operator_family | survival_law | zero_or_safe_condition | needed_input | status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| B530_0_source_AB | source_normalization_operator | allowed by generic covariance/effective expansion unless an MTS parent selector sets the coefficient to zero or proves source/readout silence | source equation or EH mass-family theorem gives B_source=A_source^2 after measured-GM normalization | A_source;B_source;measured_mu_lock;mu_extra=0 | unfilled | False |
| B530_1_R2_fR_scalar | R2_fR_scalar_mode | allowed by generic covariance/effective expansion unless an MTS parent selector sets the coefficient to zero or proves source/readout silence | c_R2=c_fR=0, scalar mass infinite, source coupling zero, or mapped residual below beta/gamma/R10 locks | c_R2_or_c_fR; scalar mass; matter/source coupling; weak-field solution | template_only | False |
| B530_2_Ricci_Weyl | Ricci_Weyl_squared | allowed by generic covariance/effective expansion unless an MTS parent selector sets the coefficient to zero or proves source/readout silence | coefficients zero, pure topological combination with harmless boundary, or weak-field map below beta/gamma/xi locks | c_Ricci_or_c_Weyl; units; topological/boundary status; weak-field map | template_only | False |
| B530_3_scalar_class | scalar_tensor_class_metric | allowed by generic covariance/effective expansion unless an MTS parent selector sets the coefficient to zero or proves source/readout silence | phi/C constant universal with zero stress/source charge, infinite mass, or mapped residual below locks | F(phi,C); scalar/class solution; source charge; beta/gamma/Gdot/R10 map | unfilled_retained | False |
| B530_4_boundary | boundary_topological_terms | allowed by generic covariance/effective expansion unless an MTS parent selector sets the coefficient to zero or proves source/readout silence | pure boundary/topological/class term has no exterior stress, no flux, no monopole shift, and no readout stress | boundary coefficient or no-flux/no-stress theorem | template_only | False |
| B530_5_projector_domain | projector_domain_stress | allowed by generic covariance/effective expansion unless an MTS parent selector sets the coefficient to zero or proves source/readout silence | projector/domain variables are metric-independent topological masks or first-class constraints with zero exterior stress | projector stress coefficient; domain no-hair theorem; alpha_i/xi map | unfilled_retained | False |
| B530_6_nonlocal_memory | nonlocal_memory_kernel | allowed by generic covariance/effective expansion unless an MTS parent selector sets the coefficient to zero or proves source/readout silence | compact-local kernel silence, screening, zero norm, or residual map below local locks | kernel form/norm; local compact limit; Gdot/alpha3/R10 map | template_only | False |
| B530_7_q_loc | q_loc_Gamma_Khat | allowed by generic covariance/effective expansion unless an MTS parent selector sets the coefficient to zero or proves source/readout silence | Ward-zero through O(U^2) or compact profile maps below beta without violating alpha3/preferred-frame gates | physical q_loc profile; U^2 conversion; projection/readout normalization | provisional_budget_not_claim | False |
| B530_8_torsion_nonmetricity | torsion_nonmetricity | allowed by generic covariance/effective expansion unless an MTS parent selector sets the coefficient to zero or proves source/readout silence | Levi-Civita compatibility theorem or projective/spin modes are inert for all matter/readout sectors | P4 connection rows; compatibility theorem; WEP/clock/light map | template_only | False |
| B530_9_vector_preferred_frame | vector_preferred_frame | allowed by generic covariance/effective expansion unless an MTS parent selector sets the coefficient to zero or proves source/readout silence | vector absent, pure gauge, dynamically aligned with zero stress, or mapped below preferred-frame locks | c_V; vector profile; alpha_i/xi map; beta cross-term map | unfilled_retained | False |
| B530_10_bulk_X | bulk_X_force_law | allowed by generic covariance/effective expansion unless an MTS parent selector sets the coefficient to zero or proves source/readout silence | positive source-free mass-gap no-hair or alpha_X(lambda_X) plus PPN/source map below locks | q_X,c_X,m_X; source/test normalization; alpha(lambda) curve | unfilled_retained | False |
| B530_11_readout_frame | observed_readout_frame | allowed by generic covariance/effective expansion unless an MTS parent selector sets the coefficient to zero or proves source/readout silence | same observed metric/coframe theorem through second PPN order | readout map from parent variables to observed isotropic PPN coordinate | unfilled_retained | False |

## Local-GR Impact
| impact_id | affected_quantity | if_EHO3404_signed | reason | current_status | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| IMP3404_0_first_order_Newton | Delta_Newton_v_coupled | 0 | EHO3404_3 and EHO3404_6 activate PC3400/T3399 source-normalization zeroes | CONDITIONAL_FROM_3399_3400 | False |
| IMP3404_1_eta_v | kappa_eta | 0 | EH one-parameter log-lapse has no U^2 term in v after measured-U normalization | CONDITIONAL_FROM_3402 | False |
| IMP3404_2_source_quad | kappa_source_quad | 0 | one mass parameter gives B_source=A_source^2 | CONDITIONAL_FROM_3402 | False |
| IMP3404_3_operator | kappa_operator | 0 | metric-only second-order selector kills R11 beta operators or moves them into explicit finite bounds | OPEN_R11_SELECTOR | False |
| IMP3404_4_PiM_boundary_readout | kappa_PiM+kappa_boundary+kappa_readout | 0 | fixed parent mass projector, fixed annulus/reference and fixed PPN readout remove post-readout beta leakage | CONDITIONAL_FROM_3403 | False |
| IMP3404_5_coupling | kappa_coupling | 0 | same Hilbert source and common kappa extend PC3400 through O(U^2) | SECOND_ORDER_EXTENSION_UNSIGNED | False |
| IMP3404_6_q_loc | kappa_q_loc plus alpha_i/xi projections | 0 only if q_loc vector silence is included | beta-only compact-shell number is not enough while preferred-frame projection is unsigned | OPEN_ALPHA_VECTOR_GUARD | False |
| IMP3404_7_local_GR | beta/gamma/alpha_i/zeta_i/xi local PPN vector | passes in the local branch at claimed order, subject to empirical locks | EH metric core plus source/readout/operator silence is the route from MTS to GR, not a dark-sector patch | NOT_CLAIMED_FULL_VECTOR_OPEN | False |

## Newton G Policy
| policy_id | question | answer | required_contract | failure_mode | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| G3404_0_dimensionful_constant | Must MTS derive the numerical value of Newton's constant to reduce to GR/Newton? | No. A dimensionful constant can be calibrated by measurement, as in GR. What must be derived is that the same branch constant is used everywhere. | kappa_MTS=8*pi*G_ref/c^4 in the field equation and mu=G_ref*M_H[Pi_M J_H] before PPN readout | separate fitted GM, source kappa, field kappa or readout kappa creates an unowned closure assumption | False |
| G3404_1_predictive_upgrade | What would be stronger than GR-style calibration? | A parent topological/superselection law for kappa_MTS or a dimensionless relation involving other measured constants. | not required for local-GR reduction; useful later as an MTS-specific upgrade | chasing G numerology before common-branch ownership distracts from the local-GR bridge | False |

## Promotion Gates
| gate_id | claim | gate_pass | reason | claim_allowed | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| GATE3404_0_contract | source-calibrated EH parent-ownership contract is written | True | EHO3404_0..8 state the exact parent clauses needed to own the EH/no-hair branch | False | False |
| GATE3404_1_EH_owned | EH-only/no-hair branch is derived by MTS parent clauses | False | metric second-order selector, connection silence and non-EH operator zeroes remain unsigned | False | False |
| GATE3404_2_source_calibrated | the EH mass parameter is the same Hilbert/PiM/measured source through O(U^2) | False | first-order source chain is staged, but second-order parent ownership remains open | False | False |
| GATE3404_3_beta | kappa_v=0 or beta bound pass is derived | False | 3402 and 3403 give exact conditional routes, but 3404 ownership clauses are not signed | False | False |
| GATE3404_4_full_PPN | local GR/PPN vector is derived | False | gamma and preferred-frame/location/vector residuals still require signed projection maps | False | False |

## Decision Ledger
| decision_id | finding | reason | next_action | valid_for_claim |
| --- | --- | --- | --- | --- |
| DEC3404_0_progress | the local-GR route is now an exact parent-ownership contract rather than a loose EH assumption | 3404 connects descent, Lovelock/Palatini, Hilbert source, no-hair, measured mu, readout and q_loc silence in one proof chain | attack the parent normal-form EH selector, because it kills the largest cluster of remaining beta lanes | False |
| DEC3404_1_no_claim | current corpus still cannot claim local GR | generic covariance allows non-EH operators; MTS-specific selector/zero laws are not signed | derive a vertical/quotient symmetry or normal-form principle that forces the non-EH coefficients to zero or makes them boundary/topological | False |
| DEC3404_2_G_constant | deriving the numerical value of G is optional, but common ownership of G_ref is mandatory | GR calibrates G; MTS must prevent field/source/readout G from splitting into hidden fit constants | keep kappa_MTS as a branch constant while proving kappa_field=kappa_source=kappa_readout | False |

## Next Target
| target_id | target_script | objective | why_next | valid_for_claim |
| --- | --- | --- | --- | --- |
| 3405-Y5-R2FR-parent-normal-form-EH-selector-proof-attempt-under-AX1090.md | scripts/Y5_R2FR_3405_parent_normal_form_EH_selector_proof_attempt.py | try to derive the metric-only second-order EH selector from MTS quotient/vertical symmetry rather than importing Lovelock premises | this is the central fork: if it works, eta/source/operator/readout/boundary lanes collapse together; if it fails, non-EH residual bounds become mandatory | False |
| 3406-Y5-R2FR-q_loc-U2-alpha-vector-projection-split-under-AX1090.md | scripts/Y5_R2FR_3406_q_loc_U2_alpha_vector_projection_split.py | separate q_loc beta, alpha_i/alpha3 and xi projections so a beta-safe number cannot hide a preferred-frame failure | this is the highest-danger remaining vector guard if the EH selector route starts to close | False |

## Validation
| check_id | check | passed | detail |
| --- | --- | --- | --- |
| VAL3404_0_sources | all registered sources exist | True | sources=25 |
| VAL3404_1_clauses | parent ownership clauses written | True |  |
| VAL3404_2_conditional_theorem | conditional EH ownership proof chain written | True |  |
| VAL3404_3_obstruction | EH import obstruction theorem written | True |  |
| VAL3404_4_operator_survival | non-EH operator survival law covers R11 beta families | True |  |
| VAL3404_5_impact | kappa_v/local-GR impact rows written | True |  |
| VAL3404_6_g_policy | Newton G policy recorded | True |  |
| VAL3404_7_gates_block_claim | local-GR/beta gates remain blocked | True |  |
| VAL3404_8_no_overclaim | all generated rows are nonclaim | True |  |
| VAL3404_9_scope | no 3404 output path targets formalization-workbench | True |  |
| VAL3404_10_next | next target is parent normal-form EH selector | True |  |
| VAL3404_11_overall | 3404 validation overall | True | all required checks passed |
