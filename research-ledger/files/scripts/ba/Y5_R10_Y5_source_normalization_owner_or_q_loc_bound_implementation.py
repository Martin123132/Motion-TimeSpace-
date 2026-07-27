from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


STARTED = datetime.now(timezone.utc)
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1012-Y5-R10-Y5-source-normalization-owner-or-q_loc-bound-implementation.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def flag(value: object) -> bool:
    return str(value).strip().lower() == "true"


def missing(value: object) -> bool:
    text = str(value or "").strip()
    return text == "" or text.upper().startswith("MISSING") or text.startswith("FILL_")


def source_path(path_text: str) -> Path:
    path = Path(path_text)
    if path.is_absolute():
        return path
    return ROOT / path


def path_exists(path_text: str) -> bool:
    text = str(path_text or "").strip()
    if missing(text):
        return False
    if text in {"THEOREM_ONLY", "NUMERIC_REQUIRED", "NOT_SCOREABLE", "FORBIDDEN"}:
        return False
    return source_path(text).exists()


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def md_cell(value: object) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def md_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    return "\n".join(
        [
            "| " + " | ".join(columns) + " |",
            "| " + " | ".join("---" for _ in columns) + " |",
            *["| " + " | ".join(md_cell(row.get(col, "")) for col in columns) + " |" for row in rows],
        ]
    ) + "\n"


def source_register_rows() -> list[dict[str, str]]:
    specs = [
        ("SRC1012_0_1011_next", "source-intake/mts_residuals/P8_Y5_R10_1011_NEXT_TARGET.csv", "derive whether measured-GM/source normalization", "1011 handoff target."),
        ("SRC1012_1_1011_doc", "1011-Y5-R10-response-doublet-source-current-zero-or-q_loc-bound-fill.md", "Y5 source-normalization", "1011 summary: Y5 is root pressure."),
        ("SRC1012_2_1011_fill", "source-intake/mts_residuals/P8_Y5_R10_1011_QLOC_BOUND_FILL_ROWS.csv", "QBF1011_5_Y5_source_normalization", "prior q_loc Y5 bound row."),
        ("SRC1012_3_1011_decision", "source-intake/mts_residuals/P8_Y5_R10_1011_DECISION_LEDGER.csv", "DEC1011_1_Y5_is_root_pressure", "prior Y5 decision."),
        ("SRC1012_4_source_norm_stack", "source-intake/mts_residuals/P8_SOURCE_NORMALIZATION_THEOREM_STACK.csv", "S5_Newton_gate", "Newton/source-normalization theorem stack."),
        ("SRC1012_5_even_odd", "source-intake/mts_residuals/P8_SOURCE_NORMALIZATION_EVEN_ODD_SPLIT.csv", "E2_even_extra_source", "exchange oddness cannot kill even offsets."),
        ("SRC1012_6_r11_minimum", "source-intake/mts_residuals/P8_R11_SOURCE_NORMALIZATION_OPERATOR_MINIMUM_FILL.csv", "R11SN_0_radial_Meff_hair", "eight-channel R11 source-normalization fill."),
        ("SRC1012_7_r11_missing", "source-intake/mts_residuals/P8_R11_SOURCE_NORMALIZATION_MISSING_LEDGER.csv", "R11SN_7_absolute_calibration_offset", "missing ledger for R11 source-normalization."),
        ("SRC1012_8_r11_gates", "source-intake/mts_residuals/P8_R11_SOURCE_NORMALIZATION_ACCEPTANCE_GATES.csv", "G4_no_absorption_cheat", "source-normalization acceptance gates."),
        ("SRC1012_9_constant_gm_input", "source-intake/mts_residuals/P8_CONSTANT_GM_LOCAL_RESIDUAL_RUNNER_INPUT.csv", "P8_Meff_conservation", "constant-GM residual input rows."),
        ("SRC1012_10_constant_gm_matrix", "source-intake/mts_residuals/P8_CONSTANT_GM_RESIDUAL_BOUND_MATRIX.csv", "P8_Geff_time_drift", "constant-GM bound matrix."),
        ("SRC1012_11_mass_flux", "source-intake/mts_residuals/P8_mass_flux_projector_Euler_calibration_CONTRACT.csv", "MF5_absolute_calibration", "mass flux/projector calibration contract."),
        ("SRC1012_12_parent_identity", "source-intake/mts_residuals/P8_PARENT_SOURCE_IDENTITY_ATTEMPT.csv", "I499_3_parent_source_identity", "parent source identity obstruction."),
        ("SRC1012_13_worldtube_glue", "source-intake/mts_residuals/P8_PARENT_WORLDTUBE_GLUE_THEOREM_CLAUSES.csv", "W504_4_worldtube_source_measure_glue", "worldtube measured-mass glue."),
        ("SRC1012_14_newton_contract", "source-intake/mts_residuals/P8_Y5_R10_868_NEWTON_SOURCE_NORMALIZATION_CONTRACT.csv", "NS868_1_measured_GM", "Newton measured-GM contract."),
        ("SRC1012_15_mhref_source_norm", "source-intake/mts_residuals/P8_Y5_R10_697_MHREF_SOURCE_NORMALIZATION_CERTIFICATE.csv", "SNC697_9_verdict", "M_H_ref source-normalization certificate failure."),
        ("SRC1012_16_ppn_gdot_map", "source-intake/mts_residuals/P8_Y5_R10_708_PPN_GDOT_WEP_MAP.csv", "PGW708_3_R9_Gdot", "PPN/Gdot/WEP mapping gaps."),
    ]
    rows = []
    for source_id, path_text, needle, role in specs:
        path = source_path(path_text)
        text = path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""
        rows.append(
            {
                "source_id": source_id,
                "source_path": path_text,
                "exists": str(path.exists()).lower(),
                "needle": needle,
                "needle_found": str(needle in text).lower(),
                "role": role,
                "generated_utc": stamp(),
            }
        )
    return rows


def owner_theorem_rows() -> list[dict[str, str]]:
    rows = [
        {
            "clause_id": "Y5O1012_0_same_frame",
            "claim_piece": "matter, clocks, source current, and orbit use one observed coframe",
            "mathematical_form": "S_matter[psi,e_obs] defines J_H[e_obs] and the same e_obs defines rods/clocks/orbital readout",
            "current_evidence": "same-frame source certificate remains missing in SNC697_2 and source-normalization stack S0.",
            "status": "conditional_not_parent_derived",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "Y5O1012_1_constant_universal_coupling",
            "claim_piece": "G_eff/kappa is constant, universal, and source/range/species/frame blind",
            "mathematical_form": "partial_t,r,A,lambda,frame G_eff = 0",
            "current_evidence": "S1 and SNC697_6 are not parent-derived; constant-GM matrix keeps Gdot rows active.",
            "status": "not_parent_derived",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "Y5O1012_2_PiM_parent_origin",
            "claim_piece": "Pi_M is parent-owned before readout",
            "mathematical_form": "Pi_M: J_H -> H^2_abs(Sigma_ext) mass-flux class; no post-fit measured-GM mask",
            "current_evidence": "MF0/PM rows say projector origin and variation are conditional/not parent-derived.",
            "status": "not_parent_derived",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "Y5O1012_3_flux_closure",
            "claim_piece": "projected Hilbert mass flux is closed in compact exterior",
            "mathematical_form": "d(Pi_M J_H)=0 or -Pi_M dJ_extra+[d,Pi_M]J_H+A_parent=0",
            "current_evidence": "I499 gives exact obstruction identity but not zero; MF2 and MF4 remain conditional.",
            "status": "exact_obstruction_not_zero",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "Y5O1012_4_worldtube_glue",
            "claim_piece": "worldtube source measure equals exterior parent charge before orbital fitting",
            "mathematical_form": "M_source[W] = integral_S Q_M[tau] = M_eff",
            "current_evidence": "W504_4 remains not_yet_derived_core_missing_piece.",
            "status": "not_derived_core_missing_piece",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "Y5O1012_5_no_extra_mu_channels",
            "claim_piece": "mu_extra from boundary, bulk, domain, projector, memory, non-EH, species, time, and calibration channels is zero or bounded",
            "mathematical_form": "mu_obs = G_EH M_EH + sum_i mu_i, with every mu_i theorem-zero or row-scored",
            "current_evidence": "R11 minimum fill has eight missing/conditional channels; source-normalization decision forbids promotion.",
            "status": "retained_debt",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "Y5O1012_6_no_absorption_cheat",
            "claim_piece": "range/time/species/radial dependence is not absorbed into measured GM",
            "mathematical_form": "partial_r mu_extra = partial_t mu_extra = partial_A mu_extra = partial_lambda mu_extra = 0 or residual rows stay active",
            "current_evidence": "R11 gate G4 exists, but rows are unfilled; constant-GM matrix marks all relevant rows not scoreable.",
            "status": "rule_written_not_satisfied",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "Y5O1012_7_Newton_Poisson_orbit",
            "claim_piece": "same charge sources Poisson/Gauss and inverse-square orbital acceleration",
            "mathematical_form": "nabla^2 Phi=4 pi G_ref rho_H and a_r=-G_ref M_ref/r^2",
            "current_evidence": "NS868_0 is only conditional and SNC697_5 fails Poisson/Gauss/orbit calibration.",
            "status": "conditional_not_parent_derived",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "Y5O1012_8_verdict",
            "claim_piece": "measured-GM/source-normalization owner theorem",
            "mathematical_form": "Y5O1012_0 through Y5O1012_7 all parent-signed and no missing R11/source-normalization channels remain",
            "current_evidence": "current corpus has exact decomposition and no-cheat gates, but not the owner theorem or numeric coefficient fills.",
            "status": "fail_current_claim",
            "valid_for_claim": "false",
        },
    ]
    for row in rows:
        row["generated_utc"] = stamp()
    return rows


def coefficient_rows() -> list[dict[str, str]]:
    rows = [
        ("Y5C1012_0_radial_Meff_hair", "R11SN_0_radial_Meff_hair", "radial_Meff_hair", "epsilon_radial_Meff", "MISSING_RADIAL_NOHAIR_THEOREM_OR_NUMERIC_PROFILE", "dimensionless_or_profile_units_declared", "epsilon_radial_Meff = mu_radial_Meff_hair/(G_EH*M_EH)", "partial_r ln(mu_obs); beta_minus_1; alpha(lambda)", "R4;R10;R11", "zero radial hair or mapped PPN/fifth-force residuals", "source-intake/mts_residuals/P8_R11_SOURCE_NORMALIZATION_OPERATOR_MINIMUM_FILL.csv"),
        ("Y5C1012_1_boundary_monopole_shift", "R11SN_1_boundary_monopole_shift", "boundary_monopole_shift", "epsilon_boundary", "MISSING_BOUNDARY_NOHAIR_THEOREM_OR_NUMERIC_COEFFICIENT", "dimensionless", "epsilon_boundary = mu_boundary/(G_EH*M_EH)", "beta_minus_1; alpha3; xi; Gdot_over_G", "R4;R7;R8;R9;R11", "boundary nohair/no-flux theorem or coefficient bounds", "source-intake/mts_residuals/P8_R11_SOURCE_NORMALIZATION_OPERATOR_MINIMUM_FILL.csv"),
        ("Y5C1012_2_domain_projector_mass", "R11SN_2_domain_projector_mass", "domain_projector_mass", "epsilon_domain_projector", "MISSING_DOMAIN_PROJECTOR_ZERO_THEOREM_OR_NUMERIC_PRODUCTS", "dimensionless", "epsilon_domain_projector = mu_domain_projector/(G_EH*M_EH)", "alpha1; alpha2; alpha3; xi; R11", "R5;R6;R7;R8;R11", "domain no-vector/no-flux/no-anisotropy theorem or numeric products below gates", "source-intake/mts_residuals/P8_R11_SOURCE_NORMALIZATION_OPERATOR_MINIMUM_FILL.csv"),
        ("Y5C1012_3_bulk_X_Yukawa_tail", "R11SN_3_bulk_X_Yukawa_tail", "bulk_X_Yukawa_tail", "epsilon_bulk_X", "MISSING_BULK_MASS_GAP_THEOREM_OR_ALPHA_LAMBDA_CURVE", "dimensionless_plus_length_scale", "epsilon_bulk_X = mu_bulk_X/(G_EH*M_EH)", "alpha(lambda); R10 fifth force", "R10;R11", "positive source-free mass-gap theorem or alpha(lambda) curve below bounds", "source-intake/mts_residuals/P8_R11_SOURCE_NORMALIZATION_OPERATOR_MINIMUM_FILL.csv"),
        ("Y5C1012_4_nonEH_operator_potential", "R11SN_4_nonEH_operator_potential", "nonEH_operator_potential", "epsilon_nonEH_source", "MISSING_EH_ONLY_THEOREM_OR_NONEH_OPERATOR_COEFFICIENT_MAP", "dimensionless_or_operator_units_declared", "epsilon_nonEH_source = mu_nonEH_operator/(G_EH*M_EH)", "gamma_minus_1; beta_minus_1; alpha(lambda); R11", "R3;R4;R10;R11", "EH-only exterior theorem or coefficient vector with source paths and bounds", "source-intake/mts_residuals/P8_R11_SOURCE_NORMALIZATION_OPERATOR_MINIMUM_FILL.csv"),
        ("Y5C1012_5_species_source_charge", "R11SN_5_species_source_charge", "species_source_charge", "epsilon_species_A", "MISSING_SELECTOR_BLIND_SOURCE_THEOREM_OR_SPECIES_CHARGE_VECTOR", "dimensionless_by_species_pair", "epsilon_species_A = Delta_A mu_obs/(G_EH*M_EH)", "eta_WEP_source_charge; clock source residual", "R1;R2;R11", "selector-blind source theorem or eta_source_AB <= 2.8e-15 sourced vector", "source-intake/mts_residuals/P8_R11_SOURCE_NORMALIZATION_OPERATOR_MINIMUM_FILL.csv"),
        ("Y5C1012_6_time_drift", "R11SN_6_time_drift", "time_drift", "epsilon_time_drift", "MISSING_STATIONARITY_THEOREM_OR_TIME_DRIFT_COEFFICIENT", "dimensionless_or_per_time_with_map", "epsilon_time_drift = mu_time_drift/(G_EH*M_EH)", "Gdot_over_G", "R9;R11", "stationarity theorem or |Gdot/G| <= 9.6e-15 yr^-1 sourced row", "source-intake/mts_residuals/P8_R11_SOURCE_NORMALIZATION_OPERATOR_MINIMUM_FILL.csv"),
        ("Y5C1012_7_absolute_calibration_offset", "R11SN_7_absolute_calibration_offset", "absolute_calibration_offset", "epsilon_calibration", "MISSING_PARENT_FIXED_UNIVERSAL_CALIBRATION_THEOREM_OR_RETAINED_OFFSET", "dimensionless", "epsilon_calibration = mu_absolute_calibration_offset/(G_EH*M_EH)", "beta_minus_1; Gdot_over_G", "R4;R9;R11", "parent-fixed universal calibration with zero range/time/species derivatives", "source-intake/mts_residuals/P8_R11_SOURCE_NORMALIZATION_OPERATOR_MINIMUM_FILL.csv"),
    ]
    output = []
    for row in rows:
        output.append(
            {
                "coefficient_id": row[0],
                "source_row": row[1],
                "channel": row[2],
                "coefficient_symbol": row[3],
                "coefficient_value_or_theorem": row[4],
                "coefficient_units": row[5],
                "normalization": row[6],
                "observable_link": row[7],
                "affected_rows": row[8],
                "bound_or_required_repair": row[9],
                "source_path": row[10],
                "current_status": "retained_unfilled",
                "claim_path": "derived_zero_or_numeric_bound_required",
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return output


def constant_gm_rows() -> list[dict[str, str]]:
    rows = [
        ("GM1012_0_Geff_time_drift", "dln_Geff_dt", "Gdot_over_G", "MISSING_NUMERIC_OR_DERIVED_ZERO_DRIFT", "yr^-1", "9.6e-15 yr^-1 or derived zero", "source-intake/mts_residuals/P8_CONSTANT_GM_LOCAL_RESIDUAL_RUNNER_INPUT.csv"),
        ("GM1012_1_Meff_conservation", "dln_Meff_dt", "beta_minus_1;Gdot_over_G", "MISSING_NUMERIC_OR_DERIVED_ZERO_MASS_FLUX", "yr^-1", "beta/Gdot locks or derived conservation", "source-intake/mts_residuals/P8_CONSTANT_GM_LOCAL_RESIDUAL_RUNNER_INPUT.csv"),
        ("GM1012_2_species_source_charge", "eta_source_AB", "eta_WEP_source_charge", "MISSING_NUMERIC_OR_DERIVED_ZERO_SOURCE_CHARGE", "dimensionless", "2.8e-15 or derived universal source charge", "source-intake/mts_residuals/P8_CONSTANT_GM_LOCAL_RESIDUAL_RUNNER_INPUT.csv"),
        ("GM1012_3_radial_source_hair", "partial_r_ln_mu_obs", "gamma_minus_1;beta_minus_1;alpha(lambda)", "MISSING_RADIAL_PROFILE_OR_DERIVED_ZERO", "inverse_length_or_dimensionless_envelope", "zero radial hair or mapped PPN/fifth-force residuals", "source-intake/mts_residuals/P8_CONSTANT_GM_LOCAL_RESIDUAL_RUNNER_INPUT.csv"),
        ("GM1012_4_range_dependence", "alpha(lambda)", "delta_G_or_fifth_force_yukawa", "MISSING_EXECUTABLE_ALPHA_LAMBDA_CURVE_OR_ZERO_THEOREM", "range-dependent", "verified alpha(lambda) bound curve or derived zero", "source-intake/mts_residuals/P8_CONSTANT_GM_LOCAL_RESIDUAL_RUNNER_INPUT.csv"),
        ("GM1012_5_frame_calibration_split", "delta_frame_source", "eta_WEP_direct_geometry;clock_redshift;operator_ledger", "MISSING_NUMERIC_OR_DERIVED_ZERO_FRAME_SPLIT", "dimensionless", "one observed frame or explicit residual below row locks", "source-intake/mts_residuals/P8_CONSTANT_GM_LOCAL_RESIDUAL_RUNNER_INPUT.csv"),
        ("GM1012_6_nonlinear_beta_source", "delta_beta_source", "beta_minus_1", "MISSING_SECOND_ORDER_PPN_SOURCE_VECTOR", "dimensionless", "7.8e-05 or derived second-order source closure", "source-intake/mts_residuals/P8_CONSTANT_GM_LOCAL_RESIDUAL_RUNNER_INPUT.csv"),
    ]
    output = []
    for row in rows:
        output.append(
            {
                "gm_row_id": row[0],
                "symbol": row[1],
                "observable_link": row[2],
                "predicted_value": row[3],
                "prediction_units": row[4],
                "bound_or_target": row[5],
                "source_path": row[6],
                "current_status": "retained_unfilled",
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return output


def evaluate_coefficient(row: dict[str, str]) -> dict[str, str]:
    reasons: list[str] = []
    if not path_exists(row["source_path"]):
        reasons.append("MISSING_EXISTING_SOURCE_PATH")
    if missing(row["coefficient_value_or_theorem"]):
        reasons.append("MISSING_COEFFICIENT_VALUE_OR_THEOREM")
    if missing(row["coefficient_units"]):
        reasons.append("MISSING_UNITS")
    if missing(row["normalization"]):
        reasons.append("MISSING_NORMALIZATION")
    if missing(row["observable_link"]):
        reasons.append("MISSING_OBSERVABLE_LINK")
    if row["current_status"] != "derived_zero" and row["current_status"] != "numeric_bound":
        reasons.append("RETAINED_UNFILLED_BLOCKS_CLAIM")
    if not flag(row["valid_for_claim"]):
        reasons.append("VALID_FOR_CLAIM_FALSE")
    claim_allowed = not reasons and flag(row["valid_for_claim"])
    return {
        "runner_id": row["coefficient_id"].replace("Y5C", "Y5R"),
        "coefficient_id": row["coefficient_id"],
        "channel": row["channel"],
        "verdict": "PASS_SOURCE_NORMALIZATION_COEFFICIENT" if claim_allowed else "RETAINED_NONCLAIM_SOURCE_NORMALIZATION_COEFFICIENT",
        "score_ready": "false",
        "claim_allowed": str(claim_allowed).lower(),
        "valid_for_claim": str(claim_allowed).lower(),
        "failure_reasons": ";".join(reasons),
        "generated_utc": stamp(),
    }


def evaluate_gm(row: dict[str, str]) -> dict[str, str]:
    reasons: list[str] = []
    if not path_exists(row["source_path"]):
        reasons.append("MISSING_EXISTING_SOURCE_PATH")
    if missing(row["predicted_value"]):
        reasons.append("MISSING_PREDICTED_VALUE_OR_THEOREM")
    if missing(row["prediction_units"]):
        reasons.append("MISSING_UNITS")
    if row["current_status"] != "derived_zero" and row["current_status"] != "numeric_bound":
        reasons.append("RETAINED_UNFILLED_BLOCKS_CLAIM")
    if not flag(row["valid_for_claim"]):
        reasons.append("VALID_FOR_CLAIM_FALSE")
    claim_allowed = not reasons and flag(row["valid_for_claim"])
    return {
        "runner_id": row["gm_row_id"].replace("GM", "GMR"),
        "gm_row_id": row["gm_row_id"],
        "symbol": row["symbol"],
        "verdict": "PASS_CONSTANT_GM_ROW" if claim_allowed else "RETAINED_NONCLAIM_CONSTANT_GM_ROW",
        "score_ready": "false",
        "claim_allowed": str(claim_allowed).lower(),
        "valid_for_claim": str(claim_allowed).lower(),
        "failure_reasons": ";".join(reasons),
        "generated_utc": stamp(),
    }


def runner_rows(coefficients: list[dict[str, str]], gm_rows: list[dict[str, str]]) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    return [evaluate_coefficient(row) for row in coefficients], [evaluate_gm(row) for row in gm_rows]


def claim_gate_rows(owner: list[dict[str, str]], coeff_runner: list[dict[str, str]], gm_runner: list[dict[str, str]]) -> list[dict[str, str]]:
    owner_failed = any(row["clause_id"] == "Y5O1012_8_verdict" and row["status"] == "fail_current_claim" for row in owner)
    coeffs_nonclaim = all(not flag(row["claim_allowed"]) for row in coeff_runner)
    gm_nonclaim = all(not flag(row["claim_allowed"]) for row in gm_runner)
    gates = [
        ("CG1012_0_Y5_owner", "measured-GM/source-normalization owner theorem passes", "false", "same-frame, Pi_M origin, flux closure, worldtube glue, and extra channels remain unsigned"),
        ("CG1012_1_R11_coefficients", "R11/source-normalization coefficient vector is claim-ready", "false", "eight channels remain missing theorem-zero or numeric coefficient values"),
        ("CG1012_2_constant_GM", "constant measured-GM branch is claim-ready", "false", "Gdot, M_eff conservation, radial/range/species/frame/beta rows remain unfilled"),
        ("CG1012_3_no_absorption", "measured-GM calibration is not hiding derivative hair", "false", "no-absorption rule exists but required rows are not scored"),
        ("CG1012_4_Htau_MHref_local_GR", "H_tau/M_H_ref/Newton/local-GR gates can reopen", "false", "Y5 source-normalization remains retained residual"),
        ("CG1012_5_bound_implementation", "Y5 bound implementation skeleton is installed", str(owner_failed and coeffs_nonclaim and gm_nonclaim).lower(), "owner theorem failed and all bound rows are explicit nonclaim rows"),
    ]
    return [
        {
            "gate_id": gate_id,
            "claim": claim,
            "gate_pass": gate_pass,
            "reason": reason,
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for gate_id, claim, gate_pass, reason in gates
    ]


def decision_rows() -> list[dict[str, str]]:
    rows = [
        {
            "decision_id": "DEC1012_0_owner_not_proved",
            "decision": "Y5 measured-GM/source-normalization ownership is not proved.",
            "because": "Pi_M origin, flux closure, worldtube source-measure glue, universal G, and eight mu_extra channels remain unsigned or unfilled.",
            "next_action": "attack Pi_M J_H flux closure and source-measure glue as the derivation route",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC1012_1_bound_skeleton_installed",
            "decision": "The R11/source-normalization and constant-GM bound skeleton is now staged under 1012.",
            "because": "all high-pressure rows are explicit and nonclaim instead of being hidden inside measured GM.",
            "next_action": "fill theorem-zero or numeric rows channel-by-channel",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC1012_2_next_root",
            "decision": "The next derivation target should be Pi_M J_H flux closure.",
            "because": "without d(Pi_M J_H)=0 or a scored obstruction, measured GM cannot reduce to Newton/GR.",
            "next_action": "derive or score -Pi_M dJ_extra + [d,Pi_M]J_H + A_parent in the compact exterior",
            "valid_for_claim": "false",
        },
    ]
    for row in rows:
        row["generated_utc"] = stamp()
    return rows


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_target": "1013-Y5-R10-PiM-JH-flux-closure-or-measured-GM-obstruction-score.md",
            "objective": "derive compact-exterior closure of d(Pi_M J_H)=0, or score the exact obstruction -Pi_M dJ_extra + [d,Pi_M]J_H + A_parent as the measured-GM/source-normalization residual",
            "include": "Pi_M, J_H, J_extra, commutator [d,Pi_M]J_H, A_parent, exterior annulus, worldtube glue, M_eff, radial/time/range/species residual maps, source paths",
            "exclude": "post-readout projector, fitted GM calibration, odd-symmetry overclaim, H_tau pass, M_H_ref pass, Newton/local-GR claim, GitHub action",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def formalization_changed_after_start() -> list[Path]:
    if not FORMALIZATION.exists():
        return []
    changed = []
    for path in FORMALIZATION.rglob("*"):
        if path.is_file() and datetime.fromtimestamp(path.stat().st_mtime, timezone.utc) >= STARTED:
            changed.append(path)
    return changed


def validation_rows(
    sources: list[dict[str, str]],
    owner: list[dict[str, str]],
    coefficients: list[dict[str, str]],
    gm_rows: list[dict[str, str]],
    coeff_runner: list[dict[str, str]],
    gm_runner: list[dict[str, str]],
    claims: list[dict[str, str]],
    decisions: list[dict[str, str]],
    next_target: list[dict[str, str]],
) -> list[dict[str, str]]:
    changed = formalization_changed_after_start()
    validations = [
        ("V1012_0_sources_exist", all(flag(row["exists"]) and flag(row["needle_found"]) for row in sources), "all source paths exist and needles are present"),
        ("V1012_1_owner_theorem_blocks_claim", any(row["clause_id"] == "Y5O1012_8_verdict" and row["status"] == "fail_current_claim" for row in owner) and all(not flag(row["valid_for_claim"]) for row in owner), "Y5 owner theorem remains nonclaim"),
        ("V1012_2_eight_channel_vector", len(coefficients) == 8 and {row["channel"] for row in coefficients} == {"radial_Meff_hair", "boundary_monopole_shift", "domain_projector_mass", "bulk_X_Yukawa_tail", "nonEH_operator_potential", "species_source_charge", "time_drift", "absolute_calibration_offset"}, "eight source-normalization channels are represented"),
        ("V1012_3_coefficient_rows_nonclaim", all(not flag(row["valid_for_claim"]) for row in coefficients) and all(row["current_status"] == "retained_unfilled" for row in coefficients), "coefficient rows remain retained/unfilled and nonclaim"),
        ("V1012_4_constant_GM_rows_nonclaim", len(gm_rows) >= 7 and all(not flag(row["valid_for_claim"]) for row in gm_rows), "constant-GM rows remain nonclaim"),
        ("V1012_5_coefficient_runner_refuses", len(coeff_runner) == len(coefficients) and all(row["verdict"] == "RETAINED_NONCLAIM_SOURCE_NORMALIZATION_COEFFICIENT" and not flag(row["claim_allowed"]) for row in coeff_runner), "coefficient runner refuses all unfilled rows"),
        ("V1012_6_GM_runner_refuses", len(gm_runner) == len(gm_rows) and all(row["verdict"] == "RETAINED_NONCLAIM_CONSTANT_GM_ROW" and not flag(row["claim_allowed"]) for row in gm_runner), "constant-GM runner refuses all unfilled rows"),
        ("V1012_7_Y5_rows_present", any(row["channel"] == "domain_projector_mass" for row in coefficients) and any(row["symbol"] == "dln_Meff_dt" for row in gm_rows), "Y5 domain/source-normalization and M_eff rows are present"),
        ("V1012_8_claim_gates_blocked", all(not flag(row["claim_allowed"]) and not flag(row["valid_for_claim"]) for row in claims), "Y5 owner, R11 coefficients, constant-GM, H_tau, M_H_ref, and local-GR claims stay blocked"),
        ("V1012_9_bound_implementation_written", any(row["gate_id"] == "CG1012_5_bound_implementation" and flag(row["gate_pass"]) for row in claims), "Y5 bound implementation skeleton is installed"),
        ("V1012_10_decision_written", any(row["decision_id"] == "DEC1012_2_next_root" for row in decisions), "Pi_M J_H flux closure next-root decision is written"),
        ("V1012_11_next_target_written", len(next_target) == 1 and "1013-Y5-R10-PiM-JH-flux-closure" in next_target[0]["next_target"], "1013 target row is present and nonclaim"),
        ("V1012_12_formalization_untouched", len(changed) == 0, f"formalization-workbench modified-file count since script start is {len(changed)}"),
    ]
    rows = [{"check_id": cid, "result": "pass" if passed else "fail", "detail": detail, "generated_utc": stamp()} for cid, passed, detail in validations]
    rows.insert(0, {"check_id": "V1012_SUMMARY", "result": "pass" if all(row["result"] == "pass" for row in rows) else "fail", "detail": "1012 Y5 source-normalization owner-or-bound validation summary", "generated_utc": stamp()})
    return rows


def write_doc(
    sources: list[dict[str, str]],
    owner: list[dict[str, str]],
    coefficients: list[dict[str, str]],
    gm_rows: list[dict[str, str]],
    coeff_runner: list[dict[str, str]],
    gm_runner: list[dict[str, str]],
    claims: list[dict[str, str]],
    decisions: list[dict[str, str]],
    next_target: list[dict[str, str]],
    validations: list[dict[str, str]],
) -> None:
    text = "\n".join(
        [
            "# 1012 Y5 R10 source-normalization owner or q_loc bound implementation",
            "",
            "**Status:** measured-GM/source-normalization ownership is not derived. The eight-channel R11/source-normalization vector and constant-GM residual rows are staged as explicit nonclaim bound inputs.",
            "",
            "**Claim ceiling:** no Y5 owner theorem, R11 source-normalization pass, constant-GM pass, Newton/GR reduction, H_tau, M_H_ref, or local-GR claim is allowed from 1012.",
            "",
            "## Source register",
            md_table(sources, ["source_id", "source_path", "exists", "needle_found", "role"]),
            "## Y5 owner theorem attempt",
            md_table(owner, ["clause_id", "claim_piece", "mathematical_form", "current_evidence", "status", "valid_for_claim"]),
            "## R11/source-normalization coefficient vector",
            md_table(coefficients, ["coefficient_id", "channel", "coefficient_symbol", "coefficient_value_or_theorem", "coefficient_units", "observable_link", "affected_rows", "current_status", "valid_for_claim"]),
            "## Constant-GM residual rows",
            md_table(gm_rows, ["gm_row_id", "symbol", "observable_link", "predicted_value", "prediction_units", "bound_or_target", "current_status", "valid_for_claim"]),
            "## Coefficient runner",
            md_table(coeff_runner, ["runner_id", "coefficient_id", "channel", "verdict", "score_ready", "claim_allowed", "failure_reasons"]),
            "## Constant-GM runner",
            md_table(gm_runner, ["runner_id", "gm_row_id", "symbol", "verdict", "score_ready", "claim_allowed", "failure_reasons"]),
            "## Claim gate",
            md_table(claims, ["gate_id", "claim", "gate_pass", "reason", "claim_allowed", "valid_for_claim"]),
            "## Decision ledger",
            md_table(decisions, ["decision_id", "decision", "because", "next_action", "valid_for_claim"]),
            "## Validation",
            md_table(validations, ["check_id", "result", "detail", "generated_utc"]),
            "## Next target",
            md_table(next_target, ["next_target", "objective", "include", "exclude", "valid_for_claim"]),
            "",
        ]
    )
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_register_rows()
    owner = owner_theorem_rows()
    coefficients = coefficient_rows()
    gm_rows = constant_gm_rows()
    coeff_runner, gm_runner = runner_rows(coefficients, gm_rows)
    claims = claim_gate_rows(owner, coeff_runner, gm_runner)
    decisions = decision_rows()
    next_target = next_target_rows()
    validations = validation_rows(sources, owner, coefficients, gm_rows, coeff_runner, gm_runner, claims, decisions, next_target)

    write_csv(OUT / "P8_Y5_R10_1012_SOURCE_REGISTER.csv", sources)
    write_csv(OUT / "P8_Y5_R10_1012_Y5_OWNER_THEOREM_ATTEMPT.csv", owner)
    write_csv(OUT / "P8_Y5_R10_1012_R11_SOURCE_NORMALIZATION_COEFFICIENT_VECTOR.csv", coefficients)
    write_csv(OUT / "P8_Y5_R10_1012_CONSTANT_GM_RESIDUAL_ROWS.csv", gm_rows)
    write_csv(OUT / "P8_Y5_R10_1012_COEFFICIENT_RUNNER.csv", coeff_runner)
    write_csv(OUT / "P8_Y5_R10_1012_CONSTANT_GM_RUNNER.csv", gm_runner)
    write_csv(OUT / "P8_Y5_R10_1012_CLAIM_GATE.csv", claims)
    write_csv(OUT / "P8_Y5_R10_1012_DECISION_LEDGER.csv", decisions)
    write_csv(OUT / "P8_Y5_R10_1012_NEXT_TARGET.csv", next_target)
    write_csv(OUT / "P8_Y5_BRR545_1012_VALIDATION.csv", validations)
    write_doc(sources, owner, coefficients, gm_rows, coeff_runner, gm_runner, claims, decisions, next_target, validations)


if __name__ == "__main__":
    main()
