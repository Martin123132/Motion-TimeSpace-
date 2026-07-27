from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CSV_DIR = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1186-Y5-R10-q_loc-response-operator-bound-or-qnorm-source-row.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
STAMP = datetime.now(timezone.utc).isoformat()


def stamp(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    return [row | {"generated_utc": STAMP} for row in rows]


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"empty csv refused: {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def md_escape(value: object) -> str:
    return str(value).replace("\\", "\\\\").replace("|", "\\|").replace("\n", " ")


def table(rows: list[dict[str, object]]) -> str:
    if not rows:
        return ""
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key == "generated_utc":
                continue
            if key not in headers:
                headers.append(key)
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(md_escape(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


def source_rows() -> list[dict[str, object]]:
    entries = [
        {
            "source_id": "SRC1186_0_1185_next",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1185_NEXT_TARGET.csv",
            "needle": "NEXT1185_0_1186",
            "role": "handoff to q_loc response operator bound or qnorm source row.",
        },
        {
            "source_id": "SRC1186_1_1185_summary",
            "relative_path": "source-intake/mts_residuals/P8_Y5_BRR545_1185_VALIDATION.csv",
            "needle": "V1185_SUMMARY",
            "role": "1185 validation summary.",
        },
        {
            "source_id": "SRC1186_2_1185_Rq",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1185_RESPONSE_INPUT_LEDGER.csv",
            "needle": "QRI1185_0_Rq_operator",
            "role": "R_q response operator missing.",
        },
        {
            "source_id": "SRC1186_3_1185_gamma",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1185_UPDATED_SCORE_ROWS.csv",
            "needle": "QSU1185_0_gamma",
            "role": "gamma score needs scalar R_q response.",
        },
        {
            "source_id": "SRC1186_4_1010_status",
            "relative_path": "1010-Y5-R10-Gamma-Khat-action-existence-Helmholtz-or-q_loc-residual-retention.md",
            "needle": "retained as an explicit nonclaim residual",
            "role": "q_loc remains retained residual.",
        },
        {
            "source_id": "SRC1186_5_1010_metric_response",
            "relative_path": "1010-Y5-R10-Gamma-Khat-action-existence-Helmholtz-or-q_loc-residual-retention.md",
            "needle": "GKT1010_1_metric_response_identity",
            "role": "metric-response identity needed for q_loc zero route.",
        },
        {
            "source_id": "SRC1186_6_1010_Euler",
            "relative_path": "1010-Y5-R10-Gamma-Khat-action-existence-Helmholtz-or-q_loc-residual-retention.md",
            "needle": "GKT1010_3_Euler_closure",
            "role": "Euler closure needed for q_loc zero route.",
        },
        {
            "source_id": "SRC1186_7_207_conservation",
            "relative_path": "207-domain-projector-action-and-Bianchi-identity.md",
            "needle": "nabla_mu T_total^{mu nu} = 0",
            "role": "Bianchi-safe stress bookkeeping.",
        },
        {
            "source_id": "SRC1186_8_207_hidden_force",
            "relative_path": "207-domain-projector-action-and-Bianchi-identity.md",
            "needle": "That would hide an external force and fake conservation.",
            "role": "hidden stress/fake conservation guard.",
        },
        {
            "source_id": "SRC1186_9_q_contract",
            "relative_path": "source-intake/mts_residuals/P8_GAMMA_KHAT_QLOC_FIRST_VARIATION_CONTRACT.csv",
            "needle": "GK513_2_Euler_closure",
            "role": "q_loc Euler closure contract.",
        },
        {
            "source_id": "SRC1186_10_q_demote",
            "relative_path": "source-intake/mts_residuals/P8_GAMMA_KHAT_QLOC_RESIDUAL_OR_DEMOTION.csv",
            "needle": "QR513_0_nonvariational_stress",
            "role": "nonvariational q_loc demotion route.",
        },
    ]
    checked: list[dict[str, object]] = []
    for entry in entries:
        path = ROOT / str(entry["relative_path"])
        text = path.read_text(encoding="utf-8", errors="ignore") if path.exists() else ""
        checked.append(entry | {"exists": path.exists(), "needle_found": str(entry["needle"]) in text})
    return stamp(checked)


def response_attempt_rows() -> list[dict[str, object]]:
    rows = [
        {
            "attempt_id": "RQB1186_0_direct_map_guard",
            "object": "direct R_q map",
            "statement": "A direct map from nonconserved q_loc to metric perturbation is not Bianchi-safe: the metric operator obeys a divergence identity, so its source must be conserved or compensated.",
            "derived_result": "direct R_q is forbidden unless q_loc is canceled or embedded in a conserved total source",
            "status": "DIRECT_RESPONSE_REJECTED_BY_WARD_GUARD",
            "missing_for_claim": "conserved total source or q_loc zero theorem",
            "valid_for_claim": False,
        },
        {
            "attempt_id": "RQB1186_1_compensator_route",
            "object": "compensator stress C_q^{mu nu}",
            "statement": "Introduce a stress compensator satisfying nabla_mu C_q^{mu nu} = -q_loc^nu so that T_total = T_EH_source + C_q is conserved.",
            "derived_result": "this is the minimum Ward-safe way to let q_loc affect metric residuals without violating Bianchi identities",
            "status": "WARD_SAFE_ROUTE_WRITTEN",
            "missing_for_claim": "parent-owned compensator or right-inverse of divergence with boundary conditions",
            "valid_for_claim": False,
        },
        {
            "attempt_id": "RQB1186_2_operator_factorization",
            "object": "R_q factorization",
            "statement": "If a right-inverse Div^{-1} and metric Green operator G_EH exist, then R_q = P_metric G_EH Div^{-1}.",
            "derived_result": "||P_scalar R_q|| <= ||P_scalar G_EH|| ||Div^{-1}|| and ||P_TF R_q|| <= ||P_TF G_EH|| ||Div^{-1}||",
            "status": "OPERATOR_BOUND_FORM_DERIVED",
            "missing_for_claim": "gauge, domain, boundary conditions, Green norm, divergence inverse norm",
            "valid_for_claim": False,
        },
        {
            "attempt_id": "RQB1186_3_zero_route",
            "object": "q_loc zero via S_GK",
            "statement": "If S_GK exists and metric-response/Helmholtz/Euler/double-zero/P_loc/boundary clauses close, q_loc vanishes on shell and R_q is unnecessary.",
            "derived_result": "zero route remains blocked by 1010; do not claim q_loc=0",
            "status": "ZERO_ROUTE_RESTATED_BLOCKED",
            "missing_for_claim": "all 1010 parent-signed certificates",
            "valid_for_claim": False,
        },
        {
            "attempt_id": "RQB1186_4_verdict",
            "object": "response operator verdict",
            "statement": "1186 derives a Ward-safe factorized response bound but cannot source the operator norms or q_loc norm.",
            "derived_result": "R_q is now a conserved-source/compensator problem, not a free response coefficient",
            "status": "BOUND_FORM_DERIVED_INPUTS_MISSING",
            "missing_for_claim": "Div^{-1}, G_EH, boundary/gauge conditions, q_loc profile/norm",
            "valid_for_claim": False,
        },
    ]
    return stamp(rows)


def operator_input_rows() -> list[dict[str, object]]:
    rows = [
        {
            "input_id": "RQI1186_0_div_inverse",
            "quantity": "||Div^{-1}||_D",
            "definition": "right-inverse-of-divergence norm mapping q_loc^nu to compensator stress C_q^{mu nu}",
            "bound_relation": "||C_q|| <= ||Div^{-1}||_D ||q_loc|| + boundary_flux",
            "current_value": "MISSING_DIVERGENCE_INVERSE_NORM",
            "source_needed": "domain/gauge/boundary conditions or parent compensator action",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "input_id": "RQI1186_1_G_scalar",
            "quantity": "||P_scalar G_EH||",
            "definition": "scalar PPN projection norm of the gauge-fixed metric Green operator",
            "bound_relation": "||P_scalar R_q|| <= ||P_scalar G_EH|| ||Div^{-1}||",
            "current_value": "MISSING_SCALAR_GREEN_NORM",
            "source_needed": "linearized metric operator, gauge, compact domain, units",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "input_id": "RQI1186_2_G_TF",
            "quantity": "||P_TF G_EH||",
            "definition": "STF/tidal PPN projection norm of the gauge-fixed metric Green operator",
            "bound_relation": "||P_TF R_q|| <= ||P_TF G_EH|| ||Div^{-1}||",
            "current_value": "MISSING_TF_GREEN_NORM",
            "source_needed": "linearized metric operator, gauge, compact domain, units",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "input_id": "RQI1186_3_qnorm",
            "quantity": "||q_loc||_PPN",
            "definition": "PPN-domain norm of P_loc(nabla Gamma_eff - nabla_mu K_hat^{mu nu})",
            "bound_relation": "feeds q_trace and q_TF after response operator",
            "current_value": "MISSING_QLOC_PROFILE_OR_NORM",
            "source_needed": "Gamma_eff/K_hat formulas, P_loc domain, units, profiles, or residual-bound source",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "input_id": "RQI1186_4_boundary_flux",
            "quantity": "B_q_boundary",
            "definition": "boundary/symplectic flux contribution to compensator or q_loc residual",
            "bound_relation": "||C_q|| <= ||Div^{-1}|| ||q_loc|| + B_q_boundary",
            "current_value": "MISSING_BOUNDARY_NO_FLUX_OR_BOUND",
            "source_needed": "boundary no-flux theorem or radial M_eff/source-measure bound",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "input_id": "RQI1186_5_compensator_action",
            "quantity": "S_comp[q] or parent C_q sector",
            "definition": "parent-owned sector whose stress divergence cancels q_loc without fake conservation",
            "bound_relation": "nabla_mu C_q^{mu nu}=-q_loc^nu",
            "current_value": "MISSING_PARENT_COMPENSATOR",
            "source_needed": "parent action / auxiliary stress with retained metric variation",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]
    return stamp(rows)


def qnorm_source_rows() -> list[dict[str, object]]:
    rows = [
        {
            "qnorm_id": "QNR1186_0_formula_row",
            "quantity": "q_loc^nu",
            "formula": "P_loc(nabla^nu Gamma_eff - nabla_mu K_hat^{mu nu})",
            "needed_values": "Gamma_eff profile; K_hat profile; P_loc; derivative convention; units; PPN domain",
            "current_status": "FORMULA_SOURCE_EXISTS_VALUES_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "qnorm_id": "QNR1186_1_norm_row",
            "quantity": "||q_loc||_PPN",
            "formula": "chosen PPN domain norm of q_loc^nu",
            "needed_values": "domain measure; tensor/vector norm; source path; uncertainty or bound",
            "current_status": "MISSING_NUMERIC_OR_THEOREM_BOUND",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "qnorm_id": "QNR1186_2_zero_certificate_row",
            "quantity": "q_loc_zero_certificate",
            "formula": "S_GK + metric response + Helmholtz + Euler/double-zero + P_loc + boundary no-flux",
            "needed_values": "all 1010 certificates pass",
            "current_status": "BLOCKED_BY_1010",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "qnorm_id": "QNR1186_3_demoted_residual_row",
            "quantity": "q_loc_residual_bound",
            "formula": "empirical/theorem upper bound carried into PPN/R10/clock/orbital residual vector",
            "needed_values": "source-backed bound; arena projection; uncertainty; valid_for_claim gate",
            "current_status": "SOURCE_READY_NONCLAIM_ROW",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]
    return stamp(rows)


def score_update_rows() -> list[dict[str, object]]:
    rows = [
        {
            "score_id": "RQS1186_0_gamma",
            "component": "gamma_minus_1",
            "updated_bound": "|gamma_MTS-1| <= other_terms + ||P_scalar G_EH|| ||Div^{-1}|| ||q_loc|| + boundary_scalar",
            "closed_by_1186": "Ward-safe R_q factorization and bound form",
            "still_missing": "Green norm; divergence inverse norm; q_loc norm; boundary flux",
            "score_status": "NOT_SCOREABLE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "score_id": "RQS1186_1_STF",
            "component": "H_TF_metric",
            "updated_bound": "||H_TF|| <= |K_S| ||S_Q|| + ||P_TF G_EH|| ||Div^{-1}|| ||q_loc|| + boundary_TF + projector_TF",
            "closed_by_1186": "Ward-safe R_q factorization and bound form",
            "still_missing": "K_S; S_Q norm; TF Green norm; divergence inverse norm; q_loc norm; boundary/projector terms",
            "score_status": "NOT_SCOREABLE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "score_id": "RQS1186_2_consistency",
            "component": "Bianchi/Ward consistency",
            "updated_bound": "either q_loc=0, or C_q exists with divergence -q_loc, or q_loc remains explicit nonmetric residual",
            "closed_by_1186": "logical trichotomy written",
            "still_missing": "which branch is parent-signed",
            "score_status": "NONCLAIM_BRANCH_GATE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]
    return stamp(rows)


def gate_rows() -> list[dict[str, object]]:
    rows = [
        {
            "gate_id": "G1186_0_direct_Rq",
            "claim": "direct R_q maps nonconserved q_loc to metric residual",
            "status": "FAILED_BIANCHI_WARD_GUARD",
            "why": "metric source must be conserved or compensated",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1186_1_compensator",
            "claim": "Ward-safe compensator response is available",
            "status": "BLOCKED_COMPENSATOR_OR_DIV_INVERSE_MISSING",
            "why": "no parent C_q sector or divergence right-inverse/source path is supplied",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1186_2_operator_norms",
            "claim": "||P_scalar R_q|| and ||P_TF R_q|| are known",
            "status": "BLOCKED_GREEN_AND_DIV_NORMS_MISSING",
            "why": "G_EH norms, Div inverse norm, domain/gauge, and boundary terms are missing",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1186_3_qnorm",
            "claim": "||q_loc||_PPN is known",
            "status": "BLOCKED_GAMMA_KHAT_PROFILES_MISSING",
            "why": "Gamma_eff/K_hat/P_loc profiles and units are missing",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1186_4_qzero",
            "claim": "q_loc=0",
            "status": "BLOCKED_1010_ZERO_ROUTE_MISSING",
            "why": "S_GK/metric-response/Helmholtz/Euler/double-zero/P_loc/boundary certificates are unsigned",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1186_5_PPN_local",
            "claim": "PPN/local-GR score is allowed",
            "status": "BLOCKED_NO_LOCAL_CLAIM",
            "why": "response operator and q_loc norm are not scoreable",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]
    return stamp(rows)


def decision_rows() -> list[dict[str, object]]:
    rows = [
        {
            "decision_id": "D1186_0_main_result",
            "decision": "direct_Rq_rejected_Ward_safe_factorization_written",
            "reason": "a nonconserved residual cannot directly source metric perturbations without violating Bianchi/Ward consistency.",
            "next_action": "derive a compensator/divergence-inverse bound or keep q_loc as explicit residual.",
            "valid_for_claim": False,
        },
        {
            "decision_id": "D1186_1_qnorm_status",
            "decision": "first_qnorm_source_rows_staged",
            "reason": "Gamma_eff/K_hat/P_loc profiles and units are still missing, but q_loc norm requirements are now concrete.",
            "next_action": "source Gamma_eff and K_hat profiles or build a residual bound from existing scripts/data.",
            "valid_for_claim": False,
        },
        {
            "decision_id": "D1186_2_best_next",
            "decision": "target_compensator_divergence_inverse_or_Gamma_Khat_profiles",
            "reason": "these are the shortest routes to making q_trace/q_TF numerically meaningful.",
            "next_action": "1187 should attempt the compensator stress/divergence inverse theorem or first Gamma/Khat qnorm source row.",
            "valid_for_claim": False,
        },
    ]
    return stamp(rows)


def next_rows() -> list[dict[str, object]]:
    rows = [
        {
            "next_id": "NEXT1186_0_1187",
            "next_target": "1187-Y5-R10-compensator-divergence-inverse-or-Gamma-Khat-qnorm-source.md",
            "objective": "derive a parent-owned compensator/right-inverse-of-divergence bound for q_loc, or source Gamma_eff/K_hat/P_loc profiles sufficient to create the first q_loc norm row",
            "include": "C_q stress; Div^{-1}; boundary no-flux; G_EH norms; Gamma_eff profile; K_hat profile; P_loc domain; no-claim validation",
            "exclude": "direct nonconserved metric source; q_loc zero claim; invented operator norms; PPN pass; GitHub; formalization edits",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]
    return stamp(rows)


def validation_rows(
    sources: list[dict[str, object]],
    attempts: list[dict[str, object]],
    inputs: list[dict[str, object]],
    qnorms: list[dict[str, object]],
    scores: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    nexts: list[dict[str, object]],
) -> list[dict[str, object]]:
    checks = [
        {
            "check_id": "V1186_0_sources_exist",
            "result": "pass" if all(r["exists"] and r["needle_found"] for r in sources) else "fail",
            "detail": "all cited local source paths exist and needles are found",
            "claim_allowed": False,
        },
        {
            "check_id": "V1186_1_direct_Rq_rejected",
            "result": "pass" if any(r["status"] == "DIRECT_RESPONSE_REJECTED_BY_WARD_GUARD" for r in attempts) else "fail",
            "detail": "direct nonconserved response map is rejected",
            "claim_allowed": False,
        },
        {
            "check_id": "V1186_2_factorization_written",
            "result": "pass" if any(r["status"] == "OPERATOR_BOUND_FORM_DERIVED" for r in attempts) else "fail",
            "detail": "Ward-safe R_q = P_metric G_EH Div^{-1} factorization is written",
            "claim_allowed": False,
        },
        {
            "check_id": "V1186_3_operator_inputs_staged",
            "result": "pass"
            if {r["quantity"] for r in inputs} >= {
                "||Div^{-1}||_D",
                "||P_scalar G_EH||",
                "||P_TF G_EH||",
                "||q_loc||_PPN",
                "B_q_boundary",
                "S_comp[q] or parent C_q sector",
            }
            else "fail",
            "detail": "all operator input rows are staged",
            "claim_allowed": False,
        },
        {
            "check_id": "V1186_4_qnorm_rows_staged",
            "result": "pass" if len(qnorms) >= 4 and all(r["claim_allowed"] is False for r in qnorms) else "fail",
            "detail": "first q_loc norm/source rows are staged and nonclaim",
            "claim_allowed": False,
        },
        {
            "check_id": "V1186_5_scores_nonclaim",
            "result": "pass" if len(scores) >= 3 and all(r["claim_allowed"] is False for r in scores) else "fail",
            "detail": "updated score rows remain nonclaim",
            "claim_allowed": False,
        },
        {
            "check_id": "V1186_6_missing_inputs_not_claim_valid",
            "result": "pass"
            if all((not any("MISSING" in str(v) for v in row.values())) or row["valid_for_claim"] is False for row in inputs + qnorms + scores)
            else "fail",
            "detail": "rows with missing inputs remain invalid for claim",
            "claim_allowed": False,
        },
        {
            "check_id": "V1186_7_gates_nonclaim",
            "result": "pass" if all(r["claim_allowed"] is False for r in gates) else "fail",
            "detail": "all gates remain nonclaim",
            "claim_allowed": False,
        },
        {
            "check_id": "V1186_8_no_claim_rows",
            "result": "pass"
            if all(row.get("valid_for_claim") is False for row in attempts + inputs + qnorms + scores + gates + decisions + nexts)
            else "fail",
            "detail": "all generated science rows remain nonclaim",
            "claim_allowed": False,
        },
        {
            "check_id": "V1186_9_next_target",
            "result": "pass" if nexts and "1187" in str(nexts[0]["next_target"]) else "fail",
            "detail": "1187 handoff targets compensator/divergence inverse or Gamma/Khat qnorm source",
            "claim_allowed": False,
        },
        {
            "check_id": "V1186_10_generated_under_post_checkpoint",
            "result": "pass" if str(DOC).startswith(str(ROOT)) and str(CSV_DIR).startswith(str(ROOT)) else "fail",
            "detail": "all generated outputs are under post-checkpoint-work",
            "claim_allowed": False,
        },
        {
            "check_id": "V1186_11_formalization_untouched",
            "result": "pass",
            "detail": "generator writes no outputs under formalization-workbench",
            "claim_allowed": False,
        },
        {
            "check_id": "V1186_SUMMARY",
            "result": "pass",
            "detail": "1186 rejects direct nonconserved R_q, derives the Ward-safe response factorization through a compensator/right-inverse of divergence, stages operator/qnorm inputs, refuses PPN/local scoring, and hands off to compensator or Gamma/Khat qnorm sourcing",
            "claim_allowed": False,
        },
    ]
    return stamp(checks)


def write_doc(
    sources: list[dict[str, object]],
    attempts: list[dict[str, object]],
    inputs: list[dict[str, object]],
    qnorms: list[dict[str, object]],
    scores: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    validations: list[dict[str, object]],
    nexts: list[dict[str, object]],
) -> None:
    parts = [
        "# 1186 - Y5/R10 q_loc response operator bound or qnorm source row",
        "**Current verdict:** a direct `R_q` from nonconserved `q_loc` into the metric is rejected. It would violate the Bianchi/Ward bookkeeping unless `q_loc` is zero or carried by a conserved compensator sector.",
        "**Main progress:** the Ward-safe response factorization is now explicit: if a compensator satisfies `nabla_mu C_q^{mu nu}=-q_loc^nu`, then `R_q = P_metric G_EH Div^{-1}` and its scalar/STF bounds factor through Green and divergence-inverse norms.",
        "**Hard blocker:** `Div^{-1}`, `G_EH` projection norms, boundary flux, the compensator action, and `||q_loc||_PPN` are not sourced.",
        "**No claim:** no q_loc zero, local-GR, Newton, R10, PPN, WEP, clock, orbital, `c_g=0`, or public-facing claim follows from this checkpoint.",
        "## Source register\n\n" + table(sources),
        "## q_loc response-operator attempt\n\n" + table(attempts),
        "## Ward-safe operator input ledger\n\n" + table(inputs),
        "## q_loc norm source rows\n\n" + table(qnorms),
        "## Updated score rows\n\n" + table(scores),
        "## Claim gates\n\n" + table(gates),
        "## Decision ledger\n\n" + table(decisions),
        "## Validation\n\n" + table(validations),
        "## Next target\n\n" + table(nexts),
    ]
    DOC.write_text("\n\n".join(parts) + "\n", encoding="utf-8")


def main() -> None:
    CSV_DIR.mkdir(parents=True, exist_ok=True)
    sources = source_rows()
    attempts = response_attempt_rows()
    inputs = operator_input_rows()
    qnorms = qnorm_source_rows()
    scores = score_update_rows()
    gates = gate_rows()
    decisions = decision_rows()
    nexts = next_rows()
    validations = validation_rows(sources, attempts, inputs, qnorms, scores, gates, decisions, nexts)

    outputs = {
        "P8_Y5_R10_1186_SOURCE_REGISTER.csv": sources,
        "P8_Y5_R10_1186_QLOC_RESPONSE_OPERATOR_ATTEMPT.csv": attempts,
        "P8_Y5_R10_1186_WARD_SAFE_OPERATOR_INPUT_LEDGER.csv": inputs,
        "P8_Y5_R10_1186_QLOC_NORM_SOURCE_ROWS.csv": qnorms,
        "P8_Y5_R10_1186_UPDATED_SCORE_ROWS.csv": scores,
        "P8_Y5_R10_1186_CLAIM_GATES.csv": gates,
        "P8_Y5_R10_1186_DECISION_LEDGER.csv": decisions,
        "P8_Y5_R10_1186_NEXT_TARGET.csv": nexts,
        "P8_Y5_BRR545_1186_VALIDATION.csv": validations,
    }
    for filename, rows in outputs.items():
        write_csv(CSV_DIR / filename, rows)

    write_doc(sources, attempts, inputs, qnorms, scores, gates, decisions, validations, nexts)

    failed = [row["check_id"] for row in validations if row["result"] != "pass"]
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    if FORMALIZATION.exists() and not FORMALIZATION.is_dir():
        failed.append("formalization_path_not_directory")

    print(f"wrote {DOC}")
    print("validation: PASS" if not failed else f"validation: FAIL {failed}")
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
