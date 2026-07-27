from __future__ import annotations

import csv
import shutil
import urllib.error
import urllib.request
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
DOC = WORK / "2778-Y5-R2FR-MICROSCOPE-full-orbit-kernel-or-source-worldtube-row-under-AX1090.md"

OUTPUTS = {
    "sources": MTS / "P8_Y5_R2FR_2778_SOURCE_REGISTER.csv",
    "external": MTS / "P8_Y5_R2FR_2778_EXTERNAL_KERNEL_SOURCE_LEDGER.csv",
    "portal": MTS / "P8_Y5_R2FR_2778_DATA_PORTAL_PROBE.csv",
    "kernel": MTS / "P8_Y5_R2FR_2778_OFFICIAL_KERNEL_COMPONENTS.csv",
    "segments": MTS / "P8_Y5_R2FR_2778_SUEP_SEGMENT_TABLE_SOURCE_BACKED.csv",
    "tau": MTS / "P8_Y5_R2FR_2778_TAU_PROJECTION_STATUS.csv",
    "candidate": MTS / "P8_Y5_R2FR_2778_WEP_PRODUCT_CANDIDATE_NONCLAIM.csv",
    "bounds": MTS / "P8_Y5_R2FR_2778_WEP_BOUND_IMPORT.csv",
    "runner": MTS / "P8_Y5_R2FR_2778_PRODUCT_RUNNER_STATUS.csv",
    "comparisons": MTS / "P8_Y5_R2FR_2778_PRODUCT_COMPARISON_ROWS.csv",
    "gates": MTS / "P8_Y5_R2FR_2778_CLAIM_GATES.csv",
    "decision": MTS / "P8_Y5_R2FR_2778_DECISION_LEDGER.csv",
    "next": MTS / "P8_Y5_R2FR_2778_NEXT_TARGET.csv",
    "branches": MTS / "P8_Y5_R2FR_2778_BRANCH_COPIES.csv",
    "validation": MTS / "P8_Y5_BRR545_2778_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "kernel_queue": RAB_QUEUE / "JR2778_MICROSCOPE_KERNEL_SKELETON_NONCLAIM.csv",
    "segment_queue": RAB_QUEUE / "JR2778_SUEP_SEGMENT_TABLE_NONCLAIM.csv",
    "beta_doc": BETA_DOCS / "MICROSCOPE_KERNEL_SKELETON_2778_NONCLAIM.csv",
    "microscope_copy": MICROSCOPE_DIR / "microscope_kernel_skeleton_2778_nonclaim.csv",
    "next_queue": RAB_QUEUE / "JR2778_DATA_PORTAL_OR_GXS_NEXT.csv",
}


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


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(WORK))
    except ValueError:
        return str(path)


def nonclaim(row: dict[str, Any]) -> dict[str, Any]:
    row["valid_for_claim"] = False
    return row


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def csv_row_count(path: Path) -> int:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return sum(1 for _ in csv.DictReader(handle))


def csv_parses(path: Path) -> bool:
    if not path.exists():
        return False
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


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


def has_missing_marker(row: dict[str, Any]) -> bool:
    return "MISSING" in " ".join(str(value) for value in row.values())


def get_local_bound(row_id: str) -> dict[str, str]:
    for row in read_csv_rows(LOCAL_BOUNDS / "local_bound_claims.csv"):
        if row.get("row_id") == row_id:
            return row
    return {}


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


def build_sources() -> list[dict[str, Any]]:
    specs = [
        ("SRC2778_00_2777_next", "2777_next", MTS / "P8_Y5_R2FR_2777_NEXT_TARGET.csv", "NEXT2777_0_2778", "current handoff into full orbit kernel/source-worldtube acquisition"),
        ("SRC2778_01_2777_validation", "2777_validation", MTS / "P8_Y5_BRR545_2777_VALIDATION.csv", "VAL2777_OVERALL", "current validation baseline"),
        ("SRC2778_02_2777_readout", "2777_readout", MTS / "P8_Y5_R2FR_2777_READOUT_FILL_MATRIX_UPDATE.csv", "RFM2777_5_full_orbit_kernel", "current full-kernel blocker"),
        ("SRC2778_03_2777_orbit", "2777_orbit", MTS / "P8_Y5_R2FR_2777_ORBIT_KERNEL_SOURCE_ROWS.csv", "ORK2777_5_verdict", "current partial orbit/readout metadata"),
        ("SRC2778_04_2777_product", "2777_product", MTS / "P8_Y5_R2FR_2777_WEP_PRODUCT_CANDIDATE_NONCLAIM.csv", "MISSING_DIRECT_PRODUCT_OR_TAU_WEP_KERNEL", "current nonclaim WEP product placeholder"),
        ("SRC2778_05_1071_doc", "1071_doc", WORK / "1071-Y5-R10-MICROSCOPE-full-orbit-kernel-or-source-worldtube-row.md", "Official kernel components", "R10 precedent for official MICROSCOPE kernel skeleton"),
        ("SRC2778_06_1071_external", "1071_external", MTS / "P8_Y5_R10_1071_EXTERNAL_KERNEL_SOURCE_LEDGER.csv", "EXT1071_3_fundamental_eq6", "source-backed external kernel source ledger"),
        ("SRC2778_07_1071_kernel", "1071_kernel", MTS / "P8_Y5_R10_1071_OFFICIAL_KERNEL_COMPONENTS.csv", "KER1071_6_verdict", "prior official kernel component table"),
        ("SRC2778_08_1071_segments", "1071_segments", MTS / "P8_Y5_R10_1071_SUEP_SEGMENT_TABLE_SOURCE_BACKED.csv", "SUEP1071_750", "prior source-backed SUEP segment table"),
        ("SRC2778_09_1071_tau", "1071_tau", MTS / "P8_Y5_R10_1071_TAU_PROJECTION_STATUS.csv", "TAU1071_3_verdict", "prior tau projection blocker"),
        ("SRC2778_10_1071_portal", "1071_portal", MTS / "P8_Y5_R10_1071_DATA_PORTAL_PROBE.csv", "cmsm-ds.onera.fr", "prior data portal probe"),
        ("SRC2778_11_local_bounds", "local_bounds", LOCAL_BOUNDS / "local_bound_claims.csv", "R1_WEP_source_charge", "local MICROSCOPE WEP bound source row"),
    ]
    return [source_row(*spec) for spec in specs]


def remap_id(value: str) -> str:
    return value.replace("1071", "2778")


def build_external_rows() -> list[dict[str, Any]]:
    source_rows = read_csv_rows(MTS / "P8_Y5_R10_1071_EXTERNAL_KERNEL_SOURCE_LEDGER.csv")
    rows: list[dict[str, Any]] = []
    for source in source_rows:
        rows.append(nonclaim({
            "external_id": remap_id(source.get("external_id", "")),
            "source_url": source.get("source_url", ""),
            "doi": source.get("doi", ""),
            "source_lines": source.get("source_lines", ""),
            "kernel_item": source.get("kernel_item", ""),
            "kernel_status": source.get("kernel_status", ""),
            "port_status": "PORTED_FROM_R10_1071_INTO_R2FR_NONCLAIM_BRANCH",
            "generated_utc": ts(),
        }))
    return rows


def probe_url(url: str) -> dict[str, Any]:
    started = ts()
    request = urllib.request.Request(url, headers={"User-Agent": "MTS-private-checkpoint/2778"})
    try:
        with urllib.request.urlopen(request, timeout=8) as response:
            sample = response.read(512)
            return nonclaim({
                "url": url,
                "probe_started_utc": started,
                "probe_status": "HTTP_OK",
                "http_status": getattr(response, "status", ""),
                "bytes_sampled": len(sample),
                "error": "",
            })
    except Exception as exc:
        status = "BLOCKED_OR_UNREACHABLE_FROM_THIS_RUN"
        if isinstance(exc, urllib.error.HTTPError):
            status = "HTTP_ERROR"
        return nonclaim({
            "url": url,
            "probe_started_utc": started,
            "probe_status": status,
            "http_status": getattr(exc, "code", ""),
            "bytes_sampled": 0,
            "error": f"{type(exc).__name__}: {exc}",
        })


def build_portal_rows() -> list[dict[str, Any]]:
    return [
        probe_url("https://microscope.onera.fr/fr/publication/microscope-data-are-available"),
        probe_url("https://cmsm-ds.onera.fr/user/microscope"),
    ]


def build_kernel_rows() -> list[dict[str, Any]]:
    source_rows = read_csv_rows(MTS / "P8_Y5_R10_1071_OFFICIAL_KERNEL_COMPONENTS.csv")
    rows: list[dict[str, Any]] = []
    for source in source_rows:
        rows.append(nonclaim({
            "kernel_id": remap_id(source.get("kernel_id", "")),
            "component": source.get("component", ""),
            "official_form": source.get("official_form", ""),
            "acquired_level": source.get("acquired_level", ""),
            "needed_numeric_inputs": source.get("needed_numeric_inputs", ""),
            "branch_status": "OFFICIAL_SKELETON_PORTED_NUMERIC_TAU_STILL_BLOCKED",
        }))
    if not any(row.get("kernel_id") == "KER2778_7_source_worldtube_verdict" for row in rows):
        rows.append(nonclaim({
            "kernel_id": "KER2778_7_source_worldtube_verdict",
            "component": "source-worldtube row",
            "official_form": "MICROSCOPE source leg is g(Osat) and T at satellite centre; this is a proxy form, not a downloaded or reconstructed Earth source-worldtube functional",
            "acquired_level": "SOURCE_WORLDTUBE_PROXY_FORM_ONLY",
            "needed_numeric_inputs": "Earth gravity model, satellite ephemeris, instrument pointing, timestamps, and residual-to-eta projection",
            "branch_status": "SOURCE_WORLDTUBE_NOT_NUMERICALLY_ACQUIRED",
        }))
    return rows


def build_segment_rows() -> list[dict[str, Any]]:
    source_rows = read_csv_rows(MTS / "P8_Y5_R10_1071_SUEP_SEGMENT_TABLE_SOURCE_BACKED.csv")
    rows: list[dict[str, Any]] = []
    for source in source_rows:
        rows.append(nonclaim({
            "segment_id": remap_id(source.get("segment_id", "")),
            "duration_orbits": source.get("duration_orbits", ""),
            "position_begin_orbit": source.get("position_begin_orbit", ""),
            "position_end_orbit": source.get("position_end_orbit", ""),
            "glitch_eliminated_percent": source.get("glitch_eliminated_percent", ""),
            "source_id": remap_id(source.get("source_id", "")),
            "numeric_tau_status": "WINDOW_METADATA_ONLY_NO_EXACT_MASKS_OR_TIMESTAMPS",
        }))
    return rows


def build_tau_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({"tau_status_id": "TAU2778_0_projection_form", "object": "tau_WEP readout projection form", "status": "OFFICIAL_KERNEL_SKELETON_ACQUIRED", "remaining_gap": "numeric gx/gz/Sxx/Sxz arrays, exact segment masks, timestamps, and MTS residual-to-X projection", "claim_allowed": False}),
        nonclaim({"tau_status_id": "TAU2778_1_source_worldtube_proxy", "object": "Earth/source gravity leg", "status": "OFFICIAL_PROXY_FORM_ACQUIRED_NOT_NUMERIC_SOURCE_WORLDTUBE", "remaining_gap": "Earth gravity model/source profile and ephemeris-attitude reconstruction inside MTS tau branch", "claim_allowed": False}),
        nonclaim({"tau_status_id": "TAU2778_2_data_portal", "object": "official data access", "status": "PUBLIC_POINTER_PROBED_DIRECT_SCHEMA_NOT_ACQUIRED", "remaining_gap": "machine-readable product schema and downloaded kernel arrays", "claim_allowed": False}),
        nonclaim({"tau_status_id": "TAU2778_3_verdict", "object": "tau_WEP numeric projection", "status": "NOT_ACQUIRED", "remaining_gap": "full numeric orbit/attitude/averaging kernel or direct parent product", "claim_allowed": False}),
    ]


def build_candidate_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({
            "prediction_id": "PRED2778_0_WEP_kernel_skeleton_nonclaim_product",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "P_WEP_relative_source_weight",
            "product_value": "MISSING_NUMERIC_TAU_WEP_KERNEL_OR_DIRECT_PARENT_PRODUCT",
            "product_units": "dimensionless",
            "derivation_status": "KERNEL_SKELETON_YES_NUMERIC_PRODUCT_NO",
            "notes": "official kernel skeleton is now staged in the R2/f(R) branch, but it is not a numeric MTS eta prediction",
        })
    ]


def build_bound_rows() -> list[dict[str, Any]]:
    bound = get_local_bound("R1_WEP_source_charge")
    return [
        nonclaim({
            "bound_id": "BOUND2778_0_MICROSCOPE_R1_eta_source_charge",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "P_WEP_relative_source_weight",
            "bound_value": bound.get("upper_bound", "2.8e-15"),
            "bound_units": bound.get("units", "dimensionless"),
            "bound_type": "source_backed_upper_bound_anchor",
            "source_row_id": "R1_WEP_source_charge",
            "bound_valid_for_internal_runner": True,
        })
    ]


def run_product_runner(predictions: list[dict[str, Any]], bounds: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    valid_predictions = [
        row for row in predictions
        if row.get("valid_for_claim") is True
        and is_numeric(row.get("product_value"))
        and not has_missing_marker(row)
    ]
    valid_bounds = [
        row for row in bounds
        if row.get("bound_valid_for_internal_runner") is True
        and is_numeric(row.get("bound_value"))
        and float(str(row["bound_value"])) > 0.0
        and not has_missing_marker(row)
    ]
    comparisons = [
        nonclaim({"comparison_id": "PRODUCT_COMPARE_NO_VALID_PREDICTIONS", "comparison_status": "not_run", "pass_for_claim": False, "issues": "no valid MTS tau_WEP/direct-product prediction rows"})
    ]
    runner = [
        nonclaim({
            "runner_id": "APR2778_0_WEP_kernel_skeleton_product_stub",
            "prediction_rows": len(predictions),
            "bound_rows": len(bounds),
            "valid_prediction_rows": len(valid_predictions),
            "valid_bound_rows": len(valid_bounds),
            "claim_allowed": False,
            "expected_result": "reject skeleton-only prediction and keep claim false",
        })
    ]
    return runner, comparisons


def build_gates() -> list[dict[str, Any]]:
    return [
        nonclaim({"gate_id": "CG2778_0_official_kernel_skeleton", "claim_component": "official MICROSCOPE fit kernel skeleton", "gate_pass": True, "claim_allowed": False, "reason": "form acquired; numeric arrays absent"}),
        nonclaim({"gate_id": "CG2778_1_suep_segment_table", "claim_component": "19 SUEP segment windows", "gate_pass": True, "claim_allowed": False, "reason": "segment metadata acquired but exact masks/timestamps absent"}),
        nonclaim({"gate_id": "CG2778_2_source_worldtube", "claim_component": "source worldtube/numeric gravity leg", "gate_pass": False, "claim_allowed": False, "reason": "only g(Osat)/T proxy form acquired"}),
        nonclaim({"gate_id": "CG2778_3_tau_WEP_numeric", "claim_component": "numeric tau_WEP or direct parent product", "gate_pass": False, "claim_allowed": False, "reason": "MISSING_NUMERIC_TAU_WEP_KERNEL_OR_DIRECT_PARENT_PRODUCT"}),
        nonclaim({"gate_id": "CG2778_4_product_runner", "claim_component": "WEP product runner", "gate_pass": False, "claim_allowed": False, "reason": "valid_prediction_rows=0"}),
        nonclaim({"gate_id": "CG2778_5_local_GR_WEP_claim", "claim_component": "local-GR/WEP pass", "gate_pass": False, "claim_allowed": False, "reason": "kernel skeleton acquired but no MTS product score"}),
    ]


def build_decisions() -> list[dict[str, Any]]:
    return [
        nonclaim({"decision_id": "DEC2778_0_kernel_skeleton_acquired", "decision": "port the official MICROSCOPE WEP readout kernel skeleton into the current R2/f(R) branch", "evidence": "KER2778_1_fit_basis; EXT2778_3_fundamental_eq6; EXT2778_4_polynomial_eq7", "consequence": "the next branch can target numeric arrays rather than re-arguing the readout form"}),
        nonclaim({"decision_id": "DEC2778_1_segment_table_acquired", "decision": "stage the 19 SUEP selected segments as a source-backed table", "evidence": "P8_Y5_R2FR_2778_SUEP_SEGMENT_TABLE_SOURCE_BACKED.csv", "consequence": "future reproducibility work has a first window ledger"}),
        nonclaim({"decision_id": "DEC2778_2_no_claim", "decision": "do not claim WEP/local-GR pass", "evidence": "TAU2778_3_verdict; APR2778_0_WEP_kernel_skeleton_product_stub", "consequence": "numeric tau_WEP remains the next barrier"}),
    ]


def build_next() -> list[dict[str, Any]]:
    return [
        nonclaim({
            "row_id": "NEXT2778_0_2779",
            "next_target": "2779-Y5-R2FR-MICROSCOPE-data-portal-schema-or-reconstructed-gxS-kernel-under-AX1090.md",
            "script": "scripts/Y5_R2FR_MICROSCOPE_data_portal_schema_or_reconstructed_gxS_kernel_under_AX1090_2779.py",
            "objective": "turn the official 2778 kernel skeleton into a numeric tau_WEP component by either acquiring the CMSM data schema/products or reconstructing gx,gz,Sxx,Sxz from sourced orbit/attitude/gravity-model inputs for at least one SUEP segment",
            "include": "CMSM portal access notes; file/schema inventory; exact timestamps/masks; gx/gz/Sxx/Sxz arrays or dry-run reconstruction; segment 210 pilot; refusal gates",
            "exclude": "public WEP/local-GR claim; tau=1; guessed phase; guessed masks; measured-G absorption; GitHub; formalization edits",
        })
    ]


def copy_branch_outputs(
    external: list[dict[str, Any]],
    portal: list[dict[str, Any]],
    kernel: list[dict[str, Any]],
    segments: list[dict[str, Any]],
    tau: list[dict[str, Any]],
    candidate: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    kernel_rows = external + portal + kernel + tau + candidate + bounds + gates
    segment_rows = segments + tau + gates
    beta_rows = kernel + tau + next_rows
    microscope_rows = external + portal + kernel + segments + tau + candidate + bounds + next_rows
    specs = [
        ("BR2778_0_kernel_queue", "kernel", kernel_rows, OUTPUTS["kernel"], BRANCH_OUTPUTS["kernel_queue"], "official MICROSCOPE kernel skeleton nonclaim copy"),
        ("BR2778_1_segment_queue", "segments", segment_rows, OUTPUTS["segments"], BRANCH_OUTPUTS["segment_queue"], "SUEP segment table nonclaim copy"),
        ("BR2778_2_beta_doc", "beta_doc", beta_rows, OUTPUTS["tau"], BRANCH_OUTPUTS["beta_doc"], "beta/source-facing kernel skeleton copy"),
        ("BR2778_3_microscope_copy", "microscope", microscope_rows, OUTPUTS["candidate"], BRANCH_OUTPUTS["microscope_copy"], "MICROSCOPE kernel skeleton acquisition copy"),
        ("BR2778_4_next_queue", "next", next_rows, OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "next data portal or reconstructed gxS target"),
    ]
    rows = []
    for copy_id, table_key, source_rows, source_table, copy_path, purpose in specs:
        write_csv(copy_path, source_rows)
        rows.append(nonclaim({
            "copy_id": copy_id,
            "table_key": table_key,
            "source_table": rel(source_table),
            "copy_path": rel(copy_path),
            "purpose": purpose,
            "exists": copy_path.exists(),
            "row_count": csv_row_count(copy_path) if copy_path.exists() else 0,
        }))
    return rows


def generated_files_under_work() -> bool:
    generated = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC]
    return all(WORK in path.parents or path == WORK for path in generated)


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    for path in FORMALIZATION.rglob("*"):
        if path.is_file() and path.stat().st_mtime > RUN_STARTED_UTC.timestamp():
            return False
    return True


def no_claim_flags(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in rows_by_name.values():
        for row in rows:
            if str(row.get("valid_for_claim", "False")).lower() == "true":
                return False
            if str(row.get("claim_allowed", "False")).lower() == "true":
                return False
            if str(row.get("pass_for_claim", "False")).lower() == "true":
                return False
    return True


def remove_pycache() -> None:
    pycache = SCRIPTS / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def segment_duration_sum(segments: list[dict[str, Any]]) -> int:
    total = 0
    for row in segments:
        total += int(str(row.get("duration_orbits", "0")))
    return total


def build_validation(rows_by_name: dict[str, list[dict[str, Any]]], csv_paths: list[Path]) -> list[dict[str, Any]]:
    sources = rows_by_name["sources"]
    external = rows_by_name["external"]
    portal = rows_by_name["portal"]
    kernel = rows_by_name["kernel"]
    segments = rows_by_name["segments"]
    tau = rows_by_name["tau"]
    candidate = rows_by_name["candidate"]
    bounds = rows_by_name["bounds"]
    runner = rows_by_name["runner"]
    gates = rows_by_name["gates"]
    next_rows = rows_by_name["next"]
    branches = rows_by_name["branches"]
    checks = [
        ("VAL2778_0_sources", all(row["exists"] and row["needle_found"] for row in sources), "every cited source path exists and source needle was found"),
        ("VAL2778_1_external_kernel_sources", len(external) >= 10 and any(row["external_id"] == "EXT2778_3_fundamental_eq6" for row in external) and any(row["external_id"] == "EXT2778_9_onera_data_availability_page" for row in external), "official model equations and ONERA data pointer recorded"),
        ("VAL2778_2_data_portal_probe_recorded", len(portal) == 2 and all(row["url"].startswith("https://") and row["probe_status"] for row in portal), "ONERA and CMSM URLs were probed and outcome recorded"),
        ("VAL2778_3_kernel_skeleton_acquired", any(row["kernel_id"] == "KER2778_6_verdict" and row["acquired_level"] == "KERNEL_SKELETON_YES_NUMERIC_TAU_NO" for row in kernel), "kernel skeleton acquired but numeric tau not acquired"),
        ("VAL2778_4_source_worldtube_proxy_only", any(row["kernel_id"] == "KER2778_7_source_worldtube_verdict" and row["acquired_level"] == "SOURCE_WORLDTUBE_PROXY_FORM_ONLY" for row in kernel), "source-worldtube remains proxy-only"),
        ("VAL2778_5_suep_segments", len(segments) == 19 and segment_duration_sum(segments) == 1362 and all(is_numeric(row["duration_orbits"]) and int(str(row["duration_orbits"])) > 0 for row in segments), "19 SUEP segments total 1362 orbits"),
        ("VAL2778_6_tau_not_acquired", any(row["tau_status_id"] == "TAU2778_3_verdict" and row["status"] == "NOT_ACQUIRED" and row["claim_allowed"] is False for row in tau), "tau_WEP numeric verdict remains blocked"),
        ("VAL2778_7_prediction_nonclaim_missing", len(candidate) == 1 and candidate[0]["valid_for_claim"] is False and has_missing_marker(candidate[0]), "prediction row stays nonclaim and missing numeric kernel"),
        ("VAL2778_8_bound_numeric", len(bounds) == 1 and is_numeric(bounds[0]["bound_value"]) and float(str(bounds[0]["bound_value"])) > 0.0 and bounds[0]["bound_valid_for_internal_runner"] is True, "bound import has positive numeric value"),
        ("VAL2778_9_runner_refuses", runner[0]["valid_prediction_rows"] == 0 and runner[0]["claim_allowed"] is False, "runner reports no valid prediction rows and claim false"),
        ("VAL2778_10_claim_gates_safe", all(row["claim_allowed"] is False for row in gates) and any(row["gate_id"] == "CG2778_0_official_kernel_skeleton" and row["gate_pass"] is True for row in gates), "claim gates allow source acquisition only as nonclaim plumbing"),
        ("VAL2778_11_next_target", any(row["row_id"] == "NEXT2778_0_2779" and "data-portal-schema-or-reconstructed-gxS-kernel" in row["next_target"] for row in next_rows), "next target selects data portal schema or reconstructed gxS kernel"),
        ("VAL2778_12_branch_outputs", all(row["exists"] and int(row["row_count"]) > 0 for row in branches), "branch copies exist and contain rows"),
        ("VAL2778_13_csv_parse", all(csv_parses(path) for path in csv_paths), "all generated CSV outputs parse cleanly"),
        ("VAL2778_14_no_claim_flags", no_claim_flags(rows_by_name), "no generated row is valid_for_claim=true/claim_allowed=true/pass_for_claim=true"),
        ("VAL2778_15_generated_under_post_checkpoint", generated_files_under_work(), "all generated outputs are under post-checkpoint-work"),
        ("VAL2778_16_formalization_untouched", formalization_untouched(), "formalization-workbench modified-file count remains zero during this run"),
        ("VAL2778_17_pycache_absent", not (SCRIPTS / "__pycache__").exists(), "scripts __pycache__ removed"),
    ]
    rows = [{"validation_id": check_id, "passed": passed, "detail": detail, "timestamp_utc": ts()} for check_id, passed, detail in checks]
    rows.append({
        "validation_id": "VAL2778_OVERALL",
        "passed": all(row["passed"] for row in rows),
        "detail": "2778 ports the official MICROSCOPE full readout-kernel skeleton and 19-segment SUEP table into the current R2/f(R) branch, records live portal probes, keeps source-worldtube numeric form and tau_WEP missing, refuses skeleton-only WEP scoring, blocks WEP/local-GR claims, and selects data portal schema or reconstructed gx/gz/Sxx/Sxz kernel as 2779.",
        "timestamp_utc": ts(),
    })
    return rows


def build_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> str:
    return "\n\n".join([
        "# 2778 - Y5 R2/f(R): MICROSCOPE Full Orbit Kernel Or Source-Worldtube Row Under AX1090",
        "## Private Verdict\n\n2778 gets us a real step closer, but not over the line: the current R2/f(R) branch now has the official MICROSCOPE WEP readout-kernel skeleton and 19 SUEP segment ledger staged in source-backed form. The actual numeric tau_WEP product is still not acquired, because gx/gz/Sxx/Sxz arrays, exact timestamps/masks, and the MTS residual-to-eta projection remain missing.",
        "## Source Register\n\n" + markdown_table(rows_by_name["sources"], ["row_id", "source_key", "source_path", "exists", "needle_found", "source_role", "valid_for_claim"]),
        "## External Kernel Source Ledger\n\n" + markdown_table(rows_by_name["external"], ["external_id", "source_url", "doi", "source_lines", "kernel_status", "kernel_item", "port_status", "valid_for_claim"]),
        "## Data Portal Probe\n\n" + markdown_table(rows_by_name["portal"], ["url", "probe_status", "http_status", "bytes_sampled", "error", "valid_for_claim"]),
        "## Official Kernel Components\n\n" + markdown_table(rows_by_name["kernel"], ["kernel_id", "component", "official_form", "acquired_level", "needed_numeric_inputs", "branch_status", "valid_for_claim"]),
        "## SUEP Segment Table\n\n" + markdown_table(rows_by_name["segments"], ["segment_id", "duration_orbits", "position_begin_orbit", "position_end_orbit", "glitch_eliminated_percent", "source_id", "numeric_tau_status", "valid_for_claim"]),
        "## Tau Projection Status\n\n" + markdown_table(rows_by_name["tau"], ["tau_status_id", "object", "status", "remaining_gap", "claim_allowed", "valid_for_claim"]),
        "## Nonclaim Product Candidate\n\n" + markdown_table(rows_by_name["candidate"], ["prediction_id", "arena", "product_symbol", "product_value", "product_units", "derivation_status", "notes", "valid_for_claim"]),
        "## Bound Import\n\n" + markdown_table(rows_by_name["bounds"], ["bound_id", "arena", "product_symbol", "bound_value", "bound_units", "bound_type", "source_row_id", "bound_valid_for_internal_runner", "valid_for_claim"]),
        "## Product Runner Status\n\n" + markdown_table(rows_by_name["runner"], ["runner_id", "prediction_rows", "bound_rows", "valid_prediction_rows", "valid_bound_rows", "claim_allowed", "expected_result", "valid_for_claim"]),
        "## Product Comparison Rows\n\n" + markdown_table(rows_by_name["comparisons"], ["comparison_id", "comparison_status", "pass_for_claim", "issues", "valid_for_claim"]),
        "## Claim Gates\n\n" + markdown_table(rows_by_name["gates"], ["gate_id", "claim_component", "gate_pass", "claim_allowed", "reason", "valid_for_claim"]),
        "## Decision Ledger\n\n" + markdown_table(rows_by_name["decision"], ["decision_id", "decision", "evidence", "consequence", "valid_for_claim"]),
        "## Next Target\n\n" + markdown_table(rows_by_name["next"], ["row_id", "next_target", "script", "objective", "include", "exclude", "valid_for_claim"]),
        "## Branch Copies\n\n" + markdown_table(rows_by_name["branches"], ["copy_id", "table_key", "source_table", "copy_path", "purpose", "exists", "row_count", "valid_for_claim"]),
        "## Validation\n\n" + markdown_table(rows_by_name["validation"], ["validation_id", "passed", "detail", "timestamp_utc"]),
        "## Plain-English Read\n\nThe boring-looking bit here is actually the win: we now know the official MICROSCOPE projection shape we must hit. No tau handwave, no unity shortcut, no measured-G hiding place. Next we either get the CMSM schema/products or reconstruct the gx/gz/Sxx/Sxz design columns for one SUEP segment.",
        "",
    ])


def main() -> None:
    ensure_dirs()
    sources = build_sources()
    external = build_external_rows()
    portal = build_portal_rows()
    kernel = build_kernel_rows()
    segments = build_segment_rows()
    tau = build_tau_rows()
    candidate = build_candidate_rows()
    bounds = build_bound_rows()
    runner, comparisons = run_product_runner(candidate, bounds)
    gates = build_gates()
    decision = build_decisions()
    next_rows = build_next()

    for key, rows in [
        ("sources", sources), ("external", external), ("portal", portal), ("kernel", kernel),
        ("segments", segments), ("tau", tau), ("candidate", candidate), ("bounds", bounds),
        ("runner", runner), ("comparisons", comparisons), ("gates", gates), ("decision", decision),
        ("next", next_rows),
    ]:
        write_csv(OUTPUTS[key], rows)

    branches = copy_branch_outputs(external, portal, kernel, segments, tau, candidate, bounds, gates, next_rows)
    write_csv(OUTPUTS["branches"], branches)
    remove_pycache()

    rows_by_name = {
        "sources": sources,
        "external": external,
        "portal": portal,
        "kernel": kernel,
        "segments": segments,
        "tau": tau,
        "candidate": candidate,
        "bounds": bounds,
        "runner": runner,
        "comparisons": comparisons,
        "gates": gates,
        "decision": decision,
        "next": next_rows,
        "branches": branches,
    }
    csv_paths = [path for key, path in OUTPUTS.items() if key != "validation"] + list(BRANCH_OUTPUTS.values())
    validation = build_validation(rows_by_name, csv_paths)
    rows_by_name["validation"] = validation
    write_csv(OUTPUTS["validation"], validation)
    DOC.write_text(build_doc(rows_by_name), encoding="utf-8")
    remove_pycache()

    overall = next(row for row in validation if row["validation_id"] == "VAL2778_OVERALL")
    print(f"2778 complete: overall={overall['passed']}")
    print(f"doc={DOC}")
    print(f"validation={OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
