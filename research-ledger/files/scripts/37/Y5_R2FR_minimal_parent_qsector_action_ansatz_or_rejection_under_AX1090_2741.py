from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_START_UTC = datetime.now(timezone.utc)

ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
SOURCE_WEIGHT = ROOT / "source-intake" / "source-weight"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "2741-Y5-R2FR-minimal-parent-qsector-action-ansatz-or-rejection-under-AX1090.md"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2741_SOURCE_REGISTER.csv",
    "ansatz": RESIDUALS / "P8_Y5_R2FR_2741_MINIMAL_QSECTOR_ANSATZ_AUDIT.csv",
    "filters": RESIDUALS / "P8_Y5_R2FR_2741_ANSATZ_FILTER_RUNNER.csv",
    "smoke": RESIDUALS / "P8_Y5_R2FR_2741_QNORM_EXTRACTION_SMOKE.csv",
    "rejection": RESIDUALS / "P8_Y5_R2FR_2741_REJECTION_LEDGER.csv",
    "decisions": RESIDUALS / "P8_Y5_R2FR_2741_DECISION_LEDGER.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_2741_CLAIM_GATES.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2741_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2741_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2741_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "ansatz": SOURCE_WEIGHT / "minimal_qsector_ansatz_audit_2741_NONCLAIM.csv",
    "smoke": LOCAL_BOUNDS / "minimal_qsector_qnorm_smoke_2741_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2741_PHASE_VOLUME_QSECTOR_ORIGIN_NEXT.csv",
}

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"


def ts() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dirs() -> None:
    for path in {p.parent for p in OUTPUTS.values()} | {p.parent for p in BRANCH_OUTPUTS.values()}:
        path.mkdir(parents=True, exist_ok=True)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing empty CSV: {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def md(value: Any) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def markdown_table(rows: list[dict[str, Any]], cols: list[str]) -> str:
    header = "| " + " | ".join(cols) + " |"
    sep = "| " + " | ".join("---" for _ in cols) + " |"
    body = ["| " + " | ".join(md(row.get(col, "")) for col in cols) + " |" for row in rows]
    return "\n".join([header, sep, *body])


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def local_path(path_text: str) -> Path:
    path = Path(path_text)
    if path.is_absolute():
        return path
    return ROOT / path


def nonclaim(row: dict[str, Any]) -> dict[str, Any]:
    row["score_ready"] = False
    row["valid_prediction_row"] = False
    row["valid_for_claim"] = False
    row["claim_allowed"] = False
    return row


def source_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "source_id": "SRC2741_0_2740_doc",
            "description": "2740 selects minimal parent q-sector ansatz/rejection.",
            "source_path": "2740-Y5-R2FR-parent-qsector-action-norm-extraction-contract-under-AX1090.md",
            "required_needles": "NEXT2740_0_2741;QS2740_1_positive_quadratic_form;FAIL2740_6_long_range_hair;VAL2740_OVERALL",
        },
        {
            "source_id": "SRC2741_1_1553_doc",
            "description": "1553 audits minimal q-sector ansatz candidates.",
            "source_path": "1553-Y5-minimal-parent-q-sector-action-ansatz-or-rejection.md",
            "required_needles": "ANS1553_0_auxiliary_algebraic_positive_norm;ANS1553_6_current_verdict;NEXT1553_0_1554",
        },
        {
            "source_id": "SRC2741_2_1554_doc",
            "description": "1554 phase-volume origin audit selected as next origin route.",
            "source_path": "1554-Y5-phase-volume-nonpropagating-qsector-origin-or-rejection.md",
            "required_needles": "ORG1554_0_radial_cell_rule;ORG1554_5_current_verdict;NEXT1554_0_1555",
        },
        {
            "source_id": "SRC2741_3_1553_ansatz_csv",
            "description": "machine-readable ansatz audit.",
            "source_path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1553_MINIMAL_QSECTOR_ANSATZ_AUDIT.csv",
            "required_needles": "ANS1553_0_auxiliary_algebraic_positive_norm;ANS1553_3_penalty_constraint_limit;ANS1553_6_current_verdict",
        },
        {
            "source_id": "SRC2741_4_1553_smoke_csv",
            "description": "machine-readable qnorm extraction smoke.",
            "source_path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1553_QNORM_EXTRACTION_SMOKE_NONCLAIM.csv",
            "required_needles": "SMOKE1553_0_auxiliary_E;SMOKE1553_2_auxiliary_Cqm;SMOKE1553_4_kinetic_E",
        },
        {
            "source_id": "SRC2741_5_2740_slots",
            "description": "live q-sector action slots from 2740.",
            "source_path": "source-intake/mts_residuals/P8_Y5_R2FR_2740_PARENT_QSECTOR_ACTION_SLOTS.csv",
            "required_needles": "QS2740_0_q_field;QS2740_4_matter_coupling;QS2740_8_verdict",
        },
        {
            "source_id": "SRC2741_6_2740_filters",
            "description": "live failure filters from 2740.",
            "source_path": "source-intake/mts_residuals/P8_Y5_R2FR_2740_ACTION_FAILURE_FILTERS.csv",
            "required_needles": "FAIL2740_0_arena_norm;FAIL2740_4_boundary_drop;FAIL2740_7_retuned_profile",
        },
        {
            "source_id": "SRC2741_7_2739_closure",
            "description": "2739 closure demotion status.",
            "source_path": "source-intake/mts_residuals/P8_Y5_R2FR_2739_LOCAL_CLOSURE_DEMOTION_GATE.csv",
            "required_needles": "DEM2739_0_scope;DEM2739_3_GR_Newton;DEM2739_4_reentry",
        },
        {
            "source_id": "SRC2741_8_1552_template",
            "description": "original q-sector action extraction template.",
            "source_path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1552_PARENT_QSECTOR_ACTION_TEMPLATE.csv",
            "required_needles": "ACT1552_0_q_field;ACT1552_4_matter_coupling;ACT1552_6_parent_action_verdict",
        },
    ]
    for row in rows:
        path = local_path(row["source_path"])
        text = path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""
        needles = [needle for needle in row["required_needles"].split(";") if needle]
        missing = [needle for needle in needles if needle not in text]
        row["exists"] = path.exists()
        row["needles_present"] = len(missing) == 0
        row["missing_needles"] = ";".join(missing)
        nonclaim(row)
    return rows


def ansatz_rows() -> list[dict[str, Any]]:
    specs = [
        ("ANS2741_0_auxiliary_algebraic_positive_norm", "nonpropagating auxiliary q-sector", "S_q=1/2 int_W mu_q^2 (q^A-Q^A(Phi)) G_AB (q^B-Q^B(Phi)) dV_e", "supplies positive local E_q without gradient/exterior hair if G_AB>0", "FORMAL_PRIVATE_CANDIDATE_NOT_ACCEPTED", "Q^A(Phi), G_AB, mu_q, J_q/matter q-coupling not parent-derived", "BEST_FORMAL_CANDIDATE"),
        ("ANS2741_1_massive_kinetic_q", "massive derivative q-sector", "S_q=1/2 int_W (Z_AB nabla q^A nabla q^B + M_AB^2 q^A q^B) dV_e", "can supply Hessian/operator norm if sourced", "REJECTED_FOR_MINIMAL_LOCAL_GR_ROUTE", "finite-range/exterior hair risk unless no-hair/source-zero/boundary locks close", "FAIL_LONG_RANGE_HAIR_FILTER"),
        ("ANS2741_2_pure_constraint_q", "pure Lagrange multiplier constraint", "S_q=int_W lambda_A(q^A-Q^A(Phi)) dV_e", "removes independent q propagation and avoids hair", "REJECTED_AS_NORM_SOURCE", "degenerate: no positive E_q for T_source_norm*C_qm", "FAIL_DEGENERATE_NORM"),
        ("ANS2741_3_penalty_constraint_limit", "regularized penalty constraint", "S_q=int_W lambda_A(q^A-Q^A)+1/2 epsilon lambda_A H^AB lambda_B dV_e", "can interpolate constraint and positive norm", "CONDITIONAL_REGULATOR_ROUTE_ONLY", "epsilon/H are inserted unless phase-volume/parent regulator derives them", "FAIL_INSERTED_REGULATOR"),
        ("ANS2741_4_reduced_quotient_norm", "quotient-reduced parent norm", "E_q=pullback/restriction of delta^2 S_red on Conf_parent/N_q", "clean if q is a true quotient coordinate and reduced Hessian positive", "CONDITIONAL_FUTURE_ROUTE_ONLY", "q/v_X/action/matter/boundary/degree certificate currently failed", "FAIL_CONDITIONAL_CERTIFICATE"),
        ("ANS2741_5_phase_volume_nonpropagating_origin", "phase-volume/nonpropagating q-origin", "q-sector arises from local capacity/phase-volume balance rather than exterior kinetic field", "best conceptual origin for auxiliary norm without hand penalty", "PROMISING_NEXT_DERIVATION_ROUTE", "origin theorem does not yet supply G_AB, mu_q, E_q, or J_q", "NEXT_ROUTE"),
        ("ANS2741_6_current_verdict", "accepted minimal parent q-sector action", "none accepted", "keeps local branch honest", "NO_ACCEPTED_PARENT_ACTION", "every candidate lacks parent source, lacks a norm, risks hair, or depends on unproved origin", "REJECT_PROMOTION"),
    ]
    return [
        nonclaim(
            {
                "same_parent_branch_id": BRANCH_ID,
                "ansatz_id": ansatz_id,
                "candidate": candidate,
                "formula": formula,
                "what_it_solves": solves,
                "current_status": status,
                "fatal_or_open_issue": issue,
                "filter_result": filter_result,
                "accepted_parent_action": False,
                "source_paths": "1553-Y5-minimal-parent-q-sector-action-ansatz-or-rejection.md; 2740-Y5-R2FR-parent-qsector-action-norm-extraction-contract-under-AX1090.md",
            }
        )
        for ansatz_id, candidate, formula, solves, status, issue, filter_result in specs
    ]


def filter_rows() -> list[dict[str, Any]]:
    rows = [
        ("FR2741_0_auxiliary", "ANS2741_0_auxiliary_algebraic_positive_norm", "passes no-exterior-gradient shape; fails parent source/provenance", "FAIL_NOT_PARENT_SOURCED"),
        ("FR2741_1_kinetic", "ANS2741_1_massive_kinetic_q", "positive norm possible; fails long-range hair/no-hair filter for current local route", "FAIL_HAIR_RISK"),
        ("FR2741_2_constraint", "ANS2741_2_pure_constraint_q", "avoids hair; fails because pure constraint has no positive dual norm", "FAIL_DEGENERATE_NORM"),
        ("FR2741_3_penalty", "ANS2741_3_penalty_constraint_limit", "positive regulator possible; fails because regulator coefficient is inserted", "FAIL_INSERTED_REGULATOR"),
        ("FR2741_4_quotient", "ANS2741_4_reduced_quotient_norm", "best theorem language; fails because quotient/action certificate is not closed", "FAIL_CONDITIONAL_CERTIFICATE"),
        ("FR2741_5_phase_volume", "ANS2741_5_phase_volume_nonpropagating_origin", "best origin route; fails current theorem/provenance, selected next", "FAIL_MISSING_ORIGIN_THEOREM"),
        ("FR2741_6_verdict", "ANS2741_6_current_verdict", "no candidate may be promoted or used for local claims", "PASS_GUARD_NONCLAIM"),
    ]
    return [
        nonclaim(
            {
                "same_parent_branch_id": BRANCH_ID,
                "runner_id": runner_id,
                "ansatz_id": ansatz_id,
                "filter_summary": summary,
                "current_status": status,
                "accepted_for_scoring": False,
                "passes_for_claim": False,
            }
        )
        for runner_id, ansatz_id, summary, status in rows
    ]


def smoke_rows() -> list[dict[str, Any]]:
    rows = [
        ("SMOKE2741_0_auxiliary_E", "auxiliary ansatz", "E_aux[delta q]^2=int_W mu_q^2 delta q^A G_AB delta q^B dV_e", "FORMALLY_EXTRACTABLE_IF_GAB_SOURCED", "G_AB, mu_q, q map, and matter coupling are missing"),
        ("SMOKE2741_1_auxiliary_Jq", "auxiliary ansatz source", "J_A=delta S_matter/delta q^A", "NOT_EXTRACTABLE_CURRENTLY", "no explicit S_matter[q]"),
        ("SMOKE2741_2_auxiliary_Cqm", "auxiliary ansatz C_qm", "C_qm^2=int_W mu_q^2 Dq[v_m]^A G_AB Dq[v_m]^B dV_e", "NOT_EXTRACTABLE_CURRENTLY", "Dq[v_m], G_AB, and mu_q are not parent-signed"),
        ("SMOKE2741_3_constraint_E", "pure constraint ansatz", "no positive E_q from lambda(q-Q) alone", "REJECTED_DEGENERATE", "dual pairing requires a norm, not just a constraint equation"),
        ("SMOKE2741_4_kinetic_E", "massive kinetic ansatz", "E_kin from Z_AB and M_AB^2", "REJECTED_FOR_CURRENT_ROUTE", "would need no-hair/source-zero/boundary theorem before local GR route"),
        ("SMOKE2741_5_phase_volume_E", "phase-volume origin", "E_q could be auxiliary algebraic if phase-volume derives mu_q^2 G_AB", "NEXT_THEOREM_ROUTE_ONLY", "origin theorem missing"),
    ]
    return [
        nonclaim(
            {
                "same_parent_branch_id": BRANCH_ID,
                "smoke_id": smoke_id,
                "route": route,
                "extraction_formula": formula,
                "current_status": status,
                "blocker": blocker,
                "source_paths": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1553_QNORM_EXTRACTION_SMOKE_NONCLAIM.csv; 2740-Y5-R2FR-parent-qsector-action-norm-extraction-contract-under-AX1090.md",
            }
        )
        for smoke_id, route, formula, status, blocker in rows
    ]


def rejection_rows() -> list[dict[str, Any]]:
    rows = [
        ("REJ2741_0_no_promotion", "no ansatz promoted", "ansatz is not a parent derivation", "claim ceiling stays locked"),
        ("REJ2741_1_best_candidate", "auxiliary algebraic norm retained privately", "least hair-prone formal candidate but unsourced", "may guide future q-sector derivation"),
        ("REJ2741_2_best_origin", "phase-volume/nonpropagating origin retained", "best conceptual way to avoid inserted penalty terms", "next derivation target"),
        ("REJ2741_3_kinetic_route", "massive kinetic q rejected for current local route", "creates finite-range/hair branch without no-hair theorem", "only fallback empirical branch"),
        ("REJ2741_4_constraint_route", "pure constraint rejected as norm source", "does not supply E_q for T_source_norm*C_qm", "can still be part of origin story"),
        ("REJ2741_5_local_claim", "GR/Newton derivation still blocked", "no accepted q-sector action", "no local claim"),
    ]
    return [nonclaim({"rejection_id": rid, "decision": decision, "reason": reason, "surviving_use": use}) for rid, decision, reason, use in rows]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        ("DEC2741_0_result", "No minimal q-sector ansatz is accepted as parent derivation.", "every candidate fails a required 2740 filter or lacks parent source", "local branch remains closure-only"),
        ("DEC2741_1_retained_candidate", "Retain auxiliary algebraic norm as private candidate.", "it supplies a positive local norm without exterior gradient hair if parent-sourced", "use as guide, not claim"),
        ("DEC2741_2_reject_kinetic", "Reject massive kinetic q for this local-GR route.", "it reopens exterior finite-range hair unless further no-hair gates close", "do not use as clean GR reduction route"),
        ("DEC2741_3_next", "Go after phase-volume/nonpropagating origin.", "it is the least-cheaty way to derive the auxiliary norm instead of inserting it", "2742 should test phase-volume/capacity origin or reject it"),
    ]
    return [nonclaim({"decision_id": did, "decision": decision, "because": because, "effect": effect}) for did, decision, because, effect in rows]


def gate_rows() -> list[dict[str, Any]]:
    gates = [
        ("GATE2741_0_ansatz_audit", "minimal q-sector ansatz audit", True, "PASS_NONCLAIM", "candidate routes tested against failure filters"),
        ("GATE2741_1_best_candidate", "auxiliary algebraic candidate", True, "PASS_PRIVATE_CANDIDATE_ONLY", "formal route retained but not parent-sourced"),
        ("GATE2741_2_parent_action", "accepted parent q-sector action", False, "BLOCKED", "no ansatz passes as parent derivation"),
        ("GATE2741_3_qnorm", "accepted q-norm E_q", False, "BLOCKED", "no sourced G_AB/Hessian/regulator exists"),
        ("GATE2741_4_envelope", "S_cg/N_pair computable", False, "BLOCKED", "E_q, J_q, Dq[v_m], and residual terms missing"),
        ("GATE2741_5_local_tests", "R10/PPN/clock/orbital pass", False, "BLOCKED_NO_CLAIM", "no arena score follows from ansatz"),
        ("GATE2741_6_GR_Newton", "derived GR/Newton local limit", False, "BLOCKED_NO_CLAIM", "no parent action accepted"),
    ]
    return [
        nonclaim(
            {
                "claim_gate_id": gid,
                "claim": claim,
                "gate_passed": passed,
                "status": status,
                "claim_allowed": False,
                "reason": reason,
            }
        )
        for gid, claim, passed, status, reason in gates
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        nonclaim(
            {
                "next_id": "NEXT2741_0_2742",
                "status": "selected_primary",
                "target_doc": "2742-Y5-R2FR-phase-volume-nonpropagating-qsector-origin-or-rejection-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_phase_volume_nonpropagating_qsector_origin_or_rejection_under_AX1090_2742.py",
                "mission": "attempt to derive the auxiliary/nonpropagating q-sector norm from a phase-volume or motion-capacity balance principle, or reject that origin route explicitly",
                "acceptance": "derive parent origin for q constraint and algebraic norm coefficients, or record exact obstruction/no-charge/matter-coupling gaps",
                "forbidden": "do not insert penalty coefficients by hand; do not reintroduce exterior hair; do not claim GR/Newton reduction",
                "selected": True,
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({"copy_id": "BR2741_0_ansatz", "source_table": rel(OUTPUTS["ansatz"]), "copy_path": rel(BRANCH_OUTPUTS["ansatz"]), "purpose": "source-weight minimal qsector ansatz audit", "exists": BRANCH_OUTPUTS["ansatz"].exists()}),
        nonclaim({"copy_id": "BR2741_1_smoke", "source_table": rel(OUTPUTS["smoke"]), "copy_path": rel(BRANCH_OUTPUTS["smoke"]), "purpose": "local-bound qnorm extraction smoke", "exists": BRANCH_OUTPUTS["smoke"].exists()}),
        nonclaim({"copy_id": "BR2741_2_next_queue", "source_table": rel(OUTPUTS["next"]), "copy_path": rel(BRANCH_OUTPUTS["next_queue"]), "purpose": "RAB acquisition queue for phase-volume qsector origin", "exists": BRANCH_OUTPUTS["next_queue"].exists()}),
    ]


def formalization_recent_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    start = SCRIPT_START_UTC.timestamp()
    return sum(1 for path in FORMALIZATION.rglob("*") if path.is_file() and path.stat().st_mtime >= start)


def validation_rows(
    sources: list[dict[str, Any]],
    ansatz: list[dict[str, Any]],
    filters: list[dict[str, Any]],
    smoke: list[dict[str, Any]],
    rejection: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    source_ok = all(row["exists"] is True and row["needles_present"] is True for row in sources)
    ansatz_ok = any(row["ansatz_id"] == "ANS2741_0_auxiliary_algebraic_positive_norm" for row in ansatz) and any(row["ansatz_id"] == "ANS2741_6_current_verdict" and row["current_status"] == "NO_ACCEPTED_PARENT_ACTION" for row in ansatz)
    filters_ok = any(row["current_status"] == "PASS_GUARD_NONCLAIM" for row in filters) and all(row["accepted_for_scoring"] is False for row in filters)
    smoke_ok = any(row["smoke_id"] == "SMOKE2741_0_auxiliary_E" for row in smoke) and any(row["current_status"] == "REJECTED_DEGENERATE" for row in smoke)
    rejection_ok = any(row["rejection_id"] == "REJ2741_0_no_promotion" for row in rejection)
    gates_ok = any(row["claim_gate_id"] == "GATE2741_1_best_candidate" and row["gate_passed"] is True for row in gates) and all(row["claim_allowed"] is False for row in gates)
    next_ok = next_target[0]["selected"] is True and "phase-volume" in next_target[0]["target_doc"]
    branch_ok = all(path.exists() for path in BRANCH_OUTPUTS.values())
    formalization_ok = formalization_recent_count() == 0
    csv_ok = True
    csv_bits: list[str] = []
    for key, path in {**OUTPUTS, **BRANCH_OUTPUTS}.items():
        if key == "validation":
            continue
        try:
            rows = read_csv(path)
            csv_bits.append(f"{path.name}:{len(rows)}:ok")
        except Exception as exc:
            csv_ok = False
            csv_bits.append(f"{path.name}:ERROR:{exc}")
    rows = [
        {"validation_id": "VAL2741_0_sources", "passed": source_ok, "detail": "all source paths exist and required anchors/needles are present", "timestamp_utc": ts()},
        {"validation_id": "VAL2741_1_ansatz_candidates", "passed": ansatz_ok, "detail": "minimal ansatz candidates audited and no action accepted", "timestamp_utc": ts()},
        {"validation_id": "VAL2741_2_filters", "passed": filters_ok, "detail": "filter runner keeps all candidates nonclaim/non-scoring", "timestamp_utc": ts()},
        {"validation_id": "VAL2741_3_smoke", "passed": smoke_ok, "detail": "qnorm extraction smoke retains auxiliary formula and rejects degenerate route", "timestamp_utc": ts()},
        {"validation_id": "VAL2741_4_rejection_ledger", "passed": rejection_ok, "detail": "no-promotion rejection ledger written", "timestamp_utc": ts()},
        {"validation_id": "VAL2741_5_claim_gates", "passed": gates_ok, "detail": "only private/nonclaim gates pass; local claims remain blocked", "timestamp_utc": ts()},
        {"validation_id": "VAL2741_6_next_target", "passed": next_ok, "detail": "next target is phase-volume/nonpropagating qsector origin", "timestamp_utc": ts()},
        {"validation_id": "VAL2741_7_branch_outputs", "passed": branch_ok, "detail": "branch copies exist", "timestamp_utc": ts()},
        {"validation_id": "VAL2741_8_csv_parse", "passed": csv_ok, "detail": "; ".join(csv_bits), "timestamp_utc": ts()},
        {"validation_id": "VAL2741_9_formalization_untouched", "passed": formalization_ok, "detail": f"formalization-workbench recent modified-file count since script start = {formalization_recent_count()}", "timestamp_utc": ts()},
    ]
    rows.append(
        {
            "validation_id": "VAL2741_OVERALL",
            "passed": all(row["passed"] is True for row in rows),
            "detail": "2741 audits minimal parent qsector ansatzes, rejects promotion, retains the auxiliary algebraic candidate privately, and selects phase-volume origin next",
            "timestamp_utc": ts(),
        }
    )
    return rows


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    DOC.write_text(
        f"""# 2741 - Y5 R2/f(R): Minimal Parent q-sector Action Ansatz Or Rejection Under AX1090

Status: `Y5_R2FR_2741_minimal_qsector_ansatz_rejected_auxiliary_candidate_retained_private`

## Private Verdict

2741 tries the leap and does not fake the landing.

No minimal q-sector action ansatz is accepted as a parent derivation. The best formal candidate is still the nonpropagating auxiliary algebraic norm:

`S_q=1/2 int_W mu_q^2 (q^A-Q^A(Phi)) G_AB (q^B-Q^B(Phi)) dV_e`.

Why it matters: it can supply a positive local `E_q` without exterior gradient hair. Why it is not accepted: `Q^A(Phi)`, `G_AB`, `mu_q`, and matter `q`-coupling are not parent-derived.

The massive kinetic route is rejected for the clean local-GR route because it reopens exterior finite-range/hair pressure. The pure constraint route avoids hair but gives no positive norm. The penalty route inserts a regulator unless a deeper origin supplies it.

So the next real derivation target is phase-volume / motion-capacity origin: can it derive the auxiliary norm instead of us inserting it?

## Source Register

{markdown_table(data["sources"], ["source_id", "description", "source_path", "exists", "needles_present", "missing_needles", "valid_for_claim"])}

## Minimal q-sector Ansatz Audit

{markdown_table(data["ansatz"], ["ansatz_id", "candidate", "formula", "what_it_solves", "current_status", "fatal_or_open_issue", "filter_result", "accepted_parent_action", "valid_for_claim"])}

## Ansatz Filter Runner

{markdown_table(data["filters"], ["runner_id", "ansatz_id", "filter_summary", "current_status", "accepted_for_scoring", "passes_for_claim", "valid_for_claim"])}

## qnorm Extraction Smoke

{markdown_table(data["smoke"], ["smoke_id", "route", "extraction_formula", "current_status", "blocker", "valid_for_claim"])}

## Rejection Ledger

{markdown_table(data["rejection"], ["rejection_id", "decision", "reason", "surviving_use", "valid_for_claim"])}

## Decision Ledger

{markdown_table(data["decisions"], ["decision_id", "decision", "because", "effect", "valid_for_claim"])}

## Claim Gates

{markdown_table(data["gates"], ["claim_gate_id", "claim", "gate_passed", "status", "claim_allowed", "valid_for_claim", "reason"])}

## Next Target

{markdown_table(data["next"], ["next_id", "status", "target_doc", "target_script", "mission", "acceptance", "forbidden", "selected", "valid_for_claim"])}

## Branch Copies

{markdown_table(data["branches"], ["copy_id", "source_table", "copy_path", "purpose", "exists", "valid_for_claim"])}

## Validation

{markdown_table(data["validation"], ["validation_id", "passed", "detail", "timestamp_utc"])}

## Plain-English Read

This is annoying but good. The clean-looking q-sector exists as a formal move, but it cannot be declared parent-derived yet. The best path is not to bolt it on; it is to try to derive that algebraic norm from the motion/phase-volume structure. That is the next serious shot.
""",
        encoding="utf-8",
    )


def main() -> None:
    ensure_dirs()
    sources = source_rows()
    ansatz = ansatz_rows()
    filters = filter_rows()
    smoke = smoke_rows()
    rejection = rejection_rows()
    decisions = decision_rows()
    gates = gate_rows()
    next_target = next_rows()

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["ansatz"], ansatz)
    write_csv(OUTPUTS["filters"], filters)
    write_csv(OUTPUTS["smoke"], smoke)
    write_csv(OUTPUTS["rejection"], rejection)
    write_csv(OUTPUTS["decisions"], decisions)
    write_csv(OUTPUTS["gates"], gates)
    write_csv(OUTPUTS["next"], next_target)

    write_csv(BRANCH_OUTPUTS["ansatz"], ansatz)
    write_csv(BRANCH_OUTPUTS["smoke"], smoke)
    write_csv(BRANCH_OUTPUTS["next_queue"], next_target)
    branches = branch_rows()
    write_csv(OUTPUTS["branches"], branches)

    validation = validation_rows(sources, ansatz, filters, smoke, rejection, gates, next_target)
    write_csv(OUTPUTS["validation"], validation)

    data = {
        "sources": sources,
        "ansatz": ansatz,
        "filters": filters,
        "smoke": smoke,
        "rejection": rejection,
        "decisions": decisions,
        "gates": gates,
        "next": next_target,
        "branches": branches,
        "validation": validation,
    }
    write_doc(data)

    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    if not all(row["passed"] is True for row in validation):
        failed = [row for row in validation if row["passed"] is not True]
        raise SystemExit(f"2741 validation failed: {failed}")
    print(f"wrote {DOC}")
    print(f"validation {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
