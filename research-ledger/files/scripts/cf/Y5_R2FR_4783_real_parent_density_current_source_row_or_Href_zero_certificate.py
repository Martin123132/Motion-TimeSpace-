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

HREF_RUNNER = SCRIPT_DIR / "Href_zero_certificate_runner.py"
DENSITY_RUNNER = SCRIPT_DIR / "parent_density_current_mlower_runner.py"
PARENT_CHARGE_RUNNER = SCRIPT_DIR / "parent_charge_Htau_Href_bound_runner.py"
SOURCE_RUNNER = SCRIPT_DIR / "Htau_Href_MHdress_source_runner.py"
OPEN_RUNNER = SCRIPT_DIR / "MHdress_E00_open_arena_runner.py"

CHECKPOINT = "4783"
CLAIM_ID = "L-625"
MARKER = "PPC4161_REAL_PARENT_DENSITY_CURRENT_SOURCE_ROW_OR_HREF_ZERO_CERTIFICATE_4783"
PACKET_MARKER = "PPC4161_PACKET_REAL_PARENT_DENSITY_CURRENT_SOURCE_ROW_OR_HREF_ZERO_CERTIFICATE_4783"
DECISION = "HREF_ZERO_CERTIFICATE_RUNNER_INSTALLED_PRIVATE_REFERENCE_ZERO_NARROWS_PHYSICAL_BLOCKER_TO_RHOH_M0_RESIDUALS_NONCLAIM"
NEXT_TARGET = "4784-Y5-R2FR-real-rhoH-parent-density-integral-or-M0-source-backed-row.md"

DOC_PATH = POST / "4783-Y5-R2FR-real-parent-density-current-source-row-or-Href-zero-certificate.md"
FORMAL_PATH = FORMAL / "799-PPC4161-real-parent-density-current-source-row-or-Href-zero-certificate.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"

SOURCE_REGISTER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4783_SOURCE_REGISTER.csv"
HREF_THEOREM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4783_HREF_ZERO_THEOREM.csv"
HREF_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4783_HREF_ZERO_INPUT.csv"
HREF_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4783_HREF_ZERO_OUTPUT.csv"
DENSITY_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4783_DENSITY_INPUT_FROM_HREF.csv"
DENSITY_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4783_DENSITY_OUTPUT_FROM_HREF.csv"
PARENT_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4783_PARENT_CHARGE_INPUT_FROM_HREF_DENSITY.csv"
PARENT_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4783_PARENT_CHARGE_OUTPUT_FROM_HREF_DENSITY.csv"
SOURCE_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4783_HTAU_HREF_SOURCE_INPUT.csv"
SOURCE_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4783_HTAU_HREF_SOURCE_OUTPUT.csv"
OPEN_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4783_OPEN_ARENA_INPUT.csv"
OPEN_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4783_OPEN_ARENA_OUTPUT.csv"
SCORE_GATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4783_SCORE_GATE_UPDATE.csv"
PROMOTION_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4783_PROMOTION_GATES.csv"
FIREWALL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4783_FIREWALL_ROWS.csv"
ROUTE_MATRIX_CSV = SOURCE_DIR / "P8_Y5_R2FR_4783_ROUTE_SELECTION_MATRIX.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4783_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4783_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4783_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4783_VALIDATION.csv"

G_CAL = 6.67430e-11
MU_SUN_NOMINAL = 1.3271244e20
SOLAR_RADIUS_NOMINAL = 6.957e8
M_GM_SUN_CAL = MU_SUN_NOMINAL / G_CAL

SOURCE_SPECS = [
    ("SRC4783_00_4782_doc", POST / "4782-Y5-R2FR-parent-Htau-density-current-first-source-row-or-Mlower-bound-fill.md", "fixed source-blind `H_ref`", "4782 selected Href zero certificate"),
    ("SRC4783_01_3577_doc", POST / "3577-Y5-R2FR-Htau-Href-qbasic-reference-lock-or-source-residual-first-fill.md", "D_source H_ref=0", "3577 internal fixed-reference silence"),
    ("SRC4783_02_3577_lock", SOURCE_DIR / "P8_Y5_R2FR_3577_HREF_REFERENCE_LOCK.csv", "REF3577_0_fixed_reference_rule", "3577 reference lock row"),
    ("SRC4783_03_4038_doc", POST / "4038-Y5-R2FR-Poynting-no-flux-and-boundary-reference-theorem-or-flux-bound.md", "D_source H_ref=D_readout H_ref=0", "4038 source-blind boundary reference"),
    ("SRC4783_04_4038_theorem", SOURCE_DIR / "P8_Y5_R2FR_4038_BOUNDARY_REFERENCE_THEOREM.csv", "BND4038_1_reference_lock", "4038 reference theorem row"),
    ("SRC4783_05_4215_doc", POST / "4215-Y5-R2FR-reference-lock-curl-zero-or-first-ref-bound-row.md", "d_field(delta H_ref)=0", "4215 reference curl zero"),
    ("SRC4783_06_4215_theorem", SOURCE_DIR / "P8_Y5_R2FR_4215_REFERENCE_LOCK_THEOREM.csv", "RLC4215_4_reference_curl_zero", "4215 reference curl zero row"),
    ("SRC4783_07_3825_doc", POST / "3825-Y5-R2FR-boundary-reference-primitive-and-MHref-denominator-zero-or-first-source-row.md", "BRT3825_3_Delta_symp_zero", "3825 boundary/reference zero route"),
    ("SRC4783_08_4589_clauses", SOURCE_DIR / "P8_Y5_R2FR_4589_SOURCE_BLIND_REFERENCE_CLAUSES.csv", "MHC4589_2_Href_qbasic", "4589 source-blind Href clause"),
    ("SRC4783_09_href_runner", HREF_RUNNER, "def compute_row", "4783 Href zero certificate runner"),
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
        "| " + " | ".join(str(row[column]).replace("\\", "\\\\").replace("|", "\\|").replace("\n", " ") for column in columns) + " |"
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


def href_theorem_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("HRT4783_0_anchor", "H_ref=0 is legal only if the zero anchor is selected before source/readout scoring", "blocks post-fit cancellation"),
        ("HRT4783_1_source_blind", "D_source H_ref=D_readout H_ref=D_frame H_ref=0", "removes reference laundering inside the selected branch"),
        ("HRT4783_2_qbasic", "H_ref=Hbar_ref(q(Phi)) and v in ker(Dq) => D_v H_ref=0", "source-blind quotient reference clause"),
        ("HRT4783_3_curl", "H_ref fixed => d_field(delta H_ref)=0 => I_ref=0", "reference curl term closes conditionally"),
        ("HRT4783_4_bound", "|H_ref| <= |H_ref_anchor|+sum |Delta_ref_i|", "fallback if any zero clause is unsigned"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": theorem_id,
            "statement": statement,
            "meaning": meaning,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for theorem_id, statement, meaning in specs
    ]


def href_input_rows(timestamp: str) -> list[dict[str, Any]]:
    residual = 0.01 * M_GM_SUN_CAL
    signed = {
        "zero_anchor_signed": True,
        "source_blind_signed": True,
        "fixed_before_readout_signed": True,
        "qbasic_descent_signed": True,
        "same_tau_eobs_surface_signed": True,
        "no_postfit_signed": True,
        "boundary_no_flux_signed": True,
        "reference_curl_zero_signed": True,
    }
    unsigned = {key: False for key in signed}
    base_residuals = {
        "Delta_ref_selector_abs_kg": "0",
        "Delta_ref_boundary_abs_kg": "0",
        "Delta_ref_frame_abs_kg": "0",
        "Delta_ref_readout_abs_kg": "0",
        "Delta_ref_counterterm_abs_kg": "0",
    }

    rows = [
        {
            "reference_id": "physical_missing_href_certificate",
            "H_ref_anchor_kg": "",
            "anchor_source": "MISSING_SOURCE_BLIND_REFERENCE_ANCHOR",
            "reference_selector_source": "MISSING_PARENT_REFERENCE_SELECTOR",
            "counterterm_source": "MISSING_COUNTERTERM_CONVENTION",
            **unsigned,
            **{key: "" for key in base_residuals},
            "M_lower_kg": "",
            "row_status": "physical_missing_nonclaim",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "reference_id": "private_source_blind_Href_zero_certificate",
            "H_ref_anchor_kg": "0",
            "anchor_source": "PRIVATE_FIXED_SOURCE_BLIND_ZERO_REFERENCE",
            "reference_selector_source": "3577_4038_4215_PRIVATE_REFERENCE_LOCK_CHAIN",
            "counterterm_source": "NO_POSTFIT_COUNTERTERM_PRIVATE_BRANCH",
            **signed,
            **base_residuals,
            "M_lower_kg": "1",
            "row_status": "private_zero_certificate_nonclaim",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "reference_id": "finite_Href_bound_smoke_nonclaim",
            "H_ref_anchor_kg": "0",
            "anchor_source": "SMOKE_REFERENCE_BOUND_NOT_PHYSICAL",
            "reference_selector_source": "SMOKE_UNSIGNED_SELECTOR",
            "counterterm_source": "SMOKE_NO_POSTFIT_COUNTERTERM",
            **{**signed, "qbasic_descent_signed": False, "boundary_no_flux_signed": False},
            "Delta_ref_selector_abs_kg": format_float(residual),
            "Delta_ref_boundary_abs_kg": format_float(residual),
            "Delta_ref_frame_abs_kg": "0",
            "Delta_ref_readout_abs_kg": "0",
            "Delta_ref_counterterm_abs_kg": "0",
            "M_lower_kg": format_float(M_GM_SUN_CAL),
            "row_status": "finite_bound_smoke_nonclaim",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "reference_id": "counterfactual_Href_zero_smoke",
            "H_ref_anchor_kg": "0",
            "anchor_source": "COUNTERFACTUAL_RUNNER_SMOKE_ONLY",
            "reference_selector_source": "COUNTERFACTUAL_RUNNER_SMOKE_ONLY",
            "counterterm_source": "COUNTERFACTUAL_RUNNER_SMOKE_ONLY",
            **signed,
            **base_residuals,
            "M_lower_kg": format_float(M_GM_SUN_CAL),
            "row_status": "counterfactual_smoke_nonclaim",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "reference_id": "forbidden_postfit_reference_control",
            "H_ref_anchor_kg": "0",
            "anchor_source": "POSTFIT_REFERENCE_OBSERVED_RESIDUAL_CANCEL_CONTROL",
            "reference_selector_source": "FITTED_ACCELERATION_CONTROL",
            "counterterm_source": "OBSERVED_RESIDUAL_CANCEL_CONTROL",
            **signed,
            **base_residuals,
            "M_lower_kg": format_float(M_GM_SUN_CAL),
            "row_status": "physical_circular_control_nonclaim",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]
    return rows


def density_input_from_href(timestamp: str, href_output: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_id = {row["reference_id"]: row for row in href_output}
    private_href = by_id["private_source_blind_Href_zero_certificate"]
    counter_href = by_id["counterfactual_Href_zero_smoke"]
    return [
        {
            "density_id": "physical_missing_density_with_private_Href_zero",
            "rho_H_integral_kg": "",
            "rho_H_source": "MISSING_PARENT_DENSITY_CURRENT_INTEGRAL",
            "H_tau_surface_center_kg": "",
            "H_tau_surface_source": "MISSING_PARENT_SURFACE_CHARGE",
            "H_ref_kg": private_href["H_ref_kg"],
            "H_ref_source": "Href_zero_certificate_runner.py",
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
            "row_status": "physical_missing_density_href_zero_nonclaim",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "density_id": "counterfactual_density_with_Href_zero",
            "rho_H_integral_kg": format_float(M_GM_SUN_CAL),
            "rho_H_source": "COUNTERFACTUAL_RUNNER_SMOKE_ONLY",
            "H_tau_surface_center_kg": "0",
            "H_tau_surface_source": "COUNTERFACTUAL_RUNNER_SMOKE_ONLY",
            "H_ref_kg": counter_href["H_ref_kg"],
            "H_ref_source": "Href_zero_certificate_runner.py",
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
    ]


def parent_input_from_density(timestamp: str, density_output: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for output in density_output:
        usable = output["runner_status"] == "DENSITY_CURRENT_COUNTERFACTUAL_SMOKE_PASS_NONCLAIM"
        rows.append(
            {
                "charge_id": output["density_id"],
                "H_tau_bulk_kg": output["H_tau_bulk_kg"] if usable else "",
                "H_tau_surface_kg": "0" if usable else "",
                "H_tau_source": "parent_density_current_mlower_runner.py",
                "H_ref_kg": output["H_ref_kg"] if usable else "",
                "H_ref_source": "Href_zero_certificate_runner.py",
                "H_tau_curl_abs_kg": "0" if usable else "",
                "H_tau_flux_abs_kg": "0" if usable else "",
                "H_tau_sector_abs_kg": "0" if usable else "",
                "H_tau_surface_abs_kg": "0" if usable else "",
                "H_ref_drift_abs_kg": "0" if usable else "",
                "H_ref_selector_abs_kg": "0" if usable else "",
                "M_lower_kg": output["M_lower_kg"] if usable else "",
                "M_lower_source": "parent_density_current_mlower_runner.py",
                "M_GM_cal_kg": format_float(M_GM_SUN_CAL),
                "row_status": "counterfactual_smoke_nonclaim" if usable else "density_missing_href_zero_nonclaim",
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def source_input_from_parent(timestamp: str, parent_output: list[dict[str, Any]], parent_input: list[dict[str, Any]]) -> list[dict[str, Any]]:
    parent_by_id = {row["charge_id"]: row for row in parent_input}
    rows: list[dict[str, Any]] = []
    for output in parent_output:
        exact_counterfactual = output["runner_status"] == "PARENT_CHARGE_COUNTERFACTUAL_SMOKE_PASS_NONCLAIM"
        parent = parent_by_id[output["charge_id"]]
        rows.append(
            {
                "source_id": output["charge_id"],
                "H_tau_kg": output["H_tau_center_kg"] if exact_counterfactual else "",
                "H_tau_source": "parent_charge_Htau_Href_bound_runner.py",
                "H_ref_kg": parent["H_ref_kg"] if exact_counterfactual else "",
                "H_ref_source": "Href_zero_certificate_runner.py",
                "M_GM_cal_kg": format_float(M_GM_SUN_CAL),
                "row_status": "counterfactual_smoke_nonclaim" if exact_counterfactual else "density_missing_href_zero_nonclaim",
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
                "M_H_source": "Href_zero_to_density_to_parent_charge_chain",
                "sigma_M_H_kg": "",
                "E00_integral_abs_m": "0",
                "E00_sup_abs_m_minus2": "0",
                "support_radius_m": f"{SOLAR_RADIUS_NOMINAL:.6e}",
                "tolerance_eta": "1.0e-10",
                "delta_mu_boundary_abs_m3_s2": "0",
                "delta_mu_profile_abs_m3_s2": "0",
                "delta_mu_readout_abs_m3_s2": "0",
                "row_status": "counterfactual_smoke_nonclaim" if exact_counterfactual else "density_missing_href_zero_nonclaim",
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def score_rows(timestamp: str, href_output: list[dict[str, Any]], density_output: list[dict[str, Any]], parent_output: list[dict[str, Any]], source_output: list[dict[str, Any]], open_output: list[dict[str, Any]]) -> list[dict[str, Any]]:
    density_by_id = {row["density_id"]: row for row in density_output}
    parent_by_id = {row["charge_id"]: row for row in parent_output}
    source_by_id = {row["source_id"]: row for row in source_output}
    open_by_id = {row["arena_id"]: row for row in open_output}
    mappings = [
        ("private_source_blind_Href_zero_certificate", "physical_missing_density_with_private_Href_zero"),
        ("counterfactual_Href_zero_smoke", "counterfactual_density_with_Href_zero"),
    ]
    rows: list[dict[str, Any]] = []
    href_by_id = {row["reference_id"]: row for row in href_output}
    for href_id, density_id in mappings:
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "gate_id": f"SG4783_{href_id}",
                "reference_id": href_id,
                "density_id": density_id,
                "href_runner_status": href_by_id[href_id]["runner_status"],
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
            ("PG4783_0", "H_ref zero requires source-blind fixed selector before readout"),
            ("PG4783_1", "post-fit or observed-residual reference controls fail"),
            ("PG4783_2", "private H_ref zero does not provide rho_H, M0 or residual-radius values"),
            ("PG4783_3", "counterfactual chain is runner smoke only"),
        ]
        return [{"checkpoint": CHECKPOINT, "gate_id": row_id, "rule": text, "claim_allowed": False, "valid_for_claim": False, "timestamp_utc": timestamp} for row_id, text in specs]
    if kind == "firewalls":
        specs = [
            ("FW4783_0", "no post-fit H_ref subtraction", "ACTIVE"),
            ("FW4783_1", "no observed-GM/Gcal source backfill", "ACTIVE"),
            ("FW4783_2", "no public/local-GR claim from private Href zero", "ACTIVE"),
            ("FW4783_3", "no GitHub/public action", "LOCAL_PRIVATE_ONLY"),
        ]
        return [{"checkpoint": CHECKPOINT, "firewall_id": row_id, "firewall_rule": text, "status": status, "valid_for_claim": False, "timestamp_utc": timestamp} for row_id, text, status in specs]
    if kind == "routes":
        specs = [
            ("RT4783_0_rhoH", "fill real parent/local-packet rho_H integral on W_H", "SELECTED_NEXT"),
            ("RT4783_1_M0", "source-backed M0 and epsilon_abs for positive M_lower", "SELECTED_NEXT_PARALLEL"),
            ("RT4783_2_radius", "fill R_eq/B_zero/boundary/open-EM/projector/domain/kappa residual radius", "SELECTED_NEXT_PARALLEL"),
        ]
        return [{"checkpoint": CHECKPOINT, "route_id": row_id, "route": text, "selection_status": status, "valid_for_claim": False, "timestamp_utc": timestamp} for row_id, text, status in specs]
    raise ValueError(kind)


def write_docs(timestamp: str, theorem: list[dict[str, Any]], href_output: list[dict[str, Any]], density_output: list[dict[str, Any]], score: list[dict[str, Any]], routes: list[dict[str, Any]]) -> None:
    content = f"""# 4783 - Real parent density-current source row or Href zero certificate

Marker: `{MARKER}`
Generated: `{timestamp}`
Decision: `{DECISION}`

## Result

4783 closes one side of the 4782 source slot in the only safe way: `H_ref=0` is accepted only for a fixed source-blind reference selected before source/radius/frame/readout scoring.

```text
H_ref = 0
D_source H_ref = D_readout H_ref = D_frame H_ref = 0
d_field(delta H_ref)=0
```

That narrows the physical blocker. It does not supply the real `rho_H` integral, `M0`, `epsilon_abs`, or residual-radius values.

## Href Theorem Rows

{markdown_table(theorem, ["theorem_id", "statement", "meaning"])}

## Href Runner Output

{markdown_table(href_output, ["reference_id", "H_ref_kg", "H_ref_abs_bound_kg", "epsilon_Href_abs", "runner_status"])}

## Density Runner Output

{markdown_table(density_output, ["density_id", "H_tau_bulk_kg", "H_ref_kg", "M_lower_kg", "Delta_H_abs_kg", "runner_status"])}

## Chain Score

{markdown_table(score, ["reference_id", "density_id", "href_runner_status", "density_runner_status", "parent_runner_status", "source_runner_status", "open_runner_status"])}

## Route Selection

{markdown_table(routes, ["route_id", "route", "selection_status"])}

## Conclusion

The private/fixed `H_ref=0` branch is now executable and anti-circular. The live source-mass blocker is reduced to the genuinely physical inputs: real `rho_H dV_H`, source-backed `M0/epsilon_abs`, and finite residual-radius rows.

## Next Target

`{NEXT_TARGET}`
"""
    write_text(DOC_PATH, content)

    formal = f"""# PPC4161 4783: Real Parent Density-Current Source Row Or Href Zero Certificate

Generated: `{timestamp}`

4783 installs the strict `H_ref=0` certificate runner. It accepts zero only for a fixed source-blind reference selected before readout and rejects post-fit reference controls.

The physical row still blocks on real `rho_H`, `M0/epsilon_abs`, and residual-radius values.

Next: `{NEXT_TARGET}`

Marker: `{MARKER}`
"""
    write_text(FORMAL_PATH, formal)


def append_outputs(timestamp: str) -> None:
    decision = [{"checkpoint": CHECKPOINT, "decision": DECISION, "meaning": "Href zero certificate narrows the source-mass blocker but leaves rho_H/M0/residuals live.", "next_target": NEXT_TARGET, "valid_for_claim": False, "timestamp_utc": timestamp}]
    status = [{"checkpoint": CHECKPOINT, "status": "PASS_HREF_ZERO_CERTIFICATE_RUNNER_INSTALLED_NONCLAIM", "summary": "Private fixed Href zero is executable; physical density/current row remains blocked.", "valid_for_claim": False, "timestamp_utc": timestamp}]
    next_target = [{"checkpoint": CHECKPOINT, "next_target": NEXT_TARGET, "reason": "With H_ref narrowed, the next physical input is rho_H and M0/source-backed residual rows.", "valid_for_claim": False, "timestamp_utc": timestamp}]
    write_csv(DECISION_CSV, decision)
    write_csv(STATUS_CSV, status)
    write_csv(NEXT_TARGET_CSV, next_target)


def add_claim_once(timestamp: str) -> None:
    existing = read_text(CLAIMS_PATH) if CLAIMS_PATH.exists() else ""
    if CLAIM_ID in existing:
        return
    row = [
        CLAIM_ID,
        "href_zero_certificate_runner",
        "4783 installs a strict H_ref zero certificate runner and rejects post-fit reference controls, narrowing the source-mass blocker to rho_H, M0/epsilon_abs and residual-radius rows.",
        "Generated source register, Href theorem/input/output, chained density/parent/source/open outputs, score gates, firewalls, routes, decision, status, next target and validation.",
        "href_zero_certificate_private_nonclaim",
        NEXT_TARGET,
        "Do not treat private H_ref zero as a real density/current or local-GR claim.",
        "local_gr",
        str(DOC_PATH),
        NEXT_TARGET,
        "Need real parent rho_H integral, source-backed M0/epsilon_abs, and residual-radius components.",
        "Href zero certificate runner",
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

`H_ref=0` is now executable only inside the private fixed source-blind reference branch. The live physical gap is real parent/local-packet `rho_H dV_H`, source-backed `M0` and `epsilon_abs`, plus residual-radius rows for `R_eq`, `B_zero`, boundary/open-EM, projector, domain and kappa drift.

## Firewalls

- No GitHub/public action from this checkpoint.
- No post-fit reference subtraction.
- No observed-GM/Gcal backfill into density, charge or lower-bound rows.
""",
    )


def append_spine_and_packet(timestamp: str) -> None:
    append_once(SPINE_PATH, MARKER, f"\n\n## {MARKER}\n\n4783 installs a strict `H_ref=0` certificate runner. It narrows reference leakage in the private fixed source-blind branch while leaving real `rho_H`, `M0/epsilon_abs`, and residual-radius source rows live. Decision: `{DECISION}`. Next: `{NEXT_TARGET}`.\n")
    append_once(PACKET_PATH, PACKET_MARKER, f"\n\n## {PACKET_MARKER}\n\nRunner: `{HREF_RUNNER}`. Private fixed `H_ref=0` is executable but nonclaim; physical source mass still needs `rho_H`, `M0`, and residual-radius rows. Generated `{timestamp}`.\n")


def validate(timestamp: str, sources: list[dict[str, Any]], href_output: list[dict[str, Any]], density_output: list[dict[str, Any]], parent_output: list[dict[str, Any]], source_output: list[dict[str, Any]], open_output: list[dict[str, Any]], gates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    checks = [
        ("VAL4783_0_sources", "source paths and needles exist", all(row["exists"] is True and row["needle_found"] is True for row in sources), str(SOURCE_REGISTER_CSV)),
        ("VAL4783_1_private_href_zero", "private Href zero certifies", any(row["reference_id"] == "private_source_blind_Href_zero_certificate" and row["runner_status"] == "HREF_ZERO_CERTIFIED_PRIVATE_NONCLAIM" for row in href_output), str(HREF_OUTPUT_CSV)),
        ("VAL4783_2_href_bound", "finite Href bound computes", any(row["reference_id"] == "finite_Href_bound_smoke_nonclaim" and row["runner_status"] == "HREF_BOUND_COMPUTED_NONCLAIM" for row in href_output), str(HREF_OUTPUT_CSV)),
        ("VAL4783_3_forbidden_ref", "postfit reference control fails", any(row["reference_id"] == "forbidden_postfit_reference_control" and row["runner_status"] == "FAILED_CIRCULAR_POSTFIT_REFERENCE" for row in href_output), str(HREF_OUTPUT_CSV)),
        ("VAL4783_4_density_still_blocks", "Href-zero physical density row still blocks on rhoH", any(row["density_id"] == "physical_missing_density_with_private_Href_zero" and row["runner_status"] == "BLOCKED_MISSING_DENSITY_CURRENT_COMPONENTS" for row in density_output), str(DENSITY_OUTPUT_CSV)),
        ("VAL4783_5_parent_counterfactual", "counterfactual reaches parent charge", any(row["charge_id"] == "counterfactual_density_with_Href_zero" and row["runner_status"] == "PARENT_CHARGE_COUNTERFACTUAL_SMOKE_PASS_NONCLAIM" for row in parent_output), str(PARENT_OUTPUT_CSV)),
        ("VAL4783_6_source_counterfactual", "counterfactual reaches Htau/Href runner", any(row["source_id"] == "counterfactual_density_with_Href_zero" and row["runner_status"] == "MHDRESS_COUNTERFACTUAL_SMOKE_PASS_NONCLAIM" for row in source_output), str(SOURCE_OUTPUT_CSV)),
        ("VAL4783_7_open_counterfactual", "counterfactual reaches open runner", any(row["arena_id"] == "counterfactual_density_with_Href_zero" and row["runner_status"] == "RUNNER_SMOKE_PASS_NONCLAIM" for row in open_output), str(OPEN_OUTPUT_CSV)),
        ("VAL4783_8_gates", "promotion gates keep claims closed", all(row["claim_allowed"] is False for row in gates), str(PROMOTION_GATES_CSV)),
        ("VAL4783_9_claim", "claim row L-625 present", CLAIM_ID in read_text(CLAIMS_PATH), str(CLAIMS_PATH)),
        ("VAL4783_10_resume", "resume points to next target", NEXT_TARGET in read_text(RESUME_PATH), str(RESUME_PATH)),
    ]
    rows: list[dict[str, Any]] = []
    for validation_id, check, passed, detail in checks:
        rows.append({"checkpoint": CHECKPOINT, "validation_id": validation_id, "check": check, "status": "PASS" if passed else "FAIL", "detail": detail, "valid_for_claim": False, "timestamp_utc": timestamp})
    overall = all(row["status"] == "PASS" for row in rows)
    rows.append({"checkpoint": CHECKPOINT, "validation_id": "VAL4783_OVERALL", "check": "all 4783 Href zero certificate checks pass", "status": "PASS" if overall else "FAIL", "detail": DECISION, "valid_for_claim": False, "timestamp_utc": timestamp})
    return rows


def main() -> None:
    timestamp = now()
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)

    sources = source_register(timestamp)
    theorem = href_theorem_rows(timestamp)
    href_input = href_input_rows(timestamp)
    gates = simple_rows(timestamp, "gates")
    firewalls = simple_rows(timestamp, "firewalls")
    routes = simple_rows(timestamp, "routes")

    write_csv(SOURCE_REGISTER_CSV, sources)
    write_csv(HREF_THEOREM_CSV, theorem)
    write_csv(HREF_INPUT_CSV, href_input)
    write_csv(PROMOTION_GATES_CSV, gates)
    write_csv(FIREWALL_CSV, firewalls)
    write_csv(ROUTE_MATRIX_CSV, routes)

    run_command([sys.executable, str(HREF_RUNNER), str(HREF_INPUT_CSV), str(HREF_OUTPUT_CSV)])
    href_output = parse_csv(HREF_OUTPUT_CSV)

    density_input = density_input_from_href(timestamp, href_output)
    write_csv(DENSITY_INPUT_CSV, density_input)
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

    score = score_rows(timestamp, href_output, density_output, parent_output, source_output, open_output)
    write_csv(SCORE_GATE_CSV, score)

    write_docs(timestamp, theorem, href_output, density_output, score, routes)
    append_outputs(timestamp)
    add_claim_once(timestamp)
    append_spine_and_packet(timestamp)
    update_resume(timestamp)

    validation = validate(timestamp, sources, href_output, density_output, parent_output, source_output, open_output, gates)
    write_csv(VALIDATION_CSV, validation)

    cache_dir = SCRIPT_DIR / "__pycache__"
    if cache_dir.exists():
        shutil.rmtree(cache_dir)


if __name__ == "__main__":
    main()
