from __future__ import annotations

import argparse
import cmath
import csv
import hashlib
import json
import os
from pathlib import Path
from typing import Any


WORKBENCH = Path(__file__).resolve().parents[1]
FUNCTIONAL_RG = WORKBENCH / "source-intake" / "functional_rg"
SOURCE = FUNCTIONAL_RG / "5256"
NODE_ROOT = SOURCE / "nodes"
NODE_ROOT_5255 = FUNCTIONAL_RG / "5255" / "nodes"
TOPOLOGY_ROOT_5224 = (
    FUNCTIONAL_RG
    / "5224"
    / "runs"
    / "replacement_scaled_controlled_v1"
    / "topologies"
)

ACTIVE_NODE_PATHS = {
    "D01A": NODE_ROOT / "D01A",
    "D01B": NODE_ROOT / "D01B",
    "C06A": NODE_ROOT_5255 / "C06A",
    "D06B": NODE_ROOT / "D06B",
}
INACTIVE_NODE_PATHS = {"D06A": NODE_ROOT / "D06A"}
NODE_IDS = (*ACTIVE_NODE_PATHS, *INACTIVE_NODE_PATHS)
ACTIVE_NODE_IDS = tuple(ACTIVE_NODE_PATHS)
INACTIVE_NODE_IDS = tuple(INACTIVE_NODE_PATHS)
REFLECTION_PAIRS = (("D01A", "D06B"),)
SUPPORTED_COMPONENTS = {
    "MC12": {
        "family": "direct:g2:minus/direct:g3:plus",
        "surface_id": "direct:L:s02",
    },
    "MC04": {
        "family": "direct:g1:minus/direct:g3:plus",
        "surface_id": "direct:L:s01",
    },
}

ROWS = SOURCE / "exact_active_denominator_crosscheck.csv"
VALIDATION = SOURCE / "exact_active_denominator_validation.csv"
RESULT = SOURCE / "exact_active_denominator_result.json"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


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


def complex_fields(prefix: str, value: complex) -> dict[str, float]:
    return {
        f"{prefix}_real": float(value.real),
        f"{prefix}_imaginary": float(value.imag),
        f"{prefix}_magnitude": float(abs(value)),
    }


def epsilon_value(epsilon_id: str) -> float:
    if not epsilon_id.startswith("E"):
        raise RuntimeError(f"unsupported epsilon id: {epsilon_id}")
    return int(epsilon_id[1:]) / 1000.0


def topology_path(seed: int, epsilon_id: str) -> Path:
    return (
        TOPOLOGY_ROOT_5224
        / f"S{seed}_N0000__{epsilon_id}_A00.json"
    )


def quadratic_coefficients(
    component_id: str,
    decay_cosine: float,
    gamma: float,
    gamma_beta: float,
    h: float,
    kappa: complex,
) -> tuple[complex, complex, complex]:
    x = decay_cosine
    coefficient_2 = h * (1.0 + kappa)
    if component_id == "MC12":
        coefficient_1 = -(
            h
            - gamma_beta * x
            - kappa * gamma_beta * (1.0 + x)
        )
        coefficient_0 = (
            -gamma_beta * x + kappa * (1.0 + gamma * x)
        )
    elif component_id == "MC04":
        coefficient_1 = -(
            h
            + gamma_beta * x
            - kappa * gamma_beta * (1.0 - x)
        )
        coefficient_0 = (
            gamma_beta * x + kappa * (1.0 - gamma * x)
        )
    else:
        raise RuntimeError(f"unsupported component: {component_id}")
    return coefficient_2, coefficient_1, coefficient_0


def quadratic_roots(
    coefficient_2: complex,
    coefficient_1: complex,
    coefficient_0: complex,
) -> tuple[complex, complex, complex]:
    discriminant = (
        coefficient_1 * coefficient_1
        - 4.0 * coefficient_2 * coefficient_0
    )
    root = cmath.sqrt(discriminant)
    return (
        (-coefficient_1 + root) / (2.0 * coefficient_2),
        (-coefficient_1 - root) / (2.0 * coefficient_2),
        discriminant,
    )


def collision_and_derivative(
    component_id: str,
    decay_cosine: float,
    pole: complex,
    recoil_root: float,
    gamma: float,
    gamma_beta: float,
    h: float,
    kappa: complex,
) -> dict[str, complex]:
    x = decay_cosine
    z = pole
    denominator = h * z + gamma_beta
    q1 = (
        gamma_beta
        - h * z
        - kappa * h * (1.0 + z)
    )

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
        partial_l_z = -(
            1.0 + kappa
        ) * (gamma_beta + h * relative_cosine)
        derivative_sign = -1.0
        derivative_offset = gamma_beta + h * relative_cosine
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
        partial_l_z = (
            1.0 + kappa
        ) * (gamma_beta - h * relative_cosine)
        derivative_sign = 1.0
        derivative_offset = -gamma_beta + h * relative_cosine
    else:
        raise RuntimeError(f"unsupported component: {component_id}")

    linear = q0 + q1 * relative_cosine
    collision = (
        (1.0 - z) * linear * linear
        - 2.0
        * kappa
        * (relative_cosine - z * x)
        * linear
        + (1.0 - x * x)
        * kappa
        * kappa
        * (1.0 + z)
    )
    partial_c = (
        2.0 * (1.0 - z) * linear * q1
        - 2.0
        * kappa
        * (
            linear
            + (relative_cosine - z * x) * q1
        )
    )
    partial_z = (
        -linear * linear
        + 2.0 * (1.0 - z) * linear * partial_l_z
        + 2.0 * kappa * x * linear
        - 2.0
        * kappa
        * (relative_cosine - z * x)
        * partial_l_z
        + (1.0 - x * x) * kappa * kappa
    )
    relative_cosine_derivative = -partial_z / partial_c
    channel_derivative = (
        derivative_sign
        * 2.0
        * recoil_root
        * (
            derivative_offset
            + denominator * relative_cosine_derivative
        )
    )
    return {
        "relative_cosine": relative_cosine,
        "collision": collision,
        "collision_partial_c": partial_c,
        "relative_cosine_derivative": relative_cosine_derivative,
        "channel_derivative": channel_derivative,
        "channel_denominator_factor": denominator,
    }


def active_rows(node_id: str) -> list[dict[str, Any]]:
    node = (
        ACTIVE_NODE_PATHS[node_id]
        if node_id in ACTIVE_NODE_PATHS
        else INACTIVE_NODE_PATHS[node_id]
    )
    fits_path = node / "corrected_residue_fits.csv"
    poles_path = node / "corrected_pole_catalog.csv"
    result_path = node / "node_result.json"
    for required in (fits_path, poles_path, result_path):
        if not required.exists():
            raise RuntimeError(f"missing completed-node source: {required}")

    pole_lookup = {
        (
            row["job_id"],
            row["pole_id"],
            row["epsilon_id"],
        ): row
        for row in read_csv(poles_path)
    }
    rows: list[dict[str, Any]] = []
    for fit in read_csv(fits_path):
        component_id = fit["component_id"]
        if component_id not in SUPPORTED_COMPONENTS:
            continue
        expected = SUPPORTED_COMPONENTS[component_id]
        if (
            fit["family"] != expected["family"]
            or fit["surface_id"] != expected["surface_id"]
        ):
            continue
        pole_source = pole_lookup[
            (fit["job_id"], fit["pole_id"], fit["epsilon_id"])
        ]
        if pole_source["causal_family_active"].lower() != "true":
            continue
        seed = int(pole_source["seed"])
        if pole_source["tranche"] != "old_5224":
            raise RuntimeError(
                "5256 exact denominator cross-check currently expects "
                f"old_5224, found {pole_source['tranche']}"
            )
        event_path = topology_path(seed, fit["epsilon_id"])
        event = read_json(event_path)
        soft_energy = float(event["soft_energy"])
        recoil_root = (1.0 - soft_energy) ** 0.5
        gamma = (2.0 - soft_energy) / (2.0 * recoil_root)
        gamma_beta = soft_energy / (2.0 * recoil_root)
        h = gamma - 1.0
        epsilon = epsilon_value(fit["epsilon_id"])
        target = complex(-9.0, epsilon)
        kappa = (1.0 - target) / (1.0 + target)
        decay_cosine = float(fit["decay_cosine"])
        fitted_pole = complex(
            float(fit["pole_real"]),
            float(fit["pole_imaginary"]),
        )
        observed_derivative = complex(
            float(fit["channel_derivative_real"]),
            float(fit["channel_derivative_imaginary"]),
        )
        fitted_numerator = complex(
            float(fit["numerator_at_pole_real"]),
            float(fit["numerator_at_pole_imaginary"]),
        )
        fitted_outer_residue = complex(
            float(fit["outer_residue_real"]),
            float(fit["outer_residue_imaginary"]),
        )
        coefficients = quadratic_coefficients(
            component_id,
            decay_cosine,
            gamma,
            gamma_beta,
            h,
            kappa,
        )
        root_1, root_2, discriminant = quadratic_roots(*coefficients)
        selected_root = min(
            (root_1, root_2),
            key=lambda value: abs(value - fitted_pole),
        )
        quadratic_partial_z = (
            2.0 * coefficients[0] * selected_root
            + coefficients[1]
        )
        if component_id == "MC12":
            quadratic_partial_x = (
                gamma_beta * (1.0 + kappa) * selected_root
                - gamma_beta
                + kappa * gamma
            )
        else:
            quadratic_partial_x = (
                -gamma_beta * (1.0 + kappa) * selected_root
                + gamma_beta
                - kappa * gamma
            )
        exact_pole_derivative_x = (
            -quadratic_partial_x / quadratic_partial_z
        )
        polynomial_at_fit = (
            coefficients[0] * fitted_pole * fitted_pole
            + coefficients[1] * fitted_pole
            + coefficients[2]
        )
        exact = collision_and_derivative(
            component_id,
            decay_cosine,
            selected_root,
            recoil_root,
            gamma,
            gamma_beta,
            h,
            kappa,
        )
        derivative_error = (
            abs(exact["channel_derivative"] - observed_derivative)
            / max(abs(observed_derivative), 1.0e-300)
        )
        root_error = abs(selected_root - fitted_pole)
        row_passed = (
            abs(polynomial_at_fit) <= 1.0e-6
            and root_error <= 1.0e-4
            and abs(discriminant) >= 1.0e-8
            and abs(quadratic_partial_z) >= 1.0e-6
            and abs(exact["channel_denominator_factor"]) >= 1.0e-6
            and abs(exact["collision_partial_c"]) >= 1.0e-6
            and abs(exact["collision"]) <= 1.0e-8
            and derivative_error <= 5.0e-4
        )
        rows.append(
            {
                "node_id": node_id,
                "source_checkpoint": node.parent.parent.name,
                "job_id": fit["job_id"],
                "component_id": component_id,
                "family": fit["family"],
                "surface_id": fit["surface_id"],
                "epsilon_id": fit["epsilon_id"],
                "epsilon": epsilon,
                "seed": seed,
                "soft_energy": soft_energy,
                "decay_cosine": decay_cosine,
                **complex_fields("kappa", kappa),
                **complex_fields("fitted_pole", fitted_pole),
                **complex_fields("exact_pole", selected_root),
                "exact_to_fitted_pole_distance": root_error,
                "quadratic_root_separation": abs(root_1 - root_2),
                **complex_fields("quadratic_discriminant", discriminant),
                **complex_fields(
                    "quadratic_partial_z",
                    quadratic_partial_z,
                ),
                **complex_fields(
                    "exact_pole_derivative_x",
                    exact_pole_derivative_x,
                ),
                **complex_fields("quadratic_at_fitted_pole", polynomial_at_fit),
                **complex_fields(
                    "channel_denominator_factor",
                    exact["channel_denominator_factor"],
                ),
                **complex_fields(
                    "collision_partial_c",
                    exact["collision_partial_c"],
                ),
                **complex_fields(
                    "collision_at_exact_pole",
                    exact["collision"],
                ),
                **complex_fields(
                    "exact_channel_derivative",
                    exact["channel_derivative"],
                ),
                **complex_fields(
                    "fitted_channel_derivative",
                    observed_derivative,
                ),
                **complex_fields(
                    "fitted_numerator",
                    fitted_numerator,
                ),
                **complex_fields(
                    "fitted_outer_residue",
                    fitted_outer_residue,
                ),
                "channel_derivative_relative_error": derivative_error,
                "exact_denominator_row_passed": row_passed,
                "topology_source_path": str(event_path),
                "topology_source_sha256": sha256(event_path),
                "fit_source_path": str(fits_path),
                "fit_source_sha256": sha256(fits_path),
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )
    return rows


def validation_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    nodes = {row["node_id"] for row in rows}
    components = {row["component_id"] for row in rows}
    row_lookup = {
        (row["node_id"], row["epsilon_id"]): row for row in rows
    }
    reflection_residuals: list[float] = []
    for left_node, right_node in REFLECTION_PAIRS:
        for epsilon_id in ("E020", "E040"):
            left = row_lookup.get((left_node, epsilon_id))
            right = row_lookup.get((right_node, epsilon_id))
            if left is None or right is None:
                reflection_residuals.append(float("inf"))
                continue
            left_numerator = complex(
                left["fitted_numerator_real"],
                left["fitted_numerator_imaginary"],
            )
            right_numerator = complex(
                right["fitted_numerator_real"],
                right["fitted_numerator_imaginary"],
            )
            left_residue = complex(
                left["fitted_outer_residue_real"],
                left["fitted_outer_residue_imaginary"],
            )
            right_residue = complex(
                right["fitted_outer_residue_real"],
                right["fitted_outer_residue_imaginary"],
            )
            left_derivative = complex(
                left["fitted_channel_derivative_real"],
                left["fitted_channel_derivative_imaginary"],
            )
            right_derivative = complex(
                right["fitted_channel_derivative_real"],
                right["fitted_channel_derivative_imaginary"],
            )
            reflection_residuals.extend(
                (
                    abs(left["decay_cosine"] + right["decay_cosine"]),
                    abs(left_numerator + right_numerator)
                    / max(abs(left_numerator), abs(right_numerator), 1.0),
                    abs(left_residue + right_residue)
                    / max(abs(left_residue), abs(right_residue), 1.0),
                    abs(left_derivative - right_derivative)
                    / max(abs(left_derivative), abs(right_derivative), 1.0),
                )
            )
    checks = [
        (
            "ALL_ACTIVE_TARGET_NODES_PRESENT",
            nodes == set(ACTIVE_NODE_IDS),
            f"nodes={sorted(nodes)}",
        ),
        (
            "KNOWN_INACTIVE_NODE_EXCLUDED",
            nodes.isdisjoint(INACTIVE_NODE_IDS)
            and all(
                int(
                    read_json(
                        INACTIVE_NODE_PATHS[node] / "node_result.json"
                    )["summary"]["active_pole_count"]
                )
                == 0
                for node in INACTIVE_NODE_IDS
            ),
            f"inactive_nodes={list(INACTIVE_NODE_IDS)}",
        ),
        (
            "BOTH_ACTIVE_REFLECTION_FAMILIES_PRESENT",
            components == set(SUPPORTED_COMPONENTS),
            f"components={sorted(components)}",
        ),
        (
            "TWO_REGULATORS_PER_NODE",
            all(
                sum(row["node_id"] == node for row in rows) == 2
                for node in ACTIVE_NODE_IDS
            ),
            f"row_count={len(rows)}",
        ),
        (
            "ALL_EXACT_DENOMINATOR_ROWS_PASS",
            all(bool(row["exact_denominator_row_passed"]) for row in rows),
            "quadratic, branch, derivative, and source checks",
        ),
        (
            "ALL_SOURCE_PATHS_EXIST",
            all(
                Path(row["topology_source_path"]).exists()
                and Path(row["fit_source_path"]).exists()
                for row in rows
            ),
            "topology and fitted cross-check sources",
        ),
        (
            "HARD_LEG_REFLECTION_MATCHES",
            bool(reflection_residuals)
            and max(reflection_residuals) <= 1.0e-10,
            (
                "x_04=-x_12, N_04=-N_12, "
                "R_04=-R_12, Dprime_04=Dprime_12; "
                f"maximum_residual={max(reflection_residuals)}"
            ),
        ),
        (
            "CLAIM_FLAGS_REMAIN_FALSE",
            all(
                not bool(row["valid_for_numeric_UV_claim"])
                and not bool(row["valid_for_local_GR_claim"])
                and not bool(row["valid_for_full_MTS_claim"])
                for row in rows
            ),
            "denominator identity does not certify the numerator",
        ),
    ]
    return [
        {
            "check_id": check_id,
            "passed": passed,
            "detail": detail,
        }
        for check_id, passed, detail in checks
    ]


def execute(dry_run: bool) -> dict[str, Any]:
    rows = [
        row
        for node_id in NODE_IDS
        for row in active_rows(node_id)
    ]
    validations = validation_rows(rows)
    passed = all(bool(row["passed"]) for row in validations)
    result = {
        "marker": "MTS_5256_EXACT_ACTIVE_DENOMINATOR_CROSSCHECK",
        "revision": "exact-mc12-mc04-denominator-v1",
        "exact_denominator_identity_derived": True,
        "row_count": len(rows),
        "validation_passed": passed,
        "maximum_quadratic_fit_residual": max(
            row["quadratic_at_fitted_pole_magnitude"] for row in rows
        ),
        "maximum_exact_to_fitted_pole_distance": max(
            row["exact_to_fitted_pole_distance"] for row in rows
        ),
        "maximum_channel_derivative_relative_error": max(
            row["channel_derivative_relative_error"] for row in rows
        ),
        "minimum_quadratic_discriminant_magnitude": min(
            row["quadratic_discriminant_magnitude"] for row in rows
        ),
        "minimum_quadratic_root_separation": min(
            row["quadratic_root_separation"] for row in rows
        ),
        "minimum_quadratic_partial_z_magnitude": min(
            row["quadratic_partial_z_magnitude"] for row in rows
        ),
        "minimum_channel_denominator_factor_magnitude": min(
            row["channel_denominator_factor_magnitude"] for row in rows
        ),
        "minimum_collision_partial_c_magnitude": min(
            row["collision_partial_c_magnitude"] for row in rows
        ),
        "numerator_interval_enclosure_complete": False,
        "continuous_residue_envelope_complete": False,
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    if not dry_run:
        write_csv(ROWS, rows)
        write_csv(VALIDATION, validations)
        atomic_text(
            RESULT,
            json.dumps(result, indent=2, sort_keys=True) + "\n",
        )
    if not passed:
        failed = [
            row["check_id"] for row in validations if not row["passed"]
        ]
        raise RuntimeError(
            f"exact active denominator validation failed: {failed}"
        )
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    arguments = parser.parse_args()
    print(
        json.dumps(
            execute(arguments.dry_run),
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
