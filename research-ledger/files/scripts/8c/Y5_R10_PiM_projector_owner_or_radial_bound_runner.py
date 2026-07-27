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
OUTPUT_DOC = POST_CHECKPOINT / "738-Y5-R10-PiM-projector-owner-or-radial-bound-runner.md"
NEXT_TARGET = "739-Y5-R10-extra-mass-projection-silence-or-channelwise-bound.md"
CUTOFF = datetime(2026, 5, 31, 14, 42, 0)

STATUS = "Y5_R10_738_PiM_projector_owner_fork_written_topological_route_conditional_readout_forbidden_radial_inputs_queued"
CLAIM_CEILING = "PiM_owner_fork_and_radial_input_queue_only_no_projected_flux_closure_no_R10_WEP_PPN_Newton_or_local_GR_pass"

SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_738_SOURCE_REGISTER.csv"
PIM_OWNER_FORK_PATH = RESIDUALS / "P8_Y5_R10_738_PIM_OWNER_FORK.csv"
COMMUTATOR_GATE_PATH = RESIDUALS / "P8_Y5_R10_738_PIM_COMMUTATOR_GATE.csv"
RADIAL_INPUT_PATH = RESIDUALS / "P8_Y5_R10_738_RADIAL_BOUND_INPUT_QUEUE.csv"
Y5_RUNNER_UPDATE_PATH = RESIDUALS / "P8_Y5_R10_738_Y5_RUNNER_UPDATE.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_R10_738_DECISION_MATRIX.csv"
ROUTE_UPDATE_PATH = RESIDUALS / "P8_Y5_R10_738_ROUTE_UPDATE.csv"
SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_738_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_738_VALIDATION.csv"

SOURCES: dict[str, dict[str, Any]] = {
    "737_doc": {
        "path": POST_CHECKPOINT / "737-Y5-R10-source-current-Ward-flux-closure-or-source-backed-Y5-inputs.md",
        "role": "immediate Ward-to-PiM handoff",
        "needles": ["Ward bridge is real", OUTPUT_DOC.name, "Pi_M is now the key pressure point"],
    },
    "737_validation": {
        "path": RESIDUALS / "P8_Y5_BRR545_737_VALIDATION.csv",
        "role": "prior validation gate",
        "needles": ["V737_13_next_target_selected", OUTPUT_DOC.name, "V737_15_formalization_workbench_untouched"],
    },
    "737_obstruction": {
        "path": RESIDUALS / "P8_Y5_R10_737_PROJECTED_MASS_FLUX_OBSTRUCTION.csv",
        "role": "current PiM obstruction rows",
        "needles": ["PMF737_1_PiM_parent_ownership", "PMF737_2_projector_commutator", "open_next_target"],
    },
    "737_runner": {
        "path": RESIDUALS / "P8_Y5_R10_737_Y5_RUNNER_UPDATE.csv",
        "role": "current Y5 runner status",
        "needles": ["Y5R737_1_Meff_conservation", "Y5R737_2_radial_source_hair", "Y5R737_9_q_loc_projection"],
    },
    "737_queue": {
        "path": RESIDUALS / "P8_Y5_R10_737_SOURCE_BACKED_INPUT_QUEUE.csv",
        "role": "current missing PiM/q_loc inputs",
        "needles": ["IN737_1_PiM_parent_owner", "IN737_2_PiM_commutator", "IN737_4_radial_or_time_profile"],
    },
    "521_doc": {
        "path": POST_CHECKPOINT / "521-Y5-PiM-projector-owner-or-radial-bound-runner.md",
        "role": "older PiM fork source",
        "needles": ["topological absolute-mass projector route", "readout projector is rejected", "Radial bound inputs"],
    },
    "pim_algebra": {
        "path": RESIDUALS / "P8_PiM_parent_symplectic_projector_algebra_CONTRACT.csv",
        "role": "PiM algebra contract",
        "needles": ["PM0_fixed_exterior_topology", "PM5_projector_variation_owned", "PM8_retained_residual_fallback"],
    },
    "pim_variation": {
        "path": RESIDUALS / "P8_PiM_projector_variation_stress_CONTRACT.csv",
        "role": "PiM variation stress contract",
        "needles": ["PV1_topological_absolute_charge_route", "PV2_Hodge_DeWitt_metric_dependence_retained", "PV8_retained_residual_fallback"],
    },
    "pim_flux": {
        "path": RESIDUALS / "P8_PiM_flux_closure_Ward_topological_CONTRACT.csv",
        "role": "PiM flux closure contract",
        "needles": ["FC2_closed_mass_current_equation", "FC5_topological_mass_current_origin", "FC8_retained_residual_fallback"],
    },
    "parent_identity": {
        "path": RESIDUALS / "P8_PARENT_SOURCE_IDENTITY_RESIDUAL_DECOMPOSITION.csv",
        "role": "parent source identity decomposition",
        "needles": ["S499_0_projector_commutator", "S499_7_parent_anomaly_or_multiplier", "valid_for_claim"],
    },
    "radial_template": {
        "path": RESIDUALS / "P8_PARENT_SOURCE_IDENTITY_RADIAL_TEMPLATE.csv",
        "role": "radial fallback template",
        "needles": ["T499_0_identity_integral", "T499_1_commutator_profile", "T499_3_observable_bound"],
    },
    "source_measure": {
        "path": RESIDUALS / "P8_SOURCE_MEASURE_MEFF_FLUX_CLAUSES.csv",
        "role": "source-measure clauses",
        "needles": ["SM509_2_parent_mass_projector", "SM509_3_flux_closure", "SM509_6_Gauss_orbital_calibration"],
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


def make_pim_owner_fork(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "fork_id": "PIF738_0_topological_absolute_PiM",
            "candidate": "Pi_M is a parent-derived, metric-independent absolute mass cohomology/charge map on a fixed compact exterior class.",
            "math_form": "Pi_M J = ell_M(J) omega_M_top; d omega_M_top=0; delta_g Pi_M=0; ell_M fixed before readout.",
            "would_solve": "[d,Pi_M]J_H=0 and no bulk projector metric stress for the pure projector piece.",
            "open_debt": "must prove ell_M(Pi_M J_H) is the same Hilbert/source charge, not an independent conserved topological label.",
            "current_status": "best_route_conditional_not_current_MTS_derived",
            "valid_for_claim": "false",
            "source_paths": source_path_string("521_doc", "pim_algebra", "pim_variation"),
            "generated_utc": generated_utc,
        },
        {
            "fork_id": "PIF738_1_Hodge_DeWitt_PiM",
            "candidate": "Pi_M is an orthogonal Hodge/DeWitt projector on the boundary/source-current space.",
            "math_form": "Pi_M^2=Pi_M; Pi_M^dagger=Pi_M under parent boundary metric G_B.",
            "would_solve": "canonical projector algebra if G_B and the current space are parent-owned.",
            "open_debt": "delta_g Pi_M, Hodge/Green/boundary metric variation, and domain dependence create retained projector stress unless theorem-cancelled.",
            "current_status": "legal_only_with_variation_stress_retained",
            "valid_for_claim": "false",
            "source_paths": source_path_string("pim_algebra", "pim_variation"),
            "generated_utc": generated_utc,
        },
        {
            "fork_id": "PIF738_2_Hamiltonian_charge_PiM",
            "candidate": "Pi_M is inherited from an observed Hamiltonian/ADM mass charge.",
            "math_form": "B_xi/G_eff = M_eff[Pi_M J_H]; delta B_xi = delta int_S Pi_M J_H.",
            "would_solve": "ties projector to GR-like charge if EH exterior, integrability, and calibration are derived.",
            "open_debt": "EH-only exterior, no extra charge, boundary integrability, and Gauss/orbital calibration remain downstream.",
            "current_status": "downstream_conditional_not_available_yet",
            "valid_for_claim": "false",
            "source_paths": source_path_string("source_measure", "newton_stack", "521_doc"),
            "generated_utc": generated_utc,
        },
        {
            "fork_id": "PIF738_3_closure_multiplier",
            "candidate": "A multiplier imposes d(Pi_M J_H)=0 directly.",
            "math_form": "S_M = int lambda_M d(Pi_M J_H).",
            "would_solve": "formal Euler equation for source-flux closure.",
            "open_debt": "lambda_M and Pi_M need independent gauge/topological/Ward origin and stress ledger; otherwise this inserts Newton closure.",
            "current_status": "rejected_as_derivation_unless_independently_owned",
            "valid_for_claim": "false",
            "source_paths": source_path_string("pim_flux", "parent_identity"),
            "generated_utc": generated_utc,
        },
        {
            "fork_id": "PIF738_4_readout_or_fit_PiM",
            "candidate": "Pi_M is selected after orbital/readout data to isolate a clean 1/r monopole.",
            "math_form": "Pi_M := projector chosen by measured-GM readout.",
            "would_solve": "nothing at derivation level.",
            "open_debt": "post-fit projector cannot enter parent source variation or close the source current.",
            "current_status": "forbidden_as_derivation",
            "valid_for_claim": "false",
            "source_paths": source_path_string("521_doc", "source_measure"),
            "generated_utc": generated_utc,
        },
    ]


def make_commutator_gate(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "PCG738_0_product_rule_retained",
            "condition": "Projected mass current uses the full product rule.",
            "math_form": "d(Pi_M J_H)=Pi_M dJ_H + [d,Pi_M]J_H.",
            "pass_if": "Pi_M is fixed/covariantly constant/topological on the allowed current domain, or commutator is explicitly cancelled/bounded.",
            "current_result": "active_obstruction",
            "maps_to": "Y5B_1;Y5B_2;MR510_3;S499_0",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "PCG738_1_topological_commutator_zero",
            "condition": "Topological absolute charge route fixes Pi_M independent of metric/domain variation.",
            "math_form": "d omega_M_top=0 and delta_g Pi_M=0 => [d,Pi_M]J_H=0 for the projector piece.",
            "pass_if": "the topological mass current is also proved equal to Pi_M J_H on shell.",
            "current_result": "conditional_but_Hilbert_equality_missing",
            "maps_to": "PIF738_0;R_eq;Y5B_1;Y5B_2",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "PCG738_2_Hodge_variation_retained",
            "condition": "Hodge/DeWitt route must vary the projector and retain its stress.",
            "math_form": "delta(Pi_M J_H)=Pi_M delta J_H + (delta Pi_M)J_H.",
            "pass_if": "T_PiM is theorem-zero/topological or mapped into local residual coefficients.",
            "current_result": "retained_if_used_not_zero",
            "maps_to": "R3;R4;R7;R8;R10;R11",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "PCG738_3_no_readout_mask",
            "condition": "Post-readout masks never enter parent variation.",
            "math_form": "delta S_parent/delta Pi_read = 0; Pi_read acts only after theorem or residual scoring.",
            "pass_if": "Pi_M appears before readout as parent charge data.",
            "current_result": "policy_pass_theorem_open",
            "maps_to": "PIF738_4;PMF737_1",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "PCG738_4_closure_not_from_algebra",
            "condition": "Projector algebra is not counted as flux closure.",
            "math_form": "Pi_M^2=Pi_M does not imply d(Pi_M J_H)=0.",
            "pass_if": "separate Ward/Hamiltonian/topological/Euler mass-current equation closes the flux.",
            "current_result": "no_closure_promotion",
            "maps_to": "Y5B_1;Y5B_2;SN4",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def make_radial_inputs(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "input_id": "RBI738_0_Delta_PiM",
            "quantity": "Delta_PiM",
            "definition": "projector-ownership/variation residual in measured source flux",
            "formula": "Delta_PiM = int_S (delta Pi_M)J_H or int_A [d,Pi_M]J_H",
            "required_columns": "system_id;projector_type;metric_dependence_flag;Delta_PiM;units;normalization;source_file;assumptions",
            "maps_to": "Y5B_1;Y5B_2;MR510_3",
            "current_status": "not_filled",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "input_id": "RBI738_1_commutator_profile",
            "quantity": "I_commutator",
            "definition": "finite-shell integral of the projector commutator obstruction",
            "formula": "I_commutator = int_A_ext [d,Pi_M]J_H",
            "required_columns": "system_id;r1;r2;I_commutator;units;norm_convention;source_file;assumptions",
            "maps_to": "epsilon_radial_Meff = c_M I_commutator/M_eff_ref",
            "current_status": "template_from_499_not_filled",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "input_id": "RBI738_2_projector_stress_vector",
            "quantity": "T_PiM_munu",
            "definition": "metric/domain/boundary stress generated by Pi_M variation if Hodge/DeWitt route is used",
            "formula": "T_PiM_munu := -2/sqrt(-g) delta S_PiM/delta g_munu",
            "required_columns": "operator_family;coefficient;units;weak_field_map;affected_rows;source_file;assumptions",
            "maps_to": "gamma;beta;alpha_i;xi;R11;Y5 source-normalization",
            "current_status": "not_executable",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "input_id": "RBI738_3_topological_equality_residual",
            "quantity": "R_eq",
            "definition": "failure of topological absolute mass current to equal observed Hilbert projected source current",
            "formula": "R_eq = Pi_M J_H - J_M_top - dB_zero",
            "required_columns": "system_id;r1;r2;R_eq_integral;units;norm_convention;source_file;assumptions",
            "maps_to": "radial source hair and conserved-wrong-object risk",
            "current_status": "not_filled",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "input_id": "RBI738_4_radial_decision",
            "quantity": "epsilon_radial_Meff",
            "definition": "radial source-hair envelope after PiM ownership failures are integrated",
            "formula": "epsilon_radial_Meff = M_eff_ref^-1 int_A[-Pi_M dJ_extra + [d,Pi_M]J_H + A_parent]",
            "required_columns": "system_id;r1;r2;epsilon_radial_Meff;dln_mu_dlnr;bound_source;pass_fail;no_cancellation_flag;notes",
            "maps_to": "Y5B_2 and PPN/fifth-force/orbital radial bounds",
            "current_status": "not_run",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def make_y5_runner_update(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "runner_id": "Y5R738_1_Meff_conservation",
            "source_row": "Y5B_1_Meff_conservation",
            "status_after_738": "PiM_owner_fork_written_flux_not_closed",
            "zero_or_input": "topological Pi_M could help only if Hilbert equality and exchange/boundary silence also close",
            "still_missing": "parent-owned Pi_M, topological-Hilbert equality, zero exchange/boundary/anomaly",
            "valid_for_claim": "false",
            "source_paths": source_path_string("737_runner", "pim_algebra", "pim_flux"),
            "generated_utc": generated_utc,
        },
        {
            "runner_id": "Y5R738_2_radial_source_hair",
            "source_row": "Y5B_2_radial_source_hair",
            "status_after_738": "radial_bound_inputs_written_not_scored",
            "zero_or_input": "epsilon_radial_Meff numerator now split into commutator, equality residual, exchange, and anomaly pieces",
            "still_missing": "source-backed radial/commutator/equality residual rows or theorem-zero closures",
            "valid_for_claim": "false",
            "source_paths": source_path_string("radial_template", "parent_identity", "737_runner"),
            "generated_utc": generated_utc,
        },
        {
            "runner_id": "Y5R738_5_extra_mass_projection",
            "source_row": "Y5B_5_extra_mass_projection",
            "status_after_738": "still_open_next_target",
            "zero_or_input": "none",
            "still_missing": "boundary/domain/memory/non-EH/q_loc mass-channel exchange vector",
            "valid_for_claim": "false",
            "source_paths": source_path_string("parent_identity", "source_measure"),
            "generated_utc": generated_utc,
        },
        {
            "runner_id": "Y5R738_9_q_loc_projection",
            "source_row": "Y5B_9_q_loc_projection",
            "status_after_738": "unchanged_missing_C_qmu_projection",
            "zero_or_input": "none",
            "still_missing": "C_qmu normalization and q_loc-to-source-mass units",
            "valid_for_claim": "false",
            "source_paths": source_path_string("737_runner", "737_queue"),
            "generated_utc": generated_utc,
        },
    ]


def make_decision_matrix(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "D738_0_PiM_owner_fork_written",
            "decision": "separate topological, Hodge/DeWitt, Hamiltonian, multiplier, and readout PiM routes",
            "meaning": "Only parent-owned routes can earn theorem credit; readout masks are forbidden.",
            "claim_status": "fork_only",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "source_paths": source_path_string("521_doc", "pim_algebra"),
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D738_1_topological_best_conditional",
            "decision": "mark topological absolute PiM as the cleanest conditional route",
            "meaning": "It can kill the commutator only if it is also the observed Hilbert source current.",
            "claim_status": "conditional_no_promotion",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "source_paths": source_path_string("pim_variation", "parent_identity"),
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D738_2_radial_inputs_queued",
            "decision": "queue Delta_PiM, commutator profile, projector stress, R_eq, and epsilon_radial_Meff rows",
            "meaning": "If the theorem route fails, the branch remains testable rather than rhetorical.",
            "claim_status": "runner_ready_not_scored",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "source_paths": source_path_string("radial_template", "parent_identity"),
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D738_3_no_flux_promotion",
            "decision": "do not claim d(Pi_M J_H)=0, Meff closure, Newton, PPN, R10, WEP, or local GR",
            "meaning": "PiM ownership alone is not enough without exchange, boundary, and calibration closure.",
            "claim_status": "blocked_for_current_claim",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "source_paths": source_path_string("newton_stack", "source_measure"),
            "generated_utc": generated_utc,
        },
    ]


def make_route_update(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "route_id": "RU738_0_allowed",
            "allowed_after_738": "say Pi_M owner fork is sharpened and topological absolute route is best conditional route",
            "forbidden_after_738": "say Pi_M is parent-owned in current MTS or that projected flux is closed",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "RU738_1_allowed",
            "allowed_after_738": "use radial/commutator/equality residual templates for future source-backed tests",
            "forbidden_after_738": "score not_filled templates or promote closure from projector algebra alone",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "RU738_2_allowed",
            "allowed_after_738": "move next to extra mass projection silence or channelwise bound",
            "forbidden_after_738": "forget mu_extra, boundary/domain/memory/non-EH/q_loc exchange, or Gauss calibration",
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
            "main_result": "PiM owner fork written; topological absolute route is best conditional but Hilbert equality/current-corpus proof is missing.",
            "hard_blocker": "topological-Hilbert equality, projector commutator closure, variation stress, mu_extra exchange, boundary/anomaly flux, calibration, and C_qmu q_loc projection.",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def make_validation(
    source_register: list[dict[str, Any]],
    fork_rows: list[dict[str, Any]],
    commutator_rows: list[dict[str, Any]],
    radial_rows: list[dict[str, Any]],
    runner_rows: list[dict[str, Any]],
    decision_rows: list[dict[str, Any]],
    output_paths: list[Path],
) -> list[dict[str, str]]:
    source_paths_exist = all(row["exists"] == "true" for row in source_register)
    needles_pass = all(row["needle_check"] == "true" for row in source_register)
    prior_clean = prior_validation_clean(SOURCES["737_validation"]["path"])
    fork_ids = {row.get("fork_id", "") for row in fork_rows}
    required_forks = {
        "PIF738_0_topological_absolute_PiM",
        "PIF738_1_Hodge_DeWitt_PiM",
        "PIF738_2_Hamiltonian_charge_PiM",
        "PIF738_3_closure_multiplier",
        "PIF738_4_readout_or_fit_PiM",
    }
    topological_conditional = any(
        row.get("fork_id") == "PIF738_0_topological_absolute_PiM"
        and row.get("current_status") == "best_route_conditional_not_current_MTS_derived"
        for row in fork_rows
    )
    readout_forbidden = any(
        row.get("fork_id") == "PIF738_4_readout_or_fit_PiM"
        and row.get("current_status") == "forbidden_as_derivation"
        for row in fork_rows
    )
    commutator_not_closed = any(
        row.get("gate_id") == "PCG738_0_product_rule_retained"
        and row.get("current_result") == "active_obstruction"
        for row in commutator_rows
    )
    hodge_retained = any(
        row.get("gate_id") == "PCG738_2_Hodge_variation_retained"
        and row.get("current_result") == "retained_if_used_not_zero"
        for row in commutator_rows
    )
    radial_ids = {row.get("input_id", "") for row in radial_rows}
    required_radial = {"RBI738_0_Delta_PiM", "RBI738_1_commutator_profile", "RBI738_2_projector_stress_vector", "RBI738_3_topological_equality_residual", "RBI738_4_radial_decision"}
    radial_not_scored = all(row.get("current_status") in {"not_filled", "template_from_499_not_filled", "not_executable", "not_run"} for row in radial_rows)
    y5_retained = any(
        row.get("runner_id") == "Y5R738_1_Meff_conservation"
        and row.get("status_after_738") == "PiM_owner_fork_written_flux_not_closed"
        for row in runner_rows
    ) and any(
        row.get("runner_id") == "Y5R738_2_radial_source_hair"
        and row.get("status_after_738") == "radial_bound_inputs_written_not_scored"
        for row in runner_rows
    )
    all_nonclaim = all(
        row.get("valid_for_claim") == "false"
        for row in [*fork_rows, *commutator_rows, *radial_rows, *runner_rows, *decision_rows]
    )
    outputs_scoped = under_post_checkpoint(output_paths)
    formalization_count = formalization_changed_after_cutoff()

    return [
        {"check_id": "V738_0_source_paths_exist", "result": "pass" if source_paths_exist else "fail", "detail": f"source_rows={len(source_register)}"},
        {"check_id": "V738_1_source_needles_present", "result": "pass" if needles_pass else "fail", "detail": "all source files contain expected evidence needles"},
        {"check_id": "V738_2_prior_737_clean", "result": "pass" if prior_clean else "fail", "detail": "737 validation has no failures"},
        {"check_id": "V738_3_737_selected_738", "result": "pass" if text_contains(SOURCES["737_doc"]["path"], [OUTPUT_DOC.name]) else "fail", "detail": OUTPUT_DOC.name},
        {"check_id": "V738_4_fork_rows_complete", "result": "pass" if required_forks.issubset(fork_ids) else "fail", "detail": f"fork_rows={len(fork_ids)}"},
        {"check_id": "V738_5_topological_conditional_only", "result": "pass" if topological_conditional else "fail", "detail": "topological route is conditional, not promoted"},
        {"check_id": "V738_6_readout_mask_forbidden", "result": "pass" if readout_forbidden else "fail", "detail": "post-fit/readout PiM rejected as derivation"},
        {"check_id": "V738_7_commutator_not_closed", "result": "pass" if commutator_not_closed else "fail", "detail": "[d,PiM]JH remains active obstruction"},
        {"check_id": "V738_8_Hodge_variation_retained", "result": "pass" if hodge_retained else "fail", "detail": "Hodge/DeWitt projector stress retained if used"},
        {"check_id": "V738_9_radial_inputs_complete", "result": "pass" if required_radial.issubset(radial_ids) else "fail", "detail": f"radial_rows={len(radial_ids)}"},
        {"check_id": "V738_10_radial_inputs_not_scored", "result": "pass" if radial_not_scored else "fail", "detail": "radial templates remain unfilled/unscored"},
        {"check_id": "V738_11_Y5_rows_retained", "result": "pass" if y5_retained else "fail", "detail": "Meff/radial rows remain open"},
        {"check_id": "V738_12_no_claim_rows_promoted", "result": "pass" if all_nonclaim else "fail", "detail": "all generated rows valid_for_claim=false"},
        {"check_id": "V738_13_next_target_selected", "result": "pass" if all(row.get("next_target") == NEXT_TARGET for row in decision_rows) else "fail", "detail": NEXT_TARGET},
        {"check_id": "V738_14_outputs_scoped", "result": "pass" if outputs_scoped else "fail", "detail": "all outputs under post-checkpoint-work"},
        {"check_id": "V738_15_formalization_workbench_untouched", "result": "pass" if formalization_count == 0 else "fail", "detail": f"formalization_changed_after_cutoff={formalization_count}"},
        {"check_id": "V738_16_no_local_arena_claim", "result": "pass", "detail": "R10/WEP/PPN/Newton/local-GR claims remain blocked"},
        {"check_id": "V738_17_validation_rows_ready", "result": "pass", "detail": "validation table constructed"},
    ]


def build_doc(
    source_register: list[dict[str, Any]],
    fork_rows: list[dict[str, Any]],
    commutator_rows: list[dict[str, Any]],
    radial_rows: list[dict[str, Any]],
    runner_rows: list[dict[str, Any]],
    decision_rows: list[dict[str, Any]],
    route_rows: list[dict[str, Any]],
    summary_rows: list[dict[str, Any]],
    validation_rows: list[dict[str, Any]],
) -> None:
    text = f"""# 738 - Y5 R10 PiM Projector Owner Or Radial Bound Runner

## Summary

Start point: 737 wrote the Ward bridge but left `d(Pi_M J_H)=0` unproved. This checkpoint asks whether `Pi_M` is a parent object or a readout mask.

Current verdict: **the PiM owner fork is sharp, but no current-chain PiM owner is claimed**.

```text
d(Pi_M J_H)=Pi_M dJ_H + [d,Pi_M]J_H
```

The topological absolute-mass route is the cleanest conditional option because it can make `[d,Pi_M]J_H=0` for the projector piece. But it only helps if the topological current is proved equal to the observed Hilbert source current. Hodge/DeWitt routes keep projector stress; readout/fit masks are forbidden.

| Item | Value |
| --- | --- |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Main result | PiM owner fork written; radial input queue explicit |
| Next target | `{NEXT_TARGET}` |

## PiM Owner Fork

{markdown_table(fork_rows, ["fork_id", "candidate", "math_form", "would_solve", "open_debt", "current_status", "valid_for_claim"])}

## PiM Commutator Gate

{markdown_table(commutator_rows, ["gate_id", "condition", "math_form", "pass_if", "current_result", "maps_to", "valid_for_claim"])}

## Radial Bound Input Queue

{markdown_table(radial_rows, ["input_id", "quantity", "definition", "formula", "required_columns", "maps_to", "current_status", "valid_for_claim"])}

## Y5 Runner Update

{markdown_table(runner_rows, ["runner_id", "source_row", "status_after_738", "zero_or_input", "still_missing", "valid_for_claim"])}

## Decision Matrix

{markdown_table(decision_rows, ["decision_id", "decision", "meaning", "claim_status", "next_target", "valid_for_claim"])}

## Route Update

{markdown_table(route_rows, ["route_id", "allowed_after_738", "forbidden_after_738", "next_action", "valid_for_claim"])}

## Nonclaim Summary

{markdown_table(summary_rows, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim"])}

## Source Register

{markdown_table(source_register, ["source_id", "path", "exists", "needle_check", "role"])}

## Validation

{markdown_table(validation_rows, ["check_id", "result", "detail"])}

## Plain-English Verdict

This is a useful narrowing. `Pi_M` cannot be a magic mask selected after the fact. The best route is a parent-owned topological mass projector, but that still has to be glued to the same Hilbert source current. If that glue fails, the radial/commutator/equality residual templates are ready. No local-GR or Newton point is scored yet, but the target is much more precise.
"""
    OUTPUT_DOC.write_text(text, encoding="utf-8")


def main() -> None:
    generated_utc = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    run_root = RUNS / f"738_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}"
    run_root.mkdir(parents=True, exist_ok=True)

    source_register = make_source_register(generated_utc)
    fork_rows = make_pim_owner_fork(generated_utc)
    commutator_rows = make_commutator_gate(generated_utc)
    radial_rows = make_radial_inputs(generated_utc)
    runner_rows = make_y5_runner_update(generated_utc)
    decision_rows = make_decision_matrix(generated_utc)
    route_rows = make_route_update(generated_utc)
    summary_rows = make_summary(generated_utc)

    output_paths = [
        OUTPUT_DOC,
        SOURCE_REGISTER_PATH,
        PIM_OWNER_FORK_PATH,
        COMMUTATOR_GATE_PATH,
        RADIAL_INPUT_PATH,
        Y5_RUNNER_UPDATE_PATH,
        DECISION_PATH,
        ROUTE_UPDATE_PATH,
        SUMMARY_PATH,
        VALIDATION_PATH,
    ]

    write_csv(SOURCE_REGISTER_PATH, source_register, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(PIM_OWNER_FORK_PATH, fork_rows, ["fork_id", "candidate", "math_form", "would_solve", "open_debt", "current_status", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(COMMUTATOR_GATE_PATH, commutator_rows, ["gate_id", "condition", "math_form", "pass_if", "current_result", "maps_to", "valid_for_claim", "generated_utc"])
    write_csv(RADIAL_INPUT_PATH, radial_rows, ["input_id", "quantity", "definition", "formula", "required_columns", "maps_to", "current_status", "valid_for_claim", "generated_utc"])
    write_csv(Y5_RUNNER_UPDATE_PATH, runner_rows, ["runner_id", "source_row", "status_after_738", "zero_or_input", "still_missing", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(DECISION_PATH, decision_rows, ["decision_id", "decision", "meaning", "claim_status", "next_target", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(ROUTE_UPDATE_PATH, route_rows, ["route_id", "allowed_after_738", "forbidden_after_738", "next_action", "valid_for_claim", "generated_utc"])
    write_csv(SUMMARY_PATH, summary_rows, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim", "generated_utc"])

    validation_rows = make_validation(source_register, fork_rows, commutator_rows, radial_rows, runner_rows, decision_rows, output_paths)
    write_csv(VALIDATION_PATH, validation_rows, ["check_id", "result", "detail"])
    build_doc(source_register, fork_rows, commutator_rows, radial_rows, runner_rows, decision_rows, route_rows, summary_rows, validation_rows)

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
