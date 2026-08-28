from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import shutil
import sys
import time
from typing import Any


for thread_variable in (
    "OMP_NUM_THREADS",
    "OPENBLAS_NUM_THREADS",
    "MKL_NUM_THREADS",
    "NUMEXPR_NUM_THREADS",
    "VECLIB_MAXIMUM_THREADS",
    "BLIS_NUM_THREADS",
):
    os.environ[thread_variable] = "1"
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[2]
POST = Path(__file__).resolve().parents[1]
SCRIPTS = POST / "scripts"
FORMAL = ROOT / "formalization-workbench"
FUNCTIONAL_RG = POST / "source-intake" / "functional_rg"
MTS_RESIDUALS = POST / "source-intake" / "mts_residuals"

SCRIPT_5317 = SCRIPTS / "Y5_R2FR_5317_targeted_inner_pole_resolution.py"
SCRIPT_5326 = SCRIPTS / "Y5_R2FR_5326_D2_midpoint_event_aligned_E0025_refinement.py"
SCRIPT_5327 = SCRIPTS / "Y5_R2FR_5327_D2_midpoint_regulator_ladder_controller.py"
SCRIPT_5334 = SCRIPTS / "Y5_R2FR_5334_D4_outer_regulator_ladder_controller.py"
SCRIPT_5371 = SCRIPTS / "Y5_R2FR_5371_D4_E020_preregistered_seventh_rung_runner.py"

TARGET = FUNCTIONAL_RG / "5334" / "E020"
TARGET_RESULT = TARGET / "D4_outer_event_aligned_E020_result.json"
TARGET_FINITE = TARGET / "D4_outer_event_aligned_E020_finite_value.csv"
TARGET_MANIFEST = TARGET / "D4_outer_event_aligned_E020_node_manifest.csv"
TARGET_POLES = TARGET / "D4_outer_event_aligned_E020_geometric_poles.csv"
TARGET_CLASSIFICATIONS = TARGET / "D4_outer_event_aligned_E020_pole_classification.csv"

COMPARATOR_CONTRACT = (
    FUNCTIONAL_RG
    / "5372"
    / "E020"
    / "D4_E020_blind_holdout_comparison_contract.json"
)
COMPARATOR_RESULT = (
    FUNCTIONAL_RG
    / "5372"
    / "E020"
    / "D4_E020_blind_holdout_comparison_result.json"
)
SEVEN_RUNG_CONTRACT = (
    FUNCTIONAL_RG / "5373" / "D4_seven_rung_extended_window_gate_contract.json"
)

OUTPUT = FUNCTIONAL_RG / "5374" / "E020"
PRE_RESULT = OUTPUT / "pre_repair_measurement_result.json"
PRE_MANIFEST = OUTPUT / "pre_repair_failed_node_manifest.csv"
PRE_POLES = OUTPUT / "pre_repair_failed_node_poles.csv"
PRE_CLASSIFICATIONS = OUTPUT / "pre_repair_failed_node_classifications.csv"
BACKUP_SHARDS = OUTPUT / "pre_repair_failed_shards"
CONTRACT = OUTPUT / "D4_E020_multipole_laurent_repair_contract.json"
CONTRACT_VALIDATION = OUTPUT / "D4_E020_multipole_laurent_repair_contract_validation.csv"
CONTRACT_SOURCES = OUTPUT / "D4_E020_multipole_laurent_repair_contract_sources.csv"
CANDIDATES = OUTPUT / "D4_E020_multipole_laurent_candidate_audit.csv"
SELECTIONS = OUTPUT / "D4_E020_multipole_laurent_selections.csv"
DIAGNOSTIC_RESULT = OUTPUT / "D4_E020_multipole_laurent_diagnostic_result.json"
V1_CANDIDATES = OUTPUT / "D4_E020_multipole_laurent_v1_failed_candidate_audit.csv"
V1_SELECTIONS = OUTPUT / "D4_E020_multipole_laurent_v1_partial_selections.csv"
V1_DIAGNOSTIC_RESULT = OUTPUT / "D4_E020_multipole_laurent_v1_failed_diagnostic_result.json"
REPAIR_LEDGER = OUTPUT / "D4_E020_multipole_laurent_repair_ledger.csv"
REPAIR_FITS = OUTPUT / "D4_E020_multipole_laurent_selected_fits.csv"
REPAIR_IDENTITIES = OUTPUT / "D4_E020_multipole_masked_identity.csv"
RESULT = OUTPUT / "D4_E020_multipole_laurent_repair_result.json"
VALIDATION = OUTPUT / "D4_E020_multipole_laurent_repair_validation.csv"
SOURCE_REGISTER = OUTPUT / "source_register.csv"
STATUS = OUTPUT / "status.json"
RESIDUAL_VALIDATION = MTS_RESIDUALS / "P8_Y5_BRR545_5374_VALIDATION.csv"
DOCUMENT = POST / "5374-Y5-R2FR-D4-E020-source-silent-multipole-laurent-repair.md"

CHECKPOINT = 5374
MARKER = "MTS_5374_D4_E020_SOURCE_SILENT_MULTIPOLE_LAURENT_REPAIR"
REVISION = "D4-E020-source-silent-multipole-laurent-repair-v2"
REPAIR_REVISION = "D4-outer-source-silent-multipole-double-laurent-v2"
EPSILON_ID = "E020"
EXPECTED_FAILED_NODE_COUNT = 4
CANDIDATE_BACKGROUND_DEGREES = (4, 5, 6)
CANDIDATE_MAXIMUM_REFINEMENTS = (4, 5, 6)
ENERGY_SUBDIVISION_LADDER = (0, 64, 128)
FORMAL_DIGEST = "0ec1bc6012136ffc6b28a1512aca6ce712b6decd2ff793310a9bd61775f3db1f"

CLAIM_LOCAL_REPAIR = "valid_for_D4_E020_source_silent_multipole_laurent_repair"
FALSE_CLAIMS = (
    "valid_for_D4_E020_complete_family_holdout_compatibility",
    "valid_for_D4_seven_rung_complete_second_order_fit",
    "valid_for_D4_numeric_uniform_remainder_bound",
    "valid_for_D4_outer_regulator_zero_limit",
    "valid_for_decay_angle_integral",
    "valid_for_full_angular_convergence",
    "valid_for_full_phase_space_coefficient",
    "valid_for_numeric_UV_claim",
    "valid_for_local_GR_claim",
    "valid_for_full_MTS_claim",
)


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


R5371 = load_module("mts_5371_for_5374", SCRIPT_5371)
M5334 = R5371.M5334
M5327 = M5334.M5327
M5326 = R5371.M5326
M5312 = M5326.M5312
M5283 = R5371.M5283


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def set_below_normal_priority() -> None:
    M5334.M5312.set_below_normal_priority()


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def parse_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() == "true"


def atomic_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"empty CSV payload: {path}")
    fields: list[str] = []
    for row in rows:
        for field in row:
            if field not in fields:
                fields.append(field)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    temporary.replace(path)


def atomic_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(payload, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


def validation_row(gate: str, passed: bool, detail: Any) -> dict[str, Any]:
    return {"gate": gate, "passed": bool(passed), "detail": str(detail)}


def false_claims() -> dict[str, bool]:
    return {field: False for field in FALSE_CLAIMS}


def complex_fields(prefix: str, value: complex) -> dict[str, float]:
    return {
        f"{prefix}_real": float(value.real),
        f"{prefix}_imaginary": float(value.imag),
        f"{prefix}_magnitude": float(abs(value)),
    }


def source_register_current(path: Path) -> tuple[bool, int, list[str]]:
    if not path.is_file():
        return False, 0, [str(path)]
    rows = read_csv(path)
    drifts: list[str] = []
    for row in rows:
        source = Path(row["path"])
        if not source.is_file() or digest(source) != row["sha256"]:
            drifts.append(str(source))
    return not drifts, len(rows), drifts


def configure() -> None:
    R5371.configure_target()
    M5326.configure_kernel()
    M5326.NEAR_SUPPORT_REPAIR_REVISION = REPAIR_REVISION


def failed_manifest_rows() -> list[dict[str, str]]:
    return [row for row in read_csv(TARGET_MANIFEST) if row["shard_state"] == "COMPLETE_FAIL"]


def unresolved_rows_for_node(node_id: str) -> list[dict[str, str]]:
    path = M5312.shard_paths(node_id)["classifications"]
    return [
        row
        for row in read_csv(path)
        if not parse_bool(row["pole_classification_resolved"])
    ]


def pole_rows_for_node(node_id: str) -> list[dict[str, str]]:
    return read_csv(M5312.shard_paths(node_id)["poles"])


def snapshot_pre_repair() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    shutil.copy2(TARGET_RESULT, PRE_RESULT)
    failed = failed_manifest_rows()
    node_ids = {row["node_id"] for row in failed}
    atomic_csv(PRE_MANIFEST, failed)
    atomic_csv(
        PRE_POLES,
        [row for row in read_csv(TARGET_POLES) if row["node_id"] in node_ids],
    )
    atomic_csv(
        PRE_CLASSIFICATIONS,
        [
            row
            for row in read_csv(TARGET_CLASSIFICATIONS)
            if row["node_id"] in node_ids
        ],
    )


def snapshot_failed_v1_diagnostic() -> None:
    if not DIAGNOSTIC_RESULT.is_file():
        return
    result = read_json(DIAGNOSTIC_RESULT)
    if (
        result.get("revision") != "D4-E020-source-silent-multipole-laurent-repair-v1"
        or result.get("validation_passed") is not False
    ):
        return
    for source, destination in (
        (CANDIDATES, V1_CANDIDATES),
        (SELECTIONS, V1_SELECTIONS),
        (DIAGNOSTIC_RESULT, V1_DIAGNOSTIC_RESULT),
    ):
        if source.is_file() and not destination.exists():
            shutil.copy2(source, destination)


def contract_source_paths() -> tuple[Path, ...]:
    return (
        Path(__file__).resolve(),
        SCRIPT_5317,
        SCRIPT_5326,
        SCRIPT_5327,
        SCRIPT_5334,
        SCRIPT_5371,
        COMPARATOR_CONTRACT,
        SEVEN_RUNG_CONTRACT,
        PRE_RESULT,
        PRE_MANIFEST,
        PRE_POLES,
        PRE_CLASSIFICATIONS,
        V1_CANDIDATES,
        V1_SELECTIONS,
        V1_DIAGNOSTIC_RESULT,
    )


def render_document(payload: dict[str, Any]) -> None:
    lines = [
        "# 5374 - D4 E020 source-silent multipole Laurent repair",
        "",
        "## Decision",
        "",
        f"`{payload['decision']}`",
        "",
        "The completed E020 run localized four failed inner nodes to residue-classification gates. This repair transfers the parent normalized double-Laurent pole-refinement method to every unresolved pole in a node, preserving all existing residual, scale-change, second-order, masked-identity, inner-quadrature, and global error thresholds.",
        "",
        "The v1 diagnostic resolved six of seven poles. Its last pole stopped after four refinement iterations with a residual double-pole ratio of 1.0589550643390497e-4, while its fourth pole correction remained 1.0991090150822313e-11 against the unchanged 1e-11 convergence tolerance. Version 2 therefore tests the deterministic refinement-count ladder 4, 5, 6 before increasing background degree; it does not relax a gate.",
        "",
        "Candidate selection uses only local pole-fit and topology diagnostics. It does not read the frozen E020 prediction, perform the holdout comparison, or optimize the measured finite-rung central value.",
        "",
        "No regulator-zero, angular, UV, local-GR, or full-MTS claim is made by the repair contract.",
    ]
    temporary = DOCUMENT.with_suffix(DOCUMENT.suffix + ".tmp")
    temporary.write_text("\n".join(lines) + "\n", encoding="utf-8")
    temporary.replace(DOCUMENT)


def freeze_contract() -> dict[str, Any]:
    configure()
    required = (
        TARGET_RESULT,
        TARGET_FINITE,
        TARGET_MANIFEST,
        TARGET_POLES,
        TARGET_CLASSIFICATIONS,
        COMPARATOR_CONTRACT,
        SEVEN_RUNG_CONTRACT,
    )
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise FileNotFoundError(missing)
    snapshot_pre_repair()
    snapshot_failed_v1_diagnostic()
    v1_missing = [
        str(path)
        for path in (V1_CANDIDATES, V1_SELECTIONS, V1_DIAGNOSTIC_RESULT)
        if not path.is_file()
    ]
    if v1_missing:
        raise FileNotFoundError(v1_missing)
    result = read_json(PRE_RESULT)
    comparator = read_json(COMPARATOR_CONTRACT)
    seven = read_json(SEVEN_RUNG_CONTRACT)
    failed = read_csv(PRE_MANIFEST)
    classifications = read_csv(PRE_CLASSIFICATIONS)
    unresolved = [
        row for row in classifications if not parse_bool(row["pole_classification_resolved"])
    ]
    node_ids = {row["node_id"] for row in failed}
    v1_result = read_json(V1_DIAGNOSTIC_RESULT)
    v1_candidates = read_csv(V1_CANDIDATES)
    v1_selections = read_csv(V1_SELECTIONS)
    checks = {
        "E020_completed_before_repair_audit": result.get("completed_full_run") is True
        and result.get("acceptance_passed") is False
        and result.get("decision") == "D4_OUTER_EVENT_ALIGNED_E020_REQUIRES_REFINEMENT",
        "exactly_four_failed_nodes_are_source_localized": len(failed)
        == EXPECTED_FAILED_NODE_COUNT
        and int(result.get("failed_inner_node_count", -1)) == EXPECTED_FAILED_NODE_COUNT
        and len(node_ids) == EXPECTED_FAILED_NODE_COUNT,
        "all_failures_are_unresolved_nonzero_residue_classifications": bool(unresolved)
        and {row["node_id"] for row in unresolved} == node_ids
        and all(
            row["failure_reason"] == "RESIDUE_CLASSIFICATION_GATE_FAILED"
            and float(row["selected_residue_magnitude"])
            >= float(M5312.MATERIAL_RESIDUE_FLOOR)
            for row in unresolved
        ),
        "comparison_and_seven_rung_rules_were_frozen_but_not_executed": comparator.get(
            "validation_passed"
        )
        is True
        and comparator.get("measurement_absent_at_freeze") is True
        and comparator.get("comparison_executed") is False
        and not COMPARATOR_RESULT.exists()
        and seven.get("validation_passed") is True
        and seven.get("measurement_absent_at_freeze") is True
        and seven.get("gate_executed") is False,
        "repair_family_is_deterministic_and_threshold_preserving": CANDIDATE_BACKGROUND_DEGREES
        == (4, 5, 6)
        and CANDIDATE_MAXIMUM_REFINEMENTS == (4, 5, 6)
        and ENERGY_SUBDIVISION_LADDER == (0, 64, 128)
        and float(M5326.NEAR_SUPPORT_FIT_RELATIVE_RESIDUAL_LIMIT) == 1.0e-5
        and float(M5326.NEAR_SUPPORT_RESIDUE_SCALE_CHANGE_LIMIT) == 1.0e-3
        and float(M5326.NEAR_SUPPORT_SECOND_ORDER_SUPPRESSION_LIMIT) == 1.0e-4
        and float(M5326.NEAR_SUPPORT_MASKED_IDENTITY_LIMIT) == 1.0e-9
        and float(M5326.NEAR_SUPPORT_POLE_REFINEMENT_TOLERANCE) == 1.0e-11,
        "v1_failure_is_preserved_and_localized_before_v2": v1_result.get(
            "validation_passed"
        )
        is False
        and v1_result.get("selected_candidate_count") == 6
        and v1_result.get("expected_unresolved_pole_count") == 7
        and len(v1_candidates) == 9
        and len(v1_selections) == 6,
        "formal_workbench_unchanged": M5283.formal_inventory_digest() == FORMAL_DIGEST,
        "scripts_cache_absent": not (SCRIPTS / "__pycache__").exists(),
    }
    validations = [validation_row(key, value, value) for key, value in checks.items()]
    passed = all(checks.values())
    claims = {CLAIM_LOCAL_REPAIR: False, **false_claims()}
    payload = {
        "checkpoint": CHECKPOINT,
        "marker": MARKER,
        "revision": REVISION,
        "mode": "D4-E020-source-silent-multipole-laurent-repair-contract",
        "validation_passed": passed,
        "decision": (
            "D4_E020_MULTIPOLE_LAURENT_REPAIR_FROZEN__RUN_SOURCE_SILENT_CANDIDATES"
            if passed
            else "D4_E020_MULTIPOLE_LAURENT_REPAIR_CONTRACT_BLOCKED"
        ),
        "failed_node_count": len(failed),
        "unresolved_pole_count": len(unresolved),
        "candidate_background_degrees": list(CANDIDATE_BACKGROUND_DEGREES),
        "candidate_maximum_refinements": list(CANDIDATE_MAXIMUM_REFINEMENTS),
        "candidate_selection_rule": "LOWEST_BACKGROUND_DEGREE_THEN_LOWEST_MAXIMUM_REFINEMENT_COUNT_PASSING_ALL_UNCHANGED_LOCAL_GATES_PER_POLE",
        "energy_subdivision_ladder": list(ENERGY_SUBDIVISION_LADDER),
        "unchanged_thresholds": {
            "fit_relative_residual": M5326.NEAR_SUPPORT_FIT_RELATIVE_RESIDUAL_LIMIT,
            "residue_scale_change": M5326.NEAR_SUPPORT_RESIDUE_SCALE_CHANGE_LIMIT,
            "second_order_suppression": M5326.NEAR_SUPPORT_SECOND_ORDER_SUPPRESSION_LIMIT,
            "masked_identity": M5326.NEAR_SUPPORT_MASKED_IDENTITY_LIMIT,
            "pole_refinement_tolerance": M5326.NEAR_SUPPORT_POLE_REFINEMENT_TOLERANCE,
            "inner_relative_change": M5312.INNER_RELATIVE_CHANGE_LIMIT,
            "inner_error_budget": M5312.INNER_ERROR_BUDGET_LIMIT,
            "outer_relative_change": M5326.LOCAL_OUTER_CHANGE_LIMIT,
            "global_error_budget": M5326.GLOBAL_ERROR_BUDGET_LIMIT,
        },
        "source_silence_contract": {
            "frozen_holdout_prediction_read_for_selection": False,
            "measured_finite_rung_central_value_read_for_selection": False,
            "comparison_or_seven_rung_gate_executed": False,
            "selection_inputs": "failed-node poles, local fit residuals, refinement-count convergence, topology purity, masked identity, and unchanged convergence gates only",
        },
        "claim_boundary": claims,
        "formalization_workbench_modified_file_count": 0,
        "updated_utc": utc_now(),
    }
    sources = contract_source_paths()
    source_rows = [
        {"path": str(path.resolve()), "sha256": digest(path), "exists": True, **claims}
        for path in sources
    ]
    atomic_csv(CONTRACT_VALIDATION, validations)
    atomic_csv(CONTRACT_SOURCES, source_rows)
    atomic_json(CONTRACT, payload)
    atomic_json(
        STATUS,
        {
            "checkpoint": CHECKPOINT,
            "state": "contract_frozen" if passed else "blocked",
            "decision": payload["decision"],
            "updated_utc": payload["updated_utc"],
        },
    )
    render_document(payload)
    return payload


def candidate_for_pole(
    node: dict[str, Any],
    pole: dict[str, str],
    degree: int,
    maximum_refinements: int,
    base_context: dict[str, Any],
) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]]]:
    term_id = pole["term_id"]
    coordinate = float(node["absolute_soft_cosine"])
    evaluator = M5326.near_support_unmasked_evaluator(base_context, term_id)
    old_degree = M5326.NEAR_SUPPORT_FIT_BACKGROUND_DEGREE
    old_maximum_refinements = M5326.NEAR_SUPPORT_MAXIMUM_POLE_REFINEMENTS
    try:
        M5326.NEAR_SUPPORT_FIT_BACKGROUND_DEGREE = degree
        M5326.NEAR_SUPPORT_MAXIMUM_POLE_REFINEMENTS = maximum_refinements
        M5327.INTERIOR_FIT_DIAGNOSTICS.clear()
        selected, fit_rows = M5327.E000625_refine_near_support_simple_pole(
            coordinate,
            pole,
            evaluator,
        )
    finally:
        M5326.NEAR_SUPPORT_FIT_BACKGROUND_DEGREE = old_degree
        M5326.NEAR_SUPPORT_MAXIMUM_POLE_REFINEMENTS = old_maximum_refinements
    identity_rows, identity_passes = M5326.near_support_masked_identity_audit(
        coordinate,
        term_id,
        selected,
        evaluator,
        M5312.M5305.component_evaluator(base_context),
    )
    topology_passes = bool(selected.get("interior_topology_preflight_passes", False))
    passes = bool(selected["fit_contract_passes"]) and topology_passes and identity_passes
    summary = {
        "node_id": node["node_id"],
        "x_panel_index": int(node["x_panel_index"]),
        "absolute_soft_cosine": coordinate,
        "term_id": term_id,
        "pole_id": pole["pole_id"],
        "primary_surface_id": pole["primary_surface_id"],
        "background_degree": degree,
        "maximum_pole_refinements": maximum_refinements,
        "fit_contract_passes": bool(selected["fit_contract_passes"]),
        "topology_preflight_passes": topology_passes,
        "masked_identity_passes": identity_passes,
        "candidate_passes": passes,
        **complex_fields("refined_pole", complex(selected["refined_pole"])),
        **complex_fields("selected_residue", complex(selected["selected_residue"])),
        "maximum_fit_relative_residual": float(selected["fit_relative_residual"]),
        "residue_scale_relative_change": float(
            selected["residue_fit_scale_relative_change"]
        ),
        "second_order_suppression_ratio": float(
            selected["second_order_suppression_ratio"]
        ),
        "fit_geometry_mode": selected.get("fit_geometry_mode", ""),
        "pole_side": selected["pole_side"],
        **false_claims(),
    }
    enriched_fits = []
    for row in fit_rows:
        enriched_fits.append(
            {
                "node_id": node["node_id"],
                "x_panel_index": int(node["x_panel_index"]),
                "absolute_soft_cosine": coordinate,
                "term_id": term_id,
                "support_id": pole["support_id"],
                "pole_id": pole["pole_id"],
                "primary_surface_id": pole["primary_surface_id"],
                "background_degree": degree,
                "maximum_pole_refinements": maximum_refinements,
                **row,
                "near_support_masked_identity_passes": identity_passes,
                "near_support_subtraction_contract_passes": passes,
                **false_claims(),
            }
        )
    enriched_identities = [
        {
            "node_id": node["node_id"],
            "x_panel_index": int(node["x_panel_index"]),
            "absolute_soft_cosine": coordinate,
            "term_id": term_id,
            "support_id": pole["support_id"],
            "pole_id": pole["pole_id"],
            "primary_surface_id": pole["primary_surface_id"],
            "background_degree": degree,
            "maximum_pole_refinements": maximum_refinements,
            **row,
            **false_claims(),
        }
        for row in identity_rows
    ]
    summary["selected_payload"] = selected
    return summary, enriched_fits, enriched_identities


def contract_is_current() -> tuple[dict[str, Any], tuple[bool, int, list[str]]]:
    if not CONTRACT.is_file():
        raise FileNotFoundError(CONTRACT)
    contract = read_json(CONTRACT)
    sources = source_register_current(CONTRACT_SOURCES)
    if contract.get("validation_passed") is not True or not sources[0]:
        raise RuntimeError(f"5374 contract is not current: {sources}")
    return contract, sources


def diagnose_candidates() -> dict[str, Any]:
    configure()
    contract, sources = contract_is_current()
    base_context = M5312.M5303.synthetic_context()
    candidates: list[dict[str, Any]] = []
    selections: list[dict[str, Any]] = []
    failed = read_csv(PRE_MANIFEST)
    for node in failed:
        node_id = node["node_id"]
        poles = {
            (row["term_id"], row["pole_id"]): row
            for row in pole_rows_for_node(node_id)
        }
        for classification in unresolved_rows_for_node(node_id):
            key = (classification["term_id"], classification["pole_id"])
            selected_summary: dict[str, Any] | None = None
            for degree in CANDIDATE_BACKGROUND_DEGREES:
                for maximum_refinements in CANDIDATE_MAXIMUM_REFINEMENTS:
                    try:
                        summary, _, _ = candidate_for_pole(
                            node,
                            poles[key],
                            degree,
                            maximum_refinements,
                            base_context,
                        )
                    except Exception as error:
                        summary = {
                            "node_id": node_id,
                            "x_panel_index": int(node["x_panel_index"]),
                            "absolute_soft_cosine": float(
                                node["absolute_soft_cosine"]
                            ),
                            "term_id": key[0],
                            "pole_id": key[1],
                            "primary_surface_id": poles[key]["primary_surface_id"],
                            "background_degree": degree,
                            "maximum_pole_refinements": maximum_refinements,
                            "fit_contract_passes": False,
                            "topology_preflight_passes": False,
                            "masked_identity_passes": False,
                            "candidate_passes": False,
                            "failure_reason": f"{type(error).__name__}: {error}",
                            **false_claims(),
                        }
                    summary.pop("selected_payload", None)
                    candidates.append(summary)
                    if parse_bool(summary.get("candidate_passes", False)):
                        selected_summary = dict(summary)
                        break
                if selected_summary is not None:
                    break
            if selected_summary is not None:
                selected_summary["selection_rule"] = contract["candidate_selection_rule"]
                selections.append(selected_summary)
    expected_count = sum(
        not parse_bool(row["pole_classification_resolved"])
        for row in read_csv(PRE_CLASSIFICATIONS)
    )
    passed = len(selections) == expected_count and all(
        parse_bool(row["candidate_passes"]) for row in selections
    )
    atomic_csv(CANDIDATES, candidates)
    if selections:
        atomic_csv(SELECTIONS, selections)
    payload = {
        "checkpoint": CHECKPOINT,
        "marker": MARKER,
        "revision": REVISION,
        "mode": "D4-E020-source-silent-multipole-laurent-candidate-diagnostic",
        "validation_passed": passed,
        "decision": (
            "D4_E020_ALL_UNRESOLVED_POLES_HAVE_SOURCE_SILENT_LAURENT_CANDIDATES__RUN_LOCAL_REPAIR"
            if passed
            else "D4_E020_MULTIPOLE_LAURENT_CANDIDATES_INCOMPLETE__DO_NOT_REPAIR"
        ),
        "failed_node_count": len(failed),
        "expected_unresolved_pole_count": expected_count,
        "selected_candidate_count": len(selections),
        "candidate_rows": len(candidates),
        "contract_sha256": digest(CONTRACT),
        "contract_source_drifts": sources[2],
        "claim_boundary": {CLAIM_LOCAL_REPAIR: False, **false_claims()},
        "formalization_workbench_modified_file_count": 0,
        "updated_utc": utc_now(),
    }
    atomic_json(DIAGNOSTIC_RESULT, payload)
    atomic_json(
        STATUS,
        {
            "checkpoint": CHECKPOINT,
            "state": "candidates_selected" if passed else "candidate_blocked",
            "decision": payload["decision"],
            "updated_utc": payload["updated_utc"],
        },
    )
    render_document(payload)
    return payload


def classification_from_candidate(
    source: dict[str, str],
    node: dict[str, Any],
    summary: dict[str, Any],
) -> dict[str, Any]:
    refined = complex(summary["selected_payload"]["refined_pole"])
    residue = complex(summary["selected_payload"]["selected_residue"])
    return {
        **source,
        "node_id": node["node_id"],
        "x_panel_index": int(node["x_panel_index"]),
        "outer_order": int(node["outer_order"]),
        "absolute_soft_cosine": float(node["absolute_soft_cosine"]),
        "pole_real": refined.real,
        "pole_imaginary": refined.imag,
        **complex_fields("selected_residue", residue),
        "maximum_fit_relative_residual": summary["maximum_fit_relative_residual"],
        "fit_residue_relative_change": summary["residue_scale_relative_change"],
        "all_fit_samples_mask_active": True,
        "material_simple_pole": True,
        "removable_zero_residue_pole": False,
        "pole_classification_resolved": True,
        "failure_reason": "",
        "valid_for_pole_subtracted_outer_soft_node": True,
        "resolution_method": "SOURCE_SILENT_NORMALIZED_DOUBLE_LAURENT",
        "background_polynomial_degree": summary["background_degree"],
        "maximum_pole_refinements": summary["maximum_pole_refinements"],
        "second_order_suppression_ratio": summary[
            "second_order_suppression_ratio"
        ],
        "masked_identity_passes": summary["masked_identity_passes"],
        **false_claims(),
    }


def backup_failed_shards(nodes: list[dict[str, str]]) -> None:
    BACKUP_SHARDS.mkdir(parents=True, exist_ok=True)
    for node in nodes:
        source = M5312.shard_paths(node["node_id"])["root"]
        destination = BACKUP_SHARDS / node["node_id"]
        if not destination.exists():
            shutil.copytree(source, destination)


def write_near_support_evidence(
    node_ids: set[str],
    fit_rows: list[dict[str, Any]],
    identity_rows: list[dict[str, Any]],
) -> None:
    old_fits = (
        read_csv(M5326.NEAR_SUPPORT_FITS) if M5326.NEAR_SUPPORT_FITS.exists() else []
    )
    old_fits = [row for row in old_fits if row["node_id"] not in node_ids]
    M5326.write_csv(
        M5326.NEAR_SUPPORT_FITS,
        old_fits + fit_rows,
        ["node_id", "term_id", "pole_id", "fit_row_type", "fit_scale"],
    )
    old_identities = (
        read_csv(M5326.NEAR_SUPPORT_IDENTITIES)
        if M5326.NEAR_SUPPORT_IDENTITIES.exists()
        else []
    )
    old_identities = [row for row in old_identities if row["node_id"] not in node_ids]
    M5326.write_csv(
        M5326.NEAR_SUPPORT_IDENTITIES,
        old_identities + identity_rows,
        ["node_id", "term_id", "pole_id", "sample_index"],
    )


def repair_nodes(runtime_limit_seconds: float) -> dict[str, Any]:
    started = time.perf_counter()
    configure()
    contract, contract_sources = contract_is_current()
    diagnostic = read_json(DIAGNOSTIC_RESULT)
    if diagnostic.get("validation_passed") is not True or not SELECTIONS.is_file():
        raise RuntimeError("source-silent candidate diagnostic has not passed")
    if COMPARATOR_RESULT.exists():
        raise RuntimeError("refusing local repair after E020 holdout comparison")
    selections = read_csv(SELECTIONS)
    selection_by_key = {
        (row["node_id"], row["term_id"], row["pole_id"]): row
        for row in selections
    }
    failed = read_csv(PRE_MANIFEST)
    backup_failed_shards(failed)
    base_context = M5312.M5303.synthetic_context()
    multiplier = M5312.M5309.physical_multiplier()
    contract_rows = M5326.read_csv(M5326.CONTRACT_5325)
    expected_plan = str(M5326.read_json(M5326.DRY_RUN)["node_plan_sha256"])
    ledger: list[dict[str, Any]] = []
    all_fit_rows: list[dict[str, Any]] = []
    all_identity_rows: list[dict[str, Any]] = []
    for node in failed:
        node_id = node["node_id"]
        source_classifications = read_csv(
            BACKUP_SHARDS / node_id / "pole_classification.csv"
        )
        source_poles = read_csv(BACKUP_SHARDS / node_id / "geometric_poles.csv")
        replacements: dict[tuple[str, str], dict[str, Any]] = {}
        replacement_fits: list[dict[str, Any]] = []
        node_identity_rows: list[dict[str, Any]] = []
        node_summaries: list[dict[str, Any]] = []
        for source_classification in source_classifications:
            if parse_bool(source_classification["pole_classification_resolved"]):
                continue
            key = (
                node_id,
                source_classification["term_id"],
                source_classification["pole_id"],
            )
            selected_row = selection_by_key[key]
            pole = next(
                row
                for row in source_poles
                if row["term_id"] == key[1] and row["pole_id"] == key[2]
            )
            summary, fit_rows, identity_rows = candidate_for_pole(
                node,
                pole,
                int(selected_row["background_degree"]),
                int(selected_row["maximum_pole_refinements"]),
                base_context,
            )
            if not parse_bool(summary["candidate_passes"]):
                raise RuntimeError(f"frozen candidate no longer passes: {key}")
            for field in (
                "maximum_fit_relative_residual",
                "residue_scale_relative_change",
                "second_order_suppression_ratio",
            ):
                if not math.isclose(
                    float(summary[field]),
                    float(selected_row[field]),
                    rel_tol=1.0e-8,
                    abs_tol=1.0e-13,
                ):
                    raise RuntimeError(f"candidate drift for {key}: {field}")
            replacements[(key[1], key[2])] = classification_from_candidate(
                source_classification,
                node,
                summary,
            )
            replacement_fits.extend(fit_rows)
            node_identity_rows.extend(identity_rows)
            node_summaries.append(summary)
        old_fit_node_poles = M5312.fit_node_poles
        old_energy_panel_rows = M5312.energy_panel_rows

        def fit_all_unresolved_poles(
            local_node: dict[str, Any],
            poles: list[dict[str, Any]],
            evaluate: Any,
        ) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
            fits, classifications = old_fit_node_poles(local_node, poles, evaluate)
            if str(local_node["node_id"]) != node_id:
                return fits, classifications
            keys = set(replacements)
            fits = [
                row
                for row in fits
                if (str(row["term_id"]), str(row["pole_id"])) not in keys
            ]
            classifications = [
                row
                for row in classifications
                if (str(row["term_id"]), str(row["pole_id"])) not in keys
            ]
            fits.extend(replacement_fits)
            classifications.extend(replacements.values())
            return fits, classifications

        final: dict[str, Any] = {}
        chosen_subdivisions = -1
        try:
            M5312.fit_node_poles = fit_all_unresolved_poles
            for subdivisions in ENERGY_SUBDIVISION_LADDER:
                if subdivisions == 0:
                    M5312.energy_panel_rows = old_energy_panel_rows
                else:
                    M5312.energy_panel_rows = (
                        lambda local_node, cell, supports, classifications, count=subdivisions: M5326.refined_energy_panel_rows(
                            local_node,
                            cell,
                            supports,
                            classifications,
                            count,
                        )
                    )
                final = M5312.run_node(
                    node,
                    contract_rows,
                    expected_plan,
                    base_context,
                    multiplier,
                )
                chosen_subdivisions = subdivisions
                if bool(final["acceptance_passed"]):
                    break
        finally:
            M5312.fit_node_poles = old_fit_node_poles
            M5312.energy_panel_rows = old_energy_panel_rows
        final["source_silent_multipole_laurent_repair_applied"] = True
        final["source_silent_multipole_laurent_repair_revision"] = REPAIR_REVISION
        final["source_silent_repaired_pole_count"] = len(replacements)
        final["source_silent_background_degrees"] = sorted(
            {int(row["background_degree"]) for row in node_summaries}
        )
        final["source_silent_maximum_pole_refinements"] = sorted(
            {int(row["maximum_pole_refinements"]) for row in node_summaries}
        )
        final["source_silent_energy_panel_subdivisions"] = chosen_subdivisions
        M5326.atomic_json(M5312.shard_paths(node_id)["result"], final)
        node_passes = bool(final.get("acceptance_passed", False))
        maximum_fit = max(
            float(row["maximum_fit_relative_residual"]) for row in node_summaries
        )
        maximum_scale_change = max(
            float(row["residue_scale_relative_change"]) for row in node_summaries
        )
        maximum_second_order = max(
            float(row["second_order_suppression_ratio"]) for row in node_summaries
        )
        M5326.record_near_support_repair(
            {
                "node_id": node_id,
                "x_panel_index": node["x_panel_index"],
                "absolute_soft_cosine": node["absolute_soft_cosine"],
                "energy_panel_subdivisions": chosen_subdivisions,
                "near_support_candidate_found": True,
                "term_id": "|".join(sorted({row["term_id"] for row in node_summaries})),
                "primary_surface_id": "|".join(
                    sorted({row["primary_surface_id"] for row in node_summaries})
                ),
                "near_support_candidate_mode": "ALL_UNRESOLVED_MATERIAL_POLES",
                "near_support_side": "INSIDE_SUPPORT",
                "fit_relative_residual": maximum_fit,
                "residue_fit_scale_relative_change": maximum_scale_change,
                "second_order_suppression_ratio": maximum_second_order,
                "near_support_masked_identity_passes": all(
                    parse_bool(row["masked_identity_passes"]) for row in node_summaries
                ),
                "near_support_subtraction_contract_passes": all(
                    parse_bool(row["candidate_passes"]) for row in node_summaries
                ),
                "pre_repair_inner_Q4_Q8_relative_change": 0.0,
                "post_repair_inner_Q4_Q8_relative_change": final.get(
                    "inner_Q4_Q8_relative_change"
                ),
                "pre_repair_inner_energy_error_budget_relative": 0.0,
                "post_repair_inner_energy_error_budget_relative": final.get(
                    "inner_energy_error_budget_relative"
                ),
                "failure_reason": "" if node_passes else "REPAIRED_NODE_INNER_GATE_FAILED",
                "repair_acceptance_passed": node_passes,
                **false_claims(),
            }
        )
        ledger.append(
            {
                "node_id": node_id,
                "repaired_pole_count": len(replacements),
                "background_degrees": "|".join(
                    str(value)
                    for value in sorted(
                        {int(row["background_degree"]) for row in node_summaries}
                    )
                ),
                "maximum_pole_refinements": "|".join(
                    str(value)
                    for value in sorted(
                        {
                            int(row["maximum_pole_refinements"])
                            for row in node_summaries
                        }
                    )
                ),
                "energy_panel_subdivisions": chosen_subdivisions,
                "maximum_fit_relative_residual": maximum_fit,
                "maximum_residue_scale_relative_change": maximum_scale_change,
                "maximum_second_order_suppression_ratio": maximum_second_order,
                "post_repair_inner_Q4_Q8_relative_change": final.get(
                    "inner_Q4_Q8_relative_change"
                ),
                "post_repair_inner_error_budget_relative": final.get(
                    "inner_energy_error_budget_relative"
                ),
                "repair_acceptance_passed": node_passes,
                **false_claims(),
            }
        )
        all_fit_rows.extend(replacement_fits)
        all_identity_rows.extend(node_identity_rows)
    node_ids = {row["node_id"] for row in failed}
    write_near_support_evidence(node_ids, all_fit_rows, all_identity_rows)
    atomic_csv(REPAIR_LEDGER, ledger)
    atomic_csv(REPAIR_FITS, all_fit_rows)
    atomic_csv(REPAIR_IDENTITIES, all_identity_rows)
    local_passes = all(parse_bool(row["repair_acceptance_passed"]) for row in ledger)
    if local_passes:
        remaining_runtime = max(
            0.0,
            runtime_limit_seconds - (time.perf_counter() - started),
        )
        raw = M5326.execute(remaining_runtime)
        source_paths = {
            Path(row["path"])
            for row in raw.get("source_files", [])
            if Path(row["path"]).is_file()
        }
        source_paths.update(
            (
                Path(__file__).resolve(),
                CONTRACT,
                CONTRACT_VALIDATION,
                CONTRACT_SOURCES,
                DIAGNOSTIC_RESULT,
                CANDIDATES,
                SELECTIONS,
                REPAIR_LEDGER,
                REPAIR_FITS,
                REPAIR_IDENTITIES,
            )
        )
        raw["source_files"] = [
            {"path": str(path.resolve()), "sha256": digest(path)}
            for path in sorted(source_paths, key=lambda path: str(path).lower())
        ]
        measurement = M5334.canonicalize_refinement_result(raw)
    else:
        measurement = read_json(TARGET_RESULT)
    measurement_accepted = measurement.get("acceptance_passed") is True
    validation_payload: dict[str, Any] = {
        "acceptance_passed": False,
        "decision": "NOT_RUN",
    }
    if measurement_accepted:
        validation_payload = M5334.validate_refinement_outputs()
    validations = [
        validation_row(
            "frozen_repair_contract_remains_current",
            contract.get("validation_passed") is True and contract_sources[0],
            contract_sources[2],
        ),
        validation_row(
            "all_source_silent_local_pole_repairs_pass",
            local_passes,
            f"nodes={len(ledger)}",
        ),
        validation_row(
            "all_existing_numerical_thresholds_remain_unchanged",
            float(M5326.NEAR_SUPPORT_FIT_RELATIVE_RESIDUAL_LIMIT) == 1.0e-5
            and float(M5326.NEAR_SUPPORT_RESIDUE_SCALE_CHANGE_LIMIT) == 1.0e-3
            and float(M5326.NEAR_SUPPORT_SECOND_ORDER_SUPPRESSION_LIMIT) == 1.0e-4
            and float(M5326.NEAR_SUPPORT_MASKED_IDENTITY_LIMIT) == 1.0e-9,
            contract["unchanged_thresholds"],
        ),
        validation_row(
            "E020_measurement_is_accepted_and_source_validated",
            measurement_accepted
            and validation_payload.get("acceptance_passed") is True,
            measurement.get("decision"),
        ),
        validation_row(
            "holdout_comparison_remains_unexecuted_during_repair",
            not COMPARATOR_RESULT.exists(),
            COMPARATOR_RESULT,
        ),
        validation_row(
            "formal_workbench_unchanged",
            M5283.formal_inventory_digest() == FORMAL_DIGEST,
            M5283.formal_inventory_digest(),
        ),
        validation_row(
            "scripts_cache_absent",
            not (SCRIPTS / "__pycache__").exists(),
            SCRIPTS / "__pycache__",
        ),
    ]
    artifact_passed = all(parse_bool(row["passed"]) for row in validations)
    claims = {
        CLAIM_LOCAL_REPAIR: artifact_passed and local_passes,
        **false_claims(),
    }
    payload = {
        "checkpoint": CHECKPOINT,
        "marker": MARKER,
        "revision": REVISION,
        "mode": "D4-E020-source-silent-multipole-laurent-repair",
        "validation_passed": artifact_passed,
        "decision": (
            "D4_E020_SOURCE_SILENT_MULTIPOLE_REPAIR_ACCEPTED__RUN_FROZEN_HOLDOUT_COMPARISON"
            if artifact_passed
            else "D4_E020_SOURCE_SILENT_MULTIPOLE_REPAIR_INCOMPLETE__DO_NOT_COMPARE"
        ),
        "local_repair_node_count": len(ledger),
        "local_repairs_pass": local_passes,
        "measurement_acceptance_passed": measurement_accepted,
        "measurement_decision": measurement.get("decision"),
        "measurement_completed_node_count": measurement.get("completed_node_count"),
        "measurement_failed_inner_node_count": measurement.get(
            "failed_inner_node_count"
        ),
        "measurement_real": measurement.get("fixed_decay_integral_real"),
        "measurement_imaginary": measurement.get("fixed_decay_integral_imaginary"),
        "measurement_disk_radius": measurement.get(
            "total_error_absolute_conservative"
        ),
        "measurement_validation_decision": validation_payload.get("decision"),
        "claim_boundary": claims,
        "formalization_workbench_modified_file_count": 0,
        "runtime_seconds": time.perf_counter() - started,
        "updated_utc": utc_now(),
    }
    final_sources = tuple(
        path
        for path in (
            *contract_source_paths(),
            CONTRACT,
            CONTRACT_VALIDATION,
            CONTRACT_SOURCES,
            CANDIDATES,
            SELECTIONS,
            DIAGNOSTIC_RESULT,
            REPAIR_LEDGER,
            REPAIR_FITS,
            REPAIR_IDENTITIES,
            TARGET_RESULT,
            TARGET_FINITE,
        )
        if path.is_file()
    )
    source_rows = [
        {"path": str(path.resolve()), "sha256": digest(path), "exists": True, **claims}
        for path in dict.fromkeys(final_sources)
    ]
    atomic_csv(VALIDATION, validations)
    atomic_csv(RESIDUAL_VALIDATION, validations)
    atomic_csv(SOURCE_REGISTER, source_rows)
    atomic_json(RESULT, payload)
    atomic_json(
        STATUS,
        {
            "checkpoint": CHECKPOINT,
            "state": "complete" if artifact_passed else "repair_incomplete",
            "decision": payload["decision"],
            "updated_utc": payload["updated_utc"],
        },
    )
    render_document(payload)
    return payload


def validate_saved() -> dict[str, Any]:
    configure()
    required = (RESULT, VALIDATION, SOURCE_REGISTER, TARGET_RESULT, TARGET_FINITE)
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise FileNotFoundError(missing)
    result = read_json(RESULT)
    measurement = read_json(TARGET_RESULT)
    sources = source_register_current(SOURCE_REGISTER)
    contract_sources = source_register_current(CONTRACT_SOURCES)
    checks = {
        "saved_repair_result_passes": result.get("validation_passed") is True,
        "target_measurement_is_accepted": measurement.get("acceptance_passed") is True
        and measurement.get("failed_inner_node_count") == 0,
        "repair_validation_rows_pass": all(
            parse_bool(row["passed"]) for row in read_csv(VALIDATION)
        ),
        "repair_sources_are_current": sources[0] and sources[1] > 0,
        "frozen_contract_sources_are_current": contract_sources[0]
        and contract_sources[1] > 0,
        "broad_claims_remain_false": all(
            result.get("claim_boundary", {}).get(field) is False
            for field in FALSE_CLAIMS
        ),
        "formal_workbench_unchanged": M5283.formal_inventory_digest() == FORMAL_DIGEST,
        "scripts_cache_absent": not (SCRIPTS / "__pycache__").exists(),
    }
    return {
        "validation_passed": all(checks.values()),
        "decision": (
            "D4_E020_SOURCE_SILENT_MULTIPOLE_REPAIR_VALIDATED"
            if all(checks.values())
            else "D4_E020_SOURCE_SILENT_MULTIPOLE_REPAIR_VALIDATION_FAILED"
        ),
        "checks": checks,
        "source_drifts": sources[2],
        "contract_source_drifts": contract_sources[2],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        choices=("freeze", "diagnose", "repair", "validate"),
        required=True,
    )
    parser.add_argument("--max-runtime-hours", type=float, default=2.0)
    arguments = parser.parse_args()
    set_below_normal_priority()
    if arguments.mode == "freeze":
        payload = freeze_contract()
    elif arguments.mode == "diagnose":
        payload = diagnose_candidates()
    elif arguments.mode == "repair":
        payload = repair_nodes(max(0.0, arguments.max_runtime_hours) * 3600.0)
    else:
        payload = validate_saved()
    print(json.dumps(payload, indent=2, sort_keys=True, allow_nan=False))
    return 0 if payload.get("validation_passed") is True else 1


if __name__ == "__main__":
    raise SystemExit(main())
