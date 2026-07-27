from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


PACK_ID = "P8_Y5_R10_1252"
TITLE = "1252-Y5-R10-local-branch-status-ledger-and-decision-tree"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_STARTED_UTC = datetime.now(timezone.utc)


SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
LOCAL_BRANCH_STATUS_PATH = OUT_DIR / f"{PACK_ID}_LOCAL_BRANCH_STATUS_LEDGER.csv"
DECISION_TREE_PATH = OUT_DIR / f"{PACK_ID}_LOCAL_BRANCH_DECISION_TREE.csv"
DERIVED_VS_CLOSURE_PATH = OUT_DIR / f"{PACK_ID}_DERIVED_VS_CLOSURE_MATRIX.csv"
NEXT_ACTION_LEDGER_PATH = OUT_DIR / f"{PACK_ID}_NEXT_ACTION_LEDGER.csv"
CLAIM_GATES_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATES.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1252_VALIDATION.csv"


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
            "source_id": "SRC1252_0_1251_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1251_NEXT_TARGET.csv",
            "needle": "NEXT1251_0_1252",
            "purpose": "handoff to local-branch status ledger",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1252_1_1246_zero",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1246_PARENT_QR_ZERO_THEOREM_ATTEMPT.csv",
            "needle": "NOT_DERIVED_CURRENT_CORPUS",
            "purpose": "parent Q_R zero theorem not derived",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1252_2_1247_lambda",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1247_ROUTE_VERDICT.csv",
            "needle": "NOT_PARENT_SIGNED_CURRENT_CORPUS",
            "purpose": "lambda_R route not parent-signed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1252_3_1248_ansatz",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1248_ZERO_THEOREM_CANDIDATE_STATUS.csv",
            "needle": "REJECT_ZERO_THEOREM_UNDERIVED",
            "purpose": "minimal ansatz zero rejected",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1252_4_1249_runner",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1249_POLICY_RUNNER_RESULTS.csv",
            "needle": "NO_ACCEPTED_FINITE_QRHAT_ROWS",
            "purpose": "finite q_Rhat runner has no accepted row",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1252_5_1250_template",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1250_FIRST_FINITE_QRHAT_TEMPLATE.csv",
            "needle": "MISSING_NUMERIC_QR_HAT",
            "purpose": "finite q_Rhat template exists but unfilled",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1252_6_1251_map",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1251_HCORE_TO_QRHAT_MAP_ATTEMPT.csv",
            "needle": "CMAP1251_0_required_chain",
            "purpose": "H_core to q_Rhat formal map attempt",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1252_7_1251_pheno",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1251_PHENOMENOLOGICAL_ROW_STATUS.csv",
            "needle": "NOT_FILLED",
            "purpose": "phenomenological row remains unfilled",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1252_8_13_closure",
            "local_path": "13-local-closure-PPN-benchmark.md",
            "needle": "R_AB=0 and Q_R=0 are closure assumptions in this branch",
            "purpose": "closure benchmark status",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    local_branch_status = [
        {
            "branch_id": "LBS1252_0_parent_zero_theorem",
            "branch": "parent Q_R=0 theorem",
            "current_status": "BLOCKED",
            "best_evidence": "1246: NOT_DERIVED_CURRENT_CORPUS; 1247: lambda_R not parent-signed; 1248: ansatz zero rejected",
            "what_is_true": "clean target is known; no parent theorem exists yet",
            "what_is_not_true": "MTS has not derived local GR via Q_R=0",
            "next_action": "derive H_core/constraint algebra or source/topological no-charge theorem",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": "LBS1252_1_finite_Hcore",
            "branch": "finite H_core q_Rhat coefficient",
            "current_status": "FORMAL_ONLY_BLOCKED_NUMERIC",
            "best_evidence": "1251: formal Q_R -> q_Rhat -> gamma map exists; H_core and boundary class missing",
            "what_is_true": "the scoring chain is mathematically clear",
            "what_is_not_true": "no coefficient/value has been derived",
            "next_action": "write reciprocal H_core/boundary source class or leave value missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": "LBS1252_2_phenomenological_bound",
            "branch": "phenomenological finite q_Rhat bound",
            "current_status": "TEMPLATE_READY_ROW_UNFILLED",
            "best_evidence": "1250 template in qr-hat/docs; 1251 phenomenological status NOT_FILLED",
            "what_is_true": "a strict nonclaim intake path exists",
            "what_is_not_true": "no empirical/phenomenological q_Rhat row exists",
            "next_action": "fill only with source-backed finite q_Rhat or bound, no closure",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": "LBS1252_3_closure_benchmark",
            "branch": "R_AB=0/Q_R=0 closure benchmark",
            "current_status": "AVAILABLE_AS_CONTROL_ONLY",
            "best_evidence": "13-local-closure-PPN-benchmark: closure reproduces GR control behavior",
            "what_is_true": "closure branch is a useful local GR baseline/control",
            "what_is_not_true": "closure is not evidence for parent derivation",
            "next_action": "use only as labelled control branch",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": "LBS1252_4_policy_runner",
            "branch": "PPN gamma q_Rhat policy runner",
            "current_status": "READY_NO_INPUT",
            "best_evidence": "1249: NO_ACCEPTED_FINITE_QRHAT_ROWS",
            "what_is_true": "policy/GM/scoring machinery is ready",
            "what_is_not_true": "no MTS finite prediction has passed",
            "next_action": "rerun only after accepted finite or theorem-zero row appears",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decision_tree = [
        {
            "node_id": "DT1252_0_parent_zero",
            "if_condition": "parent-signed Q_R=0 theorem appears",
            "then_action": "route through zero-theorem validator; then expand beta/matter/boundary local-GR gates",
            "current_result": "NO",
            "claim_boundary": "not current evidence",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "node_id": "DT1252_1_finite_model",
            "if_condition": "finite q_Rhat source row appears",
            "then_action": "run 1249 policy runner; keep result nonclaim until beta/matter/local gates close",
            "current_result": "NO",
            "claim_boundary": "future smoke score only",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "node_id": "DT1252_2_phenomenological_bound",
            "if_condition": "phenomenological bound row appears",
            "then_action": "label as phenomenological_bound_nonclaim; do not call it derived GR",
            "current_result": "NO",
            "claim_boundary": "bound-input only",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "node_id": "DT1252_3_closure_control",
            "if_condition": "using R_AB=0/Q_R=0 closure",
            "then_action": "report as GR-control closure branch only",
            "current_result": "YES_AVAILABLE",
            "claim_boundary": "control baseline, not theorem",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    derived_vs_closure = [
        {
            "item_id": "DVC1252_0_gamma_projection",
            "item": "gamma_minus_1_QR=-q_Rhat/2",
            "status": "FORMAL_SCORING_MAP",
            "derived_level": "schema/nonclaim",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "item_id": "DVC1252_1_QR_zero",
            "item": "Q_R=0",
            "status": "CLOSURE_OR_UNDERIVED",
            "derived_level": "not parent-derived",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "item_id": "DVC1252_2_lambdaR",
            "item": "lambda_R R_AB constraint",
            "status": "ALGEBRAICALLY_USEFUL_NOT_PARENT_SIGNED",
            "derived_level": "ansatz/closure until H_core proves origin",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "item_id": "DVC1252_3_finite_qRhat",
            "item": "finite q_Rhat",
            "status": "MISSING",
            "derived_level": "no value/source row",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "item_id": "DVC1252_4_local_GR",
            "item": "local GR/Newton reduction",
            "status": "OPEN",
            "derived_level": "closure control exists; derivation not achieved",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]

    next_action_ledger = [
        {
            "action_id": "NA1252_0_best_derivation",
            "priority": 1,
            "action": "derive reciprocal H_core/boundary charge class",
            "why": "this is the missing coefficient/value route for q_Rhat",
            "success_output": "finite_qRhat row source or parent zero theorem candidate",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "action_id": "NA1252_1_best_test",
            "priority": 2,
            "action": "fill phenomenological q_Rhat bound only if source-backed",
            "why": "keeps local branch testable if derivation remains open",
            "success_output": "phenomenological_bound_nonclaim row routed through 1249",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "action_id": "NA1252_2_do_not_mix",
            "priority": 3,
            "action": "keep closure benchmark separate",
            "why": "closure control is useful but not evidence",
            "success_output": "clean language and no overclaim",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    claim_gates = [
        {
            "gate_id": "GATE1252_0_status_ledger",
            "claim": "authoritative local branch status ledger exists",
            "status": "PASS_NONCLAIM",
            "reason": "branches, decision tree, derived-vs-closure matrix, and next actions are generated",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1252_1_parent_zero",
            "claim": "parent Q_R=0 theorem exists",
            "status": "BLOCKED",
            "reason": "1246/1247/1248 show it is not parent-derived",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1252_2_finite_qRhat",
            "claim": "finite q_Rhat source row exists",
            "status": "BLOCKED",
            "reason": "1249/1250/1251 show no accepted row/value",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1252_3_local_PPN",
            "claim": "local PPN pass exists",
            "status": "BLOCKED",
            "reason": "policy runner has no accepted MTS input",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1252_4_local_GR",
            "claim": "derived local GR/Newton limit exists",
            "status": "BLOCKED",
            "reason": "closure control exists, but derivation still lacks Q_R theorem/value, beta, matter descent, and boundary proof",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decisions = [
        {
            "decision_id": "DEC1252_0_status",
            "decision": "local branch is disciplined but not derived",
            "because": "the runner, templates, and maps are ready but theorem/value evidence is missing",
            "next_action": "work NA1252_0 first unless choosing a test-first phenomenological bound",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    next_target = [
        {
            "next_id": "NEXT1252_0_1253",
            "target_file": "1253-Y5-R10-reciprocal-Hcore-boundary-charge-derivation-attempt.md",
            "target_script": "scripts/Y5_R10_reciprocal_Hcore_boundary_charge_derivation_attempt.py",
            "task": "attempt the best derivation route from the 1252 ledger: derive or bound the reciprocal H_core/boundary charge class that would generate Q_R or prove its absence",
            "success_condition": "produce either a parent/source equation for Q_R, a boundary no-charge theorem candidate, or an explicit blocker that sends the branch to phenomenological finite q_Rhat sourcing",
            "do_not": "do not reuse closure zero, lambda_R ansatz zero, or comparator-only rows as evidence",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    generated_sets = [
        source_register,
        local_branch_status,
        decision_tree,
        derived_vs_closure,
        next_action_ledger,
        claim_gates,
        decisions,
        next_target,
    ]
    output_paths = [
        SOURCE_REGISTER_PATH,
        LOCAL_BRANCH_STATUS_PATH,
        DECISION_TREE_PATH,
        DERIVED_VS_CLOSURE_PATH,
        NEXT_ACTION_LEDGER_PATH,
        CLAIM_GATES_PATH,
        DECISION_PATH,
        NEXT_PATH,
    ]

    write_csv(SOURCE_REGISTER_PATH, source_register)
    write_csv(LOCAL_BRANCH_STATUS_PATH, local_branch_status)
    write_csv(DECISION_TREE_PATH, decision_tree)
    write_csv(DERIVED_VS_CLOSURE_PATH, derived_vs_closure)
    write_csv(NEXT_ACTION_LEDGER_PATH, next_action_ledger)
    write_csv(CLAIM_GATES_PATH, claim_gates)
    write_csv(DECISION_PATH, decisions)
    write_csv(NEXT_PATH, next_target)

    source_checks = [exists_and_contains(row["local_path"], row["needle"]) for row in source_register]
    all_sources_exist = all(exists for exists, _ in source_checks)
    all_needles_found = all(found for _, found in source_checks)
    branches_complete = len(local_branch_status) == 5 and all(row["claim_allowed"] is False for row in local_branch_status)
    decision_tree_complete = len(decision_tree) == 4 and any(row["current_result"] == "YES_AVAILABLE" and "closure" in row["node_id"] for row in decision_tree)
    matrix_separates = any(row["item"] == "Q_R=0" and row["status"] == "CLOSURE_OR_UNDERIVED" for row in derived_vs_closure) and any(
        row["item"] == "finite q_Rhat" and row["status"] == "MISSING" for row in derived_vs_closure
    )
    next_action_best = next_action_ledger[0]["action"] == "derive reciprocal H_core/boundary charge class"
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
    next_is_1253 = next_target[0]["next_id"] == "NEXT1252_0_1253"

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
        validation_row("VAL1252_0_sources_exist", "all cited local sources exist", all_sources_exist, f"{sum(1 for exists, _ in source_checks if exists)}/{len(source_checks)} sources exist"),
        validation_row("VAL1252_1_needles_found", "all cited local needles found", all_needles_found, f"{sum(1 for _, found in source_checks if found)}/{len(source_checks)} needles found"),
        validation_row("VAL1252_2_branches_complete", "local branch status covers all active routes", branches_complete, f"branch_rows={len(local_branch_status)}"),
        validation_row("VAL1252_3_decision_tree", "decision tree separates theorem/finite/pheno/closure routes", decision_tree_complete, f"decision_tree_rows={len(decision_tree)}"),
        validation_row("VAL1252_4_matrix_separates", "derived-vs-closure matrix keeps Q_R and finite q_Rhat distinct", matrix_separates, "Q_R=0 closure/underived and finite q_Rhat missing"),
        validation_row("VAL1252_5_next_action", "best next action targets H_core boundary charge", next_action_best, next_action_ledger[0]["action"]),
        validation_row("VAL1252_6_claim_gates", "claim gates remain blocked/nonclaim", claim_gates_blocked, f"claim_gate_rows={len(claim_gates)}"),
        validation_row("VAL1252_7_nonclaim_policy", "all generated rows remain nonclaim", all_generated_nonclaim, "valid_for_claim=false and claim_allowed=false throughout generated tables"),
        validation_row("VAL1252_8_next_target_1253", "next target is reciprocal H_core boundary charge derivation", next_is_1253, next_target[0]["target_file"]),
        validation_row("VAL1252_9_csv_parse", "all generated CSVs parse cleanly", csv_parse_ok, "; ".join(parsed_counts)),
        validation_row("VAL1252_10_formalization_untouched", "formalization-workbench untouched during run", len(fw_recent) == 0, f"formalization_recent_write_count_since_run_start={len(fw_recent)}"),
    ]
    validation.append(
        validation_row(
            "VAL1252_11_overall",
            "overall 1252 validation",
            all(row["status"] == "PASS" for row in validation),
            "1252 creates the authoritative local branch status ledger and decision tree without merging closure, theorem, finite, or phenomenological routes",
        )
    )
    write_csv(VALIDATION_PATH, validation)

    sections = [
        f"# {TITLE}",
        "",
        "**Current verdict:** 1252 is the local-branch map. Local GR is not derived yet; the closure branch is available as a control, the policy runner is ready, the finite path is formal but value-missing, and the parent zero theorem is blocked.",
        "",
        "**Main progress:** the routes are now separated cleanly: parent theorem, finite H_core coefficient, phenomenological bound, closure benchmark, and PPN runner. This prevents the project from smuggling closure into derivation or bounds into theory.",
        "",
        "**No-claim guard:** no local GR, local PPN, finite `q_R_hat`, R10/WEP, or source-coupling claim is promoted.",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "## Source Register",
        markdown_table(source_register, list(source_register[0].keys())),
        "",
        "## Local Branch Status Ledger",
        markdown_table(local_branch_status, list(local_branch_status[0].keys())),
        "",
        "## Local Branch Decision Tree",
        markdown_table(decision_tree, list(decision_tree[0].keys())),
        "",
        "## Derived Vs Closure Matrix",
        markdown_table(derived_vs_closure, list(derived_vs_closure[0].keys())),
        "",
        "## Next Action Ledger",
        markdown_table(next_action_ledger, list(next_action_ledger[0].keys())),
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
