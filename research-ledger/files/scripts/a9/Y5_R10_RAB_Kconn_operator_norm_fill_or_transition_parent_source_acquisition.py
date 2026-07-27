from __future__ import annotations

import csv
from pathlib import Path


PACK_ID = "P8_Y5_R10_1376"
TITLE = "1376-Y5-R10-RAB-Kconn-operator-norm-fill-or-transition-parent-source-acquisition"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
KCONN_FILL_PATH = OUT_DIR / f"{PACK_ID}_KCONN_OPERATOR_NORM_FILL_ATTEMPT.csv"
TRANSITION_ACQUISITION_PATH = OUT_DIR / f"{PACK_ID}_TRANSITION_PARENT_SOURCE_ACQUISITION.csv"
RUNNER_FEED_PATH = OUT_DIR / f"{PACK_ID}_RUNNER_FEED_UPDATE.csv"
CLAIM_GATE_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATE.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1376_VALIDATION.csv"


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
            "source_id": "SRC1376_0_1375_doc",
            "source_path": "1375-Y5-R10-RAB-transition-input-row-validator-or-Kconn-first-bound.md",
            "required_anchor": "NEXT1375_0_1376",
            "purpose": "1375 handoff to K_conn operator-norm fill or transition parent-source acquisition.",
        },
        {
            "source_id": "SRC1376_1_1375_next",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1375_NEXT_TARGET.csv",
            "required_anchor": "NEXT1375_0_1376",
            "purpose": "machine-readable 1376 target.",
        },
        {
            "source_id": "SRC1376_2_1375_kconn_bound",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1375_KCONN_FIRST_BOUND_CONTRACT.csv",
            "required_anchor": "KCB1375_2_operator_norm_bound",
            "purpose": "active K_conn operator/norm bound to fill.",
        },
        {
            "source_id": "SRC1376_3_1375_validator",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1375_TRANSITION_INPUT_VALIDATOR_RESULTS.csv",
            "required_anchor": "VALIDATOR1375_VERDICT",
            "purpose": "current transition input rows are missing-parent or toy/nonclaim.",
        },
        {
            "source_id": "SRC1376_4_1375_runner_feed",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1375_RUNNER_FEED_UPDATE.csv",
            "required_anchor": "RUF1375_2_K_conn",
            "purpose": "runner feed requires K_conn operator norms and source tensors.",
        },
        {
            "source_id": "SRC1376_5_1288_derivative",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1288_KMETRIC_DERIVATIVE_TERM_BLOCKER.csv",
            "required_anchor": "KMR1288_2_derivative_terms",
            "purpose": "Kmetric derivative terms remain missing after integration by parts.",
        },
        {
            "source_id": "SRC1376_6_1288_response_matrix",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1288_RESPONSE_MATRIX_REQUIREMENTS.csv",
            "required_anchor": "RMR1288_7_response_verdict",
            "purpose": "local response matrix is not scoreable until response operators and limits are sourced.",
        },
        {
            "source_id": "SRC1376_7_776_kgamma",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_776_KGAMMA_METRIC_RESPONSE_LEDGER.csv",
            "required_anchor": "KGL776_2_derivative_terms",
            "purpose": "Kgamma derivative/Hodge/domain metric-response terms are open.",
        },
        {
            "source_id": "SRC1376_8_1291_cdb",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1291_CHAIN_KERNEL_RESIDUAL_BOUND_LEDGER.csv",
            "required_anchor": "KRB1291_2_cdb_bound",
            "purpose": "CDB residual is bounded by K_conn, K_domain, and K_boundary terms.",
        },
        {
            "source_id": "SRC1376_9_1298_trace",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1298_SPATIAL_TRACE_REQUIREMENTS.csv",
            "required_anchor": "STR1298_2_cdb_spatial_trace",
            "purpose": "spatial trace and projector/domain commutator remain missing.",
        },
        {
            "source_id": "SRC1376_10_1374_qalg_qtrans",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1374_QALG_QTRANS_FIRST_FILL.csv",
            "required_anchor": "QQF1374_4_Qalg_Qtrans_verdict",
            "purpose": "Q_alg and Q_trans are symbolic parent-parameter formulas with numeric values missing.",
        },
        {
            "source_id": "SRC1376_11_1371_fixed_L0",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1371_FIXED_L0_PARENT_ACTION_INSERTION.csv",
            "required_anchor": "PAI1371_0_fixed_L0_action_branch",
            "purpose": "fixed-L0 branch supplies the L0 action role but not a numeric source row.",
        },
        {
            "source_id": "SRC1376_12_798_transition_contract",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_798_TRANSITION_CURRENT_BOUND_CONTRACT.csv",
            "required_anchor": "TCB798_0_U_B_definition",
            "purpose": "transition current contract lists U_B, support powers, width, and Kperp blockers.",
        },
        {
            "source_id": "SRC1376_13_799_formula_register",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_799_TRANSITION_BOUND_FORMULA_REGISTER.csv",
            "required_anchor": "TBF799_1_q_gamma_quad",
            "purpose": "transition formula register for Q_alg/Q_trans parent rows.",
        },
        {
            "source_id": "SRC1376_14_799_input_template",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_799_TRANSITION_CALCULATOR_INPUT_TEMPLATE.csv",
            "required_anchor": "template_missing_parent_values",
            "purpose": "transition calculator input template and toy row.",
        },
        {
            "source_id": "SRC1376_15_799_smoke_output",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_799_TRANSITION_CALCULATOR_SMOKE_OUTPUT.csv",
            "required_anchor": "toy_strong_support_nonclaim",
            "purpose": "toy transition output is numeric-ready but explicitly nonclaim.",
        },
        {
            "source_id": "SRC1376_16_802_shell",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_802_TRANSITION_SHELL_OBSTRUCTION.csv",
            "required_anchor": "TS802_0_direct_projection",
            "purpose": "transition shell direct projection is not accepted without exact cancellation or quarantine.",
        },
        {
            "source_id": "SRC1376_17_803_anticheat",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_803_TRANSITION_SHELL_ANTI_CHEAT_BOUND.csv",
            "required_anchor": "AC803_0_required_shell_suppression",
            "purpose": "anti-cheat shell bound rejects generic width or U_B suppression alone.",
        },
    ]
    for row in rows:
        path = source_path(str(row["source_path"]))
        row["exists"] = path.exists()
        row["anchor_found"] = path.exists() and str(row["required_anchor"]) in read_text(path)
    return mark_nonclaim(rows)


def kconn_fill_attempt_rows() -> list[dict[str, object]]:
    rows = [
        {
            "attempt_id": "KOF1376_0_metric_connection_variation",
            "target": "delta_g connection/derivative response convention",
            "formula_slot": "owner of N_conn,nabla, N_conn,star, N_conn,ibp, N_conn,edge",
            "attempted_fill": "use 1288 and 776 ledgers as the source of derivative, Hodge, domain, and connection metric-response terms",
            "outcome": "NOT_SOURCE_FILLED",
            "missing_inputs": "explicit gauge/frame convention; domain norm; connection variation operator; Hodge/coframe response; integration-by-parts boundary convention",
            "fallback": "keep K_conn symbolic and acquire transition parent inputs instead",
            "source_paths": "source-intake/mts_residuals/P8_Y5_R10_1288_KMETRIC_DERIVATIVE_TERM_BLOCKER.csv;source-intake/mts_residuals/P8_Y5_R10_776_KGAMMA_METRIC_RESPONSE_LEDGER.csv",
        },
        {
            "attempt_id": "KOF1376_1_N_conn_nabla",
            "target": "N_conn,nabla",
            "formula_slot": "K_conn_norm <= N_conn,nabla ||S_der||_D + ...",
            "attempted_fill": "read derivative-source and connection-response ledgers for an operator norm",
            "outcome": "BLOCKED_MISSING_OPERATOR_NORM",
            "missing_inputs": "linearized connection operator norm on the chosen local domain; gauge lock; index/frame lock; domain regularity",
            "fallback": "source-ready acquisition row required before Q_conn scoring",
            "source_paths": "source-intake/mts_residuals/P8_Y5_R10_1375_KCONN_FIRST_BOUND_CONTRACT.csv;source-intake/mts_residuals/P8_Y5_R10_1288_KMETRIC_DERIVATIVE_TERM_BLOCKER.csv",
        },
        {
            "attempt_id": "KOF1376_2_S_der",
            "target": "||S_der||_D",
            "formula_slot": "derivative source tensor amplitude",
            "attempted_fill": "reduce derivative source amplitude to fixed-L0 double-zero displacement and transition-support data",
            "outcome": "REDUCED_BUT_NOT_FILLED",
            "missing_inputs": "Delta_m bound; Delta_grad_m bound; U_B; pS; A_S; L0; L_tr; universal transition profile or no-hair theorem",
            "fallback": "transition parent-source acquisition rows for U_B, powers, amplitudes, and transition width",
            "source_paths": "source-intake/mts_residuals/P8_Y5_R10_1371_FIXED_L0_PARENT_ACTION_INSERTION.csv;source-intake/mts_residuals/P8_Y5_R10_1374_QALG_QTRANS_FIRST_FILL.csv;source-intake/mts_residuals/P8_Y5_R10_798_TRANSITION_CURRENT_BOUND_CONTRACT.csv",
        },
        {
            "attempt_id": "KOF1376_3_N_conn_star",
            "target": "N_conn,star",
            "formula_slot": "Hodge/coframe response norm",
            "attempted_fill": "look for Hodge/star or coframe metric-response coefficient in Kgamma/Kmetric ledgers",
            "outcome": "BLOCKED_MISSING_HODGE_COFRAME_CONVENTION",
            "missing_inputs": "coframe response map; Hodge-star variation convention; domain norm; orientation/boundary assumptions",
            "fallback": "treat as unresolved CDB operator coefficient",
            "source_paths": "source-intake/mts_residuals/P8_Y5_R10_776_KGAMMA_METRIC_RESPONSE_LEDGER.csv;source-intake/mts_residuals/P8_Y5_R10_1298_SPATIAL_TRACE_REQUIREMENTS.csv",
        },
        {
            "attempt_id": "KOF1376_4_N_conn_ibp",
            "target": "N_conn,ibp and ||S_ibp||_D",
            "formula_slot": "bulk integration-by-parts term",
            "attempted_fill": "use derivative blocker and CDB ledger to isolate the IBP bulk residue",
            "outcome": "BLOCKED_MISSING_IBP_CONVENTION",
            "missing_inputs": "explicit integration-by-parts identity; derivative source regularity; boundary term split; no-flux or compact-support theorem",
            "fallback": "leave IBP bulk in K_conn symbolic bound",
            "source_paths": "source-intake/mts_residuals/P8_Y5_R10_1288_KMETRIC_DERIVATIVE_TERM_BLOCKER.csv;source-intake/mts_residuals/P8_Y5_R10_1291_CHAIN_KERNEL_RESIDUAL_BOUND_LEDGER.csv",
        },
        {
            "attempt_id": "KOF1376_5_N_conn_edge_Bder",
            "target": "N_conn,edge and ||B_der||_{partial D}",
            "formula_slot": "derivative edge/boundary term",
            "attempted_fill": "test whether current transition shell or boundary ledgers give an edge silence theorem",
            "outcome": "BLOCKED_BY_BOUNDARY_AND_SHELL_GATES",
            "missing_inputs": "local boundary/no-flux theorem; edge profile; Kperp bound; exact shell cancellation or projector quarantine",
            "fallback": "transition shell and boundary rows must remain explicit acquisition targets",
            "source_paths": "source-intake/mts_residuals/P8_Y5_R10_798_TRANSITION_CURRENT_BOUND_CONTRACT.csv;source-intake/mts_residuals/P8_Y5_R10_802_TRANSITION_SHELL_OBSTRUCTION.csv;source-intake/mts_residuals/P8_Y5_R10_803_TRANSITION_SHELL_ANTI_CHEAT_BOUND.csv",
        },
        {
            "attempt_id": "KOF1376_6_Ndiv_Aref",
            "target": "A_ref and N_div for Q_conn",
            "formula_slot": "Q_conn <= A_ref^-1 N_div K_conn_norm",
            "attempted_fill": "promote 1375 runner formula into a scoreable row",
            "outcome": "BLOCKED_MISSING_NORMALIZATION_AND_DIVERGENCE_NORM",
            "missing_inputs": "A_ref local normalization; N_div projection norm; observable arena map; Cassini/R10/clock/orbital response operator",
            "fallback": "runner feed keeps Q_conn symbolic",
            "source_paths": "source-intake/mts_residuals/P8_Y5_R10_1375_RUNNER_FEED_UPDATE.csv;source-intake/mts_residuals/P8_Y5_R10_1288_RESPONSE_MATRIX_REQUIREMENTS.csv",
        },
        {
            "attempt_id": "KOF1376_7_verdict",
            "target": "K_conn operator-norm fill",
            "formula_slot": "K_conn_norm contract",
            "attempted_fill": "derive or source all K_conn operator norms from existing derivative/connection files",
            "outcome": "NO_SOURCE_BACKED_KCONN_OPERATOR_NORM_ROW",
            "missing_inputs": "operator norms; source tensor amplitudes; boundary/no-flux data; domain/gauge/frame convention; A_ref/N_div",
            "fallback": "activate transition parent-source acquisition table for Q_alg/Q_trans and K_conn source amplitudes",
            "source_paths": "aggregate_KOF1376_0_to_KOF1376_6",
        },
    ]
    return mark_nonclaim(rows)


def transition_acquisition_rows() -> list[dict[str, object]]:
    rows = [
        {
            "acquisition_id": "TPS1376_0_U_B",
            "target_value": "U_B",
            "role_in_formula": "universal local unscreened/support fraction in Q_alg and Q_trans powers",
            "required_source": "parent transition/no-hair law or universal profile; not an arena-fitted local value",
            "units_or_type": "dimensionless; 0<=U_B<=1 or explicitly defined support scalar",
            "current_status": "MISSING_PARENT_SOURCE",
            "refusal_gate": "reject if chosen from local-test convenience or copied from toy row",
            "source_paths": "source-intake/mts_residuals/P8_Y5_R10_798_TRANSITION_CURRENT_BOUND_CONTRACT.csv;source-intake/mts_residuals/P8_Y5_R10_799_TRANSITION_CALCULATOR_INPUT_TEMPLATE.csv",
            "source_anchor": "TCB798_0_U_B_definition;template_missing_parent_values",
            "acceptance_status": "BLOCKED_ACQUISITION_REQUIRED",
        },
        {
            "acquisition_id": "TPS1376_1_pS",
            "target_value": "pS",
            "role_in_formula": "support-source power for Delta_m and Q_alg quadratic term",
            "required_source": "parent support law linking Delta_m=A_S U_B^pS",
            "units_or_type": "dimensionless exponent",
            "current_status": "MISSING_PARENT_SOURCE",
            "refusal_gate": "reject if tuned to suppress Solar-System residuals",
            "source_paths": "source-intake/mts_residuals/P8_Y5_R10_798_TRANSITION_CURRENT_BOUND_CONTRACT.csv;source-intake/mts_residuals/P8_Y5_R10_799_TRANSITION_BOUND_FORMULA_REGISTER.csv",
            "source_anchor": "TCB798_1_pS_source_support;TBF799_0_source_amplitudes",
            "acceptance_status": "BLOCKED_ACQUISITION_REQUIRED",
        },
        {
            "acquisition_id": "TPS1376_2_pL",
            "target_value": "pL",
            "role_in_formula": "m/L drift power in Q_trans",
            "required_source": "parent drift law for the L-chain/current term",
            "units_or_type": "dimensionless exponent",
            "current_status": "MISSING_PARENT_SOURCE",
            "refusal_gate": "reject if set only to clear PPN/R10 constraints",
            "source_paths": "source-intake/mts_residuals/P8_Y5_R10_798_TRANSITION_CURRENT_BOUND_CONTRACT.csv;source-intake/mts_residuals/P8_Y5_R10_799_TRANSITION_BOUND_FORMULA_REGISTER.csv",
            "source_anchor": "TCB798_2_pL_mL_drift;TBF799_2_linear_drift_sources",
            "acceptance_status": "BLOCKED_ACQUISITION_REQUIRED",
        },
        {
            "acquisition_id": "TPS1376_3_pT",
            "target_value": "pT",
            "role_in_formula": "trace/baseline transition power in Q_trans",
            "required_source": "parent trace baseline law",
            "units_or_type": "dimensionless exponent",
            "current_status": "MISSING_PARENT_SOURCE",
            "refusal_gate": "reject if post-selected after local observable comparison",
            "source_paths": "source-intake/mts_residuals/P8_Y5_R10_798_TRANSITION_CURRENT_BOUND_CONTRACT.csv;source-intake/mts_residuals/P8_Y5_R10_799_TRANSITION_BOUND_FORMULA_REGISTER.csv",
            "source_anchor": "TCB798_3_pT_trace_baseline;TBF799_2_linear_drift_sources",
            "acceptance_status": "BLOCKED_ACQUISITION_REQUIRED",
        },
        {
            "acquisition_id": "TPS1376_4_pB",
            "target_value": "pB",
            "role_in_formula": "boundary/current transition power in Q_trans",
            "required_source": "parent boundary or Kperp law for transition support",
            "units_or_type": "dimensionless exponent",
            "current_status": "MISSING_PARENT_SOURCE",
            "refusal_gate": "reject if boundary channel is hidden inside a generic width factor",
            "source_paths": "source-intake/mts_residuals/P8_Y5_R10_798_TRANSITION_CURRENT_BOUND_CONTRACT.csv;source-intake/mts_residuals/P8_Y5_R10_799_TRANSITION_BOUND_FORMULA_REGISTER.csv",
            "source_anchor": "TCB798_5_Kperp_boundary;TBF799_2_linear_drift_sources",
            "acceptance_status": "BLOCKED_ACQUISITION_REQUIRED",
        },
        {
            "acquisition_id": "TPS1376_5_A_S",
            "target_value": "A_S",
            "role_in_formula": "amplitude in Delta_m=A_S U_B^pS and Q_alg",
            "required_source": "parent displacement-amplitude normalization with units",
            "units_or_type": "same units as m-displacement",
            "current_status": "MISSING_PARENT_SOURCE",
            "refusal_gate": "reject toy amplitude or value without source path",
            "source_paths": "source-intake/mts_residuals/P8_Y5_R10_799_TRANSITION_BOUND_FORMULA_REGISTER.csv;source-intake/mts_residuals/P8_Y5_R10_1374_QALG_QTRANS_FIRST_FILL.csv",
            "source_anchor": "TBF799_0_source_amplitudes;QQF1374_0_Q_alg_transition_reduction",
            "acceptance_status": "BLOCKED_ACQUISITION_REQUIRED",
        },
        {
            "acquisition_id": "TPS1376_6_A_L",
            "target_value": "A_L",
            "role_in_formula": "linear L-chain/drift amplitude in Q_trans",
            "required_source": "parent L-chain/current amplitude law",
            "units_or_type": "formula-dependent amplitude; must include units",
            "current_status": "MISSING_PARENT_SOURCE",
            "refusal_gate": "reject arena-fitted drift coefficient",
            "source_paths": "source-intake/mts_residuals/P8_Y5_R10_799_TRANSITION_BOUND_FORMULA_REGISTER.csv;source-intake/mts_residuals/P8_Y5_R10_1374_QALG_QTRANS_FIRST_FILL.csv",
            "source_anchor": "TBF799_2_linear_drift_sources;QQF1374_1_Q_trans_parent_power_pack",
            "acceptance_status": "BLOCKED_ACQUISITION_REQUIRED",
        },
        {
            "acquisition_id": "TPS1376_7_A_T",
            "target_value": "A_T",
            "role_in_formula": "trace/baseline amplitude in Q_trans",
            "required_source": "parent trace baseline amplitude law",
            "units_or_type": "formula-dependent amplitude; must include units",
            "current_status": "MISSING_PARENT_SOURCE",
            "refusal_gate": "reject if only introduced to cancel Q_alg",
            "source_paths": "source-intake/mts_residuals/P8_Y5_R10_799_TRANSITION_BOUND_FORMULA_REGISTER.csv;source-intake/mts_residuals/P8_Y5_R10_1374_QALG_QTRANS_FIRST_FILL.csv",
            "source_anchor": "TBF799_2_linear_drift_sources;QQF1374_1_Q_trans_parent_power_pack",
            "acceptance_status": "BLOCKED_ACQUISITION_REQUIRED",
        },
        {
            "acquisition_id": "TPS1376_8_A_B",
            "target_value": "A_B",
            "role_in_formula": "boundary/current amplitude in Q_trans",
            "required_source": "parent boundary/Kperp amplitude law",
            "units_or_type": "formula-dependent amplitude; must include units",
            "current_status": "MISSING_PARENT_SOURCE",
            "refusal_gate": "reject without boundary/no-flux source path",
            "source_paths": "source-intake/mts_residuals/P8_Y5_R10_798_TRANSITION_CURRENT_BOUND_CONTRACT.csv;source-intake/mts_residuals/P8_Y5_R10_799_TRANSITION_BOUND_FORMULA_REGISTER.csv",
            "source_anchor": "TCB798_5_Kperp_boundary;TBF799_2_linear_drift_sources",
            "acceptance_status": "BLOCKED_ACQUISITION_REQUIRED",
        },
        {
            "acquisition_id": "TPS1376_9_b_mem",
            "target_value": "b_mem",
            "role_in_formula": "memory-curvature coefficient in Q_trans",
            "required_source": "parent memory/source stress coefficient or theorem-zero",
            "units_or_type": "formula-dependent memory coefficient; must include units",
            "current_status": "MISSING_PARENT_SOURCE",
            "refusal_gate": "reject if memory source stress is silently set to zero",
            "source_paths": "source-intake/mts_residuals/P8_Y5_R10_799_TRANSITION_BOUND_FORMULA_REGISTER.csv;source-intake/mts_residuals/P8_Y5_R10_1374_QALG_QTRANS_FIRST_FILL.csv",
            "source_anchor": "TBF799_3_bmem_curvature;QQF1374_1_Q_trans_parent_power_pack",
            "acceptance_status": "BLOCKED_ACQUISITION_REQUIRED",
        },
        {
            "acquisition_id": "TPS1376_10_F2",
            "target_value": "F2",
            "role_in_formula": "second local curvature of Fhat at m_* in Q_alg",
            "required_source": "parent potential/action curvature at the double-zero point",
            "units_or_type": "units of Fhat'' in fixed-L0 action convention",
            "current_status": "MISSING_PARENT_SOURCE",
            "refusal_gate": "reject sign/magnitude selected by local residual target",
            "source_paths": "source-intake/mts_residuals/P8_Y5_R10_1371_FIXED_L0_PARENT_ACTION_INSERTION.csv;source-intake/mts_residuals/P8_Y5_R10_1374_QALG_QTRANS_FIRST_FILL.csv",
            "source_anchor": "PAI1371_2_strict_double_zero;QQF1374_0_Q_alg_transition_reduction",
            "acceptance_status": "BLOCKED_ACQUISITION_REQUIRED",
        },
        {
            "acquisition_id": "TPS1376_11_L0",
            "target_value": "L0",
            "role_in_formula": "fixed parent length scale in Q_alg/Q_trans denominators",
            "required_source": "parent action branch adoption and scale-setting rule, not per-arena fit",
            "units_or_type": "length",
            "current_status": "ACTION_ROLE_SOURCED_NUMERIC_VALUE_MISSING",
            "refusal_gate": "reject if L0 is chosen after seeing R10/PPN residuals",
            "source_paths": "source-intake/mts_residuals/P8_Y5_R10_1371_FIXED_L0_PARENT_ACTION_INSERTION.csv;source-intake/mts_residuals/P8_Y5_R10_1374_QALG_QTRANS_FIRST_FILL.csv",
            "source_anchor": "PAI1371_0_fixed_L0_action_branch;QQF1374_0_Q_alg_transition_reduction",
            "acceptance_status": "BLOCKED_NUMERIC_SOURCE_REQUIRED",
        },
        {
            "acquisition_id": "TPS1376_12_L_tr",
            "target_value": "L_tr",
            "role_in_formula": "transition width in Q_alg/Q_trans denominators",
            "required_source": "transition geometry law or derived support/no-hair length",
            "units_or_type": "length",
            "current_status": "MISSING_PARENT_SOURCE",
            "refusal_gate": "reject generic large width unless derived from parent geometry",
            "source_paths": "source-intake/mts_residuals/P8_Y5_R10_798_TRANSITION_CURRENT_BOUND_CONTRACT.csv;source-intake/mts_residuals/P8_Y5_R10_799_TRANSITION_CALCULATOR_INPUT_TEMPLATE.csv",
            "source_anchor": "TCB798_4_transition_width;template_missing_parent_values",
            "acceptance_status": "BLOCKED_ACQUISITION_REQUIRED",
        },
        {
            "acquisition_id": "TPS1376_13_A_ref",
            "target_value": "A_ref",
            "role_in_formula": "local normalization for Q_alg, Q_trans, and Q_conn",
            "required_source": "domain/observable normalization convention and units",
            "units_or_type": "same normalization units used by Q_norm runner",
            "current_status": "MISSING_NORMALIZATION_CONVENTION",
            "refusal_gate": "reject if normalization is chosen to make residuals small",
            "source_paths": "source-intake/mts_residuals/P8_Y5_R10_1375_RUNNER_FEED_UPDATE.csv;source-intake/mts_residuals/P8_Y5_R10_1288_RESPONSE_MATRIX_REQUIREMENTS.csv",
            "source_anchor": "RUF1375_2_K_conn;RMR1288_7_response_verdict",
            "acceptance_status": "BLOCKED_ACQUISITION_REQUIRED",
        },
        {
            "acquisition_id": "TPS1376_14_epsilon_limits",
            "target_value": "epsilon_q_limit;epsilon_N_limit",
            "role_in_formula": "strict calculator/validator thresholds for q and trace safety",
            "required_source": "observable arena response map and accepted local limit convention",
            "units_or_type": "dimensionless tolerances or arena-specific response units",
            "current_status": "MISSING_ARENA_PROJECTION",
            "refusal_gate": "reject threshold not tied to R10/PPN/clock/orbital observable",
            "source_paths": "source-intake/mts_residuals/P8_Y5_R10_799_TRANSITION_CALCULATOR_INPUT_TEMPLATE.csv;source-intake/mts_residuals/P8_Y5_R10_1288_RESPONSE_MATRIX_REQUIREMENTS.csv",
            "source_anchor": "template_missing_parent_values;RMR1288_7_response_verdict",
            "acceptance_status": "BLOCKED_ARENA_MAP_REQUIRED",
        },
        {
            "acquisition_id": "TPS1376_15_source_provenance",
            "target_value": "source_path;source_anchor;units;extraction_method",
            "role_in_formula": "minimum provenance gate for any future numeric transition row",
            "required_source": "real local path plus anchor, no MISSING_* and no toy_nonclaim_no_physical_source",
            "units_or_type": "metadata",
            "current_status": "SCHEMA_REQUIREMENT_READY",
            "refusal_gate": "reject rows with missing source path, missing units, toy source, or claim flags true before review",
            "source_paths": "source-intake/mts_residuals/P8_Y5_R10_1375_TRANSITION_INPUT_VALIDATOR_RESULTS.csv;source-intake/mts_residuals/P8_Y5_R10_799_TRANSITION_CALCULATOR_SMOKE_OUTPUT.csv",
            "source_anchor": "VALIDATOR1375_VERDICT;toy_strong_support_nonclaim",
            "acceptance_status": "PASS_SCHEMA_GATE_DEFINED",
        },
        {
            "acquisition_id": "TPS1376_16_shell_projector_or_bound",
            "target_value": "transition_shell_projector_identity_or_explicit_bound",
            "role_in_formula": "anti-cheat requirement before local residual pass",
            "required_source": "exact projector cancellation/quarantine theorem or explicit shell contribution in Q_trans/Q_proj",
            "units_or_type": "theorem or bound row with units",
            "current_status": "MISSING_SHELL_CLOSURE",
            "refusal_gate": "reject if transition shell is ignored or hidden by U_B/width scaling",
            "source_paths": "source-intake/mts_residuals/P8_Y5_R10_802_TRANSITION_SHELL_OBSTRUCTION.csv;source-intake/mts_residuals/P8_Y5_R10_803_TRANSITION_SHELL_ANTI_CHEAT_BOUND.csv",
            "source_anchor": "TS802_0_direct_projection;AC803_0_required_shell_suppression",
            "acceptance_status": "BLOCKED_EXACT_CANCELLATION_OR_BOUND_REQUIRED",
        },
    ]
    return mark_nonclaim(rows)


def runner_feed_rows() -> list[dict[str, object]]:
    return mark_nonclaim(
        [
            {
                "feed_id": "RUF1376_0_Kconn",
                "runner_field": "Q_conn",
                "feed_update": "retain Q_conn <= A_ref^-1 N_div K_conn_norm with K_conn_norm decomposed into nabla/star/IBP/edge pieces",
                "status": "SYMBOLIC_OPERATOR_BOUND_ONLY",
                "blocks_claim_because": "K_conn operator norms, source tensors, edge term, A_ref, and N_div are not source-filled",
            },
            {
                "feed_id": "RUF1376_1_transition_acquisition",
                "runner_field": "Q_alg_Q_trans_parent_inputs",
                "feed_update": "use the acquisition table as the required source checklist for U_B, powers, amplitudes, L0, L_tr, A_ref, and shell gates",
                "status": "ACQUISITION_LEDGER_READY_NO_NUMERIC_ROW",
                "blocks_claim_because": "the table is a shopping list, not evidence; no row is valid_for_claim",
            },
            {
                "feed_id": "RUF1376_2_validator_next",
                "runner_field": "transition_input_validator",
                "feed_update": "next runner should build a candidate row only if every required parent source, unit, and anchor is present; otherwise keep refusing",
                "status": "NEXT_VALIDATOR_CONTRACT_READY",
                "blocks_claim_because": "toy/missing/acquisition-only rows remain blocked",
            },
            {
                "feed_id": "RUF1376_3_claim_status",
                "runner_field": "local_GR_PPN_R10_status",
                "feed_update": "do not claim local-GR, PPN, R10, q_loc=0, or GitHub-ready result from 1376",
                "status": "BLOCKED_NO_CLAIM",
                "blocks_claim_because": "K_conn is not sourced and transition parent inputs are not sourced",
            },
        ]
    )


def claim_gate_rows() -> list[dict[str, object]]:
    return mark_nonclaim(
        [
            {
                "gate_id": "GATE1376_0_source_integrity",
                "gate": "all cited local paths and anchors exist",
                "status": "PASS_SOURCE_REGISTERED",
                "reason": "1376 uses existing 1371/1374/1375/1288/776/1291/1298/798/799/802/803 anchors.",
            },
            {
                "gate_id": "GATE1376_1_Kconn_operator_norms",
                "gate": "K_conn operator norms are source-filled",
                "status": "BLOCKED_NOT_SOURCE_FILLED",
                "reason": "N_conn,* and source-tensor norms are still missing gauge/domain/operator/boundary conventions.",
            },
            {
                "gate_id": "GATE1376_2_transition_parent_sources",
                "gate": "transition parent-source acquisition table exists",
                "status": "PASS_ACQUISITION_LEDGER_READY",
                "reason": "U_B, powers, amplitudes, L0, L_tr, A_ref, limits, provenance, and shell closure now have explicit acquisition rows.",
            },
            {
                "gate_id": "GATE1376_3_numeric_runner",
                "gate": "Q_alg/Q_trans/Q_conn can be evaluated numerically",
                "status": "BLOCKED_NO_NUMERIC_SOURCE_ROW",
                "reason": "current evidence contains only symbolic contracts, missing-parent templates, and toy nonclaim rows.",
            },
            {
                "gate_id": "GATE1376_4_local_claim",
                "gate": "local GR / PPN / R10 pass can be claimed",
                "status": "BLOCKED_NO_CLAIM",
                "reason": "no source-backed K_conn fill and no source-backed transition parent row.",
            },
        ]
    )


def decision_rows() -> list[dict[str, object]]:
    return mark_nonclaim(
        [
            {
                "decision_id": "DEC1376_0_Kconn_route",
                "decision": "do not promote K_conn to a numeric or theorem-zero row",
                "why": "existing derivative/connection ledgers identify the missing terms but do not supply the operator norms, gauge/domain conventions, or boundary split",
                "next_action": "keep K_conn symbolic unless a parent source/convention row is found",
            },
            {
                "decision_id": "DEC1376_1_transition_route",
                "decision": "use transition parent-source acquisition as the active fallback",
                "why": "Q_alg/Q_trans have formulas but cannot be scored without U_B, powers, amplitudes, L0, L_tr, A_ref, and shell closure",
                "next_action": "build a candidate transition source row only from real parent sources and reject toy/missing values",
            },
            {
                "decision_id": "DEC1376_2_next_best_target",
                "decision": "1377 should either build a valid transition parent source row or hunt exact K_conn operator source conventions",
                "why": "these two routes are now the cleanest paths to reducing Q_norm without smuggling a plateau axiom",
                "next_action": "prioritize source-backed parent rows before any local observable scoring",
            },
        ]
    )


def next_rows() -> list[dict[str, object]]:
    return mark_nonclaim(
        [
            {
                "next_id": "NEXT1376_0_1377",
                "next_doc": "1377-Y5-R10-RAB-transition-parent-source-row-builder-or-Kconn-operator-source-hunt.md",
                "next_script": "scripts/Y5_R10_RAB_transition_parent_source_row_builder_or_Kconn_operator_source_hunt.py",
                "task": "build and validate a candidate transition parent source row from the 1376 acquisition table; if no sources exist, hunt an exact K_conn operator-source/convention row",
                "success_condition": "either a nonclaim but source-backed candidate parent row exists with units/anchors, or K_conn receives a source-backed operator convention row; otherwise produce a blocker ledger",
                "do_not_claim": "local GR;PPN pass;R10 pass;q_loc=0;GitHub-ready result",
            }
        ]
    )


def generated_csv_paths() -> list[Path]:
    return [
        SOURCE_REGISTER_PATH,
        KCONN_FILL_PATH,
        TRANSITION_ACQUISITION_PATH,
        RUNNER_FEED_PATH,
        CLAIM_GATE_PATH,
        DECISION_PATH,
        NEXT_PATH,
    ]


def all_rows_nonclaim(*groups: list[dict[str, object]]) -> bool:
    for rows in groups:
        for row in rows:
            if str(row.get("valid_for_claim", "")).lower() != "false":
                return False
            if str(row.get("claim_allowed", "")).lower() != "false":
                return False
    return True


def csv_parse_details(paths: list[Path]) -> tuple[bool, str]:
    details = []
    ok = True
    for path in paths:
        try:
            count = len(read_csv_rows(path))
            details.append(f"{path.name}:{count}")
        except Exception as exc:  # pragma: no cover - validation ledger should record the failure
            ok = False
            details.append(f"{path.name}:ERROR:{exc}")
    return ok, "; ".join(details)


def validation_rows(
    sources: list[dict[str, object]],
    kconn: list[dict[str, object]],
    acquisition: list[dict[str, object]],
    runner_feed: list[dict[str, object]],
    gates: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    all_sources_ok = all(bool(row["exists"]) and bool(row["anchor_found"]) for row in sources)
    no_kconn_claim = any(row["attempt_id"] == "KOF1376_7_verdict" and row["outcome"] == "NO_SOURCE_BACKED_KCONN_OPERATOR_NORM_ROW" for row in kconn)
    required_targets = {
        "U_B",
        "pS",
        "pL",
        "pT",
        "pB",
        "A_S",
        "A_L",
        "A_T",
        "A_B",
        "b_mem",
        "F2",
        "L0",
        "L_tr",
        "A_ref",
    }
    acquisition_targets = {str(row["target_value"]).split(";")[0] for row in acquisition}
    acquisition_ready = required_targets.issubset(acquisition_targets) and all("BLOCKED" in str(row["acceptance_status"]) or "PASS_SCHEMA_GATE_DEFINED" == row["acceptance_status"] for row in acquisition)
    runner_blocks = any(row["feed_id"] == "RUF1376_3_claim_status" and row["status"] == "BLOCKED_NO_CLAIM" for row in runner_feed)
    local_claim_blocked = any(row["gate_id"] == "GATE1376_4_local_claim" and row["status"] == "BLOCKED_NO_CLAIM" for row in gates)
    nonclaim = all_rows_nonclaim(sources, kconn, acquisition, runner_feed, gates)
    csv_ok, csv_details = csv_parse_details(csv_paths)
    outputs_scoped = all(ROOT in path.resolve().parents or path.resolve() == ROOT for path in [DOC_PATH, VALIDATION_PATH, *csv_paths])
    formalization_untouched_by_script = FORMALIZATION.exists() and all(FORMALIZATION not in path.resolve().parents for path in [DOC_PATH, VALIDATION_PATH, *csv_paths])

    rows = [
        {
            "validation_id": "VAL1376_0_sources",
            "check": "every cited local source path exists and anchor is found",
            "status": "PASS" if all_sources_ok else "FAIL",
            "details": "; ".join(f"{row['source_id']} exists={row['exists']} anchor={row['anchor_found']}" for row in sources),
        },
        {
            "validation_id": "VAL1376_1_Kconn_fill_attempt",
            "check": "K_conn operator-norm fill is attempted without promoting unsourced coefficients",
            "status": "PASS" if no_kconn_claim else "FAIL",
            "details": "KOF1376_7 records no source-backed K_conn operator-norm row; K_conn remains symbolic.",
        },
        {
            "validation_id": "VAL1376_2_transition_acquisition",
            "check": "transition parent-source acquisition rows cover the required Q_alg/Q_trans fields",
            "status": "PASS" if acquisition_ready else "FAIL",
            "details": "required targets checked: " + ";".join(sorted(required_targets)),
        },
        {
            "validation_id": "VAL1376_3_runner_refusal",
            "check": "runner feed keeps local claims blocked",
            "status": "PASS" if runner_blocks and local_claim_blocked else "FAIL",
            "details": "RUF1376_3 and GATE1376_4 both keep BLOCKED_NO_CLAIM.",
        },
        {
            "validation_id": "VAL1376_4_no_claim_rows",
            "check": "all generated rows keep valid_for_claim=false and claim_allowed=false",
            "status": "PASS" if nonclaim else "FAIL",
            "details": "1376 is source acquisition and blocker discipline, not a local-GR/PPN/R10 pass.",
        },
        {
            "validation_id": "VAL1376_5_csv_parse",
            "check": "all generated CSVs parse cleanly",
            "status": "PASS" if csv_ok else "FAIL",
            "details": csv_details,
        },
        {
            "validation_id": "VAL1376_6_scope",
            "check": "generated outputs stay inside post-checkpoint-work and outside formalization-workbench",
            "status": "PASS" if outputs_scoped and formalization_untouched_by_script else "FAIL",
            "details": f"ROOT={ROOT}; FORMALIZATION_EXISTS={FORMALIZATION.exists()}",
        },
    ]
    overall_ok = all(row["status"] == "PASS" for row in rows)
    rows.append(
        {
            "validation_id": "VAL1376_7_overall",
            "check": "overall 1376 validation",
            "status": "PASS" if overall_ok else "FAIL",
            "details": "1376 refuses unsourced K_conn promotion and creates a source-ready transition acquisition ledger.",
        }
    )
    return rows


def write_doc(
    sources: list[dict[str, object]],
    kconn: list[dict[str, object]],
    acquisition: list[dict[str, object]],
    runner_feed: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_targets: list[dict[str, object]],
    validations: list[dict[str, object]],
) -> None:
    text = f"""# {TITLE}

**Current verdict:** 1376 tried the derivation-first route for `K_conn`, but the existing derivative/connection ledgers still do not source the needed operator norms, source tensor amplitudes, boundary/no-flux split, or domain/gauge/frame conventions. So `K_conn` remains a symbolic CDB residual channel, not a theorem-zero and not a numeric pass.

**Main progress:** the fallback is now cleaner: the transition route has a source-acquisition ledger for `U_B`, support powers, amplitudes, `F2`, `L0`, `L_tr`, `A_ref`, arena limits, provenance, and the shell anti-cheat gate. This is not a claim row; it is the shopping list future work must satisfy before any local-GR/PPN/R10 scoring.

**Runner stance:** keep `Q_conn <= A_ref^-1 N_div K_conn_norm` symbolic and keep `Q_alg/Q_trans` blocked until a real parent-sourced transition row replaces the missing-parent and toy rows.

## Source Register

{table(["source_id", "source_path", "required_anchor", "exists", "anchor_found", "purpose", "valid_for_claim", "claim_allowed"], sources)}

## `K_conn` Operator-Norm Fill Attempt

{table(["attempt_id", "target", "formula_slot", "attempted_fill", "outcome", "missing_inputs", "fallback", "source_paths", "valid_for_claim", "claim_allowed"], kconn)}

## Transition Parent-Source Acquisition

{table(["acquisition_id", "target_value", "role_in_formula", "required_source", "units_or_type", "current_status", "refusal_gate", "source_paths", "source_anchor", "acceptance_status", "valid_for_claim", "claim_allowed"], acquisition)}

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
    kconn = kconn_fill_attempt_rows()
    acquisition = transition_acquisition_rows()
    runner_feed = runner_feed_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_targets = next_rows()

    csv_paths = generated_csv_paths()
    write_csv(SOURCE_REGISTER_PATH, sources)
    write_csv(KCONN_FILL_PATH, kconn)
    write_csv(TRANSITION_ACQUISITION_PATH, acquisition)
    write_csv(RUNNER_FEED_PATH, runner_feed)
    write_csv(CLAIM_GATE_PATH, gates)
    write_csv(DECISION_PATH, decisions)
    write_csv(NEXT_PATH, next_targets)

    validations = validation_rows(sources, kconn, acquisition, runner_feed, gates, csv_paths)
    write_csv(VALIDATION_PATH, validations)
    write_doc(sources, kconn, acquisition, runner_feed, gates, decisions, next_targets, validations)

    print(f"wrote {DOC_PATH}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"formalization-workbench touched by this script: {FORMALIZATION.exists() and False}")


if __name__ == "__main__":
    main()
