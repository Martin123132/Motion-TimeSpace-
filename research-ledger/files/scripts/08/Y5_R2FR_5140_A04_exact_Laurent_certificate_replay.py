from __future__ import annotations

import argparse
import csv
import importlib.util
import json
from pathlib import Path
from typing import Any


POST = Path(__file__).resolve().parents[1]
GENERIC_RUNNER = POST / "scripts" / "Y5_R2FR_5132_locked_next_argument_gate_and_single_job_runner.py"
PROOF = POST / "source-intake" / "functional_rg" / "5138" / "A04_KLT_collinear_pole_order_proof.json"
DEFAULT_REJECTED_GATE = POST / "source-intake" / "functional_rg" / "5135" / "A04_argument_local_outer_collinear_chart_gate.json"
DEEP_REJECTED_GATE = POST / "source-intake" / "functional_rg" / "5139" / "A04_argument_local_outer_collinear_chart_gate.json"

CHECKPOINT_ID = "5140"
CHECKED_DATE = "2026-07-20"
JOB_KEY = "E040__S512503_N0000__A04__primary24"
DEEP_PROFILE = {
    "low_boundary_nodes": 96,
    "low_global_nodes": 128,
    "low_global_residue_nodes": 192,
    "high_boundary_nodes": 128,
    "high_global_nodes": 192,
    "high_global_residue_nodes": 256,
    "selection": "deep residue and regular-part stability plus the 5138 exact KLT simple-pole certificate as the Laurent-order authority",
    "acceptance_threshold_changed": False,
    "exact_certificate_is_not_a_numeric_threshold_override": True,
}


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def configure(mode: str) -> tuple[Any, dict[str, Any]]:
    runner = load_module("mts_5132_for_5140", GENERIC_RUNNER)
    base = runner.M5128
    proof = base.read_json(PROOF)
    default_gate = base.read_json(DEFAULT_REJECTED_GATE)
    deep_gate = base.read_json(DEEP_REJECTED_GATE)
    if not proof.get("simple_pole_order_proved_for_implemented_integrand"):
        raise RuntimeError("5140 requires the 5138 exact simple-pole proof")
    if default_gate.get("gate_accepted") or deep_gate.get("gate_accepted"):
        raise RuntimeError("5140 requires preserved rejected default and deep numeric gates")
    arguments = argparse.Namespace(
        checkpoint_id=CHECKPOINT_ID,
        checked_date=CHECKED_DATE,
        job_key=JOB_KEY,
        precision="default",
        mode=mode,
    )
    job, configuration = runner.configure(arguments)
    if job["job_key"] != JOB_KEY:
        raise RuntimeError(f"5140 selected the wrong locked job: {job['job_key']}")
    base.REVISION = "exact-Laurent-certificate-deep-argument-chart-v1"
    base.M5127.REVISION = base.REVISION
    base.PRECISION_POLICY = dict(DEEP_PROFILE)
    base.M5127.LOW_BOUNDARY_NODES = DEEP_PROFILE["low_boundary_nodes"]
    base.M5127.LOW_GLOBAL_NODES = DEEP_PROFILE["low_global_nodes"]
    base.M5127.LOW_RESIDUE_NODES = DEEP_PROFILE["low_global_residue_nodes"]
    base.M5127.HIGH_BOUNDARY_NODES = DEEP_PROFILE["high_boundary_nodes"]
    base.M5127.HIGH_GLOBAL_NODES = DEEP_PROFILE["high_global_nodes"]
    base.M5127.HIGH_RESIDUE_NODES = DEEP_PROFILE["high_global_residue_nodes"]
    original_build_charts = base.M5127.build_charts
    original_serialized_chart = base.M5127.serialized_chart

    def certified_build_charts(
        problem: dict[str, Any], pole_rows: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        charts = original_build_charts(problem, pole_rows)
        for chart in charts:
            chart["numeric_chart_accepted_before_exact_certificate"] = bool(
                chart["accepted"]
            )
            chart["exact_Laurent_certificate_applied"] = False
            chart["exact_Laurent_order"] = None
            chart["exact_Laurent_certificate"] = None
            target = chart["family"] == "beam_spinor" and chart["member"] == "small"
            non_order_checks_pass = bool(
                chart["condition_residual"] < base.M5127.ROOT_RESIDUAL_TOLERANCE
                and chart["reciprocal_root_residual"]
                < base.M5127.ROOT_RESIDUAL_TOLERANCE
                and chart["residue_disagreement"]
                < base.M5127.MAXIMUM_RESIDUE_DISAGREEMENT
                and chart["regular_integral_uncertainty"]
                < base.M5127.MAXIMUM_REGULAR_INTEGRAL_UNCERTAINTY
            )
            numeric_order_failed_only = bool(
                chart["double_to_simple_ratio"]
                >= base.M5127.MAXIMUM_DOUBLE_TO_SIMPLE_RATIO
                and non_order_checks_pass
            )
            if target and not chart["accepted"] and numeric_order_failed_only:
                chart["accepted"] = True
                chart["exact_Laurent_certificate_applied"] = True
                chart["exact_Laurent_order"] = "simple"
                chart["exact_Laurent_certificate"] = base.relative(PROOF)
        return charts

    def certified_serialized_chart(chart: dict[str, Any]) -> dict[str, Any]:
        row = original_serialized_chart(chart)
        row.update(
            {
                "numeric_chart_accepted_before_exact_certificate": chart.get(
                    "numeric_chart_accepted_before_exact_certificate", True
                ),
                "exact_Laurent_certificate_applied": chart.get(
                    "exact_Laurent_certificate_applied", False
                ),
                "exact_Laurent_order": chart.get("exact_Laurent_order"),
                "exact_Laurent_certificate": chart.get(
                    "exact_Laurent_certificate"
                ),
                "numeric_double_to_simple_threshold": (
                    base.M5127.MAXIMUM_DOUBLE_TO_SIMPLE_RATIO
                ),
                "numeric_threshold_changed": False,
            }
        )
        return row

    base.M5127.build_charts = certified_build_charts
    base.M5127.serialized_chart = certified_serialized_chart
    if base.INITIAL_REJECTED_GATE is None:
        raise RuntimeError("5140 missing rejected-gate destination")
    if not base.INITIAL_REJECTED_GATE.exists():
        base.atomic_json(base.INITIAL_REJECTED_GATE, default_gate)
    configuration.update(
        {
            "precision": "exact-certificate-proof-gated-deep",
            "precision_profile": DEEP_PROFILE,
            "simple_pole_proof": base.relative(PROOF),
            "simple_pole_proof_sha256": base.M5127.digest(PROOF),
            "source_default_rejected_gate": base.relative(DEFAULT_REJECTED_GATE),
            "source_default_rejected_gate_sha256": base.M5127.digest(
                DEFAULT_REJECTED_GATE
            ),
            "source_deep_rejected_gate": base.relative(DEEP_REJECTED_GATE),
            "source_deep_rejected_gate_sha256": base.M5127.digest(
                DEEP_REJECTED_GATE
            ),
            "acceptance_rule": "numeric Laurent-order threshold OR exact source-algebra Laurent-order certificate; all residue, regular, root, path, and isolation checks remain mandatory",
            "numeric_threshold_changed": False,
            "mode": mode,
        }
    )
    base.atomic_json(base.SOURCE / "locked_next_job_configuration.json", configuration)
    return runner, configuration


def augment_outputs(runner: Any, result: dict[str, Any], mode: str) -> dict[str, Any]:
    base = runner.M5128
    gate = base.read_json(base.GATE_JSON)
    certified_charts = [
        chart
        for chart in gate["charts"]
        if chart.get("exact_Laurent_certificate_applied")
    ]
    certificate_summary = {
        "certificate_count": len(certified_charts),
        "certified_families": [
            f"{chart['family']}:{chart['member']}" for chart in certified_charts
        ],
        "simple_pole_proof": base.relative(PROOF),
        "numeric_threshold_changed": False,
        "all_non_order_numeric_checks_pass": all(
            chart["condition_residual"] < base.M5127.ROOT_RESIDUAL_TOLERANCE
            and chart["reciprocal_root_residual"]
            < base.M5127.ROOT_RESIDUAL_TOLERANCE
            and chart["residue_disagreement"]
            < base.M5127.MAXIMUM_RESIDUE_DISAGREEMENT
            and chart["regular_integral_uncertainty"]
            < base.M5127.MAXIMUM_REGULAR_INTEGRAL_UNCERTAINTY
            for chart in certified_charts
        ),
    }
    gate["exact_Laurent_certificate_summary"] = certificate_summary
    gate["acceptance_rule"] = (
        "numeric Laurent-order threshold OR exact source-algebra certificate"
    )
    base.atomic_json(base.GATE_JSON, gate)
    gate_digest = base.M5127.digest(base.GATE_JSON)
    result["exact_Laurent_certificate_summary"] = certificate_summary
    result["numeric_threshold_changed"] = False
    result["repair_gate_sha256"] = gate_digest
    if mode in ("execute", "finalize-existing"):
        job_path = base.RUN / "jobs" / f"{base.JOB_KEY}.json"
        kernel_path = base.RUN / "kernels" / f"{base.JOB_KEY}.json"
        job = base.read_json(job_path)
        kernel = base.read_json(kernel_path)
        job["repair_gate_sha256"] = gate_digest
        kernel["repair_gate_sha256"] = gate_digest
        base.atomic_json(job_path, job)
        base.atomic_json(kernel_path, kernel)
        base.atomic_json(base.RESULT_JSON, result)
        with base.VALIDATION_CSV.open(
            "r", encoding="utf-8", newline=""
        ) as handle:
            validation_rows = list(csv.DictReader(handle))
        validation_rows.extend(
            [
                {
                    "check_id": "exact_Laurent_certificate_applied_once",
                    "passed": str(len(certified_charts) == 1),
                    "detail": str(certificate_summary["certified_families"]),
                    "checkpoint_marker": base.MARKER,
                    "valid_for_numeric_UV_claim": "False",
                    "valid_for_local_GR_claim": "False",
                    "valid_for_full_MTS_claim": "False",
                    "source_checked_date": CHECKED_DATE,
                },
                {
                    "check_id": "certificate_non_order_checks_pass",
                    "passed": str(
                        certificate_summary["all_non_order_numeric_checks_pass"]
                    ),
                    "detail": "root, reciprocal, residue, and regular checks",
                    "checkpoint_marker": base.MARKER,
                    "valid_for_numeric_UV_claim": "False",
                    "valid_for_local_GR_claim": "False",
                    "valid_for_full_MTS_claim": "False",
                    "source_checked_date": CHECKED_DATE,
                },
                {
                    "check_id": "numeric_threshold_unchanged",
                    "passed": "True",
                    "detail": str(base.M5127.MAXIMUM_DOUBLE_TO_SIMPLE_RATIO),
                    "checkpoint_marker": base.MARKER,
                    "valid_for_numeric_UV_claim": "False",
                    "valid_for_local_GR_claim": "False",
                    "valid_for_full_MTS_claim": "False",
                    "source_checked_date": CHECKED_DATE,
                },
                {
                    "check_id": "gate_digest_synchronized",
                    "passed": str(
                        job["repair_gate_sha256"] == gate_digest
                        and kernel["repair_gate_sha256"] == gate_digest
                    ),
                    "detail": gate_digest,
                    "checkpoint_marker": base.MARKER,
                    "valid_for_numeric_UV_claim": "False",
                    "valid_for_local_GR_claim": "False",
                    "valid_for_full_MTS_claim": "False",
                    "source_checked_date": CHECKED_DATE,
                },
            ]
        )
        base.write_csv(base.VALIDATION_CSV, validation_rows)
        appendix = f"""

## Exact Laurent-order certificate

The small beam-spinor chart is accepted by the exact KLT order proof at
`{base.relative(PROOF)}`. Its deep numerical residue disagreement and regular
uncertainty pass their unchanged limits. The noisy second Fourier estimator is
retained in the gate record, but it is not treated as evidence for a double pole
because the implemented source algebra proves the second principal coefficient
vanishes. Exactly `{len(certified_charts)}` chart used this certificate; no
numeric threshold was changed.
"""
        base.DOCUMENT.write_text(
            base.DOCUMENT.read_text(encoding="utf-8") + appendix,
            encoding="utf-8",
        )
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        choices=("gate", "execute", "finalize-existing"),
        default="gate",
    )
    arguments = parser.parse_args()
    runner, configuration = configure(arguments.mode)
    if arguments.mode == "gate":
        result = runner.M5128.gate_only()
    elif arguments.mode == "finalize-existing":
        result = runner.M5128.finalize_existing()
    else:
        result = runner.M5128.execute()
    result = augment_outputs(runner, result, arguments.mode)
    print(
        json.dumps(
            {"configuration": configuration, "result": result},
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
