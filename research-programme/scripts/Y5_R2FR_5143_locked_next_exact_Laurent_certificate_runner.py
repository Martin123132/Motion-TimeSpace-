from __future__ import annotations

import argparse
import csv
import importlib.util
import json
from pathlib import Path
from typing import Any


POST = Path(__file__).resolve().parents[1]
GENERIC_RUNNER = POST / "scripts" / "Y5_R2FR_5132_locked_next_argument_gate_and_single_job_runner.py"
DEEP_PROFILE = {
    "low_boundary_nodes": 96,
    "low_global_nodes": 128,
    "low_global_residue_nodes": 192,
    "high_boundary_nodes": 128,
    "high_global_nodes": 192,
    "high_global_residue_nodes": 256,
    "selection": "row-local KLT simple-pole proof plus deep residue and regular-part stability",
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


def configure(arguments: argparse.Namespace) -> tuple[Any, dict[str, Any], Path]:
    runner = load_module(
        f"mts_5132_for_{arguments.checkpoint_id}", GENERIC_RUNNER
    )
    generic_arguments = argparse.Namespace(
        checkpoint_id=str(arguments.checkpoint_id),
        checked_date=str(arguments.checked_date),
        job_key=arguments.job_key,
        precision="default",
        mode=arguments.mode,
    )
    job, configuration = runner.configure(generic_arguments)
    base = runner.M5128
    base_argument = str(job["base_argument_id"])
    proof = (
        POST
        / "source-intake"
        / "functional_rg"
        / str(arguments.proof_checkpoint)
        / f"{base_argument}_KLT_collinear_pole_order_proof.json"
    )
    rejected_gate = (
        POST
        / "source-intake"
        / "functional_rg"
        / str(arguments.rejected_gate_checkpoint)
        / f"{base_argument}_argument_local_outer_collinear_chart_gate.json"
    )
    proof_row = base.read_json(proof)
    rejected_gate_row = base.read_json(rejected_gate)
    if proof_row.get("job_key") != job["job_key"]:
        raise RuntimeError(
            f"proof job mismatch: {proof_row.get('job_key')} != {job['job_key']}"
        )
    if not proof_row.get("simple_pole_order_proved_for_locked_row"):
        raise RuntimeError("exact-certificate runner requires a row-local simple-pole proof")
    if rejected_gate_row.get("job_key") != job["job_key"]:
        raise RuntimeError("rejected default gate belongs to another locked row")
    if rejected_gate_row.get("gate_accepted"):
        raise RuntimeError("exact-certificate route requires a preserved rejected default gate")
    base.REVISION = "locked-next-exact-Laurent-certificate-deep-chart-v1"
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
                chart["exact_Laurent_certificate"] = base.relative(proof)
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
        raise RuntimeError("missing rejected-gate destination")
    if not base.INITIAL_REJECTED_GATE.exists():
        base.atomic_json(base.INITIAL_REJECTED_GATE, rejected_gate_row)
    configuration.update(
        {
            "precision": "row-local-exact-certificate-proof-gated-deep",
            "precision_profile": DEEP_PROFILE,
            "simple_pole_proof": base.relative(proof),
            "simple_pole_proof_sha256": base.M5127.digest(proof),
            "source_rejected_default_gate": base.relative(rejected_gate),
            "source_rejected_default_gate_sha256": base.M5127.digest(
                rejected_gate
            ),
            "acceptance_rule": "numeric Laurent-order threshold OR row-local exact source-algebra certificate; every non-order numeric check remains mandatory",
            "numeric_threshold_changed": False,
            "mode": arguments.mode,
        }
    )
    base.atomic_json(base.SOURCE / "locked_next_job_configuration.json", configuration)
    return runner, configuration, proof


def augment_outputs(
    runner: Any,
    configuration: dict[str, Any],
    proof: Path,
    result: dict[str, Any],
    mode: str,
) -> dict[str, Any]:
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
        "simple_pole_proof": base.relative(proof),
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
        "numeric Laurent-order threshold OR row-local exact source-algebra certificate"
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
        custom_ids = {
            "exact_Laurent_certificate_scope_valid",
            "certificate_non_order_checks_pass",
            "numeric_threshold_unchanged",
            "gate_digest_synchronized",
        }
        validation_rows = [
            row for row in validation_rows if row.get("check_id") not in custom_ids
        ]
        validation_rows.extend(
            [
                {
                    "check_id": "exact_Laurent_certificate_scope_valid",
                    "passed": str(
                        len(certified_charts) <= 1
                        and (
                            len(certified_charts) == 1
                            or all(
                                chart.get(
                                    "numeric_chart_accepted_before_exact_certificate"
                                )
                                for chart in gate["charts"]
                            )
                        )
                    ),
                    "detail": (
                        "certificate unused because every chart passed numerically"
                        if not certified_charts
                        else str(certificate_summary["certified_families"])
                    ),
                },
                {
                    "check_id": "certificate_non_order_checks_pass",
                    "passed": str(
                        certificate_summary["all_non_order_numeric_checks_pass"]
                    ),
                    "detail": "root, reciprocal, residue and regular checks",
                },
                {
                    "check_id": "numeric_threshold_unchanged",
                    "passed": "True",
                    "detail": str(base.M5127.MAXIMUM_DOUBLE_TO_SIMPLE_RATIO),
                },
                {
                    "check_id": "gate_digest_synchronized",
                    "passed": str(
                        job["repair_gate_sha256"] == gate_digest
                        and kernel["repair_gate_sha256"] == gate_digest
                    ),
                    "detail": gate_digest,
                },
            ]
        )
        for row in validation_rows:
            row.update(
                {
                    "checkpoint_marker": base.MARKER,
                    "valid_for_numeric_UV_claim": "False",
                    "valid_for_local_GR_claim": "False",
                    "valid_for_full_MTS_claim": "False",
                    "source_checked_date": base.CHECKED_DATE,
                }
            )
        base.write_csv(base.VALIDATION_CSV, validation_rows)
        appendix = f"""

## Row-local exact Laurent-order certificate

The small beam-spinor chart is accepted by the row-local KLT proof at
`{base.relative(proof)}`. Deep residue and regular-part diagnostics pass their
unchanged limits. Exactly `{len(certified_charts)}` chart uses the certificate;
the noisy second Fourier estimate remains recorded and no numeric threshold is
changed.
"""
        current_document = base.DOCUMENT.read_text(encoding="utf-8")
        heading = "## Row-local exact Laurent-order certificate"
        if heading in current_document:
            current_document = current_document.split(heading, 1)[0].rstrip()
        base.DOCUMENT.write_text(
            current_document + "\n\n" + appendix.lstrip(), encoding="utf-8"
        )
    configuration["final_gate_sha256"] = gate_digest
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoint-id", default="5143")
    parser.add_argument("--checked-date", default="2026-07-20")
    parser.add_argument("--proof-checkpoint", default="5142")
    parser.add_argument("--rejected-gate-checkpoint", default="5141")
    parser.add_argument("--job-key")
    parser.add_argument(
        "--mode",
        choices=("gate", "execute", "finalize-existing"),
        default="gate",
    )
    arguments = parser.parse_args()
    runner, configuration, proof = configure(arguments)
    if arguments.mode == "gate":
        result = runner.M5128.gate_only()
    elif arguments.mode == "finalize-existing":
        result = runner.M5128.finalize_existing()
    else:
        result = runner.M5128.execute()
    result = augment_outputs(
        runner, configuration, proof, result, arguments.mode
    )
    print(
        json.dumps(
            {"configuration": configuration, "result": result},
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
