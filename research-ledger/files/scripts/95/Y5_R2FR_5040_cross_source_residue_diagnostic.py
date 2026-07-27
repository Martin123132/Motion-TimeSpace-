from __future__ import annotations

import csv
import importlib.util
import json
from pathlib import Path
from typing import Any


POST = Path(__file__).resolve().parents[1]
RUNNER = POST / "scripts" / "Y5_R2FR_5040_nested_sobol_variance_reduction.py"
SOURCE = POST / "source-intake" / "functional_rg" / "5040"
RUN = SOURCE / "runs" / "nested_sobol_power1_s4_v1"
OUTPUT = SOURCE / "cross_source_residue_diagnostic.json"
OUTPUT_CSV = SOURCE / "cross_source_residue_diagnostic.csv"
MARKER = "MTS_5040_CROSS_SOURCE_RESIDUE_DIAGNOSTIC"
FRACTIONS = (0.2, 0.1, 0.05, 0.025)
NODE_FLOORS = (64, 96)
ZERO_THRESHOLD = 1.0e-7


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5040 = load_module("mts_5040_for_cross_source_diagnostic", RUNNER)
M5036 = M5040.M5036
M5034 = M5036.M5035.M5034
N5030 = M5036.N5030


def complex_row(value: complex) -> dict[str, float]:
    return {"real": float(value.real), "imaginary": float(value.imag)}


def unstable_rows(kernel: dict[str, Any]) -> list[tuple[int, dict[str, Any]]]:
    return [
        (int(chamber["chamber_index"]), row)
        for chamber in kernel["fixed_event_integral_gate"]["chambers"]
        for row in chamber["residue_catalog"]
        if not row["stable"]
    ]


def crossing_weight(config: dict[str, Any], base_argument_id: str) -> float:
    weights = []
    for crossing in config["crossings"]:
        if crossing["s_argument_id"] == base_argument_id:
            weights.append(1.0)
        if crossing["t_argument_id"] == base_argument_id:
            weights.append(abs(float(crossing["t_ratio"])) ** 3)
        if crossing["u_argument_id"] == base_argument_id:
            weights.append(abs(float(crossing["u_ratio"])) ** 3)
    if not weights:
        raise RuntimeError(f"argument {base_argument_id} has no cyclic weight")
    return max(weights)


def probe_job(
    config: dict[str, Any], job: dict[str, Any], kernel: dict[str, Any]
) -> dict[str, Any]:
    rows = unstable_rows(kernel)
    if len(rows) != 1:
        raise RuntimeError(f"{job['job_key']} has {len(rows)} unstable rows")
    chamber_index, unstable = rows[0]
    target = complex(
        float(kernel["argument"]["target_cosine"]["real"]),
        float(kernel["argument"]["target_cosine"]["imaginary"]),
    )
    M5034.configure(kernel["event"], target)
    ownership = N5030.physical_chambers()[1][chamber_index]
    root = complex(unstable["root"])
    pairs = [tuple(pair) for pair in unstable["pairs"]]
    safe_scale = float(unstable["outer_radius"]) / float(
        unstable["residue_contour_fraction"]
    )
    probes = []
    for fraction in FRACTIONS:
        radius = fraction * safe_scale
        values = {}
        for nodes in NODE_FLOORS:
            value = N5030.pair_local_relative_residue(
                root,
                radius,
                nodes,
                pairs,
                ownership,
                nodes,
            )
            values[nodes] = value
        probes.append(
            {
                "fraction": fraction,
                "radius": radius,
                "floor64": complex_row(values[64]),
                "floor96": complex_row(values[96]),
                "floor64_magnitude": abs(values[64]),
                "floor96_magnitude": abs(values[96]),
                "cross_floor_difference": abs(values[96] - values[64]),
            }
        )
    maximum_floor_magnitude = max(
        max(row["floor64_magnitude"], row["floor96_magnitude"])
        for row in probes
    )
    maximum_cross_floor_difference = max(
        row["cross_floor_difference"] for row in probes
    )
    zero_candidate = maximum_floor_magnitude < ZERO_THRESHOLD
    normalized_factor = abs(
        complex(
            float(job["normalized_direct_D_hhh_over_G3"]["real"]),
            float(job["normalized_direct_D_hhh_over_G3"]["imaginary"]),
        )
        / complex(
            float(job["raw_fixed_event_kernel"]["real"]),
            float(job["raw_fixed_event_kernel"]["imaginary"]),
        )
    )
    weight = crossing_weight(config, str(job["base_argument_id"]))
    probe_envelope = max(maximum_floor_magnitude, maximum_cross_floor_difference)
    return {
        "job_key": job["job_key"],
        "epsilon_id": job["epsilon_id"],
        "base_argument_id": job["base_argument_id"],
        "collision_pairs": [list(pair) for pair in pairs],
        "root": complex_row(root),
        "required_for_homotopy": bool(unstable["required_for_homotopy"]),
        "near_path": bool(unstable["near_path"]),
        "original_residue_magnitude": abs(complex(unstable["residue"])),
        "maximum_high_node_floor_magnitude": maximum_floor_magnitude,
        "maximum_high_node_cross_floor_difference": maximum_cross_floor_difference,
        "high_node_zero_candidate": zero_candidate,
        "cyclic_weight_magnitude": weight,
        "raw_to_normalized_magnitude": normalized_factor,
        "empirical_maximum_cyclic_impact": probe_envelope
        * weight
        * normalized_factor,
        "classification": (
            "HIGH_NODE_ZERO_CANDIDATE_NOT_PROMOTED"
            if zero_candidate
            else "ANALYTIC_OR_ARBITRARY_PRECISION_RESIDUE_REQUIRED"
        ),
        "probes": probes,
        "valid_for_production_claim": False,
        "valid_for_full_MTS_claim": False,
    }


def main() -> None:
    config = json.loads((RUN / "config.json").read_text(encoding="utf-8"))
    status = json.loads((RUN / "status.json").read_text(encoding="utf-8"))
    candidates = []
    for path in sorted((RUN / "jobs").glob("*.json")):
        job = json.loads(path.read_text(encoding="utf-8"))
        if job.get("status") != "COMPLETED_UNCONVERGED":
            continue
        kernel = json.loads((RUN / "kernels" / path.name).read_text(encoding="utf-8"))
        candidates.append(probe_job(config, job, kernel))
    if len(candidates) != 8:
        raise RuntimeError(f"expected eight current candidates, found {len(candidates)}")
    output = {
        "checkpoint_marker": MARKER,
        "run_state": status["state"],
        "candidate_count": len(candidates),
        "zero_candidate_count": sum(row["high_node_zero_candidate"] for row in candidates),
        "analytic_residue_required_count": sum(
            not row["high_node_zero_candidate"] for row in candidates
        ),
        "common_cross_source_pair": sorted(
            {
                tuple(sorted(pair))
                for row in candidates
                for pair in row["collision_pairs"]
            }
        ),
        "maximum_empirical_cyclic_impact": max(
            row["empirical_maximum_cyclic_impact"] for row in candidates
        ),
        "interpretation": (
            "The obstruction is one required direct-g1/subtraction-decay collision per row. "
            "Two A13 rows are high-node zero candidates; A00/A14 require an analytic or "
            "arbitrary-precision iterated residue. No row is promoted from this diagnostic."
        ),
        "rows": candidates,
        "production_precision_complete": False,
        "valid_for_full_MTS_claim": False,
    }
    M5036.atomic_json(OUTPUT, output)
    csv_rows = [
        {
            key: row[key]
            for key in (
                "job_key",
                "epsilon_id",
                "base_argument_id",
                "original_residue_magnitude",
                "maximum_high_node_floor_magnitude",
                "maximum_high_node_cross_floor_difference",
                "high_node_zero_candidate",
                "cyclic_weight_magnitude",
                "raw_to_normalized_magnitude",
                "empirical_maximum_cyclic_impact",
                "classification",
                "valid_for_production_claim",
                "valid_for_full_MTS_claim",
            )
        }
        for row in candidates
    ]
    with OUTPUT_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(csv_rows[0]))
        writer.writeheader()
        writer.writerows(csv_rows)
    print(
        json.dumps(
            {
                "marker": MARKER,
                "candidates": len(candidates),
                "zero_candidates": output["zero_candidate_count"],
                "analytic_required": output["analytic_residue_required_count"],
                "maximum_empirical_cyclic_impact": output[
                    "maximum_empirical_cyclic_impact"
                ],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
