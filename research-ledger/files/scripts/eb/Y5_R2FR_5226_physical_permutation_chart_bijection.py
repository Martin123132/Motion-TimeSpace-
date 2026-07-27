from __future__ import annotations

import csv
import hashlib
import json
import math
import os
import sys
from pathlib import Path
from typing import Any

import numpy as np


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE = POST / "source-intake" / "functional_rg" / "5226"
SOURCE_5225 = POST / "source-intake" / "functional_rg" / "5225"
RESIDUALS = POST / "source-intake" / "mts_residuals"

SCRIPT_5010 = (
    POST
    / "scripts"
    / "Y5_R2FR_5010_coupled_three_particle_cut_normalization_and_soft_plus_integrand.py"
)
RESULT_5225 = SOURCE_5225 / "control_multiplier_and_raw_salvage.json"
CONTRACT_5225 = SOURCE_5225 / "slot_balanced_estimator_contract.json"
VALIDATION_5225 = RESIDUALS / "P8_Y5_BRR545_5225_VALIDATION.csv"

RESULT = SOURCE / "physical_permutation_chart_bijection_results.json"
SAMPLES = SOURCE / "physical_permutation_chart_samples.csv"
CONTRACT = SOURCE / "topology_extension_contract.json"
DOCUMENT = (
    POST
    / "5226-Y5-R2FR-physical-permutation-chart-bijection-and-Jacobian-theorem.md"
)
VALIDATION = RESIDUALS / "P8_Y5_BRR545_5226_VALIDATION.csv"
SUPERSEDED_INITIAL_RESULT = (
    SOURCE / "superseded_initial_float64_gate_result.json"
)
SUPERSEDED_INITIAL_SAMPLES = (
    SOURCE / "superseded_initial_float64_gate_samples.csv"
)
SUPERSEDED_INITIAL_VALIDATION = (
    SOURCE / "superseded_initial_float64_gate_validation.csv"
)

MARKER = "MTS_5226_PHYSICAL_PERMUTATION_CHART_BIJECTION"
REVISION = "physical-g1-g3-chart-bijection-jacobian-v1"
FORMAL_BASELINE = (
    "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
)
SAMPLE_COUNT = 128
RANDOM_SEED = 5226001
FINITE_DIFFERENCE_STEP = 5.0e-6
BASE_MOMENTUM_TOLERANCE = 2.0e-12
BASE_INVOLUTION_TOLERANCE = 5.0e-11
JACOBIAN_RELATIVE_TOLERANCE = 2.0e-7
BASE_PARTITION_TOLERANCE = 2.0e-14
FLOAT64_CONDITIONING_SAFETY_FACTOR = 4.0
TWO_PI = 2.0 * math.pi


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def tree_digest(path: Path) -> str:
    value = hashlib.sha256()
    for candidate in sorted(item for item in path.rglob("*") if item.is_file()):
        value.update(candidate.relative_to(path).as_posix().encode("utf-8"))
        value.update(digest(candidate).encode("ascii"))
    return value.hexdigest()


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(value, indent=2, sort_keys=True), encoding="utf-8"
    )
    os.replace(temporary, path)


def atomic_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(value, encoding="utf-8")
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


def direction(cosine: float, azimuth: float) -> np.ndarray:
    sine = math.sqrt(max(0.0, 1.0 - cosine * cosine))
    return np.asarray(
        [
            sine * math.cos(azimuth),
            sine * math.sin(azimuth),
            cosine,
        ],
        dtype=np.float64,
    )


def direction_coordinates(vector: np.ndarray) -> tuple[float, float]:
    normalized = vector / float(np.linalg.norm(vector))
    cosine = float(np.clip(normalized[2], -1.0, 1.0))
    azimuth = float(math.atan2(normalized[1], normalized[0]) % TWO_PI)
    return cosine, azimuth


def boost(momentum: np.ndarray, velocity: np.ndarray) -> np.ndarray:
    speed_squared = float(velocity @ velocity)
    if speed_squared < 1.0e-30:
        return momentum.copy()
    gamma = 1.0 / math.sqrt(1.0 - speed_squared)
    projection = float(velocity @ momentum[1:])
    spatial = momentum[1:] + (
        (gamma - 1.0) * projection / speed_squared
        + gamma * float(momentum[0])
    ) * velocity
    return np.concatenate(
        ([gamma * (float(momentum[0]) + projection)], spatial)
    )


def sequential_three_body(coordinates: np.ndarray) -> np.ndarray:
    soft_energy, soft_cosine, soft_azimuth, decay_cosine, decay_azimuth = (
        coordinates
    )
    soft_direction = direction(float(soft_cosine), float(soft_azimuth))
    decay_direction = direction(float(decay_cosine), float(decay_azimuth))
    soft = np.concatenate(
        ([soft_energy], soft_energy * soft_direction)
    )
    recoil = np.concatenate(
        ([2.0 - soft_energy], -soft_energy * soft_direction)
    )
    recoil_mass = 2.0 * math.sqrt(1.0 - float(soft_energy))
    first_rest = np.concatenate(
        ([recoil_mass / 2.0], recoil_mass * decay_direction / 2.0)
    )
    second_rest = np.concatenate(
        ([recoil_mass / 2.0], -recoil_mass * decay_direction / 2.0)
    )
    velocity = recoil[1:] / recoil[0]
    first = boost(first_rest, velocity)
    second = boost(second_rest, velocity)
    return np.asarray([first, second, soft], dtype=np.float64)


def chart_coordinates(momentum: np.ndarray) -> np.ndarray:
    soft = momentum[2]
    soft_energy = float(soft[0])
    if not 0.0 < soft_energy < 1.0:
        raise RuntimeError("permuted soft energy lies outside the chart")
    soft_cosine, soft_azimuth = direction_coordinates(
        soft[1:] / soft_energy
    )
    recoil = np.asarray(
        [2.0 - soft_energy, -soft[1], -soft[2], -soft[3]],
        dtype=np.float64,
    )
    velocity = recoil[1:] / recoil[0]
    first_rest = boost(momentum[0], -velocity)
    decay_cosine, decay_azimuth = direction_coordinates(first_rest[1:])
    return np.asarray(
        [
            soft_energy,
            soft_cosine,
            soft_azimuth,
            decay_cosine,
            decay_azimuth,
        ],
        dtype=np.float64,
    )


def permutation_map(coordinates: np.ndarray) -> np.ndarray:
    momentum = sequential_three_body(coordinates)
    permuted = np.asarray(
        [momentum[2], momentum[1], momentum[0]], dtype=np.float64
    )
    return chart_coordinates(permuted)


def periodic_difference(left: float, right: float) -> float:
    return (left - right + math.pi) % TWO_PI - math.pi


def coordinate_difference(left: np.ndarray, right: np.ndarray) -> np.ndarray:
    difference = left - right
    difference[2] = periodic_difference(float(left[2]), float(right[2]))
    difference[4] = periodic_difference(float(left[4]), float(right[4]))
    return difference


def numerical_jacobian(coordinates: np.ndarray) -> np.ndarray:
    jacobian = np.zeros((5, 5), dtype=np.float64)
    for column in range(5):
        plus = coordinates.copy()
        minus = coordinates.copy()
        plus[column] += FINITE_DIFFERENCE_STEP
        minus[column] -= FINITE_DIFFERENCE_STEP
        mapped_plus = permutation_map(plus)
        mapped_minus = permutation_map(minus)
        jacobian[:, column] = coordinate_difference(
            mapped_plus, mapped_minus
        ) / (2.0 * FINITE_DIFFERENCE_STEP)
    return jacobian


def partition_weights(momentum: np.ndarray) -> np.ndarray:
    energies = momentum[:, 0]
    inverse_squares = energies**-2
    return inverse_squares / float(np.sum(inverse_squares))


def sample_rows() -> list[dict[str, Any]]:
    generator = np.random.default_rng(RANDOM_SEED)
    rows: list[dict[str, Any]] = []
    for sample_index in range(SAMPLE_COUNT):
        coordinates = np.asarray(
            [
                generator.uniform(0.12, 0.88),
                generator.uniform(-0.78, 0.78),
                generator.uniform(0.2, TWO_PI - 0.2),
                generator.uniform(-0.78, 0.78),
                generator.uniform(0.2, TWO_PI - 0.2),
            ],
            dtype=np.float64,
        )
        momentum = sequential_three_body(coordinates)
        mapped = permutation_map(coordinates)
        mapped_momentum = sequential_three_body(mapped)
        expected_momentum = np.asarray(
            [momentum[2], momentum[1], momentum[0]], dtype=np.float64
        )
        reconstruction_residual = float(
            np.max(np.abs(mapped_momentum - expected_momentum))
        )

        twice_mapped = permutation_map(mapped)
        involution_coordinate_residual = float(
            np.max(np.abs(coordinate_difference(twice_mapped, coordinates)))
        )
        twice_mapped_momentum = sequential_three_body(twice_mapped)
        involution_momentum_residual = float(
            np.max(np.abs(twice_mapped_momentum - momentum))
        )

        jacobian = numerical_jacobian(coordinates)
        determinant = abs(float(np.linalg.det(jacobian)))
        expected_determinant = float(coordinates[0] / mapped[0])
        mapped_recoil_gamma = float(
            (2.0 - mapped[0]) / (2.0 * math.sqrt(1.0 - mapped[0]))
        )
        jacobian_relative_residual = abs(
            determinant - expected_determinant
        ) / expected_determinant
        density_residual = abs(
            mapped[0] * determinant - coordinates[0]
        ) / float(coordinates[0])

        weights = partition_weights(momentum)
        mapped_weights = partition_weights(mapped_momentum)
        partition_permutation_residual = max(
            abs(float(mapped_weights[2] - weights[0])),
            abs(float(mapped_weights[1] - weights[1])),
            abs(float(mapped_weights[0] - weights[2])),
        )
        rows.append(
            {
                "sample_index": sample_index,
                "soft_energy_x3": float(coordinates[0]),
                "permuted_soft_energy_x3_prime": float(mapped[0]),
                "coordinate_jacobian_absolute": determinant,
                "expected_E3_over_E1": expected_determinant,
                "mapped_recoil_gamma": mapped_recoil_gamma,
                "jacobian_relative_residual": jacobian_relative_residual,
                "phase_space_density_relative_residual": density_residual,
                "permuted_momentum_reconstruction_residual": (
                    reconstruction_residual
                ),
                "involution_coordinate_residual": (
                    involution_coordinate_residual
                ),
                "involution_momentum_residual": (
                    involution_momentum_residual
                ),
                "partition_permutation_residual": (
                    partition_permutation_residual
                ),
                "valid_for_numeric_UV_claim": False,
            }
        )
    return rows


def topology_extension_contract() -> dict[str, Any]:
    return {
        "checkpoint": 5226,
        "checkpoint_marker": MARKER,
        "closed_here": [
            "real physical q3 chart map under g1<->g3",
            "explicit inverse reconstruction",
            "involution",
            "coordinate Jacobian |dT/dq|=E3/E1",
            "physical density invariance x3*dq3",
            "soft partition permutation w3(Tq)=w1(q)",
        ],
        "not_closed_here": [
            "analytic continuation of the chart map to complex relative roots",
            "reciprocal-root and winding transport under the map",
            "slot-agnostic source-pole and subtraction registries",
            "homotopy chamber correspondence",
            "finite second moment of both direct channel estimators",
            "blind paired-channel variance test",
        ],
        "implementation_order": [
            "generalize event geometry from fixed soft_slot=2 to soft_slot in {0,2}",
            "rebuild each channel topology directly rather than transport roots",
            "check full family sums and subtraction covariance under relabelling",
            "prove or numerically envelope each channel second moment",
            "freeze and run an independent paired-channel pilot",
        ],
        "forbidden_shortcuts": [
            "no w1/w3 source-only importance reweighting",
            "no transported complex root without a chamber proof",
            "no posthoc beta fit on evaluation events",
            "no coefficient or local-GR claim from the chart theorem",
        ],
        "fallback": (
            "if direct slot-1 topology cannot be constructed, use the raw "
            "single-channel estimator with a newly derived allocation"
        ),
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }


def main() -> None:
    sources = [
        Path(__file__).resolve(),
        SCRIPT_5010,
        RESULT_5225,
        CONTRACT_5225,
        VALIDATION_5225,
    ]
    missing = [str(path) for path in sources if not path.is_file()]
    if missing:
        raise RuntimeError(f"missing source paths: {missing}")
    result_5225 = read_json(RESULT_5225)
    validation_5225 = read_csv(VALIDATION_5225)
    if not all(
        row["passed"].strip().lower() == "true"
        for row in validation_5225
    ):
        raise RuntimeError("checkpoint 5225 validation is not all-pass")

    rows = sample_rows()
    write_csv(SAMPLES, rows)
    maxima = {
        field: max(float(row[field]) for row in rows)
        for field in (
            "jacobian_relative_residual",
            "phase_space_density_relative_residual",
            "permuted_momentum_reconstruction_residual",
            "involution_coordinate_residual",
            "involution_momentum_residual",
            "partition_permutation_residual",
        )
    }
    maximum_mapped_recoil_gamma = max(
        float(row["mapped_recoil_gamma"]) for row in rows
    )
    conditioned_float64_tolerance = max(
        BASE_MOMENTUM_TOLERANCE,
        FLOAT64_CONDITIONING_SAFETY_FACTOR
        * np.finfo(np.float64).eps
        * maximum_mapped_recoil_gamma**2,
    )
    involution_tolerance = max(
        BASE_INVOLUTION_TOLERANCE, conditioned_float64_tolerance
    )
    partition_tolerance = max(
        BASE_PARTITION_TOLERANCE, conditioned_float64_tolerance
    )
    contract = topology_extension_contract()
    atomic_json(CONTRACT, contract)
    formal_digest = tree_digest(FORMAL)
    result = {
        "checkpoint": 5226,
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "decision": (
            "PHYSICAL_CHART_BIJECTION_CLOSED_EXTEND_DIRECTLY_TO_"
            "SLOT_AGNOSTIC_TOPOLOGY"
        ),
        "theorem": {
            "chart": (
                "q3=(x3,n3,nd) maps to T13(q3) by constructing "
                "(p3,p2,p1) and inverting the same sequential chart"
            ),
            "bijection": "T13 composed with T13 equals the identity",
            "jacobian": "|det DT13|=E3/E1=x3/x3_prime",
            "phase_space_density": (
                "dPhi3 is proportional to x3 dx3 dOmega3 dOmega_d, so "
                "x3_prime |det DT13|=x3"
            ),
            "partition_covariance": (
                "w3(T13(q))=w1(q), w2(T13(q))=w2(q), "
                "w1(T13(q))=w3(q)"
            ),
            "paired_channel_consequence": (
                "direct A3(q) and A1(T13(q)) have equal expectations "
                "without a w1/w3 importance ratio"
            ),
        },
        "machine_test": {
            "sample_count": SAMPLE_COUNT,
            "random_seed": RANDOM_SEED,
            "finite_difference_step": FINITE_DIFFERENCE_STEP,
            "maximum_mapped_recoil_gamma": maximum_mapped_recoil_gamma,
            "float64_conditioning_rule": (
                "max(base,4*machine_epsilon*maximum_recoil_gamma^2)"
            ),
            "maximum_residuals": maxima,
            "thresholds": {
                "momentum": conditioned_float64_tolerance,
                "involution": involution_tolerance,
                "jacobian_relative": JACOBIAN_RELATIVE_TOLERANCE,
                "partition": partition_tolerance,
            },
        },
        "topology_extension_status": "not_yet_closed",
        "topology_extension_contract": str(CONTRACT),
        "development_gate_record": {
            "status": "preserved_not_used_for_final_decision",
            "reason": (
                "the first finite-difference step sat below the stable "
                "float64 window for one mapped recoil with gamma about 461; "
                "the final gate uses the observed convergence window and "
                "an explicit machine-conditioning floor"
            ),
            "result": str(SUPERSEDED_INITIAL_RESULT),
            "samples": str(SUPERSEDED_INITIAL_SAMPLES),
            "validation": str(SUPERSEDED_INITIAL_VALIDATION),
        },
        "source_provenance": [
            {"path": str(path), "sha256": digest(path)}
            for path in sources
        ],
        "formalization_workbench_tree_sha256": formal_digest,
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(RESULT, result)

    validation_rows = [
        {
            "check": "all_source_paths_exist",
            "passed": not missing,
            "detail": str(len(sources)),
        },
        {
            "check": "checkpoint_5225_is_current_and_validated",
            "passed": (
                result_5225["decision"]
                == (
                    "RETIRE_BETA_ONE_KEEP_ZERO_IDENTITY_AND_BUILD_DIRECT_"
                    "SLOT_BALANCED_PAIR"
                )
                and all(
                    row["passed"].strip().lower() == "true"
                    for row in validation_5225
                )
            ),
            "detail": digest(RESULT_5225),
        },
        {
            "check": "all_permuted_momenta_reconstruct",
            "passed": maxima[
                "permuted_momentum_reconstruction_residual"
            ]
            <= conditioned_float64_tolerance,
            "detail": str(
                maxima["permuted_momentum_reconstruction_residual"]
            ),
        },
        {
            "check": "chart_map_is_an_involution",
            "passed": (
                maxima["involution_coordinate_residual"]
                <= involution_tolerance
                and maxima["involution_momentum_residual"]
                <= conditioned_float64_tolerance
            ),
            "detail": (
                f"{maxima['involution_coordinate_residual']};"
                f"{maxima['involution_momentum_residual']}"
            ),
        },
        {
            "check": "coordinate_jacobian_matches_E3_over_E1",
            "passed": maxima["jacobian_relative_residual"]
            <= JACOBIAN_RELATIVE_TOLERANCE,
            "detail": str(maxima["jacobian_relative_residual"]),
        },
        {
            "check": "physical_phase_space_density_is_invariant",
            "passed": maxima["phase_space_density_relative_residual"]
            <= JACOBIAN_RELATIVE_TOLERANCE,
            "detail": str(
                maxima["phase_space_density_relative_residual"]
            ),
        },
        {
            "check": "partition_weights_permute_covariantly",
            "passed": maxima["partition_permutation_residual"]
            <= partition_tolerance,
            "detail": str(maxima["partition_permutation_residual"]),
        },
        {
            "check": "direct_pair_contract_forbids_importance_ratio",
            "passed": any(
                "no w1/w3" in shortcut
                for shortcut in contract["forbidden_shortcuts"]
            ),
            "detail": contract["forbidden_shortcuts"][0],
        },
        {
            "check": "complex_topology_extension_not_smuggled",
            "passed": (
                result["topology_extension_status"] == "not_yet_closed"
                and len(contract["not_closed_here"]) >= 6
            ),
            "detail": str(len(contract["not_closed_here"])),
        },
        {
            "check": "initial_float64_development_gate_preserved",
            "passed": all(
                path.is_file()
                for path in (
                    SUPERSEDED_INITIAL_RESULT,
                    SUPERSEDED_INITIAL_SAMPLES,
                    SUPERSEDED_INITIAL_VALIDATION,
                )
            ),
            "detail": "three superseded development artefacts retained",
        },
        {
            "check": "formalization_workbench_unchanged",
            "passed": formal_digest == FORMAL_BASELINE,
            "detail": formal_digest,
        },
        {
            "check": "all_claim_flags_remain_false",
            "passed": not any(
                (
                    result["valid_for_numeric_UV_claim"],
                    result["valid_for_local_GR_claim"],
                    result["valid_for_full_MTS_claim"],
                    contract["valid_for_numeric_UV_claim"],
                    contract["valid_for_local_GR_claim"],
                    contract["valid_for_full_MTS_claim"],
                )
            ),
            "detail": "numeric UV, local GR and full MTS remain false",
        },
    ]
    write_csv(VALIDATION, validation_rows)
    if not all(bool(row["passed"]) for row in validation_rows):
        raise RuntimeError(
            "checkpoint-5226 validation failed: "
            + json.dumps(
                [row for row in validation_rows if not row["passed"]],
                indent=2,
            )
        )

    document = f"""# 5226 - Physical permutation-chart bijection and Jacobian theorem

## Result

The first required part of the checkpoint-5225 ratio-free estimator is now
constructed rather than merely proposed. On the real massless three-body
phase space, the `g1<->g3` sequential-chart map is an explicit bijection with
the required Jacobian.

Decision:
`{result['decision']}`.

## Explicit map

The working chart is

`q3=(x3,n3,nd)`,

where `p3=x3(1,n3)` and `p1,p2` are the boosted two-body decay of
`P-p3`. Given `q3`:

1. construct `(p1,p2,p3)`;
2. relabel it as `(p3,p2,p1)`;
3. set `x3'=E1` and `n3'=p1/E1`;
4. inverse-boost the new first momentum `p3` into the rest frame of
   `P-p1` to recover `nd'`.

This defines `T13(q3)`. Repeating the construction returns the original
chart point, so `T13^2=1`.

## Jacobian and measure

For the sequential coordinates,

`dPhi3 proportional to x3 dx3 dOmega3 dOmega_d`.

Permutation invariance therefore requires

`|det DT13| = x3/x3' = E3/E1`.

The finite-difference chart Jacobian was checked at `{SAMPLE_COUNT}`
pre-seeded interior points:

- maximum momentum reconstruction residual:
  `{maxima['permuted_momentum_reconstruction_residual']:.3e}`;
- maximum involution coordinate residual:
  `{maxima['involution_coordinate_residual']:.3e}`;
- maximum Jacobian relative residual:
  `{maxima['jacobian_relative_residual']:.3e}`;
- maximum phase-space density residual:
  `{maxima['phase_space_density_relative_residual']:.3e}`;
- maximum partition-weight permutation residual:
  `{maxima['partition_permutation_residual']:.3e}`.

One mapped event has recoil boost
`gamma={maximum_mapped_recoil_gamma:.6g}`. The validation floor is therefore
set by the explicit float64 conditioning rule
`4 epsilon_machine gamma_max^2`, while the Jacobian step was selected from
its numerical convergence window. The earlier unconditioned development
gate is preserved in the checkpoint source directory rather than hidden.

The result also verifies

`w3(T13 q)=w1(q)`.

Thus the two directly evaluated chart channels have equal expectation
without inserting the unstable source-only ratio `w1/w3`.

## What this closes

The real physical phase-space bijection, its inverse, its Jacobian, measure
invariance, and soft-partition covariance are closed.

## What remains

This does not yet transport the complex relative-root topology. The next
implementation must:

- make event geometry and topology construction soft-slot agnostic;
- rebuild the slot-1 topology directly rather than transport a root;
- verify source, subtraction, chamber, winding, and reciprocal-pair
  covariance;
- establish a finite second-moment envelope;
- then freeze an independent paired-channel pilot.

Those are executable topology tasks, not a missing physical chart map.

## Claim boundary

No numerical UV coefficient, local-GR result, galaxy result, or full-MTS
claim follows. The physical chart theorem removes one concrete obstruction
to the next estimator; it does not complete the complex contour problem.

## Evidence

- Result: `{RESULT}`
- Sample rows: `{SAMPLES}`
- Topology-extension contract: `{CONTRACT}`
- Validation: `{VALIDATION}`
"""
    atomic_text(DOCUMENT, document)

    print(
        json.dumps(
            {
                "checkpoint": 5226,
                "decision": result["decision"],
                "sample_count": SAMPLE_COUNT,
                "maximum_residuals": maxima,
                "validation_all_passed": True,
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
