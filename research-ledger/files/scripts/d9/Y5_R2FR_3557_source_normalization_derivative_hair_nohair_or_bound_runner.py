from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
DOC = ROOT / "3557-Y5-R2FR-source-normalization-derivative-hair-nohair-or-bound-runner.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

BRANCH_ID = "MTS_R2FR_Y5_SOURCE_NORMALIZATION_DERIVATIVE_HAIR_3557"
CHECKPOINT_ID = "3557"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"cannot write empty CSV: {path}")
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
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def source_paths() -> dict[str, Path]:
    return {
        "handoff_3556": RESIDUALS / "P8_Y5_R2FR_3556_NEXT_TARGET.csv",
        "theorem_3556": RESIDUALS / "P8_Y5_R2FR_3556_RENORMALIZED_G_THEOREM.csv",
        "channel_triage_3556": RESIDUALS / "P8_Y5_R2FR_3556_CHANNEL_TRIAGE.csv",
        "r11_targets_3556": RESIDUALS / "P8_Y5_R2FR_3556_R11_COEFFICIENT_TARGETS.csv",
        "derivative_hair_gate": RESIDUALS / "P8_CONSTANT_GM_DERIVATIVE_HAIR_GATE.csv",
        "derivative_hair_queue": RESIDUALS / "P8_CONSTANT_GM_DERIVATIVE_HAIR_FILL_QUEUE.csv",
        "constant_gm_zero_attempt": RESIDUALS / "P8_CONSTANT_GM_ZERO_THEOREM_ATTEMPT.csv",
        "calibration_lock_attempt": RESIDUALS / "P8_CALIBRATION_LOCK_ATTEMPT.csv",
        "charge_current_equality": RESIDUALS / "P8_charge_current_equality_DIRECT_ATTEMPT.csv",
        "constant_kappa_contract": RESIDUALS / "P8_constant_universal_Geff_kappa_CONTRACT.csv",
        "constant_sector_contract": RESIDUALS / "P8_constant_sector_universality_CONTRACT.csv",
        "ward_source_owner_contract": RESIDUALS / "P8_Ward_source_owner_identity_CONTRACT.csv",
        "source_current_ward_contract": RESIDUALS / "P8_source_current_Ward_universality_CONTRACT.csv",
        "no_species_contract": RESIDUALS / "P8_no_species_source_charge_CONTRACT.csv",
        "frame_source_split": RESIDUALS / "P8_frame_source_split_residual_or_zero.csv",
        "local_bounds": LOCAL_BOUNDS / "local_bound_claims.csv",
        "r10_bound_curve_live": LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_DIGITIZED.csv",
        "r10_bound_curve_anchors": LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_3012_NONCLAIM.csv",
        "r10_kernel_contract": LOCAL_BOUNDS / "R10_q_loc_to_Yukawa_kernel_contract_3013_NONCLAIM.csv",
        "r10_prediction_template": LOCAL_BOUNDS / "R10_prediction_row_template_3013_NONCLAIM.csv",
        "r10_demotion": LOCAL_BOUNDS / "R10_finite_range_demoted_to_local_closure_3014_NONCLAIM.csv",
        "r10_source_route_audit": LOCAL_BOUNDS / "R10_source_current_route_audit_3014_NONCLAIM.csv",
        "r10_provenance": LOCAL_BOUNDS / "P8_Y5_R10_BOUND_SOURCE_PROVENANCE.csv",
    }


def bound_by_row_id(local_bound_rows: list[dict[str, str]], row_id: str) -> dict[str, str]:
    for bound_row in local_bound_rows:
        if bound_row.get("row_id") == row_id:
            return bound_row
    return {}


def source_register_rows(sources: dict[str, Path]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for source_id, source_path in sources.items():
        rows.append(
            {
                "timestamp_utc": now(),
                "branch_id": BRANCH_ID,
                "checkpoint_id": CHECKPOINT_ID,
                "source_id": source_id,
                "source_path": str(source_path),
                "source_path_exists": source_path.exists(),
                "role": {
                    "handoff_3556": "declares 3557 target",
                    "theorem_3556": "imports measured-source split and derivative-hair law",
                    "channel_triage_3556": "imports nonconstant hair channels",
                    "r11_targets_3556": "imports source-normalization coefficient targets",
                    "derivative_hair_gate": "older exact derivative scorecard",
                    "derivative_hair_queue": "priority order for derivative hair fills",
                    "constant_gm_zero_attempt": "premise audit for constant GM theorem",
                    "calibration_lock_attempt": "calibration and same-frame lock clauses",
                    "charge_current_equality": "Hilbert charge/worldtube/Gauss route",
                    "constant_kappa_contract": "global coupling clauses",
                    "constant_sector_contract": "constant-sector and species-blindness clauses",
                    "ward_source_owner_contract": "Ward/source owner closure clauses",
                    "source_current_ward_contract": "source-current universality clauses",
                    "no_species_contract": "selector-blind source-charge clauses",
                    "frame_source_split": "existing frame source residual row",
                    "local_bounds": "empirical local bounds for Gdot, WEP, PPN, R10 symbolic row",
                    "r10_bound_curve_live": "live R10 curve status, currently placeholder",
                    "r10_bound_curve_anchors": "source-backed R10 anchor rows, nonclaim",
                    "r10_kernel_contract": "Yukawa/q_loc response kernel contract",
                    "r10_prediction_template": "R10 prediction row schema",
                    "r10_demotion": "R10 finite-range demotion/refusal status",
                    "r10_source_route_audit": "R10 source-current route audit",
                    "r10_provenance": "R10 external source provenance",
                }[source_id],
                "valid_for_claim": False,
            }
        )
    return rows


def nohair_theorem_rows(sources: dict[str, Path]) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "theorem_id": "NH3557_0_master_derivative_identity",
            "name": "master measured-source derivative identity",
            "statement": "For mu_obs=G_N M_H(1+sum_i epsilon_i), every probe derivative D satisfies D ln(mu_obs)=D ln(G_N)+D ln(M_H)+D ln(1+sum_i epsilon_i).",
            "proof_sketch": "Apply D to the logarithm of the 3556 measured-source split. No dynamics are used, so the identity is exact wherever the split is defined.",
            "parent_contract": "measured-source split from same observed branch",
            "result_if_signed": "turns vague source-normalization drift into channel-by-channel derivative rows",
            "status": "EXACT_IDENTITY",
            "source_path": str(sources["theorem_3556"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "theorem_id": "NH3557_1_global_coupling_nohair",
            "name": "global-coupling no-hair clause",
            "statement": "If kappa_eff is a parent superselection constant and has no dependence on time, radius, range, species, frame, domain, memory, or quotient invariants, then D ln(G_N)=0 for all local source-hair derivatives.",
            "proof_sketch": "The empirical G_N is a fixed representative of the parent coupling sector. A superselection parameter is not varied by local fields or source labels, so its pullback derivative along local/source probes vanishes.",
            "parent_contract": "d kappa_eff=0 and partial_Z/IQ/C/D/A/lambda/frame kappa_eff=0",
            "result_if_signed": "kills Gdot/radial/range/species/frame coupling drift",
            "status": "EXACT_CONDITIONAL_UNSIGNED",
            "source_path": str(sources["constant_kappa_contract"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "theorem_id": "NH3557_2_flux_gauss_nohair",
            "name": "Hilbert flux/Gauss no-radial-hair clause",
            "statement": "If Pi_M J_H is closed in the compact exterior and all non-Hilbert exterior source tails vanish, then D_t ln(M_H)=0 and partial_r ln(M_H)=0; the exterior force is inverse-square after constant G_N calibration.",
            "proof_sketch": "Integrating d(Pi_M J_H)=0 between nested spheres gives radius-independent enclosed mass. Stationary compact exterior plus no boundary/source flux gives time independence. The weak Gauss law then gives r^2 Phi'(r)=G_N M_H.",
            "parent_contract": "closed calibrated mass projector, compact support, zero owned boundary flux, no finite-range exterior tail",
            "result_if_signed": "kills radial source hair and Meff time drift at first Newton order",
            "status": "EXACT_CONDITIONAL_UNSIGNED",
            "source_path": str(sources["charge_current_equality"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "theorem_id": "NH3557_3_selector_blind_species_nohair",
            "name": "selector-blind source-charge no-hair clause",
            "statement": "If matter/source variation factors only through one observed coframe and universal constants, with no material marker or source-weight spurion, then Delta_AB ln(mu_obs)=0.",
            "proof_sketch": "The Hilbert source is the variation of the same matter action with respect to the same e_obs. If no species label enters the active gravitational coupling or source projector, differentiating the source charge across species/material labels gives zero.",
            "parent_contract": "S_m=sum_A S_A[Psi_A,e_obs,omega[e_obs],theta_univ] and no kappa_A/source marker",
            "result_if_signed": "kills source-charge/WEP hair",
            "status": "EXACT_CONDITIONAL_UNSIGNED",
            "source_path": str(sources["no_species_contract"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "theorem_id": "NH3557_4_same_frame_nohair",
            "name": "same-frame source pullback no-hair clause",
            "statement": "If source variation, matter motion, clocks, photons, and orbital readout are all pullbacks of the same parent observed coframe, then Delta_frame ln(mu_obs)=0.",
            "proof_sketch": "A frame split requires two nonidentical source/readout maps. If the parent quotient provides a single terminal e_obs before variation and readout, there is no independent frame derivative on the source strength.",
            "parent_contract": "one q-basic observed coframe used before source variation and before readout",
            "result_if_signed": "kills frame/source calibration split",
            "status": "EXACT_CONDITIONAL_UNSIGNED",
            "source_path": str(sources["frame_source_split"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "theorem_id": "NH3557_5_no_pole_range_nohair",
            "name": "no finite-range pole clause",
            "statement": "If the non-EH/q_loc source sector has no physical scalar/vector pole coupled to the measured source channel and no exterior tail, then alpha(lambda)=0 for the source-normalization R10 branch.",
            "proof_sketch": "A finite-range Yukawa term requires a parent-owned mode with lambda_i, source/test charges, and apparatus projection. If no such pole/current exists, the only allowed exterior monopole is the constant Hilbert charge already absorbed into G_N.",
            "parent_contract": "no parent finite-range eigenmode in the measured source channel, or source-current response exactly zero",
            "result_if_signed": "kills range/R10 source-normalization hair",
            "status": "EXACT_CONDITIONAL_UNSIGNED",
            "source_path": str(sources["r10_source_route_audit"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "theorem_id": "NH3557_6_no_cancellation_rule",
            "name": "no tuned cancellation rule",
            "statement": "A channel may be zero by theorem, or bounded by sourced coefficients; cancellation between independent hair channels is not evidence unless the parent action provides the cancellation identity before fitting.",
            "proof_sketch": "The derivative identity is a sum. A numerical cancellation at one epoch, source, radius, or range does not imply zero derivative as a function. Only a Ward/superselection/source identity can cancel terms for claim credit.",
            "parent_contract": "explicit parent Ward/superselection identity if cancellations are used",
            "result_if_signed": "prevents fake Newton/GR pass by fitted GM absorption",
            "status": "CLAIM_GUARD_EXACT",
            "source_path": str(sources["derivative_hair_gate"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def derivative_channel_rows(sources: dict[str, Path]) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "channel_id": "DH3557_0_time",
            "hair_channel": "time_drift",
            "derivative_operator": "D_t",
            "residual_symbol": "sigma_Gdot = d ln(mu_obs)/dt",
            "exact_formula": "sigma_Gdot=dlnG_N_dt+dlnM_H_dt+sum_i d epsilon_i/dt/(1+sum_i epsilon_i)",
            "zero_theorem_route": "global coupling superselection plus stationary calibrated Hilbert mass flux plus time-independent mu_extra",
            "current_parent_status": "UNSIGNED",
            "bound_route": "R9_Gdot",
            "bound_source_path": str(sources["local_bounds"]),
            "status": "BOUND_ROW_READY_IF_COEFFICIENT_SUPPLIED",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "channel_id": "DH3557_1_radial",
            "hair_channel": "radial_Meff_hair",
            "derivative_operator": "partial_r",
            "residual_symbol": "partial_r ln(mu_obs)",
            "exact_formula": "partial_r ln(mu_obs)=partial_r lnG_N+partial_r lnM_H+partial_r ln(1+sum_i epsilon_i)",
            "zero_theorem_route": "Gauss/no-hair exterior with closed Pi_M J_H and no non-EH exterior density/tail",
            "current_parent_status": "UNSIGNED",
            "bound_route": "profile envelope or R10 if finite-range tail",
            "bound_source_path": str(sources["derivative_hair_gate"]),
            "status": "PROFILE_REQUIRED_OR_THEOREM_ZERO",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "channel_id": "DH3557_2_range",
            "hair_channel": "finite_range_alpha_lambda",
            "derivative_operator": "D_lambda",
            "residual_symbol": "alpha(lambda)",
            "exact_formula": "nonzero source tail maps to V=V_N[1+alpha exp(-r/lambda)] or declared non-Yukawa kernel",
            "zero_theorem_route": "no physical finite-range pole/current in measured source channel",
            "current_parent_status": "UNSIGNED_AND_R10_CURVE_NOT_LIVE",
            "bound_route": "R10 alpha(lambda) curve comparator",
            "bound_source_path": str(sources["r10_bound_curve_live"]),
            "status": "BLOCKED_UNTIL_FULL_CURVE_AND_PREDICTION",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "channel_id": "DH3557_3_species",
            "hair_channel": "species_source_charge",
            "derivative_operator": "Delta_AB",
            "residual_symbol": "eta_source_AB",
            "exact_formula": "Delta_AB ln(mu_obs)=Delta_AB lnG_N+Delta_AB lnM_H+Delta_AB ln(1+sum_i epsilon_i)",
            "zero_theorem_route": "selector-blind matter/source action with universal source coupling",
            "current_parent_status": "UNSIGNED",
            "bound_route": "R1_WEP_source_charge",
            "bound_source_path": str(sources["local_bounds"]),
            "status": "BOUND_ROW_READY_IF_COEFFICIENT_SUPPLIED",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "channel_id": "DH3557_4_frame",
            "hair_channel": "frame_calibration_split",
            "derivative_operator": "Delta_frame",
            "residual_symbol": "delta_frame_source",
            "exact_formula": "Delta_frame ln(mu_obs)=Delta_frame lnG_N+Delta_frame lnM_H+Delta_frame ln(1+sum_i epsilon_i)",
            "zero_theorem_route": "one parent-selected e_obs/q/tau before source variation and readout",
            "current_parent_status": "UNSIGNED",
            "bound_route": "R0 direct geometry and R2 clock proxy until source-frame kernel exists",
            "bound_source_path": str(sources["local_bounds"]),
            "status": "PROXY_BOUND_ONLY_NOT_SOURCE_CLAIM",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "channel_id": "DH3557_5_domain_boundary",
            "hair_channel": "boundary_domain_projector_mass",
            "derivative_operator": "D_domain; boundary flux",
            "residual_symbol": "epsilon_boundary + c_domain_source_normalization_operator",
            "exact_formula": "epsilon_channel=mu_channel/(G_N M_H), with D epsilon_channel entering the master derivative law",
            "zero_theorem_route": "owned divergence has no compact exterior boundary flux and domain/projector mass is topological/invisible",
            "current_parent_status": "UNSIGNED",
            "bound_route": "PPN alpha3/xi/Gdot/R11 products",
            "bound_source_path": str(sources["local_bounds"]),
            "status": "COEFFICIENT_PRODUCTS_REQUIRED",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "channel_id": "DH3557_6_nonEH_q_loc",
            "hair_channel": "nonEH_operator_and_q_loc_source_projection",
            "derivative_operator": "operator projection",
            "residual_symbol": "epsilon_nonEH_source + C_qmu q_loc",
            "exact_formula": "Delta operator/source term divided by 4*pi*G_N rho_H or projected into PPN/R10 source coefficients",
            "zero_theorem_route": "EH-only local operator plus q_loc source projection zero",
            "current_parent_status": "UNSIGNED",
            "bound_route": "R3/R4/R10/R11/q_loc source kernels",
            "bound_source_path": str(sources["local_bounds"]),
            "status": "KERNEL_AND_COEFFICIENT_VECTOR_REQUIRED",
            "valid_for_claim": False,
        },
    ]


def empirical_bound_rows(sources: dict[str, Path], local_bound_rows: list[dict[str, str]]) -> list[dict[str, object]]:
    gdot_bound = bound_by_row_id(local_bound_rows, "R9_Gdot")
    source_charge_bound = bound_by_row_id(local_bound_rows, "R1_WEP_source_charge")
    direct_wep_bound = bound_by_row_id(local_bound_rows, "R0_identity_coframe_direct")
    clock_bound = bound_by_row_id(local_bound_rows, "R2_clock_redshift")
    gamma_bound = bound_by_row_id(local_bound_rows, "R3_gamma")
    beta_bound = bound_by_row_id(local_bound_rows, "R4_beta")
    alpha3_bound = bound_by_row_id(local_bound_rows, "R7_alpha3")
    xi_bound = bound_by_row_id(local_bound_rows, "R8_xi")
    r10_bound = bound_by_row_id(local_bound_rows, "R10_fifth_force")
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "bound_id": "B3557_0_Gdot",
            "hair_channel": "time_drift",
            "observable": "Gdot_over_G",
            "residual_symbol": "sigma_Gdot",
            "prediction_value": "MISSING_sigma_Gdot_parent_coefficient",
            "prediction_units": "yr^-1",
            "bound_value": gdot_bound.get("upper_bound", "MISSING_BOUND"),
            "bound_units": gdot_bound.get("units", "MISSING_UNITS"),
            "comparison_rule": "abs(sigma_Gdot) <= upper_bound after source-normalization projection is parent-owned",
            "reference_path_or_url": gdot_bound.get("reference_path_or_url", "MISSING_REFERENCE"),
            "score_status": "BLOCKED_MISSING_PARENT_COEFFICIENT",
            "valid_prediction_row": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "bound_id": "B3557_1_source_charge_WEP",
            "hair_channel": "species_source_charge",
            "observable": "eta_WEP_source_charge",
            "residual_symbol": "eta_source_AB",
            "prediction_value": "MISSING_eta_source_AB_parent_coefficient",
            "prediction_units": "dimensionless",
            "bound_value": source_charge_bound.get("upper_bound", "MISSING_BOUND"),
            "bound_units": source_charge_bound.get("units", "MISSING_UNITS"),
            "comparison_rule": "abs(eta_source_AB) <= upper_bound after source/test material map is declared",
            "reference_path_or_url": source_charge_bound.get("reference_path_or_url", "MISSING_REFERENCE"),
            "score_status": "BLOCKED_MISSING_PARENT_COEFFICIENT",
            "valid_prediction_row": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "bound_id": "B3557_2_frame_proxy",
            "hair_channel": "frame_calibration_split",
            "observable": "eta_WEP_direct_geometry; alpha_clock_redshift",
            "residual_symbol": "delta_frame_source",
            "prediction_value": "MISSING_delta_frame_source_kernel",
            "prediction_units": "dimensionless",
            "bound_value": f"WEP:{direct_wep_bound.get('upper_bound', 'MISSING')}; clock:{clock_bound.get('upper_bound', 'MISSING')}",
            "bound_units": "dimensionless_proxy",
            "comparison_rule": "proxy only until source-frame kernel maps delta_frame_source into WEP/clock rows",
            "reference_path_or_url": f"{direct_wep_bound.get('reference_path_or_url', 'MISSING_REFERENCE')} | {clock_bound.get('reference_path_or_url', 'MISSING_REFERENCE')}",
            "score_status": "PROXY_ONLY_NOT_CLAIM",
            "valid_prediction_row": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "bound_id": "B3557_3_R10_range",
            "hair_channel": "finite_range_alpha_lambda",
            "observable": "alpha(lambda)",
            "residual_symbol": "alpha_X(lambda_X)",
            "prediction_value": "MISSING_alpha_lambda_prediction_or_no_pole_theorem",
            "prediction_units": "dimensionless_plus_m",
            "bound_value": r10_bound.get("upper_bound", "alpha(lambda)"),
            "bound_units": r10_bound.get("units", "range-dependent"),
            "comparison_rule": "requires valid full curve row and matched lambda interpolation; anchor-only rows cannot score",
            "reference_path_or_url": r10_bound.get("reference_path_or_url", "MISSING_REFERENCE"),
            "score_status": "BLOCKED_R10_FULL_CURVE_AND_PREDICTION_MISSING",
            "valid_prediction_row": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "bound_id": "B3557_4_radial_profile",
            "hair_channel": "radial_Meff_hair",
            "observable": "partial_r_ln_mu_obs",
            "residual_symbol": "epsilon_radial_Meff(r)",
            "prediction_value": "MISSING_radial_profile_or_Gauss_nohair_certificate",
            "prediction_units": "inverse_length_or_dimensionless_shell_profile",
            "bound_value": "MISSING_RADIAL_PROFILE_BOUND_SOURCE",
            "bound_units": "profile_units",
            "comparison_rule": "zero theorem or source-backed profile envelope; do not hide radial hair in one fitted GM",
            "reference_path_or_url": str(sources["derivative_hair_gate"]),
            "score_status": "BLOCKED_PROFILE_SOURCE_MISSING",
            "valid_prediction_row": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "bound_id": "B3557_5_PPN_operator_source",
            "hair_channel": "nonEH_operator_and_q_loc_source_projection",
            "observable": "gamma_minus_1; beta_minus_1",
            "residual_symbol": "epsilon_nonEH_source; C_qmu q_loc",
            "prediction_value": "MISSING_PPN_source_projection_vector",
            "prediction_units": "dimensionless_vector",
            "bound_value": f"gamma:{gamma_bound.get('upper_bound', 'MISSING')}; beta:{beta_bound.get('upper_bound', 'MISSING')}",
            "bound_units": "dimensionless",
            "comparison_rule": "requires source-normalized PPN projection; first-order Newton does not imply beta/gamma pass",
            "reference_path_or_url": f"{gamma_bound.get('reference_path_or_url', 'MISSING_REFERENCE')} | {beta_bound.get('reference_path_or_url', 'MISSING_REFERENCE')}",
            "score_status": "BLOCKED_PPN_KERNEL_MISSING",
            "valid_prediction_row": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "bound_id": "B3557_6_boundary_domain_flux",
            "hair_channel": "boundary_domain_projector_mass",
            "observable": "alpha3; xi",
            "residual_symbol": "epsilon_boundary; c_domain_source_normalization_operator",
            "prediction_value": "MISSING_boundary_domain_flux_products",
            "prediction_units": "dimensionless_or_operator_units",
            "bound_value": f"alpha3:{alpha3_bound.get('upper_bound', 'MISSING')}; xi:{xi_bound.get('upper_bound', 'MISSING')}",
            "bound_units": "dimensionless",
            "comparison_rule": "each boundary/domain product must pass individually unless parent cancellation identity exists",
            "reference_path_or_url": f"{alpha3_bound.get('reference_path_or_url', 'MISSING_REFERENCE')} | {xi_bound.get('reference_path_or_url', 'MISSING_REFERENCE')}",
            "score_status": "BLOCKED_PRODUCTS_MISSING",
            "valid_prediction_row": False,
            "valid_for_claim": False,
        },
    ]


def runner_decision_rows(bound_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for bound_row in bound_rows:
        prediction_value = str(bound_row["prediction_value"])
        valid_prediction = bool(bound_row["valid_prediction_row"])
        if valid_prediction and "MISSING" not in prediction_value:
            runner_status = "READY_FOR_NUMERIC_COMPARISON"
        else:
            runner_status = "BLOCKED_NONCLAIM"
        rows.append(
            {
                "timestamp_utc": now(),
                "branch_id": BRANCH_ID,
                "checkpoint_id": CHECKPOINT_ID,
                "runner_id": f"RUN3557_{bound_row['bound_id']}",
                "hair_channel": bound_row["hair_channel"],
                "observable": bound_row["observable"],
                "input_prediction": prediction_value,
                "input_bound": bound_row["bound_value"],
                "decision": runner_status,
                "reason": "prediction row lacks parent coefficient/theorem-zero certificate"
                if runner_status == "BLOCKED_NONCLAIM"
                else "numeric comparison can be run",
                "claim_allowed": False,
                "valid_for_claim": False,
            }
        )
    return rows


def route_decision_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": "DEC3557_0",
            "decision": "The derivative-hair route is mathematically sharp but not parent-signed.",
            "meaning": "There is a clean theorem: global coupling + closed Hilbert flux + selector-blind same-frame source + no finite-range/non-EH source poles implies D epsilon_i=0.",
            "claim_effect": "No Newton/local-GR claim until those clauses are signed or each residual is bounded.",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": "DEC3557_1",
            "decision": "Two empirical rows are immediately usable as bound targets, not predictions.",
            "meaning": "R9 Gdot and R1 WEP/source-charge bounds have real local-bound rows; MTS still lacks parent coefficients to compare.",
            "claim_effect": "This is now executable once sigma_Gdot or eta_source_AB is derived.",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": "DEC3557_2",
            "decision": "R10 remains a closure-only/future-runner branch.",
            "meaning": "The Yukawa convention and alpha response law exist, but full bound curve, parent lambda/alpha prediction, and q_loc/source bridge are still missing.",
            "claim_effect": "No R10 pass/fail physics claim from 3557.",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": "DEC3557_3",
            "decision": "Next best leap is to sign the same-frame Hilbert source-current chain.",
            "meaning": "That one theorem would hit time drift, radial hair, source charge, frame split, and first-order Newton at once.",
            "claim_effect": "3558 should attack Pi_M J_H closure and e_obs source-variation ownership directly.",
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "next_id": "NEXT3557_0",
            "target_doc": "3558-Y5-R2FR-same-frame-Hilbert-source-current-closure-or-coefficient-fill.md",
            "target_script": "scripts/Y5_R2FR_3558_same_frame_Hilbert_source_current_closure_or_coefficient_fill.py",
            "objective": "derive the same-frame Hilbert source-current closure d(Pi_M J_H)=0 with one e_obs/q/tau branch, or fill the sigma_Gdot, eta_source_AB, radial profile, frame split, and mu_extra coefficient rows",
            "success_gate": "source-current closure signs the first-order Newton/source-normalization no-hair clauses, or every surviving channel has a source-ready bound row",
            "reason": "3557 shows the derivative-hair theorem hinges mostly on Pi_M J_H closure and same-frame source variation",
            "valid_for_claim": False,
        }
    ]


def validation_rows(
    sources: dict[str, Path],
    outputs: dict[str, Path],
    theorem_rows: list[dict[str, object]],
    channel_rows: list[dict[str, object]],
    bound_rows: list[dict[str, object]],
    runner_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    missing_sources = [str(source_path) for source_path in sources.values() if not source_path.exists()]
    rows.append(
        {
            "validation_id": "VAL3557_0_sources_exist",
            "passes": not missing_sources,
            "status": "PASS" if not missing_sources else "FAIL",
            "detail": f"{len(sources) - len(missing_sources)}/{len(sources)} cited source paths exist"
            if not missing_sources
            else "; ".join(missing_sources),
        }
    )

    parse_failures: list[str] = []
    for output_path in outputs.values():
        if output_path.suffix.lower() == ".csv":
            try:
                read_csv(output_path)
            except Exception as exc:  # pragma: no cover
                parse_failures.append(f"{output_path}: {exc}")
    rows.append(
        {
            "validation_id": "VAL3557_1_generated_csvs_parse",
            "passes": not parse_failures,
            "status": "PASS" if not parse_failures else "FAIL",
            "detail": f"{sum(1 for output_path in outputs.values() if output_path.suffix.lower() == '.csv')} generated CSV files parse"
            if not parse_failures
            else "; ".join(parse_failures),
        }
    )

    required_theorems = {"NH3557_1_global_coupling_nohair", "NH3557_2_flux_gauss_nohair", "NH3557_3_selector_blind_species_nohair", "NH3557_5_no_pole_range_nohair"}
    present_theorems = {str(row["theorem_id"]) for row in theorem_rows}
    missing_theorems = sorted(required_theorems - present_theorems)
    rows.append(
        {
            "validation_id": "VAL3557_2_nohair_theorem_clauses_present",
            "passes": not missing_theorems,
            "status": "PASS" if not missing_theorems else "FAIL",
            "detail": "global coupling, flux/Gauss, species, and range no-hair clauses present"
            if not missing_theorems
            else "; ".join(missing_theorems),
        }
    )

    required_bound_channels = {"time_drift", "species_source_charge", "finite_range_alpha_lambda", "radial_Meff_hair", "frame_calibration_split"}
    present_bound_channels = {str(row["hair_channel"]) for row in bound_rows}
    missing_bound_channels = sorted(required_bound_channels - present_bound_channels)
    rows.append(
        {
            "validation_id": "VAL3557_3_required_bound_rows_present",
            "passes": not missing_bound_channels,
            "status": "PASS" if not missing_bound_channels else "FAIL",
            "detail": "bound rows include Gdot, WEP/source-charge, R10 alpha(lambda), radial profile, and frame split"
            if not missing_bound_channels
            else "; ".join(missing_bound_channels),
        }
    )

    gdot_row = next((row for row in bound_rows if row["bound_id"] == "B3557_0_Gdot"), None)
    species_row = next((row for row in bound_rows if row["bound_id"] == "B3557_1_source_charge_WEP"), None)
    rows.append(
        {
            "validation_id": "VAL3557_4_real_bound_values_loaded",
            "passes": bool(gdot_row) and str(gdot_row["bound_value"]) == "9.6e-15" and bool(species_row) and str(species_row["bound_value"]) == "2.8e-15",
            "status": "PASS" if bool(gdot_row) and str(gdot_row["bound_value"]) == "9.6e-15" and bool(species_row) and str(species_row["bound_value"]) == "2.8e-15" else "FAIL",
            "detail": "loaded R9 Gdot=9.6e-15 yr^-1 and R1 source-charge WEP=2.8e-15",
        }
    )

    unsafe_claims = [
        str(row["runner_id"])
        for row in runner_rows
        if str(row.get("valid_for_claim", "")).lower() == "true" or str(row.get("claim_allowed", "")).lower() == "true"
    ]
    rows.append(
        {
            "validation_id": "VAL3557_5_runner_nonclaim_until_predictions",
            "passes": not unsafe_claims and all(str(row["decision"]) == "BLOCKED_NONCLAIM" for row in runner_rows),
            "status": "PASS" if not unsafe_claims and all(str(row["decision"]) == "BLOCKED_NONCLAIM" for row in runner_rows) else "FAIL",
            "detail": "runner blocks all rows until parent coefficients/theorem-zero certificates exist"
            if not unsafe_claims
            else "; ".join(unsafe_claims),
        }
    )

    r10_row = next((row for row in bound_rows if row["bound_id"] == "B3557_3_R10_range"), None)
    rows.append(
        {
            "validation_id": "VAL3557_6_R10_not_scored_from_anchors",
            "passes": bool(r10_row) and "BLOCKED_R10_FULL_CURVE" in str(r10_row["score_status"]),
            "status": "PASS" if bool(r10_row) and "BLOCKED_R10_FULL_CURVE" in str(r10_row["score_status"]) else "FAIL",
            "detail": "R10 remains blocked because full curve and prediction are missing",
        }
    )

    formalization_touched = any(FORMALIZATION in output_path.parents or output_path == FORMALIZATION for output_path in outputs.values())
    rows.append(
        {
            "validation_id": "VAL3557_7_formalization_workbench_untouched",
            "passes": not formalization_touched,
            "status": "PASS" if not formalization_touched else "FAIL",
            "detail": "3557 generated outputs only inside post-checkpoint-work",
        }
    )

    return rows


def write_doc(
    sources: dict[str, Path],
    outputs: dict[str, Path],
    theorem_rows: list[dict[str, object]],
    channel_rows: list[dict[str, object]],
    bound_rows: list[dict[str, object]],
    decision_rows: list[dict[str, object]],
    next_rows: list[dict[str, object]],
) -> None:
    lines = [
        "# 3557 - Source-normalization derivative-hair no-hair or bound runner",
        "",
        "## Verdict",
        "3557 turns the coupling throat into an exact no-hair theorem plus executable bound rows. The theorem is sharp: if the parent branch supplies global constant coupling, closed calibrated Hilbert flux, one observed source frame, selector-blind matter/source variation, and no finite-range/non-EH source pole, then every nonconstant source-normalization hair derivative vanishes.",
        "",
        "That is progress, but it is not a live claim. The parent has not yet signed those clauses together. The empirical side is now cleaner: `Gdot/G` and WEP/source-charge have real local bounds loaded; R10 remains blocked because the full bound curve and MTS alpha prediction are both missing.",
        "",
        "## Derived no-hair contract",
        "- `D ln(mu_obs)=D ln(G_N)+D ln(M_H)+D ln(1+sum_i epsilon_i)`.",
        "- `D ln(G_N)=0` if `kappa_eff` is a parent superselection constant.",
        "- `D_t ln(M_H)=partial_r ln(M_H)=0` if `Pi_M J_H` is closed in the compact exterior.",
        "- `Delta_AB ln(mu_obs)=0` if the active source action is selector-blind.",
        "- `Delta_frame ln(mu_obs)=0` if source variation and readout share one parent-selected `e_obs`.",
        "- `alpha(lambda)=0` if no finite-range parent pole/current couples to the measured source channel.",
        "",
        "## Bound runner status",
    ]
    for bound_row in bound_rows:
        lines.append(
            f"- `{bound_row['bound_id']}` `{bound_row['hair_channel']}` -> {bound_row['score_status']} "
            f"against `{bound_row['observable']}` bound `{bound_row['bound_value']}`."
        )
    lines.extend(
        [
            "",
            "## What this changes",
            "- The source-normalization problem is no longer vague: it is a finite list of derivative channels.",
            "- `Gdot/G` and source-charge WEP can be scored immediately once parent coefficients exist.",
            "- R10 is explicitly not scoreable from anchor-only curve rows.",
            "- The next best derivation is not another R10 hunt; it is same-frame Hilbert source-current closure.",
            "",
            "## What remains open",
            "- Parent proof of `d(Pi_M J_H)=0` in the compact exterior.",
            "- Parent proof that `Pi_M J_H` is the same source charge used by matter, clocks, photons, and orbits.",
            "- Parent proof that non-Hilbert/boundary/domain/q_loc source projections have zero mass monopole or bounded coefficients.",
            "- Source-normalized PPN beta/gamma and retained `T_extra` stress gates.",
            "",
            "## Generated outputs",
        ]
    )
    for output_name, output_path in outputs.items():
        lines.append(f"- `{output_name}`: `{output_path}`")
    lines.extend(
        [
            "",
            "## Key theorem rows",
        ]
    )
    for theorem_row in theorem_rows:
        lines.append(f"- `{theorem_row['theorem_id']}`: {theorem_row['statement']}")
    lines.extend(
        [
            "",
            "## Decision ledger",
        ]
    )
    for decision_row in decision_rows:
        lines.append(f"- `{decision_row['decision_id']}`: {decision_row['decision']} {decision_row['meaning']}")
    lines.extend(
        [
            "",
            "## Next target",
            f"- `{next_rows[0]['target_doc']}`",
            f"- Objective: {next_rows[0]['objective']}",
            "",
            "## Sources",
        ]
    )
    for source_id, source_path in sources.items():
        lines.append(f"- `{source_id}`: `{source_path}`")
    DOC.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    RESIDUALS.mkdir(parents=True, exist_ok=True)
    sources = source_paths()
    local_bound_rows = read_csv(sources["local_bounds"]) if sources["local_bounds"].exists() else []

    source_rows = source_register_rows(sources)
    theorem_rows = nohair_theorem_rows(sources)
    channel_rows = derivative_channel_rows(sources)
    bound_rows = empirical_bound_rows(sources, local_bound_rows)
    runner_rows = runner_decision_rows(bound_rows)
    decision_rows = route_decision_rows()
    next_rows = next_target_rows()

    outputs = {
        "source_register": RESIDUALS / "P8_Y5_R2FR_3557_SOURCE_REGISTER.csv",
        "nohair_theorem": RESIDUALS / "P8_Y5_R2FR_3557_DERIVATIVE_HAIR_NOHAIR_THEOREM.csv",
        "channel_matrix": RESIDUALS / "P8_Y5_R2FR_3557_DERIVATIVE_CHANNEL_MATRIX.csv",
        "bound_runner_input": RESIDUALS / "P8_Y5_R2FR_3557_DERIVATIVE_HAIR_BOUND_RUNNER_INPUT.csv",
        "runner_decision": RESIDUALS / "P8_Y5_R2FR_3557_DERIVATIVE_HAIR_RUNNER_DECISION.csv",
        "decision_ledger": RESIDUALS / "P8_Y5_R2FR_3557_DECISION_LEDGER.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3557_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3557_NEXT_TARGET.csv",
        "canonical_status": RESIDUALS / "P8_Y5_source_normalization_derivative_hair_status.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3557_VALIDATION.csv",
    }

    write_csv(outputs["source_register"], source_rows)
    write_csv(outputs["nohair_theorem"], theorem_rows)
    write_csv(outputs["channel_matrix"], channel_rows)
    write_csv(outputs["bound_runner_input"], bound_rows)
    write_csv(outputs["runner_decision"], runner_rows)
    write_csv(outputs["decision_ledger"], decision_rows)
    write_csv(
        outputs["status"],
        [
            {
                "timestamp_utc": now(),
                "branch_id": BRANCH_ID,
                "checkpoint_id": CHECKPOINT_ID,
                "status_id": "STAT3557_0",
                "status": "NOHAIR_CONTRACT_SHARPENED_BOUND_RUNNER_READY_NONCLAIM",
                "summary": "Derivative hair vanishes under a five-clause parent contract; Gdot and source-WEP bounds are loaded; all predictions remain blocked pending parent coefficients or theorem-zero certificates.",
                "claim_allowed": False,
                "valid_for_claim": False,
            }
        ],
    )
    write_csv(
        outputs["canonical_status"],
        [
            {
                "timestamp_utc": now(),
                "branch_id": BRANCH_ID,
                "checkpoint_id": CHECKPOINT_ID,
                "canonical_status": "Y5_DERIVATIVE_HAIR_BOUND_RUNNER_NONCLAIM_READY",
                "what_changed": "source-normalization hair is now finite-channel and empirically routed; same-frame Hilbert source-current closure is the next derivation target",
                "next_target": next_rows[0]["target_doc"],
                "claim_allowed": False,
                "valid_for_claim": False,
            }
        ],
    )
    write_csv(outputs["next_target"], next_rows)

    validation = validation_rows(sources, {key: path for key, path in outputs.items() if key != "validation"}, theorem_rows, channel_rows, bound_rows, runner_rows)
    write_csv(outputs["validation"], validation)
    write_doc(sources, outputs, theorem_rows, channel_rows, bound_rows, decision_rows, next_rows)

    for output_path in [DOC, *outputs.values()]:
        print(f"wrote {output_path}")


if __name__ == "__main__":
    main()
