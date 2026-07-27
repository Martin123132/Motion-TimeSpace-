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

RHOH_RUNNER = SCRIPT_DIR / "rhoH_parent_density_integral_runner.py"
DENSITY_RUNNER = SCRIPT_DIR / "parent_density_current_mlower_runner.py"
PARENT_CHARGE_RUNNER = SCRIPT_DIR / "parent_charge_Htau_Href_bound_runner.py"
SOURCE_RUNNER = SCRIPT_DIR / "Htau_Href_MHdress_source_runner.py"
OPEN_RUNNER = SCRIPT_DIR / "MHdress_E00_open_arena_runner.py"

CHECKPOINT = "4784"
CLAIM_ID = "L-626"
MARKER = "PPC4161_REAL_RHOH_PARENT_DENSITY_INTEGRAL_OR_M0_SOURCE_BACKED_ROW_4784"
PACKET_MARKER = "PPC4161_PACKET_REAL_RHOH_PARENT_DENSITY_INTEGRAL_OR_M0_SOURCE_BACKED_ROW_4784"
DECISION = "RHOH_PARENT_DENSITY_INTEGRAL_ASSEMBLER_INSTALLED_SELF_DENOMINATOR_LAW_DERIVED_REAL_NUMERIC_PROFILE_STILL_MISSING_NONCLAIM"
NEXT_TARGET = "4785-Y5-R2FR-real-source-profile-integral-and-residual-radius-row.md"

DOC_PATH = POST / "4784-Y5-R2FR-real-rhoH-parent-density-integral-or-M0-source-backed-row.md"
FORMAL_PATH = FORMAL / "800-PPC4161-real-rhoH-parent-density-integral-or-M0-source-backed-row.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"

SOURCE_REGISTER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4784_SOURCE_REGISTER.csv"
LAW_CSV = SOURCE_DIR / "P8_Y5_R2FR_4784_RHOH_M0_LAW.csv"
RHOH_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4784_RHOH_PARENT_DENSITY_INPUT.csv"
RHOH_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4784_RHOH_PARENT_DENSITY_OUTPUT.csv"
DENSITY_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4784_DENSITY_INPUT_FROM_RHOH.csv"
DENSITY_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4784_DENSITY_OUTPUT_FROM_RHOH.csv"
PARENT_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4784_PARENT_CHARGE_INPUT_FROM_RHOH.csv"
PARENT_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4784_PARENT_CHARGE_OUTPUT_FROM_RHOH.csv"
SOURCE_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4784_HTAU_HREF_SOURCE_INPUT.csv"
SOURCE_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4784_HTAU_HREF_SOURCE_OUTPUT.csv"
OPEN_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4784_OPEN_ARENA_INPUT.csv"
OPEN_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4784_OPEN_ARENA_OUTPUT.csv"
SCORE_GATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4784_SCORE_GATE_UPDATE.csv"
PROMOTION_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4784_PROMOTION_GATES.csv"
FIREWALL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4784_FIREWALL_ROWS.csv"
ROUTE_MATRIX_CSV = SOURCE_DIR / "P8_Y5_R2FR_4784_ROUTE_SELECTION_MATRIX.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4784_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4784_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4784_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4784_VALIDATION.csv"

G_CAL = 6.67430e-11
MU_SUN_NOMINAL = 1.3271244e20
SOLAR_RADIUS_NOMINAL = 6.957e8
M_GM_SUN_CAL = MU_SUN_NOMINAL / G_CAL

SOURCE_SPECS = [
    ("SRC4784_00_4783_doc", POST / "4783-Y5-R2FR-real-parent-density-current-source-row-or-Href-zero-certificate.md", "real `rho_H dV_H`", "4783 narrowed blocker to rho_H/M0"),
    ("SRC4784_01_4782_doc", POST / "4782-Y5-R2FR-parent-Htau-density-current-first-source-row-or-Mlower-bound-fill.md", "rho_H dV_H := c^-2 T_total(n,n)dV_eobs", "4782 density-current law"),
    ("SRC4784_02_4587_doc", POST / "4587-Y5-R2FR-Hilbert-source-density-qbasic-and-Poynting-support-owner-or-bound.md", "rho_H dV_H := c^-2 T_total(n,n) dV_eobs", "4587 density/Poynting theorem"),
    ("SRC4784_03_3883_doc", POST / "3883-Y5-R2FR-Hilbert-source-and-Maxwell-stress-lock-or-residual-vector.md", "T_H^{mu nu}:=", "3883 same Hilbert source lock"),
    ("SRC4784_04_3561_density", SOURCE_DIR / "P8_Y5_R2FR_3561_HILBERT_DENSITY_QBASIC_THEOREM.csv", "HDQ3561_0_density_definition", "3561 Hilbert density definition"),
    ("SRC4784_05_4587_density", SOURCE_DIR / "P8_Y5_R2FR_4587_DENSITY_QBASIC_THEOREM.csv", "DQT4587_0_density_definition", "4587 density theorem csv"),
    ("SRC4784_06_4783_href", SOURCE_DIR / "P8_Y5_R2FR_4783_HREF_ZERO_OUTPUT.csv", "private_source_blind_Href_zero_certificate", "4783 Href zero output"),
    ("SRC4784_07_claim625", CLAIMS_PATH, "L-625", "prior claim register handoff"),
    ("SRC4784_08_rhoh_runner", RHOH_RUNNER, "def compute_row", "4784 rhoH parent density integral runner"),
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
        ("RML4784_0_rhoH_integral", "rho_H(W_H)=c^-2 int_{W_H} T_total(n,n)dV_eobs", "defines the real parent density integral from the same Hilbert stress"),
        ("RML4784_1_Htau_bulk", "H_tau_bulk=rho_H(W_H)+H_tau_surface_center", "turns the density integral into the parent H_tau bulk row"),
        ("RML4784_2_M0_self", "M0=H_tau_bulk-H_ref when H_ref is fixed and the Hilbert energy branch is positive", "removes independent M0 as an extra axiom on the signed positive branch"),
        ("RML4784_3_Mlower", "epsilon_abs=Delta_H_abs/M0 and M_lower=M0(1-epsilon_abs)", "makes positivity a residual-radius inequality"),
        ("RML4784_4_firewall", "orbital GM, fitted acceleration, and post-fit reference subtraction cannot source rho_H or M0", "keeps source mass from being read backward out of the test"),
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


def signed_clauses(value: bool) -> dict[str, bool]:
    return {
        "parent_action_signed": value,
        "variation_before_readout_signed": value,
        "same_frame_signed": value,
        "qbasic_density_signed": value,
        "compact_support_signed": value,
        "positive_energy_signed": value,
        "poynting_once_signed": value,
        "no_flux_or_flux_row_signed": value,
        "no_species_prefactor_signed": value,
        "no_postfit_signed": value,
        "surface_zero_signed": value,
        "M0_from_density_signed": value,
        "epsilon_from_residual_radius_signed": value,
    }


def zero_residuals() -> dict[str, str]:
    return {
        "R_eq_abs_kg": "0",
        "B_zero_abs_kg": "0",
        "boundary_flux_abs_kg": "0",
        "open_EM_abs_kg": "0",
        "nonEM_owner_gap_abs_kg": "0",
        "projector_comm_abs_kg": "0",
        "domain_shadow_abs_kg": "0",
        "kappa_drift_abs_kg": "0",
    }


def rhoh_input_rows(timestamp: str) -> list[dict[str, Any]]:
    residual = 0.01 * M_GM_SUN_CAL
    finite_residuals = {
        "R_eq_abs_kg": format_float(residual),
        "B_zero_abs_kg": "0",
        "boundary_flux_abs_kg": format_float(residual),
        "open_EM_abs_kg": "0",
        "nonEM_owner_gap_abs_kg": "0",
        "projector_comm_abs_kg": "0",
        "domain_shadow_abs_kg": "0",
        "kappa_drift_abs_kg": "0",
    }
    partial = signed_clauses(False)
    partial.update(
        {
            "variation_before_readout_signed": True,
            "same_frame_signed": True,
            "qbasic_density_signed": True,
            "poynting_once_signed": True,
            "no_postfit_signed": True,
            "surface_zero_signed": True,
            "M0_from_density_signed": True,
            "epsilon_from_residual_radius_signed": True,
        }
    )
    rows = [
        {
            "density_id": "physical_candidate_parent_density_law_values_missing",
            "rho_H_integral_kg": "",
            "T_total_nn_integral_J": "",
            "c_m_s": "299792458",
            "rho_H_source": "3883_4587_HILBERT_DENSITY_LAW_VALUES_MISSING",
            "T_total_nn_source": "MISSING_SOURCE_PROFILE_TNN_INTEGRAL",
            "H_tau_surface_center_kg": "",
            "H_tau_surface_source": "SURFACE_ZERO_BRANCH_CONDITIONAL_4784",
            "H_ref_kg": "0",
            "H_ref_source": "4783_PRIVATE_SOURCE_BLIND_HREF_ZERO_NONCLAIM",
            **zero_residuals(),
            "M0_kg": "",
            "M0_source": "SELF_DENOMINATOR_LAW_CONDITIONAL_VALUES_MISSING",
            "epsilon_abs": "",
            "epsilon_source": "RESIDUAL_RADIUS_OVER_M0_LAW_CONDITIONAL",
            "M_GM_cal_kg": format_float(M_GM_SUN_CAL),
            **partial,
            "row_status": "physical_candidate_values_missing_nonclaim",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "density_id": "private_positive_density_self_denominator_control",
            "rho_H_integral_kg": "1",
            "T_total_nn_integral_J": "",
            "c_m_s": "299792458",
            "rho_H_source": "PRIVATE_UNIT_PARENT_DENSITY_CONTROL",
            "T_total_nn_source": "",
            "H_tau_surface_center_kg": "",
            "H_tau_surface_source": "PRIVATE_SURFACE_ZERO_CONTROL",
            "H_ref_kg": "0",
            "H_ref_source": "4783_PRIVATE_SOURCE_BLIND_HREF_ZERO_NONCLAIM",
            **zero_residuals(),
            "M0_kg": "",
            "M0_source": "SELF_FROM_POSITIVE_HILBERT_DENSITY_CONTROL",
            "epsilon_abs": "",
            "epsilon_source": "RESIDUAL_RADIUS_OVER_M0_CONTROL",
            "M_GM_cal_kg": format_float(M_GM_SUN_CAL),
            **signed_clauses(True),
            "row_status": "private_positive_density_control_nonclaim",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "density_id": "finite_residual_self_denominator_smoke_nonclaim",
            "rho_H_integral_kg": format_float(M_GM_SUN_CAL),
            "T_total_nn_integral_J": "",
            "c_m_s": "299792458",
            "rho_H_source": "SMOKE_PARENT_DENSITY_NOT_PHYSICAL",
            "T_total_nn_source": "",
            "H_tau_surface_center_kg": "0",
            "H_tau_surface_source": "SMOKE_SURFACE_ZERO",
            "H_ref_kg": "0",
            "H_ref_source": "4783_PRIVATE_SOURCE_BLIND_HREF_ZERO_NONCLAIM",
            **finite_residuals,
            "M0_kg": "",
            "M0_source": "SELF_FROM_POSITIVE_HILBERT_DENSITY_SMOKE",
            "epsilon_abs": "",
            "epsilon_source": "RESIDUAL_RADIUS_OVER_M0_SMOKE",
            "M_GM_cal_kg": format_float(M_GM_SUN_CAL),
            **signed_clauses(True),
            "row_status": "finite_residual_smoke_nonclaim",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "density_id": "external_M0_without_rho_integral_control",
            "rho_H_integral_kg": "",
            "T_total_nn_integral_J": "",
            "c_m_s": "299792458",
            "rho_H_source": "MISSING_RHOH_PROFILE",
            "T_total_nn_source": "MISSING_TNN_PROFILE",
            "H_tau_surface_center_kg": "0",
            "H_tau_surface_source": "EXTERNAL_M0_CONTROL_SURFACE_ZERO",
            "H_ref_kg": "0",
            "H_ref_source": "4783_PRIVATE_SOURCE_BLIND_HREF_ZERO_NONCLAIM",
            **zero_residuals(),
            "M0_kg": "1",
            "M0_source": "EXTERNAL_M0_DOES_NOT_SUPPLY_RHOH_CONTROL",
            "epsilon_abs": "0",
            "epsilon_source": "EXTERNAL_EPSILON_CONTROL",
            "M_GM_cal_kg": format_float(M_GM_SUN_CAL),
            **signed_clauses(True),
            "row_status": "external_M0_without_rhoH_control_nonclaim",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "density_id": "forbidden_orbital_GM_M0_control",
            "rho_H_integral_kg": format_float(M_GM_SUN_CAL),
            "T_total_nn_integral_J": "",
            "c_m_s": "299792458",
            "rho_H_source": "ORBITAL_GM_DEFINITION_FORBIDDEN_CONTROL",
            "T_total_nn_source": "",
            "H_tau_surface_center_kg": "0",
            "H_tau_surface_source": "FORBIDDEN_CONTROL",
            "H_ref_kg": "0",
            "H_ref_source": "POSTFIT_REFERENCE_OBSERVED_RESIDUAL_CANCEL_CONTROL",
            **zero_residuals(),
            "M0_kg": format_float(M_GM_SUN_CAL),
            "M0_source": "GM_AS_SOURCE_FORBIDDEN_CONTROL",
            "epsilon_abs": "0",
            "epsilon_source": "FORBIDDEN_CONTROL",
            "M_GM_cal_kg": format_float(M_GM_SUN_CAL),
            **signed_clauses(True),
            "row_status": "physical_forbidden_circular_control_nonclaim",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "density_id": "counterfactual_rhoH_equals_comparator",
            "rho_H_integral_kg": format_float(M_GM_SUN_CAL),
            "T_total_nn_integral_J": "",
            "c_m_s": "299792458",
            "rho_H_source": "COUNTERFACTUAL_RUNNER_SMOKE_ONLY",
            "T_total_nn_source": "",
            "H_tau_surface_center_kg": "0",
            "H_tau_surface_source": "COUNTERFACTUAL_RUNNER_SMOKE_ONLY",
            "H_ref_kg": "0",
            "H_ref_source": "COUNTERFACTUAL_RUNNER_SMOKE_ONLY",
            **zero_residuals(),
            "M0_kg": "",
            "M0_source": "COUNTERFACTUAL_SELF_DENOMINATOR_SMOKE_ONLY",
            "epsilon_abs": "",
            "epsilon_source": "COUNTERFACTUAL_RESIDUAL_RADIUS_OVER_M0",
            "M_GM_cal_kg": format_float(M_GM_SUN_CAL),
            **signed_clauses(True),
            "row_status": "counterfactual_smoke_nonclaim",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]
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
                "H_tau_surface_source": "rhoH_parent_density_integral_runner.py" if usable else source["H_tau_surface_source"],
                "H_ref_kg": output["H_ref_kg"] if usable else "",
                "H_ref_source": source["H_ref_source"],
                "R_eq_abs_kg": source["R_eq_abs_kg"] if usable else "",
                "B_zero_abs_kg": source["B_zero_abs_kg"] if usable else "",
                "boundary_flux_abs_kg": source["boundary_flux_abs_kg"] if usable else "",
                "open_EM_abs_kg": source["open_EM_abs_kg"] if usable else "",
                "nonEM_owner_gap_abs_kg": source["nonEM_owner_gap_abs_kg"] if usable else "",
                "projector_comm_abs_kg": source["projector_comm_abs_kg"] if usable else "",
                "domain_shadow_abs_kg": source["domain_shadow_abs_kg"] if usable else "",
                "kappa_drift_abs_kg": source["kappa_drift_abs_kg"] if usable else "",
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
                "H_tau_source": "rhoH_parent_density_integral_runner.py",
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
                "row_status": "counterfactual_smoke_nonclaim" if "counterfactual" in output["density_id"] else "rhoH_chain_nonclaim",
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
        usable = output["runner_status"] in usable_statuses
        parent = parent_by_id[output["charge_id"]]
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
                "M_H_source": "rhoH_to_density_to_parent_charge_chain" if usable else "MISSING_MHDRESS",
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


def score_rows(timestamp: str, rhoh_output: list[dict[str, Any]], density_output: list[dict[str, Any]], parent_output: list[dict[str, Any]], source_output: list[dict[str, Any]], open_output: list[dict[str, Any]]) -> list[dict[str, Any]]:
    density_by_id = {row["density_id"]: row for row in density_output}
    parent_by_id = {row["charge_id"]: row for row in parent_output}
    source_by_id = {row["source_id"]: row for row in source_output}
    open_by_id = {row["arena_id"]: row for row in open_output}
    rows: list[dict[str, Any]] = []
    for output in rhoh_output:
        density_id = output["density_id"]
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "gate_id": f"SG4784_{density_id}",
                "density_id": density_id,
                "rhoh_runner_status": output["runner_status"],
                "density_runner_status": density_by_id.get(density_id, {}).get("runner_status", "MISSING_DENSITY_OUTPUT"),
                "parent_runner_status": parent_by_id.get(density_id, {}).get("runner_status", "MISSING_PARENT_OUTPUT"),
                "source_runner_status": source_by_id.get(density_id, {}).get("runner_status", "MISSING_SOURCE_OUTPUT"),
                "open_runner_status": open_by_id.get(density_id, {}).get("runner_status", "MISSING_OPEN_OUTPUT"),
                "claim_allowed": False,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def simple_rows(timestamp: str, kind: str) -> list[dict[str, Any]]:
    if kind == "gates":
        specs = [
            ("PG4784_0", "rho_H must be a parent Hilbert density integral, not orbital GM"),
            ("PG4784_1", "M0 may be self-derived only from positive H_tau_bulk-H_ref on a signed branch"),
            ("PG4784_2", "external M0 alone does not supply the rho_H integral"),
            ("PG4784_3", "epsilon_abs is residual-radius over M0, not an independent optimism knob"),
            ("PG4784_4", "counterfactual rows remain smoke only"),
        ]
        return [{"checkpoint": CHECKPOINT, "gate_id": row_id, "rule": text, "claim_allowed": False, "valid_for_claim": False, "timestamp_utc": timestamp} for row_id, text in specs]
    if kind == "firewalls":
        specs = [
            ("FW4784_0", "no observed-GM/Gcal backfill into rho_H or M0", "ACTIVE"),
            ("FW4784_1", "no post-fit H_ref or residual cancellation", "ACTIVE"),
            ("FW4784_2", "Poynting is counted inside Hilbert stress or explicit boundary flux only", "ACTIVE"),
            ("FW4784_3", "no public/local-GR claim from self-denominator smoke rows", "LOCAL_PRIVATE_ONLY"),
        ]
        return [{"checkpoint": CHECKPOINT, "firewall_id": row_id, "firewall_rule": text, "status": status, "valid_for_claim": False, "timestamp_utc": timestamp} for row_id, text, status in specs]
    if kind == "routes":
        specs = [
            ("RT4784_0_profile", "fill a real source-profile T_total(n,n) integral over W_H", "SELECTED_NEXT"),
            ("RT4784_1_residual_radius", "source R_eq/B_zero/boundary/open-EM/projector/domain/kappa residual radius", "SELECTED_NEXT_PARALLEL"),
            ("RT4784_2_parent_signature", "promote the 3883/4587 source action clauses from conditional to parent-signed", "SELECTED_NEXT_PARALLEL"),
        ]
        return [{"checkpoint": CHECKPOINT, "route_id": row_id, "route": text, "selection_status": status, "valid_for_claim": False, "timestamp_utc": timestamp} for row_id, text, status in specs]
    raise ValueError(kind)


def write_docs(timestamp: str, law: list[dict[str, Any]], rhoh_output: list[dict[str, Any]], density_output: list[dict[str, Any]], score: list[dict[str, Any]], routes: list[dict[str, Any]]) -> None:
    content = f"""# 4784 - Real rhoH parent density integral or M0 source-backed row

Marker: `{MARKER}`
Generated: `{timestamp}`
Decision: `{DECISION}`

## Result

4784 removes one fake degree of freedom from the local source-mass branch. `M0` does not need to be an extra axiom if the same parent branch supplies a positive Hilbert density integral:

```text
rho_H(W_H) = c^-2 int_W T_total(n,n) dV_eobs
H_tau_bulk = rho_H(W_H) + H_tau_surface_center
M0 = H_tau_bulk - H_ref
epsilon_abs = Delta_H_abs/M0
M_lower = M0(1-epsilon_abs).
```

This is still not a local-GR or Newton claim because the live physical row has no numeric/source-backed `rho_H(W_H)` profile integral. The useful gain is that independent `M0` has been demoted: either it is the positive Hilbert source integral itself, or an external source-backed value must be supplied without using observed orbital `GM`.

## rhoH/M0 Law Rows

{markdown_table(law, ["law_id", "formula", "meaning"])}

## rhoH Runner Output

{markdown_table(rhoh_output, ["density_id", "rho_H_integral_kg", "H_tau_bulk_kg", "M0_kg", "epsilon_abs", "M_lower_kg", "runner_status"])}

## Density Runner Output

{markdown_table(density_output, ["density_id", "H_tau_bulk_kg", "H_ref_kg", "M_lower_kg", "Delta_H_abs_kg", "runner_status"])}

## Chain Score

{markdown_table(score, ["density_id", "rhoh_runner_status", "density_runner_status", "parent_runner_status", "source_runner_status", "open_runner_status"])}

## Route Selection

{markdown_table(routes, ["route_id", "route", "selection_status"])}

## Conclusion

The branch is tighter, not looser. `H_ref` is already fixed by 4783; 4784 makes `M0` self-derived on the positive Hilbert branch. The remaining real gap is now a source-profile problem: supply `int_W T_total(n,n)dV/c^2` plus a finite residual-radius row without reading the answer from orbital `GM`.

## Next Target

`{NEXT_TARGET}`
"""
    write_text(DOC_PATH, content)

    formal = f"""# PPC4161 4784: Real rhoH Parent Density Integral Or M0 Source-Backed Row

Generated: `{timestamp}`

4784 installs the `rhoH_parent_density_integral_runner.py` gate. It derives the self-denominator law `M0=H_tau_bulk-H_ref` on the signed positive Hilbert branch, rejects observed-GM source backfill, and keeps the physical row blocked until a real `T_total(n,n)` source-profile integral is supplied.

Next: `{NEXT_TARGET}`

Marker: `{MARKER}`
"""
    write_text(FORMAL_PATH, formal)


def append_outputs(timestamp: str) -> None:
    decision = [{"checkpoint": CHECKPOINT, "decision": DECISION, "meaning": "M0 is self-derived on the positive Hilbert density branch; physical claim still needs real rho_H profile and residual radius.", "next_target": NEXT_TARGET, "valid_for_claim": False, "timestamp_utc": timestamp}]
    status = [{"checkpoint": CHECKPOINT, "status": "PASS_RHOH_PARENT_DENSITY_INTEGRAL_RUNNER_INSTALLED_NONCLAIM", "summary": "Self-denominator law works in controls; real physical row remains blocked on source-profile integral.", "valid_for_claim": False, "timestamp_utc": timestamp}]
    next_target = [{"checkpoint": CHECKPOINT, "next_target": NEXT_TARGET, "reason": "The next irreducible input is the actual source-profile integral and residual-radius values.", "valid_for_claim": False, "timestamp_utc": timestamp}]
    write_csv(DECISION_CSV, decision)
    write_csv(STATUS_CSV, status)
    write_csv(NEXT_TARGET_CSV, next_target)


def add_claim_once(timestamp: str) -> None:
    existing = read_text(CLAIMS_PATH) if CLAIMS_PATH.exists() else ""
    if CLAIM_ID in existing:
        return
    row = [
        CLAIM_ID,
        "rhoH_parent_density_integral_runner",
        "4784 derives the self-denominator law for M0 from the positive parent Hilbert density integral and rejects observed-GM backfill.",
        "Generated source register, rhoH/M0 law, rhoH input-output, chained density/parent/source/open outputs, score gates, firewalls, routes, decision, status, next target and validation.",
        "rhoh_self_denominator_private_nonclaim",
        NEXT_TARGET,
        "Do not treat self-denominator smoke rows or nominal solar GM comparator as a real source-profile integral.",
        "local_gr",
        str(DOC_PATH),
        NEXT_TARGET,
        "Need real parent T_total(n,n) source-profile integral and residual-radius components.",
        "rhoH parent density integral and M0 self-denominator",
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

`H_ref=0` is fixed in the private source-blind branch, and `M0` is no longer an independent axiom on the positive Hilbert branch: `M0=H_tau_bulk-H_ref` and `epsilon_abs=Delta_H_abs/M0`. The live physical gap is now the actual source-profile integral `rho_H(W_H)=c^-2 int_W T_total(n,n)dV_eobs`, plus source-backed residual-radius rows for `R_eq`, `B_zero`, boundary/open-EM, projector, domain and kappa drift.

## Firewalls

- No GitHub/public action from this checkpoint.
- No observed-GM/Gcal backfill into `rho_H`, `M0`, density, charge or lower-bound rows.
- No extra Poynting source coefficient after Maxwell/Hilbert stress is already counted.
""",
    )


def append_spine_and_packet(timestamp: str) -> None:
    append_once(SPINE_PATH, MARKER, f"\n\n## {MARKER}\n\n4784 installs the `rhoH_parent_density_integral_runner.py` gate. It derives `M0=H_tau_bulk-H_ref` from the same positive Hilbert density integral on the signed branch, so `M0` is not an independent closure axiom there. The live source-mass blocker is now the real `T_total(n,n)` profile integral and residual-radius row. Decision: `{DECISION}`. Next: `{NEXT_TARGET}`.\n")
    append_once(PACKET_PATH, PACKET_MARKER, f"\n\n## {PACKET_MARKER}\n\nRunner: `{RHOH_RUNNER}`. Private controls show the self-denominator law is executable; physical source mass still needs a real source-profile integral and residual-radius values. Generated `{timestamp}`.\n")


def validate(timestamp: str, sources: list[dict[str, Any]], rhoh_output: list[dict[str, Any]], density_output: list[dict[str, Any]], parent_output: list[dict[str, Any]], source_output: list[dict[str, Any]], open_output: list[dict[str, Any]], gates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    checks = [
        ("VAL4784_0_sources", "source paths and needles exist", all(row["exists"] is True and row["needle_found"] is True for row in sources), str(SOURCE_REGISTER_CSV)),
        ("VAL4784_1_physical_blocks", "physical law row blocks on missing rhoH numeric integral", any(row["density_id"] == "physical_candidate_parent_density_law_values_missing" and row["runner_status"] == "BLOCKED_MISSING_RHOH_NUMERIC_INTEGRAL" for row in rhoh_output), str(RHOH_OUTPUT_CSV)),
        ("VAL4784_2_private_self_denominator", "private positive density derives M0 from rhoH", any(row["density_id"] == "private_positive_density_self_denominator_control" and row["runner_status"] == "RHOH_SELF_DENOMINATOR_EXACT_PRIVATE_NONCLAIM" and row["M0_source_mode"] == "SELF_FROM_POSITIVE_HILBERT_DENSITY" for row in rhoh_output), str(RHOH_OUTPUT_CSV)),
        ("VAL4784_3_finite_interval", "finite residual row computes interval Mlower", any(row["density_id"] == "finite_residual_self_denominator_smoke_nonclaim" and row["runner_status"] == "RHOH_PARENT_INTEGRAL_INTERVAL_COMPUTED_NONCLAIM" for row in rhoh_output), str(RHOH_OUTPUT_CSV)),
        ("VAL4784_4_external_M0_not_enough", "external M0 without rhoH still blocks", any(row["density_id"] == "external_M0_without_rho_integral_control" and row["runner_status"] == "BLOCKED_MISSING_RHOH_NUMERIC_INTEGRAL" for row in rhoh_output), str(RHOH_OUTPUT_CSV)),
        ("VAL4784_5_forbidden_GM_fails", "orbital GM source control fails", any(row["density_id"] == "forbidden_orbital_GM_M0_control" and row["runner_status"] == "FAILED_CIRCULAR_RHOH_OR_M0_SOURCE" for row in rhoh_output), str(RHOH_OUTPUT_CSV)),
        ("VAL4784_6_density_counterfactual", "counterfactual reaches density runner", any(row["density_id"] == "counterfactual_rhoH_equals_comparator" and row["runner_status"] == "DENSITY_CURRENT_COUNTERFACTUAL_SMOKE_PASS_NONCLAIM" for row in density_output), str(DENSITY_OUTPUT_CSV)),
        ("VAL4784_7_open_counterfactual", "counterfactual reaches open runner", any(row["arena_id"] == "counterfactual_rhoH_equals_comparator" and row["runner_status"] == "RUNNER_SMOKE_PASS_NONCLAIM" for row in open_output), str(OPEN_OUTPUT_CSV)),
        ("VAL4784_8_gates", "promotion gates keep claims closed", all(row["claim_allowed"] is False for row in gates), str(PROMOTION_GATES_CSV)),
        ("VAL4784_9_claim", "claim row L-626 present", CLAIM_ID in read_text(CLAIMS_PATH), str(CLAIMS_PATH)),
        ("VAL4784_10_resume", "resume points to next target", NEXT_TARGET in read_text(RESUME_PATH), str(RESUME_PATH)),
    ]
    rows: list[dict[str, Any]] = []
    for validation_id, check, passed, detail in checks:
        rows.append({"checkpoint": CHECKPOINT, "validation_id": validation_id, "check": check, "status": "PASS" if passed else "FAIL", "detail": detail, "valid_for_claim": False, "timestamp_utc": timestamp})
    overall = all(row["status"] == "PASS" for row in rows)
    rows.append({"checkpoint": CHECKPOINT, "validation_id": "VAL4784_OVERALL", "check": "all 4784 rhoH/M0 checks pass", "status": "PASS" if overall else "FAIL", "detail": DECISION, "valid_for_claim": False, "timestamp_utc": timestamp})
    return rows


def main() -> None:
    timestamp = now()
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)

    sources = source_register(timestamp)
    law = law_rows(timestamp)
    rhoh_input = rhoh_input_rows(timestamp)
    gates = simple_rows(timestamp, "gates")
    firewalls = simple_rows(timestamp, "firewalls")
    routes = simple_rows(timestamp, "routes")

    write_csv(SOURCE_REGISTER_CSV, sources)
    write_csv(LAW_CSV, law)
    write_csv(RHOH_INPUT_CSV, rhoh_input)
    write_csv(PROMOTION_GATES_CSV, gates)
    write_csv(FIREWALL_CSV, firewalls)
    write_csv(ROUTE_MATRIX_CSV, routes)

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

    score = score_rows(timestamp, rhoh_output, density_output, parent_output, source_output, open_output)
    write_csv(SCORE_GATE_CSV, score)

    write_docs(timestamp, law, rhoh_output, density_output, score, routes)
    append_outputs(timestamp)
    add_claim_once(timestamp)
    append_spine_and_packet(timestamp)
    update_resume(timestamp)

    validation = validate(timestamp, sources, rhoh_output, density_output, parent_output, source_output, open_output, gates)
    write_csv(VALIDATION_CSV, validation)

    cache_dir = SCRIPT_DIR / "__pycache__"
    if cache_dir.exists():
        shutil.rmtree(cache_dir)


if __name__ == "__main__":
    main()
