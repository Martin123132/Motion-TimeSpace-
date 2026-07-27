# 3235 - Matter-marker Source-functor Silence Or Bound for Jperp under AX1090

Private checkpoint. This is not a local-GR claim, Maxwell derivation claim, Newtonian-limit claim, WEP pass, R10 pass, clock pass, source-coupling claim, PPN pass, or public-facing result.

## Result

3235 takes the ordinary matter channel out of the fog and puts it into the local `J_perp` residual vector.

The exact chain-rule identity is:

```text
delta_v S_A
= 1/2 int sqrt(-g_obs) T_A^{mu nu} L_v g_obs_munu
 + sum_a int J_theta,A^a L_v theta_A^a
 + E_A delta_v Psi_A
 + B_A[v].
```

So the clean zero theorem is real:

```text
S_A = S_A[Psi_A, e_obs(q(Phi)), theta_A^0],
Dq[v_perp]=0,
L_v theta_A=0,
delta_v Psi_A is fixed/gauge/on-shell,
B_A[v_perp]=0
=> delta_v S_A=0
=> J_matter=0.
```

But it is not a current MTS claim, because the same parent clause must also rule out:

```text
co-moving material/preparation markers,
continuous mass/charge/alpha/clock constants,
relative source weights kappa_A or w_A,
post-readout/source-domain/non-Hilbert tails,
matter boundary/support terms.
```

The finite no-cancellation envelope is:

```text
||J_matter||_2
<= J_geom_matter_bound
 + J_constants_bound
 + J_marker_bound
 + J_source_weight_bound
 + J_matter_boundary_bound
 + J_readout_nonH_bound
 + J_matter_lift_bound.
```

Current verdict: `MATTER_SOURCE_FUNCTOR_CHAIN_RULE_DERIVED_ZERO_UNSIGNED_BOUND_ENVELOPE_READY`.

## Matter Source-functor Derivation

| derivation_id | object | formula | zero_condition | finite_bound | status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| MSF3235_0_target | transverse ordinary-matter source | J_matter := local projection of delta_{v_perp} S_matter plus marker/readout/source-weight tails | delta_{v_perp} S_matter=0 channel-by-channel before cancellation | \|\|J_matter\|\|_2 <= sum of absolute geometry, constant, marker, source-weight, boundary, readout, and non-Hilbert components | TARGET_RESTATED_FOR_R2FR_JPERP | false |
| MSF3235_1_chain_rule | matter action variation | delta_v S_A = 1/2 int sqrt(-g_obs) T_A^{mu nu} L_v g_obs_munu + sum_a int J_theta,A^a L_v theta_A^a + E_A delta_v Psi_A + B_A[v] | on-shell matter or owned gauge lift kills E_A delta_v Psi_A; observed geometry and constants are v_perp-blind; boundary term is compact/exact/proper | C_e,A\|\|D_perp e_obs\|\| + sum_a C_theta,Aa\|\|D_perp theta_A^a\|\| + C_Psi,A\|\|delta_v Psi_A\|\|_nongauge + C_B,A\|\|B_A[v]\|\| | EXACT_CHAIN_RULE_DERIVED_CONDITIONALLY | false |
| MSF3235_2_pullback_zero_theorem | ordinary matter pullback | S_A = S_A[Psi_A, e_obs(q(Phi)), theta_A^0] and Dq[v_perp]=0 imply L_v e_obs=0 and L_v theta_A=0 | parent signs e_obs(q), theta_A superselection, matter lift, and boundary support in one clause | if unsigned, keep qbar_geom and qbar_constants components | EXACT_IF_PARENT_SIGNED_NOT_CURRENT_CLAIM | false |
| MSF3235_3_source_functor | source-current universality | one S_matter gives T_A := 2/sqrt(-g_obs) delta S_A/delta g_obs and source current sum_A T_A with one common kappa | no relative w_A, kappa_A, source-label, hidden-frame, or non-Hilbert source covector exists in parent constructor image | J_source_weight_bound := C_kappa max_A \|kappa_A/kappa_univ - 1\| + C_label\|\|a_source\|\| | CONDITIONAL_SOURCE_FUNCTOR_ROUTE_COUNTERMODEL_RETAINED | false |
| MSF3235_4_total_zero | J_matter=0 | J_matter=0 follows only if geometry pullback, constants/no-marker, matter lift, boundary silence, readout closure, and source-current universality all close on the same branch | all MSF3235 antecedents parent-signed; no cancellation between components | otherwise use JMB3235_7_total_abs_guard | FAIL_CURRENT_CLAIM_ZERO_NOT_SIGNED | false |

## No-marker Source-functor Gate

| gate_id | gate | statement | status | surviving_counterexample | effect_on_Jmatter | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| NMG3235_0_fixed_label | fixed/discrete labels | True species/representation labels that are fixed external data have D_v theta_A=0. | EXACT_CONDITIONAL_THEOREM | co-moving material/preparation/domain labels are not fixed representation data | kills only fixed-label marker pieces | false |
| NMG3235_1_no_extension_domain | no co-moving marker extension | Parent ordinary-matter category excludes theta_A=theta_A(q(Phi),m_A(X_perp)) extensions. | NOT_PARENT_SIGNED | m_A=m0+epsilon I_perp remains legal if I_perp is an allowed scalar/readout/domain invariant | retain J_marker_bound | false |
| NMG3235_2_constant_superselection | masses, charges, alpha_EM, clock standards | Lie_v theta_A=0 for all constants entering matter, clocks, EM, and material standards. | NOT_PARENT_SIGNED | continuous constants can carry transverse/readout dependence unless topological or superselection ownership is supplied | retain J_constants_bound and clock/alpha links | false |
| NMG3235_3_source_weight | relative source weights | S_matter=sum_A S_A with one common normalization, not sum_A w_A S_A with active w_A. | COUNTERMODEL_LIVE | w_A or kappa_A changes active source normalization while preserving covariance/additivity | retain J_source_weight_bound | false |
| NMG3235_4_readout_nonhilbert_tail | readout, non-Hilbert, support/domain tail | post-readout masks, source support shifts, domain terms, connection tails, and non-Hilbert currents are absent or separately bounded. | NOT_DERIVED | readout/source-domain operations can add transverse source terms after the bare matter functor descends | retain J_readout_nonH_bound | false |
| NMG3235_5_verdict | full matter no-marker/source-functor theorem | ordinary matter has no independent transverse marker/source covector only if every preceding gate closes in one parent clause. | FAIL_CURRENT_CLAIM | material markers, constants, source weights, readout tails, and boundary/support terms remain legal | J_matter remains a finite residual component, not a zero claim | false |

## Jmatter Component Bound

| bound_id | quantity | formula | required_inputs | status | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| JMB3235_0_geom | J_geom_matter_bound | sum_A C_e,A \|\|D_perp e_obs\|\|_A | observed coframe functor e_obs(q); Dq[v_perp]=0 certificate; stress envelope C_e,A; support/norm units | FORMULA_READY_INPUTS_MISSING | false |
| JMB3235_1_constants | J_constants_bound | sum_A,a C_theta,Aa \|\|D_perp theta_A^a\|\| | mass/charge/alpha/clock/material constant list; D_perp theta values or theorem-zero certificates; units/source paths | FORMULA_READY_INPUTS_MISSING | false |
| JMB3235_2_marker | J_marker_bound | sum_m C_marker,m \|\|b_marker,m\|\| with b_marker,m := D_vperp ln M_m or D_vperp theta_m | material/preparation/source marker catalogue; sensitivities C_marker,m; b_marker values or no-marker theorem | FORMULA_READY_INPUTS_MISSING | false |
| JMB3235_3_source_weight | J_source_weight_bound | C_kappa max_A \|kappa_A/kappa_univ - 1\| + C_label \|\|a_source\|\| | source-current universality certificate or relative source-weight values; same-frame normalization | FORMULA_READY_INPUTS_MISSING | false |
| JMB3235_4_boundary_support | J_matter_boundary_bound | C_B \|\|B_matter[v_perp]\|\| + C_support \|\|Delta_W_support\|\| | compact support/exact boundary theorem or boundary/source-support norms | FORMULA_READY_INPUTS_MISSING | false |
| JMB3235_5_readout_nonH | J_readout_nonH_bound | C_readout \|\|D_perp R_matter\|\| + C_nonH \|\|q_nonH\|\| + C_domain \|\|q_domain\|\| | readout closure theorem or finite readout/non-Hilbert/domain coefficients | FORMULA_READY_INPUTS_MISSING | false |
| JMB3235_6_matter_lift | J_matter_lift_bound | sum_A C_Psi,A \|\|delta_v Psi_A\|\|_nongauge | ordinary matter bundle/category; gauge/Lorentz/diffeomorphism lift theorem or nongauge lift norm | FORMULA_READY_INPUTS_MISSING | false |
| JMB3235_7_total_abs_guard | J_matter_bound | \|\|J_matter\|\|_2 <= J_geom_matter_bound + J_constants_bound + J_marker_bound + J_source_weight_bound + J_matter_boundary_bound + J_readout_nonH_bound + J_matter_lift_bound | each component theorem-zero or finite source-backed numeric bound; no cancellation allowed | NO_CANCELLATION_BOUND_READY_VALUES_MISSING | false |

## Jperp Update

| update_id | target | formula | change | status | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| UP3235_0_refined_jperp | J_perp source norm | \|\|J_perp^tau\|\|_2 <= J_geom_bound + J_matter_bound + J_EM_trace_bound + (1/4) C_F2_perp \|\|F^2\|\|_2 + J_Poynting_bound + J_memory_projector_bound | J_matter_bound is now the explicit JMB3235_7 no-cancellation envelope rather than a blank symbol | REFINED_BOUND_FOR_LOCAL_BRANCH | false |
| UP3235_1_exact_zero_requirements | v_perp exact-zero route | J_matter=0 requires MSF3235_2 + NMG3235_5 plus boundary/readout/source-current closure on the same branch | ordinary matter can be killed by derivation, but only with a signed parent matter functor/no-marker source certificate | ZERO_ROUTE_EXACT_BUT_UNSIGNED | false |
| UP3235_2_observable_links | empirical residual vector | J_matter components feed WEP/source charge, clocks/fine-structure, R10/local fifth force, and composition/source-normalization tests | if zero theorem fails, the right data route is component rows for b_marker, D_perp theta, delta_kappa_A, q_nonH, q_domain, and readout leakage | EVIDENCE_MAPPING_READY_NONCLAIM | false |

## Decision

| decision_id | decision | because | claim_status | next_action | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| DEC3235_0_result | MATTER_SOURCE_FUNCTOR_CHAIN_RULE_DERIVED_ZERO_UNSIGNED_BOUND_ENVELOPE_READY | the matter channel has an exact chain-rule zero theorem if ordinary matter, constants, matter lift, boundary support, readout, and source-current functors all descend through the same quotient branch; current sources leave material markers/source weights/readout tails legal | NO_LOCAL_GR_NO_WEP_NO_CLOCK_NO_R10_NO_SOURCE_COUPLING_CLAIM | carry J_matter_bound in the local residual vector unless a parent matter-functor/no-marker certificate is supplied | false |
| DEC3235_1_next_target | 3236-Y5-R2FR-memory-projector-domain-commutation-or-finite-bound-for-Jperp-under-AX1090 | after EM_F2, Poynting, and ordinary matter/source markers are explicit, the remaining non-geometric live channel is memory/projector/domain commutation | PRIVATE_NEXT_TARGET | derive whether memory kernel/projector/domain variations commute with the transverse split, or stage a finite J_memory_projector_bound | false |

## Generated Evidence

- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3235_INPUTS.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3235_MATTER_SOURCE_FUNCTOR_DERIVATION.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3235_NO_MARKER_SOURCE_FUNCTOR_GATE.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3235_JMATTER_COMPONENT_BOUND.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3235_JPERP_UPDATE.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3235_DECISION.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3235_VALIDATION.csv`

## Source Register

| input_id | relative_path | exists | role | evidence_hits | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| SRC3235_00_3234_doc | 3234-Y5-R2FR-Poynting-boundary-flux-silence-or-finite-bound-under-AX1090.md | true | 3234 handoff selecting matter/source functor next | L77:\| PB3234_3_total_jperp \| J_perp_bound update \| \\\|\\\|J_perp^tau\\\|\\\|_2 <= J_other_bound + (1/4) C_F2_perp \\\|\\\|F^2\\\|\\\|_2 + C_coll \\\|\\\|T_EM(u,n)\\\|\\\|_collar \| J_other_bound; C_F2_perp; F2 norm; C_coll; collar stress flux norm  \| L84:\| UP3234_1_Yperp_feedback \| transverse amplitude law \| Y_perp <= (a_perp + sqrt(a_perp^2+4 b_perp))/2 with a_perp=J_perp_bound/m_perp_min and b_perp=Phi_perp_bound \| local PPN branch cannot claim v_perp=0 unless both EM_ \| L92:\| DEC3234_1_next_target \| 3235-Y5-R2FR-matter-marker-source-functor-silence-or-bound-for-Jperp-under-AX1090 \| after EM_F2 and Poynting are explicit, the remaining live J_perp channels are ordinary matter/marker/readout,  \| L111:\| SRC3234_03_3232_update \| P8_Y5_R2FR_3232_JPERP_PHI_BOUND_UPDATE.csv \| true \| machine J_perp/Phi update carrying Poynting term \| L2:UP3232_0_Jperp_update,\\\|\\\|J_perp^tau\\\|\\\|_2,\\\|\\\|J_perp^tau\\\|\\\|_2 <= J_other_bound + (1/4 | false |
| SRC3235_01_3231_doc | 3231-Y5-R2FR-transverse-source-channel-silence-or-bound-for-Jperp-under-AX1090.md | true | J_perp source split containing matter marker channel | L12:J_perp^tau = 0, \| L19:But `J_perp^tau=0` is not a single statement. The no-cancellation split is: \| L22:J_perp^tau \| L24:+ J_matter | false |
| SRC3235_02_3231_source_csv | P8_Y5_R2FR_3231_JPERP_SOURCE_SILENCE_AUDIT.csv | true | machine J_perp source-channel row | L7:JPA3231_5_matter_marker,matter/readout/material markers,J_matter = Lie_vperp S_matter plus label/readout/material-constant variations,"matter functor, labels, masses, charges, and readout descend through q with no transv | false |
| SRC3235_03_1044_doc | 1044-Y5-R10-matter-pullback-JX-zero-or-qbarXT-bound-row.md | true | exact matter-pullback chain rule reused for R2FR transverse branch | L3:**Progress:** the ordinary-matter chain-rule route is now exact. If matter sees only `e_obs(q_loc(Phi))`, constants are vertical-trivial, matter fields have an owned fixed/gauge lift, and boundary terms are silent, then  \| L7:**Fallback:** a no-cancellation `qbar_XT` component envelope is staged for WEP/R10/clock links, but every MTS component remains value-missing and invalid for claim scoring. \| L38:\| MPD1044_1_chain_rule_identity \| chain-rule variation \| delta_v S_T = 1/2 int sqrt(-g_hat) T_T^{mu nu} Lie_v ghat_munu + sum_a int J_theta^a Lie_v theta_a + boundary/gauge/E_Psi terms \| DERIVED_STANDARD_ON_SHELL_IDENTIT \| L44:\| MPD1044_7_exact_theorem_if_signed \| conditional matter-pullback theorem \| MPD1044_2 and MPD1044_3 and MPD1044_4 and MPD1044_5 imply delta_v S_T=0, hence qbar_XT=0 and J_matter=0 for ordinary matter \| EXACT_CONDITIONAL_ | false |
| SRC3235_04_1044_derivation | P8_Y5_R10_1044_MATTER_PULLBACK_DERIVATION.csv | true | machine matter-pullback derivation | L3:MPD1044_1_chain_rule_identity,chain-rule variation,delta_v S_T = 1/2 int sqrt(-g_hat) T_T^{mu nu} Lie_v ghat_munu + sum_a int J_theta^a Lie_v theta_a + boundary/gauge/E_Psi terms,DERIVED_STANDARD_ON_SHELL_IDENTITY,condit \| L9:MPD1044_7_exact_theorem_if_signed,conditional matter-pullback theorem,"MPD1044_2 and MPD1044_3 and MPD1044_4 and MPD1044_5 imply delta_v S_T=0, hence qbar_XT=0 and J_matter=0 for ordinary matter",EXACT_CONDITIONAL_THEORE \| L10:MPD1044_8_current_verdict,current MTS matter-pullback zero,qbar_XT=0 and J_matter=0 cannot be promoted until the parent matter functor and no-marker/source-current clauses are signed,FAIL_CURRENT_CLAIM_QBARXT_ZERO_NOT_SI | false |
| SRC3235_05_1044_components | P8_Y5_R10_1044_QBARXT_COMPONENT_ENVELOPE.csv | true | machine no-cancellation qbar component envelope | L2:QBC1044_0_qbar_geom,qbar_geom,ordinary test-body X charge from observed metric/coframe leakage,qbar_geom = (2 M_T)^-1 int sqrt(-g_hat) T_T^{mu nu} Lie_v ghat_munu,Lie_v ghat_munu or theorem-zero geometry descent certific \| L4:QBC1044_2_qbar_marker,qbar_marker,"source/test charge from material markers, hidden frames, direct MTS vertices, or post-readout masks",\|qbar_marker\| <= sum \|s_marker b_marker\| over declared material/marker channels,no-m \| L7:QBC1044_5_total_abs_guard,qbar_XT_bound_abs,no-cancellation envelope for ordinary test-body X charge,\|qbar_XT\| <= \|qbar_geom\| + \|qbar_constants\| + \|qbar_marker\| + \|qbar_source_weight\| + \|qbar_nonH\|,all components theorem | false |
| SRC3235_06_3136_clock_owner | 3136-Y5-R2FR-observed-coframe-clock-functional-owner-under-AX1090.md | true | observed-coframe matter functor precedent | L10:ordinary clock matter descends to the observed coframe \| L41:\| `e_obs=Obs_e(q(Phi))`, `Dq(v)=0` \| representative/internal variations do not change the observed coframe \| \| L42:\| `S_matter=S_matter[e_obs,psi_A,theta_A]` \| clock matter sees the observed coframe \| \| L47:So the clock functional is not arbitrary. If the parent action signs the observed-coframe matter functor, `R_clock` is forced. | false |
| SRC3235_07_3096_no_marker | P8_Y5_R2FR_3096_NO_MARKER_THEOREM_ATTEMPT.csv | true | latest R2FR no-marker theorem attempt | L5:3096,MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428,2026-06-25T21:26:17.297692+00:00,False,False,False,False,NMT3096_3_co_moving_material_marker,material markers cannot source X,"A material label m_A, isotope fraction, prepar \| L6:3096,MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428,2026-06-25T21:26:17.297692+00:00,False,False,False,False,NMT3096_4_constant_superselection,"masses, charges, alpha_EM and clock constants are X-independent","Lie_v theta_A=0 \| L8:3096,MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428,2026-06-25T21:26:17.297692+00:00,False,False,False,False,NMT3096_6_verdict,full no-marker theorem,"NMT3096_1 and NMT3096_2 are useful partial results, but NMT3096_3 through  | false |
| SRC3235_08_2979_source_covector | P8_Y5_R2FR_2979_NO_MARKER_SOURCE_COVECTOR_THEOREM_ATTEMPT.csv | true | source-covector theorem and countermodel | L5:NMC2979_3_countermodel,relative source-weight countermodel,S_matter=sum_A w_A S_A is diffeomorphism-covariant/additive and changes Hilbert source to sum_A w_A T_A.,COUNTERMODEL_LIVE,"covariance, additivity and classical  \| L10:NMC2979_8_verdict,no-marker source-covector theorem,"Current corpus does not derive Hom_parent(source labels/hidden markers, Coeff_source-only)=empty.",NOT_DERIVED_CONSTRUCTOR_EXHAUSTION_OR_FINITE_JZ_COEFFICIENTS_REQUIRE | false |
| SRC3235_09_2958_bmarker | P8_Y5_R2FR_2958_BMARKER_NO_MARKER_THEOREM_GATE.csv | true | b_marker no-marker gate | L2:BMARK2958_0_definition,define b_marker,"For a material/source/preparation marker m_A, b_marker,A := D_vX ln M_A or D_vX theta_A(m_A) after sensitivity normalization.",DEFINITION_SHARP,The row captures composition/source  \| L6:BMARK2958_4_source_preparation_marker,source/preparation marker,"Isotope fraction, material preparation, source domain, or post-readout P_active labels must be fixed inputs, pure gauge, or explicit residuals.",MATERIAL_M \| L7:BMARK2958_5_verdict,b_marker theorem-zero,BMARK2958_1 plus BMARK2958_2 plus no scalar-marker counterexample and no post-readout source marker all hold.,BMARKER_ZERO_NOT_DERIVED,"Fixed labels can be silent, but the parent | false |
| SRC3235_10_3210_source_split | P8_Y5_R2FR_3210_SOURCE_CHANNEL_SPLIT_WITH_EM_POYNTING.csv | true | source split with ordinary matter/material constants | L6:JXS3210_4_matter_marker,ordinary matter/material constants,"J_X^matter=Lie_vX S_matter or qbar_XT; vanishes if matter, constants, masses, EM markers, and readout labels descend through q with Lie_vX theta_A=0.",no-marker | false |

## Validation

| check_id | pass | detail |
| --- | --- | --- |
| VAL3235_00_inputs_exist | true | inputs=11 |
| VAL3235_01_chain_rule | true | matter chain-rule source identity present |
| VAL3235_02_zero_unsigned | true | exact zero route specified as unsigned |
| VAL3235_03_no_marker_gate | true | no-marker/source-functor verdict present |
| VAL3235_04_finite_bound | true | J_matter no-cancellation envelope present |
| VAL3235_05_jperp_update | true | J_perp refined bound present |
| VAL3235_06_claims_blocked | true | claim_rows_true=0 |
| VAL3235_07_no_formalization_workbench_edit | true | no formalization-workbench paths are output targets |
| VAL3235_08_csv_parse | true | P8_Y5_R2FR_3235_INPUTS.csv;P8_Y5_R2FR_3235_MATTER_SOURCE_FUNCTOR_DERIVATION.csv;P8_Y5_R2FR_3235_NO_MARKER_SOURCE_FUNCTOR_GATE.csv;P8_Y5_R2FR_3235_JMATTER_COMPONENT_BOUND.csv;P8_Y5_R2FR_3235_JPERP_UPDATE.csv;P8_Y5_R2FR_3235_DECISION.csv |
| VAL3235_09_next_target | true | 3236-Y5-R2FR-memory-projector-domain-commutation-or-finite-bound-for-Jperp-under-AX1090 |

All generated rows remain `valid_for_claim=false`.
