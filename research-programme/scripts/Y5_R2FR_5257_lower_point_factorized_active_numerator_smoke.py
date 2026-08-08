from __future__ import annotations

import argparse
import cmath
import csv
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
from typing import Any

import numpy as np


WORKBENCH = Path(__file__).resolve().parents[1]
SCRIPTS = WORKBENCH / "scripts"
FUNCTIONAL_RG = WORKBENCH / "source-intake" / "functional_rg"
SOURCE_5256 = FUNCTIONAL_RG / "5256"
SOURCE = FUNCTIONAL_RG / "5257"

SCRIPT_5023 = (
    SCRIPTS / "Y5_R2FR_5023_causal_covariant_KLT_endpoint_gate.py"
)
SCRIPT_5026 = (
    SCRIPTS / "Y5_R2FR_5026_finite_x_global_pole_transport_smoke.py"
)
SCRIPT_5028 = (
    SCRIPTS / "Y5_R2FR_5028_finite_x_relative_chamber_transport_event.py"
)
SCRIPT_5256 = (
    SCRIPTS
    / "Y5_R2FR_5256_outer_topology_bisection_generation2_and_half_residue_bound.py"
)

DENOMINATOR_ROWS = SOURCE_5256 / "exact_active_denominator_crosscheck.csv"
NODE_ROOT = SOURCE_5256 / "nodes"
ROWS = SOURCE / "factorized_active_numerator_smoke.csv"
VALIDATION = SOURCE / "factorized_active_numerator_validation.csv"
RESULT = SOURCE / "factorized_active_numerator_result.json"

S_VALUE = 4.0
SUPPORTED_COMPONENTS = {
    "MC12": {
        "hard_index": 2,
        "family": "direct:g2:minus/direct:g3:plus",
        "surface_id": "direct:L:s02",
    },
    "MC04": {
        "hard_index": 1,
        "family": "direct:g1:minus/direct:g3:plus",
        "surface_id": "direct:L:s01",
    },
}


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5023 = load_module("mts_5023_for_5257", SCRIPT_5023)
M5026 = load_module("mts_5026_for_5257", SCRIPT_5026)
M5028 = load_module("mts_5028_for_5257", SCRIPT_5028)
M5256 = load_module("mts_5256_for_5257", SCRIPT_5256)
M5017 = M5023.M5017
M5024 = M5028.M5024


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def sha256(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def atomic_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(text, encoding="utf-8")
    os.replace(temporary, path)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise RuntimeError(f"refusing to write empty CSV: {path}")
    fields: list[str] = []
    for row in rows:
        for field in row:
            if field not in fields:
                fields.append(field)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    os.replace(temporary, path)


def complex_from_row(row: dict[str, str], prefix: str) -> complex:
    return complex(
        float(row[f"{prefix}_real"]),
        float(row[f"{prefix}_imaginary"]),
    )


def complex_fields(prefix: str, value: complex) -> dict[str, float]:
    return {
        f"{prefix}_real": float(value.real),
        f"{prefix}_imaginary": float(value.imag),
        f"{prefix}_magnitude": float(abs(value)),
    }


def helicity(index: int, special: int, chirality: int) -> int:
    if chirality == 0:
        return -1 if index == special else 1
    return 1 if index == special else -1


def scalar_klt_four_with_helicities(
    momenta: np.ndarray,
    helicities: dict[int, int],
) -> complex:
    polarizations = {
        index: M5023.polarization(
            momenta[index],
            momenta[0],
            helicities[index],
        )
        for index in (1, 2)
    }
    left = M5023.gauge_four_ordered(
        [0, 1, 2, 4],
        momenta,
        polarizations,
        0.0,
    )
    right = M5023.gauge_four_ordered(
        [2, 4, 1, 0],
        momenta,
        polarizations,
        0.0,
    )
    kernel = complex(M5017.invariant(momenta, 0, 1))
    return complex(-left * kernel * right)


def factorized_left_klt_residue(
    left: np.ndarray,
    hard_index: int,
    special: int,
    chirality: int,
) -> complex:
    hard_polarization = M5023.polarization(
        left[hard_index],
        left[4],
        helicity(hard_index, special, chirality),
    )
    gravity_three = 2.0 * M5023.minkowski(
        hard_polarization,
        left[0],
    ) ** 2

    remaining = [
        index for index in (1, 2, 3) if index != hard_index
    ]
    reduced = np.zeros((5, 4), dtype=np.complex128)
    reduced[0] = left[0] + left[hard_index]
    reduced[1] = left[remaining[0]]
    reduced[2] = left[remaining[1]]
    reduced[4] = left[4]
    reduced_helicities = {
        reduced_index: helicity(
            original_index,
            special,
            chirality,
        )
        for reduced_index, original_index in (
            (1, remaining[0]),
            (2, remaining[1]),
        )
    }
    gravity_four = scalar_klt_four_with_helicities(
        reduced,
        reduced_helicities,
    )
    return complex(gravity_three * gravity_four)


def factorized_d_hhh(
    internal: np.ndarray,
    target: complex,
    hard_index: int,
) -> complex:
    left, right = M5017.cut_momenta(internal, target, 1.0)
    result = 0.0j
    for special in (1, 2, 3):
        for chirality in (0, 1):
            left_residue = factorized_left_klt_residue(
                left,
                hard_index,
                special,
                chirality,
            )
            right_value = M5023.causal_scalar_klt_five(
                right,
                special,
                1 - chirality,
                0.0,
            )
            result += left_residue * right_value
    return complex(result / 6.0)


def exact_branch(row: dict[str, str]) -> dict[str, complex | float]:
    component_id = row["component_id"]
    x = float(row["decay_cosine"])
    e = float(row["soft_energy"])
    z = complex_from_row(row, "exact_pole")
    kappa = complex_from_row(row, "kappa")
    recoil_root = math.sqrt(1.0 - e)
    gamma = (2.0 - e) / (2.0 * recoil_root)
    gamma_beta = e / (2.0 * recoil_root)
    h = gamma - 1.0
    denominator = h * z + gamma_beta
    if component_id == "MC12":
        relative_cosine = -(
            gamma + x + gamma_beta * z
        ) / denominator
        q0 = (
            gamma
            - x
            - gamma_beta * z
            - kappa * gamma_beta * (1.0 + z)
        )
        hard_sign = -1.0
    elif component_id == "MC04":
        relative_cosine = (
            gamma + gamma_beta * z - x
        ) / denominator
        q0 = (
            -gamma
            - x
            + gamma_beta * z
            + kappa * gamma_beta * (1.0 + z)
        )
        hard_sign = 1.0
    else:
        raise RuntimeError(f"unsupported component: {component_id}")
    q1 = (
        gamma_beta
        - h * z
        - kappa * h * (1.0 + z)
    )
    linear = q0 + q1 * relative_cosine
    soft_transverse = cmath.sqrt(1.0 - z * z)
    decay_transverse = math.sqrt(1.0 - x * x)
    relative_root = (
        soft_transverse
        * linear
        / (kappa * (1.0 + z) * decay_transverse)
    )
    global_root = (
        cmath.sqrt(kappa)
        * (1.0 + z)
        / soft_transverse
    )

    relative_derivative = (
        soft_transverse
        * decay_transverse
        * (1.0 - relative_root ** -2)
        / 2.0
    )
    energy_plus_pz = recoil_root * (
        gamma
        + hard_sign * x
        - gamma_beta * z
        + hard_sign
        * (h * z - gamma_beta)
        * relative_cosine
    )
    p_plus = recoil_root * (
        hard_sign * decay_transverse * relative_root
        + hard_sign
        * h
        * soft_transverse
        * relative_cosine
        - gamma_beta * soft_transverse
    )
    energy_plus_pz_derivative = (
        recoil_root
        * hard_sign
        * (h * z - gamma_beta)
        * relative_derivative
    )
    p_plus_derivative = (
        recoil_root
        * hard_sign
        * (
            decay_transverse
            + h * soft_transverse * relative_derivative
        )
    )
    square_root_kappa = cmath.sqrt(kappa)
    collision_jacobian = -(
        energy_plus_pz_derivative * p_plus
        - energy_plus_pz * p_plus_derivative
    ) / (square_root_kappa * p_plus * p_plus)
    hard_global_root = -energy_plus_pz / (
        square_root_kappa * p_plus
    )
    return {
        "decay_cosine": x,
        "soft_energy": e,
        "soft_cosine": z,
        "relative_cosine": relative_cosine,
        "relative_root": relative_root,
        "global_root": global_root,
        "hard_global_root": hard_global_root,
        "collision_jacobian": collision_jacobian,
    }


def winding_difference(row: dict[str, str]) -> int:
    topology_path = (
        Path(row["fit_source_path"]).parent
        / "corrected_pole_topology.csv"
    )
    candidates = [
        item
        for item in read_csv(topology_path)
        if item["component_id"] == row["component_id"]
        and item["epsilon_id"] == row["epsilon_id"]
        and item["causal_family_active"].lower() == "true"
    ]
    by_suffix = {
        item["suffix"]: int(item["winding_sum"])
        for item in candidates
    }
    if set(by_suffix) != {"u", "v"}:
        raise RuntimeError(
            f"incomplete active winding pair for {row['node_id']} "
            f"{row['epsilon_id']}: {by_suffix}"
        )
    return by_suffix["u"] - by_suffix["v"]


def orientation_key(row: dict[str, str]) -> tuple[str, str, str]:
    return row["node_id"], row["job_id"], row["epsilon_id"]


def parent_orientation_lookup(
    source_rows: list[dict[str, str]],
) -> dict[tuple[str, str, str], dict[str, Any]]:
    engines = {
        "5255": M5256.M5255,
        "5256": M5256,
    }
    problems_by_node: dict[
        tuple[str, str],
        dict[str, dict[str, Any]],
    ] = {}
    for checkpoint in sorted(
        {row["source_checkpoint"] for row in source_rows}
    ):
        engine = engines[checkpoint]
        engine.configure_node_engine()
        batch_manifest = json.loads(
            Path(engine.MANIFEST).read_text(encoding="utf-8")
        )
        for node_id in sorted(
            {
                row["node_id"]
                for row in source_rows
                if row["source_checkpoint"] == checkpoint
            }
        ):
            _, _, _, problems = engine.M5251.build_node_problem(
                batch_manifest,
                node_id,
            )
            problems_by_node[(checkpoint, node_id)] = {
                problem["job"]["job_id"]: problem
                for problem in problems
            }

    fit_rows_by_path: dict[Path, list[dict[str, str]]] = {}
    lookup: dict[tuple[str, str, str], dict[str, Any]] = {}
    for row in source_rows:
        fit_path = Path(row["fit_source_path"])
        if fit_path not in fit_rows_by_path:
            fit_rows_by_path[fit_path] = read_csv(fit_path)
        fit = next(
            candidate
            for candidate in fit_rows_by_path[fit_path]
            if candidate["job_id"] == row["job_id"]
            and candidate["epsilon_id"] == row["epsilon_id"]
            and candidate["component_id"] == row["component_id"]
        )
        problem = problems_by_node[
            (row["source_checkpoint"], row["node_id"])
        ][row["job_id"]]
        center = float(fit["center"])
        topology = (
            M5256.M5251.M5239.M5237.updated_component_topology(
                problem,
                center,
            )
        )
        event = dict(problem["event"])
        event[problem["case"]["outer_coordinate"]] = center
        expected_root = complex(exact_branch(row)["relative_root"])
        candidates: list[dict[str, Any]] = []
        for first, second, _ in M5256.M5231.reciprocal_pairs(
            topology
        ):
            family = M5256.M5231.canonical_family(first, second)
            if family != row["family"]:
                continue
            representative, partner = (
                (first, second)
                if abs(
                    M5256.M5231.complex_value(first["target_root"])
                )
                >= 1.0
                else (second, first)
            )
            representative_root = M5256.M5231.complex_value(
                representative["target_root"]
            )
            chamber = topology["chambers"][
                int(representative["chamber_index"])
            ]
            ownership = M5256.M5231.chamber_ownership(event, chamber)
            labels = list(representative["representing_pairs"][0])
            owned = [bool(ownership[label]) for label in labels]
            candidates.append(
                {
                    "orientation": 1 if owned[0] else -1,
                    "labels": labels,
                    "owned": owned,
                    "owned_label": labels[owned.index(True)]
                    if sum(owned) == 1
                    else "",
                    "ownership_unique": sum(owned) == 1,
                    "representative_root": representative_root,
                    "representative_root_relative_residual": (
                        abs(representative_root - expected_root)
                        / max(abs(expected_root), 1.0)
                    ),
                    "partner_root": M5256.M5231.complex_value(
                        partner["target_root"]
                    ),
                    "chamber_index": int(
                        representative["chamber_index"]
                    ),
                }
            )
        if not candidates:
            raise RuntimeError(
                "parent topology has no matching active family for "
                f"{orientation_key(row)}"
            )
        selected = min(
            candidates,
            key=lambda candidate: candidate[
                "representative_root_relative_residual"
            ],
        )
        selected.update(
            {
                "center": center,
                "node_manifest_path": str(
                    fit_path.parent / "node_manifest.json"
                ),
                "fit_source_path": str(fit_path),
                "parent_script_path": str(SCRIPT_5256),
            }
        )
        lookup[orientation_key(row)] = selected
    return lookup


def coefficient_radius(
    internal: np.ndarray,
    soft_direction: np.ndarray,
    decay_direction: np.ndarray,
    target: complex,
    global_root: complex,
) -> float:
    directions = [
        *(M5026.internal_direction(momentum) for momentum in internal),
        soft_direction,
        decay_direction,
    ]
    roots = [
        complex(root)
        for direction in directions
        for root in M5024.all_factor_roots(direction, target).values()
    ]
    active_residual = min(abs(root - global_root) for root in roots)
    if active_residual > 1.0e-7 * max(1.0, abs(global_root)):
        raise RuntimeError(
            f"factorized global root mismatch: {active_residual}"
        )
    coincidence_tolerance = 5.0e-10 * max(1.0, abs(global_root))
    separations = [
        abs(root - global_root)
        for root in roots
        if abs(root - global_root) > coincidence_tolerance
    ]
    if not separations:
        raise RuntimeError("global coefficient circle has no distinct roots")
    safe_scale = min([abs(global_root), *separations])
    if safe_scale <= 0.0:
        raise RuntimeError("global coefficient circle has zero safe scale")
    return 0.02 * safe_scale


def cauchy_coefficient(
    internal: np.ndarray,
    soft_energy: float,
    target: complex,
    hard_index: int,
    global_root: complex,
    radius: float,
    nodes: int,
) -> complex:
    total = 0.0j
    for index in range(nodes):
        phase = cmath.exp(
            2.0j * math.pi * (index + 0.317) / nodes
        )
        displacement = radius * phase
        rotated = M5024.rotate_internal(
            internal,
            global_root + displacement,
        )
        inverse_energy_square_sum = sum(
            1.0 / (momentum[0] * momentum[0])
            for momentum in rotated
        )
        multiplier = (
            3.0
            / (rotated[2, 0] * rotated[2, 0])
            / inverse_energy_square_sum
        )
        d_times_direct = (
            soft_energy
            * multiplier
            * factorized_d_hhh(
                rotated,
                target,
                hard_index,
            )
            / (S_VALUE * S_VALUE)
        )
        total += displacement * displacement * d_times_direct
    return complex(total / nodes)


def evaluate_row(
    row: dict[str, str],
    nodes: int,
    orientation: dict[str, Any],
) -> dict[str, Any]:
    branch = exact_branch(row)
    x = float(branch["decay_cosine"])
    e = float(branch["soft_energy"])
    z = complex(branch["soft_cosine"])
    relative_root = complex(branch["relative_root"])
    global_root = complex(branch["global_root"])
    target = complex(-9.0, float(row["epsilon"]))
    soft_direction, decay_direction, internal = M5028.event_geometry(
        e,
        z,
        complex(x),
        relative_root,
    )
    radius = coefficient_radius(
        internal,
        soft_direction,
        decay_direction,
        target,
        global_root,
    )
    coefficient_large = cauchy_coefficient(
        internal,
        e,
        target,
        SUPPORTED_COMPONENTS[row["component_id"]]["hard_index"],
        global_root,
        radius,
        nodes,
    )
    coefficient_small = cauchy_coefficient(
        internal,
        e,
        target,
        SUPPORTED_COMPONENTS[row["component_id"]]["hard_index"],
        global_root,
        radius / 2.0,
        nodes,
    )
    coefficient_stability = abs(
        coefficient_small - coefficient_large
    ) / max(abs(coefficient_small), 1.0)
    winding = winding_difference(row)
    candidate = (
        int(orientation["orientation"])
        * winding
        * coefficient_small
        / (
            relative_root
            * global_root
            * complex(branch["collision_jacobian"])
        )
    )
    fitted = complex_from_row(row, "fitted_numerator")
    direct_error = abs(candidate - fitted) / max(abs(fitted), 1.0)
    sign_flipped_error = abs(candidate + fitted) / max(
        abs(fitted), 1.0
    )
    best_signed_error = min(direct_error, sign_flipped_error)
    row_passed = (
        abs(relative_root) > 1.0
        and abs(
            complex(branch["hard_global_root"]) - global_root
        )
        <= 1.0e-7 * max(1.0, abs(global_root))
        and abs(branch["collision_jacobian"]) >= 1.0e-6
        and bool(orientation["ownership_unique"])
        and float(
            orientation["representative_root_relative_residual"]
        )
        <= 5.0e-3
        and coefficient_stability <= 2.0e-4
        and direct_error <= 2.0e-3
    )
    return {
        "node_id": row["node_id"],
        "component_id": row["component_id"],
        "family": row["family"],
        "surface_id": row["surface_id"],
        "epsilon_id": row["epsilon_id"],
        "epsilon": row["epsilon"],
        "decay_cosine": x,
        "soft_energy": e,
        **complex_fields("exact_pole", z),
        **complex_fields("relative_root", relative_root),
        **complex_fields("global_root", global_root),
        "global_collision_residual": abs(
            complex(branch["hard_global_root"]) - global_root
        ),
        **complex_fields(
            "collision_jacobian",
            complex(branch["collision_jacobian"]),
        ),
        "winding_difference": winding,
        "local_residue_orientation": int(orientation["orientation"]),
        "orientation_labels": "|".join(orientation["labels"]),
        "orientation_owned_label": orientation["owned_label"],
        "orientation_ownership_unique": bool(
            orientation["ownership_unique"]
        ),
        "orientation_representative_root_relative_residual": float(
            orientation["representative_root_relative_residual"]
        ),
        "orientation_chamber_index": int(
            orientation["chamber_index"]
        ),
        "orientation_proof_status": (
            "PARENT_CHAMBER_OWNERSHIP_DERIVED"
        ),
        "orientation_node_manifest_path": orientation[
            "node_manifest_path"
        ],
        "orientation_fit_source_path": orientation["fit_source_path"],
        "orientation_parent_script_path": orientation[
            "parent_script_path"
        ],
        "cauchy_nodes": nodes,
        "large_radius": radius,
        "small_radius": radius / 2.0,
        **complex_fields(
            "large_radius_coefficient",
            coefficient_large,
        ),
        **complex_fields(
            "small_radius_coefficient",
            coefficient_small,
        ),
        "coefficient_radius_stability": coefficient_stability,
        **complex_fields("factorized_numerator_candidate", candidate),
        **complex_fields("fitted_numerator", fitted),
        "direct_sign_relative_error": direct_error,
        "flipped_sign_relative_error": sign_flipped_error,
        "best_signed_relative_error": best_signed_error,
        "factorized_numerator_smoke_passed": row_passed,
        "orientation_sign_resolved": (
            bool(orientation["ownership_unique"])
            and direct_error <= 2.0e-3
        ),
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }


def execute(
    nodes: int,
    selected_nodes: set[str] | None,
    dry_run: bool,
) -> dict[str, Any]:
    if not DENOMINATOR_ROWS.exists():
        raise RuntimeError(
            f"run the 5256 denominator cross-check first: {DENOMINATOR_ROWS}"
        )
    source_rows = read_csv(DENOMINATOR_ROWS)
    if selected_nodes is not None:
        source_rows = [
            row for row in source_rows if row["node_id"] in selected_nodes
        ]
    if not source_rows:
        raise RuntimeError("no selected denominator rows")
    orientations = parent_orientation_lookup(source_rows)
    rows = [
        evaluate_row(row, nodes, orientations[orientation_key(row)])
        for row in source_rows
    ]
    checks = [
        {
            "check_id": "ALL_SELECTED_ROWS_EVALUATED",
            "passed": len(rows) == len(source_rows),
            "detail": f"rows={len(rows)}",
        },
        {
            "check_id": "ALL_FACTORIZED_NUMERATOR_SMOKES_PASS",
            "passed": all(
                bool(row["factorized_numerator_smoke_passed"])
                for row in rows
            ),
            "detail": (
                "finite lower-point factorization matches the fitted "
                "numerator with the parent-derived local orientation"
            ),
        },
        {
            "check_id": "ALL_PARENT_ORIENTATION_SIGNS_DERIVED",
            "passed": all(
                bool(row["orientation_ownership_unique"])
                and bool(row["orientation_sign_resolved"])
                and row["orientation_proof_status"]
                == "PARENT_CHAMBER_OWNERSHIP_DERIVED"
                for row in rows
            ),
            "detail": (
                "one owned member per representative collision pair"
            ),
        },
        {
            "check_id": "CLAIM_FLAGS_REMAIN_FALSE",
            "passed": all(
                not bool(row["valid_for_numeric_UV_claim"])
                and not bool(row["valid_for_local_GR_claim"])
                and not bool(row["valid_for_full_MTS_claim"])
                for row in rows
            ),
            "detail": "smoke calculation is not an interval enclosure",
        },
    ]
    passed = all(bool(row["passed"]) for row in checks)
    result = {
        "marker": "MTS_5257_LOWER_POINT_FACTORIZED_ACTIVE_NUMERATOR_SMOKE",
        "revision": "lower-point-factorized-active-numerator-v2",
        "row_count": len(rows),
        "cauchy_nodes": nodes,
        "validation_passed": passed,
        "maximum_coefficient_radius_stability": max(
            row["coefficient_radius_stability"] for row in rows
        ),
        "maximum_best_signed_relative_error": max(
            row["best_signed_relative_error"] for row in rows
        ),
        "maximum_oriented_relative_error": max(
            row["direct_sign_relative_error"] for row in rows
        ),
        "lower_point_factorization_numerically_supported": passed,
        "orientation_sign_fully_derived": all(
            bool(row["orientation_sign_resolved"]) for row in rows
        ),
        "outward_rounded_numerator_enclosure_complete": False,
        "continuous_residue_envelope_complete": False,
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    if not dry_run:
        write_csv(ROWS, rows)
        write_csv(VALIDATION, checks)
        atomic_text(
            RESULT,
            json.dumps(result, indent=2, sort_keys=True) + "\n",
        )
    if not passed:
        failed = [
            row["check_id"] for row in checks if not row["passed"]
        ]
        raise RuntimeError(
            f"5257 factorized numerator smoke failed: {failed}"
        )
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--nodes", type=int, default=32)
    parser.add_argument("--node-id", action="append")
    parser.add_argument("--dry-run", action="store_true")
    arguments = parser.parse_args()
    selected = set(arguments.node_id) if arguments.node_id else None
    print(
        json.dumps(
            execute(arguments.nodes, selected, arguments.dry_run),
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
