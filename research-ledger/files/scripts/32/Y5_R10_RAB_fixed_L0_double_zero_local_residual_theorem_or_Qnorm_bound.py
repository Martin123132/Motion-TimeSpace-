from __future__ import annotations

import csv
from pathlib import Path


PACK_ID = "P8_Y5_R10_1372"
TITLE = "1372-Y5-R10-RAB-fixed-L0-double-zero-local-residual-theorem-or-Qnorm-bound"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
THEOREM_ATTEMPT_PATH = OUT_DIR / f"{PACK_ID}_LOCAL_RESIDUAL_THEOREM_ATTEMPT.csv"
QNORM_BOUND_PATH = OUT_DIR / f"{PACK_ID}_QNORM_DECOMPOSITION_BOUND.csv"
RUNNER_FEED_PATH = OUT_DIR / f"{PACK_ID}_CQGAMMA_RUNNER_FEED.csv"
CLAIM_GATE_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATE.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1372_VALIDATION.csv"


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


def table(headers: list[str], rows: list[dict[str, object]]) -> str:
    out = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        values = [str(row.get(header, "")).replace("\n", " ") for header in headers]
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
            "source_id": "SRC1372_0_1371_doc",
            "source_path": "1371-Y5-R10-RAB-fixed-Lcg-parent-action-insertion-or-Cqgamma-norm-bound.md",
            "required_anchor": "NEXT1371_0_1372",
            "purpose": "1371 handoff to fixed-L0 double-zero residual theorem or Q_norm bound.",
        },
        {
            "source_id": "SRC1372_1_1371_next",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1371_NEXT_TARGET.csv",
            "required_anchor": "NEXT1371_0_1372",
            "purpose": "machine-readable 1372 target.",
        },
        {
            "source_id": "SRC1372_2_1371_residuals",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1371_LOCAL_RESIDUAL_ZERO_OR_BOUND_LEDGER.csv",
            "required_anchor": "LRZ1371_4_cdb_terms",
            "purpose": "current local residual channels after fixed-L0 double-zero branch.",
        },
        {
            "source_id": "SRC1372_3_1371_qnorm",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1371_CQGAMMA_NORM_BOUND_INPUT_TABLE.csv",
            "required_anchor": "CQN1371_7_pass_threshold",
            "purpose": "C_qgamma norm-bound acceptance row.",
        },
        {
            "source_id": "SRC1372_4_1291_cdb",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1291_CHAIN_KERNEL_RESIDUAL_BOUND_LEDGER.csv",
            "required_anchor": "KRB1291_2_cdb_bound",
            "purpose": "K_conn/K_domain/K_boundary residual bound form.",
        },
        {
            "source_id": "SRC1372_5_776_metric_response",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_776_KGAMMA_METRIC_RESPONSE_LEDGER.csv",
            "required_anchor": "KGL776_2_derivative_terms",
            "purpose": "derivative/projector and boundary metric response remains open.",
        },
        {
            "source_id": "SRC1372_6_1117_domain",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1117_DOMAIN_ZERO_THEOREM_ATTEMPT.csv",
            "required_anchor": "DSZ1117_6_verdict",
            "purpose": "domain selector zero theorem not derived.",
        },
        {
            "source_id": "SRC1372_7_1170_boundary_split",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1170_BOUNDARY_SPLIT_THEOREM.csv",
            "required_anchor": "BST1170_1_local_top_zero_not_enough",
            "purpose": "local topology reduces residual to boundary primitive term.",
        },
        {
            "source_id": "SRC1372_8_1171_boundary_nogo",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1171_BOUNDARY_NO_GO_LEDGER.csv",
            "required_anchor": "NOG1171_0_neumann_gap",
            "purpose": "boundary no-flux theorem not available as general local result.",
        },
        {
            "source_id": "SRC1372_9_1301_memory_stress",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1301_MEMORY_STRESS_SPLIT_LEDGER.csv",
            "required_anchor": "MSS1301_1_memory_kinetic_stress",
            "purpose": "memory kinetic/potential/source/bath stress remains separate.",
        },
        {
            "source_id": "SRC1372_10_1186_qnorm",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1186_QLOC_NORM_SOURCE_ROWS.csv",
            "required_anchor": "QNR1186_1_norm_row",
            "purpose": "q_loc norm row missing numeric/theorem bound.",
        },
        {
            "source_id": "SRC1372_11_798_gamma",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_798_GAMMA_SOURCE_EXPANSION.csv",
            "required_anchor": "GSE798_2_local_locked_expansion",
            "purpose": "quadratic Gamma_eff gradient suppression around m_*.",
        },
        {
            "source_id": "SRC1372_12_1280_contract",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1280_EPSILON_GK_QLOC_BOUND_CONTRACT.csv",
            "required_anchor": "BND1280_3_no_cancellation",
            "purpose": "componentwise no-cancellation guard for q_loc bounds.",
        },
        {
            "source_id": "SRC1372_13_1011_doublet",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1011_RESPONSED_DOUBLET_THEOREM_ATTEMPT.csv",
            "required_anchor": "RDT1011_7_verdict",
            "purpose": "source-current/boundary zero theorem fails current corpus.",
        },
        {
            "source_id": "SRC1372_14_1244_policy",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1244_RUNNER_POLICY_FEED.csv",
            "required_anchor": "RPF1244_0_policy",
            "purpose": "strict Cassini gamma policy feed for Q_allowed.",
        },
    ]
    for row in rows:
        path = source_path(str(row["source_path"]))
        row["exists"] = path.exists()
        row["anchor_found"] = path.exists() and str(row["required_anchor"]) in read_text(path)
    return mark_nonclaim(rows)


def theorem_attempt_rows() -> list[dict[str, object]]:
    return mark_nonclaim(
        [
            {
                "theorem_id": "LRT1372_0_algebraic_fixed_L0_double_zero",
                "target": "volume+m-chain+L-chain algebraic residual",
                "attempt": "Use fixed L0, Fhat(m_*)=0, Fhat_prime(m_*)=0, and fixed/locked m=m_*.",
                "result": "CLOSED_UNDER_1371_CLOSURE_BRANCH",
                "reason": "1371 exposes volume stress and closes it only under strict vacuum subtraction/double-zero; L0 closes M_L.",
                "remaining_gap": "parent adoption and source-independent m_* still missing",
                "source_paths": "source-intake/mts_residuals/P8_Y5_R10_1371_FIXED_L0_PARENT_ACTION_INSERTION.csv;source-intake/mts_residuals/P8_Y5_R10_798_GAMMA_SOURCE_EXPANSION.csv",
                "source_anchors": "PAI1371_2_strict_double_zero;GSE798_2_local_locked_expansion",
            },
            {
                "theorem_id": "LRT1372_1_connection_terms",
                "target": "K_conn",
                "attempt": "Set connection/derivative metric-response leakage to zero by fixed L0 and algebraic double-zero.",
                "result": "FAIL_NOT_COVERED_BY_ALGEBRAIC_ZERO",
                "reason": "derivative/connection response is an independent open channel in the Kgamma ledger.",
                "remaining_gap": "connection variation or Helmholtz/integrability theorem",
                "source_paths": "source-intake/mts_residuals/P8_Y5_R10_776_KGAMMA_METRIC_RESPONSE_LEDGER.csv;source-intake/mts_residuals/P8_Y5_R10_1291_CHAIN_KERNEL_RESIDUAL_BOUND_LEDGER.csv",
                "source_anchors": "KGL776_2_derivative_terms;KRB1291_2_cdb_bound",
            },
            {
                "theorem_id": "LRT1372_2_domain_projector_terms",
                "target": "K_domain / P_loc commutator",
                "attempt": "Use local exact/trivial domain branch to remove domain selector leakage.",
                "result": "FAIL_CURRENT_CORPUS",
                "reason": "domain selector zero is conditional and R11/source-normalization silence fails current corpus.",
                "remaining_gap": "parent scalar/auxiliary selector proof or numeric domain-product bound",
                "source_paths": "source-intake/mts_residuals/P8_Y5_R10_1117_DOMAIN_ZERO_THEOREM_ATTEMPT.csv;source-intake/mts_residuals/P8_Y5_R10_1117_DOMAIN_COMPONENT_STATUS.csv",
                "source_anchors": "DSZ1117_6_verdict;COMP1117_3_R11_operator",
            },
            {
                "theorem_id": "LRT1372_3_boundary_terms",
                "target": "K_boundary / boundary primitive flux",
                "attempt": "Use compact local topology or natural boundary condition to set boundary term to zero.",
                "result": "FAIL_GENERAL_ZERO_THEOREM",
                "reason": "local topology reduces to a boundary primitive; Neumann/Dirichlet/gauge/Bianchi shortcuts all fail as general theorems.",
                "remaining_gap": "no-flux theorem, boundary primitive zero, or finite edge bound",
                "source_paths": "source-intake/mts_residuals/P8_Y5_R10_1170_BOUNDARY_SPLIT_THEOREM.csv;source-intake/mts_residuals/P8_Y5_R10_1171_BOUNDARY_NO_GO_LEDGER.csv",
                "source_anchors": "BST1170_1_local_top_zero_not_enough;NOG1171_0_neumann_gap",
            },
            {
                "theorem_id": "LRT1372_4_memory_stress",
                "target": "memory kinetic/potential/source/bath stress",
                "attempt": "Use fixed m=m_* and background subtraction to delete all memory-sector stress.",
                "result": "PARTIAL_ONLY",
                "reason": "algebraic potential volume can be subtracted, but kinetic/source/bath/boundary stress is retained unless local no-hair/source silence is proved.",
                "remaining_gap": "constant-m no-hair theorem, source-current zero, source/bath silence",
                "source_paths": "source-intake/mts_residuals/P8_Y5_R10_1301_MEMORY_STRESS_SPLIT_LEDGER.csv;source-intake/mts_residuals/P8_Y5_R10_1011_RESPONSED_DOUBLET_THEOREM_ATTEMPT.csv",
                "source_anchors": "MSS1301_1_memory_kinetic_stress;RDT1011_7_verdict",
            },
            {
                "theorem_id": "LRT1372_5_zero_theorem_verdict",
                "target": "fixed-L0 double-zero local residual theorem",
                "attempt": "Combine algebraic closure with CDB and memory/source stress closure.",
                "result": "ZERO_THEOREM_NOT_DERIVED",
                "reason": "algebraic sector closes conditionally, but K_conn/K_domain/K_boundary and memory/source stress remain live.",
                "remaining_gap": "derive residual theorem or carry Q_norm bound into PPN/R10/clock/orbital lanes",
                "source_paths": "aggregate_1372_theorem_attempt",
                "source_anchors": "LRT1372_0_to_LRT1372_4",
            },
        ]
    )


def qnorm_bound_rows() -> list[dict[str, object]]:
    return mark_nonclaim(
        [
            {
                "bound_id": "QNB1372_0_total_decomposition",
                "quantity": "Q_norm",
                "bound_formula": "Q_norm <= Q_alg + Q_cdb + Q_mem + Q_bdy + Q_trans + Q_proj",
                "status": "SYMBOLIC_DECOMPOSITION_DERIVED",
                "needed_inputs": "all component bounds below; A_ref/norm/domain convention",
                "claim_effect": "turns local theorem failure into a componentwise no-cancellation bound",
            },
            {
                "bound_id": "QNB1372_1_algebraic_quadratic_source",
                "quantity": "Q_alg",
                "bound_formula": "Q_alg <= A_ref^-1 L0^-2 |Fhat''(m_*)| Delta_m Delta_grad_m + O(Delta_m^2 Delta_grad_m)",
                "status": "SYMBOLIC_BOUND_FORM_DERIVED",
                "needed_inputs": "Delta_m;Delta_grad_m;Fhat'';L0;A_ref;local norm",
                "claim_effect": "quadratic suppression is usable only after amplitude/gradient law is sourced",
            },
            {
                "bound_id": "QNB1372_2_cdb_divergence",
                "quantity": "Q_cdb",
                "bound_formula": "Q_cdb <= A_ref^-1 N_div (K_conn_norm + K_domain_norm + K_boundary_norm + K_comm_norm)",
                "status": "SYMBOLIC_BOUND_FORM_DERIVED_INPUTS_MISSING",
                "needed_inputs": "N_div;K_conn_norm;K_domain_norm;K_boundary_norm;K_comm_norm",
                "claim_effect": "CDB residual remains the main local-theorem blocker",
            },
            {
                "bound_id": "QNB1372_3_memory_stress",
                "quantity": "Q_mem",
                "bound_formula": "Q_mem <= A_ref^-1 (N_kin K_mem_kin + N_pot K_mem_drift + N_src J_mem + N_bath B_mem)",
                "status": "SYMBOLIC_BOUND_FORM_DERIVED_INPUTS_MISSING",
                "needed_inputs": "constant-m/no-hair theorem or kinetic/source/bath norms",
                "claim_effect": "memory stress cannot be hidden inside Gamma_eff algebraic closure",
            },
            {
                "bound_id": "QNB1372_4_boundary_flux",
                "quantity": "Q_bdy",
                "bound_formula": "Q_bdy <= A_ref^-1 N_bdy ||pullback(B_C)||_{partial D} plus corner/reference terms",
                "status": "SYMBOLIC_BOUND_FORM_DERIVED_INPUTS_MISSING",
                "needed_inputs": "boundary primitive; boundary measure; no-flux or edge bound",
                "claim_effect": "local topology alone is insufficient; boundary has to be bounded",
            },
            {
                "bound_id": "QNB1372_5_transition_support",
                "quantity": "Q_trans",
                "bound_formula": "Q_trans <= A_ref^-1 (U_B^(2pS) C_S/L_tr + U_B^pL C_L/L_tr + U_B^pT C_T/L_tr)",
                "status": "SYMBOLIC_BOUND_FORM_DERIVED_INPUTS_MISSING",
                "needed_inputs": "U_B;pS;pL;pT;L_tr;C_S;C_L;C_T",
                "claim_effect": "connects 798 screened-source scaling to local residual norm",
            },
            {
                "bound_id": "QNB1372_6_projection_commutator",
                "quantity": "Q_proj",
                "bound_formula": "Q_proj <= A_ref^-1 ||[P_loc, divergence/trace/readout] K_res||",
                "status": "SYMBOLIC_BOUND_FORM_DERIVED_INPUTS_MISSING",
                "needed_inputs": "P_loc definition; domain/readout convention; commutator norm",
                "claim_effect": "keeps projector/readout leakage explicit",
            },
            {
                "bound_id": "QNB1372_7_no_cancellation_policy",
                "quantity": "Q_norm bound policy",
                "bound_formula": "every Q_i is bounded independently; no cancellation between algebraic, cdb, memory, boundary, transition, or projection channels",
                "status": "GUARD_READY",
                "needed_inputs": "componentwise source-backed rows before any pass",
                "claim_effect": "prevents tuned residual cancellations from masquerading as local GR",
            },
        ]
    )


def runner_feed_rows() -> list[dict[str, object]]:
    return mark_nonclaim(
        [
            {
                "feed_id": "QGF1372_0_bound_feed",
                "runner_field": "Q_norm",
                "feed_formula": "Q_norm <= Q_alg + Q_cdb + Q_mem + Q_bdy + Q_trans + Q_proj",
                "status": "SYMBOLIC_FEED_READY",
                "blocks_claim_because": "component values are not numeric/source-backed",
            },
            {
                "feed_id": "QGF1372_1_gamma_bound",
                "runner_field": "B_gamma",
                "feed_formula": "B_gamma <= (c^2/(2U_min)) N_G N_D (Q_alg+Q_cdb+Q_mem+Q_bdy+Q_trans+Q_proj)",
                "status": "SYMBOLIC_CASSINI_BOUND_READY",
                "blocks_claim_because": "U_min,N_G,N_D and Q_i values remain missing",
            },
            {
                "feed_id": "QGF1372_2_acceptance",
                "runner_field": "Q_allowed",
                "feed_formula": "Q_alg+Q_cdb+Q_mem+Q_bdy+Q_trans+Q_proj <= 2 U_min sigma_gamma/(c^2 N_G N_D)",
                "status": "NONCLAIM_ACCEPTANCE_RULE_READY",
                "blocks_claim_because": "left and right sides are symbolic only",
            },
            {
                "feed_id": "QGF1372_3_proxy_guard",
                "runner_field": "old compact-shell proxy",
                "feed_formula": "do not import QBF1011_0=7.432631961576971e-06 as Q_norm",
                "status": "PROXY_NOT_IMPORTED",
                "blocks_claim_because": "mapping into PPN/source-normalization units is missing",
            },
        ]
    )


def claim_gate_rows() -> list[dict[str, object]]:
    return mark_nonclaim(
        [
            {
                "gate_id": "GATE1372_0_algebraic_closure",
                "gate": "fixed-L0 double-zero closes algebraic volume/m/L sector",
                "status": "PASS_CLOSURE_ONLY",
                "reason": "strict 1371 branch closes algebraic pieces but requires parent adoption.",
            },
            {
                "gate_id": "GATE1372_1_cdb_zero",
                "gate": "K_conn/K_domain/K_boundary vanish",
                "status": "BLOCKED",
                "reason": "connection, domain, and boundary no-flux theorems remain unsigned or failed generally.",
            },
            {
                "gate_id": "GATE1372_2_memory_source_zero",
                "gate": "memory kinetic/source/bath stress vanishes",
                "status": "BLOCKED",
                "reason": "local no-hair/source-current/boundary zero theorem is not derived.",
            },
            {
                "gate_id": "GATE1372_3_local_zero_theorem",
                "gate": "q_loc/local residual theorem proves zero",
                "status": "BLOCKED_ZERO_THEOREM_NOT_DERIVED",
                "reason": "algebraic branch is not enough; residual channels remain live.",
            },
            {
                "gate_id": "GATE1372_4_Qnorm_bound",
                "gate": "Q_norm receives usable source-ready symbolic decomposition",
                "status": "PASS_SYMBOLIC_BOUND",
                "reason": "Q_norm decomposition and Cassini feed are now explicit.",
            },
            {
                "gate_id": "GATE1372_5_numeric_runner",
                "gate": "C_qgamma/PPN runner can score numerically",
                "status": "BLOCKED_NUMERIC_INPUTS_MISSING",
                "reason": "Q_i, U_min, N_G, and N_D remain unfilled.",
            },
            {
                "gate_id": "GATE1372_6_local_GR_claim",
                "gate": "local GR / PPN / R10 pass can be claimed",
                "status": "BLOCKED_NO_CLAIM",
                "reason": "no zero theorem and no numeric bound pass.",
            },
        ]
    )


def decision_rows() -> list[dict[str, object]]:
    return mark_nonclaim(
        [
            {
                "decision_id": "DEC1372_0_theorem_status",
                "decision": "do not claim fixed-L0 double-zero local theorem",
                "why": "CDB and memory/source residuals remain live after algebraic closure",
                "next_action": "attempt cdb no-flux theorem or fill Q_cdb/Q_mem bounds",
            },
            {
                "decision_id": "DEC1372_1_Qnorm_route",
                "decision": "carry Q_norm decomposition as the active empirical discipline lane",
                "why": "it turns residual debt into named quantities with an acceptance inequality",
                "next_action": "derive or source Delta_m/Delta_grad_m, K_cdb norms, memory stress norms, and boundary flux norms",
            },
            {
                "decision_id": "DEC1372_2_proxy_policy",
                "decision": "do not use the old compact-shell proxy as a claim value",
                "why": "its units/projection mapping are explicitly missing",
                "next_action": "use it only as a smoke/proxy seed after a mapping row is created",
            },
        ]
    )


def next_rows() -> list[dict[str, object]]:
    return mark_nonclaim(
        [
            {
                "next_id": "NEXT1372_0_1373",
                "next_doc": "1373-Y5-R10-RAB-Qnorm-first-fill-from-fixed-L0-branch-or-cdb-no-flux-theorem.md",
                "next_script": "scripts/Y5_R10_RAB_Qnorm_first_fill_from_fixed_L0_branch_or_cdb_no_flux_theorem.py",
                "task": "attempt to close K_cdb by a fixed-L0 no-flux/domain theorem; if not, create first-fill symbolic/numeric-ready rows for Q_alg, Q_cdb, Q_mem, Q_bdy, Q_trans, and Q_proj",
                "success_condition": "either cdb residuals are theorem-zero under source-backed clauses, or every Q_norm component receives a fill contract with units, source path, and acceptance status",
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
    theorem_attempts: list[dict[str, object]],
    qnorm_bounds: list[dict[str, object]],
    runner_feed: list[dict[str, object]],
    gates: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    all_sources_ok = all(row["exists"] and row["anchor_found"] for row in sources)
    all_nonclaim = all(
        not bool(row.get("valid_for_claim")) and not bool(row.get("claim_allowed"))
        for row in sources + theorem_attempts + qnorm_bounds + runner_feed + gates
    )
    zero_blocked = any(row["theorem_id"] == "LRT1372_5_zero_theorem_verdict" and row["result"] == "ZERO_THEOREM_NOT_DERIVED" for row in theorem_attempts)
    algebraic_closed = any(row["theorem_id"] == "LRT1372_0_algebraic_fixed_L0_double_zero" and row["result"] == "CLOSED_UNDER_1371_CLOSURE_BRANCH" for row in theorem_attempts)
    qnorm_total = any(row["bound_id"] == "QNB1372_0_total_decomposition" and row["status"] == "SYMBOLIC_DECOMPOSITION_DERIVED" for row in qnorm_bounds)
    no_cancellation = any(row["bound_id"] == "QNB1372_7_no_cancellation_policy" and row["status"] == "GUARD_READY" for row in qnorm_bounds)
    runner_ready = any(row["feed_id"] == "QGF1372_2_acceptance" and row["status"] == "NONCLAIM_ACCEPTANCE_RULE_READY" for row in runner_feed)
    proxy_guard = any(row["feed_id"] == "QGF1372_3_proxy_guard" and row["status"] == "PROXY_NOT_IMPORTED" for row in runner_feed)
    local_claim_blocked = any(row["gate_id"] == "GATE1372_6_local_GR_claim" and row["status"] == "BLOCKED_NO_CLAIM" for row in gates)
    csv_ok, csv_details = csv_parse_check(csv_paths)

    rows = [
        {
            "validation_id": "VAL1372_0_sources",
            "check": "every cited local source path exists and anchor is found",
            "status": "PASS" if all_sources_ok else "FAIL",
            "details": "; ".join(f"{row['source_id']} exists={row['exists']} anchor={row['anchor_found']}" for row in sources),
        },
        {
            "validation_id": "VAL1372_1_theorem_attempt",
            "check": "algebraic closure is retained but full zero theorem is blocked",
            "status": "PASS" if algebraic_closed and zero_blocked else "FAIL",
            "details": "fixed-L0 double-zero closes algebraic sector; cdb/memory residuals block theorem",
        },
        {
            "validation_id": "VAL1372_2_Qnorm_bound",
            "check": "Q_norm decomposition and no-cancellation guard are written",
            "status": "PASS" if qnorm_total and no_cancellation else "FAIL",
            "details": "Q_norm <= Q_alg+Q_cdb+Q_mem+Q_bdy+Q_trans+Q_proj",
        },
        {
            "validation_id": "VAL1372_3_runner_feed",
            "check": "C_qgamma runner feed and proxy guard are ready",
            "status": "PASS" if runner_ready and proxy_guard else "FAIL",
            "details": "acceptance inequality is symbolic; old proxy is not imported",
        },
        {
            "validation_id": "VAL1372_4_no_claim_rows",
            "check": "all new rows keep valid_for_claim=false and claim_allowed=false",
            "status": "PASS" if all_nonclaim else "FAIL",
            "details": "1372 is theorem/bound discipline, not a local-GR or PPN pass",
        },
        {
            "validation_id": "VAL1372_5_local_claim_blocked",
            "check": "local GR / PPN / R10 claim remains blocked",
            "status": "PASS" if local_claim_blocked else "FAIL",
            "details": "GATE1372_6_local_GR_claim remains BLOCKED_NO_CLAIM",
        },
        {
            "validation_id": "VAL1372_6_csv_parse",
            "check": "all generated CSVs parse cleanly",
            "status": "PASS" if csv_ok else "FAIL",
            "details": csv_details,
        },
    ]
    overall_ok = all(row["status"] == "PASS" for row in rows)
    rows.append(
        {
            "validation_id": "VAL1372_7_overall",
            "check": "overall 1372 validation",
            "status": "PASS" if overall_ok else "FAIL",
            "details": "1372 blocks the full local zero theorem, preserves algebraic fixed-L0 progress, and creates the Q_norm decomposition/feed.",
        }
    )
    return rows


def write_doc(
    sources: list[dict[str, object]],
    theorem_attempts: list[dict[str, object]],
    qnorm_bounds: list[dict[str, object]],
    runner_feed: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_targets: list[dict[str, object]],
    validations: list[dict[str, object]],
) -> None:
    text = f"""# {TITLE}

**Current verdict:** 1372 does **not** prove the full fixed-`L0` double-zero local residual theorem. It preserves the 1371 algebraic win — fixed `L0` plus strict double-zero closes the volume/`m`/`L_cg` algebraic pieces — but `K_conn`, `K_domain`, `K_boundary`, and memory/source stress remain live.

**Main progress:** the fallback is now useful instead of vague. The local residual norm is decomposed as `Q_norm <= Q_alg + Q_cdb + Q_mem + Q_bdy + Q_trans + Q_proj`, with no cancellation allowed between channels. This turns the local-GR blocker into a concrete shopping list.

**Testing progress:** the `C_qgamma` runner can now consume the symbolic feed `B_gamma <= (c^2/(2U_min)) N_G N_D Q_norm`. The nonclaim acceptance rule is `Q_alg+Q_cdb+Q_mem+Q_bdy+Q_trans+Q_proj <= 2 U_min sigma_gamma/(c^2 N_G N_D)`. No numeric pass is made.

## Source Register

{table(["source_id", "source_path", "required_anchor", "exists", "anchor_found", "purpose", "valid_for_claim", "claim_allowed"], sources)}

## Local Residual Theorem Attempt

{table(["theorem_id", "target", "result", "attempt", "reason", "remaining_gap", "source_paths", "source_anchors", "valid_for_claim", "claim_allowed"], theorem_attempts)}

## `Q_norm` Decomposition Bound

{table(["bound_id", "quantity", "status", "bound_formula", "needed_inputs", "claim_effect", "valid_for_claim", "claim_allowed"], qnorm_bounds)}

## `C_qgamma` Runner Feed

{table(["feed_id", "runner_field", "status", "feed_formula", "blocks_claim_because", "valid_for_claim", "claim_allowed"], runner_feed)}

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
    theorem_attempts = theorem_attempt_rows()
    qnorm_bounds = qnorm_bound_rows()
    runner_feed = runner_feed_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_targets = next_rows()

    write_csv(SOURCE_REGISTER_PATH, sources)
    write_csv(THEOREM_ATTEMPT_PATH, theorem_attempts)
    write_csv(QNORM_BOUND_PATH, qnorm_bounds)
    write_csv(RUNNER_FEED_PATH, runner_feed)
    write_csv(CLAIM_GATE_PATH, gates)
    write_csv(DECISION_PATH, decisions)
    write_csv(NEXT_PATH, next_targets)

    csv_paths = [
        SOURCE_REGISTER_PATH,
        THEOREM_ATTEMPT_PATH,
        QNORM_BOUND_PATH,
        RUNNER_FEED_PATH,
        CLAIM_GATE_PATH,
        DECISION_PATH,
        NEXT_PATH,
    ]
    validations = validation_rows(sources, theorem_attempts, qnorm_bounds, runner_feed, gates, csv_paths)
    write_csv(VALIDATION_PATH, validations)
    write_doc(sources, theorem_attempts, qnorm_bounds, runner_feed, gates, decisions, next_targets, validations)

    print(f"wrote {DOC_PATH}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"formalization-workbench touched by this script: {FORMALIZATION.exists() and False}")


if __name__ == "__main__":
    main()
