from __future__ import annotations

import csv
import math
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
DOC = ROOT / "1081-Y5-R10-DD-basis-finite-WEP-smoke-runner-or-parent-basis-derivation.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_DIR = ROOT / "runs" / "1081-DD-basis-finite-WEP-smoke-runner-or-parent-basis-derivation" / "results"
PRODUCT_RUN_DIR = RUN_DIR / "product_runner"
PREDICTION_TEMPLATE = OUT / "P8_Y5_R10_1081_WEP_PRODUCT_CANDIDATE_NONCLAIM.csv"
BOUND_IMPORT = OUT / "P8_Y5_R10_1081_WEP_BOUND_IMPORT.csv"
CHARGE_MATRIX = OUT / "P8_Y5_R10_1053_WEP_COMPOSITION_CHARGE_MATRIX.csv"


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


def parse_float(value: object) -> float:
    parsed = float(str(value).strip())
    if not math.isfinite(parsed):
        raise ValueError(f"non-finite float {value}")
    return parsed


def local_bound_row(row_id: str) -> dict[str, str]:
    for row in read_csv(LOCAL_BOUNDS):
        if row.get("row_id") == row_id:
            return row
    raise ValueError(f"missing local bound row {row_id}")


def charge_row(matrix_id: str) -> dict[str, str]:
    for row in read_csv(CHARGE_MATRIX):
        if row.get("matrix_id") == matrix_id:
            return row
    raise ValueError(f"missing charge matrix row {matrix_id}")


def split_reference(reference: str) -> tuple[str, str]:
    parts = [part.strip() for part in reference.split(";")]
    url = next((part for part in parts if part.startswith("http")), "")
    doi = next((part.replace("doi:", "").strip() for part in parts if part.lower().startswith("doi:")), "")
    return url, doi


def source_register_rows() -> list[dict[str, str]]:
    specs = [
        ("SRC1081_0_1080_next", "source-intake/mts_residuals/P8_Y5_R10_1080_NEXT_TARGET.csv", "1081-Y5-R10-DD-basis-finite-WEP-smoke-runner-or-parent-basis-derivation.md", "1080 handoff."),
        ("SRC1081_1_1080_validation", "source-intake/mts_residuals/P8_Y5_BRR545_1080_VALIDATION.csv", "V1080_SUMMARY", "1080 validation summary."),
        ("SRC1081_2_1080_web", "source-intake/mts_residuals/P8_Y5_R10_1080_WEB_SOURCE_CANDIDATE_REGISTER.csv", "WEB1080_1_DAMOUR_DONOGHUE_2010", "DD source register."),
        ("SRC1081_3_1080_material", "source-intake/mts_residuals/P8_Y5_R10_1080_MATERIAL_COMPOSITION_AND_TENSOR_CANDIDATES.csv", "MAT1080_2_delta_alpha_smoke", "material candidate rows."),
        ("SRC1081_4_1080_input", "source-intake/mts_residuals/P8_Y5_R10_1080_FINITE_WEP_INPUT_PACK_NONCLAIM.csv", "FIP1080_3_R_material", "finite WEP input pack."),
        ("SRC1081_5_1080_readout", "source-intake/mts_residuals/P8_Y5_R10_1080_MICROSCOPE_READOUT_GATE.csv", "READ1080_1_CMSM_portal", "readout gate."),
        ("SRC1081_6_1080_Cparent", "source-intake/mts_residuals/P8_Y5_R10_1080_C_PARENT_COEFFICIENT_CONTRACT.csv", "CP1080_0_definition", "C_parent contract."),
        ("SRC1081_7_1053_matrix", "source-intake/mts_residuals/P8_Y5_R10_1053_WEP_COMPOSITION_CHARGE_MATRIX.csv", "WCM1053_4", "DD smoke material deltas."),
        ("SRC1081_8_1052_projection", "source-intake/mts_residuals/P8_Y5_R10_1052_ALPHA_WEP_PROJECTION_LEDGER.csv", "AWP1052_0_alpha_Coulomb", "older WEP projection thresholds."),
        ("SRC1081_9_local_bounds", "source-intake/local_bounds/local_bound_claims.csv", "R1_WEP_source_charge", "MICROSCOPE WEP bound row."),
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


def parent_basis_attempt_rows() -> list[dict[str, str]]:
    return [
        {
            "basis_attempt_id": "PB1081_0_target",
            "claim": "derive the finite WEP parent basis from MTS action slots",
            "required_map": "parent vertical/coupling generators e_I -> local matter response components R_A^I and source components R_source^I",
            "proof_move": "look for a parent-owned basis that simultaneously defines C_parent, R_source^Earth, R_TA6V-PtRh10, and K_MICROSCOPE",
            "result": "TARGET_SHARPENED",
            "gap": "basis must be derived before any external DD components can become MTS components",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "basis_attempt_id": "PB1081_1_parent_slots",
            "claim": "MTS already supplies a typed local WEP component basis",
            "required_map": "basis labels, units, source/test response maps, and coefficient dimensions",
            "proof_move": "reuse current-owner/Hilbert source subtheorem as basis owner",
            "result": "NOT_DERIVED",
            "gap": "current-owner subtheorem owns post-variation source definition only; it does not supply material-response basis or coefficient units",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "basis_attempt_id": "PB1081_2_DD_embedding",
            "claim": "Damour-Donoghue alpha/surface basis is the MTS parent basis",
            "required_map": "MTS parent slots -> DD alpha/Coulomb and surface/binding charge components",
            "proof_move": "identify DD basis as an external phenomenological comparator and ask whether MTS has a functor into it",
            "result": "EXTERNAL_BASIS_ONLY",
            "gap": "no MTS-to-DD map or parent coefficient vector is signed",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "basis_attempt_id": "PB1081_3_source_readout",
            "claim": "source/readout normalization is already fixed",
            "required_map": "Earth source vector and MICROSCOPE readout kernel in the same DD/MTS basis",
            "proof_move": "use unit-normalized smoke convention to test algebra while keeping physical source/readout missing",
            "result": "SMOKE_ONLY_NOT_PHYSICAL",
            "gap": "unit convention is not tau_WEP, not measured-G absorption, and not a physical source vector",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "basis_attempt_id": "PB1081_4_verdict",
            "claim": "MTS parent WEP basis is derived",
            "required_map": "same-basis C_parent, R_source, R_material, K_readout",
            "proof_move": "assemble parent slots, DD embedding, and source/readout normalization checks",
            "result": "PARENT_WEP_BASIS_NOT_DERIVED",
            "gap": "DD smoke runner may be built only as an external nonclaim comparator",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def dd_basis_schema_rows() -> list[dict[str, str]]:
    return [
        {
            "basis_id": "DDB1081_0_alpha_Coulomb",
            "component": "Q_alpha_Coulomb",
            "basis_source": "WEB1080_1_DAMOUR_DONOGHUE_2010; WCM1053_4",
            "material_delta_source": "WCM1053_4",
            "coefficient_symbol": "c_alpha_proxy",
            "status": "EXTERNAL_PHENOMENOLOGICAL_SMOKE_BASIS",
            "claim_policy": "not MTS-derived; comparator/smoke only",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "basis_id": "DDB1081_1_surface_binding",
            "component": "Q_surface_binding",
            "basis_source": "WEB1080_1_DAMOUR_DONOGHUE_2010; WCM1053_5",
            "material_delta_source": "WCM1053_5",
            "coefficient_symbol": "c_surface_proxy",
            "status": "EXTERNAL_PHENOMENOLOGICAL_SMOKE_BASIS",
            "claim_policy": "not MTS-derived; comparator/smoke only",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "basis_id": "DDB1081_2_two_component_proxy",
            "component": "Q_alpha_Coulomb + Q_surface_binding",
            "basis_source": "WCM1053_4; WCM1053_5",
            "material_delta_source": "sum of absolute smoke deltas",
            "coefficient_symbol": "c_equal_proxy",
            "status": "PIPELINE_STRESS_TEST_BASIS",
            "claim_policy": "tests algebra and signs only; no physical coefficient vector",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def source_proxy_policy_rows() -> list[dict[str, str]]:
    return [
        {
            "policy_id": "SPP1081_0_unit_source_proxy",
            "object": "DD source proxy",
            "policy": "set source_proxy_norm=1 only to compute coefficient-normalized sensitivity rows",
            "allowed_use": "pipeline algebra smoke; required coefficient bound per unit source/readout convention",
            "forbidden_use": "physical tau_WEP, Earth source vector, measured-G absorption, or MTS claim",
            "claim_gate": "BLOCK_CLAIM",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "policy_id": "SPP1081_1_readout_proxy",
            "object": "K_MICROSCOPE proxy",
            "policy": "set readout_proxy_norm=1 only in the same coefficient-normalized smoke convention",
            "allowed_use": "unit-response and coefficient-bound sanity checks",
            "forbidden_use": "replacement for official gx,gz,Sxx,Sxz arrays or physical tau_WEP",
            "claim_gate": "BLOCK_CLAIM",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "policy_id": "SPP1081_2_parent_map",
            "object": "MTS-to-DD map",
            "policy": "no MTS-to-DD map exists in this checkpoint",
            "allowed_use": "external comparator branch only",
            "forbidden_use": "call DD smoke coefficients MTS-derived",
            "claim_gate": "BLOCK_CLAIM",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def dd_material_delta_rows() -> list[dict[str, str]]:
    alpha = charge_row("WCM1053_4")
    surface = charge_row("WCM1053_5")
    return [
        {
            "delta_id": "DDM1081_0_delta_alpha",
            "component": "Q_alpha_Coulomb",
            "test_pair": alpha["test_pair"],
            "delta_value": alpha["charge_value"],
            "delta_abs": alpha["delta_Q_abs_for_pair"],
            "source_row": "WCM1053_4",
            "status": "NUMERIC_SMOKE_DELTA_NONCLAIM",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "delta_id": "DDM1081_1_delta_surface",
            "component": "Q_surface_binding",
            "test_pair": surface["test_pair"],
            "delta_value": surface["charge_value"],
            "delta_abs": surface["delta_Q_abs_for_pair"],
            "source_row": "WCM1053_5",
            "status": "NUMERIC_SMOKE_DELTA_NONCLAIM",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def dd_unit_response_smoke_rows() -> list[dict[str, str]]:
    eta_bound = parse_float(local_bound_row("R1_WEP_source_charge")["upper_bound"])
    alpha_abs = parse_float(charge_row("WCM1053_4")["delta_Q_abs_for_pair"])
    surface_abs = parse_float(charge_row("WCM1053_5")["delta_Q_abs_for_pair"])
    combined_abs = alpha_abs + surface_abs
    rows = [
        ("DDS1081_0_alpha_unit", "Q_alpha_Coulomb", alpha_abs, "c_alpha_proxy", "WCM1053_4"),
        ("DDS1081_1_surface_unit", "Q_surface_binding", surface_abs, "c_surface_proxy", "WCM1053_5"),
        ("DDS1081_2_equal_two_component_unit", "Q_alpha_Coulomb + Q_surface_binding", combined_abs, "c_equal_proxy", "WCM1053_4;WCM1053_5"),
    ]
    return [
        {
            "smoke_id": smoke_id,
            "component": component,
            "unit_source_proxy": "1_nonphysical_coefficient_normalization",
            "unit_readout_proxy": "1_nonphysical_coefficient_normalization",
            "unit_response_abs": f"{unit_response:.12e}",
            "eta_bound": f"{eta_bound:.12e}",
            "required_abs_coefficient_max": f"{eta_bound / unit_response:.12e}",
            "coefficient_symbol": coefficient_symbol,
            "source_rows": source_rows,
            "status": "NUMERIC_UNIT_RESPONSE_SMOKE_NONCLAIM",
            "claim_blocker": "source/readout proxy is nonphysical and MTS-to-DD map is unsigned",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for smoke_id, component, unit_response, coefficient_symbol, source_rows in rows
    ]


def smoke_runner_status_rows(smoke_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    numeric_rows = 0
    positive_bounds = 0
    for row in smoke_rows:
        unit_response = parse_float(row["unit_response_abs"])
        required_bound = parse_float(row["required_abs_coefficient_max"])
        numeric_rows += int(unit_response > 0)
        positive_bounds += int(required_bound > 0)
    return [
        {
            "runner_id": "DDS1081_RUNNER_0_unit_response",
            "smoke_rows": str(len(smoke_rows)),
            "numeric_unit_response_rows": str(numeric_rows),
            "positive_coefficient_bound_rows": str(positive_bounds),
            "physical_source_vector_present": "false",
            "physical_readout_kernel_present": "false",
            "MTS_to_DD_map_present": "false",
            "claim_allowed": "false",
            "expected_result": "numeric smoke rows exist but cannot be promoted to MTS prediction",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def parent_to_dd_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "PDD1081_0_parent_basis",
            "needed_object": "MTS parent WEP basis",
            "current_status": "NOT_DERIVED",
            "blocks": "DD smoke basis cannot be called MTS basis",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "PDD1081_1_coefficient_map",
            "needed_object": "C_parent -> (c_alpha_proxy,c_surface_proxy)",
            "current_status": "MISSING",
            "blocks": "no MTS coefficient vector in DD basis",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "PDD1081_2_source_vector",
            "needed_object": "R_source^Earth in DD/MTS basis",
            "current_status": "MISSING",
            "blocks": "unit source proxy is nonphysical",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "PDD1081_3_readout_kernel",
            "needed_object": "K_MICROSCOPE official/validated readout",
            "current_status": "SURROGATE_ONLY",
            "blocks": "unit readout proxy is nonphysical",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def product_prediction_rows() -> list[dict[str, str]]:
    return [
        {
            "prediction_id": "PRED1081_0_DD_smoke_not_MTS_product",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "P_WEP_relative_source_weight",
            "product_value": "MISSING_PARENT_TO_DD_MAP_OR_PHYSICAL_SOURCE_READOUT_NORMALIZATION",
            "product_units": "dimensionless",
            "product_source": "source-intake/mts_residuals/P8_Y5_R10_1081_DD_UNIT_RESPONSE_SMOKE_RUNNER.csv",
            "inputs_present": "DD smoke material deltas; unit source/readout proxy; MICROSCOPE bound",
            "required_inputs": "MTS-to-DD coefficient map; physical R_source^Earth; official/validated K_MICROSCOPE; parent claim policy",
            "derivation_status": "DD_SMOKE_NUMERIC_BUT_MTS_PRODUCT_MISSING",
            "valid_for_claim": "false",
            "notes": "generic product runner must refuse because this is an external smoke comparator",
        }
    ]


def bound_rows() -> list[dict[str, str]]:
    row = local_bound_row("R1_WEP_source_charge")
    url, doi = split_reference(row.get("reference_path_or_url", ""))
    return [
        {
            "bound_id": "BOUND1081_0_MICROSCOPE_WEP_source_charge",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "P_WEP_relative_source_weight",
            "bound_value": row["upper_bound"],
            "bound_units": row["units"],
            "bound_source": url,
            "source_row": f"{row['dataset_id']}:{row['row_id']};doi:{doi}",
            "bound_type": "upper_abs_WEP_proxy_bound",
            "valid_for_claim": "true",
            "notes": "source-backed numeric bound only; DD smoke product remains invalid",
        }
    ]


def product_status_rows(status: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "runner_id": "APR1081_0_DD_smoke_product_stub",
            "prediction_rows": str(status.get("prediction_rows", "")),
            "bound_rows": str(status.get("bound_rows", "")),
            "valid_prediction_rows": str(status.get("valid_prediction_rows", "")),
            "valid_bound_rows": str(status.get("valid_bound_rows", "")),
            "comparison_rows": str(status.get("comparison_rows", "")),
            "passed_rows": str(status.get("passed_rows", "")),
            "claim_allowed": str(status.get("claim_allowed", "")).lower(),
            "expected_result": "reject DD smoke rows as MTS product",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def claim_gate_rows(product_status: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "gate_id": "CG1081_0_parent_basis",
            "claim_component": "MTS parent WEP basis",
            "gate_pass": "false",
            "claim_allowed": "false",
            "reason": "PB1081_4_verdict=PARENT_WEP_BASIS_NOT_DERIVED",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1081_1_DD_smoke_numeric",
            "claim_component": "DD unit-response smoke rows",
            "gate_pass": "true",
            "claim_allowed": "false",
            "reason": "numeric unit-response rows exist but are external nonphysical proxy rows",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1081_2_source_proxy",
            "claim_component": "source/readout proxy",
            "gate_pass": "false",
            "claim_allowed": "false",
            "reason": "unit proxy is not physical tau_WEP, not Earth source vector, and not official readout",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1081_3_parent_to_DD_map",
            "claim_component": "MTS-to-DD coefficient map",
            "gate_pass": "false",
            "claim_allowed": "false",
            "reason": "C_parent -> DD coefficient vector is missing",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1081_4_product_runner",
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
            "decision_id": "DEC1081_0_parent_basis",
            "decision": "MTS parent WEP basis remains unsigned",
            "because": "current corpus does not derive component basis, coefficient vector, Earth source vector, and readout kernel in one convention",
            "next_action": "do not promote DD smoke rows to MTS",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1081_1_smoke_runner",
            "decision": "DD alpha/surface unit-response smoke runner is useful and numeric",
            "because": "it gives coefficient-normalized WEP sensitivity rows for algebra/pipeline checks",
            "next_action": "use as nonclaim scaffold to test sign, units, and coefficient-bound plumbing",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1081_2_next_route",
            "decision": "next target should attack parent-to-DD coefficient map or physical source/readout fill",
            "because": "these are the exact locks that turn the smoke runner into a possible finite WEP prediction",
            "next_action": "try parent-to-DD map first, then Earth-source/readout acquisition if unsigned",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_id": "NEXT1081_0_1082",
            "next_target": "1082-Y5-R10-parent-to-DD-coefficient-map-or-physical-source-readout-fill.md",
            "objective": "try to derive the MTS-to-DD alpha/surface coefficient map C_parent -> (c_alpha,c_surface); if it remains unsigned, acquire physical Earth-source and MICROSCOPE readout normalization rows for the DD smoke branch without claiming an MTS pass.",
            "include": "parent-to-DD map; coefficient units; Earth source vector policy; official readout normalization; DD smoke runner reuse; strict claim gates",
            "exclude": "DD smoke as MTS claim; unit source/readout as tau_WEP; measured-G absorption; public claim; GitHub; formalization edits",
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
    parent_rows: list[dict[str, str]],
    dd_basis_rows: list[dict[str, str]],
    proxy_rows: list[dict[str, str]],
    material_rows: list[dict[str, str]],
    smoke_rows: list[dict[str, str]],
    smoke_status: list[dict[str, str]],
    pdd_rows: list[dict[str, str]],
    prediction_rows: list[dict[str, str]],
    bound_rows_: list[dict[str, str]],
    product_status: dict[str, Any],
    claim_rows: list[dict[str, str]],
    next_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    checks: list[tuple[str, bool, str]] = []
    checks.append(("V1081_0_sources_exist", all(row["exists"] == "true" and row["needle_found"] == "true" for row in source_rows), "all cited local source paths and needles are present"))
    checks.append(("V1081_1_parent_basis_not_derived", any(row["basis_attempt_id"] == "PB1081_4_verdict" and row["result"] == "PARENT_WEP_BASIS_NOT_DERIVED" for row in parent_rows), "MTS parent WEP basis remains unsigned"))
    checks.append(("V1081_2_DD_basis_schema", {row["component"] for row in dd_basis_rows} == {"Q_alpha_Coulomb", "Q_surface_binding", "Q_alpha_Coulomb + Q_surface_binding"}, "DD alpha/surface schema is present"))
    checks.append(("V1081_3_source_proxy_blocks_claim", len(proxy_rows) == 3 and all(row["claim_gate"] == "BLOCK_CLAIM" and row["valid_for_claim"] == "false" for row in proxy_rows), "source/readout proxy policy blocks claims"))
    checks.append(("V1081_4_material_deltas_numeric", len(material_rows) == 2 and all(parse_float(row["delta_abs"]) > 0 and row["valid_for_claim"] == "false" for row in material_rows), "DD material delta rows are numeric nonclaim"))
    checks.append(("V1081_5_smoke_rows_numeric", len(smoke_rows) == 3 and all(parse_float(row["unit_response_abs"]) > 0 and parse_float(row["required_abs_coefficient_max"]) > 0 and row["valid_for_claim"] == "false" for row in smoke_rows), "DD unit-response smoke rows are numeric nonclaim"))
    checks.append(("V1081_6_smoke_status_nonclaim", bool(smoke_status) and smoke_status[0]["claim_allowed"] == "false" and smoke_status[0]["MTS_to_DD_map_present"] == "false", "DD smoke runner status blocks claims"))
    checks.append(("V1081_7_parent_to_DD_gates", len(pdd_rows) == 4 and all(row["valid_for_claim"] == "false" for row in pdd_rows), "parent-to-DD gates are explicit"))
    checks.append(("V1081_8_prediction_nonclaim_missing", any("MISSING_PARENT_TO_DD_MAP" in row["product_value"] and row["valid_for_claim"] == "false" for row in prediction_rows), "generic prediction row remains missing parent-to-DD/source/readout inputs"))
    checks.append(("V1081_9_bound_numeric", bool(bound_rows_) and float(bound_rows_[0]["bound_value"]) > 0 and bound_rows_[0]["valid_for_claim"] == "true", "bound import is positive numeric"))
    checks.append(("V1081_10_product_runner_refuses", product_status.get("valid_prediction_rows") == 0 and product_status.get("claim_allowed") is False, "generic product runner reports no valid prediction rows and claim false"))
    checks.append(("V1081_11_claim_gates_safe", all(row["claim_allowed"] == "false" for row in claim_rows), "all claim gates deny WEP/local-GR claim"))
    checks.append(("V1081_12_next_target", any(row["next_target"].startswith("1082-Y5-R10-parent-to-DD") for row in next_rows), "1082 handoff written"))
    generated_paths = list(outputs.values()) + [DOC]
    checks.append(("V1081_13_generated_under_post_checkpoint", all(str(path.resolve()).startswith(str(ROOT.resolve())) for path in generated_paths), "all generated outputs are under post-checkpoint-work"))
    checks.append(("V1081_14_csv_parse", all(path.exists() and csv_rows_parse(path) for path in outputs.values() if path.suffix == ".csv" and path.name != "P8_Y5_BRR545_1081_VALIDATION.csv"), "all 1081 CSV outputs parse cleanly"))
    checks.append(("V1081_15_formalization_untouched", count_formalization_modified_since_start() == 0, "formalization-workbench modified-file count remains zero"))
    checks.append(("V1081_SUMMARY", True, "MTS parent WEP basis not derived; DD unit-response smoke runner numeric but nonclaim; parent-to-DD/source/readout locks remain"))
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
    parent_rows: list[dict[str, str]],
    dd_basis_rows: list[dict[str, str]],
    proxy_rows: list[dict[str, str]],
    material_rows: list[dict[str, str]],
    smoke_rows: list[dict[str, str]],
    smoke_status: list[dict[str, str]],
    pdd_rows: list[dict[str, str]],
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
            "# 1081 - DD-basis finite WEP smoke runner or parent-basis derivation",
            "",
            "## Current verdict",
            "1081 does not derive the MTS parent WEP basis. It does build a useful Damour-Donoghue alpha/surface unit-response smoke runner: the material deltas are numeric and the coefficient-normalized sensitivity rows are numeric. But the branch is explicitly nonclaim because the MTS-to-DD coefficient map, physical Earth source vector, and official/validated MICROSCOPE readout normalization remain missing.",
            "",
            "## Local source register",
            md_table(source_rows, ["source_id", "relative_path", "exists", "needle_found", "note"]),
            "## Parent WEP basis derivation attempt",
            md_table(parent_rows, ["basis_attempt_id", "claim", "result", "gap"]),
            "## DD basis schema",
            md_table(dd_basis_rows, ["basis_id", "component", "coefficient_symbol", "status", "claim_policy"]),
            "## Source/readout proxy policy",
            md_table(proxy_rows, ["policy_id", "object", "policy", "forbidden_use", "claim_gate"]),
            "## DD material delta import",
            md_table(material_rows, ["delta_id", "component", "delta_value", "delta_abs", "source_row", "status"]),
            "## DD unit-response smoke runner",
            md_table(smoke_rows, ["smoke_id", "component", "unit_response_abs", "eta_bound", "required_abs_coefficient_max", "status"]),
            "## DD smoke runner status",
            md_table(smoke_status, ["runner_id", "numeric_unit_response_rows", "positive_coefficient_bound_rows", "MTS_to_DD_map_present", "claim_allowed"]),
            "## Parent-to-DD claim gates",
            md_table(pdd_rows, ["gate_id", "needed_object", "current_status", "blocks"]),
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
    parent_rows = parent_basis_attempt_rows()
    dd_basis_rows = dd_basis_schema_rows()
    proxy_rows = source_proxy_policy_rows()
    material_rows = dd_material_delta_rows()
    smoke_rows = dd_unit_response_smoke_rows()
    smoke_status = smoke_runner_status_rows(smoke_rows)
    pdd_rows = parent_to_dd_gate_rows()
    prediction_rows = product_prediction_rows()
    bound_rows_ = bound_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    outputs = {
        "source_register": OUT / "P8_Y5_R10_1081_SOURCE_REGISTER.csv",
        "parent_basis": OUT / "P8_Y5_R10_1081_PARENT_WEP_BASIS_DERIVATION_ATTEMPT.csv",
        "DD_basis": OUT / "P8_Y5_R10_1081_DD_BASIS_SCHEMA.csv",
        "source_proxy": OUT / "P8_Y5_R10_1081_DD_SOURCE_PROXY_POLICY.csv",
        "material_delta": OUT / "P8_Y5_R10_1081_DD_MATERIAL_DELTA_IMPORT.csv",
        "DD_smoke": OUT / "P8_Y5_R10_1081_DD_UNIT_RESPONSE_SMOKE_RUNNER.csv",
        "DD_smoke_status": OUT / "P8_Y5_R10_1081_DD_SMOKE_RUNNER_STATUS.csv",
        "parent_to_DD": OUT / "P8_Y5_R10_1081_PARENT_TO_DD_GATE.csv",
        "prediction": PREDICTION_TEMPLATE,
        "bound": BOUND_IMPORT,
        "product_status": OUT / "P8_Y5_R10_1081_PRODUCT_RUNNER_STATUS.csv",
        "product_comparison": OUT / "P8_Y5_R10_1081_PRODUCT_COMPARISON_ROWS.csv",
        "claim_gates": OUT / "P8_Y5_R10_1081_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_R10_1081_DECISION_LEDGER.csv",
        "next_target": OUT / "P8_Y5_R10_1081_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_1081_VALIDATION.csv",
    }

    write_csv(outputs["source_register"], source_rows)
    write_csv(outputs["parent_basis"], parent_rows)
    write_csv(outputs["DD_basis"], dd_basis_rows)
    write_csv(outputs["source_proxy"], proxy_rows)
    write_csv(outputs["material_delta"], material_rows)
    write_csv(outputs["DD_smoke"], smoke_rows)
    write_csv(outputs["DD_smoke_status"], smoke_status)
    write_csv(outputs["parent_to_DD"], pdd_rows)
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
        parent_rows,
        dd_basis_rows,
        proxy_rows,
        material_rows,
        smoke_rows,
        smoke_status,
        pdd_rows,
        prediction_rows,
        bound_rows_,
        product_status,
        claim_rows,
        next_rows,
    )
    write_csv(outputs["validation"], validation_rows)
    write_doc(
        source_rows,
        parent_rows,
        dd_basis_rows,
        proxy_rows,
        material_rows,
        smoke_rows,
        smoke_status,
        pdd_rows,
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
