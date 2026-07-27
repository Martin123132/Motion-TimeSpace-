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
DOC = ROOT / "1552-Y5-parent-q-sector-action-norm-extraction-template.md"
START_TS = datetime.now(timezone.utc).timestamp()

SOURCE_FILES = {
    "1551_doc": ROOT / "1551-Y5-parent-qnorm-source-or-local-closure-demotion.md",
    "1551_validation": OUT / "P8_Y5_BRR545_1551_VALIDATION.csv",
    "1551_next": OUT / "P8_Y5_PARENT_QLOC_1551_NEXT_TARGET.csv",
    "1551_hunt": OUT / "P8_Y5_PARENT_QLOC_1551_PARENT_QNORM_SOURCE_HUNT.csv",
    "1551_reentry": OUT / "P8_Y5_PARENT_QLOC_1551_QNORM_REENTRY_CONDITIONS.csv",
    "1551_demotion": OUT / "P8_Y5_PARENT_QLOC_1551_LOCAL_CLOSURE_DEMOTION_GATE.csv",
    "1550_qnorm": OUT / "P8_Y5_PARENT_QLOC_1550_QNORM_CANDIDATE_AUDIT.csv",
    "1550_dual": OUT / "P8_Y5_PARENT_QLOC_1550_DUAL_PAIRING_CONTRACT.csv",
    "1550_envelope": OUT / "P8_Y5_PARENT_QLOC_1550_SCG_ENVELOPE_UNIT_GATE.csv",
    "1550_guard": OUT / "P8_Y5_PARENT_QLOC_1550_NO_MIXED_NORM_GUARD.csv",
    "1549_variational": OUT / "P8_Y5_PARENT_QLOC_1549_VARIATIONAL_SOURCE_CURRENT_LAW.csv",
    "1549_unit": OUT / "P8_Y5_PARENT_QLOC_1549_UNIT_PAIRING_THEOREM_CONDITIONAL.csv",
    "1548_symbolic": OUT / "P8_Y5_PARENT_QLOC_1548_SHARED_SYMBOLIC_PROFILE_CANDIDATES.csv",
    "1547_support": OUT / "P8_Y5_PARENT_QLOC_1547_SUPPORT_DOMAIN_CONVENTIONS.csv",
    "source_owner": OUT / "P8_source_owner_parent_action_terms_CONTRACT.csv",
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1552_SOURCE_REGISTER.csv"
ACTION_TEMPLATE = OUT / "P8_Y5_PARENT_QLOC_1552_PARENT_QSECTOR_ACTION_TEMPLATE.csv"
EXTRACTION_ALGORITHM = OUT / "P8_Y5_PARENT_QLOC_1552_QNORM_EXTRACTION_ALGORITHM.csv"
FAILURE_FILTERS = OUT / "P8_Y5_PARENT_QLOC_1552_ACTION_FAILURE_FILTERS.csv"
REENTRY_RUNNER = OUT / "P8_Y5_PARENT_QLOC_1552_REENTRY_RUNNER_NONCLAIM.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1552_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1552_DECISION.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1552_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1552_VALIDATION.csv"

QUARANTINE = MICROSCOPE / "quarantine" / "1552"
QUAR_ACTION = QUARANTINE / "PARENT_QSECTOR_ACTION_TEMPLATE_NONCLAIM.csv"
QUAR_EXTRACTION = QUARANTINE / "QNORM_EXTRACTION_ALGORITHM_NONCLAIM.csv"
QUAR_FILTERS = QUARANTINE / "ACTION_FAILURE_FILTERS_NONCLAIM.csv"
QUAR_RUNNER = QUARANTINE / "REENTRY_RUNNER_NONCLAIM.csv"
QUAR_DECISION = QUARANTINE / "DECISION_NONCLAIM.csv"
BRANCH_ACTION = BRANCH_RESIDUALS / "parent_qsector_action_template_nonclaim_1552.csv"
BRANCH_EXTRACTION = BRANCH_RESIDUALS / "qnorm_extraction_algorithm_nonclaim_1552.csv"
BRANCH_FILTERS = BRANCH_RESIDUALS / "action_failure_filters_nonclaim_1552.csv"
BRANCH_RUNNER = BRANCH_RESIDUALS / "reentry_runner_nonclaim_1552.csv"
BRANCH_DECISION = BRANCH_RESIDUALS / "qsector_decision_nonclaim_1552.csv"


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
            "source_id": f"SRC1552_{index}_{key}",
            "source_path": rel(path),
            "exists": path.exists(),
            "purpose": "input evidence for parent q-sector action/norm extraction template",
            **flags(),
        }
        for index, (key, path) in enumerate(SOURCE_FILES.items())
    ]


def action_template_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "slot_id": "ACT1552_0_q_field",
            "action_slot": "q-sector field definition",
            "template_formula": "q^A or q^A(Phi) with dim(q^A), observed-frame descent, and variation class declared",
            "must_supply": "field identity, parent map, dimension, quotient/gauge status, domain",
            "acceptance_test": "q is defined before readout and not selected by local test fits",
            "current_status": "TEMPLATE_REQUIRED_NOT_SUPPLIED",
        },
        {
            "slot_id": "ACT1552_1_quadratic_form",
            "action_slot": "positive parent quadratic form",
            "template_formula": "delta^2 S_q = 1/2 int_W delta q^A G_AB delta q^B dV_e + boundary",
            "must_supply": "G_AB or Hessian/operator, positivity/coercivity, units, gauge quotient",
            "acceptance_test": "G_AB defines one parent-owned E used by both T_source_norm and C_qm",
            "current_status": "TEMPLATE_REQUIRED_NOT_SUPPLIED",
        },
        {
            "slot_id": "ACT1552_2_derivative_operator",
            "action_slot": "kinetic/operator terms",
            "template_formula": "int_W 1/2 Z_AB^{mu nu} nabla_mu q^A nabla_nu q^B dV_e",
            "must_supply": "Z_AB signature, elliptic/hyperbolic branch, boundary conditions, no ghost",
            "acceptance_test": "operator produces a positive local norm or is explicitly quotient/gauge removed",
            "current_status": "TEMPLATE_OPTIONAL_ROUTE",
        },
        {
            "slot_id": "ACT1552_3_regulator",
            "action_slot": "worldtube regulator/excision",
            "template_formula": "E_epsilon[delta q;W_src] with epsilon_reg, support, and matching surface",
            "must_supply": "regulator law, compact support, boundary flux rule, limiting procedure",
            "acceptance_test": "same regulator enters source norm, C_qm, and arena projections",
            "current_status": "TEMPLATE_OPTIONAL_ROUTE",
        },
        {
            "slot_id": "ACT1552_4_matter_coupling",
            "action_slot": "matter source variation",
            "template_formula": "delta S_matter = int_W J_A delta q^A dV_e + boundary",
            "must_supply": "explicit S_matter[q], coupling projector, hidden channel audit",
            "acceptance_test": "J_q is parent-derived and not a readout-defined source",
            "current_status": "TEMPLATE_REQUIRED_NOT_SUPPLIED",
        },
        {
            "slot_id": "ACT1552_5_boundary",
            "action_slot": "boundary and domain terms",
            "template_formula": "delta S_boundary + integration-by-parts boundary terms",
            "must_supply": "zero theorem or finite S_boundary_m bound",
            "acceptance_test": "no boundary term is silently dropped before S_cg envelope scoring",
            "current_status": "TEMPLATE_REQUIRED_NOT_SUPPLIED",
        },
        {
            "slot_id": "ACT1552_6_parent_action_verdict",
            "action_slot": "accepted parent q-sector",
            "template_formula": "S_parent contains q-sector enough to extract E, J_q, Dq[v_m], and boundary accounting",
            "must_supply": "all required slots above",
            "acceptance_test": "reopens local finite branch only after validation",
            "current_status": "NOT_SUPPLIED_CURRENTLY",
        },
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            **row,
            "source_paths": source_list("1551_reentry", "1551_hunt", "1549_variational", "source_owner"),
            **flags(),
        }
        for row in rows
    ]


def extraction_algorithm_rows() -> list[dict[str, Any]]:
    rows = [
        ("ALG1552_0_define_q", "define q and variation domain", "identify q^A, dim(q^A), allowed delta q, gauge/quotient class, and W_src", "BLOCKED_PENDING_PARENT_ACTION"),
        ("ALG1552_1_second_variation", "take parent second variation", "compute delta^2 S_parent restricted to the local q-sector and retained boundary terms", "BLOCKED_PENDING_PARENT_ACTION"),
        ("ALG1552_2_extract_E", "extract E norm", "accept E only if the quadratic form is positive/coercive after quotienting gauge/null directions", "BLOCKED_PENDING_POSITIVITY"),
        ("ALG1552_3_extract_Jq", "extract source current", "derive J_q=delta S_matter/delta q in the same observed frame and variation domain", "BLOCKED_PENDING_PARENT_COUPLING"),
        ("ALG1552_4_compute_Cqm", "compute C_qm", "evaluate C_qm=||Dq[v_m]||_E using the same E", "BLOCKED_PENDING_DQVM"),
        ("ALG1552_5_insert_envelope", "insert S_cg envelope", "use |<J_q,Dq[v_m]>|<=T_source_norm*C_qm and keep direct/source-extra/boundary terms explicit", "BLOCKED_PENDING_INPUTS"),
        ("ALG1552_6_project_arenas", "project to local arenas", "only after envelope closes, derive Pi_R10/Pi_PPN/Pi_clock/Pi_orbital/Pi_local with same source norm", "BLOCKED_NO_CLAIM"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "algorithm_id": algorithm_id,
            "step": step,
            "required_operation": required_operation,
            "current_status": current_status,
            "source_paths": source_list("1550_dual", "1550_envelope", "1551_reentry"),
            **flags(),
        }
        for algorithm_id, step, required_operation, current_status in rows
    ]


def failure_filter_rows() -> list[dict[str, Any]]:
    rows = [
        ("FAIL1552_0_arena_norm", "arena-selected norm", "reject if E is chosen to improve R10/PPN/clock/orbital fits", "REJECTED_SHORTCUT"),
        ("FAIL1552_1_mixed_norm", "mixed source/C_qm norms", "reject if T_source_norm and C_qm use different norms", "REJECTED_SHORTCUT"),
        ("FAIL1552_2_negative_mode", "negative/ghost direction", "reject or quotient only if negative direction is parent gauge with proof", "BLOCKER"),
        ("FAIL1552_3_zero_mode", "unquotiented zero mode", "reject if zero mode is physical and not regulated or constrained", "BLOCKER"),
        ("FAIL1552_4_boundary_drop", "silent boundary discard", "reject if integration-by-parts boundary terms are omitted without proof", "BLOCKER"),
        ("FAIL1552_5_readout_source", "readout-defined J_q", "reject if orbital GM, alpha(lambda), PPN, or clock data define source current", "REJECTED_SHORTCUT"),
        ("FAIL1552_6_long_range_hair", "unwanted exterior hair", "reject if kinetic route recreates the demoted reciprocal-hair obstruction", "BLOCKER"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "filter_id": filter_id,
            "failure_mode": failure_mode,
            "filter_rule": filter_rule,
            "current_status": current_status,
            "source_paths": source_list("1551_hunt", "1550_guard", "1549_variational"),
            **flags(),
        }
        for filter_id, failure_mode, filter_rule, current_status in rows
    ]


def reentry_runner_rows() -> list[dict[str, Any]]:
    rows = [
        ("RUN1552_0_template_written", "parent q-sector action template exists", "PASS_NONCLAIM", "action slots are written but not supplied"),
        ("RUN1552_1_q_field", "q field/dimension supplied", "REFUSED_MISSING_PARENT_FIELD", "q/q_loc field definition remains absent"),
        ("RUN1552_2_norm", "parent E norm supplied", "REFUSED_MISSING_PARENT_NORM", "kinetic/Hessian/regulator norm remains absent"),
        ("RUN1552_3_Jq", "J_q supplied", "REFUSED_MISSING_PARENT_SOURCE", "matter q-variation remains conditional"),
        ("RUN1552_4_Cqm", "Dq[v_m] in E supplied", "REFUSED_MISSING_DQVM_NORM", "C_qm is not norm-evaluated"),
        ("RUN1552_5_filters", "failure filters active", "PASS_GUARD", "arena norm, mixed norm, and readout source shortcuts rejected"),
        ("RUN1552_6_reentry_status", "local branch reentry", "REFUSED_NOT_READY", "template does not reopen claims without parent action data"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": runner_id,
            "check": check,
            "current_status": current_status,
            "reason": reason,
            "accepted_for_scoring": False,
            "passes_for_claim": False,
            **flags(),
        }
        for runner_id, check, current_status, reason in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("GATE1552_0_template", "parent q-sector extraction template", "PASS_NONCLAIM", "required action slots and extraction algorithm are explicit"),
        ("GATE1552_1_filters", "failure filters", "PASS_GUARD", "shortcut and pathology filters are active"),
        ("GATE1552_2_parent_action", "parent q-sector supplied", "BLOCKED", "template is not a supplied action"),
        ("GATE1552_3_norm", "accepted q-norm E", "BLOCKED", "no positive/coercive norm extracted"),
        ("GATE1552_4_envelope", "S_cg envelope computable", "BLOCKED", "E, J_q, Dq[v_m], and residual terms missing"),
        ("GATE1552_5_local_tests", "local arena claims", "BLOCKED_NO_CLAIM", "no local test score follows from a template"),
        ("GATE1552_6_GR_Newton", "derived GR/Newton limit", "BLOCKED_NO_CLAIM", "parent q-sector still unsupplied"),
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
        ("DEC1552_0_progress", "The parent q-sector action/norm extraction contract is written.", "ACTION_TEMPLATE_WRITTEN", "future derivation now has exact slots and failure filters"),
        ("DEC1552_1_no_claim", "The template does not reopen local claims.", "NO_PARENT_ACTION_SUPPLIED", "it is a contract, not evidence"),
        ("DEC1552_2_best_next", "Next target is a minimal parent q-sector action ansatz attempt.", "NEXT_1553_MINIMAL_QSECTOR_ACTION", "try constructing the least-assumption q-sector that supplies E without exterior hair or arena fitting"),
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
            "next_id": "NEXT1552_0_1553",
            "next_target": "1553-Y5-minimal-parent-q-sector-action-ansatz-or-rejection.md",
            "script": "scripts/Y5_minimal_parent_q_sector_action_ansatz_or_rejection.py",
            "objective": "attempt a minimal parent q-sector action ansatz that supplies a positive q-norm without exterior hair or arena-fit tuning, or reject it explicitly",
            "do_not": "do not promote ansatz to theory; do not choose coefficients by local tests; do not claim GR/Newton reduction",
            **flags(),
        }
    ]


def copy_outputs() -> None:
    copies = [
        (ACTION_TEMPLATE, QUAR_ACTION),
        (EXTRACTION_ALGORITHM, QUAR_EXTRACTION),
        (FAILURE_FILTERS, QUAR_FILTERS),
        (REENTRY_RUNNER, QUAR_RUNNER),
        (DECISION, QUAR_DECISION),
        (ACTION_TEMPLATE, BRANCH_ACTION),
        (EXTRACTION_ALGORITHM, BRANCH_EXTRACTION),
        (FAILURE_FILTERS, BRANCH_FILTERS),
        (REENTRY_RUNNER, BRANCH_RUNNER),
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
    action_rows = read_csv(ACTION_TEMPLATE)
    algorithm_rows = read_csv(EXTRACTION_ALGORITHM)
    filter_rows = read_csv(FAILURE_FILTERS)
    runner_rows = read_csv(REENTRY_RUNNER)
    gate_rows = read_csv(CLAIM_GATE)
    decision_items = read_csv(DECISION)
    next_rows = read_csv(NEXT_TARGET)

    required_slots = {
        "ACT1552_0_q_field",
        "ACT1552_1_quadratic_form",
        "ACT1552_4_matter_coupling",
        "ACT1552_5_boundary",
    }
    action_ids = {row["slot_id"] for row in action_rows}
    checks = [
        ("VAL1552_0_sources_exist", all(row["exists"] == "True" for row in sources), "all cited 1552 source paths exist"),
        ("VAL1552_1_action_template", required_slots.issubset(action_ids), "required parent q-sector action slots written"),
        ("VAL1552_2_algorithm", len(algorithm_rows) >= 7 and any(row["algorithm_id"] == "ALG1552_2_extract_E" for row in algorithm_rows), "q-norm extraction algorithm written"),
        ("VAL1552_3_failure_filters", any(row["filter_id"] == "FAIL1552_0_arena_norm" and row["current_status"] == "REJECTED_SHORTCUT" for row in filter_rows) and any(row["filter_id"] == "FAIL1552_1_mixed_norm" for row in filter_rows), "arena-fit and mixed-norm filters active"),
        ("VAL1552_4_runner_refuses_reentry", any(row["runner_id"] == "RUN1552_6_reentry_status" and row["current_status"] == "REFUSED_NOT_READY" for row in runner_rows), "reentry runner refuses local claims"),
        ("VAL1552_5_claim_gates_block", any(row["gate_id"] == "GATE1552_6_GR_Newton" and row["status"] == "BLOCKED_NO_CLAIM" for row in gate_rows), "GR/Newton claim remains blocked"),
        ("VAL1552_6_decision_next", any(row["result"] == "NEXT_1553_MINIMAL_QSECTOR_ACTION" for row in decision_items), "decision selects minimal parent q-sector action ansatz next"),
        ("VAL1552_7_next_target", any("1553-Y5-minimal-parent-q-sector" in row["next_target"] for row in next_rows), "next target is minimal parent q-sector action ansatz or rejection"),
        ("VAL1552_8_csv_parse", all(parse_csv(path) for path in generated_csvs), "all generated 1552 CSVs parse cleanly"),
        ("VAL1552_9_claim_flags_false", generated_flags_false(generated_csvs), "all generated prediction/claim flags remain false"),
        ("VAL1552_10_branch_copies", all(path.exists() for path in [QUAR_ACTION, QUAR_EXTRACTION, QUAR_FILTERS, QUAR_RUNNER, QUAR_DECISION, BRANCH_ACTION, BRANCH_EXTRACTION, BRANCH_FILTERS, BRANCH_RUNNER, BRANCH_DECISION]), "branch/quarantine nonclaim copies written"),
        ("VAL1552_11_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent after run"),
        ("VAL1552_12_formalization_untouched", formalization_modified_count_since_start() == 0, "formalization modified-file count since start=0"),
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
            "check_id": "VAL1552_13_overall",
            "result": "PASS" if overall else "FAIL",
            "detail": "1552 writes the parent q-sector action/norm extraction template, failure filters, and reentry runner while keeping local GR/Newton claims blocked"
            if overall
            else "1552 validation failed; inspect failed rows before continuing",
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
    action_rows: list[dict[str, Any]],
    algorithm_rows: list[dict[str, Any]],
    filter_rows: list[dict[str, Any]],
    runner_rows: list[dict[str, Any]],
    gate_rows: list[dict[str, Any]],
    decision_items: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 1552 - Parent q-sector Action Norm Extraction Template",
                "",
                "## Verdict",
                "- The exact parent q-sector action/norm extraction contract is now written.",
                "- This is a reentry contract, not a claim: it says what a future parent action must supply before the local GR/Newton route can reopen.",
                "- The required chain is `q field -> parent quadratic form or regulator -> positive norm E -> J_q -> C_qm in E -> S_cg envelope -> arena kernels`.",
                "- Failure filters reject arena-fit norms, mixed source/C_qm norms, ghost/zero-mode pathologies, silent boundary drops, readout-defined sources, and exterior hair reintroduction.",
                "- Next target is an actual minimal parent q-sector action ansatz attempt, with permission to reject it if it smuggles in the answer.",
                "",
                "## Source Register",
                md_table(sources, ["source_id", "source_path", "exists", "purpose"]),
                "",
                "## Parent q-sector Action Template",
                md_table(action_rows, ["slot_id", "action_slot", "template_formula", "must_supply", "current_status"]),
                "",
                "## q-norm Extraction Algorithm",
                md_table(algorithm_rows, ["algorithm_id", "step", "required_operation", "current_status"]),
                "",
                "## Failure Filters",
                md_table(filter_rows, ["filter_id", "failure_mode", "filter_rule", "current_status"]),
                "",
                "## Reentry Runner",
                md_table(runner_rows, ["runner_id", "check", "current_status", "reason"]),
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
    action_rows = action_template_rows()
    algorithm_rows = extraction_algorithm_rows()
    filter_rows = failure_filter_rows()
    runner_rows = reentry_runner_rows()
    gate_rows = claim_gate_rows()
    decision_items = decision_rows()
    next_rows = next_target_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(ACTION_TEMPLATE, action_rows)
    write_csv(EXTRACTION_ALGORITHM, algorithm_rows)
    write_csv(FAILURE_FILTERS, filter_rows)
    write_csv(REENTRY_RUNNER, runner_rows)
    write_csv(CLAIM_GATE, gate_rows)
    write_csv(DECISION, decision_items)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()
    remove_pycache()

    generated_csvs = [
        SOURCE_REGISTER,
        ACTION_TEMPLATE,
        EXTRACTION_ALGORITHM,
        FAILURE_FILTERS,
        REENTRY_RUNNER,
        CLAIM_GATE,
        DECISION,
        NEXT_TARGET,
    ]
    validation = validation_rows(generated_csvs)
    write_csv(VALIDATION, validation)
    write_doc(sources, action_rows, algorithm_rows, filter_rows, runner_rows, gate_rows, decision_items, validation, next_rows)


if __name__ == "__main__":
    main()
