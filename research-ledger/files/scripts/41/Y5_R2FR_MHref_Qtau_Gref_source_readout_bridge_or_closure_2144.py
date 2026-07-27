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


DOC = ROOT / "2144-Y5-R2FR-MHref-Qtau-Gref-source-readout-bridge-or-closure.md"
REPO = ROOT.parent
FORMALIZATION = REPO / "formalization-workbench"

DOC_2143 = ROOT / "2143-Y5-R2FR-local-curvature-operator-norm-and-source-bridge-bound.md"
CSV_2143_VAL = OUT / "P8_Y5_BRR545_2143_VALIDATION.csv"
CSV_2143_NEXT = OUT / "P8_Y5_PARENT_QLOC_2143_NEXT_TARGET.csv"
CSV_2143_RUNNER = OUT / "P8_Y5_PARENT_QLOC_2143_OPERATOR_BOUND_RUNNER.csv"

DOC_1339 = ROOT / "1339-Y5-R10-RAB-source-closure-to-EH-left-hand-local-GR-reduction-gate.md"
DOC_1008 = ROOT / "1008-Y5-R10-parent-theta-Qtau-extraction-or-charge-decomposition-runner.md"
DOC_1793 = ROOT / "1793-Y5-R2FR-Y5-source-charge-owner-and-Y6-extra-stress-gate-or-finite-coupling-pack.md"
DOC_1794 = ROOT / "1794-Y5-R2FR-parent-PiM-observed-time-generator-or-finite-Y5-pack.md"
DOC_1795 = ROOT / "1795-Y5-R2FR-Hamiltonian-PiM-adoption-or-Delta-Hsrc-component-pack.md"

ACTION_RESIDUAL_COEFF = "2.000000E-122"


def row(**kwargs: object) -> dict[str, object]:
    data = base_row()
    data["claim_allowed"] = False
    data.update(kwargs)
    return data


def truthy(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "1", "yes", "pass", "valid"}


def has_any(text: str, alternatives: list[str]) -> bool:
    return any(item in text for item in alternatives)


def find_line(path: Path, alternatives: list[str]) -> tuple[int, str]:
    text = read_text(path) if path.exists() else ""
    for line_number, line in enumerate(text.splitlines(), start=1):
        if has_any(line, alternatives):
            return line_number, line.strip()
    return 0, "MISSING_NEEDLE"


def formalization_has_2144_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2144-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2144*",
        "*Y5_R2FR_MHref_Qtau_Gref_source_readout_bridge_or_closure_2144*",
        "*AFRAME_MHREF_QTAU_GREF_BRIDGE_2144*",
        "*JR2144*",
    )
    try:
        return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))
    except Exception:
        return False


def source_register_rows() -> list[dict[str, object]]:
    specs = [
        (
            "SRC2144_00_2143_doc",
            DOC_2143,
            [["Current Verdict"], ["mu=G_ref M_H_ref/c^2=GM_orbital/c^2"], ["source bridge"]],
            "2143 reduces deltaK to source/readout fractions and selects the bridge as the bottleneck.",
        ),
        (
            "SRC2144_01_2143_validation",
            CSV_2143_VAL,
            [["VAL2143_OVERALL"], ["PASS"], ["source/readout fractional bounds"]],
            "2143 validation confirms the previous checkpoint.",
        ),
        (
            "SRC2144_02_2143_next",
            CSV_2143_NEXT,
            [["NEXT2143_0_2144"], ["M_H_ref"], ["Q_tau"], ["G_ref"]],
            "2143 handoff requires the M_H_ref/Q_tau/G_ref source-readout bridge.",
        ),
        (
            "SRC2144_03_2143_runner",
            CSV_2143_RUNNER,
            [["RUN2143_2_action_residual_fractional"], ["2.000000E-122"], ["SYMBOLIC_ACTION_BOUND_REDUCED"]],
            "machine-readable operator bound to be updated by 2144.",
        ),
        (
            "SRC2144_04_1339_source_GM",
            DOC_1339,
            [["EHGate1339_6_source_GM_transfer"], ["NEW1339_2_GM_calibration"], ["PPN Completion Gate"]],
            "1339 blocks source-GM transfer and measured Newtonian calibration.",
        ),
        (
            "SRC2144_05_1008_Qtau_MHref",
            DOC_1008,
            [["Q_tau^MTS"], ["CG1008_5_MHref"], ["parent theta/Q_tau"]],
            "1008 blocks parent Q_tau extraction and M_H_ref denominator promotion.",
        ),
        (
            "SRC2144_06_1793_source_owner",
            DOC_1793,
            [["mu_obs = G_eff M_H"], ["source-normalization owner theorem"], ["SOURCE_CHARGE_OWNER_THEOREM_NOT_ACTIVATED", "CG1793_0_Y5_source_charge_owner"]],
            "1793 writes the exact source owner chain and keeps it inactive.",
        ),
        (
            "SRC2144_07_1794_PiM_tau",
            DOC_1794,
            [["Pi_M^H"], ["tau_obs"], ["Delta_Hsrc"]],
            "1794 identifies Hamiltonian Pi_M and observed-time normalization as the cleanest route.",
        ),
        (
            "SRC2144_08_1795_Delta_Hsrc",
            DOC_1795,
            [["Delta_Hsrc :="], ["DHI1795_1_component_split"], ["DHC1795_7_total_abs_envelope"]],
            "1795 stages Delta_Hsrc as the central source-measure mismatch and component envelope.",
        ),
    ]
    rows: list[dict[str, object]] = []
    for source_id, path, needle_groups, role in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        groups_found = exists and all(has_any(text, alternatives) for alternatives in needle_groups)
        rows.append(
            row(
                source_id=source_id,
                source_path=str(path),
                path_exists=exists,
                needles_found=groups_found,
                expected_needles="; ".join(" OR ".join(group) for group in needle_groups),
                role=role,
            )
        )
    return rows


def source_anchor_rows() -> list[dict[str, object]]:
    anchors = [
        ("ANCH2144_0_2143_bridge", DOC_2143, ["mu=G_ref M_H_ref/c^2=GM_orbital/c^2"], "2143 bridge equation"),
        ("ANCH2144_1_2143_bound", DOC_2143, ["2.000000E-122"], "2143 K-channel bound"),
        ("ANCH2144_2_1339_GM_transfer", DOC_1339, ["EHGate1339_6_source_GM_transfer"], "source-GM blocker"),
        ("ANCH2144_3_1008_MHref", DOC_1008, ["CG1008_5_MHref"], "M_H_ref blocker"),
        ("ANCH2144_4_1793_source_chain", DOC_1793, ["mu_obs = G_eff M_H"], "source-normalization chain"),
        ("ANCH2144_5_1794_PiMH", DOC_1794, ["Pi_M^H"], "Hamiltonian Pi_M route"),
        ("ANCH2144_6_1795_Delta_Hsrc", DOC_1795, ["Delta_Hsrc :="], "central source mismatch"),
        ("ANCH2144_7_1795_component_pack", DOC_1795, ["DHC1795_7_total_abs_envelope"], "no-cancellation component envelope"),
        ("ANCH2144_8_1795_MHref_gate", DOC_1795, ["AEG1795_4_MHref"], "M_H_ref source gate"),
    ]
    rows: list[dict[str, object]] = []
    for anchor_id, path, needles, role in anchors:
        line_number, snippet = find_line(path, needles)
        rows.append(row(anchor_id=anchor_id, source_path=str(path), line_number=line_number, snippet=snippet, role=role))
    return rows


def bridge_clause_rows() -> list[dict[str, object]]:
    return [
        row(clause_id="BRIDGE2144_0_mu_target", object="measured exterior mass parameter", exact_contract="mu_obs/c^0 = G_ref*M_H_ref/c^2 = GM_orbital/c^2 in the same observed frame", current_status="TARGET_WRITTEN_NOT_SIGNED", blocker="source charge and orbital readout are not yet proved equal"),
        row(clause_id="BRIDGE2144_1_Qtau_to_MHref", object="Q_tau^MTS to source mass", exact_contract="M_H_ref = G_ref^-1 int_S Q_tau^MTS - H_ref for a fixed integrable reference and selected tau_obs", current_status="BLOCKED_BY_DELTA_HSRC", blocker="1795 keeps Delta_Hsrc nonzero/noncomputed"),
        row(clause_id="BRIDGE2144_2_PiMH_source_measure", object="Hamiltonian Pi_M^H source readout", exact_contract="G_ref^-1 int_S Q_tau^MTS-H_ref = M_eff[Pi_M^H J_H^dress]", current_status="CONDITIONAL_LEMMA_ONLY", blocker="Pi_M adoption/equivalence, source functor, commutator, boundary and extra-charge silence are unsigned"),
        row(clause_id="BRIDGE2144_3_Gref", object="G_ref normalization", exact_contract="G_ref is fixed before local/orbital residual readout and not fitted to absorb Delta_Hsrc", current_status="UNSIGNED", blocker="no parent normalization certificate tied to source charge yet"),
        row(clause_id="BRIDGE2144_4_radius_frame", object="radius/readout frame", exact_contract="r_obs, tau_obs, coframe and orbital/clock/photon readout use the same parent-selected observed representative", current_status="UNSIGNED", blocker="same-frame and pre-readout selection remain gate conditions"),
        row(clause_id="BRIDGE2144_5_no_shortcut", object="Newtonian calibration guardrail", exact_contract="Poisson/Gauss shape cannot prove measured GM; it can only be downstream after source-measure equality", current_status="POLICY_RETAINED", blocker="prevents circular proof by orbital fitting"),
        row(clause_id="BRIDGE2144_6_verdict", object="source-readout bridge", exact_contract="all clauses above close in one parent action before local GR/Newton claim", current_status="SOURCE_READOUT_BRIDGE_NOT_CLOSED", blocker="Delta_Hsrc, G_ref, tau_obs/r_obs and PPN followthrough remain open"),
    ]


def epsilon_closure_rows() -> list[dict[str, object]]:
    return [
        row(epsilon_id="EPS2144_0_epsilon_mu_definition", symbol="epsilon_mu", definition="fractional uncertainty/residual in the source mass parameter entering K=48mu^2/r^6", closure_law="epsilon_mu := |delta ln mu_obs| <= epsilon_Gref + epsilon_Hsrc_abs + epsilon_Gauss + epsilon_PPN + epsilon_readout", current_status="STRICT_ABSOLUTE_ENVELOPE_NONCLAIM"),
        row(epsilon_id="EPS2144_1_epsilon_Hsrc_abs", symbol="epsilon_Hsrc_abs", definition="Hamiltonian source-measure mismatch from 1795", closure_law="epsilon_Hsrc_abs=(|Delta_integrability|+|R_eq|+|I_commutator|+|B_ref|+|Delta_extra_charge|+|Delta_tau_MHref|+|Delta_Gauss_PPN|)/M_H_ref", current_status="IMPORT_FROM_1795_COMPONENTS_MISSING"),
        row(epsilon_id="EPS2144_2_epsilon_r", symbol="epsilon_r", definition="fractional radius/readout residual in Schwarzschild reference K", closure_law="epsilon_r <= epsilon_radius_obs + epsilon_tau_obs + epsilon_coframe + epsilon_orbit_model + epsilon_boundary_frame", current_status="SOURCE_BACKED_VALUES_MISSING"),
        row(epsilon_id="EPS2144_3_epsilon_frame", symbol="epsilon_frame", definition="projector/coframe/representative mismatch in the deltaK/K conversion", closure_law="epsilon_frame <= epsilon_same_frame + epsilon_pre_readout + epsilon_Dq_kernel + epsilon_projector_shadow", current_status="SOURCE_BACKED_VALUES_MISSING"),
        row(epsilon_id="EPS2144_4_eps_combo_substitution", symbol="eps_combo_2144", definition="2143 source/readout combo after source-bridge decomposition", closure_law="2*epsilon_mu + 6*epsilon_r + epsilon_frame <= 2*(epsilon_Gref + epsilon_Hsrc_abs + epsilon_Gauss + epsilon_PPN + epsilon_readout)+6*epsilon_r+epsilon_frame", current_status="BOUND_REWRITTEN_NOT_NUMERIC"),
        row(epsilon_id="EPS2144_5_verdict", symbol="epsilon closure", definition="the epsilons are named and decomposed but not proved small", closure_law="local K-channel remains a symbolic nonclaim bound until each component is theorem-zero or source-backed", current_status="CLOSURE_ROWS_STAGED_NONCLAIM"),
    ]


def delta_hsrc_rows() -> list[dict[str, object]]:
    return [
        row(component_id="DHSRC2144_0_definition", component="Delta_Hsrc", formula="Delta_Hsrc := G_ref^-1 int_S Q_tau^MTS - H_ref - M_eff[Pi_M^H J_H^dress]", required_input="parent Q_tau, fixed H_ref, Pi_M^H, dressed source current, units", current_status="IDENTITY_IMPORTED_NONCLAIM"),
        row(component_id="DHSRC2144_1_integrability", component="Delta_integrability", formula="failure of Q_tau to be integrable with fixed reference", required_input="Hamiltonian charge integrability/reference certificate or finite residual row", current_status="MISSING_INTEGRABILITY_REFERENCE_LOCK"),
        row(component_id="DHSRC2144_2_R_eq", component="R_eq", formula="Hilbert/source/topological equality residual", required_input="same-worldtube equality theorem or source-backed mismatch over M_H_ref", current_status="MISSING_SOURCE_EQUALITY_INPUT"),
        row(component_id="DHSRC2144_3_I_commutator", component="I_commutator", formula="M_H_ref^-1 int_A [d,Pi_M]J_H", required_input="fixed-chainmap theorem or finite annulus/profile row", current_status="MISSING_COMMUTATOR_ZERO_OR_PROFILE"),
        row(component_id="DHSRC2144_4_boundary_reference", component="B_ref", formula="boundary/reference/improvement offset in source charge", required_input="exact boundary flux theorem or finite reference convention row", current_status="MISSING_BOUNDARY_REFERENCE_INPUT"),
        row(component_id="DHSRC2144_5_extra_charge", component="Delta_extra_charge", formula="sum of independent non-EH/domain/memory/range/frame Hamiltonian mass channels", required_input="channelwise silence theorem or source-backed absolute envelope", current_status="MISSING_EXTRA_CHARGE_CHANNEL_INPUT"),
        row(component_id="DHSRC2144_6_tau_MHref_readout", component="Delta_tau_MHref", formula="tau_obs, M_H_ref denominator and same-frame readout mismatch", required_input="tau_obs lock, positive M_H_ref, observed coframe/radius/source paths", current_status="MISSING_TAU_MHREF_READOUT_INPUT"),
        row(component_id="DHSRC2144_7_Gauss_PPN", component="Delta_Gauss_PPN", formula="downstream orbital Gauss and PPN source-stability mismatch", required_input="GM_orbit, PPN vector, alpha(lambda), partial_r ln mu_obs", current_status="MISSING_GAUSS_PPN_INPUT"),
        row(component_id="DHSRC2144_8_total", component="epsilon_Hsrc_abs", formula="strict no-cancellation sum of components divided by M_H_ref", required_input="all components theorem-zero or source-backed with units", current_status="REJECT_CURRENT_DELTA_HSRC_PACK_NONCLAIM"),
    ]


def operator_bound_update_rows() -> list[dict[str, object]]:
    return [
        row(bound_id="BOUND2144_0_2143_import", object="2143 K-channel action residual", expression=f"|D_S^K deltaK| <= {ACTION_RESIDUAL_COEFF}*(2 epsilon_mu + 6 epsilon_r + epsilon_frame)", current_status="IMPORTED_FROM_2143"),
        row(bound_id="BOUND2144_1_substitute_epsilon_mu", object="source-decomposed bound", expression=f"|D_S^K deltaK| <= {ACTION_RESIDUAL_COEFF}*(2*(epsilon_Gref+epsilon_Hsrc_abs+epsilon_Gauss+epsilon_PPN+epsilon_readout)+6*epsilon_r+epsilon_frame)", current_status="SYMBOLIC_SUBSTITUTION_NONCLAIM"),
        row(bound_id="BOUND2144_2_if_zero_theorem", object="ideal theorem branch", expression="if Delta_Hsrc=0 and G_ref/tau_obs/r_obs/frame gates close, the K-channel residual becomes controlled by downstream readout/PPN residuals only", current_status="CONDITIONAL_ROUTE_ONLY"),
        row(bound_id="BOUND2144_3_if_finite_pack", object="finite residual branch", expression="if Delta_Hsrc components are source-backed, epsilon_mu can be bounded by epsilon_Gref+epsilon_Hsrc_abs+epsilon_Gauss+epsilon_PPN+epsilon_readout", current_status="FINITE_PACK_NOT_SCOREABLE"),
        row(bound_id="BOUND2144_4_verdict", object="local curvature bridge", expression="2144 closes no claim, but replaces vague epsilon_mu with Delta_Hsrc and readout component rows", current_status="BRIDGE_SHARPENED_NOT_CLOSED"),
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    return [
        row(gate_id="GATE2144_0_sources", gate="2143/1339/1008/1793/1794/1795 evidence validates", gate_pass=True, rationale="all source paths and needles are checked"),
        row(gate_id="GATE2144_1_bridge_contract_written", gate="exact source-readout bridge contract written", gate_pass=True, rationale="mu, Q_tau, M_H_ref, G_ref and frame requirements are explicit"),
        row(gate_id="GATE2144_2_epsilon_decomposition", gate="epsilon_mu/r/frame decomposition staged", gate_pass=True, rationale="2143 eps_combo is rewritten through Delta_Hsrc/readout rows"),
        row(gate_id="GATE2144_3_bridge_closed", gate="mu=G_ref*M_H_ref/c^2=GM_orbital/c^2 derived", gate_pass=False, rationale="Delta_Hsrc, G_ref and readout-frame clauses remain unsigned"),
        row(gate_id="GATE2144_4_Delta_Hsrc_zero", gate="Delta_Hsrc=0 theorem", gate_pass=False, rationale="1795 retains integrability, R_eq, commutator, boundary, extra charge and M_H_ref blockers"),
        row(gate_id="GATE2144_5_finite_score", gate="finite epsilon_mu score allowed", gate_pass=False, rationale="component rows have no source-backed values/units yet"),
        row(gate_id="GATE2144_6_local_GR_Newton_claim", gate="local GR/Newton claim allowed", gate_pass=False, rationale="source-normalized Newton remains blocked by Delta_Hsrc and PPN/source stability gates"),
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        row(decision_id="DEC2144_0", decision="BRIDGE_NOT_CLOSED", because="no parent action signs Q_tau/M_H_ref/G_ref/readout equality in one chain", next_action="do not claim local GR/Newton"),
        row(decision_id="DEC2144_1", decision="EPSILON_MU_NOW_HAS_OWNER", because="epsilon_mu is no longer a vague fudge factor; it is controlled by epsilon_Gref plus Delta_Hsrc/readout pieces", next_action="attack Delta_Hsrc components"),
        row(decision_id="DEC2144_2", decision="DELTA_HSRC_IS_PRIMARY_SOURCE_BLOCKER", because="1795 supplies the exact mismatch object and no-cancellation component envelope", next_action="try integrability/reference lock first"),
        row(decision_id="DEC2144_3", decision="NEXT_1796_STYLE_INTEGRABILITY_OR_FIRST_COMPONENT_ROW", because="the least circular path is to sign Q_tau integrability/reference before orbital calibration", next_action="2145 imports 1795/2144 and targets Delta_integrability or Pi_M^H adoption theorem"),
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        row(
            route_id="NEXT2144_0_2145",
            next_target="2145-Y5-R2FR-Delta-Hsrc-integrability-reference-lock-or-first-source-row.md",
            script="scripts/Y5_R2FR_Delta_Hsrc_integrability_reference_lock_or_first_source_row_2145.py",
            objective="Try to prove Q_tau integrability and fixed-reference silence for the Hamiltonian mass functional used in Delta_Hsrc; if it fails, emit the first strict source-backed/nonclaim Delta_integrability residual row.",
            forbidden_shortcuts="orbital GM fitting as proof; importing EH mass as MTS mass; cancellation credit among Delta_Hsrc components; local GR/Newton/PPN/R10 claim; formalization-workbench edits; GitHub action",
        )
    ]


def write_branch_copies(
    bridge: list[dict[str, object]],
    epsilons: list[dict[str, object]],
    delta_hsrc: list[dict[str, object]],
    bounds: list[dict[str, object]],
    next_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    copies = [
        ("COPY2144_0_source_weight_docs", SOURCE_WEIGHT_DOCS / "AFRAME_MHREF_QTAU_GREF_BRIDGE_2144_NONCLAIM.csv", bridge + epsilons + bounds),
        ("COPY2144_1_branch_locked_wep", BRANCH_WEP / "P8_Y5_PARENT_QLOC_2144_EPSILON_SOURCE_BRIDGE_NONCLAIM.csv", epsilons + bounds),
        ("COPY2144_2_acquisition_queue", QUEUE / "JR2144_DELTA_HSRC_COMPONENT_QUEUE.csv", delta_hsrc + next_rows),
    ]
    results: list[dict[str, object]] = []
    for copy_id, destination, rows_to_write in copies:
        write_csv(destination, rows_to_write)
        results.append(row(copy_id=copy_id, destination=str(destination), path_exists=destination.exists(), row_count=len(rows_to_write), parse_ok=csv_rows_parse(destination)))
    return results


def validation_rows(
    sources: list[dict[str, object]],
    anchors: list[dict[str, object]],
    bridge: list[dict[str, object]],
    epsilons: list[dict[str, object]],
    delta_hsrc: list[dict[str, object]],
    bounds: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    copies: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    sources_ok = all(truthy(item["path_exists"]) and truthy(item["needles_found"]) for item in sources)
    anchors_ok = all(int(item["line_number"]) > 0 for item in anchors)
    bridge_ok = any(item["clause_id"] == "BRIDGE2144_6_verdict" and item["current_status"] == "SOURCE_READOUT_BRIDGE_NOT_CLOSED" for item in bridge)
    eps_ok = (
        any(item["epsilon_id"] == "EPS2144_0_epsilon_mu_definition" for item in epsilons)
        and any(item["epsilon_id"] == "EPS2144_4_eps_combo_substitution" and item["current_status"] == "BOUND_REWRITTEN_NOT_NUMERIC" for item in epsilons)
    )
    delta_ok = (
        any(item["component_id"] == "DHSRC2144_0_definition" for item in delta_hsrc)
        and any(item["component_id"] == "DHSRC2144_8_total" and item["current_status"] == "REJECT_CURRENT_DELTA_HSRC_PACK_NONCLAIM" for item in delta_hsrc)
    )
    bound_ok = any(item["bound_id"] == "BOUND2144_1_substitute_epsilon_mu" and item["current_status"] == "SYMBOLIC_SUBSTITUTION_NONCLAIM" for item in bounds)
    gates_ok = (
        any(item["gate_id"] == "GATE2144_2_epsilon_decomposition" and truthy(item["gate_pass"]) for item in gates)
        and any(item["gate_id"] == "GATE2144_6_local_GR_Newton_claim" and not truthy(item["gate_pass"]) for item in gates)
    )
    decisions_ok = any(item["decision_id"] == "DEC2144_3" and item["decision"] == "NEXT_1796_STYLE_INTEGRABILITY_OR_FIRST_COMPONENT_ROW" for item in decisions)
    next_ok = any(item["route_id"] == "NEXT2144_0_2145" for item in next_rows)
    copies_ok = all(truthy(item["path_exists"]) and truthy(item["parse_ok"]) for item in copies)
    csv_ok = all(path.exists() and csv_rows_parse(path) for path in csv_paths)
    no_claim_flags = all(
        not truthy(item.get("claim_allowed", False)) and not truthy(item.get("valid_for_claim", False))
        for group in (sources, anchors, bridge, epsilons, delta_hsrc, bounds, gates, decisions, next_rows, copies)
        for item in group
    )
    formalization_clean = count_formalization_modified() == 0 and not formalization_has_2144_artifacts()
    pycache_clean = not (Path(__file__).resolve().parent / "__pycache__").exists()
    all_ok = all([sources_ok, anchors_ok, bridge_ok, eps_ok, delta_ok, bound_ok, gates_ok, decisions_ok, next_ok, copies_ok, csv_ok, no_claim_flags, formalization_clean, pycache_clean])
    checks = [
        ("VAL2144_00_sources", sources_ok, "2143/1339/1008/1793/1794/1795 sources validate"),
        ("VAL2144_01_anchors", anchors_ok, "line anchors for bridge, bound, Q_tau, M_H_ref and Delta_Hsrc exist"),
        ("VAL2144_02_bridge_not_closed", bridge_ok, "source-readout bridge is explicitly not closed"),
        ("VAL2144_03_epsilon_decomposition", eps_ok, "epsilon_mu/r/frame closure rows staged"),
        ("VAL2144_04_Delta_Hsrc_pack", delta_ok, "Delta_Hsrc component pack imported and rejected nonclaim"),
        ("VAL2144_05_operator_update", bound_ok, "2143 operator bound rewritten through source components"),
        ("VAL2144_06_claim_gates", gates_ok, "epsilon decomposition gate passes while local claim gate fails"),
        ("VAL2144_07_decisions", decisions_ok, "decision ledger selects integrability/reference or first component row"),
        ("VAL2144_08_next", next_ok, "next target is 2145"),
        ("VAL2144_09_branch_copies", copies_ok, "branch copies exist and parse"),
        ("VAL2144_10_csv_parse", csv_ok, "all generated CSVs parse cleanly"),
        ("VAL2144_11_no_claim_flags", no_claim_flags, "no generated row allows a claim"),
        ("VAL2144_12_formalization_clean", formalization_clean, "formalization-workbench untouched by 2144"),
        ("VAL2144_13_no_pycache", pycache_clean, "scripts __pycache__ removed"),
        ("VAL2144_OVERALL", all_ok, "2144 rewrites the measured-source bridge through Delta_Hsrc/epsilon closure rows but keeps local GR/Newton nonclaim."),
    ]
    return [row(check_id=check_id, status="PASS" if passed else "FAIL", detail=detail) for check_id, passed, detail in checks]


def write_doc(
    sources: list[dict[str, object]],
    anchors: list[dict[str, object]],
    bridge: list[dict[str, object]],
    epsilons: list[dict[str, object]],
    delta_hsrc: list[dict[str, object]],
    bounds: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    content = "\n\n".join(
        [
            "# 2144 - Y5/R2FR M_H_ref, Q_tau, G_ref Source-Readout Bridge Or Closure",
            "## Current Verdict",
            "2144 does **not** close the measured-source bridge. The equality `mu=G_ref M_H_ref/c^2=GM_orbital/c^2` is still not parent-signed, because the Hamiltonian source-measure mismatch `Delta_Hsrc` remains unresolved.",
            "But this is useful progress, not circling. The vague 2143 quantity `epsilon_mu` is now decomposed into an explicit no-cancellation source object: `epsilon_mu <= epsilon_Gref + epsilon_Hsrc_abs + epsilon_Gauss + epsilon_PPN + epsilon_readout`, with `epsilon_Hsrc_abs` inherited from the 1795 `Delta_Hsrc` component pack.",
            f"So the 2143 local K-channel bound becomes `{ACTION_RESIDUAL_COEFF}*(2*(epsilon_Gref+epsilon_Hsrc_abs+epsilon_Gauss+epsilon_PPN+epsilon_readout)+6*epsilon_r+epsilon_frame)`. That is not a claim, but it tells us exactly where the remaining local-GR/Newton source-normalization debt lives.",
            "## Source Register",
            md_table(sources, ["source_id", "source_path", "path_exists", "needles_found", "role", "valid_for_claim"]),
            "## Source Anchors",
            md_table(anchors, ["anchor_id", "source_path", "line_number", "snippet", "role", "valid_for_claim"]),
            "## Bridge Clauses",
            md_table(bridge, ["clause_id", "object", "exact_contract", "current_status", "blocker", "valid_for_claim"]),
            "## Epsilon Closure Rows",
            md_table(epsilons, ["epsilon_id", "symbol", "definition", "closure_law", "current_status", "valid_for_claim"]),
            "## Delta_Hsrc Component Rows",
            md_table(delta_hsrc, ["component_id", "component", "formula", "required_input", "current_status", "valid_for_claim"]),
            "## Operator Bound Update",
            md_table(bounds, ["bound_id", "object", "expression", "current_status", "valid_for_claim"]),
            "## Claim Gates",
            md_table(gates, ["gate_id", "gate", "gate_pass", "rationale", "claim_allowed", "valid_for_claim"]),
            "## Decision Ledger",
            md_table(decisions, ["decision_id", "decision", "because", "next_action", "valid_for_claim"]),
            "## Next Target",
            md_table(next_rows, ["route_id", "next_target", "script", "objective", "forbidden_shortcuts", "valid_for_claim"]),
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
    anchors = source_anchor_rows()
    bridge = bridge_clause_rows()
    epsilons = epsilon_closure_rows()
    delta_hsrc = delta_hsrc_rows()
    bounds = operator_bound_update_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    paths = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2144_SOURCE_REGISTER.csv",
        "anchors": OUT / "P8_Y5_PARENT_QLOC_2144_SOURCE_ANCHORS.csv",
        "bridge": OUT / "P8_Y5_PARENT_QLOC_2144_BRIDGE_CLAUSE_ROWS.csv",
        "epsilons": OUT / "P8_Y5_PARENT_QLOC_2144_EPSILON_CLOSURE_ROWS.csv",
        "delta_hsrc": OUT / "P8_Y5_PARENT_QLOC_2144_DELTA_HSRC_COMPONENT_ROWS.csv",
        "bounds": OUT / "P8_Y5_PARENT_QLOC_2144_OPERATOR_BOUND_UPDATE.csv",
        "gates": OUT / "P8_Y5_PARENT_QLOC_2144_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_PARENT_QLOC_2144_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2144_NEXT_TARGET.csv",
        "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2144_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2144_VALIDATION.csv",
    }

    write_csv(paths["sources"], sources)
    write_csv(paths["anchors"], anchors)
    write_csv(paths["bridge"], bridge)
    write_csv(paths["epsilons"], epsilons)
    write_csv(paths["delta_hsrc"], delta_hsrc)
    write_csv(paths["bounds"], bounds)
    write_csv(paths["gates"], gates)
    write_csv(paths["decisions"], decisions)
    write_csv(paths["next"], next_rows)

    copies = write_branch_copies(bridge, epsilons, delta_hsrc, bounds, next_rows)
    write_csv(paths["branch_copies"], copies)

    remove_pycache()
    csv_paths = [path for key, path in paths.items() if key != "validation"] + [Path(str(copy["destination"])) for copy in copies]
    validation = validation_rows(sources, anchors, bridge, epsilons, delta_hsrc, bounds, gates, decisions, next_rows, copies, csv_paths)
    write_csv(paths["validation"], validation)
    write_doc(sources, anchors, bridge, epsilons, delta_hsrc, bounds, gates, decisions, next_rows, copies, validation)

    print(f"wrote {DOC}")
    print(f"validation {paths['validation']}")


if __name__ == "__main__":
    main()
