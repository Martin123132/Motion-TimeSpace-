# 3343 — epsilon_EM Public Hodge/Poynting Zero Or Bound Under AX1090

Generated: `2026-06-28T02:34:36.101179+00:00`

## Summary
- The clean EM route is now explicit: use the public Maxwell action, vary it with respect to the observed metric, and count Poynting as EM Hilbert-stress flux.
- This gives an exact conditional zero theorem for `epsilon_EM`, but not a promoted MTS claim because hidden `Z_Q`, current lattice, Hodge/readout, and boundary flux ownership are not parent-signed.
- The least-scrutiny discipline is to **not** add Poynting as a separate background force unless a new parent vertex is derived and bounded.
- No local-GR, Maxwell, alpha, WEP, R10, or source-coupling claim is made.

## Public Maxwell Action Derivation
| derivation_id | claim_piece | formula | derivation | result | status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| EMD3343_0_action | public Maxwell action | S_EM[g_obs,A_Q]=-lambda_0/4 int sqrt(-g_obs) F_{mu nu}F^{mu nu} + int sqrt(-g_obs) A_mu J_Q^mu | The only metric/coframe dependence is public g_obs and lambda_0 is hidden-independent. | EM belongs in the same Hilbert-stress source sector as ordinary matter. | EXACT_CONDITIONAL_ACTION_FORM | false |
| EMD3343_1_metric_variation | Hilbert EM stress | T_EM^{mu nu}=lambda_0(F^{mu alpha}F^nu_alpha - 1/4 g_obs^{mu nu}F_{alpha beta}F^{alpha beta}) | Vary S_EM with respect to g_obs; no private Hodge or background-flow tensor is varied separately. | EM energy density, stress, pressure, and radiation flux are source terms through T_EM. | EXACT_CONDITIONAL_VARIATION | false |
| EMD3343_2_current_variation | Maxwell equation/current owner | nabla_mu(lambda_0 F^{mu nu})=J_Q^nu | Vary A_Q; if J_Q is the same Noether current/readout lattice, delta_J=0. | A floating source/test charge normalization is not allowed in the clean branch. | EXACT_CONDITIONAL_CURRENT_ROUTE | false |
| EMD3343_3_poynting_balance | Poynting as flux of Hilbert stress | dE_EM/dt = - surface_int S dot dA - int J dot E dV | Project nabla_mu T_EM^{mu nu}=-F^nu_mu J^mu onto an observer slice. | Poynting is not a separate MTS force in the clean route; it is the spatial energy-flux component of T_EM. | EXACT_CONDITIONAL_FLUX_LAW | false |
| EMD3343_4_vertical_zero | epsilon_EM theorem-zero condition | L_v g_obs=L_v lambda_0=L_v J_Q=L_v chi_nonmetric=L_v(readout)=0 => epsilon_EM=0 | Chain rule and Leibniz rule kill b_alpha, delta_J, delta_star, DeltaT_EM, and unclosed Poynting flux. | epsilon_EM is zero only if every EM coefficient/readout factor is q-basic or constant. | EXACT_CONDITIONAL_THEOREM_NOT_PARENT_SIGNED | false |

## Hodge/Poynting Zero Audit
| audit_id | subterm | zero_condition | proof_piece | current_status | parent_signed | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| HPZ3343_0_metric_hodge | delta_star | chi^{mu nu alpha beta}=lambda_0 sqrt(-g_obs)(g_obs^{mu alpha}g_obs^{nu beta}-g_obs^{mu beta}g_obs^{nu alpha}) with no nonmetric Delta_chi | metric Hodge specialization and reconstruction rows 3286/3287 | EXACT_CONDITIONAL_NOT_PARENT_SIGNED | false | false |
| HPZ3343_1_poynting | Phi_Poynting_unclosed | Poynting vector is read as S_EM^a=-h^a_mu T_EM^{mu nu}u_nu from same public Hodge/coframe and has zero or explicitly balanced boundary flux | Poynting q-basic lemma plus 3127 flux guard | EXACT_CONDITIONAL_WITH_BOUNDARY_GUARD | false | false |
| HPZ3343_2_ZQ | b_alpha | Z_Q=lambda_0 is constant/q-basic and no hidden f_X, radiative readout drift, or F^2 counterterm survives | 3289 q-basic Z_Q theorem and 3290 no-hidden Z_Q theorem | COUNTERMODEL_RETAINED | false | false |
| HPZ3343_3_current | delta_J | J_Q is the same Noether current with fixed representation charge labels and no source/test current renormalization | 3290 source-current universality theorem | EXACT_CONDITIONAL_NOT_PARENT_SIGNED | false | false |
| HPZ3343_4_no_direct_vertex | direct EM-background force | no f(psi)F^2, psi J.A, or direct Poynting-background force term unless parent-derived and separately bounded | 3323/3324 clean-route discipline | RECOMMENDED_DISCIPLINE_NOT_PARENT_EXCLUSION | false | false |

## epsilon_EM Residual Decomposition
| term_id | component | definition | zero_route | finite_route | current_status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| EEM3343_0_b_alpha | b_alpha | vertical/readout drift of alpha_EM or Z_Q | q-basic/constant Z_Q and q-basic hbar,c,readout | alpha drift, clock products, spectra, R10 alpha products | NOT_NUMERIC_FULL_COMPONENT | false |
| EEM3343_1_delta_J | delta_J | source/test current or charge normalization drift | same Noether current and fixed representation charge lattice | WEP/R10 source-current rows; 3127 has one nonclaim smoke reproduction | PARTIAL_NONCLAIM_SMOKE_ONLY | false |
| EEM3343_2_delta_star | delta_star | hidden Hodge/coframe/constitutive drift | metric Hodge from public g_obs and constant Z_Q | constitutive/birefringence/stress projection bounds | DERIVED_CONDITIONAL_NEEDS_PROJECTION_BOUND | false |
| EEM3343_3_delta_TEM | \|\|P_EM DeltaT_EM\|\|/\|\|T_EM\|\| | non-Hilbert EM stress tensor mismatch | T_EM is metric variation of the public Maxwell action | EM stress/light propagation residual projection | EXACT_CONDITIONAL_NOT_PARENT_SIGNED | false |
| EEM3343_4_poynting | Phi_Poynting_unclosed | unbalanced EM energy flux or double-counted wave/Poynting channel | flux is the spatial component of Hilbert T_EM with closed or explicitly balanced boundary | radiative flux/readout coefficient separate from static ADM source coefficient | GUARD_DERIVED_BOUNDARY_NOT_FILLED | false |

## Partial Zero Certificate
| zero_id | claim_piece | deduction | still_missing | status | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| PZ3343_0_constant_lambda0 | constant lambda_0 does not create a local EM residual | L_v lambda_0=0, so lambda_0 can calibrate alpha/Z_Q without producing b_alpha. | parent must forbid hidden f_X(I_hid), radiative/readout alpha drift, or current normalization drift | PARTIAL_ZERO_DERIVED | false |
| PZ3343_1_poynting_inside_TEM | Poynting is safe if kept inside Hilbert T_EM | S_EM^a=-h^a_mu T_EM^{mu nu}u_nu is q-basic when T_EM,h,u are q-basic. | worldtube/boundary flux balance and public coframe/readout signature | PARTIAL_ZERO_DERIVED | false |
| PZ3343_2_direct_background_force_forbidden | direct Poynting-background force is not the clean route | Adding Poynting again outside T_EM double-counts EM flux unless a distinct parent vertex is derived. | formal parent exclusion of f(psi)F^2 and psi J.A terms | DISCIPLINE_DERIVED_NOT_PARENT_SIGNED | false |

## FRV3340 epsilon_EM Component Rows
| candidate_id | component_id | symbol | mode | theorem_zero | zero_authority | component_value | response_factor | component_units | source_path | equation_ref | arena | no_cancellation_guard | runner_acceptance | valid_for_claim | claim_blocker |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CAND3343_FRV3340_4_epsilon_EM_theorem_zero_unsigned | FRV3340_4_epsilon_EM | epsilon_EM | public_Maxwell_Hodge_Poynting_theorem_zero | true | CONDITIONAL_PUBLIC_MAXWELL_NOT_PARENT_SIGNED | 0.000000e+00 | 1.000000e+00 | dimensionless_fractional_EM_residual | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3343_PUBLIC_MAXWELL_ACTION_DERIVATION.csv | EMD3343_4_vertical_zero | Maxwell_EM_stress_Poynting | ABS_SUM_NO_CANCELLATION | false | false | 3341 accepts theorem-zero only with PARENT_SIGNED_HSC3340; HSC3340_4 remains unsigned. |
| CAND3343_FRV3340_4_epsilon_EM_finite_incomplete | FRV3340_4_epsilon_EM | epsilon_EM | finite_residual_decomposition_nonclaim | false | NONE | MISSING_B_ALPHA_DELTA_J_DELTA_STAR_POYNTING_NUMERIC_SUM | 1.000000e+00 | dimensionless_fractional_EM_residual | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3343_EPSILON_EM_RESIDUAL_DECOMPOSITION.csv | epsilon_EM <= \|b_alpha\| + \|delta_J\| + \|delta_star\| + \|\|P_EM DeltaT_EM\|\|/\|\|T_EM\|\| + \|Phi_Poynting_unclosed\| | Maxwell_EM_stress_Poynting | ABS_SUM_NO_CANCELLATION | false | false | finite numeric source-backed values for every residual subterm are not filled. |

## Poynting Double-Count Guard
| guard_id | rule | allowed | forbidden | why | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| DCG3343_0_clean_route | EM waves and Poynting flux are counted through Hilbert T_EM in the clean public Maxwell branch. | true | false | This preserves local GR/Maxwell stress coupling and avoids a new fifth-force channel. | false |
| DCG3343_1_double_count | Do not add a second Poynting/background-force source if the same EM flux is already included in T_EM. | false | true | The same energy flux would source curvature twice unless a separate parent vertex and subtraction rule are derived. | false |
| DCG3343_2_direct_vertex | Any f(psi)F^2, psi J.A, or nonmetric constitutive term is a named epsilon_EM residual, not a quiet improvement. | conditional_parent_derived_and_bounded | as_unlabelled_closure | It opens clocks, WEP, optical propagation, R10, and source-current tests. | false |

## Promotion Gates
| gate_id | claim | passed | reason | valid_for_claim |
| --- | --- | --- | --- | --- |
| GATE3343_0_public_action_derivation | public Maxwell action gives Hilbert EM stress and Poynting flux law | true | 3343 records the action, metric variation, current variation, and Poynting balance identities. | false |
| GATE3343_1_poynting_double_count_guard | Poynting is routed through T_EM, not added as a second force | true | double-count guard forbids separate Poynting-background source unless parent-derived and bounded. | false |
| GATE3343_2_parent_signed_epsilon_zero | epsilon_EM=0 is parent-signed for MTS | false | HSC3340_4_public_Maxwell_Hodge remains conditional with hidden F2/Hodge/current closure unsigned. | false |
| GATE3343_3_finite_numeric_epsilon_bound | finite numeric epsilon_EM row is score-ready | false | b_alpha, delta_J, delta_star, DeltaT_EM, and Poynting subterms do not yet have a complete source-backed absolute-sum vector. | false |
| GATE3343_4_local_GR_claim | local-GR source-coupling branch is claim-ready | false | epsilon_EM theorem-zero is conditional only and other FRV3340 components remain open. | false |

## Decision Ledger
| decision_id | question | answer | reason | next_action | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| DEC3343_0 | Should Poynting be treated as the missing separate background field force? | no, not on the least-scrutiny route | If EM is public Maxwell, Poynting is already a component/flux of T_EM. Adding it again double-counts unless a new parent vertex is explicitly derived. | Keep Poynting inside Hilbert EM stress and attack the hidden Z_Q/current/Hodge clauses. | false |
| DEC3343_1 | Did 3343 close epsilon_EM? | not yet | It derives the zero theorem shape, but parent ownership of Z_Q, current lattice, Hodge/readout, and boundary flux is still unsigned. | Try no-hidden-Z_Q first because it controls b_alpha and alpha-readout drift without needing to predict the numerical value of alpha. | false |

## Next Target
| target_id | target_script | objective | why_next | valid_for_claim |
| --- | --- | --- | --- | --- |
| 3344-Y5-R2FR-no-hidden-ZQ-or-alpha-drift-bound-under-AX1090.md | scripts/Y5_R2FR_3344_no_hidden_ZQ_or_alpha_drift_bound.py | prove Z_Q is q-basic/constant on the local branch, or stage source-backed alpha-drift/readout bounds for b_alpha without claiming epsilon_EM closure | b_alpha is the first residual in epsilon_EM and 3289/3290 already isolate the exact hidden coefficient obstruction. | false |
| 3344b-Y5-R2FR-source-current-universality-or-deltaJ-bound.md | scripts/Y5_R2FR_3344b_source_current_universality_or_deltaJ_bound.py | prove fixed Noether charge/current lattice or turn existing WEP/R10 current-normalization rows into a source-backed delta_J component | delta_J is second EM residual and directly links EM charge/current to WEP/R10 source-coupling tests. | false |
