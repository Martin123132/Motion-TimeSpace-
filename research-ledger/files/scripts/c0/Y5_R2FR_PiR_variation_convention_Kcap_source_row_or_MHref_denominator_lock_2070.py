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


DOC = ROOT / "2070-Y5-R2FR-PiR-variation-convention-Kcap-source-row-or-MHref-denominator-lock.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()


def formalization_has_2070_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    try:
        patterns = (
            "*2070-Y5-R2FR*",
            "*P8_Y5_PARENT_QLOC_2070*",
            "*Y5_R2FR_PiR_variation_convention_Kcap_source_row_or_MHref_denominator_lock_2070*",
        )
        return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))
    except Exception:
        return False


def scripts_pycache_exists() -> bool:
    return (SCRIPT_PATH.parent / "__pycache__").exists()


def source_register_rows() -> list[dict[str, object]]:
    specs = [
        (
            "SRC2070_00_2069_doc",
            ROOT / "2069-Y5-R2FR-Kcap-to-PiR-conversion-or-Mref-theta-component-first-row.md",
            ["NEXT2069_0_2070", "KPC2069_3_operator_norm_definition", "MTR2069_0_MHref_candidate"],
            "2069 handoff into Pi_R variation convention or M_H_ref denominator lock.",
        ),
        (
            "SRC2070_01_2069_next",
            OUT / "P8_Y5_PARENT_QLOC_2069_NEXT_TARGET.csv",
            ["NEXT2069_0_2070", "Pi_R density/integrated convention", "H_tau-H_ref denominator gate"],
            "machine-readable 2070 target.",
        ),
        (
            "SRC2070_02_2069_Kcap",
            OUT / "P8_Y5_PARENT_QLOC_2069_KCAP_TO_PIR_CONVERSION_GATE.csv",
            ["KPC2069_2_same_functional_requirement", "KPC2069_5_reject_fake_unity", "FAIL_CURRENT_CLAIM_KCAP_TO_PIR_UNSIGNED"],
            "K_cap_to_PiR gate and fake-unity rejection.",
        ),
        (
            "SRC2070_03_2069_Mref_theta",
            OUT / "P8_Y5_PARENT_QLOC_2069_MREF_THETA_FIRST_ROW.csv",
            ["MTR2069_0_MHref_candidate", "MTR2069_5_first_row_formula", "SCHEMA_ONLY_NONCLAIM"],
            "M_ref/theta first-row schema.",
        ),
        (
            "SRC2070_04_legacy_PiR",
            ROOT / "06-reciprocal-charge-source-neutrality.md",
            ["delta S_boundary = [W R_AB' + Pi_R]", "Q_R = -Pi_R", "Pi_R = source reciprocal momentum/charge"],
            "legacy Pi_R boundary-variation definition.",
        ),
        (
            "SRC2070_05_2062_boundary_grammar",
            OUT / "P8_Y5_PARENT_QLOC_2062_BOUNDARY_FUNCTIONAL_GRAMMAR.csv",
            ["BGA2062_1_natural_variation", "BGA2062_3_corner_worldtube", "BGA2062_4_orientation"],
            "R_AB natural variation, corner/worldtube blocker and orientation debt.",
        ),
        (
            "SRC2070_06_2063_component_intake",
            OUT / "P8_Y5_PARENT_QLOC_2063_FINITE_PIR_COMPONENT_INTAKE.csv",
            ["PCI2063_3_corner_bound", "PCI2063_4_total_join", "PCI2063_5_qR_Cassini_join"],
            "Pi_R component absolute join and q_R guard.",
        ),
        (
            "SRC2070_07_1006_MHref_doc",
            ROOT / "1006-Y5-R10-MHref-positive-same-frame-denominator-or-Htau-source-row.md",
            ["DEC1006_0_denominator_not_claimed", "DEC1006_2_next_integrability_target", "V1006_8_claim_gates_blocked"],
            "M_H_ref denominator remains nonclaim and points to integrability.",
        ),
        (
            "SRC2070_08_1006_denominator_audit",
            OUT / "P8_Y5_R10_1006_MHREF_DENOMINATOR_THEOREM_AUDIT.csv",
            ["MHA1006_1_integrability", "MHA1006_5_anti_circularity", "MHA1006_6_theorem_verdict"],
            "M_H_ref theorem audit.",
        ),
        (
            "SRC2070_09_1007_integrability",
            ROOT / "1007-Y5-R10-Htau-integrability-fixed-reference-theorem-or-symplectic-residual-row.md",
            ["SRS1007_0_integrability_formula", "SFR1007_0_missing_theta_Qtau", "DEC1007_0_integrability_not_claimed"],
            "H_tau integrability/fixed-reference checkpoint.",
        ),
        (
            "SRC2070_10_1008_theta_Qtau",
            ROOT / "1008-Y5-R10-parent-theta-Qtau-extraction-or-charge-decomposition-runner.md",
            ["CDS1008_3_reference_guard", "CDS1008_4_total_promoter", "CG1008_5_MHref"],
            "parent theta/Q_tau extraction and M_H_ref dependency.",
        ),
    ]
    rows: list[dict[str, object]] = []
    for source_id, source_path, needles, note in specs:
        exists = source_path.exists()
        text = read_text(source_path) if exists else ""
        ok = exists and all(needle in text for needle in needles)
        row = base_row()
        row.update(
            {
                "source_id": source_id,
                "source_kind": "local",
                "source_path": str(source_path),
                "status": "EXISTS_NEEDLES_CONFIRMED" if ok else "MISSING_OR_NEEDLE_FAIL",
                "needles": ";".join(needles),
                "note": note,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def pir_variation_rows() -> list[dict[str, object]]:
    data = [
        (
            "PVC2070_0_variation_variable",
            "R_AB",
            "delta R_AB is allowed in the auxiliary natural boundary variation class",
            "free natural variation, not fixed boundary data",
            "CONDITIONAL_FROM_2062",
            "needs parent action boundary class, but fixed-boundary shortcut is rejected",
        ),
        (
            "PVC2070_1_density_convention",
            "pi_R^cap",
            "delta B_cap = integral_Ccap pi_R^cap delta R_AB dSigma_C",
            "density-level convention",
            "CONVENTION_WRITTEN_NOT_PARENT_SIGNED",
            "declares how an integrated Pi_R row would be formed",
        ),
        (
            "PVC2070_2_integrated_convention",
            "Pi_R_time_caps",
            "Pi_R_time_caps_abs := integral_Ccap |pi_R^cap| dSigma_C",
            "integrated absolute cap component",
            "CONVENTION_WRITTEN_NOT_SOURCE_FILLED",
            "surface measure, cap class and orientation remain missing",
        ),
        (
            "PVC2070_3_same_parent_Bcap",
            "B_cap[R_AB,tau,T_H]",
            "B_cap must produce both pi_R^cap=delta B_cap/delta R_AB and N_tau_cap as the same cap leakage functional",
            "same-parent functional bridge",
            "MISSING_PARENT_BCAP_FUNCTIONAL",
            "without this, K_cap_to_PiR is only a source-row slot",
        ),
        (
            "PVC2070_4_orientation_measure",
            "C_cap orientation/measure",
            "declare normal direction, cap orientation, dSigma_C, and whether caps are temporal faces or regulator joins",
            "finite scoring convention",
            "MISSING_CAP_ORIENTATION_AND_MEASURE",
            "needed for units and no-cancellation absolute sum",
        ),
        (
            "PVC2070_5_Kcap_source_row",
            "K_cap_to_PiR",
            "K_cap_to_PiR := ||pi_R^cap||_L1(Ccap) / N_tau_cap for a sourced same-parent cap functional",
            "Pi_R boundary-current units per mass/energy unit",
            "SOURCE_ROW_SCHEMA_AVAILABLE_VALUES_MISSING",
            "source path/equation/value or theorem-zero still missing",
        ),
        (
            "PVC2070_6_qR_guard",
            "q_R cap contribution",
            "|Pi_R_time_caps|/(N_sphere Z_R_infty r_s) joins q_R only after all Pi_R components are absolute-summed",
            "dimensionless q_R guard",
            "MISSING_QR_NORMALIZATION_CHAIN",
            "prevents cap-only local-GR claim",
        ),
        (
            "PVC2070_7_verdict",
            "Pi_R variation convention",
            "the convention is now explicit enough for a future source row, but same-parent B_cap and K value remain unowned",
            "nonclaim verdict",
            "PIR_CONVENTION_WRITTEN_KCAP_STILL_UNSIGNED",
            "do not claim K_cap_to_PiR or local-GR pass",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, object_id, statement, role, status, note in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "object_id": object_id,
                "statement": statement,
                "role": role,
                "status": status,
                "note": note,
                "ready_for_scoring": False,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def mhref_lock_rows() -> list[dict[str, object]]:
    data = [
        (
            "MHL2070_0_definition",
            "M_H_ref",
            "M_H_ref := H_tau[S_link] - H_ref",
            "finite positive same-frame denominator",
            "DEFINITION_ONLY_NONCLAIM",
            "1006 already identifies this but does not sign it",
        ),
        (
            "MHL2070_1_Htau_integrability",
            "H_tau",
            "delta H_tau = integral_S(delta Q_tau - i_tau theta) must be integrable",
            "Hamiltonian charge lock",
            "MISSING_HTAU_INTEGRABILITY",
            "1007 blocks this on missing parent theta/Q_tau and boundary conditions",
        ),
        (
            "MHL2070_2_fixed_reference",
            "H_ref",
            "reference/counterterm convention fixed before source/orbit/clock readout",
            "anti-retuning guard",
            "MISSING_FIXED_REFERENCE_CERTIFICATE",
            "1008 protects M_H_ref from fitted counterterms",
        ),
        (
            "MHL2070_3_tau_coframe_lock",
            "tau_obs/e_obs",
            "same tau and coframe across source, clocks, boundary charge and orbital readout",
            "same-frame lock",
            "MISSING_TAU_COFRAME_LOCK",
            "needed before denominator can normalize epsilon_tau",
        ),
        (
            "MHL2070_4_positivity",
            "M_H_ref > 0",
            "positive source energy after reference subtraction with no boundary/extra-sector contamination",
            "positivity gate",
            "MISSING_POSITIVITY_CERTIFICATE",
            "negative/zero denominator rows are refused",
        ),
        (
            "MHL2070_5_anti_circularity",
            "no orbital GM import",
            "GM_orbit/G_ref cannot be used until Poisson/Gauss/orbital readout is derived from M_H_ref",
            "anti-circularity guard",
            "GUARDRAIL_PASS_NONCLAIM",
            "keeps denominator from being fitted to the answer",
        ),
        (
            "MHL2070_6_theta_Qtau_dependency",
            "parent theta_MTS and Q_tau^MTS",
            "H_tau lock requires parent MTS theta/Q_tau extraction or sector-by-sector charge decomposition",
            "upstream dependency",
            "MISSING_PARENT_THETA_QTAU_EXTRACTION",
            "1008/1009 are the upstream route",
        ),
        (
            "MHL2070_7_verdict",
            "M_H_ref denominator lock",
            "definition and guardrails are strong, but no positive same-frame denominator is claim-ready",
            "nonclaim verdict",
            "MHREF_LOCK_STILL_BLOCKED_BY_THETA_QTAU",
            "do not use M_ref_candidate numerically",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, object_id, statement, role, status, note in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "object_id": object_id,
                "statement": statement,
                "role": role,
                "status": status,
                "note": note,
                "ready_for_scoring": False,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def kcap_source_template_rows() -> list[dict[str, object]]:
    row = base_row()
    row.update(
        {
            "row_id": "KST2070_0_Kcap_live_template",
            "system_id": "R10_local_reference_branch",
            "R_AB_variation_variable": "MISSING_R_AB_VARIATION_VARIABLE",
            "PiR_density_or_integrated": "MISSING_PIR_DENSITY_OR_INTEGRATED_CONVENTION",
            "B_cap_functional": "MISSING_PARENT_BCAP_FUNCTIONAL",
            "C_cap_surface": "MISSING_CAP_SURFACE_CLASS",
            "orientation_measure": "MISSING_ORIENTATION_MEASURE",
            "N_tau_cap": "MISSING_N_TAU_CAP_SOURCE",
            "K_cap_to_PiR": "MISSING_K_CAP_TO_PIR_VALUE",
            "K_cap_units": "MISSING_K_CAP_UNITS",
            "source_reference_caps": "MISSING_SOURCE_REFERENCE_CAP_SEPARATION",
            "qR_normalization_source": "MISSING_QR_NORMALIZATION_SOURCE",
            "source_path": "MISSING_SOURCE_PATH",
            "equation_ref": "MISSING_EQUATION_REF",
            "status": "SOURCE_ROW_TEMPLATE_ONLY",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    return [row]


def dry_run_rows(pir_rows: list[dict[str, object]], mhref_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    pir_verdict = next(row for row in pir_rows if row["row_id"] == "PVC2070_7_verdict")
    mhref_verdict = next(row for row in mhref_rows if row["row_id"] == "MHL2070_7_verdict")
    rows_data = [
        (
            "RUN2070_0_PiR_convention",
            "Pi_R variation convention",
            "CONVENTION_WRITTEN_NOT_SOURCE_OWNED",
            str(pir_verdict["status"]),
            False,
        ),
        (
            "RUN2070_1_Kcap_source_row",
            "K_cap_to_PiR source row",
            "SCHEMA_WRITTEN_VALUES_MISSING",
            "B_cap, measure, source path and K value missing",
            False,
        ),
        (
            "RUN2070_2_MHref_lock",
            "M_H_ref denominator lock",
            "REFUSED_MHREF_UNSIGNED",
            str(mhref_verdict["status"]),
            False,
        ),
        (
            "RUN2070_VERDICT",
            "PiR convention or MHref denominator lock",
            "PIR_CONVENTION_AND_MHREF_CONTRACTS_WRITTEN_BOTH_UNSCORED",
            "2071 should attempt B_cap same-parent functional or parent theta/Q_tau denominator route",
            False,
        ),
    ]
    rows: list[dict[str, object]] = []
    for run_id, target, verdict, reason, accepted in rows_data:
        row = base_row()
        row.update(
            {
                "run_id": run_id,
                "target": target,
                "verdict": verdict,
                "reason": reason,
                "accepted_for_scoring": accepted,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def claim_gate_rows() -> list[dict[str, object]]:
    data = [
        (
            "GATE2070_0_PiR_convention",
            "Pi_R variation convention can score",
            "FAIL_BLOCKED",
            "density/integrated convention is written but not parent-owned by B_cap",
        ),
        (
            "GATE2070_1_Kcap",
            "K_cap_to_PiR value/theorem-zero",
            "FAIL_BLOCKED",
            "same-parent cap functional, cap measure, K value and source path missing",
        ),
        (
            "GATE2070_2_MHref",
            "M_H_ref positive same-frame denominator",
            "FAIL_BLOCKED",
            "H_tau integrability, fixed reference, tau/coframe lock and positivity missing",
        ),
        (
            "GATE2070_3_no_orbital_import",
            "orbital GM denominator shortcut",
            "PASS_GUARDRAIL",
            "orbital GM import is explicitly rejected",
        ),
        (
            "GATE2070_4_qR",
            "q_R/local PPN scoring",
            "FAIL_BLOCKED",
            "Pi_R total join and q_R normalization chain remain incomplete",
        ),
        (
            "GATE2070_5_local_GR",
            "local GR/Newton claim",
            "FAIL_BLOCKED",
            "neither Kcap nor MHref route is scoreable",
        ),
        (
            "GATE2070_6_formalization",
            "formalization-workbench edit allowed",
            "PASS_NO_EDIT",
            "no formalization-workbench edit is made",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, gate, status, detail in data:
        row = base_row()
        row.update({"row_id": row_id, "gate": gate, "status": status, "detail": detail, "claim_allowed": False})
        rows.append(row)
    return rows


def decision_rows() -> list[dict[str, object]]:
    data = [
        (
            "DEC2070_0_PiR_progress",
            "PIR_VARIATION_CONVENTION_IS_NOW_EXPLICIT",
            "We now have a density/integrated cap convention suitable for future source rows.",
        ),
        (
            "DEC2070_1_PiR_block",
            "BCAP_PARENT_FUNCTIONAL_IS_THE_REAL_KCAP_BLOCKER",
            "Kcap cannot score until B_cap produces both Pi_R_time_caps and N_tau_cap.",
        ),
        (
            "DEC2070_2_MHref_status",
            "MHREF_DENOMINATOR_REMAINS_UPSTREAM_THETA_QTAU_BLOCKED",
            "The denominator route runs through parent theta/Q_tau extraction and fixed reference.",
        ),
        (
            "DEC2070_3_best_next",
            "TRY_BCAP_FIRST_THEN_THETA_QTAU",
            "B_cap is narrower and directly unlocks Kcap; if it fails, the denominator route goes back to theta/Q_tau.",
        ),
        (
            "DEC2070_4_next",
            "TARGET_BCAP_SAME_PARENT_FUNCTIONAL_OR_THETA_QTAU_ROUTE",
            "2071 should attempt the same-parent cap functional; otherwise route to parent theta/Q_tau extraction for M_H_ref.",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, decision, rationale in data:
        row = base_row()
        row.update({"row_id": row_id, "decision": decision, "rationale": rationale, "claim_allowed": False})
        rows.append(row)
    return rows


def next_target_rows() -> list[dict[str, object]]:
    row = base_row()
    row.update(
        {
            "target_id": "NEXT2070_0_2071",
            "target_doc": "2071-Y5-R2FR-Bcap-same-parent-functional-or-theta-Qtau-denominator-route.md",
            "objective": "derive the same-parent cap functional B_cap that owns both Pi_R_time_caps and N_tau_cap for K_cap_to_PiR, or route the denominator branch through parent theta/Q_tau extraction for M_H_ref",
            "must_include": "B_cap[R_AB,tau,T_H]; delta B_cap/delta R_AB; N_tau_cap from same functional; Kcap units/value/theorem-zero; source/reference cap separation; theta_MTS/Q_tau_MTS dependency; fixed reference; q_R normalization guard",
            "excluded": "K=1 by convention; fixed R_AB boundary shortcut; fitted H_ref; orbital GM import; cancellation; local-GR/PPN scoring; GitHub; formalization-workbench edits",
            "claim_allowed": False,
        }
    )
    return [row]


def write_branch_copies(
    pir_rows: list[dict[str, object]],
    mhref_rows: list[dict[str, object]],
    template_rows: list[dict[str, object]],
    dry_rows_: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
) -> list[dict[str, object]]:
    copies = [
        (
            "COPY2070_0_source_weight_PiR",
            SOURCE_WEIGHT_DOCS / "AFRAME_PIR_VARIATION_CONVENTION_2070_NONCLAIM.csv",
            pir_rows,
        ),
        (
            "COPY2070_1_source_weight_MHref",
            SOURCE_WEIGHT_DOCS / "AFRAME_MHREF_DENOMINATOR_LOCK_2070_NONCLAIM.csv",
            mhref_rows,
        ),
        (
            "COPY2070_2_source_template_Kcap",
            SOURCE_WEIGHT_DOCS / "AFRAME_KCAP_SOURCE_TEMPLATE_2070_NONCLAIM.csv",
            template_rows,
        ),
        (
            "COPY2070_3_wep_dry_run",
            BRANCH_WEP / "P8_Y5_PARENT_QLOC_2070_PIR_MHREF_DRY_RUN_NONCLAIM.csv",
            dry_rows_,
        ),
        (
            "COPY2070_4_queue_next",
            QUEUE / "JR2070_BCAP_OR_THETA_QTAU_NEXT_NONCLAIM.csv",
            next_rows_,
        ),
    ]
    rows: list[dict[str, object]] = []
    for copy_id, path, data in copies:
        write_csv(path, data)
        row = base_row()
        row.update({"copy_id": copy_id, "path": str(path), "rows": len(data), "status": "WRITTEN_NONCLAIM_COPY", "claim_allowed": False})
        rows.append(row)
    return rows


def validation_rows(
    sources: list[dict[str, object]],
    pir_rows: list[dict[str, object]],
    mhref_rows: list[dict[str, object]],
    template_rows: list[dict[str, object]],
    dry_rows_: list[dict[str, object]],
    gates: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    source_ok = all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in sources)
    csv_ok = all(csv_rows_parse(path) for path in csv_paths)
    pir_verdict = next(row for row in pir_rows if row["row_id"] == "PVC2070_7_verdict")
    pir_ok = (
        any(row["row_id"] == "PVC2070_1_density_convention" for row in pir_rows)
        and any(row["row_id"] == "PVC2070_3_same_parent_Bcap" and row["status"] == "MISSING_PARENT_BCAP_FUNCTIONAL" for row in pir_rows)
        and pir_verdict["status"] == "PIR_CONVENTION_WRITTEN_KCAP_STILL_UNSIGNED"
        and all(not bool(row["ready_for_scoring"]) for row in pir_rows)
    )
    mhref_verdict = next(row for row in mhref_rows if row["row_id"] == "MHL2070_7_verdict")
    mhref_ok = (
        any(row["row_id"] == "MHL2070_0_definition" for row in mhref_rows)
        and any(row["row_id"] == "MHL2070_6_theta_Qtau_dependency" for row in mhref_rows)
        and mhref_verdict["status"] == "MHREF_LOCK_STILL_BLOCKED_BY_THETA_QTAU"
        and all(not bool(row["ready_for_scoring"]) for row in mhref_rows)
    )
    template_ok = len(template_rows) == 1 and template_rows[0]["status"] == "SOURCE_ROW_TEMPLATE_ONLY" and template_rows[0]["valid_for_claim"] is False
    dry_verdict = next(row for row in dry_rows_ if row["run_id"] == "RUN2070_VERDICT")
    dry_ok = dry_verdict["verdict"] == "PIR_CONVENTION_AND_MHREF_CONTRACTS_WRITTEN_BOTH_UNSCORED"
    gates_ok = all(row["claim_allowed"] is False for row in gates) and all(row["status"] != "PASS_CLAIM" for row in gates)
    next_ok = next_rows_[0]["target_id"] == "NEXT2070_0_2071"
    no_claim = all(
        not bool(row.get("claim_allowed", False)) and not bool(row.get("valid_for_claim", False))
        for group in [sources, pir_rows, mhref_rows, template_rows, dry_rows_, gates, next_rows_]
        for row in group
    )
    checks: list[tuple[str, bool, str]] = []
    checks.append(("VAL2070_00_local_sources_exist", source_ok, "all cited source paths and needles exist"))
    checks.append(("VAL2070_01_csv_parse", csv_ok, "all generated CSV files parse cleanly"))
    checks.append(("VAL2070_02_PiR_convention", pir_ok, "Pi_R convention is written and Kcap remains blocked on B_cap"))
    checks.append(("VAL2070_03_MHref_lock", mhref_ok, "M_H_ref lock contract is written and blocked on theta/Q_tau"))
    checks.append(("VAL2070_04_Kcap_template", template_ok, "Kcap source row template is nonclaim and placeholder-marked"))
    checks.append(("VAL2070_05_dry_verdict", dry_ok, "dry run refuses both physical scoring routes"))
    checks.append(("VAL2070_06_claim_gates_blocked", gates_ok, "all claim gates remain blocked/nonclaim"))
    checks.append(("VAL2070_07_next_selected", next_ok, "2071 Bcap or theta/Qtau target selected"))
    checks.append(("VAL2070_08_no_claim_flags", no_claim, "no generated row allows a claim"))
    checks.append(("VAL2070_09_formalization_unchanged", count_formalization_modified() == 0, "formalization-workbench modified-file count remains 0"))
    checks.append(("VAL2070_10_no_formalization_artifacts", not formalization_has_2070_artifacts(), "no 2070 artifacts were written under formalization-workbench"))
    checks.append(("VAL2070_11_no_pycache", not scripts_pycache_exists(), "scripts __pycache__ removed"))
    overall = all(ok for _, ok, _ in checks)
    checks.append(("VAL2070_OVERALL", overall, "2070 writes PiR and MHref contracts without promoting local claims"))
    rows: list[dict[str, object]] = []
    for check_id, ok, detail in checks:
        row = base_row()
        row.update({"check_id": check_id, "status": "PASS" if ok else "FAIL", "detail": detail, "claim_allowed": False})
        rows.append(row)
    return rows


def write_doc(
    sources: list[dict[str, object]],
    pir_rows: list[dict[str, object]],
    mhref_rows: list[dict[str, object]],
    template_rows: list[dict[str, object]],
    dry_rows_: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    sections = [
        "# 2070 Y5 R2FR PiR Variation Convention Kcap Source Row Or MHref Denominator Lock",
        "",
        "## Current Verdict",
        "",
        "2070 makes useful formal progress but still no physical local-GR score. The `Pi_R` cap convention is now explicit: write `delta B_cap = integral_Ccap pi_R^cap delta R_AB dSigma_C`, then `Pi_R_time_caps_abs = integral_Ccap |pi_R^cap| dSigma_C`. This is the right shape for a future source row.",
        "",
        "The missing object is the same-parent cap functional `B_cap[R_AB,tau,T_H]`. It must generate both `pi_R^cap=delta B_cap/delta R_AB` and the cap-current leakage `N_tau_cap`; without that, `K_cap_to_PiR` remains a source-row slot, not a value or theorem-zero.",
        "",
        "The denominator route is also structurally clear but blocked: `M_H_ref = H_tau[S_link] - H_ref` needs integrable `H_tau`, fixed `H_ref`, tau/coframe lock, positivity, no orbital-GM import, and parent `theta_MTS/Q_tau^MTS`. Current evidence keeps those unsigned.",
        "",
        "No local-GR/Newton, Cassini, PPN, R10, clock, orbital, corner-zero, or finite-residual claim is allowed. No GitHub action and no `formalization-workbench` edit is made.",
        "",
        "## Source Register",
        md_table(sources, ["source_id", "source_kind", "source_path", "status", "note", "valid_for_claim"]),
        "## PiR Variation Convention",
        md_table(pir_rows, ["row_id", "object_id", "statement", "role", "status", "note", "ready_for_scoring", "claim_allowed"]),
        "## MHref Denominator Lock",
        md_table(mhref_rows, ["row_id", "object_id", "statement", "role", "status", "note", "ready_for_scoring", "claim_allowed"]),
        "## Kcap Source Template",
        md_table(template_rows, ["row_id", "system_id", "R_AB_variation_variable", "B_cap_functional", "K_cap_to_PiR", "MISSING_K_CAP_UNITS", "source_path", "status", "valid_for_claim"]),
        "## Dry Run",
        md_table(dry_rows_, ["run_id", "target", "verdict", "reason", "accepted_for_scoring", "claim_allowed"]),
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
    pir_rows = pir_variation_rows()
    mhref_rows = mhref_lock_rows()
    template_rows = kcap_source_template_rows()
    dry_rows_ = dry_run_rows(pir_rows, mhref_rows)
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows_ = next_target_rows()
    paths = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2070_SOURCE_REGISTER.csv",
        "pir": OUT / "P8_Y5_PARENT_QLOC_2070_PIR_VARIATION_CONVENTION.csv",
        "mhref": OUT / "P8_Y5_PARENT_QLOC_2070_MHREF_DENOMINATOR_LOCK.csv",
        "template": OUT / "P8_Y5_PARENT_QLOC_2070_KCAP_SOURCE_TEMPLATE.csv",
        "dry": OUT / "P8_Y5_PARENT_QLOC_2070_DRY_RUN.csv",
        "gates": OUT / "P8_Y5_PARENT_QLOC_2070_CLAIM_GATE.csv",
        "decision": OUT / "P8_Y5_PARENT_QLOC_2070_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2070_NEXT_TARGET.csv",
        "branch": OUT / "P8_Y5_PARENT_QLOC_2070_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2070_VALIDATION.csv",
    }
    write_csv(paths["sources"], sources)
    write_csv(paths["pir"], pir_rows)
    write_csv(paths["mhref"], mhref_rows)
    write_csv(paths["template"], template_rows)
    write_csv(paths["dry"], dry_rows_)
    write_csv(paths["gates"], gates)
    write_csv(paths["decision"], decisions)
    write_csv(paths["next"], next_rows_)
    copies = write_branch_copies(pir_rows, mhref_rows, template_rows, dry_rows_, next_rows_)
    write_csv(paths["branch"], copies)
    remove_pycache()
    csv_paths_without_validation = [path for key, path in paths.items() if key != "validation"] + [Path(row["path"]) for row in copies]
    validation = validation_rows(sources, pir_rows, mhref_rows, template_rows, dry_rows_, gates, next_rows_, csv_paths_without_validation)
    write_csv(paths["validation"], validation)
    csv_paths = list(paths.values()) + [Path(row["path"]) for row in copies]
    remove_pycache()
    validation = validation_rows(sources, pir_rows, mhref_rows, template_rows, dry_rows_, gates, next_rows_, csv_paths)
    write_csv(paths["validation"], validation)
    write_doc(sources, pir_rows, mhref_rows, template_rows, dry_rows_, gates, decisions, next_rows_, copies, validation)
    remove_pycache()


if __name__ == "__main__":
    main()
