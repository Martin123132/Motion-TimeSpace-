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

DOC_PATH = ROOT / "1998-Y5-R2FR-MICROSCOPE-eta-readout-formula-or-orbit-kernel-acquisition.md"
VALIDATION_PATH = MTS_RESIDUALS / "P8_Y5_BRR545_1998_VALIDATION.csv"

SOURCES = {
    "1997_doc": {
        "path": ROOT / "1997-Y5-R2FR-direct-WEP-product-theorem-or-first-real-tau-source-row.md",
        "needles": ["REQ1997_0_readout_formula", "NEXT1997_0_primary"],
    },
    "1997_validation": {
        "path": MTS_RESIDUALS / "P8_Y5_BRR545_1997_VALIDATION.csv",
        "needles": ["VAL1997_OVERALL", "PASS"],
    },
    "1070_eta_readout": {
        "path": ROOT / "1070-Y5-R10-MICROSCOPE-eta-readout-formula-or-orbit-kernel-acquisition.md",
        "needles": ["ETA1070_0_formula", "ORK1070_5_verdict", "V1070_SUMMARY"],
    },
    "1070_validation": {
        "path": MTS_RESIDUALS / "P8_Y5_BRR545_1070_VALIDATION.csv",
        "needles": ["V1070_SUMMARY", "pass"],
    },
    "1071_kernel": {
        "path": ROOT / "1071-Y5-R10-MICROSCOPE-full-orbit-kernel-or-source-worldtube-row.md",
        "needles": ["KER1071_6_verdict", "TAU1071_3_verdict", "NEXT1071_0_1072"],
    },
    "1071_validation": {
        "path": MTS_RESIDUALS / "P8_Y5_BRR545_1071_VALIDATION.csv",
        "needles": ["V1071_SUMMARY", "pass"],
    },
    "local_bounds": {
        "path": ROOT / "source-intake" / "local_bounds" / "local_bound_claims.csv",
        "needles": ["R1_WEP_source_charge", "2.8e-15"],
    },
}

OUTPUTS = {
    "source_register": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1998_SOURCE_REGISTER.csv",
    "eta_readout": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1998_ETA_READOUT_FORMULA_ROWS.csv",
    "kernel_skeleton": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1998_MICROSCOPE_KERNEL_SKELETON.csv",
    "tau_impact": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1998_TAU_IMPACT_LEDGER.csv",
    "runner_dryrun": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1998_RUNNER_DRYRUN.csv",
    "claim_gate": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1998_CLAIM_GATE.csv",
    "decision": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1998_DECISION_LEDGER.csv",
    "next": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1998_NEXT_TARGET.csv",
    "source_weight": SOURCE_WEIGHT_DOCS / "MICROSCOPE_ETA_KERNEL_1998_NONCLAIM.csv",
    "wep_coeffs": MICROSCOPE_COEFFS / "P8_Y5_PARENT_QLOC_1998_ETA_KERNEL_NONCLAIM.csv",
    "queue": RAB_QUEUE / "JR1998_MICROSCOPE_NUMERIC_KERNEL_OR_SOURCE_WORLDTUBE_QUEUE.csv",
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
                "needed_for": "1998 MICROSCOPE eta readout formula or orbit kernel acquisition",
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

    eta_readout = [
        row(
            {
                "eta_id": "ETA1998_0_formula",
                "formula_or_item": "eta_AB = 2(a_A-a_B)/(a_A+a_B)",
                "units": "dimensionless",
                "source_basis": "1070 ETA1070_0_formula; DOI 10.1088/1361-6382/ac84be",
                "status": "SOURCE_BACKED_FORMULA_FILLED",
                "MTS_impact": "observable normalization acquired; not a tau_WEP prediction",
            }
        ),
        row(
            {
                "eta_id": "ETA1998_1_delta_x_identification",
                "formula_or_item": "eta(Ti,Pt) is identified with measured delta_x in the MICROSCOPE convention",
                "units": "dimensionless",
                "source_basis": "1070 ETA1070_1_delta_x_identification",
                "status": "SOURCE_BACKED_READOUT_IDENTIFICATION_FILLED",
                "MTS_impact": "links eta observable to the instrument differential channel",
            }
        ),
        row(
            {
                "eta_id": "ETA1998_2_bound_context",
                "formula_or_item": "Ti/Pt eta upper-bound anchor 2.8e-15",
                "units": "dimensionless",
                "source_basis": "local_bound_claims.csv:R1_WEP_source_charge; DOI 10.1103/PhysRevLett.129.121102",
                "status": "SOURCE_BACKED_BOUND_CONTEXT_FILLED",
                "MTS_impact": "nonclaim comparator only; not an MTS prediction",
            }
        ),
        row(
            {
                "eta_id": "ETA1998_3_sign_pair_convention",
                "formula_or_item": "A/B sign convention is source-backed for eta_AB, but not mapped onto every MTS material-source basis sign",
                "units": "dimensionless",
                "source_basis": "1070 ETA1070_3_sign_pair_convention",
                "status": "PARTIAL_SIGN_CONTEXT_ONLY",
                "MTS_impact": "absolute-value bound can be used; signed model comparison still needs material/readout orientation",
            }
        ),
        row(
            {
                "eta_id": "ETA1998_4_verdict",
                "formula_or_item": "eta formula and delta_x readout are acquired; tau_WEP/direct product are not",
                "units": "dimensionless",
                "source_basis": "1070 V1070_SUMMARY",
                "status": "FORMULA_FILLED_NOT_TAU",
                "MTS_impact": "data plumbing improved; WEP/local-GR still blocked",
            }
        ),
    ]

    kernel_skeleton = [
        row(
            {
                "kernel_id": "KER1998_0_sampling_axis",
                "component": "sample/readout axis",
                "official_form": "4 Hz acceleration sampling; differential acceleration along sensitive X axis",
                "acquired_level": "SOURCE_BACKED_PARTIAL_READOUT_ROW",
                "needed_numeric_inputs": "full map from parent residual to X-axis eta channel",
            }
        ),
        row(
            {
                "kernel_id": "KER1998_1_segments_orbits",
                "component": "segment/orbit exposure",
                "official_form": "SUEP Pt/Ti 19 segments, 1362 orbits, 94 days; SUREF Pt/Pt 13 segments, 598 orbits, 41 days",
                "acquired_level": "SOURCE_BACKED_PARTIAL_ORBIT_ROW",
                "needed_numeric_inputs": "exact timestamps, masks, attitude/spin phase, and source line-of-sight kernel",
            }
        ),
        row(
            {
                "kernel_id": "KER1998_2_source_gravity_leg",
                "component": "Earth/source gravity proxy",
                "official_form": "g(Osat) and gravity-gradient tensor T computed at satellite centre",
                "acquired_level": "SOURCE_WORLDTUBE_PROXY_FORM_ACQUIRED_NOT_NUMERIC",
                "needed_numeric_inputs": "satellite position/velocity and gravity model used by MICROSCOPE processing",
            }
        ),
        row(
            {
                "kernel_id": "KER1998_3_segment_window",
                "component": "segment/window operator",
                "official_form": "selected continuous segments; even-orbit DFT-aligned windows; glitch masks",
                "acquired_level": "SOURCE_BACKED_SEGMENT_TABLE_ACQUIRED",
                "needed_numeric_inputs": "segment masks, removed-sample indices, exact timestamps",
            }
        ),
        row(
            {
                "kernel_id": "KER1998_4_verdict",
                "component": "tau_WEP kernel verdict",
                "official_form": "official kernel skeleton acquired, numeric orbit/attitude/source-worldtube kernel not reconstructed",
                "acquired_level": "KERNEL_SKELETON_YES_NUMERIC_TAU_NO",
                "needed_numeric_inputs": "data portal products or reproduced gx/gz/Sxx/Sxz arrays",
            }
        ),
    ]

    tau_impact = [
        row(
            {
                "impact_id": "TAI1998_0_formula_does_not_define_tau",
                "object": "eta_AB formula",
                "what_it_gives": "observable normalization and readout comparison convention",
                "what_is_missing": "source residual to eta projection functional",
                "claim_status": "NOT_TAU",
            }
        ),
        row(
            {
                "impact_id": "TAI1998_1_kernel_skeleton_not_numeric",
                "object": "official MICROSCOPE kernel skeleton",
                "what_it_gives": "fit/readout structure and segment-window shape",
                "what_is_missing": "numeric gx/gz/Sxx/Sxz arrays, exact masks, attitude/orbit kernel",
                "claim_status": "NOT_NUMERIC_TAU",
            }
        ),
        row(
            {
                "impact_id": "TAI1998_2_source_worldtube_proxy",
                "object": "g(Osat) and T source-gravity proxy form",
                "what_it_gives": "source leg structure",
                "what_is_missing": "Earth/source model values in MTS tau convention",
                "claim_status": "PROXY_FORM_ONLY",
            }
        ),
        row(
            {
                "impact_id": "TAI1998_3_no_unity_shortcut",
                "object": "eta formula plus kernel skeleton",
                "what_it_gives": "better acquisition target",
                "what_is_missing": "direct P_WEP product or numeric tau_WEP kernel",
                "claim_status": "UNITY_SHORTCUT_FORBIDDEN",
            }
        ),
    ]

    runner_dryrun = [
        row(
            {
                "run_id": "RUN1998_0_eta_formula",
                "check": "import official eta_AB formula and delta_x readout identification",
                "result": "PASS_NONCLAIM_FORMULA",
                "reason": "1070 source-backed rows are present and validated",
            }
        ),
        row(
            {
                "run_id": "RUN1998_1_kernel_skeleton",
                "check": "import official MICROSCOPE kernel skeleton",
                "result": "PASS_NONCLAIM_SKELETON",
                "reason": "1071 source-backed kernel skeleton and segment table are present and validated",
            }
        ),
        row(
            {
                "run_id": "RUN1998_2_numeric_tau",
                "check": "promote tau_WEP to numeric or theorem-zero",
                "result": "FAIL_NUMERIC_KERNEL_MISSING",
                "reason": "kernel skeleton lacks numeric arrays/timestamps/masks/source-worldtube values",
            }
        ),
        row(
            {
                "run_id": "RUN1998_3_product_score",
                "check": "score WEP product",
                "result": "FAIL_VALID_PREDICTION_ROWS_ZERO",
                "reason": "direct P_WEP product and tau split product remain missing",
            }
        ),
        row(
            {
                "run_id": "RUN1998_4_verdict",
                "check": "1998 next-step decision",
                "result": "NEXT_1999_MICROSCOPE_NUMERIC_KERNEL_OR_SOURCE_WORLDTUBE_ROW",
                "reason": "formula and skeleton are acquired; numeric tau/source-worldtube is next",
            }
        ),
    ]

    claim_gate = [
        row(
            {
                "gate_id": "CG1998_0_eta_formula",
                "claim": "eta formula/readout convention is acquired",
                "status": "PASS_NONCLAIM_FORMULA",
                "reason": "source-backed observable definition, not an MTS prediction",
            }
        ),
        row(
            {
                "gate_id": "CG1998_1_kernel_skeleton",
                "claim": "official MICROSCOPE kernel skeleton is acquired",
                "status": "PASS_NONCLAIM_SKELETON",
                "reason": "kernel form and segment metadata exist, but no numeric tau",
            }
        ),
        row(
            {
                "gate_id": "CG1998_2_numeric_tau",
                "claim": "tau_WEP is numeric/theorem-zero",
                "status": "FAIL_BLOCKED",
                "reason": "full numeric kernel/source-worldtube missing",
            }
        ),
        row(
            {
                "gate_id": "CG1998_3_WEP_product",
                "claim": "WEP product can be scored",
                "status": "FAIL_BLOCKED",
                "reason": "valid_prediction_rows remains zero",
            }
        ),
        row(
            {
                "gate_id": "CG1998_4_local_GR",
                "claim": "local GR/WEP branch is derived",
                "status": "FAIL_BLOCKED",
                "reason": "eta/kernel acquisition is plumbing, not a parent product theorem",
            }
        ),
    ]

    decision = [
        row(
            {
                "decision_id": "DEC1998_0_readout_status",
                "decision": "ETA_FORMULA_AND_DELTA_X_READOUT_ARE_SOURCE_BACKED",
                "because": "1070 acquired the official formula and readout identification",
                "next_action": "use these rows as readout plumbing only",
            }
        ),
        row(
            {
                "decision_id": "DEC1998_1_kernel_status",
                "decision": "KERNEL_SKELETON_ACQUIRED_BUT_NUMERIC_TAU_MISSING",
                "because": "1071 acquired official fit/kernel structure and segments but not gx/gz/Sxx/Sxz arrays or masks",
                "next_action": "target data portal schema/products or reconstruct a single segment kernel",
            }
        ),
        row(
            {
                "decision_id": "DEC1998_2_best_next",
                "decision": "NUMERIC_KERNEL_OR_SOURCE_WORLDTUBE_ROW_NEXT",
                "because": "formula and skeleton are no longer the first blockers; numeric tau projection is",
                "next_action": "1999-Y5-R2FR-MICROSCOPE-numeric-kernel-or-source-worldtube-row.md",
            }
        ),
    ]

    next_target = [
        row(
            {
                "next_id": "NEXT1998_0_primary",
                "selection_status": "selected",
                "target_doc": "1999-Y5-R2FR-MICROSCOPE-numeric-kernel-or-source-worldtube-row.md",
                "target_script": "scripts/Y5_R2FR_MICROSCOPE_numeric_kernel_or_source_worldtube_row_1999.py",
                "task": "turn the kernel skeleton into a numeric tau_WEP component by acquiring CMSM data schema/products or reconstructing gx,gz,Sxx,Sxz for one SUEP segment; fallback to a source-backed Earth/source-worldtube row",
                "success_condition": "numeric kernel component or source-worldtube row with source path, units, schema/provenance, and refusal gates; no WEP/local-GR scoring yet",
                "do_not": "do not set tau_WEP=1, guess phase/masks, claim WEP/local-GR, absorb relative weights into measured G, push GitHub, or edit formalization-workbench",
            }
        )
    ]

    source_weight = [
        row(
            {
                "artifact_id": "SW1998_0_eta_kernel",
                "artifact_type": "MICROSCOPE_eta_kernel_nonclaim",
                "status": "FORMULA_AND_KERNEL_SKELETON_ACQUIRED_NUMERIC_TAU_MISSING",
                "source_path": str(DOC_PATH),
                "next_target": "1999-Y5-R2FR-MICROSCOPE-numeric-kernel-or-source-worldtube-row.md",
            }
        )
    ]

    wep_coeffs = [
        row(
            {
                "coefficient_id": "WEP1998_0_eta_kernel_contract",
                "quantity": "eta_AB formula and MICROSCOPE kernel skeleton",
                "required_formula": "P_WEP direct parent product or numeric tau_WEP kernel",
                "required_evidence": "numeric gx/gz/Sxx/Sxz arrays, masks/timestamps, source worldtube, material tensor, Xhat normalization",
                "current_status": "FORMULA_AND_SKELETON_ONLY",
                "status": "NONCLAIM_PLUMBING_ONLY",
            }
        )
    ]

    queue = [
        row(
            {
                "queue_id": "JR1998_0_numeric_kernel_or_worldtube",
                "priority": "1",
                "needed_input": "numeric MICROSCOPE kernel component or source-worldtube row",
                "route": "probe/acquire CMSM data schema/products or reconstruct one SUEP segment gx,gz,Sxx,Sxz from sourced orbit/attitude/gravity inputs",
                "required_fields": "data_schema;timestamps;masks;gx;gz;Sxx;Sxz;source_worldtube;units;source_path",
                "blocked_claims": "tau_WEP_numeric;WEP_product_score;local_GR;Newton",
            }
        )
    ]

    return {
        "source_register": source_register(stamp),
        "eta_readout": eta_readout,
        "kernel_skeleton": kernel_skeleton,
        "tau_impact": tau_impact,
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
    val("VAL1998_00_sources", "PASS" if not source_failures else "FAIL", "all source paths exist and needles found" if not source_failures else ";".join(row["source_id"] for row in source_failures))

    eta_formula = any(row["eta_id"] == "ETA1998_0_formula" and row["status"] == "SOURCE_BACKED_FORMULA_FILLED" for row in tables["eta_readout"])
    eta_not_tau = any(row["eta_id"] == "ETA1998_4_verdict" and row["status"] == "FORMULA_FILLED_NOT_TAU" for row in tables["eta_readout"])
    val("VAL1998_01_eta_readout", "PASS" if eta_formula and eta_not_tau else "FAIL", "eta formula acquired and not promoted to tau")

    skeleton = any(row["kernel_id"] == "KER1998_4_verdict" and row["acquired_level"] == "KERNEL_SKELETON_YES_NUMERIC_TAU_NO" for row in tables["kernel_skeleton"])
    val("VAL1998_02_kernel_skeleton", "PASS" if skeleton else "FAIL", "kernel skeleton acquired but numeric tau missing")

    tau_blocked = all(row["claim_status"] in {"NOT_TAU", "NOT_NUMERIC_TAU", "PROXY_FORM_ONLY", "UNITY_SHORTCUT_FORBIDDEN"} for row in tables["tau_impact"])
    val("VAL1998_03_tau_impact", "PASS" if tau_blocked else "FAIL", "tau impact ledger blocks shortcuts")

    runner_selects = tables["runner_dryrun"][-1]["result"] == "NEXT_1999_MICROSCOPE_NUMERIC_KERNEL_OR_SOURCE_WORLDTUBE_ROW"
    val("VAL1998_04_runner_decision", "PASS" if runner_selects else "FAIL", "runner selects numeric kernel/source-worldtube target")

    gates_safe = all(row["status"] in {"FAIL_BLOCKED", "PASS_NONCLAIM_FORMULA", "PASS_NONCLAIM_SKELETON"} for row in tables["claim_gate"])
    no_physics_claim = all(row["status"] == "FAIL_BLOCKED" for row in tables["claim_gate"] if row["gate_id"] not in {"CG1998_0_eta_formula", "CG1998_1_kernel_skeleton"})
    val("VAL1998_05_claim_gates", "PASS" if gates_safe and no_physics_claim else "FAIL", "formula/skeleton pass only as nonclaim plumbing")

    next_ok = tables["next"][0]["target_doc"] == "1999-Y5-R2FR-MICROSCOPE-numeric-kernel-or-source-worldtube-row.md"
    val("VAL1998_06_next_target", "PASS" if next_ok else "FAIL", "1999 numeric kernel/source-worldtube target selected")

    all_rows = [row for rows_for_table in tables.values() for row in rows_for_table]
    flags_safe = all(row.get("valid_for_claim") == "false" and row.get("claim_allowed") == "false" for row in all_rows)
    val("VAL1998_07_claim_flags_safe", "PASS" if flags_safe else "FAIL", "claim flags all false")

    parse_failures = []
    for output_name, path in OUTPUTS.items():
        if not path.exists():
            parse_failures.append(f"{output_name}:missing")
            continue
        with path.open(newline="", encoding="utf-8") as handle:
            parsed = list(csv.DictReader(handle))
        if not parsed:
            parse_failures.append(f"{output_name}:empty")
    val("VAL1998_08_csv_parse", "PASS" if not parse_failures else "FAIL", "all generated CSVs parse with rows" if not parse_failures else ";".join(parse_failures))

    pycache_exists = (ROOT / "scripts" / "__pycache__").exists()
    val("VAL1998_09_pycache_absent", "PASS" if not pycache_exists else "FAIL", "scripts __pycache__ absent")

    formalization_artifacts = []
    checkpoint_markers = ("Y5_R2FR", "P8_Y5", "JR1998", "ETA1998", "KER1998", "WEP")
    if FORMALIZATION.exists():
        formalization_artifacts = [
            path
            for path in FORMALIZATION.rglob("*")
            if "1998" in path.name and any(marker in path.name for marker in checkpoint_markers)
        ]
    val("VAL1998_10_formalization_untouched", "PASS" if not formalization_artifacts else "FAIL", f"formalization_1998_artifact_count={len(formalization_artifacts)}")

    overall = "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL"
    val("VAL1998_OVERALL", overall, "1998 MICROSCOPE eta formula and kernel skeleton acquisition")
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
        ("Eta Readout Formula Rows", tables["eta_readout"]),
        ("MICROSCOPE Kernel Skeleton", tables["kernel_skeleton"]),
        ("Tau Impact Ledger", tables["tau_impact"]),
        ("Runner Dryrun", tables["runner_dryrun"]),
        ("Claim Gate", tables["claim_gate"]),
        ("Decision Ledger", tables["decision"]),
        ("Next Target", tables["next"]),
        ("Validation", validation_rows),
    ]
    lines = [
        "# 1998 Y5 R2FR: MICROSCOPE Eta Readout Formula Or Orbit-Kernel Acquisition",
        "",
        "Private checkpoint. This folds the 1070/1071 MICROSCOPE readout work into the current WEP/direct-product branch.",
        "",
        "Verdict: the official `eta_AB` formula and delta-x readout identification are source-backed, and the official MICROSCOPE kernel skeleton is acquired. This is real plumbing progress, not a WEP prediction.",
        "",
        "Still missing: numeric `tau_WEP`. The branch needs machine-readable or reconstructed `gx/gz/Sxx/Sxz` arrays, exact masks/timestamps, source-worldtube values, material tensor, and `Xhat` normalization before any product score.",
        "",
        "Next honest move: numeric kernel component or source-worldtube row, not another symbolic shortcut.",
        "",
        "No WEP, local-GR, Newton, R10, PPN, clock, orbital, or public claim follows from 1998.",
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
    print(f"VAL1998_OVERALL={overall}")
    return 0 if overall == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
