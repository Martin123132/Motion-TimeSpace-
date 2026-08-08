from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1537-Y5-Jeff-Bm-component-norm-input-pack.md"
START_TS = datetime.now(timezone.utc).timestamp()

SOURCE_FILES = {
    "1536_doc": ROOT / "1536-Y5-Jeff-Bm-source-boundary-silence-or-bound.md",
    "1536_validation": OUT / "P8_Y5_BRR545_1536_VALIDATION.csv",
    "1536_jeff": OUT / "P8_Y5_PARENT_QLOC_1536_JEFF_COMPONENT_SPLIT.csv",
    "1536_bm": OUT / "P8_Y5_PARENT_QLOC_1536_BM_COMPONENT_SPLIT.csv",
    "1536_nlock": OUT / "P8_Y5_PARENT_QLOC_1536_NLOCK_ENVELOPE_CONTRACT.csv",
    "1535_audit": OUT / "P8_Y5_PARENT_QLOC_1535_LOCKING_INPUT_SOURCE_AUDIT.csv",
    "1534_leakage": OUT / "P8_Y5_PARENT_QLOC_1534_QUADRATIC_LEAKAGE_BOUND_CONTRACT.csv",
    "gamma_expansion": OUT / "P8_Y5_R10_798_GAMMA_SOURCE_EXPANSION.csv",
    "positive_nohair": OUT / "P8_Y5_R10_POSITIVE_OPERATOR_NOHAIR_ATTEMPT.csv",
    "boundary_certificate": OUT / "P8_Y5_PARENT_QLOC_1529_BOUNDARY_CERTIFICATE_AUDIT.csv",
    "source_current": OUT / "P8_Y5_SOURCE_CURRENT_CLOSURE_THEOREM_ATTEMPT.csv",
    "source_measure": OUT / "P8_SOURCE_MEASURE_MEFF_FLUX_THEOREM.csv",
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1537_SOURCE_REGISTER.csv"
NORM_INPUT_PACK = OUT / "P8_Y5_PARENT_QLOC_1537_COMPONENT_NORM_INPUT_PACK.csv"
FIRST_PRIORITY = OUT / "P8_Y5_PARENT_QLOC_1537_FIRST_PRIORITY_NORM_ROWS.csv"
NLOCK_RUNNER_INPUT = OUT / "P8_Y5_PARENT_QLOC_1537_NLOCK_RUNNER_INPUT_NONCLAIM.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1537_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1537_DECISION.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1537_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1537_VALIDATION.csv"

QUARANTINE = MICROSCOPE / "quarantine" / "1537"
QUAR_PACK = QUARANTINE / "COMPONENT_NORM_INPUT_PACK_NONCLAIM.csv"
QUAR_FIRST = QUARANTINE / "FIRST_PRIORITY_NORM_ROWS_NONCLAIM.csv"
QUAR_RUNNER = QUARANTINE / "NLOCK_RUNNER_INPUT_NONCLAIM.csv"
QUAR_DECISION = QUARANTINE / "DECISION_NONCLAIM.csv"
BRANCH_PACK = BRANCH_RESIDUALS / "Jeff_Bm_component_norm_input_pack_nonclaim_1537.csv"
BRANCH_FIRST = BRANCH_RESIDUALS / "Jeff_Bm_first_priority_norm_rows_nonclaim_1537.csv"
BRANCH_RUNNER = BRANCH_RESIDUALS / "Nlock_runner_input_nonclaim_1537.csv"
BRANCH_DECISION = BRANCH_RESIDUALS / "Jeff_Bm_norm_decision_nonclaim_1537.csv"


def flags() -> dict[str, bool]:
    return {
        "score_ready": False,
        "valid_prediction_row": False,
        "valid_for_claim": False,
        "claim_allowed": False,
    }


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def source_list(*keys: str) -> str:
    return "; ".join(rel(SOURCE_FILES[key]) for key in keys)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def parse_csv(path: Path) -> bool:
    read_csv(path)
    return True


def generated_flags_false(paths: list[Path]) -> bool:
    false_values = {"", "false", "0", "no", "none", "null"}
    claim_keys = [
        "score_ready",
        "valid_prediction_row",
        "valid_for_claim",
        "claim_allowed",
        "accepted_for_scoring",
        "passes_for_claim",
    ]
    for path in paths:
        for row in read_csv(path):
            for key in claim_keys:
                if key in row and str(row[key]).strip().lower() not in false_values:
                    return False
    return True


def source_register_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "source_id": f"SRC1537_{index}_{key}",
            "source_path": rel(path),
            "exists": path.exists(),
            "purpose": "input evidence for J_eff/B_m component norm input pack",
            **flags(),
        }
        for index, (key, path) in enumerate(SOURCE_FILES.items())
    ]


def norm_rows() -> list[dict[str, Any]]:
    rows = [
        ("NORM1537_0_N_src", "N_src", "J_src=U_B S_cg", "||U_B S_cg||_{E*}", "PRIMARY_MISSING", "U_B bound; S_cg norm; source projection; E* norm", "source", source_list("gamma_expansion", "1536_jeff")),
        ("NORM1537_1_N_drift_mL", "N_drift_mL", "J_drift_mL", "||J_drift_mL||_{E*}", "MISSING", "m_L drift law or bound", "source", source_list("gamma_expansion", "1536_jeff")),
        ("NORM1537_2_N_drift_Lcg", "N_drift_Lcg", "J_drift_Lcg", "||J_drift_Lcg||_{E*}", "MISSING", "L_cg drift law or bound", "source", source_list("gamma_expansion", "1536_jeff")),
        ("NORM1537_3_N_selector", "N_selector", "J_selector", "||J_selector||_{E*}", "MISSING", "Pi_B/mu_B/tau_L variation bounds", "source", source_list("gamma_expansion", "source_current")),
        ("NORM1537_4_N_history", "N_history", "J_history", "||J_history||_{E*}", "MISSING", "history/memory injection norm", "source", source_list("1536_jeff", "1535_audit")),
        ("NORM1537_5_N_transition", "N_transition", "J_transition", "||J_transition||_{E*}", "MISSING", "transition-current/K_perp norm", "source", source_list("gamma_expansion", "1536_jeff")),
        ("NORM1537_6_N_mass_current", "N_mass_current", "J_mass_current", "||J_mass_current||_{E*}", "MISSING", "source-current/Meff closure residual norm", "source-current", source_list("source_current", "source_measure")),
        ("NORM1537_7_N_inner", "N_inner", "B_inner or Q_m^H", "boundary-dual norm of inner compact-source charge", "PRIMARY_MISSING", "inner monopole/source charge theorem or finite boundary norm", "boundary", source_list("positive_nohair", "1536_bm")),
        ("NORM1537_8_N_no_flux", "N_no_flux", "B_no_flux", "boundary-dual norm of no-flux violation", "MISSING", "boundary condition certificate or violation norm", "boundary", source_list("boundary_certificate", "1536_bm")),
        ("NORM1537_9_N_zero_mode", "N_zero_mode", "B_zero_mode", "boundary-dual norm of zero-mode/reference leakage", "MISSING", "zero-mode certificate or reference norm", "boundary", source_list("boundary_certificate", "1536_bm")),
        ("NORM1537_10_N_outer", "N_outer", "B_outer", "boundary-dual norm of outer/reference flux", "MISSING", "outer flux/fixed-reference norm", "boundary", source_list("source_measure", "1536_bm")),
        ("NORM1537_11_N_history_boundary", "N_history_boundary", "B_history", "boundary-dual norm of history boundary injection", "MISSING", "history boundary norm", "boundary", source_list("1536_bm", "1535_audit")),
        ("NORM1537_12_N_domain", "N_domain", "B_domain", "boundary-dual norm of domain/support motion", "MISSING", "domain/support variation norm", "boundary", source_list("boundary_certificate", "1536_bm")),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "norm_id": norm_id,
            "symbol": symbol,
            "component": component,
            "norm_definition": definition,
            "status": status,
            "missing_to_promote": missing,
            "category": category,
            "source_paths": sources,
            **flags(),
        }
        for norm_id, symbol, component, definition, status, missing, category, sources in rows
    ]


def first_priority_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "FP1537_0_N_src_zero",
            "N_src exact zero",
            "U_B=0 or S_cg has zero local exterior projection in the same parent branch",
            "NOT_PROVED",
            "GSE798 leaves source-support powers unsigned",
        ),
        (
            "FP1537_1_N_src_bound",
            "N_src finite bound",
            "N_src <= ||U_B||_inf ||S_cg||_{E*}",
            "FORMULA_ONLY",
            "U_B and S_cg norms missing",
        ),
        (
            "FP1537_2_N_inner_zero",
            "N_inner exact zero",
            "Q_m^H=0 or the inner compact-source boundary charge is projected out by a parent source-silence theorem",
            "NOT_PROVED",
            "positive no-hair warns this is not automatic",
        ),
        (
            "FP1537_3_N_inner_bound",
            "N_inner finite bound",
            "N_inner <= C_inner |Q_m^H| or finite boundary-dual norm",
            "FORMULA_ONLY",
            "C_inner and Q_m^H/source charge missing",
        ),
        (
            "FP1537_4_pair_verdict",
            "first-priority pair",
            "N_src and N_inner are the first physical blockers for N_lock",
            "PRIORITY_CONFIRMED",
            "they decide source support and compact-source boundary hair",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "priority_id": priority_id,
            "target": target,
            "formula_or_condition": formula,
            "status": status,
            "missing_to_promote": missing,
            "source_paths": source_list("1536_jeff", "1536_bm", "gamma_expansion", "positive_nohair"),
            **flags(),
        }
        for priority_id, target, formula, status, missing in rows
    ]


def nlock_runner_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "NLR1537_0_NJ",
            "quantity": "N_J",
            "formula": "N_J <= N_src+N_drift_mL+N_drift_Lcg+N_selector+N_history+N_transition+N_mass_current",
            "current_status": "FORMULA_ONLY_COMPONENTS_MISSING",
            "missing_inputs": "all N_J component norms",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "NLR1537_1_NB",
            "quantity": "N_B",
            "formula": "N_B <= N_inner+N_no_flux+N_zero_mode+N_outer+N_history_boundary+N_domain",
            "current_status": "FORMULA_ONLY_COMPONENTS_MISSING",
            "missing_inputs": "all N_B component norms",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "NLR1537_2_Nlock",
            "quantity": "N_lock",
            "formula": "N_lock=N_J+N_B",
            "current_status": "NOT_COMPUTABLE",
            "missing_inputs": "N_src and N_inner first; then remaining component norms",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "NLR1537_3_local_lock",
            "quantity": "local locking/leakage",
            "formula": "E_m(u)<=N_lock; U_m<=C_emb N_lock",
            "current_status": "BLOCKED",
            "missing_inputs": "N_lock and C_emb",
            **flags(),
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("GATE1537_0_norm_pack", "component norm input pack written", "PASS_NONCLAIM", "all J/B components have norm slots"),
        ("GATE1537_1_Nsrc", "N_src zero/bound", "BLOCKED", "U_B and S_cg source norm missing"),
        ("GATE1537_2_Ninner", "N_inner zero/bound", "BLOCKED", "inner charge/source boundary norm missing"),
        ("GATE1537_3_Nlock", "N_lock computable", "BLOCKED", "component norms missing"),
        ("GATE1537_4_local_GR", "local GR/Newton/PPN claim", "BLOCKED_NO_CLAIM", "pre-lock and hidden-kernel gates remain"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "claim": claim,
            "status": status,
            "reason": reason,
            **flags(),
        }
        for gate_id, claim, status, reason in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        ("DEC1537_0_progress", "Keep the N_lock component norm schema.", "NORM_SCHEMA_WRITTEN", "it makes the leakage route fillable without cancellations"),
        ("DEC1537_1_first_targets", "Prioritize N_src and N_inner.", "SOURCE_AND_INNER_BOUNDARY_FIRST", "these are the most physical blockers and hardest to hide"),
        ("DEC1537_2_no_claim", "Do not claim local lock or local GR.", "CLAIM_BLOCKED", "no component norm is numeric or theorem-zero"),
        ("DEC1537_3_next", "Next target is U_B S_cg and Q_m^H theorem-or-bound.", "NEXT_1538_SOURCE_SUPPORT_INNER_CHARGE", "fill the first two component norms or prove they vanish"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": decision_id,
            "decision": decision,
            "result": result,
            "rationale": rationale,
            **flags(),
        }
        for decision_id, decision, result, rationale in rows
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "next_id": "NEXT1537_0_1538",
            "next_target": "1538-Y5-source-support-and-inner-charge-theorem-or-bound.md",
            "script": "scripts/Y5_source_support_and_inner_charge_theorem_or_bound.py",
            "objective": "derive or bound N_src=||U_B S_cg|| and N_inner from compact-source boundary charge Q_m^H; decide whether the first N_lock inputs can become zero/bounded rows",
            "do_not": "do not claim U_B=0 or Q_m^H=0 without parent proof; do not use cancellation; do not promote local GR",
            **flags(),
        }
    ]


def copy_outputs() -> None:
    copies = [
        (NORM_INPUT_PACK, QUAR_PACK),
        (FIRST_PRIORITY, QUAR_FIRST),
        (NLOCK_RUNNER_INPUT, QUAR_RUNNER),
        (DECISION, QUAR_DECISION),
        (NORM_INPUT_PACK, BRANCH_PACK),
        (FIRST_PRIORITY, BRANCH_FIRST),
        (NLOCK_RUNNER_INPUT, BRANCH_RUNNER),
        (DECISION, BRANCH_DECISION),
    ]
    for source, destination in copies:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def formalization_modified_count_since_start() -> int:
    if not FORMALIZATION.exists():
        return 0
    return sum(1 for path in FORMALIZATION.rglob("*") if path.is_file() and path.stat().st_mtime >= START_TS)


def validation_rows(generated_csvs: list[Path]) -> list[dict[str, Any]]:
    sources = read_csv(SOURCE_REGISTER)
    norms = read_csv(NORM_INPUT_PACK)
    first = read_csv(FIRST_PRIORITY)
    runner = read_csv(NLOCK_RUNNER_INPUT)
    gates = read_csv(CLAIM_GATE)
    decisions = read_csv(DECISION)
    next_rows = read_csv(NEXT_TARGET)

    required_norms = {"N_src", "N_drift_mL", "N_drift_Lcg", "N_selector", "N_history", "N_transition", "N_mass_current", "N_inner", "N_no_flux", "N_zero_mode", "N_outer", "N_history_boundary", "N_domain"}
    norm_symbols = {row["symbol"] for row in norms}
    checks = [
        ("VAL1537_0_sources_exist", all(row["exists"] == "True" for row in sources), "all cited 1537 input source paths exist"),
        ("VAL1537_1_norm_slots_complete", required_norms.issubset(norm_symbols), "all J/B component norm slots written"),
        ("VAL1537_2_primary_rows", any(row["symbol"] == "N_src" and row["status"] == "PRIMARY_MISSING" for row in norms) and any(row["symbol"] == "N_inner" and row["status"] == "PRIMARY_MISSING" for row in norms), "N_src and N_inner marked as first-priority missing rows"),
        ("VAL1537_3_first_priority_contract", any(row["priority_id"] == "FP1537_4_pair_verdict" and row["status"] == "PRIORITY_CONFIRMED" for row in first), "first-priority N_src/N_inner contract written"),
        ("VAL1537_4_runner_noncomputable", any(row["runner_id"] == "NLR1537_2_Nlock" and row["current_status"] == "NOT_COMPUTABLE" for row in runner), "N_lock runner remains noncomputable"),
        ("VAL1537_5_claim_gates_block", any(row["gate_id"] == "GATE1537_4_local_GR" and row["status"] == "BLOCKED_NO_CLAIM" for row in gates), "local GR claim remains blocked"),
        ("VAL1537_6_decision_next", any(row["result"] == "NEXT_1538_SOURCE_SUPPORT_INNER_CHARGE" for row in decisions), "decision selects source-support/inner-charge target next"),
        ("VAL1537_7_next_target", any("1538-Y5-source-support" in row["next_target"] for row in next_rows), "next target is source support and inner charge theorem or bound"),
        ("VAL1537_8_csv_parse", all(parse_csv(path) for path in generated_csvs), "all generated 1537 CSVs parse cleanly"),
        ("VAL1537_9_claim_flags_false", generated_flags_false(generated_csvs), "all generated prediction/claim flags remain false"),
        ("VAL1537_10_branch_copies", all(path.exists() for path in [QUAR_PACK, QUAR_FIRST, QUAR_RUNNER, QUAR_DECISION, BRANCH_PACK, BRANCH_FIRST, BRANCH_RUNNER, BRANCH_DECISION]), "branch/quarantine nonclaim copies written"),
        ("VAL1537_11_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent after run"),
        ("VAL1537_12_formalization_untouched", formalization_modified_count_since_start() == 0, "formalization modified-file count since start=0"),
    ]
    overall = all(result for _, result, _ in checks)
    rows = [
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail,
        }
        for check_id, result, detail in checks
    ]
    rows.append(
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": "VAL1537_13_overall",
            "result": "PASS" if overall else "FAIL",
            "detail": "1537 creates a nonclaim N_lock component norm input pack, prioritizes N_src and N_inner, keeps local claims blocked, and selects source support/inner charge next"
            if overall
            else "1537 validation failed; inspect failed rows before continuing",
        }
    )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    output = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    for row in rows:
        output.append(
            "| "
            + " | ".join(str(row.get(column, "")).replace("\n", " ").replace("|", "\\|") for column in columns)
            + " |"
        )
    return "\n".join(output)


def write_doc(
    sources: list[dict[str, Any]],
    norms: list[dict[str, Any]],
    first: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 1537 - J_eff / B_m Component Norm Input Pack",
                "",
                "## Verdict",
                "- The `N_lock` leakage route now has explicit nonclaim norm slots for every `J_eff` and `B_m` component.",
                "- `N_src=||U_B S_cg||_{E*}` and `N_inner` from compact-source boundary charge are the first-priority blockers.",
                "- No component norm is numeric or theorem-zero yet, so `N_lock` is not computable.",
                "- This remains private/nonclaim; no exact local lock, local-GR, Newton, PPN, or R10 pass is promoted.",
                "- Next target is to derive or bound `U_B S_cg` and the inner compact-source charge `Q_m^H`.",
                "",
                "## Source Register",
                md_table(sources, ["source_id", "source_path", "exists", "purpose"]),
                "",
                "## Component Norm Input Pack",
                md_table(norms, ["norm_id", "symbol", "component", "norm_definition", "status", "missing_to_promote", "category"]),
                "",
                "## First Priority Norm Rows",
                md_table(first, ["priority_id", "target", "formula_or_condition", "status", "missing_to_promote"]),
                "",
                "## N_lock Runner Input",
                md_table(runner, ["runner_id", "quantity", "formula", "current_status", "missing_inputs"]),
                "",
                "## Claim Gates",
                md_table(gates, ["gate_id", "claim", "status", "reason"]),
                "",
                "## Decision",
                md_table(decisions, ["decision_id", "decision", "result", "rationale"]),
                "",
                "## Validation",
                md_table(validation, ["check_id", "result", "detail"]),
                "",
                "## Next Target",
                md_table(next_rows, ["next_id", "next_target", "script", "objective", "do_not"]),
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_register_rows()
    norms = norm_rows()
    first = first_priority_rows()
    runner = nlock_runner_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(NORM_INPUT_PACK, norms)
    write_csv(FIRST_PRIORITY, first)
    write_csv(NLOCK_RUNNER_INPUT, runner)
    write_csv(CLAIM_GATE, gates)
    write_csv(DECISION, decisions)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()
    remove_pycache()

    generated_csvs = [
        SOURCE_REGISTER,
        NORM_INPUT_PACK,
        FIRST_PRIORITY,
        NLOCK_RUNNER_INPUT,
        CLAIM_GATE,
        DECISION,
        NEXT_TARGET,
    ]
    validation = validation_rows(generated_csvs)
    write_csv(VALIDATION, validation)
    write_doc(sources, norms, first, runner, gates, decisions, validation, next_rows)


if __name__ == "__main__":
    main()
