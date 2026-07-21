from __future__ import annotations

import argparse
import cmath
import csv
import hashlib
import importlib.util
import json
import math
import os
import time
from pathlib import Path
from typing import Any

import numpy as np


POST = Path(__file__).resolve().parents[1]
SCRIPT_5041 = POST / "scripts" / "Y5_R2FR_5041_cross_source_additive_zero_repair.py"
RUN_5040 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5040"
    / "runs"
    / "nested_sobol_power1_s4_v1"
)
SOURCE = POST / "source-intake" / "functional_rg" / "5043"
RUNS = SOURCE / "runs"
BENCHMARK_JSON = SOURCE / "coarse_profile_benchmark.json"
RESULT_JSON = SOURCE / "multilevel_coarse_E040_gate.json"
COMPONENT_CSV = SOURCE / "multilevel_component_gate.csv"
LOCK_JSON = SOURCE / "locked_multilevel_pilot_contract.json"
VALIDATION_CSV = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5043_VALIDATION.csv"
)
ENDPOINT_REPAIR_SUMMARY = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5037"
    / "repairs"
    / "finite_endpoint_sector_v1"
    / "repair_summary.json"
)
MARKER = "MTS_5043_THEOREM_FIRST_COARSE_E040_MULTILEVEL_GATE"
REVISION = "theorem-first-cross-source-zero-chart-filtered-shrinking-radius-v1"
FORMAL_BASELINE = "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
CANDIDATE_FRACTIONS = (0.1, 0.05, 0.025, 0.0125, 0.2)
CHART_PAIR_SUFFIXES = {
    frozenset(("plus_u", "minus_u")),
    frozenset(("plus_v", "minus_v")),
}
PROFILES: dict[str, dict[str, Any]] = {
    "coarse8": {
        "relative_orders": (8,),
        "global_nodes": 8,
        "global_residue_nodes": 8,
        "relative_residue_nodes": 8,
        "model_distance": 0.65,
        "relative_quadrature_mode": "collision_scaled_adaptive",
        "relative_adaptive_tolerance": 1.0e-3,
        "relative_adaptive_maximum_intervals": 512,
    },
    "coarse12": {
        "relative_orders": (12,),
        "global_nodes": 12,
        "global_residue_nodes": 12,
        "relative_residue_nodes": 12,
        "model_distance": 0.65,
        "relative_quadrature_mode": "collision_scaled_adaptive",
        "relative_adaptive_tolerance": 5.0e-4,
        "relative_adaptive_maximum_intervals": 1024,
    },
}
TOPOLOGY_RUNS = (
    RUN_5040,
    POST / "source-intake" / "functional_rg" / "5037" / "runs" / "paired_outer_precision_s4_v1",
    POST / "source-intake" / "functional_rg" / "5036" / "runs" / "paired_full_vector_s2_v1",
    POST / "source-intake" / "functional_rg" / "5035" / "runs" / "central_eps008_004_002_s4_v1",
    POST / "source-intake" / "functional_rg" / "5034" / "runs" / "bounded_smoke_eps008_v2",
)
CENTRAL_TOPOLOGY_IDS = {"A02": "ZN3", "A07": "Z0", "A12": "ZP3"}
LOCKED_PROFILE_DIGESTS = {
    "coarse8": "fc7e020d4ecb173fcf444f085cb1fb2293888dcbb18c7ea4c9753150b545d258",
    "coarse12": "1e07bbafb4cdec4afc28533b3eecbec2254fdb87d428022196c425238ad56ac3",
}
CURRENT_JOB = ""
THEOREM_AUDIT: list[dict[str, Any]] = []
CHART_AUDIT: list[dict[str, Any]] = []
NUMERIC_AUDIT: list[dict[str, Any]] = []


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5041 = load_module("mts_5041_for_coarse_multilevel", SCRIPT_5041)
M5040 = M5041.M5040
M5036 = M5041.M5036
M5034 = M5041.M5034
N5030 = M5041.N5030
ORIGINAL_CATALOG = N5030.chamber_residue_catalog
ORIGINAL_GLOBAL_CHAMBER_VALUE = N5030.global_chamber_value


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def canonical_digest(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def tree_digest(path: Path) -> str:
    value = hashlib.sha256()
    if not path.exists():
        return "MISSING"
    for file_path in sorted(candidate for candidate in path.rglob("*") if candidate.is_file()):
        value.update(file_path.relative_to(path).as_posix().encode("utf-8"))
        value.update(digest(file_path).encode("ascii"))
    return value.hexdigest()


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True), encoding="utf-8")
    os.replace(temporary, path)


def serialized(value: complex) -> dict[str, float]:
    return {"real": float(value.real), "imaginary": float(value.imag)}


def complex_value(row: dict[str, float]) -> complex:
    return complex(float(row["real"]), float(row["imaginary"]))


def ownership_digest(ownership: dict[str, bool]) -> str:
    payload = json.dumps(ownership, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def lifted_log_near(value: complex, reference: complex) -> complex:
    principal = cmath.log(value)
    turn = round((reference.imag - principal.imag) / (2.0 * math.pi))
    return principal + 2.0j * math.pi * turn


def quadratic_value(
    points: tuple[tuple[float, complex], ...], parameter: float
) -> complex:
    result = 0.0j
    for index, (abscissa, value) in enumerate(points):
        basis = 1.0
        for other_index, (other_abscissa, _) in enumerate(points):
            if other_index == index:
                continue
            basis *= (parameter - other_abscissa) / (abscissa - other_abscissa)
        result += basis * value
    return result


class CertifiedSectorExtension:
    def __init__(self, certificates: list[dict[str, Any]]) -> None:
        self.certificates = certificates
        self.calls: list[dict[str, Any]] = []

    def __call__(
        self,
        relative_circle: complex,
        ownership: dict[str, bool],
        global_nodes: int,
        global_residue_nodes: int,
    ) -> complex:
        try:
            return ORIGINAL_GLOBAL_CHAMBER_VALUE(
                relative_circle,
                ownership,
                global_nodes,
                global_residue_nodes,
            )
        except RuntimeError as error:
            if "unsectorized global collision" not in str(error):
                raise
            wanted_digest = ownership_digest(ownership)
            candidates: list[tuple[float, float, float, dict[str, Any]]] = []
            for certificate in self.certificates:
                if certificate["ownership_digest"] != wanted_digest:
                    continue
                base_log = certificate["base_log"]
                direction = certificate["direction"]
                lifted = lifted_log_near(relative_circle, base_log)
                displacement = lifted - base_log
                parameter = float(
                    (displacement * direction.conjugate()).real
                    / max(abs(direction) ** 2, 1.0e-300)
                )
                transverse = float(abs(displacement - parameter * direction))
                candidates.append(
                    (abs(displacement), parameter, transverse, certificate)
                )
            if not candidates:
                raise
            distance, parameter, transverse, certificate = min(
                candidates, key=lambda row: row[0]
            )
            if not (
                -1.0e-12 <= parameter <= 1.0e-7
                and transverse <= 1.0e-8
            ):
                raise
            value = quadratic_value(certificate["polynomial_points"], parameter)
            error_bound = (
                certificate["derivative_bound"] * abs(parameter)
                + abs(certificate["fine_limit"] - certificate["coarse_limit"])
                + certificate["adjacent_limit_relative_residual"]
                * max(1.0, abs(certificate["fine_limit"]))
            )
            self.calls.append(
                {
                    "boundary_index": certificate["boundary_index"],
                    "side": certificate["side"],
                    "chamber_index": certificate["chamber_index"],
                    "relative_circle": serialized(relative_circle),
                    "log_distance": float(distance),
                    "sector_parameter": parameter,
                    "transverse_distance": transverse,
                    "returned_value": serialized(value),
                    "absolute_error_bound": float(error_bound),
                    "original_error": str(error),
                }
            )
            return value


def certified_endpoint_extension(topology_source: Path) -> CertifiedSectorExtension:
    summary = json.loads(ENDPOINT_REPAIR_SUMMARY.read_text(encoding="utf-8"))
    contract = summary["repair_contract"]
    if not (
        summary.get("accepted")
        and summary.get("promoted")
        and contract.get("certificate_gate")
        and contract.get("accepted")
        and float(contract.get("kernel_relative_residual", math.inf)) == 0.0
    ):
        raise RuntimeError("5037 endpoint-sector source contract is not accepted")
    if digest(topology_source) != contract["topology_file_sha256"]:
        raise RuntimeError("5037 endpoint-sector topology digest mismatch")
    primary = contract["primary_certificates"]
    audit = contract["audit_certificates"]
    if not primary or len(primary) != len(audit):
        raise RuntimeError("5037 endpoint-sector certificate matrix is incomplete")
    if not all(
        bool(row["side_valid"] and row["boundary_valid"])
        for row in primary + audit
    ):
        raise RuntimeError("5037 endpoint-sector certificate has an invalid side")
    certificates = []
    for row in primary:
        samples = sorted(
            (
                float(sample["fraction"]),
                complex_value(sample["value"]),
            )
            for sample in row["samples"]
        )
        certificates.append(
            {
                "boundary_index": int(row["boundary_index"]),
                "side": str(row["side"]),
                "chamber_index": int(row["chamber_index"]),
                "ownership_digest": str(row["ownership_digest"]),
                "base_log": complex_value(row["base_log"]),
                "direction": complex_value(row["direction"]),
                "polynomial_points": tuple(samples[:3]),
                "fine_limit": complex_value(row["fine_limit"]),
                "coarse_limit": complex_value(row["coarse_limit"]),
                "adjacent_limit_relative_residual": float(
                    row["adjacent_limit_relative_residual"]
                ),
                "derivative_bound": float(row["derivative_bound"]),
            }
        )
    return CertifiedSectorExtension(certificates)


def chart_pair(pair: tuple[str, str] | list[str]) -> bool:
    first_source, first_suffix = str(pair[0]).rsplit(":", 1)
    second_source, second_suffix = str(pair[1]).rsplit(":", 1)
    return (
        first_source == second_source
        and frozenset((first_suffix, second_suffix)) in CHART_PAIR_SUFFIXES
    )


def chart_origin_evidence(
    group: dict[str, Any], root: complex
) -> dict[str, Any] | None:
    pairs = [tuple(pair) for pair in group["pairs"]]
    if not pairs or not all(chart_pair(pair) for pair in pairs):
        return None
    rationals = N5030.M5029.root_rationals(
        N5030.SOFT_ENERGY,
        N5030.SOFT_COSINE,
        N5030.DECAY_COSINE,
        N5030.TARGET_COSINE,
    )
    values: dict[str, complex] = {}
    for pair in pairs:
        for label in pair:
            try:
                values[label] = N5030.M5029.rational_value(rationals[label], root)
            except (KeyError, ZeroDivisionError, FloatingPointError):
                return None
    maximum_modulus = max(abs(value) for value in values.values())
    if maximum_modulus >= 1.0e-7:
        return None
    return {
        "root": serialized(root),
        "pairs": [list(pair) for pair in pairs],
        "global_factor_roots": {
            label: serialized(value) for label, value in values.items()
        },
        "maximum_global_factor_root_modulus": maximum_modulus,
        "classification": "same-source stereographic chart-origin coalescence",
    }


def theorem_first_chamber_residue_catalog(
    ownership: dict[str, bool],
    start: complex,
    end: complex,
    required_roots: list[complex],
    global_nodes: int,
    global_residue_nodes: int,
    relative_residue_nodes: int,
    model_distance: float,
) -> tuple[list[dict[str, Any]], bool]:
    target_groups = N5030.collision_groups(N5030.TARGET_COSINE, ownership)
    retained_groups: list[dict[str, Any]] = []
    for group in target_groups:
        root = complex(group["root"])
        required = any(
            abs(root - candidate) < 2.0e-5 * max(1.0, abs(root), abs(candidate))
            for candidate in required_roots
        )
        evidence = chart_origin_evidence(group, root)
        if evidence is not None and not required:
            CHART_AUDIT.append(
                {
                    "job_key": CURRENT_JOB,
                    **evidence,
                    "required_for_homotopy": False,
                    "reason": "same-source chart-origin coalescence without a tracked crossing",
                }
            )
            continue
        retained_groups.append(group)
    all_roots = [complex(group["root"]) for group in retained_groups]
    selected: list[dict[str, Any]] = []
    for group in retained_groups:
        root = complex(group["root"])
        log_point, distance, projection, copy_index = N5030.nearest_log_copy_to_segment(
            root, start, end
        )
        near_path = distance < model_distance and -0.25 < projection < 1.25
        required = any(
            abs(root - candidate) < 2.0e-5 * max(1.0, abs(root), abs(candidate))
            for candidate in required_roots
        )
        if not near_path and not required:
            continue
        selected.append(
            {
                "root": root,
                "pairs": group["pairs"],
                "log_point": log_point,
                "log_distance": distance,
                "segment_projection": projection,
                "copy_index": copy_index,
                "near_path": near_path,
                "required_for_homotopy": required,
            }
        )
    catalog: list[dict[str, Any]] = []
    all_stable = True
    for row in selected:
        root = row["root"]
        separations = [
            abs(root - other)
            for other in all_roots
            if abs(root - other) > 1.0e-7 * max(1.0, abs(root), abs(other))
        ]
        safe_scale = min([abs(root)] + separations)
        if not math.isfinite(safe_scale) or safe_scale <= 0.0:
            raise RuntimeError(f"invalid local residue safe scale at {root}")
        tentative = {
            **row,
            "outer_radius": 0.1 * safe_scale,
            "residue_contour_fraction": 0.1,
        }
        certificate = M5041.theorem_certificate(tentative, ownership)
        if certificate["passed"]:
            certificate["job_key"] = CURRENT_JOB
            certificate["numerical_residue_evaluation_skipped"] = True
            THEOREM_AUDIT.append(certificate)
            catalog.append(
                {
                    **row,
                    "outer_radius": 0.1 * safe_scale,
                    "residue_method": REVISION,
                    "residue_contour_fraction": 0.1,
                    "outer_residue": 0.0j,
                    "inner_residue": 0.0j,
                    "residue": 0.0j,
                    "residue_stability": 0.0,
                    "numerically_zero": True,
                    "stable": True,
                    "included_as_pole_model": False,
                    "cross_source_zero_certificate": certificate,
                }
            )
            continue

        def residue_pair(fraction: float) -> dict[str, Any]:
            radius = fraction * safe_scale
            outer = N5030.pair_local_relative_residue(
                root,
                radius,
                max(32, relative_residue_nodes + 8),
                row["pairs"],
                ownership,
                max(32, global_residue_nodes + 8),
            )
            inner = N5030.pair_local_relative_residue(
                root,
                radius / 2.0,
                max(48, relative_residue_nodes + 24),
                row["pairs"],
                ownership,
                max(48, global_residue_nodes + 16),
            )
            magnitude = max(abs(inner), abs(outer))
            stability = abs(inner - outer) / max(magnitude, 1.0e-30)
            numerically_zero = magnitude < 1.0e-7
            stable = numerically_zero or stability < 5.0e-3
            return {
                "fraction": fraction,
                "radius": radius,
                "outer": outer,
                "inner": inner,
                "stability": stability,
                "numerically_zero": numerically_zero,
                "stable": stable,
            }

        candidates = [residue_pair(0.1)]
        if not candidates[0]["stable"]:
            for fraction in CANDIDATE_FRACTIONS[1:4]:
                candidates.append(residue_pair(fraction))
                if candidates[-1]["stable"]:
                    break
            if not any(candidate["stable"] for candidate in candidates):
                candidates.append(residue_pair(0.2))
        stable_candidates = [candidate for candidate in candidates if candidate["stable"]]
        chosen = (
            stable_candidates[0]
            if stable_candidates
            else min(candidates, key=lambda candidate: candidate["stability"])
        )
        NUMERIC_AUDIT.append(
            {
                "job_key": CURRENT_JOB,
                "root": serialized(root),
                "pairs": row["pairs"],
                "safe_scale": safe_scale,
                "selected_fraction": chosen["fraction"],
                "selected_stable": chosen["stable"],
                "candidate_count": len(candidates),
                "cross_source_theorem_guard_passed": False,
            }
        )
        all_stable = all_stable and bool(chosen["stable"])
        catalog.append(
            {
                **row,
                "outer_radius": chosen["radius"],
                "residue_method": REVISION,
                "residue_contour_fraction": chosen["fraction"],
                "outer_residue": chosen["outer"],
                "inner_residue": chosen["inner"],
                "residue": 0.0j if chosen["numerically_zero"] else chosen["inner"],
                "residue_stability": chosen["stability"],
                "numerically_zero": chosen["numerically_zero"],
                "stable": chosen["stable"],
                "included_as_pole_model": row["near_path"]
                and not chosen["numerically_zero"]
                and chosen["stable"],
            }
        )
    return catalog, all_stable


def load_config() -> dict[str, Any]:
    return json.loads((RUN_5040 / "config.json").read_text(encoding="utf-8"))


def event_lookup(config: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {row["event_id"]: row for row in config["events"]}


def argument_lookup(config: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        row["base_argument_id"]: row
        for row in config["arguments"]
        if row["epsilon_id"] == "E040"
    }


def topology_path(event_id: str, argument: dict[str, Any]) -> Path:
    names = [f"{event_id}__{argument['argument_id']}.json"]
    alternate = CENTRAL_TOPOLOGY_IDS.get(argument["base_argument_id"])
    if alternate is not None:
        names.append(f"{event_id}__E040_{alternate}.json")
    candidates = [run / "topologies" / name for name in names for run in TOPOLOGY_RUNS]
    existing = [path for path in candidates if path.exists()]
    if not existing:
        raise FileNotFoundError(
            f"no exact E040 topology for {event_id} {argument['base_argument_id']}"
        )
    topology = json.loads(existing[0].read_text(encoding="utf-8"))
    if topology.get("event_id") != event_id:
        raise RuntimeError(f"topology event mismatch: {existing[0]}")
    if not (
        topology.get("assignment_tracking_passed")
        and topology.get("crossing_groups_consistent")
    ):
        raise RuntimeError(f"topology is not validated: {existing[0]}")
    return existing[0]


def primary_job(epsilon_id: str, event_id: str, base_id: str) -> dict[str, Any]:
    path = RUN_5040 / "jobs" / f"{epsilon_id}__{event_id}__{base_id}__primary24.json"
    if not path.exists():
        raise FileNotFoundError(path)
    row = json.loads(path.read_text(encoding="utf-8"))
    if row.get("status") not in {"IMPORTED_CONVERGED", "COMPLETED_CONVERGED"}:
        raise RuntimeError(f"primary source is not converged: {path}")
    return row


def localize_stale_path(value: str) -> Path:
    path = Path(value)
    if path.exists():
        return path
    normalized = value.replace("\\", "/")
    marker = "/post-checkpoint-work/"
    if marker not in normalized:
        raise FileNotFoundError(value)
    candidate = POST / normalized.split(marker, 1)[1]
    if not candidate.exists():
        raise FileNotFoundError(candidate)
    return candidate


def source_runtime(row: dict[str, Any]) -> tuple[float, float, str]:
    runtime = float(row.get("job_runtime_seconds", 0.0) or 0.0)
    topology_runtime = float(row.get("topology_runtime_seconds", 0.0) or 0.0)
    if runtime > 0.0:
        return runtime, topology_runtime, "direct"
    imported = row.get("imported_from")
    while imported:
        source_path = localize_stale_path(str(imported["source_job"]))
        source = json.loads(source_path.read_text(encoding="utf-8"))
        runtime = float(source.get("job_runtime_seconds", 0.0) or 0.0)
        topology_runtime = float(source.get("topology_runtime_seconds", 0.0) or 0.0)
        if runtime > 0.0:
            return runtime, topology_runtime, str(source_path)
        imported = source.get("imported_from") or imported.get("upstream_import")
    raise RuntimeError(f"no positive source runtime for {row['job_key']}")


def profile_digest(profile_name: str) -> str:
    return LOCKED_PROFILE_DIGESTS[profile_name]


def result_path(profile_name: str, event_id: str, base_id: str) -> Path:
    return RUNS / profile_name / "jobs" / f"{event_id}__{base_id}.json"


def evaluate_job(
    config: dict[str, Any],
    profile_name: str,
    event_id: str,
    base_id: str,
) -> dict[str, Any]:
    global CURRENT_JOB
    output = result_path(profile_name, event_id, base_id)
    expected_digest = profile_digest(profile_name)
    if output.exists():
        existing = json.loads(output.read_text(encoding="utf-8"))
        if (
            existing.get("profile_digest") == expected_digest
            and existing.get("status") == "COMPLETED_CONVERGED"
        ):
            return existing
    events = event_lookup(config)
    arguments = argument_lookup(config)
    event = events[event_id]
    argument = arguments[base_id]
    topology_source = topology_path(event_id, argument)
    topology = json.loads(topology_source.read_text(encoding="utf-8"))
    target = complex_value(argument["target_cosine"])
    M5034.configure(event, target)
    CURRENT_JOB = f"{profile_name}__{event_id}__{base_id}"
    THEOREM_AUDIT.clear()
    CHART_AUDIT.clear()
    NUMERIC_AUDIT.clear()
    profile = PROFILES[profile_name]
    started = time.monotonic()
    extension: CertifiedSectorExtension | None = None
    previous_global_chamber_value = N5030.global_chamber_value
    try:
        if event_id == "S503403_N0000" and base_id == "A14":
            extension = certified_endpoint_extension(topology_source)
            N5030.global_chamber_value = extension
        try:
            gate = N5030.fixed_event_integral_gate(
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
            N5030.global_chamber_value = previous_global_chamber_value
        kernel = M5034.highest_value(gate)
        direct = M5034.KERNEL_MULTIPLIER * kernel
        primary = complex_value(
            primary_job("E040", event_id, base_id)["normalized_direct_D_hhh_over_G3"]
        )
        converged = bool(gate["fixed_event_crossed_integral_converged"])
        result = {
            "checkpoint_marker": MARKER,
            "revision": REVISION,
            "profile": profile_name,
            "profile_settings": profile,
            "profile_digest": expected_digest,
            "event_id": event_id,
            "seed": int(event["seed"]),
            "sample_index": int(event["sample_index"]),
            "base_argument_id": base_id,
            "argument_id": argument["argument_id"],
            "target_cosine": argument["target_cosine"],
            "topology_source": str(topology_source),
            "topology_source_sha256": digest(topology_source),
            "status": "COMPLETED_CONVERGED" if converged else "COMPLETED_UNCONVERGED",
            "raw_fixed_event_kernel": serialized(kernel),
            "normalized_direct_D_hhh_over_G3": serialized(direct),
            "primary24_direct_D_hhh_over_G3": serialized(primary),
            "coarse_minus_primary24": serialized(direct - primary),
            "coarse_primary_relative_difference": float(
                abs(direct - primary) / max(1.0, abs(primary))
            ),
            "kernel_runtime_seconds": time.monotonic() - started,
            "all_residues_stable": bool(gate["all_residues_stable"]),
            "adaptive_quadrature_converged": all(
                bool(row["adaptive_quadrature_converged"])
                for row in gate["order_rows"]
            ),
            "highest_two_order_relative_residual": float(
                gate["highest_two_order_relative_residual"]
            ),
            "topological_correction": gate["topological_correction"],
            "highest_order_value": gate["highest_order_value"],
            "theorem_zero_residue_count": len(THEOREM_AUDIT),
            "numeric_residue_count": len(NUMERIC_AUDIT),
            "chart_origin_exclusion_count": len(CHART_AUDIT),
            "endpoint_sector_extension_count": (
                len(extension.calls) if extension is not None else 0
            ),
            "endpoint_sector_extension_calls": (
                extension.calls if extension is not None else []
            ),
            "endpoint_sector_certificate_source": (
                str(ENDPOINT_REPAIR_SUMMARY) if extension is not None else None
            ),
            "endpoint_sector_certificate_source_sha256": (
                digest(ENDPOINT_REPAIR_SUMMARY) if extension is not None else None
            ),
            "unstable_numeric_residue_count": sum(
                not bool(row["selected_stable"]) for row in NUMERIC_AUDIT
            ),
            "theorem_zero_rows": THEOREM_AUDIT,
            "numeric_residue_rows": NUMERIC_AUDIT,
            "chart_origin_exclusions": CHART_AUDIT,
            "full_gate_sha256": canonical_digest(gate),
            "valid_for_full_MTS_claim": False,
        }
    except Exception as error:
        N5030.global_chamber_value = previous_global_chamber_value
        result = {
            "checkpoint_marker": MARKER,
            "revision": REVISION,
            "profile": profile_name,
            "profile_settings": profile,
            "profile_digest": expected_digest,
            "event_id": event_id,
            "base_argument_id": base_id,
            "topology_source": str(topology_source),
            "status": "FAILED",
            "error": f"{type(error).__name__}: {error}",
            "kernel_runtime_seconds": time.monotonic() - started,
            "valid_for_full_MTS_claim": False,
        }
    atomic_json(output, result)
    return result


def expected_matrix(config: dict[str, Any]) -> list[tuple[str, str]]:
    events = sorted(config["events"], key=lambda row: (row["seed"], row["sample_index"]))
    base_ids = sorted(argument_lookup(config))
    return [(event["event_id"], base_id) for event in events for base_id in base_ids]


def dry_run(config: dict[str, Any]) -> dict[str, Any]:
    rows = []
    for event_id, base_id in expected_matrix(config):
        argument = argument_lookup(config)[base_id]
        topology = topology_path(event_id, argument)
        primary = primary_job("E040", event_id, base_id)
        rows.append(
            {
                "event_id": event_id,
                "base_argument_id": base_id,
                "topology": str(topology),
                "primary_status": primary["status"],
            }
        )
    result = {
        "expected_jobs": len(rows),
        "unique_topologies": len({row["topology"] for row in rows}),
        "all_primary_sources_converged": all(
            row["primary_status"] in {"IMPORTED_CONVERGED", "COMPLETED_CONVERGED"}
            for row in rows
        ),
        "all_topologies_exist": all(Path(row["topology"]).exists() for row in rows),
    }
    atomic_json(SOURCE / "dry_run.json", {**result, "rows": rows})
    return result


def benchmark(config: dict[str, Any], profiles: list[str]) -> dict[str, Any]:
    rows = []
    for profile_name in profiles:
        row = evaluate_job(config, profile_name, "S503401_N0001", "A00")
        rows.append(
            {
                "profile": profile_name,
                "status": row["status"],
                "kernel_runtime_seconds": row["kernel_runtime_seconds"],
                "coarse_primary_relative_difference": row.get(
                    "coarse_primary_relative_difference"
                ),
                "highest_two_order_relative_residual": row.get(
                    "highest_two_order_relative_residual"
                ),
                "theorem_zero_residue_count": row.get("theorem_zero_residue_count"),
                "numeric_residue_count": row.get("numeric_residue_count"),
                "chart_origin_exclusion_count": row.get(
                    "chart_origin_exclusion_count"
                ),
            }
        )
    converged = [row for row in rows if row["status"] == "COMPLETED_CONVERGED"]
    selected = min(converged, key=lambda row: row["kernel_runtime_seconds"])["profile"] if converged else None
    result = {
        "checkpoint_marker": MARKER,
        "benchmark_job": "E040__S503401_N0001__A00",
        "rows": rows,
        "selected_profile": selected,
        "selection_rule": "fastest fixed profile whose residue and adaptive gates converge",
        "correlation_selection_deferred_to_full retrospective matrix": True,
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(BENCHMARK_JSON, result)
    return result


def run_matrix(
    config: dict[str, Any],
    profile_name: str,
    max_jobs: int,
    max_wall_seconds: float,
) -> dict[str, Any]:
    started = time.monotonic()
    executed = 0
    rows = []
    for event_id, base_id in expected_matrix(config):
        output = result_path(profile_name, event_id, base_id)
        cached = False
        if output.exists():
            existing = json.loads(output.read_text(encoding="utf-8"))
            cached = (
                existing.get("profile_digest") == profile_digest(profile_name)
                and existing.get("status") == "COMPLETED_CONVERGED"
            )
        if not cached:
            if max_jobs > 0 and executed >= max_jobs:
                break
            if time.monotonic() - started >= max_wall_seconds:
                break
            print(f"starting {profile_name} {event_id} {base_id}", flush=True)
            executed += 1
        row = evaluate_job(config, profile_name, event_id, base_id)
        rows.append(row)
        print(
            f"finished {profile_name} {event_id} {base_id} status={row['status']} "
            f"seconds={row['kernel_runtime_seconds']:.3f}",
            flush=True,
        )
    all_rows = []
    for event_id, base_id in expected_matrix(config):
        output = result_path(profile_name, event_id, base_id)
        if output.exists():
            all_rows.append(json.loads(output.read_text(encoding="utf-8")))
    status = {
        "checkpoint_marker": MARKER,
        "profile": profile_name,
        "expected_jobs": len(expected_matrix(config)),
        "terminal_jobs": len(all_rows),
        "converged_jobs": sum(
            row.get("status") == "COMPLETED_CONVERGED" for row in all_rows
        ),
        "unconverged_jobs": sum(
            row.get("status") == "COMPLETED_UNCONVERGED" for row in all_rows
        ),
        "failed_jobs": sum(row.get("status") == "FAILED" for row in all_rows),
        "executed_this_call": executed,
        "wall_seconds": time.monotonic() - started,
        "complete": len(all_rows) == len(expected_matrix(config))
        and all(row.get("status") == "COMPLETED_CONVERGED" for row in all_rows),
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(RUNS / profile_name / "status.json", status)
    return status


def cyclic_nonlocal(
    config: dict[str, Any], values: dict[tuple[str, str], complex]
) -> np.ndarray:
    components = []
    for crossing in config["crossings"]:
        components.append(
            values[(crossing["s_argument_id"], "value")]
            + float(crossing["t_ratio"]) ** 3
            * values[(crossing["t_argument_id"], "value")]
            + float(crossing["u_ratio"]) ** 3
            * values[(crossing["u_argument_id"], "value")]
        )
    vector = np.asarray(components, dtype=np.complex128)
    shape = 1.0 - np.asarray(config["physical_cosines"], dtype=float) ** 2
    _, residual, orthogonality = M5036.project_vector(vector, shape)
    if orthogonality > 1.0e-10:
        raise RuntimeError("coarse event projection lost orthogonality")
    return residual


def scalar_beta(x_values: np.ndarray, y_values: np.ndarray) -> float:
    centered_x = x_values - np.mean(x_values)
    centered_y = y_values - np.mean(y_values)
    denominator = float(np.dot(centered_x, centered_x))
    if denominator <= 1.0e-24:
        return 0.0
    return float(np.dot(centered_x, centered_y) / denominator)


def channel_matrix(values: np.ndarray) -> np.ndarray:
    return np.concatenate((values.real, values.imag), axis=1)


def pair_means(
    event_rows: list[dict[str, Any]], values: np.ndarray
) -> tuple[list[int], np.ndarray]:
    seeds = sorted({int(row["seed"]) for row in event_rows})
    paired = []
    for seed in seeds:
        indices = [index for index, row in enumerate(event_rows) if row["seed"] == seed]
        if len(indices) != 2:
            raise RuntimeError(f"seed {seed} does not have exactly two nested events")
        paired.append(np.mean(values[indices], axis=0))
    return seeds, np.stack(paired)


def analyze(config: dict[str, Any], profile_name: str) -> dict[str, Any]:
    event_rows = sorted(
        config["events"], key=lambda row: (row["seed"], row["sample_index"])
    )
    low_values = []
    high_values = []
    high_costs = []
    low_kernel_costs = []
    low_topology_costs = []
    for event in event_rows:
        event_id = event["event_id"]
        low_arguments: dict[tuple[str, str], complex] = {}
        e040_arguments: dict[tuple[str, str], complex] = {}
        e020_arguments: dict[tuple[str, str], complex] = {}
        high_cost = 0.0
        low_kernel_cost = 0.0
        low_topology_cost = 0.0
        for base_id in sorted(argument_lookup(config)):
            low_path = result_path(profile_name, event_id, base_id)
            if not low_path.exists():
                raise RuntimeError(f"coarse matrix is incomplete: {low_path}")
            low = json.loads(low_path.read_text(encoding="utf-8"))
            if low.get("status") != "COMPLETED_CONVERGED":
                raise RuntimeError(f"coarse row is not converged: {low_path}")
            e040 = primary_job("E040", event_id, base_id)
            e020 = primary_job("E020", event_id, base_id)
            low_arguments[(base_id, "value")] = complex_value(
                low["normalized_direct_D_hhh_over_G3"]
            )
            e040_arguments[(base_id, "value")] = complex_value(
                e040["normalized_direct_D_hhh_over_G3"]
            )
            e020_arguments[(base_id, "value")] = complex_value(
                e020["normalized_direct_D_hhh_over_G3"]
            )
            e040_runtime, e040_topology, _ = source_runtime(e040)
            e020_runtime, _, _ = source_runtime(e020)
            high_cost += e040_runtime + e020_runtime
            low_kernel_cost += float(low["kernel_runtime_seconds"])
            low_topology_cost += e040_topology
        low_values.append(cyclic_nonlocal(config, low_arguments))
        e040_residual = cyclic_nonlocal(config, e040_arguments)
        e020_residual = cyclic_nonlocal(config, e020_arguments)
        high_values.append(2.0 * e020_residual - e040_residual)
        high_costs.append(high_cost)
        low_kernel_costs.append(low_kernel_cost)
        low_topology_costs.append(low_topology_cost)
    high_complex = np.stack(high_values)
    low_complex = np.stack(low_values)
    high = channel_matrix(high_complex)
    low = channel_matrix(low_complex)
    seeds = sorted({int(row["seed"]) for row in event_rows})
    crossfit_pair_corrections = []
    fold_rows = []
    for held_seed in seeds:
        train = np.asarray([row["seed"] != held_seed for row in event_rows], dtype=bool)
        held = ~train
        betas = np.asarray(
            [scalar_beta(low[train, index], high[train, index]) for index in range(high.shape[1])]
        )
        correction = high[held] - low[held] * betas
        crossfit_pair_corrections.append(np.mean(correction, axis=0))
        fold_rows.append(
            {
                "held_seed": held_seed,
                "training_seeds": [seed for seed in seeds if seed != held_seed],
                "betas": betas.tolist(),
            }
        )
    _, raw_pairs = pair_means(event_rows, high)
    crossfit_pairs = np.stack(crossfit_pair_corrections)
    raw_sd = np.std(raw_pairs, axis=0, ddof=1)
    crossfit_sd = np.std(crossfit_pairs, axis=0, ddof=1)
    crossfit_ratio = np.divide(
        crossfit_sd,
        raw_sd,
        out=np.full_like(raw_sd, math.inf),
        where=raw_sd > 0.0,
    )
    beta = np.asarray(
        [scalar_beta(low[:, index], high[:, index]) for index in range(high.shape[1])]
    )
    correction = high - low * beta
    _, correction_pairs = pair_means(event_rows, correction)
    _, low_pairs = pair_means(event_rows, low)
    variance_y = np.var(raw_pairs, axis=0, ddof=1)
    variance_d = np.var(correction_pairs, axis=0, ddof=1)
    variance_x = np.var(low_pairs, axis=0, ddof=1)
    high_cost = float(np.mean(high_costs))
    low_kernel_cost = float(np.mean(low_kernel_costs))
    low_topology_cost = float(np.mean(low_topology_costs))
    low_future_cost = low_kernel_cost + low_topology_cost
    margins_real = np.asarray(
        [float(row["target_equivalence_margin"]) for row in config["target_precision_budgets"]]
    )
    margins = np.concatenate((margins_real, margins_real))
    base_score = float(np.max(np.sqrt(variance_y * high_cost) / margins))
    allocation_rows = []
    for ratio in np.geomspace(0.25, 512.0, 4097):
        variance_cost = (
            variance_d + beta * beta * variance_x / ratio
        ) * (high_cost + ratio * low_future_cost)
        score = float(np.max(np.sqrt(np.maximum(variance_cost, 0.0)) / margins))
        allocation_rows.append((float(ratio), score, score / base_score))
    optimal_ratio, optimal_score, optimal_score_ratio = min(
        allocation_rows, key=lambda row: row[1]
    )
    labels = [
        *[f"real_z{value:+.1f}" for value in config["physical_cosines"]],
        *[f"imag_z{value:+.1f}" for value in config["physical_cosines"]],
    ]
    components = []
    for index, label in enumerate(labels):
        components.append(
            {
                "component": label,
                "beta": float(beta[index]),
                "crossfit_sd_ratio": float(crossfit_ratio[index]),
                "variance_Y": float(variance_y[index]),
                "variance_correction": float(variance_d[index]),
                "variance_low": float(variance_x[index]),
                "correction_variance_ratio": float(
                    variance_d[index] / variance_y[index]
                    if variance_y[index] > 0.0
                    else math.inf
                ),
                "target_margin": float(margins[index]),
            }
        )
    matrix_complete = len(event_rows) * 15 == 120
    no_component_instability = bool(
        np.all(np.isfinite(crossfit_ratio)) and np.max(crossfit_ratio) < 1.5
    )
    efficiency_gate = bool(optimal_score_ratio < 0.8)
    fresh_pilot_authorized = bool(
        matrix_complete and no_component_instability and efficiency_gate
    )
    result = {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "profile": profile_name,
        "events": len(event_rows),
        "jobs": len(event_rows) * 15,
        "crossfit_folds": fold_rows,
        "components": components,
        "worst_crossfit_sd_ratio": float(np.max(crossfit_ratio)),
        "components_improved_crossfit": int(np.sum(crossfit_ratio < 1.0)),
        "mean_high_event_cost_seconds": high_cost,
        "mean_low_kernel_event_cost_seconds": low_kernel_cost,
        "mean_low_topology_event_cost_seconds": low_topology_cost,
        "mean_low_future_event_cost_seconds": low_future_cost,
        "low_to_high_future_cost_ratio": low_future_cost / high_cost,
        "optimal_low_to_high_sample_ratio": optimal_ratio,
        "high_only_target_normalized_variance_cost_score": base_score,
        "multilevel_target_normalized_variance_cost_score": optimal_score,
        "equal_cost_score_ratio": optimal_score_ratio,
        "efficiency_gate_threshold": 0.8,
        "efficiency_gate_passed": efficiency_gate,
        "no_component_instability": no_component_instability,
        "fresh_independent_pilot_authorized": fresh_pilot_authorized,
        "unbiased_estimator": "mean_H(Y-beta*X)+beta*mean_L(X), with fixed beta and independent future H/L samples",
        "target_values_used_to_fit_beta": False,
        "retrospective_only": True,
        "valid_for_full_MTS_claim": False,
        "formalization_workbench_tree_sha256": tree_digest(POST.parent / "formalization-workbench"),
    }
    atomic_json(RESULT_JSON, result)
    COMPONENT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with COMPONENT_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(components[0]))
        writer.writeheader()
        writer.writerows(components)
    lock = {
        "checkpoint_marker": MARKER,
        "authorized": fresh_pilot_authorized,
        "profile": profile_name,
        "profile_digest": profile_digest(profile_name),
        "beta_channel_order": labels,
        "fixed_betas": beta.tolist(),
        "low_to_high_sample_ratio": optimal_ratio,
        "high_observable": "Y=2*R(E020_primary24)-R(E040_primary24)",
        "low_observable": f"X=R(E040_{profile_name})",
        "estimator": "mean_H(Y-beta*X)+beta*mean_L(X)",
        "future_high_and_low_samples_must_be_independent_of_this_training_matrix": True,
        "target_values_must_not_refit_beta": True,
        "pilot_is_not_production_evidence": True,
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(LOCK_JSON, lock)
    return result


def write_validation(
    config: dict[str, Any], profile_name: str, result: dict[str, Any] | None
) -> list[dict[str, str]]:
    status_path = RUNS / profile_name / "status.json"
    status = json.loads(status_path.read_text(encoding="utf-8")) if status_path.exists() else {}
    checks: list[tuple[str, bool, str]] = [
        ("source_5041_exists", SCRIPT_5041.exists(), str(SCRIPT_5041)),
        ("locked_5040_config_exists", (RUN_5040 / "config.json").exists(), str(RUN_5040 / "config.json")),
        ("dry_run_covers_120", dry_run(config)["expected_jobs"] == 120, "expected=120"),
        ("matrix_has_no_failed_rows", int(status.get("failed_jobs", -1)) == 0, str(status.get("failed_jobs"))),
        ("matrix_has_no_unconverged_rows", int(status.get("unconverged_jobs", -1)) == 0, str(status.get("unconverged_jobs"))),
        ("matrix_complete", bool(status.get("complete")), str(status.get("terminal_jobs"))),
        ("result_is_nonclaim", result is not None and not bool(result.get("valid_for_full_MTS_claim")), "required false"),
        ("target_not_fit", result is not None and not bool(result.get("target_values_used_to_fit_beta")), "required false"),
        ("formalization_workbench_unchanged", tree_digest(POST.parent / "formalization-workbench") == FORMAL_BASELINE, tree_digest(POST.parent / "formalization-workbench")),
    ]
    rows = [
        {"check": name, "passed": str(passed).lower(), "evidence": evidence}
        for name, passed, evidence in checks
    ]
    VALIDATION_CSV.parent.mkdir(parents=True, exist_ok=True)
    with VALIDATION_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=("check", "passed", "evidence"))
        writer.writeheader()
        writer.writerows(rows)
    return rows


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        choices=("dry-run", "benchmark", "matrix", "analyze", "all"),
        default="dry-run",
    )
    parser.add_argument("--profiles", default="coarse8,coarse12")
    parser.add_argument("--profile", choices=tuple(PROFILES), default="coarse8")
    parser.add_argument("--max-jobs", type=int, default=0)
    parser.add_argument("--max-wall-seconds", type=float, default=13_800.0)
    return parser.parse_args()


def main() -> None:
    arguments = parse_arguments()
    config = load_config()
    N5030.chamber_residue_catalog = theorem_first_chamber_residue_catalog
    try:
        if arguments.mode == "dry-run":
            print(json.dumps(dry_run(config), indent=2))
            return
        selected = arguments.profile
        if arguments.mode in {"benchmark", "all"}:
            profiles = [value.strip() for value in arguments.profiles.split(",") if value.strip()]
            if any(value not in PROFILES for value in profiles):
                raise ValueError("unknown benchmark profile")
            benchmark_result = benchmark(config, profiles)
            print(json.dumps(benchmark_result, indent=2))
            if benchmark_result["selected_profile"] is not None:
                selected = str(benchmark_result["selected_profile"])
            if arguments.mode == "benchmark":
                return
        if arguments.mode in {"matrix", "all"}:
            status = run_matrix(
                config,
                selected,
                arguments.max_jobs,
                arguments.max_wall_seconds,
            )
            print(json.dumps(status, indent=2))
            if arguments.mode == "matrix" and not status["complete"]:
                write_validation(config, selected, None)
                return
        if arguments.mode in {"analyze", "all"}:
            result = analyze(config, selected)
            validation = write_validation(config, selected, result)
            print(json.dumps(result, indent=2))
            print(
                json.dumps(
                    {
                        "validation_passed": sum(row["passed"] == "true" for row in validation),
                        "validation_total": len(validation),
                    },
                    indent=2,
                )
            )
    finally:
        N5030.chamber_residue_catalog = ORIGINAL_CATALOG
        N5030.global_chamber_value = ORIGINAL_GLOBAL_CHAMBER_VALUE


if __name__ == "__main__":
    main()
