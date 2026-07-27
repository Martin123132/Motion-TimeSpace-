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
QUARANTINE = MICROSCOPE / "quarantine" / "1612"
INPUT_1612 = QUARANTINE / "input"
INPUT_DIRS = [
    INPUT_1612,
    MICROSCOPE / "quarantine" / "1611" / "input",
    MICROSCOPE / "quarantine" / "1610" / "input",
    MICROSCOPE / "quarantine" / "1609" / "input",
]
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1612-Y5-R2FR-no-cancellation-theorem-or-CMSM-file-drop.md"

SOURCE_FILES = {
    "1611_doc": ROOT / "1611-Y5-R2FR-source-pack-import-validator-or-sign-definite-readout-theorem.md",
    "1611_validation": OUT / "P8_Y5_BRR545_1611_VALIDATION.csv",
    "1611_next": OUT / "P8_Y5_PARENT_QLOC_1611_NEXT_TARGET.csv",
    "1611_dry_run": OUT / "P8_Y5_PARENT_QLOC_1611_SOURCE_PACK_VALIDATOR_DRY_RUN.csv",
    "1611_sign_theorem": OUT / "P8_Y5_PARENT_QLOC_1611_SIGN_DEFINITE_READOUT_THEOREM_ATTEMPT.csv",
    "1611_sign_counters": OUT / "P8_Y5_PARENT_QLOC_1611_SIGN_DEFINITE_COUNTERMODEL_AUDIT.csv",
    "1611_claim_gate": OUT / "P8_Y5_PARENT_QLOC_1611_CLAIM_GATE.csv",
    "1610_positive_cone": OUT / "P8_Y5_PARENT_QLOC_1610_POSITIVE_CONE_THEOREM_ATTEMPT.csv",
    "1609_alignment": OUT / "P8_Y5_PARENT_QLOC_1609_ALIGNMENT_COMPUTATION_CONTRACT.csv",
    "1456_worldtube": COEFF / "source_worldtube_projection_theorem_attempt_1456.csv",
    "1455_readout": COEFF / "official_readout_acquisition_ledger_nonclaim_1455.csv",
}

NEEDLES = {
    "1611_doc": ["SIGN_DEFINITE_READOUT_NOT_DERIVED", "NEXT_1612_NO_CANCELLATION_THEOREM_OR_CMSM_FILE_DROP"],
    "1611_validation": ["VAL1611_OVERALL", "PASS"],
    "1611_next": ["1612-Y5-R2FR-no-cancellation-theorem-or-CMSM-file-drop.md", "no-cancellation"],
    "1611_dry_run": ["MISSING_INPUT_FILE", "K_CMSM_readout"],
    "1611_sign_theorem": ["SDR1611_3_verdict", "SIGN_DEFINITE_READOUT_NOT_DERIVED"],
    "1611_sign_counters": ["SDC1611_0_orbit_window", "COUNTERMODEL_RETAINED"],
    "1611_claim_gate": ["CG1611_2_cmin", "BLOCKED"],
    "1610_positive_cone": ["PCN1610_1_positive_functional_lemma", "EXACT_CONDITIONAL_LEMMA"],
    "1609_alignment": ["ALI1609_5_no_cancellation", "MISSING"],
    "1456_worldtube": ["SWP1456_4_mask_orbit_limit", "DOMAIN_SELECTOR_COUNTERMODEL_RETAINED"],
    "1455_readout": ["KC1455_2_design_values", "STRUCTURE_ONLY_VALUES_ABSENT"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1612_SOURCE_REGISTER.csv"
FILE_DROP_INVENTORY = OUT / "P8_Y5_PARENT_QLOC_1612_CMSM_FILE_DROP_INVENTORY.csv"
NO_CANCELLATION = OUT / "P8_Y5_PARENT_QLOC_1612_NO_CANCELLATION_THEOREM_ATTEMPT.csv"
COUNTERMODEL = OUT / "P8_Y5_PARENT_QLOC_1612_CANCELLATION_COUNTERMODEL_AUDIT.csv"
SIGN_SAFE_REQUIREMENTS = OUT / "P8_Y5_PARENT_QLOC_1612_SIGN_SAFE_REQUIREMENTS.csv"
RUNNER = OUT / "P8_Y5_PARENT_QLOC_1612_RUNNER.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1612_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1612_DECISION.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1612_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1612_VALIDATION.csv"

COPY_TARGETS = {
    FILE_DROP_INVENTORY: [
        QUARANTINE / "CMSM_FILE_DROP_INVENTORY_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_CMSM_file_drop_inventory_nonclaim_1612.csv",
    ],
    NO_CANCELLATION: [
        QUARANTINE / "NO_CANCELLATION_THEOREM_ATTEMPT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_no_cancellation_theorem_attempt_nonclaim_1612.csv",
    ],
    COUNTERMODEL: [
        QUARANTINE / "CANCELLATION_COUNTERMODEL_AUDIT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_cancellation_countermodel_audit_nonclaim_1612.csv",
    ],
    SIGN_SAFE_REQUIREMENTS: [
        QUARANTINE / "SIGN_SAFE_REQUIREMENTS_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_sign_safe_requirements_nonclaim_1612.csv",
    ],
    CLAIM_GATE: [
        QUARANTINE / "CLAIM_GATE_CLOSED.csv",
        BRANCH_RESIDUALS / "R2FR_claim_gate_closed_1612.csv",
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


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def truthy(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "y"}


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, (source_id, path) in enumerate(SOURCE_FILES.items()):
        text = read_text(path) if path.exists() else ""
        needles = NEEDLES[source_id]
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "source_id": f"SRC1612_{index}_{source_id}",
                "source_path": rel(path) if path.exists() else str(path),
                "exists": path.exists(),
                "needle_found": all(needle in text for needle in needles),
                "needles": "; ".join(needles),
                "source_role": "1612_no_cancellation_theorem_or_CMSM_file_drop_input",
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
    return "unknown"


def validate_candidate(role: str, path: Path) -> tuple[str, str, int]:
    if not path.exists():
        return "MISSING_INPUT_FILE", "candidate file is absent", 0
    if role == "template":
        return "TEMPLATE_ONLY_NOT_IMPORTABLE", "template files are useful examples but not official source rows", 0
    if role == "unknown":
        return "UNRECOGNIZED_FILE_ROLE", "file does not match a known CMSM/readout/material/alignment role", 0
    if path.suffix.lower() == ".har":
        return "HAR_PRESENT_NOT_PARSED_BY_1612", "HAR capture is present but still needs a source-pack extraction pass", 0
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
    return "ACCEPT_NONCLAIM_QUARANTINE", "row parses under 1612 file-drop validator; still nonclaim", len(rows)


def file_drop_inventory_rows() -> list[dict[str, Any]]:
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
                    "inventory_id": f"FDI1612_{len(rows)}_{input_dir.parent.name}_{role}",
                    "input_dir": rel(input_dir),
                    "file_role": role,
                    "candidate_path": rel(path) if path.exists() else str(path),
                    "exists": path.exists(),
                    "row_count": row_count,
                    "validator_result": status,
                    "reason": reason,
                    "accepted_for_quarantine": status == "ACCEPT_NONCLAIM_QUARANTINE",
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
                    "inventory_id": f"FDI1612_{len(rows)}_{input_dir.parent.name}_{role}_extra",
                    "input_dir": rel(input_dir),
                    "file_role": role,
                    "candidate_path": rel(path),
                    "exists": True,
                    "row_count": row_count,
                    "validator_result": status,
                    "reason": reason,
                    "accepted_for_quarantine": status == "ACCEPT_NONCLAIM_QUARANTINE",
                    "score_ready": False,
                    "valid_prediction_row": False,
                    "valid_for_claim": False,
                    "claim_allowed": False,
                }
            )
    return rows


def no_cancellation_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": "NCT1612_0_target",
            "statement": "prove a parent-signed lower bound |<K_CMSM,V_source_material>| >= c_min ||K_CMSM|| ||V_source_material|| with c_min>0",
            "mathematical_status": "TARGET_SHARPENED",
            "what_is_exact": "this is the missing bridge from nonzero source/material response to nonzero WEP/local residual amplitude",
            "blocking_gap": "neither official K/V arrays nor a parent cone disjoint from ker(K_CMSM) is present",
            "theorem_closed": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": "NCT1612_1_finite_dimensional_margin_lemma",
            "statement": "For normalized allowed set C, a no-cancellation bound exists iff dist(C,ker K)>0; then c_min=inf_{V in C}|<K,V>|/(||K||||V||).",
            "mathematical_status": "EXACT_CONDITIONAL_LEMMA",
            "what_is_exact": "the margin theorem is standard finite-dimensional geometry and gives the right quantity to compute",
            "blocking_gap": "current corpus does not parent-sign C or compute its distance to ker(K_CMSM)",
            "theorem_closed": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": "NCT1612_2_dual_cone_sufficient_condition",
            "statement": "If K_CMSM has a fixed signed representative in the dual cone and V is restricted to a compact positive cone with a strict margin, cancellation is forbidden.",
            "mathematical_status": "EXACT_CONDITIONAL_ROUTE",
            "what_is_exact": "a sign-safe readout/current cone would close the branch without fitting tau_eff=1",
            "blocking_gap": "sign-safe representative, nonnegative windows, material cone and covariance margin are all unsigned",
            "theorem_closed": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": "NCT1612_3_kernel_no_go",
            "statement": "Without cone restriction or official alignment data, there can be nonzero V in ker(K_CMSM), so <K_CMSM,V>=0.",
            "mathematical_status": "EXACT_NO_GO",
            "what_is_exact": "nonzero source/material response alone cannot imply nonzero readout amplitude",
            "blocking_gap": "must exclude the kernel by data or parent theorem",
            "theorem_closed": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": "NCT1612_4_WEP_obstruction",
            "statement": "MICROSCOPE Ti/Pt differential readout is not a bulk-positive scalar channel; material contrasts, masks, orbit windows and corrections can be signed.",
            "mathematical_status": "OBSTRUCTION_RETAINED",
            "what_is_exact": "this explains why positivity of Earth mass density is insufficient",
            "blocking_gap": "need official arrays or parent sign/covariance theorem",
            "theorem_closed": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": "NCT1612_5_verdict",
            "statement": "1612 does not derive the no-cancellation theorem; it reduces the target to a signed-margin/source-file problem.",
            "mathematical_status": "NO_CANCELLATION_THEOREM_NOT_DERIVED",
            "what_is_exact": "the exact c_min object and sufficient clauses are now explicit",
            "blocking_gap": "parent-signed sign-safe cone or real CMSM alignment/source files still missing",
            "theorem_closed": False,
            "claim_allowed": False,
        },
    ]


def countermodel_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "CAN1612_0_kernel_vector",
            "choose a nonzero allowed-looking source/material vector V in ker(K_CMSM)",
            "<K_CMSM,V>=0 despite V != 0",
            "blocks amplitude lower bound without dist(C,ker K)>0",
        ),
        (
            "CAN1612_1_signed_orbit_windows",
            "positive and negative orbit/session weights act on the same source profile",
            "time averages can cancel",
            "blocks sign-definite readout from density positivity alone",
        ),
        (
            "CAN1612_2_material_contrast",
            "Ti/Pt differential response has signed component contrasts",
            "material vector is not a one-dimensional positive scalar",
            "blocks positive-cone proof without component covariance rule",
        ),
        (
            "CAN1612_3_gradient_rotation",
            "gravity-gradient/inertia correction basis rotates the EP template",
            "projection can be reduced or sign-flipped",
            "blocks K sign proof without official correction arrays",
        ),
        (
            "CAN1612_4_mask_domain",
            "masks/windows alter readout support unless proven downstream-only",
            "domain selection can mimic or erase a residual",
            "blocks parent-domain proof",
        ),
        (
            "CAN1612_5_measured_G_absorption",
            "common-mode normalization can be absorbed into measured GM/G but differential residuals cannot",
            "a fake pass is possible if relative source weights are hidden",
            "blocks local-GR claim from normalization alone",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "countermodel_id": counter_id,
            "construction": construction,
            "math_result": result,
            "blocked_claim": blocked_claim,
            "status": "COUNTERMODEL_RETAINED",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for counter_id, construction, result, blocked_claim in rows
    ]


def sign_safe_requirement_rows() -> list[dict[str, Any]]:
    rows = [
        ("SSR1612_0_official_K", "official K_CMSM/readout arrays with units/sign convention", "MISSING_OFFICIAL_ARRAYS", "required to compute or sign the functional"),
        ("SSR1612_1_downstream_masks", "masks/orbit/windows proven downstream-only", "UNSIGNED", "prevents parent-domain selector shortcut"),
        ("SSR1612_2_material_cone", "Ti/Pt material/source response cone in the same branch basis", "MISSING_MATERIAL_TENSOR", "needed to define C"),
        ("SSR1612_3_covariance_margin", "covariance/no-cancellation rule showing dist(C,ker K)>0", "MISSING_MARGIN", "needed for c_min>0"),
        ("SSR1612_4_alignment_result", "K_norm, V_norm, projection_value, c_min, tau_min with uncertainty", "MISSING_ALIGNMENT_RESULT", "data route to the same theorem object"),
        ("SSR1612_5_no_shortcuts", "reject tau_eff=1, symbolic K alone, surrogate arrays, bound inversion and measured-G absorption", "FIREWALL_ACTIVE", "keeps branch honest"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "requirement_id": requirement_id,
            "required_input_or_clause": clause,
            "current_status": status,
            "why_it_matters": why,
            "parent_signed": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for requirement_id, clause, status, why in rows
    ]


def runner_rows(inventory: list[dict[str, Any]]) -> list[dict[str, Any]]:
    accepted = [row for row in inventory if truthy(row["accepted_for_quarantine"])]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1612_0_file_drop",
            "input_state": f"{len(accepted)} accepted nonclaim file rows",
            "runner_result": "SOURCE_FILES_ACCEPTED_NONCLAIM" if accepted else "NO_CMSM_FILE_DROP_ACCEPTED",
            "effect": "real files can feed 1613 loader if present; no claim promotion in 1612",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1612_1_no_cancellation",
            "input_state": "countermodels survive and sign-safe requirements remain unsigned",
            "runner_result": "REJECT_NO_CANCELLATION_THEOREM",
            "effect": "no c_min/tau_min lower bound follows",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    gates = [
        ("CG1612_0_file_drop", "official CMSM/source/readout files accepted", "BLOCKED", "no complete source pack/alignment set accepted for promotion"),
        ("CG1612_1_no_cancellation", "no-cancellation theorem", "BLOCKED", "kernel/sign/material/mask countermodels survive"),
        ("CG1612_2_cmin", "positive c_min/tau_min", "BLOCKED", "no parent-signed margin and no accepted alignment result"),
        ("CG1612_3_WEP", "WEP score", "BLOCKED", "readout/source/material/tau gates open"),
        ("CG1612_4_R10_local", "R10/local-GR/Newton claim", "BLOCKED", "source-normalization branch unresolved"),
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


def decision_rows(inventory: list[dict[str, Any]]) -> list[dict[str, Any]]:
    accepted = any(truthy(row["accepted_for_quarantine"]) for row in inventory)
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1612_0_file_drop",
            "decision": "SOURCE_FILE_DROP_ACCEPTED_NONCLAIM" if accepted else "NO_SOURCE_FILE_DROP_ACCEPTED",
            "reason": "all accepted rows remain quarantine-only" if accepted else "only missing/template/unrecognized inputs are present",
            "next_action": "run strict source-pack loader on accepted rows" if accepted else "supply/capture real CMSM files or keep deriving signed-margin theorem",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1612_1_no_cancellation",
            "decision": "NO_CANCELLATION_THEOREM_NOT_DERIVED",
            "reason": "exact c_min object identified but sign-safe cone/covariance/readout clauses are not parent-signed",
            "next_action": "derive signed-margin theorem or compute c_min from official K/V/alignment files",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1612_2_next",
            "decision": "NEXT_1613_CMSM_FILE_DROP_LOADER_OR_SIGNED_MARGIN_BOUND",
            "reason": "the cleanest next branch is a real file loader if data exists, otherwise a quantitative signed-margin proof attempt",
            "next_action": "build 1613 loader/margin-bound checkpoint without promoting any local claim",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "next_target": "1613-Y5-R2FR-CMSM-file-drop-loader-or-signed-margin-bound.md",
            "script": "scripts/Y5_R2FR_CMSM_file_drop_loader_or_signed_margin_bound.py",
            "objective": "load/validate any real CMSM file drops or derive a quantitative signed-margin bound for c_min",
            "success_condition": "validator-accepted official readout/material/alignment inputs as nonclaim rows, or parent-signed c_min>0 signed-margin theorem",
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
            for field in ("score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"):
                if truthy(row.get(field, "")):
                    return False
    return True


def no_formalization_1612() -> bool:
    if not FORMALIZATION.exists():
        return True
    artifact_markers = (
        "1612-Y5",
        "P8_Y5_PARENT_QLOC_1612",
        "P8_Y5_BRR545_1612",
        "Y5_R2FR_no_cancellation_theorem_or_CMSM_file_drop",
        "R2FR_no_cancellation",
        "R2FR_CMSM_file_drop",
    )
    return not any(any(marker in path.name for marker in artifact_markers) for path in FORMALIZATION.rglob("*"))


def validation_rows(generated_csvs: list[Path]) -> list[dict[str, Any]]:
    sources = source_register_rows()
    inventory = read_csv(FILE_DROP_INVENTORY)
    theorem = read_csv(NO_CANCELLATION)
    counters = read_csv(COUNTERMODEL)
    requirements = read_csv(SIGN_SAFE_REQUIREMENTS)
    runner = read_csv(RUNNER)
    gates = read_csv(CLAIM_GATE)
    decisions = read_csv(DECISION)
    copies = [target for targets in COPY_TARGETS.values() for target in targets]
    accepted = [row for row in inventory if truthy(row["accepted_for_quarantine"])]
    checks = [
        ("VAL1612_0_sources_exist", all(truthy(row["exists"]) for row in sources), "all cited 1612 local source paths exist"),
        ("VAL1612_1_needles_found", all(truthy(row["needle_found"]) for row in sources), "all required 1612 source needles found"),
        ("VAL1612_2_input_dir_ready", INPUT_1612.exists(), "1612 quarantine input directory exists for future CMSM file drops"),
        ("VAL1612_3_inventory_written", len(inventory) >= len(INPUT_DIRS) * len(EXPECTED_FILES), "file-drop inventory covers expected CMSM/readout/material/alignment roles"),
        ("VAL1612_4_accepted_rows_nonclaim", all(row["valid_for_claim"].lower() == "false" and row["claim_allowed"].lower() == "false" for row in accepted), "any accepted source rows remain nonclaim"),
        ("VAL1612_5_no_cancellation_not_derived", any(row["theorem_id"] == "NCT1612_5_verdict" and row["mathematical_status"] == "NO_CANCELLATION_THEOREM_NOT_DERIVED" for row in theorem), "no-cancellation theorem remains unproved"),
        ("VAL1612_6_countermodels_retained", len(counters) >= 6 and all(row["status"] == "COUNTERMODEL_RETAINED" for row in counters), "cancellation countermodels retained"),
        ("VAL1612_7_requirements_unsigned", all(row["parent_signed"].lower() == "false" for row in requirements), "sign-safe requirements remain unsigned"),
        ("VAL1612_8_runner_refuses", any(row["runner_id"] == "RUN1612_1_no_cancellation" and row["runner_result"] == "REJECT_NO_CANCELLATION_THEOREM" for row in runner), "runner rejects no-cancellation theorem"),
        ("VAL1612_9_claim_gates_closed", gates and all(row["claim_allowed"].lower() == "false" and row["status"] == "BLOCKED" for row in gates), "all 1612 claim gates remain closed"),
        ("VAL1612_10_decision_next", any(row["decision"] == "NEXT_1613_CMSM_FILE_DROP_LOADER_OR_SIGNED_MARGIN_BOUND" for row in decisions), "decision selects 1613 loader or signed-margin bound"),
        ("VAL1612_11_csv_parse", csv_parses(generated_csvs), "all generated 1612 CSVs parse"),
        ("VAL1612_12_claim_safety_flags", no_claim_flags(generated_csvs), "no generated 1612 rows are score-ready, prediction rows, valid-for-claim, or claim-allowed"),
        ("VAL1612_13_branch_copies", all(path.exists() for path in copies), "branch/quarantine nonclaim copies exist"),
        ("VAL1612_14_pycache_absent", not (Path(__file__).resolve().parent / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1612_15_formalization_untouched", no_formalization_1612(), "no 1612 outputs found under formalization-workbench"),
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
            "check_id": "VAL1612_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1612 no-cancellation theorem or CMSM file-drop validation",
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
    inventory: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    counters: list[dict[str, Any]],
    requirements: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n\n".join(
            [
                "# 1612 - R2/fR No-Cancellation Theorem Or CMSM File Drop",
                "## Verdict\n"
                "- 1612 tries the exact no-cancellation route first and does not close it.\n"
                "- The exact object is now clean: a positive signed-margin lower bound `c_min=inf |<K,V>|/(||K||||V||)` on the parent-allowed source/material cone.\n"
                "- Without a parent-signed cone disjoint from `ker(K_CMSM)` or official CMSM/readout/material/alignment files, cancellation countermodels survive.\n"
                "- The 1612 quarantine input folder is ready for real CMSM file drops, but current inputs are missing/template-only/unrecognized rather than claim-ready.\n"
                "- No WEP, R10, PPN, clock, orbital, Newton, local-GR, beta/coupling, or public claim is made.",
                "## Source Register",
                md_table(sources, ["source_id", "source_path", "exists", "needle_found", "needles"]),
                "## CMSM File Drop Inventory",
                md_table(inventory, ["inventory_id", "file_role", "exists", "validator_result", "reason", "accepted_for_quarantine"]),
                "## No-Cancellation Theorem Attempt",
                md_table(theorem, ["theorem_id", "mathematical_status", "what_is_exact", "blocking_gap", "theorem_closed"]),
                "## Cancellation Countermodel Audit",
                md_table(counters, ["countermodel_id", "construction", "math_result", "blocked_claim", "status"]),
                "## Sign-Safe Requirements",
                md_table(requirements, ["requirement_id", "required_input_or_clause", "current_status", "why_it_matters", "parent_signed"]),
                "## Runner Refusal",
                md_table(runner, ["runner_id", "input_state", "runner_result", "effect"]),
                "## Claim Gates",
                md_table(gates, ["gate_id", "claim", "status", "reason"]),
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
    INPUT_1612.mkdir(parents=True, exist_ok=True)
    sources = source_register_rows()
    inventory = file_drop_inventory_rows()
    theorem = no_cancellation_rows()
    counters = countermodel_rows()
    requirements = sign_safe_requirement_rows()
    runner = runner_rows(inventory)
    gates = claim_gate_rows()
    decisions = decision_rows(inventory)
    next_rows = next_target_rows()
    generated_csvs = [
        SOURCE_REGISTER,
        FILE_DROP_INVENTORY,
        NO_CANCELLATION,
        COUNTERMODEL,
        SIGN_SAFE_REQUIREMENTS,
        RUNNER,
        CLAIM_GATE,
        DECISION,
        NEXT_TARGET,
    ]
    write_csv(SOURCE_REGISTER, sources)
    write_csv(FILE_DROP_INVENTORY, inventory)
    write_csv(NO_CANCELLATION, theorem)
    write_csv(COUNTERMODEL, counters)
    write_csv(SIGN_SAFE_REQUIREMENTS, requirements)
    write_csv(RUNNER, runner)
    write_csv(CLAIM_GATE, gates)
    write_csv(DECISION, decisions)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()
    remove_pycache()
    validation = validation_rows(generated_csvs)
    write_csv(VALIDATION, validation)
    write_doc(sources, inventory, theorem, counters, requirements, runner, gates, decisions, next_rows, validation)


if __name__ == "__main__":
    main()
