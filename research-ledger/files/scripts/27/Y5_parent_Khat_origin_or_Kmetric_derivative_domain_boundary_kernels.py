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
DOC = ROOT / "1525-Y5-parent-Khat-origin-or-Kmetric-derivative-domain-boundary-kernels.md"
START_TS = datetime.now(timezone.utc).timestamp()

SOURCE_FILES = {
    "1524_doc": ROOT / "1524-Y5-parent-Khat-DeltaK-scalar-channel-profile-or-Green-normalization.md",
    "1524_validation": OUT / "P8_Y5_BRR545_1524_VALIDATION.csv",
    "1524_profile": OUT / "P8_Y5_PARENT_QLOC_1524_KHAT_DELTAK_SCALAR_PROFILE.csv",
    "1524_claim_gate": OUT / "P8_Y5_PARENT_QLOC_1524_CLAIM_GATE.csv",
    "1524_next": OUT / "P8_Y5_PARENT_QLOC_1524_NEXT_TARGET.csv",
    "1287_khat": OUT / "P8_Y5_R10_1287_FIRST_KHAT_COMPONENT_ROW_NONCLAIM.csv",
    "1287_kmetric_volume": OUT / "P8_Y5_R10_1287_FIRST_KMETRIC_VOLUME_ROW_NONCLAIM.csv",
    "1287_deltak_status": OUT / "P8_Y5_R10_1287_DELTAK_COMPONENT_STATUS_LEDGER.csv",
    "1289_delta": OUT / "P8_Y5_R10_1289_DELTAK00_COMPARISON_TEMPLATE.csv",
    "1289_derivative": OUT / "P8_Y5_R10_1289_FIRST_DERIVATIVE_TERM_ROW_NONCLAIM.csv",
    "1289_variation": OUT / "P8_Y5_R10_1289_KMETRIC_VARIATION_EXPANSION_NONCLAIM.csv",
    "1289_hunt": OUT / "P8_Y5_R10_1289_RESPONSE_COEFFICIENT_HUNT_LEDGER.csv",
    "1289_claims": OUT / "P8_Y5_R10_1289_CLAIM_GATES.csv",
    "1288_blocker": OUT / "P8_Y5_R10_1288_KMETRIC_DERIVATIVE_TERM_BLOCKER.csv",
    "1367_kernel": OUT / "P8_Y5_R10_1367_KMETRIC_CHAIN_KERNEL_ATTEMPT.csv",
    "776_kgamma": OUT / "P8_Y5_R10_776_KGAMMA_METRIC_RESPONSE_LEDGER.csv",
    "798_gamma": OUT / "P8_Y5_R10_798_GAMMA_SOURCE_EXPANSION.csv",
    "1010_doc": ROOT / "1010-Y5-R10-Gamma-Khat-action-existence-Helmholtz-or-q_loc-residual-retention.md",
    "gk_candidates": OUT / "P8_GK_STRESS_ACTION_CANDIDATES.csv",
    "gk_gates": OUT / "P8_GK_STRESS_ACTION_GATE_TESTS.csv",
    "gk_decision": OUT / "P8_GK_STRESS_ACTION_DECISION.csv",
    "gk_evidence": OUT / "P8_GK_METRIC_RESPONSE_SOURCE_EVIDENCE.csv",
    "gk_contract": OUT / "P8_GK_METRIC_RESPONSE_CONTRACT.csv",
    "gamma_owner": OUT / "P8_GAMMA_OWNER_CANDIDATE_ACTION.csv",
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1525_SOURCE_REGISTER.csv"
KHAT_ORIGIN = OUT / "P8_Y5_PARENT_QLOC_1525_KHAT_ORIGIN_AUDIT.csv"
KMETRIC_KERNELS = OUT / "P8_Y5_PARENT_QLOC_1525_KMETRIC_KERNEL_REQUIREMENTS.csv"
DELTAK_RUNNER = OUT / "P8_Y5_PARENT_QLOC_1525_DELTAK_COMPUTABILITY_RUNNER.csv"
BOUND_ZERO = OUT / "P8_Y5_PARENT_QLOC_1525_BOUND_OR_ZERO_LEDGER.csv"
REJECTION_LEDGER = OUT / "P8_Y5_PARENT_QLOC_1525_REJECTION_LEDGER.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1525_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1525_DECISION.csv"
LOCAL_STATUS = OUT / "P8_Y5_PARENT_QLOC_1525_LOCAL_GR_NEWTON_STATUS.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1525_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1525_VALIDATION.csv"

QUARANTINE = MICROSCOPE / "quarantine" / "1525"
QUAR_ORIGIN = QUARANTINE / "KHAT_ORIGIN_AUDIT_NONCLAIM.csv"
QUAR_KERNELS = QUARANTINE / "KMETRIC_KERNEL_REQUIREMENTS_NONCLAIM.csv"
QUAR_RUNNER = QUARANTINE / "DELTAK_COMPUTABILITY_RUNNER_NONCLAIM.csv"
QUAR_DECISION = QUARANTINE / "DECISION_NONCLAIM.csv"
BRANCH_ORIGIN = BRANCH_RESIDUALS / "khat_origin_audit_nonclaim_1525.csv"
BRANCH_KERNELS = BRANCH_RESIDUALS / "kmetric_kernel_requirements_nonclaim_1525.csv"
BRANCH_RUNNER = BRANCH_RESIDUALS / "deltak_computability_runner_nonclaim_1525.csv"
BRANCH_DECISION = BRANCH_RESIDUALS / "khat_kmetric_decision_nonclaim_1525.csv"


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
            "source_id": f"SRC1525_{index}_{key}",
            "source_path": rel(path),
            "exists": path.exists(),
            "purpose": "input evidence for Khat parent-origin or Kmetric kernel computability gate",
            **flags(),
        }
        for index, (key, path) in enumerate(SOURCE_FILES.items())
    ]


def khat_origin_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "KOR1525_0_formal_candidate",
            "K_L^{mu nu}",
            "K_L^{mu nu}=2 nabla^mu nabla^nu phi - (1/2)g^{mu nu}Box phi with Box phi=(2/3)(Gamma_eff+C)",
            "FORMAL_CANDIDATE_EXISTS_NONCLAIM",
            "candidate row exists, but current MTS K_hat is not identified with it",
            source_list("1287_khat", "1289_delta"),
        ),
        (
            "KOR1525_1_tracefree_identity",
            "trace-free Hessian identity",
            "in four dimensions K_L^{mu nu}=2[nabla^mu nabla^nu phi-(1/4)g^{mu nu}Box phi], so g_{mu nu}K_L^{mu nu}=0",
            "ALGEBRAIC_IDENTITY_DERIVED",
            "this is algebra only; it does not prove parent ownership or the coefficient",
            source_list("1287_khat"),
        ),
        (
            "KOR1525_2_improvement_action_route",
            "curvature/improvement parent route",
            "a local scalar-curvature/improvement coupling can generate Hessian metric-response terms, whose trace-free projection has the K_L tensor shape",
            "BEST_PARENT_ORIGIN_ROUTE_CONDITIONAL",
            "needs explicit parent action, coefficient, sign convention, boundary term, and projection rule",
            source_list("gk_candidates", "gk_contract", "gk_evidence", "1010_doc"),
        ),
        (
            "KOR1525_3_current_symbol_match",
            "current MTS K_hat equals trace-free improvement response",
            "K_hat^{mu nu} ?= K_L^{mu nu} or K_hat^{mu nu} ?= K_metric^{TF mu nu}[phi R/improvement]",
            "MISSING_CURRENT_KHAT_MATCH",
            "no source row proves the live corpus K_hat tensor is this improvement response",
            source_list("gk_gates", "gk_decision", "1010_doc"),
        ),
        (
            "KOR1525_4_parent_signing_requirements",
            "birth-certificate checklist",
            "S_parent term; phi definition; variation variable; coefficient; volume convention; boundary convention; trace-free projection; source paths",
            "CHECKLIST_WRITTEN_NONCLAIM",
            "all checklist entries must be sourced before DeltaK can be zeroed or scored",
            source_list("gk_contract", "gamma_owner", "1289_variation"),
        ),
        (
            "KOR1525_5_verdict",
            "K_hat parent origin",
            "trace-free-improvement route is the least-scrutiny path, but not yet a proof",
            "NOT_PARENT_SIGNED",
            "K_hat remains retained; do not use K_L as live K_hat in PPN/local-GR scoring",
            source_list("1524_claim_gate", "1287_deltak_status"),
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "origin_id": origin_id,
            "object": obj,
            "formula_or_contract": formula,
            "status": status,
            "missing_to_promote": missing,
            "source_paths": sources,
            **flags(),
        }
        for origin_id, obj, formula, status, missing, sources in rows
    ]


def kmetric_kernel_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "KER1525_0_volume",
            "Kmetric_volume^{mu nu}",
            "delta sqrt(-g) Gamma_eff gives a metric-proportional volume piece, up to sign convention",
            "FORMAL_SUBPIECE_EXISTS_NONCLAIM",
            "sign/volume convention still not fixed",
            source_list("1287_kmetric_volume", "776_kgamma"),
        ),
        (
            "KER1525_1_m_response",
            "M_m^{mu nu}:=delta m/delta g_{mu nu}",
            "Kmetric_chain contains L_cg^-2 F_prime(m) M_m^{mu nu}",
            "MISSING_PARENT_RESPONSE_KERNEL",
            "m must be defined as a metric-dependent or metric-silent parent scalar with sourced variation",
            source_list("1289_derivative", "1289_variation", "1367_kernel"),
        ),
        (
            "KER1525_2_Lcg_response",
            "M_L^{mu nu}:=delta L_cg/delta g_{mu nu}",
            "Kmetric_chain contains -2 L_cg^-3 F(m) M_L^{mu nu}",
            "MISSING_PARENT_RESPONSE_KERNEL",
            "L_cg must be parent-fixed, metric-silent, or explicitly varied",
            source_list("1289_derivative", "1289_variation", "1367_kernel"),
        ),
        (
            "KER1525_3_connection_terms",
            "K_conn^{mu nu}",
            "metric response hidden in covariant derivatives, Christoffel symbols, Hodge/domain operators, and projector definitions",
            "MISSING_CONNECTION_KERNEL",
            "must be proven zero in local compact branch or bounded separately",
            source_list("776_kgamma", "1288_blocker", "1367_kernel"),
        ),
        (
            "KER1525_4_domain_terms",
            "K_domain^{mu nu}",
            "metric response of integration domain, averaging cells, local collar, and projection support",
            "MISSING_DOMAIN_KERNEL",
            "domain/cell variation must descend or be no-flux",
            source_list("776_kgamma", "1010_doc", "gk_evidence"),
        ),
        (
            "KER1525_5_boundary_terms",
            "K_boundary^{mu nu}",
            "boundary, reference subtraction, corner, and no-flux response terms",
            "MISSING_BOUNDARY_KERNEL",
            "must be source-backed zero or retained in S_total",
            source_list("776_kgamma", "1010_doc", "gk_contract"),
        ),
        (
            "KER1525_6_chain_zero_condition",
            "fixed-point chain silence",
            "F_prime(m_*)=0 removes m-kernel; M_L=0 or F(m_*)=0 removes L_cg response; K_conn=K_domain=K_boundary=0 removes hidden metric response",
            "CONDITIONAL_ZERO_NOT_PROVEN",
            "every zero clause is unsigned; no cancellation is allowed",
            source_list("1289_derivative", "798_gamma", "1367_kernel"),
        ),
        (
            "KER1525_7_verdict",
            "full Kmetric[Gamma_eff]",
            "Kmetric=volume+chain+connection+domain+boundary",
            "NOT_COMPUTABLE",
            "DeltaK cannot be computed until these kernels are zeroed, bounded, or explicitly sourced",
            source_list("1287_deltak_status", "1289_claims", "1524_profile"),
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "kernel_id": kernel_id,
            "kernel": kernel,
            "formula_or_requirement": formula,
            "status": status,
            "missing_to_promote": missing,
            "source_paths": sources,
            **flags(),
        }
        for kernel_id, kernel, formula, status, missing, sources in rows
    ]


def deltak_runner_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "DTR1525_0_zero_route",
            "route": "DeltaK_zero_if_Khat_equals_full_Kmetric",
            "required_inputs": "parent-signed K_hat=K_metric plus volume/chain/connection/domain/boundary kernels",
            "current_inputs": "formal K_L only; volume subpiece only; missing chain/domain/boundary kernels",
            "result": "BLOCKED_NOT_ZERO_PROVEN",
            "next_required_object": "trace-free improvement action coefficient or full Kmetric kernel table",
            "source_paths": source_list("1010_doc", "1524_profile", "1289_delta"),
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "DTR1525_1_compute_route",
            "route": "DeltaK_computable_if_Khat_and_Kmetric_components_are_live",
            "required_inputs": "K_hat^{mu nu}; Kmetric_volume; Kmetric_chain; K_conn; K_domain; K_boundary; sign and units",
            "current_inputs": "K_L template and Kmetric volume/chain formulas only",
            "result": "BLOCKED_NOT_COMPUTABLE",
            "next_required_object": "M_m, M_L, K_conn, K_domain, K_boundary, C_sign",
            "source_paths": source_list("1287_deltak_status", "1289_variation", "1367_kernel"),
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "DTR1525_2_score_route",
            "route": "PPN_q_loc_score_after_DeltaK",
            "required_inputs": "S_Delta(r), S_total, C_op, Q_loc, GM, PPN map",
            "current_inputs": "none live enough for scoring",
            "result": "BLOCKED_NO_LOCAL_GR_CLAIM",
            "next_required_object": "after DeltaK gate, return to q_loc_hat normalization",
            "source_paths": source_list("1524_doc", "1524_claim_gate"),
            **flags(),
        },
    ]


def bound_zero_rows() -> list[dict[str, Any]]:
    rows = [
        ("BZ1525_0_Khat_zero", "K_hat-Kmetric", "zero theorem", "requires parent-signed same metric response", "MISSING_PARENT_SIGNED_IDENTITY"),
        ("BZ1525_1_m_kernel_zero", "M_m channel", "fixed point zero", "requires F_prime(m_*)=0 and sourced m response", "UNSIGNED"),
        ("BZ1525_2_Lcg_kernel_zero", "L_cg channel", "metric silence or F(m_*)=0", "requires M_L=0 or F(m_*)=0 with source path", "UNSIGNED"),
        ("BZ1525_3_connection_zero", "connection/domain/projector channel", "geometric silence", "requires local collar/projector descent proof", "UNSIGNED"),
        ("BZ1525_4_boundary_zero", "boundary/reference/corner channel", "no-flux theorem", "requires boundary term and reference subtraction proof", "UNSIGNED"),
        ("BZ1525_5_bound_fallback", "retained DeltaK", "independent bound", "requires norm bound on each retained kernel before q_loc scoring", "MISSING_BOUND"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "bound_id": bound_id,
            "channel": channel,
            "route": route,
            "requirement": requirement,
            "status": status,
            "source_paths": source_list("1010_doc", "1289_claims", "1524_claim_gate"),
            **flags(),
        }
        for bound_id, channel, route, requirement, status in rows
    ]


def rejection_rows() -> list[dict[str, Any]]:
    rows = [
        ("REJ1525_0_tracefree_identity_as_proof", "treat trace-free Hessian identity as parent proof", "REJECTED", "algebraic tensor identity does not establish parent action or current-symbol match"),
        ("REJ1525_1_phiR_without_coefficient", "declare improvement action without coefficient/sign", "REJECTED", "wrong coefficient or boundary convention changes DeltaK and q_loc"),
        ("REJ1525_2_volume_only_Kmetric", "compute DeltaK from volume term only", "REJECTED", "chain, connection, domain, and boundary kernels are retained"),
        ("REJ1525_3_fixed_point_cancellation", "assume missing kernels cancel each other", "REJECTED", "1524 forbids cancellation without independent zero/bounds"),
        ("REJ1525_4_score_PPN_now", "use K_L template to score Cassini/local GR", "REJECTED", "K_hat and q_loc_hat are not live"),
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


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("GATE1525_0_tracefree_identity", "K_L trace-free Hessian identity is algebraically written", "PASS_NONCLAIM", "identity sharpens the parent-action search"),
        ("GATE1525_1_parent_Khat", "K_hat is parent-signed current MTS tensor", "BLOCKED", "improvement action coefficient/current-symbol match missing"),
        ("GATE1525_2_full_Kmetric", "full Kmetric is computable", "BLOCKED", "M_m, M_L, connection, domain, boundary, sign kernels missing"),
        ("GATE1525_3_DeltaK", "DeltaK is zero or computable", "BLOCKED", "neither zero theorem nor full component table exists"),
        ("GATE1525_4_qloch", "q_loc_hat can be normalized", "BLOCKED", "DeltaK/S_total/C_op still missing"),
        ("GATE1525_5_local_GR", "local GR/Newton/PPN recovery is claimable", "BLOCKED_NO_CLAIM", "local branch remains nonclaim"),
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
            "DEC1525_0_best_route",
            "Pursue the trace-free Hessian/improvement-action route before grinding every Kmetric kernel.",
            "BEST_ROUTE_TRACEFREE_IMPROVEMENT",
            "it can parent-sign K_hat in one move if coefficient, sign, boundary, and current-symbol match close.",
        ),
        (
            "DEC1525_1_kernel_fallback",
            "Keep the full kernel table as the fallback if improvement action cannot be sourced.",
            "FALLBACK_FULL_KMETRIC_KERNEL_TABLE",
            "this prevents hidden cancellation and gives independent bound targets.",
        ),
        (
            "DEC1525_2_claim_status",
            "No local-GR/PPN/q_loc claim is promoted from 1525.",
            "CLAIM_BLOCKED_NONCLAIM",
            "trace-free identity is progress, not a parent proof.",
        ),
        (
            "DEC1525_3_next",
            "Next target is trace-free Hessian improvement action coefficient and current-symbol match.",
            "NEXT_1526_IMPROVEMENT_ACTION_GATE",
            "this is the shortest derivation path to live K_hat; if it fails, return to M_m/M_L/kernel bounds.",
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
        ("LOCAL1525_0_Khat_shape", "K_L tensor shape", "SHARPENED_NONCLAIM", "identified as four-dimensional trace-free Hessian"),
        ("LOCAL1525_1_Khat_origin", "parent origin", "NOT_PARENT_SIGNED", "improvement-action route conditional only"),
        ("LOCAL1525_2_Kmetric", "full Kmetric", "NOT_COMPUTABLE", "kernel table has named missing pieces"),
        ("LOCAL1525_3_DeltaK", "DeltaK scalar source", "NOT_ZERO_OR_COMPUTABLE", "zero theorem and compute route both blocked"),
        ("LOCAL1525_4_GR", "derived local GR/Newton", "NOT_CLAIMED", "q_loc_hat normalization remains downstream"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "status_id": status_id,
            "claim": claim,
            "current_status": status,
            "reason": reason,
            **flags(),
        }
        for status_id, claim, status, reason in rows
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "next_id": "NEXT1525_0_1526",
            "next_target": "1526-Y5-tracefree-Hessian-improvement-action-coefficient-and-symbol-match.md",
            "script": "scripts/Y5_tracefree_Hessian_improvement_action_coefficient_and_symbol_match.py",
            "objective": "derive or reject the parent action whose trace-free metric response gives K_L, including coefficient, sign, boundary convention, phi=(2/3)(Gamma_eff+C), and current MTS K_hat symbol match",
            "do_not": "do not treat the trace-free identity alone as proof; do not score PPN/local GR; do not drop Kmetric kernels unless the parent identity closes",
            **flags(),
        }
    ]


def copy_outputs() -> None:
    copies = [
        (KHAT_ORIGIN, QUAR_ORIGIN),
        (KMETRIC_KERNELS, QUAR_KERNELS),
        (DELTAK_RUNNER, QUAR_RUNNER),
        (DECISION, QUAR_DECISION),
        (KHAT_ORIGIN, BRANCH_ORIGIN),
        (KMETRIC_KERNELS, BRANCH_KERNELS),
        (DELTAK_RUNNER, BRANCH_RUNNER),
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
    origins = read_csv(KHAT_ORIGIN)
    kernels = read_csv(KMETRIC_KERNELS)
    runners = read_csv(DELTAK_RUNNER)
    bounds = read_csv(BOUND_ZERO)
    rejections = read_csv(REJECTION_LEDGER)
    gates = read_csv(CLAIM_GATE)
    decisions = read_csv(DECISION)
    next_rows = read_csv(NEXT_TARGET)

    checks = [
        ("VAL1525_0_sources_exist", all(row["exists"] == "True" for row in sources), "all cited 1525 input source paths exist"),
        ("VAL1525_1_tracefree_identity", any(row["origin_id"] == "KOR1525_1_tracefree_identity" and row["status"] == "ALGEBRAIC_IDENTITY_DERIVED" for row in origins), "K_L trace-free Hessian identity is written"),
        ("VAL1525_2_parent_not_signed", any(row["origin_id"] == "KOR1525_5_verdict" and row["status"] == "NOT_PARENT_SIGNED" for row in origins), "Khat parent origin remains nonclaim"),
        ("VAL1525_3_kernel_table_complete", len(kernels) >= 8 and any(row["kernel_id"] == "KER1525_7_verdict" and row["status"] == "NOT_COMPUTABLE" for row in kernels), "Kmetric kernel table names missing pieces"),
        ("VAL1525_4_DeltaK_runner_blocked", all(row["result"].startswith("BLOCKED") for row in runners), "DeltaK zero/compute/score routes remain blocked"),
        ("VAL1525_5_bound_zero_unsigned", len(bounds) >= 6 and all(row["status"] != "SIGNED" for row in bounds), "zero/bound ledger has no signed shortcut"),
        ("VAL1525_6_rejections_guardrails", len(rejections) >= 5 and all(row["status"] == "REJECTED" for row in rejections), "shortcuts rejected"),
        ("VAL1525_7_claim_gates_block", any(row["gate_id"] == "GATE1525_5_local_GR" and row["status"] == "BLOCKED_NO_CLAIM" for row in gates), "local GR claim remains blocked"),
        ("VAL1525_8_decision_next", any(row["result"] == "NEXT_1526_IMPROVEMENT_ACTION_GATE" for row in decisions), "decision selects trace-free improvement action gate next"),
        ("VAL1525_9_next_target", any("1526-Y5-tracefree-Hessian" in row["next_target"] for row in next_rows), "next target is 1526 trace-free Hessian improvement gate"),
        ("VAL1525_10_csv_parse", all(parse_csv(path) for path in generated_csvs), "all generated 1525 CSVs parse cleanly"),
        ("VAL1525_11_claim_flags_false", generated_flags_false(generated_csvs), "all generated prediction/claim flags remain false"),
        ("VAL1525_12_branch_copies", all(path.exists() for path in [QUAR_ORIGIN, QUAR_KERNELS, QUAR_RUNNER, QUAR_DECISION, BRANCH_ORIGIN, BRANCH_KERNELS, BRANCH_RUNNER, BRANCH_DECISION]), "branch/quarantine nonclaim copies written"),
        ("VAL1525_13_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent after run"),
        ("VAL1525_14_formalization_untouched", formalization_modified_count_since_start() == 0, "formalization modified-file count since start=0"),
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
            "check_id": "VAL1525_15_overall",
            "result": "PASS" if overall else "FAIL",
            "detail": "1525 sharpens K_L as trace-free Hessian, keeps Khat/Kmetric nonclaim, and selects the improvement-action coefficient gate next"
            if overall
            else "1525 validation failed; inspect failed rows before continuing",
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
    origins: list[dict[str, Any]],
    kernels: list[dict[str, Any]],
    runners: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    rejections: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    local_rows: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 1525 - Parent Khat Origin or Kmetric Derivative/Domain/Boundary Kernels",
                "",
                "## Verdict",
                "- The `K_L` candidate has been sharpened: in four dimensions it is exactly a trace-free Hessian, `K_L^{mu nu}=2[nabla^mu nabla^nu phi-(1/4)g^{mu nu}Box phi]`.",
                "- That makes the least-scrutiny route a parent curvature/improvement action whose trace-free metric response supplies the live `K_hat`.",
                "- This is progress, not a claim: the coefficient, sign, boundary convention, `phi=(2/3)(Gamma_eff+C)` ownership, and current MTS `K_hat` symbol match are still missing.",
                "- The fallback route is now explicit too: compute or zero `M_m`, `M_L`, `K_conn`, `K_domain`, `K_boundary`, and the sign/volume convention before `DeltaK` can be used.",
                "- No local-GR/Newton/PPN claim is promoted from 1525.",
                "",
                "## Source Register",
                md_table(sources, ["source_id", "source_path", "exists", "purpose"]),
                "",
                "## Khat Origin Audit",
                md_table(origins, ["origin_id", "object", "formula_or_contract", "status", "missing_to_promote"]),
                "",
                "## Kmetric Kernel Requirements",
                md_table(kernels, ["kernel_id", "kernel", "formula_or_requirement", "status", "missing_to_promote"]),
                "",
                "## DeltaK Computability Runner",
                md_table(runners, ["runner_id", "route", "required_inputs", "current_inputs", "result", "next_required_object"]),
                "",
                "## Bound Or Zero Ledger",
                md_table(bounds, ["bound_id", "channel", "route", "requirement", "status"]),
                "",
                "## Rejection Ledger",
                md_table(rejections, ["rejection_id", "shortcut", "status", "reason"]),
                "",
                "## Claim Gates",
                md_table(gates, ["gate_id", "claim", "status", "reason"]),
                "",
                "## Decision",
                md_table(decisions, ["decision_id", "decision", "result", "rationale"]),
                "",
                "## Local GR / Newton Status",
                md_table(local_rows, ["status_id", "claim", "current_status", "reason"]),
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
    origins = khat_origin_rows()
    kernels = kmetric_kernel_rows()
    runners = deltak_runner_rows()
    bounds = bound_zero_rows()
    rejections = rejection_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    local_rows = local_status_rows()
    next_rows = next_target_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(KHAT_ORIGIN, origins)
    write_csv(KMETRIC_KERNELS, kernels)
    write_csv(DELTAK_RUNNER, runners)
    write_csv(BOUND_ZERO, bounds)
    write_csv(REJECTION_LEDGER, rejections)
    write_csv(CLAIM_GATE, gates)
    write_csv(DECISION, decisions)
    write_csv(LOCAL_STATUS, local_rows)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()
    remove_pycache()

    generated_csvs = [
        SOURCE_REGISTER,
        KHAT_ORIGIN,
        KMETRIC_KERNELS,
        DELTAK_RUNNER,
        BOUND_ZERO,
        REJECTION_LEDGER,
        CLAIM_GATE,
        DECISION,
        LOCAL_STATUS,
        NEXT_TARGET,
    ]
    validation = validation_rows(generated_csvs)
    write_csv(VALIDATION, validation)
    write_doc(sources, origins, kernels, runners, bounds, rejections, gates, decisions, local_rows, validation, next_rows)


if __name__ == "__main__":
    main()
