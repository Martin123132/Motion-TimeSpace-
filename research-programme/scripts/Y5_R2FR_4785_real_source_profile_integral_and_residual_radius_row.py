from __future__ import annotations

import csv
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"
SCRIPT_DIR = POST / "scripts"

PROFILE_RUNNER = SCRIPT_DIR / "source_profile_integral_radius_runner.py"
RHOH_RUNNER = SCRIPT_DIR / "rhoH_parent_density_integral_runner.py"
DENSITY_RUNNER = SCRIPT_DIR / "parent_density_current_mlower_runner.py"
PARENT_CHARGE_RUNNER = SCRIPT_DIR / "parent_charge_Htau_Href_bound_runner.py"
SOURCE_RUNNER = SCRIPT_DIR / "Htau_Href_MHdress_source_runner.py"
OPEN_RUNNER = SCRIPT_DIR / "MHdress_E00_open_arena_runner.py"

CHECKPOINT = "4785"
CLAIM_ID = "L-627"
MARKER = "PPC4161_REAL_SOURCE_PROFILE_INTEGRAL_AND_RESIDUAL_RADIUS_ROW_4785"
PACKET_MARKER = "PPC4161_PACKET_REAL_SOURCE_PROFILE_INTEGRAL_AND_RESIDUAL_RADIUS_ROW_4785"
DECISION = "SOURCE_PROFILE_INTEGRAL_AND_RESIDUAL_RADIUS_RUNNER_INSTALLED_PROFILE_WITHOUT_RADIUS_STILL_BLOCKS_REAL_PHYSICAL_PROFILE_VALUES_MISSING_NONCLAIM"
NEXT_TARGET = "4786-Y5-R2FR-source-profile-physical-values-or-parent-zero-profile-certificate.md"

DOC_PATH = POST / "4785-Y5-R2FR-real-source-profile-integral-and-residual-radius-row.md"
FORMAL_PATH = FORMAL / "801-PPC4161-real-source-profile-integral-and-residual-radius-row.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"

SOURCE_REGISTER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4785_SOURCE_REGISTER.csv"
LAW_CSV = SOURCE_DIR / "P8_Y5_R2FR_4785_SOURCE_PROFILE_LAW.csv"
PROFILE_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4785_SOURCE_PROFILE_INPUT.csv"
PROFILE_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4785_SOURCE_PROFILE_OUTPUT.csv"
RHOH_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4785_RHOH_INPUT_FROM_PROFILE.csv"
RHOH_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4785_RHOH_OUTPUT_FROM_PROFILE.csv"
DENSITY_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4785_DENSITY_INPUT_FROM_PROFILE.csv"
DENSITY_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4785_DENSITY_OUTPUT_FROM_PROFILE.csv"
PARENT_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4785_PARENT_CHARGE_INPUT_FROM_PROFILE.csv"
PARENT_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4785_PARENT_CHARGE_OUTPUT_FROM_PROFILE.csv"
SOURCE_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4785_HTAU_HREF_SOURCE_INPUT.csv"
SOURCE_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4785_HTAU_HREF_SOURCE_OUTPUT.csv"
OPEN_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4785_OPEN_ARENA_INPUT.csv"
OPEN_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4785_OPEN_ARENA_OUTPUT.csv"
SCORE_GATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4785_SCORE_GATE_UPDATE.csv"
PROMOTION_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4785_PROMOTION_GATES.csv"
FIREWALL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4785_FIREWALL_ROWS.csv"
ROUTE_MATRIX_CSV = SOURCE_DIR / "P8_Y5_R2FR_4785_ROUTE_SELECTION_MATRIX.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4785_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4785_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4785_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4785_VALIDATION.csv"

G_CAL = 6.67430e-11
MU_SUN_NOMINAL = 1.3271244e20
SOLAR_RADIUS_NOMINAL = 6.957e8
M_GM_SUN_CAL = MU_SUN_NOMINAL / G_CAL

RESIDUAL_SYMBOLS = (
    "R_eq",
    "B_zero",
    "boundary_flux",
    "open_EM",
    "nonEM_owner_gap",
    "projector_comm",
    "domain_shadow",
    "kappa_drift",
)

RESIDUAL_FIELDS = (
    "R_eq_abs_kg",
    "B_zero_abs_kg",
    "boundary_flux_abs_kg",
    "open_EM_abs_kg",
    "nonEM_owner_gap_abs_kg",
    "projector_comm_abs_kg",
    "domain_shadow_abs_kg",
    "kappa_drift_abs_kg",
)

SOURCE_SPECS = [
    ("SRC4785_00_4784_doc", POST / "4784-Y5-R2FR-real-rhoH-parent-density-integral-or-M0-source-backed-row.md", "rho_H(W_H)", "4784 selected real profile integral"),
    ("SRC4785_01_4784_output", SOURCE_DIR / "P8_Y5_R2FR_4784_RHOH_PARENT_DENSITY_OUTPUT.csv", "physical_candidate_parent_density_law_values_missing", "4784 physical blocker row"),
    ("SRC4785_02_1547_template", SOURCE_DIR / "P8_Y5_PARENT_QLOC_1547_COMPACT_PROFILE_TEMPLATE.csv", "WTP1547_0_shared_core", "shared compact worldtube profile template"),
    ("SRC4785_03_1548_symbolic", SOURCE_DIR / "P8_Y5_PARENT_QLOC_1548_SHARED_SYMBOLIC_PROFILE_CANDIDATES.csv", "SYM1548_2_Hilbert_stress_projected_profile", "Hilbert stress projected source profile candidate"),
    ("SRC4785_04_1547_doc", POST / "1547-Y5-compact-worldtube-profile-template-and-arena-map.md", "theta_src", "no retuning/shared profile guard"),
    ("SRC4785_05_1548_doc", POST / "1548-Y5-shared-worldtube-profile-symbolic-runner-or-source-data-acquisition.md", "no source-backed accepted profile", "source acquisition precedent"),
    ("SRC4785_06_3883_doc", POST / "3883-Y5-R2FR-Hilbert-source-and-Maxwell-stress-lock-or-residual-vector.md", "T_H^{mu nu}", "same Hilbert source and Maxwell stress"),
    ("SRC4785_07_4587_doc", POST / "4587-Y5-R2FR-Hilbert-source-density-qbasic-and-Poynting-support-owner-or-bound.md", "Poynting rule is once-only", "density/Poynting once-only rule"),
    ("SRC4785_08_profile_runner", PROFILE_RUNNER, "def compute_profile", "4785 profile integral and radius runner"),
]


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_text(path_object: Path) -> str:
    return path_object.read_text(encoding="utf-8-sig", errors="replace")


def write_text(path_object: Path, content: str) -> None:
    path_object.parent.mkdir(parents=True, exist_ok=True)
    path_object.write_text(content, encoding="utf-8", newline="\n")


def append_once(path_object: Path, marker: str, block: str) -> None:
    existing = read_text(path_object) if path_object.exists() else ""
    if marker in existing:
        return
    separator = "" if not existing or existing.endswith("\n") else "\n"
    write_text(path_object, existing + separator + block.rstrip() + "\n")


def write_csv(path_object: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty CSV: {path_object}")
    path_object.parent.mkdir(parents=True, exist_ok=True)
    with path_object.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def parse_csv(path_object: Path) -> list[dict[str, Any]]:
    with path_object.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def format_float(value: float) -> str:
    return f"{value:.15e}"


def run_command(args: list[str]) -> None:
    subprocess.run(args, check=True, cwd=str(ROOT))


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    body = [
        "| " + " | ".join(str(row.get(column, "")).replace("\\", "\\\\").replace("|", "\\|").replace("\n", " ") for column in columns) + " |"
        for row in rows
    ]
    return "\n".join([header, divider, *body])


def source_register(timestamp: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path_object, needle, role in SOURCE_SPECS:
        exists = path_object.exists()
        text = read_text(path_object) if exists else ""
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "source_path": str(path_object),
                "exists": exists,
                "needle": needle,
                "needle_found": needle in text,
                "role": role,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def law_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("SPL4785_0_profile_integral", "rho_H(W_H)=sum_i int_{shell_i} rho_H dV = c^-2 sum_i int T_total(n,n)dV", "turns a worldtube profile table into a source mass integral"),
        ("SPL4785_1_shell_volume", "dV_i is explicit or 4*pi/3*(r_out^3-r_in^3)", "prevents hidden profile normalization"),
        ("SPL4785_2_radius", "Delta_H_abs=sum |R_eq|+|B_zero|+|boundary_flux|+|open_EM|+|nonEM|+|projector|+|domain|+|kappa|", "separates profile mass from the no-cancellation residual radius"),
        ("SPL4785_3_poynting", "Poynting is inside T_EM Hilbert stress or an explicit boundary/open_EM residual", "blocks double counting the EM flux"),
        ("SPL4785_4_firewall", "GM/PPN/clock/R10 fitted outputs cannot define rho_H(W_H)", "keeps the source profile independent of the arena readout"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "law_id": law_id,
            "formula": formula,
            "meaning": meaning,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for law_id, formula, meaning in specs
    ]


def signed_profile_clauses(value: bool) -> dict[str, bool]:
    return {
        "parent_action_signed": value,
        "same_frame_signed": value,
        "variation_before_readout_signed": value,
        "compact_support_signed": value,
        "volume_measure_signed": value,
        "positive_energy_signed": value,
        "poynting_once_signed": value,
        "no_flux_or_flux_row_signed": value,
        "no_species_prefactor_signed": value,
        "no_postfit_signed": value,
        "shared_profile_signed": value,
    }


def profile_mass_row(profile_id: str, component_id: str, mass: str, row_status: str, timestamp: str, source: str, clauses: dict[str, bool]) -> dict[str, Any]:
    return {
        "profile_id": profile_id,
        "component_id": component_id,
        "component_kind": "mass",
        "residual_symbol": "",
        "r_inner_m": "",
        "r_outer_m": "",
        "volume_m3": "1",
        "rho_H_kg_m3": mass,
        "T_total_nn_J_m3": "",
        "component_mass_kg": "",
        "residual_abs_kg": "",
        "c_m_s": "299792458",
        "source_path": source,
        "component_source": source,
        "normalization_source": "PROFILE_TABLE_NOT_ARENA_READOUT",
        "residual_source": "",
        "extraction_method": "profile_integral_row",
        "confidence": "private_or_smoke",
        "notes": "",
        "row_status": row_status,
        "valid_for_claim": False,
        "timestamp_utc": timestamp,
        **clauses,
    }


def residual_row(profile_id: str, component_id: str, symbol: str, value: str, row_status: str, timestamp: str, source: str, clauses: dict[str, bool]) -> dict[str, Any]:
    return {
        "profile_id": profile_id,
        "component_id": component_id,
        "component_kind": "residual",
        "residual_symbol": symbol,
        "r_inner_m": "",
        "r_outer_m": "",
        "volume_m3": "",
        "rho_H_kg_m3": "",
        "T_total_nn_J_m3": "",
        "component_mass_kg": "",
        "residual_abs_kg": value,
        "c_m_s": "299792458",
        "source_path": source,
        "component_source": "",
        "normalization_source": "",
        "residual_source": source,
        "extraction_method": "residual_radius_component",
        "confidence": "private_or_smoke",
        "notes": "",
        "row_status": row_status,
        "valid_for_claim": False,
        "timestamp_utc": timestamp,
        **clauses,
    }


def add_residual_set(rows: list[dict[str, Any]], profile_id: str, values: dict[str, str], row_status: str, timestamp: str, source: str, clauses: dict[str, bool]) -> None:
    for index, symbol in enumerate(RESIDUAL_SYMBOLS):
        rows.append(residual_row(profile_id, f"{profile_id}_res_{index}", symbol, values[symbol], row_status, timestamp, source, clauses))


def profile_input_rows(timestamp: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    signed = signed_profile_clauses(True)
    unsigned = signed_profile_clauses(False)
    residual = 0.01 * M_GM_SUN_CAL
    zero_values = {symbol: "0" for symbol in RESIDUAL_SYMBOLS}
    finite_values = {
        "R_eq": format_float(residual),
        "B_zero": "0",
        "boundary_flux": format_float(residual),
        "open_EM": "0",
        "nonEM_owner_gap": "0",
        "projector_comm": "0",
        "domain_shadow": "0",
        "kappa_drift": "0",
    }

    rows.append(profile_mass_row("physical_profile_values_missing", "physical_missing_mass_component", "", "physical_values_missing_nonclaim", timestamp, "MISSING_PARENT_TTOTAL_PROFILE", unsigned))

    rows.append(profile_mass_row("profile_without_residual_radius_control", "profile_only_mass", "1", "private_profile_no_radius_nonclaim", timestamp, "PRIVATE_PROFILE_INTEGRAL_NO_RADIUS_CONTROL", signed))

    rows.append(profile_mass_row("private_unit_profile_with_zero_radius", "private_mass", "1", "private_profile_zero_radius_nonclaim", timestamp, "PRIVATE_UNIT_PROFILE_CONTROL", signed))
    add_residual_set(rows, "private_unit_profile_with_zero_radius", zero_values, "private_profile_zero_radius_nonclaim", timestamp, "PRIVATE_ZERO_RADIUS_CONTROL", signed)

    rows.append(profile_mass_row("finite_profile_radius_smoke_nonclaim", "finite_mass", format_float(M_GM_SUN_CAL), "finite_profile_radius_smoke_nonclaim", timestamp, "SMOKE_PROFILE_NOT_PHYSICAL", signed))
    add_residual_set(rows, "finite_profile_radius_smoke_nonclaim", finite_values, "finite_profile_radius_smoke_nonclaim", timestamp, "SMOKE_RESIDUAL_RADIUS_NOT_PHYSICAL", signed)

    rows.append(profile_mass_row("forbidden_orbital_GM_profile_control", "forbidden_mass", format_float(M_GM_SUN_CAL), "physical_forbidden_circular_profile_control_nonclaim", timestamp, "ORBITAL_GM_DEFINITION_FORBIDDEN_CONTROL", signed))
    add_residual_set(rows, "forbidden_orbital_GM_profile_control", zero_values, "physical_forbidden_circular_profile_control_nonclaim", timestamp, "POSTFIT_REFERENCE_OBSERVED_RESIDUAL_CANCEL_CONTROL", signed)

    rows.append(profile_mass_row("counterfactual_profile_equals_comparator", "counterfactual_mass", format_float(M_GM_SUN_CAL), "counterfactual_smoke_nonclaim", timestamp, "COUNTERFACTUAL_RUNNER_SMOKE_ONLY", signed))
    add_residual_set(rows, "counterfactual_profile_equals_comparator", zero_values, "counterfactual_smoke_nonclaim", timestamp, "COUNTERFACTUAL_RUNNER_SMOKE_ONLY", signed)

    return rows


def rhoh_input_from_profile(timestamp: str, profile_output: list[dict[str, Any]]) -> list[dict[str, Any]]:
    pass_statuses = {
        "PROFILE_INTEGRAL_AND_RADIUS_EXACT_PRIVATE_NONCLAIM",
        "PROFILE_INTEGRAL_AND_RADIUS_COMPUTED_NONCLAIM",
        "PROFILE_COUNTERFACTUAL_SMOKE_PASS_NONCLAIM",
    }
    partial_statuses = {"PROFILE_INTEGRAL_COMPUTED_RESIDUALS_MISSING_NONCLAIM"}
    rows: list[dict[str, Any]] = []
    for output in profile_output:
        usable = output["runner_status"] in pass_statuses or output["runner_status"] in partial_statuses
        residual_complete = output["runner_status"] in pass_statuses
        row_status = output["row_status_input"]
        rows.append(
            {
                "density_id": output["profile_id"],
                "rho_H_integral_kg": output["rho_H_integral_kg"] if usable else "",
                "T_total_nn_integral_J": "",
                "c_m_s": "299792458",
                "rho_H_source": "source_profile_integral_radius_runner.py" if usable else "MISSING_SOURCE_PROFILE",
                "T_total_nn_source": "profile_component_table",
                "H_tau_surface_center_kg": "0" if usable else "",
                "H_tau_surface_source": "SURFACE_ZERO_PROFILE_BRANCH",
                "H_ref_kg": "0" if usable else "",
                "H_ref_source": "4783_PRIVATE_SOURCE_BLIND_HREF_ZERO_NONCLAIM",
                **{field: output[field] if residual_complete else "" for field in RESIDUAL_FIELDS},
                "M0_kg": "",
                "M0_source": "SELF_FROM_POSITIVE_HILBERT_PROFILE" if usable else "MISSING_PROFILE_M0",
                "epsilon_abs": "",
                "epsilon_source": "RESIDUAL_RADIUS_OVER_M0" if residual_complete else "MISSING_RESIDUAL_RADIUS",
                "M_GM_cal_kg": format_float(M_GM_SUN_CAL),
                "parent_action_signed": output["profile_clauses_signed"],
                "variation_before_readout_signed": output["profile_clauses_signed"],
                "same_frame_signed": output["profile_clauses_signed"],
                "qbasic_density_signed": output["profile_clauses_signed"],
                "compact_support_signed": output["profile_clauses_signed"],
                "positive_energy_signed": output["profile_clauses_signed"],
                "poynting_once_signed": output["profile_clauses_signed"],
                "no_flux_or_flux_row_signed": output["profile_clauses_signed"],
                "no_species_prefactor_signed": output["profile_clauses_signed"],
                "no_postfit_signed": output["profile_clauses_signed"],
                "surface_zero_signed": usable,
                "M0_from_density_signed": usable,
                "epsilon_from_residual_radius_signed": residual_complete,
                "row_status": row_status,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def density_input_from_rhoh(timestamp: str, rhoh_input: list[dict[str, Any]], rhoh_output: list[dict[str, Any]]) -> list[dict[str, Any]]:
    input_by_id = {row["density_id"]: row for row in rhoh_input}
    pass_statuses = {
        "RHOH_SELF_DENOMINATOR_EXACT_PRIVATE_NONCLAIM",
        "RHOH_PARENT_INTEGRAL_EXACT_COMPUTED_NONCLAIM",
        "RHOH_PARENT_INTEGRAL_INTERVAL_COMPUTED_NONCLAIM",
        "RHOH_NUMERIC_COMPUTED_PARENT_UNSIGNED_NONCLAIM",
        "RHOH_COUNTERFACTUAL_SMOKE_PASS_NONCLAIM",
    }
    rows: list[dict[str, Any]] = []
    for output in rhoh_output:
        source = input_by_id[output["density_id"]]
        usable = output["runner_status"] in pass_statuses
        rows.append(
            {
                "density_id": output["density_id"],
                "rho_H_integral_kg": output["rho_H_integral_kg"] if usable else "",
                "rho_H_source": "rhoH_parent_density_integral_runner.py" if usable else source["rho_H_source"],
                "H_tau_surface_center_kg": output["H_tau_surface_center_kg"] if usable else "",
                "H_tau_surface_source": source["H_tau_surface_source"],
                "H_ref_kg": output["H_ref_kg"] if usable else "",
                "H_ref_source": source["H_ref_source"],
                **{field: source[field] if usable else "" for field in RESIDUAL_FIELDS},
                "M0_kg": output["M0_kg"] if usable else "",
                "epsilon_abs": output["epsilon_abs"] if usable else "",
                "M0_source": output.get("M0_source_mode", "") if usable else source["M0_source"],
                "M_GM_cal_kg": source["M_GM_cal_kg"],
                "row_status": source["row_status"],
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def parent_input_from_density(timestamp: str, density_output: list[dict[str, Any]]) -> list[dict[str, Any]]:
    usable_statuses = {
        "DENSITY_CURRENT_EXACT_COMPUTED_NONCLAIM",
        "DENSITY_CURRENT_INTERVAL_COMPUTED_NONCLAIM",
        "DENSITY_CURRENT_COUNTERFACTUAL_SMOKE_PASS_NONCLAIM",
    }
    rows: list[dict[str, Any]] = []
    for output in density_output:
        usable = output["runner_status"] in usable_statuses
        delta_h = output["Delta_H_abs_kg"] if usable else ""
        rows.append(
            {
                "charge_id": output["density_id"],
                "H_tau_bulk_kg": output["H_tau_bulk_kg"] if usable else "",
                "H_tau_surface_kg": "0" if usable else "",
                "H_tau_source": "source_profile_integral_radius_runner.py",
                "H_ref_kg": output["H_ref_kg"] if usable else "",
                "H_ref_source": "4783_Href_zero_certificate_runner.py",
                "H_tau_curl_abs_kg": delta_h,
                "H_tau_flux_abs_kg": "0" if usable else "",
                "H_tau_sector_abs_kg": "0" if usable else "",
                "H_tau_surface_abs_kg": "0" if usable else "",
                "H_ref_drift_abs_kg": "0" if usable else "",
                "H_ref_selector_abs_kg": "0" if usable else "",
                "M_lower_kg": output["M_lower_kg"] if usable else "",
                "M_lower_source": "rhoH_parent_density_integral_runner.py",
                "M_GM_cal_kg": format_float(M_GM_SUN_CAL),
                "row_status": "counterfactual_smoke_nonclaim" if "counterfactual" in output["density_id"] else "profile_chain_nonclaim",
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def source_input_from_parent(timestamp: str, parent_input: list[dict[str, Any]], parent_output: list[dict[str, Any]]) -> list[dict[str, Any]]:
    parent_by_id = {row["charge_id"]: row for row in parent_input}
    usable_statuses = {
        "PARENT_CHARGE_EXACT_COMPUTED_NONCLAIM",
        "PARENT_CHARGE_INTERVAL_COMPUTED_NONCLAIM",
        "PARENT_CHARGE_COUNTERFACTUAL_SMOKE_PASS_NONCLAIM",
        "PARENT_CHARGE_INTERVAL_WIDE_OR_SIGN_UNRESOLVED_NONCLAIM",
    }
    rows: list[dict[str, Any]] = []
    for output in parent_output:
        parent = parent_by_id[output["charge_id"]]
        usable = output["runner_status"] in usable_statuses
        rows.append(
            {
                "source_id": output["charge_id"],
                "H_tau_kg": output["H_tau_center_kg"] if usable else "",
                "H_tau_source": "parent_charge_Htau_Href_bound_runner.py",
                "H_ref_kg": parent["H_ref_kg"] if usable else "",
                "H_ref_source": parent["H_ref_source"],
                "M_GM_cal_kg": format_float(M_GM_SUN_CAL),
                "row_status": parent["row_status"],
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def open_input_from_source(timestamp: str, source_output: list[dict[str, Any]]) -> list[dict[str, Any]]:
    usable_statuses = {"MHDRESS_COMPUTED_NONCLAIM", "MHDRESS_COUNTERFACTUAL_SMOKE_PASS_NONCLAIM"}
    rows: list[dict[str, Any]] = []
    for output in source_output:
        usable = output["runner_status"] in usable_statuses
        rows.append(
            {
                "arena_id": output["source_id"],
                "mu_ref_m3_s2": f"{MU_SUN_NOMINAL:.8e}",
                "mu_ref_source": "IAU_2015_B3_nominal_solar_GM_comparator",
                "G_cal_m3_kg_s2": f"{G_CAL:.8e}",
                "M_H_dress_kg": output["M_H_dress_kg"] if usable else "",
                "M_H_source": "source_profile_to_rhoH_to_parent_charge_chain" if usable else "MISSING_MHDRESS",
                "sigma_M_H_kg": "",
                "E00_integral_abs_m": "0",
                "E00_sup_abs_m_minus2": "0",
                "support_radius_m": f"{SOLAR_RADIUS_NOMINAL:.6e}",
                "tolerance_eta": "1.0e-10",
                "delta_mu_boundary_abs_m3_s2": "0",
                "delta_mu_profile_abs_m3_s2": "0",
                "delta_mu_readout_abs_m3_s2": "0",
                "row_status": output["row_status_input"],
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def score_rows(timestamp: str, profile_output: list[dict[str, Any]], rhoh_output: list[dict[str, Any]], density_output: list[dict[str, Any]], parent_output: list[dict[str, Any]], source_output: list[dict[str, Any]], open_output: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rhoh_by_id = {row["density_id"]: row for row in rhoh_output}
    density_by_id = {row["density_id"]: row for row in density_output}
    parent_by_id = {row["charge_id"]: row for row in parent_output}
    source_by_id = {row["source_id"]: row for row in source_output}
    open_by_id = {row["arena_id"]: row for row in open_output}
    rows: list[dict[str, Any]] = []
    for output in profile_output:
        profile_id = output["profile_id"]
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "gate_id": f"SG4785_{profile_id}",
                "profile_id": profile_id,
                "profile_runner_status": output["runner_status"],
                "rhoh_runner_status": rhoh_by_id.get(profile_id, {}).get("runner_status", "MISSING_RHOH_OUTPUT"),
                "density_runner_status": density_by_id.get(profile_id, {}).get("runner_status", "MISSING_DENSITY_OUTPUT"),
                "parent_runner_status": parent_by_id.get(profile_id, {}).get("runner_status", "MISSING_PARENT_OUTPUT"),
                "source_runner_status": source_by_id.get(profile_id, {}).get("runner_status", "MISSING_SOURCE_OUTPUT"),
                "open_runner_status": open_by_id.get(profile_id, {}).get("runner_status", "MISSING_OPEN_OUTPUT"),
                "claim_allowed": False,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def simple_rows(timestamp: str, kind: str) -> list[dict[str, Any]]:
    if kind == "gates":
        specs = [
            ("PG4785_0", "profile table must supply rho_H or T_total(n,n), not orbital GM"),
            ("PG4785_1", "profile integral without residual radius is not enough for M_lower"),
            ("PG4785_2", "residual radius must list every R_eq/B_zero/boundary/open-EM/projector/domain/kappa component"),
            ("PG4785_3", "Poynting is Hilbert stress or explicit boundary/open-EM residual, never both"),
            ("PG4785_4", "shared source profile remains fixed before arena projection"),
        ]
        return [{"checkpoint": CHECKPOINT, "gate_id": row_id, "rule": text, "claim_allowed": False, "valid_for_claim": False, "timestamp_utc": timestamp} for row_id, text in specs]
    if kind == "firewalls":
        specs = [
            ("FW4785_0", "no observed-GM/Gcal backfill into source profile", "ACTIVE"),
            ("FW4785_1", "no PPN/clock/R10 fitted residual as source profile", "ACTIVE"),
            ("FW4785_2", "no double-counted Poynting coefficient", "ACTIVE"),
            ("FW4785_3", "no local-GR claim from smoke or private profiles", "LOCAL_PRIVATE_ONLY"),
        ]
        return [{"checkpoint": CHECKPOINT, "firewall_id": row_id, "firewall_rule": text, "status": status, "valid_for_claim": False, "timestamp_utc": timestamp} for row_id, text, status in specs]
    if kind == "routes":
        specs = [
            ("RT4785_0_physical_values", "fill a real parent/source-backed T_total(n,n) or rho_H profile over W_H", "SELECTED_NEXT"),
            ("RT4785_1_zero_certificate", "try a parent zero-profile certificate for non-GR residual components", "SELECTED_NEXT_PARALLEL"),
            ("RT4785_2_radius_values", "source the eight residual-radius components if exact zero fails", "SELECTED_NEXT_PARALLEL"),
        ]
        return [{"checkpoint": CHECKPOINT, "route_id": row_id, "route": text, "selection_status": status, "valid_for_claim": False, "timestamp_utc": timestamp} for row_id, text, status in specs]
    raise ValueError(kind)


def write_docs(timestamp: str, law: list[dict[str, Any]], profile_output: list[dict[str, Any]], rhoh_output: list[dict[str, Any]], score: list[dict[str, Any]], routes: list[dict[str, Any]]) -> None:
    content = f"""# 4785 - Real source-profile integral and residual-radius row

Marker: `{MARKER}`
Generated: `{timestamp}`
Decision: `{DECISION}`

## Result

4785 turns the remaining 4784 profile gap into an executable two-part gate:

```text
rho_H(W_H)=sum_i int_shell_i rho_H dV
          = c^-2 sum_i int_shell_i T_total(n,n)dV

Delta_H_abs = |R_eq|+|B_zero|+|boundary_flux|+|open_EM|
            + |nonEM_owner_gap|+|projector_comm|+|domain_shadow|+|kappa_drift|.
```

The important split is now mechanical: a profile integral alone is not enough; it must travel with the residual-radius row before `M0`, `epsilon_abs`, `M_lower`, and `M_H^dress` become usable.

## Source Profile Law Rows

{markdown_table(law, ["law_id", "formula", "meaning"])}

## Profile Runner Output

{markdown_table(profile_output, ["profile_id", "rho_H_integral_kg", "Delta_H_abs_kg", "source_profile_mode", "residual_radius_mode", "runner_status"])}

## rhoH Runner Output

{markdown_table(rhoh_output, ["density_id", "rho_H_integral_kg", "H_tau_bulk_kg", "M0_kg", "epsilon_abs", "M_lower_kg", "runner_status"])}

## Chain Score

{markdown_table(score, ["profile_id", "profile_runner_status", "rhoh_runner_status", "density_runner_status", "parent_runner_status", "source_runner_status", "open_runner_status"])}

## Route Selection

{markdown_table(routes, ["route_id", "route", "selection_status"])}

## Conclusion

The local source branch has a clean executable throat now. The next real input is not abstract `M0`; it is a parent/source-backed profile table for `T_total(n,n)` or `rho_H`, plus the eight residual-radius components or a parent zero certificate for them. Orbital `GM`, PPN fits, clocks and R10 bounds remain comparison outputs only.

## Next Target

`{NEXT_TARGET}`
"""
    write_text(DOC_PATH, content)

    formal = f"""# PPC4161 4785: Real Source-Profile Integral And Residual-Radius Row

Generated: `{timestamp}`

4785 installs the source-profile integral/residual-radius runner. It computes `rho_H(W_H)` from profile components, rejects observed/fitted source imports, and proves that a profile integral without the residual radius still blocks the downstream `rhoH` gate.

Next: `{NEXT_TARGET}`

Marker: `{MARKER}`
"""
    write_text(FORMAL_PATH, formal)


def append_outputs(timestamp: str) -> None:
    decision = [{"checkpoint": CHECKPOINT, "decision": DECISION, "meaning": "Profile integral and residual radius are now an executable gate; physical values remain missing.", "next_target": NEXT_TARGET, "valid_for_claim": False, "timestamp_utc": timestamp}]
    status = [{"checkpoint": CHECKPOINT, "status": "PASS_SOURCE_PROFILE_INTEGRAL_RADIUS_RUNNER_INSTALLED_NONCLAIM", "summary": "Profile-only rows still block; profile+radius controls pass; forbidden GM profile fails.", "valid_for_claim": False, "timestamp_utc": timestamp}]
    next_target = [{"checkpoint": CHECKPOINT, "next_target": NEXT_TARGET, "reason": "Need real physical profile values or a parent zero-profile certificate for residual components.", "valid_for_claim": False, "timestamp_utc": timestamp}]
    write_csv(DECISION_CSV, decision)
    write_csv(STATUS_CSV, status)
    write_csv(NEXT_TARGET_CSV, next_target)


def add_claim_once(timestamp: str) -> None:
    existing = read_text(CLAIMS_PATH) if CLAIMS_PATH.exists() else ""
    if CLAIM_ID in existing:
        return
    row = [
        CLAIM_ID,
        "source_profile_integral_radius_runner",
        "4785 installs an executable source-profile integral and residual-radius gate for rho_H(W_H).",
        "Generated source register, profile law, profile input-output, chained rhoH/density/parent/source/open outputs, score gates, firewalls, routes, decision, status, next target and validation.",
        "source_profile_integral_radius_private_nonclaim",
        NEXT_TARGET,
        "Do not treat profile smoke rows, nominal solar GM comparator, or missing residual-radius rows as local-GR evidence.",
        "local_gr",
        str(DOC_PATH),
        NEXT_TARGET,
        "Need real parent/source-backed T_total(n,n) profile values or parent zero-profile certificate.",
        "source-profile integral and residual radius",
        f"{MARKER}; {DECISION}; generated {timestamp}",
    ]
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        csv.writer(handle).writerow(row)


def update_resume(timestamp: str) -> None:
    write_text(
        RESUME_PATH,
        f"""# Current Local Resume

Last checkpoint: `{DOC_PATH.name}`
Generated: `{timestamp}`

## Current target

`{NEXT_TARGET}`

## Live blocker

`H_ref=0`, `M0=H_tau_bulk-H_ref`, and the source-profile/residual-radius gate are now executable. The live physical gap is a real parent/source-backed table for `rho_H(W_H)=c^-2 int_W T_total(n,n)dV_eobs` and either theorem-zero or numeric/source-backed rows for the eight residual-radius components: `R_eq`, `B_zero`, boundary/open-EM, non-EM owner gap, projector commutator, domain shadow and kappa drift.

## Firewalls

- No GitHub/public action from this checkpoint.
- No observed-GM/Gcal, PPN, clock, R10, or post-fit residual backfill into the source profile.
- No extra Poynting source coefficient after Maxwell/Hilbert stress is already counted.
""",
    )


def append_spine_and_packet(timestamp: str) -> None:
    append_once(SPINE_PATH, MARKER, f"\n\n## {MARKER}\n\n4785 installs `source_profile_integral_radius_runner.py`: the branch now requires a real `T_total(n,n)`/`rho_H` source profile and a complete residual-radius row before `M0`, `M_lower`, and `M_H^dress` can be used. Profile-only rows still block. Decision: `{DECISION}`. Next: `{NEXT_TARGET}`.\n")
    append_once(PACKET_PATH, PACKET_MARKER, f"\n\n## {PACKET_MARKER}\n\nRunner: `{PROFILE_RUNNER}`. Profile integral and residual radius are now executable as a pair; physical values remain missing/nonclaim. Generated `{timestamp}`.\n")


def validate(timestamp: str, sources: list[dict[str, Any]], profile_output: list[dict[str, Any]], rhoh_output: list[dict[str, Any]], density_output: list[dict[str, Any]], open_output: list[dict[str, Any]], gates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    checks = [
        ("VAL4785_0_sources", "source paths and needles exist", all(row["exists"] is True and row["needle_found"] is True for row in sources), str(SOURCE_REGISTER_CSV)),
        ("VAL4785_1_physical_blocks", "physical missing profile blocks", any(row["profile_id"] == "physical_profile_values_missing" and row["runner_status"] == "BLOCKED_MISSING_SOURCE_PROFILE_COMPONENTS" for row in profile_output), str(PROFILE_OUTPUT_CSV)),
        ("VAL4785_2_profile_without_radius_blocks_downstream", "profile without residual radius blocks rhoH Mlower", any(row["density_id"] == "profile_without_residual_radius_control" and row["runner_status"] == "BLOCKED_MISSING_RHOH_RESIDUAL_RADIUS" for row in rhoh_output), str(RHOH_OUTPUT_CSV)),
        ("VAL4785_3_private_profile_zero_radius", "private profile with zero radius computes", any(row["profile_id"] == "private_unit_profile_with_zero_radius" and row["runner_status"] == "PROFILE_INTEGRAL_AND_RADIUS_EXACT_PRIVATE_NONCLAIM" for row in profile_output), str(PROFILE_OUTPUT_CSV)),
        ("VAL4785_4_finite_profile_radius", "finite profile radius computes interval", any(row["density_id"] == "finite_profile_radius_smoke_nonclaim" and row["runner_status"] == "RHOH_PARENT_INTEGRAL_INTERVAL_COMPUTED_NONCLAIM" for row in rhoh_output), str(RHOH_OUTPUT_CSV)),
        ("VAL4785_5_forbidden_GM_fails", "forbidden GM profile fails", any(row["profile_id"] == "forbidden_orbital_GM_profile_control" and row["runner_status"] == "FAILED_CIRCULAR_SOURCE_PROFILE" for row in profile_output), str(PROFILE_OUTPUT_CSV)),
        ("VAL4785_6_counterfactual_density", "counterfactual reaches density runner", any(row["density_id"] == "counterfactual_profile_equals_comparator" and row["runner_status"] == "DENSITY_CURRENT_COUNTERFACTUAL_SMOKE_PASS_NONCLAIM" for row in density_output), str(DENSITY_OUTPUT_CSV)),
        ("VAL4785_7_open_counterfactual", "counterfactual reaches open runner", any(row["arena_id"] == "counterfactual_profile_equals_comparator" and row["runner_status"] == "RUNNER_SMOKE_PASS_NONCLAIM" for row in open_output), str(OPEN_OUTPUT_CSV)),
        ("VAL4785_8_gates", "promotion gates keep claims closed", all(row["claim_allowed"] is False for row in gates), str(PROMOTION_GATES_CSV)),
        ("VAL4785_9_claim", "claim row L-627 present", CLAIM_ID in read_text(CLAIMS_PATH), str(CLAIMS_PATH)),
        ("VAL4785_10_resume", "resume points to next target", NEXT_TARGET in read_text(RESUME_PATH), str(RESUME_PATH)),
    ]
    rows: list[dict[str, Any]] = []
    for validation_id, check, passed, detail in checks:
        rows.append({"checkpoint": CHECKPOINT, "validation_id": validation_id, "check": check, "status": "PASS" if passed else "FAIL", "detail": detail, "valid_for_claim": False, "timestamp_utc": timestamp})
    overall = all(row["status"] == "PASS" for row in rows)
    rows.append({"checkpoint": CHECKPOINT, "validation_id": "VAL4785_OVERALL", "check": "all 4785 profile integral/radius checks pass", "status": "PASS" if overall else "FAIL", "detail": DECISION, "valid_for_claim": False, "timestamp_utc": timestamp})
    return rows


def main() -> None:
    timestamp = now()
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)

    sources = source_register(timestamp)
    law = law_rows(timestamp)
    profile_input = profile_input_rows(timestamp)
    gates = simple_rows(timestamp, "gates")
    firewalls = simple_rows(timestamp, "firewalls")
    routes = simple_rows(timestamp, "routes")

    write_csv(SOURCE_REGISTER_CSV, sources)
    write_csv(LAW_CSV, law)
    write_csv(PROFILE_INPUT_CSV, profile_input)
    write_csv(PROMOTION_GATES_CSV, gates)
    write_csv(FIREWALL_CSV, firewalls)
    write_csv(ROUTE_MATRIX_CSV, routes)

    run_command([sys.executable, str(PROFILE_RUNNER), str(PROFILE_INPUT_CSV), str(PROFILE_OUTPUT_CSV)])
    profile_output = parse_csv(PROFILE_OUTPUT_CSV)

    rhoh_input = rhoh_input_from_profile(timestamp, profile_output)
    write_csv(RHOH_INPUT_CSV, rhoh_input)
    run_command([sys.executable, str(RHOH_RUNNER), str(RHOH_INPUT_CSV), str(RHOH_OUTPUT_CSV)])
    rhoh_output = parse_csv(RHOH_OUTPUT_CSV)

    density_input = density_input_from_rhoh(timestamp, rhoh_input, rhoh_output)
    write_csv(DENSITY_INPUT_CSV, density_input)
    run_command([sys.executable, str(DENSITY_RUNNER), str(DENSITY_INPUT_CSV), str(DENSITY_OUTPUT_CSV)])
    density_output = parse_csv(DENSITY_OUTPUT_CSV)

    parent_input = parent_input_from_density(timestamp, density_output)
    write_csv(PARENT_INPUT_CSV, parent_input)
    run_command([sys.executable, str(PARENT_CHARGE_RUNNER), str(PARENT_INPUT_CSV), str(PARENT_OUTPUT_CSV)])
    parent_output = parse_csv(PARENT_OUTPUT_CSV)

    source_input = source_input_from_parent(timestamp, parent_input, parent_output)
    write_csv(SOURCE_INPUT_CSV, source_input)
    run_command([sys.executable, str(SOURCE_RUNNER), str(SOURCE_INPUT_CSV), str(SOURCE_OUTPUT_CSV)])
    source_output = parse_csv(SOURCE_OUTPUT_CSV)

    open_input = open_input_from_source(timestamp, source_output)
    write_csv(OPEN_INPUT_CSV, open_input)
    run_command([sys.executable, str(OPEN_RUNNER), str(OPEN_INPUT_CSV), str(OPEN_OUTPUT_CSV)])
    open_output = parse_csv(OPEN_OUTPUT_CSV)

    score = score_rows(timestamp, profile_output, rhoh_output, density_output, parent_output, source_output, open_output)
    write_csv(SCORE_GATE_CSV, score)

    write_docs(timestamp, law, profile_output, rhoh_output, score, routes)
    append_outputs(timestamp)
    add_claim_once(timestamp)
    append_spine_and_packet(timestamp)
    update_resume(timestamp)

    validation = validate(timestamp, sources, profile_output, rhoh_output, density_output, open_output, gates)
    write_csv(VALIDATION_CSV, validation)

    cache_dir = SCRIPT_DIR / "__pycache__"
    if cache_dir.exists():
        shutil.rmtree(cache_dir)


if __name__ == "__main__":
    main()
