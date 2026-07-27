from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


PACK_ID = "P8_Y5_R10_1259"
TITLE = "1259-Y5-R10-RAB-gradient-counterterm-ban-or-ZR-source-row"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
RAB_DOCS_DIR = ROOT / "source-intake" / "rab-sector" / "docs"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_STARTED_UTC = datetime.now(timezone.utc)


SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
BAN_ATTEMPT_PATH = OUT_DIR / f"{PACK_ID}_RAB_GRADIENT_COUNTERTERM_BAN_ATTEMPT.csv"
BAN_THEOREM_PATH = OUT_DIR / f"{PACK_ID}_OPERATOR_EXCLUSION_THEOREM_CANDIDATE.csv"
COEFFICIENT_CONTRACT_PATH = OUT_DIR / f"{PACK_ID}_ZR_POSITIVE_COEFFICIENT_CONTRACT.csv"
SOURCE_ROW_STATUS_PATH = OUT_DIR / f"{PACK_ID}_ZR_SOURCE_ROW_STATUS.csv"
CLAIM_GATES_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATES.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1259_VALIDATION.csv"
ZR_TEMPLATE_PATH = RAB_DOCS_DIR / "ZR1259_RAB_GRADIENT_COEFFICIENT_TEMPLATE_NONCLAIM.csv"


ZR_TEMPLATE_FIELDS = [
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


def has_missing_marker(rows: list[dict[str, str]]) -> bool:
    joined = "\n".join(str(value) for row in rows for value in row.values())
    return "MISSING" in joined or "TEMPLATE" in joined or "REQUIRED" in joined


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
    RAB_DOCS_DIR.mkdir(parents=True, exist_ok=True)

    source_register = [
        {
            "source_id": "SRC1259_0_1258_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1258_NEXT_TARGET.csv",
            "needle": "NEXT1258_0_1259",
            "purpose": "handoff to R_AB gradient-counterterm ban or Z_R source row",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1259_1_1258_risk",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1258_RAB_GRADIENT_COUNTERTERM_RISK_LEDGER.csv",
            "needle": "CTR1258_0_composite_gradient",
            "purpose": "retained R_AB gradient counterterm risk",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1259_2_1258_handoff",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1258_ZR_POSITIVE_HANDOFF.csv",
            "needle": "RETAINED_AS_REQUIRED_FALLBACK",
            "purpose": "Z_R-positive finite/suppressed branch retained",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1259_3_1058_exhaustion",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1058_VISIBLE_OPERATOR_DOMAIN_EXHAUSTION_ATTEMPT.csv",
            "needle": "REJECT_CURRENT_CLAIM_RETAIN_COUNTERTERM_PRIOR",
            "purpose": "visible operator exhaustion not derived; counterterm risk retained",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1259_4_1107_exhaustion",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1107_OBJECT_LANGUAGE_EXHAUSTION_ATTEMPT.csv",
            "needle": "OBJECT_LANGUAGE_EXHAUSTION_NOT_DERIVED",
            "purpose": "parent object-language exhaustion remains closure-only",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1259_5_1236_typed",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1236_PARENT_TYPED_OBJECT_LANGUAGE_CERTIFICATE_ATTEMPT.csv",
            "needle": "CERTIFICATE_SCHEMA_VALID_NOT_PARENT_DERIVED",
            "purpose": "typed grammar exact if signed but not derived from MTS primitives",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1259_6_1256_contract",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1256_MINIMAL_HCORE_SOURCE_EQUATION_CONTRACT.csv",
            "needle": "Z_R h^{ij} D_i R_AB D_j R_AB",
            "purpose": "formal kinetic coefficient that would need ban/source",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1259_7_1255_ceiling",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1255_1249_RUNNER_SNAPSHOT.csv",
            "needle": "READY_NONCLAIM_NUMERIC_PASS",
            "purpose": "available q_Rhat empirical ceiling for future finite residual branch",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    ban_attempt = [
        {
            "ban_id": "BAN1259_0_composite_not_enough",
            "ban_route": "R_AB is composite/readout so gradient term is illegal",
            "formal_test": "composite status alone forbids int sqrt(h) Z_R (nabla R_AB)^2",
            "result": "FAIL",
            "reason": "composite scalars can still appear in effective/readout counterterms unless object language bans them",
            "effect": "cannot set Z_R=0",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "ban_id": "BAN1259_1_typed_grammar",
            "ban_route": "typed parent grammar excludes the operator",
            "formal_test": "R_AB is not in allowed visible operator/coefficient domain and no hidden/readout counterterm can generate it",
            "result": "CONDITIONAL_NOT_DERIVED",
            "reason": "1236 certificate is exact as a discipline contract but not parent-signed",
            "effect": "would ban Z_R only after parent signature",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "ban_id": "BAN1259_2_operator_exhaustion",
            "ban_route": "Allowed local operators are exhausted by ParentGenerate image",
            "formal_test": "int sqrt(h) Z_R (nabla R_AB)^2 is outside Image(ParentGenerate)",
            "result": "FAIL_CURRENT_CORPUS",
            "reason": "1058/1107 both retain counterterm priors when exhaustion is unsigned",
            "effect": "must retain Z_R-positive branch",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "ban_id": "BAN1259_3_first_class_constraint",
            "ban_route": "R_AB is removed by first-class/algebraic constraint",
            "formal_test": "lambda_R primary/secondary chain makes kinetic term redundant/illegal",
            "result": "NOT_PROVED",
            "reason": "lambda_R origin and Dirac closure are still missing",
            "effect": "zero route stays conditional",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    ban_theorem = [
        {
            "candidate_id": "THEO1259_0_gradient_ban_if_parent_exhaustion",
            "theorem_name": "R_AB gradient counterterm ban",
            "candidate_statement": "If the parent object language is exhausted by EH/readout/topological generators and R_AB appears only as a constrained coframe compatibility variable, then int sqrt(h) Z_R h^{ij}D_iR_ABD_jR_AB is not an allowed independent operator and Z_R=0.",
            "proof_status": "EXACT_IF_PARENT_SIGNED_NOT_DERIVED",
            "missing_for_derivation": "parent operator exhaustion; R_AB compatibility sort; first-class/algebraic constraint; radiative/readout stability",
            "claim_effect": "cannot promote Z_R=0 in current corpus",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    coefficient_contract = [
        {
            "contract_id": "ZRC1259_0_ZR",
            "symbol": "Z_R",
            "role": "kinetic reciprocal-gradient coefficient",
            "operator_or_relation": "int sqrt(h) 1/2 Z_R h^{ij}D_iR_ABD_jR_AB",
            "required_source": "parent H_core/L_MTS_core coefficient, theorem-zero, or source-backed bound",
            "units_or_normalization": "must match R_AB dimensionless and derivative convention; declare length powers explicitly",
            "status": "SOURCE_REQUIRED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "ZRC1259_1_MR2",
            "symbol": "M_R^2",
            "role": "local mass-gap/suppression coefficient",
            "operator_or_relation": "ell_R=sqrt(Z_R/M_R^2) for constant-coefficient branch",
            "required_source": "parent Hessian/second variation around local fixed point",
            "units_or_normalization": "inverse length squared after Z_R normalization or declared equivalent",
            "status": "SOURCE_REQUIRED_IF_ZR_POSITIVE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "ZRC1259_2_JR",
            "symbol": "J_R",
            "role": "matter/source coupling to reciprocal strain",
            "operator_or_relation": "J_R R_AB source term and exterior Q_R",
            "required_source": "matter descent/source current map proving zero, finite value, or bound",
            "units_or_normalization": "must convert through q_Rhat=Q_R c^2/(G M_source) or direct dimensionless q_Rhat",
            "status": "SOURCE_REQUIRED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "ZRC1259_3_BR",
            "symbol": "B_R",
            "role": "boundary/counterterm/no-hair owner",
            "operator_or_relation": "Pi_R^n=Z_R n^iD_iR_AB + partial B_R/partial R_AB",
            "required_source": "boundary variation, source-worldtube class, reference subtraction, no-flux/exactness theorem or finite flux",
            "units_or_normalization": "must declare surface measure and sign/orientation convention",
            "status": "SOURCE_REQUIRED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    zr_template = [
        {
            "row_id": "ZR1259_TEMPLATE_DO_NOT_SCORE",
            "coefficient_symbol": "Z_R_or_M_R2_or_J_R_or_B_R",
            "operator_or_term": "MISSING_OPERATOR_OR_TERM",
            "coefficient_value": "MISSING_NUMERIC_VALUE_OR_THEOREM_ZERO",
            "coefficient_units": "MISSING_UNITS",
            "sign_domain": "MISSING_POSITIVE_ZERO_OR_BOUND_SIGN",
            "derivation_status": "MISSING_PARENT_DERIVED_OR_SOURCE_BACKED_BOUND",
            "source_path": "MISSING_SOURCE_PATH",
            "parent_action_block": "MISSING_PARENT_ACTION_BLOCK",
            "normalization_convention": "MISSING_NORMALIZATION_CONVENTION",
            "links_to_qRhat": "MISSING_QRHAT_OR_SUPPRESSION_MAP",
            "valid_for_claim": False,
            "claim_allowed": False,
            "notes": "Docs-only template. Do not move to live intake until all MISSING markers are removed and row is explicitly nonclaim or theorem-audited.",
        }
    ]
    write_csv(ZR_TEMPLATE_PATH, zr_template, ZR_TEMPLATE_FIELDS)

    source_row_status = [
        {
            "status_id": "ZRS1259_0_template",
            "template_path": str(ZR_TEMPLATE_PATH),
            "folder_role": "docs_only_not_live_intake",
            "contains_missing_markers": True,
            "ready_for_scoring": False,
            "reason": "operator ban failed; coefficient contract exists but no source-backed row exists",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    claim_gates = [
        {
            "gate_id": "GATE1259_0_gradient_ban",
            "claim": "R_AB gradient counterterm is banned",
            "status": "BLOCKED",
            "reason": "ban is exact only if parent operator exhaustion/constraint is signed; current corpus does not sign it",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1259_1_ZR_zero",
            "claim": "Z_R=0 is derived",
            "status": "BLOCKED",
            "reason": "gradient counterterm remains legal risk",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1259_2_ZR_source",
            "claim": "Z_R-positive coefficients are source-backed",
            "status": "BLOCKED",
            "reason": "only docs-only coefficient template exists; no numeric/theorem row is scored",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1259_3_local_GR",
            "claim": "local GR/Newton branch is derived",
            "status": "BLOCKED",
            "reason": "zero route and finite/suppressed coefficient route both remain unclosed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decisions = [
        {
            "decision_id": "DEC1259_0_ban_result",
            "decision": "do not ban the R_AB gradient counterterm yet",
            "because": "object-language exhaustion and first-class constraint routes are exact conditionally but unsigned",
            "next_action": "keep Z_R-positive coefficient sourcing live while continuing the operator-ban proof path",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1259_1_best_next",
            "decision": "next target is the Z_R-positive coefficient/suppression intake gate",
            "because": "a serious theory must either derive the ban or quantify the residual; current evidence does neither",
            "next_action": "1260-Y5-R10-ZR-positive-suppression-coefficient-intake-and-qRhat-link.md",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1259_0_1260",
            "target_file": "1260-Y5-R10-ZR-positive-suppression-coefficient-intake-and-qRhat-link.md",
            "target_script": "scripts/Y5_R10_ZR_positive_suppression_coefficient_intake_and_qRhat_link.py",
            "task": "build the strict nonclaim intake/validation path for Z_R, M_R^2, J_R, B_R and connect any finite branch to q_Rhat/Cassini ceiling or massive suppression scale",
            "success_condition": "schema validates coefficient rows, refuses placeholders, and maps accepted future rows to either q_Rhat finite-hair scoring or ell_R suppression scoring",
            "do_not": "do not fabricate coefficients and do not treat docs-only templates as live evidence",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    generated_tables = [
        (SOURCE_REGISTER_PATH, source_register),
        (BAN_ATTEMPT_PATH, ban_attempt),
        (BAN_THEOREM_PATH, ban_theorem),
        (COEFFICIENT_CONTRACT_PATH, coefficient_contract),
        (SOURCE_ROW_STATUS_PATH, source_row_status),
        (CLAIM_GATES_PATH, claim_gates),
        (DECISION_PATH, decisions),
        (NEXT_PATH, next_target),
    ]

    for path, rows in generated_tables:
        write_csv(path, rows)

    source_checks = [exists_and_contains(str(row["local_path"]), str(row["needle"])) for row in source_register]
    sources_exist = all(exists for exists, _ in source_checks)
    needles_found = all(found for _, found in source_checks)
    ban_attempt_complete = {row["ban_id"] for row in ban_attempt} == {
        "BAN1259_0_composite_not_enough",
        "BAN1259_1_typed_grammar",
        "BAN1259_2_operator_exhaustion",
        "BAN1259_3_first_class_constraint",
    }
    ban_not_promoted = ban_theorem[0]["proof_status"] == "EXACT_IF_PARENT_SIGNED_NOT_DERIVED"
    coefficient_contract_complete = {row["symbol"] for row in coefficient_contract} == {"Z_R", "M_R^2", "J_R", "B_R"}
    template_rows = read_csv(ZR_TEMPLATE_PATH)
    template_columns = set(template_rows[0].keys()) if template_rows else set()
    template_schema_ok = all(field in template_columns for field in ZR_TEMPLATE_FIELDS)
    template_docs_only = ZR_TEMPLATE_PATH.parent == RAB_DOCS_DIR
    template_has_missing = has_missing_marker(template_rows)
    claims_ok = all(row["status"] == "BLOCKED" and is_false(row["claim_allowed"]) for row in claim_gates)
    all_nonclaim = all(
        is_false(row.get("valid_for_claim", "")) and is_false(row.get("claim_allowed", ""))
        for _, rows in generated_tables
        for row in rows
    ) and all(is_false(row.get("valid_for_claim", "")) and is_false(row.get("claim_allowed", "")) for row in template_rows)
    next_is_1260 = next_target[0]["target_file"].startswith("1260-")

    csv_parse_details: list[str] = []
    csv_parse_ok = True
    for path, _ in generated_tables + [(ZR_TEMPLATE_PATH, zr_template)]:
        try:
            rows = read_csv(path)
            csv_parse_details.append(f"{path.name}:{len(rows)}")
        except Exception as exc:  # pragma: no cover
            csv_parse_ok = False
            csv_parse_details.append(f"{path.name}:ERROR:{exc}")

    formalization_writes = recent_formalization_writes()

    validation_rows = [
        validation_row("VAL1259_0_sources_exist", "all cited local sources exist", sources_exist, f"{sum(1 for exists, _ in source_checks if exists)}/{len(source_checks)} sources exist"),
        validation_row("VAL1259_1_needles_found", "all cited local needles found", needles_found, f"{sum(1 for _, found in source_checks if found)}/{len(source_checks)} needles found"),
        validation_row("VAL1259_2_ban_attempt_complete", "counterterm ban audit covers composite/typed/exhaustion/constraint routes", ban_attempt_complete, f"ban_rows={len(ban_attempt)}"),
        validation_row("VAL1259_3_ban_not_promoted", "operator-exclusion theorem remains conditional", ban_not_promoted, ban_theorem[0]["proof_status"]),
        validation_row("VAL1259_4_coefficient_contract", "Z_R/M_R2/J_R/B_R coefficient contract is complete", coefficient_contract_complete, f"contract_rows={len(coefficient_contract)}"),
        validation_row("VAL1259_5_template_schema", "ZR coefficient template has required schema", template_schema_ok, f"template_columns={len(template_columns)}"),
        validation_row("VAL1259_6_template_docs_only", "ZR coefficient template is docs-only", template_docs_only, str(ZR_TEMPLATE_PATH)),
        validation_row("VAL1259_7_template_placeholders", "ZR coefficient template is not score-ready", template_has_missing, "MISSING markers retained by design"),
        validation_row("VAL1259_8_claim_gates", "claim gates block gradient ban/Z_R/local GR", claims_ok, f"claim_gate_rows={len(claim_gates)}"),
        validation_row("VAL1259_9_nonclaim_policy", "all generated rows remain nonclaim", all_nonclaim, "valid_for_claim=false and claim_allowed=false throughout generated tables and template"),
        validation_row("VAL1259_10_next_target_1260", "next target is Z_R-positive coefficient intake", next_is_1260, str(next_target[0]["target_file"])),
        validation_row("VAL1259_11_csv_parse", "all generated CSVs parse cleanly", csv_parse_ok, "; ".join(csv_parse_details)),
        validation_row("VAL1259_12_formalization_untouched", "formalization-workbench untouched during run", not formalization_writes, f"formalization_recent_write_count_since_run_start={len(formalization_writes)}"),
    ]
    overall = all(row["status"] == "PASS" for row in validation_rows)
    validation_rows.append(
        validation_row(
            "VAL1259_13_overall",
            "overall 1259 validation",
            overall,
            "1259 keeps the R_AB gradient-counterterm ban conditional, creates a strict Z_R coefficient contract/template, and blocks all claims",
        )
    )
    write_csv(VALIDATION_PATH, validation_rows)

    doc = f"""# {TITLE}

**Current verdict:** 1259 does **not** ban the `R_AB` gradient/kinetic counterterm in the current corpus. The ban is exact only if parent operator exhaustion or a first-class `R_AB` constraint is signed.

**Main progress:** the coupling goblin is now boxed. If the ban fails, the live fallback is not vague: source or bound `Z_R`, `M_R^2`, `J_R`, and `B_R`, then connect the finite branch to `q_R_hat` or the suppressed branch to `ell_R`.

**No-claim guard:** no `Z_R=0`, no `Q_R=0`, no finite MTS `q_R_hat` prediction, and no local-GR/Newton derivation is promoted. The new coefficient template is docs-only and deliberately contains placeholders.

Generated UTC: {datetime.now(timezone.utc).isoformat()}

## Source Register
{markdown_table(source_register, ["source_id", "local_path", "needle", "purpose", "valid_for_claim", "claim_allowed"])}

## R_AB Gradient Counterterm Ban Attempt
{markdown_table(ban_attempt, ["ban_id", "ban_route", "formal_test", "result", "reason", "effect", "valid_for_claim", "claim_allowed"])}

## Operator Exclusion Theorem Candidate
{markdown_table(ban_theorem, ["candidate_id", "theorem_name", "candidate_statement", "proof_status", "missing_for_derivation", "claim_effect", "valid_for_claim", "claim_allowed"])}

## Z_R Positive Coefficient Contract
{markdown_table(coefficient_contract, ["contract_id", "symbol", "role", "operator_or_relation", "required_source", "units_or_normalization", "status", "valid_for_claim", "claim_allowed"])}

## Z_R Source Row Status
{markdown_table(source_row_status, ["status_id", "template_path", "folder_role", "contains_missing_markers", "ready_for_scoring", "reason", "valid_for_claim", "claim_allowed"])}

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
