from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from Y5_R10_alpha_product_prediction_stub_runner_and_required_inputs import (
    BOUND_REQUIRED_COLUMNS,
    PRODUCT_REQUIRED_COLUMNS,
    run_product_runner,
)


STARTED = datetime.now(timezone.utc)
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds" / "local_bound_claims.csv"
DOC = ROOT / "1082-Y5-R10-parent-to-DD-coefficient-map-or-physical-source-readout-fill.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_DIR = ROOT / "runs" / "1082-parent-to-DD-coefficient-map-or-physical-source-readout-fill" / "results"
PRODUCT_RUN_DIR = RUN_DIR / "product_runner"
PREDICTION_TEMPLATE = OUT / "P8_Y5_R10_1082_WEP_PRODUCT_CANDIDATE_NONCLAIM.csv"
BOUND_IMPORT = OUT / "P8_Y5_R10_1082_WEP_BOUND_IMPORT.csv"
DD_SMOKE = OUT / "P8_Y5_R10_1081_DD_UNIT_RESPONSE_SMOKE_RUNNER.csv"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def source_path(path_text: str) -> Path:
    path = Path(path_text)
    if path.is_absolute():
        return path
    return ROOT / path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def md_cell(value: object) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def md_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    return "\n".join(
        [
            "| " + " | ".join(columns) + " |",
            "| " + " | ".join("---" for _ in columns) + " |",
            *["| " + " | ".join(md_cell(row.get(column, "")) for column in columns) + " |" for row in rows],
        ]
    ) + "\n"


def count_formalization_modified_since_start() -> int:
    if not FORMALIZATION.exists():
        return 0
    return sum(
        1
        for path in FORMALIZATION.rglob("*")
        if path.is_file() and datetime.fromtimestamp(path.stat().st_mtime, timezone.utc) >= STARTED
    )


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def local_bound_row(row_id: str) -> dict[str, str]:
    for row in read_csv(LOCAL_BOUNDS):
        if row.get("row_id") == row_id:
            return row
    raise ValueError(f"missing local bound row {row_id}")


def split_reference(reference: str) -> tuple[str, str]:
    parts = [part.strip() for part in reference.split(";")]
    url = next((part for part in parts if part.startswith("http")), "")
    doi = next((part.replace("doi:", "").strip() for part in parts if part.lower().startswith("doi:")), "")
    return url, doi


def source_register_rows() -> list[dict[str, str]]:
    specs = [
        ("SRC1082_0_1081_next", "source-intake/mts_residuals/P8_Y5_R10_1081_NEXT_TARGET.csv", "1082-Y5-R10-parent-to-DD-coefficient-map-or-physical-source-readout-fill.md", "1081 handoff."),
        ("SRC1082_1_1081_validation", "source-intake/mts_residuals/P8_Y5_BRR545_1081_VALIDATION.csv", "V1081_SUMMARY", "1081 validation summary."),
        ("SRC1082_2_1081_parent_basis", "source-intake/mts_residuals/P8_Y5_R10_1081_PARENT_WEP_BASIS_DERIVATION_ATTEMPT.csv", "PB1081_4_verdict", "parent WEP basis failure."),
        ("SRC1082_3_1081_DD_basis", "source-intake/mts_residuals/P8_Y5_R10_1081_DD_BASIS_SCHEMA.csv", "DDB1081_0_alpha_Coulomb", "DD basis schema."),
        ("SRC1082_4_1081_proxy", "source-intake/mts_residuals/P8_Y5_R10_1081_DD_SOURCE_PROXY_POLICY.csv", "SPP1081_0_unit_source_proxy", "source/readout proxy policy."),
        ("SRC1082_5_1081_delta", "source-intake/mts_residuals/P8_Y5_R10_1081_DD_MATERIAL_DELTA_IMPORT.csv", "DDM1081_0_delta_alpha", "DD material delta import."),
        ("SRC1082_6_1081_smoke", "source-intake/mts_residuals/P8_Y5_R10_1081_DD_UNIT_RESPONSE_SMOKE_RUNNER.csv", "DDS1081_0_alpha_unit", "DD unit-response smoke rows."),
        ("SRC1082_7_1081_pdd", "source-intake/mts_residuals/P8_Y5_R10_1081_PARENT_TO_DD_GATE.csv", "PDD1081_1_coefficient_map", "parent-to-DD gates."),
        ("SRC1082_8_1080_earth", "source-intake/mts_residuals/P8_Y5_R10_1080_EARTH_SOURCE_VECTOR_CANDIDATES.csv", "EARTH1080_2_parent_basis_block", "Earth source vector candidates."),
        ("SRC1082_9_1080_readout", "source-intake/mts_residuals/P8_Y5_R10_1080_MICROSCOPE_READOUT_GATE.csv", "READ1080_1_CMSM_portal", "readout gate."),
        ("SRC1082_10_local_bounds", "source-intake/local_bounds/local_bound_claims.csv", "R1_WEP_source_charge", "MICROSCOPE WEP bound row."),
    ]
    rows: list[dict[str, str]] = []
    for source_id, relative_path, needle, note in specs:
        path = source_path(relative_path)
        exists = path.exists()
        needle_found = exists and needle in read_text(path)
        rows.append(
            {
                "source_id": source_id,
                "relative_path": relative_path,
                "absolute_path": str(path),
                "exists": str(exists).lower(),
                "needle": needle,
                "needle_found": str(needle_found).lower(),
                "note": note,
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def parent_to_dd_map_attempt_rows() -> list[dict[str, str]]:
    return [
        {
            "map_id": "PTD1082_0_target",
            "claim": "derive C_parent -> (c_alpha,c_surface)",
            "needed_parent_object": "local WEP coupling basis with explicit EM/Coulomb and nuclear surface/binding slots",
            "proof_attempt": "search for an MTS parent operator decomposition that naturally selects the two DD components",
            "result": "TARGET_SHARPENED",
            "gap": "the map must specify basis, units, signs, source normalization, and readout placement",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "map_id": "PTD1082_1_alpha_channel",
            "claim": "MTS alpha/EM sector maps to DD Q_alpha_Coulomb",
            "needed_parent_object": "signed parent EM/fine-structure response operator with material charge pullback",
            "proof_attempt": "use the existence of EM/charge work as a candidate parent slot",
            "result": "NOT_SIGNED",
            "gap": "no source-backed operator pullback from MTS EM sector to DD Q_alpha_Coulomb is present",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "map_id": "PTD1082_2_surface_channel",
            "claim": "MTS binding/mass sector maps to DD Q_surface_binding",
            "needed_parent_object": "signed nuclear/surface/binding response operator with material tensor pullback",
            "proof_attempt": "treat surface/binding row as a possible residual mass/binding channel",
            "result": "NOT_SIGNED",
            "gap": "no parent nuclear/binding operator or coefficient normalization is derived",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "map_id": "PTD1082_3_units_and_sign",
            "claim": "C_parent units and sign convention match DD proxy coefficients",
            "needed_parent_object": "dimensionless coefficient vector in the DD charge convention",
            "proof_attempt": "compare 1081 coefficient-normalized smoke rows to parent C_parent contract",
            "result": "MISSING_UNITS_MAP",
            "gap": "C_parent is basis-dependent and no parent action coefficient dimension/sign is fixed",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "map_id": "PTD1082_4_verdict",
            "claim": "parent-to-DD coefficient map is derived",
            "needed_parent_object": "C_parent -> (c_alpha,c_surface) plus same-basis source/readout normalization",
            "proof_attempt": "assemble alpha, surface, units, sign, and source/readout conditions",
            "result": "PARENT_TO_DD_MAP_NOT_DERIVED",
            "gap": "DD branch remains an external comparator unless future parent operator/basis work closes it",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def coefficient_units_contract_rows() -> list[dict[str, str]]:
    smoke_by_symbol = {row["coefficient_symbol"]: row for row in read_csv(DD_SMOKE)}
    return [
        {
            "coefficient_id": "CUC1082_0_c_alpha_proxy",
            "coefficient_symbol": "c_alpha_proxy",
            "basis": "DD Q_alpha_Coulomb unit-response smoke convention",
            "units": "dimensionless per unit source/readout proxy",
            "bound_or_value": smoke_by_symbol["c_alpha_proxy"]["required_abs_coefficient_max"],
            "source_row": "DDS1081_0_alpha_unit",
            "status": "NUMERIC_SMOKE_BOUND_NONCLAIM",
            "missing_for_claim": "MTS-to-DD coefficient map and physical source/readout normalization",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "coefficient_id": "CUC1082_1_c_surface_proxy",
            "coefficient_symbol": "c_surface_proxy",
            "basis": "DD Q_surface_binding unit-response smoke convention",
            "units": "dimensionless per unit source/readout proxy",
            "bound_or_value": smoke_by_symbol["c_surface_proxy"]["required_abs_coefficient_max"],
            "source_row": "DDS1081_1_surface_unit",
            "status": "NUMERIC_SMOKE_BOUND_NONCLAIM",
            "missing_for_claim": "MTS-to-DD coefficient map and physical source/readout normalization",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "coefficient_id": "CUC1082_2_c_equal_proxy",
            "coefficient_symbol": "c_equal_proxy",
            "basis": "DD equal alpha+surface unit-response smoke convention",
            "units": "dimensionless per unit source/readout proxy",
            "bound_or_value": smoke_by_symbol["c_equal_proxy"]["required_abs_coefficient_max"],
            "source_row": "DDS1081_2_equal_two_component_unit",
            "status": "NUMERIC_SMOKE_BOUND_NONCLAIM",
            "missing_for_claim": "MTS-to-DD coefficient map and physical source/readout normalization",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "coefficient_id": "CUC1082_3_C_parent",
            "coefficient_symbol": "C_parent",
            "basis": "MTS parent WEP basis",
            "units": "MISSING_PARENT_UNITS",
            "bound_or_value": "MISSING_PARENT_COEFFICIENT_VECTOR",
            "source_row": "PTD1082_4_verdict",
            "status": "MISSING_FOR_CLAIM",
            "missing_for_claim": "parent action coefficient extraction",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def physical_earth_source_fill_rows() -> list[dict[str, str]]:
    return [
        {
            "fill_id": "ESF1082_0_reference",
            "object": "Earth source composition reference",
            "candidate_source": "WEB1080_2_MCDONOUGH_SUN_1995",
            "needed_content": "bulk Earth or shell-weighted elemental composition table with uncertainties",
            "current_status": "REFERENCE_IDENTIFIED_NOT_EXTRACTED",
            "claim_blocker": "no numeric DD/MTS source vector",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "fill_id": "ESF1082_1_vectorization",
            "object": "R_source^Earth in DD alpha/surface basis",
            "candidate_source": "Damour-Donoghue charge formulas plus Earth composition table",
            "needed_content": "compute Q_alpha_Coulomb^Earth and Q_surface_binding^Earth or justify common-mode cancellation",
            "current_status": "NOT_VECTORIZED",
            "claim_blocker": "source leg cannot remain unit proxy",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "fill_id": "ESF1082_2_profile",
            "object": "source profile/worldtube weighting",
            "candidate_source": "Earth gravity/source model in MICROSCOPE orbit",
            "needed_content": "which Earth layers/source components couple to the measured acceleration channel",
            "current_status": "MISSING_PROFILE_WEIGHTING",
            "claim_blocker": "bulk composition alone may not be the measured source vector",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "fill_id": "ESF1082_3_no_absorption",
            "object": "no measured-G absorption rule",
            "candidate_source": "claim policy",
            "needed_content": "source vector is explicit or theorem-common-mode; it is not absorbed into measured G",
            "current_status": "RULE_RETAINED",
            "claim_blocker": "any shortcut would invalidate finite branch",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def physical_readout_fill_rows() -> list[dict[str, str]]:
    return [
        {
            "fill_id": "ROF1082_0_official_arrays",
            "object": "K_MICROSCOPE official arrays",
            "candidate_source": "CMSM data portal / official export",
            "needed_content": "gx, gz, Sxx, Sxz, segment masks, timing, and calibration/readout convention",
            "current_status": "OFFICIAL_ARRAYS_NOT_IMPORTED",
            "claim_blocker": "unit readout proxy cannot be physical tau_WEP",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "fill_id": "ROF1082_1_surrogate_reuse",
            "object": "surrogate readout matrix",
            "candidate_source": "P8_Y5_R10_1075_TAU_SHAPE_STATUS.csv",
            "needed_content": "surrogate can test algebra only",
            "current_status": "SURROGATE_AVAILABLE_NONCLAIM",
            "claim_blocker": "surrogate matrix cannot replace official readout for claim",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "fill_id": "ROF1082_2_normalization",
            "object": "readout normalization into eta_AB",
            "candidate_source": "MICROSCOPE measurement equation",
            "needed_content": "normalization from source-response product to reported Eotvos parameter",
            "current_status": "MODEL_STRUCTURE_KNOWN_NORMALIZATION_NOT_FILLED",
            "claim_blocker": "no physical projection scalar or kernel",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def dd_smoke_reuse_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for row in read_csv(DD_SMOKE):
        rows.append(
            {
                "reuse_id": row["smoke_id"].replace("DDS1081", "REUSE1082"),
                "source_smoke_id": row["smoke_id"],
                "component": row["component"],
                "unit_response_abs": row["unit_response_abs"],
                "required_abs_coefficient_max": row["required_abs_coefficient_max"],
                "reuse_policy": "algebra/pipeline smoke only",
                "promotion_blocker": "parent-to-DD map and physical source/readout normalization missing",
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def product_prediction_rows() -> list[dict[str, str]]:
    return [
        {
            "prediction_id": "PRED1082_0_parent_to_DD_or_physical_fill_missing",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "P_WEP_relative_source_weight",
            "product_value": "MISSING_PARENT_TO_DD_MAP_AND_PHYSICAL_EARTH_SOURCE_READOUT",
            "product_units": "dimensionless",
            "product_source": "source-intake/mts_residuals/P8_Y5_R10_1082_PARENT_TO_DD_COEFFICIENT_MAP_ATTEMPT.csv",
            "inputs_present": "DD smoke unit-response rows; coefficient-unit contract; source/readout fill contracts",
            "required_inputs": "parent-to-DD map; physical R_source^Earth; official/validated K_MICROSCOPE; C_parent vector",
            "derivation_status": "MAP_UNSIGNED_PHYSICAL_FILL_MISSING",
            "valid_for_claim": "false",
            "notes": "generic product runner must refuse; this checkpoint only narrows the missing locks",
        }
    ]


def bound_rows() -> list[dict[str, str]]:
    row = local_bound_row("R1_WEP_source_charge")
    url, doi = split_reference(row.get("reference_path_or_url", ""))
    return [
        {
            "bound_id": "BOUND1082_0_MICROSCOPE_WEP_source_charge",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "P_WEP_relative_source_weight",
            "bound_value": row["upper_bound"],
            "bound_units": row["units"],
            "bound_source": url,
            "source_row": f"{row['dataset_id']}:{row['row_id']};doi:{doi}",
            "bound_type": "upper_abs_WEP_proxy_bound",
            "valid_for_claim": "true",
            "notes": "source-backed numeric bound only; parent-to-DD prediction remains invalid",
        }
    ]


def product_status_rows(status: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "runner_id": "APR1082_0_parent_to_DD_product_stub",
            "prediction_rows": str(status.get("prediction_rows", "")),
            "bound_rows": str(status.get("bound_rows", "")),
            "valid_prediction_rows": str(status.get("valid_prediction_rows", "")),
            "valid_bound_rows": str(status.get("valid_bound_rows", "")),
            "comparison_rows": str(status.get("comparison_rows", "")),
            "passed_rows": str(status.get("passed_rows", "")),
            "claim_allowed": str(status.get("claim_allowed", "")).lower(),
            "expected_result": "reject missing parent-to-DD map and physical source/readout",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def claim_gate_rows(product_status: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "gate_id": "CG1082_0_parent_to_DD_map",
            "claim_component": "C_parent -> DD coefficient map",
            "gate_pass": "false",
            "claim_allowed": "false",
            "reason": "PTD1082_4_verdict=PARENT_TO_DD_MAP_NOT_DERIVED",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1082_1_DD_smoke_reuse",
            "claim_component": "DD smoke runner reuse",
            "gate_pass": "true",
            "claim_allowed": "false",
            "reason": "DD unit-response rows are reusable for algebra only",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1082_2_earth_source",
            "claim_component": "physical R_source^Earth",
            "gate_pass": "false",
            "claim_allowed": "false",
            "reason": "Earth source reference not extracted/vectorized/profile-weighted",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1082_3_readout",
            "claim_component": "physical K_MICROSCOPE",
            "gate_pass": "false",
            "claim_allowed": "false",
            "reason": "official arrays not imported and surrogate is nonclaim",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1082_4_product_runner",
            "claim_component": "WEP product runner",
            "gate_pass": "false",
            "claim_allowed": str(product_status.get("claim_allowed", "")).lower(),
            "reason": f"valid_prediction_rows={product_status.get('valid_prediction_rows')}",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC1082_0_map_failed",
            "decision": "parent-to-DD coefficient map remains unsigned",
            "because": "MTS has no signed alpha/surface operator pullback or coefficient unit/sign map",
            "next_action": "do not promote DD smoke to MTS prediction",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1082_1_physical_fill",
            "decision": "physical source/readout fill is the next empirical scaffold",
            "because": "unit proxy rows are useful but nonphysical; Earth source and official readout are the next concrete data locks",
            "next_action": "build Earth-source vector extraction plan and CMSM readout import/checklist",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1082_2_priority",
            "decision": "prioritize physical Earth source vector before official arrays if limited time",
            "because": "without source vector, official readout still cannot produce a finite WEP product",
            "next_action": "1083 should stage DD Earth-source vector extraction from composition references",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_id": "NEXT1082_0_1083",
            "next_target": "1083-Y5-R10-DD-Earth-source-vector-extraction-plan-and-nonclaim-first-row.md",
            "objective": "construct the DD-basis Earth/source vector extraction plan and first nonclaim source-row contract from Earth composition references; keep MICROSCOPE readout and MTS coefficient map blocked until sourced.",
            "include": "Earth composition table targets; DD alpha/surface charge formulas; shell/profile caveats; common-mode theorem alternative; source vector schema; strict nonclaim gates",
            "exclude": "unit source proxy as physical source; measured-G absorption; DD smoke as MTS claim; public claim; GitHub; formalization edits",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def csv_rows_parse(path: Path) -> bool:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            list(csv.DictReader(handle))
    except csv.Error:
        return False
    return True


def validate_outputs(
    outputs: dict[str, Path],
    source_rows: list[dict[str, str]],
    map_rows: list[dict[str, str]],
    units_rows: list[dict[str, str]],
    earth_rows: list[dict[str, str]],
    readout_rows: list[dict[str, str]],
    reuse_rows: list[dict[str, str]],
    prediction_rows: list[dict[str, str]],
    bound_rows_: list[dict[str, str]],
    product_status: dict[str, Any],
    claim_rows: list[dict[str, str]],
    next_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    checks: list[tuple[str, bool, str]] = []
    checks.append(("V1082_0_sources_exist", all(row["exists"] == "true" and row["needle_found"] == "true" for row in source_rows), "all cited local source paths and needles are present"))
    checks.append(("V1082_1_parent_to_DD_not_derived", any(row["map_id"] == "PTD1082_4_verdict" and row["result"] == "PARENT_TO_DD_MAP_NOT_DERIVED" for row in map_rows), "parent-to-DD coefficient map remains unsigned"))
    checks.append(("V1082_2_coefficient_units_contract", len(units_rows) == 4 and any(row["coefficient_id"] == "CUC1082_3_C_parent" and row["status"] == "MISSING_FOR_CLAIM" for row in units_rows), "coefficient units contract records missing C_parent"))
    checks.append(("V1082_3_earth_fill_nonclaim", len(earth_rows) == 4 and all(row["valid_for_claim"] == "false" for row in earth_rows) and any(row["fill_id"] == "ESF1082_1_vectorization" and row["current_status"] == "NOT_VECTORIZED" for row in earth_rows), "Earth/source fill rows remain nonclaim and not vectorized"))
    checks.append(("V1082_4_readout_fill_nonclaim", len(readout_rows) == 3 and all(row["valid_for_claim"] == "false" for row in readout_rows) and any(row["fill_id"] == "ROF1082_0_official_arrays" and row["current_status"] == "OFFICIAL_ARRAYS_NOT_IMPORTED" for row in readout_rows), "readout fill rows remain nonclaim and official arrays are missing"))
    checks.append(("V1082_5_DD_smoke_reuse", len(reuse_rows) == 3 and all(row["valid_for_claim"] == "false" for row in reuse_rows), "DD smoke rows are reused only as nonclaim algebra checks"))
    checks.append(("V1082_6_prediction_nonclaim_missing", any("MISSING_PARENT_TO_DD_MAP" in row["product_value"] and row["valid_for_claim"] == "false" for row in prediction_rows), "prediction row remains missing parent-to-DD/source/readout"))
    checks.append(("V1082_7_bound_numeric", bool(bound_rows_) and float(bound_rows_[0]["bound_value"]) > 0 and bound_rows_[0]["valid_for_claim"] == "true", "bound import is positive numeric"))
    checks.append(("V1082_8_product_runner_refuses", product_status.get("valid_prediction_rows") == 0 and product_status.get("claim_allowed") is False, "generic product runner reports no valid prediction rows and claim false"))
    checks.append(("V1082_9_claim_gates_safe", all(row["claim_allowed"] == "false" for row in claim_rows), "all claim gates deny WEP/local-GR claim"))
    checks.append(("V1082_10_next_target", any(row["next_target"].startswith("1083-Y5-R10-DD-Earth-source") for row in next_rows), "1083 handoff written"))
    generated_paths = list(outputs.values()) + [DOC]
    checks.append(("V1082_11_generated_under_post_checkpoint", all(str(path.resolve()).startswith(str(ROOT.resolve())) for path in generated_paths), "all generated outputs are under post-checkpoint-work"))
    checks.append(("V1082_12_csv_parse", all(path.exists() and csv_rows_parse(path) for path in outputs.values() if path.suffix == ".csv" and path.name != "P8_Y5_BRR545_1082_VALIDATION.csv"), "all 1082 CSV outputs parse cleanly"))
    checks.append(("V1082_13_formalization_untouched", count_formalization_modified_since_start() == 0, "formalization-workbench modified-file count remains zero"))
    checks.append(("V1082_SUMMARY", True, "parent-to-DD coefficient map not derived; physical Earth-source/readout fill rows staged; DD smoke remains nonclaim"))
    return [
        {
            "check_id": check_id,
            "result": "pass" if passed else "fail",
            "detail": detail,
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for check_id, passed, detail in checks
    ]


def write_doc(
    source_rows: list[dict[str, str]],
    map_rows: list[dict[str, str]],
    units_rows: list[dict[str, str]],
    earth_rows: list[dict[str, str]],
    readout_rows: list[dict[str, str]],
    reuse_rows: list[dict[str, str]],
    prediction_rows: list[dict[str, str]],
    bound_rows_: list[dict[str, str]],
    product_status_rows_: list[dict[str, str]],
    product_comparison_rows: list[dict[str, Any]],
    claim_rows: list[dict[str, str]],
    decisions: list[dict[str, str]],
    validation_rows: list[dict[str, str]],
    next_rows: list[dict[str, str]],
) -> None:
    text = "\n".join(
        [
            "# 1082 - Parent-to-DD coefficient map or physical source/readout fill",
            "",
            "## Current verdict",
            "1082 does not derive the parent-to-DD coefficient map. The alpha/Coulomb and surface/binding DD smoke rows remain useful external algebra checks, but MTS still lacks the signed operator pullback and coefficient-unit map C_parent -> (c_alpha,c_surface). The checkpoint therefore stages physical Earth-source and MICROSCOPE readout fill contracts as the next empirical scaffold, with all claim gates closed.",
            "",
            "## Local source register",
            md_table(source_rows, ["source_id", "relative_path", "exists", "needle_found", "note"]),
            "## Parent-to-DD coefficient map attempt",
            md_table(map_rows, ["map_id", "claim", "result", "gap"]),
            "## Coefficient units contract",
            md_table(units_rows, ["coefficient_id", "coefficient_symbol", "basis", "bound_or_value", "status", "missing_for_claim"]),
            "## Physical Earth-source fill rows",
            md_table(earth_rows, ["fill_id", "object", "current_status", "claim_blocker"]),
            "## Physical MICROSCOPE readout fill rows",
            md_table(readout_rows, ["fill_id", "object", "current_status", "claim_blocker"]),
            "## DD smoke reuse rows",
            md_table(reuse_rows, ["reuse_id", "component", "required_abs_coefficient_max", "reuse_policy", "promotion_blocker"]),
            "## Nonclaim product candidate",
            md_table(prediction_rows, ["prediction_id", "product_symbol", "product_value", "derivation_status", "valid_for_claim"]),
            "## Bound import",
            md_table(bound_rows_, ["bound_id", "product_symbol", "bound_value", "bound_units", "valid_for_claim"]),
            "## Product runner status",
            md_table(product_status_rows_, ["runner_id", "valid_prediction_rows", "valid_bound_rows", "claim_allowed", "expected_result"]),
            "## Product comparison rows",
            md_table(product_comparison_rows, ["comparison_id", "comparison_status", "pass_for_claim", "issues"]),
            "## Claim gates",
            md_table(claim_rows, ["gate_id", "claim_component", "gate_pass", "claim_allowed", "reason"]),
            "## Decision ledger",
            md_table(decisions, ["decision_id", "decision", "because", "next_action"]),
            "## Validation",
            md_table(validation_rows, ["check_id", "result", "detail"]),
            "## Next target",
            md_table(next_rows, ["next_id", "next_target", "objective", "include", "exclude"]),
            "",
        ]
    )
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    source_rows = source_register_rows()
    map_rows = parent_to_dd_map_attempt_rows()
    units_rows = coefficient_units_contract_rows()
    earth_rows = physical_earth_source_fill_rows()
    readout_rows = physical_readout_fill_rows()
    reuse_rows = dd_smoke_reuse_rows()
    prediction_rows = product_prediction_rows()
    bound_rows_ = bound_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    outputs = {
        "source_register": OUT / "P8_Y5_R10_1082_SOURCE_REGISTER.csv",
        "map_attempt": OUT / "P8_Y5_R10_1082_PARENT_TO_DD_COEFFICIENT_MAP_ATTEMPT.csv",
        "units_contract": OUT / "P8_Y5_R10_1082_COEFFICIENT_UNITS_CONTRACT.csv",
        "earth_fill": OUT / "P8_Y5_R10_1082_PHYSICAL_EARTH_SOURCE_FILL_ROWS.csv",
        "readout_fill": OUT / "P8_Y5_R10_1082_PHYSICAL_MICROSCOPE_READOUT_FILL_ROWS.csv",
        "DD_reuse": OUT / "P8_Y5_R10_1082_DD_SMOKE_REUSE_ROWS.csv",
        "prediction": PREDICTION_TEMPLATE,
        "bound": BOUND_IMPORT,
        "product_status": OUT / "P8_Y5_R10_1082_PRODUCT_RUNNER_STATUS.csv",
        "product_comparison": OUT / "P8_Y5_R10_1082_PRODUCT_COMPARISON_ROWS.csv",
        "claim_gates": OUT / "P8_Y5_R10_1082_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_R10_1082_DECISION_LEDGER.csv",
        "next_target": OUT / "P8_Y5_R10_1082_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_1082_VALIDATION.csv",
    }

    write_csv(outputs["source_register"], source_rows)
    write_csv(outputs["map_attempt"], map_rows)
    write_csv(outputs["units_contract"], units_rows)
    write_csv(outputs["earth_fill"], earth_rows)
    write_csv(outputs["readout_fill"], readout_rows)
    write_csv(outputs["DD_reuse"], reuse_rows)
    write_csv(outputs["prediction"], prediction_rows, PRODUCT_REQUIRED_COLUMNS)
    write_csv(outputs["bound"], bound_rows_, BOUND_REQUIRED_COLUMNS)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["next_target"], next_rows)

    product_result = run_product_runner(PREDICTION_TEMPLATE, BOUND_IMPORT, PRODUCT_RUN_DIR)
    product_status = product_result["status"]
    product_status_rows_ = product_status_rows(product_status)
    claim_rows = claim_gate_rows(product_status)

    write_csv(outputs["product_status"], product_status_rows_)
    write_csv(outputs["product_comparison"], product_result["comparisons"])
    write_csv(outputs["claim_gates"], claim_rows)

    remove_pycache()
    validation_rows = validate_outputs(
        outputs,
        source_rows,
        map_rows,
        units_rows,
        earth_rows,
        readout_rows,
        reuse_rows,
        prediction_rows,
        bound_rows_,
        product_status,
        claim_rows,
        next_rows,
    )
    write_csv(outputs["validation"], validation_rows)
    write_doc(
        source_rows,
        map_rows,
        units_rows,
        earth_rows,
        readout_rows,
        reuse_rows,
        prediction_rows,
        bound_rows_,
        product_status_rows_,
        product_result["comparisons"],
        claim_rows,
        decisions,
        validation_rows,
        next_rows,
    )
    remove_pycache()

    failed = [row for row in validation_rows if row["result"] != "pass"]
    print(f"wrote {DOC}")
    print(f"validation: {'PASS' if not failed else 'FAIL'}")
    for row in failed:
        print(f"{row['check_id']}: {row['detail']}")


if __name__ == "__main__":
    main()
