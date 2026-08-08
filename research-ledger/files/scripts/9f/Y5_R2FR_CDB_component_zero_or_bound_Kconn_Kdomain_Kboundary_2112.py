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


DOC = ROOT / "2112-Y5-R2FR-CDB-component-zero-or-bound-Kconn-Kdomain-Kboundary.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

SRC_2111_DOC = ROOT / "2111-Y5-R2FR-fixed-L0-Khat-metric-response-match-or-Qcdb-bound.md"
CSV_2111_VAL = OUT / "P8_Y5_BRR545_2111_VALIDATION.csv"
CSV_2111_QCDB = OUT / "P8_Y5_PARENT_QLOC_2111_QCDB_BOUND_LEDGER.csv"
CSV_2111_NEXT = OUT / "P8_Y5_PARENT_QLOC_2111_NEXT_TARGET.csv"

CSV_1291_CDB = OUT / "P8_Y5_R10_1291_CHAIN_KERNEL_RESIDUAL_BOUND_LEDGER.csv"
CSV_1291_DELTAK = OUT / "P8_Y5_R10_1291_DELTAK_STATUS_UPDATE.csv"

SRC_1039_DOC = ROOT / "1039-Y5-R10-boundary-charge-QX-Kboundary-zero-or-beta-bound-first-row.md"
CSV_1039_BOUNDARY = OUT / "P8_Y5_R10_1039_COMPACT_PROPER_BOUNDARY_SILENCE_LEMMA.csv"

SRC_1204_DOC = ROOT / "1204-Y5-R10-boundary-projector-zero-or-finite-amplitude-bound.md"
CSV_1204_PROJECTOR = OUT / "P8_Y5_R10_1204_BOUNDARY_PROJECTOR_ZERO_ATTEMPT.csv"

SRC_1675_DOC = ROOT / "1675-Y5-R2FR-constraint-first-Z-elimination-and-coframe-source-descent.md"
CSV_1675_PROJECTOR = OUT / "P8_Y5_PARENT_QLOC_1675_BOUNDARY_PROJECTOR_DESCENT_GATE.csv"

SRC_1829_DOC = ROOT / "1829-Y5-R2FR-metric-only-connection-theorem-or-P4-hinge-source-pack.md"
CSV_1829_METRIC_ONLY = OUT / "P8_Y5_PARENT_QLOC_1829_METRIC_ONLY_CONNECTION_THEOREM_ATTEMPT.csv"
SRC_1830_DOC = ROOT / "1830-Y5-R2FR-no-independent-connection-parent-grammar-or-P4-row-fill.md"
CSV_1830_GRAMMAR = OUT / "P8_Y5_PARENT_QLOC_1830_NO_INDEPENDENT_CONNECTION_GRAMMAR_ATTEMPT.csv"
CSV_1843_DOMAIN = OUT / "P8_Y5_PARENT_QLOC_1843_BOUNDARY_DOMAIN_CERTIFICATE.csv"
CSV_1898_COMM = OUT / "P8_Y5_PARENT_QLOC_1898_READOUT_VARIATION_COMMUTATOR_ZERO_ATTEMPT.csv"
CSV_2036_DOMAIN = OUT / "P8_Y5_PARENT_QLOC_2036_MINIMAL_U_DOMAIN_CERTIFICATE.csv"
CSV_2041_CONN = OUT / "P8_Y5_PARENT_QLOC_2041_TORSION_CONNECTION_DECISION_LEDGER.csv"
CSV_2042_P4 = OUT / "P8_Y5_PARENT_QLOC_2042_P4_CONNECTION_INTERFACE.csv"
CSV_2046_CONN = OUT / "P8_Y5_PARENT_QLOC_2046_CONNECTION_DECISION_RUNNER.csv"
CSV_2074_BOUNDARY = OUT / "P8_Y5_PARENT_QLOC_2074_BOUNDARY_SILENCE_AUDIT.csv"
CSV_2084_TRACE = OUT / "P8_Y5_PARENT_QLOC_2084_PROJECTOR_TRACE_LEMMAS.csv"
CSV_2088_BOUNDARY = OUT / "P8_Y5_PARENT_QLOC_2088_SOURCE_BOUNDARY_CLAUSES.csv"
CSV_2109_DOMAIN = OUT / "P8_Y5_PARENT_QLOC_2109_DOMAIN_PROJECTOR_LIFT_TEST.csv"


def row(**kwargs: object) -> dict[str, object]:
    data = base_row()
    data["claim_allowed"] = False
    data.update(kwargs)
    return data


def truthy(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "1", "yes", "pass", "valid", "claim_allowed", "selected"}


def formalization_has_2112_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2112-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2112*",
        "*Y5_R2FR_CDB_component_zero_or_bound_Kconn_Kdomain_Kboundary_2112*",
        "*AFRAME_CDB_COMPONENT_2112*",
        "*JR2112_CONNECTION*",
    )
    try:
        return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))
    except Exception:
        return False


def source_register_rows() -> list[dict[str, object]]:
    source_specs = [
        (
            "SRC2112_00_2111_doc",
            SRC_2111_DOC,
            ["NEXT2111_0_2112", "K_conn", "K_domain", "K_boundary", "P_loc"],
            "2111 handoff identifies the CDB/projector components as the next bottleneck.",
        ),
        (
            "SRC2112_01_2111_validation",
            CSV_2111_VAL,
            ["VAL2111_OVERALL", "PASS", "local-GR/Newton remains blocked"],
            "2111 validation passed while leaving local GR/Newton blocked.",
        ),
        (
            "SRC2112_02_2111_qcdb",
            CSV_2111_QCDB,
            ["QCB2111_1_Q_cdb", "K_conn_norm", "K_domain_norm", "K_boundary_norm", "K_comm_norm"],
            "2111 supplies the Q_cdb component list.",
        ),
        (
            "SRC2112_03_1291_cdb",
            CSV_1291_CDB,
            ["KRB1291_2_cdb_bound", "MISSING_K_CONN_BOUND", "MISSING_K_DOMAIN_BOUND", "MISSING_K_BOUNDAR"],
            "1291 is the older chain-kernel residual bound for CDB terms.",
        ),
        (
            "SRC2112_04_1291_deltak",
            CSV_1291_DELTAK,
            ["DKS1291_2_DeltaK00", "MISSING_CURRENT_KHAT_MATCH", "MISSING_CDB_ZERO"],
            "1291 keeps Delta_K uncomputable without current Khat and CDB closure.",
        ),
        (
            "SRC2112_05_1039_doc",
            SRC_1039_DOC,
            ["proper compact representative-X transformations", "full_boundary_claim_not_promoted"],
            "1039 records the narrow compact/proper representative boundary zero.",
        ),
        (
            "SRC2112_06_1039_boundary",
            CSV_1039_BOUNDARY,
            ["QK1039_3_Kboundary_zero", "proper compact representative sub-branch", "QK1039_5_source_boundary_limit"],
            "1039 gives an importable boundary zero sublemma with an explicit source-boundary guard.",
        ),
        (
            "SRC2112_07_1204_projector",
            CSV_1204_PROJECTOR,
            ["ZBP1204_1_projector_exact_silence", "ZBP1204_2_projector_absorption", "ZBP1204_3_no_shortcut_guard"],
            "1204 gives sufficient projector-zero or absorption conditions, not a global pass.",
        ),
        (
            "SRC2112_08_1675_projector",
            CSV_1675_PROJECTOR,
            ["BDG1675_1_projector", "BOUNDARY_PROJECTOR_OPEN", "BOUNDARY_DESCENT_NOT_CLOSED"],
            "1675 blocks broad boundary/projector descent.",
        ),
        (
            "SRC2112_09_1829_metric_only",
            CSV_1829_METRIC_ONLY,
            ["MOC1829_1_exact_lemma", "MOC1829_6_verdict", "do not close in the current corpus"],
            "1829 contains the exact metric-only connection lemma but not the parent signature.",
        ),
        (
            "SRC2112_10_1830_no_connection",
            CSV_1830_GRAMMAR,
            ["NIC1830_6_verdict", "NO_INDEPENDENT_CONNECTION_GRAMMAR_NOT_PROVEN", "Gamma/Khat/q_loc"],
            "1830 says the no-independent-connection grammar is not parent-signed.",
        ),
        (
            "SRC2112_11_1843_domain",
            CSV_1843_DOMAIN,
            ["BDC1843_5_verdict", "boundary domain certificate", "closed/corner-free"],
            "1843 lists boundary/domain certificate clauses for an untracked edge-free domain.",
        ),
        (
            "SRC2112_12_1898_commutator",
            CSV_1898_COMM,
            ["RVC1898_1_pure_postprocessing_zero", "RVC1898_2_projection_commutator_survives", "PURE_POSTPROCESSING_ZERO_ONLY_GENERAL_COMMUTATOR_NOT_DERIVED"],
            "1898 separates harmless postprocessing from live projector/source-worldtube commutators.",
        ),
        (
            "SRC2112_13_2036_domain",
            CSV_2036_DOMAIN,
            ["UDOM2036_7_certificate_verdict", "minimal u-domain certificate is not derived"],
            "2036 keeps the minimal u-domain certificate as not derived.",
        ),
        (
            "SRC2112_14_2041_connection",
            CSV_2041_CONN,
            ["LC2041_0_metric_formalism", "LC2041_4_P4_fallback", "LC2041_5_verdict"],
            "2041 identifies metric formalism, Palatini, and P4 fallback connection routes.",
        ),
        (
            "SRC2112_15_2042_p4",
            CSV_2042_P4,
            ["P4C1960_5_hypermomentum", "MISSING_NO_GAMMA_MATTER_PROOF_OR_BOUND"],
            "2042 gives the affine/P4 residual channel list if connection zero fails.",
        ),
        (
            "SRC2112_16_2046_connection",
            CSV_2046_CONN,
            ["RUN2046_0_metric_coframe_branch", "RUN2046_2_affine_residual_branch", "CONNECTION_FORK_EXPOSED_NONCLAIM"],
            "2046 exposes the connection fork: sign LC zero or keep affine residual coefficients.",
        ),
        (
            "SRC2112_17_2074_boundary",
            CSV_2074_BOUNDARY,
            ["BSA2074_5_verdict", "BOUNDARY_SILENCE_BLOCKED", "FINITE_RESIDUAL_ROWS_REQUIRED"],
            "2074 says full boundary silence remains blocked and requires residual rows.",
        ),
        (
            "SRC2112_18_2084_trace",
            CSV_2084_TRACE,
            ["LEM2084_2_trace_owner", "LEM2084_3_round_trace_to_CQX_unit"],
            "2084 supplies conditional trace/round-domain bound factors.",
        ),
        (
            "SRC2112_19_2088_boundary",
            CSV_2088_BOUNDARY,
            ["SBC2088_2_BR_boundary", "SBC2088_4_readout_regeneration"],
            "2088 gives exact-zero clauses and finite clauses for boundary/source regeneration.",
        ),
        (
            "SRC2112_20_2109_domain",
            CSV_2109_DOMAIN,
            ["DPL2109_6_commutator", "FAIL_CURRENT_CLAIM", "DPL2109_8_verdict"],
            "2109 keeps domain/projector natural lift failed as a current claim.",
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


def zero_gate_rows() -> list[dict[str, object]]:
    rows_data = [
        (
            "CZG2112_0_total_CDB",
            "K_conn + K_domain + K_boundary + K_comm",
            "all four CDB/projector components vanish or are source-bounded in one parent branch",
            "ZERO_THEOREM_NOT_DERIVED",
            "the components have different missing parent clauses; cannot be collapsed into a single zero",
            "retain Q_cdb",
        ),
        (
            "CZG2112_1_Kconn_metric_only",
            "K_conn",
            "parent configuration is metric/coframe-only and Gamma is LC[g_obs]",
            "CONDITIONAL_EXACT_LEMMA_NOT_PARENT_SIGNED",
            "1829 proves the kinematic lemma, but 1830/2046 do not sign the field grammar",
            "either sign LC parent grammar or retain affine/P4 residual",
        ),
        (
            "CZG2112_2_Kconn_palatini",
            "K_conn",
            "Palatini EH-only connection with zero hypermomentum and projective silence",
            "NOT_ACCEPTED_CURRENT_CORPUS",
            "EH-only, no-hypermomentum, and projective silence are not all supplied",
            "retain c_T/c_Q/c_Delta rows",
        ),
        (
            "CZG2112_3_Kdomain_parent_selector",
            "K_domain",
            "domain/window/support/readout selector descends from parent Euler/topological law",
            "NOT_DERIVED",
            "2109 and 2036 leave domain selector and minimal u-domain certificates unsigned",
            "retain domain variation norm",
        ),
        (
            "CZG2112_4_Kboundary_proper_collar",
            "K_boundary",
            "proper compact representative generator and all finite jets vanish on boundary collar",
            "NARROW_SUBBRANCH_ZERO_DERIVED",
            "1039 gives K_boundary=0 only for the representative compact/proper subbranch",
            "do not apply to source worldtubes or reference/corner terms",
        ),
        (
            "CZG2112_5_Kboundary_source_worldtube",
            "K_boundary",
            "source/test worldtube boundary, reference subtraction, corner and edge classes are silent",
            "BLOCKED_CURRENT_CLAIM",
            "1675/1843/2074/2088 keep boundary class, cohomology, corners and source regeneration unsigned",
            "retain b_C/outer_flux/corner/h_edge bound rows",
        ),
        (
            "CZG2112_6_Kcomm_pure_postprocess",
            "K_comm",
            "readout is pure postprocessing and absent from parent/effective pre-variation action",
            "EXACT_CONDITIONAL_LEMMA",
            "1898 shows this safe case but it does not cover projectors depending on field/support/source",
            "usable only for pure reporting maps",
        ),
        (
            "CZG2112_7_Kcomm_projector",
            "K_comm",
            "P_loc, source-measure projection and trace/readout commute with variation/divergence",
            "COUNTERMODEL_ACTIVE",
            "1898/2109 show projector/source-worldtube commutators survive generically",
            "retain K_comm_norm",
        ),
        (
            "CZG2112_8_projector_absorption",
            "K_comm/K_domain",
            "small projector perturbation absorbs into anchored CK/Korn/trace inequality",
            "CONDITIONAL_BOUND_ROUTE_NOT_NUMERIC",
            "1204 and 2084 give the form, but constants and norms are not sourced for this branch",
            "retain epsilon_P and C_trace inputs",
        ),
        (
            "CZG2112_9_verdict",
            "CDB component zero theorem",
            "every CDB component zeroed on the same local parent branch",
            "FAIL_CURRENT_CLAIM",
            "only narrow boundary/proper and pure-postprocess sublemmas import; full CDB zero not proven",
            "move to connection parent signature first or bound each component",
        ),
    ]
    return [
        row(
            gate_id=gate_id,
            component=component,
            exact_zero_route=route,
            current_status=status,
            evidence=evidence,
            next_requirement=next_requirement,
            score_ready=False,
        )
        for gate_id, component, route, status, evidence, next_requirement in rows_data
    ]


def sublemma_rows() -> list[dict[str, object]]:
    rows_data = [
        (
            "SUB2112_0_metric_only_connection",
            "K_conn",
            "On a metric/coframe-only configuration space, Gamma=LC[g_obs] is kinematic.",
            "IMPORTABLE_AS_CONDITIONAL",
            "requires parent field inventory to exclude independent connection and hypermomentum",
        ),
        (
            "SUB2112_1_boundary_proper_collar",
            "K_boundary",
            "Proper compact representative-X generators kill finite-jet local boundary cocycles.",
            "IMPORTABLE_NARROW_ZERO",
            "does not cover source worldtubes, large transformations, reference boundaries, corners, or edge projectors",
        ),
        (
            "SUB2112_2_pure_postprocess_commutator",
            "K_comm",
            "Readout maps absent from parent/effective variation cannot generate source coefficients.",
            "IMPORTABLE_NARROW_ZERO",
            "does not cover projectors, material/source-worldtube maps, calibration feedback, or pre-variation EFT coefficients",
        ),
        (
            "SUB2112_3_projector_absorption",
            "K_comm/K_domain",
            "If ||Delta_P|| <= eps_P||V|| and C_CK eps_P < 1, projector leakage can be absorbed.",
            "IMPORTABLE_CONDITIONAL_BOUND",
            "requires same-domain constants, epsilon_P, norm convention and source paths",
        ),
        (
            "SUB2112_4_trace_bound",
            "K_boundary/K_domain",
            "Trace constants map exterior H1 control to boundary L2/charge bounds.",
            "IMPORTABLE_CONDITIONAL_BOUND",
            "requires C_tr, w_RAB, domain regularity, roundness and units",
        ),
    ]
    return [
        row(
            sublemma_id=sublemma_id,
            component=component,
            statement=statement,
            import_status=status,
            guard=guard,
        )
        for sublemma_id, component, statement, status, guard in rows_data
    ]


def finite_bound_rows() -> list[dict[str, object]]:
    rows_data = [
        (
            "CDB2112_0_total",
            "Q_cdb",
            "Q_cdb <= A_ref^-1 N_div (K_conn_norm + K_domain_norm + K_boundary_norm + K_comm_norm + Delta_K_live_norm)",
            "SYMBOLIC_COMPONENT_SUM_DERIVED",
            "A_ref;N_div;all component norms;no-cancellation guard",
            "local-GR residual carrier",
        ),
        (
            "CDB2112_1_Kconn_norm",
            "K_conn_norm",
            "K_conn_norm <= K_LC_mismatch + |c_T_or_c_Q| + |c_A_or_S| + |c_Ttrace| + |c_Qtrace| + |c_Qshear| + |c_Delta|",
            "SYMBOLIC_BOUND_FORM_DERIVED_INPUTS_MISSING",
            "LC parent signature or P4 coefficients with units/source maps",
            "connection/torsion/nonmetricity/hypermomentum leakage",
        ),
        (
            "CDB2112_2_Kdomain_norm",
            "K_domain_norm",
            "K_domain_norm <= C_chi||delta_g chi_D|| + C_sup||delta_g support|| + C_read||delta_g R_readout||",
            "SYMBOLIC_BOUND_FORM_DERIVED_INPUTS_MISSING",
            "parent domain selector; support variation; readout variation constants",
            "domain/window/source-support leakage",
        ),
        (
            "CDB2112_3_Kboundary_norm",
            "K_boundary_norm",
            "K_boundary_norm <= I_not_proper(|b_C| + |outer_flux| + |corner| + |h_edge| + |Pi_R_tot|)",
            "NARROW_ZERO_PLUS_FINITE_SOURCE_BRANCH",
            "proper-collar switch; boundary class; cohomology; corner/source flux values",
            "boundary/corner/cohomology leakage",
        ),
        (
            "CDB2112_4_Kcomm_norm",
            "K_comm_norm",
            "K_comm_norm <= ||(delta P_loc)J|| + ||[P_loc,nabla]K_res|| + ||[delta_parent,R_pre]T_H||",
            "SYMBOLIC_BOUND_FORM_DERIVED_INPUTS_MISSING",
            "projector variation; source worldtube; pre-variation readout/EFT clauses",
            "projector/readout commutator leakage",
        ),
        (
            "CDB2112_5_DeltaK_live",
            "Delta_K_live_norm",
            "Delta_K_live_norm := ||K_hat_live - K_metric0[Gamma_eff]||_D",
            "MISSING_LIVE_PARENT_TENSOR",
            "live K_hat tensor, index convention, units and local norm",
            "metric-response mismatch",
        ),
        (
            "CDB2112_6_q_loc_feed",
            "q_loc_CDB",
            "||P_loc nabla_mu Delta_K^{mu nu}|| <= N_div||Delta_K|| + K_comm_norm",
            "SYMBOLIC_FEED_READY_INPUTS_MISSING",
            "N_div;P_loc commutator;component norms",
            "PPN/local residual vector feed",
        ),
        (
            "CDB2112_7_no_cancellation",
            "policy",
            "Q_cdb pass requires every component zero/bounded independently; no cancellation between CDB pieces",
            "GUARD_READY",
            "component rows all sourced before any score",
            "prevents tuned local silence",
        ),
        (
            "CDB2112_8_verdict",
            "CDB finite score",
            "score only after component values/zero theorems, units, source paths and arena projections are filled",
            "CLAIM_BLOCKED_COMPONENT_INPUTS_MISSING",
            "CDB2112_1 through CDB2112_6",
            "no local-GR/Newton/PPN claim",
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
        ("GATE2112_0_boundary_narrow_zero", "proper compact representative K_boundary zero is importable", True, "1039 subbranch can be used only with its source-boundary guard"),
        ("GATE2112_1_pure_postprocess_zero", "pure postprocess commutator zero is importable", True, "1898 exact lemma applies only to true downstream reporting"),
        ("GATE2112_2_Kconn_zero", "K_conn zero theorem closes", False, "metric-only/Palatini/no-hypermomentum grammar is not parent-signed"),
        ("GATE2112_3_Kdomain_zero", "K_domain zero theorem closes", False, "domain selector and support/readout variation remain unsigned"),
        ("GATE2112_4_Kboundary_full_zero", "full source/test boundary zero closes", False, "source worldtube, corner, cohomology and reference terms remain live"),
        ("GATE2112_5_Kcomm_full_zero", "full projector/readout commutator zero closes", False, "projector/source-worldtube commutator countermodel remains active"),
        ("GATE2112_6_Qcdb_bound_lane", "finite Q_cdb component bound lane is source-ready", True, "component formulas and missing inputs are explicit"),
        ("GATE2112_7_local_GR_Newton", "derived local GR/Newton follows", False, "CDB zero theorem fails and component bounds are not numeric/source-backed"),
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
            "DEC2112_0_real_imports",
            "TWO_NARROW_ZERO_SUBLEMMAS_IMPORTED",
            "Proper compact representative boundary zero and pure-postprocess commutator zero are legitimate but narrow.",
            "Use them only under their guards, never for source/test worldtube or projector-dependent readout.",
        ),
        (
            "DEC2112_1_main_failure",
            "FULL_CDB_ZERO_FAILS_CURRENT_CLAIM",
            "K_conn, K_domain, full K_boundary and projector K_comm are not all zero on one parent branch.",
            "Retain Q_cdb component bound rows.",
        ),
        (
            "DEC2112_2_best_next",
            "CONNECTION_PARENT_SIGNATURE_FIRST",
            "K_conn is the highest-leverage GR bottleneck: if LC parent grammar closes, torsion/nonmetricity/hypermomentum rows collapse; if not, P4 coefficients must be filled.",
            "Attempt metric/coframe LC parent signature or retain affine/P4 residual coefficients.",
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
            route_id="NEXT2112_0_2113",
            next_target="2113-Y5-R2FR-metric-coframe-LC-parent-signature-or-affine-P4-bound.md",
            script="scripts/Y5_R2FR_metric_coframe_LC_parent_signature_or_affine_P4_bound_2113.py",
            objective=(
                "Try to sign the parent metric/coframe-only Levi-Civita branch: no independent affine Gamma, no hypermomentum, "
                "one observed geometry stack, and Gamma_eff/Khat reconciled to LC[g_obs]. If any clause fails, retain affine/P4 "
                "torsion, nonmetricity, projective and hypermomentum coefficient rows with units and source maps."
            ),
            forbidden_shortcuts=(
                "declaring Gamma LC by notation; ignoring spin/hypermomentum/projective trace; treating visible connection "
                "owner as already proven; deleting K_conn while Khat/Gamma_eff mismatch remains; local-GR/Newton/PPN claim; "
                "formalization-workbench edits; GitHub action"
            ),
        )
    ]


def write_branch_copies(
    zero_gates: list[dict[str, object]],
    sublemmas: list[dict[str, object]],
    bounds: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> list[dict[str, object]]:
    copy_specs = [
        (
            "COPY2112_0_source_weight_docs",
            SOURCE_WEIGHT_DOCS / "AFRAME_CDB_COMPONENT_2112_NONCLAIM.csv",
            zero_gates + sublemmas + bounds,
        ),
        (
            "COPY2112_1_branch_locked_wep",
            BRANCH_WEP / "P8_Y5_PARENT_QLOC_2112_CDB_COMPONENT_STATUS_NONCLAIM.csv",
            zero_gates + bounds,
        ),
        (
            "COPY2112_2_acquisition_queue",
            QUEUE / "JR2112_CONNECTION_PARENT_SIGNATURE_OR_P4_QUEUE.csv",
            next_target + bounds,
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


def all_nonclaim(groups: list[list[dict[str, object]]]) -> bool:
    for group in groups:
        for item in group:
            if truthy(item.get("claim_allowed")) or truthy(item.get("valid_for_claim")):
                return False
    return True


def validation_rows(
    sources: list[dict[str, object]],
    zero_gates: list[dict[str, object]],
    sublemmas: list[dict[str, object]],
    bounds: list[dict[str, object]],
    claim_gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_target: list[dict[str, object]],
    copies: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    source_ok = all(truthy(source.get("path_exists")) and truthy(source.get("needles_found")) for source in sources)
    zero_ok = (
        any(gate.get("gate_id") == "CZG2112_4_Kboundary_proper_collar" and gate.get("current_status") == "NARROW_SUBBRANCH_ZERO_DERIVED" for gate in zero_gates)
        and any(gate.get("gate_id") == "CZG2112_7_Kcomm_projector" and gate.get("current_status") == "COUNTERMODEL_ACTIVE" for gate in zero_gates)
        and any(gate.get("gate_id") == "CZG2112_9_verdict" and gate.get("current_status") == "FAIL_CURRENT_CLAIM" for gate in zero_gates)
    )
    sublemma_ok = (
        any(sub.get("sublemma_id") == "SUB2112_1_boundary_proper_collar" and sub.get("import_status") == "IMPORTABLE_NARROW_ZERO" for sub in sublemmas)
        and any(sub.get("sublemma_id") == "SUB2112_2_pure_postprocess_commutator" and sub.get("import_status") == "IMPORTABLE_NARROW_ZERO" for sub in sublemmas)
        and any(sub.get("sublemma_id") == "SUB2112_3_projector_absorption" and sub.get("import_status") == "IMPORTABLE_CONDITIONAL_BOUND" for sub in sublemmas)
    )
    bound_ok = (
        any(bound.get("bound_id") == "CDB2112_0_total" and bound.get("current_status") == "SYMBOLIC_COMPONENT_SUM_DERIVED" for bound in bounds)
        and any(bound.get("bound_id") == "CDB2112_1_Kconn_norm" and bound.get("current_status") == "SYMBOLIC_BOUND_FORM_DERIVED_INPUTS_MISSING" for bound in bounds)
        and any(bound.get("bound_id") == "CDB2112_7_no_cancellation" and bound.get("current_status") == "GUARD_READY" for bound in bounds)
    )
    gates_ok = (
        any(gate.get("gate_id") == "GATE2112_0_boundary_narrow_zero" and truthy(gate.get("gate_pass")) for gate in claim_gates)
        and any(gate.get("gate_id") == "GATE2112_2_Kconn_zero" and not truthy(gate.get("gate_pass")) for gate in claim_gates)
        and any(gate.get("gate_id") == "GATE2112_7_local_GR_Newton" and not truthy(gate.get("gate_pass")) for gate in claim_gates)
    )
    decision_ok = any(decision.get("decision_id") == "DEC2112_2_best_next" and decision.get("decision") == "CONNECTION_PARENT_SIGNATURE_FIRST" for decision in decisions)
    next_ok = any(target.get("route_id") == "NEXT2112_0_2113" and "metric-coframe-LC-parent-signature" in str(target.get("next_target")) for target in next_target)
    copies_ok = all(truthy(copy.get("path_exists")) and truthy(copy.get("parse_ok")) and int(copy.get("row_count", 0)) > 0 for copy in copies)
    csv_ok = all(path.exists() and csv_rows_parse(path) for path in csv_paths)
    no_claims_ok = all_nonclaim([sources, zero_gates, sublemmas, bounds, claim_gates, decisions, next_target, copies])
    formalization_ok = count_formalization_modified() == 0 and not formalization_has_2112_artifacts()
    no_pycache_ok = not (Path(__file__).resolve().parent / "__pycache__").exists()

    checks = [
        ("VAL2112_00_sources", source_ok, "all cited CDB/connection/domain/boundary/projector sources exist and contain expected needles"),
        ("VAL2112_01_zero_gates", zero_ok, "narrow zero subbranches are separated from full CDB zero failure"),
        ("VAL2112_02_sublemmas", sublemma_ok, "importable sublemmas and guards are recorded"),
        ("VAL2112_03_bounds", bound_ok, "Q_cdb component-sum bound and no-cancellation guard are present"),
        ("VAL2112_04_claim_gates", gates_ok, "partial sublemmas pass but Kconn/local-GR remain blocked"),
        ("VAL2112_05_decision", decision_ok, "decision selects connection parent signature first"),
        ("VAL2112_06_next", next_ok, "next target is 2113 metric/coframe LC signature or affine/P4 bound"),
        ("VAL2112_07_branch_copies", copies_ok, "branch copies exist and parse"),
        ("VAL2112_08_csv_parse", csv_ok, "all generated CSVs parse cleanly"),
        ("VAL2112_09_no_claim_flags", no_claims_ok, "no generated row allows a claim or score"),
        ("VAL2112_10_formalization_clean", formalization_ok, "formalization-workbench untouched by 2112"),
        ("VAL2112_11_no_pycache", no_pycache_ok, "scripts __pycache__ removed"),
    ]
    validation = [
        row(check_id=check_id, status="PASS" if passed else "FAIL", detail=detail)
        for check_id, passed, detail in checks
    ]
    overall_ok = all(item["status"] == "PASS" for item in validation)
    validation.append(
        row(
            check_id="VAL2112_OVERALL",
            status="PASS" if overall_ok else "FAIL",
            detail=(
                "2112 componentizes Q_cdb, imports only narrow zero sublemmas, blocks full local-GR promotion, "
                "and selects the connection/LC parent signature fork next."
            ),
        )
    )
    return validation


def write_doc(
    sources: list[dict[str, object]],
    zero_gates: list[dict[str, object]],
    sublemmas: list[dict[str, object]],
    bounds: list[dict[str, object]],
    claim_gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_target: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    content = "\n".join(
        [
            "# 2112 - Y5/R2FR CDB Component Zero Or Bound: Kconn, Kdomain, Kboundary",
            "",
            "## Current Verdict",
            "",
            "2112 does not close the full CDB zero theorem, but it makes the obstruction sharper. Two sublemmas are genuinely importable: the proper compact representative boundary zero from 1039, and the pure-postprocessing commutator zero from 1898. Both are narrow and guarded; neither may be used for source worldtubes, projector-dependent readout, boundary corners, cohomology, or pre-variation EFT/calibration maps.",
            "",
            "The broad `Q_cdb` route therefore remains nonclaim. `K_conn` is now the highest-leverage blocker because it decides whether the local branch is genuinely metric/coframe Levi-Civita or whether torsion, nonmetricity, projective trace, and hypermomentum must be carried as affine/P4 residual coefficients.",
            "",
            "This is useful progress: the CDB fog has become a ranked component queue rather than a single vague objection.",
            "",
            "## Source Register",
            md_table(sources, ["source_id", "source_path", "path_exists", "needles_found", "role", "valid_for_claim"]),
            "## Component Zero Gates",
            md_table(zero_gates, ["gate_id", "component", "current_status", "exact_zero_route", "evidence", "next_requirement", "valid_for_claim"]),
            "## Importable Sublemmas",
            md_table(sublemmas, ["sublemma_id", "component", "import_status", "statement", "guard", "valid_for_claim"]),
            "## Finite Bound Rows",
            md_table(bounds, ["bound_id", "quantity", "current_status", "bound_formula", "needed_inputs", "claim_effect", "valid_for_claim"]),
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
    zero_gates = zero_gate_rows()
    sublemmas = sublemma_rows()
    bounds = finite_bound_rows()
    claim_gates = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_target_rows()

    paths = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2112_SOURCE_REGISTER.csv",
        "zero": OUT / "P8_Y5_PARENT_QLOC_2112_CDB_COMPONENT_ZERO_GATES.csv",
        "sublemmas": OUT / "P8_Y5_PARENT_QLOC_2112_IMPORTABLE_SUBLEMMAS.csv",
        "bounds": OUT / "P8_Y5_PARENT_QLOC_2112_CDB_COMPONENT_BOUND_ROWS.csv",
        "gates": OUT / "P8_Y5_PARENT_QLOC_2112_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_PARENT_QLOC_2112_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2112_NEXT_TARGET.csv",
        "branch": OUT / "P8_Y5_PARENT_QLOC_2112_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2112_VALIDATION.csv",
    }

    write_csv(paths["sources"], sources)
    write_csv(paths["zero"], zero_gates)
    write_csv(paths["sublemmas"], sublemmas)
    write_csv(paths["bounds"], bounds)
    write_csv(paths["gates"], claim_gates)
    write_csv(paths["decisions"], decisions)
    write_csv(paths["next"], next_target)

    copies = write_branch_copies(zero_gates, sublemmas, bounds, next_target)
    write_csv(paths["branch"], copies)

    remove_pycache()

    csv_paths = [path for key, path in paths.items() if key != "validation"] + [Path(str(copy["destination"])) for copy in copies]
    validation = validation_rows(sources, zero_gates, sublemmas, bounds, claim_gates, decisions, next_target, copies, csv_paths)
    write_csv(paths["validation"], validation)
    write_doc(sources, zero_gates, sublemmas, bounds, claim_gates, decisions, next_target, copies, validation)

    print(f"wrote {DOC}")
    print(f"validation {paths['validation']}")


if __name__ == "__main__":
    main()
