from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


PACK_ID = "P8_Y5_R10_1269"
TITLE = "1269-Y5-R10-RAB-operator-exclusion-parent-sort-proof-or-ZR-template-intake-validator"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
RAB_INTAKE_DIR = ROOT / "source-intake" / "rab-sector"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_STARTED_UTC = datetime.now(timezone.utc)


SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
OPERATOR_PROOF_PATH = OUT_DIR / f"{PACK_ID}_OPERATOR_EXCLUSION_PARENT_SORT_ATTEMPT.csv"
AP1265_1_PATH = OUT_DIR / f"{PACK_ID}_AP1265_1_OPERATOR_EXCLUSION_GATE.csv"
VALIDATOR_RULES_PATH = OUT_DIR / f"{PACK_ID}_ZR_INTAKE_VALIDATOR_RULES.csv"
INTAKE_SCAN_PATH = OUT_DIR / f"{PACK_ID}_ZR_INTAKE_VALIDATOR_RESULTS.csv"
VALIDATOR_SUMMARY_PATH = OUT_DIR / f"{PACK_ID}_ZR_INTAKE_VALIDATOR_SUMMARY.csv"
CLAIM_GATES_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATES.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1269_VALIDATION.csv"


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


def contains_missing_marker(row: dict[str, object]) -> bool:
    return any("MISSING_" in str(value) for value in row.values())


def resolve_declared_source(row: dict[str, str]) -> Path | None:
    source = str(row.get("source_path", "")).strip()
    if not source or source.startswith("MISSING_"):
        return None
    return source_path(source)


def row_has_claim_flag(row: dict[str, str]) -> bool:
    return str(row.get("valid_for_claim", "")).strip().lower() == "true" or str(
        row.get("claim_allowed", "")
    ).strip().lower() == "true"


def validate_intake_row(path: Path, intake_class: str, row: dict[str, str]) -> dict[str, object]:
    row_id = row.get("row_id") or row.get("template_id") or row.get("coefficient_symbol") or "MISSING_ROW_ID"
    required_columns = [
        "coefficient_symbol",
        "coefficient_value",
        "coefficient_units",
        "normalization_convention",
        "parent_action_block",
        "source_path",
        "source_anchor",
        "arena_projection",
        "valid_for_claim",
        "claim_allowed",
    ]
    missing_columns = [column for column in required_columns if column not in row]
    source = resolve_declared_source(row)
    anchor = str(row.get("source_anchor", "")).strip()
    source_exists = bool(source and source.exists())
    anchor_found = bool(source_exists and anchor and not anchor.startswith("MISSING_") and anchor in read_text(source))
    reasons: list[str] = []
    if intake_class == "docs":
        reasons.append("DOCS_TEMPLATE_NOT_LIVE_INTAKE")
    if missing_columns:
        reasons.append("MISSING_REQUIRED_COLUMNS:" + ";".join(missing_columns))
    if contains_missing_marker(row):
        reasons.append("MISSING_MARKER_PRESENT")
    if source is None:
        reasons.append("SOURCE_PATH_MISSING_OR_PLACEHOLDER")
    elif not source_exists:
        reasons.append("SOURCE_PATH_NOT_FOUND")
    if not anchor or anchor.startswith("MISSING_"):
        reasons.append("SOURCE_ANCHOR_MISSING_OR_PLACEHOLDER")
    elif source_exists and not anchor_found:
        reasons.append("SOURCE_ANCHOR_NOT_FOUND")
    for field in ["coefficient_value", "coefficient_units", "normalization_convention", "parent_action_block", "arena_projection"]:
        if not str(row.get(field, "")).strip():
            reasons.append(f"{field.upper()}_EMPTY")
    if row_has_claim_flag(row):
        reasons.append("CLAIM_FLAG_TRUE_REJECTED_IN_PRIVATE_NONCLAIM_PHASE")
    if reasons:
        status = "REJECT"
        intake_eligible = False
    else:
        status = "ACCEPT_NONCLAIM_SOURCE_READY"
        intake_eligible = True
    return {
        "scan_id": f"SCAN1269_{intake_class}_{path.stem}_{row_id}",
        "intake_class": intake_class,
        "file_path": str(path),
        "row_id": row_id,
        "coefficient_symbol": row.get("coefficient_symbol", ""),
        "status": status,
        "reasons": "|".join(reasons) if reasons else "NO_PLACEHOLDERS_SOURCE_ANCHOR_FOUND_NONCLAIM",
        "source_exists": source_exists,
        "anchor_found": anchor_found,
        "intake_eligible": intake_eligible,
        "valid_for_claim": False,
        "claim_allowed": False,
    }


def scan_rab_intake() -> list[dict[str, object]]:
    results: list[dict[str, object]] = []
    for intake_class in ["docs", "raw", "accepted"]:
        directory = RAB_INTAKE_DIR / intake_class
        directory.mkdir(parents=True, exist_ok=True)
        for path in sorted(directory.glob("*.csv")):
            for row in read_csv(path):
                results.append(validate_intake_row(path, intake_class, row))
    return results


def generated_inside_formalization() -> list[Path]:
    generated_paths = [
        SOURCE_REGISTER_PATH,
        OPERATOR_PROOF_PATH,
        AP1265_1_PATH,
        VALIDATOR_RULES_PATH,
        INTAKE_SCAN_PATH,
        VALIDATOR_SUMMARY_PATH,
        CLAIM_GATES_PATH,
        DECISION_PATH,
        NEXT_PATH,
        VALIDATION_PATH,
        DOC_PATH,
    ]
    return [path for path in generated_paths if FORMALIZATION in path.parents]


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    source_register = [
        {
            "source_id": "SRC1269_0_1268_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1268_NEXT_TARGET.csv",
            "needle": "NEXT1268_0_1269",
            "purpose": "handoff to operator exclusion or finite-ZR intake validator",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1269_1_1268_action",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1268_COMPATIBILITY_ACTION_CANDIDATE.csv",
            "needle": "CAC1268_2_no_derivative_grammar",
            "purpose": "no-derivative grammar clause to prove",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1269_2_1268_ap",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1268_AP1265_COMPATIBILITY_CLOSURE_MATRIX.csv",
            "needle": "AP1265_1_no_derivatives",
            "purpose": "AP1265_1 operator-exclusion blocker",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1269_3_1262_minimal",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1262_MINIMAL_ASSUMPTION_AUDIT.csv",
            "needle": "MIN1262_2_no_vertical_metric_connection",
            "purpose": "minimal assumptions needed to ban vertical gradient energy",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1269_4_1262_theorem",
            "local_path": "1262-Y5-R10-RAB-operator-exhaustion-minimal-assumption-audit-or-ZR-prior-envelope.md",
            "needle": "THEO1262_0_vertical_null_ban",
            "purpose": "conditional vertical-null operator ban",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1269_5_1259_theorem",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1259_OPERATOR_EXCLUSION_THEOREM_CANDIDATE.csv",
            "needle": "THEO1259_0_gradient_ban_if_parent_exhaustion",
            "purpose": "older conditional gradient counterterm ban",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1269_6_1236_typed",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1236_PARENT_TYPED_OBJECT_LANGUAGE_CERTIFICATE_ATTEMPT.csv",
            "needle": "CERT1236_6_current_verdict",
            "purpose": "typed object-language certificate remains not parent-derived",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1269_7_1107_exhaustion",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1107_OBJECT_LANGUAGE_EXHAUSTION_ATTEMPT.csv",
            "needle": "OBJECT_LANGUAGE_EXHAUSTION_NOT_DERIVED",
            "purpose": "object-language exhaustion not derived",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1269_8_1058_operator",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1058_VISIBLE_OPERATOR_DOMAIN_EXHAUSTION_ATTEMPT.csv",
            "needle": "REJECT_CURRENT_CLAIM_RETAIN_COUNTERTERM_PRIOR",
            "purpose": "generic operator-domain exhaustion counterterm warning",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1269_9_1268_template",
            "local_path": "source-intake/rab-sector/docs/ZR1268_FINITE_ZR_SOURCE_ROW_TEMPLATE_NONCLAIM.csv",
            "needle": "ZR1268_TEMPLATE_ZR",
            "purpose": "finite-ZR docs template to validate/refuse",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    operator_attempt = [
        {
            "attempt_id": "OP1269_0_parent_sort",
            "claim_piece": "R_AB is a parent compatibility sort, not a physical scalar",
            "needed_proof": "typed parent field/sort list and quotient map q with R_AB variations in ker(Dq)",
            "current_evidence": "1268 writes candidate compatibility action; 1262 records R_AB vertical sort as not parent-derived",
            "result": "NOT_PARENT_SIGNED",
            "effect": "cannot ban Z_R from sort alone",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "OP1269_1_no_vertical_metric",
            "claim_piece": "parent has no vertical fibre metric/connection/Sobolev norm for R_AB",
            "needed_proof": "absence theorem for G_vert, nabla_vert, and local density G_vert(DR,D R)",
            "current_evidence": "MIN1262_2_no_vertical_metric_connection remains NOT_PARENT_DERIVED",
            "result": "NOT_PARENT_SIGNED",
            "effect": "a gauge/representative gradient energy remains a legal countermodel if a fibre metric exists",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "OP1269_2_object_exhaustion",
            "claim_piece": "parent object language excludes non-parent R_AB kinetic counterterms",
            "needed_proof": "Allowed[S_parent] is exhausted by parent generators and has no R_AB derivative constructor",
            "current_evidence": "1236/1107/1058 all keep object-language exhaustion as exact conditional, not derived",
            "result": "EXACT_CONDITIONAL_NOT_DERIVED",
            "effect": "operator exclusion cannot be promoted",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "OP1269_3_radiative_readout",
            "claim_piece": "effective/readout reduction cannot regenerate finite Z_R",
            "needed_proof": "S_eff and readout maps remain in Image(ParentGenerate[q,theta,top])",
            "current_evidence": "1265/1268 readout stability remains unsigned; 1058/1107 show radiative exhaustion is not signed",
            "result": "UNSIGNED",
            "effect": "tree-level operator ban would still be insufficient for a claim",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "OP1269_4_theorem_candidate",
            "claim_piece": "AP1265_1 no-derivative/operator-exclusion theorem",
            "needed_proof": "OP1269_0 through OP1269_3 all parent-signed",
            "current_evidence": "proof skeleton is coherent but missing parent sort, no-vertical-metric, object-exhaustion, and readout closure",
            "result": "BLOCKED_EXACT_CONDITIONAL",
            "effect": "finite-ZR intake validator is mandatory",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    ap1265_1_gate = [
        {
            "gate_id": "AP1265_1_0_sort",
            "requirement": "R_AB has compatibility/auxiliary sort only",
            "status": "BLOCKED",
            "reason": "parent sort list not derived from primitives",
            "validator_fallback": "reject rows without parent_action_block/source_path/source_anchor",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "AP1265_1_1_no_metric",
            "requirement": "no vertical fibre metric/connection for R_AB gradients",
            "status": "BLOCKED",
            "reason": "MIN1262_2 remains not parent-derived",
            "validator_fallback": "require Z_R theorem-zero or numeric source if gradient branch is used",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "AP1265_1_2_no_counterterm",
            "requirement": "no independent kinetic counterterm constructor",
            "status": "BLOCKED",
            "reason": "object-language exhaustion remains a contract not a theorem",
            "validator_fallback": "reject MISSING coefficient/units/normalization rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "AP1265_1_3_readout",
            "requirement": "readout/effective action cannot regenerate Z_R",
            "status": "BLOCKED",
            "reason": "radiative/readout closure is unsigned",
            "validator_fallback": "require arena_projection and source anchor for every tau row",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    validator_rules = [
        {
            "rule_id": "RULE1269_0_docs_not_live",
            "rule": "Rows in source-intake/rab-sector/docs are always rejected as docs templates.",
            "failure_status": "DOCS_TEMPLATE_NOT_LIVE_INTAKE",
            "severity": "hard_reject",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "rule_id": "RULE1269_1_no_missing_markers",
            "rule": "Any field containing MISSING_ rejects the row.",
            "failure_status": "MISSING_MARKER_PRESENT",
            "severity": "hard_reject",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "rule_id": "RULE1269_2_source_path_exists",
            "rule": "source_path must be non-placeholder and resolve to an existing local file.",
            "failure_status": "SOURCE_PATH_MISSING_OR_NOT_FOUND",
            "severity": "hard_reject",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "rule_id": "RULE1269_3_source_anchor_found",
            "rule": "source_anchor must be non-placeholder and occur in source_path text.",
            "failure_status": "SOURCE_ANCHOR_MISSING_OR_NOT_FOUND",
            "severity": "hard_reject",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "rule_id": "RULE1269_4_required_fields",
            "rule": "coefficient_symbol, value, units, normalization, parent_action_block, arena_projection, and claim flags must exist.",
            "failure_status": "MISSING_REQUIRED_COLUMNS_OR_EMPTY_FIELD",
            "severity": "hard_reject",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "rule_id": "RULE1269_5_private_nonclaim",
            "rule": "During this private checkpoint, valid_for_claim=true or claim_allowed=true rejects the row.",
            "failure_status": "CLAIM_FLAG_TRUE_REJECTED_IN_PRIVATE_NONCLAIM_PHASE",
            "severity": "hard_reject",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    intake_scan = scan_rab_intake()
    docs_rows = [row for row in intake_scan if row["intake_class"] == "docs"]
    raw_rows = [row for row in intake_scan if row["intake_class"] == "raw"]
    accepted_rows = [row for row in intake_scan if row["intake_class"] == "accepted"]
    accepted_ready = [row for row in accepted_rows if row["intake_eligible"]]
    rejected_rows = [row for row in intake_scan if row["status"] == "REJECT"]
    invalid_live_rows = [row for row in [*raw_rows, *accepted_rows] if row["status"] == "REJECT"]
    validator_summary = [
        {
            "summary_id": "VS1269_0_scan_counts",
            "docs_rows": len(docs_rows),
            "raw_rows": len(raw_rows),
            "accepted_rows": len(accepted_rows),
            "rejected_rows": len(rejected_rows),
            "accepted_ready_rows": len(accepted_ready),
            "invalid_live_rows": len(invalid_live_rows),
            "status": "NO_ACCEPTED_SOURCE_READY_ROWS",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "summary_id": "VS1269_1_template_refusal",
            "docs_rows": len(docs_rows),
            "raw_rows": len(raw_rows),
            "accepted_rows": len(accepted_rows),
            "rejected_rows": len([row for row in docs_rows if row["status"] == "REJECT"]),
            "accepted_ready_rows": 0,
            "invalid_live_rows": len(invalid_live_rows),
            "status": "DOCS_TEMPLATES_REJECTED_AS_EXPECTED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    claim_gates = [
        {
            "gate_id": "GATE1269_0_AP1265_1",
            "claim": "AP1265_1 no-derivative/operator-exclusion clause is parent-signed",
            "status": "BLOCKED",
            "reason": "parent sort, no vertical metric/connection, object-language exhaustion, and readout closure remain unsigned",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1269_1_ZR_zero",
            "claim": "Z_R=0 follows from operator exclusion",
            "status": "BLOCKED",
            "reason": "operator-exclusion theorem is exact conditional only",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1269_2_validator",
            "claim": "finite-ZR intake validator refuses placeholders and source-missing rows",
            "status": "PASS_NONCLAIM",
            "reason": "all docs template rows are rejected; no raw/accepted source-ready rows exist",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1269_3_local_tests",
            "claim": "local GR/R10/PPN/clock/orbital pass",
            "status": "BLOCKED",
            "reason": "neither theorem-zero nor accepted finite-ZR rows are available",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decisions = [
        {
            "decision_id": "DEC1269_0_operator_proof",
            "decision": "do not promote AP1265_1 yet",
            "because": "the typed sort/operator-exclusion proof still depends on unsourced parent grammar and readout closure",
            "status": "EXACT_CONDITIONAL_BLOCKED",
            "next_action": "attack parent sort/quotient-map derivation or keep finite intake locked behind validator",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1269_1_validator",
            "decision": "finite-ZR fallback now has a hard refusal gate",
            "because": "every template/source-missing row is rejected before scoring",
            "status": "VALIDATOR_ACTIVE_NONCLAIM",
            "next_action": "future rows must move to raw/accepted only after replacing MISSING markers and supplying source anchors",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1269_2_next_route",
            "decision": "next derivation target should be the parent quotient/sort map for R_AB",
            "because": "without R_AB in ker(Dq) and no vertical metric, every operator ban remains taste rather than theorem",
            "status": "NEXT_PROOF_TARGET_NARROWED",
            "next_action": "try to derive R_AB compatibility sort from q(Phi) and coframe variables",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1269_0_1270",
            "target_file": "1270-Y5-R10-RAB-quotient-map-parent-sort-derivation-or-finite-ZR-first-source-row.md",
            "target_script": "scripts/Y5_R10_RAB_quotient_map_parent_sort_derivation_or_finite_ZR_first_source_row.py",
            "task": "try to derive R_AB as a compatibility/vertical sort from the parent quotient map q(Phi); if that fails, create the first raw finite-ZR candidate row only if it is source-backed and passes the 1269 validator",
            "success_condition": "R_AB in ker(Dq) and no physical scalar status are parent-signed, or a finite-ZR row is accepted by the validator without MISSING markers",
            "do_not": "do not promote AP1265_1 or score finite-ZR templates without source-backed rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    generated_tables = [
        (SOURCE_REGISTER_PATH, source_register),
        (OPERATOR_PROOF_PATH, operator_attempt),
        (AP1265_1_PATH, ap1265_1_gate),
        (VALIDATOR_RULES_PATH, validator_rules),
        (INTAKE_SCAN_PATH, intake_scan),
        (VALIDATOR_SUMMARY_PATH, validator_summary),
        (CLAIM_GATES_PATH, claim_gates),
        (DECISION_PATH, decisions),
        (NEXT_PATH, next_target),
    ]
    for path, rows in generated_tables:
        write_csv(path, rows)

    source_checks = [exists_and_contains(row["local_path"], row["needle"]) for row in source_register]
    all_sources_exist = all(exists for exists, _ in source_checks)
    all_needles_found = all(found for _, found in source_checks)
    operator_blocked = any(row["result"] == "BLOCKED_EXACT_CONDITIONAL" for row in operator_attempt)
    ap1265_1_blocked = all(row["status"] == "BLOCKED" for row in ap1265_1_gate)
    rules_complete = len(validator_rules) == 6 and all(row["severity"] == "hard_reject" for row in validator_rules)
    docs_rejected = len(docs_rows) > 0 and all(row["status"] == "REJECT" for row in docs_rows)
    no_bad_live_rows = len(invalid_live_rows) == 0 and len(accepted_ready) == 0
    validator_nonclaim = all(is_false(row["valid_for_claim"]) and is_false(row["claim_allowed"]) for row in intake_scan)
    claim_gates_safe = all(
        row["status"] in {"BLOCKED", "PASS_NONCLAIM"} and is_false(row["valid_for_claim"]) and is_false(row["claim_allowed"])
        for row in claim_gates
    )
    all_generated_rows = [
        *source_register,
        *operator_attempt,
        *ap1265_1_gate,
        *validator_rules,
        *intake_scan,
        *validator_summary,
        *claim_gates,
        *decisions,
        *next_target,
    ]
    nonclaim_policy = all(is_false(row.get("valid_for_claim")) and is_false(row.get("claim_allowed")) for row in all_generated_rows)
    formalization_generated = generated_inside_formalization()

    parsed_details = []
    csv_parse_ok = True
    for path, _rows in generated_tables:
        try:
            parsed_rows = read_csv(path)
            parsed_details.append(f"{path.name}:{len(parsed_rows)}")
        except Exception as exc:
            csv_parse_ok = False
            parsed_details.append(f"{path.name}:ERROR:{exc}")

    validation = [
        validation_row(
            "VAL1269_0_sources_exist",
            "all cited local sources exist",
            all_sources_exist,
            f"{sum(1 for exists, _ in source_checks if exists)}/{len(source_checks)} sources exist",
        ),
        validation_row(
            "VAL1269_1_needles_found",
            "all cited local needles found",
            all_needles_found,
            f"{sum(1 for _, found in source_checks if found)}/{len(source_checks)} needles found",
        ),
        validation_row(
            "VAL1269_2_operator_proof_blocked",
            "operator exclusion proof remains exact conditional, not promoted",
            operator_blocked,
            "OP1269_4_theorem_candidate=BLOCKED_EXACT_CONDITIONAL",
        ),
        validation_row(
            "VAL1269_3_ap1265_1_blocked",
            "AP1265_1 subclauses remain blocked",
            ap1265_1_blocked,
            f"subgate_rows={len(ap1265_1_gate)}",
        ),
        validation_row(
            "VAL1269_4_validator_rules",
            "finite-ZR intake validator has hard refusal rules",
            rules_complete,
            f"validator_rule_rows={len(validator_rules)}",
        ),
        validation_row(
            "VAL1269_5_docs_rejected",
            "docs template rows are rejected by validator",
            docs_rejected,
            f"docs_rows={len(docs_rows)}; rejected_docs={len([row for row in docs_rows if row['status'] == 'REJECT'])}",
        ),
        validation_row(
            "VAL1269_6_no_live_rows",
            "no raw/accepted finite-ZR rows are currently score-ready or invalid",
            no_bad_live_rows,
            f"raw_rows={len(raw_rows)}; accepted_rows={len(accepted_rows)}; accepted_ready={len(accepted_ready)}; invalid_live={len(invalid_live_rows)}",
        ),
        validation_row(
            "VAL1269_7_validator_nonclaim",
            "validator results remain nonclaim",
            validator_nonclaim,
            f"intake_scan_rows={len(intake_scan)}",
        ),
        validation_row(
            "VAL1269_8_claim_gates",
            "claim gates block AP1265_1/Z_R/local tests while validator passes nonclaim",
            claim_gates_safe,
            f"claim_gate_rows={len(claim_gates)}",
        ),
        validation_row(
            "VAL1269_9_nonclaim_policy",
            "all generated rows remain nonclaim",
            nonclaim_policy,
            "valid_for_claim=false and claim_allowed=false throughout generated tables",
        ),
        validation_row(
            "VAL1269_10_next_target_1270",
            "next target routes to quotient-map parent sort or source-backed finite row",
            next_target[0]["next_id"] == "NEXT1269_0_1270",
            str(next_target[0]["target_file"]),
        ),
        validation_row(
            "VAL1269_11_csv_parse",
            "all generated CSVs parse cleanly",
            csv_parse_ok,
            "; ".join(parsed_details),
        ),
        validation_row(
            "VAL1269_12_formalization_untouched",
            "formalization-workbench untouched by generated outputs",
            len(formalization_generated) == 0,
            f"formalization_generated_output_count={len(formalization_generated)}",
        ),
    ]
    overall_pass = all(row["status"] == "PASS" for row in validation)
    validation.append(
        validation_row(
            "VAL1269_13_overall",
            "overall 1269 validation",
            overall_pass,
            "1269 keeps AP1265_1/operator exclusion conditional, implements a hard finite-ZR intake validator, rejects all docs templates, and routes next to the R_AB quotient-map parent sort derivation",
        )
    )
    write_csv(VALIDATION_PATH, validation)

    doc = f"""# {TITLE}

**Current verdict:** 1269 does not parent-sign the `R_AB` operator-exclusion theorem. The proof skeleton is clean, but it still needs a parent quotient/sort map, absence of vertical metric/connection, object-language exhaustion, and radiative/readout closure. So `AP1265_1` remains blocked.

**Main progress:** the fallback is now much safer. A finite-`Z_R` intake validator is active: docs rows are rejected, any `MISSING_*` marker is rejected, source paths and anchors must resolve, required coefficient/projection fields must exist, and claim flags are refused during this private nonclaim phase.

**No-claim guard:** no `Z_R=0`, local-GR/Newton, R10, PPN, clock, orbital, or finite-`Z_R` score is claimed. The validator currently rejects the docs templates and finds no raw/accepted source-ready rows.

Run timestamp UTC: `{RUN_STARTED_UTC.isoformat()}`

## Source Register
{markdown_table(source_register, ["source_id", "local_path", "needle", "purpose", "valid_for_claim", "claim_allowed"])}

## Operator Exclusion Parent Sort Attempt
{markdown_table(operator_attempt, ["attempt_id", "claim_piece", "needed_proof", "current_evidence", "result", "effect", "valid_for_claim", "claim_allowed"])}

## AP1265_1 Operator Exclusion Gate
{markdown_table(ap1265_1_gate, ["gate_id", "requirement", "status", "reason", "validator_fallback", "valid_for_claim", "claim_allowed"])}

## Z_R Intake Validator Rules
{markdown_table(validator_rules, ["rule_id", "rule", "failure_status", "severity", "valid_for_claim", "claim_allowed"])}

## Z_R Intake Validator Summary
{markdown_table(validator_summary, ["summary_id", "docs_rows", "raw_rows", "accepted_rows", "rejected_rows", "accepted_ready_rows", "invalid_live_rows", "status", "valid_for_claim", "claim_allowed"])}

## Z_R Intake Validator Results
{markdown_table(intake_scan, ["scan_id", "intake_class", "row_id", "coefficient_symbol", "status", "reasons", "source_exists", "anchor_found", "intake_eligible", "valid_for_claim", "claim_allowed"])}

## Claim Gates
{markdown_table(claim_gates, ["gate_id", "claim", "status", "reason", "valid_for_claim", "claim_allowed"])}

## Decision Ledger
{markdown_table(decisions, ["decision_id", "decision", "because", "status", "next_action", "valid_for_claim", "claim_allowed"])}

## Next Target
{markdown_table(next_target, ["next_id", "target_file", "target_script", "task", "success_condition", "do_not", "valid_for_claim", "claim_allowed"])}

## Validation
{markdown_table(validation, ["check_id", "check", "status", "details"])}
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


if __name__ == "__main__":
    main()
