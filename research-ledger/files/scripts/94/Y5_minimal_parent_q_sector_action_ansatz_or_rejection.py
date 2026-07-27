from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1553-Y5-minimal-parent-q-sector-action-ansatz-or-rejection.md"
START_TS = datetime.now(timezone.utc).timestamp()

SOURCE_FILES = {
    "1552_doc": ROOT / "1552-Y5-parent-q-sector-action-norm-extraction-template.md",
    "1552_validation": OUT / "P8_Y5_BRR545_1552_VALIDATION.csv",
    "1552_next": OUT / "P8_Y5_PARENT_QLOC_1552_NEXT_TARGET.csv",
    "1552_template": OUT / "P8_Y5_PARENT_QLOC_1552_PARENT_QSECTOR_ACTION_TEMPLATE.csv",
    "1552_algorithm": OUT / "P8_Y5_PARENT_QLOC_1552_QNORM_EXTRACTION_ALGORITHM.csv",
    "1552_filters": OUT / "P8_Y5_PARENT_QLOC_1552_ACTION_FAILURE_FILTERS.csv",
    "1551_hunt": OUT / "P8_Y5_PARENT_QLOC_1551_PARENT_QNORM_SOURCE_HUNT.csv",
    "1550_qnorm": OUT / "P8_Y5_PARENT_QLOC_1550_QNORM_CANDIDATE_AUDIT.csv",
    "1550_dual": OUT / "P8_Y5_PARENT_QLOC_1550_DUAL_PAIRING_CONTRACT.csv",
    "1549_variational": OUT / "P8_Y5_PARENT_QLOC_1549_VARIATIONAL_SOURCE_CURRENT_LAW.csv",
    "1548_symbolic": OUT / "P8_Y5_PARENT_QLOC_1548_SHARED_SYMBOLIC_PROFILE_CANDIDATES.csv",
    "1547_support": OUT / "P8_Y5_PARENT_QLOC_1547_SUPPORT_DOMAIN_CONVENTIONS.csv",
    "1023_doc": ROOT / "1023-Y5-R10-q-vX-action-descent-certificate-or-scalar-nohair-demotion.md",
    "1022_doc": ROOT / "1022-Y5-R10-vertical-quotient-LX-construction-or-scalar-nohair-branch-choice.md",
    "07_doc": ROOT / "07-nonpropagating-reciprocity-constraint.md",
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1553_SOURCE_REGISTER.csv"
ANSATZ_AUDIT = OUT / "P8_Y5_PARENT_QLOC_1553_MINIMAL_QSECTOR_ANSATZ_AUDIT.csv"
FILTER_RUNNER = OUT / "P8_Y5_PARENT_QLOC_1553_ANSATZ_FILTER_RUNNER_NONCLAIM.csv"
NORM_EXTRACTION_SMOKE = OUT / "P8_Y5_PARENT_QLOC_1553_QNORM_EXTRACTION_SMOKE_NONCLAIM.csv"
REJECTION_LEDGER = OUT / "P8_Y5_PARENT_QLOC_1553_ANSATZ_REJECTION_LEDGER.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1553_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1553_DECISION.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1553_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1553_VALIDATION.csv"

QUARANTINE = MICROSCOPE / "quarantine" / "1553"
QUAR_ANSATZ = QUARANTINE / "MINIMAL_QSECTOR_ANSATZ_AUDIT_NONCLAIM.csv"
QUAR_FILTER = QUARANTINE / "ANSATZ_FILTER_RUNNER_NONCLAIM.csv"
QUAR_SMOKE = QUARANTINE / "QNORM_EXTRACTION_SMOKE_NONCLAIM.csv"
QUAR_REJECT = QUARANTINE / "ANSATZ_REJECTION_LEDGER_NONCLAIM.csv"
QUAR_DECISION = QUARANTINE / "DECISION_NONCLAIM.csv"
BRANCH_ANSATZ = BRANCH_RESIDUALS / "minimal_qsector_ansatz_audit_nonclaim_1553.csv"
BRANCH_FILTER = BRANCH_RESIDUALS / "ansatz_filter_runner_nonclaim_1553.csv"
BRANCH_SMOKE = BRANCH_RESIDUALS / "qnorm_extraction_smoke_nonclaim_1553.csv"
BRANCH_REJECT = BRANCH_RESIDUALS / "ansatz_rejection_ledger_nonclaim_1553.csv"
BRANCH_DECISION = BRANCH_RESIDUALS / "qsector_decision_nonclaim_1553.csv"


def flags() -> dict[str, bool]:
    return {
        "numeric_value_present": False,
        "source_backed": False,
        "score_ready": False,
        "valid_prediction_row": False,
        "valid_for_claim": False,
        "claim_allowed": False,
    }


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def source_list(*keys: str) -> str:
    return "; ".join(rel(SOURCE_FILES[key]) for key in keys)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def parse_csv(path: Path) -> bool:
    read_csv(path)
    return True


def generated_flags_false(paths: list[Path]) -> bool:
    false_values = {"", "false", "0", "no", "none", "null"}
    claim_keys = [
        "numeric_value_present",
        "source_backed",
        "score_ready",
        "valid_prediction_row",
        "valid_for_claim",
        "claim_allowed",
        "accepted_for_scoring",
        "passes_for_claim",
    ]
    for path in paths:
        for row in read_csv(path):
            for key in claim_keys:
                if key in row and str(row[key]).strip().lower() not in false_values:
                    return False
    return True


def source_register_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "source_id": f"SRC1553_{index}_{key}",
            "source_path": rel(path),
            "exists": path.exists(),
            "purpose": "input evidence for minimal parent q-sector action ansatz audit",
            **flags(),
        }
        for index, (key, path) in enumerate(SOURCE_FILES.items())
    ]


def ansatz_audit_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "ansatz_id": "ANS1553_0_auxiliary_algebraic_positive_norm",
            "candidate": "nonpropagating auxiliary q-sector",
            "formula": "S_q=1/2 int_W mu_q^2 (q^A-Q^A(Phi)) G_AB (q^B-Q^B(Phi)) dV_e",
            "what_it_solves": "can define a positive local q-norm without gradient/exterior hair if G_AB>0",
            "fatal_or_open_issue": "Q^A(Phi), G_AB, mu_q, and matter q-coupling are not parent-derived",
            "filter_result": "BEST_FORMAL_CANDIDATE_NOT_ACCEPTED",
            "current_status": "FORMAL_ANSATZ_NOT_PARENT_SOURCED",
            "source_paths": source_list("1552_template", "1552_filters", "1551_hunt"),
        },
        {
            "ansatz_id": "ANS1553_1_massive_kinetic_q",
            "candidate": "massive derivative q-sector",
            "formula": "S_q=1/2 int_W (Z_AB nabla q^A nabla q^B + M_AB^2 q^A q^B) dV_e",
            "what_it_solves": "can provide Hessian/operator norm if Z/M are positive and sourced",
            "fatal_or_open_issue": "creates physical finite-range/exterior hair unless no-hair/source-zero/boundary locks close",
            "filter_result": "REJECT_FOR_MINIMAL_LOCAL_GR_ROUTE",
            "current_status": "REJECTED_HAIR_RISK_AND_PARENT_INPUTS_MISSING",
            "source_paths": source_list("1022_doc", "1023_doc", "1552_filters"),
        },
        {
            "ansatz_id": "ANS1553_2_pure_constraint_q",
            "candidate": "pure Lagrange multiplier constraint",
            "formula": "S_q=int_W lambda_A(q^A-Q^A(Phi)) dV_e",
            "what_it_solves": "removes independent q propagation and exterior hair",
            "fatal_or_open_issue": "degenerate: supplies constraint but no positive q-norm E for T_source_norm*C_qm",
            "filter_result": "REJECT_AS_NORM_SOURCE",
            "current_status": "DEGENERATE_NO_QNORM",
            "source_paths": source_list("1552_template", "1550_dual", "07_doc"),
        },
        {
            "ansatz_id": "ANS1553_3_penalty_constraint_limit",
            "candidate": "regularized penalty constraint",
            "formula": "S_q=int_W lambda_A(q^A-Q^A)+1/2 epsilon lambda_A H^AB lambda_B dV_e",
            "what_it_solves": "can interpolate between pure constraint and positive norm",
            "fatal_or_open_issue": "epsilon/H choice is inserted unless phase-volume or parent regulator theorem derives it",
            "filter_result": "CONDITIONAL_REGULATOR_ROUTE_ONLY",
            "current_status": "NOT_ACCEPTED_WITHOUT_PARENT_REGULATOR",
            "source_paths": source_list("1552_template", "1548_symbolic", "1547_support"),
        },
        {
            "ansatz_id": "ANS1553_4_reduced_quotient_norm",
            "candidate": "quotient-reduced parent norm",
            "formula": "E_q = pullback/restriction of delta^2 S_red on Conf_parent/N_q",
            "what_it_solves": "cleanest if q is a true quotient coordinate and reduced Hessian is positive",
            "fatal_or_open_issue": "q/v_X/action/matter/boundary/degree certificate failed for current MTS",
            "filter_result": "FUTURE_THEOREM_ROUTE_ONLY",
            "current_status": "CONDITIONAL_NOT_CURRENTLY_AVAILABLE",
            "source_paths": source_list("1022_doc", "1023_doc", "1551_hunt"),
        },
        {
            "ansatz_id": "ANS1553_5_phase_volume_nonpropagating_origin",
            "candidate": "phase-volume/nonpropagating q-origin",
            "formula": "q-sector arises as a local capacity/phase-volume balance constraint, not an exterior kinetic field",
            "what_it_solves": "aligns with the earlier nonpropagating reciprocity route and avoids hair",
            "fatal_or_open_issue": "phase-volume principle is not yet a parent theorem and does not yet supply G_AB/E",
            "filter_result": "PROMISING_NEXT_DERIVATION_ROUTE",
            "current_status": "ORIGIN_ROUTE_MISSING_THEOREM",
            "source_paths": source_list("07_doc", "1552_template", "1551_hunt"),
        },
        {
            "ansatz_id": "ANS1553_6_current_verdict",
            "candidate": "accepted minimal parent q-sector action",
            "formula": "none accepted",
            "what_it_solves": "none yet",
            "fatal_or_open_issue": "every minimal ansatz either lacks parent source, lacks a norm, risks exterior hair, or depends on an unproved origin principle",
            "filter_result": "REJECT_PROMOTION_KEEP_BEST_CANDIDATE_PRIVATE",
            "current_status": "NO_ACCEPTED_PARENT_ACTION",
            "source_paths": source_list("1552_template", "1552_filters", "1551_hunt"),
        },
    ]
    return [{**{"same_parent_branch_id": BRANCH_ID}, **row, **flags()} for row in rows]


def filter_runner_rows() -> list[dict[str, Any]]:
    rows = [
        ("FR1553_0_auxiliary", "ANS1553_0_auxiliary_algebraic_positive_norm", "passes no-hair shape but fails parent-source and matter-coupling provenance", "FAIL_NOT_PARENT_SOURCED"),
        ("FR1553_1_kinetic", "ANS1553_1_massive_kinetic_q", "positive norm possible but exterior hair/source-zero/boundary locks missing", "FAIL_HAIR_RISK"),
        ("FR1553_2_constraint", "ANS1553_2_pure_constraint_q", "no exterior hair but no positive norm for dual pairing", "FAIL_DEGENERATE_NORM"),
        ("FR1553_3_penalty", "ANS1553_3_penalty_constraint_limit", "regularized norm possible but regulator parameter is not derived", "FAIL_INSERTED_REGULATOR"),
        ("FR1553_4_quotient", "ANS1553_4_reduced_quotient_norm", "best theorem language but current quotient certificate failed", "FAIL_CONDITIONAL_CERTIFICATE"),
        ("FR1553_5_phase_volume", "ANS1553_5_phase_volume_nonpropagating_origin", "best conceptual origin route but no parent theorem or norm extraction", "FAIL_MISSING_ORIGIN_THEOREM"),
        ("FR1553_6_verdict", "ANS1553_6_current_verdict", "no ansatz may be promoted to theory or local claim", "PASS_GUARD_NONCLAIM"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": runner_id,
            "ansatz_id": ansatz_id,
            "filter_summary": filter_summary,
            "current_status": current_status,
            "accepted_for_scoring": False,
            "passes_for_claim": False,
            "source_paths": source_list("1552_filters", "1552_algorithm", "1551_reentry") if "1551_reentry" in SOURCE_FILES else source_list("1552_filters", "1552_algorithm", "1551_hunt"),
            **flags(),
        }
        for runner_id, ansatz_id, filter_summary, current_status in rows
    ]


def norm_extraction_smoke_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "SMOKE1553_0_auxiliary_E",
            "auxiliary ansatz",
            "E_aux[delta q]^2=int_W mu_q^2 delta q^A G_AB delta q^B dV_e",
            "FORMALLY_EXTRACTABLE_IF_GAB_SOURCED",
            "G_AB, mu_q, q map, and matter coupling are missing",
        ),
        (
            "SMOKE1553_1_auxiliary_Jq",
            "auxiliary ansatz source",
            "J_A=delta S_matter/delta q^A",
            "NOT_EXTRACTABLE_CURRENTLY",
            "no explicit S_matter[q]",
        ),
        (
            "SMOKE1553_2_auxiliary_Cqm",
            "auxiliary ansatz C_qm",
            "C_qm^2=int_W mu_q^2 Dq[v_m]^A G_AB Dq[v_m]^B dV_e",
            "NOT_EXTRACTABLE_CURRENTLY",
            "Dq[v_m] and G_AB are not parent-signed",
        ),
        (
            "SMOKE1553_3_constraint_E",
            "pure constraint ansatz",
            "no positive E from lambda(q-Q) alone",
            "REJECTED_DEGENERATE",
            "dual pairing requires a norm, not just a constraint equation",
        ),
        (
            "SMOKE1553_4_kinetic_E",
            "massive kinetic ansatz",
            "E_kin from Z_AB and M_AB^2",
            "REJECTED_FOR_CURRENT_ROUTE",
            "would need no-hair/source-zero/boundary theorem before local GR route",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "smoke_id": smoke_id,
            "route": route,
            "extraction_formula": extraction_formula,
            "current_status": current_status,
            "blocker": blocker,
            "source_paths": source_list("1550_dual", "1552_template", "1549_variational"),
            **flags(),
        }
        for smoke_id, route, extraction_formula, current_status, blocker in rows
    ]


def rejection_ledger_rows() -> list[dict[str, Any]]:
    rows = [
        ("REJ1553_0_no_promotion", "no ansatz promoted", "ansatz is not a parent derivation", "claim ceiling stays locked"),
        ("REJ1553_1_best_candidate", "auxiliary algebraic norm retained privately", "least hair-prone formal candidate but unsourced", "may guide future q-sector derivation"),
        ("REJ1553_2_best_origin", "phase-volume/nonpropagating origin retained", "best conceptual way to avoid inserted penalty terms", "next derivation target"),
        ("REJ1553_3_kinetic_route", "massive kinetic q rejected for current local route", "creates finite-range/hair branch without no-hair theorem", "only fallback empirical branch"),
        ("REJ1553_4_constraint_route", "pure constraint rejected as norm source", "does not supply E for T_source_norm*C_qm", "can still be part of origin story"),
        ("REJ1553_5_local_claim", "GR/Newton derivation still blocked", "no accepted q-sector action", "no local claim"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "rejection_id": rejection_id,
            "decision": decision,
            "reason": reason,
            "surviving_use": surviving_use,
            "source_paths": source_list("1552_filters", "1551_hunt", "07_doc"),
            **flags(),
        }
        for rejection_id, decision, reason, surviving_use in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("GATE1553_0_ansatz_audit", "minimal q-sector ansatz audit", "PASS_NONCLAIM", "candidate routes tested against failure filters"),
        ("GATE1553_1_best_candidate", "auxiliary algebraic candidate", "PASS_PRIVATE_CANDIDATE_ONLY", "formal route retained but not parent-sourced"),
        ("GATE1553_2_parent_action", "accepted parent q-sector action", "BLOCKED", "no ansatz passes as a parent derivation"),
        ("GATE1553_3_qnorm", "accepted q-norm E", "BLOCKED", "no sourced G_AB/Hessian/regulator exists"),
        ("GATE1553_4_envelope", "S_cg envelope computable", "BLOCKED", "E, J_q, Dq[v_m], and residual terms missing"),
        ("GATE1553_5_local_tests", "R10/PPN/clock/orbital/local test pass", "BLOCKED_NO_CLAIM", "no arena score follows from ansatz"),
        ("GATE1553_6_GR_Newton", "derived GR/Newton local limit", "BLOCKED_NO_CLAIM", "no parent action accepted"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "claim": claim,
            "status": status,
            "reason": reason,
            **flags(),
        }
        for gate_id, claim, status, reason in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        ("DEC1553_0_result", "No minimal q-sector ansatz is accepted as a parent derivation.", "NO_ACCEPTED_ANSATZ", "each candidate fails a required filter or lacks parent source"),
        ("DEC1553_1_retained", "Retain the auxiliary algebraic norm as the best formal candidate.", "PRIVATE_CANDIDATE_ONLY", "it can avoid exterior hair but needs a parent origin for G_AB and coupling"),
        ("DEC1553_2_next", "Next target is phase-volume/nonpropagating q-sector origin.", "NEXT_1554_PHASE_VOLUME_ORIGIN", "this is the least-cheaty path to derive the auxiliary norm rather than inserting it"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": decision_id,
            "decision": decision,
            "result": result,
            "rationale": rationale,
            **flags(),
        }
        for decision_id, decision, result, rationale in rows
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "next_id": "NEXT1553_0_1554",
            "next_target": "1554-Y5-phase-volume-nonpropagating-qsector-origin-or-rejection.md",
            "script": "scripts/Y5_phase_volume_nonpropagating_qsector_origin_or_rejection.py",
            "objective": "attempt to derive the auxiliary/nonpropagating q-sector norm from a phase-volume or motion-capacity balance principle, or reject that origin route explicitly",
            "do_not": "do not insert penalty coefficients by hand; do not reintroduce exterior hair; do not claim GR/Newton reduction",
            **flags(),
        }
    ]


def copy_outputs() -> None:
    copies = [
        (ANSATZ_AUDIT, QUAR_ANSATZ),
        (FILTER_RUNNER, QUAR_FILTER),
        (NORM_EXTRACTION_SMOKE, QUAR_SMOKE),
        (REJECTION_LEDGER, QUAR_REJECT),
        (DECISION, QUAR_DECISION),
        (ANSATZ_AUDIT, BRANCH_ANSATZ),
        (FILTER_RUNNER, BRANCH_FILTER),
        (NORM_EXTRACTION_SMOKE, BRANCH_SMOKE),
        (REJECTION_LEDGER, BRANCH_REJECT),
        (DECISION, BRANCH_DECISION),
    ]
    for source, destination in copies:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def formalization_modified_count_since_start() -> int:
    if not FORMALIZATION.exists():
        return 0
    return sum(1 for path in FORMALIZATION.rglob("*") if path.is_file() and path.stat().st_mtime >= START_TS)


def validation_rows(generated_csvs: list[Path]) -> list[dict[str, Any]]:
    sources = read_csv(SOURCE_REGISTER)
    ansatz_rows = read_csv(ANSATZ_AUDIT)
    filter_rows = read_csv(FILTER_RUNNER)
    smoke_rows = read_csv(NORM_EXTRACTION_SMOKE)
    rejection_rows = read_csv(REJECTION_LEDGER)
    gate_rows = read_csv(CLAIM_GATE)
    decision_items = read_csv(DECISION)
    next_rows = read_csv(NEXT_TARGET)

    checks = [
        ("VAL1553_0_sources_exist", all(row["exists"] == "True" for row in sources), "all cited 1553 source paths exist"),
        ("VAL1553_1_ansatz_candidates", len(ansatz_rows) >= 7 and any(row["ansatz_id"] == "ANS1553_0_auxiliary_algebraic_positive_norm" for row in ansatz_rows), "minimal ansatz candidates audited"),
        ("VAL1553_2_no_accepted_action", any(row["ansatz_id"] == "ANS1553_6_current_verdict" and row["current_status"] == "NO_ACCEPTED_PARENT_ACTION" for row in ansatz_rows), "no parent q-sector action accepted"),
        ("VAL1553_3_filters", any(row["runner_id"] == "FR1553_6_verdict" and row["current_status"] == "PASS_GUARD_NONCLAIM" for row in filter_rows), "ansatz filter runner keeps no-claim guard"),
        ("VAL1553_4_smoke_refuses", any(row["smoke_id"] == "SMOKE1553_0_auxiliary_E" and row["current_status"] == "FORMALLY_EXTRACTABLE_IF_GAB_SOURCED" for row in smoke_rows), "norm extraction smoke remains conditional"),
        ("VAL1553_5_rejection_ledger", any(row["rejection_id"] == "REJ1553_0_no_promotion" for row in rejection_rows), "ansatz rejection ledger written"),
        ("VAL1553_6_claim_gates_block", any(row["gate_id"] == "GATE1553_6_GR_Newton" and row["status"] == "BLOCKED_NO_CLAIM" for row in gate_rows), "GR/Newton claim remains blocked"),
        ("VAL1553_7_decision_next", any(row["result"] == "NEXT_1554_PHASE_VOLUME_ORIGIN" for row in decision_items), "decision selects phase-volume/nonpropagating origin next"),
        ("VAL1553_8_next_target", any("1554-Y5-phase-volume" in row["next_target"] for row in next_rows), "next target is phase-volume nonpropagating q-sector origin or rejection"),
        ("VAL1553_9_csv_parse", all(parse_csv(path) for path in generated_csvs), "all generated 1553 CSVs parse cleanly"),
        ("VAL1553_10_claim_flags_false", generated_flags_false(generated_csvs), "all generated prediction/claim flags remain false"),
        ("VAL1553_11_branch_copies", all(path.exists() for path in [QUAR_ANSATZ, QUAR_FILTER, QUAR_SMOKE, QUAR_REJECT, QUAR_DECISION, BRANCH_ANSATZ, BRANCH_FILTER, BRANCH_SMOKE, BRANCH_REJECT, BRANCH_DECISION]), "branch/quarantine nonclaim copies written"),
        ("VAL1553_12_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent after run"),
        ("VAL1553_13_formalization_untouched", formalization_modified_count_since_start() == 0, "formalization modified-file count since start=0"),
    ]
    overall = all(result for _, result, _ in checks)
    rows = [
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail,
        }
        for check_id, result, detail in checks
    ]
    rows.append(
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": "VAL1553_14_overall",
            "result": "PASS" if overall else "FAIL",
            "detail": "1553 audits minimal parent q-sector action ansatzes, rejects promotion, retains the auxiliary algebraic candidate privately, and selects phase-volume origin next"
            if overall
            else "1553 validation failed; inspect failed rows before continuing",
        }
    )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    output = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    for row in rows:
        output.append(
            "| "
            + " | ".join(str(row.get(column, "")).replace("\n", " ").replace("|", "\\|") for column in columns)
            + " |"
        )
    return "\n".join(output)


def write_doc(
    sources: list[dict[str, Any]],
    ansatz_rows: list[dict[str, Any]],
    filter_rows: list[dict[str, Any]],
    smoke_rows: list[dict[str, Any]],
    rejection_rows: list[dict[str, Any]],
    gate_rows: list[dict[str, Any]],
    decision_items: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 1553 - Minimal Parent q-sector Action Ansatz or Rejection",
                "",
                "## Verdict",
                "- No minimal q-sector action ansatz is accepted as a parent derivation.",
                "- The best formal candidate is a nonpropagating auxiliary algebraic norm because it can supply a positive local norm without exterior hair, but it is not parent-sourced.",
                "- The massive kinetic route is rejected for the current local-GR path because it reopens finite-range/hair pressure unless a no-hair theorem closes.",
                "- The pure constraint route avoids hair but is degenerate and does not supply the `q` norm needed by `T_source_norm*C_qm`.",
                "- The best next route is to derive the auxiliary/nonpropagating q-sector from a phase-volume or motion-capacity balance principle, not to insert a penalty by hand.",
                "",
                "## Source Register",
                md_table(sources, ["source_id", "source_path", "exists", "purpose"]),
                "",
                "## Minimal q-sector Ansatz Audit",
                md_table(ansatz_rows, ["ansatz_id", "candidate", "formula", "filter_result", "current_status", "fatal_or_open_issue"]),
                "",
                "## Ansatz Filter Runner",
                md_table(filter_rows, ["runner_id", "ansatz_id", "filter_summary", "current_status"]),
                "",
                "## q-norm Extraction Smoke",
                md_table(smoke_rows, ["smoke_id", "route", "extraction_formula", "current_status", "blocker"]),
                "",
                "## Rejection Ledger",
                md_table(rejection_rows, ["rejection_id", "decision", "reason", "surviving_use"]),
                "",
                "## Claim Gates",
                md_table(gate_rows, ["gate_id", "claim", "status", "reason"]),
                "",
                "## Decision",
                md_table(decision_items, ["decision_id", "decision", "result", "rationale"]),
                "",
                "## Validation",
                md_table(validation, ["check_id", "result", "detail"]),
                "",
                "## Next Target",
                md_table(next_rows, ["next_id", "next_target", "script", "objective", "do_not"]),
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> None:
    sources = source_register_rows()
    ansatz_rows = ansatz_audit_rows()
    filter_rows = filter_runner_rows()
    smoke_rows = norm_extraction_smoke_rows()
    rejection_rows = rejection_ledger_rows()
    gate_rows = claim_gate_rows()
    decision_items = decision_rows()
    next_rows = next_target_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(ANSATZ_AUDIT, ansatz_rows)
    write_csv(FILTER_RUNNER, filter_rows)
    write_csv(NORM_EXTRACTION_SMOKE, smoke_rows)
    write_csv(REJECTION_LEDGER, rejection_rows)
    write_csv(CLAIM_GATE, gate_rows)
    write_csv(DECISION, decision_items)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()
    remove_pycache()

    generated_csvs = [
        SOURCE_REGISTER,
        ANSATZ_AUDIT,
        FILTER_RUNNER,
        NORM_EXTRACTION_SMOKE,
        REJECTION_LEDGER,
        CLAIM_GATE,
        DECISION,
        NEXT_TARGET,
    ]
    validation = validation_rows(generated_csvs)
    write_csv(VALIDATION, validation)
    write_doc(sources, ansatz_rows, filter_rows, smoke_rows, rejection_rows, gate_rows, decision_items, validation, next_rows)


if __name__ == "__main__":
    main()
