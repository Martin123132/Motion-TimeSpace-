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
    read_csv,
    read_text,
    remove_pycache,
    write_csv,
)


DOC = ROOT / "2052-Y5-R2FR-finite-RAB-residual-source-acquisition-and-bound-runner.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"


def formalization_has_2052_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    try:
        patterns = (
            "*2052-Y5-R2FR*",
            "*P8_Y5_PARENT_QLOC_2052*",
            "*Y5_R2FR_finite_RAB_residual_source_acquisition_and_bound_runner_2052*",
        )
        return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))
    except Exception:
        return False


def scripts_pycache_exists() -> bool:
    return (SCRIPT_PATH.parent / "__pycache__").exists()


def has_missing_marker(path: Path) -> bool:
    if not path.exists():
        return True
    return "MISSING_" in read_text(path)


def numeric_positive(value: object) -> bool:
    try:
        return float(str(value)) > 0.0
    except Exception:
        return False


def csv_positive_columns(path: Path, *columns: str) -> bool:
    if not path.exists():
        return False
    try:
        rows = read_csv(path)
    except Exception:
        return False
    if not rows:
        return False
    return all(all(numeric_positive(row.get(column, "")) for column in columns) for row in rows)


def source_register_rows() -> list[dict[str, object]]:
    specs = [
        (
            "SRC2052_00_2051_doc",
            DOC.parent / "2051-Y5-R2FR-lambdaR-origin-or-QR-nocharge-certificate.md",
            ["NEXT2051_0_2052", "FINITE_RAB_ACQUISITION_SELECTED_NONCLAIM"],
            "2051 proof-first result and handoff into finite R_AB acquisition.",
        ),
        (
            "SRC2052_01_2051_queue",
            OUT / "P8_Y5_PARENT_QLOC_2051_FINITE_RESIDUAL_ACQUISITION_QUEUE.csv",
            ["FACQ2051_5_tau_PPN", "FACQ2051_6_tau_R10", "FACQ2051_8_tau_orbital"],
            "machine-readable finite residual acquisition rows.",
        ),
        (
            "SRC2052_02_finite_bound_schema",
            QUEUE / "JR1736_FINITE_BOUND_SCHEMA.csv",
            ["MISSING_PARENT_TAU", "MISSING_NUMERIC_OR_THEOREM_ZERO"],
            "older finite-bound schema proving the runner must refuse placeholders.",
        ),
        (
            "SRC2052_03_arena_product_map",
            QUEUE / "JR1701_ARENA_FINITE_PRODUCT_MAP.csv",
            ["FPM1701_3_R10_alpha_lambda", "FPM1701_4_PPN_frame_vector", "FPM1701_5_orbital_GM_source"],
            "cross-arena finite product map.",
        ),
        (
            "SRC2052_04_residual_requirements",
            QUEUE / "JR1863_P8_Y5_PARENT_QLOC_1863_FINITE_RESIDUAL_REQUIREMENTS.csv",
            ["FRR1863_1_arena_projections", "MISSING_ARENA_PROJECTIONS", "POLICY_ACTIVE"],
            "finite residual requirement contract.",
        ),
        (
            "SRC2052_05_zrjr_intake",
            QUEUE / "JR1867_P8_Y5_PARENT_QLOC_1867_FINITE_ZRJR_INTAKE_ROWS.csv",
            ["FINT1867_6_tau_R10", "FINT1867_7_tau_PPN", "FINT1867_9_tau_orbital"],
            "finite Z_R/J_R/tau arena input rows.",
        ),
        (
            "SRC2052_06_r10_bound_pack",
            OUT / "P8_Y5_PARENT_QLOC_1688_R10_BULK_BOUND_DATA_PACK.csv",
            ["RDP1688_6_live_curve", "R10 full bound curve"],
            "R10 bulk bound data pack.",
        ),
        (
            "SRC2052_07_r10_template_doc",
            ROOT / "1689-Y5-R2FR-bulk-alpha-template-beta-kernel-tail-fill-or-r10-curve-digitization.md",
            ["MTS-side comparator row now exists", "full digitized `alpha_bound(lambda)` curve is missing"],
            "R10 MTS-side comparator template and external curve blocker.",
        ),
        (
            "SRC2052_08_r10_anchor_bound",
            LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_ANCHOR_SMOKE.csv",
            ["R10_ANCHOR_EOTWASH_2020_ALPHA1_38P6UM", "3.86e-5"],
            "source-backed R10 anchor rows only.",
        ),
        (
            "SRC2052_09_r10_live_curve",
            LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_DIGITIZED.csv",
            ["MISSING_DIGITIZED_ALPHA_BOUND", "MISSING_NUMERIC_LAMBDA"],
            "live full R10 curve remains placeholder-blocked.",
        ),
        (
            "SRC2052_10_r10_vector_candidate",
            LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_VECTOR_2020_REVIEW_CANDIDATE.csv",
            ["R10_VECTOR_2020_REVIEW", "Lee_Adelberger_Cook_Fleischer_Heckel_2020"],
            "vector review candidate curve, not live claim curve.",
        ),
        (
            "SRC2052_11_ppn_sources",
            OUT / "P8_Y5_PARENT_QLOC_1643_EXTERNAL_PPN_SOURCE_REGISTER.csv",
            ["EXT1643_0_Cassini_gamma", "10.1038/nature01997"],
            "external PPN gamma source register.",
        ),
        (
            "SRC2052_12_ppn_runner",
            OUT / "P8_Y5_PARENT_QLOC_1643_NORMALIZED_PPN_BOUND_RUNNER.csv",
            ["RUN1643_2_gamma_bound_inversion", "RUN1643_3_R10_guard"],
            "normalized PPN runner and R10 guard.",
        ),
        (
            "SRC2052_13_ppn_bound_inputs",
            OUT / "P8_Y5_PARENT_QLOC_1640_NORMALIZED_PPN_BOUND_INPUTS.csv",
            ["NPPN1640_0_PiR_abs", "NPPN1640_3_gamma_bound"],
            "PPN finite q_R/Pi_R input blockers.",
        ),
        (
            "SRC2052_14_multiarena_pack",
            OUT / "P8_Y5_PARENT_QLOC_1735_PPN_WEP_CLOCK_ORBIT_SOURCE_PACK_TEMPLATE.csv",
            ["R2_clock_redshift", "R3_gamma", "R4_beta"],
            "PPN/clock/orbit source-pack template.",
        ),
        (
            "SRC2052_15_clock_projection",
            OUT / "P8_Y5_PARENT_QLOC_1804_CLOCK_PROJECTION_ROWS.csv",
            ["CLK1804_0_CAS646_0_AlHg", "CLK1804_2_clock_redshift_anchor"],
            "clock sensitivity/projection rows.",
        ),
        (
            "SRC2052_16_clock_bound",
            OUT / "P8_Y5_PARENT_QLOC_1809_ALPHA_CLOCK_PRODUCT_BOUND_LEDGER.csv",
            ["ACB1809_2", "best_current"],
            "clock product bound ledger.",
        ),
        (
            "SRC2052_17_orbital_formula",
            OUT / "P8_Y5_GAUSS_ORBITAL_FORMULA_LEDGER.csv",
            ["GO523_5_no_cancellation_bound", "GO523_6_PPN_residual_vector"],
            "source-normalized Newton/orbital residual formula ledger.",
        ),
        (
            "SRC2052_18_orbital_gates",
            OUT / "P8_Y5_GAUSS_ORBITAL_ACCEPTANCE_GATES.csv",
            ["AG523_3_residual_scorecard_scored", "AG523_5_no_overclaim"],
            "orbital acceptance gates.",
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
            }
        )
        rows.append(row)
    return rows


def empirical_bound_status_rows() -> list[dict[str, object]]:
    anchor_path = LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_ANCHOR_SMOKE.csv"
    live_curve_path = LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_DIGITIZED.csv"
    vector_candidate_path = LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_VECTOR_2020_REVIEW_CANDIDATE.csv"
    rowspecs = [
        (
            "EBS2052_0_PPN_gamma",
            "PPN",
            "gamma_minus_1",
            "2.3e-5 source-pack row; 6.7e-5 conservative inversion row in 1643",
            "dimensionless",
            OUT / "P8_Y5_PARENT_QLOC_1643_EXTERNAL_PPN_SOURCE_REGISTER.csv",
            "SOURCE_BACKED_EXTERNAL_BOUND_AVAILABLE",
            "usable as a bound only after tau_PPN/q_R/profile convention is supplied",
        ),
        (
            "EBS2052_1_PPN_beta",
            "PPN_orbital",
            "beta_minus_1",
            "7.8e-5 source-pack template row",
            "dimensionless",
            OUT / "P8_Y5_PARENT_QLOC_1735_PPN_WEP_CLOCK_ORBIT_SOURCE_PACK_TEMPLATE.csv",
            "TEMPLATE_EXTERNAL_BOUND_AVAILABLE",
            "not first target because beta needs second-order/source/operator bridge",
        ),
        (
            "EBS2052_2_R10_anchor",
            "R10",
            "alpha(lambda) anchor",
            "alpha=1 at lambda=38.6 um plus 56 um continuity anchor",
            "dimensionless alpha, metres lambda",
            anchor_path,
            "ANCHOR_ONLY_NONCURVE_SOURCE_BACKED",
            "use for smoke/provenance only, not dense curve scoring",
        ),
        (
            "EBS2052_3_R10_live_curve",
            "R10",
            "alpha_bound(lambda) live curve",
            "MISSING_DIGITIZED_ALPHA_BOUND",
            "dimensionless alpha, metres lambda",
            live_curve_path,
            "PLACEHOLDER_BLOCKED",
            "not scoreable until dense positive numeric curve is promoted",
        ),
        (
            "EBS2052_4_R10_vector_candidate",
            "R10",
            "alpha_bound(lambda) vector review candidate",
            "dense positive review candidate from 2020 figure",
            "dimensionless alpha, metres lambda",
            vector_candidate_path,
            "REVIEW_CANDIDATE_NOT_PROMOTED",
            "can test runner plumbing but cannot be a live claim curve without QA/promotion",
        ),
        (
            "EBS2052_5_clock_product",
            "clock",
            "b_alpha*tau_clock product",
            "best imported product bound 3.2e-18 yr^-1 two-sigma",
            "yr^-1 product",
            OUT / "P8_Y5_PARENT_QLOC_1809_ALPHA_CLOCK_PRODUCT_BOUND_LEDGER.csv",
            "SOURCE_BACKED_PRODUCT_BOUND_AVAILABLE",
            "bounds EM-constant product, not pure R_AB without b_alpha/tau_clock map",
        ),
        (
            "EBS2052_6_orbital_newton",
            "orbital",
            "epsilon_SN and PPN residual vector",
            "formula ledger and gates available, no numeric residual score",
            "dimensionless residual",
            OUT / "P8_Y5_GAUSS_ORBITAL_FORMULA_LEDGER.csv",
            "FORMULA_AND_GATE_AVAILABLE_BOUND_NOT_DIRECT",
            "requires source-normalized Newton/GM chain and no-cancellation scorecard",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, arena, observable, empirical_bound, units, source_path, status, limitation in rowspecs:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "arena": arena,
                "observable": observable,
                "empirical_bound_or_status": empirical_bound,
                "units": units,
                "source_path": str(source_path),
                "source_exists": source_path.exists(),
                "source_status": status,
                "limitation": limitation,
                "usable_for_MTS_score_now": False,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def residual_input_schema_rows() -> list[dict[str, object]]:
    data = [
        ("RIN2052_0_C_R_profile", "C_R(r)=ln(T^2S)", "finite reciprocal profile", "profile, theorem-zero, or parent Euler difference", "MISSING_PROFILE_OR_PARENT_EQUATION", "PPN;clock;orbital"),
        ("RIN2052_1_q_R_hat", "q_R_hat/Q_R", "exterior reciprocal hair amplitude", "source-backed value, theorem-zero, or boundary momentum relation", "MISSING_QR_VALUE_OR_ZERO_THEOREM", "PPN;R10;clock;orbital"),
        ("RIN2052_2_J_R", "J_R/S_R", "source drive/source balance", "matter descent map or finite source row", "MISSING_PARENT_SOURCE_MAP", "Newton;PPN;orbital"),
        ("RIN2052_3_Pi_R", "Pi_R/B_R", "boundary reciprocal momentum/tail", "boundary variation class or numeric bound", "MISSING_BOUNDARY_VARIATION_CLASS", "PPN;clock;orbital;R10"),
        ("RIN2052_4_W_R", "W_R", "reciprocal strain weight", "positive parent coefficient and normalization", "MISSING_PARENT_SIGN_AND_NORMALIZATION", "stability;current"),
        ("RIN2052_5_tau_PPN", "tau_PPN_R", "projection into gamma/beta/preferred-frame residuals", "explicit map from C_R/q_R to PPN vector", "MISSING_PPN_PROJECTION", "PPN"),
        ("RIN2052_6_tau_R10", "tau_R10_R", "projection into Yukawa alpha(lambda)", "finite-range carrier/kernel/material pair map", "MISSING_R10_PROJECTION", "R10"),
        ("RIN2052_7_tau_clock", "tau_clock_R", "projection into clock/redshift residuals", "clock sensitivity/product map tied to R_AB", "MISSING_CLOCK_PROJECTION", "clock"),
        ("RIN2052_8_tau_orbital", "tau_orbital_R", "projection into acceleration/precession residuals", "source-normalized Newton/orbital map", "MISSING_ORBITAL_PROJECTION", "orbital"),
        ("RIN2052_9_no_cancel", "absolute residual vector", "no hidden cancellation policy", "componentwise bounds or theorem-zero per component", "POLICY_ACTIVE_NOT_SCORE", "all"),
    ]
    rows: list[dict[str, object]] = []
    for row_id, symbol, role, required_source, current_status, arena_links in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "symbol": symbol,
                "role": role,
                "required_source": required_source,
                "current_status": current_status,
                "arena_links": arena_links,
                "numeric_or_theorem_zero": False,
                "ready_for_scoring": False,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def arena_projection_rows() -> list[dict[str, object]]:
    data = [
        (
            "APR2052_0_PPN_gamma",
            "PPN_gamma",
            "Delta_gamma_R = tau_PPN_R*q_R_hat + tail_R + gauge_readout_R",
            "Cassini gamma source exists",
            "q_R_hat;tau_PPN_R;tail_R;gauge_readout_R;same-frame convention",
            "FIRST_LOCAL_GR_BOUND_TARGET_NONCLAIM",
            "closest direct test of time-radial local-GR recovery",
        ),
        (
            "APR2052_1_PPN_beta",
            "PPN_beta",
            "Delta_beta_R = tau_beta_R*q_R_hat + second_order_source_R + operator_tail_R",
            "beta source-pack template exists",
            "q_R_hat;tau_beta_R;second-order source map;operator tail",
            "SECOND_STAGE_AFTER_GAMMA",
            "more GR-like but depends on second-order/source closure",
        ),
        (
            "APR2052_2_R10",
            "R10_alpha_lambda",
            "alpha_R10(lambda)=K_R(lambda)*beta_source_R*beta_test_R + epsilon_tail(lambda)",
            "anchor and vector candidate exist; live curve placeholder",
            "full bound curve;K_R;beta_source_R;beta_test_R;finite range lambda_R",
            "BLOCKED_BY_CURVE_AND_THEORY_LEGS",
            "use only after finite-range projection exists",
        ),
        (
            "APR2052_3_clock",
            "clock_redshift_or_constants",
            "Delta_clock = tau_clock_R*q_R_hat + b_alpha*tau_alpha + b_mu*tau_mu",
            "clock product bounds and sensitivities exist",
            "pure R_AB-to-clock map;b_alpha/b_mu ownership;clock convention",
            "BLOCKED_BY_PRODUCT_DECOMPOSITION",
            "good cross-check, not the first local-GR gate",
        ),
        (
            "APR2052_4_orbital",
            "orbital_Newton_GM",
            "epsilon_SN = epsilon_charge + epsilon_Poisson + epsilon_Gauss + epsilon_orbit + epsilon_extra + epsilon_PPN",
            "Gauss/orbital formula and gates exist",
            "source-normalized GM chain;orbital projection;component values",
            "BLOCKED_BY_FULL_NEWTON_CHAIN",
            "important for Newton reduction after PPN gamma map",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, arena, projection_formula, empirical_side, required_inputs, status, reason in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "arena": arena,
                "projection_formula": projection_formula,
                "empirical_side": empirical_side,
                "required_inputs": required_inputs,
                "status": status,
                "reason": reason,
                "projection_ready": False,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def bound_runner_rows(arena_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    verdict_by_arena = {
        "PPN_gamma": ("REJECTED_PPN_PROJECTION_MISSING", "external gamma bound exists but q_R_hat/tau_PPN/profile convention is missing"),
        "PPN_beta": ("REJECTED_SECOND_ORDER_SOURCE_MAP_MISSING", "beta needs second-order source/operator projection after gamma"),
        "R10_alpha_lambda": ("REJECTED_R10_CURVE_AND_THEORY_LEGS_MISSING", "live full curve is placeholder and MTS finite-range alpha legs are missing"),
        "clock_redshift_or_constants": ("REJECTED_CLOCK_PRODUCT_DECOMPOSITION_MISSING", "clock product bounds exist but pure R_AB clock map is not separated"),
        "orbital_Newton_GM": ("REJECTED_ORBITAL_GM_CHAIN_MISSING", "orbital formulas exist but source-normalized GM residual inputs are unfilled"),
    }
    rows: list[dict[str, object]] = []
    for arena_row in arena_rows:
        arena = str(arena_row["arena"])
        verdict, reason = verdict_by_arena[arena]
        row = base_row()
        row.update(
            {
                "run_id": "RUN_" + str(arena_row["row_id"]),
                "arena": arena,
                "projection_ready": arena_row["projection_ready"],
                "external_bound_available": arena in {"PPN_gamma", "PPN_beta", "clock_redshift_or_constants"},
                "accepted_for_scoring": False,
                "verdict": verdict,
                "reason": reason,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    overall = base_row()
    overall.update(
        {
            "run_id": "RUN2052_VERDICT",
            "arena": "all_local_finite_RAB",
            "projection_ready": False,
            "external_bound_available": True,
            "accepted_for_scoring": False,
            "verdict": "FINITE_RAB_BOUND_RUNNER_BUILT_ALL_ARENAS_BLOCKED_NONCLAIM",
            "reason": "runner separates external empirical locks from missing MTS finite residual/projection rows; PPN_gamma selected as first local-GR bound target",
            "claim_allowed": False,
        }
    )
    rows.append(overall)
    return rows


def priority_rows() -> list[dict[str, object]]:
    data = [
        (
            "PRI2052_0_PPN_gamma",
            "PPN_gamma",
            "SELECT_FIRST",
            "directly tests local GR time-radial recovery and already has source-backed external gamma bound",
            "derive C_R/q_R -> gamma_minus_1 map or produce first finite q_R bound row",
        ),
        (
            "PRI2052_1_clock",
            "clock",
            "SECONDARY_CROSS_CHECK",
            "external clock product rows exist, but they constrain constant-sector products rather than pure R_AB",
            "use after b_alpha/b_mu and tau_clock_R ownership are separated",
        ),
        (
            "PRI2052_2_R10",
            "R10",
            "DEFER_UNTIL_FINITE_RANGE_OR_CURVE",
            "R10 has useful anchors and vector candidate but live full curve and finite-range theory legs are blocked",
            "reopen once lambda_R/tau_R10/K_R or promoted curve exists",
        ),
        (
            "PRI2052_3_orbital",
            "orbital_Newton_GM",
            "DEFER_UNTIL_GAMMA_AND_GM_CHAIN",
            "orbital route is essential for Newton reduction but has the broadest source-normalization chain",
            "use after PPN gamma map and source-normalized GM rows are filled",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, arena, priority, reason, next_action in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "arena": arena,
                "priority": priority,
                "reason": reason,
                "next_action": next_action,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def claim_gate_rows() -> list[dict[str, object]]:
    data = [
        ("GATE2052_0_sources_loaded", "finite residual source and empirical-bound ledgers loaded", "PASS_NONCLAIM", "sources exist and runner can see the arena blockers"),
        ("GATE2052_1_external_bounds_separated", "external empirical locks are separated from MTS prediction rows", "PASS_NONCLAIM", "prevents treating source-backed bounds as theory success"),
        ("GATE2052_2_no_missing_scored", "no MISSING_* row accepted for scoring", "PASS_NONCLAIM", "runner refuses all placeholder/theory-missing rows"),
        ("GATE2052_3_PPN_first", "PPN gamma selected as first finite local-GR residual target", "PASS_NONCLAIM", "best next move toward derivable GR reduction"),
        ("GATE2052_4_RAB_zero_claim", "R_AB=0/p=1/beta=1/local GR claimed", "FAIL_BLOCKED", "zero theorem and finite residual score remain absent"),
        ("GATE2052_5_R10_claim", "R10 finite residual pass claimed", "FAIL_BLOCKED", "full curve and theory-side alpha legs missing"),
        ("GATE2052_6_Newton_or_orbital_claim", "source-normalized Newton/orbital pass claimed", "FAIL_BLOCKED", "GM/source-normalization residual scorecard unfilled"),
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
            "DEC2052_0_runner_status",
            "The finite R_AB runner now exists but scores nothing.",
            "This is the correct state: empirical locks exist, but MTS finite residual/projection rows are still missing.",
        ),
        (
            "DEC2052_1_best_attack",
            "Attack PPN gamma first.",
            "Gamma is the shortest bridge from R_AB=time-radial mismatch to GR recovery; it needs fewer external-data repairs than R10 and fewer source-chain repairs than orbits.",
        ),
        (
            "DEC2052_2_R10_status",
            "R10 remains useful but not first for local GR.",
            "The anchor/vector data are good plumbing, but the live curve and finite-range theory legs are still blockers.",
        ),
        (
            "DEC2052_3_orbital_status",
            "Orbital/Newton reduction is still a main goal, but after the first local PPN map.",
            "Newtonian GM needs source-normalization and no-cancellation rows; gamma gives a cleaner first residual vector.",
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
            "target_id": "NEXT2052_0_2053",
            "target_doc": "2053-Y5-R2FR-PPN-gamma-map-from-RAB-profile-or-finite-qR-first-bound.md",
            "objective": "derive the explicit map from finite C_R/q_R/R_AB hair into PPN gamma_minus_1, or produce the first source-backed nonclaim q_R bound row from Cassini without claiming local GR",
            "must_include": "C_R weak-field normalization; q_R convention; tau_PPN_R map; gauge/readout guard; Cassini bound import; no-cancellation policy; runner refusal/pass logic",
            "excluded": "assuming gamma_minus_1=q_R without derivation; using R_AB=0 closure; scoring missing q_R; claiming beta/local GR/Newton; GitHub; formalization-workbench edits",
            "claim_allowed": False,
        }
    )
    return [row]


def write_branch_copies(
    residual_rows: list[dict[str, object]],
    arena_rows: list[dict[str, object]],
    runner_rows_: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
) -> list[dict[str, object]]:
    copies = [
        (
            "COPY2052_0_source_weight_residual_schema",
            SOURCE_WEIGHT_DOCS / "AFRAME_FINITE_RAB_RESIDUAL_SCHEMA_2052_NONCLAIM.csv",
            residual_rows,
        ),
        (
            "COPY2052_1_wep_arena_projection",
            BRANCH_WEP / "P8_Y5_PARENT_QLOC_2052_FINITE_RAB_ARENA_PROJECTION_NONCLAIM.csv",
            arena_rows,
        ),
        (
            "COPY2052_2_wep_runner",
            BRANCH_WEP / "P8_Y5_PARENT_QLOC_2052_FINITE_RAB_BOUND_RUNNER_NONCLAIM.csv",
            runner_rows_,
        ),
        (
            "COPY2052_3_rab_next",
            QUEUE / "JR2052_PPN_GAMMA_FIRST_FINITE_QR_BOUND_NEXT_NONCLAIM.csv",
            next_rows_,
        ),
    ]
    rows: list[dict[str, object]] = []
    for copy_id, path, data in copies:
        write_csv(path, data)
        row = base_row()
        row.update({"copy_id": copy_id, "path": str(path), "rows": len(data), "status": "WRITTEN_NONCLAIM_COPY"})
        rows.append(row)
    return rows


def validation_rows(
    sources: list[dict[str, object]],
    empirical_bounds: list[dict[str, object]],
    residual_inputs: list[dict[str, object]],
    arena_rows: list[dict[str, object]],
    runner_rows_: list[dict[str, object]],
    priority: list[dict[str, object]],
    gates: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    source_ok = all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in sources)
    csv_ok = all(csv_rows_parse(path) for path in csv_paths)
    anchor_numeric = csv_positive_columns(LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_ANCHOR_SMOKE.csv", "lambda_value", "alpha_bound")
    live_curve_blocked = has_missing_marker(LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_DIGITIZED.csv")
    vector_candidate_positive = csv_positive_columns(LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_VECTOR_2020_REVIEW_CANDIDATE.csv", "lambda_value", "alpha_bound")
    no_missing_scored = all(not bool(row.get("ready_for_scoring", False)) for row in residual_inputs) and all(not bool(row.get("accepted_for_scoring", False)) for row in runner_rows_)
    ppn_selected = next(row for row in priority if row["row_id"] == "PRI2052_0_PPN_gamma")["priority"] == "SELECT_FIRST"
    runner_verdict = next(row for row in runner_rows_ if row["run_id"] == "RUN2052_VERDICT")
    rab_gate = next(row for row in gates if row["row_id"] == "GATE2052_4_RAB_zero_claim")
    r10_gate = next(row for row in gates if row["row_id"] == "GATE2052_5_R10_claim")
    external_bounds_split = any(row["source_status"] == "SOURCE_BACKED_EXTERNAL_BOUND_AVAILABLE" for row in empirical_bounds) and any(
        row["source_status"] == "PLACEHOLDER_BLOCKED" for row in empirical_bounds
    )
    required_arenas = {"PPN_gamma", "R10_alpha_lambda", "clock_redshift_or_constants", "orbital_Newton_GM"}
    arena_coverage = required_arenas.issubset({str(row["arena"]) for row in arena_rows})
    checks: list[tuple[str, bool, str]] = []
    checks.append(("VAL2052_00_local_sources_exist", source_ok, "all cited local source paths and needles exist"))
    checks.append(("VAL2052_01_csv_parse", csv_ok, "all generated CSV files parse cleanly"))
    checks.append(("VAL2052_02_anchor_rows_positive", anchor_numeric, "R10 anchor rows have positive numeric lambda and alpha"))
    checks.append(("VAL2052_03_live_curve_blocked", live_curve_blocked, "live R10 curve still contains MISSING markers and is blocked"))
    checks.append(("VAL2052_04_vector_candidate_positive_nonclaim", vector_candidate_positive, "R10 vector candidate is numeric but remains nonclaim"))
    checks.append(("VAL2052_05_external_bounds_split", external_bounds_split, "external empirical bounds are separated from MTS prediction readiness"))
    checks.append(("VAL2052_06_no_missing_scored", no_missing_scored, "no missing residual/projection row is accepted for scoring"))
    checks.append(("VAL2052_07_arena_coverage", arena_coverage, "PPN, R10, clock and orbital arenas are covered"))
    checks.append(("VAL2052_08_ppn_gamma_selected", ppn_selected, "PPN gamma selected as first finite local-GR residual target"))
    checks.append(("VAL2052_09_runner_blocks_claims", runner_verdict["verdict"] == "FINITE_RAB_BOUND_RUNNER_BUILT_ALL_ARENAS_BLOCKED_NONCLAIM", "runner built and blocks all claims"))
    checks.append(("VAL2052_10_RAB_zero_blocked", rab_gate["status"] == "FAIL_BLOCKED", "R_AB=0/local-GR claim remains blocked"))
    checks.append(("VAL2052_11_R10_claim_blocked", r10_gate["status"] == "FAIL_BLOCKED", "R10 claim remains blocked"))
    checks.append(("VAL2052_12_next_selected", next_rows_[0]["target_id"] == "NEXT2052_0_2053", "2053 PPN-gamma first-bound target selected"))
    checks.append(("VAL2052_13_formalization_unchanged", count_formalization_modified() == 0, "formalization-workbench modified-file count remains 0"))
    checks.append(("VAL2052_14_no_formalization_2052_artifacts", not formalization_has_2052_artifacts(), "no 2052 artifacts were written under formalization-workbench"))
    checks.append(("VAL2052_15_no_pycache", not scripts_pycache_exists(), "scripts __pycache__ removed"))
    overall = all(ok for _, ok, _ in checks)
    checks.append(("VAL2052_OVERALL", overall, "2052 builds the finite R_AB bound runner, blocks claims, and selects PPN gamma as the next target"))
    rows: list[dict[str, object]] = []
    for check_id, ok, detail in checks:
        row = base_row()
        row.update({"check_id": check_id, "status": "PASS" if ok else "FAIL", "detail": detail, "claim_allowed": False})
        rows.append(row)
    return rows


def write_doc(
    sources: list[dict[str, object]],
    empirical_bounds: list[dict[str, object]],
    residual_inputs: list[dict[str, object]],
    arena_rows: list[dict[str, object]],
    runner_rows_: list[dict[str, object]],
    priority: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    sections = [
        "# 2052 Y5 R2FR Finite R_AB Residual Source Acquisition And Bound Runner",
        "",
        "## Current Verdict",
        "",
        "2052 converts the post-`lambda_R`/`Q_R` obstruction into a runner-shaped finite-residual programme. The important move is separation: external empirical locks exist in several arenas, but they are not MTS success until the finite `R_AB` residual, projection kernels, units, source paths and no-cancellation policy are supplied.",
        "",
        "The runner scores nothing yet. That is the point. It refuses placeholders, keeps R10/clocks/orbits alive, and selects PPN gamma as the first serious local-GR residual target because `gamma-1` is the shortest bridge from time-radial mismatch to the question we actually care about: does the local branch reduce to GR/Newton rather than merely mimic a rotation-curve phenomenology?",
        "",
        "No `R_AB=0`, `p=1`, `beta=1`, local-GR, Newton, PPN, R10, clock or orbital pass is claimed. No GitHub action and no `formalization-workbench` edits are made.",
        "",
        "## Source Register",
        md_table(sources, ["source_id", "source_kind", "source_path", "status", "note", "valid_for_claim"]),
        "## Empirical Bound Status",
        md_table(empirical_bounds, ["row_id", "arena", "observable", "empirical_bound_or_status", "units", "source_status", "usable_for_MTS_score_now", "limitation", "claim_allowed"]),
        "## Finite Residual Input Schema",
        md_table(residual_inputs, ["row_id", "symbol", "role", "required_source", "current_status", "arena_links", "ready_for_scoring", "claim_allowed"]),
        "## Arena Projection Map",
        md_table(arena_rows, ["row_id", "arena", "projection_formula", "empirical_side", "required_inputs", "status", "projection_ready", "reason", "claim_allowed"]),
        "## Bound Runner",
        md_table(runner_rows_, ["run_id", "arena", "external_bound_available", "projection_ready", "accepted_for_scoring", "verdict", "reason", "claim_allowed"]),
        "## Arena Priority",
        md_table(priority, ["row_id", "arena", "priority", "reason", "next_action", "claim_allowed"]),
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
    empirical_bounds = empirical_bound_status_rows()
    residual_inputs = residual_input_schema_rows()
    arena_rows = arena_projection_rows()
    runner_rows_ = bound_runner_rows(arena_rows)
    priority = priority_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows_ = next_target_rows()
    paths = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2052_SOURCE_REGISTER.csv",
        "empirical": OUT / "P8_Y5_PARENT_QLOC_2052_EMPIRICAL_BOUND_STATUS.csv",
        "residual": OUT / "P8_Y5_PARENT_QLOC_2052_FINITE_RAB_RESIDUAL_INPUT_SCHEMA.csv",
        "arena": OUT / "P8_Y5_PARENT_QLOC_2052_ARENA_PROJECTION_MAP.csv",
        "runner": OUT / "P8_Y5_PARENT_QLOC_2052_BOUND_RUNNER.csv",
        "priority": OUT / "P8_Y5_PARENT_QLOC_2052_ARENA_PRIORITY.csv",
        "gates": OUT / "P8_Y5_PARENT_QLOC_2052_CLAIM_GATE.csv",
        "decision": OUT / "P8_Y5_PARENT_QLOC_2052_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2052_NEXT_TARGET.csv",
        "branch": OUT / "P8_Y5_PARENT_QLOC_2052_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2052_VALIDATION.csv",
    }
    write_csv(paths["sources"], sources)
    write_csv(paths["empirical"], empirical_bounds)
    write_csv(paths["residual"], residual_inputs)
    write_csv(paths["arena"], arena_rows)
    write_csv(paths["runner"], runner_rows_)
    write_csv(paths["priority"], priority)
    write_csv(paths["gates"], gates)
    write_csv(paths["decision"], decisions)
    write_csv(paths["next"], next_rows_)
    copies = write_branch_copies(residual_inputs, arena_rows, runner_rows_, next_rows_)
    write_csv(paths["branch"], copies)
    remove_pycache()
    csv_paths_without_validation = [path for key, path in paths.items() if key != "validation"] + [Path(row["path"]) for row in copies]
    validation = validation_rows(sources, empirical_bounds, residual_inputs, arena_rows, runner_rows_, priority, gates, next_rows_, csv_paths_without_validation)
    write_csv(paths["validation"], validation)
    csv_paths = list(paths.values()) + [Path(row["path"]) for row in copies]
    remove_pycache()
    validation = validation_rows(sources, empirical_bounds, residual_inputs, arena_rows, runner_rows_, priority, gates, next_rows_, csv_paths)
    write_csv(paths["validation"], validation)
    write_doc(sources, empirical_bounds, residual_inputs, arena_rows, runner_rows_, priority, gates, decisions, next_rows_, copies, validation)
    remove_pycache()


if __name__ == "__main__":
    main()
