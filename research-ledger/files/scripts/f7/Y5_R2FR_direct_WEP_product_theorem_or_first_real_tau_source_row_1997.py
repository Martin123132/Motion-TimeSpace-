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

DOC_PATH = ROOT / "1997-Y5-R2FR-direct-WEP-product-theorem-or-first-real-tau-source-row.md"
VALIDATION_PATH = MTS_RESIDUALS / "P8_Y5_BRR545_1997_VALIDATION.csv"

SOURCES = {
    "1996_doc": {
        "path": ROOT / "1996-Y5-R2FR-parent-action-scale-normalization-or-WEP-tau-projection.md",
        "needles": ["DWP1996_0_preferred_direct_theorem", "NEXT1996_0_primary"],
    },
    "1996_validation": {
        "path": MTS_RESIDUALS / "P8_Y5_BRR545_1996_VALIDATION.csv",
        "needles": ["VAL1996_OVERALL", "PASS"],
    },
    "1069_direct_wep": {
        "path": ROOT / "1069-Y5-R10-direct-WEP-product-theorem-or-first-real-tau-source-row.md",
        "needles": ["DWT1069_5_verdict", "WTS1069_0_MICROSCOPE_eta_source_charge_proxy"],
    },
    "1069_validation": {
        "path": MTS_RESIDUALS / "P8_Y5_BRR545_1069_VALIDATION.csv",
        "needles": ["V1069_SUMMARY", "pass"],
    },
    "1068_tau_pack": {
        "path": ROOT / "1068-Y5-R10-WEP-tau-source-worldtube-orbit-readout-acquisition-pack.md",
        "needles": ["TAP1068_2_eta_readout", "DEC1068_2_best_next"],
    },
    "local_bounds": {
        "path": ROOT / "source-intake" / "local_bounds" / "local_bound_claims.csv",
        "needles": ["R1_WEP_source_charge", "2.8e-15"],
    },
}

OUTPUTS = {
    "source_register": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1997_SOURCE_REGISTER.csv",
    "direct_theorem": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1997_DIRECT_WEP_PRODUCT_THEOREM_ATTEMPT.csv",
    "readout_provenance": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1997_MICROSCOPE_READOUT_PROVENANCE.csv",
    "remaining_requirements": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1997_TAU_REMAINING_REQUIREMENTS.csv",
    "runner_dryrun": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1997_RUNNER_DRYRUN.csv",
    "claim_gate": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1997_CLAIM_GATE.csv",
    "decision": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1997_DECISION_LEDGER.csv",
    "next": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1997_NEXT_TARGET.csv",
    "source_weight": SOURCE_WEIGHT_DOCS / "DIRECT_WEP_PRODUCT_1997_NONCLAIM.csv",
    "wep_coeffs": MICROSCOPE_COEFFS / "P8_Y5_PARENT_QLOC_1997_MICROSCOPE_READOUT_PROVENANCE_NONCLAIM.csv",
    "queue": RAB_QUEUE / "JR1997_MICROSCOPE_ETA_OR_ORBIT_QUEUE.csv",
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
                "needed_for": "1997 direct WEP product theorem or first real tau source row",
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

    direct_theorem = [
        row(
            {
                "theorem_id": "DWT1997_0_target",
                "statement": "Derive P_WEP_relative_source_weight directly from parent variation into the MICROSCOPE eta_AB observable, without splitting the prediction into arbitrary Delta_w and tau factors.",
                "needed_map": "delta S_parent -> source residual -> Earth/source worldtube -> observed-frame force -> Ti/Pt material response -> orbit/readout eta_AB",
                "current_status": "TARGET_SHARPENED",
                "verdict": "THEOREM_NOT_DERIVED",
            }
        ),
        row(
            {
                "theorem_id": "DWT1997_1_variation_route",
                "statement": "A direct theorem would output either P_WEP=0 or a dimensionless predicted eta_AB residual with units/source path.",
                "needed_map": "parent variation plus force/readout kernel and source/material conventions",
                "current_status": "FORMALLY_CLEAN_IF_MAPS_EXIST",
                "verdict": "BLOCKED_BY_MISSING_MAPS",
            }
        ),
        row(
            {
                "theorem_id": "DWT1997_2_zero_route",
                "statement": "P_WEP=0 if action-scale/source-scalar theorem or WEP projection silence is parent-signed.",
                "needed_map": "parent action-scale owner or projection-silence theorem",
                "current_status": "CONDITIONAL_ONLY",
                "verdict": "ZERO_NOT_PROMOTED",
            }
        ),
        row(
            {
                "theorem_id": "DWT1997_3_finite_route",
                "statement": "A finite prediction requires the direct product or all split-product factors to be real, sourced, numeric/theorem-zero, and convention-matched.",
                "needed_map": "P_WEP direct product OR Delta_w_TiPt and tau_WEP pack",
                "current_status": "MISSING_NUMERIC_PARENT_PRODUCT",
                "verdict": "RUNNER_MUST_REFUSE",
            }
        ),
    ]

    readout_provenance = [
        row(
            {
                "provenance_id": "MRP1997_0_eta_source_charge_proxy",
                "pack_component": "eta/readout bound anchor",
                "fills_prior_row": "TAP1068_2_eta_readout; ORB1068_2_eta_convention",
                "dataset_id": "MICROSCOPE_final_TiPt_source_charge_proxy",
                "row_id": "R1_WEP_source_charge",
                "observable": "eta_WEP_source_charge",
                "upper_bound": "2.8e-15",
                "units": "dimensionless",
                "reference_url": "https://arxiv.org/abs/2209.15487",
                "doi": "10.1103/PhysRevLett.129.121102",
                "source_backed": "true",
                "claim_ready": "false",
            }
        ),
        row(
            {
                "provenance_id": "MRP1997_1_direct_geometry_context",
                "pack_component": "direct eta context",
                "fills_prior_row": "FRM1068_1_eta_mapping",
                "dataset_id": "MICROSCOPE_final_TiPt",
                "row_id": "R0_identity_coframe_direct",
                "observable": "eta_WEP_direct_geometry",
                "upper_bound": "2.8e-15",
                "units": "dimensionless",
                "reference_url": "https://arxiv.org/abs/2209.15487",
                "doi": "10.1103/PhysRevLett.129.121102",
                "source_backed": "true",
                "claim_ready": "false",
            }
        ),
    ]

    remaining_requirements = [
        row(
            {
                "requirement_id": "REQ1997_0_readout_formula",
                "required_input": "official MICROSCOPE eta_AB formula, sign convention, absolute-value convention, and test-mass pair mapping",
                "current_status": "PARTIAL_BOUND_PROVENANCE_ONLY",
                "blocks": "dimensionless direct product and tau_WEP readout convention",
            }
        ),
        row(
            {
                "requirement_id": "REQ1997_1_orbit_kernel",
                "required_input": "MICROSCOPE orbit/attitude/time averaging kernel or source-backed averaged equivalent",
                "current_status": "MISSING_ORBIT_KERNEL",
                "blocks": "projection from source residual to measured eta_AB",
            }
        ),
        row(
            {
                "requirement_id": "REQ1997_2_source_worldtube",
                "required_input": "Earth/source worldtube and source charge convention in the observed local frame",
                "current_status": "MISSING_SOURCE_WORLDTUBE",
                "blocks": "source leg of direct product/tau_WEP",
            }
        ),
        row(
            {
                "requirement_id": "REQ1997_3_material_tensor",
                "required_input": "Ti/Pt material response tensor for relative source-weight or material-charge channel",
                "current_status": "MISSING_FULL_MATERIAL_TENSOR",
                "blocks": "test-body leg and no-cancellation guard",
            }
        ),
        row(
            {
                "requirement_id": "REQ1997_4_xhat_norm",
                "required_input": "shared Xhat/chi_X normalization or declared branch-specific convention",
                "current_status": "MISSING_XHAT_NORMALIZATION",
                "blocks": "comparison across WEP, R10, clocks, and finite local branches",
            }
        ),
    ]

    runner_dryrun = [
        row(
            {
                "run_id": "RUN1997_0_direct_theorem",
                "check": "derive direct WEP product theorem",
                "result": "FAIL_PARENT_VARIATION_TO_ETA_MISSING",
                "reason": "source worldtube, force/readout map, material response, and eta convention are not jointly derived",
            }
        ),
        row(
            {
                "run_id": "RUN1997_1_first_source_row",
                "check": "import first real MICROSCOPE eta/readout provenance row",
                "result": "PASS_NONCLAIM_PROVENANCE",
                "reason": "numeric bound, units, URL, and DOI are recorded, but this is not an MTS prediction",
            }
        ),
        row(
            {
                "run_id": "RUN1997_2_tau_numeric",
                "check": "promote tau_WEP to numeric/theorem-zero",
                "result": "FAIL_NOT_TAU",
                "reason": "readout bound anchor is not a source-worldtube/orbit/material projection",
            }
        ),
        row(
            {
                "run_id": "RUN1997_3_runner_score",
                "check": "score WEP product",
                "result": "FAIL_VALID_PREDICTION_ROWS_ZERO",
                "reason": "direct product and split product remain missing",
            }
        ),
        row(
            {
                "run_id": "RUN1997_4_verdict",
                "check": "1997 next-step decision",
                "result": "NEXT_1998_MICROSCOPE_ETA_FORMULA_OR_ORBIT_KERNEL_ACQUISITION",
                "reason": "bound provenance exists; readout formula/orbit kernel is the next real component",
            }
        ),
    ]

    claim_gate = [
        row(
            {
                "gate_id": "CG1997_0_direct_product",
                "claim": "direct WEP product theorem is derived",
                "status": "FAIL_BLOCKED",
                "reason": "parent variation to eta_AB remains missing",
            }
        ),
        row(
            {
                "gate_id": "CG1997_1_first_source_row",
                "claim": "first real MICROSCOPE source/readout provenance row is acquired",
                "status": "PASS_NONCLAIM_PROVENANCE",
                "reason": "numeric bound, units, URL, and DOI are present",
            }
        ),
        row(
            {
                "gate_id": "CG1997_2_tau_WEP",
                "claim": "tau_WEP is numeric or theorem-zero",
                "status": "FAIL_BLOCKED",
                "reason": "the acquired row is a bound/readout anchor, not a tau projection",
            }
        ),
        row(
            {
                "gate_id": "CG1997_3_WEP_score",
                "claim": "WEP product can be scored",
                "status": "FAIL_BLOCKED",
                "reason": "strict runner has no valid prediction rows",
            }
        ),
        row(
            {
                "gate_id": "CG1997_4_local_GR",
                "claim": "local GR/WEP coupling branch is derived",
                "status": "FAIL_BLOCKED",
                "reason": "direct product, tau projection, and action-scale theorem routes remain open",
            }
        ),
    ]

    decision = [
        row(
            {
                "decision_id": "DEC1997_0_direct_status",
                "decision": "DIRECT_WEP_PRODUCT_THEOREM_NOT_DERIVED",
                "because": "parent variation still lacks source worldtube, force/readout, material response, and eta convention maps",
                "next_action": "keep direct theorem as preferred route but do not claim it",
            }
        ),
        row(
            {
                "decision_id": "DEC1997_1_source_status",
                "decision": "FIRST_REAL_READOUT_BOUND_PROVENANCE_IS_IMPORTED",
                "because": "MICROSCOPE R1 row supplies bound, units, URL, and DOI",
                "next_action": "extract official eta_AB formula/readout convention or orbit kernel",
            }
        ),
        row(
            {
                "decision_id": "DEC1997_2_best_next",
                "decision": "ETA_FORMULA_OR_ORBIT_KERNEL_NEXT",
                "because": "the bound anchor is not a projection functional; the next row must make the readout map explicit",
                "next_action": "1998-Y5-R2FR-MICROSCOPE-eta-readout-formula-or-orbit-kernel-acquisition.md",
            }
        ),
    ]

    next_target = [
        row(
            {
                "next_id": "NEXT1997_0_primary",
                "selection_status": "selected",
                "target_doc": "1998-Y5-R2FR-MICROSCOPE-eta-readout-formula-or-orbit-kernel-acquisition.md",
                "target_script": "scripts/Y5_R2FR_MICROSCOPE_eta_readout_formula_or_orbit_kernel_acquisition_1998.py",
                "task": "extract the official MICROSCOPE eta_AB formula/readout convention and, if available, the first orbit/averaging kernel row",
                "success_condition": "source-backed eta formula/sign/absolute convention and/or orbit kernel row with URL/DOI/provenance, still nonclaim until direct P_WEP or tau_WEP exists",
                "do_not": "do not set tau_WEP=1, set Delta_w=0 by taste, absorb relative weights into measured G, use cancellation arguments, claim WEP/local-GR, push GitHub, or edit formalization-workbench",
            }
        )
    ]

    source_weight = [
        row(
            {
                "artifact_id": "SW1997_0_direct_wep_product",
                "artifact_type": "direct_WEP_product_or_readout_provenance_nonclaim",
                "status": "DIRECT_THEOREM_MISSING_READOUT_PROVENANCE_IMPORTED",
                "source_path": str(DOC_PATH),
                "next_target": "1998-Y5-R2FR-MICROSCOPE-eta-readout-formula-or-orbit-kernel-acquisition.md",
            }
        )
    ]

    wep_coeffs = [
        row(
            {
                "coefficient_id": "WEP1997_0_readout_anchor",
                "quantity": "MICROSCOPE eta_AB bound/readout provenance",
                "required_formula": "P_WEP direct parent product or abs(Delta_w_TiPt*tau_WEP)",
                "required_evidence": "eta formula, orbit/readout kernel, source worldtube, material tensor, direct product or split product",
                "current_status": "READOUT_BOUND_ANCHOR_ONLY",
                "status": "NONCLAIM_PROVENANCE_ONLY",
            }
        )
    ]

    queue = [
        row(
            {
                "queue_id": "JR1997_0_eta_formula_or_orbit",
                "priority": "1",
                "needed_input": "official eta_AB formula/readout convention or orbit/averaging kernel",
                "route": "extract from MICROSCOPE paper/local source rows; keep provenance URL/DOI and unit convention",
                "required_fields": "eta_formula;sign_convention;absolute_value_rule;test_pair;orbit_kernel;source_path;doi;units",
                "blocked_claims": "tau_WEP_numeric;WEP_product_score;local_GR;Newton",
            }
        )
    ]

    return {
        "source_register": source_register(stamp),
        "direct_theorem": direct_theorem,
        "readout_provenance": readout_provenance,
        "remaining_requirements": remaining_requirements,
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
    val("VAL1997_00_sources", "PASS" if not source_failures else "FAIL", "all source paths exist and needles found" if not source_failures else ";".join(row["source_id"] for row in source_failures))

    theorem_not_promoted = any(row["theorem_id"] == "DWT1997_0_target" and row["verdict"] == "THEOREM_NOT_DERIVED" for row in tables["direct_theorem"])
    val("VAL1997_01_direct_theorem", "PASS" if theorem_not_promoted else "FAIL", "direct WEP product theorem remains unproved")

    provenance_rows = tables["readout_provenance"]
    provenance_ok = all(row["source_backed"] == "true" and row["doi"] and row["reference_url"] for row in provenance_rows)
    nonclaim = all(row["claim_ready"] == "false" and row["valid_for_claim"] == "false" for row in provenance_rows)
    val("VAL1997_02_readout_provenance", "PASS" if provenance_ok and nonclaim else "FAIL", "readout provenance rows have URL/DOI and remain nonclaim")

    requirements_missing = all(row["current_status"] in {"PARTIAL_BOUND_PROVENANCE_ONLY", "MISSING_ORBIT_KERNEL", "MISSING_SOURCE_WORLDTUBE", "MISSING_FULL_MATERIAL_TENSOR", "MISSING_XHAT_NORMALIZATION"} for row in tables["remaining_requirements"])
    val("VAL1997_03_remaining_requirements", "PASS" if requirements_missing else "FAIL", "remaining tau/direct-product requirements are explicit")

    runner_selects = tables["runner_dryrun"][-1]["result"] == "NEXT_1998_MICROSCOPE_ETA_FORMULA_OR_ORBIT_KERNEL_ACQUISITION"
    val("VAL1997_04_runner_decision", "PASS" if runner_selects else "FAIL", "runner selects eta formula/orbit target")

    gates_safe = all(row["status"] in {"FAIL_BLOCKED", "PASS_NONCLAIM_PROVENANCE"} for row in tables["claim_gate"])
    no_physics_claim = all(row["status"] == "FAIL_BLOCKED" for row in tables["claim_gate"] if row["gate_id"] != "CG1997_1_first_source_row")
    val("VAL1997_05_claim_gates", "PASS" if gates_safe and no_physics_claim else "FAIL", "only nonclaim provenance passes; physics claims blocked")

    next_ok = tables["next"][0]["target_doc"] == "1998-Y5-R2FR-MICROSCOPE-eta-readout-formula-or-orbit-kernel-acquisition.md"
    val("VAL1997_06_next_target", "PASS" if next_ok else "FAIL", "1998 eta formula/orbit target selected")

    all_rows = [row for rows_for_table in tables.values() for row in rows_for_table]
    flags_safe = all(row.get("valid_for_claim") == "false" and row.get("claim_allowed") == "false" for row in all_rows)
    val("VAL1997_07_claim_flags_safe", "PASS" if flags_safe else "FAIL", "claim flags all false")

    parse_failures = []
    for output_name, path in OUTPUTS.items():
        if not path.exists():
            parse_failures.append(f"{output_name}:missing")
            continue
        with path.open(newline="", encoding="utf-8") as handle:
            parsed = list(csv.DictReader(handle))
        if not parsed:
            parse_failures.append(f"{output_name}:empty")
    val("VAL1997_08_csv_parse", "PASS" if not parse_failures else "FAIL", "all generated CSVs parse with rows" if not parse_failures else ";".join(parse_failures))

    pycache_exists = (ROOT / "scripts" / "__pycache__").exists()
    val("VAL1997_09_pycache_absent", "PASS" if not pycache_exists else "FAIL", "scripts __pycache__ absent")

    formalization_artifacts = []
    checkpoint_markers = ("Y5_R2FR", "P8_Y5", "JR1997", "DWT1997", "MRP1997", "WEP")
    if FORMALIZATION.exists():
        formalization_artifacts = [
            path
            for path in FORMALIZATION.rglob("*")
            if "1997" in path.name and any(marker in path.name for marker in checkpoint_markers)
        ]
    val("VAL1997_10_formalization_untouched", "PASS" if not formalization_artifacts else "FAIL", f"formalization_1997_artifact_count={len(formalization_artifacts)}")

    overall = "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL"
    val("VAL1997_OVERALL", overall, "1997 direct WEP product theorem or first real tau source row")
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
        ("Direct WEP Product Theorem Attempt", tables["direct_theorem"]),
        ("MICROSCOPE Readout Provenance", tables["readout_provenance"]),
        ("tau/Direct Product Remaining Requirements", tables["remaining_requirements"]),
        ("Runner Dryrun", tables["runner_dryrun"]),
        ("Claim Gate", tables["claim_gate"]),
        ("Decision Ledger", tables["decision"]),
        ("Next Target", tables["next"]),
        ("Validation", validation_rows),
    ]
    lines = [
        "# 1997 Y5 R2FR: Direct WEP Product Theorem Or First Real tau Source Row",
        "",
        "Private checkpoint. This tries the clean direct WEP product route before falling back to tau/source acquisition.",
        "",
        "Verdict: direct `P_WEP_relative_source_weight` is still the cleanest theory route, but it does not close because parent variation has not yet produced the MICROSCOPE `eta_AB` observable with source worldtube, force/readout, material response, and units.",
        "",
        "Concrete progress: the first real MICROSCOPE eta/readout provenance row is imported into the current branch with numeric bound, units, URL, and DOI. This is not `tau_WEP` and not an MTS prediction.",
        "",
        "Next honest move: extract the official `eta_AB` formula/readout convention or the first orbit/averaging kernel row.",
        "",
        "No WEP, local-GR, Newton, R10, PPN, clock, orbital, or public claim follows from 1997.",
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
    print(f"VAL1997_OVERALL={overall}")
    return 0 if overall == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
