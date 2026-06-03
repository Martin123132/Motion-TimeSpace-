from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "epsilon-loc-parent-coefficient-map-attempt"
STATUS = "epsilon_loc_parent_coefficients_partially_derived_common_mode_beta_and_fifth_force_open"
CLAIM_CEILING = "partial_coefficient_map_no_official_PPN_or_local_GR_promotion"


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def relpath(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def source_register_rows() -> list[dict[str, Any]]:
    sources = [
        (ROOT / "227-local-PPN-coefficient-map-or-official-bound-manifest.md", "common-mode coefficient contract and official-bound manifest"),
        (ROOT / "298-open-boundary-parent-sector-attempt.md", "trace-only open sector source construction"),
        (ROOT / "299-local-silence-selector-attempt.md", "epsilon_loc definition and PPN contract"),
        (ROOT / "301-epsilon-loc-local-bound-runner.md", "epsilon_loc runner and proxy policies"),
        (ROOT / "runs" / "20260601-000124-epsilon-loc-local-bound-runner" / "results" / "coefficient_policies.csv", "checkpoint 301 proxy coefficient policies"),
    ]
    return [{"source": relpath(path), "role": role, "exists": "yes" if path.exists() else "no"} for path, role in sources]


def coefficient_derivation_rows() -> list[dict[str, Any]]:
    return [
        {
            "channel": "gamma_minus_1",
            "coefficient": 0.0,
            "status": "conditional_derived_zero",
            "derivation": "trace-only source gives deltaPhi=deltaPsi at leading weak-field order, so gamma=Psi/Phi remains 1",
            "assumptions": "universal metric coupling; no local anisotropic stress; no R_aniso source leakage",
            "blocker": "full local metric solution/Bianchi identity still missing",
            "runner_policy": "common_mode_contract",
        },
        {
            "channel": "metric_slip_Phi_minus_Psi",
            "coefficient": 0.0,
            "status": "conditional_derived_zero",
            "derivation": "scalar trace source has no trace-free spatial stress in the effective open sector",
            "assumptions": "Ward trace coupling only; anisotropic residual decays or is unsourced",
            "blocker": "anisotropic perturbation sector not solved",
            "runner_policy": "not_in_301_manifest",
        },
        {
            "channel": "alpha_clock",
            "coefficient": 0.0,
            "status": "conditional_contract_zero",
            "derivation": "clock rates follow the same metric if no direct clock-sector coupling exists",
            "assumptions": "universal metric coupling and no explicit clock coupling to q_r/J_B",
            "blocker": "matter/clock action not yet fully varied",
            "runner_policy": "common_mode_contract",
        },
        {
            "channel": "epsilon_matter",
            "coefficient": 0.0,
            "status": "conditional_contract_zero",
            "derivation": "composition dependence is absent if matter couples only through the metric/coframe",
            "assumptions": "no direct composition-dependent coupling to open-sector variables",
            "blocker": "universal matter coupling is still a parent-action contract",
            "runner_policy": "common_mode_contract",
        },
        {
            "channel": "beta_minus_1",
            "coefficient": 1.0,
            "status": "safety_proxy_not_derived",
            "derivation": "second-order temporal metric response is not derived; runner should keep beta active as conservative guard",
            "assumptions": "none strong enough for promotion",
            "blocker": "needs second-order weak-field solution for the trace source",
            "runner_policy": "common_mode_contract_beta_guard",
        },
        {
            "channel": "fifth_force_gradient",
            "coefficient": 1.0,
            "status": "safety_proxy_not_derived",
            "derivation": "a spatially varying local trace source could generate an extra force unless sigma_D=0 or gradients vanish",
            "assumptions": "exact silence or constant/unobservable local trace source",
            "blocker": "needs local field profile and gradient bound",
            "runner_policy": "future_epsilon_gradient_runner",
        },
        {
            "channel": "G_eff_common_rescaling",
            "coefficient": 1.0,
            "status": "proxy_interpretation",
            "derivation": "common-mode trace source may appear as local Newtonian-strength renormalization rather than PPN slip",
            "assumptions": "source is universal and compact/local",
            "blocker": "must be separated from fitted GM and ephemeris constraints",
            "runner_policy": "future_Geff_runner",
        },
    ]


def metric_response_case_rows() -> list[dict[str, Any]]:
    return [
        {
            "case": "exact_selector_silence",
            "condition": "sigma_D=0",
            "gamma_status": "zero",
            "beta_status": "zero",
            "clock_status": "zero",
            "matter_status": "zero",
            "promotion": "conditional_exact_if_selector_theorem_is_derived",
        },
        {
            "case": "trace_only_common_mode",
            "condition": "deltaPhi=deltaPsi and no direct matter/clock coupling",
            "gamma_status": "zero_leading_order",
            "beta_status": "open_second_order",
            "clock_status": "zero_by_contract",
            "matter_status": "zero_by_contract",
            "promotion": "best_current_nonzero_leakage_policy",
        },
        {
            "case": "anisotropic_stress_leakage",
            "condition": "deltaPhi != deltaPsi or R_aniso sources local stress",
            "gamma_status": "active_fail_risk",
            "beta_status": "active",
            "clock_status": "depends_on_coupling",
            "matter_status": "depends_on_coupling",
            "promotion": "rejected_unless_bounded",
        },
        {
            "case": "direct_matter_or_clock_coupling",
            "condition": "q_r/J_B couples directly to matter species or clocks",
            "gamma_status": "active_or_indirect",
            "beta_status": "active_or_indirect",
            "clock_status": "active",
            "matter_status": "active",
            "promotion": "dangerous_WEP_LPI_fail_risk",
        },
    ]


def runner_policy_rows() -> list[dict[str, Any]]:
    return [
        {
            "policy": "recommended_current_policy",
            "c_gamma": 0.0,
            "c_beta": 1.0,
            "c_clock": 0.0,
            "c_matter": 0.0,
            "c_fifth_force": 1.0,
            "status": "common_mode_with_beta_and_gradient_guards",
            "claim_limit": "usable for internal gate only; not official PPN",
        },
        {
            "policy": "promotion_policy_required",
            "c_gamma": 0.0,
            "c_beta": "derived_second_order_value_required",
            "c_clock": 0.0,
            "c_matter": 0.0,
            "c_fifth_force": "derived_gradient_value_required",
            "status": "not_available_yet",
            "claim_limit": "required before any local-GR promotion",
        },
        {
            "policy": "exact_silence_policy",
            "c_gamma": "irrelevant",
            "c_beta": "irrelevant",
            "c_clock": "irrelevant",
            "c_matter": "irrelevant",
            "c_fifth_force": "irrelevant",
            "status": "valid_if_sigma_D_zero_theorem_is_derived",
            "claim_limit": "depends entirely on selector theorem",
        },
    ]


def coefficient_gate_rows() -> list[dict[str, Any]]:
    source_missing = [source for source in source_register_rows() if source["exists"] != "yes"]
    return [
        {
            "gate": "source_paths_exist",
            "status": "pass" if not source_missing else "fail",
            "evidence": "all cited checkpoint inputs exist" if not source_missing else ";".join(source["source"] for source in source_missing),
            "claim_effect": "attempt traceable",
        },
        {
            "gate": "gamma_coefficient_derived",
            "status": "conditional_pass",
            "evidence": "c_gamma=0 for trace-only common-mode response",
            "claim_effect": "leading gamma/slip danger can be neutralized if trace-only source is parent-owned",
        },
        {
            "gate": "clock_matter_coefficients_zero",
            "status": "conditional_pass",
            "evidence": "c_clock=c_matter=0 under universal metric coupling",
            "claim_effect": "direct WEP/LPI failures avoided only by coupling contract",
        },
        {
            "gate": "beta_coefficient_derived",
            "status": "fail",
            "evidence": "second-order weak-field temporal response not derived",
            "claim_effect": "beta remains active safety guard",
        },
        {
            "gate": "fifth_force_gradient_derived",
            "status": "fail",
            "evidence": "local trace-source gradient profile not solved",
            "claim_effect": "bounded leakage still needs gradient/fifth-force runner",
        },
        {
            "gate": "official_PPN_claim_allowed",
            "status": "fail",
            "evidence": "coefficient map is conditional and incomplete",
            "claim_effect": "no local-GR/PPN promotion",
        },
        {
            "gate": "epsilon_runner_policy_improved",
            "status": "pass",
            "evidence": "recommended policy now uses c_gamma=0, c_beta=1 guard, c_clock=0, c_matter=0, fifth-force guard",
            "claim_effect": "future local-bound runner can be less toy-like but still conservative",
        },
        {
            "gate": "B_mem_parent_derived",
            "status": "fail",
            "evidence": "coefficient map does not derive amplitude",
            "claim_effect": "2/27 remains closure/theorem target",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "priority": 1,
            "target": "second_order_beta_solution",
            "task": "derive local weak-field g_00 at second order for trace-only epsilon_loc source",
            "success_gate": "c_beta is derived rather than guarded by proxy c_beta=1",
        },
        {
            "priority": 2,
            "target": "fifth_force_gradient_runner",
            "task": "bound grad(Lambda_D Tr(P_iso q_r)) for nonzero local selectors",
            "success_gate": "nonzero selector leakage is below local fifth-force constraints or requires exact silence",
        },
        {
            "priority": 3,
            "target": "update_epsilon_runner_policy",
            "task": "add recommended_current_policy to epsilon_loc runner",
            "success_gate": "runner reports common-mode gamma zero with beta/fifth-force guards",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "meaning": (
                "The epsilon_loc coefficient map is partially improved: trace-only common-mode response gives c_gamma=0 "
                "at leading order, and universal metric coupling gives c_clock=c_matter=0 by contract. But c_beta is not "
                "derived because the second-order weak-field response is missing, and fifth-force gradients remain open "
                "for nonzero local selectors. Therefore the local runner can be improved, but local GR is still unpromoted."
            ),
            "next_target": "second_order_beta_solution_or_fifth_force_gradient_runner",
        }
    ]


def build_outputs(timestamp: str) -> dict[str, Any]:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    outputs = {
        "source_register.csv": (source_register_rows(), ["source", "role", "exists"]),
        "coefficient_derivation.csv": (
            coefficient_derivation_rows(),
            ["channel", "coefficient", "status", "derivation", "assumptions", "blocker", "runner_policy"],
        ),
        "metric_response_cases.csv": (
            metric_response_case_rows(),
            ["case", "condition", "gamma_status", "beta_status", "clock_status", "matter_status", "promotion"],
        ),
        "recommended_runner_policies.csv": (
            runner_policy_rows(),
            ["policy", "c_gamma", "c_beta", "c_clock", "c_matter", "c_fifth_force", "status", "claim_limit"],
        ),
        "coefficient_gates.csv": (
            coefficient_gate_rows(),
            ["gate", "status", "evidence", "claim_effect"],
        ),
        "next_targets.csv": (
            next_target_rows(),
            ["priority", "target", "task", "success_gate"],
        ),
        "decision.csv": (
            decision_rows(),
            ["decision", "claim_ceiling", "meaning", "next_target"],
        ),
    }
    for filename, (rows, fieldnames) in outputs.items():
        write_csv(results_dir / filename, rows, fieldnames)

    payload = {
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "generated": list(outputs),
        "gamma_coefficient_conditionally_zero": True,
        "clock_matter_coefficients_conditionally_zero": True,
        "beta_coefficient_derived_now": False,
        "fifth_force_gradient_derived_now": False,
        "local_GR_promoted_now": False,
        "B_mem_parent_derived_now": False,
        "next_target": "second_order_beta_solution_or_fifth_force_gradient_runner",
    }
    write_json(run_dir / "status.json", payload)
    (run_dir / "DONE.txt").write_text(STATUS + "\n", encoding="utf-8")
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="epsilon_loc parent coefficient map attempt.")
    parser.add_argument("--timestamp", default=datetime.now().strftime("%Y%m%d-%H%M%S"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = build_outputs(args.timestamp)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
