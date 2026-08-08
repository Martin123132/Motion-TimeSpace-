from __future__ import annotations

import csv
import math
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_GK_STRESS_BOUND_RUNNER_DRY_RUN_AND_PLACEHOLDER_REJECTION_2474"
CHECKPOINT_ID = "2474"

ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

DOC = ROOT / "2474-Y5-R2FR-GK-stress-bound-runner-dry-run-and-placeholder-rejection.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_GK_BOUND_RUNNER_2474_SOURCE_REGISTER.csv",
    "dry_run_inputs": OUT / "P8_Y5_GK_BOUND_RUNNER_2474_DRY_RUN_INPUTS.csv",
    "dry_run_results": OUT / "P8_Y5_GK_BOUND_RUNNER_2474_DRY_RUN_RESULTS.csv",
    "rejection_ledger": OUT / "P8_Y5_GK_BOUND_RUNNER_2474_REJECTION_LEDGER.csv",
    "toy_arithmetic": OUT / "P8_Y5_GK_BOUND_RUNNER_2474_TOY_ARITHMETIC_SMOKE.csv",
    "claim_gates": OUT / "P8_Y5_GK_BOUND_RUNNER_2474_CLAIM_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_GK_BOUND_RUNNER_2474_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_GK_BOUND_RUNNER_2474_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_GK_BOUND_RUNNER_2474_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2474_VALIDATION.csv",
}

COPY_TARGETS = {
    "dry_run_results": LOCAL_BOUNDS / "GK_stress_bound_runner_dry_run_results_2474_NONCLAIM.csv",
    "rejection_ledger": LOCAL_BOUNDS / "GK_stress_bound_runner_rejection_ledger_2474_NONCLAIM.csv",
    "claim_gate_copy": QUEUE / "JR2474_GK_STRESS_BOUND_CLAIM_GATES_NONCLAIM.csv",
}

SOURCES = [
    {
        "source_id": "SRC2474_00_2473_doc",
        "source_path": ROOT / "2473-Y5-R2FR-GK-stress-bound-local-arena-projection-runner.md",
        "needles": ["SCHEMA2473_3_block_rule", "NEXT2473_0_selected", "VAL2473_OVERALL"],
        "role": "handoff selecting dry-run placeholder rejection runner",
    },
    {
        "source_id": "SRC2474_01_2473_schema",
        "source_path": OUT / "P8_Y5_GK_STRESS_BOUND_2473_NONCLAIM_RUNNER_SCHEMA.csv",
        "needles": ["SCHEMA2473_1_prediction", "SCHEMA2473_3_block_rule", "SCHEMA2473_4_no_shortcuts"],
        "role": "runner schema and guardrails",
    },
    {
        "source_id": "SRC2474_02_2473_arenas",
        "source_path": OUT / "P8_Y5_GK_STRESS_BOUND_2473_ARENA_PROJECTION_ROWS.csv",
        "needles": ["ARENA2473_R10", "ARENA2473_PPN", "valid_for_claim=false"],
        "role": "arena projection schema",
    },
    {
        "source_id": "SRC2474_03_2473_missing",
        "source_path": OUT / "P8_Y5_GK_STRESS_BOUND_2473_MISSING_COEFFICIENT_LEDGER.csv",
        "needles": ["MISS2473_5_Cmetric", "MISSING_ARENA_PROJECTION", "MISSING_BOUND_DATA"],
        "role": "missing coefficient ledger",
    },
]


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base_row() -> dict[str, Any]:
    return {"timestamp_utc": stamp(), "branch_id": BRANCH_ID, "checkpoint_id": CHECKPOINT_ID, "valid_for_claim": False, "claim_allowed": False}


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    columns: list[str] = []
    for row in rows:
        for key in row:
            if key not in columns:
                columns.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def source_register() -> list[dict[str, Any]]:
    rows = []
    for source in SOURCES:
        path = Path(source["source_path"])
        exists = path.exists()
        missing: list[str] = []
        if exists:
            text = read_text(path)
            missing = [needle for needle in source["needles"] if needle not in text]
        else:
            missing = list(source["needles"])
        rows.append({**base_row(), "source_id": source["source_id"], "source_path": str(path), "exists": exists, "missing_needles": ";".join(missing), "source_pass": exists and not missing, "role": source["role"]})
    return rows


def dry_run_input_rows() -> list[dict[str, Any]]:
    rows = [
        ("DRY2474_0_R10_missing", "R10_short_range", "", "", "", "", "alpha_bound", "", "false", "MISSING_COEFFICIENTS", "none"),
        ("DRY2474_1_PPN_toy_nonclaim", "PPN_solar_system", "1.0e-12", "2.0", "3.0", "1.0e-10", "dimensionless", "toy_internal", "false", "TOY_NUMERIC_NONCLAIM", "none"),
        ("DRY2474_2_CLOCK_bad_units", "clock_redshift_time", "1.0e-12", "1.0", "1.0", "1.0e-15", "banana_units", "toy_internal", "false", "BAD_UNITS", "none"),
        ("DRY2474_3_ORBITAL_fitted_GM", "orbital_dynamics", "1.0e-13", "1.0", "1.0", "1.0e-12", "dimensionless", "toy_internal", "false", "FITTED_GM_FORBIDDEN", "uses_fitted_GM"),
        ("DRY2474_4_WEP_future_shape", "WEP_composition", "2.0e-15", "4.0", "5.0", "1.0e-12", "dimensionless", "future_source_required", "false", "FUTURE_SHAPE_NONCLAIM", "none"),
    ]
    return [
        {
            **base_row(),
            "input_id": i,
            "arena": arena,
            "E_GK_bound": egk,
            "C_metric": cmetric,
            "K_arena": karena,
            "arena_bound": bound,
            "units": units,
            "source_path": source,
            "valid_for_claim": valid,
            "input_status": status,
            "forbidden_marker": forbidden,
        }
        for i, arena, egk, cmetric, karena, bound, units, source, valid, status, forbidden in rows
    ]


def parse_float(value: str) -> float | None:
    if value == "":
        return None
    try:
        parsed = float(value)
    except ValueError:
        return None
    if not math.isfinite(parsed) or parsed < 0:
        return None
    return parsed


def evaluate_row(row: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any] | None, dict[str, Any] | None]:
    allowed_units = {"dimensionless", "alpha_bound", "fractional_frequency", "radian_per_orbit"}
    reasons: list[str] = []
    numeric_values = {field: parse_float(str(row[field])) for field in ["E_GK_bound", "C_metric", "K_arena", "arena_bound"]}
    if any(value is None for value in numeric_values.values()):
        reasons.append("MISSING_OR_INVALID_NUMERIC_INPUT")
    if row["units"] not in allowed_units:
        reasons.append("BAD_UNITS")
    if str(row["valid_for_claim"]).lower() != "true":
        reasons.append("VALID_FOR_CLAIM_FALSE")
    if str(row["source_path"]) in {"", "toy_internal", "future_source_required"}:
        reasons.append("MISSING_REAL_SOURCE_PATH")
    if row["forbidden_marker"] == "uses_fitted_GM":
        reasons.append("FITTED_GM_FORBIDDEN")

    residual = None
    ratio = None
    if not any(reason in reasons for reason in ["MISSING_OR_INVALID_NUMERIC_INPUT", "BAD_UNITS"]):
        residual = numeric_values["E_GK_bound"] * numeric_values["C_metric"] * numeric_values["K_arena"]
        ratio = residual / numeric_values["arena_bound"] if numeric_values["arena_bound"] else None

    result_status = "CLAIM_BLOCKED"
    if residual is not None and str(row["valid_for_claim"]).lower() != "true":
        result_status = "COMPUTED_TOY_NONCLAIM"
    if residual is not None and not reasons:
        result_status = "FUTURE_CLAIM_SHAPE_ONLY"

    result = {
        **base_row(),
        "input_id": row["input_id"],
        "arena": row["arena"],
        "residual_predicted": "" if residual is None else f"{residual:.6e}",
        "ratio_to_bound": "" if ratio is None else f"{ratio:.6e}",
        "result_status": result_status,
        "block_reasons": ";".join(reasons),
        "claim_allowed": False,
        "valid_for_claim": False,
    }
    rejection = None
    if reasons:
        rejection = {
            **base_row(),
            "input_id": row["input_id"],
            "arena": row["arena"],
            "rejection_reasons": ";".join(reasons),
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    toy = None
    if residual is not None:
        toy = {
            **base_row(),
            "input_id": row["input_id"],
            "arena": row["arena"],
            "calculation": "residual_predicted=E_GK_bound*C_metric*K_arena",
            "numeric_result": f"{residual:.6e}",
            "toy_only": True,
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    return result, rejection, toy


def dry_run_outputs(inputs: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    results: list[dict[str, Any]] = []
    rejections: list[dict[str, Any]] = []
    toy_rows: list[dict[str, Any]] = []
    for row in inputs:
        result, rejection, toy = evaluate_row(row)
        results.append(result)
        if rejection:
            rejections.append(rejection)
        if toy:
            toy_rows.append(toy)
    return results, rejections, toy_rows


def claim_gate_rows(results: list[dict[str, Any]], rejections: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = [
        ("GATE2474_0_dry_run", "Dry-run calculator executes.", "PASS", "results rows written", True, False),
        ("GATE2474_1_placeholder_rejection", "Placeholder/missing rows are rejected.", "PASS", f"{len(rejections)} rejection rows written", True, False),
        ("GATE2474_2_toy_arithmetic", "Toy numeric rows can compute but remain nonclaim.", "PASS", "computed rows have claim_allowed=false", True, False),
        ("GATE2474_3_claim_rows", "Any current row can support a local-test claim.", "BLOCKED", "all rows remain valid_for_claim=false or have missing inputs", False, False),
        ("GATE2474_4_local_GR", "local GR/PPN branch passes.", "BLOCKED", "stress-bound dry-run is compatibility plumbing only", False, False),
        ("GATE2474_5_no_GitHub", "No public/GitHub update.", "PASS_GUARDRAIL", "private dry-run only", True, False),
    ]
    return [{**base_row(), "gate_id": i, "claim": c, "gate_status": st, "reason": r, "gate_pass": gp, "claim_allowed": ca} for i, c, st, r, gp, ca in rows]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        ("DEC2474_0_runner_works", "Keep the stress-bound runner pattern.", "it computes toy rows and rejects placeholders", "ready for real coefficient acquisition"),
        ("DEC2474_1_no_claim", "No local compatibility claim.", "all current rows are nonclaim/missing", "claim discipline retained"),
        ("DEC2474_2_next", "Next acquire first real local arena coefficient source, preferably R10 or PPN.", "runner now has a schema to receive sourced rows", "2475 selected"),
    ]
    return [{**base_row(), "decision_id": i, "decision": d, "reason": r, "effect": e} for i, d, r, e in rows]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            **base_row(),
            "route_id": "NEXT2474_0_selected",
            "selection_status": "selected",
            "target_file": "2475-Y5-R2FR-first-real-local-arena-coefficient-source-acquisition.md",
            "target_script": "scripts/Y5_R2FR_first_real_local_arena_coefficient_source_acquisition_2475.py",
            "task": "try to source the first real coefficient/bound row for the stress-bound local runner, prioritizing R10 or PPN, while keeping all rows nonclaim unless coefficients, units and source paths are real",
            "acceptance_target": "source acquisition ledger, candidate real row or blocker, units validation, no fitted-GM guardrail, and claim gates",
            "guardrails": "no local-GR claim; no fitted GM; no M_H_ref reuse; no plateau axiom; no GitHub",
        }
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    for target in COPY_TARGETS.values():
        target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(OUTPUTS["dry_run_results"], COPY_TARGETS["dry_run_results"])
    shutil.copyfile(OUTPUTS["rejection_ledger"], COPY_TARGETS["rejection_ledger"])
    shutil.copyfile(OUTPUTS["claim_gates"], COPY_TARGETS["claim_gate_copy"])
    source_map = {
        "dry_run_results": OUTPUTS["dry_run_results"],
        "rejection_ledger": OUTPUTS["rejection_ledger"],
        "claim_gate_copy": OUTPUTS["claim_gates"],
    }
    return [{**base_row(), "copy_id": cid, "source_path": str(source_map[cid]), "target_path": str(target), "source_exists": source_map[cid].exists(), "target_exists": target.exists()} for cid, target in COPY_TARGETS.items()]


def csv_row_count(path: Path) -> int:
    with path.open(newline="", encoding="utf-8") as handle:
        return len(list(csv.DictReader(handle)))


def validation_rows(data: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, status: bool, notes: str, detail: str = "") -> None:
        rows.append({**base_row(), "check_id": check_id, "status": "PASS" if status else "FAIL", "notes": notes, "detail": detail})

    add("VAL2474_00_sources_exist", all(row["source_pass"] is True or str(row["source_pass"]) == "True" for row in data["sources"]), "all cited source paths exist and needles are present")
    add("VAL2474_01_inputs_written", len(data["inputs"]) >= 5, "dry-run inputs written")
    add("VAL2474_02_results_written", len(data["results"]) == len(data["inputs"]), "dry-run result rows written")
    add("VAL2474_03_rejections_written", len(data["rejections"]) >= 4, "placeholder/missing/bad rows rejected")
    add("VAL2474_04_toy_arithmetic", any(row["toy_only"] is True for row in data["toy"]), "toy arithmetic rows computed")
    add("VAL2474_05_all_nonclaim", all(row["claim_allowed"] is False or str(row["claim_allowed"]) == "False" for row in data["results"]), "all result rows claim-blocked")
    add("VAL2474_06_fitted_GM_rejected", any("FITTED_GM_FORBIDDEN" in row["rejection_reasons"] for row in data["rejections"]), "fitted GM row rejected")
    add("VAL2474_07_bad_units_rejected", any("BAD_UNITS" in row["rejection_reasons"] for row in data["rejections"]), "bad unit row rejected")
    add("VAL2474_08_claim_gates_safe", all(row["claim_allowed"] is False for row in data["gates"]), "no claim gate allows local-GR/PPN claim")
    add("VAL2474_09_next_target_written", bool(data["next"]) and data["next"][0]["route_id"] == "NEXT2474_0_selected", "2475 coefficient acquisition selected")
    add("VAL2474_10_branch_copies", all(row["source_exists"] and row["target_exists"] for row in data["copies"]), "nonclaim branch copies exist")
    markers = ("2474-Y5", "P8_Y5_GK_BOUND_RUNNER_2474", "P8_Y5_BRR545_2474", "JR2474")
    formal_hits = [path for path in FORMALIZATION.rglob("*") if path.is_file() and any(marker in path.name for marker in markers)] if FORMALIZATION.exists() else []
    add("VAL2474_11_no_formalization_artifacts", not formal_hits, "no 2474 artifacts were written to formalization-workbench", ";".join(str(path) for path in formal_hits))
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        try:
            count = csv_row_count(path)
            add(f"VAL2474_CSV_{path.stem}", count > 0, f"CSV parses with {count} rows", str(path))
        except Exception as exc:
            add(f"VAL2474_CSV_{path.stem}", False, f"CSV parse failed: {exc}", str(path))
    for copy_id, path in COPY_TARGETS.items():
        try:
            count = csv_row_count(path)
            add(f"VAL2474_COPY_CSV_{copy_id}", count > 0, f"copy CSV parses with {count} rows", str(path))
        except Exception as exc:
            add(f"VAL2474_COPY_CSV_{copy_id}", False, f"copy CSV parse failed: {exc}", str(path))
    add("VAL2474_OVERALL", all(row["status"] == "PASS" for row in rows), "2474 dry-run runner computes toy rows, rejects placeholders, and keeps stress-bound branch nonclaim")
    return rows


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(column, "")) for column in columns) + " |")
    return "\n".join(lines)


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    sections = [
        "# 2474 Y5 R2FR GK Stress-bound Runner Dry-run And Placeholder Rejection",
        "",
        "**Status:** dry-run runner works and blocks claims. Toy numeric rows compute, but every row remains nonclaim. Rows with missing coefficients, bad units or fitted-GM contamination are rejected by design.",
        "",
        "**Meaning:** the local stress-bound branch now has a test harness. It cannot claim compatibility yet, but it can safely receive real coefficient rows later without letting placeholders sneak into evidence.",
        "",
        "## Source Register",
        markdown_table(data["sources"], ["source_id", "source_path", "exists", "missing_needles", "source_pass", "role"]),
        "",
        "## Dry-run Inputs",
        markdown_table(data["inputs"], ["input_id", "arena", "E_GK_bound", "C_metric", "K_arena", "arena_bound", "units", "source_path", "valid_for_claim", "input_status", "forbidden_marker"]),
        "",
        "## Dry-run Results",
        markdown_table(data["results"], ["input_id", "arena", "residual_predicted", "ratio_to_bound", "result_status", "block_reasons", "claim_allowed"]),
        "",
        "## Rejection Ledger",
        markdown_table(data["rejections"], ["input_id", "arena", "rejection_reasons", "claim_allowed"]),
        "",
        "## Toy Arithmetic Smoke",
        markdown_table(data["toy"], ["input_id", "arena", "calculation", "numeric_result", "toy_only", "claim_allowed"]),
        "",
        "## Claim Gates",
        markdown_table(data["gates"], ["gate_id", "claim", "gate_status", "reason", "gate_pass", "claim_allowed"]),
        "",
        "## Decision Ledger",
        markdown_table(data["decisions"], ["decision_id", "decision", "reason", "effect"]),
        "",
        "## Next Target",
        markdown_table(data["next"], ["route_id", "selection_status", "target_file", "target_script", "task", "acceptance_target", "guardrails"]),
        "",
        "## Branch Copies",
        markdown_table(data["copies"], ["copy_id", "source_path", "target_path", "source_exists", "target_exists"]),
        "",
        "## Validation",
        markdown_table(data["validations"], ["check_id", "status", "notes", "detail"]),
        "",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    LOCAL_BOUNDS.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)
    inputs = dry_run_input_rows()
    results, rejections, toy = dry_run_outputs(inputs)
    data = {
        "sources": source_register(),
        "inputs": inputs,
        "results": results,
        "rejections": rejections,
        "toy": toy,
        "gates": claim_gate_rows(results, rejections),
        "decisions": decision_rows(),
        "next": next_target_rows(),
    }
    write_csv(OUTPUTS["source_register"], data["sources"])
    write_csv(OUTPUTS["dry_run_inputs"], data["inputs"])
    write_csv(OUTPUTS["dry_run_results"], data["results"])
    write_csv(OUTPUTS["rejection_ledger"], data["rejections"])
    write_csv(OUTPUTS["toy_arithmetic"], data["toy"])
    write_csv(OUTPUTS["claim_gates"], data["gates"])
    write_csv(OUTPUTS["decision_ledger"], data["decisions"])
    write_csv(OUTPUTS["next_target"], data["next"])
    data["copies"] = copy_branch_outputs()
    write_csv(OUTPUTS["branch_copies"], data["copies"])
    data["validations"] = validation_rows(data)
    write_csv(OUTPUTS["validation"], data["validations"])
    write_doc(data)
    print(f"wrote {DOC}")
    for key, path in OUTPUTS.items():
        print(f"wrote {key}: {path}")
    for key, path in COPY_TARGETS.items():
        print(f"copied {key}: {path}")


if __name__ == "__main__":
    main()
