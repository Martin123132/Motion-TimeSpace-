from __future__ import annotations

import csv
import importlib.util
import shutil
import sys
from pathlib import Path
from types import ModuleType


ROOT = Path(__file__).resolve().parents[1]
FORMALIZATION = ROOT.parent / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
MICROSCOPE = ROOT / "source-intake" / "microscope"
RAB_SECTOR = ROOT / "source-intake" / "rab-sector"
QUEUE = RAB_SECTOR / "acquisition-queue"
QUARANTINE = MICROSCOPE / "quarantine" / "1688"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1688-Y5-R2FR-action-measure-owner-source-search-or-qbar-bound-data-pack.md"
VALIDATOR_MODULE = ROOT / "scripts" / "qbar_source_weight_intake_validator_1685.py"

SOURCE_FILES = {
    "1687_doc": ROOT / "1687-Y5-R2FR-common-action-measure-current-owner-or-source-weight-bound-acquisition.md",
    "1687_validation": OUT / "P8_Y5_BRR545_1687_VALIDATION.csv",
    "1687_common_owner": OUT / "P8_Y5_PARENT_QLOC_1687_COMMON_ACTION_MEASURE_CURRENT_OWNER_PROOF_ATTEMPT.csv",
    "1687_bound_contract": OUT / "P8_Y5_PARENT_QLOC_1687_SOURCE_WEIGHT_BOUND_ACQUISITION_CONTRACT.csv",
    "1687_validator_result": OUT / "P8_Y5_PARENT_QLOC_1687_QBAR_VALIDATOR_RESULT.csv",
    "1685_validator_module": VALIDATOR_MODULE,
    "1389_doc": ROOT / "1389-Y5-R10-RAB-Delta-w-material-source-map-or-action-measure-owner-proof.md",
    "1389_owner": OUT / "P8_Y5_R10_1389_ACTION_MEASURE_OWNER_PROOF_ATTEMPT.csv",
    "1389_material_map": OUT / "P8_Y5_R10_1389_MATERIAL_SOURCE_CLASS_MAP.csv",
    "1390_doc": ROOT / "1390-Y5-R10-RAB-common-calibration-silence-or-first-material-coefficient-bound.md",
    "1390_silence": OUT / "P8_Y5_R10_1390_COMMON_CALIBRATION_SILENCE_PROOF.csv",
    "1390_bulk_rows": OUT / "P8_Y5_R10_1390_BULK_MATERIAL_COEFFICIENT_BOUND_ROWS.csv",
    "1391_doc": ROOT / "1391-Y5-R10-RAB-bulk-neutral-coefficient-source-pack-and-R10-kernel-gate.md",
    "1391_bulk_pack": OUT / "P8_Y5_R10_1391_BULK_NEUTRAL_COEFFICIENT_SOURCE_PACK.csv",
    "1391_kernel_gate": OUT / "P8_Y5_R10_1391_R10_BULK_MATERIAL_KERNEL_GATE.csv",
    "1391_runner_refusal": OUT / "P8_Y5_R10_1391_R10_RUNNER_REFUSAL_AUDIT.csv",
    "563_blockers": OUT / "P8_Y5_R10_563_BLOCKER_LEDGER.csv",
    "563_evaluator": OUT / "P8_Y5_R10_563_EVALUATOR.csv",
    "r10_anchor_bound": LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_ANCHOR_SMOKE.csv",
    "r10_live_bound": LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_DIGITIZED.csv",
}

NEEDLES = {
    "1687_doc": ["TARGET_ACTION_MEASURE_OWNER_SOURCE_SEARCH_OR_BOUND_DATA", "source-weight bound formulas are written", "1688-Y5-R2FR-action-measure-owner-source-search-or-qbar-bound-data-pack.md"],
    "1687_validation": ["VAL1687_OVERALL", "PASS"],
    "1687_common_owner": ["COM1687_6_verdict", "PROOF_NOT_CLOSED"],
    "1687_bound_contract": ["BND1687_5_verdict", "BOUND_CONTRACT_READY_INPUTS_MISSING_NONCLAIM"],
    "1687_validator_result": ["QVR1687_0", "PLACEHOLDER_OR_BLOCKED_FIELDS"],
    "1685_validator_module": ["def evaluate_qbar_source_weight_row", "REQUIRED_FIELDS"],
    "1389_doc": ["ACTION_MEASURE_OWNER_NOT_PARENT_SIGNED", "material/source classes"],
    "1389_owner": ["AMP1389_7_current_verdict", "ACTION_MEASURE_OWNER_NOT_PARENT_SIGNED"],
    "1389_material_map": ["MSC1389_0_bulk_neutral_baryonic", "MAP_READY_VALUE_MISSING"],
    "1390_doc": ["COMMON_SILENCE_NOT_PARENT_SIGNED", "BMB1390_6_bound_verdict"],
    "1390_silence": ["CCS1390_7_verdict", "COMMON_SILENCE_NOT_PARENT_SIGNED"],
    "1390_bulk_rows": ["BMB1390_6_bound_verdict", "BULK_BOUND_ROWS_READY_NONCLAIM"],
    "1391_doc": ["BULK_ZERO_NOT_PARENT_SIGNED", "R10_KERNEL_GATE_READY_SCORING_BLOCKED"],
    "1391_bulk_pack": ["BCP1391_7_pack_verdict", "BULK_SOURCE_PACK_READY_SCORING_BLOCKED"],
    "1391_kernel_gate": ["R10K1391_6_verdict", "R10_KERNEL_GATE_READY_SCORING_BLOCKED"],
    "1391_runner_refusal": ["RRF1391_3_verdict", "BLOCKED_NO_SCORE"],
    "563_blockers": ["B563_0_no_full_bound_curve", "B563_1_no_numeric_MTS_alpha"],
    "563_evaluator": ["E563_1_full_curve_missing", "E563_2_mts_parent_coefficients_missing"],
    "r10_anchor_bound": ["R10_ANCHOR_EOTWASH_2020_ALPHA1_38P6UM", "anchor_only_non_curve_from_alpha_equals_1_threshold_statement"],
    "r10_live_bound": ["R10_BOUND_PLACEHOLDER_0", "MISSING_DIGITIZED_ALPHA_BOUND"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1688_SOURCE_REGISTER.csv"
OWNER_SOURCE_SEARCH = OUT / "P8_Y5_PARENT_QLOC_1688_ACTION_MEASURE_OWNER_SOURCE_SEARCH.csv"
BOUND_ROUTE_SELECTION = OUT / "P8_Y5_PARENT_QLOC_1688_QBAR_BOUND_ROUTE_SELECTION.csv"
R10_DATA_PACK = OUT / "P8_Y5_PARENT_QLOC_1688_R10_BULK_BOUND_DATA_PACK.csv"
QBAR_CANDIDATE = OUT / "P8_Y5_PARENT_QLOC_1688_QBAR_R10_BULK_CANDIDATE_NONCLAIM.csv"
QBAR_VALIDATOR_RESULT = OUT / "P8_Y5_PARENT_QLOC_1688_QBAR_VALIDATOR_RESULT.csv"
GATE_STATUS = OUT / "P8_Y5_PARENT_QLOC_1688_GATE_STATUS.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1688_DECISION.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1688_CLAIM_GATE.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1688_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1688_VALIDATION.csv"

GENERATED = [
    SOURCE_REGISTER,
    OWNER_SOURCE_SEARCH,
    BOUND_ROUTE_SELECTION,
    R10_DATA_PACK,
    QBAR_CANDIDATE,
    QBAR_VALIDATOR_RESULT,
    GATE_STATUS,
    DECISION,
    CLAIM_GATE,
    NEXT_TARGET,
]

CLAIM_CHECKED = [
    OWNER_SOURCE_SEARCH,
    BOUND_ROUTE_SELECTION,
    R10_DATA_PACK,
    QBAR_CANDIDATE,
    QBAR_VALIDATOR_RESULT,
    GATE_STATUS,
    DECISION,
    CLAIM_GATE,
    NEXT_TARGET,
]

COPY_TARGETS = {
    OWNER_SOURCE_SEARCH: [
        QUARANTINE / "ACTION_MEASURE_OWNER_SOURCE_SEARCH.csv",
        BRANCH_RESIDUALS / "R2FR_action_measure_owner_source_search_1688.csv",
        QUEUE / "JR1688_ACTION_MEASURE_OWNER_SOURCE_SEARCH.csv",
    ],
    BOUND_ROUTE_SELECTION: [
        QUARANTINE / "QBAR_BOUND_ROUTE_SELECTION.csv",
        BRANCH_RESIDUALS / "R2FR_qbar_bound_route_selection_1688.csv",
        QUEUE / "JR1688_QBAR_BOUND_ROUTE_SELECTION.csv",
    ],
    R10_DATA_PACK: [
        QUARANTINE / "R10_BULK_BOUND_DATA_PACK.csv",
        BRANCH_RESIDUALS / "R2FR_R10_bulk_bound_data_pack_1688.csv",
        QUEUE / "JR1688_R10_BULK_BOUND_DATA_PACK.csv",
    ],
    QBAR_VALIDATOR_RESULT: [
        QUARANTINE / "QBAR_VALIDATOR_RESULT.csv",
        BRANCH_RESIDUALS / "R2FR_qbar_validator_result_1688.csv",
        QUEUE / "JR1688_QBAR_VALIDATOR_RESULT.csv",
    ],
    NEXT_TARGET: [
        QUARANTINE / "NEXT_TARGET_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_next_target_nonclaim_1688.csv",
        QUEUE / "JR1688_NEXT_TARGET_NONCLAIM.csv",
    ],
}

SCORE_FLAGS = [
    "source_found",
    "route_selected",
    "data_pack_ready",
    "row_pass",
    "gate_pass",
    "accepted_for_scoring",
    "score_ready",
    "valid_prediction_row",
    "valid_for_claim",
    "claim_allowed",
]


def ensure_dirs() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    BRANCH_RESIDUALS.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def bool_cell(value: object) -> bool:
    return str(value).strip().lower() == "true"


def blocked_marker(value: object) -> bool:
    text = str(value)
    markers = [
        "MISSING_",
        "NOT_",
        "BLOCKED",
        "REJECT",
        "FAIL",
        "UNSIGNED",
        "NO_SCORE",
        "NONCLAIM",
        "PLACEHOLDER",
        "ANCHOR_ONLY",
    ]
    return any(marker in text for marker in markers)


def list_cell(value: object) -> str:
    if isinstance(value, (list, tuple, set)):
        return ";".join(str(item) for item in value)
    if isinstance(value, dict):
        return ";".join(f"{key}={item}" for key, item in sorted(value.items()))
    return str(value)


def load_validator() -> ModuleType:
    sys.dont_write_bytecode = True
    spec = importlib.util.spec_from_file_location("qbar_source_weight_intake_validator_1685", VALIDATOR_MODULE)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load validator module: {VALIDATOR_MODULE}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def source_register_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for source_key, source_path in SOURCE_FILES.items():
        exists = source_path.exists()
        body = read_text(source_path) if exists else ""
        needles_present = all(needle in body for needle in NEEDLES[source_key])
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_key": source_key,
                "source_path": str(source_path),
                "exists": exists,
                "needles_present": needles_present,
                "required_needles": "; ".join(NEEDLES[source_key]),
                "use_in_1688": "action-measure owner source search or qbar/R10 bound data pack",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def owner_source_search_rows() -> list[dict[str, object]]:
    rows = [
        (
            "OSS1688_0_1687",
            "1687 common owner proof",
            "COM1687_6_verdict",
            "PROOF_NOT_CLOSED",
            "Hilbert/current subtheorem retained, but pre-variation weights and measure owner remain open",
            "not a source signing action-measure ownership",
        ),
        (
            "OSS1688_1_1389",
            "1389 action-measure owner proof",
            "AMP1389_7_current_verdict",
            "ACTION_MEASURE_OWNER_NOT_PARENT_SIGNED",
            "exact conditional theorem exists but object-language/action-measure/connectedness/silence do not close together",
            "not a source signing action-measure ownership",
        ),
        (
            "OSS1688_2_1390",
            "1390 common calibration silence",
            "CCS1390_7_verdict",
            "COMMON_SILENCE_NOT_PARENT_SIGNED",
            "common factor is harmless only if parent-signed as one global constant",
            "not a source signing derivative silence",
        ),
        (
            "OSS1688_3_1391",
            "1391 bulk zero theorem",
            "BZT1391_5_current_verdict",
            "BULK_ZERO_NOT_PARENT_SIGNED",
            "bulk universality, binding inheritance, beta zero, and tail silence remain unsigned",
            "not a source signing bulk zero",
        ),
        (
            "OSS1688_4_verdict",
            "local corpus source search verdict",
            "this checkpoint",
            "NO_PARENT_ACTION_MEASURE_OWNER_SOURCE_FOUND",
            "no inspected source signs hbar/action-measure ownership strongly enough to set qbar_source_weight theorem-zero",
            "finite bound data pack selected",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "search_id": search_id,
            "source_or_route": source_or_route,
            "anchor": anchor,
            "status": status,
            "meaning": meaning,
            "next_action": next_action,
            "source_found": False,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for search_id, source_or_route, anchor, status, meaning, next_action in rows
    ]


def bound_route_selection_rows() -> list[dict[str, object]]:
    rows = [
        (
            "BRS1688_0_WEP",
            "WEP/MICROSCOPE",
            "eta_bound available in older rows, but tau/material/source denominator still not filled",
            "not selected first",
            "needs orbit/readout/material tensor before qbar denominator can be numeric",
        ),
        (
            "BRS1688_1_R10",
            "R10 bulk neutral",
            "1391 already defines source leg, test leg, K(lambda), tail, and alpha_bound(lambda) gate; anchor bound files exist",
            "SELECTED_FIRST_FINITE_DATA_ROUTE",
            "closest path to a comparator-compatible qbar/R10 alpha row, though both theory side and full curve are still incomplete",
        ),
        (
            "BRS1688_2_Newton_GM",
            "Newton/GM",
            "common measured-G calibration and source composition contrast remain unsigned",
            "not selected first",
            "risk of hiding source weights in measured G unless silence theorem closes",
        ),
        (
            "BRS1688_3_PPN",
            "PPN/local GR",
            "weak-field residual vector and denominator rank missing",
            "not selected first",
            "too many upstream geometric/source gates remain open",
        ),
        (
            "BRS1688_4_verdict",
            "route selection verdict",
            "R10 bulk neutral selected as the first finite qbar bound data pack route",
            "ROUTE_SELECTED_NONCLAIM",
            "selected for discipline/plumbing only, not for R10 evidence",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": route_id,
            "arena": arena,
            "available_evidence": available_evidence,
            "selection_status": selection_status,
            "reason": reason,
            "route_selected": selection_status == "SELECTED_FIRST_FINITE_DATA_ROUTE",
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for route_id, arena, available_evidence, selection_status, reason in rows
    ]


def r10_data_pack_rows() -> list[dict[str, object]]:
    rows = [
        (
            "RDP1688_0_force_law",
            "R10 alpha convention",
            "alpha_bulk,ST(lambda)=K_bulk,ST(lambda) beta_bulk,S beta_bulk,T + epsilon_tail(lambda)",
            "schema from 1391",
            "SCHEMA_READY",
            "valid alpha prediction shape exists, but values are missing",
        ),
        (
            "RDP1688_1_source_leg",
            "beta_bulk,S",
            "bulk source beta leg or theorem-zero certificate",
            "BCP1391_2_beta_bulk_source",
            "MISSING_SOURCE_LEG",
            "no sourced beta or zero theorem",
        ),
        (
            "RDP1688_2_test_leg",
            "beta_bulk,T",
            "bulk test beta leg or theorem-zero certificate",
            "BCP1391_3_beta_bulk_test",
            "MISSING_TEST_LEG",
            "no sourced beta or zero theorem",
        ),
        (
            "RDP1688_3_kernel",
            "K_bulk,ST(lambda)",
            "finite-size/profile/source-test geometry kernel",
            "BCP1391_4_K_bulk_ST;R10K1391_3_profile_kernel",
            "MISSING_PROFILE_KERNEL",
            "no source/test geometry or lambda convention",
        ),
        (
            "RDP1688_4_tail",
            "epsilon_tail(lambda)",
            "tail theorem-zero or conservative envelope",
            "BCP1391_5_epsilon_tail",
            "MISSING_TAIL_BOUND",
            "no tail theorem or bound",
        ),
        (
            "RDP1688_5_bound_anchor",
            "R10 alpha_bound(lambda) anchor",
            "alpha=1 at lambda=38.6 um from 2020 Eot-Wash source hierarchy; alpha=1 at 56 um from 2007 continuity anchor",
            "R10_alpha_lambda_bound_curve_ANCHOR_SMOKE.csv",
            "ANCHOR_ONLY_NONCLAIM_AVAILABLE",
            "useful provenance and plumbing only, not a full curve",
        ),
        (
            "RDP1688_6_live_curve",
            "R10 full bound curve",
            "dense positive numeric alpha_bound(lambda) curve or official machine-readable table",
            "R10_alpha_lambda_bound_curve_DIGITIZED.csv;B563_0_no_full_bound_curve",
            "MISSING_FULL_DIGITIZED_CURVE",
            "live curve remains placeholder invalid",
        ),
        (
            "RDP1688_7_verdict",
            "R10 bulk data pack",
            "all theory-side alpha legs and external bound curve must be numeric/sourced before validator pass",
            "RRF1391_3_verdict;E563_1_full_curve_missing;E563_2_mts_parent_coefficients_missing",
            "DATA_PACK_READY_SCORING_BLOCKED",
            "selected data pack is real scaffolding but not evidence",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "pack_id": pack_id,
            "data_leg": data_leg,
            "formula_or_requirement": formula_or_requirement,
            "source_anchor": source_anchor,
            "current_status": current_status,
            "notes": notes,
            "data_pack_ready": current_status in {"SCHEMA_READY", "ANCHOR_ONLY_NONCLAIM_AVAILABLE"},
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for pack_id, data_leg, formula_or_requirement, source_anchor, current_status, notes in rows
    ]


def qbar_candidate_rows(validator: ModuleType) -> list[dict[str, object]]:
    row = {
        "branch_id": BRANCH_ID,
        "candidate_id": "CAND1688_0_R10_bulk_qbar_bound_data_pack_candidate",
        "basis_component": "qbar_source_weight",
        "coefficient_symbol": "zeta_source_weight_I",
        "accepted_form": "R10 bulk finite source-weight bound via alpha_bulk,ST(lambda) or theorem-zero action-measure owner",
        "theorem_route_status": "NOT_PARENT_SIGNED",
        "finite_route_status": "NOT_FILLED",
        "source_label_forgetting_status": "NOT_DERIVED",
        "ordinary_matter_connectedness_status": "NOT_DERIVED",
        "value_or_bound": "MISSING_NUMERIC_QBAR_R10_BULK_BOUND",
        "uncertainty": "MISSING_BOUND_UNCERTAINTY",
        "sign_convention": "absolute envelope bound; R10 alpha product sign not claimed",
        "material_or_source_tags": "bulk_neutral_R10_source;bulk_neutral_R10_test;MISSING_MATERIAL_PAIR",
        "lambda_or_domain_if_range_dependent": "anchor lambda 3.86e-5 m exists nonclaim; full lambda curve missing",
        "parent_basis_X_I": "MISSING_PARENT_BASIS_X_I",
        "normalization": "MISSING_CANONICAL_PHI_AND_QBAR_NORMALIZATION",
        "units": "dimensionless qbar envelope; alpha dimensionless; lambda m",
        "coordinate_dimension": "MISSING_COORDINATE_DIMENSION",
        "common_mode_measured_G_convention": "MISSING_COMMON_MODE_MEASURED_G_CONVENTION",
        "local_source_path": str(R10_DATA_PACK),
        "source_anchor": "RDP1688_7_verdict",
        "derivation_or_data_method": "R10 bulk data pack selected; theory legs and full curve missing",
        "confidence": "route selection high; numeric bound unavailable",
        "extraction_status": "DATA_PACK_READY_SCORING_BLOCKED_NONCLAIM",
        "WEP_tau_material_worldtube": "MISSING_WEP_TAU_MATERIAL_WORLDTUBE",
        "R10_lambda_alpha_projection": "MISSING_R10_BETA_SOURCE_TEST_KERNEL_TAIL_AND_FULL_CURVE",
        "Newton_GM_calibration": "MISSING_NEWTON_GM_CALIBRATION",
        "R11_operator_projection": "MISSING_R11_OPERATOR_PROJECTION",
        "PPN_local_GR_projection": "MISSING_PPN_LOCAL_GR_PROJECTION",
        "accepted_for_scoring": False,
        "score_ready": False,
        "valid_prediction_row": False,
        "valid_for_claim": False,
        "claim_allowed": False,
    }
    return [{field: row.get(field, "") for field in validator.REQUIRED_FIELDS}]


def validator_result_rows(validator: ModuleType, candidates: list[dict[str, object]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for candidate in candidates:
        result = validator.evaluate_qbar_source_weight_row(candidate, root=ROOT)
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "result_id": f"QVR1688_{len(rows)}",
                "candidate_id": candidate["candidate_id"],
                "row_pass": result["row_pass"],
                "reason": result["reason"],
                "route": result["route"],
                "route_ok": result["route_ok"],
                "placeholder_fields": list_cell(result["placeholder_fields"]),
                "numeric_failures": list_cell(result["numeric_failures"]),
                "source_path_exists": result["source_path_exists"],
                "resolved_source_path": result["resolved_source_path"],
                "claim_safety_violation": result["claim_safety_violation"],
                "accepted_for_scoring": False,
                "score_ready": False,
                "valid_prediction_row": False,
                "valid_for_claim": result["valid_for_claim"],
                "claim_allowed": result["claim_allowed"],
            }
        )
    return rows


def gate_status_rows(
    owner_rows: list[dict[str, object]],
    route_rows: list[dict[str, object]],
    data_rows: list[dict[str, object]],
    validator_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    owner_found = any(bool_cell(row["source_found"]) for row in owner_rows)
    route_selected = any(row["route_id"] == "BRS1688_1_R10" and bool_cell(row["route_selected"]) for row in route_rows)
    hard_missing = [row for row in data_rows if str(row["current_status"]).startswith("MISSING_") or "BLOCKED" in str(row["current_status"])]
    validator_pass = any(bool_cell(row["row_pass"]) for row in validator_rows)
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GST1688_0_owner_source",
            "gate": "action-measure owner source search",
            "current_status": "NO_PARENT_OWNER_SOURCE_FOUND" if not owner_found else "UNEXPECTED_OWNER_SOURCE_FOUND",
            "gate_pass": False,
            "reason": "inspected sources keep owner theorem conditional/unsigned",
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GST1688_1_route_selection",
            "gate": "finite qbar bound route selection",
            "current_status": "R10_BULK_SELECTED_NONCLAIM" if route_selected else "NO_ROUTE_SELECTED",
            "gate_pass": False,
            "reason": "R10 bulk route is selected for data plumbing only, not scoring",
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GST1688_2_R10_data_pack",
            "gate": "R10 bulk data pack completeness",
            "current_status": "DATA_PACK_INCOMPLETE" if hard_missing else "UNEXPECTED_DATA_PACK_COMPLETE",
            "gate_pass": False,
            "reason": "beta source/test, K(lambda), tail, and full alpha bound curve remain missing",
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GST1688_3_qbar_validator",
            "gate": "1685 qbar intake validator",
            "current_status": "ACTIVE_REJECTS_1688_CANDIDATE" if not validator_pass else "UNEXPECTED_VALIDATOR_PASS",
            "gate_pass": False,
            "reason": "candidate is route-selected but still lacks numeric bound/value, parent basis, and arena projection fields",
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def decision_rows() -> list[dict[str, object]]:
    rows = [
        ("D1688_0_owner", "NO_ACTION_MEASURE_OWNER_SOURCE_FOUND", "local corpus search finds exact conditional owner theorems but no parent-signed source", "do not set qbar_source_weight=0"),
        ("D1688_1_route", "R10_BULK_SELECTED_AS_FIRST_FINITE_ROUTE", "1391 already exposes theory legs, R10 kernel gate, and external bound-curve blockers", "use R10 bulk as the first qbar bound data pack"),
        ("D1688_2_bound", "ANCHOR_ONLY_BOUND_NOT_ENOUGH", "Eot-Wash anchor rows are provenance, not a dense alpha(lambda) curve", "digitize/source full curve before R10 scoring"),
        ("D1688_3_theory", "MTS_ALPHA_LEGS_MISSING", "beta source/test, K(lambda), epsilon tail, material pair, and parent basis are not filled", "fill theory-side alpha template before comparator claim"),
        ("D1688_4_next", "TARGET_BULK_ALPHA_TEMPLATE_OR_FULL_CURVE_DIGITIZATION", "next useful move is theory-side alpha template or full external curve acquisition", "move to 1689"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": decision_id,
            "decision": decision,
            "reason": reason,
            "next_action": next_action,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for decision_id, decision, reason, next_action in rows
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    rows = [
        ("CG1688_0_owner_zero", "qbar_source_weight theorem-zero", "BLOCKED", "no parent action-measure owner source found"),
        ("CG1688_1_R10_bound_curve", "external R10 full bound curve", "BLOCKED", "only anchor smoke rows and invalid placeholders exist"),
        ("CG1688_2_MTS_alpha", "MTS R10 bulk alpha prediction", "BLOCKED", "beta source/test, K, tail, material pair, and parent basis missing"),
        ("CG1688_3_qbar_validator", "qbar validator pass", "BLOCKED", "1688 candidate rejected"),
        ("CG1688_4_R10_score", "R10 score/pass", "BLOCKED", "both prediction and bound curve are nonclaim"),
        ("CG1688_5_local_claim", "local GR/Newton/PPN/WEP/R10 source-side claim", "BLOCKED", "finite route is data plumbing only"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "gate": gate,
            "gate_pass": False,
            "status": status,
            "reason": reason,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for gate_id, gate, status, reason in rows
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "next_target": "1689-Y5-R2FR-bulk-alpha-template-beta-kernel-tail-fill-or-r10-curve-digitization.md",
            "script": "scripts/Y5_R2FR_bulk_alpha_template_beta_kernel_tail_fill_or_r10_curve_digitization.py",
            "objective": "either build a strict nonclaim bulk alpha(lambda) template with beta source/test, K(lambda), epsilon tail, lambda units, and material pair, or acquire a full R10 alpha(lambda) bound curve from source-backed digitization",
            "success_condition": "one side of the R10 comparator becomes validator-ready without placeholders while the opposite side remains explicitly nonclaim if still missing",
            "why_next": "1688 selects the finite route; the next blocker is whether to fill MTS theory-side alpha first or the external full curve first",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def copy_outputs() -> None:
    for source_path, target_paths in COPY_TARGETS.items():
        for target_path in target_paths:
            target_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_path, target_path)


def validate(
    source_rows: list[dict[str, object]],
    owner_rows: list[dict[str, object]],
    route_rows: list[dict[str, object]],
    data_rows: list[dict[str, object]],
    candidate_rows_: list[dict[str, object]],
    validator_rows: list[dict[str, object]],
    gate_rows: list[dict[str, object]],
    decisions: list[dict[str, object]],
    claims: list[dict[str, object]],
    next_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    sources_ok = all(bool_cell(row["exists"]) and bool_cell(row["needles_present"]) for row in source_rows)
    owner_not_found = any(row["search_id"] == "OSS1688_4_verdict" and row["status"] == "NO_PARENT_ACTION_MEASURE_OWNER_SOURCE_FOUND" for row in owner_rows) and all(not bool_cell(row["source_found"]) for row in owner_rows)
    r10_selected = any(row["route_id"] == "BRS1688_1_R10" and bool_cell(row["route_selected"]) for row in route_rows)
    selected_nonclaim = all(not bool_cell(row["score_ready"]) and not bool_cell(row["valid_for_claim"]) for row in route_rows)
    data_pack_has_anchor = any(row["pack_id"] == "RDP1688_5_bound_anchor" and row["current_status"] == "ANCHOR_ONLY_NONCLAIM_AVAILABLE" for row in data_rows)
    data_pack_blocks = any(row["pack_id"] == "RDP1688_7_verdict" and row["current_status"] == "DATA_PACK_READY_SCORING_BLOCKED" for row in data_rows)
    full_curve_missing = any(row["pack_id"] == "RDP1688_6_live_curve" and row["current_status"] == "MISSING_FULL_DIGITIZED_CURVE" for row in data_rows)
    theory_legs_missing = all(any(status in row["current_status"] for status in ["MISSING_SOURCE_LEG", "MISSING_TEST_LEG", "MISSING_PROFILE_KERNEL", "MISSING_TAIL_BOUND"]) for row in data_rows if row["pack_id"] in {"RDP1688_1_source_leg", "RDP1688_2_test_leg", "RDP1688_3_kernel", "RDP1688_4_tail"})
    candidate_nonclaim = len(candidate_rows_) == 1 and candidate_rows_[0]["candidate_id"] == "CAND1688_0_R10_bulk_qbar_bound_data_pack_candidate" and not bool_cell(candidate_rows_[0]["valid_for_claim"])
    validator_rejects = len(validator_rows) == 1 and not bool_cell(validator_rows[0]["row_pass"]) and "PLACEHOLDER_OR_BLOCKED_FIELDS" in validator_rows[0]["reason"]
    source_path_used = len(validator_rows) == 1 and bool_cell(validator_rows[0]["source_path_exists"])
    gate_locked = all(not bool_cell(row["gate_pass"]) for row in gate_rows)
    decision_safe = any(row["decision"] == "TARGET_BULK_ALPHA_TEMPLATE_OR_FULL_CURVE_DIGITIZATION" for row in decisions)
    claim_gate_safe = all(not bool_cell(row["gate_pass"]) and not bool_cell(row["claim_allowed"]) for row in claims)
    next_target_selected = next_rows[0]["next_target"] == "1689-Y5-R2FR-bulk-alpha-template-beta-kernel-tail-fill-or-r10-curve-digitization.md"
    csv_parse = all(path.exists() and len(read_csv(path)) >= 1 for path in GENERATED)
    branch_copies = all(target_path.exists() for target_paths in COPY_TARGETS.values() for target_path in target_paths)
    pycache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    formalization_clean = not any(FORMALIZATION.rglob("*1688*")) if FORMALIZATION.exists() else True

    no_claim_flags = True
    blocked_not_ready = True
    for generated_path in CLAIM_CHECKED:
        for generated_row in read_csv(generated_path):
            if generated_row.get("valid_for_claim", "False").lower() == "true" or generated_row.get("claim_allowed", "False").lower() == "true":
                no_claim_flags = False
            if any(blocked_marker(value) for value in generated_row.values()):
                for claim_key in SCORE_FLAGS:
                    if claim_key in generated_row and bool_cell(generated_row[claim_key]):
                        if claim_key == "route_selected":
                            continue
                        if claim_key == "data_pack_ready" and generated_row.get("current_status") in {"SCHEMA_READY", "ANCHOR_ONLY_NONCLAIM_AVAILABLE"}:
                            continue
                        blocked_not_ready = False

    checks = [
        ("VAL1688_0_sources_exist", sources_ok, "all cited 1688 source paths exist and required needles are present"),
        ("VAL1688_1_owner_not_found", owner_not_found, "no parent action-measure owner source found"),
        ("VAL1688_2_R10_selected", r10_selected, "R10 bulk selected as first finite route"),
        ("VAL1688_3_selection_nonclaim", selected_nonclaim, "route selection remains nonclaim/non-scoreable"),
        ("VAL1688_4_anchor_available", data_pack_has_anchor, "source-backed R10 anchor rows are available only as nonclaim"),
        ("VAL1688_5_data_pack_blocks", data_pack_blocks, "R10 data pack records scoring blocked"),
        ("VAL1688_6_full_curve_missing", full_curve_missing, "full digitized R10 alpha curve missing"),
        ("VAL1688_7_theory_legs_missing", theory_legs_missing, "MTS beta/kernel/tail theory legs missing"),
        ("VAL1688_8_candidate_nonclaim", candidate_nonclaim, "qbar R10 candidate remains nonclaim"),
        ("VAL1688_9_validator_rejects", validator_rejects, "1685 validator rejects 1688 candidate"),
        ("VAL1688_10_source_path_used", source_path_used, "candidate points to existing R10 data pack"),
        ("VAL1688_11_gate_locked", gate_locked, "all gates remain locked"),
        ("VAL1688_12_decision_safe", decision_safe, "decision selects bulk alpha template or full curve digitization"),
        ("VAL1688_13_claim_gate_safe", claim_gate_safe, "all claim gates remain false"),
        ("VAL1688_14_no_claim_flags", no_claim_flags, "all generated rows keep claim flags false"),
        ("VAL1688_15_blocked_not_ready", blocked_not_ready, "no blocked/missing row is marked claim/scoring ready"),
        ("VAL1688_16_next_target_selected", next_target_selected, "next target selects bulk alpha template or R10 curve digitization"),
        ("VAL1688_17_csv_parse", csv_parse, "all generated 1688 CSVs parse"),
        ("VAL1688_18_branch_copies", branch_copies, "branch/quarantine/queue copies exist"),
        ("VAL1688_19_pycache_absent", pycache_absent, "scripts __pycache__ absent"),
        ("VAL1688_20_formalization_untouched", formalization_clean, "no 1688 outputs found under formalization-workbench"),
    ]
    overall = all(result for _, result, _ in checks)
    validation_rows = [
        {
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for check_id, result, detail in checks
    ]
    validation_rows.append(
        {
            "check_id": "VAL1688_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1688 action-measure owner source search or qbar bound data pack validation",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    return validation_rows


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join(["---"] * len(columns)) + " |"
    table_rows = []
    for row in rows:
        table_rows.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return "\n".join([header, separator, *table_rows])


def write_doc(
    source_rows: list[dict[str, object]],
    owner_rows: list[dict[str, object]],
    route_rows: list[dict[str, object]],
    data_rows: list[dict[str, object]],
    candidate_rows_: list[dict[str, object]],
    validator_rows: list[dict[str, object]],
    gate_rows: list[dict[str, object]],
    decision_rows_: list[dict[str, object]],
    claim_rows: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    validation_rows: list[dict[str, object]],
) -> None:
    body = f"""# 1688 - Action-Measure Owner Source Search Or Qbar Bound Data Pack

**Private status:** owner-source search plus finite qbar/R10 data-pack checkpoint. No `q_loc=0`, local-GR pass, Newton pass, PPN pass, WEP pass, R10 pass, R11 pass, clock pass, orbital pass, or public claim is made.

## Verdict

The action-measure owner source search does not find a parent-signed theorem. The local corpus has exact conditional owner theorems, but not a source that signs the object-language, hbar/action-measure, connectedness, current-owner, and derivative-silence clauses together. So `qbar_source_weight=0` is still not claimed.

The finite route is now concretely selected: use the R10 bulk-neutral path first. That path already has a bulk coefficient pack and R10 kernel gate from 1391, plus source-backed Eot-Wash anchor rows from 563. But it is still not evidence: the MTS side lacks beta source/test legs, `K(lambda)`, tail bounds, material pair, and parent basis; the external side lacks a full digitized alpha(lambda) curve.

## Source Register

{markdown_table(source_rows, ["source_key", "source_path", "exists", "needles_present", "use_in_1688"])}

## Owner Source Search

{markdown_table(owner_rows, ["search_id", "source_or_route", "anchor", "status", "meaning"])}

## Bound Route Selection

{markdown_table(route_rows, ["route_id", "arena", "selection_status", "available_evidence", "reason"])}

## R10 Bulk Bound Data Pack

{markdown_table(data_rows, ["pack_id", "data_leg", "formula_or_requirement", "current_status", "notes"])}

## Qbar Candidate

{markdown_table(candidate_rows_, ["candidate_id", "basis_component", "coefficient_symbol", "finite_route_status", "value_or_bound", "R10_lambda_alpha_projection", "valid_for_claim"])}

## Validator Result

{markdown_table(validator_rows, ["result_id", "candidate_id", "row_pass", "reason", "route", "source_path_exists", "claim_safety_violation"])}

## Gate Status

{markdown_table(gate_rows, ["gate_id", "gate", "current_status", "gate_pass", "reason"])}

## Decisions

{markdown_table(decision_rows_, ["decision_id", "decision", "reason", "next_action"])}

## Claim Gates

{markdown_table(claim_rows, ["gate_id", "gate", "gate_pass", "status", "reason"])}

## Next Target

{markdown_table(next_rows, ["next_target", "script", "objective", "success_condition"])}

## Validation

{markdown_table(validation_rows, ["check_id", "result", "detail"])}

## Working Interpretation

1688 turns the vague finite fallback into a specific road. We either fill the MTS-side bulk alpha template, or acquire/digitize the full R10 bound curve. Both are useful, but neither allows a local/R10 claim until the validator sees numeric, sourced, non-placeholder rows.
"""
    DOC.write_text(body, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    validator = load_validator()
    source_rows = source_register_rows()
    owner_rows = owner_source_search_rows()
    route_rows = bound_route_selection_rows()
    data_rows = r10_data_pack_rows()

    write_csv(SOURCE_REGISTER, source_rows, ["branch_id", "source_key", "source_path", "exists", "needles_present", "required_needles", "use_in_1688", "valid_for_claim", "claim_allowed"])
    write_csv(OWNER_SOURCE_SEARCH, owner_rows, ["branch_id", "search_id", "source_or_route", "anchor", "status", "meaning", "next_action", "source_found", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"])
    write_csv(BOUND_ROUTE_SELECTION, route_rows, ["branch_id", "route_id", "arena", "available_evidence", "selection_status", "reason", "route_selected", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"])
    write_csv(R10_DATA_PACK, data_rows, ["branch_id", "pack_id", "data_leg", "formula_or_requirement", "source_anchor", "current_status", "notes", "data_pack_ready", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"])

    candidates = qbar_candidate_rows(validator)
    validator_rows = validator_result_rows(validator, candidates)
    gate_rows = gate_status_rows(owner_rows, route_rows, data_rows, validator_rows)
    decisions = decision_rows()
    claims = claim_gate_rows()
    next_rows = next_target_rows()

    write_csv(QBAR_CANDIDATE, candidates, list(validator.REQUIRED_FIELDS))
    write_csv(QBAR_VALIDATOR_RESULT, validator_rows, ["branch_id", "result_id", "candidate_id", "row_pass", "reason", "route", "route_ok", "placeholder_fields", "numeric_failures", "source_path_exists", "resolved_source_path", "claim_safety_violation", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"])
    write_csv(GATE_STATUS, gate_rows, ["branch_id", "gate_id", "gate", "current_status", "gate_pass", "reason", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"])
    write_csv(DECISION, decisions, ["branch_id", "decision_id", "decision", "reason", "next_action", "valid_for_claim", "claim_allowed"])
    write_csv(CLAIM_GATE, claims, ["branch_id", "gate_id", "gate", "gate_pass", "status", "reason", "valid_for_claim", "claim_allowed"])
    write_csv(NEXT_TARGET, next_rows, ["branch_id", "next_target", "script", "objective", "success_condition", "why_next", "valid_for_claim", "claim_allowed"])

    copy_outputs()
    validation_rows = validate(source_rows, owner_rows, route_rows, data_rows, candidates, validator_rows, gate_rows, decisions, claims, next_rows)
    write_csv(VALIDATION, validation_rows, ["check_id", "result", "detail", "valid_for_claim", "claim_allowed"])
    write_doc(source_rows, owner_rows, route_rows, data_rows, candidates, validator_rows, gate_rows, decisions, claims, next_rows, validation_rows)

    failed_rows = [row for row in validation_rows if row["result"] != "PASS"]
    print(f"wrote {DOC}")
    print(f"wrote {VALIDATION}")
    if failed_rows:
        for failed_row in failed_rows:
            print(f"FAIL {failed_row['check_id']}: {failed_row['detail']}")
        raise SystemExit(1)
    print("1688 validation PASS")


if __name__ == "__main__":
    main()
