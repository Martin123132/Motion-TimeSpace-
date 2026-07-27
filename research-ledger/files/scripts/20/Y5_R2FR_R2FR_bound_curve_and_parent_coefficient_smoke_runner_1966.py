from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


BRANCH = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
ROOT = Path(__file__).resolve().parents[1]
FORMALIZATION = ROOT.parent / "formalization-workbench"
MTS_RESIDUALS = ROOT / "source-intake" / "mts_residuals"
SOURCE_WEIGHT_DOCS = ROOT / "source-intake" / "source-weight" / "docs"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
EXTERNAL_SOURCES = ROOT / "source-intake" / "external-sources"

DOC_PATH = ROOT / "1966-Y5-R2FR-R2FR-bound-curve-and-parent-coefficient-smoke-runner.md"
VALIDATION_PATH = MTS_RESIDUALS / "P8_Y5_BRR545_1966_VALIDATION.csv"

LOCAL_SOURCES = {
    "1965_doc": {
        "path": ROOT / "1965-Y5-R2FR-R2-fR-zero-proof-or-executable-R11-bound-row.md",
        "needles": ["ZP1965_6_verdict", "SM1965_2_yukawa_alpha", "NEXT1965_0_primary"],
    },
    "1965_validation": {
        "path": MTS_RESIDUALS / "P8_Y5_BRR545_1965_VALIDATION.csv",
        "needles": ["VAL1965_OVERALL", "PASS"],
    },
    "963_runner_spec": {
        "path": MTS_RESIDUALS / "P8_Y5_R10_963_R2FR_BOUND_RUNNER_SPEC.csv",
        "needles": ["R2RUN963_2_R10_bound_curve", "R2RUN963_4_decision_logic"],
    },
    "964_runner": {
        "path": MTS_RESIDUALS / "P8_Y5_R10_964_R2FR_NONCLAIM_RUNNER_RESULT.csv",
        "needles": ["R2RUN964_2_Lee2020_anchor", "R2RUN964_VERDICT"],
    },
}

WEB_SOURCES = [
    {
        "source_id": "WEB1966_0_Lee2020_arxiv",
        "title": "New Test of the Gravitational 1/r^2 Law at Separations down to 52 um",
        "url": "https://arxiv.org/abs/2002.11761",
        "doi": "10.1103/PhysRevLett.124.101101",
        "year": 2020,
        "usable_content": "abstract/source record gives alpha=1 range anchor and experimental separation range",
        "full_curve_status": "FULL_CURVE_NOT_MACHINE_READABLE_IN_QUICK_PASS",
    },
    {
        "source_id": "WEB1966_1_Lee2020_pdf",
        "title": "Lee et al. 2020 PDF",
        "url": "https://arxiv.org/pdf/2002.11761",
        "doi": "10.1103/PhysRevLett.124.101101",
        "year": 2020,
        "usable_content": "paper figure can potentially be digitized later",
        "full_curve_status": "DIGITIZATION_REQUIRED",
    },
    {
        "source_id": "WEB1966_2_Kapner2007_arxiv",
        "title": "Tests of the Gravitational Inverse-Square Law below the Dark-Energy Length Scale",
        "url": "https://arxiv.org/abs/hep-ph/0611184",
        "doi": "10.1103/PhysRevLett.98.021101",
        "year": 2007,
        "usable_content": "older continuity alpha=1 range anchor",
        "full_curve_status": "ANCHOR_ONLY_FOR_THIS_CHECKPOINT",
    },
    {
        "source_id": "WEB1966_3_EotWash_publications",
        "title": "Eot-Wash publications page",
        "url": "https://www.npl.washington.edu/eotwash/publications",
        "doi": "not_applicable",
        "year": 2026,
        "usable_content": "publication provenance for Lee et al. short-range gravity paper",
        "full_curve_status": "PUBLICATION_LEDGER_ONLY",
    },
]


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dirs() -> None:
    for directory in (MTS_RESIDUALS, SOURCE_WEIGHT_DOCS, RAB_QUEUE, EXTERNAL_SOURCES):
        directory.mkdir(parents=True, exist_ok=True)


def base(row_id: str) -> dict[str, object]:
    return {
        "branch": BRANCH,
        "row_id": row_id,
        "valid_for_claim": False,
        "public_claim": False,
        "created_utc": stamp(),
    }


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def local_source_register() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for source_id, source_spec in LOCAL_SOURCES.items():
        path = source_spec["path"]
        needles = source_spec["needles"]
        exists = path.exists()
        text = path.read_text(encoding="utf-8", errors="replace") if exists else ""
        missing = [needle for needle in needles if needle not in text]
        row = base(source_id)
        row.update(
            {
                "source_path": str(path),
                "purpose": "1966 R2/fR bound curve and parent coefficient smoke runner",
                "required_needles": ";".join(needles),
                "status": "EXISTS_NEEDLES_CONFIRMED" if exists and not missing else "MISSING_SOURCE_OR_NEEDLE",
                "missing_needles": ";".join(missing),
            }
        )
        rows.append(row)
    return rows


def web_source_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for source in WEB_SOURCES:
        row = base(source["source_id"])
        row.update(
            {
                "source_id": source["source_id"],
                "title": source["title"],
                "url": source["url"],
                "doi": source["doi"],
                "year": source["year"],
                "usable_content": source["usable_content"],
                "full_curve_status": source["full_curve_status"],
                "source_quality": "PRIMARY_OR_GROUP_LEDGER" if "arxiv" in source["url"] or "washington" in source["url"] else "REFERENCE",
            }
        )
        rows.append(row)
    return rows


def bound_anchor_rows() -> list[dict[str, object]]:
    entries = [
        {
            "row_id": "BND1966_0_Lee2020_alpha1_anchor",
            "source_id": "WEB1966_0_Lee2020_arxiv",
            "lambda_value": 38.6,
            "lambda_units": "micrometer",
            "alpha_bound": 1.0,
            "bound_interpretation": "gravitational-strength Yukawa alpha=1 excluded for ranges greater than this anchor at 95 percent confidence",
            "extraction_method": "abstract_anchor",
            "curve_role": "anchor_only_non_curve",
        },
        {
            "row_id": "BND1966_1_Kapner2007_alpha1_anchor",
            "source_id": "WEB1966_2_Kapner2007_arxiv",
            "lambda_value": 56.0,
            "lambda_units": "micrometer",
            "alpha_bound": 1.0,
            "bound_interpretation": "older continuity anchor: alpha<=1 down to this length scale at 95 percent confidence",
            "extraction_method": "abstract_anchor",
            "curve_role": "anchor_only_non_curve",
        },
        {
            "row_id": "BND1966_2_full_curve_required",
            "source_id": "WEB1966_1_Lee2020_pdf",
            "lambda_value": "MISSING_DIGITIZED_CURVE",
            "lambda_units": "micrometer",
            "alpha_bound": "MISSING_DIGITIZED_CURVE",
            "bound_interpretation": "required for claim-grade interpolation/scoring",
            "extraction_method": "figure_digitization_required_or_machine_table_needed",
            "curve_role": "full_curve_required",
        },
    ]
    rows: list[dict[str, object]] = []
    for entry in entries:
        row = base(entry["row_id"])
        row.update(
            {
                "source_id": entry["source_id"],
                "lambda_value": entry["lambda_value"],
                "lambda_units": entry["lambda_units"],
                "alpha_bound": entry["alpha_bound"],
                "bound_interpretation": entry["bound_interpretation"],
                "extraction_method": entry["extraction_method"],
                "curve_role": entry["curve_role"],
                "valid_for_claim": False,
                "public_claim": False,
            }
        )
        rows.append(row)
    return rows


def mts_prediction_rows() -> list[dict[str, object]]:
    entries = [
        (
            "MTS1966_0_parent_coefficient_required",
            "R2_fR_scalar_mode",
            "c_R2_or_fRR",
            "MISSING_PARENT_COEFFICIENT",
            "MISSING_UNITS",
            "MISSING_NORMALIZATION",
            "MISSING_SOURCE_EQUATION",
            "REJECT_FOR_CLAIM",
        ),
        (
            "MTS1966_1_zero_switch_required",
            "R2_fR_scalar_mode",
            "c_R2=f_RR=0",
            "MISSING_PARENT_MINIMALITY_ZERO_CERTIFICATE",
            "not_applicable_if_zero",
            "not_applicable_if_zero",
            "MISSING_PARENT_ACTION_SIGNATURE",
            "REJECT_FOR_CLAIM",
        ),
        (
            "MTS1966_2_scalar_map_required",
            "R2_fR_scalar_mode",
            "alpha_s_lambda_s",
            "MISSING_ALPHA_AND_LAMBDA",
            "alpha_dimensionless_lambda_micrometer",
            "R_plus_cR2R2_or_declared_fR_normalization",
            "MISSING_FORMULA_SOURCE_IN_PARENT_CONTEXT",
            "REJECT_FOR_CLAIM",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, operator_family, parameter, value, units, normalization, source_equation, status in entries:
        row = base(row_id)
        row.update(
            {
                "operator_family": operator_family,
                "parameter": parameter,
                "value": value,
                "units": units,
                "normalization": normalization,
                "source_equation": source_equation,
                "status": status,
            }
        )
        rows.append(row)
    return rows


def smoke_runner_rows() -> list[dict[str, object]]:
    entries = [
        (
            "SMOKE1966_0_anchor_parse",
            "BND1966_0_Lee2020_alpha1_anchor;BND1966_1_Kapner2007_alpha1_anchor",
            "PASS_SCHEMA_ONLY",
            "positive lambda and alpha values parse, but anchor_only_non_curve cannot support interpolation or pass/fail claims",
        ),
        (
            "SMOKE1966_1_full_curve",
            "BND1966_2_full_curve_required",
            "REJECTED_MISSING_FULL_CURVE",
            "full digitized curve or machine-readable table required before alpha(lambda) scoring",
        ),
        (
            "SMOKE1966_2_mts_coefficient",
            "MTS1966_0_parent_coefficient_required",
            "REJECTED_MISSING_PARENT_COEFFICIENT",
            "MTS coefficient cannot be fitted to external bound",
        ),
        (
            "SMOKE1966_3_zero_switch",
            "MTS1966_1_zero_switch_required",
            "REJECTED_ZERO_THEOREM_NOT_PARENT_SIGNED",
            "minimality/no-extension/no-integrated-out-tower certificate missing",
        ),
        (
            "SMOKE1966_4_decision",
            "all_rows",
            "R2FR_SMOKE_RUNNER_BLOCKED_NONCLAIM",
            "data plumbing works, but no claim-grade branch exists yet",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, input_rows, runner_status, reason in entries:
        row = base(row_id)
        row.update(
            {
                "input_rows": input_rows,
                "runner_status": runner_status,
                "reason": reason,
                "accepted_for_claim": False,
            }
        )
        rows.append(row)
    return rows


def claim_gate_rows() -> list[dict[str, object]]:
    entries = [
        ("CG1966_0_source_anchors", "Source-backed anchor rows exist.", "PASS_NONCLAIM", "anchors are smoke data only"),
        ("CG1966_1_full_curve", "Claim-grade alpha(lambda) full curve exists.", "FAIL_BLOCKED", "digitized/machine-readable curve missing"),
        ("CG1966_2_mts_prediction", "MTS supplies c_R2/f_RR or alpha(lambda).", "FAIL_BLOCKED", "parent coefficient missing"),
        ("CG1966_3_R2FR_score", "R2/fR residual branch can be scored.", "FAIL_BLOCKED", "full curve and MTS prediction missing"),
        ("CG1966_4_EH_second_order", "EH second-order premise is cleared.", "FAIL_BLOCKED", "R2/fR remains zero-or-bound unresolved"),
    ]
    rows: list[dict[str, object]] = []
    for row_id, claim, status, reason in entries:
        row = base(row_id)
        row.update({"claim": claim, "status": status, "reason": reason})
        rows.append(row)
    return rows


def decision_rows() -> list[dict[str, object]]:
    entries = [
        (
            "DEC1966_0_verdict",
            "REAL_ANCHORS_RECORDED_FULL_CURVE_AND_PARENT_COEFFICIENT_MISSING",
            "Lee 2020 and Kapner 2007 anchors are source-backed but not claim-grade curves; MTS still lacks c_R2/f_RR.",
            "do not score R2/fR; acquire full curve or derive zero/coefficient",
        ),
        (
            "DEC1966_1_next",
            "RETURN_TO_PARENT_COEFFICIENT_OR_DIGITIZE_CURVE",
            "A bound curve alone is not enough without MTS prediction, and MTS prediction alone is not enough without source-backed bounds.",
            "next best theory step is parent minimality/coefficient; next empirical step is full curve digitization",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, decision, reason, next_action in entries:
        row = base(row_id)
        row.update({"decision": decision, "reason": reason, "next_action": next_action})
        rows.append(row)
    return rows


def next_rows() -> list[dict[str, object]]:
    row = base("NEXT1966_0_primary")
    row.update(
        {
            "priority": "selected",
            "target_doc": "1967-Y5-R2FR-parent-minimality-or-R2FR-coefficient-origin.md",
            "target_script": "scripts/Y5_R2FR_parent_minimality_or_R2FR_coefficient_origin_1967.py",
            "objective": "derive the parent minimality/no-extension theorem or identify the coefficient origin for c_R2/f_RR; keep digitized curve acquisition as parallel empirical task",
            "acceptance_output": "parent zero/coefficient origin proof attempt, or explicit coefficient-origin blocker plus data-acquisition queue",
            "nonclaim_rule": "no R2/fR score, EH claim, or Newton claim without zero/coefficient plus source-backed bounds",
        }
    )
    return [row]


def snapshot_rows() -> list[dict[str, object]]:
    row = base("SNAP1966_0_project_position")
    row.update(
        {
            "strongest_result": "R2/fR empirical plumbing now has real source-backed anchors and a strict refusal path for anchor-only/non-curve data.",
            "what_improved": "The project can no longer handwave higher-curvature tests; it knows exactly what data and parent coefficients are missing.",
            "still_missing": "full alpha(lambda) curve, MTS c_R2/f_RR or zero theorem, scalar screening/regime map, PPN projection, EH/GM/PPN completion",
            "claim_status": "anchor-only smoke data and missing MTS coefficient; no R2/fR or EH claim",
        }
    )
    return [row]


OUTPUTS = {
    "local_source_register": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1966_LOCAL_SOURCE_REGISTER.csv",
    "web_sources": EXTERNAL_SOURCES / "R2FR_BOUND_WEB_SOURCES_1966.csv",
    "bound_anchors": EXTERNAL_SOURCES / "R2FR_ALPHA_LAMBDA_BOUND_ANCHORS_1966_NONCLAIM.csv",
    "mts_predictions": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1966_MTS_R2FR_PREDICTION_PLACEHOLDERS.csv",
    "smoke_runner": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1966_R2FR_SMOKE_RUNNER.csv",
    "claim_gate": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1966_CLAIM_GATE.csv",
    "decision": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1966_DECISION_LEDGER.csv",
    "next": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1966_NEXT_TARGET.csv",
    "snapshot": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1966_PROJECT_STATUS_SNAPSHOT.csv",
    "source_weight": SOURCE_WEIGHT_DOCS / "R2FR_BOUND_CURVE_1966_NONCLAIM.csv",
    "queue": RAB_QUEUE / "JR1966_R2FR_FULL_CURVE_AND_PARENT_COEFFICIENT_QUEUE.csv",
}


def build_tables() -> dict[str, list[dict[str, object]]]:
    source_weight = [
        {
            **base("SW1966_0_nonclaim_weight"),
            "artifact": "1966 R2/fR bound anchors and smoke runner",
            "weight": "SOURCE_ANCHORS_ONLY_NOT_SCOREABLE",
            "reason": "anchors are sourced but full curve and parent coefficients are missing",
        }
    ]
    queue = [
        {
            **base("AQ1966_0_full_curve"),
            "target": "digitize or acquire full Lee2020 alpha(lambda) curve",
            "needed_inputs": "lambda grid; alpha_bound grid; extraction uncertainty; source page/figure; units; valid_for_claim",
            "priority": "HIGH_EMPIRICAL",
        },
        {
            **base("AQ1966_1_parent_coefficient"),
            "target": "derive c_R2/f_RR origin or zero",
            "needed_inputs": "parent action term; normalization; coefficient units; sign; no-integrated-out-tower certificate",
            "priority": "HIGHEST_THEORY",
        },
    ]
    return {
        "local_source_register": local_source_register(),
        "web_sources": web_source_rows(),
        "bound_anchors": bound_anchor_rows(),
        "mts_predictions": mts_prediction_rows(),
        "smoke_runner": smoke_runner_rows(),
        "claim_gate": claim_gate_rows(),
        "decision": decision_rows(),
        "next": next_rows(),
        "snapshot": snapshot_rows(),
        "source_weight": source_weight,
        "queue": queue,
    }


def validation_row(validation_id: str, status: str, detail: str) -> dict[str, object]:
    return {
        "validation_id": validation_id,
        "status": status,
        "detail": detail,
        "valid_for_claim": False,
        "public_claim": False,
    }


def formalization_hits() -> int:
    if not FORMALIZATION.exists():
        return 0
    patterns = ("1966-", "*_1966_*", "*Y5*1966*", "*VAL1966*", "*P8*1966*")
    return sum(1 for path in FORMALIZATION.rglob("*") if any(Path(path.name).match(pattern) for pattern in patterns))


def validate(tables: dict[str, list[dict[str, object]]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    local_sources_ok = all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in tables["local_source_register"])
    rows.append(validation_row("VAL1966_00_local_sources", "PASS" if local_sources_ok else "FAIL", "local source paths exist and needles found"))

    web_ok = all(str(row["url"]).startswith("https://") and str(row["source_id"]).startswith("WEB1966_") for row in tables["web_sources"])
    rows.append(validation_row("VAL1966_01_web_sources", "PASS" if web_ok else "FAIL", "web source strings and provenance recorded"))

    anchor_rows = [row for row in tables["bound_anchors"] if row["curve_role"] == "anchor_only_non_curve"]
    anchors_ok = all(float(row["lambda_value"]) > 0 and float(row["alpha_bound"]) > 0 and not bool(row["valid_for_claim"]) for row in anchor_rows)
    rows.append(validation_row("VAL1966_02_anchor_rows", "PASS" if anchors_ok else "FAIL", "anchor rows parse positive but remain nonclaim"))

    full_curve_missing = any(row["row_id"] == "BND1966_2_full_curve_required" and row["lambda_value"] == "MISSING_DIGITIZED_CURVE" and not bool(row["valid_for_claim"]) for row in tables["bound_anchors"])
    rows.append(validation_row("VAL1966_03_full_curve_missing", "PASS" if full_curve_missing else "FAIL", "full curve blocker retained"))

    mts_missing = all(str(row["value"]).startswith("MISSING") and not bool(row["valid_for_claim"]) for row in tables["mts_predictions"])
    rows.append(validation_row("VAL1966_04_mts_placeholders", "PASS" if mts_missing else "FAIL", "MTS parent coefficient placeholders remain rejected"))

    runner_ok = any(row["row_id"] == "SMOKE1966_4_decision" and row["runner_status"] == "R2FR_SMOKE_RUNNER_BLOCKED_NONCLAIM" for row in tables["smoke_runner"])
    rows.append(validation_row("VAL1966_05_smoke_runner", "PASS" if runner_ok else "FAIL", "smoke runner blocks claims"))

    gate_ok = all(row["status"] != "PASS_CLAIM" for row in tables["claim_gate"]) and any(row["row_id"] == "CG1966_3_R2FR_score" and row["status"] == "FAIL_BLOCKED" for row in tables["claim_gate"])
    rows.append(validation_row("VAL1966_06_claim_gates", "PASS" if gate_ok else "FAIL", "R2/fR and EH claims remain blocked"))

    decision_ok = any(row["decision"] == "REAL_ANCHORS_RECORDED_FULL_CURVE_AND_PARENT_COEFFICIENT_MISSING" for row in tables["decision"])
    rows.append(validation_row("VAL1966_07_decision", "PASS" if decision_ok else "FAIL", "source anchors/nonclaim decision recorded"))

    next_ok = tables["next"][0]["target_doc"] == "1967-Y5-R2FR-parent-minimality-or-R2FR-coefficient-origin.md"
    rows.append(validation_row("VAL1966_08_next_target", "PASS" if next_ok else "FAIL", "1967 target selected"))

    flags_ok = all(not bool(row.get("valid_for_claim")) and not bool(row.get("public_claim")) for table in tables.values() for row in table)
    rows.append(validation_row("VAL1966_09_claim_flags_safe", "PASS" if flags_ok else "FAIL", "claim flags all false"))

    csv_ok = all(bool(read_csv(path)) for path in OUTPUTS.values())
    rows.append(validation_row("VAL1966_10_csv_parse", "PASS" if csv_ok else "FAIL", "all generated CSVs parse with rows"))

    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    rows.append(validation_row("VAL1966_11_pycache_absent", "PASS" if not pycache.exists() else "FAIL", "scripts __pycache__ absent"))

    count = formalization_hits()
    rows.append(validation_row("VAL1966_12_formalization_untouched", "PASS" if count == 0 else "FAIL", f"formalization_1966_artifact_count={count}"))

    overall = "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL"
    rows.append(validation_row("VAL1966_OVERALL", overall, "1966 R2/fR bound curve and parent coefficient smoke runner"))
    return rows


def markdown_table(rows: list[dict[str, object]]) -> str:
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    lines = ["| " + " | ".join(fields) + " |", "| " + " | ".join("---" for _ in fields) + " |"]
    for row in rows:
        values = [str(row.get(field, "")).replace("\n", " ") for field in fields]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def write_markdown(tables: dict[str, list[dict[str, object]]], validation_rows: list[dict[str, object]]) -> None:
    sections = [
        ("Local Source Register", tables["local_source_register"]),
        ("Web Source Ledger", tables["web_sources"]),
        ("Bound Anchors", tables["bound_anchors"]),
        ("MTS Prediction Placeholders", tables["mts_predictions"]),
        ("Smoke Runner", tables["smoke_runner"]),
        ("Claim Gate", tables["claim_gate"]),
        ("Decision Ledger", tables["decision"]),
        ("Next Target", tables["next"]),
        ("Project Status Snapshot", tables["snapshot"]),
        ("Validation", validation_rows),
    ]
    lines = [
        "# 1966 Y5 R2FR: R2/fR Bound Curve And Parent Coefficient Smoke Runner",
        "",
        "Private checkpoint. This adds real source-backed short-range gravity anchors for the R2/fR scalar-mode branch and refuses to treat them as a full alpha(lambda) curve.",
        "",
        "Verdict: Lee 2020 and Kapner 2007 provide useful alpha=1 range anchors, but they are anchor-only smoke rows here. A claim-grade R2/fR score still needs a full digitized or machine-readable alpha(lambda) bound curve and an MTS parent coefficient or parent zero theorem.",
        "",
        "No R2/fR, EH, Newton, or local-GR claim follows from this checkpoint.",
        "",
    ]
    for title, rows in sections:
        lines.extend([f"## {title}", "", markdown_table(rows), ""])
    DOC_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    ensure_dirs()
    tables = build_tables()
    for output_name, path in OUTPUTS.items():
        write_csv(path, tables[output_name])
    validation_rows = validate(tables)
    write_csv(VALIDATION_PATH, validation_rows)
    write_markdown(tables, validation_rows)
    overall = validation_rows[-1]["status"]
    print(f"wrote {DOC_PATH}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"VAL1966_OVERALL={overall}")
    return 0 if overall == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
