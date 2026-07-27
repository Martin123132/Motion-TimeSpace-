from __future__ import annotations

import csv
from pathlib import Path


PACK_ID = "P8_Y5_R10_1373"
TITLE = "1373-Y5-R10-RAB-Qnorm-first-fill-from-fixed-L0-branch-or-cdb-no-flux-theorem"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
CDB_ATTEMPT_PATH = OUT_DIR / f"{PACK_ID}_CDB_NO_FLUX_THEOREM_ATTEMPT.csv"
FIRST_FILL_PATH = OUT_DIR / f"{PACK_ID}_QNORM_COMPONENT_FIRST_FILL_CONTRACTS.csv"
RUNNER_INPUT_PATH = OUT_DIR / f"{PACK_ID}_QNORM_RUNNER_INPUT_SCHEMA.csv"
CLAIM_GATE_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATE.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1373_VALIDATION.csv"


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
        values = [cell(row.get(header, "")) for header in headers]
        out.append("| " + " | ".join(values) + " |")
    return "\n".join(out)


def mark_nonclaim(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    for row in rows:
        row["valid_for_claim"] = False
        row["claim_allowed"] = False
    return rows


def source_register() -> list[dict[str, object]]:
    rows = [
        {
            "source_id": "SRC1373_0_1372_doc",
            "source_path": "1372-Y5-R10-RAB-fixed-L0-double-zero-local-residual-theorem-or-Qnorm-bound.md",
            "required_anchor": "NEXT1372_0_1373",
            "purpose": "1372 handoff to Q_norm first fill or CDB no-flux theorem.",
        },
        {
            "source_id": "SRC1373_1_1372_next",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1372_NEXT_TARGET.csv",
            "required_anchor": "NEXT1372_0_1373",
            "purpose": "machine-readable 1373 target.",
        },
        {
            "source_id": "SRC1373_2_1372_qnorm",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1372_QNORM_DECOMPOSITION_BOUND.csv",
            "required_anchor": "QNB1372_0_total_decomposition",
            "purpose": "Q_norm component decomposition.",
        },
        {
            "source_id": "SRC1373_3_1372_runner",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1372_CQGAMMA_RUNNER_FEED.csv",
            "required_anchor": "QGF1372_2_acceptance",
            "purpose": "symbolic Cassini/PPN acceptance feed.",
        },
        {
            "source_id": "SRC1373_4_1291_cdb",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1291_CHAIN_KERNEL_RESIDUAL_BOUND_LEDGER.csv",
            "required_anchor": "KRB1291_2_cdb_bound",
            "purpose": "CDB residual bound form.",
        },
        {
            "source_id": "SRC1373_5_776_response",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_776_KGAMMA_METRIC_RESPONSE_LEDGER.csv",
            "required_anchor": "KGL776_2_derivative_terms",
            "purpose": "connection/projector/boundary response channels.",
        },
        {
            "source_id": "SRC1373_6_1117_domain_theorem",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1117_DOMAIN_ZERO_THEOREM_ATTEMPT.csv",
            "required_anchor": "DSZ1117_6_verdict",
            "purpose": "domain selector zero theorem status.",
        },
        {
            "source_id": "SRC1373_7_1117_domain_components",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1117_DOMAIN_COMPONENT_STATUS.csv",
            "required_anchor": "COMP1117_3_R11_operator",
            "purpose": "domain source-normalization operator failure row.",
        },
        {
            "source_id": "SRC1373_8_1170_boundary_split",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1170_BOUNDARY_SPLIT_THEOREM.csv",
            "required_anchor": "BST1170_1_local_top_zero_not_enough",
            "purpose": "boundary primitive survives local topology.",
        },
        {
            "source_id": "SRC1373_9_1171_boundary_nogo",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1171_BOUNDARY_NO_GO_LEDGER.csv",
            "required_anchor": "NOG1171_0_neumann_gap",
            "purpose": "boundary no-flux shortcut failure.",
        },
        {
            "source_id": "SRC1373_10_1301_memory",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1301_MEMORY_STRESS_SPLIT_LEDGER.csv",
            "required_anchor": "MSS1301_1_memory_kinetic_stress",
            "purpose": "memory stress retained channels.",
        },
        {
            "source_id": "SRC1373_11_boundary_flux_fill",
            "source_path": "source-intake/mts_residuals/P8_Y5_BRR545_BOUNDARY_FLUX_BOUND_FILL_ROW.csv",
            "required_anchor": "FB549_0_boundary_flux_bound",
            "purpose": "boundary flux first-fill row with missing values.",
        },
        {
            "source_id": "SRC1373_12_domain_flux_fill",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1144_EPSILON_DOMAIN_FLUX_PROFILE_FILL_QUEUE.csv",
            "required_anchor": "EPF1144_0_epsilon_profile_local",
            "purpose": "domain flux first-fill queue.",
        },
        {
            "source_id": "SRC1373_13_transition_contract",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_798_TRANSITION_CURRENT_BOUND_CONTRACT.csv",
            "required_anchor": "TCB798_0_U_B_definition",
            "purpose": "transition support-power missing inputs.",
        },
        {
            "source_id": "SRC1373_14_transition_formula",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_799_TRANSITION_BOUND_FORMULA_REGISTER.csv",
            "required_anchor": "TBF799_1_q_gamma_quad",
            "purpose": "transition/source bound formulas.",
        },
        {
            "source_id": "SRC1373_15_qnorm_proxy",
            "source_path": "source-intake/mts_residuals/P8_QLOC_BOUND_RUNNER_SPEC.csv",
            "required_anchor": "QB516_0_compact_shell_budget",
            "purpose": "old compact-shell proxy, retained only as nonclaim smoke seed.",
        },
        {
            "source_id": "SRC1373_16_1280_guard",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1280_EPSILON_GK_QLOC_BOUND_CONTRACT.csv",
            "required_anchor": "BND1280_3_no_cancellation",
            "purpose": "no-cancellation guard.",
        },
    ]
    for row in rows:
        path = source_path(str(row["source_path"]))
        row["exists"] = path.exists()
        row["anchor_found"] = path.exists() and str(row["required_anchor"]) in read_text(path)
    return mark_nonclaim(rows)


def cdb_attempt_rows() -> list[dict[str, object]]:
    return mark_nonclaim(
        [
            {
                "attempt_id": "CDB1373_0_fixed_L0_effect",
                "target": "K_cdb under fixed L0",
                "attempt": "Use fixed L0 and strict double-zero to remove connection/domain/boundary response.",
                "result": "FAIL_SCOPE_MISMATCH",
                "reason": "fixed L0 closes algebraic L_cg variation; it does not by itself silence derivative, projector, domain, or boundary metric responses.",
                "source_paths": "source-intake/mts_residuals/P8_Y5_R10_1372_QNORM_DECOMPOSITION_BOUND.csv;source-intake/mts_residuals/P8_Y5_R10_776_KGAMMA_METRIC_RESPONSE_LEDGER.csv",
                "source_anchors": "QNB1372_2_cdb_divergence;KGL776_2_derivative_terms",
            },
            {
                "attempt_id": "CDB1373_1_connection_no_flux",
                "target": "K_conn",
                "attempt": "Promote connection/derivative terms to zero from local vacuum/double-zero.",
                "result": "NOT_DERIVED",
                "reason": "derivative/connection metric response requires Helmholtz/integrability and explicit G_AB/tensor-slot comparison, still open.",
                "source_paths": "source-intake/mts_residuals/P8_Y5_R10_776_KGAMMA_METRIC_RESPONSE_LEDGER.csv;source-intake/mts_residuals/P8_Y5_R10_1291_CHAIN_KERNEL_RESIDUAL_BOUND_LEDGER.csv",
                "source_anchors": "KGL776_2_derivative_terms;KRB1291_2_cdb_bound",
            },
            {
                "attempt_id": "CDB1373_2_domain_no_flux",
                "target": "K_domain",
                "attempt": "Use compact local exact/trivial domain branch to set domain projector/source leakage to zero.",
                "result": "FAIL_CURRENT_CORPUS",
                "reason": "domain selector zero is conditional and the R11/source-normalization operator row fails current corpus.",
                "source_paths": "source-intake/mts_residuals/P8_Y5_R10_1117_DOMAIN_ZERO_THEOREM_ATTEMPT.csv;source-intake/mts_residuals/P8_Y5_R10_1117_DOMAIN_COMPONENT_STATUS.csv",
                "source_anchors": "DSZ1117_6_verdict;COMP1117_3_R11_operator",
            },
            {
                "attempt_id": "CDB1373_3_boundary_no_flux",
                "target": "K_boundary",
                "attempt": "Use local topology, natural boundary, or gauge to zero boundary primitive/flux.",
                "result": "FAIL_GENERAL_THEOREM",
                "reason": "local topology reduces to boundary primitive; Neumann, Dirichlet, gauge, and Bianchi shortcuts fail as general proofs.",
                "source_paths": "source-intake/mts_residuals/P8_Y5_R10_1170_BOUNDARY_SPLIT_THEOREM.csv;source-intake/mts_residuals/P8_Y5_R10_1171_BOUNDARY_NO_GO_LEDGER.csv",
                "source_anchors": "BST1170_1_local_top_zero_not_enough;NOG1171_0_neumann_gap",
            },
            {
                "attempt_id": "CDB1373_4_verdict",
                "target": "K_cdb no-flux/domain theorem",
                "attempt": "Close all CDB terms under fixed-L0 branch.",
                "result": "CDB_ZERO_THEOREM_NOT_DERIVED",
                "reason": "each subchannel remains theorem-open or failed; proceed with Q_cdb first-fill contract.",
                "source_paths": "aggregate_cdb_attempt",
                "source_anchors": "CDB1373_0_to_CDB1373_3",
            },
        ]
    )


def first_fill_rows() -> list[dict[str, object]]:
    return mark_nonclaim(
        [
            {
                "fill_id": "QFF1373_0_Q_alg",
                "component": "Q_alg",
                "formula": "Q_alg <= A_ref^-1 L0^-2 |Fhat''(m_*)| Delta_m Delta_grad_m + O(Delta_m^2 Delta_grad_m)",
                "units": "dimensionless_after_A_ref_normalization",
                "required_values": "L0;Fhat_second_at_mstar;Delta_m;Delta_grad_m;A_ref;local_norm_domain",
                "source_paths": "source-intake/mts_residuals/P8_Y5_R10_1372_QNORM_DECOMPOSITION_BOUND.csv;source-intake/mts_residuals/P8_Y5_R10_799_TRANSITION_BOUND_FORMULA_REGISTER.csv",
                "acceptance_status": "FILL_CONTRACT_READY_VALUES_MISSING",
                "validity_rule": "may be filled by parent amplitude law or transition calculator; no proxy substitution",
            },
            {
                "fill_id": "QFF1373_1_Q_cdb",
                "component": "Q_cdb",
                "formula": "Q_cdb <= A_ref^-1 N_div (K_conn_norm + K_domain_norm + K_boundary_norm + K_comm_norm)",
                "units": "dimensionless_after_A_ref_normalization",
                "required_values": "N_div;K_conn_norm;K_domain_norm;K_boundary_norm;K_comm_norm;domain_frame",
                "source_paths": "source-intake/mts_residuals/P8_Y5_R10_1291_CHAIN_KERNEL_RESIDUAL_BOUND_LEDGER.csv;source-intake/mts_residuals/P8_Y5_R10_776_KGAMMA_METRIC_RESPONSE_LEDGER.csv",
                "acceptance_status": "FILL_CONTRACT_READY_THEOREM_FAILED_FOR_NOW",
                "validity_rule": "either CDB1373 theorem closes or every norm is source-backed and bounded independently",
            },
            {
                "fill_id": "QFF1373_2_Q_mem",
                "component": "Q_mem",
                "formula": "Q_mem <= A_ref^-1 (N_kin K_mem_kin + N_pot K_mem_drift + N_src J_mem + N_bath B_mem)",
                "units": "dimensionless_after_A_ref_normalization",
                "required_values": "N_kin;K_mem_kin;N_pot;K_mem_drift;N_src;J_mem;N_bath;B_mem",
                "source_paths": "source-intake/mts_residuals/P8_Y5_R10_1301_MEMORY_STRESS_SPLIT_LEDGER.csv;source-intake/mts_residuals/P8_Y5_R10_1011_RESPONSED_DOUBLET_THEOREM_ATTEMPT.csv",
                "acceptance_status": "FILL_CONTRACT_READY_VALUES_MISSING",
                "validity_rule": "constant-m no-hair/source silence theorem or component stress bounds required",
            },
            {
                "fill_id": "QFF1373_3_Q_bdy",
                "component": "Q_bdy",
                "formula": "Q_bdy <= A_ref^-1 N_bdy ||pullback(B_C)||_{partial D} + corner/reference terms",
                "units": "dimensionless_after_A_ref_normalization",
                "required_values": "N_bdy;boundary_primitive_norm;corner_norm;reference_norm;boundary_measure",
                "source_paths": "source-intake/mts_residuals/P8_Y5_BRR545_BOUNDARY_FLUX_BOUND_FILL_ROW.csv;source-intake/mts_residuals/P8_Y5_R10_1171_BOUNDARY_NO_GO_LEDGER.csv",
                "acceptance_status": "FILL_CONTRACT_READY_VALUES_MISSING",
                "validity_rule": "theorem-zero or boundary flux profile with mapped coefficients; topology alone not accepted",
            },
            {
                "fill_id": "QFF1373_4_Q_trans",
                "component": "Q_trans",
                "formula": "Q_trans <= A_ref^-1 (U_B^(2pS) C_S/L_tr + U_B^pL C_L/L_tr + U_B^pT C_T/L_tr + U_B^pB C_B/L_tr)",
                "units": "dimensionless_after_A_ref_normalization",
                "required_values": "U_B;pS;pL;pT;pB;C_S;C_L;C_T;C_B;L_tr;A_ref",
                "source_paths": "source-intake/mts_residuals/P8_Y5_R10_798_TRANSITION_CURRENT_BOUND_CONTRACT.csv;source-intake/mts_residuals/P8_Y5_R10_799_TRANSITION_BOUND_FORMULA_REGISTER.csv",
                "acceptance_status": "FILL_CONTRACT_READY_VALUES_MISSING",
                "validity_rule": "support powers and transition geometry must be parent-derived, not chosen to hide gradients",
            },
            {
                "fill_id": "QFF1373_5_Q_proj",
                "component": "Q_proj",
                "formula": "Q_proj <= A_ref^-1 ||[P_loc, divergence/trace/readout]K_res||",
                "units": "dimensionless_after_A_ref_normalization",
                "required_values": "P_loc_definition;commutator_norm;readout_frame;domain_motion_bound;trace_reversal_convention",
                "source_paths": "source-intake/mts_residuals/P8_Y5_R10_1298_SPATIAL_TRACE_REQUIREMENTS.csv;source-intake/mts_residuals/P8_Y5_R10_1282_QLOC_PROFILE_FILL_REQUIREMENTS.csv",
                "acceptance_status": "FILL_CONTRACT_READY_VALUES_MISSING",
                "validity_rule": "projection/readout commutator must be zero-derived or bounded before PPN scoring",
            },
            {
                "fill_id": "QFF1373_6_Q_proxy_smoke_only",
                "component": "old_compact_shell_proxy",
                "formula": "Q_proxy=7.432631961576971e-06 from QB516_0, not a Q_norm value",
                "units": "dimensionless_proxy_not_PPN_units",
                "required_values": "mapping_to_Q_norm;PPN/source_normalization_units;coefficient_to_gamma",
                "source_paths": "source-intake/mts_residuals/P8_QLOC_BOUND_RUNNER_SPEC.csv",
                "acceptance_status": "SMOKE_ONLY_NOT_IMPORTED",
                "validity_rule": "may exercise runner plumbing only; never valid_for_claim until mapping exists",
            },
        ]
    )


def runner_input_rows() -> list[dict[str, object]]:
    return mark_nonclaim(
        [
            {
                "runner_id": "QRI1373_0_contract_schema",
                "field": "Q_components",
                "schema_value": "Q_alg,Q_cdb,Q_mem,Q_bdy,Q_trans,Q_proj",
                "status": "RUNNER_SCHEMA_READY",
                "acceptance": "each component must be numeric or theorem-zero with source path before scoring",
            },
            {
                "runner_id": "QRI1373_1_total_bound",
                "field": "Q_norm_bound",
                "schema_value": "sum(max(0,Q_i_bound)) over all six components",
                "status": "NO_CANCELLATION_SUM_READY",
                "acceptance": "all components included; missing component blocks score",
            },
            {
                "runner_id": "QRI1373_2_gamma_bound",
                "field": "B_gamma",
                "schema_value": "B_gamma=(c^2/(2U_min))*N_G*N_D*Q_norm_bound",
                "status": "PPN_BOUND_SCHEMA_READY_INPUTS_MISSING",
                "acceptance": "requires U_min,N_G,N_D plus all Q components",
            },
            {
                "runner_id": "QRI1373_3_pass_rule",
                "field": "nonclaim_Cassini_gate",
                "schema_value": "B_gamma <= sigma_gamma where sigma_gamma=2.3e-5",
                "status": "PASS_RULE_READY_NOT_EXECUTABLE",
                "acceptance": "execute only after all fields are source-backed and no MISSING markers remain",
            },
            {
                "runner_id": "QRI1373_4_failure_modes",
                "field": "refusal_conditions",
                "schema_value": "missing_Q_component;missing_U_min;missing_operator_norm;proxy_input;claim_flag_true_with_missing_values",
                "status": "REFUSAL_GATES_READY",
                "acceptance": "runner must refuse rather than silently score",
            },
        ]
    )


def claim_gate_rows() -> list[dict[str, object]]:
    return mark_nonclaim(
        [
            {
                "gate_id": "GATE1373_0_cdb_no_flux",
                "gate": "K_cdb no-flux/domain theorem closes",
                "status": "BLOCKED_THEOREM_NOT_DERIVED",
                "reason": "fixed L0 does not silence connection/projector/boundary response; domain and boundary shortcuts fail or remain conditional.",
            },
            {
                "gate_id": "GATE1373_1_Q_components_contracts",
                "gate": "all Q_norm components have first-fill contracts",
                "status": "PASS_CONTRACTS_READY",
                "reason": "Q_alg,Q_cdb,Q_mem,Q_bdy,Q_trans,Q_proj rows now have formulas, units, source paths, and acceptance status.",
            },
            {
                "gate_id": "GATE1373_2_Q_components_numeric",
                "gate": "all Q_norm components are numeric or theorem-zero",
                "status": "BLOCKED_VALUES_MISSING",
                "reason": "contracts are ready, but values/operator norms/amplitude laws remain missing.",
            },
            {
                "gate_id": "GATE1373_3_proxy_import",
                "gate": "old compact-shell proxy can be used as Q_norm",
                "status": "BLOCKED_PROXY_NOT_IMPORTED",
                "reason": "proxy lacks PPN/source-normalization mapping.",
            },
            {
                "gate_id": "GATE1373_4_runner_executable",
                "gate": "Q_norm/Cassini runner can execute a score",
                "status": "BLOCKED_INPUTS_MISSING",
                "reason": "Q components, U_min, N_G, and N_D remain unfilled.",
            },
            {
                "gate_id": "GATE1373_5_local_claim",
                "gate": "local GR / PPN / R10 pass can be claimed",
                "status": "BLOCKED_NO_CLAIM",
                "reason": "no CDB theorem and no numeric Q_norm bound pass.",
            },
        ]
    )


def decision_rows() -> list[dict[str, object]]:
    return mark_nonclaim(
        [
            {
                "decision_id": "DEC1373_0_cdb_route",
                "decision": "do not promote fixed-L0 to CDB no-flux theorem",
                "why": "CDB terms are derivative/projector/boundary response channels, not L_cg algebraic variation",
                "next_action": "try targeted K_conn/K_domain/K_boundary fills or a real no-flux theorem",
            },
            {
                "decision_id": "DEC1373_1_first_fill_status",
                "decision": "treat 1373 as first-fill contract checkpoint, not a numeric result",
                "why": "all Q components now have formulas/units/source paths, but none are filled enough to score",
                "next_action": "start with Q_alg and Q_trans because they are closest to existing transition formulas",
            },
            {
                "decision_id": "DEC1373_2_next_best_attack",
                "decision": "attack Q_alg/Q_trans before Q_cdb if seeking fastest empirical readiness",
                "why": "CDB no-flux has failed multiple theorem shortcuts, while transition/amplitude rows already have formula scaffolding",
                "next_action": "derive Delta_m, Delta_grad_m, U_B, pS/pL/pT/pB, L_tr, and A_ref contracts",
            },
        ]
    )


def next_rows() -> list[dict[str, object]]:
    return mark_nonclaim(
        [
            {
                "next_id": "NEXT1373_0_1374",
                "next_doc": "1374-Y5-R10-RAB-Qalg-Qtrans-first-fill-or-Kcdb-subchannel-bound.md",
                "next_script": "scripts/Y5_R10_RAB_Qalg_Qtrans_first_fill_or_Kcdb_subchannel_bound.py",
                "task": "derive first source-ready fills for Q_alg and Q_trans from fixed-L0 double-zero/transition support laws; if that fails, split Q_cdb into K_conn, K_domain, K_boundary, and K_comm fill rows with units and refusal gates",
                "success_condition": "Q_alg/Q_trans receive concrete symbolic/numeric-ready inputs, or Q_cdb is decomposed into subchannel fill contracts ready for a runner",
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
    cdb_attempts: list[dict[str, object]],
    first_fills: list[dict[str, object]],
    runner_inputs: list[dict[str, object]],
    gates: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    all_sources_ok = all(row["exists"] and row["anchor_found"] for row in sources)
    all_nonclaim = all(
        not bool(row.get("valid_for_claim")) and not bool(row.get("claim_allowed"))
        for row in sources + cdb_attempts + first_fills + runner_inputs + gates
    )
    cdb_blocked = any(row["attempt_id"] == "CDB1373_4_verdict" and row["result"] == "CDB_ZERO_THEOREM_NOT_DERIVED" for row in cdb_attempts)
    component_names = {"Q_alg", "Q_cdb", "Q_mem", "Q_bdy", "Q_trans", "Q_proj"}
    fill_components = {str(row["component"]) for row in first_fills if str(row["component"]).startswith("Q_")}
    contracts_ready = component_names.issubset(fill_components) and all(str(row["units"]) for row in first_fills if str(row["component"]) in component_names)
    proxy_guard = any(row["fill_id"] == "QFF1373_6_Q_proxy_smoke_only" and row["acceptance_status"] == "SMOKE_ONLY_NOT_IMPORTED" for row in first_fills)
    runner_ready = any(row["runner_id"] == "QRI1373_4_failure_modes" and row["status"] == "REFUSAL_GATES_READY" for row in runner_inputs)
    local_claim_blocked = any(row["gate_id"] == "GATE1373_5_local_claim" and row["status"] == "BLOCKED_NO_CLAIM" for row in gates)
    csv_ok, csv_details = csv_parse_check(csv_paths)

    rows = [
        {
            "validation_id": "VAL1373_0_sources",
            "check": "every cited local source path exists and anchor is found",
            "status": "PASS" if all_sources_ok else "FAIL",
            "details": "; ".join(f"{row['source_id']} exists={row['exists']} anchor={row['anchor_found']}" for row in sources),
        },
        {
            "validation_id": "VAL1373_1_cdb_attempt",
            "check": "CDB no-flux theorem is attempted and correctly blocked",
            "status": "PASS" if cdb_blocked else "FAIL",
            "details": "fixed L0 cannot silence derivative/projector/boundary channels by itself",
        },
        {
            "validation_id": "VAL1373_2_component_contracts",
            "check": "all six Q_norm components receive first-fill contracts with units",
            "status": "PASS" if contracts_ready else "FAIL",
            "details": "components found: " + ",".join(sorted(fill_components)),
        },
        {
            "validation_id": "VAL1373_3_proxy_guard",
            "check": "old compact-shell proxy is not imported as Q_norm",
            "status": "PASS" if proxy_guard else "FAIL",
            "details": "QFF1373_6 remains smoke-only",
        },
        {
            "validation_id": "VAL1373_4_runner_refusal",
            "check": "runner schema has refusal gates for missing/proxy inputs",
            "status": "PASS" if runner_ready else "FAIL",
            "details": "QRI1373_4_failure_modes blocks silent scoring",
        },
        {
            "validation_id": "VAL1373_5_no_claim_rows",
            "check": "all new rows keep valid_for_claim=false and claim_allowed=false",
            "status": "PASS" if all_nonclaim else "FAIL",
            "details": "1373 is first-fill scaffolding, not a local-GR or PPN pass",
        },
        {
            "validation_id": "VAL1373_6_local_claim_blocked",
            "check": "local GR / PPN / R10 claim remains blocked",
            "status": "PASS" if local_claim_blocked else "FAIL",
            "details": "GATE1373_5_local_claim remains BLOCKED_NO_CLAIM",
        },
        {
            "validation_id": "VAL1373_7_csv_parse",
            "check": "all generated CSVs parse cleanly",
            "status": "PASS" if csv_ok else "FAIL",
            "details": csv_details,
        },
    ]
    overall_ok = all(row["status"] == "PASS" for row in rows)
    rows.append(
        {
            "validation_id": "VAL1373_8_overall",
            "check": "overall 1373 validation",
            "status": "PASS" if overall_ok else "FAIL",
            "details": "1373 blocks the CDB no-flux theorem, creates Q_norm first-fill contracts, and keeps runner refusal gates active.",
        }
    )
    return rows


def write_doc(
    sources: list[dict[str, object]],
    cdb_attempts: list[dict[str, object]],
    first_fills: list[dict[str, object]],
    runner_inputs: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_targets: list[dict[str, object]],
    validations: list[dict[str, object]],
) -> None:
    text = f"""# {TITLE}

**Current verdict:** 1373 does not close `K_cdb` by a fixed-`L0` no-flux theorem. Fixed `L0` is an algebraic-chain result; it does not automatically silence connection, domain/projector, or boundary response. The domain and boundary shortcuts remain failed/conditional in the existing ledgers.

**Main progress:** every `Q_norm` component now has a first-fill contract with formula, units, source path, and acceptance status: `Q_alg`, `Q_cdb`, `Q_mem`, `Q_bdy`, `Q_trans`, and `Q_proj`. This makes the next runner concrete instead of philosophical.

**Testing progress:** the compact-shell proxy remains smoke-only. The future runner must refuse to score if any Q component, `U_min`, `N_G`, or `N_D` is missing, or if a proxy value is fed as claim data.

## Source Register

{table(["source_id", "source_path", "required_anchor", "exists", "anchor_found", "purpose", "valid_for_claim", "claim_allowed"], sources)}

## CDB No-Flux Theorem Attempt

{table(["attempt_id", "target", "result", "attempt", "reason", "source_paths", "source_anchors", "valid_for_claim", "claim_allowed"], cdb_attempts)}

## `Q_norm` Component First-Fill Contracts

{table(["fill_id", "component", "formula", "units", "required_values", "source_paths", "acceptance_status", "validity_rule", "valid_for_claim", "claim_allowed"], first_fills)}

## `Q_norm` Runner Input Schema

{table(["runner_id", "field", "schema_value", "status", "acceptance", "valid_for_claim", "claim_allowed"], runner_inputs)}

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
    cdb_attempts = cdb_attempt_rows()
    first_fills = first_fill_rows()
    runner_inputs = runner_input_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_targets = next_rows()

    write_csv(SOURCE_REGISTER_PATH, sources)
    write_csv(CDB_ATTEMPT_PATH, cdb_attempts)
    write_csv(FIRST_FILL_PATH, first_fills)
    write_csv(RUNNER_INPUT_PATH, runner_inputs)
    write_csv(CLAIM_GATE_PATH, gates)
    write_csv(DECISION_PATH, decisions)
    write_csv(NEXT_PATH, next_targets)

    csv_paths = [
        SOURCE_REGISTER_PATH,
        CDB_ATTEMPT_PATH,
        FIRST_FILL_PATH,
        RUNNER_INPUT_PATH,
        CLAIM_GATE_PATH,
        DECISION_PATH,
        NEXT_PATH,
    ]
    validations = validation_rows(sources, cdb_attempts, first_fills, runner_inputs, gates, csv_paths)
    write_csv(VALIDATION_PATH, validations)
    write_doc(sources, cdb_attempts, first_fills, runner_inputs, gates, decisions, next_targets, validations)

    print(f"wrote {DOC_PATH}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"formalization-workbench touched by this script: {FORMALIZATION.exists() and False}")


if __name__ == "__main__":
    main()
