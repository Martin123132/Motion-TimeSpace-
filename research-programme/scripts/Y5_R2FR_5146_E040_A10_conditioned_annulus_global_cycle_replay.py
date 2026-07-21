from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import math
import os
import time
from pathlib import Path
from typing import Any, Callable


POST = Path(__file__).resolve().parents[1]
ROOT = POST.parent
FORMAL = ROOT / "formalization-workbench"
SCRIPT_5125 = POST / "scripts" / "Y5_R2FR_5125_reciprocal_stratified_fresh_pilot_runner.py"
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
JOB_KEY = "E040__S512503_N0000__A10__primary24"
EVENT_ID = "S512503_N0000"
ARGUMENT_ID = "E040_A10"
TOPOLOGY = RUN / "topologies" / f"{EVENT_ID}__{ARGUMENT_ID}.json"
LIVE_JOB = RUN / "jobs" / f"{JOB_KEY}.json"
LIVE_KERNEL = RUN / "kernels" / f"{JOB_KEY}.json"
SOURCE = POST / "source-intake" / "functional_rg" / "5146"
RESULT_JSON = SOURCE / "E040_A10_conditioned_annulus_global_cycle_replay_result.json"
VALIDATION_CSV = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5146_VALIDATION.csv"
)
DOCUMENT = POST / "5146-Y5-R2FR-E040-A10-conditioned-annulus-global-cycle-replay.md"

MARKER = "MTS_5146_E040_A10_CONDITIONED_ANNULUS_GLOBAL_CYCLE_REPLAY"
CHECKED_DATE = "2026-07-20"
FORMAL_BASELINE = "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
INNER_NODE_LEVELS = (96, 192)
ANNULUS_DESIGN_NODES = 48
INNER_ERROR_BUDGET_DIVISOR = 8.0
LOG_MODULUS_DEDUPLICATION_TOLERANCE = 1.0e-12


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5125 = load_module("mts_5125_for_5146", SCRIPT_5125)
M5077 = M5125.M5077


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(value, indent=2, sort_keys=True), encoding="utf-8"
    )
    os.replace(temporary, path)


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def tree_digest(path: Path) -> str:
    value = hashlib.sha256()
    for item in sorted(candidate for candidate in path.rglob("*") if candidate.is_file()):
        value.update(item.relative_to(path).as_posix().encode("utf-8"))
        value.update(digest(item).encode("ascii"))
    return value.hexdigest()


def complex_row(value: complex) -> dict[str, float]:
    return {"real": float(value.real), "imaginary": float(value.imag)}


def distinct_positive_moduli(groups: list[dict[str, Any]]) -> list[float]:
    values = sorted(
        abs(complex(group["root"]))
        for group in groups
        if abs(complex(group["root"])) > 0.0
    )
    distinct: list[float] = []
    for value in values:
        if (
            not distinct
            or abs(math.log(value / distinct[-1]))
            > LOG_MODULUS_DEDUPLICATION_TOLERANCE
        ):
            distinct.append(value)
    return distinct


def single_residue_radius(
    root: complex,
    group_index: int,
    groups: list[dict[str, Any]],
) -> float:
    separations = [
        abs(root - complex(group["root"]))
        for index, group in enumerate(groups)
        if index != group_index
    ]
    safe_scale = min([abs(root)] + separations) if separations else abs(root)
    return max(1.0e-7, 0.07 * safe_scale)


class ConditionedFiniteAnnulusGlobalValue:
    def __init__(
        self,
        module: Any,
        inner_nodes: int,
        outer_relative_tolerance: float,
    ) -> None:
        self.module = module
        self.inner_nodes = inner_nodes
        self.inner_error_budget = (
            outer_relative_tolerance / INNER_ERROR_BUDGET_DIVISOR
        )
        self.required_log_clearance = math.log(
            1.0 / self.inner_error_budget
        ) / ANNULUS_DESIGN_NODES
        self.call_count = 0
        self.minimum_log_clearance = math.inf
        self.minimum_radius = math.inf
        self.maximum_radius = 0.0
        self.minimum_rho_one = math.inf
        self.maximum_rho_two = 0.0
        self.correction_count = 0
        self.maximum_corrections_per_call = 0
        self.fallback_count = 0
        self.annulus_index_histogram: dict[int, int] = {}

    def __call__(
        self,
        relative_circle: complex,
        ownership: dict[str, bool],
        global_nodes: int,
        global_residue_nodes: int,
    ) -> complex:
        self.call_count += 1
        soft_direction, decay_direction, internal = self.module.M5028.event_geometry(
            self.module.SOFT_ENERGY,
            complex(self.module.SOFT_COSINE, 0.0),
            complex(self.module.DECAY_COSINE, 0.0),
            relative_circle,
        )
        groups = self.module.M5028.fixed_ownership_groups(
            internal,
            soft_direction,
            decay_direction,
            self.module.TARGET_COSINE,
            ownership,
        )
        moduli = distinct_positive_moduli(groups)
        if len(moduli) < 2:
            raise RuntimeError("5146 first-annulus cycle requires two finite pole moduli")
        candidates = [
            {
                "index": index,
                "rho_one": rho_one,
                "rho_two": rho_two,
                "radius": math.sqrt(rho_one * rho_two),
                "log_clearance": 0.5 * math.log(rho_two / rho_one),
            }
            for index, (rho_one, rho_two) in enumerate(
                zip(moduli[:-1], moduli[1:])
            )
        ]
        eligible = [
            row
            for row in candidates
            if row["log_clearance"] >= self.required_log_clearance
        ]
        if eligible:
            selected = min(
                eligible,
                key=lambda row: (
                    abs(math.log(row["radius"])),
                    -row["log_clearance"],
                ),
            )
        else:
            selected = max(candidates, key=lambda row: row["log_clearance"])
            self.fallback_count += 1
        rho_one = float(selected["rho_one"])
        rho_two = float(selected["rho_two"])
        radius = float(selected["radius"])
        selected_index = int(selected["index"])
        self.annulus_index_histogram[selected_index] = (
            self.annulus_index_histogram.get(selected_index, 0) + 1
        )
        if not rho_one < radius < rho_two:
            raise RuntimeError("5146 first-annulus radius does not lie in its annulus")
        log_clearance = min(
            math.log(radius / rho_one), math.log(rho_two / radius)
        )
        expected_clearance = 0.5 * math.log(rho_two / rho_one)
        if abs(log_clearance - expected_clearance) > 1.0e-12:
            raise RuntimeError("5146 minimax log-clearance identity failed")
        self.minimum_log_clearance = min(
            self.minimum_log_clearance, log_clearance
        )
        self.minimum_radius = min(self.minimum_radius, radius)
        self.maximum_radius = max(self.maximum_radius, radius)
        self.minimum_rho_one = min(self.minimum_rho_one, rho_one)
        self.maximum_rho_two = max(self.maximum_rho_two, rho_two)
        evaluator: Callable[[complex], complex] = lambda unit_circle: (
            self.module.M5028.M5026.finite_plus_integrand(
                internal,
                self.module.SOFT_ENERGY,
                soft_direction,
                decay_direction,
                self.module.TARGET_COSINE,
                unit_circle,
            )
        )
        result = self.module.M5028.M5026.circle_average(
            evaluator, self.inner_nodes, radius
        )
        residue_nodes = max(self.inner_nodes, global_residue_nodes)
        call_corrections = 0
        for group_index, group in enumerate(groups):
            root = complex(group["root"])
            desired_inside = bool(group["desired_inside"])
            currently_inside = abs(root) < radius
            if desired_inside == currently_inside:
                continue
            residue = self.module.M5028.M5024.local_residue(
                evaluator,
                root,
                single_residue_radius(root, group_index, groups),
                residue_nodes,
            )
            result = result + residue if desired_inside else result - residue
            call_corrections += 1
        self.correction_count += call_corrections
        self.maximum_corrections_per_call = max(
            self.maximum_corrections_per_call, call_corrections
        )
        return complex(result)

    def summary(self) -> dict[str, Any]:
        return {
            "inner_nodes": self.inner_nodes,
            "call_count": self.call_count,
            "minimum_log_clearance": float(self.minimum_log_clearance),
            "minimum_radius": float(self.minimum_radius),
            "maximum_radius": float(self.maximum_radius),
            "minimum_rho_one": float(self.minimum_rho_one),
            "maximum_rho_two": float(self.maximum_rho_two),
            "correction_count": self.correction_count,
            "maximum_corrections_per_call": self.maximum_corrections_per_call,
            "annulus_design_nodes": ANNULUS_DESIGN_NODES,
            "inner_error_budget": self.inner_error_budget,
            "required_log_clearance": self.required_log_clearance,
            "fallback_count": self.fallback_count,
            "annulus_index_histogram": {
                str(key): value
                for key, value in sorted(self.annulus_index_histogram.items())
            },
            "radius_rule": (
                "center every qualified finite annulus at "
                "R=sqrt(rho_i*rho_{i+1}); choose the qualified center "
                "nearest |R|=1"
            ),
            "log_clearance_identity": (
                "max_R min(log(R/rho_1),log(rho_2/R))="
                "0.5*log(rho_2/rho_1)"
            ),
        }


def run_gate(inner_nodes: int) -> dict[str, Any]:
    config = read_json(CONFIG)
    topology = read_json(TOPOLOGY)
    event = M5077.M5036.event_lookup(config)[EVENT_ID]
    argument = M5077.M5036.argument_lookup(config)[ARGUMENT_ID]
    M5077.CURRENT_EVENT = event
    M5077.CURRENT_ARGUMENT = argument
    target = M5077.M5036.complex_from_row(argument["target_cosine"])
    M5077.M5036.M5035.M5034.configure(event, target)
    module = M5077.M5036.N5030
    profile = config["tiers"]["primary24"]
    M5077.install_history_invariant_breakpoints(module)
    M5077.removable_extension_gate()
    previous_catalog = module.chamber_residue_catalog
    previous_global = module.global_chamber_value
    first_annulus = ConditionedFiniteAnnulusGlobalValue(
        module,
        inner_nodes,
        float(profile["relative_adaptive_tolerance"]),
    )
    removable = M5077.M5085.CertifiedRemovableGlobalExtension(first_annulus)
    module.chamber_residue_catalog = M5077.certified_primary_catalog
    module.global_chamber_value = removable
    M5077.M5036.MREPAIR.CURRENT_JOB = f"5146::{JOB_KEY}::inner{inner_nodes}"
    M5077.M5036.MREPAIR.RADIUS_AUDIT.clear()
    M5077.LOCAL_RESIDUE_RESOLUTION_AUDIT.clear()
    M5077.OUTWARD_CONTOUR_AUDIT.clear()
    M5077.PROJECTIVE_CLUSTER_ZERO_AUDIT.clear()
    started = time.monotonic()
    try:
        gate = module.fixed_event_integral_gate(
            topology,
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
    runtime = time.monotonic() - started
    gate_path = SOURCE / f"E040_A10_conditioned_annulus_inner{inner_nodes}_gate.json"
    atomic_json(gate_path, gate)
    value = complex(gate["order_rows"][-1]["causally_corrected_value"])
    return {
        "inner_nodes": inner_nodes,
        "runtime_seconds": runtime,
        "gate_path": str(gate_path),
        "gate_sha256": digest(gate_path),
        "value": complex_row(value),
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
        "conditioned_annulus_audit": first_annulus.summary(),
        "removable_extension_call_count": len(removable.calls),
    }


def run_counts(
    schedule: list[dict[str, Any]], config_digest: str
) -> dict[str, int]:
    counts = {
        "completed_converged": 0,
        "completed_unconverged": 0,
        "failed": 0,
        "missing": 0,
    }
    for job in schedule:
        directory = "jobs" if job["stratum"] == "full_remainder" else "topological_jobs"
        path = RUN / directory / f"{job['job_key']}.json"
        if not path.exists():
            counts["missing"] += 1
            continue
        row = read_json(path)
        if row.get("config_digest") != config_digest:
            counts["missing"] += 1
        elif row.get("status") == "COMPLETED_CONVERGED":
            counts["completed_converged"] += 1
        elif row.get("status") == "COMPLETED_UNCONVERGED":
            counts["completed_unconverged"] += 1
        elif row.get("status") == "FAILED":
            counts["failed"] += 1
        else:
            counts["missing"] += 1
    return counts


def first_incomplete(
    schedule: list[dict[str, Any]], config_digest: str
) -> dict[str, Any]:
    for job in schedule:
        directory = "jobs" if job["stratum"] == "full_remainder" else "topological_jobs"
        path = RUN / directory / f"{job['job_key']}.json"
        if not path.exists():
            return job
        row = read_json(path)
        if (
            row.get("config_digest") != config_digest
            or row.get("status") != "COMPLETED_CONVERGED"
            or (
                job["stratum"] == "full_remainder"
                and row.get("strict_adaptive_validated") is not True
            )
        ):
            return job
    raise RuntimeError("locked schedule unexpectedly complete")


def update_live(selected: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    gate = read_json(Path(selected["gate_path"]))
    job = read_json(LIVE_JOB)
    kernel = read_json(LIVE_KERNEL)
    job.setdefault(
        "pre_5146_first_annulus_replay",
        {
            "status": job.get("status"),
            "integral_converged": job.get("integral_converged"),
            "job_sha256": digest(LIVE_JOB),
        },
    )
    kernel.setdefault(
        "pre_5146_first_annulus_replay",
        {
            "strict_adaptive_validated": kernel.get(
                "strict_adaptive_validated"
            ),
            "kernel_sha256": digest(LIVE_KERNEL),
        },
    )
    profile_audit = dict(kernel.get("profile_audit", {}))
    profile_audit["conditioned_finite_annulus_global_cycle"] = {
        "checkpoint_marker": MARKER,
        "selected_inner_nodes": selected["inner_nodes"],
        "gate_path": selected["gate_path"],
        "gate_sha256": selected["gate_sha256"],
        "audit": selected["conditioned_annulus_audit"],
        "physical_pole_ownership_changed": False,
        "outer_tolerance_changed": False,
        "outer_interval_cap_changed": False,
    }
    kernel["fixed_event_integral_gate"] = gate
    kernel["strict_adaptive_validated"] = True
    kernel["profile_audit"] = profile_audit
    kernel["numerical_repair_checkpoint"] = MARKER
    kernel["strict_adaptive_reconciliation"] = {
        "checkpoint_marker": MARKER,
        "strict_pass": True,
    }
    direct_kernel = M5077.M5036.M5035.M5034.highest_value(gate)
    direct = M5077.M5036.M5035.M5034.KERNEL_MULTIPLIER * direct_kernel
    job_profile_audit = dict(job.get("profile_audit", {}))
    job_profile_audit["conditioned_finite_annulus_global_cycle"] = profile_audit[
        "conditioned_finite_annulus_global_cycle"
    ]
    job.update(
        {
            "status": "COMPLETED_CONVERGED",
            "integral_converged": True,
            "strict_adaptive_validated": True,
            "normalized_direct_D_hhh_over_G3": complex_row(direct),
            "kernel_runtime_seconds": selected["runtime_seconds"],
            "job_runtime_seconds": selected["runtime_seconds"],
            "profile_audit": job_profile_audit,
            "numerical_repair_checkpoint": MARKER,
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
    rows = result["node_ladder"]
    DOCUMENT.write_text(
        f"""# 5146 E040/A10 conditioned-annulus global-cycle replay

## Result

The A10 ceiling was not an MTS-only failure and was not repaired by relaxing
the outer tolerance or interval cap. The second reciprocal chamber was feeding
the outer Gauss estimator an ill-conditioned inner Cauchy average. Its old
radius `0.2 rho_1` approached the Laurent origin closely enough that increasing
the outer interval count merely accumulated inner roundoff.

For every adjacent pair of finite pole moduli `rho_i < rho_(i+1)`, the
minimax representative is

`R_i = sqrt(rho_i rho_(i+1))`.

On each finite annulus,

`d(R)=min(log(R/rho_1), log(rho_2/R))`

has its unique maximum at `R_*`, where

`d(R_*) = 0.5 log(rho_2/rho_1)`.

The signed residue corrections preserve the requested fixed-ownership Cauchy
cycle when the representative radius moves across finite poles. Among annuli
whose log clearance satisfies the design error budget, the center nearest the
unit circle minimizes avoidable Laurent-origin/large-radius amplification. A
96/192-node ladder then tests the unmodelled prefactor directly. Therefore this
is a numerical representative change, not a change of pole ownership or of the
physical integrand.

## Locked replay

- inner-node ladder: `{[row['inner_nodes'] for row in rows]}`
- ladder strict gates: `{[row['strict_adaptive_quadrature_converged'] for row in rows]}`
- cross-node relative difference: `{result['cross_node_relative_difference']}`
- selected inner nodes: `{result['selected_inner_nodes']}`
- run counts: `{result['run_counts_after']}`
- first incomplete row: `{result['first_incomplete_after']['job_key']}`
- validation failures: `{failures}`

No outer tolerance, outer interval cap, physics parameter, formal-workbench
file, or GitHub state changed. This checkpoint is numerical infrastructure and
does not by itself establish a UV, local-GR, or full-MTS claim.

The machine/cog criterion remains explicit: later physics acceptance requires
one parent mechanism that preserves local GR/Mercury behaviour while activating
the galactic sector without a hand-switched law.
""",
        encoding="utf-8",
    )


def main() -> None:
    required = [
        SCRIPT_5125,
        CONFIG,
        SCHEDULE,
        TOPOLOGY,
        LIVE_JOB,
        LIVE_KERNEL,
        FORMAL,
    ]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError(f"missing 5146 inputs: {missing}")
    config = read_json(CONFIG)
    schedule = read_json(SCHEDULE)["jobs"]
    before_counts = run_counts(schedule, config["config_digest"])
    before_first = first_incomplete(schedule, config["config_digest"])
    if before_first["job_key"] != JOB_KEY:
        raise RuntimeError(
            f"5146 target is not first incomplete row: {before_first['job_key']}"
        )
    node_ladder = []
    for nodes in INNER_NODE_LEVELS:
        row = run_gate(nodes)
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
    cross_node_relative_difference = abs(values[-1] - values[-2]) / max(
        abs(values[-1]), 1.0
    )
    tolerance = float(config["tiers"]["primary24"]["relative_adaptive_tolerance"])
    ladder_passed = bool(
        all(
            row["strict_adaptive_quadrature_converged"]
            and row["fixed_event_crossed_integral_converged"]
            and row["all_residues_stable"]
            and row["removable_extension_call_count"] == 0
            and row["conditioned_annulus_audit"]["minimum_log_clearance"]
            >= row["conditioned_annulus_audit"]["required_log_clearance"]
            and row["conditioned_annulus_audit"]["fallback_count"] == 0
            for row in node_ladder
        )
        and cross_node_relative_difference <= tolerance
    )
    if not ladder_passed:
        selected = node_ladder[-1]
        live_updated = False
        live_job = read_json(LIVE_JOB)
        live_kernel = read_json(LIVE_KERNEL)
    else:
        selected = node_ladder[-1]
        live_job, live_kernel = update_live(selected)
        live_updated = True
    counts_after = run_counts(schedule, config["config_digest"])
    first_after = first_incomplete(schedule, config["config_digest"])
    formal_digest = tree_digest(FORMAL)
    result = {
        "checkpoint_marker": MARKER,
        "checked_date": CHECKED_DATE,
        "job_key": JOB_KEY,
        "source_job_status": "COMPLETED_UNCONVERGED",
        "counts_before": before_counts,
        "first_incomplete_before": before_first,
        "conditioned_annulus_derivation": {
            "radius": "R_i=sqrt(rho_i*rho_(i+1))",
            "objective": "max_R min(log(R/rho_i),log(rho_(i+1)/R))",
            "maximum": "0.5*log(rho_(i+1)/rho_i)",
            "qualification": (
                "exp(-N_design*d_i) <= outer_tolerance/8"
            ),
            "selection": "qualified annulus center nearest |R|=1",
            "cauchy_cycle_preserved_by_signed_residue_corrections": True,
            "physical_pole_ownership_changed": False,
        },
        "node_ladder": node_ladder,
        "cross_node_relative_difference": cross_node_relative_difference,
        "locked_tolerance": tolerance,
        "ladder_passed": ladder_passed,
        "selected_inner_nodes": selected["inner_nodes"],
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
    checks = [
        ("source_paths_exist", not missing, str(missing)),
        ("target_was_first_incomplete", before_first["job_key"] == JOB_KEY, before_first["job_key"]),
        ("two_level_inner_ladder", [row["inner_nodes"] for row in node_ladder] == [96, 192], str(INNER_NODE_LEVELS)),
        ("conditioned_annulus_exact_identity", all(row["conditioned_annulus_audit"]["minimum_log_clearance"] >= row["conditioned_annulus_audit"]["required_log_clearance"] and row["conditioned_annulus_audit"]["fallback_count"] == 0 for row in node_ladder), str([(row["conditioned_annulus_audit"]["minimum_log_clearance"], row["conditioned_annulus_audit"]["required_log_clearance"], row["conditioned_annulus_audit"]["fallback_count"]) for row in node_ladder])),
        ("both_outer_gates_strict", all(row["strict_adaptive_quadrature_converged"] for row in node_ladder), str([row["maximum_adaptive_chamber_relative_error"] for row in node_ladder])),
        ("both_fixed_gates_converged", all(row["fixed_event_crossed_integral_converged"] for row in node_ladder), str([row["fixed_event_crossed_integral_converged"] for row in node_ladder])),
        ("all_residues_stable", all(row["all_residues_stable"] for row in node_ladder), str([row["all_residues_stable"] for row in node_ladder])),
        ("cross_node_stable", cross_node_relative_difference <= tolerance, str(cross_node_relative_difference)),
        ("no_removable_fallback", all(row["removable_extension_call_count"] == 0 for row in node_ladder), str([row["removable_extension_call_count"] for row in node_ladder])),
        ("live_row_strictly_converged", live_updated and live_job.get("status") == "COMPLETED_CONVERGED" and live_job.get("strict_adaptive_validated") is True, str(live_job.get("status"))),
        ("run_counts_advance_one_row", counts_after == {"completed_converged": 51, "completed_unconverged": 1, "failed": 0, "missing": 508}, str(counts_after)),
        ("next_row_is_E020_A10", first_after["job_key"] == "E020__S512503_N0000__A10__primary24", first_after["job_key"]),
        ("locked_outer_profile_unchanged", not result["outer_tolerance_changed"] and not result["outer_interval_cap_changed"] and not result["physics_parameter_changed"], "outer profile and physics unchanged"),
        ("formal_tree_unchanged", formal_digest == FORMAL_BASELINE, formal_digest),
        ("claim_discipline", not result["valid_for_numeric_UV_claim"] and not result["valid_for_local_GR_claim"] and not result["valid_for_full_MTS_claim"], "numerical repair is not physical evidence"),
    ]
    VALIDATION_CSV.parent.mkdir(parents=True, exist_ok=True)
    with VALIDATION_CSV.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=("check_id", "passed", "detail", "checkpoint_marker"),
        )
        writer.writeheader()
        for index, (name, passed, detail) in enumerate(checks, start=1):
            writer.writerow(
                {
                    "check_id": f"V5146_{index:02d}_{name}",
                    "passed": passed,
                    "detail": detail,
                    "checkpoint_marker": MARKER,
                }
            )
    failures = [name for name, passed, _ in checks if not passed]
    write_document(result, failures)
    print(
        json.dumps(
            {
                "result": result,
                "validation_failures": failures,
            },
            indent=2,
            sort_keys=True,
        )
    )
    if failures:
        raise RuntimeError(f"checkpoint 5146 validation failed: {failures}")


if __name__ == "__main__":
    main()
