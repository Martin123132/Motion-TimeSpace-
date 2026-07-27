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
DOC = ROOT / "1083-Y5-R10-DD-Earth-source-vector-extraction-plan-and-nonclaim-first-row.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_DIR = ROOT / "runs" / "1083-DD-Earth-source-vector-extraction-plan" / "results"
PRODUCT_RUN_DIR = RUN_DIR / "product_runner"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds" / "local_bound_claims.csv"
DD_MATERIAL_DELTA = OUT / "P8_Y5_R10_1081_DD_MATERIAL_DELTA_IMPORT.csv"
PREDICTION_TEMPLATE = OUT / "P8_Y5_R10_1083_WEP_PRODUCT_CANDIDATE_NONCLAIM.csv"
BOUND_IMPORT = OUT / "P8_Y5_R10_1083_WEP_BOUND_IMPORT.csv"

ETA_BOUND = 2.8e-15

ELEMENTS = [
    ("Fe", 32.0, 26, 55.845),
    ("O", 29.7, 8, 15.999),
    ("Si", 16.1, 14, 28.085),
    ("Mg", 15.4, 12, 24.305),
    ("Ni", 1.82, 28, 58.693),
    ("Ca", 1.71, 20, 40.078),
    ("Al", 1.59, 13, 26.982),
    ("S", 0.64, 16, 32.06),
    ("Cr", 0.47, 24, 51.996),
    ("Na", 0.18, 11, 22.990),
    ("P", 0.07, 15, 30.974),
    ("Mn", 0.08, 25, 54.938),
    ("C", 0.07, 6, 12.011),
    ("H", 0.03, 1, 1.008),
]


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


def parse_float(value: object) -> float | None:
    try:
        return float(str(value).strip())
    except ValueError:
        return None


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


def source_register_rows() -> list[dict[str, str]]:
    specs = [
        ("SRC1083_0_1082_next", "source-intake/mts_residuals/P8_Y5_R10_1082_NEXT_TARGET.csv", "1083-Y5-R10-DD-Earth-source-vector-extraction-plan-and-nonclaim-first-row.md", "1082 handoff."),
        ("SRC1083_1_1082_validation", "source-intake/mts_residuals/P8_Y5_BRR545_1082_VALIDATION.csv", "V1082_SUMMARY", "1082 validation summary."),
        ("SRC1083_2_1082_earth_fill", "source-intake/mts_residuals/P8_Y5_R10_1082_PHYSICAL_EARTH_SOURCE_FILL_ROWS.csv", "ESF1082_1_vectorization", "Earth source vectorization gap."),
        ("SRC1083_3_1082_parent_to_DD", "source-intake/mts_residuals/P8_Y5_R10_1082_PARENT_TO_DD_COEFFICIENT_MAP_ATTEMPT.csv", "PTD1082_4_verdict", "parent-to-DD map remains unsigned."),
        ("SRC1083_4_1082_readout_fill", "source-intake/mts_residuals/P8_Y5_R10_1082_PHYSICAL_MICROSCOPE_READOUT_FILL_ROWS.csv", "ROF1082_0_official_arrays", "MICROSCOPE readout arrays still missing."),
        ("SRC1083_5_1081_delta", "source-intake/mts_residuals/P8_Y5_R10_1081_DD_MATERIAL_DELTA_IMPORT.csv", "DDM1081_0_delta_alpha", "DD material delta import."),
        ("SRC1083_6_1081_basis", "source-intake/mts_residuals/P8_Y5_R10_1081_DD_BASIS_SCHEMA.csv", "DDB1081_0_alpha_Coulomb", "DD basis schema."),
        ("SRC1083_7_1080_web", "source-intake/mts_residuals/P8_Y5_R10_1080_WEB_SOURCE_CANDIDATE_REGISTER.csv", "WEB1080_2_MCDONOUGH_SUN_1995", "web source candidate register."),
        ("SRC1083_8_1080_earth", "source-intake/mts_residuals/P8_Y5_R10_1080_EARTH_SOURCE_VECTOR_CANDIDATES.csv", "EARTH1080_2_parent_basis_block", "Earth source route gates."),
        ("SRC1083_9_1080_readout", "source-intake/mts_residuals/P8_Y5_R10_1080_MICROSCOPE_READOUT_GATE.csv", "READ1080_1_CMSM_portal", "MICROSCOPE readout gate."),
        ("SRC1083_10_local_bounds", "source-intake/local_bounds/local_bound_claims.csv", "R1_WEP_source_charge", "MICROSCOPE WEP bound row."),
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


def web_source_register_rows() -> list[dict[str, str]]:
    return [
        {
            "web_source_id": "WEB1083_0_MCDONOUGH_2003_TABLE5",
            "role": "bulk Earth composition table target",
            "source_url": "https://www.mso.anu.edu.au/PSI/PSI_Meetings/Entries/2007/6/13_The_bulk_composition_of_the_Earth_%281%29_files/Treatise%20on%20Geochemistry%202003%20McDonough.pdf",
            "source_title": "Compositional Model for the Earth's Core",
            "evidence_used": "Table 5 bulk Earth wt.% abundant-element rows plus text stating the table compares bulk Earth, silicate Earth, and core by weight percent and atomic proportion",
            "extraction_method": "manual table-target transcription into candidate rows; not a machine-readable official table import",
            "confidence_level": "medium_for_nonclaim_source_vector; insufficient_for_claim",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "web_source_id": "WEB1083_1_MCDONOUGH_SUN_1995",
            "role": "composition provenance continuity",
            "source_url": "https://earthref.org/ERR/n%3A3%2Cb%3Aaaaa0000003tab05/",
            "source_title": "McDonough and Sun 1995, Composition of the Earth",
            "evidence_used": "older bulk-Earth/silicate-Earth composition reference already registered in 1080",
            "extraction_method": "provenance link only; no new numeric extraction from this page",
            "confidence_level": "source-continuity-only",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "web_source_id": "WEB1083_2_DAMOUR_DONOGHUE_2010",
            "role": "external DD alpha/surface charge basis",
            "source_url": "https://arxiv.org/abs/1007.2792",
            "source_title": "Equivalence Principle Violations and Couplings of a Light Dilaton",
            "evidence_used": "two dominant composition-charge style used by the existing 1053/1081 smoke matrix",
            "extraction_method": "reuse existing local smoke convention rather than promote the external basis to MTS",
            "confidence_level": "good_for_external_comparator; not_MTS_derived",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "web_source_id": "WEB1083_3_MICROSCOPE_FINAL",
            "role": "WEP bound source",
            "source_url": "https://arxiv.org/abs/2209.15487",
            "source_title": "MICROSCOPE mission: final results of the test of the Equivalence Principle",
            "evidence_used": "eta(Ti,Pt) final-result bound inherited from local_bound_claims.csv",
            "extraction_method": "bound import only; official readout arrays still not imported",
            "confidence_level": "bound_source_backed; prediction_nonclaim",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def q_alpha_coulomb(z_value: int, a_value: float) -> float:
    return 7.7e-4 * z_value * (z_value - 1) / (a_value ** (4.0 / 3.0))


def q_surface_binding(z_value: int, a_value: float) -> float:
    return -0.036 / (a_value ** (1.0 / 3.0)) - 1.4e-4 * z_value * (z_value - 1) / (a_value ** (4.0 / 3.0))


def composition_sum() -> float:
    return sum(wt_percent for _, wt_percent, _, _ in ELEMENTS)


def bulk_earth_composition_target_rows() -> list[dict[str, str]]:
    total = composition_sum()
    return [
        {
            "element": element,
            "wt_percent": f"{wt_percent:.12g}",
            "normalized_mass_fraction": f"{wt_percent / total:.15e}",
            "Z": str(z_value),
            "A": f"{a_value:.12g}",
            "source_table": "WEB1083_0_MCDONOUGH_2003_TABLE5",
            "extraction_status": "TABLE_TARGET_CANDIDATE_NONCLAIM",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for element, wt_percent, z_value, a_value in ELEMENTS
    ]


def dd_charge_formula_rows() -> list[dict[str, str]]:
    return [
        {
            "formula_id": "DDF1083_0_alpha_Coulomb",
            "component": "Q_alpha_Coulomb",
            "formula": "7.7e-4 * Z*(Z-1) / A^(4/3)",
            "basis_source": "WEB1083_2_DAMOUR_DONOGHUE_2010; local WCM1053_4 convention",
            "status": "IMPORTED_FROM_EXISTING_SMOKE_CONVENTION_NONCLAIM",
            "claim_blocker": "not derived from MTS parent action",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "formula_id": "DDF1083_1_surface_binding",
            "component": "Q_surface_binding",
            "formula": "-0.036 / A^(1/3) - 1.4e-4 * Z*(Z-1) / A^(4/3)",
            "basis_source": "WEB1083_2_DAMOUR_DONOGHUE_2010; local WCM1053_5 convention",
            "status": "IMPORTED_FROM_EXISTING_SMOKE_CONVENTION_NONCLAIM",
            "claim_blocker": "not derived from MTS parent action",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def dd_earth_element_charge_rows() -> list[dict[str, str]]:
    total = composition_sum()
    rows: list[dict[str, str]] = []
    for element, wt_percent, z_value, a_value in ELEMENTS:
        fraction = wt_percent / total
        alpha = q_alpha_coulomb(z_value, a_value)
        surface = q_surface_binding(z_value, a_value)
        rows.append(
            {
                "charge_id": f"DEC1083_{element}",
                "element": element,
                "normalized_mass_fraction": f"{fraction:.15e}",
                "Z": str(z_value),
                "A": f"{a_value:.12g}",
                "Q_alpha_Coulomb": f"{alpha:.15e}",
                "Q_surface_binding": f"{surface:.15e}",
                "weighted_Q_alpha_Coulomb": f"{fraction * alpha:.15e}",
                "weighted_Q_surface_binding": f"{fraction * surface:.15e}",
                "status": "NUMERIC_ELEMENT_DD_CHARGE_NONCLAIM",
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def earth_source_vector_values() -> dict[str, float]:
    rows = dd_earth_element_charge_rows()
    return {
        "composition_sum_wt_percent": composition_sum(),
        "normalized_mass_fraction_sum": sum(float(row["normalized_mass_fraction"]) for row in rows),
        "Q_alpha_Coulomb_Earth": sum(float(row["weighted_Q_alpha_Coulomb"]) for row in rows),
        "Q_surface_binding_Earth": sum(float(row["weighted_Q_surface_binding"]) for row in rows),
    }


def earth_source_vector_rows(values: dict[str, float]) -> list[dict[str, str]]:
    return [
        {
            "source_vector_id": "DD_EARTH1083_0_bulk_weighted",
            "source_body": "Earth",
            "basis": "DD_Q_alpha_Coulomb_Q_surface_binding",
            "Q_alpha_Coulomb_Earth": f"{values['Q_alpha_Coulomb_Earth']:.15e}",
            "Q_surface_binding_Earth": f"{values['Q_surface_binding_Earth']:.15e}",
            "composition_sum_wt_percent": f"{values['composition_sum_wt_percent']:.12g}",
            "normalized_mass_fraction_sum": f"{values['normalized_mass_fraction_sum']:.15e}",
            "source_rows": "P8_Y5_R10_1083_BULK_EARTH_COMPOSITION_TARGET.csv; P8_Y5_R10_1083_DD_EARTH_ELEMENT_CHARGES.csv",
            "status": "NUMERIC_BULK_EARTH_DD_SOURCE_VECTOR_NONCLAIM",
            "claim_blocker": "bulk Earth source is not shell/profile/worldtube weighted and parent-to-DD/readout maps remain missing",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def material_delta_by_id() -> dict[str, dict[str, str]]:
    return {row["delta_id"]: row for row in read_csv(DD_MATERIAL_DELTA)}


def source_material_product_rows(values: dict[str, float]) -> list[dict[str, str]]:
    deltas = material_delta_by_id()
    alpha_delta_abs = float(deltas["DDM1081_0_delta_alpha"]["delta_abs"])
    surface_delta_abs = float(deltas["DDM1081_1_delta_surface"]["delta_abs"])
    alpha_product = values["Q_alpha_Coulomb_Earth"] * alpha_delta_abs
    surface_product = values["Q_surface_binding_Earth"] * surface_delta_abs
    combined_abs = abs(alpha_product) + abs(surface_product)
    equal_product_coefficient_bound = ETA_BOUND / combined_abs
    return [
        {
            "product_id": "DD_PRODUCT1083_0_alpha",
            "component": "Q_alpha_Coulomb",
            "source_value": f"{values['Q_alpha_Coulomb_Earth']:.15e}",
            "material_delta_abs": f"{alpha_delta_abs:.15e}",
            "source_material_product": f"{alpha_product:.15e}",
            "product_abs": f"{abs(alpha_product):.15e}",
            "eta_bound": f"{ETA_BOUND:.15e}",
            "required_abs_coefficient_max_if_single_component": f"{ETA_BOUND / abs(alpha_product):.15e}",
            "status": "NUMERIC_DD_SOURCE_MATERIAL_PRODUCT_NONCLAIM",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "product_id": "DD_PRODUCT1083_1_surface",
            "component": "Q_surface_binding",
            "source_value": f"{values['Q_surface_binding_Earth']:.15e}",
            "material_delta_abs": f"{surface_delta_abs:.15e}",
            "source_material_product": f"{surface_product:.15e}",
            "product_abs": f"{abs(surface_product):.15e}",
            "eta_bound": f"{ETA_BOUND:.15e}",
            "required_abs_coefficient_max_if_single_component": f"{ETA_BOUND / abs(surface_product):.15e}",
            "status": "NUMERIC_DD_SOURCE_MATERIAL_PRODUCT_NONCLAIM",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "product_id": "DD_PRODUCT1083_2_combined_abs",
            "component": "Q_alpha_Coulomb + Q_surface_binding",
            "source_value": "bulk Earth DD two-component vector",
            "material_delta_abs": "TA6V_minus_PtRh10 DD two-component abs deltas",
            "source_material_product": f"{alpha_product + surface_product:.15e}",
            "product_abs": f"{combined_abs:.15e}",
            "eta_bound": f"{ETA_BOUND:.15e}",
            "required_abs_coefficient_max_if_equal_component": f"{equal_product_coefficient_bound:.15e}",
            "status": "NUMERIC_DD_SOURCE_MATERIAL_PRODUCT_NONCLAIM",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def source_vector_caveat_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "SCG1083_0_profile_weighting",
            "claim_component": "Earth source profile/worldtube weighting",
            "gate_pass": "false",
            "status": "MISSING_SOURCE_PROFILE_WEIGHTING",
            "reason": "bulk composition is not the same object as the orbit- and shell-weighted source vector seen by MICROSCOPE",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "SCG1083_1_parent_to_DD_map",
            "claim_component": "C_parent -> DD coefficient map",
            "gate_pass": "false",
            "status": "MISSING_PARENT_OPERATOR_BASIS_MAP",
            "reason": "alpha/surface DD basis remains external comparator not an MTS-derived basis",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "SCG1083_2_official_readout",
            "claim_component": "K_MICROSCOPE official readout",
            "gate_pass": "false",
            "status": "OFFICIAL_ARRAYS_NOT_IMPORTED",
            "reason": "gx/gz/Sxx/Sxz/masks/timing arrays or validated export are not yet in the product convention",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "SCG1083_3_no_measured_G_absorption",
            "claim_component": "source response treatment",
            "gate_pass": "false",
            "status": "NO_ABSORPTION_SHORTCUT_ALLOWED",
            "reason": "measured-G absorption would hide the finite WEP branch instead of deriving or bounding it",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def common_mode_alternative_rows() -> list[dict[str, str]]:
    return [
        {
            "route_id": "CMA1083_0_theorem_target",
            "claim": "Earth source vector cancels as a universal common mode",
            "needed_parent_clause": "source-side coupling is species-blind and appears only as a common acceleration scale before differential readout",
            "status": "THEOREM_TARGET_DEFINED",
            "gap": "must be proven before replacing the explicit source vector",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "route_id": "CMA1083_1_counterpressure",
            "claim": "source vector may be ignored",
            "needed_parent_clause": "no source-composition dependent residual and no measured-G absorption",
            "status": "NOT_SIGNED",
            "gap": "finite WEP products generally contain source x test-material response unless parent action kills the source leg",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "route_id": "CMA1083_2_verdict",
            "claim": "common-mode route closes 1083",
            "needed_parent_clause": "parent-signed common-mode theorem",
            "status": "SOURCE_COMMON_MODE_NOT_SIGNED",
            "gap": "retain explicit source-vector acquisition route",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def prediction_rows() -> list[dict[str, str]]:
    return [
        {
            "prediction_id": "PRED1083_0_DD_Earth_source_vector_nonclaim",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "P_WEP_relative_source_weight",
            "product_value": "MISSING_MTS_COEFFICIENT_MAP_AND_OFFICIAL_READOUT_FOR_DD_EARTH_SOURCE_VECTOR",
            "product_units": "dimensionless",
            "product_source": "source-intake/mts_residuals/P8_Y5_R10_1083_DD_EARTH_SOURCE_VECTOR_FIRST_ROW_NONCLAIM.csv",
            "inputs_present": "bulk Earth DD source vector candidate; DD material deltas; MICROSCOPE bound",
            "required_inputs": "MTS parent-to-DD coefficient map; source profile/worldtube weighting; official K_MICROSCOPE readout; C_parent vector",
            "derivation_status": "SOURCE_VECTOR_NUMERIC_BUT_MTS_PRODUCT_MISSING",
            "valid_for_claim": "false",
            "notes": "generic product runner must refuse; numeric DD products live in the nonclaim product ledger only",
        }
    ]


def bound_import_rows() -> list[dict[str, str]]:
    return [
        {
            "bound_id": "BOUND1083_0_MICROSCOPE_WEP_source_charge",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "P_WEP_relative_source_weight",
            "bound_value": f"{ETA_BOUND:.15e}",
            "bound_units": "dimensionless",
            "bound_source": "https://arxiv.org/abs/2209.15487",
            "source_row": "MICROSCOPE_final_TiPt_source_charge_proxy:R1_WEP_source_charge;doi:10.1103/PhysRevLett.129.121102",
            "bound_type": "upper_abs_WEP_proxy_bound",
            "valid_for_claim": "true",
            "notes": "source-backed numeric bound only; MTS prediction remains invalid",
        }
    ]


def product_status_rows(product_status: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "runner_id": "APR1083_0_DD_Earth_source_vector_product_stub",
            "prediction_rows": str(product_status.get("prediction_rows", "")),
            "bound_rows": str(product_status.get("bound_rows", "")),
            "valid_prediction_rows": str(product_status.get("valid_prediction_rows", "")),
            "valid_bound_rows": str(product_status.get("valid_bound_rows", "")),
            "comparison_rows": str(product_status.get("comparison_rows", "")),
            "passed_rows": str(product_status.get("passed_rows", "")),
            "claim_allowed": str(product_status.get("claim_allowed", "")).lower(),
            "expected_result": "reject missing MTS coefficient map and official readout",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def claim_gate_rows(product_status: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "gate_id": "CG1083_0_source_vector",
            "claim_component": "physical R_source^Earth",
            "gate_pass": "false",
            "claim_allowed": "false",
            "reason": "candidate is bulk-composition DD vector, not shell/profile/worldtube weighted",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1083_1_parent_to_DD_map",
            "claim_component": "MTS parent-to-DD coefficient map",
            "gate_pass": "false",
            "claim_allowed": "false",
            "reason": "PTD1082_4_verdict=PARENT_TO_DD_MAP_NOT_DERIVED",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1083_2_official_readout",
            "claim_component": "K_MICROSCOPE readout",
            "gate_pass": "false",
            "claim_allowed": "false",
            "reason": "official arrays/masks/timing not imported",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1083_3_common_mode",
            "claim_component": "source common-mode cancellation",
            "gate_pass": "false",
            "claim_allowed": "false",
            "reason": "CMA1083_2_verdict=SOURCE_COMMON_MODE_NOT_SIGNED",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1083_4_product_runner",
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
            "decision_id": "DECISION1083_0",
            "decision": "DD Earth source vector first row is numeric but nonclaim",
            "because": "bulk composition can be transformed into the external DD alpha/surface basis, but profile/readout/parent maps are missing",
            "next_action": "do not treat this as an MTS WEP prediction",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DECISION1083_1",
            "decision": "explicit source-vector route remains open",
            "because": "common-mode theorem is not signed and measured-G absorption is forbidden",
            "next_action": "refine source profile weighting or import MICROSCOPE readout arrays before trying a physical product",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_id": "NEXT1083_0_1084",
            "next_target": "1084-Y5-R10-DD-source-profile-weighting-or-MICROSCOPE-readout-import-gate.md",
            "objective": "choose whether to refine the DD Earth source vector with shell/profile/worldtube weighting or begin the official MICROSCOPE readout import gate; keep parent-to-DD map blocked and no MTS claim",
            "include": "Earth shell/profile targets; candidate weighting kernels; CMSM/readout array requirements; product convention; strict claim gates",
            "exclude": "unit source proxy as physical source; measured-G absorption; DD smoke as MTS claim; GitHub; formalization edits",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def csv_outputs_parse(paths: list[Path]) -> bool:
    try:
        for path in paths:
            with path.open(newline="", encoding="utf-8") as handle:
                list(csv.DictReader(handle))
        return True
    except csv.Error:
        return False


def validate_outputs(
    outputs: dict[str, Path],
    source_rows: list[dict[str, str]],
    web_rows: list[dict[str, str]],
    composition_rows: list[dict[str, str]],
    formula_rows: list[dict[str, str]],
    charge_rows: list[dict[str, str]],
    source_vector_rows_: list[dict[str, str]],
    product_rows_: list[dict[str, str]],
    caveat_rows: list[dict[str, str]],
    common_rows: list[dict[str, str]],
    prediction_rows_: list[dict[str, str]],
    bound_rows_: list[dict[str, str]],
    product_status: dict[str, Any],
    claim_rows: list[dict[str, str]],
    next_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    checks: list[tuple[str, bool, str]] = []
    values = earth_source_vector_values()
    checks.append(("V1083_0_local_sources_exist", all(row["exists"] == "true" and row["needle_found"] == "true" for row in source_rows), "all cited local source paths and needles are present"))
    checks.append(("V1083_1_web_sources_recorded", len(web_rows) == 4 and all(row["source_url"].startswith("https://") and row["valid_for_claim"] == "false" for row in web_rows), "web source urls/provenance are recorded as nonclaim"))
    checks.append(("V1083_2_composition_target_numeric", len(composition_rows) == len(ELEMENTS) and abs(values["composition_sum_wt_percent"] - 99.86) < 1e-9 and abs(values["normalized_mass_fraction_sum"] - 1.0) < 1e-12, "bulk Earth composition target rows are numeric and normalized"))
    checks.append(("V1083_3_DD_formulas_present", {row["component"] for row in formula_rows} == {"Q_alpha_Coulomb", "Q_surface_binding"}, "DD alpha/surface formulas are present"))
    checks.append(("V1083_4_element_charges_numeric", len(charge_rows) == len(ELEMENTS) and all(parse_float(row["Q_alpha_Coulomb"]) is not None and parse_float(row["Q_surface_binding"]) is not None for row in charge_rows), "per-element DD charges are numeric"))
    checks.append(("V1083_5_source_vector_numeric_nonclaim", any(row["source_vector_id"] == "DD_EARTH1083_0_bulk_weighted" and parse_float(row["Q_alpha_Coulomb_Earth"]) is not None and parse_float(row["Q_surface_binding_Earth"]) is not None and row["valid_for_claim"] == "false" for row in source_vector_rows_), "Earth DD source vector first row is numeric but nonclaim"))
    checks.append(("V1083_6_products_numeric_nonclaim", len(product_rows_) == 3 and all(parse_float(row["product_abs"]) is not None and parse_float(row["product_abs"]) > 0 and row["valid_for_claim"] == "false" for row in product_rows_), "source-material products are numeric and nonclaim"))
    checks.append(("V1083_7_caveats_block_claim", len(caveat_rows) == 4 and all(row["gate_pass"] == "false" for row in caveat_rows), "profile/readout/parent/no-absorption caveats block claims"))
    checks.append(("V1083_8_common_mode_unsigned", any(row["route_id"] == "CMA1083_2_verdict" and row["status"] == "SOURCE_COMMON_MODE_NOT_SIGNED" for row in common_rows), "common-mode alternative remains unsigned"))
    checks.append(("V1083_9_prediction_missing_nonclaim", any("MISSING_MTS_COEFFICIENT_MAP" in row["product_value"] and row["valid_for_claim"] == "false" for row in prediction_rows_), "generic prediction row remains missing parent/readout inputs"))
    checks.append(("V1083_10_bound_numeric", bool(bound_rows_) and parse_float(bound_rows_[0]["bound_value"]) is not None and float(bound_rows_[0]["bound_value"]) > 0 and bound_rows_[0]["valid_for_claim"] == "true", "MICROSCOPE bound import is positive numeric"))
    checks.append(("V1083_11_product_runner_refuses", product_status.get("valid_prediction_rows") == 0 and product_status.get("claim_allowed") is False, "generic product runner reports no valid prediction rows and claim false"))
    checks.append(("V1083_12_claim_gates_safe", claim_rows and all(row["claim_allowed"] == "false" for row in claim_rows), "all claim gates deny WEP/local-GR claim"))
    checks.append(("V1083_13_next_target", any(row["next_target"].startswith("1084-Y5-R10-DD-source-profile") for row in next_rows), "1084 handoff written"))
    generated_paths = list(outputs.values()) + [DOC]
    checks.append(("V1083_14_generated_under_post_checkpoint", all(str(path.resolve()).startswith(str(ROOT.resolve())) for path in generated_paths), "all generated outputs are under post-checkpoint-work"))
    prevalidation_csv_paths = [path for key, path in outputs.items() if key != "validation"]
    checks.append(("V1083_15_csv_parse", csv_outputs_parse(prevalidation_csv_paths), "all 1083 CSV outputs parse cleanly"))
    checks.append(("V1083_16_formalization_untouched", count_formalization_modified_since_start() == 0, "formalization-workbench modified-file count remains zero"))
    checks.append(("V1083_SUMMARY", True, "DD Earth source vector first row built as numeric nonclaim; parent-to-DD/readout/profile gates remain closed"))
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
    web_rows: list[dict[str, str]],
    composition_rows: list[dict[str, str]],
    formula_rows: list[dict[str, str]],
    charge_rows: list[dict[str, str]],
    source_vector_rows_: list[dict[str, str]],
    product_rows_: list[dict[str, str]],
    caveat_rows: list[dict[str, str]],
    common_rows: list[dict[str, str]],
    product_status_rows_: list[dict[str, str]],
    product_comparisons: list[dict[str, Any]],
    claim_rows: list[dict[str, str]],
    decisions: list[dict[str, str]],
    validation_rows: list[dict[str, str]],
    next_rows: list[dict[str, str]],
) -> None:
    text = "\n".join(
        [
            "# 1083-Y5-R10 DD Earth source vector extraction plan and nonclaim first row",
            "",
            "## Current verdict",
            "1083 builds the first numeric DD-basis Earth source-vector candidate from a bulk-Earth composition table target and the existing alpha/surface smoke convention. This is useful plumbing, not a claim: the row is bulk-weighted rather than shell/profile/worldtube weighted, the parent-to-DD coefficient map is still unsigned, the official MICROSCOPE readout arrays are still missing, and the common-mode shortcut is not proven.",
            "",
            "## Local source register",
            md_table(source_rows, ["source_id", "relative_path", "exists", "needle_found", "note"]),
            "## Web source register",
            md_table(web_rows, ["web_source_id", "role", "source_url", "extraction_method", "confidence_level"]),
            "## Bulk Earth composition target",
            md_table(composition_rows, ["element", "wt_percent", "normalized_mass_fraction", "Z", "A", "extraction_status"]),
            "## DD charge formula ledger",
            md_table(formula_rows, ["formula_id", "component", "formula", "status", "claim_blocker"]),
            "## DD Earth element charges",
            md_table(charge_rows, ["charge_id", "element", "weighted_Q_alpha_Coulomb", "weighted_Q_surface_binding", "status"]),
            "## DD Earth source vector first row",
            md_table(source_vector_rows_, ["source_vector_id", "basis", "Q_alpha_Coulomb_Earth", "Q_surface_binding_Earth", "status", "claim_blocker"]),
            "## DD source-material product nonclaim",
            md_table(product_rows_, ["product_id", "component", "source_material_product", "product_abs", "eta_bound", "status"]),
            "## Source vector caveat gate",
            md_table(caveat_rows, ["gate_id", "claim_component", "gate_pass", "status", "reason"]),
            "## Common-mode alternative",
            md_table(common_rows, ["route_id", "claim", "status", "gap"]),
            "## Product runner status",
            md_table(product_status_rows_, ["runner_id", "valid_prediction_rows", "valid_bound_rows", "comparison_rows", "claim_allowed", "expected_result"]),
            "## Product comparison rows",
            md_table(product_comparisons, ["comparison_id", "arena", "product_symbol", "product_value", "bound_value", "comparison_status", "pass_for_claim", "issues"]),
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
    web_rows = web_source_register_rows()
    composition_rows = bulk_earth_composition_target_rows()
    formula_rows = dd_charge_formula_rows()
    charge_rows = dd_earth_element_charge_rows()
    values = earth_source_vector_values()
    source_vector_rows_ = earth_source_vector_rows(values)
    product_rows_ = source_material_product_rows(values)
    caveat_rows = source_vector_caveat_gate_rows()
    common_rows = common_mode_alternative_rows()
    prediction_rows_ = prediction_rows()
    bound_rows_ = bound_import_rows()
    next_rows = next_target_rows()

    outputs = {
        "source_register": OUT / "P8_Y5_R10_1083_SOURCE_REGISTER.csv",
        "web_source_register": OUT / "P8_Y5_R10_1083_WEB_SOURCE_REGISTER.csv",
        "composition_target": OUT / "P8_Y5_R10_1083_BULK_EARTH_COMPOSITION_TARGET.csv",
        "formula_ledger": OUT / "P8_Y5_R10_1083_DD_CHARGE_FORMULA_LEDGER.csv",
        "element_charges": OUT / "P8_Y5_R10_1083_DD_EARTH_ELEMENT_CHARGES.csv",
        "source_vector": OUT / "P8_Y5_R10_1083_DD_EARTH_SOURCE_VECTOR_FIRST_ROW_NONCLAIM.csv",
        "source_material_product": OUT / "P8_Y5_R10_1083_DD_SOURCE_MATERIAL_PRODUCT_NONCLAIM.csv",
        "caveat_gate": OUT / "P8_Y5_R10_1083_SOURCE_VECTOR_CAVEAT_GATE.csv",
        "common_mode": OUT / "P8_Y5_R10_1083_COMMON_MODE_ALTERNATIVE.csv",
        "prediction": PREDICTION_TEMPLATE,
        "bound": BOUND_IMPORT,
        "product_status": OUT / "P8_Y5_R10_1083_PRODUCT_RUNNER_STATUS.csv",
        "product_comparison": OUT / "P8_Y5_R10_1083_PRODUCT_COMPARISON_ROWS.csv",
        "claim_gates": OUT / "P8_Y5_R10_1083_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_R10_1083_DECISION_LEDGER.csv",
        "next_target": OUT / "P8_Y5_R10_1083_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_1083_VALIDATION.csv",
    }

    write_csv(outputs["source_register"], source_rows)
    write_csv(outputs["web_source_register"], web_rows)
    write_csv(outputs["composition_target"], composition_rows)
    write_csv(outputs["formula_ledger"], formula_rows)
    write_csv(outputs["element_charges"], charge_rows)
    write_csv(outputs["source_vector"], source_vector_rows_)
    write_csv(outputs["source_material_product"], product_rows_)
    write_csv(outputs["caveat_gate"], caveat_rows)
    write_csv(outputs["common_mode"], common_rows)
    write_csv(outputs["prediction"], prediction_rows_, PRODUCT_REQUIRED_COLUMNS)
    write_csv(outputs["bound"], bound_rows_, BOUND_REQUIRED_COLUMNS)

    product_result = run_product_runner(PREDICTION_TEMPLATE, BOUND_IMPORT, PRODUCT_RUN_DIR)
    product_status = product_result["status"]
    product_status_rows_ = product_status_rows(product_status)
    product_comparisons = product_result["comparisons"]
    claim_rows = claim_gate_rows(product_status)
    decisions = decision_rows()

    write_csv(outputs["product_status"], product_status_rows_)
    write_csv(outputs["product_comparison"], product_comparisons)
    write_csv(outputs["claim_gates"], claim_rows)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["next_target"], next_rows)

    validation_rows = validate_outputs(
        outputs,
        source_rows,
        web_rows,
        composition_rows,
        formula_rows,
        charge_rows,
        source_vector_rows_,
        product_rows_,
        caveat_rows,
        common_rows,
        prediction_rows_,
        bound_rows_,
        product_status,
        claim_rows,
        next_rows,
    )
    write_csv(outputs["validation"], validation_rows)
    write_doc(
        source_rows,
        web_rows,
        composition_rows,
        formula_rows,
        charge_rows,
        source_vector_rows_,
        product_rows_,
        caveat_rows,
        common_rows,
        product_status_rows_,
        product_comparisons,
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
