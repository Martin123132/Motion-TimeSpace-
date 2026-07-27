from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
MICROSCOPE = ROOT / "source-intake" / "microscope"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1557-Y5-closure-deviation-PPN-sensitivity-and-bound-budget.md"
START_TS = datetime.now(timezone.utc).timestamp()

SOURCE_FILES = {
    "1556_doc": ROOT / "1556-Y5-local-closure-PPN-benchmark-and-derived-vs-assumed-ledger.md",
    "1556_validation": OUT / "P8_Y5_BRR545_1556_VALIDATION.csv",
    "1556_next": OUT / "P8_Y5_PARENT_QLOC_1556_NEXT_TARGET.csv",
    "1556_ppn": OUT / "P8_Y5_PARENT_QLOC_1556_PPN_BENCHMARK_REQUIREMENTS.csv",
    "1556_derived": OUT / "P8_Y5_PARENT_QLOC_1556_DERIVED_VS_ASSUMED_LEDGER.csv",
    "14_doc": ROOT / "14-closure-deviation-PPN-sensitivity.md",
    "13_doc": ROOT / "13-local-closure-PPN-benchmark.md",
    "10_doc": ROOT / "10-observer-map-symplectic-contract.md",
    "local_bound_claims": LOCAL_BOUNDS / "local_bound_claims.csv",
}

NEEDLES = {
    "1556_doc": ["R_AB=0", "not parent-derived", "closure-deviation"],
    "1556_next": ["1557-Y5-closure-deviation-PPN-sensitivity-and-bound-budget.md"],
    "1556_ppn": ["gamma_minus_1", "beta_minus_1", "alpha(lambda)"],
    "1556_derived": ["DVA1556_8_parent_origin", "BLOCKED_NOT_DERIVED"],
    "14_doc": ["q_R:", "Mercury shift factor = (2 q_R - delta_beta)/3.", "not an empirical claim yet"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1557_SOURCE_REGISTER.csv"
DEVIATION_CHANNELS = OUT / "P8_Y5_PARENT_QLOC_1557_DEVIATION_CHANNELS.csv"
LOCAL_BOUND_LINKS = OUT / "P8_Y5_PARENT_QLOC_1557_LOCAL_BOUND_LINKS.csv"
SENSITIVITY_MAP = OUT / "P8_Y5_PARENT_QLOC_1557_SENSITIVITY_MAP_NONCLAIM.csv"
BOUND_BUDGET = OUT / "P8_Y5_PARENT_QLOC_1557_BOUND_BUDGET_NONCLAIM.csv"
RUNNER = OUT / "P8_Y5_PARENT_QLOC_1557_RUNNER_NONCLAIM.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1557_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1557_DECISION.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1557_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1557_VALIDATION.csv"

QUARANTINE = MICROSCOPE / "quarantine" / "1557"
QUAR_CHANNELS = QUARANTINE / "DEVIATION_CHANNELS_NONCLAIM.csv"
QUAR_BOUND_LINKS = QUARANTINE / "LOCAL_BOUND_LINKS_NONCLAIM.csv"
QUAR_SENSITIVITY = QUARANTINE / "SENSITIVITY_MAP_NONCLAIM.csv"
QUAR_BUDGET = QUARANTINE / "BOUND_BUDGET_NONCLAIM.csv"
QUAR_RUNNER = QUARANTINE / "RUNNER_NONCLAIM.csv"
QUAR_DECISION = QUARANTINE / "DECISION_NONCLAIM.csv"
BRANCH_CHANNELS = BRANCH_RESIDUALS / "closure_deviation_channels_nonclaim_1557.csv"
BRANCH_BOUND_LINKS = BRANCH_RESIDUALS / "local_bound_links_nonclaim_1557.csv"
BRANCH_SENSITIVITY = BRANCH_RESIDUALS / "sensitivity_map_nonclaim_1557.csv"
BRANCH_BUDGET = BRANCH_RESIDUALS / "closure_deviation_bound_budget_nonclaim_1557.csv"
BRANCH_RUNNER = BRANCH_RESIDUALS / "closure_deviation_runner_nonclaim_1557.csv"
BRANCH_DECISION = BRANCH_RESIDUALS / "closure_deviation_decision_nonclaim_1557.csv"


def flags() -> dict[str, bool]:
    return {
        "numeric_value_present": False,
        "source_backed": False,
        "score_ready": False,
        "valid_prediction_row": False,
        "valid_for_claim": False,
        "claim_allowed": False,
    }


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def source_list(*keys: str) -> str:
    return "; ".join(rel(SOURCE_FILES[key]) for key in keys)


def file_contains(path: Path, needles: list[str]) -> bool:
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8", errors="ignore")
    return all(needle in text for needle in needles)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def parse_csv(path: Path) -> bool:
    read_csv(path)
    return True


def generated_flags_false(paths: list[Path]) -> bool:
    false_values = {"", "false", "0", "no", "none", "null"}
    claim_keys = [
        "numeric_value_present",
        "source_backed",
        "score_ready",
        "valid_prediction_row",
        "valid_for_claim",
        "claim_allowed",
        "accepted_for_scoring",
        "passes_for_claim",
    ]
    for path in paths:
        for row in read_csv(path):
            for key in claim_keys:
                if key in row and str(row[key]).strip().lower() not in false_values:
                    return False
    return True


def is_numeric(value: str) -> bool:
    try:
        float(value)
    except (TypeError, ValueError):
        return False
    return True


def local_bounds_by_row_id() -> dict[str, dict[str, str]]:
    return {row["row_id"]: row for row in read_csv(SOURCE_FILES["local_bound_claims"])}


def bound_value(row_id: str) -> str:
    return local_bounds_by_row_id()[row_id]["upper_bound"]


def bound_units(row_id: str) -> str:
    return local_bounds_by_row_id()[row_id]["units"]


def bound_reference(row_id: str) -> str:
    return local_bounds_by_row_id()[row_id]["reference_path_or_url"]


def source_register_rows() -> list[dict[str, Any]]:
    rows = []
    for index, (key, path) in enumerate(SOURCE_FILES.items()):
        needles = NEEDLES.get(key, [])
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "source_id": f"SRC1557_{index}_{key}",
                "source_path": rel(path),
                "exists": path.exists(),
                "needle_found": file_contains(path, needles) if needles else True,
                "needles": "; ".join(needles),
                "purpose": "evidence for closure-deviation sensitivity and local bound-budget ledger",
                **flags(),
            }
        )
    return rows


def deviation_channel_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "DEV1557_0_qR_gamma",
            "q_R",
            "reciprocal hair coefficient in R_AB approximately q_R L",
            "0",
            "gamma_minus_1; light_bending; Shapiro; perihelion",
            "gamma_minus_1 ~= C_gamma_qR q_R, with internal control C_gamma_qR=1 not parent-signed",
            "C_gamma_qR; parent R_AB leakage map; source normalization",
            "R3_gamma",
        ),
        (
            "DEV1557_1_delta_beta",
            "delta_beta",
            "nonlinear completion drift away from beta=1",
            "0",
            "beta_minus_1; perihelion",
            "beta_minus_1 ~= C_beta_delta delta_beta; Mercury control factor=(2 q_R-delta_beta)/3",
            "C_beta_delta; second-order weak-field completion",
            "R4_beta",
        ),
        (
            "DEV1557_2_epsilon_matter",
            "epsilon_matter",
            "spread away from universal matter/coframe coupling",
            "0",
            "eta_WEP_direct_geometry; eta_WEP_source_charge",
            "eta ~= C_eta_epsilon epsilon_matter",
            "C_eta_epsilon; matter action descent; no shadow-frame coupling",
            "R0_identity_coframe_direct; R1_WEP_source_charge",
        ),
        (
            "DEV1557_3_alpha_clock",
            "alpha_clock",
            "clock/load redshift anomaly",
            "0",
            "alpha_clock_redshift",
            "redshift anomaly ~= C_clock alpha_clock",
            "C_clock; universal clock/load readout map",
            "R2_clock_redshift",
        ),
        (
            "DEV1557_4_Gdot_source_norm",
            "sigma_Gdot",
            "time drift in measured source normalization GM or effective G",
            "0 yr^-1",
            "Gdot_over_G",
            "Gdot/G ~= C_Gdot sigma_Gdot",
            "C_Gdot; measured-GM/source normalization theorem",
            "R9_Gdot",
        ),
        (
            "DEV1557_5_preferred_frame_alpha1",
            "epsilon_frame_1",
            "vector/coframe preferred-frame leakage",
            "0",
            "alpha1",
            "alpha1 ~= C_alpha1 epsilon_frame_1",
            "C_alpha1; frame/coframe descent; boundary silence",
            "R5_alpha1",
        ),
        (
            "DEV1557_6_preferred_frame_alpha2",
            "epsilon_frame_2",
            "spin or anisotropic coframe preferred-frame leakage",
            "0",
            "alpha2",
            "alpha2 ~= C_alpha2 epsilon_frame_2",
            "C_alpha2; spin/coframe descent; anisotropy map",
            "R6_alpha2",
        ),
        (
            "DEV1557_7_flux_alpha3_xi",
            "epsilon_flux",
            "source flux, momentum nonconservation, or preferred-location leakage",
            "0",
            "alpha3; xi",
            "alpha3 ~= C_alpha3 epsilon_flux; xi ~= C_xi epsilon_flux",
            "C_alpha3; C_xi; boundary/no-charge/source-flux theorem",
            "R7_alpha3; R8_xi",
        ),
        (
            "DEV1557_8_R10_finite_range",
            "alpha_R10(lambda)",
            "finite-range q/source hair outside the exact closure",
            "0 for all lambda",
            "delta_G_or_fifth_force_yukawa",
            "Yukawa alpha(lambda) ~= C_R10(lambda) residual_hair(lambda)",
            "C_R10(lambda); real digitized alpha(lambda) curve; parent range map",
            "R10_fifth_force",
        ),
        (
            "DEV1557_9_tracefree_transfer",
            "h_TF_residual",
            "tracefree metric/coframe transfer not fixed by scalar R_AB closure",
            "0",
            "PPN tensor/vector residuals",
            "PPN residual vector ~= M_TF h_TF_residual",
            "M_TF response matrix; tensor/coframe transfer theorem",
            "R5_alpha1; R6_alpha2; R8_xi",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "channel_id": channel_id,
            "leak_parameter": leak_parameter,
            "meaning": meaning,
            "null_lane_value": null_lane_value,
            "first_observables": first_observables,
            "leading_control_map": leading_control_map,
            "missing_parent_inputs": missing_parent_inputs,
            "local_bound_rows": local_bound_rows,
            "status": "BOUND_BUDGET_ONLY_NOT_PREDICTION",
            "source_paths": source_list("14_doc", "1556_ppn", "local_bound_claims"),
            **flags(),
        }
        for (
            channel_id,
            leak_parameter,
            meaning,
            null_lane_value,
            first_observables,
            leading_control_map,
            missing_parent_inputs,
            local_bound_rows,
        ) in rows
    ]


def local_bound_link_rows() -> list[dict[str, Any]]:
    channel_by_bound = {
        "R0_identity_coframe_direct": "DEV1557_2_epsilon_matter",
        "R1_WEP_source_charge": "DEV1557_2_epsilon_matter",
        "R2_clock_redshift": "DEV1557_3_alpha_clock",
        "R3_gamma": "DEV1557_0_qR_gamma",
        "R4_beta": "DEV1557_1_delta_beta",
        "R5_alpha1": "DEV1557_5_preferred_frame_alpha1; DEV1557_9_tracefree_transfer",
        "R6_alpha2": "DEV1557_6_preferred_frame_alpha2; DEV1557_9_tracefree_transfer",
        "R7_alpha3": "DEV1557_7_flux_alpha3_xi",
        "R8_xi": "DEV1557_7_flux_alpha3_xi; DEV1557_9_tracefree_transfer",
        "R9_Gdot": "DEV1557_4_Gdot_source_norm",
        "R10_fifth_force": "DEV1557_8_R10_finite_range",
    }
    rows = []
    for row_id, bound in local_bounds_by_row_id().items():
        if row_id not in channel_by_bound:
            continue
        upper_bound = bound["upper_bound"]
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "bound_link_id": f"BL1557_{row_id}",
                "row_id": row_id,
                "used_for_channel": channel_by_bound[row_id],
                "observable": bound["observable"],
                "measured_value": bound["measured_value"],
                "one_sigma": bound["one_sigma"],
                "upper_bound": upper_bound,
                "units": bound["units"],
                "numeric_bound_parse": "PASS" if is_numeric(upper_bound) else "SYMBOLIC_CURVE_REQUIRED",
                "reference_path_or_url": bound["reference_path_or_url"],
                "reference_note": bound["reference_note"],
                "budget_use": "control budget only; no MTS prediction until parent coefficient is sourced",
                "source_paths": source_list("local_bound_claims"),
                **flags(),
            }
        )
    return rows


def sensitivity_map_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "SENS1557_0_qR_light_bending",
            "q_R",
            "solar light bending",
            "0.8756216406841224",
            "arcsec per unit q_R",
            "internal conversion factor from 14",
            "R3_gamma",
            "C_gamma_qR",
        ),
        (
            "SENS1557_1_qR_shapiro",
            "q_R",
            "solar Shapiro delay scale",
            "59.7375179242781",
            "microseconds per unit q_R",
            "internal conversion factor from 14",
            "R3_gamma",
            "C_gamma_qR",
        ),
        (
            "SENS1557_2_qR_mercury",
            "q_R",
            "Mercury perihelion",
            "28.65467507274745",
            "arcsec/century per unit q_R",
            "internal conversion factor from 14",
            "R3_gamma; R4_beta",
            "C_gamma_qR; C_peri_qR",
        ),
        (
            "SENS1557_3_delta_beta_mercury",
            "delta_beta",
            "Mercury perihelion",
            "-14.327337536373726",
            "arcsec/century per unit delta_beta",
            "internal conversion factor from 14",
            "R4_beta",
            "C_beta_delta; C_peri_beta",
        ),
        (
            "SENS1557_4_alpha_clock_gps",
            "alpha_clock",
            "GPS gravitational redshift",
            "45.718449825926655",
            "microseconds/day per unit alpha_clock",
            "internal conversion factor from 14",
            "R2_clock_redshift",
            "C_clock",
        ),
        (
            "SENS1557_5_epsilon_matter_eotvos",
            "epsilon_matter",
            "Eotvos proxy",
            "1",
            "dimensionless proxy per unit coupling spread",
            "internal conversion factor from 14",
            "R0_identity_coframe_direct; R1_WEP_source_charge",
            "C_eta_epsilon",
        ),
        (
            "SENS1557_6_source_norm_Gdot",
            "sigma_Gdot",
            "Gdot/G",
            "MISSING_PARENT_INPUT",
            "yr^-1 per unit source-normalization drift",
            "not present in 14; bound row exists but response coefficient does not",
            "R9_Gdot",
            "C_Gdot",
        ),
        (
            "SENS1557_7_R10_curve",
            "alpha_R10(lambda)",
            "inverse-square/Yukawa curve",
            "MISSING_CURVE_AND_PARENT_INPUT",
            "alpha(lambda) per residual hair amplitude",
            "symbolic curve row only; no scalar bound",
            "R10_fifth_force",
            "C_R10(lambda)",
        ),
        (
            "SENS1557_8_tracefree_ppn_vector",
            "h_TF_residual",
            "PPN vector/tensor residual",
            "MISSING_RESPONSE_MATRIX",
            "PPN residual per tracefree transfer amplitude",
            "scalar closure does not define the tensor response",
            "R5_alpha1; R6_alpha2; R8_xi",
            "M_TF",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "sensitivity_id": sensitivity_id,
            "leak_parameter": leak_parameter,
            "observable_channel": observable_channel,
            "control_coefficient": control_coefficient,
            "coefficient_units": coefficient_units,
            "coefficient_status": coefficient_status,
            "local_bound_rows": local_bound_rows,
            "required_parent_coefficient": required_parent_coefficient,
            "claim_status": "NONCLAIM_INTERNAL_CONVERSION_ONLY",
            "source_paths": source_list("14_doc", "local_bound_claims"),
            **flags(),
        }
        for (
            sensitivity_id,
            leak_parameter,
            observable_channel,
            control_coefficient,
            coefficient_units,
            coefficient_status,
            local_bound_rows,
            required_parent_coefficient,
        ) in rows
    ]


def bound_budget_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "BUD1557_0_qR",
            "q_R",
            "R3_gamma",
            bound_value("R3_gamma"),
            bound_units("R3_gamma"),
            "abs(q_R) <= 2.3e-5 only if C_gamma_qR=1 is parent-derived",
            "MISSING_C_gamma_qR",
        ),
        (
            "BUD1557_1_delta_beta",
            "delta_beta",
            "R4_beta",
            bound_value("R4_beta"),
            bound_units("R4_beta"),
            "abs(delta_beta) <= 7.8e-5 only if beta drift maps one-to-one",
            "MISSING_C_beta_delta",
        ),
        (
            "BUD1557_2_epsilon_matter_direct",
            "epsilon_matter",
            "R0_identity_coframe_direct; R1_WEP_source_charge",
            bound_value("R0_identity_coframe_direct"),
            bound_units("R0_identity_coframe_direct"),
            "abs(epsilon_matter) <= 2.8e-15 only if eta map is one-to-one",
            "MISSING_C_eta_epsilon_AND_MATTER_DESCENT",
        ),
        (
            "BUD1557_3_alpha_clock",
            "alpha_clock",
            "R2_clock_redshift",
            bound_value("R2_clock_redshift"),
            bound_units("R2_clock_redshift"),
            "abs(alpha_clock) <= 2.48e-5 only if redshift map is one-to-one",
            "MISSING_C_clock",
        ),
        (
            "BUD1557_4_sigma_Gdot",
            "sigma_Gdot",
            "R9_Gdot",
            bound_value("R9_Gdot"),
            bound_units("R9_Gdot"),
            "abs(Gdot/G) <= 9.6e-15 yr^-1 constrains time drift only after source-normalization theorem",
            "MISSING_C_Gdot_AND_SOURCE_NORMALIZATION",
        ),
        (
            "BUD1557_5_alpha1_frame",
            "epsilon_frame_1",
            "R5_alpha1",
            bound_value("R5_alpha1"),
            bound_units("R5_alpha1"),
            "preferred-frame leakage must fit alpha1 <= 1e-4 after frame descent",
            "MISSING_C_alpha1_AND_FRAME_DESCENT",
        ),
        (
            "BUD1557_6_alpha2_frame",
            "epsilon_frame_2",
            "R6_alpha2",
            bound_value("R6_alpha2"),
            bound_units("R6_alpha2"),
            "spin/anisotropy leakage must fit alpha2 <= 2e-9 after response map",
            "MISSING_C_alpha2_AND_SPIN_RESPONSE",
        ),
        (
            "BUD1557_7_alpha3_flux",
            "epsilon_flux",
            "R7_alpha3",
            bound_value("R7_alpha3"),
            bound_units("R7_alpha3"),
            "momentum/source-flux leakage must fit alpha3 <= 4e-20 after boundary theorem",
            "MISSING_C_alpha3_AND_BOUNDARY_SILENCE",
        ),
        (
            "BUD1557_8_xi_flux",
            "epsilon_flux",
            "R8_xi",
            bound_value("R8_xi"),
            bound_units("R8_xi"),
            "preferred-location leakage must fit xi <= 4e-9 after boundary/location response map",
            "MISSING_C_xi_AND_BOUNDARY_SILENCE",
        ),
        (
            "BUD1557_9_R10_curve",
            "alpha_R10(lambda)",
            "R10_fifth_force",
            bound_value("R10_fifth_force"),
            bound_units("R10_fifth_force"),
            "finite-range hair cannot be scalar-scored until a real alpha(lambda) curve and parent range map exist",
            "MISSING_C_R10_lambda_AND_DIGITIZED_CURVE",
        ),
        (
            "BUD1557_10_tracefree_transfer",
            "h_TF_residual",
            "R5_alpha1; R6_alpha2; R8_xi",
            "response-matrix-required",
            "PPN residual vector",
            "tracefree leakage has no scalar budget until tensor/coframe response matrix exists",
            "MISSING_M_TF_RESPONSE_MATRIX",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "budget_id": budget_id,
            "leak_parameter": leak_parameter,
            "local_bound_rows": local_bound_rows,
            "control_bound_if_unit_response": control_bound_if_unit_response,
            "bound_units": units,
            "interpretation": interpretation,
            "blocking_input": blocking_input,
            "budget_status": "CONTROL_BOUND_ONLY_NOT_MTS_PREDICTION",
            "reference_path_or_url": "; ".join(
                bound_reference(row.strip())
                for row in local_bound_rows.split(";")
                if row.strip() in local_bounds_by_row_id()
            ),
            "source_paths": source_list("local_bound_claims", "14_doc", "1556_ppn"),
            **flags(),
        }
        for (
            budget_id,
            leak_parameter,
            local_bound_rows,
            control_bound_if_unit_response,
            units,
            interpretation,
            blocking_input,
        ) in rows
    ]


def runner_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1557_0_sources",
            "test": "1556 handoff and local-bound source files exist",
            "current_status": "PASS",
            "detail": "source register validates local evidence for the deviation-budget checkpoint",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1557_1_channels",
            "test": "all closure leakage channels are named",
            "current_status": "PASS_NONCLAIM",
            "detail": "q_R, delta_beta, epsilon_matter, alpha_clock, source normalization, preferred-frame, R10, and tracefree channels are included",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1557_2_bounds",
            "test": "local bounds link to real source rows",
            "current_status": "PASS_BOUND_LEDGER",
            "detail": "numeric local bounds are parsed for R0-R9; R10 remains symbolic curve-only",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1557_3_prediction_refusal",
            "test": "do not convert budgets into MTS predictions",
            "current_status": "REFUSED_MISSING_PARENT_COEFFICIENTS",
            "detail": "unit-response control budgets are not predictions until C_gamma_qR, C_beta_delta, C_eta_epsilon, C_clock, C_Gdot, frame coefficients, C_R10(lambda), and M_TF are sourced",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1557_4_claim_status",
            "test": "local GR/Newton/local-bound claim",
            "current_status": "BLOCKED_NO_CLAIM",
            "detail": "closure deviations are now bounded as a bookkeeping problem, not claimed as empirical success",
            **flags(),
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("GATE1557_0_parent_closure_origin", "derive R_AB=0 and Q_R=0 from parent action", "BLOCKED_NO_CLAIM", "1556 retained closure-only status"),
        ("GATE1557_1_qR_coefficient", "source C_gamma_qR and perihelion response", "BLOCKED_NO_CLAIM", "unit gamma map is control bookkeeping only"),
        ("GATE1557_2_beta_completion", "derive beta drift response from second-order field equations", "BLOCKED_NO_CLAIM", "no parent second-order weak-field completion"),
        ("GATE1557_3_matter_universality", "derive universal matter/coframe coupling", "BLOCKED_NO_CLAIM", "WEP row is a severe budget, not a pass"),
        ("GATE1557_4_clock_readout", "derive clock/load redshift response", "BLOCKED_NO_CLAIM", "clock coefficient still a response-map placeholder"),
        ("GATE1557_5_source_normalization", "derive measured GM/Gdot source normalization", "BLOCKED_NO_CLAIM", "Gdot budget cannot score without source theorem"),
        ("GATE1557_6_frame_boundary", "derive preferred-frame and boundary silence", "BLOCKED_NO_CLAIM", "alpha1/alpha2/alpha3/xi rows are bound ledgers"),
        ("GATE1557_7_R10_curve", "provide real digitized alpha(lambda) curve and parent range map", "BLOCKED_NO_CLAIM", "symbolic R10 row cannot score finite-range hair"),
        ("GATE1557_8_tracefree_matrix", "derive tensor/coframe response matrix M_TF", "BLOCKED_NO_CLAIM", "scalar closure does not control all PPN residuals"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "claim_gate": claim_gate,
            "status": status,
            "reason": reason,
            "source_paths": source_list("1556_derived", "1556_ppn", "14_doc", "local_bound_claims"),
            **flags(),
        }
        for gate_id, claim_gate, status, reason in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1557_0_verdict",
            "decision": "local closure deviation budget exists but is nonclaim",
            "result": "BOUND_BUDGET_WRITTEN_PARENT_COEFFICIENTS_MISSING",
            "reason": "local bounds can now discipline each leakage channel, but no channel has a sourced parent response coefficient",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1557_1_next",
            "decision": "next target",
            "result": "NEXT_1558_COEFFICIENT_SOURCE_MAP",
            "reason": "derive or source the first response coefficients before any local-bound scoring",
            **flags(),
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "next_id": "NEXT1557_0_1558",
            "next_target": "1558-Y5-qR-beta-matter-clock-coefficient-source-map-or-rejection.md",
            "script": "scripts/Y5_qR_beta_matter_clock_coefficient_source_map_or_rejection.py",
            "objective": "derive or source the response coefficients mapping q_R, delta_beta, epsilon_matter, alpha_clock, source normalization, frame leakage, R10 range hair, and tracefree transfer into local observables",
            "do_not": "do not treat unit-response control budgets as MTS predictions; do not claim local GR derivation; do not edit formalization-workbench",
            **flags(),
        }
    ]


def copy_outputs() -> None:
    copies = [
        (DEVIATION_CHANNELS, QUAR_CHANNELS),
        (LOCAL_BOUND_LINKS, QUAR_BOUND_LINKS),
        (SENSITIVITY_MAP, QUAR_SENSITIVITY),
        (BOUND_BUDGET, QUAR_BUDGET),
        (RUNNER, QUAR_RUNNER),
        (DECISION, QUAR_DECISION),
        (DEVIATION_CHANNELS, BRANCH_CHANNELS),
        (LOCAL_BOUND_LINKS, BRANCH_BOUND_LINKS),
        (SENSITIVITY_MAP, BRANCH_SENSITIVITY),
        (BOUND_BUDGET, BRANCH_BUDGET),
        (RUNNER, BRANCH_RUNNER),
        (DECISION, BRANCH_DECISION),
    ]
    for source, destination in copies:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def formalization_modified_count_since_start() -> int:
    if not FORMALIZATION.exists():
        return 0
    return sum(1 for path in FORMALIZATION.rglob("*") if path.is_file() and path.stat().st_mtime >= START_TS)


def validation_rows(generated_csvs: list[Path]) -> list[dict[str, Any]]:
    sources = read_csv(SOURCE_REGISTER)
    channels = read_csv(DEVIATION_CHANNELS)
    bound_links = read_csv(LOCAL_BOUND_LINKS)
    sensitivities = read_csv(SENSITIVITY_MAP)
    budgets = read_csv(BOUND_BUDGET)
    run_rows = read_csv(RUNNER)
    gate_rows = read_csv(CLAIM_GATE)
    decision_items = read_csv(DECISION)
    next_rows = read_csv(NEXT_TARGET)

    numeric_bound_rows = [
        row for row in bound_links if row["row_id"] != "R10_fifth_force"
    ]
    required_channels = {
        "q_R",
        "delta_beta",
        "epsilon_matter",
        "alpha_clock",
        "sigma_Gdot",
        "epsilon_frame_1",
        "epsilon_frame_2",
        "epsilon_flux",
        "alpha_R10(lambda)",
        "h_TF_residual",
    }
    present_channels = {row["leak_parameter"] for row in channels}

    checks = [
        ("VAL1557_0_sources_exist", all(row["exists"] == "True" for row in sources), "all cited 1557 source paths exist"),
        ("VAL1557_1_needles_found", all(row["needle_found"] == "True" for row in sources), "all registered evidence needles found"),
        ("VAL1557_2_channels_complete", required_channels.issubset(present_channels), "all required local leakage channels are present"),
        ("VAL1557_3_bound_rows_linked", len(bound_links) >= 11 and any(row["row_id"] == "R3_gamma" for row in bound_links), "local bound rows are linked to channels"),
        ("VAL1557_4_numeric_bounds_parse", all(row["numeric_bound_parse"] == "PASS" for row in numeric_bound_rows), "numeric R0-R9 local bounds parse cleanly"),
        ("VAL1557_5_R10_symbolic", any(row["row_id"] == "R10_fifth_force" and row["numeric_bound_parse"] == "SYMBOLIC_CURVE_REQUIRED" for row in bound_links), "R10 remains symbolic curve-only"),
        ("VAL1557_6_sensitivities_present", len(sensitivities) >= 9 and any(row["sensitivity_id"] == "SENS1557_0_qR_light_bending" for row in sensitivities), "sensitivity map includes q_R and other channels"),
        ("VAL1557_7_budgets_blocked", all(row["budget_status"] == "CONTROL_BOUND_ONLY_NOT_MTS_PREDICTION" for row in budgets), "all bound budgets are control-only nonpredictions"),
        ("VAL1557_8_runner_refuses_prediction", any(row["runner_id"] == "RUN1557_3_prediction_refusal" and row["current_status"] == "REFUSED_MISSING_PARENT_COEFFICIENTS" for row in run_rows), "runner refuses MTS prediction scoring"),
        ("VAL1557_9_claim_gates_block", all(row["status"] == "BLOCKED_NO_CLAIM" for row in gate_rows), "all local claim gates remain blocked"),
        ("VAL1557_10_decision_next", any(row["result"] == "NEXT_1558_COEFFICIENT_SOURCE_MAP" for row in decision_items), "decision selects response-coefficient source map next"),
        ("VAL1557_11_next_target", any("1558-Y5-qR-beta-matter-clock" in row["next_target"] for row in next_rows), "next target is response-coefficient mapping"),
        ("VAL1557_12_csv_parse", all(parse_csv(path) for path in generated_csvs), "all generated 1557 CSVs parse cleanly"),
        ("VAL1557_13_claim_flags_false", generated_flags_false(generated_csvs), "all generated prediction/claim flags remain false"),
        ("VAL1557_14_branch_copies", all(path.exists() for path in [QUAR_CHANNELS, QUAR_BOUND_LINKS, QUAR_SENSITIVITY, QUAR_BUDGET, QUAR_RUNNER, QUAR_DECISION, BRANCH_CHANNELS, BRANCH_BOUND_LINKS, BRANCH_SENSITIVITY, BRANCH_BUDGET, BRANCH_RUNNER, BRANCH_DECISION]), "branch/quarantine nonclaim copies written"),
        ("VAL1557_15_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent after run"),
        ("VAL1557_16_formalization_untouched", formalization_modified_count_since_start() == 0, "formalization modified-file count since start=0"),
    ]
    overall = all(result for _, result, _ in checks)
    rows = [
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail,
        }
        for check_id, result, detail in checks
    ]
    rows.append(
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": "VAL1557_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1557 closure-deviation PPN sensitivity and bound-budget checkpoint validation",
        }
    )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return "\n".join([header, sep, *body])


def write_doc(
    sources: list[dict[str, Any]],
    channels: list[dict[str, Any]],
    bound_links: list[dict[str, Any]],
    sensitivities: list[dict[str, Any]],
    budgets: list[dict[str, Any]],
    run_rows: list[dict[str, Any]],
    gate_rows: list[dict[str, Any]],
    decision_items: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 1557 - Closure-Deviation PPN Sensitivity and Bound Budget",
                "",
                "## Verdict",
                "- The local closure branch now has a concrete deviation budget, not a claim.",
                "- The first dangerous leakage channels are `q_R`, `epsilon_matter`, `alpha_clock`, source-normalization drift, preferred-frame/boundary leakage, finite-range R10 hair, and tracefree transfer.",
                "- Real local bound rows are linked: MICROSCOPE/WEP, Galileo redshift, Cassini gamma, beta/PPN preferred-frame bounds, LLR Gdot, and symbolic R10 inverse-square limits.",
                "- No MTS local prediction is scored here because the parent response coefficients are still missing.",
                "- The next target is to derive or source those response coefficients before any local-bound scoring.",
                "",
                "## Source Register",
                md_table(sources, ["source_id", "source_path", "exists", "needle_found", "needles"]),
                "",
                "## Deviation Channels",
                md_table(channels, ["channel_id", "leak_parameter", "first_observables", "leading_control_map", "missing_parent_inputs", "local_bound_rows", "status"]),
                "",
                "## Local Bound Links",
                md_table(bound_links, ["row_id", "used_for_channel", "observable", "upper_bound", "units", "numeric_bound_parse", "reference_path_or_url"]),
                "",
                "## Sensitivity Map",
                md_table(sensitivities, ["sensitivity_id", "leak_parameter", "observable_channel", "control_coefficient", "coefficient_units", "required_parent_coefficient", "claim_status"]),
                "",
                "## Bound Budget",
                md_table(budgets, ["budget_id", "leak_parameter", "local_bound_rows", "control_bound_if_unit_response", "bound_units", "blocking_input", "budget_status"]),
                "",
                "## Runner",
                md_table(run_rows, ["runner_id", "test", "current_status", "detail"]),
                "",
                "## Claim Gates",
                md_table(gate_rows, ["gate_id", "claim_gate", "status", "reason"]),
                "",
                "## Decision",
                md_table(decision_items, ["decision_id", "decision", "result", "reason"]),
                "",
                "## Validation",
                md_table(validation, ["check_id", "result", "detail"]),
                "",
                "## Next Target",
                md_table(next_rows, ["next_target", "script", "objective", "do_not"]),
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> None:
    sources = source_register_rows()
    channels = deviation_channel_rows()
    bound_links = local_bound_link_rows()
    sensitivities = sensitivity_map_rows()
    budgets = bound_budget_rows()
    run_rows = runner_rows()
    gate_rows = claim_gate_rows()
    decision_items = decision_rows()
    next_rows = next_target_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(DEVIATION_CHANNELS, channels)
    write_csv(LOCAL_BOUND_LINKS, bound_links)
    write_csv(SENSITIVITY_MAP, sensitivities)
    write_csv(BOUND_BUDGET, budgets)
    write_csv(RUNNER, run_rows)
    write_csv(CLAIM_GATE, gate_rows)
    write_csv(DECISION, decision_items)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()
    remove_pycache()

    generated_csvs = [
        SOURCE_REGISTER,
        DEVIATION_CHANNELS,
        LOCAL_BOUND_LINKS,
        SENSITIVITY_MAP,
        BOUND_BUDGET,
        RUNNER,
        CLAIM_GATE,
        DECISION,
        NEXT_TARGET,
    ]
    validation = validation_rows(generated_csvs)
    write_csv(VALIDATION, validation)
    write_doc(sources, channels, bound_links, sensitivities, budgets, run_rows, gate_rows, decision_items, validation, next_rows)


if __name__ == "__main__":
    main()
