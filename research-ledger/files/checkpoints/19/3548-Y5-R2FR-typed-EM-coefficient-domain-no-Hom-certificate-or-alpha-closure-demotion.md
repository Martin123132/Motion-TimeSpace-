# 3548 — Typed EM coefficient-domain no-Hom certificate or alpha closure demotion

## Verdict

- **The no-Hom theorem is exact but not parent-signed.** If the parent object-language really restricts visible coefficients to `q_obs`, fixed representation data and topological/level constants, then `f_X(Phi)F_Q^2` and `c_X(Phi)A.J` are untypeable.
- **The current corpus does not prove that restriction.** Existing audits repeatedly keep the parent signature, unique curvature norm, no-extension rule and readout/radiative closure unsigned.
- **Alpha is therefore demoted to disciplined closure:** use measured `alpha_0` for baseline local Maxwell stress, and keep any active nonzero alpha/source branch behind the finite gates.
- **Main spine resumes at source calibration:** local GR/Newton should now attack the Hilbert source denominator, especially `R_PiM + R_Htau`, rather than looping around alpha.

## Certificate Clauses

| clause_id | certificate_clause | formal_requirement | would_forbid | verdict |
| --- | --- | --- | --- | --- |
| CERT3548_0_parent_object_language | parent action domain is fixed before readout/fitting | S_parent object language declares fields, coefficient sorts, allowed constructors and readout order | post-hoc hidden-visible coefficient closures | NOT_SIGNED |
| CERT3548_1_visible_coefficient_domain | visible coefficient slots exclude hidden/local representative arguments | Arg(Coeff(F_Q^2)) and Arg(Coeff(A.J)) subset {q_obs, fixed representation data, topological/level constants} | f_X(Phi)F_Q^2 and c_X(Phi)A.J | POWERFUL_BUT_UNSIGNED |
| CERT3548_2_no_extension_marker | no hidden invariant, domain selector or material marker can be retyped as coefficient data | no extension functor C_hid -> Coeff_vis and no marker labels enter visible coefficients | renamed scalar or source marker leakage into alpha/source coupling | UNSIGNED |
| CERT3548_3_unique_curvature_norm | the EM kinetic term is inherited from one parent curvature norm | no independent visible lambda_A F_Q^2 counterterm in addition to hidden-visible no-Hom | constant or visible Maxwell normalization counterterm being mistaken for a derived alpha | UNSIGNED |
| CERT3548_4_same_current_owner | A.J current normalization is owned by the same parent generator/current before readout | J_Q = delta S_matter/delta A_Q with fixed representation weights and no c_X(Phi) prefactor | current-prefactor branch z_g != 0 | UNSIGNED |
| CERT3548_5_readout_radiative_closure | EFT, clocks, material response and lab readout preserve the same coefficient domain | S_eff and observable maps stay in Alg[q_obs, fixed representation data, level constants] | readout-regenerated alpha/source coupling after a bare action theorem | UNSIGNED_CRITICAL |

## Slot Verdicts

| slot_id | operator_slot | dangerous_term | conditional_typing_result | current_result | route |
| --- | --- | --- | --- | --- | --- |
| SLOT3548_0_hidden_F2 | Coeff(F_Q^2) | f_X(Phi) F_Q^2 | ill-typed if CERT3548_0,1,2,5 are signed | RETAINED_COUNTERMODEL | finite alpha product bound or parent certificate |
| SLOT3548_1_visible_lambda | Coeff(F_Q^2) | lambda_A F_Q^2 as independent visible counterterm | not killed by no-Hom alone; requires unique parent curvature norm | RETAINED_CALIBRATED_CONSTANT_BRANCH | calibrated alpha baseline; no derived-alpha claim |
| SLOT3548_2_current_prefactor | Coeff(A.J) | c_X(Phi) A_mu J^mu | ill-typed if same current owner and no source/current prefactor grammar are signed | RETAINED_COUNTERMODEL | source-current owner theorem or finite source-normalization bound |
| SLOT3548_3_readout_F2 | Coeff(S_eff/readout F_Q^2) | f_eff(Phi) F_Q^2 after loop/readout reduction | excluded only if radiative/readout closure preserves the typed domain | RETAINED_COUNTERMODEL | direct observable bound rows or readout theorem |

## Demotion Ledger

| demotion_id | route | decision | because | allowed_use | forbidden_use |
| --- | --- | --- | --- | --- | --- |
| DEM3548_0_noHom_route | typed EM coefficient-domain no-Hom theorem | DEMOTE_TO_CONDITIONAL_CONTRACT | the theorem is exact if the grammar is signed, but current evidence repeatedly shows the parent signature is not derived | private discipline contract and future proof target | b_alpha=0, C_XF2=0, or local-GR source coupling claim |
| DEM3548_1_alpha_baseline | local alpha in baseline Maxwell stress | CALIBRATED_CLOSURE_ALLOWED | measured alpha_0 can play the same local-effective-theory role as measured G_N, provided it is labelled as calibration | compute Maxwell stress and Poynting/Hilbert bookkeeping in the baseline local branch | derived-alpha public claim or cancellation of active source residuals |
| DEM3548_2_active_alpha_branch | nonzero alpha/source coupling branch | FINITE_BOUND_BRANCH_ONLY | f_X(Phi)F_Q^2 and c_X(Phi)A.J remain live countermodels | score future sourced products against 1.372549e-12 or 1.407170e-12 gates | placeholder K_e_alpha*b_alpha or bound inversion as MTS prediction |
| DEM3548_3_project_spine | main local GR/Newton source-coupling spine | RETURN_TO_HILBERT_SOURCE_DENOMINATOR | alpha is now quarantined and no longer needs to block the source-current/Poisson/PPN bridge | continue with Pi_M/H_tau/ell_J/source denominator derivation | using alpha no-Hom failure as a reason to stop local GR/Newton work |

## Source-Coupling Handoff

| handoff_id | sector | current_state | next_owner | local_gr_relevance |
| --- | --- | --- | --- | --- |
| HAND3548_0_alpha | Maxwell/alpha | calibrated baseline plus finite active-branch bounds | only revisit if parent coefficient-domain certificate or numeric product appears | baseline Maxwell stress is usable conditionally; alpha theorem-zero is not required for next Newton bridge step |
| HAND3548_1_source_current | Hilbert source denominator | z_ellJ exact decomposition exists but Pi_M/H_tau owner remains open | R_PiM + R_Htau source-current square residual | this is the direct route to calibrated Newtonian source mass and PPN residuals |
| HAND3548_2_poynting | EM stress/Poynting | static bound EM stress belongs in T_total; exterior radiative flux remains a source/time-hair residual | source-current flux closure and Gdot/clock bound rows if nonzero | Poynting should police source conservation, not substitute for alpha no-Hom proof |

## Decisions

| decision_id | question | decision | basis | consequence |
| --- | --- | --- | --- | --- |
| DEC3548_0_certificate | Does the current corpus prove the typed EM no-Hom certificate? | NO | 2659/1235/1319 all preserve the exact conditional theorem but record missing parent signature, unique curvature norm, no-extension and readout clauses | do not claim b_alpha=0 or C_XF2=0 from this route |
| DEC3548_1_alpha_policy | Can alpha be used in the local framework without finishing the parent derivation? | YES_AS_CALIBRATED_BASELINE_ONLY | 3528 calibrated alpha contract already separates measured alpha_0 from active residual branches | Maxwell stress/Poynting bookkeeping can proceed while active alpha branches remain bounded |
| DEC3548_2_next_route | What is the best next move for the full goal? | RETURN_TO_HILBERT_SOURCE_DENOMINATOR | local GR/Newton depends most directly on M_H/Pi_M/H_tau/source-current closure, not on deriving alpha's numerical value | 3549 targets the Pi_M/H_tau Newton bridge rather than another alpha loop |

## Validation

| validation_id | passes | status | detail |
| --- | --- | --- | --- |
| VAL3548_0_sources_exist | True | PASS | all cited 3548 source paths exist |
| VAL3548_1_generated_csvs_parse | True | PASS | 9 generated CSV files parse with DictReader |
| VAL3548_2_certificate_not_signed | True | PASS | no typed no-Hom certificate clause is promoted as signed |
| VAL3548_3_demotion_nonclaim | True | PASS | alpha/no-Hom demotion rows remain nonclaim |
| VAL3548_4_countermodels_retained | True | PASS | F2, current-prefactor and readout slot countermodels are not silently erased |
| VAL3548_5_formalization_workbench_untouched | True | PASS | 3548 generated outputs only inside post-checkpoint-work |

## Next target

Move to `3549-Y5-R2FR-Hilbert-source-denominator-PiM-Htau-local-Newton-bridge.md`. The aim is to derive or bound the source denominator bridge behind Newton/Poisson/PPN: `M_H_ref`, `Pi_M`, `H_tau`, `H_ref`, and the residual `R_PiM+R_Htau`.

Generated UTC: 2026-06-29T11:11:06.553477+00:00