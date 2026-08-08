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


DOC = ROOT / "2069-Y5-R2FR-Kcap-to-PiR-conversion-or-Mref-theta-component-first-row.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()


def formalization_has_2069_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    try:
        patterns = (
            "*2069-Y5-R2FR*",
            "*P8_Y5_PARENT_QLOC_2069*",
            "*Y5_R2FR_Kcap_to_PiR_conversion_or_Mref_theta_component_first_row_2069*",
        )
        return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))
    except Exception:
        return False


def scripts_pycache_exists() -> bool:
    return (SCRIPT_PATH.parent / "__pycache__").exists()


def source_register_rows() -> list[dict[str, object]]:
    specs = [
        (
            "SRC2069_00_2068_doc",
            ROOT / "2068-Y5-R2FR-time-cap-current-normalization-Ccap-or-epsilon-tau-component-pack.md",
            ["NEXT2068_0_2069", "K_cap_to_PiR", "ECP2068_1_theta_first_row"],
            "2068 handoff into K_cap_to_PiR conversion or M_ref/theta first row.",
        ),
        (
            "SRC2069_01_2068_next",
            OUT / "P8_Y5_PARENT_QLOC_2068_NEXT_TARGET.csv",
            ["NEXT2068_0_2069", "Pi_R variation convention", "theta/X_D source row"],
            "machine-readable 2069 target.",
        ),
        (
            "SRC2069_02_2068_norm",
            OUT / "P8_Y5_PARENT_QLOC_2068_CAP_NORMALIZATION_ATTEMPT.csv",
            ["TCN2068_4_physical_PiR_map", "MISSING_K_CAP_TO_PIR_MAP", "PARTIAL_NORMAL_FORM_NOT_PHYSICAL_SCORE"],
            "normalization split and physical Pi_R map blocker.",
        ),
        (
            "SRC2069_03_2068_components",
            OUT / "P8_Y5_PARENT_QLOC_2068_EPSILON_TAU_COMPONENT_PACK.csv",
            ["ECP2068_1_theta_first_row", "ECP2068_8_denominator", "MISSING_CLAIM_READY_M_REF_CANDIDATE"],
            "epsilon_tau component pack requiring theta and denominator rows.",
        ),
        (
            "SRC2069_04_2068_join",
            OUT / "P8_Y5_PARENT_QLOC_2068_PHYSICAL_PIR_JOIN.csv",
            ["PJR2068_1_physical_cap_component", "MISSING_K_CAP_TO_PIR_AND_CAP_SEPARATION", "PJR2068_4_qR_guard"],
            "physical Pi_R/q_R join guard.",
        ),
        (
            "SRC2069_05_PiR_source",
            ROOT / "06-reciprocal-charge-source-neutrality.md",
            ["delta S_boundary = [W R_AB' + Pi_R]", "Q_R = -Pi_R", "Pi_R = source reciprocal momentum/charge"],
            "legacy Pi_R boundary-variation definition.",
        ),
        (
            "SRC2069_06_1006_MHref_doc",
            ROOT / "1006-Y5-R10-MHref-positive-same-frame-denominator-or-Htau-source-row.md",
            ["DEC1006_0_denominator_not_claimed", "M_H_ref", "positive same-frame"],
            "M_H_ref denominator checkpoint and nonclaim verdict.",
        ),
        (
            "SRC2069_07_1006_denominator_template",
            OUT / "P8_Y5_R10_1006_CANDIDATE_DENOMINATOR_TEMPLATE.csv",
            ["MHC1006_0_missing_Htau", "MHC1006_3_orbital_GM_substitution", "MHC1006_6_live_placeholder"],
            "candidate denominator template and refusal rows.",
        ),
        (
            "SRC2069_08_1006_audit",
            OUT / "P8_Y5_R10_1006_MHREF_DENOMINATOR_THEOREM_AUDIT.csv",
            ["MHA1006_0_definition", "MHA1006_5_anti_circularity", "MHA1006_6_theorem_verdict"],
            "M_H_ref theorem audit.",
        ),
        (
            "SRC2069_09_603_primitive",
            OUT / "P8_Y5_R10_603_ND_PRIMITIVE_DERIVATION_ATTEMPT.csv",
            ["NDP603_3_coherent_trace_factor", "X_D", "not parent-owned"],
            "theta/X_D primitive and its parent-ownership blocker.",
        ),
        (
            "SRC2069_10_688_template",
            OUT / "P8_Y5_R10_688_COMPONENT_BOUND_INPUT_TEMPLATE.csv",
            ["CSI688_0_theta", "CSI688_6_stress_envelope", "CSI688_7_denominator"],
            "source-input requirements for theta, stress envelope and denominator.",
        ),
        (
            "SRC2069_11_2064_corner_bound",
            OUT / "P8_Y5_PARENT_QLOC_2064_FINITE_PIR_CORNER_BOUND_SCHEMA.csv",
            ["PCB2064_3_component_abs_sum", "PCB2064_4_join_PiRtot", "PCB2064_5_qR_guard"],
            "absolute Pi_R corner/total/q_R guardrail.",
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


def kcap_conversion_rows() -> list[dict[str, object]]:
    data = [
        (
            "KPC2069_0_PiR_boundary_definition",
            "Pi_R",
            "delta S_boundary = [W R_AB' + Pi_R] delta R_AB|_surface",
            "Pi_R is a boundary-variation coefficient/source reciprocal momentum",
            "DEFINITION_SOURCE_EXISTS",
            "defines the object but not the time-cap conversion units",
            False,
        ),
        (
            "KPC2069_1_cap_current_numerator",
            "N_tau_cap",
            "N_tau_cap = abs(int_slab T_H^{mu nu} nabla_(mu tau_nu) dV_tau)",
            "stress-current leakage in same-frame mass/energy units",
            "DEFINED_SYMBOLIC_NONCLAIM",
            "not automatically a Pi_R variation coefficient",
            False,
        ),
        (
            "KPC2069_2_same_functional_requirement",
            "B_cap[R_AB,tau,T_H]",
            "Pi_R_time_caps = delta B_cap/delta R_AB and N_tau_cap = norm(B_cap leakage) must be derived from the same parent cap functional",
            "same-functional bridge",
            "MISSING_PARENT_CAP_FUNCTIONAL_BRIDGE",
            "this is the core reason K_cap_to_PiR cannot be set to one",
            False,
        ),
        (
            "KPC2069_3_operator_norm_definition",
            "K_cap_to_PiR",
            "K_cap_to_PiR := ||delta Pi_R_time_caps / delta N_tau_cap||_(cap norm -> Pi_R norm)",
            "Pi_R boundary-current units per mass/energy unit",
            "SOURCE_ROW_DEFINITION_AVAILABLE",
            "definition is useful; value/source/equation are missing",
            False,
        ),
        (
            "KPC2069_4_variation_convention",
            "Pi_R norm convention",
            "declare the R_AB variation variable, cap surface orientation, density/measure, and whether Pi_R is integrated or density-level",
            "required convention",
            "MISSING_PIR_VARIATION_CONVENTION",
            "without this, K_cap_to_PiR has ambiguous units",
            False,
        ),
        (
            "KPC2069_5_reject_fake_unity",
            "K_cap_to_PiR=1 shortcut",
            "K=1 is valid only if Pi_R units are defined to be the same cap-energy functional and the q_R normalization chain is separately proved",
            "guardrail",
            "REJECTED_UNITY_BY_CONVENTION_AS_PHYSICAL_SCORE",
            "prevents winning by changing units",
            False,
        ),
        (
            "KPC2069_6_source_reference_caps",
            "B_source_caps_abs + B_ref_caps_abs",
            "source endpoint and reference cap terms must be zeroed or bounded separately from K_cap_to_PiR N_tau_cap",
            "boundary-current units",
            "MISSING_SOURCE_REFERENCE_CAP_SEPARATION",
            "cap leakage cannot hide endpoint/reference terms",
            False,
        ),
        (
            "KPC2069_7_verdict",
            "physical K_cap_to_PiR map",
            "K_cap_to_PiR is now a precise source row, but no value/theorem-zero is claim-ready",
            "nonclaim",
            "FAIL_CURRENT_CLAIM_KCAP_TO_PIR_UNSIGNED",
            "next route needs Pi_R variation convention owner or source row",
            False,
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, quantity, formula, units_or_role, status, note, ready in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "quantity": quantity,
                "formula": formula,
                "units_or_role": units_or_role,
                "status": status,
                "note": note,
                "ready_for_scoring": ready,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def mref_theta_rows() -> list[dict[str, object]]:
    data = [
        (
            "MTR2069_0_MHref_candidate",
            "M_ref_candidate",
            "M_ref_candidate := M_H_ref = H_tau[S_link] - H_ref",
            "mass/energy units",
            "positive same-frame denominator",
            "MISSING_H_TAU_H_REF_INTEGRABILITY_AND_POSITIVITY",
            "1006 keeps this definition-only and nonclaim",
            False,
        ),
        (
            "MTR2069_1_no_orbital_import",
            "anti-circularity guard",
            "GM_orbit/G_ref cannot fill M_ref_candidate until M_H_ref -> Poisson/Gauss -> orbital readout is derived",
            "boolean guard",
            "guardrail",
            "ORBITAL_GM_SUBSTITUTION_REJECTED",
            "prevents fitted denominator from replacing derivation",
            False,
        ),
        (
            "MTR2069_2_theta_XD_candidate",
            "theta_D_or_X_D",
            "X_D := (1/3)<Tr_h Q>_D or coherent trace/volume-flow scalar in a fixed-D branch",
            "1/time or normalized dimensionless",
            "first theta source component",
            "MISSING_PARENT_OWNED_Q_D_PCOH_AND_LOCAL_XD_ZERO_SOURCE",
            "603 gives a conditional primitive, not a parent theorem",
            False,
        ),
        (
            "MTR2069_3_stress_weight",
            "S_theta",
            "same-frame stress weight contracted with the trace piece of symgrad_tau",
            "mass/energy units or declared density-integral units",
            "stress envelope for epsilon_theta",
            "MISSING_SAME_FRAME_STRESS_WEIGHT",
            "needed before epsilon_theta can be numeric",
            False,
        ),
        (
            "MTR2069_4_coefficient",
            "C_theta",
            "norm coefficient mapping theta_D_or_X_D convention into the symgrad_tau contraction",
            "dimensionless or declared",
            "component norm coefficient",
            "MISSING_C_THETA_NORM_COEFFICIENT",
            "depends on averaging/projection convention",
            False,
        ),
        (
            "MTR2069_5_first_row_formula",
            "epsilon_theta",
            "epsilon_theta <= C_theta * S_theta * |theta_D_or_X_D| / M_ref_candidate",
            "dimensionless",
            "first epsilon_tau component row",
            "MISSING_NUMERIC_OR_THEOREM_ZERO_INPUTS",
            "source-ready formula only",
            False,
        ),
        (
            "MTR2069_6_acceptance",
            "theta row acceptance",
            "valid_for_claim=true only if M_ref_candidate, theta/X_D, S_theta, C_theta, units, source paths, and assumptions are all real with no MISSING markers",
            "boolean gate",
            "acceptance rule",
            "SCHEMA_ONLY_NONCLAIM",
            "keeps theta row useful but private",
            False,
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, quantity, formula, units, role, blocker, note, ready in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "quantity": quantity,
                "formula": formula,
                "units": units,
                "role": role,
                "blocker": blocker,
                "note": note,
                "source_ready_schema": True,
                "ready_for_scoring": ready,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def source_row_template_rows() -> list[dict[str, object]]:
    columns = [
        "row_id",
        "system_id",
        "K_cap_to_PiR",
        "K_cap_units",
        "Pi_R_variation_convention",
        "N_tau_cap_source",
        "M_ref_candidate",
        "M_ref_units",
        "theta_D_or_X_D",
        "theta_units",
        "S_theta",
        "C_theta",
        "B_source_caps_abs",
        "B_ref_caps_abs",
        "qR_normalization_source",
        "source_path",
        "equation_ref",
        "valid_for_claim",
    ]
    row = base_row()
    row.update({column: f"MISSING_{column.upper()}" for column in columns if column not in {"row_id", "valid_for_claim"}})
    row.update(
        {
            "row_id": "SRT2069_0_live_source_row_template",
            "valid_for_claim": False,
            "claim_allowed": False,
            "status": "SOURCE_ROW_TEMPLATE_ONLY",
            "required_no_missing": ";".join(columns),
        }
    )
    return [row]


def dry_run_rows(kcap_rows: list[dict[str, object]], theta_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    kcap_verdict = next(row for row in kcap_rows if row["row_id"] == "KPC2069_7_verdict")
    theta_verdict = next(row for row in theta_rows if row["row_id"] == "MTR2069_6_acceptance")
    rows_data = [
        (
            "RUN2069_0_Kcap_derivation",
            "K_cap_to_PiR physical conversion",
            "REFUSED_KCAP_UNSIGNED",
            str(kcap_verdict["status"]),
            False,
        ),
        (
            "RUN2069_1_fake_unity",
            "K_cap_to_PiR=1 shortcut",
            "REFUSED_UNIT_CONVENTION_SHORTCUT",
            "C_cap_norm=1 is not physical Pi_R scoring",
            False,
        ),
        (
            "RUN2069_2_Mref_theta",
            "M_ref_candidate plus theta/X_D first row",
            "SCHEMA_WRITTEN_VALUES_MISSING",
            str(theta_verdict["blocker"]),
            False,
        ),
        (
            "RUN2069_VERDICT",
            "Kcap conversion or Mref/theta first row",
            "KCAP_AND_THETA_ROWS_STAGED_PHYSICAL_SCORE_BLOCKED",
            "2070 should prove Pi_R variation convention/Kcap source row or lock M_H_ref denominator",
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
            "GATE2069_0_Kcap",
            "K_cap_to_PiR physical map",
            "FAIL_BLOCKED",
            "same parent cap functional, Pi_R variation convention, units and source path are missing",
        ),
        (
            "GATE2069_1_K_equals_one",
            "K_cap_to_PiR=1 by convention",
            "FAIL_REJECTED",
            "valid only for normalized diagnostic, not physical Pi_R/q_R scoring",
        ),
        (
            "GATE2069_2_Mref",
            "M_ref_candidate claim-ready",
            "FAIL_BLOCKED",
            "H_tau/H_ref integrability, fixed reference, positivity and anti-circularity gates are not closed",
        ),
        (
            "GATE2069_3_theta",
            "theta/X_D first component claim-ready",
            "FAIL_BLOCKED",
            "theta/X_D parent ownership, stress weight, C_theta and denominator are missing",
        ),
        (
            "GATE2069_4_source_reference_caps",
            "source/reference cap separation",
            "FAIL_BLOCKED",
            "B_source_caps_abs and B_ref_caps_abs are not zeroed or bounded",
        ),
        (
            "GATE2069_5_qR",
            "q_R/local PPN scoring",
            "FAIL_BLOCKED",
            "Pi_R total join and q_R normalization remain incomplete",
        ),
        (
            "GATE2069_6_formalization",
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
            "DEC2069_0_Kcap_defined_not_filled",
            "KCAP_IS_NOW_A_PRECISE_OPERATOR_NORM_ROW",
            "K_cap_to_PiR is no longer vague, but it needs a parent cap functional or source-backed value.",
        ),
        (
            "DEC2069_1_no_unity_shortcut",
            "K_EQUALS_ONE_IS_REJECTED_FOR_PHYSICAL_SCORING",
            "C_cap_norm=1 belongs to epsilon_cap_norm only; Pi_R boundary-current units still need a map.",
        ),
        (
            "DEC2069_2_Mref_theta_staged",
            "MREF_THETA_FIRST_ROW_IS_READY_BUT_UNFILLED",
            "The formula is now explicit, but M_H_ref and theta/X_D ownership remain upstream blockers.",
        ),
        (
            "DEC2069_3_best_next",
            "PIR_VARIATION_CONVENTION_OR_MHREF_LOCK",
            "Those two objects unblock the most downstream rows at once.",
        ),
        (
            "DEC2069_4_next",
            "TARGET_PIR_VARIATION_CONVENTION_OR_MHREF_DENOMINATOR_LOCK",
            "2070 should either own the Pi_R variation/cap functional map or return to H_tau/H_ref denominator lock.",
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
            "target_id": "NEXT2069_0_2070",
            "target_doc": "2070-Y5-R2FR-PiR-variation-convention-Kcap-source-row-or-MHref-denominator-lock.md",
            "objective": "derive the Pi_R variation convention and same-parent cap functional that gives K_cap_to_PiR, or lock the positive same-frame M_H_ref denominator needed by epsilon_tau/theta rows",
            "must_include": "R_AB variation variable; Pi_R density/integrated convention; cap functional B_cap; K_cap_to_PiR units/source row; source/reference cap separation; H_tau-H_ref denominator gate; no orbital-GM import; q_R normalization guard",
            "excluded": "K=1 by unit convention; fitted denominator; orbital GM import; cancellation; local-GR/PPN scoring; GitHub; formalization-workbench edits",
            "claim_allowed": False,
        }
    )
    return [row]


def write_branch_copies(
    kcap_rows: list[dict[str, object]],
    theta_rows: list[dict[str, object]],
    source_template: list[dict[str, object]],
    dry_rows_: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
) -> list[dict[str, object]]:
    copies = [
        (
            "COPY2069_0_source_weight_Kcap",
            SOURCE_WEIGHT_DOCS / "AFRAME_KCAP_TO_PIR_2069_SOURCE_ROW_SCHEMA_NONCLAIM.csv",
            kcap_rows,
        ),
        (
            "COPY2069_1_source_weight_Mref_theta",
            SOURCE_WEIGHT_DOCS / "AFRAME_MREF_THETA_COMPONENT_2069_SOURCE_ROW_SCHEMA_NONCLAIM.csv",
            theta_rows,
        ),
        (
            "COPY2069_2_source_template",
            SOURCE_WEIGHT_DOCS / "AFRAME_KCAP_MREF_THETA_LIVE_TEMPLATE_2069_NONCLAIM.csv",
            source_template,
        ),
        (
            "COPY2069_3_wep_dry_run",
            BRANCH_WEP / "P8_Y5_PARENT_QLOC_2069_KCAP_THETA_DRY_RUN_NONCLAIM.csv",
            dry_rows_,
        ),
        (
            "COPY2069_4_queue_next",
            QUEUE / "JR2069_PIR_VARIATION_OR_MHREF_LOCK_NEXT_NONCLAIM.csv",
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
    kcap_rows: list[dict[str, object]],
    theta_rows: list[dict[str, object]],
    source_template: list[dict[str, object]],
    dry_rows_: list[dict[str, object]],
    gates: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    source_ok = all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in sources)
    csv_ok = all(csv_rows_parse(path) for path in csv_paths)
    kcap_verdict = next(row for row in kcap_rows if row["row_id"] == "KPC2069_7_verdict")
    kcap_ok = (
        any(row["row_id"] == "KPC2069_3_operator_norm_definition" and row["status"] == "SOURCE_ROW_DEFINITION_AVAILABLE" for row in kcap_rows)
        and any(row["row_id"] == "KPC2069_5_reject_fake_unity" and row["status"] == "REJECTED_UNITY_BY_CONVENTION_AS_PHYSICAL_SCORE" for row in kcap_rows)
        and kcap_verdict["status"] == "FAIL_CURRENT_CLAIM_KCAP_TO_PIR_UNSIGNED"
        and all(not bool(row["ready_for_scoring"]) for row in kcap_rows)
    )
    theta_ok = (
        any(row["row_id"] == "MTR2069_0_MHref_candidate" for row in theta_rows)
        and any(row["row_id"] == "MTR2069_5_first_row_formula" for row in theta_rows)
        and all(bool(row["source_ready_schema"]) and not bool(row["ready_for_scoring"]) for row in theta_rows)
    )
    template_ok = len(source_template) == 1 and source_template[0]["status"] == "SOURCE_ROW_TEMPLATE_ONLY" and source_template[0]["valid_for_claim"] is False
    dry_verdict = next(row for row in dry_rows_ if row["run_id"] == "RUN2069_VERDICT")
    dry_ok = dry_verdict["verdict"] == "KCAP_AND_THETA_ROWS_STAGED_PHYSICAL_SCORE_BLOCKED"
    gates_ok = all(row["claim_allowed"] is False for row in gates) and all(row["status"] != "PASS_CLAIM" for row in gates)
    next_ok = next_rows_[0]["target_id"] == "NEXT2069_0_2070"
    no_claim = all(
        not bool(row.get("claim_allowed", False)) and not bool(row.get("valid_for_claim", False))
        for group in [sources, kcap_rows, theta_rows, source_template, dry_rows_, gates, next_rows_]
        for row in group
    )
    checks: list[tuple[str, bool, str]] = []
    checks.append(("VAL2069_00_local_sources_exist", source_ok, "all cited source paths and needles exist"))
    checks.append(("VAL2069_01_csv_parse", csv_ok, "all generated CSV files parse cleanly"))
    checks.append(("VAL2069_02_Kcap_gate", kcap_ok, "K_cap_to_PiR is defined as source row and fake unity is refused"))
    checks.append(("VAL2069_03_Mref_theta", theta_ok, "M_ref/theta first row is source-ready but unscored"))
    checks.append(("VAL2069_04_source_template", template_ok, "live source row template is nonclaim and placeholder-marked"))
    checks.append(("VAL2069_05_dry_verdict", dry_ok, "dry run stages rows and refuses physical score"))
    checks.append(("VAL2069_06_claim_gates_blocked", gates_ok, "all claim gates remain blocked/nonclaim"))
    checks.append(("VAL2069_07_next_selected", next_ok, "2070 Pi_R variation or M_H_ref lock target selected"))
    checks.append(("VAL2069_08_no_claim_flags", no_claim, "no generated row allows a claim"))
    checks.append(("VAL2069_09_formalization_unchanged", count_formalization_modified() == 0, "formalization-workbench modified-file count remains 0"))
    checks.append(("VAL2069_10_no_formalization_artifacts", not formalization_has_2069_artifacts(), "no 2069 artifacts were written under formalization-workbench"))
    checks.append(("VAL2069_11_no_pycache", not scripts_pycache_exists(), "scripts __pycache__ removed"))
    overall = all(ok for _, ok, _ in checks)
    checks.append(("VAL2069_OVERALL", overall, "2069 stages Kcap and Mref/theta rows without physical-score claims"))
    rows: list[dict[str, object]] = []
    for check_id, ok, detail in checks:
        row = base_row()
        row.update({"check_id": check_id, "status": "PASS" if ok else "FAIL", "detail": detail, "claim_allowed": False})
        rows.append(row)
    return rows


def write_doc(
    sources: list[dict[str, object]],
    kcap_rows: list[dict[str, object]],
    theta_rows: list[dict[str, object]],
    source_template: list[dict[str, object]],
    dry_rows_: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    sections = [
        "# 2069 Y5 R2FR Kcap To PiR Conversion Or Mref Theta Component First Row",
        "",
        "## Current Verdict",
        "",
        "2069 blocks the tempting but invalid shortcut. `Pi_R` is a boundary-variation coefficient from the `R_AB` surface variation, while `N_tau_cap` is a stress-current leakage numerator. Therefore `K_cap_to_PiR=1` is not allowed as a physical local-PPN score unless both objects are proved to be the same parent cap functional in the same units.",
        "",
        "`K_cap_to_PiR` is now a precise source row: the operator norm mapping cap-current leakage into `Pi_R` boundary-current units. The value remains missing because the `R_AB` variation convention, cap functional, density/integrated convention, source/reference cap separation, and q_R normalization chain are not parent-owned.",
        "",
        "The fallback denominator/theta row is also staged: `epsilon_theta <= C_theta * S_theta * |theta_D_or_X_D| / M_ref_candidate`. It cannot score because `M_H_ref`, parent-owned `theta_D/X_D`, `S_theta`, and `C_theta` are still missing or conditional.",
        "",
        "No local-GR/Newton, Cassini, PPN, R10, clock, orbital, corner-zero, or finite-residual claim is allowed. No GitHub action and no `formalization-workbench` edit is made.",
        "",
        "## Source Register",
        md_table(sources, ["source_id", "source_kind", "source_path", "status", "note", "valid_for_claim"]),
        "## Kcap To PiR Conversion Gate",
        md_table(kcap_rows, ["row_id", "quantity", "formula", "units_or_role", "status", "note", "ready_for_scoring", "claim_allowed"]),
        "## Mref Theta First Row",
        md_table(theta_rows, ["row_id", "quantity", "formula", "units", "role", "blocker", "note", "source_ready_schema", "ready_for_scoring", "claim_allowed"]),
        "## Live Source Row Template",
        md_table(source_template, ["row_id", "system_id", "K_cap_to_PiR", "M_ref_candidate", "theta_D_or_X_D", "S_theta", "C_theta", "source_path", "status", "valid_for_claim"]),
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
    kcap_rows = kcap_conversion_rows()
    theta_rows = mref_theta_rows()
    source_template = source_row_template_rows()
    dry_rows_ = dry_run_rows(kcap_rows, theta_rows)
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows_ = next_target_rows()
    paths = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2069_SOURCE_REGISTER.csv",
        "kcap": OUT / "P8_Y5_PARENT_QLOC_2069_KCAP_TO_PIR_CONVERSION_GATE.csv",
        "theta": OUT / "P8_Y5_PARENT_QLOC_2069_MREF_THETA_FIRST_ROW.csv",
        "template": OUT / "P8_Y5_PARENT_QLOC_2069_LIVE_SOURCE_ROW_TEMPLATE.csv",
        "dry": OUT / "P8_Y5_PARENT_QLOC_2069_DRY_RUN.csv",
        "gates": OUT / "P8_Y5_PARENT_QLOC_2069_CLAIM_GATE.csv",
        "decision": OUT / "P8_Y5_PARENT_QLOC_2069_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2069_NEXT_TARGET.csv",
        "branch": OUT / "P8_Y5_PARENT_QLOC_2069_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2069_VALIDATION.csv",
    }
    write_csv(paths["sources"], sources)
    write_csv(paths["kcap"], kcap_rows)
    write_csv(paths["theta"], theta_rows)
    write_csv(paths["template"], source_template)
    write_csv(paths["dry"], dry_rows_)
    write_csv(paths["gates"], gates)
    write_csv(paths["decision"], decisions)
    write_csv(paths["next"], next_rows_)
    copies = write_branch_copies(kcap_rows, theta_rows, source_template, dry_rows_, next_rows_)
    write_csv(paths["branch"], copies)
    remove_pycache()
    csv_paths_without_validation = [path for key, path in paths.items() if key != "validation"] + [Path(row["path"]) for row in copies]
    validation = validation_rows(sources, kcap_rows, theta_rows, source_template, dry_rows_, gates, next_rows_, csv_paths_without_validation)
    write_csv(paths["validation"], validation)
    csv_paths = list(paths.values()) + [Path(row["path"]) for row in copies]
    remove_pycache()
    validation = validation_rows(sources, kcap_rows, theta_rows, source_template, dry_rows_, gates, next_rows_, csv_paths)
    write_csv(paths["validation"], validation)
    write_doc(sources, kcap_rows, theta_rows, source_template, dry_rows_, gates, decisions, next_rows_, copies, validation)
    remove_pycache()


if __name__ == "__main__":
    main()
