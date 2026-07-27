from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


BRANCH = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FORMALIZATION = REPO / "formalization-workbench"
MTS_RESIDUALS = ROOT / "source-intake" / "mts_residuals"
SOURCE_WEIGHT_DOCS = ROOT / "source-intake" / "source-weight" / "docs"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICROSCOPE_COEFFS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "coefficients"

DOC_PATH = ROOT / "1999-Y5-R2FR-MICROSCOPE-numeric-kernel-or-source-worldtube-row.md"
VALIDATION_PATH = MTS_RESIDUALS / "P8_Y5_BRR545_1999_VALIDATION.csv"

SOURCES = {
    "1998_doc": {
        "path": ROOT / "1998-Y5-R2FR-MICROSCOPE-eta-readout-formula-or-orbit-kernel-acquisition.md",
        "needles": ["KER1998_4_verdict", "NEXT1998_0_primary"],
    },
    "1998_validation": {
        "path": MTS_RESIDUALS / "P8_Y5_BRR545_1998_VALIDATION.csv",
        "needles": ["VAL1998_OVERALL", "PASS"],
    },
    "1072_numeric_kernel": {
        "path": ROOT / "1072-Y5-R10-MICROSCOPE-data-portal-schema-or-reconstructed-gxS-kernel.md",
        "needles": ["DRY1072_0_segment210_kernel_preview", "NTS1072_2_tau_WEP", "NEXT1072_0_1073"],
    },
    "1072_validation": {
        "path": MTS_RESIDUALS / "P8_Y5_BRR545_1072_VALIDATION.csv",
        "needles": ["V1072_SUMMARY", "pass"],
    },
    "1071_kernel": {
        "path": ROOT / "1071-Y5-R10-MICROSCOPE-full-orbit-kernel-or-source-worldtube-row.md",
        "needles": ["KER1071_6_verdict", "TAU1071_3_verdict"],
    },
}

OUTPUTS = {
    "source_register": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1999_SOURCE_REGISTER.csv",
    "portal_route": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1999_CMSM_PORTAL_ROUTE.csv",
    "numeric_requirements": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1999_NUMERIC_KERNEL_REQUIREMENTS.csv",
    "dry_run": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1999_SEGMENT210_DRY_RUN_LEDGER.csv",
    "tau_status": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1999_TAU_STATUS.csv",
    "runner_dryrun": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1999_RUNNER_DRYRUN.csv",
    "claim_gate": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1999_CLAIM_GATE.csv",
    "decision": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1999_DECISION_LEDGER.csv",
    "next": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1999_NEXT_TARGET.csv",
    "source_weight": SOURCE_WEIGHT_DOCS / "MICROSCOPE_NUMERIC_KERNEL_1999_NONCLAIM.csv",
    "wep_coeffs": MICROSCOPE_COEFFS / "P8_Y5_PARENT_QLOC_1999_NUMERIC_KERNEL_NONCLAIM.csv",
    "queue": RAB_QUEUE / "JR1999_CMSM_SCHEMA_OR_ONE_SEGMENT_ARRAY_QUEUE.csv",
}


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
                "needed_for": "1999 MICROSCOPE numeric kernel or source worldtube row",
                "needles": ";".join(spec["needles"]),
                "exists": str(exists),
                "anchor_found": str(exists and not missing),
                "missing_needles": ";".join(missing),
                "status": "EXISTS_NEEDLES_CONFIRMED" if exists and not missing else "MISSING_SOURCE_OR_ANCHOR",
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

    portal_route = [
        row(
            {
                "route_id": "CMSM1999_0_data_inventory_pointer",
                "source": "OCA/MICROSCOPE CMSM REGARDS route",
                "what_it_provides": "source-backed pointer to raw/calibrated/auxiliary MICROSCOPE data products",
                "current_status": "ROUTE_STAGED_SCHEMA_NOT_ACQUIRED",
                "needed_next": "browser/manual CMSM session or public REGARDS query with actual file/schema inventory",
            }
        ),
        row(
            {
                "route_id": "CMSM1999_1_REGARDS_api_candidate",
                "source": "REGARDS OpenSearch/GeoJSON/STAC candidate route",
                "what_it_provides": "possible API/search/download pattern",
                "current_status": "CANDIDATE_ENDPOINTS_STAGED",
                "needed_next": "working query parameters or UI-derived dataset/file names",
            }
        ),
        row(
            {
                "route_id": "CMSM1999_2_CQG_product_requirements",
                "source": "CQG 2022 data product description",
                "what_it_provides": "4 Hz accelerometer measurements, same-stamp attitude/angular rates, minute position/velocity requirements",
                "current_status": "REQUIREMENTS_RECORDED",
                "needed_next": "actual arrays or source-reconstructed official-equivalent inputs",
            }
        ),
    ]

    numeric_requirements = [
        row(
            {
                "requirement_id": "NKR1999_0_exact_time_grid",
                "required_input": "exact segment timestamps and sample masks",
                "why_required": "phase of gx/gz/Sxx/Sxz depends on actual timestamps and removed samples",
                "current_status": "MISSING_EXACT_TIMESTAMPS_AND_MASKS",
                "source_route": "CMSM 4 Hz accelerometer products or processing metadata",
            }
        ),
        row(
            {
                "requirement_id": "NKR1999_1_orbit_ephemeris",
                "required_input": "J2000 satellite position/velocity",
                "why_required": "compute g(Osat) and gravity-gradient tensor T at satellite centre",
                "current_status": "MISSING_NUMERIC_EPHEMERIS",
                "source_route": "CMSM minute-sampled orbit products",
            }
        ),
        row(
            {
                "requirement_id": "NKR1999_2_attitude_rates",
                "required_input": "attitude, angular velocity, angular acceleration",
                "why_required": "rotate gravity into instrument frame and build inertia-gradient correction",
                "current_status": "MISSING_NUMERIC_ATTITUDE_RATES",
                "source_route": "CMSM same-stamp attitude products",
            }
        ),
        row(
            {
                "requirement_id": "NKR1999_3_gravity_model",
                "required_input": "official gravity model convention or approved surrogate with error bound",
                "why_required": "do not substitute guessed spherical model for claim-grade kernel",
                "current_status": "MISSING_OFFICIAL_GRAVITY_MODEL_OR_SURROGATE",
                "source_route": "MICROSCOPE processing references and auxiliary products",
            }
        ),
        row(
            {
                "requirement_id": "NKR1999_4_output_arrays",
                "required_input": "gx, gz, Sxx, Sxz arrays for at least one SUEP pilot segment",
                "why_required": "first numeric tau_WEP projection component",
                "current_status": "MISSING_OFFICIAL_NUMERIC_ARRAYS",
                "source_route": "CMSM products or reproducible reconstruction",
            }
        ),
    ]

    dry_run = [
        row(
            {
                "dry_run_id": "DRY1999_0_segment210_kernel_preview",
                "segment": "210",
                "spin_mode": "V3",
                "full_grid_samples": "1189200",
                "preview_rows_written": "32",
                "phase_convention": "dry_run_zero_phase_not_claim",
                "kernel_status": "DRY_RUN_NUMERIC_PREVIEW_ONLY_NOT_TAU",
            }
        ),
        row(
            {
                "dry_run_id": "DRY1999_1_reconstruction_path",
                "segment": "210",
                "spin_mode": "V3",
                "full_grid_samples": "1189200",
                "preview_rows_written": "32",
                "phase_convention": "replace_with_official_phase_and_amplitude_before_scoring",
                "kernel_status": "CODE_PATH_EXERCISED_OFFICIAL_ARRAYS_MISSING",
            }
        ),
    ]

    tau_status = [
        row(
            {
                "status_id": "NTS1999_0_schema_inventory",
                "object": "CMSM schema/file inventory",
                "status": "NOT_ACQUIRED_FROM_LOCAL_PROBE",
                "remaining_gap": "use browser/manual session or discover public API query parameters",
            }
        ),
        row(
            {
                "status_id": "NTS1999_1_dry_run_preview",
                "object": "segment 210 gx/gz/Sxx/Sxz preview",
                "status": "DRY_RUN_NUMERIC_PREVIEW_ONLY",
                "remaining_gap": "replace zero-phase/unit-amplitude columns with official arrays",
            }
        ),
        row(
            {
                "status_id": "NTS1999_2_tau_WEP",
                "object": "numeric tau_WEP",
                "status": "NOT_ACQUIRED",
                "remaining_gap": "official numeric kernel arrays or source-reconstructed arrays with provenance",
            }
        ),
        row(
            {
                "status_id": "NTS1999_3_source_worldtube",
                "object": "Earth/source-worldtube row",
                "status": "NOT_ACQUIRED",
                "remaining_gap": "source profile/composition convention or calibrated point-source theorem with error bound",
            }
        ),
    ]

    runner_dryrun = [
        row(
            {
                "run_id": "RUN1999_0_portal_route",
                "check": "import CMSM/REGARDS route and requirements",
                "result": "PASS_NONCLAIM_ROUTE",
                "reason": "route and candidate endpoints are staged, but schema/products are not acquired",
            }
        ),
        row(
            {
                "run_id": "RUN1999_1_dry_run_preview",
                "check": "import segment-210 dry-run gx/gz/Sxx/Sxz preview",
                "result": "PASS_NONCLAIM_DRY_RUN",
                "reason": "preview exercises reconstruction path only; zero-phase/unit amplitude is not physical tau",
            }
        ),
        row(
            {
                "run_id": "RUN1999_2_numeric_tau",
                "check": "promote numeric tau_WEP",
                "result": "FAIL_OFFICIAL_ARRAYS_MISSING",
                "reason": "exact timestamps/masks, ephemeris, attitude, gravity model, and official arrays are missing",
            }
        ),
        row(
            {
                "run_id": "RUN1999_3_product_score",
                "check": "score WEP product",
                "result": "FAIL_VALID_PREDICTION_ROWS_ZERO",
                "reason": "dry-run kernel is not a prediction and tau_WEP remains missing",
            }
        ),
        row(
            {
                "run_id": "RUN1999_4_verdict",
                "check": "1999 next-step decision",
                "result": "NEXT_2000_CMSM_SCHEMA_OR_ONE_SEGMENT_OFFICIAL_ARRAY_EXTRACT",
                "reason": "the next real move is CMSM UI/API schema capture or one official/reconstructed segment array",
            }
        ),
    ]

    claim_gate = [
        row(
            {
                "gate_id": "CG1999_0_portal_route",
                "claim": "CMSM/REGARDS route is staged",
                "status": "PASS_NONCLAIM_ROUTE",
                "reason": "source-backed route exists but file inventory not acquired",
            }
        ),
        row(
            {
                "gate_id": "CG1999_1_dry_run_preview",
                "claim": "dry-run kernel preview exists",
                "status": "PASS_NONCLAIM_DRY_RUN",
                "reason": "code path preview only; not physical tau",
            }
        ),
        row(
            {
                "gate_id": "CG1999_2_official_numeric_kernel",
                "claim": "official numeric gx/gz/Sxx/Sxz kernel is acquired",
                "status": "FAIL_BLOCKED",
                "reason": "official arrays/schema not acquired",
            }
        ),
        row(
            {
                "gate_id": "CG1999_3_tau_WEP",
                "claim": "tau_WEP is numeric",
                "status": "FAIL_BLOCKED",
                "reason": "dry-run preview is not tau_WEP",
            }
        ),
        row(
            {
                "gate_id": "CG1999_4_local_GR",
                "claim": "WEP/local-GR branch is scored",
                "status": "FAIL_BLOCKED",
                "reason": "valid prediction rows remain zero",
            }
        ),
    ]

    decision = [
        row(
            {
                "decision_id": "DEC1999_0_status",
                "decision": "PORTAL_ROUTE_AND_DRY_RUN_EXIST_BUT_NUMERIC_TAU_DOES_NOT",
                "because": "1072 records CMSM/REGARDS route and dry-run preview, but official arrays/schema are not acquired",
                "next_action": "capture CMSM schema/products or one official/reconstructed segment",
            }
        ),
        row(
            {
                "decision_id": "DEC1999_1_dry_run_policy",
                "decision": "DRY_RUN_IS_RECONSTRUCTION_PATH_NOT_EVIDENCE",
                "because": "zero-phase/unit-amplitude preview lacks timestamps, masks, ephemeris, attitude, and gravity model",
                "next_action": "replace dry-run columns with official/source-reconstructed arrays before tau scoring",
            }
        ),
        row(
            {
                "decision_id": "DEC1999_2_best_next",
                "decision": "CMSM_SCHEMA_OR_ONE_SEGMENT_OFFICIAL_ARRAY_EXTRACT",
                "because": "that is the first step capable of turning kernel skeleton into numeric tau_WEP",
                "next_action": "2000-Y5-R2FR-CMSM-schema-or-one-segment-official-array-extract.md",
            }
        ),
    ]

    next_target = [
        row(
            {
                "next_id": "NEXT1999_0_primary",
                "selection_status": "selected",
                "target_doc": "2000-Y5-R2FR-CMSM-schema-or-one-segment-official-array-extract.md",
                "target_script": "scripts/Y5_R2FR_CMSM_schema_or_one_segment_official_array_extract_2000.py",
                "task": "use a browser/manual CMSM session or discovered public REGARDS query to obtain MICROSCOPE file/schema inventory, then replace segment-210 dry-run gx/gz/Sxx/Sxz with official or source-reconstructed arrays for one pilot segment",
                "success_condition": "schema/file inventory or one segment official/source-reconstructed array row with timestamps/masks/provenance; still no WEP/local-GR claim",
                "do_not": "do not use zero-phase dry-run as evidence, guess masks/amplitudes, set tau_WEP=1, claim WEP/local-GR, push GitHub, or edit formalization-workbench",
            }
        )
    ]

    source_weight = [
        row(
            {
                "artifact_id": "SW1999_0_numeric_kernel",
                "artifact_type": "MICROSCOPE_numeric_kernel_nonclaim",
                "status": "PORTAL_ROUTE_AND_DRY_RUN_READY_OFFICIAL_NUMERIC_TAU_MISSING",
                "source_path": str(DOC_PATH),
                "next_target": "2000-Y5-R2FR-CMSM-schema-or-one-segment-official-array-extract.md",
            }
        )
    ]

    wep_coeffs = [
        row(
            {
                "coefficient_id": "WEP1999_0_numeric_kernel_requirements",
                "quantity": "gx/gz/Sxx/Sxz numeric tau_WEP kernel component",
                "required_formula": "numeric tau_WEP projection or direct P_WEP product",
                "required_evidence": "schema/products, exact timestamps/masks, ephemeris, attitude, gravity model, source-worldtube values, units",
                "current_status": "DRY_RUN_ONLY_OFFICIAL_ARRAYS_MISSING",
                "status": "NONCLAIM_REQUIREMENTS_ONLY",
            }
        )
    ]

    queue = [
        row(
            {
                "queue_id": "JR1999_0_CMSM_schema_or_segment",
                "priority": "1",
                "needed_input": "CMSM schema/file inventory or one segment official/source-reconstructed gx/gz/Sxx/Sxz array",
                "route": "browser/manual CMSM session, REGARDS API discovery, or sourced reconstruction for segment 210",
                "required_fields": "dataset_names;schema_columns;timestamps;masks;gx;gz;Sxx;Sxz;source_path;units;provenance",
                "blocked_claims": "tau_WEP_numeric;WEP_product_score;local_GR;Newton",
            }
        )
    ]

    return {
        "source_register": source_register(stamp),
        "portal_route": portal_route,
        "numeric_requirements": numeric_requirements,
        "dry_run": dry_run,
        "tau_status": tau_status,
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
    val("VAL1999_00_sources", "PASS" if not source_failures else "FAIL", "all source paths exist and needles found" if not source_failures else ";".join(row["source_id"] for row in source_failures))

    route_staged = any(row["route_id"] == "CMSM1999_0_data_inventory_pointer" and row["current_status"] == "ROUTE_STAGED_SCHEMA_NOT_ACQUIRED" for row in tables["portal_route"])
    val("VAL1999_01_portal_route", "PASS" if route_staged else "FAIL", "CMSM route staged without claiming schema")

    reqs_missing = all(row["current_status"].startswith("MISSING") for row in tables["numeric_requirements"])
    val("VAL1999_02_numeric_requirements", "PASS" if reqs_missing else "FAIL", "numeric kernel requirements remain explicit")

    dry_nonclaim = all("NOT_TAU" in row["kernel_status"] or "OFFICIAL_ARRAYS_MISSING" in row["kernel_status"] for row in tables["dry_run"])
    val("VAL1999_03_dry_run", "PASS" if dry_nonclaim else "FAIL", "dry-run kernel preview remains nonclaim")

    tau_missing = any(row["status"] == "NOT_ACQUIRED" and row["object"] == "numeric tau_WEP" for row in tables["tau_status"])
    val("VAL1999_04_tau_status", "PASS" if tau_missing else "FAIL", "numeric tau_WEP remains not acquired")

    runner_selects = tables["runner_dryrun"][-1]["result"] == "NEXT_2000_CMSM_SCHEMA_OR_ONE_SEGMENT_OFFICIAL_ARRAY_EXTRACT"
    val("VAL1999_05_runner_decision", "PASS" if runner_selects else "FAIL", "runner selects CMSM schema/one-segment extract")

    gates_safe = all(row["status"] in {"FAIL_BLOCKED", "PASS_NONCLAIM_ROUTE", "PASS_NONCLAIM_DRY_RUN"} for row in tables["claim_gate"])
    no_physics_claim = all(row["status"] == "FAIL_BLOCKED" for row in tables["claim_gate"] if row["gate_id"] not in {"CG1999_0_portal_route", "CG1999_1_dry_run_preview"})
    val("VAL1999_06_claim_gates", "PASS" if gates_safe and no_physics_claim else "FAIL", "only route/dry-run pass as nonclaim")

    next_ok = tables["next"][0]["target_doc"] == "2000-Y5-R2FR-CMSM-schema-or-one-segment-official-array-extract.md"
    val("VAL1999_07_next_target", "PASS" if next_ok else "FAIL", "2000 CMSM schema/segment target selected")

    all_rows = [row for rows_for_table in tables.values() for row in rows_for_table]
    flags_safe = all(row.get("valid_for_claim") == "false" and row.get("claim_allowed") == "false" for row in all_rows)
    val("VAL1999_08_claim_flags_safe", "PASS" if flags_safe else "FAIL", "claim flags all false")

    parse_failures = []
    for output_name, path in OUTPUTS.items():
        if not path.exists():
            parse_failures.append(f"{output_name}:missing")
            continue
        with path.open(newline="", encoding="utf-8") as handle:
            parsed = list(csv.DictReader(handle))
        if not parsed:
            parse_failures.append(f"{output_name}:empty")
    val("VAL1999_09_csv_parse", "PASS" if not parse_failures else "FAIL", "all generated CSVs parse with rows" if not parse_failures else ";".join(parse_failures))

    pycache_exists = (ROOT / "scripts" / "__pycache__").exists()
    val("VAL1999_10_pycache_absent", "PASS" if not pycache_exists else "FAIL", "scripts __pycache__ absent")

    formalization_artifacts = []
    checkpoint_markers = ("Y5_R2FR", "P8_Y5", "JR1999", "CMSM1999", "NKR1999", "WEP")
    if FORMALIZATION.exists():
        formalization_artifacts = [
            path
            for path in FORMALIZATION.rglob("*")
            if "1999" in path.name and any(marker in path.name for marker in checkpoint_markers)
        ]
    val("VAL1999_11_formalization_untouched", "PASS" if not formalization_artifacts else "FAIL", f"formalization_1999_artifact_count={len(formalization_artifacts)}")

    overall = "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL"
    val("VAL1999_OVERALL", overall, "1999 MICROSCOPE numeric kernel or source worldtube row")
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
        ("CMSM Portal Route", tables["portal_route"]),
        ("Numeric Kernel Requirements", tables["numeric_requirements"]),
        ("Segment 210 Dry-Run Ledger", tables["dry_run"]),
        ("Tau Status", tables["tau_status"]),
        ("Runner Dryrun", tables["runner_dryrun"]),
        ("Claim Gate", tables["claim_gate"]),
        ("Decision Ledger", tables["decision"]),
        ("Next Target", tables["next"]),
        ("Validation", validation_rows),
    ]
    lines = [
        "# 1999 Y5 R2FR: MICROSCOPE Numeric Kernel Or Source-Worldtube Row",
        "",
        "Private checkpoint. This imports the 1072 CMSM/REGARDS route and segment-210 dry-run into the current WEP/direct-product branch.",
        "",
        "Verdict: the CMSM data route and reconstruction path are staged, but no official numeric `tau_WEP` kernel is acquired. The segment-210 `gx/gz/Sxx/Sxz` preview is a dry-run only, not evidence.",
        "",
        "Still missing: CMSM schema/file inventory, exact timestamps/masks, orbit ephemeris, attitude/rates, official gravity model or approved surrogate, and official/source-reconstructed numeric arrays.",
        "",
        "Next honest move: CMSM schema capture or one pilot segment official/source-reconstructed array extract.",
        "",
        "No WEP, local-GR, Newton, R10, PPN, clock, orbital, or public claim follows from 1999.",
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
    print(f"VAL1999_OVERALL={overall}")
    return 0 if overall == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
