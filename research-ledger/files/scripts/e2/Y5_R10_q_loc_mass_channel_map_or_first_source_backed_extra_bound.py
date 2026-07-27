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

OUTPUT_DOC = POST_CHECKPOINT / "740-Y5-R10-q_loc-mass-channel-map-or-first-source-backed-extra-bound.md"
NEXT_TARGET = "741-Y5-R10-Cqmu-parent-owner-or-compact-shell-unit-map.md"
STATUS = "Y5_R10_740_q_loc_mass_channel_identity_written_Cqmu_owner_missing_compact_proxy_nonclaim"
CLAIM_CEILING = "q_loc_mass_channel_map_and_nonclaim_proxy_only_no_Cqmu_owner_no_mu_extra_zero_no_R10_PPN_Newton_or_local_GR_pass"

SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_740_SOURCE_REGISTER.csv"
MASS_MAP_PATH = RESIDUALS / "P8_Y5_R10_740_QLOC_MASS_CHANNEL_MAP.csv"
SILENCE_GATE_PATH = RESIDUALS / "P8_Y5_R10_740_CQMU_SILENCE_GATE.csv"
BOUND_ATTEMPT_PATH = RESIDUALS / "P8_Y5_R10_740_FIRST_QLOC_BOUND_ATTEMPT.csv"
OBSERVABLE_MAP_PATH = RESIDUALS / "P8_Y5_R10_740_QLOC_OBSERVABLE_TRANSFER_MAP.csv"
Y5_UPDATE_PATH = RESIDUALS / "P8_Y5_R10_740_Y5_RUNNER_UPDATE.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_R10_740_DECISION_MATRIX.csv"
ROUTE_PATH = RESIDUALS / "P8_Y5_R10_740_ROUTE_UPDATE.csv"
SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_740_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_740_VALIDATION.csv"

FORMALIZATION_CUTOFF = datetime(2026, 5, 31, 14, 42, 0)


SOURCES: dict[str, dict[str, Any]] = {
    "739_doc": {
        "path": POST_CHECKPOINT / "739-Y5-R10-extra-mass-projection-silence-or-channelwise-bound.md",
        "needles": [OUTPUT_DOC.name, "EX739_4_q_loc_mass_projection", "C_qmu"],
        "role": "handoff selecting q_loc mass projection",
    },
    "739_validation": {
        "path": RESIDUALS / "P8_Y5_BRR545_739_VALIDATION.csv",
        "needles": ["V739_13_next_target_selected", "V739_15_formalization_workbench_untouched", "V739_16_no_local_arena_claim"],
        "role": "prior validation guard",
    },
    "739_channel_ledger": {
        "path": RESIDUALS / "P8_Y5_R10_739_CHANNELWISE_PROJECTION_LEDGER.csv",
        "needles": ["EX739_4_q_loc_mass_projection", "I_q=int_A C_qmu q_loc^mu", "open_observed_q_loc_not_zero_C_qmu_missing"],
        "role": "q_loc channel row",
    },
    "739_bound_queue": {
        "path": RESIDUALS / "P8_Y5_R10_739_CHANNEL_BOUND_INPUT_QUEUE.csv",
        "needles": ["CBI739_4_q_loc_mass_projection", "C_qmu;q_loc_profile;units", "no_cancellation_flag"],
        "role": "q_loc bound input schema",
    },
    "734_runner": {
        "path": RESIDUALS / "P8_Y5_R10_734_HYBRID_QLOC_RESIDUAL_RUNNER_FILLED.csv",
        "needles": ["HQR734_1_source_normalization_Y5", "C_qmu", "7.432631961576971e-06"],
        "role": "filled q_loc runner and compact proxy",
    },
    "734_formula": {
        "path": RESIDUALS / "P8_Y5_R10_734_RESIDUAL_FORMULA_LEDGER.csv",
        "needles": ["RFL734_0_reduced_Ward_shape", "q_loc^nu = P_loc", "RFL734_2_observed_residual_survives"],
        "role": "q_loc reduced Ward formula and observed residual survival",
    },
    "733_ward_gate": {
        "path": RESIDUALS / "P8_Y5_R10_733_WARD_ZERO_GATE.csv",
        "needles": ["WZG733_0_current_symbol_match", "WZG733_5_Y5_source_normalization", "boundary_no_flux"],
        "role": "exact q_loc zero blockers",
    },
    "513_doc": {
        "path": POST_CHECKPOINT / "513-Gamma-Khat-q_loc-first-variation-or-demotion.md",
        "needles": ["T_GK^{mu nu} := Gamma_eff g^{mu nu} - K_hat^{mu nu}", "q_loc^nu = P_loc nabla_mu T_GK^{mu nu}", "conditional_variational_stress_route_only"],
        "role": "stress-divergence identity source",
    },
    "qloc_bound_spec": {
        "path": RESIDUALS / "P8_QLOC_BOUND_RUNNER_SPEC.csv",
        "needles": ["QB516_0_compact_shell_budget", "7.432631961576971e-06", "QB516_2_Gdot_GMdot"],
        "role": "q_loc fallback bound spec",
    },
    "y5_bound_input": {
        "path": RESIDUALS / "P8_Y5_SOURCE_NORMALIZATION_BOUND_RUNNER_INPUT.csv",
        "needles": ["Y5B_9_q_loc_projection", "C_qmu q_loc", "mixed_until_projection_fixed"],
        "role": "Y5 q_loc source-normalization row",
    },
    "737_input_queue": {
        "path": RESIDUALS / "P8_Y5_R10_737_SOURCE_BACKED_INPUT_QUEUE.csv",
        "needles": ["IN737_5_C_qmu_projection", "q_loc", "source-normalization/PPN units"],
        "role": "missing C_qmu projection source queue",
    },
    "513_residual_demotion": {
        "path": RESIDUALS / "P8_GAMMA_KHAT_QLOC_RESIDUAL_OR_DEMOTION.csv",
        "needles": ["QR513_0_nonvariational_stress", "QR513_3_projector_unowned", "QR513_4_boundary_flux"],
        "role": "q_loc residual demotion blockers",
    },
    "local_prediction_template": {
        "path": RESIDUALS / "MTS_local_residual_predictions_TEMPLATE.csv",
        "needles": ["R7_alpha3", "unowned q_loc^nu", "R10_fifth_force"],
        "role": "local observable row locks for q_loc leakage",
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


def source_register(generated_utc: str) -> list[dict[str, Any]]:
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


def mass_map_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "map_id": "QMM740_0_define_mass_channel",
            "quantity": "I_q[A]",
            "formula": "I_q[A]=int_A C_{q nu} q_loc^nu dV = int_A C_{q nu} P_loc nabla_mu T_GK^{mu nu} dV",
            "derivation": "insert q_loc^nu=P_loc nabla_mu T_GK^{mu nu} from the stress-divergence identity",
            "current_status": "identity_written",
            "missing_for_claim": "parent-owned C_qnu, units, source-normalization frame, and arena transfer map",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "map_id": "QMM740_1_integrate_by_parts",
            "quantity": "I_q[A]",
            "formula": "I_q[A]=int_partialA C_{q nu} P_loc T_GK^{mu nu} n_mu dS - int_A T_GK^{mu nu} nabla_mu(C_q P_loc)_nu dV + Euler/source terms",
            "derivation": "apply the covariant product rule to C_q P_loc T_GK and keep boundary plus projector/coefficient-gradient terms",
            "current_status": "derived_identity_not_zero",
            "missing_for_claim": "boundary flux zero, covariantly constant C_q P_loc, and on-shell source-free reduced fields",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "map_id": "QMM740_2_killing_mass_projection",
            "quantity": "C_qnu",
            "formula": "C_{q nu}=N_M tau_nu only if tau is the observed parent-owned mass generator and N_M fixes GM/source units",
            "derivation": "mass projection must contract q_loc with the same stationary/Hamiltonian generator used for source measure",
            "current_status": "candidate_owner_not_current_derived",
            "missing_for_claim": "observed tau ownership, normalization N_M, and proof that C_q is not chosen after readout",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "map_id": "QMM740_3_transverse_silence_option",
            "quantity": "C_qnu q_loc^nu",
            "formula": "C_qnu q_loc^nu=0 if q_loc^nu is purely transverse to tau_nu and C_qnu=N_M tau_nu",
            "derivation": "orthogonality to the mass generator would remove source-normalization leakage while leaving spatial/PPN channels separate",
            "current_status": "conditional_zero_not_current_derived",
            "missing_for_claim": "tau-orthogonality theorem for observed q_loc, not merely representative-vertical blindness",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "map_id": "QMM740_4_bound_fallback",
            "quantity": "epsilon_q_loc",
            "formula": "epsilon_q_loc = |I_q[A]|/M_eff_ref <= bound_arena",
            "derivation": "if silence fails, q_loc enters the no-cancellation extra-mass envelope as a separately bounded channel",
            "current_status": "fallback_ready_not_scored",
            "missing_for_claim": "M_eff_ref, units, q_loc profile, C_q normalization, source file, and arena bound row",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def silence_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "CQG740_0_exact_q_loc_zero",
            "needed_condition": "observed q_loc^nu=0",
            "math_form": "P_loc(sum_A E_A nabla^nu Phi_A + B_boundary^nu)=0",
            "current_result": "not_derived",
            "why": "current Gamma/Khat owner, source-free Euler equations, P_loc ownership, Y5/Y6, and boundary no-flux remain open",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "CQG740_1_mass_generator_orthogonality",
            "needed_condition": "tau_nu q_loc^nu=0",
            "math_form": "C_qnu=N_M tau_nu and tau.q_loc=0 => C_qnu q_loc^nu=0",
            "current_result": "conditional_zero_only",
            "why": "no parent theorem proves observed q_loc is transverse to the mass generator",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "CQG740_2_covariantly_constant_projection",
            "needed_condition": "nabla_mu(C_q P_loc)_nu=0 on compact local exterior",
            "math_form": "bulk term in integration-by-parts identity vanishes",
            "current_result": "open",
            "why": "C_q and P_loc are not parent-owned or unit-normalized for the current chain",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "CQG740_3_boundary_flux_silence",
            "needed_condition": "int_partialA C_qnu P_loc T_GK^{mu nu} n_mu dS=0",
            "math_form": "boundary contribution from q_loc source channel vanishes",
            "current_result": "open",
            "why": "proper representative boundary zeros do not kill observed reduced boundary/source-measure flux",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "CQG740_4_units_and_no_readout",
            "needed_condition": "C_q converts q_loc to Y5/R10/PPN units before empirical readout",
            "math_form": "C_q is a parent/source-normalization map, not a fitted post-readout mask",
            "current_result": "missing",
            "why": "Y5B_9 remains mixed_until_projection_fixed",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def bound_attempt_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "bound_id": "QBA740_0_compact_shell_proxy",
            "quantity": "max_abs_Ploc_drelJrel_proxy",
            "value": "7.432631961576971e-06",
            "units": "dimensionless_proxy",
            "source": str(RESIDUALS / "P8_QLOC_BOUND_RUNNER_SPEC.csv") + "; " + str(RESIDUALS / "P8_Y5_R10_734_HYBRID_QLOC_RESIDUAL_RUNNER_FILLED.csv"),
            "status": "source_backed_proxy_not_arena_bound",
            "why_not_claimable": "not mapped through C_qmu into Y5/PPN/R10 units and not compared to an arena bound",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "bound_id": "QBA740_1_Y5_mass_projection",
            "quantity": "epsilon_q_loc_Y5",
            "value": "unfilled",
            "units": "mixed_until_projection_fixed",
            "source": str(RESIDUALS / "P8_Y5_SOURCE_NORMALIZATION_BOUND_RUNNER_INPUT.csv"),
            "status": "blocked_Cqmu_missing",
            "why_not_claimable": "C_qmu, q_loc profile, units, and M_eff_ref are not supplied",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "bound_id": "QBA740_2_alpha3_pressure_projection",
            "quantity": "alpha3_equivalent_q_loc",
            "value": "unfilled",
            "units": "dimensionless",
            "source": str(RESIDUALS / "P8_QLOC_BOUND_RUNNER_SPEC.csv"),
            "status": "blocked_projection_coefficient_missing",
            "why_not_claimable": "alpha3 row is ultratight and needs a sourced q_loc-to-momentum-flux coefficient",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "bound_id": "QBA740_3_R10_range_projection",
            "quantity": "alpha_q_loc(lambda)",
            "value": "unfilled",
            "units": "dimensionless_plus_range",
            "source": str(RESIDUALS / "P8_Y5_R10_739_CHANNEL_BOUND_INPUT_QUEUE.csv"),
            "status": "blocked_range_map_missing",
            "why_not_claimable": "lambda, alpha coefficient, source path, and bound-curve comparison are absent",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def observable_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "observable_id": "QOT740_0_Y5_source_strength",
            "target_row": "Y5B_9_q_loc_projection",
            "transfer": "epsilon_q_loc=|int_A C_qmu q_loc^mu|/M_eff_ref",
            "needed_inputs": "C_qmu;M_eff_ref;q_loc_profile;units;source_file;no_cancellation_flag",
            "current_status": "not_executable",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "observable_id": "QOT740_1_Gdot_Mdot",
            "target_row": "Y5B_0/Y5B_1",
            "transfer": "dln_mu_obs_dt contains time projection of C_qmu q_loc^mu if q_loc has tau component",
            "needed_inputs": "observed tau;time window;C_qtau;Gdot/Mdot unit map",
            "current_status": "not_executable",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "observable_id": "QOT740_2_radial_hair",
            "target_row": "Y5B_2",
            "transfer": "partial_r ln mu_obs sourced by shell difference of I_q[A(r1,r2)]",
            "needed_inputs": "radial shell profile;M_eff_ref;r1;r2;normalization",
            "current_status": "not_executable",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "observable_id": "QOT740_3_PPN_vector",
            "target_row": "Y5B_8/R3-R8",
            "transfer": "linearized metric Green operator maps q_loc/source-normalization leakage into Delta_PPN_source",
            "needed_inputs": "weak-field Green operator;gauge;component split;official PPN row map",
            "current_status": "not_executable",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "observable_id": "QOT740_4_R10_range",
            "target_row": "R10_fifth_force",
            "transfer": "range-dependent q_loc kernel maps to alpha(lambda)",
            "needed_inputs": "lambda;alpha coefficient;source-normalization;real bound curve row",
            "current_status": "not_executable",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def y5_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "runner_id": "Y5R740_5_extra_mass_projection",
            "source_row": "Y5B_5_extra_mass_projection",
            "status_after_740": "q_loc_channel_split_but_not_zero_or_bounded",
            "zero_or_input": "q_loc channel now has I_q=int_A C_qmu q_loc^mu and integration-by-parts identity",
            "still_missing": "C_qmu owner, units, boundary silence, covariant projection, and arena transfer map",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "runner_id": "Y5R740_9_q_loc_projection",
            "source_row": "Y5B_9_q_loc_projection",
            "status_after_740": "Cqmu_owner_missing_compact_proxy_nonclaim",
            "zero_or_input": "compact-shell proxy sourced but not an arena-bound row",
            "still_missing": "parent C_qmu, M_eff_ref, q_loc profile, unit map, no-readout proof",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "runner_id": "Y5R740_8_full_PPN_source_vector",
            "source_row": "Y5B_8_full_PPN_source_vector",
            "status_after_740": "PPN_transfer_map_named_not_filled",
            "zero_or_input": "q_loc spatial/vector/STF pieces require weak-field Green operator before PPN scoring",
            "still_missing": "gauge, Green operator, component split, official PPN coefficients",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "D740_0_identity_success",
            "decision": "accept q_loc mass-channel integration identity",
            "meaning": "the q_loc source-mass channel is now a concrete contraction/integration problem, not a loose phrase",
            "claim_status": "map_only",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D740_1_zero_rejected",
            "decision": "do not claim C_qmu q_loc=0",
            "meaning": "exact q_loc zero, tau-orthogonality, boundary silence, and C_q parent ownership remain open",
            "claim_status": "blocked_for_current_claim",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D740_2_proxy_not_bound",
            "decision": "do not score compact-shell proxy",
            "meaning": "7.4326e-06 is sourced as an internal proxy but lacks C_qmu units and arena comparison",
            "claim_status": "nonclaim_proxy_only",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D740_3_next_Cqmu_owner",
            "decision": "try to derive parent C_qmu owner and compact-shell unit map next",
            "meaning": "without C_qmu ownership, no q_loc bound can be safely compared to Y5/PPN/R10 rows",
            "claim_status": "next_derivation_target",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def route_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "route_id": "RU740_0_allowed",
            "allowed_after_740": "say q_loc mass-channel identity and integration-by-parts map are written",
            "forbidden_after_740": "say q_loc mass projection is zero or locally bounded",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "RU740_1_allowed",
            "allowed_after_740": "use compact-shell value as a nonclaim proxy needing unit map",
            "forbidden_after_740": "compare the proxy directly to PPN/R10/Y5 bounds",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "RU740_2_allowed",
            "allowed_after_740": "derive C_qmu from parent mass generator/tau or demote it to an explicit free coefficient",
            "forbidden_after_740": "choose C_qmu after orbital readout to hide q_loc",
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
            "main_result": "q_loc mass-channel identity and integration-by-parts silence gates written; compact-shell proxy recorded as nonclaim",
            "hard_blocker": "C_qmu owner/unit map is missing, exact observed q_loc zero is not derived, and the proxy cannot yet be compared to local bounds",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def make_validation(
    sources: list[dict[str, Any]],
    mass_rows: list[dict[str, Any]],
    silence: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    observables: list[dict[str, Any]],
    y5_update: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    outputs: list[Path],
) -> list[dict[str, str]]:
    validation: list[dict[str, str]] = []
    validation.append({"check_id": "V740_0_source_paths_exist", "result": "pass" if all(row["exists"] == "true" for row in sources) else "fail", "detail": f"source_rows={len(sources)}"})
    validation.append({"check_id": "V740_1_source_needles_present", "result": "pass" if all(row["needle_check"] == "true" for row in sources) else "fail", "detail": "all source files contain expected evidence needles"})
    prior = read_csv_rows(RESIDUALS / "P8_Y5_BRR545_739_VALIDATION.csv")
    validation.append({"check_id": "V740_2_prior_739_clean", "result": "pass" if prior and all(row.get("result") == "pass" for row in prior) else "fail", "detail": "739 validation has no failures"})
    validation.append({"check_id": "V740_3_739_selected_740", "result": "pass" if text_contains(SOURCES["739_doc"]["path"], [OUTPUT_DOC.name]) else "fail", "detail": OUTPUT_DOC.name})
    validation.append({"check_id": "V740_4_mass_identity_written", "result": "pass" if any("int_A C_{q nu}" in row["formula"] for row in mass_rows) else "fail", "detail": f"mass_rows={len(mass_rows)}"})
    validation.append({"check_id": "V740_5_integration_by_parts_retained", "result": "pass" if any("int_partialA" in row["formula"] and "nabla_mu(C_q P_loc)" in row["formula"] for row in mass_rows) else "fail", "detail": "boundary and coefficient-gradient terms retained"})
    validation.append({"check_id": "V740_6_Cqmu_zero_not_promoted", "result": "pass" if all(row["valid_for_claim"] == "false" for row in silence) and any(row["current_result"] == "not_derived" for row in silence) else "fail", "detail": "C_qmu q_loc zero not claimed"})
    validation.append({"check_id": "V740_7_compact_proxy_nonclaim", "result": "pass" if any(row["status"] == "source_backed_proxy_not_arena_bound" and row["valid_for_claim"] == "false" for row in bounds) else "fail", "detail": "compact-shell proxy recorded but not scored"})
    validation.append({"check_id": "V740_8_no_source_backed_bound_claim", "result": "pass" if all(row["valid_for_claim"] == "false" for row in bounds) else "fail", "detail": "no q_loc bound row valid_for_claim=true"})
    validation.append({"check_id": "V740_9_observable_maps_unfilled", "result": "pass" if all(row["current_status"] == "not_executable" for row in observables) else "fail", "detail": f"observable_rows={len(observables)}"})
    validation.append({"check_id": "V740_10_Y5_rows_retained", "result": "pass" if {"Y5R740_5_extra_mass_projection", "Y5R740_9_q_loc_projection"}.issubset({row["runner_id"] for row in y5_update}) else "fail", "detail": "extra mass and q_loc Y5 rows retained"})
    all_generated = mass_rows + silence + bounds + observables + y5_update + decisions
    validation.append({"check_id": "V740_11_no_claim_rows_promoted", "result": "pass" if all(row.get("valid_for_claim") == "false" for row in all_generated) else "fail", "detail": "all generated rows valid_for_claim=false"})
    validation.append({"check_id": "V740_12_next_target_selected", "result": "pass" if all(row.get("next_target") == NEXT_TARGET for row in decisions) else "fail", "detail": NEXT_TARGET})
    validation.append({"check_id": "V740_13_outputs_scoped", "result": "pass" if all(under_post(path) for path in outputs) else "fail", "detail": "all outputs under post-checkpoint-work"})
    changed = formalization_changed_after_cutoff()
    validation.append({"check_id": "V740_14_formalization_workbench_untouched", "result": "pass" if changed == 0 else "fail", "detail": f"formalization_changed_after_cutoff={changed}"})
    validation.append({"check_id": "V740_15_no_local_arena_claim", "result": "pass" if "no_R10_PPN_Newton_or_local_GR_pass" in CLAIM_CEILING else "fail", "detail": "R10/PPN/Newton/local-GR claims remain blocked"})
    validation.append({"check_id": "V740_16_validation_rows_ready", "result": "pass", "detail": "validation table constructed"})
    return validation


def build_doc(
    sources: list[dict[str, Any]],
    mass_rows: list[dict[str, Any]],
    silence: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    observables: list[dict[str, Any]],
    y5_update: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    summary: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    text = f"""# 740 - Y5 R10 q_loc Mass-Channel Map Or First Source-Backed Extra Bound

Start point: 739 isolated `q_loc` as the most dangerous extra-mass channel:

```text
I_q[A] = int_A C_qmu q_loc^mu
```

Current verdict: **the q_loc mass-channel identity is now explicit, but `C_qmu` is not parent-owned or unit-normalized**. The old compact-shell number is source-backed as an internal proxy, but it is not a claim-ready local bound.

## Summary

| Field | Value |
| --- | --- |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Main result | q_loc mass-channel map plus nonclaim compact proxy |
| Next target | `{NEXT_TARGET}` |

## q_loc Mass-Channel Map

{markdown_table(mass_rows, ["map_id", "quantity", "formula", "derivation", "current_status", "missing_for_claim", "valid_for_claim"])}

## C_qmu Silence Gate

{markdown_table(silence, ["gate_id", "needed_condition", "math_form", "current_result", "why", "next_action", "valid_for_claim"])}

## First Bound Attempt

{markdown_table(bounds, ["bound_id", "quantity", "value", "units", "source", "status", "why_not_claimable", "valid_for_claim"])}

## Observable Transfer Map

{markdown_table(observables, ["observable_id", "target_row", "transfer", "needed_inputs", "current_status", "valid_for_claim"])}

## Y5 Runner Update

{markdown_table(y5_update, ["runner_id", "source_row", "status_after_740", "zero_or_input", "still_missing", "valid_for_claim"])}

## Decisions

{markdown_table(decisions, ["decision_id", "decision", "meaning", "claim_status", "next_target", "valid_for_claim"])}

## Route Update

{markdown_table(routes, ["route_id", "allowed_after_740", "forbidden_after_740", "next_action", "valid_for_claim"])}

## Nonclaim Summary

{markdown_table(summary, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim"])}

## Source Register

{markdown_table(sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}

## Plain-English Verdict

This is an honest little gearbox step. We did not prove `q_loc` is harmless, but we have stopped treating it like a ghost. It now has to enter through a specific contraction `C_qmu q_loc^mu`, and that contraction has to be owned before readout, normalized into source-mass units, and then either killed or compared to a real local arena. The compact-shell value is useful as a breadcrumb, not a trophy. Next up is `C_qmu`: derive it from the parent mass generator, or demote it to a free coefficient with a unit map.
"""
    OUTPUT_DOC.write_text(text, encoding="utf-8")


def main() -> None:
    generated_utc = utc_stamp()
    sources = source_register(generated_utc)
    mass = mass_map_rows(generated_utc)
    silence = silence_rows(generated_utc)
    bounds = bound_attempt_rows(generated_utc)
    observables = observable_rows(generated_utc)
    y5_update = y5_rows(generated_utc)
    decisions = decision_rows(generated_utc)
    routes = route_rows(generated_utc)
    summary = summary_rows(generated_utc)
    outputs = [
        OUTPUT_DOC,
        SOURCE_REGISTER_PATH,
        MASS_MAP_PATH,
        SILENCE_GATE_PATH,
        BOUND_ATTEMPT_PATH,
        OBSERVABLE_MAP_PATH,
        Y5_UPDATE_PATH,
        DECISION_PATH,
        ROUTE_PATH,
        SUMMARY_PATH,
        VALIDATION_PATH,
    ]
    validation = make_validation(sources, mass, silence, bounds, observables, y5_update, decisions, outputs)

    write_csv(SOURCE_REGISTER_PATH, sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(MASS_MAP_PATH, mass, ["map_id", "quantity", "formula", "derivation", "current_status", "missing_for_claim", "valid_for_claim", "generated_utc"])
    write_csv(SILENCE_GATE_PATH, silence, ["gate_id", "needed_condition", "math_form", "current_result", "why", "next_action", "valid_for_claim", "generated_utc"])
    write_csv(BOUND_ATTEMPT_PATH, bounds, ["bound_id", "quantity", "value", "units", "source", "status", "why_not_claimable", "valid_for_claim", "generated_utc"])
    write_csv(OBSERVABLE_MAP_PATH, observables, ["observable_id", "target_row", "transfer", "needed_inputs", "current_status", "valid_for_claim", "generated_utc"])
    write_csv(Y5_UPDATE_PATH, y5_update, ["runner_id", "source_row", "status_after_740", "zero_or_input", "still_missing", "valid_for_claim", "generated_utc"])
    write_csv(DECISION_PATH, decisions, ["decision_id", "decision", "meaning", "claim_status", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(ROUTE_PATH, routes, ["route_id", "allowed_after_740", "forbidden_after_740", "next_action", "valid_for_claim", "generated_utc"])
    write_csv(SUMMARY_PATH, summary, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])
    build_doc(sources, mass, silence, bounds, observables, y5_update, decisions, routes, summary, validation)

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
