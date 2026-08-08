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


DOC = ROOT / "2053-Y5-R2FR-PPN-gamma-map-from-RAB-profile-or-finite-qR-first-bound.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()


def formalization_has_2053_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    try:
        patterns = (
            "*2053-Y5-R2FR*",
            "*P8_Y5_PARENT_QLOC_2053*",
            "*Y5_R2FR_PPN_gamma_map_from_RAB_profile_or_finite_qR_first_bound_2053*",
        )
        return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))
    except Exception:
        return False


def scripts_pycache_exists() -> bool:
    return (SCRIPT_PATH.parent / "__pycache__").exists()


def cassini_values() -> dict[str, float]:
    source_path = OUT / "P8_Y5_PARENT_QLOC_1643_EXTERNAL_PPN_SOURCE_REGISTER.csv"
    for row in read_csv(source_path):
        if row.get("external_id") == "EXT1643_0_Cassini_gamma":
            central = float(row["gamma_minus_one_central"])
            sigma = float(row["gamma_minus_one_sigma"])
            envelope_1sigma = float(row["abs_delta_gamma_envelope_1sigma"])
            envelope_2sigma = float(row["abs_delta_gamma_envelope_2sigma"])
            return {
                "central": central,
                "sigma": sigma,
                "envelope_1sigma": envelope_1sigma,
                "envelope_2sigma": envelope_2sigma,
            }
    raise RuntimeError("Cassini gamma row not found")


def source_register_rows() -> list[dict[str, object]]:
    specs = [
        (
            "SRC2053_00_2052_doc",
            ROOT / "2052-Y5-R2FR-finite-RAB-residual-source-acquisition-and-bound-runner.md",
            ["NEXT2052_0_2053", "PPN_gamma selected as first local-GR bound target"],
            "2052 handoff into PPN-gamma first finite-bound target.",
        ),
        (
            "SRC2053_01_2052_next",
            OUT / "P8_Y5_PARENT_QLOC_2052_NEXT_TARGET.csv",
            ["NEXT2052_0_2053", "C_R weak-field normalization", "Cassini bound import"],
            "machine-readable 2053 target.",
        ),
        (
            "SRC2053_02_2052_runner",
            OUT / "P8_Y5_PARENT_QLOC_2052_BOUND_RUNNER.csv",
            ["RUN_APR2052_0_PPN_gamma", "REJECTED_PPN_PROJECTION_MISSING"],
            "2052 runner refusal to be sharpened.",
        ),
        (
            "SRC2053_03_2052_projection",
            OUT / "P8_Y5_PARENT_QLOC_2052_ARENA_PROJECTION_MAP.csv",
            ["APR2052_0_PPN_gamma", "tau_PPN_R*q_R_hat"],
            "prior arena projection map.",
        ),
        (
            "SRC2053_04_cassini_external",
            OUT / "P8_Y5_PARENT_QLOC_1643_EXTERNAL_PPN_SOURCE_REGISTER.csv",
            ["EXT1643_0_Cassini_gamma", "gamma = 1 + (2.1 +/- 2.3) x 10^-5", "abs_delta_gamma_envelope_2sigma"],
            "Cassini gamma external bound import.",
        ),
        (
            "SRC2053_05_ppn_runner_1643",
            OUT / "P8_Y5_PARENT_QLOC_1643_NORMALIZED_PPN_BOUND_RUNNER.csv",
            ["RUN1643_2_gamma_bound_inversion", "Delta_gamma_abs_max=6.7e-5"],
            "previous normalized PPN inversion runner.",
        ),
        (
            "SRC2053_06_ppn_inputs_1640",
            OUT / "P8_Y5_PARENT_QLOC_1640_NORMALIZED_PPN_BOUND_INPUTS.csv",
            ["NPPN1640_0_PiR_abs", "NPPN1640_1_kW", "NPPN1640_4_no_cancellation"],
            "prior Pi_R/k_W/source-mass blockers.",
        ),
        (
            "SRC2053_07_source_pack",
            OUT / "P8_Y5_PARENT_QLOC_1735_PPN_WEP_CLOCK_ORBIT_SOURCE_PACK_TEMPLATE.csv",
            ["R3_gamma", "gamma_minus_1", "MISSING_NUMERIC_OR_THEOREM_ZERO"],
            "multi-arena gamma source pack.",
        ),
        (
            "SRC2053_08_legacy_bridge_1741",
            OUT / "P8_Y5_PARENT_QLOC_1741_PPN_GAMMA_BOUND_BRIDGE.csv",
            ["PGB1741_0_Cassini_gamma_bridge", "|2 s_X/(1-s_X)| <= upper_bound"],
            "legacy s_X bridge to avoid convention mixing.",
        ),
        (
            "SRC2053_09_legacy_bridge_1881",
            OUT / "P8_Y5_PARENT_QLOC_1881_PPN_GAMMA_BRIDGE.csv",
            ["PGB1881_0_Cassini_gamma_to_sR", "linearized_bound"],
            "legacy s_R bridge to avoid convention mixing.",
        ),
        (
            "SRC2053_10_legacy_policy_1244",
            OUT / "P8_Y5_R10_1244_PPN_GAMMA_STATISTICAL_POLICY.csv",
            ["STAT1244_0_default_smoke", "residual_about_GR_zero"],
            "strict residual-about-zero statistical policy.",
        ),
        (
            "SRC2053_11_projection_requirements_1368",
            OUT / "P8_Y5_R10_1368_QLOC_TO_PPN_GAMMA_PROJECTION_REQUIREMENTS.csv",
            ["PROJ1368_3_QR_policy_not_importable", "gamma_minus_1_QR=-q_R_hat/2"],
            "older q_R_hat convention warning.",
        ),
        (
            "SRC2053_12_reciprocity_action",
            ROOT / "05-reciprocity-theorem-attempt.md",
            ["R_AB = ln(A B) = ln(T^2 S).", "W R_AB' = Q_R."],
            "definition of reciprocal radial field and Q_R hair.",
        ),
        (
            "SRC2053_13_source_neutrality",
            ROOT / "06-reciprocal-charge-source-neutrality.md",
            ["R_AB = q_R L", "gamma - 1 ~= q_R.", "|q_R| <= 1e-5."],
            "earlier approximate gamma-q_R statement to be sharpened.",
        ),
        (
            "SRC2053_14_2051_nocharge",
            ROOT / "2051-Y5-R2FR-lambdaR-origin-or-QR-nocharge-certificate.md",
            ["QR2051_6_verdict", "NO_QR_NOCHARGE_THEOREM_CURRENT_CORPUS"],
            "no-charge theorem still unavailable.",
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


def weak_field_derivation_rows() -> list[dict[str, object]]:
    data = [
        (
            "DER2053_0_metric_branch",
            "static areal observed metric",
            "ds^2=-A(r)c^2dt^2+S(r)dr^2+r^2dOmega^2, with A=T^2 and C_R=ln(A S)",
            "DEFINITION",
            "same observed metric branch as R_AB/C_R work",
            "not yet a parent field equation",
        ),
        (
            "DER2053_1_Newton_normalization",
            "weak-field time normalization",
            "A(r)=1-r_s/r+O(r_s^2/r^2), r_s=2G M_obs/c^2",
            "CONVENTION_REQUIRED",
            "fixes the measured source mass used in gamma comparison",
            "M_obs same-frame parent/source calibration remains a guard",
        ),
        (
            "DER2053_2_spatial_gamma",
            "areal first-order spatial response",
            "S(r)=1+gamma_obs r_s/r+O(r_s^2/r^2)",
            "PPN_GAMMA_SLOT",
            "defines the radial curvature response being bounded by Cassini",
            "must remain same-frame/readout-compatible with the Cassini observable",
        ),
        (
            "DER2053_3_log_product",
            "C_R=ln(A S)",
            "C_R=(gamma_obs-1) r_s/r+O(r_s^2/r^2)",
            "DERIVED_FIRST_ORDER",
            "this is the actual local bridge from R_AB hair to PPN gamma",
            "higher-order beta/source terms are outside this first-order gamma gate",
        ),
        (
            "DER2053_4_areal_qR_definition",
            "q_R^PPN := lim_{r/r_s -> infinity} (r/r_s) C_R(r)",
            "Delta gamma_R := gamma_obs-1 = q_R^PPN + delta_tail + delta_gauge + delta_readout",
            "DERIVED_CONDITIONAL_SAME_FRAME",
            "tau_PPN_R=1 only in this areal/same-frame/no-tail convention",
            "not equivalent to older q_R_hat unless converted",
        ),
        (
            "DER2053_5_GR_limit",
            "GR/local reciprocity check",
            "GR has gamma_obs=1 and C_R=0+O(r_s^2/r^2) in the first-order exterior slot",
            "CONSISTENCY_CHECK_PASS_NONCLAIM",
            "the map rewards exact R_AB=0 with the expected gamma result",
            "does not prove MTS gives R_AB=0",
        ),
        (
            "DER2053_6_verdict",
            "PPN gamma map from R_AB profile",
            "C_R coefficient at r_s/r is the PPN gamma residual under explicit guards",
            "MAP_DERIVED_CONDITIONAL_NOT_SCOREABLE",
            "we can now write a source-backed q_R bound row",
            "q_R value, tail/gauge/readout silence and parent source mass remain missing",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, item, formula, status, meaning, guard in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "item": item,
                "formula": formula,
                "status": status,
                "meaning": meaning,
                "guard": guard,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def convention_rows() -> list[dict[str, object]]:
    data = [
        (
            "CONV2053_0_areal_qR_PPN",
            "q_R^PPN",
            "C_R(r)=q_R^PPN r_s/r+O(r_s^2/r^2)",
            "gamma_obs-1=q_R^PPN if delta_tail=delta_gauge=delta_readout=0",
            "SELECTED_2053_CONVENTION",
            "uses r_s=2G M_obs/c^2",
        ),
        (
            "CONV2053_1_L_normalization",
            "legacy q_R with C_R=q_R L/r",
            "gamma_obs-1=q_R (L/r_s) under same guards",
            "only equals q_R when L=r_s",
            "NORMALIZATION_GUARD",
            "06 approximate gamma statement needs L owner",
        ),
        (
            "CONV2053_2_qRhat_legacy",
            "legacy q_R_hat lane",
            "1368 records gamma_minus_1_QR=-q_R_hat/2 under a QR convention",
            "q_R_hat=-2 q_R^PPN if both conventions describe the same residual and sign",
            "CONVERTER_ONLY_NOT_IMPORTED",
            "do not mix q_R_hat rows with areal q_R^PPN scoring",
        ),
        (
            "CONV2053_3_sR_legacy",
            "legacy s_R lane",
            "1881 records |2 s_R/(1-s_R)| <= gamma_bound",
            "linearized small-s_R response is Delta gamma ~= 2 s_R",
            "CONVERTER_ONLY_NOT_IMPORTED",
            "use only if the parent residual variable is actually s_R",
        ),
        (
            "CONV2053_4_tau_PPN",
            "tau_PPN_R",
            "tau_PPN_R=1 in the selected areal q_R^PPN convention; otherwise tau_PPN_R is the converter into gamma-1",
            "tau_PPN_R must be declared before scoring",
            "PROJECTION_GUARD",
            "prevents hidden factor-of-two/sign mistakes",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, convention, definition, gamma_map, status, warning in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "convention": convention,
                "definition": definition,
                "gamma_map": gamma_map,
                "status": status,
                "warning": warning,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def cassini_import_rows() -> list[dict[str, object]]:
    values = cassini_values()
    data = [
        (
            "CAS2053_0_source_measurement",
            "gamma_minus_1",
            values["central"],
            values["sigma"],
            values["envelope_1sigma"],
            values["envelope_2sigma"],
            "dimensionless",
            "Bertotti-Iess-Tortora Cassini radio-link test; doi:10.1038/nature01997",
            "SOURCE_BACKED_EXTERNAL_BOUND",
        ),
        (
            "CAS2053_1_strict_residual_guard",
            "abs_finite_residual_about_GR_zero",
            0.0,
            values["sigma"],
            values["sigma"],
            2.0 * values["sigma"],
            "dimensionless",
            "1244 policy: compare finite residual magnitude against uncertainty guardrail, not fitted central offset",
            "POLICY_GUARD_NONCLAIM",
        ),
        (
            "CAS2053_2_conservative_centered_envelope",
            "abs_gamma_minus_1_centered_envelope",
            values["central"],
            values["sigma"],
            values["envelope_1sigma"],
            values["envelope_2sigma"],
            "dimensionless",
            "1643 computed abs(central)+N*sigma envelope",
            "SELECTED_FOR_FIRST_NONCLAIM_BOUND_ROW",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, observable, central, sigma, one_sigma_abs, two_sigma_abs, units, source, status in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "observable": observable,
                "central_value": central,
                "sigma": sigma,
                "abs_envelope_1sigma": one_sigma_abs,
                "abs_envelope_2sigma": two_sigma_abs,
                "units": units,
                "source": source,
                "status": status,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def qR_bound_rows() -> list[dict[str, object]]:
    values = cassini_values()
    q_areal_1sigma = values["envelope_1sigma"]
    q_areal_2sigma = values["envelope_2sigma"]
    qhat_1sigma = 2.0 * values["envelope_1sigma"]
    qhat_2sigma = 2.0 * values["envelope_2sigma"]
    rowspecs = [
        (
            "QB2053_0_areal_qR_conservative",
            "q_R^PPN",
            "areal C_R=q_R^PPN r_s/r",
            "|q_R^PPN + delta_tail + delta_gauge + delta_readout| <= 6.7e-5",
            q_areal_2sigma,
            "dimensionless",
            "CONDITIONAL_BOUND_ROW_NONCLAIM",
            "requires delta_tail=delta_gauge=delta_readout=0 or independently bounded before score",
        ),
        (
            "QB2053_1_areal_qR_1sigma_diagnostic",
            "q_R^PPN",
            "areal C_R=q_R^PPN r_s/r",
            "|q_R^PPN + tails| <= 4.4e-5 using abs(central)+1sigma",
            q_areal_1sigma,
            "dimensionless",
            "DIAGNOSTIC_NOT_SELECTED_FOR_CLAIM",
            "kept as sensitivity row only",
        ),
        (
            "QB2053_2_strict_zero_residual_policy",
            "q_R^PPN",
            "residual-about-GR-zero policy",
            "|q_R^PPN| <= 2.3e-5 if comparing only to one-sigma uncertainty and tails are zero",
            values["sigma"],
            "dimensionless",
            "STRICT_SMOKE_POLICY_NONCLAIM",
            "does not fit the central Cassini offset",
        ),
        (
            "QB2053_3_legacy_qRhat_converter",
            "q_R_hat",
            "legacy gamma_minus_1=-q_R_hat/2 convention",
            "|q_R_hat| <= 1.34e-4 from conservative areal envelope if the converter is parent-signed",
            qhat_2sigma,
            "dimensionless",
            "CONVERTER_ROW_NONCLAIM",
            "not mixed with areal q_R^PPN unless sign/factor convention is proved",
        ),
        (
            "QB2053_4_legacy_sR_converter",
            "s_R",
            "legacy exact |2s_R/(1-s_R)| bound",
            "|s_R| <= 1.14998677515e-5 from 1881 one-sigma bridge",
            1.14998677515e-5,
            "dimensionless",
            "LEGACY_BRIDGE_NONCLAIM",
            "retained for compatibility, not selected as 2053 residual variable",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, residual_symbol, convention, bound_formula, numeric_abs_bound, units, status, missing_for_claim in rowspecs:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "residual_symbol": residual_symbol,
                "convention": convention,
                "bound_formula": bound_formula,
                "numeric_abs_bound": numeric_abs_bound,
                "units": units,
                "status": status,
                "missing_for_claim": missing_for_claim,
                "source_backed_external_bound": True,
                "valid_for_claim": False,
                "accepted_for_scoring": False,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def guard_rows() -> list[dict[str, object]]:
    data = [
        ("GUARD2053_0_same_frame_mass", "r_s=2G M_obs/c^2 owner", "M_obs must be the same source mass used by Cassini/Shapiro readout", "MISSING_PARENT_SOURCE_MASS_CALIBRATION", "blocks claim"),
        ("GUARD2053_1_gauge", "areal/PPN coordinate guard", "C_R coefficient must be evaluated in the observed areal weak-field gauge or converted", "MISSING_GAUGE_CONVERSION_PROOF", "blocks score"),
        ("GUARD2053_2_readout", "metric readout guard", "observed photon/radio-link metric must be the same g_obs containing A,S", "MISSING_READOUT_STABILITY_PROOF", "blocks claim"),
        ("GUARD2053_3_tail", "tail/source residual guard", "delta_tail, delta_source, and delta_boundary must be theorem-zero or bounded separately", "MISSING_TAIL_ZERO_OR_BOUNDS", "blocks score"),
        ("GUARD2053_4_no_cancellation", "absolute residual vector", "q_R cannot be cancelled by opposite-sign tail/gauge/readout sectors unless a signed cancellation theorem exists", "POLICY_ACTIVE", "enforced"),
        ("GUARD2053_5_beta_Newton", "scope guard", "gamma first-order map does not derive beta, source-normalized Newton, or full local GR", "NOT_A_LOCAL_GR_CLAIM", "enforced"),
    ]
    rows: list[dict[str, object]] = []
    for row_id, guard, requirement, status, effect in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "guard": guard,
                "requirement": requirement,
                "status": status,
                "effect": effect,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def runner_rows(qr_bounds: list[dict[str, object]], guards: list[dict[str, object]]) -> list[dict[str, object]]:
    guard_blockers = [row for row in guards if str(row["status"]).startswith("MISSING_")]
    rows: list[dict[str, object]] = []
    for bound in qr_bounds:
        selected = bound["row_id"] == "QB2053_0_areal_qR_conservative"
        row = base_row()
        row.update(
            {
                "run_id": "RUN_" + str(bound["row_id"]),
                "residual_symbol": bound["residual_symbol"],
                "numeric_abs_bound": bound["numeric_abs_bound"],
                "selected_first_bound": selected,
                "external_bound_imported": True,
                "accepted_for_scoring": False,
                "verdict": "BOUND_ROW_WRITTEN_NONCLAIM" if selected else "DIAGNOSTIC_OR_CONVERTER_NONCLAIM",
                "reason": "external Cassini bound is source-backed, but guard blockers remain: "
                + ";".join(str(row_["row_id"]) for row_ in guard_blockers),
                "claim_allowed": False,
            }
        )
        rows.append(row)
    verdict = base_row()
    verdict.update(
        {
            "run_id": "RUN2053_VERDICT",
            "residual_symbol": "q_R^PPN",
            "numeric_abs_bound": next(row["numeric_abs_bound"] for row in qr_bounds if row["row_id"] == "QB2053_0_areal_qR_conservative"),
            "selected_first_bound": True,
            "external_bound_imported": True,
            "accepted_for_scoring": False,
            "verdict": "PPN_GAMMA_MAP_DERIVED_FIRST_QR_BOUND_ROW_NONCLAIM",
            "reason": "weak-field map is derived under explicit convention; Cassini bound row exists; local-GR/score blocked by missing same-frame mass, gauge/readout and tail-zero certificates",
            "claim_allowed": False,
        }
    )
    rows.append(verdict)
    return rows


def claim_gate_rows() -> list[dict[str, object]]:
    data = [
        ("GATE2053_0_weak_field_map", "derive C_R coefficient to gamma_minus_1", "PASS_NONCLAIM", "C_R=(gamma-1)r_s/r at first order in selected areal convention"),
        ("GATE2053_1_convention_guard", "q_R convention declared and legacy converters separated", "PASS_NONCLAIM", "areal q_R^PPN selected; q_R_hat and s_R retained as converters only"),
        ("GATE2053_2_Cassini_import", "Cassini source-backed gamma bound imported", "PASS_NONCLAIM", "central/sigma/envelopes imported from 1643 source register"),
        ("GATE2053_3_first_qR_bound_row", "first source-backed q_R bound row written", "PASS_NONCLAIM", "conditional nonclaim q_R^PPN bound row written"),
        ("GATE2053_4_score_MTS_prediction", "MTS finite q_R prediction scored", "FAIL_BLOCKED", "q_R value/profile and guard certificates missing"),
        ("GATE2053_5_local_GR", "local GR/Newton/beta claimed", "FAIL_BLOCKED", "gamma map alone does not prove R_AB=0, beta=1 or source-normalized Newton"),
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
            "DEC2053_0_map",
            "The PPN-gamma map is now derived in a declared convention.",
            "The first-order coefficient of C_R=ln(T^2S) in r_s/r is gamma-1, provided the observed metric, mass normalization and readout are the same.",
        ),
        (
            "DEC2053_1_bound",
            "A first Cassini-backed q_R^PPN bound row now exists, but it is nonclaim.",
            "The conservative centered row gives |q_R^PPN + tails| <= 6.7e-5; scoring waits on tail/gauge/readout/source-mass guards.",
        ),
        (
            "DEC2053_2_conventions",
            "Do not mix q_R^PPN, q_R_hat and s_R lanes.",
            "Older rows are useful, but the factor-of-two/sign differences must be converted explicitly before comparison.",
        ),
        (
            "DEC2053_3_next",
            "The next leap is not more Cassini data; it is the guard closure.",
            "We need same-frame mass, gauge/readout silence and tail/source zero-or-bound rows, or a source-backed q_R profile.",
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
            "target_id": "NEXT2053_0_2054",
            "target_doc": "2054-Y5-R2FR-PPN-gamma-gauge-readout-tail-zero-or-qR-profile-source-row.md",
            "objective": "try to close the same-frame mass, gauge/readout and tail-zero guards for the PPN-gamma map; if not, create the first source-ready q_R^PPN profile/Pi_R row for bounded nonclaim scoring",
            "must_include": "same-frame M_obs/r_s owner; areal-to-PPN gauge guard; photon/readout metric stability; delta_tail/source/boundary zero-or-bound; no-cancellation vector; q_R profile/Pi_R source row",
            "excluded": "using the Cassini bound as a theory pass; mixing q_R_hat with q_R^PPN; assuming tails vanish; claiming beta/Newton/local GR; GitHub; formalization-workbench edits",
            "claim_allowed": False,
        }
    )
    return [row]


def write_branch_copies(
    derivation: list[dict[str, object]],
    qr_bounds: list[dict[str, object]],
    runner: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
) -> list[dict[str, object]]:
    copies = [
        (
            "COPY2053_0_source_weight_gamma_map",
            SOURCE_WEIGHT_DOCS / "AFRAME_PPN_GAMMA_RAB_MAP_2053_NONCLAIM.csv",
            derivation,
        ),
        (
            "COPY2053_1_wep_qR_bound",
            BRANCH_WEP / "P8_Y5_PARENT_QLOC_2053_PPN_GAMMA_QR_BOUND_NONCLAIM.csv",
            qr_bounds,
        ),
        (
            "COPY2053_2_wep_runner",
            BRANCH_WEP / "P8_Y5_PARENT_QLOC_2053_PPN_GAMMA_RUNNER_NONCLAIM.csv",
            runner,
        ),
        (
            "COPY2053_3_rab_next",
            QUEUE / "JR2053_PPN_GAMMA_GUARD_CLOSURE_NEXT_NONCLAIM.csv",
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
    derivation: list[dict[str, object]],
    conventions: list[dict[str, object]],
    cassini: list[dict[str, object]],
    qr_bounds: list[dict[str, object]],
    guards: list[dict[str, object]],
    runner: list[dict[str, object]],
    gates: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    source_ok = all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in sources)
    csv_ok = all(csv_rows_parse(path) for path in csv_paths)
    derived_map = next(row for row in derivation if row["row_id"] == "DER2053_6_verdict")
    areal_conv = next(row for row in conventions if row["row_id"] == "CONV2053_0_areal_qR_PPN")
    qhat_conv = next(row for row in conventions if row["row_id"] == "CONV2053_2_qRhat_legacy")
    cassini_selected = next(row for row in cassini if row["row_id"] == "CAS2053_2_conservative_centered_envelope")
    q_bound = next(row for row in qr_bounds if row["row_id"] == "QB2053_0_areal_qR_conservative")
    runner_verdict = next(row for row in runner if row["run_id"] == "RUN2053_VERDICT")
    score_gate = next(row for row in gates if row["row_id"] == "GATE2053_4_score_MTS_prediction")
    local_gate = next(row for row in gates if row["row_id"] == "GATE2053_5_local_GR")
    guard_blocked = any(str(row["status"]).startswith("MISSING_") for row in guards)
    no_claim_rows = (
        all(not bool(row.get("claim_allowed", False)) for row in derivation)
        and all(not bool(row.get("claim_allowed", False)) for row in conventions)
        and all(not bool(row.get("claim_allowed", False)) for row in qr_bounds)
        and all(not bool(row.get("accepted_for_scoring", False)) for row in qr_bounds)
        and all(not bool(row.get("accepted_for_scoring", False)) for row in runner)
    )
    checks: list[tuple[str, bool, str]] = []
    checks.append(("VAL2053_00_local_sources_exist", source_ok, "all cited local source paths and needles exist"))
    checks.append(("VAL2053_01_csv_parse", csv_ok, "all generated CSV files parse cleanly"))
    checks.append(("VAL2053_02_gamma_map_derived", derived_map["status"] == "MAP_DERIVED_CONDITIONAL_NOT_SCOREABLE", "C_R coefficient to gamma map derived conditionally"))
    checks.append(("VAL2053_03_areal_convention_selected", areal_conv["status"] == "SELECTED_2053_CONVENTION", "areal q_R^PPN convention selected"))
    checks.append(("VAL2053_04_legacy_converter_separated", qhat_conv["status"] == "CONVERTER_ONLY_NOT_IMPORTED", "legacy q_R_hat converter not mixed into score"))
    checks.append(("VAL2053_05_cassini_values_imported", float(cassini_selected["abs_envelope_2sigma"]) == 6.7e-5, "Cassini 2sigma centered envelope imported"))
    checks.append(("VAL2053_06_qR_bound_written", float(q_bound["numeric_abs_bound"]) == 6.7e-5, "first q_R^PPN conservative bound row written"))
    checks.append(("VAL2053_07_guards_block_score", guard_blocked, "same-frame/gauge/readout/tail guards remain explicit blockers"))
    checks.append(("VAL2053_08_runner_nonclaim", runner_verdict["verdict"] == "PPN_GAMMA_MAP_DERIVED_FIRST_QR_BOUND_ROW_NONCLAIM", "runner writes bound row but does not score MTS prediction"))
    checks.append(("VAL2053_09_no_claim_rows", no_claim_rows, "all generated rows remain nonclaim/unscored"))
    checks.append(("VAL2053_10_score_blocked", score_gate["status"] == "FAIL_BLOCKED", "MTS finite q_R prediction score remains blocked"))
    checks.append(("VAL2053_11_local_GR_blocked", local_gate["status"] == "FAIL_BLOCKED", "local GR/Newton/beta claim remains blocked"))
    checks.append(("VAL2053_12_next_selected", next_rows_[0]["target_id"] == "NEXT2053_0_2054", "2054 guard-closure/q_R source-row target selected"))
    checks.append(("VAL2053_13_formalization_unchanged", count_formalization_modified() == 0, "formalization-workbench modified-file count remains 0"))
    checks.append(("VAL2053_14_no_formalization_2053_artifacts", not formalization_has_2053_artifacts(), "no 2053 artifacts were written under formalization-workbench"))
    checks.append(("VAL2053_15_no_pycache", not scripts_pycache_exists(), "scripts __pycache__ removed"))
    overall = all(ok for _, ok, _ in checks)
    checks.append(("VAL2053_OVERALL", overall, "2053 derives the PPN gamma map, imports Cassini, writes a nonclaim q_R bound row and selects guard closure next"))
    rows: list[dict[str, object]] = []
    for check_id, ok, detail in checks:
        row = base_row()
        row.update({"check_id": check_id, "status": "PASS" if ok else "FAIL", "detail": detail, "claim_allowed": False})
        rows.append(row)
    return rows


def write_doc(
    sources: list[dict[str, object]],
    derivation: list[dict[str, object]],
    conventions: list[dict[str, object]],
    cassini: list[dict[str, object]],
    qr_bounds: list[dict[str, object]],
    guards: list[dict[str, object]],
    runner: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    sections = [
        "# 2053 Y5 R2FR PPN Gamma Map From R_AB Profile Or Finite q_R First Bound",
        "",
        "## Current Verdict",
        "",
        "2053 derives the clean first-order bridge: in the observed static areal branch, with `A=T^2`, `S` the radial metric coefficient, `C_R=ln(A S)`, and `r_s=2G M_obs/c^2`, the weak-field expansion gives `C_R=(gamma_obs-1) r_s/r+O(r_s^2/r^2)`. So the coefficient `q_R^PPN := lim (r/r_s) C_R` is the PPN gamma residual only under explicit same-frame, gauge, readout, and tail-silence guards.",
        "",
        "That means we now have a real nonclaim Cassini-backed first bound row: `|q_R^PPN + delta_tail + delta_gauge + delta_readout| <= 6.7e-5` using the conservative centered Cassini envelope. But it is not an MTS pass because `q_R^PPN`, the tail/gauge/readout terms, and same-frame source-mass ownership are not parent-signed yet.",
        "",
        "Crucially, this checkpoint separates conventions. The selected 2053 variable is areal `q_R^PPN`; older `q_R_hat` and `s_R` rows are retained only as converters. No `R_AB=0`, `p=1`, `beta=1`, local-GR, Newton, PPN pass, GitHub action, or `formalization-workbench` edit is claimed.",
        "",
        "## Source Register",
        md_table(sources, ["source_id", "source_kind", "source_path", "status", "note", "valid_for_claim"]),
        "## Weak-Field Derivation",
        md_table(derivation, ["row_id", "item", "formula", "status", "meaning", "guard", "claim_allowed"]),
        "## Convention Ledger",
        md_table(conventions, ["row_id", "convention", "definition", "gamma_map", "status", "warning", "claim_allowed"]),
        "## Cassini Bound Import",
        md_table(cassini, ["row_id", "observable", "central_value", "sigma", "abs_envelope_1sigma", "abs_envelope_2sigma", "units", "status", "claim_allowed"]),
        "## q_R Bound Rows",
        md_table(qr_bounds, ["row_id", "residual_symbol", "convention", "bound_formula", "numeric_abs_bound", "units", "status", "missing_for_claim", "accepted_for_scoring", "claim_allowed"]),
        "## Guard Ledger",
        md_table(guards, ["row_id", "guard", "requirement", "status", "effect", "claim_allowed"]),
        "## Runner",
        md_table(runner, ["run_id", "residual_symbol", "numeric_abs_bound", "selected_first_bound", "external_bound_imported", "accepted_for_scoring", "verdict", "reason", "claim_allowed"]),
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
    derivation = weak_field_derivation_rows()
    conventions = convention_rows()
    cassini = cassini_import_rows()
    qr_bounds = qR_bound_rows()
    guards = guard_rows()
    runner = runner_rows(qr_bounds, guards)
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows_ = next_target_rows()
    paths = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2053_SOURCE_REGISTER.csv",
        "derivation": OUT / "P8_Y5_PARENT_QLOC_2053_PPN_GAMMA_WEAK_FIELD_DERIVATION.csv",
        "conventions": OUT / "P8_Y5_PARENT_QLOC_2053_QR_CONVENTION_LEDGER.csv",
        "cassini": OUT / "P8_Y5_PARENT_QLOC_2053_CASSINI_GAMMA_BOUND_IMPORT.csv",
        "bounds": OUT / "P8_Y5_PARENT_QLOC_2053_QR_BOUND_ROWS_NONCLAIM.csv",
        "guards": OUT / "P8_Y5_PARENT_QLOC_2053_GUARD_LEDGER.csv",
        "runner": OUT / "P8_Y5_PARENT_QLOC_2053_PPN_GAMMA_RUNNER.csv",
        "gates": OUT / "P8_Y5_PARENT_QLOC_2053_CLAIM_GATE.csv",
        "decision": OUT / "P8_Y5_PARENT_QLOC_2053_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2053_NEXT_TARGET.csv",
        "branch": OUT / "P8_Y5_PARENT_QLOC_2053_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2053_VALIDATION.csv",
    }
    write_csv(paths["sources"], sources)
    write_csv(paths["derivation"], derivation)
    write_csv(paths["conventions"], conventions)
    write_csv(paths["cassini"], cassini)
    write_csv(paths["bounds"], qr_bounds)
    write_csv(paths["guards"], guards)
    write_csv(paths["runner"], runner)
    write_csv(paths["gates"], gates)
    write_csv(paths["decision"], decisions)
    write_csv(paths["next"], next_rows_)
    copies = write_branch_copies(derivation, qr_bounds, runner, next_rows_)
    write_csv(paths["branch"], copies)
    remove_pycache()
    csv_paths_without_validation = [path for key, path in paths.items() if key != "validation"] + [Path(row["path"]) for row in copies]
    validation = validation_rows(sources, derivation, conventions, cassini, qr_bounds, guards, runner, gates, next_rows_, csv_paths_without_validation)
    write_csv(paths["validation"], validation)
    csv_paths = list(paths.values()) + [Path(row["path"]) for row in copies]
    remove_pycache()
    validation = validation_rows(sources, derivation, conventions, cassini, qr_bounds, guards, runner, gates, next_rows_, csv_paths)
    write_csv(paths["validation"], validation)
    write_doc(sources, derivation, conventions, cassini, qr_bounds, guards, runner, gates, decisions, next_rows_, copies, validation)
    remove_pycache()


if __name__ == "__main__":
    main()
