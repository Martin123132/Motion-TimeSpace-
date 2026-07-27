from __future__ import annotations

import csv
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FORMALIZATION = ROOT.parent / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
RAB_SECTOR = ROOT / "source-intake" / "rab-sector"
QUEUE = RAB_SECTOR / "acquisition-queue"
QUARANTINE = MICROSCOPE / "quarantine" / "1678"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1678-Y5-R2FR-Rsource-parent-basis-and-WEP-R10-projection-acquisition.md"

SOURCE_FILES = {
    "1677_doc": ROOT / "1677-Y5-R2FR-single-action-scale-current-owner-or-Rsource-acquisition.md",
    "1677_validation": OUT / "P8_Y5_BRR545_1677_VALIDATION.csv",
    "1677_acquisition": OUT / "P8_Y5_PARENT_QLOC_1677_RSOURCE_ACQUISITION_ROWS_NONCLAIM.csv",
    "1677_projection": OUT / "P8_Y5_PARENT_QLOC_1677_ARENA_PROJECTION_REQUIREMENTS_NONCLAIM.csv",
    "1224_finite_contract": OUT / "P8_Y5_R10_1224_FINITE_SOURCE_WEIGHT_INPUT_CONTRACT.csv",
    "1224_product": OUT / "P8_Y5_R10_1224_SOURCE_WEIGHT_PRODUCT_LAW.csv",
    "1225_formula": OUT / "P8_Y5_R10_1225_SYMBOLIC_TAU_WEP_FORMULA.csv",
    "1225_acquisition": OUT / "P8_Y5_R10_1225_TAU_WEP_SOURCE_ACQUISITION_TABLE.csv",
    "1084_readout_gate": OUT / "P8_Y5_R10_1084_MICROSCOPE_READOUT_IMPORT_GATE.csv",
    "1084_profile_grid": OUT / "P8_Y5_R10_1084_SOURCE_PROFILE_WEIGHTING_GRID_NONCLAIM.csv",
    "1084_profile_gates": OUT / "P8_Y5_R10_1084_PROFILE_CLOSURE_GATES.csv",
    "1409_blockers": OUT / "P8_Y5_R10_1409_OFFICIAL_READOUT_BLOCKER_LEDGER.csv",
    "1310_qc_acquisition": OUT / "P8_Y5_R10_1310_QC_COEFFICIENT_ACQUISITION_NONCLAIM.csv",
    "1310_r10_bridge": OUT / "P8_Y5_R10_1310_R10_QC_TEMPLATE_BRIDGE_NONCLAIM.csv",
    "1076_owner_gates": OUT / "P8_Y5_R10_1076_COUPLING_OWNER_GATES.csv",
    "1416_first_rows": OUT / "P8_Y5_R10_1416_FIRST_RSOURCE_COEFFICIENT_ROW.csv",
}

NEEDLES = {
    "1677_doc": ["R_source parent basis", "1678-Y5-R2FR-Rsource-parent-basis-and-WEP-R10-projection-acquisition.md"],
    "1677_validation": ["VAL1677_OVERALL", "PASS"],
    "1677_acquisition": ["RSA1677_5_readout_kernel", "OFFICIAL_ARRAYS_NOT_IMPORTED"],
    "1677_projection": ["APR1677_2_R10", "MISSING_R10_SOURCE_PROJECTION"],
    "1224_finite_contract": ["FSW1224_4_readout_kernel", "OFFICIAL_ARRAYS_NOT_IMPORTED"],
    "1224_product": ["PROD1224_0_source_weight", "NOT_SCOREABLE"],
    "1225_formula": ["FORM1225_0_tau_WEP_functional", "SYMBOLIC_ONLY_NONCLAIM"],
    "1225_acquisition": ["ACQ1225_0_official_readout_arrays", "OFFICIAL_ARRAYS_NOT_IMPORTED"],
    "1084_readout_gate": ["RIG1084_0_CMSM_arrays", "OFFICIAL_ARRAYS_NOT_IMPORTED"],
    "1084_profile_grid": ["PROFILE1084_long_range_mass_average", "NUMERIC_PROFILE_WEIGHTING_SMOKE_NONCLAIM"],
    "1084_profile_gates": ["PCG1084_1_finite_range_profile", "MISSING_PREM_IMPORT_AND_LAMBDA_OWNER"],
    "1409_blockers": ["ORB1409_7_verdict", "UA_KERNEL_BLOCKED"],
    "1310_qc_acquisition": ["QCA1310_5_qbar_source_weight", "MISSING_SOURCE_WEIGHT_EXCLUSION_OR_COEFFICIENT"],
    "1310_r10_bridge": ["RTB1310_2_source_weight_alpha", "TEMPLATE_NONCLAIM_SOURCE_WEIGHT_ROW_CREATED"],
    "1076_owner_gates": ["OWN1076_0_parent_object_language", "MISSING_PARENT_COUPLING_BASIS"],
    "1416_first_rows": ["RSC1416_2_parent_basis", "MISSING_PARENT_COUPLING_BASIS"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1678_SOURCE_REGISTER.csv"
PARENT_BASIS_GATE = OUT / "P8_Y5_PARENT_QLOC_1678_RSOURCE_PARENT_BASIS_GATE.csv"
WEP_ACQUISITION = OUT / "P8_Y5_PARENT_QLOC_1678_WEP_PROJECTION_ACQUISITION_TABLE_NONCLAIM.csv"
NEWTON_ACQUISITION = OUT / "P8_Y5_PARENT_QLOC_1678_NEWTON_GM_PROJECTION_ACQUISITION_TABLE_NONCLAIM.csv"
R10_ACQUISITION = OUT / "P8_Y5_PARENT_QLOC_1678_R10_SOURCE_PROJECTION_ACQUISITION_TABLE_NONCLAIM.csv"
R11_ACQUISITION = OUT / "P8_Y5_PARENT_QLOC_1678_R11_SOURCE_OPERATOR_ACQUISITION_TABLE_NONCLAIM.csv"
BLOCKER_LEDGER = OUT / "P8_Y5_PARENT_QLOC_1678_CONSOLIDATED_BLOCKER_LEDGER.csv"
RUNNER_STUB = OUT / "P8_Y5_PARENT_QLOC_1678_RSOURCE_PROJECTION_RUNNER_STUB_NONCLAIM.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1678_DECISION.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1678_CLAIM_GATE.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1678_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1678_VALIDATION.csv"

GENERATED = [
    SOURCE_REGISTER,
    PARENT_BASIS_GATE,
    WEP_ACQUISITION,
    NEWTON_ACQUISITION,
    R10_ACQUISITION,
    R11_ACQUISITION,
    BLOCKER_LEDGER,
    RUNNER_STUB,
    DECISION,
    CLAIM_GATE,
    NEXT_TARGET,
]

CLAIM_CHECKED = [
    PARENT_BASIS_GATE,
    WEP_ACQUISITION,
    NEWTON_ACQUISITION,
    R10_ACQUISITION,
    R11_ACQUISITION,
    BLOCKER_LEDGER,
    RUNNER_STUB,
    DECISION,
    CLAIM_GATE,
    NEXT_TARGET,
]

COPY_TARGETS = {
    BLOCKER_LEDGER: [
        QUARANTINE / "CONSOLIDATED_BLOCKER_LEDGER.csv",
        BRANCH_RESIDUALS / "R2FR_Rsource_consolidated_blocker_ledger_1678.csv",
        QUEUE / "JR1678_CONSOLIDATED_BLOCKER_LEDGER.csv",
    ],
    WEP_ACQUISITION: [
        QUARANTINE / "WEP_PROJECTION_ACQUISITION_TABLE_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_WEP_projection_acquisition_nonclaim_1678.csv",
        QUEUE / "JR1678_WEP_PROJECTION_ACQUISITION_NONCLAIM.csv",
    ],
    R10_ACQUISITION: [
        QUARANTINE / "R10_SOURCE_PROJECTION_ACQUISITION_TABLE_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_R10_source_projection_acquisition_nonclaim_1678.csv",
        QUEUE / "JR1678_R10_SOURCE_PROJECTION_ACQUISITION_NONCLAIM.csv",
    ],
    NEXT_TARGET: [
        QUARANTINE / "NEXT_TARGET_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_next_target_nonclaim_1678.csv",
        QUEUE / "JR1678_NEXT_TARGET_NONCLAIM.csv",
    ],
}


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


def bool_cell(value: str | bool) -> bool:
    if isinstance(value, bool):
        return value
    return value.strip().lower() == "true"


def blocked_marker(value: object) -> bool:
    value_text = str(value)
    markers = ["MISSING_", "NOT_SCOREABLE", "NOT_IMPORTED", "NOT_DERIVED", "BLOCKED", "TEMPLATE_NONCLAIM"]
    return any(marker in value_text for marker in markers)


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
                "use_in_1678": "R_source parent-basis and WEP/Newton/R10/R11 projection acquisition",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def parent_basis_rows() -> list[dict[str, object]]:
    rows = [
        (
            "PBG1678_0_basis",
            "R_source parent basis X_I",
            "MISSING_PARENT_COUPLING_BASIS",
            "typed parent object language or explicit finite coupling basis",
        ),
        (
            "PBG1678_1_units",
            "source-current coordinate normalization and units",
            "MISSING_PARENT_SOURCE_CURRENT_UNITS",
            "dimensionless/source-current units for qbar_source_weight/current_rescaling/marker rows",
        ),
        (
            "PBG1678_2_owner",
            "source-current owner or finite residual declaration",
            "MISSING_CURRENT_OWNER",
            "Noether/current owner theorem or explicit retained finite coefficients",
        ),
        (
            "PBG1678_3_verdict",
            "parent source basis ready",
            "PARENT_BASIS_NOT_READY",
            "no arena projection may be claim-ready before basis/units are declared",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "required_object": required_object,
            "current_status": status,
            "promotion_requirement": requirement,
            "gate_pass": False,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for gate_id, required_object, status, requirement in rows
    ]


def acquisition_rows(table: str) -> list[dict[str, object]]:
    if table == "WEP":
        rows = [
            ("WEP1678_0_delta_w", "Delta_w_TiPt", "MISSING_NUMERIC_PRIOR_WIDTH", "dimensionless", "theorem-zero owner or finite Ti/Pt source-weight coefficient"),
            ("WEP1678_1_tau", "tau_WEP", "MISSING_LAB_SOURCE_ORBIT_PROJECTION", "dimensionless", "official/equivalent readout kernel, source worldtube, orbit average, material tensor"),
            ("WEP1678_2_arrays", "official CMSM/readout arrays", "OFFICIAL_ARRAYS_NOT_IMPORTED", "readout kernel", "time/segment/gx/gz/Sxx/Sxz/masks/calibration/attitude convention"),
            ("WEP1678_3_worldtube", "T_source^Earth(x)", "MISSING_SOURCE_PROFILE_WEIGHTING", "stress/profile", "PREM/source profile/composition/frame or theorem-reduced common mode"),
            ("WEP1678_4_material", "Ti/Pt material response tensor", "MISSING_FULL_MATERIAL_TENSOR", "material source response", "full tensor in same basis as R_source, not one-pair cancellation"),
            ("WEP1678_5_verdict", "WEP product readiness", "NOT_SCOREABLE", "dimensionless eta product", "all WEP1678 inputs source-backed and no-cancellation guard active"),
        ]
    elif table == "NEWTON":
        rows = [
            ("NEW1678_0_current_owner", "source-current owner", "MISSING_CURRENT_OWNER", "owner theorem", "single Hilbert source current or explicit finite residual"),
            ("NEW1678_1_GN", "single measured G_N normalization", "MISSING_SINGLE_GN_NORMALIZATION", "calibration convention", "common-mode absorption allowed only once"),
            ("NEW1678_2_Gauss", "Gauss/orbital source calibration", "MISSING_GAUSS_OR_ORBITAL_CALIBRATION", "DeltaGM projection", "source/current basis to measured GM map"),
            ("NEW1678_3_verdict", "Newton source projection readiness", "NOT_SCOREABLE", "DeltaGM/GM", "owner or source-backed projection rows"),
        ]
    elif table == "R10":
        rows = [
            ("R10S1678_0_coeff", "qbar_source_weight/current_rescaling/marker coefficients", "MISSING_COMPONENT_VALUES", "dimensionless", "theorem-zero or source-backed finite coefficients"),
            ("R10S1678_1_field_map", "R10 source field map", "MISSING_R10_SOURCE_PROJECTION", "alpha(lambda)", "source-current basis to alpha_source(lambda) map"),
            ("R10S1678_2_lambda", "lambda_X/source range owner", "MISSING_LAMBDA_OWNER", "length", "parent mass/range or scan convention with source path"),
            ("R10S1678_3_bound", "alpha_bound(lambda)", "BOUND_CURVE_REQUIRED_FOR_CLAIM", "dimensionless", "real bound curve/anchors with valid_for_claim policy"),
            ("R10S1678_4_verdict", "R10 source projection readiness", "NOT_SCOREABLE", "alpha(lambda)", "coefficients, source map, lambda, and bound curve all source-backed"),
        ]
    else:
        rows = [
            ("R11S1678_0_operator_basis", "R11 operator/source basis", "MISSING_R11_OPERATOR_SOURCE_BASIS", "operator units", "local non-EH/source operator basis"),
            ("R11S1678_1_projection", "R11 projection coefficients", "MISSING_R11_PROJECTION_COEFFICIENTS", "operator/source projection", "Pi_R11 source-current projection matrix"),
            ("R11S1678_2_current_owner", "source-current owner or residual", "MISSING_CURRENT_OWNER", "owner theorem or residual", "single current owner or finite source row"),
            ("R11S1678_3_verdict", "R11 source operator readiness", "NOT_SCOREABLE", "operator residual", "basis/projection/current rows source-backed"),
        ]
    return [
        {
            "branch_id": BRANCH_ID,
            "acquisition_id": acquisition_id,
            "needed_object": needed_object,
            "current_status": status,
            "units_or_convention": units,
            "promotion_requirement": requirement,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for acquisition_id, needed_object, status, units, requirement in rows
    ]


def blocker_rows() -> list[dict[str, object]]:
    blockers = [
        ("BLK1678_0_parent_basis", "R_source parent basis/units", "MISSING_PARENT_COUPLING_BASIS", "blocks all finite source projections"),
        ("BLK1678_1_WEP_readout", "official/equivalent MICROSCOPE readout arrays", "OFFICIAL_ARRAYS_NOT_IMPORTED", "blocks tau_WEP and WEP product"),
        ("BLK1678_2_WEP_source", "source worldtube/profile/material tensor", "MISSING_SOURCE_PROFILE_WEIGHTING", "blocks source side of tau_WEP"),
        ("BLK1678_3_Newton", "source-current/G_N/Gauss calibration", "MISSING_SOURCE_CURRENT_OWNER_AND_GAUSS_CALIBRATION", "blocks Newton source normalization"),
        ("BLK1678_4_R10", "R10 source field map/lambda/bound curve", "MISSING_R10_SOURCE_PROJECTION", "blocks short-range source alpha"),
        ("BLK1678_5_R11", "R11 source operator basis/projection", "MISSING_R11_OPERATOR_SOURCE_BASIS", "blocks operator/source residual"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "blocker_id": blocker_id,
            "missing_object": missing_object,
            "status": status,
            "effect": effect,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for blocker_id, missing_object, status, effect in blockers
    ]


def runner_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "runner_id": "RUN1678_0_Rsource_projection_runner_stub",
            "runner_status": "DRY_RUN_SCHEMA_ONLY",
            "inputs": "PARENT_BASIS_GATE;WEP_ACQUISITION;NEWTON_ACQUISITION;R10_ACQUISITION;R11_ACQUISITION",
            "acceptance_rule": "run only after required rows have source-backed values/units/projections or theorem-zero status; claim false while any blocker remains",
            "current_status": "BLOCKED_BY_PARENT_BASIS_AND_PROJECTION_INPUTS",
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def decision_rows() -> list[dict[str, object]]:
    rows = [
        ("D1678_0_basis", "PARENT_BASIS_FIRST", "without R_source basis/units no arena projection has meaning", "derive/fill parent basis before scoring"),
        ("D1678_1_WEP", "WEP_DATA_NOT_SCORE_READY", "official/equivalent readout arrays, source worldtube, material tensor, and Delta_w are missing", "source-block WEP rather than claim"),
        ("D1678_2_R10", "R10_SOURCE_PROJECTION_NOT_READY", "source coefficients and source field map/lambda/bound curve are not claim-ready", "keep R10 source branch nonclaim"),
        ("D1678_3_safety", "NO_LOCAL_GR_SOURCE_CLAIM", "finite source branch has acquisition rows but no source-backed runner inputs", "keep all source/local claim gates false"),
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
    gates = [
        ("CG1678_0_basis", "R_source parent basis/units source-backed", False, "BLOCKED", "parent basis missing"),
        ("CG1678_1_WEP", "WEP finite source product score-ready", False, "BLOCKED", "official/readout/source/material inputs missing"),
        ("CG1678_2_Newton", "Newton source normalization score-ready", False, "BLOCKED", "current/G_N/Gauss calibration missing"),
        ("CG1678_3_R10", "R10 source projection score-ready", False, "BLOCKED", "source map/lambda/bound curve missing"),
        ("CG1678_4_R11", "R11 source operator score-ready", False, "BLOCKED", "operator basis/projection missing"),
        ("CG1678_5_local_GR", "GR/Newton source side derived or bounded", False, "BLOCKED", "source branch is acquisition-only"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "gate": gate,
            "gate_pass": gate_pass,
            "status": status,
            "reason": reason,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for gate_id, gate, gate_pass, status, reason in gates
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "next_target": "1679-Y5-R2FR-parent-Rsource-basis-minimal-symbolic-map-or-data-probe.md",
            "script": "scripts/Y5_R2FR_parent_Rsource_basis_minimal_symbolic_map_or_data_probe.py",
            "objective": "try to construct the minimal symbolic R_source parent basis from the MTS parent variables; if it fails, prepare a dry-run data probe for official/equivalent WEP readout and R10 bound/source projection inputs",
            "success_condition": "either the R_source basis/units are parent-signed, or the data-probe ledger identifies exact source URLs/files/blockers without turning any row claim-ready",
            "why_next": "1678 shows all finite source tests depend first on the parent basis and only then on readout/projection data",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def copy_outputs() -> None:
    for source_path, target_paths in COPY_TARGETS.items():
        for target_path in target_paths:
            target_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source_path, target_path)


def validate() -> list[dict[str, object]]:
    source_rows = read_csv(SOURCE_REGISTER)
    basis_rows = read_csv(PARENT_BASIS_GATE)
    wep_rows = read_csv(WEP_ACQUISITION)
    newton_rows = read_csv(NEWTON_ACQUISITION)
    r10_rows = read_csv(R10_ACQUISITION)
    r11_rows = read_csv(R11_ACQUISITION)
    blockers = read_csv(BLOCKER_LEDGER)
    runners = read_csv(RUNNER_STUB)
    decisions = read_csv(DECISION)
    claims = read_csv(CLAIM_GATE)
    next_rows = read_csv(NEXT_TARGET)

    sources_ok = all(bool_cell(row["exists"]) and bool_cell(row["needles_present"]) for row in source_rows)
    basis_blocked = any(row["gate_id"] == "PBG1678_3_verdict" and row["current_status"] == "PARENT_BASIS_NOT_READY" for row in basis_rows)
    wep_complete = {"Delta_w_TiPt", "tau_WEP", "official CMSM/readout arrays", "T_source^Earth(x)", "Ti/Pt material response tensor", "WEP product readiness"} == {row["needed_object"] for row in wep_rows}
    newton_complete = {"source-current owner", "single measured G_N normalization", "Gauss/orbital source calibration", "Newton source projection readiness"} == {row["needed_object"] for row in newton_rows}
    r10_complete = len(r10_rows) == 5 and any(row["needed_object"] == "R10 source field map" for row in r10_rows)
    r11_complete = len(r11_rows) == 4 and any(row["needed_object"] == "R11 operator/source basis" for row in r11_rows)
    blockers_complete = len(blockers) == 6 and all(row["status"] for row in blockers)
    runner_blocked = runners[0]["runner_status"] == "DRY_RUN_SCHEMA_ONLY" and runners[0]["current_status"] == "BLOCKED_BY_PARENT_BASIS_AND_PROJECTION_INPUTS"
    decision_next = any(row["decision"] == "PARENT_BASIS_FIRST" for row in decisions)
    claim_gate_safe = all(not bool_cell(row["gate_pass"]) and not bool_cell(row["claim_allowed"]) for row in claims)
    next_target_selected = next_rows[0]["next_target"] == "1679-Y5-R2FR-parent-Rsource-basis-minimal-symbolic-map-or-data-probe.md"
    csv_parse = all(path.exists() and len(read_csv(path)) >= 1 for path in GENERATED)
    branch_copies = all(target_path.exists() for target_paths in COPY_TARGETS.values() for target_path in target_paths)
    pycache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    formalization_clean = not any(FORMALIZATION.rglob("*1678*")) if FORMALIZATION.exists() else True

    no_claim_flags = True
    blocked_not_ready = True
    for generated_path in CLAIM_CHECKED:
        for generated_row in read_csv(generated_path):
            if generated_row.get("valid_for_claim", "False").lower() == "true" or generated_row.get("claim_allowed", "False").lower() == "true":
                no_claim_flags = False
            if any(blocked_marker(value) for value in generated_row.values()):
                for claim_key in ["valid_for_claim", "claim_allowed", "score_ready", "accepted_for_scoring", "valid_prediction_row"]:
                    if claim_key in generated_row and bool_cell(generated_row[claim_key]):
                        blocked_not_ready = False

    checks = [
        ("VAL1678_0_sources_exist", sources_ok, "all cited 1678 source paths exist and needles are present"),
        ("VAL1678_1_basis_blocked", basis_blocked, "R_source parent basis remains not ready"),
        ("VAL1678_2_wep_complete", wep_complete, "WEP acquisition rows cover Delta_w/tau/arrays/worldtube/material/verdict"),
        ("VAL1678_3_newton_complete", newton_complete, "Newton projection acquisition rows are present"),
        ("VAL1678_4_r10_complete", r10_complete, "R10 source projection acquisition rows are present"),
        ("VAL1678_5_r11_complete", r11_complete, "R11 source operator acquisition rows are present"),
        ("VAL1678_6_blockers_complete", blockers_complete, "consolidated blocker ledger has six active blockers"),
        ("VAL1678_7_runner_blocked", runner_blocked, "runner remains dry-run schema only"),
        ("VAL1678_8_decision_next", decision_next, "decision selects parent basis first"),
        ("VAL1678_9_claim_gate_safe", claim_gate_safe, "all claim gates keep source/local claims false"),
        ("VAL1678_10_no_claim_flags", no_claim_flags, "all generated rows keep claim flags false"),
        ("VAL1678_11_blocked_not_ready", blocked_not_ready, "no blocked/missing row is marked claim/scoring ready"),
        ("VAL1678_12_next_target_selected", next_target_selected, "next target selects parent R_source basis or data probe"),
        ("VAL1678_13_csv_parse", csv_parse, "all generated 1678 CSVs parse"),
        ("VAL1678_14_branch_copies", branch_copies, "branch/quarantine/queue copies exist"),
        ("VAL1678_15_pycache_absent", pycache_absent, "scripts __pycache__ absent"),
        ("VAL1678_16_formalization_untouched", formalization_clean, "no 1678 outputs found under formalization-workbench"),
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
            "check_id": "VAL1678_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1678 R_source parent-basis and projection acquisition validation",
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
    basis_rows: list[dict[str, object]],
    wep_rows: list[dict[str, object]],
    newton_rows: list[dict[str, object]],
    r10_rows: list[dict[str, object]],
    r11_rows: list[dict[str, object]],
    blocker_rows_: list[dict[str, object]],
    runner_rows_: list[dict[str, object]],
    decision_rows_: list[dict[str, object]],
    claim_rows: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    validation_rows: list[dict[str, object]],
) -> None:
    body = f"""# 1678 - Rsource Parent Basis And WEP/R10 Projection Acquisition

**Private status:** finite source-side acquisition/projection pack. No `q_loc=0`, local-GR pass, Newton pass, PPN pass, R10 pass, WEP pass, clock pass, orbital pass, or public claim is made.

## Verdict

The finite `R_source` branch is now projection-plumbed but **not score-ready**.

The first blocker is still the parent source basis: without `R_source` basis/units, WEP/Newton/R10/R11 projections are not meaningful numbers. WEP additionally needs official or exactly equivalent readout arrays, source worldtube/profile, material response tensor, and `Delta_w`; R10 needs source coefficients, field map, range owner, and bound curve.

## Source Register

{markdown_table(source_rows, ["source_key", "source_path", "exists", "needles_present", "use_in_1678"])}

## Parent Basis Gate

{markdown_table(basis_rows, ["gate_id", "required_object", "current_status", "promotion_requirement"])}

## WEP Projection Acquisition

{markdown_table(wep_rows, ["acquisition_id", "needed_object", "current_status", "units_or_convention", "promotion_requirement"])}

## Newton-GM Projection Acquisition

{markdown_table(newton_rows, ["acquisition_id", "needed_object", "current_status", "units_or_convention", "promotion_requirement"])}

## R10 Source Projection Acquisition

{markdown_table(r10_rows, ["acquisition_id", "needed_object", "current_status", "units_or_convention", "promotion_requirement"])}

## R11 Source Operator Acquisition

{markdown_table(r11_rows, ["acquisition_id", "needed_object", "current_status", "units_or_convention", "promotion_requirement"])}

## Consolidated Blocker Ledger

{markdown_table(blocker_rows_, ["blocker_id", "missing_object", "status", "effect"])}

## Runner Stub

{markdown_table(runner_rows_, ["runner_id", "runner_status", "inputs", "current_status"])}

## Decisions

{markdown_table(decision_rows_, ["decision_id", "decision", "reason", "next_action"])}

## Claim Gates

{markdown_table(claim_rows, ["gate_id", "gate", "gate_pass", "status", "reason"])}

## Next Target

{markdown_table(next_rows, ["next_target", "script", "objective", "success_condition"])}

## Validation

{markdown_table(validation_rows, ["check_id", "result", "detail"])}

## Working Interpretation

This checkpoint turns the source-side problem into an engineering board. The first switch is not the MICROSCOPE arrays; it is the parent `R_source` basis. After that, WEP data and R10 projections become meaningful. Before that, numbers would be a costume party.
"""
    DOC.write_text(body, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    source_rows = source_register_rows()
    basis_rows = parent_basis_rows()
    wep_rows = acquisition_rows("WEP")
    newton_rows = acquisition_rows("NEWTON")
    r10_rows = acquisition_rows("R10")
    r11_rows = acquisition_rows("R11")
    blockers = blocker_rows()
    runner_stub = runner_rows()
    decisions = decision_rows()
    claims = claim_gate_rows()
    next_rows = next_target_rows()

    write_csv(
        SOURCE_REGISTER,
        source_rows,
        ["branch_id", "source_key", "source_path", "exists", "needles_present", "required_needles", "use_in_1678", "valid_for_claim", "claim_allowed"],
    )
    write_csv(
        PARENT_BASIS_GATE,
        basis_rows,
        ["branch_id", "gate_id", "required_object", "current_status", "promotion_requirement", "gate_pass", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"],
    )
    for path, rows in [
        (WEP_ACQUISITION, wep_rows),
        (NEWTON_ACQUISITION, newton_rows),
        (R10_ACQUISITION, r10_rows),
        (R11_ACQUISITION, r11_rows),
    ]:
        write_csv(
            path,
            rows,
            ["branch_id", "acquisition_id", "needed_object", "current_status", "units_or_convention", "promotion_requirement", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"],
        )
    write_csv(BLOCKER_LEDGER, blockers, ["branch_id", "blocker_id", "missing_object", "status", "effect", "valid_for_claim", "claim_allowed"])
    write_csv(
        RUNNER_STUB,
        runner_stub,
        ["branch_id", "runner_id", "runner_status", "inputs", "acceptance_rule", "current_status", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"],
    )
    write_csv(DECISION, decisions, ["branch_id", "decision_id", "decision", "reason", "next_action", "valid_for_claim", "claim_allowed"])
    write_csv(CLAIM_GATE, claims, ["branch_id", "gate_id", "gate", "gate_pass", "status", "reason", "valid_for_claim", "claim_allowed"])
    write_csv(NEXT_TARGET, next_rows, ["branch_id", "next_target", "script", "objective", "success_condition", "why_next", "valid_for_claim", "claim_allowed"])

    copy_outputs()
    validation_rows = validate()
    write_csv(VALIDATION, validation_rows, ["check_id", "result", "detail", "valid_for_claim", "claim_allowed"])
    write_doc(source_rows, basis_rows, wep_rows, newton_rows, r10_rows, r11_rows, blockers, runner_stub, decisions, claims, next_rows, validation_rows)

    failed_rows = [row for row in validation_rows if row["result"] != "PASS"]
    print(f"wrote {DOC}")
    print(f"wrote {VALIDATION}")
    if failed_rows:
        for failed_row in failed_rows:
            print(f"FAIL {failed_row['check_id']}: {failed_row['detail']}")
        raise SystemExit(1)
    print("1678 validation PASS")


if __name__ == "__main__":
    main()
