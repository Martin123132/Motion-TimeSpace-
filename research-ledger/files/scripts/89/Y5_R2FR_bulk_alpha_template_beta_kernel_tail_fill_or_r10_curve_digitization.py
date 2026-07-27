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
QUARANTINE = MICROSCOPE / "quarantine" / "1689"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1689-Y5-R2FR-bulk-alpha-template-beta-kernel-tail-fill-or-r10-curve-digitization.md"
VALIDATOR_MODULE = ROOT / "scripts" / "qbar_source_weight_intake_validator_1685.py"

SOURCE_FILES = {
    "1688_doc": ROOT / "1688-Y5-R2FR-action-measure-owner-source-search-or-qbar-bound-data-pack.md",
    "1688_validation": OUT / "P8_Y5_BRR545_1688_VALIDATION.csv",
    "1688_data_pack": OUT / "P8_Y5_PARENT_QLOC_1688_R10_BULK_BOUND_DATA_PACK.csv",
    "1688_route": OUT / "P8_Y5_PARENT_QLOC_1688_QBAR_BOUND_ROUTE_SELECTION.csv",
    "1688_qbar_result": OUT / "P8_Y5_PARENT_QLOC_1688_QBAR_VALIDATOR_RESULT.csv",
    "1685_validator_module": VALIDATOR_MODULE,
    "1392_doc": ROOT / "1392-Y5-R10-RAB-bulk-alpha-template-beta-kernel-tail-fill-or-zero-proof.md",
    "1392_zero": OUT / "P8_Y5_R10_1392_BETA_KERNEL_TAIL_ZERO_ATTEMPT.csv",
    "1392_template_register": OUT / "P8_Y5_R10_1392_BULK_ALPHA_TEMPLATE_REGISTER.csv",
    "1392_template": OUT / "R10_alpha_lambda_curve_MTS_1392_BULK_ALPHA_TEMPLATE_NONCLAIM.csv",
    "1392_runner": OUT / "P8_Y5_R10_1392_R10_RUNNER_SMOKE_SUMMARY.csv",
    "1392_validation": OUT / "P8_Y5_BRR545_1392_VALIDATION.csv",
    "1391_pack": OUT / "P8_Y5_R10_1391_BULK_NEUTRAL_COEFFICIENT_SOURCE_PACK.csv",
    "1391_kernel_gate": OUT / "P8_Y5_R10_1391_R10_BULK_MATERIAL_KERNEL_GATE.csv",
    "563_blockers": OUT / "P8_Y5_R10_563_BLOCKER_LEDGER.csv",
    "563_evaluator": OUT / "P8_Y5_R10_563_EVALUATOR.csv",
    "r10_anchor_bound": LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_ANCHOR_SMOKE.csv",
    "r10_live_bound": LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_DIGITIZED.csv",
}

NEEDLES = {
    "1688_doc": ["TARGET_BULK_ALPHA_TEMPLATE_OR_FULL_CURVE_DIGITIZATION", "MTS_ALPHA_LEGS_MISSING", "1689-Y5-R2FR-bulk-alpha-template-beta-kernel-tail-fill-or-r10-curve-digitization.md"],
    "1688_validation": ["VAL1688_OVERALL", "PASS"],
    "1688_data_pack": ["RDP1688_7_verdict", "DATA_PACK_READY_SCORING_BLOCKED"],
    "1688_route": ["BRS1688_1_R10", "SELECTED_FIRST_FINITE_DATA_ROUTE"],
    "1688_qbar_result": ["QVR1688_0", "PLACEHOLDER_OR_BLOCKED_FIELDS"],
    "1685_validator_module": ["def evaluate_qbar_source_weight_row", "REQUIRED_FIELDS"],
    "1392_doc": ["alpha_bulk,ST(lambda)=0", "PASS_NONCLAIM_TEMPLATE"],
    "1392_zero": ["BKT1392_5_current_verdict", "ZERO_PROOF_UNSIGNED_TEMPLATE_REQUIRED"],
    "1392_template_register": ["ATR1392_0_schema", "RUNNER_COMPATIBLE_SCHEMA"],
    "1392_template": ["R10_alpha_lambda_curve_MTS_1392_BULK_ALPHA_TEMPLATE_NONCLAIM", "K_bulk_ST(lambda)*beta_bulk_S*beta_bulk_T+epsilon_tail(lambda)"],
    "1392_runner": ["RUN1392_0_anchor_smoke", "R10_pass_for_claim"],
    "1392_validation": ["VAL1392_6_overall", "PASS"],
    "1391_pack": ["BCP1391_7_pack_verdict", "BULK_SOURCE_PACK_READY_SCORING_BLOCKED"],
    "1391_kernel_gate": ["R10K1391_6_verdict", "R10_KERNEL_GATE_READY_SCORING_BLOCKED"],
    "563_blockers": ["B563_0_no_full_bound_curve", "B563_1_no_numeric_MTS_alpha"],
    "563_evaluator": ["E563_1_full_curve_missing", "E563_2_mts_parent_coefficients_missing"],
    "r10_anchor_bound": ["R10_ANCHOR_EOTWASH_2020_ALPHA1_38P6UM", "anchor_only_non_curve_from_alpha_equals_1_threshold_statement"],
    "r10_live_bound": ["R10_BOUND_PLACEHOLDER_0", "MISSING_DIGITIZED_ALPHA_BOUND"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1689_SOURCE_REGISTER.csv"
ZERO_OR_TEMPLATE_AUDIT = OUT / "P8_Y5_PARENT_QLOC_1689_BULK_ALPHA_ZERO_OR_TEMPLATE_AUDIT.csv"
BULK_ALPHA_TEMPLATE = OUT / "R10_alpha_lambda_curve_MTS_1689_BULK_ALPHA_TEMPLATE_NONCLAIM.csv"
BULK_ALPHA_TEMPLATE_SOURCE_ALIAS = OUT / "R10_alpha_lambda_curve_MTS_1689_BULK_ALPHA_TEMPLATE_SOURCE.csv"
TEMPLATE_BRIDGE = OUT / "P8_Y5_PARENT_QLOC_1689_BULK_ALPHA_TEMPLATE_BRIDGE.csv"
CURVE_DIGITIZATION_STATUS = OUT / "P8_Y5_PARENT_QLOC_1689_R10_CURVE_DIGITIZATION_STATUS.csv"
COMPARATOR_READINESS = OUT / "P8_Y5_PARENT_QLOC_1689_COMPARATOR_READINESS_MATRIX.csv"
QBAR_CANDIDATE = OUT / "P8_Y5_PARENT_QLOC_1689_QBAR_BULK_ALPHA_CANDIDATE_NONCLAIM.csv"
QBAR_VALIDATOR_RESULT = OUT / "P8_Y5_PARENT_QLOC_1689_QBAR_VALIDATOR_RESULT.csv"
GATE_STATUS = OUT / "P8_Y5_PARENT_QLOC_1689_GATE_STATUS.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1689_DECISION.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1689_CLAIM_GATE.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1689_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1689_VALIDATION.csv"

GENERATED = [
    SOURCE_REGISTER,
    ZERO_OR_TEMPLATE_AUDIT,
    BULK_ALPHA_TEMPLATE,
    BULK_ALPHA_TEMPLATE_SOURCE_ALIAS,
    TEMPLATE_BRIDGE,
    CURVE_DIGITIZATION_STATUS,
    COMPARATOR_READINESS,
    QBAR_CANDIDATE,
    QBAR_VALIDATOR_RESULT,
    GATE_STATUS,
    DECISION,
    CLAIM_GATE,
    NEXT_TARGET,
]

CLAIM_CHECKED = [
    ZERO_OR_TEMPLATE_AUDIT,
    BULK_ALPHA_TEMPLATE,
    BULK_ALPHA_TEMPLATE_SOURCE_ALIAS,
    TEMPLATE_BRIDGE,
    CURVE_DIGITIZATION_STATUS,
    COMPARATOR_READINESS,
    QBAR_CANDIDATE,
    QBAR_VALIDATOR_RESULT,
    GATE_STATUS,
    DECISION,
    CLAIM_GATE,
    NEXT_TARGET,
]

COPY_TARGETS = {
    ZERO_OR_TEMPLATE_AUDIT: [
        QUARANTINE / "BULK_ALPHA_ZERO_OR_TEMPLATE_AUDIT.csv",
        BRANCH_RESIDUALS / "R2FR_bulk_alpha_zero_or_template_audit_1689.csv",
        QUEUE / "JR1689_BULK_ALPHA_ZERO_OR_TEMPLATE_AUDIT.csv",
    ],
    BULK_ALPHA_TEMPLATE: [
        QUARANTINE / "R10_alpha_lambda_curve_MTS_1689_BULK_ALPHA_TEMPLATE_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R10_alpha_lambda_curve_MTS_1689_BULK_ALPHA_TEMPLATE_NONCLAIM.csv",
        QUEUE / "JR1689_R10_ALPHA_TEMPLATE_NONCLAIM.csv",
    ],
    BULK_ALPHA_TEMPLATE_SOURCE_ALIAS: [
        QUARANTINE / "R10_alpha_lambda_curve_MTS_1689_BULK_ALPHA_TEMPLATE_SOURCE.csv",
        BRANCH_RESIDUALS / "R10_alpha_lambda_curve_MTS_1689_BULK_ALPHA_TEMPLATE_SOURCE.csv",
        QUEUE / "JR1689_R10_ALPHA_TEMPLATE_SOURCE.csv",
    ],
    TEMPLATE_BRIDGE: [
        QUARANTINE / "BULK_ALPHA_TEMPLATE_BRIDGE.csv",
        BRANCH_RESIDUALS / "R2FR_bulk_alpha_template_bridge_1689.csv",
        QUEUE / "JR1689_BULK_ALPHA_TEMPLATE_BRIDGE.csv",
    ],
    COMPARATOR_READINESS: [
        QUARANTINE / "COMPARATOR_READINESS_MATRIX.csv",
        BRANCH_RESIDUALS / "R2FR_comparator_readiness_matrix_1689.csv",
        QUEUE / "JR1689_COMPARATOR_READINESS_MATRIX.csv",
    ],
    QBAR_VALIDATOR_RESULT: [
        QUARANTINE / "QBAR_VALIDATOR_RESULT.csv",
        BRANCH_RESIDUALS / "R2FR_qbar_validator_result_1689.csv",
        QUEUE / "JR1689_QBAR_VALIDATOR_RESULT.csv",
    ],
    NEXT_TARGET: [
        QUARANTINE / "NEXT_TARGET_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_next_target_nonclaim_1689.csv",
        QUEUE / "JR1689_NEXT_TARGET_NONCLAIM.csv",
    ],
}

SCORE_FLAGS = [
    "zero_signed",
    "template_ready",
    "curve_ready",
    "comparator_ready",
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
        "SYMBOLIC",
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
                "use_in_1689": "bulk alpha template bridge, beta/kernel/tail audit, and R10 curve digitization status",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def zero_or_template_audit_rows() -> list[dict[str, object]]:
    rows = [
        (
            "ZTA1689_0_beta_source",
            "beta_bulk,S=0",
            "bulk source leg inherits common ordinary-matter owner and has no independent binding/source marker",
            "CONDITIONAL_ZERO_ROUTE",
            "common owner, binding inheritance, and source material composition are not parent-signed",
            "keep beta_bulk,S as explicit factor",
        ),
        (
            "ZTA1689_1_beta_test",
            "beta_bulk,T=0",
            "bulk test leg inherits same ordinary-matter owner and has no independent readout/material marker",
            "CONDITIONAL_ZERO_ROUTE",
            "test material composition and binding/readout inheritance remain unsigned",
            "keep beta_bulk,T as explicit factor",
        ),
        (
            "ZTA1689_2_kernel",
            "K_bulk,ST(lambda) finite and convention locked",
            "profile kernel is finite-size/source-test correction, not a free alpha parameter",
            "KERNEL_SCHEMA_READY_NOT_FILLED",
            "source/test geometry, density profile, and lambda convention are not filled",
            "keep K_bulk,ST(lambda) required",
        ),
        (
            "ZTA1689_3_tail",
            "epsilon_tail(lambda)=0",
            "all nonbulk, boundary, binding, and projection leakage terms vanish or are separately bounded",
            "TAIL_ZERO_NOT_SIGNED",
            "tail channels are not theorem-zero and no conservative envelope exists",
            "keep epsilon_tail(lambda) required",
        ),
        (
            "ZTA1689_4_alpha_zero",
            "alpha_bulk,ST(lambda)=0",
            "if beta_bulk,S=0, beta_bulk,T=0, and epsilon_tail(lambda)=0, then alpha_bulk,ST(lambda)=0 for finite K",
            "EXACT_CONDITIONAL_ZERO",
            "zero premises unsigned",
            "zero certificate shape only",
        ),
        (
            "ZTA1689_5_verdict",
            "bulk alpha route",
            "bridge 1392 exact conditional/template into current 1688 qbar route",
            "ZERO_PROOF_UNSIGNED_TEMPLATE_REQUIRED",
            "beta source/test, K(lambda), tail, and full bound curve are still not claim-ready",
            "write current nonclaim template and qbar validator result",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "audit_id": audit_id,
            "target": target,
            "attempted_derivation": attempted_derivation,
            "current_result": current_result,
            "gap": gap,
            "template_consequence": template_consequence,
            "zero_signed": False,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for audit_id, target, attempted_derivation, current_result, gap, template_consequence in rows
    ]


def bulk_alpha_template_rows() -> list[dict[str, object]]:
    base_rows = read_csv(SOURCE_FILES["1392_template"])
    rows: list[dict[str, object]] = []
    for index, base_row in enumerate(base_rows):
        rows.append(
            {
                "model_id": "MTS_source_normalized_Newton_branch",
                "branch_id": "R10_bulk_neutral_beta_kernel_tail_template_R2FR_1689",
                "curve_id": "R10_alpha_lambda_curve_MTS_1689_BULK_ALPHA_TEMPLATE_NONCLAIM",
                "lambda_units": base_row["lambda_units"],
                "alpha_predicted": base_row["alpha_predicted"],
                "alpha_bound": base_row["alpha_bound"],
                "force_law_form": base_row["force_law_form"],
                "derivation_status": "symbolic_bulk_alpha_template_nonclaim_zero_premises_unsigned_R2FR_1689",
                "formula_reference": f"{DOC.name}::alpha_bulk_ST(lambda)=K_bulk_ST(lambda) beta_bulk_S beta_bulk_T + epsilon_tail(lambda)",
                "source_file": str(DOC),
                "assumptions": base_row["assumptions"],
                "valid_for_claim": False,
                "beta_source_handle": base_row["beta_source_handle"],
                "beta_test_handle": base_row["beta_test_handle"],
                "K_lambda_handle": base_row["K_lambda_handle"],
                "epsilon_tail_handle": base_row["epsilon_tail_handle"],
                "material_pair": base_row["material_pair"],
                "blocking_inputs": base_row["blocking_inputs"],
                "lambda_value": base_row["lambda_value"],
                "alpha_bound_source": base_row["alpha_bound_source"],
                "notes": f"1689 bridge row {index}; inherited from 1392 template; still symbolic and nonclaim.",
            }
        )
    return rows


def template_bridge_rows(template_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    required_columns = {
        "model_id",
        "branch_id",
        "curve_id",
        "lambda_units",
        "alpha_predicted",
        "alpha_bound",
        "force_law_form",
        "derivation_status",
        "formula_reference",
        "source_file",
        "assumptions",
        "valid_for_claim",
        "lambda_value",
    }
    columns_ok = all(required_columns.issubset(row.keys()) for row in template_rows)
    factors_exposed = all(row.get("beta_source_handle") and row.get("beta_test_handle") and row.get("K_lambda_handle") and row.get("epsilon_tail_handle") for row in template_rows)
    all_nonclaim = all(not bool_cell(row["valid_for_claim"]) for row in template_rows)
    symbolic_alpha = any("beta_bulk" in str(row["alpha_predicted"]) or "K_bulk" in str(row["alpha_predicted"]) for row in template_rows)
    rows = [
        ("TBR1689_0_schema", "runner columns", columns_ok, "template has R10 runner-compatible columns"),
        ("TBR1689_1_factors", "factor exposure", factors_exposed, "beta source/test, K(lambda), tail, and material pair are exposed"),
        ("TBR1689_2_nonclaim", "claim flags", all_nonclaim, "all rows keep valid_for_claim=false"),
        ("TBR1689_3_symbolic", "symbolic alpha", symbolic_alpha, "alpha_predicted is symbolic, so runner must reject claims"),
        ("TBR1689_4_verdict", "current-side readiness", columns_ok and factors_exposed and all_nonclaim and symbolic_alpha, "current side is shape-ready but not value-ready"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "bridge_id": bridge_id,
            "check": check,
            "check_pass": check_pass,
            "detail": detail,
            "template_ready": bool(check_pass),
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for bridge_id, check, check_pass, detail in rows
    ]


def curve_digitization_rows() -> list[dict[str, object]]:
    rows = [
        (
            "CDS1689_0_anchor_2020",
            "Eot-Wash 2020 alpha=1 threshold",
            "lambda=3.86e-5 m, alpha_bound=1",
            "ANCHOR_ONLY_NONCLAIM",
            str(SOURCE_FILES["r10_anchor_bound"]),
            "source-backed provenance, not full curve",
        ),
        (
            "CDS1689_1_anchor_2007",
            "Eot-Wash 2007 alpha=1 threshold",
            "lambda=5.6e-5 m, alpha_bound=1",
            "ANCHOR_ONLY_NONCLAIM",
            str(SOURCE_FILES["r10_anchor_bound"]),
            "continuity provenance, not full curve",
        ),
        (
            "CDS1689_2_live_curve",
            "live digitized alpha(lambda) curve",
            "positive numeric lambda and alpha_bound rows over required range",
            "MISSING_FULL_DIGITIZED_CURVE",
            str(SOURCE_FILES["r10_live_bound"]),
            "placeholder rows remain invalid",
        ),
        (
            "CDS1689_3_claim_requirement",
            "R10 external curve claim requirement",
            "full digitized/source-backed alpha(lambda) curve or official machine-readable table",
            "CURVE_REQUIRED_BEFORE_R10_SCORE",
            "B563_0_no_full_bound_curve;E563_1_full_curve_missing",
            "anchor rows can only smoke-test plumbing",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "curve_id": curve_id,
            "object": obj,
            "data_or_requirement": data_or_requirement,
            "current_status": current_status,
            "source_path_or_anchor": source_path_or_anchor,
            "notes": notes,
            "curve_ready": False,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for curve_id, obj, data_or_requirement, current_status, source_path_or_anchor, notes in rows
    ]


def comparator_readiness_rows(template_rows: list[dict[str, object]], curve_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    template_shape_ready = len(template_rows) >= 1
    template_value_ready = all(str(row["alpha_predicted"]).replace(".", "", 1).replace("-", "", 1).isdigit() and bool_cell(row["valid_for_claim"]) for row in template_rows)
    curve_ready = any(bool_cell(row["curve_ready"]) for row in curve_rows)
    rows = [
        ("CR1689_0_MTS_shape", "MTS alpha row shape", template_shape_ready, "template rows exist and are runner-shaped"),
        ("CR1689_1_MTS_value", "MTS alpha numeric/claim value", template_value_ready, "alpha_predicted remains symbolic and valid_for_claim=false"),
        ("CR1689_2_external_curve", "external bound curve", curve_ready, "full digitized alpha(lambda) curve missing"),
        ("CR1689_3_comparator", "R10 comparator readiness", template_value_ready and curve_ready, "both MTS numeric alpha and external full curve are required"),
        ("CR1689_4_verdict", "R10 scoring", False, "R10 score remains blocked by symbolic MTS alpha and missing full curve"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "readiness_id": readiness_id,
            "component": component,
            "component_ready": component_ready,
            "detail": detail,
            "comparator_ready": False,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for readiness_id, component, component_ready, detail in rows
    ]


def qbar_candidate_rows(validator: ModuleType) -> list[dict[str, object]]:
    row = {
        "branch_id": BRANCH_ID,
        "candidate_id": "CAND1689_0_bulk_alpha_template_qbar_candidate",
        "basis_component": "qbar_source_weight",
        "coefficient_symbol": "zeta_source_weight_I",
        "accepted_form": "R10 bulk alpha template alpha_bulk,ST(lambda)=K beta_S beta_T + epsilon_tail",
        "theorem_route_status": "NOT_PARENT_SIGNED",
        "finite_route_status": "NOT_FILLED",
        "source_label_forgetting_status": "NOT_DERIVED",
        "ordinary_matter_connectedness_status": "NOT_DERIVED",
        "value_or_bound": "MISSING_NUMERIC_QBAR_OR_ALPHA_BOUND",
        "uncertainty": "MISSING_BOUND_UNCERTAINTY",
        "sign_convention": "absolute envelope / alpha product sign not claimed",
        "material_or_source_tags": "bulk_neutral_source__bulk_neutral_test",
        "lambda_or_domain_if_range_dependent": "3.86e-5 m and 5.6e-5 m anchor-aligned nonclaim rows; full curve missing",
        "parent_basis_X_I": "MISSING_PARENT_BASIS_X_I",
        "normalization": "MISSING_CANONICAL_PHI_AND_QBAR_NORMALIZATION",
        "units": "dimensionless qbar envelope; alpha dimensionless; lambda m",
        "coordinate_dimension": "MISSING_COORDINATE_DIMENSION",
        "common_mode_measured_G_convention": "MISSING_COMMON_MODE_MEASURED_G_CONVENTION",
        "local_source_path": str(BULK_ALPHA_TEMPLATE_SOURCE_ALIAS),
        "source_anchor": "TBR1689_4_verdict",
        "derivation_or_data_method": "runner-shaped symbolic template inherited from 1392 and bridged to 1689",
        "confidence": "schema high; numeric claim value unavailable",
        "extraction_status": "SYMBOLIC_TEMPLATE_NONCLAIM",
        "WEP_tau_material_worldtube": "MISSING_WEP_TAU_MATERIAL_WORLDTUBE",
        "R10_lambda_alpha_projection": "SYMBOLIC_ALPHA_TEMPLATE_BETA_K_TAIL_MISSING_FULL_CURVE",
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
                "result_id": f"QVR1689_{len(rows)}",
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
    audit_rows: list[dict[str, object]],
    bridge_rows: list[dict[str, object]],
    curve_rows: list[dict[str, object]],
    readiness_rows: list[dict[str, object]],
    validator_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    zero_signed = any(bool_cell(row["zero_signed"]) for row in audit_rows)
    template_ready = any(row["bridge_id"] == "TBR1689_4_verdict" and bool_cell(row["template_ready"]) for row in bridge_rows)
    curve_ready = any(bool_cell(row["curve_ready"]) for row in curve_rows)
    comparator_ready = any(bool_cell(row["comparator_ready"]) for row in readiness_rows)
    validator_pass = any(bool_cell(row["row_pass"]) for row in validator_rows)
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GST1689_0_zero",
            "gate": "bulk beta/kernel/tail zero proof",
            "current_status": "ZERO_PROOF_UNSIGNED" if not zero_signed else "UNEXPECTED_ZERO_SIGNED",
            "gate_pass": False,
            "reason": "beta source/test and tail-zero premises remain unsigned",
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GST1689_1_template",
            "gate": "bulk alpha template shape",
            "current_status": "RUNNER_SHAPED_NONCLAIM_TEMPLATE" if template_ready else "TEMPLATE_MISSING",
            "gate_pass": False,
            "reason": "template is shape-ready but alpha is symbolic and claim flags false",
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GST1689_2_curve",
            "gate": "full R10 bound curve",
            "current_status": "FULL_CURVE_MISSING" if not curve_ready else "UNEXPECTED_CURVE_READY",
            "gate_pass": False,
            "reason": "external R10 rows are anchor-only or placeholders",
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GST1689_3_comparator",
            "gate": "R10 comparator readiness",
            "current_status": "COMPARATOR_BLOCKED" if not comparator_ready else "UNEXPECTED_COMPARATOR_READY",
            "gate_pass": False,
            "reason": "MTS alpha not numeric/claim-valid and external curve missing",
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GST1689_4_qbar_validator",
            "gate": "1685 qbar intake validator",
            "current_status": "ACTIVE_REJECTS_1689_CANDIDATE" if not validator_pass else "UNEXPECTED_VALIDATOR_PASS",
            "gate_pass": False,
            "reason": "qbar candidate is symbolic and lacks numeric bound/projection fields",
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def decision_rows() -> list[dict[str, object]]:
    rows = [
        ("D1689_0_zero", "BULK_ALPHA_ZERO_NOT_SIGNED", "exact alpha-zero condition exists but beta source/test and tail-zero premises are unsigned", "do not claim R10/local pass"),
        ("D1689_1_template", "RUNNER_SHAPED_TEMPLATE_BRIDGED", "1392 template is copied into current 1689 route with factor exposure and nonclaim flags", "use it as plumbing only"),
        ("D1689_2_curve", "FULL_R10_CURVE_STILL_MISSING", "anchor rows are source-backed but not a full alpha(lambda) bound curve", "curve digitization remains a separate blocker"),
        ("D1689_3_next_priority", "BETA_SOURCE_TEST_CONVENTION_FIRST", "without beta source/test convention, a full curve cannot test MTS alpha", "move to 1690 beta source/test convention"),
        ("D1689_4_claim", "CLAIMS_BLOCKED", "MTS side and external curve side are both nonclaim", "no R10/Newton/PPN/WEP/local-GR claim"),
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
        ("CG1689_0_zero", "bulk alpha theorem-zero", "BLOCKED", "beta source/test and tail-zero premises unsigned"),
        ("CG1689_1_MTS_alpha", "MTS bulk alpha numeric row", "BLOCKED", "alpha_predicted is symbolic"),
        ("CG1689_2_curve", "external full R10 bound curve", "BLOCKED", "full digitized curve missing"),
        ("CG1689_3_qbar", "qbar validator pass", "BLOCKED", "1689 qbar candidate rejected"),
        ("CG1689_4_R10", "R10 comparator score", "BLOCKED", "both comparator sides are nonclaim"),
        ("CG1689_5_local", "local GR/Newton/WEP/PPN source-side claim", "BLOCKED", "1689 is template plumbing, not a derived local reduction"),
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
            "next_target": "1690-Y5-R2FR-beta-bulk-source-test-convention-or-r10-curve-first-digitization.md",
            "script": "scripts/Y5_R2FR_beta_bulk_source_test_convention_or_r10_curve_first_digitization.py",
            "objective": "derive or source the beta_bulk source/test convention first; if that stalls, create a full R10 curve digitization work order with figure/source provenance and no claim promotion",
            "success_condition": "beta_bulk,S and beta_bulk,T become theorem-zero/source-backed nonclaim rows, or the external curve acquisition workflow produces validated full-curve rows with claim flags still false until MTS alpha is numeric",
            "why_next": "1689 shows the current-side template exists, but beta source/test convention is the first theory-side blocker before R10 scoring",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def copy_outputs() -> None:
    for source_path, target_paths in COPY_TARGETS.items():
        for target_path in target_paths:
            target_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_path, target_path)


def cleanup_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def validate(
    source_rows: list[dict[str, object]],
    audit_rows: list[dict[str, object]],
    template_rows: list[dict[str, object]],
    bridge_rows: list[dict[str, object]],
    curve_rows: list[dict[str, object]],
    readiness_rows: list[dict[str, object]],
    candidate_rows_: list[dict[str, object]],
    validator_rows: list[dict[str, object]],
    gate_rows: list[dict[str, object]],
    decisions: list[dict[str, object]],
    claims: list[dict[str, object]],
    next_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    sources_ok = all(bool_cell(row["exists"]) and bool_cell(row["needles_present"]) for row in source_rows)
    zero_unsigned = any(row["audit_id"] == "ZTA1689_5_verdict" and row["current_result"] == "ZERO_PROOF_UNSIGNED_TEMPLATE_REQUIRED" for row in audit_rows) and all(not bool_cell(row["zero_signed"]) for row in audit_rows)
    template_rows_written = len(template_rows) == 2 and all(str(row["curve_id"]) == "R10_alpha_lambda_curve_MTS_1689_BULK_ALPHA_TEMPLATE_NONCLAIM" for row in template_rows)
    template_nonclaim = all(not bool_cell(row["valid_for_claim"]) for row in template_rows)
    template_symbolic = all("beta_bulk" in str(row["alpha_predicted"]) and "epsilon_tail" in str(row["alpha_predicted"]) for row in template_rows)
    bridge_ready = any(row["bridge_id"] == "TBR1689_4_verdict" and bool_cell(row["template_ready"]) for row in bridge_rows)
    curve_missing = any(row["curve_id"] == "CDS1689_2_live_curve" and row["current_status"] == "MISSING_FULL_DIGITIZED_CURVE" for row in curve_rows)
    anchor_nonclaim = any(row["current_status"] == "ANCHOR_ONLY_NONCLAIM" for row in curve_rows)
    comparator_blocked = any(row["readiness_id"] == "CR1689_4_verdict" and not bool_cell(row["comparator_ready"]) for row in readiness_rows)
    candidate_nonclaim = len(candidate_rows_) == 1 and candidate_rows_[0]["candidate_id"] == "CAND1689_0_bulk_alpha_template_qbar_candidate" and not bool_cell(candidate_rows_[0]["valid_for_claim"])
    validator_rejects = len(validator_rows) == 1 and not bool_cell(validator_rows[0]["row_pass"]) and "PLACEHOLDER_OR_BLOCKED_FIELDS" in validator_rows[0]["reason"]
    source_path_used = len(validator_rows) == 1 and bool_cell(validator_rows[0]["source_path_exists"])
    gate_locked = all(not bool_cell(row["gate_pass"]) for row in gate_rows)
    decision_safe = any(row["decision"] == "BETA_SOURCE_TEST_CONVENTION_FIRST" for row in decisions)
    claim_gate_safe = all(not bool_cell(row["gate_pass"]) and not bool_cell(row["claim_allowed"]) for row in claims)
    next_target_selected = next_rows[0]["next_target"] == "1690-Y5-R2FR-beta-bulk-source-test-convention-or-r10-curve-first-digitization.md"
    csv_parse = all(path.exists() and len(read_csv(path)) >= 1 for path in GENERATED)
    branch_copies = all(target_path.exists() for target_paths in COPY_TARGETS.values() for target_path in target_paths)
    pycache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    formalization_clean = not any(FORMALIZATION.rglob("*1689*")) if FORMALIZATION.exists() else True

    no_claim_flags = True
    blocked_not_ready = True
    for generated_path in CLAIM_CHECKED:
        for generated_row in read_csv(generated_path):
            if generated_row.get("valid_for_claim", "False").lower() == "true" or generated_row.get("claim_allowed", "False").lower() == "true":
                no_claim_flags = False
            if any(blocked_marker(value) for value in generated_row.values()):
                for claim_key in SCORE_FLAGS:
                    if claim_key in generated_row and bool_cell(generated_row[claim_key]):
                        if claim_key == "template_ready" and generated_row.get("bridge_id") in {"TBR1689_0_schema", "TBR1689_1_factors", "TBR1689_2_nonclaim", "TBR1689_3_symbolic", "TBR1689_4_verdict"}:
                            continue
                        blocked_not_ready = False

    checks = [
        ("VAL1689_0_sources_exist", sources_ok, "all cited 1689 source paths exist and required needles are present"),
        ("VAL1689_1_zero_unsigned", zero_unsigned, "bulk alpha zero route remains unsigned"),
        ("VAL1689_2_template_rows_written", template_rows_written, "1689 template rows are written"),
        ("VAL1689_3_template_nonclaim", template_nonclaim, "template rows remain nonclaim"),
        ("VAL1689_4_template_symbolic", template_symbolic, "template alpha is symbolic and factor-exposing"),
        ("VAL1689_5_bridge_ready", bridge_ready, "template is runner-shaped but nonclaim"),
        ("VAL1689_6_curve_missing", curve_missing, "full R10 digitized curve remains missing"),
        ("VAL1689_7_anchor_nonclaim", anchor_nonclaim, "anchor rows remain nonclaim provenance"),
        ("VAL1689_8_comparator_blocked", comparator_blocked, "R10 comparator remains blocked"),
        ("VAL1689_9_candidate_nonclaim", candidate_nonclaim, "qbar candidate remains nonclaim"),
        ("VAL1689_10_validator_rejects", validator_rejects, "1685 validator rejects 1689 candidate"),
        ("VAL1689_11_source_path_used", source_path_used, "candidate points to existing neutral 1689 template source alias"),
        ("VAL1689_12_gate_locked", gate_locked, "all gates remain locked"),
        ("VAL1689_13_decision_safe", decision_safe, "decision selects beta source/test convention first"),
        ("VAL1689_14_claim_gate_safe", claim_gate_safe, "all claim gates remain false"),
        ("VAL1689_15_no_claim_flags", no_claim_flags, "all generated rows keep claim flags false"),
        ("VAL1689_16_blocked_not_ready", blocked_not_ready, "no blocked/missing row is marked claim/scoring ready"),
        ("VAL1689_17_next_target_selected", next_target_selected, "next target selects beta source/test convention or curve digitization"),
        ("VAL1689_18_csv_parse", csv_parse, "all generated 1689 CSVs parse"),
        ("VAL1689_19_branch_copies", branch_copies, "branch/quarantine/queue copies exist"),
        ("VAL1689_20_pycache_absent", pycache_absent, "scripts __pycache__ absent"),
        ("VAL1689_21_formalization_untouched", formalization_clean, "no 1689 outputs found under formalization-workbench"),
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
            "check_id": "VAL1689_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1689 bulk alpha template beta/kernel/tail fill or R10 curve digitization validation",
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
    audit_rows: list[dict[str, object]],
    template_rows: list[dict[str, object]],
    bridge_rows: list[dict[str, object]],
    curve_rows: list[dict[str, object]],
    readiness_rows: list[dict[str, object]],
    candidate_rows_: list[dict[str, object]],
    validator_rows: list[dict[str, object]],
    gate_rows: list[dict[str, object]],
    decision_rows_: list[dict[str, object]],
    claim_rows: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    validation_rows: list[dict[str, object]],
) -> None:
    body = f"""# 1689 - Bulk Alpha Template Beta Kernel Tail Fill Or R10 Curve Digitization

**Private status:** current R2FR/qbar bridge for the R10 bulk-alpha template. No `q_loc=0`, local-GR pass, Newton pass, PPN pass, WEP pass, R10 pass, R11 pass, clock pass, orbital pass, or public claim is made.

## Verdict

The MTS-side comparator row now exists in the current route as a runner-shaped nonclaim template. It exposes `beta_bulk,S`, `beta_bulk,T`, `K_bulk,ST(lambda)`, `epsilon_tail(lambda)`, material pair, lambda units, and blocking inputs. That is real progress because the R10 machinery can now see the exact theory-side missing legs.

It is still not evidence. `alpha_bulk,ST(lambda)=0` is only an exact conditional theorem; beta source/test zero and tail zero are unsigned. The external side also remains nonclaim because Eot-Wash anchors are provenance-only and the full digitized `alpha_bound(lambda)` curve is missing.

## Source Register

{markdown_table(source_rows, ["source_key", "source_path", "exists", "needles_present", "use_in_1689"])}

## Zero Or Template Audit

{markdown_table(audit_rows, ["audit_id", "target", "current_result", "gap", "template_consequence"])}

## Bulk Alpha Template

{markdown_table(template_rows, ["curve_id", "lambda_value", "alpha_predicted", "valid_for_claim", "blocking_inputs"])}

## Template Bridge

{markdown_table(bridge_rows, ["bridge_id", "check", "check_pass", "detail"])}

## Curve Digitization Status

{markdown_table(curve_rows, ["curve_id", "object", "current_status", "data_or_requirement", "notes"])}

## Comparator Readiness

{markdown_table(readiness_rows, ["readiness_id", "component", "component_ready", "detail"])}

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

1689 is a plumbing win, not a physics claim. The next highest-leverage theory move is `beta_bulk,S` and `beta_bulk,T`: either derive/source those legs or keep them explicit. Curve digitization remains necessary, but a perfect curve cannot test MTS until the predicted alpha side is numeric or zero-certified.
"""
    DOC.write_text(body, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    validator = load_validator()
    source_rows = source_register_rows()
    audit_rows = zero_or_template_audit_rows()
    template_rows = bulk_alpha_template_rows()
    bridge_rows = template_bridge_rows(template_rows)
    curve_rows = curve_digitization_rows()
    readiness_rows = comparator_readiness_rows(template_rows, curve_rows)

    write_csv(SOURCE_REGISTER, source_rows, ["branch_id", "source_key", "source_path", "exists", "needles_present", "required_needles", "use_in_1689", "valid_for_claim", "claim_allowed"])
    write_csv(ZERO_OR_TEMPLATE_AUDIT, audit_rows, ["branch_id", "audit_id", "target", "attempted_derivation", "current_result", "gap", "template_consequence", "zero_signed", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"])
    template_fields = ["model_id", "branch_id", "curve_id", "lambda_units", "alpha_predicted", "alpha_bound", "force_law_form", "derivation_status", "formula_reference", "source_file", "assumptions", "valid_for_claim", "beta_source_handle", "beta_test_handle", "K_lambda_handle", "epsilon_tail_handle", "material_pair", "blocking_inputs", "lambda_value", "alpha_bound_source", "notes"]
    write_csv(BULK_ALPHA_TEMPLATE, template_rows, template_fields)
    write_csv(BULK_ALPHA_TEMPLATE_SOURCE_ALIAS, template_rows, template_fields)
    write_csv(TEMPLATE_BRIDGE, bridge_rows, ["branch_id", "bridge_id", "check", "check_pass", "detail", "template_ready", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"])
    write_csv(CURVE_DIGITIZATION_STATUS, curve_rows, ["branch_id", "curve_id", "object", "data_or_requirement", "current_status", "source_path_or_anchor", "notes", "curve_ready", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"])
    write_csv(COMPARATOR_READINESS, readiness_rows, ["branch_id", "readiness_id", "component", "component_ready", "detail", "comparator_ready", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"])

    candidates = qbar_candidate_rows(validator)
    validator_rows = validator_result_rows(validator, candidates)
    gate_rows = gate_status_rows(audit_rows, bridge_rows, curve_rows, readiness_rows, validator_rows)
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
    cleanup_pycache()
    validation_rows = validate(source_rows, audit_rows, template_rows, bridge_rows, curve_rows, readiness_rows, candidates, validator_rows, gate_rows, decisions, claims, next_rows)
    write_csv(VALIDATION, validation_rows, ["check_id", "result", "detail", "valid_for_claim", "claim_allowed"])
    write_doc(source_rows, audit_rows, template_rows, bridge_rows, curve_rows, readiness_rows, candidates, validator_rows, gate_rows, decisions, claims, next_rows, validation_rows)

    failed_rows = [row for row in validation_rows if row["result"] != "PASS"]
    print(f"wrote {DOC}")
    print(f"wrote {VALIDATION}")
    if failed_rows:
        for failed_row in failed_rows:
            print(f"FAIL {failed_row['check_id']}: {failed_row['detail']}")
        raise SystemExit(1)
    print("1689 validation PASS")


if __name__ == "__main__":
    main()
