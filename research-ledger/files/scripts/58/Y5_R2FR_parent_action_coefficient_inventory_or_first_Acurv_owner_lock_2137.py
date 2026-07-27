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


DOC = ROOT / "2137-Y5-R2FR-parent-action-coefficient-inventory-or-first-Acurv-owner-lock.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

CSV_2136_NEXT = OUT / "P8_Y5_PARENT_QLOC_2136_NEXT_TARGET.csv"
CSV_2136_VAL = OUT / "P8_Y5_BRR545_2136_VALIDATION.csv"
CSV_2136_FIXED = OUT / "P8_Y5_PARENT_QLOC_2136_FIXED_EH_COEFFICIENT_ATTEMPT.csv"
CSV_2136_MAP = OUT / "P8_Y5_PARENT_QLOC_2136_ACURV_PARENT_VARIABLE_MAP.csv"
CSV_2136_BETA = OUT / "P8_Y5_PARENT_QLOC_2136_BETA_OWNER_UPDATE.csv"
DOC_2136 = ROOT / "2136-Y5-R2FR-fixed-EH-coefficient-naturality-or-Acurv-parent-variable-map.md"
DOC_2135 = ROOT / "2135-Y5-R2FR-no-mixed-curvature-morphism-lemma-or-first-beta-source-owner.md"
DOC_2131 = ROOT / "2131-Y5-R2FR-cR2-coefficient-owner-or-zero-certificate.md"
DOC_1010 = ROOT / "1010-Y5-R10-Gamma-Khat-action-existence-Helmholtz-or-q_loc-residual-retention.md"
DOC_1018 = ROOT / "1018-Y5-R10-sector-Lagrangian-boundary-owner-or-FB5540-source-row.md"
DOC_1028 = ROOT / "1028-Y5-R10-frame-marker-coupling-bound-input-pack-or-no-marker-theorem.md"
DOC_01 = ROOT / "01-motion-load-route-contract.md"


def row(**kwargs: object) -> dict[str, object]:
    data = base_row()
    data["claim_allowed"] = False
    data.update(kwargs)
    return data


def truthy(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "1", "yes", "pass", "valid"}


def formalization_has_2137_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2137-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2137*",
        "*Y5_R2FR_parent_action_coefficient_inventory_or_first_Acurv_owner_lock_2137*",
        "*AFRAME_COEFF_R_INVENTORY_2137*",
        "*JR2137*",
    )
    try:
        return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))
    except Exception:
        return False


def source_register_rows() -> list[dict[str, object]]:
    specs = [
        ("SRC2137_00_2136_next", CSV_2136_NEXT, ["NEXT2136_0_2137", "parent-action coefficient"], "2136 handoff selects coefficient-of-R inventory."),
        ("SRC2137_01_2136_validation", CSV_2136_VAL, ["VAL2136_OVERALL", "PASS"], "2136 validation passed."),
        ("SRC2137_02_2136_fixed", CSV_2136_FIXED, ["FEH2136_5_verdict", "FIXED_EH_COEFFICIENT_NOT_PARENT_SIGNED"], "2136 fixed-EH theorem remains unsigned."),
        ("SRC2137_03_2136_map", CSV_2136_MAP, ["MAP2136_6_verdict", "NOT_IDENTIFIED"], "2136 did not identify actual A_curv parent variable."),
        ("SRC2137_04_2136_beta", CSV_2136_BETA, ["BETA2136_2_beta", "MISSING_BETA_A"], "2136 beta owner update keeps beta_A missing."),
        ("SRC2137_05_2136_doc", DOC_2136, ["Setting `G=1`", "A_curv_aux_2135"], "2136 prose rejects unit shortcut and quarantines A_curv name collision."),
        ("SRC2137_06_2135_doc", DOC_2135, ["A_curv_aux_2135", "NO_MIXED_CURVATURE_MORPHISM_NOT_DERIVED"], "2135 creates A_curv_aux proxy and blocks no-mixed curvature theorem."),
        ("SRC2137_07_2131_cR2", DOC_2131, ["OWN2131_0_total_definition", "c_R2_eff = c_bare"], "2131 decomposes R2/fR owner routes."),
        ("SRC2137_08_1010_Gamma", DOC_1010, ["GKT1010_0_variational_route", "Gamma_eff"], "1010 records Gamma/Khat action-density route and residual."),
        ("SRC2137_09_1018_MHref", DOC_1018, ["LOC1018_7_MHref_owner", "M_H_ref=G_ref^-1"], "1018 source denominator/G_ref bridge remains unsigned."),
        ("SRC2137_10_1028_marker", DOC_1028, ["NM1028_6_verdict", "FAIL_CURRENT_CLAIM"], "1028 no-marker/constant descent is conditional only."),
        ("SRC2137_11_motion_load", DOC_01, ["Gamma_eff", "Lambda_mem", "A_curv/(A_curv+5)"], "motion-load route contains empirical/route variables that must not be mistaken for parent coefficient owners."),
    ]
    rows: list[dict[str, object]] = []
    for source_id, path, needles, role in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            row(
                source_id=source_id,
                source_path=str(path),
                path_exists=exists,
                expected_needles="; ".join(needles),
                needles_found=exists and all(needle in text for needle in needles),
                role=role,
            )
        )
    return rows


def coefficient_inventory_rows() -> list[dict[str, object]]:
    return [
        row(
            candidate_id="COEFF2137_0_kappa0_terminal",
            symbol_or_route="kappa_0 / Coeff(R[g_obs])",
            candidate_class="terminal_constant_candidate",
            source_path=str(CSV_2136_FIXED),
            current_role="would be the true parent EH coefficient if signed",
            status="EXACT_CONDITIONAL_NOT_PARENT_SIGNED",
            blocks_or_closes="closes beta_A only if terminal coefficient, source bridge, and frame/no-marker clauses are signed",
            next_requirement="parent action basis with kappa_0 terminal plus source/readout bridge",
            priority="P0",
        ),
        row(
            candidate_id="COEFF2137_1_Gref_MHref_Qtau",
            symbol_or_route="G_ref / M_H_ref / Q_tau",
            candidate_class="source_readout_normalization_not_parent_R_coefficient",
            source_path=str(DOC_1018),
            current_role="measured Newton coefficient bridge and same-frame source denominator",
            status="UNSIGNED_SOURCE_BRIDGE",
            blocks_or_closes="blocks promotion from fixed EH notation to derived Newton/GR",
            next_requirement="Q_tau integral, tau lock, Gauss/Poisson/orbital readout and positive M_H_ref",
            priority="P0",
        ),
        row(
            candidate_id="COEFF2137_2_beta_A_Acurv_aux",
            symbol_or_route="beta_A A_curv_aux_2135 R[g_obs]",
            candidate_class="hidden_auxiliary_curvature_owner_proxy",
            source_path=str(CSV_2136_BETA),
            current_role="canonical proxy for integrated-out auxiliary curvature coupling",
            status="PROXY_RETAINED_PARENT_VARIABLE_MISSING",
            blocks_or_closes="if real and finite it generates c_R2_aux; if beta_A=0 or pure constraint it may close",
            next_requirement="actual parent variable, beta_A, M_A^2, normalization, source/readout map",
            priority="P0",
        ),
        row(
            candidate_id="COEFF2137_3_marker_prefactor",
            symbol_or_route="F(sigma_marker, chi_B, domain/source marker) R[g_obs]",
            candidate_class="marker_hidden_invariant_prefactor",
            source_path=str(DOC_2131) + "; " + str(DOC_1028),
            current_role="quotient-invariant marker/class scalar can mimic scalar-tensor/f(R) leakage",
            status="NO_MARKER_THEOREM_MISSING",
            blocks_or_closes="keeps coefficient-of-R from being terminal unless marker derivatives vanish or are forbidden",
            next_requirement="no-marker/constant descent theorem or finite marker coefficient row",
            priority="P1",
        ),
        row(
            candidate_id="COEFF2137_4_Gamma_Khat",
            symbol_or_route="Gamma_eff / K_hat / q_loc",
            candidate_class="extra_action_density_or_metric_response_residual",
            source_path=str(DOC_1010),
            current_role="not a direct Coeff(R) owner, but a local residual/stress-density route into PPN/source normalization",
            status="METRIC_RESPONSE_AND_DOUBLE_ZERO_UNSIGNED",
            blocks_or_closes="must not be counted as EH coefficient; retained until S_GK and K_metric match are parent-signed",
            next_requirement="metric-response identity, Helmholtz, Euler/double-zero and boundary/source-current closure",
            priority="P1",
        ),
        row(
            candidate_id="COEFF2137_5_measure_coframe_tau",
            symbol_or_route="mu_obs(q), e_obs, omega_obs, tau_source/tau_clock",
            candidate_class="quotient_owned_geometry_or_frame_measure",
            source_path=str(DOC_2136) + "; " + str(DOC_1018),
            current_role="measure/coframe/frame route can change observed coefficient/readout even if algebraic kappa is fixed",
            status="QUOTIENT_DESCENT_AND_TAU_LOCK_UNSIGNED",
            blocks_or_closes="blocks measured local GR unless observed frame/source/clock coframe are locked together",
            next_requirement="observed coframe descent, tau lock, matter/readout equivalence theorem",
            priority="P1",
        ),
        row(
            candidate_id="COEFF2137_6_common_frame_cg",
            symbol_or_route="c_g / common Weyl-disformal frame",
            candidate_class="frame_readout_coupling",
            source_path=str(DOC_1028),
            current_role="can move apparent curvature coupling into matter/source/readout constants",
            status="NO_SHADOW_FRAME_THEOREM_MISSING",
            blocks_or_closes="prevents Einstein-frame rewrite from being harmless",
            next_requirement="no-shadow-frame theorem or numeric/source-backed c_g and projection rows",
            priority="P1",
        ),
        row(
            candidate_id="COEFF2137_7_bare_R2_fR",
            symbol_or_route="c_R2_bare / f_RR / curvature-square tower",
            candidate_class="higher_curvature_not_linear_R_but_EH_selector_blocker",
            source_path=str(DOC_2131),
            current_role="does not own Coeff(R), but blocks pure EH second-order selector if nonzero",
            status="ZERO_CERTIFICATE_NOT_DERIVED",
            blocks_or_closes="keeps f(R)/scalaron branch retained until killed or sourced",
            next_requirement="bare-operator absence plus integrated-out/marker/nonlocal/boundary route closure",
            priority="P1",
        ),
        row(
            candidate_id="COEFF2137_8_Lambda_mem_bmem",
            symbol_or_route="Lambda_mem / b_mem / cosmology-memory amplitude",
            candidate_class="empirical_memory_or_routing_amplitude_not_parent_R_coefficient",
            source_path=str(DOC_01),
            current_role="evidence-side memory/routing amplitude with cosmology/galaxy utility",
            status="NAME_COLLISION_GUARDED_NOT_COEFF_R_OWNER",
            blocks_or_closes="must not be used as local EH coefficient or beta owner without parent action bridge",
            next_requirement="separate parent memory action owner before any local-GR coefficient claim",
            priority="P2",
        ),
        row(
            candidate_id="COEFF2137_9_Acurv_empirical",
            symbol_or_route="A_curv empirical motion-load route",
            candidate_class="empirical_motion_load_amplitude_not_parent_auxiliary",
            source_path=str(DOC_01),
            current_role="appears in motion-load simplification and empirical response formulas",
            status="NAME_COLLISION_QUARANTINED",
            blocks_or_closes="cannot be equated with A_curv_aux_2135 without beta_A A R parent action term",
            next_requirement="parent action bridge if it is ever to become the actual auxiliary owner",
            priority="P2",
        ),
    ]


def terminal_kappa_audit_rows() -> list[dict[str, object]]:
    return [
        row(audit_id="KAP2137_0_terminal_shape", clause="terminal kappa theorem shape", condition="S_grav=(1/2kappa_0) int mu_obs(q) R[g_obs(q)] with kappa_0 not a field/function", status="CONDITIONAL_PASS", missing="parent action source/signature", consequence="theorem shape is usable but not claimable"),
        row(audit_id="KAP2137_1_no_hidden_argument", clause="no hidden scalar or marker in Coeff(R)", condition="d Coeff(R)/d I_hid = d Coeff(R)/d sigma_marker = 0 by parent grammar", status="UNSIGNED", missing="hidden invariant triviality or no-marker coefficient theorem", consequence="F(I)R and F(sigma)R remain legal"),
        row(audit_id="KAP2137_2_measure_frame", clause="measure/coframe do not smuggle coefficient variation", condition="mu_obs,e_obs,tau are q-owned and common-frame c_g/disformal tails vanish or are bounded", status="UNSIGNED", missing="observed coframe/tau/no-shadow-frame theorem", consequence="Einstein-frame fixes can move the coupling elsewhere"),
        row(audit_id="KAP2137_3_source_bridge", clause="fixed EH implies measured Newton only with source bridge", condition="M_H_ref=G_ref^-1 int_S Q_tau^MTS and GM_orbit=G_ref M_H_ref are derived, not borrowed", status="UNSIGNED", missing="M_H_ref, Q_tau, Gauss/Poisson/orbital readout", consequence="Newton/local-GR remains blocked"),
        row(audit_id="KAP2137_4_higher_curvature", clause="no higher curvature or integrated-out scalar route", condition="c_R2_bare=0 and beta_A^2/(2M_A^2)=0 and marker/nonlocal/boundary routes closed", status="UNSIGNED", missing="2131/2132/2135 owner rows", consequence="EH selector cannot be promoted"),
        row(audit_id="KAP2137_5_verdict", clause="prove kappa terminal now", condition="KAP2137_0 through KAP2137_4 parent-signed together", status="KAPPA_TERMINAL_NOT_DERIVED", missing="coefficient inventory has multiple live unsigned routes", consequence="go to parent action coefficient source scan"),
    ]


def acurv_owner_lock_rows() -> list[dict[str, object]]:
    return [
        row(lock_id="LOCK2137_0_proxy", field="proxy_owner", value="A_curv_aux_2135", source_path=str(CSV_2136_MAP), lock_status="RETAIN_PROXY_ONLY", reason="selected as canonical beta_A/M_A^2 interface holder, not a parent variable"),
        row(lock_id="LOCK2137_1_actual_parent_variable", field="actual_parent_variable", value="MISSING_PARENT_ACTION_SOURCE", source_path="MISSING", lock_status="NOT_LOCKED", reason="inventory found no sourced term beta_A A_parent R[g_obs]"),
        row(lock_id="LOCK2137_2_beta", field="beta_A", value="MISSING_BETA_A", source_path=str(CSV_2136_BETA), lock_status="NOT_LOCKED", reason="no parent coefficient or theorem-zero row"),
        row(lock_id="LOCK2137_3_mass", field="M_A^2", value="MISSING_M_A2_OR_CONSTRAINT", source_path=str(CSV_2136_BETA), lock_status="NOT_LOCKED", reason="no parent Hessian, mass, or pure-constraint theorem"),
        row(lock_id="LOCK2137_4_empirical_Acurv", field="A_curv_empirical_name", value="QUARANTINED", source_path=str(DOC_01), lock_status="GUARD_ACTIVE", reason="existing A_curv is route/empirical amplitude, not the parent auxiliary owner"),
        row(lock_id="LOCK2137_5_selection_verdict", field="first_actual_owner_lock", value="NONE_SELECTED", source_path="INVENTORY_RESULT", lock_status="OWNER_LOCK_FAILED_CLEANLY", reason="need parent action coefficient source scan before selecting actual owner"),
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    return [
        row(gate_id="GATE2137_0_sources", gate="all source rows loaded", gate_pass=True, rationale="source register checks 2136 plus coefficient owner evidence"),
        row(gate_id="GATE2137_1_inventory_complete", gate="coefficient-of-R inventory covers required candidate families", gate_pass=True, rationale="kappa/G_ref/Gamma/marker/coframe/frame/R2/memory/A_curv routes are separated"),
        row(gate_id="GATE2137_2_kappa_terminal", gate="kappa_0 terminal parent theorem derived", gate_pass=False, rationale="hidden arguments, measure/frame, source bridge and higher-curvature routes are unsigned"),
        row(gate_id="GATE2137_3_actual_Acurv_owner", gate="actual A_curv_aux parent owner locked", gate_pass=False, rationale="no sourced parent variable with beta_A and M_A^2 was identified"),
        row(gate_id="GATE2137_4_name_collision_guard", gate="empirical A_curv/Lambda_mem/Gamma variables are quarantined from parent R coefficient", gate_pass=True, rationale="inventory classifies route variables separately from parent coefficient owners"),
        row(gate_id="GATE2137_5_units_shortcut_rejected", gate="unit choice can prove fixed coefficient", gate_pass=False, rationale="G=1/kappa=1 remains rejected as notation only"),
        row(gate_id="GATE2137_6_local_GR_Newton_PPN_claim", gate="local GR/Newton/PPN claim allowed", gate_pass=False, rationale="terminal kappa and beta owner routes remain blocked"),
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        row(decision_id="DEC2137_0", decision="COEFF_R_INVENTORY_WRITTEN", because="candidate routes are now separated by role and priority instead of being collapsed into one coupling problem", next_action="use inventory as the local-GR coefficient spine"),
        row(decision_id="DEC2137_1", decision="KAPPA_TERMINAL_NOT_DERIVED", because="terminal EH coefficient requires parent action basis plus source bridge/no-marker/frame/higher-curvature closures", next_action="do not claim derived GR/Newton"),
        row(decision_id="DEC2137_2", decision="NO_ACTUAL_ACURV_OWNER_LOCK", because="A_curv_aux_2135 remains a proxy and empirical A_curv is quarantined", next_action="scan parent action/core files for the first actual beta_A A R source"),
        row(decision_id="DEC2137_3", decision="BEST_NEXT_PARENT_ACTION_SOURCE_SCAN", because="the least-scrutiny route is to inspect source texts for literal coefficient owners before deriving from abstractions again", next_action="2138 parent action coefficient source scan"),
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        row(
            route_id="NEXT2137_0_2138",
            next_target="2138-Y5-R2FR-parent-action-coefficient-source-scan-or-kappa-terminal-proof.md",
            script="scripts/Y5_R2FR_parent_action_coefficient_source_scan_or_kappa_terminal_proof_2138.py",
            objective="Scan parent/action/core documents and source CSVs for literal coefficient-of-R owners and action terms involving kappa, G_ref, Gamma_eff, chi_B/markers, Lambda/memory, coframe/measure, c_g/frame, and beta_A A R; then either promote a sourced terminal-kappa proof clause or lock the first actual A_curv_aux parent owner.",
            forbidden_shortcuts="unit-choice proof; empirical A_curv equals parent auxiliary; ignoring M_H_ref/source bridge; cancellation between coefficient families; local-GR/PPN/R10 claim; formalization-workbench edits; GitHub action",
        )
    ]


def write_branch_copies(
    inventory: list[dict[str, object]],
    kappa: list[dict[str, object]],
    locks: list[dict[str, object]],
    gates: list[dict[str, object]],
    next_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    copies = [
        ("COPY2137_0_source_weight_docs", SOURCE_WEIGHT_DOCS / "AFRAME_COEFF_R_INVENTORY_2137_NONCLAIM.csv", inventory + kappa + gates),
        ("COPY2137_1_branch_locked_wep", BRANCH_WEP / "P8_Y5_PARENT_QLOC_2137_ACURV_OWNER_LOCK_NONCLAIM.csv", locks),
        ("COPY2137_2_acquisition_queue", QUEUE / "JR2137_PARENT_ACTION_COEFF_SOURCE_SCAN_QUEUE.csv", next_rows + inventory + locks),
    ]
    results: list[dict[str, object]] = []
    for copy_id, destination, rows_to_write in copies:
        write_csv(destination, rows_to_write)
        results.append(row(copy_id=copy_id, destination=str(destination), path_exists=destination.exists(), row_count=len(rows_to_write), parse_ok=csv_rows_parse(destination)))
    return results


def validation_rows(
    sources: list[dict[str, object]],
    inventory: list[dict[str, object]],
    kappa: list[dict[str, object]],
    locks: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    copies: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    sources_ok = all(truthy(item["path_exists"]) and truthy(item["needles_found"]) for item in sources)
    required_classes = {
        "terminal_constant_candidate",
        "source_readout_normalization_not_parent_R_coefficient",
        "hidden_auxiliary_curvature_owner_proxy",
        "marker_hidden_invariant_prefactor",
        "extra_action_density_or_metric_response_residual",
        "quotient_owned_geometry_or_frame_measure",
        "frame_readout_coupling",
        "higher_curvature_not_linear_R_but_EH_selector_blocker",
        "empirical_memory_or_routing_amplitude_not_parent_R_coefficient",
        "empirical_motion_load_amplitude_not_parent_auxiliary",
    }
    inventory_ok = required_classes.issubset({str(item["candidate_class"]) for item in inventory})
    kappa_ok = any(item["audit_id"] == "KAP2137_5_verdict" and item["status"] == "KAPPA_TERMINAL_NOT_DERIVED" for item in kappa)
    locks_ok = any(item["lock_id"] == "LOCK2137_5_selection_verdict" and item["lock_status"] == "OWNER_LOCK_FAILED_CLEANLY" for item in locks) and any(item["lock_id"] == "LOCK2137_4_empirical_Acurv" and item["lock_status"] == "GUARD_ACTIVE" for item in locks)
    gates_ok = any(item["gate_id"] == "GATE2137_1_inventory_complete" and truthy(item["gate_pass"]) for item in gates) and any(item["gate_id"] == "GATE2137_6_local_GR_Newton_PPN_claim" and not truthy(item["gate_pass"]) for item in gates)
    decisions_ok = any(item["decision_id"] == "DEC2137_3" and "PARENT_ACTION_SOURCE_SCAN" in str(item["decision"]) for item in decisions)
    next_ok = any(item["route_id"] == "NEXT2137_0_2138" for item in next_rows)
    branch_ok = all(truthy(item["path_exists"]) and truthy(item["parse_ok"]) for item in copies)
    csv_ok = all(path.exists() and csv_rows_parse(path) for path in csv_paths)
    no_claim_flags = all(
        not truthy(item.get("claim_allowed", False)) and not truthy(item.get("valid_for_claim", False))
        for group in (sources, inventory, kappa, locks, gates, decisions, next_rows, copies)
        for item in group
    )
    formalization_clean = count_formalization_modified() == 0 and not formalization_has_2137_artifacts()
    pycache_clean = not (Path(__file__).resolve().parent / "__pycache__").exists()
    all_ok = all([sources_ok, inventory_ok, kappa_ok, locks_ok, gates_ok, decisions_ok, next_ok, branch_ok, csv_ok, no_claim_flags, formalization_clean, pycache_clean])
    checks = [
        ("VAL2137_00_sources", sources_ok, "all cited 2136/2135/2131/1010/1018/1028/motion-load sources exist and contain expected needles"),
        ("VAL2137_01_inventory", inventory_ok, "inventory covers kappa/G_ref/Gamma/marker/coframe/frame/R2/memory/A_curv candidate classes"),
        ("VAL2137_02_kappa", kappa_ok, "terminal kappa proof is explicitly not derived"),
        ("VAL2137_03_Acurv_lock", locks_ok, "actual A_curv owner lock fails cleanly while empirical A_curv guard remains active"),
        ("VAL2137_04_gates", gates_ok, "inventory gate passes while local-GR claim gate fails"),
        ("VAL2137_05_decisions", decisions_ok, "decision ledger selects parent action source scan next"),
        ("VAL2137_06_next", next_ok, "next target is 2138"),
        ("VAL2137_07_branch_copies", branch_ok, "branch copies exist and parse"),
        ("VAL2137_08_csv_parse", csv_ok, "all generated CSVs parse cleanly"),
        ("VAL2137_09_no_claim_flags", no_claim_flags, "no generated row allows a claim"),
        ("VAL2137_10_formalization_clean", formalization_clean, "formalization-workbench untouched by 2137"),
        ("VAL2137_11_no_pycache", pycache_clean, "scripts __pycache__ removed"),
        ("VAL2137_OVERALL", all_ok, "2137 writes the coefficient-of-R inventory, keeps kappa terminal and A_curv owner unclaimed, and selects a parent action source scan next."),
    ]
    return [row(check_id=check_id, status="PASS" if passed else "FAIL", detail=detail) for check_id, passed, detail in checks]


def write_doc(
    sources: list[dict[str, object]],
    inventory: list[dict[str, object]],
    kappa: list[dict[str, object]],
    locks: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    content = "\n\n".join(
        [
            "# 2137 - Y5/R2FR Parent Action Coefficient Inventory Or First Acurv Owner Lock",
            "## Current Verdict",
            "2137 turns the coupling hunt into an inventory instead of another foggy theorem attempt. The coefficient-of-`R` problem now has named candidate families: terminal `kappa_0`, measured `G_ref/M_H_ref`, hidden auxiliary `beta_A A R`, marker prefactors, `Gamma_eff/K_hat`, coframe/measure/tau, common frame `c_g`, higher-curvature `c_R2`, memory amplitudes, and empirical `A_curv`.",
            "The inventory does not derive local GR yet. `kappa_0` is still only an exact conditional theorem, not a parent-signed terminal datum. `A_curv_aux_2135` remains a proxy, not an actual parent field. Empirical `A_curv`, `Lambda_mem`, and `Gamma_eff` are explicitly quarantined from being treated as coefficient owners without a parent action bridge.",
            "The next least-scrutiny move is a source scan: inspect parent/action/core texts and CSVs for literal coefficient-of-`R` owners before trying another abstraction leap.",
            "## Source Register",
            md_table(sources, ["source_id", "source_path", "path_exists", "needles_found", "role", "valid_for_claim"]),
            "## Coefficient-of-R Inventory",
            md_table(inventory, ["candidate_id", "symbol_or_route", "candidate_class", "source_path", "current_role", "status", "blocks_or_closes", "next_requirement", "priority", "valid_for_claim"]),
            "## Terminal Kappa Audit",
            md_table(kappa, ["audit_id", "clause", "condition", "status", "missing", "consequence", "valid_for_claim"]),
            "## Acurv Owner Lock",
            md_table(locks, ["lock_id", "field", "value", "source_path", "lock_status", "reason", "valid_for_claim"]),
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
    inventory = coefficient_inventory_rows()
    kappa = terminal_kappa_audit_rows()
    locks = acurv_owner_lock_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    paths = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2137_SOURCE_REGISTER.csv",
        "inventory": OUT / "P8_Y5_PARENT_QLOC_2137_COEFF_R_INVENTORY.csv",
        "kappa": OUT / "P8_Y5_PARENT_QLOC_2137_TERMINAL_KAPPA_AUDIT.csv",
        "locks": OUT / "P8_Y5_PARENT_QLOC_2137_ACURV_OWNER_LOCK.csv",
        "gates": OUT / "P8_Y5_PARENT_QLOC_2137_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_PARENT_QLOC_2137_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2137_NEXT_TARGET.csv",
        "branch": OUT / "P8_Y5_PARENT_QLOC_2137_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2137_VALIDATION.csv",
    }
    write_csv(paths["sources"], sources)
    write_csv(paths["inventory"], inventory)
    write_csv(paths["kappa"], kappa)
    write_csv(paths["locks"], locks)
    write_csv(paths["gates"], gates)
    write_csv(paths["decisions"], decisions)
    write_csv(paths["next"], next_rows)

    copies = write_branch_copies(inventory, kappa, locks, gates, next_rows)
    write_csv(paths["branch"], copies)

    remove_pycache()
    csv_paths = [path for key, path in paths.items() if key != "validation"] + [Path(str(copy["destination"])) for copy in copies]
    validation = validation_rows(sources, inventory, kappa, locks, gates, decisions, next_rows, copies, csv_paths)
    write_csv(paths["validation"], validation)
    write_doc(sources, inventory, kappa, locks, gates, decisions, next_rows, copies, validation)

    print(f"wrote {DOC}")
    print(f"validation {paths['validation']}")


if __name__ == "__main__":
    main()
