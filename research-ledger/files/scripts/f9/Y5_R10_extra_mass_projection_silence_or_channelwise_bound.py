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

CHECKPOINT = "739"
OUTPUT_DOC = POST_CHECKPOINT / "739-Y5-R10-extra-mass-projection-silence-or-channelwise-bound.md"
NEXT_TARGET = "740-Y5-R10-q_loc-mass-channel-map-or-first-source-backed-extra-bound.md"
STATUS = "Y5_R10_739_extra_mass_silence_attempt_failed_channelwise_projection_bound_queue_written"
CLAIM_CEILING = "extra_mass_projection_silence_failed_for_current_chain_channelwise_bounds_only_no_mu_extra_zero_Newton_PPN_R10_or_local_GR_pass"

SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_739_SOURCE_REGISTER.csv"
SILENCE_ATTEMPT_PATH = RESIDUALS / "P8_Y5_R10_739_EXTRA_MASS_SILENCE_ATTEMPT.csv"
CHANNEL_LEDGER_PATH = RESIDUALS / "P8_Y5_R10_739_CHANNELWISE_PROJECTION_LEDGER.csv"
BOUND_QUEUE_PATH = RESIDUALS / "P8_Y5_R10_739_CHANNEL_BOUND_INPUT_QUEUE.csv"
Y5_UPDATE_PATH = RESIDUALS / "P8_Y5_R10_739_Y5_RUNNER_UPDATE.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_R10_739_DECISION_MATRIX.csv"
ROUTE_PATH = RESIDUALS / "P8_Y5_R10_739_ROUTE_UPDATE.csv"
SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_739_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_739_VALIDATION.csv"

FORMALIZATION_CUTOFF = datetime(2026, 5, 31, 14, 42, 0)


SOURCES: dict[str, dict[str, Any]] = {
    "738_doc": {
        "path": POST_CHECKPOINT / "738-Y5-R10-PiM-projector-owner-or-radial-bound-runner.md",
        "needles": [OUTPUT_DOC.name, "Y5R738_5_extra_mass_projection", "boundary/domain/memory/non-EH/q_loc mass-channel exchange vector"],
        "role": "immediate PiM handoff selecting extra-mass projection silence",
    },
    "738_validation": {
        "path": RESIDUALS / "P8_Y5_BRR545_738_VALIDATION.csv",
        "needles": ["V738_13_next_target_selected", "V738_15_formalization_workbench_untouched", "V738_16_no_local_arena_claim"],
        "role": "prior validation guard",
    },
    "old_522_doc": {
        "path": POST_CHECKPOINT / "522-Y5-extra-mass-projection-silence-or-channelwise-bound.md",
        "needles": ["Pi_M dJ_extra = 0", "channel-by-channel", "Current MTS has not derived zero projection"],
        "role": "earlier extra-mass projection theorem target",
    },
    "source_measure_clauses": {
        "path": RESIDUALS / "P8_SOURCE_MEASURE_MEFF_FLUX_CLAUSES.csv",
        "needles": ["SM509_5_no_extra_channel", "Delta_nonEH", "SM509_6_Gauss_orbital_calibration"],
        "role": "source-measure no-extra-channel contract",
    },
    "mu_extra_owner": {
        "path": RESIDUALS / "P8_MU_EXTRA_CHANNEL_OWNER_LEDGER.csv",
        "needles": ["bulk_X_Yukawa_tail", "domain_projector_mass", "absolute_calibration_offset"],
        "role": "existing mu_extra channel ownership ledger",
    },
    "mu_extra_bound_summary": {
        "path": RESIDUALS / "P8_MU_EXTRA_CHANNEL_BOUND_SUMMARY.csv",
        "needles": ["epsilon_bulk_X", "R10_fifth_force", "epsilon_species_A"],
        "role": "existing local-bound target map for mu_extra channels",
    },
    "mu_extra_coefficients": {
        "path": RESIDUALS / "P8_MU_EXTRA_SOURCE_NORMALIZATION_COEFFICIENT_VECTOR.csv",
        "needles": ["MISSING_DERIVED_ZERO_OR_NUMERIC_COEFFICIENT", "epsilon_radial_Meff", "epsilon_calibration"],
        "role": "current coefficient vector showing no claim-ready channel rows",
    },
    "extra_energy_identity": {
        "path": RESIDUALS / "P8_EXTRA_SECTOR_SILENCE_ENERGY_IDENTITY.csv",
        "needles": ["E506_scalar_positive_operator", "memory response", "boundary_flux"],
        "role": "positive-operator/nohair route for extra sectors",
    },
    "737_obstruction": {
        "path": RESIDUALS / "P8_Y5_R10_737_PROJECTED_MASS_FLUX_OBSTRUCTION.csv",
        "needles": ["PMF737_3_extra_exchange_projection", "C_qmu q_loc", "PMF737_5_calibration_not_closure"],
        "role": "projected mass-flux obstruction including q_loc exchange",
    },
    "737_input_queue": {
        "path": RESIDUALS / "P8_Y5_R10_737_SOURCE_BACKED_INPUT_QUEUE.csv",
        "needles": ["IN737_3_mu_extra_exchange_vector", "IN737_5_C_qmu_projection", "q_loc"],
        "role": "missing input queue for exchange vector and C_qmu",
    },
    "734_zero_attempt": {
        "path": RESIDUALS / "P8_Y5_R10_734_FIRST_ZERO_ATTEMPT.csv",
        "needles": ["FZA734_2_exact_observed_q_loc_zero", "not_derived_for_current_claim", "Observed q_loc"],
        "role": "q_loc exact-zero rejection and residual survival",
    },
    "736_zero_attempt": {
        "path": RESIDUALS / "P8_Y5_R10_736_THIRD_ZERO_ATTEMPT.csv",
        "needles": ["TZA736_0_direct_representative_matter_marker", "TZA736_4_full_Y5_source_normalization_zero", "q_loc"],
        "role": "no-marker partial zero and full Y5 blocker",
    },
    "738_radial_queue": {
        "path": RESIDUALS / "P8_Y5_R10_738_RADIAL_BOUND_INPUT_QUEUE.csv",
        "needles": ["RBI738_4_radial_decision", "dJ_extra", "I_commutator"],
        "role": "radial formula that now receives channelwise extra-mass rows",
    },
}


def utc_stamp() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def text_contains(path: Path, needles: list[str]) -> bool:
    haystack = read_text(path)
    return bool(haystack) and all(needle in haystack for needle in needles)


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
    text = "" if value is None else str(value)
    return text.replace("|", "\\|").replace("\n", "<br>")


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    body = [
        "| " + " | ".join(markdown_cell(row.get(column, "")) for column in columns) + " |"
        for row in rows
    ]
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


def build_silence_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "attempt_id": "ESA739_0_split_identity",
            "target": "J_extra",
            "math_form": "J_extra=J_boundary+J_domain+J_memory+J_nonEH+J_q_loc+J_PiM+J_coupling+J_frame_species+J_anomaly+J_calibration",
            "zero_route": "prove Pi_M dJ_i=0 for every channel, before cancellation or fitting",
            "current_result": "decomposition_written_not_zero",
            "blocker": "several channels are retained from prior ledgers and q_loc observed residual is still alive",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "attempt_id": "ESA739_1_projection_sum_rule",
            "target": "I_extra[A]",
            "math_form": "I_extra[A]=int_A Pi_M dJ_extra=sum_i int_A Pi_M dJ_i",
            "zero_route": "each summand is theorem-zero or source-backed below local bound",
            "current_result": "identity_written_not_scored",
            "blocker": "no channel has claim-ready numeric coefficient and no all-channel theorem exists",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "attempt_id": "ESA739_2_no_cancellation_norm",
            "target": "epsilon_extra",
            "math_form": "|epsilon_extra| <= sum_i |epsilon_i|; tuned cancellation is not evidence",
            "zero_route": "bound every absolute channel contribution independently",
            "current_result": "policy_gate_active",
            "blocker": "prevents hiding an open q_loc/boundary/projector channel behind another open channel",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "attempt_id": "ESA739_3_conditional_silence_theorem",
            "target": "Pi_M dJ_extra",
            "math_form": "forall i: Pi_M dJ_i=0 and [d,Pi_M]J_H=0 => Pi_M dJ_extra=0",
            "zero_route": "boundary exactness, topological/covariant domain, positive source-free memory operator, EH-only exterior, q_loc zero, PiM commutator zero, no anomaly",
            "current_result": "conditional_theorem_only",
            "blocker": "q_loc, PiM commutator, domain, nonEH, memory/range, anomaly, and calibration clauses are not all parent-signed",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "attempt_id": "ESA739_4_current_chain_verdict",
            "target": "mu_extra=0",
            "math_form": "mu_extra=0 would require epsilon_i=0 for all force and source-normalization channels",
            "zero_route": "derive zeros or fill source-backed coefficients",
            "current_result": "not_derived_for_current_chain",
            "blocker": "coefficient vector still contains MISSING_DERIVED_ZERO_OR_NUMERIC_COEFFICIENT rows",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def build_channel_rows(generated_utc: str) -> list[dict[str, Any]]:
    rows = [
        {
            "channel_id": "EX739_0_boundary_reference",
            "source_channel": "boundary_monopole_shift",
            "symbol": "epsilon_boundary",
            "projection_formula": "I_boundary=int_A Pi_M dJ_boundary or int_partialA Pi_M K_boundary",
            "theorem_zero_route": "boundary term is exact/topological with fixed reference class and no observed edge-mode mass flux",
            "current_status": "proper_representative_boundary_zero_only_observed_boundary_flux_open",
            "observable_locks": "alpha3;xi;Gdot;beta;compact-shell",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "channel_id": "EX739_1_domain_projector",
            "source_channel": "domain_projector_mass",
            "symbol": "epsilon_domain_projector",
            "projection_formula": "I_domain=int_A Pi_M dJ_domain + domain/homology variation",
            "theorem_zero_route": "domain selector is parent-owned, covariantly constant/topological, and carries no mass/vector/shear leakage",
            "current_status": "open_no_parent_domain_silence",
            "observable_locks": "alpha1;alpha2;alpha3;xi;R11",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "channel_id": "EX739_2_memory_range",
            "source_channel": "bulk_X_Yukawa_tail",
            "symbol": "epsilon_bulk_X",
            "projection_formula": "I_memory=int_A Pi_M dJ_memory/range",
            "theorem_zero_route": "positive source-free mass-gap/nohair theorem kills local exterior tail",
            "current_status": "conditional_positive_operator_route_not_current_derived",
            "observable_locks": "R10 alpha(lambda);R11 operator vector;radial hair",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "channel_id": "EX739_3_nonEH_operator",
            "source_channel": "nonEH_operator_potential",
            "symbol": "epsilon_nonEH_source",
            "projection_formula": "I_nonEH=int_A Pi_M dJ_nonEH or weak-field operator source",
            "theorem_zero_route": "local exterior is strictly EH/spin-2 with all scalar/vector/tensor extra modes absent or massive and unexcited",
            "current_status": "open_EH_selection_not_complete",
            "observable_locks": "gamma;beta;R10;R11",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "channel_id": "EX739_4_q_loc_mass_projection",
            "source_channel": "q_loc_projection",
            "symbol": "epsilon_q_loc",
            "projection_formula": "I_q=int_A C_qmu q_loc^mu or int_A Pi_M dJ_q",
            "theorem_zero_route": "observed q_loc=0 from reduced Ward/on-shell/boundary silence or sourced C_qmu map below local bounds",
            "current_status": "open_observed_q_loc_not_zero_C_qmu_missing",
            "observable_locks": "Y5 source normalization;PPN;R10;R11;compact-shell",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "channel_id": "EX739_5_projector_stress",
            "source_channel": "projector_variation_mass",
            "symbol": "Delta_PiM",
            "projection_formula": "I_PiM=int_A [d,Pi_M]J_H or int_S (delta Pi_M)J_H",
            "theorem_zero_route": "topological absolute Pi_M with Hilbert equality, or Hodge/DeWitt projector stress theorem-cancelled",
            "current_status": "open_after_738_commutator_and_Hilbert_equality_missing",
            "observable_locks": "Meff radial hair;gamma;beta;alpha_i;xi;R11",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "channel_id": "EX739_6_coupling_or_constant_drift",
            "source_channel": "time_drift_and_coupling_drift",
            "symbol": "epsilon_time_drift",
            "projection_formula": "I_coupling ~ d ln(G_eff or kappa or source prefactor)",
            "theorem_zero_route": "parent action fixes local coupling/reference constants with no radial, temporal, or species dependence",
            "current_status": "open_constant_sector_not_locked",
            "observable_locks": "Gdot;clocks;PPN;R10 coefficient drift",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "channel_id": "EX739_7_frame_species_dressed_charge",
            "source_channel": "species_source_charge",
            "symbol": "epsilon_species_A",
            "projection_formula": "I_species=int_A Pi_M dJ_species+dressed binding/field contribution",
            "theorem_zero_route": "one observed coframe/no-marker plus dressed Hilbert source universality for binding, field, boundary, and material sectors",
            "current_status": "direct_marker_partly_zero_dressed_charge_open",
            "observable_locks": "WEP;clock redshift;composition tests",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "channel_id": "EX739_8_parent_anomaly_multiplier",
            "source_channel": "parent_anomaly_or_multiplier",
            "symbol": "epsilon_anomaly",
            "projection_formula": "I_anomaly=int_A A_parent or multiplier-source leakage",
            "theorem_zero_route": "Noether/Bianchi identity is anomaly-free and no multiplier inserts mass closure by hand",
            "current_status": "open_closure_multiplier_forbidden_unless_independently_owned",
            "observable_locks": "all local source-normalization gates",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "channel_id": "EX739_9_absolute_calibration",
            "source_channel": "absolute_calibration_offset",
            "symbol": "epsilon_calibration",
            "projection_formula": "mu_obs=lambda0 G_ref M_H plus possible radial/time/species derivative",
            "theorem_zero_route": "lambda0 is universal, constant, parent-fixed, and absorbed into measured GM with zero derivative hair",
            "current_status": "harmless_only_if_parent_fixed_not_force_channel",
            "observable_locks": "Gauss/orbital calibration;Gdot;beta;absolute GM",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]
    return rows


def build_bound_rows(channel_rows: list[dict[str, Any]], generated_utc: str) -> list[dict[str, Any]]:
    requirement_map = {
        "boundary_monopole_shift": "epsilon_boundary;units;reference_class;boundary_integral;alpha3_equivalent;source_file;no_cancellation_flag",
        "domain_projector_mass": "epsilon_domain_projector;domain_selector;projector_variation;alpha_i_or_R11_map;source_file;no_cancellation_flag",
        "bulk_X_Yukawa_tail": "lambda_X;alpha_X;operator_mass;source_normalization;R10_bound_row;source_file;no_cancellation_flag",
        "nonEH_operator_potential": "operator_family;coefficient;Green_function;PPN_or_R11_map;source_file;no_cancellation_flag",
        "q_loc_projection": "C_qmu;q_loc_profile;units;weak_field_map;Y5_PPN_R10_row;source_file;no_cancellation_flag",
        "projector_variation_mass": "Delta_PiM;projector_type;metric_dependence_flag;Hilbert_equality_residual;source_file;no_cancellation_flag",
        "time_drift_and_coupling_drift": "dlnGdt_or_dlnkappadt;clock_or_Gdot_bound;units;source_file;no_cancellation_flag",
        "species_source_charge": "Delta_A_mu;composition_pair;WEP_or_clock_bound;binding_energy_map;source_file;no_cancellation_flag",
        "parent_anomaly_or_multiplier": "A_parent_integral;identity_residual;multiplier_owner;units;source_file;no_cancellation_flag",
        "absolute_calibration_offset": "lambda0;universality_certificate;range_derivative;time_derivative;species_derivative;source_file",
    }
    rows: list[dict[str, Any]] = []
    for channel in channel_rows:
        rows.append(
            {
                "input_id": channel["channel_id"].replace("EX739", "CBI739"),
                "quantity": channel["symbol"],
                "source_channel": channel["source_channel"],
                "formula": channel["projection_formula"],
                "required_columns": requirement_map[channel["source_channel"]],
                "observable_locks": channel["observable_locks"],
                "current_status": "template_written_not_filled",
                "acceptance_gate": "valid_for_claim only if theorem_zero=true or numeric row is sourced, unit-normalized, below bound, and no_cancellation_flag=true",
                "valid_for_claim": "false",
                "generated_utc": generated_utc,
            }
        )
    rows.append(
        {
            "input_id": "CBI739_total_norm",
            "quantity": "epsilon_extra_total",
            "source_channel": "all_channels",
            "formula": "epsilon_extra_total <= sum_i abs(epsilon_i)",
            "required_columns": "all channel rows above plus common normalization M_eff_ref and arena-specific bound map",
            "observable_locks": "Y5;PPN;R10;R11;WEP;clock;orbital",
            "current_status": "not_run",
            "acceptance_gate": "no total-pass unless every channel is individually zero/bounded; no tuned cancellation",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    )
    return rows


def build_y5_update_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "runner_id": "Y5R739_1_Meff_conservation",
            "source_row": "Y5B_1_Meff_conservation",
            "status_after_739": "still_open_projected_flux_needs_PiM_and_extra_silence",
            "zero_or_input": "d(Pi_M J_H)=Pi_M dJ_H+[d,Pi_M]J_H+Pi_M dJ_extra+A_parent",
            "still_missing": "PiM Hilbert equality, commutator zero/bound, all extra channel zeros/bounds, anomaly silence",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "runner_id": "Y5R739_2_radial_source_hair",
            "source_row": "Y5B_2_radial_source_hair",
            "status_after_739": "channelwise_radial_numerator_split_not_scored",
            "zero_or_input": "epsilon_radial_Meff includes commutator, equality residual, extra-channel integrals, and anomaly terms",
            "still_missing": "source-backed shell profiles or theorem-zero rows for each channel",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "runner_id": "Y5R739_5_extra_mass_projection",
            "source_row": "Y5B_5_extra_mass_projection",
            "status_after_739": "full_silence_not_derived_channelwise_queue_written",
            "zero_or_input": "conditional theorem written: forall i Pi_M dJ_i=0 implies Pi_M dJ_extra=0",
            "still_missing": "q_loc C_qmu map, boundary/domain/memory/nonEH/projector/coupling/species/anomaly/calibration rows",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "runner_id": "Y5R739_9_q_loc_projection",
            "source_row": "Y5B_9_q_loc_projection",
            "status_after_739": "promoted_to_first_next_channel_target",
            "zero_or_input": "I_q=int_A C_qmu q_loc^mu is now an explicit mass-channel row",
            "still_missing": "C_qmu normalization, q_loc profile/units, weak-field map, and arena bounds",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def build_decision_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "D739_0_silence_attempt_result",
            "decision": "do not claim Pi_M dJ_extra=0",
            "meaning": "the all-channel theorem is only conditional; current corpus leaves q_loc, boundary/domain/memory/nonEH/projector/coupling/species/anomaly/calibration channels open",
            "claim_status": "blocked_for_current_claim",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D739_1_no_cancellation_gate",
            "decision": "score absolute channel envelope, not tuned totals",
            "meaning": "MTS can still win like Mayweather, but not by hiding one unproven source behind another; every punch has to be legal on its own card",
            "claim_status": "policy_guard_active",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D739_2_q_loc_next",
            "decision": "attack q_loc mass-channel first",
            "meaning": "q_loc is the most explicit current missing projection because the previous narrow zeros do not kill observed q_loc and C_qmu remains missing",
            "claim_status": "next_derivation_or_bound_target",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D739_3_Gauss_not_yet",
            "decision": "defer Gauss/orbital calibration until source charge is cleaner",
            "meaning": "a calibration theorem is premature while extra-channel source normalization is neither zeroed nor bounded",
            "claim_status": "deferred_not_rejected",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def build_route_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "route_id": "RU739_0_allowed",
            "allowed_after_739": "say extra-mass projection has a clean channel split and conditional silence theorem",
            "forbidden_after_739": "say mu_extra=0, source-normalized Newton, R10, PPN, WEP, or local GR has passed",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "RU739_1_allowed",
            "allowed_after_739": "use channelwise bound rows with no-cancellation envelope",
            "forbidden_after_739": "cancel open channels against each other or score placeholder coefficients",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "RU739_2_allowed",
            "allowed_after_739": "attack q_loc-to-mass projection C_qmu as the next first channel",
            "forbidden_after_739": "move to Gauss/orbital calibration as if source mass were already clean",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def build_summary_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "main_result": "extra-mass projection silence theorem written as a conditional all-channel theorem; current-chain proof fails honestly; channelwise bound queue written",
            "hard_blocker": "observed q_loc/C_qmu, PiM commutator/equality, domain/boundary/memory/nonEH/projector/coupling/species/anomaly/calibration rows remain unsourced or nonzero",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def make_validation(
    source_register: list[dict[str, Any]],
    silence_rows: list[dict[str, Any]],
    channel_rows: list[dict[str, Any]],
    bound_rows: list[dict[str, Any]],
    y5_rows: list[dict[str, Any]],
    decision_rows: list[dict[str, Any]],
    output_paths: list[Path],
) -> list[dict[str, str]]:
    validation: list[dict[str, str]] = []
    validation.append(
        {
            "check_id": "V739_0_source_paths_exist",
            "result": "pass" if all(row["exists"] == "true" for row in source_register) else "fail",
            "detail": f"source_rows={len(source_register)}",
        }
    )
    validation.append(
        {
            "check_id": "V739_1_source_needles_present",
            "result": "pass" if all(row["needle_check"] == "true" for row in source_register) else "fail",
            "detail": "all source files contain expected evidence needles",
        }
    )
    prior_validation = read_csv_rows(RESIDUALS / "P8_Y5_BRR545_738_VALIDATION.csv")
    validation.append(
        {
            "check_id": "V739_2_prior_738_clean",
            "result": "pass" if prior_validation and all(row.get("result") == "pass" for row in prior_validation) else "fail",
            "detail": "738 validation has no failures",
        }
    )
    validation.append(
        {
            "check_id": "V739_3_738_selected_739",
            "result": "pass" if text_contains(SOURCES["738_doc"]["path"], ["739-Y5-R10-extra-mass-projection-silence-or-channelwise-bound.md"]) else "fail",
            "detail": "739-Y5-R10-extra-mass-projection-silence-or-channelwise-bound.md",
        }
    )
    validation.append(
        {
            "check_id": "V739_4_silence_rows_complete",
            "result": "pass" if len(silence_rows) == 5 else "fail",
            "detail": f"silence_rows={len(silence_rows)}",
        }
    )
    validation.append(
        {
            "check_id": "V739_5_full_silence_not_promoted",
            "result": "pass" if any(row["current_result"] == "not_derived_for_current_chain" for row in silence_rows) else "fail",
            "detail": "mu_extra zero not claimed",
        }
    )
    validation.append(
        {
            "check_id": "V739_6_no_cancellation_gate_active",
            "result": "pass" if any("sum_i |epsilon_i|" in row["math_form"] for row in silence_rows) else "fail",
            "detail": "absolute-envelope no-cancellation rule present",
        }
    )
    channel_ids = {row["channel_id"] for row in channel_rows}
    required_channels = {"EX739_4_q_loc_mass_projection", "EX739_5_projector_stress", "EX739_8_parent_anomaly_multiplier"}
    validation.append(
        {
            "check_id": "V739_7_hard_channels_present",
            "result": "pass" if required_channels.issubset(channel_ids) else "fail",
            "detail": ";".join(sorted(channel_ids)),
        }
    )
    validation.append(
        {
            "check_id": "V739_8_q_loc_open",
            "result": "pass" if any(row["source_channel"] == "q_loc_projection" and "open" in row["current_status"] for row in channel_rows) else "fail",
            "detail": "observed q_loc/C_qmu remains open",
        }
    )
    validation.append(
        {
            "check_id": "V739_9_projector_stress_retained",
            "result": "pass" if any(row["source_channel"] == "projector_variation_mass" and "commutator" in row["current_status"] for row in channel_rows) else "fail",
            "detail": "PiM commutator/equality remains retained",
        }
    )
    validation.append(
        {
            "check_id": "V739_10_bound_queue_complete",
            "result": "pass" if len(bound_rows) == len(channel_rows) + 1 else "fail",
            "detail": f"bound_rows={len(bound_rows)};channel_rows={len(channel_rows)}",
        }
    )
    validation.append(
        {
            "check_id": "V739_11_Y5_rows_retained",
            "result": "pass" if {"Y5R739_5_extra_mass_projection", "Y5R739_9_q_loc_projection"}.issubset({row["runner_id"] for row in y5_rows}) else "fail",
            "detail": "extra mass and q_loc Y5 rows retained",
        }
    )
    all_rows = silence_rows + channel_rows + bound_rows + y5_rows + decision_rows
    validation.append(
        {
            "check_id": "V739_12_no_claim_rows_promoted",
            "result": "pass" if all(str(row.get("valid_for_claim", "false")).lower() == "false" for row in all_rows) else "fail",
            "detail": "all generated rows valid_for_claim=false",
        }
    )
    validation.append(
        {
            "check_id": "V739_13_next_target_selected",
            "result": "pass" if all(row.get("next_target") == NEXT_TARGET for row in decision_rows) else "fail",
            "detail": NEXT_TARGET,
        }
    )
    validation.append(
        {
            "check_id": "V739_14_outputs_scoped",
            "result": "pass" if all(under_post(path) for path in output_paths) else "fail",
            "detail": "all outputs under post-checkpoint-work",
        }
    )
    changed = formalization_changed_after_cutoff()
    validation.append(
        {
            "check_id": "V739_15_formalization_workbench_untouched",
            "result": "pass" if changed == 0 else "fail",
            "detail": f"formalization_changed_after_cutoff={changed}",
        }
    )
    validation.append(
        {
            "check_id": "V739_16_no_local_arena_claim",
            "result": "pass" if CLAIM_CEILING.endswith("no_mu_extra_zero_Newton_PPN_R10_or_local_GR_pass") else "fail",
            "detail": "R10/WEP/PPN/Newton/local-GR claims remain blocked",
        }
    )
    validation.append(
        {
            "check_id": "V739_17_validation_rows_ready",
            "result": "pass",
            "detail": "validation table constructed",
        }
    )
    return validation


def build_doc(
    source_register: list[dict[str, Any]],
    silence_rows: list[dict[str, Any]],
    channel_rows: list[dict[str, Any]],
    bound_rows: list[dict[str, Any]],
    y5_rows: list[dict[str, Any]],
    decision_rows: list[dict[str, Any]],
    route_rows: list[dict[str, Any]],
    summary_rows: list[dict[str, Any]],
    validation_rows: list[dict[str, Any]],
) -> None:
    text = f"""# 739 - Y5 R10 Extra-Mass Projection Silence Or Channelwise Bound

Start point: 738 sharpened `Pi_M` ownership but left the source chain unclosed. This checkpoint asks whether the non-Hilbert/extra projected mass channel is silent:

```text
Pi_M dJ_extra = 0
```

Current verdict: **the exact extra-mass silence theorem does not close for the current chain**. The clean theorem is only conditional; the useful output is now a channelwise residual/bound ledger.

```text
I_extra[A] = int_A Pi_M dJ_extra
           = sum_i int_A Pi_M dJ_i
|epsilon_extra| <= sum_i |epsilon_i|
```

No cancellation credit is allowed: every channel must be theorem-zero or individually source-backed below its mapped local bound.

## Summary

| Field | Value |
| --- | --- |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Main result | conditional silence theorem plus channelwise bound queue |
| Next target | `{NEXT_TARGET}` |

## Silence Attempt

{markdown_table(silence_rows, ["attempt_id", "target", "math_form", "zero_route", "current_result", "blocker", "valid_for_claim"])}

## Channelwise Projection Ledger

{markdown_table(channel_rows, ["channel_id", "source_channel", "symbol", "projection_formula", "theorem_zero_route", "current_status", "observable_locks", "valid_for_claim"])}

## Bound Input Queue

{markdown_table(bound_rows, ["input_id", "quantity", "source_channel", "formula", "required_columns", "observable_locks", "current_status", "acceptance_gate", "valid_for_claim"])}

## Y5 Runner Update

{markdown_table(y5_rows, ["runner_id", "source_row", "status_after_739", "zero_or_input", "still_missing", "valid_for_claim"])}

## Decisions

{markdown_table(decision_rows, ["decision_id", "decision", "meaning", "claim_status", "next_target", "valid_for_claim"])}

## Route Update

{markdown_table(route_rows, ["route_id", "allowed_after_739", "forbidden_after_739", "next_action", "valid_for_claim"])}

## Nonclaim Summary

{markdown_table(summary_rows, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim"])}

## Source Register

{markdown_table(source_register, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim"])}

## Validation

{markdown_table(validation_rows, ["check_id", "result", "detail"])}

## Plain-English Verdict

This is not the fireworks theorem, but it is a useful narrowing. The extra-mass problem is no longer a fog bank called `mu_extra`; it is a finite list of channels with one harsh rule: no hidden cancellations. The most dangerous live channel is now `q_loc` projected into source mass by `C_qmu`, because the previous q_loc work killed only narrow representative/direct-marker pieces, not the observed reduced residual. So 740 should go straight at `C_qmu q_loc`: derive its silence, or turn it into the first source-backed channel bound.
"""
    OUTPUT_DOC.write_text(text, encoding="utf-8")


def main() -> None:
    generated_utc = utc_stamp()
    source_register = make_source_register(generated_utc)
    silence_rows = build_silence_rows(generated_utc)
    channel_rows = build_channel_rows(generated_utc)
    bound_rows = build_bound_rows(channel_rows, generated_utc)
    y5_rows = build_y5_update_rows(generated_utc)
    decision_rows = build_decision_rows(generated_utc)
    route_rows = build_route_rows(generated_utc)
    summary_rows = build_summary_rows(generated_utc)

    output_paths = [
        OUTPUT_DOC,
        SOURCE_REGISTER_PATH,
        SILENCE_ATTEMPT_PATH,
        CHANNEL_LEDGER_PATH,
        BOUND_QUEUE_PATH,
        Y5_UPDATE_PATH,
        DECISION_PATH,
        ROUTE_PATH,
        SUMMARY_PATH,
        VALIDATION_PATH,
    ]

    validation_rows = make_validation(
        source_register,
        silence_rows,
        channel_rows,
        bound_rows,
        y5_rows,
        decision_rows,
        output_paths,
    )

    write_csv(SOURCE_REGISTER_PATH, source_register, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(SILENCE_ATTEMPT_PATH, silence_rows, ["attempt_id", "target", "math_form", "zero_route", "current_result", "blocker", "valid_for_claim", "generated_utc"])
    write_csv(CHANNEL_LEDGER_PATH, channel_rows, ["channel_id", "source_channel", "symbol", "projection_formula", "theorem_zero_route", "current_status", "observable_locks", "valid_for_claim", "generated_utc"])
    write_csv(BOUND_QUEUE_PATH, bound_rows, ["input_id", "quantity", "source_channel", "formula", "required_columns", "observable_locks", "current_status", "acceptance_gate", "valid_for_claim", "generated_utc"])
    write_csv(Y5_UPDATE_PATH, y5_rows, ["runner_id", "source_row", "status_after_739", "zero_or_input", "still_missing", "valid_for_claim", "generated_utc"])
    write_csv(DECISION_PATH, decision_rows, ["decision_id", "decision", "meaning", "claim_status", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(ROUTE_PATH, route_rows, ["route_id", "allowed_after_739", "forbidden_after_739", "next_action", "valid_for_claim", "generated_utc"])
    write_csv(SUMMARY_PATH, summary_rows, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(VALIDATION_PATH, validation_rows, ["check_id", "result", "detail"])
    build_doc(source_register, silence_rows, channel_rows, bound_rows, y5_rows, decision_rows, route_rows, summary_rows, validation_rows)

    print(
        json.dumps(
            {
                "generated_utc": generated_utc,
                "status": STATUS,
                "claim_ceiling": CLAIM_CEILING,
                "next_target": NEXT_TARGET,
                "doc": str(OUTPUT_DOC),
                "validation": str(VALIDATION_PATH),
                "all_validation_pass": all(row["result"] == "pass" for row in validation_rows),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
