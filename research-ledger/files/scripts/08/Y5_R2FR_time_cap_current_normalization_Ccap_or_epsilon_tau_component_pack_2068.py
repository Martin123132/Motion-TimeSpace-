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


DOC = ROOT / "2068-Y5-R2FR-time-cap-current-normalization-Ccap-or-epsilon-tau-component-pack.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()


def formalization_has_2068_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    try:
        patterns = (
            "*2068-Y5-R2FR*",
            "*P8_Y5_PARENT_QLOC_2068*",
            "*Y5_R2FR_time_cap_current_normalization_Ccap_or_epsilon_tau_component_pack_2068*",
        )
        return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))
    except Exception:
        return False


def scripts_pycache_exists() -> bool:
    return (SCRIPT_PATH.parent / "__pycache__").exists()


def source_register_rows() -> list[dict[str, object]]:
    specs = [
        (
            "SRC2068_00_2067_doc",
            ROOT / "2067-Y5-R2FR-stationary-tau-Killing-owner-or-beta-time-caps-bound.md",
            ["NEXT2067_0_2068", "C_cap", "BTC2067_12_total_join"],
            "2067 handoff into cap-current normalization or epsilon_tau component pack.",
        ),
        (
            "SRC2068_01_2067_next",
            OUT / "P8_Y5_PARENT_QLOC_2067_NEXT_TARGET.csv",
            ["NEXT2067_0_2068", "cap-current definition", "W_time_caps"],
            "machine-readable 2068 target.",
        ),
        (
            "SRC2068_02_2067_bridge",
            OUT / "P8_Y5_PARENT_QLOC_2067_CAP_CURRENT_BRIDGE.csv",
            ["CCB2067_0_exact_current_identity", "CCB2067_2_epsilon_tau_bridge", "BOUND_BRIDGE_NONCLAIM_READY"],
            "cap-current bridge from epsilon_tau to beta_time_caps.",
        ),
        (
            "SRC2068_03_2067_inputs",
            OUT / "P8_Y5_PARENT_QLOC_2067_BETA_TIME_CAPS_INPUT_PACK.csv",
            ["BTC2067_0_C_cap", "BTC2067_1_W_time_caps", "BTC2067_12_total_join"],
            "beta_time_caps input pack requiring C_cap/W_time_caps and components.",
        ),
        (
            "SRC2068_04_686_killing_identity",
            OUT / "P8_Y5_R10_686_KILLING_IDENTITY_ATTEMPT.csv",
            ["KIA686_0_exact_identity", "KIA686_3_residual_definition", "epsilon_nonstationary_tau"],
            "exact current-divergence identity and nonstationary residual definition.",
        ),
        (
            "SRC2068_05_686_nonstationary",
            OUT / "P8_Y5_R10_686_NONSTATIONARY_TAU_RESIDUAL_ROW.csv",
            ["NTR686_0_epsilon_nonstationary_tau", "M_ref_candidate", "MISSING_STATIONARY_KILLING_CERTIFICATE_OR_SOURCE_BACKED_BOUND"],
            "epsilon_nonstationary_tau residual row.",
        ),
        (
            "SRC2068_06_687_bound_contract",
            OUT / "P8_Y5_R10_687_EPSILON_TAU_BOUND_CONTRACT.csv",
            ["ETB687_0_exact_numerator", "ETB687_3_dimensionless_epsilon", "ETB687_4_acceptance_rule"],
            "epsilon_tau numerator, denominator and acceptance rule.",
        ),
        (
            "SRC2068_07_688_symgrad",
            OUT / "P8_Y5_R10_688_SYMGRAD_TAU_DECOMPOSITION.csv",
            ["SGT688_0_exact_congruence_identity", "SGT688_7_stress_contraction", "SGT688_8_verdict"],
            "symgrad_tau decomposition and source-input verdict.",
        ),
        (
            "SRC2068_08_688_component_template",
            OUT / "P8_Y5_R10_688_COMPONENT_BOUND_INPUT_TEMPLATE.csv",
            ["CSI688_0_theta", "CSI688_7_denominator", "CSI688_8_coefficients"],
            "epsilon_tau component-bound input template.",
        ),
        (
            "SRC2068_09_2064_corner_bound",
            OUT / "P8_Y5_PARENT_QLOC_2064_FINITE_PIR_CORNER_BOUND_SCHEMA.csv",
            ["PCB2064_3_component_abs_sum", "PCB2064_4_join_PiRtot", "PCB2064_5_qR_guard"],
            "Pi_R corner absolute-sum and q_R guardrail.",
        ),
        (
            "SRC2068_10_2065_beta_rows",
            OUT / "P8_Y5_PARENT_QLOC_2065_BETA_CORNER_PLACEHOLDER_ROWS.csv",
            ["BCP2065_6_no_cancellation_join", "Pi_R_corner_abs_total", "MISSING_ALL_BETA_CORNER_VALUES_AND_WEIGHTS"],
            "no-cancellation corner join precedent.",
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


def normalization_attempt_rows() -> list[dict[str, object]]:
    data = [
        (
            "TCN2068_0_current_numerator",
            "N_tau_cap",
            "N_tau_cap := abs(int_slab T_H^{mu nu} nabla_(mu tau_nu) dV_tau)",
            "same mass/energy units as T_H integrated over the cap/slab convention",
            "exact numerator definition from KIA686/ETB687",
            "DEFINED_SYMBOLIC_NONCLAIM",
            "requires same-frame T_H, tau, domain/slab orientation and units before numeric use",
            False,
        ),
        (
            "TCN2068_1_dimensionless_fraction",
            "epsilon_cap_norm",
            "epsilon_cap_norm := N_tau_cap / M_ref_candidate",
            "dimensionless",
            "normalized cap fraction",
            "CONDITIONAL_NORMAL_FORM_AVAILABLE",
            "only meaningful if M_ref_candidate is positive, same-frame, sourced and denominator-valid",
            False,
        ),
        (
            "TCN2068_2_Ccap_norm",
            "C_cap_norm",
            "C_cap_norm = 1",
            "dimensionless",
            "definition-level normalization for epsilon_cap_norm only",
            "EXACT_BY_DEFINITION_FOR_NORMALIZED_FRACTION",
            "does not map to physical Pi_R boundary-current units",
            False,
        ),
        (
            "TCN2068_3_Wtime_norm",
            "W_time_caps_norm",
            "W_time_caps_norm = 1",
            "dimensionless",
            "definition-level weight for epsilon_cap_norm only",
            "EXACT_BY_DEFINITION_FOR_NORMALIZED_FRACTION",
            "does not eliminate physical cap/source/reference terms",
            False,
        ),
        (
            "TCN2068_4_physical_PiR_map",
            "K_cap_to_PiR",
            "Pi_R_time_caps_abs <= K_cap_to_PiR * M_ref_candidate * epsilon_cap_norm + B_source_caps_abs + B_ref_caps_abs",
            "Pi_R boundary-current units per mass/energy unit",
            "physical conversion from normalized cap leakage into Pi_R corner units",
            "MISSING_K_CAP_TO_PIR_MAP",
            "this is the real unclosed normalization, not C_cap_norm",
            False,
        ),
        (
            "TCN2068_5_qR_join",
            "q_R_time_caps_guard",
            "abs(Pi_R_time_caps)/(N_sphere Z_R_infty r_s) enters q_R guard after component absolute join",
            "dimensionless after full q_R normalization chain",
            "connects cap leakage to PPN/local scoring",
            "MISSING_QR_NORMALIZATION_CHAIN",
            "requires N_sphere, Z_R_infty, same-frame r_s, orientation and tail terms",
            False,
        ),
        (
            "TCN2068_6_verdict",
            "C_cap/W_time_caps normalization",
            "C_cap_norm=W_time_caps_norm=1 closes only the normalized epsilon fraction; physical Pi_R scoring still needs K_cap_to_PiR and q_R normalization",
            "mixed",
            "normalization split",
            "PARTIAL_NORMAL_FORM_NOT_PHYSICAL_SCORE",
            "do not claim beta_time_caps or local-GR pass from the normalized row",
            False,
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, quantity, formula, units, role, status, note, ready_for_scoring in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "quantity": quantity,
                "formula": formula,
                "units": units,
                "role": role,
                "status": status,
                "note": note,
                "ready_for_scoring": ready_for_scoring,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def epsilon_component_pack_rows() -> list[dict[str, object]]:
    data = [
        (
            "ECP2068_0_master_bound",
            "epsilon_nonstationary_tau",
            "epsilon_tau <= epsilon_theta + epsilon_shear + epsilon_lapse + epsilon_shift + epsilon_boundary + epsilon_tau_mismatch + epsilon_stress_exchange",
            "dimensionless",
            "all component rows numeric/theorem-zero, same-frame, denominator-valid and absolute-summed",
            "MISSING_COMPONENT_VALUES_AND_DENOMINATOR",
        ),
        (
            "ECP2068_1_theta_first_row",
            "epsilon_theta",
            "epsilon_theta <= C_theta * S_theta * |theta_D_or_X_D| / M_ref_candidate",
            "dimensionless",
            "theta/X_D source bound, stress weight S_theta, coefficient C_theta, M_ref_candidate",
            "MISSING_THETA_D_OR_XD_SOURCE_BOUND",
        ),
        (
            "ECP2068_2_shear",
            "epsilon_shear",
            "epsilon_shear <= C_sigma * S_sigma * ||sigma|| / M_ref_candidate",
            "dimensionless",
            "shear source/theorem-zero, stress weight, coefficient, denominator",
            "MISSING_SHEAR_SOURCE_BOUND",
        ),
        (
            "ECP2068_3_lapse",
            "epsilon_lapse",
            "epsilon_lapse <= C_lapse * S_lapse * ||a + grad log N|| / M_ref_candidate",
            "dimensionless",
            "lapse/acceleration gauge-safe source bound, stress weight, coefficient, denominator",
            "MISSING_LAPSE_ACCELERATION_SOURCE_BOUND",
        ),
        (
            "ECP2068_4_shift",
            "epsilon_shift",
            "epsilon_shift <= C_shift * S_shift * ||K_shift|| / M_ref_candidate",
            "dimensionless",
            "shift/extrinsic curvature source bound, ADM convention, coefficient, denominator",
            "MISSING_SHIFT_EXTRINSIC_SOURCE_BOUND",
        ),
        (
            "ECP2068_5_boundary",
            "epsilon_boundary",
            "epsilon_boundary <= C_boundary * S_boundary * |v_boundary/reference_shift| / M_ref_candidate",
            "dimensionless",
            "boundary motion/reference-shift source bound, coefficient, denominator",
            "MISSING_BOUNDARY_MOTION_SOURCE_BOUND",
        ),
        (
            "ECP2068_6_tau_mismatch",
            "epsilon_tau_mismatch",
            "epsilon_tau_mismatch <= C_tau * |tau_source_clock_charge_orbit_boundary_mismatch|",
            "dimensionless",
            "same-tau mismatch source/theorem-zero and coefficient",
            "MISSING_TAU_ROLE_MISMATCH_SOURCE_BOUND",
        ),
        (
            "ECP2068_7_stress_exchange",
            "epsilon_stress_exchange",
            "epsilon_stress_exchange <= abs(int (nabla_mu T_H^{mu nu}) tau_nu dV_tau)/M_ref_candidate",
            "dimensionless",
            "mass-channel exchange silence or source-backed exchange numerator and denominator",
            "MISSING_MASS_CHANNEL_EXCHANGE_BOUND",
        ),
        (
            "ECP2068_8_denominator",
            "M_ref_candidate",
            "positive same-frame mass/energy denominator",
            "mass/energy units",
            "M_H_ref or sourced denominator, same-frame flag, positive value, source path",
            "MISSING_CLAIM_READY_M_REF_CANDIDATE",
        ),
        (
            "ECP2068_9_acceptance",
            "epsilon_tau_acceptance",
            "valid_for_claim=true only if all retained components are numeric/theorem-zero, sourced, unit-compatible and absolute-summed",
            "boolean gate",
            "no MISSING markers, denominator-valid, source paths and assumptions complete",
            "SCHEMA_ONLY_NONCLAIM",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, quantity, formula, units, required_input, blocker in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "quantity": quantity,
                "formula": formula,
                "units": units,
                "required_input": required_input,
                "blocker": blocker,
                "source_ready_schema": True,
                "ready_for_scoring": False,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def physical_join_rows() -> list[dict[str, object]]:
    data = [
        (
            "PJR2068_0_normalized_cap_fraction",
            "epsilon_cap_norm",
            "epsilon_cap_norm = N_tau_cap/M_ref_candidate",
            "dimensionless",
            "normalized diagnostic only",
            "NOT_PHYSICAL_PIR_UNITS",
        ),
        (
            "PJR2068_1_physical_cap_component",
            "Pi_R_time_caps_abs",
            "Pi_R_time_caps_abs <= K_cap_to_PiR * M_ref_candidate * epsilon_cap_norm + B_source_caps_abs + B_ref_caps_abs",
            "Pi_R boundary-current units",
            "physical Pi_R corner component",
            "MISSING_K_CAP_TO_PIR_AND_CAP_SEPARATION",
        ),
        (
            "PJR2068_2_corner_abs_join",
            "Pi_R_corner_abs",
            "Pi_R_corner_abs = Pi_R_time_caps_abs + sum_other abs(beta_corner_i) W_i",
            "Pi_R boundary-current units",
            "no-cancellation corner join",
            "MISSING_OTHER_BETA_CORNER_ROWS",
        ),
        (
            "PJR2068_3_total_PiR_join",
            "Pi_R_tot_abs",
            "|Pi_R^matter| + |Pi_R^boundary| + |Pi_R^corner| + |Pi_R^readout|",
            "Pi_R boundary-current units",
            "full local residual join",
            "MISSING_COMPONENT_ABSOLUTE_SUM",
        ),
        (
            "PJR2068_4_qR_guard",
            "q_R^PPN guard",
            "|Pi_R^tot/(N_sphere Z_R_infty r_s)| + B_tail_abs <= local bound",
            "dimensionless",
            "PPN/local scoring guard",
            "MISSING_NORMALIZATION_AND_TAILS",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, quantity, formula, units, role, blocker in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "quantity": quantity,
                "formula": formula,
                "units": units,
                "role": role,
                "blocker": blocker,
                "ready_for_scoring": False,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def dry_run_rows(
    norm_rows: list[dict[str, object]],
    component_rows: list[dict[str, object]],
    join_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    verdict = next(row for row in norm_rows if row["row_id"] == "TCN2068_6_verdict")
    rows_data = [
        (
            "RUN2068_0_normalized_fraction",
            "C_cap_norm and W_time_caps_norm",
            "NORMAL_FORM_PARTIAL_SUCCESS",
            "C_cap_norm=W_time_caps_norm=1 by definition for epsilon_cap_norm only",
            False,
        ),
        (
            "RUN2068_1_physical_PiR",
            "physical beta_time_caps/Pi_R map",
            "REFUSED_PHYSICAL_SCORE",
            str(verdict["status"]),
            False,
        ),
        (
            "RUN2068_2_component_pack",
            "epsilon_tau component source pack",
            "SCHEMA_WRITTEN_VALUES_MISSING",
            f"component_rows={len(component_rows)}; no numeric/theorem-zero values accepted",
            False,
        ),
        (
            "RUN2068_3_join_guard",
            "Pi_R/q_R join",
            "JOIN_SCHEMA_WRITTEN_NOT_SCORABLE",
            f"join_rows={len(join_rows)}; missing K_cap_to_PiR and q_R normalization",
            False,
        ),
        (
            "RUN2068_VERDICT",
            "time-cap current normalization or epsilon component pack",
            "NORMALIZED_CAP_FRACTION_CLOSED_PHYSICAL_PIR_STILL_BLOCKED",
            "2069 should derive K_cap_to_PiR or fill M_ref/first epsilon component row",
            False,
        ),
    ]
    rows: list[dict[str, object]] = []
    for run_id, target, verdict_status, reason, accepted in rows_data:
        row = base_row()
        row.update(
            {
                "run_id": run_id,
                "target": target,
                "verdict": verdict_status,
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
            "GATE2068_0_Ccap_norm",
            "C_cap/W_time_caps normalized fraction",
            "PASS_CONDITIONAL_DEFINITION_ONLY",
            "C=1/W=1 only for epsilon_cap_norm, not physical Pi_R units",
        ),
        (
            "GATE2068_1_physical_PiR_map",
            "K_cap_to_PiR maps epsilon into Pi_R units",
            "FAIL_BLOCKED",
            "physical conversion coefficient/source path is missing",
        ),
        (
            "GATE2068_2_epsilon_components",
            "epsilon_tau component pack source-backed",
            "FAIL_BLOCKED",
            "theta/shear/lapse/shift/boundary/tau-mismatch/stress/denominator values missing",
        ),
        (
            "GATE2068_3_denominator",
            "M_ref_candidate denominator claim-ready",
            "FAIL_BLOCKED",
            "positive same-frame denominator remains missing",
        ),
        (
            "GATE2068_4_cap_separation",
            "source/reference cap separation complete",
            "FAIL_BLOCKED",
            "B_source_caps_abs and B_ref_caps_abs are not zeroed or bounded",
        ),
        (
            "GATE2068_5_qR_score",
            "q_R/local PPN score allowed",
            "FAIL_BLOCKED",
            "Pi_R total join and q_R normalization chain remain incomplete",
        ),
        (
            "GATE2068_6_formalization",
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
            "DEC2068_0_partial_success",
            "NORMALIZED_CAP_FRACTION_HAS_EXACT_C_EQUALS_ONE",
            "For epsilon_cap_norm=N_tau/M_ref, C_cap_norm and W_time_caps_norm are one by definition.",
        ),
        (
            "DEC2068_1_main_guardrail",
            "DO_NOT_CONFUSE_NORMALIZED_FRACTION_WITH_PHYSICAL_PIR",
            "The local PPN branch needs Pi_R/q_R units; that still needs K_cap_to_PiR and the q_R normalization chain.",
        ),
        (
            "DEC2068_2_component_pack",
            "EPSILON_TAU_SOURCE_PACK_IS_READY_BUT_UNFILLED",
            "The first theta row and the full component split are staged, but no numeric/theorem-zero component is claim-ready.",
        ),
        (
            "DEC2068_3_next_order",
            "KCAP_OR_DENOMINATOR_FIRST",
            "K_cap_to_PiR and M_ref_candidate are upstream of any useful numeric epsilon_tau score.",
        ),
        (
            "DEC2068_4_next",
            "TARGET_KCAP_TO_PIR_OR_MREF_THETA_FIRST_ROW",
            "2069 should derive the physical Pi_R conversion or fill M_ref_candidate plus the first theta/X_D component source row.",
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
            "target_id": "NEXT2068_0_2069",
            "target_doc": "2069-Y5-R2FR-Kcap-to-PiR-conversion-or-Mref-theta-component-first-row.md",
            "objective": "derive the physical conversion K_cap_to_PiR from normalized cap leakage into Pi_R boundary-current units, or fill M_ref_candidate plus the first theta/X_D epsilon_tau component source row",
            "must_include": "K_cap_to_PiR units; Pi_R variation convention; cap/slab orientation; M_ref_candidate denominator; theta/X_D source row; stress weight; coefficient C_theta; source/reference cap separation; q_R normalization guard",
            "excluded": "using C_cap_norm=1 as physical Pi_R score; numeric placeholders; fitted denominator; cancellation; local-GR/PPN scoring; GitHub; formalization-workbench edits",
            "claim_allowed": False,
        }
    )
    return [row]


def write_branch_copies(
    norm_rows: list[dict[str, object]],
    component_rows: list[dict[str, object]],
    join_rows: list[dict[str, object]],
    dry_rows_: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
) -> list[dict[str, object]]:
    copies = [
        (
            "COPY2068_0_source_weight_norm",
            SOURCE_WEIGHT_DOCS / "AFRAME_TIME_CAP_NORMALIZATION_2068_NONCLAIM.csv",
            norm_rows,
        ),
        (
            "COPY2068_1_source_weight_components",
            SOURCE_WEIGHT_DOCS / "AFRAME_EPSILON_TAU_COMPONENT_PACK_2068_SOURCE_ROW_SCHEMA_NONCLAIM.csv",
            component_rows,
        ),
        (
            "COPY2068_2_source_weight_join",
            SOURCE_WEIGHT_DOCS / "AFRAME_TIME_CAP_PIR_JOIN_2068_NONCLAIM.csv",
            join_rows,
        ),
        (
            "COPY2068_3_wep_dry_run",
            BRANCH_WEP / "P8_Y5_PARENT_QLOC_2068_NORMALIZATION_DRY_RUN_NONCLAIM.csv",
            dry_rows_,
        ),
        (
            "COPY2068_4_queue_next",
            QUEUE / "JR2068_KCAP_OR_MREF_THETA_NEXT_NONCLAIM.csv",
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
    norm_rows: list[dict[str, object]],
    component_rows: list[dict[str, object]],
    join_rows: list[dict[str, object]],
    dry_rows_: list[dict[str, object]],
    gates: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    source_ok = all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in sources)
    csv_ok = all(csv_rows_parse(path) for path in csv_paths)
    norm_verdict = next(row for row in norm_rows if row["row_id"] == "TCN2068_6_verdict")
    norm_ok = (
        any(row["row_id"] == "TCN2068_2_Ccap_norm" and row["status"] == "EXACT_BY_DEFINITION_FOR_NORMALIZED_FRACTION" for row in norm_rows)
        and any(row["row_id"] == "TCN2068_4_physical_PiR_map" and row["status"] == "MISSING_K_CAP_TO_PIR_MAP" for row in norm_rows)
        and norm_verdict["status"] == "PARTIAL_NORMAL_FORM_NOT_PHYSICAL_SCORE"
        and all(not bool(row["ready_for_scoring"]) for row in norm_rows)
    )
    required_components = {
        "epsilon_nonstationary_tau",
        "epsilon_theta",
        "epsilon_shear",
        "epsilon_lapse",
        "epsilon_shift",
        "epsilon_boundary",
        "epsilon_tau_mismatch",
        "epsilon_stress_exchange",
        "M_ref_candidate",
        "epsilon_tau_acceptance",
    }
    component_ok = required_components.issubset({str(row["quantity"]) for row in component_rows}) and all(
        bool(row["source_ready_schema"]) and not bool(row["ready_for_scoring"]) for row in component_rows
    )
    join_ok = any(row["row_id"] == "PJR2068_1_physical_cap_component" and row["blocker"] == "MISSING_K_CAP_TO_PIR_AND_CAP_SEPARATION" for row in join_rows) and all(
        not bool(row["ready_for_scoring"]) for row in join_rows
    )
    dry_verdict = next(row for row in dry_rows_ if row["run_id"] == "RUN2068_VERDICT")
    dry_ok = dry_verdict["verdict"] == "NORMALIZED_CAP_FRACTION_CLOSED_PHYSICAL_PIR_STILL_BLOCKED"
    gates_ok = all(row["claim_allowed"] is False for row in gates) and all(row["status"] != "PASS_CLAIM" for row in gates)
    next_ok = next_rows_[0]["target_id"] == "NEXT2068_0_2069"
    no_claim = all(
        not bool(row.get("claim_allowed", False)) and not bool(row.get("valid_for_claim", False))
        for group in [sources, norm_rows, component_rows, join_rows, dry_rows_, gates, next_rows_]
        for row in group
    )
    checks: list[tuple[str, bool, str]] = []
    checks.append(("VAL2068_00_local_sources_exist", source_ok, "all cited source paths and needles exist"))
    checks.append(("VAL2068_01_csv_parse", csv_ok, "all generated CSV files parse cleanly"))
    checks.append(("VAL2068_02_normalization_split", norm_ok, "C=1 normal form is limited to normalized fraction; physical Pi_R remains blocked"))
    checks.append(("VAL2068_03_component_pack", component_ok, "epsilon_tau component pack is source-ready but unscored"))
    checks.append(("VAL2068_04_physical_join", join_ok, "physical Pi_R/q_R join is written and blocked on K_cap_to_PiR"))
    checks.append(("VAL2068_05_dry_verdict", dry_ok, "dry run refuses physical scoring while accepting normalized fraction form"))
    checks.append(("VAL2068_06_claim_gates_blocked", gates_ok, "all claim gates remain blocked/nonclaim"))
    checks.append(("VAL2068_07_next_selected", next_ok, "2069 K_cap_to_PiR or M_ref/theta target selected"))
    checks.append(("VAL2068_08_no_claim_flags", no_claim, "no generated row allows a claim"))
    checks.append(("VAL2068_09_formalization_unchanged", count_formalization_modified() == 0, "formalization-workbench modified-file count remains 0"))
    checks.append(("VAL2068_10_no_formalization_artifacts", not formalization_has_2068_artifacts(), "no 2068 artifacts were written under formalization-workbench"))
    checks.append(("VAL2068_11_no_pycache", not scripts_pycache_exists(), "scripts __pycache__ removed"))
    overall = all(ok for _, ok, _ in checks)
    checks.append(("VAL2068_OVERALL", overall, "2068 closes the normalized cap fraction but keeps physical Pi_R scoring blocked"))
    rows: list[dict[str, object]] = []
    for check_id, ok, detail in checks:
        row = base_row()
        row.update({"check_id": check_id, "status": "PASS" if ok else "FAIL", "detail": detail, "claim_allowed": False})
        rows.append(row)
    return rows


def write_doc(
    sources: list[dict[str, object]],
    norm_rows: list[dict[str, object]],
    component_rows: list[dict[str, object]],
    join_rows: list[dict[str, object]],
    dry_rows_: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    sections = [
        "# 2068 Y5 R2FR Time-Cap Current Normalization Ccap Or Epsilon Tau Component Pack",
        "",
        "## Current Verdict",
        "",
        "2068 closes a narrow but useful normalization point: if we define the normalized cap fraction `epsilon_cap_norm := N_tau_cap/M_ref_candidate`, then `C_cap_norm=1` and `W_time_caps_norm=1` by definition. That is a clean diagnostic row, not a physical `Pi_R` score.",
        "",
        "The physical local branch still needs a conversion map: `Pi_R_time_caps_abs <= K_cap_to_PiR * M_ref_candidate * epsilon_cap_norm + B_source_caps_abs + B_ref_caps_abs`. The missing object is now sharply named: `K_cap_to_PiR`, plus source/reference cap separation and the ordinary q_R normalization chain.",
        "",
        "The epsilon component pack is now staged: trace/`X_D`, shear, lapse, shift/extrinsic curvature, boundary/reference motion, tau-role mismatch, stress-exchange, and denominator rows. None are numeric or theorem-zero yet, so no local-GR/PPN claim follows.",
        "",
        "No local-GR/Newton, Cassini, PPN, R10, clock, orbital, corner-zero, or finite-residual claim is allowed. No GitHub action and no `formalization-workbench` edit is made.",
        "",
        "## Source Register",
        md_table(sources, ["source_id", "source_kind", "source_path", "status", "note", "valid_for_claim"]),
        "## Cap Normalization Attempt",
        md_table(norm_rows, ["row_id", "quantity", "formula", "units", "role", "status", "note", "ready_for_scoring", "claim_allowed"]),
        "## Epsilon Tau Component Pack",
        md_table(component_rows, ["row_id", "quantity", "formula", "units", "required_input", "blocker", "source_ready_schema", "ready_for_scoring", "claim_allowed"]),
        "## Physical Pi_R Join",
        md_table(join_rows, ["row_id", "quantity", "formula", "units", "role", "blocker", "ready_for_scoring", "claim_allowed"]),
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
    norm_rows = normalization_attempt_rows()
    component_rows = epsilon_component_pack_rows()
    join_rows = physical_join_rows()
    dry_rows_ = dry_run_rows(norm_rows, component_rows, join_rows)
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows_ = next_target_rows()
    paths = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2068_SOURCE_REGISTER.csv",
        "norm": OUT / "P8_Y5_PARENT_QLOC_2068_CAP_NORMALIZATION_ATTEMPT.csv",
        "components": OUT / "P8_Y5_PARENT_QLOC_2068_EPSILON_TAU_COMPONENT_PACK.csv",
        "join": OUT / "P8_Y5_PARENT_QLOC_2068_PHYSICAL_PIR_JOIN.csv",
        "dry": OUT / "P8_Y5_PARENT_QLOC_2068_DRY_RUN.csv",
        "gates": OUT / "P8_Y5_PARENT_QLOC_2068_CLAIM_GATE.csv",
        "decision": OUT / "P8_Y5_PARENT_QLOC_2068_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2068_NEXT_TARGET.csv",
        "branch": OUT / "P8_Y5_PARENT_QLOC_2068_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2068_VALIDATION.csv",
    }
    write_csv(paths["sources"], sources)
    write_csv(paths["norm"], norm_rows)
    write_csv(paths["components"], component_rows)
    write_csv(paths["join"], join_rows)
    write_csv(paths["dry"], dry_rows_)
    write_csv(paths["gates"], gates)
    write_csv(paths["decision"], decisions)
    write_csv(paths["next"], next_rows_)
    copies = write_branch_copies(norm_rows, component_rows, join_rows, dry_rows_, next_rows_)
    write_csv(paths["branch"], copies)
    remove_pycache()
    csv_paths_without_validation = [path for key, path in paths.items() if key != "validation"] + [Path(row["path"]) for row in copies]
    validation = validation_rows(sources, norm_rows, component_rows, join_rows, dry_rows_, gates, next_rows_, csv_paths_without_validation)
    write_csv(paths["validation"], validation)
    csv_paths = list(paths.values()) + [Path(row["path"]) for row in copies]
    remove_pycache()
    validation = validation_rows(sources, norm_rows, component_rows, join_rows, dry_rows_, gates, next_rows_, csv_paths)
    write_csv(paths["validation"], validation)
    write_doc(sources, norm_rows, component_rows, join_rows, dry_rows_, gates, decisions, next_rows_, copies, validation)
    remove_pycache()


if __name__ == "__main__":
    main()
