from __future__ import annotations

import csv
from pathlib import Path


PACK_ID = "P8_Y5_R10_1375"
TITLE = "1375-Y5-R10-RAB-transition-input-row-validator-or-Kconn-first-bound"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
VALIDATOR_RULES_PATH = OUT_DIR / f"{PACK_ID}_TRANSITION_INPUT_VALIDATOR_RULES.csv"
VALIDATOR_RESULTS_PATH = OUT_DIR / f"{PACK_ID}_TRANSITION_INPUT_VALIDATOR_RESULTS.csv"
KCONN_BOUND_PATH = OUT_DIR / f"{PACK_ID}_KCONN_FIRST_BOUND_CONTRACT.csv"
RUNNER_FEED_PATH = OUT_DIR / f"{PACK_ID}_RUNNER_FEED_UPDATE.csv"
CLAIM_GATE_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATE.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1375_VALIDATION.csv"


def source_path(relative_path: str) -> Path:
    path = Path(relative_path)
    if path.is_absolute():
        return path
    return ROOT / path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def cell(value: object) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def table(headers: list[str], rows: list[dict[str, object]]) -> str:
    out = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        out.append("| " + " | ".join(cell(row.get(header, "")) for header in headers) + " |")
    return "\n".join(out)


def mark_nonclaim(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    for row in rows:
        row["valid_for_claim"] = False
        row["claim_allowed"] = False
    return rows


def source_register() -> list[dict[str, object]]:
    rows = [
        {
            "source_id": "SRC1375_0_1374_doc",
            "source_path": "1374-Y5-R10-RAB-Qalg-Qtrans-first-fill-or-Kcdb-subchannel-bound.md",
            "required_anchor": "NEXT1374_0_1375",
            "purpose": "1374 handoff to transition validator or K_conn first bound.",
        },
        {
            "source_id": "SRC1375_1_1374_next",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1374_NEXT_TARGET.csv",
            "required_anchor": "NEXT1374_0_1375",
            "purpose": "machine-readable 1375 target.",
        },
        {
            "source_id": "SRC1375_2_1374_qalg_qtrans",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1374_QALG_QTRANS_FIRST_FILL.csv",
            "required_anchor": "QQF1374_4_Qalg_Qtrans_verdict",
            "purpose": "symbolic Q_alg/Q_trans fills and toy quarantine.",
        },
        {
            "source_id": "SRC1375_3_1374_kcdb",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1374_KCDB_SUBCHANNEL_BOUND_CONTRACTS.csv",
            "required_anchor": "KCS1374_0_K_conn",
            "purpose": "K_conn subchannel first contract.",
        },
        {
            "source_id": "SRC1375_4_799_input_template",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_799_TRANSITION_CALCULATOR_INPUT_TEMPLATE.csv",
            "required_anchor": "template_missing_parent_values",
            "purpose": "transition input rows: missing template and toy nonclaim row.",
        },
        {
            "source_id": "SRC1375_5_799_smoke",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_799_TRANSITION_CALCULATOR_SMOKE_OUTPUT.csv",
            "required_anchor": "toy_strong_support_nonclaim",
            "purpose": "transition calculator output rows and symbolic gate.",
        },
        {
            "source_id": "SRC1375_6_799_standalone",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_799_TRANSITION_CALCULATOR_STANDALONE_CHECK.csv",
            "required_anchor": "toy_strong_support_nonclaim",
            "purpose": "standalone cross-check of transition calculator output.",
        },
        {
            "source_id": "SRC1375_7_802_shell",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_802_TRANSITION_SHELL_OBSTRUCTION.csv",
            "required_anchor": "TS802_0_direct_projection",
            "purpose": "transition shell direct-projection obstruction.",
        },
        {
            "source_id": "SRC1375_8_803_anticheat",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_803_TRANSITION_SHELL_ANTI_CHEAT_BOUND.csv",
            "required_anchor": "AC803_0_required_shell_suppression",
            "purpose": "anti-cheat shell suppression refusal.",
        },
        {
            "source_id": "SRC1375_9_1288_derivative",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1288_KMETRIC_DERIVATIVE_TERM_BLOCKER.csv",
            "required_anchor": "KMR1288_2_derivative_terms",
            "purpose": "derivative/connection terms missing from Kmetric.",
        },
        {
            "source_id": "SRC1375_10_1288_response_matrix",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1288_RESPONSE_MATRIX_REQUIREMENTS.csv",
            "required_anchor": "RMR1288_7_response_verdict",
            "purpose": "local response matrix still missing.",
        },
        {
            "source_id": "SRC1375_11_776_response",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_776_KGAMMA_METRIC_RESPONSE_LEDGER.csv",
            "required_anchor": "KGL776_2_derivative_terms",
            "purpose": "connection/derivative/projector metric-response source.",
        },
        {
            "source_id": "SRC1375_12_1291_cdb",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1291_CHAIN_KERNEL_RESIDUAL_BOUND_LEDGER.csv",
            "required_anchor": "KRB1291_2_cdb_bound",
            "purpose": "CDB residual bound form.",
        },
    ]
    for row in rows:
        path = source_path(str(row["source_path"]))
        row["exists"] = path.exists()
        row["anchor_found"] = path.exists() and str(row["required_anchor"]) in read_text(path)
    return mark_nonclaim(rows)


def validator_rules_rows() -> list[dict[str, object]]:
    return mark_nonclaim(
        [
            {
                "rule_id": "TVR1375_0_no_missing_parent_inputs",
                "field_group": "transition parent values",
                "rule": "reject if any required Q_alg/Q_trans field is MISSING_PARENT_INPUT or MISSING_*",
                "reason": "Q_alg/Q_trans scoring requires parent values for U_B, powers, amplitudes, lengths, A_ref, and limits.",
                "failure_status": "BLOCKED_MISSING_PARENT_INPUTS",
            },
            {
                "rule_id": "TVR1375_1_no_toy_rows",
                "field_group": "case_id/source_path",
                "rule": "reject if case_id starts with toy_ or source_path is toy_nonclaim_no_physical_source",
                "reason": "toy rows test calculator wiring only and are not physics evidence.",
                "failure_status": "REFUSED_TOY_NONCLAIM",
            },
            {
                "rule_id": "TVR1375_2_claim_flags",
                "field_group": "valid_for_claim/claim_allowed",
                "rule": "reject if claim flags are true while any source, parent value, or anti-cheat gate is missing",
                "reason": "symbolic or toy values cannot promote local-GR/PPN/R10 claims.",
                "failure_status": "REFUSED_INVALID_CLAIM_FLAG",
            },
            {
                "rule_id": "TVR1375_3_shell_guard",
                "field_group": "transition shell",
                "rule": "reject local pass if direct shell projection is ignored or hidden by generic width/U_B suppression",
                "reason": "802/803 reject generic shell hiding and require exact cancellation/projector quarantine or explicit shell bound.",
                "failure_status": "BLOCKED_SHELL_ANTI_CHEAT",
            },
            {
                "rule_id": "TVR1375_4_required_fields",
                "field_group": "source-ready transition row",
                "rule": "require A_ref,F2,A_S,A_L,A_T,A_B,b_mem,U_B,pS,pL,pT,pB,L0,L_tr,source_path,source_anchor,units",
                "reason": "these fields are the minimum to evaluate Q_alg/Q_trans formulas from 1374.",
                "failure_status": "BLOCKED_REQUIRED_FIELD_ABSENT",
            },
        ]
    )


def validator_results_rows() -> list[dict[str, object]]:
    input_rows = read_csv_rows(source_path("source-intake/mts_residuals/P8_Y5_R10_799_TRANSITION_CALCULATOR_INPUT_TEMPLATE.csv"))
    output_rows = read_csv_rows(source_path("source-intake/mts_residuals/P8_Y5_R10_799_TRANSITION_CALCULATOR_SMOKE_OUTPUT.csv"))
    by_case_output = {row["case_id"]: row for row in output_rows}
    results: list[dict[str, object]] = []

    for row in input_rows:
        case_id = row.get("case_id", "")
        output = by_case_output.get(case_id, {})
        missing_fields = [
            key
            for key, value in row.items()
            if key
            in {
                "U_B",
                "pS",
                "pL",
                "pT",
                "pB",
                "L_cg",
                "L_tr",
                "F2",
                "A_S",
                "A_L",
                "A_T",
                "A_B",
                "b_mem",
                "epsilon_q_limit",
                "epsilon_N_limit",
            }
            and str(value).startswith("MISSING")
        ]
        is_toy = case_id.startswith("toy_") or row.get("source_path") == "toy_nonclaim_no_physical_source"
        numeric_ready = output.get("numeric_ready", "false")
        passes_symbolic_gate = output.get("passes_symbolic_gate", "false")
        if missing_fields:
            verdict = "BLOCKED_MISSING_PARENT_INPUTS"
            reason = "missing_fields:" + ";".join(missing_fields)
        elif is_toy:
            verdict = "REFUSED_TOY_NONCLAIM"
            reason = "toy row cannot become evidence; source_path=" + str(row.get("source_path", ""))
        elif str(row.get("valid_for_claim", "")).lower() != "true":
            verdict = "REFUSED_NOT_VALID_FOR_CLAIM"
            reason = "row valid_for_claim is not true"
        elif str(passes_symbolic_gate).lower() != "true":
            verdict = "REFUSED_SYMBOLIC_GATE_FALSE"
            reason = "calculator output does not pass symbolic gate"
        else:
            verdict = "SOURCE_READY_NONCLAIM_INPUT_CANDIDATE"
            reason = "all required fields present; still requires separate claim review"

        results.append(
            {
                "case_id": case_id,
                "row_status": row.get("row_status", ""),
                "numeric_ready": numeric_ready,
                "passes_symbolic_gate": passes_symbolic_gate,
                "validator_verdict": verdict,
                "reason": reason,
                "Q_alg_formula": "A_ref^-1 |F2| A_S^2 U_B^(2pS)/(L0^2 L_tr)",
                "Q_trans_formula": "A_ref^-1[A_L U_B^pL/(L0^2 L_tr)+A_T U_B^pT/L_tr+A_B U_B^pB/(L0^2 L_tr)+|b_mem|A_S^2 U_B^(2pS)/L_tr^3]",
                "source_path": row.get("source_path", ""),
            }
        )

    results.append(
        {
            "case_id": "VALIDATOR1375_VERDICT",
            "row_status": "aggregate_transition_inputs",
            "numeric_ready": "false",
            "passes_symbolic_gate": "false",
            "validator_verdict": "NO_SOURCE_READY_TRANSITION_ROW_FOUND",
            "reason": "available rows are missing-parent template or toy/nonclaim rows",
            "Q_alg_formula": "symbolic only",
            "Q_trans_formula": "symbolic only",
            "source_path": "aggregate_799_input_and_output_rows",
        }
    )
    return mark_nonclaim(results)


def kconn_bound_rows() -> list[dict[str, object]]:
    return mark_nonclaim(
        [
            {
                "bound_id": "KCB1375_0_owner",
                "component": "K_conn_norm",
                "bound_contract": "K_conn is the norm of derivative/connection metric-response terms in delta(S_Gamma)/delta g after the algebraic volume/m/L chain is separated.",
                "derived_status": "OWNER_SHARPENED",
                "required_inputs": "explicit derivative operator; connection variation convention; integration-by-parts convention",
                "source_paths": "source-intake/mts_residuals/P8_Y5_R10_1288_KMETRIC_DERIVATIVE_TERM_BLOCKER.csv;source-intake/mts_residuals/P8_Y5_R10_776_KGAMMA_METRIC_RESPONSE_LEDGER.csv",
            },
            {
                "bound_id": "KCB1375_1_decomposition",
                "component": "K_conn_norm",
                "bound_contract": "K_conn_norm <= K_nabla_norm + K_hodge_norm + K_ibp_bulk_norm + K_ibp_edge_norm",
                "derived_status": "SUBDECOMPOSITION_DERIVED",
                "required_inputs": "delta_g nabla term; delta_g Hodge/star/coframe term; bulk integration-by-parts term; derivative edge term",
                "source_paths": "source-intake/mts_residuals/P8_Y5_R10_776_KGAMMA_METRIC_RESPONSE_LEDGER.csv",
            },
            {
                "bound_id": "KCB1375_2_operator_norm_bound",
                "component": "K_conn_norm",
                "bound_contract": "K_conn_norm <= N_conn,nabla ||S_der||_D + N_conn,star ||S_star||_D + N_conn,ibp ||S_ibp||_D + N_conn,edge ||B_der||_{partial D}",
                "derived_status": "FIRST_OPERATOR_NORM_BOUND_WRITTEN",
                "required_inputs": "N_conn,nabla;N_conn,star;N_conn,ibp;N_conn,edge;S_der;S_star;S_ibp;B_der;domain norm",
                "source_paths": "source-intake/mts_residuals/P8_Y5_R10_1288_KMETRIC_DERIVATIVE_TERM_BLOCKER.csv;source-intake/mts_residuals/P8_Y5_R10_1291_CHAIN_KERNEL_RESIDUAL_BOUND_LEDGER.csv",
            },
            {
                "bound_id": "KCB1375_3_fixed_L0_double_zero_reduction",
                "component": "K_conn source scale",
                "bound_contract": "under fixed L0 and strict double-zero, derivative source amplitudes may be bounded by the same Delta_m, Delta_grad_m, and transition-support data used by Q_alg/Q_trans, but derivative operators are not zero by that fact alone",
                "derived_status": "REDUCED_TO_TRANSITION_AND_OPERATOR_INPUTS",
                "required_inputs": "Delta_m;Delta_grad_m;transition support powers;operator norms;edge/no-flux terms",
                "source_paths": "source-intake/mts_residuals/P8_Y5_R10_1374_QALG_QTRANS_FIRST_FILL.csv;source-intake/mts_residuals/P8_Y5_R10_798_TRANSITION_CURRENT_BOUND_CONTRACT.csv",
            },
            {
                "bound_id": "KCB1375_4_runner_formula",
                "component": "Q_cdb contribution from K_conn",
                "bound_contract": "Q_conn <= A_ref^-1 N_div K_conn_norm, with K_conn_norm supplied by KCB1375_2",
                "derived_status": "RUNNER_FEED_READY_SYMBOLIC",
                "required_inputs": "A_ref;N_div;all KCB1375_2 operator/input norms",
                "source_paths": "source-intake/mts_residuals/P8_Y5_R10_1374_KCDB_SUBCHANNEL_BOUND_CONTRACTS.csv",
            },
            {
                "bound_id": "KCB1375_5_verdict",
                "component": "K_conn first bound",
                "bound_contract": "K_conn has a sharper operator/norm bound contract, but no numeric or theorem-zero value.",
                "derived_status": "BOUND_CONTRACT_READY_NUMERIC_VALUES_MISSING",
                "required_inputs": "operator norms; source tensors; boundary term; domain/gauge/frame; A_ref/N_div",
                "source_paths": "aggregate_KCB1375_0_to_KCB1375_4",
            },
        ]
    )


def runner_feed_rows() -> list[dict[str, object]]:
    return mark_nonclaim(
        [
            {
                "feed_id": "RUF1375_0_transition_validator",
                "runner_field": "transition_input_rows",
                "feed_update": "validator refuses missing-parent and toy rows before Q_alg/Q_trans scoring",
                "status": "VALIDATOR_READY_NO_SOURCE_READY_ROW",
                "blocks_claim_because": "current rows are template_missing_parent_values or toy_strong_support_nonclaim",
            },
            {
                "feed_id": "RUF1375_1_Q_alg_Q_trans",
                "runner_field": "Q_alg_Q_trans",
                "feed_update": "retain 1374 symbolic formulas; do not evaluate numeric values",
                "status": "SYMBOLIC_ONLY",
                "blocks_claim_because": "A_ref, U_B, powers, amplitudes, L0, and L_tr are not source-filled",
            },
            {
                "feed_id": "RUF1375_2_K_conn",
                "runner_field": "Q_conn",
                "feed_update": "Q_conn <= A_ref^-1 N_div [N_conn,nabla||S_der||+N_conn,star||S_star||+N_conn,ibp||S_ibp||+N_conn,edge||B_der||]",
                "status": "SYMBOLIC_OPERATOR_BOUND_READY",
                "blocks_claim_because": "operator norms and source tensors are missing",
            },
            {
                "feed_id": "RUF1375_3_refusal",
                "runner_field": "refusal_gates",
                "feed_update": "refuse toy rows, proxy rows, missing operator norms, missing source anchors, or claim flags on symbolic rows",
                "status": "REFUSAL_GATES_READY",
                "blocks_claim_because": "prevents fake numeric/local-GR pass",
            },
        ]
    )


def claim_gate_rows() -> list[dict[str, object]]:
    return mark_nonclaim(
        [
            {
                "gate_id": "GATE1375_0_transition_validator",
                "gate": "strict transition input validator exists",
                "status": "PASS_VALIDATOR_READY",
                "reason": "missing-parent, toy, shell, and claim-flag refusal rules are explicit.",
            },
            {
                "gate_id": "GATE1375_1_source_ready_transition_row",
                "gate": "current transition rows include a source-ready input row",
                "status": "BLOCKED_NO_SOURCE_READY_ROW",
                "reason": "available rows are missing-parent template or toy/nonclaim rows.",
            },
            {
                "gate_id": "GATE1375_2_Kconn_bound",
                "gate": "K_conn receives sharper first bound contract",
                "status": "PASS_SYMBOLIC_OPERATOR_BOUND",
                "reason": "K_conn is decomposed into derivative/star/IBP/edge operator-norm pieces.",
            },
            {
                "gate_id": "GATE1375_3_Kconn_numeric",
                "gate": "K_conn bound can be evaluated numerically",
                "status": "BLOCKED_OPERATOR_VALUES_MISSING",
                "reason": "operator norms, source tensors, edge term, and domain/gauge are missing.",
            },
            {
                "gate_id": "GATE1375_4_local_claim",
                "gate": "local GR / PPN / R10 pass can be claimed",
                "status": "BLOCKED_NO_CLAIM",
                "reason": "no source-ready transition row and no numeric/theorem-zero K_conn bound.",
            },
        ]
    )


def decision_rows() -> list[dict[str, object]]:
    return mark_nonclaim(
        [
            {
                "decision_id": "DEC1375_0_transition_status",
                "decision": "do not use current transition rows for Q_alg/Q_trans scoring",
                "why": "validator finds only missing-parent and toy rows",
                "next_action": "either source real parent transition values or keep transition lane symbolic",
            },
            {
                "decision_id": "DEC1375_1_Kconn_status",
                "decision": "use K_conn operator-bound contract as the active fallback",
                "why": "it sharpens the CDB blocker without pretending derivative/connection terms vanish",
                "next_action": "try to fill N_conn,* operator norms or derive a connection no-response theorem",
            },
            {
                "decision_id": "DEC1375_2_next_best_route",
                "decision": "next target should attempt K_conn operator norm fill before broader CDB channels",
                "why": "K_conn is the most local tensor-calculus piece; domain/boundary routes have stronger no-go ledgers",
                "next_action": "derive/source derivative operator, local gauge/frame, IBP convention, and edge term",
            },
        ]
    )


def next_rows() -> list[dict[str, object]]:
    return mark_nonclaim(
        [
            {
                "next_id": "NEXT1375_0_1376",
                "next_doc": "1376-Y5-R10-RAB-Kconn-operator-norm-fill-or-transition-parent-source-acquisition.md",
                "next_script": "scripts/Y5_R10_RAB_Kconn_operator_norm_fill_or_transition_parent_source_acquisition.py",
                "task": "attempt to fill K_conn operator norms from derivative/connection metric-response conventions; if not possible, create a transition parent-source acquisition table for U_B, powers, amplitudes, L0, L_tr, and A_ref",
                "success_condition": "either K_conn receives source-backed symbolic/numeric operator-norm rows, or transition parent inputs receive acquisition rows with source requirements and refusal gates",
                "do_not_claim": "local GR;PPN pass;R10 pass;q_loc=0;GitHub-ready result",
            }
        ]
    )


def csv_parse_check(paths: list[Path]) -> tuple[bool, str]:
    details = []
    ok = True
    for path in paths:
        try:
            rows = read_csv_rows(path)
            details.append(f"{path.name}:{len(rows)}")
        except Exception as exc:
            ok = False
            details.append(f"{path.name}:ERROR:{exc}")
    return ok, "; ".join(details)


def validation_rows(
    sources: list[dict[str, object]],
    rules: list[dict[str, object]],
    results: list[dict[str, object]],
    kconn: list[dict[str, object]],
    runner_feed: list[dict[str, object]],
    gates: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    all_sources_ok = all(row["exists"] and row["anchor_found"] for row in sources)
    all_nonclaim = all(
        not bool(row.get("valid_for_claim")) and not bool(row.get("claim_allowed"))
        for row in sources + rules + results + kconn + runner_feed + gates
    )
    validator_ready = len(rules) >= 5 and any(row["rule_id"] == "TVR1375_1_no_toy_rows" for row in rules)
    no_ready_row = any(row["case_id"] == "VALIDATOR1375_VERDICT" and row["validator_verdict"] == "NO_SOURCE_READY_TRANSITION_ROW_FOUND" for row in results)
    toy_refused = any(row["validator_verdict"] == "REFUSED_TOY_NONCLAIM" for row in results)
    kconn_ready = any(row["bound_id"] == "KCB1375_2_operator_norm_bound" and row["derived_status"] == "FIRST_OPERATOR_NORM_BOUND_WRITTEN" for row in kconn)
    runner_refusal = any(row["feed_id"] == "RUF1375_3_refusal" and row["status"] == "REFUSAL_GATES_READY" for row in runner_feed)
    local_claim_blocked = any(row["gate_id"] == "GATE1375_4_local_claim" and row["status"] == "BLOCKED_NO_CLAIM" for row in gates)
    csv_ok, csv_details = csv_parse_check(csv_paths)

    rows = [
        {
            "validation_id": "VAL1375_0_sources",
            "check": "every cited local source path exists and anchor is found",
            "status": "PASS" if all_sources_ok else "FAIL",
            "details": "; ".join(f"{row['source_id']} exists={row['exists']} anchor={row['anchor_found']}" for row in sources),
        },
        {
            "validation_id": "VAL1375_1_validator",
            "check": "strict transition validator exists and refuses current rows",
            "status": "PASS" if validator_ready and no_ready_row and toy_refused else "FAIL",
            "details": "missing-parent and toy rows are refused; no source-ready row found",
        },
        {
            "validation_id": "VAL1375_2_Kconn_bound",
            "check": "K_conn receives first operator/norm bound contract",
            "status": "PASS" if kconn_ready else "FAIL",
            "details": "KCB1375_2 decomposes derivative/star/IBP/edge pieces",
        },
        {
            "validation_id": "VAL1375_3_runner_refusal",
            "check": "runner feed keeps refusal gates active",
            "status": "PASS" if runner_refusal else "FAIL",
            "details": "RUF1375_3 blocks toy/proxy/missing/operator rows",
        },
        {
            "validation_id": "VAL1375_4_no_claim_rows",
            "check": "all new rows keep valid_for_claim=false and claim_allowed=false",
            "status": "PASS" if all_nonclaim else "FAIL",
            "details": "1375 is validation/bound scaffolding, not a local-GR or PPN pass",
        },
        {
            "validation_id": "VAL1375_5_local_claim_blocked",
            "check": "local GR / PPN / R10 claim remains blocked",
            "status": "PASS" if local_claim_blocked else "FAIL",
            "details": "GATE1375_4_local_claim remains BLOCKED_NO_CLAIM",
        },
        {
            "validation_id": "VAL1375_6_csv_parse",
            "check": "all generated CSVs parse cleanly",
            "status": "PASS" if csv_ok else "FAIL",
            "details": csv_details,
        },
    ]
    overall_ok = all(row["status"] == "PASS" for row in rows)
    rows.append(
        {
            "validation_id": "VAL1375_7_overall",
            "check": "overall 1375 validation",
            "status": "PASS" if overall_ok else "FAIL",
            "details": "1375 refuses current transition rows and adds a sharper symbolic K_conn operator-bound contract.",
        }
    )
    return rows


def write_doc(
    sources: list[dict[str, object]],
    rules: list[dict[str, object]],
    results: list[dict[str, object]],
    kconn: list[dict[str, object]],
    runner_feed: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_targets: list[dict[str, object]],
    validations: list[dict[str, object]],
) -> None:
    text = f"""# {TITLE}

**Current verdict:** 1375 finds no source-ready transition input row. The current transition rows are either missing parent values or explicitly toy/nonclaim, so `Q_alg` and `Q_trans` remain symbolic. No local-GR, PPN, or R10 pass is allowed.

**Main progress:** the transition validator is now strict and machine-readable: it refuses missing parent inputs, toy rows, hidden transition shells, proxy rows, and claim flags on symbolic data. Since the transition lane has no real row yet, 1375 falls through to the useful fallback: a sharper `K_conn` operator/norm bound.

**K_conn progress:** `K_conn_norm` is decomposed into derivative, Hodge/coframe, integration-by-parts bulk, and derivative edge pieces: `K_conn_norm <= N_conn,nabla ||S_der|| + N_conn,star ||S_star|| + N_conn,ibp ||S_ibp|| + N_conn,edge ||B_der||`. Still symbolic, but no longer a fog word.

## Source Register

{table(["source_id", "source_path", "required_anchor", "exists", "anchor_found", "purpose", "valid_for_claim", "claim_allowed"], sources)}

## Transition Input Validator Rules

{table(["rule_id", "field_group", "rule", "reason", "failure_status", "valid_for_claim", "claim_allowed"], rules)}

## Transition Input Validator Results

{table(["case_id", "row_status", "numeric_ready", "passes_symbolic_gate", "validator_verdict", "reason", "Q_alg_formula", "Q_trans_formula", "source_path", "valid_for_claim", "claim_allowed"], results)}

## `K_conn` First Bound Contract

{table(["bound_id", "component", "derived_status", "bound_contract", "required_inputs", "source_paths", "valid_for_claim", "claim_allowed"], kconn)}

## Runner Feed Update

{table(["feed_id", "runner_field", "feed_update", "status", "blocks_claim_because", "valid_for_claim", "claim_allowed"], runner_feed)}

## Claim Gates

{table(["gate_id", "gate", "status", "reason", "valid_for_claim", "claim_allowed"], gates)}

## Decision Ledger

{table(["decision_id", "decision", "why", "next_action", "valid_for_claim", "claim_allowed"], decisions)}

## Next Target

{table(["next_id", "next_doc", "next_script", "task", "success_condition", "do_not_claim", "valid_for_claim", "claim_allowed"], next_targets)}

## Validation

{table(["validation_id", "check", "status", "details"], validations)}
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def main() -> None:
    sources = source_register()
    rules = validator_rules_rows()
    results = validator_results_rows()
    kconn = kconn_bound_rows()
    runner_feed = runner_feed_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_targets = next_rows()

    write_csv(SOURCE_REGISTER_PATH, sources)
    write_csv(VALIDATOR_RULES_PATH, rules)
    write_csv(VALIDATOR_RESULTS_PATH, results)
    write_csv(KCONN_BOUND_PATH, kconn)
    write_csv(RUNNER_FEED_PATH, runner_feed)
    write_csv(CLAIM_GATE_PATH, gates)
    write_csv(DECISION_PATH, decisions)
    write_csv(NEXT_PATH, next_targets)

    csv_paths = [
        SOURCE_REGISTER_PATH,
        VALIDATOR_RULES_PATH,
        VALIDATOR_RESULTS_PATH,
        KCONN_BOUND_PATH,
        RUNNER_FEED_PATH,
        CLAIM_GATE_PATH,
        DECISION_PATH,
        NEXT_PATH,
    ]
    validations = validation_rows(sources, rules, results, kconn, runner_feed, gates, csv_paths)
    write_csv(VALIDATION_PATH, validations)
    write_doc(sources, rules, results, kconn, runner_feed, gates, decisions, next_targets, validations)

    print(f"wrote {DOC_PATH}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"formalization-workbench touched by this script: {FORMALIZATION.exists() and False}")


if __name__ == "__main__":
    main()
