# 509 - Source-Measure M_eff Flux Closure After Kappa Gate

Generated: 2026-06-04T03:07:45.211795+00:00  
Run: `runs/20260604-170000-source-measure-Meff-flux-closure-after-kappa-gate`  
Status: `source_measure_Meff_flux_closure_contract_built_conditional_current_MTS_not_derived_residual_map_written`  
Claim ceiling: `conditional_source_measure_flux_only_no_measured_GM_Newton_PPN_or_local_GR_promotion`

## 1. Verdict

This checkpoint answers the next honest question after the kappa gate:

```text
Even if kappa/G_eff is constant, what makes measured GM the parent source charge?
```

The answer cannot be "because orbits fit it". That would smuggle the calibration back in.

The clean derivation route is:

```text
M_eff[W] = M_source[W]
         = integral_S Q_M[tau]
         = (4*pi*G_ref)^-1 integral_S Pi_M J_H

M_eff(S2)-M_eff(S1) = integral_A d(Pi_M J_H)
```

So `epsilon_radial_Meff -> 0` follows only if the parent action gives `d(Pi_M J_H)=0` in the source-free exterior and all extra source/charge channels are zero.

That is a real theorem route, but it is still **not derived for current MTS**. The current status is therefore:

```text
conditional source-measure flux theorem written;
MTS parent derivation still missing;
residual map active;
no local GR claim.
```

## 2. Theorem Rows

| theorem_id | statement | mathematical_form | result | status | MTS_current_status |
| --- | --- | --- | --- | --- | --- |
| T509_0_charge_identity_needed | After the conditional kappa gate, measured GM still requires M_eff to be the same parent source charge seen by the exterior Hilbert/Noether flux. | M_eff[W] = M_source[W] = integral_S Q_M[tau] = (4*pi*G_ref)^-1 integral_S Pi_M J_H | source measure and exterior mass flux are the same object only if the parent action owns the projector, observed time generator, and source pullback | conditional_required_identity | not_parent_derived |
| T509_1_flux_closure | If the projected Hilbert mass current is closed in the source-free exterior, then M_eff cannot drift radially between linked spheres. | M_eff(S2)-M_eff(S1) = integral_A d(Pi_M J_H); d(Pi_M J_H)=0 => epsilon_radial_Meff=0 | radial measured-mass leakage is zero only under the parent Ward/Euler/topological closure premise | conditional_corollary | closure_not_derived_for_current_MTS |
| T509_2_no_extra_mass_channel | The flux equality is invalid if non-EH, symplectic-boundary, projector-stress, memory, domain, range, or frame channels carry mass charge. | d(Pi_M J_H) = Delta_nonEH + Delta_symp + Delta_PiM + Delta_extra + Delta_frame + Delta_cal + Delta_PPN | all Delta terms must be derived zero or bounded before Newton/PPN/local-GR promotion | necessary_no_cheat_clause | residual_map_active |

## 3. Required Clauses

| clause_id | required_clause | mathematical_form | if_missing | current_status |
| --- | --- | --- | --- | --- |
| SM509_0_observed_generator | The same observed time/translation generator tau is used in matter source variation, exterior Hilbert charge, and orbital readout. | tau_source = tau_Hilbert = tau_orbit | measured GM may be a frame-mixed calibration rather than a derived source charge | not_parent_derived |
| SM509_1_source_current | The parent matter action defines a source current J_H from the observed coframe/metric variation before phenomenological readout. | J_H[tau] = delta S_matter / delta e_obs contracted with tau | M_eff can be fitted to matter rather than derived from matter | conditional |
| SM509_2_parent_mass_projector | Pi_M is fixed by the parent symplectic/projector algebra and is not tuned separately per source, radius, or test arena. | Pi_M: parent currents -> scalar mass charge | projector freedom can absorb failures and becomes a patch | not_parent_derived |
| SM509_3_flux_closure | The projected Hilbert mass current is closed in compact source-free exterior domains by a Ward/Euler/topological identity. | d(Pi_M J_H)=0 outside W | dln_Meff_dt and epsilon_radial_Meff remain physical residuals | not_parent_derived |
| SM509_4_worldtube_source_measure | The worldtube source measure equals the exterior parent charge on any linking sphere. | M_source[W] = integral_S Q_M[tau] = (4*pi*G_ref)^-1 integral_S Pi_M J_H | orbital mass is not yet proven to be the same as source mass | not_parent_derived |
| SM509_5_no_extra_channel | Boundary, non-Hilbert, projector-stress, memory, domain, range, and connection terms carry no independent mass charge. | Delta_nonEH = Delta_symp = Delta_PiM = Delta_extra = Delta_frame = 0 | local-GR branch needs residual bounds rather than a theorem | not_parent_derived |
| SM509_6_Gauss_orbital_calibration | The closed charge normalizes to the orbital inverse-square coefficient with one reference zero and one universal G_ref. | a_r = -G_ref M_source/r^2 + higher-order controlled terms | Newton recovery remains a readout assumption | not_parent_derived |
| SM509_7_second_order_PPN_stability | The same source charge remains stable through the beta/gamma PPN expansion and cannot hide second-order derivative hair. | gamma-1, beta-1, alpha_i, zeta_i residuals depend only on explicit Delta rows | local Newton may pass while local GR still fails | not_parent_derived |

## 4. Residual Map

| residual_id | if_theorem_missing | symbol | observable_lock | required_artifact | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| SMR509_0_Delta_flux | M_eff has time/radial leakage | dln_Meff_dt; epsilon_radial_Meff | Gdot/GMdot, orbital residuals, radial source normalization | P8_time_drift_residual_or_zero.csv and/or P8_radial_mu_profile_or_zero.csv | false |
| SMR509_1_Delta_PiM | mass projector carries unowned variation | Delta_PiM | source-normalized Newton branch, PPN projector hair | parent projector variation ledger or explicit Delta_PiM coefficient | false |
| SMR509_2_Delta_symp | boundary symplectic/reference term shifts exterior mass | Delta_symp | worldtube boundary/reference zero and orbital calibration | boundary charge reference-zero theorem or bound | false |
| SMR509_3_Delta_extra | non-EH/domain/memory/range/connection sector carries mass charge | Delta_extra; mu_extra | local PPN, fifth-force, source universality, clocks | extra-sector silence theorem by field or residual coefficient matrix | false |
| SMR509_4_Delta_cal | closed charge does not calibrate to observed inverse-square orbital GM | Delta_cal | Kepler/Newton readout and absolute mass normalization | Gauss/orbital calibration theorem or external calibration ledger | false |
| SMR509_5_Delta_frame | source frame and orbital/clock frame disagree | Delta_frame_source | WEP, frame preferred effects, clock/local source tests | single observed source-frame theorem or frame residual bound | false |
| SMR509_6_Delta_nonEH | operator charge differs from EH/Hilbert charge | Delta_nonEH | GR limit, PPN gamma/beta, non-EH force channels | local EH reduction and non-EH charge silence theorem | false |
| SMR509_7_Delta_PPN | source equality holds only at leading order | Delta_PPN | beta, gamma, perihelion, Shapiro, light bending, preferred-frame tests | second-order source-charge PPN expansion or explicit residual vector | false |

## 5. Gate Tests

| gate_id | gate | result | evidence |
| --- | --- | --- | --- |
| G509_0_kappa_carried_conditionally | constant kappa from 508 can be carried only as a conditional/global premise | pass_conditional | 508 status keeps kappa_Geff_silence_derived_for_MTS=false |
| G509_1_source_measure_equality | M_source[W] equals exterior parent mass charge before readout | fail_for_current_claim | CC3/CC4/CC7 and W504_4 remain not parent-derived |
| G509_2_flux_closure | d(Pi_M J_H)=0 is derived from parent Ward/Euler/topological structure | fail_for_current_claim | MF2/MF4/MF6 and SN4 remain conditional/not parent-derived |
| G509_3_residual_map_complete | failed source-measure identities are mapped to explicit residual rows | pass | residual_rows=8 |
| G509_4_no_local_GR_claim | no measured-GM/Newton/PPN/local-GR promotion is made from conditional source flux | pass | claim ceiling blocks promotion until source measure and PPN residuals close |

## 6. Decision

| decision_id | decision | meaning | claim_status |
| --- | --- | --- | --- |
| D509_0 | source_measure_flux_is_the_next_true_blocker | constant kappa is not enough; M_eff must be shown to be the conserved parent source charge | conditional_only |
| D509_1 | current_MTS_has_not_earned_Meff_closure | the clean theorem is now written, but the present corpus still lacks the parent identity d(Pi_M J_H)=0 and worldtube source-measure glue | Meff_conservation_derived_false |
| D509_2 | do_not_smuggle_orbital_GM | orbital GM cannot be treated as proof of source matching; it is either a derived Gauss/readout theorem or an external calibration ledger | Newton_promoted_false |
| D509_3 | next_branch_is_theorem_or_runner | either derive worldtube source-measure glue directly or build a residual runner for Delta_flux, Delta_PiM, Delta_symp, Delta_extra, Delta_cal, Delta_frame, Delta_nonEH, and Delta_PPN | 510-worldtube-source-measure-glue-or-Meff-residual-runner.md |

## 7. Source Register

| source_file | role | exists |
| --- | --- | --- |
| 508-constant-kappa-superselection-or-drift-residual.md | conditional constant-kappa gate carried forward, but measured GM still open | True |
| 505-parent-Noether-mass-charge-closure-theorem-or-closure-demotion.md | conditional parent Noether mass-charge closure theorem and open premises | True |
| 504-parent-Hilbert-worldtube-glue-or-external-radial-input-plan.md | worldtube/Hilbert glue decomposition and C-term ledger path | True |
| 501-topological-Hilbert-current-equality-or-radial-bound-runner.md | Hilbert-current equality attempt and radial-bound fallback | True |
| 498-source-normalization-radial-and-calibration-theorem-attempt.md | source-normalized Newton branch stack and radial/calibration blockers | True |
| 451-mass-flux-projector-Euler-calibration-attempt.md | mass-flux projector/Euler calibration contract | True |
| 454-PiM-parent-symplectic-projector-algebra-attempt.md | Pi_M parent symplectic projector algebra attempt | True |
| source-intake/mts_residuals/P8_mass_flux_projector_Euler_calibration_CONTRACT.csv | MF0-MF8 mass-flux source/projector/calibration requirements | True |
| source-intake/mts_residuals/P8_charge_current_equality_DIRECT_ATTEMPT.csv | CC0-CC8 direct source-charge equality blockers | True |
| source-intake/mts_residuals/P8_charge_current_equality_RESIDUAL_DECOMPOSITION.csv | Delta_frame, Delta_nonEH, Delta_symp, Delta_PiM, Delta_extra, Delta_flux, Delta_G, Delta_cal, Delta_PPN residuals | True |
| source-intake/mts_residuals/P8_source_normalized_Newton_branch_STACK.csv | SN3/SN4/SN8/SN9/SN10 open Newton-source branch rungs | True |
| source-intake/mts_residuals/P8_PARENT_WORLDTUBE_GLUE_THEOREM_CLAUSES.csv | worldtube source-measure equality and calibration clauses | True |
| source-intake/mts_residuals/P8_CONSTANT_GM_LOCAL_RESIDUAL_RUNNER_INPUT.csv | local residual runner input showing M_eff conservation is not currently scoreable | True |
| scripts/source_measure_Meff_flux_closure_after_kappa_gate.py | this checkpoint generator | True |

## 8. Validation

| check_id | result | detail |
| --- | --- | --- |
| V509_0_source_paths_exist | pass | missing=0 |
| V509_1_clause_stack_complete | pass | clause_rows=8 |
| V509_2_residual_map_complete | pass | residual_rows=8 |
| V509_3_claim_ceiling_enforced | pass | measured_GM_parent_derived=false; local_GR_claim_allowed=false |
| V509_4_next_target_set | pass | 510-worldtube-source-measure-glue-or-Meff-residual-runner.md |

## 9. Route Update

| route_id | status | update | next_target |
| --- | --- | --- | --- |
| RU509_0 | source_measure_flux_contract_sharpened | measured GM is now split into a parent source-measure theorem plus explicit residual fallback | 510-worldtube-source-measure-glue-or-Meff-residual-runner.md |
| RU509_1 | local_GR_still_blocked | without Pi_M current closure, worldtube source equality, and PPN stability, MTS cannot claim derived local GR | 510-worldtube-source-measure-glue-or-Meff-residual-runner.md |
| RU509_2 | derivation_path_kept_alive | the path is not dead; it has been reduced to exact premises a parent action must satisfy instead of a vague plateau/source axiom | 510-worldtube-source-measure-glue-or-Meff-residual-runner.md |

## 10. Claim Ceiling

Allowed:

```text
MTS has a precise conditional route for measured-GM/source-measure closure.
The missing identities are now localised to Pi_M current closure, worldtube glue, no-extra-channel silence, and PPN stability.
If those identities fail, each failure has a named residual.
```

Forbidden:

```text
MTS has derived measured GM.
MTS has derived Newtonian recovery from the current parent action.
MTS has derived local GR or PPN consistency.
MTS may hide M_eff drift inside orbital calibration.
```

## 11. What This Means

This is not a dead end. It is the opposite: the branch is now sharp enough to be falsifiable inside the formalism.

The local-GR route survives only if the next step can either:

```text
derive worldtube source-measure glue and d(Pi_M J_H)=0,
```

or, failing that,

```text
turn every nonzero Delta term into an explicit residual vector and show it is below local bounds.
```

## 12. Next Target

`510-worldtube-source-measure-glue-or-Meff-residual-runner.md`
