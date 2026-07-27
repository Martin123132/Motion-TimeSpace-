from __future__ import annotations

import csv
from pathlib import Path


PACK_ID = "P8_Y5_R10_1374"
TITLE = "1374-Y5-R10-RAB-Qalg-Qtrans-first-fill-or-Kcdb-subchannel-bound"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
QALG_QTRANS_PATH = OUT_DIR / f"{PACK_ID}_QALG_QTRANS_FIRST_FILL.csv"
KCDB_SPLIT_PATH = OUT_DIR / f"{PACK_ID}_KCDB_SUBCHANNEL_BOUND_CONTRACTS.csv"
RUNNER_SCHEMA_PATH = OUT_DIR / f"{PACK_ID}_QNORM_RUNNER_SCHEMA_UPDATE.csv"
CLAIM_GATE_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATE.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1374_VALIDATION.csv"


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
            "source_id": "SRC1374_0_1373_doc",
            "source_path": "1373-Y5-R10-RAB-Qnorm-first-fill-from-fixed-L0-branch-or-cdb-no-flux-theorem.md",
            "required_anchor": "NEXT1373_0_1374",
            "purpose": "1373 handoff to Q_alg/Q_trans first fill or K_cdb subchannel split.",
        },
        {
            "source_id": "SRC1374_1_1373_next",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1373_NEXT_TARGET.csv",
            "required_anchor": "NEXT1373_0_1374",
            "purpose": "machine-readable 1374 target.",
        },
        {
            "source_id": "SRC1374_2_1373_first_fill",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1373_QNORM_COMPONENT_FIRST_FILL_CONTRACTS.csv",
            "required_anchor": "QFF1373_0_Q_alg",
            "purpose": "Q_norm component first-fill contracts.",
        },
        {
            "source_id": "SRC1374_3_1373_cdb",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1373_CDB_NO_FLUX_THEOREM_ATTEMPT.csv",
            "required_anchor": "CDB1373_4_verdict",
            "purpose": "CDB no-flux theorem remains blocked.",
        },
        {
            "source_id": "SRC1374_4_798_transition_contract",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_798_TRANSITION_CURRENT_BOUND_CONTRACT.csv",
            "required_anchor": "TCB798_0_U_B_definition",
            "purpose": "transition parent inputs required for Q_alg/Q_trans.",
        },
        {
            "source_id": "SRC1374_5_799_formula",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_799_TRANSITION_BOUND_FORMULA_REGISTER.csv",
            "required_anchor": "TBF799_1_q_gamma_quad",
            "purpose": "transition source formulas.",
        },
        {
            "source_id": "SRC1374_6_799_input_template",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_799_TRANSITION_CALCULATOR_INPUT_TEMPLATE.csv",
            "required_anchor": "template_missing_parent_values",
            "purpose": "transition calculator required inputs and toy row.",
        },
        {
            "source_id": "SRC1374_7_799_smoke",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_799_TRANSITION_CALCULATOR_SMOKE_OUTPUT.csv",
            "required_anchor": "toy_strong_support_nonclaim",
            "purpose": "toy nonclaim calculator output that must not be imported.",
        },
        {
            "source_id": "SRC1374_8_802_shell",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_802_TRANSITION_SHELL_OBSTRUCTION.csv",
            "required_anchor": "TS802_0_direct_projection",
            "purpose": "transition shell direct projection obstruction.",
        },
        {
            "source_id": "SRC1374_9_803_anticheat",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_803_TRANSITION_SHELL_ANTI_CHEAT_BOUND.csv",
            "required_anchor": "AC803_0_required_shell_suppression",
            "purpose": "anti-cheat guard against hiding transition shells.",
        },
        {
            "source_id": "SRC1374_10_1291_cdb",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1291_CHAIN_KERNEL_RESIDUAL_BOUND_LEDGER.csv",
            "required_anchor": "KRB1291_2_cdb_bound",
            "purpose": "CDB residual bound form.",
        },
        {
            "source_id": "SRC1374_11_776_response",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_776_KGAMMA_METRIC_RESPONSE_LEDGER.csv",
            "required_anchor": "KGL776_2_derivative_terms",
            "purpose": "connection/projector/boundary response blockers.",
        },
        {
            "source_id": "SRC1374_12_1298_trace",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1298_SPATIAL_TRACE_REQUIREMENTS.csv",
            "required_anchor": "STR1298_2_cdb_spatial_trace",
            "purpose": "CDB spatial trace and index-convention requirements.",
        },
        {
            "source_id": "SRC1374_13_1289_response_hunt",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1289_RESPONSE_COEFFICIENT_HUNT_LEDGER.csv",
            "required_anchor": "RCH1289_0_response_matrix_route",
            "purpose": "response coefficients not found.",
        },
    ]
    for row in rows:
        path = source_path(str(row["source_path"]))
        row["exists"] = path.exists()
        row["anchor_found"] = path.exists() and str(row["required_anchor"]) in read_text(path)
    return mark_nonclaim(rows)


def qalg_qtrans_rows() -> list[dict[str, object]]:
    return mark_nonclaim(
        [
            {
                "fill_id": "QQF1374_0_Q_alg_transition_reduction",
                "component": "Q_alg",
                "derived_formula": "Q_alg <= A_ref^-1 |F2| A_S^2 U_B^(2pS)/(L0^2 L_tr)",
                "derivation": "Use Delta_m=M_src=A_S U_B^pS and Delta_grad_m<=M_src/L_tr in the 1373 Q_alg formula; identify L_cg=L0.",
                "status": "SYMBOLIC_FIRST_FILL_DERIVED_VALUES_MISSING",
                "required_values": "A_ref;F2;A_S;U_B;pS;L0;L_tr",
                "source_paths": "source-intake/mts_residuals/P8_Y5_R10_1373_QNORM_COMPONENT_FIRST_FILL_CONTRACTS.csv;source-intake/mts_residuals/P8_Y5_R10_799_TRANSITION_BOUND_FORMULA_REGISTER.csv",
                "refusal_rule": "refuse if any parent value is toy, missing, arena-fitted, or lacks source path",
            },
            {
                "fill_id": "QQF1374_1_Q_trans_parent_power_pack",
                "component": "Q_trans",
                "derived_formula": "Q_trans <= A_ref^-1[A_L U_B^pL/(L0^2 L_tr)+A_T U_B^pT/L_tr+A_B U_B^pB/(L0^2 L_tr)+|b_mem|A_S^2 U_B^(2pS)/L_tr^3]",
                "derivation": "Map TBF799 q_mL, q_trace, q_boundary, and q_bmem into the 1373 Q_trans component.",
                "status": "SYMBOLIC_FIRST_FILL_DERIVED_VALUES_MISSING",
                "required_values": "A_ref;A_L;A_T;A_B;b_mem;A_S;U_B;pL;pT;pB;pS;L0;L_tr",
                "source_paths": "source-intake/mts_residuals/P8_Y5_R10_1373_QNORM_COMPONENT_FIRST_FILL_CONTRACTS.csv;source-intake/mts_residuals/P8_Y5_R10_799_TRANSITION_BOUND_FORMULA_REGISTER.csv",
                "refusal_rule": "refuse if support powers or transition width are selected by local-test convenience rather than parent law",
            },
            {
                "fill_id": "QQF1374_2_shell_projection_guard",
                "component": "transition_shell",
                "derived_formula": "direct local shell projection is not accepted; require exact cancellation/projector quarantine or include shell in Q_trans/Q_proj",
                "derivation": "802/803 reject generic U_B^2 or width-scaling safety for transition shells.",
                "status": "ANTI_CHEAT_GUARD_ACTIVE",
                "required_values": "parent projector identity or explicit shell bound",
                "source_paths": "source-intake/mts_residuals/P8_Y5_R10_802_TRANSITION_SHELL_OBSTRUCTION.csv;source-intake/mts_residuals/P8_Y5_R10_803_TRANSITION_SHELL_ANTI_CHEAT_BOUND.csv",
                "refusal_rule": "refuse local pass if transition shell is simply ignored",
            },
            {
                "fill_id": "QQF1374_3_toy_row_quarantine",
                "component": "toy_transition_calculator_row",
                "derived_formula": "toy_strong_support_nonclaim output remains calculator wiring only",
                "derivation": "toy row has numeric_ready=true but valid_for_claim=false and passes_symbolic_gate=false.",
                "status": "TOY_NUMERIC_ROW_NOT_IMPORTED",
                "required_values": "real parent-sourced row replacing toy inputs",
                "source_paths": "source-intake/mts_residuals/P8_Y5_R10_799_TRANSITION_CALCULATOR_INPUT_TEMPLATE.csv;source-intake/mts_residuals/P8_Y5_R10_799_TRANSITION_CALCULATOR_SMOKE_OUTPUT.csv",
                "refusal_rule": "refuse if case_id starts with toy_ or source_path=toy_nonclaim_no_physical_source",
            },
            {
                "fill_id": "QQF1374_4_Qalg_Qtrans_verdict",
                "component": "Q_alg_Q_trans_first_fill",
                "derived_formula": "Q_alg and Q_trans are now parent-parameter formulas, not blank contracts.",
                "derivation": "transition formula register supplies the algebraic reduction; parent numeric/source values remain absent.",
                "status": "SOURCE_READY_SYMBOLIC_INPUT_PACK_READY_NUMERIC_VALUES_MISSING",
                "required_values": "complete sourced transition calculator row with no MISSING_* and valid_for_claim reviewed separately",
                "source_paths": "aggregate_QQF1374_0_to_QQF1374_3",
                "refusal_rule": "do not score PPN/R10/local-GR until numeric values and operator/PPN maps exist",
            },
        ]
    )


def kcdb_split_rows() -> list[dict[str, object]]:
    return mark_nonclaim(
        [
            {
                "sub_id": "KCS1374_0_K_conn",
                "component": "K_conn_norm",
                "bound_formula": "K_conn_norm >= ||connection/derivative metric-response terms|| on the local domain",
                "units": "same_response_units_as_Kmetric_before_A_ref",
                "required_values": "connection variation convention; derivative operator; local gauge/frame; source path",
                "status": "SUBCHANNEL_CONTRACT_READY_VALUES_MISSING",
                "source_paths": "source-intake/mts_residuals/P8_Y5_R10_776_KGAMMA_METRIC_RESPONSE_LEDGER.csv",
            },
            {
                "sub_id": "KCS1374_1_K_domain",
                "component": "K_domain_norm",
                "bound_formula": "K_domain_norm >= ||domain/projector selector response||",
                "units": "same_response_units_as_Kmetric_before_A_ref",
                "required_values": "domain selector law; projector variation; domain source-normalization coefficient",
                "status": "SUBCHANNEL_CONTRACT_READY_THEOREM_FAILED_FOR_NOW",
                "source_paths": "source-intake/mts_residuals/P8_Y5_R10_1117_DOMAIN_ZERO_THEOREM_ATTEMPT.csv;source-intake/mts_residuals/P8_Y5_R10_1117_DOMAIN_COMPONENT_STATUS.csv",
            },
            {
                "sub_id": "KCS1374_2_K_boundary",
                "component": "K_boundary_norm",
                "bound_formula": "K_boundary_norm >= ||boundary/reference/corner metric response||",
                "units": "same_response_units_as_Kmetric_before_A_ref",
                "required_values": "boundary primitive; reference subtraction; corner terms; no-flux theorem or profile",
                "status": "SUBCHANNEL_CONTRACT_READY_THEOREM_FAILED_FOR_NOW",
                "source_paths": "source-intake/mts_residuals/P8_Y5_R10_1170_BOUNDARY_SPLIT_THEOREM.csv;source-intake/mts_residuals/P8_Y5_R10_1171_BOUNDARY_NO_GO_LEDGER.csv",
            },
            {
                "sub_id": "KCS1374_3_K_comm",
                "component": "K_comm_norm",
                "bound_formula": "K_comm_norm >= ||[P_loc, divergence/trace/readout]K_res||",
                "units": "same_response_units_as_Kmetric_before_A_ref",
                "required_values": "P_loc definition; readout frame; trace-reversal convention; commutator norm",
                "status": "SUBCHANNEL_CONTRACT_READY_VALUES_MISSING",
                "source_paths": "source-intake/mts_residuals/P8_Y5_R10_1298_SPATIAL_TRACE_REQUIREMENTS.csv",
            },
            {
                "sub_id": "KCS1374_4_spatial_trace",
                "component": "K_cdb_spatial_trace",
                "bound_formula": "sum_i R_cdb^{ii} must be bounded because Kbar_00 includes spatial trace",
                "units": "same_response_units_as_Kmetric_before_A_ref",
                "required_values": "spatial trace convention; local orthonormal frame; K_conn/K_domain/K_boundary ii components",
                "status": "SUBCHANNEL_CONTRACT_READY_VALUES_MISSING",
                "source_paths": "source-intake/mts_residuals/P8_Y5_R10_1298_SPATIAL_TRACE_REQUIREMENTS.csv",
            },
            {
                "sub_id": "KCS1374_5_index_convention",
                "component": "index_frame_lock",
                "bound_formula": "lock covariant/contravariant 00 and ii conversion before summing K_cdb",
                "units": "logic_gate",
                "required_values": "signature; local coframe; index placement; trace-reversal convention",
                "status": "REQUIRED_GATE_READY_VALUES_MISSING",
                "source_paths": "source-intake/mts_residuals/P8_Y5_R10_1298_SPATIAL_TRACE_REQUIREMENTS.csv",
            },
            {
                "sub_id": "KCS1374_6_Q_cdb_update",
                "component": "Q_cdb",
                "bound_formula": "Q_cdb <= A_ref^-1 N_div(K_conn_norm+K_domain_norm+K_boundary_norm+K_comm_norm) plus spatial-trace/index gates",
                "units": "dimensionless_after_A_ref_normalization",
                "required_values": "all KCS1374_0..5 fields",
                "status": "SUBCHANNEL_DECOMPOSITION_READY_NUMERIC_VALUES_MISSING",
                "source_paths": "aggregate_KCS1374_0_to_KCS1374_5",
            },
        ]
    )


def runner_schema_rows() -> list[dict[str, object]]:
    return mark_nonclaim(
        [
            {
                "runner_id": "QRS1374_0_Qalg_inputs",
                "field": "Q_alg_inputs",
                "schema": "A_ref,F2,A_S,U_B,pS,L0,L_tr with source_path/source_anchor per value",
                "status": "SCHEMA_READY_VALUES_MISSING",
                "refusal": "refuse toy/MISSING/arena-fitted values",
            },
            {
                "runner_id": "QRS1374_1_Qtrans_inputs",
                "field": "Q_trans_inputs",
                "schema": "A_ref,A_L,A_T,A_B,b_mem,A_S,U_B,pL,pT,pB,pS,L0,L_tr",
                "status": "SCHEMA_READY_VALUES_MISSING",
                "refusal": "refuse if transition-shell anti-cheat guard is unresolved",
            },
            {
                "runner_id": "QRS1374_2_Qcdb_inputs",
                "field": "Q_cdb_inputs",
                "schema": "N_div,K_conn_norm,K_domain_norm,K_boundary_norm,K_comm_norm,spatial_trace_gate,index_frame_lock",
                "status": "SUBCHANNEL_SCHEMA_READY_VALUES_MISSING",
                "refusal": "refuse if any subchannel is missing or theorem-failed without bound",
            },
            {
                "runner_id": "QRS1374_3_claim_policy",
                "field": "claim_flags",
                "schema": "valid_for_claim remains false until every component has source-backed values and separate review",
                "status": "REFUSAL_POLICY_READY",
                "refusal": "claim_allowed cannot become true from symbolic or toy rows",
            },
        ]
    )


def claim_gate_rows() -> list[dict[str, object]]:
    return mark_nonclaim(
        [
            {
                "gate_id": "GATE1374_0_Qalg_symbolic_fill",
                "gate": "Q_alg has source-ready parent-parameter formula",
                "status": "PASS_SYMBOLIC_FILL",
                "reason": "Q_alg reduced to A_ref^-1 |F2| A_S^2 U_B^(2pS)/(L0^2 L_tr).",
            },
            {
                "gate_id": "GATE1374_1_Qtrans_symbolic_fill",
                "gate": "Q_trans has source-ready parent-parameter formula",
                "status": "PASS_SYMBOLIC_FILL",
                "reason": "Q_trans now maps mL/trace/boundary/bmem transition terms to one formula.",
            },
            {
                "gate_id": "GATE1374_2_numeric_transition_fill",
                "gate": "Q_alg/Q_trans can be scored numerically",
                "status": "BLOCKED_PARENT_VALUES_MISSING",
                "reason": "U_B, support powers, amplitudes, L0, L_tr, and A_ref are not source-filled.",
            },
            {
                "gate_id": "GATE1374_3_toy_rows",
                "gate": "toy transition calculator row may be used as evidence",
                "status": "BLOCKED_TOY_NOT_IMPORTED",
                "reason": "toy row is valid_for_claim=false and passes_symbolic_gate=false.",
            },
            {
                "gate_id": "GATE1374_4_Qcdb_subchannels",
                "gate": "Q_cdb is split into runner-ready subchannels",
                "status": "PASS_SUBCHANNEL_SPLIT",
                "reason": "K_conn, K_domain, K_boundary, K_comm, trace, and index gates are explicit.",
            },
            {
                "gate_id": "GATE1374_5_local_claim",
                "gate": "local GR / PPN / R10 pass can be claimed",
                "status": "BLOCKED_NO_CLAIM",
                "reason": "all fills are symbolic/refusal-ready, not numeric/theorem-zero.",
            },
        ]
    )


def decision_rows() -> list[dict[str, object]]:
    return mark_nonclaim(
        [
            {
                "decision_id": "DEC1374_0_transition_route",
                "decision": "Q_alg/Q_trans are the fastest route to a future numeric smoke runner",
                "why": "they now reduce to a finite set of parent transition parameters already named by 798/799",
                "next_action": "build a sourced transition input row or derive parent values for U_B,pS,pL,pT,pB,L0,L_tr,A_ref and amplitudes",
            },
            {
                "decision_id": "DEC1374_1_cdb_route",
                "decision": "K_cdb remains a theorem-hard route but is now runner-decomposed",
                "why": "no-flux/domain shortcuts fail; each subchannel needs its own bound",
                "next_action": "attack K_conn first if deriving, or K_boundary first if using existing boundary flux ledgers",
            },
            {
                "decision_id": "DEC1374_2_no_toy_claims",
                "decision": "keep toy transition calculator rows as plumbing only",
                "why": "toy rows are useful for code shape but poison evidence if treated as physics",
                "next_action": "add a strict runner refusal test for case_id toy_* and source_path toy_nonclaim_no_physical_source",
            },
        ]
    )


def next_rows() -> list[dict[str, object]]:
    return mark_nonclaim(
        [
            {
                "next_id": "NEXT1374_0_1375",
                "next_doc": "1375-Y5-R10-RAB-transition-input-row-validator-or-Kconn-first-bound.md",
                "next_script": "scripts/Y5_R10_RAB_transition_input_row_validator_or_Kconn_first_bound.py",
                "task": "create a strict transition input-row validator for Q_alg/Q_trans with toy/proxy refusal gates; if no real parent values exist, derive the first K_conn bound contract from derivative/connection metric response",
                "success_condition": "either a transition row can be validated as source-ready nonclaim input, or K_conn receives a sharper operator/norm bound contract",
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
    qalg_qtrans: list[dict[str, object]],
    kcdb_split: list[dict[str, object]],
    runner_schema: list[dict[str, object]],
    gates: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    all_sources_ok = all(row["exists"] and row["anchor_found"] for row in sources)
    all_nonclaim = all(
        not bool(row.get("valid_for_claim")) and not bool(row.get("claim_allowed"))
        for row in sources + qalg_qtrans + kcdb_split + runner_schema + gates
    )
    qalg_ready = any(row["fill_id"] == "QQF1374_0_Q_alg_transition_reduction" and row["status"] == "SYMBOLIC_FIRST_FILL_DERIVED_VALUES_MISSING" for row in qalg_qtrans)
    qtrans_ready = any(row["fill_id"] == "QQF1374_1_Q_trans_parent_power_pack" and row["status"] == "SYMBOLIC_FIRST_FILL_DERIVED_VALUES_MISSING" for row in qalg_qtrans)
    toy_guard = any(row["fill_id"] == "QQF1374_3_toy_row_quarantine" and row["status"] == "TOY_NUMERIC_ROW_NOT_IMPORTED" for row in qalg_qtrans)
    expected_kcdb = {"K_conn_norm", "K_domain_norm", "K_boundary_norm", "K_comm_norm", "K_cdb_spatial_trace", "index_frame_lock", "Q_cdb"}
    found_kcdb = {str(row["component"]) for row in kcdb_split}
    kcdb_ready = expected_kcdb.issubset(found_kcdb)
    refusal_ready = any(row["runner_id"] == "QRS1374_3_claim_policy" and row["status"] == "REFUSAL_POLICY_READY" for row in runner_schema)
    local_claim_blocked = any(row["gate_id"] == "GATE1374_5_local_claim" and row["status"] == "BLOCKED_NO_CLAIM" for row in gates)
    csv_ok, csv_details = csv_parse_check(csv_paths)

    rows = [
        {
            "validation_id": "VAL1374_0_sources",
            "check": "every cited local source path exists and anchor is found",
            "status": "PASS" if all_sources_ok else "FAIL",
            "details": "; ".join(f"{row['source_id']} exists={row['exists']} anchor={row['anchor_found']}" for row in sources),
        },
        {
            "validation_id": "VAL1374_1_Qalg_Qtrans",
            "check": "Q_alg and Q_trans have source-ready symbolic first-fill formulas",
            "status": "PASS" if qalg_ready and qtrans_ready else "FAIL",
            "details": "Q_alg/Q_trans reduced to parent transition parameters; numeric values remain missing",
        },
        {
            "validation_id": "VAL1374_2_toy_guard",
            "check": "toy transition calculator row is quarantined",
            "status": "PASS" if toy_guard else "FAIL",
            "details": "QQF1374_3_toy_row_quarantine prevents importing toy values",
        },
        {
            "validation_id": "VAL1374_3_Kcdb_split",
            "check": "Q_cdb is split into required subchannels",
            "status": "PASS" if kcdb_ready else "FAIL",
            "details": "components found: " + ",".join(sorted(found_kcdb)),
        },
        {
            "validation_id": "VAL1374_4_runner_refusal",
            "check": "runner schema has claim/proxy refusal policy",
            "status": "PASS" if refusal_ready else "FAIL",
            "details": "QRS1374_3_claim_policy remains active",
        },
        {
            "validation_id": "VAL1374_5_no_claim_rows",
            "check": "all new rows keep valid_for_claim=false and claim_allowed=false",
            "status": "PASS" if all_nonclaim else "FAIL",
            "details": "1374 is symbolic fill scaffolding, not a local-GR or PPN pass",
        },
        {
            "validation_id": "VAL1374_6_local_claim_blocked",
            "check": "local GR / PPN / R10 claim remains blocked",
            "status": "PASS" if local_claim_blocked else "FAIL",
            "details": "GATE1374_5_local_claim remains BLOCKED_NO_CLAIM",
        },
        {
            "validation_id": "VAL1374_7_csv_parse",
            "check": "all generated CSVs parse cleanly",
            "status": "PASS" if csv_ok else "FAIL",
            "details": csv_details,
        },
    ]
    overall_ok = all(row["status"] == "PASS" for row in rows)
    rows.append(
        {
            "validation_id": "VAL1374_8_overall",
            "check": "overall 1374 validation",
            "status": "PASS" if overall_ok else "FAIL",
            "details": "1374 derives symbolic Q_alg/Q_trans fills, quarantines toy rows, and splits Q_cdb into subchannel contracts.",
        }
    )
    return rows


def write_doc(
    sources: list[dict[str, object]],
    qalg_qtrans: list[dict[str, object]],
    kcdb_split: list[dict[str, object]],
    runner_schema: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_targets: list[dict[str, object]],
    validations: list[dict[str, object]],
) -> None:
    text = f"""# {TITLE}

**Current verdict:** 1374 gives `Q_alg` and `Q_trans` their first real symbolic fills, but still no numeric/local-GR claim. The transition register reduces `Q_alg` to `A_ref^-1 |F2| A_S^2 U_B^(2pS)/(L0^2 L_tr)` and `Q_trans` to a parent-power pack, but all parent values remain missing or toy.

**Main progress:** the toy transition calculator row is quarantined, and `Q_cdb` is split into runner-ready subchannels: `K_conn`, `K_domain`, `K_boundary`, `K_comm`, spatial trace, and index/frame lock. This means the next runner can refuse missing physics cleanly instead of silently swallowing it.

**Still blocked:** no local-GR, PPN, or R10 pass. The next best move is a strict transition input-row validator; if no real parent values exist, attack `K_conn` as the first CDB subchannel.

## Source Register

{table(["source_id", "source_path", "required_anchor", "exists", "anchor_found", "purpose", "valid_for_claim", "claim_allowed"], sources)}

## `Q_alg` / `Q_trans` First Fill

{table(["fill_id", "component", "status", "derived_formula", "derivation", "required_values", "source_paths", "refusal_rule", "valid_for_claim", "claim_allowed"], qalg_qtrans)}

## `Q_cdb` Subchannel Bound Contracts

{table(["sub_id", "component", "status", "bound_formula", "units", "required_values", "source_paths", "valid_for_claim", "claim_allowed"], kcdb_split)}

## `Q_norm` Runner Schema Update

{table(["runner_id", "field", "schema", "status", "refusal", "valid_for_claim", "claim_allowed"], runner_schema)}

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
    qalg_qtrans = qalg_qtrans_rows()
    kcdb_split = kcdb_split_rows()
    runner_schema = runner_schema_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_targets = next_rows()

    write_csv(SOURCE_REGISTER_PATH, sources)
    write_csv(QALG_QTRANS_PATH, qalg_qtrans)
    write_csv(KCDB_SPLIT_PATH, kcdb_split)
    write_csv(RUNNER_SCHEMA_PATH, runner_schema)
    write_csv(CLAIM_GATE_PATH, gates)
    write_csv(DECISION_PATH, decisions)
    write_csv(NEXT_PATH, next_targets)

    csv_paths = [
        SOURCE_REGISTER_PATH,
        QALG_QTRANS_PATH,
        KCDB_SPLIT_PATH,
        RUNNER_SCHEMA_PATH,
        CLAIM_GATE_PATH,
        DECISION_PATH,
        NEXT_PATH,
    ]
    validations = validation_rows(sources, qalg_qtrans, kcdb_split, runner_schema, gates, csv_paths)
    write_csv(VALIDATION_PATH, validations)
    write_doc(sources, qalg_qtrans, kcdb_split, runner_schema, gates, decisions, next_targets, validations)

    print(f"wrote {DOC_PATH}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"formalization-workbench touched by this script: {FORMALIZATION.exists() and False}")


if __name__ == "__main__":
    main()
