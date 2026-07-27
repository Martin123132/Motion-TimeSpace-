from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
from typing import Any

import mpmath as mp


POST = Path(__file__).resolve().parents[1]
ROOT = POST.parent
FORMAL = ROOT / "formalization-workbench"
SCRIPT_5040 = (
    POST
    / "scripts"
    / "Y5_R2FR_5040_arbitrary_precision_cross_source_residue.py"
)
V12 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5079"
    / "runs"
    / "bounded_central_anchor_pilot_v12"
)
CURRENT_CONFIG = V12 / "config.json"
CURRENT_TOPOLOGY = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5111"
    / "runs"
    / "E020_primary_complex_control_extension_v1"
    / "topologies"
    / "S507611_N0000__E020_A00.json"
)
SOURCE = POST / "source-intake" / "functional_rg" / "5112"
RESULT_JSON = SOURCE / "recoil_holomorphy_scope_correction.json"
REGISTRY_JSON = SOURCE / "event_local_direct_zero_registry.json"
AUDIT_CSV = SOURCE / "direct_component_arbitrary_precision_audit.csv"
VALIDATION_CSV = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5112_VALIDATION.csv"
)
MARKER = "MTS_5112_RECOIL_HOLOMORPHY_SCOPE_CORRECTION"
REVISION = "source-separated-direct-residue-scope-correction-v1"
FORMAL_BASELINE = (
    "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
)
ZERO_TOLERANCE = 1.0e-20
NONZERO_FLOOR = 1.0e-8
NONZERO_RELATIVE_SPREAD_TOLERANCE = 1.0e-9
ROOT_MATCH_TOLERANCE = 2.0e-8


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5040 = load_module("mts_5040_for_5112", SCRIPT_5040)
N5030 = M5040.N5030


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


def serialized(value: mp.mpc | complex) -> dict[str, str]:
    return {
        "real": mp.nstr(mp.re(value), 50),
        "imaginary": mp.nstr(mp.im(value), 50),
    }


def complex_from_serialized(value: dict[str, Any]) -> complex:
    return complex(float(value["real"]), float(value["imaginary"]))


def canonical_pairs(value: list[list[str]] | list[tuple[str, str]]) -> tuple[tuple[str, str], ...]:
    return tuple(sorted(tuple(sorted((str(pair[0]), str(pair[1])))) for pair in value))


def v12_promotions() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for job_path in sorted((V12 / "jobs").glob("*.json")):
        job = json.loads(job_path.read_text(encoding="utf-8"))
        promotions = job.get("profile_audit", {}).get(
            "guarded_recoil_zero_certificate_rows", []
        )
        if not promotions:
            continue
        kernel_path = V12 / "kernels" / job_path.name
        kernel = json.loads(kernel_path.read_text(encoding="utf-8"))
        for promotion in promotions:
            certificate = promotion["certificate"]
            rows.append(
                {
                    "scope": "v12_historical_5084_promotion",
                    "job_key": str(job["job_key"]),
                    "event": kernel["event"],
                    "argument": kernel["argument"],
                    "pairs": [list(pair) for pair in promotion["pairs"]],
                    "root": certificate["root"],
                    "safe_scale": float(certificate["relative_safe_scale"]),
                    "source_job": str(job_path.resolve()),
                    "source_job_sha256": digest(job_path),
                    "source_kernel": str(kernel_path.resolve()),
                    "source_kernel_sha256": digest(kernel_path),
                    "previous_numeric_probe": promotion["original_numeric_probe"],
                }
            )
    return rows


def current_collision_records() -> list[dict[str, Any]]:
    config = json.loads(CURRENT_CONFIG.read_text(encoding="utf-8"))
    event = next(row for row in config["events"] if int(row["seed"]) == 507611)
    argument = next(
        row for row in config["arguments"] if row["argument_id"] == "E020_A00"
    )
    topology = json.loads(CURRENT_TOPOLOGY.read_text(encoding="utf-8"))
    pair = ["direct:g2:plus_u", "subtraction:decay:minus_u"]
    crossings = [
        row
        for chamber in topology["chambers"]
        for row in chamber["surface_crossings"]
        if any(set(candidate) == set(pair) for candidate in row["representing_pairs"])
    ]
    if len(crossings) != 2:
        raise RuntimeError("5111 topology no longer contains the inner/outer collision pair")
    roots = sorted((complex(row["target_root"]) for row in crossings), key=abs)
    return [
        {
            "scope": "5111_first_job_inner_collision",
            "job_key": "E020__S507611_N0000__A00__primary24",
            "event": event,
            "argument": argument,
            "pairs": [pair],
            "root": {"real": roots[0].real, "imaginary": roots[0].imag},
            "safe_scale": 0.002526315031088964,
            "source_topology": str(CURRENT_TOPOLOGY.resolve()),
            "source_topology_sha256": digest(CURRENT_TOPOLOGY),
        },
        {
            "scope": "5111_first_job_outer_collision",
            "job_key": "E020__S507611_N0000__A00__primary24",
            "event": event,
            "argument": argument,
            "pairs": [pair],
            "root": {"real": roots[1].real, "imaginary": roots[1].imag},
            "safe_scale": 2.1135337496209985,
            "source_topology": str(CURRENT_TOPOLOGY.resolve()),
            "source_topology_sha256": digest(CURRENT_TOPOLOGY),
        },
    ]


def configure(record: dict[str, Any]) -> dict[str, bool]:
    target = complex(
        float(record["argument"]["target_cosine"]["real"]),
        float(record["argument"]["target_cosine"]["imaginary"]),
    )
    M5040.M5034.configure(record["event"], target)
    ownerships = N5030.physical_chambers()[1]
    chamber_index = int(record.get("chamber_index", 0))
    if not 0 <= chamber_index < len(ownerships):
        raise RuntimeError(f"invalid physical chamber index {chamber_index}")
    return ownerships[chamber_index]


def selected_global_data(
    relative_circle: mp.mpc,
    collision_pairs: list[tuple[str, str]],
    ownership: dict[str, bool],
) -> tuple[str, int, complex, float]:
    soft_direction, decay_direction, internal = N5030.M5028.event_geometry(
        N5030.SOFT_ENERGY,
        complex(N5030.SOFT_COSINE, 0.0),
        complex(N5030.DECAY_COSINE, 0.0),
        complex(relative_circle),
    )
    groups = N5030.M5028.fixed_ownership_groups(
        internal,
        soft_direction,
        decay_direction,
        N5030.TARGET_COSINE,
        ownership,
    )
    owned_labels = {
        label
        for pair in collision_pairs
        for label in pair
        if bool(ownership[label])
    }
    selected = [
        group for group in groups if owned_labels.intersection(group["labels"])
    ]
    if len(owned_labels) != 1 or len(selected) != 1:
        raise RuntimeError("direct-source evaluator requires one causally owned pole")
    label = next(iter(owned_labels))
    if not label.startswith(("direct:g1:", "direct:g2:")):
        raise RuntimeError(f"unsupported owned recoil label {label}")
    source_index = int(label.split(":")[1][1:]) - 1
    selected_root = complex(selected[0]["root"])
    separations = [
        abs(selected_root - complex(group["root"]))
        for group in groups
        if group is not selected[0]
    ]
    safe_scale = min([abs(selected_root)] + separations)
    return label, source_index, selected_root, safe_scale


def direct_global_residue(
    relative_circle: mp.mpc,
    collision_pairs: list[tuple[str, str]],
    ownership: dict[str, bool],
    nodes: int,
    radius_fraction: float,
) -> mp.mpc:
    label, source_index, transported_root, safe_scale = selected_global_data(
        relative_circle, collision_pairs, ownership
    )
    soft_direction, decay_direction, internal = M5040.event_geometry(
        N5030.SOFT_ENERGY,
        complex(N5030.SOFT_COSINE, 0.0),
        complex(N5030.DECAY_COSINE, 0.0),
        relative_circle,
    )
    direction = [
        internal[source_index][index] / internal[source_index][0]
        for index in range(1, 4)
    ]
    root = M5040.factor_root(
        direction, N5030.TARGET_COSINE, label.rsplit(":", 1)[1]
    )
    root_residual = abs(complex(root) - transported_root) / max(
        1.0, abs(transported_root)
    )
    if root_residual > ROOT_MATCH_TOLERANCE:
        raise RuntimeError(f"arbitrary-precision root mismatch: {root_residual}")
    radius = mp.mpf(str(radius_fraction * safe_scale))
    total = mp.mpc(0)
    for index in range(nodes):
        phase = mp.e ** (
            2j * mp.pi * (mp.mpf(index) + mp.mpf("0.317")) / nodes
        )
        unit_circle = root + radius * phase
        total += (
            M5040.finite_plus_component(
                "direct",
                internal,
                N5030.SOFT_ENERGY,
                soft_direction,
                decay_direction,
                N5030.TARGET_COSINE,
                unit_circle,
            )
            / unit_circle
            * radius
            * phase
        )
    return total / nodes


def direct_relative_residue(
    root: complex,
    safe_scale: float,
    collision_pairs: list[tuple[str, str]],
    ownership: dict[str, bool],
    relative_nodes: int,
    global_nodes: int,
    relative_fraction: float,
    global_fraction: float,
) -> mp.mpc:
    radius = mp.mpf(str(relative_fraction * safe_scale))
    root_mp = M5040.mpc(root)
    total = mp.mpc(0)
    for index in range(relative_nodes):
        phase = mp.e ** (
            2j * mp.pi * (mp.mpf(index) + mp.mpf("0.317")) / relative_nodes
        )
        relative_circle = root_mp + radius * phase
        total += (
            direct_global_residue(
                relative_circle,
                collision_pairs,
                ownership,
                global_nodes,
                global_fraction,
            )
            / relative_circle
            * radius
            * phase
        )
    return total / relative_nodes


def evaluate_record(
    record: dict[str, Any],
    relative_nodes: int,
    global_nodes: int,
    relative_fractions: tuple[float, ...],
    global_fractions: tuple[float, ...],
) -> dict[str, Any]:
    ownership = configure(record)
    root = complex_from_serialized(record["root"])
    pairs = [tuple(str(value) for value in pair) for pair in record["pairs"]]
    values: list[dict[str, Any]] = []
    for relative_fraction in relative_fractions:
        for global_fraction in global_fractions:
            value = direct_relative_residue(
                root,
                float(record["safe_scale"]),
                pairs,
                ownership,
                relative_nodes,
                global_nodes,
                relative_fraction,
                global_fraction,
            )
            values.append(
                {
                    "relative_fraction": relative_fraction,
                    "global_fraction": global_fraction,
                    "value": serialized(value),
                    "magnitude": float(abs(value)),
                }
            )
    complex_values = [complex_from_serialized(row["value"]) for row in values]
    mean = sum(complex_values) / len(complex_values)
    maximum_spread = max(abs(value - mean) for value in complex_values)
    maximum_magnitude = max(abs(value) for value in complex_values)
    minimum_magnitude = min(abs(value) for value in complex_values)
    if maximum_magnitude < ZERO_TOLERANCE:
        classification = "EVENT_LOCAL_ARBITRARY_PRECISION_ZERO"
    elif (
        minimum_magnitude > NONZERO_FLOOR
        and maximum_spread / abs(mean) < NONZERO_RELATIVE_SPREAD_TOLERANCE
    ):
        classification = "STABLE_DIRECT_COMPONENT_NONZERO"
    else:
        classification = "UNRESOLVED"
    return {
        **record,
        "root_modulus": abs(root),
        "relative_nodes": relative_nodes,
        "global_nodes": global_nodes,
        "relative_fractions": list(relative_fractions),
        "global_fractions": list(global_fractions),
        "values": values,
        "mean": {"real": mean.real, "imaginary": mean.imag},
        "maximum_spread": maximum_spread,
        "maximum_magnitude": maximum_magnitude,
        "minimum_magnitude": minimum_magnitude,
        "classification": classification,
        "valid_for_full_MTS_claim": False,
    }


def registry_row(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "job_key": row["job_key"],
        "event_id": row["event"]["event_id"],
        "argument_id": row["argument"]["argument_id"],
        "pairs": row["pairs"],
        "root": row["root"],
        "root_match_relative_tolerance": ROOT_MATCH_TOLERANCE,
        "classification": row["classification"],
        "maximum_magnitude": row["maximum_magnitude"],
        "zero_tolerance": ZERO_TOLERANCE,
        "mean": row["mean"],
        "scope": "exact job, event, argument, pair, ownership, and collision root only",
        "valid_for_full_MTS_claim": False,
    }


def write_audit_csv(rows: list[dict[str, Any]]) -> None:
    AUDIT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with AUDIT_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=(
                "scope",
                "job_key",
                "event_id",
                "argument_id",
                "pairs",
                "root_real",
                "root_imaginary",
                "root_modulus",
                "mean_real",
                "mean_imaginary",
                "maximum_magnitude",
                "maximum_spread",
                "classification",
                "valid_for_full_MTS_claim",
            ),
        )
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    "scope": row["scope"],
                    "job_key": row["job_key"],
                    "event_id": row["event"]["event_id"],
                    "argument_id": row["argument"]["argument_id"],
                    "pairs": json.dumps(row["pairs"], separators=(",", ":")),
                    "root_real": row["root"]["real"],
                    "root_imaginary": row["root"]["imaginary"],
                    "root_modulus": row["root_modulus"],
                    "mean_real": row["mean"]["real"],
                    "mean_imaginary": row["mean"]["imaginary"],
                    "maximum_magnitude": row["maximum_magnitude"],
                    "maximum_spread": row["maximum_spread"],
                    "classification": row["classification"],
                    "valid_for_full_MTS_claim": False,
                }
            )


def write_validation(checks: list[tuple[str, bool, str]]) -> None:
    VALIDATION_CSV.parent.mkdir(parents=True, exist_ok=True)
    with VALIDATION_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(("check", "passed", "detail"))
        for name, passed, detail in checks:
            writer.writerow((name, str(bool(passed)).lower(), detail))


def run(arguments: argparse.Namespace) -> dict[str, Any]:
    if arguments.dps < 50 or arguments.relative_nodes < 16 or arguments.global_nodes < 16:
        raise ValueError("5112 precision floors are dps>=50 and nodes>=16")
    mp.mp.dps = arguments.dps
    historical = v12_promotions()
    current = current_collision_records()
    records = historical + current
    evaluated = [
        evaluate_record(
            record,
            arguments.relative_nodes,
            arguments.global_nodes,
            tuple(arguments.relative_fractions),
            tuple(arguments.global_fractions),
        )
        for record in records
    ]
    historical_rows = [
        row for row in evaluated if row["scope"] == "v12_historical_5084_promotion"
    ]
    inner = next(row for row in evaluated if row["scope"].endswith("inner_collision"))
    outer = next(row for row in evaluated if row["scope"].endswith("outer_collision"))
    registry_rows = [
        registry_row(row)
        for row in evaluated
        if row["classification"] == "EVENT_LOCAL_ARBITRARY_PRECISION_ZERO"
    ]
    registry = {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "policy": "event-local arbitrary-precision zeros only; no structural family theorem",
        "zero_tolerance": ZERO_TOLERANCE,
        "rows": registry_rows,
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(REGISTRY_JSON, registry)
    write_audit_csv(evaluated)
    formal_hash = tree_digest(FORMAL)
    checks = [
        ("formalization_workbench_unchanged", formal_hash == FORMAL_BASELINE, formal_hash),
        ("historical_promotion_count_is_eight", len(historical_rows) == 8, str(len(historical_rows))),
        (
            "historical_promotions_rechecked_as_event_local_zeros",
            all(row["classification"] == "EVENT_LOCAL_ARBITRARY_PRECISION_ZERO" for row in historical_rows),
            json.dumps([row["classification"] for row in historical_rows]),
        ),
        (
            "5111_inner_collision_is_event_local_zero",
            inner["classification"] == "EVENT_LOCAL_ARBITRARY_PRECISION_ZERO",
            inner["classification"],
        ),
        (
            "5111_outer_collision_is_stable_direct_nonzero",
            outer["classification"] == "STABLE_DIRECT_COMPONENT_NONZERO",
            outer["classification"],
        ),
        (
            "inner_and_outer_share_the_same_pair",
            canonical_pairs(inner["pairs"]) == canonical_pairs(outer["pairs"]),
            json.dumps(inner["pairs"]),
        ),
        (
            "all_source_paths_exist",
            all(
                Path(row[key]).exists()
                for row in records
                for key in ("source_job", "source_kernel", "source_topology")
                if key in row
            ),
            str(len(records)),
        ),
        (
            "registry_contains_only_zero_rows",
            len(registry_rows) == len(historical_rows) + 1,
            str(len(registry_rows)),
        ),
        ("no_full_MTS_claim", all(not row["valid_for_full_MTS_claim"] for row in evaluated), str(len(evaluated))),
    ]
    write_validation(checks)
    passed = all(check[1] for check in checks)
    result = {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "dps": arguments.dps,
        "records": evaluated,
        "historical_5084_promotions_rechecked": len(historical_rows),
        "event_local_zero_registry": str(REGISTRY_JSON.resolve()),
        "event_local_zero_registry_sha256": digest(REGISTRY_JSON),
        "direct_component_audit_csv": str(AUDIT_CSV.resolve()),
        "direct_component_audit_csv_sha256": digest(AUDIT_CSV),
        "broad_5084_recoil_holomorphy_theorem_rejected": outer["classification"] == "STABLE_DIRECT_COMPONENT_NONZERO",
        "finite_x_catalog_completeness_is_not_a_valid_holomorphy_proof": True,
        "stable_catalog_rows_take_precedence_over_the_rejected_structural_theorem": True,
        "unstable_rows_require_exact_event_local_registry_match": True,
        "runner_integration_authorized": passed,
        "validation_csv": str(VALIDATION_CSV.resolve()),
        "formalization_workbench_tree_sha256": formal_hash,
        "passed": passed,
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(RESULT_JSON, result)
    return result


def parse_floats(value: str) -> list[float]:
    return [float(item.strip()) for item in value.split(",") if item.strip()]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dps", type=int, default=60)
    parser.add_argument("--relative-nodes", type=int, default=24)
    parser.add_argument("--global-nodes", type=int, default=24)
    parser.add_argument("--relative-fractions", type=parse_floats, default=[0.1, 0.05])
    parser.add_argument("--global-fractions", type=parse_floats, default=[0.15, 0.3])
    arguments = parser.parse_args()
    result = run(arguments)
    print(
        json.dumps(
            {
                "checkpoint_marker": result["checkpoint_marker"],
                "historical_5084_promotions_rechecked": result[
                    "historical_5084_promotions_rechecked"
                ],
                "broad_5084_recoil_holomorphy_theorem_rejected": result[
                    "broad_5084_recoil_holomorphy_theorem_rejected"
                ],
                "runner_integration_authorized": result[
                    "runner_integration_authorized"
                ],
                "passed": result["passed"],
            },
            indent=2,
        )
    )
    if not result["passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
