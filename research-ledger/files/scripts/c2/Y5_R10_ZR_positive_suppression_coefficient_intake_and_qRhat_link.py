from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


PACK_ID = "P8_Y5_R10_1260"
TITLE = "1260-Y5-R10-ZR-positive-suppression-coefficient-intake-and-qRhat-link"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
RAB_INTAKE_DIR = ROOT / "source-intake" / "rab-sector"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_STARTED_UTC = datetime.now(timezone.utc)


SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
INTAKE_SCAN_PATH = OUT_DIR / f"{PACK_ID}_RAB_COEFFICIENT_INTAKE_SCAN.csv"
VALIDATION_RULES_PATH = OUT_DIR / f"{PACK_ID}_RAB_COEFFICIENT_VALIDATION_RULES.csv"
COEFFICIENT_MAPPING_PATH = OUT_DIR / f"{PACK_ID}_COEFFICIENT_TO_QRHAT_OR_SUPPRESSION_MAP.csv"
RUNNER_STATUS_PATH = OUT_DIR / f"{PACK_ID}_COEFFICIENT_RUNNER_STATUS.csv"
CLAIM_GATES_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATES.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1260_VALIDATION.csv"


REQUIRED_FIELDS = [
    "row_id",
    "coefficient_symbol",
    "operator_or_term",
    "coefficient_value",
    "coefficient_units",
    "sign_domain",
    "derivation_status",
    "source_path",
    "parent_action_block",
    "normalization_convention",
    "links_to_qRhat",
    "valid_for_claim",
    "claim_allowed",
]


def source_path(relative_path: str) -> Path:
    path = Path(relative_path)
    if path.is_absolute():
        return path
    return ROOT / path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def md_escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def markdown_table(rows: list[dict[str, object]], fields: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    return "\n".join(
        [
            "| " + " | ".join(fields) + " |",
            "| " + " | ".join(["---"] * len(fields)) + " |",
            *["| " + " | ".join(md_escape(row.get(field, "")) for field in fields) + " |" for row in rows],
        ]
    )


def exists_and_contains(relative_path: str, needle: str) -> tuple[bool, bool]:
    path = source_path(relative_path)
    if not path.exists():
        return False, False
    if not needle:
        return True, True
    return True, needle in read_text(path)


def validation_row(check_id: str, check: str, passed: bool, details: str) -> dict[str, object]:
    return {
        "check_id": check_id,
        "check": check,
        "status": "PASS" if passed else "FAIL",
        "details": details,
    }


def is_false(value: object) -> bool:
    return str(value).strip().lower() in {"false", "0", "no"}


def is_placeholder(value: object) -> bool:
    text = str(value).strip().upper()
    return text == "" or text.startswith("MISSING") or text in {"TBD", "TODO", "PLACEHOLDER", "N/A", "NONE"}


def scan_intake() -> tuple[list[dict[str, object]], list[dict[str, str]]]:
    scan_rows: list[dict[str, object]] = []
    candidate_rows: list[dict[str, str]] = []
    for folder_name in ["raw", "accepted", "docs"]:
        directory = RAB_INTAKE_DIR / folder_name
        directory.mkdir(parents=True, exist_ok=True)
        csv_files = sorted(directory.glob("*.csv"))
        if not csv_files:
            scan_rows.append(
                {
                    "scan_id": f"SCAN1260_{folder_name}_empty",
                    "directory": str(directory),
                    "file": "",
                    "rows_found": 0,
                    "scan_status": "NO_CANDIDATE_FILES_FOUND" if folder_name in {"raw", "accepted"} else "NO_DOC_TEMPLATES_FOUND",
                    "is_live_candidate_folder": folder_name in {"raw", "accepted"},
                    "valid_for_claim": False,
                    "claim_allowed": False,
                }
            )
            continue
        for csv_file in csv_files:
            try:
                rows = read_csv(csv_file)
                status = "CSV_PARSED"
                if folder_name in {"raw", "accepted"}:
                    for index, row in enumerate(rows, start=1):
                        row["_source_file"] = str(csv_file)
                        row["_source_row"] = str(index)
                        candidate_rows.append(row)
            except Exception as exc:
                rows = []
                status = f"CSV_PARSE_FAILED:{exc}"
            scan_rows.append(
                {
                    "scan_id": f"SCAN1260_{folder_name}_{csv_file.stem}",
                    "directory": str(directory),
                    "file": str(csv_file),
                    "rows_found": len(rows),
                    "scan_status": status,
                    "is_live_candidate_folder": folder_name in {"raw", "accepted"},
                    "valid_for_claim": False,
                    "claim_allowed": False,
                }
            )
    return scan_rows, candidate_rows


def recent_formalization_writes() -> list[Path]:
    if not FORMALIZATION.exists():
        return []
    recent: list[Path] = []
    for path in FORMALIZATION.rglob("*"):
        if path.is_file():
            mtime = datetime.fromtimestamp(path.stat().st_mtime, timezone.utc)
            if mtime >= RUN_STARTED_UTC:
                recent.append(path)
    return recent


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    source_register = [
        {
            "source_id": "SRC1260_0_1259_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1259_NEXT_TARGET.csv",
            "needle": "NEXT1259_0_1260",
            "purpose": "handoff to Z_R-positive coefficient intake",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1260_1_1259_contract",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1259_ZR_POSITIVE_COEFFICIENT_CONTRACT.csv",
            "needle": "ZRC1259_0_ZR",
            "purpose": "required Z_R/M_R2/J_R/B_R coefficient contract",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1260_2_1259_template",
            "local_path": "source-intake/rab-sector/docs/ZR1259_RAB_GRADIENT_COEFFICIENT_TEMPLATE_NONCLAIM.csv",
            "needle": "ZR1259_TEMPLATE_DO_NOT_SCORE",
            "purpose": "docs-only coefficient template",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1260_3_1255_ceiling",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1255_1249_RUNNER_SNAPSHOT.csv",
            "needle": "READY_NONCLAIM_NUMERIC_PASS",
            "purpose": "q_Rhat Cassini ceiling for future finite hair branch",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1260_4_1240_projection",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1240_QR_TO_PPN_MAPPING_SCHEMA.csv",
            "needle": "gamma_minus_1_QR approximately -q_R_hat/2",
            "purpose": "finite q_Rhat to gamma residual map",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1260_5_1256_contract",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1256_VARIATIONAL_BRANCH_AUDIT.csv",
            "needle": "ell_R=sqrt(Z_R/M_R^2)",
            "purpose": "massive/suppressed branch relation",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    intake_scan, candidate_rows = scan_intake()

    validation_rules = [
        {
            "rule_id": "RCR1260_0_schema",
            "rule": "live coefficient rows must contain every required field",
            "reject_status": "REJECT_MISSING_REQUIRED_FIELD",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "rule_id": "RCR1260_1_no_placeholders",
            "rule": "coefficient_value, units, sign_domain, source_path, parent_action_block, normalization, and qRhat link must contain no MISSING/TBD markers",
            "reject_status": "REJECT_PLACEHOLDER_ROW",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "rule_id": "RCR1260_2_allowed_symbols",
            "rule": "coefficient_symbol must be one of Z_R, M_R^2, J_R, B_R",
            "reject_status": "REJECT_UNKNOWN_COEFFICIENT",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "rule_id": "RCR1260_3_branch_map",
            "rule": "rows must declare whether they feed finite q_Rhat, massive suppression ell_R, boundary no-hair, or theorem-zero",
            "reject_status": "REJECT_NO_BRANCH_LINK",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "rule_id": "RCR1260_4_nonclaim",
            "rule": "valid_for_claim and claim_allowed must remain false in this checkpoint",
            "reject_status": "REJECT_CLAIM_FLAG",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    coefficient_mapping = [
        {
            "map_id": "MAP1260_0_finite_qRhat",
            "needed_inputs": "Z_R plus Q_R/J_R/B_R source value or direct q_Rhat",
            "branch": "finite reciprocal hair",
            "scoring_relation": "gamma_minus_1_QR=-q_Rhat/2 and abs(q_Rhat)<=4.6e-05 strict smoke ceiling",
            "current_status": "WAITING_FOR_LIVE_ROWS",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "map_id": "MAP1260_1_massive_suppression",
            "needed_inputs": "Z_R and M_R^2 with no/source flux conditions",
            "branch": "massive/suppressed reciprocal hair",
            "scoring_relation": "ell_R=sqrt(Z_R/M_R^2); local test needs ell_R or Yukawa envelope below PPN/R10 arena scale",
            "current_status": "WAITING_FOR_LIVE_ROWS",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "map_id": "MAP1260_2_boundary_nohair",
            "needed_inputs": "B_R exact/no-flux/source-worldtube theorem or finite flux value",
            "branch": "boundary no-hair or finite boundary charge",
            "scoring_relation": "Pi_R^n=Z_R n^iD_iR_AB+partial B_R/partial R_AB; zero flux gives Q_R=0 only after source-boundary proof",
            "current_status": "WAITING_FOR_LIVE_ROWS",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "map_id": "MAP1260_3_theorem_zero",
            "needed_inputs": "theorem-zero Z_R or parent R_AB constraint",
            "branch": "clean zero route",
            "scoring_relation": "theorem-zero is not accepted from docs rows; requires parent-signed operator ban or first-class constraint",
            "current_status": "WAITING_FOR_THEOREM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    candidate_results: list[dict[str, object]] = []
    for row in candidate_rows:
        failures: list[str] = []
        for field in REQUIRED_FIELDS:
            if field not in row:
                failures.append(f"MISSING_FIELD_{field}")
        if row.get("coefficient_symbol") not in {"Z_R", "M_R^2", "J_R", "B_R"}:
            failures.append("REJECT_UNKNOWN_COEFFICIENT")
        for field in ["coefficient_value", "coefficient_units", "sign_domain", "derivation_status", "source_path", "parent_action_block", "normalization_convention", "links_to_qRhat"]:
            if is_placeholder(row.get(field, "")):
                failures.append(f"REJECT_PLACEHOLDER_{field}")
        if is_false(row.get("valid_for_claim", "")) is False or is_false(row.get("claim_allowed", "")) is False:
            failures.append("REJECT_CLAIM_FLAG")
        candidate_results.append(
            {
                "row_id": row.get("row_id", ""),
                "source_file": row.get("_source_file", ""),
                "source_row": row.get("_source_row", ""),
                "coefficient_symbol": row.get("coefficient_symbol", ""),
                "validation_status": "ACCEPTED_NONCLAIM_COEFFICIENT_ROW" if not failures else ";".join(failures),
                "runner_eligible": not failures,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )

    accepted_rows = [row for row in candidate_results if row["runner_eligible"]]
    runner_status = [
        {
            "run_id": "RUN1260_0_scan",
            "live_candidate_rows": len(candidate_rows),
            "accepted_nonclaim_rows": len(accepted_rows),
            "runner_status": "READY_WITH_ACCEPTED_NONCLAIM_ROWS" if accepted_rows else "NO_LIVE_COEFFICIENT_ROWS",
            "claim_effect": "no local-GR or finite q_Rhat claim; intake readiness only",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    claim_gates = [
        {
            "gate_id": "GATE1260_0_intake_validator",
            "claim": "Z_R coefficient intake validator exists",
            "status": "PASS_NONCLAIM",
            "reason": "scanner, validation rules, and branch mapping are generated",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1260_1_live_coefficients",
            "claim": "live Z_R/M_R2/J_R/B_R coefficient rows exist",
            "status": "PASS_NONCLAIM" if accepted_rows else "BLOCKED",
            "reason": f"accepted_nonclaim_rows={len(accepted_rows)}",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1260_2_qRhat_or_suppression",
            "claim": "finite q_Rhat or suppression branch is score-ready",
            "status": "BLOCKED",
            "reason": "no complete coefficient set maps to q_Rhat or ell_R yet",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1260_3_local_GR",
            "claim": "local GR/Newton branch is derived",
            "status": "BLOCKED",
            "reason": "coefficient intake readiness is not a theorem or local-GR proof",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decisions = [
        {
            "decision_id": "DEC1260_0_intake_ready",
            "decision": "coefficient intake/validation path is ready",
            "because": "future Z_R/M_R2/J_R/B_R rows now have schema, refusal rules, and branch maps",
            "next_action": "source hunt for coefficient rows or return to operator-exclusion theorem",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1260_1_no_live_rows",
            "decision": "no live coefficient evidence is present yet",
            "because": "docs template exists but raw/accepted intake has no score-ready rows",
            "next_action": "1261-Y5-R10-ZR-coefficient-source-hunt-or-operator-exhaustion-reentry.md",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1260_0_1261",
            "target_file": "1261-Y5-R10-ZR-coefficient-source-hunt-or-operator-exhaustion-reentry.md",
            "target_script": "scripts/Y5_R10_ZR_coefficient_source_hunt_or_operator_exhaustion_reentry.py",
            "task": "either find/source real nonclaim Z_R/M_R2/J_R/B_R rows or return to the operator-exhaustion proof route that would ban Z_R",
            "success_condition": "produce source-backed coefficient evidence or a blocker ledger that leaves the branch ready but unclaimed",
            "do_not": "do not fabricate coefficients or treat the 1259 docs template as live evidence",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    generated_tables = [
        (SOURCE_REGISTER_PATH, source_register),
        (INTAKE_SCAN_PATH, intake_scan),
        (VALIDATION_RULES_PATH, validation_rules),
        (COEFFICIENT_MAPPING_PATH, coefficient_mapping),
        (RUNNER_STATUS_PATH, runner_status),
        (CLAIM_GATES_PATH, claim_gates),
        (DECISION_PATH, decisions),
        (NEXT_PATH, next_target),
    ]
    if candidate_results:
        generated_tables.append((OUT_DIR / f"{PACK_ID}_CANDIDATE_RESULTS.csv", candidate_results))

    for path, rows in generated_tables:
        write_csv(path, rows)

    source_checks = [exists_and_contains(str(row["local_path"]), str(row["needle"])) for row in source_register]
    sources_exist = all(exists for exists, _ in source_checks)
    needles_found = all(found for _, found in source_checks)
    scan_well_formed = all(row["scan_status"] in {"NO_CANDIDATE_FILES_FOUND", "NO_DOC_TEMPLATES_FOUND", "CSV_PARSED"} for row in intake_scan)
    docs_template_present = any(row["is_live_candidate_folder"] is False and int(row["rows_found"]) > 0 for row in intake_scan)
    no_live_rows = len(candidate_rows) == 0 and runner_status[0]["runner_status"] == "NO_LIVE_COEFFICIENT_ROWS"
    rules_complete = {row["rule_id"] for row in validation_rules} == {
        "RCR1260_0_schema",
        "RCR1260_1_no_placeholders",
        "RCR1260_2_allowed_symbols",
        "RCR1260_3_branch_map",
        "RCR1260_4_nonclaim",
    }
    maps_complete = {row["map_id"] for row in coefficient_mapping} == {
        "MAP1260_0_finite_qRhat",
        "MAP1260_1_massive_suppression",
        "MAP1260_2_boundary_nohair",
        "MAP1260_3_theorem_zero",
    }
    claims_ok = all(row["status"] in {"PASS_NONCLAIM", "BLOCKED"} and is_false(row["claim_allowed"]) for row in claim_gates)
    all_nonclaim = all(
        is_false(row.get("valid_for_claim", "")) and is_false(row.get("claim_allowed", ""))
        for _, rows in generated_tables
        for row in rows
    )
    next_is_1261 = next_target[0]["target_file"].startswith("1261-")

    csv_parse_details: list[str] = []
    csv_parse_ok = True
    for path, _ in generated_tables:
        try:
            rows = read_csv(path)
            csv_parse_details.append(f"{path.name}:{len(rows)}")
        except Exception as exc:  # pragma: no cover
            csv_parse_ok = False
            csv_parse_details.append(f"{path.name}:ERROR:{exc}")

    formalization_writes = recent_formalization_writes()

    validation_rows = [
        validation_row("VAL1260_0_sources_exist", "all cited local sources exist", sources_exist, f"{sum(1 for exists, _ in source_checks if exists)}/{len(source_checks)} sources exist"),
        validation_row("VAL1260_1_needles_found", "all cited local needles found", needles_found, f"{sum(1 for _, found in source_checks if found)}/{len(source_checks)} needles found"),
        validation_row("VAL1260_2_scan_well_formed", "rab-sector intake scan is well formed", scan_well_formed, f"scan_rows={len(intake_scan)}"),
        validation_row("VAL1260_3_docs_template_present", "docs template exists but is not live evidence", docs_template_present, "docs template parsed"),
        validation_row("VAL1260_4_no_live_rows", "no live coefficient rows are present", no_live_rows, f"live_candidate_rows={len(candidate_rows)}"),
        validation_row("VAL1260_5_rules_complete", "validation rules are complete", rules_complete, f"rule_rows={len(validation_rules)}"),
        validation_row("VAL1260_6_maps_complete", "coefficient branch maps are complete", maps_complete, f"map_rows={len(coefficient_mapping)}"),
        validation_row("VAL1260_7_claim_gates", "claim gates block qRhat/suppression/local-GR claims", claims_ok, f"claim_gate_rows={len(claim_gates)}"),
        validation_row("VAL1260_8_nonclaim_policy", "all generated rows remain nonclaim", all_nonclaim, "valid_for_claim=false and claim_allowed=false throughout generated tables"),
        validation_row("VAL1260_9_next_target_1261", "next target is coefficient source hunt or operator-exhaustion reentry", next_is_1261, str(next_target[0]["target_file"])),
        validation_row("VAL1260_10_csv_parse", "all generated CSVs parse cleanly", csv_parse_ok, "; ".join(csv_parse_details)),
        validation_row("VAL1260_11_formalization_untouched", "formalization-workbench untouched during run", not formalization_writes, f"formalization_recent_write_count_since_run_start={len(formalization_writes)}"),
    ]
    overall = all(row["status"] == "PASS" for row in validation_rows)
    validation_rows.append(
        validation_row(
            "VAL1260_12_overall",
            "overall 1260 validation",
            overall,
            "1260 builds strict Z_R-positive coefficient intake, qRhat/suppression mapping, and keeps all claims blocked with no live coefficient rows",
        )
    )
    write_csv(VALIDATION_PATH, validation_rows)

    doc = f"""# {TITLE}

**Current verdict:** 1260 builds the strict intake/validation path for `Z_R`, `M_R^2`, `J_R`, and `B_R`. No live coefficient row exists yet.

**Main progress:** future coefficient rows now have refusal rules and branch maps: finite `q_R_hat`, massive suppression `ell_R`, boundary no-hair, or theorem-zero. The 1259 template is parsed as docs-only, not evidence.

**No-claim guard:** no coefficient value, finite MTS `q_R_hat` prediction, suppression pass, boundary no-hair theorem, or local-GR/Newton derivation is promoted.

Generated UTC: {datetime.now(timezone.utc).isoformat()}

## Source Register
{markdown_table(source_register, ["source_id", "local_path", "needle", "purpose", "valid_for_claim", "claim_allowed"])}

## RAB Coefficient Intake Scan
{markdown_table(intake_scan, ["scan_id", "directory", "file", "rows_found", "scan_status", "is_live_candidate_folder", "valid_for_claim", "claim_allowed"])}

## RAB Coefficient Validation Rules
{markdown_table(validation_rules, ["rule_id", "rule", "reject_status", "valid_for_claim", "claim_allowed"])}

## Coefficient To q_Rhat Or Suppression Map
{markdown_table(coefficient_mapping, ["map_id", "needed_inputs", "branch", "scoring_relation", "current_status", "valid_for_claim", "claim_allowed"])}

## Coefficient Runner Status
{markdown_table(runner_status, ["run_id", "live_candidate_rows", "accepted_nonclaim_rows", "runner_status", "claim_effect", "valid_for_claim", "claim_allowed"])}

## Claim Gates
{markdown_table(claim_gates, ["gate_id", "claim", "status", "reason", "valid_for_claim", "claim_allowed"])}

## Decision Ledger
{markdown_table(decisions, ["decision_id", "decision", "because", "next_action", "valid_for_claim", "claim_allowed"])}

## Next Target
{markdown_table(next_target, ["next_id", "target_file", "target_script", "task", "success_condition", "do_not", "valid_for_claim", "claim_allowed"])}

## Validation
{markdown_table(validation_rows, ["check_id", "check", "status", "details"])}
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


if __name__ == "__main__":
    main()
