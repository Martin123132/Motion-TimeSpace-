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
DOC = ROOT / "1531-Y5-delta-g-SGamma-Kmetric-kernel-norm-source-pass.md"
START_TS = datetime.now(timezone.utc).timestamp()

SOURCE_FILES = {
    "1530_doc": ROOT / "1530-Y5-lambda-phi-bound-input-source-pass.md",
    "1530_validation": OUT / "P8_Y5_BRR545_1530_VALIDATION.csv",
    "1530_deltag": OUT / "P8_Y5_PARENT_QLOC_1530_DELTA_G_SGAMMA_REDUCTION.csv",
    "1530_runner": OUT / "P8_Y5_PARENT_QLOC_1530_BOUND_INPUT_RUNNER.csv",
    "1530_gate": OUT / "P8_Y5_PARENT_QLOC_1530_CLAIM_GATE.csv",
    "1529_boundary": OUT / "P8_Y5_PARENT_QLOC_1529_BOUNDARY_CERTIFICATE_AUDIT.csv",
    "1525_kernel_req": OUT / "P8_Y5_PARENT_QLOC_1525_KMETRIC_KERNEL_REQUIREMENTS.csv",
    "1526_kernel_fallback": OUT / "P8_Y5_PARENT_QLOC_1526_RETAINED_KERNEL_FALLBACK.csv",
    "1368_lcg_hunt": OUT / "P8_Y5_R10_1368_M_LCG_KERNEL_HUNT.csv",
    "1367_chain": OUT / "P8_Y5_R10_1367_KMETRIC_CHAIN_KERNEL_ATTEMPT.csv",
    "1301_m_attempt": OUT / "P8_Y5_R10_1301_M_m_ij_DERIVATION_ATTEMPT.csv",
    "1301_fixed_contract": OUT / "P8_Y5_R10_1301_PARENT_FIXED_FIELD_CLOSURE_CONTRACT.csv",
    "1301_doc": ROOT / "1301-Y5-R10-RAB-parent-metric-response-components-for-m-spatial-trace.md",
    "1289_variation": OUT / "P8_Y5_R10_1289_KMETRIC_VARIATION_EXPANSION_NONCLAIM.csv",
    "1289_derivative": OUT / "P8_Y5_R10_1289_FIRST_DERIVATIVE_TERM_ROW_NONCLAIM.csv",
    "1288_blocker": OUT / "P8_Y5_R10_1288_KMETRIC_DERIVATIVE_TERM_BLOCKER.csv",
    "1287_volume": OUT / "P8_Y5_R10_1287_FIRST_KMETRIC_VOLUME_ROW_NONCLAIM.csv",
    "798_gamma": OUT / "P8_Y5_R10_798_GAMMA_SOURCE_EXPANSION.csv",
    "776_kgamma": OUT / "P8_Y5_R10_776_KGAMMA_METRIC_RESPONSE_LEDGER.csv",
    "gk_contract": OUT / "P8_GK_METRIC_RESPONSE_CONTRACT.csv",
    "gk_evidence": OUT / "P8_GK_METRIC_RESPONSE_SOURCE_EVIDENCE.csv",
    "gk_stress": OUT / "P8_GK_STRESS_ACTION_CANDIDATES.csv",
    "1523_units": OUT / "P8_Y5_PARENT_QLOC_1523_UNITS_LEDGER.csv",
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1531_SOURCE_REGISTER.csv"
KERNEL_AUDIT = OUT / "P8_Y5_PARENT_QLOC_1531_KMETRIC_KERNEL_NORM_SOURCE_AUDIT.csv"
BOUND_ENVELOPE = OUT / "P8_Y5_PARENT_QLOC_1531_DELTAG_SGAMMA_BOUND_ENVELOPE.csv"
ZERO_ROUTE = OUT / "P8_Y5_PARENT_QLOC_1531_ZERO_ROUTE_AUDIT.csv"
RUNNER = OUT / "P8_Y5_PARENT_QLOC_1531_KERNEL_NORM_RUNNER.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1531_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1531_DECISION.csv"
LOCAL_STATUS = OUT / "P8_Y5_PARENT_QLOC_1531_LOCAL_GR_NEWTON_STATUS.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1531_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1531_VALIDATION.csv"

QUARANTINE = MICROSCOPE / "quarantine" / "1531"
QUAR_KERNEL_AUDIT = QUARANTINE / "KMETRIC_KERNEL_NORM_SOURCE_AUDIT_NONCLAIM.csv"
QUAR_ENVELOPE = QUARANTINE / "DELTAG_SGAMMA_BOUND_ENVELOPE_NONCLAIM.csv"
QUAR_ZERO_ROUTE = QUARANTINE / "ZERO_ROUTE_AUDIT_NONCLAIM.csv"
QUAR_DECISION = QUARANTINE / "DECISION_NONCLAIM.csv"
BRANCH_KERNEL_AUDIT = BRANCH_RESIDUALS / "kmetric_kernel_norm_source_audit_nonclaim_1531.csv"
BRANCH_ENVELOPE = BRANCH_RESIDUALS / "delta_g_sgamma_bound_envelope_nonclaim_1531.csv"
BRANCH_ZERO_ROUTE = BRANCH_RESIDUALS / "delta_g_sgamma_zero_route_audit_nonclaim_1531.csv"
BRANCH_DECISION = BRANCH_RESIDUALS / "delta_g_sgamma_kernel_decision_nonclaim_1531.csv"


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
            "source_id": f"SRC1531_{index}_{key}",
            "source_path": rel(path),
            "exists": path.exists(),
            "purpose": "input evidence for delta_g S_Gamma Kmetric-kernel norm source pass",
            **flags(),
        }
        for index, (key, path) in enumerate(SOURCE_FILES.items())
    ]


def kernel_audit_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "KNA1531_0_C_sign",
            "C_sign",
            "Hilbert-stress sign and volume convention multiplying Kmetric_chain",
            "CONVENTION_REQUIRED_NOT_FIXED",
            "1289/776 identify the sign/volume branch but do not lock it to a claim-ready convention",
            "fixed action sign, volume normalization, and tensor-index convention",
            source_list("1289_derivative", "1289_variation", "776_kgamma", "gk_contract"),
        ),
        (
            "KNA1531_1_L_cg_value",
            "L_cg",
            "local coarse-graining scale and units",
            "SYMBOLIC_SOURCE_ONLY",
            "Gamma_eff=L_cg^-2 F(m) is sourced, but L_cg has no live parent value, range, or metric ownership",
            "parent definition of L_cg; units; local frame; numeric or theorem-bound range",
            source_list("798_gamma", "1368_lcg_hunt", "1523_units"),
        ),
        (
            "KNA1531_2_F_value",
            "F(m)",
            "memory-source function value at the local branch",
            "FUNCTION_FORM_MISSING",
            "F appears in the L_cg response term; no parent-selected F(m_*) or bound is sourced",
            "functional form, local fixed point m_*, F(m_*), and allowed branch range",
            source_list("798_gamma", "gk_contract", "1289_derivative"),
        ),
        (
            "KNA1531_3_F_prime",
            "F_prime(m)",
            "stationary derivative controlling the m-response term",
            "CONDITIONAL_DOUBLE_ZERO_ONLY",
            "MR514_5 and GSE798_2 state the desired double-zero/stationary condition, but the parent action has not signed it",
            "parent proof of F_prime(m_*)=0 or sourced nonzero bound",
            source_list("798_gamma", "gk_contract", "1289_derivative"),
        ),
        (
            "KNA1531_4_M_m",
            "M_m^{mu nu}",
            "metric-response kernel delta m/delta g_{mu nu}",
            "PARTIAL_CONDITIONAL_ZERO_NOT_LIVE",
            "1368/1301 give a clean route: if m is an independent parent scalar held fixed in Hilbert variation, the algebraic chain M_m can vanish; counterbranches and active memory stress remain",
            "parent choice of fixed-independent m; exclusion of metric-composite/projector/domain readout; separate memory-stress theorem or bound",
            source_list("1368_lcg_hunt", "1301_m_attempt", "1301_fixed_contract", "1301_doc"),
        ),
        (
            "KNA1531_5_M_L",
            "M_L^{mu nu}",
            "metric-response kernel delta L_cg/delta g_{mu nu}",
            "MISSING_PARENT_OWNERSHIP",
            "1368 identifies fixed-scale silence as the cleanest route, but L_cg is not yet declared parent-fixed, metric-silent, or metric-composite with a bound",
            "L_cg ownership theorem; fixed-scale silence; or explicit M_L norm with units",
            source_list("1368_lcg_hunt", "1367_chain", "1289_derivative", "1525_kernel_req"),
        ),
        (
            "KNA1531_6_K_conn",
            "K_conn^{mu nu}",
            "connection/covariant-derivative/Hodge/projector metric response",
            "OPEN_HIDDEN_KERNEL",
            "776/1525 retain derivative and projector stress terms; no same-branch local zero or bound is sourced",
            "connection variation theorem, local-collar bound, or proof that the operator descends metric-silently",
            source_list("776_kgamma", "1288_blocker", "1367_chain", "1525_kernel_req"),
        ),
        (
            "KNA1531_7_K_domain",
            "K_domain^{mu nu}",
            "domain, averaging cell, collar, and projection-support metric response",
            "OPEN_HIDDEN_KERNEL",
            "1525 retains domain/cell variation; 1529 does not provide a parent no-flux/domain certificate",
            "fixed support/domain theorem, quotient descent of the domain map, or finite domain-variation norm",
            source_list("1525_kernel_req", "1529_boundary", "gk_evidence"),
        ),
        (
            "KNA1531_8_K_boundary",
            "K_boundary^{mu nu}",
            "boundary, reference subtraction, and corner metric response",
            "OPEN_HIDDEN_KERNEL",
            "776/1525 retain boundary/reference terms; 1529 found no parent boundary/no-flux certificate for this branch",
            "boundary no-flux theorem, fixed-reference subtraction, or finite boundary kernel norm",
            source_list("776_kgamma", "1525_kernel_req", "1529_boundary", "gk_contract"),
        ),
        (
            "KNA1531_9_K_C",
            "K_C^{mu nu}=delta_g C",
            "metric response of the constant/background part in S_Gamma=(2/3)(Gamma_eff+C)",
            "BACKGROUND_SILENCE_UNSIGNED",
            "1530 reduction assumes delta_g C=0; no parent row yet signs that C is metric-silent or background-subtracted in this local variation",
            "metric-silence/background-subtraction proof for C, or finite K_C bound",
            source_list("1530_deltag", "gk_contract", "1289_variation"),
        ),
        (
            "KNA1531_10_units_norm",
            "operator norm and units",
            "shared norm for all Kmetric kernels entering ||delta_g S_Gamma||",
            "MISSING_UNIFIED_NORM",
            "1523 gives unit ledgers but no live same-frame operator norm for the Kmetric kernel pack",
            "single tensor norm, volume measure, unit conversion, and local-frame convention",
            source_list("1523_units", "1289_derivative", "1530_deltag"),
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "audit_id": audit_id,
            "quantity": quantity,
            "role": role,
            "status": status,
            "finding": finding,
            "missing_to_promote": missing,
            "source_paths": sources,
            **flags(),
        }
        for audit_id, quantity, role, status, finding, missing, sources in rows
    ]


def bound_envelope_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "ENV1531_0_imported_1530",
            "||delta_g S_Gamma||",
            "||delta_g S_Gamma|| <= (2/3)(L_cg^-2|F'| ||M_m|| + 2L_cg^-3|F| ||M_L|| + ||K_conn|| + ||K_domain|| + ||K_boundary||)",
            "IMPORTED_SYMBOLIC_ENVELOPE",
            "1530 envelope retained as the base no-cancellation form",
        ),
        (
            "ENV1531_1_background_constant",
            "K_C",
            "if delta_g C is not parent-signed zero, add +(2/3)||K_C|| to the envelope",
            "ADDED_GUARD_TERM",
            "prevents silent use of a metric-dependent background constant",
        ),
        (
            "ENV1531_2_convention_guard",
            "C_sign",
            "absolute-value scoring requires |C_sign| or a fixed convention; do not cancel sign branches",
            "NO_CANCELLATION_GUARD",
            "sign cannot be used to cancel M_m, M_L, or hidden kernels",
        ),
        (
            "ENV1531_3_M_m_pruning",
            "M_m term",
            "m-channel may be removed only if F'(m_*)=0 or M_m=0 in the same Hilbert-variation branch",
            "CONDITIONAL_PRUNING_ONLY",
            "partial progress exists, but no live deletion yet",
        ),
        (
            "ENV1531_4_M_L_pruning",
            "M_L term",
            "L_cg-channel may be removed only if F(m_*)=0 or M_L=0 in the same Hilbert-variation branch",
            "NEXT_CRITICAL_PRUNING_TARGET",
            "this is the cleanest next algebraic route because F_prime=0 does not touch the L_cg term",
        ),
        (
            "ENV1531_5_hidden_kernel_guard",
            "K_conn+K_domain+K_boundary",
            "hidden kernels remain additively retained unless separately zeroed or bounded",
            "RETAINED_RESIDUALS",
            "finite local-GR/PPN claim remains blocked",
        ),
        (
            "ENV1531_6_score_verdict",
            "delta_g S_Gamma score",
            "no numeric upper bound can be computed from current rows",
            "NOT_SCORE_READY",
            "every live kernel is missing either a zero theorem or a norm",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "envelope_id": envelope_id,
            "quantity": quantity,
            "formula_or_rule": formula,
            "status": status,
            "reason": reason,
            "source_paths": source_list("1530_deltag", "1367_chain", "1368_lcg_hunt", "1289_derivative"),
            **flags(),
        }
        for envelope_id, quantity, formula, status, reason in rows
    ]


def zero_route_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "ZERO1531_0_same_branch",
            "all zero clauses live in the same parent action and same Hilbert-variation convention",
            "UNSIGNED",
            "prevents mixing fixed-field, fixed-scale, and metric-composite branches",
        ),
        (
            "ZERO1531_1_background",
            "delta_g C=0 or C is background-subtracted before local variation",
            "UNSIGNED",
            "1530 reduction requires this but does not prove it",
        ),
        (
            "ZERO1531_2_m_channel",
            "F_prime(m_*)=0 or M_m^{mu nu}=0",
            "PARTIAL_CONDITIONAL",
            "fixed-independent m can prune the algebraic chain, but parent ownership and active memory stress are not closed",
        ),
        (
            "ZERO1531_3_Lcg_channel",
            "F(m_*)=0 or M_L^{mu nu}=0",
            "OPEN",
            "F_prime(m_*)=0 is insufficient; L_cg ownership is the next major clause",
        ),
        (
            "ZERO1531_4_connection",
            "K_conn^{mu nu}=0",
            "OPEN",
            "connection/projector/derivative metric response still retained",
        ),
        (
            "ZERO1531_5_domain",
            "K_domain^{mu nu}=0",
            "OPEN",
            "support/collar/domain response still retained",
        ),
        (
            "ZERO1531_6_boundary",
            "K_boundary^{mu nu}=0",
            "OPEN",
            "boundary/no-flux certificate not found in 1529",
        ),
        (
            "ZERO1531_7_verdict",
            "delta_g S_Gamma=0 theorem",
            "NOT_PROVED",
            "exact clauses are now listed; the theorem is blocked mainly by L_cg ownership and hidden kernels",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "zero_id": zero_id,
            "clause": clause,
            "status": status,
            "reason": reason,
            "source_paths": source_list("1530_deltag", "1368_lcg_hunt", "1525_kernel_req", "1529_boundary"),
            **flags(),
        }
        for zero_id, clause, status, reason in rows
    ]


def runner_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "RUN1531_0_zero_delta_g_SGamma",
            "prove ||delta_g S_Gamma||=0",
            "delta_g C=0; m-channel zero; Lcg-channel zero; K_conn=K_domain=K_boundary=0; same-branch convention",
            "m-channel has conditional partial route; Lcg and hidden kernels open",
            "BLOCKED_ZERO_THEOREM_INCOMPLETE",
            "L_cg parent ownership/fixed-scale silence first",
        ),
        (
            "RUN1531_1_bound_delta_g_SGamma",
            "produce finite source-backed norm",
            "numeric/theorem bounds for L_cg, F, F_prime, M_m, M_L, K_conn, K_domain, K_boundary, K_C, norm units",
            "symbolic formulas and missing kernels only",
            "BLOCKED_NUMERIC_KERNEL_NORMS_MISSING",
            "kernel norm source pack",
        ),
        (
            "RUN1531_2_lambda_phi_bound",
            "advance epsilon_lambda_phi bound from 1530",
            "delta_g S_Gamma norm plus C_P, C_E, C_T, R_norm, boundary/initial norms",
            "delta_g S_Gamma still not zero or bounded",
            "BLOCKED_BY_DELTAG_SGAMMA",
            "finish or bound Kmetric kernels first",
        ),
        (
            "RUN1531_3_DeltaK_Khat",
            "compare Kmetric to K_hat / DeltaK",
            "full Kmetric kernel pack with sign/units and hidden terms",
            "same kernel pack unresolved",
            "BLOCKED_SHARED_KMETRIC_BOTTLENECK",
            "do not promote Khat or local GR",
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
            "next_required_object": next_required,
            "source_paths": source_list("1530_runner", "1525_kernel_req", "1367_chain", "1368_lcg_hunt"),
            **flags(),
        }
        for runner_id, route, required, current, result, next_required in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("GATE1531_0_kernel_audit", "Kmetric kernel norm source audit completed", "PASS_NONCLAIM", "all live kernel slots are audited"),
        ("GATE1531_1_M_m", "m-channel deleted or bounded", "PARTIAL_BLOCKED", "conditional fixed-field route exists but is not parent-signed and active stress remains"),
        ("GATE1531_2_M_L", "L_cg channel deleted or bounded", "BLOCKED", "L_cg ownership/metric silence is missing"),
        ("GATE1531_3_hidden_kernels", "connection/domain/boundary kernels deleted or bounded", "BLOCKED", "K_conn, K_domain, and K_boundary remain open"),
        ("GATE1531_4_background_C", "background constant metric response deleted or bounded", "BLOCKED", "delta_g C silence is unsigned"),
        ("GATE1531_5_delta_g_SGamma", "delta_g S_Gamma is zero or bounded", "BLOCKED", "zero theorem and numeric bound both fail currently"),
        ("GATE1531_6_lambda_phi", "lambda_phi multiplier-stress bound can progress", "BLOCKED", "depends on delta_g S_Gamma plus domain constants"),
        ("GATE1531_7_local_GR", "derived local GR/Newton/PPN recovery is claimable", "BLOCKED_NO_CLAIM", "shared local residual branch remains nonclaim"),
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
            "DEC1531_0_progress",
            "Keep the 1530 delta_g S_Gamma reduction.",
            "SHARED_KERNEL_BOTTLENECK_CONFIRMED",
            "the lambda_phi multiplier problem and DeltaK/Khat problem now point to the same finite kernel pack.",
        ),
        (
            "DEC1531_1_partial_win",
            "Record the m-channel fixed-field route as partial but nonclaim.",
            "M_M_CONDITIONAL_ROUTE_EXISTS",
            "if the parent action owns m as an independent fixed scalar in Hilbert variation, one algebraic chain term can vanish, but this does not remove active memory stress.",
        ),
        (
            "DEC1531_2_best_next",
            "Attack L_cg ownership next.",
            "NEXT_1532_LCG_PARENT_OWNERSHIP",
            "F_prime(m_*)=0 does not touch the L_cg response; a parent-fixed L_cg or F(m_*)=0 clause would remove the cleanest remaining algebraic chain term.",
        ),
        (
            "DEC1531_3_guardrail",
            "Do not claim delta_g S_Gamma=0 or a local-GR pass.",
            "CLAIM_BLOCKED",
            "hidden connection/domain/boundary kernels and background C remain open even after the algebraic chain is addressed.",
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


def local_status_rows() -> list[dict[str, Any]]:
    rows = [
        ("LOCAL1531_0_delta_g_SGamma", "delta_g S_Gamma", "REDUCED_NOT_BOUND", "kernel pack exact enough to audit, not exact enough to score"),
        ("LOCAL1531_1_M_m", "m-channel", "PARTIAL_CONDITIONAL_ROUTE", "fixed-independent scalar route exists but parent not signed"),
        ("LOCAL1531_2_M_L", "L_cg-channel", "PRIMARY_OPEN_ALGEBRAIC_BLOCKER", "L_cg ownership/metric silence undecided"),
        ("LOCAL1531_3_hidden", "hidden metric kernels", "OPEN", "connection/domain/boundary kernels retained"),
        ("LOCAL1531_4_lambda_phi", "lambda_phi multiplier stress", "BLOCKED", "requires delta_g S_Gamma zero or bound"),
        ("LOCAL1531_5_GR", "local GR/Newton/PPN", "NOT_CLAIMED", "q_loc residual branch still retained"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "status_id": status_id,
            "object": obj,
            "current_status": status,
            "reason": reason,
            **flags(),
        }
        for status_id, obj, status, reason in rows
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "next_id": "NEXT1531_0_1532",
            "next_target": "1532-Y5-Lcg-parent-ownership-and-fixed-scale-silence-audit.md",
            "script": "scripts/Y5_Lcg_parent_ownership_fixed_scale_silence_audit.py",
            "objective": "decide whether L_cg is parent-fixed, quotient-owned, or metric-composite; either prove M_L=0/F(m_*)=0 for the same branch or demote L_cg to a bounded retained kernel",
            "do_not": "do not use F_prime(m_*)=0 to erase the L_cg term; do not mix fixed-scale and metric-composite branches; do not promote local GR",
            **flags(),
        }
    ]


def copy_outputs() -> None:
    copies = [
        (KERNEL_AUDIT, QUAR_KERNEL_AUDIT),
        (BOUND_ENVELOPE, QUAR_ENVELOPE),
        (ZERO_ROUTE, QUAR_ZERO_ROUTE),
        (DECISION, QUAR_DECISION),
        (KERNEL_AUDIT, BRANCH_KERNEL_AUDIT),
        (BOUND_ENVELOPE, BRANCH_ENVELOPE),
        (ZERO_ROUTE, BRANCH_ZERO_ROUTE),
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
    audit = read_csv(KERNEL_AUDIT)
    envelope = read_csv(BOUND_ENVELOPE)
    zero_route = read_csv(ZERO_ROUTE)
    runners = read_csv(RUNNER)
    gates = read_csv(CLAIM_GATE)
    decisions = read_csv(DECISION)
    next_rows = read_csv(NEXT_TARGET)

    required_quantities = {
        "C_sign",
        "L_cg",
        "F(m)",
        "F_prime(m)",
        "M_m^{mu nu}",
        "M_L^{mu nu}",
        "K_conn^{mu nu}",
        "K_domain^{mu nu}",
        "K_boundary^{mu nu}",
        "K_C^{mu nu}=delta_g C",
        "operator norm and units",
    }
    audited_quantities = {row["quantity"] for row in audit}
    zero_statuses = {row["zero_id"]: row["status"] for row in zero_route}
    checks = [
        ("VAL1531_0_sources_exist", all(row["exists"] == "True" for row in sources), "all cited 1531 input source paths exist"),
        ("VAL1531_1_required_kernels_audited", required_quantities.issubset(audited_quantities), "all requested Kmetric kernel/norm slots audited"),
        ("VAL1531_2_M_m_partial_nonclaim", any(row["audit_id"] == "KNA1531_4_M_m" and row["status"] == "PARTIAL_CONDITIONAL_ZERO_NOT_LIVE" for row in audit), "M_m fixed-field route retained as partial nonclaim"),
        ("VAL1531_3_M_L_primary_blocker", any(row["audit_id"] == "KNA1531_5_M_L" and row["status"] == "MISSING_PARENT_OWNERSHIP" for row in audit), "M_L/L_cg ownership identified as primary algebraic blocker"),
        ("VAL1531_4_envelope_no_cancellation", any(row["envelope_id"] == "ENV1531_2_convention_guard" for row in envelope) and any(row["envelope_id"] == "ENV1531_5_hidden_kernel_guard" for row in envelope), "absolute/no-cancellation and hidden-kernel guards retained"),
        ("VAL1531_5_background_guard", any(row["envelope_id"] == "ENV1531_1_background_constant" for row in envelope), "delta_g C guard added to the envelope"),
        ("VAL1531_6_zero_route_not_proved", zero_statuses.get("ZERO1531_7_verdict") == "NOT_PROVED", "zero theorem remains explicitly unproved"),
        ("VAL1531_7_runners_blocked", all(row["result"].startswith("BLOCKED") for row in runners), "all score/claim runners remain blocked"),
        ("VAL1531_8_claim_gates_block", any(row["gate_id"] == "GATE1531_7_local_GR" and row["status"] == "BLOCKED_NO_CLAIM" for row in gates), "local GR claim remains blocked"),
        ("VAL1531_9_decision_next", any(row["result"] == "NEXT_1532_LCG_PARENT_OWNERSHIP" for row in decisions), "decision selects L_cg parent-ownership audit next"),
        ("VAL1531_10_next_target", any("1532-Y5-Lcg-parent-ownership" in row["next_target"] for row in next_rows), "next target is L_cg parent ownership/fixed-scale silence audit"),
        ("VAL1531_11_csv_parse", all(parse_csv(path) for path in generated_csvs), "all generated 1531 CSVs parse cleanly"),
        ("VAL1531_12_claim_flags_false", generated_flags_false(generated_csvs), "all generated prediction/claim flags remain false"),
        ("VAL1531_13_branch_copies", all(path.exists() for path in [QUAR_KERNEL_AUDIT, QUAR_ENVELOPE, QUAR_ZERO_ROUTE, QUAR_DECISION, BRANCH_KERNEL_AUDIT, BRANCH_ENVELOPE, BRANCH_ZERO_ROUTE, BRANCH_DECISION]), "branch/quarantine nonclaim copies written"),
        ("VAL1531_14_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent after run"),
        ("VAL1531_15_formalization_untouched", formalization_modified_count_since_start() == 0, "formalization modified-file count since start=0"),
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
            "check_id": "VAL1531_16_overall",
            "result": "PASS" if overall else "FAIL",
            "detail": "1531 audits the shared Kmetric kernel norm pack, records the partial M_m route, identifies L_cg ownership as the next target, and keeps all local-GR claims blocked"
            if overall
            else "1531 validation failed; inspect failed rows before continuing",
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
    audit: list[dict[str, Any]],
    envelope: list[dict[str, Any]],
    zero_route: list[dict[str, Any]],
    runners: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    local_rows: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 1531 - Delta g S_Gamma Kmetric Kernel Norm Source Pass",
                "",
                "## Verdict",
                "- The `delta_g S_Gamma` problem is now reduced to an explicit Kmetric-kernel pack, not a vague residual.",
                "- There is a real partial route for the `M_m` algebraic chain: if `m` is parent-owned as an independent scalar held fixed in Hilbert variation, that chain contribution can vanish.",
                "- That partial route is not a claim: metric-composite/readout branches and active memory stress remain open.",
                "- The cleanest next blocker is `L_cg` ownership: `F_prime(m_*)=0` does not erase the `M_L` term.",
                "- Hidden `K_conn`, `K_domain`, `K_boundary`, and background `delta_g C` terms remain retained; no local-GR/Newton/PPN claim is promoted.",
                "",
                "## Source Register",
                md_table(sources, ["source_id", "source_path", "exists", "purpose"]),
                "",
                "## Kmetric Kernel Norm Source Audit",
                md_table(audit, ["audit_id", "quantity", "role", "status", "finding", "missing_to_promote"]),
                "",
                "## Delta g S_Gamma Bound Envelope",
                md_table(envelope, ["envelope_id", "quantity", "formula_or_rule", "status", "reason"]),
                "",
                "## Zero Route Audit",
                md_table(zero_route, ["zero_id", "clause", "status", "reason"]),
                "",
                "## Kernel Norm Runner",
                md_table(runners, ["runner_id", "route", "required_inputs", "current_inputs", "result", "next_required_object"]),
                "",
                "## Claim Gates",
                md_table(gates, ["gate_id", "claim", "status", "reason"]),
                "",
                "## Decision",
                md_table(decisions, ["decision_id", "decision", "result", "rationale"]),
                "",
                "## Local GR / Newton Status",
                md_table(local_rows, ["status_id", "object", "current_status", "reason"]),
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
    audit = kernel_audit_rows()
    envelope = bound_envelope_rows()
    zero_route = zero_route_rows()
    runners = runner_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    local_rows = local_status_rows()
    next_rows = next_target_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(KERNEL_AUDIT, audit)
    write_csv(BOUND_ENVELOPE, envelope)
    write_csv(ZERO_ROUTE, zero_route)
    write_csv(RUNNER, runners)
    write_csv(CLAIM_GATE, gates)
    write_csv(DECISION, decisions)
    write_csv(LOCAL_STATUS, local_rows)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()
    remove_pycache()

    generated_csvs = [
        SOURCE_REGISTER,
        KERNEL_AUDIT,
        BOUND_ENVELOPE,
        ZERO_ROUTE,
        RUNNER,
        CLAIM_GATE,
        DECISION,
        LOCAL_STATUS,
        NEXT_TARGET,
    ]
    validation = validation_rows(generated_csvs)
    write_csv(VALIDATION, validation)
    write_doc(sources, audit, envelope, zero_route, runners, gates, decisions, local_rows, validation, next_rows)


if __name__ == "__main__":
    main()
