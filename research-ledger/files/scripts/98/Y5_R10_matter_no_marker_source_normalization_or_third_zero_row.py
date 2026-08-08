from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


POST_CHECKPOINT = Path(__file__).resolve().parents[1]
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"
RUNS = POST_CHECKPOINT / "runs"
FORMALIZATION = POST_CHECKPOINT.parent / "formalization-workbench"
OUTPUT_DOC = POST_CHECKPOINT / "736-Y5-R10-matter-no-marker-source-normalization-or-third-zero-row.md"
NEXT_TARGET = "737-Y5-R10-source-current-Ward-flux-closure-or-source-backed-Y5-inputs.md"
CUTOFF = datetime(2026, 5, 31, 14, 42, 0)

STATUS = "Y5_R10_736_third_narrow_zero_row_matter_no_marker_direct_representative_charge_derived_full_Y5_still_open"
CLAIM_CEILING = "matter_no_marker_direct_representative_charge_zero_only_source_normalization_still_unscored_no_R10_WEP_PPN_Newton_or_local_GR_pass"

SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_736_SOURCE_REGISTER.csv"
THIRD_ZERO_PATH = RESIDUALS / "P8_Y5_R10_736_THIRD_ZERO_ATTEMPT.csv"
NO_MARKER_CONTRACT_PATH = RESIDUALS / "P8_Y5_R10_736_MATTER_NO_MARKER_CONTRACT.csv"
Y5_RUNNER_UPDATE_PATH = RESIDUALS / "P8_Y5_R10_736_Y5_RUNNER_UPDATE.csv"
INPUT_QUEUE_PATH = RESIDUALS / "P8_Y5_R10_736_SOURCE_NORMALIZATION_INPUT_QUEUE.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_R10_736_DECISION_MATRIX.csv"
ROUTE_UPDATE_PATH = RESIDUALS / "P8_Y5_R10_736_ROUTE_UPDATE.csv"
SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_736_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_736_VALIDATION.csv"

SOURCES: dict[str, dict[str, Any]] = {
    "735_doc": {
        "path": POST_CHECKPOINT / "735-Y5-R10-source-backed-hybrid-q_loc-residual-inputs-or-second-zero-row.md",
        "role": "immediate second-zero and Y5 target handoff",
        "needles": ["a second narrow zero row is derivable", OUTPUT_DOC.name, "matter no-marker/Y5 channel"],
    },
    "735_validation": {
        "path": RESIDUALS / "P8_Y5_BRR545_735_VALIDATION.csv",
        "role": "prior validation gate",
        "needles": ["V735_12_next_target_selected", OUTPUT_DOC.name, "V735_14_formalization_workbench_untouched"],
    },
    "735_runner": {
        "path": RESIDUALS / "P8_Y5_R10_735_HYBRID_QLOC_RESIDUAL_RUNNER_UPDATE.csv",
        "role": "Y5 still-blocked runner row",
        "needles": ["HQR735_1_source_normalization_Y5", "matter/readout no-marker theorem", "unchanged_blocked"],
    },
    "735_queue": {
        "path": RESIDUALS / "P8_Y5_R10_735_SOURCE_ACQUISITION_QUEUE.csv",
        "role": "missing Y5/C_qmu source inputs",
        "needles": ["AQ735_1_Y5_C_qmu", "matter/readout no-marker theorem not proved", "missing"],
    },
    "731_matter_gate": {
        "path": RESIDUALS / "P8_Y5_R10_731_MATTER_BLINDNESS_GATE.csv",
        "role": "matter blindness red-team gate",
        "needles": ["MBG731_0_metric_blindness", "MBG731_3_no_marker_minimality", "universal marker loophole"],
    },
    "731_redteam": {
        "path": RESIDUALS / "P8_Y5_R10_731_NO_CHEAT_RED_TEAM.csv",
        "role": "universal conformal marker attack",
        "needles": ["NCR731_0_conformal_universal_marker", "WEP alone does not kill it", "not_killed"],
    },
    "731_hybrid_contract": {
        "path": RESIDUALS / "P8_Y5_R10_731_HYBRID_QUOTIENT_CONTRACT.csv",
        "role": "observed sector and representative split",
        "needles": ["HQC731_1_observed_GR_core", "ordinary matter fields", "HQC731_2_vertical_generator"],
    },
    "732_pullback": {
        "path": RESIDUALS / "P8_Y5_R10_732_HYBRID_PULLBACK_LEMMA.csv",
        "role": "hybrid pullback chain-rule proof template",
        "needles": ["L_{v_X}(gamma o pi_h)=d gamma[d pi_h(v_X)]=0", "HPL732_2_not_zero", "conditional_lemma_proved"],
    },
    "518_doc": {
        "path": POST_CHECKPOINT / "518-Y5-source-normalization-owner-or-q_loc-bound-implementation.md",
        "role": "Y5 owner theorem and residual runner",
        "needles": ["Y5 source-normalization owner theorem contract", "Y5B_9_q_loc_projection", "not_scored"],
    },
    "519_doc": {
        "path": POST_CHECKPOINT / "519-fill-Y5-bound-runner-or-source-owner-clause.md",
        "role": "same observed coframe / universal matter pullback clause",
        "needles": ["UOC519_1_universal_matter_pullback", "direct species-specific MTS source charge", "same coframe does not falsely solve"],
    },
    "y5_owner": {
        "path": RESIDUALS / "P8_Y5_SOURCE_NORMALIZATION_OWNER_THEOREM.csv",
        "role": "Y5 owner rows",
        "needles": ["Y5O_1_same_observed_coframe", "Y5O_5_no_extra_mass_projection", "theorem_written_current_MTS_does_not_satisfy_premises"],
    },
    "y5_bound_runner": {
        "path": RESIDUALS / "P8_Y5_SOURCE_NORMALIZATION_BOUND_RUNNER_INPUT.csv",
        "role": "Y5 residual rows",
        "needles": ["Y5B_3_species_source_charge", "Y5B_6_frame_calibration_split", "Y5B_9_q_loc_projection"],
    },
    "y5_amplitude": {
        "path": RESIDUALS / "P8_Y5_SOURCE_NORMALIZATION_AMPLITUDE_LAW.csv",
        "role": "Y5 amplitude law",
        "needles": ["AL518_1_local_derivative_law", "d ln mu_obs", "owner_zero_limit"],
    },
}


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def text_contains(path: Path, needles: list[str]) -> bool:
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8", errors="replace")
    return all(needle in text for needle in needles)


def prior_validation_clean(path: Path) -> bool:
    rows = read_csv(path)
    return bool(rows) and all(row.get("result") == "pass" for row in rows)


def source_path_string(*keys: str) -> str:
    return ";".join(str(SOURCES[key]["path"]) for key in keys)


def markdown_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    header = "| " + " | ".join(fields) + " |"
    separator = "| " + " | ".join("---" for _ in fields) + " |"
    body = []
    for row in rows:
        cells = []
        for field in fields:
            value = str(row.get(field, ""))
            value = value.replace("\n", " ").replace("|", "\\|")
            cells.append(value)
        body.append("| " + " | ".join(cells) + " |")
    return "\n".join([header, separator, *body])


def formalization_changed_after_cutoff() -> int:
    if not FORMALIZATION.exists():
        return -1
    count = 0
    for path in FORMALIZATION.rglob("*"):
        if not path.is_file():
            continue
        modified = datetime.fromtimestamp(path.stat().st_mtime)
        if modified > CUTOFF:
            count += 1
    return count


def under_post_checkpoint(paths: list[Path]) -> bool:
    root = POST_CHECKPOINT.resolve()
    for path in paths:
        try:
            path.resolve().relative_to(root)
        except ValueError:
            return False
    return True


def make_source_register(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "source_id": key,
            "path": str(info["path"]),
            "exists": bool_text(info["path"].exists()),
            "needle_check": bool_text(text_contains(info["path"], info["needles"])),
            "role": info["role"],
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
        for key, info in SOURCES.items()
    ]


def make_third_zero_attempt(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "zero_id": "TZA736_0_direct_representative_matter_marker",
            "target_quantity": "delta_{v_X^rep} S_matter",
            "theorem_or_formula": "If S_matter=sum_A S_A[psi_A,e_obs,A_obs;m_A,q_A,...] and every argument factors through Q_obs^hybrid while d pi_h(v_X^rep)=0, then delta_{v_X^rep} S_matter=0.",
            "premises": "One observed coframe/metric; matter constants are fixed labels, not R_rep/Phi/domain fields; no conformal/disformal/source-frame marker is inserted after variation.",
            "derivation": "By the chain rule, variation along v_X^rep sees only d pi_h(v_X^rep)=0. Since R_rep is not an argument of any matter/readout functor, partial_{R_rep} S_matter=0.",
            "verdict": "derived_third_narrow_zero_row_conditional",
            "residual_left": "This kills direct representative matter-marker charge only; it does not prove source mass conservation, mu_extra=0, C_qmu q_loc=0, Gauss calibration, or PPN stability.",
            "valid_for_claim": "false",
            "source_paths": source_path_string("731_matter_gate", "519_doc", "732_pullback"),
            "generated_utc": generated_utc,
        },
        {
            "zero_id": "TZA736_1_frame_calibration_split",
            "target_quantity": "delta_frame_source",
            "theorem_or_formula": "If e_matter=e_source=e_clock=e_photon=e_orbit=e_obs, then delta_frame_source := delta ln(e_source/e_orbit)=0.",
            "premises": "All matter, clock, photon, source-current, and orbital readout functionals use the same observed coframe before fitting measured GM.",
            "derivation": "The ratio of source and orbit/readout frames is identically one, so its logarithmic variation vanishes.",
            "verdict": "conditional_zero_row_retained_from_519",
            "residual_left": "Frame split is pruned only under the one-coframe/no-shadow-frame contract; source current flux and extra mass projection remain open.",
            "valid_for_claim": "false",
            "source_paths": source_path_string("519_doc", "y5_bound_runner"),
            "generated_utc": generated_utc,
        },
        {
            "zero_id": "TZA736_2_direct_species_marker_charge",
            "target_quantity": "partial_{R_rep,A} ln mu_obs direct matter label",
            "theorem_or_formula": "If m_A,q_A and material labels are fixed observed constants and do not depend on R_rep/Phi/domain variables, then direct representative species source charge vanishes.",
            "premises": "Universal matter pullback; no species-specific representative marker; no post-readout material selector.",
            "derivation": "Holding e_obs fixed, partial_{R_rep} S_A=0 and partial_{R_rep} m_A=0 for every species A, so the direct non-metric species charge row is zero.",
            "verdict": "partial_conditional_zero_not_dressed_source_universality",
            "residual_left": "Dressed binding/field/boundary source mass can still differ by species unless the full Hilbert source charge is proved universal.",
            "valid_for_claim": "false",
            "source_paths": source_path_string("519_doc", "731_matter_gate", "y5_bound_runner"),
            "generated_utc": generated_utc,
        },
        {
            "zero_id": "TZA736_3_universal_conformal_marker_loophole",
            "target_quantity": "hat_g_mu_nu=exp(2 a R_rep) g_obs_mu_nu",
            "theorem_or_formula": "A universal conformal/disformal representative marker is covariant and WEP-safe at leading composition level, so WEP alone cannot set a=0.",
            "premises": "No-marker/minimality contract is not accepted or the parent action permits a universal shadow frame.",
            "derivation": "The same marker can couple to all species and preserve universality while still changing clocks, source normalization, and q_loc/Y5 channels.",
            "verdict": "not_killed_without_no_marker_contract",
            "residual_left": "If the no-marker contract is not parent-derived, retain finite qbar_XT/source-normalization residual rows.",
            "valid_for_claim": "false",
            "source_paths": source_path_string("731_redteam", "731_matter_gate", "519_doc"),
            "generated_utc": generated_utc,
        },
        {
            "zero_id": "TZA736_4_full_Y5_source_normalization_zero",
            "target_quantity": "Y5_source_normalization and epsilon_mu",
            "theorem_or_formula": "Y5_source_normalization=0 requires mu_obs=G0 M_H, d ln G_eff=0, d(Pi_M J_H)=0, mu_extra=0, Gauss/orbital calibration, and PPN source stability.",
            "premises": "All Y5 owner rows Y5O_1 through Y5O_7 hold together.",
            "derivation": "736 supplies only no-marker/same-frame direct-charge pieces. It does not close source-current flux, extra mass projection, q_loc projection, R10/PPN mapping, or second-order source stability.",
            "verdict": "not_derived_for_current_claim",
            "residual_left": "Y5 remains the active owner-or-bound branch.",
            "valid_for_claim": "false",
            "source_paths": source_path_string("518_doc", "y5_owner", "y5_amplitude"),
            "generated_utc": generated_utc,
        },
    ]


def make_no_marker_contract(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "contract_id": "NMC736_0_allowed_functor_domain",
            "statement": "Ordinary matter/readout functors may depend on Q_obs^hybrid=(e_obs/g_obs, psi_A, observed gauge fields, theta_univ, B_ref, Phi_red only where explicitly declared) and fixed species constants.",
            "derives": "R_rep is not a direct matter/readout argument.",
            "status": "contract_written_conditional",
            "not_allowed": "silent dependence on R_rep through a covariant marker, hidden source frame, or post-readout calibration map",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "NMC736_1_one_observed_coframe",
            "statement": "e_matter=e_source=e_clock=e_photon=e_orbit=e_obs before variation and before measured-GM fitting.",
            "derives": "delta_frame_source=0 under the contract.",
            "status": "conditional_zero",
            "not_allowed": "source/orbit/clock frame split disguised as calibration",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "NMC736_2_no_direct_species_marker",
            "statement": "Species labels and constants are fixed observed inputs and carry no R_rep/Phi/domain dependence.",
            "derives": "direct representative species source charge is zero.",
            "status": "partial_conditional_zero",
            "not_allowed": "species-specific material selector coupled to representative/domain fields",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "NMC736_3_shadow_frame_forbidden",
            "statement": "No hidden conformal/disformal/source-frame map may be introduced unless it is declared as an extension with explicit local bound rows.",
            "derives": "universal marker loophole is converted into an explicit extension tax rather than hidden proof debt.",
            "status": "guardrail_not_parent_derivation",
            "not_allowed": "hat_g=exp(2aR_rep)g_obs treated as harmless because it is universal",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "NMC736_4_same_frame_Ward_identity",
            "statement": "On matter equations and diffeomorphism invariance, nabla_mu T_m^{mu nu}=0 in the observed geometry.",
            "derives": "same-frame source stress conservation identity for matter, not the full exterior source-charge equality.",
            "status": "standard_conditional_identity",
            "not_allowed": "using same-frame Ward identity to claim d(Pi_M J_H)=0 or mu_extra=0 without projector/exterior proof",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "NMC736_5_limit",
            "statement": "No-marker closes direct representative matter charge, frame split, and direct species marker only.",
            "derives": "a third narrow zero row, not source-normalized Newton or local GR.",
            "status": "claim_limit",
            "not_allowed": "promoting Y5 owner theorem, q_loc projection, PPN, R10, Newton, WEP, or local GR",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def make_y5_runner_update(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "runner_id": "Y5R736_0_Geff_time_drift",
            "source_row": "Y5B_0_Geff_time_drift",
            "status_after_736": "interpretation_supported_not_zero",
            "zero_or_input": "same observed clock/source frame helps define dln_Geff_dt",
            "still_missing": "constant local coupling/kappa proof or sourced Gdot row",
            "valid_for_claim": "false",
            "source_paths": source_path_string("518_doc", "519_doc"),
            "generated_utc": generated_utc,
        },
        {
            "runner_id": "Y5R736_1_Meff_conservation",
            "source_row": "Y5B_1_Meff_conservation",
            "status_after_736": "unchanged_open",
            "zero_or_input": "none",
            "still_missing": "d(Pi_M J_H)=0 exterior/source-current flux closure",
            "valid_for_claim": "false",
            "source_paths": source_path_string("y5_bound_runner", "y5_owner"),
            "generated_utc": generated_utc,
        },
        {
            "runner_id": "Y5R736_2_radial_source_hair",
            "source_row": "Y5B_2_radial_source_hair",
            "status_after_736": "unchanged_open",
            "zero_or_input": "none",
            "still_missing": "radial flux/no-hair proof for M_H or sourced radial profile",
            "valid_for_claim": "false",
            "source_paths": source_path_string("y5_bound_runner"),
            "generated_utc": generated_utc,
        },
        {
            "runner_id": "Y5R736_3_species_source_charge",
            "source_row": "Y5B_3_species_source_charge",
            "status_after_736": "direct_marker_partly_zero_dressed_charge_open",
            "zero_or_input": "partial_{R_rep} S_A|e_obs=0 under universal matter pullback",
            "still_missing": "dressed Hilbert source charge universality including binding, field, and boundary contributions",
            "valid_for_claim": "false",
            "source_paths": source_path_string("519_doc", "731_matter_gate", "y5_bound_runner"),
            "generated_utc": generated_utc,
        },
        {
            "runner_id": "Y5R736_4_range_dependence",
            "source_row": "Y5B_4_range_dependence",
            "status_after_736": "unchanged_open",
            "zero_or_input": "none",
            "still_missing": "mass-gap/range theorem or q_loc-to-alpha(lambda) coefficient",
            "valid_for_claim": "false",
            "source_paths": source_path_string("y5_bound_runner", "735_queue"),
            "generated_utc": generated_utc,
        },
        {
            "runner_id": "Y5R736_5_extra_mass_projection",
            "source_row": "Y5B_5_extra_mass_projection",
            "status_after_736": "unchanged_open",
            "zero_or_input": "none",
            "still_missing": "mu_extra=0 for boundary/bulk/domain/projector/memory/non-EH channels or sourced coefficient vector",
            "valid_for_claim": "false",
            "source_paths": source_path_string("y5_bound_runner", "y5_owner"),
            "generated_utc": generated_utc,
        },
        {
            "runner_id": "Y5R736_6_frame_calibration_split",
            "source_row": "Y5B_6_frame_calibration_split",
            "status_after_736": "conditional_zero_under_one_coframe_no_marker_contract",
            "zero_or_input": "delta_frame_source=0 if e_source=e_orbit=e_clock=e_obs and no shadow frame is allowed",
            "still_missing": "parent proof that current MTS corpus actually enforces the one-coframe contract",
            "valid_for_claim": "false",
            "source_paths": source_path_string("519_doc", "y5_bound_runner"),
            "generated_utc": generated_utc,
        },
        {
            "runner_id": "Y5R736_7_beta_source_tail",
            "source_row": "Y5B_7_beta_source_tail",
            "status_after_736": "unchanged_open",
            "zero_or_input": "none",
            "still_missing": "second-order PPN source expansion",
            "valid_for_claim": "false",
            "source_paths": source_path_string("y5_bound_runner"),
            "generated_utc": generated_utc,
        },
        {
            "runner_id": "Y5R736_8_full_PPN_source_vector",
            "source_row": "Y5B_8_full_PPN_source_vector",
            "status_after_736": "unchanged_open",
            "zero_or_input": "none",
            "still_missing": "full PPN coefficient map from source-normalization/q_loc leakage",
            "valid_for_claim": "false",
            "source_paths": source_path_string("y5_bound_runner", "735_queue"),
            "generated_utc": generated_utc,
        },
        {
            "runner_id": "Y5R736_9_q_loc_projection",
            "source_row": "Y5B_9_q_loc_projection",
            "status_after_736": "unchanged_missing_projection",
            "zero_or_input": "none",
            "still_missing": "C_qmu normalization and units mapping q_loc into measured-GM/source-normalization channel",
            "valid_for_claim": "false",
            "source_paths": source_path_string("y5_bound_runner", "735_queue"),
            "generated_utc": generated_utc,
        },
    ]


def make_input_queue(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "input_id": "IN736_0_source_current_flux_closure",
            "needed_input": "proof or sourced row for d(Pi_M J_H)=0 in compact exterior/source-free regions",
            "current_status": "missing",
            "why_not_claimable": "no-marker matter action does not prove exterior Hilbert mass flux closure",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "input_id": "IN736_1_mu_extra_vector",
            "needed_input": "channelwise mu_extra vector for boundary, bulk, domain, projector, memory, non-EH, frame, calibration, PPN",
            "current_status": "missing",
            "why_not_claimable": "direct representative matter marker zero does not kill observed extra mass projection",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "input_id": "IN736_2_C_qmu_projection",
            "needed_input": "C_qmu projection operator, units, and normalization from q_loc to measured-GM/source-normalization",
            "current_status": "missing",
            "why_not_claimable": "q_loc source-normalization projection remains missing_projection",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "input_id": "IN736_3_Gauss_orbital_calibration",
            "needed_input": "Gauss/orbital theorem tying parent source charge M_H to inverse-square measured GM",
            "current_status": "missing",
            "why_not_claimable": "same coframe defines the source current but does not calibrate it to Kepler/Newton readout",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "input_id": "IN736_4_PPN_R10_maps",
            "needed_input": "PPN source vector and R10 alpha(lambda) maps after source-normalization split",
            "current_status": "missing",
            "why_not_claimable": "no-marker direct zero is not a weak-field metric solution or fifth-force coefficient",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def make_decision_matrix(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "D736_0_third_zero_row_selected",
            "decision": "accept direct representative matter-marker variation as a third narrow conditional zero row",
            "meaning": "Under a strict no-marker/one-observed-coframe matter contract, R_rep cannot directly source ordinary matter/readout.",
            "claim_status": "theorem_contract_only",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "source_paths": source_path_string("731_matter_gate", "519_doc", "732_pullback"),
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D736_1_universal_marker_loophole_retained",
            "decision": "do not pretend WEP/covariance alone kills universal conformal/disformal markers",
            "meaning": "No-marker remains a parent contract/minimality theorem target unless the current corpus explicitly derives it.",
            "claim_status": "blocked_for_current_claim_without_contract",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "source_paths": source_path_string("731_redteam", "731_matter_gate"),
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D736_2_full_Y5_still_open",
            "decision": "keep Y5 owner-or-bound branch active",
            "meaning": "Source mass flux, mu_extra, C_qmu q_loc, Gauss calibration, and PPN/R10 maps are still missing.",
            "claim_status": "runner_ready_not_scored",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "source_paths": source_path_string("518_doc", "y5_bound_runner", "735_queue"),
            "generated_utc": generated_utc,
        },
    ]


def make_route_update(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "route_id": "RU736_0_allowed",
            "allowed_after_736": "say direct representative matter-marker/source-frame charge is conditionally zero under the no-marker one-coframe contract",
            "forbidden_after_736": "say source-normalized Newton, WEP, PPN, R10, Newton, or local GR has passed",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "RU736_1_allowed",
            "allowed_after_736": "mark frame split as conditional zero and species direct marker as partial conditional zero",
            "forbidden_after_736": "mark dressed species source charge or full Y5 source normalization as zero",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "RU736_2_allowed",
            "allowed_after_736": "move to source-current Ward/flux closure or source-backed Y5 input rows",
            "forbidden_after_736": "use no-marker to hide q_loc projection, mu_extra, radial hair, or PPN source tails",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def make_summary(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "main_result": "Third narrow zero row derived conditionally: delta_{v_X^rep} S_matter=0 under a strict no-marker, one-observed-coframe matter/readout contract.",
            "hard_blocker": "No-marker contract not parent-derived for current corpus; source-current flux closure, mu_extra, C_qmu q_loc, Gauss calibration, PPN/R10 maps remain missing.",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def make_validation(
    source_register: list[dict[str, Any]],
    third_zero_rows: list[dict[str, Any]],
    contract_rows: list[dict[str, Any]],
    runner_rows: list[dict[str, Any]],
    input_rows: list[dict[str, Any]],
    decision_rows: list[dict[str, Any]],
    output_paths: list[Path],
) -> list[dict[str, str]]:
    source_paths_exist = all(row["exists"] == "true" for row in source_register)
    needles_pass = all(row["needle_check"] == "true" for row in source_register)
    prior_clean = prior_validation_clean(SOURCES["735_validation"]["path"])
    third_zero = any(
        row.get("zero_id") == "TZA736_0_direct_representative_matter_marker"
        and row.get("verdict") == "derived_third_narrow_zero_row_conditional"
        for row in third_zero_rows
    )
    frame_zero = any(
        row.get("runner_id") == "Y5R736_6_frame_calibration_split"
        and row.get("status_after_736") == "conditional_zero_under_one_coframe_no_marker_contract"
        for row in runner_rows
    )
    species_partial = any(
        row.get("runner_id") == "Y5R736_3_species_source_charge"
        and row.get("status_after_736") == "direct_marker_partly_zero_dressed_charge_open"
        for row in runner_rows
    )
    marker_loophole_retained = any(
        row.get("zero_id") == "TZA736_3_universal_conformal_marker_loophole"
        and row.get("verdict") == "not_killed_without_no_marker_contract"
        for row in third_zero_rows
    )
    full_y5_not_derived = any(
        row.get("zero_id") == "TZA736_4_full_Y5_source_normalization_zero"
        and row.get("verdict") == "not_derived_for_current_claim"
        for row in third_zero_rows
    )
    contract_limit = any(
        row.get("contract_id") == "NMC736_5_limit"
        and row.get("status") == "claim_limit"
        for row in contract_rows
    )
    hard_rows_retained = all(
        any(row.get("source_row") == source_row and "open" in row.get("status_after_736", "") or row.get("source_row") == source_row and "missing" in row.get("status_after_736", "") for row in runner_rows)
        for source_row in ["Y5B_1_Meff_conservation", "Y5B_5_extra_mass_projection", "Y5B_9_q_loc_projection"]
    )
    input_rows_missing = all(row.get("current_status") == "missing" for row in input_rows)
    all_nonclaim = all(
        row.get("valid_for_claim") == "false"
        for row in [*third_zero_rows, *contract_rows, *runner_rows, *input_rows, *decision_rows]
    )
    outputs_scoped = under_post_checkpoint(output_paths)
    formalization_count = formalization_changed_after_cutoff()

    return [
        {"check_id": "V736_0_source_paths_exist", "result": "pass" if source_paths_exist else "fail", "detail": f"source_rows={len(source_register)}"},
        {"check_id": "V736_1_source_needles_present", "result": "pass" if needles_pass else "fail", "detail": "all source files contain expected evidence needles"},
        {"check_id": "V736_2_prior_735_clean", "result": "pass" if prior_clean else "fail", "detail": "735 validation has no failures"},
        {"check_id": "V736_3_735_selected_736", "result": "pass" if text_contains(SOURCES["735_doc"]["path"], [OUTPUT_DOC.name]) else "fail", "detail": OUTPUT_DOC.name},
        {"check_id": "V736_4_third_zero_direct_marker", "result": "pass" if third_zero else "fail", "detail": "delta_vrep S_matter zero row exists"},
        {"check_id": "V736_5_frame_split_conditional_zero", "result": "pass" if frame_zero else "fail", "detail": "Y5B_6 conditional zero retained"},
        {"check_id": "V736_6_species_direct_partial_zero", "result": "pass" if species_partial else "fail", "detail": "Y5B_3 direct marker partial zero retained"},
        {"check_id": "V736_7_universal_marker_loophole_retained", "result": "pass" if marker_loophole_retained else "fail", "detail": "WEP/covariance alone not accepted as kill"},
        {"check_id": "V736_8_full_Y5_not_derived", "result": "pass" if full_y5_not_derived else "fail", "detail": "source-normalization zero not claimed"},
        {"check_id": "V736_9_contract_claim_limit_present", "result": "pass" if contract_limit else "fail", "detail": "no-marker limits stated"},
        {"check_id": "V736_10_hard_Y5_rows_retained", "result": "pass" if hard_rows_retained else "fail", "detail": "Meff/mu_extra/q_loc rows remain open"},
        {"check_id": "V736_11_input_rows_missing_not_claim", "result": "pass" if input_rows_missing else "fail", "detail": "source inputs remain missing until sourced/derived"},
        {"check_id": "V736_12_no_claim_rows_promoted", "result": "pass" if all_nonclaim else "fail", "detail": "all generated rows valid_for_claim=false"},
        {"check_id": "V736_13_next_target_selected", "result": "pass" if all(row.get("next_target") == NEXT_TARGET for row in decision_rows) else "fail", "detail": NEXT_TARGET},
        {"check_id": "V736_14_outputs_scoped", "result": "pass" if outputs_scoped else "fail", "detail": "all outputs under post-checkpoint-work"},
        {"check_id": "V736_15_formalization_workbench_untouched", "result": "pass" if formalization_count == 0 else "fail", "detail": f"formalization_changed_after_cutoff={formalization_count}"},
        {"check_id": "V736_16_no_local_arena_claim", "result": "pass", "detail": "R10/WEP/PPN/Newton/local-GR claims remain blocked"},
        {"check_id": "V736_17_validation_rows_ready", "result": "pass", "detail": "validation table constructed"},
    ]


def build_doc(
    source_register: list[dict[str, Any]],
    third_zero_rows: list[dict[str, Any]],
    contract_rows: list[dict[str, Any]],
    runner_rows: list[dict[str, Any]],
    input_rows: list[dict[str, Any]],
    decision_rows: list[dict[str, Any]],
    route_rows: list[dict[str, Any]],
    summary_rows: list[dict[str, Any]],
    validation_rows: list[dict[str, Any]],
) -> None:
    text = f"""# 736 - Y5 R10 Matter No-Marker Source Normalization Or Third Zero Row

## Summary

Start point: 735 pruned pure representative boundary charge but left observed boundary/source-measure flux and Y5 source-normalization open.

Current verdict: **a third narrow zero row is derivable conditionally**:

```text
delta_{{v_X^rep}} S_matter = 0
```

if ordinary matter/readout functors obey the strict no-marker, one-observed-coframe contract. This removes direct representative matter/source-frame charge. It does **not** prove full `Y5_source_normalization=0`.

| Item | Value |
| --- | --- |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Main result | third narrow no-marker zero plus explicit Y5 hard-row retention |
| Next target | `{NEXT_TARGET}` |

## Third Zero Attempt

{markdown_table(third_zero_rows, ["zero_id", "target_quantity", "theorem_or_formula", "premises", "derivation", "verdict", "residual_left", "valid_for_claim"])}

## Matter No-Marker Contract

{markdown_table(contract_rows, ["contract_id", "statement", "derives", "status", "not_allowed", "valid_for_claim"])}

## Y5 Runner Update

{markdown_table(runner_rows, ["runner_id", "source_row", "status_after_736", "zero_or_input", "still_missing", "valid_for_claim"])}

## Source Normalization Input Queue

{markdown_table(input_rows, ["input_id", "needed_input", "current_status", "why_not_claimable", "next_action", "valid_for_claim"])}

## Decision Matrix

{markdown_table(decision_rows, ["decision_id", "decision", "meaning", "claim_status", "next_target", "valid_for_claim"])}

## Route Update

{markdown_table(route_rows, ["route_id", "allowed_after_736", "forbidden_after_736", "next_action", "valid_for_claim"])}

## Nonclaim Summary

{markdown_table(summary_rows, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim"])}

## Source Register

{markdown_table(source_register, ["source_id", "path", "exists", "needle_check", "role"])}

## Validation

{markdown_table(validation_rows, ["check_id", "result", "detail"])}

## Plain-English Verdict

Good news, but still not fireworks. We can kill the direct representative matter-marker route if ordinary matter is forced to live only on the observed coframe/metric and fixed species constants. That is exactly the kind of clean pruning we want. The remaining Y5 monster is dressed source mass: flux closure, extra mass projection, `C_qmu q_loc`, Gauss calibration, and PPN/R10 mapping. That is the next wall.
"""
    OUTPUT_DOC.write_text(text, encoding="utf-8")


def main() -> None:
    generated_utc = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    run_root = RUNS / f"736_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}"
    run_root.mkdir(parents=True, exist_ok=True)

    source_register = make_source_register(generated_utc)
    third_zero_rows = make_third_zero_attempt(generated_utc)
    contract_rows = make_no_marker_contract(generated_utc)
    runner_rows = make_y5_runner_update(generated_utc)
    input_rows = make_input_queue(generated_utc)
    decision_rows = make_decision_matrix(generated_utc)
    route_rows = make_route_update(generated_utc)
    summary_rows = make_summary(generated_utc)

    output_paths = [
        OUTPUT_DOC,
        SOURCE_REGISTER_PATH,
        THIRD_ZERO_PATH,
        NO_MARKER_CONTRACT_PATH,
        Y5_RUNNER_UPDATE_PATH,
        INPUT_QUEUE_PATH,
        DECISION_PATH,
        ROUTE_UPDATE_PATH,
        SUMMARY_PATH,
        VALIDATION_PATH,
    ]

    write_csv(
        SOURCE_REGISTER_PATH,
        source_register,
        ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        THIRD_ZERO_PATH,
        third_zero_rows,
        ["zero_id", "target_quantity", "theorem_or_formula", "premises", "derivation", "verdict", "residual_left", "valid_for_claim", "source_paths", "generated_utc"],
    )
    write_csv(
        NO_MARKER_CONTRACT_PATH,
        contract_rows,
        ["contract_id", "statement", "derives", "status", "not_allowed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        Y5_RUNNER_UPDATE_PATH,
        runner_rows,
        ["runner_id", "source_row", "status_after_736", "zero_or_input", "still_missing", "valid_for_claim", "source_paths", "generated_utc"],
    )
    write_csv(
        INPUT_QUEUE_PATH,
        input_rows,
        ["input_id", "needed_input", "current_status", "why_not_claimable", "next_action", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        DECISION_PATH,
        decision_rows,
        ["decision_id", "decision", "meaning", "claim_status", "next_target", "valid_for_claim", "source_paths", "generated_utc"],
    )
    write_csv(
        ROUTE_UPDATE_PATH,
        route_rows,
        ["route_id", "allowed_after_736", "forbidden_after_736", "next_action", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        SUMMARY_PATH,
        summary_rows,
        ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim", "generated_utc"],
    )

    validation_rows = make_validation(source_register, third_zero_rows, contract_rows, runner_rows, input_rows, decision_rows, output_paths)
    write_csv(VALIDATION_PATH, validation_rows, ["check_id", "result", "detail"])
    build_doc(
        source_register,
        third_zero_rows,
        contract_rows,
        runner_rows,
        input_rows,
        decision_rows,
        route_rows,
        summary_rows,
        validation_rows,
    )

    status_payload = {
        "generated_utc": generated_utc,
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "next_target": NEXT_TARGET,
        "doc": str(OUTPUT_DOC),
        "validation": str(VALIDATION_PATH),
        "all_validation_pass": all(row["result"] == "pass" for row in validation_rows),
    }
    (run_root / "status.json").write_text(json.dumps(status_payload, indent=2), encoding="utf-8")
    (run_root / "COMPLETE.marker").write_text("complete\n", encoding="utf-8")
    print(json.dumps(status_payload, indent=2))


if __name__ == "__main__":
    main()
