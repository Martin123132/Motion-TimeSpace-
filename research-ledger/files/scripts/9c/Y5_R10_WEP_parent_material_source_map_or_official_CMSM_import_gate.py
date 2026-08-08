from __future__ import annotations

import csv
import math
import shutil
from collections import defaultdict
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
MATERIAL_MODEL = OUT / "P8_Y5_R10_651_MICROSCOPE_MATERIAL_MODEL.csv"
DOC = ROOT / "1076-Y5-R10-WEP-parent-material-source-map-or-official-CMSM-import-gate.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_DIR = ROOT / "runs" / "1076-WEP-parent-material-source-map-or-CMSM-import" / "results"
PRODUCT_RUN_DIR = RUN_DIR / "product_runner"
PREDICTION_TEMPLATE = OUT / "P8_Y5_R10_1076_WEP_PRODUCT_CANDIDATE_NONCLAIM.csv"
BOUND_IMPORT = OUT / "P8_Y5_R10_1076_WEP_BOUND_IMPORT.csv"


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
        ("SRC1076_0_1075_next", "source-intake/mts_residuals/P8_Y5_R10_1075_NEXT_TARGET.csv", "1076-Y5-R10-WEP-parent-material-source-map-or-official-CMSM-import-gate.md", "1075 handoff."),
        ("SRC1076_1_1075_validation", "source-intake/mts_residuals/P8_Y5_BRR545_1075_VALIDATION.csv", "V1075_SUMMARY", "1075 validation summary."),
        ("SRC1076_2_1075_replacement", "source-intake/mts_residuals/P8_Y5_R10_1075_REPLACEMENT_GATES.csv", "RG1075_2_material_source_map", "material/source gate still missing."),
        ("SRC1076_3_1075_tau", "source-intake/mts_residuals/P8_Y5_R10_1075_TAU_SHAPE_STATUS.csv", "TAUSHAPE1075_2_physics_tau", "physical tau still missing."),
        ("SRC1076_4_1061_material", "source-intake/mts_residuals/P8_Y5_R10_1061_WEP_MATERIAL_CONVENTION.csv", "MCON1061_1_delta_Q_alpha", "Ti/Pt smoke alpha charge."),
        ("SRC1076_5_651_material", "source-intake/mts_residuals/P8_Y5_R10_651_MICROSCOPE_MATERIAL_MODEL.csv", "MM651_TA6V_Ti", "nominal alloy model."),
        ("SRC1076_6_1068_material_req", "source-intake/mts_residuals/P8_Y5_R10_1068_MATERIAL_RESPONSE_REQUIREMENTS.csv", "MAT1068_5_verdict", "full material response not acquired."),
        ("SRC1076_7_1068_worldtube_req", "source-intake/mts_residuals/P8_Y5_R10_1068_SOURCE_WORLDTUBE_REQUIREMENTS.csv", "SWT1068_5_verdict", "source worldtube not acquired."),
        ("SRC1076_8_1062_parent", "source-intake/mts_residuals/P8_Y5_R10_1062_PARENT_PRODUCT_THEOREM_ATTEMPT.csv", "THM1062_6_verdict", "parent product theorem not closed."),
        ("SRC1076_9_1066_scalar", "source-intake/mts_residuals/P8_Y5_R10_1066_SOURCE_SCALAR_EXCLUSION_LEMMA.csv", "SSE1066_5_verdict", "source scalar exclusion conditional."),
        ("SRC1076_10_1067_action", "source-intake/mts_residuals/P8_Y5_R10_1067_PARENT_ACTION_SCALE_OWNER_ATTEMPT.csv", "ASO1067_5_verdict", "action-scale owner conditional."),
        ("SRC1076_11_708_map", "source-intake/mts_residuals/P8_Y5_R10_708_PPN_GDOT_WEP_MAP.csv", "PGW708_0_R1_WEP", "source/test charge vector missing."),
        ("SRC1076_12_1073_schema", "source-intake/mts_residuals/P8_Y5_R10_1073_OFFICIAL_ARRAY_SCHEMA_CONTRACT.csv", "ARR1073_3_gx", "official CMSM array schema contract."),
        ("SRC1076_13_local_bounds", "source-intake/local_bounds/local_bound_claims.csv", "R1_WEP_source_charge", "MICROSCOPE WEP bound row."),
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


def material_model_rows() -> list[dict[str, object]]:
    material_rows = read_csv(MATERIAL_MODEL)
    groups: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in material_rows:
        groups[row["material_id"]].append(row)
    rows: list[dict[str, object]] = []
    material_values: dict[str, dict[str, float]] = {}
    for material_id, group in sorted(groups.items()):
        z_over_a = 0.0
        neutron_excess = 0.0
        z_mean = 0.0
        a_mean = 0.0
        for item in group:
            fraction = float(item["mass_fraction"])
            z = float(item["Z"])
            a = float(item["A_used"])
            z_over_a += fraction * z / a
            neutron_excess += fraction * (a - 2.0 * z) / a
            z_mean += fraction * z
            a_mean += fraction * a
        material_values[material_id] = {
            "z_over_a": z_over_a,
            "neutron_excess": neutron_excess,
            "z_mean": z_mean,
            "a_mean": a_mean,
        }
        rows.append(
            {
                "material_vector_id": f"MV1076_{material_id}",
                "material_id": material_id,
                "source_rows": ";".join(item["material_model_id"] for item in group),
                "q_Z_over_A_toy": f"{z_over_a:.15e}",
                "q_neutron_excess_toy": f"{neutron_excess:.15e}",
                "Z_mean_toy": f"{z_mean:.15e}",
                "A_mean_toy": f"{a_mean:.15e}",
                "model_status": "TOY_FROM_651_NOMINAL_ALLOY_NOT_PARENT_RESPONSE",
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    ta = material_values.get("TA6V", {})
    pt = material_values.get("PtRh10", {})
    if ta and pt:
        rows.append(
            {
                "material_vector_id": "MV1076_delta_TA6V_minus_PtRh10",
                "material_id": "TA6V_minus_PtRh10",
                "source_rows": "MV1076_TA6V;MV1076_PtRh10;MCON1061_0_test_pair",
                "q_Z_over_A_toy": f"{ta['z_over_a'] - pt['z_over_a']:.15e}",
                "q_neutron_excess_toy": f"{ta['neutron_excess'] - pt['neutron_excess']:.15e}",
                "Z_mean_toy": f"{ta['z_mean'] - pt['z_mean']:.15e}",
                "A_mean_toy": f"{ta['a_mean'] - pt['a_mean']:.15e}",
                "model_status": "TOY_DIFFERENCE_NOT_DELTA_W_NOT_PARENT_DERIVED",
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def existing_input_rows() -> list[dict[str, str]]:
    smoke = next(row for row in read_csv(OUT / "P8_Y5_R10_1061_WEP_MATERIAL_CONVENTION.csv") if row["convention_id"] == "MCON1061_1_delta_Q_alpha")
    return [
        {
            "input_id": "IN1076_0_TiPt_pair",
            "object": "MICROSCOPE Ti/Pt pair",
            "current_value_or_status": "TA6V_minus_PtRh10",
            "source": "MCON1061_0_test_pair",
            "usefulness": "sign and material context",
            "gap_remaining": "does not define parent response vector",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "input_id": "IN1076_1_alpha_smoke_charge",
            "object": "Delta_Q_alpha_Coulomb_abs",
            "current_value_or_status": smoke["numeric_value"],
            "source": "MCON1061_1_delta_Q_alpha",
            "usefulness": "one smoke channel in Damour-Donoghue-like basis",
            "gap_remaining": "not full Ti/Pt material tensor and not parent-derived",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "input_id": "IN1076_2_nominal_alloy_table",
            "object": "PtRh10 and TA6V nominal alloy composition",
            "current_value_or_status": "5 source rows parsed",
            "source": "P8_Y5_R10_651_MICROSCOPE_MATERIAL_MODEL.csv",
            "usefulness": "toy charge-vector construction",
            "gap_remaining": "not isotope/chemical/material tensor and not source-backed enough for WEP claim",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "input_id": "IN1076_3_source_worldtube",
            "object": "Earth/source leg",
            "current_value_or_status": "SOURCE_WORLDTUBE_NOT_ACQUIRED",
            "source": "SWT1068_5_verdict",
            "usefulness": "required for finite WEP product",
            "gap_remaining": "source profile/composition/common-mode theorem missing",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "input_id": "IN1076_4_CMSM_arrays",
            "object": "official MICROSCOPE gx/gz/Sxx/Sxz arrays",
            "current_value_or_status": "MISSING_OFFICIAL_ARRAYS",
            "source": "ARR1073_3_gx; RG1075_0_official_arrays",
            "usefulness": "readout kernel for scoring",
            "gap_remaining": "can be imported later, but does not by itself derive material/source coupling",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def parent_product_contract_rows() -> list[dict[str, str]]:
    return [
        {
            "contract_id": "PWC1076_0_direct_product",
            "object": "direct WEP parent product",
            "formal_contract": "P_WEP = abs(Readout_MICROSCOPE[delta a_TA6V - delta a_PtRh10]) derived directly from delta S_parent",
            "required_parent_objects": "parent variation; observed coframe; source worldtube; material response; orbit/readout kernel",
            "current_status": "MISSING_DIRECT_PARENT_PRODUCT",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "contract_id": "PWC1076_1_factorized_product",
            "object": "finite factorized WEP product",
            "formal_contract": "P_WEP = abs(<R_source^Earth, C_parent (R_TA6V - R_PtRh10)>_K)",
            "required_parent_objects": "R_source^Earth; R_TA6V; R_PtRh10; coupling owner C_parent; kernel K; Xhat normalization",
            "current_status": "FORMAL_SHAPE_STAGED_FACTORS_MISSING",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "contract_id": "PWC1076_2_theorem_zero",
            "object": "universal metric/coframe theorem-zero",
            "formal_contract": "If C_parent has only universal metric/coframe coupling and no species/source labels, then R_TA6V - R_PtRh10 is invisible to WEP and P_WEP=0",
            "required_parent_objects": "source-scalar exclusion; species-blind action measure; current owner; readout closure",
            "current_status": "CONDITIONAL_ZERO_UNSIGNED",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "contract_id": "PWC1076_3_CMSM_import_gate",
            "object": "official array import alternative",
            "formal_contract": "CMSM official gx/gz/Sxx/Sxz arrays may replace surrogate kernel columns but do not replace R_source/R_material/C_parent",
            "required_parent_objects": "official arrays plus parent material/source product",
            "current_status": "ARRAY_GATE_OPEN_COUPLING_GATE_CLOSED",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def derivation_attempt_rows() -> list[dict[str, str]]:
    return [
        {
            "attempt_id": "DER1076_0_material_response_definition",
            "claim": "define material response vector from parent matter action",
            "formal_move": "R_A^I := partial ln m_A / partial X_I or Hilbert-current response delta S_A/delta X_I after canonical parent normalization",
            "result": "DEFINITION_SHARPENED_NOT_DERIVED",
            "gap": "parent fields/coupling basis X_I and mass/current normalization owner are not signed",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "attempt_id": "DER1076_1_source_leg_definition",
            "claim": "derive Earth/source response vector",
            "formal_move": "R_source^I := integral_Earth K_source(x) delta T_source(x)/delta X_I with common-mode GM removed only after universality proof",
            "result": "SOURCE_LEG_FORM_ONLY",
            "gap": "source worldtube/profile/composition and common-mode theorem missing",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "attempt_id": "DER1076_2_coupling_owner",
            "claim": "one parent coupling owner C_parent controls material and source legs",
            "formal_move": "C_parent must descend from parent action coefficients, not post-fit beta_source or tau slots",
            "result": "OWNER_REQUIRED_NOT_FOUND",
            "gap": "source-scalar exclusion and action-scale owner remain conditional in 1066/1067",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "attempt_id": "DER1076_3_toy_material_vector",
            "claim": "use 651 alloy table to create a placeholder material vector",
            "formal_move": "compute toy Z/A and neutron-excess differences for TA6V_minus_PtRh10",
            "result": "TOY_VECTOR_AVAILABLE_NONCLAIM",
            "gap": "toy vector is not Delta_w, not full material tensor, and not parent-derived",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "attempt_id": "DER1076_4_zero_branch",
            "claim": "close WEP by theorem-zero rather than finite product",
            "formal_move": "universal parent metric/coframe coupling + species-blind measure => no relative source-weight channel",
            "result": "BEST_DERIVATION_ROUTE_BUT_UNSIGNED",
            "gap": "must prove parent object-language/current/action-measure owner",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "attempt_id": "DER1076_5_verdict",
            "claim": "parent material/source map derivation",
            "formal_move": "derive or stage R_source, R_TA6V, R_PtRh10, and C_parent",
            "result": "NOT_DERIVED_CURRENT_CORPUS",
            "gap": "exact contract staged; coupling-owner theorem is next",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def coupling_owner_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "OWN1076_0_parent_object_language",
            "owner_object": "parent coupling basis X_I",
            "required_evidence": "typed parent object language or explicit finite coupling basis",
            "current_status": "MISSING_PARENT_COUPLING_BASIS",
            "blocks": "R_A^I and R_source^I definitions",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "OWN1076_1_species_blind_measure",
            "owner_object": "action-scale/measure owner",
            "required_evidence": "single hbar/action measure and species-blind Jacobian",
            "current_status": "CONDITIONAL_NOT_PARENT_DERIVED",
            "blocks": "theorem-zero WEP closure",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "OWN1076_2_current_owner",
            "owner_object": "current/source normalization",
            "required_evidence": "one current owner shared by source and test sectors",
            "current_status": "MISSING_CURRENT_OWNER",
            "blocks": "source-only weight exclusion",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "OWN1076_3_material_tensor",
            "owner_object": "Ti/Pt material response tensor",
            "required_evidence": "source-backed tensor or parent theorem reducing all ordinary matter to universal response",
            "current_status": "TOY_VECTOR_ONLY",
            "blocks": "finite WEP product",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "OWN1076_4_source_worldtube",
            "owner_object": "Earth/source response",
            "required_evidence": "source profile/composition or theorem reducing source leg to common universal mode",
            "current_status": "MISSING_SOURCE_WORLDTUBE",
            "blocks": "finite WEP product",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "OWN1076_5_CMSM_arrays",
            "owner_object": "official MICROSCOPE readout arrays",
            "required_evidence": "CMSM gx/gz/Sxx/Sxz arrays and masks",
            "current_status": "MISSING_OFFICIAL_ARRAYS",
            "blocks": "empirical readout scoring but not parent coupling derivation",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def official_import_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "import_id": "IMP1076_0_official_arrays",
            "artifact": "CMSM gx/gz/Sxx/Sxz arrays",
            "required_columns": "segment_id;t_utc;mask_flag;gx;gz;Sxx;Sxz;generation_method;source_file",
            "current_status": "NOT_IMPORTED",
            "effect_if_imported": "replaces surrogate kernel columns in 1075 design matrix",
            "remaining_after_import": "parent material/source map and coupling owner still required",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "import_id": "IMP1076_1_exact_masks",
            "artifact": "exact MICROSCOPE segment masks",
            "required_columns": "segment_id;t_utc;sample_index;mask_flag;mask_reason",
            "current_status": "NOT_IMPORTED",
            "effect_if_imported": "replaces all-unmasked surrogate rows",
            "remaining_after_import": "official acceleration/readout and parent product still required",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "import_id": "IMP1076_2_kernel_score",
            "artifact": "official-kernel WEP design matrix",
            "required_columns": "polynomial;gx;gz;Sxx;Sxz;mask;weights",
            "current_status": "NOT_BUILDABLE",
            "effect_if_imported": "allows data-side score runner",
            "remaining_after_import": "MTS prediction still invalid until P_WEP or tau_WEP product is derived",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def product_prediction_rows() -> list[dict[str, str]]:
    return [
        {
            "prediction_id": "PRED1076_0_WEP_parent_material_source_map_nonclaim",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "P_WEP_relative_source_weight",
            "product_value": "MISSING_PARENT_MATERIAL_SOURCE_MAP_AND_OFFICIAL_ARRAYS",
            "product_units": "dimensionless",
            "product_source": "source-intake/mts_residuals/P8_Y5_R10_1076_PARENT_PRODUCT_CONTRACT_UPDATE.csv",
            "inputs_present": "TiPt_pair;alpha_smoke_charge;toy_alloy_vector;surrogate_design_matrix;formal_product_contract",
            "required_inputs": "parent coupling owner; R_source; R_TA6V; R_PtRh10; official kernel arrays or validated readout; Xhat normalization",
            "derivation_status": "CONTRACT_STAGED_PRODUCT_MISSING",
            "valid_for_claim": "false",
            "notes": "parent map is not derived; toy material vectors cannot score WEP",
        }
    ]


def bound_rows() -> list[dict[str, str]]:
    row = local_bound_row("R1_WEP_source_charge")
    url, doi = split_reference(row["reference_path_or_url"])
    return [
        {
            "bound_id": "BOUND1076_0_MICROSCOPE_R1_eta_source_charge",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "P_WEP_relative_source_weight",
            "bound_value": row["upper_bound"],
            "bound_units": row["units"],
            "bound_source": url,
            "source_row": f"source-intake/local_bounds/local_bound_claims.csv::{row['row_id']}; doi:{doi}",
            "bound_type": "source_backed_upper_bound_anchor",
            "valid_for_claim": "true",
            "notes": "valid bound anchor only; MTS parent product remains missing",
        }
    ]


def product_status_rows(status: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "runner_id": "APR1076_0_WEP_parent_map_product_stub",
            "prediction_rows": str(status.get("prediction_rows", "")),
            "bound_rows": str(status.get("bound_rows", "")),
            "valid_prediction_rows": str(status.get("valid_prediction_rows", "")),
            "valid_bound_rows": str(status.get("valid_bound_rows", "")),
            "comparison_rows": str(status.get("comparison_rows", "")),
            "passed_rows": str(status.get("passed_rows", "")),
            "claim_allowed": str(status.get("claim_allowed", "")).lower(),
            "expected_result": "reject missing parent material/source map and keep claim false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def claim_gate_rows(product_status: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "gate_id": "CG1076_0_toy_material_vector",
            "claim_component": "toy Ti/Pt material vector",
            "gate_pass": "true",
            "claim_allowed": "false",
            "reason": "toy vector is useful but not parent response",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1076_1_parent_coupling_owner",
            "claim_component": "parent coupling owner",
            "gate_pass": "false",
            "claim_allowed": "false",
            "reason": "MISSING_PARENT_COUPLING_BASIS_AND_OWNER",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1076_2_source_worldtube",
            "claim_component": "Earth/source response leg",
            "gate_pass": "false",
            "claim_allowed": "false",
            "reason": "MISSING_SOURCE_WORLDTUBE",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1076_3_official_CMSM_arrays",
            "claim_component": "official MICROSCOPE kernel arrays",
            "gate_pass": "false",
            "claim_allowed": "false",
            "reason": "MISSING_OFFICIAL_ARRAYS",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1076_4_product_runner",
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
            "decision_id": "DEC1076_0_parent_map_not_derived",
            "decision": "parent material/source response map is not derived by current corpus",
            "evidence": "DER1076_5_verdict; OWN1076_0_parent_object_language",
            "consequence": "WEP/local-GR product remains blocked",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1076_1_toy_vector_staged",
            "decision": "toy Ti/Pt material vector is staged for nonclaim algebra tests",
            "evidence": "MV1076_delta_TA6V_minus_PtRh10",
            "consequence": "can test map plumbing but not score MICROSCOPE",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1076_2_best_next",
            "decision": "best next move is the parent WEP coupling-owner theorem",
            "evidence": "DER1076_4_zero_branch; OWN1076_1_species_blind_measure",
            "consequence": "try to close theorem-zero or explicitly demote WEP finite branch to sourced-input route",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_id": "NEXT1076_0_1077",
            "next_target": "1077-Y5-R10-parent-WEP-coupling-owner-theorem-or-material-vector-source-row.md",
            "objective": "attempt the parent WEP coupling-owner theorem: either prove ordinary matter has only universal metric/coframe coupling with species-blind action measure/current owner, yielding theorem-zero WEP, or explicitly require sourced finite material/source vectors.",
            "include": "parent object-language typing; species-blind action measure; current/source normalization owner; Ti/Pt toy vector demotion; Earth/source leg; no measured-G absorption; product-runner refusal",
            "exclude": "Delta_w=0 by taste; tau=1; cancellation tuning; treating toy material vector as evidence; public WEP/local-GR claim; GitHub; formalization edits",
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
    input_rows: list[dict[str, str]],
    material_rows: list[dict[str, object]],
    contract_rows: list[dict[str, str]],
    derivation_rows: list[dict[str, str]],
    owner_rows: list[dict[str, str]],
    import_rows: list[dict[str, str]],
    prediction_rows: list[dict[str, str]],
    bound_rows_: list[dict[str, str]],
    product_status: dict[str, Any],
    claim_rows: list[dict[str, str]],
    next_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    material_ids = {row["material_vector_id"] for row in material_rows}
    checks: list[tuple[str, bool, str]] = []
    checks.append(("V1076_0_sources_exist", all(row["exists"] == "true" and row["needle_found"] == "true" for row in source_rows), "all cited local source paths and needles are present"))
    checks.append(("V1076_1_inputs_staged", len(input_rows) == 5 and all(row["valid_for_claim"] == "false" for row in input_rows), "existing WEP inputs staged as nonclaim"))
    checks.append(("V1076_2_material_toy_vector", {"MV1076_TA6V", "MV1076_PtRh10", "MV1076_delta_TA6V_minus_PtRh10"}.issubset(material_ids) and all(row["valid_for_claim"] == "false" for row in material_rows), "toy Ti/Pt material vectors computed and nonclaim"))
    checks.append(("V1076_3_product_contract", any(row["contract_id"] == "PWC1076_1_factorized_product" and "R_source^Earth" in row["formal_contract"] for row in contract_rows), "factorized parent product contract staged"))
    checks.append(("V1076_4_derivation_not_closed", any(row["attempt_id"] == "DER1076_5_verdict" and row["result"] == "NOT_DERIVED_CURRENT_CORPUS" for row in derivation_rows), "derivation verdict remains not closed"))
    checks.append(("V1076_5_owner_gates_block", any(row["gate_id"] == "OWN1076_0_parent_object_language" and row["current_status"] == "MISSING_PARENT_COUPLING_BASIS" for row in owner_rows) and any(row["gate_id"] == "OWN1076_4_source_worldtube" for row in owner_rows), "parent coupling/source owner gates block claims"))
    checks.append(("V1076_6_import_gate_open_not_sufficient", len(import_rows) == 3 and all(row["valid_for_claim"] == "false" for row in import_rows), "official import gate remains staged but nonclaim"))
    checks.append(("V1076_7_prediction_nonclaim_missing", any("MISSING_PARENT_MATERIAL_SOURCE_MAP" in row["product_value"] and row["valid_for_claim"] == "false" for row in prediction_rows), "prediction row remains missing parent map"))
    checks.append(("V1076_8_bound_numeric", bool(bound_rows_) and float(bound_rows_[0]["bound_value"]) > 0 and bound_rows_[0]["valid_for_claim"] == "true", "bound import is positive numeric"))
    checks.append(("V1076_9_runner_refuses", product_status.get("valid_prediction_rows") == 0 and product_status.get("claim_allowed") is False, "runner reports no valid prediction rows and claim false"))
    checks.append(("V1076_10_claim_gates_safe", all(row["claim_allowed"] == "false" for row in claim_rows), "all claim gates deny WEP/local-GR claim"))
    checks.append(("V1076_11_next_target", any("1077-Y5-R10-parent-WEP-coupling-owner-theorem-or-material-vector-source-row.md" in row["next_target"] for row in next_rows), "1077 handoff written"))
    generated_paths = list(outputs.values()) + [DOC]
    checks.append(("V1076_12_generated_under_post_checkpoint", all(str(path.resolve()).startswith(str(ROOT.resolve())) for path in generated_paths), "all generated outputs are under post-checkpoint-work"))
    checks.append(("V1076_13_csv_parse", all(path.exists() and csv_rows_parse(path) for path in outputs.values() if path.suffix == ".csv" and path.name != "P8_Y5_BRR545_1076_VALIDATION.csv"), "all 1076 CSV outputs parse cleanly"))
    checks.append(("V1076_14_formalization_untouched", count_formalization_modified_since_start() == 0, "formalization-workbench modified-file count remains zero"))
    checks.append(("V1076_SUMMARY", True, "parent material/source map not derived; toy material vector and exact product contract staged; WEP/product claim blocked"))
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
    input_rows: list[dict[str, str]],
    material_rows: list[dict[str, object]],
    contract_rows: list[dict[str, str]],
    derivation_rows: list[dict[str, str]],
    owner_rows: list[dict[str, str]],
    import_rows: list[dict[str, str]],
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
            "# 1076 - WEP parent material/source map or official CMSM import gate",
            "",
            "## Current verdict",
            "1076 does not derive the parent material/source response map. It stages the exact WEP product contract and a toy Ti/Pt material vector from the nominal alloy table, but the parent coupling owner, Earth/source leg, species-blind measure/current theorem, and official CMSM arrays remain missing.",
            "",
            "## Local source register",
            md_table(source_rows, ["source_id", "relative_path", "exists", "needle_found", "note"]),
            "## Existing input status",
            md_table(input_rows, ["input_id", "object", "current_value_or_status", "source", "gap_remaining"]),
            "## Toy material vector",
            md_table(material_rows, ["material_vector_id", "material_id", "q_Z_over_A_toy", "q_neutron_excess_toy", "model_status"]),
            "## Parent product contract",
            md_table(contract_rows, ["contract_id", "object", "formal_contract", "current_status"]),
            "## Derivation attempt",
            md_table(derivation_rows, ["attempt_id", "claim", "result", "gap"]),
            "## Coupling owner gates",
            md_table(owner_rows, ["gate_id", "owner_object", "current_status", "blocks"]),
            "## Official CMSM import gate",
            md_table(import_rows, ["import_id", "artifact", "current_status", "effect_if_imported", "remaining_after_import"]),
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
            md_table(decisions, ["decision_id", "decision", "evidence", "consequence"]),
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
    input_rows = existing_input_rows()
    material_rows = material_model_rows()
    contract_rows = parent_product_contract_rows()
    derivation_rows = derivation_attempt_rows()
    owner_rows = coupling_owner_gate_rows()
    import_rows = official_import_gate_rows()
    prediction_rows = product_prediction_rows()
    bound_rows_ = bound_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    outputs = {
        "source_register": OUT / "P8_Y5_R10_1076_SOURCE_REGISTER.csv",
        "inputs": OUT / "P8_Y5_R10_1076_EXISTING_WEP_INPUT_STATUS.csv",
        "material_vector": OUT / "P8_Y5_R10_1076_TOY_MATERIAL_VECTOR_FROM_651.csv",
        "contract": OUT / "P8_Y5_R10_1076_PARENT_PRODUCT_CONTRACT_UPDATE.csv",
        "derivation": OUT / "P8_Y5_R10_1076_PARENT_MAP_DERIVATION_ATTEMPT.csv",
        "owner_gates": OUT / "P8_Y5_R10_1076_COUPLING_OWNER_GATES.csv",
        "import_gate": OUT / "P8_Y5_R10_1076_OFFICIAL_CMSM_IMPORT_GATE.csv",
        "prediction": PREDICTION_TEMPLATE,
        "bound": BOUND_IMPORT,
        "product_status": OUT / "P8_Y5_R10_1076_PRODUCT_RUNNER_STATUS.csv",
        "product_comparison": OUT / "P8_Y5_R10_1076_PRODUCT_COMPARISON_ROWS.csv",
        "claim_gates": OUT / "P8_Y5_R10_1076_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_R10_1076_DECISION_LEDGER.csv",
        "next_target": OUT / "P8_Y5_R10_1076_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_1076_VALIDATION.csv",
    }

    write_csv(outputs["source_register"], source_rows)
    write_csv(outputs["inputs"], input_rows)
    write_csv(outputs["material_vector"], material_rows)
    write_csv(outputs["contract"], contract_rows)
    write_csv(outputs["derivation"], derivation_rows)
    write_csv(outputs["owner_gates"], owner_rows)
    write_csv(outputs["import_gate"], import_rows)
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
        input_rows,
        material_rows,
        contract_rows,
        derivation_rows,
        owner_rows,
        import_rows,
        prediction_rows,
        bound_rows_,
        product_status,
        claim_rows,
        next_rows,
    )
    write_csv(outputs["validation"], validation_rows)
    write_doc(
        source_rows,
        input_rows,
        material_rows,
        contract_rows,
        derivation_rows,
        owner_rows,
        import_rows,
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
