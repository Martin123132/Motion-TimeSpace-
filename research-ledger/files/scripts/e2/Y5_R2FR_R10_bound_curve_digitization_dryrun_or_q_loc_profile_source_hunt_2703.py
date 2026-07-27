from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "2703"
BRANCH_ID = "Y5_R2FR_R10_BOUND_CURVE_DIGITIZATION_DRYRUN_OR_QLOC_PROFILE_SOURCE_HUNT_2703"

ROOT = Path(__file__).resolve().parents[1]
SOURCE_INTAKE = ROOT / "source-intake"
RESIDUALS = SOURCE_INTAKE / "mts_residuals"
LOCAL_BOUNDS = SOURCE_INTAKE / "local_bounds"
WEP_RESIDUALS = SOURCE_INTAKE / "microscope" / "branch_locked_wep" / "residuals"
SOURCE_WEIGHT = SOURCE_INTAKE / "source-weight"
RAB_QUEUE = SOURCE_INTAKE / "rab-sector" / "acquisition-queue"
CACHE = LOCAL_BOUNDS / "r10_source_cache_2703"

DOC_PATH = ROOT / "2703-Y5-R2FR-R10-bound-curve-digitization-dryrun-or-q-loc-profile-source-hunt.md"

OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_R2FR_2703_SOURCE_REGISTER.csv",
    "web_source_access": RESIDUALS / "P8_Y5_R2FR_2703_WEB_SOURCE_ACCESS_DRYRUN.csv",
    "source_bundle_audit": RESIDUALS / "P8_Y5_R2FR_2703_ARXIV_SOURCE_BUNDLE_AUDIT.csv",
    "bound_curve_dryrun": RESIDUALS / "P8_Y5_R2FR_2703_BOUND_CURVE_DIGITIZATION_DRYRUN.csv",
    "candidate_bound_rows": RESIDUALS / "P8_Y5_R2FR_2703_CANDIDATE_BOUND_ROWS_NONCLAIM.csv",
    "qloc_profile_hunt": RESIDUALS / "P8_Y5_R2FR_2703_QLOC_PROFILE_SOURCE_HUNT.csv",
    "blocker_ledger": RESIDUALS / "P8_Y5_R2FR_2703_BLOCKER_LEDGER.csv",
    "claim_gates": RESIDUALS / "P8_Y5_R2FR_2703_CLAIM_GATES.csv",
    "decision_ledger": RESIDUALS / "P8_Y5_R2FR_2703_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_R2FR_2703_NEXT_TARGET.csv",
    "project_status": RESIDUALS / "P8_Y5_R2FR_2703_PROJECT_STATUS_SNAPSHOT.csv",
    "branch_copies": RESIDUALS / "P8_Y5_R2FR_2703_BRANCH_COPIES.csv",
    "validation": RESIDUALS / f"P8_Y5_BRR545_{CHECKPOINT}_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "local_bound_dryrun": LOCAL_BOUNDS / "R10_bound_curve_digitization_dryrun_2703_NONCLAIM.csv",
    "local_candidate_anchors": LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_CANDIDATE_ANCHOR_ONLY_2703_NONCLAIM.csv",
    "local_qloc_hunt": LOCAL_BOUNDS / "q_loc_profile_source_hunt_2703_NONCLAIM.csv",
    "wep_qloc_hunt": WEP_RESIDUALS / "q_loc_profile_source_hunt_2703_NONCLAIM.csv",
    "source_weight_qloc_hunt": SOURCE_WEIGHT / "QLOC_PROFILE_SOURCE_HUNT_2703_NONCLAIM.csv",
    "rab_next": RAB_QUEUE / "JR2703_APS_SUPPLEMENT_OR_QLOC_PROFILE_DERIVATION_NEXT.csv",
}

SOURCE_SPECS: list[dict[str, Any]] = [
    {
        "source_id": "SRC2703_2702_NEXT",
        "relative_path": "2702-Y5-R2FR-q-loc-radial-profile-or-R10-bound-curve-digitization-input.md",
        "required_needles": ["NEXT2702_0_selected", "QPROF2702_0_required_prediction_row", "VAL2702_OVERALL"],
        "purpose": "imports the selected 2703 execution target and q_loc profile schema",
    },
    {
        "source_id": "SRC2703_563_R10_BLOCKER",
        "relative_path": "563-Y5-R10-real-bound-curve-acquisition-and-alpha-row-smoke-runner.md",
        "required_needles": ["E563_1_full_curve_missing", "B563_0_no_full_bound_curve", "V563_10_no_overclaim"],
        "purpose": "imports the prior R10 full-curve blocker and no-overclaim rule",
    },
    {
        "source_id": "SRC2703_ANCHOR_SMOKE",
        "relative_path": "source-intake/local_bounds/R10_alpha_lambda_bound_curve_ANCHOR_SMOKE.csv",
        "required_needles": ["R10_ANCHOR_EOTWASH_2020_ALPHA1_38P6UM", "R10_ANCHOR_EOTWASH_2007_ALPHA1_56UM"],
        "purpose": "imports source-backed anchor-only rows for nonclaim smoke use",
    },
    {
        "source_id": "SRC2703_LIVE_DIGITIZED_PLACEHOLDER",
        "relative_path": "source-intake/local_bounds/R10_alpha_lambda_bound_curve_DIGITIZED.csv",
        "required_needles": ["R10_BOUND_PLACEHOLDER_0", "MISSING_NUMERIC_LAMBDA"],
        "purpose": "confirms the live digitized curve remains invalid placeholder data",
    },
    {
        "source_id": "SRC2703_1712_QLOC_TEMPLATE",
        "relative_path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1712_FIRST_QLOC_PROFILE_ROW.csv",
        "required_needles": ["QPROF1712_0_parent_residual_vector", "QPROF1712_1_R10_projection"],
        "purpose": "imports q_loc residual vector and R10 projection templates",
    },
    {
        "source_id": "SRC2703_1790_QLOC_FALLBACK",
        "relative_path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1790_QLOC_PROFILE_FALLBACK.csv",
        "required_needles": ["QLP1790_1_profile_values", "MISSING_NUMERIC_PROFILE"],
        "purpose": "imports q_loc profile fallback status",
    },
    {
        "source_id": "SRC2703_WEB_ACCESS_JSON",
        "relative_path": "source-intake/local_bounds/r10_source_cache_2703/source_access_results_2703.json",
        "required_needles": ["arxiv_abs_2002_11761", "arxiv_pdf_2002_11761", "arxiv_eprint_2002_11761", "aps_supplement_material1_pdf"],
        "purpose": "imports local source-access dry-run evidence",
    },
    {
        "source_id": "SRC2703_ARXIV_BUNDLE_AUDIT",
        "relative_path": "source-intake/local_bounds/r10_source_cache_2703/source_bundle_audit_2703.json",
        "required_needles": ["FB_ISL_pdf.tex", "fig5a.pdf", "fig5b1.pdf"],
        "purpose": "imports arXiv source bundle and figure asset audit",
    },
]


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def as_bool(value: bool) -> str:
    return "true" if value else "false"


def path_for(relative_path: str) -> Path:
    return ROOT / relative_path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def read_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"Refusing to write empty CSV: {path}")
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def parse_csv(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            rows = list(reader)
            if not reader.fieldnames:
                return False, 0, "missing_header"
            return True, len(rows), "parsed"
    except Exception as exc:
        return False, 0, f"{type(exc).__name__}: {exc}"


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    headers = list(rows[0].keys())
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        cells = [str(row.get(header, "")).replace("|", "\\|").replace("\n", "<br>") for header in headers]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for spec in SOURCE_SPECS:
        path = path_for(spec["relative_path"])
        text = read_text(path)
        needles = list(spec["required_needles"])
        found = [needle for needle in needles if needle in text]
        missing = [needle for needle in needles if needle not in text]
        rows.append(
            {
                "source_id": spec["source_id"],
                "relative_path": spec["relative_path"],
                "absolute_path": str(path),
                "exists": as_bool(path.exists()),
                "required_needles": ";".join(needles),
                "found_needles": ";".join(found),
                "missing_needles": ";".join(missing),
                "purpose": spec["purpose"],
                "valid_for_claim": "false",
                "timestamp_utc": stamp(),
            }
        )
    return rows


def web_source_access_rows() -> list[dict[str, Any]]:
    access = read_json(CACHE / "source_access_results_2703.json", [])
    rows: list[dict[str, Any]] = []
    for item in access:
        status = str(item.get("status", "missing"))
        key = str(item.get("key", "unknown"))
        supports_claim = "false"
        extraction_role = "source_locator"
        if key == "arxiv_pdf_2002_11761" and status == "cached":
            extraction_role = "figure_digitization_candidate"
        elif key == "arxiv_eprint_2002_11761" and status == "cached":
            extraction_role = "figure_source_asset_candidate"
        elif key == "aps_supplement_material1_pdf":
            extraction_role = "official_numeric_values_target_blocked_locally"
        elif key.startswith("eotwash"):
            extraction_role = "official_context_page_not_machine_table"
        rows.append(
            {
                "access_id": f"WEB2703_{len(rows)}_{key}",
                "source_key": key,
                "url": item.get("url", ""),
                "status": status,
                "http_status": item.get("http_status", ""),
                "content_type": item.get("content_type", ""),
                "bytes_saved": item.get("bytes_saved", 0),
                "local_file": item.get("local_file", ""),
                "sha256": item.get("sha256", ""),
                "extraction_role": extraction_role,
                "claim_usable_now": supports_claim,
                "notes": item.get("notes", ""),
                "timestamp_utc": stamp(),
            }
        )
    if not rows:
        rows.append(
            {
                "access_id": "WEB2703_0_not_run",
                "source_key": "source_access_results_2703_missing",
                "url": "",
                "status": "not_run",
                "http_status": "",
                "content_type": "",
                "bytes_saved": 0,
                "local_file": "",
                "sha256": "",
                "extraction_role": "blocked_missing_source_access_json",
                "claim_usable_now": "false",
                "notes": "run the local source-access dry-run before treating 2703 as complete",
                "timestamp_utc": stamp(),
            }
        )
    return rows


def source_bundle_audit_rows() -> list[dict[str, Any]]:
    bundle = read_json(CACHE / "source_bundle_audit_2703.json", {})
    members = [str(member) for member in bundle.get("members", [])]
    figures = [str(path) for path in bundle.get("figure_like_files", [])]
    tex_hits = [str(hit.get("needle", "")) for hit in bundle.get("tex_hits", []) if isinstance(hit, dict)]
    has_fig5 = any("fig5" in item.lower() for item in figures + members)
    has_numeric_table = any(item.lower().endswith((".csv", ".dat")) for item in figures + members)
    return [
        {
            "audit_id": "BUNDLE2703_0_unpack",
            "object": "arXiv e-print source bundle",
            "status": bundle.get("mode", "missing_audit"),
            "evidence": ";".join(members) if members else "MISSING_BUNDLE_MEMBERS",
            "interpretation": "source bundle cached and unpacked" if members else "source bundle audit missing",
            "score_ready": "false",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "audit_id": "BUNDLE2703_1_tex",
            "object": "FB_ISL_pdf.tex",
            "status": "tex_needles_found" if tex_hits else "tex_needles_missing",
            "evidence": ";".join(sorted(set(tex_hits))) if tex_hits else "MISSING_TEX_HITS",
            "interpretation": "paper text confirms Yukawa alpha/lambda context and points to supplement for numerical constraints",
            "score_ready": "false",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "audit_id": "BUNDLE2703_2_fig5_assets",
            "object": "fig5a/fig5b1 PDF assets",
            "status": "figure_assets_found" if has_fig5 else "figure_assets_missing",
            "evidence": ";".join(item for item in figures if "fig5" in item.lower()) or "MISSING_FIG5_ASSETS",
            "interpretation": "Fig. 5 bound plot is present graphically; numeric curve still requires supplement retrieval or digitization QA",
            "score_ready": "false",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "audit_id": "BUNDLE2703_3_machine_table",
            "object": "machine-readable bound curve table",
            "status": "not_found_in_arxiv_bundle" if not has_numeric_table else "candidate_machine_table_found",
            "evidence": ";".join(item for item in figures + members if item.lower().endswith((".csv", ".dat"))) or "NO_CSV_OR_DAT_IN_BUNDLE",
            "interpretation": "do not fabricate full curve rows from the paper text; locate supplement or digitize figure",
            "score_ready": "false",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
    ]


def bound_curve_dryrun_rows() -> list[dict[str, Any]]:
    access_rows = web_source_access_rows()
    by_key = {row["source_key"]: row for row in access_rows}
    return [
        {
            "dryrun_id": "BDRY2703_0_arxiv_abs",
            "source": "https://arxiv.org/abs/2002.11761",
            "local_status": by_key.get("arxiv_abs_2002_11761", {}).get("status", "missing"),
            "extraction_result": "metadata_cached_threshold_statement_only",
            "claim_value_status": "anchor_context_only",
            "needed_next": "use PDF/source/supplement for curve; do not score threshold alone",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "dryrun_id": "BDRY2703_1_arxiv_pdf",
            "source": "https://arxiv.org/pdf/2002.11761",
            "local_status": by_key.get("arxiv_pdf_2002_11761", {}).get("status", "missing"),
            "extraction_result": "pdf_cached_fig5_digitization_candidate",
            "claim_value_status": "no_numeric_curve_extracted",
            "needed_next": "digitize Fig. 5 bottom plot only with axis calibration and QA, unless official supplement is acquired first",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "dryrun_id": "BDRY2703_2_arxiv_source",
            "source": "https://arxiv.org/e-print/2002.11761",
            "local_status": by_key.get("arxiv_eprint_2002_11761", {}).get("status", "missing"),
            "extraction_result": "source_bundle_cached_fig5_assets_found_no_csv_dat",
            "claim_value_status": "figure_assets_only",
            "needed_next": "inspect fig5b1.pdf or retrieve APS supplement numerical values",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "dryrun_id": "BDRY2703_3_aps_supplement",
            "source": "https://journals.aps.org/prl/supplemental/10.1103/PhysRevLett.124.101101/suppMaterial1.pdf",
            "local_status": by_key.get("aps_supplement_material1_pdf", {}).get("status", "missing"),
            "extraction_result": "identified_as_official_numeric_target_but_local_fetch_blocked",
            "claim_value_status": "blocked_not_acquired",
            "needed_next": "manual/browser retrieval or alternate accessible mirror before full curve rows become claim-grade",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "dryrun_id": "BDRY2703_4_eotwash_pages",
            "source": "https://www.npl.washington.edu/eotwash/inverse-square-law",
            "local_status": by_key.get("eotwash_inverse_square", {}).get("status", "missing"),
            "extraction_result": "official_context_page_cached_not_machine_table",
            "claim_value_status": "context_only",
            "needed_next": "use as provenance/context, not as full curve data",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
    ]


def candidate_bound_rows() -> list[dict[str, Any]]:
    anchor_path = LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_ANCHOR_SMOKE.csv"
    rows: list[dict[str, Any]] = []
    if anchor_path.exists():
        with anchor_path.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            for row in reader:
                rows.append(
                    {
                        "candidate_id": f"CAND2703_{len(rows)}_{row.get('bound_id', '')}",
                        "bound_id": row.get("bound_id", ""),
                        "dataset_id": row.get("dataset_id", ""),
                        "lambda_value": row.get("lambda_value", ""),
                        "lambda_units": row.get("lambda_units", ""),
                        "alpha_bound": row.get("alpha_bound", ""),
                        "alpha_bound_source": row.get("alpha_bound_source", ""),
                        "digitization_method": row.get("digitization_method", ""),
                        "source_file": row.get("source_file", ""),
                        "row_role": "anchor_only_non_curve_smoke",
                        "why_not_claim": "single alpha_equals_1 threshold anchor is not a full alpha(lambda) curve",
                        "valid_for_claim": "false",
                        "timestamp_utc": stamp(),
                    }
                )
    return rows or [
        {
            "candidate_id": "CAND2703_0_no_anchor_file",
            "bound_id": "NO_ANCHOR_FILE",
            "dataset_id": "missing",
            "lambda_value": "",
            "lambda_units": "",
            "alpha_bound": "",
            "alpha_bound_source": "",
            "digitization_method": "",
            "source_file": "",
            "row_role": "blocked_missing_anchor_file",
            "why_not_claim": "anchor smoke file missing",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        }
    ]


def qloc_profile_hunt_rows() -> list[dict[str, Any]]:
    return [
        {
            "hunt_id": "QH2703_0_1712_parent_vector",
            "source_path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1712_FIRST_QLOC_PROFILE_ROW.csv",
            "object_sought": "q_loc finite residual vector",
            "found_object": "formula/template only",
            "blocking_gap": "MISSING_COMPONENT_LOCK;MISSING_JZ_BZ;MISSING_DELTA_K;MISSING_PLOC_OWNER;MISSING_UNITS",
            "score_ready": "false",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "hunt_id": "QH2703_1_1712_R10_projection",
            "source_path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1712_FIRST_QLOC_PROFILE_ROW.csv",
            "object_sought": "R10 alpha(lambda) projection from q_loc",
            "found_object": "symbolic K_X Qbar_XH qbar_XT template",
            "blocking_gap": "MISSING_PARENT_COEFFICIENTS;MISSING_NUMERIC_PROFILE;MISSING_REAL_BOUND_CURVE",
            "score_ready": "false",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "hunt_id": "QH2703_2_1790_profile_values",
            "source_path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1790_QLOC_PROFILE_FALLBACK.csv",
            "object_sought": "q_loc^nu(r, material, domain) values",
            "found_object": "fallback row says values missing",
            "blocking_gap": "MISSING_NUMERIC_PROFILE;MISSING_UNITS;MISSING_SOURCE_PATH",
            "score_ready": "false",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "hunt_id": "QH2703_3_2038_2039_PPN_rulers",
            "source_path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2038_FIRST_REAL_ROW_ACQUISITION.csv;source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2039_CASSINI_ABSOLUTE_BUDGET.csv",
            "object_sought": "external local bound ruler",
            "found_object": "PPN/Cassini style external target exists but MTS prediction and tails are missing",
            "blocking_gap": "MISSING_MTS_PREDICTION;MISSING_TAIL_COMPONENT_VALUES",
            "score_ready": "false",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "hunt_id": "QH2703_4_theorem_zero_route",
            "source_path": "2702-Y5-R2FR-q-loc-radial-profile-or-R10-bound-curve-digitization-input.md",
            "object_sought": "q_loc theorem-zero certificate",
            "found_object": "schema only; no theorem source bundle",
            "blocking_gap": "MISSING_GAMMA_KHAT_METRIC_RESPONSE;MISSING_EULER_SOURCE_ZERO;MISSING_BOUNDARY_NO_FLUX;MISSING_PLOC_OWNER",
            "score_ready": "false",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "hunt_id": "QH2703_5_verdict",
            "source_path": "profile hunt synthesis",
            "object_sought": "source-backed q_loc R10 profile or exact zero proof",
            "found_object": "NO_SOURCE_BACKED_QLOC_PROFILE",
            "blocking_gap": "derive parent profile or retrieve official bound curve before score work",
            "score_ready": "false",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
    ]


def blocker_ledger_rows() -> list[dict[str, Any]]:
    return [
        {
            "blocker_id": "BLK2703_0_full_curve",
            "blocker": "full alpha(lambda) curve not acquired",
            "evidence": "arXiv PDF/source cached; official supplement identified but blocked by APS 401/403 locally; no CSV/DAT in arXiv source bundle",
            "effect": "R10 score cannot become claim-grade",
            "next_action": "retrieve supplement or digitize Fig. 5 with QA",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "blocker_id": "BLK2703_1_q_loc_profile",
            "blocker": "q_loc R10 profile missing",
            "evidence": "1712/1790 rows are templates; theorem-zero certificate absent",
            "effect": "MTS alpha prediction remains absent",
            "next_action": "derive q_loc radial/range profile or exact zero certificate",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "blocker_id": "BLK2703_2_source_normalization",
            "blocker": "same-frame Newtonian denominator not locked",
            "evidence": "a_N/source mass normalization absent from profile rows",
            "effect": "alpha_q(lambda) cannot be interpreted dimensionlessly",
            "next_action": "lock source/test geometry and normalization with SI units",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "blocker_id": "BLK2703_3_overclaim",
            "blocker": "anchor rows are not full curve rows",
            "evidence": "candidate rows are anchor_only_non_curve_smoke and valid_for_claim=false",
            "effect": "no R10/local-GR pass can be claimed from 2703",
            "next_action": "keep claim gates shut",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "claim_gate_id": "CG2703_0_source_access",
            "gate": "primary R10 sources cached or blocker recorded",
            "status": "PASS_NONCLAIM_SOURCE_ROUTE",
            "gate_passed": "true",
            "claim_allowed": "false",
            "reason": "source route exists but no numeric curve extracted",
            "timestamp_utc": stamp(),
        },
        {
            "claim_gate_id": "CG2703_1_full_curve",
            "gate": "full alpha(lambda) numeric curve",
            "status": "BLOCKED_NONCLAIM",
            "gate_passed": "false",
            "claim_allowed": "false",
            "reason": "official supplement not acquired and figure not digitized",
            "timestamp_utc": stamp(),
        },
        {
            "claim_gate_id": "CG2703_2_q_loc_profile",
            "gate": "source-backed q_loc profile or zero proof",
            "status": "BLOCKED_NONCLAIM",
            "gate_passed": "false",
            "claim_allowed": "false",
            "reason": "only templates and missing-input rows exist",
            "timestamp_utc": stamp(),
        },
        {
            "claim_gate_id": "CG2703_3_R10_runner",
            "gate": "runner can score a live claim",
            "status": "BLOCKED_NONCLAIM",
            "gate_passed": "false",
            "claim_allowed": "false",
            "reason": "both prediction row and full bound curve are absent",
            "timestamp_utc": stamp(),
        },
        {
            "claim_gate_id": "CG2703_4_local_GR",
            "gate": "local GR/Newton recovery",
            "status": "BLOCKED_NONCLAIM",
            "gate_passed": "false",
            "claim_allowed": "false",
            "reason": "q_loc remains unbounded finite residual, not zero/controlled",
            "timestamp_utc": stamp(),
        },
        {
            "claim_gate_id": "CG2703_5_public",
            "gate": "public/GitHub readiness",
            "status": "PRIVATE_NO_ACTION",
            "gate_passed": "false",
            "claim_allowed": "false",
            "reason": "private checkpoint only",
            "timestamp_utc": stamp(),
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC2703_0_bound_route",
            "decision": "SOURCE_ROUTE_FOUND_BUT_CURVE_NOT_ACQUIRED",
            "rationale": "arXiv PDF/source and Eot-Wash pages are cached; arXiv source contains Fig. 5 assets; APS supplement is identified as official numeric target but local retrieval is blocked",
            "next_action": "retrieve supplement or digitize Fig. 5 before any R10 scoring claim",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "decision_id": "DEC2703_1_q_loc_route",
            "decision": "QLOC_PROFILE_NOT_FOUND",
            "rationale": "all local q_loc profile files remain formula/template/fallback rows with missing coefficients, units and source paths",
            "next_action": "try parent-profile derivation or theorem-zero certificate route",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "decision_id": "DEC2703_2_scoring",
            "decision": "NO_R10_SCORING_YET",
            "rationale": "the two inputs needed for a meaningful R10 comparator are still missing",
            "next_action": "do not run the comparator as evidence; only schema/dry-run is allowed",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "decision_id": "DEC2703_3_next",
            "decision": "APS_SUPPLEMENT_OR_QLOC_PROFILE_DERIVATION_NEXT",
            "rationale": "best route is to either acquire official numerical Fig. 5 constraints or derive the MTS q_loc profile; both are now sharply specified",
            "next_action": "run 2704",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT2703_0_selected",
            "selection": "selected_primary",
            "target_doc": "2704-Y5-R2FR-APS-supplement-retrieval-or-q-loc-parent-profile-derivation.md",
            "target_script": "scripts/Y5_R2FR_APS_supplement_retrieval_or_q_loc_parent_profile_derivation_2704.py",
            "task": "try to acquire the official APS supplemental numerical Fig. 5 values; if blocked, prepare a QA digitization route from cached fig5b1.pdf while also attempting the q_loc parent-profile derivation contract",
            "success_condition": "either a full nonclaim numeric alpha(lambda) candidate table exists with provenance and QA flags, or the q_loc parent-profile derivation states exact theorem premises/finite profile inputs still missing",
            "forbidden_shortcuts": "anchor-only scoring; hand-picked graph points without axis QA; invented q_loc profile; symbolic alpha as number; R10/local-GR claim; GitHub action; formalization-workbench edits",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        }
    ]


def project_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "status_id": "STATUS2703_0_R10_data",
            "topic": "R10 bound data",
            "status": "SOURCE_ROUTE_ALIVE_BUT_NOT_SCORE_READY",
            "meaning": "we found and cached the paper/source/figure route and identified the supplement target, but no full curve rows are acquired",
            "next_action": "supplement retrieval or Fig. 5 digitization QA",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "status_id": "STATUS2703_1_q_loc",
            "topic": "q_loc profile",
            "status": "STILL_MISSING",
            "meaning": "local profile/zero theorem remains the live theory gap",
            "next_action": "derive parent profile or theorem-zero certificate",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "status_id": "STATUS2703_2_local_GR",
            "topic": "local GR/Newton",
            "status": "BLOCKED_BUT_MORE_DIAGNOSTIC",
            "meaning": "the blocker is now less vague: control q_loc or provide a boundable nonzero profile",
            "next_action": "2704 derivation/data split",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "status_id": "STATUS2703_3_public",
            "topic": "public/GitHub",
            "status": "NO_ACTION_PRIVATE",
            "meaning": "nothing was pushed; this is private plumbing and derivability discipline",
            "next_action": "keep private",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    return [
        {
            "copy_id": key,
            "path": str(path),
            "relative_path": str(path.relative_to(ROOT)),
            "exists_after_run": as_bool(path.exists()),
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        }
        for key, path in BRANCH_OUTPUTS.items()
    ]


def validate(generated_paths: dict[str, Path], generated_rows: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    validation: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        validation.append({"check_id": check_id, "passed": as_bool(passed), "detail": detail, "timestamp_utc": stamp()})

    sources = generated_rows["source_register"]
    add("VAL2703_0_sources_exist", all(row["exists"] == "true" for row in sources), "all cited local source paths exist")
    add("VAL2703_1_needles_found", all(not row["missing_needles"] for row in sources), "all required source needles were found")

    access = generated_rows["web_source_access"]
    access_keys = {row["source_key"]: row["status"] for row in access}
    add("VAL2703_2_web_access_attempted", {"arxiv_abs_2002_11761", "arxiv_pdf_2002_11761", "arxiv_eprint_2002_11761"}.issubset(access_keys), "primary arXiv access attempts are recorded")
    add("VAL2703_3_arxiv_sources_cached", all(access_keys.get(key) == "cached" for key in ["arxiv_abs_2002_11761", "arxiv_pdf_2002_11761", "arxiv_eprint_2002_11761"]), "arXiv abs/PDF/source are cached")
    add("VAL2703_4_aps_supplement_blocked_recorded", access_keys.get("aps_supplement_material1_pdf") in {"http_error", "url_error", "error"}, "APS supplement attempt is explicitly recorded as blocked")

    bundle = generated_rows["source_bundle_audit"]
    add("VAL2703_5_fig5_assets_found", any(row["audit_id"] == "BUNDLE2703_2_fig5_assets" and row["status"] == "figure_assets_found" for row in bundle), "arXiv source bundle contains Fig. 5 assets")
    add("VAL2703_6_no_machine_table_claim", any(row["audit_id"] == "BUNDLE2703_3_machine_table" and row["status"] == "not_found_in_arxiv_bundle" for row in bundle), "no CSV/DAT machine table was treated as acquired")

    candidates = generated_rows["candidate_bound_rows"]
    all_candidate_nonclaim = all(str(row.get("valid_for_claim", "")).lower() == "false" for row in candidates)
    numeric_anchor_rows = []
    for row in candidates:
        try:
            numeric_anchor_rows.append(float(row.get("lambda_value", "")) > 0 and float(row.get("alpha_bound", "")) > 0)
        except ValueError:
            numeric_anchor_rows.append(False)
    add("VAL2703_7_candidate_rows_nonclaim", all_candidate_nonclaim, "candidate/anchor rows remain valid_for_claim=false")
    add("VAL2703_8_anchor_values_positive", all(numeric_anchor_rows), "anchor-only smoke rows have positive numeric lambda and alpha values")

    qloc = generated_rows["qloc_profile_hunt"]
    add("VAL2703_9_q_loc_missing_recorded", any(row["hunt_id"] == "QH2703_5_verdict" and row["found_object"] == "NO_SOURCE_BACKED_QLOC_PROFILE" for row in qloc), "q_loc profile hunt records no source-backed profile")

    gates = generated_rows["claim_gates"]
    add("VAL2703_10_no_claims", all(row["claim_allowed"] == "false" for row in gates), "all claim gates keep claim_allowed=false")
    add("VAL2703_11_next_2704", any(row["next_id"] == "NEXT2703_0_selected" and "2704" in row["target_doc"] for row in generated_rows["next_target"]), "2704 target selected")
    add("VAL2703_12_no_formalization_outputs", not any("formalization-workbench" in str(path).lower() for path in generated_paths.values()), "no output path points into formalization-workbench")
    add("VAL2703_13_no_github_outputs", not any(".git" in str(path).lower() or "github" in str(path).lower() for path in generated_paths.values()), "no GitHub/public-output path was written")

    for key, path in generated_paths.items():
        ok, count, detail = parse_csv(path)
        add(f"VAL2703_PARSE_{key}", ok and count > 0, f"{detail}; rows={count}")

    core_checks = [row for row in validation if not row["check_id"].startswith("VAL2703_PARSE_validation")]
    overall = all(row["passed"] == "true" for row in core_checks)
    add(
        "VAL2703_OVERALL",
        overall,
        "2703 caches real R10 source routes, identifies the official supplement blocker, audits arXiv Fig. 5 assets, confirms no q_loc profile exists, and keeps all R10/local-GR claims closed",
    )
    return validation


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    sections = [
        ("Web Source Access Dryrun", rows_by_name["web_source_access"]),
        ("Arxiv Source Bundle Audit", rows_by_name["source_bundle_audit"]),
        ("Bound-Curve Digitization Dryrun", rows_by_name["bound_curve_dryrun"]),
        ("Candidate Bound Rows", rows_by_name["candidate_bound_rows"]),
        ("q_loc Profile Source Hunt", rows_by_name["qloc_profile_hunt"]),
        ("Blocker Ledger", rows_by_name["blocker_ledger"]),
        ("Source Register", rows_by_name["source_register"]),
        ("Claim Gates", rows_by_name["claim_gates"]),
        ("Decisions", rows_by_name["decision_ledger"]),
        ("Next Target", rows_by_name["next_target"]),
        ("Project Status", rows_by_name["project_status"]),
        ("Validation", rows_by_name["validation"]),
    ]
    lines = [
        "# 2703: R10 Bound-Curve Digitization Dryrun Or q_loc Profile Source Hunt",
        "",
        f"**Branch:** `{BRANCH_ID}`",
        "",
        "## Private Verdict",
        "",
        "2703 makes a useful, non-glamorous move: the real R10 source route is now live and cached, but it is still not a claim-grade curve. The arXiv paper, PDF, source bundle, and Eöt-Wash context pages cached successfully; the source bundle contains Fig. 5 assets, but no machine-readable CSV/DAT curve. The official APS supplemental numerical material is identified as the clean target, but local retrieval is blocked by 401/403. On the theory side, the q_loc profile hunt still finds templates and missing-input ledgers, not a source-backed radial/range profile or exact zero proof.",
        "",
        "## Bottom Line",
        "",
        "- R10 data path: alive, sourced, but not score-ready.",
        "- MTS prediction path: still missing q_loc profile or theorem-zero certificate.",
        "- Claim posture: no R10 pass, no local-GR pass, no public claim.",
        "- Best next move: retrieve the official supplement or run a QA digitization of cached Fig. 5 while continuing the q_loc parent-profile derivation route.",
        "",
    ]
    for title, rows in sections:
        lines.extend([f"## {title}", "", markdown_table(rows), ""])
    DOC_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    rows_by_name: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register_rows(),
        "web_source_access": web_source_access_rows(),
        "source_bundle_audit": source_bundle_audit_rows(),
        "bound_curve_dryrun": bound_curve_dryrun_rows(),
        "candidate_bound_rows": candidate_bound_rows(),
        "qloc_profile_hunt": qloc_profile_hunt_rows(),
        "blocker_ledger": blocker_ledger_rows(),
        "claim_gates": claim_gate_rows(),
        "decision_ledger": decision_rows(),
        "next_target": next_target_rows(),
        "project_status": project_status_rows(),
    }

    for name, path in OUTPUTS.items():
        if name in {"validation", "branch_copies"}:
            continue
        write_csv(path, rows_by_name[name])

    write_csv(BRANCH_OUTPUTS["local_bound_dryrun"], rows_by_name["bound_curve_dryrun"])
    write_csv(BRANCH_OUTPUTS["local_candidate_anchors"], rows_by_name["candidate_bound_rows"])
    write_csv(BRANCH_OUTPUTS["local_qloc_hunt"], rows_by_name["qloc_profile_hunt"])
    write_csv(BRANCH_OUTPUTS["wep_qloc_hunt"], rows_by_name["qloc_profile_hunt"])
    write_csv(BRANCH_OUTPUTS["source_weight_qloc_hunt"], rows_by_name["qloc_profile_hunt"])
    write_csv(BRANCH_OUTPUTS["rab_next"], rows_by_name["next_target"])

    branch_rows = branch_copy_rows()
    rows_by_name["branch_copies"] = branch_rows
    write_csv(OUTPUTS["branch_copies"], branch_rows)

    generated_paths = {name: path for name, path in OUTPUTS.items() if name != "validation"}
    generated_paths.update(BRANCH_OUTPUTS)
    validation_rows = validate(generated_paths, rows_by_name)
    rows_by_name["validation"] = validation_rows
    write_csv(OUTPUTS["validation"], validation_rows)

    write_doc(rows_by_name)
    print(f"wrote {DOC_PATH}")
    print(f"wrote {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
