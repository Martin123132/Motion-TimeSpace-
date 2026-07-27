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
DOC = ROOT / "1562-Y5-lambdaR-parent-origin-zero-stress-and-first-class-constraint-test.md"
START_TS = datetime.now(timezone.utc).timestamp()

SOURCE_FILES = {
    "1561_doc": ROOT / "1561-Y5-minimal-parent-weak-field-action-ansatz-and-Euler-Ward-PPN-gate.md",
    "1561_validation": OUT / "P8_Y5_BRR545_1561_VALIDATION.csv",
    "1561_next": OUT / "P8_Y5_PARENT_QLOC_1561_NEXT_TARGET.csv",
    "1561_euler": OUT / "P8_Y5_PARENT_QLOC_1561_EULER_VARIATION_GATE.csv",
    "1561_ansatz": OUT / "P8_Y5_PARENT_QLOC_1561_MINIMAL_ACTION_ANSATZ_REGISTER.csv",
    "07_doc": ROOT / "07-nonpropagating-reciprocity-constraint.md",
    "19_doc": ROOT / "19-constrained-parent-action-skeleton.md",
    "1248_doc": ROOT / "1248-Y5-R10-minimal-lambdaR-parent-action-ansatz-and-Dirac-check.md",
    "1268_doc": ROOT / "1268-Y5-R10-RAB-second-class-auxiliary-compatibility-action-or-finite-ZR-source-row.md",
    "1555_doc": ROOT / "1555-Y5-gauge-noether-zero-charge-qsector-origin-audit.md",
}

NEEDLES = {
    "1561_doc": ["`lambda_R` still lacks parent origin and zero-stress proof", "prove or reject `lambda_R`"],
    "1561_validation": ["VAL1561_OVERALL", "PASS"],
    "1561_next": ["1562-Y5-lambdaR-parent-origin-zero-stress-and-first-class-constraint-test.md"],
    "1561_euler": ["EUL1561_1_lambda_variation", "FAIL_UNSIGNED_STRESS_SILENCE"],
    "1561_ansatz": ["ANS1561_A_EH_lambdaR_silent", "BEST_CONDITIONAL_ANSATZ_NOT_ADOPTED"],
    "07_doc": ["S_constraint = integral lambda_R R_AB", "why does the parent motion-load action contain lambda_R"],
    "19_doc": ["S_R_constraint = integral sqrt(-g) lambda_R R_AB.", "closure_term."],
    "1248_doc": ["minimal `lambda_R C_R` parent-action ansatz", "REJECT_ZERO_THEOREM_UNDERIVED"],
    "1268_doc": ["second-class/algebraic auxiliary compatibility action", "EXACT_CONDITIONAL_NOT_PARENT_SIGNED"],
    "1555_doc": ["first-class parent constraint", "POSSIBLE_IN_PRINCIPLE_NOT_PRESENT"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1562_SOURCE_REGISTER.csv"
ORIGIN_AUDIT = OUT / "P8_Y5_PARENT_QLOC_1562_LAMBDAR_ORIGIN_AUDIT.csv"
STRESS_GATE = OUT / "P8_Y5_PARENT_QLOC_1562_ZERO_STRESS_VARIATION_GATE.csv"
CLASS_GATE = OUT / "P8_Y5_PARENT_QLOC_1562_CONSTRAINT_CLASS_GATE.csv"
BOUNDARY_GATE = OUT / "P8_Y5_PARENT_QLOC_1562_BOUNDARY_DEGREE_COUNT_GATE.csv"
ROUTE_DECISION = OUT / "P8_Y5_PARENT_QLOC_1562_ROUTE_DECISION_LEDGER.csv"
RUNNER = OUT / "P8_Y5_PARENT_QLOC_1562_RUNNER_NONCLAIM.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1562_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1562_DECISION.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1562_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1562_VALIDATION.csv"

QUARANTINE = MICROSCOPE / "quarantine" / "1562"
QUAR_ORIGIN = QUARANTINE / "LAMBDAR_ORIGIN_AUDIT_NONCLAIM.csv"
QUAR_STRESS = QUARANTINE / "ZERO_STRESS_VARIATION_GATE_NONCLAIM.csv"
QUAR_CLASS = QUARANTINE / "CONSTRAINT_CLASS_GATE_NONCLAIM.csv"
QUAR_BOUNDARY = QUARANTINE / "BOUNDARY_DEGREE_COUNT_GATE_NONCLAIM.csv"
QUAR_ROUTE = QUARANTINE / "ROUTE_DECISION_LEDGER_NONCLAIM.csv"
QUAR_RUNNER = QUARANTINE / "RUNNER_NONCLAIM.csv"
QUAR_DECISION = QUARANTINE / "DECISION_NONCLAIM.csv"
BRANCH_ORIGIN = BRANCH_RESIDUALS / "lambdaR_origin_audit_nonclaim_1562.csv"
BRANCH_STRESS = BRANCH_RESIDUALS / "zero_stress_variation_gate_nonclaim_1562.csv"
BRANCH_CLASS = BRANCH_RESIDUALS / "constraint_class_gate_nonclaim_1562.csv"
BRANCH_BOUNDARY = BRANCH_RESIDUALS / "boundary_degree_count_gate_nonclaim_1562.csv"
BRANCH_ROUTE = BRANCH_RESIDUALS / "route_decision_ledger_nonclaim_1562.csv"
BRANCH_RUNNER = BRANCH_RESIDUALS / "lambdaR_runner_nonclaim_1562.csv"
BRANCH_DECISION = BRANCH_RESIDUALS / "lambdaR_decision_nonclaim_1562.csv"


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


def file_contains(path: Path, needles: list[str]) -> bool:
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8", errors="ignore")
    return all(needle in text for needle in needles)


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
    rows = []
    for index, (key, path) in enumerate(SOURCE_FILES.items()):
        needles = NEEDLES.get(key, [])
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "source_id": f"SRC1562_{index}_{key}",
                "source_path": rel(path),
                "exists": path.exists(),
                "needle_found": file_contains(path, needles) if needles else True,
                "needles": "; ".join(needles),
                "purpose": "evidence for lambda_R parent-origin, zero-stress, and constraint-class test",
                **flags(),
            }
        )
    return rows


def origin_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "ORG1562_0_delta_lambda",
            "bare multiplier insertion",
            "S_lambda=int sqrt(-g) lambda_R R_AB; delta lambda_R -> R_AB=0",
            "FORMAL_ONLY",
            "variation works but does not explain why lambda_R exists in the parent action",
            "REJECT_AS_DERIVATION",
        ),
        (
            "ORG1562_1_phase_volume",
            "phase-volume/cell-balance motivation",
            "local reciprocal volume balance suggests a nonpropagating constraint",
            "MOTIVATION_ONLY",
            "motivation does not supply L_parent, symplectic form, or variation class",
            "NOT_PARENT_SIGNED",
        ),
        (
            "ORG1562_2_first_class",
            "first-class constraint route",
            "C_R=R_AB with differentiable generator, zero/proper boundary charge, bracket closure, and degree count",
            "POSSIBLE_IN_PRINCIPLE",
            "generator, brackets, boundary charge, and degree count are not supplied",
            "NOT_PRESENT",
        ),
        (
            "ORG1562_3_second_class_auxiliary",
            "second-class/algebraic auxiliary compatibility route",
            "S_R=int mu_parent Lambda_R [R_AB-C_AB(q,theta,top)] with no derivative grammar",
            "BEST_CONDITIONAL_ROUTE",
            "parent sort, no-derivative operator exclusion, matter descent, boundary silence, and readout stability remain unsigned",
            "KEEP_AS_REPAIR_TARGET",
        ),
        (
            "ORG1562_4_kinetic_RAB",
            "kinetic reciprocal strain",
            "0.5 W (grad R_AB)^2 gives reciprocal hair Q_R/r",
            "REJECTED",
            "turns q_R=0 into an unsolved zero-charge theorem",
            "FINITE_QR_BRANCH_IF_ALLOWED",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "origin_id": origin_id,
            "route": route,
            "mechanism": mechanism,
            "status": status,
            "problem": problem,
            "decision": decision,
            "source_paths": source_list("07_doc", "19_doc", "1248_doc", "1268_doc", "1555_doc", "1561_euler"),
            **flags(),
        }
        for origin_id, route, mechanism, status, problem, decision in rows
    ]


def stress_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "STR1562_0_multiplier_E_lambda",
            "delta_{lambda_R} S",
            "R_AB=0",
            "PASS_FORMAL",
            "this is only the constraint equation",
            "NOT_ENOUGH_FOR_ZERO_STRESS",
        ),
        (
            "STR1562_1_multiplier_metric_stress",
            "delta_g(lambda_R R_AB)",
            "terms proportional to lambda_R delta_g R_AB can survive even when R_AB=0",
            "FAIL_UNSIGNED",
            "on-shell R_AB=0 alone does not prove lambda_R carries no metric/source stress",
            "NEEDS_E_R_OR_REACTION_STRESS_THEOREM",
        ),
        (
            "STR1562_2_aux_E_R",
            "delta_{R_AB} S_R",
            "Lambda_R + J_R + delta B_R/delta R_AB + readout_regen = 0",
            "PASS_ONLY_IF_SOURCES_ZERO",
            "Lambda_R=0 follows only with matter descent, boundary silence, and readout stability",
            "EXACT_CONDITIONAL",
        ),
        (
            "STR1562_3_no_derivative",
            "operator grammar",
            "no D R_AB, D Lambda_R, vertical metric, or boundary derivative operator",
            "REQUIRED_UNSIGNED",
            "derivative terms regenerate physical R_AB hair and boundary charge",
            "NEEDS_OPERATOR_EXCLUSION_PROOF",
        ),
        (
            "STR1562_4_matter_boundary_readout",
            "source and boundary variations",
            "delta S_matter/delta R_AB=0 and delta B/delta R_AB=0 before readout",
            "REQUIRED_UNSIGNED",
            "otherwise E_R sources finite Lambda_R or reciprocal hair",
            "NEEDS_DESCENT_AND_BOUNDARY_CERTIFICATES",
        ),
        (
            "STR1562_5_current",
            "zero-stress verdict",
            "no current proof that lambda_R is zero-stress in the accepted parent action",
            "FAIL_CURRENT_CLAIM",
            "best route is exact conditional auxiliary compatibility, not first-class promotion",
            "LOCAL_GR_STILL_BLOCKED",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "stress_id": stress_id,
            "variation": variation,
            "result": result,
            "status": status,
            "reason": reason,
            "next_condition": next_condition,
            "source_paths": source_list("1268_doc", "1561_euler", "19_doc"),
            **flags(),
        }
        for stress_id, variation, result, status, reason, next_condition in rows
    ]


def class_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "CLASS1562_0_first_primary",
            "first-class/Dirac primary",
            "pi_lambda approx 0",
            "FORMAL_PASS_WITHIN_ANSATZ",
            "only after lambda_R is inserted",
        ),
        (
            "CLASS1562_1_first_secondary",
            "first-class/Dirac secondary",
            "C_R=R_AB approx 0",
            "FORMAL_PASS_WITHIN_ANSATZ",
            "desired closure appears as secondary constraint",
        ),
        (
            "CLASS1562_2_preservation",
            "constraint preservation",
            "dot C_R={C_R,H_core}+... closes or fixes multiplier",
            "BLOCKED",
            "H_core and Poisson brackets for parent variables are absent",
        ),
        (
            "CLASS1562_3_brackets_degree",
            "constraint class and degree count",
            "brackets close and remove reciprocal pair without hiding physical mode",
            "BLOCKED",
            "no algebra/degree-count certificate exists",
        ),
        (
            "CLASS1562_4_boundary_generator",
            "differentiable generator",
            "G_R[epsilon]=int epsilon C_R + Q_R has zero/proper boundary charge",
            "BLOCKED",
            "boundary/corner charge audit missing",
        ),
        (
            "CLASS1562_5_second_class",
            "second-class auxiliary elimination",
            "E_Lambda and E_R eliminate R_AB,Lambda_R algebraically before readout",
            "BETTER_CONDITIONAL_THAN_FIRST_CLASS",
            "still unsigned until parent sort/no-derivative/matter/boundary/readout gates pass",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "class_id": class_id,
            "constraint_test": constraint_test,
            "required_statement": required_statement,
            "status": status,
            "blocker": blocker,
            "source_paths": source_list("1248_doc", "1268_doc", "1555_doc"),
            **flags(),
        }
        for class_id, constraint_test, required_statement, status, blocker in rows
    ]


def boundary_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "BD1562_0_no_QR",
            "no reciprocal boundary charge",
            "R_AB/Lambda_R sector has no differentiable boundary charge after elimination",
            "UNSIGNED",
            "no boundary/corner variational class proves this",
        ),
        (
            "BD1562_1_degree",
            "degree-count safety",
            "auxiliary pair removes no physical propagating local mode",
            "UNSIGNED",
            "parent sort and phase-space list are not sourced from primitives",
        ),
        (
            "BD1562_2_matter",
            "matter descent",
            "matter action factors through public/quotient variables and not R_AB",
            "UNSIGNED",
            "without this E_R has J_R source",
        ),
        (
            "BD1562_3_readout",
            "readout stability",
            "eliminating R_AB,Lambda_R does not regenerate finite q_R in effective/readout action",
            "UNSIGNED",
            "readout/EFT closure proof absent",
        ),
        (
            "BD1562_4_operator",
            "no derivative operator",
            "D R_AB kinetic/gradient operators are illegal in the parent grammar",
            "UNSIGNED",
            "if allowed, finite q_R/Z_R source branch is required",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "boundary_id": boundary_id,
            "gate": gate,
            "required_statement": required_statement,
            "status": status,
            "blocker": blocker,
            "source_paths": source_list("1268_doc", "1248_doc", "1555_doc"),
            **flags(),
        }
        for boundary_id, gate, required_statement, status, blocker in rows
    ]


def route_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "route_id": "ROUTE1562_0_first_class",
            "route": "first-class lambda_R/R_AB constraint",
            "verdict": "REJECT_CURRENT_PROMOTION",
            "reason": "primary/secondary steps are formal, but preservation, brackets, degree count, and boundary generator are missing",
            "next_action": "do not spend next pass on first-class language unless parent H_core and symplectic form are supplied",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "route_id": "ROUTE1562_1_second_class_auxiliary",
            "route": "second-class auxiliary compatibility",
            "verdict": "BEST_DERIVATION_ROUTE_CONDITIONAL",
            "reason": "E_Lambda enforces compatibility and E_R can kill Lambda_R/stress if matter, boundary, readout, and derivative grammar gates pass",
            "next_action": "attack parent sort and no-derivative grammar first",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "route_id": "ROUTE1562_2_finite_qR",
            "route": "bounded finite q_R fallback",
            "verdict": "FALLBACK_IF_AUXILIARY_GATES_FAIL",
            "reason": "1559 control runner can bound finite q_R/delta_beta without claiming derivation",
            "next_action": "keep as nonclaim fallback",
            **flags(),
        },
    ]


def runner_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1562_0_sources",
            "test": "lambda_R hinge sources loaded",
            "current_status": "PASS",
            "detail": "1561, 07, 19, 1248, 1268, and 1555 evidence loaded",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1562_1_origin",
            "test": "lambda_R parent origin",
            "current_status": "FAILED_CURRENT_PARENT_ORIGIN",
            "detail": "lambda_R remains inserted/motivated, not parent-derived",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1562_2_stress",
            "test": "zero-stress theorem",
            "current_status": "FAILED_CURRENT_ZERO_STRESS",
            "detail": "delta lambda_R gives R_AB=0, but zero stress requires E_R/source/boundary/readout silence not signed",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1562_3_class",
            "test": "first-class vs auxiliary route",
            "current_status": "SECOND_CLASS_AUXILIARY_BEST_CONDITIONAL",
            "detail": "first-class route is not present; auxiliary compatibility is mathematically cleaner but still unsigned",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1562_4_claim",
            "test": "local GR/Newton claim",
            "current_status": "BLOCKED_NO_CLAIM",
            "detail": "q_R=0 remains closure/conditional; bounded PPN runner remains the honest test lane",
            **flags(),
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("GATE1562_0_origin", "lambda_R parent origin", "BLOCKED_NO_CLAIM", "origin remains schematic/motivational"),
        ("GATE1562_1_stress", "lambda_R zero stress", "BLOCKED_NO_CLAIM", "E_R/source/boundary/readout silence not signed"),
        ("GATE1562_2_first_class", "first-class constraint promotion", "BLOCKED_NO_CLAIM", "brackets, generator, degree count, and boundary charge missing"),
        ("GATE1562_3_auxiliary", "second-class auxiliary theorem", "BLOCKED_NO_CLAIM", "exact conditional only; parent sort/no-derivative/matter/boundary/readout gates unsigned"),
        ("GATE1562_4_qR", "q_R=0 as MTS prediction", "BLOCKED_NO_CLAIM", "lambda_R route not parent-signed"),
        ("GATE1562_5_local_GR", "derived local GR/Newton", "BLOCKED_NO_CLAIM", "bounded closure control remains active"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "claim_gate": claim_gate,
            "status": status,
            "reason": reason,
            "source_paths": source_list("1561_doc", "1248_doc", "1268_doc", "1555_doc"),
            **flags(),
        }
        for gate_id, claim_gate, status, reason in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1562_0_verdict",
            "decision": "lambda_R as parent derivation",
            "result": "NOT_PARENT_SIGNED_ZERO_STRESS_FAILED",
            "reason": "delta lambda_R is formal; parent origin and stress silence are not proven",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1562_1_best_route",
            "decision": "least-cheaty repair path",
            "result": "SECOND_CLASS_AUXILIARY_COMPATIBILITY_ROUTE",
            "reason": "auxiliary elimination can make Lambda_R zero and avoid Q_R hair if parent sort/no-derivative/matter/boundary/readout gates are signed",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1562_2_next",
            "decision": "next target",
            "result": "NEXT_1563_AUXILIARY_PARENT_SORT_NO_DERIVATIVE_GRAMMAR",
            "reason": "the next decisive gate is whether R_AB is an auxiliary compatibility coordinate with derivative operators forbidden",
            **flags(),
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "next_id": "NEXT1562_0_1563",
            "next_target": "1563-Y5-RAB-auxiliary-compatibility-parent-sort-and-no-derivative-grammar.md",
            "script": "scripts/Y5_RAB_auxiliary_compatibility_parent_sort_and_no_derivative_grammar.py",
            "objective": "prove or reject that R_AB is an auxiliary compatibility coordinate with no legal derivative/kinetic operators, so Lambda_R can be algebraically eliminated without Q_R hair; otherwise retain finite q_R/Z_R bounded closure branch",
            "do_not": "do not call second-class compatibility a theorem unless parent sort, operator exclusion, matter descent, boundary silence, and readout stability are all signed; do not edit formalization-workbench",
            **flags(),
        }
    ]


def copy_outputs() -> None:
    copies = [
        (ORIGIN_AUDIT, QUAR_ORIGIN),
        (STRESS_GATE, QUAR_STRESS),
        (CLASS_GATE, QUAR_CLASS),
        (BOUNDARY_GATE, QUAR_BOUNDARY),
        (ROUTE_DECISION, QUAR_ROUTE),
        (RUNNER, QUAR_RUNNER),
        (DECISION, QUAR_DECISION),
        (ORIGIN_AUDIT, BRANCH_ORIGIN),
        (STRESS_GATE, BRANCH_STRESS),
        (CLASS_GATE, BRANCH_CLASS),
        (BOUNDARY_GATE, BRANCH_BOUNDARY),
        (ROUTE_DECISION, BRANCH_ROUTE),
        (RUNNER, BRANCH_RUNNER),
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
    origins = read_csv(ORIGIN_AUDIT)
    stress = read_csv(STRESS_GATE)
    class_gate = read_csv(CLASS_GATE)
    boundary = read_csv(BOUNDARY_GATE)
    routes = read_csv(ROUTE_DECISION)
    run_rows = read_csv(RUNNER)
    gate_rows = read_csv(CLAIM_GATE)
    decision_items = read_csv(DECISION)
    next_rows = read_csv(NEXT_TARGET)

    checks = [
        ("VAL1562_0_sources_exist", all(row["exists"] == "True" for row in sources), "all cited 1562 source paths exist"),
        ("VAL1562_1_needles_found", all(row["needle_found"] == "True" for row in sources), "all registered evidence needles found"),
        ("VAL1562_2_origin_best_route", any(row["origin_id"] == "ORG1562_3_second_class_auxiliary" and row["status"] == "BEST_CONDITIONAL_ROUTE" for row in origins), "second-class auxiliary route selected as best conditional"),
        ("VAL1562_3_origin_not_signed", any(row["origin_id"] == "ORG1562_0_delta_lambda" and row["decision"] == "REJECT_AS_DERIVATION" for row in origins), "bare delta-lambda route rejected as derivation"),
        ("VAL1562_4_stress_fail", any(row["stress_id"] == "STR1562_5_current" and row["status"] == "FAIL_CURRENT_CLAIM" for row in stress), "zero-stress theorem fails current claim"),
        ("VAL1562_5_first_class_blocked", any(row["class_id"] == "CLASS1562_2_preservation" and row["status"] == "BLOCKED" for row in class_gate), "first-class preservation/bracket route blocked"),
        ("VAL1562_6_boundary_unsigned", all(row["status"] == "UNSIGNED" for row in boundary), "boundary/degree/matter/readout/operator gates remain unsigned"),
        ("VAL1562_7_route_decision", any(row["route_id"] == "ROUTE1562_1_second_class_auxiliary" and row["verdict"] == "BEST_DERIVATION_ROUTE_CONDITIONAL" for row in routes), "route decision ledger favors auxiliary compatibility conditionally"),
        ("VAL1562_8_runner_claim_block", any(row["runner_id"] == "RUN1562_4_claim" and row["current_status"] == "BLOCKED_NO_CLAIM" for row in run_rows), "runner blocks local claim"),
        ("VAL1562_9_claim_gates", all(row["status"] == "BLOCKED_NO_CLAIM" for row in gate_rows), "all claim gates remain blocked"),
        ("VAL1562_10_decision_next", any(row["result"] == "NEXT_1563_AUXILIARY_PARENT_SORT_NO_DERIVATIVE_GRAMMAR" for row in decision_items), "decision selects auxiliary parent sort/no-derivative grammar next"),
        ("VAL1562_11_next_target", any("1563-Y5-RAB-auxiliary-compatibility" in row["next_target"] for row in next_rows), "next target is auxiliary compatibility parent sort/no-derivative grammar"),
        ("VAL1562_12_csv_parse", all(parse_csv(path) for path in generated_csvs), "all generated 1562 CSVs parse cleanly"),
        ("VAL1562_13_claim_flags_false", generated_flags_false(generated_csvs), "all generated prediction/claim flags remain false"),
        ("VAL1562_14_branch_copies", all(path.exists() for path in [QUAR_ORIGIN, QUAR_STRESS, QUAR_CLASS, QUAR_BOUNDARY, QUAR_ROUTE, QUAR_RUNNER, QUAR_DECISION, BRANCH_ORIGIN, BRANCH_STRESS, BRANCH_CLASS, BRANCH_BOUNDARY, BRANCH_ROUTE, BRANCH_RUNNER, BRANCH_DECISION]), "branch/quarantine nonclaim copies written"),
        ("VAL1562_15_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent after run"),
        ("VAL1562_16_formalization_untouched", formalization_modified_count_since_start() == 0, "formalization modified-file count since start=0"),
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
            "check_id": "VAL1562_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1562 lambda_R parent-origin zero-stress and constraint-class test validation",
        }
    )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return "\n".join([header, sep, *body])


def write_doc(
    sources: list[dict[str, Any]],
    origins: list[dict[str, Any]],
    stress: list[dict[str, Any]],
    class_gate: list[dict[str, Any]],
    boundary: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    run_rows: list[dict[str, Any]],
    gate_rows: list[dict[str, Any]],
    decision_items: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 1562 - lambda_R Parent-Origin, Zero-Stress, and Constraint-Class Test",
                "",
                "## Verdict",
                "- `delta lambda_R` formally gives `R_AB=0`, but that alone is not a derivation.",
                "- The first-class route remains blocked by missing preservation, brackets, degree count, and boundary generator.",
                "- The cleaner route is second-class/algebraic auxiliary compatibility: `E_Lambda` enforces `R_AB-C_AB=0`, while `E_R` can kill `Lambda_R` only if matter, boundary, readout, and derivative-operator gates are signed.",
                "- Current MTS does not yet sign those gates, so `q_R=0` remains closure/conditional rather than a parent theorem.",
                "- Next target: prove or reject the auxiliary parent sort and no-derivative grammar.",
                "",
                "## Source Register",
                md_table(sources, ["source_id", "source_path", "exists", "needle_found", "needles"]),
                "",
                "## lambda_R Origin Audit",
                md_table(origins, ["origin_id", "route", "mechanism", "status", "problem", "decision"]),
                "",
                "## Zero-Stress Variation Gate",
                md_table(stress, ["stress_id", "variation", "result", "status", "reason", "next_condition"]),
                "",
                "## Constraint-Class Gate",
                md_table(class_gate, ["class_id", "constraint_test", "required_statement", "status", "blocker"]),
                "",
                "## Boundary / Degree-Count Gate",
                md_table(boundary, ["boundary_id", "gate", "required_statement", "status", "blocker"]),
                "",
                "## Route Decision Ledger",
                md_table(routes, ["route_id", "route", "verdict", "reason", "next_action"]),
                "",
                "## Runner",
                md_table(run_rows, ["runner_id", "test", "current_status", "detail"]),
                "",
                "## Claim Gates",
                md_table(gate_rows, ["gate_id", "claim_gate", "status", "reason"]),
                "",
                "## Decision",
                md_table(decision_items, ["decision_id", "decision", "result", "reason"]),
                "",
                "## Validation",
                md_table(validation, ["check_id", "result", "detail"]),
                "",
                "## Next Target",
                md_table(next_rows, ["next_target", "script", "objective", "do_not"]),
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> None:
    sources = source_register_rows()
    origins = origin_rows()
    stress = stress_rows()
    class_gate = class_rows()
    boundary = boundary_rows()
    routes = route_rows()
    run_rows = runner_rows()
    gate_rows = claim_gate_rows()
    decision_items = decision_rows()
    next_rows = next_target_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(ORIGIN_AUDIT, origins)
    write_csv(STRESS_GATE, stress)
    write_csv(CLASS_GATE, class_gate)
    write_csv(BOUNDARY_GATE, boundary)
    write_csv(ROUTE_DECISION, routes)
    write_csv(RUNNER, run_rows)
    write_csv(CLAIM_GATE, gate_rows)
    write_csv(DECISION, decision_items)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()
    remove_pycache()

    generated_csvs = [
        SOURCE_REGISTER,
        ORIGIN_AUDIT,
        STRESS_GATE,
        CLASS_GATE,
        BOUNDARY_GATE,
        ROUTE_DECISION,
        RUNNER,
        CLAIM_GATE,
        DECISION,
        NEXT_TARGET,
    ]
    validation = validation_rows(generated_csvs)
    write_csv(VALIDATION, validation)
    write_doc(sources, origins, stress, class_gate, boundary, routes, run_rows, gate_rows, decision_items, validation, next_rows)


if __name__ == "__main__":
    main()
