from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
from typing import Any, Callable

import numpy as np


POST = Path(__file__).resolve().parents[1]
SCRIPT_5077 = POST / "scripts" / "Y5_R2FR_5077_central_anchor_pilot_runner.py"
PILOT_V6 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5079"
    / "runs"
    / "bounded_central_anchor_pilot_v6"
)
SOURCE = POST / "source-intake" / "functional_rg" / "5087"
RESULT_JSON = SOURCE / "finer_removable_limit_certificate.json"
GATE_JSON = SOURCE / "E020_A07_primary24_finer_limit_gate.json"
VALIDATION_CSV = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5087_VALIDATION.csv"
)
MARKER = "MTS_5087_FINER_REMOVABLE_LIMIT_CERTIFICATE"
REVISION = "four-level-fallback-with-unchanged-one-e-minus-seven-gate-v1"
FORMAL_BASELINE = (
    "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
)
EVENT_ID = "S507603_N0000"
ARGUMENT_ID = "E020_A07"
BASE_ARGUMENT_ID = "A07"
PROFILE = "primary24"
OLD_LEVELS = (3.125e-5, 1.5625e-5, 7.8125e-6)
NEW_LEVELS = (*OLD_LEVELS, 3.90625e-6)
DIRECTIONS = (1.0 + 0.0j, 0.0 + 1.0j, complex(np.exp(0.37j)))
UNCHANGED_TOLERANCE = 1.0e-7


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(value, indent=2, sort_keys=True), encoding="utf-8"
    )
    os.replace(temporary, path)


def serialized(value: complex) -> dict[str, float]:
    return {"real": float(value.real), "imaginary": float(value.imag)}


def ownership_digest(ownership: dict[str, bool]) -> str:
    payload = json.dumps(ownership, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def symmetric_limit_audit(
    relative_circle: complex,
    ownership: dict[str, bool],
    global_nodes: int,
    global_residue_nodes: int,
    original: Callable[[complex, dict[str, bool], int, int], complex],
    labels: tuple[str, ...],
    levels: tuple[float, ...],
) -> tuple[complex, dict[str, Any]]:
    scale = max(abs(relative_circle), 1.0e-6)
    direction_rows = []
    limits = []
    for direction in DIRECTIONS:
        level_rows = []
        averages = []
        for fraction in levels:
            offset = fraction * scale * direction
            minus = original(
                relative_circle - offset,
                ownership,
                global_nodes,
                global_residue_nodes,
            )
            plus = original(
                relative_circle + offset,
                ownership,
                global_nodes,
                global_residue_nodes,
            )
            average = (minus + plus) / 2.0
            averages.append(average)
            level_rows.append(
                {
                    "fraction": fraction,
                    "minus": serialized(minus),
                    "plus": serialized(plus),
                    "symmetric_average": serialized(average),
                    "side_difference": float(abs(minus - plus)),
                }
            )
        limit = (4.0 * averages[-1] - averages[-2]) / 3.0
        convergence = abs(averages[-1] - averages[-2]) / max(1.0, abs(limit))
        limits.append(limit)
        direction_rows.append(
            {
                "direction": serialized(direction),
                "levels": level_rows,
                "richardson_limit": serialized(limit),
                "finest_average_relative_change": float(convergence),
            }
        )
    mean_limit = sum(limits) / len(limits)
    direction_spread = max(abs(value - mean_limit) for value in limits) / max(
        1.0, abs(mean_limit)
    )
    maximum_convergence = max(
        row["finest_average_relative_change"] for row in direction_rows
    )
    accepted = bool(
        maximum_convergence < UNCHANGED_TOLERANCE
        and direction_spread < UNCHANGED_TOLERANCE
        and math.isfinite(mean_limit.real)
        and math.isfinite(mean_limit.imag)
    )
    return mean_limit, {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "relative_circle": serialized(relative_circle),
        "labels": list(labels),
        "ownership_digest": ownership_digest(ownership),
        "global_nodes": int(global_nodes),
        "global_residue_nodes": int(global_residue_nodes),
        "levels": list(levels),
        "directions": direction_rows,
        "returned_limit": serialized(mean_limit),
        "maximum_directional_convergence_residual": float(maximum_convergence),
        "direction_independence_relative_spread": float(direction_spread),
        "tolerance": UNCHANGED_TOLERANCE,
        "accepted": accepted,
        "valid_for_full_MTS_claim": False,
    }


class FinerCertifiedRemovableGlobalExtension:
    def __init__(
        self,
        original: Callable[[complex, dict[str, bool], int, int], complex],
        module_5085: Any,
    ) -> None:
        self.original = original
        self.module_5085 = module_5085
        self.calls: list[dict[str, Any]] = []
        self.cache: dict[tuple[Any, ...], complex] = {}

    def __call__(
        self,
        relative_circle: complex,
        ownership: dict[str, bool],
        global_nodes: int,
        global_residue_nodes: int,
    ) -> complex:
        try:
            return self.original(
                relative_circle,
                ownership,
                global_nodes,
                global_residue_nodes,
            )
        except RuntimeError as error:
            labels = self.module_5085.labels_from_error(error)
            if not self.module_5085.eligible_collision(labels, ownership):
                raise
            key = (
                round(relative_circle.real, 11),
                round(relative_circle.imag, 11),
                tuple(sorted(labels)),
                ownership_digest(ownership),
                int(global_nodes),
                int(global_residue_nodes),
            )
            if key in self.cache:
                return self.cache[key]
            old_value, old_audit = symmetric_limit_audit(
                relative_circle,
                ownership,
                global_nodes,
                global_residue_nodes,
                self.original,
                labels,
                OLD_LEVELS,
            )
            selected_value = old_value
            selected_audit = old_audit
            selected_mode = "unchanged_5085_three_level"
            refinement_used = False
            contraction_passed = True
            new_audit = None
            if not old_audit["accepted"]:
                refinement_used = True
                selected_mode = "5087_four_level_fallback"
                selected_value, new_audit = symmetric_limit_audit(
                    relative_circle,
                    ownership,
                    global_nodes,
                    global_residue_nodes,
                    self.original,
                    labels,
                    NEW_LEVELS,
                )
                selected_audit = new_audit
                contraction_passed = bool(
                    new_audit["maximum_directional_convergence_residual"]
                    < old_audit["maximum_directional_convergence_residual"]
                    and new_audit["direction_independence_relative_spread"]
                    < old_audit["direction_independence_relative_spread"]
                )
            call = {
                "checkpoint_marker": MARKER,
                "revision": REVISION,
                "original_error": str(error),
                "selected_mode": selected_mode,
                "refinement_used": refinement_used,
                "old_three_level_audit": old_audit,
                "new_four_level_audit": new_audit,
                "selected_limit": serialized(selected_value),
                "selected_audit": selected_audit,
                "contraction_passed": contraction_passed,
                "valid_for_full_MTS_claim": False,
            }
            self.calls.append(call)
            if not selected_audit["accepted"] or not contraction_passed:
                raise RuntimeError(
                    "5087 finer removable extension did not converge: "
                    f"convergence={selected_audit['maximum_directional_convergence_residual']}, "
                    f"direction_spread={selected_audit['direction_independence_relative_spread']}"
                )
            self.cache[key] = selected_value
            return selected_value


def main() -> None:
    topology_path = PILOT_V6 / "topologies" / f"{EVENT_ID}__{ARGUMENT_ID}.json"
    failed_job_path = (
        PILOT_V6
        / "jobs"
        / f"E020__{EVENT_ID}__{BASE_ARGUMENT_ID}__{PROFILE}.json"
    )
    required = [
        SCRIPT_5077,
        PILOT_V6 / "config.json",
        topology_path,
        failed_job_path,
    ]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError(f"missing 5087 inputs: {missing}")
    module_5077 = load_module("mts_5077_for_5087", SCRIPT_5077)
    module_5085 = module_5077.M5085
    config = json.loads((PILOT_V6 / "config.json").read_text(encoding="utf-8"))
    event = module_5077.M5036.event_lookup(config)[EVENT_ID]
    argument = module_5077.M5036.argument_lookup(config)[ARGUMENT_ID]
    target = module_5077.M5036.complex_from_row(argument["target_cosine"])
    module_5077.M5036.M5035.M5034.configure(event, target)
    numerical_module = module_5077.M5036.N5030
    topology = json.loads(topology_path.read_text(encoding="utf-8"))
    profile = config["tiers"][PROFILE]
    previous_catalog = numerical_module.chamber_residue_catalog
    previous_global = numerical_module.global_chamber_value
    extension = FinerCertifiedRemovableGlobalExtension(
        previous_global, module_5085
    )
    numerical_module.chamber_residue_catalog = module_5077.certified_primary_catalog
    numerical_module.global_chamber_value = extension
    module_5077.M5036.MREPAIR.CURRENT_JOB = "5087::E020_A07_primary24"
    module_5077.M5036.MREPAIR.RADIUS_AUDIT.clear()
    module_5077.LOCAL_ZERO_AUDIT.clear()
    module_5077.OUTWARD_CONTOUR_AUDIT.clear()
    gate = None
    gate_error = None
    try:
        gate = numerical_module.fixed_event_integral_gate(
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
    except Exception as error:
        gate_error = f"{type(error).__name__}: {error}"
    finally:
        numerical_module.chamber_residue_catalog = previous_catalog
        numerical_module.global_chamber_value = previous_global
    refinement_calls = [row for row in extension.calls if row["refinement_used"]]
    unchanged_calls = [row for row in extension.calls if not row["refinement_used"]]
    all_refinements_accepted = bool(
        refinement_calls
        and all(
            row["new_four_level_audit"]["accepted"]
            and row["contraction_passed"]
            for row in refinement_calls
        )
    )
    numerical_route_rejected = bool(
        refinement_calls
        and not all_refinements_accepted
        and gate_error is not None
        and "5087 finer removable extension did not converge" in gate_error
    )
    gate_converged = bool(
        gate is not None and gate["fixed_event_crossed_integral_converged"]
    )
    gate_residues_stable = bool(gate is not None and gate["all_residues_stable"])
    gate_result = {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "event_id": EVENT_ID,
        "argument_id": ARGUMENT_ID,
        "profile": PROFILE,
        "converged": gate_converged,
        "all_residues_stable": gate_residues_stable,
        "highest_two_order_relative_residual": (
            float(gate["highest_two_order_relative_residual"])
            if gate is not None
            else None
        ),
        "highest_value": (
            module_5077.M5036.complex_row(
                module_5077.M5036.M5035.M5034.highest_value(gate)
            )
            if gate is not None
            else None
        ),
        "gate_error": gate_error,
        "numerical_route_rejected": numerical_route_rejected,
        "extension_call_count": len(extension.calls),
        "refinement_call_count": len(refinement_calls),
        "unchanged_5085_call_count": len(unchanged_calls),
        "extension_calls": extension.calls,
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(GATE_JSON, gate_result)
    failed_job = json.loads(failed_job_path.read_text(encoding="utf-8"))
    accepted = bool(
        failed_job["status"] == "FAILED"
        and "5085 removable extension did not converge" in failed_job["error"]
        and all_refinements_accepted
        and gate_converged
        and gate_residues_stable
        and gate_result["refinement_call_count"] > 0
    )
    result = {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "event_id": EVENT_ID,
        "argument_id": ARGUMENT_ID,
        "profile": PROFILE,
        "old_levels": list(OLD_LEVELS),
        "new_levels": list(NEW_LEVELS),
        "added_level": NEW_LEVELS[-1],
        "tolerance_before": UNCHANGED_TOLERANCE,
        "tolerance_after": UNCHANGED_TOLERANCE,
        "tolerance_relaxed": False,
        "old_failure": failed_job,
        "gate_path": str(GATE_JSON),
        "gate_sha256": digest(GATE_JSON),
        "refinement_calls": refinement_calls,
        "unchanged_5085_calls": unchanged_calls,
        "all_refinements_accepted": all_refinements_accepted,
        "finer_removable_limit_certificate_accepted": accepted,
        "numerical_removable_extension_route_rejected": numerical_route_rejected,
        "decision": (
            "ACCEPT_FOUR_LEVEL_EXTENSION"
            if accepted
            else "REJECT_NUMERICAL_REMOVABLE_EXTENSION"
            if numerical_route_rejected
            else "INDETERMINATE"
        ),
        "runner_integration_authorized": accepted,
        "next_route": (
            "integrate guarded four-level extension"
            if accepted
            else "derive exact local Laurent/pinch classification"
        ),
        "pilot_result_claimed": False,
        "formalization_workbench_tree_sha256": FORMAL_BASELINE,
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(RESULT_JSON, result)
    checks = [
        ("source_paths_exist", not missing, "all exact-row inputs exist"),
        (
            "old_failure_reproduced",
            failed_job["status"] == "FAILED"
            and "5085 removable extension did not converge" in failed_job["error"],
            failed_job.get("error", ""),
        ),
        (
            "one_predeclared_level_added",
            NEW_LEVELS == (*OLD_LEVELS, 3.90625e-6),
            str(NEW_LEVELS),
        ),
        (
            "tolerance_unchanged",
            not result["tolerance_relaxed"]
            and result["tolerance_before"] == result["tolerance_after"],
            str(UNCHANGED_TOLERANCE),
        ),
        (
            "refinement_exercised",
            gate_result["refinement_call_count"] > 0,
            f"count={gate_result['refinement_call_count']}",
        ),
        (
            "refinement_decision_recorded",
            all_refinements_accepted or numerical_route_rejected,
            f"accepted={all_refinements_accepted}; rejected={numerical_route_rejected}",
        ),
        (
            "failed_row_fail_closed",
            (gate_converged and gate_residues_stable) or numerical_route_rejected,
            gate_error or f"residual={gate_result['highest_two_order_relative_residual']}",
        ),
        (
            "integration_authorization_consistent",
            result["runner_integration_authorized"] == accepted
            and not (numerical_route_rejected and accepted),
            result["decision"],
        ),
        (
            "formalization_unchanged",
            result["formalization_workbench_tree_sha256"] == FORMAL_BASELINE,
            result["formalization_workbench_tree_sha256"],
        ),
        (
            "claim_discipline",
            not result["pilot_result_claimed"]
            and not result["valid_for_full_MTS_claim"],
            "exact numerical repair is not physical evidence",
        ),
    ]
    VALIDATION_CSV.parent.mkdir(parents=True, exist_ok=True)
    with VALIDATION_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=("check_id", "passed", "detail", "checkpoint_marker"),
        )
        writer.writeheader()
        for index, (name, passed, detail) in enumerate(checks, start=1):
            writer.writerow(
                {
                    "check_id": f"V5087_{index:02d}_{name}",
                    "passed": bool(passed),
                    "detail": detail,
                    "checkpoint_marker": MARKER,
                }
            )
    failed = [name for name, passed, _ in checks if not passed]
    if failed:
        raise RuntimeError(f"checkpoint 5087 validation failed: {failed}")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
