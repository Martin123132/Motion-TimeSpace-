from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "epsilon-loc-local-bound-runner"
STATUS = "epsilon_loc_local_bound_runner_beta_guard_2_ready_no_local_GR_promotion"
CLAIM_CEILING = "symbolic_proxy_local_bound_runner_no_official_PPN_or_local_GR_claim"


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
        (ROOT / "227-local-PPN-coefficient-map-or-official-bound-manifest.md", "official-bound manifest and coefficient readiness"),
        (ROOT / "299-local-silence-selector-attempt.md", "epsilon_loc contract"),
        (ROOT / "300-boundary-state-local-silence-theorem-attempt.md", "IR boundary selector and next runner target"),
        (ROOT / "303-second-order-beta-response-attempt.md", "beta guard update: c_beta=2 unless B=A^2 is derived"),
        (ROOT / "scripts" / "epsilon_loc_local_bound_runner.py", "this local-bound runner"),
    ]
    return [{"source": relpath(path), "role": role, "exists": "yes" if path.exists() else "no"} for path, role in sources]


def bound_manifest_rows() -> list[dict[str, Any]]:
    return [
        {
            "channel": "gamma_minus_1",
            "proxy_bound": 2.3e-5,
            "source_label": "Cassini gamma scale from checkpoint 227 manifest",
            "claim_policy": "proxy only until MTS coefficient map is parent-derived",
        },
        {
            "channel": "beta_minus_1",
            "proxy_bound": 7.8e-5,
            "source_label": "PPN beta scale from checkpoint 227 manifest",
            "claim_policy": "proxy only; beta coefficient remains open",
        },
        {
            "channel": "alpha_clock",
            "proxy_bound": 2.48e-5,
            "source_label": "Galileo redshift/LPI scale from checkpoint 227 manifest",
            "claim_policy": "proxy only unless direct clock coupling is derived",
        },
        {
            "channel": "epsilon_matter",
            "proxy_bound": 2.3e-15,
            "source_label": "MICROSCOPE WEP scale from checkpoint 227 manifest",
            "claim_policy": "only applies if open sector creates direct composition-dependent coupling",
        },
    ]


def coefficient_policy_rows() -> list[dict[str, Any]]:
    return [
        {
            "policy": "scalar_metric_proxy",
            "c_gamma": 1.0,
            "c_beta": 2.0,
            "c_clock": 0.0,
            "c_matter": 0.0,
            "status": "proxy_conservative_for_gamma_beta_guard_2_no_direct_clock_or_matter",
            "claim_limit": "not parent-derived",
        },
        {
            "policy": "common_mode_contract",
            "c_gamma": 0.0,
            "c_beta": 2.0,
            "c_clock": 0.0,
            "c_matter": 0.0,
            "status": "uses_common_mode_gamma_zero_with_beta_guard_2_from_checkpoint_303",
            "claim_limit": "not parent-derived; beta remains active unless B=A^2",
        },
        {
            "policy": "direct_matter_stress_test",
            "c_gamma": 1.0,
            "c_beta": 2.0,
            "c_clock": 1.0,
            "c_matter": 1.0,
            "status": "deliberately_harsh_fail_probe",
            "claim_limit": "tests why direct matter coupling is dangerous",
        },
        {
            "policy": "exact_silence",
            "c_gamma": 1.0,
            "c_beta": 1.0,
            "c_clock": 1.0,
            "c_matter": 1.0,
            "status": "coefficients_irrelevant_if_epsilon_loc_zero",
            "claim_limit": "requires selector zero theorem",
        },
    ]


def candidate_rows() -> list[dict[str, Any]]:
    return [
        {
            "case": "local_bath_absent_exact",
            "domain_class": "local_bound",
            "b_D": 0.0,
            "c_D": 1.0,
            "mu2": 1.0,
            "Lambda_open": 1.0,
            "trace_charge": 1.0,
            "policy": "exact_silence",
            "purpose": "exact silence because IR bath strength vanishes",
        },
        {
            "case": "local_relative_class_trivial_exact",
            "domain_class": "local_bound",
            "b_D": 1.0,
            "c_D": 0.0,
            "mu2": 1.0,
            "Lambda_open": 1.0,
            "trace_charge": 1.0,
            "policy": "exact_silence",
            "purpose": "exact silence because relative class vanishes",
        },
        {
            "case": "local_tiny_selector_scalar_proxy",
            "domain_class": "local_bound",
            "b_D": 1.0e-8,
            "c_D": 1.0e-2,
            "mu2": 1.0,
            "Lambda_open": 1.0,
            "trace_charge": 1.0,
            "policy": "scalar_metric_proxy",
            "purpose": "small nonzero selector should pass proxy gamma/beta gates",
        },
        {
            "case": "local_beta_edge_common_mode",
            "domain_class": "local_bound",
            "b_D": 7.0e-5,
            "c_D": 1.0,
            "mu2": 1.0,
            "Lambda_open": 1.0,
            "trace_charge": 1.0,
            "policy": "common_mode_contract",
            "purpose": "old near-edge case now fails under beta guard 2 unless B=A^2 is derived",
        },
        {
            "case": "local_beta_guard2_bounded_common_mode",
            "domain_class": "local_bound",
            "b_D": 3.0e-5,
            "c_D": 1.0,
            "mu2": 1.0,
            "Lambda_open": 1.0,
            "trace_charge": 1.0,
            "policy": "common_mode_contract",
            "purpose": "nonzero common-mode leakage that survives the updated beta guard 2",
        },
        {
            "case": "local_proxy_fail",
            "domain_class": "local_bound",
            "b_D": 1.0e-3,
            "c_D": 1.0,
            "mu2": 1.0,
            "Lambda_open": 1.0,
            "trace_charge": 1.0,
            "policy": "scalar_metric_proxy",
            "purpose": "deliberately too large for local proxy bounds",
        },
        {
            "case": "direct_matter_tiny_fail_probe",
            "domain_class": "local_bound",
            "b_D": 1.0e-14,
            "c_D": 1.0,
            "mu2": 1.0,
            "Lambda_open": 1.0,
            "trace_charge": 1.0,
            "policy": "direct_matter_stress_test",
            "purpose": "shows WEP/direct matter gate is brutally tight",
        },
        {
            "case": "FLRW_active_control_not_local",
            "domain_class": "FLRW_control",
            "b_D": 1.0,
            "c_D": 1.0,
            "mu2": 1.0,
            "Lambda_open": 1.0,
            "trace_charge": 1.0,
            "policy": "scalar_metric_proxy",
            "purpose": "active cosmological branch control; not a local pass/fail claim",
        },
    ]


def coefficient_map() -> dict[str, dict[str, float]]:
    return {
        row["policy"]: {
            "gamma_minus_1": float(row["c_gamma"]),
            "beta_minus_1": float(row["c_beta"]),
            "alpha_clock": float(row["c_clock"]),
            "epsilon_matter": float(row["c_matter"]),
        }
        for row in coefficient_policy_rows()
    }


def bound_map() -> dict[str, float]:
    return {row["channel"]: float(row["proxy_bound"]) for row in bound_manifest_rows()}


def sigma_value(b_d: float, c_d: float, mu2: float) -> float:
    product = b_d * c_d
    if product <= 0.0:
        return 0.0
    return product / (product + mu2)


def epsilon_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for candidate in candidate_rows():
        sigma = sigma_value(float(candidate["b_D"]), float(candidate["c_D"]), float(candidate["mu2"]))
        epsilon = abs(sigma * float(candidate["Lambda_open"]) * float(candidate["trace_charge"]))
        if candidate["domain_class"] != "local_bound":
            status = "not_local_control"
        elif epsilon == 0.0:
            status = "exact_silence_pass"
        else:
            status = "requires_proxy_bound_check"
        rows.append(
            {
                **candidate,
                "sigma_D": sigma,
                "epsilon_loc": epsilon,
                "epsilon_status": status,
            }
        )
    return rows


def residual_rows(epsilon_result_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    coefficients = coefficient_map()
    bounds = bound_map()
    rows: list[dict[str, Any]] = []
    for result in epsilon_result_rows:
        policy_coefficients = coefficients[result["policy"]]
        for channel, coefficient in policy_coefficients.items():
            residual = abs(float(result["epsilon_loc"]) * coefficient)
            bound = bounds[channel]
            if result["domain_class"] != "local_bound":
                status = "not_local_control"
            elif residual == 0.0:
                status = "pass_exact_zero"
            elif residual <= bound:
                status = "pass_proxy_bound"
            else:
                status = "fail_proxy_bound"
            rows.append(
                {
                    "case": result["case"],
                    "domain_class": result["domain_class"],
                    "policy": result["policy"],
                    "channel": channel,
                    "epsilon_loc": result["epsilon_loc"],
                    "coefficient": coefficient,
                    "residual": residual,
                    "proxy_bound": bound,
                    "residual_over_bound": "" if bound == 0.0 else residual / bound,
                    "status": status,
                }
            )
    return rows


def case_summary_rows(epsilon_result_rows: list[dict[str, Any]], channel_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for result in epsilon_result_rows:
        related = [row for row in channel_rows if row["case"] == result["case"]]
        failures = [row for row in related if row["status"] == "fail_proxy_bound"]
        exact_passes = [row for row in related if row["status"] == "pass_exact_zero"]
        proxy_passes = [row for row in related if row["status"] == "pass_proxy_bound"]
        if result["domain_class"] != "local_bound":
            case_status = "not_local_control"
        elif failures:
            case_status = "fail_proxy_local_bound"
        elif exact_passes and len(exact_passes) == len(related):
            case_status = "pass_exact_silence"
        elif proxy_passes or exact_passes:
            case_status = "pass_proxy_local_bound"
        else:
            case_status = "undetermined"
        rows.append(
            {
                "case": result["case"],
                "domain_class": result["domain_class"],
                "policy": result["policy"],
                "sigma_D": result["sigma_D"],
                "epsilon_loc": result["epsilon_loc"],
                "case_status": case_status,
                "failed_channels": ";".join(row["channel"] for row in failures),
                "claim_limit": "proxy runner only; coefficients/manifest not parent-derived",
            }
        )
    return rows


def gate_rows(case_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    exact_cases = [row for row in case_rows if row["case_status"] == "pass_exact_silence"]
    proxy_pass_cases = [row for row in case_rows if row["case_status"] == "pass_proxy_local_bound"]
    fail_cases = [row for row in case_rows if row["case_status"] == "fail_proxy_local_bound"]
    return [
        {
            "gate": "source_paths_exist",
            "status": "pass" if all(row["exists"] == "yes" for row in source_register_rows()) else "fail",
            "evidence": "all cited checkpoints/scripts exist",
            "claim_effect": "runner traceable",
        },
        {
            "gate": "epsilon_runner_constructed",
            "status": "pass",
            "evidence": "sigma_D and epsilon_loc are computed for exact, bounded, fail, and FLRW-control cases",
            "claim_effect": "local selector now faces a quantitative gate",
        },
        {
            "gate": "exact_silence_cases_pass",
            "status": "pass" if len(exact_cases) >= 2 else "fail",
            "evidence": ";".join(row["case"] for row in exact_cases),
            "claim_effect": "sigma_D=0 gives zero residual as expected",
        },
        {
            "gate": "proxy_bounded_case_exists",
            "status": "pass" if proxy_pass_cases else "fail",
            "evidence": ";".join(row["case"] for row in proxy_pass_cases),
            "claim_effect": "nonzero selector can be tested against proxy bounds",
        },
        {
            "gate": "beta_guard_2_active",
            "status": "pass",
            "evidence": "scalar_metric_proxy/common_mode_contract/direct_matter_stress_test use c_beta=2 unless exact silence or B=A^2",
            "claim_effect": "checkpoint 303 linear-only beta risk is now represented in the runner",
        },
        {
            "gate": "failure_probes_fail",
            "status": "pass" if {"local_proxy_fail", "direct_matter_tiny_fail_probe"}.issubset({row["case"] for row in fail_cases}) else "fail",
            "evidence": ";".join(row["case"] + ":" + row["failed_channels"] for row in fail_cases),
            "claim_effect": "runner is not rubber-stamping MTS",
        },
        {
            "gate": "official_PPN_claim_allowed",
            "status": "fail",
            "evidence": "coefficients and bounds are proxy/manifest-level, not parent-derived official local solution",
            "claim_effect": "no local-GR claim",
        },
        {
            "gate": "local_GR_promoted",
            "status": "fail",
            "evidence": "exact silence needs selector theorem; bounded cases use proxy coefficients",
            "claim_effect": "local branch remains unpromoted",
        },
        {
            "gate": "B_mem_parent_derived",
            "status": "fail",
            "evidence": "epsilon_loc runner only tests local residuals; it does not derive 2/27",
            "claim_effect": "amplitude remains closure/theorem target",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "meaning": (
                "The epsilon_loc runner now converts the local selector contract into a quantitative gate. "
                "Exact selector silence passes with zero residual, small nonzero selectors can be tested against proxy "
                "PPN-style bounds, deliberate fail probes fail, and the beta guard is updated to |c_beta|=2 unless "
                "the parent proves B=A^2. The runner is not an official PPN proof because the MTS residual coefficients "
                "and selector theorem are not parent-derived."
            ),
            "next_target": "build_fifth_force_gradient_runner_for_nonzero_epsilon_loc",
        }
    ]


def build_outputs(timestamp: str) -> dict[str, Any]:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)
    eps_rows = epsilon_rows()
    channel_rows = residual_rows(eps_rows)
    summary_rows = case_summary_rows(eps_rows, channel_rows)
    outputs = {
        "source_register.csv": (source_register_rows(), ["source", "role", "exists"]),
        "bound_manifest_proxy.csv": (
            bound_manifest_rows(),
            ["channel", "proxy_bound", "source_label", "claim_policy"],
        ),
        "coefficient_policies.csv": (
            coefficient_policy_rows(),
            ["policy", "c_gamma", "c_beta", "c_clock", "c_matter", "status", "claim_limit"],
        ),
        "candidate_domains.csv": (
            candidate_rows(),
            ["case", "domain_class", "b_D", "c_D", "mu2", "Lambda_open", "trace_charge", "policy", "purpose"],
        ),
        "epsilon_results.csv": (
            eps_rows,
            ["case", "domain_class", "b_D", "c_D", "mu2", "Lambda_open", "trace_charge", "policy", "purpose", "sigma_D", "epsilon_loc", "epsilon_status"],
        ),
        "residual_channel_results.csv": (
            channel_rows,
            ["case", "domain_class", "policy", "channel", "epsilon_loc", "coefficient", "residual", "proxy_bound", "residual_over_bound", "status"],
        ),
        "case_summary.csv": (
            summary_rows,
            ["case", "domain_class", "policy", "sigma_D", "epsilon_loc", "case_status", "failed_channels", "claim_limit"],
        ),
        "promotion_gates.csv": (
            gate_rows(summary_rows),
            ["gate", "status", "evidence", "claim_effect"],
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
        "exact_silence_cases_pass": True,
        "proxy_bounds_exercised": True,
        "failure_probes_fail": True,
        "official_PPN_claim_now": False,
        "local_GR_promoted_now": False,
        "B_mem_parent_derived_now": False,
        "next_target": "build_fifth_force_gradient_runner_for_nonzero_epsilon_loc",
    }
    write_json(run_dir / "status.json", payload)
    (run_dir / "DONE.txt").write_text(STATUS + "\n", encoding="utf-8")
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="epsilon_loc local-bound proxy runner.")
    parser.add_argument("--timestamp", default=datetime.now().strftime("%Y%m%d-%H%M%S"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = build_outputs(args.timestamp)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
