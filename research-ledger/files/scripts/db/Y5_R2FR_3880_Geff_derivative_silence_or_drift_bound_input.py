from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3880"
BRANCH = "MTS_R2FR_Y5_GEFF_DERIVATIVE_SILENCE_OR_DRIFT_BOUND_INPUT_3880"

PCW = Path(__file__).resolve().parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
OUT = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3880-Y5-R2FR-Geff-derivative-silence-or-drift-bound-input.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

CSV_3879_NEXT = OUT / "P8_Y5_R2FR_3879_NEXT_TARGET.csv"
CSV_3879_THEOREM = OUT / "P8_Y5_R2FR_3879_COMMON_GN_CALIBRATION_THEOREM.csv"
CSV_3879_DRIFT = OUT / "P8_Y5_R2FR_3879_COMMON_DRIFT_VECTOR_CONTRACT.csv"
CSV_3879_RUNNER = OUT / "P8_Y5_R2FR_3879_ACTIVE_RUNNER_GN_CALIBRATION_UPDATE.csv"
CSV_KAPPA_THEOREM = OUT / "P8_CONSTANT_KAPPA_SUPERSELECTION_THEOREM.csv"
CSV_KAPPA_RESIDUAL = OUT / "P8_CONSTANT_KAPPA_RESIDUAL_MAP.csv"
CSV_GM_ZERO = OUT / "P8_CONSTANT_GM_ZERO_THEOREM_ATTEMPT.csv"
CSV_DERIV_GATE = OUT / "P8_CONSTANT_GM_DERIVATIVE_HAIR_GATE.csv"
CSV_RUNNER_INPUT = OUT / "P8_CONSTANT_GM_LOCAL_RESIDUAL_RUNNER_INPUT.csv"
CSV_BOUND_MATRIX = OUT / "P8_CONSTANT_GM_RESIDUAL_BOUND_MATRIX.csv"
CSV_GDOT_FILL = OUT / "P8_Y5_R2FR_3757_GDOT_CONDITIONAL_FILL.csv"
CSV_GDOT_EVAL = OUT / "P8_Y5_R2FR_3758_GDOT_BOUND_EVALUATION.csv"
CSV_RADIAL = OUT / "P8_radial_mu_profile_or_zero.csv"
CSV_FRAME = OUT / "P8_frame_source_split_residual_or_zero.csv"
CSV_R10_STATUS = OUT / "P8_Y5_R10_1495_R10_ALPHA_LAMBDA_CURVE_STATUS.csv"
CSV_R10_CURVE = OUT / "R10_alpha_lambda_curve_MTS_source_normalization.csv"
CSV_3501_MU = OUT / "P8_Y5_R2FR_3501_MU_EXTRA_OVER_GREF_MH_VECTOR.csv"
CSV_SOURCE_STACK = OUT / "P8_source_normalized_Newton_branch_STACK.csv"
CSV_Y5_OWNER = OUT / "P8_Y5_SOURCE_NORMALIZATION_OWNER_THEOREM.csv"
CSV_PG_MAP = OUT / "P8_PG_calibration_residual_MAP.csv"
CSV_PG_TEMPLATE = OUT / "P8_PG_calibration_residual_INPUT_TEMPLATE.csv"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3880_SOURCE_REGISTER.csv",
    "silence_theorem": OUT / "P8_Y5_R2FR_3880_GEFF_DERIVATIVE_SILENCE_THEOREM.csv",
    "channel_audit": OUT / "P8_Y5_R2FR_3880_DERIVATIVE_CHANNEL_AUDIT.csv",
    "bound_inputs": OUT / "P8_Y5_R2FR_3880_DRIFT_BOUND_INPUT_ROWS.csv",
    "runner_update": OUT / "P8_Y5_R2FR_3880_BGCOMMON_RUNNER_UPDATE.csv",
    "claim_gates": OUT / "P8_Y5_R2FR_3880_CLAIM_GATES.csv",
    "next": OUT / "P8_Y5_R2FR_3880_NEXT_TARGET.csv",
    "status": OUT / "P8_Y5_R2FR_3880_STATUS.csv",
    "validation": OUT / "P8_Y5_BRR545_3880_VALIDATION.csv",
}

SOURCE_SPECS = [
    ("SRC3880_00_3879_next", CSV_3879_NEXT, "NEXT3879_0", "3879 selected Geff derivative-silence target"),
    ("SRC3880_01_3879_constancy", CSV_3879_THEOREM, "CGT3879_2_local_constancy", "common tail derivative silence theorem"),
    ("SRC3880_02_3879_bound", CSV_3879_THEOREM, "CGT3879_3_drift_bound", "finite drift bound"),
    ("SRC3880_03_3879_bcommon", CSV_3879_DRIFT, "DVC3879_1_bcommon", "b_common_drift row"),
    ("SRC3880_04_3879_bG", CSV_3879_DRIFT, "DVC3879_0_bGcommon", "b_Gcommon row"),
    ("SRC3880_05_3879_runner", CSV_3879_RUNNER, "RUNU3879_2_updated_runner", "b_Gcommon runner"),
    ("SRC3880_06_kappa_global", CSV_KAPPA_THEOREM, "T508_0_global_sector", "global/superselection kappa route"),
    ("SRC3880_07_kappa_topological", CSV_KAPPA_THEOREM, "T508_1_topological_zeroform", "topological zero-form kappa route"),
    ("SRC3880_08_kappa_corollary", CSV_KAPPA_THEOREM, "T508_2_no_residual_if_closed", "kappa derivative silence corollary"),
    ("SRC3880_09_kr_time", CSV_KAPPA_RESIDUAL, "KR508_0_time_drift", "time drift residual if theorem missing"),
    ("SRC3880_10_kr_radial", CSV_KAPPA_RESIDUAL, "KR508_1_radial_hair", "radial hair residual if theorem missing"),
    ("SRC3880_11_kr_range", CSV_KAPPA_RESIDUAL, "KR508_2_range_dependence", "range dependence residual if theorem missing"),
    ("SRC3880_12_kr_frame", CSV_KAPPA_RESIDUAL, "KR508_4_frame_domain_split", "frame/domain residual if theorem missing"),
    ("SRC3880_13_kr_bianchi", CSV_KAPPA_RESIDUAL, "KR508_5_Bianchi_exchange", "Bianchi exchange residual"),
    ("SRC3880_14_gm_Z1", CSV_GM_ZERO, "Z1_global_coupling_superselection", "global coupling superselection open"),
    ("SRC3880_15_gm_Z5", CSV_GM_ZERO, "Z5_no_radial_or_range_hair", "radial/range hair open"),
    ("SRC3880_16_gm_Z6", CSV_GM_ZERO, "Z6_same_frame_source_pullback", "same-frame source pullback open"),
    ("SRC3880_17_gm_Z7", CSV_GM_ZERO, "Z7_parent_identity_cancellation", "no tuned cancellation"),
    ("SRC3880_18_gate_time", CSV_DERIV_GATE, "CGM1_time_drift", "time derivative hair gate"),
    ("SRC3880_19_gate_radial", CSV_DERIV_GATE, "CGM2_radial_hair", "radial derivative hair gate"),
    ("SRC3880_20_gate_range", CSV_DERIV_GATE, "CGM4_range_dependence", "range derivative hair gate"),
    ("SRC3880_21_gate_frame", CSV_DERIV_GATE, "CGM5_frame_domain_split", "frame/domain hair gate"),
    ("SRC3880_22_gate_mu", CSV_DERIV_GATE, "CGM6_mu_extra_amplitude", "mu-extra derivative hair gate"),
    ("SRC3880_23_input_gdot", CSV_RUNNER_INPUT, "P8_Geff_time_drift", "Gdot runner input"),
    ("SRC3880_24_input_radial", CSV_RUNNER_INPUT, "P8_radial_source_hair", "radial runner input"),
    ("SRC3880_25_input_range", CSV_RUNNER_INPUT, "P8_range_dependence", "range runner input"),
    ("SRC3880_26_input_frame", CSV_RUNNER_INPUT, "P8_frame_calibration_split", "frame runner input"),
    ("SRC3880_27_bound_gdot", CSV_BOUND_MATRIX, "P8_Geff_time_drift", "Gdot bound target"),
    ("SRC3880_28_bound_range", CSV_BOUND_MATRIX, "P8_range_dependence", "R10 curve target"),
    ("SRC3880_29_gdot_conditional", CSV_GDOT_FILL, "GF3757_0_Gdot_conditional_zero", "conditional Gdot zero row"),
    ("SRC3880_30_gdot_eval", CSV_GDOT_EVAL, "GB3758_1_residual_bound", "Gdot residual bound formula"),
    ("SRC3880_31_radial_row", CSV_RADIAL, "RH3048_0_radial_hair_definition", "radial hair seeded row"),
    ("SRC3880_32_frame_row", CSV_FRAME, "FS3048_0_frame_split_definition", "frame/domain seeded row"),
    ("SRC3880_33_r10_status", CSV_R10_STATUS, "CURVE1495_0_R10_alpha_lambda", "R10 curve digitization status"),
    ("SRC3880_34_r10_curve", CSV_R10_CURVE, "R10_alpha_lambda_curve_MTS_source_normalization", "R10 source-normalization curve template"),
    ("SRC3880_35_mu_time", CSV_3501_MU, "EMV3501_2_time_MH_flux", "time mass-flux channel"),
    ("SRC3880_36_mu_range", CSV_3501_MU, "EMV3501_6_bulk_range_yukawa_tail", "range/Yukawa channel"),
    ("SRC3880_37_mu_cal", CSV_3501_MU, "EMV3501_11_absolute_calibration_offset", "absolute calibration offset channel"),
    ("SRC3880_38_stack_Geff", CSV_SOURCE_STACK, "SN7_constant_universal_Geff", "constant universal Geff rung"),
    ("SRC3880_39_stack_hair", CSV_SOURCE_STACK, "SN10_no_derivative_hair", "no derivative hair rung"),
    ("SRC3880_40_Y5_constant", CSV_Y5_OWNER, "Y5O_2_constant_universal_coupling", "Y5 constant universal coupling owner"),
    ("SRC3880_41_Y5_theorem", CSV_Y5_OWNER, "Y5O_8_owner_theorem", "Y5 source normalization owner theorem"),
    ("SRC3880_42_PG7", CSV_PG_MAP, "PG7_constant_universal_Geff", "PG7 constant Geff residual map"),
    ("SRC3880_43_PG8", CSV_PG_MAP, "PG8_no_derivative_hair", "PG8 derivative hair residual map"),
    ("SRC3880_44_template_gdot", CSV_PG_TEMPLATE, "P8_Geff_time_drift", "PG calibration Gdot input template"),
    ("SRC3880_45_template_range", CSV_PG_TEMPLATE, "P8_range_dependence", "PG calibration range input template"),
]

SUPERSELECTION_THEOREM = (
    "If C_* is a parent global/superselected coupling-coordinate or a topological zero-form integration constant, "
    "and it carries no source/species, range, frame, or domain labels, then D_t ln C_*=D_r ln C_*=D_frame ln C_*=D_lambda ln C_*=Delta_domain(C_*)=0 on a connected local branch."
)

TOPOLOGICAL_ROUTE = (
    "A sufficient parent mechanism is S_C=int C_* dA_3, whose A_3 variation gives dC_*=0; this would make the calibrated G0 an integration constant rather than a local scalar field."
)

DRIFT_VECTOR = (
    "b_common_drift = b_t + b_r + b_lambda + b_frame + b_domain + b_Bianchi"
)

UPDATED_BG = (
    "b_Gcommon := b_t+b_r+b_lambda+b_frame+b_domain+b_Bianchi+b_MHref_lock+b_PiM_JH_flux+b_GM_anti_circular+b_PPN_readout"
)

UPDATED_RUNNER = (
    "|z_g_active,cal| <= b_Qstar + b_Noether + b_tail_rel + b_Gcommon"
)


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8-sig", errors="replace")


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(PCW))
    except ValueError:
        return str(path)


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def source_register_rows(timestamp: str) -> list[dict[str, object]]:
    rows = []
    for source_id, path, needle, role in SOURCE_SPECS:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            {
                "source_id": source_id,
                "checkpoint": CHECKPOINT,
                "path": rel(path),
                "exists": exists,
                "needle": needle,
                "needle_found": needle in text,
                "role": role,
                "claim_use": "nonclaim_Geff_derivative_silence_or_bound_input",
                "timestamp_utc": timestamp,
            }
        )
    return rows


def silence_theorem_rows(timestamp: str) -> list[dict[str, object]]:
    rows = [
        ("GST3880_0_target", "Geff derivative-silence target", SUPERSELECTION_THEOREM, "EXACT_CONDITIONAL_SUPERSELECTION_THEOREM", "parent global/topological clause not signed"),
        ("GST3880_1_topological_route", "topological integration-constant route", TOPOLOGICAL_ROUTE, "EXACT_CONDITIONAL_MECHANISM", "not in current parent action"),
        ("GST3880_2_chain_rule", "q-basic constant route", "If C_*=C_bar(q_global) with D_local q_global=0 and no labels in {source,lambda,frame,domain}, local derivatives vanish by the chain rule.", "EXACT_CONDITIONAL_CHAIN_RULE", "q_global ownership not parent-signed"),
        ("GST3880_3_Bianchi_guard", "Bianchi/source-exchange guard", "If kappa varies, Bianchi gives source-exchange terms rather than free calibration; D C_*=0 or explicit exchange rows are required.", "NO_SMUGGLING_GUARD", "delta_kappa_source retained"),
        ("GST3880_4_no_tuned_cancellation", "no cancellation policy", "D_X ln G_eff, D_X ln M_eff, and D_X epsilon_mu may cancel only by a parent Ward/superselection identity, not by fitted epoch/radius/source tuning.", "NO_CANCELLATION_GUARD", "all channels absolute-summed unless identity signed"),
        ("GST3880_5_verdict", "current 3880 status", "The derivative-silence theorem is exact but conditional; current branch must carry theorem-or-bound rows for time, radial, range, frame, domain, and Bianchi exchange.", "NONCLAIM_THEOREM_OR_BOUND_ROWS", "b_common_drift not zero-claimed"),
    ]
    return [
        {
            "theorem_id": row_id,
            "piece": piece,
            "statement": statement,
            "status": status,
            "remaining_gap": gap,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, piece, statement, status, gap in rows
    ]


def channel_audit_rows(timestamp: str) -> list[dict[str, object]]:
    rows = [
        ("DCA3880_0_time", "b_t", "D_t ln C_*", "zero if global/topological C_* and closed Pi_M/M_eff flux; otherwise Gdot row", "P8_time_drift_residual_or_zero.csv", "OPEN_NOT_PARENT_SIGNED"),
        ("DCA3880_1_radial", "b_r", "D_r ln C_*", "zero if source-free exterior no-hair/Gauss charge is radius-independent; otherwise radial profile", "P8_radial_mu_profile_or_zero.csv", "OPEN_NOT_PARENT_SIGNED"),
        ("DCA3880_2_range", "b_lambda", "D_lambda ln C_* or finite-range alpha(lambda)", "zero if no sourced finite-range pole/no-range theorem; otherwise executable alpha(lambda) curve", "R10_alpha_lambda_curve_MTS_source_normalization.csv", "OPEN_CURVE_REQUIRED"),
        ("DCA3880_3_frame", "b_frame", "D_frame ln C_*", "zero if source variation and matter/readout use one parent observed coframe", "P8_frame_source_split_residual_or_zero.csv", "OPEN_NOT_PARENT_SIGNED"),
        ("DCA3880_4_domain", "b_domain", "Delta_domain(C_*)", "zero if support/domain/readout selector is q-basic and parent fixed", "P8_frame_source_split_residual_or_zero.csv;P8_DOMAIN_SELECTOR_*", "OPEN_NOT_PARENT_SIGNED"),
        ("DCA3880_5_Bianchi", "b_Bianchi", "T_obs nabla ln C_* exchange", "zero if D C_*=0; otherwise source-exchange coefficient row", "P8_delta_kappa_source_exchange_residual.csv", "OPEN_NO_SOURCE_ROW"),
        ("DCA3880_6_mu_extra", "b_epsilon_mu", "D_X ln(1+epsilon_mu)", "zero if mu_extra=0 or universal derivative-silent calibration", "P8_mu_extra_over_Geff_Meff_vector.csv", "PARALLEL_HAIR_VECTOR_RETAINED"),
    ]
    return [
        {
            "channel_id": row_id,
            "bound_component": component,
            "derivative_or_residual": derivative,
            "zero_condition": zero,
            "required_artifact_if_not_zero": artifact,
            "current_status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, component, derivative, zero, artifact, status in rows
    ]


def bound_input_rows(timestamp: str) -> list[dict[str, object]]:
    rows = [
        ("DBI3880_0_time_Geff", "P8_Geff_time_drift", "b_t", "dln_Geff_dt", "yr^-1", "9.6e-15", "P8_Y5_R2FR_3758_GDOT_BOUND_EVALUATION.csv:GB3758_1_residual_bound", "MISSING_NUMERIC_OR_PARENT_ZERO", "source-intake\\mts_residuals\\P8_time_drift_residual_or_zero.csv", "valid only if separated from dln_Meff_dt and epsilon_mu drift"),
        ("DBI3880_1_time_Meff", "P8_Meff_conservation", "b_t", "dln_Meff_dt", "yr^-1", "Gdot/beta locks after decomposition", "P8_CONSTANT_GM_DERIVATIVE_HAIR_GATE.csv:CGM1_time_drift", "MISSING_MASS_FLUX_ZERO_OR_BOUND", "source-intake\\mts_residuals\\P8_time_drift_residual_or_zero.csv", "requires Pi_M/Ward flux closure or numeric mass drift"),
        ("DBI3880_2_radial", "P8_radial_source_hair", "b_r", "partial_r_ln_mu_obs", "inverse_length_or_dimensionless_envelope", "zero radial hair or mapped PPN/R10 bound", "P8_radial_mu_profile_or_zero.csv:RH3048_0_radial_hair_definition", "MISSING_RADIAL_PROFILE_OR_NOHAIR", "source-intake\\mts_residuals\\P8_radial_mu_profile_or_zero.csv", "single-radius calibration cannot pass"),
        ("DBI3880_3_range", "P8_range_dependence", "b_lambda", "alpha(lambda)", "range-dependent", "verified alpha(lambda) bound curve", "P8_Y5_R10_1495_R10_ALPHA_LAMBDA_CURVE_STATUS.csv:CURVE1495_0_R10_alpha_lambda", "MISSING_EXECUTABLE_ALPHA_LAMBDA_CURVE_OR_NO_RANGE_THEOREM", "source-intake\\mts_residuals\\R10_alpha_lambda_curve_MTS_source_normalization.csv", "functional in lambda, not one scale"),
        ("DBI3880_4_frame", "P8_frame_calibration_split", "b_frame", "delta_frame_source", "dimensionless", "one observed source frame or residual below WEP/clock locks", "P8_frame_source_split_residual_or_zero.csv:FS3048_0_frame_split_definition", "MISSING_FRAME_SOURCE_THEOREM_OR_BOUND", "source-intake\\mts_residuals\\P8_frame_source_split_residual_or_zero.csv", "must attach to source variation, not only geodesic readout"),
        ("DBI3880_5_domain", "P8_domain_calibration_split", "b_domain", "Delta_domain(C_*)", "dimensionless", "q-basic fixed domain selector or explicit domain-motion bound", "P8_CONSTANT_GM_DERIVATIVE_HAIR_GATE.csv:CGM5_frame_domain_split", "MISSING_DOMAIN_LOCK_OR_BOUND", "source-intake\\mts_residuals\\P8_Y5_PARENT_QLOC_2356_DOMAIN_MOTION_BOUND_ROWS.csv", "domain masks cannot be hidden in calibration"),
        ("DBI3880_6_Bianchi", "P8_delta_kappa_source_exchange", "b_Bianchi", "delta_kappa_source", "source_exchange_units_or_dimensionless_after_norm", "zero if D C_*=0, otherwise explicit exchange coefficient", "P8_CONSTANT_KAPPA_RESIDUAL_MAP.csv:KR508_5_Bianchi_exchange", "MISSING_EXCHANGE_COEFFICIENT_OR_SUPERSELECTION", "source-intake\\mts_residuals\\P8_delta_kappa_source_exchange_residual.csv", "Bianchi cannot be bypassed by a variable coupling"),
        ("DBI3880_7_mu_extra", "P8_boundary_bulk_domain_mu_extra", "b_epsilon_mu", "D_X_epsilon_mu", "dimensionless_or_rate/profile_units", "mu_extra=0 or coefficient vector below locks", "P8_CONSTANT_GM_DERIVATIVE_HAIR_GATE.csv:CGM6_mu_extra_amplitude", "MISSING_MU_EXTRA_VECTOR_OR_ZERO", "source-intake\\mts_residuals\\P8_mu_extra_over_Geff_Meff_vector.csv", "parallel source-hair vector remains visible"),
    ]
    return [
        {
            "input_id": row_id,
            "component_id": component,
            "feeds_component": feeds,
            "symbol": symbol,
            "units": units,
            "bound_or_target": target,
            "source_basis": source,
            "current_status": status,
            "required_artifact": artifact,
            "claim_guard": guard,
            "numeric_prediction": "MISSING_PARENT_ZERO_OR_SOURCE_BOUND",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, component, feeds, symbol, units, target, source, status, artifact, guard in rows
    ]


def runner_update_rows(timestamp: str) -> list[dict[str, object]]:
    rows = [
        ("RUNU3880_0_previous", "b_Gcommon", "b_Gcommon := b_common_drift + b_delta_kappa + b_MHref_lock + b_PiM_JH_flux + b_GM_anti_circular + b_PPN_readout", "imports 3879", "previous common residual"),
        ("RUNU3880_1_bcommon_split", "b_common_drift", DRIFT_VECTOR, "3880 derivative-channel split", "DERIVATIVE_HAIR_CHANNELS_EXPLICIT"),
        ("RUNU3880_2_bG_update", "b_Gcommon", UPDATED_BG, "3880 bcommon decomposition plus carried source locks", "RUNNER_SCHEMA_REFINED"),
        ("RUNU3880_3_runner", "z_g_active,cal", UPDATED_RUNNER, "unchanged top-level runner with refined b_Gcommon", "NO_CANCELLATION_RUNNER"),
        ("RUNU3880_4_conditional_zero", "Geff derivative silence", "all b_t,b_r,b_lambda,b_frame,b_domain,b_Bianchi vanish only if GST3880_0 or GST3880_1 is parent-signed", "superselection/topological route", "CONDITIONAL_ONLY"),
        ("RUNU3880_5_no_claim", "claim_allowed", "false until derivative hair rows are zero-proved or source-backed and same-source/PPN locks close", "acceptance policy", "NO_NEWTON_LOCAL_GR_CLAIM"),
    ]
    return [
        {
            "update_id": row_id,
            "runner_field": field,
            "rule": rule,
            "source_logic": logic,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, field, rule, logic, status in rows
    ]


def claim_gate_rows(
    sources: list[dict[str, object]],
    theorem: list[dict[str, object]],
    audit: list[dict[str, object]],
    inputs: list[dict[str, object]],
    runner: list[dict[str, object]],
    timestamp: str,
) -> list[dict[str, object]]:
    all_sources = all(row["exists"] and row["needle_found"] for row in sources)
    required_inputs = {"b_t", "b_r", "b_lambda", "b_frame", "b_domain", "b_Bianchi"}
    observed_inputs = {row["feeds_component"] for row in inputs}
    rows = [
        ("G3880_0_sources", "all cited source rows resolved", "PASS" if all_sources else "FAIL", f"{sum(1 for row in sources if row['exists'] and row['needle_found'])}/{len(sources)} sources resolved"),
        ("G3880_1_theorem", "derivative-silence theorem written", "PASS" if any(row["status"] == "EXACT_CONDITIONAL_SUPERSELECTION_THEOREM" for row in theorem) else "FAIL", "global/topological C_* route"),
        ("G3880_2_topological", "topological zero-form route written", "PASS" if any(row["status"] == "EXACT_CONDITIONAL_MECHANISM" for row in theorem) else "FAIL", "S_C=int C_* dA_3 route"),
        ("G3880_3_no_cancel", "no tuned cancellation guard retained", "PASS" if any(row["status"] == "NO_CANCELLATION_GUARD" for row in theorem) else "FAIL", "absolute-sum channels"),
        ("G3880_4_channels", "derivative channel audit complete", "PASS" if len(audit) >= 7 else "FAIL", f"{len(audit)} channels"),
        ("G3880_5_inputs", "bound input rows cover required derivative channels", "PASS" if required_inputs.issubset(observed_inputs) else "FAIL", ",".join(sorted(observed_inputs))),
        ("G3880_6_runner", "b_Gcommon runner refined", "PASS" if any(row["rule"] == UPDATED_BG for row in runner) else "FAIL", UPDATED_BG),
        ("G3880_7_no_claim", "no generated row allows Newton/local-GR claim", "PASS", "valid_for_claim=false throughout"),
    ]
    return [
        {
            "gate_id": gate_id,
            "gate": gate,
            "status": status,
            "detail": detail,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for gate_id, gate, status, detail in rows
    ]


def next_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "next_id": "NEXT3880_0",
            "target_checkpoint": "3881-Y5-R2FR-topological-zeroform-coupling-mechanism-or-Gdot-bound-fill.md",
            "script": "scripts/Y5_R2FR_3881_topological_zeroform_coupling_mechanism_or_Gdot_bound_fill.py",
            "objective": "attempt to insert/derive the topological zero-form/three-form mechanism that makes C_* an integration constant; if this cannot be parent-derived, fill the first executable Gdot drift-bound row with separated G_eff/M_eff/epsilon_mu components",
            "why_next": "3880 isolates the cleanest theorem route for derivative silence and the first empirical fallback row; Gdot is the sharpest first channel because a numeric bound already exists",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH,
            "result": "GEFF_DERIVATIVE_SILENCE_THEOREM_AND_DRIFT_BOUND_INPUT_ROWS_BUILT_NONCLAIM",
            "claim_allowed": False,
            "short_summary": "3880 derives the exact conditional superselection/topological route for Geff derivative silence and stages theorem-or-bound rows for time, radial, range, frame, domain, Bianchi and mu-extra hair.",
            "timestamp_utc": timestamp,
        }
    ]


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    lines = [header, sep]
    for row in rows:
        values = []
        for col in columns:
            values.append(str(row.get(col, "")).replace("\n", " ").replace("|", "\\|"))
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def write_doc(
    sources: list[dict[str, object]],
    theorem: list[dict[str, object]],
    audit: list[dict[str, object]],
    inputs: list[dict[str, object]],
    runner: list[dict[str, object]],
    gates: list[dict[str, object]],
    next_target: list[dict[str, object]],
    timestamp: str,
) -> None:
    resolved = sum(1 for row in sources if row["exists"] and row["needle_found"])
    doc = f"""# 3880 - G_eff Derivative Silence or Drift Bound Input

Generated: `{timestamp}`

## Result

3880 attacks the derivative part of the calibrated `G_N` route:

`{SUPERSELECTION_THEOREM}`

The cleanest mechanism is:

`{TOPOLOGICAL_ROUTE}`

But because that parent mechanism is not signed yet, the common drift is now split into explicit channels:

`{DRIFT_VECTOR}`

and the common branch runner is:

`{UPDATED_BG}`

with top-level:

`{UPDATED_RUNNER}`

## Interpretation

This is the point where the work either earns a GR-like constant coupling or becomes a data-bounded variable-coupling theory. A single calibrated `G0` is allowed. A hidden time, radial, range, frame, domain, or Bianchi-exchange drift is not.

## Source Register

Resolved `{resolved}/{len(sources)}` source rows.

{markdown_table(sources, ["source_id", "path", "needle_found", "role"])}

## G_eff Derivative-Silence Theorem

{markdown_table(theorem, ["theorem_id", "piece", "statement", "status"])}

## Derivative Channel Audit

{markdown_table(audit, ["channel_id", "bound_component", "derivative_or_residual", "current_status", "required_artifact_if_not_zero"])}

## Drift Bound Input Rows

{markdown_table(inputs, ["input_id", "component_id", "feeds_component", "symbol", "bound_or_target", "current_status"])}

## Runner Update

{markdown_table(runner, ["update_id", "runner_field", "rule", "status"])}

## Claim Gates

{markdown_table(gates, ["gate_id", "status", "detail", "claim_allowed"])}

## Next Target

{markdown_table(next_target, ["next_id", "target_checkpoint", "objective", "why_next"])}

## Bottom Line

3880 did not claim `G_eff` is constant. It did something more useful: it wrote the exact route that would make it constant, and converted every failed derivative into a concrete input row. The best next move is to try the topological zero-form mechanism; if that fails, fill the first real drift row, starting with `Gdot` because the local bound already exists.
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


def update_spine(timestamp: str) -> None:
    start = "<!-- BEGIN 3880 GEFF DERIVATIVE SILENCE -->"
    end = "<!-- END 3880 GEFF DERIVATIVE SILENCE -->"
    block = f"""{start}

## 3880 - G_eff derivative silence or drift-bound inputs

`3880` isolates the exact route for common-coupling derivative silence:

`{SUPERSELECTION_THEOREM}`

Best mechanism:

`{TOPOLOGICAL_ROUTE}`

Since this is not parent-signed, the carried drift vector is:

`{DRIFT_VECTOR}`

Updated common branch:

`{UPDATED_BG}`

No Newton/local-GR claim is made. The next route is either a parent topological zero-form/three-form coupling mechanism or the first executable drift-bound fill, probably `Gdot`.

Generated outputs:
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3880_GEFF_DERIVATIVE_SILENCE_THEOREM.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3880_DERIVATIVE_CHANNEL_AUDIT.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3880_DRIFT_BOUND_INPUT_ROWS.csv`
- `source-intake\\mts_residuals\\P8_Y5_BRR545_3880_VALIDATION.csv`

Next gate: `3881`, topological zero-form coupling mechanism or `Gdot` bound fill.

<!-- Generated by 3880 at {timestamp} -->
{end}
"""
    existing = read_text(SPINE_PATH) if SPINE_PATH.exists() else "# Local GR Coupling Spine Current State\n"
    if start in existing and end in existing:
        before = existing.split(start)[0].rstrip()
        after = existing.split(end, 1)[1].lstrip()
        new_text = f"{before}\n\n{block}\n\n{after}".rstrip() + "\n"
    else:
        new_text = existing.rstrip() + "\n\n" + block + "\n"
    SPINE_PATH.write_text(new_text, encoding="utf-8")


def validation_rows(
    sources: list[dict[str, object]],
    theorem: list[dict[str, object]],
    audit: list[dict[str, object]],
    inputs: list[dict[str, object]],
    runner: list[dict[str, object]],
    gates: list[dict[str, object]],
    timestamp: str,
) -> list[dict[str, object]]:
    checks: list[tuple[str, str, bool, str]] = []
    all_sources = all(row["exists"] and row["needle_found"] for row in sources)
    checks.append(("VAL3880_0_sources", "all cited source paths exist and needles are found", all_sources, f"{sum(1 for row in sources if row['exists'] and row['needle_found'])}/{len(sources)} sources resolved"))
    checks.append(("VAL3880_1_superselection", "superselection derivative-silence theorem exists", any(row["status"] == "EXACT_CONDITIONAL_SUPERSELECTION_THEOREM" for row in theorem), "superselection theorem"))
    checks.append(("VAL3880_2_topological", "topological zero-form route exists", any(row["status"] == "EXACT_CONDITIONAL_MECHANISM" for row in theorem), "topological mechanism"))
    checks.append(("VAL3880_3_no_cancel", "no tuned cancellation guard exists", any(row["status"] == "NO_CANCELLATION_GUARD" for row in theorem), "no cancellation"))
    required_channels = {"b_t", "b_r", "b_lambda", "b_frame", "b_domain", "b_Bianchi"}
    audit_channels = {row["bound_component"] for row in audit}
    checks.append(("VAL3880_4_audit_channels", "derivative channel audit covers required channels", required_channels.issubset(audit_channels), ",".join(sorted(audit_channels))))
    input_channels = {row["feeds_component"] for row in inputs}
    checks.append(("VAL3880_5_input_rows", "bound input rows cover required channels", required_channels.issubset(input_channels), ",".join(sorted(input_channels))))
    checks.append(("VAL3880_6_gdot_target", "Gdot row carries numeric target", any(row["component_id"] == "P8_Geff_time_drift" and row["bound_or_target"] == "9.6e-15" for row in inputs), "Gdot target 9.6e-15 yr^-1"))
    checks.append(("VAL3880_7_r10_curve_guard", "range row requires executable alpha(lambda) curve", any(row["component_id"] == "P8_range_dependence" and "CURVE" in row["current_status"] for row in inputs), "range curve guard"))
    checks.append(("VAL3880_8_runner_update", "b_Gcommon runner is refined", any(row["rule"] == UPDATED_BG for row in runner), UPDATED_BG))
    checks.append(("VAL3880_9_no_claim_gates", "no claim gate allows a claim", all(str(row["claim_allowed"]) == "False" for row in gates), "claim_allowed=false"))
    checks.append(("VAL3880_10_doc", "markdown checkpoint exists with expected bottom line", DOC_PATH.exists() and "converted every failed derivative into a concrete input row" in read_text(DOC_PATH), rel(DOC_PATH)))
    checks.append(("VAL3880_11_spine", "spine updated with 3880 block", SPINE_PATH.exists() and "BEGIN 3880 GEFF DERIVATIVE SILENCE" in read_text(SPINE_PATH), rel(SPINE_PATH)))
    csv_outputs = [path for key, path in OUTPUTS.items() if key != "validation"]
    csv_parse_ok = True
    parse_details = []
    for path in csv_outputs:
        try:
            count = len(read_csv_rows(path))
            parse_details.append(f"{path.name}:{count}")
        except Exception as exc:  # pragma: no cover
            csv_parse_ok = False
            parse_details.append(f"{path.name}:{exc}")
    checks.append(("VAL3880_12_csv_parse", "all generated CSV outputs parse", csv_parse_ok, "; ".join(parse_details)))
    formalization_hits = []
    generated_patterns = ("3880-Y5", "P8_Y5_R2FR_3880", "P8_Y5_BRR545_3880")
    if FWB.exists():
        formalization_hits = [
            path
            for path in FWB.rglob("*3880*")
            if path.is_file() and any(pattern in path.name for pattern in generated_patterns)
        ]
    checks.append(("VAL3880_13_formalization_untouched", "no generated 3880 files appear in formalization-workbench", not formalization_hits, f"{len(formalization_hits)} hits"))
    pycache_hits = [path for path in (PCW / "scripts").rglob("__pycache__") if path.is_dir()]
    checks.append(("VAL3880_14_no_pycache", "scripts __pycache__ removed", not pycache_hits, f"{len(pycache_hits)} pycache dirs"))
    checks.append(("VAL3880_15_no_generated_claim", "all analytical rows are nonclaim", all(str(row.get("valid_for_claim")) == "False" for collection in [theorem, audit, inputs, runner] for row in collection), "valid_for_claim=false"))
    checks.append(("VAL3880_16_next_target", "next target attacks topological route or Gdot fill", any("topological-zeroform" in str(row["target_checkpoint"]) for row in next_rows(timestamp)), "3881 topological/Gdot"))
    return [
        {
            "check_id": check_id,
            "description": description,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "timestamp_utc": timestamp,
        }
        for check_id, description, passed, detail in checks
    ]


def main() -> int:
    timestamp = now_utc()
    sources = source_register_rows(timestamp)
    theorem = silence_theorem_rows(timestamp)
    audit = channel_audit_rows(timestamp)
    inputs = bound_input_rows(timestamp)
    runner = runner_update_rows(timestamp)
    gates = claim_gate_rows(sources, theorem, audit, inputs, runner, timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["silence_theorem"], theorem)
    write_csv(OUTPUTS["channel_audit"], audit)
    write_csv(OUTPUTS["bound_inputs"], inputs)
    write_csv(OUTPUTS["runner_update"], runner)
    write_csv(OUTPUTS["claim_gates"], gates)
    write_csv(OUTPUTS["next"], next_target)
    write_csv(OUTPUTS["status"], status)
    write_doc(sources, theorem, audit, inputs, runner, gates, next_target, timestamp)
    update_spine(timestamp)

    for pycache in (PCW / "scripts").rglob("__pycache__"):
        shutil.rmtree(pycache, ignore_errors=True)

    validation = validation_rows(sources, theorem, audit, inputs, runner, gates, timestamp)
    write_csv(OUTPUTS["validation"], validation)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        return 1
    print(f"{CHECKPOINT} PASS_GEFF_DERIVATIVE_SILENCE_OR_BOUND_INPUT")
    print(rel(DOC_PATH))
    print(rel(OUTPUTS["validation"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
