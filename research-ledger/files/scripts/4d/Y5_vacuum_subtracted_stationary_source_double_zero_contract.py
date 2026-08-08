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
DOC = ROOT / "1533-Y5-vacuum-subtracted-stationary-source-double-zero-contract.md"
START_TS = datetime.now(timezone.utc).timestamp()

SOURCE_FILES = {
    "1532_doc": ROOT / "1532-Y5-Lcg-parent-ownership-and-fixed-scale-silence-audit.md",
    "1532_validation": OUT / "P8_Y5_BRR545_1532_VALIDATION.csv",
    "1532_double_zero": OUT / "P8_Y5_PARENT_QLOC_1532_DOUBLE_ZERO_SOURCE_CONTRACT.csv",
    "1532_lcg_zero": OUT / "P8_Y5_PARENT_QLOC_1532_LCG_ZERO_CONTRACT.csv",
    "1532_lcg_audit": OUT / "P8_Y5_PARENT_QLOC_1532_LCG_OWNERSHIP_AUDIT.csv",
    "1531_zero": OUT / "P8_Y5_PARENT_QLOC_1531_ZERO_ROUTE_AUDIT.csv",
    "1531_envelope": OUT / "P8_Y5_PARENT_QLOC_1531_DELTAG_SGAMMA_BOUND_ENVELOPE.csv",
    "gk_contract": OUT / "P8_GK_METRIC_RESPONSE_CONTRACT.csv",
    "798_gamma": OUT / "P8_Y5_R10_798_GAMMA_SOURCE_EXPANSION.csv",
    "1289_derivative": OUT / "P8_Y5_R10_1289_FIRST_DERIVATIVE_TERM_ROW_NONCLAIM.csv",
    "1368_lcg_hunt": OUT / "P8_Y5_R10_1368_M_LCG_KERNEL_HUNT.csv",
    "double_zero_memory": OUT / "P8_DOUBLE_ZERO_MEMORY_SOURCE_REGISTER.csv",
    "double_zero_r11": OUT / "P8_DOUBLE_ZERO_R11_PARENT_SOURCE_REGISTER.csv",
    "yloc_parent_contract": OUT / "P8_YLOC_NO_LINEAR_SOURCE_PARENT_CONTRACT.csv",
    "yloc_theorem": OUT / "P8_YLOC_NO_LINEAR_SOURCE_THEOREM.csv",
    "energy_identity": OUT / "P8_EXTRA_SECTOR_SILENCE_ENERGY_IDENTITY.csv",
    "positive_nohair": OUT / "P8_Y5_R10_POSITIVE_OPERATOR_NOHAIR_ATTEMPT.csv",
    "local_lock_map": OUT / "P8_Y5_BRR545_LOCAL_LOCK_MAP.csv",
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1533_SOURCE_REGISTER.csv"
PARENT_ACTION_CONTRACT = OUT / "P8_Y5_PARENT_QLOC_1533_PARENT_ACTION_DOUBLE_ZERO_CONTRACT.csv"
DERIVATION = OUT / "P8_Y5_PARENT_QLOC_1533_DOUBLE_ZERO_DERIVATION.csv"
LOCKING_REQUIREMENTS = OUT / "P8_Y5_PARENT_QLOC_1533_LOCAL_LOCKING_REQUIREMENTS.csv"
REJECTION_LEDGER = OUT / "P8_Y5_PARENT_QLOC_1533_REJECTION_LEDGER.csv"
RUNNER = OUT / "P8_Y5_PARENT_QLOC_1533_DOUBLE_ZERO_RUNNER.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1533_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1533_DECISION.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1533_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1533_VALIDATION.csv"

QUARANTINE = MICROSCOPE / "quarantine" / "1533"
QUAR_PARENT = QUARANTINE / "PARENT_ACTION_DOUBLE_ZERO_CONTRACT_NONCLAIM.csv"
QUAR_DERIVATION = QUARANTINE / "DOUBLE_ZERO_DERIVATION_NONCLAIM.csv"
QUAR_LOCKING = QUARANTINE / "LOCAL_LOCKING_REQUIREMENTS_NONCLAIM.csv"
QUAR_DECISION = QUARANTINE / "DECISION_NONCLAIM.csv"
BRANCH_PARENT = BRANCH_RESIDUALS / "parent_action_double_zero_contract_nonclaim_1533.csv"
BRANCH_DERIVATION = BRANCH_RESIDUALS / "double_zero_derivation_nonclaim_1533.csv"
BRANCH_LOCKING = BRANCH_RESIDUALS / "local_locking_requirements_nonclaim_1533.csv"
BRANCH_DECISION = BRANCH_RESIDUALS / "double_zero_decision_nonclaim_1533.csv"


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
            "source_id": f"SRC1533_{index}_{key}",
            "source_path": rel(path),
            "exists": path.exists(),
            "purpose": "input evidence for vacuum-subtracted stationary-source double-zero contract",
            **flags(),
        }
        for index, (key, path) in enumerate(SOURCE_FILES.items())
    ]


def parent_action_contract_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "VAC1533_0_parent_variable",
            "m is a parent local memory variable with a same-branch Euler equation.",
            "m is not merely a fitted post-readout scalar; it is varied or constrained by the parent action.",
            "REQUIRED_UNSIGNED",
            "needed so m_* and stationarity are physical, not notation",
            source_list("1532_double_zero", "gk_contract", "yloc_parent_contract"),
        ),
        (
            "VAC1533_1_potential_source",
            "There exists a parent local source potential V(m) with stable stationary vacuum m_*.",
            "V'(m_*)=0 and V''(m_*) finite/nonnegative after gauge/constraint modes are removed.",
            "CONDITIONAL_PARENT_ACTION_FORM",
            "this is the cleanest way to derive F_prime(m_*)=0",
            source_list("1532_double_zero", "gk_contract", "798_gamma", "energy_identity"),
        ),
        (
            "VAC1533_2_vacuum_subtraction",
            "Define the source entering Gamma_eff by F_vac(m)=V(m)-V(m_*).",
            "This subtracts the vacuum density/source, not an empirical local-test fit.",
            "CONDITIONAL_PARENT_SUBTRACTION",
            "gives F_vac(m_*)=0 while preserving the stationary derivative V'(m_*)",
            source_list("1532_lcg_zero", "gk_contract", "double_zero_memory"),
        ),
        (
            "VAC1533_3_gamma_definition",
            "Gamma_eff=L_cg^-2 F_vac(m) in the local branch.",
            "The same branch and sign/volume convention must be used for Kmetric.",
            "CONDITIONAL_SAME_BRANCH_FORM",
            "links the parent source to the 1531/1532 Kmetric chain",
            source_list("798_gamma", "1289_derivative", "1531_envelope"),
        ),
        (
            "VAC1533_4_local_lock",
            "The local exterior must lock to m=m_* up to controlled source/boundary hair.",
            "A positive operator/no-hair or explicit finite bound is required.",
            "REQUIRED_UNSIGNED",
            "without lock, the double-zero is evaluated at the wrong field value",
            source_list("positive_nohair", "energy_identity", "local_lock_map"),
        ),
        (
            "VAC1533_5_hidden_residual_separation",
            "K_conn, K_domain, K_boundary, delta_g C, and active memory stress are separate residuals.",
            "The double-zero only silences the algebraic M_m/M_L coefficients.",
            "GUARDRAIL_REQUIRED",
            "prevents overclaiming local GR/Newton from an algebraic source theorem",
            source_list("1531_zero", "1532_lcg_zero", "1368_lcg_hunt"),
        ),
        (
            "VAC1533_6_verdict",
            "The parent-action double-zero contract can be written cleanly but is not live-proved by current corpus rows.",
            "Adopt it as a conditional theorem target, not a claim.",
            "CONTRACT_WRITTEN_NOT_CLAIMED",
            "next bottleneck is local locking/no-hair plus source/boundary control",
            source_list("1532_doc", "1532_validation", "1532_double_zero"),
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "contract_id": contract_id,
            "clause": clause,
            "math_or_test": math_or_test,
            "status": status,
            "why_needed": why_needed,
            "source_paths": sources,
            **flags(),
        }
        for contract_id, clause, math_or_test, status, why_needed, sources in rows
    ]


def derivation_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "DZD1533_0_stationary",
            "From parent stationarity at the local vacuum, V'(m_*)=0.",
            "Euler/stability premise of the parent local memory sector.",
            "CONDITIONAL_DERIVED_FROM_PREMISE",
            "requires real parent V and local vacuum branch",
        ),
        (
            "DZD1533_1_subtraction",
            "With F_vac(m)=V(m)-V(m_*), F_vac(m_*)=0.",
            "Direct evaluation at m=m_*.",
            "DERIVED_IDENTITY_CONDITIONAL",
            "requires parent-owned vacuum subtraction/background normalization",
        ),
        (
            "DZD1533_2_derivative",
            "F_vac'(m_*)=V'(m_*)=0.",
            "Differentiate the vacuum-subtracted source and use stationarity.",
            "DERIVED_IDENTITY_CONDITIONAL",
            "requires stationarity, not a fitted linear counterterm",
        ),
        (
            "DZD1533_3_quadratic_leakage",
            "F_vac(m_*+delta m)=1/2 V''(m_*) delta m^2+O(delta m^3).",
            "Taylor expansion around the stationary vacuum.",
            "QUADRATIC_SUPPRESSION_CONDITIONAL",
            "controls algebraic leakage only if delta m is locked/bounded",
        ),
        (
            "DZD1533_4_chain_silence",
            "delta Gamma_eff=L_cg^-2 F_vac'(m) delta m - 2L_cg^-3 F_vac(m) delta L_cg, so both algebraic coefficients vanish at m=m_*.",
            "Insert F_vac(m_*)=F_vac'(m_*)=0 into the chain rule.",
            "ALGEBRAIC_M_M_AND_M_L_ZERO_CONDITIONAL",
            "does not require M_L=0 or fixed L_cg, but requires local lock",
        ),
        (
            "DZD1533_5_no_full_stress_silence",
            "The chain silence does not remove kinetic/stability stress, boundary terms, domain/projector response, or delta_g C.",
            "Those are not multiplied solely by F_vac or F_vac'.",
            "NO_OVERCLAIM_GUARD",
            "local GR remains unclaimed",
        ),
        (
            "DZD1533_6_verdict",
            "The double-zero derivation is mathematically clean as a conditional parent-action contract.",
            "It is not a completed theorem because parent V, local lock, and hidden-kernel silence are unsigned.",
            "CONDITIONAL_THEOREM_NOT_LIVE_CLAIM",
            "advance to local locking/no-hair before attempting local-GR promotion",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "derivation_id": derivation_id,
            "statement": statement,
            "derivation": derivation,
            "status": status,
            "missing_to_promote": missing,
            "source_paths": source_list("1532_double_zero", "1532_lcg_zero", "798_gamma", "1289_derivative", "gk_contract"),
            **flags(),
        }
        for derivation_id, statement, derivation, status, missing in rows
    ]


def locking_requirement_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "LOCK1533_0_operator",
            "local memory perturbation delta m must obey a sourced positive operator or energy identity",
            "(-D_m Delta + M_scr^2)delta m = source + drift + boundary",
            "REQUIRED_UNSIGNED",
            "needed to evaluate F_vac at m_* rather than away from it",
        ),
        (
            "LOCK1533_1_source_silence",
            "compact local exterior source term must vanish or be bounded",
            "J_m=0 or ||J_m|| source-backed",
            "REQUIRED_UNSIGNED",
            "positive operator alone gives decay, not zero charge",
        ),
        (
            "LOCK1533_2_boundary_silence",
            "boundary/no-flux/history injection must vanish or be bounded",
            "boundary_flux=0 or finite boundary norm",
            "REQUIRED_UNSIGNED",
            "inner boundary hair can reintroduce local fifth-force terms",
        ),
        (
            "LOCK1533_3_mass_gap",
            "operator must have healthy sign and no unsuppressed zero mode",
            "Z_m>0 and M_scr^2>=0 with zero-mode gauge/constraint handled",
            "REQUIRED_UNSIGNED",
            "otherwise stationary point need not imply local locking",
        ),
        (
            "LOCK1533_4_leakage_bound",
            "if delta m is not zero, quadratic leakage must be propagated into q_loc/PPN bounds",
            "|F_vac|=O(delta m^2), |F_vac'|=O(delta m)",
            "BOUND_FALLBACK_REQUIRED",
            "keeps the route testable if exact no-hair fails",
        ),
        (
            "LOCK1533_5_verdict",
            "double-zero contract shifts the next hard work to local locking/no-hair",
            "prove delta m=0 or build a finite leakage bound",
            "NEXT_LOCKING_GATE",
            "this is the immediate derivation target before hidden-kernel cleanup",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "lock_id": lock_id,
            "requirement": requirement,
            "math_contract": math_contract,
            "status": status,
            "reason": reason,
            "source_paths": source_list("798_gamma", "positive_nohair", "energy_identity", "local_lock_map"),
            **flags(),
        }
        for lock_id, requirement, math_contract, status, reason in rows
    ]


def rejection_rows() -> list[dict[str, Any]]:
    rows = [
        ("REJ1533_0_fit_root", "choose m_* only because it fits local tests", "REJECTED", "the root must come from parent vacuum stationarity"),
        ("REJ1533_1_linear_counterterm_shortcut", "force F'=0 by arbitrary tangent subtraction without parent variation", "REJECTED", "looks like a tuned closure unless the counterterm is parent-owned"),
        ("REJ1533_2_fixed_Lcg_smuggle", "replace double-zero derivation with bare fixed L_cg axiom", "REJECTED_AS_PRIMARY_ROUTE", "1532 already found a cleaner route that does not over-assume L_cg ownership"),
        ("REJ1533_3_zero_without_lock", "use F(m_*)=F'(m_*)=0 while m is not locked to m_*", "REJECTED", "field can sit away from the double-zero under source/boundary hair"),
        ("REJ1533_4_local_GR_claim", "claim GR/Newton from algebraic chain silence alone", "REJECTED", "hidden kernels and active memory stress remain"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "rejection_id": rejection_id,
            "shortcut": shortcut,
            "status": status,
            "reason": reason,
            **flags(),
        }
        for rejection_id, shortcut, status, reason in rows
    ]


def runner_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "RUN1533_0_parent_double_zero",
            "prove F_vac(m_*)=F_vac'(m_*)=0",
            "parent V(m), stationary m_*, vacuum subtraction, same branch",
            "conditional theorem written; parent action not signed",
            "BLOCKED_PARENT_ACTION_UNSIGNED",
        ),
        (
            "RUN1533_1_chain_silence",
            "delete M_m and M_L algebraic Kmetric coefficients",
            "double-zero plus local lock m=m_*",
            "double-zero conditional; local lock missing",
            "BLOCKED_LOCAL_LOCK_MISSING",
        ),
        (
            "RUN1533_2_leakage_bound",
            "bound residual if delta m hair remains",
            "operator constants, source norms, boundary norms, V'' and local projection",
            "inputs missing",
            "BLOCKED_LEAKAGE_BOUND_INPUTS_MISSING",
        ),
        (
            "RUN1533_3_hidden_kernel_cleanup",
            "continue toward delta_g S_Gamma=0",
            "K_conn, K_domain, K_boundary, delta_g C, active stress",
            "not touched by double-zero contract",
            "BLOCKED_HIDDEN_KERNELS_REMAIN",
        ),
        (
            "RUN1533_4_local_GR",
            "promote local GR/Newton/PPN",
            "chain silence, local lock, hidden kernels, source normalization, projection",
            "multiple gates remain open",
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
            "source_paths": source_list("1532_double_zero", "1532_lcg_zero", "positive_nohair", "1531_zero"),
            **flags(),
        }
        for runner_id, route, required, current, result in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("GATE1533_0_contract_written", "parent-action double-zero contract is written", "PASS_NONCLAIM", "conditional theorem form is explicit"),
        ("GATE1533_1_stationary_source", "F_vac(m_*)=F_vac'(m_*)=0 is parent-derived", "BLOCKED", "actual parent V and vacuum branch are unsigned"),
        ("GATE1533_2_local_lock", "local branch locks to m=m_*", "BLOCKED", "positive operator/source/boundary gate not proven"),
        ("GATE1533_3_chain_silence", "M_m/M_L algebraic chain is deleted", "BLOCKED", "requires live double-zero plus local lock"),
        ("GATE1533_4_hidden_kernels", "hidden kernels are zero/bounded", "BLOCKED", "K_conn/K_domain/K_boundary/delta_g C/active stress remain"),
        ("GATE1533_5_leakage_bound", "nonzero delta m leakage is bounded", "BLOCKED", "operator/source/boundary constants missing"),
        ("GATE1533_6_local_GR", "local GR/Newton/PPN recovery is claimable", "BLOCKED_NO_CLAIM", "this checkpoint is nonclaim and pre-local-lock"),
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
            "DEC1533_0_progress",
            "Adopt the vacuum-subtracted stationary source as the clean conditional double-zero contract.",
            "CONDITIONAL_CONTRACT_ADVANCES",
            "it kills the M_m and M_L algebraic coefficients without smuggling in fixed L_cg.",
        ),
        (
            "DEC1533_1_no_promotion",
            "Do not promote the contract to a live theorem yet.",
            "PARENT_AND_LOCK_UNSIGNED",
            "actual parent V(m), local branch lock, and hidden-kernel silence are missing.",
        ),
        (
            "DEC1533_2_best_next",
            "Go after local locking/no-hair for delta m.",
            "NEXT_1534_LOCAL_LOCKING_NOHAIR",
            "the double-zero only matters physically if the local branch is actually driven to m_* or leakage is bounded.",
        ),
        (
            "DEC1533_3_guardrail",
            "Keep local GR/Newton and PPN claims blocked.",
            "CLAIM_BLOCKED",
            "algebraic chain silence is one gate, not the whole local-GR reduction.",
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
            "next_id": "NEXT1533_0_1534",
            "next_target": "1534-Y5-local-memory-locking-nohair-or-leakage-bound.md",
            "script": "scripts/Y5_local_memory_locking_nohair_or_leakage_bound.py",
            "objective": "prove or bound local locking delta m -> 0 around the vacuum-subtracted stationary source, including positive operator sign, source silence, boundary/no-flux, zero-mode control, and quadratic leakage propagation",
            "do_not": "do not claim algebraic double-zero unless m is locked or leakage is bounded; do not erase hidden Kmetric kernels; do not promote local GR",
            **flags(),
        }
    ]


def copy_outputs() -> None:
    copies = [
        (PARENT_ACTION_CONTRACT, QUAR_PARENT),
        (DERIVATION, QUAR_DERIVATION),
        (LOCKING_REQUIREMENTS, QUAR_LOCKING),
        (DECISION, QUAR_DECISION),
        (PARENT_ACTION_CONTRACT, BRANCH_PARENT),
        (DERIVATION, BRANCH_DERIVATION),
        (LOCKING_REQUIREMENTS, BRANCH_LOCKING),
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
    parent = read_csv(PARENT_ACTION_CONTRACT)
    derivation = read_csv(DERIVATION)
    locking = read_csv(LOCKING_REQUIREMENTS)
    rejections = read_csv(REJECTION_LEDGER)
    runners = read_csv(RUNNER)
    gates = read_csv(CLAIM_GATE)
    decisions = read_csv(DECISION)
    next_rows = read_csv(NEXT_TARGET)

    checks = [
        ("VAL1533_0_sources_exist", all(row["exists"] == "True" for row in sources), "all cited 1533 input source paths exist"),
        ("VAL1533_1_parent_contract_written", any(row["contract_id"] == "VAC1533_2_vacuum_subtraction" for row in parent) and any(row["contract_id"] == "VAC1533_1_potential_source" for row in parent), "parent potential plus vacuum subtraction contract written"),
        ("VAL1533_2_double_zero_derived_conditionally", any(row["derivation_id"] == "DZD1533_4_chain_silence" and row["status"] == "ALGEBRAIC_M_M_AND_M_L_ZERO_CONDITIONAL" for row in derivation), "conditional chain-silence derivation written"),
        ("VAL1533_3_quadratic_leakage", any(row["derivation_id"] == "DZD1533_3_quadratic_leakage" for row in derivation), "quadratic leakage law recorded"),
        ("VAL1533_4_locking_requirements", any(row["lock_id"] == "LOCK1533_5_verdict" and row["status"] == "NEXT_LOCKING_GATE" for row in locking), "local locking/no-hair selected as next gate"),
        ("VAL1533_5_shortcuts_rejected", len(rejections) >= 5 and all(row["status"].startswith("REJECTED") for row in rejections), "unsafe double-zero shortcuts rejected"),
        ("VAL1533_6_runners_blocked", all(row["result"].startswith("BLOCKED") for row in runners), "all score/claim runners remain blocked"),
        ("VAL1533_7_claim_gates_block", any(row["gate_id"] == "GATE1533_6_local_GR" and row["status"] == "BLOCKED_NO_CLAIM" for row in gates), "local GR claim remains blocked"),
        ("VAL1533_8_decision_next", any(row["result"] == "NEXT_1534_LOCAL_LOCKING_NOHAIR" for row in decisions), "decision selects local locking/no-hair next"),
        ("VAL1533_9_next_target", any("1534-Y5-local-memory-locking" in row["next_target"] for row in next_rows), "next target is local memory locking/no-hair or leakage bound"),
        ("VAL1533_10_csv_parse", all(parse_csv(path) for path in generated_csvs), "all generated 1533 CSVs parse cleanly"),
        ("VAL1533_11_claim_flags_false", generated_flags_false(generated_csvs), "all generated prediction/claim flags remain false"),
        ("VAL1533_12_branch_copies", all(path.exists() for path in [QUAR_PARENT, QUAR_DERIVATION, QUAR_LOCKING, QUAR_DECISION, BRANCH_PARENT, BRANCH_DERIVATION, BRANCH_LOCKING, BRANCH_DECISION]), "branch/quarantine nonclaim copies written"),
        ("VAL1533_13_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent after run"),
        ("VAL1533_14_formalization_untouched", formalization_modified_count_since_start() == 0, "formalization modified-file count since start=0"),
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
            "check_id": "VAL1533_15_overall",
            "result": "PASS" if overall else "FAIL",
            "detail": "1533 writes a conditional parent-action double-zero theorem, rejects fitted shortcuts, keeps claims blocked, and selects local locking/no-hair as the next gate"
            if overall
            else "1533 validation failed; inspect failed rows before continuing",
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
    parent: list[dict[str, Any]],
    derivation: list[dict[str, Any]],
    locking: list[dict[str, Any]],
    rejections: list[dict[str, Any]],
    runners: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 1533 - Vacuum-Subtracted Stationary Source Double-Zero Contract",
                "",
                "## Verdict",
                "- A clean conditional parent-action route exists: let `F_vac(m)=V(m)-V(m_*)` where `m_*` is a stationary parent vacuum of `V`.",
                "- Then `F_vac(m_*)=0` and `F_vac'(m_*)=0`, so the algebraic `M_m` and `M_L` Kmetric-chain coefficients vanish at the locked local vacuum.",
                "- This is better than assuming fixed `L_cg`, because the `L_cg` response is killed by its coefficient rather than by a scale axiom.",
                "- It is still not a claim: the actual parent `V(m)`, local locking to `m_*`, boundary/source silence, hidden kernels, and active memory stress remain unsigned.",
                "- Next target is local memory locking/no-hair or a finite quadratic leakage bound.",
                "",
                "## Source Register",
                md_table(sources, ["source_id", "source_path", "exists", "purpose"]),
                "",
                "## Parent Action Contract",
                md_table(parent, ["contract_id", "clause", "math_or_test", "status", "why_needed"]),
                "",
                "## Double-Zero Derivation",
                md_table(derivation, ["derivation_id", "statement", "derivation", "status", "missing_to_promote"]),
                "",
                "## Local Locking Requirements",
                md_table(locking, ["lock_id", "requirement", "math_contract", "status", "reason"]),
                "",
                "## Rejection Ledger",
                md_table(rejections, ["rejection_id", "shortcut", "status", "reason"]),
                "",
                "## Double-Zero Runner",
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
    parent = parent_action_contract_rows()
    derivation = derivation_rows()
    locking = locking_requirement_rows()
    rejections = rejection_rows()
    runners = runner_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(PARENT_ACTION_CONTRACT, parent)
    write_csv(DERIVATION, derivation)
    write_csv(LOCKING_REQUIREMENTS, locking)
    write_csv(REJECTION_LEDGER, rejections)
    write_csv(RUNNER, runners)
    write_csv(CLAIM_GATE, gates)
    write_csv(DECISION, decisions)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()
    remove_pycache()

    generated_csvs = [
        SOURCE_REGISTER,
        PARENT_ACTION_CONTRACT,
        DERIVATION,
        LOCKING_REQUIREMENTS,
        REJECTION_LEDGER,
        RUNNER,
        CLAIM_GATE,
        DECISION,
        NEXT_TARGET,
    ]
    validation = validation_rows(generated_csvs)
    write_csv(VALIDATION, validation)
    write_doc(sources, parent, derivation, locking, rejections, runners, gates, decisions, validation, next_rows)


if __name__ == "__main__":
    main()
