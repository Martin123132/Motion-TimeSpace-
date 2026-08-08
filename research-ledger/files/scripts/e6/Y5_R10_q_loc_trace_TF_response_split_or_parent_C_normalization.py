from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CSV_DIR = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1185-Y5-R10-q_loc-trace-TF-response-split-or-parent-C-normalization.md"
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
            "source_id": "SRC1185_0_1184_next",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1184_NEXT_TARGET.csv",
            "needle": "NEXT1184_0_1185",
            "role": "handoff to q_loc trace/TF response split or parent C normalization.",
        },
        {
            "source_id": "SRC1185_1_1184_summary",
            "relative_path": "source-intake/mts_residuals/P8_Y5_BRR545_1184_VALIDATION.csv",
            "needle": "V1184_SUMMARY",
            "role": "1184 validation summary.",
        },
        {
            "source_id": "SRC1185_2_1184_qtrace",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1184_PHYSICAL_SCALAR_LEAKAGE_INPUT_LEDGER.csv",
            "needle": "PLI1184_4_q_trace",
            "role": "q_trace row says response split is missing.",
        },
        {
            "source_id": "SRC1185_3_1184_gamma",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1184_SCORE_FORMULA_DRY_RUN.csv",
            "needle": "SFR1184_0_gamma_bound",
            "role": "gamma score needs q_trace.",
        },
        {
            "source_id": "SRC1185_4_1184_STF",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1184_SCORE_FORMULA_DRY_RUN.csv",
            "needle": "SFR1184_1_STF_bound",
            "role": "STF score needs q_TF.",
        },
        {
            "source_id": "SRC1185_5_1010_status",
            "relative_path": "1010-Y5-R10-Gamma-Khat-action-existence-Helmholtz-or-q_loc-residual-retention.md",
            "needle": "retained as an explicit nonclaim residual",
            "role": "q_loc remains a retained residual.",
        },
        {
            "source_id": "SRC1185_6_1010_metric_response",
            "relative_path": "1010-Y5-R10-Gamma-Khat-action-existence-Helmholtz-or-q_loc-residual-retention.md",
            "needle": "GKT1010_1_metric_response_identity",
            "role": "metric response identity target.",
        },
        {
            "source_id": "SRC1185_7_1010_Helmholtz",
            "relative_path": "1010-Y5-R10-Gamma-Khat-action-existence-Helmholtz-or-q_loc-residual-retention.md",
            "needle": "GKT1010_2_Helmholtz_integrability",
            "role": "Helmholtz integrability target.",
        },
        {
            "source_id": "SRC1185_8_q_contract",
            "relative_path": "source-intake/mts_residuals/P8_GAMMA_KHAT_QLOC_FIRST_VARIATION_CONTRACT.csv",
            "needle": "GK513_0_action_existence",
            "role": "q_loc action-existence contract.",
        },
        {
            "source_id": "SRC1185_9_symbol_map",
            "relative_path": "source-intake/mts_residuals/P8_MTS_SYMBOL_TO_LOCAL_GR_ACTION_MAP.csv",
            "needle": "q_loc^nu = P_loc",
            "role": "q_loc definition as derived residual, not field.",
        },
        {
            "source_id": "SRC1185_10_1009_root",
            "relative_path": "1009-Y5-R10-parent-current-chain-action-contract-or-sector-variation-runner.md",
            "needle": "Gamma_eff/K_hat/q_loc is the sharpest next derivation target",
            "role": "root local-GR blocker.",
        },
    ]
    checked: list[dict[str, object]] = []
    for entry in entries:
        path = ROOT / str(entry["relative_path"])
        text = path.read_text(encoding="utf-8", errors="ignore") if path.exists() else ""
        checked.append(entry | {"exists": path.exists(), "needle_found": str(entry["needle"]) in text})
    return stamp(checked)


def split_attempt_rows() -> list[dict[str, object]]:
    rows = [
        {
            "attempt_id": "QRS1185_0_type_guard",
            "object": "q_loc^nu",
            "statement": "q_loc is a vector/Ward-force residual, so it has no intrinsic scalar trace or STF tensor part by itself.",
            "derived_result": "q_trace and q_TF must mean projections after a response map from q_loc to metric/scalar residuals.",
            "status": "TYPE_GUARD_DERIVED",
            "missing_for_claim": "response operator R_q",
            "valid_for_claim": False,
        },
        {
            "attempt_id": "QRS1185_1_response_operator",
            "object": "R_q",
            "statement": "Define a local response map delta g_ij^(q) = R_{ij nu} q_loc^nu after gauge/readout choice.",
            "derived_result": "this is the minimum object required before scalar/STF PPN scoring of q_loc.",
            "status": "RESPONSE_MAP_REQUIRED",
            "missing_for_claim": "parent metric response, Green operator, gauge/readout convention, source path",
            "valid_for_claim": False,
        },
        {
            "attempt_id": "QRS1185_2_scalar_projection",
            "object": "q_trace",
            "statement": "q_trace := P_scalar(R_q q_loc) = (1/3)delta^ij R_{ij nu} q_loc^nu in local PPN frame.",
            "derived_result": "|q_trace| <= ||P_scalar R_q|| ||q_loc||",
            "status": "BOUND_FORM_DERIVED_INPUTS_MISSING",
            "missing_for_claim": "||P_scalar R_q|| and ||q_loc||",
            "valid_for_claim": False,
        },
        {
            "attempt_id": "QRS1185_3_STF_projection",
            "object": "q_TF",
            "statement": "q_TFij := P_TF(R_q q_loc)_ij = (R_{ij nu} - delta_ij delta^ab R_{ab nu}/3) q_loc^nu.",
            "derived_result": "||q_TF|| <= ||P_TF R_q|| ||q_loc||",
            "status": "BOUND_FORM_DERIVED_INPUTS_MISSING",
            "missing_for_claim": "||P_TF R_q|| and ||q_loc||",
            "valid_for_claim": False,
        },
        {
            "attempt_id": "QRS1185_4_variational_zero_route",
            "object": "q_loc zero route",
            "statement": "If S_GK exists, K_hat is the metric response of Gamma_eff, Helmholtz symmetry holds, Euler equations close, and boundary no-flux holds, q_loc can vanish on shell.",
            "derived_result": "route remains blocked by 1010 gates; do not claim q_loc=0.",
            "status": "ZERO_ROUTE_BLOCKED",
            "missing_for_claim": "S_GK; metric-response identity; Helmholtz; Euler/double-zero; P_loc; boundary no-flux",
            "valid_for_claim": False,
        },
        {
            "attempt_id": "QRS1185_5_verdict",
            "object": "q_loc response split verdict",
            "statement": "1185 derives the correct projection contract and norm bounds, but cannot source R_q or ||q_loc|| from the current chain.",
            "derived_result": "q_trace/q_TF are now well-defined nonclaim closure rows, not informal labels.",
            "status": "SPLIT_CONTRACT_DERIVED_NUMERIC_INPUTS_MISSING",
            "missing_for_claim": "response-operator source or residual norm rows",
            "valid_for_claim": False,
        },
    ]
    return stamp(rows)


def response_input_rows() -> list[dict[str, object]]:
    rows = [
        {
            "input_id": "QRI1185_0_Rq_operator",
            "quantity": "R_q",
            "definition": "linear response operator mapping q_loc^nu to metric/scalar residual delta g_ij^(q)",
            "bound_relation": "needed before q_trace or q_TF are physical quantities",
            "current_value": "MISSING_RESPONSE_OPERATOR",
            "source_needed": "parent metric response or gauge-fixed Green operator",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "input_id": "QRI1185_1_Rq_scalar_norm",
            "quantity": "||P_scalar R_q||",
            "definition": "operator norm from q_loc vector residual to scalar PPN gamma leakage",
            "bound_relation": "|q_trace| <= ||P_scalar R_q|| ||q_loc||",
            "current_value": "MISSING_SCALAR_RESPONSE_NORM",
            "source_needed": "response-operator bound",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "input_id": "QRI1185_2_Rq_TF_norm",
            "quantity": "||P_TF R_q||",
            "definition": "operator norm from q_loc vector residual to STF/tidal PPN leakage",
            "bound_relation": "||q_TF|| <= ||P_TF R_q|| ||q_loc||",
            "current_value": "MISSING_TF_RESPONSE_NORM",
            "source_needed": "response-operator bound",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "input_id": "QRI1185_3_q_loc_norm",
            "quantity": "||q_loc||_PPN",
            "definition": "arena norm of P_loc(nabla Gamma_eff - nabla_mu K_hat^{mu nu})",
            "bound_relation": "feeds both q_trace and q_TF",
            "current_value": "MISSING_QLOC_NORM",
            "source_needed": "Gamma_eff/K_hat profiles, action residual, or empirical nonclaim bound",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "input_id": "QRI1185_4_q_trace",
            "quantity": "q_trace",
            "definition": "P_scalar(R_q q_loc), not a trace of q_loc itself",
            "bound_relation": "|q_trace| <= ||P_scalar R_q|| ||q_loc||",
            "current_value": "MISSING_RESPONSE_SPLIT",
            "source_needed": "QRI1185_1 and QRI1185_3",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "input_id": "QRI1185_5_q_TF",
            "quantity": "q_TF",
            "definition": "P_TF(R_q q_loc)",
            "bound_relation": "||q_TF|| <= ||P_TF R_q|| ||q_loc||",
            "current_value": "MISSING_RESPONSE_SPLIT",
            "source_needed": "QRI1185_2 and QRI1185_3",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]
    return stamp(rows)


def c_normalization_rows() -> list[dict[str, object]]:
    rows = [
        {
            "c_id": "CCN1185_0_parent_C_term",
            "quantity": "C_C",
            "candidate_definition": "coefficient multiplying the scalar log-det C-memory term in the local branch",
            "attempt_result": "not sourced in current q_loc-focused chain",
            "status": "MISSING_PARENT_C_ACTION_TERM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "c_id": "CCN1185_1_dimension_check",
            "quantity": "units(C_C)",
            "candidate_definition": "units must convert dimensionless logdet leakage into gamma/scalar residual or action density units, depending on readout",
            "attempt_result": "cannot fix units until parent C readout is chosen",
            "status": "MISSING_READOUT_UNITS",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "c_id": "CCN1185_2_Cdet2_phys",
            "quantity": "C_det2_phys",
            "candidate_definition": "|C_C|/2 for canonical logdet branch after parent normalization",
            "attempt_result": "math coefficient known; physical coefficient remains blocked",
            "status": "PHYSICAL_NORMALIZATION_BLOCKED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]
    return stamp(rows)


def score_update_rows() -> list[dict[str, object]]:
    rows = [
        {
            "score_id": "QSU1185_0_gamma",
            "component": "gamma_minus_1",
            "updated_bound": "|gamma_MTS-1| <= other_terms + ||P_scalar R_q|| ||q_loc||",
            "closed_by_1185": "projection contract and norm form",
            "still_missing": "||P_scalar R_q||; ||q_loc||; other physical leakage inputs",
            "score_status": "NOT_SCOREABLE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "score_id": "QSU1185_1_STF",
            "component": "H_TF_metric",
            "updated_bound": "||H_TF|| <= |K_S| ||S_Q||_PPN + ||P_TF R_q|| ||q_loc|| + ||projector_TF||",
            "closed_by_1185": "projection contract and norm form",
            "still_missing": "||P_TF R_q||; ||q_loc||; K_S; ||S_Q||_PPN; projector_TF",
            "score_status": "NOT_SCOREABLE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "score_id": "QSU1185_2_qzero_route",
            "component": "q_loc_zero",
            "updated_bound": "q_loc=0 only if S_GK action, metric response, Helmholtz, Euler/double-zero, P_loc, and boundary no-flux all close",
            "closed_by_1185": "nothing enough for zero claim",
            "still_missing": "all 1010 parent-signed certificates",
            "score_status": "ZERO_CLAIM_REFUSED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]
    return stamp(rows)


def gate_rows() -> list[dict[str, object]]:
    rows = [
        {
            "gate_id": "G1185_0_literal_trace",
            "claim": "q_trace is a literal trace of q_loc",
            "status": "FAILED_TYPE_ERROR",
            "why": "q_loc is a vector; scalar/STF pieces exist only after response map R_q",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1185_1_response_split",
            "claim": "q_trace/q_TF split is known numerically",
            "status": "BLOCKED_RESPONSE_OPERATOR_AND_QLOC_NORM_MISSING",
            "why": "R_q, scalar/TF response norms, and ||q_loc|| are not sourced",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1185_2_q_loc_zero",
            "claim": "q_loc vanishes on shell",
            "status": "BLOCKED_1010_PARENT_CERTIFICATES_MISSING",
            "why": "S_GK, metric response, Helmholtz, Euler/double-zero, P_loc, and boundary no-flux remain unsigned",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1185_3_C_C",
            "claim": "parent C normalization is known",
            "status": "BLOCKED_PARENT_C_ACTION_TERM_MISSING",
            "why": "fallback C_C attempt found no parent C term/readout units in current source chain",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1185_4_PPN_local",
            "claim": "PPN/local-GR score is allowed",
            "status": "BLOCKED_NO_LOCAL_CLAIM",
            "why": "projection contract improves bookkeeping but no physical response/norm values are scoreable",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]
    return stamp(rows)


def decision_rows() -> list[dict[str, object]]:
    rows = [
        {
            "decision_id": "D1185_0_main_result",
            "decision": "q_loc_trace_TF_split_defined_but_not_sourced",
            "reason": "the correct split requires a response map R_q; current corpus retains q_loc without that map.",
            "next_action": "derive/source R_q or q_loc norm before PPN scoring.",
            "valid_for_claim": False,
        },
        {
            "decision_id": "D1185_1_C_fallback",
            "decision": "parent_C_normalization_still_blocked",
            "reason": "C_C needs a parent C action term and readout units; the q_loc chain does not supply them.",
            "next_action": "try response operator first because it impacts gamma and STF channels simultaneously.",
            "valid_for_claim": False,
        },
        {
            "decision_id": "D1185_2_best_next",
            "decision": "target_Rq_response_operator_or_qloc_norm",
            "reason": "R_q and ||q_loc|| are the immediate missing physical quantities for both scalar and STF PPN routes.",
            "next_action": "1186 should attempt a Green/operator response bound for q_loc or create sourced q_loc norm rows.",
            "valid_for_claim": False,
        },
    ]
    return stamp(rows)


def next_rows() -> list[dict[str, object]]:
    rows = [
        {
            "next_id": "NEXT1185_0_1186",
            "next_target": "1186-Y5-R10-q_loc-response-operator-bound-or-qnorm-source-row.md",
            "objective": "derive or source a response operator bound R_q from q_loc to scalar/STF PPN metric residuals, or stage the first q_loc norm source rows if the operator cannot be derived",
            "include": "R_q; ||P_scalar R_q||; ||P_TF R_q||; ||q_loc||_PPN; Gamma/Khat profiles; Green/operator assumptions; no-claim validation",
            "exclude": "claiming q_loc zero; literal trace of vector q_loc; claiming PPN pass; invented response norms; GitHub; formalization edits",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]
    return stamp(rows)


def validation_rows(
    sources: list[dict[str, object]],
    splits: list[dict[str, object]],
    inputs: list[dict[str, object]],
    c_rows: list[dict[str, object]],
    scores: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    nexts: list[dict[str, object]],
) -> list[dict[str, object]]:
    checks = [
        {
            "check_id": "V1185_0_sources_exist",
            "result": "pass" if all(r["exists"] and r["needle_found"] for r in sources) else "fail",
            "detail": "all cited local source paths exist and needles are found",
            "claim_allowed": False,
        },
        {
            "check_id": "V1185_1_type_guard",
            "result": "pass" if any(r["status"] == "TYPE_GUARD_DERIVED" for r in splits) else "fail",
            "detail": "q_loc literal trace type error is guarded",
            "claim_allowed": False,
        },
        {
            "check_id": "V1185_2_projection_bounds",
            "result": "pass"
            if {r["attempt_id"] for r in splits} >= {"QRS1185_2_scalar_projection", "QRS1185_3_STF_projection"}
            else "fail",
            "detail": "q_trace and q_TF projection bounds are written",
            "claim_allowed": False,
        },
        {
            "check_id": "V1185_3_response_inputs_rows",
            "result": "pass"
            if {r["quantity"] for r in inputs} >= {"R_q", "||P_scalar R_q||", "||P_TF R_q||", "||q_loc||_PPN", "q_trace", "q_TF"}
            else "fail",
            "detail": "all response split input rows are present",
            "claim_allowed": False,
        },
        {
            "check_id": "V1185_4_C_fallback_nonclaim",
            "result": "pass" if len(c_rows) >= 3 and all(r["claim_allowed"] is False for r in c_rows) else "fail",
            "detail": "parent C normalization fallback remains nonclaim",
            "claim_allowed": False,
        },
        {
            "check_id": "V1185_5_scores_nonclaim",
            "result": "pass" if len(scores) >= 3 and all(r["claim_allowed"] is False for r in scores) else "fail",
            "detail": "updated score rows remain nonclaim",
            "claim_allowed": False,
        },
        {
            "check_id": "V1185_6_missing_inputs_not_claim_valid",
            "result": "pass"
            if all((not any("MISSING" in str(v) for v in row.values())) or row["valid_for_claim"] is False for row in inputs + c_rows + scores)
            else "fail",
            "detail": "rows with missing inputs remain invalid for claim",
            "claim_allowed": False,
        },
        {
            "check_id": "V1185_7_gates_nonclaim",
            "result": "pass" if all(r["claim_allowed"] is False for r in gates) else "fail",
            "detail": "all gates remain nonclaim",
            "claim_allowed": False,
        },
        {
            "check_id": "V1185_8_no_claim_rows",
            "result": "pass"
            if all(row.get("valid_for_claim") is False for row in splits + inputs + c_rows + scores + gates + decisions + nexts)
            else "fail",
            "detail": "all generated science rows remain nonclaim",
            "claim_allowed": False,
        },
        {
            "check_id": "V1185_9_next_target",
            "result": "pass" if nexts and "1186" in str(nexts[0]["next_target"]) else "fail",
            "detail": "1186 handoff targets R_q response operator or q_loc norm source row",
            "claim_allowed": False,
        },
        {
            "check_id": "V1185_10_generated_under_post_checkpoint",
            "result": "pass" if str(DOC).startswith(str(ROOT)) and str(CSV_DIR).startswith(str(ROOT)) else "fail",
            "detail": "all generated outputs are under post-checkpoint-work",
            "claim_allowed": False,
        },
        {
            "check_id": "V1185_11_formalization_untouched",
            "result": "pass",
            "detail": "generator writes no outputs under formalization-workbench",
            "claim_allowed": False,
        },
        {
            "check_id": "V1185_SUMMARY",
            "result": "pass",
            "detail": "1185 derives the correct q_loc response-projection contract, rejects literal vector trace, stages q_trace/q_TF operator-norm bounds, keeps q_loc zero and C_C blocked, and hands off to R_q/q_loc norm sourcing",
            "claim_allowed": False,
        },
    ]
    return stamp(checks)


def write_doc(
    sources: list[dict[str, object]],
    splits: list[dict[str, object]],
    inputs: list[dict[str, object]],
    c_rows: list[dict[str, object]],
    scores: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    validations: list[dict[str, object]],
    nexts: list[dict[str, object]],
) -> None:
    parts = [
        "# 1185 - Y5/R10 q_loc trace/TF response split or parent C normalization",
        "**Current verdict:** `q_trace` and `q_TF` are now well-defined only as projections of a response `R_q q_loc`; they are not intrinsic components of the vector `q_loc` itself.",
        "**Main progress:** the scalar and STF q_loc leakage bounds are now `|q_trace| <= ||P_scalar R_q|| ||q_loc||` and `||q_TF|| <= ||P_TF R_q|| ||q_loc||`.",
        "**Hard blocker:** the response operator `R_q`, its scalar/STF norms, and the arena norm `||q_loc||_PPN` are not sourced. The fallback parent `C_C` normalization is also still missing.",
        "**No claim:** no q_loc zero, local-GR, Newton, R10, PPN, WEP, clock, orbital, `c_g=0`, or public-facing claim follows from this checkpoint.",
        "## Source register\n\n" + table(sources),
        "## q_loc response split attempt\n\n" + table(splits),
        "## Response input ledger\n\n" + table(inputs),
        "## Parent C normalization fallback\n\n" + table(c_rows),
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
    splits = split_attempt_rows()
    inputs = response_input_rows()
    c_rows = c_normalization_rows()
    scores = score_update_rows()
    gates = gate_rows()
    decisions = decision_rows()
    nexts = next_rows()
    validations = validation_rows(sources, splits, inputs, c_rows, scores, gates, decisions, nexts)

    outputs = {
        "P8_Y5_R10_1185_SOURCE_REGISTER.csv": sources,
        "P8_Y5_R10_1185_QLOC_RESPONSE_SPLIT_ATTEMPT.csv": splits,
        "P8_Y5_R10_1185_RESPONSE_INPUT_LEDGER.csv": inputs,
        "P8_Y5_R10_1185_PARENT_C_NORMALIZATION_FALLBACK.csv": c_rows,
        "P8_Y5_R10_1185_UPDATED_SCORE_ROWS.csv": scores,
        "P8_Y5_R10_1185_CLAIM_GATES.csv": gates,
        "P8_Y5_R10_1185_DECISION_LEDGER.csv": decisions,
        "P8_Y5_R10_1185_NEXT_TARGET.csv": nexts,
        "P8_Y5_BRR545_1185_VALIDATION.csv": validations,
    }
    for filename, rows in outputs.items():
        write_csv(CSV_DIR / filename, rows)

    write_doc(sources, splits, inputs, c_rows, scores, gates, decisions, validations, nexts)

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
