from __future__ import annotations

import argparse
import cmath
import hashlib
import importlib.util
import json
import math
import shutil
import time
from pathlib import Path
from typing import Any, Callable


POST = Path(__file__).resolve().parents[1]
CHART_REPAIR_SCRIPT = (
    POST / "scripts" / "Y5_R2FR_5037_chart_origin_collision_repair.py"
)
PRODUCTION_SCRIPT = (
    POST / "scripts" / "Y5_R2FR_5037_paired_outer_precision_reflection_control.py"
)
SOURCE = POST / "source-intake" / "functional_rg" / "5037"
RUNS = SOURCE / "runs"
REPAIRS = SOURCE / "repairs"
MARKER = "MTS_5037_FINITE_ENDPOINT_SECTOR_REPAIR"
REVISION = "finite-endpoint-removable-sector-extension-v1"
ZERO_RESIDUE_ABSOLUTE_TOLERANCE = 1.0e-7
LIMIT_RELATIVE_TOLERANCE = 2.0e-8
ADJACENT_LIMIT_RELATIVE_TOLERANCE = 2.0e-8
AUDIT_KERNEL_RELATIVE_TOLERANCE = 5.0e-5
MAXIMUM_EXTENSION_PARAMETER = 1.0e-7
MAXIMUM_EXTENSION_TRANSVERSE_DISTANCE = 1.0e-8


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


CHART_REPAIR = load_module(
    "mts_5037_chart_repair_for_endpoint_sector", CHART_REPAIR_SCRIPT
)
M5037 = CHART_REPAIR.M5037
M5036 = CHART_REPAIR.M5036
M5035 = CHART_REPAIR.M5035
N5030 = CHART_REPAIR.N5030
ORIGINAL_GLOBAL_CHAMBER_VALUE = N5030.global_chamber_value
ORIGINAL_CHAMBER_RESIDUE_CATALOG = N5030.chamber_residue_catalog


def serialized_complex(value: complex) -> dict[str, float]:
    return {"real": float(value.real), "imaginary": float(value.imag)}


def ownership_digest(ownership: dict[str, bool]) -> str:
    payload = json.dumps(ownership, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def normalized_pair(pair: tuple[str, str] | list[str]) -> tuple[str, str]:
    return tuple(sorted((str(pair[0]), str(pair[1]))))


def relative_difference(first: complex, second: complex) -> float:
    return float(abs(first - second) / max(1.0, abs(first), abs(second)))


def quadratic_zero_limit(
    half_value: complex,
    one_value: complex,
    two_value: complex,
) -> complex:
    return (8.0 / 3.0) * half_value - 2.0 * one_value + (1.0 / 3.0) * two_value


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


def lifted_log_near(value: complex, reference: complex) -> complex:
    principal = cmath.log(value)
    turn = round((reference.imag - principal.imag) / (2.0 * math.pi))
    return principal + 2.0j * math.pi * turn


def endpoint_group(
    groups: list[dict[str, Any]], endpoint_root: complex
) -> dict[str, Any]:
    candidates = [
        group
        for group in groups
        if any(
            normalized_pair(pair) in N5030.ENDPOINT_COLLISION_PAIRS
            for pair in group["pairs"]
        )
    ]
    if not candidates:
        raise RuntimeError("endpoint has no declared endpoint-collision pair")
    selected = min(candidates, key=lambda row: abs(complex(row["root"]) - endpoint_root))
    residual = abs(complex(selected["root"]) - endpoint_root) / max(
        1.0, abs(complex(selected["root"])), abs(endpoint_root)
    )
    if residual > 2.0e-5:
        raise RuntimeError(f"endpoint collision root mismatch: {residual}")
    return selected


def residue_probe(
    root: complex,
    group: dict[str, Any],
    groups: list[dict[str, Any]],
    ownership: dict[str, bool],
    global_residue_nodes: int,
    relative_residue_nodes: int,
) -> dict[str, Any]:
    other_roots = [
        complex(row["root"])
        for row in groups
        if abs(root - complex(row["root"]))
        > 1.0e-7 * max(1.0, abs(root), abs(complex(row["root"])))
    ]
    separations = [abs(root - other) for other in other_roots]
    safe_scale = min([abs(root)] + separations)
    outer_radius = 0.1 * safe_scale
    inner_radius = 0.05 * safe_scale
    outer = N5030.pair_local_relative_residue(
        root,
        outer_radius,
        max(32, relative_residue_nodes + 8),
        group["pairs"],
        ownership,
        max(32, global_residue_nodes + 8),
    )
    inner = N5030.pair_local_relative_residue(
        root,
        inner_radius,
        max(48, relative_residue_nodes + 24),
        group["pairs"],
        ownership,
        max(48, global_residue_nodes + 16),
    )
    maximum_magnitude = max(abs(outer), abs(inner))
    return {
        "safe_scale": float(safe_scale),
        "outer_radius": float(outer_radius),
        "inner_radius": float(inner_radius),
        "outer_residue": outer,
        "inner_residue": inner,
        "maximum_residue_magnitude": float(maximum_magnitude),
        "numerically_zero": maximum_magnitude < ZERO_RESIDUE_ABSOLUTE_TOLERANCE,
    }


def sector_samples(
    base_log: complex,
    direction: complex,
    ownership: dict[str, bool],
    floor: float,
    global_nodes: int,
    global_residue_nodes: int,
) -> dict[float, complex]:
    fractions = (floor / 2.0, floor, 2.0 * floor, 4.0 * floor)
    return {
        fraction: ORIGINAL_GLOBAL_CHAMBER_VALUE(
            cmath.exp(base_log + fraction * direction),
            ownership,
            global_nodes,
            global_residue_nodes,
        )
        for fraction in fractions
    }


def build_certificates(
    topology: dict[str, Any],
    floor: float,
    global_nodes: int,
    global_residue_nodes: int,
    relative_residue_nodes: int,
    residue_cache: dict[tuple[int, str], dict[str, Any]] | None = None,
) -> tuple[list[dict[str, Any]], dict[tuple[int, str], dict[str, Any]]]:
    _, ownerships = N5030.physical_chambers()
    chamber_count = len(topology["chambers"])
    if chamber_count != len(ownerships):
        raise RuntimeError("topology and physical chamber counts differ")
    cache = {} if residue_cache is None else residue_cache
    certificates: list[dict[str, Any]] = []
    for boundary_index in range(chamber_count):
        right_index = boundary_index
        left_index = (boundary_index - 1) % chamber_count
        right_start = complex(
            topology["chambers"][right_index]["target_start_log"]
        )
        endpoint_root = cmath.exp(right_start)
        side_specs = (
            (
                "left",
                left_index,
                complex(topology["chambers"][left_index]["target_end_log"]),
                complex(topology["chambers"][left_index]["target_start_log"])
                - complex(topology["chambers"][left_index]["target_end_log"]),
            ),
            (
                "right",
                right_index,
                right_start,
                complex(topology["chambers"][right_index]["target_end_log"])
                - right_start,
            ),
        )
        boundary_rows: list[dict[str, Any]] = []
        for side, chamber_index, base_log, direction in side_specs:
            ownership = ownerships[chamber_index]
            groups = N5030.collision_groups(N5030.TARGET_COSINE, ownership)
            group = endpoint_group(groups, endpoint_root)
            root = complex(group["root"])
            cache_key = (boundary_index, side)
            if cache_key not in cache:
                cache[cache_key] = residue_probe(
                    root,
                    group,
                    groups,
                    ownership,
                    global_residue_nodes,
                    relative_residue_nodes,
                )
            residue = cache[cache_key]
            samples = sector_samples(
                base_log,
                direction,
                ownership,
                floor,
                global_nodes,
                global_residue_nodes,
            )
            fine_limit = quadratic_zero_limit(
                samples[floor / 2.0], samples[floor], samples[2.0 * floor]
            )
            coarse_limit = quadratic_zero_limit(
                samples[floor], samples[2.0 * floor], samples[4.0 * floor]
            )
            limit_residual = relative_difference(fine_limit, coarse_limit)
            derivative_bound = max(
                abs(value - fine_limit) / fraction
                for fraction, value in samples.items()
            )
            polynomial_points = (
                (floor / 2.0, samples[floor / 2.0]),
                (floor, samples[floor]),
                (2.0 * floor, samples[2.0 * floor]),
            )
            boundary_rows.append(
                {
                    "boundary_index": boundary_index,
                    "side": side,
                    "chamber_index": chamber_index,
                    "ownership": ownership,
                    "ownership_digest": ownership_digest(ownership),
                    "base_log": base_log,
                    "direction": direction,
                    "endpoint_root": endpoint_root,
                    "collision_root": root,
                    "collision_root_relative_residual": relative_difference(
                        root, endpoint_root
                    ),
                    "pairs": [tuple(pair) for pair in group["pairs"]],
                    "residue_probe": residue,
                    "sample_floor": float(floor),
                    "samples": samples,
                    "fine_limit": fine_limit,
                    "coarse_limit": coarse_limit,
                    "limit_relative_residual": limit_residual,
                    "derivative_bound": float(derivative_bound),
                    "polynomial_points": polynomial_points,
                    "side_valid": bool(
                        residue["numerically_zero"]
                        and limit_residual < LIMIT_RELATIVE_TOLERANCE
                    ),
                }
            )
        adjacent_residual = relative_difference(
            boundary_rows[0]["fine_limit"], boundary_rows[1]["fine_limit"]
        )
        boundary_valid = bool(
            all(row["side_valid"] for row in boundary_rows)
            and adjacent_residual < ADJACENT_LIMIT_RELATIVE_TOLERANCE
        )
        for row in boundary_rows:
            row["adjacent_limit_relative_residual"] = adjacent_residual
            row["boundary_valid"] = boundary_valid
            certificates.append(row)
    return certificates, cache


def serialized_residue_probe(row: dict[str, Any]) -> dict[str, Any]:
    return {
        **{
            key: value
            for key, value in row.items()
            if key not in {"outer_residue", "inner_residue"}
        },
        "outer_residue": serialized_complex(row["outer_residue"]),
        "inner_residue": serialized_complex(row["inner_residue"]),
    }


def serialized_certificate(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "boundary_index": row["boundary_index"],
        "side": row["side"],
        "chamber_index": row["chamber_index"],
        "ownership_digest": row["ownership_digest"],
        "base_log": serialized_complex(row["base_log"]),
        "direction": serialized_complex(row["direction"]),
        "endpoint_root": serialized_complex(row["endpoint_root"]),
        "collision_root": serialized_complex(row["collision_root"]),
        "collision_root_relative_residual": row[
            "collision_root_relative_residual"
        ],
        "pairs": [list(pair) for pair in row["pairs"]],
        "residue_probe": serialized_residue_probe(row["residue_probe"]),
        "sample_floor": row["sample_floor"],
        "samples": [
            {
                "fraction": fraction,
                "value": serialized_complex(value),
            }
            for fraction, value in sorted(row["samples"].items())
        ],
        "fine_limit": serialized_complex(row["fine_limit"]),
        "coarse_limit": serialized_complex(row["coarse_limit"]),
        "limit_relative_residual": row["limit_relative_residual"],
        "adjacent_limit_relative_residual": row[
            "adjacent_limit_relative_residual"
        ],
        "derivative_bound": row["derivative_bound"],
        "side_valid": row["side_valid"],
        "boundary_valid": row["boundary_valid"],
    }


class SectorExtension:
    def __init__(self, certificates: list[dict[str, Any]]) -> None:
        self.certificates = [row for row in certificates if row["boundary_valid"]]
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
            digest = ownership_digest(ownership)
            candidates: list[tuple[float, float, float, dict[str, Any]]] = []
            for certificate in self.certificates:
                if certificate["ownership_digest"] != digest:
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
                -1.0e-12 <= parameter <= MAXIMUM_EXTENSION_PARAMETER
                and transverse <= MAXIMUM_EXTENSION_TRANSVERSE_DISTANCE
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
                    "relative_circle": serialized_complex(relative_circle),
                    "log_distance": float(distance),
                    "sector_parameter": parameter,
                    "transverse_distance": transverse,
                    "returned_value": serialized_complex(value),
                    "absolute_error_bound": float(error_bound),
                    "original_error": str(error),
                }
            )
            return value


def copy_topology(
    run_directory: Path,
    scratch_run: Path,
    job: dict[str, Any],
) -> None:
    source = M5035.M5034.topology_path(
        run_directory, job["event_id"], job["argument_id"]
    )
    target = M5035.M5034.topology_path(
        scratch_run, job["event_id"], job["argument_id"]
    )
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)


def expected_job(job: dict[str, Any]) -> dict[str, Any]:
    return {
        key: job[key]
        for key in (
            "job_key",
            "epsilon_id",
            "evaluation_epsilon",
            "event_id",
            "argument_id",
            "base_argument_id",
            "tier",
        )
    }


def execute_variant(
    label: str,
    scratch_run: Path,
    run_directory: Path,
    config: dict[str, Any],
    job: dict[str, Any],
    certificates: list[dict[str, Any]],
) -> dict[str, Any]:
    copy_topology(run_directory, scratch_run, job)
    extension = SectorExtension(certificates)
    CHART_REPAIR.CURRENT_JOB = f"{job['job_key']}::{label}"
    CHART_REPAIR.EXCLUSION_AUDIT.clear()
    CHART_REPAIR.RADIUS_AUDIT.clear()
    N5030.chamber_residue_catalog = CHART_REPAIR.repaired_chamber_residue_catalog
    N5030.global_chamber_value = extension
    started = time.monotonic()
    try:
        result = M5035.execute_job(scratch_run, config, expected_job(job))
    finally:
        N5030.chamber_residue_catalog = ORIGINAL_CHAMBER_RESIDUE_CATALOG
        N5030.global_chamber_value = ORIGINAL_GLOBAL_CHAMBER_VALUE
    kernel_path = scratch_run / "kernels" / f"{job['job_key']}.json"
    kernel = (
        json.loads(kernel_path.read_text(encoding="utf-8"))
        if kernel_path.exists()
        else None
    )
    return {
        "label": label,
        "result": result,
        "kernel": kernel,
        "extension_calls": list(extension.calls),
        "chart_origin_exclusions": list(CHART_REPAIR.EXCLUSION_AUDIT),
        "radius_audit": list(CHART_REPAIR.RADIUS_AUDIT),
        "runtime_seconds": time.monotonic() - started,
    }


def numeric_result(result: dict[str, Any]) -> bool:
    return bool(
        result.get("status") == "COMPLETED_CONVERGED"
        and result.get("integral_converged")
        and isinstance(result.get("normalized_direct_D_hhh_over_G3"), dict)
    )


def result_value(result: dict[str, Any]) -> complex:
    return M5035.complex_from_row(result["normalized_direct_D_hhh_over_G3"])


def compact_variant(row: dict[str, Any]) -> dict[str, Any]:
    result = row["result"]
    return {
        "label": row["label"],
        "status": result.get("status"),
        "error_type": result.get("error_type"),
        "error": result.get("error"),
        "integral_converged": result.get("integral_converged"),
        "normalized_direct_D_hhh_over_G3": result.get(
            "normalized_direct_D_hhh_over_G3"
        ),
        "highest_two_order_relative_residual": result.get(
            "highest_two_order_relative_residual"
        ),
        "extension_call_count": len(row["extension_calls"]),
        "extension_calls": row["extension_calls"],
        "chart_origin_exclusion_count": len(row["chart_origin_exclusions"]),
        "radius_adjustment_count": len(row["radius_audit"]),
        "runtime_seconds": row["runtime_seconds"],
    }


def run(arguments: argparse.Namespace) -> dict[str, Any]:
    run_directory = RUNS / arguments.run_id
    config_path = run_directory / "config.json"
    config = json.loads(config_path.read_text(encoding="utf-8"))
    recorded_digest = config["source_files"].get(str(PRODUCTION_SCRIPT))
    if recorded_digest != M5036.file_digest(PRODUCTION_SCRIPT):
        raise RuntimeError("5037 production runner changed after its locked run")
    job_path = run_directory / "jobs" / f"{arguments.job_key}.json"
    job = json.loads(job_path.read_text(encoding="utf-8"))
    event = M5035.event_lookup(config)[job["event_id"]]
    argument = M5035.argument_lookup(config)[job["argument_id"]]
    tier = config["tiers"][job["tier"]]
    target = M5035.complex_from_row(argument["target_cosine"])
    M5035.M5034.configure(event, target)
    topology_path = M5035.M5034.topology_path(
        run_directory, job["event_id"], job["argument_id"]
    )
    topology = json.loads(topology_path.read_text(encoding="utf-8"))
    repair_directory = REPAIRS / arguments.repair_id
    primary_scratch = repair_directory / "primary_scratch"
    audit_scratch = repair_directory / "audit_scratch"
    original_directory = repair_directory / "original"
    repaired_directory = repair_directory / "repaired"
    started = time.monotonic()

    primary_certificates, residue_cache = build_certificates(
        topology,
        arguments.sector_floor,
        int(tier["global_nodes"]),
        int(tier["global_residue_nodes"]),
        int(tier["relative_residue_nodes"]),
    )
    audit_certificates, _ = build_certificates(
        topology,
        arguments.audit_sector_floor,
        int(tier["global_nodes"]),
        int(tier["global_residue_nodes"]),
        int(tier["relative_residue_nodes"]),
        residue_cache,
    )
    certificate_gate = all(
        row["boundary_valid"]
        for row in primary_certificates + audit_certificates
    )
    primary = execute_variant(
        "primary", primary_scratch, run_directory, config, job, primary_certificates
    )
    audit = execute_variant(
        "audit", audit_scratch, run_directory, config, job, audit_certificates
    )
    kernel_residual = None
    if numeric_result(primary["result"]) and numeric_result(audit["result"]):
        kernel_residual = relative_difference(
            result_value(primary["result"]), result_value(audit["result"])
        )
    accepted = bool(
        certificate_gate
        and numeric_result(primary["result"])
        and numeric_result(audit["result"])
        and len(primary["extension_calls"]) > 0
        and len(audit["extension_calls"]) > 0
        and kernel_residual is not None
        and kernel_residual < AUDIT_KERNEL_RELATIVE_TOLERANCE
    )

    serialized_primary_certificates = [
        serialized_certificate(row) for row in primary_certificates
    ]
    serialized_audit_certificates = [
        serialized_certificate(row) for row in audit_certificates
    ]
    repair_contract = {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "repair_script": str(Path(__file__).resolve()),
        "repair_script_sha256": M5036.file_digest(Path(__file__).resolve()),
        "chart_repair_script": str(CHART_REPAIR_SCRIPT),
        "chart_repair_script_sha256": M5036.file_digest(CHART_REPAIR_SCRIPT),
        "production_script": str(PRODUCTION_SCRIPT),
        "production_script_sha256": M5036.file_digest(PRODUCTION_SCRIPT),
        "topology_file": str(topology_path),
        "topology_file_sha256": M5036.file_digest(topology_path),
        "primary_sector_floor": arguments.sector_floor,
        "audit_sector_floor": arguments.audit_sector_floor,
        "zero_residue_absolute_tolerance": ZERO_RESIDUE_ABSOLUTE_TOLERANCE,
        "limit_relative_tolerance": LIMIT_RELATIVE_TOLERANCE,
        "adjacent_limit_relative_tolerance": ADJACENT_LIMIT_RELATIVE_TOLERANCE,
        "audit_kernel_relative_tolerance": AUDIT_KERNEL_RELATIVE_TOLERANCE,
        "primary_certificates": serialized_primary_certificates,
        "audit_certificates": serialized_audit_certificates,
        "primary_extension_calls": primary["extension_calls"],
        "audit_extension_calls": audit["extension_calls"],
        "primary_chart_origin_exclusions": primary["chart_origin_exclusions"],
        "audit_chart_origin_exclusions": audit["chart_origin_exclusions"],
        "primary_radius_audit": primary["radius_audit"],
        "audit_radius_audit": audit["radius_audit"],
        "kernel_relative_residual": kernel_residual,
        "certificate_gate": certificate_gate,
        "accepted": accepted,
        "derivation": (
            "the endpoint double residue vanishes, both inherited ownership "
            "sectors have the same finite one-sided limit, and only evaluations "
            "inside the numerical root-coincidence tube use the certified "
            "quadratic continuous extension"
        ),
        "target_fit_or_representative_interpolation_used": False,
        "valid_for_full_MTS_claim": False,
    }

    promoted = False
    if accepted and arguments.promote:
        original_directory.mkdir(parents=True, exist_ok=True)
        shutil.copy2(job_path, original_directory / job_path.name)
        original_kernel_path = run_directory / "kernels" / job_path.name
        if original_kernel_path.exists():
            shutil.copy2(
                original_kernel_path,
                original_directory / f"kernel__{job_path.name}",
            )
        result = dict(primary["result"])
        kernel = dict(primary["kernel"])
        result["repair_contract"] = repair_contract
        result["residue_radius_contract"] = {
            "revision": REVISION,
            "chart_origin_exclusion_count": len(
                primary["chart_origin_exclusions"]
            ),
            "endpoint_sector_extension_count": len(primary["extension_calls"]),
            "repair_script": str(Path(__file__).resolve()),
            "repair_script_sha256": M5036.file_digest(Path(__file__).resolve()),
            "valid_for_full_MTS_claim": False,
        }
        kernel["repair_contract"] = repair_contract
        kernel["residue_radius_contract"] = result["residue_radius_contract"]
        kernel["fixed_event_integral_gate"]["relative_residue_revision"] = REVISION
        repaired_directory.mkdir(parents=True, exist_ok=True)
        M5036.atomic_json(repaired_directory / job_path.name, result)
        M5036.atomic_json(
            repaired_directory / f"kernel__{job_path.name}", kernel
        )
        M5036.atomic_json(job_path, result)
        M5036.atomic_json(original_kernel_path, kernel)
        promoted = True
        jobs = M5036.load_jobs(run_directory)
        summary = M5037.write_augmented_status(
            run_directory,
            config,
            jobs,
            "PAUSED_AFTER_FINITE_ENDPOINT_SECTOR_REPAIR",
            started,
        )
        M5037.write_checkpoint_artifacts(config, summary, run_directory)
        M5036.append_log(
            run_directory,
            f"finite endpoint sector repair promoted {job['job_key']}",
        )

    summary = {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "run_id": arguments.run_id,
        "job_key": job["job_key"],
        "target_cosine": serialized_complex(target),
        "certificate_gate": certificate_gate,
        "primary": compact_variant(primary),
        "audit": compact_variant(audit),
        "kernel_relative_residual": kernel_residual,
        "accepted": accepted,
        "promoted": promoted,
        "repair_contract": repair_contract,
        "runtime_seconds": time.monotonic() - started,
        "valid_for_full_MTS_claim": False,
    }
    M5036.atomic_json(repair_directory / "repair_summary.json", summary)
    print(json.dumps(summary, indent=2))
    return summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-id", default="paired_outer_precision_s4_v1")
    parser.add_argument(
        "--job-key", default="E040__S503403_N0000__A14__primary24"
    )
    parser.add_argument("--repair-id", default="finite_endpoint_sector_v1")
    parser.add_argument("--sector-floor", type=float, default=1.0e-9)
    parser.add_argument("--audit-sector-floor", type=float, default=2.0e-9)
    parser.add_argument("--promote", action="store_true")
    run(parser.parse_args())


if __name__ == "__main__":
    main()
