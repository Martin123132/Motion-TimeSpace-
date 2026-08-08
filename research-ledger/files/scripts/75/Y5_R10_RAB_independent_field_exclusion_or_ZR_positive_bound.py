from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


PACK_ID = "P8_Y5_R10_1258"
TITLE = "1258-Y5-R10-RAB-independent-field-exclusion-or-ZR-positive-bound"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_STARTED_UTC = datetime.now(timezone.utc)


SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
FIELD_STATUS_TESTS_PATH = OUT_DIR / f"{PACK_ID}_RAB_FIELD_STATUS_TESTS.csv"
EXCLUSION_CERTIFICATE_PATH = OUT_DIR / f"{PACK_ID}_FIELD_EXCLUSION_CERTIFICATE_ATTEMPT.csv"
COUNTERTERM_RISK_PATH = OUT_DIR / f"{PACK_ID}_RAB_GRADIENT_COUNTERTERM_RISK_LEDGER.csv"
ZR_HANDOFF_PATH = OUT_DIR / f"{PACK_ID}_ZR_POSITIVE_HANDOFF.csv"
CLAIM_GATES_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATES.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1258_VALIDATION.csv"


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


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    source_register = [
        {
            "source_id": "SRC1258_0_1257_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1257_NEXT_TARGET.csv",
            "needle": "NEXT1257_0_1258",
            "purpose": "handoff to R_AB field-status exclusion attempt",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1258_1_1257_selector",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1257_ZR_LAMBDAR_SELECTOR_CLAUSES.csv",
            "needle": "SEL1257_0_field_exclusion",
            "purpose": "field-exclusion selector clause",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1258_2_1236_typed",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1236_PARENT_TYPED_OBJECT_LANGUAGE_CERTIFICATE_ATTEMPT.csv",
            "needle": "CERTIFICATE_SCHEMA_VALID_NOT_PARENT_DERIVED",
            "purpose": "typed object-language certificate exists but is not parent-derived",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1258_3_1107_exhaustion",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1107_OBJECT_LANGUAGE_EXHAUSTION_ATTEMPT.csv",
            "needle": "OBJECT_LANGUAGE_EXHAUSTION_NOT_DERIVED",
            "purpose": "object-language exhaustion/membership not derived",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1258_4_1009_sector",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1009_PARENT_SECTOR_CONTRACT.csv",
            "needle": "PCS1009_9_total_parent_contract",
            "purpose": "total parent sector field list is not promoted",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1258_5_1009_gate",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1009_CLAIM_GATE.csv",
            "needle": "sector action blocks are candidates, not a signed parent action",
            "purpose": "total parent action not accepted",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1258_6_10_observer",
            "local_path": "10-observer-map-symplectic-contract.md",
            "needle": "R_AB = ln(T^2 S) = 2 ln(J_q)",
            "purpose": "R_AB as observer/coframe compatibility strain",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1258_7_1256_contract",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1256_MINIMAL_HCORE_SOURCE_EQUATION_CONTRACT.csv",
            "needle": "Z_R h^{ij} D_i R_AB D_j R_AB",
            "purpose": "formal Z_R kinetic contract from 1256",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    field_status_tests = [
        {
            "test_id": "FST1258_0_not_listed",
            "test": "R_AB appears as an explicit parent field in the inspected sector contract",
            "evidence": "1009 sector contract does not list R_AB as parent field",
            "result": "ABSENCE_NOT_PROOF",
            "reason": "1009 total parent action is itself not promoted and not an exhaustive field list",
            "effect": "cannot certify Z_R=0 from non-listing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "test_id": "FST1258_1_observer_composite",
            "test": "R_AB is defined as composite observer/coframe strain",
            "evidence": "10 gives R_AB=ln(T^2 S)=2 ln(J_q)",
            "result": "SUPPORTS_COMPATIBILITY_READING",
            "reason": "R_AB is naturally a readout/compatibility scalar, but composite scalars can still appear in higher-gradient counterterms unless banned",
            "effect": "supports but does not prove independent-field exclusion",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "test_id": "FST1258_2_typed_object_certificate",
            "test": "typed object-language certificate excludes R_AB kinetic/gradient operators",
            "evidence": "1236 certificate schema is valid but not parent-derived",
            "result": "CONDITIONAL_ONLY",
            "reason": "the grammar can exclude terms only if parent-signed",
            "effect": "cannot ban Z_R today",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "test_id": "FST1258_3_operator_exhaustion",
            "test": "object-language exhaustion leaves no room for a (nabla R_AB)^2 counterterm",
            "evidence": "1107 says membership in Image(ParentGenerate) is not derived and counterterms remain legal in analogous cases",
            "result": "FAIL_CURRENT_CORPUS",
            "reason": "without exhaustion, allowed local operators are not proven limited to the desired parent-generated image",
            "effect": "Z_R-positive/counterterm risk remains open",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "test_id": "FST1258_4_constraint_origin",
            "test": "R_AB is removed by first-class/algebraic constraint",
            "evidence": "1257 and 07 identify clean route but parent origin is open",
            "result": "NOT_PROVED",
            "reason": "lambda_R origin and Dirac chain are unsigned",
            "effect": "Z_R=0 remains conditional",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    exclusion_certificate = [
        {
            "certificate_id": "EXC1258_0_RAB_field_exclusion",
            "claim": "R_AB is not an independent propagating parent field and therefore Z_R=0",
            "status": "REJECT_CERTIFICATE_CURRENT_CORPUS",
            "supporting_evidence": "R_AB is naturally composite/readout: R_AB=ln(T^2S)=2ln(J_q)",
            "failed_requirements": "exhaustive parent field list; parent-signed typed grammar; no-gradient counterterm theorem; lambda_R/constraint origin",
            "consequence": "do not select Z_R=0; keep kinetic/suppressed branches open",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    counterterm_risk = [
        {
            "risk_id": "CTR1258_0_composite_gradient",
            "candidate_operator": "int sqrt(h) Z_R h^{ij} D_i R_AB D_j R_AB",
            "why_allowed_if_unsigned": "R_AB is a scalar composite of local readout/coframe variables; without EH/operator-exhaustion a gradient counterterm is not syntactically forbidden",
            "risk_to_GR_route": "produces Q_R hair or requires finite/suppressed residual scoring",
            "needed_ban": "parent object-language exhaustion or first-class constraint showing this operator is illegal/redundant",
            "current_status": "RETAIN_RISK",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "risk_id": "CTR1258_1_higher_derivative_metric",
            "candidate_operator": "if R_AB is metric/coframe composite, (nabla R_AB)^2 behaves like extra higher-gradient gravitational/readout operator",
            "why_allowed_if_unsigned": "minimal EH-only operator content is not yet derived for full MTS parent action",
            "risk_to_GR_route": "local PPN deviations or extra boundary charge",
            "needed_ban": "EH minimality plus readout stability theorem",
            "current_status": "RETAIN_RISK",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    zr_handoff = [
        {
            "handoff_id": "ZRH1258_0_zero_route",
            "route": "Z_R=0/lambda_R",
            "status_after_1258": "CONDITIONAL_NOT_SELECTED",
            "why": "field-exclusion certificate failed current corpus",
            "next_requirement": "derive object-language/operator ban or first-class R_AB constraint",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "handoff_id": "ZRH1258_1_positive_route",
            "route": "Z_R-positive finite/suppressed branch",
            "status_after_1258": "RETAINED_AS_REQUIRED_FALLBACK",
            "why": "gradient counterterm/independent-field possibility is not banned",
            "next_requirement": "source or bound Z_R, M_R^2, J_R, and B_R, or prove the gradient operator is illegal",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "handoff_id": "ZRH1258_2_boundary_route",
            "route": "boundary no-hair with Z_R present",
            "status_after_1258": "RETAINED",
            "why": "even a kinetic R_AB branch can be safe if physical source boundaries are no-flux/exact",
            "next_requirement": "source-worldtube boundary class and no-flux theorem",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    claim_gates = [
        {
            "gate_id": "GATE1258_0_field_exclusion",
            "claim": "R_AB independent-field exclusion is proved",
            "status": "BLOCKED",
            "reason": "supporting composite evidence exists but parent field list/object-language exhaustion/constraint origin are unsigned",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1258_1_ZR_zero",
            "claim": "Z_R=0 is selected",
            "status": "BLOCKED",
            "reason": "field-exclusion certificate rejected for current corpus",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1258_2_ZR_positive_bound",
            "claim": "Z_R-positive branch has a sourced coefficient/bound",
            "status": "BLOCKED",
            "reason": "1258 retains the branch but does not source Z_R/M_R^2/J_R/B_R",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1258_3_local_GR",
            "claim": "local GR/Newton branch is derived",
            "status": "BLOCKED",
            "reason": "the field-status proof fails; zero, finite, mass-gap, and boundary routes remain open",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decisions = [
        {
            "decision_id": "DEC1258_0_no_exclusion_claim",
            "decision": "do not claim R_AB field exclusion",
            "because": "R_AB is composite/readout-like, but object-language exhaustion and total field list are not parent-derived",
            "next_action": "attack the narrower R_AB gradient-counterterm ban or source Z_R-positive coefficients",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1258_1_best_next",
            "decision": "next target is the R_AB gradient-counterterm ban",
            "because": "banning int Z_R (nabla R_AB)^2 would recover the clean zero route without needing to call R_AB a fundamental field",
            "next_action": "1259-Y5-R10-RAB-gradient-counterterm-ban-or-ZR-source-row.md",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1258_0_1259",
            "target_file": "1259-Y5-R10-RAB-gradient-counterterm-ban-or-ZR-source-row.md",
            "target_script": "scripts/Y5_R10_RAB_gradient_counterterm_ban_or_ZR_source_row.py",
            "task": "try to ban the R_AB gradient/kinetic counterterm from the parent object language; if the ban fails, create a nonclaim Z_R/M_R2/J_R/B_R source-row contract",
            "success_condition": "either a parent-signed operator-exclusion theorem candidate for Z_R=0, or a strict finite/suppressed coefficient intake ledger",
            "do_not": "do not treat R_AB composite status alone as a counterterm ban",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    generated_tables = [
        (SOURCE_REGISTER_PATH, source_register),
        (FIELD_STATUS_TESTS_PATH, field_status_tests),
        (EXCLUSION_CERTIFICATE_PATH, exclusion_certificate),
        (COUNTERTERM_RISK_PATH, counterterm_risk),
        (ZR_HANDOFF_PATH, zr_handoff),
        (CLAIM_GATES_PATH, claim_gates),
        (DECISION_PATH, decisions),
        (NEXT_PATH, next_target),
    ]

    for path, rows in generated_tables:
        write_csv(path, rows)

    source_checks = [exists_and_contains(str(row["local_path"]), str(row["needle"])) for row in source_register]
    sources_exist = all(exists for exists, _ in source_checks)
    needles_found = all(found for _, found in source_checks)
    tests_complete = {row["test_id"] for row in field_status_tests} == {
        "FST1258_0_not_listed",
        "FST1258_1_observer_composite",
        "FST1258_2_typed_object_certificate",
        "FST1258_3_operator_exhaustion",
        "FST1258_4_constraint_origin",
    }
    certificate_rejected = exclusion_certificate[0]["status"] == "REJECT_CERTIFICATE_CURRENT_CORPUS"
    counterterm_retained = all(row["current_status"] == "RETAIN_RISK" for row in counterterm_risk)
    handoff_keeps_positive = any(row["route"] == "Z_R-positive finite/suppressed branch" and row["status_after_1258"] == "RETAINED_AS_REQUIRED_FALLBACK" for row in zr_handoff)
    claims_ok = all(row["status"] == "BLOCKED" and is_false(row["claim_allowed"]) for row in claim_gates)
    all_nonclaim = all(
        is_false(row.get("valid_for_claim", "")) and is_false(row.get("claim_allowed", ""))
        for _, rows in generated_tables
        for row in rows
    )
    next_is_1259 = next_target[0]["target_file"].startswith("1259-")

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
        validation_row("VAL1258_0_sources_exist", "all cited local sources exist", sources_exist, f"{sum(1 for exists, _ in source_checks if exists)}/{len(source_checks)} sources exist"),
        validation_row("VAL1258_1_needles_found", "all cited local needles found", needles_found, f"{sum(1 for _, found in source_checks if found)}/{len(source_checks)} needles found"),
        validation_row("VAL1258_2_tests_complete", "field-status tests cover listing/composite/typing/exhaustion/constraint", tests_complete, f"test_rows={len(field_status_tests)}"),
        validation_row("VAL1258_3_certificate_rejected", "R_AB field-exclusion certificate is rejected for current corpus", certificate_rejected, exclusion_certificate[0]["status"]),
        validation_row("VAL1258_4_counterterm_retained", "R_AB gradient counterterm risk remains retained", counterterm_retained, f"counterterm_rows={len(counterterm_risk)}"),
        validation_row("VAL1258_5_positive_handoff", "Z_R-positive fallback remains open", handoff_keeps_positive, "Z_R-positive finite/suppressed branch retained"),
        validation_row("VAL1258_6_claim_gates", "claim gates block field exclusion/Z_R/local GR", claims_ok, f"claim_gate_rows={len(claim_gates)}"),
        validation_row("VAL1258_7_nonclaim_policy", "all generated rows remain nonclaim", all_nonclaim, "valid_for_claim=false and claim_allowed=false throughout generated tables"),
        validation_row("VAL1258_8_next_target_1259", "next target is R_AB gradient-counterterm ban or Z_R source row", next_is_1259, str(next_target[0]["target_file"])),
        validation_row("VAL1258_9_csv_parse", "all generated CSVs parse cleanly", csv_parse_ok, "; ".join(csv_parse_details)),
        validation_row("VAL1258_10_formalization_untouched", "formalization-workbench untouched during run", not formalization_writes, f"formalization_recent_write_count_since_run_start={len(formalization_writes)}"),
    ]
    overall = all(row["status"] == "PASS" for row in validation_rows)
    validation_rows.append(
        validation_row(
            "VAL1258_11_overall",
            "overall 1258 validation",
            overall,
            "1258 rejects the R_AB field-exclusion certificate for the current corpus and routes next to gradient-counterterm ban or Z_R source row",
        )
    )
    write_csv(VALIDATION_PATH, validation_rows)

    doc = f"""# {TITLE}

**Current verdict:** 1258 does **not** prove that `R_AB` is excluded as an independent propagating parent field. `R_AB` is strongly readout/composite-like, but that alone does not ban a gradient/kinetic counterterm.

**Main progress:** the clean zero route now has a sharper missing theorem: ban `int Z_R (nabla R_AB)^2` from the parent object language, or keep the `Z_R>0` finite/suppressed branch and source its coefficients.

**No-claim guard:** no `R_AB` field-exclusion certificate, `Z_R=0`, `Q_R=0`, finite MTS `q_R_hat` prediction, or local-GR/Newton derivation is promoted.

Generated UTC: {datetime.now(timezone.utc).isoformat()}

## Source Register
{markdown_table(source_register, ["source_id", "local_path", "needle", "purpose", "valid_for_claim", "claim_allowed"])}

## R_AB Field Status Tests
{markdown_table(field_status_tests, ["test_id", "test", "evidence", "result", "reason", "effect", "valid_for_claim", "claim_allowed"])}

## Field Exclusion Certificate Attempt
{markdown_table(exclusion_certificate, ["certificate_id", "claim", "status", "supporting_evidence", "failed_requirements", "consequence", "valid_for_claim", "claim_allowed"])}

## R_AB Gradient Counterterm Risk Ledger
{markdown_table(counterterm_risk, ["risk_id", "candidate_operator", "why_allowed_if_unsigned", "risk_to_GR_route", "needed_ban", "current_status", "valid_for_claim", "claim_allowed"])}

## Z_R Positive Handoff
{markdown_table(zr_handoff, ["handoff_id", "route", "status_after_1258", "why", "next_requirement", "valid_for_claim", "claim_allowed"])}

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
