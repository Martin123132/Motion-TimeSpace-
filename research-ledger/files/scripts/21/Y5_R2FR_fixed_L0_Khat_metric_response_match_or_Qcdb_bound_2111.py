from __future__ import annotations

from pathlib import Path

from Y5_R2FR_Dq_vX_observed_metric_zero_or_finite_DObs_leak_row_2025 import (
    BRANCH_WEP,
    OUT,
    QUEUE,
    ROOT,
    SOURCE_WEIGHT_DOCS,
    base_row,
    count_formalization_modified,
    csv_rows_parse,
    md_table,
    read_text,
    remove_pycache,
    write_csv,
)


DOC = ROOT / "2111-Y5-R2FR-fixed-L0-Khat-metric-response-match-or-Qcdb-bound.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

SRC_2110_DOC = ROOT / "2110-Y5-R2FR-Gamma-Khat-q_loc-parent-action-owner-or-DqZ-GK-tail-bound.md"
CSV_2110_VAL = OUT / "P8_Y5_BRR545_2110_VALIDATION.csv"
CSV_2110_NEXT = OUT / "P8_Y5_PARENT_QLOC_2110_NEXT_TARGET.csv"
CSV_2110_RESIDUAL = OUT / "P8_Y5_PARENT_QLOC_2110_QNORM_RESIDUAL_BOUND_LEDGER.csv"

SRC_1366_DOC = ROOT / "1366-Y5-R10-RAB-Gamma-eff-scalar-density-definition-hunt-or-q_loc-envelope.md"
CSV_1366_KMATCH = OUT / "P8_Y5_R10_1366_KMETRIC_KHAT_MATCH_LEDGER.csv"

SRC_1371_DOC = ROOT / "1371-Y5-R10-RAB-fixed-Lcg-parent-action-insertion-or-Cqgamma-norm-bound.md"
CSV_1371_ACTION = OUT / "P8_Y5_R10_1371_FIXED_L0_PARENT_ACTION_INSERTION.csv"
CSV_1371_RESIDUAL = OUT / "P8_Y5_R10_1371_LOCAL_RESIDUAL_ZERO_OR_BOUND_LEDGER.csv"

SRC_1372_DOC = ROOT / "1372-Y5-R10-RAB-fixed-L0-double-zero-local-residual-theorem-or-Qnorm-bound.md"
CSV_1372_THEOREM = OUT / "P8_Y5_R10_1372_LOCAL_RESIDUAL_THEOREM_ATTEMPT.csv"
CSV_1372_QNORM = OUT / "P8_Y5_R10_1372_QNORM_DECOMPOSITION_BOUND.csv"

SRC_1590_DOC = ROOT / "1590-Y5-R2FR-Gamma-Khat-Ploc-owner-bundle-or-cR2-finite-coefficient-row.md"
CSV_1590_FIXED = OUT / "P8_Y5_PARENT_QLOC_1590_FIXED_L0_DOUBLE_ZERO_CONTRACT_GATE.csv"


def row(**kwargs: object) -> dict[str, object]:
    data = base_row()
    data["claim_allowed"] = False
    data.update(kwargs)
    return data


def truthy(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "1", "yes", "pass", "valid", "claim_allowed", "selected"}


def formalization_has_2111_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2111-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2111*",
        "*Y5_R2FR_fixed_L0_Khat_metric_response_match_or_Qcdb_bound_2111*",
        "*AFRAME_KHAT_RESPONSE_2111*",
        "*JR2111_CDB*",
    )
    try:
        return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))
    except Exception:
        return False


def source_register_rows() -> list[dict[str, object]]:
    source_specs = [
        (
            "SRC2111_00_2110_doc",
            SRC_2110_DOC,
            ["NEXT2110_0_2111", "MISSING_EXPLICIT_GAMMA_KGAMMA_MATCH", "Q_cdb"],
            "2110 selects fixed-L0 Khat metric-response match as the next fork.",
        ),
        (
            "SRC2111_01_2110_validation",
            CSV_2110_VAL,
            ["VAL2110_OVERALL", "PASS", "formalization-workbench untouched"],
            "2110 validation passed and kept this phase private.",
        ),
        (
            "SRC2111_02_2110_residuals",
            CSV_2110_RESIDUAL,
            ["QNR2110_2_Q_cdb", "K_conn_norm", "K_domain_norm", "K_boundary_norm", "no-cancellation"],
            "2110 retained the finite Q_cdb residual lane.",
        ),
        (
            "SRC2111_03_1366_doc",
            SRC_1366_DOC,
            ["Gamma_eff=L_cg^-2 F(m)", "MISSING_EXPLICIT_GAMMA_KGAMMA_MATCH", "K_conn+K_domain+K_boundary"],
            "1366 supplies the nonclaim Gamma_eff shape and old Kmetric/Khat gap.",
        ),
        (
            "SRC2111_04_1366_kmatch",
            CSV_1366_KMATCH,
            ["MATCH1366_2_Kmetric_kernel", "MATCH1366_3_live_Khat_comparison", "CLAIM_BLOCKED"],
            "1366 Kmetric/Khat rows keep Delta_K active.",
        ),
        (
            "SRC2111_05_1371_doc",
            SRC_1371_DOC,
            ["Fixed `L_cg=L0`", "strict double-zero", "K_conn, K_domain, K_boundary"],
            "1371 exposes the volume term and closes only the algebraic branch under strict clauses.",
        ),
        (
            "SRC2111_06_1371_action",
            CSV_1371_ACTION,
            ["PAI1371_1_volume_stress_gate", "PAI1371_2_strict_double_zero", "PAI1371_3_first_variation_result"],
            "1371 action insertion is the fixed-L0 double-zero source for the algebraic response split.",
        ),
        (
            "SRC2111_07_1371_residual",
            CSV_1371_RESIDUAL,
            ["LRZ1371_0_volume", "LRZ1371_4_cdb_terms", "OPEN_RETAINED_RESIDUAL"],
            "1371 residual ledger says CDB terms survive the algebraic closure.",
        ),
        (
            "SRC2111_08_1372_doc",
            SRC_1372_DOC,
            ["ZERO_THEOREM_NOT_DERIVED", "Q_norm <= Q_alg + Q_cdb + Q_mem + Q_bdy + Q_trans + Q_proj"],
            "1372 preserves the fixed-L0 algebraic win and the componentwise bound lane.",
        ),
        (
            "SRC2111_09_1372_theorem",
            CSV_1372_THEOREM,
            ["LRT1372_0_algebraic_fixed_L0_double_zero", "LRT1372_1_connection_terms", "ZERO_THEOREM_NOT_DERIVED"],
            "1372 theorem attempt separates algebraic closure from connection/domain/boundary failure.",
        ),
        (
            "SRC2111_10_1372_qnorm",
            CSV_1372_QNORM,
            ["QNB1372_2_cdb_divergence", "K_conn_norm", "QNB1372_7_no_cancellation_policy"],
            "1372 gives the previous Q_cdb formula and no-cancellation rule.",
        ),
        (
            "SRC2111_11_1590_fixed",
            CSV_1590_FIXED,
            ["FLG1590_2_algebraic_closure", "FLG1590_3_cdb_residuals", "ZERO_THEOREM_NOT_DERIVED"],
            "1590 confirms the fixed-L0 double-zero branch is closure-only, not local-GR proof.",
        ),
        (
            "SRC2111_12_1590_doc",
            SRC_1590_DOC,
            ["fixed `L0`", "K_conn/K_domain/K_boundary", "No R2/fR"],
            "1590 keeps local-GR promotion blocked while preserving the finite coefficient lane.",
        ),
    ]
    rows: list[dict[str, object]] = []
    for source_id, path, needles, role in source_specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        found = all(needle in text for needle in needles)
        rows.append(
            row(
                source_id=source_id,
                source_path=str(path),
                path_exists=exists,
                expected_needles="; ".join(needles),
                needles_found=found,
                role=role,
            )
        )
    return rows


def response_split_rows() -> list[dict[str, object]]:
    rows_data = [
        (
            "KRS2111_0_total_split",
            "K_metric^0[Gamma_eff]",
            "K_metric^0 = K_vol + K_m + K_L + K_conn + K_domain + K_boundary + K_proj",
            "DECOMPOSITION_WRITTEN",
            "Hilbert response is split before trying to identify it with live K_hat.",
            "term-by-term parent signature and live tensor comparison",
            "Delta_K",
        ),
        (
            "KRS2111_1_volume",
            "K_vol",
            "K_vol^{mu nu} proportional to L0^-2 Fhat(m_*) g^{mu nu}",
            "CLOSED_UNDER_STRICT_DOUBLE_ZERO_CLOSURE",
            "Fhat(m_*)=0 or source-independent subtraction deletes the metric-proportional volume term.",
            "parent adoption of subtraction and local vacuum branch",
            "none under closure",
        ),
        (
            "KRS2111_2_m_chain",
            "K_m",
            "K_m^{mu nu} proportional to L0^-2 Fhat_prime(m_*) M_m^{mu nu}",
            "CLOSED_UNDER_FIXED_FIELD_DOUBLE_ZERO_CLOSURE",
            "Fhat_prime(m_*)=0 makes the first m-chain response vanish at the local vacuum.",
            "fixed/locked m branch and amplitude law for departures",
            "Q_alg if displaced",
        ),
        (
            "KRS2111_3_L_chain",
            "K_L",
            "K_L^{mu nu} proportional to delta L0 / delta g_{mu nu}",
            "CLOSED_UNDER_FIXED_L0_CLOSURE",
            "L0 is treated as parent fixed constant, not live readout length.",
            "parent notation split between L0 and empirical readout lengths",
            "none under closure",
        ),
        (
            "KRS2111_4_connection",
            "K_conn",
            "metric response of connection/derivative dependence hidden in Gamma_eff or K_hat",
            "OPEN_RETAINED_RESIDUAL",
            "Fixed L0 and double-zero do not by themselves remove derivative/connection kernels.",
            "explicit connection dependence theorem or component norm",
            "Q_cdb",
        ),
        (
            "KRS2111_5_domain",
            "K_domain",
            "metric response of local domain/window/support/readout selection",
            "OPEN_RETAINED_RESIDUAL",
            "Local domain silence is not automatic; domain variation can feed Delta_K.",
            "domain descent/no-leak theorem or component norm",
            "Q_cdb",
        ),
        (
            "KRS2111_6_boundary",
            "K_boundary",
            "boundary primitive, corner, and no-flux response from integration by parts",
            "OPEN_RETAINED_RESIDUAL",
            "Compact/local topology alone does not prove boundary primitive silence.",
            "boundary no-flux theorem or edge/corner bound",
            "Q_cdb/Q_bdy",
        ),
        (
            "KRS2111_7_projector",
            "K_proj",
            "[P_loc, divergence/trace/readout] response leakage",
            "OPEN_RETAINED_RESIDUAL",
            "The projector/readout commutator has to be owned by the parent branch.",
            "explicit P_loc definition and commutator norm/zero theorem",
            "Q_proj/Q_cdb",
        ),
        (
            "KRS2111_8_deltaK",
            "Delta_K^{mu nu}",
            "Delta_K = K_hat_live - K_metric^0[Gamma_eff]",
            "MISSING_EXPLICIT_GAMMA_KGAMMA_MATCH",
            "Algebraic pieces close, but live K_hat has not been matched term-by-term.",
            "live K_hat components and CDB/projector comparison",
            "Q_cdb finite tail",
        ),
    ]
    return [
        row(
            split_id=split_id,
            term=term,
            fixed_L0_response=response,
            current_status=status,
            proof_or_bound=proof,
            missing_for_claim=missing,
            residual_channel=residual,
            score_ready=False,
        )
        for split_id, term, response, status, proof, missing, residual in rows_data
    ]


def khat_match_gate_rows() -> list[dict[str, object]]:
    rows_data = [
        (
            "KMG2111_0_conditional_theorem",
            "If S_GK^0 is the parent scalar-density action, K_hat is its Hilbert response, CDB/projector/boundary terms vanish, and P_loc commutes with the local divergence/readout, then Delta_K=0.",
            "CONDITIONAL_THEOREM_WRITTEN",
            "This is the clean route from Gamma closure to q_loc silence.",
            "parent signatures for every clause",
        ),
        (
            "KMG2111_1_fixed_L0_double_zero",
            "fixed L0 plus Fhat(m_*)=0 and Fhat_prime(m_*)=0",
            "CLOSED_UNDER_CLOSURE_ONLY",
            "Volume, m-chain, and L-chain response can be made silent.",
            "parent adoption and amplitude law for off-vacuum departures",
        ),
        (
            "KMG2111_2_algebraic_match",
            "K_metric^alg -> 0 at local vacuum",
            "ALGEBRAIC_RESPONSE_MATCH_CONDITIONAL",
            "The old algebraic blocker is no longer the main issue.",
            "strict same-branch closure clauses",
        ),
        (
            "KMG2111_3_live_Khat",
            "live K_hat tensor definition",
            "MISSING_LIVE_PARENT_TENSOR",
            "No current source gives the explicit live K_hat components to compare.",
            "parent K_hat definition with units and indices",
        ),
        (
            "KMG2111_4_connection",
            "K_conn term",
            "OPEN_RETAINED_RESIDUAL",
            "Derivative/connection metric response may survive the algebraic double-zero.",
            "connection zero theorem or K_conn_norm",
        ),
        (
            "KMG2111_5_domain",
            "K_domain term",
            "OPEN_RETAINED_RESIDUAL",
            "Domain/readout selection can vary with the metric unless descent is signed.",
            "domain descent zero theorem or K_domain_norm",
        ),
        (
            "KMG2111_6_boundary",
            "K_boundary term",
            "OPEN_RETAINED_RESIDUAL",
            "Boundary primitives remain live unless no-flux/corner conditions are signed.",
            "boundary zero theorem or K_boundary_norm",
        ),
        (
            "KMG2111_7_projector_commutator",
            "P_loc commutator",
            "OPEN_RETAINED_RESIDUAL",
            "P_loc cannot be assumed to commute with divergence/readout.",
            "commutator zero theorem or K_comm_norm",
        ),
        (
            "KMG2111_8_verdict",
            "K_hat=K_metric[Gamma_eff] promotion",
            "FAIL_CURRENT_CLAIM",
            "Only algebraic response is conditionally closed; live CDB/projector match is unsigned.",
            "derive CDB zeros or source component bounds",
        ),
    ]
    return [
        row(
            gate_id=gate_id,
            requirement=requirement,
            current_status=status,
            what_it_proves=proves,
            still_missing=missing,
            score_ready=False,
        )
        for gate_id, requirement, status, proves, missing in rows_data
    ]


def qcdb_bound_rows() -> list[dict[str, object]]:
    rows_data = [
        (
            "QCB2111_0_Delta_K",
            "Delta_K^{mu nu}",
            "Delta_K^{mu nu}=K_hat_live^{mu nu}-K_metric0^{mu nu}[Gamma_eff]",
            "SYMBOLIC_RESIDUAL_DEFINITION_READY",
            "live K_hat; Kmetric CDB kernels; norm convention",
            "metric-response mismatch source",
        ),
        (
            "QCB2111_1_Q_cdb",
            "Q_cdb",
            "Q_cdb <= A_ref^-1 N_div (K_conn_norm + K_domain_norm + K_boundary_norm + K_comm_norm + Delta_K_live_norm)",
            "SYMBOLIC_BOUND_FORM_DERIVED_INPUTS_MISSING",
            "A_ref;N_div;K_conn_norm;K_domain_norm;K_boundary_norm;K_comm_norm;Delta_K_live_norm",
            "main local-GR residual lane",
        ),
        (
            "QCB2111_2_K_conn_norm",
            "K_conn_norm",
            "sup_D ||K_conn|| in the selected local norm",
            "MISSING_COMPONENT_VALUE_OR_ZERO_THEOREM",
            "connection dependence of Gamma_eff/K_hat or no-connection parent theorem",
            "connection leakage",
        ),
        (
            "QCB2111_3_K_domain_norm",
            "K_domain_norm",
            "sup_D ||delta_g window/domain/readout contribution||",
            "MISSING_COMPONENT_VALUE_OR_ZERO_THEOREM",
            "domain descent or local support variation bound",
            "domain leakage",
        ),
        (
            "QCB2111_4_K_boundary_norm",
            "K_boundary_norm",
            "||pullback(B_K)||_{partial D} plus corner/reference terms",
            "MISSING_COMPONENT_VALUE_OR_ZERO_THEOREM",
            "boundary primitive, measure, no-flux, corner convention",
            "boundary leakage",
        ),
        (
            "QCB2111_5_K_comm_norm",
            "K_comm_norm",
            "||[P_loc, divergence/trace/readout]K_res||",
            "MISSING_COMPONENT_VALUE_OR_ZERO_THEOREM",
            "P_loc definition and commutator theorem/bound",
            "projector leakage",
        ),
        (
            "QCB2111_6_q_loc_feed",
            "q_loc^nu",
            "||P_loc nabla_mu Delta_K^{mu nu}|| <= N_div ||Delta_K|| plus projector commutator",
            "SYMBOLIC_FEED_READY_INPUTS_MISSING",
            "N_div;local norm;projector commutator;component values",
            "PPN/local residual feed",
        ),
        (
            "QCB2111_7_no_cancellation",
            "policy",
            "each CDB/projector component is bounded independently; cancellation cannot be used for a pass",
            "GUARD_READY",
            "componentwise values or zero theorems",
            "prevents tuned local silence",
        ),
        (
            "QCB2111_8_verdict",
            "Q_cdb score row",
            "score only after every component is sourced, positive-normed, unit-tagged, and non-placeholder",
            "CLAIM_BLOCKED_NUMERIC_INPUTS_MISSING",
            "all QCB2111_1 through QCB2111_6 inputs",
            "no R10/PPN/local-GR claim",
        ),
    ]
    return [
        row(
            bound_id=bound_id,
            quantity=quantity,
            bound_formula=formula,
            current_status=status,
            needed_inputs=needed,
            claim_effect=effect,
            score_ready=False,
        )
        for bound_id, quantity, formula, status, needed, effect in rows_data
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    rows_data = [
        ("GATE2111_0_algebraic_closure", "fixed-L0 algebraic Hilbert response closes", True, "volume/m/L chains close under strict branch clauses"),
        ("GATE2111_1_live_Khat_match", "live K_hat equals K_metric[Gamma_eff]", False, "CDB/projector/boundary terms are not parent-signed"),
        ("GATE2111_2_CDB_zero_theorem", "K_conn/K_domain/K_boundary/K_comm all vanish", False, "no component zero theorem exists yet"),
        ("GATE2111_3_Qcdb_bound_lane", "finite Q_cdb bound lane is explicit", True, "symbolic residual formula and inputs are listed"),
        ("GATE2111_4_local_GR_Newton", "derived local GR/Newton follows", False, "Delta_K and Q_cdb remain live"),
        ("GATE2111_5_PPN_claim", "PPN residual acceptable", False, "no numeric component values or arena projection"),
    ]
    return [
        row(
            gate_id=gate_id,
            gate=gate,
            gate_pass=passes,
            rationale=rationale,
            score_ready=False,
        )
        for gate_id, gate, passes, rationale in rows_data
    ]


def decision_rows() -> list[dict[str, object]]:
    rows_data = [
        (
            "DEC2111_0_progress",
            "ALGEBRAIC_RESPONSE_NO_LONGER_MAIN_BLOCKER",
            "Fixed L0 plus strict double-zero closes the volume, m-chain and L-chain response under closure clauses.",
            "Do not reopen old M_L/volume loops unless parent branch changes.",
        ),
        (
            "DEC2111_1_no_promotion",
            "KHAT_MATCH_FAILS_CURRENT_CLAIM",
            "The live K_hat tensor and CDB/projector/boundary response are unsigned.",
            "Keep Delta_K and Q_cdb rows nonclaim.",
        ),
        (
            "DEC2111_2_next",
            "CDB_COMPONENTS_NEXT",
            "This is the smallest remaining non-algebraic obstruction to local GR/Newton from the GK route.",
            "Try to zero or bound K_conn, K_domain, K_boundary and K_comm component by component.",
        ),
    ]
    return [
        row(
            decision_id=decision_id,
            decision=decision,
            because=because,
            next_action=next_action,
        )
        for decision_id, decision, because, next_action in rows_data
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        row(
            route_id="NEXT2111_0_2112",
            next_target="2112-Y5-R2FR-CDB-component-zero-or-bound-Kconn-Kdomain-Kboundary.md",
            script="scripts/Y5_R2FR_CDB_component_zero_or_bound_Kconn_Kdomain_Kboundary_2112.py",
            objective=(
                "Under the fixed-L0 double-zero branch, try to derive actual zero theorems or source-ready finite bounds "
                "for K_conn, K_domain, K_boundary and K_comm. Promote nothing unless every component is either zero by "
                "parent descent/no-flux/commutator theorem or bounded with units, source paths and norm conventions."
            ),
            forbidden_shortcuts=(
                "declaring CDB zero by local intuition; deleting boundary terms by compactness alone; hiding projector "
                "leakage in notation; using cancellation between components; local-GR/Newton/PPN claim; "
                "formalization-workbench edits; GitHub action"
            ),
        )
    ]


def write_branch_copies(
    response_split: list[dict[str, object]],
    match_gates: list[dict[str, object]],
    qcdb_bounds: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> list[dict[str, object]]:
    copy_specs = [
        (
            "COPY2111_0_source_weight_docs",
            SOURCE_WEIGHT_DOCS / "AFRAME_KHAT_RESPONSE_2111_NONCLAIM.csv",
            response_split + match_gates + qcdb_bounds,
        ),
        (
            "COPY2111_1_branch_locked_wep",
            BRANCH_WEP / "P8_Y5_PARENT_QLOC_2111_KHAT_RESPONSE_STATUS_NONCLAIM.csv",
            match_gates + qcdb_bounds,
        ),
        (
            "COPY2111_2_acquisition_queue",
            QUEUE / "JR2111_CDB_COMPONENT_ZERO_OR_BOUND_QUEUE.csv",
            next_target + qcdb_bounds,
        ),
    ]
    rows: list[dict[str, object]] = []
    for copy_id, destination, copy_rows in copy_specs:
        write_csv(destination, copy_rows)
        rows.append(
            row(
                copy_id=copy_id,
                destination=str(destination),
                path_exists=destination.exists(),
                row_count=len(copy_rows),
                parse_ok=csv_rows_parse(destination),
            )
        )
    return rows


def all_nonclaim(table_groups: list[list[dict[str, object]]]) -> bool:
    for table in table_groups:
        for table_row in table:
            if truthy(table_row.get("claim_allowed")) or truthy(table_row.get("valid_for_claim")):
                return False
    return True


def validation_rows(
    sources: list[dict[str, object]],
    response_split: list[dict[str, object]],
    match_gates: list[dict[str, object]],
    qcdb_bounds: list[dict[str, object]],
    claim_gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_target: list[dict[str, object]],
    copies: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    source_ok = all(truthy(source.get("path_exists")) and truthy(source.get("needles_found")) for source in sources)
    split_ok = (
        any(split.get("split_id") == "KRS2111_1_volume" and split.get("current_status") == "CLOSED_UNDER_STRICT_DOUBLE_ZERO_CLOSURE" for split in response_split)
        and any(split.get("split_id") == "KRS2111_2_m_chain" and split.get("current_status") == "CLOSED_UNDER_FIXED_FIELD_DOUBLE_ZERO_CLOSURE" for split in response_split)
        and any(split.get("split_id") == "KRS2111_4_connection" and split.get("current_status") == "OPEN_RETAINED_RESIDUAL" for split in response_split)
        and any(split.get("split_id") == "KRS2111_8_deltaK" and split.get("current_status") == "MISSING_EXPLICIT_GAMMA_KGAMMA_MATCH" for split in response_split)
    )
    match_ok = (
        any(gate.get("gate_id") == "KMG2111_3_live_Khat" and gate.get("current_status") == "MISSING_LIVE_PARENT_TENSOR" for gate in match_gates)
        and any(gate.get("gate_id") == "KMG2111_8_verdict" and gate.get("current_status") == "FAIL_CURRENT_CLAIM" for gate in match_gates)
    )
    qcdb_ok = (
        any(bound.get("bound_id") == "QCB2111_1_Q_cdb" and bound.get("current_status") == "SYMBOLIC_BOUND_FORM_DERIVED_INPUTS_MISSING" for bound in qcdb_bounds)
        and any(bound.get("bound_id") == "QCB2111_7_no_cancellation" and bound.get("current_status") == "GUARD_READY" for bound in qcdb_bounds)
    )
    gates_ok = (
        any(gate.get("gate_id") == "GATE2111_0_algebraic_closure" and truthy(gate.get("gate_pass")) for gate in claim_gates)
        and any(gate.get("gate_id") == "GATE2111_4_local_GR_Newton" and not truthy(gate.get("gate_pass")) for gate in claim_gates)
        and any(gate.get("gate_id") == "GATE2111_3_Qcdb_bound_lane" and truthy(gate.get("gate_pass")) for gate in claim_gates)
    )
    decision_ok = any(decision.get("decision_id") == "DEC2111_2_next" and decision.get("decision") == "CDB_COMPONENTS_NEXT" for decision in decisions)
    next_ok = any(
        target.get("route_id") == "NEXT2111_0_2112" and "CDB-component-zero-or-bound" in str(target.get("next_target"))
        for target in next_target
    )
    copies_ok = all(truthy(copy.get("path_exists")) and truthy(copy.get("parse_ok")) and int(copy.get("row_count", 0)) > 0 for copy in copies)
    csv_ok = all(path.exists() and csv_rows_parse(path) for path in csv_paths)
    no_claims_ok = all_nonclaim([sources, response_split, match_gates, qcdb_bounds, claim_gates, decisions, next_target, copies])
    formalization_ok = count_formalization_modified() == 0 and not formalization_has_2111_artifacts()
    no_pycache_ok = not (Path(__file__).resolve().parent / "__pycache__").exists()

    checks = [
        ("VAL2111_00_sources", source_ok, "all cited sources exist and contain fixed-L0/Khat/Qcdb needles"),
        ("VAL2111_01_response_split", split_ok, "response split closes algebraic pieces but leaves CDB/Delta_K live"),
        ("VAL2111_02_khat_match", match_ok, "live Khat match fails current claim instead of being asserted by notation"),
        ("VAL2111_03_qcdb_bound", qcdb_ok, "Q_cdb residual bound and no-cancellation guard are explicit"),
        ("VAL2111_04_claim_gates", gates_ok, "algebraic closure passes but local-GR/Newton remains blocked"),
        ("VAL2111_05_decision", decision_ok, "decision selects CDB component zero/bound hunt next"),
        ("VAL2111_06_next", next_ok, "next target is 2112 CDB component zero-or-bound"),
        ("VAL2111_07_branch_copies", copies_ok, "branch copies exist and parse"),
        ("VAL2111_08_csv_parse", csv_ok, "all generated CSVs parse cleanly"),
        ("VAL2111_09_no_claim_flags", no_claims_ok, "no generated row allows a claim or score"),
        ("VAL2111_10_formalization_clean", formalization_ok, "formalization-workbench untouched by 2111"),
        ("VAL2111_11_no_pycache", no_pycache_ok, "scripts __pycache__ removed"),
    ]
    validation = [
        row(
            check_id=check_id,
            status="PASS" if passed else "FAIL",
            detail=detail,
        )
        for check_id, passed, detail in checks
    ]
    overall_ok = all(validation_row["status"] == "PASS" for validation_row in validation)
    validation.append(
        row(
            check_id="VAL2111_OVERALL",
            status="PASS" if overall_ok else "FAIL",
            detail=(
                "2111 proves the fixed-L0 algebraic response split is no longer the main blocker, "
                "rejects live Khat promotion, and retains Q_cdb/Delta_K as the next finite residual target."
            ),
        )
    )
    return validation


def write_doc(
    sources: list[dict[str, object]],
    response_split: list[dict[str, object]],
    match_gates: list[dict[str, object]],
    qcdb_bounds: list[dict[str, object]],
    claim_gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_target: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    content = "\n".join(
        [
            "# 2111 - Y5/R2FR Fixed-L0 Khat Metric-Response Match Or Qcdb Bound",
            "",
            "## Current Verdict",
            "",
            "2111 is progress, but not a local-GR claim. Under the fixed-`L0` and strict double-zero branch, the algebraic Hilbert response from `Gamma_eff` can be split cleanly: the volume term, first `m`-chain term, and `L_cg` chain are silent under the same closure clauses already isolated in 1371/1590.",
            "",
            "The live match `K_hat = K_metric[Gamma_eff]` still fails as a current claim. The unresolved terms are no longer vague: they are `K_conn`, `K_domain`, `K_boundary`, and the `P_loc` commutator/readout leakage. Therefore `Delta_K` and `Q_cdb` remain explicit finite residual rows, with no cancellation allowed.",
            "",
            "This means the route has moved from broad doubt to a precise fork: either derive zero theorems for the CDB/projector components, or source component bounds and carry them into the local PPN residual lane.",
            "",
            "## Source Register",
            md_table(sources, ["source_id", "source_path", "path_exists", "needles_found", "role", "valid_for_claim"]),
            "## Fixed-L0 Response Split",
            md_table(response_split, ["split_id", "term", "current_status", "fixed_L0_response", "proof_or_bound", "missing_for_claim", "residual_channel", "valid_for_claim"]),
            "## Khat Match Gate",
            md_table(match_gates, ["gate_id", "requirement", "current_status", "what_it_proves", "still_missing", "valid_for_claim"]),
            "## Qcdb / Delta-K Bound Ledger",
            md_table(qcdb_bounds, ["bound_id", "quantity", "current_status", "bound_formula", "needed_inputs", "claim_effect", "valid_for_claim"]),
            "## Claim Gates",
            md_table(claim_gates, ["gate_id", "gate", "gate_pass", "rationale", "valid_for_claim", "claim_allowed"]),
            "## Decision Ledger",
            md_table(decisions, ["decision_id", "decision", "because", "next_action", "valid_for_claim"]),
            "## Next Target",
            md_table(next_target, ["route_id", "next_target", "script", "objective", "forbidden_shortcuts", "valid_for_claim"]),
            "## Branch Copies",
            md_table(copies, ["copy_id", "destination", "path_exists", "row_count", "parse_ok", "valid_for_claim"]),
            "## Validation",
            md_table(validation, ["check_id", "status", "detail", "claim_allowed", "valid_for_claim"]),
        ]
    )
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    SOURCE_WEIGHT_DOCS.mkdir(parents=True, exist_ok=True)
    BRANCH_WEP.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)

    sources = source_register_rows()
    response_split = response_split_rows()
    match_gates = khat_match_gate_rows()
    qcdb_bounds = qcdb_bound_rows()
    claim_gates = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_target_rows()

    paths = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2111_SOURCE_REGISTER.csv",
        "response": OUT / "P8_Y5_PARENT_QLOC_2111_KMETRIC_RESPONSE_SPLIT.csv",
        "match": OUT / "P8_Y5_PARENT_QLOC_2111_KHAT_MATCH_GATE.csv",
        "qcdb": OUT / "P8_Y5_PARENT_QLOC_2111_QCDB_BOUND_LEDGER.csv",
        "gates": OUT / "P8_Y5_PARENT_QLOC_2111_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_PARENT_QLOC_2111_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2111_NEXT_TARGET.csv",
        "branch": OUT / "P8_Y5_PARENT_QLOC_2111_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2111_VALIDATION.csv",
    }

    write_csv(paths["sources"], sources)
    write_csv(paths["response"], response_split)
    write_csv(paths["match"], match_gates)
    write_csv(paths["qcdb"], qcdb_bounds)
    write_csv(paths["gates"], claim_gates)
    write_csv(paths["decisions"], decisions)
    write_csv(paths["next"], next_target)

    copies = write_branch_copies(response_split, match_gates, qcdb_bounds, next_target)
    write_csv(paths["branch"], copies)

    remove_pycache()

    csv_paths = [path for key, path in paths.items() if key != "validation"] + [Path(str(copy["destination"])) for copy in copies]
    validation = validation_rows(sources, response_split, match_gates, qcdb_bounds, claim_gates, decisions, next_target, copies, csv_paths)
    write_csv(paths["validation"], validation)
    write_doc(sources, response_split, match_gates, qcdb_bounds, claim_gates, decisions, next_target, copies, validation)

    print(f"wrote {DOC}")
    print(f"validation {paths['validation']}")


if __name__ == "__main__":
    main()
