# 4495 Y5/R2FR - Ward/Cohomology/Public Projection Theorem Or CDeltaKTF Closure Comparator

Private post-checkpoint mirror for:

`D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\511-PPC4161-Ward-cohomology-public-projection-theorem-or-CDeltaKTF-closure-comparator.md`

## What Actually Moved

4495 keeps the good theorem but cages it properly: support-separated compact collars get conditional zero; generic `DeltaKTF` shell gets an explicit comparator, not a pretend theorem.

## Theorem And Comparator

| attempt_id | route | target_statement | derivation_status | reason | effect_on_C_DeltaKTF | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| WCP4495_0_Ward_identity | transition Ward/anomaly-inflow identity | delta_g S_bulk[DeltaKTF] + delta_g S_boundary[DeltaKTF] = 0 while ordinary matter still has delta S_m/delta g != 0 | NOT_DERIVED | Current corpus repeatedly says no transition Ward/anomaly identity is present for this branch. | no zero theorem | False |
| WCP4495_1_support_separated_cohomology | support-separated exact/no-flux local collar | If supp(DeltaKTF/transition stress) is outside W_loc and side/interface pullbacks plus Hamiltonian boundary terms vanish or are routed, local transition response is zero through <=2PN. | CONDITIONAL_SPECIAL_CASE_DERIVED | 192/4176 establish J_tr^nu=0 in compact no-flux local collars; 4288 imports the finite-margin AJ zero in that restricted domain. | C_DeltaKTF_effective=0 only for support-separated compact-collar branch | False |
| WCP4495_2_terminal_public_metric | terminal public metric/coframe alone | terminal public metric exists, therefore all non-public representative couplings vanish | REJECTED | 4276 countermodels show terminality alone does not force action-domain descent or eliminate labels, source weights, field renames, or kernel motion. | does not set C_DeltaKTF=0 | False |
| WCP4495_3_matter_interface_action_domain | terminal public metric plus matter-interface descent | S_matter=Sbar[Psi, Eval(e_pub(q(Phi))), theta(q)] and Dg_public[DeltaK_TF]=0 with no shadow labels or field-rename tails | BEST_THEOREM_TARGET_NOT_SIGNED | 4276 identifies this as the stronger surviving route, but it is not parent-signed in the current chain. | could set zero if derived, but not current evidence | False |
| WCP4495_4_explicit_closure | finite C_DeltaKTF closure comparator | Keep C_DeltaKTF visible and test it against 4493/4494 maxima instead of hiding it as a theorem. | IMPLEMENTED_AS_COMPARATOR | 4494 made this the only currently honest route for generic DeltaKTF. | numeric pass/fail comparator, no derived zero | False |

| zero_id | branch | conditions | derived_result | sets_C_DeltaKTF_zero | scope | not_scope | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CZ4495_0_domain | support_separated_compact_local_collar | supp(T_local) subset int(W_loc); supp(DeltaKTF/transition shell) outside W_loc or side/interface pullbacks vanish | J_tr^nu=0 through <=2PN in W_loc | True | conditional private selector branch only | generic transition shell or nonzero boundary/domain-wall response | False |
| CZ4495_1_boundary | fixed_or_routed_boundary_Hamiltonian_charge | delta H_tau fixed, zero, or explicitly routed; no unrouted C_side/I_sector pullback | boundary flux is not hidden bulk local metric response | True | local no-flux/collar calculation | radiative or transition boundary treated as invisible without routing | False |
| CZ4495_2_AJ_import | finite_margin_AJ_support_separated_window | 4288 support-separated compact local collar; R_transport_to_local=R_Bgrad_to_local=0 | A_J,eff_private=0 in the finite-margin window | True | AJ/cGamma side-channel in compact collar | DeltaKTF transition shell profile or public local-GR claim | False |
| CZ4495_3_generic_shell | generic_transition_shell | transition support intersects local collar or finite boundary/domain-wall response survives | no zero theorem; must use explicit C_DeltaKTF closure comparator or source real shell profiles | False | generic branch verdict | not a theorem-zero branch | False |

| summary_id | profile_id | abs_sK2_kappaSTF | required_CDeltaKTF_max | passing_trial_count | largest_passing_trial_CDeltaKTF | unit_CDeltaKTF_passes | exact_zero_required | status | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CTS4495_PSEL4489_0_smoothstep_minN4_candidate_1.000000000000000e+09 | PSEL4489_0_smoothstep_minN4_candidate | 1.000000000000000e+09 | 3.048717236713601e-23 | 5 | 1.000000000000000e-23 | False | False | COMPARATOR_READY_NONCLAIM | False |
| CTS4495_PSEL4489_0_smoothstep_minN4_candidate_1.000000000000000e+11 | PSEL4489_0_smoothstep_minN4_candidate | 1.000000000000000e+11 | 0.000000000000000e+00 | 1 | 0.000000000000000e+00 | False | True | COMPARATOR_READY_NONCLAIM | False |
| CTS4495_PSEL4489_1_balanced_Fpp_jump_1.000000000000000e+11 | PSEL4489_1_balanced_Fpp_jump | 1.000000000000000e+11 | 4.116843186890008e-25 | 3 | 1.000000000000000e-25 | False | False | COMPARATOR_READY_NONCLAIM | False |
| CTS4495_PSEL4489_1_min_N4_exact_EL_scan_1.000000000000000e+11 | PSEL4489_1_min_N4_exact_EL_scan | 1.000000000000000e+11 | 1.633797482706481e-26 | 2 | 1.000000000000000e-26 | False | False | COMPARATOR_READY_NONCLAIM | False |

| trial_id | profile_id | abs_sK2_kappaSTF | required_CDeltaKTF_max | trial_CDeltaKTF_label | trial_CDeltaKTF | passes_closure_limit | verdict | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CT4495_PSEL4489_0_smoothstep_minN4_candidate_1.000000000000000e+09_exact_zero | PSEL4489_0_smoothstep_minN4_candidate | 1.000000000000000e+09 | 3.048717236713601e-23 | exact_zero | 0.000000000000000e+00 | True | PASS_CLOSURE_COMPARATOR | False |
| CT4495_PSEL4489_0_smoothstep_minN4_candidate_1.000000000000000e+09_1e-26 | PSEL4489_0_smoothstep_minN4_candidate | 1.000000000000000e+09 | 3.048717236713601e-23 | 1e-26 | 1.000000000000000e-26 | True | PASS_CLOSURE_COMPARATOR | False |
| CT4495_PSEL4489_0_smoothstep_minN4_candidate_1.000000000000000e+09_1e-25 | PSEL4489_0_smoothstep_minN4_candidate | 1.000000000000000e+09 | 3.048717236713601e-23 | 1e-25 | 1.000000000000000e-25 | True | PASS_CLOSURE_COMPARATOR | False |
| CT4495_PSEL4489_0_smoothstep_minN4_candidate_1.000000000000000e+09_1e-24 | PSEL4489_0_smoothstep_minN4_candidate | 1.000000000000000e+09 | 3.048717236713601e-23 | 1e-24 | 9.999999999999999e-25 | True | PASS_CLOSURE_COMPARATOR | False |
| CT4495_PSEL4489_0_smoothstep_minN4_candidate_1.000000000000000e+09_1e-23 | PSEL4489_0_smoothstep_minN4_candidate | 1.000000000000000e+09 | 3.048717236713601e-23 | 1e-23 | 1.000000000000000e-23 | True | PASS_CLOSURE_COMPARATOR | False |
| CT4495_PSEL4489_0_smoothstep_minN4_candidate_1.000000000000000e+09_1e-22 | PSEL4489_0_smoothstep_minN4_candidate | 1.000000000000000e+09 | 3.048717236713601e-23 | 1e-22 | 1.000000000000000e-22 | False | FAIL_CDELTAKTF_TOO_LARGE | False |
| CT4495_PSEL4489_0_smoothstep_minN4_candidate_1.000000000000000e+09_1e-20 | PSEL4489_0_smoothstep_minN4_candidate | 1.000000000000000e+09 | 3.048717236713601e-23 | 1e-20 | 9.999999999999999e-21 | False | FAIL_CDELTAKTF_TOO_LARGE | False |
| CT4495_PSEL4489_0_smoothstep_minN4_candidate_1.000000000000000e+09_unit | PSEL4489_0_smoothstep_minN4_candidate | 1.000000000000000e+09 | 3.048717236713601e-23 | unit | 1.000000000000000e+00 | False | FAIL_CDELTAKTF_TOO_LARGE | False |
| CT4495_PSEL4489_0_smoothstep_minN4_candidate_1.000000000000000e+11_exact_zero | PSEL4489_0_smoothstep_minN4_candidate | 1.000000000000000e+11 | 0.000000000000000e+00 | exact_zero | 0.000000000000000e+00 | True | PASS_CLOSURE_COMPARATOR | False |
| CT4495_PSEL4489_0_smoothstep_minN4_candidate_1.000000000000000e+11_1e-26 | PSEL4489_0_smoothstep_minN4_candidate | 1.000000000000000e+11 | 0.000000000000000e+00 | 1e-26 | 1.000000000000000e-26 | False | FAIL_EXACT_ZERO_REQUIRED | False |
| CT4495_PSEL4489_0_smoothstep_minN4_candidate_1.000000000000000e+11_1e-25 | PSEL4489_0_smoothstep_minN4_candidate | 1.000000000000000e+11 | 0.000000000000000e+00 | 1e-25 | 1.000000000000000e-25 | False | FAIL_EXACT_ZERO_REQUIRED | False |
| CT4495_PSEL4489_0_smoothstep_minN4_candidate_1.000000000000000e+11_1e-24 | PSEL4489_0_smoothstep_minN4_candidate | 1.000000000000000e+11 | 0.000000000000000e+00 | 1e-24 | 9.999999999999999e-25 | False | FAIL_EXACT_ZERO_REQUIRED | False |
| CT4495_PSEL4489_0_smoothstep_minN4_candidate_1.000000000000000e+11_1e-23 | PSEL4489_0_smoothstep_minN4_candidate | 1.000000000000000e+11 | 0.000000000000000e+00 | 1e-23 | 1.000000000000000e-23 | False | FAIL_EXACT_ZERO_REQUIRED | False |
| CT4495_PSEL4489_0_smoothstep_minN4_candidate_1.000000000000000e+11_1e-22 | PSEL4489_0_smoothstep_minN4_candidate | 1.000000000000000e+11 | 0.000000000000000e+00 | 1e-22 | 1.000000000000000e-22 | False | FAIL_EXACT_ZERO_REQUIRED | False |
| CT4495_PSEL4489_0_smoothstep_minN4_candidate_1.000000000000000e+11_1e-20 | PSEL4489_0_smoothstep_minN4_candidate | 1.000000000000000e+11 | 0.000000000000000e+00 | 1e-20 | 9.999999999999999e-21 | False | FAIL_EXACT_ZERO_REQUIRED | False |
| CT4495_PSEL4489_0_smoothstep_minN4_candidate_1.000000000000000e+11_unit | PSEL4489_0_smoothstep_minN4_candidate | 1.000000000000000e+11 | 0.000000000000000e+00 | unit | 1.000000000000000e+00 | False | FAIL_EXACT_ZERO_REQUIRED | False |
| CT4495_PSEL4489_1_balanced_Fpp_jump_1.000000000000000e+11_exact_zero | PSEL4489_1_balanced_Fpp_jump | 1.000000000000000e+11 | 4.116843186890008e-25 | exact_zero | 0.000000000000000e+00 | True | PASS_CLOSURE_COMPARATOR | False |
| CT4495_PSEL4489_1_balanced_Fpp_jump_1.000000000000000e+11_1e-26 | PSEL4489_1_balanced_Fpp_jump | 1.000000000000000e+11 | 4.116843186890008e-25 | 1e-26 | 1.000000000000000e-26 | True | PASS_CLOSURE_COMPARATOR | False |
| CT4495_PSEL4489_1_balanced_Fpp_jump_1.000000000000000e+11_1e-25 | PSEL4489_1_balanced_Fpp_jump | 1.000000000000000e+11 | 4.116843186890008e-25 | 1e-25 | 1.000000000000000e-25 | True | PASS_CLOSURE_COMPARATOR | False |
| CT4495_PSEL4489_1_balanced_Fpp_jump_1.000000000000000e+11_1e-24 | PSEL4489_1_balanced_Fpp_jump | 1.000000000000000e+11 | 4.116843186890008e-25 | 1e-24 | 9.999999999999999e-25 | False | FAIL_CDELTAKTF_TOO_LARGE | False |
| CT4495_PSEL4489_1_balanced_Fpp_jump_1.000000000000000e+11_1e-23 | PSEL4489_1_balanced_Fpp_jump | 1.000000000000000e+11 | 4.116843186890008e-25 | 1e-23 | 1.000000000000000e-23 | False | FAIL_CDELTAKTF_TOO_LARGE | False |
| CT4495_PSEL4489_1_balanced_Fpp_jump_1.000000000000000e+11_1e-22 | PSEL4489_1_balanced_Fpp_jump | 1.000000000000000e+11 | 4.116843186890008e-25 | 1e-22 | 1.000000000000000e-22 | False | FAIL_CDELTAKTF_TOO_LARGE | False |
| CT4495_PSEL4489_1_balanced_Fpp_jump_1.000000000000000e+11_1e-20 | PSEL4489_1_balanced_Fpp_jump | 1.000000000000000e+11 | 4.116843186890008e-25 | 1e-20 | 9.999999999999999e-21 | False | FAIL_CDELTAKTF_TOO_LARGE | False |
| CT4495_PSEL4489_1_balanced_Fpp_jump_1.000000000000000e+11_unit | PSEL4489_1_balanced_Fpp_jump | 1.000000000000000e+11 | 4.116843186890008e-25 | unit | 1.000000000000000e+00 | False | FAIL_CDELTAKTF_TOO_LARGE | False |
| CT4495_PSEL4489_1_min_N4_exact_EL_scan_1.000000000000000e+11_exact_zero | PSEL4489_1_min_N4_exact_EL_scan | 1.000000000000000e+11 | 1.633797482706481e-26 | exact_zero | 0.000000000000000e+00 | True | PASS_CLOSURE_COMPARATOR | False |
| CT4495_PSEL4489_1_min_N4_exact_EL_scan_1.000000000000000e+11_1e-26 | PSEL4489_1_min_N4_exact_EL_scan | 1.000000000000000e+11 | 1.633797482706481e-26 | 1e-26 | 1.000000000000000e-26 | True | PASS_CLOSURE_COMPARATOR | False |
| CT4495_PSEL4489_1_min_N4_exact_EL_scan_1.000000000000000e+11_1e-25 | PSEL4489_1_min_N4_exact_EL_scan | 1.000000000000000e+11 | 1.633797482706481e-26 | 1e-25 | 1.000000000000000e-25 | False | FAIL_CDELTAKTF_TOO_LARGE | False |
| CT4495_PSEL4489_1_min_N4_exact_EL_scan_1.000000000000000e+11_1e-24 | PSEL4489_1_min_N4_exact_EL_scan | 1.000000000000000e+11 | 1.633797482706481e-26 | 1e-24 | 9.999999999999999e-25 | False | FAIL_CDELTAKTF_TOO_LARGE | False |
| CT4495_PSEL4489_1_min_N4_exact_EL_scan_1.000000000000000e+11_1e-23 | PSEL4489_1_min_N4_exact_EL_scan | 1.000000000000000e+11 | 1.633797482706481e-26 | 1e-23 | 1.000000000000000e-23 | False | FAIL_CDELTAKTF_TOO_LARGE | False |
| CT4495_PSEL4489_1_min_N4_exact_EL_scan_1.000000000000000e+11_1e-22 | PSEL4489_1_min_N4_exact_EL_scan | 1.000000000000000e+11 | 1.633797482706481e-26 | 1e-22 | 1.000000000000000e-22 | False | FAIL_CDELTAKTF_TOO_LARGE | False |
| CT4495_PSEL4489_1_min_N4_exact_EL_scan_1.000000000000000e+11_1e-20 | PSEL4489_1_min_N4_exact_EL_scan | 1.000000000000000e+11 | 1.633797482706481e-26 | 1e-20 | 9.999999999999999e-21 | False | FAIL_CDELTAKTF_TOO_LARGE | False |
| CT4495_PSEL4489_1_min_N4_exact_EL_scan_1.000000000000000e+11_unit | PSEL4489_1_min_N4_exact_EL_scan | 1.000000000000000e+11 | 1.633797482706481e-26 | unit | 1.000000000000000e+00 | False | FAIL_CDELTAKTF_TOO_LARGE | False |

## Gates And Decisions

| gate_id | requirement | passed | claim_allowed | reason | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| CG4495_0_sources | all cited source paths exist and needles are found | True | False | source-backed private theorem/comparator checkpoint | False |
| CG4495_1_conditional_zero_scope | conditional no-flux zero exists but is scoped | True | False | closed only in support-separated compact collars | False |
| CG4495_2_generic_theorem_not_derived | generic Ward/public-projection theorem is not claimed | True | False | terminality and Ward shortcuts are blocked | False |
| CG4495_3_comparator_rows | closure comparator rows exist for every closure contract and trial value | True | False | closure coefficients are explicit | False |
| CG4495_4_smoothstep_1e9_scale | smoothstep 1e9 allows tiny trials but rejects unit C_DeltaKTF | True | False | scale discipline preserved | False |
| CG4495_5_local_GR | local-GR/J2/PPN claim | False | False | generic DeltaKTF remains explicit closure or needs real shell/profile theorem | False |

| decision_id | finding | reason | effect | next_action | valid_for_claim |
| --- | --- | --- | --- | --- | --- |
| DEC4495_0_conditional_zero | support-separated compact collars retain a real conditional zero theorem | 192/4176 no-flux clauses plus 4288 finite-margin import close local transition/AJ leakage in that restricted domain | this branch can be used as a private selector, not as generic shell local-GR proof | 4496-Y5-R2FR-real-DeltaKTF-shell-profile-inputs-or-terminal-projection-parent-theorem.md | False |
| DEC4495_1_generic_shell_not_zero | generic DeltaKTF transition shell remains nonzero/closure-only | Ward identity and terminal public projection are not parent-signed, and terminality alone has countermodels | generic branch must use explicit C_DeltaKTF comparator or real shell profiles | 4496-Y5-R2FR-real-DeltaKTF-shell-profile-inputs-or-terminal-projection-parent-theorem.md | False |
| DEC4495_2_comparator_ready | C_DeltaKTF closure comparator is executable | 4494 maxima are converted to pass/fail rows for trial closure coefficients | future empirical/local tests can include this lane transparently without smuggling a zero | 4496-Y5-R2FR-real-DeltaKTF-shell-profile-inputs-or-terminal-projection-parent-theorem.md | False |

| checkpoint | marker | claim_id | decision | support_separated_zero | generic_DeltaKTF_status | smoothstep_1e9_largest_passing_trial_CDeltaKTF | local_GR_claim | sharpest_open_clause | next_target | valid_for_claim | generated_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4495 | PPC4161_WARD_COHOMOLOGY_PUBLIC_PROJECTION_OR_CDELTAKTF_CLOSURE_COMPARATOR_4495 | L-337 | SUPPORT_SEPARATED_CONDITIONAL_ZERO_GENERIC_DELTAKTF_CLOSURE_COMPARATOR_READY_NONCLAIM | conditional_private_selector_only | explicit_CDeltaKTF_closure_or_real_shell_profiles_required | 1.000000000000000e-23 | False | real_DeltaKTF_shell_profile_or_parent_matter_interface_projection_theorem | 4496-Y5-R2FR-real-DeltaKTF-shell-profile-inputs-or-terminal-projection-parent-theorem.md | False | 2026-07-05T23:17:33+00:00 |

| next_id | target | objective | derive_first | fallback | risk | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- |
| NT4495_0 | 4496-Y5-R2FR-real-DeltaKTF-shell-profile-inputs-or-terminal-projection-parent-theorem.md | Either source/build real DeltaKTF transition-shell profile inputs for the comparator, or derive the stronger parent matter-interface/terminal-projection theorem that sets the coefficient to zero. | parent matter-interface action-domain descent with Dg_public[DeltaK_TF]=0 and no shadow labels | real shell/profile rows feeding C_DeltaKTF comparator across J2/PPN/clock/orbital arenas | using the support-separated collar zero outside its domain | False |

| checkpoint | marker | claim_id | decision | proof_result | fallback_result | claim_status | next_target | valid_for_claim | generated_utc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4495 | PPC4161_WARD_COHOMOLOGY_PUBLIC_PROJECTION_OR_CDELTAKTF_CLOSURE_COMPARATOR_4495 | L-337 | SUPPORT_SEPARATED_CONDITIONAL_ZERO_GENERIC_DELTAKTF_CLOSURE_COMPARATOR_READY_NONCLAIM | support-separated no-flux/cohomology branch gives a conditional private zero; generic Ward/public-projection theorem remains not derived | C_DeltaKTF closure comparator generated from 4494 maxima and trial coefficients | private_nonclaim | 4496-Y5-R2FR-real-DeltaKTF-shell-profile-inputs-or-terminal-projection-parent-theorem.md | False | 2026-07-05T23:17:33+00:00 |

## Sources

| checkpoint | source_id | source_kind | source_ref | local_path_exists | needle | needle_found | line_number | role | valid_for_claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4495 | SRC4495_00_formal510 | local | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\510-PPC4161-parent-public-metric-projection-CDeltaKTF-zero-or-local-branch-demotion.md | True | explicit closure-only unless a genuinely new parent theorem is added | True | 31 | 4494 handoff. | False |
| 4495 | SRC4495_01_closure4494 | local | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4494_CDELTAKTF_CLOSURE_CONTRACT.csv | True | CDC4494_PSEL4489_0_smoothstep_minN4_candidate_1.000000000000000e+09 | True | 2 | 4494 closure maxima. | False |
| 4495 | SRC4495_02_formal192 | local | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\192-PPC4161-local-boundary-no-flux-sector-interface-theorem.md | True | J_tr^nu = 0 through <=2PN | True | 70 | 192 no-flux theorem. | False |
| 4495 | SRC4495_03_post4176 | local | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\4176-Y5-R2FR-local-boundary-no-flux-sector-interface-theorem-or-transition-current-bound.md | True | LOCAL_BOUNDARY_NO_FLUX_THEOREM_CLOSES_TRANSITION_CURRENT_PRIVATE_SELECTOR | True | 4 | 4176 no-flux checkpoint. | False |
| 4495 | SRC4495_04_post4276 | local | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\4276-Y5-R2FR-parent-gX-zero-no-shadow-theorem-or-first-canonical-gX-source-row.md | True | terminal metric exists => g_X=0 | True | 10 | 4276 terminality rejection. | False |
| 4495 | SRC4495_05_counter4276 | local | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4276_TERMINALITY_COUNTERMODEL_AUDIT.csv | True | CM4276_0_terminal_but_E_visible | True | 2 | 4276 terminality countermodels. | False |
| 4495 | SRC4495_06_post4288 | local | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\4288-Y5-R2FR-finite-margin-AJ-zero-domain-split-and-transition-frontier.md | True | A_J,eff_private=0 | True | 12 | 4288 support-separated AJ zero import. | False |
| 4495 | SRC4495_07_formal143 | local | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\143-boundary-topological-backup-gate.md | True | boundary_topological_backup_fails_transition_branch_demoted_closure_only | True | 37 | 143 generic backup failure. | False |
| 4495 | SRC4495_08_formal299 | local | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\formalization-workbench\299-PPC4161-transition-boundary-topological-superpotential-or-shell-profile-runner.md | True | generic boundary/topological route fails as a derivation | True | 13 | 299/4283 generic superpotential failure. | False |
| 4495 | SRC4495_09_gate | local | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\scripts\ward_cohomology_projection_gate.py | True | def closure_trial_rows | True | 125 | 4495 helper. | False |
| 4495 | SRC4495_10_generator | local | D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\scripts\Y5_R2FR_4495_Ward_cohomology_public_projection_theorem_or_CDeltaKTF_closure_comparator.py | True | CHECKPOINT = "4495" | True | 31 | 4495 generator script. | False |
