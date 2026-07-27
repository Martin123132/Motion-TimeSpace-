from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


PACK_ID = "P8_Y5_R10_1270"
TITLE = "1270-Y5-R10-RAB-quotient-map-parent-sort-derivation-or-finite-ZR-first-source-row"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
RAB_INTAKE_DIR = ROOT / "source-intake" / "rab-sector"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_STARTED_UTC = datetime.now(timezone.utc)


SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
QUOTIENT_SORT_PATH = OUT_DIR / f"{PACK_ID}_RAB_QUOTIENT_SORT_DERIVATION_ATTEMPT.csv"
DQ_TEST_PATH = OUT_DIR / f"{PACK_ID}_DQ_KERNEL_TEST_MATRIX.csv"
ROUTE_SELECTION_PATH = OUT_DIR / f"{PACK_ID}_RAB_ROUTE_SELECTION_AFTER_QUOTIENT_TEST.csv"
FINITE_ROW_ATTEMPT_PATH = OUT_DIR / f"{PACK_ID}_FINITE_ZR_FIRST_SOURCE_ROW_ATTEMPT.csv"
VALIDATOR_RESCAN_PATH = OUT_DIR / f"{PACK_ID}_ZR_VALIDATOR_RESCAN.csv"
CLAIM_GATES_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATES.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1270_VALIDATION.csv"


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
    if str(row.get("valid_for_claim", "")).strip().lower() == "true" or str(row.get("claim_allowed", "")).strip().lower() == "true":
        reasons.append("CLAIM_FLAG_TRUE_REJECTED_IN_PRIVATE_NONCLAIM_PHASE")
    return {
        "scan_id": f"SCAN1270_{intake_class}_{path.stem}_{row_id}",
        "intake_class": intake_class,
        "file_path": str(path),
        "row_id": row_id,
        "coefficient_symbol": row.get("coefficient_symbol", ""),
        "status": "REJECT" if reasons else "ACCEPT_NONCLAIM_SOURCE_READY",
        "reasons": "|".join(reasons) if reasons else "NO_PLACEHOLDERS_SOURCE_ANCHOR_FOUND_NONCLAIM",
        "source_exists": source_exists,
        "anchor_found": anchor_found,
        "intake_eligible": not reasons,
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
        QUOTIENT_SORT_PATH,
        DQ_TEST_PATH,
        ROUTE_SELECTION_PATH,
        FINITE_ROW_ATTEMPT_PATH,
        VALIDATOR_RESCAN_PATH,
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
            "source_id": "SRC1270_0_1269_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1269_NEXT_TARGET.csv",
            "needle": "NEXT1269_0_1270",
            "purpose": "handoff to R_AB quotient-map parent sort derivation",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1270_1_1269_operator",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1269_OPERATOR_EXCLUSION_PARENT_SORT_ATTEMPT.csv",
            "needle": "OP1269_0_parent_sort",
            "purpose": "operator exclusion blocker requiring R_AB parent sort",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1270_2_1269_validator",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1269_ZR_INTAKE_VALIDATOR_SUMMARY.csv",
            "needle": "NO_ACCEPTED_SOURCE_READY_ROWS",
            "purpose": "current finite-ZR intake has no source-ready rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1270_3_637_qmap",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_637_QUOTIENT_MAP_DERIVATION.csv",
            "needle": "QM637_2_vertical_kernel",
            "purpose": "generic quotient kernel theorem",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1270_4_581_chain",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_581_QUOTIENT_VERTICAL_THEOREM_CHAIN.csv",
            "needle": "QVT581_0_parent_projection",
            "purpose": "quotient/vertical theorem chain",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1270_5_595_observed",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_595_PI_OBSERVED_QUOTIENT_MAP.csv",
            "needle": "PIM595_3_vertical_generator",
            "purpose": "formal observed quotient map and vertical generator contract",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1270_6_594_contract",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_594_QUOTIENT_MAP_CONSTRUCTION_CONTRACT.csv",
            "needle": "QMC594_1_vertical_generator",
            "purpose": "quotient-map construction contract",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1270_7_1263_rab",
            "local_path": "1263-Y5-R10-vertical-fibre-null-from-parent-presymplectic-degeneracy-or-RAB-prior-envelope-fill.md",
            "needle": "PND1263_2_RAB_vertical_generator",
            "purpose": "R_AB-specific vertical-generator blocker",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1270_8_1262_minimal",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1262_MINIMAL_ASSUMPTION_AUDIT.csv",
            "needle": "MIN1262_0_RAB_vertical_sort",
            "purpose": "R_AB vertical sort remains not parent-derived",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1270_9_760_descent",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_760_QUOTIENT_DESCENT_PROOF_ATTEMPT.csv",
            "needle": "QMD760_1_parent_quotient_object",
            "purpose": "matter/geometry descent requires parent quotient object",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1270_10_965_primitive",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_965_PRIMITIVE_QUOTIENT_THEOREM_ATTEMPT.csv",
            "needle": "PQ965_0_theorem_target",
            "purpose": "primitive quotient theorem remains not derived",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1270_11_728_omega",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_728_PARENT_OMEGA_CANDIDATE.csv",
            "needle": "OM728_4_reduced_Omega",
            "purpose": "reduced symplectic form not constructed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    quotient_sort_attempt = [
        {
            "attempt_id": "QSR1270_0_generic_q_kernel",
            "claim_piece": "generic quotient maps satisfy Dq[v]=0 for vertical generators",
            "test": "Use 637/581/595/594 generic quotient machinery.",
            "result": "GENERIC_CONDITIONAL_PASS",
            "why_not_enough_for_RAB": "generic theorem does not identify the actual R_AB variation as a parent null/representative direction",
            "claim_effect": "cannot parent-sign AP1265_0 or AP1265_1 for R_AB",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "QSR1270_1_observed_full_metric",
            "claim_piece": "q observes the local metric/coframe components containing T and S",
            "test": "If q includes A=T^2 and B=S separately, then delta R_AB=delta ln(A B) changes q.",
            "result": "DQ_NONZERO_COUNTERMODEL",
            "why_not_enough_for_RAB": "R_AB is PPN/light-cone relevant when A and B are observed separately",
            "claim_effect": "R_AB cannot be called vertical in this readout without extra parent quotient rule",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "QSR1270_2_reciprocal_class_q",
            "claim_piece": "q identifies reciprocal split changes and observes only a reduced class",
            "test": "Define q_R so changes in ln(T^2 S) are representative data.",
            "result": "VERTICAL_BY_DEFINITION_ONLY",
            "why_not_enough_for_RAB": "this smuggles the desired local-GR closure unless the parent primitive action proves this quotient before readout",
            "claim_effect": "not a derivation; it is a closure convention",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "QSR1270_3_auxiliary_before_q",
            "claim_piece": "R_AB is eliminated by auxiliary compatibility before q/readout",
            "test": "Use 1268 compatibility action: E_Lambda sets R_AB-C_AB=0 before observed geometry is evaluated.",
            "result": "BEST_ROUTE_BUT_NOT_QUOTIENT_SORT",
            "why_not_enough_for_RAB": "this can be exact if parent-signed, but it is algebraic elimination rather than Dq[v_R]=0",
            "claim_effect": "keeps second-class auxiliary route as best derivation path",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "QSR1270_4_presymplectic_null",
            "claim_piece": "R_AB variation is a presymplectic null generator",
            "test": "Need parent theta/Omega, R_AB vertical generator, and zero boundary charge.",
            "result": "NOT_DERIVED_FOR_RAB",
            "why_not_enough_for_RAB": "1263 says v_R, parent Omega, and boundary silence remain missing",
            "claim_effect": "cannot ban Z_R as a vertical-null contradiction yet",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "QSR1270_5_verdict",
            "claim_piece": "derive R_AB as parent quotient/vertical sort",
            "test": "QSR1270_0 through QSR1270_4 close without closure smuggling.",
            "result": "RAB_QUOTIENT_SORT_NOT_PARENT_SIGNED",
            "why_not_enough_for_RAB": "the only clean non-smuggling route is still parent-signed auxiliary compatibility or future finite residual sourcing",
            "claim_effect": "no AP1265_0/AP1265_1 promotion; no finite row created",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    dq_kernel_tests = [
        {
            "test_id": "DQ1270_0_full_metric_readout",
            "candidate_q": "q_full=(A=T^2,B=S,r,theta,...)",
            "candidate_vR": "delta R_AB=delta ln A + delta ln B",
            "Dq_result": "Dq_full[v_R] != 0 for generic delta R_AB",
            "status": "FAILS_VERTICALITY",
            "lesson": "full metric/coframe readout makes R_AB observable",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "test_id": "DQ1270_1_fixed_reciprocity_readout",
            "candidate_q": "q_GRlocal=(A,B with AB=1 already imposed)",
            "candidate_vR": "delta R_AB removed by constraint",
            "Dq_result": "no independent v_R exists after elimination",
            "status": "AUXILIARY_ELIMINATION_NOT_QUOTIENT_KERNEL",
            "lesson": "good if parent-signed, but it is not proof that R_AB was vertical before the constraint",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "test_id": "DQ1270_2_representative_class_readout",
            "candidate_q": "q_class=[A,B]/R_AB representative equivalence",
            "candidate_vR": "delta R_AB tangent to equivalence class",
            "Dq_result": "Dq_class[v_R]=0 by definition",
            "status": "CIRCULAR_UNLESS_PARENT_PRIMITIVE_PROVES_EQUIVALENCE",
            "lesson": "cannot define away a PPN-relevant component after seeing the problem",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "test_id": "DQ1270_3_generic_hidden_X",
            "candidate_q": "q_X from 637/581 quotient vertical chain",
            "candidate_vR": "identify v_R with generic v_X",
            "Dq_result": "conditional only if R_AB is proven to be that null representative",
            "status": "MISSING_IDENTIFICATION",
            "lesson": "generic quotient success does not transfer automatically to R_AB",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    route_selection = [
        {
            "route_id": "ROUTE1270_0_quotient_vertical",
            "route": "R_AB in ker(Dq) before variation",
            "current_status": "REJECT_CURRENT_PROMOTION",
            "reason": "full metric readout countermodel and missing R_AB-specific parent quotient equivalence",
            "next_requirement": "derive q_RAB and v_R field-by-field before readout",
            "selected_now": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "route_id": "ROUTE1270_1_auxiliary_compatibility",
            "route": "R_AB eliminated by parent-signed second-class compatibility action",
            "current_status": "BEST_DERIVATION_ROUTE_RETAINED",
            "reason": "does not require pretending R_AB is gauge; it only needs parent ownership and source/readout silence",
            "next_requirement": "prove parent necessity of compatibility block plus AP1265_2/3/4",
            "selected_now": True,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "route_id": "ROUTE1270_2_finite_ZR",
            "route": "finite/suppressed R_AB residual coefficient branch",
            "current_status": "FALLBACK_LOCKED_BY_VALIDATOR",
            "reason": "no source-backed finite row exists; templates are rejected",
            "next_requirement": "only create raw row with source path, anchor, units, normalization, and arena projection",
            "selected_now": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    validator_rescan = scan_rab_intake()
    accepted_ready = [row for row in validator_rescan if row["intake_eligible"] and row["intake_class"] in {"raw", "accepted"}]
    raw_rows = [row for row in validator_rescan if row["intake_class"] == "raw"]
    accepted_rows = [row for row in validator_rescan if row["intake_class"] == "accepted"]
    docs_rows = [row for row in validator_rescan if row["intake_class"] == "docs"]
    finite_row_attempt = [
        {
            "attempt_id": "FZR1270_0_first_raw_row",
            "action": "do not create first raw finite-ZR candidate row",
            "reason": "no source-backed coefficient/theorem row is available and the 1269/1270 validator accepts no raw/accepted rows",
            "raw_rows": len(raw_rows),
            "accepted_rows": len(accepted_rows),
            "accepted_ready_rows": len(accepted_ready),
            "template_rows_rejected": len([row for row in docs_rows if row["status"] == "REJECT"]),
            "status": "NO_SOURCE_BACKED_ROW_CREATED",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    claim_gates = [
        {
            "gate_id": "GATE1270_0_RAB_quotient_sort",
            "claim": "R_AB is parent-signed as a quotient/vertical sort in ker(Dq)",
            "status": "BLOCKED",
            "reason": "generic quotient machinery exists, but R_AB-specific Dq[v_R]=0 fails for full metric readout and is circular for class readout",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1270_1_AP1265_1",
            "claim": "operator exclusion follows from R_AB quotient sort",
            "status": "BLOCKED",
            "reason": "R_AB sort is not parent-signed; no vertical metric/readout closure remains open",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1270_2_finite_row",
            "claim": "first finite-ZR source row is accepted",
            "status": "BLOCKED",
            "reason": "no source-backed raw/accepted row exists; docs templates are rejected",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1270_3_local_tests",
            "claim": "local GR/R10/PPN/clock/orbital pass",
            "status": "BLOCKED",
            "reason": "neither quotient-zero, auxiliary-zero, nor finite residual row is claim-valid",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decisions = [
        {
            "decision_id": "DEC1270_0_no_quotient_shortcut",
            "decision": "do not treat R_AB as vertical by borrowing generic X quotient machinery",
            "because": "R_AB changes metric potentials seen by local tests unless the parent quotient/readout rule is independently derived",
            "status": "SHORTCUT_REJECTED",
            "next_action": "derive R_AB-specific q_RAB/v_R field map or stay with auxiliary compatibility",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1270_1_auxiliary_route",
            "decision": "keep parent-signed auxiliary compatibility as the best non-smuggling route",
            "because": "it eliminates R_AB before readout rather than pretending a readout-visible component is gauge",
            "status": "BEST_ROUTE_RETAINED_NONCLAIM",
            "next_action": "attack parent necessity and source/readout silence clauses",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1270_2_finite_row",
            "decision": "do not create a raw finite-ZR row yet",
            "because": "a serious source row needs source path, anchor, coefficient, units, normalization, and arena projection; none exists",
            "status": "VALIDATOR_PREVENTS_FAKE_EVIDENCE",
            "next_action": "source real finite coefficients or prove theorem-zero",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1270_0_1271",
            "target_file": "1271-Y5-R10-RAB-field-by-field-qRAB-vR-map-or-auxiliary-parent-necessity.md",
            "target_script": "scripts/Y5_R10_RAB_field_by_field_qRAB_vR_map_or_auxiliary_parent_necessity.py",
            "task": "try the only remaining quotient route honestly: write a field-by-field q_RAB/v_R map and test whether all observed metric, matter, clock, and boundary variables are invariant; if not, attack the parent necessity of the auxiliary compatibility block instead",
            "success_condition": "either a non-circular Dq[v_R]=0 map exists for R_AB before readout, or the auxiliary compatibility route gets a parent-necessity proof target with finite residual fallback retained",
            "do_not": "do not borrow generic X quotient results for R_AB without field identification, and do not create finite-ZR rows without validator acceptance",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    generated_tables = [
        (SOURCE_REGISTER_PATH, source_register),
        (QUOTIENT_SORT_PATH, quotient_sort_attempt),
        (DQ_TEST_PATH, dq_kernel_tests),
        (ROUTE_SELECTION_PATH, route_selection),
        (FINITE_ROW_ATTEMPT_PATH, finite_row_attempt),
        (VALIDATOR_RESCAN_PATH, validator_rescan),
        (CLAIM_GATES_PATH, claim_gates),
        (DECISION_PATH, decisions),
        (NEXT_PATH, next_target),
    ]
    for path, rows in generated_tables:
        write_csv(path, rows)

    source_checks = [exists_and_contains(row["local_path"], row["needle"]) for row in source_register]
    all_sources_exist = all(exists for exists, _ in source_checks)
    all_needles_found = all(found for _, found in source_checks)
    quotient_not_signed = any(
        row["attempt_id"] == "QSR1270_5_verdict" and row["result"] == "RAB_QUOTIENT_SORT_NOT_PARENT_SIGNED"
        for row in quotient_sort_attempt
    )
    dq_countermodel_present = any(row["status"] == "FAILS_VERTICALITY" for row in dq_kernel_tests)
    aux_selected = any(
        row["route_id"] == "ROUTE1270_1_auxiliary_compatibility"
        and str(row["selected_now"]).strip().lower() == "true"
        for row in route_selection
    )
    no_raw_row_created = finite_row_attempt[0]["status"] == "NO_SOURCE_BACKED_ROW_CREATED" and len(accepted_ready) == 0
    docs_rejected = len(docs_rows) > 0 and all(row["status"] == "REJECT" for row in docs_rows)
    validator_nonclaim = all(is_false(row["valid_for_claim"]) and is_false(row["claim_allowed"]) for row in validator_rescan)
    claim_gates_blocked = all(row["status"] == "BLOCKED" for row in claim_gates)
    all_generated_rows = [
        *source_register,
        *quotient_sort_attempt,
        *dq_kernel_tests,
        *route_selection,
        *finite_row_attempt,
        *validator_rescan,
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
            "VAL1270_0_sources_exist",
            "all cited local sources exist",
            all_sources_exist,
            f"{sum(1 for exists, _ in source_checks if exists)}/{len(source_checks)} sources exist",
        ),
        validation_row(
            "VAL1270_1_needles_found",
            "all cited local needles found",
            all_needles_found,
            f"{sum(1 for _, found in source_checks if found)}/{len(source_checks)} needles found",
        ),
        validation_row(
            "VAL1270_2_quotient_not_signed",
            "R_AB quotient sort is not parent-signed",
            quotient_not_signed,
            "QSR1270_5_verdict=RAB_QUOTIENT_SORT_NOT_PARENT_SIGNED",
        ),
        validation_row(
            "VAL1270_3_dq_countermodel",
            "Dq kernel matrix includes full metric readout countermodel",
            dq_countermodel_present,
            "DQ1270_0_full_metric_readout fails verticality",
        ),
        validation_row(
            "VAL1270_4_aux_route_retained",
            "auxiliary compatibility remains selected best route",
            aux_selected,
            "ROUTE1270_1_auxiliary_compatibility selected_now=True",
        ),
        validation_row(
            "VAL1270_5_no_finite_row_created",
            "no raw finite-ZR row is created without source-backed validator acceptance",
            no_raw_row_created,
            f"raw_rows={len(raw_rows)}; accepted_rows={len(accepted_rows)}; accepted_ready={len(accepted_ready)}",
        ),
        validation_row(
            "VAL1270_6_docs_rejected",
            "docs templates remain rejected by validator rescan",
            docs_rejected,
            f"docs_rows={len(docs_rows)}; rejected_docs={len([row for row in docs_rows if row['status'] == 'REJECT'])}",
        ),
        validation_row(
            "VAL1270_7_validator_nonclaim",
            "validator rescan remains nonclaim",
            validator_nonclaim,
            f"validator_rescan_rows={len(validator_rescan)}",
        ),
        validation_row(
            "VAL1270_8_claim_gates",
            "all claim gates remain blocked",
            claim_gates_blocked,
            f"claim_gate_rows={len(claim_gates)}",
        ),
        validation_row(
            "VAL1270_9_nonclaim_policy",
            "all generated rows remain nonclaim",
            nonclaim_policy,
            "valid_for_claim=false and claim_allowed=false throughout generated tables",
        ),
        validation_row(
            "VAL1270_10_next_target_1271",
            "next target routes to field-by-field q_RAB/v_R map or auxiliary parent necessity",
            next_target[0]["next_id"] == "NEXT1270_0_1271",
            str(next_target[0]["target_file"]),
        ),
        validation_row(
            "VAL1270_11_csv_parse",
            "all generated CSVs parse cleanly",
            csv_parse_ok,
            "; ".join(parsed_details),
        ),
        validation_row(
            "VAL1270_12_formalization_untouched",
            "formalization-workbench untouched by generated outputs",
            len(formalization_generated) == 0,
            f"formalization_generated_output_count={len(formalization_generated)}",
        ),
    ]
    overall_pass = all(row["status"] == "PASS" for row in validation)
    validation.append(
        validation_row(
            "VAL1270_13_overall",
            "overall 1270 validation",
            overall_pass,
            "1270 rejects a non-specific quotient shortcut for R_AB, records the full-metric Dq countermodel, retains auxiliary compatibility as best route, and refuses to create a finite-ZR row without source-backed validator acceptance",
        )
    )
    write_csv(VALIDATION_PATH, validation)

    doc = f"""# {TITLE}

**Current verdict:** 1270 does not derive `R_AB` as a parent quotient/vertical sort. Generic quotient machinery exists, but it cannot simply be borrowed for `R_AB`: if the observed local metric/coframe sees `A=T^2` and `B=S` separately, then changing `R_AB=ln(A B)` changes the observed geometry and `Dq[v_R]` is not zero.

**Main progress:** this blocks a subtle cheat. A quotient where `R_AB` is vertical can be defined, but unless the parent primitives prove that quotient before readout, it is just the local-GR closure in quotient clothing. The best non-smuggling route remains the second-class/algebraic auxiliary compatibility action.

**No-claim guard:** no `R_AB` quotient theorem, `Z_R=0`, local-GR/Newton, R10, PPN, clock, orbital, or finite-`Z_R` row is claimed. The finite-row path stays locked by the validator; no raw row was created.

Run timestamp UTC: `{RUN_STARTED_UTC.isoformat()}`

## Source Register
{markdown_table(source_register, ["source_id", "local_path", "needle", "purpose", "valid_for_claim", "claim_allowed"])}

## R_AB Quotient Sort Derivation Attempt
{markdown_table(quotient_sort_attempt, ["attempt_id", "claim_piece", "test", "result", "why_not_enough_for_RAB", "claim_effect", "valid_for_claim", "claim_allowed"])}

## Dq Kernel Test Matrix
{markdown_table(dq_kernel_tests, ["test_id", "candidate_q", "candidate_vR", "Dq_result", "status", "lesson", "valid_for_claim", "claim_allowed"])}

## R_AB Route Selection After Quotient Test
{markdown_table(route_selection, ["route_id", "route", "current_status", "reason", "next_requirement", "selected_now", "valid_for_claim", "claim_allowed"])}

## Finite Z_R First Source Row Attempt
{markdown_table(finite_row_attempt, ["attempt_id", "action", "reason", "raw_rows", "accepted_rows", "accepted_ready_rows", "template_rows_rejected", "status", "valid_for_claim", "claim_allowed"])}

## Z_R Validator Rescan
{markdown_table(validator_rescan, ["scan_id", "intake_class", "row_id", "coefficient_symbol", "status", "reasons", "source_exists", "anchor_found", "intake_eligible", "valid_for_claim", "claim_allowed"])}

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
