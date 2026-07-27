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

DOC = ROOT / "2750-Y5-R2FR-lambdaR-parent-origin-zero-stress-and-first-class-constraint-test-under-AX1090.md"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2750_SOURCE_REGISTER.csv",
    "origin": RESIDUALS / "P8_Y5_R2FR_2750_LAMBDAR_ORIGIN_AUDIT.csv",
    "stress": RESIDUALS / "P8_Y5_R2FR_2750_ZERO_STRESS_VARIATION_GATE.csv",
    "constraint": RESIDUALS / "P8_Y5_R2FR_2750_CONSTRAINT_CLASS_GATE.csv",
    "boundary": RESIDUALS / "P8_Y5_R2FR_2750_BOUNDARY_DEGREE_COUNT_GATE.csv",
    "routes": RESIDUALS / "P8_Y5_R2FR_2750_ROUTE_DECISION_LEDGER.csv",
    "runner": RESIDUALS / "P8_Y5_R2FR_2750_RUNNER_NONCLAIM.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_2750_CLAIM_GATES.csv",
    "decisions": RESIDUALS / "P8_Y5_R2FR_2750_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2750_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2750_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2750_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "routes": SOURCE_WEIGHT / "lambdaR_route_decision_2750_NONCLAIM.csv",
    "stress": LOCAL_BOUNDS / "lambdaR_zero_stress_gate_2750_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2750_RAB_AUXILIARY_COMPATIBILITY_GRAMMAR_NEXT.csv",
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
    row["numeric_value_present"] = False
    row["source_backed"] = False
    row["score_ready"] = False
    row["valid_prediction_row"] = False
    row["valid_for_claim"] = False
    row["claim_allowed"] = False
    return row


def source_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "source_id": "SRC2750_0_2749_doc",
            "description": "2749 selects lambda_R parent-origin and zero-stress test.",
            "source_path": "2749-Y5-R2FR-minimal-parent-weak-field-action-ansatz-and-Euler-Ward-PPN-gate-under-AX1090.md",
            "required_needles": "NEXT2749_0_2750;EUL2749_2_lambda_stress;VAL2749_OVERALL",
        },
        {
            "source_id": "SRC2750_1_2749_validation",
            "description": "2749 validation output.",
            "source_path": "source-intake/mts_residuals/P8_Y5_BRR545_2749_VALIDATION.csv",
            "required_needles": "VAL2749_OVERALL;True;lambda_R parent-origin zero-stress test",
        },
        {
            "source_id": "SRC2750_2_2749_ansatz",
            "description": "live minimal weak-field ansatz register.",
            "source_path": "source-intake/mts_residuals/P8_Y5_R2FR_2749_MINIMAL_ACTION_ANSATZ_REGISTER.csv",
            "required_needles": "ANS2749_A_EH_lambdaR_silent;BEST_CONDITIONAL_ANSATZ_NOT_ADOPTED",
        },
        {
            "source_id": "SRC2750_3_2749_euler",
            "description": "live Euler variation gate.",
            "source_path": "source-intake/mts_residuals/P8_Y5_R2FR_2749_EULER_VARIATION_GATE.csv",
            "required_needles": "EUL2749_1_lambda_variation;EUL2749_2_lambda_stress;FAIL_UNSIGNED_STRESS_SILENCE",
        },
        {
            "source_id": "SRC2750_4_1562_doc",
            "description": "prior lambda_R origin, stress, and constraint-class test.",
            "source_path": "1562-Y5-lambdaR-parent-origin-zero-stress-and-first-class-constraint-test.md",
            "required_needles": "STR1562_5_current;ROUTE1562_1_second_class_auxiliary;NEXT_1563_AUXILIARY_PARENT_SORT_NO_DERIVATIVE_GRAMMAR",
        },
        {
            "source_id": "SRC2750_5_1562_origin",
            "description": "machine-readable prior lambda_R origin audit.",
            "source_path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1562_LAMBDAR_ORIGIN_AUDIT.csv",
            "required_needles": "ORG1562_3_second_class_auxiliary;BEST_CONDITIONAL_ROUTE",
        },
        {
            "source_id": "SRC2750_6_1562_stress",
            "description": "machine-readable prior zero-stress variation gate.",
            "source_path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1562_ZERO_STRESS_VARIATION_GATE.csv",
            "required_needles": "STR1562_1_multiplier_metric_stress;FAIL_UNSIGNED;STR1562_5_current",
        },
        {
            "source_id": "SRC2750_7_1562_constraint",
            "description": "machine-readable prior constraint-class gate.",
            "source_path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1562_CONSTRAINT_CLASS_GATE.csv",
            "required_needles": "CLASS1562_2_preservation;CLASS1562_5_second_class",
        },
        {
            "source_id": "SRC2750_8_1248_doc",
            "description": "minimal lambdaR parent action ansatz and Dirac check.",
            "source_path": "1248-Y5-R10-minimal-lambdaR-parent-action-ansatz-and-Dirac-check.md",
            "required_needles": "lambdaR;Dirac",
        },
        {
            "source_id": "SRC2750_9_1268_doc",
            "description": "RAB second-class auxiliary compatibility action or finite source row.",
            "source_path": "1268-Y5-R10-RAB-second-class-auxiliary-compatibility-action-or-finite-ZR-source-row.md",
            "required_needles": "second-class;auxiliary",
        },
        {
            "source_id": "SRC2750_10_1555_doc",
            "description": "first-class/Noether zero-charge prior failure.",
            "source_path": "1555-Y5-gauge-noether-zero-charge-qsector-origin-audit.md",
            "required_needles": "GAUGE1555_4_first_class_constraint;RUN1555_3_current",
        },
        {
            "source_id": "SRC2750_11_2749_queue",
            "description": "live queue into this checkpoint.",
            "source_path": "source-intake/rab-sector/acquisition-queue/JR2749_LAMBDAR_ORIGIN_ZERO_STRESS_NEXT.csv",
            "required_needles": "NEXT2749_0_2750;lambda_R R_AB",
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


def origin_rows() -> list[dict[str, Any]]:
    specs = [
        ("ORG2750_0_delta_lambda", "bare multiplier insertion", "S_lambda=int sqrt(-g) lambda_R R_AB; delta lambda_R -> R_AB=0", "FORMAL_VARIATION_ONLY_NOT_DERIVATION", "variation works only after inserting lambda_R"),
        ("ORG2750_1_phase_volume", "phase-volume/cell-balance motivation", "local reciprocal volume balance suggests a nonpropagating constraint", "MOTIVATION_NOT_PARENT_ORIGIN", "does not provide parent variable sort, multiplier origin, or stress theorem"),
        ("ORG2750_2_first_class", "first-class constraint route", "C_R=R_AB with differentiable generator, zero/proper boundary charge, bracket closure, and degree count", "POSSIBLE_NOT_PRESENT", "preservation, bracket closure, degree count, and boundary generator are missing"),
        ("ORG2750_3_second_class_auxiliary", "second-class/algebraic auxiliary compatibility route", "S_R=int mu_parent Lambda_R [R_AB-C_AB(q,theta,top)] with no derivative grammar", "BEST_CONDITIONAL_ROUTE_UNSIGNED", "could eliminate R_AB/Lambda_R algebraically if parent sort/no-derivative/matter/boundary/readout gates pass"),
        ("ORG2750_4_kinetic_RAB", "kinetic reciprocal strain", "0.5 W (grad R_AB)^2 gives reciprocal hair Q_R/r", "REJECTED_QR_HAIR", "requires finite q_R/Z_R bounded branch unless Q_R=0 theorem exists"),
    ]
    return [nonclaim({"same_parent_branch_id": BRANCH_ID, "origin_id": oid, "route": route, "mechanism": mechanism, "status": status, "limitation": limitation}) for oid, route, mechanism, status, limitation in specs]


def stress_rows() -> list[dict[str, Any]]:
    specs = [
        ("STR2750_0_multiplier_E_lambda", "delta_{lambda_R} S", "R_AB=0", "PASS_FORMAL", "this is only the constraint equation, not parent legitimacy"),
        ("STR2750_1_multiplier_metric_stress", "delta_g(lambda_R R_AB)", "terms proportional to lambda_R delta_g R_AB can survive even when R_AB=0", "FAIL_UNSIGNED", "on-shell R_AB=0 alone does not prove lambda_R stress silence"),
        ("STR2750_2_aux_E_R", "delta_{R_AB} S_R", "Lambda_R + J_R + delta B_R/delta R_AB + readout_regen = 0", "PASS_ONLY_IF_SOURCES_ZERO", "Lambda_R=0 follows only with matter/boundary/readout source silence"),
        ("STR2750_3_no_derivative", "operator grammar", "no D R_AB, D Lambda_R, vertical metric, or boundary derivative operator", "REQUIRED_UNSIGNED", "derivative terms regenerate finite reciprocal hair"),
        ("STR2750_4_matter_boundary_readout", "source and boundary variations", "delta S_matter/delta R_AB=0 and delta B/delta R_AB=0 before readout", "REQUIRED_UNSIGNED", "otherwise E_R sources finite Lambda_R/stress"),
        ("STR2750_5_current", "zero-stress verdict", "no current proof that lambda_R is zero-stress in the accepted parent action", "FAIL_CURRENT_CLAIM", "best route is exact conditional auxiliary compatibility, not first-class promotion"),
    ]
    return [nonclaim({"same_parent_branch_id": BRANCH_ID, "stress_id": sid, "variation": variation, "result": result, "status": status, "reason": reason}) for sid, variation, result, status, reason in specs]


def constraint_rows() -> list[dict[str, Any]]:
    specs = [
        ("CLASS2750_0_first_primary", "first-class/Dirac primary", "pi_lambda approx 0", "FORMAL_PASS_WITHIN_ANSATZ", "only after lambda_R is inserted"),
        ("CLASS2750_1_first_secondary", "first-class/Dirac secondary", "C_R=R_AB approx 0", "FORMAL_PASS_WITHIN_ANSATZ", "desired closure appears as secondary constraint"),
        ("CLASS2750_2_preservation", "constraint preservation", "dot C_R={C_R,H_core}+... closes or fixes multiplier", "BLOCKED", "H_core and Poisson brackets for parent variables are absent"),
        ("CLASS2750_3_brackets_degree", "constraint class and degree count", "brackets close and remove reciprocal pair without hiding physical mode", "BLOCKED", "no algebra/degree-count certificate exists"),
        ("CLASS2750_4_boundary_generator", "differentiable generator", "G_R[epsilon]=int epsilon C_R + Q_R has zero/proper boundary charge", "BLOCKED", "boundary/corner charge audit missing"),
        ("CLASS2750_5_second_class", "second-class auxiliary elimination", "E_Lambda and E_R eliminate R_AB,Lambda_R algebraically before readout", "BETTER_CONDITIONAL_THAN_FIRST_CLASS", "still unsigned until parent sort/no-derivative/matter/boundary/readout gates pass"),
    ]
    return [nonclaim({"same_parent_branch_id": BRANCH_ID, "class_id": cid, "constraint_test": test, "required_statement": req, "status": status, "blocker": blocker}) for cid, test, req, status, blocker in specs]


def boundary_rows() -> list[dict[str, Any]]:
    specs = [
        ("BD2750_0_no_QR", "no reciprocal boundary charge", "R_AB/Lambda_R sector has no differentiable boundary charge after elimination", "UNSIGNED", "no boundary/corner variational class proves this"),
        ("BD2750_1_degree", "degree-count safety", "auxiliary pair removes no physical propagating local mode", "UNSIGNED", "parent sort and phase-space list are not sourced from primitives"),
        ("BD2750_2_matter", "matter descent", "matter action factors through public/quotient variables and not R_AB", "UNSIGNED", "without this E_R has J_R source"),
        ("BD2750_3_readout", "readout stability", "eliminating R_AB,Lambda_R does not regenerate finite q_R in effective/readout action", "UNSIGNED", "readout/EFT closure proof absent"),
        ("BD2750_4_operator", "no derivative operator", "D R_AB kinetic/gradient operators are illegal in the parent grammar", "UNSIGNED", "if allowed, finite q_R/Z_R source branch is required"),
    ]
    return [nonclaim({"same_parent_branch_id": BRANCH_ID, "boundary_id": bid, "gate": gate, "required_statement": req, "status": status, "blocker": blocker}) for bid, gate, req, status, blocker in specs]


def route_rows() -> list[dict[str, Any]]:
    specs = [
        ("ROUTE2750_0_first_class", "first-class lambda_R/R_AB constraint", "REJECT_CURRENT_PROMOTION", "primary/secondary steps are formal, but preservation, brackets, degree count, and boundary generator are missing", "do not spend next pass on first-class language unless parent H_core and symplectic form are supplied"),
        ("ROUTE2750_1_second_class_auxiliary", "second-class auxiliary compatibility", "BEST_DERIVATION_ROUTE_CONDITIONAL", "E_Lambda enforces compatibility and E_R can kill Lambda_R/stress if matter, boundary, readout, and derivative grammar gates pass", "attack parent sort and no-derivative grammar first"),
        ("ROUTE2750_2_finite_qR", "bounded finite q_R fallback", "FALLBACK_IF_AUXILIARY_GATES_FAIL", "2747 control runner can bound finite q_R/delta_beta without claiming derivation", "keep as nonclaim fallback"),
    ]
    return [nonclaim({"same_parent_branch_id": BRANCH_ID, "route_id": rid, "route": route, "verdict": verdict, "reason": reason, "next_action": action}) for rid, route, verdict, reason, action in specs]


def runner_rows() -> list[dict[str, Any]]:
    specs = [
        ("RUN2750_0_sources", "lambdaR origin/stress/class source rows loaded", "PASS", "2749 handoff plus 1562 precedent and route CSVs loaded"),
        ("RUN2750_1_delta_lambda", "delta lambda_R closes R_AB", "PASS_FORMAL_ONLY", "formal variation is not enough for parent derivation"),
        ("RUN2750_2_stress", "lambda_R zero stress", "FAIL_CURRENT_CLAIM", "metric variation can leave unowned stress unless auxiliary source-silence gates close"),
        ("RUN2750_3_first_class", "first-class constraint promotion", "REJECT_CURRENT_PROMOTION", "preservation, brackets, degree count, and boundary generator are absent"),
        ("RUN2750_4_second_class", "second-class auxiliary compatibility route", "PASS_CONDITIONAL_ROUTE_ONLY", "best next route if parent sort/no-derivative/matter/boundary/readout gates pass"),
        ("RUN2750_5_claim", "local GR/Newton claim", "BLOCKED_NO_CLAIM", "lambda_R is not parent-signed"),
    ]
    return [nonclaim({"same_parent_branch_id": BRANCH_ID, "runner_id": rid, "test": test, "current_status": status, "detail": detail}) for rid, test, status, detail in specs]


def gate_rows() -> list[dict[str, Any]]:
    specs = [
        ("GATE2750_0_lambda_origin", "lambda_R parent origin", "BLOCKED_NO_CLAIM", "bare multiplier insertion is not a derivation"),
        ("GATE2750_1_zero_stress", "lambda_R zero-stress/reaction-stress theorem", "BLOCKED_NO_CLAIM", "metric variation stress silence not proven"),
        ("GATE2750_2_first_class", "first-class parent constraint", "BLOCKED_NO_CLAIM", "constraint preservation/bracket/boundary/degree certificates absent"),
        ("GATE2750_3_second_class", "second-class auxiliary compatibility theorem", "OPEN_CONDITIONAL_NONCLAIM", "best route, but parent sort/no-derivative/matter/boundary/readout gates unsigned"),
        ("GATE2750_4_local_GR", "derived local GR/Newton reduction", "BLOCKED_NO_CLAIM", "q_R=0 remains closure unless auxiliary compatibility is signed"),
        ("GATE2750_5_empirical_score", "local empirical score", "BLOCKED_NO_CLAIM", "bounded runner scores hypothetical q_R/delta_beta only"),
    ]
    return [nonclaim({"claim_gate_id": gid, "claim_gate": gate, "status": status, "reason": reason}) for gid, gate, status, reason in specs]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        ("DEC2750_0_verdict", "lambda_R as parent derivation", "NOT_PARENT_SIGNED_ZERO_STRESS_FAILED", "delta lambda_R is formal; parent origin and stress silence are not proven"),
        ("DEC2750_1_route", "best route", "SECOND_CLASS_AUXILIARY_COMPATIBILITY_CONDITIONAL", "first-class language is currently weaker than auxiliary compatibility because the algebra/boundary machinery is absent"),
        ("DEC2750_2_next", "next target", "NEXT_2751_RAB_AUXILIARY_COMPATIBILITY_GRAMMAR", "prove or reject parent sort/no-derivative grammar before trying local-GR promotion again"),
    ]
    return [nonclaim({"decision_id": did, "decision": decision, "result": result, "reason": reason}) for did, decision, result, reason in specs]


def next_rows() -> list[dict[str, Any]]:
    return [
        nonclaim(
            {
                "next_id": "NEXT2750_0_2751",
                "status": "selected_primary",
                "target_doc": "2751-Y5-R2FR-RAB-auxiliary-compatibility-parent-sort-and-no-derivative-grammar-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_RAB_auxiliary_compatibility_parent_sort_and_no_derivative_grammar_under_AX1090_2751.py",
                "mission": "prove or reject that R_AB is an auxiliary compatibility coordinate with no legal derivative/kinetic operators, so Lambda_R can be algebraically eliminated without Q_R hair; otherwise retain finite q_R/Z_R bounded closure branch",
                "acceptance": "sign parent sort, operator exclusion, matter descent, boundary silence, and readout stability; or reject auxiliary theorem and keep finite q_R branch",
                "forbidden": "do not call second-class compatibility a theorem unless parent sort, operator exclusion, matter descent, boundary silence, and readout stability are all signed; do not edit formalization-workbench",
                "selected": True,
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({"copy_id": "BR2750_0_routes", "source_table": rel(OUTPUTS["routes"]), "copy_path": rel(BRANCH_OUTPUTS["routes"]), "purpose": "source-weight lambdaR route decision", "exists": BRANCH_OUTPUTS["routes"].exists()}),
        nonclaim({"copy_id": "BR2750_1_stress", "source_table": rel(OUTPUTS["stress"]), "copy_path": rel(BRANCH_OUTPUTS["stress"]), "purpose": "local-bound lambdaR zero-stress gate", "exists": BRANCH_OUTPUTS["stress"].exists()}),
        nonclaim({"copy_id": "BR2750_2_next_queue", "source_table": rel(OUTPUTS["next"]), "copy_path": rel(BRANCH_OUTPUTS["next_queue"]), "purpose": "RAB acquisition queue for auxiliary compatibility grammar", "exists": BRANCH_OUTPUTS["next_queue"].exists()}),
    ]


def formalization_recent_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    start = SCRIPT_START_UTC.timestamp()
    return sum(1 for path in FORMALIZATION.rglob("*") if path.is_file() and path.stat().st_mtime >= start)


def pycache_path() -> Path:
    return Path(__file__).resolve().parent / "__pycache__"


def remove_pycache() -> None:
    pycache = pycache_path()
    if pycache.exists():
        shutil.rmtree(pycache)


def validation_rows(
    sources: list[dict[str, Any]],
    origin: list[dict[str, Any]],
    stress: list[dict[str, Any]],
    constraint: list[dict[str, Any]],
    boundary: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    source_ok = all(row["exists"] is True and row["needles_present"] is True for row in sources)
    origin_ok = any(row["origin_id"] == "ORG2750_3_second_class_auxiliary" and row["status"] == "BEST_CONDITIONAL_ROUTE_UNSIGNED" for row in origin)
    stress_ok = any(row["stress_id"] == "STR2750_1_multiplier_metric_stress" and row["status"] == "FAIL_UNSIGNED" for row in stress) and any(row["stress_id"] == "STR2750_5_current" and row["status"] == "FAIL_CURRENT_CLAIM" for row in stress)
    class_ok = any(row["class_id"] == "CLASS2750_2_preservation" and row["status"] == "BLOCKED" for row in constraint) and any(row["class_id"] == "CLASS2750_5_second_class" and row["status"] == "BETTER_CONDITIONAL_THAN_FIRST_CLASS" for row in constraint)
    boundary_ok = len(boundary) == 5 and all(row["status"] == "UNSIGNED" for row in boundary)
    route_ok = any(row["route_id"] == "ROUTE2750_1_second_class_auxiliary" and row["verdict"] == "BEST_DERIVATION_ROUTE_CONDITIONAL" for row in routes)
    runner_ok = any(row["runner_id"] == "RUN2750_2_stress" and row["current_status"] == "FAIL_CURRENT_CLAIM" for row in runner)
    gates_ok = any(row["claim_gate_id"] == "GATE2750_3_second_class" and row["status"] == "OPEN_CONDITIONAL_NONCLAIM" for row in gates) and any(row["claim_gate_id"] == "GATE2750_4_local_GR" and row["status"] == "BLOCKED_NO_CLAIM" for row in gates)
    no_claim_flags_ok = all(row.get("valid_for_claim") is False and row.get("claim_allowed") is False for block in [origin, stress, constraint, boundary, routes, runner, gates] for row in block)
    next_ok = next_target[0]["selected"] is True and "2751" in next_target[0]["target_doc"] and "auxiliary-compatibility" in next_target[0]["target_doc"]
    branch_ok = all(path.exists() for path in BRANCH_OUTPUTS.values())
    pycache_ok = not pycache_path().exists()
    formalization_count = formalization_recent_count()
    formalization_ok = formalization_count == 0
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
        {"validation_id": "VAL2750_0_sources", "passed": source_ok, "detail": "all source paths exist and required anchors/needles are present", "timestamp_utc": ts()},
        {"validation_id": "VAL2750_1_origin_best_route", "passed": origin_ok, "detail": "second-class auxiliary route selected as best conditional", "timestamp_utc": ts()},
        {"validation_id": "VAL2750_2_stress_fail", "passed": stress_ok, "detail": "zero-stress theorem fails current claim", "timestamp_utc": ts()},
        {"validation_id": "VAL2750_3_first_class_blocked", "passed": class_ok, "detail": "first-class preservation/bracket route blocked and second-class route preferred conditionally", "timestamp_utc": ts()},
        {"validation_id": "VAL2750_4_boundary_unsigned", "passed": boundary_ok, "detail": "boundary/degree/matter/readout/operator gates remain unsigned", "timestamp_utc": ts()},
        {"validation_id": "VAL2750_5_route_decision", "passed": route_ok, "detail": "route decision ledger favors auxiliary compatibility conditionally", "timestamp_utc": ts()},
        {"validation_id": "VAL2750_6_runner_claim_block", "passed": runner_ok, "detail": "runner blocks local claim", "timestamp_utc": ts()},
        {"validation_id": "VAL2750_7_claim_gates", "passed": gates_ok and no_claim_flags_ok, "detail": "all claim gates remain nonclaim/blocked and flags false", "timestamp_utc": ts()},
        {"validation_id": "VAL2750_8_next_target", "passed": next_ok, "detail": "next target is auxiliary parent sort/no-derivative grammar", "timestamp_utc": ts()},
        {"validation_id": "VAL2750_9_branch_outputs", "passed": branch_ok, "detail": "branch copies exist", "timestamp_utc": ts()},
        {"validation_id": "VAL2750_10_csv_parse", "passed": csv_ok, "detail": "; ".join(csv_bits), "timestamp_utc": ts()},
        {"validation_id": "VAL2750_11_pycache_absent", "passed": pycache_ok, "detail": f"scripts __pycache__ absent={pycache_ok}", "timestamp_utc": ts()},
        {"validation_id": "VAL2750_12_formalization_untouched", "passed": formalization_ok, "detail": f"formalization-workbench recent modified-file count since script start = {formalization_count}", "timestamp_utc": ts()},
    ]
    rows.append(
        {
            "validation_id": "VAL2750_OVERALL",
            "passed": all(row["passed"] is True for row in rows),
            "detail": "2750 tests lambda_R parent origin/stress/constraint class, rejects current promotion, and selects auxiliary compatibility grammar next",
            "timestamp_utc": ts(),
        }
    )
    return rows


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    DOC.write_text(
        f"""# 2750 - Y5 R2/f(R): lambda_R Parent-Origin Zero-Stress And First-Class Constraint Test Under AX1090

Status: `Y5_R2FR_2750_lambdaR_not_parent_signed_second_class_auxiliary_route_selected`

## Private Verdict

2750 tests whether `lambda_R R_AB` is a real parent constraint or just closure in better clothes.

The result is strict:

`delta lambda_R -> R_AB=0` is formally true, but not enough.

Current first-class promotion fails because preservation, bracket closure, degree count, and boundary generator are absent. Current zero-stress also fails because `delta_g(lambda_R R_AB)` can leave unowned stress unless `Lambda_R` is eliminated by a signed auxiliary system with matter/boundary/readout silence.

The best next route is not first-class language. It is second-class auxiliary compatibility: prove `R_AB` is a parent auxiliary compatibility coordinate with no legal derivative grammar, no matter source, no boundary source, and stable readout. If that fails, keep finite `q_R` bounded by the PPN runner.

## Source Register

{markdown_table(data["sources"], ["source_id", "description", "source_path", "exists", "needles_present", "missing_needles", "valid_for_claim"])}

## lambda_R Origin Audit

{markdown_table(data["origin"], ["origin_id", "route", "mechanism", "status", "limitation", "valid_for_claim"])}

## Zero-Stress Variation Gate

{markdown_table(data["stress"], ["stress_id", "variation", "result", "status", "reason", "valid_for_claim"])}

## Constraint Class Gate

{markdown_table(data["constraint"], ["class_id", "constraint_test", "required_statement", "status", "blocker", "valid_for_claim"])}

## Boundary/Degree/Readout Gate

{markdown_table(data["boundary"], ["boundary_id", "gate", "required_statement", "status", "blocker", "valid_for_claim"])}

## Route Decision Ledger

{markdown_table(data["routes"], ["route_id", "route", "verdict", "reason", "next_action", "valid_for_claim"])}

## Runner

{markdown_table(data["runner"], ["runner_id", "test", "current_status", "detail", "valid_for_claim"])}

## Claim Gates

{markdown_table(data["gates"], ["claim_gate_id", "claim_gate", "status", "reason", "valid_for_claim"])}

## Decision Ledger

{markdown_table(data["decisions"], ["decision_id", "decision", "result", "reason", "valid_for_claim"])}

## Next Target

{markdown_table(data["next"], ["next_id", "status", "target_doc", "target_script", "mission", "acceptance", "forbidden", "selected", "valid_for_claim"])}

## Branch Copies

{markdown_table(data["branches"], ["copy_id", "source_table", "copy_path", "purpose", "exists", "valid_for_claim"])}

## Validation

{markdown_table(data["validation"], ["validation_id", "passed", "detail", "timestamp_utc"])}

## Plain-English Read

This is the coupling hinge, but it has not clicked shut yet. `lambda_R` can enforce the right local geometry only if it is a legitimate auxiliary compatibility object, not a free multiplier we invented to win. The next pass is therefore parent grammar: is `R_AB` legally auxiliary and non-derivative, or does finite reciprocal hair remain part of the theory?
""",
        encoding="utf-8",
    )


def main() -> None:
    ensure_dirs()
    sources = source_rows()
    origin = origin_rows()
    stress = stress_rows()
    constraint = constraint_rows()
    boundary = boundary_rows()
    routes = route_rows()
    runner = runner_rows()
    gates = gate_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["origin"], origin)
    write_csv(OUTPUTS["stress"], stress)
    write_csv(OUTPUTS["constraint"], constraint)
    write_csv(OUTPUTS["boundary"], boundary)
    write_csv(OUTPUTS["routes"], routes)
    write_csv(OUTPUTS["runner"], runner)
    write_csv(OUTPUTS["gates"], gates)
    write_csv(OUTPUTS["decisions"], decisions)
    write_csv(OUTPUTS["next"], next_target)

    write_csv(BRANCH_OUTPUTS["routes"], routes)
    write_csv(BRANCH_OUTPUTS["stress"], stress)
    write_csv(BRANCH_OUTPUTS["next_queue"], next_target)
    branches = branch_rows()
    write_csv(OUTPUTS["branches"], branches)

    remove_pycache()
    validation = validation_rows(sources, origin, stress, constraint, boundary, routes, runner, gates, next_target)
    write_csv(OUTPUTS["validation"], validation)

    data = {
        "sources": sources,
        "origin": origin,
        "stress": stress,
        "constraint": constraint,
        "boundary": boundary,
        "routes": routes,
        "runner": runner,
        "gates": gates,
        "decisions": decisions,
        "next": next_target,
        "branches": branches,
        "validation": validation,
    }
    write_doc(data)

    remove_pycache()

    if not all(row["passed"] is True for row in validation):
        failed = [row for row in validation if row["passed"] is not True]
        raise SystemExit(f"2750 validation failed: {failed}")
    print(f"wrote {DOC}")
    print(f"validation {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
