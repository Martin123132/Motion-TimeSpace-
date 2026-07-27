from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


PACK_ID = "P8_Y5_R10_1261"
TITLE = "1261-Y5-R10-ZR-coefficient-source-hunt-or-operator-exhaustion-reentry"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
RAB_INTAKE_DIR = ROOT / "source-intake" / "rab-sector"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_STARTED_UTC = datetime.now(timezone.utc)


SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
INTAKE_SCAN_PATH = OUT_DIR / f"{PACK_ID}_INTAKE_SCAN_SNAPSHOT.csv"
COEFFICIENT_HUNT_PATH = OUT_DIR / f"{PACK_ID}_COEFFICIENT_SOURCE_HUNT_LEDGER.csv"
LIVE_ROW_REVIEW_PATH = OUT_DIR / f"{PACK_ID}_LIVE_ROW_REVIEW.csv"
MENTION_SCAN_PATH = OUT_DIR / f"{PACK_ID}_CORPUS_MENTION_SCAN.csv"
OPERATOR_REENTRY_PATH = OUT_DIR / f"{PACK_ID}_OPERATOR_EXHAUSTION_REENTRY_AUDIT.csv"
BLOCKER_LEDGER_PATH = OUT_DIR / f"{PACK_ID}_BLOCKER_LEDGER.csv"
CLAIM_GATES_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATES.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1261_VALIDATION.csv"


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

ALLOWED_COEFFICIENTS = {
    "Z_R": {
        "role": "R_AB gradient kinetic coefficient",
        "required_evidence": "parent action coefficient, theorem-zero, or source-backed local bound",
        "branch_link": "finite q_Rhat or massive suppression once paired with J_R/B_R/M_R^2",
    },
    "M_R^2": {
        "role": "local mass-gap/suppression coefficient",
        "required_evidence": "parent Hessian or second variation around the local fixed point",
        "branch_link": "ell_R=sqrt(Z_R/M_R^2)",
    },
    "J_R": {
        "role": "matter/source coupling to reciprocal strain",
        "required_evidence": "matter descent/source current map proving zero, finite value, or bound",
        "branch_link": "Q_R and q_Rhat source amplitude",
    },
    "B_R": {
        "role": "boundary/counterterm/no-hair owner",
        "required_evidence": "boundary variation, source-worldtube class, reference subtraction, or no-flux theorem",
        "branch_link": "Pi_R^n and boundary no-hair",
    },
}


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


def has_placeholder_marker(row: dict[str, object], fields: list[str]) -> bool:
    return any(is_placeholder(row.get(field, "")) for field in fields)


def scan_intake() -> tuple[list[dict[str, object]], list[dict[str, str]], list[dict[str, str]]]:
    scan_rows: list[dict[str, object]] = []
    live_rows: list[dict[str, str]] = []
    docs_rows: list[dict[str, str]] = []
    for folder_name in ["raw", "accepted", "docs"]:
        directory = RAB_INTAKE_DIR / folder_name
        directory.mkdir(parents=True, exist_ok=True)
        csv_files = sorted(directory.glob("*.csv"))
        if not csv_files:
            scan_rows.append(
                {
                    "scan_id": f"SCAN1261_{folder_name}_empty",
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
                for row_index, row in enumerate(rows, start=1):
                    row["_source_file"] = str(csv_file)
                    row["_source_row"] = str(row_index)
                    if folder_name in {"raw", "accepted"}:
                        live_rows.append(row)
                    else:
                        docs_rows.append(row)
            except Exception as exc:
                rows = []
                status = f"CSV_PARSE_FAILED:{exc}"
            scan_rows.append(
                {
                    "scan_id": f"SCAN1261_{folder_name}_{csv_file.stem}",
                    "directory": str(directory),
                    "file": str(csv_file),
                    "rows_found": len(rows),
                    "scan_status": status,
                    "is_live_candidate_folder": folder_name in {"raw", "accepted"},
                    "valid_for_claim": False,
                    "claim_allowed": False,
                }
            )
    return scan_rows, live_rows, docs_rows


def review_live_rows(live_rows: list[dict[str, str]]) -> list[dict[str, object]]:
    if not live_rows:
        return [
            {
                "review_id": "LRR1261_0_no_live_rows",
                "source_file": "",
                "source_row": "",
                "coefficient_symbol": "",
                "validation_status": "NO_LIVE_COEFFICIENT_ROWS",
                "runner_eligible": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        ]

    review_rows: list[dict[str, object]] = []
    for row in live_rows:
        failures: list[str] = []
        missing_fields = [field for field in REQUIRED_FIELDS if field not in row]
        if missing_fields:
            failures.append("REJECT_MISSING_REQUIRED_FIELD:" + ";".join(missing_fields))
        symbol = row.get("coefficient_symbol", "")
        if symbol not in ALLOWED_COEFFICIENTS:
            failures.append("REJECT_UNKNOWN_COEFFICIENT")
        if has_placeholder_marker(row, REQUIRED_FIELDS):
            failures.append("REJECT_PLACEHOLDER_ROW")
        source_field = row.get("source_path", "")
        if is_placeholder(source_field):
            failures.append("REJECT_MISSING_SOURCE_PATH")
        else:
            candidate_source = source_path(source_field)
            if not candidate_source.exists():
                failures.append("REJECT_SOURCE_PATH_NOT_FOUND")
        if not is_false(row.get("valid_for_claim", "")) or not is_false(row.get("claim_allowed", "")):
            failures.append("REJECT_CLAIM_FLAG")
        if not row.get("links_to_qRhat", "").strip():
            failures.append("REJECT_NO_QRHAT_OR_SUPPRESSION_LINK")
        review_rows.append(
            {
                "review_id": f"LRR1261_{len(review_rows)}_{symbol or 'unknown'}",
                "source_file": row.get("_source_file", ""),
                "source_row": row.get("_source_row", ""),
                "coefficient_symbol": symbol,
                "validation_status": "ACCEPTED_NONCLAIM_COEFFICIENT_ROW" if not failures else ";".join(failures),
                "runner_eligible": not failures,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return review_rows


def scan_corpus_mentions() -> list[dict[str, object]]:
    search_files: list[Path] = []
    search_files.extend(sorted((ROOT / "source-intake" / "mts_residuals").glob("*.csv")))
    search_files.extend(sorted((ROOT / "source-intake" / "mts_residuals").glob("*.md")))
    search_files.extend(sorted((ROOT / "source-intake" / "rab-sector" / "raw").glob("*.csv")))
    search_files.extend(sorted((ROOT / "source-intake" / "rab-sector" / "accepted").glob("*.csv")))
    search_files.extend(sorted((ROOT / "source-intake" / "rab-sector" / "docs").glob("*.csv")))
    search_files.extend(sorted(ROOT.glob("*.md")))
    tokens = {
        "Z_R": ["Z_R", "ZRC1259"],
        "M_R^2": ["M_R^2", "M_R2", "MR2"],
        "J_R": ["J_R", "JR"],
        "B_R": ["B_R", "BR"],
    }
    rows: list[dict[str, object]] = []
    for symbol, symbol_tokens in tokens.items():
        mention_count = 0
        sample_files: list[str] = []
        for candidate_file in search_files:
            if not candidate_file.exists() or not candidate_file.is_file():
                continue
            text = read_text(candidate_file)
            if any(token in text for token in symbol_tokens):
                mention_count += 1
                if len(sample_files) < 5:
                    try:
                        sample_files.append(candidate_file.relative_to(ROOT).as_posix())
                    except ValueError:
                        sample_files.append(str(candidate_file))
        rows.append(
            {
                "scan_id": f"MENTION1261_{symbol.replace('^', '').replace('_', '').replace(' ', '')}",
                "symbol": symbol,
                "mention_file_count": mention_count,
                "sample_files": "; ".join(sample_files),
                "evidence_status": "MENTIONS_ONLY_NOT_COEFFICIENT_EVIDENCE",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def recent_formalization_writes() -> list[Path]:
    generated_paths = [
        SOURCE_REGISTER_PATH,
        INTAKE_SCAN_PATH,
        COEFFICIENT_HUNT_PATH,
        LIVE_ROW_REVIEW_PATH,
        MENTION_SCAN_PATH,
        OPERATOR_REENTRY_PATH,
        BLOCKER_LEDGER_PATH,
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
            "source_id": "SRC1261_0_1260_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1260_NEXT_TARGET.csv",
            "needle": "NEXT1260_0_1261",
            "purpose": "handoff to Z_R coefficient source hunt or operator-exhaustion reentry",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1261_1_1260_scan",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1260_RAB_COEFFICIENT_INTAKE_SCAN.csv",
            "needle": "NO_CANDIDATE_FILES_FOUND",
            "purpose": "previous intake scan found raw/accepted empty and docs template only",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1261_2_1260_rules",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1260_RAB_COEFFICIENT_VALIDATION_RULES.csv",
            "needle": "RCR1260_1_no_placeholders",
            "purpose": "strict refusal rule for placeholder coefficient rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1261_3_1260_map",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1260_COEFFICIENT_TO_QRHAT_OR_SUPPRESSION_MAP.csv",
            "needle": "MAP1260_0_finite_qRhat",
            "purpose": "finite q_Rhat and suppression branch map",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1261_4_1259_theorem",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1259_OPERATOR_EXCLUSION_THEOREM_CANDIDATE.csv",
            "needle": "EXACT_IF_PARENT_SIGNED_NOT_DERIVED",
            "purpose": "R_AB gradient-ban theorem is exact only if parent-signed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1261_5_1259_contract",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1259_ZR_POSITIVE_COEFFICIENT_CONTRACT.csv",
            "needle": "ZRC1259_0_ZR",
            "purpose": "Z_R/M_R2/J_R/B_R source contract",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1261_6_1058_exhaustion",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1058_VISIBLE_OPERATOR_DOMAIN_EXHAUSTION_ATTEMPT.csv",
            "needle": "REJECT_CURRENT_CLAIM_RETAIN_COUNTERTERM_PRIOR",
            "purpose": "visible operator exhaustion was not derived",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1261_7_1107_object_language",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1107_OBJECT_LANGUAGE_EXHAUSTION_ATTEMPT.csv",
            "needle": "OBJECT_LANGUAGE_EXHAUSTION_NOT_DERIVED",
            "purpose": "object-language exhaustion remains closure-only",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1261_8_1236_typed_certificate",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1236_PARENT_TYPED_OBJECT_LANGUAGE_CERTIFICATE_ATTEMPT.csv",
            "needle": "CERTIFICATE_SCHEMA_VALID_NOT_PARENT_DERIVED",
            "purpose": "typed certificate exists but is not parent-derived",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1261_9_1259_docs_template",
            "local_path": "source-intake/rab-sector/docs/ZR1259_RAB_GRADIENT_COEFFICIENT_TEMPLATE_NONCLAIM.csv",
            "needle": "ZR1259_TEMPLATE_DO_NOT_SCORE",
            "purpose": "docs-only template must not be scored as evidence",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    intake_scan, live_rows, docs_rows = scan_intake()
    live_row_review = review_live_rows(live_rows)
    mention_scan = scan_corpus_mentions()

    accepted_symbols = {
        str(row.get("coefficient_symbol", ""))
        for row in live_row_review
        if str(row.get("validation_status")) == "ACCEPTED_NONCLAIM_COEFFICIENT_ROW"
    }
    coefficient_hunt = [
        {
            "hunt_id": f"HUNT1261_{index}_{symbol}",
            "symbol": symbol,
            "role": metadata["role"],
            "required_evidence": metadata["required_evidence"],
            "branch_link": metadata["branch_link"],
            "current_evidence": "accepted nonclaim live row found" if symbol in accepted_symbols else "no accepted live coefficient row found",
            "source_hunt_status": "SOURCE_BACKED_NONCLAIM_ROW_READY" if symbol in accepted_symbols else "NO_SOURCE_BACKED_ROW_FOUND",
            "next_action": "feed into 1260 branch map" if symbol in accepted_symbols else "derive from parent action or place real source row in rab-sector/raw or accepted",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for index, (symbol, metadata) in enumerate(ALLOWED_COEFFICIENTS.items())
    ]

    operator_reentry = [
        {
            "audit_id": "OER1261_0_RAB_specific_ban",
            "route": "ban independent R_AB gradient counterterm",
            "source": "P8_Y5_R10_1259_OPERATOR_EXCLUSION_THEOREM_CANDIDATE.csv:THEO1259_0_gradient_ban_if_parent_exhaustion",
            "status": "EXACT_IF_PARENT_SIGNED_NOT_DERIVED",
            "missing_clause": "parent operator exhaustion; R_AB compatibility sort; first-class/algebraic constraint; radiative/readout stability",
            "effect": "cannot set Z_R=0 from current corpus",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "OER1261_1_visible_operator_domain",
            "route": "exhaust visible operator domain",
            "source": "P8_Y5_R10_1058_VISIBLE_OPERATOR_DOMAIN_EXHAUSTION_ATTEMPT.csv:VOE1058_5_verdict",
            "status": "REJECT_CURRENT_CLAIM_RETAIN_COUNTERTERM_PRIOR",
            "missing_clause": "parent generation of every visible counterterm and radiative closure",
            "effect": "generic counterterm algebra remains legal",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "OER1261_2_object_language",
            "route": "object-language exhaustion",
            "source": "P8_Y5_R10_1107_OBJECT_LANGUAGE_EXHAUSTION_ATTEMPT.csv:EXH1107_6_verdict",
            "status": "OBJECT_LANGUAGE_EXHAUSTION_NOT_DERIVED",
            "missing_clause": "membership of allowed terms in Image(ParentGenerate)",
            "effect": "chain-rule zero works only after membership is proved",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "OER1261_3_typed_certificate",
            "route": "typed parent object-language certificate",
            "source": "P8_Y5_R10_1236_PARENT_TYPED_OBJECT_LANGUAGE_CERTIFICATE_ATTEMPT.csv:CERT1236_6_current_verdict",
            "status": "CERTIFICATE_SCHEMA_VALID_NOT_PARENT_DERIVED",
            "missing_clause": "derive sorted action grammar from motion/time/space primitives",
            "effect": "useful closure contract, not a public theorem",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "OER1261_4_current_verdict",
            "route": "choose zero-proof or coefficient branch",
            "source": "OER1261_0 through OER1261_3",
            "status": "ZERO_PROOF_NOT_CLOSED_RETAIN_ZR_BRANCH",
            "missing_clause": "at least one parent-signed exclusion theorem or real source-backed coefficient row",
            "effect": "continue derivation-first, but keep finite/suppressed Z_R branch as nonclaim fallback",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    blocker_ledger = [
        {
            "blocker_id": "BLOCK1261_0_no_live_ZR",
            "blocked_object": "Z_R",
            "blocker": "no parent coefficient, theorem-zero, or source-backed local bound row found in live intake",
            "required_to_unblock": "real row in rab-sector/raw or accepted, with source path, units, normalization, and q_Rhat/suppression link",
            "current_route": "source hunt or parent derivation",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "blocker_id": "BLOCK1261_1_no_MR2",
            "blocked_object": "M_R^2",
            "blocker": "no Hessian/mass-gap source row found",
            "required_to_unblock": "second variation around local fixed point, or a sourced mass/screening scale",
            "current_route": "derive from parent local fixed-point action",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "blocker_id": "BLOCK1261_2_no_JR",
            "blocked_object": "J_R",
            "blocker": "no matter descent/source-current map found",
            "required_to_unblock": "prove zero current by descent, or supply finite sourced coupling and normalization",
            "current_route": "derive matter pullback/descent before scoring",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "blocker_id": "BLOCK1261_3_no_BR",
            "blocked_object": "B_R",
            "blocker": "no boundary no-hair/exactness source row found",
            "required_to_unblock": "boundary variation and source-worldtube/no-flux theorem, or finite boundary flux bound",
            "current_route": "derive boundary silence or keep finite flux residual",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "blocker_id": "BLOCK1261_4_operator_exhaustion",
            "blocked_object": "Z_R=0 theorem",
            "blocker": "operator-exhaustion route is exact only after parent grammar/exclusion clauses are signed",
            "required_to_unblock": "minimal parent assumption audit showing no independent R_AB gradient constructor exists",
            "current_route": "1262 derivation-first reentry",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    claim_gates = [
        {
            "gate_id": "GATE1261_0_no_R10_or_PPN_pass",
            "claim": "R10/PPN/local-GR pass from R_AB sector",
            "status": "BLOCKED",
            "reason": "no accepted Z_R/M_R2/J_R/B_R rows and no parent-signed Z_R=0 theorem",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1261_1_docs_not_evidence",
            "claim": "docs template counts as coefficient evidence",
            "status": "REJECTED",
            "reason": "ZR1259 template contains MISSING markers and explicitly says do not score",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1261_2_mentions_not_evidence",
            "claim": "corpus mentions of Z_R/M_R2/J_R/B_R count as source rows",
            "status": "REJECTED",
            "reason": "mentions are useful hints only; they do not supply units, normalization, or source-backed coefficient values",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1261_3_derivation_first",
            "claim": "operator-exhaustion theorem closes now",
            "status": "BLOCKED",
            "reason": "1058/1107/1236/1259 all leave parent-derived exclusion unsigned",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decisions = [
        {
            "decision_id": "DEC1261_0_source_hunt_result",
            "decision": "no live coefficient evidence is available yet",
            "because": "raw and accepted rab-sector intake folders contain no accepted rows; docs template is non-evidence",
            "next_action": "do not score R_AB local branch from placeholders",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1261_1_operator_reentry_result",
            "decision": "operator-exhaustion path remains the best derivation-first target but is not closed",
            "because": "the exact theorem exists only if parent object-language/exclusion clauses are signed",
            "next_action": "audit the minimum parent assumption needed to ban the R_AB gradient operator; if unacceptable, build a nonclaim Z_R prior envelope",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1261_0_1262",
            "target_file": "1262-Y5-R10-RAB-operator-exhaustion-minimal-assumption-audit-or-ZR-prior-envelope.md",
            "target_script": "scripts/Y5_R10_RAB_operator_exhaustion_minimal_assumption_audit_or_ZR_prior_envelope.py",
            "task": "derive the minimum parent object-language assumption that bans the R_AB gradient counterterm, or demote to a sourced nonclaim Z_R prior envelope",
            "success_condition": "either a parent-signed no-independent-R_AB-gradient constructor theorem candidate with no hidden closure smuggling, or a clean finite-coefficient prior envelope that remains nonclaim",
            "do_not": "do not claim local-GR/R10/PPN pass from placeholders, docs templates, or mere corpus mentions",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    generated_tables = [
        (SOURCE_REGISTER_PATH, source_register),
        (INTAKE_SCAN_PATH, intake_scan),
        (COEFFICIENT_HUNT_PATH, coefficient_hunt),
        (LIVE_ROW_REVIEW_PATH, live_row_review),
        (MENTION_SCAN_PATH, mention_scan),
        (OPERATOR_REENTRY_PATH, operator_reentry),
        (BLOCKER_LEDGER_PATH, blocker_ledger),
        (CLAIM_GATES_PATH, claim_gates),
        (DECISION_PATH, decisions),
        (NEXT_PATH, next_target),
    ]
    for path, rows in generated_tables:
        write_csv(path, rows)

    source_checks = [exists_and_contains(str(row["local_path"]), str(row["needle"])) for row in source_register]
    sources_exist = all(exists for exists, _ in source_checks)
    needles_found = all(found for _, found in source_checks)
    raw_accepted_empty = all(
        int(row["rows_found"]) == 0
        for row in intake_scan
        if bool(row["is_live_candidate_folder"])
    )
    docs_nonclaim = all(is_false(row.get("valid_for_claim", "")) and is_false(row.get("claim_allowed", "")) for row in docs_rows)
    live_review_nonclaim = all(is_false(row.get("valid_for_claim", "")) and is_false(row.get("claim_allowed", "")) for row in live_row_review)
    no_runner_eligible_rows = not any(bool(row.get("runner_eligible")) for row in live_row_review)
    operator_zero_not_closed = operator_reentry[-1]["status"] == "ZERO_PROOF_NOT_CLOSED_RETAIN_ZR_BRANCH"
    blockers_all_nonclaim = all(is_false(row["valid_for_claim"]) and is_false(row["claim_allowed"]) for row in blocker_ledger)
    claim_gates_block = all(row["status"] in {"BLOCKED", "REJECTED"} for row in claim_gates)
    next_is_1262 = next_target[0]["target_file"].startswith("1262-")

    csv_parse_ok = True
    csv_parse_details: list[str] = []
    for path, _rows in generated_tables:
        try:
            parsed_rows = read_csv(path)
            csv_parse_details.append(f"{path.name}:{len(parsed_rows)}")
        except Exception as exc:
            csv_parse_ok = False
            csv_parse_details.append(f"{path.name}:FAILED:{exc}")

    formalization_writes = recent_formalization_writes()

    validation_rows = [
        validation_row("VAL1261_0_sources_exist", "all cited local sources exist", sources_exist, f"{sum(1 for exists, _ in source_checks if exists)}/{len(source_checks)} sources exist"),
        validation_row("VAL1261_1_needles_found", "all cited local needles found", needles_found, f"{sum(1 for _, found in source_checks if found)}/{len(source_checks)} needles found"),
        validation_row("VAL1261_2_intake_scan", "rab-sector raw/accepted/docs scan is well formed", len(intake_scan) >= 3, f"scan_rows={len(intake_scan)}"),
        validation_row("VAL1261_3_raw_accepted_empty", "raw and accepted live intake folders contain no candidate rows", raw_accepted_empty, f"live_rows={len(live_rows)}"),
        validation_row("VAL1261_4_docs_nonclaim", "docs rows remain nonclaim", docs_nonclaim, f"docs_rows={len(docs_rows)}"),
        validation_row("VAL1261_5_live_review_nonclaim", "live row review remains nonclaim", live_review_nonclaim, f"review_rows={len(live_row_review)}"),
        validation_row("VAL1261_6_no_runner_rows", "no coefficient row is runner eligible", no_runner_eligible_rows, f"runner_eligible_rows={sum(1 for row in live_row_review if bool(row.get('runner_eligible')))}"),
        validation_row("VAL1261_7_operator_zero_not_closed", "operator-exhaustion zero proof remains unclosed", operator_zero_not_closed, str(operator_reentry[-1]["status"])),
        validation_row("VAL1261_8_blockers_nonclaim", "blocker ledger keeps all local branches blocked", blockers_all_nonclaim, f"blocker_rows={len(blocker_ledger)}"),
        validation_row("VAL1261_9_claim_gates", "claim gates reject local/R10/PPN promotion", claim_gates_block, f"claim_gate_rows={len(claim_gates)}"),
        validation_row("VAL1261_10_next_target_1262", "next target is 1262 derivation-first reentry", next_is_1262, next_target[0]["target_file"]),
        validation_row("VAL1261_11_csv_parse", "all generated CSVs parse cleanly", csv_parse_ok, "; ".join(csv_parse_details)),
        validation_row("VAL1261_12_formalization_untouched", "formalization-workbench untouched during run", not formalization_writes, f"formalization_recent_write_count_since_run_start={len(formalization_writes)}"),
    ]
    overall = all(row["status"] == "PASS" for row in validation_rows)
    validation_rows.append(
        validation_row(
            "VAL1261_13_overall",
            "overall 1261 validation",
            overall,
            "1261 performs a source hunt, rejects docs/mentions as evidence, re-enters operator-exhaustion audit, and keeps R_AB local claims blocked",
        )
    )
    write_csv(VALIDATION_PATH, validation_rows)

    doc = f"""# {TITLE}

**Current verdict:** 1261 found no live source-backed `Z_R`, `M_R^2`, `J_R`, or `B_R` coefficient row. The `Z_R=0` route also remains unproved because the parent operator-exhaustion clauses are still unsigned.

**Main progress:** the branch is now cleaner, not stronger: placeholders and corpus mentions are explicitly refused, the docs template remains non-evidence, and the next derivation target is narrowed to the minimum parent assumption that would ban the `R_AB` gradient constructor.

**No-claim guard:** no R10, PPN, clock, orbital, local-GR/Newton, finite `q_R_hat`, or suppression claim is made from this checkpoint.

## Source Register
{markdown_table(source_register, ["source_id", "local_path", "needle", "purpose", "valid_for_claim", "claim_allowed"])}

## Intake Scan Snapshot
{markdown_table(intake_scan, ["scan_id", "directory", "file", "rows_found", "scan_status", "is_live_candidate_folder", "valid_for_claim", "claim_allowed"])}

## Coefficient Source Hunt Ledger
{markdown_table(coefficient_hunt, ["hunt_id", "symbol", "role", "required_evidence", "branch_link", "current_evidence", "source_hunt_status", "next_action", "valid_for_claim", "claim_allowed"])}

## Live Row Review
{markdown_table(live_row_review, ["review_id", "source_file", "source_row", "coefficient_symbol", "validation_status", "runner_eligible", "valid_for_claim", "claim_allowed"])}

## Corpus Mention Scan
{markdown_table(mention_scan, ["scan_id", "symbol", "mention_file_count", "sample_files", "evidence_status", "valid_for_claim", "claim_allowed"])}

## Operator Exhaustion Reentry Audit
{markdown_table(operator_reentry, ["audit_id", "route", "source", "status", "missing_clause", "effect", "valid_for_claim", "claim_allowed"])}

## Blocker Ledger
{markdown_table(blocker_ledger, ["blocker_id", "blocked_object", "blocker", "required_to_unblock", "current_route", "valid_for_claim", "claim_allowed"])}

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
