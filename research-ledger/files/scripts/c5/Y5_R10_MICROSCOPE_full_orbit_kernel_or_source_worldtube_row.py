from __future__ import annotations

import csv
import shutil
import urllib.request
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
DOC = ROOT / "1071-Y5-R10-MICROSCOPE-full-orbit-kernel-or-source-worldtube-row.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_DIR = ROOT / "runs" / "1071-MICROSCOPE-full-orbit-kernel-or-source-worldtube" / "results"
PRODUCT_RUN_DIR = RUN_DIR / "product_runner"
PREDICTION_TEMPLATE = OUT / "P8_Y5_R10_1071_WEP_PRODUCT_CANDIDATE_NONCLAIM.csv"
BOUND_IMPORT = OUT / "P8_Y5_R10_1071_WEP_BOUND_IMPORT.csv"


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


def probe_url(url: str, timeout: int = 8) -> dict[str, str]:
    try:
        request = urllib.request.Request(url, headers={"User-Agent": "MTS-private-audit/1071"})
        with urllib.request.urlopen(request, timeout=timeout) as response:
            payload = response.read(512)
            status = getattr(response, "status", 200)
        return {
            "url": url,
            "probe_status": "HTTP_OK",
            "http_status": str(status),
            "bytes_sampled": str(len(payload)),
            "error": "",
            "generated_utc": stamp(),
            "valid_for_claim": "false",
        }
    except Exception as exc:
        return {
            "url": url,
            "probe_status": "BLOCKED_OR_UNREACHABLE_FROM_THIS_RUN",
            "http_status": "",
            "bytes_sampled": "0",
            "error": type(exc).__name__ + ": " + str(exc),
            "generated_utc": stamp(),
            "valid_for_claim": "false",
        }


def source_register_rows() -> list[dict[str, str]]:
    specs = [
        ("SRC1071_0_1070_next", "source-intake/mts_residuals/P8_Y5_R10_1070_NEXT_TARGET.csv", "1071-Y5-R10-MICROSCOPE-full-orbit-kernel-or-source-worldtube-row.md", "1070 handoff."),
        ("SRC1071_1_1070_validation", "source-intake/mts_residuals/P8_Y5_BRR545_1070_VALIDATION.csv", "V1070_SUMMARY", "1070 validation summary."),
        ("SRC1071_2_1070_eta", "source-intake/mts_residuals/P8_Y5_R10_1070_ETA_READOUT_FORMULA_ROWS.csv", "ETA1070_0_formula", "eta formula acquired."),
        ("SRC1071_3_1070_orbit", "source-intake/mts_residuals/P8_Y5_R10_1070_ORBIT_KERNEL_SOURCE_ROWS.csv", "ORK1070_5_verdict", "orbit metadata partial."),
        ("SRC1071_4_1070_fill", "source-intake/mts_residuals/P8_Y5_R10_1070_READOUT_FILL_MATRIX_UPDATE.csv", "RFM1070_5_full_orbit_kernel", "full orbit kernel still missing."),
        ("SRC1071_5_1070_tau", "source-intake/mts_residuals/P8_Y5_R10_1070_TAU_IMPACT_LEDGER.csv", "TAI1070_4_verdict", "tau still missing."),
        ("SRC1071_6_1070_product", "source-intake/mts_residuals/P8_Y5_R10_1070_WEP_PRODUCT_CANDIDATE_NONCLAIM.csv", "PRED1070_0", "product runner remains blocked."),
        ("SRC1071_7_1068_worldtube", "source-intake/mts_residuals/P8_Y5_R10_1068_SOURCE_WORLDTUBE_REQUIREMENTS.csv", "SWT1068_5_verdict", "source worldtube missing."),
        ("SRC1071_8_1061_material", "source-intake/mts_residuals/P8_Y5_R10_1061_WEP_MATERIAL_CONVENTION.csv", "MCON1061_0_test_pair", "material pair context only."),
        ("SRC1071_9_local_bounds", "source-intake/local_bounds/local_bound_claims.csv", "R1_WEP_source_charge", "source-backed WEP bound row."),
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


def external_kernel_source_rows() -> list[dict[str, str]]:
    cqg_pdf = "https://elib.dlr.de/193667/2/Touboul_2022_Class._Quantum_Grav._39_204009.pdf"
    ready_pdf = "https://microscope3.sciencesconf.org/conference/microscope3/pages/2012_Touboul_CQG_The_MICROSCOPE_experiment_ready_for_the_in_orbit_test_of_the_equivalence_principle_.pdf"
    return [
        {
            "external_id": "EXT1071_0_data_products",
            "source_url": cqg_pdf,
            "doi": "10.1088/1361-6382/ac84be",
            "source_lines": "CQG 2022 PDF lines 308-351",
            "kernel_item": "session data include 4 Hz accelerations, same-stamp attitude/angular velocity/angular acceleration in J2000, and minute-sampled satellite position/velocity",
            "kernel_status": "SOURCE_BACKED_DATA_PRODUCT_REQUIREMENTS",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "external_id": "EXT1071_1_measurement_model_eq3",
            "source_url": cqg_pdf,
            "doi": "10.1088/1361-6382/ac84be",
            "source_lines": "CQG 2022 PDF lines 399-412",
            "kernel_item": "differential measured acceleration equals bias plus mapped applied differential acceleration plus common-mode/angular-coupling/noise terms",
            "kernel_status": "SOURCE_BACKED_MEASUREMENT_MODEL",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "external_id": "EXT1071_2_applied_acceleration_eq4",
            "source_url": cqg_pdf,
            "doi": "10.1088/1361-6382/ac84be",
            "source_lines": "CQG 2022 PDF lines 428-445",
            "kernel_item": "applied differential acceleration has WEP source leg delta*g(Osat), gravity-gradient/inertia offcentring leg ([T]-[In])*Delta, and physical bias",
            "kernel_status": "SOURCE_BACKED_SOURCE_WORLDTUBE_PROXY_FORM",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "external_id": "EXT1071_3_fundamental_eq6",
            "source_url": cqg_pdf,
            "doi": "10.1088/1361-6382/ac84be",
            "source_lines": "CQG 2022 PDF lines 491-523",
            "kernel_item": "corrected X-axis regression uses bias, delta_x*g_x, delta_z*g_z, Delta_x*Sxx, Delta_z*Sxz, and noise; g/S functions are computed from position, pointing, angular velocity and acceleration",
            "kernel_status": "SOURCE_BACKED_REGRESSION_KERNEL_SKELETON",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "external_id": "EXT1071_4_polynomial_eq7",
            "source_url": cqg_pdf,
            "doi": "10.1088/1361-6382/ac84be",
            "source_lines": "CQG 2022 PDF lines 533-543",
            "kernel_item": "bias trend is a degree-three polynomial; final fit basis is polynomial trend plus gx,gz,Sxx,Sxz",
            "kernel_status": "SOURCE_BACKED_FIT_BASIS",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "external_id": "EXT1071_5_frequency_table",
            "source_url": cqg_pdf,
            "doi": "10.1088/1361-6382/ac84be",
            "source_lines": "CQG 2022 PDF lines 210-220",
            "kernel_item": "forb=0.16818e-3 Hz; fspin2=0.75681e-3 Hz; fspin3=2.94315e-3 Hz; fEP2=0.92499e-3 Hz; fEP3=3.11133e-3 Hz",
            "kernel_status": "SOURCE_BACKED_FREQUENCY_KERNEL",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "external_id": "EXT1071_6_segmentation_dft",
            "source_url": cqg_pdf,
            "doi": "10.1088/1361-6382/ac84be",
            "source_lines": "CQG 2022 PDF lines 584-600",
            "kernel_item": "selected segments are even numbers of orbits so combinations of orbital and spin frequencies land on DFT bins with low theoretical correlation",
            "kernel_status": "SOURCE_BACKED_SEGMENT_WINDOW_RULE",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "external_id": "EXT1071_7_suep_segment_table",
            "source_url": cqg_pdf,
            "doi": "10.1088/1361-6382/ac84be",
            "source_lines": "CQG 2022 PDF lines 607-628",
            "kernel_item": "SUEP selected segment durations and glitch percentages are tabulated for 19 segments totalling 1362 orbits",
            "kernel_status": "SOURCE_BACKED_SUEP_SEGMENT_LEDGER",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "external_id": "EXT1071_8_position_pointing_requirements",
            "source_url": ready_pdf,
            "doi": "10.1088/0264-9381/29/18/184010",
            "source_lines": "CQG 2012 PDF lines 209-227",
            "kernel_item": "kernel construction requires measurement dating, satellite position, instrument pointing, and fEP=forb+fspin in spin mode",
            "kernel_status": "SOURCE_BACKED_POSITION_POINTING_REQUIREMENTS",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "external_id": "EXT1071_9_onera_data_availability_page",
            "source_url": "https://microscope.onera.fr/fr/publication/microscope-data-are-available",
            "doi": "",
            "source_lines": "ONERA public page",
            "kernel_item": "ONERA states MICROSCOPE mission data are available at https://cmsm-ds.onera.fr/user/microscope",
            "kernel_status": "SOURCE_BACKED_DATA_PORTAL_POINTER",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def portal_probe_rows() -> list[dict[str, str]]:
    return [
        probe_url("https://microscope.onera.fr/fr/publication/microscope-data-are-available"),
        probe_url("https://cmsm-ds.onera.fr/user/microscope"),
    ]


def kernel_component_rows() -> list[dict[str, str]]:
    return [
        {
            "kernel_id": "KER1071_0_data_vector",
            "component": "observed vector",
            "official_form": "y(t)=Gamma_x,corr^(d)(t) after calibration/correction",
            "source_id": "EXT1071_0_data_products; EXT1071_3_fundamental_eq6",
            "needed_numeric_inputs": "4Hz corrected differential acceleration per selected segment",
            "acquired_level": "FORM_AND_DATA_PRODUCT_REQUIREMENT_ONLY",
            "blocks_tau": "true",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "kernel_id": "KER1071_1_fit_basis",
            "component": "regression design basis",
            "official_form": "columns=[1,(t-t0),(t-t0)^2,(t-t0)^3,gx(t),gz(t),Sxx(t),Sxz(t)]",
            "source_id": "EXT1071_3_fundamental_eq6; EXT1071_4_polynomial_eq7",
            "needed_numeric_inputs": "time stamps; gx; gz; Sxx; Sxz in instrument frame",
            "acquired_level": "OFFICIAL_KERNEL_SKELETON_ACQUIRED",
            "blocks_tau": "true",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "kernel_id": "KER1071_2_source_gravity_leg",
            "component": "Earth/source gravity proxy",
            "official_form": "g(Osat) and gravity-gradient tensor T computed at satellite centre",
            "source_id": "EXT1071_2_applied_acceleration_eq4; EXT1071_3_fundamental_eq6",
            "needed_numeric_inputs": "satellite position/velocity and gravity model used by MICROSCOPE processing",
            "acquired_level": "SOURCE_WORLDTUBE_PROXY_FORM_ACQUIRED_NOT_NUMERIC",
            "blocks_tau": "true",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "kernel_id": "KER1071_3_inertial_leg",
            "component": "inertia-gradient subtraction",
            "official_form": "S is the symmetric part of T-In, with In=Omega^2+Omega_dot",
            "source_id": "EXT1071_2_applied_acceleration_eq4; EXT1071_3_fundamental_eq6",
            "needed_numeric_inputs": "attitude, angular velocity, angular acceleration at accelerometer time stamps",
            "acquired_level": "FORM_ACQUIRED_NOT_NUMERIC",
            "blocks_tau": "true",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "kernel_id": "KER1071_4_segment_window",
            "component": "segment/window operator",
            "official_form": "selected continuous segments; even-orbit DFT-aligned windows; glitch masks",
            "source_id": "EXT1071_6_segmentation_dft; EXT1071_7_suep_segment_table",
            "needed_numeric_inputs": "segment masks, removed-sample indices, exact timestamps",
            "acquired_level": "SOURCE_BACKED_SEGMENT_TABLE_ACQUIRED",
            "blocks_tau": "true",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "kernel_id": "KER1071_5_frequency_projection",
            "component": "frequency separation",
            "official_form": "gx,gz at fEP in phase quadrature; Sxx,Sxz mainly DC and 2fEP",
            "source_id": "EXT1071_3_fundamental_eq6; EXT1071_5_frequency_table",
            "needed_numeric_inputs": "mode-specific fEP, phase convention, segment timestamps",
            "acquired_level": "FREQUENCY_KERNEL_FORM_ACQUIRED",
            "blocks_tau": "true",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "kernel_id": "KER1071_6_verdict",
            "component": "tau_WEP kernel verdict",
            "official_form": "official kernel skeleton acquired, but no numeric orbit/attitude/source-worldtube kernel has been downloaded or reconstructed",
            "source_id": "KER1071_0_data_vector; KER1071_1_fit_basis; KER1071_2_source_gravity_leg; KER1071_4_segment_window",
            "needed_numeric_inputs": "data portal products or reproduced gx/gz/Sxx/Sxz arrays",
            "acquired_level": "KERNEL_SKELETON_YES_NUMERIC_TAU_NO",
            "blocks_tau": "true",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def suep_segment_rows() -> list[dict[str, object]]:
    rows = [
        ("210", "50", "1", "50", "18"),
        ("212", "60", "1", "60", "17"),
        ("218", "120", "1", "120", "15"),
        ("234", "92", "1", "92", "18"),
        ("236", "120", "1", "120", "21"),
        ("238", "120", "1", "120", "24"),
        ("252", "106", "1", "106", "26"),
        ("254", "120", "1", "120", "27"),
        ("256", "120", "1", "120", "28"),
        ("326-1", "66", "2", "67", "12"),
        ("326-2", "34", "69", "102", "7"),
        ("358", "92", "1", "92", "14"),
        ("402", "18", "3", "20", "35"),
        ("404", "120", "1", "120", "23"),
        ("406", "20", "1", "20", "23"),
        ("438", "32", "1", "32", "21"),
        ("442", "40", "1", "40", "21"),
        ("748", "24", "1", "24", "25"),
        ("750", "8", "1", "8", "19"),
    ]
    return [
        {
            "segment_id": f"SUEP1071_{segment}",
            "segment_number": segment,
            "duration_orbits": duration,
            "position_begin_orbit": begin,
            "position_end_orbit": end,
            "glitch_eliminated_percent": glitch,
            "source_id": "EXT1071_7_suep_segment_table",
            "role_in_kernel": "segment/window metadata only",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for segment, duration, begin, end, glitch in rows
    ]


def tau_projection_status_rows() -> list[dict[str, str]]:
    return [
        {
            "tau_status_id": "TAU1071_0_projection_form",
            "object": "tau_WEP readout projection form",
            "status": "PARTIAL_FORM_ACQUIRED",
            "evidence": "KER1071_1_fit_basis",
            "remaining_gap": "numeric gx/gz/Sxx/Sxz arrays and exact segment masks",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "tau_status_id": "TAU1071_1_source_worldtube_proxy",
            "object": "source leg",
            "status": "OFFICIAL_PROXY_FORM_ACQUIRED",
            "evidence": "KER1071_2_source_gravity_leg",
            "remaining_gap": "Earth gravity model/source profile not reconstructed inside MTS tau branch",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "tau_status_id": "TAU1071_2_data_portal",
            "object": "official data access",
            "status": "PUBLIC_POINTER_ACQUIRED_DIRECT_ACCESS_UNVERIFIED_OR_BLOCKED",
            "evidence": "EXT1071_9_onera_data_availability_page; P8_Y5_R10_1071_DATA_PORTAL_PROBE.csv",
            "remaining_gap": "machine-readable product schema and downloaded kernel arrays",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "tau_status_id": "TAU1071_3_verdict",
            "object": "tau_WEP numeric projection",
            "status": "NOT_ACQUIRED",
            "evidence": "KER1071_6_verdict",
            "remaining_gap": "full numeric orbit/attitude/averaging kernel or direct parent product",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def product_prediction_rows() -> list[dict[str, str]]:
    return [
        {
            "prediction_id": "PRED1071_0_WEP_kernel_skeleton_nonclaim_product",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "P_WEP_relative_source_weight",
            "product_value": "MISSING_NUMERIC_TAU_WEP_KERNEL_OR_DIRECT_PARENT_PRODUCT",
            "product_units": "dimensionless",
            "product_source": "source-intake/mts_residuals/P8_Y5_R10_1071_OFFICIAL_KERNEL_COMPONENTS.csv",
            "inputs_present": "eta_formula;official_fit_basis;frequency_table;SUEP_segment_table;source_gravity_proxy_form",
            "required_inputs": "numeric gx/gz/Sxx/Sxz arrays; exact masks/timestamps; material tensor; Xhat normalization; direct parent product or tau_WEP map",
            "derivation_status": "KERNEL_SKELETON_YES_NUMERIC_PRODUCT_NO",
            "valid_for_claim": "false",
            "notes": "source-backed kernel skeleton is useful but cannot be scored as an MTS prediction",
        }
    ]


def bound_rows() -> list[dict[str, str]]:
    row = local_bound_row("R1_WEP_source_charge")
    url, doi = split_reference(row["reference_path_or_url"])
    return [
        {
            "bound_id": "BOUND1071_0_MICROSCOPE_R1_eta_source_charge",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "P_WEP_relative_source_weight",
            "bound_value": row["upper_bound"],
            "bound_units": row["units"],
            "bound_source": url,
            "source_row": f"source-intake/local_bounds/local_bound_claims.csv::{row['row_id']}; doi:{doi}",
            "bound_type": "source_backed_upper_bound_anchor",
            "valid_for_claim": "true",
            "notes": "valid bound anchor only; no scoreable MTS kernel product yet",
        }
    ]


def product_status_rows(status: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "runner_id": "APR1071_0_WEP_kernel_skeleton_product_stub",
            "prediction_rows": str(status.get("prediction_rows", "")),
            "bound_rows": str(status.get("bound_rows", "")),
            "valid_prediction_rows": str(status.get("valid_prediction_rows", "")),
            "valid_bound_rows": str(status.get("valid_bound_rows", "")),
            "comparison_rows": str(status.get("comparison_rows", "")),
            "passed_rows": str(status.get("passed_rows", "")),
            "claim_allowed": str(status.get("claim_allowed", "")).lower(),
            "expected_result": "reject skeleton-only prediction and keep claim false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def claim_gate_rows(product_status: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "gate_id": "CG1071_0_official_kernel_skeleton",
            "claim_component": "official MICROSCOPE fit kernel skeleton",
            "gate_pass": "true",
            "claim_allowed": "false",
            "reason": "form acquired, numeric arrays absent",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1071_1_suep_segment_table",
            "claim_component": "19 SUEP segment windows",
            "gate_pass": "true",
            "claim_allowed": "false",
            "reason": "segment metadata acquired but exact masks/timestamps absent",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1071_2_source_worldtube",
            "claim_component": "source worldtube/numeric gravity leg",
            "gate_pass": "false",
            "claim_allowed": "false",
            "reason": "only g(Osat)/T proxy form acquired",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1071_3_tau_WEP_numeric",
            "claim_component": "numeric tau_WEP or direct parent product",
            "gate_pass": "false",
            "claim_allowed": "false",
            "reason": "MISSING_NUMERIC_TAU_WEP_KERNEL_OR_DIRECT_PARENT_PRODUCT",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1071_4_product_runner",
            "claim_component": "WEP product runner",
            "gate_pass": "false",
            "claim_allowed": str(product_status.get("claim_allowed", "")).lower(),
            "reason": f"valid_prediction_rows={product_status.get('valid_prediction_rows')}",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1071_5_local_GR_WEP_claim",
            "claim_component": "local-GR/WEP pass",
            "gate_pass": "false",
            "claim_allowed": "false",
            "reason": "kernel shape acquired but no MTS product score",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC1071_0_kernel_skeleton_acquired",
            "decision": "the official MICROSCOPE WEP readout kernel skeleton is acquired",
            "evidence": "KER1071_1_fit_basis; EXT1071_3_fundamental_eq6; EXT1071_4_polynomial_eq7",
            "consequence": "the next branch can target numeric arrays, not just equations",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1071_1_segment_table_acquired",
            "decision": "the 19 SUEP selected segments are staged as a source-backed table",
            "evidence": "P8_Y5_R10_1071_SUEP_SEGMENT_TABLE_SOURCE_BACKED.csv",
            "consequence": "future reproducibility work has a first window ledger",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1071_2_no_claim",
            "decision": "do not claim WEP/local-GR pass",
            "evidence": "TAU1071_3_verdict; APR1071_0_WEP_kernel_skeleton_product_stub",
            "consequence": "numeric tau_WEP remains the next barrier",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_id": "NEXT1071_0_1072",
            "next_target": "1072-Y5-R10-MICROSCOPE-data-portal-schema-or-reconstructed-gxS-kernel.md",
            "objective": "turn the official 1071 kernel skeleton into a numeric tau_WEP component by either acquiring the CMSM data schema/products or reconstructing gx,gz,Sxx,Sxz from sourced orbit/attitude/gravity-model inputs for at least one SUEP segment.",
            "include": "CMSM portal access notes; file/schema inventory; exact timestamps/masks; gx/gz/Sxx/Sxz arrays or dry-run reconstruction; segment 210 or another single SUEP pilot; refusal gates",
            "exclude": "public WEP/local-GR claim; tau=1; guessed phase; guessed masks; measured-G absorption; GitHub; formalization edits",
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
    external_rows: list[dict[str, str]],
    portal_rows: list[dict[str, str]],
    kernel_rows: list[dict[str, str]],
    segment_rows: list[dict[str, object]],
    tau_rows: list[dict[str, str]],
    prediction_rows: list[dict[str, str]],
    bound_rows_: list[dict[str, str]],
    product_status: dict[str, Any],
    claim_rows: list[dict[str, str]],
    next_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    segment_total = sum(int(str(row["duration_orbits"])) for row in segment_rows)
    external_ids = {row["external_id"] for row in external_rows}
    checks: list[tuple[str, bool, str]] = []
    checks.append(("V1071_0_sources_exist", all(row["exists"] == "true" and row["needle_found"] == "true" for row in source_rows), "all cited local source paths and needles are present"))
    checks.append(("V1071_1_external_kernel_sources", {"EXT1071_1_measurement_model_eq3", "EXT1071_2_applied_acceleration_eq4", "EXT1071_3_fundamental_eq6", "EXT1071_4_polynomial_eq7"}.issubset(external_ids), "official model equations recorded"))
    checks.append(("V1071_2_data_products_recorded", any(row["external_id"] == "EXT1071_0_data_products" and "position/velocity" in row["kernel_item"] for row in external_rows), "data product requirements recorded"))
    checks.append(("V1071_3_portal_probe_recorded", len(portal_rows) == 2 and all(row["probe_status"] for row in portal_rows), "ONERA/CMSM portal probes recorded whether reachable or blocked"))
    checks.append(("V1071_4_kernel_skeleton_acquired", any(row["kernel_id"] == "KER1071_6_verdict" and row["acquired_level"] == "KERNEL_SKELETON_YES_NUMERIC_TAU_NO" for row in kernel_rows), "kernel skeleton acquired but numeric tau not acquired"))
    checks.append(("V1071_5_suep_segments", len(segment_rows) == 19 and segment_total == 1362, "19 SUEP segments total 1362 orbits"))
    checks.append(("V1071_6_tau_not_acquired", any(row["tau_status_id"] == "TAU1071_3_verdict" and row["status"] == "NOT_ACQUIRED" for row in tau_rows), "tau_WEP numeric verdict remains blocked"))
    checks.append(("V1071_7_prediction_nonclaim_missing", any("MISSING_NUMERIC_TAU_WEP_KERNEL" in row["product_value"] and row["valid_for_claim"] == "false" for row in prediction_rows), "prediction row remains nonclaim and missing numeric kernel"))
    checks.append(("V1071_8_bound_numeric", bool(bound_rows_) and float(bound_rows_[0]["bound_value"]) > 0 and bound_rows_[0]["valid_for_claim"] == "true", "bound import is positive numeric"))
    checks.append(("V1071_9_runner_refuses", product_status.get("valid_prediction_rows") == 0 and product_status.get("claim_allowed") is False, "runner reports no valid prediction rows and claim false"))
    checks.append(("V1071_10_claim_gates_safe", all(row["claim_allowed"] == "false" for row in claim_rows), "all claim gates deny WEP/local-GR claim"))
    checks.append(("V1071_11_next_target", any("1072-Y5-R10-MICROSCOPE-data-portal-schema-or-reconstructed-gxS-kernel.md" in row["next_target"] for row in next_rows), "1072 handoff written"))
    generated_paths = list(outputs.values()) + [DOC]
    checks.append(("V1071_12_generated_under_post_checkpoint", all(str(path.resolve()).startswith(str(ROOT.resolve())) for path in generated_paths), "all generated outputs are under post-checkpoint-work"))
    checks.append(("V1071_13_csv_parse", all(path.exists() and csv_rows_parse(path) for path in outputs.values() if path.suffix == ".csv" and path.name != "P8_Y5_BRR545_1071_VALIDATION.csv"), "all 1071 CSV outputs parse cleanly"))
    checks.append(("V1071_14_formalization_untouched", count_formalization_modified_since_start() == 0, "formalization-workbench modified-file count remains zero"))
    checks.append(("V1071_SUMMARY", True, "official kernel skeleton and SUEP segment table acquired; numeric tau/product claim blocked"))
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
    external_rows: list[dict[str, str]],
    portal_rows: list[dict[str, str]],
    kernel_rows: list[dict[str, str]],
    segment_rows: list[dict[str, object]],
    tau_rows: list[dict[str, str]],
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
            "# 1071 - MICROSCOPE full orbit kernel or source-worldtube row",
            "",
            "## Current verdict",
            "1071 acquires the official MICROSCOPE WEP readout kernel **skeleton**: data vector, fit basis, source-gravity proxy, inertia-gradient subtraction, segment/window rule, and frequency projection. It still does **not** acquire a numeric tau_WEP kernel or direct MTS product, so WEP/local-GR claims remain blocked.",
            "",
            "## Local source register",
            md_table(source_rows, ["source_id", "relative_path", "exists", "needle_found", "note"]),
            "## External kernel source ledger",
            md_table(external_rows, ["external_id", "source_lines", "kernel_status", "kernel_item", "valid_for_claim"]),
            "## Data portal probe",
            md_table(portal_rows, ["url", "probe_status", "http_status", "bytes_sampled", "error"]),
            "## Official kernel components",
            md_table(kernel_rows, ["kernel_id", "component", "official_form", "acquired_level", "needed_numeric_inputs", "valid_for_claim"]),
            "## SUEP segment table",
            md_table(segment_rows, ["segment_id", "duration_orbits", "position_begin_orbit", "position_end_orbit", "glitch_eliminated_percent", "source_id"]),
            "## Tau projection status",
            md_table(tau_rows, ["tau_status_id", "object", "status", "remaining_gap", "claim_allowed"]),
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
    external_rows = external_kernel_source_rows()
    portal_rows = portal_probe_rows()
    kernel_rows = kernel_component_rows()
    segment_rows = suep_segment_rows()
    tau_rows = tau_projection_status_rows()
    prediction_rows = product_prediction_rows()
    bound_rows_ = bound_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    outputs = {
        "source_register": OUT / "P8_Y5_R10_1071_SOURCE_REGISTER.csv",
        "external_ledger": OUT / "P8_Y5_R10_1071_EXTERNAL_KERNEL_SOURCE_LEDGER.csv",
        "portal_probe": OUT / "P8_Y5_R10_1071_DATA_PORTAL_PROBE.csv",
        "kernel_components": OUT / "P8_Y5_R10_1071_OFFICIAL_KERNEL_COMPONENTS.csv",
        "suep_segments": OUT / "P8_Y5_R10_1071_SUEP_SEGMENT_TABLE_SOURCE_BACKED.csv",
        "tau_status": OUT / "P8_Y5_R10_1071_TAU_PROJECTION_STATUS.csv",
        "prediction": PREDICTION_TEMPLATE,
        "bound": BOUND_IMPORT,
        "product_status": OUT / "P8_Y5_R10_1071_PRODUCT_RUNNER_STATUS.csv",
        "product_comparison": OUT / "P8_Y5_R10_1071_PRODUCT_COMPARISON_ROWS.csv",
        "claim_gates": OUT / "P8_Y5_R10_1071_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_R10_1071_DECISION_LEDGER.csv",
        "next_target": OUT / "P8_Y5_R10_1071_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_1071_VALIDATION.csv",
    }

    write_csv(outputs["source_register"], source_rows)
    write_csv(outputs["external_ledger"], external_rows)
    write_csv(outputs["portal_probe"], portal_rows)
    write_csv(outputs["kernel_components"], kernel_rows)
    write_csv(outputs["suep_segments"], segment_rows)
    write_csv(outputs["tau_status"], tau_rows)
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
        external_rows,
        portal_rows,
        kernel_rows,
        segment_rows,
        tau_rows,
        prediction_rows,
        bound_rows_,
        product_status,
        claim_rows,
        next_rows,
    )
    write_csv(outputs["validation"], validation_rows)
    write_doc(
        source_rows,
        external_rows,
        portal_rows,
        kernel_rows,
        segment_rows,
        tau_rows,
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
