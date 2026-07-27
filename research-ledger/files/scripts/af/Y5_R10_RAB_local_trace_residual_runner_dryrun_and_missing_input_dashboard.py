from __future__ import annotations

import csv
import shutil
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


STARTED = datetime.now(timezone.utc)
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
BRANCH_ROOT = ROOT / "source-intake" / "microscope" / "branch_locked_wep"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1435-Y5-R10-RAB-local-trace-residual-runner-dryrun-and-missing-input-dashboard.md"
BRANCH_ID_FILE = BRANCH_ROOT / "branch_id.csv"
RESIDUAL_SCHEMA_FILE = BRANCH_ROOT / "residuals" / "local_trace_residual_source_pack_schema.csv"
BOUND_MAP_FILE = BRANCH_ROOT / "residuals" / "local_trace_bound_map.csv"
DRYRUN_DASHBOARD_FILE = BRANCH_ROOT / "residuals" / "local_trace_residual_dryrun_dashboard.csv"
MISSING_MATRIX_FILE = BRANCH_ROOT / "residuals" / "local_trace_missing_input_matrix.csv"

SOURCE_REGISTER = OUT / "P8_Y5_R10_1435_SOURCE_REGISTER.csv"
SCHEMA_PARSE_AUDIT = OUT / "P8_Y5_R10_1435_SCHEMA_PARSE_AUDIT.csv"
ARENA_DRYRUN_DASHBOARD = OUT / "P8_Y5_R10_1435_ARENA_DRYRUN_DASHBOARD.csv"
MISSING_INPUT_MATRIX = OUT / "P8_Y5_R10_1435_MISSING_INPUT_MATRIX.csv"
BRANCH_ID_AUDIT = OUT / "P8_Y5_R10_1435_BRANCH_ID_AUDIT.csv"
RUNNER_REFUSAL = OUT / "P8_Y5_R10_1435_RUNNER_REFUSAL_STATUS.csv"
CLAIM_GATE = OUT / "P8_Y5_R10_1435_CLAIM_GATE.csv"
DECISION_LEDGER = OUT / "P8_Y5_R10_1435_DECISION_LEDGER.csv"
NEXT_TARGET = OUT / "P8_Y5_R10_1435_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1435_VALIDATION.csv"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def clean(value: Any) -> str:
    return str(value).replace("\n", " ").replace("\r", " ").strip()


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows supplied for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: clean(row.get(key, "")) for key in fieldnames})


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def text_has(path: Path, needle: str) -> bool:
    if not path.exists():
        return False
    return needle in path.read_text(encoding="utf-8", errors="ignore")


def md_cell(value: Any) -> str:
    return clean(value).replace("|", "\\|")


def md_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    headers = list(rows[0].keys())
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(md_cell(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


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


def branch_id() -> str:
    rows = read_csv(BRANCH_ID_FILE)
    if len(rows) != 1:
        raise ValueError(f"expected one branch row, got {len(rows)}")
    value = rows[0].get("same_parent_branch_id", "").strip()
    if not value:
        raise ValueError("same_parent_branch_id missing")
    return value


def source_register_rows(branch: str) -> list[dict[str, Any]]:
    specs = [
        ("SRC1435_0_1434_next", OUT / "P8_Y5_R10_1434_NEXT_TARGET.csv", "NEXT1434_0_1435", "1434 handoff selecting dry-run dashboard."),
        ("SRC1435_1_1434_validation", OUT / "P8_Y5_BRR545_1434_VALIDATION.csv", "VAL1434_9_overall", "1434 validation summary."),
        ("SRC1435_2_branch_id", BRANCH_ID_FILE, branch, "branch lock row."),
        ("SRC1435_3_schema_file", RESIDUAL_SCHEMA_FILE, "projection_matrix_id", "branch-locked residual source-pack schema."),
        ("SRC1435_4_bound_map_file", BOUND_MAP_FILE, "ABM1434_4_ORBITAL_NEWTON", "branch-locked local trace bound map."),
        ("SRC1435_5_components", OUT / "P8_Y5_R10_1434_RESIDUAL_COMPONENTS.csv", "LTRC1434_4_source_normalization", "residual components."),
        ("SRC1435_6_inputs", OUT / "P8_Y5_R10_1434_REQUIRED_INPUTS_LEDGER.csv", "REQ1434_1_projection_matrices", "required input ledger."),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, anchor, role in specs:
        rows.append(
            {
                "source_id": source_id,
                "source_path": str(path),
                "path_exists": path.exists(),
                "anchor": anchor,
                "anchor_found": text_has(path, anchor),
                "role": role,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def schema_parse_audit_rows(branch: str, schema_rows: list[dict[str, str]], bound_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    schema_fields = {row.get("schema_field", "") for row in schema_rows}
    required_schema_fields = {
        "same_parent_branch_id",
        "residual_component",
        "coefficient_symbol",
        "value_or_bound",
        "units",
        "projection_matrix_id",
        "arena",
        "source_path",
        "parent_status",
        "valid_for_claim",
        "claim_allowed",
    }
    bound_branch_values = sorted({row.get("same_parent_branch_id", "") for row in bound_rows})
    return [
        {
            "audit_id": "SPA1435_0_schema_exists",
            "target_path": str(RESIDUAL_SCHEMA_FILE),
            "result": "PASS" if RESIDUAL_SCHEMA_FILE.exists() else "FAIL",
            "detail": "schema file exists",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "SPA1435_1_schema_fields",
            "target_path": str(RESIDUAL_SCHEMA_FILE),
            "result": "PASS" if required_schema_fields.issubset(schema_fields) else "FAIL",
            "detail": "all required dry-run schema fields present",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "SPA1435_2_bound_map_exists",
            "target_path": str(BOUND_MAP_FILE),
            "result": "PASS" if BOUND_MAP_FILE.exists() else "FAIL",
            "detail": "bound map file exists",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "SPA1435_3_bound_map_branch",
            "target_path": str(BOUND_MAP_FILE),
            "result": "PASS" if bound_branch_values == [branch] else "FAIL",
            "detail": ";".join(bound_branch_values),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def missing_input_matrix_rows(bound_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for bound_row in bound_rows:
        missing_parts = [part.strip() for part in bound_row.get("missing_inputs", "").split(";") if part.strip()]
        for index, missing_input in enumerate(missing_parts):
            rows.append(
                {
                    "same_parent_branch_id": bound_row["same_parent_branch_id"],
                    "matrix_id": f"MIM1435_{len(rows)}",
                    "arena_id": bound_row["arena_id"],
                    "arena": bound_row["arena"],
                    "observable": bound_row["observable"],
                    "missing_input": missing_input,
                    "required_projection": bound_row["required_projection"],
                    "source_status": bound_row["source_status"],
                    "runner_effect": "BLOCKS_SCORE",
                    "valid_for_claim": False,
                    "claim_allowed": False,
                }
            )
    return rows


def arena_dashboard_rows(bound_rows: list[dict[str, str]], missing_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    missing_counts = Counter(row["arena_id"] for row in missing_rows)
    rows: list[dict[str, Any]] = []
    for bound_row in bound_rows:
        rows.append(
            {
                "same_parent_branch_id": bound_row["same_parent_branch_id"],
                "dashboard_id": f"DRY1435_{len(rows)}",
                "arena_id": bound_row["arena_id"],
                "arena": bound_row["arena"],
                "observable": bound_row["observable"],
                "bound_source_anchor": bound_row["bound_source_anchor"],
                "source_status": bound_row["source_status"],
                "missing_input_count": missing_counts[bound_row["arena_id"]],
                "score_status": "REFUSED_MISSING_INPUTS",
                "first_next_action": "derive_or_source_projection_matrix_before_numeric_score",
                "valid_prediction_row": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def branch_id_audit_rows(branch: str, schema_rows: list[dict[str, str]], bound_rows: list[dict[str, str]], dashboard_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    targets = [
        ("BIA1435_0_branch_id", read_csv(BRANCH_ID_FILE)),
        ("BIA1435_1_schema", schema_rows),
        ("BIA1435_2_bound_map", bound_rows),
        ("BIA1435_3_dashboard", dashboard_rows),
    ]
    rows: list[dict[str, Any]] = []
    for audit_id, parsed in targets:
        values = sorted({row.get("same_parent_branch_id", "") for row in parsed if row.get("same_parent_branch_id")})
        rows.append(
            {
                "audit_id": audit_id,
                "branch_values": ";".join(values),
                "result": "PASS" if values == [branch] else "FAIL",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def write_dashboard_files(dashboard: list[dict[str, Any]], missing: list[dict[str, Any]]) -> None:
    write_csv(DRYRUN_DASHBOARD_FILE, dashboard)
    write_csv(MISSING_MATRIX_FILE, missing)


def runner_refusal_rows(dashboard: list[dict[str, Any]], missing: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "runner_id": "RUN1435_0_dryrun",
            "target": "local trace residual runner dry-run",
            "input_status": f"{len(dashboard)}_arenas_parsed_{len(missing)}_missing_inputs",
            "runner_status": "REFUSE_NUMERIC_SCORE",
            "score_ready": False,
            "reason": "every arena has missing projection/source inputs",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "runner_id": "RUN1435_1_claim_policy",
            "target": "claim promotion",
            "input_status": "SCHEMA_ONLY",
            "runner_status": "NO_CLAIM_NO_LOCAL_GR",
            "score_ready": False,
            "reason": "dry-run dashboard is a gap report, not evidence of a residual passing bounds",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "CG1435_0_dryrun_dashboard",
            "claim_component": "dry-run dashboard",
            "gate_pass": True,
            "claim_allowed": False,
            "reason": "dashboard exists but reports missing inputs",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1435_1_numeric_residual_score",
            "claim_component": "numeric residual score",
            "gate_pass": False,
            "claim_allowed": False,
            "reason": "no arena has complete projection/source inputs",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1435_2_local_GR",
            "claim_component": "local-GR/Newton reduction",
            "gate_pass": False,
            "claim_allowed": False,
            "reason": "local trace residual branch remains active and unbounded",
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC1435_0_dashboard",
            "decision": "write executable missing-input dashboard",
            "because": "future testing should know exactly which projection/source input blocks each arena",
            "effect": "residual branch is now dry-run auditable without long computation",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1435_1_no_numeric_run",
            "decision": "refuse numeric scoring",
            "because": "the dashboard finds no complete arena row",
            "effect": "no accidental local-GR or residual-bound pass",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1435_2_next",
            "decision": "select the first projection matrix target",
            "because": "projection matrices are the common bottleneck across arenas",
            "effect": "1436 should prioritize P_WEP/P_R10/P_PPN with a branch-locked first-row contract",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT1435_0_1436",
            "next_target": "1436-Y5-R10-RAB-first-projection-matrix-target-selection-and-row-contract.md",
            "script": "scripts/Y5_R10_RAB_first_projection_matrix_target_selection_and_row_contract.py",
            "objective": "choose the first residual-to-observable projection matrix target and write a branch-locked row contract, likely comparing P_WEP, P_R10, and P_PPN by leverage and missing inputs.",
            "include": "priority ranking; projection-row schema; first target contract; anti-claim gates",
            "exclude": "numeric scoring; fitted coupling; local-GR claim; formalization edits; GitHub",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def validation_rows(
    sources: list[dict[str, Any]],
    schema_audit: list[dict[str, Any]],
    dashboard: list[dict[str, Any]],
    missing: list[dict[str, Any]],
    branch_audit: list[dict[str, Any]],
    claims: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    csvs = [
        SOURCE_REGISTER,
        SCHEMA_PARSE_AUDIT,
        ARENA_DRYRUN_DASHBOARD,
        MISSING_INPUT_MATRIX,
        BRANCH_ID_AUDIT,
        RUNNER_REFUSAL,
        CLAIM_GATE,
        DECISION_LEDGER,
        NEXT_TARGET,
        DRYRUN_DASHBOARD_FILE,
        MISSING_MATRIX_FILE,
    ]
    parse_ok = True
    parse_errors: list[str] = []
    truthy_claim_flags: list[str] = []
    for path in csvs:
        try:
            rows = read_csv(path)
        except Exception as exc:
            parse_ok = False
            parse_errors.append(f"{path.name}:{type(exc).__name__}")
            continue
        for index, row in enumerate(rows, start=2):
            for key in ("claim_allowed", "valid_for_claim", "valid_prediction_row"):
                if (row.get(key) or "").strip().lower() == "true":
                    truthy_claim_flags.append(f"{path.name}:{index}:{key}=true")
    sources_ok = all(row["path_exists"] and row["anchor_found"] for row in sources)
    schema_ok = all(row["result"] == "PASS" for row in schema_audit)
    branch_ok = all(row["result"] == "PASS" for row in branch_audit)
    dashboard_written = DRYRUN_DASHBOARD_FILE.exists() and len(read_csv(DRYRUN_DASHBOARD_FILE)) == len(dashboard)
    matrix_written = MISSING_MATRIX_FILE.exists() and len(read_csv(MISSING_MATRIX_FILE)) == len(missing)
    all_refused = all(row["score_status"] == "REFUSED_MISSING_INPUTS" for row in dashboard)
    claims_safe = all(str(row.get("claim_allowed")).lower() == "false" for row in claims) and not truthy_claim_flags
    formalization_count = count_formalization_modified_since_start()
    checks = [
        ("VAL1435_0_sources", sources_ok, "all 1435 cited source paths and anchors resolve"),
        ("VAL1435_1_schema_parse", schema_ok, "schema and bound-map parse audits pass"),
        ("VAL1435_2_branch_audit", branch_ok, "all parsed rows share one branch id"),
        ("VAL1435_3_dashboard_files", dashboard_written and matrix_written, "dashboard and missing-input matrix files written"),
        ("VAL1435_4_all_refused", all_refused and len(missing) > 0, "all arenas refuse scoring with visible missing inputs"),
        ("VAL1435_5_claim_gates", claims_safe, "all claim/valid/prediction flags remain false"),
        ("VAL1435_6_csv_parse", parse_ok, "all generated 1435 CSVs parse cleanly" if parse_ok else ";".join(parse_errors)),
        ("VAL1435_7_formalization_untouched", formalization_count == 0, f"formalization modified-file count since start={formalization_count}"),
        ("VAL1435_8_next_target", True, "1436 handoff written"),
    ]
    rows = [
        {
            "check_id": check_id,
            "result": "PASS" if passed else "FAIL",
            "detail": detail,
            "generated_utc": stamp(),
        }
        for check_id, passed, detail in checks
    ]
    rows.append(
        {
            "check_id": "VAL1435_9_overall",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1435 dry-run dashboard parses local trace residual maps and refuses all numeric claims",
            "generated_utc": stamp(),
        }
    )
    return rows


def write_doc(sections: dict[str, list[dict[str, Any]]]) -> None:
    content = "\n\n".join(
        [
            "# 1435 - Local trace residual runner dry-run and missing-input dashboard",
            "**Current verdict:** the dry-run runner parses the local trace residual schema and bound map, then refuses every arena because projection/source inputs remain missing.",
            "**Main progress:** the active residual branch now has an executable missing-input dashboard and matrix, so future testing can target the bottleneck rows instead of guessing.",
            "## Source register\n" + md_table(sections["sources"]),
            "## Schema parse audit\n" + md_table(sections["schema_audit"]),
            "## Arena dry-run dashboard\n" + md_table(sections["dashboard"]),
            "## Missing input matrix\n" + md_table(sections["missing"]),
            "## Branch id audit\n" + md_table(sections["branch_audit"]),
            "## Runner refusal status\n" + md_table(sections["runner"]),
            "## Claim gates\n" + md_table(sections["claims"]),
            "## Decision ledger\n" + md_table(sections["decisions"]),
            "## Validation\n" + md_table(sections["validation"]),
            "## Next target\n" + md_table(sections["next"]),
        ]
    )
    DOC.write_text(content + "\n", encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    branch = branch_id()
    sources = source_register_rows(branch)
    schema_rows = read_csv(RESIDUAL_SCHEMA_FILE)
    bound_rows = read_csv(BOUND_MAP_FILE)
    schema_audit = schema_parse_audit_rows(branch, schema_rows, bound_rows)
    missing = missing_input_matrix_rows(bound_rows)
    dashboard = arena_dashboard_rows(bound_rows, missing)
    branch_audit = branch_id_audit_rows(branch, schema_rows, bound_rows, dashboard)
    write_dashboard_files(dashboard, missing)
    runner = runner_refusal_rows(dashboard, missing)
    claims = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(SCHEMA_PARSE_AUDIT, schema_audit)
    write_csv(ARENA_DRYRUN_DASHBOARD, dashboard)
    write_csv(MISSING_INPUT_MATRIX, missing)
    write_csv(BRANCH_ID_AUDIT, branch_audit)
    write_csv(RUNNER_REFUSAL, runner)
    write_csv(CLAIM_GATE, claims)
    write_csv(DECISION_LEDGER, decisions)
    write_csv(NEXT_TARGET, next_rows)

    validation = validation_rows(sources, schema_audit, dashboard, missing, branch_audit, claims)
    write_csv(VALIDATION, validation)
    write_doc(
        {
            "sources": sources,
            "schema_audit": schema_audit,
            "dashboard": dashboard,
            "missing": missing,
            "branch_audit": branch_audit,
            "runner": runner,
            "claims": claims,
            "decisions": decisions,
            "validation": validation,
            "next": next_rows,
        }
    )
    remove_pycache()
    print("Y5_R10_1435_local_trace_residual_dryrun_dashboard_refuses_all_nonclaim")


if __name__ == "__main__":
    main()
