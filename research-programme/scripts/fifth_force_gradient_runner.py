from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "fifth-force-gradient-runner"
STATUS = "fifth_force_gradient_runner_ready_nonzero_epsilon_requires_flat_profile_no_local_GR_promotion"
CLAIM_CEILING = "proxy_gradient_bound_runner_no_official_fifth_force_or_local_GR_claim"


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
        (ROOT / "301-epsilon-loc-local-bound-runner.md", "epsilon_loc local-bound runner"),
        (ROOT / "304-epsilon-loc-beta-guard-update.md", "updated beta guard and next fifth-force target"),
        (ROOT / "runs" / "20260601-000127-epsilon-loc-local-bound-runner" / "results" / "case_summary.csv", "updated epsilon local cases"),
        (ROOT / "scripts" / "fifth_force_gradient_runner.py", "this gradient runner"),
    ]
    return [{"source": relpath(path), "role": role, "exists": "yes" if path.exists() else "no"} for path, role in sources]


def bound_manifest_rows() -> list[dict[str, Any]]:
    return [
        {
            "bound_name": "cassini_scale_proxy",
            "accel_ratio_bound": 2.3e-5,
            "source": "Cassini gamma scale reused only as a weak proxy",
            "claim_policy": "not an official fifth-force bound",
        },
        {
            "bound_name": "strict_internal_proxy",
            "accel_ratio_bound": 1.0e-8,
            "source": "internal stress-test scale",
            "claim_policy": "sanity check for profile flatness, not external evidence",
        },
    ]


def candidate_profile_rows() -> list[dict[str, Any]]:
    return [
        {
            "case": "exact_silence_no_gradient",
            "domain_class": "local_bound",
            "epsilon_loc": 0.0,
            "test_scale_L": 1.0,
            "profile_scale_L": 1.0,
            "shape_factor": 1.0,
            "bound_name": "cassini_scale_proxy",
            "purpose": "exact silence control",
        },
        {
            "case": "constant_trace_source",
            "domain_class": "local_bound",
            "epsilon_loc": 3.0e-5,
            "test_scale_L": 1.0,
            "profile_scale_L": 1.0,
            "shape_factor": 0.0,
            "bound_name": "cassini_scale_proxy",
            "purpose": "nonzero epsilon but spatially constant source gives no fifth force",
        },
        {
            "case": "beta_bounded_flat_profile",
            "domain_class": "local_bound",
            "epsilon_loc": 3.0e-5,
            "test_scale_L": 1.0,
            "profile_scale_L": 1.0e4,
            "shape_factor": 1.0,
            "bound_name": "cassini_scale_proxy",
            "purpose": "bounded beta case with very flat profile",
        },
        {
            "case": "beta_bounded_profile_edge",
            "domain_class": "local_bound",
            "epsilon_loc": 3.0e-5,
            "test_scale_L": 1.0,
            "profile_scale_L": 1.5,
            "shape_factor": 1.0,
            "bound_name": "cassini_scale_proxy",
            "purpose": "near fifth-force edge for nonzero epsilon",
        },
        {
            "case": "beta_bounded_local_gradient_fail",
            "domain_class": "local_bound",
            "epsilon_loc": 3.0e-5,
            "test_scale_L": 1.0,
            "profile_scale_L": 1.0,
            "shape_factor": 1.0,
            "bound_name": "cassini_scale_proxy",
            "purpose": "same epsilon as beta-bounded case but locally varying profile",
        },
        {
            "case": "tiny_selector_strict_profile_pass",
            "domain_class": "local_bound",
            "epsilon_loc": 1.0e-10,
            "test_scale_L": 1.0,
            "profile_scale_L": 1.0,
            "shape_factor": 1.0,
            "bound_name": "strict_internal_proxy",
            "purpose": "tiny selector survives even strict internal gradient proxy",
        },
        {
            "case": "FLRW_control_not_local",
            "domain_class": "FLRW_control",
            "epsilon_loc": 0.5,
            "test_scale_L": 1.0,
            "profile_scale_L": 1.0,
            "shape_factor": 1.0,
            "bound_name": "cassini_scale_proxy",
            "purpose": "cosmology branch control is not a local fifth-force claim",
        },
    ]


def bound_map() -> dict[str, float]:
    return {row["bound_name"]: float(row["accel_ratio_bound"]) for row in bound_manifest_rows()}


def gradient_result_rows() -> list[dict[str, Any]]:
    bounds = bound_map()
    rows: list[dict[str, Any]] = []
    for candidate in candidate_profile_rows():
        epsilon_loc = float(candidate["epsilon_loc"])
        test_scale = float(candidate["test_scale_L"])
        profile_scale = float(candidate["profile_scale_L"])
        shape_factor = float(candidate["shape_factor"])
        bound = bounds[candidate["bound_name"]]
        gradient_ratio = abs(epsilon_loc * shape_factor * test_scale / profile_scale)
        if candidate["domain_class"] != "local_bound":
            status = "not_local_control"
        elif gradient_ratio == 0.0:
            status = "pass_exact_zero_gradient"
        elif gradient_ratio <= bound:
            status = "pass_proxy_gradient_bound"
        else:
            status = "fail_proxy_gradient_bound"
        required_profile_scale = "infinite_or_constant" if shape_factor == 0.0 or bound == 0.0 else abs(epsilon_loc * shape_factor * test_scale / bound)
        rows.append(
            {
                **candidate,
                "gradient_accel_ratio": gradient_ratio,
                "proxy_bound": bound,
                "ratio_over_bound": "" if bound == 0.0 else gradient_ratio / bound,
                "required_profile_scale_for_pass": required_profile_scale,
                "status": status,
            }
        )
    return rows


def gate_rows(results: list[dict[str, Any]]) -> list[dict[str, Any]]:
    exact = [row for row in results if row["status"] == "pass_exact_zero_gradient"]
    proxy_pass = [row for row in results if row["status"] == "pass_proxy_gradient_bound"]
    failures = [row for row in results if row["status"] == "fail_proxy_gradient_bound"]
    return [
        {
            "gate": "source_paths_exist",
            "status": "pass" if all(row["exists"] == "yes" for row in source_register_rows()) else "fail",
            "evidence": "all cited checkpoints/scripts exist",
            "claim_effect": "runner traceable",
        },
        {
            "gate": "gradient_runner_constructed",
            "status": "pass",
            "evidence": "gradient_accel_ratio=epsilon_loc*shape_factor*L_test/L_profile",
            "claim_effect": "nonzero epsilon now faces a spatial-gradient gate",
        },
        {
            "gate": "exact_or_constant_sources_pass",
            "status": "pass" if {"exact_silence_no_gradient", "constant_trace_source"}.issubset({row["case"] for row in exact}) else "fail",
            "evidence": ";".join(row["case"] for row in exact),
            "claim_effect": "zero gradient is safe in this proxy runner",
        },
        {
            "gate": "flat_profile_pass_exists",
            "status": "pass" if any(row["case"] == "beta_bounded_flat_profile" for row in proxy_pass) else "fail",
            "evidence": ";".join(row["case"] for row in proxy_pass),
            "claim_effect": "nonzero epsilon can pass only if profile is sufficiently flat/small",
        },
        {
            "gate": "local_gradient_failure_probe_fails",
            "status": "pass" if any(row["case"] == "beta_bounded_local_gradient_fail" for row in failures) else "fail",
            "evidence": ";".join(row["case"] for row in failures),
            "claim_effect": "runner catches locally varying trace-source leakage",
        },
        {
            "gate": "official_fifth_force_claim_allowed",
            "status": "fail",
            "evidence": "bounds are proxy/internal scales and no official fifth-force manifest is used",
            "claim_effect": "no official local evidence claim",
        },
        {
            "gate": "local_GR_promoted",
            "status": "fail",
            "evidence": "profile shape and selector theorem are not parent-derived",
            "claim_effect": "local branch remains conditional",
        },
        {
            "gate": "B_mem_parent_derived",
            "status": "fail",
            "evidence": "gradient runner tests local residuals only",
            "claim_effect": "2/27 amplitude remains closure/theorem target",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "meaning": (
                "The fifth-force runner converts nonzero epsilon_loc into a proxy acceleration ratio "
                "epsilon_loc*shape_factor*L_test/L_profile. Exact silence and constant trace sources pass, "
                "very flat or tiny profiles can pass, and local-gradient fail probes fail. This is not an official "
                "fifth-force test because the profile, selector, and bounds are not parent-derived or official."
            ),
            "next_target": "derive_trace_source_profile_or_return_to_empirical_holdout",
        }
    ]


def build_outputs(timestamp: str) -> dict[str, Any]:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)
    gradient_rows = gradient_result_rows()
    outputs = {
        "source_register.csv": (source_register_rows(), ["source", "role", "exists"]),
        "bound_manifest_proxy.csv": (
            bound_manifest_rows(),
            ["bound_name", "accel_ratio_bound", "source", "claim_policy"],
        ),
        "candidate_profiles.csv": (
            candidate_profile_rows(),
            ["case", "domain_class", "epsilon_loc", "test_scale_L", "profile_scale_L", "shape_factor", "bound_name", "purpose"],
        ),
        "gradient_results.csv": (
            gradient_rows,
            ["case", "domain_class", "epsilon_loc", "test_scale_L", "profile_scale_L", "shape_factor", "bound_name", "purpose", "gradient_accel_ratio", "proxy_bound", "ratio_over_bound", "required_profile_scale_for_pass", "status"],
        ),
        "promotion_gates.csv": (
            gate_rows(gradient_rows),
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
        "gradient_runner_constructed": True,
        "failure_probes_fail": True,
        "official_fifth_force_claim_now": False,
        "local_GR_promoted_now": False,
        "B_mem_parent_derived_now": False,
        "next_target": "derive_trace_source_profile_or_return_to_empirical_holdout",
    }
    write_json(run_dir / "status.json", payload)
    (run_dir / "DONE.txt").write_text(STATUS + "\n", encoding="utf-8")
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fifth-force gradient proxy runner.")
    parser.add_argument("--timestamp", default=datetime.now().strftime("%Y%m%d-%H%M%S"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = build_outputs(args.timestamp)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
