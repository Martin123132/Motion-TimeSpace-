from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


POST_CHECKPOINT = Path(__file__).resolve().parents[1]
REPO_ROOT = POST_CHECKPOINT.parent
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"
FORMALIZATION = REPO_ROOT / "formalization-workbench"

OUTPUT_DOC = POST_CHECKPOINT / "746-Y5-R10-q_loc-to-PPN-or-alpha3-projection-map-contract.md"
NEXT_TARGET = "747-Y5-R10-alpha3-momentum-flux-zero-or-q_loc-vector-coefficient-bound.md"
STATUS = "Y5_R10_746_q_loc_projection_map_contract_written_alpha3_pressure_selected_nonclaim"
CLAIM_CEILING = "projection_map_contract_only_no_q_loc_PPN_alpha3_R10_pass_no_mu_extra_zero_no_R10_PPN_Newton_or_local_GR_pass"
Q_PROXY = 7.432631961576971e-06
ALPHA3_BOUND = 4.0e-20
FORMALIZATION_CUTOFF = datetime(2026, 5, 31, 14, 42, 0)

SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_746_SOURCE_REGISTER.csv"
PROJECTION_CONTRACT_PATH = RESIDUALS / "P8_Y5_R10_746_QLOC_PROJECTION_CONTRACT.csv"
CHANNEL_ROUTER_PATH = RESIDUALS / "P8_Y5_R10_746_QLOC_CHANNEL_ROUTER.csv"
ALPHA3_GATE_PATH = RESIDUALS / "P8_Y5_R10_746_ALPHA3_MOMENTUM_FLUX_GATE.csv"
PPN_GATE_PATH = RESIDUALS / "P8_Y5_R10_746_PPN_SCALAR_VECTOR_GATE.csv"
R10_GATE_PATH = RESIDUALS / "P8_Y5_R10_746_R10_RANGE_GATE.csv"
Y5_UPDATE_PATH = RESIDUALS / "P8_Y5_R10_746_Y5_RUNNER_UPDATE.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_R10_746_DECISION_MATRIX.csv"
ROUTE_PATH = RESIDUALS / "P8_Y5_R10_746_ROUTE_UPDATE.csv"
SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_746_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_746_VALIDATION.csv"

SOURCES: dict[str, dict[str, Any]] = {
    "745_doc": {
        "path": POST_CHECKPOINT / "745-Y5-R10-c_qM-engineering-smoke-row-or-source-backed-Mref-hunt.md",
        "needles": ["NLC745_alpha3", "derive q_loc-to-PPN or alpha3 projection map", "746-Y5-R10-q_loc-to-PPN-or-alpha3-projection-map-contract.md"],
        "role": "immediate projection-map handoff",
    },
    "745_validation": {
        "path": RESIDUALS / "P8_Y5_BRR545_745_VALIDATION.csv",
        "needles": ["V745_7_naive_lock_mixed_results", "V745_14_formalization_workbench_untouched", "V745_15_no_local_arena_claim"],
        "role": "prior validation guard",
    },
    "745_locks": {
        "path": RESIDUALS / "P8_Y5_R10_745_NAIVE_LOCK_COMPARISON.csv",
        "needles": ["NLC745_alpha3", "185815799039424", "not_scoreable"],
        "role": "naive lock comparison forcing projection map",
    },
    "PPN_vector": {
        "path": RESIDUALS / "P8_Y5_PPN_RESIDUAL_VECTOR.csv",
        "needles": ["PPN524_7_q_loc_second_order_force", "PPN524_5_alpha3_flux", "not_derived_zero"],
        "role": "PPN residual vector with q_loc and alpha3 rows",
    },
    "PPN_metric_contract": {
        "path": RESIDUALS / "P8_Y5_PPN_METRIC_EXPANSION_CONTRACT.csv",
        "needles": ["MEX524_5_q_loc_second_order_silence", "MEX524_3_gravitomagnetic_preferred_frame", "not_derived_zero"],
        "role": "metric expansion contract",
    },
    "PPN_gates": {
        "path": RESIDUALS / "P8_Y5_PPN_SOURCE_STABILITY_GATES.csv",
        "needles": ["PSG524_7_q_loc_second_order_silent", "PSG524_6_preferred_frame_location_zero", "pass_policy_enforced"],
        "role": "PPN promotion gates",
    },
    "beta_q_loc_gates": {
        "path": RESIDUALS / "P8_Y5_BETA_QLOC_ACCEPTANCE_GATES.csv",
        "needles": ["BG526_2_q_loc_U2_bound_mapped", "provisional_compact_shell_budget_only", "cannot_promote_q_loc_silence"],
        "role": "beta/q_loc acceptance gates",
    },
    "beta_q_loc_decision": {
        "path": RESIDUALS / "P8_Y5_BETA_QLOC_DECISION.csv",
        "needles": ["D526_2_q_loc_budget_provisional", "D526_3_alpha3_warning", "blocks_local_GR"],
        "role": "beta provisional and alpha3 warning",
    },
    "q_loc_U2_bound": {
        "path": RESIDUALS / "P8_Y5_QLOC_U2_BOUND.csv",
        "needles": ["QBU526_0_compact_shell_to_beta_if_same_normalization", "QBU526_1_compact_shell_to_alpha3_warning", "MISSING_CONVERSION"],
        "role": "older q_loc U2/beta/alpha3 smoke comparison",
    },
    "q_loc_transfer": {
        "path": RESIDUALS / "P8_Y5_R10_740_QLOC_OBSERVABLE_TRANSFER_MAP.csv",
        "needles": ["QOT740_3_PPN_vector", "QOT740_4_R10_range", "not_executable"],
        "role": "q_loc observable transfer map skeleton",
    },
    "alpha3_product_input": {
        "path": RESIDUALS / "P8_ALPHA3_BOUND_PRODUCT_INPUT.csv",
        "needles": ["target_bound", "4e-20", "MISSING_NUMERIC_OR_THEOREM_ZERO"],
        "role": "alpha3 product input template",
    },
    "alpha3_product_eval": {
        "path": RESIDUALS / "P8_ALPHA3_BOUND_PRODUCT_EVALUATION.csv",
        "needles": ["target_bound", "4e-20", "not_scoreable_inputs_missing"],
        "role": "alpha3 product evaluator",
    },
    "q_loc_spec": {
        "path": RESIDUALS / "P8_QLOC_BOUND_RUNNER_SPEC.csv",
        "needles": ["alpha3-equivalent channel", "coefficient normalization from q_loc to alpha3", "PPN_metric_tail"],
        "role": "q_loc bound runner spec",
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
        if path.is_file() and datetime.fromtimestamp(path.stat().st_mtime) > FORMALIZATION_CUTOFF:
            count += 1
    return count


def make_source_register(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "source_id": source_id,
            "path": str(spec["path"]),
            "exists": bool_string(Path(spec["path"]).exists()),
            "needle_check": bool_string(text_contains(Path(spec["path"]), spec["needles"])),
            "role": spec["role"],
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
        for source_id, spec in SOURCES.items()
    ]


def projection_contract_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "contract_id": "QPC746_0_decompose_q_loc",
            "clause": "q_loc must be decomposed before any PPN/alpha3/R10 comparison",
            "mathematical_form": "q_loc^nu = q_T tau^nu + q_L n^nu + q_V^nu + q_TF^nu with channel-specific projectors",
            "required_inputs": "observed frame; tau/n split; spatial projector; domain/shell; units; source path",
            "current_status": "contract_written_components_unfilled",
            "claim_effect": "prevents scalar smoke from becoming all-channel evidence",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "QPC746_1_scalar_even_PPN",
            "clause": "beta/gamma channels need scalar/even weak-field map",
            "mathematical_form": "delta_beta_q or delta_gamma_q = W_even[q_T,q_L,q_TF] * q_proxy",
            "required_inputs": "weak-field Green operator; gauge; beta/gamma normalization; W_even coefficient",
            "current_status": "not_executable",
            "claim_effect": "old beta-smoke remains interesting but not claimable",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "QPC746_2_alpha3_momentum_flux",
            "clause": "alpha3 applies only to momentum-flux/preferred-frame projection",
            "mathematical_form": "alpha3_q = W_q_alpha3 * epsilon_q_momentum",
            "required_inputs": "q_loc momentum flux component; preferred-frame map; W_q_alpha3; source path; alpha3 bound",
            "current_status": "highest_pressure_if_nonzero",
            "claim_effect": "alpha3 is the most dangerous branch only if q_loc has this vector/flux projection",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "QPC746_3_R10_range",
            "clause": "R10 applies only if q_loc supplies finite-range kernel",
            "mathematical_form": "alpha_q(lambda)=c_q_alpha(lambda) * q_proxy",
            "required_inputs": "lambda; range kernel; real bound curve; c_q_alpha(lambda); no-range theorem or source",
            "current_status": "not_executable",
            "claim_effect": "R10 remains unscoreable without lambda/projection map",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "QPC746_4_no_single_scalar_pass",
            "clause": "one c_qM scalar cannot decide PPN, alpha3, and R10 together",
            "mathematical_form": "Delta_q = {delta_gamma_q, delta_beta_q, alpha_i_q, xi_q, alpha_q(lambda)} componentwise",
            "required_inputs": "separate coefficients and bounds per component; no cancellation",
            "current_status": "policy_active",
            "claim_effect": "all outputs remain nonclaim until component map is filled",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def channel_router_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "route_id": "QCR746_0_beta_scalar_U2",
            "target": "R4_beta",
            "condition": "q_loc maps to O(U^2) scalar g00 coefficient with same beta normalization",
            "known_pressure": f"unit smoke ratio to beta = {Q_PROXY / 7.8e-5:.15g}",
            "current_result": "provisionally_below_if_same_normalization_but_conversion_missing",
            "missing": "q_loc_U2_conversion_factor; A/B source equation; weak-field Green operator",
            "priority": "medium_after_alpha3",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "QCR746_1_gamma_slip",
            "target": "R3_gamma",
            "condition": "q_loc sources spatial curvature slip or non-EH operator tail",
            "known_pressure": f"unit smoke ratio to gamma = {Q_PROXY / 2.3e-5:.15g}",
            "current_result": "below_naive_lock_but_map_missing",
            "missing": "spatial metric Green operator; gauge; slip coefficient",
            "priority": "medium_after_alpha3",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "QCR746_2_alpha3_momentum_flux",
            "target": "R7_alpha3",
            "condition": "q_loc has momentum nonconservation/preferred-frame flux projection",
            "known_pressure": f"unit smoke ratio to alpha3 = {Q_PROXY / ALPHA3_BOUND:.15g}",
            "current_result": "highest_pressure_branch_if_projection_applies",
            "missing": "W_q_alpha3; epsilon_q_momentum; theorem-zero of momentum flux or numeric product",
            "priority": "highest",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "QCR746_3_xi_alpha2_preferred_location",
            "target": "R6_alpha2/R8_xi",
            "condition": "q_loc carries domain/vector/preferred-location anisotropy",
            "known_pressure": "unit smoke above xi and alpha2 naive locks",
            "current_result": "danger_branch_if_anisotropy_projection_applies",
            "missing": "domain/vector anisotropy coefficient; location potential map",
            "priority": "high_after_alpha3",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "QCR746_4_R10_range",
            "target": "R10_alpha_lambda",
            "condition": "q_loc has finite-range/range-dependent source kernel",
            "known_pressure": "not scoreable without lambda",
            "current_result": "unrouted",
            "missing": "lambda; c_q_alpha(lambda); real bound curve; range kernel",
            "priority": "defer_until_range_kernel_exists",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def alpha3_gate_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "A3Q746_0_product_law",
            "target": "alpha3_q",
            "formula": "alpha3_q = W_q_alpha3 * epsilon_q_momentum",
            "current_status": "product_law_written_inputs_missing",
            "blocker": "W_q_alpha3 and epsilon_q_momentum are not sourced; theorem-zero not proved",
            "acceptance": "valid only if product is theorem-zero or numeric and |alpha3_q|<=4e-20",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "A3Q746_1_zero_route",
            "target": "epsilon_q_momentum=0",
            "formula": "P_momentum q_loc = 0 or q_loc is purely scalar/even with no g0i/preferred-frame flux",
            "current_status": "not_derived",
            "blocker": "observed q_loc decomposition and parent Ward zero through O(U^2) missing",
            "acceptance": "would remove alpha3 pressure for q_loc only, not other alpha3 channels",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "A3Q746_2_bound_route",
            "target": "numeric alpha3_q bound",
            "formula": f"|W_q_alpha3 * epsilon_q_momentum| <= {ALPHA3_BOUND:.1e}",
            "current_status": "not_scoreable",
            "blocker": "numeric product missing; naive unit projection would exceed bound by huge factor if W=1 and epsilon=q_proxy",
            "acceptance": "requires source-backed product, not q_proxy direct comparison",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "A3Q746_3_next",
            "target": "next target",
            "formula": "derive zero of q_loc momentum flux or fill W_q_alpha3 epsilon_q_momentum product",
            "current_status": "selected",
            "blocker": "highest-pressure branch unresolved",
            "acceptance": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def ppn_gate_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "PPNQ746_0_beta",
            "target": "delta_beta_q",
            "formula": "delta_beta_q = W_q_beta * q_proxy",
            "current_status": "conversion_missing",
            "known_pressure": "old QBU526 says below beta if same normalization",
            "missing": "W_q_beta; source A/B equation; U2 conversion factor",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "PPNQ746_1_gamma",
            "target": "delta_gamma_q",
            "formula": "delta_gamma_q = W_q_gamma * q_proxy",
            "current_status": "map_missing",
            "known_pressure": "unit smoke below gamma naive lock",
            "missing": "spatial curvature slip map and gauge",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "PPNQ746_2_preferred_frame",
            "target": "alpha1/alpha2/alpha3/xi",
            "formula": "Delta_pref_q = W_pref_q * q_proxy",
            "current_status": "highest_tightness_unresolved",
            "known_pressure": "alpha2/xi/alpha3 naive locks are much tighter than q_proxy",
            "missing": "vector/preferred-frame decomposition",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "PPNQ746_3_envelope",
            "target": "componentwise PPN q_loc envelope",
            "formula": "|Delta_PPN_q| <= {|delta_gamma_q|,|delta_beta_q|,|alpha_i_q|,|xi_q|} componentwise",
            "current_status": "not_run",
            "known_pressure": "no cancellation allowed",
            "missing": "all W coefficients and component source rows",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def r10_gate_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "R10Q746_0_range_kernel",
            "target": "alpha_q(lambda)",
            "formula": "alpha_q(lambda)=c_q_alpha(lambda)*q_proxy",
            "current_status": "lambda_kernel_missing",
            "missing": "lambda, kernel shape, source normalization, real bound curve comparison",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "R10Q746_1_no_range_zero",
            "target": "c_q_alpha(lambda)=0",
            "formula": "q_loc has no finite-range source kernel in compact local branch",
            "current_status": "not_derived",
            "missing": "mass-gap/no-range theorem tied to q_loc, not just scalar memory",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "R10Q746_2_defer",
            "target": "R10 branch priority",
            "formula": "defer until alpha3/preferred-frame projection is routed or killed",
            "current_status": "deferred_not_rejected",
            "missing": "projection map and range kernel",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def y5_update_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "runner_id": "Y5R746_q_loc_PPN",
            "source_row": "Y5B_8/Y5B_9/PPN524_7",
            "status_after_746": "projection_contract_written_not_executable",
            "zero_or_input": "component map required before beta/gamma/alpha_i/xi scoring",
            "still_missing": "W_q_beta; W_q_gamma; W_q_alpha3; W_q_xi; component decomposition",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "runner_id": "Y5R746_alpha3",
            "source_row": "R7_alpha3",
            "status_after_746": "highest_pressure_branch_selected_if_momentum_projection_applies",
            "zero_or_input": "alpha3_q = W_q_alpha3 * epsilon_q_momentum",
            "still_missing": "momentum-flux zero theorem or numeric product <=4e-20",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "runner_id": "Y5R746_R10",
            "source_row": "R10_alpha_lambda",
            "status_after_746": "deferred_until_range_kernel_exists",
            "zero_or_input": "alpha_q(lambda)=c_q_alpha(lambda)*q_proxy",
            "still_missing": "lambda/range kernel and curve comparison",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "D746_0_projection_contract",
            "decision": "write componentwise q_loc projection contract",
            "meaning": "q_loc must be split before any PPN/alpha3/R10 comparison",
            "claim_status": "contract_only",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D746_1_beta_gamma",
            "decision": "keep beta/gamma as lower-pressure but unresolved",
            "meaning": "unit smoke is below naive beta/gamma locks, but U2/slip conversion is missing",
            "claim_status": "interesting_not_claim",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D746_2_alpha3",
            "decision": "select alpha3 momentum-flux branch as next target",
            "meaning": "if q_loc has preferred-frame/momentum-flux projection, alpha3 is the tightest danger lock",
            "claim_status": "highest_pressure_nonclaim",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D746_3_R10",
            "decision": "defer R10 range branch",
            "meaning": "R10 cannot score until lambda/range kernel exists; alpha3 routing is more urgent",
            "claim_status": "deferred_not_rejected",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def route_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "route_id": "RU746_0_allowed",
            "allowed_after_746": "say q_loc projection map is now componentwise",
            "forbidden_after_746": "use one scalar smoke number as PPN/R10/alpha3 evidence",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "RU746_1_allowed",
            "allowed_after_746": "attack alpha3 by proving q_loc momentum-flux zero or filling W_q_alpha3 epsilon_q_momentum",
            "forbidden_after_746": "claim alpha3 failure/pass from q_proxy alone",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "RU746_2_allowed",
            "allowed_after_746": "defer R10 until q_loc finite-range kernel exists",
            "forbidden_after_746": "invent lambda from the compact-shell proxy",
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
            "main_result": "q_loc projection map contract written; alpha3 momentum-flux branch selected as highest pressure if projection applies",
            "hard_blocker": "W_q_alpha3, epsilon_q_momentum, PPN W coefficients, and R10 range kernel remain missing",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def make_validation(
    sources: list[dict[str, Any]],
    contract: list[dict[str, Any]],
    router: list[dict[str, Any]],
    alpha3: list[dict[str, Any]],
    ppn: list[dict[str, Any]],
    r10: list[dict[str, Any]],
    y5_update: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    outputs: list[Path],
) -> list[dict[str, str]]:
    prior = read_csv_rows(RESIDUALS / "P8_Y5_BRR545_745_VALIDATION.csv")
    all_rows = contract + router + alpha3 + ppn + r10 + y5_update + decisions + routes
    validation: list[dict[str, str]] = []
    validation.append({"check_id": "V746_0_source_paths_exist", "result": "pass" if all(row["exists"] == "true" for row in sources) else "fail", "detail": f"source_rows={len(sources)}"})
    validation.append({"check_id": "V746_1_source_needles_present", "result": "pass" if all(row["needle_check"] == "true" for row in sources) else "fail", "detail": "all source files contain expected evidence needles"})
    validation.append({"check_id": "V746_2_prior_745_clean", "result": "pass" if prior and all(row.get("result") == "pass" for row in prior) else "fail", "detail": "745 validation has no failures"})
    validation.append({"check_id": "V746_3_component_decomposition_required", "result": "pass" if any("q_loc^nu" in row["mathematical_form"] and "q_T" in row["mathematical_form"] for row in contract) else "fail", "detail": "component decomposition contract written"})
    validation.append({"check_id": "V746_4_alpha3_product_law_written", "result": "pass" if any(row["formula"] == "alpha3_q = W_q_alpha3 * epsilon_q_momentum" for row in alpha3) else "fail", "detail": "alpha3 product law written"})
    validation.append({"check_id": "V746_5_alpha3_selected_next", "result": "pass" if any(row["priority"] == "highest" and row["target"] == "R7_alpha3" for row in router) else "fail", "detail": "alpha3 is highest pressure branch if projection applies"})
    validation.append({"check_id": "V746_6_beta_gamma_not_claimed", "result": "pass" if all(row["valid_for_claim"] == "false" for row in ppn) and any(row["current_status"] == "conversion_missing" for row in ppn) else "fail", "detail": "beta/gamma gates remain nonclaim"})
    validation.append({"check_id": "V746_7_R10_deferred", "result": "pass" if any(row["current_status"] == "deferred_not_rejected" for row in r10) else "fail", "detail": "R10 deferred until range kernel exists"})
    validation.append({"check_id": "V746_8_no_single_scalar_policy", "result": "pass" if any(row["contract_id"] == "QPC746_4_no_single_scalar_pass" for row in contract) else "fail", "detail": "single scalar c_qM cannot decide all observables"})
    validation.append({"check_id": "V746_9_Y5_rows_retained", "result": "pass" if {"Y5R746_q_loc_PPN", "Y5R746_alpha3", "Y5R746_R10"}.issubset({row["runner_id"] for row in y5_update}) else "fail", "detail": "PPN/alpha3/R10 rows retained"})
    validation.append({"check_id": "V746_10_no_claim_rows_promoted", "result": "pass" if all(row.get("valid_for_claim") == "false" for row in all_rows) else "fail", "detail": "all generated rows valid_for_claim=false"})
    validation.append({"check_id": "V746_11_next_target_selected", "result": "pass" if all(row.get("next_target") == NEXT_TARGET for row in decisions) else "fail", "detail": NEXT_TARGET})
    validation.append({"check_id": "V746_12_outputs_scoped", "result": "pass" if all(under_post(path) for path in outputs) else "fail", "detail": "all outputs under post-checkpoint-work"})
    changed = formalization_changed_after_cutoff()
    validation.append({"check_id": "V746_13_formalization_workbench_untouched", "result": "pass" if changed == 0 else "fail", "detail": f"formalization_changed_after_cutoff={changed}"})
    validation.append({"check_id": "V746_14_no_local_arena_claim", "result": "pass" if "no_R10_PPN_Newton_or_local_GR_pass" in CLAIM_CEILING else "fail", "detail": "R10/PPN/Newton/local-GR claims remain blocked"})
    validation.append({"check_id": "V746_15_validation_rows_ready", "result": "pass", "detail": "validation table constructed"})
    return validation


def build_doc(
    sources: list[dict[str, Any]],
    contract: list[dict[str, Any]],
    router: list[dict[str, Any]],
    alpha3: list[dict[str, Any]],
    ppn: list[dict[str, Any]],
    r10: list[dict[str, Any]],
    y5_update: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    summary: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    text = f"""# 746 - Y5 R10 q_loc To PPN Or alpha3 Projection Map Contract

Start point: 745 showed that a unit `c_qM` smoke row is not automatically safe or fatal. It depends entirely on which observable projection `q_loc` actually feeds.

Current result: **the projection map is now componentwise, and alpha3 momentum-flux is selected as the next highest-pressure target if that projection exists**.

The core rule is:

```text
q_loc^nu -> {{delta_gamma_q, delta_beta_q, alpha1_q, alpha2_q, alpha3_q, xi_q, alpha_q(lambda)}}
```

There is no legal single scalar pass. Beta/gamma remain interesting because the old compact-shell number is below their naive locks if the normalization matched. But alpha3 is the dragon: if `q_loc` has a momentum-flux/preferred-frame projection, the product must satisfy

```text
alpha3_q = W_q_alpha3 * epsilon_q_momentum
|alpha3_q| <= {ALPHA3_BOUND:.1e}
```

No such zero theorem or product row exists yet.

## Summary

| Field | Value |
| --- | --- |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Main result | q_loc projection map contract written; alpha3 branch selected if momentum projection applies |
| Next target | `{NEXT_TARGET}` |

## Projection Contract

{markdown_table(contract, ["contract_id", "clause", "mathematical_form", "required_inputs", "current_status", "claim_effect", "valid_for_claim"])}

## Channel Router

{markdown_table(router, ["route_id", "target", "condition", "known_pressure", "current_result", "missing", "priority", "valid_for_claim"])}

## Alpha3 Momentum-Flux Gate

{markdown_table(alpha3, ["gate_id", "target", "formula", "current_status", "blocker", "acceptance", "valid_for_claim"])}

## PPN Scalar/Vector Gate

{markdown_table(ppn, ["gate_id", "target", "formula", "current_status", "known_pressure", "missing", "valid_for_claim"])}

## R10 Range Gate

{markdown_table(r10, ["gate_id", "target", "formula", "current_status", "missing", "valid_for_claim"])}

## Y5 Runner Update

{markdown_table(y5_update, ["runner_id", "source_row", "status_after_746", "zero_or_input", "still_missing", "valid_for_claim"])}

## Decisions

{markdown_table(decisions, ["decision_id", "decision", "meaning", "claim_status", "next_target", "valid_for_claim"])}

## Route Update

{markdown_table(routes, ["route_id", "allowed_after_746", "forbidden_after_746", "next_action", "valid_for_claim"])}

## Source Register

{markdown_table(sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}

## Plain-English Verdict

This gets us out of scalar fog. `q_loc` is not one number anymore; it has to pick a lane. If it lands in beta/gamma, the old smoke number is not terrifying, though still unclaimable. If it lands in alpha3/preferred-frame momentum flux, it is under the nastiest microscope in the whole local branch. So the best next attack is not R10 and not broad PPN: prove the `q_loc` momentum-flux projection is zero, or write the actual `W_q_alpha3 epsilon_q_momentum` product and face the bound.
"""
    OUTPUT_DOC.write_text(text, encoding="utf-8")


def main() -> None:
    generated_utc = utc_stamp()
    sources = make_source_register(generated_utc)
    contract = projection_contract_rows(generated_utc)
    router = channel_router_rows(generated_utc)
    alpha3 = alpha3_gate_rows(generated_utc)
    ppn = ppn_gate_rows(generated_utc)
    r10 = r10_gate_rows(generated_utc)
    y5_update = y5_update_rows(generated_utc)
    decisions = decision_rows(generated_utc)
    routes = route_rows(generated_utc)
    summary = summary_rows(generated_utc)
    outputs = [
        OUTPUT_DOC,
        SOURCE_REGISTER_PATH,
        PROJECTION_CONTRACT_PATH,
        CHANNEL_ROUTER_PATH,
        ALPHA3_GATE_PATH,
        PPN_GATE_PATH,
        R10_GATE_PATH,
        Y5_UPDATE_PATH,
        DECISION_PATH,
        ROUTE_PATH,
        SUMMARY_PATH,
        VALIDATION_PATH,
    ]
    validation = make_validation(sources, contract, router, alpha3, ppn, r10, y5_update, decisions, routes, outputs)

    write_csv(SOURCE_REGISTER_PATH, sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(PROJECTION_CONTRACT_PATH, contract, ["contract_id", "clause", "mathematical_form", "required_inputs", "current_status", "claim_effect", "valid_for_claim", "generated_utc"])
    write_csv(CHANNEL_ROUTER_PATH, router, ["route_id", "target", "condition", "known_pressure", "current_result", "missing", "priority", "valid_for_claim", "generated_utc"])
    write_csv(ALPHA3_GATE_PATH, alpha3, ["gate_id", "target", "formula", "current_status", "blocker", "acceptance", "valid_for_claim", "generated_utc"])
    write_csv(PPN_GATE_PATH, ppn, ["gate_id", "target", "formula", "current_status", "known_pressure", "missing", "valid_for_claim", "generated_utc"])
    write_csv(R10_GATE_PATH, r10, ["gate_id", "target", "formula", "current_status", "missing", "valid_for_claim", "generated_utc"])
    write_csv(Y5_UPDATE_PATH, y5_update, ["runner_id", "source_row", "status_after_746", "zero_or_input", "still_missing", "valid_for_claim", "generated_utc"])
    write_csv(DECISION_PATH, decisions, ["decision_id", "decision", "meaning", "claim_status", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(ROUTE_PATH, routes, ["route_id", "allowed_after_746", "forbidden_after_746", "next_action", "valid_for_claim", "generated_utc"])
    write_csv(SUMMARY_PATH, summary, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])
    build_doc(sources, contract, router, alpha3, ppn, r10, y5_update, decisions, routes, summary, validation)

    failures = [row for row in validation if row["result"] != "pass"]
    print(f"wrote={OUTPUT_DOC}")
    print(f"validation_rows={len(validation)}")
    print(f"validation_failures={len(failures)}")
    if failures:
        for failure in failures:
            print(f"FAIL {failure['check_id']}: {failure['detail']}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
