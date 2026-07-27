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
OUTPUT_DOC = POST_CHECKPOINT / "737-Y5-R10-source-current-Ward-flux-closure-or-source-backed-Y5-inputs.md"
NEXT_TARGET = "738-Y5-R10-PiM-projector-owner-or-radial-bound-runner.md"
CUTOFF = datetime(2026, 5, 31, 14, 42, 0)

STATUS = "Y5_R10_737_Ward_current_bridge_written_projected_Meff_flux_not_closed_Y5_inputs_queued"
CLAIM_CEILING = "same_frame_Ward_current_conservation_only_projected_source_flux_unclosed_no_R10_WEP_PPN_Newton_or_local_GR_pass"

SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_737_SOURCE_REGISTER.csv"
WARD_ATTEMPT_PATH = RESIDUALS / "P8_Y5_R10_737_SOURCE_CURRENT_WARD_FLUX_ATTEMPT.csv"
OBSTRUCTION_PATH = RESIDUALS / "P8_Y5_R10_737_PROJECTED_MASS_FLUX_OBSTRUCTION.csv"
Y5_RUNNER_UPDATE_PATH = RESIDUALS / "P8_Y5_R10_737_Y5_RUNNER_UPDATE.csv"
INPUT_QUEUE_PATH = RESIDUALS / "P8_Y5_R10_737_SOURCE_BACKED_INPUT_QUEUE.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_R10_737_DECISION_MATRIX.csv"
ROUTE_UPDATE_PATH = RESIDUALS / "P8_Y5_R10_737_ROUTE_UPDATE.csv"
SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_737_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_737_VALIDATION.csv"

SOURCES: dict[str, dict[str, Any]] = {
    "736_doc": {
        "path": POST_CHECKPOINT / "736-Y5-R10-matter-no-marker-source-normalization-or-third-zero-row.md",
        "role": "immediate no-marker and Y5 hard-row handoff",
        "needles": ["third narrow zero row is derivable", OUTPUT_DOC.name, "source-current Ward/flux closure"],
    },
    "736_validation": {
        "path": RESIDUALS / "P8_Y5_BRR545_736_VALIDATION.csv",
        "role": "prior validation gate",
        "needles": ["V736_13_next_target_selected", OUTPUT_DOC.name, "V736_15_formalization_workbench_untouched"],
    },
    "736_runner": {
        "path": RESIDUALS / "P8_Y5_R10_736_Y5_RUNNER_UPDATE.csv",
        "role": "Y5 rows after no-marker pass",
        "needles": ["Y5R736_1_Meff_conservation", "d(Pi_M J_H)=0 exterior/source-current flux closure", "Y5R736_9_q_loc_projection"],
    },
    "736_queue": {
        "path": RESIDUALS / "P8_Y5_R10_736_SOURCE_NORMALIZATION_INPUT_QUEUE.csv",
        "role": "missing flux/projector/q_loc inputs",
        "needles": ["IN736_0_source_current_flux_closure", "IN736_2_C_qmu_projection", "missing"],
    },
    "520_doc": {
        "path": POST_CHECKPOINT / "520-Y5-source-current-Ward-closure-or-bound-row.md",
        "role": "older Ward bridge and obstruction source",
        "needles": ["Ward conservation alone does not prove", "d(Pi_M J_H)=0", "projector commutator"],
    },
    "519_doc": {
        "path": POST_CHECKPOINT / "519-fill-Y5-bound-runner-or-source-owner-clause.md",
        "role": "same-coframe source current clause",
        "needles": ["J_H[tau]", "diffeomorphism_Ward_identity", "same coframe does not falsely solve"],
    },
    "518_doc": {
        "path": POST_CHECKPOINT / "518-Y5-source-normalization-owner-or-q_loc-bound-implementation.md",
        "role": "Y5 owner theorem and residual runner",
        "needles": ["Y5_SOURCE_NORMALIZATION", "hard_fail_current", "Y5B_9_q_loc_projection"],
    },
    "y5_owner": {
        "path": RESIDUALS / "P8_Y5_SOURCE_NORMALIZATION_OWNER_THEOREM.csv",
        "role": "Y5 owner rows",
        "needles": ["Y5O_3_parent_source_charge", "Y5O_4_flux_closure", "Y5O_8_owner_theorem"],
    },
    "y5_bound_runner": {
        "path": RESIDUALS / "P8_Y5_SOURCE_NORMALIZATION_BOUND_RUNNER_INPUT.csv",
        "role": "Y5 bound runner rows",
        "needles": ["Y5B_1_Meff_conservation", "Y5B_2_radial_source_hair", "Y5B_9_q_loc_projection"],
    },
    "worldtube_runner": {
        "path": RESIDUALS / "P8_WORLDTUBE_MEFF_RESIDUAL_RUNNER.csv",
        "role": "worldtube M_eff residual runner",
        "needles": ["MR510_0_flux_leak", "d(Pi_M J_H)=0", "MR510_3_projector_hair"],
    },
    "source_measure_map": {
        "path": RESIDUALS / "P8_SOURCE_MEASURE_MEFF_FLUX_RESIDUAL_MAP.csv",
        "role": "source-measure flux residual map",
        "needles": ["SMR509_0_Delta_flux", "SMR509_1_Delta_PiM", "SMR509_7_Delta_PPN"],
    },
    "newton_stack": {
        "path": RESIDUALS / "P8_source_normalized_Newton_branch_STACK.csv",
        "role": "source-normalized Newton stack",
        "needles": ["SN4_closed_Meff_flux", "SN6_zero_mu_extra_and_source_residuals", "SN11_second_order_PPN_source_stability"],
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


def make_ward_attempt(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "ward_id": "WFA737_0_same_frame_matter_Ward",
            "target_quantity": "nabla_mu T_m^{mu nu}",
            "theorem_or_formula": "For a diffeomorphism-invariant same-frame matter action, E_psi=0 implies nabla_mu T_m^{mu nu}=0 in the observed geometry.",
            "premises": "Same observed coframe/no-marker contract, matter equations, no post-readout frame split.",
            "derivation": "Vary S_m under an infinitesimal diffeomorphism, integrate by parts, and use arbitrariness of xi^nu to obtain the Hilbert stress Ward identity.",
            "verdict": "standard_conditional_Ward_identity",
            "residual_left": "Stress conservation is not yet a closed projected source-mass flux.",
            "valid_for_claim": "false",
            "source_paths": source_path_string("519_doc", "520_doc", "736_doc"),
            "generated_utc": generated_utc,
        },
        {
            "ward_id": "WFA737_1_Killing_source_current",
            "target_quantity": "nabla_mu(T_m^{mu nu} tau_nu)",
            "theorem_or_formula": "If tau is an observed Killing or stationary Hamiltonian generator, nabla_mu(T_m^{mu nu} tau_nu)=0.",
            "premises": "WFA737_0 plus nabla_(mu tau_nu)=0 or controlled stationary source frame.",
            "derivation": "nabla_mu(T_m^{mu nu} tau_nu)=tau_nu nabla_mu T_m^{mu nu}+T_m^{mu nu} nabla_mu tau_nu; the first term vanishes by Ward and the second by Killing symmetry.",
            "verdict": "derived_narrow_conditional_current_zero",
            "residual_left": "This is an unprojected/same-frame matter current zero; it does not define Pi_M or include gravitational/binding/boundary dressing.",
            "valid_for_claim": "false",
            "source_paths": source_path_string("520_doc", "y5_owner"),
            "generated_utc": generated_utc,
        },
        {
            "ward_id": "WFA737_2_projected_mass_flux_target",
            "target_quantity": "d(Pi_M J_H)",
            "theorem_or_formula": "d(Pi_M J_H)=Pi_M dJ_H + [d,Pi_M]J_H + Pi_M J_exchange + A_parent.",
            "premises": "Parent-owned mass projector Pi_M, zero commutator, no exchange projection, no boundary/anomaly flux.",
            "derivation": "Apply the product rule to the projected mass current. Ward conservation can kill dJ_H only after a mass generator/current is selected; the remaining terms are independent closure gates.",
            "verdict": "not_derived_for_current_claim",
            "residual_left": "Y5B_1 and Y5B_2 remain open until Pi_M, exchange, and boundary/anomaly terms close.",
            "valid_for_claim": "false",
            "source_paths": source_path_string("520_doc", "worldtube_runner", "source_measure_map"),
            "generated_utc": generated_utc,
        },
        {
            "ward_id": "WFA737_3_radial_shell_Stokes_limit",
            "target_quantity": "M_H(S2)-M_H(S1)",
            "theorem_or_formula": "If d(Pi_M J_H)=0 on the compact exterior annulus A, then M_H(S2)-M_H(S1)=int_A d(Pi_M J_H)=0.",
            "premises": "WFA737_2 closes, surfaces S1/S2 bound a source-free exterior annulus, and no hidden boundary/source-measure leakage is present.",
            "derivation": "Use Stokes' theorem on the projected mass current.",
            "verdict": "conditional_Stokes_zero_not_current_MTS",
            "residual_left": "The Stokes step is fine; the missing object is the closed projected current.",
            "valid_for_claim": "false",
            "source_paths": source_path_string("520_doc", "worldtube_runner", "newton_stack"),
            "generated_utc": generated_utc,
        },
        {
            "ward_id": "WFA737_4_full_source_normalized_Newton",
            "target_quantity": "mu_obs=G0 M_H and Y5_source_normalization=0",
            "theorem_or_formula": "Needs closed M_H, zero mu_extra, one constant G0, Gauss/orbital calibration, and PPN source stability.",
            "premises": "All source-normalized Newton stack rows SN0-SN11 are derived or bounded.",
            "derivation": "737 only supplies the Ward bridge and projected-flux obstruction. It does not close Pi_M, mu_extra, C_qmu, Gauss readout, R10, or PPN maps.",
            "verdict": "not_derived_for_current_claim",
            "residual_left": "Source-normalized Newton/local GR remains blocked.",
            "valid_for_claim": "false",
            "source_paths": source_path_string("518_doc", "newton_stack", "y5_bound_runner"),
            "generated_utc": generated_utc,
        },
    ]


def make_obstruction_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "obstruction_id": "PMF737_0_no_observed_tau",
            "problem": "Ward conservation does not select an energy/mass current without an observed stationary generator tau.",
            "formula": "nabla_mu(T^{mu nu} tau_nu)=T^{mu nu} nabla_(mu tau_nu) if tau is not Killing/stationary.",
            "required_kill": "observed local time/Hamiltonian generator normalized in Q_obs^hybrid",
            "status": "open_for_current_claim",
            "mapped_rows": "Y5B_1;SN2;SN4",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "obstruction_id": "PMF737_1_PiM_parent_ownership",
            "problem": "Pi_M may be a readout/post-fit projector rather than a parent charge map.",
            "formula": "J_M=Pi_M J_H is not a source current until Pi_M is parent-owned before orbital calibration.",
            "required_kill": "derive Pi_M from Hamiltonian/Hilbert/Noether source charge",
            "status": "open_next_target",
            "mapped_rows": "Y5B_1;Y5B_2;SMR509_1",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "obstruction_id": "PMF737_2_projector_commutator",
            "problem": "A field/domain-dependent Pi_M creates radial/time leakage by product rule.",
            "formula": "[d,Pi_M]J_H != 0",
            "required_kill": "Pi_M covariantly constant/topological or metric-response cancellation",
            "status": "open_next_target",
            "mapped_rows": "Y5B_1;Y5B_2;MR510_3",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "obstruction_id": "PMF737_3_extra_exchange_projection",
            "problem": "Boundary, domain, memory, non-EH, coupling, and q_loc sectors can carry mass-channel projection.",
            "formula": "Pi_M J_exchange + A_parent + C_qmu q_loc can enter d(Pi_M J_H).",
            "required_kill": "mu_extra vector zero theorem or source-backed coefficient vector",
            "status": "open",
            "mapped_rows": "Y5B_5;Y5B_9;SMR509_3;SMR509_7",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "obstruction_id": "PMF737_4_boundary_improvement_flux",
            "problem": "A total divergence can still carry finite compact-boundary mass flux.",
            "formula": "int_boundary Pi_M K_owner may shift M_eff unless reference/topological cancellation is proved.",
            "required_kill": "boundary/reference no-flux theorem or explicit alpha3/xi/Gdot coefficient bounds",
            "status": "open",
            "mapped_rows": "Y5B_2;Y5B_5;SMR509_2",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "obstruction_id": "PMF737_5_calibration_not_closure",
            "problem": "A closed source charge is not yet the measured inverse-square orbital GM.",
            "formula": "dJ_M=0 does not imply a_r=-G0 M_H/r^2 without Gauss/orbital calibration.",
            "required_kill": "Gauss surface integral and slow-orbit readout theorem",
            "status": "open",
            "mapped_rows": "Y5B_7;Y5B_8;SN8;SN9",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def make_y5_runner_update(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "runner_id": "Y5R737_0_Geff_time_drift",
            "source_row": "Y5B_0_Geff_time_drift",
            "status_after_737": "unchanged_requires_constant_coupling_or_Gdot_row",
            "zero_or_input": "Ward bridge does not set dln_Geff_dt=0",
            "still_missing": "constant local G_eff/kappa proof or sourced Gdot/G row",
            "valid_for_claim": "false",
            "source_paths": source_path_string("736_runner", "y5_bound_runner"),
            "generated_utc": generated_utc,
        },
        {
            "runner_id": "Y5R737_1_Meff_conservation",
            "source_row": "Y5B_1_Meff_conservation",
            "status_after_737": "Ward_bridge_written_projected_flux_not_closed",
            "zero_or_input": "nabla_mu(T_m^{mu nu}tau_nu)=0 if tau is observed Killing/stationary; d(Pi_M J_H)=0 only if Pi_M/exchange/boundary gates close",
            "still_missing": "observed tau, parent-owned Pi_M, [d,Pi_M]=0, zero exchange, zero boundary/anomaly",
            "valid_for_claim": "false",
            "source_paths": source_path_string("520_doc", "worldtube_runner", "736_runner"),
            "generated_utc": generated_utc,
        },
        {
            "runner_id": "Y5R737_2_radial_source_hair",
            "source_row": "Y5B_2_radial_source_hair",
            "status_after_737": "Stokes_formula_written_not_scored",
            "zero_or_input": "epsilon_radial_Meff = M_H^-1 int_A d(Pi_M J_H), zero only if projected flux closes",
            "still_missing": "closed Pi_M flux theorem or sourced radial shell profile",
            "valid_for_claim": "false",
            "source_paths": source_path_string("520_doc", "worldtube_runner"),
            "generated_utc": generated_utc,
        },
        {
            "runner_id": "Y5R737_3_species_source_charge",
            "source_row": "Y5B_3_species_source_charge",
            "status_after_737": "unchanged_direct_marker_partly_zero_dressed_open",
            "zero_or_input": "direct representative marker remained pruned from 736",
            "still_missing": "dressed source charge universality through binding/field/boundary terms",
            "valid_for_claim": "false",
            "source_paths": source_path_string("736_runner", "y5_bound_runner"),
            "generated_utc": generated_utc,
        },
        {
            "runner_id": "Y5R737_4_range_dependence",
            "source_row": "Y5B_4_range_dependence",
            "status_after_737": "unchanged_open",
            "zero_or_input": "none",
            "still_missing": "range theorem or alpha(lambda) coefficient after projected source split",
            "valid_for_claim": "false",
            "source_paths": source_path_string("736_runner", "y5_bound_runner"),
            "generated_utc": generated_utc,
        },
        {
            "runner_id": "Y5R737_5_extra_mass_projection",
            "source_row": "Y5B_5_extra_mass_projection",
            "status_after_737": "open_as_projected_exchange_vector",
            "zero_or_input": "Ward matter conservation does not kill mu_extra",
            "still_missing": "boundary/bulk/domain/projector/memory/non-EH/q_loc coefficient vector or zero theorem",
            "valid_for_claim": "false",
            "source_paths": source_path_string("520_doc", "source_measure_map", "y5_bound_runner"),
            "generated_utc": generated_utc,
        },
        {
            "runner_id": "Y5R737_6_frame_calibration_split",
            "source_row": "Y5B_6_frame_calibration_split",
            "status_after_737": "retained_conditional_zero_under_one_coframe_contract",
            "zero_or_input": "delta_frame_source=0 if one-coframe/no-shadow-frame contract is parent-derived",
            "still_missing": "parent proof current corpus enforces one-coframe contract",
            "valid_for_claim": "false",
            "source_paths": source_path_string("736_runner", "519_doc"),
            "generated_utc": generated_utc,
        },
        {
            "runner_id": "Y5R737_7_beta_source_tail",
            "source_row": "Y5B_7_beta_source_tail",
            "status_after_737": "unchanged_open",
            "zero_or_input": "none",
            "still_missing": "second-order PPN source expansion",
            "valid_for_claim": "false",
            "source_paths": source_path_string("newton_stack", "y5_bound_runner"),
            "generated_utc": generated_utc,
        },
        {
            "runner_id": "Y5R737_8_full_PPN_source_vector",
            "source_row": "Y5B_8_full_PPN_source_vector",
            "status_after_737": "unchanged_open",
            "zero_or_input": "none",
            "still_missing": "PPN coefficient map from projected source/q_loc leakage",
            "valid_for_claim": "false",
            "source_paths": source_path_string("newton_stack", "y5_bound_runner"),
            "generated_utc": generated_utc,
        },
        {
            "runner_id": "Y5R737_9_q_loc_projection",
            "source_row": "Y5B_9_q_loc_projection",
            "status_after_737": "unchanged_missing_C_qmu_projection",
            "zero_or_input": "none",
            "still_missing": "C_qmu normalization and units mapping q_loc into d(Pi_M J_H), epsilon_mu, or Delta_PPN_source",
            "valid_for_claim": "false",
            "source_paths": source_path_string("736_queue", "y5_bound_runner"),
            "generated_utc": generated_utc,
        },
    ]


def make_input_queue(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "input_id": "IN737_0_observed_tau",
            "needed_input": "observed stationary/Killing or Hamiltonian time generator tau normalized in Q_obs^hybrid",
            "current_status": "missing",
            "why_not_claimable": "Ward stress conservation alone does not select an energy/mass current",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "input_id": "IN737_1_PiM_parent_owner",
            "needed_input": "parent-owned Pi_M mass projector/charge map before orbital readout",
            "current_status": "missing",
            "why_not_claimable": "post-fit/readout Pi_M cannot prove source flux closure",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "input_id": "IN737_2_PiM_commutator",
            "needed_input": "proof that [d,Pi_M]J_H=0 or explicit commutator residual coefficient",
            "current_status": "missing",
            "why_not_claimable": "projector product-rule leakage can create radial/time mass hair",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "input_id": "IN737_3_mu_extra_exchange_vector",
            "needed_input": "channelwise exchange vector for mu_extra, including boundary, domain, memory, non-EH, q_loc, and anomaly terms",
            "current_status": "missing",
            "why_not_claimable": "matter Ward conservation does not zero non-Hilbert projected exchange",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "input_id": "IN737_4_radial_or_time_profile",
            "needed_input": "source-backed dln_Meff_dt or epsilon_radial_Meff profile if projected flux theorem fails",
            "current_status": "missing",
            "why_not_claimable": "Y5B_1/Y5B_2 remain unscored without theorem or data",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "input_id": "IN737_5_C_qmu_projection",
            "needed_input": "C_qmu projection from q_loc to source-normalization/PPN units",
            "current_status": "missing",
            "why_not_claimable": "compact-shell proxy is still dimensionless and not mapped into Y5/PPN rows",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def make_decision_matrix(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "D737_0_Ward_bridge_written",
            "decision": "accept same-frame matter Ward current conservation as a conditional bridge",
            "meaning": "The matter source current is now mathematically sharper, but still unprojected.",
            "claim_status": "bridge_only",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "source_paths": source_path_string("520_doc", "519_doc"),
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D737_1_projected_flux_not_closed",
            "decision": "do not claim d(Pi_M J_H)=0 for current MTS",
            "meaning": "Pi_M ownership, commutator, exchange, boundary/anomaly, and calibration remain open.",
            "claim_status": "blocked_for_current_claim",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "source_paths": source_path_string("520_doc", "worldtube_runner"),
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D737_2_next_target_PiM",
            "decision": "move next to Pi_M projector owner or radial bound runner",
            "meaning": "Pi_M is now the key pressure point for Y5B_1/Y5B_2.",
            "claim_status": "runner_ready_not_scored",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "source_paths": source_path_string("newton_stack", "source_measure_map"),
            "generated_utc": generated_utc,
        },
    ]


def make_route_update(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "route_id": "RU737_0_allowed",
            "allowed_after_737": "say same-frame matter Ward current conservation is conditionally available",
            "forbidden_after_737": "say projected source mass flux, measured GM, Newton, PPN, R10, WEP, or local GR has passed",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "RU737_1_allowed",
            "allowed_after_737": "use d(Pi_M J_H)=Pi_M dJ_H+[d,Pi_M]J_H+exchange+anomaly as the exact Y5 obstruction ledger",
            "forbidden_after_737": "hide Pi_M commutator or mu_extra exchange inside Ward conservation",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "RU737_2_allowed",
            "allowed_after_737": "attack Pi_M ownership next or fill radial/time residual inputs",
            "forbidden_after_737": "mark Y5B_1/Y5B_2 as zero without Pi_M/exchange/boundary closure",
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
            "main_result": "Same-frame matter Ward current bridge written; projected M_eff flux closure remains unproved.",
            "hard_blocker": "Observed tau, parent-owned Pi_M, [d,Pi_M]=0, mu_extra/exchange vector, boundary/anomaly flux, C_qmu projection, Gauss/PPN/R10 maps.",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def make_validation(
    source_register: list[dict[str, Any]],
    ward_rows: list[dict[str, Any]],
    obstruction_rows: list[dict[str, Any]],
    runner_rows: list[dict[str, Any]],
    input_rows: list[dict[str, Any]],
    decision_rows: list[dict[str, Any]],
    output_paths: list[Path],
) -> list[dict[str, str]]:
    source_paths_exist = all(row["exists"] == "true" for row in source_register)
    needles_pass = all(row["needle_check"] == "true" for row in source_register)
    prior_clean = prior_validation_clean(SOURCES["736_validation"]["path"])
    ward_bridge = any(
        row.get("ward_id") == "WFA737_0_same_frame_matter_Ward"
        and row.get("verdict") == "standard_conditional_Ward_identity"
        for row in ward_rows
    )
    killing_current = any(
        row.get("ward_id") == "WFA737_1_Killing_source_current"
        and row.get("verdict") == "derived_narrow_conditional_current_zero"
        for row in ward_rows
    )
    projected_not_closed = any(
        row.get("ward_id") == "WFA737_2_projected_mass_flux_target"
        and row.get("verdict") == "not_derived_for_current_claim"
        for row in ward_rows
    )
    full_newton_not_derived = any(
        row.get("ward_id") == "WFA737_4_full_source_normalized_Newton"
        and row.get("verdict") == "not_derived_for_current_claim"
        for row in ward_rows
    )
    obstruction_ids = {row.get("obstruction_id", "") for row in obstruction_rows}
    required_obstructions = {
        "PMF737_0_no_observed_tau",
        "PMF737_1_PiM_parent_ownership",
        "PMF737_2_projector_commutator",
        "PMF737_3_extra_exchange_projection",
        "PMF737_4_boundary_improvement_flux",
        "PMF737_5_calibration_not_closure",
    }
    runner_meff_open = any(
        row.get("runner_id") == "Y5R737_1_Meff_conservation"
        and row.get("status_after_737") == "Ward_bridge_written_projected_flux_not_closed"
        for row in runner_rows
    )
    runner_radial_open = any(
        row.get("runner_id") == "Y5R737_2_radial_source_hair"
        and row.get("status_after_737") == "Stokes_formula_written_not_scored"
        for row in runner_rows
    )
    qloc_missing = any(
        row.get("runner_id") == "Y5R737_9_q_loc_projection"
        and row.get("status_after_737") == "unchanged_missing_C_qmu_projection"
        for row in runner_rows
    )
    input_rows_missing = all(row.get("current_status") == "missing" for row in input_rows)
    all_nonclaim = all(
        row.get("valid_for_claim") == "false"
        for row in [*ward_rows, *obstruction_rows, *runner_rows, *input_rows, *decision_rows]
    )
    outputs_scoped = under_post_checkpoint(output_paths)
    formalization_count = formalization_changed_after_cutoff()

    return [
        {"check_id": "V737_0_source_paths_exist", "result": "pass" if source_paths_exist else "fail", "detail": f"source_rows={len(source_register)}"},
        {"check_id": "V737_1_source_needles_present", "result": "pass" if needles_pass else "fail", "detail": "all source files contain expected evidence needles"},
        {"check_id": "V737_2_prior_736_clean", "result": "pass" if prior_clean else "fail", "detail": "736 validation has no failures"},
        {"check_id": "V737_3_736_selected_737", "result": "pass" if text_contains(SOURCES["736_doc"]["path"], [OUTPUT_DOC.name]) else "fail", "detail": OUTPUT_DOC.name},
        {"check_id": "V737_4_Ward_bridge_written", "result": "pass" if ward_bridge else "fail", "detail": "same-frame matter Ward identity row exists"},
        {"check_id": "V737_5_Killing_current_conditional_zero", "result": "pass" if killing_current else "fail", "detail": "stationary/Killing current zero row exists"},
        {"check_id": "V737_6_projected_flux_not_closed", "result": "pass" if projected_not_closed else "fail", "detail": "d(Pi_M J_H)=0 not claimed"},
        {"check_id": "V737_7_full_Newton_not_derived", "result": "pass" if full_newton_not_derived else "fail", "detail": "source-normalized Newton/local GR not claimed"},
        {"check_id": "V737_8_obstruction_rows_complete", "result": "pass" if required_obstructions.issubset(obstruction_ids) else "fail", "detail": f"obstruction_rows={len(obstruction_ids)}"},
        {"check_id": "V737_9_Y5B1_Y5B2_retained", "result": "pass" if runner_meff_open and runner_radial_open else "fail", "detail": "Meff conservation and radial source hair remain unscored"},
        {"check_id": "V737_10_q_loc_projection_retained", "result": "pass" if qloc_missing else "fail", "detail": "C_qmu projection still missing"},
        {"check_id": "V737_11_input_rows_missing_not_claim", "result": "pass" if input_rows_missing else "fail", "detail": "source inputs remain missing until sourced/derived"},
        {"check_id": "V737_12_no_claim_rows_promoted", "result": "pass" if all_nonclaim else "fail", "detail": "all generated rows valid_for_claim=false"},
        {"check_id": "V737_13_next_target_selected", "result": "pass" if all(row.get("next_target") == NEXT_TARGET for row in decision_rows) else "fail", "detail": NEXT_TARGET},
        {"check_id": "V737_14_outputs_scoped", "result": "pass" if outputs_scoped else "fail", "detail": "all outputs under post-checkpoint-work"},
        {"check_id": "V737_15_formalization_workbench_untouched", "result": "pass" if formalization_count == 0 else "fail", "detail": f"formalization_changed_after_cutoff={formalization_count}"},
        {"check_id": "V737_16_no_local_arena_claim", "result": "pass", "detail": "R10/WEP/PPN/Newton/local-GR claims remain blocked"},
        {"check_id": "V737_17_validation_rows_ready", "result": "pass", "detail": "validation table constructed"},
    ]


def build_doc(
    source_register: list[dict[str, Any]],
    ward_rows: list[dict[str, Any]],
    obstruction_rows: list[dict[str, Any]],
    runner_rows: list[dict[str, Any]],
    input_rows: list[dict[str, Any]],
    decision_rows: list[dict[str, Any]],
    route_rows: list[dict[str, Any]],
    summary_rows: list[dict[str, Any]],
    validation_rows: list[dict[str, Any]],
) -> None:
    text = f"""# 737 - Y5 R10 Source-Current Ward Flux Closure Or Source-Backed Y5 Inputs

## Summary

Start point: 736 killed the direct representative matter-marker route conditionally, but left dressed source mass and projected source flux open.

Current verdict: **the Ward bridge is real, but projected source flux is not closed**.

```text
nabla_mu T_m^{{mu nu}} = 0
nabla_mu(T_m^{{mu nu}} tau_nu) = 0       if tau is observed Killing/stationary
d(Pi_M J_H) != proved zero
```

The important distinction is now explicit: matter stress conservation is not the same as a closed measured source-mass current. `Pi_M`, exchange terms, boundary/anomaly flux, and calibration still decide Y5.

| Item | Value |
| --- | --- |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Main result | same-frame Ward bridge written; projected flux closure blocked |
| Next target | `{NEXT_TARGET}` |

## Source-Current Ward Flux Attempt

{markdown_table(ward_rows, ["ward_id", "target_quantity", "theorem_or_formula", "premises", "derivation", "verdict", "residual_left", "valid_for_claim"])}

## Projected Mass Flux Obstruction

{markdown_table(obstruction_rows, ["obstruction_id", "problem", "formula", "required_kill", "status", "mapped_rows", "valid_for_claim"])}

## Y5 Runner Update

{markdown_table(runner_rows, ["runner_id", "source_row", "status_after_737", "zero_or_input", "still_missing", "valid_for_claim"])}

## Source-Backed Input Queue

{markdown_table(input_rows, ["input_id", "needed_input", "current_status", "why_not_claimable", "next_action", "valid_for_claim"])}

## Decision Matrix

{markdown_table(decision_rows, ["decision_id", "decision", "meaning", "claim_status", "next_target", "valid_for_claim"])}

## Route Update

{markdown_table(route_rows, ["route_id", "allowed_after_737", "forbidden_after_737", "next_action", "valid_for_claim"])}

## Nonclaim Summary

{markdown_table(summary_rows, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim"])}

## Source Register

{markdown_table(source_register, ["source_id", "path", "exists", "needle_check", "role"])}

## Validation

{markdown_table(validation_rows, ["check_id", "result", "detail"])}

## Plain-English Verdict

This is a solid bookkeeping win, not a victory lap. We have the Ward bridge: same-frame matter stress conservation can give a conserved current if there is a proper observed time generator. But the MTS local problem is the projected dressed source mass. Until `Pi_M` is parent-owned and its commutator/exchange/boundary terms vanish or are bounded, Y5 still blocks source-normalized Newton and local GR.
"""
    OUTPUT_DOC.write_text(text, encoding="utf-8")


def main() -> None:
    generated_utc = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    run_root = RUNS / f"737_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}"
    run_root.mkdir(parents=True, exist_ok=True)

    source_register = make_source_register(generated_utc)
    ward_rows = make_ward_attempt(generated_utc)
    obstruction_rows = make_obstruction_rows(generated_utc)
    runner_rows = make_y5_runner_update(generated_utc)
    input_rows = make_input_queue(generated_utc)
    decision_rows = make_decision_matrix(generated_utc)
    route_rows = make_route_update(generated_utc)
    summary_rows = make_summary(generated_utc)

    output_paths = [
        OUTPUT_DOC,
        SOURCE_REGISTER_PATH,
        WARD_ATTEMPT_PATH,
        OBSTRUCTION_PATH,
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
        WARD_ATTEMPT_PATH,
        ward_rows,
        ["ward_id", "target_quantity", "theorem_or_formula", "premises", "derivation", "verdict", "residual_left", "valid_for_claim", "source_paths", "generated_utc"],
    )
    write_csv(
        OBSTRUCTION_PATH,
        obstruction_rows,
        ["obstruction_id", "problem", "formula", "required_kill", "status", "mapped_rows", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        Y5_RUNNER_UPDATE_PATH,
        runner_rows,
        ["runner_id", "source_row", "status_after_737", "zero_or_input", "still_missing", "valid_for_claim", "source_paths", "generated_utc"],
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
        ["route_id", "allowed_after_737", "forbidden_after_737", "next_action", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        SUMMARY_PATH,
        summary_rows,
        ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim", "generated_utc"],
    )

    validation_rows = make_validation(source_register, ward_rows, obstruction_rows, runner_rows, input_rows, decision_rows, output_paths)
    write_csv(VALIDATION_PATH, validation_rows, ["check_id", "result", "detail"])
    build_doc(
        source_register,
        ward_rows,
        obstruction_rows,
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
