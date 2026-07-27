from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
CHECKPOINT_ID = "1876"

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / CHECKPOINT_ID
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1876-Y5-R2FR-RAB-residual-vector-blocking-runner-dryrun.md"

INPUTS = {
    "1875_doc": ROOT / "1875-Y5-R2FR-RAB-residual-operator-source-vector-and-test-routing.md",
    "1875_validation": OUT / "P8_Y5_BRR545_1875_VALIDATION.csv",
    "1875_vector": OUT / "P8_Y5_PARENT_QLOC_1875_RAB_RESIDUAL_OPERATOR_SOURCE_VECTOR.csv",
    "1875_routing": OUT / "P8_Y5_PARENT_QLOC_1875_RAB_TEST_ROUTING_MATRIX.csv",
    "1875_contract": OUT / "P8_Y5_PARENT_QLOC_1875_RAB_RUNNER_BLOCKER_CONTRACT.csv",
    "1875_claim_gate": OUT / "P8_Y5_PARENT_QLOC_1875_CLAIM_GATE.csv",
    "1875_next_target": OUT / "P8_Y5_PARENT_QLOC_1875_NEXT_TARGET.csv",
}

SOURCE_NEEDLES = {
    "1875_doc": [
        "RAB_RESIDUAL_VECTOR_READY_NONCLAIM",
        "BLOCKING_RUNNER_DRYRUN_SELECTED_NEXT",
    ],
    "1875_validation": [
        "VAL1875_OVERALL,PASS",
    ],
    "1875_vector": [
        "RV1875_5_massless_tail",
        "RESIDUAL_VECTOR_READY_NONCLAIM_ALL_SCORES_BLOCKED",
    ],
    "1875_routing": [
        "massless C_R/r tail routed into alpha(lambda)",
        "BLOCKED_NONCLAIM_MASSLESS_ROUTE_FORBIDDEN",
    ],
    "1875_contract": [
        "WRONG_ARENA_ROUTE_BLOCKS_SCORE",
        "NO_CANCELLATION_GUARD_BLOCKS_CLAIM",
    ],
    "1875_claim_gate": [
        "CG1875_1_local_GR",
        "BLOCKED",
    ],
    "1875_next_target": [
        "scripts/Y5_R2FR_RAB_residual_vector_blocking_runner_dryrun_1876.py",
        "selected",
    ],
}

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_1876_SOURCE_REGISTER.csv",
    "input_audit": OUT / "P8_Y5_PARENT_QLOC_1876_RUNNER_INPUT_AUDIT.csv",
    "arena_dryrun": OUT / "P8_Y5_PARENT_QLOC_1876_ARENA_BLOCKING_DRYRUN.csv",
    "forbidden_route_tests": OUT / "P8_Y5_PARENT_QLOC_1876_FORBIDDEN_ROUTE_TESTS.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_1876_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_1876_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_1876_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_1876_VALIDATION.csv",
}


def ensure_dirs() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    MICROSCOPE_RESIDUALS.mkdir(parents=True, exist_ok=True)
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)


def bool_string(value: Any) -> str:
    return str(value).strip().lower()


def path_has_needles(path: Path, needles: list[str]) -> tuple[bool, str]:
    if not path.exists():
        return False, "MISSING_SOURCE_PATH"
    text = path.read_text(encoding="utf-8", errors="ignore")
    missing = [needle for needle in needles if needle not in text]
    if missing:
        return False, "MISSING_NEEDLES=" + ";".join(missing)
    return True, "OK"


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path in INPUTS.items():
        ok, detail = path_has_needles(path, SOURCE_NEEDLES[source_id])
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "checkpoint_id": CHECKPOINT_ID,
                "source_id": source_id,
                "source_path": str(path),
                "required_needles": " ; ".join(SOURCE_NEEDLES[source_id]),
                "source_exists": path.exists(),
                "needle_check": detail,
                "usable_for_1876": ok,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def keyed(rows: list[dict[str, str]], key: str) -> dict[str, dict[str, str]]:
    return {row[key]: row for row in rows}


def input_audit_rows() -> list[dict[str, Any]]:
    vector_rows = csv_rows(INPUTS["1875_vector"])
    routing_rows = csv_rows(INPUTS["1875_routing"])
    contract_rows = csv_rows(INPUTS["1875_contract"])
    rows: list[dict[str, Any]] = []
    for row in vector_rows:
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "checkpoint_id": CHECKPOINT_ID,
                "input_table": "1875_residual_vector",
                "input_id": row["vector_id"],
                "input_status": row["current_status"],
                "route_or_sector": row["sector"],
                "score_ready": row.get("score_ready", False),
                "valid_prediction_row": row.get("valid_prediction_row", False),
                "valid_for_claim": False,
                "claim_allowed": False,
                "runner_interpretation": "missing_or_nonclaim_input_blocks_score",
            }
        )
    for row in routing_rows:
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "checkpoint_id": CHECKPOINT_ID,
                "input_table": "1875_test_routing",
                "input_id": row["route_id"],
                "input_status": row["current_status"],
                "route_or_sector": row["arena"],
                "score_ready": False,
                "valid_prediction_row": False,
                "valid_for_claim": False,
                "claim_allowed": False,
                "runner_interpretation": "route_is_contract_only_until_inputs_are_signed",
            }
        )
    for row in contract_rows:
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "checkpoint_id": CHECKPOINT_ID,
                "input_table": "1875_runner_contract",
                "input_id": row["contract_id"],
                "input_status": row["failure_mode"],
                "route_or_sector": "runner_safety_contract",
                "score_ready": False,
                "valid_prediction_row": False,
                "valid_for_claim": False,
                "claim_allowed": False,
                "runner_interpretation": "failed_contract_forces_claim_allowed_false",
            }
        )
    return rows


ARENA_SPECS = [
    {
        "arena_id": "AR1876_0_local_GR",
        "arena": "local_GR/Newton_limit",
        "source_route": "TR1875_0_local_GR",
        "route_type": "theorem_zero_or_all_components_bounded",
        "allowed_input": "parent-signed constraint/no-pole or every local residual component theorem-zero/source-bounded absolutely",
        "required_vector_rows": [
            "RV1875_0_domain_visibility",
            "RV1875_1_constraint_owner",
            "RV1875_5_massless_tail",
            "RV1875_6_boundary_readout_tail",
            "RV1875_9_no_cancellation",
        ],
        "forbidden_vector_rows": [],
        "block_reason": "local GR cannot be claimed while verticality/constraint, massless tail, boundary silence, and no-cancellation are unsigned",
    },
    {
        "arena_id": "AR1876_1_PPN_light_time",
        "arena": "PPN/light-time",
        "source_route": "TR1875_1_PPN_orbital_massless",
        "route_type": "massless_tail_only",
        "allowed_input": "C_R/Pi_R/kappa_W/M_* row, tau_PPN/light-time projection, and no-cancellation guard",
        "required_vector_rows": [
            "RV1875_5_massless_tail",
            "RV1875_6_boundary_readout_tail",
            "RV1875_8_projection_kernels",
            "RV1875_9_no_cancellation",
        ],
        "forbidden_vector_rows": [
            "RV1875_2_operator_ZR",
            "RV1875_3_operator_MR2_lambda",
        ],
        "block_reason": "Cassini/light-time score has no signed C_R/Pi_R/kappa/Mstar row or projection/no-cancellation closure",
    },
    {
        "arena_id": "AR1876_2_R10_finite_range",
        "arena": "R10 alpha(lambda)",
        "source_route": "TR1875_2_R10_finite_range",
        "route_type": "finite_operator_only",
        "allowed_input": "Z_R, M_R^2, lambda_range, beta_source_R, beta_test_R, tau_R10, and accepted bound curve",
        "required_vector_rows": [
            "RV1875_2_operator_ZR",
            "RV1875_3_operator_MR2_lambda",
            "RV1875_4_bulk_source_charges",
            "RV1875_8_projection_kernels",
            "RV1875_9_no_cancellation",
        ],
        "forbidden_vector_rows": [
            "RV1875_5_massless_tail",
        ],
        "block_reason": "R10 finite-range score has no same-normalized operator/source/projection rows, and massless C_R/r is forbidden in alpha(lambda)",
    },
    {
        "arena_id": "AR1876_3_clock",
        "arena": "clock/material",
        "source_route": "TR1875_3_clock_WEP",
        "route_type": "material_marker_projection",
        "allowed_input": "material constants/markers, beta charges, tau_clock, and source-backed clock bounds",
        "required_vector_rows": [
            "RV1875_4_bulk_source_charges",
            "RV1875_7_constants_markers",
            "RV1875_8_projection_kernels",
            "RV1875_9_no_cancellation",
        ],
        "forbidden_vector_rows": [],
        "block_reason": "clock score has no matter-blindness theorem, material coefficient table, tau_clock, or no-cancellation guard",
    },
    {
        "arena_id": "AR1876_4_WEP",
        "arena": "WEP/material",
        "source_route": "TR1875_3_clock_WEP",
        "route_type": "material_marker_projection",
        "allowed_input": "source/test material charges, tau_WEP, and accepted WEP bound interface",
        "required_vector_rows": [
            "RV1875_4_bulk_source_charges",
            "RV1875_7_constants_markers",
            "RV1875_8_projection_kernels",
            "RV1875_9_no_cancellation",
        ],
        "forbidden_vector_rows": [],
        "block_reason": "WEP score has no signed source/test charge resolution, no marker silence theorem, tau_WEP, or no-cancellation guard",
    },
    {
        "arena_id": "AR1876_5_orbital_massless",
        "arena": "orbital_massless_tail",
        "source_route": "TR1875_1_PPN_orbital_massless",
        "route_type": "massless_tail_only",
        "allowed_input": "C_R/Pi_R/kappa_W/M_* row, tau_orbital, and no-cancellation guard",
        "required_vector_rows": [
            "RV1875_5_massless_tail",
            "RV1875_6_boundary_readout_tail",
            "RV1875_8_projection_kernels",
            "RV1875_9_no_cancellation",
        ],
        "forbidden_vector_rows": [
            "RV1875_2_operator_ZR",
            "RV1875_3_operator_MR2_lambda",
        ],
        "block_reason": "orbital massless-tail score lacks C_R/Pi_R/kappa/Mstar, boundary/readout silence, tau_orbital, and no-cancellation",
    },
    {
        "arena_id": "AR1876_6_orbital_finite",
        "arena": "orbital_finite_range",
        "source_route": "TR1875_2_R10_finite_range",
        "route_type": "finite_operator_range",
        "allowed_input": "Z_R, M_R^2, lambda_range, source charges, tau_orbital, and orbital baseline",
        "required_vector_rows": [
            "RV1875_2_operator_ZR",
            "RV1875_3_operator_MR2_lambda",
            "RV1875_4_bulk_source_charges",
            "RV1875_8_projection_kernels",
            "RV1875_9_no_cancellation",
        ],
        "forbidden_vector_rows": [],
        "block_reason": "orbital finite-range score lacks operator/range/source/projection rows and no-cancellation",
    },
]


def missing_vector_details(required_ids: list[str], vector_by_id: dict[str, dict[str, str]]) -> tuple[str, str]:
    missing_ids: list[str] = []
    details: list[str] = []
    for vector_id in required_ids:
        row = vector_by_id.get(vector_id)
        if row is None:
            missing_ids.append(vector_id)
            details.append(f"{vector_id}=MISSING_VECTOR_ROW")
            continue
        current_status = row.get("current_status", "")
        score_ready = bool_string(row.get("score_ready", "false")) == "true"
        valid_prediction = bool_string(row.get("valid_prediction_row", "false")) == "true"
        if "MISSING" in current_status or not score_ready or not valid_prediction:
            missing_ids.append(vector_id)
            details.append(f"{vector_id}={current_status}")
    return ";".join(missing_ids), " ; ".join(details)


def arena_dryrun_rows() -> list[dict[str, Any]]:
    vector_by_id = keyed(csv_rows(INPUTS["1875_vector"]), "vector_id")
    rows: list[dict[str, Any]] = []
    for spec in ARENA_SPECS:
        required_ids = spec["required_vector_rows"]
        missing_ids, missing_statuses = missing_vector_details(required_ids, vector_by_id)
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "checkpoint_id": CHECKPOINT_ID,
                "arena_id": spec["arena_id"],
                "arena": spec["arena"],
                "source_route": spec["source_route"],
                "route_type": spec["route_type"],
                "allowed_input": spec["allowed_input"],
                "required_vector_rows": ";".join(required_ids),
                "forbidden_vector_rows": ";".join(spec["forbidden_vector_rows"]),
                "missing_vector_rows": missing_ids,
                "missing_statuses": missing_statuses,
                "runner_status": "BLOCKED_NONCLAIM",
                "block_reason": spec["block_reason"],
                "score_attempted": False,
                "score_ready": False,
                "valid_prediction_row": False,
                "valid_for_claim": False,
                "claim_allowed": False,
                "public_claim_allowed": False,
            }
        )
    return rows


def forbidden_route_test_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "test_id": "FRT1876_0_R10_massless_injection",
            "arena": "R10 alpha(lambda)",
            "attempted_input": "RV1875_5_massless_tail as C_R/r alpha(lambda) source",
            "expected_contract": "RBC1875_1_route_separation",
            "runner_status": "WRONG_ARENA_ROUTE_BLOCKS_SCORE",
            "reason": "massless C_R/r is PPN/orbital/light-time only; finite R10 requires Z_R/M_R^2/lambda_range",
            "score_attempted": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "test_id": "FRT1876_1_local_GR_closure_only",
            "arena": "local_GR/Newton_limit",
            "attempted_input": "closure-only R_AB=0 benchmark without parent theorem",
            "expected_contract": "RBC1875_0_input_validity",
            "runner_status": "CLOSURE_ONLY_BLOCKS_CLAIM",
            "reason": "closure benchmark is not a derivation of local GR unless q_shape, constraint/no-pole, or all residuals are parent-signed",
            "score_attempted": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "test_id": "FRT1876_2_cancellation_credit",
            "arena": "all_local_arenas",
            "attempted_input": "operator/source/tail residuals cancel numerically without parent identity",
            "expected_contract": "RBC1875_3_no_cancellation",
            "runner_status": "NO_CANCELLATION_GUARD_BLOCKS_CLAIM",
            "reason": "every component must be independently zero or source-bounded unless a parent identity proves cancellation",
            "score_attempted": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "test_id": "FRT1876_3_normalization_mismatch",
            "arena": "R10/clock/orbital",
            "attempted_input": "Z_R, M_R^2, beta charges, C_R/Pi_R, kappa_W, or M_* from mixed frames",
            "expected_contract": "RBC1875_2_same_normalization",
            "runner_status": "NORMALIZATION_MISMATCH_BLOCKS_SCORE",
            "reason": "all retained coefficients must share a declared parent/source frame before comparison",
            "score_attempted": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "test_id": "FRT1876_4_baseline_missing",
            "arena": "empirical_local_arena",
            "attempted_input": "raw MTS residual score without same-pipeline GR/PPN baseline",
            "expected_contract": "RBC1875_4_baseline_comparison",
            "runner_status": "BASELINE_MISSING_BLOCKS_PUBLIC_EVIDENCE",
            "reason": "a future empirical score must compare against the appropriate baseline under the same projection assumptions",
            "score_attempted": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "gate_id": "CG1876_0_internal_runner",
            "claim": "1876 blocking runner dry-run may be used as an internal safety harness",
            "status": "ALLOW_INTERNAL_NONCLAIM_RUNNER",
            "reason": "it consumes the 1875 vector and emits only blocked/nonclaim statuses",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "gate_id": "CG1876_1_local_GR",
            "claim": "derived local GR/Newton limit from current R_AB branch",
            "status": "BLOCKED",
            "reason": "q_shape/verticality or lambda_R/no-pole parent owner is unsigned",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "gate_id": "CG1876_2_R10",
            "claim": "R10 alpha(lambda) pass",
            "status": "BLOCKED",
            "reason": "Z_R, M_R^2, lambda_range, source/test charges, tau_R10, accepted bounds, and no-cancellation are missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "gate_id": "CG1876_3_PPN_clock_WEP_orbital",
            "claim": "PPN, clock, WEP, or orbital pass",
            "status": "BLOCKED",
            "reason": "massless/source/material/projection/no-cancellation rows remain nonclaim or missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "gate_id": "CG1876_4_public_evidence",
            "claim": "public local-arena evidence from this branch",
            "status": "BLOCKED",
            "reason": "all current routes are blocked and no baseline comparison has been run",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": "DEC1876_0_result",
            "decision": "BLOCKING_RUNNER_DRYRUN_PASS_ALL_ARENAS_BLOCKED",
            "reason": "local_GR, PPN/light-time, R10, clock, WEP, and orbital routes all return claim_allowed=false with exact RV1875 blockers",
            "consequence": "future local tests cannot accidentally treat unsigned residuals as a pass",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": "DEC1876_1_R10_route",
            "decision": "R10_MASSLESS_ROUTE_FORBIDDEN_MACHINE_READABLE",
            "reason": "RV1875_5_massless_tail is deliberately excluded from the R10 finite-range required vector rows and appears only as a forbidden route test",
            "consequence": "R10 can only be attempted after finite operator/source/projection rows exist",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": "DEC1876_2_next",
            "decision": "DERIVATION_PRIORITY_RETURNS_TO_QSHAPE_OR_LAMBDAR",
            "reason": "the cleanest route is still a parent theorem for q_shape/Dq[v_R]=0 or lambda_R/no-pole ownership",
            "consequence": "1877 should hunt the parent origin before spending more time on empirical coefficient sourcing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "route_id": "NEXT1876_0_primary",
            "target_doc": "1877-Y5-R2FR-qshape-or-lambdaR-parent-origin-source-hunt.md",
            "target_script": "scripts/Y5_R2FR_qshape_or_lambdaR_parent_origin_source_hunt_1877.py",
            "objective": "try to derive a parent q_shape or lambda_R/no-pole mechanism that signs Dq[v_R]=0 or removes R_AB before local observables see it.",
            "selection_status": "selected",
            "success_condition": "source-backed parent theorem, or explicit no-go that keeps R_AB as a finite residual field.",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "route_id": "NEXT1876_1_fallback",
            "target_doc": "1877b-Y5-R2FR-CR-PiR-kappaMstar-bound-runner.md",
            "target_script": "scripts/Y5_R2FR_CR_PiR_kappaMstar_bound_runner_1877b.py",
            "objective": "if the parent theorem still fails, stage the massless-tail PPN/orbital bound runner without claiming a pass.",
            "selection_status": "held_fallback",
            "success_condition": "nonclaim bound rows for C_R/Pi_R/kappa_W/M_* and tau_PPN/tau_orbital, with all claims blocked unless sourced.",
            "valid_for_claim": False,
        },
    ]


def all_output_rows() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "input_audit": input_audit_rows(),
        "arena_dryrun": arena_dryrun_rows(),
        "forbidden_route_tests": forbidden_route_test_rows(),
        "claim_gate": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
    }


def all_claim_flags_false(paths: list[Path]) -> tuple[bool, str]:
    checked = 0
    for path in paths:
        for row_index, row in enumerate(csv_rows(path), start=2):
            for column in [
                "valid_for_claim",
                "claim_allowed",
                "public_claim_allowed",
                "score_ready",
                "valid_prediction_row",
            ]:
                if column in row:
                    checked += 1
                    if bool_string(row[column]) == "true":
                        return False, f"{path.name}:{row_index}:{column}=true"
    return checked > 0, f"checked={checked}"


def csv_parse_check(paths: list[Path]) -> tuple[bool, str]:
    details: list[str] = []
    for path in paths:
        rows = csv_rows(path)
        if not rows:
            return False, f"EMPTY_CSV={path.name}"
        details.append(f"{path.name}:{len(rows)}")
    return True, ";".join(details)


def copy_branch_artifacts() -> None:
    for path in OUTPUTS.values():
        if path.name.endswith("_VALIDATION.csv"):
            continue
        shutil.copy2(path, MICROSCOPE_RESIDUALS / path.name)
        shutil.copy2(path, QUARANTINE / path.name)
    shutil.copy2(OUTPUTS["arena_dryrun"], QUEUE / "JR1876_RAB_ARENA_BLOCKING_DRYRUN_NONCLAIM.csv")
    shutil.copy2(OUTPUTS["forbidden_route_tests"], QUEUE / "JR1876_RAB_FORBIDDEN_ROUTE_TESTS_NONCLAIM.csv")
    shutil.copy2(OUTPUTS["next_target"], QUEUE / "JR1876_NEXT_TARGET_NONCLAIM.csv")


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def validation_rows() -> list[dict[str, Any]]:
    generated_without_validation = [path for key, path in OUTPUTS.items() if key != "validation"]
    rows_by_name = {key: csv_rows(path) for key, path in OUTPUTS.items() if key != "validation"}
    checks: list[dict[str, Any]] = []

    sources = rows_by_name["source_register"]
    checks.append(
        {
            "validation_id": "VAL1876_0_sources",
            "status": "PASS" if all(bool_string(row["usable_for_1876"]) == "true" for row in sources) else "FAIL",
            "detail": "1875 vector, routing, contract, claim gate, validation, and selected target are present",
            "valid_for_claim": False,
        }
    )

    audit = rows_by_name["input_audit"]
    checks.append(
        {
            "validation_id": "VAL1876_1_input_audit",
            "status": "PASS"
            if sum(1 for row in audit if row["input_table"] == "1875_residual_vector") == 11
            and sum(1 for row in audit if row["input_table"] == "1875_test_routing") == 5
            and sum(1 for row in audit if row["input_table"] == "1875_runner_contract") == 5
            else "FAIL",
            "detail": "runner consumed all 1875 vector, routing, and contract rows",
            "valid_for_claim": False,
        }
    )

    arena = rows_by_name["arena_dryrun"]
    arena_names = {row["arena"] for row in arena}
    required_coverage = {
        "local_GR/Newton_limit",
        "PPN/light-time",
        "R10 alpha(lambda)",
        "clock/material",
        "WEP/material",
        "orbital_massless_tail",
        "orbital_finite_range",
    }
    checks.append(
        {
            "validation_id": "VAL1876_2_arena_coverage",
            "status": "PASS" if required_coverage.issubset(arena_names) else "FAIL",
            "detail": "local_GR, PPN, R10, clock, WEP, and orbital branches are represented",
            "valid_for_claim": False,
        }
    )

    checks.append(
        {
            "validation_id": "VAL1876_3_all_arenas_blocked",
            "status": "PASS"
            if all(row["runner_status"] == "BLOCKED_NONCLAIM" for row in arena)
            and all(bool_string(row["claim_allowed"]) == "false" for row in arena)
            and all(row["missing_vector_rows"].startswith("RV1875_") for row in arena)
            else "FAIL",
            "detail": "every arena returns blocked/nonclaim with exact RV1875 missing row IDs",
            "valid_for_claim": False,
        }
    )

    r10_rows = [row for row in arena if row["arena"] == "R10 alpha(lambda)"]
    forbidden = rows_by_name["forbidden_route_tests"]
    checks.append(
        {
            "validation_id": "VAL1876_4_R10_route_separation",
            "status": "PASS"
            if len(r10_rows) == 1
            and "RV1875_5_massless_tail" not in r10_rows[0]["required_vector_rows"]
            and "RV1875_5_massless_tail" in r10_rows[0]["forbidden_vector_rows"]
            and any(row["runner_status"] == "WRONG_ARENA_ROUTE_BLOCKS_SCORE" for row in forbidden)
            else "FAIL",
            "detail": "massless C_R/r route is machine-blocked from R10 alpha(lambda)",
            "valid_for_claim": False,
        }
    )

    checks.append(
        {
            "validation_id": "VAL1876_5_contract_forbidden_tests",
            "status": "PASS"
            if all("BLOCKS" in row["runner_status"] or row["runner_status"] == "CLOSURE_ONLY_BLOCKS_CLAIM" for row in forbidden)
            and all(bool_string(row["claim_allowed"]) == "false" for row in forbidden)
            else "FAIL",
            "detail": "route separation, closure-only, no-cancellation, normalization, and baseline failures all block",
            "valid_for_claim": False,
        }
    )

    claim_gates = rows_by_name["claim_gate"]
    checks.append(
        {
            "validation_id": "VAL1876_6_claim_gate",
            "status": "PASS"
            if any(row["status"] == "ALLOW_INTERNAL_NONCLAIM_RUNNER" for row in claim_gates)
            and all(bool_string(row["claim_allowed"]) == "false" for row in claim_gates)
            else "FAIL",
            "detail": "only the internal dry-run harness is allowed, not any physics claim",
            "valid_for_claim": False,
        }
    )

    decisions = rows_by_name["decision"]
    checks.append(
        {
            "validation_id": "VAL1876_7_decision",
            "status": "PASS"
            if any(row["decision"] == "BLOCKING_RUNNER_DRYRUN_PASS_ALL_ARENAS_BLOCKED" for row in decisions)
            and any(row["decision"] == "DERIVATION_PRIORITY_RETURNS_TO_QSHAPE_OR_LAMBDAR" for row in decisions)
            else "FAIL",
            "detail": "decision ledger records all-arenas blocked and selects derivation-first next target",
            "valid_for_claim": False,
        }
    )

    next_targets = rows_by_name["next_target"]
    checks.append(
        {
            "validation_id": "VAL1876_8_next_target",
            "status": "PASS"
            if any(row["route_id"] == "NEXT1876_0_primary" and row["selection_status"] == "selected" for row in next_targets)
            else "FAIL",
            "detail": "1877 q_shape/lambda_R parent-origin hunt selected",
            "valid_for_claim": False,
        }
    )

    flags_ok, flags_detail = all_claim_flags_false(generated_without_validation)
    checks.append(
        {
            "validation_id": "VAL1876_9_claim_flags_false",
            "status": "PASS" if flags_ok else "FAIL",
            "detail": flags_detail,
            "valid_for_claim": False,
        }
    )

    parse_ok, parse_detail = csv_parse_check(generated_without_validation)
    checks.append(
        {
            "validation_id": "VAL1876_10_csv_parse",
            "status": "PASS" if parse_ok else "FAIL",
            "detail": parse_detail,
            "valid_for_claim": False,
        }
    )

    copied_paths = [
        MICROSCOPE_RESIDUALS / OUTPUTS["arena_dryrun"].name,
        QUARANTINE / OUTPUTS["forbidden_route_tests"].name,
        QUEUE / "JR1876_RAB_ARENA_BLOCKING_DRYRUN_NONCLAIM.csv",
        QUEUE / "JR1876_RAB_FORBIDDEN_ROUTE_TESTS_NONCLAIM.csv",
    ]
    checks.append(
        {
            "validation_id": "VAL1876_11_branch_copies",
            "status": "PASS" if all(path.exists() for path in copied_paths) else "FAIL",
            "detail": ";".join(str(path) for path in copied_paths),
            "valid_for_claim": False,
        }
    )

    pycache = Path(__file__).resolve().parent / "__pycache__"
    checks.append(
        {
            "validation_id": "VAL1876_12_pycache_absent",
            "status": "PASS" if not pycache.exists() else "FAIL",
            "detail": str(pycache),
            "valid_for_claim": False,
        }
    )

    formalization_hits = list(FORMALIZATION.rglob("*1876*")) if FORMALIZATION.exists() else []
    checks.append(
        {
            "validation_id": "VAL1876_13_formalization_untouched",
            "status": "PASS" if not formalization_hits else "FAIL",
            "detail": f"formalization_1876_count={len(formalization_hits)}",
            "valid_for_claim": False,
        }
    )

    fail_count = sum(1 for row in checks if row["status"] != "PASS")
    checks.append(
        {
            "validation_id": "VAL1876_OVERALL",
            "status": "PASS" if fail_count == 0 else "FAIL",
            "detail": "1876 R_AB residual vector blocking runner dry-run",
            "valid_for_claim": False,
        }
    )
    return checks


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key not in headers:
                headers.append(key)
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        values = [str(row.get(header, "")).replace("\n", " ") for header in headers]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    validation = csv_rows(OUTPUTS["validation"])
    content = f"""# 1876 - R_AB Residual Vector Blocking Runner Dry-Run

**Private status:** nonclaim checkpoint. This is a machine-readable safety harness, not a physics pass.

## Result

The 1875 residual vector now has a dry-run runner. Every current local arena is forced to `claim_allowed=false` until its required rows are either theorem-zero or numeric, source-backed, unit-declared, and in the correct arena route.

The important lock is:

```text
R10 alpha(lambda) must use: Z_R, M_R^2, lambda_range, source/test charges, tau_R10.
R10 alpha(lambda) must not use: C_R/r massless tail.
C_R/r massless tail may only go to: PPN, light-time, or orbital massless-tail tests.
```

This is useful even though it is all blocked: it stops the framework from accidentally winning by smuggling a closure, a wrong-route residual, or a cancellation into a test.

## Source Register

{markdown_table(rows_by_name["source_register"])}

## Runner Input Audit

{markdown_table(rows_by_name["input_audit"])}

## Arena Blocking Dry-Run

{markdown_table(rows_by_name["arena_dryrun"])}

## Forbidden Route Tests

{markdown_table(rows_by_name["forbidden_route_tests"])}

## Claim Gate

{markdown_table(rows_by_name["claim_gate"])}

## Decision Ledger

{markdown_table(rows_by_name["decision"])}

## Next Target

{markdown_table(rows_by_name["next_target"])}

## Validation

{markdown_table(validation)}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    rows_by_name = all_output_rows()
    for key, rows in rows_by_name.items():
        write_csv(OUTPUTS[key], rows)
    copy_branch_artifacts()
    remove_pycache()
    write_csv(OUTPUTS["validation"], validation_rows())
    write_doc(rows_by_name)


if __name__ == "__main__":
    main()
