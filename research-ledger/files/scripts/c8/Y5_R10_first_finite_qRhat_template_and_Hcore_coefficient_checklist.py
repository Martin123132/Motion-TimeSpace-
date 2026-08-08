from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


PACK_ID = "P8_Y5_R10_1250"
TITLE = "1250-Y5-R10-first-finite-qRhat-template-and-Hcore-coefficient-checklist"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
QR_DOCS_DIR = ROOT / "source-intake" / "qr-hat" / "docs"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_STARTED_UTC = datetime.now(timezone.utc)


SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
TEMPLATE_PATH = OUT_DIR / f"{PACK_ID}_FIRST_FINITE_QRHAT_TEMPLATE.csv"
DOC_TEMPLATE_PATH = QR_DOCS_DIR / "QRHAT1250_FIRST_FINITE_QRHAT_TEMPLATE.csv"
HCORE_CHECKLIST_PATH = OUT_DIR / f"{PACK_ID}_HCORE_COEFFICIENT_CHECKLIST.csv"
EVIDENCE_MODES_PATH = OUT_DIR / f"{PACK_ID}_FINITE_QRHAT_EVIDENCE_MODES.csv"
REFUSAL_RULES_PATH = OUT_DIR / f"{PACK_ID}_REFUSAL_RULES.csv"
CLAIM_GATES_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATES.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1250_VALIDATION.csv"


FIELDS = [
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


def is_false(row: dict[str, object], key: str) -> bool:
    return str(row.get(key, "")).strip().lower() in {"false", "0", "no"}


def validation_row(check_id: str, check: str, passed: bool, details: str) -> dict[str, object]:
    return {
        "check_id": check_id,
        "check": check,
        "status": "PASS" if passed else "FAIL",
        "details": details,
    }


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
    QR_DOCS_DIR.mkdir(parents=True, exist_ok=True)

    source_register = [
        {
            "source_id": "SRC1250_0_1249_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1249_NEXT_TARGET.csv",
            "needle": "NEXT1249_0_1250",
            "purpose": "handoff to first finite q_Rhat template/checklist",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1250_1_1249_rules",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1249_FINITE_QRHAT_VALIDATION_RULES.csv",
            "needle": "QRV1249_4_no_closure",
            "purpose": "finite q_Rhat refusal rules",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1250_2_1249_runner",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1249_POLICY_RUNNER_RESULTS.csv",
            "needle": "NO_ACCEPTED_FINITE_QRHAT_ROWS",
            "purpose": "runner has no accepted finite row yet",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1250_3_1249_source_ledger",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1249_SOURCE_ACQUISITION_LEDGER.csv",
            "needle": "MISSING_PARENT_COEFFICIENT_MAP",
            "purpose": "H_core coefficient map is missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1250_4_1244_policy",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1244_RUNNER_POLICY_FEED.csv",
            "needle": "4.6e-05",
            "purpose": "policy values for template",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1250_5_1244_GM",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1244_GM_CONVENTION_PACK.csv",
            "needle": "GM1244_0_qR_definition",
            "purpose": "GM convention for template",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1250_6_1248_failure",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1248_FAILURE_LEDGER.csv",
            "needle": "FAIL1248_1_core",
            "purpose": "H_core/bracket closure failure from ansatz attempt",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    template_rows = [
        {
            "candidate_id": "QRHAT1250_TEMPLATE_DO_NOT_SCORE",
            "route_type": "finite_qR_hat",
            "q_R_hat": "MISSING_NUMERIC_QR_HAT",
            "q_R_hat_units": "dimensionless",
            "Q_R_units_before_normalization": "MISSING_QR_UNITS_OR_DIRECT_DIMENSIONLESS",
            "GM_convention": "MISSING_GM_CONVENTION_BIND_TO_GM1244",
            "source_path": "MISSING_SOURCE_PATH_OR_EXTERNAL_PROVENANCE",
            "derivation_status": "phenomenological_bound_nonclaim_OR_sourced_finite_model",
            "N_sigma": "1",
            "sigma_gamma": "2.3e-5",
            "zero_theorem_statement": "",
            "closure_used": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    hcore_checklist = [
        {
            "check_id": "HC1250_0_core_action",
            "needed_object": "L_MTS_core or H_core",
            "minimum_evidence": "explicit local weak-field parent core for T,S/e_pub/chi_load, not just lambda_R C_R",
            "why_needed": "q_R_hat must come from a coefficient equation or boundary charge, not template arithmetic",
            "current_status": "MISSING_HCORE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "check_id": "HC1250_1_canonical_brackets",
            "needed_object": "canonical variables and brackets",
            "minimum_evidence": "Poisson/Dirac bracket table for T,S or C_R sector",
            "why_needed": "constraint preservation and finite residual coefficient require bracket closure",
            "current_status": "MISSING_BRACKET_TABLE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "check_id": "HC1250_2_boundary_charge",
            "needed_object": "Q_R boundary/corner class",
            "minimum_evidence": "boundary variation identifies whether Q_R is forbidden, zero, or finite with units",
            "why_needed": "finite q_R_hat is meaningless unless Q_R is a defined charge/source coefficient",
            "current_status": "MISSING_BOUNDARY_CLASS",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "check_id": "HC1250_3_GM_projection",
            "needed_object": "Q_R to q_R_hat projection",
            "minimum_evidence": "q_R_hat=Q_R c^2/(G M_source) with source body, measured GM, and coordinate convention",
            "why_needed": "local PPN runner uses dimensionless q_R_hat",
            "current_status": "MISSING_QR_TO_QRHAT_SOURCE_ROW",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "check_id": "HC1250_4_gamma_policy",
            "needed_object": "PPN gamma scoring map",
            "minimum_evidence": "gamma_minus_1_QR=-q_R_hat/2 and strict 1244 policy values",
            "why_needed": "finite row must be smoke-scored consistently",
            "current_status": "READY_NONCLAIM_POLICY_ONLY",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "check_id": "HC1250_5_no_closure",
            "needed_object": "no-closure certificate",
            "minimum_evidence": "source derivation does not use R_AB=0, q_R_hat=0 by closure, or 1248 ansatz-zero",
            "why_needed": "prevents importing the desired local GR result",
            "current_status": "REQUIRED_FOR_ANY_ROW",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    evidence_modes = [
        {
            "mode_id": "EM1250_0_parent_derived",
            "mode": "sourced_finite_model",
            "acceptable_evidence": "parent H_core/boundary calculation produces finite q_R_hat or raw Q_R with conversion",
            "claim_ceiling": "nonclaim smoke row until beta/matter/boundary gates close",
            "status": "PREFERRED_BUT_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "mode_id": "EM1250_1_phenomenological_bound",
            "mode": "phenomenological_bound_nonclaim",
            "acceptable_evidence": "source-backed empirical/phenomenological upper bound on q_R_hat, with no closure and full provenance",
            "claim_ceiling": "bound-input only; not derivation of GR",
            "status": "ALLOWED_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "mode_id": "EM1250_2_zero_theorem",
            "mode": "parent_derived_zero",
            "acceptable_evidence": "only if parent theorem proves Q_R=0 without closure and passes 1242 zero-theorem gates",
            "claim_ceiling": "not part of finite q_Rhat template; route back to zero-theorem validator",
            "status": "SEPARATE_ROUTE_BLOCKED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    refusal_rules = [
        {
            "refusal_id": "REF1250_0_template",
            "bad_input": "QRHAT1250_TEMPLATE_DO_NOT_SCORE",
            "refusal": "template row contains MISSING markers",
            "status": "REJECT_MISSING_OR_NONNUMERIC_QR",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "refusal_id": "REF1250_1_closure_zero",
            "bad_input": "q_R_hat=0 because R_AB=0 closure",
            "refusal": "closure zero is not evidence",
            "status": "REJECT_CLOSURE_AS_EVIDENCE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "refusal_id": "REF1250_2_ansatz_zero",
            "bad_input": "1248 minimal lambda_R ansatz zero",
            "refusal": "ansatz zero is not parent-signed",
            "status": "REJECT_ZERO_THEOREM_UNDERIVED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "refusal_id": "REF1250_3_comparator_only",
            "bad_input": "Cassini/PPN comparator without MTS q_R_hat",
            "refusal": "comparator is a bound, not a prediction",
            "status": "REFUSED_COMPARATOR_ONLY",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "refusal_id": "REF1250_4_hidden_GM",
            "bad_input": "raw Q_R without source body/GM convention",
            "refusal": "normalization hidden",
            "status": "REJECT_MISSING_GM_CONVENTION",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    claim_gates = [
        {
            "gate_id": "GATE1250_0_template",
            "claim": "first finite q_Rhat template exists",
            "status": "PASS_NONCLAIM",
            "reason": "template written to mts_residuals and qr-hat/docs",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1250_1_hcore_checklist",
            "claim": "H_core coefficient checklist exists",
            "status": "PASS_NONCLAIM",
            "reason": "six coefficient/source requirements are explicit",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1250_2_finite_qR_value",
            "claim": "finite q_Rhat value exists",
            "status": "BLOCKED",
            "reason": "template intentionally contains MISSING_NUMERIC_QR_HAT",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1250_3_local_PPN",
            "claim": "finite local PPN smoke pass",
            "status": "BLOCKED",
            "reason": "no real finite q_Rhat candidate has been entered",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1250_4_local_GR",
            "claim": "derived local GR/Newton limit",
            "status": "BLOCKED",
            "reason": "H_core, boundary class, matter descent, beta, and q_R theorem/value remain open",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decisions = [
        {
            "decision_id": "DEC1250_0_template_docs_only",
            "decision": "write the template to qr-hat/docs, not raw/accepted",
            "because": "docs templates must not be accidentally scanned as candidate evidence",
            "next_action": "copy into raw only after replacing all MISSING markers with real sourced values",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1250_1_Hcore_first",
            "decision": "next derivation route should target H_core coefficient map",
            "because": "finite q_Rhat is valuable only if its coefficient/source meaning is defined",
            "next_action": "attempt H_core to q_Rhat coefficient map or explicitly keep phenomenological mode separate",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1250_0_1251",
            "target_file": "1251-Y5-R10-Hcore-to-qRhat-coefficient-map-attempt-or-phenomenological-row.md",
            "target_script": "scripts/Y5_R10_Hcore_to_qRhat_coefficient_map_attempt_or_phenomenological_row.py",
            "task": "try to derive the first finite q_Rhat coefficient map from H_core/boundary data; if not possible, keep the phenomenological row pathway separate and nonclaim",
            "success_condition": "either a real coefficient map target is produced, or the next source row is explicitly marked phenomenological_bound_nonclaim with no derivation claim",
            "do_not": "do not fill the template with fabricated q_Rhat or closure zero",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    generated_sets = [
        source_register,
        template_rows,
        hcore_checklist,
        evidence_modes,
        refusal_rules,
        claim_gates,
        decisions,
        next_target,
    ]
    output_paths = [
        SOURCE_REGISTER_PATH,
        TEMPLATE_PATH,
        DOC_TEMPLATE_PATH,
        HCORE_CHECKLIST_PATH,
        EVIDENCE_MODES_PATH,
        REFUSAL_RULES_PATH,
        CLAIM_GATES_PATH,
        DECISION_PATH,
        NEXT_PATH,
    ]

    write_csv(SOURCE_REGISTER_PATH, source_register)
    write_csv(TEMPLATE_PATH, template_rows, FIELDS)
    write_csv(DOC_TEMPLATE_PATH, template_rows, FIELDS)
    write_csv(HCORE_CHECKLIST_PATH, hcore_checklist)
    write_csv(EVIDENCE_MODES_PATH, evidence_modes)
    write_csv(REFUSAL_RULES_PATH, refusal_rules)
    write_csv(CLAIM_GATES_PATH, claim_gates)
    write_csv(DECISION_PATH, decisions)
    write_csv(NEXT_PATH, next_target)

    source_checks = [exists_and_contains(row["local_path"], row["needle"]) for row in source_register]
    all_sources_exist = all(exists for exists, _ in source_checks)
    all_needles_found = all(found for _, found in source_checks)
    template_fields_ok = list(read_csv(TEMPLATE_PATH)[0].keys()) == FIELDS and list(read_csv(DOC_TEMPLATE_PATH)[0].keys()) == FIELDS
    template_has_missing = any("MISSING" in str(value) for value in template_rows[0].values())
    docs_only = DOC_TEMPLATE_PATH.exists() and not (ROOT / "source-intake" / "qr-hat" / "raw" / DOC_TEMPLATE_PATH.name).exists()
    hcore_complete = len(hcore_checklist) == 6 and any(row["check_id"] == "HC1250_0_core_action" for row in hcore_checklist)
    refusal_complete = len(refusal_rules) == 5 and any(row["status"] == "REJECT_ZERO_THEOREM_UNDERIVED" for row in refusal_rules)
    no_claim_pass = all(
        row["status"] in {"PASS_NONCLAIM", "BLOCKED"} and is_false(row, "claim_allowed")
        for row in claim_gates
    )
    all_generated_nonclaim = all(
        is_false(row, "valid_for_claim") and (("claim_allowed" not in row) or is_false(row, "claim_allowed"))
        for rows in generated_sets
        for row in rows
        if "valid_for_claim" in row
    )
    next_is_1251 = next_target[0]["next_id"] == "NEXT1250_0_1251"

    parsed_counts: list[str] = []
    csv_parse_ok = True
    for path in output_paths:
        try:
            parsed_counts.append(f"{path.name}:{len(read_csv(path))}")
        except Exception as exc:
            csv_parse_ok = False
            parsed_counts.append(f"{path.name}:PARSE_FAIL:{exc}")

    fw_recent = recent_formalization_writes()

    validation = [
        validation_row("VAL1250_0_sources_exist", "all cited local sources exist", all_sources_exist, f"{sum(1 for exists, _ in source_checks if exists)}/{len(source_checks)} sources exist"),
        validation_row("VAL1250_1_needles_found", "all cited local needles found", all_needles_found, f"{sum(1 for _, found in source_checks if found)}/{len(source_checks)} needles found"),
        validation_row("VAL1250_2_template_fields", "template has exact 1249-required fields", template_fields_ok, f"fields={len(FIELDS)}"),
        validation_row("VAL1250_3_template_missing", "template remains placeholder and cannot be scored", template_has_missing, "MISSING markers present by design"),
        validation_row("VAL1250_4_docs_only", "template is in docs, not raw candidate intake", docs_only, str(DOC_TEMPLATE_PATH)),
        validation_row("VAL1250_5_hcore_checklist", "H_core coefficient checklist is complete", hcore_complete, f"hcore_rows={len(hcore_checklist)}"),
        validation_row("VAL1250_6_refusal_rules", "known bad rows have refusal rules", refusal_complete, f"refusal_rows={len(refusal_rules)}"),
        validation_row("VAL1250_7_claim_gates", "claim gates remain blocked/nonclaim", no_claim_pass, f"claim_gate_rows={len(claim_gates)}"),
        validation_row("VAL1250_8_nonclaim_policy", "all generated rows remain nonclaim", all_generated_nonclaim, "valid_for_claim=false and claim_allowed=false throughout generated tables"),
        validation_row("VAL1250_9_next_target_1251", "next target is H_core to q_Rhat coefficient map", next_is_1251, next_target[0]["target_file"]),
        validation_row("VAL1250_10_csv_parse", "all generated CSVs parse cleanly", csv_parse_ok, "; ".join(parsed_counts)),
        validation_row("VAL1250_11_formalization_untouched", "formalization-workbench untouched during run", len(fw_recent) == 0, f"formalization_recent_write_count_since_run_start={len(fw_recent)}"),
    ]
    validation.append(
        validation_row(
            "VAL1250_12_overall",
            "overall 1250 validation",
            all(row["status"] == "PASS" for row in validation),
            "1250 creates the first finite q_Rhat template and H_core coefficient checklist without fabricating a value or promoting a claim",
        )
    )
    write_csv(VALIDATION_PATH, validation)

    sections = [
        f"# {TITLE}",
        "",
        "**Current verdict:** 1250 creates the first finite `q_R_hat` template and the `H_core` coefficient checklist. It does not fill a value; the template deliberately contains `MISSING` markers and lives in `qr-hat/docs`, not candidate intake.",
        "",
        "**Main progress:** the first real finite row now has a strict shape. To enter candidate intake, it must replace every placeholder with sourced coefficient/provenance data and satisfy the no-closure, GM, policy, and source gates.",
        "",
        "**No-claim guard:** no finite `q_R_hat`, PPN pass, local-GR pass, R10/WEP pass, or source-coupling claim is promoted.",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "## Source Register",
        markdown_table(source_register, list(source_register[0].keys())),
        "",
        "## First Finite QRhat Template",
        markdown_table(template_rows, FIELDS),
        "",
        f"Template copy for future manual fill: `{DOC_TEMPLATE_PATH}`",
        "",
        "## Hcore Coefficient Checklist",
        markdown_table(hcore_checklist, list(hcore_checklist[0].keys())),
        "",
        "## Finite QRhat Evidence Modes",
        markdown_table(evidence_modes, list(evidence_modes[0].keys())),
        "",
        "## Refusal Rules",
        markdown_table(refusal_rules, list(refusal_rules[0].keys())),
        "",
        "## Claim Gates",
        markdown_table(claim_gates, list(claim_gates[0].keys())),
        "",
        "## Decision Ledger",
        markdown_table(decisions, list(decisions[0].keys())),
        "",
        "## Next Target",
        markdown_table(next_target, list(next_target[0].keys())),
        "",
        "## Validation",
        markdown_table(validation, list(validation[0].keys())),
        "",
    ]
    DOC_PATH.write_text("\n".join(sections), encoding="utf-8")

    print(f"Wrote {DOC_PATH}")
    print(f"Wrote validation {VALIDATION_PATH}")
    print(f"Wrote template {DOC_TEMPLATE_PATH}")


if __name__ == "__main__":
    main()
