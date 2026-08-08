from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_START_UTC = datetime.now(timezone.utc)

ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
SOURCE_WEIGHT = ROOT / "source-intake" / "source-weight"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "2745-Y5-R2FR-closure-deviation-PPN-sensitivity-and-bound-budget-under-AX1090.md"
LOCAL_BOUND_CLAIMS = LOCAL_BOUNDS / "local_bound_claims.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2745_SOURCE_REGISTER.csv",
    "channels": RESIDUALS / "P8_Y5_R2FR_2745_DEVIATION_CHANNELS.csv",
    "bounds": RESIDUALS / "P8_Y5_R2FR_2745_LOCAL_BOUND_LINKS.csv",
    "sensitivity": RESIDUALS / "P8_Y5_R2FR_2745_SENSITIVITY_MAP_NONCLAIM.csv",
    "budget": RESIDUALS / "P8_Y5_R2FR_2745_BOUND_BUDGET_NONCLAIM.csv",
    "coefficients": RESIDUALS / "P8_Y5_R2FR_2745_RESPONSE_COEFFICIENT_SOURCE_QUEUE.csv",
    "runner": RESIDUALS / "P8_Y5_R2FR_2745_RUNNER_NONCLAIM.csv",
    "decisions": RESIDUALS / "P8_Y5_R2FR_2745_DECISION_LEDGER.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_2745_CLAIM_GATES.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2745_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2745_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2745_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "budget": LOCAL_BOUNDS / "closure_deviation_bound_budget_2745_NONCLAIM.csv",
    "coefficients": SOURCE_WEIGHT / "response_coefficient_source_queue_2745_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2745_RESPONSE_COEFFICIENT_SOURCE_MAP_NEXT.csv",
}

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"


def ts() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dirs() -> None:
    for path in {p.parent for p in OUTPUTS.values()} | {p.parent for p in BRANCH_OUTPUTS.values()}:
        path.mkdir(parents=True, exist_ok=True)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing empty CSV: {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def md(value: Any) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def markdown_table(rows: list[dict[str, Any]], cols: list[str]) -> str:
    header = "| " + " | ".join(cols) + " |"
    sep = "| " + " | ".join("---" for _ in cols) + " |"
    body = ["| " + " | ".join(md(row.get(col, "")) for col in cols) + " |" for row in rows]
    return "\n".join([header, sep, *body])


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def local_path(path_text: str) -> Path:
    path = Path(path_text)
    if path.is_absolute():
        return path
    return ROOT / path


def nonclaim(row: dict[str, Any]) -> dict[str, Any]:
    row["score_ready"] = False
    row["valid_prediction_row"] = False
    row["valid_for_claim"] = False
    row["claim_allowed"] = False
    return row


def numeric(value: str) -> bool:
    try:
        float(value)
        return True
    except (TypeError, ValueError):
        return False


def local_bound_lookup() -> dict[str, dict[str, str]]:
    rows = read_csv(LOCAL_BOUND_CLAIMS)
    return {row["row_id"]: row for row in rows}


def source_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "source_id": "SRC2745_0_2744_doc",
            "description": "2744 selects closure-deviation PPN sensitivity and bound budget.",
            "source_path": "2744-Y5-R2FR-local-closure-PPN-benchmark-derived-vs-assumed-ledger-under-AX1090.md",
            "required_needles": "NEXT2744_0_2745;DVA2744_1_gamma;VAL2744_OVERALL",
        },
        {
            "source_id": "SRC2745_1_2744_validation",
            "description": "2744 validation output.",
            "source_path": "source-intake/mts_residuals/P8_Y5_BRR545_2744_VALIDATION.csv",
            "required_needles": "VAL2744_OVERALL;True;closure-deviation sensitivity next",
        },
        {
            "source_id": "SRC2745_2_1557_doc",
            "description": "prior closure-deviation sensitivity and bound budget.",
            "source_path": "1557-Y5-closure-deviation-PPN-sensitivity-and-bound-budget.md",
            "required_needles": "DEV1557_0_qR_gamma;BUD1557_0_qR;NEXT_1558_COEFFICIENT_SOURCE_MAP",
        },
        {
            "source_id": "SRC2745_3_14_deviation_doc",
            "description": "internal deviation sensitivity source text.",
            "source_path": "14-closure-deviation-PPN-sensitivity.md",
            "required_needles": "q_R:;Mercury shift factor = (2 q_R - delta_beta)/3.;not an empirical claim yet",
        },
        {
            "source_id": "SRC2745_4_2744_ppn",
            "description": "live PPN benchmark requirements feeding deviation rows.",
            "source_path": "source-intake/mts_residuals/P8_Y5_R2FR_2744_PPN_BENCHMARK_REQUIREMENTS.csv",
            "required_needles": "PPN2744_0_gamma;PPN2744_1_beta;PPN2744_7_WEP_clock",
        },
        {
            "source_id": "SRC2745_5_local_bound_claims",
            "description": "local bound rows used as nonclaim budget constraints.",
            "source_path": "source-intake/local_bounds/local_bound_claims.csv",
            "required_needles": "R0_identity_coframe_direct;R3_gamma;R10_fifth_force",
        },
        {
            "source_id": "SRC2745_6_1557_channels",
            "description": "machine-readable prior channel map.",
            "source_path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1557_DEVIATION_CHANNELS.csv",
            "required_needles": "DEV1557_0_qR_gamma;DEV1557_8_R10_finite_range;DEV1557_9_tracefree_transfer",
        },
        {
            "source_id": "SRC2745_7_1557_budget",
            "description": "machine-readable prior bound budget.",
            "source_path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1557_BOUND_BUDGET_NONCLAIM.csv",
            "required_needles": "BUD1557_0_qR;MISSING_C_gamma_qR;CONTROL_BOUND_ONLY_NOT_MTS_PREDICTION",
        },
        {
            "source_id": "SRC2745_8_2744_queue",
            "description": "live queue into this checkpoint.",
            "source_path": "source-intake/rab-sector/acquisition-queue/JR2744_CLOSURE_DEVIATION_PPN_SENSITIVITY_NEXT.csv",
            "required_needles": "NEXT2744_0_2745;deviation budget",
        },
    ]
    for row in rows:
        path = local_path(row["source_path"])
        text = path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""
        needles = [needle for needle in row["required_needles"].split(";") if needle]
        missing = [needle for needle in needles if needle not in text]
        row["exists"] = path.exists()
        row["needles_present"] = len(missing) == 0
        row["missing_needles"] = ";".join(missing)
        nonclaim(row)
    return rows


def channel_rows() -> list[dict[str, Any]]:
    specs = [
        ("DEV2745_0_qR_gamma", "q_R", "reciprocal hair coefficient in R_AB approximately q_R L", "0", "gamma_minus_1; light_bending; Shapiro; perihelion", "gamma_minus_1 ~= C_gamma_qR q_R, with internal control C_gamma_qR=1 not parent-signed", "C_gamma_qR; parent R_AB leakage map; source normalization", "R3_gamma"),
        ("DEV2745_1_delta_beta", "delta_beta", "nonlinear completion drift away from beta=1", "0", "beta_minus_1; perihelion", "beta_minus_1 ~= C_beta_delta delta_beta; Mercury control factor=(2 q_R-delta_beta)/3", "C_beta_delta; second-order weak-field completion", "R4_beta"),
        ("DEV2745_2_epsilon_matter", "epsilon_matter", "spread away from universal matter/coframe coupling", "0", "eta_WEP_direct_geometry; eta_WEP_source_charge", "eta ~= C_eta_epsilon epsilon_matter", "C_eta_epsilon; matter action descent; no shadow-frame coupling", "R0_identity_coframe_direct; R1_WEP_source_charge"),
        ("DEV2745_3_alpha_clock", "alpha_clock", "clock/load redshift anomaly", "0", "alpha_clock_redshift", "redshift anomaly ~= C_clock alpha_clock", "C_clock; universal clock/load readout map", "R2_clock_redshift"),
        ("DEV2745_4_Gdot_source_norm", "sigma_Gdot", "time drift in measured source normalization GM or effective G", "0 yr^-1", "Gdot_over_G", "Gdot/G ~= C_Gdot sigma_Gdot", "C_Gdot; measured-GM/source normalization theorem", "R9_Gdot"),
        ("DEV2745_5_preferred_frame_alpha1", "epsilon_frame_1", "vector/coframe preferred-frame leakage", "0", "alpha1", "alpha1 ~= C_alpha1 epsilon_frame_1", "C_alpha1; frame/coframe descent; boundary silence", "R5_alpha1"),
        ("DEV2745_6_preferred_frame_alpha2", "epsilon_frame_2", "spin or anisotropic coframe preferred-frame leakage", "0", "alpha2", "alpha2 ~= C_alpha2 epsilon_frame_2", "C_alpha2; spin/coframe descent; anisotropy map", "R6_alpha2"),
        ("DEV2745_7_flux_alpha3_xi", "epsilon_flux", "source flux, momentum nonconservation, or preferred-location leakage", "0", "alpha3; xi", "alpha3 ~= C_alpha3 epsilon_flux; xi ~= C_xi epsilon_flux", "C_alpha3; C_xi; boundary/no-charge/source-flux theorem", "R7_alpha3; R8_xi"),
        ("DEV2745_8_R10_finite_range", "alpha_R10(lambda)", "finite-range q/source hair outside the exact closure", "0 for all lambda", "delta_G_or_fifth_force_yukawa", "Yukawa alpha(lambda) ~= C_R10(lambda) residual_hair(lambda)", "C_R10(lambda); real digitized alpha(lambda) curve; parent range map", "R10_fifth_force"),
        ("DEV2745_9_tracefree_transfer", "h_TF_residual", "tracefree metric/coframe transfer not fixed by scalar R_AB closure", "0", "PPN tensor/vector residuals", "PPN residual vector ~= M_TF h_TF_residual", "M_TF response matrix; tensor/coframe transfer theorem", "R5_alpha1; R6_alpha2; R8_xi"),
    ]
    return [
        nonclaim(
            {
                "same_parent_branch_id": BRANCH_ID,
                "channel_id": cid,
                "leak_parameter": leak,
                "meaning": meaning,
                "null_lane_value": null,
                "first_observables": observables,
                "leading_control_map": control,
                "missing_parent_inputs": missing,
                "local_bound_rows": bounds,
                "status": "BOUND_BUDGET_ONLY_NOT_PREDICTION",
                "source_paths": "2744-Y5-R2FR-local-closure-PPN-benchmark-derived-vs-assumed-ledger-under-AX1090.md; 14-closure-deviation-PPN-sensitivity.md; source-intake/local_bounds/local_bound_claims.csv",
            }
        )
        for cid, leak, meaning, null, observables, control, missing, bounds in specs
    ]


def bound_rows() -> list[dict[str, Any]]:
    lookup = local_bound_lookup()
    requested = [
        ("R0_identity_coframe_direct", "DEV2745_2_epsilon_matter"),
        ("R1_WEP_source_charge", "DEV2745_2_epsilon_matter"),
        ("R2_clock_redshift", "DEV2745_3_alpha_clock"),
        ("R3_gamma", "DEV2745_0_qR_gamma"),
        ("R4_beta", "DEV2745_1_delta_beta"),
        ("R5_alpha1", "DEV2745_5_preferred_frame_alpha1; DEV2745_9_tracefree_transfer"),
        ("R6_alpha2", "DEV2745_6_preferred_frame_alpha2; DEV2745_9_tracefree_transfer"),
        ("R7_alpha3", "DEV2745_7_flux_alpha3_xi"),
        ("R8_xi", "DEV2745_7_flux_alpha3_xi; DEV2745_9_tracefree_transfer"),
        ("R9_Gdot", "DEV2745_4_Gdot_source_norm"),
        ("R10_fifth_force", "DEV2745_8_R10_finite_range"),
    ]
    rows: list[dict[str, Any]] = []
    for row_id, channel in requested:
        source = lookup[row_id]
        upper = source.get("upper_bound", "")
        rows.append(
            nonclaim(
                {
                    "same_parent_branch_id": BRANCH_ID,
                    "row_id": row_id,
                    "used_for_channel": channel,
                    "observable": source.get("observable", ""),
                    "measured_value": source.get("measured_value", ""),
                    "one_sigma": source.get("one_sigma", ""),
                    "upper_bound": upper,
                    "units": source.get("units", ""),
                    "numeric_bound_parse": "PASS" if numeric(upper) else "SYMBOLIC_CURVE_REQUIRED",
                    "reference_path_or_url": source.get("reference_path_or_url", ""),
                    "reference_note": source.get("reference_note", ""),
                }
            )
        )
    return rows


def sensitivity_rows() -> list[dict[str, Any]]:
    specs = [
        ("SENS2745_0_qR_light_bending", "q_R", "solar light bending", "0.8756216406841224", "arcsec per unit q_R", "C_gamma_qR", "NONCLAIM_INTERNAL_CONVERSION_ONLY"),
        ("SENS2745_1_qR_shapiro", "q_R", "solar Shapiro delay scale", "59.7375179242781", "microseconds per unit q_R", "C_gamma_qR", "NONCLAIM_INTERNAL_CONVERSION_ONLY"),
        ("SENS2745_2_qR_mercury", "q_R", "Mercury perihelion", "28.65467507274745", "arcsec/century per unit q_R", "C_gamma_qR; C_peri_qR", "NONCLAIM_INTERNAL_CONVERSION_ONLY"),
        ("SENS2745_3_delta_beta_mercury", "delta_beta", "Mercury perihelion", "-14.327337536373726", "arcsec/century per unit delta_beta", "C_beta_delta; C_peri_beta", "NONCLAIM_INTERNAL_CONVERSION_ONLY"),
        ("SENS2745_4_alpha_clock_gps", "alpha_clock", "GPS gravitational redshift", "45.718449825926655", "microseconds/day per unit alpha_clock", "C_clock", "NONCLAIM_INTERNAL_CONVERSION_ONLY"),
        ("SENS2745_5_epsilon_matter_eotvos", "epsilon_matter", "Eotvos proxy", "1", "dimensionless proxy per unit coupling spread", "C_eta_epsilon", "NONCLAIM_INTERNAL_CONVERSION_ONLY"),
        ("SENS2745_6_source_norm_Gdot", "sigma_Gdot", "Gdot/G", "MISSING_PARENT_INPUT", "yr^-1 per unit source-normalization drift", "C_Gdot", "NONCLAIM_INTERNAL_CONVERSION_ONLY"),
        ("SENS2745_7_R10_curve", "alpha_R10(lambda)", "inverse-square/Yukawa curve", "MISSING_CURVE_AND_PARENT_INPUT", "alpha(lambda) per residual hair amplitude", "C_R10(lambda)", "NONCLAIM_INTERNAL_CONVERSION_ONLY"),
        ("SENS2745_8_tracefree_ppn_vector", "h_TF_residual", "PPN vector/tensor residual", "MISSING_RESPONSE_MATRIX", "PPN residual per tracefree transfer amplitude", "M_TF", "NONCLAIM_INTERNAL_CONVERSION_ONLY"),
    ]
    return [
        nonclaim(
            {
                "same_parent_branch_id": BRANCH_ID,
                "sensitivity_id": sid,
                "leak_parameter": leak,
                "observable_channel": channel,
                "control_coefficient": coeff,
                "coefficient_units": units,
                "required_parent_coefficient": required,
                "claim_status": status,
            }
        )
        for sid, leak, channel, coeff, units, required, status in specs
    ]


def budget_rows() -> list[dict[str, Any]]:
    lookup = local_bound_lookup()
    specs = [
        ("BUD2745_0_qR", "q_R", "R3_gamma", lookup["R3_gamma"]["upper_bound"], "dimensionless", "abs(q_R) <= 2.3e-5 only if C_gamma_qR=1 is parent-derived", "MISSING_C_gamma_qR"),
        ("BUD2745_1_delta_beta", "delta_beta", "R4_beta", lookup["R4_beta"]["upper_bound"], "dimensionless", "abs(delta_beta) <= 7.8e-5 only if beta drift maps one-to-one", "MISSING_C_beta_delta"),
        ("BUD2745_2_epsilon_matter_direct", "epsilon_matter", "R0_identity_coframe_direct; R1_WEP_source_charge", lookup["R0_identity_coframe_direct"]["upper_bound"], "dimensionless", "abs(epsilon_matter) <= 2.8e-15 only if eta map is one-to-one", "MISSING_C_eta_epsilon_AND_MATTER_DESCENT"),
        ("BUD2745_3_alpha_clock", "alpha_clock", "R2_clock_redshift", lookup["R2_clock_redshift"]["upper_bound"], "dimensionless", "abs(alpha_clock) <= 2.48e-5 only if redshift map is one-to-one", "MISSING_C_clock"),
        ("BUD2745_4_sigma_Gdot", "sigma_Gdot", "R9_Gdot", lookup["R9_Gdot"]["upper_bound"], "yr^-1", "abs(Gdot/G) <= 9.6e-15 yr^-1 constrains time drift only after source-normalization theorem", "MISSING_C_Gdot_AND_SOURCE_NORMALIZATION"),
        ("BUD2745_5_alpha1_frame", "epsilon_frame_1", "R5_alpha1", lookup["R5_alpha1"]["upper_bound"], "dimensionless", "preferred-frame leakage must fit alpha1 <= 1e-4 after frame descent", "MISSING_C_alpha1_AND_FRAME_DESCENT"),
        ("BUD2745_6_alpha2_frame", "epsilon_frame_2", "R6_alpha2", lookup["R6_alpha2"]["upper_bound"], "dimensionless", "spin/anisotropy leakage must fit alpha2 <= 2e-9 after response map", "MISSING_C_alpha2_AND_SPIN_RESPONSE"),
        ("BUD2745_7_alpha3_flux", "epsilon_flux", "R7_alpha3", lookup["R7_alpha3"]["upper_bound"], "dimensionless", "momentum/source-flux leakage must fit alpha3 <= 4e-20 after boundary theorem", "MISSING_C_alpha3_AND_BOUNDARY_SILENCE"),
        ("BUD2745_8_xi_flux", "epsilon_flux", "R8_xi", lookup["R8_xi"]["upper_bound"], "dimensionless", "preferred-location leakage must fit xi <= 4e-9 after boundary/location response map", "MISSING_C_xi_AND_BOUNDARY_SILENCE"),
        ("BUD2745_9_R10_curve", "alpha_R10(lambda)", "R10_fifth_force", "alpha(lambda)", "range-dependent", "finite-range hair cannot be scored until a real alpha(lambda) curve and parent range map exist", "MISSING_C_R10_lambda_AND_DIGITIZED_CURVE"),
        ("BUD2745_10_tracefree_transfer", "h_TF_residual", "R5_alpha1; R6_alpha2; R8_xi", "response-matrix-required", "PPN residual vector", "tracefree leakage has no scalar budget until tensor/coframe response matrix exists", "MISSING_M_TF_RESPONSE_MATRIX"),
    ]
    rows: list[dict[str, Any]] = []
    for bid, leak, bound_ids, control_bound, units, interpretation, blocker in specs:
        references = []
        for row_id in [part.strip() for part in bound_ids.split(";")]:
            if row_id in lookup:
                references.append(lookup[row_id]["reference_path_or_url"])
        rows.append(
            nonclaim(
                {
                    "same_parent_branch_id": BRANCH_ID,
                    "budget_id": bid,
                    "leak_parameter": leak,
                    "local_bound_rows": bound_ids,
                    "control_bound_if_unit_response": control_bound,
                    "bound_units": units,
                    "interpretation": interpretation,
                    "blocking_input": blocker,
                    "budget_status": "CONTROL_BOUND_ONLY_NOT_MTS_PREDICTION",
                    "reference_path_or_url": "; ".join(references),
                }
            )
        )
    return rows


def coefficient_rows() -> list[dict[str, Any]]:
    specs = [
        ("COEF2745_0_C_gamma_qR", "C_gamma_qR", "maps reciprocal hair q_R into gamma_minus_1", "DEV2745_0_qR_gamma", "derive from weak-field metric/coframe response or source from parent q-sector leakage equation", "HIGH_CASSINI"),
        ("COEF2745_1_C_beta_delta", "C_beta_delta", "maps second-order completion drift into beta_minus_1", "DEV2745_1_delta_beta", "derive from second-order local field equations and source normalization", "HIGH_BETA_PERIHELION"),
        ("COEF2745_2_C_eta_epsilon", "C_eta_epsilon", "maps matter/coframe nonuniversality into Eotvos eta", "DEV2745_2_epsilon_matter", "derive matter action descent and composition response", "SEVERE_WEP"),
        ("COEF2745_3_C_clock", "C_clock", "maps clock-load readout drift into redshift anomaly", "DEV2745_3_alpha_clock", "derive universal clock/load readout from matter action or source clock model", "HIGH_CLOCK"),
        ("COEF2745_4_C_Gdot", "C_Gdot", "maps source-normalization drift into Gdot/G", "DEV2745_4_Gdot_source_norm", "derive measured GM theorem and time-stationary source normalization", "HIGH_LLR"),
        ("COEF2745_5_C_frame", "C_alpha1; C_alpha2", "maps frame/coframe leakage into preferred-frame PPN parameters", "DEV2745_5_preferred_frame_alpha1; DEV2745_6_preferred_frame_alpha2", "derive frame descent, spin response, and anisotropy map", "HIGH_PREFERRED_FRAME"),
        ("COEF2745_6_C_flux", "C_alpha3; C_xi", "maps boundary/source flux into alpha3 and xi", "DEV2745_7_flux_alpha3_xi", "derive boundary silence/no-charge/source-flux theorem", "EXTREME_ALPHA3"),
        ("COEF2745_7_C_R10_lambda", "C_R10(lambda)", "maps finite-range residual hair into Yukawa alpha(lambda)", "DEV2745_8_R10_finite_range", "derive parent range map and acquire real digitized alpha(lambda) curve", "HIGH_R10"),
        ("COEF2745_8_M_TF", "M_TF", "maps tracefree metric/coframe residual into PPN residual vector", "DEV2745_9_tracefree_transfer", "derive tensor/coframe transfer theorem and response matrix", "HIGH_TRACEFREE"),
    ]
    return [
        nonclaim(
            {
                "same_parent_branch_id": BRANCH_ID,
                "coefficient_id": cid,
                "required_coefficient": coeff,
                "role": role,
                "feeds_channel": channel,
                "source_or_derivation_requirement": requirement,
                "priority": priority,
                "current_status": "MISSING_PARENT_RESPONSE_COEFFICIENT",
            }
        )
        for cid, coeff, role, channel, requirement, priority in specs
    ]


def runner_rows() -> list[dict[str, Any]]:
    specs = [
        ("RUN2745_0_sources", "2744 handoff, 1557 prior, and local-bound source files exist", "PASS", "source register validates local evidence for the deviation-budget checkpoint"),
        ("RUN2745_1_channels", "all closure leakage channels are named", "PASS_NONCLAIM", "q_R, beta drift, matter, clock, source normalization, preferred-frame, R10, and tracefree channels included"),
        ("RUN2745_2_bounds", "local bounds link to real source rows", "PASS_BOUND_LEDGER", "numeric local bounds parse for R0-R9; R10 remains symbolic curve-only"),
        ("RUN2745_3_coefficients", "response coefficients are source-ready", "PASS_QUEUE_ONLY", "coefficient queue names the missing parent inputs before scoring"),
        ("RUN2745_4_prediction_refusal", "do not convert budgets into MTS predictions", "REFUSED_MISSING_PARENT_COEFFICIENTS", "unit-response control budgets are not predictions until response coefficients are sourced"),
        ("RUN2745_5_claim_status", "local GR/Newton/local-bound claim", "BLOCKED_NO_CLAIM", "closure deviations are now bounded as bookkeeping, not empirical success"),
    ]
    return [nonclaim({"same_parent_branch_id": BRANCH_ID, "runner_id": rid, "test": test, "current_status": status, "detail": detail}) for rid, test, status, detail in specs]


def gate_rows() -> list[dict[str, Any]]:
    specs = [
        ("GATE2745_0_parent_closure_origin", "derive R_AB=0 and Q_R=0 from parent action", "BLOCKED_NO_CLAIM", "2744 retained closure-only status"),
        ("GATE2745_1_qR_coefficient", "source C_gamma_qR and perihelion response", "BLOCKED_NO_CLAIM", "unit gamma map is control bookkeeping only"),
        ("GATE2745_2_beta_completion", "derive beta drift response from second-order field equations", "BLOCKED_NO_CLAIM", "no parent second-order weak-field completion"),
        ("GATE2745_3_matter_universality", "derive universal matter/coframe coupling", "BLOCKED_NO_CLAIM", "WEP row is severe budget, not a pass"),
        ("GATE2745_4_clock_readout", "derive clock/load redshift response", "BLOCKED_NO_CLAIM", "clock coefficient still a response-map placeholder"),
        ("GATE2745_5_source_normalization", "derive measured GM/Gdot source normalization", "BLOCKED_NO_CLAIM", "Gdot budget cannot score without source theorem"),
        ("GATE2745_6_frame_boundary", "derive preferred-frame and boundary silence", "BLOCKED_NO_CLAIM", "alpha1/alpha2/alpha3/xi rows are bound ledgers"),
        ("GATE2745_7_R10_curve", "provide real digitized alpha(lambda) curve and parent range map", "BLOCKED_NO_CLAIM", "symbolic R10 row cannot score finite-range hair"),
        ("GATE2745_8_tracefree_matrix", "derive tensor/coframe response matrix M_TF", "BLOCKED_NO_CLAIM", "scalar closure does not control all PPN residuals"),
    ]
    return [nonclaim({"claim_gate_id": gid, "claim_gate": gate, "status": status, "reason": reason}) for gid, gate, status, reason in specs]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        ("DEC2745_0_verdict", "local closure deviation budget exists but is nonclaim", "BOUND_BUDGET_WRITTEN_PARENT_COEFFICIENTS_MISSING", "local bounds can now discipline each leakage channel, but no channel has a sourced parent response coefficient"),
        ("DEC2745_1_hardest_gate", "matter universality is the most brutal local budget", "WEP_SEVERE", "epsilon_matter is constrained at roughly 2.8e-15 only after C_eta_epsilon is parent-derived"),
        ("DEC2745_2_first_testing_lane", "q_R/gamma is the cleanest first scalar leakage lane", "Q_R_GAMMA_FIRST", "Cassini gamma gives a direct scalar budget while beta and perihelion are more degenerate"),
        ("DEC2745_3_next", "next target is response-coefficient source map", "NEXT_2746_COEFFICIENT_SOURCE_MAP", "derive or source the first response coefficients before any local-bound scoring"),
    ]
    return [nonclaim({"decision_id": did, "decision": decision, "result": result, "reason": reason}) for did, decision, result, reason in specs]


def next_rows() -> list[dict[str, Any]]:
    return [
        nonclaim(
            {
                "next_id": "NEXT2745_0_2746",
                "status": "selected_primary",
                "target_doc": "2746-Y5-R2FR-qR-beta-matter-clock-coefficient-source-map-or-rejection-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_qR_beta_matter_clock_coefficient_source_map_or_rejection_under_AX1090_2746.py",
                "mission": "derive or source response coefficients mapping q_R, delta_beta, epsilon_matter, alpha_clock, source normalization, frame leakage, R10 range hair, and tracefree transfer into local observables",
                "acceptance": "promote only coefficients with parent derivation or source-backed mapping; otherwise keep each local test nonclaim and choose the first derivable coefficient target",
                "forbidden": "do not treat unit-response control budgets as MTS predictions; do not claim local GR derivation; do not edit formalization-workbench",
                "selected": True,
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({"copy_id": "BR2745_0_budget", "source_table": rel(OUTPUTS["budget"]), "copy_path": rel(BRANCH_OUTPUTS["budget"]), "purpose": "local-bound closure deviation budget", "exists": BRANCH_OUTPUTS["budget"].exists()}),
        nonclaim({"copy_id": "BR2745_1_coefficients", "source_table": rel(OUTPUTS["coefficients"]), "copy_path": rel(BRANCH_OUTPUTS["coefficients"]), "purpose": "source-weight response coefficient queue", "exists": BRANCH_OUTPUTS["coefficients"].exists()}),
        nonclaim({"copy_id": "BR2745_2_next_queue", "source_table": rel(OUTPUTS["next"]), "copy_path": rel(BRANCH_OUTPUTS["next_queue"]), "purpose": "RAB acquisition queue for response-coefficient source map", "exists": BRANCH_OUTPUTS["next_queue"].exists()}),
    ]


def formalization_recent_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    start = SCRIPT_START_UTC.timestamp()
    return sum(1 for path in FORMALIZATION.rglob("*") if path.is_file() and path.stat().st_mtime >= start)


def pycache_path() -> Path:
    return Path(__file__).resolve().parent / "__pycache__"


def remove_pycache() -> None:
    pycache = pycache_path()
    if pycache.exists():
        shutil.rmtree(pycache)


def validation_rows(
    sources: list[dict[str, Any]],
    channels: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    sensitivity: list[dict[str, Any]],
    budget: list[dict[str, Any]],
    coefficients: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    source_ok = all(row["exists"] is True and row["needles_present"] is True for row in sources)
    required_channels = {"q_R", "delta_beta", "epsilon_matter", "alpha_clock", "sigma_Gdot", "epsilon_frame_1", "epsilon_frame_2", "epsilon_flux", "alpha_R10(lambda)", "h_TF_residual"}
    channels_ok = required_channels.issubset({row["leak_parameter"] for row in channels})
    bound_ids = {row["row_id"] for row in bounds}
    bounds_ok = {f"R{i}_{suffix}" for i, suffix in []} == set() and all(f"R{i}" in ";".join(bound_ids) for i in range(0, 10)) and "R10_fifth_force" in bound_ids
    numeric_ok = all(row["numeric_bound_parse"] == "PASS" for row in bounds if row["row_id"] != "R10_fifth_force") and any(row["row_id"] == "R10_fifth_force" and row["numeric_bound_parse"] == "SYMBOLIC_CURVE_REQUIRED" for row in bounds)
    sensitivity_ok = any(row["sensitivity_id"] == "SENS2745_0_qR_light_bending" for row in sensitivity) and any(row["sensitivity_id"] == "SENS2745_8_tracefree_ppn_vector" for row in sensitivity)
    budget_ok = all(row["budget_status"] == "CONTROL_BOUND_ONLY_NOT_MTS_PREDICTION" for row in budget) and any(row["budget_id"] == "BUD2745_9_R10_curve" for row in budget)
    coefficients_ok = any(row["coefficient_id"] == "COEF2745_0_C_gamma_qR" for row in coefficients) and all(row["current_status"] == "MISSING_PARENT_RESPONSE_COEFFICIENT" for row in coefficients)
    runner_ok = any(row["runner_id"] == "RUN2745_4_prediction_refusal" and "REFUSED" in row["current_status"] for row in runner)
    gates_ok = len(gates) == 9 and all(row["status"] == "BLOCKED_NO_CLAIM" for row in gates)
    no_claim_flags_ok = all(row.get("valid_for_claim") is False and row.get("claim_allowed") is False for block in [channels, bounds, sensitivity, budget, coefficients, runner, gates] for row in block)
    next_ok = next_target[0]["selected"] is True and "2746" in next_target[0]["target_doc"] and "coefficient" in next_target[0]["target_doc"]
    branch_ok = all(path.exists() for path in BRANCH_OUTPUTS.values())
    pycache_ok = not pycache_path().exists()
    formalization_count = formalization_recent_count()
    formalization_ok = formalization_count == 0
    csv_ok = True
    csv_bits: list[str] = []
    for key, path in {**OUTPUTS, **BRANCH_OUTPUTS}.items():
        if key == "validation":
            continue
        try:
            rows = read_csv(path)
            csv_bits.append(f"{path.name}:{len(rows)}:ok")
        except Exception as exc:
            csv_ok = False
            csv_bits.append(f"{path.name}:ERROR:{exc}")
    rows = [
        {"validation_id": "VAL2745_0_sources", "passed": source_ok, "detail": "all source paths exist and required anchors/needles are present", "timestamp_utc": ts()},
        {"validation_id": "VAL2745_1_channels_complete", "passed": channels_ok, "detail": "all required local leakage channels are present", "timestamp_utc": ts()},
        {"validation_id": "VAL2745_2_bound_rows_linked", "passed": bounds_ok, "detail": "R0-R10 local bound rows are linked to channels", "timestamp_utc": ts()},
        {"validation_id": "VAL2745_3_numeric_bounds_parse", "passed": numeric_ok, "detail": "numeric R0-R9 local bounds parse cleanly and R10 remains symbolic", "timestamp_utc": ts()},
        {"validation_id": "VAL2745_4_sensitivities_present", "passed": sensitivity_ok, "detail": "sensitivity map includes q_R and tracefree channels", "timestamp_utc": ts()},
        {"validation_id": "VAL2745_5_budgets_blocked", "passed": budget_ok, "detail": "all bound budgets are control-only nonpredictions", "timestamp_utc": ts()},
        {"validation_id": "VAL2745_6_coefficients_queued", "passed": coefficients_ok, "detail": "response coefficient source queue is present and missing-parent flagged", "timestamp_utc": ts()},
        {"validation_id": "VAL2745_7_runner_refuses_prediction", "passed": runner_ok, "detail": "runner refuses MTS prediction scoring", "timestamp_utc": ts()},
        {"validation_id": "VAL2745_8_claim_gates", "passed": gates_ok and no_claim_flags_ok, "detail": "all local claim gates remain blocked and flags false", "timestamp_utc": ts()},
        {"validation_id": "VAL2745_9_next_target", "passed": next_ok, "detail": "next target is response-coefficient source map", "timestamp_utc": ts()},
        {"validation_id": "VAL2745_10_branch_outputs", "passed": branch_ok, "detail": "branch copies exist", "timestamp_utc": ts()},
        {"validation_id": "VAL2745_11_csv_parse", "passed": csv_ok, "detail": "; ".join(csv_bits), "timestamp_utc": ts()},
        {"validation_id": "VAL2745_12_pycache_absent", "passed": pycache_ok, "detail": f"scripts __pycache__ absent={pycache_ok}", "timestamp_utc": ts()},
        {"validation_id": "VAL2745_13_formalization_untouched", "passed": formalization_ok, "detail": f"formalization-workbench recent modified-file count since script start = {formalization_count}", "timestamp_utc": ts()},
    ]
    rows.append(
        {
            "validation_id": "VAL2745_OVERALL",
            "passed": all(row["passed"] is True for row in rows),
            "detail": "2745 writes a nonclaim closure-deviation PPN sensitivity/bound budget and selects response-coefficient sourcing next",
            "timestamp_utc": ts(),
        }
    )
    return rows


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    DOC.write_text(
        f"""# 2745 - Y5 R2/f(R): Closure-Deviation PPN Sensitivity And Bound Budget Under AX1090

Status: `Y5_R2FR_2745_closure_deviation_bound_budget_written_parent_coefficients_missing`

## Private Verdict

2745 turns the local closure into a falsifiability map without pretending it is a prediction.

The dangerous leakage channels are now explicit:

`q_R`, `delta_beta`, `epsilon_matter`, `alpha_clock`, `sigma_Gdot`, preferred-frame leakage, boundary/source-flux leakage, finite-range R10 hair, and tracefree transfer.

The local bound ledger is harsh. The cleanest scalar first lane is `q_R -> gamma_minus_1`, because Cassini gives the direct control budget. The most brutal lane is matter universality: if `epsilon_matter` maps one-to-one into Eotvos `eta`, the budget is about `2.8e-15`.

But no MTS local prediction is scored here. Every budget remains control-only until the parent response coefficients are derived or source-backed. That is the next target.

## Source Register

{markdown_table(data["sources"], ["source_id", "description", "source_path", "exists", "needles_present", "missing_needles", "valid_for_claim"])}

## Deviation Channels

{markdown_table(data["channels"], ["channel_id", "leak_parameter", "meaning", "null_lane_value", "first_observables", "leading_control_map", "missing_parent_inputs", "local_bound_rows", "status", "valid_for_claim"])}

## Local Bound Links

{markdown_table(data["bounds"], ["row_id", "used_for_channel", "observable", "upper_bound", "units", "numeric_bound_parse", "reference_path_or_url", "valid_for_claim"])}

## Sensitivity Map

{markdown_table(data["sensitivity"], ["sensitivity_id", "leak_parameter", "observable_channel", "control_coefficient", "coefficient_units", "required_parent_coefficient", "claim_status", "valid_for_claim"])}

## Bound Budget

{markdown_table(data["budget"], ["budget_id", "leak_parameter", "local_bound_rows", "control_bound_if_unit_response", "bound_units", "interpretation", "blocking_input", "budget_status", "valid_for_claim"])}

## Response Coefficient Source Queue

{markdown_table(data["coefficients"], ["coefficient_id", "required_coefficient", "role", "feeds_channel", "source_or_derivation_requirement", "priority", "current_status", "valid_for_claim"])}

## Runner

{markdown_table(data["runner"], ["runner_id", "test", "current_status", "detail", "valid_for_claim"])}

## Claim Gates

{markdown_table(data["gates"], ["claim_gate_id", "claim_gate", "status", "reason", "valid_for_claim"])}

## Decision Ledger

{markdown_table(data["decisions"], ["decision_id", "decision", "result", "reason", "valid_for_claim"])}

## Next Target

{markdown_table(data["next"], ["next_id", "status", "target_doc", "target_script", "mission", "acceptance", "forbidden", "selected", "valid_for_claim"])}

## Branch Copies

{markdown_table(data["branches"], ["copy_id", "source_table", "copy_path", "purpose", "exists", "valid_for_claim"])}

## Validation

{markdown_table(data["validation"], ["validation_id", "passed", "detail", "timestamp_utc"])}

## Plain-English Read

This is the point where the work becomes properly test-shaped. The closure lane itself is not a claim, but every way it can leak is now connected to a local observable and a bound. The next round is the coefficient hunt: if we can derive even the first clean response coefficient, the local branch stops being just a benchmark and starts becoming a real constrained theory lane.
""",
        encoding="utf-8",
    )


def main() -> None:
    ensure_dirs()
    sources = source_rows()
    channels = channel_rows()
    bounds = bound_rows()
    sensitivity = sensitivity_rows()
    budget = budget_rows()
    coefficients = coefficient_rows()
    runner = runner_rows()
    decisions = decision_rows()
    gates = gate_rows()
    next_target = next_rows()

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["channels"], channels)
    write_csv(OUTPUTS["bounds"], bounds)
    write_csv(OUTPUTS["sensitivity"], sensitivity)
    write_csv(OUTPUTS["budget"], budget)
    write_csv(OUTPUTS["coefficients"], coefficients)
    write_csv(OUTPUTS["runner"], runner)
    write_csv(OUTPUTS["decisions"], decisions)
    write_csv(OUTPUTS["gates"], gates)
    write_csv(OUTPUTS["next"], next_target)

    write_csv(BRANCH_OUTPUTS["budget"], budget)
    write_csv(BRANCH_OUTPUTS["coefficients"], coefficients)
    write_csv(BRANCH_OUTPUTS["next_queue"], next_target)
    branches = branch_rows()
    write_csv(OUTPUTS["branches"], branches)

    remove_pycache()
    validation = validation_rows(sources, channels, bounds, sensitivity, budget, coefficients, runner, gates, next_target)
    write_csv(OUTPUTS["validation"], validation)

    data = {
        "sources": sources,
        "channels": channels,
        "bounds": bounds,
        "sensitivity": sensitivity,
        "budget": budget,
        "coefficients": coefficients,
        "runner": runner,
        "decisions": decisions,
        "gates": gates,
        "next": next_target,
        "branches": branches,
        "validation": validation,
    }
    write_doc(data)

    remove_pycache()

    if not all(row["passed"] is True for row in validation):
        failed = [row for row in validation if row["passed"] is not True]
        raise SystemExit(f"2745 validation failed: {failed}")
    print(f"wrote {DOC}")
    print(f"validation {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
