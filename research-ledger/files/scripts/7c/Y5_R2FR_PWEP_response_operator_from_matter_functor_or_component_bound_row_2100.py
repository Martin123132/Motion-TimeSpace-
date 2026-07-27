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


DOC = ROOT / "2100-Y5-R2FR-PWEP-response-operator-from-matter-functor-or-component-bound-row.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()

SRC_2099 = ROOT / "2099-Y5-R2FR-DeltaGamma-component-map-to-P4-WEP-PPN-clock-orbital-residuals.md"
SRC_1837 = ROOT / "1837-Y5-R2FR-PWEP-response-operator-from-matter-functor-or-component-bound-row.md"
SRC_1838 = ROOT / "1838-Y5-R2FR-ordinary-matter-action-signature-source-label-forgetting-or-WEP-bound-first-fill.md"
SRC_1839 = ROOT / "1839-Y5-R2FR-source-shadow-ban-or-tauWEP-direct-product-first-source-row.md"
SRC_1840 = ROOT / "1840-Y5-R2FR-EH-dominance-and-residual-sector-silence-or-operator-coefficient-pack.md"
SRC_1841 = ROOT / "1841-Y5-R2FR-sector-action-variation-and-local-scaling-silence-or-operator-bounds.md"
CSV_1837_WEP_BOUNDS = OUT / "P8_Y5_PARENT_QLOC_1837_WEP_COMPONENT_BOUND_ROWS.csv"
CSV_1838_FIRST_WEP = OUT / "P8_Y5_PARENT_QLOC_1838_FIRST_WEP_COMPONENT_BOUND_INPUT.csv"
CSV_1839_TAU = OUT / "P8_Y5_PARENT_QLOC_1839_TAUWEP_DIRECT_PRODUCT_SOURCE_ROW.csv"
CSV_1840_OPS = OUT / "P8_Y5_PARENT_QLOC_1840_OPERATOR_COEFFICIENT_PACK.csv"
CSV_1841_DEC = OUT / "P8_Y5_PARENT_QLOC_1841_DECISION_LEDGER.csv"
CSV_1069_MICROSCOPE = OUT / "P8_Y5_R10_1069_MICROSCOPE_PROVENANCE_LEDGER.csv"
CSV_1067_TAU = OUT / "P8_Y5_R10_1067_TAU_WEP_ACQUISITION_SCHEMA.csv"
BRANCH_LOCK = ROOT / "source-intake" / "microscope" / "branch_classifier" / "P_WEP_same_parent_branch_lock.csv"


def row(**kwargs: object) -> dict[str, object]:
    data = base_row()
    data["claim_allowed"] = False
    data.update(kwargs)
    return data


def truthy(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "1", "yes", "pass", "valid", "claim_allowed", "selected"}


def formalization_has_2100_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2100-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2100*",
        "*Y5_R2FR_PWEP_response_operator_from_matter_functor_or_component_bound_row_2100*",
        "*AFRAME_PWEP_RESPONSE_OPERATOR_2100*",
        "*JR2100_SECTOR_LAGRANGIAN_BOUNDARY_OWNER*",
    )
    try:
        return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))
    except Exception:
        return False


def source_register_rows() -> list[dict[str, object]]:
    specs: list[tuple[str, Path, list[str], str]] = [
        (
            "SRC2100_00_2099_handoff",
            SRC_2099,
            ["NEXT2099_0_2100", "P_WEP_FROM_MATTER_FUNCTOR_NEXT", "VAL2099_OVERALL"],
            "2099 selects P_WEP from the matter functor as the first response operator.",
        ),
        (
            "SRC2100_01_1837_PWEP",
            SRC_1837,
            ["PWD1837_1_conditional_zero_theorem", "PWEP_NOT_DERIVED_CURRENT_CORPUS", "VAL1837_OVERALL"],
            "1837 gives the exact conditional P_WEP=0 theorem and refuses the current claim.",
        ),
        (
            "SRC2100_02_1838_matter_signature",
            SRC_1838,
            ["ORDINARY_MATTER_SIGNATURE_NOT_PARENT_SIGNED", "FWCB1838_0_delta_w_TiPt", "VAL1838_OVERALL"],
            "1838 tests ordinary-matter signature/source-label forgetting and stages first WEP input rows.",
        ),
        (
            "SRC2100_03_1839_tau_direct",
            CSV_1839_TAU,
            ["TDP1839_0_tau_WEP", "TDP1839_2_direct_product", "REFUSAL_ACTIVE"],
            "1839 stages tau_WEP/direct-product acquisition rows as nonclaim.",
        ),
        (
            "SRC2100_04_1839_decision_doc",
            SRC_1839,
            ["SOURCE_SHADOW_CLASSIFIED_NOT_ZEROED", "TAUWEP_DIRECT_PRODUCT_FIRST_SOURCE_ROW_STAGED_NONCLAIM", "VAL1839_OVERALL"],
            "1839 classifies source shadow and routes the serious GR/Newton work back to EH/operator residuals.",
        ),
        (
            "SRC2100_05_1840_operator_pack",
            CSV_1840_OPS,
            ["OPC1840_0_total_DeltaE", "OPC1840_6_source_normalization", "MISSING_ZERO_THEOREM_OR_BOUNDED_COEFFICIENTS"],
            "1840 carries the left-hand non-Einstein operator residual pack.",
        ),
        (
            "SRC2100_06_1841_sector_decision",
            CSV_1841_DEC,
            ["NO_NON_EH_SECTOR_FULLY_SILENCED", "SECTOR_LAGRANGIAN_BOUNDARY_OWNER_OR_FB5540_SOURCE_ROW_IS_NEXT"],
            "1841 says no non-EH sector is fully silenced and selects sector Lagrangian/boundary owner next.",
        ),
        (
            "SRC2100_07_1837_WEP_bounds",
            CSV_1837_WEP_BOUNDS,
            ["WCB1837_0_spin", "WCB1837_5_total_guard", "TOTAL_SCORE_REFUSED"],
            "1837 component-bound rows are the WEP fallback ledger.",
        ),
        (
            "SRC2100_08_1838_first_input",
            CSV_1838_FIRST_WEP,
            ["FWCB1838_0_delta_w_TiPt", "FWCB1838_4_refusal_guard", "MISSING_TAU_WEP"],
            "1838 first WEP material/source input row records Delta_w/tau/direct-product requirements.",
        ),
        (
            "SRC2100_09_MICROSCOPE_anchor",
            CSV_1069_MICROSCOPE,
            ["PROV1069_1_R0_direct_geometry", "PhysRevLett.129.121102"],
            "MICROSCOPE Ti/Pt bound anchor exists but is comparator-only for MTS rows.",
        ),
        (
            "SRC2100_10_tau_schema",
            CSV_1067_TAU,
            ["TAQ1067_0_tau_zero_option", "TAQ1067_4_refusal_rule", "MISSING_THEOREM_ZERO"],
            "tau_WEP acquisition schema refuses tau=1 and other shortcut rows.",
        ),
        (
            "SRC2100_11_branch_lock",
            BRANCH_LOCK,
            ["forbidden_mixing_rule", "BRANCH_CLASSIFIER_FIRST_FILL_NONCLAIM"],
            "same-parent-branch lock prevents mixed-basis WEP products becoming predictions.",
        ),
    ]
    rows: list[dict[str, object]] = []
    for source_id, path, needles, use in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            row(
                source_id=source_id,
                source_kind="2100_PWEP_response_operator_gate",
                source_path=str(path),
                path_exists=exists,
                needles="; ".join(needles),
                needle_found=exists and all(needle in text for needle in needles),
                use_in_2100=use,
                valid_for_claim=False,
            )
        )
    return rows


def pwep_derivation_rows() -> list[dict[str, object]]:
    return [
        row(
            theorem_id="PWE2100_0_target",
            claim_piece="P_WEP response operator",
            formal_statement="eta_AB = g_N^-1 n_mu[(a_A^mu-a_B^mu)] = P_WEP_eta_AB · DeltaGamma_WEP for ordinary test bodies A,B.",
            proof_status="TARGET_DEFINED",
            missing_for_parent_claim="derive P_WEP_eta_AB from one parent matter functor, same-frame readout and common DeltaGamma units",
            parent_signed=False,
            valid_for_claim=False,
        ),
        row(
            theorem_id="PWE2100_1_conditional_zero",
            claim_piece="universal observed matter descent gives P_WEP=0",
            formal_statement="If all ordinary matter actions factor through one observed coframe/metric, omega[e_obs], q-owned constants, one measure/current owner and no source-only species selector, then structureless test accelerations are common-mode and P_WEP_eta_AB=0.",
            proof_status="EXACT_CONDITIONAL_THEOREM",
            missing_for_parent_claim="ordinary matter signature, no shadow source/readout, source-label forgetting and variation-before-readout are not all parent-signed",
            parent_signed=False,
            valid_for_claim=False,
        ),
        row(
            theorem_id="PWE2100_2_current_blocker",
            claim_piece="current MTS derives P_WEP=0",
            formal_statement="The current corpus supplies the universal ordinary-matter action signature needed by PWE2100_1.",
            proof_status="FAIL_CURRENT_CORPUS",
            missing_for_parent_claim="1838 keeps ordinary matter signature/source-label forgetting unsigned; 1839 keeps shadow/tau/direct rows nonclaim",
            parent_signed=False,
            valid_for_claim=False,
        ),
        row(
            theorem_id="PWE2100_3_leakage_decomposition",
            claim_piece="WEP leakage vector",
            formal_statement="eta_AB = eta_spin_AB + eta_material_AB + eta_clock_AB + eta_projective_AB + eta_frame/readout_AB with absolute-sum guard unless a parent cancellation identity is signed.",
            proof_status="FORMAL_DECOMPOSITION_WRITTEN",
            missing_for_parent_claim="component response tensors, numeric values, common units and no-cancellation identity are missing",
            parent_signed=False,
            valid_for_claim=False,
        ),
        row(
            theorem_id="PWE2100_4_MICROSCOPE_comparator",
            claim_piece="MICROSCOPE comparison path",
            formal_statement="A prediction may compare to the Ti/Pt MICROSCOPE anchor only after P_WEP/product convention/source-material branch lock and component rows share one parent branch.",
            proof_status="COMPARATOR_EXISTS_PREDICTION_MISSING",
            missing_for_parent_claim="tau_WEP/direct product and official source/readout/material product files remain missing",
            parent_signed=False,
            valid_for_claim=False,
        ),
        row(
            theorem_id="PWE2100_5_verdict",
            claim_piece="current P_WEP status",
            formal_statement="P_WEP=0 is a clean conditional theorem, not a current MTS claim; the WEP branch remains an explicit nonclaim component-bound route.",
            proof_status="PWEP_NOT_DERIVED_CURRENT_CHAIN",
            missing_for_parent_claim="parent matter action signature or source-backed WEP component/direct-product inputs",
            parent_signed=False,
            valid_for_claim=False,
        ),
    ]


def wep_component_bound_rows() -> list[dict[str, object]]:
    specs = [
        (
            "WCB2100_0_spin",
            "spin_hypermomentum",
            "eta_spin_AB",
            "abs(g_N^-1 n_mu (P_A^spin-P_B^spin)^mu_i DeltaGamma_spin^i)",
            "parent spin-torsion zero theorem OR numeric spin response with units/source path",
            "MISSING_SPIN_RESPONSE_AND_DELTAGAMMA_SPIN",
            str(CSV_1069_MICROSCOPE),
        ),
        (
            "WCB2100_1_material_source_weight",
            "material_marker_connection_current",
            "eta_material_AB",
            "abs(Delta_w_TiPt * tau_WEP) or abs(P_WEP_material · DeltaGamma_material)",
            "source-label forgetting zero theorem OR numeric Delta_w_TiPt and tau_WEP/direct product",
            "MISSING_DELTA_W_AND_TAU_WEP",
            str(CSV_1838_FIRST_WEP),
        ),
        (
            "WCB2100_2_clock_rods",
            "clock_rod_nonmetric_connection_current",
            "eta_clock_AB",
            "abs(g_N^-1 n_mu (P_A^Qtrace-P_B^Qtrace)^mu_i DeltaGamma_clock^i)",
            "clock/rod metric descent theorem OR numeric Q_trace clock/rod response",
            "MISSING_CLOCK_ROD_RESPONSE_AND_Q_TRACE",
            str(CSV_1069_MICROSCOPE),
        ),
        (
            "WCB2100_3_projective_trace",
            "projective_trace_current",
            "eta_projective_AB",
            "abs(g_N^-1 n_mu (P_A^proj-P_B^proj)^mu_i DeltaGamma_projective^i)",
            "all-sector projective invariance theorem OR sourced trace leakage bound",
            "MISSING_PROJECTIVE_INVARIANCE_OR_TRACE_BOUND",
            str(CSV_1069_MICROSCOPE),
        ),
        (
            "WCB2100_4_frame_readout",
            "Delta_frame_Delta_cal_Delta_tau_n",
            "eta_frame_readout_AB",
            "abs(P_frame · Delta_frame + P_cal · Delta_cal + P_tau · Delta_tau_n)",
            "single observed coframe/source/readout theorem OR numeric frame/readout residuals",
            "MISSING_SINGLE_FRAME_THEOREM_OR_NUMERIC_FRAME_RESIDUAL",
            str(ROOT / "1155-Y5-R10-single-observed-coframe-source-frame-owner-or-frame-residual-row.md"),
        ),
        (
            "WCB2100_5_total_guard",
            "WEP_component_vector",
            "eta_total_guard",
            "sum_i abs(eta_i) <= eta_bound unless parent identity proves exact cancellation",
            "all WCB2100 component rows pass or theorem-zero vector identity is parent-signed",
            "MISSING_COMPONENT_VALUES",
            str(BRANCH_LOCK),
        ),
    ]
    return [
        row(
            bound_row_id=bound_id,
            component=component,
            target=target,
            formula=formula,
            accepted_evidence=evidence,
            current_value=current_value,
            units="dimensionless",
            comparison_bound="MICROSCOPE_TiPt_eta_bound_anchor_nonclaim",
            source_path=source_path,
            status="TOTAL_SCORE_REFUSED" if bound_id.endswith("_total_guard") else "COMPONENT_BOUND_ROW_STAGED_NONCLAIM",
            source_backed=False,
            score_ready=False,
            valid_for_claim=False,
        )
        for bound_id, component, target, formula, evidence, current_value, source_path in specs
    ]


def tau_direct_rows() -> list[dict[str, object]]:
    return [
        row(
            source_row_id="TDP2100_0_tau_WEP",
            quantity="tau_WEP",
            definition="branch-locked normalized local source/readout/material projection converting Delta_w_TiPt into eta_material_TiPt",
            current_value="MISSING_OFFICIAL_READOUT_SOURCE_MATERIAL_PRODUCT",
            units="dimensionless projection factor",
            source_path=str(CSV_1839_TAU),
            status="TAUWEP_SOURCE_ROW_STAGED_NONCLAIM",
            score_ready=False,
            valid_for_claim=False,
        ),
        row(
            source_row_id="TDP2100_1_direct_product",
            quantity="P_WEP_source_weight",
            definition="unsplit parent product in the reported MICROSCOPE Ti/Pt channel",
            current_value="MISSING_DIRECT_PRODUCT_INPUTS",
            units="dimensionless eta contribution",
            source_path=str(CSV_1839_TAU),
            status="DIRECT_PRODUCT_ROW_STAGED_NONCLAIM",
            score_ready=False,
            valid_for_claim=False,
        ),
        row(
            source_row_id="TDP2100_2_product_comparator",
            quantity="abs(Delta_w_TiPt * tau_WEP)",
            definition="comparison-side MICROSCOPE product bound anchor",
            current_value="BOUND_COMPARATOR_ONLY_NONCLAIM",
            units="dimensionless",
            source_path=str(CSV_1839_TAU),
            status="COMPARATOR_NOT_PREDICTION",
            score_ready=False,
            valid_for_claim=False,
        ),
        row(
            source_row_id="TDP2100_3_refusal_guard",
            quantity="tau/direct shortcut guard",
            definition="reject tau_WEP=1, bound inversion, measured-G absorption, cancellation, surrogate arrays and mixed branch rows",
            current_value="REFUSAL_ACTIVE",
            units="not_applicable",
            source_path=str(BRANCH_LOCK),
            status="GUARD_ACTIVE",
            score_ready=False,
            valid_for_claim=False,
        ),
    ]


def gr_handoff_rows() -> list[dict[str, object]]:
    return [
        row(
            handoff_id="GRH2100_0_source_side_status",
            subject="WEP/source-side coupling",
            status="NARROWED_NOT_CLAIMED",
            evidence="P_WEP conditional theorem exact; WEP component and tau/direct rows explicit nonclaim",
            consequence="do not loop on WEP without new matter-signature or tau/direct-product source input",
            valid_for_claim=False,
        ),
        row(
            handoff_id="GRH2100_1_left_hand_operator",
            subject="EH/Einstein operator dominance",
            status="OPEN_HARD_BLOCKER",
            evidence="1840 retains DeltaE_munu and operator coefficient pack; 1841 says no non-EH sector fully silenced",
            consequence="GR/Newton reduction needs sector action variation and boundary/current owner, not another WEP slogan",
            valid_for_claim=False,
        ),
        row(
            handoff_id="GRH2100_2_next_structure",
            subject="sector Lagrangian/boundary owner",
            status="SELECTED_NEXT",
            evidence="1841 DEC1841_3 selects sector Lagrangian boundary owner or FB5540 source row",
            consequence="next checkpoint should derive L_X/Theta_X/Q_X plus B_ref/B_class/tau ownership or stage FB5540 source rows",
            valid_for_claim=False,
        ),
    ]


def gate_rows() -> list[dict[str, object]]:
    gates = [
        ("GATE2100_0_conditional_PWEP", "universal matter descent implies P_WEP=0", "PASS_CONDITIONAL_NONCLAIM", "mathematically exact under unsigned premises"),
        ("GATE2100_1_current_PWEP", "current MTS derives P_WEP=0", "FAIL_UNSIGNED_PARENT_SIGNATURE", "ordinary matter signature/source-label/source-shadow clauses are unsigned"),
        ("GATE2100_2_WEP_bound_rows", "WEP component rows are score-ready", "FAIL_MISSING_VALUES", "component values, response tensors, tau/direct product and official product files are missing"),
        ("GATE2100_3_MICROSCOPE_score", "MTS can compare a prediction to MICROSCOPE", "FAIL_COMPARATOR_ONLY", "bound anchor exists but prediction-side rows are nonclaim"),
        ("GATE2100_4_EH_dominance", "local Einstein operator dominance is derived", "FAIL_BLOCKED", "1840/1841 retain non-EH operator residuals"),
        ("GATE2100_5_local_GR_Newton", "local GR/Newton recovery is derived", "FAIL_BLOCKED", "source-side and left-hand operator gates remain incomplete"),
    ]
    return [
        row(gate_id=gate_id, claim=claim, status=status, reason=reason, valid_for_claim=False)
        for gate_id, claim, status, reason in gates
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        row(
            decision_id="DEC2100_0_PWEP_result",
            decision="PWEP_ZERO_THEOREM_EXACT_CONDITIONAL_NOT_CURRENT_CLAIM",
            basis="1837/1838 show universal observed-matter descent would kill P_WEP, but the parent signature and source-label shadow clauses are unsigned.",
            consequence="no WEP/local-GR claim and no tau/direct-product shortcut.",
            valid_for_claim=False,
        ),
        row(
            decision_id="DEC2100_1_WEP_rows",
            decision="WEP_COMPONENT_AND_TAU_DIRECT_ROWS_STAGED_NONCLAIM",
            basis="1837-1839 provide component, Delta_w, tau_WEP and direct-product ledgers with refusal guards.",
            consequence="WEP can become empirical only with theorem-zero or source-backed component/product inputs.",
            valid_for_claim=False,
        ),
        row(
            decision_id="DEC2100_2_no_WEP_loop",
            decision="DO_NOT_RECIRCLE_WEP_WITHOUT_NEW_INPUTS",
            basis="the WEP path is narrowed; repeating matter-functor prose will not derive GR/Newton.",
            consequence="shift the current-chain target to the left-hand sector Lagrangian/boundary owner blocker.",
            valid_for_claim=False,
        ),
        row(
            decision_id="DEC2100_3_best_next",
            decision="SECTOR_LAGRANGIAN_BOUNDARY_OWNER_OR_FB5540_SOURCE_ROW_NEXT",
            basis="1841 identifies this as the first missing structure that can make Pi_M^H, M_H_ref, boundary lock and tau lock derivable.",
            consequence="2101 should attack L_X/Theta_X/Q_X plus B_ref/B_class/tau ownership or stage FB5540 rows.",
            valid_for_claim=False,
        ),
    ]


def next_rows() -> list[dict[str, object]]:
    return [
        row(
            target_id="NEXT2100_0_2101",
            target_doc="2101-Y5-R2FR-sector-Lagrangian-boundary-owner-or-FB5540-source-row.md",
            target_script="scripts/Y5_R2FR_sector_Lagrangian_boundary_owner_or_FB5540_source_row_2101.py",
            objective="derive L_X/Theta_X/Q_X plus B_ref/B_class/tau ownership for the Hamiltonian source charge, or fill source-backed FB5540 rows with M_H_ref and all numerator components",
            success_condition="M_H_ref and every FB5540 numerator component are theorem-zero or source-backed nonclaim rows with units, signs, source paths and no-cancellation bookkeeping",
            forbidden_shortcuts="WEP pass claim; P_WEP=0 promotion; tau_WEP=1; measured-G absorption; EH import; GitHub; formalization-workbench edits",
            valid_for_claim=False,
        )
    ]


def write_branch_copies(
    pwep: list[dict[str, object]],
    wep_bounds: list[dict[str, object]],
    tau_rows: list[dict[str, object]],
    handoff: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
) -> list[dict[str, object]]:
    copies = [
        (
            SOURCE_WEIGHT_DOCS / "AFRAME_PWEP_RESPONSE_OPERATOR_2100_NONCLAIM.csv",
            pwep + wep_bounds + decisions,
            "source_weight_docs",
        ),
        (
            BRANCH_WEP / "P8_Y5_PARENT_QLOC_2100_WEP_GATE_NONCLAIM.csv",
            wep_bounds + tau_rows,
            "branch_locked_wep",
        ),
        (
            QUEUE / "JR2100_SECTOR_LAGRANGIAN_BOUNDARY_OWNER_NEXT_QUEUE.csv",
            handoff + decisions + next_rows_,
            "rab_acquisition_queue",
        ),
    ]
    rows: list[dict[str, object]] = []
    for path, data_rows, copy_kind in copies:
        write_csv(path, data_rows)
        rows.append(
            row(
                copy_id=f"COPY2100_{len(rows)}",
                copy_kind=copy_kind,
                path=str(path),
                rows=len(data_rows),
                parses=csv_rows_parse(path),
                valid_for_claim=False,
            )
        )
    return rows


def validation_rows(
    sources: list[dict[str, object]],
    pwep: list[dict[str, object]],
    wep_bounds: list[dict[str, object]],
    tau_rows: list[dict[str, object]],
    handoff: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    copies: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    source_ok = all(truthy(r["path_exists"]) and truthy(r["needle_found"]) for r in sources)
    conditional_ok = any(r["theorem_id"] == "PWE2100_1_conditional_zero" and r["proof_status"] == "EXACT_CONDITIONAL_THEOREM" for r in pwep)
    current_refused = any(r["theorem_id"] == "PWE2100_5_verdict" and r["proof_status"] == "PWEP_NOT_DERIVED_CURRENT_CHAIN" for r in pwep)
    bounds_nonclaim = len(wep_bounds) == 6 and all(not truthy(r["source_backed"]) and not truthy(r["score_ready"]) for r in wep_bounds)
    tau_nonclaim = len(tau_rows) == 4 and all(not truthy(r["score_ready"]) for r in tau_rows)
    handoff_ok = any(r["handoff_id"] == "GRH2100_2_next_structure" and r["status"] == "SELECTED_NEXT" for r in handoff)
    gates_safe = all(not truthy(r["claim_allowed"]) for r in gates) and all(
        str(r["status"]).startswith("FAIL") or r["status"] == "PASS_CONDITIONAL_NONCLAIM" for r in gates
    )
    decision_ok = any(r["decision_id"] == "DEC2100_3_best_next" and r["decision"] == "SECTOR_LAGRANGIAN_BOUNDARY_OWNER_OR_FB5540_SOURCE_ROW_NEXT" for r in decisions)
    next_ok = next_rows_[0]["target_id"] == "NEXT2100_0_2101"
    copies_ok = all(truthy(r["parses"]) and Path(str(r["path"])).exists() for r in copies)
    csv_ok = all(path.exists() and csv_rows_parse(path) for path in csv_paths)
    no_claim_flags = all(
        not truthy(r.get("claim_allowed")) and not truthy(r.get("valid_for_claim"))
        for group in [sources, pwep, wep_bounds, tau_rows, handoff, gates, decisions, next_rows_, copies]
        for r in group
    )
    formalization_clean = count_formalization_modified() == 0 and not formalization_has_2100_artifacts()
    pycache_clean = not (SCRIPT_PATH.parent / "__pycache__").exists()
    checks = [
        ("VAL2100_00_sources", source_ok, "all cited source paths exist and contain required needles"),
        ("VAL2100_01_conditional", conditional_ok, "conditional P_WEP zero theorem is recorded"),
        ("VAL2100_02_current_refused", current_refused, "current P_WEP claim is refused"),
        ("VAL2100_03_wep_bounds", bounds_nonclaim, "six WEP component-bound rows remain nonclaim and not score-ready"),
        ("VAL2100_04_tau_direct", tau_nonclaim, "tau/direct product rows remain nonclaim"),
        ("VAL2100_05_handoff", handoff_ok, "GR/operator handoff selects sector Lagrangian boundary owner"),
        ("VAL2100_06_claim_gates", gates_safe, "claim gates block WEP/EH/local-GR promotion"),
        ("VAL2100_07_decision", decision_ok, "decision selects sector Lagrangian boundary owner next"),
        ("VAL2100_08_next", next_ok, "next target is 2101 sector Lagrangian boundary owner"),
        ("VAL2100_09_branch_copies", copies_ok, "branch copies exist and parse"),
        ("VAL2100_10_csv_parse", csv_ok, "all generated CSVs parse cleanly"),
        ("VAL2100_11_no_claim_flags", no_claim_flags, "no generated row allows a claim"),
        ("VAL2100_12_formalization_clean", formalization_clean, "formalization-workbench untouched by 2100"),
        ("VAL2100_13_no_pycache", pycache_clean, "scripts __pycache__ removed"),
    ]
    rows = [
        row(check_id=check_id, status="PASS" if passed else "FAIL", detail=detail, valid_for_claim=False)
        for check_id, passed, detail in checks
    ]
    overall = all(r["status"] == "PASS" for r in rows)
    rows.append(
        row(
            check_id="VAL2100_OVERALL",
            status="PASS" if overall else "FAIL",
            detail="2100 records P_WEP as exact conditional but not current MTS, keeps WEP rows nonclaim, and hands off to sector Lagrangian/boundary owner for GR/Newton reduction" if overall else "one or more 2100 validation gates failed",
            valid_for_claim=False,
        )
    )
    return rows


def write_doc(
    sources: list[dict[str, object]],
    pwep: list[dict[str, object]],
    wep_bounds: list[dict[str, object]],
    tau_rows: list[dict[str, object]],
    handoff: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    text = "\n\n".join(
        [
            "# 2100 - Y5/R2FR P_WEP Response Operator From Matter Functor Or Component Bound Row",
            "## Current Verdict\n\n2100 closes the current WEP loop without pretending WEP is solved. The clean theorem is real: if ordinary matter descends through one observed geometry/current/measure stack with no source-only species labels or shadow readout, then `P_WEP=0`. That is an exact conditional theorem, not a current MTS claim.\n\nThe honest state is sharper than before: WEP is now a ledger of explicit nonclaim rows (`eta_spin`, `eta_material`, `eta_clock`, `eta_projective`, frame/readout, and total guard), plus tau/direct-product acquisition rows. Since 1838 and 1839 already chased the ordinary-matter/source-shadow route and kept it nonclaim, the next serious GR/Newton move is not more WEP prose; it is the sector Lagrangian/boundary owner needed for EH dominance and the Hamiltonian source charge.",
            "## Source Register",
            md_table(sources, ["source_id", "source_kind", "source_path", "path_exists", "needle_found", "use_in_2100", "claim_allowed", "valid_for_claim"]),
            "## P_WEP Derivation Attempt",
            md_table(pwep, ["theorem_id", "claim_piece", "formal_statement", "proof_status", "missing_for_parent_claim", "parent_signed", "claim_allowed", "valid_for_claim"]),
            "## WEP Component-Bound Rows",
            md_table(wep_bounds, ["bound_row_id", "component", "target", "formula", "accepted_evidence", "current_value", "units", "comparison_bound", "source_path", "status", "source_backed", "score_ready", "claim_allowed", "valid_for_claim"]),
            "## TauWEP / Direct Product Rows",
            md_table(tau_rows, ["source_row_id", "quantity", "definition", "current_value", "units", "source_path", "status", "score_ready", "claim_allowed", "valid_for_claim"]),
            "## GR Newton Handoff",
            md_table(handoff, ["handoff_id", "subject", "status", "evidence", "consequence", "claim_allowed", "valid_for_claim"]),
            "## Claim Gates",
            md_table(gates, ["gate_id", "claim", "status", "reason", "claim_allowed", "valid_for_claim"]),
            "## Decision Ledger",
            md_table(decisions, ["decision_id", "decision", "basis", "consequence", "claim_allowed", "valid_for_claim"]),
            "## Next Target",
            md_table(next_rows_, ["target_id", "target_doc", "target_script", "objective", "success_condition", "forbidden_shortcuts", "claim_allowed", "valid_for_claim"]),
            "## Branch Copies",
            md_table(copies, ["copy_id", "copy_kind", "path", "rows", "parses", "claim_allowed", "valid_for_claim"]),
            "## Validation",
            md_table(validation, ["check_id", "status", "detail", "claim_allowed", "valid_for_claim"]),
        ]
    )
    DOC.write_text(text + "\n", encoding="utf-8")


def main() -> None:
    remove_pycache()
    sources = source_register_rows()
    pwep = pwep_derivation_rows()
    wep_bounds = wep_component_bound_rows()
    tau_rows = tau_direct_rows()
    handoff = gr_handoff_rows()
    gates = gate_rows()
    decisions = decision_rows()
    next_rows_ = next_rows()
    paths = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2100_SOURCE_REGISTER.csv",
        "pwep": OUT / "P8_Y5_PARENT_QLOC_2100_PWEP_DERIVATION_ATTEMPT.csv",
        "wep_bounds": OUT / "P8_Y5_PARENT_QLOC_2100_WEP_COMPONENT_BOUND_ROWS.csv",
        "tau": OUT / "P8_Y5_PARENT_QLOC_2100_TAUWEP_DIRECT_PRODUCT_ROWS.csv",
        "handoff": OUT / "P8_Y5_PARENT_QLOC_2100_GR_NEWTON_HANDOFF.csv",
        "gates": OUT / "P8_Y5_PARENT_QLOC_2100_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_PARENT_QLOC_2100_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2100_NEXT_TARGET.csv",
        "branch": OUT / "P8_Y5_PARENT_QLOC_2100_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2100_VALIDATION.csv",
    }
    write_csv(paths["sources"], sources)
    write_csv(paths["pwep"], pwep)
    write_csv(paths["wep_bounds"], wep_bounds)
    write_csv(paths["tau"], tau_rows)
    write_csv(paths["handoff"], handoff)
    write_csv(paths["gates"], gates)
    write_csv(paths["decisions"], decisions)
    write_csv(paths["next"], next_rows_)
    copies = write_branch_copies(pwep, wep_bounds, tau_rows, handoff, decisions, next_rows_)
    write_csv(paths["branch"], copies)
    csv_paths = [path for key, path in paths.items() if key != "validation"] + [Path(str(r["path"])) for r in copies]
    remove_pycache()
    validation = validation_rows(sources, pwep, wep_bounds, tau_rows, handoff, gates, decisions, next_rows_, copies, csv_paths)
    write_csv(paths["validation"], validation)
    write_doc(sources, pwep, wep_bounds, tau_rows, handoff, gates, decisions, next_rows_, copies, validation)
    remove_pycache()
    print(f"wrote {DOC}")
    print(f"validation {paths['validation']}")


if __name__ == "__main__":
    main()
