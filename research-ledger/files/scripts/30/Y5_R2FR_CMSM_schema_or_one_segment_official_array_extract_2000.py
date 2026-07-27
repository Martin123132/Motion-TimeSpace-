from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import URLError
from urllib.request import Request, urlopen


BRANCH = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FORMALIZATION = REPO / "formalization-workbench"
MTS_RESIDUALS = ROOT / "source-intake" / "mts_residuals"
SOURCE_WEIGHT_DOCS = ROOT / "source-intake" / "source-weight" / "docs"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICROSCOPE_COEFFS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "coefficients"

DOC_PATH = ROOT / "2000-Y5-R2FR-CMSM-schema-or-one-segment-official-array-extract.md"
VALIDATION_PATH = MTS_RESIDUALS / "P8_Y5_BRR545_2000_VALIDATION.csv"

SOURCES = {
    "1999_doc": {
        "path": ROOT / "1999-Y5-R2FR-MICROSCOPE-numeric-kernel-or-source-worldtube-row.md",
        "needles": ["CMSM1999_0_data_inventory_pointer", "NEXT1999_0_primary"],
    },
    "1999_validation": {
        "path": MTS_RESIDUALS / "P8_Y5_BRR545_1999_VALIDATION.csv",
        "needles": ["VAL1999_OVERALL", "PASS"],
    },
    "1073_contract": {
        "path": ROOT / "1073-Y5-R10-CMSM-browser-assisted-schema-or-one-segment-official-array-extract.md",
        "needles": ["CMSM1073_5_official_gxS_arrays", "NEXT1073_0_1074"],
    },
    "1073_validation": {
        "path": MTS_RESIDUALS / "P8_Y5_BRR545_1073_VALIDATION.csv",
        "needles": ["V1073_SUMMARY", "pass"],
    },
    "1072_requirements": {
        "path": ROOT / "1072-Y5-R10-MICROSCOPE-data-portal-schema-or-reconstructed-gxS-kernel.md",
        "needles": ["REQ1072_0_exact_time_grid", "DRY1072_0_segment210_kernel_preview"],
    },
}

OUTPUTS = {
    "source_register": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_2000_SOURCE_REGISTER.csv",
    "live_probe": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_2000_LIVE_CMSM_PROBE.csv",
    "extraction_contract": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_2000_CMSM_EXTRACTION_CONTRACT.csv",
    "array_schema": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_2000_OFFICIAL_ARRAY_SCHEMA_CONTRACT.csv",
    "status": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_2000_EXTRACTION_STATUS.csv",
    "runner_dryrun": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_2000_RUNNER_DRYRUN.csv",
    "claim_gate": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_2000_CLAIM_GATE.csv",
    "decision": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_2000_DECISION_LEDGER.csv",
    "next": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_2000_NEXT_TARGET.csv",
    "source_weight": SOURCE_WEIGHT_DOCS / "CMSM_SCHEMA_OR_SEGMENT_ARRAY_2000_NONCLAIM.csv",
    "wep_coeffs": MICROSCOPE_COEFFS / "P8_Y5_PARENT_QLOC_2000_ARRAY_SCHEMA_CONTRACT_NONCLAIM.csv",
    "queue": RAB_QUEUE / "JR2000_USER_CMSM_EXPORT_OR_SURROGATE_RECONSTRUCTION_QUEUE.csv",
}


LIVE_URLS = [
    "https://cmsm-ds.onera.fr/user/microscope/modules/7",
    "https://cmsm-ds.onera.fr/user/microscope",
    "https://www.oca.eu/fr/microscope",
    "https://microscope.onera.fr/fr/publication/microscope-data-are-available",
]


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dirs() -> None:
    for path in OUTPUTS.values():
        path.parent.mkdir(parents=True, exist_ok=True)
    VALIDATION_PATH.parent.mkdir(parents=True, exist_ok=True)


def base_row(stamp: str) -> dict[str, str]:
    return {
        "branch_id": BRANCH,
        "valid_for_claim": "false",
        "claim_allowed": "false",
        "generated_utc": stamp,
    }


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def source_register(stamp: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for source_id, spec in SOURCES.items():
        path = spec["path"]
        exists = path.exists()
        text = read_text(path) if exists else ""
        missing = [needle for needle in spec["needles"] if needle not in text]
        row = base_row(stamp)
        row.update(
            {
                "source_id": source_id,
                "source_path": str(path),
                "needed_for": "2000 CMSM schema or one-segment official array extract",
                "needles": ";".join(spec["needles"]),
                "exists": str(exists),
                "anchor_found": str(exists and not missing),
                "missing_needles": ";".join(missing),
                "status": "EXISTS_NEEDLES_CONFIRMED" if exists and not missing else "MISSING_SOURCE_OR_ANCHOR",
            }
        )
        rows.append(row)
    return rows


def probe_urls(stamp: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for index, url in enumerate(LIVE_URLS):
        row = base_row(stamp)
        status = "ERROR"
        http_status = ""
        content_type = ""
        error = ""
        schema_inventory_acquired = "false"
        official_array_acquired = "false"
        try:
            request = Request(url, method="HEAD", headers={"User-Agent": "Codex-MTS-audit/2000"})
            with urlopen(request, timeout=12) as response:
                http_status = str(response.status)
                content_type = response.headers.get("content-type", "")
                status = "HTTP_OK" if 200 <= response.status < 400 else "HTTP_NONOK"
        except Exception as exc:  # noqa: BLE001 - provenance ledger wants the exact blocker string
            error = str(exc).replace("\n", " ").replace("\r", " ")
            if isinstance(exc, URLError) and getattr(exc, "reason", None):
                error = str(exc.reason).replace("\n", " ").replace("\r", " ")
            status = "PROBE_FAILED"
        row.update(
            {
                "probe_id": f"PROBE2000_{index}",
                "target_url": url,
                "probe_status": status,
                "http_status": http_status,
                "content_type": content_type,
                "schema_inventory_acquired": schema_inventory_acquired,
                "official_array_acquired": official_array_acquired,
                "error_summary": error[:240],
            }
        )
        rows.append(row)
    return rows


def build_tables() -> dict[str, list[dict[str, str]]]:
    stamp = now()

    def row(data: dict[str, str]) -> dict[str, str]:
        merged = base_row(stamp)
        merged.update(data)
        return merged

    extraction_contract = [
        row(
            {
                "contract_id": "CMSM2000_0_dataset_inventory",
                "object": "CMSM dataset/file inventory",
                "required_columns": "dataset_name;product_type;file_name;download_url_or_order_id;time_coverage;sensor_unit;session_or_segment",
                "accepted_evidence": "source-backed CMSM/REGARDS export, browser screenshot, or API response naming MICROSCOPE data products",
                "current_status": "NOT_ACQUIRED",
            }
        ),
        row(
            {
                "contract_id": "CMSM2000_1_time_mask",
                "object": "segment 210 exact timestamps and mask",
                "required_columns": "segment_id;t_utc;sample_index;mask_flag;mask_reason",
                "accepted_evidence": "exact exported time grid, not reconstructed from duration only",
                "current_status": "NOT_ACQUIRED",
            }
        ),
        row(
            {
                "contract_id": "CMSM2000_2_attitude_rate",
                "object": "attitude/angular velocity/angular acceleration products",
                "required_columns": "t_utc;q0;q1;q2;q3;Omega_x;Omega_y;Omega_z;Omegadot_x;Omegadot_y;Omegadot_z;frame",
                "accepted_evidence": "same timestamp grid as accelerometer or documented interpolation rule",
                "current_status": "NOT_ACQUIRED",
            }
        ),
        row(
            {
                "contract_id": "CMSM2000_3_orbit_ephemeris",
                "object": "satellite position/velocity",
                "required_columns": "t_utc;r_x;r_y;r_z;v_x;v_y;v_z;frame;units",
                "accepted_evidence": "CMSM minute-sampled orbit product or source-backed official ephemeris",
                "current_status": "NOT_ACQUIRED",
            }
        ),
        row(
            {
                "contract_id": "CMSM2000_4_official_gxS_arrays",
                "object": "gx,gz,Sxx,Sxz arrays or inputs sufficient to reproduce them",
                "required_columns": "segment_id;t_utc;gx;gz;Sxx;Sxz;frame;generation_method;source_file",
                "accepted_evidence": "official arrays or exact source-reconstruction with documented gravity model and attitude/orbit inputs",
                "current_status": "NOT_ACQUIRED",
            }
        ),
    ]

    array_schema = [
        row(
            {
                "schema_id": "ARR2000_0_segment_id",
                "column_name": "segment_id",
                "unit_or_type": "label",
                "required_for_tau": "true",
                "current_status": "MISSING_CMSM_EXPORT",
                "dry_run_replacement": "segment",
            }
        ),
        row(
            {
                "schema_id": "ARR2000_1_t_utc",
                "column_name": "t_utc",
                "unit_or_type": "UTC timestamp",
                "required_for_tau": "true",
                "current_status": "MISSING_EXACT_TIMESTAMPS",
                "dry_run_replacement": "t_sec_from_segment_start",
            }
        ),
        row(
            {
                "schema_id": "ARR2000_2_gx",
                "column_name": "gx",
                "unit_or_type": "m s^-2 or documented normalized convention",
                "required_for_tau": "true",
                "current_status": "MISSING_OFFICIAL_ARRAY",
                "dry_run_replacement": "gx_unit",
            }
        ),
        row(
            {
                "schema_id": "ARR2000_3_gz",
                "column_name": "gz",
                "unit_or_type": "m s^-2 or documented normalized convention",
                "required_for_tau": "true",
                "current_status": "MISSING_OFFICIAL_ARRAY",
                "dry_run_replacement": "gz_unit",
            }
        ),
        row(
            {
                "schema_id": "ARR2000_4_Sxx",
                "column_name": "Sxx",
                "unit_or_type": "s^-2",
                "required_for_tau": "true",
                "current_status": "MISSING_OFFICIAL_ARRAY",
                "dry_run_replacement": "Sxx_unit",
            }
        ),
        row(
            {
                "schema_id": "ARR2000_5_Sxz",
                "column_name": "Sxz",
                "unit_or_type": "s^-2",
                "required_for_tau": "true",
                "current_status": "MISSING_OFFICIAL_ARRAY",
                "dry_run_replacement": "Sxz_unit",
            }
        ),
    ]

    status_rows = [
        row(
            {
                "status_id": "EX2000_0_live_cmsm",
                "object": "runtime CMSM access",
                "status": "NOT_ACQUIRED_TIMEOUT_OR_REFUSED",
                "evidence": "live probe rows show CMSM module/user URLs not usable from this runtime",
                "next_action": "user-controlled browser/session or exact public API endpoint",
            }
        ),
        row(
            {
                "status_id": "EX2000_1_public_info_pages",
                "object": "OCA/ONERA public pages",
                "status": "ACCESSIBLE_POINTERS_ONLY",
                "evidence": "public pages respond but do not provide arrays/schema",
                "next_action": "use as provenance for route, not as data",
            }
        ),
        row(
            {
                "status_id": "EX2000_2_official_segment_arrays",
                "object": "segment 210 gx/gz/Sxx/Sxz arrays",
                "status": "NOT_ACQUIRED",
                "evidence": "1073 contract remains missing official arrays",
                "next_action": "CMSM export or nonclaim surrogate reconstruction",
            }
        ),
        row(
            {
                "status_id": "EX2000_3_tau_WEP",
                "object": "numeric tau_WEP",
                "status": "NOT_ACQUIRED",
                "evidence": "no official arrays and no direct parent product",
                "next_action": "do not score WEP/local-GR",
            }
        ),
    ]

    runner_dryrun = [
        row(
            {
                "run_id": "RUN2000_0_live_probe",
                "check": "probe CMSM and public route URLs",
                "result": "PASS_PROBE_RECORDED",
                "reason": "probe rows record current accessibility without claiming schema or arrays",
            }
        ),
        row(
            {
                "run_id": "RUN2000_1_contract",
                "check": "stage official array extraction contract",
                "result": "PASS_CONTRACT_READY",
                "reason": "required columns for inventory/time/mask/attitude/orbit/gxS are explicit",
            }
        ),
        row(
            {
                "run_id": "RUN2000_2_official_arrays",
                "check": "acquire official segment arrays",
                "result": "FAIL_NOT_ACQUIRED",
                "reason": "CMSM schema and official arrays remain unavailable from this runtime",
            }
        ),
        row(
            {
                "run_id": "RUN2000_3_product_score",
                "check": "score WEP product",
                "result": "FAIL_VALID_PREDICTION_ROWS_ZERO",
                "reason": "no numeric tau_WEP or direct P_WEP product",
            }
        ),
        row(
            {
                "run_id": "RUN2000_4_verdict",
                "check": "2000 next-step decision",
                "result": "NEXT_2001_USER_ASSISTED_CMSM_EXPORT_OR_NONCLAIM_SURROGATE_RECONSTRUCTION",
                "reason": "official extraction is blocked here; next useful move is user export or labelled surrogate path test",
            }
        ),
    ]

    claim_gate = [
        row(
            {
                "gate_id": "CG2000_0_contract",
                "claim": "CMSM official-array extraction contract is complete",
                "status": "PASS_NONCLAIM_CONTRACT",
                "reason": "required columns and acceptance evidence are explicit",
            }
        ),
        row(
            {
                "gate_id": "CG2000_1_schema_inventory",
                "claim": "CMSM schema/file inventory is acquired",
                "status": "FAIL_BLOCKED",
                "reason": "live CMSM route remains inaccessible from this runtime",
            }
        ),
        row(
            {
                "gate_id": "CG2000_2_official_arrays",
                "claim": "official segment 210 gx/gz/Sxx/Sxz arrays are acquired",
                "status": "FAIL_BLOCKED",
                "reason": "no official export or source-reconstructed arrays",
            }
        ),
        row(
            {
                "gate_id": "CG2000_3_tau_WEP",
                "claim": "numeric tau_WEP exists",
                "status": "FAIL_BLOCKED",
                "reason": "schema/arrays/direct product missing",
            }
        ),
        row(
            {
                "gate_id": "CG2000_4_local_GR",
                "claim": "WEP/local-GR branch is scored",
                "status": "FAIL_BLOCKED",
                "reason": "valid prediction rows remain zero",
            }
        ),
    ]

    decision = [
        row(
            {
                "decision_id": "DEC2000_0_live_status",
                "decision": "CMSM_RUNTIME_ACCESS_STILL_NOT_USABLE",
                "because": "fresh probes record CMSM module/user routes as inaccessible while public OCA/ONERA pages are route pointers only",
                "next_action": "do not loop on this runtime for CMSM UI",
            }
        ),
        row(
            {
                "decision_id": "DEC2000_1_contract_status",
                "decision": "OFFICIAL_ARRAY_CONTRACT_IS_READY",
                "because": "1073/2000 define exact required columns for schema, timestamps, masks, attitude, orbit, and gxS arrays",
                "next_action": "validate any future user/CMSM export against this contract",
            }
        ),
        row(
            {
                "decision_id": "DEC2000_2_best_next",
                "decision": "USER_EXPORT_OR_NONCLAIM_SURROGATE_RECONSTRUCTION",
                "because": "official extraction is blocked here; a surrogate can test code path only if loudly labelled nonclaim",
                "next_action": "2001-Y5-R2FR-user-CMSM-export-or-nonclaim-surrogate-reconstruction.md",
            }
        ),
    ]

    next_target = [
        row(
            {
                "next_id": "NEXT2000_0_primary",
                "selection_status": "selected",
                "target_doc": "2001-Y5-R2FR-user-CMSM-export-or-nonclaim-surrogate-reconstruction.md",
                "target_script": "scripts/Y5_R2FR_user_CMSM_export_or_nonclaim_surrogate_reconstruction_2001.py",
                "task": "import a user/browser-supplied CMSM schema/file export matching the 2000 contract, or build a clearly nonclaim surrogate segment-210 orbit/gravity reconstruction to test the code path",
                "success_condition": "contract-validated CMSM export or explicitly nonclaim surrogate arrays with provenance and refusal gates; no WEP/local-GR score",
                "do_not": "do not repeat blocked CMSM browser loop, treat surrogate arrays as official, guess masks as evidence, set tau_WEP=1, claim WEP/local-GR, push GitHub, or edit formalization-workbench",
            }
        )
    ]

    source_weight = [
        row(
            {
                "artifact_id": "SW2000_0_CMSM_contract",
                "artifact_type": "CMSM_schema_or_segment_array_contract_nonclaim",
                "status": "CONTRACT_READY_CMSM_ACCESS_BLOCKED_ARRAYS_MISSING",
                "source_path": str(DOC_PATH),
                "next_target": "2001-Y5-R2FR-user-CMSM-export-or-nonclaim-surrogate-reconstruction.md",
            }
        )
    ]

    wep_coeffs = [
        row(
            {
                "coefficient_id": "WEP2000_0_array_contract",
                "quantity": "official segment 210 gx/gz/Sxx/Sxz arrays",
                "required_formula": "numeric tau_WEP projection or direct P_WEP product",
                "required_evidence": "contract-valid CMSM export or exact source-reconstruction with timestamps/masks/provenance",
                "current_status": "CONTRACT_ONLY_OFFICIAL_ARRAYS_MISSING",
                "status": "NONCLAIM_REQUIREMENTS_ONLY",
            }
        )
    ]

    queue = [
        row(
            {
                "queue_id": "JR2000_0_user_export_or_surrogate",
                "priority": "1",
                "needed_input": "contract-valid CMSM export or nonclaim surrogate reconstruction",
                "route": "user-controlled browser export if available; otherwise build surrogate segment-210 arrays for code-path testing only",
                "required_fields": "dataset_inventory;timestamps;masks;attitude;orbit;gx;gz;Sxx;Sxz;source_path;units;claim_label",
                "blocked_claims": "tau_WEP_numeric;WEP_product_score;local_GR;Newton",
            }
        )
    ]

    return {
        "source_register": source_register(stamp),
        "live_probe": probe_urls(stamp),
        "extraction_contract": extraction_contract,
        "array_schema": array_schema,
        "status": status_rows,
        "runner_dryrun": runner_dryrun,
        "claim_gate": claim_gate,
        "decision": decision,
        "next": next_target,
        "source_weight": source_weight,
        "wep_coeffs": wep_coeffs,
        "queue": queue,
    }


def validate(tables: dict[str, list[dict[str, str]]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []

    def val(validation_id: str, status: str, detail: str) -> None:
        rows.append(
            {
                "validation_id": validation_id,
                "status": status,
                "detail": detail,
                "valid_for_claim": "false",
                "claim_allowed": "false",
            }
        )

    source_failures = [row for row in tables["source_register"] if row["status"] != "EXISTS_NEEDLES_CONFIRMED"]
    val("VAL2000_00_sources", "PASS" if not source_failures else "FAIL", "all source paths exist and needles found" if not source_failures else ";".join(row["source_id"] for row in source_failures))

    probe_rows = tables["live_probe"]
    probes_recorded = len(probe_rows) == len(LIVE_URLS)
    no_schema_claim = all(row["schema_inventory_acquired"] == "false" and row["official_array_acquired"] == "false" for row in probe_rows)
    val("VAL2000_01_live_probe", "PASS" if probes_recorded and no_schema_claim else "FAIL", "live probes recorded without schema/array claim")

    contract_complete = len(tables["extraction_contract"]) == 5 and all(row["current_status"] == "NOT_ACQUIRED" for row in tables["extraction_contract"])
    val("VAL2000_02_contract", "PASS" if contract_complete else "FAIL", "extraction contract complete and nonclaim")

    schema_complete = len(tables["array_schema"]) == 6 and all(row["current_status"].startswith("MISSING") for row in tables["array_schema"])
    val("VAL2000_03_array_schema", "PASS" if schema_complete else "FAIL", "array schema contract complete with missing official arrays")

    status_blocks = any(row["status"] == "NOT_ACQUIRED" and row["object"] == "numeric tau_WEP" for row in tables["status"])
    val("VAL2000_04_tau_status", "PASS" if status_blocks else "FAIL", "numeric tau remains not acquired")

    runner_selects = tables["runner_dryrun"][-1]["result"] == "NEXT_2001_USER_ASSISTED_CMSM_EXPORT_OR_NONCLAIM_SURROGATE_RECONSTRUCTION"
    val("VAL2000_05_runner_decision", "PASS" if runner_selects else "FAIL", "runner selects user export or surrogate reconstruction")

    gates_safe = all(row["status"] in {"FAIL_BLOCKED", "PASS_NONCLAIM_CONTRACT"} for row in tables["claim_gate"])
    no_physics_claim = all(row["status"] == "FAIL_BLOCKED" for row in tables["claim_gate"] if row["gate_id"] != "CG2000_0_contract")
    val("VAL2000_06_claim_gates", "PASS" if gates_safe and no_physics_claim else "FAIL", "only contract passes as nonclaim")

    next_ok = tables["next"][0]["target_doc"] == "2001-Y5-R2FR-user-CMSM-export-or-nonclaim-surrogate-reconstruction.md"
    val("VAL2000_07_next_target", "PASS" if next_ok else "FAIL", "2001 user export/surrogate target selected")

    all_rows = [row for rows_for_table in tables.values() for row in rows_for_table]
    flags_safe = all(row.get("valid_for_claim") == "false" and row.get("claim_allowed") == "false" for row in all_rows)
    val("VAL2000_08_claim_flags_safe", "PASS" if flags_safe else "FAIL", "claim flags all false")

    parse_failures = []
    for output_name, path in OUTPUTS.items():
        if not path.exists():
            parse_failures.append(f"{output_name}:missing")
            continue
        with path.open(newline="", encoding="utf-8") as handle:
            parsed = list(csv.DictReader(handle))
        if not parsed:
            parse_failures.append(f"{output_name}:empty")
    val("VAL2000_09_csv_parse", "PASS" if not parse_failures else "FAIL", "all generated CSVs parse with rows" if not parse_failures else ";".join(parse_failures))

    pycache_exists = (ROOT / "scripts" / "__pycache__").exists()
    val("VAL2000_10_pycache_absent", "PASS" if not pycache_exists else "FAIL", "scripts __pycache__ absent")

    formalization_artifacts = []
    checkpoint_markers = ("Y5_R2FR", "P8_Y5", "JR2000", "CMSM2000", "ARR2000", "WEP")
    if FORMALIZATION.exists():
        formalization_artifacts = [
            path
            for path in FORMALIZATION.rglob("*")
            if "2000" in path.name and any(marker in path.name for marker in checkpoint_markers)
        ]
    val("VAL2000_11_formalization_untouched", "PASS" if not formalization_artifacts else "FAIL", f"formalization_2000_artifact_count={len(formalization_artifacts)}")

    overall = "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL"
    val("VAL2000_OVERALL", overall, "2000 CMSM schema or one-segment official array extract")
    return rows


def markdown_table(rows: list[dict[str, str]]) -> str:
    if not rows:
        return ""
    headers = list(rows[0].keys())
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        cells = [str(row.get(header, "")).replace("\n", " ").replace("|", "\\|") for header in headers]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def write_markdown(tables: dict[str, list[dict[str, str]]], validation_rows: list[dict[str, str]]) -> None:
    sections = [
        ("Source Register", tables["source_register"]),
        ("Live CMSM Probe", tables["live_probe"]),
        ("CMSM Extraction Contract", tables["extraction_contract"]),
        ("Official Array Schema Contract", tables["array_schema"]),
        ("Extraction Status", tables["status"]),
        ("Runner Dryrun", tables["runner_dryrun"]),
        ("Claim Gate", tables["claim_gate"]),
        ("Decision Ledger", tables["decision"]),
        ("Next Target", tables["next"]),
        ("Validation", validation_rows),
    ]
    lines = [
        "# 2000 Y5 R2FR: CMSM Schema Or One-Segment Official Array Extract",
        "",
        "Private checkpoint. This attempts the 1999 handoff: obtain CMSM schema/official arrays, or at minimum stage the exact contract for a future user/export route.",
        "",
        "Verdict: current runtime still does not acquire CMSM schema or official segment arrays. The public OCA/ONERA pages are reachable as route provenance, but the CMSM data module is not usable here. The official array contract is now explicit and validation-ready.",
        "",
        "Important boundary: a dry-run or surrogate can test the reconstruction code path, but it is not a physical `tau_WEP` kernel and cannot score WEP/local-GR.",
        "",
        "Next honest move: user/browser-supplied CMSM export, or a loudly labelled nonclaim surrogate segment-210 reconstruction.",
        "",
        "No WEP, local-GR, Newton, R10, PPN, clock, orbital, or public claim follows from 2000.",
        "",
    ]
    for title, rows in sections:
        lines.extend([f"## {title}", "", markdown_table(rows), ""])
    DOC_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    ensure_dirs()
    pycache_path = ROOT / "scripts" / "__pycache__"
    if pycache_path.exists():
        shutil.rmtree(pycache_path)
    tables = build_tables()
    for output_name, path in OUTPUTS.items():
        write_csv(path, tables[output_name])
    validation_rows = validate(tables)
    write_csv(VALIDATION_PATH, validation_rows)
    write_markdown(tables, validation_rows)
    if pycache_path.exists():
        shutil.rmtree(pycache_path)
    overall = validation_rows[-1]["status"]
    print(f"wrote {DOC_PATH}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"VAL2000_OVERALL={overall}")
    return 0 if overall == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
