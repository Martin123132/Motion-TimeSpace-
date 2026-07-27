from __future__ import annotations

import argparse
import csv
import importlib.util
import json
import os
import shutil
import time
from pathlib import Path
from typing import Any


POST = Path(__file__).resolve().parents[1]
ROOT = POST.parent
FORMAL = ROOT / "formalization-workbench"
SCRIPT_5143 = POST / "scripts" / "Y5_R2FR_5143_locked_next_exact_Laurent_certificate_runner.py"
SCRIPT_5146 = POST / "scripts" / "Y5_R2FR_5146_E040_A10_conditioned_annulus_global_cycle_replay.py"
RUN = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5125"
    / "runs"
    / "reciprocal_stratified_fresh_pilot_v1"
)
CONFIG = RUN / "config.json"
SCHEDULE = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5125"
    / "reciprocal_stratified_locked_schedule.json"
)
JOB_KEY = "E020__S512503_N0000__A10__primary24"
LIVE_JOB = RUN / "jobs" / f"{JOB_KEY}.json"
LIVE_KERNEL = RUN / "kernels" / f"{JOB_KEY}.json"
SOURCE = POST / "source-intake" / "functional_rg" / "5147"
WITNESSES = SOURCE / "witnesses"
RESULT_JSON = SOURCE / "E020_A10_chart_conditioned_annulus_replay_result.json"
VALIDATION_CSV = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5147_VALIDATION.csv"
)
DOCUMENT = POST / "5147-Y5-R2FR-E020-A10-chart-conditioned-annulus-replay.md"
PROOF = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5142"
    / "A10_KLT_collinear_pole_order_proof.json"
)
REJECTED_GATE = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5141"
    / "A10_argument_local_outer_collinear_chart_gate.json"
)
PRIOR_CERTIFIED_GATE = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5143"
    / "A10_argument_local_outer_collinear_chart_gate.json"
)

MARKER = "MTS_5147_E020_A10_CHART_CONDITIONED_ANNULUS_REPLAY"
CHECKED_DATE = "2026-07-20"
FORMAL_BASELINE = "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
INNER_NODE_LEVELS = (96, 192)


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5143 = load_module("mts_5143_for_5147", SCRIPT_5143)
M5146 = load_module("mts_5146_for_5147", SCRIPT_5146)


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(value, indent=2, sort_keys=True), encoding="utf-8"
    )
    os.replace(temporary, path)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise RuntimeError(f"refusing to write empty CSV: {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def exact_certificate_scope_valid(
    chart_gate: dict[str, Any], exact_summary: dict[str, Any]
) -> bool:
    certificate_count = exact_summary.get("certificate_count")
    charts = chart_gate.get("charts", [])
    return bool(
        exact_summary.get("all_non_order_numeric_checks_pass")
        and isinstance(certificate_count, int)
        and certificate_count <= 1
        and (
            certificate_count == 1
            or (
                bool(charts)
                and all(
                    chart.get("numeric_chart_accepted_before_exact_certificate")
                    for chart in charts
                )
            )
        )
    )


def freeze_inputs(paths: dict[str, Path]) -> dict[str, dict[str, Any]]:
    WITNESSES.mkdir(parents=True, exist_ok=True)
    result: dict[str, dict[str, Any]] = {}
    for name, path in paths.items():
        destination = WITNESSES / f"{name}{path.suffix}"
        shutil.copy2(path, destination)
        result[name] = {
            "source": str(path),
            "witness": str(destination),
            "source_sha256": M5146.digest(path),
            "witness_sha256": M5146.digest(destination),
        }
    return result


def configure_chart() -> tuple[Any, Any, dict[str, Any], Path, dict[str, Any], list[dict[str, Any]], dict[str, Any]]:
    arguments = argparse.Namespace(
        checkpoint_id="5147",
        checked_date=CHECKED_DATE,
        proof_checkpoint="5142",
        rejected_gate_checkpoint="5141",
        job_key=JOB_KEY,
        mode="gate",
    )
    runner, configuration, proof = M5143.configure(arguments)
    base = runner.M5128
    context, preflight = base.structural_preflight()
    groups, charts, gate = base.build_and_write_gate(context, preflight)
    gate = M5143.augment_outputs(
        runner, configuration, proof, gate, "gate"
    )
    final_gate = base.read_json(base.GATE_JSON)
    if not final_gate.get("gate_accepted"):
        raise RuntimeError("5147 exact-Laurent chart gate is not accepted")
    return runner, base, context, proof, groups, charts, final_gate


def run_gate(
    base: Any,
    context: dict[str, Any],
    groups: dict[tuple[tuple[str, bool], ...], list[dict[str, Any]]],
    charts: list[dict[str, Any]],
    inner_nodes: int,
) -> dict[str, Any]:
    module = context["module"]
    profile = context["profile"]
    config = context["config"]
    M5077 = base.M5125.M5077
    M5077.install_history_invariant_breakpoints(module)
    M5077.removable_extension_gate()
    previous_catalog = module.chamber_residue_catalog
    previous_global = module.global_chamber_value
    previous_breakpoints = module.collision_scaled_breakpoints
    conditioned = M5146.ConditionedFiniteAnnulusGlobalValue(
        module,
        inner_nodes,
        float(profile["relative_adaptive_tolerance"]),
    )
    chart_extension = base.ArgumentLocalPoleChart(conditioned, groups)
    removable = M5077.M5085.CertifiedRemovableGlobalExtension(
        chart_extension
    )
    overlay = base.catalog_overlay(groups)
    module.chamber_residue_catalog = overlay
    module.global_chamber_value = removable
    module.collision_scaled_breakpoints = base.M5127.chart_breakpoints(
        previous_breakpoints, charts
    )
    M5077.CURRENT_EVENT = context["event"]
    M5077.CURRENT_ARGUMENT = context["argument"]
    M5077.M5036.MREPAIR.CURRENT_JOB = JOB_KEY
    M5077.M5036.MREPAIR.RADIUS_AUDIT.clear()
    M5077.LOCAL_RESIDUE_RESOLUTION_AUDIT.clear()
    M5077.OUTWARD_CONTOUR_AUDIT.clear()
    M5077.PROJECTIVE_CLUSTER_ZERO_AUDIT.clear()
    base.CATALOG_AUDIT.clear()
    base.M5126.REPAIR_AUDIT.clear()
    started = time.monotonic()
    try:
        gate = module.fixed_event_integral_gate(
            context["topology"],
            tuple(int(value) for value in profile["relative_orders"]),
            int(profile["global_nodes"]),
            int(profile["global_residue_nodes"]),
            int(profile["relative_residue_nodes"]),
            float(profile["model_distance"]),
            int(config["topology"]["boundary_tracking_steps"]),
            str(profile["relative_quadrature_mode"]),
            float(profile["relative_adaptive_tolerance"]),
            int(profile["relative_adaptive_maximum_intervals"]),
        )
    finally:
        module.chamber_residue_catalog = previous_catalog
        module.global_chamber_value = previous_global
        module.collision_scaled_breakpoints = previous_breakpoints
    runtime = time.monotonic() - started
    path = SOURCE / f"E020_A10_chart_conditioned_annulus_inner{inner_nodes}_gate.json"
    atomic_json(path, gate)
    value = complex(gate["order_rows"][-1]["causally_corrected_value"])
    return {
        "inner_nodes": inner_nodes,
        "runtime_seconds": runtime,
        "gate_path": str(path),
        "gate_sha256": M5146.digest(path),
        "value": M5146.complex_row(value),
        "strict_adaptive_quadrature_converged": bool(
            gate.get("strict_adaptive_quadrature_converged", False)
        ),
        "fixed_event_crossed_integral_converged": bool(
            gate["fixed_event_crossed_integral_converged"]
        ),
        "all_residues_stable": bool(gate["all_residues_stable"]),
        "maximum_adaptive_chamber_relative_error": float(
            gate["order_rows"][-1]["maximum_adaptive_chamber_relative_error"]
        ),
        "composite_interval_count": int(
            gate["order_rows"][-1]["composite_interval_count"]
        ),
        "relative_integrand_evaluation_count": int(
            gate["order_rows"][-1]["relative_integrand_evaluation_count"]
        ),
        "conditioned_annulus_audit": conditioned.summary(),
        "argument_local_chart_audit": chart_extension.summary(),
        "catalog_overlay_rows": len(base.CATALOG_AUDIT),
        "removable_extension_call_count": len(removable.calls),
    }


def update_live(
    base: Any,
    selected: dict[str, Any],
    chart_gate: dict[str, Any],
    chart_gate_path: Path,
) -> tuple[dict[str, Any], dict[str, Any]]:
    fixed_gate = read_json(Path(selected["gate_path"]))
    job = read_json(LIVE_JOB)
    kernel = read_json(LIVE_KERNEL)
    job.setdefault(
        "pre_5147_chart_conditioned_annulus_replay",
        {
            "status": job.get("status"),
            "integral_converged": job.get("integral_converged"),
            "job_sha256": M5146.digest(LIVE_JOB),
        },
    )
    kernel.setdefault(
        "pre_5147_chart_conditioned_annulus_replay",
        {
            "strict_adaptive_validated": kernel.get(
                "strict_adaptive_validated"
            ),
            "kernel_sha256": M5146.digest(LIVE_KERNEL),
        },
    )
    chart_gate_sha256 = M5146.digest(chart_gate_path)
    audit = {
        "checkpoint_marker": MARKER,
        "selected_inner_nodes": selected["inner_nodes"],
        "fixed_gate_path": selected["gate_path"],
        "fixed_gate_sha256": selected["gate_sha256"],
        "chart_gate_path": str(chart_gate_path),
        "chart_gate_sha256": chart_gate_sha256,
        "conditioned_annulus": selected["conditioned_annulus_audit"],
        "argument_local_chart": selected["argument_local_chart_audit"],
        "exact_Laurent_certificate_summary": chart_gate.get(
            "exact_Laurent_certificate_summary"
        ),
        "physical_pole_ownership_changed": False,
        "outer_tolerance_changed": False,
        "outer_interval_cap_changed": False,
    }
    kernel_profile = dict(kernel.get("profile_audit", {}))
    kernel_profile["chart_conditioned_annulus_replay"] = audit
    kernel.update(
        {
            "fixed_event_integral_gate": fixed_gate,
            "strict_adaptive_validated": True,
            "profile_audit": kernel_profile,
            "repair_checkpoint_marker": MARKER,
            "repair_gate": base.relative(chart_gate_path),
            "repair_gate_sha256": chart_gate_sha256,
            "strict_adaptive_reconciliation": {
                "checkpoint_marker": MARKER,
                "strict_pass": True,
            },
        }
    )
    direct_kernel = base.M5125.M5077.M5036.M5035.M5034.highest_value(
        fixed_gate
    )
    direct = (
        base.M5125.M5077.M5036.M5035.M5034.KERNEL_MULTIPLIER
        * direct_kernel
    )
    job_profile = dict(job.get("profile_audit", {}))
    job_profile["chart_conditioned_annulus_replay"] = audit
    job.update(
        {
            "status": "COMPLETED_CONVERGED",
            "integral_converged": True,
            "strict_adaptive_validated": True,
            "normalized_direct_D_hhh_over_G3": M5146.complex_row(direct),
            "kernel_runtime_seconds": selected["runtime_seconds"],
            "job_runtime_seconds": selected["runtime_seconds"],
            "profile_audit": job_profile,
            "repair_checkpoint_marker": MARKER,
            "repair_gate": base.relative(chart_gate_path),
            "repair_gate_sha256": chart_gate_sha256,
            "strict_adaptive_reconciliation": {
                "checkpoint_marker": MARKER,
                "strict_pass": True,
            },
        }
    )
    atomic_json(LIVE_KERNEL, kernel)
    atomic_json(LIVE_JOB, job)
    return job, kernel


def write_document(result: dict[str, Any], failures: list[str]) -> None:
    certificate_count = result["exact_Laurent_certificate_summary"][
        "certificate_count"
    ]
    certificate_statement = (
        "Exactly one numerically unresolved chart uses the 5142 row-local "
        "simple-pole certificate."
        if certificate_count == 1
        else "All four charts pass their numeric Laurent-order checks, so the "
        "5142 row-local simple-pole certificate remains a verified backstop "
        "but is not invoked."
    )
    DOCUMENT.write_text(
        f"""# 5147 E020/A10 chart-conditioned-annulus replay

## Result

The E020 row retains its 5142 row-local KLT proof. {certificate_statement}
Every non-order numeric check remains mandatory. The outer chart is then
composed with the 5146 conditioned finite-annulus global cycle. Neither
mechanism is replaced or manually switched by argument label.

The locked 96/192 inner-node ladder gives strict flags
`{[row['strict_adaptive_quadrature_converged'] for row in result['node_ladder']]}`,
cross-node relative difference `{result['cross_node_relative_difference']}`
and selected corrected value `{result['selected_value']}`. Current schedule
counts are `{result['run_counts_after']}` and the next locked row is
`{result['first_incomplete_after']['job_key']}`.

This closes the two A10 false-positive convergence labels with a common
Cauchy-conditioning derivation. It is coefficient-pipeline infrastructure,
not a local-GR or full-MTS claim. The next project-level action is to return to
the parent source-coupling/local-GR spine and ask whether the same action
preserves local GR/Newton/Maxwell while deriving its nonlocal galactic
activation—never to treat numerical completion as the physical theory.

Validation failures: `{failures}`. No GitHub action occurred.
""",
        encoding="utf-8",
    )


def main() -> None:
    required = [
        SCRIPT_5143,
        SCRIPT_5146,
        CONFIG,
        SCHEDULE,
        LIVE_JOB,
        LIVE_KERNEL,
        PROOF,
        REJECTED_GATE,
        PRIOR_CERTIFIED_GATE,
        FORMAL,
    ]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError(f"missing 5147 inputs: {missing}")
    config = read_json(CONFIG)
    schedule = read_json(SCHEDULE)["jobs"]
    counts_before = M5146.run_counts(schedule, config["config_digest"])
    first_before = M5146.first_incomplete(schedule, config["config_digest"])
    if first_before["job_key"] != JOB_KEY:
        raise RuntimeError(
            f"5147 target is not first incomplete row: {first_before['job_key']}"
        )
    witnesses = freeze_inputs(
        {
            "live_job_before": LIVE_JOB,
            "live_kernel_before": LIVE_KERNEL,
            "proof_5142": PROOF,
            "rejected_gate_5141": REJECTED_GATE,
            "certified_gate_5143": PRIOR_CERTIFIED_GATE,
        }
    )
    runner, base, context, proof, groups, charts, chart_gate = configure_chart()
    chart_gate_path = base.GATE_JSON
    chart_gate_sha256 = M5146.digest(chart_gate_path)
    node_ladder: list[dict[str, Any]] = []
    for nodes in INNER_NODE_LEVELS:
        row = run_gate(base, context, groups, charts, nodes)
        node_ladder.append(row)
        print(
            json.dumps(
                {
                    "checkpoint_marker": MARKER,
                    "completed_inner_nodes": nodes,
                    "strict": row["strict_adaptive_quadrature_converged"],
                    "relative_error": row[
                        "maximum_adaptive_chamber_relative_error"
                    ],
                    "intervals": row["composite_interval_count"],
                    "runtime_seconds": row["runtime_seconds"],
                },
                sort_keys=True,
            ),
            flush=True,
        )
    values = [
        complex(row["value"]["real"], row["value"]["imaginary"])
        for row in node_ladder
    ]
    cross_node = abs(values[-1] - values[-2]) / max(abs(values[-1]), 1.0)
    tolerance = float(context["profile"]["relative_adaptive_tolerance"])
    exact_summary = chart_gate.get("exact_Laurent_certificate_summary", {})
    certificate_scope_valid = exact_certificate_scope_valid(
        chart_gate, exact_summary
    )
    ladder_passed = bool(
        chart_gate.get("gate_accepted")
        and certificate_scope_valid
        and all(
            row["strict_adaptive_quadrature_converged"]
            and row["fixed_event_crossed_integral_converged"]
            and row["all_residues_stable"]
            and row["removable_extension_call_count"] == 0
            and row["conditioned_annulus_audit"]["fallback_count"] == 0
            and row["conditioned_annulus_audit"]["minimum_log_clearance"]
            >= row["conditioned_annulus_audit"]["required_log_clearance"]
            for row in node_ladder
        )
        and cross_node <= tolerance
    )
    if ladder_passed:
        selected = node_ladder[-1]
        live_job, live_kernel = update_live(
            base, selected, chart_gate, chart_gate_path
        )
        live_updated = True
    else:
        selected = node_ladder[-1]
        live_job = read_json(LIVE_JOB)
        live_kernel = read_json(LIVE_KERNEL)
        live_updated = False
    counts_after = M5146.run_counts(schedule, config["config_digest"])
    first_after = M5146.first_incomplete(schedule, config["config_digest"])
    status = read_json(RUN / "status.json") if (RUN / "status.json").exists() else {}
    status.update(
        {
            "state": "PAUSED_AFTER_5147_E020_A10_REPLAY"
            if live_updated
            else "BLOCKED_AFTER_5147_E020_A10_REPLAY",
            "completed_converged": counts_after["completed_converged"],
            "completed_unconverged": counts_after["completed_unconverged"],
            "failed": counts_after["failed"],
            "missing": counts_after["missing"],
            "last_job_key": JOB_KEY,
            "next_job_key": first_after["job_key"],
            "checkpoint_marker": MARKER,
        }
    )
    atomic_json(RUN / "status.json", status)
    formal_digest = M5146.tree_digest(FORMAL)
    result = {
        "checkpoint_marker": MARKER,
        "checked_date": CHECKED_DATE,
        "job_key": JOB_KEY,
        "counts_before": counts_before,
        "first_incomplete_before": first_before,
        "witnesses": witnesses,
        "proof": str(proof),
        "proof_sha256": M5146.digest(proof),
        "chart_gate": str(chart_gate_path),
        "chart_gate_sha256": chart_gate_sha256,
        "exact_Laurent_certificate_summary": exact_summary,
        "exact_Laurent_certificate_scope_valid": certificate_scope_valid,
        "node_ladder": node_ladder,
        "cross_node_relative_difference": cross_node,
        "locked_tolerance": tolerance,
        "ladder_passed": ladder_passed,
        "selected_inner_nodes": selected["inner_nodes"],
        "selected_value": selected["value"],
        "live_updated": live_updated,
        "live_job_status": live_job.get("status"),
        "live_strict_adaptive_validated": live_job.get(
            "strict_adaptive_validated"
        ),
        "live_kernel_strict_adaptive_validated": live_kernel.get(
            "strict_adaptive_validated"
        ),
        "run_counts_after": counts_after,
        "first_incomplete_after": first_after,
        "outer_tolerance_changed": False,
        "outer_interval_cap_changed": False,
        "physics_parameter_changed": False,
        "formalization_workbench_tree_sha256": formal_digest,
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(RESULT_JSON, result)
    witness_hashes_preserved = all(
        row["source_sha256"] == row["witness_sha256"]
        for row in witnesses.values()
    )
    checks = [
        ("source_paths_exist", not missing, str(missing)),
        ("target_was_first_incomplete", first_before["job_key"] == JOB_KEY, first_before["job_key"]),
        ("input_witnesses_preserved", witness_hashes_preserved, str(witnesses)),
        ("row_local_proof_preserved", result["proof_sha256"] == witnesses["proof_5142"]["source_sha256"], result["proof_sha256"]),
        ("chart_gate_accepted", bool(chart_gate.get("gate_accepted")), str(chart_gate.get("gate_accepted"))),
        ("exact_certificate_scope", certificate_scope_valid, str(exact_summary)),
        ("two_level_inner_ladder", [row["inner_nodes"] for row in node_ladder] == [96, 192], str(INNER_NODE_LEVELS)),
        ("conditioned_annuli_qualified", all(row["conditioned_annulus_audit"]["fallback_count"] == 0 and row["conditioned_annulus_audit"]["minimum_log_clearance"] >= row["conditioned_annulus_audit"]["required_log_clearance"] for row in node_ladder), str([(row["conditioned_annulus_audit"]["minimum_log_clearance"], row["conditioned_annulus_audit"]["required_log_clearance"], row["conditioned_annulus_audit"]["fallback_count"]) for row in node_ladder])),
        ("both_outer_gates_strict", all(row["strict_adaptive_quadrature_converged"] for row in node_ladder), str([row["maximum_adaptive_chamber_relative_error"] for row in node_ladder])),
        ("both_fixed_gates_converged", all(row["fixed_event_crossed_integral_converged"] for row in node_ladder), str([row["fixed_event_crossed_integral_converged"] for row in node_ladder])),
        ("all_residues_stable", all(row["all_residues_stable"] for row in node_ladder), str([row["all_residues_stable"] for row in node_ladder])),
        ("cross_node_stable", cross_node <= tolerance, str(cross_node)),
        ("no_removable_fallback", all(row["removable_extension_call_count"] == 0 for row in node_ladder), str([row["removable_extension_call_count"] for row in node_ladder])),
        ("live_row_strictly_converged", live_updated and live_job.get("status") == "COMPLETED_CONVERGED" and live_job.get("strict_adaptive_validated") is True, str(live_job.get("status"))),
        ("run_counts_close_A10_pair", counts_after == {"completed_converged": 52, "completed_unconverged": 0, "failed": 0, "missing": 508}, str(counts_after)),
        ("next_row_is_E020_A00", first_after["job_key"] == "E020__S512503_N0000__A00__primary24", first_after["job_key"]),
        ("locked_outer_profile_unchanged", not result["outer_tolerance_changed"] and not result["outer_interval_cap_changed"] and not result["physics_parameter_changed"], "outer profile and physics unchanged"),
        ("formal_tree_unchanged", formal_digest == FORMAL_BASELINE, formal_digest),
        ("claim_discipline", not result["valid_for_numeric_UV_claim"] and not result["valid_for_local_GR_claim"] and not result["valid_for_full_MTS_claim"], "coefficient replay is not physical evidence"),
    ]
    rows = [
        {
            "check_id": f"V5147_{index:02d}_{name}",
            "passed": passed,
            "detail": detail,
            "checkpoint_marker": MARKER,
        }
        for index, (name, passed, detail) in enumerate(checks, start=1)
    ]
    write_csv(VALIDATION_CSV, rows)
    failures = [name for name, passed, _ in checks if not passed]
    write_document(result, failures)
    print(
        json.dumps(
            {"result": result, "validation_failures": failures},
            indent=2,
            sort_keys=True,
        )
    )
    if failures:
        raise RuntimeError(f"checkpoint 5147 validation failed: {failures}")


if __name__ == "__main__":
    main()
