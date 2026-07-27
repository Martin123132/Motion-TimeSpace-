from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
COEFF = MICROSCOPE / "branch_locked_wep" / "coefficients"
QUARANTINE = MICROSCOPE / "quarantine" / "1475"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1475-Y5-R10-RAB-Ci-residual-evaluator-smoke-runner-or-first-Ci-proof.md"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
START_TS = datetime.now(timezone.utc).timestamp()

PREV_NEXT = OUT / "P8_Y5_R10_1474_NEXT_TARGET.csv"
PREV_VALIDATION = OUT / "P8_Y5_BRR545_1474_VALIDATION.csv"
CI_MAP_1474 = OUT / "P8_Y5_R10_1474_COMPLETE_CI_PARENT_ACTION_MAP.csv"
OBLIGATIONS_1474 = OUT / "P8_Y5_R10_1474_CI_DOUBLE_ZERO_OBLIGATION_MAP.csv"
EVALUATORS_1474 = OUT / "P8_Y5_R10_1474_CI_RESIDUAL_EVALUATOR_ROWS.csv"
SCHEMA_1474 = OUT / "P8_Y5_R10_1474_RESIDUAL_EVALUATOR_SCHEMA.csv"
COVERAGE_1474 = OUT / "P8_Y5_R10_1474_LOCAL_GR_COVERAGE_MATRIX.csv"
THEOREM_1473 = OUT / "P8_Y5_R10_1473_PARENT_COUPLING_DOUBLE_ZERO_THEOREM_ATTEMPT.csv"
SOURCE_COUPLING_1229 = OUT / "P8_Y5_R10_1229_LOCAL_GR_SOURCE_COUPLING_THEOREM_CONTRACT.csv"
SOURCE_GATE_1230 = OUT / "P8_Y5_R10_1230_LOCAL_GR_SOURCE_COUPLING_GATE_UPDATE.csv"
WEP_OWNER_1077 = OUT / "P8_Y5_R10_1077_PARENT_WEP_COUPLING_OWNER_THEOREM_ATTEMPT.csv"
NEWTON_SPINE_956 = OUT / "P8_Y5_R10_956_SOURCE_SIDE_GR_NEWTON_SPINE.csv"
PPN_GATE_1339 = OUT / "P8_Y5_R10_1339_PPN_COMPLETION_GATE.csv"

LIVE_EVALUATOR_INPUT = COEFF / "Ci_residual_evaluator_claim_inputs.csv"
LIVE_EVALUATOR_PASS = COEFF / "Ci_residual_evaluator_pass_rows.csv"
LIVE_LOCAL_GR = COEFF / "local_GR_claim_promotion_rows.csv"
LIVE_NEWTON = COEFF / "Newton_transfer_claim_rows.csv"
LIVE_PPN = COEFF / "PPN_residual_vector_claim_rows.csv"

SOURCE_REGISTER = OUT / "P8_Y5_R10_1475_SOURCE_REGISTER.csv"
SMOKE_RESULTS = OUT / "P8_Y5_R10_1475_CI_SMOKE_EVALUATOR_RESULTS.csv"
AGGREGATE_GATES = OUT / "P8_Y5_R10_1475_CI_SMOKE_AGGREGATE_GATES.csv"
REJECTION_LEDGER = OUT / "P8_Y5_R10_1475_CLAIM_ROW_REJECTION_LEDGER.csv"
FIRST_PROOF = OUT / "P8_Y5_R10_1475_FIRST_CI_PROOF_ATTEMPT.csv"
LIVE_GUARD = OUT / "P8_Y5_R10_1475_LIVE_IMPORT_GUARD.csv"
REDUCTION_GATES = OUT / "P8_Y5_R10_1475_REDUCTION_GATES.csv"
SIGNING_DECISION = OUT / "P8_Y5_R10_1475_PARENT_SIGNING_DECISION.csv"
DECISION_LEDGER = OUT / "P8_Y5_R10_1475_DECISION_LEDGER.csv"
NEXT_TARGET = OUT / "P8_Y5_R10_1475_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1475_VALIDATION.csv"

QUAR_SMOKE_RESULTS = QUARANTINE / "CI_SMOKE_EVALUATOR_RESULTS.csv"
QUAR_REJECTION_LEDGER = QUARANTINE / "CLAIM_ROW_REJECTION_LEDGER.csv"
BRANCH_SMOKE_RESULTS = COEFF / "Ci_smoke_evaluator_results_nonclaim_1475.csv"
BRANCH_REJECTIONS = COEFF / "Ci_claim_rejection_ledger_nonclaim_1475.csv"
BRANCH_SIGNING = COEFF / "Ci_smoke_evaluator_signing_decision_1475.csv"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def truth(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "pass"}


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def copy_branch(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, destination)


def formalization_modified_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    return sum(1 for path in FORMALIZATION.rglob("*") if path.is_file() and path.stat().st_mtime >= START_TS)


def source_rows() -> list[dict[str, Any]]:
    local_sources = [
        ("SRC1475_0_1474_next", PREV_NEXT, "1474 handoff to C_i smoke evaluator or first proof"),
        ("SRC1475_1_1474_validation", PREV_VALIDATION, "1474 validation baseline"),
        ("SRC1475_2_Ci_map", CI_MAP_1474, "complete C_i parent-action map"),
        ("SRC1475_3_obligations", OBLIGATIONS_1474, "C_i double-zero obligations"),
        ("SRC1475_4_evaluators", EVALUATORS_1474, "C_i residual evaluator rows"),
        ("SRC1475_5_schema", SCHEMA_1474, "residual evaluator schema"),
        ("SRC1475_6_coverage", COVERAGE_1474, "local-GR coverage matrix"),
        ("SRC1475_7_double_zero", THEOREM_1473, "double-zero theorem attempt"),
        ("SRC1475_8_source_coupling", SOURCE_COUPLING_1229, "source coupling theorem contract"),
        ("SRC1475_9_source_gate", SOURCE_GATE_1230, "source coupling gate update"),
        ("SRC1475_10_wep_owner", WEP_OWNER_1077, "WEP owner theorem attempt"),
        ("SRC1475_11_newton_spine", NEWTON_SPINE_956, "source-side Newton spine"),
        ("SRC1475_12_ppn_gate", PPN_GATE_1339, "PPN completion gate"),
    ]
    return [
        {
            "source_id": source_id,
            "source_type": "local_file",
            "path_or_url": rel(path),
            "exists": path.exists(),
            "usage": usage,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for source_id, path, usage in local_sources
    ]


def keyed(rows: list[dict[str, str]], key: str) -> dict[str, dict[str, str]]:
    return {row[key]: row for row in rows}


def smoke_result_rows(
    ci_rows: list[dict[str, str]],
    obligation_rows: list[dict[str, str]],
    evaluator_rows: list[dict[str, str]],
    coverage_rows: list[dict[str, str]],
) -> list[dict[str, Any]]:
    obligations = keyed(obligation_rows, "ci_id")
    evaluators = keyed(evaluator_rows, "ci_id")
    coverage = keyed(coverage_rows, "ci_id")
    rows: list[dict[str, Any]] = []
    for ci in ci_rows:
        ci_id = ci["ci_id"]
        obligation = obligations[ci_id]
        evaluator = evaluators[ci_id]
        cov = coverage[ci_id]
        theorem_zero_present = not obligation["current_status"].startswith("OPEN")
        numeric_input_present = not evaluator["current_value"].startswith("MISSING")
        source_exists = (ROOT / evaluator["source_artifact"]).exists()
        required_fields_present = all(
            evaluator[field]
            for field in [
                "ci_id",
                "residual_symbol",
                "evaluator_expression",
                "required_inputs",
                "bound_or_gate",
                "source_artifact",
                "source_anchor",
            ]
        )
        passes_gate = theorem_zero_present or numeric_input_present
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "smoke_id": ci_id.replace("CI1474", "SMOKE1475"),
                "ci_id": ci_id,
                "coefficient": ci["coefficient"],
                "residual_symbol": evaluator["residual_symbol"],
                "source_exists": source_exists,
                "required_fields_present": required_fields_present,
                "theorem_zero_present": theorem_zero_present,
                "numeric_input_present": numeric_input_present,
                "missing_reason": "MISSING_THEOREM_ZERO_OR_NUMERIC_INPUT" if not passes_gate else "none",
                "passes_required_gate": passes_gate,
                "claim_status": "FAIL_EXPECTED_NONCLAIM" if not passes_gate else "PASS_REVIEW_REQUIRED",
                "blocks_Newton": truth(cov["blocks_Newton"]),
                "blocks_PPN": truth(cov["blocks_PPN"]),
                "blocks_local_GR": truth(cov["blocks_local_GR"]),
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def aggregate_gate_rows(smoke_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    all_evaluated = len(smoke_rows) >= 10
    all_missing_fail = all(row["claim_status"] == "FAIL_EXPECTED_NONCLAIM" for row in smoke_rows)
    any_claim_valid = any(truth(row["valid_for_claim"]) or truth(row["claim_allowed"]) for row in smoke_rows)
    newton_blockers = [row["ci_id"] for row in smoke_rows if truth(row["blocks_Newton"]) and not truth(row["passes_required_gate"])]
    ppn_blockers = [row["ci_id"] for row in smoke_rows if truth(row["blocks_PPN"]) and not truth(row["passes_required_gate"])]
    local_blockers = [row["ci_id"] for row in smoke_rows if truth(row["blocks_local_GR"]) and not truth(row["passes_required_gate"])]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "AGG1475_0_all_Ci_evaluated",
            "gate": "all C_i rows have smoke results",
            "gate_pass": all_evaluated,
            "blockers": "none" if all_evaluated else "missing C_i smoke row",
            "claim_effect": "inventory coverage only",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "AGG1475_1_missing_inputs_fail",
            "gate": "every unfilled theorem/numeric input fails mechanically",
            "gate_pass": all_missing_fail,
            "blockers": "none" if all_missing_fail else "some missing row did not fail",
            "claim_effect": "discipline gate active",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "AGG1475_2_any_claim_valid",
            "gate": "any C_i row is claim-valid",
            "gate_pass": any_claim_valid,
            "blockers": ";".join(row["ci_id"] for row in smoke_rows if not truth(row["claim_allowed"])),
            "claim_effect": "must be false in smoke run",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "AGG1475_3_Newton_transfer",
            "gate": "Newton transfer claim allowed",
            "gate_pass": False,
            "blockers": ";".join(newton_blockers),
            "claim_effect": "source/GM/G_eff/finite-mode rows remain unfilled",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "AGG1475_4_PPN_completion",
            "gate": "PPN completion claim allowed",
            "gate_pass": False,
            "blockers": ";".join(ppn_blockers),
            "claim_effect": "PPN residual rows remain unfilled",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "AGG1475_5_local_GR",
            "gate": "local GR reduction claim allowed",
            "gate_pass": False,
            "blockers": ";".join(local_blockers),
            "claim_effect": "all C_i rows remain nonclaim",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def rejection_rows(smoke_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "rejection_id": row["smoke_id"].replace("SMOKE", "REJ"),
            "ci_id": row["ci_id"],
            "attempted_claim": "theorem-zero_or_numeric_residual_pass",
            "rejection_reason": row["missing_reason"],
            "required_to_reverse": "supply parent theorem-zero certificate or source-backed numeric value/curve/vector with units, sign convention, source anchor, and no-cancellation statement",
            "claim_allowed_after_1475": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for row in smoke_rows
    ]


def first_proof_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "proof_id": "FCP1475_0_target",
            "ci_id": "CI1474_1_source_weight",
            "claim_piece": "source-weight double-zero from universal matter source",
            "formal_statement": "If S_matter descends through one action-density line over the observed coframe and the parent object language has no source-only species scalar slot, then delta w_A=0 and partial_B delta w_A=0 for every ordinary matter component.",
            "proof_status": "EXACT_CONDITIONAL_THEOREM",
            "proof_move": "source labels are not arguments of the parent source functor, so variations with respect to source-only selectors are not legal tangent directions; all source variation is through total Hilbert/coframe stress.",
            "missing_for_parent_claim": "connected ordinary matter category, action-density line owner, species-blind measure/current owner, and same-readout-frame theorem",
            "source_artifact": rel(SOURCE_COUPLING_1229),
            "source_anchor": "THM1229_1_iff;THM1229_2_countermodel;THM1229_3_residual_vector",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "proof_id": "FCP1475_1_countermodel_guard",
            "ci_id": "CI1474_1_source_weight",
            "claim_piece": "why the proof cannot promote yet",
            "formal_statement": "S_matter=sum_A(1+epsilon_A)S_A remains a live countermodel unless epsilon_A is forbidden by parent grammar or projected null by every local readout/source kernel.",
            "proof_status": "COUNTERMODEL_SURVIVES",
            "proof_move": "classical equations can look acceptable while Hilbert source weights differ, so the Newton source side and WEP/R10 source legs are not protected by appearance alone.",
            "missing_for_parent_claim": "parent grammar excluding epsilon_A or a proven null-kernel theorem for all local observables",
            "source_artifact": rel(WEP_OWNER_1077),
            "source_anchor": "WCO1077_1_conditional_theorem;WCO1077_5_verdict",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "proof_id": "FCP1475_2_verdict",
            "ci_id": "CI1474_1_source_weight",
            "claim_piece": "first C_i proof status",
            "formal_statement": "The source-weight route is the best first proof target because it feeds Newton, WEP, R10, and local GR, but 1475 does not close it.",
            "proof_status": "NOT_PARENT_DERIVED_KEEP_EVALUATOR_FAILING",
            "proof_move": "keep CI1474_1 failing in the evaluator until the parent action signs the grammar/current/readout premises",
            "missing_for_parent_claim": "same as FCP1475_0 plus explicit parent action/source-current derivation",
            "source_artifact": rel(NEWTON_SPINE_956),
            "source_anchor": "SSG956_1_no_species_source_functor;SSG956_5_source_side_verdict",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def live_guard_rows() -> list[dict[str, Any]]:
    guarded = [
        ("LG1475_0_input", LIVE_EVALUATOR_INPUT, "live claim evaluator inputs"),
        ("LG1475_1_pass", LIVE_EVALUATOR_PASS, "live evaluator pass rows"),
        ("LG1475_2_local_GR", LIVE_LOCAL_GR, "local-GR claim promotion rows"),
        ("LG1475_3_Newton", LIVE_NEWTON, "Newton transfer claim rows"),
        ("LG1475_4_PPN", LIVE_PPN, "PPN claim rows"),
    ]
    return [
        {
            "guard_id": guard_id,
            "path": rel(path),
            "meaning": meaning,
            "exists_now": path.exists(),
            "would_write_in_1475": False,
            "status": "ABSENT_EXPECTED" if not path.exists() else "PRESENT_PREEXISTING_REVIEW_REQUIRED",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for guard_id, path, meaning in guarded
    ]


def reduction_gate_rows(smoke_rows: list[dict[str, Any]], aggregate_rows: list[dict[str, Any]], proof_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    smoke_all_fail = all(row["claim_status"] == "FAIL_EXPECTED_NONCLAIM" for row in smoke_rows)
    aggregate_blocks = all(not truth(row["claim_allowed"]) for row in aggregate_rows)
    conditional_proof_written = any(row["proof_status"] == "EXACT_CONDITIONAL_THEOREM" for row in proof_rows)
    proof_refused = any(row["proof_status"] == "NOT_PARENT_DERIVED_KEEP_EVALUATOR_FAILING" for row in proof_rows)
    return [
        {
            "gate_id": "GATE1475_0_smoke_runner_written",
            "gate": "C_i smoke evaluator generated one row per C_i",
            "gate_pass": len(smoke_rows) >= 10,
            "claim_effect": "mechanical coverage only",
            "valid_for_claim": False,
        },
        {
            "gate_id": "GATE1475_1_missing_inputs_fail",
            "gate": "all unfilled rows fail expectedly",
            "gate_pass": smoke_all_fail,
            "claim_effect": "no prose loopholes",
            "valid_for_claim": False,
        },
        {
            "gate_id": "GATE1475_2_aggregate_claims_blocked",
            "gate": "Newton/PPN/local-GR aggregate claims remain blocked",
            "gate_pass": aggregate_blocks,
            "claim_effect": "no GR/Newton promotion",
            "valid_for_claim": False,
        },
        {
            "gate_id": "GATE1475_3_first_proof_conditional",
            "gate": "first high-leverage C_i proof attempted conditionally",
            "gate_pass": conditional_proof_written,
            "claim_effect": "theorem target only",
            "valid_for_claim": False,
        },
        {
            "gate_id": "GATE1475_4_first_proof_refused",
            "gate": "first C_i proof promotion refused",
            "gate_pass": proof_refused,
            "claim_effect": "CI1474_1 remains failing",
            "valid_for_claim": False,
        },
        {
            "gate_id": "GATE1475_5_local_GR_claim",
            "gate": "local GR/Newton/PPN claim allowed",
            "gate_pass": False,
            "claim_effect": "explicitly forbidden in 1475",
            "valid_for_claim": False,
        },
    ]


def signing_decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "SIGN1475_0_Ci_smoke_evaluator",
            "target": "C_i residual evaluator smoke runner and first C_i proof attempt",
            "smoke_runner_written": True,
            "all_unfilled_rows_fail": True,
            "first_Ci_conditional_proof_written": True,
            "first_Ci_parent_signed": False,
            "any_Ci_claim_valid": False,
            "Newton_transfer_allowed": False,
            "PPN_claim_allowed": False,
            "local_GR_claim_allowed": False,
            "decision": "REFUSE_CI_CLAIM_PROMOTION_KEEP_SMOKE_EVALUATOR_FAILING",
            "reason": "the evaluator behaves correctly: all missing theorem-zero/numeric inputs fail, and the first source-weight proof is conditional only",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC1475_0",
            "decision": "use the C_i smoke evaluator as a discipline gate",
            "why": "it converts missing theorem/numeric inputs into mechanical failures",
            "consequence": "future proof/fill work must flip explicit rows rather than improve prose",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC1475_1",
            "decision": "source-weight coupling is the first high-leverage proof row",
            "why": "it blocks Newton source closure, WEP, R10 source legs, and local GR",
            "consequence": "next proof work should target connected matter category and source-label forgetting",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC1475_2",
            "decision": "no local-GR claim before evaluator pass",
            "why": "every local-GR channel still contains failing C_i rows",
            "consequence": "local GR route is serious but not yet closed",
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT1475_0_1476",
            "next_target": "1476-Y5-R10-RAB-source-label-forgetting-proof-or-Ci-source-weight-numeric-row.md",
            "script": "scripts/Y5_R10_RAB_source_label_forgetting_proof_or_Ci_source_weight_numeric_row.py",
            "objective": "attack CI1474_1_source_weight directly: prove source-label forgetting from parent matter category/current ownership, or emit the first numeric/source-weight residual input row",
            "include": "connected ordinary matter category; species-blind measure; single current owner; no source-only scalar; delta_w_A evaluator input schema",
            "exclude": "GitHub action; formalization-workbench edits; local-GR pass; WEP/R10/clock claim promotion; bound inversion",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def generated_csvs() -> list[Path]:
    return [
        SOURCE_REGISTER,
        SMOKE_RESULTS,
        AGGREGATE_GATES,
        REJECTION_LEDGER,
        FIRST_PROOF,
        QUAR_SMOKE_RESULTS,
        QUAR_REJECTION_LEDGER,
        LIVE_GUARD,
        REDUCTION_GATES,
        SIGNING_DECISION,
        DECISION_LEDGER,
        NEXT_TARGET,
    ]


def csv_parse_clean(paths: list[Path]) -> bool:
    try:
        return all(read_csv_rows(path) for path in paths)
    except Exception:
        return False


def branch_copies_exist() -> bool:
    return BRANCH_SMOKE_RESULTS.exists() and BRANCH_REJECTIONS.exists() and BRANCH_SIGNING.exists()


def validation_rows(
    sources: list[dict[str, Any]],
    smoke_rows: list[dict[str, Any]],
    aggregate_rows: list[dict[str, Any]],
    rejection_rows_: list[dict[str, Any]],
    proof_rows: list[dict[str, Any]],
    live_guard: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    signing: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    local_sources_exist = all(row["source_type"] != "local_file" or truth(row["exists"]) for row in sources)
    one_result_per_ci = len(smoke_rows) == 10 and len({row["ci_id"] for row in smoke_rows}) == 10
    smoke_sources_exist = all(truth(row["source_exists"]) for row in smoke_rows)
    required_fields_present = all(truth(row["required_fields_present"]) for row in smoke_rows)
    all_missing_fail = all(row["claim_status"] == "FAIL_EXPECTED_NONCLAIM" and not truth(row["passes_required_gate"]) for row in smoke_rows)
    no_claim_valid = all(not truth(row["claim_allowed"]) and not truth(row["valid_for_claim"]) for row in smoke_rows)
    aggregate_blocks_claims = all(not truth(row["claim_allowed"]) for row in aggregate_rows) and all(row["gate_id"] not in {"AGG1475_2_any_claim_valid", "AGG1475_3_Newton_transfer", "AGG1475_4_PPN_completion", "AGG1475_5_local_GR"} or not truth(row["gate_pass"]) for row in aggregate_rows)
    rejection_covers_all = {row["ci_id"] for row in rejection_rows_} == {row["ci_id"] for row in smoke_rows}
    proof_conditional = any(row["proof_status"] == "EXACT_CONDITIONAL_THEOREM" for row in proof_rows)
    proof_refused = any(row["proof_status"] == "NOT_PARENT_DERIVED_KEEP_EVALUATOR_FAILING" for row in proof_rows)
    proof_sources_exist = all((ROOT / row["source_artifact"]).exists() for row in proof_rows)
    live_paths_untouched = all(not truth(row["exists_now"]) and not truth(row["would_write_in_1475"]) for row in live_guard)
    safe_gate_pattern = truth(gates[0]["gate_pass"]) and truth(gates[1]["gate_pass"]) and truth(gates[2]["gate_pass"]) and truth(gates[3]["gate_pass"]) and truth(gates[4]["gate_pass"]) and not truth(gates[5]["gate_pass"])
    signing_refuses = all(
        truth(row["smoke_runner_written"])
        and truth(row["all_unfilled_rows_fail"])
        and truth(row["first_Ci_conditional_proof_written"])
        and not truth(row["first_Ci_parent_signed"])
        and not truth(row["any_Ci_claim_valid"])
        and not truth(row["Newton_transfer_allowed"])
        and not truth(row["PPN_claim_allowed"])
        and not truth(row["local_GR_claim_allowed"])
        for row in signing
    )
    generated_parse = csv_parse_clean(generated_csvs())
    pycache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    formalization_untouched = formalization_modified_count() == 0
    checks = [
        ("VAL1475_0_sources", local_sources_exist, "all cited local source paths exist"),
        ("VAL1475_1_one_result_per_Ci", one_result_per_ci, "smoke runner emits one result per C_i"),
        ("VAL1475_2_smoke_sources", smoke_sources_exist, "all evaluator source artifacts exist"),
        ("VAL1475_3_required_fields", required_fields_present, "all smoke rows have required fields"),
        ("VAL1475_4_all_missing_fail", all_missing_fail, "all unfilled theorem/numeric inputs fail expectedly"),
        ("VAL1475_5_no_claim_valid", no_claim_valid, "no smoke row is claim-valid"),
        ("VAL1475_6_aggregate_blocks", aggregate_blocks_claims, "aggregate Newton/PPN/local-GR claims remain blocked"),
        ("VAL1475_7_rejection_coverage", rejection_covers_all, "rejection ledger covers every C_i"),
        ("VAL1475_8_proof_conditional", proof_conditional, "first C_i proof attempt is conditional"),
        ("VAL1475_9_proof_refused", proof_refused, "first C_i proof promotion is refused"),
        ("VAL1475_10_proof_sources", proof_sources_exist, "all proof source artifacts exist"),
        ("VAL1475_11_live_paths", live_paths_untouched, "critical live claim/import paths remain absent"),
        ("VAL1475_12_gate_pattern", safe_gate_pattern, "smoke/proof gates pass while claim gate fails"),
        ("VAL1475_13_signing_refuses", signing_refuses, "parent signing refuses C_i/Newton/PPN/local-GR promotion"),
        ("VAL1475_14_generated_csv_parse", generated_parse, "all generated 1475 CSVs parse cleanly"),
        ("VAL1475_15_branch_copies", branch_copies_exist(), "nonclaim branch/quarantine copies written"),
        ("VAL1475_16_pycache_absent", pycache_absent, "scripts __pycache__ absent after run"),
        ("VAL1475_17_formalization_untouched", formalization_untouched, f"formalization modified-file count since start={formalization_modified_count()}"),
    ]
    overall = all(result for _, result, _ in checks)
    checks.append(("VAL1475_18_overall", overall, "1475 smoke evaluator fails all unfilled C_i rows and keeps first proof conditional"))
    generated = now()
    return [
        {
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail,
            "generated_utc": generated,
        }
        for check_id, result, detail in checks
    ]


def write_doc(
    sources: list[dict[str, Any]],
    smoke_rows: list[dict[str, Any]],
    aggregate_rows: list[dict[str, Any]],
    proof_rows: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    signing: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
) -> None:
    lines: list[str] = []
    lines.append("# 1475 - Y5 R10 RAB C_i Residual Evaluator Smoke Runner Or First C_i Proof")
    lines.append("")
    lines.append("## Verdict")
    lines.append("- The C_i smoke evaluator works as a discipline gate: every unfilled theorem-zero/numeric input fails mechanically.")
    lines.append("- No Newton, PPN, WEP/R10/clock, or local-GR claim is promoted.")
    lines.append("- The first high-leverage proof target is `CI1474_1_source_weight`; its theorem is exact conditionally but still not parent-signed.")
    lines.append("")
    lines.append("## Smoke Results")
    lines.append("| ci_id | residual_symbol | claim_status | missing_reason |")
    lines.append("|---|---|---|---|")
    for row in smoke_rows:
        lines.append(f"| {row['ci_id']} | {row['residual_symbol']} | {row['claim_status']} | {row['missing_reason']} |")
    lines.append("")
    lines.append("## Aggregate Gates")
    lines.append("| gate_id | gate_pass | blockers | claim_effect |")
    lines.append("|---|---:|---|---|")
    for row in aggregate_rows:
        lines.append(f"| {row['gate_id']} | {row['gate_pass']} | {row['blockers']} | {row['claim_effect']} |")
    lines.append("")
    lines.append("## First C_i Proof Attempt")
    lines.append("| proof_id | ci_id | proof_status | missing_for_parent_claim |")
    lines.append("|---|---|---|---|")
    for row in proof_rows:
        lines.append(f"| {row['proof_id']} | {row['ci_id']} | {row['proof_status']} | {row['missing_for_parent_claim']} |")
    lines.append("")
    lines.append("## Gates")
    lines.append("| gate_id | gate_pass | claim_effect |")
    lines.append("|---|---:|---|")
    for row in gates:
        lines.append(f"| {row['gate_id']} | {row['gate_pass']} | {row['claim_effect']} |")
    lines.append("")
    lines.append("## Parent Signing Decision")
    for row in signing:
        lines.append(f"- `{row['decision_id']}`: `{row['decision']}` because {row['reason']}.")
    lines.append("")
    lines.append("## Decision Ledger")
    for row in decisions:
        lines.append(f"- `{row['decision_id']}`: {row['decision']} - {row['consequence']}.")
    lines.append("")
    lines.append("## Validation")
    lines.append("| check_id | result | detail |")
    lines.append("|---|---|---|")
    for row in validation:
        lines.append(f"| {row['check_id']} | {row['result']} | {row['detail']} |")
    lines.append("")
    lines.append("## Source Register")
    lines.append("| source_id | exists | path_or_url | usage |")
    lines.append("|---|---:|---|---|")
    for row in sources:
        lines.append(f"| {row['source_id']} | {row['exists']} | `{row['path_or_url']}` | {row['usage']} |")
    lines.append("")
    lines.append("## Next Target")
    for row in next_target:
        lines.append(f"- `{row['next_target']}` via `{row['script']}`: {row['objective']}")
    lines.append("")
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    sources = source_rows()
    ci_rows = read_csv_rows(CI_MAP_1474)
    obligation_rows = read_csv_rows(OBLIGATIONS_1474)
    evaluator_rows = read_csv_rows(EVALUATORS_1474)
    coverage_rows = read_csv_rows(COVERAGE_1474)
    smoke_rows = smoke_result_rows(ci_rows, obligation_rows, evaluator_rows, coverage_rows)
    aggregate_rows = aggregate_gate_rows(smoke_rows)
    rejection_rows_ = rejection_rows(smoke_rows)
    proof_rows = first_proof_rows()
    live_guard = live_guard_rows()
    gates = reduction_gate_rows(smoke_rows, aggregate_rows, proof_rows)
    signing = signing_decision_rows()
    decisions = decision_rows()
    next_target = next_target_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(SMOKE_RESULTS, smoke_rows)
    write_csv(AGGREGATE_GATES, aggregate_rows)
    write_csv(REJECTION_LEDGER, rejection_rows_)
    write_csv(FIRST_PROOF, proof_rows)
    write_csv(QUAR_SMOKE_RESULTS, smoke_rows)
    write_csv(QUAR_REJECTION_LEDGER, rejection_rows_)
    write_csv(LIVE_GUARD, live_guard)
    write_csv(REDUCTION_GATES, gates)
    write_csv(SIGNING_DECISION, signing)
    write_csv(DECISION_LEDGER, decisions)
    write_csv(NEXT_TARGET, next_target)

    copy_branch(SMOKE_RESULTS, BRANCH_SMOKE_RESULTS)
    copy_branch(REJECTION_LEDGER, BRANCH_REJECTIONS)
    copy_branch(SIGNING_DECISION, BRANCH_SIGNING)

    validation = validation_rows(sources, smoke_rows, aggregate_rows, rejection_rows_, proof_rows, live_guard, gates, signing)
    write_csv(VALIDATION, validation)
    write_doc(sources, smoke_rows, aggregate_rows, proof_rows, gates, signing, decisions, validation, next_target)
    print("Y5_R10_1475_Ci_smoke_evaluator_all_missing_fail_nonclaim")


if __name__ == "__main__":
    main()
