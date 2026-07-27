from __future__ import annotations

import csv
import math
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


RUN_STARTED_UTC = datetime.now(timezone.utc)
ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
WORK = ROOT / "post-checkpoint-work"
MTS = WORK / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = WORK / "source-intake" / "local_bounds"
RAB_QUEUE = WORK / "source-intake" / "rab-sector" / "acquisition-queue"
BETA_DOCS = WORK / "source-intake" / "beta-source" / "docs"
MICROSCOPE_DIR = WORK / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
SCRIPTS = WORK / "scripts"
FORMALIZATION = ROOT / "formalization-workbench"
DOC = WORK / "2789-Y5-R2FR-DD-Earth-source-vector-extraction-plan-and-nonclaim-first-row-under-AX1090.md"

OUTPUTS = {
    "sources": MTS / "P8_Y5_R2FR_2789_SOURCE_REGISTER.csv",
    "web_sources": MTS / "P8_Y5_R2FR_2789_WEB_SOURCE_REGISTER.csv",
    "bulk_earth": MTS / "P8_Y5_R2FR_2789_BULK_EARTH_COMPOSITION_TARGET.csv",
    "formulas": MTS / "P8_Y5_R2FR_2789_DD_CHARGE_FORMULA_LEDGER.csv",
    "element_charges": MTS / "P8_Y5_R2FR_2789_DD_EARTH_ELEMENT_CHARGES.csv",
    "source_vector": MTS / "P8_Y5_R2FR_2789_DD_EARTH_SOURCE_VECTOR_FIRST_ROW_NONCLAIM.csv",
    "source_material_product": MTS / "P8_Y5_R2FR_2789_DD_SOURCE_MATERIAL_PRODUCT_NONCLAIM.csv",
    "caveat_gates": MTS / "P8_Y5_R2FR_2789_SOURCE_VECTOR_CAVEAT_GATE.csv",
    "common_mode": MTS / "P8_Y5_R2FR_2789_COMMON_MODE_ALTERNATIVE.csv",
    "candidate": MTS / "P8_Y5_R2FR_2789_WEP_PRODUCT_CANDIDATE_NONCLAIM.csv",
    "bounds": MTS / "P8_Y5_R2FR_2789_WEP_BOUND_IMPORT.csv",
    "runner": MTS / "P8_Y5_R2FR_2789_PRODUCT_RUNNER_STATUS.csv",
    "comparisons": MTS / "P8_Y5_R2FR_2789_PRODUCT_COMPARISON_ROWS.csv",
    "gates": MTS / "P8_Y5_R2FR_2789_CLAIM_GATES.csv",
    "decision": MTS / "P8_Y5_R2FR_2789_DECISION_LEDGER.csv",
    "next": MTS / "P8_Y5_R2FR_2789_NEXT_TARGET.csv",
    "branches": MTS / "P8_Y5_R2FR_2789_BRANCH_COPIES.csv",
    "validation": MTS / "P8_Y5_BRR545_2789_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "composition_queue": RAB_QUEUE / "JR2789_BULK_EARTH_COMPOSITION_TARGET_NONCLAIM.csv",
    "source_vector_queue": RAB_QUEUE / "JR2789_DD_EARTH_SOURCE_VECTOR_NONCLAIM.csv",
    "product_queue": RAB_QUEUE / "JR2789_DD_SOURCE_MATERIAL_PRODUCT_NONCLAIM.csv",
    "beta_doc": BETA_DOCS / "DD_EARTH_SOURCE_VECTOR_2789_NONCLAIM.csv",
    "microscope_copy": MICROSCOPE_DIR / "microscope_dd_earth_source_vector_2789_nonclaim.csv",
    "next_queue": RAB_QUEUE / "JR2789_SOURCE_PROFILE_OR_READOUT_NEXT.csv",
}


EARTH_COMPOSITION = [
    ("Fe", 32.0, 26, 55.845),
    ("O", 29.7, 8, 15.999),
    ("Si", 16.1, 14, 28.085),
    ("Mg", 15.4, 12, 24.305),
    ("Ni", 1.82, 28, 58.693),
    ("Ca", 1.71, 20, 40.078),
    ("Al", 1.59, 13, 26.982),
    ("S", 0.64, 16, 32.06),
    ("Cr", 0.47, 24, 51.996),
    ("Na", 0.18, 11, 22.99),
    ("P", 0.07, 15, 30.974),
    ("Mn", 0.08, 25, 54.938),
    ("C", 0.07, 6, 12.011),
    ("H", 0.03, 1, 1.008),
]


def ts() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dirs() -> None:
    for path in {p.parent for p in OUTPUTS.values()} | {p.parent for p in BRANCH_OUTPUTS.values()} | {DOC.parent}:
        path.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except FileNotFoundError:
        return ""


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def find_row(path: Path, key: str, value: str) -> dict[str, str]:
    for row in read_csv_rows(path):
        if row.get(key) == value:
            return row
    return {}


def nonclaim(row: dict[str, Any]) -> dict[str, Any]:
    row["valid_for_claim"] = False
    return row


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def csv_parses(path: Path) -> bool:
    if not path.exists():
        return False
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def csv_row_count(path: Path) -> int:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return sum(1 for _ in csv.DictReader(handle))


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        cells = [str(row.get(column, "")).replace("\n", " ").replace("|", "\\|") for column in columns]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def is_numeric(value: Any) -> bool:
    try:
        float(str(value))
    except (TypeError, ValueError):
        return False
    return True


def trueish(value: Any) -> bool:
    return str(value).strip().lower() == "true"


def has_missing_marker(row: dict[str, Any]) -> bool:
    return "MISSING" in " ".join(str(value) for value in row.values()).upper()


def source_row(row_id: str, source_key: str, path: Path, needle: str, role: str) -> dict[str, Any]:
    text = read_text(path)
    exists = path.exists()
    return nonclaim({
        "row_id": row_id,
        "source_key": source_key,
        "source_path": str(path),
        "exists": exists,
        "needle": needle,
        "needle_found": exists and needle in text,
        "source_role": role,
    })


def get_local_bound(row_id: str) -> dict[str, str]:
    for row in read_csv_rows(LOCAL_BOUNDS / "local_bound_claims.csv"):
        if row.get("row_id") == row_id:
            return row
    return {}


def safe_float(value: Any, fallback: float = 0.0) -> float:
    try:
        return float(str(value))
    except (TypeError, ValueError):
        return fallback


def q_alpha(z: float, a: float) -> float:
    return 7.7e-4 * z * (z - 1.0) / (a ** (4.0 / 3.0))


def q_surface(z: float, a: float) -> float:
    return -0.036 / (a ** (1.0 / 3.0)) - 1.4e-4 * z * (z - 1.0) / (a ** (4.0 / 3.0))


def build_sources() -> list[dict[str, Any]]:
    specs = [
        ("SRC2789_00_2788_next", "2788_next", MTS / "P8_Y5_R2FR_2788_NEXT_TARGET.csv", "NEXT2788_0_2789", "current handoff into DD Earth-source vector extraction"),
        ("SRC2789_01_2788_validation", "2788_validation", MTS / "P8_Y5_BRR545_2788_VALIDATION.csv", "VAL2788_OVERALL", "2788 validation baseline"),
        ("SRC2789_02_2788_earth_fill", "2788_earth_fill", MTS / "P8_Y5_R2FR_2788_PHYSICAL_EARTH_SOURCE_FILL_ROWS.csv", "ESF2788_1_vectorization", "Earth/source vector still not vectorized"),
        ("SRC2789_03_2788_chain_rule", "2788_chain_rule", MTS / "P8_Y5_R2FR_2788_DD_CHAIN_RULE_MAP_CONTRACT.csv", "DCR2788_4_product_projection", "DD product projection contract"),
        ("SRC2789_04_2788_dd_reuse", "2788_dd_reuse", MTS / "P8_Y5_R2FR_2788_DD_SMOKE_REUSE_ROWS.csv", "REUSE2788_0_alpha", "DD material smoke reuse rows"),
        ("SRC2789_05_1083_web", "1083_web", MTS / "P8_Y5_R10_1083_WEB_SOURCE_REGISTER.csv", "WEB1083_0_MCDONOUGH_2003_TABLE5", "R10 web/source register precedent"),
        ("SRC2789_06_1083_bulk", "1083_bulk", MTS / "P8_Y5_R10_1083_BULK_EARTH_COMPOSITION_TARGET.csv", "Fe", "R10 bulk Earth composition candidate rows"),
        ("SRC2789_07_1083_formulas", "1083_formulas", MTS / "P8_Y5_R10_1083_DD_CHARGE_FORMULA_LEDGER.csv", "DDF1083_0_alpha_Coulomb", "R10 DD charge formula ledger"),
        ("SRC2789_08_1083_first_vector", "1083_first_vector", MTS / "P8_Y5_R10_1083_DD_EARTH_SOURCE_VECTOR_FIRST_ROW_NONCLAIM.csv", "DD_EARTH1083_0_bulk_weighted", "R10 first DD Earth-source vector"),
        ("SRC2789_09_1083_product", "1083_product", MTS / "P8_Y5_R10_1083_DD_SOURCE_MATERIAL_PRODUCT_NONCLAIM.csv", "DD_PRODUCT1083_0_alpha", "R10 source-material product precedent"),
        ("SRC2789_10_1083_common_mode", "1083_common_mode", MTS / "P8_Y5_R10_1083_COMMON_MODE_ALTERNATIVE.csv", "CMA1083_2_verdict", "R10 common-mode alternative"),
        ("SRC2789_11_1083_next", "1083_next", MTS / "P8_Y5_R10_1083_NEXT_TARGET.csv", "NEXT1083_0_1084", "R10 next target after first source vector"),
        ("SRC2789_12_1084_next", "1084_next", MTS / "P8_Y5_R10_1084_NEXT_TARGET.csv", "NEXT1084_0_1085", "R10 source-profile/range/readout route"),
        ("SRC2789_13_local_bounds", "local_bounds", LOCAL_BOUNDS / "local_bound_claims.csv", "R1_WEP_source_charge", "MICROSCOPE WEP bound row"),
    ]
    return [source_row(*spec) for spec in specs]


def build_web_sources() -> list[dict[str, Any]]:
    generated = ts()
    return [
        nonclaim({
            "web_source_id": "WEB2789_0_MCDONOUGH_2003_TABLE5",
            "role": "bulk Earth composition table target",
            "source_url": "https://www.mso.anu.edu.au/PSI/PSI_Meetings/Entries/2007/6/13_The_bulk_composition_of_the_Earth_%281%29_files/Treatise%20on%20Geochemistry%202003%20McDonough.pdf",
            "source_title": "Compositional Model for the Earth's Core",
            "evidence_used": "Table 5 bulk Earth wt.% abundant-element rows plus text stating the table compares bulk Earth, silicate Earth, and core by weight percent and atomic proportion",
            "extraction_method": "manual table-target transcription into candidate rows; not a machine-readable official table import",
            "confidence_level": "medium_for_nonclaim_source_vector; insufficient_for_claim",
            "generated_utc": generated,
        }),
        nonclaim({
            "web_source_id": "WEB2789_1_MCDONOUGH_SUN_1995",
            "role": "composition provenance continuity",
            "source_url": "https://earthref.org/ERR/n%3A3%2Cb%3Aaaaa0000003tab05/",
            "source_title": "McDonough and Sun 1995, Composition of the Earth",
            "evidence_used": "older bulk-Earth/silicate-Earth composition reference already registered in 2786/1080",
            "extraction_method": "provenance link only; no new numeric extraction from this page",
            "confidence_level": "source-continuity-only",
            "generated_utc": generated,
        }),
        nonclaim({
            "web_source_id": "WEB2789_2_DAMOUR_DONOGHUE_2010",
            "role": "external DD alpha/surface charge basis",
            "source_url": "https://arxiv.org/abs/1007.2792",
            "source_title": "Equivalence Principle Violations and Couplings of a Light Dilaton",
            "evidence_used": "two dominant composition-charge style used by the existing 1053/1081/2787 smoke matrix",
            "extraction_method": "reuse existing local smoke convention rather than promote the external basis to MTS",
            "confidence_level": "good_for_external_comparator; not_MTS_derived",
            "generated_utc": generated,
        }),
        nonclaim({
            "web_source_id": "WEB2789_3_MICROSCOPE_FINAL",
            "role": "WEP bound source",
            "source_url": "https://arxiv.org/abs/2209.15487",
            "source_title": "MICROSCOPE mission: final results of the test of the Equivalence Principle",
            "evidence_used": "eta(Ti,Pt) final-result bound inherited from local_bound_claims.csv",
            "extraction_method": "bound import only; official readout arrays still not imported",
            "confidence_level": "bound_source_backed; prediction_nonclaim",
            "generated_utc": generated,
        }),
    ]


def build_bulk_earth_rows() -> list[dict[str, Any]]:
    generated = ts()
    wt_total = sum(row[1] for row in EARTH_COMPOSITION)
    return [
        nonclaim({
            "element": element,
            "wt_percent": f"{wt_percent:g}",
            "normalized_mass_fraction": f"{wt_percent / wt_total:.15e}",
            "Z": z,
            "A": a,
            "source_table": "WEB2789_0_MCDONOUGH_2003_TABLE5",
            "extraction_status": "TABLE_TARGET_CANDIDATE_NONCLAIM",
            "generated_utc": generated,
        })
        for element, wt_percent, z, a in EARTH_COMPOSITION
    ]


def build_formula_rows() -> list[dict[str, Any]]:
    generated = ts()
    return [
        nonclaim({
            "formula_id": "DDF2789_0_alpha_Coulomb",
            "component": "Q_alpha_Coulomb",
            "formula": "7.7e-4 * Z*(Z-1) / A^(4/3)",
            "basis_source": "WEB2789_2_DAMOUR_DONOGHUE_2010; local WCM1053/2787 convention",
            "status": "IMPORTED_FROM_EXISTING_SMOKE_CONVENTION_NONCLAIM",
            "claim_blocker": "not derived from MTS parent action",
            "generated_utc": generated,
        }),
        nonclaim({
            "formula_id": "DDF2789_1_surface_binding",
            "component": "Q_surface_binding",
            "formula": "-0.036 / A^(1/3) - 1.4e-4 * Z*(Z-1) / A^(4/3)",
            "basis_source": "WEB2789_2_DAMOUR_DONOGHUE_2010; local WCM1053/2787 convention",
            "status": "IMPORTED_FROM_EXISTING_SMOKE_CONVENTION_NONCLAIM",
            "claim_blocker": "not derived from MTS parent action",
            "generated_utc": generated,
        }),
    ]


def build_element_charge_rows(bulk_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    generated = ts()
    rows = []
    for row in bulk_rows:
        element = row["element"]
        mass_fraction = safe_float(row["normalized_mass_fraction"])
        z = safe_float(row["Z"])
        a = safe_float(row["A"])
        alpha = q_alpha(z, a)
        surface = q_surface(z, a)
        rows.append(nonclaim({
            "charge_id": f"DEC2789_{element}",
            "element": element,
            "normalized_mass_fraction": f"{mass_fraction:.15e}",
            "Z": row["Z"],
            "A": row["A"],
            "Q_alpha_Coulomb": f"{alpha:.15e}",
            "Q_surface_binding": f"{surface:.15e}",
            "weighted_Q_alpha_Coulomb": f"{mass_fraction * alpha:.15e}",
            "weighted_Q_surface_binding": f"{mass_fraction * surface:.15e}",
            "status": "NUMERIC_ELEMENT_DD_CHARGE_NONCLAIM",
            "generated_utc": generated,
        }))
    return rows


def build_source_vector_rows(element_charge_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    generated = ts()
    q_alpha_earth = sum(safe_float(row["weighted_Q_alpha_Coulomb"]) for row in element_charge_rows)
    q_surface_earth = sum(safe_float(row["weighted_Q_surface_binding"]) for row in element_charge_rows)
    composition_sum = sum(row[1] for row in EARTH_COMPOSITION)
    normalized_sum = sum(safe_float(row["normalized_mass_fraction"]) for row in element_charge_rows)
    return [
        nonclaim({
            "source_vector_id": "DD_EARTH2789_0_bulk_weighted",
            "source_body": "Earth",
            "basis": "DD_Q_alpha_Coulomb_Q_surface_binding",
            "Q_alpha_Coulomb_Earth": f"{q_alpha_earth:.15e}",
            "Q_surface_binding_Earth": f"{q_surface_earth:.15e}",
            "composition_sum_wt_percent": f"{composition_sum:g}",
            "normalized_mass_fraction_sum": f"{normalized_sum:.15e}",
            "source_rows": "P8_Y5_R2FR_2789_BULK_EARTH_COMPOSITION_TARGET.csv; P8_Y5_R2FR_2789_DD_EARTH_ELEMENT_CHARGES.csv",
            "status": "NUMERIC_BULK_EARTH_DD_SOURCE_VECTOR_NONCLAIM",
            "claim_blocker": "bulk Earth source is not shell/profile/worldtube weighted and parent-to-DD/readout maps remain missing",
            "generated_utc": generated,
        })
    ]


def build_source_material_product_rows(source_vector_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    generated = ts()
    bound = get_local_bound("R1_WEP_source_charge")
    eta_bound = safe_float(bound.get("upper_bound"), 2.8e-15)
    source_alpha = safe_float(source_vector_rows[0]["Q_alpha_Coulomb_Earth"])
    source_surface = safe_float(source_vector_rows[0]["Q_surface_binding_Earth"])
    alpha_delta = safe_float(find_row(MTS / "P8_Y5_R2FR_2787_DD_MATERIAL_DELTA_IMPORT.csv", "delta_id", "DDM2787_0_delta_alpha").get("delta_abs"), 0.001989808886825)
    surface_delta = safe_float(find_row(MTS / "P8_Y5_R2FR_2787_DD_MATERIAL_DELTA_IMPORT.csv", "delta_id", "DDM2787_1_delta_surface").get("delta_abs"), 0.003306456347405)
    alpha_product = source_alpha * alpha_delta
    surface_product = source_surface * surface_delta
    combined_abs = abs(alpha_product) + abs(surface_product)
    return [
        nonclaim({
            "product_id": "DD_PRODUCT2789_0_alpha",
            "component": "Q_alpha_Coulomb",
            "source_value": f"{source_alpha:.15e}",
            "material_delta_abs": f"{alpha_delta:.15e}",
            "source_material_product": f"{alpha_product:.15e}",
            "product_abs": f"{abs(alpha_product):.15e}",
            "eta_bound": f"{eta_bound:.15e}",
            "required_abs_coefficient_max_if_single_component": f"{eta_bound / abs(alpha_product):.15e}",
            "status": "NUMERIC_DD_SOURCE_MATERIAL_PRODUCT_NONCLAIM",
            "generated_utc": generated,
        }),
        nonclaim({
            "product_id": "DD_PRODUCT2789_1_surface",
            "component": "Q_surface_binding",
            "source_value": f"{source_surface:.15e}",
            "material_delta_abs": f"{surface_delta:.15e}",
            "source_material_product": f"{surface_product:.15e}",
            "product_abs": f"{abs(surface_product):.15e}",
            "eta_bound": f"{eta_bound:.15e}",
            "required_abs_coefficient_max_if_single_component": f"{eta_bound / abs(surface_product):.15e}",
            "status": "NUMERIC_DD_SOURCE_MATERIAL_PRODUCT_NONCLAIM",
            "generated_utc": generated,
        }),
        nonclaim({
            "product_id": "DD_PRODUCT2789_2_combined_abs",
            "component": "Q_alpha_Coulomb + Q_surface_binding",
            "source_value": "bulk Earth DD two-component vector",
            "material_delta_abs": "TA6V_minus_PtRh10 DD two-component abs deltas",
            "source_material_product": f"{alpha_product + surface_product:.15e}",
            "product_abs": f"{combined_abs:.15e}",
            "eta_bound": f"{eta_bound:.15e}",
            "required_abs_coefficient_max_if_equal_component": f"{eta_bound / combined_abs:.15e}",
            "status": "NUMERIC_DD_SOURCE_MATERIAL_PRODUCT_NONCLAIM",
            "generated_utc": generated,
        }),
    ]


def build_caveat_gate_rows() -> list[dict[str, Any]]:
    generated = ts()
    specs = [
        ("SCG2789_0_profile_weighting", "Earth source profile/worldtube weighting", False, "MISSING_SOURCE_PROFILE_WEIGHTING", "bulk composition is not the same object as the orbit- and shell-weighted source vector seen by MICROSCOPE"),
        ("SCG2789_1_parent_to_DD_map", "C_parent -> DD coefficient map", False, "MISSING_PARENT_OPERATOR_BASIS_MAP", "alpha/surface DD basis remains external comparator not an MTS-derived basis"),
        ("SCG2789_2_official_readout", "K_MICROSCOPE official readout", False, "OFFICIAL_ARRAYS_NOT_IMPORTED", "gx/gz/Sxx/Sxz/masks/timing arrays or validated export are not yet in the product convention"),
        ("SCG2789_3_no_measured_G_absorption", "source response treatment", False, "NO_ABSORPTION_SHORTCUT_ALLOWED", "measured-G absorption would hide the finite WEP branch instead of deriving or bounding it"),
    ]
    return [
        nonclaim({
            "gate_id": gate_id,
            "claim_component": component,
            "gate_pass": gate_pass,
            "status": status,
            "reason": reason,
            "generated_utc": generated,
        })
        for gate_id, component, gate_pass, status, reason in specs
    ]


def build_common_mode_rows() -> list[dict[str, Any]]:
    generated = ts()
    specs = [
        ("CMA2789_0_theorem_target", "Earth source vector cancels as a universal common mode", "source-side coupling is species-blind and appears only as a common acceleration scale before differential readout", "THEOREM_TARGET_DEFINED", "must be proven before replacing the explicit source vector"),
        ("CMA2789_1_counterpressure", "source vector may be ignored", "no source-composition dependent residual and no measured-G absorption", "NOT_SIGNED", "finite WEP products generally contain source x test-material response unless parent action kills the source leg"),
        ("CMA2789_2_verdict", "common-mode route closes 2789", "parent-signed common-mode theorem", "SOURCE_COMMON_MODE_NOT_SIGNED", "retain explicit source-vector acquisition route"),
    ]
    return [
        nonclaim({
            "route_id": route_id,
            "claim": claim,
            "needed_parent_clause": needed,
            "status": status,
            "gap": gap,
            "generated_utc": generated,
        })
        for route_id, claim, needed, status, gap in specs
    ]


def build_candidate_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({
            "prediction_id": "PRED2789_0_DD_bulk_Earth_source_not_MTS_product",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "P_WEP_relative_source_weight",
            "product_value": "MISSING_PARENT_TO_DD_MAP_OR_PROFILE_READOUT_NORMALIZATION",
            "product_units": "dimensionless",
            "product_source": "source-intake/mts_residuals/P8_Y5_R2FR_2789_DD_SOURCE_MATERIAL_PRODUCT_NONCLAIM.csv",
            "inputs_present": "bulk Earth DD source vector; DD material deltas; MICROSCOPE bound",
            "required_inputs": "parent-to-DD coefficient map; shell/profile/worldtube weighting or common-mode theorem; official/validated readout",
            "derivation_status": "BULK_EARTH_DD_SOURCE_NUMERIC_BUT_MTS_PRODUCT_MISSING",
            "notes": "generic product runner must refuse because this is still an external DD source scaffold",
        })
    ]


def build_bound_rows() -> list[dict[str, Any]]:
    bound = get_local_bound("R1_WEP_source_charge")
    return [
        nonclaim({
            "bound_id": "BOUND2789_0_MICROSCOPE_WEP_source_charge",
            "arena": "MICROSCOPE_WEP",
            "observable": "eta_WEP_source_charge",
            "upper_bound": bound.get("upper_bound", "2.8e-15"),
            "units": bound.get("units", "dimensionless"),
            "source_path_or_url": bound.get("reference_path_or_url", "https://arxiv.org/abs/2209.15487; doi:10.1103/PhysRevLett.129.121102"),
            "source_row": "source-intake/local_bounds/local_bound_claims.csv:R1_WEP_source_charge",
            "valid_bound_row": True,
        })
    ]


def build_runner_rows(candidate_rows: list[dict[str, Any]], bound_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    valid_prediction_rows = [
        row for row in candidate_rows
        if trueish(row.get("valid_for_claim")) and is_numeric(row.get("product_value")) and not has_missing_marker(row)
    ]
    valid_bound_rows = [
        row for row in bound_rows
        if trueish(row.get("valid_bound_row")) and is_numeric(row.get("upper_bound")) and float(row.get("upper_bound", 0)) > 0
    ]
    return [
        nonclaim({
            "runner_id": "APR2789_0_DD_bulk_Earth_source_product_stub",
            "prediction_rows": len(candidate_rows),
            "bound_rows": len(bound_rows),
            "valid_prediction_rows": len(valid_prediction_rows),
            "valid_bound_rows": len(valid_bound_rows),
            "comparison_rows": 1,
            "passed_rows": 0,
            "claim_allowed": False,
            "expected_result": "reject DD bulk Earth source row as MTS product",
        })
    ]


def build_comparison_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({
            "comparison_id": "COMP2789_0_MICROSCOPE_WEP",
            "prediction_id": "PRED2789_0_DD_bulk_Earth_source_not_MTS_product",
            "bound_id": "BOUND2789_0_MICROSCOPE_WEP_source_charge",
            "abs_prediction": "MISSING_PARENT_TO_DD_MAP_OR_PROFILE_READOUT_NORMALIZATION",
            "upper_bound": "2.8e-15",
            "passes_bound": False,
            "comparison_status": "NOT_RUN_AS_MTS_PRODUCT",
            "reason": "bulk DD Earth source vector is numeric but not profile-weighted, parent-mapped, or readout-projected",
        })
    ]


def build_gate_rows() -> list[dict[str, Any]]:
    generated = ts()
    specs = [
        ("CG2789_0_source_vector", "physical R_source^Earth", False, False, "candidate is bulk-composition DD vector, not shell/profile/worldtube weighted"),
        ("CG2789_1_parent_to_DD_map", "MTS parent-to-DD coefficient map", False, False, "PTD2788_6_verdict=PARENT_TO_DD_MAP_NOT_DERIVED_BUT_CONDITIONAL_CHAIN_RULE_WRITTEN"),
        ("CG2789_2_official_readout", "K_MICROSCOPE readout", False, False, "official arrays/masks/timing not imported"),
        ("CG2789_3_common_mode", "source common-mode cancellation", False, False, "CMA2789_2_verdict=SOURCE_COMMON_MODE_NOT_SIGNED"),
        ("CG2789_4_product_runner", "WEP product runner", False, False, "valid_prediction_rows=0"),
    ]
    return [
        nonclaim({
            "gate_id": gate_id,
            "claim_component": component,
            "gate_pass": gate_pass,
            "claim_allowed": claim_allowed,
            "reason": reason,
            "generated_utc": generated,
        })
        for gate_id, component, gate_pass, claim_allowed, reason in specs
    ]


def build_decision_rows() -> list[dict[str, Any]]:
    generated = ts()
    specs = [
        ("DECISION2789_0", "DD Earth source vector first row is numeric but nonclaim", "bulk composition can be transformed into the external DD alpha/surface basis, but profile/readout/parent maps are missing", "do not treat this as an MTS WEP prediction"),
        ("DECISION2789_1", "explicit source-vector route remains open", "common-mode theorem is not signed and measured-G absorption is forbidden", "refine source profile weighting or import MICROSCOPE readout arrays before trying a physical product"),
        ("DECISION2789_2", "range/profile question is now unavoidable", "bulk Earth vector assumes the relevant carrier samples the whole Earth coherently", "2790 should choose profile weighting/readout import or derive long-range source condition"),
    ]
    return [
        nonclaim({
            "decision_id": decision_id,
            "decision": decision,
            "because": because,
            "next_action": next_action,
            "generated_utc": generated,
        })
        for decision_id, decision, because, next_action in specs
    ]


def build_next_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({
            "next_id": "NEXT2789_0_2790",
            "next_target": "2790-Y5-R2FR-DD-source-profile-weighting-or-MICROSCOPE-readout-import-gate-under-AX1090.md",
            "script": "scripts/Y5_R2FR_DD_source_profile_weighting_or_MICROSCOPE_readout_import_gate_under_AX1090_2790.py",
            "objective": "choose whether to refine the DD Earth source vector with shell/profile/worldtube weighting or begin the official MICROSCOPE readout import gate; keep parent-to-DD map blocked and no MTS claim",
            "include": "Earth shell/profile targets; candidate weighting kernels; CMSM/readout array requirements; product convention; strict claim gates",
            "exclude": "unit source proxy as physical source; measured-G absorption; DD profile smoke as MTS claim; GitHub; formalization edits",
        })
    ]


def copy_branches() -> list[dict[str, Any]]:
    copy_pairs = [
        (OUTPUTS["bulk_earth"], BRANCH_OUTPUTS["composition_queue"], "composition_queue"),
        (OUTPUTS["source_vector"], BRANCH_OUTPUTS["source_vector_queue"], "source_vector_queue"),
        (OUTPUTS["source_material_product"], BRANCH_OUTPUTS["product_queue"], "product_queue"),
        (OUTPUTS["source_vector"], BRANCH_OUTPUTS["beta_doc"], "beta_doc"),
        (OUTPUTS["source_material_product"], BRANCH_OUTPUTS["microscope_copy"], "microscope_copy"),
        (OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "next_queue"),
    ]
    rows = []
    for source, target, branch_key in copy_pairs:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        rows.append(nonclaim({
            "branch_id": f"BR2789_{len(rows)}_{branch_key}",
            "source_path": str(source),
            "branch_path": str(target),
            "exists": target.exists(),
            "row_count": csv_row_count(target) if target.exists() else 0,
            "branch_role": branch_key,
        }))
    return rows


def no_claim_flags(paths: list[Path]) -> bool:
    flag_fields = {"valid_for_claim", "claim_allowed", "pass_for_claim"}
    for path in paths:
        for row in read_csv_rows(path):
            for field in flag_fields:
                if trueish(row.get(field)):
                    return False
    return True


def formalization_modified_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    started = RUN_STARTED_UTC.timestamp()
    count = 0
    for path in FORMALIZATION.rglob("*"):
        if path.is_file() and path.stat().st_mtime >= started:
            count += 1
    return count


def build_validation_rows(sections: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    generated_paths = [path for key, path in OUTPUTS.items() if key != "validation"] + list(BRANCH_OUTPUTS.values())
    checks = [
        ("VAL2789_0_sources", all(trueish(row["exists"]) and trueish(row["needle_found"]) for row in sections["sources"]), "every cited source path exists and source needle was found"),
        ("VAL2789_1_web_sources_recorded", all(row["source_url"].startswith("http") for row in sections["web_sources"]), "web/source candidates are recorded"),
        ("VAL2789_2_bulk_mass_normalized", abs(sum(safe_float(row["normalized_mass_fraction"]) for row in sections["bulk_earth"]) - 1.0) < 1e-12, "bulk Earth mass fractions normalize to one"),
        ("VAL2789_3_formula_rows", any(row["formula_id"] == "DDF2789_0_alpha_Coulomb" for row in sections["formulas"]) and any(row["formula_id"] == "DDF2789_1_surface_binding" for row in sections["formulas"]), "DD charge formula rows are present"),
        ("VAL2789_4_element_charges_numeric", len(sections["element_charges"]) >= 10 and all(is_numeric(row["Q_alpha_Coulomb"]) and is_numeric(row["Q_surface_binding"]) for row in sections["element_charges"]), "element DD charges are numeric"),
        ("VAL2789_5_source_vector_numeric_nonclaim", all(is_numeric(row["Q_alpha_Coulomb_Earth"]) and is_numeric(row["Q_surface_binding_Earth"]) and not trueish(row["valid_for_claim"]) for row in sections["source_vector"]), "bulk Earth source vector is numeric but nonclaim"),
        ("VAL2789_6_source_product_numeric_nonclaim", all((is_numeric(row.get("product_abs")) or is_numeric(row.get("source_material_product"))) and not trueish(row["valid_for_claim"]) for row in sections["source_material_product"]), "source-material products are numeric but nonclaim"),
        ("VAL2789_7_caveat_gates_block", all(not trueish(row["gate_pass"]) for row in sections["caveat_gates"]), "source-vector caveat gates block claims"),
        ("VAL2789_8_common_mode_not_signed", any(row["route_id"] == "CMA2789_2_verdict" and row["status"] == "SOURCE_COMMON_MODE_NOT_SIGNED" for row in sections["common_mode"]), "common-mode route remains unsigned"),
        ("VAL2789_9_prediction_nonclaim_missing", all(has_missing_marker(row) and not trueish(row["valid_for_claim"]) for row in sections["candidate"]), "prediction row remains missing parent/profile/readout inputs"),
        ("VAL2789_10_bound_numeric", all(is_numeric(row["upper_bound"]) and float(row["upper_bound"]) > 0 for row in sections["bounds"]), "bound import is positive numeric"),
        ("VAL2789_11_runner_refuses", sections["runner"][0]["valid_prediction_rows"] == 0 and not trueish(sections["runner"][0]["claim_allowed"]), "generic product runner refuses DD source row as MTS product"),
        ("VAL2789_12_claim_gates_safe", all(not trueish(row.get("claim_allowed")) for row in sections["gates"]), "all claim gates deny WEP/local-GR claim"),
        ("VAL2789_13_next_target", "2790-Y5-R2FR" in sections["next"][0]["next_target"], "2790 handoff written"),
        ("VAL2789_14_branch_outputs", all(trueish(row["exists"]) and int(row["row_count"]) > 0 for row in sections["branches"]), "branch copies exist and contain rows"),
        ("VAL2789_15_csv_parse", all(csv_parses(path) for path in generated_paths), "all generated CSV outputs parse cleanly"),
        ("VAL2789_16_no_claim_flags", no_claim_flags(generated_paths), "no generated row is valid_for_claim=true/claim_allowed=true/pass_for_claim=true"),
        ("VAL2789_17_generated_under_post_checkpoint", all(WORK in path.parents or path == WORK for path in generated_paths + [DOC]), "all generated outputs are under post-checkpoint-work"),
        ("VAL2789_18_formalization_untouched", formalization_modified_count() == 0, "formalization-workbench modified-file count remains zero during this run"),
        ("VAL2789_19_pycache_absent", not (SCRIPTS / "__pycache__").exists(), "scripts __pycache__ absent at validation write"),
    ]
    rows = [
        {
            "validation_id": check_id,
            "passed": bool(passed),
            "detail": detail,
            "timestamp_utc": ts(),
        }
        for check_id, passed, detail in checks
    ]
    rows.append({
        "validation_id": "VAL2789_OVERALL",
        "passed": all(row["passed"] for row in rows),
        "detail": "2789 constructs the first numeric DD-basis bulk Earth/source vector and source-material products as nonclaim rows. The scaffold improves empirical plumbing, but parent-to-DD map, source profile/worldtube weighting, common-mode theorem, and official readout remain blocking gates.",
        "timestamp_utc": ts(),
    })
    return rows


def build_doc(sections: dict[str, list[dict[str, Any]]]) -> str:
    lines = [
        "# 2789 - DD Earth-source vector extraction plan and nonclaim first row under AX1090",
        "",
        "## Private Verdict",
        "",
        "2789 replaces the fake unit source proxy with a real first DD-basis bulk Earth/source vector row, but it is still strictly nonclaim. The row is useful: it gives numeric source-side alpha/Coulomb and surface/binding components and source-material product scales. It is not yet the physical MICROSCOPE source vector, because shell/profile/worldtube weighting, parent-to-DD coefficient map, source common-mode theorem, and official readout are still missing.",
        "",
        "## Source Register",
        markdown_table(sections["sources"], ["row_id", "source_key", "exists", "needle_found", "source_role"]),
        "",
        "## Web/Source Register",
        markdown_table(sections["web_sources"], ["web_source_id", "role", "source_url", "extraction_method", "confidence_level"]),
        "",
        "## Bulk Earth Composition Target",
        markdown_table(sections["bulk_earth"], ["element", "wt_percent", "normalized_mass_fraction", "Z", "A", "extraction_status"]),
        "",
        "## DD Charge Formula Ledger",
        markdown_table(sections["formulas"], ["formula_id", "component", "formula", "status", "claim_blocker"]),
        "",
        "## DD Earth Element Charges",
        markdown_table(sections["element_charges"], ["charge_id", "element", "normalized_mass_fraction", "Q_alpha_Coulomb", "Q_surface_binding", "status"]),
        "",
        "## DD Earth Source Vector First Row",
        markdown_table(sections["source_vector"], ["source_vector_id", "source_body", "basis", "Q_alpha_Coulomb_Earth", "Q_surface_binding_Earth", "status", "claim_blocker"]),
        "",
        "## DD Source-Material Product",
        markdown_table(sections["source_material_product"], ["product_id", "component", "source_material_product", "product_abs", "required_abs_coefficient_max_if_single_component", "required_abs_coefficient_max_if_equal_component", "status"]),
        "",
        "## Source Vector Caveat Gates",
        markdown_table(sections["caveat_gates"], ["gate_id", "claim_component", "gate_pass", "status", "reason"]),
        "",
        "## Common-Mode Alternative",
        markdown_table(sections["common_mode"], ["route_id", "claim", "status", "gap"]),
        "",
        "## Product Stub And Bound",
        markdown_table(sections["candidate"], ["prediction_id", "product_symbol", "product_value", "derivation_status", "valid_for_claim"]),
        "",
        markdown_table(sections["bounds"], ["bound_id", "observable", "upper_bound", "units", "valid_bound_row"]),
        "",
        markdown_table(sections["runner"], ["runner_id", "valid_prediction_rows", "valid_bound_rows", "claim_allowed", "expected_result"]),
        "",
        "## Claim Gates",
        markdown_table(sections["gates"], ["gate_id", "claim_component", "gate_pass", "claim_allowed", "reason"]),
        "",
        "## Decision Ledger",
        markdown_table(sections["decision"], ["decision_id", "decision", "because", "next_action"]),
        "",
        "## Validation",
        markdown_table(sections["validation"], ["validation_id", "passed", "detail"]),
        "",
        "## Next Target",
        markdown_table(sections["next"], ["next_id", "next_target", "objective", "include", "exclude"]),
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    ensure_dirs()
    if (SCRIPTS / "__pycache__").exists():
        shutil.rmtree(SCRIPTS / "__pycache__")

    bulk_rows = build_bulk_earth_rows()
    element_charge_rows = build_element_charge_rows(bulk_rows)
    source_vector_rows = build_source_vector_rows(element_charge_rows)
    source_material_product_rows = build_source_material_product_rows(source_vector_rows)

    sections: dict[str, list[dict[str, Any]]] = {
        "sources": build_sources(),
        "web_sources": build_web_sources(),
        "bulk_earth": bulk_rows,
        "formulas": build_formula_rows(),
        "element_charges": element_charge_rows,
        "source_vector": source_vector_rows,
        "source_material_product": source_material_product_rows,
        "caveat_gates": build_caveat_gate_rows(),
        "common_mode": build_common_mode_rows(),
        "candidate": build_candidate_rows(),
        "bounds": build_bound_rows(),
    }
    sections["runner"] = build_runner_rows(sections["candidate"], sections["bounds"])
    sections["comparisons"] = build_comparison_rows()
    sections["gates"] = build_gate_rows()
    sections["decision"] = build_decision_rows()
    sections["next"] = build_next_rows()

    for key, rows in sections.items():
        if key in OUTPUTS:
            write_csv(OUTPUTS[key], rows)

    sections["branches"] = copy_branches()
    write_csv(OUTPUTS["branches"], sections["branches"])

    sections["validation"] = build_validation_rows(sections)
    write_csv(OUTPUTS["validation"], sections["validation"])

    DOC.write_text(build_doc(sections), encoding="utf-8")
    print(f"wrote {DOC}")
    print(f"validation overall: {sections['validation'][-1]['passed']}")


if __name__ == "__main__":
    main()
