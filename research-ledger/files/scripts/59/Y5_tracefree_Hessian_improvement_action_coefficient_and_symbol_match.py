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
DOC = ROOT / "1526-Y5-tracefree-Hessian-improvement-action-coefficient-and-symbol-match.md"
START_TS = datetime.now(timezone.utc).timestamp()

SOURCE_FILES = {
    "route_contract": ROOT / "01-motion-load-route-contract.md",
    "local_gr_reduction": ROOT / "02-motion-load-local-GR-reduction.md",
    "1010_doc": ROOT / "1010-Y5-R10-Gamma-Khat-action-existence-Helmholtz-or-q_loc-residual-retention.md",
    "1525_doc": ROOT / "1525-Y5-parent-Khat-origin-or-Kmetric-derivative-domain-boundary-kernels.md",
    "1525_validation": OUT / "P8_Y5_BRR545_1525_VALIDATION.csv",
    "1525_origin": OUT / "P8_Y5_PARENT_QLOC_1525_KHAT_ORIGIN_AUDIT.csv",
    "1525_claim_gate": OUT / "P8_Y5_PARENT_QLOC_1525_CLAIM_GATE.csv",
    "1525_next": OUT / "P8_Y5_PARENT_QLOC_1525_NEXT_TARGET.csv",
    "1287_khat": OUT / "P8_Y5_R10_1287_FIRST_KHAT_COMPONENT_ROW_NONCLAIM.csv",
    "1287_deltak": OUT / "P8_Y5_R10_1287_DELTAK_COMPONENT_STATUS_LEDGER.csv",
    "1289_delta": OUT / "P8_Y5_R10_1289_DELTAK00_COMPARISON_TEMPLATE.csv",
    "1289_variation": OUT / "P8_Y5_R10_1289_KMETRIC_VARIATION_EXPANSION_NONCLAIM.csv",
    "1525_kernels": OUT / "P8_Y5_PARENT_QLOC_1525_KMETRIC_KERNEL_REQUIREMENTS.csv",
    "gk_contract": OUT / "P8_GK_METRIC_RESPONSE_CONTRACT.csv",
    "gk_evidence": OUT / "P8_GK_METRIC_RESPONSE_SOURCE_EVIDENCE.csv",
    "gk_candidates": OUT / "P8_GK_STRESS_ACTION_CANDIDATES.csv",
    "gk_gates": OUT / "P8_GK_STRESS_ACTION_GATE_TESTS.csv",
    "gk_decision": OUT / "P8_GK_STRESS_ACTION_DECISION.csv",
    "first_variation_contract": OUT / "P8_GAMMA_KHAT_QLOC_FIRST_VARIATION_CONTRACT.csv",
    "gamma_owner": OUT / "P8_GAMMA_OWNER_CANDIDATE_ACTION.csv",
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1526_SOURCE_REGISTER.csv"
VARIATION_DERIVATION = OUT / "P8_Y5_PARENT_QLOC_1526_VARIATION_DERIVATION.csv"
COEFFICIENT_CONTRACT = OUT / "P8_Y5_PARENT_QLOC_1526_COEFFICIENT_SIGN_CONTRACT.csv"
SYMBOL_MATCH = OUT / "P8_Y5_PARENT_QLOC_1526_SYMBOL_MATCH_AUDIT.csv"
DELTAK_OUTCOME = OUT / "P8_Y5_PARENT_QLOC_1526_DELTAK_OUTCOME_RUNNER.csv"
KERNEL_FALLBACK = OUT / "P8_Y5_PARENT_QLOC_1526_RETAINED_KERNEL_FALLBACK.csv"
REJECTION_LEDGER = OUT / "P8_Y5_PARENT_QLOC_1526_REJECTION_LEDGER.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1526_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1526_DECISION.csv"
LOCAL_STATUS = OUT / "P8_Y5_PARENT_QLOC_1526_LOCAL_GR_NEWTON_STATUS.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1526_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1526_VALIDATION.csv"

QUARANTINE = MICROSCOPE / "quarantine" / "1526"
QUAR_VARIATION = QUARANTINE / "VARIATION_DERIVATION_NONCLAIM.csv"
QUAR_CONTRACT = QUARANTINE / "COEFFICIENT_SIGN_CONTRACT_NONCLAIM.csv"
QUAR_SYMBOL = QUARANTINE / "SYMBOL_MATCH_AUDIT_NONCLAIM.csv"
QUAR_DECISION = QUARANTINE / "DECISION_NONCLAIM.csv"
BRANCH_VARIATION = BRANCH_RESIDUALS / "tracefree_hessian_variation_derivation_nonclaim_1526.csv"
BRANCH_CONTRACT = BRANCH_RESIDUALS / "improvement_action_coefficient_contract_nonclaim_1526.csv"
BRANCH_SYMBOL = BRANCH_RESIDUALS / "khat_symbol_match_audit_nonclaim_1526.csv"
BRANCH_DECISION = BRANCH_RESIDUALS / "improvement_action_decision_nonclaim_1526.csv"


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
            "source_id": f"SRC1526_{index}_{key}",
            "source_path": rel(path),
            "exists": path.exists(),
            "purpose": "input evidence for trace-free Hessian improvement-action coefficient and Khat symbol-match gate",
            **flags(),
        }
        for index, (key, path) in enumerate(SOURCE_FILES.items())
    ]


def variation_derivation_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "VAR1526_0_parent_action_candidate",
            "scalar-curvature improvement term",
            "S_I[c_I]=c_I int sqrt(-g) phi R plus the boundary term required by the chosen variational problem",
            "PARENT_ACTION_SHAPE_WRITTEN",
            "coefficient, boundary term, and phi owner are not sourced in current MTS symbols",
            source_list("1525_origin", "gk_candidates", "gk_contract"),
        ),
        (
            "VAR1526_1_standard_variation_identity",
            "first metric variation",
            "delta[sqrt(-g)phi R]/delta g^{mu nu}=sqrt(-g)[phi G_{mu nu}+(g_{mu nu}Box-nabla_mu nabla_nu)phi] up to boundary",
            "VARIATION_IDENTITY_WRITTEN",
            "sign depends on whether K/T is defined using delta/delta g^{mu nu} or delta/delta g_{mu nu}",
            source_list("gk_contract", "first_variation_contract"),
        ),
        (
            "VAR1526_2_ricci_flat_derivative_response",
            "local Ricci-flat derivative part",
            "with phi G^{mu nu} routed to the metric/EH channel or zero in the Ricci-flat branch, the derivative response is proportional to 2(nabla^mu nabla^nu phi-g^{mu nu}Box phi)",
            "CONDITIONAL_DERIVATIVE_RESPONSE",
            "needs Ricci-flat/local branch condition and channel-routing guard",
            source_list("1525_doc", "1010_doc"),
        ),
        (
            "VAR1526_3_tracefree_projection",
            "trace-free projection in four dimensions",
            "TF[2(nabla^mu nabla^nu phi-g^{mu nu}Box phi)]=2nabla^mu nabla^nu phi-(1/2)g^{mu nu}Box phi=K_L^{mu nu}",
            "EXACT_TRACEFREE_MATCH_DERIVED",
            "exact algebra under 4D trace-free projection; still not a current-symbol proof",
            source_list("1525_origin", "1287_khat"),
        ),
        (
            "VAR1526_4_phi_equation_guard",
            "phi owner",
            "source row gives Box phi=(2/3)(Gamma_eff+C); parent theory must make phi an auxiliary constrained field or accept a nonlocal inverse-Box definition",
            "PHI_OWNER_MISSING",
            "without a local phi constraint/action, the route may be nonlocal rather than field-theoretic",
            source_list("1287_khat", "gamma_owner"),
        ),
        (
            "VAR1526_5_verdict",
            "improvement derivation",
            "the trace-free metric response of phi R can produce the K_L tensor shape exactly up to coefficient/sign/current-symbol clauses",
            "DERIVED_CONDITIONAL_NOT_PROMOTED",
            "coefficient, sign, boundary, phi owner, and live K_hat match remain unsigned",
            source_list("1525_claim_gate", "gk_gates"),
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "variation_id": variation_id,
            "object": obj,
            "formula_or_statement": formula,
            "status": status,
            "missing_to_promote": missing,
            "source_paths": sources,
            **flags(),
        }
        for variation_id, obj, formula, status, missing, sources in rows
    ]


def coefficient_contract_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "SIG1526_0_response_sign",
            "sigma_resp",
            "define sigma_resp=+1 if the chosen K_hat convention uses the trace-free part of +2/sqrt(-g) delta S_I/delta g^{mu nu}; otherwise sigma_resp=-1 after lowering/raising convention",
            "SIGN_CONVENTION_REQUIRED",
            "current source rows require a fixed sign but do not provide it",
        ),
        (
            "SIG1526_1_coefficient_law",
            "c_I",
            "matching K_hat=K_L requires sigma_resp*c_I=1 in the local trace-free derivative channel",
            "COEFFICIENT_MATCH_LAW_DERIVED",
            "this is a contract, not a sourced value",
        ),
        (
            "SIG1526_2_boundary_term",
            "B_I[phi,g]",
            "a scalar-curvature improvement action needs a compatible boundary term/reference subtraction so the bulk variation above is the whole local response",
            "BOUNDARY_CONVENTION_MISSING",
            "uncancelled boundary response must stay in S_total",
        ),
        (
            "SIG1526_3_curvature_channel",
            "phi G^{mu nu}",
            "outside the Ricci-flat/local-GR limit the phi G^{mu nu} part is a metric-channel term, not part of K_L unless explicitly projected/routed",
            "CURVATURE_ROUTING_REQUIRED",
            "prevents hiding genuine GR curvature in the memory scalar",
        ),
        (
            "SIG1526_4_phi_locality",
            "Box phi=(2/3)(Gamma_eff+C)",
            "either add a local auxiliary constraint for phi or mark the route as nonlocal inverse-Box; no local field-theory claim without this",
            "LOCALITY_CLAUSE_MISSING",
            "parent action remains incomplete",
        ),
        (
            "SIG1526_5_verdict",
            "coefficient/sign contract",
            "sigma_resp*c_I=1 plus boundary, curvature-routing, and phi-locality clauses would parent-sign the K_L shape",
            "CONTRACT_READY_NOT_SOURCED",
            "needs current MTS adoption/source rows",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "contract_id": contract_id,
            "quantity": quantity,
            "contract_or_formula": formula,
            "status": status,
            "missing_to_promote": missing,
            "source_paths": source_list("gk_contract", "1525_origin", "1289_variation"),
            **flags(),
        }
        for contract_id, quantity, formula, status, missing in rows
    ]


def symbol_match_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "SYM1526_0_symbol_occurrence",
            "Gamma_eff/K_hat/q_loc symbols",
            "route docs list Gamma_eff, K_hat, and q_loc as local-GR branch objects",
            "SYMBOLS_PRESENT",
            "presence is not a tensor definition",
            source_list("route_contract", "local_gr_reduction"),
        ),
        (
            "SYM1526_1_metric_response_contract",
            "K_hat metric-response requirement",
            "existing contract requires K_hat to be exactly the metric response of Gamma_eff including derivative and boundary terms",
            "REQUIREMENT_PRESENT",
            "requirement is not yet satisfied for current symbols",
            source_list("gk_contract", "gk_evidence"),
        ),
        (
            "SYM1526_2_tracefree_candidate_match",
            "K_L shape match",
            "formal K_L candidate matches the trace-free improvement response shape",
            "SHAPE_MATCH_ONLY",
            "shape match lacks phi owner, coefficient, sign, and live K_hat adoption",
            source_list("1287_khat", "1525_origin"),
        ),
        (
            "SYM1526_3_current_MTS_match",
            "current MTS K_hat equals improvement response",
            "K_hat^{mu nu} := TF metric response of c_I int sqrt(-g) phi R with sigma_resp*c_I=1",
            "MISSING_ADOPTION_OR_SOURCE_ROW",
            "no current file makes this definition live",
            source_list("gk_gates", "gk_decision", "1010_doc"),
        ),
        (
            "SYM1526_4_deltaK_zero_condition",
            "DeltaK Khat side",
            "if SYM1526_3 plus full Kmetric ownership closes, the trace-free Khat-origin part of DeltaK can be zeroed",
            "CONDITIONAL_ONLY",
            "full Kmetric and retained kernel fallback still required",
            source_list("1525_kernels", "1287_deltak"),
        ),
        (
            "SYM1526_5_verdict",
            "symbol match",
            "current corpus supports a strong candidate route, but not a live current-symbol match",
            "NOT_MATCHED",
            "do not promote K_L as K_hat in local tests",
            source_list("1525_claim_gate", "1525_validation"),
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "match_id": match_id,
            "object": obj,
            "evidence_or_contract": evidence,
            "status": status,
            "missing_to_promote": missing,
            "source_paths": sources,
            **flags(),
        }
        for match_id, obj, evidence, status, missing, sources in rows
    ]


def deltak_outcome_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "OUT1526_0_if_all_signed",
            "best-case outcome",
            "if phi owner, sigma_resp*c_I=1, boundary convention, curvature routing, and live K_hat match all close, K_L is parent-owned as the trace-free improvement response",
            "CONDITIONAL_SUCCESS_PATH",
            "would reduce the Khat-origin obstruction, not yet full q_loc scoring",
        ),
        (
            "OUT1526_1_current_status",
            "current outcome",
            "exact K_L shape derived, but parent/locality/sign/symbol clauses remain unsigned",
            "BLOCKED_NOT_PROMOTED",
            "DeltaK remains retained",
        ),
        (
            "OUT1526_2_kernel_fallback",
            "fallback outcome",
            "if current-symbol adoption fails, return to M_m, M_L, K_conn, K_domain, K_boundary bounds",
            "FALLBACK_ACTIVE",
            "no cancellation allowed",
        ),
        (
            "OUT1526_3_q_loc_status",
            "q_loc/local PPN",
            "no q_loc_hat, C_op, S_total, or Cassini/PPN scoring follows from 1526",
            "BLOCKED_NO_LOCAL_GR_CLAIM",
            "keep this private/nonclaim",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "outcome_id": outcome_id,
            "branch": branch,
            "statement": statement,
            "status": status,
            "reason": reason,
            "source_paths": source_list("1525_claim_gate", "1525_kernels", "1289_delta"),
            **flags(),
        }
        for outcome_id, branch, statement, status, reason in rows
    ]


def kernel_fallback_rows() -> list[dict[str, Any]]:
    rows = [
        ("KF1526_0_M_m", "M_m^{mu nu}", "needed if Khat adoption fails or if phi owner couples through m", "MISSING_PARENT_RESPONSE_KERNEL"),
        ("KF1526_1_M_L", "M_L^{mu nu}", "needed for L_cg metric response in Gamma_eff", "MISSING_PARENT_RESPONSE_KERNEL"),
        ("KF1526_2_K_conn", "K_conn^{mu nu}", "needed for covariant derivative/Hodge/projector metric response", "MISSING_CONNECTION_KERNEL"),
        ("KF1526_3_K_domain", "K_domain^{mu nu}", "needed for cell/domain/support variation", "MISSING_DOMAIN_KERNEL"),
        ("KF1526_4_K_boundary", "K_boundary^{mu nu}", "needed for boundary/reference/corner response", "MISSING_BOUNDARY_KERNEL"),
        ("KF1526_5_bound_route", "retained DeltaK bound", "needed before any local test if zero route fails", "MISSING_NUMERIC_OR_THEOREM_BOUND"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "fallback_id": fallback_id,
            "object": obj,
            "why_needed": why_needed,
            "status": status,
            "source_paths": source_list("1525_kernels", "1289_variation"),
            **flags(),
        }
        for fallback_id, obj, why_needed, status in rows
    ]


def rejection_rows() -> list[dict[str, Any]]:
    rows = [
        ("REJ1526_0_shape_equals_parent", "declare K_L parent-owned from trace-free shape alone", "REJECTED", "shape equality is not an action/sign/current-symbol proof"),
        ("REJ1526_1_ignore_phi_owner", "use Box phi relation without local phi action or constraint", "REJECTED", "inverse-Box/nonlocality would break the field-theory claim unless explicitly owned"),
        ("REJ1526_2_drop_boundary", "ignore scalar-curvature boundary/reference terms", "REJECTED", "boundary variation can re-enter S_total/q_loc"),
        ("REJ1526_3_hide_phiG", "absorb phi G^{mu nu} into K_L without routing", "REJECTED", "curvature channel must route to metric/EH side or be retained"),
        ("REJ1526_4_score_local_tests", "score PPN/Cassini from the improvement identity", "REJECTED", "q_loc_hat and DeltaK remain blocked"),
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
        ("GATE1526_0_variation_identity", "phi R trace-free variation produces K_L shape", "PASS_CONDITIONAL", "exact trace-free identity is derived under stated conventions"),
        ("GATE1526_1_coefficient", "coefficient/sign are fixed", "BLOCKED", "sigma_resp*c_I=1 is a contract, not sourced current convention"),
        ("GATE1526_2_phi_owner", "phi is locally parent-owned", "BLOCKED", "Box phi relation needs auxiliary constraint or nonlocal branch declaration"),
        ("GATE1526_3_current_Khat", "current MTS K_hat equals this response", "BLOCKED", "no adoption/source row"),
        ("GATE1526_4_full_DeltaK", "DeltaK can be zeroed or computed", "BLOCKED", "Kmetric fallback kernels remain"),
        ("GATE1526_5_local_GR", "local GR/Newton/PPN recovery is claimable", "BLOCKED_NO_CLAIM", "q_loc local branch remains nonclaim"),
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
            "DEC1526_0_math_result",
            "Accept the trace-free phi R improvement identity as a real conditional derivation.",
            "DERIVATION_GAIN",
            "the K_L tensor shape is no longer mysterious; it is the trace-free derivative response of a scalar-curvature improvement term.",
        ),
        (
            "DEC1526_1_not_promoted",
            "Do not promote K_L to live K_hat yet.",
            "CLAIM_BLOCKED",
            "phi owner, sign/coefficient, boundary, curvature routing, and symbol match are unsigned.",
        ),
        (
            "DEC1526_2_new_bottleneck",
            "The next bottleneck is phi ownership plus current K_hat adoption/source.",
            "NEXT_PHI_OWNER_AND_SYMBOL_MATCH",
            "without that, the route risks being nonlocal or merely a candidate tensor.",
        ),
        (
            "DEC1526_3_fallback",
            "Keep the full Kmetric kernel fallback active.",
            "FALLBACK_RETAINED",
            "if adoption fails, the theory must bound/compute M_m, M_L, K_conn, K_domain, and K_boundary.",
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
        ("LOCAL1526_0_KL_origin", "K_L origin", "DERIVED_CONDITIONAL", "trace-free phi R response gives exact K_L shape"),
        ("LOCAL1526_1_phi", "phi owner/locality", "BLOCKED", "needs auxiliary constraint or explicit nonlocal branch"),
        ("LOCAL1526_2_Khat", "current K_hat", "NOT_MATCHED", "no live source/adoption row"),
        ("LOCAL1526_3_DeltaK", "DeltaK", "NOT_ZERO_OR_COMPUTABLE", "kernel fallback remains active"),
        ("LOCAL1526_4_GR", "derived local GR/Newton", "NOT_CLAIMED", "no q_loc_hat normalization or PPN score"),
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
            "next_id": "NEXT1526_0_1527",
            "next_target": "1527-Y5-phi-owner-and-current-Khat-symbol-match-source-hunt.md",
            "script": "scripts/Y5_phi_owner_and_current_Khat_symbol_match_source_hunt.py",
            "objective": "hunt or construct the parent-owned phi sector and current MTS K_hat adoption row: auxiliary constraint versus nonlocal inverse-Box, sigma_resp*c_I=1, boundary term, curvature routing, and source paths",
            "do_not": "do not promote K_L as live K_hat; do not hide inverse-Box nonlocality; do not score local GR/PPN; do not edit formalization-workbench",
            **flags(),
        }
    ]


def copy_outputs() -> None:
    copies = [
        (VARIATION_DERIVATION, QUAR_VARIATION),
        (COEFFICIENT_CONTRACT, QUAR_CONTRACT),
        (SYMBOL_MATCH, QUAR_SYMBOL),
        (DECISION, QUAR_DECISION),
        (VARIATION_DERIVATION, BRANCH_VARIATION),
        (COEFFICIENT_CONTRACT, BRANCH_CONTRACT),
        (SYMBOL_MATCH, BRANCH_SYMBOL),
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
    variations = read_csv(VARIATION_DERIVATION)
    contracts = read_csv(COEFFICIENT_CONTRACT)
    symbols = read_csv(SYMBOL_MATCH)
    outcomes = read_csv(DELTAK_OUTCOME)
    fallback = read_csv(KERNEL_FALLBACK)
    rejections = read_csv(REJECTION_LEDGER)
    gates = read_csv(CLAIM_GATE)
    decisions = read_csv(DECISION)
    next_rows = read_csv(NEXT_TARGET)

    checks = [
        ("VAL1526_0_sources_exist", all(row["exists"] == "True" for row in sources), "all cited 1526 input source paths exist"),
        ("VAL1526_1_tracefree_variation", any(row["variation_id"] == "VAR1526_3_tracefree_projection" and row["status"] == "EXACT_TRACEFREE_MATCH_DERIVED" for row in variations), "trace-free phi R response gives K_L shape"),
        ("VAL1526_2_phi_owner_block", any(row["variation_id"] == "VAR1526_4_phi_equation_guard" and row["status"] == "PHI_OWNER_MISSING" for row in variations), "phi owner/locality blocker is retained"),
        ("VAL1526_3_coefficient_law", any(row["contract_id"] == "SIG1526_1_coefficient_law" and row["status"] == "COEFFICIENT_MATCH_LAW_DERIVED" for row in contracts), "sigma_resp*c_I=1 coefficient law is written"),
        ("VAL1526_4_symbol_not_matched", any(row["match_id"] == "SYM1526_5_verdict" and row["status"] == "NOT_MATCHED" for row in symbols), "current Khat match remains blocked"),
        ("VAL1526_5_DeltaK_blocked", any(row["outcome_id"] == "OUT1526_1_current_status" and row["status"] == "BLOCKED_NOT_PROMOTED" for row in outcomes), "DeltaK not promoted"),
        ("VAL1526_6_fallback_retained", len(fallback) >= 6 and all("MISSING" in row["status"] for row in fallback), "Kmetric fallback kernels retained"),
        ("VAL1526_7_rejections_guardrails", len(rejections) >= 5 and all(row["status"] == "REJECTED" for row in rejections), "unsafe shortcuts rejected"),
        ("VAL1526_8_claim_gates_block", any(row["gate_id"] == "GATE1526_5_local_GR" and row["status"] == "BLOCKED_NO_CLAIM" for row in gates), "local GR claim remains blocked"),
        ("VAL1526_9_decision_next", any(row["result"] == "NEXT_PHI_OWNER_AND_SYMBOL_MATCH" for row in decisions), "decision selects phi owner and Khat symbol match next"),
        ("VAL1526_10_next_target", any("1527-Y5-phi-owner" in row["next_target"] for row in next_rows), "next target is phi owner/current Khat source hunt"),
        ("VAL1526_11_csv_parse", all(parse_csv(path) for path in generated_csvs), "all generated 1526 CSVs parse cleanly"),
        ("VAL1526_12_claim_flags_false", generated_flags_false(generated_csvs), "all generated prediction/claim flags remain false"),
        ("VAL1526_13_branch_copies", all(path.exists() for path in [QUAR_VARIATION, QUAR_CONTRACT, QUAR_SYMBOL, QUAR_DECISION, BRANCH_VARIATION, BRANCH_CONTRACT, BRANCH_SYMBOL, BRANCH_DECISION]), "branch/quarantine nonclaim copies written"),
        ("VAL1526_14_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent after run"),
        ("VAL1526_15_formalization_untouched", formalization_modified_count_since_start() == 0, "formalization modified-file count since start=0"),
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
            "check_id": "VAL1526_16_overall",
            "result": "PASS" if overall else "FAIL",
            "detail": "1526 derives the conditional trace-free phi R route, keeps phi/Khat/local-GR nonclaim, and selects phi owner/current Khat source hunt next"
            if overall
            else "1526 validation failed; inspect failed rows before continuing",
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
    variations: list[dict[str, Any]],
    contracts: list[dict[str, Any]],
    symbols: list[dict[str, Any]],
    outcomes: list[dict[str, Any]],
    fallback: list[dict[str, Any]],
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
                "# 1526 - Trace-Free Hessian Improvement Action Coefficient and Symbol Match",
                "",
                "## Verdict",
                "- Real derivation gain: the trace-free part of the metric variation of `int sqrt(-g) phi R` gives the exact `K_L` tensor shape, up to the response sign/convention.",
                "- The coefficient law is now explicit: the live convention must satisfy `sigma_resp*c_I=1` for `K_hat=K_L` in the local trace-free derivative channel.",
                "- New hard bottleneck: `Box phi=(2/3)(Gamma_eff+C)` needs a parent-owned local auxiliary constraint, otherwise the route risks becoming an inverse-Box/nonlocal construction.",
                "- Current MTS `K_hat` is still not matched to this improvement response; the result is conditional and nonclaim.",
                "- No local-GR/Newton/PPN claim is promoted from 1526.",
                "",
                "## Source Register",
                md_table(sources, ["source_id", "source_path", "exists", "purpose"]),
                "",
                "## Variation Derivation",
                md_table(variations, ["variation_id", "object", "formula_or_statement", "status", "missing_to_promote"]),
                "",
                "## Coefficient / Sign Contract",
                md_table(contracts, ["contract_id", "quantity", "contract_or_formula", "status", "missing_to_promote"]),
                "",
                "## Symbol Match Audit",
                md_table(symbols, ["match_id", "object", "evidence_or_contract", "status", "missing_to_promote"]),
                "",
                "## DeltaK Outcome Runner",
                md_table(outcomes, ["outcome_id", "branch", "statement", "status", "reason"]),
                "",
                "## Retained Kernel Fallback",
                md_table(fallback, ["fallback_id", "object", "why_needed", "status"]),
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
    variations = variation_derivation_rows()
    contracts = coefficient_contract_rows()
    symbols = symbol_match_rows()
    outcomes = deltak_outcome_rows()
    fallback = kernel_fallback_rows()
    rejections = rejection_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    local_rows = local_status_rows()
    next_rows = next_target_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(VARIATION_DERIVATION, variations)
    write_csv(COEFFICIENT_CONTRACT, contracts)
    write_csv(SYMBOL_MATCH, symbols)
    write_csv(DELTAK_OUTCOME, outcomes)
    write_csv(KERNEL_FALLBACK, fallback)
    write_csv(REJECTION_LEDGER, rejections)
    write_csv(CLAIM_GATE, gates)
    write_csv(DECISION, decisions)
    write_csv(LOCAL_STATUS, local_rows)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()
    remove_pycache()

    generated_csvs = [
        SOURCE_REGISTER,
        VARIATION_DERIVATION,
        COEFFICIENT_CONTRACT,
        SYMBOL_MATCH,
        DELTAK_OUTCOME,
        KERNEL_FALLBACK,
        REJECTION_LEDGER,
        CLAIM_GATE,
        DECISION,
        LOCAL_STATUS,
        NEXT_TARGET,
    ]
    validation = validation_rows(generated_csvs)
    write_csv(VALIDATION, validation)
    write_doc(sources, variations, contracts, symbols, outcomes, fallback, rejections, gates, decisions, local_rows, validation, next_rows)


if __name__ == "__main__":
    main()
