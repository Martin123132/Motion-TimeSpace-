# 1581 - R_AB q_R_hat Profile And Cassini Bound Row Or No-Charge Return

## Verdict
- The exterior current-hair profile is now explicit: with `W(r)=kappa_W r^2`, `R_AB=-Q_R/(kappa_W r)+O(r^-2)` after asymptotic flatness.
- Using the 1580 PPN bridge gives `q_R_hat=-Q_R/(2 kappa_W G M)+O(GM/r)`, so Cassini pressures the dimensionless reciprocal charge directly.
- If `kappa_W=1` and all tails vanish, the Cassini row implies the conditional target `|Q_R/(G M)| <= 4.6e-05`; this is not an MTS prediction or pass.
- The clean GR route is still `Q_R=0` plus tail silence from a parent source-boundary/no-charge theorem.
- No Cassini, PPN, local GR/Newton, no-charge, finite-hair, R10, WEP, clock, orbital, beta, or conservation claim is made.

## Source Register

| source_id | source_path | exists | needle_found | needles |
| --- | --- | --- | --- | --- |
| SRC1581_0_1580_doc | 1580-Y5-RAB-PPN-residual-vector-or-qRhat-source-row.md | True | True | NEXT_1581_RAB_QRHAT_PROFILE_AND_CASSINI_BOUND_ROW_OR_NO_CHARGE_RETURN; q_R_hat~sigma_Q Q_R/(2GM) |
| SRC1581_1_1580_validation | source-intake/mts_residuals/P8_Y5_BRR545_1580_VALIDATION.csv | True | True | VAL1580_OVERALL; PASS |
| SRC1581_2_1580_qrhat | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1580_QRHAT_SOURCE_ROW_NONCLAIM.csv | True | True | QRHAT1580_1_current_hair_target; CONDITIONAL_BOUND_TARGET_VALUE_MISSING |
| SRC1581_3_1580_cassini | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1580_CASSINI_BOUND_CONTRACT.csv | True | True | CAS1580_0_gamma_bound; 2.3e-05 |
| SRC1581_4_05_reciprocity | 05-reciprocity-theorem-attempt.md | True | True | W ~ r^2; R_AB ~ Q_R/r. |
| SRC1581_5_06_source_neutrality | 06-reciprocal-charge-source-neutrality.md | True | True | Pi_R = 0 -> Q_R = 0 -> R_AB = 0 -> AB = 1.; gamma - 1 ~= q_R. |
| SRC1581_6_1577_nocharge | source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1577_QR_NO_CHARGE_THEOREM_AUDIT.csv | True | True | NCA1577_4_verdict; NOT_DERIVED_CURRENT_CORPUS |
| SRC1581_7_local_bound_claims | source-intake/local_bounds/local_bound_claims.csv | True | True | Cassini_Shapiro_gamma_2003; gamma_minus_1; 2.3e-05 |

## q_R_hat Profile Derivation

| profile_id | object | equation | status | blocking_gap |
| --- | --- | --- | --- | --- |
| PROF1581_0_current_equation | exterior current equation | W(r) dR_AB/dr = Q_R | FORMAL_INPUT | ordinary current preserves Q_R rather than setting it to zero |
| PROF1581_1_asymptotic_weight | radial asymptotic weight | W(r)=kappa_W r^2[1+O(GM/r)] | CONDITIONAL_ASYMPTOTIC_GRAMMAR | kappa_W must be fixed by parent radial-cell normalization |
| PROF1581_2_profile | reciprocal hair profile | R_AB(r)=R_AB(infinity)-Q_R/(kappa_W r)+O(r^-2) | DERIVED_CONDITIONAL_PROFILE | sign convention and kappa_W normalization remain open |
| PROF1581_3_ppn_ratio | dimensionless q_R_hat | q_R_hat=R_AB/(2U_N)=-Q_R/(2 kappa_W G M)+O(GM/r) | DERIVED_CONDITIONAL_BOUND_TARGET | source mass M, kappa_W, gauge and tails remain unsourced |
| PROF1581_4_zero_route | derived GR route | Q_R=0 and tails=0 imply q_R_hat=0 and gamma_minus_1=0 at leading PPN order | SUFFICIENT_CONDITIONAL_NOT_PARENT_SIGNED | Pi_R=0/source-neutral boundary theorem is still not parent-derived |

## Cassini Q_R Bound Row

| bound_id | observable | conditional_bound_expression | q_R_hat_bound_if_tails_zero | QR_over_GM_bound_if_kappa1_tails_zero | current_status |
| --- | --- | --- | --- | --- | --- |
| CB1581_0_qRhat | q_R_hat + PPN tails | abs(-Q_R/(2 kappa_W G M)+delta_gauge+delta_source+delta_boundary) <= 2.3e-05 | 2.3e-05 | 4.6e-05 | CONDITIONAL_BOUND_ROW_NONCLAIM |
| CB1581_1_nocharge_limit | q_R_hat | Q_R=0 plus zero tails gives q_R_hat=0, automatically within Cassini gamma at leading order | 0 if no-charge theorem closes | 0 if no-charge theorem closes | SUFFICIENT_IF_PARENT_SIGNED_NOT_CLAIMED |

## No-Charge Return Audit

| audit_id | route | condition | status | why_not_claim |
| --- | --- | --- | --- | --- |
| NCR1581_0_source_boundary | Pi_R=0 source-boundary neutrality | Pi_R=0 -> Q_R=0 -> R_AB=0 -> AB=1 | SUFFICIENT_CONDITIONAL | 06 writes this route, but source boundary class is not parent-derived |
| NCR1581_1_free_variation | free/proper R_AB boundary variation | delta S_boundary=[W R_AB' + Pi_R] delta R_AB; if Pi_R=0 then Q_R=0 | OPEN_NOT_SIGNED | needs matter/source action to forbid hidden reciprocal momentum |
| NCR1581_2_constraint | constraint/no-pole return | lambda_R R_AB or no physical R_AB pole removes Q_R before PPN | OPEN_NOT_SIGNED | 1576 and 1577 keep multiplier/current-chain owner unsigned |
| NCR1581_3_finite_bound | finite hair fallback | if Q_R is not zero, Cassini bounds Q_R/(kappa_W GM) through q_R_hat | BOUND_TARGET_ONLY | bound target is not a prediction and cannot replace derived GR |
| NCR1581_4_verdict | best next route | return to Q_R no-charge/source denominator plus PPN tail envelope | NEXT_ROUTE | without Q_R=0 or a sourced Q_R value, Cassini cannot be scored |

## PPN Dry Run Update

| dry_run_id | arena | bound_expression | missing_for_score | dry_run_status |
| --- | --- | --- | --- | --- |
| PPN1581_0_Cassini_QR_bound | PPN/Cassini gamma | abs(-Q_R/(2 kappa_W G M)+tails) <= 2.3e-05 | Q_R value or Q_R=0 theorem; kappa_W normalization; source mass convention; gauge/source/boundary tails | NOT_RUN_BLOCKED |
| PPN1581_1_GR_zero_limit | derived local GR gamma channel | Q_R=0 and tails=0 -> gamma_minus_1=0 | parent no-charge theorem and tail silence | NOT_RUN_BLOCKED |

## Claim Gates

| gate_id | claim | status | reason |
| --- | --- | --- | --- |
| GATE1581_0_profile | q_R_hat radial profile is derived | PASS_FORMAL_NONCLAIM | profile follows conditionally from W R_AB'=Q_R and W~r^2 |
| GATE1581_1_Cassini_bound | Cassini gives a conditional Q_R/(GM) bound target | PASS_FORMAL_NONCLAIM | bound expression is algebraic but not a prediction |
| GATE1581_2_QR_value | Q_R value or Q_R=0 theorem exists | BLOCKED_NO_CLAIM | Q_R remains unsourced and no-charge theorem is unsigned |
| GATE1581_3_PPN_score | PPN/Cassini can be scored | BLOCKED_NO_CLAIM | kappa_W, source mass, gauge and tails are missing |
| GATE1581_4_local_GR | derived local GR/Newton branch | BLOCKED_NO_CLAIM | gamma channel alone is conditional and beta/conservation/common matter coupling remain open |

## Decision

| decision_id | decision | reason | consequence |
| --- | --- | --- | --- |
| DEC1581_0_progress | QRHAT_PROFILE_AND_CASSINI_BOUND_TARGET_DERIVED_CONDITIONALLY | finite reciprocal hair maps to q_R_hat=-Q_R/(2 kappa_W G M), giving a concrete Cassini pressure row | the local branch is now test-shaped, but not test-passed |
| DEC1581_1_claim_ceiling | NO_PPN_OR_GR_CLAIM | a bound target is not an MTS prediction while Q_R and tails are unknown | do not promote Cassini, PPN, or local-GR claims |
| DEC1581_2_next | NEXT_1582_QR_NO_CHARGE_SOURCE_DENOMINATOR_AND_TAIL_ENVELOPE | the least-scrutiny path is to prove Q_R=0/tails=0; the fallback path is a sourced finite Q_R/(GM) row | try the no-charge/source-boundary theorem with a PPN tail envelope |

## Validation

| check_id | result | detail |
| --- | --- | --- |
| VAL1581_0_sources_exist | PASS | all cited source paths exist |
| VAL1581_1_needles_found | PASS | all source needles found |
| VAL1581_2_profile_formula | PASS | q_R_hat profile relation is recorded |
| VAL1581_3_cassini_bound_target | PASS | conditional Cassini target bound on Q_R/(GM) is recorded |
| VAL1581_4_nocharge_not_claimed | PASS | no-charge route is selected as next route but not claimed |
| VAL1581_5_ppn_dry_run_blocked | PASS | PPN dry-run rows remain blocked |
| VAL1581_6_claim_gates_closed | PASS | claim gates remain nonclaim even when profile and bound target pass formally |
| VAL1581_7_decision_next | PASS | decision selects Q_R no-charge/source denominator and tail envelope |
| VAL1581_8_csv_parse | PASS | all generated 1581 CSVs parse cleanly |
| VAL1581_9_claim_flags_false | PASS | all generated prediction/claim flags remain false |
| VAL1581_10_no_raw_accepted | PASS | no 1581 rows written to raw/accepted finite directories |
| VAL1581_11_branch_copies | PASS | branch/quarantine nonclaim copies written |
| VAL1581_12_pycache_absent | PASS | scripts __pycache__ absent after run |
| VAL1581_13_formalization_untouched | PASS | all generated 1581 paths are outside formalization-workbench; git status is clean when available |
| VAL1581_OVERALL | PASS | 1581 q_R_hat profile and Cassini bound-row validation |

## Next Target

| next_target | script | objective | do_not |
| --- | --- | --- | --- |
| 1582-Y5-QR-no-charge-source-denominator-and-tail-envelope.md | scripts/Y5_QR_no_charge_source_denominator_and_tail_envelope.py | prove Q_R=0 from source-boundary/no-charge conditions or construct the absolute PPN tail/source-denominator envelope needed before any Cassini score | do not claim local GR from the conditional q_R_hat profile; do not cancel tails; do not score Cassini without Q_R and kappa_W/source normalization |
