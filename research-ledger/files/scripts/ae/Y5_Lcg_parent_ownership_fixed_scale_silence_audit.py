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
DOC = ROOT / "1532-Y5-Lcg-parent-ownership-and-fixed-scale-silence-audit.md"
START_TS = datetime.now(timezone.utc).timestamp()

SOURCE_FILES = {
    "1531_doc": ROOT / "1531-Y5-delta-g-SGamma-Kmetric-kernel-norm-source-pass.md",
    "1531_validation": OUT / "P8_Y5_BRR545_1531_VALIDATION.csv",
    "1531_audit": OUT / "P8_Y5_PARENT_QLOC_1531_KMETRIC_KERNEL_NORM_SOURCE_AUDIT.csv",
    "1531_envelope": OUT / "P8_Y5_PARENT_QLOC_1531_DELTAG_SGAMMA_BOUND_ENVELOPE.csv",
    "1531_zero": OUT / "P8_Y5_PARENT_QLOC_1531_ZERO_ROUTE_AUDIT.csv",
    "1368_lcg_hunt": OUT / "P8_Y5_R10_1368_M_LCG_KERNEL_HUNT.csv",
    "1299_trace": OUT / "P8_Y5_R10_1299_SPATIAL_TRACE_KERNEL_ROWS_NONCLAIM.csv",
    "798_gamma": OUT / "P8_Y5_R10_798_GAMMA_SOURCE_EXPANSION.csv",
    "gk_contract": OUT / "P8_GK_METRIC_RESPONSE_CONTRACT.csv",
    "1289_derivative": OUT / "P8_Y5_R10_1289_FIRST_DERIVATIVE_TERM_ROW_NONCLAIM.csv",
    "1367_chain": OUT / "P8_Y5_R10_1367_KMETRIC_CHAIN_KERNEL_ATTEMPT.csv",
    "1525_kernel_req": OUT / "P8_Y5_PARENT_QLOC_1525_KMETRIC_KERNEL_REQUIREMENTS.csv",
    "1529_boundary": OUT / "P8_Y5_PARENT_QLOC_1529_BOUNDARY_CERTIFICATE_AUDIT.csv",
    "1523_units": OUT / "P8_Y5_PARENT_QLOC_1523_UNITS_LEDGER.csv",
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1532_SOURCE_REGISTER.csv"
OWNERSHIP_AUDIT = OUT / "P8_Y5_PARENT_QLOC_1532_LCG_OWNERSHIP_AUDIT.csv"
ZERO_CONTRACT = OUT / "P8_Y5_PARENT_QLOC_1532_LCG_ZERO_CONTRACT.csv"
DOUBLE_ZERO_CONTRACT = OUT / "P8_Y5_PARENT_QLOC_1532_DOUBLE_ZERO_SOURCE_CONTRACT.csv"
RUNNER = OUT / "P8_Y5_PARENT_QLOC_1532_LCG_RUNNER.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1532_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1532_DECISION.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1532_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1532_VALIDATION.csv"

QUARANTINE = MICROSCOPE / "quarantine" / "1532"
QUAR_OWNERSHIP = QUARANTINE / "LCG_OWNERSHIP_AUDIT_NONCLAIM.csv"
QUAR_ZERO = QUARANTINE / "LCG_ZERO_CONTRACT_NONCLAIM.csv"
QUAR_DOUBLE = QUARANTINE / "DOUBLE_ZERO_SOURCE_CONTRACT_NONCLAIM.csv"
QUAR_DECISION = QUARANTINE / "DECISION_NONCLAIM.csv"
BRANCH_OWNERSHIP = BRANCH_RESIDUALS / "lcg_ownership_audit_nonclaim_1532.csv"
BRANCH_ZERO = BRANCH_RESIDUALS / "lcg_zero_contract_nonclaim_1532.csv"
BRANCH_DOUBLE = BRANCH_RESIDUALS / "double_zero_source_contract_nonclaim_1532.csv"
BRANCH_DECISION = BRANCH_RESIDUALS / "lcg_decision_nonclaim_1532.csv"


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
            "source_id": f"SRC1532_{index}_{key}",
            "source_path": rel(path),
            "exists": path.exists(),
            "purpose": "input evidence for L_cg parent-ownership and fixed-scale silence audit",
            **flags(),
        }
        for index, (key, path) in enumerate(SOURCE_FILES.items())
    ]


def ownership_audit_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "LCG1532_0_fixed_scale",
            "parent-fixed external/local scale",
            "If L_cg is a parent-fixed scalar scale held fixed in Hilbert variation, then M_L^{mu nu}=delta_g L_cg=0 for the algebraic chain.",
            "CANDIDATE_CLEAN_BUT_UNSIGNED",
            "requires parent declaration that L_cg is not a metric-composite readout and does not vary under delta_g",
            "could remove the L_cg chain term, but invites scrutiny about covariance/scale ownership if not derived",
            source_list("1368_lcg_hunt", "1299_trace", "1289_derivative"),
        ),
        (
            "LCG1532_1_quotient_owned",
            "quotient-owned scale",
            "If L_cg = Lbar(q(Phi),theta) and q plus theta descend metric-silently, then delta_g L_cg=0 in the same quotient branch.",
            "CANDIDATE_DESCENT_ROUTE_UNSIGNED",
            "requires explicit quotient map, clock/scale variable theta, and proof of metric-silent descent",
            "more covariant than a bare external scale, but currently not sourced as a theorem",
            source_list("1531_audit", "gk_contract", "1523_units"),
        ),
        (
            "LCG1532_2_metric_composite",
            "metric-composite scale",
            "If L_cg is built from proper length, curvature, density, domain size, projector support, or local collar geometry, M_L generically survives.",
            "COUNTERBRANCH_RETAINED",
            "requires explicit M_L norm or a later zero theorem",
            "local-GR branch remains blocked if this is the parent choice",
            source_list("1368_lcg_hunt", "1299_trace", "1525_kernel_req"),
        ),
        (
            "LCG1532_3_F_root_route",
            "source-root route",
            "The L_cg response is multiplied by F(m); if the local vacuum is parent-locked to F(m_*)=0, the algebraic L_cg term vanishes even when M_L is not known.",
            "BEST_ALGEBRAIC_ROUTE_UNSIGNED",
            "requires parent-signed vacuum subtraction/root condition F(m_*)=0",
            "less dependent on declaring L_cg fixed; still leaves hidden kernels and active stress",
            source_list("798_gamma", "gk_contract", "1289_derivative", "1531_envelope"),
        ),
        (
            "LCG1532_4_double_zero_route",
            "vacuum-subtracted stationary source",
            "If F(m_*)=0 and F_prime(m_*)=0 in the same branch, both algebraic M_m and M_L chain coefficients vanish at the locked local vacuum.",
            "STRONGEST_CLEAN_CONTRACT_UNSIGNED",
            "requires parent action to make m_* a stationary source root, not just a fitted cancellation",
            "turns the algebraic Kmetric chain from a live residual into a theorem target",
            source_list("798_gamma", "gk_contract", "1531_zero"),
        ),
        (
            "LCG1532_5_gradient_vs_variation",
            "nabla L_cg versus delta_g L_cg",
            "Local-gradient suppression and Hilbert metric-variation silence are different gates; one cannot substitute for the other.",
            "GUARDRAIL_RETAINED",
            "requires separate proof for local source gradient and metric-response stress",
            "prevents accidental proof-smuggling between q_loc force and Kmetric stress",
            source_list("798_gamma", "1368_lcg_hunt", "1531_envelope"),
        ),
        (
            "LCG1532_6_numeric_bound_route",
            "finite retained M_L bound",
            "If neither fixed-scale nor source-root route is signed, the fallback is |R_L| <= 2|C_sign| L_cg^-3 |F| ||M_L|| with sourced lower bound on L_cg.",
            "BOUND_ROUTE_MISSING_INPUTS",
            "requires L_cg lower bound, F bound, M_L norm, sign/units, and projector/domain convention",
            "fallback remains nonclaim and not score-ready",
            source_list("1299_trace", "1531_audit", "1523_units"),
        ),
        (
            "LCG1532_7_verdict",
            "L_cg branch verdict",
            "Do not promote fixed-scale silence; pursue the vacuum-subtracted stationary source contract first because it can delete the L_cg coefficient without over-assuming L_cg ownership.",
            "NEXT_DOUBLE_ZERO_CONTRACT",
            "F(m_*)=F_prime(m_*)=0 must be parent-derived",
            "selects 1533 as the next derivation target",
            source_list("1531_doc", "798_gamma", "gk_contract"),
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "audit_id": audit_id,
            "route": route,
            "statement": statement,
            "status": status,
            "missing_to_promote": missing,
            "effect": effect,
            "source_paths": sources,
            **flags(),
        }
        for audit_id, route, statement, status, missing, effect, sources in rows
    ]


def zero_contract_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "ZLCG1532_0_chain_identity",
            "delta Gamma_eff = L_cg^-2 F_prime(m) delta m - 2 L_cg^-3 F(m) delta L_cg",
            "SOURCE_BACKED_IDENTITY",
            "this is the exact algebraic place where L_cg enters",
        ),
        (
            "ZLCG1532_1_fixed_scale_sufficient",
            "M_L=0 is sufficient to remove the L_cg algebraic chain term.",
            "SUFFICIENT_CONDITION_UNSIGNED",
            "requires parent-fixed or quotient-silent L_cg",
        ),
        (
            "ZLCG1532_2_source_root_sufficient",
            "F(m_*)=0 is sufficient to remove the L_cg algebraic chain term at the locked local vacuum.",
            "SUFFICIENT_CONDITION_UNSIGNED",
            "does not require M_L=0, but requires a real parent root",
        ),
        (
            "ZLCG1532_3_double_zero_sufficient",
            "F(m_*)=0 and F_prime(m_*)=0 remove both algebraic M_L and M_m coefficients at the fixed point.",
            "STRONG_CONDITION_UNSIGNED",
            "the strongest clean route for the algebraic chain",
        ),
        (
            "ZLCG1532_4_same_branch",
            "The root/stationary conditions must be in the same parent action, local vacuum branch, and variation convention as Kmetric.",
            "REQUIRED_GUARD",
            "prevents mixing an empirical fitting root with a formal Hilbert-variation theorem",
        ),
        (
            "ZLCG1532_5_not_full_local_GR",
            "Even a double-zero algebraic chain does not delete K_conn, K_domain, K_boundary, delta_g C, or active memory stress.",
            "NO_OVERCLAIM_GUARD",
            "local-GR/Newton remains blocked until hidden kernels are handled",
        ),
        (
            "ZLCG1532_6_verdict",
            "The L_cg algebraic problem has an exact contract, but no parent proof yet.",
            "CONTRACT_WRITTEN_NOT_PROVED",
            "advance to deriving the vacuum-subtracted stationary source from a parent action",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "contract_id": contract_id,
            "clause": clause,
            "status": status,
            "reason": reason,
            "source_paths": source_list("798_gamma", "1289_derivative", "1531_zero", "1368_lcg_hunt"),
            **flags(),
        }
        for contract_id, clause, status, reason in rows
    ]


def double_zero_contract_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "DZ1532_0_parent_field",
            "Declare m as a parent local vacuum variable or readout with a same-branch Euler equation.",
            "REQUIRED_UNSIGNED",
            "without an owned m equation, F root language is a closure",
        ),
        (
            "DZ1532_1_stationary",
            "Derive F_prime(m_*)=0 from stationarity of the local source/vacuum functional, not from fitting.",
            "REQUIRED_UNSIGNED",
            "this is the m-chain deletion clause",
        ),
        (
            "DZ1532_2_vacuum_subtraction",
            "Set F(m_*)=0 by parent-owned background subtraction so the local vacuum source is zero.",
            "REQUIRED_UNSIGNED",
            "this is the L_cg-chain deletion clause",
        ),
        (
            "DZ1532_3_stability",
            "Require F_second(m_*) finite and nonnegative or otherwise bounded.",
            "REQUIRED_UNSIGNED",
            "keeps the local branch stable and controls quadratic leakage",
        ),
        (
            "DZ1532_4_locking",
            "Prove the local branch locks to m=m_* up to controlled boundary/source hair.",
            "REQUIRED_UNSIGNED",
            "without locking, F and F_prime are evaluated away from the double zero",
        ),
        (
            "DZ1532_5_hidden_residuals",
            "State explicitly that hidden metric kernels are separate and not solved by the double zero.",
            "GUARDRAIL",
            "prevents overclaiming local GR from algebra alone",
        ),
        (
            "DZ1532_6_verdict",
            "The double-zero source contract is the best next derivation target.",
            "NEXT_TARGET",
            "it is cleaner than a bare fixed-scale axiom and directly attacks both algebraic chain coefficients",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "double_zero_id": double_zero_id,
            "requirement": requirement,
            "status": status,
            "reason": reason,
            "source_paths": source_list("gk_contract", "798_gamma", "1531_zero"),
            **flags(),
        }
        for double_zero_id, requirement, status, reason in rows
    ]


def runner_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "RUN1532_0_fixed_scale",
            "promote M_L=0 from fixed L_cg",
            "parent declaration that L_cg is fixed/quotient-silent plus units/covariance convention",
            "route identified but unsigned",
            "BLOCKED_FIXED_SCALE_UNSIGNED",
        ),
        (
            "RUN1532_1_source_root",
            "promote L_cg algebraic coefficient zero from F(m_*)=0",
            "parent vacuum subtraction/root theorem and local branch lock",
            "contract written but not proved",
            "BLOCKED_SOURCE_ROOT_UNSIGNED",
        ),
        (
            "RUN1532_2_double_zero",
            "delete both M_m and M_L algebraic coefficients",
            "F(m_*)=0, F_prime(m_*)=0, same branch, local lock",
            "best next derivation target",
            "BLOCKED_PARENT_DOUBLE_ZERO_MISSING",
        ),
        (
            "RUN1532_3_bound_route",
            "retain M_L and bound it numerically",
            "L_cg lower bound, F bound, M_L norm, sign/units, projector/domain convention",
            "inputs missing",
            "BLOCKED_BOUND_INPUTS_MISSING",
        ),
        (
            "RUN1532_4_local_GR",
            "promote local-GR/Newton/PPN",
            "algebraic chain zero plus hidden kernels and active stress handled",
            "hidden kernels and active stress still open",
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
            "source_paths": source_list("1531_audit", "1368_lcg_hunt", "798_gamma", "gk_contract"),
            **flags(),
        }
        for runner_id, route, required, current, result in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("GATE1532_0_ownership_audit", "L_cg ownership alternatives audited", "PASS_NONCLAIM", "fixed, quotient, metric-composite, source-root, and bound routes are separated"),
        ("GATE1532_1_fixed_scale", "M_L=0 via fixed L_cg", "BLOCKED", "parent-fixed/quotient-silent L_cg is not signed"),
        ("GATE1532_2_source_root", "M_L term deleted by F(m_*)=0", "BLOCKED", "vacuum-subtracted root is not parent-derived"),
        ("GATE1532_3_double_zero", "algebraic chain deleted by F=F_prime=0", "BLOCKED", "stationary source root and branch lock missing"),
        ("GATE1532_4_bound", "M_L retained and bounded", "BLOCKED", "numeric/theorem inputs missing"),
        ("GATE1532_5_hidden", "hidden kernels solved", "BLOCKED", "K_conn/K_domain/K_boundary/delta_g C/active stress remain separate"),
        ("GATE1532_6_local_GR", "local GR/Newton/PPN recovery claim", "BLOCKED_NO_CLAIM", "no local-GR claim follows from 1532"),
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
            "DEC1532_0_result",
            "Do not promote L_cg fixed-scale silence.",
            "FIXED_SCALE_UNSIGNED",
            "it is available as a route, but without parent ownership it would look axiomatic.",
        ),
        (
            "DEC1532_1_best_route",
            "Prefer the vacuum-subtracted stationary source contract.",
            "DOUBLE_ZERO_ROUTE_BEST_NEXT",
            "F(m_*)=0 deletes the L_cg coefficient and F_prime(m_*)=0 deletes the m coefficient without assuming L_cg is fixed.",
        ),
        (
            "DEC1532_2_no_claim",
            "Keep all local claims blocked.",
            "CLAIM_BLOCKED",
            "double-zero contract is not yet derived, and hidden kernels remain after it.",
        ),
        (
            "DEC1532_3_next",
            "Next target is a parent action contract for F(m_*)=F_prime(m_*)=0.",
            "NEXT_1533_DOUBLE_ZERO_SOURCE_CONTRACT",
            "derive the stationary vacuum-subtracted source or demote it to an explicit closure.",
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
            "next_id": "NEXT1532_0_1533",
            "next_target": "1533-Y5-vacuum-subtracted-stationary-source-double-zero-contract.md",
            "script": "scripts/Y5_vacuum_subtracted_stationary_source_double_zero_contract.py",
            "objective": "derive or reject the parent action contract F(m_*)=0 and F_prime(m_*)=0, including local locking, stability, background subtraction, and explicit separation of hidden kernels",
            "do_not": "do not claim local GR from the double-zero contract alone; do not use fitted cancellations; do not erase hidden kernels or active stress",
            **flags(),
        }
    ]


def copy_outputs() -> None:
    copies = [
        (OWNERSHIP_AUDIT, QUAR_OWNERSHIP),
        (ZERO_CONTRACT, QUAR_ZERO),
        (DOUBLE_ZERO_CONTRACT, QUAR_DOUBLE),
        (DECISION, QUAR_DECISION),
        (OWNERSHIP_AUDIT, BRANCH_OWNERSHIP),
        (ZERO_CONTRACT, BRANCH_ZERO),
        (DOUBLE_ZERO_CONTRACT, BRANCH_DOUBLE),
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
    ownership = read_csv(OWNERSHIP_AUDIT)
    zero_contract = read_csv(ZERO_CONTRACT)
    double_zero = read_csv(DOUBLE_ZERO_CONTRACT)
    runners = read_csv(RUNNER)
    gates = read_csv(CLAIM_GATE)
    decisions = read_csv(DECISION)
    next_rows = read_csv(NEXT_TARGET)

    ownership_ids = {row["audit_id"] for row in ownership}
    checks = [
        ("VAL1532_0_sources_exist", all(row["exists"] == "True" for row in sources), "all cited 1532 input source paths exist"),
        ("VAL1532_1_routes_separated", {"LCG1532_0_fixed_scale", "LCG1532_1_quotient_owned", "LCG1532_2_metric_composite", "LCG1532_3_F_root_route", "LCG1532_4_double_zero_route"}.issubset(ownership_ids), "fixed, quotient, metric-composite, source-root, and double-zero routes separated"),
        ("VAL1532_2_fixed_not_promoted", any(row["audit_id"] == "LCG1532_0_fixed_scale" and row["status"] == "CANDIDATE_CLEAN_BUT_UNSIGNED" for row in ownership), "fixed-scale silence remains unsigned"),
        ("VAL1532_3_double_zero_selected", any(row["audit_id"] == "LCG1532_4_double_zero_route" and row["status"] == "STRONGEST_CLEAN_CONTRACT_UNSIGNED" for row in ownership), "double-zero route identified as strongest clean contract"),
        ("VAL1532_4_zero_contract_written", any(row["contract_id"] == "ZLCG1532_3_double_zero_sufficient" for row in zero_contract), "sufficient double-zero algebraic silence clause written"),
        ("VAL1532_5_no_overclaim_guard", any(row["contract_id"] == "ZLCG1532_5_not_full_local_GR" for row in zero_contract), "double-zero no-overclaim guard retained"),
        ("VAL1532_6_parent_requirements", len(double_zero) >= 7 and all(row["status"] in {"REQUIRED_UNSIGNED", "GUARDRAIL", "NEXT_TARGET"} for row in double_zero), "parent double-zero requirements recorded as unsigned/guarded"),
        ("VAL1532_7_runners_blocked", all(row["result"].startswith("BLOCKED") for row in runners), "all L_cg runners remain blocked"),
        ("VAL1532_8_claim_gates_block", any(row["gate_id"] == "GATE1532_6_local_GR" and row["status"] == "BLOCKED_NO_CLAIM" for row in gates), "local GR claim remains blocked"),
        ("VAL1532_9_decision_next", any(row["result"] == "NEXT_1533_DOUBLE_ZERO_SOURCE_CONTRACT" for row in decisions), "decision selects parent double-zero source contract next"),
        ("VAL1532_10_next_target", any("1533-Y5-vacuum-subtracted" in row["next_target"] for row in next_rows), "next target is vacuum-subtracted stationary source double-zero contract"),
        ("VAL1532_11_csv_parse", all(parse_csv(path) for path in generated_csvs), "all generated 1532 CSVs parse cleanly"),
        ("VAL1532_12_claim_flags_false", generated_flags_false(generated_csvs), "all generated prediction/claim flags remain false"),
        ("VAL1532_13_branch_copies", all(path.exists() for path in [QUAR_OWNERSHIP, QUAR_ZERO, QUAR_DOUBLE, QUAR_DECISION, BRANCH_OWNERSHIP, BRANCH_ZERO, BRANCH_DOUBLE, BRANCH_DECISION]), "branch/quarantine nonclaim copies written"),
        ("VAL1532_14_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent after run"),
        ("VAL1532_15_formalization_untouched", formalization_modified_count_since_start() == 0, "formalization modified-file count since start=0"),
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
            "check_id": "VAL1532_16_overall",
            "result": "PASS" if overall else "FAIL",
            "detail": "1532 separates L_cg ownership routes, refuses unsigned fixed-scale silence, selects the vacuum-subtracted stationary source double-zero contract, and keeps local-GR claims blocked"
            if overall
            else "1532 validation failed; inspect failed rows before continuing",
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
    ownership: list[dict[str, Any]],
    zero_contract: list[dict[str, Any]],
    double_zero: list[dict[str, Any]],
    runners: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 1532 - Lcg Parent Ownership and Fixed-Scale Silence Audit",
                "",
                "## Verdict",
                "- Fixed-scale `L_cg` silence is a clean sufficient route, but it is not parent-signed and would look axiomatic if promoted now.",
                "- The stronger route is a vacuum-subtracted stationary source: `F(m_*)=0` deletes the `L_cg` coefficient and `F_prime(m_*)=0` deletes the `m` coefficient.",
                "- This is not a local-GR claim; it only targets the algebraic Kmetric chain.",
                "- Hidden `K_conn`, `K_domain`, `K_boundary`, background `delta_g C`, and active memory stress remain separate blockers.",
                "- Next target is to derive or reject the parent action contract for `F(m_*)=F_prime(m_*)=0`.",
                "",
                "## Source Register",
                md_table(sources, ["source_id", "source_path", "exists", "purpose"]),
                "",
                "## Lcg Ownership Audit",
                md_table(ownership, ["audit_id", "route", "statement", "status", "missing_to_promote", "effect"]),
                "",
                "## Lcg Zero Contract",
                md_table(zero_contract, ["contract_id", "clause", "status", "reason"]),
                "",
                "## Double-Zero Source Contract",
                md_table(double_zero, ["double_zero_id", "requirement", "status", "reason"]),
                "",
                "## Lcg Runner",
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
    ownership = ownership_audit_rows()
    zero_contract = zero_contract_rows()
    double_zero = double_zero_contract_rows()
    runners = runner_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(OWNERSHIP_AUDIT, ownership)
    write_csv(ZERO_CONTRACT, zero_contract)
    write_csv(DOUBLE_ZERO_CONTRACT, double_zero)
    write_csv(RUNNER, runners)
    write_csv(CLAIM_GATE, gates)
    write_csv(DECISION, decisions)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()
    remove_pycache()

    generated_csvs = [
        SOURCE_REGISTER,
        OWNERSHIP_AUDIT,
        ZERO_CONTRACT,
        DOUBLE_ZERO_CONTRACT,
        RUNNER,
        CLAIM_GATE,
        DECISION,
        NEXT_TARGET,
    ]
    validation = validation_rows(generated_csvs)
    write_csv(VALIDATION, validation)
    write_doc(sources, ownership, zero_contract, double_zero, runners, gates, decisions, validation, next_rows)


if __name__ == "__main__":
    main()
