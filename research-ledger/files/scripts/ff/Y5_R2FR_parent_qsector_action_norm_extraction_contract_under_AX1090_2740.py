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

DOC = ROOT / "2740-Y5-R2FR-parent-qsector-action-norm-extraction-contract-under-AX1090.md"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2740_SOURCE_REGISTER.csv",
    "slots": RESIDUALS / "P8_Y5_R2FR_2740_PARENT_QSECTOR_ACTION_SLOTS.csv",
    "algorithm": RESIDUALS / "P8_Y5_R2FR_2740_QNORM_EXTRACTION_ALGORITHM.csv",
    "filters": RESIDUALS / "P8_Y5_R2FR_2740_ACTION_FAILURE_FILTERS.csv",
    "runner": RESIDUALS / "P8_Y5_R2FR_2740_REENTRY_RUNNER_NONCLAIM.csv",
    "decisions": RESIDUALS / "P8_Y5_R2FR_2740_DECISION_LEDGER.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_2740_CLAIM_GATES.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2740_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2740_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2740_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "contract": SOURCE_WEIGHT / "qsector_action_norm_extraction_contract_2740_NONCLAIM.csv",
    "runner": LOCAL_BOUNDS / "qsector_reentry_runner_2740_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2740_MINIMAL_QSECTOR_ANSATZ_NEXT.csv",
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
            "source_id": "SRC2740_0_2739_doc",
            "description": "2739 demotes finite qnorm route and selects q-sector action contract.",
            "source_path": "2739-Y5-R2FR-parent-qnorm-Cqm-dual-pairing-closure-under-AX1090.md",
            "required_needles": "DEM2739_0_scope;RE2739_1_Eq;NEXT2739_0_2740;VAL2739_OVERALL",
        },
        {
            "source_id": "SRC2740_1_1552_doc",
            "description": "1552 parent q-sector action/norm extraction template.",
            "source_path": "1552-Y5-parent-q-sector-action-norm-extraction-template.md",
            "required_needles": "ACT1552_0_q_field;ALG1552_2_extract_E;FAIL1552_0_arena_norm;NEXT1552_0_1553",
        },
        {
            "source_id": "SRC2740_2_1551_doc",
            "description": "1551 closure demotion and reentry conditions.",
            "source_path": "1551-Y5-parent-qnorm-source-or-local-closure-demotion.md",
            "required_needles": "DEM1551_0_scope;RE1551_1_norm;HUNT1551_5_current_verdict",
        },
        {
            "source_id": "SRC2740_3_1550_doc",
            "description": "1550 same-norm theorem and failure policy.",
            "source_path": "1550-Y5-qnorm-Cqm-dual-pairing-and-envelope-closure.md",
            "required_needles": "DUAL1550_3_holder_bound;NMN1550_0_single_E;ENV1550_0_sgeom_units",
        },
        {
            "source_id": "SRC2740_4_1549_doc",
            "description": "1549 variational source-current law and readout rejection.",
            "source_path": "1549-Y5-Jq-unit-dimension-and-parent-source-variation-closure.md",
            "required_needles": "VAR1549_0_variational_definition;VAR1549_4_no_readout_definition;UNIT1549_5_product_law",
        },
        {
            "source_id": "SRC2740_5_1552_action_csv",
            "description": "machine-readable q-sector action slots.",
            "source_path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1552_PARENT_QSECTOR_ACTION_TEMPLATE.csv",
            "required_needles": "ACT1552_0_q_field;ACT1552_4_matter_coupling;ACT1552_6_parent_action_verdict",
        },
        {
            "source_id": "SRC2740_6_1552_algorithm_csv",
            "description": "machine-readable extraction algorithm.",
            "source_path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1552_QNORM_EXTRACTION_ALGORITHM.csv",
            "required_needles": "ALG1552_0_define_q;ALG1552_4_compute_Cqm;ALG1552_6_project_arenas",
        },
        {
            "source_id": "SRC2740_7_1552_filters_csv",
            "description": "machine-readable failure filters.",
            "source_path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1552_ACTION_FAILURE_FILTERS.csv",
            "required_needles": "FAIL1552_0_arena_norm;FAIL1552_4_boundary_drop;FAIL1552_6_long_range_hair",
        },
        {
            "source_id": "SRC2740_8_2738_core",
            "description": "live first-pair template needing parent qnorm.",
            "source_path": "source-intake/mts_residuals/P8_Y5_R2FR_2738_WORLDTUBE_FIRST_PAIR_CORE_TEMPLATE.csv",
            "required_needles": "CORE2738_2_qnorm;CORE2738_3_Tsource;CORE2738_6_QmH",
        },
        {
            "source_id": "SRC2740_9_2739_reentry",
            "description": "live qnorm reentry conditions from 2739.",
            "source_path": "source-intake/mts_residuals/P8_Y5_R2FR_2739_QNORM_REENTRY_CONDITIONS.csv",
            "required_needles": "RE2739_0_q_field;RE2739_1_Eq;RE2739_8_claim_policy",
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


def slot_rows() -> list[dict[str, Any]]:
    specs = [
        ("QS2740_0_q_field", "q field / q_loc map", "q^A or q^A(Phi) with dim(q^A), observed-frame descent, and quotient/gauge status", "field identity; parent map; dimension; variation class; domain", "REQUIRED_NOT_SUPPLIED"),
        ("QS2740_1_positive_quadratic_form", "positive quadratic form", "delta^2 S_q = 1/2 int_W delta q^A G_AB delta q^B dV_e + boundary", "G_AB/Hessian/operator; positivity/coercivity; units; null/gauge quotient", "REQUIRED_NOT_SUPPLIED"),
        ("QS2740_2_derivative_operator", "kinetic/operator route", "1/2 int_W Z_AB^{mu nu} nabla_mu q^A nabla_nu q^B dV_e", "elliptic/static branch; no ghost/tachyon; boundary conditions; no exterior hair", "OPTIONAL_ROUTE_WITH_FILTERS"),
        ("QS2740_3_regulator", "worldtube regulator/excision", "E_epsilon[delta q;W_src] with epsilon_reg, support, matching surface, and finite limit", "regulator law; compact support; boundary flux; limiting procedure", "OPTIONAL_ROUTE_WITH_FILTERS"),
        ("QS2740_4_matter_coupling", "matter q-source", "delta S_matter = int_W J_A delta q^A dV_e + boundary", "explicit S_matter[q] or coupling projector; hidden channel audit", "REQUIRED_NOT_SUPPLIED"),
        ("QS2740_5_Cqm", "C_qm in E_q", "C_qm=||Dq[v_m]||_E with same E_q used by T_source_norm", "Dq[v_m]; v_m action; no norm switch; units", "REQUIRED_NOT_SUPPLIED"),
        ("QS2740_6_boundary", "boundary/domain terms", "integration-by-parts and worldtube boundary terms retained as zero theorem or finite S_boundary_m/N_inner rows", "boundary sign; trace norm; zero-mode; domain motion", "REQUIRED_NOT_SUPPLIED"),
        ("QS2740_7_arena_kernels", "arena projection kernels", "Pi_R10/Pi_PPN/Pi_clock/Pi_orbital/Pi_local after E_q and N_pair close", "same profile/norm maps to observables without retuning", "DOWNSTREAM_REQUIRED_NOT_SUPPLIED"),
        ("QS2740_8_verdict", "accepted parent q-sector", "all previous slots close with failure filters passed", "complete parent q-sector data", "NOT_SUPPLIED_CURRENTLY"),
    ]
    return [
        nonclaim(
            {
                "same_parent_branch_id": BRANCH_ID,
                "slot_id": slot_id,
                "action_slot": slot,
                "template_formula": formula,
                "must_supply": must,
                "current_status": status,
                "reopens": "finite local qnorm route; N_pair/Nlock source-profile branch; local GR/Newton derivation only after all slots pass",
                "source_paths": "1552-Y5-parent-q-sector-action-norm-extraction-template.md; 2739-Y5-R2FR-parent-qnorm-Cqm-dual-pairing-closure-under-AX1090.md",
            }
        )
        for slot_id, slot, formula, must, status in specs
    ]


def algorithm_rows() -> list[dict[str, Any]]:
    steps = [
        ("ALG2740_0_define_q", "define q", "identify q^A, dim(q^A), allowed delta q, gauge/quotient class, W_src", "BLOCKED_PENDING_PARENT_ACTION"),
        ("ALG2740_1_variation_domain", "fix variation domain", "declare compact support, boundary behavior, regularity, zero modes, quotient nulls", "BLOCKED_PENDING_DOMAIN"),
        ("ALG2740_2_second_variation", "take second variation", "compute delta^2 S_parent restricted to local q-sector including boundary terms", "BLOCKED_PENDING_PARENT_ACTION"),
        ("ALG2740_3_extract_E", "extract E_q", "accept norm only if positive/coercive after gauge/null quotient and regulator limit", "BLOCKED_PENDING_POSITIVITY"),
        ("ALG2740_4_extract_Jq", "derive J_q", "compute delta S_matter/delta q in same observed frame and variation domain", "BLOCKED_PENDING_PARENT_COUPLING"),
        ("ALG2740_5_compute_Cqm", "compute C_qm", "evaluate Dq[v_m] in E_q with no arena or mixed-norm substitution", "BLOCKED_PENDING_DQVM"),
        ("ALG2740_6_insert_envelope", "insert S_cg", "use same-norm dual pairing and keep direct/source-extra/boundary terms explicit", "BLOCKED_PENDING_INPUTS"),
        ("ALG2740_7_project_arenas", "project arenas", "derive Pi_arena only after source envelope and N_pair are legal", "BLOCKED_NO_CLAIM"),
    ]
    return [
        nonclaim(
            {
                "same_parent_branch_id": BRANCH_ID,
                "algorithm_id": algorithm_id,
                "step": step,
                "required_operation": operation,
                "current_status": status,
                "source_paths": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1552_QNORM_EXTRACTION_ALGORITHM.csv; 2739-Y5-R2FR-parent-qnorm-Cqm-dual-pairing-closure-under-AX1090.md",
            }
        )
        for algorithm_id, step, operation, status in steps
    ]


def filter_rows() -> list[dict[str, Any]]:
    filters = [
        ("FAIL2740_0_arena_norm", "arena-selected norm", "reject if E_q is chosen to improve R10/PPN/clock/orbital fits", "REJECTED_SHORTCUT"),
        ("FAIL2740_1_mixed_norm", "mixed source/Cqm norms", "reject if T_source_norm and C_qm use different norms", "REJECTED_SHORTCUT"),
        ("FAIL2740_2_negative_mode", "negative/ghost direction", "reject or quotient only if negative direction is parent gauge with proof", "BLOCKER"),
        ("FAIL2740_3_zero_mode", "unquotiented zero mode", "reject if zero mode is physical and not regulated or constrained", "BLOCKER"),
        ("FAIL2740_4_boundary_drop", "silent boundary discard", "reject if boundary terms are omitted without theorem-zero or finite residual row", "BLOCKER"),
        ("FAIL2740_5_readout_source", "readout-defined J_q", "reject if orbital GM, alpha(lambda), PPN, or clock data define source current", "REJECTED_SHORTCUT"),
        ("FAIL2740_6_long_range_hair", "unwanted exterior hair", "reject if q kinetic route recreates reciprocal/exterior hair obstruction", "BLOCKER"),
        ("FAIL2740_7_retuned_profile", "per-arena profile retuning", "reject if W_src/theta_src differs between arenas except through declared Pi_arena projection", "REJECTED_SHORTCUT"),
    ]
    return [
        nonclaim(
            {
                "same_parent_branch_id": BRANCH_ID,
                "filter_id": filter_id,
                "failure_mode": failure,
                "filter_rule": rule,
                "current_status": status,
                "source_paths": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1552_ACTION_FAILURE_FILTERS.csv; source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1547_NO_RETUNING_GUARD.csv",
            }
        )
        for filter_id, failure, rule, status in filters
    ]


def runner_rows() -> list[dict[str, Any]]:
    checks = [
        ("RUN2740_0_contract_written", "parent q-sector contract exists", "PASS_NONCLAIM", "slots and algorithm are explicit"),
        ("RUN2740_1_q_field", "q field/dimension supplied", "REFUSED_MISSING_PARENT_FIELD", "contract is not supplied parent action"),
        ("RUN2740_2_Eq", "positive E_q extracted", "REFUSED_MISSING_PARENT_NORM", "no G_AB/Hessian/regulator supplied"),
        ("RUN2740_3_Jq", "J_q supplied", "REFUSED_MISSING_PARENT_SOURCE", "matter q-variation remains conditional"),
        ("RUN2740_4_Cqm", "Dq[v_m] in E_q supplied", "REFUSED_MISSING_DQVM_NORM", "C_qm is not norm-evaluated"),
        ("RUN2740_5_filters", "failure filters active", "PASS_GUARD", "arena norm, mixed norm, readout source, boundary drop, hair filters active"),
        ("RUN2740_6_reentry", "local branch reentry", "REFUSED_NOT_READY", "template alone does not reopen local claims"),
    ]
    return [
        nonclaim(
            {
                "same_parent_branch_id": BRANCH_ID,
                "runner_id": runner_id,
                "check": check,
                "current_status": status,
                "reason": reason,
                "accepted_for_scoring": False,
                "passes_for_claim": False,
            }
        )
        for runner_id, check, status, reason in checks
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        ("DEC2740_0_contract", "Write the parent q-sector action/norm extraction contract.", "2739 demoted the route until this exact parent action data exists", "reentry requirements are concrete rather than vague"),
        ("DEC2740_1_no_reentry", "Do not reopen local claims from a contract.", "no parent action data is supplied here", "local GR/Newton remains blocked"),
        ("DEC2740_2_filters", "Keep strong failure filters active.", "a minimal action must not smuggle in arena fitting, mixed norms, boundary deletion, or exterior hair", "future ansatz can be rejected quickly"),
        ("DEC2740_3_next", "Attempt a minimal q-sector action ansatz next.", "the contract is now explicit enough to test an ansatz", "2741 should try the least-assumption action or reject it"),
    ]
    return [nonclaim({"decision_id": decision_id, "decision": decision, "because": because, "effect": effect}) for decision_id, decision, because, effect in rows]


def gate_rows() -> list[dict[str, Any]]:
    gates = [
        ("GATE2740_0_contract", "parent q-sector contract", True, "PASS_NONCLAIM", "action slots and algorithm written"),
        ("GATE2740_1_filters", "failure filters", True, "PASS_GUARD", "shortcut/pathology filters active"),
        ("GATE2740_2_parent_action", "parent q-sector supplied", False, "BLOCKED", "contract does not supply action data"),
        ("GATE2740_3_Eq", "accepted q-norm E_q", False, "BLOCKED", "no positive/coercive norm extracted"),
        ("GATE2740_4_envelope", "S_cg/N_pair computable", False, "BLOCKED", "E_q/J_q/Dq[v_m]/residual terms missing"),
        ("GATE2740_5_local_tests", "R10/PPN/clock/orbital pass", False, "BLOCKED_NO_CLAIM", "no legal local projection score"),
        ("GATE2740_6_GR_Newton", "derived GR/Newton limit", False, "BLOCKED_NO_CLAIM", "parent q-sector still unsupplied"),
    ]
    return [
        nonclaim(
            {
                "claim_gate_id": gate_id,
                "claim": claim,
                "gate_passed": passed,
                "status": status,
                "claim_allowed": False,
                "reason": reason,
            }
        )
        for gate_id, claim, passed, status, reason in gates
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        nonclaim(
            {
                "next_id": "NEXT2740_0_2741",
                "status": "selected_primary",
                "target_doc": "2741-Y5-R2FR-minimal-parent-qsector-action-ansatz-or-rejection-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_minimal_parent_qsector_action_ansatz_or_rejection_under_AX1090_2741.py",
                "mission": "attempt a minimal parent q-sector action ansatz that supplies positive E_q without exterior hair or arena-fit tuning, or reject it explicitly against the 2740 failure filters",
                "acceptance": "ansatz either supplies q field, positive norm, J_q, C_qm route, boundary treatment, and no-hair/no-retuning checks as nonclaim theorem candidate; or is rejected with exact failure row",
                "forbidden": "do not promote ansatz to theory; do not choose coefficients by local tests; do not claim GR/Newton reduction",
                "selected": True,
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({"copy_id": "BR2740_0_contract", "source_table": rel(OUTPUTS["slots"]), "copy_path": rel(BRANCH_OUTPUTS["contract"]), "purpose": "source-weight q-sector action/norm extraction contract", "exists": BRANCH_OUTPUTS["contract"].exists()}),
        nonclaim({"copy_id": "BR2740_1_runner", "source_table": rel(OUTPUTS["runner"]), "copy_path": rel(BRANCH_OUTPUTS["runner"]), "purpose": "local-bound nonclaim q-sector reentry runner", "exists": BRANCH_OUTPUTS["runner"].exists()}),
        nonclaim({"copy_id": "BR2740_2_next_queue", "source_table": rel(OUTPUTS["next"]), "copy_path": rel(BRANCH_OUTPUTS["next_queue"]), "purpose": "RAB acquisition queue for minimal q-sector ansatz attempt", "exists": BRANCH_OUTPUTS["next_queue"].exists()}),
    ]


def formalization_recent_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    start = SCRIPT_START_UTC.timestamp()
    return sum(1 for path in FORMALIZATION.rglob("*") if path.is_file() and path.stat().st_mtime >= start)


def validation_rows(
    sources: list[dict[str, Any]],
    slots: list[dict[str, Any]],
    algorithm: list[dict[str, Any]],
    filters: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    source_ok = all(row["exists"] is True and row["needles_present"] is True for row in sources)
    slots_ok = len(slots) == 9 and any(row["slot_id"] == "QS2740_1_positive_quadratic_form" for row in slots)
    algorithm_ok = len(algorithm) == 8 and any(row["algorithm_id"] == "ALG2740_3_extract_E" for row in algorithm)
    filters_ok = len(filters) == 8 and any(row["filter_id"] == "FAIL2740_6_long_range_hair" for row in filters)
    runner_ok = any(row["current_status"] == "PASS_NONCLAIM" for row in runner) and any(row["current_status"] == "REFUSED_NOT_READY" for row in runner)
    gates_ok = any(row["claim_gate_id"] == "GATE2740_0_contract" and row["gate_passed"] is True for row in gates) and all(row["claim_allowed"] is False for row in gates)
    next_ok = next_target[0]["selected"] is True and "minimal-parent-qsector" in next_target[0]["target_doc"]
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
        {"validation_id": "VAL2740_0_sources", "passed": source_ok, "detail": "all source paths exist and required anchors/needles are present", "timestamp_utc": ts()},
        {"validation_id": "VAL2740_1_action_slots", "passed": slots_ok, "detail": "parent q-sector action slots are complete", "timestamp_utc": ts()},
        {"validation_id": "VAL2740_2_algorithm", "passed": algorithm_ok, "detail": "q-norm extraction algorithm is complete", "timestamp_utc": ts()},
        {"validation_id": "VAL2740_3_filters", "passed": filters_ok, "detail": "failure filters include exterior hair and shortcut guards", "timestamp_utc": ts()},
        {"validation_id": "VAL2740_4_runner_refuses_reentry", "passed": runner_ok, "detail": "runner records contract progress but refuses local reentry", "timestamp_utc": ts()},
        {"validation_id": "VAL2740_5_claim_gates", "passed": gates_ok, "detail": "only contract/guard gates pass; local claims remain blocked", "timestamp_utc": ts()},
        {"validation_id": "VAL2740_6_next_target", "passed": next_ok, "detail": "next target is minimal parent q-sector action ansatz or rejection", "timestamp_utc": ts()},
        {"validation_id": "VAL2740_7_branch_outputs", "passed": branch_ok, "detail": "branch copies exist", "timestamp_utc": ts()},
        {"validation_id": "VAL2740_8_csv_parse", "passed": csv_ok, "detail": "; ".join(csv_bits), "timestamp_utc": ts()},
        {"validation_id": "VAL2740_9_formalization_untouched", "passed": formalization_ok, "detail": f"formalization-workbench recent modified-file count since script start = {formalization_recent_count()}", "timestamp_utc": ts()},
    ]
    rows.append(
        {
            "validation_id": "VAL2740_OVERALL",
            "passed": all(row["passed"] is True for row in rows),
            "detail": "2740 writes the parent q-sector action/norm extraction contract, failure filters, reentry runner, and selects minimal q-sector ansatz/rejection next",
            "timestamp_utc": ts(),
        }
    )
    return rows


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    DOC.write_text(
        f"""# 2740 - Y5 R2/f(R): Parent q-sector Action/Norm Extraction Contract Under AX1090

Status: `Y5_R2FR_2740_parent_qsector_reentry_contract_written_no_claim_reopened`

## Private Verdict

2740 turns the 2739 closure into a reentry contract.

To reopen the local GR/Newton derivation route, a parent q-sector must supply:

`q field -> positive quadratic form/regulator -> parent norm E_q -> J_q -> C_qm in E_q -> boundary accounting -> S_cg/N_pair -> arena kernels`.

This checkpoint supplies the exact slots and failure filters. It does **not** supply the parent action itself, so no local claim reopens.

The next honest move is a minimal parent q-sector ansatz attempt. If it smuggles in arena fitting, mixed norms, silent boundary drops, ghosts, zero modes, or exterior hair, it gets rejected.

## Source Register

{markdown_table(data["sources"], ["source_id", "description", "source_path", "exists", "needles_present", "missing_needles", "valid_for_claim"])}

## Parent q-sector Action Slots

{markdown_table(data["slots"], ["slot_id", "action_slot", "template_formula", "must_supply", "current_status", "reopens", "valid_for_claim"])}

## qnorm Extraction Algorithm

{markdown_table(data["algorithm"], ["algorithm_id", "step", "required_operation", "current_status", "valid_for_claim"])}

## Action Failure Filters

{markdown_table(data["filters"], ["filter_id", "failure_mode", "filter_rule", "current_status", "valid_for_claim"])}

## Reentry Runner

{markdown_table(data["runner"], ["runner_id", "check", "current_status", "reason", "accepted_for_scoring", "passes_for_claim", "valid_for_claim"])}

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

This is the clean doorway back into derivation. The local branch is still not proven, but now it has an engineering spec: build a minimal q-sector that passes these filters, or bin it. No vibes, no patchwork quilt.
""",
        encoding="utf-8",
    )


def main() -> None:
    ensure_dirs()
    sources = source_rows()
    slots = slot_rows()
    algorithm = algorithm_rows()
    filters = filter_rows()
    runner = runner_rows()
    decisions = decision_rows()
    gates = gate_rows()
    next_target = next_rows()

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["slots"], slots)
    write_csv(OUTPUTS["algorithm"], algorithm)
    write_csv(OUTPUTS["filters"], filters)
    write_csv(OUTPUTS["runner"], runner)
    write_csv(OUTPUTS["decisions"], decisions)
    write_csv(OUTPUTS["gates"], gates)
    write_csv(OUTPUTS["next"], next_target)

    write_csv(BRANCH_OUTPUTS["contract"], slots)
    write_csv(BRANCH_OUTPUTS["runner"], runner)
    write_csv(BRANCH_OUTPUTS["next_queue"], next_target)
    branches = branch_rows()
    write_csv(OUTPUTS["branches"], branches)

    validation = validation_rows(sources, slots, algorithm, filters, runner, gates, next_target)
    write_csv(OUTPUTS["validation"], validation)

    data = {
        "sources": sources,
        "slots": slots,
        "algorithm": algorithm,
        "filters": filters,
        "runner": runner,
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
        raise SystemExit(f"2740 validation failed: {failed}")
    print(f"wrote {DOC}")
    print(f"validation {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
