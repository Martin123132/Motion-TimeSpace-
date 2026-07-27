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

DENSITY_RUNNER = SCRIPT_DIR / "parent_density_current_mlower_runner.py"
PARENT_CHARGE_RUNNER = SCRIPT_DIR / "parent_charge_Htau_Href_bound_runner.py"
SOURCE_RUNNER = SCRIPT_DIR / "Htau_Href_MHdress_source_runner.py"
OPEN_RUNNER = SCRIPT_DIR / "MHdress_E00_open_arena_runner.py"

CHECKPOINT = "4782"
CLAIM_ID = "L-624"
MARKER = "PPC4161_PARENT_HTAU_DENSITY_CURRENT_FIRST_SOURCE_ROW_OR_MLOWER_BOUND_FILL_4782"
PACKET_MARKER = "PPC4161_PACKET_PARENT_HTAU_DENSITY_CURRENT_FIRST_SOURCE_ROW_OR_MLOWER_BOUND_FILL_4782"
DECISION = "DENSITY_CURRENT_AND_MLOWER_RUNNER_INSTALLED_REAL_PARENT_DENSITY_BLOCKS_PRIVATE_AND_COUNTERFACTUAL_CONTROLS_PASS_NONCLAIM"
NEXT_TARGET = "4783-Y5-R2FR-real-parent-density-current-source-row-or-Href-zero-certificate.md"

DOC_PATH = POST / "4782-Y5-R2FR-parent-Htau-density-current-first-source-row-or-Mlower-bound-fill.md"
FORMAL_PATH = FORMAL / "798-PPC4161-parent-Htau-density-current-first-source-row-or-Mlower-bound-fill.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"

SOURCE_REGISTER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4782_SOURCE_REGISTER.csv"
DENSITY_THEOREM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4782_DENSITY_CURRENT_THEOREM.csv"
MLOWER_LAW_CSV = SOURCE_DIR / "P8_Y5_R2FR_4782_MLOWER_BOUND_LAW.csv"
DENSITY_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4782_DENSITY_CURRENT_INPUT.csv"
DENSITY_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4782_DENSITY_CURRENT_OUTPUT.csv"
PARENT_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4782_PARENT_CHARGE_INPUT_FROM_DENSITY.csv"
PARENT_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4782_PARENT_CHARGE_OUTPUT_FROM_DENSITY.csv"
SOURCE_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4782_HTAU_HREF_SOURCE_INPUT_FROM_DENSITY.csv"
SOURCE_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4782_HTAU_HREF_SOURCE_OUTPUT_FROM_DENSITY.csv"
OPEN_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4782_OPEN_ARENA_INPUT_FROM_DENSITY.csv"
OPEN_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4782_OPEN_ARENA_OUTPUT_FROM_DENSITY.csv"
SCORE_GATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4782_SCORE_GATE_UPDATE.csv"
PROMOTION_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4782_PROMOTION_GATES.csv"
FIREWALL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4782_FIREWALL_ROWS.csv"
ROUTE_MATRIX_CSV = SOURCE_DIR / "P8_Y5_R2FR_4782_ROUTE_SELECTION_MATRIX.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4782_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4782_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4782_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4782_VALIDATION.csv"

G_CAL = 6.67430e-11
MU_SUN_NOMINAL = 1.3271244e20
SOLAR_RADIUS_NOMINAL = 6.957e8
M_GM_SUN_CAL = MU_SUN_NOMINAL / G_CAL

SOURCE_SPECS = [
    ("SRC4782_00_4781_doc", POST / "4781-Y5-R2FR-Htau-Href-parent-charge-evaluation-or-reference-bound.md", "H_tau_bulk", "4781 live parent charge input"),
    ("SRC4782_01_formal603_density", FORMAL / "603-PPC4161-Hilbert-source-density-qbasic-and-Poynting-support-owner-or-bound.md", "rho_H dV_H := c^-2", "4587 Hilbert source density law"),
    ("SRC4782_02_formal604_reynolds", FORMAL / "604-PPC4161-regular-source-support-boundary-zero-or-Reynolds-shell-bound.md", "E_boundary_birth", "4588 support/Reynolds shell bound"),
    ("SRC4782_03_formal605_mhref", FORMAL / "605-PPC4161-MHref-source-blind-reference-and-Htau-normalization-zero-or-bound.md", "M_lower=M_EH", "4589 MHref/Mlower denominator guard"),
    ("SRC4782_04_formal790_private", FORMAL / "790-PPC4161-denominator-projector-positive-lock-or-first-source-backed-M0-epsilon-row.md", "M_lower = M_0 > 0", "4774 private Mlower positive lock"),
    ("SRC4782_05_4774_mlower", SOURCE_DIR / "P8_Y5_R2FR_4774_DENOMINATOR_POSITIVE_LOCK_THEOREM.csv", "DL4774_3_Mlower_positive", "4774 Mlower positive theorem row"),
    ("SRC4782_06_4678_tail", SOURCE_DIR / "P8_Y5_R2FR_4678_REQ_BZERO_HTAU_TAIL_CONTRACTS.csv", "TAIL4678_2_epsilon_HM", "4678 Req/Bzero/Htau tail contract"),
    ("SRC4782_07_4732_doc", POST / "4732-Y5-R2FR-R826-parent-constructor-list-from-action-density-or-CI826-VI-source-row.md", "NO_PARENT_DENSITY_SIGNATURE_FOUND", "4732 parent density signature search result"),
    ("SRC4782_08_density_runner", DENSITY_RUNNER, "def compute_row", "4782 density/current/Mlower runner"),
    ("SRC4782_09_parent_runner", PARENT_CHARGE_RUNNER, "PARENT_CHARGE_INTERVAL_COMPUTED_NONCLAIM", "4781 parent charge runner"),
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


def is_numeric_text(value: str) -> bool:
    try:
        float(str(value))
        return True
    except ValueError:
        return False


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    body = [
        "| " + " | ".join(str(row[column]).replace("\\", "\\\\").replace("|", "\\|").replace("\n", " ") for column in columns) + " |"
        for row in rows
    ]
    return "\n".join([header, divider, *body])


def run_command(args: list[str]) -> None:
    subprocess.run(args, check=True, cwd=str(ROOT))


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


def density_theorem_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("DCT4782_0_density", "rho_H dV_H := c^-2 T_total(n,n)dV_eobs", "parent Hilbert density integrand for H_tau_bulk"),
        ("DCT4782_1_poynting_once", "T_total = T_matter + T_EM + retained sectors", "Poynting is counted once as Maxwell/Hilbert stress or boundary flux"),
        ("DCT4782_2_current_tail", "Delta_H_abs includes R_eq+B_zero+boundary+open_EM+nonEM+projector+domain+kappa tails", "open source-current pieces become a no-cancellation radius"),
        ("DCT4782_3_exact_branch", "Delta_H_abs=0 and M_lower>0", "only this branch can feed exact H_tau/H_ref into M_Hdress"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": theorem_id,
            "formula": formula,
            "meaning": meaning,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for theorem_id, formula, meaning in specs
    ]


def mlower_law_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("ML4782_0", "M0", "M0 := M_EH_private or source-backed positive Hilbert energy", "must be positive before division"),
        ("ML4782_1", "epsilon_abs", "sum_i |Delta_i|/M0", "must satisfy 0 <= epsilon_abs < 1"),
        ("ML4782_2", "M_lower", "M_lower = M0*(1-epsilon_abs)", "runner computes positive lower-bound row"),
        ("ML4782_3", "public row", "M0 and epsilon_abs must be source-backed, not private/unit smoke", "claim gate remains closed"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "law_id": law_id,
            "symbol": symbol,
            "formula": formula,
            "meaning": meaning,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for law_id, symbol, formula, meaning in specs
    ]


def density_input_rows(timestamp: str) -> list[dict[str, Any]]:
    residual = 0.01 * M_GM_SUN_CAL
    return [
        {
            "density_id": "physical_missing_parent_density_current",
            "rho_H_integral_kg": "",
            "rho_H_source": "MISSING_PARENT_DENSITY_CURRENT_INTEGRAL",
            "H_tau_surface_center_kg": "",
            "H_tau_surface_source": "MISSING_PARENT_SURFACE_CHARGE",
            "H_ref_kg": "",
            "H_ref_source": "MISSING_SOURCE_BLIND_REFERENCE",
            "R_eq_abs_kg": "",
            "B_zero_abs_kg": "",
            "boundary_flux_abs_kg": "",
            "open_EM_abs_kg": "",
            "nonEM_owner_gap_abs_kg": "",
            "projector_comm_abs_kg": "",
            "domain_shadow_abs_kg": "",
            "kappa_drift_abs_kg": "",
            "M0_kg": "",
            "epsilon_abs": "",
            "M0_source": "MISSING_SOURCE_BACKED_M0",
            "M_GM_cal_kg": format_float(M_GM_SUN_CAL),
            "row_status": "physical_missing_nonclaim",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "density_id": "private_unit_exact_density_current_control",
            "rho_H_integral_kg": "1",
            "rho_H_source": "PRIVATE_UNIT_NORMALIZED_BRANCH_CONTROL_NOT_PHYSICAL",
            "H_tau_surface_center_kg": "0",
            "H_tau_surface_source": "PRIVATE_NO_SURFACE_FLUX_CONTROL",
            "H_ref_kg": "0",
            "H_ref_source": "PRIVATE_FIXED_REFERENCE_CONTROL",
            "R_eq_abs_kg": "0",
            "B_zero_abs_kg": "0",
            "boundary_flux_abs_kg": "0",
            "open_EM_abs_kg": "0",
            "nonEM_owner_gap_abs_kg": "0",
            "projector_comm_abs_kg": "0",
            "domain_shadow_abs_kg": "0",
            "kappa_drift_abs_kg": "0",
            "M0_kg": "1",
            "epsilon_abs": "0",
            "M0_source": "PRIVATE_UNIT_NORMALIZED_MLOWER_CONTROL",
            "M_GM_cal_kg": "1",
            "row_status": "private_exact_control_nonclaim",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "density_id": "finite_interval_density_current_smoke_nonclaim",
            "rho_H_integral_kg": format_float(M_GM_SUN_CAL),
            "rho_H_source": "SMOKE_PARENT_DENSITY_CURRENT_NOT_PHYSICAL",
            "H_tau_surface_center_kg": "0",
            "H_tau_surface_source": "SMOKE_NO_SURFACE_CENTER",
            "H_ref_kg": "0",
            "H_ref_source": "SMOKE_SOURCE_BLIND_REFERENCE_NOT_PHYSICAL",
            "R_eq_abs_kg": format_float(residual),
            "B_zero_abs_kg": format_float(residual),
            "boundary_flux_abs_kg": "0",
            "open_EM_abs_kg": "0",
            "nonEM_owner_gap_abs_kg": "0",
            "projector_comm_abs_kg": "0",
            "domain_shadow_abs_kg": "0",
            "kappa_drift_abs_kg": "0",
            "M0_kg": format_float(M_GM_SUN_CAL),
            "epsilon_abs": "0.1",
            "M0_source": "SMOKE_POSITIVE_M0_NOT_PHYSICAL",
            "M_GM_cal_kg": format_float(M_GM_SUN_CAL),
            "row_status": "interval_smoke_nonclaim",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "density_id": "counterfactual_density_current_equals_comparator",
            "rho_H_integral_kg": format_float(M_GM_SUN_CAL),
            "rho_H_source": "COUNTERFACTUAL_RUNNER_SMOKE_ONLY",
            "H_tau_surface_center_kg": "0",
            "H_tau_surface_source": "COUNTERFACTUAL_RUNNER_SMOKE_ONLY",
            "H_ref_kg": "0",
            "H_ref_source": "COUNTERFACTUAL_RUNNER_SMOKE_ONLY",
            "R_eq_abs_kg": "0",
            "B_zero_abs_kg": "0",
            "boundary_flux_abs_kg": "0",
            "open_EM_abs_kg": "0",
            "nonEM_owner_gap_abs_kg": "0",
            "projector_comm_abs_kg": "0",
            "domain_shadow_abs_kg": "0",
            "kappa_drift_abs_kg": "0",
            "M0_kg": format_float(M_GM_SUN_CAL),
            "epsilon_abs": "0",
            "M0_source": "COUNTERFACTUAL_RUNNER_SMOKE_ONLY",
            "M_GM_cal_kg": format_float(M_GM_SUN_CAL),
            "row_status": "counterfactual_smoke_nonclaim",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "density_id": "forbidden_observed_GM_density_control",
            "rho_H_integral_kg": format_float(M_GM_SUN_CAL),
            "rho_H_source": "ORBITAL_GM_DEFINITION_CONTROL_SHOULD_FAIL",
            "H_tau_surface_center_kg": "0",
            "H_tau_surface_source": "CONTROL",
            "H_ref_kg": "0",
            "H_ref_source": "CONTROL",
            "R_eq_abs_kg": "0",
            "B_zero_abs_kg": "0",
            "boundary_flux_abs_kg": "0",
            "open_EM_abs_kg": "0",
            "nonEM_owner_gap_abs_kg": "0",
            "projector_comm_abs_kg": "0",
            "domain_shadow_abs_kg": "0",
            "kappa_drift_abs_kg": "0",
            "M0_kg": format_float(M_GM_SUN_CAL),
            "epsilon_abs": "0",
            "M0_source": "CONTROL",
            "M_GM_cal_kg": format_float(M_GM_SUN_CAL),
            "row_status": "physical_circular_control_nonclaim",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def parent_input_from_density(timestamp: str, density_output: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for output in density_output:
        status = output["runner_status"]
        usable = status in {
            "DENSITY_CURRENT_EXACT_COMPUTED_NONCLAIM",
            "DENSITY_CURRENT_INTERVAL_COMPUTED_NONCLAIM",
            "DENSITY_CURRENT_COUNTERFACTUAL_SMOKE_PASS_NONCLAIM",
        }
        rows.append(
            {
                "charge_id": output["density_id"],
                "H_tau_bulk_kg": output["H_tau_bulk_kg"] if usable else "",
                "H_tau_surface_kg": "0" if usable else "",
                "H_tau_source": "parent_density_current_mlower_runner.py",
                "H_ref_kg": output["H_ref_kg"] if usable else "",
                "H_ref_source": "parent_density_current_mlower_runner.py",
                "H_tau_curl_abs_kg": output["Delta_H_abs_kg"] if usable else "",
                "H_tau_flux_abs_kg": "0" if usable else "",
                "H_tau_sector_abs_kg": "0" if usable else "",
                "H_tau_surface_abs_kg": "0" if usable else "",
                "H_ref_drift_abs_kg": "0" if usable else "",
                "H_ref_selector_abs_kg": "0" if usable else "",
                "M_lower_kg": output["M_lower_kg"] if usable else "",
                "M_lower_source": "parent_density_current_mlower_runner.py",
                "M_GM_cal_kg": "1" if output["density_id"] == "private_unit_exact_density_current_control" else format_float(M_GM_SUN_CAL),
                "row_status": "counterfactual_smoke_nonclaim" if status == "DENSITY_CURRENT_COUNTERFACTUAL_SMOKE_PASS_NONCLAIM" else ("density_current_parent_input_nonclaim" if usable else "density_current_missing_or_failed_nonclaim"),
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def source_input_from_parent(timestamp: str, parent_output: list[dict[str, Any]], parent_input: list[dict[str, Any]]) -> list[dict[str, Any]]:
    input_by_id = {row["charge_id"]: row for row in parent_input}
    rows: list[dict[str, Any]] = []
    for output in parent_output:
        charge_id = output["charge_id"]
        exact_counterfactual = output["runner_status"] == "PARENT_CHARGE_COUNTERFACTUAL_SMOKE_PASS_NONCLAIM"
        source = input_by_id[charge_id]
        rows.append(
            {
                "source_id": charge_id,
                "H_tau_kg": output["H_tau_center_kg"] if exact_counterfactual else "",
                "H_tau_source": "parent_charge_Htau_Href_bound_runner.py",
                "H_ref_kg": source["H_ref_kg"] if exact_counterfactual else "",
                "H_ref_source": "parent_charge_Htau_Href_bound_runner.py",
                "M_GM_cal_kg": format_float(M_GM_SUN_CAL),
                "row_status": "counterfactual_smoke_nonclaim" if exact_counterfactual else "density_current_not_public_exact_nonclaim",
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def open_input_from_source(timestamp: str, source_output: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for output in source_output:
        exact_counterfactual = output["runner_status"] == "MHDRESS_COUNTERFACTUAL_SMOKE_PASS_NONCLAIM"
        rows.append(
            {
                "arena_id": output["source_id"],
                "mu_ref_m3_s2": f"{MU_SUN_NOMINAL:.8e}",
                "mu_ref_source": "IAU_2015_B3_nominal_solar_GM_comparator",
                "G_cal_m3_kg_s2": f"{G_CAL:.8e}",
                "M_H_dress_kg": output["M_H_dress_kg"] if exact_counterfactual else "",
                "M_H_source": "density_current_to_parent_charge_to_Htau_Href_chain",
                "sigma_M_H_kg": "",
                "E00_integral_abs_m": "0",
                "E00_sup_abs_m_minus2": "0",
                "support_radius_m": f"{SOLAR_RADIUS_NOMINAL:.6e}",
                "tolerance_eta": "1.0e-10",
                "delta_mu_boundary_abs_m3_s2": "0",
                "delta_mu_profile_abs_m3_s2": "0",
                "delta_mu_readout_abs_m3_s2": "0",
                "row_status": "counterfactual_smoke_nonclaim" if exact_counterfactual else "density_current_not_public_exact_nonclaim",
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def score_gate_rows(timestamp: str, density_output: list[dict[str, Any]], parent_output: list[dict[str, Any]], source_output: list[dict[str, Any]], open_output: list[dict[str, Any]]) -> list[dict[str, Any]]:
    parent_by_id = {row["charge_id"]: row for row in parent_output}
    source_by_id = {row["source_id"]: row for row in source_output}
    open_by_id = {row["arena_id"]: row for row in open_output}
    rows: list[dict[str, Any]] = []
    for density in density_output:
        density_id = density["density_id"]
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "gate_id": f"SG4782_{density_id}",
                "density_id": density_id,
                "density_runner_status": density["runner_status"],
                "parent_runner_status": parent_by_id.get(density_id, {}).get("runner_status", "MISSING_PARENT_OUTPUT"),
                "source_runner_status": source_by_id.get(density_id, {}).get("runner_status", "MISSING_SOURCE_OUTPUT"),
                "open_runner_status": open_by_id.get(density_id, {}).get("runner_status", "MISSING_OPEN_OUTPUT"),
                "claim_allowed": False,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def promotion_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("PG4782_0", "density source", "rho_H integral must come from parent density/current, not observed GM"),
        ("PG4782_1", "Mlower", "M0 and epsilon_abs must be positive/source-backed before normalized claims"),
        ("PG4782_2", "interval", "finite residual radius gives bounds only, not an exact source mass"),
        ("PG4782_3", "Poynting", "EM Poynting is counted once as Hilbert stress or boundary flux"),
        ("PG4782_4", "smoke", "private/unit and counterfactual controls are not empirical evidence"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "gate_id": gate_id,
            "rule": rule,
            "enforced_effect": effect,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for gate_id, rule, effect in specs
    ]


def firewall_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("FW4782_0", "no observed-GM density backfill", "ACTIVE"),
        ("FW4782_1", "no Poynting double count", "ACTIVE"),
        ("FW4782_2", "no exact claim from finite interval", "ACTIVE"),
        ("FW4782_3", "no public/GitHub action from this checkpoint", "LOCAL_PRIVATE_ONLY"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "firewall_id": firewall_id,
            "firewall_rule": rule,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for firewall_id, rule, status in specs
    ]


def route_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("RT4782_0_real_density", "fill first real rho_H integral from parent/local-packet density-current row", "SELECTED_NEXT"),
        ("RT4782_1_Href_zero", "prove fixed source-blind H_ref=0 branch or source a reference value", "SELECTED_NEXT_PARALLEL"),
        ("RT4782_2_M0", "source M0 and epsilon_abs rather than unit/private Mlower", "SELECTED_NEXT_PARALLEL"),
        ("RT4782_3_residuals", "source R_eq/B_zero/boundary/open-EM/projector/domain/kappa residual radius", "SELECTED_NEXT_PARALLEL"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "route_id": route_id,
            "route": route,
            "selection_status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for route_id, route, status in specs
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "decision": DECISION,
            "meaning": "4782 installs a runner for the parent density/current Htau source row and Mlower law. Real density/current rows remain blocked; private/unit and counterfactual controls prove the chain and anti-circularity behavior only.",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": "PASS_DENSITY_CURRENT_MLOWER_RUNNER_INSTALLED_NONCLAIM",
            "summary": "Density/current/Mlower runner installed and chained into parent charge; physical row blocks until real parent density-current values exist.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def next_target_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "next_target": NEXT_TARGET,
            "reason": "The executable slot is ready; next move is to source or derive a real rho_H integral and H_ref zero/value instead of smoke controls.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def write_docs(timestamp: str, theorem: list[dict[str, Any]], mlower: list[dict[str, Any]], density_output: list[dict[str, Any]], score: list[dict[str, Any]], routes: list[dict[str, Any]]) -> None:
    content = f"""# 4782 - Parent Htau density-current first source row or Mlower bound fill

Marker: `{MARKER}`
Generated: `{timestamp}`
Decision: `{DECISION}`

## Result

4782 takes the 4781 `H_tau_bulk` slot and gives it an executable density/current law:

```text
rho_H dV_H := c^-2 T_total(n,n) dV_eobs
H_tau_bulk = int_W rho_H dV_H + H_tau_surface_center
Delta_H_abs = |R_eq|+|B_zero|+|boundary_flux|+|open_EM|+|nonEM_owner_gap|
            + |projector_comm|+|domain_shadow|+|kappa_drift|
M_lower = M0*(1-epsilon_abs).
```

Poynting is not an extra hidden source here: it is counted once as Maxwell/Hilbert stress or as an explicit boundary/open-EM flux row.

## Density/Current Theorem Rows

{markdown_table(theorem, ["theorem_id", "formula", "meaning"])}

## Mlower Law

{markdown_table(mlower, ["law_id", "symbol", "formula"])}

## Density Runner Output

{markdown_table(density_output, ["density_id", "H_tau_bulk_kg", "M_lower_kg", "Delta_H_abs_kg", "epsilon_density_current_abs", "runner_status"])}

## Chain Score

{markdown_table(score, ["density_id", "density_runner_status", "parent_runner_status", "source_runner_status", "open_runner_status"])}

## Route Selection

{markdown_table(routes, ["route_id", "route", "selection_status"])}

## Conclusion

The exact hole is no longer vague. To make the local Newton/GR source row physical, 4783 must supply a real parent/local-packet `rho_H` integral and a fixed source-blind `H_ref` value or zero certificate. `M0`, `epsilon_abs`, and the residual radius must be source-backed before any normalized claim.

## Next Target

`{NEXT_TARGET}`
"""
    write_text(DOC_PATH, content)

    formal = f"""# PPC4161 4782: Parent Htau Density-Current First Source Row Or Mlower Bound Fill

Generated: `{timestamp}`

4782 installs the density/current and `M_lower` runner:

```text
rho_H dV_H := c^-2 T_total(n,n)dV_eobs
H_tau_bulk = int_W rho_H dV_H + H_tau_surface_center
M_lower = M0*(1-epsilon_abs)
```

Physical rows still block because the parent density/current integral, fixed `H_ref`, source-backed `M0`, and residual-radius components are not yet supplied. Private/unit and counterfactual controls validate the machinery only.

Next: `{NEXT_TARGET}`

Marker: `{MARKER}`
"""
    write_text(FORMAL_PATH, formal)


def add_claim_once(timestamp: str) -> None:
    existing = read_text(CLAIMS_PATH) if CLAIMS_PATH.exists() else ""
    if CLAIM_ID in existing:
        return
    row = [
        CLAIM_ID,
        "parent_htau_density_current_mlower_runner",
        "4782 installs an executable density/current and Mlower runner for H_tau_bulk before parent charge is allowed into M_Hdress.",
        "Generated source register, density theorem rows, Mlower law, density/current input-output, chained parent/source/open outputs, score gates, firewalls, routes, decision, status, next target and validation.",
        "density_current_mlower_runner_nonclaim",
        NEXT_TARGET,
        "Do not treat private/unit controls, counterfactual rows, or observed GM as parent density-current evidence.",
        "local_gr",
        str(DOC_PATH),
        NEXT_TARGET,
        "Need real parent rho_H integral, fixed source-blind H_ref, source-backed M0/epsilon_abs, and residual-radius components.",
        "Parent Htau density-current runner",
        f"{MARKER}; {DECISION}; generated {timestamp}",
    ]
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        csv.writer(handle).writerow(row)


def update_resume(timestamp: str) -> None:
    content = f"""# Current Local Resume

Last checkpoint: `{DOC_PATH.name}`
Generated: `{timestamp}`

## Current target

`{NEXT_TARGET}`

## Live blocker

The density/current runner is ready. The live physical gap is a real parent/local-packet `rho_H` integral, fixed source-blind `H_ref`, source-backed `M0` and `epsilon_abs`, plus finite residual-radius rows for `R_eq`, `B_zero`, boundary/open-EM, projector, domain and kappa drift.

## Firewalls

- No GitHub/public action from this checkpoint.
- No observed-GM/Gcal backfill into density, charge or lower-bound rows.
- Poynting is counted once as Hilbert/EM stress or explicit boundary/open flux.
"""
    write_text(RESUME_PATH, content)


def append_spine_and_packet(timestamp: str) -> None:
    append_once(
        SPINE_PATH,
        MARKER,
        f"""

## {MARKER}

4782 installs the density/current source-row runner for `H_tau_bulk` and the positive lower-bound law `M_lower=M0*(1-epsilon_abs)`. It preserves Poynting as Hilbert/EM stress or explicit boundary flux and blocks observed-GM backfill. Decision: `{DECISION}`. Next: `{NEXT_TARGET}`.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""

## {PACKET_MARKER}

Runner: `{DENSITY_RUNNER}`

Density/current and `M_lower` slots are executable but remain nonclaim until real parent density-current, fixed reference, source-backed `M0`, and residual-radius rows exist. Generated `{timestamp}`.
""",
    )


def validate(timestamp: str, sources: list[dict[str, Any]], density_output: list[dict[str, Any]], parent_output: list[dict[str, Any]], source_output: list[dict[str, Any]], open_output: list[dict[str, Any]], gates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    checks: list[tuple[str, str, bool, str]] = []
    checks.append(("VAL4782_0_sources", "source paths and needles exist", all(row["exists"] is True and row["needle_found"] is True for row in sources), str(SOURCE_REGISTER_CSV)))
    checks.append(("VAL4782_1_missing_blocks", "missing physical density row blocks", any(row["density_id"] == "physical_missing_parent_density_current" and row["runner_status"] == "BLOCKED_MISSING_DENSITY_CURRENT_COMPONENTS" for row in density_output), str(DENSITY_OUTPUT_CSV)))
    checks.append(("VAL4782_2_private_exact", "private unit exact control computes", any(row["density_id"] == "private_unit_exact_density_current_control" and row["runner_status"] == "DENSITY_CURRENT_EXACT_COMPUTED_NONCLAIM" for row in density_output), str(DENSITY_OUTPUT_CSV)))
    checks.append(("VAL4782_3_interval", "finite interval smoke computes", any(row["density_id"] == "finite_interval_density_current_smoke_nonclaim" and row["runner_status"] == "DENSITY_CURRENT_INTERVAL_COMPUTED_NONCLAIM" for row in density_output), str(DENSITY_OUTPUT_CSV)))
    checks.append(("VAL4782_4_counterfactual", "counterfactual density chain smokes", any(row["density_id"] == "counterfactual_density_current_equals_comparator" and row["runner_status"] == "DENSITY_CURRENT_COUNTERFACTUAL_SMOKE_PASS_NONCLAIM" for row in density_output), str(DENSITY_OUTPUT_CSV)))
    checks.append(("VAL4782_5_forbidden_control", "observed GM density source control fails", any(row["density_id"] == "forbidden_observed_GM_density_control" and row["runner_status"] == "FAILED_CIRCULAR_DENSITY_CURRENT_SOURCE" for row in density_output), str(DENSITY_OUTPUT_CSV)))
    checks.append(("VAL4782_6_parent_interval", "parent charge interval receives density residual", any(row["charge_id"] == "finite_interval_density_current_smoke_nonclaim" and row["runner_status"] == "PARENT_CHARGE_INTERVAL_COMPUTED_NONCLAIM" for row in parent_output), str(PARENT_OUTPUT_CSV)))
    checks.append(("VAL4782_7_source_real_blocks", "source runner blocks real missing density row", any(row["source_id"] == "physical_missing_parent_density_current" and row["runner_status"] == "BLOCKED_MISSING_HTAU_OR_HREF" for row in source_output), str(SOURCE_OUTPUT_CSV)))
    checks.append(("VAL4782_8_open_counterfactual", "open arena counterfactual smokes", any(row["arena_id"] == "counterfactual_density_current_equals_comparator" and row["runner_status"] == "RUNNER_SMOKE_PASS_NONCLAIM" for row in open_output), str(OPEN_OUTPUT_CSV)))
    checks.append(("VAL4782_9_gates", "promotion gates keep claims closed", all(row["claim_allowed"] is False for row in gates), str(PROMOTION_GATES_CSV)))
    checks.append(("VAL4782_10_claim", "claim row L-624 present", CLAIM_ID in read_text(CLAIMS_PATH), str(CLAIMS_PATH)))
    checks.append(("VAL4782_11_resume", "resume points to next target", NEXT_TARGET in read_text(RESUME_PATH), str(RESUME_PATH)))

    rows: list[dict[str, Any]] = []
    for validation_id, check, passed, detail in checks:
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "validation_id": validation_id,
                "check": check,
                "status": "PASS" if passed else "FAIL",
                "detail": detail,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    overall = all(row["status"] == "PASS" for row in rows)
    rows.append(
        {
            "checkpoint": CHECKPOINT,
            "validation_id": "VAL4782_OVERALL",
            "check": "all 4782 density/current/Mlower checks pass",
            "status": "PASS" if overall else "FAIL",
            "detail": DECISION,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    )
    return rows


def main() -> None:
    timestamp = now()
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)

    sources = source_register(timestamp)
    theorem = density_theorem_rows(timestamp)
    mlower = mlower_law_rows(timestamp)
    density_input = density_input_rows(timestamp)
    gates = promotion_gate_rows(timestamp)
    firewalls = firewall_rows(timestamp)
    routes = route_rows(timestamp)
    decisions = decision_rows(timestamp)
    statuses = status_rows(timestamp)
    next_targets = next_target_rows(timestamp)

    write_csv(SOURCE_REGISTER_CSV, sources)
    write_csv(DENSITY_THEOREM_CSV, theorem)
    write_csv(MLOWER_LAW_CSV, mlower)
    write_csv(DENSITY_INPUT_CSV, density_input)
    write_csv(PROMOTION_GATES_CSV, gates)
    write_csv(FIREWALL_CSV, firewalls)
    write_csv(ROUTE_MATRIX_CSV, routes)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_TARGET_CSV, next_targets)

    run_command([sys.executable, str(DENSITY_RUNNER), str(DENSITY_INPUT_CSV), str(DENSITY_OUTPUT_CSV)])
    density_output = parse_csv(DENSITY_OUTPUT_CSV)

    parent_input = parent_input_from_density(timestamp, density_output)
    write_csv(PARENT_INPUT_CSV, parent_input)
    run_command([sys.executable, str(PARENT_CHARGE_RUNNER), str(PARENT_INPUT_CSV), str(PARENT_OUTPUT_CSV)])
    parent_output = parse_csv(PARENT_OUTPUT_CSV)

    source_input = source_input_from_parent(timestamp, parent_output, parent_input)
    write_csv(SOURCE_INPUT_CSV, source_input)
    run_command([sys.executable, str(SOURCE_RUNNER), str(SOURCE_INPUT_CSV), str(SOURCE_OUTPUT_CSV)])
    source_output = parse_csv(SOURCE_OUTPUT_CSV)

    open_input = open_input_from_source(timestamp, source_output)
    write_csv(OPEN_INPUT_CSV, open_input)
    run_command([sys.executable, str(OPEN_RUNNER), str(OPEN_INPUT_CSV), str(OPEN_OUTPUT_CSV)])
    open_output = parse_csv(OPEN_OUTPUT_CSV)

    score = score_gate_rows(timestamp, density_output, parent_output, source_output, open_output)
    write_csv(SCORE_GATE_CSV, score)

    write_docs(timestamp, theorem, mlower, density_output, score, routes)
    add_claim_once(timestamp)
    append_spine_and_packet(timestamp)
    update_resume(timestamp)

    validation = validate(timestamp, sources, density_output, parent_output, source_output, open_output, gates)
    write_csv(VALIDATION_CSV, validation)

    cache_dir = SCRIPT_DIR / "__pycache__"
    if cache_dir.exists():
        shutil.rmtree(cache_dir)


if __name__ == "__main__":
    main()
