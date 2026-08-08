from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


PACK_ID = "P8_Y5_R10_1251"
TITLE = "1251-Y5-R10-Hcore-to-qRhat-coefficient-map-attempt-or-phenomenological-row"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_STARTED_UTC = datetime.now(timezone.utc)


SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
COEFFICIENT_MAP_ATTEMPT_PATH = OUT_DIR / f"{PACK_ID}_HCORE_TO_QRHAT_MAP_ATTEMPT.csv"
FORMAL_CHAIN_PATH = OUT_DIR / f"{PACK_ID}_FORMAL_CHAIN_NONCLAIM.csv"
PHENOMENOLOGICAL_ROW_STATUS_PATH = OUT_DIR / f"{PACK_ID}_PHENOMENOLOGICAL_ROW_STATUS.csv"
BLOCKER_LEDGER_PATH = OUT_DIR / f"{PACK_ID}_BLOCKER_LEDGER.csv"
CLAIM_GATES_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATES.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1251_VALIDATION.csv"


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

    source_register = [
        {
            "source_id": "SRC1251_0_1250_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1250_NEXT_TARGET.csv",
            "needle": "NEXT1250_0_1251",
            "purpose": "handoff to H_core-to-q_Rhat coefficient map attempt",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1251_1_1250_hcore",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1250_HCORE_COEFFICIENT_CHECKLIST.csv",
            "needle": "HC1250_0_core_action",
            "purpose": "H_core checklist requirements",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1251_2_1250_template",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1250_FIRST_FINITE_QRHAT_TEMPLATE.csv",
            "needle": "MISSING_NUMERIC_QR_HAT",
            "purpose": "template remains unfilled",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1251_3_1240_map",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1240_QR_TO_PPN_MAPPING_SCHEMA.csv",
            "needle": "QMAP1240_2_dimensionless_qR",
            "purpose": "dimensionless q_Rhat and gamma projection map",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1251_4_1248_fail",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1248_FAILURE_LEDGER.csv",
            "needle": "constraint preservation cannot be checked",
            "purpose": "H_core/bracket closure failure",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1251_5_1244_policy",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1244_RUNNER_POLICY_FEED.csv",
            "needle": "4.6e-05",
            "purpose": "strict q_Rhat guardrail",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    coefficient_map_attempt = [
        {
            "map_id": "CMAP1251_0_required_chain",
            "chain_piece": "H_core -> Euler/source equation",
            "formal_need": "delta H_core/delta R_AB or equivalent canonical equation defines reciprocal source/current",
            "current_input": "MISSING_HCORE",
            "attempt_result": "BLOCKED",
            "blocker": "no explicit weak-field H_core for T,S/e_pub/chi_load",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "map_id": "CMAP1251_1_charge_definition",
            "chain_piece": "source/current -> Q_R",
            "formal_need": "Q_R = boundary integral or integration constant with declared units",
            "current_input": "MISSING_BOUNDARY_CLASS",
            "attempt_result": "BLOCKED",
            "blocker": "no boundary/corner class defining finite Q_R as source-backed charge",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "map_id": "CMAP1251_2_normalization",
            "chain_piece": "Q_R -> q_R_hat",
            "formal_need": "q_R_hat=Q_R c^2/(G M_source) with GM/source convention",
            "current_input": "GM1244_CONVENTION_READY_BUT_QR_MISSING",
            "attempt_result": "WAITING_FOR_QR",
            "blocker": "normalization rule exists but no Q_R value/source exists",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "map_id": "CMAP1251_3_gamma_score",
            "chain_piece": "q_R_hat -> gamma_minus_1_QR",
            "formal_need": "gamma_minus_1_QR=-q_R_hat/2 and abs(q_R_hat)<=4.6e-05 strict smoke guardrail",
            "current_input": "POLICY_READY_BUT_QRHAT_MISSING",
            "attempt_result": "WAITING_FOR_QRHAT",
            "blocker": "policy cannot score without accepted finite q_R_hat",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    formal_chain = [
        {
            "chain_id": "FCHAIN1251_0_symbolic_only",
            "statement": "If H_core supplies a finite exterior reciprocal charge Q_R, then q_R_hat=Q_R c^2/(G M_source) and gamma_minus_1_QR=-q_R_hat/2.",
            "status": "FORMAL_MAP_ONLY",
            "missing_for_numeric_use": "H_core coefficient; boundary charge; source body; measured GM row; no-closure certificate",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "chain_id": "FCHAIN1251_1_zero_not_used",
            "statement": "The 1248 ansatz-zero and explicit closure-zero are not accepted as finite q_R_hat inputs.",
            "status": "REFUSAL_POLICY_RETAINED",
            "missing_for_numeric_use": "real finite row or parent-signed zero theorem",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    phenomenological_row_status = [
        {
            "row_id": "PHENO1251_0_first_row_status",
            "route_type": "phenomenological_bound_nonclaim",
            "template": "source-intake/qr-hat/docs/QRHAT1250_FIRST_FINITE_QRHAT_TEMPLATE.csv",
            "status": "NOT_FILLED",
            "minimum_before_raw": "replace MISSING q_R_hat/source/GM/raw-unit fields with source-backed values; closure_used=false; claim flags false",
            "claim_ceiling": "bound-input only, not local-GR derivation",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    blocker_ledger = [
        {
            "blocker_id": "BLK1251_0_Hcore",
            "blocker": "explicit weak-field H_core missing",
            "effect": "cannot derive q_R_hat coefficient",
            "repair": "write H_core/L_MTS_core terms for reciprocal sector or cite parent source",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "blocker_id": "BLK1251_1_boundary",
            "blocker": "boundary/corner charge class missing",
            "effect": "Q_R is not a sourced charge with units",
            "repair": "derive boundary variation and allowed exterior charge class",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "blocker_id": "BLK1251_2_matter",
            "blocker": "matter/source descent missing",
            "effect": "finite residual could hide source-coupling leakage",
            "repair": "add matter descent/no-shadow-frame theorem or residual source coefficients",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "blocker_id": "BLK1251_3_data_row",
            "blocker": "no numerical q_R_hat source row",
            "effect": "policy runner cannot score",
            "repair": "fill 1250 template only with source-backed finite row",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    claim_gates = [
        {
            "gate_id": "GATE1251_0_formal_map",
            "claim": "formal q_Rhat map exists",
            "status": "PASS_NONCLAIM",
            "reason": "symbolic chain Q_R -> q_R_hat -> gamma is explicit",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1251_1_Hcore_coefficient",
            "claim": "H_core supplies q_Rhat coefficient",
            "status": "BLOCKED",
            "reason": "explicit H_core and boundary charge class are missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1251_2_phenomenological_row",
            "claim": "phenomenological finite q_Rhat row is filled",
            "status": "BLOCKED",
            "reason": "template remains unfilled and not in raw intake",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1251_3_local_PPN",
            "claim": "local PPN gamma pass",
            "status": "BLOCKED",
            "reason": "no accepted finite row or parent zero theorem exists",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1251_4_local_GR",
            "claim": "derived local GR/Newton limit",
            "status": "BLOCKED",
            "reason": "Q_R coefficient/value, beta, matter descent, and boundary silence remain open",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decisions = [
        {
            "decision_id": "DEC1251_0_map_not_numeric",
            "decision": "do not fill q_Rhat from the formal map",
            "because": "the map is symbolic until H_core and Q_R boundary/source class exist",
            "next_action": "either derive H_core reciprocal sector or fill a phenomenological bound row with external/source-backed values",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1251_1_route_split",
            "decision": "separate derivation branch from phenomenological bound branch",
            "because": "mixing them would make a bound look like a field-theory derivation",
            "next_action": "write a local-branch status ledger separating theorem, finite model, and empirical bound modes",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1251_0_1252",
            "target_file": "1252-Y5-R10-local-branch-status-ledger-and-decision-tree.md",
            "target_script": "scripts/Y5_R10_local_branch_status_ledger_and_decision_tree.py",
            "task": "summarize the local-GR branch into a decision tree: parent theorem route, finite H_core coefficient route, phenomenological bound route, and closure benchmark route, with exact blockers and next actions",
            "success_condition": "the project has one authoritative local-branch status ledger showing what is derived, what is closure, what is finite-testable, and what remains blocked",
            "do_not": "do not merge closure, phenomenological bounds, and parent derivations into one claim",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    generated_sets = [
        source_register,
        coefficient_map_attempt,
        formal_chain,
        phenomenological_row_status,
        blocker_ledger,
        claim_gates,
        decisions,
        next_target,
    ]
    output_paths = [
        SOURCE_REGISTER_PATH,
        COEFFICIENT_MAP_ATTEMPT_PATH,
        FORMAL_CHAIN_PATH,
        PHENOMENOLOGICAL_ROW_STATUS_PATH,
        BLOCKER_LEDGER_PATH,
        CLAIM_GATES_PATH,
        DECISION_PATH,
        NEXT_PATH,
    ]

    write_csv(SOURCE_REGISTER_PATH, source_register)
    write_csv(COEFFICIENT_MAP_ATTEMPT_PATH, coefficient_map_attempt)
    write_csv(FORMAL_CHAIN_PATH, formal_chain)
    write_csv(PHENOMENOLOGICAL_ROW_STATUS_PATH, phenomenological_row_status)
    write_csv(BLOCKER_LEDGER_PATH, blocker_ledger)
    write_csv(CLAIM_GATES_PATH, claim_gates)
    write_csv(DECISION_PATH, decisions)
    write_csv(NEXT_PATH, next_target)

    source_checks = [exists_and_contains(row["local_path"], row["needle"]) for row in source_register]
    all_sources_exist = all(exists for exists, _ in source_checks)
    all_needles_found = all(found for _, found in source_checks)
    formal_map_present = any(row["status"] == "FORMAL_MAP_ONLY" for row in formal_chain)
    hcore_blocked = any(row["map_id"] == "CMAP1251_0_required_chain" and row["attempt_result"] == "BLOCKED" for row in coefficient_map_attempt)
    qR_waiting = any(row["map_id"] == "CMAP1251_2_normalization" and row["attempt_result"] == "WAITING_FOR_QR" for row in coefficient_map_attempt)
    pheno_unfilled = phenomenological_row_status[0]["status"] == "NOT_FILLED"
    claim_gates_blocked = all(
        row["status"] in {"PASS_NONCLAIM", "BLOCKED"} and is_false(row, "claim_allowed")
        for row in claim_gates
    )
    all_generated_nonclaim = all(
        is_false(row, "valid_for_claim") and (("claim_allowed" not in row) or is_false(row, "claim_allowed"))
        for rows in generated_sets
        for row in rows
        if "valid_for_claim" in row
    )
    next_is_1252 = next_target[0]["next_id"] == "NEXT1251_0_1252"

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
        validation_row("VAL1251_0_sources_exist", "all cited local sources exist", all_sources_exist, f"{sum(1 for exists, _ in source_checks if exists)}/{len(source_checks)} sources exist"),
        validation_row("VAL1251_1_needles_found", "all cited local needles found", all_needles_found, f"{sum(1 for _, found in source_checks if found)}/{len(source_checks)} needles found"),
        validation_row("VAL1251_2_formal_map", "formal Q_R -> q_Rhat map is present", formal_map_present, "FORMAL_MAP_ONLY"),
        validation_row("VAL1251_3_Hcore_blocked", "H_core coefficient derivation remains blocked", hcore_blocked, "CMAP1251_0_required_chain -> BLOCKED"),
        validation_row("VAL1251_4_QR_waiting", "normalization waits for Q_R", qR_waiting, "CMAP1251_2_normalization -> WAITING_FOR_QR"),
        validation_row("VAL1251_5_pheno_unfilled", "phenomenological row remains unfilled", pheno_unfilled, "PHENO1251_0_first_row_status -> NOT_FILLED"),
        validation_row("VAL1251_6_claim_gates", "claim gates remain blocked/nonclaim", claim_gates_blocked, f"claim_gate_rows={len(claim_gates)}"),
        validation_row("VAL1251_7_nonclaim_policy", "all generated rows remain nonclaim", all_generated_nonclaim, "valid_for_claim=false and claim_allowed=false throughout generated tables"),
        validation_row("VAL1251_8_next_target_1252", "next target is local branch status ledger", next_is_1252, next_target[0]["target_file"]),
        validation_row("VAL1251_9_csv_parse", "all generated CSVs parse cleanly", csv_parse_ok, "; ".join(parsed_counts)),
        validation_row("VAL1251_10_formalization_untouched", "formalization-workbench untouched during run", len(fw_recent) == 0, f"formalization_recent_write_count_since_run_start={len(fw_recent)}"),
    ]
    validation.append(
        validation_row(
            "VAL1251_11_overall",
            "overall 1251 validation",
            all(row["status"] == "PASS" for row in validation),
            "1251 derives only a formal Q_R->q_Rhat map, keeps H_core coefficient and phenomenological rows unfilled, and sends the local branch to a status decision tree",
        )
    )
    write_csv(VALIDATION_PATH, validation)

    sections = [
        f"# {TITLE}",
        "",
        "**Current verdict:** 1251 obtains only a formal `Q_R -> q_R_hat -> gamma` chain. It cannot derive a numeric finite `q_R_hat` because `H_core`, the reciprocal boundary charge class, matter/source descent, and the actual source row are missing.",
        "",
        "**Main progress:** the finite branch is now separated into two honest lanes: a parent-derived coefficient map, currently blocked, and a phenomenological bound row, currently unfilled and nonclaim.",
        "",
        "**No-claim guard:** no finite `q_R_hat`, PPN pass, local-GR pass, R10/WEP pass, or source-coupling claim is promoted.",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "## Source Register",
        markdown_table(source_register, list(source_register[0].keys())),
        "",
        "## Hcore To QRhat Map Attempt",
        markdown_table(coefficient_map_attempt, list(coefficient_map_attempt[0].keys())),
        "",
        "## Formal Chain Nonclaim",
        markdown_table(formal_chain, list(formal_chain[0].keys())),
        "",
        "## Phenomenological Row Status",
        markdown_table(phenomenological_row_status, list(phenomenological_row_status[0].keys())),
        "",
        "## Blocker Ledger",
        markdown_table(blocker_ledger, list(blocker_ledger[0].keys())),
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


if __name__ == "__main__":
    main()
