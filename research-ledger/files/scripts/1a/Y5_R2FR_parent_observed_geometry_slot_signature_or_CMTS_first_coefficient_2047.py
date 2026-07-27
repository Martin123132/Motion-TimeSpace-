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


DOC = ROOT / "2047-Y5-R2FR-parent-observed-geometry-slot-signature-or-CMTS-first-coefficient.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()
HBARC_GEV_M = "1.973269804e-16"


def formalization_has_2047_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    try:
        patterns = (
            "*2047-Y5-R2FR*",
            "*P8_Y5_PARENT_QLOC_2047*",
            "*Y5_R2FR_parent_observed_geometry_slot_signature_or_CMTS_first_coefficient_2047*",
        )
        return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))
    except Exception:
        return False


def scripts_pycache_exists() -> bool:
    return (SCRIPT_PATH.parent / "__pycache__").exists()


def source_register_rows() -> list[dict[str, object]]:
    specs = [
        (
            "SRC2047_00_2046_doc",
            ROOT / "2046-Y5-R2FR-GammaMTS-affine-torsion-definition-or-LC-zero-theorem.md",
            ["NEXT2046_0_2047", "LCZ2046_7_verdict", "AFF2046_7_verdict", "VAL2046_OVERALL"],
            "2046 exposed the GammaMTS fork and selected this parent observed-geometry slot test.",
        ),
        (
            "SRC2047_01_2046_next",
            OUT / "P8_Y5_PARENT_QLOC_2046_NEXT_TARGET.csv",
            ["NEXT2046_0_2047", "parent action argument list"],
            "machine-readable 2047 target.",
        ),
        (
            "SRC2047_02_1045_matter_functor",
            ROOT / "1045-Y5-R10-parent-matter-functor-descent-signature-or-qbar-component-fill.md",
            ["MFS1045_1_observed_coframe_functor", "QG1045_2_connection_stack", "MFS1045_6_verdict"],
            "observed coframe functor and connection caveat source.",
        ),
        (
            "SRC2047_03_1737_qmap_coframe",
            ROOT / "1737-Y5-R2FR-q-map-Dq-vertical-basis-source-row-or-coframe-functor-zero.md",
            ["QMAP1737_1_e_obs", "CFZ1737_0_exact_conditional", "DQM1737_0_DObs_e"],
            "q-map/coframe chain-rule source.",
        ),
        (
            "SRC2047_04_1030_spm_contract",
            ROOT / "1030-Y5-R10-single-public-metric-parent-action-derivation-or-cg-provenance-gate.md",
            ["SPD1030_6_verdict", "SPM1030_6_contract_verdict", "CPG1030_0_zero_branch"],
            "single-public-metric contract and c_g provenance gate source.",
        ),
        (
            "SRC2047_05_1031_terminal_route",
            ROOT / "1031-Y5-R10-quotient-naturality-terminal-public-metric-proof-or-spm-closure.md",
            ["TPM1031_6_verdict", "SPMC1031_0_closure_name", "FCG1031_0_cg_value"],
            "terminal-public-metric route demoted to explicit closure source.",
        ),
        (
            "SRC2047_06_same_coframe_clause",
            OUT / "P8_Y5_SAME_COFRAME_PARENT_CLAUSE.csv",
            ["UOC519_0_single_coframe_field", "UOC519_5_no_conformal_disformal_shadow_frame"],
            "same-coframe/no-shadow-frame clause source.",
        ),
        (
            "SRC2047_07_constant_owner",
            OUT / "P8_Y5_R10_1098_ORDINARY_CONSTANT_OWNER_SIGNATURE_ATTEMPT.csv",
            ["OCS1098_4_source_weight_exclusion", "OCS1098_6_verdict"],
            "ordinary constant/source-weight owner obstruction source.",
        ),
        (
            "SRC2047_08_2043_gamma_slot",
            ROOT / "2043-Y5-R2FR-parent-Gamma-slot-owner-or-first-P4-connection-bound-row.md",
            ["GSO2043_0_target", "ARG2043_3_affine_Gamma", "SPG2043_0_spin_guard"],
            "Gamma-slot owner and spin guard source.",
        ),
        (
            "SRC2047_09_2044_torsion_anchor",
            OUT / "P8_Y5_PARENT_QLOC_2044_NUMERIC_P4_SOURCE_ANCHORS.csv",
            ["P4SRC2044_0_KRT2008_axial_torsion_anchor", "1e-31"],
            "KRT axial torsion anchor retained for future C_MTS scoring only.",
        ),
    ]
    rows = []
    for source_id, path, needles, note in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        ok = exists and all(needle in text for needle in needles)
        row = base_row()
        row.update(
            {
                "source_id": source_id,
                "source_kind": "local",
                "source_path": str(path),
                "status": "EXISTS_NEEDLES_CONFIRMED" if ok else "MISSING_OR_NEEDLE_FAIL",
                "needles": ";".join(needles),
                "note": note,
            }
        )
        rows.append(row)
    return rows


def observed_geometry_signature_rows() -> list[dict[str, object]]:
    data = [
        (
            "OGS2047_0_parent_action_domain",
            "parent local ordinary action argument list",
            "S_ord^local = S_matter[Psi_A,e_obs(q),omega_LC[e_obs],A_Q,theta_rep] + S_source/readout[e_obs,theta_rep] with no independent affine Gamma_MTS argument.",
            "TARGET_EXACT",
            "would make delta S_ord/delta Gamma_MTS = 0 by absence of the slot",
            "contract exists across prior files but is not parent-signed in one action object",
        ),
        (
            "OGS2047_1_observed_coframe_owner",
            "observed coframe/metric is quotient-owned",
            "e_obs = E(q(Phi)) and g_obs = eta_ab e_obs^a e_obs^b; candidate vertical directions satisfy Dq[v]=0 before ordinary readout.",
            "CONDITIONAL_CHAIN_RULE_AVAILABLE",
            "DObs_e[v]=0 follows by chain rule",
            "q, Dq kernel, E(q), and vertical basis are not jointly parent-signed",
        ),
        (
            "OGS2047_2_no_affine_Gamma_slot",
            "independent affine connection excluded from ordinary slots",
            "Gamma_MTS is either defined as LC[g_obs] or absent from args(S_matter,S_source,S_clock,S_light,S_orbit).",
            "UNSIGNED_CORE_CLAUSE",
            "activates the 2046 LC-zero theorem",
            "spin, source, clock, light and orbit slots have not all signed no-Gamma language",
        ),
        (
            "OGS2047_3_spin_connection",
            "spin connection is coframe-owned",
            "omega_spin = omega_LC[e_obs]; no independent contorsion K_abc or axial torsion source is allowed unless retained as C_MTS.",
            "UNSIGNED_SPIN_GUARD",
            "kills axial torsion coupling without fitting c_A small",
            "fermion/spin transport guard is still contractual rather than derived",
        ),
        (
            "OGS2047_4_source_clock_light_orbit",
            "source and readout use the same observed geometry",
            "worldtubes, clocks, rods, lightcones and slow orbits are functors of g_obs and LC[g_obs], not post-readout affine/source frames.",
            "UNSIGNED_READOUT_GUARD",
            "prevents Gamma_MTS from re-entering through measurement rather than matter action",
            "source support, tau lock, clock calibration, orbital GM and boundary readout remain open",
        ),
        (
            "OGS2047_5_no_shadow_constants",
            "no shadow frame or hidden constant vertices",
            "Forbid A_g(X)e_obs, B_g(X) disformal slots, m_A(X), alpha_EM(X), source-only weights, or marker labels unless retained as residuals.",
            "UNSIGNED_RENAME_GUARD",
            "stops LC-zero from being undone by field-renaming the same coupling elsewhere",
            "1030/1031/1098 keep these countermodels legal in current corpus",
        ),
        (
            "OGS2047_6_boundary_nonhilbert",
            "boundary and non-Hilbert currents do not carry affine charge",
            "Boundary/support/projector terms are q-basic, fixed before readout, or explicitly residualized; no hidden connection current contributes to local source balance.",
            "UNSIGNED_BOUNDARY_GUARD",
            "keeps local Newton/PPN source normalization from reopening connection leakage",
            "boundary/projector/source-measure rows remain unresolved",
        ),
        (
            "OGS2047_7_verdict",
            "parent observed-geometry slot signature",
            "OGS2047_0 through OGS2047_6 would sign the 2046 LC-zero branch, but current evidence still leaves several clauses unsigned.",
            "FAIL_CURRENT_CORPUS_PARENT_SIGNATURE_NOT_DERIVED",
            "LC-zero remains the preferred route, but not yet a claim",
            "missing one parent action signature joining geometry, matter, spin, source/readout, constants and boundary guards",
        ),
    ]
    rows = []
    for row_id, clause, mathematical_form, status, if_signed, blocker in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "clause": clause,
                "mathematical_form": mathematical_form,
                "status": status,
                "if_signed": if_signed,
                "blocker": blocker,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def lc_derivation_attempt_rows() -> list[dict[str, object]]:
    data = [
        (
            "LCD2047_0_variational_absence",
            "hypermomentum zero from no slot",
            "If Gamma_MTS is not an independent argument of S_ord, Delta_lambda^{mu nu} := -2/sqrt(-g) delta S_ord/delta Gamma_MTS^lambda_{mu nu} = 0.",
            "EXACT_CONDITIONAL",
            "OGS2047_0 plus OGS2047_2",
            "not applicable until parent action domain is signed",
        ),
        (
            "LCD2047_1_metric_definition",
            "Gamma_MTS defined rather than varied",
            "Define Gamma_MTS^lambda_{mu nu}:={lambda}_{mu nu}[g_obs] inside the ordinary local branch; then there is no independent connection equation to solve.",
            "EXACT_IF_PARENT_SELECTED",
            "OGS2047_1 plus OGS2047_2",
            "currently a branch selection, not a derivation from primitive MTS variables",
        ),
        (
            "LCD2047_2_torsion_nonmetricity_zero",
            "connection residuals vanish",
            "C_MTS=0, T_MTS=2 Gamma_MTS^[lower antisym]=0, and Q_MTS=-nabla^Gamma g_obs=0 for Gamma_MTS=LC[g_obs].",
            "EXACT_CONDITIONAL_ZERO",
            "LCD2047_1",
            "cannot be promoted while OGS2047_7 fails",
        ),
        (
            "LCD2047_3_axial_bound_effect",
            "KRT torsion branch becomes irrelevant under LC-zero",
            "A_MTS^mu=(1/6)epsilon T_MTS=0, so the axial torsion P4 row is closed by theorem rather than by comparing to 1e-31 GeV.",
            "EXACT_CONDITIONAL_ZERO",
            "LCD2047_2 plus spin guard",
            "spin guard and parent LC selection remain unsigned",
        ),
        (
            "LCD2047_4_left_hand_effect",
            "Levi-Civita premise for EH/Newton route",
            "A signed LC-zero branch would close the connection premise in the Lovelock/EH local operator route, but not the metric-only, second-order, source-GM, boundary and PPN gates.",
            "CONDITIONAL_GATE_IMPROVEMENT",
            "removes one major left-hand blocker",
            "not a full local-GR/Newton proof by itself",
        ),
        (
            "LCD2047_5_verdict",
            "LC-zero proof attempt",
            "The proof is algebraically clean; the failure is not math but missing parent action authority for the ordinary observed-geometry slots.",
            "MATH_CLEAN_PARENT_SIGNATURE_MISSING",
            "gives the precise derivation we need to source next",
            "do not claim Gamma_MTS=LC[g_obs] yet",
        ),
    ]
    rows = []
    for row_id, step, statement, status, required_clause, blocker in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "step": step,
                "statement": statement,
                "status": status,
                "required_clause": required_clause,
                "blocker": blocker,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def cmts_first_coefficient_rows() -> list[dict[str, object]]:
    data = [
        (
            "CMTS2047_0_C_tensor",
            "C_MTS^lambda_{mu nu}",
            "C_MTS^lambda_{mu nu} := Gamma_MTS^lambda_{mu nu} - {lambda}_{mu nu}[g_obs]",
            "L^-1; m^-1 if coordinates are meters",
            "MISSING_PARENT_C_MTS_FIELD_OR_LC_ZERO_SELECTION",
            "connection;PPN;clock;light;spin;source",
            "AFF2046_0_residual_definition",
            "false",
        ),
        (
            "CMTS2047_1_axial_component_m_inv",
            "A_MTS^mu_component",
            "A_MTS^mu = (1/3) epsilon^{alpha beta gamma mu} C_MTS,alpha[beta gamma] in the declared orientation and component frame",
            "m^-1",
            "MISSING_C_MTS_COMPONENTS_OR_ZERO_THEOREM",
            "spin_transport;torsion_bound;clock",
            "AFF2046_3_axial_projection",
            "false",
        ),
        (
            "CMTS2047_2_axial_component_GeV",
            "A_MTS_component_GeV",
            f"A_MTS_component_GeV = {HBARC_GEV_M} * A_MTS_component_m^-1 before xi_A and KRT basis factors",
            "GeV",
            "MISSING_A_MTS_VALUE_XI_A_C_BASIS_AND_FRAME",
            "KRT2008_torsion_anchor;spin_transport",
            "P4SRC2044_0_KRT2008_axial_torsion_anchor",
            "false",
        ),
        (
            "CMTS2047_3_spin_coupling",
            "b_eff^mu",
            "b_eff^mu = xi_A C_basis A_MTS^mu + retained vector/tensor torsion mixing, with no cancellation against unmapped pieces",
            "GeV or declared KRT convention units",
            "MISSING_XI_A_C_BASIS_MIXING_MATRIX",
            "spin_transport;clock;matter_coupling",
            "MAP2045_3_coupling_kernel",
            "false",
        ),
        (
            "CMTS2047_4_frame_component",
            "R_lab<-MTS A_MTS",
            "component row must name lab/Sun-centered frame convention, time dependence, and the bounded KRT component label",
            "frame map plus component label",
            "MISSING_FRAME_ROTATION_AND_COMPONENT_LABEL",
            "torsion_bound;PPN_preferred_frame;clock",
            "MAP2045_5_lab_frame",
            "false",
        ),
        (
            "CMTS2047_5_bound_rule",
            "absolute no-cancellation score",
            "score only abs(b_eff_component) <= bound_component with every retained C_MTS projection either zero-theorem or separately bounded",
            "policy",
            "MISSING_NUMERIC_COMPONENTS_AND_SOURCE_BACKED_BOUND_TABLE",
            "R11_connection;local_GR",
            "AFF2046_6_no_cancellation_envelope",
            "false",
        ),
        (
            "CMTS2047_VERDICT",
            "first C_MTS coefficient row",
            "The fallback branch now has an executable-shaped first coefficient chain, but every numeric/coupling/frame field remains nonclaim until sourced.",
            "nonclaim coefficient chain",
            "FIRST_CMTS_COEFFICIENT_ROW_STAGED_NOT_SCOREABLE",
            "connection;spin;PPN;clock;source",
            "RUN2046_2_affine_residual_branch",
            "false",
        ),
    ]
    rows = []
    for row_id, symbol, formula, units, current_status, observable_links, source_anchor, ready in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "symbol": symbol,
                "formula": formula,
                "units": units,
                "current_status": current_status,
                "observable_links": observable_links,
                "source_anchor": source_anchor,
                "ready_for_scoring": ready == "true",
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def runner_rows() -> list[dict[str, object]]:
    data = [
        (
            "RUN2047_0_LC_zero_branch",
            "OGS2047_7_verdict",
            "attempt to claim Gamma_MTS=LC[g_obs]",
            "REJECTED_PARENT_SIGNATURE_MISSING",
            "missing observed-geometry parent action signature across spin/source/readout/constants/boundary",
            "false",
        ),
        (
            "RUN2047_1_CMTS_fallback",
            "CMTS2047_VERDICT",
            "attempt to score C_MTS axial component against KRT anchor",
            "REJECTED_NUMERIC_COUPLING_FRAME_MISSING",
            "missing C_MTS components, xi_A, C_basis, frame map, component label and full bound table",
            "false",
        ),
        (
            "RUN2047_2_EH_route",
            "LCD2047_4_left_hand_effect",
            "attempt to promote local EH/Newton connection premise",
            "REJECTED_LC_NOT_PARENT_DERIVED",
            "Levi-Civita premise remains conditional; other EH/Newton gates remain open",
            "false",
        ),
        (
            "RUN2047_VERDICT",
            "all_2047_branches",
            "LC-zero route preferred but unsigned; C_MTS fallback staged but unscoreable",
            "PARENT_SIGNATURE_OR_SOURCED_CMTS_REQUIRED",
            "next work must construct the observed coframe from primitive motion/load variables or source C_MTS coefficients",
            "false",
        ),
    ]
    rows = []
    for run_id, input_id, attempted, verdict, reason, score_attempted in data:
        row = base_row()
        row.update(
            {
                "run_id": run_id,
                "input_id": input_id,
                "attempted": attempted,
                "verdict": verdict,
                "reason": reason,
                "score_attempted": score_attempted == "true",
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def claim_gate_rows() -> list[dict[str, object]]:
    data = [
        ("GATE2047_0_parent_geometry_signature", "parent observed-geometry slot signed", "FAIL_BLOCKED", "signature clauses are exact but not parent-derived"),
        ("GATE2047_1_Gamma_LC", "Gamma_MTS=LC[g_obs]", "FAIL_BLOCKED", "would follow from metric/coframe-only ordinary slots, but OGS2047_7 fails"),
        ("GATE2047_2_torsion_zero", "T_MTS=Q_MTS=A_MTS=0", "FAIL_BLOCKED", "exact under LC-zero only; not promoted"),
        ("GATE2047_3_CMTS_score", "C_MTS first coefficient scoreable", "FAIL_BLOCKED", "coefficient row lacks numeric components and coupling/frame/source map"),
        ("GATE2047_4_EH_Newton", "EH/Newton connection premise closed", "FAIL_BLOCKED", "LC premise is conditional and other left-hand/source gates remain open"),
        ("GATE2047_5_public_claim", "public local-GR/torsion/PPN claim", "FAIL_BLOCKED", "private nonclaim checkpoint only"),
    ]
    rows = []
    for row_id, gate, status, detail in data:
        row = base_row()
        row.update({"row_id": row_id, "gate": gate, "status": status, "detail": detail, "claim_allowed": False})
        rows.append(row)
    return rows


def decision_rows() -> list[dict[str, object]]:
    data = [
        (
            "DEC2047_0_clean_route_status",
            "LC-zero remains the best route, but it is not signed.",
            "It gives real zeros rather than small fitted couplings, but needs one parent action signature that current evidence does not yet provide.",
        ),
        (
            "DEC2047_1_not_a_dead_end",
            "Failure to sign the slot is informative, not fatal.",
            "The exact missing clauses are now listed, and the fallback C_MTS coefficient chain has units and observable links.",
        ),
        (
            "DEC2047_2_no_smuggling",
            "Do not call Single Public Metric a derivation unless the matter-interface restriction is parent-owned.",
            "1031 already showed terminality/closure language is insufficient unless the action domain forbids non-terminal frames and labels.",
        ),
        (
            "DEC2047_3_next_leap",
            "The next best leap is primitive construction, not another abstract closure audit.",
            "Use the motion/load coframe route to try constructing e_obs and omega_LC directly from MTS primitive variables; if that fails, continue C_MTS provenance.",
        ),
    ]
    rows = []
    for row_id, decision, rationale in data:
        row = base_row()
        row.update({"row_id": row_id, "decision": decision, "rationale": rationale, "claim_allowed": False})
        rows.append(row)
    return rows


def next_target_rows() -> list[dict[str, object]]:
    row = base_row()
    row.update(
        {
            "target_id": "NEXT2047_0_2048",
            "target_doc": "2048-Y5-R2FR-motion-load-coframe-construction-or-CMTS-provenance.md",
            "objective": "try to construct e_obs and omega_LC[e_obs] directly from the motion/load/clock-routing primitive route so the observed-geometry slot is derived rather than closed by declaration; if this fails, continue C_MTS coefficient provenance",
            "must_include": "motion-load coframe variables; clock-routing metric construction; LC spin connection from coframe; source/readout same-frame test; comparison to OGS2047 clauses; C_MTS fallback if any primitive connection remains",
            "excluded": "declaring Single Public Metric as proof; claiming local GR from closure; inventing C_MTS values; GitHub; formalization-workbench edits",
            "claim_allowed": False,
        }
    )
    return [row]


def write_branch_copies(
    signature_rows: list[dict[str, object]],
    cmts_rows: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
) -> list[dict[str, object]]:
    copies = [
        (
            "COPY2047_0_source_weight_geometry_signature",
            SOURCE_WEIGHT_DOCS / "AFRAME_PARENT_OBSERVED_GEOMETRY_SIGNATURE_2047_NONCLAIM.csv",
            signature_rows,
        ),
        (
            "COPY2047_1_wep_cmts_first_coefficient",
            BRANCH_WEP / "P8_Y5_PARENT_QLOC_2047_CMTS_FIRST_COEFFICIENT_NONCLAIM.csv",
            cmts_rows,
        ),
        (
            "COPY2047_2_rab_next",
            QUEUE / "JR2047_MOTION_LOAD_COFRAME_CONSTRUCTION_NEXT_NONCLAIM.csv",
            next_rows_,
        ),
    ]
    rows = []
    for copy_id, path, data in copies:
        write_csv(path, data)
        row = base_row()
        row.update({"copy_id": copy_id, "path": str(path), "rows": len(data), "status": "WRITTEN_NONCLAIM_COPY"})
        rows.append(row)
    return rows


def validation_rows(
    sources: list[dict[str, object]],
    signature_rows: list[dict[str, object]],
    lc_rows: list[dict[str, object]],
    cmts_rows: list[dict[str, object]],
    runner: list[dict[str, object]],
    gates: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    source_ok = all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in sources)
    signature_verdict = next(row for row in signature_rows if row["row_id"] == "OGS2047_7_verdict")
    lc_verdict = next(row for row in lc_rows if row["row_id"] == "LCD2047_5_verdict")
    cmts_verdict = next(row for row in cmts_rows if row["row_id"] == "CMTS2047_VERDICT")
    runner_verdict = next(row for row in runner if row["run_id"] == "RUN2047_VERDICT")
    claim_gate = next(row for row in gates if row["row_id"] == "GATE2047_0_parent_geometry_signature")
    checks: list[tuple[str, bool, str]] = []
    checks.append(("VAL2047_00_local_sources_exist", source_ok, "all cited local source paths and needles exist"))
    checks.append(("VAL2047_01_csv_parse", all(csv_rows_parse(path) for path in csv_paths), "all generated CSV files parse cleanly"))
    checks.append(("VAL2047_02_signature_not_promoted", signature_verdict["status"] == "FAIL_CURRENT_CORPUS_PARENT_SIGNATURE_NOT_DERIVED", "observed-geometry slot signature is not promoted"))
    checks.append(("VAL2047_03_lc_derivation_conditional", lc_verdict["status"] == "MATH_CLEAN_PARENT_SIGNATURE_MISSING", "LC-zero derivation remains conditional"))
    checks.append(("VAL2047_04_cmts_first_row_nonclaim", cmts_verdict["current_status"] == "FIRST_CMTS_COEFFICIENT_ROW_STAGED_NOT_SCOREABLE", "first C_MTS coefficient chain is staged but nonclaim"))
    checks.append(("VAL2047_05_runner_rejects", runner_verdict["verdict"] == "PARENT_SIGNATURE_OR_SOURCED_CMTS_REQUIRED", "runner refuses both LC claim and C_MTS score"))
    checks.append(("VAL2047_06_claim_gates_closed", claim_gate["status"] == "FAIL_BLOCKED", "claim gates remain closed"))
    checks.append(("VAL2047_07_next_selected", next_rows_[0]["target_id"] == "NEXT2047_0_2048", "2048 motion-load coframe construction target selected"))
    checks.append(("VAL2047_08_formalization_unchanged", count_formalization_modified() == 0, "formalization-workbench modified-file count remains 0"))
    checks.append(("VAL2047_09_no_formalization_2047_artifacts", not formalization_has_2047_artifacts(), "no 2047 artifacts were written under formalization-workbench"))
    checks.append(("VAL2047_10_no_pycache", not scripts_pycache_exists(), "scripts __pycache__ removed"))
    overall_ok = all(ok for _, ok, _ in checks)
    checks.append(("VAL2047_OVERALL", overall_ok, "2047 fails the parent-signature promotion honestly, stages first C_MTS coefficient chain, and routes to primitive motion-load coframe construction"))
    rows = []
    for check_id, ok, detail in checks:
        row = base_row()
        row.update({"check_id": check_id, "status": "PASS" if ok else "FAIL", "detail": detail, "claim_allowed": False})
        rows.append(row)
    return rows


def write_doc(
    sources: list[dict[str, object]],
    signature_rows: list[dict[str, object]],
    lc_rows: list[dict[str, object]],
    cmts_rows: list[dict[str, object]],
    runner: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    sections = [
        "# 2047 Y5 R2FR Parent Observed Geometry Slot Signature Or C_MTS First Coefficient",
        "",
        "## Current Verdict",
        "",
        "2047 tries the clean connection route first. The exact LC-zero proof is available: if the parent local ordinary action has one quotient-owned observed coframe/metric and no independent affine `Gamma_MTS` slot in matter, spin, source, clocks, light or orbital readout, then `Gamma_MTS=LC[g_obs]`, `T_MTS=0`, `Q_MTS=0`, and the axial torsion branch dies by theorem.",
        "",
        "The current corpus still does not parent-sign that full observed-geometry slot. The failure is now narrow: it is not the algebra, it is the missing parent action authority across observed coframe, spin connection, source/readout, constants/shadow frames and boundary currents. Therefore 2047 also stages the first executable-shaped `C_MTS` coefficient chain with units and observable links, but no numeric score. No local-GR, Newton, WEP, clock, orbital, PPN, R10, torsion, GitHub, or public claim is made.",
        "",
        "## Source Register",
        md_table(sources, ["source_id", "source_kind", "source_path", "status", "note", "valid_for_claim"]),
        "## Parent Observed-Geometry Slot Audit",
        md_table(signature_rows, ["row_id", "clause", "mathematical_form", "status", "if_signed", "blocker", "claim_allowed"]),
        "## LC-Zero Derivation Attempt",
        md_table(lc_rows, ["row_id", "step", "statement", "status", "required_clause", "blocker", "claim_allowed"]),
        "## C_MTS First Coefficient Chain",
        md_table(cmts_rows, ["row_id", "symbol", "formula", "units", "current_status", "observable_links", "source_anchor", "ready_for_scoring", "claim_allowed"]),
        "## Runner Refusals",
        md_table(runner, ["run_id", "input_id", "attempted", "verdict", "reason", "score_attempted", "claim_allowed"]),
        "## Claim Gate",
        md_table(gates, ["row_id", "gate", "status", "detail", "claim_allowed"]),
        "## Decision Ledger",
        md_table(decisions, ["row_id", "decision", "rationale", "claim_allowed"]),
        "## Next Target",
        md_table(next_rows_, ["target_id", "target_doc", "objective", "must_include", "excluded", "claim_allowed"]),
        "## Branch Copies",
        md_table(copies, ["copy_id", "path", "rows", "status", "valid_for_claim"]),
        "## Validation",
        md_table(validation, ["check_id", "status", "detail", "claim_allowed"]),
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    sources = source_register_rows()
    signature_rows = observed_geometry_signature_rows()
    lc_rows = lc_derivation_attempt_rows()
    cmts_rows = cmts_first_coefficient_rows()
    runner = runner_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows_ = next_target_rows()
    paths = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2047_SOURCE_REGISTER.csv",
        "signature": OUT / "P8_Y5_PARENT_QLOC_2047_OBSERVED_GEOMETRY_SLOT_AUDIT.csv",
        "lc": OUT / "P8_Y5_PARENT_QLOC_2047_LC_ZERO_DERIVATION_ATTEMPT.csv",
        "cmts": OUT / "P8_Y5_PARENT_QLOC_2047_CMTS_FIRST_COEFFICIENT_CHAIN.csv",
        "runner": OUT / "P8_Y5_PARENT_QLOC_2047_RUNNER_REFUSALS.csv",
        "gates": OUT / "P8_Y5_PARENT_QLOC_2047_CLAIM_GATE.csv",
        "decision": OUT / "P8_Y5_PARENT_QLOC_2047_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2047_NEXT_TARGET.csv",
        "branch": OUT / "P8_Y5_PARENT_QLOC_2047_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2047_VALIDATION.csv",
    }
    write_csv(paths["sources"], sources)
    write_csv(paths["signature"], signature_rows)
    write_csv(paths["lc"], lc_rows)
    write_csv(paths["cmts"], cmts_rows)
    write_csv(paths["runner"], runner)
    write_csv(paths["gates"], gates)
    write_csv(paths["decision"], decisions)
    write_csv(paths["next"], next_rows_)
    copies = write_branch_copies(signature_rows, cmts_rows, next_rows_)
    write_csv(paths["branch"], copies)
    remove_pycache()
    csv_paths_without_validation = [path for key, path in paths.items() if key != "validation"] + [Path(row["path"]) for row in copies]
    validation = validation_rows(sources, signature_rows, lc_rows, cmts_rows, runner, gates, next_rows_, csv_paths_without_validation)
    write_csv(paths["validation"], validation)
    csv_paths = list(paths.values()) + [Path(row["path"]) for row in copies]
    remove_pycache()
    validation = validation_rows(sources, signature_rows, lc_rows, cmts_rows, runner, gates, next_rows_, csv_paths)
    write_csv(paths["validation"], validation)
    write_doc(sources, signature_rows, lc_rows, cmts_rows, runner, gates, decisions, next_rows_, copies, validation)
    remove_pycache()


if __name__ == "__main__":
    main()
