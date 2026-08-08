# 3547 — Parent EM same-owner zero or Ke-alpha source leg

## Verdict

- **The same-owner route is mathematically sufficient:** fixed parent charge generator, fixed generator norm, unique `F_Q^2` curvature subblock, and same Noether current owner imply `z_lambda=0`, `z_g=0`, hence `b_alpha=2 z_g-z_lambda=0`.
- **It is not yet a live MTS claim:** generic gauge/diffeomorphism symmetry still allows `f_X(Phi)F^2`, current-prefactor, readout-regeneration, and Poynting-boundary counterbranches unless the parent object language forbids or bounds them.
- **Finite branch remains ready:** any future nonzero `K_e_alpha*b_alpha` must pass the nonclaim gate `<= 1.372549e-12` in a declared DD e-basis convention.
- **Poynting role clarified:** Poynting stress is part of the total Hilbert source/radiative flux accounting; it is not a shortcut proof of alpha silence.

## Parent Action Contract

| contract_id | parent_clause | mathematical_form | implies | current_status |
| --- | --- | --- | --- | --- |
| PACT3547_0_fixed_charge_generator | the local EM field is the connection component A_Q of one fixed compact parent generator T_Q | T_Q in Lie(G_parent) or charge lattice L_Q; exp(2 pi T_Q)=1; D_X T_Q=0 | no source/material dependence can enter through the charge label itself | SUFFICIENT_CONTRACT_NOT_PARENT_SIGNED |
| PACT3547_1_fixed_generator_norm | the parent fibre metric/symplectic/lattice form fixes the norm of T_Q | N_Q=<T_Q,T_Q>_P is quotient-fixed; D_X N_Q=0 | the Maxwell kinetic normalization cannot slide with motion/time/source fields | SUFFICIENT_CONTRACT_NOT_PARENT_SIGNED |
| PACT3547_2_unique_curvature_norm | the observed F_Q^2 term is only the inherited parent curvature norm | S_EM=-C_P/4 int <F,F>_P and no independent f_X(Phi) F_Q^2 term exists | z_lambda=0 unless a common pure-unit line is also explicitly owned | CORE_GAP_COUNTERTERM_STILL_LEGAL |
| PACT3547_3_same_current_owner | the source current is the Noether/Ward current of the same parent generator and normalization | J_Q = delta S_matter/delta A_Q with fixed representation weights n_A; D_X n_A=0 | z_g=0 and no independent current rescaling appears | SUFFICIENT_CONTRACT_NOT_PARENT_SIGNED |
| PACT3547_4_readout_and_radiative_stability | readout, clocks, loops, Poynting flux and material binding do not regenerate a hidden alpha coefficient | R_readout_alpha=R_rad_alpha=Phi_EM_rad=C_EM_readout=0 or individually bounded | baseline b_alpha zero survives the lab reduction | SUFFICIENT_CONTRACT_NOT_PARENT_SIGNED |
| PACT3547_5_factorized_source_leg | if b_alpha is not zero, K_e_alpha is a factorized source/material/readout projection rather than a fitted knob | K_e_alpha=K[Earth, Ti/Pt material tensor, q units, sign, readout] | nonzero alpha branch can be tested against 1.372549e-12 | FINITE_ROUTE_INPUTS_MISSING |

## Theorem Attempt

| step_id | statement | derivation | result | status |
| --- | --- | --- | --- | --- |
| THM3547_0_assume_contract | Assume PACT3547_0 through PACT3547_4 hold as parent action clauses. | All EM normalization data descend from a single fixed quotient object before source/material readout. | the only legal local EM action has fixed lambda_0 and fixed current coupling g_0 in the chosen observed convention | CONDITIONAL_THEOREM_STEP |
| THM3547_1_kinetic_silence | The kinetic coefficient has no vertical derivative. | lambda_A = C_P N_Q with D_X C_P=0 and D_X N_Q=0; no f_X(Phi)F_Q^2 slot is legal. | z_lambda = D_X ln lambda_A = 0 | CONDITIONAL_IF_UNIQUE_F2_SIGNED |
| THM3547_2_current_silence | The current coupling has no vertical derivative. | J_Q is varied from the same parent connection and fixed integer representation weights; no c_X(Phi) A.J source slot is legal. | z_g = D_X ln g_J = 0 | CONDITIONAL_IF_CURRENT_OWNER_SIGNED |
| THM3547_3_alpha_zero | The invariant alpha residual vanishes. | 3546 gives b_alpha=2 z_g - z_lambda; with z_g=z_lambda=0, b_alpha=0. | b_alpha=0 and therefore K_e_alpha*b_alpha=0 for any finite K_e_alpha | CONDITIONAL_THEOREM_VALID_NOT_PARENT_SIGNED |
| THM3547_4_common_line_variant | A common pure-unit line can also kill alpha drift if it scales kinetic and current terms with powers lambda~n^2 and g~n. | If z_lambda=2 z_g from one parent-owned unit line and the line is not a physical source marker, then b_alpha=0. | common-line cancellation is allowed only as a tracked unit/readout theorem, not as a tuned cancellation | ALTERNATIVE_CONDITIONAL_ROUTE |
| THM3547_5_verdict | The same-owner route is mathematically sufficient but not forced by the current corpus. | Gauge/diffeomorphism invariance alone still permits f_X(Phi)F^2 and source-current rescaling countermodels. | parent action must explicitly contain the fixed generator/unique-F2/current-owner contract, or the active alpha branch stays bounded not derived | THEOREM_CONSTRUCTED_AS_CONTRACT_NOT_CLAIM |

## Countermodels

| countermodel_id | legal_deformation | why_it_survives_generic_symmetry | effect | what_kills_it |
| --- | --- | --- | --- | --- |
| CM3547_0_nonminimal_F2 | Delta S = -1/4 int f_X(Phi) F_Q wedge *F_Q | gauge invariant and diffeomorphism covariant for scalar f_X | z_lambda != 0, so b_alpha can be nonzero | typed no-Hom/coefficient-domain theorem or unique parent curvature norm |
| CM3547_1_current_prefactor | Delta S = int c_X(Phi) A_mu J^mu | can be written as a source/current normalization if the current is not fixed as a parent Noether current | z_g != 0 and source/material charge can leak into alpha/source coupling | same parent connection/current owner plus fixed representation weights |
| CM3547_2_readout_regeneration | S_eff or clock/material readout contains f_eff(Phi) F^2 after reduction | effective/readout maps can reintroduce dependence even if the bare parent action is fixed | calibrated alpha baseline can fail as a lab observable theorem | radiative/readout stability theorem or explicit clock/WEP bound row |
| CM3547_3_poynting_flux_boundary | net exterior Phi_EM_rad = integral S_Poynting dot n dA | Poynting flux is a real Hilbert stress/boundary-energy channel, not a gauge artifact | affects source normalization/time hair rather than static alpha itself | stationary isolated local branch or finite Gdot/clock/source flux bound |

## Poynting Interface

| interface_id | poynting_object | role_in_alpha_problem | zero_or_bound | next_action |
| --- | --- | --- | --- | --- |
| POY3547_0_static_bound_fields | ordinary bound EM fields inside the source | contribute to total Hilbert stress and material binding sensitivity, not an independent alpha drift | included in M_H/T_total if Maxwell stress owner is fixed | keep inside source normalization rather than double-counting as a separate alpha source coefficient |
| POY3547_1_radiative_flux | net exterior Poynting flux | can regenerate time/source hair even when static alpha is calibrated | zero for stationary isolated branch, otherwise bound by Gdot/clock/source-flux rows | do not use Poynting language to prove alpha zero; use it to police radiative reentry |
| POY3547_2_cross_term | nonminimal hidden-visible F^2 or F*F cross term | is exactly the C_XF2 throat behind z_lambda and b_alpha | requires no-Hom/unique-F2 theorem or finite WEP/clock/R10 bound | make C_XF2 the coefficient-domain proof target if same-owner proof is pursued |

## Fallback Branches

| fallback_id | branch | required_next_input | acceptance_gate | current_status |
| --- | --- | --- | --- | --- |
| FB3547_0_parent_zero_path | derive b_alpha=0 | parent object-language certificate for fixed T_Q, fixed N_Q, unique F2, same current owner and readout stability | no f_X(Phi)F^2 or c_X(Phi)A.J countermodel remains legal | BEST_DERIVATION_ROUTE_NOT_CLOSED |
| FB3547_1_finite_source_leg | bound nonzero alpha branch | factorized K_e_alpha source leg and b_alpha parent value/bound | abs(K_e_alpha*b_alpha) <= 1.372549019608e-12 in a single declared convention | FINITE_ROUTE_READY_FOR_INPUTS |
| FB3547_2_calibrated_baseline | use measured alpha locally | label alpha_0 as calibrated local constant and keep active alpha branch quarantined | not advertised as derived alpha; no cancellation with WEP/source residuals | SAFE_FOR_BASELINE_MAXWELL_STRESS |

## Decisions

| decision_id | question | decision | basis | forward_value |
| --- | --- | --- | --- | --- |
| DEC3547_0_same_owner_proof | Was b_alpha=0 derived outright from existing corpus? | NO_EXISTING_CORPUS_DOES_NOT_FORCE_IT | generic gauge/diffeomorphism symmetry still permits nonminimal F2 and current-prefactor countermodels | a sufficient parent action contract is now explicit and narrow |
| DEC3547_1_conditional_theorem | Is there a mathematically clean theorem if the parent contract is signed? | YES | fixed generator norm plus unique curvature norm gives z_lambda=0; same current owner gives z_g=0; hence b_alpha=0 | this is the derivable path, not just a closure statement, but it needs a parent object-language certificate |
| DEC3547_2_poynting_role | Does the Poynting vector prove or kill the alpha branch? | NEITHER | Poynting stress belongs in total Hilbert source and radiative flux gates; C_XF2 remains the alpha throat | use Poynting to police source/radiative reentry, not as a shortcut alpha proof |

## Validation

| validation_id | passes | status | detail |
| --- | --- | --- | --- |
| VAL3547_0_sources_exist | True | PASS | all cited 3547 source paths exist |
| VAL3547_1_generated_csvs_parse | True | PASS | 10 generated CSV files parse with DictReader |
| VAL3547_2_contract_complete | True | PASS | every parent action contract row has a clause, mathematical form, and status |
| VAL3547_3_theorem_nonclaim | True | PASS | same-owner theorem rows remain conditional/nonclaim |
| VAL3547_4_countermodels_retained | True | PASS | blocking countermodels are explicitly retained with kill conditions |
| VAL3547_5_formalization_workbench_untouched | True | PASS | 3547 generated outputs only inside post-checkpoint-work |

## Next target

Move to `3548-Y5-R2FR-typed-EM-coefficient-domain-no-Hom-certificate-or-alpha-closure-demotion.md`. This attacks the exact countermodels: if `f_X(Phi)F^2` and `c_X(Phi)A.J` are untypeable, the same-owner theorem has teeth; if they remain legal, alpha should be treated as calibrated closure plus finite active-branch bounds while the main GR/Newton source route continues elsewhere.

Generated UTC: 2026-06-29T11:04:14.998794+00:00