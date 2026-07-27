from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FORMALIZATION = ROOT.parent / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
COEFF = MICROSCOPE / "branch_locked_wep" / "coefficients"
QUARANTINE = MICROSCOPE / "quarantine" / "1613"
INPUT_1613 = QUARANTINE / "input"
INPUT_DIRS = [
    INPUT_1613,
    MICROSCOPE / "quarantine" / "1612" / "input",
    MICROSCOPE / "quarantine" / "1611" / "input",
    MICROSCOPE / "quarantine" / "1610" / "input",
    MICROSCOPE / "quarantine" / "1609" / "input",
]
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1613-Y5-R2FR-CMSM-file-drop-loader-or-signed-margin-bound.md"

SOURCE_FILES = {
    "1612_doc": ROOT / "1612-Y5-R2FR-no-cancellation-theorem-or-CMSM-file-drop.md",
    "1612_validation": OUT / "P8_Y5_BRR545_1612_VALIDATION.csv",
    "1612_next": OUT / "P8_Y5_PARENT_QLOC_1612_NEXT_TARGET.csv",
    "1612_inventory": OUT / "P8_Y5_PARENT_QLOC_1612_CMSM_FILE_DROP_INVENTORY.csv",
    "1612_theorem": OUT / "P8_Y5_PARENT_QLOC_1612_NO_CANCELLATION_THEOREM_ATTEMPT.csv",
    "1612_requirements": OUT / "P8_Y5_PARENT_QLOC_1612_SIGN_SAFE_REQUIREMENTS.csv",
    "1612_claim_gate": OUT / "P8_Y5_PARENT_QLOC_1612_CLAIM_GATE.csv",
    "1611_validator": OUT / "P8_Y5_PARENT_QLOC_1611_SOURCE_PACK_VALIDATOR_SPEC.csv",
    "1611_dry_run": OUT / "P8_Y5_PARENT_QLOC_1611_SOURCE_PACK_VALIDATOR_DRY_RUN.csv",
    "1609_alignment": OUT / "P8_Y5_PARENT_QLOC_1609_ALIGNMENT_COMPUTATION_CONTRACT.csv",
    "1456_worldtube": COEFF / "source_worldtube_projection_theorem_attempt_1456.csv",
}

NEEDLES = {
    "1612_doc": ["NO_CANCELLATION_THEOREM_NOT_DERIVED", "NEXT_1613_CMSM_FILE_DROP_LOADER_OR_SIGNED_MARGIN_BOUND"],
    "1612_validation": ["VAL1612_OVERALL", "PASS"],
    "1612_next": ["1613-Y5-R2FR-CMSM-file-drop-loader-or-signed-margin-bound.md", "signed-margin"],
    "1612_inventory": ["TEMPLATE_ONLY_NOT_IMPORTABLE", "MISSING_INPUT_FILE"],
    "1612_theorem": ["NCT1612_1_finite_dimensional_margin_lemma", "EXACT_CONDITIONAL_LEMMA"],
    "1612_requirements": ["SSR1612_3_covariance_margin", "MISSING_MARGIN"],
    "1612_claim_gate": ["CG1612_2_cmin", "BLOCKED"],
    "1611_validator": ["VALSPEC1611_4_shortcut_firewall", "REJECT_SHORTCUT"],
    "1611_dry_run": ["MISSING_INPUT_FILE", "K_CMSM_readout"],
    "1609_alignment": ["ALI1609_3_c_min", "MISSING_CRITICAL"],
    "1456_worldtube": ["SWP1456_4_mask_orbit_limit", "DOMAIN_SELECTOR_COUNTERMODEL_RETAINED"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1613_SOURCE_REGISTER.csv"
FILE_DROP_LOADER = OUT / "P8_Y5_PARENT_QLOC_1613_CMSM_FILE_DROP_LOADER_DRY_RUN.csv"
SIGNED_MARGIN_THEOREM = OUT / "P8_Y5_PARENT_QLOC_1613_SIGNED_MARGIN_THEOREM_ATTEMPT.csv"
INTERVAL_SCHEMA = OUT / "P8_Y5_PARENT_QLOC_1613_INTERVAL_MARGIN_CERTIFICATE_SCHEMA.csv"
MARGIN_EVALUATOR = OUT / "P8_Y5_PARENT_QLOC_1613_MARGIN_BOUND_EVALUATOR_DRY_RUN.csv"
CERTIFICATE_GATES = OUT / "P8_Y5_PARENT_QLOC_1613_CERTIFICATE_ACCEPTANCE_GATES.csv"
RUNNER = OUT / "P8_Y5_PARENT_QLOC_1613_RUNNER.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1613_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1613_DECISION.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1613_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1613_VALIDATION.csv"

COPY_TARGETS = {
    FILE_DROP_LOADER: [
        QUARANTINE / "CMSM_FILE_DROP_LOADER_DRY_RUN_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_CMSM_file_drop_loader_dry_run_nonclaim_1613.csv",
    ],
    SIGNED_MARGIN_THEOREM: [
        QUARANTINE / "SIGNED_MARGIN_THEOREM_ATTEMPT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_signed_margin_theorem_attempt_nonclaim_1613.csv",
    ],
    INTERVAL_SCHEMA: [
        QUARANTINE / "INTERVAL_MARGIN_CERTIFICATE_SCHEMA_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_interval_margin_certificate_schema_nonclaim_1613.csv",
    ],
    MARGIN_EVALUATOR: [
        QUARANTINE / "MARGIN_BOUND_EVALUATOR_DRY_RUN_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_margin_bound_evaluator_dry_run_nonclaim_1613.csv",
    ],
    CLAIM_GATE: [
        QUARANTINE / "CLAIM_GATE_CLOSED.csv",
        BRANCH_RESIDUALS / "R2FR_claim_gate_closed_1613.csv",
    ],
}

REQUIRED_BY_ROLE = {
    "source_pack_filelist": {"dataset_id", "product_id", "file_name", "file_role", "download_url", "checksum"},
    "CMSM_network_capture": {"request_url", "method", "status_code", "response_kind", "captured_at"},
    "K_CMSM_readout": {"time_s", "session_id", "orbit_id", "gx", "gz", "Sxx", "Sxz", "mask_flag", "units", "sign_convention"},
    "alignment_result": {"K_norm", "V_norm", "projection_value", "c_min", "tau_min", "uncertainty", "basis"},
    "material_tensor": {"material_pair", "component", "value", "units", "basis", "source_path"},
    "source_worldtube": {"time_s", "position_basis", "source_component", "value", "units", "source_path"},
    "mask_orbit": {"time_s", "orbit_id", "mask_flag", "window_weight", "basis", "source_path"},
}

EXPECTED_FILES = [
    ("source_pack_filelist", "CMSM_source_pack_filelist.csv"),
    ("CMSM_network_capture", "CMSM_network_capture.csv"),
    ("K_CMSM_readout", "K_CMSM_readout.csv"),
    ("alignment_result", "alignment_result.csv"),
    ("material_tensor", "material_tensor.csv"),
    ("source_worldtube", "source_worldtube.csv"),
    ("mask_orbit", "mask_orbit.csv"),
]

CERTIFICATE_FILE = INPUT_1613 / "signed_margin_certificate.csv"
CERTIFICATE_COLUMNS = {
    "certificate_id",
    "component_id",
    "K_abs_lower",
    "V_abs_lower",
    "K_norm_upper",
    "V_norm_upper",
    "sign_compatible",
    "parent_signed",
    "source_path",
    "units",
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def truthy(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "y"}


def as_float(value: Any) -> float | None:
    try:
        numeric = float(str(value).strip())
    except (TypeError, ValueError):
        return None
    if numeric != numeric or numeric in {float("inf"), float("-inf")}:
        return None
    return numeric


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, (source_id, path) in enumerate(SOURCE_FILES.items()):
        text = read_text(path) if path.exists() else ""
        needles = NEEDLES[source_id]
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "source_id": f"SRC1613_{index}_{source_id}",
                "source_path": rel(path) if path.exists() else str(path),
                "exists": path.exists(),
                "needle_found": all(needle in text for needle in needles),
                "needles": "; ".join(needles),
                "source_role": "1613_CMSM_loader_or_signed_margin_bound_input",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def detect_role(path: Path, expected_role: str | None = None) -> str:
    name = path.name.lower()
    if "template" in name:
        return "template"
    if expected_role:
        return expected_role
    if "source_pack" in name and "filelist" in name:
        return "source_pack_filelist"
    if "network" in name or path.suffix.lower() == ".har":
        return "CMSM_network_capture"
    if "k_cmsm" in name or "readout" in name:
        return "K_CMSM_readout"
    if "alignment" in name:
        return "alignment_result"
    if "material" in name:
        return "material_tensor"
    if "worldtube" in name or "source" in name:
        return "source_worldtube"
    if "mask" in name or "orbit" in name:
        return "mask_orbit"
    if "signed_margin" in name:
        return "signed_margin_certificate"
    return "unknown"


def validate_candidate(role: str, path: Path) -> tuple[str, str, int]:
    if not path.exists():
        return "MISSING_INPUT_FILE", "candidate file is absent", 0
    if role == "template":
        return "TEMPLATE_ONLY_NOT_IMPORTABLE", "template files are useful examples but not official source rows", 0
    if role == "signed_margin_certificate":
        return "CERTIFICATE_FILE_HANDLED_BY_MARGIN_EVALUATOR", "certificate files are validated by the margin evaluator", 0
    if role == "unknown":
        return "UNRECOGNIZED_FILE_ROLE", "file does not match a known CMSM/readout/material/alignment role", 0
    if path.suffix.lower() == ".har":
        return "HAR_PRESENT_NOT_PARSED_BY_1613", "HAR capture is present but still needs source-pack extraction", 0
    try:
        rows = read_csv(path)
    except Exception as exc:
        return "REJECT_PARSE_ERROR", str(exc), 0
    if not rows:
        return "REJECT_EMPTY_CSV", "candidate contains no rows", 0
    required = REQUIRED_BY_ROLE[role]
    fieldnames = set(rows[0].keys())
    missing = sorted(required - fieldnames)
    if missing:
        return "REJECT_MISSING_COLUMNS", "missing " + ";".join(missing), len(rows)
    row = rows[0]
    if role == "source_pack_filelist" and (not row.get("download_url") or not row.get("checksum")):
        return "REJECT_BAD_PROVENANCE", "download_url/checksum missing", len(rows)
    if role == "CMSM_network_capture" and not row.get("request_url"):
        return "REJECT_BAD_PROVENANCE", "request_url missing", len(rows)
    if role == "K_CMSM_readout" and (not row.get("units") or not row.get("sign_convention")):
        return "REJECT_BAD_UNITS_SIGN_BASIS", "units/sign_convention missing", len(rows)
    if role == "alignment_result" and (not row.get("basis") or not row.get("c_min")):
        return "REJECT_BAD_UNITS_SIGN_BASIS", "basis/c_min missing", len(rows)
    return "ACCEPT_NONCLAIM_QUARANTINE", "row parses under 1613 loader; still nonclaim", len(rows)


def file_drop_loader_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    seen: set[Path] = set()
    for input_dir in INPUT_DIRS:
        input_dir.mkdir(parents=True, exist_ok=True)
        for role, file_name in EXPECTED_FILES:
            path = input_dir / file_name
            seen.add(path)
            status, reason, row_count = validate_candidate(role, path)
            rows.append(
                {
                    "same_parent_branch_id": BRANCH_ID,
                    "loader_id": f"LOA1613_{len(rows)}_{input_dir.parent.name}_{role}",
                    "input_dir": rel(input_dir),
                    "file_role": role,
                    "candidate_path": rel(path) if path.exists() else str(path),
                    "exists": path.exists(),
                    "row_count": row_count,
                    "loader_result": status,
                    "reason": reason,
                    "accepted_for_nonclaim_loader": status == "ACCEPT_NONCLAIM_QUARANTINE",
                    "source_promoted": False,
                    "score_ready": False,
                    "valid_prediction_row": False,
                    "valid_for_claim": False,
                    "claim_allowed": False,
                }
            )
        for path in sorted(p for p in input_dir.glob("*") if p.is_file() and p not in seen):
            role = detect_role(path)
            status, reason, row_count = validate_candidate(role, path)
            rows.append(
                {
                    "same_parent_branch_id": BRANCH_ID,
                    "loader_id": f"LOA1613_{len(rows)}_{input_dir.parent.name}_{role}_extra",
                    "input_dir": rel(input_dir),
                    "file_role": role,
                    "candidate_path": rel(path),
                    "exists": True,
                    "row_count": row_count,
                    "loader_result": status,
                    "reason": reason,
                    "accepted_for_nonclaim_loader": status == "ACCEPT_NONCLAIM_QUARANTINE",
                    "source_promoted": False,
                    "score_ready": False,
                    "valid_prediction_row": False,
                    "valid_for_claim": False,
                    "claim_allowed": False,
                }
            )
    return rows


def signed_margin_theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": "SMT1613_0_exact_object",
            "statement": "For readout functional K and normalized allowed source-material cone C, c_min := inf_{V in C} |<K,V>|/(||K||||V||).",
            "status": "EXACT_DEFINITION",
            "derived_result": "c_min is the precise local/WEP suppression escape hatch: c_min>0 forbids silent cancellation",
            "missing_for_promotion": "K, C and basis are not parent-signed by current files",
            "theorem_closed": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": "SMT1613_1_compact_kernel_theorem",
            "statement": "If C is compact in the unit sphere and C cap ker(K)=empty, continuity gives c_min>0; if C intersects ker(K), c_min=0.",
            "status": "EXACT_IFF_THEOREM",
            "derived_result": "the proof route is now binary: exclude ker(K) or the local branch fails to produce a lower bound",
            "missing_for_promotion": "current corpus has not parent-derived C cap ker(K)=empty",
            "theorem_closed": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": "SMT1613_2_interval_sufficient_bound",
            "statement": "If each certified component has compatible sign, |K_i|>=k_i-, |V_i|>=v_i-, ||K||<=K+, ||V||<=V+, then c_min >= sum_i k_i- v_i-/(K+ V+) when all omitted terms are nonnegative or bounded.",
            "status": "EXACT_CONDITIONAL_CERTIFICATE",
            "derived_result": "this gives a computable certificate format for future official arrays or parent-derived intervals",
            "missing_for_promotion": "no parent-signed interval rows exist in input/1613",
            "theorem_closed": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": "SMT1613_3_signed_component_problem",
            "statement": "If any component has unknown sign, unknown covariance, or omitted signed corrections, the interval lower bound is invalid.",
            "status": "SHORTCUT_FIREWALL",
            "derived_result": "prevents converting symbolic K or positive density into a fake nonzero c_min",
            "missing_for_promotion": "official correction/material covariance data are absent",
            "theorem_closed": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": "SMT1613_4_verdict",
            "statement": "1613 derives the exact signed-margin theorem and a computable certificate gate, but does not close the physical MTS/WEP local branch.",
            "status": "SIGNED_MARGIN_BOUND_NOT_PHYSICALLY_CERTIFIED",
            "derived_result": "mathematics is sharp; physics input is still missing",
            "missing_for_promotion": "needs official CMSM K/V/alignment files or a parent-signed cone theorem",
            "theorem_closed": False,
            "claim_allowed": False,
        },
    ]


def interval_schema_rows() -> list[dict[str, Any]]:
    rows = [
        ("certificate_id", "string", "groups certificate rows", "must match across rows"),
        ("component_id", "string", "component/basis label", "must map to K and V basis"),
        ("K_abs_lower", "positive float", "lower bound on |K_i|", "must be parent-signed or official-array certified"),
        ("V_abs_lower", "positive float", "lower bound on |V_i|", "must be parent-signed or official-array certified"),
        ("K_norm_upper", "positive float", "upper bound on ||K||", "shared certificate denominator"),
        ("V_norm_upper", "positive float", "upper bound on ||V||", "shared certificate denominator"),
        ("sign_compatible", "boolean", "K_i V_i terms have certified nonnegative contribution", "false blocks certificate"),
        ("parent_signed", "boolean", "row is sourced to parent theorem or official files", "false blocks certificate"),
        ("source_path", "path/url", "provenance for coefficient/bound", "must not be placeholder"),
        ("units", "string", "declared units/basis", "must be compatible across rows"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "column_name": name,
            "expected_type": expected_type,
            "role": role,
            "acceptance_rule": rule,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for name, expected_type, role, rule in rows
    ]


def evaluate_certificate_rows() -> list[dict[str, Any]]:
    if not CERTIFICATE_FILE.exists():
        return [
            {
                "same_parent_branch_id": BRANCH_ID,
                "eval_id": "MBE1613_0_missing_certificate",
                "candidate_path": str(CERTIFICATE_FILE),
                "exists": False,
                "row_count": 0,
                "evaluator_result": "MISSING_SIGNED_MARGIN_CERTIFICATE",
                "numerator_lower_bound": "",
                "denominator_upper_bound": "",
                "c_min_lower_bound": "",
                "reason": "no signed_margin_certificate.csv file is present in quarantine/1613/input",
                "score_ready": False,
                "valid_prediction_row": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        ]
    try:
        rows = read_csv(CERTIFICATE_FILE)
    except Exception as exc:
        return [
            {
                "same_parent_branch_id": BRANCH_ID,
                "eval_id": "MBE1613_0_parse_error",
                "candidate_path": rel(CERTIFICATE_FILE),
                "exists": True,
                "row_count": 0,
                "evaluator_result": "REJECT_PARSE_ERROR",
                "numerator_lower_bound": "",
                "denominator_upper_bound": "",
                "c_min_lower_bound": "",
                "reason": str(exc),
                "score_ready": False,
                "valid_prediction_row": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        ]
    if not rows:
        status = "REJECT_EMPTY_CERTIFICATE"
        reason = "certificate contains no rows"
        numerator = denominator = c_min = ""
    else:
        missing = sorted(CERTIFICATE_COLUMNS - set(rows[0].keys()))
        if missing:
            status = "REJECT_MISSING_COLUMNS"
            reason = "missing " + ";".join(missing)
            numerator = denominator = c_min = ""
        else:
            numeric_ok = True
            sign_ok = True
            parent_ok = True
            numerator_value = 0.0
            k_norm_upper = 0.0
            v_norm_upper = 0.0
            for row in rows:
                k_lower = as_float(row.get("K_abs_lower"))
                v_lower = as_float(row.get("V_abs_lower"))
                k_upper = as_float(row.get("K_norm_upper"))
                v_upper = as_float(row.get("V_norm_upper"))
                if k_lower is None or v_lower is None or k_upper is None or v_upper is None:
                    numeric_ok = False
                    continue
                if k_lower < 0 or v_lower < 0 or k_upper <= 0 or v_upper <= 0:
                    numeric_ok = False
                    continue
                if not truthy(row.get("sign_compatible")):
                    sign_ok = False
                if not truthy(row.get("parent_signed")):
                    parent_ok = False
                numerator_value += k_lower * v_lower
                k_norm_upper = max(k_norm_upper, k_upper)
                v_norm_upper = max(v_norm_upper, v_upper)
            denominator_value = k_norm_upper * v_norm_upper
            if not numeric_ok:
                status = "REJECT_BAD_NUMERIC_INTERVALS"
                reason = "all numeric interval bounds must be finite with positive denominator"
                c_value: float | None = None
            elif not sign_ok:
                status = "REJECT_UNSIGNED_COMPONENTS"
                reason = "all rows must be sign_compatible=true"
                c_value = None
            elif not parent_ok:
                status = "REJECT_PARENT_UNSIGNED"
                reason = "all rows must be parent_signed=true or sourced to official files"
                c_value = None
            elif numerator_value <= 0 or denominator_value <= 0:
                status = "REJECT_ZERO_MARGIN"
                reason = "computed lower bound is not strictly positive"
                c_value = None
            else:
                status = "ACCEPT_CONDITIONAL_MARGIN_NONCLAIM"
                reason = "certificate computes a positive lower bound but remains nonclaim until full branch gates pass"
                c_value = numerator_value / denominator_value
            numerator = f"{numerator_value:.17g}" if numeric_ok else ""
            denominator = f"{denominator_value:.17g}" if numeric_ok else ""
            c_min = f"{c_value:.17g}" if c_value is not None else ""
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "eval_id": "MBE1613_0_certificate_eval",
            "candidate_path": rel(CERTIFICATE_FILE),
            "exists": True,
            "row_count": len(rows),
            "evaluator_result": status,
            "numerator_lower_bound": numerator,
            "denominator_upper_bound": denominator,
            "c_min_lower_bound": c_min,
            "reason": reason,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def certificate_gate_rows(loader: list[dict[str, Any]], evaluator: list[dict[str, Any]]) -> list[dict[str, Any]]:
    accepted_loader = any(truthy(row["accepted_for_nonclaim_loader"]) for row in loader)
    accepted_margin = any(row["evaluator_result"] == "ACCEPT_CONDITIONAL_MARGIN_NONCLAIM" for row in evaluator)
    rows = [
        ("CAC1613_0_source_files", "official CMSM/readout/material/alignment files parse with provenance", accepted_loader, "source rows are absent or template-only"),
        ("CAC1613_1_margin_certificate", "signed_margin_certificate.csv computes c_min_lower_bound>0", accepted_margin, "certificate missing or not parent-signed"),
        ("CAC1613_2_parent_basis", "K and V use the same parent branch basis", False, "basis map not signed by current corpus"),
        ("CAC1613_3_covariance", "omitted/correction terms cannot cancel the certified numerator", False, "covariance/no-cancellation rule absent"),
        ("CAC1613_4_claim_policy", "even accepted rows stay nonclaim until WEP/local branch closes", False, "branch gates still open"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "gate": gate,
            "condition_met": met,
            "status": "NONCLAIM_READY" if met else "BLOCKED",
            "reason": reason if not met else "condition met but not promoted",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for gate_id, gate, met, reason in rows
    ]


def runner_rows(loader: list[dict[str, Any]], evaluator: list[dict[str, Any]]) -> list[dict[str, Any]]:
    accepted_loader = [row for row in loader if truthy(row["accepted_for_nonclaim_loader"])]
    margin_result = evaluator[0]["evaluator_result"] if evaluator else "NO_EVALUATOR"
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1613_0_file_loader",
            "input_state": f"{len(accepted_loader)} accepted nonclaim loader rows",
            "runner_result": "SOURCE_FILES_ACCEPTED_NONCLAIM" if accepted_loader else "NO_CMSM_FILE_DROP_ACCEPTED",
            "effect": "loader is ready; no source is promoted",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1613_1_margin_evaluator",
            "input_state": margin_result,
            "runner_result": "SIGNED_MARGIN_CERTIFICATE_ACCEPTED_NONCLAIM" if margin_result == "ACCEPT_CONDITIONAL_MARGIN_NONCLAIM" else "NO_SIGNED_MARGIN_CERTIFICATE_ACCEPTED",
            "effect": "no positive physical c_min is promoted",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    gates = [
        ("CG1613_0_file_loader", "official CMSM source rows loaded", "BLOCKED", "no complete official source/readout/material/alignment set accepted"),
        ("CG1613_1_signed_margin", "positive parent-signed c_min", "BLOCKED", "no signed_margin_certificate or parent cone theorem closes c_min"),
        ("CG1613_2_no_cancellation", "no-cancellation theorem", "BLOCKED", "kernel/covariance/correction countermodels remain live"),
        ("CG1613_3_WEP", "WEP score", "BLOCKED", "readout/source/material/tau gates open"),
        ("CG1613_4_local_GR", "R10/Newton/local-GR claim", "BLOCKED", "local source-normalization branch unresolved"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "claim": claim,
            "status": status,
            "reason": reason,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for gate_id, claim, status, reason in gates
    ]


def decision_rows(loader: list[dict[str, Any]], evaluator: list[dict[str, Any]]) -> list[dict[str, Any]]:
    accepted_loader = any(truthy(row["accepted_for_nonclaim_loader"]) for row in loader)
    accepted_margin = any(row["evaluator_result"] == "ACCEPT_CONDITIONAL_MARGIN_NONCLAIM" for row in evaluator)
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1613_0_file_loader",
            "decision": "FILE_LOADER_READY_NO_SOURCE_PROMOTION" if accepted_loader else "FILE_LOADER_READY_NO_FILES_ACCEPTED",
            "reason": "accepted files remain nonclaim" if accepted_loader else "only missing/template rows are available",
            "next_action": "use official file rows in a quarantined alignment computation" if accepted_loader else "capture official CMSM files or continue parent-cone derivation",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1613_1_margin",
            "decision": "SIGNED_MARGIN_CERTIFICATE_ACCEPTED_NONCLAIM" if accepted_margin else "SIGNED_MARGIN_BOUND_NOT_CERTIFIED",
            "reason": "certificate computes a positive nonclaim lower bound" if accepted_margin else "no parent-signed interval certificate exists",
            "next_action": "check covariance/branch gates" if accepted_margin else "derive parent cone/basis map or acquire official K/V/alignment arrays",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1613_2_next",
            "decision": "NEXT_1614_PARENT_CONE_BASIS_OR_OFFICIAL_CMSM_ACQUISITION",
            "reason": "the remaining fork is now explicit: derive C cap ker(K)=empty in parent basis, or get official files and compute c_min",
            "next_action": "attempt parent cone/basis derivation while keeping CMSM acquisition route ready",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "next_target": "1614-Y5-R2FR-parent-cone-basis-or-official-CMSM-acquisition.md",
            "script": "scripts/Y5_R2FR_parent_cone_basis_or_official_CMSM_acquisition.py",
            "objective": "derive the parent allowed cone/basis map proving C cap ker(K)=empty, or acquire official CMSM readout/material/alignment arrays",
            "success_condition": "parent-signed cone/basis/covariance theorem giving c_min>0, or official CMSM arrays enabling a nonclaim c_min computation",
            "do_not": "do not use tau_eff=1, symbolic K alone, surrogate arrays, bound inversion, closure-only zero, measured-G absorption, or public/local-GR claims",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def copy_outputs() -> None:
    for source, targets in COPY_TARGETS.items():
        for target in targets:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def csv_parses(paths: list[Path]) -> bool:
    try:
        for path in paths:
            read_csv(path)
    except Exception:
        return False
    return True


def no_claim_flags(paths: list[Path]) -> bool:
    for path in paths:
        for row in read_csv(path):
            for field in ("source_promoted", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"):
                if truthy(row.get(field, "")):
                    return False
    return True


def no_formalization_1613() -> bool:
    if not FORMALIZATION.exists():
        return True
    artifact_markers = (
        "1613-Y5",
        "P8_Y5_PARENT_QLOC_1613",
        "P8_Y5_BRR545_1613",
        "Y5_R2FR_CMSM_file_drop_loader_or_signed_margin_bound",
        "R2FR_signed_margin",
        "R2FR_margin_bound",
        "R2FR_CMSM_file_drop_loader",
    )
    return not any(any(marker in path.name for marker in artifact_markers) for path in FORMALIZATION.rglob("*"))


def validation_rows(generated_csvs: list[Path]) -> list[dict[str, Any]]:
    sources = source_register_rows()
    loader = read_csv(FILE_DROP_LOADER)
    theorem = read_csv(SIGNED_MARGIN_THEOREM)
    schema = read_csv(INTERVAL_SCHEMA)
    evaluator = read_csv(MARGIN_EVALUATOR)
    gates = read_csv(CERTIFICATE_GATES)
    runner = read_csv(RUNNER)
    claim_gates = read_csv(CLAIM_GATE)
    decisions = read_csv(DECISION)
    copies = [target for targets in COPY_TARGETS.values() for target in targets]
    accepted_loader = [row for row in loader if truthy(row["accepted_for_nonclaim_loader"])]
    checks = [
        ("VAL1613_0_sources_exist", all(truthy(row["exists"]) for row in sources), "all cited 1613 local source paths exist"),
        ("VAL1613_1_needles_found", all(truthy(row["needle_found"]) for row in sources), "all required 1613 source needles found"),
        ("VAL1613_2_input_dir_ready", INPUT_1613.exists(), "1613 quarantine input directory exists"),
        ("VAL1613_3_loader_covers_roles", len(loader) >= len(INPUT_DIRS) * len(EXPECTED_FILES), "loader covers expected CMSM/readout/material/alignment roles"),
        ("VAL1613_4_loader_nonclaim", all(row["source_promoted"].lower() == "false" and row["valid_for_claim"].lower() == "false" for row in accepted_loader), "accepted loader rows remain nonclaim"),
        ("VAL1613_5_signed_margin_theorem", any(row["theorem_id"] == "SMT1613_1_compact_kernel_theorem" and row["status"] == "EXACT_IFF_THEOREM" for row in theorem), "exact compact-kernel theorem recorded"),
        ("VAL1613_6_margin_not_certified", any(row["theorem_id"] == "SMT1613_4_verdict" and row["status"] == "SIGNED_MARGIN_BOUND_NOT_PHYSICALLY_CERTIFIED" for row in theorem), "physical signed margin remains uncertified"),
        ("VAL1613_7_interval_schema", len(schema) == len(CERTIFICATE_COLUMNS), "interval certificate schema written"),
        ("VAL1613_8_evaluator_refuses_or_nonclaim", evaluator and all(row["valid_for_claim"].lower() == "false" and row["claim_allowed"].lower() == "false" for row in evaluator), "margin evaluator never promotes claims"),
        ("VAL1613_9_certificate_gates", len(gates) >= 5 and all(row["claim_allowed"].lower() == "false" for row in gates), "certificate acceptance gates are nonclaim"),
        ("VAL1613_10_runner_refuses_claim", all(row["claim_allowed"].lower() == "false" for row in runner), "runner does not allow claims"),
        ("VAL1613_11_claim_gates_closed", claim_gates and all(row["status"] == "BLOCKED" and row["claim_allowed"].lower() == "false" for row in claim_gates), "all 1613 claim gates remain closed"),
        ("VAL1613_12_decision_next", any(row["decision"] == "NEXT_1614_PARENT_CONE_BASIS_OR_OFFICIAL_CMSM_ACQUISITION" for row in decisions), "decision selects 1614 parent cone/basis or official CMSM acquisition"),
        ("VAL1613_13_csv_parse", csv_parses(generated_csvs), "all generated 1613 CSVs parse"),
        ("VAL1613_14_claim_safety_flags", no_claim_flags(generated_csvs), "no generated 1613 rows are source-promoted, score-ready, prediction rows, valid-for-claim, or claim-allowed"),
        ("VAL1613_15_branch_copies", all(path.exists() for path in copies), "branch/quarantine nonclaim copies exist"),
        ("VAL1613_16_pycache_absent", not (Path(__file__).resolve().parent / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1613_17_formalization_untouched", no_formalization_1613(), "no 1613 outputs found under formalization-workbench"),
    ]
    rows = [
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if ok else "FAIL",
            "detail": detail,
        }
        for check_id, ok, detail in checks
    ]
    rows.append(
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": "VAL1613_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1613 CMSM file-drop loader or signed-margin bound validation",
        }
    )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ").replace("|", "/") for column in columns) + " |")
    return "\n".join([header, sep, *body])


def write_doc(
    sources: list[dict[str, Any]],
    loader: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    schema: list[dict[str, Any]],
    evaluator: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    claim_gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n\n".join(
            [
                "# 1613 - R2/fR CMSM File-Drop Loader Or Signed-Margin Bound",
                "## Verdict\n"
                "- 1613 converts the 1612 no-cancellation obstruction into a concrete loader plus a signed-margin certificate gate.\n"
                "- The exact theorem is now sharp: for normalized allowed cone `C`, a positive `c_min` exists iff `C` avoids `ker(K_CMSM)`.\n"
                "- A computable interval certificate schema is written for future official arrays or parent-derived bounds.\n"
                "- No real CMSM/readout/material/alignment file is currently accepted, and no signed-margin certificate is present.\n"
                "- No WEP, R10, PPN, clock, orbital, Newton, local-GR, beta/coupling, or public claim is made.",
                "## Source Register",
                md_table(sources, ["source_id", "source_path", "exists", "needle_found", "needles"]),
                "## CMSM File-Drop Loader Dry Run",
                md_table(loader, ["loader_id", "file_role", "exists", "loader_result", "reason", "accepted_for_nonclaim_loader"]),
                "## Signed-Margin Theorem Attempt",
                md_table(theorem, ["theorem_id", "status", "derived_result", "missing_for_promotion", "theorem_closed"]),
                "## Interval Margin Certificate Schema",
                md_table(schema, ["column_name", "expected_type", "role", "acceptance_rule"]),
                "## Margin Bound Evaluator Dry Run",
                md_table(evaluator, ["eval_id", "exists", "row_count", "evaluator_result", "c_min_lower_bound", "reason"]),
                "## Certificate Acceptance Gates",
                md_table(gates, ["gate_id", "gate", "condition_met", "status", "reason"]),
                "## Runner",
                md_table(runner, ["runner_id", "input_state", "runner_result", "effect"]),
                "## Claim Gates",
                md_table(claim_gates, ["gate_id", "claim", "status", "reason"]),
                "## Decision",
                md_table(decisions, ["decision_id", "decision", "reason", "next_action"]),
                "## Next Target",
                md_table(next_rows, ["next_target", "script", "objective", "success_condition", "do_not"]),
                "## Validation",
                md_table(validation, ["check_id", "result", "detail"]),
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    INPUT_1613.mkdir(parents=True, exist_ok=True)
    sources = source_register_rows()
    loader = file_drop_loader_rows()
    theorem = signed_margin_theorem_rows()
    schema = interval_schema_rows()
    evaluator = evaluate_certificate_rows()
    gates = certificate_gate_rows(loader, evaluator)
    runner = runner_rows(loader, evaluator)
    claim_gates = claim_gate_rows()
    decisions = decision_rows(loader, evaluator)
    next_rows = next_target_rows()
    generated_csvs = [
        SOURCE_REGISTER,
        FILE_DROP_LOADER,
        SIGNED_MARGIN_THEOREM,
        INTERVAL_SCHEMA,
        MARGIN_EVALUATOR,
        CERTIFICATE_GATES,
        RUNNER,
        CLAIM_GATE,
        DECISION,
        NEXT_TARGET,
    ]
    write_csv(SOURCE_REGISTER, sources)
    write_csv(FILE_DROP_LOADER, loader)
    write_csv(SIGNED_MARGIN_THEOREM, theorem)
    write_csv(INTERVAL_SCHEMA, schema)
    write_csv(MARGIN_EVALUATOR, evaluator)
    write_csv(CERTIFICATE_GATES, gates)
    write_csv(RUNNER, runner)
    write_csv(CLAIM_GATE, claim_gates)
    write_csv(DECISION, decisions)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()
    remove_pycache()
    validation = validation_rows(generated_csvs)
    write_csv(VALIDATION, validation)
    write_doc(sources, loader, theorem, schema, evaluator, gates, runner, claim_gates, decisions, next_rows, validation)


if __name__ == "__main__":
    main()
