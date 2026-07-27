from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


PACK_ID = "P8_Y5_R10_1254"
TITLE = "1254-Y5-R10-boundary-flux-source-template-or-phenomenological-qRhat-row"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
QR_INTAKE_DIR = ROOT / "source-intake" / "qr-hat"
QR_DOCS_DIR = QR_INTAKE_DIR / "docs"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_STARTED_UTC = datetime.now(timezone.utc)


SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
INTAKE_SCAN_PATH = OUT_DIR / f"{PACK_ID}_QRHAT_INTAKE_SCAN.csv"
REQUIREMENTS_PATH = OUT_DIR / f"{PACK_ID}_QRHAT_INTAKE_REQUIREMENTS.csv"
BOUNDARY_FLUX_CONTRACT_PATH = OUT_DIR / f"{PACK_ID}_BOUNDARY_FLUX_CONTRACT.csv"
TEMPLATE_STATUS_PATH = OUT_DIR / f"{PACK_ID}_TEMPLATE_STATUS.csv"
CLAIM_GATES_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATES.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1254_VALIDATION.csv"
QRHAT_TEMPLATE_PATH = QR_DOCS_DIR / "QRHAT1254_BOUNDARY_FLUX_OR_PHENOMENOLOGICAL_TEMPLATE.csv"


REQUIRED_1249_FIELDS = [
    "candidate_id",
    "route_type",
    "q_R_hat",
    "q_R_hat_units",
    "Q_R_units_before_normalization",
    "GM_convention",
    "source_path",
    "derivation_status",
    "N_sigma",
    "sigma_gamma",
    "zero_theorem_statement",
    "closure_used",
    "valid_for_claim",
    "claim_allowed",
]

EXTRA_TEMPLATE_FIELDS = [
    "source_body",
    "coordinate_convention",
    "observable_anchor",
    "input_kind",
    "bound_direction",
    "uncertainty_policy",
    "notes",
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


def scan_qrhat_intake() -> list[dict[str, object]]:
    scan_rows: list[dict[str, object]] = []
    for folder_name in ["raw", "accepted", "docs"]:
        directory = QR_INTAKE_DIR / folder_name
        directory.mkdir(parents=True, exist_ok=True)
        csv_files = sorted(directory.glob("*.csv"))
        if not csv_files:
            scan_rows.append(
                {
                    "scan_id": f"SCAN1254_{folder_name}_empty",
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
            except Exception as exc:
                rows = []
                status = f"CSV_PARSE_FAILED:{exc}"
            scan_rows.append(
                {
                    "scan_id": f"SCAN1254_{folder_name}_{csv_file.stem}",
                    "directory": str(directory),
                    "file": str(csv_file),
                    "rows_found": len(rows),
                    "scan_status": status,
                    "is_live_candidate_folder": folder_name in {"raw", "accepted"},
                    "valid_for_claim": False,
                    "claim_allowed": False,
                }
            )
    return scan_rows


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    QR_DOCS_DIR.mkdir(parents=True, exist_ok=True)

    source_register = [
        {
            "source_id": "SRC1254_0_1253_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1253_NEXT_TARGET.csv",
            "needle": "NEXT1253_0_1254",
            "purpose": "handoff from failed H_core/boundary derivation to finite q_Rhat intake",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1254_1_1253_handoff",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1253_FINITE_QR_HANDOFF_STATUS.csv",
            "needle": "FQH1253_2_phenomenological_path",
            "purpose": "1253 says phenomenological finite q_Rhat is the best fallback after failed proof route",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1254_2_1249_rules",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1249_FINITE_QRHAT_VALIDATION_RULES.csv",
            "needle": "QRV1249_1_numeric",
            "purpose": "existing finite q_Rhat candidate validation rules",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1254_3_1249_runner",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1249_POLICY_RUNNER_RESULTS.csv",
            "needle": "NO_ACCEPTED_FINITE_QRHAT_ROWS",
            "purpose": "current q_Rhat runner has no accepted rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1254_4_1250_template",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1250_FIRST_FINITE_QRHAT_TEMPLATE.csv",
            "needle": "MISSING_NUMERIC_QR_HAT",
            "purpose": "first finite q_Rhat template remains placeholder",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1254_5_1244_GM",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1244_GM_CONVENTION_PACK.csv",
            "needle": "q_R_hat = Q_R c^2/(G M_source)",
            "purpose": "GM/source normalization convention for raw Q_R to q_R_hat",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1254_6_1040_boundary",
            "local_path": "1040-Y5-R10-parent-boundary-charge-formula-BX-or-alpha3-projection-bound.md",
            "needle": "Q_X[epsilon]=int_partialSigma epsilon_nu B_X^nu dS",
            "purpose": "boundary flux contract analogue for the reciprocal sector",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    intake_scan = scan_qrhat_intake()

    q_rhat_template = [
        {
            "candidate_id": "QRHAT1254_TEMPLATE_DO_NOT_SCORE",
            "route_type": "finite_qR_hat",
            "q_R_hat": "MISSING_NUMERIC_Q_R_HAT_OR_UPPER_BOUND",
            "q_R_hat_units": "dimensionless",
            "Q_R_units_before_normalization": "MISSING_RAW_QR_UNITS_OR_DIRECT_DIMENSIONLESS_DECLARATION",
            "GM_convention": "GM1244_SOURCE_NORMALIZATION_CONVENTION_REQUIRED",
            "source_path": "MISSING_SOURCE_PATH",
            "derivation_status": "phenomenological_bound_nonclaim",
            "N_sigma": "2",
            "sigma_gamma": "2.3e-5",
            "zero_theorem_statement": "NOT_A_ZERO_THEOREM_ROW",
            "closure_used": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "source_body": "MISSING_SOURCE_BODY",
            "coordinate_convention": "MISSING_AREAL_RADIAL_OR_EXPLICIT_MAP",
            "observable_anchor": "MISSING_OBSERVABLE_ANCHOR",
            "input_kind": "direct_q_R_hat_value_or_bound",
            "bound_direction": "abs(q_R_hat)<=q_R_hat_bound_if_bound_row",
            "uncertainty_policy": "MISSING_UNCERTAINTY_POLICY",
            "notes": "Place a completed copy in source-intake/qr-hat/raw only after all MISSING markers are removed; do not use closure zero as evidence.",
        }
    ]
    write_csv(QRHAT_TEMPLATE_PATH, q_rhat_template, REQUIRED_1249_FIELDS + EXTRA_TEMPLATE_FIELDS)

    requirements = [
        {
            "requirement_id": "REQ1254_0_schema",
            "field_or_object": "1249 required fields",
            "acceptable_content": "; ".join(REQUIRED_1249_FIELDS),
            "reject_if": "any required field is absent",
            "reason": "keeps future row compatible with the existing policy runner",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "requirement_id": "REQ1254_1_direct_value",
            "field_or_object": "q_R_hat",
            "acceptable_content": "finite dimensionless numeric value or clearly labelled upper-bound value for nonclaim smoke",
            "reject_if": "MISSING marker, nonnumeric text, hidden closure zero, or value without provenance",
            "reason": "the runner can only score numbers and must know whether it is prediction or bound",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "requirement_id": "REQ1254_2_raw_flux",
            "field_or_object": "Q_R -> q_R_hat",
            "acceptable_content": "raw Q_R plus units, source body, GM_source convention, and formula q_R_hat=Q_R c^2/(G M_source)",
            "reject_if": "raw Q_R units or GM convention are missing",
            "reason": "prevents a boundary flux number being silently treated as dimensionless",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "requirement_id": "REQ1254_3_boundary_flux",
            "field_or_object": "B_R/Q_R source",
            "acceptable_content": "parent-owned boundary density, integration surface, reference subtraction, sign/orientation, source class, and source path",
            "reject_if": "B_R is only an analogy to B_X or derived from closure",
            "reason": "1253 found the boundary formula shape but not the reciprocal-sector owner",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "requirement_id": "REQ1254_4_nonclaim",
            "field_or_object": "claim flags",
            "acceptable_content": "valid_for_claim=false and claim_allowed=false for this private smoke path",
            "reject_if": "either flag is true",
            "reason": "no local-GR or PPN claim is allowed from a bound-input row",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    boundary_flux_contract = [
        {
            "contract_id": "BFC1254_0_direct_dimensionless",
            "route": "direct q_R_hat",
            "formula": "q_R_hat supplied directly as a dimensionless number or upper bound",
            "must_supply": "source_path; observable_anchor; source_body; coordinate_convention; uncertainty_policy",
            "score_status": "TEMPLATE_ONLY_NO_ROW",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "BFC1254_1_raw_boundary_flux",
            "route": "raw Q_R boundary flux",
            "formula": "q_R_hat = Q_R c^2/(G M_source)",
            "must_supply": "Q_R value or bound; Q_R units; B_R/Q_R definition; integration surface; GM_source; source_path",
            "score_status": "TEMPLATE_ONLY_NO_ROW",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "BFC1254_2_zero_theorem",
            "route": "Q_R=0 theorem row",
            "formula": "q_R_hat = 0 only if a parent no-charge theorem is supplied",
            "must_supply": "parent H_core/source equation or first-class boundary/no-charge certificate",
            "score_status": "NOT_ALLOWED_FROM_CURRENT_CORPUS",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    live_candidate_rows = []
    for row in intake_scan:
        if str(row["is_live_candidate_folder"]).lower() == "true" and int(row["rows_found"]) > 0:
            live_candidate_rows.append(row)

    template_status = [
        {
            "template_id": "TSTAT1254_0_template_written",
            "template_path": str(QRHAT_TEMPLATE_PATH),
            "folder_role": "docs_only_not_live_intake",
            "required_1249_fields_present": all(field in q_rhat_template[0] for field in REQUIRED_1249_FIELDS),
            "contains_missing_markers": True,
            "ready_for_runner": False,
            "reason": "template is a completion contract, not a candidate row",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "template_id": "TSTAT1254_1_live_intake",
            "template_path": str(QR_INTAKE_DIR / "raw"),
            "folder_role": "future_candidate_folder",
            "required_1249_fields_present": "N/A",
            "contains_missing_markers": "N/A",
            "ready_for_runner": bool(live_candidate_rows),
            "reason": "no raw/accepted candidate rows found during 1254 scan",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    claim_gates = [
        {
            "gate_id": "GATE1254_0_template",
            "claim": "strict q_Rhat source template exists",
            "status": "PASS_NONCLAIM",
            "reason": "template written in docs folder with all 1249 required fields and explicit MISSING markers",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1254_1_live_candidate",
            "claim": "live finite q_Rhat candidate exists",
            "status": "BLOCKED",
            "reason": "raw and accepted intake folders have no candidate rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1254_2_boundary_flux",
            "claim": "boundary flux value is source-backed",
            "status": "BLOCKED",
            "reason": "B_R/Q_R owner, units, source class, and source path are missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1254_3_local_PPN",
            "claim": "local PPN branch passes",
            "status": "BLOCKED",
            "reason": "a template/bound-input gate is not a prediction or derived GR limit",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decision_ledger = [
        {
            "decision_id": "DEC1254_0_status",
            "decision": "1254 produces a strict intake contract, not a scoreable q_Rhat row",
            "because": "there are no source-backed raw or accepted q_Rhat candidates and the new template deliberately contains MISSING markers",
            "next_action": "hunt for a real source-backed q_Rhat/bound input or return to parent H_core if a new equation is supplied",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1254_1_runner",
            "decision": "do not rerun 1249 as a claim update yet",
            "because": "the live intake is still empty; the template is in docs only",
            "next_action": "only rerun 1249 after a completed copy is placed in source-intake/qr-hat/raw",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1254_0_1255",
            "target_file": "1255-Y5-R10-qRhat-source-hunt-or-parent-Hcore-reentry.md",
            "target_script": "scripts/Y5_R10_qRhat_source_hunt_or_parent_Hcore_reentry.py",
            "task": "either find a real source-backed finite q_Rhat/bound input for the 1254 template or re-enter parent H_core derivation if a candidate equation is available",
            "success_condition": "produce a completed nonclaim raw candidate row with no MISSING markers, or a blocker ledger proving no acceptable source-backed input is currently present",
            "do_not": "do not move the docs template into raw, do not invent q_Rhat, and do not convert comparator bounds into MTS predictions",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    generated_tables = [
        (SOURCE_REGISTER_PATH, source_register),
        (INTAKE_SCAN_PATH, intake_scan),
        (REQUIREMENTS_PATH, requirements),
        (BOUNDARY_FLUX_CONTRACT_PATH, boundary_flux_contract),
        (TEMPLATE_STATUS_PATH, template_status),
        (CLAIM_GATES_PATH, claim_gates),
        (DECISION_PATH, decision_ledger),
        (NEXT_PATH, next_target),
    ]

    for path, rows in generated_tables:
        write_csv(path, rows)

    source_checks = [exists_and_contains(str(row["local_path"]), str(row["needle"])) for row in source_register]
    sources_exist = all(exists for exists, _ in source_checks)
    needles_found = all(found for _, found in source_checks)
    template_rows = read_csv(QRHAT_TEMPLATE_PATH)
    template_columns = set(template_rows[0].keys()) if template_rows else set()
    template_has_required = all(field in template_columns for field in REQUIRED_1249_FIELDS)
    template_in_docs_only = QRHAT_TEMPLATE_PATH.parent == QR_DOCS_DIR
    raw_or_accepted_with_rows = any(
        str(row["is_live_candidate_folder"]).lower() == "true" and int(row["rows_found"]) > 0 for row in intake_scan
    )
    all_nonclaim = all(
        is_false(row.get("valid_for_claim", "")) and is_false(row.get("claim_allowed", ""))
        for _, rows in generated_tables
        for row in rows
    ) and all(is_false(row.get("valid_for_claim", "")) and is_false(row.get("claim_allowed", "")) for row in q_rhat_template)
    claims_blocked_or_nonclaim = all(row["status"] in {"BLOCKED", "PASS_NONCLAIM"} and is_false(row["claim_allowed"]) for row in claim_gates)
    next_is_1255 = next_target[0]["target_file"].startswith("1255-")

    csv_parse_details: list[str] = []
    csv_parse_ok = True
    for path, _ in generated_tables + [(QRHAT_TEMPLATE_PATH, q_rhat_template)]:
        try:
            rows = read_csv(path)
            csv_parse_details.append(f"{path.name}:{len(rows)}")
        except Exception as exc:  # pragma: no cover
            csv_parse_ok = False
            csv_parse_details.append(f"{path.name}:ERROR:{exc}")

    formalization_writes = recent_formalization_writes()

    validation_rows = [
        validation_row("VAL1254_0_sources_exist", "all cited local sources exist", sources_exist, f"{sum(1 for exists, _ in source_checks if exists)}/{len(source_checks)} sources exist"),
        validation_row("VAL1254_1_needles_found", "all cited local needles found", needles_found, f"{sum(1 for _, found in source_checks if found)}/{len(source_checks)} needles found"),
        validation_row("VAL1254_2_template_required_fields", "1254 template has every 1249 required field", template_has_required, f"required_fields={len(REQUIRED_1249_FIELDS)}; template_columns={len(template_columns)}"),
        validation_row("VAL1254_3_template_docs_only", "template is docs-only and not live intake", template_in_docs_only, str(QRHAT_TEMPLATE_PATH)),
        validation_row("VAL1254_4_no_live_candidates", "raw/accepted q_Rhat candidate intake remains empty", not raw_or_accepted_with_rows, "no raw or accepted rows found"),
        validation_row("VAL1254_5_boundary_contract_nonclaim", "boundary flux contract remains nonclaim", all(row["score_status"] != "SCORE_READY" for row in boundary_flux_contract), "direct/raw/zero routes are template-only or not allowed"),
        validation_row("VAL1254_6_claim_gates", "claim gates block live q_Rhat/local PPN claims", claims_blocked_or_nonclaim, f"claim_gate_rows={len(claim_gates)}"),
        validation_row("VAL1254_7_nonclaim_policy", "all generated rows remain nonclaim", all_nonclaim, "valid_for_claim=false and claim_allowed=false throughout generated tables and template"),
        validation_row("VAL1254_8_next_target_1255", "next target is source hunt or parent Hcore reentry", next_is_1255, str(next_target[0]["target_file"])),
        validation_row("VAL1254_9_csv_parse", "all generated CSVs parse cleanly", csv_parse_ok, "; ".join(csv_parse_details)),
        validation_row("VAL1254_10_formalization_untouched", "formalization-workbench untouched during run", not formalization_writes, f"formalization_recent_write_count_since_run_start={len(formalization_writes)}"),
    ]
    overall = all(row["status"] == "PASS" for row in validation_rows)
    validation_rows.append(
        validation_row(
            "VAL1254_11_overall",
            "overall 1254 validation",
            overall,
            "1254 writes a strict docs-only q_Rhat/boundary-flux intake template, confirms no live candidates exist, and keeps all claims blocked",
        )
    )
    write_csv(VALIDATION_PATH, validation_rows)

    doc = f"""# {TITLE}

**Current verdict:** 1254 builds the strict source-backed intake gate for finite `q_R_hat` or boundary-flux rows. No score-ready row exists yet.

**Main progress:** the fallback is now executable without being loose: a completed future row must either supply dimensionless `q_R_hat` directly, or raw `Q_R` with units plus `q_R_hat = Q_R c^2/(G M_source)`. The template stays in `source-intake/qr-hat/docs`, not in live intake.

**No-claim guard:** no local GR, local PPN, finite `q_R_hat`, R10/WEP, or source-coupling claim is promoted. The live `raw` and `accepted` folders remain empty.

Generated UTC: {datetime.now(timezone.utc).isoformat()}

## Source Register
{markdown_table(source_register, ["source_id", "local_path", "needle", "purpose", "valid_for_claim", "claim_allowed"])}

## q_Rhat Intake Scan
{markdown_table(intake_scan, ["scan_id", "directory", "file", "rows_found", "scan_status", "is_live_candidate_folder", "valid_for_claim", "claim_allowed"])}

## q_Rhat Intake Requirements
{markdown_table(requirements, ["requirement_id", "field_or_object", "acceptable_content", "reject_if", "reason", "valid_for_claim", "claim_allowed"])}

## Boundary Flux Contract
{markdown_table(boundary_flux_contract, ["contract_id", "route", "formula", "must_supply", "score_status", "valid_for_claim", "claim_allowed"])}

## Template Status
{markdown_table(template_status, ["template_id", "template_path", "folder_role", "required_1249_fields_present", "contains_missing_markers", "ready_for_runner", "reason", "valid_for_claim", "claim_allowed"])}

## Claim Gates
{markdown_table(claim_gates, ["gate_id", "claim", "status", "reason", "valid_for_claim", "claim_allowed"])}

## Decision Ledger
{markdown_table(decision_ledger, ["decision_id", "decision", "because", "next_action", "valid_for_claim", "claim_allowed"])}

## Next Target
{markdown_table(next_target, ["next_id", "target_file", "target_script", "task", "success_condition", "do_not", "valid_for_claim", "claim_allowed"])}

## Validation
{markdown_table(validation_rows, ["check_id", "check", "status", "details"])}
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


if __name__ == "__main__":
    main()
