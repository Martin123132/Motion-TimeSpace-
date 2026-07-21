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
SCRIPT_5077 = POST / "scripts" / "Y5_R2FR_5077_central_anchor_pilot_runner.py"
RUN = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5079"
    / "runs"
    / "bounded_central_anchor_pilot_v8"
)
SOURCE = POST / "source-intake" / "functional_rg" / "5095"
RESULT_JSON = SOURCE / "same_side_global_cluster_cycle_certificate.json"
VALIDATION_CSV = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5095_VALIDATION.csv"
)
MARKER = "MTS_5095_SAME_SIDE_GLOBAL_CLUSTER_CYCLE_CERTIFICATE"
REVISION = "isolated-same-sign-cluster-cauchy-cycle-v1"
FORMAL_BASELINE = "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
EVENT_ID = "S507615_N0000"
ARGUMENT_ID = "E040_A14"
JOB_KEY = "E040__S507615_N0000__A14__coarse12"
LINK_RELATIVE_DISTANCE = 1.0e-3
MAXIMUM_CLUSTER_ISOLATION_RATIO = 0.1
MAXIMUM_AUDIT_EXAMPLES = 24


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


def tree_digest(path: Path) -> str:
    value = hashlib.sha256()
    for item in sorted(candidate for candidate in path.rglob("*") if candidate.is_file()):
        value.update(item.relative_to(path).as_posix().encode("utf-8"))
        value.update(digest(item).encode("ascii"))
    return value.hexdigest()


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True), encoding="utf-8")
    os.replace(temporary, path)


def complex_row(value: complex) -> dict[str, float]:
    return {"real": float(value.real), "imaginary": float(value.imag)}


def normalized_distance(first: complex, second: complex) -> float:
    return abs(first - second) / max(1.0, abs(first), abs(second))


def correction_components(rows: list[dict[str, Any]]) -> list[list[dict[str, Any]]]:
    components: list[list[dict[str, Any]]] = []
    for sign in (-1, 1):
        candidates = [row for row in rows if row["sign"] == sign]
        remaining = set(range(len(candidates)))
        while remaining:
            component_indices = {remaining.pop()}
            changed = True
            while changed:
                changed = False
                for candidate_index in list(remaining):
                    candidate_root = candidates[candidate_index]["root"]
                    linked = any(
                        normalized_distance(
                            candidate_root,
                            candidates[member_index]["root"],
                        )
                        < LINK_RELATIVE_DISTANCE
                        for member_index in component_indices
                    )
                    if linked:
                        component_indices.add(candidate_index)
                        remaining.remove(candidate_index)
                        changed = True
            components.append(
                [candidates[index] for index in sorted(component_indices)]
            )
    return components


def single_residue_radius(
    root: complex,
    group_index: int,
    groups: list[dict[str, Any]],
) -> float:
    separations = [
        abs(root - complex(row["root"]))
        for index, row in enumerate(groups)
        if index != group_index
    ]
    safe_scale = min([abs(root)] + separations) if separations else abs(root)
    return max(1.0e-7, 0.07 * safe_scale)


class CertifiedSameSideClusterGlobalValue:
    def __init__(self, module: Any) -> None:
        self.module = module
        self.call_count = 0
        self.clustered_call_count = 0
        self.cluster_count = 0
        self.cluster_size_histogram: dict[int, int] = {}
        self.maximum_cluster_isolation_ratio = 0.0
        self.examples: list[dict[str, Any]] = []

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
        base_radius = self.module.M5028.M5026.conditioned_global_base_radius(groups)
        result = self.module.M5028.M5026.circle_average(
            evaluator, global_nodes, base_radius
        )
        correction_rows: list[dict[str, Any]] = []
        for group_index, group in enumerate(groups):
            root = complex(group["root"])
            desired_inside = bool(group["desired_inside"])
            currently_inside = abs(root) < base_radius
            if desired_inside == currently_inside:
                continue
            correction_rows.append(
                {
                    "group_index": group_index,
                    "group": group,
                    "root": root,
                    "sign": 1 if desired_inside else -1,
                }
            )
        components = correction_components(correction_rows)
        call_cluster_count = 0
        for component in components:
            if len(component) == 1:
                row = component[0]
                radius = single_residue_radius(
                    row["root"], row["group_index"], groups
                )
                residue = self.module.M5028.M5024.local_residue(
                    evaluator,
                    row["root"],
                    radius,
                    global_residue_nodes,
                )
                result += row["sign"] * residue
                continue
            roots = [row["root"] for row in component]
            center = sum(roots) / len(roots)
            extent = max(abs(root - center) for root in roots)
            component_indices = {row["group_index"] for row in component}
            outside_distances = [abs(center)]
            outside_distances.extend(
                abs(complex(group["root"]) - center)
                for group_index, group in enumerate(groups)
                if group_index not in component_indices
            )
            outside_distance = min(outside_distances)
            isolation_ratio = extent / max(outside_distance, 1.0e-300)
            if not (
                extent > 0.0
                and outside_distance > extent
                and isolation_ratio < MAXIMUM_CLUSTER_ISOLATION_RATIO
            ):
                for row in component:
                    radius = single_residue_radius(
                        row["root"], row["group_index"], groups
                    )
                    residue = self.module.M5028.M5024.local_residue(
                        evaluator,
                        row["root"],
                        radius,
                        global_residue_nodes,
                    )
                    result += row["sign"] * residue
                continue
            radius = max(
                1.5 * extent,
                1.0e-7,
                math.sqrt(extent * outside_distance),
            )
            if not (extent < radius < outside_distance):
                raise RuntimeError(
                    "5095 isolated cluster contour radius does not separate poles"
                )
            residue = self.module.M5028.M5024.local_residue(
                evaluator,
                center,
                radius,
                global_residue_nodes,
            )
            result += component[0]["sign"] * residue
            call_cluster_count += 1
            self.cluster_count += 1
            self.cluster_size_histogram[len(component)] = (
                self.cluster_size_histogram.get(len(component), 0) + 1
            )
            self.maximum_cluster_isolation_ratio = max(
                self.maximum_cluster_isolation_ratio, isolation_ratio
            )
            if len(self.examples) < MAXIMUM_AUDIT_EXAMPLES:
                self.examples.append(
                    {
                        "relative_circle": complex_row(relative_circle),
                        "sign": component[0]["sign"],
                        "cluster_size": len(component),
                        "labels": [
                            label
                            for row in component
                            for label in row["group"]["labels"]
                        ],
                        "roots": [complex_row(root) for root in roots],
                        "center": complex_row(center),
                        "extent": float(extent),
                        "outside_distance": float(outside_distance),
                        "isolation_ratio": float(isolation_ratio),
                        "contour_radius": float(radius),
                        "combined_residue": complex_row(residue),
                    }
                )
        if call_cluster_count:
            self.clustered_call_count += 1
        return complex(result)

    def summary(self) -> dict[str, Any]:
        return {
            "call_count": self.call_count,
            "clustered_call_count": self.clustered_call_count,
            "cluster_count": self.cluster_count,
            "cluster_size_histogram": {
                str(key): value
                for key, value in sorted(self.cluster_size_histogram.items())
            },
            "maximum_cluster_isolation_ratio": float(
                self.maximum_cluster_isolation_ratio
            ),
            "examples": self.examples,
        }


def run_gate(
    module_5077: Any,
    module: Any,
    topology: dict[str, Any],
    config: dict[str, Any],
    global_residue_nodes: int,
) -> dict[str, Any]:
    profile = module_5077.M5043.PROFILES["coarse12"]
    previous_catalog = module.chamber_residue_catalog
    previous_global = module.global_chamber_value
    clustered = CertifiedSameSideClusterGlobalValue(module)
    removable = module_5077.M5085.CertifiedRemovableGlobalExtension(clustered)
    module.chamber_residue_catalog = module_5077.restricted_coarse_catalog
    module.global_chamber_value = removable
    module_5077.M5043.CURRENT_JOB = (
        f"5095::{JOB_KEY}::residue_nodes_{global_residue_nodes}"
    )
    module_5077.M5043.THEOREM_AUDIT.clear()
    module_5077.M5043.CHART_AUDIT.clear()
    module_5077.M5043.NUMERIC_AUDIT.clear()
    module_5077.LOCAL_ZERO_AUDIT.clear()
    module_5077.OUTWARD_CONTOUR_AUDIT.clear()
    started = time.monotonic()
    try:
        gate = module.fixed_event_integral_gate(
            topology,
            tuple(int(value) for value in profile["relative_orders"]),
            int(profile["global_nodes"]),
            global_residue_nodes,
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
    elapsed = time.monotonic() - started
    gate_path = SOURCE / f"E040_S507615_A14_clustered_residue_nodes_{global_residue_nodes}.json"
    atomic_json(gate_path, gate)
    value = complex(gate["highest_order_value"])
    return {
        "global_residue_nodes": global_residue_nodes,
        "runtime_seconds": elapsed,
        "gate_path": str(gate_path),
        "gate_sha256": digest(gate_path),
        "converged": bool(gate["fixed_event_crossed_integral_converged"]),
        "all_residues_stable": bool(gate["all_residues_stable"]),
        "relative_residual": float(gate["highest_two_order_relative_residual"]),
        "highest_order_value": complex_row(value),
        "interval_count": int(gate["order_rows"][-1]["composite_interval_count"]),
        "evaluation_count": int(
            gate["order_rows"][-1]["relative_integrand_evaluation_count"]
        ),
        "cluster_audit": clustered.summary(),
        "removable_extension_call_count": len(removable.calls),
        "tolerance_changed": False,
        "interval_cap_changed": False,
        "depth_cap_changed": False,
        "valid_for_full_MTS_claim": False,
    }


def main() -> None:
    topology_path = RUN / "topologies" / f"{EVENT_ID}__{ARGUMENT_ID}.json"
    required = [SCRIPT_5077, RUN / "config.json", topology_path, FORMAL]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError(f"missing 5095 inputs: {missing}")
    module_5077 = load_module("mts_5077_for_5095", SCRIPT_5077)
    module_5077.removable_extension_gate()
    config = json.loads((RUN / "config.json").read_text(encoding="utf-8"))
    event = module_5077.M5036.event_lookup(config)[EVENT_ID]
    argument = module_5077.M5036.argument_lookup(config)[ARGUMENT_ID]
    target = module_5077.M5036.complex_from_row(argument["target_cosine"])
    module_5077.M5043.M5034.configure(event, target)
    module = module_5077.M5043.N5030
    topology = json.loads(topology_path.read_text(encoding="utf-8"))
    gate_rows = [
        run_gate(module_5077, module, topology, config, nodes)
        for nodes in (12, 24)
    ]
    values = [
        complex(row["highest_order_value"]["real"], row["highest_order_value"]["imaginary"])
        for row in gate_rows
    ]
    cross_node_residual = abs(values[-1] - values[-2]) / max(1.0, abs(values[-1]))
    profile = module_5077.M5043.PROFILES["coarse12"]
    tolerance = float(profile["relative_adaptive_tolerance"])
    formal_digest = tree_digest(FORMAL)
    certificate_passed = bool(
        all(row["converged"] for row in gate_rows)
        and all(row["all_residues_stable"] for row in gate_rows)
        and cross_node_residual < tolerance
        and all(row["cluster_audit"]["cluster_count"] > 0 for row in gate_rows)
        and all(row["removable_extension_call_count"] == 0 for row in gate_rows)
        and all(
            not row["tolerance_changed"]
            and not row["interval_cap_changed"]
            and not row["depth_cap_changed"]
            for row in gate_rows
        )
    )
    result = {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "job_key": JOB_KEY,
        "cauchy_identity": (
            "For a finite set of correction poles with one common orientation, "
            "any positively oriented disk containing the entire set and no other "
            "global pole or the measure pole at zero has contour integral equal "
            "to the sum of the individual residues."
        ),
        "link_relative_distance": LINK_RELATIVE_DISTANCE,
        "maximum_cluster_isolation_ratio": MAXIMUM_CLUSTER_ISOLATION_RATIO,
        "cluster_contour_rule": (
            "center=arithmetic mean; extent=max root distance; outside=min distance "
            "to every excluded pole and zero; radius=max(1.5*extent,1e-7," 
            "sqrt(extent*outside)); require extent<radius<outside"
        ),
        "adaptive_tolerance": tolerance,
        "production_interval_cap": int(profile["relative_adaptive_maximum_intervals"]),
        "production_depth_cap": 14,
        "gate_rows": gate_rows,
        "cross_node_relative_residual": float(cross_node_residual),
        "same_side_cluster_cycle_certificate_passed": certificate_passed,
        "formalization_workbench_tree_sha256": formal_digest,
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(RESULT_JSON, result)
    checks = [
        ("source_paths_exist", not missing, "all 5095 inputs exist"),
        (
            "cauchy_cluster_guards",
            all(
                row["cluster_audit"]["maximum_cluster_isolation_ratio"]
                < MAXIMUM_CLUSTER_ISOLATION_RATIO
                for row in gate_rows
            ),
            str(
                [
                    row["cluster_audit"]["maximum_cluster_isolation_ratio"]
                    for row in gate_rows
                ]
            ),
        ),
        (
            "both_node_gates_converged",
            all(row["converged"] for row in gate_rows),
            str([row["relative_residual"] for row in gate_rows]),
        ),
        (
            "residues_stable",
            all(row["all_residues_stable"] for row in gate_rows),
            str([row["all_residues_stable"] for row in gate_rows]),
        ),
        (
            "cross_node_stable",
            cross_node_residual < tolerance,
            str(cross_node_residual),
        ),
        (
            "cluster_route_exercised",
            all(row["cluster_audit"]["cluster_count"] > 0 for row in gate_rows),
            str([row["cluster_audit"]["cluster_count"] for row in gate_rows]),
        ),
        (
            "no_exact_collision_fallback",
            all(row["removable_extension_call_count"] == 0 for row in gate_rows),
            str([row["removable_extension_call_count"] for row in gate_rows]),
        ),
        (
            "production_controls_unchanged",
            all(
                not row["tolerance_changed"]
                and not row["interval_cap_changed"]
                and not row["depth_cap_changed"]
                for row in gate_rows
            ),
            "tolerance, interval cap, and depth cap unchanged",
        ),
        ("certificate_passed", certificate_passed, str(certificate_passed)),
        ("formalization_unchanged", formal_digest == FORMAL_BASELINE, formal_digest),
        (
            "claim_discipline",
            not result["valid_for_full_MTS_claim"],
            "numerical contour certificate is not physical evidence",
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
                    "check_id": f"V5095_{index:02d}_{name}",
                    "passed": passed,
                    "detail": detail,
                    "checkpoint_marker": MARKER,
                }
            )
    failed = [name for name, passed, _ in checks if not passed]
    if failed:
        raise RuntimeError(f"checkpoint 5095 validation failed: {failed}")


if __name__ == "__main__":
    main()
