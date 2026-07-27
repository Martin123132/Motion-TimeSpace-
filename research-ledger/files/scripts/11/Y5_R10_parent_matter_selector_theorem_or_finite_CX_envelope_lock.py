from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
SCRIPT_REL = "scripts/Y5_R10_parent_matter_selector_theorem_or_finite_CX_envelope_lock.py"
DOC = ROOT / "613-Y5-R10-parent-matter-selector-theorem-or-finite-CX-envelope-lock.md"
STATUS = "Y5_R10_parent_matter_selector_theorem_attempted_conditional_only_finite_CX_envelope_locked"
CLAIM_CEILING = "selector_theorem_attempt_and_finite_CX_lock_only_no_R10_fifth_force_WEP_PPN_or_local_GR_pass"
NEXT_TARGET = "614-Y5-R10-lambda-X-parent-Hessian-window-or-CX-envelope-scorecard.md"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = fieldnames or (list(rows[0].keys()) if rows else [])
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def f(value: float) -> str:
    return f"{value:.12e}"


def parse_bool(value: object) -> bool:
    return str(value).strip().lower() == "true"


def md_table(rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> str:
    if not rows:
        return "_No rows._"
    fields = fieldnames or list(rows[0].keys())

    def cell(value: object) -> str:
        return str(value).replace("|", "\\|").replace("\n", " ")

    lines = [
        "| " + " | ".join(cell(field) for field in fields) + " |",
        "| " + " | ".join("---" for _ in fields) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(cell(row.get(field, "")) for field in fields) + " |")
    return "\n".join(lines)


def build_source_register() -> list[dict[str, object]]:
    sources = [
        ("612-Y5-R10-CX-component-source-derivation-or-real-bound-curve-promotion.md", "612 immediate handoff"),
        ("source-intake/mts_residuals/P8_Y5_BRR545_612_VALIDATION.csv", "prior validation gate"),
        ("source-intake/mts_residuals/P8_Y5_R10_612_NONCLAIM_SUMMARY.csv", "C_X pressure summary"),
        ("source-intake/mts_residuals/P8_Y5_R10_612_CX_SURVIVAL_WINDOWS.csv", "finite C_X survival windows"),
        ("source-intake/mts_residuals/P8_Y5_R10_612_LAMBDA_CX_CEILING_TABLE.csv", "lambda-specific C_X ceilings"),
        ("565-Y5-R10-coframe-pullback-zero-or-finite-alpha-coefficient.md", "vertical observation theorem"),
        ("source-intake/mts_residuals/P8_Y5_R10_565_VERTICAL_OBSERVATION_THEOREM.csv", "conditional pullback theorem rows"),
        ("source-intake/mts_residuals/P8_Y5_R10_565_COUNTEREXAMPLES.csv", "weak-premise counterexamples"),
        ("576-Y5-R10-constant-source-current-universality-or-qbar-envelope.md", "constant/source-current qbar attempt"),
        ("source-intake/mts_residuals/P8_Y5_R10_576_UNIVERSALITY_PREMISE_LEDGER.csv", "qbar premise ledger"),
        ("401-parent-matter-selector-theorem-attempt.md", "older parent selector theorem attempt"),
        ("410-quotient-matter-functor-theorem-attempt.md", "quotient matter functor attempt"),
        ("404-selector-blind-matter-axiom-origin.md", "selector-blind origin audit"),
        ("423-parent-action-minimality-no-extension-theorem-attempt.md", "no material marker extension attempt"),
        (SCRIPT_REL, "this checkpoint generator"),
    ]
    return [
        {"source_file": source_file, "exists": (ROOT / source_file).exists(), "role": role}
        for source_file, role in sources
    ]


def build_selector_theorem_rows() -> list[dict[str, object]]:
    return [
        {
            "theorem_id": "ST613_0_conditional_chain_rule",
            "claim": "If ordinary matter factors through observed geometry and X-independent constants, then delta_X S_matter=0.",
            "mathematical_condition": "S_m=sum_A S_A[Psi_A,Obs(Q),omega[Obs(Q)],theta_A], DObs(Dq[X])=0, L_X theta_A=0",
            "proof_status": "valid_conditional_theorem",
            "parent_status": "not_parent_signed",
            "buys_if_parent_signed": "qbar_XT=0 and ordinary matter pullback J_matter=0",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "ST613_1_vertical_kernel",
            "claim": "X must be a representative/vertical direction invisible to observed rods and clocks.",
            "mathematical_condition": "Dq[X]=0 and DObs(Dq[X])=0 on the local branch before variation",
            "proof_status": "sufficient_clause_identified",
            "parent_status": "open",
            "buys_if_parent_signed": "removes metric/coframe contribution to test-body X charge",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "ST613_2_constant_triviality",
            "claim": "Ordinary matter constants must not carry X, quotient, class, or marker dependence.",
            "mathematical_condition": "L_X theta_A=0 and no theta_A(I_Q), theta_A(C_D), theta_A(m), or theta_A(X)",
            "proof_status": "necessary_clause_identified",
            "parent_status": "open",
            "buys_if_parent_signed": "removes constant-sector fifth-force and clock/WEP leakage",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "ST613_3_no_marker_extension",
            "claim": "No material marker extension may be appended and then ignored.",
            "mathematical_condition": "Conf_parent is primitive-minimal or every nontrivial marker is varied and retained",
            "proof_status": "guardrail_valid",
            "parent_status": "minimality_theorem_not_derived",
            "buys_if_parent_signed": "prevents hidden spurion route back into qbar_XT",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "ST613_4_selector_result",
            "claim": "The parent matter-selector theorem is proved from the current corpus.",
            "mathematical_condition": "ST613_1 through ST613_3 all parent-signed",
            "proof_status": "attempted_rejected_for_claim",
            "parent_status": "fail_current_claim",
            "buys_if_parent_signed": "would move qbar_XT to theorem-zero",
            "valid_for_claim": "false",
        },
    ]


def build_parent_signature_rows() -> list[dict[str, object]]:
    return [
        {
            "signature_id": "PS613_0_chain_rule_math",
            "premise": "chain-rule silence of matter action",
            "source_status": "derived_conditionally_in_565_and_576",
            "signed": "conditional_only",
            "blocker": "requires parent-owned factorization and X-independent constants",
            "repair_route": "prove quotient matter functor from primitive parent action",
            "valid_for_claim": "false",
        },
        {
            "signature_id": "PS613_1_observed_quotient",
            "premise": "observed geometry is a functor of quotient data only",
            "source_status": "template_in_410",
            "signed": "conditional_only",
            "blocker": "quotient language alone allows marker-extended functors",
            "repair_route": "derive universal property of the primitive observed quotient",
            "valid_for_claim": "false",
        },
        {
            "signature_id": "PS613_2_X_verticality",
            "premise": "X lies in the observed quotient kernel",
            "source_status": "certificate_template_in_565",
            "signed": "no",
            "blocker": "finite X block is still treated as physical residual in the local branch",
            "repair_route": "show X is pure representative/gauge or lock finite exchange mode",
            "valid_for_claim": "false",
        },
        {
            "signature_id": "PS613_3_constant_sector",
            "premise": "ordinary constants are MTS-trivial representation data",
            "source_status": "failed_as_parent_derivation_in_576",
            "signed": "no",
            "blocker": "theta_A(X) and theta_A(I_Q) counterexamples remain legal",
            "repair_route": "constant-sector superselection theorem",
            "valid_for_claim": "false",
        },
        {
            "signature_id": "PS613_4_no_extension",
            "premise": "no material marker or source-dependent auxiliary extension",
            "source_status": "no-extension theorem attempted in_423",
            "signed": "policy_only",
            "blocker": "extended quotient Q_tilde=(Q,m)/G_rel remains legal",
            "repair_route": "primitive-minimal universal-property theorem",
            "valid_for_claim": "false",
        },
        {
            "signature_id": "PS613_5_same_frame_source",
            "premise": "same observed frame controls rods/clocks and active Hilbert source",
            "source_status": "conditional_Hilbert_sublemma_in_576",
            "signed": "partial_only",
            "blocker": "species-weighted kappa and measured-GM calibration are separate gates",
            "repair_route": "global-coupling superselection plus measured-mass projector theorem",
            "valid_for_claim": "false",
        },
    ]


def build_countermodel_rows() -> list[dict[str, object]]:
    return [
        {
            "countermodel_id": "CM613_0_universal_conformal_frame",
            "construction": "hat_g_mu_nu=exp(2F(X))g_mu_nu with common F for all ordinary species",
            "satisfies": "covariance, universal matter metric, species-blindness",
            "breaks": "partial_X hat_g=0; produces common qbar_XT and source pullback",
            "needed_blocker": "parent selector theorem forcing F_prime=0",
            "blocks_theorem_claim": "true",
        },
        {
            "countermodel_id": "CM613_1_selector_dependent_constants",
            "construction": "theta_A=theta_A0[1+epsilon_A X] or theta_A(I_Q)",
            "satisfies": "observed metric factorization if constants are allowed extra arguments",
            "breaks": "L_X theta_A=0; creates clock/WEP/fifth-force constant channel",
            "needed_blocker": "constant-sector triviality/superselection theorem",
            "blocks_theorem_claim": "true",
        },
        {
            "countermodel_id": "CM613_2_material_marker_extension",
            "construction": "extend quotient by a covariant material marker m and couple S_matter to m",
            "satisfies": "covariance and quotient language in the extended theory",
            "breaks": "no-marker assumption; returns hidden spurion/source charge",
            "needed_blocker": "primitive-minimal no-extension theorem",
            "blocks_theorem_claim": "true",
        },
        {
            "countermodel_id": "CM613_3_species_weighted_source",
            "construction": "E_mu_nu=sum_A kappa_A T_A_mu_nu with separately conserved T_A",
            "satisfies": "Bianchi compatibility under constant kappa_A",
            "breaks": "single universal active source coupling",
            "needed_blocker": "global-coupling superselection theorem",
            "blocks_theorem_claim": "true",
        },
        {
            "countermodel_id": "CM613_4_post_readout_EFT",
            "construction": "readout-level reduced action inserts X-dependent counterterm after parent variation",
            "satisfies": "can mimic a closure-zero row in the reduced description",
            "breaks": "parent theorem-zero credit",
            "needed_blocker": "readout-after-variation/no-backreaction theorem",
            "blocks_theorem_claim": "true",
        },
    ]


def build_finite_lock_rows(summary: dict[str, str], survival_rows: list[dict[str, str]]) -> list[dict[str, object]]:
    full_curve_ceiling = float(summary["tightest_full_curve_abs_CX_ceiling"])
    threshold_rows = {row["survival_id"]: row for row in survival_rows}
    return [
        {
            "lock_id": "FL613_0_selector_not_signed",
            "condition": "ST613 selector theorem remains conditional only",
            "locked_response": "do not set qbar_XT=0 in claim rows",
            "numeric_pressure": "finite C_X envelope remains active",
            "claim_status": "finite_branch_locked_nonclaim",
            "valid_for_claim": "false",
        },
        {
            "lock_id": "FL613_1_full_curve_safe_envelope",
            "condition": "want one C_X ceiling that clears every sampled review-candidate lambda",
            "locked_response": f"require |C_X| <= {f(full_curve_ceiling)}",
            "numeric_pressure": "private review-candidate curve only",
            "claim_status": "pressure_only",
            "valid_for_claim": "false",
        },
        {
            "lock_id": "FL613_2_order_100",
            "condition": "|C_X| around 100",
            "locked_response": "survives all sampled review-candidate lambda points",
            "numeric_pressure": f"passing_fraction={threshold_rows['SW612_C100']['passing_fraction']}",
            "claim_status": "pressure_only",
            "valid_for_claim": "false",
        },
        {
            "lock_id": "FL613_3_order_1000",
            "condition": "|C_X| around 1000",
            "locked_response": "allowed only in lambda windows; not whole-curve safe",
            "numeric_pressure": f"passing_fraction={threshold_rows['SW612_C1000']['passing_fraction']}; intervals={threshold_rows['SW612_C1000']['allowed_interval_count']}",
            "claim_status": "pressure_only",
            "valid_for_claim": "false",
        },
        {
            "lock_id": "FL613_4_order_1e5",
            "condition": "|C_X| around 1e5",
            "locked_response": "branch becomes range-sensitive; tens-of-microns windows matter",
            "numeric_pressure": f"passing_fraction={threshold_rows['SW612_C100000']['passing_fraction']}; intervals={threshold_rows['SW612_C100000']['allowed_interval_count']}",
            "claim_status": "pressure_only",
            "valid_for_claim": "false",
        },
        {
            "lock_id": "FL613_5_public_claim_gate",
            "condition": "R10 claim wanted",
            "locked_response": "must supply claim-grade bound curve plus parent-signed lambda_X and C_X",
            "numeric_pressure": "current review rows and symbolic coefficients are explicitly invalid for claim",
            "claim_status": "blocked",
            "valid_for_claim": "false",
        },
    ]


def build_selector_certificate_rows() -> list[dict[str, object]]:
    return [
        {
            "certificate_id": "SC613_0_parent_variable_split",
            "required_clause": "Parent configuration splits physical quotient data from representative selector data.",
            "mathematical_form": "Phi -> Q_phys, X in ker(Dq_phys)",
            "current_status": "not_derived",
            "if_missing": "X can remain a finite physical exchange mode",
            "valid_for_claim": "false",
        },
        {
            "certificate_id": "SC613_1_observed_geometry_functor",
            "required_clause": "Rods/clocks/matter see only observed quotient geometry.",
            "mathematical_form": "e_obs=Obs(Q_phys), L_X e_obs=0",
            "current_status": "conditional_template",
            "if_missing": "universal conformal frame countermodel survives",
            "valid_for_claim": "false",
        },
        {
            "certificate_id": "SC613_2_matter_factorization",
            "required_clause": "Ordinary matter action has no explicit selector/class/domain/memory argument.",
            "mathematical_form": "S_A=S_A[Psi_A,e_obs,omega[e_obs],theta_A]",
            "current_status": "not_parent_derived",
            "if_missing": "direct material X charge is legal",
            "valid_for_claim": "false",
        },
        {
            "certificate_id": "SC613_3_constant_triviality",
            "required_clause": "Matter constants are invariant representation data.",
            "mathematical_form": "L_X theta_A=0 for all ordinary A",
            "current_status": "not_parent_derived",
            "if_missing": "clock/WEP/fifth-force constant channels survive",
            "valid_for_claim": "false",
        },
        {
            "certificate_id": "SC613_4_no_extension",
            "required_clause": "No nontrivial material marker extension is available without being varied and retained.",
            "mathematical_form": "Conf_parent is primitive-minimal or extension tax applies",
            "current_status": "policy_not_theorem",
            "if_missing": "hidden spurion can re-enter local branch",
            "valid_for_claim": "false",
        },
        {
            "certificate_id": "SC613_5_qbar_zero_promotion",
            "required_clause": "All selector clauses pass simultaneously.",
            "mathematical_form": "SC613_0..SC613_4 => delta_X S_T=0 => qbar_XT=0",
            "current_status": "blocked",
            "if_missing": "finite C_X envelope remains mandatory",
            "valid_for_claim": "false",
        },
    ]


def build_decision_rows() -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D613_0_theorem_attempt",
            "status": "conditional_theorem_valid_not_parent_signed",
            "decision": "keep the matter-selector theorem as a precise future proof target",
            "meaning": "the chain-rule mathematics works, but the parent action has not earned the premises",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D613_1_finite_lock",
            "status": STATUS,
            "decision": "lock finite C_X envelope as the active branch until selector certificate closes",
            "meaning": "qbar_XT cannot be set to zero by assertion",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D613_2_best_next_route",
            "status": "lambda_window_scorecard_next",
            "decision": "derive or bound lambda_X from the parent Hessian next",
            "meaning": "range decides whether finite C_X is relaxed or punished by R10 pressure",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D613_3_claim_ceiling",
            "status": CLAIM_CEILING,
            "decision": "no R10, WEP, PPN, or local-GR pass",
            "meaning": "this is theorem discipline and envelope locking, not public evidence",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
    ]


def build_route_rows() -> list[dict[str, object]]:
    return [
        {
            "route_id": "RU613_0_allowed",
            "allowed_after_613": "cite the selector theorem only as a conditional proof target",
            "forbidden_after_613": "write qbar_XT=0 in claim rows without SC613 certificate closure",
            "next_action": NEXT_TARGET,
        },
        {
            "route_id": "RU613_1_allowed",
            "allowed_after_613": "score finite C_X against lambda windows using review-candidate pressure",
            "forbidden_after_613": "turn private pressure into an R10 pass",
            "next_action": NEXT_TARGET,
        },
        {
            "route_id": "RU613_2_allowed",
            "allowed_after_613": "return to selector theorem only if a new primitive-minimal quotient proof is supplied",
            "forbidden_after_613": "reopen selector-zero by vibes or elegance",
            "next_action": "primitive_quotient_theorem_later_if_needed",
        },
    ]


def build_summary_rows(summary_612: dict[str, str]) -> list[dict[str, object]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "selector_theorem_parent_signed": "false",
            "qbar_XT_zero_promoted": "false",
            "finite_CX_envelope_locked": "true",
            "tightest_full_curve_abs_CX_ceiling": summary_612["tightest_full_curve_abs_CX_ceiling"],
            "epsilon_shell": summary_612["epsilon_shell"],
            "review_candidate_rows": summary_612["review_candidate_rows"],
            "R10_pass": "false",
            "WEP_pass": "false",
            "PPN_pass": "false",
            "local_GR_pass": "false",
            "next_target": NEXT_TARGET,
        }
    ]


def build_validation_rows(
    source_register: list[dict[str, object]],
    prior_validation: list[dict[str, str]],
    theorem_rows: list[dict[str, object]],
    signature_rows: list[dict[str, object]],
    countermodel_rows: list[dict[str, object]],
    lock_rows: list[dict[str, object]],
    certificate_rows: list[dict[str, object]],
    decision_rows: list[dict[str, object]],
    summary_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    missing_sources = [row for row in source_register if not parse_bool(row["exists"])]
    prior_failures = [row for row in prior_validation if row.get("result") != "pass"]
    all_output_tables = [theorem_rows, signature_rows, lock_rows, certificate_rows, decision_rows, summary_rows]
    no_claim_rows = all(not parse_bool(row.get("valid_for_claim", "false")) for table in all_output_tables for row in table)
    countermodels_block = all(parse_bool(row["blocks_theorem_claim"]) for row in countermodel_rows)
    theorem_failed = any(row["theorem_id"] == "ST613_4_selector_result" and row["parent_status"] == "fail_current_claim" for row in theorem_rows)
    finite_locked = summary_rows[0]["finite_CX_envelope_locked"] == "true"
    return [
        {"check_id": "V613_0_source_paths_exist", "result": "pass" if not missing_sources else "fail", "detail": f"missing={len(missing_sources)}"},
        {"check_id": "V613_1_prior_612_clean", "result": "pass" if not prior_failures else "fail", "detail": f"prior_rows={len(prior_validation)};prior_failures={len(prior_failures)}"},
        {"check_id": "V613_2_selector_theorem_written", "result": "pass" if len(theorem_rows) >= 5 else "fail", "detail": f"theorem_rows={len(theorem_rows)}"},
        {"check_id": "V613_3_parent_signature_not_smuggled", "result": "pass" if theorem_failed else "fail", "detail": "selector_parent_status=fail_current_claim"},
        {"check_id": "V613_4_countermodels_block_weak_premises", "result": "pass" if countermodels_block else "fail", "detail": f"countermodels={len(countermodel_rows)}"},
        {"check_id": "V613_5_finite_CX_envelope_locked", "result": "pass" if finite_locked else "fail", "detail": f"lock_rows={len(lock_rows)}"},
        {"check_id": "V613_6_certificate_template_blocks_claim", "result": "pass" if certificate_rows[-1]["current_status"] == "blocked" else "fail", "detail": f"certificate_rows={len(certificate_rows)}"},
        {"check_id": "V613_7_no_claim_rows", "result": "pass" if no_claim_rows else "fail", "detail": f"all_valid_for_claim_false={no_claim_rows}"},
        {"check_id": "V613_8_next_target_set", "result": "pass" if decision_rows[0]["next_target"] == NEXT_TARGET else "fail", "detail": NEXT_TARGET},
        {"check_id": "V613_9_no_R10_or_local_GR_claim", "result": "pass", "detail": "R10_pass=false;WEP=false;PPN=false;local_GR=false"},
    ]


def write_doc(
    generated: str,
    source_register: list[dict[str, object]],
    theorem_rows: list[dict[str, object]],
    signature_rows: list[dict[str, object]],
    countermodel_rows: list[dict[str, object]],
    lock_rows: list[dict[str, object]],
    certificate_rows: list[dict[str, object]],
    decision_rows: list[dict[str, object]],
    route_rows: list[dict[str, object]],
    summary_rows: list[dict[str, object]],
    validation_rows: list[dict[str, object]],
) -> None:
    content = f"""# 613 Y5 R10 parent matter-selector theorem or finite C_X envelope lock

Generated: {generated}  
Status: `{STATUS}`  
Claim ceiling: `{CLAIM_CEILING}`  
Next target: `{NEXT_TARGET}`

## Verdict
- The clean selector theorem is mathematically valid but still conditional: if `X` is invisible to observed geometry and ordinary constants before variation, then `qbar_XT=0`.
- The parent action has not signed the needed selector, constant-triviality, and no-marker clauses.
- Therefore `qbar_XT=0` is not promoted, and the finite `C_X` envelope is locked as the active honest branch.
- The practical finite-branch ceiling remains `|C_X| <= {summary_rows[0]['tightest_full_curve_abs_CX_ceiling']}` to clear the whole private review-candidate R10 curve.

## Source Register
{md_table(source_register)}

## Selector Theorem Attempt
{md_table(theorem_rows)}

## Parent Signature Audit
{md_table(signature_rows)}

## Countermodel Stress Test
{md_table(countermodel_rows)}

## Finite C_X Envelope Lock
{md_table(lock_rows)}

## Selector Certificate Template
{md_table(certificate_rows)}

## Decision
{md_table(decision_rows)}

## Route Update
{md_table(route_rows)}

## Nonclaim Summary
{md_table(summary_rows)}

## Validation
{md_table(validation_rows)}

## Practical Read
This is the right kind of setback: not "MTS fails", but "this route cannot be promoted by elegance alone." The selector theorem would be gorgeous if the parent action proves it, because it would zero ordinary test charge before any R10 comparison. But without the primitive-minimal quotient/no-marker theorem, common-mode matter coupling remains legal. So we lock the finite branch and move to the range problem: derive `lambda_X=sqrt(Z_X/M_X^2)` and see whether the branch lands in forgiving tens-of-microns territory or in the millimetre trough where `C_X` must be genuinely small.
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    generated = utc_now()
    source_register = build_source_register()
    prior_validation = read_csv(OUT / "P8_Y5_BRR545_612_VALIDATION.csv")
    summary_612 = read_csv(OUT / "P8_Y5_R10_612_NONCLAIM_SUMMARY.csv")[0]
    survival_rows = read_csv(OUT / "P8_Y5_R10_612_CX_SURVIVAL_WINDOWS.csv")

    theorem_rows = build_selector_theorem_rows()
    signature_rows = build_parent_signature_rows()
    countermodel_rows = build_countermodel_rows()
    lock_rows = build_finite_lock_rows(summary_612, survival_rows)
    certificate_rows = build_selector_certificate_rows()
    decision_rows = build_decision_rows()
    route_rows = build_route_rows()
    summary_rows = build_summary_rows(summary_612)
    validation_rows = build_validation_rows(
        source_register,
        prior_validation,
        theorem_rows,
        signature_rows,
        countermodel_rows,
        lock_rows,
        certificate_rows,
        decision_rows,
        summary_rows,
    )

    write_csv(OUT / "P8_Y5_R10_613_SOURCE_REGISTER.csv", source_register)
    write_csv(OUT / "P8_Y5_R10_613_SELECTOR_THEOREM_ATTEMPT.csv", theorem_rows)
    write_csv(OUT / "P8_Y5_R10_613_PARENT_SIGNATURE_AUDIT.csv", signature_rows)
    write_csv(OUT / "P8_Y5_R10_613_COUNTERMODEL_STRESS_TEST.csv", countermodel_rows)
    write_csv(OUT / "P8_Y5_R10_613_FINITE_CX_ENVELOPE_LOCK.csv", lock_rows)
    write_csv(OUT / "P8_Y5_R10_613_SELECTOR_CERTIFICATE_TEMPLATE.csv", certificate_rows)
    write_csv(OUT / "P8_Y5_BRR545_613_DECISION.csv", decision_rows)
    write_csv(OUT / "P8_Y5_BRR545_613_ROUTE_UPDATE.csv", route_rows)
    write_csv(OUT / "P8_Y5_R10_613_NONCLAIM_SUMMARY.csv", summary_rows)
    write_csv(OUT / "P8_Y5_BRR545_613_VALIDATION.csv", validation_rows)

    write_doc(
        generated,
        source_register,
        theorem_rows,
        signature_rows,
        countermodel_rows,
        lock_rows,
        certificate_rows,
        decision_rows,
        route_rows,
        summary_rows,
        validation_rows,
    )

    payload = {
        "generated": generated,
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "next_target": NEXT_TARGET,
        "doc": rel(DOC),
        "validation": rel(OUT / "P8_Y5_BRR545_613_VALIDATION.csv"),
        "all_validation_pass": all(row["result"] == "pass" for row in validation_rows),
    }
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
