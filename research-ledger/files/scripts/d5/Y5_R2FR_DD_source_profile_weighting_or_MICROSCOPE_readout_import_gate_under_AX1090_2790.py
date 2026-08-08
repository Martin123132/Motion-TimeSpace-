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
DOC = WORK / "2790-Y5-R2FR-DD-source-profile-weighting-or-MICROSCOPE-readout-import-gate-under-AX1090.md"

OUTPUTS = {
    "sources": MTS / "P8_Y5_R2FR_2790_SOURCE_REGISTER.csv",
    "web_sources": MTS / "P8_Y5_R2FR_2790_WEB_SOURCE_REGISTER.csv",
    "kernel": MTS / "P8_Y5_R2FR_2790_SOURCE_PROFILE_KERNEL_DERIVATION_LEDGER.csv",
    "layers": MTS / "P8_Y5_R2FR_2790_CORE_MANTLE_COMPOSITION_CANDIDATE.csv",
    "layer_charges": MTS / "P8_Y5_R2FR_2790_CORE_MANTLE_DD_CHARGE_VECTORS.csv",
    "profile_grid": MTS / "P8_Y5_R2FR_2790_SOURCE_PROFILE_WEIGHTING_GRID_NONCLAIM.csv",
    "profile_gates": MTS / "P8_Y5_R2FR_2790_PROFILE_CLOSURE_GATES.csv",
    "readout_gate": MTS / "P8_Y5_R2FR_2790_MICROSCOPE_READOUT_IMPORT_GATE.csv",
    "candidate": MTS / "P8_Y5_R2FR_2790_WEP_PRODUCT_CANDIDATE_NONCLAIM.csv",
    "bounds": MTS / "P8_Y5_R2FR_2790_WEP_BOUND_IMPORT.csv",
    "runner": MTS / "P8_Y5_R2FR_2790_PRODUCT_RUNNER_STATUS.csv",
    "comparisons": MTS / "P8_Y5_R2FR_2790_PRODUCT_COMPARISON_ROWS.csv",
    "gates": MTS / "P8_Y5_R2FR_2790_CLAIM_GATES.csv",
    "decision": MTS / "P8_Y5_R2FR_2790_DECISION_LEDGER.csv",
    "next": MTS / "P8_Y5_R2FR_2790_NEXT_TARGET.csv",
    "branches": MTS / "P8_Y5_R2FR_2790_BRANCH_COPIES.csv",
    "validation": MTS / "P8_Y5_BRR545_2790_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "profile_grid_queue": RAB_QUEUE / "JR2790_SOURCE_PROFILE_WEIGHTING_GRID_NONCLAIM.csv",
    "readout_gate_queue": RAB_QUEUE / "JR2790_MICROSCOPE_READOUT_IMPORT_GATE_NONCLAIM.csv",
    "kernel_doc": BETA_DOCS / "DD_SOURCE_PROFILE_KERNEL_2790_NONCLAIM.csv",
    "microscope_copy": MICROSCOPE_DIR / "microscope_readout_import_gate_2790_nonclaim.csv",
    "next_queue": RAB_QUEUE / "JR2790_WEP_RANGE_OWNER_NEXT.csv",
}

RE = 6.371e6
CORE_RADIUS = 3.48e6
ORBIT_ALTITUDE = 710e3

LAYER_COMPOSITION = [
    ("mantle", "Fe", 6.26, 26, 55.845),
    ("mantle", "O", 44.0, 8, 15.999),
    ("mantle", "Si", 21.0, 14, 28.085),
    ("mantle", "Mg", 22.8, 12, 24.305),
    ("mantle", "Ni", 0.2, 28, 58.693),
    ("mantle", "Ca", 2.53, 20, 40.078),
    ("mantle", "Al", 2.35, 13, 26.982),
    ("mantle", "S", 0.03, 16, 32.06),
    ("mantle", "Cr", 0.26, 24, 51.996),
    ("core", "Fe", 85.5, 26, 55.845),
    ("core", "O", 0.0, 8, 15.999),
    ("core", "Si", 6.0, 14, 28.085),
    ("core", "Mg", 0.0, 12, 24.305),
    ("core", "Ni", 5.2, 28, 58.693),
    ("core", "Ca", 0.0, 20, 40.078),
    ("core", "Al", 0.0, 13, 26.982),
    ("core", "S", 1.9, 16, 32.06),
    ("core", "Cr", 0.9, 24, 51.996),
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


def safe_float(value: Any, fallback: float = 0.0) -> float:
    try:
        return float(str(value))
    except (TypeError, ValueError):
        return fallback


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


def q_alpha(z: float, a: float) -> float:
    return 7.7e-4 * z * (z - 1.0) / (a ** (4.0 / 3.0))


def q_surface(z: float, a: float) -> float:
    return -0.036 / (a ** (1.0 / 3.0)) - 1.4e-4 * z * (z - 1.0) / (a ** (4.0 / 3.0))


def shell_kernel_mean(inner_radius: float, outer_radius: float, lambda_m: float | None, n_steps: int = 20000) -> float:
    if lambda_m is None:
        return 1.0
    n = n_steps + (n_steps % 2)
    h = (outer_radius - inner_radius) / n

    def integrand(radius: float) -> float:
        x = radius / lambda_m
        return radius * radius * (math.sinh(x) / x if x else 1.0)

    total = integrand(inner_radius) + integrand(outer_radius)
    for idx in range(1, n):
        total += (4 if idx % 2 else 2) * integrand(inner_radius + idx * h)
    integral = total * h / 3.0
    denominator = (outer_radius**3 - inner_radius**3) / 3.0
    return integral / denominator


def build_sources() -> list[dict[str, Any]]:
    specs = [
        ("SRC2790_00_2789_next", "2789_next", MTS / "P8_Y5_R2FR_2789_NEXT_TARGET.csv", "NEXT2789_0_2790", "current handoff into profile/readout gate"),
        ("SRC2790_01_2789_validation", "2789_validation", MTS / "P8_Y5_BRR545_2789_VALIDATION.csv", "VAL2789_OVERALL", "2789 validation baseline"),
        ("SRC2790_02_2789_source_vector", "2789_source_vector", MTS / "P8_Y5_R2FR_2789_DD_EARTH_SOURCE_VECTOR_FIRST_ROW_NONCLAIM.csv", "DD_EARTH2789_0_bulk_weighted", "R2FR first bulk Earth DD source vector"),
        ("SRC2790_03_2789_product", "2789_product", MTS / "P8_Y5_R2FR_2789_DD_SOURCE_MATERIAL_PRODUCT_NONCLAIM.csv", "DD_PRODUCT2789_0_alpha", "R2FR DD source-material products"),
        ("SRC2790_04_2789_caveat", "2789_caveat", MTS / "P8_Y5_R2FR_2789_SOURCE_VECTOR_CAVEAT_GATE.csv", "SCG2789_0_profile_weighting", "R2FR source vector caveat gates"),
        ("SRC2790_05_1084_kernel", "1084_kernel", MTS / "P8_Y5_R10_1084_SOURCE_PROFILE_KERNEL_DERIVATION_LEDGER.csv", "K1084_1_effective_source_charge", "R10 finite-range profile kernel precedent"),
        ("SRC2790_06_1084_layers", "1084_layers", MTS / "P8_Y5_R10_1084_CORE_MANTLE_COMPOSITION_CANDIDATE.csv", "LAYER1084_mantle_Fe", "R10 core/mantle composition rows"),
        ("SRC2790_07_1084_profile_grid", "1084_profile_grid", MTS / "P8_Y5_R10_1084_SOURCE_PROFILE_WEIGHTING_GRID_NONCLAIM.csv", "PROFILE1084_lambda_over_RE_1", "R10 profile weighting grid precedent"),
        ("SRC2790_08_1084_readout", "1084_readout", MTS / "P8_Y5_R10_1084_MICROSCOPE_READOUT_IMPORT_GATE.csv", "RIG1084_0_CMSM_arrays", "R10 MICROSCOPE readout import gate"),
        ("SRC2790_09_1084_next", "1084_next", MTS / "P8_Y5_R10_1084_NEXT_TARGET.csv", "NEXT1084_0_1085", "R10 next target after profile/readout gate"),
        ("SRC2790_10_2780_cmsm", "2780_cmsm", MTS / "P8_Y5_R2FR_2780_CMSM_EXPORT_INVENTORY_CHECK.csv", "INV2780_0_search_root", "R2FR official CMSM export search"),
        ("SRC2790_11_2781_tau", "2781_tau", MTS / "P8_Y5_R2FR_2781_TAU_SHAPE_STATUS.csv", "TAUSHAPE2781_2_physics_tau", "R2FR physical tau missing status"),
        ("SRC2790_12_local_bounds", "local_bounds", LOCAL_BOUNDS / "local_bound_claims.csv", "R1_WEP_source_charge", "MICROSCOPE WEP bound row"),
    ]
    return [source_row(*spec) for spec in specs]


def build_web_sources() -> list[dict[str, Any]]:
    generated = ts()
    return [
        nonclaim({
            "web_source_id": "WEB2790_0_MCDONOUGH_2003_TABLE5",
            "role": "core/mantle/bulk composition source",
            "source_url": "https://www.mso.anu.edu.au/PSI/PSI_Meetings/Entries/2007/6/13_The_bulk_composition_of_the_Earth_%281%29_files/Treatise%20on%20Geochemistry%202003%20McDonough.pdf",
            "source_title": "Compositional Model for the Earth's Core",
            "evidence_used": "bulk Earth, mantle, and core candidate compositions reused from the 1084 extraction precedent",
            "extraction_method": "candidate manual table rows; profile smoke only",
            "confidence_level": "sufficient_for_nonclaim_profile_grid; insufficient_for_claim",
            "generated_utc": generated,
        }),
        nonclaim({
            "web_source_id": "WEB2790_1_MICROSCOPE_READOUT",
            "role": "official MICROSCOPE readout/data portal context",
            "source_url": "https://moriond.in2p3.fr/2023/Gravitation/transparencies/06_friday/01_morning/02_metris.pdf",
            "source_title": "Analysis and results from MICROSCOPE",
            "evidence_used": "CMSM/readout arrays requirement inherited from 2780/1084 gates",
            "extraction_method": "no local official arrays imported in this checkpoint",
            "confidence_level": "readout_gate_only",
            "generated_utc": generated,
        }),
    ]


def build_kernel_rows() -> list[dict[str, Any]]:
    generated = ts()
    rows = [
        ("K2790_0_angular_integral", "external finite-range spherical source reduces to a radial kernel", "for r>R, angular integral gives common exp(-r/lambda)/r factor times int rho(r') q(r') r'^2 sinh(r'/lambda)/(r'/lambda) dr", "DERIVED_AS_KERNEL_CONTRACT", "kernel is external DD/Yukawa profile algebra, not yet MTS parent-derived"),
        ("K2790_1_effective_source_charge", "profile-weighted source charge can be defined", "Q_eff(lambda)=int rho q W_lambda dr / int rho W_lambda dr, W_lambda=4*pi*r^2*sinh(r/lambda)/(r/lambda)", "DERIVED_AS_NONCLAIM_PROFILE_RULE", "requires lambda owner and sourced rho(r), q(r)"),
        ("K2790_2_long_range_limit", "bulk source vector is recovered in the long-range limit", "lambda >> R_E makes sinh(r/lambda)/(r/lambda)=1+O(R_E^2/lambda^2), so Q_eff tends the mass-weighted source average", "LONG_RANGE_LIMIT_CONDITIONALLY_DERIVED", "MTS has not derived that the WEP carrier range is long compared with Earth radius"),
        ("K2790_3_finite_range_profile_dependency", "finite-range branch is surface/profile sensitive", "as lambda decreases, W_lambda favors larger r and the effective source vector tends the near-surface layer composition", "FINITE_RANGE_PROFILE_DEPENDENCY_RETAINED", "no PREM/compositional shell vector and no MTS lambda_WEP selection"),
        ("K2790_4_orbit_factor", "710 km orbit is a common first-pass amplitude factor for a spherical source", "outside-source r=R_E+h appears in the common exp(-r/lambda)/r and force derivative factor, not in Q_eff(lambda), under spherical symmetry", "READOUT_AMPLITUDE_SEPARATED_NONCLAIM", "actual MICROSCOPE readout uses time-dependent gx/gz/Sxx/Sxz/masks not imported here"),
    ]
    return [
        nonclaim({
            "kernel_id": kernel_id,
            "claim": claim,
            "formula_or_condition": formula,
            "status": status,
            "claim_blocker": blocker,
            "generated_utc": generated,
        })
        for kernel_id, claim, formula, status, blocker in rows
    ]


def layer_mass_fractions() -> tuple[float, float]:
    bulk_fe = 32.0
    mantle_fe = 6.26
    core_fe = 85.5
    core_fraction = (bulk_fe - mantle_fe) / (core_fe - mantle_fe)
    return 1.0 - core_fraction, core_fraction


def build_layer_rows() -> list[dict[str, Any]]:
    generated = ts()
    rows = []
    sums = {
        "mantle": sum(wt for layer, _, wt, _, _ in LAYER_COMPOSITION if layer == "mantle"),
        "core": sum(wt for layer, _, wt, _, _ in LAYER_COMPOSITION if layer == "core"),
    }
    for layer, element, wt_percent, z, a in LAYER_COMPOSITION:
        rows.append(nonclaim({
            "layer_id": f"LAYER2790_{layer}_{element}",
            "layer": layer,
            "element": element,
            "wt_percent": f"{wt_percent:g}",
            "normalized_layer_mass_fraction": f"{wt_percent / sums[layer]:.15e}",
            "Z": z,
            "A": a,
            "source_table": "WEB2790_0_MCDONOUGH_2003_TABLE5",
            "extraction_status": "TABLE5_LAYER_TARGET_CANDIDATE_NONCLAIM",
            "generated_utc": generated,
        }))
    return rows


def build_layer_charge_rows(layer_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    generated = ts()
    mantle_fraction, core_fraction = layer_mass_fractions()
    mass_fraction_by_layer = {"mantle": mantle_fraction, "core": core_fraction}
    radius_by_layer = {"mantle": (CORE_RADIUS, RE), "core": (0.0, CORE_RADIUS)}
    output = []
    for layer in ["mantle", "core"]:
        layer_specific = [row for row in layer_rows if row["layer"] == layer]
        q_alpha_layer = sum(safe_float(row["normalized_layer_mass_fraction"]) * q_alpha(safe_float(row["Z"]), safe_float(row["A"])) for row in layer_specific)
        q_surface_layer = sum(safe_float(row["normalized_layer_mass_fraction"]) * q_surface(safe_float(row["Z"]), safe_float(row["A"])) for row in layer_specific)
        composition_sum = sum(safe_float(row["wt_percent"]) for row in layer_specific)
        inner, outer = radius_by_layer[layer]
        output.append(nonclaim({
            "layer_charge_id": f"LC2790_{layer}",
            "layer": layer,
            "inner_radius_m": f"{inner:.6e}",
            "outer_radius_m": f"{outer:.6e}",
            "mass_fraction_candidate": f"{mass_fraction_by_layer[layer]:.15e}",
            "composition_sum_wt_percent": f"{composition_sum:g}",
            "Q_alpha_Coulomb_layer": f"{q_alpha_layer:.15e}",
            "Q_surface_binding_layer": f"{q_surface_layer:.15e}",
            "mass_fraction_source": "derived from Table5 Fe mass balance: Fe_bulk=f_mantle*Fe_mantle+f_core*Fe_core",
            "status": "NUMERIC_TWO_LAYER_DD_CHARGE_NONCLAIM",
            "generated_utc": generated,
        }))
    return output


def build_profile_grid_rows(layer_charge_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    generated = ts()
    bulk = read_csv_rows(MTS / "P8_Y5_R2FR_2789_DD_EARTH_SOURCE_VECTOR_FIRST_ROW_NONCLAIM.csv")
    bulk_alpha = safe_float(bulk[0].get("Q_alpha_Coulomb_Earth") if bulk else None, 1.691260686750872e-03)
    bulk_surface = safe_float(bulk[0].get("Q_surface_binding_Earth") if bulk else None, -1.211918219995745e-02)
    by_layer = {row["layer"]: row for row in layer_charge_rows}
    mantle_fraction, core_fraction = layer_mass_fractions()
    lambdas: list[tuple[str, float | None, str]] = [
        ("PROFILE2790_long_range_mass_average", None, "long_range_mass_average"),
        ("PROFILE2790_lambda_over_RE_100", 100.0 * RE, "lambda_over_RE_100"),
        ("PROFILE2790_lambda_over_RE_10", 10.0 * RE, "lambda_over_RE_10"),
        ("PROFILE2790_lambda_over_RE_1", RE, "lambda_over_RE_1"),
        ("PROFILE2790_lambda_over_RE_0p3", 0.3 * RE, "lambda_over_RE_0p3"),
        ("PROFILE2790_lambda_over_RE_0p1", 0.1 * RE, "lambda_over_RE_0p1"),
        ("PROFILE2790_lambda_over_RE_0p03", 0.03 * RE, "lambda_over_RE_0p03"),
    ]
    rows = []
    for profile_id, lambda_m, label in lambdas:
        mantle_kernel = shell_kernel_mean(CORE_RADIUS, RE, lambda_m)
        core_kernel = shell_kernel_mean(0.0, CORE_RADIUS, lambda_m)
        mantle_weight = mantle_fraction * mantle_kernel
        core_weight = core_fraction * core_kernel
        denominator = mantle_weight + core_weight
        q_alpha_eff = (
            mantle_weight * safe_float(by_layer["mantle"]["Q_alpha_Coulomb_layer"])
            + core_weight * safe_float(by_layer["core"]["Q_alpha_Coulomb_layer"])
        ) / denominator
        q_surface_eff = (
            mantle_weight * safe_float(by_layer["mantle"]["Q_surface_binding_layer"])
            + core_weight * safe_float(by_layer["core"]["Q_surface_binding_layer"])
        ) / denominator
        rows.append(nonclaim({
            "profile_row_id": profile_id,
            "lambda_label": label,
            "lambda_m": "inf" if lambda_m is None else f"{lambda_m:.15e}",
            "lambda_over_R_E": "inf" if lambda_m is None else f"{lambda_m / RE:.15e}",
            "mantle_kernel_mean": f"{mantle_kernel:.15e}",
            "core_kernel_mean": f"{core_kernel:.15e}",
            "Q_alpha_Coulomb_eff": f"{q_alpha_eff:.15e}",
            "Q_surface_binding_eff": f"{q_surface_eff:.15e}",
            "delta_alpha_vs_2789_bulk": f"{q_alpha_eff - bulk_alpha:.15e}",
            "delta_surface_vs_2789_bulk": f"{q_surface_eff - bulk_surface:.15e}",
            "profile_model": "two_layer_uniform_core_mantle_candidate",
            "status": "NUMERIC_PROFILE_WEIGHTING_SMOKE_NONCLAIM",
            "generated_utc": generated,
        }))
    return rows


def build_profile_gate_rows() -> list[dict[str, Any]]:
    generated = ts()
    specs = [
        ("PCG2790_0_long_range_bulk_limit", "bulk source vector suffices", "conditional", "derive lambda_WEP >> R_E or massless/common long-range source carrier from parent action", "CONDITION_NOT_PARENT_SIGNED"),
        ("PCG2790_1_finite_range_profile", "finite-range source profile vector", "false", "import PREM density plus shell composition profile and choose lambda_WEP", "MISSING_PREM_IMPORT_AND_LAMBDA_OWNER"),
        ("PCG2790_2_source_charge_basis", "DD profile vector is an MTS source vector", "false", "derive parent-to-DD coefficient/source basis map", "PARENT_TO_DD_MAP_NOT_DERIVED"),
        ("PCG2790_3_readout_projection", "profile vector is projected into MICROSCOPE eta", "false", "import official/validated MICROSCOPE readout arrays", "OFFICIAL_READOUT_NOT_IMPORTED"),
    ]
    return [
        nonclaim({
            "gate_id": gate_id,
            "claim_component": component,
            "gate_pass": gate_pass,
            "condition": condition,
            "current_status": status,
            "generated_utc": generated,
        })
        for gate_id, component, gate_pass, condition, status in specs
    ]


def build_readout_gate_rows() -> list[dict[str, Any]]:
    generated = ts()
    specs = [
        ("RIG2790_0_CMSM_arrays", "official MICROSCOPE CMSM/export arrays", "time, segment/session id, gx, gz, Sxx, Sxz, masks, calibration flags, attitude/orbit convention", "OFFICIAL_ARRAYS_NOT_IMPORTED", "unit or surrogate readout cannot become physical tau_WEP"),
        ("RIG2790_1_product_convention", "eta_AB product normalization", "map from source response x material response x readout kernel to reported Eotvos eta", "NORMALIZATION_NOT_FILLED", "numeric profile products are scale probes only"),
        ("RIG2790_2_surrogate_limit", "surrogate design matrix relation to official readout", "proof surrogate kernel has same units/normalization as official arrays", "SURROGATE_AVAILABLE_NONCLAIM", "cannot replace official readout for a WEP claim"),
        ("RIG2790_3_CMSM_inventory", "local CMSM export status", "official export search and user-supplied array directory", "NO_USER_SUPPLIED_CMSM_EXPORT_FOUND", "2780 inventory found no official local export"),
    ]
    return [
        nonclaim({
            "readout_id": readout_id,
            "needed_object": needed,
            "required_content": required,
            "current_status": status,
            "claim_blocker": blocker,
            "generated_utc": generated,
        })
        for readout_id, needed, required, status, blocker in specs
    ]


def build_candidate_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({
            "prediction_id": "PRED2790_0_DD_profile_or_readout_not_MTS_product",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "P_WEP_relative_source_weight",
            "product_value": "MISSING_LAMBDA_WEP_OR_PREM_PROFILE_AND_OFFICIAL_READOUT_AND_PARENT_TO_DD_MAP",
            "product_units": "dimensionless",
            "product_source": "source-intake/mts_residuals/P8_Y5_R2FR_2790_SOURCE_PROFILE_WEIGHTING_GRID_NONCLAIM.csv",
            "inputs_present": "two-layer DD profile smoke grid; bulk Earth source vector; MICROSCOPE bound",
            "required_inputs": "lambda_WEP/range owner or long-range theorem; PREM/shell profile; official/validated readout; parent-to-DD map",
            "derivation_status": "PROFILE_GRID_NUMERIC_BUT_PHYSICAL_PRODUCT_MISSING",
            "notes": "generic product runner must refuse because profile rows are external DD smoke without range/readout/map closure",
        })
    ]


def build_bound_rows() -> list[dict[str, Any]]:
    bound = get_local_bound("R1_WEP_source_charge")
    return [
        nonclaim({
            "bound_id": "BOUND2790_0_MICROSCOPE_WEP_source_charge",
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
            "runner_id": "APR2790_0_DD_profile_readout_product_stub",
            "prediction_rows": len(candidate_rows),
            "bound_rows": len(bound_rows),
            "valid_prediction_rows": len(valid_prediction_rows),
            "valid_bound_rows": len(valid_bound_rows),
            "comparison_rows": 1,
            "passed_rows": 0,
            "claim_allowed": False,
            "expected_result": "reject DD profile/readout rows as MTS product",
        })
    ]


def build_comparison_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({
            "comparison_id": "COMP2790_0_MICROSCOPE_WEP",
            "prediction_id": "PRED2790_0_DD_profile_or_readout_not_MTS_product",
            "bound_id": "BOUND2790_0_MICROSCOPE_WEP_source_charge",
            "abs_prediction": "MISSING_LAMBDA_WEP_OR_PREM_PROFILE_AND_OFFICIAL_READOUT_AND_PARENT_TO_DD_MAP",
            "upper_bound": "2.8e-15",
            "passes_bound": False,
            "comparison_status": "NOT_RUN_AS_MTS_PRODUCT",
            "reason": "profile grid is numeric but lambda/range owner, profile data, parent map, and readout are missing",
        })
    ]


def build_gate_rows() -> list[dict[str, Any]]:
    generated = ts()
    specs = [
        ("CG2790_0_profile_rule", "source-profile rule", "conditional", False, "radial kernel rule derived as external DD/Yukawa algebra, but physical source needs lambda/profile"),
        ("CG2790_1_long_range_bulk", "bulk source vector suffices", "conditional", False, "requires parent-signed lambda_WEP >> R_E or massless common carrier"),
        ("CG2790_2_parent_to_DD", "MTS parent-to-DD map", "false", False, "still not derived"),
        ("CG2790_3_readout", "MICROSCOPE official readout", "false", False, "CMSM/export arrays and eta normalization not imported"),
        ("CG2790_4_product_runner", "WEP product runner", "false", False, "valid_prediction_rows=0"),
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
        ("DECISION2790_0", "source-profile algebra is explicit in R2FR", "finite-range spherical source weighting reduces to a hyperbolic radial kernel and has a clean long-range bulk limit", "derive lambda_WEP from parent action before using either bulk or finite-range profile rows as physical"),
        ("DECISION2790_1", "MICROSCOPE readout import remains a separate hard gate", "710 km orbit and spherical source profile do not substitute for gx/gz/Sxx/Sxz/masks/timing/product normalization", "either acquire official arrays or continue parent-side derivation of the coefficient/range owner"),
        ("DECISION2790_2", "next derivation target is range owner", "profile grid shows bulk-vs-finite-range dependence; deciding bulk source legitimacy requires lambda_WEP >> R_E or a common long-range carrier theorem", "2791 should derive WEP range owner or retain lambda-dependent profile rows and route to PREM/readout import"),
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
            "next_id": "NEXT2790_0_2791",
            "next_target": "2791-Y5-R2FR-WEP-range-owner-or-long-range-limit-theorem-under-AX1090.md",
            "script": "scripts/Y5_R2FR_WEP_range_owner_or_long_range_limit_theorem_under_AX1090_2791.py",
            "objective": "derive whether the local WEP carrier/source response is long range enough for the bulk Earth vector, or retain lambda-dependent profile rows and route to PREM/readout import; do not claim WEP/local-GR",
            "include": "parent mass/range operator; lambda_WEP >> R_E condition; relation to local/R10 lambda; parent-to-DD coefficient pressure point; readout import fallback",
            "exclude": "measured-G absorption; unit source proxy; DD profile smoke as MTS claim; GitHub; formalization edits",
        })
    ]


def copy_branches() -> list[dict[str, Any]]:
    copy_pairs = [
        (OUTPUTS["profile_grid"], BRANCH_OUTPUTS["profile_grid_queue"], "profile_grid_queue"),
        (OUTPUTS["readout_gate"], BRANCH_OUTPUTS["readout_gate_queue"], "readout_gate_queue"),
        (OUTPUTS["kernel"], BRANCH_OUTPUTS["kernel_doc"], "kernel_doc"),
        (OUTPUTS["readout_gate"], BRANCH_OUTPUTS["microscope_copy"], "microscope_copy"),
        (OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "next_queue"),
    ]
    rows = []
    for source, target, branch_key in copy_pairs:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        rows.append(nonclaim({
            "branch_id": f"BR2790_{len(rows)}_{branch_key}",
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
        ("VAL2790_0_sources", all(trueish(row["exists"]) and trueish(row["needle_found"]) for row in sections["sources"]), "every cited source path exists and source needle was found"),
        ("VAL2790_1_kernel_rule", any(row["kernel_id"] == "K2790_1_effective_source_charge" and row["status"] == "DERIVED_AS_NONCLAIM_PROFILE_RULE" for row in sections["kernel"]), "effective profile source charge rule is staged"),
        ("VAL2790_2_layer_rows", len(sections["layers"]) >= 18 and all(is_numeric(row["normalized_layer_mass_fraction"]) for row in sections["layers"]), "core/mantle composition rows are numeric"),
        ("VAL2790_3_layer_charges", len(sections["layer_charges"]) == 2 and all(is_numeric(row["Q_alpha_Coulomb_layer"]) and is_numeric(row["Q_surface_binding_layer"]) for row in sections["layer_charges"]), "core/mantle DD charge vectors are numeric"),
        ("VAL2790_4_profile_grid", len(sections["profile_grid"]) >= 7 and all(is_numeric(row["Q_alpha_Coulomb_eff"]) and is_numeric(row["Q_surface_binding_eff"]) for row in sections["profile_grid"]), "profile weighting grid is numeric"),
        ("VAL2790_5_profile_gates_block", all(not trueish(row["valid_for_claim"]) for row in sections["profile_gates"]) and any(row["gate_id"] == "PCG2790_1_finite_range_profile" and row["current_status"] == "MISSING_PREM_IMPORT_AND_LAMBDA_OWNER" for row in sections["profile_gates"]), "profile closure gates block claims"),
        ("VAL2790_6_readout_gate_blocks", any(row["readout_id"] == "RIG2790_0_CMSM_arrays" and row["current_status"] == "OFFICIAL_ARRAYS_NOT_IMPORTED" for row in sections["readout_gate"]), "official MICROSCOPE readout arrays are not imported"),
        ("VAL2790_7_prediction_nonclaim_missing", all(has_missing_marker(row) and not trueish(row["valid_for_claim"]) for row in sections["candidate"]), "prediction row remains missing lambda/profile/readout/map inputs"),
        ("VAL2790_8_bound_numeric", all(is_numeric(row["upper_bound"]) and float(row["upper_bound"]) > 0 for row in sections["bounds"]), "bound import is positive numeric"),
        ("VAL2790_9_runner_refuses", sections["runner"][0]["valid_prediction_rows"] == 0 and not trueish(sections["runner"][0]["claim_allowed"]), "generic product runner refuses DD profile/readout rows as MTS product"),
        ("VAL2790_10_claim_gates_safe", all(not trueish(row.get("claim_allowed")) for row in sections["gates"]), "all claim gates deny WEP/local-GR claim"),
        ("VAL2790_11_next_target", "2791-Y5-R2FR" in sections["next"][0]["next_target"], "2791 handoff written"),
        ("VAL2790_12_branch_outputs", all(trueish(row["exists"]) and int(row["row_count"]) > 0 for row in sections["branches"]), "branch copies exist and contain rows"),
        ("VAL2790_13_csv_parse", all(csv_parses(path) for path in generated_paths), "all generated CSV outputs parse cleanly"),
        ("VAL2790_14_no_claim_flags", no_claim_flags(generated_paths), "no generated row is valid_for_claim=true/claim_allowed=true/pass_for_claim=true"),
        ("VAL2790_15_generated_under_post_checkpoint", all(WORK in path.parents or path == WORK for path in generated_paths + [DOC]), "all generated outputs are under post-checkpoint-work"),
        ("VAL2790_16_formalization_untouched", formalization_modified_count() == 0, "formalization-workbench modified-file count remains zero during this run"),
        ("VAL2790_17_pycache_absent", not (SCRIPTS / "__pycache__").exists(), "scripts __pycache__ absent at validation write"),
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
        "validation_id": "VAL2790_OVERALL",
        "passed": all(row["passed"] for row in rows),
        "detail": "2790 stages the finite-range DD source-profile kernel, a two-layer core/mantle profile grid, and the MICROSCOPE readout import gate. Numeric profile rows remain nonclaim because lambda_WEP/range owner, PREM/profile closure, parent-to-DD map, and official readout are still missing.",
        "timestamp_utc": ts(),
    })
    return rows


def build_doc(sections: dict[str, list[dict[str, Any]]]) -> str:
    lines = [
        "# 2790 - DD source-profile weighting or MICROSCOPE readout import gate under AX1090",
        "",
        "## Private Verdict",
        "",
        "2790 answers the route-choice question by keeping both gates explicit. The source profile algebra is now in the R2FR branch: finite-range spherical source weighting gives a clean radial kernel and a long-range bulk limit. But using the bulk Earth row physically requires a parent-signed long-range condition lambda_WEP >> R_E, while using finite-range rows requires PREM/profile weighting and a lambda owner. MICROSCOPE readout import remains separate; gx/gz/Sxx/Sxz/masks/timing and eta normalization are not replaced by the spherical profile smoke rows.",
        "",
        "## Source Register",
        markdown_table(sections["sources"], ["row_id", "source_key", "exists", "needle_found", "source_role"]),
        "",
        "## Profile Kernel Ledger",
        markdown_table(sections["kernel"], ["kernel_id", "claim", "status", "claim_blocker"]),
        "",
        "## Core/Mantle Composition Candidate",
        markdown_table(sections["layers"], ["layer_id", "layer", "element", "normalized_layer_mass_fraction", "Z", "A", "extraction_status"]),
        "",
        "## Core/Mantle DD Charge Vectors",
        markdown_table(sections["layer_charges"], ["layer_charge_id", "layer", "mass_fraction_candidate", "Q_alpha_Coulomb_layer", "Q_surface_binding_layer", "status"]),
        "",
        "## Source Profile Weighting Grid",
        markdown_table(sections["profile_grid"], ["profile_row_id", "lambda_label", "lambda_over_R_E", "Q_alpha_Coulomb_eff", "Q_surface_binding_eff", "delta_alpha_vs_2789_bulk", "delta_surface_vs_2789_bulk", "status"]),
        "",
        "## Profile Closure Gates",
        markdown_table(sections["profile_gates"], ["gate_id", "claim_component", "gate_pass", "condition", "current_status"]),
        "",
        "## MICROSCOPE Readout Import Gate",
        markdown_table(sections["readout_gate"], ["readout_id", "needed_object", "current_status", "claim_blocker"]),
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

    layer_rows = build_layer_rows()
    layer_charge_rows = build_layer_charge_rows(layer_rows)
    profile_grid_rows = build_profile_grid_rows(layer_charge_rows)

    sections: dict[str, list[dict[str, Any]]] = {
        "sources": build_sources(),
        "web_sources": build_web_sources(),
        "kernel": build_kernel_rows(),
        "layers": layer_rows,
        "layer_charges": layer_charge_rows,
        "profile_grid": profile_grid_rows,
        "profile_gates": build_profile_gate_rows(),
        "readout_gate": build_readout_gate_rows(),
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
