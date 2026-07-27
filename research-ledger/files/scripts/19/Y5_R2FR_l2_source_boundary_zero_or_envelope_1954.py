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

DOC_PATH = ROOT / "1954-Y5-R2FR-l2-source-boundary-zero-or-envelope.md"
VALIDATION_PATH = MTS_RESIDUALS / "P8_Y5_BRR545_1954_VALIDATION.csv"

SOURCES = {
    "1953_doc": {
        "path": ROOT / "1953-Y5-R2FR-parent-B_eff-profile-or-kernel-bound.md",
        "needles": ["PB1953_2_kernel_transport_caveat", "NEXT1953_0_primary", "VAL1953_OVERALL"],
    },
    "1953_validation": {
        "path": MTS_RESIDUALS / "P8_Y5_BRR545_1953_VALIDATION.csv",
        "needles": ["VAL1953_OVERALL", "PASS"],
    },
    "1953_profile": {
        "path": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1953_BEFF_PROFILE_DECOMPOSITION.csv",
        "needles": ["PB1953_4_source_worldtube_profile", "PB1953_5_full_zero_condition"],
    },
    "1953_envelopes": {
        "path": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1953_L2_ENVELOPE_LEDGER.csv",
        "needles": ["ENV1953_2_kernel_transport", "ENV1953_3_boundary_transport"],
    },
}


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dirs() -> None:
    for directory in (MTS_RESIDUALS, SOURCE_WEIGHT_DOCS, RAB_QUEUE):
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


def source_register() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for source_id, spec in SOURCES.items():
        path = spec["path"]
        needles = spec["needles"]
        exists = path.exists()
        text = path.read_text(encoding="utf-8", errors="replace") if exists else ""
        missing = [needle for needle in needles if needle not in text]
        row = base(source_id)
        row.update(
            {
                "source_path": str(path),
                "purpose": "1954 l2 source boundary zero or envelope",
                "required_needles": ";".join(needles),
                "status": "EXISTS_NEEDLES_CONFIRMED" if exists and not missing else "MISSING_SOURCE_OR_NEEDLE",
                "missing_needles": ";".join(missing),
            }
        )
        rows.append(row)
    return rows


def residual_split_rows() -> list[dict[str, object]]:
    entries = [
        (
            "L2R1954_0_baseline_subtraction",
            "Solar-system l=2 structure is not itself a failure; Cassini constrains extra l=2 slip beyond the GR baseline.",
            "B_2^obs = B_2^GR + Delta B_2^MTS; S_TF reads Delta B_2^MTS",
            "BASELINE_SPLIT_BUILT_NONCLAIM",
            "This fixes an important fairness issue: MTS should not be punished for l=2 structure already present in GR.",
            "no pass until Delta B_2^MTS is zero or bounded",
        ),
        (
            "L2R1954_1_same_source_map_condition",
            "If the local parent action reduces to the EH source map for ordinary matter, ordinary source multipoles feed GR, not extra MTS slip.",
            "Delta J_2^MTS=0 if delta S_parent/delta g -> delta S_EH+matter/delta g and extra fields are source-silent",
            "CONDITION_SHARPENED_NOT_SIGNED",
            "The source l=2 zero target becomes a same-source-map theorem, not a demand that the Sun be spherical.",
            "need parent EH-core/same-source proof",
        ),
        (
            "L2R1954_2_no_extra_boundary_dof_condition",
            "If the extra local branch has no independent l=2 boundary data, boundary l=2 remains GR baseline only.",
            "Delta h_boundary2^MTS=0 if boundary data are fixed by GR matching plus decaying extra branch",
            "CONDITION_SHARPENED_NOT_SIGNED",
            "Boundary l=2 is not fatal if it is not an extra MTS degree of freedom.",
            "need parent boundary uniqueness/decay proof",
        ),
        (
            "L2R1954_3_kernel_residual_condition",
            "An equivariant kernel transports only residual l=2 input after GR subtraction.",
            "Delta B_K2=K_2[Delta J_2^MTS]",
            "CONDITIONAL_PROFILE_RULE",
            "Kernel transport becomes safe once residual source l=2 is zero or bounded.",
            "need residual l=2 source envelope or zero theorem",
        ),
        (
            "L2R1954_4_finite_residual_envelope",
            "If zero fails, the correct bound uses residual l=2 envelopes, not total solar/GR multipoles.",
            "|Delta B_eff| <= |K_2[Delta J_2]| + |H_2[Delta h_2]| + |K_2[Delta J_source2]|",
            "BOUND_TEMPLATE_REFINED_NOT_SOURCED",
            "This is the right finite-bound route and avoids over-penalising MTS against its own GR baseline.",
            "need numeric residual envelopes and W_STF",
        ),
        (
            "L2R1954_5_verdict",
            "The source/boundary l=2 problem is reframed as an extra-residual problem, but not solved.",
            "Delta B_2^MTS=0 requires same-source map + no extra boundary dof + source-silent extra sector",
            "RESIDUAL_SPLIT_DONE_ZERO_UNSIGNED",
            "This is progress: the target is now local EH equivalence for residual multipoles.",
            "move to same-source-map/no-extra-boundary proof",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, statement, math_form, status, implication, required_fix in entries:
        row = base(row_id)
        row.update(
            {
                "statement": statement,
                "math_form": math_form,
                "status": status,
                "implication": implication,
                "required_fix": required_fix,
            }
        )
        rows.append(row)
    return rows


def residual_input_rows() -> list[dict[str, object]]:
    entries = [
        (
            "RIN1954_0_DeltaJ2",
            "Delta J_2^MTS",
            "extra source l=2 current after GR baseline subtraction",
            "MISSING",
            "source-current units",
            "MISSING_SAME_SOURCE_MAP_OR_ENVELOPE",
        ),
        (
            "RIN1954_1_Deltah2",
            "Delta h_boundary2^MTS",
            "extra l=2 boundary/matching data after GR baseline subtraction",
            "MISSING",
            "boundary data units",
            "MISSING_NO_EXTRA_BOUNDARY_DOF_OR_ENVELOPE",
        ),
        (
            "RIN1954_2_DeltaJsource2",
            "Delta J_source2^MTS",
            "extra source-worldtube anisotropy current beyond GR matter coupling",
            "MISSING",
            "source-current units",
            "MISSING_SOURCE_SILENCE_OR_ENVELOPE",
        ),
        (
            "RIN1954_3_WSTF",
            "||W_STF||_1",
            "Cassini readout norm for residual l=2 profile",
            "MISSING",
            "inverse profile units",
            "MISSING_READOUT_NORM",
        ),
        (
            "RIN1954_4_S_TF_residual_bound",
            "abs(S_TF_extra)",
            "residual Cassini-visible STF slip bound after GR subtraction",
            "MISSING",
            "dimensionless",
            "MISSING_COMBINED_RESIDUAL_BOUND",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, symbol, definition, value, units, status in entries:
        row = base(row_id)
        row.update({"symbol": symbol, "definition": definition, "value": value, "units": units, "status": status})
        rows.append(row)
    return rows


def runner_rows() -> list[dict[str, object]]:
    entries = [
        (
            "RUN1954_0_GR_baseline_split",
            "S_TF reads Delta B_2^MTS, not B_2^GR",
            "baseline split accepted as nonclaim guard",
            "",
            "PASS_NONCLAIM_SCOPE_GUARD",
            "fair comparator principle established",
        ),
        (
            "RUN1954_1_residual_zero",
            "Delta B_2^MTS=0",
            "same-source map + no extra boundary dof + source silence",
            "MISSING_SAME_SOURCE_MAP;MISSING_BOUNDARY_UNIQUENESS;MISSING_SOURCE_SILENCE",
            "BLOCKED_ZERO_THEOREM_NOT_CLOSED",
            "no Cassini pass from residual zero yet",
        ),
        (
            "RUN1954_2_residual_bound",
            "abs(S_TF_extra) <= ||W_STF||_1 residual l=2 envelopes",
            "bound <= 6.7e-5",
            "MISSING_RESIDUAL_L2_ENVELOPES;MISSING_W_STF",
            "BLOCKED_MISSING_BOUND_FACTORS",
            "finite residual bound not scoreable yet",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, prediction, acceptance_rule, missing_inputs, runner_status, consequence in entries:
        row = base(row_id)
        row.update(
            {
                "prediction": prediction,
                "acceptance_rule": acceptance_rule,
                "missing_inputs": missing_inputs,
                "runner_status": runner_status,
                "consequence": consequence,
            }
        )
        rows.append(row)
    return rows


def claim_gate_rows() -> list[dict[str, object]]:
    entries = [
        (
            "CG1954_0_baseline_split",
            "GR l=2 baseline is separated from extra MTS residual.",
            "PASS_NONCLAIM",
            "scope guard only; not a physical pass",
        ),
        (
            "CG1954_1_same_source_map",
            "Parent local action has same source map as EH/GR for ordinary matter.",
            "FAIL_BLOCKED",
            "not parent-signed here",
        ),
        (
            "CG1954_2_no_extra_boundary_dof",
            "Extra MTS branch has no independent l=2 boundary data.",
            "FAIL_BLOCKED",
            "boundary uniqueness/decay theorem missing",
        ),
        (
            "CG1954_3_residual_l2_zero",
            "Residual l=2 MTS slip vanishes.",
            "FAIL_BLOCKED",
            "same-source, boundary, and source-silence clauses missing",
        ),
        (
            "CG1954_4_residual_l2_bound",
            "Residual l=2 MTS slip is finite and below Cassini policy.",
            "FAIL_BLOCKED",
            "residual envelopes and W_STF missing",
        ),
        (
            "CG1954_5_Cassini_pass",
            "MTS passes Cassini gamma.",
            "FAIL_BLOCKED",
            "baseline split exists but residual zero/bound does not",
        ),
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
            "DEC1954_0_progress",
            "GR_BASELINE_SUBTRACTION_INSERTED",
            "we no longer confuse real GR source/boundary multipoles with extra MTS slip",
            "prove local same-source EH reduction for residual l=2",
        ),
        (
            "DEC1954_1_best_next",
            "EH_SAME_SOURCE_MAP_OR_RESIDUAL_BOUND",
            "if MTS local action has the same matter/source map as EH and no extra boundary dof, inherited l=2 residual vanishes",
            "target parent local EH-core source-map theorem before external readout-norm work",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, decision, reason, next_action in entries:
        row = base(row_id)
        row.update({"decision": decision, "reason": reason, "next_action": next_action})
        rows.append(row)
    return rows


def next_rows() -> list[dict[str, object]]:
    row = base("NEXT1954_0_primary")
    row.update(
        {
            "priority": "selected",
            "target_doc": "1955-Y5-R2FR-local-EH-same-source-map-or-residual-l2-bound.md",
            "target_script": "scripts/Y5_R2FR_local_EH_same_source_map_or_residual_l2_bound_1955.py",
            "objective": "prove the local EH same-source map/no-extra-boundary condition for residual l=2, or fill residual l=2 envelope rows",
            "acceptance_output": "same-source theorem clauses or conservative residual l=2 bounds",
            "nonclaim_rule": "no Cassini/local-GR claim until residual S_TF is zero or bounded below policy",
        }
    )
    return [row]


def snapshot_rows() -> list[dict[str, object]]:
    row = base("SNAP1954_0_project_position")
    row.update(
        {
            "strongest_result": "The l=2 problem is now fairly framed as extra residual slip beyond the GR baseline.",
            "what_improved": "real solar-system multipoles no longer falsely count against MTS if local EH source-map equivalence holds",
            "still_missing": "parent same-source map, no-extra-boundary-dof theorem, source-silent extra sector, or residual l=2 envelopes",
            "claim_status": "not a Cassini/local-GR pass; a sharper bridge toward GR reduction",
        }
    )
    return [row]


OUTPUTS = {
    "source_register": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1954_SOURCE_REGISTER.csv",
    "residual_split": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1954_L2_RESIDUAL_SPLIT.csv",
    "residual_inputs": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1954_RESIDUAL_L2_INPUT_LEDGER.csv",
    "runner": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1954_RUNNER_UPDATE.csv",
    "claim_gate": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1954_CLAIM_GATE.csv",
    "decision": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1954_DECISION_LEDGER.csv",
    "next": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1954_NEXT_TARGET.csv",
    "snapshot": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1954_PROJECT_STATUS_SNAPSHOT.csv",
    "source_weight": SOURCE_WEIGHT_DOCS / "L2_BASELINE_SUBTRACTION_1954_NONCLAIM.csv",
    "queue": RAB_QUEUE / "JR1954_EH_SAME_SOURCE_MAP_OR_RESIDUAL_L2_BOUND_QUEUE.csv",
}


def build_tables() -> dict[str, list[dict[str, object]]]:
    source_weight = [
        {
            **base("SW1954_0_nonclaim_weight"),
            "artifact": "1954 l=2 GR-baseline residual split",
            "weight": "SCOPE_GUARD_NOT_EVIDENCE",
            "reason": "fair comparison structure improved, but no residual zero/bound is proved",
        }
    ]
    queue = [
        {
            **base("AQ1954_0_same_source_map"),
            "target": "local EH same-source map",
            "needed_inputs": "parent local action; EH core variation; ordinary matter coupling descent; extra-sector source silence",
            "priority": "HIGH",
        },
        {
            **base("AQ1954_1_no_extra_boundary"),
            "target": "no independent residual l=2 boundary data",
            "needed_inputs": "local matching condition; decaying branch; boundary uniqueness theorem",
            "priority": "HIGH",
        },
    ]
    return {
        "source_register": source_register(),
        "residual_split": residual_split_rows(),
        "residual_inputs": residual_input_rows(),
        "runner": runner_rows(),
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
    patterns = ("1954-", "*_1954_*", "*Y5*1954*", "*VAL1954*", "*P8*1954*")
    return sum(1 for path in FORMALIZATION.rglob("*") if any(Path(path.name).match(pattern) for pattern in patterns))


def validate(tables: dict[str, list[dict[str, object]]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    sources_ok = all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in tables["source_register"])
    rows.append(validation_row("VAL1954_00_sources", "PASS" if sources_ok else "FAIL", "all source files exist and needles found"))

    baseline_ok = any(row["row_id"] == "L2R1954_0_baseline_subtraction" and row["status"] == "BASELINE_SPLIT_BUILT_NONCLAIM" for row in tables["residual_split"])
    rows.append(validation_row("VAL1954_01_baseline_split", "PASS" if baseline_ok else "FAIL", "GR baseline subtraction recorded"))

    same_source_ok = any(row["row_id"] == "L2R1954_1_same_source_map_condition" and row["status"] == "CONDITION_SHARPENED_NOT_SIGNED" for row in tables["residual_split"])
    rows.append(validation_row("VAL1954_02_same_source_condition", "PASS" if same_source_ok else "FAIL", "same-source map condition recorded"))

    inputs_ok = {"Delta J_2^MTS", "Delta h_boundary2^MTS", "Delta J_source2^MTS"}.issubset({row["symbol"] for row in tables["residual_inputs"]})
    rows.append(validation_row("VAL1954_03_residual_inputs", "PASS" if inputs_ok else "FAIL", "residual l=2 inputs explicit"))

    runner_statuses = {row["runner_status"] for row in tables["runner"]}
    runner_ok = {"PASS_NONCLAIM_SCOPE_GUARD", "BLOCKED_ZERO_THEOREM_NOT_CLOSED", "BLOCKED_MISSING_BOUND_FACTORS"}.issubset(runner_statuses)
    rows.append(validation_row("VAL1954_04_runner", "PASS" if runner_ok else "FAIL", "runner separates scope guard from blocked claims"))

    gate_ok = any(row["row_id"] == "CG1954_0_baseline_split" and row["status"] == "PASS_NONCLAIM" for row in tables["claim_gate"]) and all(
        row["status"] != "PASS_CLAIM" for row in tables["claim_gate"]
    )
    rows.append(validation_row("VAL1954_05_claim_gates", "PASS" if gate_ok else "FAIL", "only baseline scope guard passes nonclaim"))

    decision_ok = any(row["decision"] == "EH_SAME_SOURCE_MAP_OR_RESIDUAL_BOUND" for row in tables["decision"])
    rows.append(validation_row("VAL1954_06_decision", "PASS" if decision_ok else "FAIL", "EH same-source map selected"))

    next_ok = tables["next"][0]["target_doc"] == "1955-Y5-R2FR-local-EH-same-source-map-or-residual-l2-bound.md"
    rows.append(validation_row("VAL1954_07_next_target", "PASS" if next_ok else "FAIL", "1955 target selected"))

    flags_ok = all(not bool(row.get("valid_for_claim")) and not bool(row.get("public_claim")) for table in tables.values() for row in table)
    rows.append(validation_row("VAL1954_08_claim_flags_safe", "PASS" if flags_ok else "FAIL", "claim flags all false"))

    csv_ok = all(bool(read_csv(path)) for path in OUTPUTS.values())
    rows.append(validation_row("VAL1954_09_csv_parse", "PASS" if csv_ok else "FAIL", "all generated CSVs parse with rows"))

    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    rows.append(validation_row("VAL1954_10_pycache_absent", "PASS" if not pycache.exists() else "FAIL", "scripts __pycache__ absent"))

    count = formalization_hits()
    rows.append(validation_row("VAL1954_11_formalization_untouched", "PASS" if count == 0 else "FAIL", f"formalization_1954_artifact_count={count}"))

    overall = "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL"
    rows.append(validation_row("VAL1954_OVERALL", overall, "1954 l2 source boundary zero or envelope"))
    return rows


def markdown_table(rows: list[dict[str, object]]) -> str:
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    lines = ["| " + " | ".join(fields) + " |", "| " + " | ".join("---" for _ in fields) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(field, "")).replace("\n", " ") for field in fields) + " |")
    return "\n".join(lines)


def write_markdown(tables: dict[str, list[dict[str, object]]], validation_rows: list[dict[str, object]]) -> None:
    sections = [
        ("Source Register", tables["source_register"]),
        ("L2 Residual Split", tables["residual_split"]),
        ("Residual L2 Input Ledger", tables["residual_inputs"]),
        ("Runner Update", tables["runner"]),
        ("Claim Gate", tables["claim_gate"]),
        ("Decision Ledger", tables["decision"]),
        ("Next Target", tables["next"]),
        ("Project Status Snapshot", tables["snapshot"]),
        ("Validation", validation_rows),
    ]
    lines = [
        "# 1954 Y5 R2FR: L2 Source Boundary Zero Or Envelope",
        "",
        "Private checkpoint. This prevents an unfair comparison mistake: real solar-system l=2 multipoles belong to the GR baseline unless the MTS parent action creates extra residual l=2 slip.",
        "",
        "Result: the problem is reframed as `Delta B_2^MTS`, the extra residual after GR baseline subtraction. The zero route now requires a local EH same-source map, no independent extra boundary l=2 degree of freedom, and source-silent extra sector. These are not yet parent-signed.",
        "",
    ]
    for title, rows in sections:
        lines.extend([f"## {title}", "", markdown_table(rows), ""])
    DOC_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    ensure_dirs()
    tables = build_tables()
    for name, path in OUTPUTS.items():
        write_csv(path, tables[name])
    validation_rows = validate(tables)
    write_csv(VALIDATION_PATH, validation_rows)
    write_markdown(tables, validation_rows)
    overall = validation_rows[-1]["status"]
    print(f"wrote {DOC_PATH}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"VAL1954_OVERALL={overall}")
    return 0 if overall == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
