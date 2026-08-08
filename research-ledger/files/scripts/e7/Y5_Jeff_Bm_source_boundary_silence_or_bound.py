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
DOC = ROOT / "1536-Y5-Jeff-Bm-source-boundary-silence-or-bound.md"
START_TS = datetime.now(timezone.utc).timestamp()

SOURCE_FILES = {
    "1535_doc": ROOT / "1535-Y5-local-locking-input-source-pass.md",
    "1535_validation": OUT / "P8_Y5_BRR545_1535_VALIDATION.csv",
    "1535_audit": OUT / "P8_Y5_PARENT_QLOC_1535_LOCKING_INPUT_SOURCE_AUDIT.csv",
    "1535_nohair": OUT / "P8_Y5_PARENT_QLOC_1535_EXACT_NOHAIR_STATUS.csv",
    "1535_leakage": OUT / "P8_Y5_PARENT_QLOC_1535_LEAKAGE_SCORE_STATUS.csv",
    "1535_priority": OUT / "P8_Y5_PARENT_QLOC_1535_NEXT_INPUT_PRIORITY.csv",
    "1534_nohair": OUT / "P8_Y5_PARENT_QLOC_1534_LOCAL_LOCKING_NOHAIR_THEOREM.csv",
    "1534_leakage": OUT / "P8_Y5_PARENT_QLOC_1534_QUADRATIC_LEAKAGE_BOUND_CONTRACT.csv",
    "1534_inputs": OUT / "P8_Y5_PARENT_QLOC_1534_LOCKING_INPUT_LEDGER.csv",
    "gamma_expansion": OUT / "P8_Y5_R10_798_GAMMA_SOURCE_EXPANSION.csv",
    "positive_nohair": OUT / "P8_Y5_R10_POSITIVE_OPERATOR_NOHAIR_ATTEMPT.csv",
    "boundary_certificate": OUT / "P8_Y5_PARENT_QLOC_1529_BOUNDARY_CERTIFICATE_AUDIT.csv",
    "energy_identity": OUT / "P8_EXTRA_SECTOR_SILENCE_ENERGY_IDENTITY.csv",
    "source_current": OUT / "P8_Y5_SOURCE_CURRENT_CLOSURE_THEOREM_ATTEMPT.csv",
    "source_measure": OUT / "P8_SOURCE_MEASURE_MEFF_FLUX_THEOREM.csv",
    "local_lock_map": OUT / "P8_Y5_BRR545_LOCAL_LOCK_MAP.csv",
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1536_SOURCE_REGISTER.csv"
JEFF_SPLIT = OUT / "P8_Y5_PARENT_QLOC_1536_JEFF_COMPONENT_SPLIT.csv"
BM_SPLIT = OUT / "P8_Y5_PARENT_QLOC_1536_BM_COMPONENT_SPLIT.csv"
SILENCE_AUDIT = OUT / "P8_Y5_PARENT_QLOC_1536_EXACT_SILENCE_AUDIT.csv"
NLOCK_ENVELOPE = OUT / "P8_Y5_PARENT_QLOC_1536_NLOCK_ENVELOPE_CONTRACT.csv"
RUNNER = OUT / "P8_Y5_PARENT_QLOC_1536_JEFF_BM_RUNNER.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1536_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1536_DECISION.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1536_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1536_VALIDATION.csv"

QUARANTINE = MICROSCOPE / "quarantine" / "1536"
QUAR_JEFF = QUARANTINE / "JEFF_COMPONENT_SPLIT_NONCLAIM.csv"
QUAR_BM = QUARANTINE / "BM_COMPONENT_SPLIT_NONCLAIM.csv"
QUAR_NLOCK = QUARANTINE / "NLOCK_ENVELOPE_CONTRACT_NONCLAIM.csv"
QUAR_DECISION = QUARANTINE / "DECISION_NONCLAIM.csv"
BRANCH_JEFF = BRANCH_RESIDUALS / "Jeff_component_split_nonclaim_1536.csv"
BRANCH_BM = BRANCH_RESIDUALS / "Bm_component_split_nonclaim_1536.csv"
BRANCH_NLOCK = BRANCH_RESIDUALS / "Nlock_envelope_contract_nonclaim_1536.csv"
BRANCH_DECISION = BRANCH_RESIDUALS / "Jeff_Bm_decision_nonclaim_1536.csv"


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
            "source_id": f"SRC1536_{index}_{key}",
            "source_path": rel(path),
            "exists": path.exists(),
            "purpose": "input evidence for J_eff/B_m source-boundary silence or bound",
            **flags(),
        }
        for index, (key, path) in enumerate(SOURCE_FILES.items())
    ]


def jeff_split_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "JEFF1536_0_screened_source",
            "J_src = U_B S_cg",
            "screened compact-source support term in the static relaxation law",
            "UNSIGNED_ZERO_OR_BOUND",
            "need U_B=0/source silence or finite ||U_B S_cg||_{E*}",
            "source",
            source_list("gamma_expansion", "positive_nohair", "1535_audit"),
        ),
        (
            "JEFF1536_1_baseline_drift",
            "J_drift_mL",
            "baseline/local-state drift from m_L or locked-state motion",
            "UNSIGNED_ZERO_OR_BOUND",
            "need locked baseline theorem or finite drift norm",
            "drift",
            source_list("gamma_expansion", "1534_nohair"),
        ),
        (
            "JEFF1536_2_Lcg_drift",
            "J_drift_Lcg",
            "drift from L_cg or trace-baseline variation in the local branch",
            "UNSIGNED_ZERO_OR_BOUND",
            "need L_cg local silence, fixed-source root branch, or finite drift norm",
            "drift",
            source_list("gamma_expansion", "1535_audit"),
        ),
        (
            "JEFF1536_3_selector_drift",
            "J_selector(Pi_B,mu_B,tau_L)",
            "screening selector and relaxation-parameter drift",
            "UNSIGNED_ZERO_OR_BOUND",
            "need parent-owned selector law or finite variation norm",
            "selector",
            source_list("gamma_expansion", "source_current"),
        ),
        (
            "JEFF1536_4_history",
            "J_history",
            "memory/history injection into the local relaxation equation",
            "UNSIGNED_ZERO_OR_BOUND",
            "need local causal/history silence or finite history norm",
            "history",
            source_list("energy_identity", "gamma_expansion"),
        ),
        (
            "JEFF1536_5_transition",
            "J_transition",
            "transition-current/K_perp leakage at branch interfaces",
            "UNSIGNED_ZERO_OR_BOUND",
            "GSE798 explicitly leaves transition-current assumptions unsigned",
            "transition",
            source_list("gamma_expansion", "1535_priority"),
        ),
        (
            "JEFF1536_6_source_current",
            "J_mass_current",
            "source-current/worldtube mass-flux mismatch that can feed local drift",
            "UNSIGNED_ZERO_OR_BOUND",
            "source-current closure and Meff flux equality remain conditional/not parent-derived",
            "source-current",
            source_list("source_current", "source_measure", "local_lock_map"),
        ),
        (
            "JEFF1536_7_verdict",
            "J_eff",
            "J_eff = J_src + J_drift_mL + J_drift_Lcg + J_selector + J_history + J_transition + J_mass_current",
            "SPLIT_COMPLETE_NOT_ZEROED",
            "no component has a parent-signed zero theorem or finite norm",
            "aggregate",
            source_list("1535_audit", "gamma_expansion", "source_current"),
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "component_id": component_id,
            "component": component,
            "meaning": meaning,
            "status": status,
            "missing_to_promote": missing,
            "category": category,
            "source_paths": sources,
            **flags(),
        }
        for component_id, component, meaning, status, missing, category, sources in rows
    ]


def bm_split_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "BM1536_0_inner_charge",
            "B_inner or Q_m^H",
            "inner compact-source boundary charge/monopole that can support exterior hair",
            "PRIMARY_BOUNDARY_CHARGE_OPEN",
            "positive-operator no-hair rows explicitly warn this is not automatic",
            "inner-boundary",
            source_list("positive_nohair", "boundary_certificate"),
        ),
        (
            "BM1536_1_no_flux",
            "B_no_flux",
            "Neumann/no-flux or Dirichlet boundary condition needed by the energy identity",
            "NO_FLUX_CERTIFICATE_MISSING",
            "1529 found no parent-signed boundary condition certificate",
            "boundary-condition",
            source_list("boundary_certificate", "1534_nohair"),
        ),
        (
            "BM1536_2_zero_mode_boundary",
            "B_zero_mode",
            "constant/gauge zero-mode reference coupled to boundary condition",
            "ZERO_MODE_CERTIFICATE_MISSING",
            "zero-mode/reference condition is required before Neumann no-hair can close",
            "zero-mode",
            source_list("boundary_certificate", "1535_audit"),
        ),
        (
            "BM1536_3_outer_flux",
            "B_outer",
            "outer/collar/reference-sphere flux or reference subtraction",
            "UNSIGNED_ZERO_OR_BOUND",
            "no fixed-reference or zero outer-flux theorem is live",
            "outer-boundary",
            source_list("boundary_certificate", "source_measure"),
        ),
        (
            "BM1536_4_history_boundary",
            "B_history",
            "history/memory injection through the boundary/collar",
            "UNSIGNED_ZERO_OR_BOUND",
            "memory-kernel silence is conditional and not source-backed",
            "history-boundary",
            source_list("energy_identity", "gamma_expansion"),
        ),
        (
            "BM1536_5_domain_motion",
            "B_domain",
            "domain/collar/support motion boundary work",
            "UNSIGNED_ZERO_OR_BOUND",
            "domain certificate is missing, so moving-support work cannot be deleted",
            "domain",
            source_list("boundary_certificate", "1535_audit"),
        ),
        (
            "BM1536_6_verdict",
            "B_m",
            "B_m = B_inner + B_no_flux + B_zero_mode + B_outer + B_history + B_domain",
            "SPLIT_COMPLETE_NOT_ZEROED",
            "no component has a parent-signed zero theorem or finite norm",
            "aggregate",
            source_list("1535_audit", "positive_nohair", "boundary_certificate"),
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "component_id": component_id,
            "component": component,
            "meaning": meaning,
            "status": status,
            "missing_to_promote": missing,
            "category": category,
            "source_paths": sources,
            **flags(),
        }
        for component_id, component, meaning, status, missing, category, sources in rows
    ]


def silence_audit_rows() -> list[dict[str, Any]]:
    rows = [
        ("SIL1536_0_Jsrc", "J_src=0", "BLOCKED", "requires U_B S_cg source silence"),
        ("SIL1536_1_Jdrift", "J_drift=0", "BLOCKED", "baseline/L_cg/selector drift silence unsigned"),
        ("SIL1536_2_Jhistory", "J_history+J_transition=0", "BLOCKED", "history and transition-current silence unsigned"),
        ("SIL1536_3_Jmass", "J_mass_current=0", "BLOCKED", "source-current/Meff flux closure not parent-derived"),
        ("SIL1536_4_Binner", "B_inner=0", "BLOCKED", "inner charge can encode source monopole"),
        ("SIL1536_5_Bboundary", "B_no_flux+B_outer+B_domain=0", "BLOCKED", "boundary/domain/no-flux certificate missing"),
        ("SIL1536_6_exact_lock", "J_eff=0 and B_m=0", "NOT_PROVED", "no exact source-boundary silence theorem can be promoted"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "silence_id": silence_id,
            "condition": condition,
            "status": status,
            "reason": reason,
            "source_paths": source_list("1535_nohair", "gamma_expansion", "positive_nohair", "boundary_certificate"),
            **flags(),
        }
        for silence_id, condition, status, reason in rows
    ]


def nlock_envelope_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "NLOCK1536_0_energy_identity",
            "E_m(u)^2 = <u,J_eff> + B_m",
            "starting point from 1534 no-hair/leakage gate",
            "IMPORTED_IDENTITY",
        ),
        (
            "NLOCK1536_1_dual_norm",
            "|<u,J_eff>| <= N_J E_m(u)",
            "N_J is an absolute-sum dual norm over J_eff components",
            "CONDITIONAL_BOUND_FORM",
        ),
        (
            "NLOCK1536_2_boundary_norm",
            "|B_m| <= N_B E_m(u)",
            "N_B is an absolute-sum boundary norm over B_m components",
            "CONDITIONAL_BOUND_FORM",
        ),
        (
            "NLOCK1536_3_component_sum",
            "N_J <= N_src+N_drift_mL+N_drift_Lcg+N_selector+N_history+N_transition+N_mass_current",
            "no cancellation among source/current pieces",
            "NO_CANCELLATION_ENVELOPE",
        ),
        (
            "NLOCK1536_4_boundary_sum",
            "N_B <= N_inner+N_no_flux+N_zero_mode+N_outer+N_history_boundary+N_domain",
            "no cancellation among boundary pieces",
            "NO_CANCELLATION_ENVELOPE",
        ),
        (
            "NLOCK1536_5_lock_norm",
            "E_m(u) <= N_lock := N_J + N_B",
            "finite leakage norm if all component norms are sourced",
            "CONDITIONAL_NLOCK_FORM",
        ),
        (
            "NLOCK1536_6_verdict",
            "N_lock is formula-ready but not numeric or theorem-zero",
            "all component norms are currently missing/unsigned",
            "NOT_SCORE_READY",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "envelope_id": envelope_id,
            "formula_or_rule": formula,
            "meaning": meaning,
            "status": status,
            "source_paths": source_list("1534_leakage", "1535_leakage", "1535_audit"),
            **flags(),
        }
        for envelope_id, formula, meaning, status in rows
    ]


def runner_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "RUN1536_0_exact_silence",
            "prove J_eff=B_m=0",
            "zero theorem for every J/B component",
            "all components unsigned",
            "BLOCKED_EXACT_SILENCE_NOT_PROVED",
        ),
        (
            "RUN1536_1_Nlock",
            "compute finite N_lock",
            "component dual/boundary norms for J_eff and B_m",
            "component split exists but no numeric/source-backed norms",
            "BLOCKED_COMPONENT_NORMS_MISSING",
        ),
        (
            "RUN1536_2_local_lock",
            "advance exact no-hair or leakage",
            "J/B zero or N_lock plus domain/operator constants",
            "J/B still open",
            "BLOCKED_LOCAL_LOCK_NOT_LIVE",
        ),
        (
            "RUN1536_3_local_GR",
            "promote local GR/Newton/PPN",
            "local lock plus hidden kernels/projection/source normalization",
            "pre-lock and hidden gates remain",
            "BLOCKED_NO_LOCAL_GR_CLAIM",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": runner_id,
            "route": route,
            "required_inputs": required,
            "current_inputs": current,
            "result": result,
            "source_paths": source_list("1535_audit", "1534_nohair", "1534_leakage"),
            **flags(),
        }
        for runner_id, route, required, current, result in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("GATE1536_0_split", "J_eff/B_m component split completed", "PASS_NONCLAIM", "components are explicit and source-linked"),
        ("GATE1536_1_exact_silence", "J_eff=B_m=0", "BLOCKED", "no componentwise zero theorem"),
        ("GATE1536_2_Nlock", "finite N_lock bound", "BLOCKED", "component norms missing"),
        ("GATE1536_3_local_lock", "delta m exact lock or scored leakage", "BLOCKED", "requires exact silence or N_lock"),
        ("GATE1536_4_local_GR", "local GR/Newton/PPN recovery claim", "BLOCKED_NO_CLAIM", "local branch remains nonclaim"),
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
        (
            "DEC1536_0_progress",
            "Keep the J_eff/B_m component split.",
            "COMPONENT_SPLIT_WRITTEN",
            "the source-boundary blocker is now decomposed rather than vague.",
        ),
        (
            "DEC1536_1_no_exact",
            "Do not claim exact no-hair.",
            "EXACT_SILENCE_BLOCKED",
            "no source or boundary component is parent-zeroed.",
        ),
        (
            "DEC1536_2_bound_route",
            "Use the absolute N_lock envelope as fallback.",
            "NLOCK_FORMULA_READY_NOT_NUMERIC",
            "component norms can make the leakage route scoreable later.",
        ),
        (
            "DEC1536_3_next",
            "Next target is a component norm input pack, prioritizing J_src and B_inner.",
            "NEXT_1537_COMPONENT_NORM_INPUT_PACK",
            "screened source support and inner boundary charge are the sharpest physical blockers.",
        ),
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
            "next_id": "NEXT1536_0_1537",
            "next_target": "1537-Y5-Jeff-Bm-component-norm-input-pack.md",
            "script": "scripts/Y5_Jeff_Bm_component_norm_input_pack.py",
            "objective": "source or construct nonclaim input rows for the N_lock component norms, prioritizing N_src=||U_B S_cg|| and N_inner from compact-source boundary charge; keep exact no-hair and local-GR claims blocked unless all components are zero/bounded",
            "do_not": "do not use cancellations among J/B components; do not claim inner boundary silence without source proof; do not promote local GR",
            **flags(),
        }
    ]


def copy_outputs() -> None:
    copies = [
        (JEFF_SPLIT, QUAR_JEFF),
        (BM_SPLIT, QUAR_BM),
        (NLOCK_ENVELOPE, QUAR_NLOCK),
        (DECISION, QUAR_DECISION),
        (JEFF_SPLIT, BRANCH_JEFF),
        (BM_SPLIT, BRANCH_BM),
        (NLOCK_ENVELOPE, BRANCH_NLOCK),
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
    jeff = read_csv(JEFF_SPLIT)
    bm = read_csv(BM_SPLIT)
    silence = read_csv(SILENCE_AUDIT)
    nlock = read_csv(NLOCK_ENVELOPE)
    runners = read_csv(RUNNER)
    gates = read_csv(CLAIM_GATE)
    decisions = read_csv(DECISION)
    next_rows = read_csv(NEXT_TARGET)

    jeff_categories = {row["category"] for row in jeff}
    bm_categories = {row["category"] for row in bm}
    checks = [
        ("VAL1536_0_sources_exist", all(row["exists"] == "True" for row in sources), "all cited 1536 input source paths exist"),
        ("VAL1536_1_Jeff_split_complete", {"source", "drift", "selector", "history", "transition", "source-current", "aggregate"}.issubset(jeff_categories), "J_eff split includes source, drift, selector, history, transition, source-current, aggregate"),
        ("VAL1536_2_Bm_split_complete", {"inner-boundary", "boundary-condition", "zero-mode", "outer-boundary", "history-boundary", "domain", "aggregate"}.issubset(bm_categories), "B_m split includes inner, condition, zero-mode, outer, history, domain, aggregate"),
        ("VAL1536_3_exact_silence_blocked", any(row["silence_id"] == "SIL1536_6_exact_lock" and row["status"] == "NOT_PROVED" for row in silence), "exact J/B silence remains not proved"),
        ("VAL1536_4_Nlock_written", any(row["envelope_id"] == "NLOCK1536_5_lock_norm" for row in nlock) and any(row["envelope_id"] == "NLOCK1536_6_verdict" and row["status"] == "NOT_SCORE_READY" for row in nlock), "N_lock absolute envelope written but not score-ready"),
        ("VAL1536_5_runners_blocked", all(row["result"].startswith("BLOCKED") for row in runners), "all J/B runners remain blocked"),
        ("VAL1536_6_claim_gates_block", any(row["gate_id"] == "GATE1536_4_local_GR" and row["status"] == "BLOCKED_NO_CLAIM" for row in gates), "local GR claim remains blocked"),
        ("VAL1536_7_decision_next", any(row["result"] == "NEXT_1537_COMPONENT_NORM_INPUT_PACK" for row in decisions), "decision selects component norm input pack next"),
        ("VAL1536_8_next_target", any("1537-Y5-Jeff-Bm-component" in row["next_target"] for row in next_rows), "next target is J_eff/B_m component norm input pack"),
        ("VAL1536_9_csv_parse", all(parse_csv(path) for path in generated_csvs), "all generated 1536 CSVs parse cleanly"),
        ("VAL1536_10_claim_flags_false", generated_flags_false(generated_csvs), "all generated prediction/claim flags remain false"),
        ("VAL1536_11_branch_copies", all(path.exists() for path in [QUAR_JEFF, QUAR_BM, QUAR_NLOCK, QUAR_DECISION, BRANCH_JEFF, BRANCH_BM, BRANCH_NLOCK, BRANCH_DECISION]), "branch/quarantine nonclaim copies written"),
        ("VAL1536_12_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent after run"),
        ("VAL1536_13_formalization_untouched", formalization_modified_count_since_start() == 0, "formalization modified-file count since start=0"),
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
            "check_id": "VAL1536_14_overall",
            "result": "PASS" if overall else "FAIL",
            "detail": "1536 splits J_eff and B_m, writes the absolute N_lock envelope, keeps exact no-hair/leakage/local-GR claims blocked, and selects component norm inputs next"
            if overall
            else "1536 validation failed; inspect failed rows before continuing",
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
    jeff: list[dict[str, Any]],
    bm: list[dict[str, Any]],
    silence: list[dict[str, Any]],
    nlock: list[dict[str, Any]],
    runners: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 1536 - J_eff / B_m Source-Boundary Silence or Bound",
                "",
                "## Verdict",
                "- `J_eff` and `B_m` are now split into explicit source, drift, history, transition, source-current, boundary, inner-charge, zero-mode, and domain pieces.",
                "- Exact local no-hair is still not proved: no componentwise zero theorem is live.",
                "- The finite leakage route is sharper: `E_m(u) <= N_lock := N_J + N_B`, with both `N_J` and `N_B` built as absolute sums.",
                "- No cancellation between source and boundary pieces is allowed.",
                "- Next target is a nonclaim component norm input pack, starting with `N_src=||U_B S_cg||` and the inner boundary/source charge norm.",
                "",
                "## Source Register",
                md_table(sources, ["source_id", "source_path", "exists", "purpose"]),
                "",
                "## J_eff Component Split",
                md_table(jeff, ["component_id", "component", "meaning", "status", "missing_to_promote", "category"]),
                "",
                "## B_m Component Split",
                md_table(bm, ["component_id", "component", "meaning", "status", "missing_to_promote", "category"]),
                "",
                "## Exact Silence Audit",
                md_table(silence, ["silence_id", "condition", "status", "reason"]),
                "",
                "## N_lock Envelope Contract",
                md_table(nlock, ["envelope_id", "formula_or_rule", "meaning", "status"]),
                "",
                "## J_eff / B_m Runner",
                md_table(runners, ["runner_id", "route", "required_inputs", "current_inputs", "result"]),
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
    jeff = jeff_split_rows()
    bm = bm_split_rows()
    silence = silence_audit_rows()
    nlock = nlock_envelope_rows()
    runners = runner_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(JEFF_SPLIT, jeff)
    write_csv(BM_SPLIT, bm)
    write_csv(SILENCE_AUDIT, silence)
    write_csv(NLOCK_ENVELOPE, nlock)
    write_csv(RUNNER, runners)
    write_csv(CLAIM_GATE, gates)
    write_csv(DECISION, decisions)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()
    remove_pycache()

    generated_csvs = [
        SOURCE_REGISTER,
        JEFF_SPLIT,
        BM_SPLIT,
        SILENCE_AUDIT,
        NLOCK_ENVELOPE,
        RUNNER,
        CLAIM_GATE,
        DECISION,
        NEXT_TARGET,
    ]
    validation = validation_rows(generated_csvs)
    write_csv(VALIDATION, validation)
    write_doc(sources, jeff, bm, silence, nlock, runners, gates, decisions, validation, next_rows)


if __name__ == "__main__":
    main()
