from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


POST_CHECKPOINT = Path(__file__).resolve().parents[1]
REPO_ROOT = POST_CHECKPOINT.parent
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"
FORMALIZATION = REPO_ROOT / "formalization-workbench"

OUTPUT_DOC = POST_CHECKPOINT / "741-Y5-R10-Cqmu-parent-owner-or-compact-shell-unit-map.md"
NEXT_TARGET = "742-Y5-R10-observed-tau-owner-or-q_loc-free-coefficient-pack.md"
STATUS = "Y5_R10_741_Cqmu_parent_owner_fork_written_tau_and_NM_missing_compact_shell_unit_map_blocked"
CLAIM_CEILING = "Cqmu_owner_fork_and_unit_map_gate_only_no_q_loc_bound_no_mu_extra_zero_no_R10_PPN_Newton_or_local_GR_pass"

SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_741_SOURCE_REGISTER.csv"
OWNER_FORK_PATH = RESIDUALS / "P8_Y5_R10_741_CQMU_OWNER_FORK.csv"
UNIT_MAP_PATH = RESIDUALS / "P8_Y5_R10_741_COMPACT_SHELL_UNIT_MAP_GATE.csv"
FREE_COEFF_PATH = RESIDUALS / "P8_Y5_R10_741_FREE_COEFFICIENT_PACK_QUEUE.csv"
Y5_UPDATE_PATH = RESIDUALS / "P8_Y5_R10_741_Y5_RUNNER_UPDATE.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_R10_741_DECISION_MATRIX.csv"
ROUTE_PATH = RESIDUALS / "P8_Y5_R10_741_ROUTE_UPDATE.csv"
SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_741_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_741_VALIDATION.csv"

FORMALIZATION_CUTOFF = datetime(2026, 5, 31, 14, 42, 0)


SOURCES: dict[str, dict[str, Any]] = {
    "740_doc": {
        "path": POST_CHECKPOINT / "740-Y5-R10-q_loc-mass-channel-map-or-first-source-backed-extra-bound.md",
        "needles": [OUTPUT_DOC.name, "C_qmu", "compact-shell value is useful as a breadcrumb"],
        "role": "immediate q_loc/Cqmu handoff",
    },
    "740_validation": {
        "path": RESIDUALS / "P8_Y5_BRR545_740_VALIDATION.csv",
        "needles": ["V740_12_next_target_selected", "V740_14_formalization_workbench_untouched", "V740_15_no_local_arena_claim"],
        "role": "prior validation guard",
    },
    "740_mass_map": {
        "path": RESIDUALS / "P8_Y5_R10_740_QLOC_MASS_CHANNEL_MAP.csv",
        "needles": ["QMM740_2_killing_mass_projection", "C_{q nu}=N_M tau_nu", "QMM740_4_bound_fallback"],
        "role": "Cqmu candidate and bound fallback",
    },
    "740_silence_gate": {
        "path": RESIDUALS / "P8_Y5_R10_740_CQMU_SILENCE_GATE.csv",
        "needles": ["CQG740_1_mass_generator_orthogonality", "CQG740_4_units_and_no_readout", "mixed_until_projection_fixed"],
        "role": "Cqmu silence and no-readout gates",
    },
    "740_bound_attempt": {
        "path": RESIDUALS / "P8_Y5_R10_740_FIRST_QLOC_BOUND_ATTEMPT.csv",
        "needles": ["QBA740_0_compact_shell_proxy", "7.432631961576971e-06", "blocked_Cqmu_missing"],
        "role": "compact-shell proxy and blocked Y5 mass projection",
    },
    "740_observable_map": {
        "path": RESIDUALS / "P8_Y5_R10_740_QLOC_OBSERVABLE_TRANSFER_MAP.csv",
        "needles": ["QOT740_0_Y5_source_strength", "C_qmu;M_eff_ref", "QOT740_4_R10_range"],
        "role": "observable transfer inputs",
    },
    "source_measure_clauses": {
        "path": RESIDUALS / "P8_SOURCE_MEASURE_MEFF_FLUX_CLAUSES.csv",
        "needles": ["SM509_0_observed_generator", "tau_source = tau_Hilbert = tau_orbit", "SM509_6_Gauss_orbital_calibration"],
        "role": "same observed generator and calibration contract",
    },
    "pim_flux_contract": {
        "path": RESIDUALS / "P8_PiM_flux_closure_Ward_topological_CONTRACT.csv",
        "needles": ["FC1_stationary_or_Hamiltonian_time_generator", "FC7_absolute_calibration_after_closure", "FC8_retained_residual_fallback"],
        "role": "stationary/Hamiltonian mass-current route",
    },
    "pim_algebra_contract": {
        "path": RESIDUALS / "P8_PiM_parent_symplectic_projector_algebra_CONTRACT.csv",
        "needles": ["PM2_harmonic_mass_generator", "PM3_charge_functional_before_readout", "PM7_absolute_calibration_deferred"],
        "role": "parent mass-generator/projector algebra",
    },
    "qloc_bound_spec": {
        "path": RESIDUALS / "P8_QLOC_BOUND_RUNNER_SPEC.csv",
        "needles": ["QB516_0_compact_shell_budget", "map this dimensionless proxy into PPN/source-normalization units", "QB516_2_Gdot_GMdot"],
        "role": "compact-shell proxy unit-map demand",
    },
    "y5_bound_input": {
        "path": RESIDUALS / "P8_Y5_SOURCE_NORMALIZATION_BOUND_RUNNER_INPUT.csv",
        "needles": ["Y5B_9_q_loc_projection", "C_qmu q_loc", "mixed_until_projection_fixed"],
        "role": "Y5 q_loc source-normalization row",
    },
    "737_input_queue": {
        "path": RESIDUALS / "P8_Y5_R10_737_SOURCE_BACKED_INPUT_QUEUE.csv",
        "needles": ["IN737_0_observed_tau", "IN737_5_C_qmu_projection", "compact-shell proxy is still dimensionless"],
        "role": "observed tau and Cqmu missing-input queue",
    },
    "constant_gm_gate": {
        "path": RESIDUALS / "P8_CONSTANT_GM_DERIVATIVE_HAIR_GATE.csv",
        "needles": ["CGM0_master_identity", "D_X ln mu_obs", "C" if False else "R10"],
        "role": "derivative-hair guard after source normalization",
    },
}


def utc_stamp() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def text_contains(path: Path, needles: list[str]) -> bool:
    text = read_text(path)
    return bool(text) and all(needle in text for needle in needles)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def markdown_cell(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(markdown_cell(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, divider, *body])


def bool_string(value: bool) -> str:
    return "true" if value else "false"


def under_post(path: Path) -> bool:
    try:
        path.resolve().relative_to(POST_CHECKPOINT.resolve())
        return True
    except ValueError:
        return False


def formalization_changed_after_cutoff() -> int:
    if not FORMALIZATION.exists():
        return -1
    count = 0
    for path in FORMALIZATION.rglob("*"):
        if path.is_file():
            modified = datetime.fromtimestamp(path.stat().st_mtime)
            if modified > FORMALIZATION_CUTOFF:
                count += 1
    return count


def make_source_register(generated_utc: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, spec in SOURCES.items():
        path = Path(spec["path"])
        rows.append(
            {
                "source_id": source_id,
                "path": str(path),
                "exists": bool_string(path.exists()),
                "needle_check": bool_string(text_contains(path, spec["needles"])),
                "role": spec["role"],
                "valid_for_claim": "false",
                "generated_utc": generated_utc,
            }
        )
    return rows


def owner_fork_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "owner_id": "CQM741_0_parent_tau_contraction",
            "candidate_owner": "C_qnu=N_M tau_nu",
            "math_form": "I_q[A]=N_M int_A tau_nu q_loc^nu dV",
            "would_solve": "turns q_loc mass-channel projection into contraction with the same observed mass/time generator used by source measure",
            "current_result": "best_conditional_route_not_current_derived",
            "missing": "tau_source=tau_Hilbert=tau_orbit as parent object; N_M units; no-readout proof; tau.q_loc theorem or bound",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "owner_id": "CQM741_1_Hamiltonian_boundary_owner",
            "candidate_owner": "C_q from Hamiltonian boundary variation delta H_tau",
            "math_form": "C_qnu q_loc^nu dV := delta_tau H_extra or source-current defect in the Hamiltonian mass charge",
            "would_solve": "connects C_q directly to source charge bookkeeping before orbital calibration",
            "current_result": "downstream_conditional_not_available",
            "missing": "integrable Hamiltonian charge, boundary reference lock, PiM Hilbert equality, and exact defect-to-q_loc map",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "owner_id": "CQM741_2_topological_mass_generator_owner",
            "candidate_owner": "C_q from harmonic/topological mass generator omega_M",
            "math_form": "C_qnu q_loc^nu ~ ell_M(P_loc nabla_mu T_GK^{mu nu})",
            "would_solve": "could give metric-independent normalization if ell_M equals observed Hilbert/source mass",
            "current_result": "conditional_but_Hilbert_equality_missing",
            "missing": "topological-Hilbert equality, source-current equality, and unit normalization to M_eff_ref",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "owner_id": "CQM741_3_free_projection_coefficient",
            "candidate_owner": "C_q as explicit residual coefficient vector",
            "math_form": "epsilon_q_loc = c_q * q_proxy or c_q(lambda,row) * q_profile",
            "would_solve": "does not derive silence, but makes falsifiable coefficient rows for Y5/PPN/R10",
            "current_result": "fallback_queue_only",
            "missing": "source-backed c_q, units, row mapping, priors, no-cancellation flag, and bound comparison",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "owner_id": "CQM741_4_readout_mask",
            "candidate_owner": "C_q chosen after orbital/PPN/R10 data",
            "math_form": "C_q := argmin residual after readout",
            "would_solve": "nothing at derivation level",
            "current_result": "forbidden_as_derivation",
            "missing": "post-readout masks cannot define parent source-normalization maps",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def unit_map_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "unit_gate_id": "CSU741_0_proxy_loaded",
            "quantity": "q_proxy",
            "formula": "q_proxy=max_abs_Ploc_drelJrel=7.432631961576971e-06",
            "needed_to_score": "prove q_proxy is the same norm entering int_A tau.q_loc or supply conversion factor",
            "current_result": "source_backed_internal_proxy",
            "why_blocked": "dimensionless proxy has no C_q, M_eff_ref, shell-volume, or arena units",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "unit_gate_id": "CSU741_1_Y5_mass_units",
            "quantity": "epsilon_q_loc_Y5",
            "formula": "epsilon_q_loc = |N_M int_A tau_nu q_loc^nu dV|/M_eff_ref",
            "needed_to_score": "N_M, tau normalization, integration measure, M_eff_ref, q_loc profile, source path",
            "current_result": "not_executable",
            "why_blocked": "N_M and M_eff_ref are not parent-fixed for the q_loc channel",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "unit_gate_id": "CSU741_2_time_drift_units",
            "quantity": "dln_mu_obs_dt",
            "formula": "dln_mu_obs_dt|_q = partial_t epsilon_q_loc or shell time-flux of I_q/M_eff_ref",
            "needed_to_score": "time window, observed tau, derivative convention, yr^-1 conversion, Gdot bound source",
            "current_result": "not_executable",
            "why_blocked": "compact proxy is a static dimensionless amplitude, not a time derivative",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "unit_gate_id": "CSU741_3_R10_range_units",
            "quantity": "alpha_q_loc(lambda)",
            "formula": "alpha_q(lambda)=c_q(lambda) q_proxy or alpha from a q_loc Green kernel",
            "needed_to_score": "lambda, source-normalization, q_loc kernel, alpha coefficient, real bound curve comparison",
            "current_result": "not_executable",
            "why_blocked": "no range kernel or alpha coefficient is supplied",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "unit_gate_id": "CSU741_4_PPN_units",
            "quantity": "Delta_PPN_q_loc",
            "formula": "Delta_PPN = G_PPN[q_loc source] after gauge-fixed weak-field solve",
            "needed_to_score": "Green operator, gauge, component split, official PPN row map",
            "current_result": "not_executable",
            "why_blocked": "C_q mass units do not by themselves provide spatial/vector/STF metric response",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def free_coeff_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "queue_id": "FCQ741_0_Cq_scalar_mass",
            "target_row": "Y5B_9_q_loc_projection",
            "coefficient": "c_qM",
            "template_formula": "epsilon_q_loc_Y5 = abs(c_qM * q_proxy)",
            "required_columns": "c_qM;units;q_proxy;M_eff_ref;source_file;prior_or_derivation;no_cancellation_flag",
            "current_status": "template_only",
            "acceptance_gate": "valid only if c_qM is parent-derived or source-backed and compared to a specific bound",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "queue_id": "FCQ741_1_Cq_time",
            "target_row": "Y5B_0/Y5B_1",
            "coefficient": "c_qt",
            "template_formula": "dln_mu_dt|_q = c_qt * q_proxy / Delta_t",
            "required_columns": "c_qt;Delta_t;units_yr^-1;source_file;Gdot_bound;no_cancellation_flag",
            "current_status": "template_only",
            "acceptance_gate": "requires actual time profile, not static proxy amplitude",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "queue_id": "FCQ741_2_Cq_R10",
            "target_row": "R10_fifth_force",
            "coefficient": "c_q_alpha(lambda)",
            "template_formula": "alpha_q_loc(lambda)=c_q_alpha(lambda)*q_proxy",
            "required_columns": "lambda;alpha_predicted;alpha_bound;curve_source;c_q_alpha_source;no_cancellation_flag",
            "current_status": "template_only",
            "acceptance_gate": "requires full alpha(lambda) curve or theorem-zero no-range proof",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "queue_id": "FCQ741_3_Cq_PPN",
            "target_row": "Y5B_8/R3-R8",
            "coefficient": "c_q_PPN_vector",
            "template_formula": "Delta_PPN_q = c_q_PPN_vector * q_proxy",
            "required_columns": "component;coefficient;units;PPN_bound;weak_field_map;source_file;no_cancellation_flag",
            "current_status": "template_only",
            "acceptance_gate": "each component must pass separately; no total-vector cancellation",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def y5_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "runner_id": "Y5R741_9_q_loc_projection",
            "source_row": "Y5B_9_q_loc_projection",
            "status_after_741": "Cqmu_owner_fork_written_no_unit_map",
            "zero_or_input": "best route C_qnu=N_M tau_nu is conditional; free-coefficient fallback queued",
            "still_missing": "observed tau ownership, N_M, M_eff_ref, q_loc profile, compact-shell conversion, no-readout proof",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "runner_id": "Y5R741_5_extra_mass_projection",
            "source_row": "Y5B_5_extra_mass_projection",
            "status_after_741": "q_loc_channel_still_open",
            "zero_or_input": "q_loc remains a separate no-cancellation channel in mu_extra envelope",
            "still_missing": "same Cqmu unit map plus channelwise bound or theorem-zero",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "runner_id": "Y5R741_8_PPN_source_vector",
            "source_row": "Y5B_8_full_PPN_source_vector",
            "status_after_741": "PPN_free_coefficient_template_only",
            "zero_or_input": "Cq PPN vector template queued but unfilled",
            "still_missing": "weak-field map and component coefficients",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "D741_0_best_route",
            "decision": "try C_qnu=N_M tau_nu as the clean parent route",
            "meaning": "this keeps q_loc mass projection tied to the observed source generator rather than a fitted mask",
            "claim_status": "conditional_only",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D741_1_no_owner_claim",
            "decision": "do not claim Cqmu is parent-owned",
            "meaning": "observed tau, N_M, source/Hamiltonian/orbit equality, and no-readout proof remain absent",
            "claim_status": "blocked_for_current_claim",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D741_2_proxy_still_not_bound",
            "decision": "do not convert compact proxy into a bound",
            "meaning": "the proxy lacks M_eff_ref, N_M, shell measure, and arena units",
            "claim_status": "nonclaim_proxy_only",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D741_3_next_tau_owner",
            "decision": "hunt observed tau owner next",
            "meaning": "without tau ownership, C_q cannot be derived; if tau fails, use the free coefficient pack explicitly",
            "claim_status": "next_derivation_or_demotion_target",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def route_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "route_id": "RU741_0_allowed",
            "allowed_after_741": "say the clean Cqmu owner candidate is C_qnu=N_M tau_nu",
            "forbidden_after_741": "say Cqmu is parent-owned in current MTS",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "RU741_1_allowed",
            "allowed_after_741": "use compact-shell proxy only as a unit-map target",
            "forbidden_after_741": "score the proxy against Y5/PPN/R10 bounds",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "RU741_2_allowed",
            "allowed_after_741": "demote Cqmu to explicit free coefficient pack if tau ownership fails",
            "forbidden_after_741": "hide q_loc by choosing Cqmu after readout",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def summary_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "main_result": "Cqmu owner fork written; best route is C_qnu=N_M tau_nu but tau/N_M are not parent-owned; compact-shell unit map remains blocked",
            "hard_blocker": "observed tau ownership, N_M normalization, M_eff_ref, compact-shell conversion, and no-readout proof are missing",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def make_validation(
    sources: list[dict[str, Any]],
    owner_rows: list[dict[str, Any]],
    unit_rows: list[dict[str, Any]],
    free_rows: list[dict[str, Any]],
    y5_update: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    outputs: list[Path],
) -> list[dict[str, str]]:
    validation: list[dict[str, str]] = []
    validation.append({"check_id": "V741_0_source_paths_exist", "result": "pass" if all(row["exists"] == "true" for row in sources) else "fail", "detail": f"source_rows={len(sources)}"})
    validation.append({"check_id": "V741_1_source_needles_present", "result": "pass" if all(row["needle_check"] == "true" for row in sources) else "fail", "detail": "all source files contain expected evidence needles"})
    prior = read_csv_rows(RESIDUALS / "P8_Y5_BRR545_740_VALIDATION.csv")
    validation.append({"check_id": "V741_2_prior_740_clean", "result": "pass" if prior and all(row.get("result") == "pass" for row in prior) else "fail", "detail": "740 validation has no failures"})
    validation.append({"check_id": "V741_3_740_selected_741", "result": "pass" if text_contains(SOURCES["740_doc"]["path"], [OUTPUT_DOC.name]) else "fail", "detail": OUTPUT_DOC.name})
    validation.append({"check_id": "V741_4_owner_fork_complete", "result": "pass" if len(owner_rows) == 5 else "fail", "detail": f"owner_rows={len(owner_rows)}"})
    validation.append({"check_id": "V741_5_tau_route_conditional", "result": "pass" if any(row["candidate_owner"] == "C_qnu=N_M tau_nu" and row["current_result"].startswith("best_conditional") for row in owner_rows) else "fail", "detail": "C_qnu=N_M tau_nu kept conditional"})
    validation.append({"check_id": "V741_6_readout_mask_forbidden", "result": "pass" if any(row["current_result"] == "forbidden_as_derivation" for row in owner_rows) else "fail", "detail": "post-readout Cq mask rejected"})
    validation.append({"check_id": "V741_7_unit_map_not_executable", "result": "pass" if any(row["current_result"] == "source_backed_internal_proxy" for row in unit_rows) and all(row["valid_for_claim"] == "false" for row in unit_rows) else "fail", "detail": "compact proxy retained as nonclaim"})
    validation.append({"check_id": "V741_8_free_coeff_pack_queued", "result": "pass" if len(free_rows) == 4 and all(row["current_status"] == "template_only" for row in free_rows) else "fail", "detail": f"free_rows={len(free_rows)}"})
    validation.append({"check_id": "V741_9_Y5_rows_retained", "result": "pass" if {"Y5R741_9_q_loc_projection", "Y5R741_5_extra_mass_projection"}.issubset({row["runner_id"] for row in y5_update}) else "fail", "detail": "q_loc and extra mass rows retained"})
    all_rows = owner_rows + unit_rows + free_rows + y5_update + decisions
    validation.append({"check_id": "V741_10_no_claim_rows_promoted", "result": "pass" if all(row.get("valid_for_claim") == "false" for row in all_rows) else "fail", "detail": "all generated rows valid_for_claim=false"})
    validation.append({"check_id": "V741_11_next_target_selected", "result": "pass" if all(row.get("next_target") == NEXT_TARGET for row in decisions) else "fail", "detail": NEXT_TARGET})
    validation.append({"check_id": "V741_12_outputs_scoped", "result": "pass" if all(under_post(path) for path in outputs) else "fail", "detail": "all outputs under post-checkpoint-work"})
    changed = formalization_changed_after_cutoff()
    validation.append({"check_id": "V741_13_formalization_workbench_untouched", "result": "pass" if changed == 0 else "fail", "detail": f"formalization_changed_after_cutoff={changed}"})
    validation.append({"check_id": "V741_14_no_local_arena_claim", "result": "pass" if "no_R10_PPN_Newton_or_local_GR_pass" in CLAIM_CEILING else "fail", "detail": "R10/PPN/Newton/local-GR claims remain blocked"})
    validation.append({"check_id": "V741_15_validation_rows_ready", "result": "pass", "detail": "validation table constructed"})
    return validation


def build_doc(
    sources: list[dict[str, Any]],
    owner_rows: list[dict[str, Any]],
    unit_rows: list[dict[str, Any]],
    free_rows: list[dict[str, Any]],
    y5_update: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    summary: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    text = f"""# 741 - Y5 R10 Cqmu Parent Owner Or Compact-Shell Unit Map

Start point: 740 made the `q_loc` source-mass channel explicit:

```text
I_q[A] = int_A C_qmu q_loc^mu
```

Current verdict: **the cleanest `C_qmu` route is `C_qmu=N_M tau_mu`, but current MTS has not parent-owned `tau_mu` or `N_M`**. The compact-shell proxy stays useful but nonclaim.

## Summary

| Field | Value |
| --- | --- |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Main result | Cqmu owner fork plus blocked compact-shell unit map |
| Next target | `{NEXT_TARGET}` |

## Cqmu Owner Fork

{markdown_table(owner_rows, ["owner_id", "candidate_owner", "math_form", "would_solve", "current_result", "missing", "valid_for_claim"])}

## Compact-Shell Unit Map Gate

{markdown_table(unit_rows, ["unit_gate_id", "quantity", "formula", "needed_to_score", "current_result", "why_blocked", "valid_for_claim"])}

## Free Coefficient Pack Queue

{markdown_table(free_rows, ["queue_id", "target_row", "coefficient", "template_formula", "required_columns", "current_status", "acceptance_gate", "valid_for_claim"])}

## Y5 Runner Update

{markdown_table(y5_update, ["runner_id", "source_row", "status_after_741", "zero_or_input", "still_missing", "valid_for_claim"])}

## Decisions

{markdown_table(decisions, ["decision_id", "decision", "meaning", "claim_status", "next_target", "valid_for_claim"])}

## Route Update

{markdown_table(routes, ["route_id", "allowed_after_741", "forbidden_after_741", "next_action", "valid_for_claim"])}

## Nonclaim Summary

{markdown_table(summary, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim"])}

## Source Register

{markdown_table(sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}

## Plain-English Verdict

This pass found the right-looking coupling shape but not the right to use it yet. `C_qmu=N_M tau_mu` is exactly the kind of thing we want because it would tie `q_loc` to the same mass generator as the source measure. But the missing object is now brutally specific: parent-own the observed `tau`, fix `N_M`, and prove it is not chosen after orbital readout. If that fails, the honest route is a free coefficient pack. Annoying? Yes. Useful? Also yes. The goblin now has a name badge.
"""
    OUTPUT_DOC.write_text(text, encoding="utf-8")


def main() -> None:
    generated_utc = utc_stamp()
    sources = make_source_register(generated_utc)
    owner = owner_fork_rows(generated_utc)
    unit = unit_map_rows(generated_utc)
    free = free_coeff_rows(generated_utc)
    y5_update = y5_rows(generated_utc)
    decisions = decision_rows(generated_utc)
    routes = route_rows(generated_utc)
    summary = summary_rows(generated_utc)
    outputs = [
        OUTPUT_DOC,
        SOURCE_REGISTER_PATH,
        OWNER_FORK_PATH,
        UNIT_MAP_PATH,
        FREE_COEFF_PATH,
        Y5_UPDATE_PATH,
        DECISION_PATH,
        ROUTE_PATH,
        SUMMARY_PATH,
        VALIDATION_PATH,
    ]
    validation = make_validation(sources, owner, unit, free, y5_update, decisions, outputs)

    write_csv(SOURCE_REGISTER_PATH, sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(OWNER_FORK_PATH, owner, ["owner_id", "candidate_owner", "math_form", "would_solve", "current_result", "missing", "valid_for_claim", "generated_utc"])
    write_csv(UNIT_MAP_PATH, unit, ["unit_gate_id", "quantity", "formula", "needed_to_score", "current_result", "why_blocked", "valid_for_claim", "generated_utc"])
    write_csv(FREE_COEFF_PATH, free, ["queue_id", "target_row", "coefficient", "template_formula", "required_columns", "current_status", "acceptance_gate", "valid_for_claim", "generated_utc"])
    write_csv(Y5_UPDATE_PATH, y5_update, ["runner_id", "source_row", "status_after_741", "zero_or_input", "still_missing", "valid_for_claim", "generated_utc"])
    write_csv(DECISION_PATH, decisions, ["decision_id", "decision", "meaning", "claim_status", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(ROUTE_PATH, routes, ["route_id", "allowed_after_741", "forbidden_after_741", "next_action", "valid_for_claim", "generated_utc"])
    write_csv(SUMMARY_PATH, summary, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])
    build_doc(sources, owner, unit, free, y5_update, decisions, routes, summary, validation)

    print(
        json.dumps(
            {
                "generated_utc": generated_utc,
                "status": STATUS,
                "claim_ceiling": CLAIM_CEILING,
                "next_target": NEXT_TARGET,
                "doc": str(OUTPUT_DOC),
                "validation": str(VALIDATION_PATH),
                "all_validation_pass": all(row["result"] == "pass" for row in validation),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
