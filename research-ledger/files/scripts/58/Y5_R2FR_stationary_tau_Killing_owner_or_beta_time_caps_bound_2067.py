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


DOC = ROOT / "2067-Y5-R2FR-stationary-tau-Killing-owner-or-beta-time-caps-bound.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()


def formalization_has_2067_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    try:
        patterns = (
            "*2067-Y5-R2FR*",
            "*P8_Y5_PARENT_QLOC_2067*",
            "*Y5_R2FR_stationary_tau_Killing_owner_or_beta_time_caps_bound_2067*",
        )
        return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))
    except Exception:
        return False


def scripts_pycache_exists() -> bool:
    return (SCRIPT_PATH.parent / "__pycache__").exists()


def source_register_rows() -> list[dict[str, object]]:
    specs = [
        (
            "SRC2067_00_2066_doc",
            ROOT / "2066-Y5-R2FR-stationary-PPN-surface-owner-or-first-beta-corner-row.md",
            ["SURF_PPN_STAT_ANNULUS_2066", "FBC2066_2_epsilon_tau_bridge", "NEXT2066_0_2067"],
            "2066 handoff into stationary tau/Killing owner or beta_time_caps bound.",
        ),
        (
            "SRC2067_01_2066_next",
            OUT / "P8_Y5_PARENT_QLOC_2066_NEXT_TARGET.csv",
            ["NEXT2066_0_2067", "epsilon_nonstationary_tau bridge", "C_cap"],
            "machine-readable 2067 target.",
        ),
        (
            "SRC2067_02_686_stationary_certificate",
            OUT / "P8_Y5_R10_686_LOCAL_STATIONARY_CERTIFICATE.csv",
            ["LSC686_1_stationary_solution", "LSC686_2_same_tau", "LSC686_7_verdict"],
            "local stationary/Killing certificate attempt and failed current claim.",
        ),
        (
            "SRC2067_03_686_killing_identity",
            OUT / "P8_Y5_R10_686_KILLING_IDENTITY_ATTEMPT.csv",
            ["KIA686_0_exact_identity", "KIA686_1_Killing_zero", "KIA686_3_residual_definition"],
            "exact stress-current divergence identity and epsilon_tau fallback.",
        ),
        (
            "SRC2067_04_686_nonstationary_row",
            OUT / "P8_Y5_R10_686_NONSTATIONARY_TAU_RESIDUAL_ROW.csv",
            ["NTR686_0_epsilon_nonstationary_tau", "MISSING_STATIONARY_KILLING_CERTIFICATE_OR_SOURCE_BACKED_BOUND", "M_ref_candidate"],
            "epsilon_nonstationary_tau residual row.",
        ),
        (
            "SRC2067_05_687_selector_tau",
            OUT / "P8_Y5_R10_687_SELECTOR_TO_TAU_THEOREM_ATTEMPT.csv",
            ["STT687_3_Killing_upgrade", "STT687_5_verdict", "failed_for_claim"],
            "selector-to-stationary generator failure modes.",
        ),
        (
            "SRC2067_06_687_bound_contract",
            OUT / "P8_Y5_R10_687_EPSILON_TAU_BOUND_CONTRACT.csv",
            ["ETB687_0_exact_numerator", "ETB687_3_dimensionless_epsilon", "ETB687_4_acceptance_rule"],
            "epsilon_tau source-backed bound contract.",
        ),
        (
            "SRC2067_07_687_obstructions",
            OUT / "P8_Y5_R10_687_STATIONARITY_OBSTRUCTION_LEDGER.csv",
            ["OBS687_0_selector_not_geometry", "OBS687_1_trace_not_Killing", "OBS687_5_denominator_open"],
            "stationarity obstruction ledger.",
        ),
        (
            "SRC2067_08_688_symgrad",
            OUT / "P8_Y5_R10_688_SYMGRAD_TAU_DECOMPOSITION.csv",
            ["SGT688_0_exact_congruence_identity", "SGT688_7_stress_contraction", "SGT688_8_verdict"],
            "symgrad_tau decomposition and source-input verdict.",
        ),
        (
            "SRC2067_09_688_component_template",
            OUT / "P8_Y5_R10_688_COMPONENT_BOUND_INPUT_TEMPLATE.csv",
            ["CSI688_0_theta", "CSI688_7_denominator", "CSI688_8_coefficients"],
            "component source-input template for epsilon_tau.",
        ),
        (
            "SRC2067_10_1002_stationary_tau_doc",
            ROOT / "1002-Y5-R10-Bref-stationary-tau-theorem-or-Delta-ref-time-profile-row.md",
            ["STA1002_2_stationary_generator", "TPS1002_1_stationary_tau_zero_switch", "DEC1002_0_theorem_not_closed"],
            "stationary-by-assumption guardrail.",
        ),
        (
            "SRC2067_11_tau_contract",
            OUT / "P8_Y5_R10_685_TAU_GENERATOR_CONTRACT.csv",
            ["TGC685_1_Killing_stationary_route", "TGC685_6_verdict", "blocked_nonclaim"],
            "tau generator and same-tau lock contract.",
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


def tau_owner_attempt_rows() -> list[dict[str, object]]:
    data = [
        (
            "STO2067_0_tau_obs_owner",
            "tau_obs",
            "parent-selected observed time-flow vector, fixed before source/readout fitting",
            "needed to define Sigma_tau in SURF_PPN_STAT_ANNULUS_2066",
            "MISSING_PARENT_TAU_OBS_OWNER",
            "TGC685_0 remains definition target only",
            False,
        ),
        (
            "STO2067_1_Killing_identity",
            "L_tau g_obs=0",
            "nabla_(mu tau_nu)=0 in the tested local exterior",
            "removes nonstationary cap flux and closes the Killing mass-current route with conserved same-frame stress",
            "MISSING_STATIONARY_KILLING_CERTIFICATE",
            "LSC686_1 and STT687_5 explicitly block this",
            False,
        ),
        (
            "STO2067_2_same_tau_lock",
            "tau_source=tau_charge=tau_clock=tau_boundary=tau_orbit=tau_obs",
            "one normalized generator across source, Hamiltonian charge, clocks, boundary reference, and orbital readout",
            "prevents a cap zero in one tau from being scored in another tau",
            "MISSING_SAME_TAU_NORMALIZATION_THEOREM",
            "TGC685_6 blocked_nonclaim",
            False,
        ),
        (
            "STO2067_3_Hilbert_stress_conservation",
            "nabla_mu T_H^{mu nu}=0",
            "same-frame Hilbert stress is separately conserved in the exterior",
            "then KIA686_0 reduces cap leakage to the symgrad_tau contraction",
            "MISSING_MASS_CHANNEL_EXCHANGE_SILENCE",
            "Ward conservation is total; projected mass-channel silence is not proved",
            False,
        ),
        (
            "STO2067_4_domain_owner",
            "D_loc and W_source",
            "parent-owned local domain and compact source support before readout",
            "attaches tau to the real local branch rather than a chosen box",
            "MISSING_PARENT_DOMAIN_AND_SOURCE_OWNER",
            "LSC686_0 and PSC1016 remain conditional",
            False,
        ),
        (
            "STO2067_5_EH_or_R11_operator",
            "local exterior operator",
            "exterior is EH stationary or every retained R11/non-EH operator has a time-dependence/source map",
            "prevents hidden operators from sourcing nonstationary tau even when selector is quiet",
            "MISSING_EH_OR_R11_TIME_DEPENDENCE_MAP",
            "LSC686_3 and OBS687_3 remain blocked",
            False,
        ),
        (
            "STO2067_6_boundary_reference_lock",
            "H_ref and boundary class",
            "stationary boundary/reference subtraction is fixed once in the same tau",
            "needed before epsilon_tau has a claim-grade denominator",
            "MISSING_FIXED_REFERENCE_TAU_BOUNDARY_CLASS",
            "OBS687_5 denominator open",
            False,
        ),
        (
            "STO2067_7_verdict",
            "stationary tau/Killing owner",
            "STO2067_0 through STO2067_6 must close before beta_time_caps=0 can be promoted",
            "current MTS does not prove the owner theorem; epsilon_tau remains the honest residual",
            "FAIL_CURRENT_CLAIM_STATIONARY_TAU_OWNER_UNSIGNED",
            "derive C_cap bridge or source epsilon_tau components next",
            False,
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, object_id, required_identity, implication, status, note, parent_signed in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "object_id": object_id,
                "required_identity": required_identity,
                "implication": implication,
                "status": status,
                "note": note,
                "parent_signed": parent_signed,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def cap_current_bridge_rows() -> list[dict[str, object]]:
    data = [
        (
            "CCB2067_0_exact_current_identity",
            "J_tau",
            "nabla_mu J_tau^mu = (nabla_mu T_H^{mu nu}) tau_nu + T_H^{mu nu} nabla_(mu tau_nu)",
            "from KIA686_0; exact identity, not a zero theorem",
            "EXACT_IDENTITY_AVAILABLE",
            "turns stationary failure into a sourceable numerator",
            False,
        ),
        (
            "CCB2067_1_finite_slab_stokes",
            "cap flux difference",
            "abs(Pi_R_time_caps) <= abs(int_{slab} nabla_mu J_tau^mu dV_tau) + abs(endpoint/source/reference cap terms)",
            "Stokes-style absolute-value guard; no sign cancellation",
            "BOUND_FORM_AVAILABLE_CONDITIONAL",
            "needs cap-current normalization and endpoint separation",
            False,
        ),
        (
            "CCB2067_2_epsilon_tau_bridge",
            "beta_corner_time_caps_abs",
            "beta_corner_time_caps_abs <= C_cap * epsilon_nonstationary_tau * W_time_caps + B_source_caps_abs + B_ref_caps_abs",
            "bridge to 2066 first beta row",
            "SCHEMA_AVAILABLE_VALUES_MISSING",
            "C_cap, W_time_caps, source/reference cap separation and denominator are missing",
            False,
        ),
        (
            "CCB2067_3_zero_switch",
            "beta_time_caps_zero",
            "if stationary_tau_owner=true and endpoint/reference cap terms are zero, then beta_corner_time_caps=0",
            "conditional theorem-zero switch",
            "CONDITIONAL_ZERO_NOT_ARENA_CERTIFIED",
            "blocked by STO2067 verdict",
            False,
        ),
        (
            "CCB2067_4_no_cancellation_join",
            "Pi_R_corner_abs_total",
            "Pi_R^corner_abs >= beta_time_caps_abs and must add other active corner families by absolute value",
            "prevents time-cap cancellation against source/excision/reference corners",
            "NO_CANCELLATION_GUARD_WRITTEN",
            "other beta_corner rows still missing",
            False,
        ),
        (
            "CCB2067_5_verdict",
            "time-cap bridge",
            "the bridge is exact enough to guide sourcing, but not numeric or theorem-zero",
            "future source pack can fill it without changing the logic",
            "BOUND_BRIDGE_NONCLAIM_READY",
            "next target should normalize C_cap/W_time_caps or fill epsilon_tau components",
            False,
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, quantity, formula, derivation_source, status, note, ready_for_scoring in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "quantity": quantity,
                "formula": formula,
                "derivation_source": derivation_source,
                "status": status,
                "note": note,
                "ready_for_scoring": ready_for_scoring,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def beta_time_caps_input_rows() -> list[dict[str, object]]:
    data = [
        (
            "BTC2067_0_C_cap",
            "C_cap",
            "normalization constant mapping epsilon_nonstationary_tau into beta_corner_time_caps units",
            "dimensionless or declared conversion",
            "cap-current definition; norm convention; surface/slab measure convention; source path",
            "MISSING_C_CAP_NORMALIZATION",
        ),
        (
            "BTC2067_1_W_time_caps",
            "W_time_caps",
            "measure/weight of the time-cap contribution in the Pi_R^corner_abs join",
            "declared cap-current weight units",
            "finite slab convention or theorem that W_time_caps=0 under stationary spatial reduction",
            "MISSING_W_TIME_CAPS_MEASURE",
        ),
        (
            "BTC2067_2_epsilon_tau",
            "epsilon_nonstationary_tau",
            "abs(int T_H^{mu nu} symgrad_tau_mu_nu dV_tau)/M_ref_candidate",
            "dimensionless",
            "same-frame numerator and denominator; no MISSING markers",
            "MISSING_SOURCE_BACKED_EPSILON_TAU",
        ),
        (
            "BTC2067_3_theta_component",
            "theta_D_or_X_D",
            "trace/volume component of symgrad_tau",
            "1/time or normalized dimensionless",
            "component bound, averaging rule, source path, coefficient",
            "MISSING_THETA_D_OR_XD_SOURCE_BOUND",
        ),
        (
            "BTC2067_4_shear_component",
            "sigma_mu_nu",
            "tracefree shear component of symgrad_tau",
            "1/time or normalized dimensionless",
            "shear norm bound/source or theorem-zero",
            "MISSING_SHEAR_SOURCE_BOUND",
        ),
        (
            "BTC2067_5_lapse_component",
            "a_mu_and_grad_lapse",
            "lapse/acceleration contribution to symgrad_tau",
            "1/time or normalized dimensionless",
            "clock/lapse gauge-safe bound or theorem-zero",
            "MISSING_LAPSE_ACCELERATION_SOURCE_BOUND",
        ),
        (
            "BTC2067_6_shift_component",
            "shift_or_extrinsic_curvature",
            "ADM shift/extrinsic curvature contribution to spatial stationarity",
            "1/time or normalized dimensionless",
            "K_ij/shift convention and source bound",
            "MISSING_SHIFT_EXTRINSIC_SOURCE_BOUND",
        ),
        (
            "BTC2067_7_boundary_motion",
            "boundary_velocity_and_reference_shift",
            "moving boundary/reference-class contribution",
            "dimensionless or energy fraction",
            "boundary class, velocity/reference rule, source path",
            "MISSING_BOUNDARY_MOTION_SOURCE_BOUND",
        ),
        (
            "BTC2067_8_tau_mismatch",
            "tau_source_clock_charge_orbit_boundary_mismatch",
            "same-tau normalization mismatch",
            "dimensionless",
            "tau role map and mismatch norm/source",
            "MISSING_TAU_ROLE_MISMATCH_SOURCE_BOUND",
        ),
        (
            "BTC2067_9_stress_envelope",
            "same_frame_T_H_envelope",
            "stress envelope for contracting symgrad_tau",
            "energy/mass units or declared density units",
            "same-frame stress source, integration domain, norm convention",
            "MISSING_SAME_FRAME_STRESS_SOURCE_BOUND",
        ),
        (
            "BTC2067_10_denominator",
            "M_ref_candidate",
            "same-frame positive mass/energy denominator",
            "mass/energy units",
            "M_H_ref or sourced denominator with same-frame flag",
            "MISSING_CLAIM_READY_M_REF_CANDIDATE",
        ),
        (
            "BTC2067_11_source_reference_caps",
            "B_source_caps_abs + B_ref_caps_abs",
            "endpoint/source/reference cap terms not covered by epsilon_tau",
            "boundary-current units",
            "endpoint ledger, reference cap rule, separate beta/source-zero rows",
            "MISSING_SOURCE_REFERENCE_CAP_SEPARATION",
        ),
        (
            "BTC2067_12_total_join",
            "beta_corner_time_caps_abs",
            "C_cap * epsilon_tau * W_time_caps + B_source_caps_abs + B_ref_caps_abs",
            "boundary-current units",
            "all prior inputs numeric/theorem-zero and source-backed",
            "MISSING_ALL_NUMERIC_OR_THEOREM_ZERO_INPUTS",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, quantity, definition, units, required_input, blocker in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "quantity": quantity,
                "definition": definition,
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


def dry_run_rows(
    owner_rows: list[dict[str, object]],
    bridge_rows: list[dict[str, object]],
    beta_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    owner_verdict = next(row for row in owner_rows if row["row_id"] == "STO2067_7_verdict")
    bridge_verdict = next(row for row in bridge_rows if row["row_id"] == "CCB2067_5_verdict")
    rows_data = [
        (
            "RUN2067_0_Killing_owner",
            "stationary tau/Killing owner",
            "REFUSED_OWNER_UNSIGNED",
            str(owner_verdict["status"]),
            False,
        ),
        (
            "RUN2067_1_cap_bridge",
            "epsilon_tau to beta_time_caps bridge",
            "BOUND_BRIDGE_WRITTEN_NONCLAIM",
            str(bridge_verdict["status"]),
            False,
        ),
        (
            "RUN2067_2_beta_inputs",
            "beta_time_caps source pack",
            "SCHEMA_WRITTEN_VALUES_MISSING",
            f"input_rows={len(beta_rows)}; all ready_for_scoring=false",
            False,
        ),
        (
            "RUN2067_VERDICT",
            "stationary tau or beta_time_caps bound",
            "KILLING_OWNER_FAILS_CAP_BOUND_BRIDGE_STAGED",
            "2068 should derive C_cap/W_time_caps normalization or fill epsilon_tau component inputs",
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
            "GATE2067_0_Killing_owner",
            "stationary tau/Killing owner passes",
            "FAIL_BLOCKED",
            "tau owner, Killing identity, same-tau lock, source domain, and boundary reference are unsigned",
        ),
        (
            "GATE2067_1_beta_time_caps_zero",
            "beta_corner_time_caps=0 theorem",
            "FAIL_BLOCKED",
            "conditional on stationary owner and endpoint/reference cap zero",
        ),
        (
            "GATE2067_2_cap_bridge_numeric",
            "epsilon_tau bridge gives numeric beta_time_caps bound",
            "FAIL_BLOCKED",
            "C_cap, W_time_caps, epsilon_tau, source/reference caps, and denominator missing",
        ),
        (
            "GATE2067_3_epsilon_tau",
            "epsilon_nonstationary_tau is source-backed and denominator-valid",
            "FAIL_BLOCKED",
            "symgrad/stress/denominator component pack is unfilled",
        ),
        (
            "GATE2067_4_PiRcorner_total",
            "Pi_R^corner_abs total is scoreable",
            "FAIL_BLOCKED",
            "other active corner families remain unbounded",
        ),
        (
            "GATE2067_5_local_GR",
            "local GR/PPN branch can claim pass",
            "FAIL_BLOCKED",
            "time-cap branch remains nonclaim and q_R normalization remains incomplete",
        ),
        (
            "GATE2067_6_formalization",
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
            "DEC2067_0_Killing_route",
            "KILLING_ROUTE_REMAINS_CONDITIONAL",
            "The formal identity is clean, but current MTS lacks the parent tau owner, same-tau lock, and mass-channel conservation needed for theorem-zero.",
        ),
        (
            "DEC2067_1_progress",
            "TIME_CAP_LEAKAGE_IS_NOW_A_BOUNDABLE_CURRENT",
            "The cap problem is no longer vague: it is controlled by epsilon_tau plus explicit source/reference cap terms.",
        ),
        (
            "DEC2067_2_no_cancellation",
            "ABSOLUTE_CAP_JOIN_REQUIRED",
            "Time-cap leakage cannot be canceled against source, reference, patch, or excision corners.",
        ),
        (
            "DEC2067_3_next_order",
            "NORMALIZE_CCAP_BEFORE_NUMERIC_SCORING",
            "A future epsilon_tau number is not useful unless the cap-current normalization and W_time_caps convention are fixed.",
        ),
        (
            "DEC2067_4_next",
            "TARGET_CCAP_OR_EPSILON_TAU_COMPONENTS",
            "2068 should either derive C_cap/W_time_caps from the cap-current definition or fill the first source-backed epsilon_tau component row.",
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
            "target_id": "NEXT2067_0_2068",
            "target_doc": "2068-Y5-R2FR-time-cap-current-normalization-Ccap-or-epsilon-tau-component-pack.md",
            "objective": "derive the cap-current normalization C_cap and W_time_caps convention that maps epsilon_nonstationary_tau into beta_corner_time_caps, or fill the first source-backed epsilon_tau component row",
            "must_include": "cap-current definition; finite-slab/Stokes orientation; C_cap units; W_time_caps measure; endpoint/source/reference cap separation; theta/shear/lapse/shift/boundary/tau-mismatch component pack; same-frame denominator guard; no-cancellation Pi_Rcorner join",
            "excluded": "numeric placeholders; cancellation; fitted stationary tau; clock/lapse gauge shortcut; source cap hiding; local-GR/PPN scoring; GitHub; formalization-workbench edits",
            "claim_allowed": False,
        }
    )
    return [row]


def write_branch_copies(
    owner_rows: list[dict[str, object]],
    bridge_rows: list[dict[str, object]],
    beta_rows: list[dict[str, object]],
    dry_rows_: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
) -> list[dict[str, object]]:
    copies = [
        (
            "COPY2067_0_source_weight_tau_owner",
            SOURCE_WEIGHT_DOCS / "AFRAME_STATIONARY_TAU_OWNER_2067_CONDITIONAL_NONCLAIM.csv",
            owner_rows,
        ),
        (
            "COPY2067_1_source_weight_cap_bridge",
            SOURCE_WEIGHT_DOCS / "AFRAME_TIME_CAP_EPSILON_TAU_BRIDGE_2067_NONCLAIM.csv",
            bridge_rows,
        ),
        (
            "COPY2067_2_source_weight_beta_inputs",
            SOURCE_WEIGHT_DOCS / "AFRAME_BETA_TIME_CAPS_INPUT_PACK_2067_SOURCE_ROW_SCHEMA_NONCLAIM.csv",
            beta_rows,
        ),
        (
            "COPY2067_3_wep_dry_run",
            BRANCH_WEP / "P8_Y5_PARENT_QLOC_2067_TAU_CAP_DRY_RUN_NONCLAIM.csv",
            dry_rows_,
        ),
        (
            "COPY2067_4_queue_next",
            QUEUE / "JR2067_CCAP_OR_EPSILON_TAU_COMPONENTS_NEXT_NONCLAIM.csv",
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
    owner_rows: list[dict[str, object]],
    bridge_rows: list[dict[str, object]],
    beta_rows: list[dict[str, object]],
    dry_rows_: list[dict[str, object]],
    gates: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    source_ok = all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in sources)
    csv_ok = all(csv_rows_parse(path) for path in csv_paths)
    owner_verdict = next(row for row in owner_rows if row["row_id"] == "STO2067_7_verdict")
    owner_ok = (
        any(row["row_id"] == "STO2067_1_Killing_identity" for row in owner_rows)
        and owner_verdict["status"] == "FAIL_CURRENT_CLAIM_STATIONARY_TAU_OWNER_UNSIGNED"
        and all(not bool(row["parent_signed"]) for row in owner_rows)
    )
    bridge_verdict = next(row for row in bridge_rows if row["row_id"] == "CCB2067_5_verdict")
    bridge_ok = (
        any(row["row_id"] == "CCB2067_0_exact_current_identity" for row in bridge_rows)
        and any(row["row_id"] == "CCB2067_2_epsilon_tau_bridge" for row in bridge_rows)
        and bridge_verdict["status"] == "BOUND_BRIDGE_NONCLAIM_READY"
        and all(not bool(row["ready_for_scoring"]) for row in bridge_rows)
    )
    required_inputs = {
        "C_cap",
        "W_time_caps",
        "epsilon_nonstationary_tau",
        "theta_D_or_X_D",
        "sigma_mu_nu",
        "a_mu_and_grad_lapse",
        "shift_or_extrinsic_curvature",
        "boundary_velocity_and_reference_shift",
        "tau_source_clock_charge_orbit_boundary_mismatch",
        "same_frame_T_H_envelope",
        "M_ref_candidate",
        "B_source_caps_abs + B_ref_caps_abs",
        "beta_corner_time_caps_abs",
    }
    beta_ok = required_inputs.issubset({str(row["quantity"]) for row in beta_rows}) and all(
        bool(row["source_ready_schema"]) and not bool(row["ready_for_scoring"]) for row in beta_rows
    )
    dry_verdict = next(row for row in dry_rows_ if row["run_id"] == "RUN2067_VERDICT")
    dry_ok = dry_verdict["verdict"] == "KILLING_OWNER_FAILS_CAP_BOUND_BRIDGE_STAGED"
    gates_ok = all(row["claim_allowed"] is False for row in gates) and all(row["status"] != "PASS_CLAIM" for row in gates)
    next_ok = next_rows_[0]["target_id"] == "NEXT2067_0_2068"
    no_claim = all(
        not bool(row.get("claim_allowed", False)) and not bool(row.get("valid_for_claim", False))
        for group in [sources, owner_rows, bridge_rows, beta_rows, dry_rows_, gates, next_rows_]
        for row in group
    )
    checks: list[tuple[str, bool, str]] = []
    checks.append(("VAL2067_00_local_sources_exist", source_ok, "all cited source paths and needles exist"))
    checks.append(("VAL2067_01_csv_parse", csv_ok, "all generated CSV files parse cleanly"))
    checks.append(("VAL2067_02_tau_owner", owner_ok, "stationary tau/Killing owner attempted and correctly refused"))
    checks.append(("VAL2067_03_cap_bridge", bridge_ok, "epsilon_tau to beta_time_caps bridge is written but nonclaim"))
    checks.append(("VAL2067_04_beta_inputs", beta_ok, "beta_time_caps input pack contains all required unscored rows"))
    checks.append(("VAL2067_05_dry_verdict", dry_ok, "dry run refuses zero claim and stages cap bound bridge"))
    checks.append(("VAL2067_06_claim_gates_blocked", gates_ok, "all claim gates remain blocked/nonclaim"))
    checks.append(("VAL2067_07_next_selected", next_ok, "2068 C_cap or epsilon_tau component target selected"))
    checks.append(("VAL2067_08_no_claim_flags", no_claim, "no generated row allows a claim"))
    checks.append(("VAL2067_09_formalization_unchanged", count_formalization_modified() == 0, "formalization-workbench modified-file count remains 0"))
    checks.append(("VAL2067_10_no_formalization_artifacts", not formalization_has_2067_artifacts(), "no 2067 artifacts were written under formalization-workbench"))
    checks.append(("VAL2067_11_no_pycache", not scripts_pycache_exists(), "scripts __pycache__ removed"))
    overall = all(ok for _, ok, _ in checks)
    checks.append(("VAL2067_OVERALL", overall, "2067 refuses the Killing shortcut and creates a sourceable time-cap residual bridge"))
    rows: list[dict[str, object]] = []
    for check_id, ok, detail in checks:
        row = base_row()
        row.update({"check_id": check_id, "status": "PASS" if ok else "FAIL", "detail": detail, "claim_allowed": False})
        rows.append(row)
    return rows


def write_doc(
    sources: list[dict[str, object]],
    owner_rows: list[dict[str, object]],
    bridge_rows: list[dict[str, object]],
    beta_rows: list[dict[str, object]],
    dry_rows_: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    sections = [
        "# 2067 Y5 R2FR Stationary Tau Killing Owner Or Beta Time Caps Bound",
        "",
        "## Current Verdict",
        "",
        "2067 tries the honest theorem route first: make `tau_obs` a parent-owned stationary/Killing generator for `SURF_PPN_STAT_ANNULUS_2066`. The exact current identity is available, but the owner theorem still does not close because the parent tau owner, same-tau lock, mass-channel Hilbert conservation, local domain/source owner, exterior operator status, and boundary/reference lock remain unsigned.",
        "",
        "The useful gain is that the time-cap problem is now converted into a boundable current leakage. The bridge is `beta_corner_time_caps_abs <= C_cap * epsilon_nonstationary_tau * W_time_caps + B_source_caps_abs + B_ref_caps_abs`, with an absolute-value/no-cancellation join into `Pi_R^corner_abs`.",
        "",
        "This does not yet score. `C_cap`, `W_time_caps`, the source/reference cap separation, the same-frame stress/symgrad numerator, and the positive denominator are missing. But the fallback is no longer philosophical; it is a concrete source-input pack.",
        "",
        "No local-GR/Newton, Cassini, PPN, R10, clock, orbital, corner-zero, or finite-residual claim is allowed. No GitHub action and no `formalization-workbench` edit is made.",
        "",
        "## Source Register",
        md_table(sources, ["source_id", "source_kind", "source_path", "status", "note", "valid_for_claim"]),
        "## Stationary Tau Owner Attempt",
        md_table(owner_rows, ["row_id", "object_id", "required_identity", "implication", "status", "note", "parent_signed", "claim_allowed"]),
        "## Cap Current Bridge",
        md_table(bridge_rows, ["row_id", "quantity", "formula", "derivation_source", "status", "note", "ready_for_scoring", "claim_allowed"]),
        "## Beta Time Caps Input Pack",
        md_table(beta_rows, ["row_id", "quantity", "definition", "units", "required_input", "blocker", "source_ready_schema", "ready_for_scoring", "claim_allowed"]),
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
    owner_rows = tau_owner_attempt_rows()
    bridge_rows = cap_current_bridge_rows()
    beta_rows = beta_time_caps_input_rows()
    dry_rows_ = dry_run_rows(owner_rows, bridge_rows, beta_rows)
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows_ = next_target_rows()
    paths = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2067_SOURCE_REGISTER.csv",
        "owner": OUT / "P8_Y5_PARENT_QLOC_2067_STATIONARY_TAU_OWNER_ATTEMPT.csv",
        "bridge": OUT / "P8_Y5_PARENT_QLOC_2067_CAP_CURRENT_BRIDGE.csv",
        "beta": OUT / "P8_Y5_PARENT_QLOC_2067_BETA_TIME_CAPS_INPUT_PACK.csv",
        "dry": OUT / "P8_Y5_PARENT_QLOC_2067_DRY_RUN.csv",
        "gates": OUT / "P8_Y5_PARENT_QLOC_2067_CLAIM_GATE.csv",
        "decision": OUT / "P8_Y5_PARENT_QLOC_2067_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2067_NEXT_TARGET.csv",
        "branch": OUT / "P8_Y5_PARENT_QLOC_2067_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2067_VALIDATION.csv",
    }
    write_csv(paths["sources"], sources)
    write_csv(paths["owner"], owner_rows)
    write_csv(paths["bridge"], bridge_rows)
    write_csv(paths["beta"], beta_rows)
    write_csv(paths["dry"], dry_rows_)
    write_csv(paths["gates"], gates)
    write_csv(paths["decision"], decisions)
    write_csv(paths["next"], next_rows_)
    copies = write_branch_copies(owner_rows, bridge_rows, beta_rows, dry_rows_, next_rows_)
    write_csv(paths["branch"], copies)
    remove_pycache()
    csv_paths_without_validation = [path for key, path in paths.items() if key != "validation"] + [Path(row["path"]) for row in copies]
    validation = validation_rows(sources, owner_rows, bridge_rows, beta_rows, dry_rows_, gates, next_rows_, csv_paths_without_validation)
    write_csv(paths["validation"], validation)
    csv_paths = list(paths.values()) + [Path(row["path"]) for row in copies]
    remove_pycache()
    validation = validation_rows(sources, owner_rows, bridge_rows, beta_rows, dry_rows_, gates, next_rows_, csv_paths)
    write_csv(paths["validation"], validation)
    write_doc(sources, owner_rows, bridge_rows, beta_rows, dry_rows_, gates, decisions, next_rows_, copies, validation)
    remove_pycache()


if __name__ == "__main__":
    main()
