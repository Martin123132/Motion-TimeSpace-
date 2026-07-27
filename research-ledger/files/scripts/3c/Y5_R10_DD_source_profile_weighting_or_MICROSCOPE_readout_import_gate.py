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
DOC = ROOT / "1084-Y5-R10-DD-source-profile-weighting-or-MICROSCOPE-readout-import-gate.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_DIR = ROOT / "runs" / "1084-DD-source-profile-weighting-or-readout-import" / "results"
PRODUCT_RUN_DIR = RUN_DIR / "product_runner"
PREDICTION_TEMPLATE = OUT / "P8_Y5_R10_1084_WEP_PRODUCT_CANDIDATE_NONCLAIM.csv"
BOUND_IMPORT = OUT / "P8_Y5_R10_1084_WEP_BOUND_IMPORT.csv"

EARTH_RADIUS_M = 6_371_000.0
CORE_RADIUS_M = 3_480_000.0
ORBIT_ALTITUDE_M = 710_000.0
ETA_BOUND = 2.8e-15

ELEMENT_ZA = {
    "Fe": (26, 55.845),
    "O": (8, 15.999),
    "Si": (14, 28.085),
    "Mg": (12, 24.305),
    "Ni": (28, 58.693),
    "Ca": (20, 40.078),
    "Al": (13, 26.982),
    "S": (16, 32.06),
    "Cr": (24, 51.996),
}

MANTLE_COMPOSITION = {
    "Fe": 6.26,
    "O": 44.0,
    "Si": 21.0,
    "Mg": 22.8,
    "Ni": 0.20,
    "Ca": 2.53,
    "Al": 2.35,
    "S": 0.03,
    "Cr": 0.26,
}

CORE_COMPOSITION = {
    "Fe": 85.5,
    "O": 0.0,
    "Si": 6.0,
    "Mg": 0.0,
    "Ni": 5.2,
    "Ca": 0.0,
    "Al": 0.0,
    "S": 1.9,
    "Cr": 0.9,
}


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


def q_alpha_coulomb(z_value: int, a_value: float) -> float:
    return 7.7e-4 * z_value * (z_value - 1) / (a_value ** (4.0 / 3.0))


def q_surface_binding(z_value: int, a_value: float) -> float:
    return -0.036 / (a_value ** (1.0 / 3.0)) - 1.4e-4 * z_value * (z_value - 1) / (a_value ** (4.0 / 3.0))


def composition_charge(composition: dict[str, float]) -> tuple[float, float, float]:
    total = sum(composition.values())
    alpha = 0.0
    surface = 0.0
    for element, wt_percent in composition.items():
        z_value, a_value = ELEMENT_ZA[element]
        fraction = wt_percent / total
        alpha += fraction * q_alpha_coulomb(z_value, a_value)
        surface += fraction * q_surface_binding(z_value, a_value)
    return alpha, surface, total


def derived_core_mass_fraction() -> float:
    fe_bulk = 32.0
    fe_mantle = MANTLE_COMPOSITION["Fe"]
    fe_core = CORE_COMPOSITION["Fe"]
    return (fe_bulk - fe_mantle) / (fe_core - fe_mantle)


def sinh_over_x(x_value: float) -> float:
    if abs(x_value) < 1e-6:
        return 1.0 + x_value * x_value / 6.0 + x_value**4 / 120.0
    return math.sinh(x_value) / x_value


def shell_average_kernel(inner_radius: float, outer_radius: float, lambda_m: float, steps: int = 3000) -> float:
    if math.isinf(lambda_m):
        return 1.0
    dr = (outer_radius - inner_radius) / steps
    numerator = 0.0
    denominator = (outer_radius**3 - inner_radius**3) / 3.0
    for index in range(steps):
        radius = inner_radius + (index + 0.5) * dr
        numerator += radius * radius * sinh_over_x(radius / lambda_m) * dr
    return numerator / denominator


def source_register_rows() -> list[dict[str, str]]:
    specs = [
        ("SRC1084_0_1083_next", "source-intake/mts_residuals/P8_Y5_R10_1083_NEXT_TARGET.csv", "1084-Y5-R10-DD-source-profile-weighting-or-MICROSCOPE-readout-import-gate.md", "1083 handoff."),
        ("SRC1084_1_1083_validation", "source-intake/mts_residuals/P8_Y5_BRR545_1083_VALIDATION.csv", "V1083_SUMMARY", "1083 validation summary."),
        ("SRC1084_2_1083_source_vector", "source-intake/mts_residuals/P8_Y5_R10_1083_DD_EARTH_SOURCE_VECTOR_FIRST_ROW_NONCLAIM.csv", "DD_EARTH1083_0_bulk_weighted", "bulk DD source vector candidate."),
        ("SRC1084_3_1083_products", "source-intake/mts_residuals/P8_Y5_R10_1083_DD_SOURCE_MATERIAL_PRODUCT_NONCLAIM.csv", "DD_PRODUCT1083_2_combined_abs", "source-material product nonclaim rows."),
        ("SRC1084_4_1083_caveats", "source-intake/mts_residuals/P8_Y5_R10_1083_SOURCE_VECTOR_CAVEAT_GATE.csv", "SCG1083_0_profile_weighting", "profile gate from 1083."),
        ("SRC1084_5_1083_common_mode", "source-intake/mts_residuals/P8_Y5_R10_1083_COMMON_MODE_ALTERNATIVE.csv", "CMA1083_2_verdict", "common-mode theorem remains unsigned."),
        ("SRC1084_6_1082_readout", "source-intake/mts_residuals/P8_Y5_R10_1082_PHYSICAL_MICROSCOPE_READOUT_FILL_ROWS.csv", "ROF1082_0_official_arrays", "readout arrays missing."),
        ("SRC1084_7_1081_delta", "source-intake/mts_residuals/P8_Y5_R10_1081_DD_MATERIAL_DELTA_IMPORT.csv", "DDM1081_0_delta_alpha", "test-material deltas."),
        ("SRC1084_8_local_bounds", "source-intake/local_bounds/local_bound_claims.csv", "R1_WEP_source_charge", "MICROSCOPE WEP bound row."),
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


def web_source_rows() -> list[dict[str, str]]:
    return [
        {
            "web_source_id": "WEB1084_0_PREM_IRIS",
            "role": "density/radius profile source for future weighting",
            "source_url": "https://ds.iris.edu/spud/earthmodel/10131390",
            "source_title": "Preliminary Reference Earth Model (PREM)",
            "evidence_used": "PREM radius/depth/density CSV availability and Earth radius/depth coverage",
            "extraction_status": "SOURCE_IDENTIFIED_NOT_IMPORTED",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "web_source_id": "WEB1084_1_YUKAWA_NONHOMOGENEOUS_SPHERE",
            "role": "finite-range shell-weighting kernel reference",
            "source_url": "https://arxiv.org/pdf/2507.02723",
            "source_title": "The Yukawa potential of a non-homogeneous sphere, with new limits on an ultralight boson",
            "evidence_used": "external Yukawa potential integral; hyperbolic form factor; long-range internal-structure limit",
            "extraction_status": "FORMULA_REFERENCE_ONLY_NONCLAIM",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "web_source_id": "WEB1084_2_MCDONOUGH_2003_TABLE5",
            "role": "core/mantle/bulk composition table target",
            "source_url": "https://www.mso.anu.edu.au/PSI/PSI_Meetings/Entries/2007/6/13_The_bulk_composition_of_the_Earth_%281%29_files/Treatise%20on%20Geochemistry%202003%20McDonough.pdf",
            "source_title": "Compositional Model for the Earth's Core",
            "evidence_used": "Table 5 candidate core/mantle/bulk abundant-element wt.% rows",
            "extraction_status": "MANUAL_TABLE_TARGET_CANDIDATE_NONCLAIM",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "web_source_id": "WEB1084_3_MICROSCOPE_ORBIT",
            "role": "orbit/readout context",
            "source_url": "https://comptes-rendus.academie-sciences.fr/physique/item/10.5802/crphys.24.pdf",
            "source_title": "The MICROSCOPE space mission to test the Equivalence Principle",
            "evidence_used": "710 km circular orbit context; readout arrays still not imported",
            "extraction_status": "ORBIT_CONTEXT_ONLY_NONCLAIM",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def kernel_theorem_rows() -> list[dict[str, str]]:
    return [
        {
            "kernel_id": "K1084_0_angular_integral",
            "claim": "external finite-range spherical source reduces to a radial kernel",
            "formula_or_condition": "for r>R, angular integral gives common exp(-r/lambda)/r factor times int rho(r') q(r') r'^2 sinh(r'/lambda)/(r'/lambda) dr'",
            "status": "DERIVED_AS_KERNEL_CONTRACT",
            "claim_blocker": "kernel is external DD/Yukawa profile algebra, not yet MTS parent-derived",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "kernel_id": "K1084_1_effective_source_charge",
            "claim": "profile-weighted source charge can be defined",
            "formula_or_condition": "Q_eff(lambda)=int rho q W_lambda dr / int rho W_lambda dr, W_lambda=4*pi*r^2*sinh(r/lambda)/(r/lambda)",
            "status": "DERIVED_AS_NONCLAIM_PROFILE_RULE",
            "claim_blocker": "requires lambda owner and sourced rho(r), q(r)",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "kernel_id": "K1084_2_long_range_limit",
            "claim": "bulk source vector is recovered in the long-range limit",
            "formula_or_condition": "lambda >> R_E makes sinh(r/lambda)/(r/lambda)=1+O(R_E^2/lambda^2), so Q_eff tends the mass-weighted source average",
            "status": "LONG_RANGE_LIMIT_CONDITIONALLY_DERIVED",
            "claim_blocker": "MTS has not derived that the WEP carrier range is long compared with Earth radius",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "kernel_id": "K1084_3_finite_range_profile_dependency",
            "claim": "finite-range branch is surface/profile sensitive",
            "formula_or_condition": "as lambda decreases, W_lambda favors larger r and the effective source vector tends the near-surface layer composition",
            "status": "FINITE_RANGE_PROFILE_DEPENDENCY_RETAINED",
            "claim_blocker": "no PREM/compositional shell vector and no MTS lambda_WEP selection",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "kernel_id": "K1084_4_orbit_factor",
            "claim": "710 km orbit is a common first-pass amplitude factor for a spherical source",
            "formula_or_condition": "outside-source r=R_E+h appears in the common exp(-r/lambda)/r and force derivative factor, not in Q_eff(lambda), under spherical symmetry",
            "status": "READOUT_AMPLITUDE_SEPARATED_NONCLAIM",
            "claim_blocker": "actual MICROSCOPE readout uses time-dependent gx/gz/Sxx/Sxz/masks not imported here",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def layer_composition_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for layer_id, composition in [("mantle", MANTLE_COMPOSITION), ("core", CORE_COMPOSITION)]:
        total = sum(composition.values())
        for element, wt_percent in composition.items():
            z_value, a_value = ELEMENT_ZA[element]
            rows.append(
                {
                    "layer_id": f"LAYER1084_{layer_id}_{element}",
                    "layer": layer_id,
                    "element": element,
                    "wt_percent": f"{wt_percent:.12g}",
                    "normalized_layer_mass_fraction": f"{wt_percent / total:.15e}",
                    "Z": str(z_value),
                    "A": f"{a_value:.12g}",
                    "source_table": "WEB1084_2_MCDONOUGH_2003_TABLE5",
                    "extraction_status": "TABLE5_LAYER_TARGET_CANDIDATE_NONCLAIM",
                    "valid_for_claim": "false",
                    "generated_utc": stamp(),
                }
            )
    return rows


def layer_charge_rows() -> list[dict[str, str]]:
    core_mass_fraction = derived_core_mass_fraction()
    mantle_mass_fraction = 1.0 - core_mass_fraction
    rows: list[dict[str, str]] = []
    for layer_id, composition, mass_fraction, inner_radius, outer_radius in [
        ("mantle", MANTLE_COMPOSITION, mantle_mass_fraction, CORE_RADIUS_M, EARTH_RADIUS_M),
        ("core", CORE_COMPOSITION, core_mass_fraction, 0.0, CORE_RADIUS_M),
    ]:
        alpha, surface, total = composition_charge(composition)
        rows.append(
            {
                "layer_charge_id": f"LC1084_{layer_id}",
                "layer": layer_id,
                "inner_radius_m": f"{inner_radius:.6e}",
                "outer_radius_m": f"{outer_radius:.6e}",
                "mass_fraction_candidate": f"{mass_fraction:.15e}",
                "composition_sum_wt_percent": f"{total:.12g}",
                "Q_alpha_Coulomb_layer": f"{alpha:.15e}",
                "Q_surface_binding_layer": f"{surface:.15e}",
                "mass_fraction_source": "derived from Table5 Fe mass balance: Fe_bulk=f_mantle*Fe_mantle+f_core*Fe_core",
                "status": "NUMERIC_TWO_LAYER_DD_CHARGE_NONCLAIM",
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def profile_weighting_grid_rows() -> list[dict[str, str]]:
    layer_rows = layer_charge_rows()
    mantle = next(row for row in layer_rows if row["layer"] == "mantle")
    core = next(row for row in layer_rows if row["layer"] == "core")
    source_1083 = read_csv(OUT / "P8_Y5_R10_1083_DD_EARTH_SOURCE_VECTOR_FIRST_ROW_NONCLAIM.csv")[0]
    bulk_alpha = float(source_1083["Q_alpha_Coulomb_Earth"])
    bulk_surface = float(source_1083["Q_surface_binding_Earth"])
    grid: list[tuple[str, float]] = [
        ("long_range_mass_average", math.inf),
        ("lambda_over_RE_100", 100.0 * EARTH_RADIUS_M),
        ("lambda_over_RE_10", 10.0 * EARTH_RADIUS_M),
        ("lambda_over_RE_1", EARTH_RADIUS_M),
        ("lambda_over_RE_0p3", 0.3 * EARTH_RADIUS_M),
        ("lambda_over_RE_0p1", 0.1 * EARTH_RADIUS_M),
        ("lambda_over_RE_0p03", 0.03 * EARTH_RADIUS_M),
    ]
    rows: list[dict[str, str]] = []
    for grid_id, lambda_m in grid:
        layer_data = []
        for row in [mantle, core]:
            if row["layer"] == "mantle":
                mean_kernel = shell_average_kernel(CORE_RADIUS_M, EARTH_RADIUS_M, lambda_m)
            else:
                mean_kernel = shell_average_kernel(0.0, CORE_RADIUS_M, lambda_m)
            layer_data.append(
                {
                    "layer": row["layer"],
                    "mass_fraction": float(row["mass_fraction_candidate"]),
                    "mean_kernel": mean_kernel,
                    "alpha": float(row["Q_alpha_Coulomb_layer"]),
                    "surface": float(row["Q_surface_binding_layer"]),
                }
            )
        denominator = sum(item["mass_fraction"] * item["mean_kernel"] for item in layer_data)
        q_alpha = sum(item["mass_fraction"] * item["mean_kernel"] * item["alpha"] for item in layer_data) / denominator
        q_surface = sum(item["mass_fraction"] * item["mean_kernel"] * item["surface"] for item in layer_data) / denominator
        rows.append(
            {
                "profile_row_id": f"PROFILE1084_{grid_id}",
                "lambda_label": grid_id,
                "lambda_m": "inf" if math.isinf(lambda_m) else f"{lambda_m:.15e}",
                "lambda_over_R_E": "inf" if math.isinf(lambda_m) else f"{lambda_m / EARTH_RADIUS_M:.15e}",
                "mantle_kernel_mean": f"{layer_data[0]['mean_kernel']:.15e}",
                "core_kernel_mean": f"{layer_data[1]['mean_kernel']:.15e}",
                "Q_alpha_Coulomb_eff": f"{q_alpha:.15e}",
                "Q_surface_binding_eff": f"{q_surface:.15e}",
                "delta_alpha_vs_1083_bulk": f"{q_alpha - bulk_alpha:.15e}",
                "delta_surface_vs_1083_bulk": f"{q_surface - bulk_surface:.15e}",
                "profile_model": "two_layer_uniform_core_mantle_candidate",
                "status": "NUMERIC_PROFILE_WEIGHTING_SMOKE_NONCLAIM",
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def profile_closure_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "PCG1084_0_long_range_bulk_limit",
            "claim_component": "bulk source vector suffices",
            "gate_pass": "conditional",
            "condition": "derive lambda_WEP >> R_E or massless/common long-range source carrier from parent action",
            "current_status": "CONDITION_NOT_PARENT_SIGNED",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "PCG1084_1_finite_range_profile",
            "claim_component": "finite-range source profile vector",
            "gate_pass": "false",
            "condition": "import PREM density plus shell composition profile and choose lambda_WEP",
            "current_status": "MISSING_PREM_IMPORT_AND_LAMBDA_OWNER",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "PCG1084_2_source_charge_basis",
            "claim_component": "DD profile vector is an MTS source vector",
            "gate_pass": "false",
            "condition": "derive parent-to-DD coefficient/source basis map",
            "current_status": "PARENT_TO_DD_MAP_NOT_DERIVED",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def readout_import_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "readout_id": "RIG1084_0_CMSM_arrays",
            "needed_object": "official MICROSCOPE CMSM/export arrays",
            "required_content": "time, segment/session id, gx, gz, Sxx, Sxz, masks, calibration flags, attitude/orbit convention",
            "current_status": "OFFICIAL_ARRAYS_NOT_IMPORTED",
            "claim_blocker": "unit or surrogate readout cannot become physical tau_WEP",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "readout_id": "RIG1084_1_product_convention",
            "needed_object": "eta_AB product normalization",
            "required_content": "map from source response x material response x readout kernel to reported Eotvos eta",
            "current_status": "NORMALIZATION_NOT_FILLED",
            "claim_blocker": "numeric profile products are scale probes only",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "readout_id": "RIG1084_2_surrogate_limit",
            "needed_object": "surrogate design matrix relation to official readout",
            "required_content": "proof surrogate kernel has same units/normalization as official arrays",
            "current_status": "SURROGATE_AVAILABLE_NONCLAIM",
            "claim_blocker": "cannot replace official readout for a WEP claim",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def prediction_rows() -> list[dict[str, str]]:
    return [
        {
            "prediction_id": "PRED1084_0_profile_weighted_DD_source_nonclaim",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "P_WEP_relative_source_weight",
            "product_value": "MISSING_LAMBDA_WEP_PARENT_TO_DD_MAP_AND_OFFICIAL_READOUT",
            "product_units": "dimensionless",
            "product_source": "source-intake/mts_residuals/P8_Y5_R10_1084_SOURCE_PROFILE_WEIGHTING_GRID_NONCLAIM.csv",
            "inputs_present": "two-layer DD source profile smoke grid; bulk DD source vector; DD material deltas; MICROSCOPE bound",
            "required_inputs": "lambda_WEP owner; PREM/shell composition import; parent-to-DD map; official MICROSCOPE readout normalization",
            "derivation_status": "PROFILE_RULE_DERIVED_BUT_PHYSICAL_PRODUCT_MISSING",
            "valid_for_claim": "false",
            "notes": "runner must refuse; profile grid only says when bulk approximation is conditionally safe",
        }
    ]


def bound_import_rows() -> list[dict[str, str]]:
    return [
        {
            "bound_id": "BOUND1084_0_MICROSCOPE_WEP_source_charge",
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
            "runner_id": "APR1084_0_profile_weighted_product_stub",
            "prediction_rows": str(product_status.get("prediction_rows", "")),
            "bound_rows": str(product_status.get("bound_rows", "")),
            "valid_prediction_rows": str(product_status.get("valid_prediction_rows", "")),
            "valid_bound_rows": str(product_status.get("valid_bound_rows", "")),
            "comparison_rows": str(product_status.get("comparison_rows", "")),
            "passed_rows": str(product_status.get("passed_rows", "")),
            "claim_allowed": str(product_status.get("claim_allowed", "")).lower(),
            "expected_result": "reject missing lambda_WEP, parent-to-DD map, and official readout",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def claim_gate_rows(product_status: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "gate_id": "CG1084_0_profile_rule",
            "claim_component": "source-profile rule",
            "gate_pass": "conditional",
            "claim_allowed": "false",
            "reason": "radial kernel rule derived as external DD/Yukawa algebra, but physical source needs lambda/profile",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1084_1_long_range_bulk",
            "claim_component": "bulk source vector suffices",
            "gate_pass": "conditional",
            "claim_allowed": "false",
            "reason": "requires parent-signed lambda_WEP >> R_E or massless common carrier",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1084_2_parent_to_DD",
            "claim_component": "MTS parent-to-DD map",
            "gate_pass": "false",
            "claim_allowed": "false",
            "reason": "still not derived",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1084_3_readout",
            "claim_component": "MICROSCOPE official readout",
            "gate_pass": "false",
            "claim_allowed": "false",
            "reason": "CMSM/export arrays and eta normalization not imported",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1084_4_product_runner",
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
            "decision_id": "DECISION1084_0",
            "decision": "source-profile algebra is now explicit",
            "because": "finite-range spherical source weighting reduces to a hyperbolic radial kernel and has a clean long-range bulk limit",
            "next_action": "derive lambda_WEP from parent action before using either bulk or finite-range profile rows as physical",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DECISION1084_1",
            "decision": "MICROSCOPE readout import remains a separate hard gate",
            "because": "710 km orbit and spherical source profile do not substitute for gx/gz/Sxx/Sxz/masks/timing/product normalization",
            "next_action": "either acquire official arrays or continue parent-side derivation of the coefficient/range owner",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_id": "NEXT1084_0_1085",
            "next_target": "1085-Y5-R10-WEP-range-owner-or-long-range-limit-theorem.md",
            "objective": "derive whether the local WEP carrier/source response is long range enough for the bulk Earth vector, or retain lambda-dependent profile rows and route to PREM/readout import; do not claim WEP/local-GR",
            "include": "parent mass/range operator; lambda_WEP >> R_E condition; relation to R10 lambda; parent-to-DD coefficient pressure point; readout import fallback",
            "exclude": "measured-G absorption; unit source proxy; DD profile smoke as MTS claim; GitHub; formalization edits",
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
    kernel_rows: list[dict[str, str]],
    layer_comp_rows: list[dict[str, str]],
    layer_charge_rows_: list[dict[str, str]],
    profile_rows: list[dict[str, str]],
    closure_rows: list[dict[str, str]],
    readout_rows: list[dict[str, str]],
    prediction_rows_: list[dict[str, str]],
    bound_rows_: list[dict[str, str]],
    product_status: dict[str, Any],
    claim_rows: list[dict[str, str]],
    next_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    checks: list[tuple[str, bool, str]] = []
    checks.append(("V1084_0_local_sources_exist", all(row["exists"] == "true" and row["needle_found"] == "true" for row in source_rows), "all cited local source paths and needles are present"))
    checks.append(("V1084_1_web_sources_recorded", len(web_rows) == 4 and all(row["source_url"].startswith("https://") and row["valid_for_claim"] == "false" for row in web_rows), "web source urls/provenance are recorded as nonclaim"))
    checks.append(("V1084_2_kernel_contract", {row["kernel_id"] for row in kernel_rows} >= {"K1084_1_effective_source_charge", "K1084_2_long_range_limit", "K1084_3_finite_range_profile_dependency"}, "profile kernel and long-range/finite-range rules are explicit"))
    checks.append(("V1084_3_layer_composition_numeric", len(layer_comp_rows) == 18 and all(parse_float(row["normalized_layer_mass_fraction"]) is not None for row in layer_comp_rows), "core/mantle composition candidate rows are numeric"))
    checks.append(("V1084_4_layer_charges_numeric", len(layer_charge_rows_) == 2 and all(parse_float(row["Q_alpha_Coulomb_layer"]) is not None and parse_float(row["Q_surface_binding_layer"]) is not None for row in layer_charge_rows_), "core/mantle DD charges are numeric"))
    checks.append(("V1084_5_profile_grid_numeric_nonclaim", len(profile_rows) >= 7 and all(parse_float(row["Q_alpha_Coulomb_eff"]) is not None and row["valid_for_claim"] == "false" for row in profile_rows), "profile weighting grid is numeric and nonclaim"))
    checks.append(("V1084_6_profile_gates_block_claim", len(closure_rows) == 3 and all(row["valid_for_claim"] == "false" for row in closure_rows), "profile closure gates retain lambda/profile/parent blockers"))
    checks.append(("V1084_7_readout_gate_blocks_claim", len(readout_rows) == 3 and all(row["valid_for_claim"] == "false" for row in readout_rows), "readout import gates remain nonclaim"))
    checks.append(("V1084_8_prediction_missing_nonclaim", any("MISSING_LAMBDA_WEP" in row["product_value"] and row["valid_for_claim"] == "false" for row in prediction_rows_), "generic prediction row remains missing lambda/parent/readout inputs"))
    checks.append(("V1084_9_bound_numeric", bool(bound_rows_) and parse_float(bound_rows_[0]["bound_value"]) is not None and float(bound_rows_[0]["bound_value"]) > 0 and bound_rows_[0]["valid_for_claim"] == "true", "MICROSCOPE bound import is positive numeric"))
    checks.append(("V1084_10_product_runner_refuses", product_status.get("valid_prediction_rows") == 0 and product_status.get("claim_allowed") is False, "generic product runner reports no valid prediction rows and claim false"))
    checks.append(("V1084_11_claim_gates_safe", claim_rows and all(row["claim_allowed"] == "false" for row in claim_rows), "all claim gates deny WEP/local-GR claim"))
    checks.append(("V1084_12_next_target", any(row["next_target"].startswith("1085-Y5-R10-WEP-range-owner") for row in next_rows), "1085 handoff written"))
    generated_paths = list(outputs.values()) + [DOC]
    checks.append(("V1084_13_generated_under_post_checkpoint", all(str(path.resolve()).startswith(str(ROOT.resolve())) for path in generated_paths), "all generated outputs are under post-checkpoint-work"))
    checks.append(("V1084_14_csv_parse", csv_outputs_parse([path for key, path in outputs.items() if key != "validation"]), "all 1084 CSV outputs parse cleanly"))
    checks.append(("V1084_15_formalization_untouched", count_formalization_modified_since_start() == 0, "formalization-workbench modified-file count remains zero"))
    checks.append(("V1084_SUMMARY", True, "finite-range source-profile kernel derived as nonclaim; long-range bulk limit conditional; lambda/readout/parent gates remain closed"))
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
    kernel_rows: list[dict[str, str]],
    layer_comp_rows: list[dict[str, str]],
    layer_charge_rows_: list[dict[str, str]],
    profile_rows: list[dict[str, str]],
    closure_rows: list[dict[str, str]],
    readout_rows: list[dict[str, str]],
    product_status_rows_: list[dict[str, str]],
    product_comparisons: list[dict[str, Any]],
    claim_rows: list[dict[str, str]],
    decisions: list[dict[str, str]],
    validation_rows: list[dict[str, str]],
    next_rows: list[dict[str, str]],
) -> None:
    text = "\n".join(
        [
            "# 1084-Y5-R10 DD source-profile weighting or MICROSCOPE readout import gate",
            "",
            "## Current verdict",
            "1084 gets a real derivation step: for a finite-range spherical source, the Earth source vector is not automatically the bulk vector; it is a radial-kernel weighted charge vector. The bulk source vector is recovered only in the long-range limit lambda_WEP >> R_E. Since MTS has not yet derived lambda_WEP, the parent-to-DD map, or the official MICROSCOPE readout normalization, the branch remains nonclaim.",
            "",
            "## Local source register",
            md_table(source_rows, ["source_id", "relative_path", "exists", "needle_found", "note"]),
            "## Web source register",
            md_table(web_rows, ["web_source_id", "role", "source_url", "extraction_status"]),
            "## Kernel derivation ledger",
            md_table(kernel_rows, ["kernel_id", "claim", "formula_or_condition", "status", "claim_blocker"]),
            "## Core/mantle composition candidate",
            md_table(layer_comp_rows, ["layer_id", "layer", "element", "wt_percent", "normalized_layer_mass_fraction", "extraction_status"]),
            "## Core/mantle DD charge vectors",
            md_table(layer_charge_rows_, ["layer_charge_id", "layer", "mass_fraction_candidate", "Q_alpha_Coulomb_layer", "Q_surface_binding_layer", "status"]),
            "## Source-profile weighting grid",
            md_table(profile_rows, ["profile_row_id", "lambda_over_R_E", "Q_alpha_Coulomb_eff", "Q_surface_binding_eff", "delta_alpha_vs_1083_bulk", "delta_surface_vs_1083_bulk", "status"]),
            "## Profile closure gates",
            md_table(closure_rows, ["gate_id", "claim_component", "gate_pass", "condition", "current_status"]),
            "## MICROSCOPE readout import gate",
            md_table(readout_rows, ["readout_id", "needed_object", "required_content", "current_status", "claim_blocker"]),
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
    web_rows = web_source_rows()
    kernel_rows = kernel_theorem_rows()
    layer_comp_rows = layer_composition_rows()
    layer_charge_rows_ = layer_charge_rows()
    profile_rows = profile_weighting_grid_rows()
    closure_rows = profile_closure_gate_rows()
    readout_rows = readout_import_gate_rows()
    prediction_rows_ = prediction_rows()
    bound_rows_ = bound_import_rows()
    next_rows = next_target_rows()

    outputs = {
        "source_register": OUT / "P8_Y5_R10_1084_SOURCE_REGISTER.csv",
        "web_source_register": OUT / "P8_Y5_R10_1084_WEB_SOURCE_REGISTER.csv",
        "kernel_ledger": OUT / "P8_Y5_R10_1084_SOURCE_PROFILE_KERNEL_DERIVATION_LEDGER.csv",
        "layer_composition": OUT / "P8_Y5_R10_1084_CORE_MANTLE_COMPOSITION_CANDIDATE.csv",
        "layer_charge": OUT / "P8_Y5_R10_1084_CORE_MANTLE_DD_CHARGE_VECTORS.csv",
        "profile_grid": OUT / "P8_Y5_R10_1084_SOURCE_PROFILE_WEIGHTING_GRID_NONCLAIM.csv",
        "profile_gates": OUT / "P8_Y5_R10_1084_PROFILE_CLOSURE_GATES.csv",
        "readout_import_gate": OUT / "P8_Y5_R10_1084_MICROSCOPE_READOUT_IMPORT_GATE.csv",
        "prediction": PREDICTION_TEMPLATE,
        "bound": BOUND_IMPORT,
        "product_status": OUT / "P8_Y5_R10_1084_PRODUCT_RUNNER_STATUS.csv",
        "product_comparison": OUT / "P8_Y5_R10_1084_PRODUCT_COMPARISON_ROWS.csv",
        "claim_gates": OUT / "P8_Y5_R10_1084_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_R10_1084_DECISION_LEDGER.csv",
        "next_target": OUT / "P8_Y5_R10_1084_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_1084_VALIDATION.csv",
    }

    write_csv(outputs["source_register"], source_rows)
    write_csv(outputs["web_source_register"], web_rows)
    write_csv(outputs["kernel_ledger"], kernel_rows)
    write_csv(outputs["layer_composition"], layer_comp_rows)
    write_csv(outputs["layer_charge"], layer_charge_rows_)
    write_csv(outputs["profile_grid"], profile_rows)
    write_csv(outputs["profile_gates"], closure_rows)
    write_csv(outputs["readout_import_gate"], readout_rows)
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
        kernel_rows,
        layer_comp_rows,
        layer_charge_rows_,
        profile_rows,
        closure_rows,
        readout_rows,
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
        kernel_rows,
        layer_comp_rows,
        layer_charge_rows_,
        profile_rows,
        closure_rows,
        readout_rows,
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
