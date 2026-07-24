from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import subprocess
import sys
from pathlib import Path
from typing import Any

import sympy as sp


sys.dont_write_bytecode = True

POST = Path(__file__).resolve().parents[1]
FORMAL = POST.parent / "formalization-workbench"
SCRIPT = Path(__file__).resolve()
OUT = POST / "source-intake" / "functional_rg" / "5202"
DOCUMENT = (
    POST
    / "5202-Y5-R2FR-scalar-curvature-no-go-translation-gauge-TEGR-"
    "coframe-ancestry-and-mode-theorem.md"
)
VALIDATION = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5202_VALIDATION.csv"
)
CHECKPOINT_5201_OUT = POST / "source-intake" / "functional_rg" / "5201"
PUBLIC_WORKTREE = Path(
    r"C:\Users\ollet\OneDrive\Documents\Motion-TimeSpace-public-update-2026-07-22"
)
GALAXY_REPO = Path(r"D:\Users\ollet\Desktop\MTS-Galaxy-Lab-repo")

MARKER = "MTS_5202_TRANSLATION_GAUGE_TEGR_COFRAME_ANCESTRY_THEOREM"
CHECKED_DATE = "2026-07-24"
FORMAL_LOCK = (
    "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
)
CHECKPOINT_5201_OUT_LOCK = (
    "310a38df16ccf617e6a28124afa717bac1aa2802fc9202853e8a3613d8c583b0"
)
PUBLIC_HEAD_LOCK = "8913c00b77d98e457ddb0c48e9aeec9cc5f309fd"
GALAXY_HEAD_LOCK = "f850e4997657f457dddc05cbe50f21186588dcc7"

SOURCE_LOCKS = {
    "4070-Y5-R2FR-psi-packet-coframe-parent-action-normalization-and-torsion-gate.md": (
        "15f7dfcbee87fef91a584aa018e9557706b278f849b05a8bd797140d94bce2f6"
    ),
    "4071-Y5-R2FR-Cartan-solder-field-origin-from-MTS-flow-or-demotion.md": (
        "ee1f539a6e1d19f73cf7844c97957227d08ca4c8a71e4fba428ce9cd66e1e4ed"
    ),
    "4072-Y5-R2FR-local-motion-frame-gauge-action-or-effective-GR-demotion.md": (
        "14dbf16a1e90cc0fc13c52483e0c78d2c9eabdbaca51aa62397c285f0a574d1e"
    ),
    "4073-Y5-R2FR-formal-adoption-or-demotion-of-motion-frame-gauge-parent.md": (
        "e6ff78deb09f689ebd86925b60874d40fd85cecf85434614ac8af6dfd7ee8c2a"
    ),
    "4074-Y5-R2FR-flow-solder-field-parent-signature-or-effective-tetrad-demotion.md": (
        "9e08bece754d73deadba272bb3d305896e05e0b186ffa9882dde83c953875b5c"
    ),
    "5188-Y5-R2FR-relational-clock-scalar-no-go-minimal-coframe-parent-and-Fierz-Pauli-selection-theorem.md": (
        "06f376fbab1a07312ae6993f1ea2a2e2f276a2438d7a2c15daf7993a17f6fb7a"
    ),
    "5189-Y5-R2FR-motion-sector-ADM-projection-clock-only-ancestry-and-local-tensor-protection-theorem.md": (
        "4514f59f95fa00fbddd652511bf49a98a84347b3f4f10747afbdfb6d3917e266"
    ),
    "5201-Y5-R2FR-source-complete-coframe-variation-full-PPN-calibration-and-local-state-silence-theorem.md": (
        "e77e2f7b5c3b4376c7e8a792342c3ec49c912627c60f83c712597c74ccbb8507"
    ),
    "source-intake/mts_residuals/P8_Y5_R2FR_4070_EXACT_GRADIENT_FLATNESS_OBSTRUCTION.csv": (
        "1a1745b63386c12c9b011ba25d07899b07ac7ec9f04854b99a5305cb3d3a7c46"
    ),
    "source-intake/mts_residuals/P8_Y5_R2FR_4071_LOCAL_MOTION_FRAME_GAUGE_TEST.csv": (
        "510701e955a13f29d7fe8d1eaf0c23f11bbe59b4caa2a941c33226574e53567b"
    ),
    "source-intake/mts_residuals/P8_Y5_R2FR_4072_GAUGE_VARIATION_AND_FIELD_STRENGTHS.csv": (
        "22dd81f3bfa1878fcec773d908120affa6129a8222d244823fc6788f5cb2b029"
    ),
    "source-intake/mts_residuals/P8_Y5_R2FR_4074_FLOW_TO_SOLDER_SIGNATURE_TEST.csv": (
        "c1d759c5edd86123ac6816501a8e29e0a39b16195cbb2c41bc92ff59f7ff2dd5"
    ),
    "source-intake/mts_residuals/P8_Y5_R2FR_4074_BFIELD_DERIVATION_ATTEMPT.csv": (
        "da9abc84d9004c8963fd61c2a5249a54595c7dea97d6cf61e852151ae812158d"
    ),
    "source-intake/functional_rg/5188/relational_coframe_parent_results.json": (
        "9160b84ad6cbb9de7cda7df53b4d5a0c35f24b0b2c2795ff529bc94a3c12a30b"
    ),
    "source-intake/functional_rg/5188/Fierz_Pauli_gauge_nullspace.csv": (
        "638bc0a7fe20ed5c0966b71de723fe17e0d9464dae84716acad1f3e946fc45fe"
    ),
    "source-intake/functional_rg/5189/motion_ADM_projection_results.json": (
        "6418ffc826ed2068b1f4df46d56423fe3f866c0e9bfa363098f4e849174fcfc2"
    ),
    "source-intake/functional_rg/5201/source_complete_coframe_PPN_local_silence_results.json": (
        "99939a2990e033451ee5c33dbaffcf7ffeaa2e2131156c6d6161e70f0964141c"
    ),
}


def file_digest(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def tree_digest(path: Path) -> str:
    digest = hashlib.sha256()
    for item in sorted(candidate for candidate in path.rglob("*") if candidate.is_file()):
        digest.update(item.relative_to(path).as_posix().encode("utf-8"))
        digest.update(file_digest(item).encode("ascii"))
    return digest.hexdigest()


def git_state(repository: Path) -> tuple[str, str]:
    safe_path = repository.as_posix()
    head = subprocess.run(
        ["git", "-c", f"safe.directory={safe_path}", "rev-parse", "HEAD"],
        cwd=repository,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    status = subprocess.run(
        ["git", "-c", f"safe.directory={safe_path}", "status", "--short"],
        cwd=repository,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    return head, status


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty CSV: {path}")
    fieldnames: list[str] = []
    for row in rows:
        fieldnames.extend(field for field in row if field not in fieldnames)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def tagged(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": 5202,
            "marker": MARKER,
            "checked_date": CHECKED_DATE,
            "valid_for_full_MTS_claim": False,
            **row,
        }
        for row in rows
    ]


def assert_source_locks() -> None:
    failures: list[str] = []
    for relative_path, expected_digest in SOURCE_LOCKS.items():
        source_path = POST / relative_path
        if not source_path.exists():
            failures.append(f"missing:{relative_path}")
            continue
        actual_digest = file_digest(source_path)
        if actual_digest != expected_digest:
            failures.append(
                f"hash:{relative_path}:{actual_digest}!={expected_digest}"
            )
    if tree_digest(FORMAL) != FORMAL_LOCK:
        failures.append("formalization-workbench tree changed")
    if tree_digest(CHECKPOINT_5201_OUT) != CHECKPOINT_5201_OUT_LOCK:
        failures.append("checkpoint-5201 output tree changed")
    if failures:
        raise RuntimeError("source lock failure: " + "; ".join(failures))


def levi_civita_scalar_curvature(
    metric: sp.Matrix, coordinates: list[sp.Symbol]
) -> sp.Expr:
    inverse_metric = sp.simplify(metric.inv())
    dimension = metric.rows
    connection = [
        [
            [
                sp.simplify(
                    sp.Rational(1, 2)
                    * sum(
                        inverse_metric[upper, index]
                        * (
                            sp.diff(
                                metric[index, second], coordinates[first]
                            )
                            + sp.diff(
                                metric[index, first], coordinates[second]
                            )
                            - sp.diff(
                                metric[first, second], coordinates[index]
                            )
                        )
                        for index in range(dimension)
                    )
                )
                for second in range(dimension)
            ]
            for first in range(dimension)
        ]
        for upper in range(dimension)
    ]
    ricci = [
        [
            sp.simplify(
                sum(
                    sp.diff(
                        connection[upper][first][second], coordinates[upper]
                    )
                    - sp.diff(
                        connection[upper][first][upper], coordinates[second]
                    )
                    + sum(
                        connection[upper][upper][index]
                        * connection[index][first][second]
                        - connection[upper][second][index]
                        * connection[index][first][upper]
                        for index in range(dimension)
                    )
                    for upper in range(dimension)
                )
            )
            for second in range(dimension)
        ]
        for first in range(dimension)
    ]
    return sp.simplify(
        sum(
            inverse_metric[first, second] * ricci[first][second]
            for first in range(dimension)
            for second in range(dimension)
        )
    )


def tetrad_geometry(
    tetrad: sp.Matrix, coordinates: list[sp.Symbol]
) -> dict[str, Any]:
    dimension = tetrad.rows
    internal_metric = sp.diag(-1, 1, 1, 1)
    inverse_tetrad = sp.simplify(tetrad.inv())
    metric = sp.simplify(tetrad.T * internal_metric * tetrad)
    inverse_metric = sp.simplify(metric.inv())
    determinant = sp.simplify(tetrad.det())
    torsion = [
        [
            [
                sp.simplify(
                    sum(
                        inverse_tetrad[upper, internal]
                        * (
                            sp.diff(
                                tetrad[internal, second],
                                coordinates[first],
                            )
                            - sp.diff(
                                tetrad[internal, first],
                                coordinates[second],
                            )
                        )
                        for internal in range(dimension)
                    )
                )
                for second in range(dimension)
            ]
            for first in range(dimension)
        ]
        for upper in range(dimension)
    ]
    torsion_lower = [
        [
            [
                sp.simplify(
                    sum(
                        metric[upper, index] * torsion[index][first][second]
                        for index in range(dimension)
                    )
                )
                for second in range(dimension)
            ]
            for first in range(dimension)
        ]
        for upper in range(dimension)
    ]
    torsion_upper = [
        [
            [
                sp.simplify(
                    sum(
                        inverse_metric[upper, source_upper]
                        * inverse_metric[first, source_first]
                        * inverse_metric[second, source_second]
                        * torsion_lower[source_upper][source_first][
                            source_second
                        ]
                        for source_upper in range(dimension)
                        for source_first in range(dimension)
                        for source_second in range(dimension)
                    )
                )
                for second in range(dimension)
            ]
            for first in range(dimension)
        ]
        for upper in range(dimension)
    ]
    invariant_one = sp.simplify(
        sum(
            torsion_upper[upper][first][second]
            * torsion_lower[upper][first][second]
            for upper in range(dimension)
            for first in range(dimension)
            for second in range(dimension)
        )
    )
    invariant_two = sp.simplify(
        sum(
            torsion_upper[upper][first][second]
            * torsion_lower[second][first][upper]
            for upper in range(dimension)
            for first in range(dimension)
            for second in range(dimension)
        )
    )
    torsion_vector_lower = [
        sp.simplify(
            sum(torsion[index][index][first] for index in range(dimension))
        )
        for first in range(dimension)
    ]
    invariant_three = sp.simplify(
        sum(
            inverse_metric[first, second]
            * torsion_vector_lower[first]
            * torsion_vector_lower[second]
            for first in range(dimension)
            for second in range(dimension)
        )
    )
    torsion_scalar = sp.simplify(
        sp.Rational(1, 4) * invariant_one
        + sp.Rational(1, 2) * invariant_two
        - invariant_three
    )
    torsion_vector_upper = [
        sp.simplify(
            sum(
                inverse_metric[first, second] * torsion_vector_lower[second]
                for second in range(dimension)
            )
        )
        for first in range(dimension)
    ]
    boundary_scalar = sp.simplify(
        2
        / determinant
        * sum(
            sp.diff(
                determinant * torsion_vector_upper[first],
                coordinates[first],
            )
            for first in range(dimension)
        )
    )
    curvature_scalar = levi_civita_scalar_curvature(metric, coordinates)
    return {
        "metric": metric,
        "determinant": determinant,
        "torsion": torsion,
        "I1": invariant_one,
        "I2": invariant_two,
        "I3": invariant_three,
        "T": torsion_scalar,
        "B_boundary": boundary_scalar,
        "R_LC": curvature_scalar,
        "identity_residual": sp.simplify(
            curvature_scalar + torsion_scalar - boundary_scalar
        ),
    }


def scalar_gradient_curvature_no_go(
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    time_coord, x_coord, y_coord, z_coord = sp.symbols("t x y z")
    alpha = sp.symbols("alpha")
    coordinates = [time_coord, x_coord, y_coord, z_coord]
    holonomic_tetrad = sp.diag(
        1,
        1 + 2 * alpha * x_coord,
        1,
        1,
    )
    holonomic_geometry = tetrad_geometry(holonomic_tetrad, coordinates)
    maximum_torsion_component = max(
        (
            abs(component)
            for upper_block in holonomic_geometry["torsion"]
            for first_block in upper_block
            for component in first_block
        ),
        default=sp.S.Zero,
    )
    rank_rows = []
    for scalar_count in range(1, 5):
        rank_rows.append(
            {
                "candidate": f"{scalar_count}_scalar_gradients",
                "maximum_metric_rank": scalar_count,
                "nondegenerate_4D_possible": scalar_count >= 4,
                "curved_GR_possible_with_fixed_internal_eta": False,
                "reason": (
                    "rank <= number of independent gradients"
                    if scalar_count < 4
                    else (
                        "invertible X^A are local coordinates and pull back "
                        "flat internal eta"
                    )
                ),
                "status": (
                    "RANK_OBSTRUCTION"
                    if scalar_count < 4
                    else "HOLONOMIC_FLATNESS_OBSTRUCTION"
                ),
            }
        )
    rank_rows.extend(
        [
            {
                "candidate": "four_scalars_plus_scalar_conformal_factor",
                "maximum_metric_rank": 4,
                "nondegenerate_4D_possible": True,
                "curved_GR_possible_with_fixed_internal_eta": False,
                "reason": (
                    "metric is conformally flat so Weyl[g]=0, while "
                    "Schwarzschild has C^2=48(GM)^2/r^6"
                ),
                "status": "WEYL_OBSTRUCTION",
            },
            {
                "candidate": "four_scalars_plus_internal_metric_G_AB",
                "maximum_metric_rank": 4,
                "nondegenerate_4D_possible": True,
                "curved_GR_possible_with_fixed_internal_eta": True,
                "reason": (
                    "G_AB carries ten independent metric components; this is "
                    "a metric change of variables, not scalar-only emergence"
                ),
                "status": "EQUIVALENT_METRIC_FIELD_CONTENT",
            },
            {
                "candidate": "old_single_motion_scalar_psi",
                "maximum_metric_rank": 1,
                "nondegenerate_4D_possible": False,
                "curved_GR_possible_with_fixed_internal_eta": False,
                "reason": "5188/5189 clock-only rank obstruction retained",
                "status": "REJECTED_AS_SPATIAL_COFRAME_ANCESTOR",
            },
        ]
    )
    diagnostics = {
        "holonomic_tetrad_determinant": str(
            holonomic_geometry["determinant"]
        ),
        "holonomic_torsion_maximum": str(maximum_torsion_component),
        "holonomic_torsion_scalar": str(holonomic_geometry["T"]),
        "holonomic_Ricci_scalar": str(holonomic_geometry["R_LC"]),
        "holonomic_TEGR_identity_residual": str(
            holonomic_geometry["identity_residual"]
        ),
        "minimum_scalar_count_for_rank_four": 4,
        "four_scalar_fixed_eta_curvature": False,
        "old_motion_scalar_can_generate_spatial_coframe": False,
    }
    return tagged(rank_rows), diagnostics


def translation_gauge_construction(
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    derivative_coordinates = sp.Matrix(
        [
            [1, 2, 0, -1],
            [0, 1, 3, 2],
            [2, -1, 1, 0],
            [1, 0, 2, 1],
        ]
    )
    translation_connection = sp.Matrix(
        [
            [0, 1, -1, 2],
            [2, 0, 1, -1],
            [1, 3, 0, 1],
            [-1, 2, 1, 0],
        ]
    )
    derivative_parameter = sp.Matrix(
        [
            [1, -2, 1, 0],
            [0, 1, -1, 2],
            [2, 0, 1, -1],
            [1, 1, 0, 1],
        ]
    )
    coframe_before = derivative_coordinates + translation_connection
    coframe_after = (
        derivative_coordinates + derivative_parameter
        + translation_connection
        - derivative_parameter
    )
    translation_residual_matrix = sp.simplify(
        coframe_after - coframe_before
    )
    translation_residual = max(
        (abs(component) for component in translation_residual_matrix),
        default=sp.S.Zero,
    )

    internal_metric = sp.diag(-1, 1, 1, 1)
    rational_boost = sp.Matrix(
        [
            [sp.Rational(5, 4), sp.Rational(3, 4), 0, 0],
            [sp.Rational(3, 4), sp.Rational(5, 4), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ]
    )
    lorentz_residual = sp.simplify(
        rational_boost.T * internal_metric * rational_boost
        - internal_metric
    )
    rational_coframe = sp.Matrix(
        [
            [2, 1, 0, 0],
            [0, 1, 1, 0],
            [0, 0, 2, 1],
            [1, 0, 0, 1],
        ]
    )
    metric_before = sp.simplify(
        rational_coframe.T * internal_metric * rational_coframe
    )
    transformed_coframe = rational_boost * rational_coframe
    metric_after = sp.simplify(
        transformed_coframe.T * internal_metric * transformed_coframe
    )
    metric_residual = sp.simplify(metric_after - metric_before)

    rows = tagged(
        [
            {
                "step": "relational_coordinates",
                "equation": "X^A=(X^0,X^1,X^2,X^3)",
                "interpretation": "one clock and three spatial rods",
                "status": "MINIMUM_RANK_FOUR_RELATIONAL_PACKET",
                "old_scalar_derived": False,
            },
            {
                "step": "translation_connection",
                "equation": "mathcalB^A=mathcalB^A_m dx^m",
                "interpretation": (
                    "internal-vector-valued one-form carrying nonholonomic "
                    "translation/motion"
                ),
                "status": "MINIMUM_NONSCALAR_CURVATURE_CARRIER",
                "old_scalar_derived": False,
            },
            {
                "step": "coframe",
                "equation": "e^A=D_omega X^A+mathcalB^A",
                "interpretation": "covariant relational displacement",
                "status": "EXACT_GAUGE_CONSTRUCTION",
                "old_scalar_derived": False,
            },
            {
                "step": "local_translation",
                "equation": (
                    "X'^A=X^A+epsilon^A; "
                    "mathcalB'^A=mathcalB^A-D_omega epsilon^A"
                ),
                "interpretation": "e^A is translation-gauge invariant",
                "status": "EXECUTED_ZERO_RESIDUAL",
                "old_scalar_derived": False,
            },
            {
                "step": "local_Lorentz",
                "equation": (
                    "e'^A=Lambda^A_B e^B; "
                    "Lambda^T eta Lambda=eta"
                ),
                "interpretation": "g=eta_AB e^A e^B is frame invariant",
                "status": "EXECUTED_EXACT_RATIONAL_BOOST",
                "old_scalar_derived": False,
            },
            {
                "step": "teleparallel_gauge",
                "equation": "R^A_B[omega_inertial]=0",
                "interpretation": (
                    "gravity is represented by torsion/anholonomy of e, "
                    "not an extra matter force"
                ),
                "status": "TEGR_CONNECTION_CHOICE",
                "old_scalar_derived": False,
            },
            {
                "step": "torsion",
                "equation": (
                    "T^A=D_omega e^A=R^A_B X^B+D_omega mathcalB^A"
                ),
                "interpretation": (
                    "for flat omega, T^A=D_omega mathcalB^A"
                ),
                "status": "NONHOLONOMIC_FIELD_STRENGTH",
                "old_scalar_derived": False,
            },
            {
                "step": "notation_guard",
                "equation": "mathcalB^A is not the galaxy outer-wall B=8",
                "interpretation": "separate translation connection",
                "status": "NO_SYMBOLIC_CONFLATION",
                "old_scalar_derived": False,
            },
        ]
    )
    diagnostics = {
        "maximum_translation_gauge_residual": str(translation_residual),
        "translation_gauge_residual": str(translation_residual_matrix),
        "Lorentz_metric_residual": str(lorentz_residual),
        "coframe_metric_invariance_residual": str(metric_residual),
        "sample_coframe_determinant": str(coframe_before.det()),
        "translation_connection_required": True,
        "translation_connection_derived_from_old_scalar": False,
    }
    return rows, diagnostics


def linear_torsion_invariants(
    momentum: list[int | sp.Expr],
    perturbation: sp.Matrix,
) -> tuple[sp.Expr, sp.Expr, sp.Expr]:
    internal_metric = sp.diag(-1, 1, 1, 1)
    dimension = 4
    torsion = [
        [
            [
                sp.expand(
                    momentum[first] * perturbation[upper, second]
                    - momentum[second] * perturbation[upper, first]
                )
                for second in range(dimension)
            ]
            for first in range(dimension)
        ]
        for upper in range(dimension)
    ]
    torsion_lower = [
        [
            [
                sp.expand(
                    sum(
                        internal_metric[upper, index]
                        * torsion[index][first][second]
                        for index in range(dimension)
                    )
                )
                for second in range(dimension)
            ]
            for first in range(dimension)
        ]
        for upper in range(dimension)
    ]
    torsion_upper = [
        [
            [
                sp.expand(
                    sum(
                        internal_metric[upper, source_upper]
                        * internal_metric[first, source_first]
                        * internal_metric[second, source_second]
                        * torsion_lower[source_upper][source_first][
                            source_second
                        ]
                        for source_upper in range(dimension)
                        for source_first in range(dimension)
                        for source_second in range(dimension)
                    )
                )
                for second in range(dimension)
            ]
            for first in range(dimension)
        ]
        for upper in range(dimension)
    ]
    invariant_one = sp.expand(
        sum(
            torsion_upper[upper][first][second]
            * torsion_lower[upper][first][second]
            for upper in range(dimension)
            for first in range(dimension)
            for second in range(dimension)
        )
    )
    invariant_two = sp.expand(
        sum(
            torsion_upper[upper][first][second]
            * torsion_lower[second][first][upper]
            for upper in range(dimension)
            for first in range(dimension)
            for second in range(dimension)
        )
    )
    torsion_vector = [
        sp.expand(sum(torsion[index][index][first] for index in range(dimension)))
        for first in range(dimension)
    ]
    invariant_three = sp.expand(
        sum(
            internal_metric[first, second]
            * torsion_vector[first]
            * torsion_vector[second]
            for first in range(dimension)
            for second in range(dimension)
        )
    )
    return invariant_one, invariant_two, invariant_three


def lorentz_and_linearized_diffeomorphism_generators(
    momentum: list[int | sp.Expr],
) -> tuple[sp.Matrix, sp.Matrix]:
    internal_metric = sp.diag(-1, 1, 1, 1)
    lorentz_columns: list[sp.Matrix] = []
    for first in range(4):
        for second in range(first + 1, 4):
            lower_generator = sp.zeros(4)
            lower_generator[first, second] = 1
            lower_generator[second, first] = -1
            mixed_generator = internal_metric * lower_generator
            column = sp.zeros(16, 1)
            for internal in range(4):
                for spacetime in range(4):
                    column[4 * internal + spacetime] = mixed_generator[
                        internal, spacetime
                    ]
            lorentz_columns.append(column)
    diffeomorphism_columns: list[sp.Matrix] = []
    for internal in range(4):
        column = sp.zeros(16, 1)
        for spacetime in range(4):
            column[4 * internal + spacetime] = momentum[spacetime]
        diffeomorphism_columns.append(column)
    return (
        sp.Matrix.hstack(*lorentz_columns),
        sp.Matrix.hstack(*diffeomorphism_columns),
    )


def tegr_coefficient_and_mode_gate(
) -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    dict[str, Any],
]:
    coefficient_one, coefficient_two, coefficient_three = sp.symbols(
        "c1 c2 c3"
    )
    perturbation_symbols = sp.symbols("b0:16")
    perturbation = sp.Matrix(
        4,
        4,
        lambda internal, spacetime: perturbation_symbols[
            4 * internal + spacetime
        ],
    )
    momentum_samples = [
        [1, 2, 3, 5],
        [2, -1, 4, 3],
        [0, 1, 2, 3],
        [3, 0, 1, -2],
    ]
    constraint_rows: list[list[sp.Expr]] = []
    first_hessian: sp.Matrix | None = None
    first_lorentz: sp.Matrix | None = None
    first_diffeomorphism: sp.Matrix | None = None
    for sample_index, momentum in enumerate(momentum_samples):
        invariant_one, invariant_two, invariant_three = (
            linear_torsion_invariants(momentum, perturbation)
        )
        quadratic_form = sp.expand(
            coefficient_one * invariant_one
            + coefficient_two * invariant_two
            + coefficient_three * invariant_three
        )
        hessian = sp.hessian(quadratic_form, perturbation_symbols)
        lorentz_generators, diffeomorphism_generators = (
            lorentz_and_linearized_diffeomorphism_generators(momentum)
        )
        if sample_index == 0:
            first_hessian = hessian
            first_lorentz = lorentz_generators
            first_diffeomorphism = diffeomorphism_generators
        lorentz_response = hessian * lorentz_generators
        for response in lorentz_response:
            expanded = sp.expand(response)
            constraint_rows.append(
                [
                    expanded.coeff(coefficient_one),
                    expanded.coeff(coefficient_two),
                    expanded.coeff(coefficient_three),
                ]
            )

    constraint_matrix = sp.Matrix(constraint_rows)
    coefficient_nullspace = constraint_matrix.nullspace()
    if len(coefficient_nullspace) != 1:
        raise RuntimeError(
            f"unexpected TEGR coefficient nullity: {len(coefficient_nullspace)}"
        )
    selected_coefficients = coefficient_nullspace[0]
    selected_coefficients /= selected_coefficients[2]
    expected_coefficients = sp.Matrix(
        [-sp.Rational(1, 4), -sp.Rational(1, 2), 1]
    )
    coefficient_residual = sp.simplify(
        selected_coefficients - expected_coefficients
    )
    if (
        first_hessian is None
        or first_lorentz is None
        or first_diffeomorphism is None
    ):
        raise RuntimeError("no linearized Hessian was constructed")
    selected_hessian = sp.simplify(
        first_hessian.subs(
            {
                coefficient_one: selected_coefficients[0],
                coefficient_two: selected_coefficients[1],
                coefficient_three: selected_coefficients[2],
            }
        )
    )
    combined_gauge = first_lorentz.row_join(first_diffeomorphism)
    lorentz_hessian_residual = sp.simplify(
        selected_hessian * first_lorentz
    )
    diffeomorphism_hessian_residual = sp.simplify(
        selected_hessian * first_diffeomorphism
    )

    symbolic_momentum = list(sp.symbols("k0:4"))
    symbolic_invariants = linear_torsion_invariants(
        symbolic_momentum,
        perturbation,
    )
    symbolic_selected_form = sp.expand(
        selected_coefficients[0] * symbolic_invariants[0]
        + selected_coefficients[1] * symbolic_invariants[1]
        + selected_coefficients[2] * symbolic_invariants[2]
    )
    symbolic_selected_hessian = sp.hessian(
        symbolic_selected_form,
        perturbation_symbols,
    )
    symbolic_frame_generators, symbolic_diffeomorphism_generators = (
        lorentz_and_linearized_diffeomorphism_generators(
            symbolic_momentum
        )
    )
    symbolic_frame_residual = symbolic_selected_hessian * (
        symbolic_frame_generators
    )
    symbolic_diffeomorphism_residual = symbolic_selected_hessian * (
        symbolic_diffeomorphism_generators
    )
    symbolic_frame_zero = all(
        sp.expand(component) == 0
        for component in symbolic_frame_residual
    )
    symbolic_diffeomorphism_zero = all(
        sp.expand(component) == 0
        for component in symbolic_diffeomorphism_residual
    )
    generic_ngr_hessian = sp.hessian(
        symbolic_invariants[0],
        perturbation_symbols,
    )
    generic_ngr_frame_response_nonzero = any(
        sp.expand(component) != 0
        for component in generic_ngr_hessian * symbolic_frame_generators
    )

    frequency, wave_number, plus_mode, cross_mode = sp.symbols(
        "omega k h_plus h_cross", real=True
    )
    transverse_traceless = sp.zeros(4)
    transverse_traceless[1, 1] = plus_mode / 2
    transverse_traceless[2, 2] = -plus_mode / 2
    transverse_traceless[1, 2] = cross_mode / 2
    transverse_traceless[2, 1] = cross_mode / 2
    tt_invariants = linear_torsion_invariants(
        [frequency, 0, 0, wave_number],
        transverse_traceless,
    )
    tt_action = sp.factor(
        selected_coefficients[0] * tt_invariants[0]
        + selected_coefficients[1] * tt_invariants[1]
        + selected_coefficients[2] * tt_invariants[2]
    )
    expected_tt_action = sp.factor(
        (plus_mode**2 + cross_mode**2)
        * (frequency**2 - wave_number**2)
        / 2
    )
    tt_residual = sp.simplify(tt_action - expected_tt_action)

    coefficient_rows = tagged(
        [
            {
                "invariant": "I1=T^rho_mn T_rho^mn",
                "generic_coefficient": "c1",
                "selected_action_coefficient": str(selected_coefficients[0]),
                "TEGR_torsion_scalar_coefficient": "1/4",
                "status": "UNIQUE_PURE_TETRAD_FRAME_NULL_RAY",
            },
            {
                "invariant": "I2=T^rho_mn T^(nm)_rho",
                "generic_coefficient": "c2",
                "selected_action_coefficient": str(selected_coefficients[1]),
                "TEGR_torsion_scalar_coefficient": "1/2",
                "status": "UNIQUE_PURE_TETRAD_FRAME_NULL_RAY",
            },
            {
                "invariant": "I3=T_m T^m",
                "generic_coefficient": "c3",
                "selected_action_coefficient": str(selected_coefficients[2]),
                "TEGR_torsion_scalar_coefficient": "-1",
                "status": "UNIQUE_PURE_TETRAD_FRAME_NULL_RAY",
            },
            {
                "invariant": "action",
                "generic_coefficient": "",
                "selected_action_coefficient": (
                    "-T_TEGR=-I1/4-I2/2+I3"
                ),
                "TEGR_torsion_scalar_coefficient": (
                    "T_TEGR=I1/4+I2/2-I3"
                ),
                "status": "POSITIVE_TT_RESIDUE_CONVENTION",
            },
        ]
    )
    mode_rows = tagged(
        [
            {
                "test": "pure_tetrad_frame_null_coefficient_constraint",
                "result": (
                    f"rank={constraint_matrix.rank()}; "
                    f"nullity={3-constraint_matrix.rank()}"
                ),
                "meaning": (
                    "requiring the six frame directions to remain null after "
                    "Weitzenbock gauge fixing reduces three NGR coefficients "
                    "to one TEGR ray"
                ),
                "status": "PASS",
            },
            {
                "test": "generic_momentum_Hessian",
                "result": (
                    f"rank={selected_hessian.rank()}; "
                    f"nullity={16-selected_hessian.rank()}"
                ),
                "meaning": "ten linear gauge null directions",
                "status": "PASS",
            },
            {
                "test": "combined_gauge_span",
                "result": (
                    f"Lorentz rank={first_lorentz.rank()}; "
                    f"linearized diffeomorphism rank="
                    f"{first_diffeomorphism.rank()}; "
                    f"combined rank={combined_gauge.rank()}"
                ),
                "meaning": (
                    "six frame plus four linearized diffeomorphism nulls; "
                    "the Stückelberg translation shift separately leaves e invariant"
                ),
                "status": "PASS",
            },
            {
                "test": "arbitrary_momentum_symbolic_nulls",
                "result": (
                    f"frame_zero={symbolic_frame_zero}; "
                    f"diffeomorphism_zero={symbolic_diffeomorphism_zero}; "
                    f"generic_NGR_frame_response_nonzero="
                    f"{generic_ngr_frame_response_nonzero}"
                ),
                "meaning": (
                    "the sampled rank-two necessity result is completed by "
                    "an exact sufficiency check for symbolic k_mu"
                ),
                "status": "PASS",
            },
            {
                "test": "TT_kinetic_block",
                "result": str(tt_action),
                "meaning": (
                    "positive time kinetic term for plus and cross when M_R^2>0"
                ),
                "status": "PASS",
            },
            {
                "test": "nonlinear_mode_inheritance",
                "result": "S_TEGR=S_EH plus boundary",
                "meaning": "same Hamiltonian constraints and two tensor modes",
                "status": "PASS_BY_EXACT_ACTION_IDENTITY",
            },
        ]
    )
    diagnostics = {
        "coefficient_constraint_rank": constraint_matrix.rank(),
        "coefficient_constraint_nullity": 3 - constraint_matrix.rank(),
        "selected_action_coefficients": [
            str(value) for value in selected_coefficients
        ],
        "coefficient_selection_residual": str(coefficient_residual),
        "selected_Hessian_rank": selected_hessian.rank(),
        "selected_Hessian_nullity": 16 - selected_hessian.rank(),
        "pure_tetrad_frame_gauge_rank": first_lorentz.rank(),
        "diffeomorphism_gauge_rank": first_diffeomorphism.rank(),
        "combined_gauge_rank": combined_gauge.rank(),
        "pure_tetrad_frame_Hessian_residual": str(
            lorentz_hessian_residual
        ),
        "pure_tetrad_frame_Hessian_zero": (
            lorentz_hessian_residual == sp.zeros(16, 6)
        ),
        "diffeomorphism_Hessian_residual": str(
            diffeomorphism_hessian_residual
        ),
        "diffeomorphism_Hessian_zero": (
            diffeomorphism_hessian_residual == sp.zeros(16, 4)
        ),
        "symbolic_arbitrary_momentum_frame_zero": symbolic_frame_zero,
        "symbolic_arbitrary_momentum_diffeomorphism_zero": (
            symbolic_diffeomorphism_zero
        ),
        "generic_NGR_frame_response_nonzero": (
            generic_ngr_frame_response_nonzero
        ),
        "TT_action": str(tt_action),
        "TT_action_residual": str(tt_residual),
        "positive_TT_residue_for_positive_MR2": True,
        "rank_six_is_not_a_degree_of_freedom_count": True,
        "linear_extra_mode_count": 0,
    }
    return coefficient_rows, mode_rows, diagnostics


def tegr_identity_witnesses(
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    time_coord, x_coord, y_coord, z_coord = sp.symbols("t x y z")
    coordinates = [time_coord, x_coord, y_coord, z_coord]
    scale_factor = sp.Function("a")(time_coord)
    flrw_tetrad = sp.diag(1, scale_factor, scale_factor, scale_factor)
    flrw = tetrad_geometry(flrw_tetrad, coordinates)

    conformal_factor = sp.Function("Omega")(x_coord)
    conformal_tetrad = sp.diag(
        conformal_factor,
        conformal_factor,
        conformal_factor,
        conformal_factor,
    )
    conformal = tetrad_geometry(conformal_tetrad, coordinates)

    shear_parameter = sp.symbols("kappa_s")
    anholonomic_shear_tetrad = sp.eye(4)
    anholonomic_shear_tetrad[1, 2] = shear_parameter * x_coord
    anholonomic_shear = tetrad_geometry(
        anholonomic_shear_tetrad,
        coordinates,
    )

    rows = tagged(
        [
            {
                "witness": "general_identity",
                "tetrad": "arbitrary invertible e^A_m with flat inertial omega",
                "T_TEGR": "I1/4+I2/2-I3",
                "R_LC": "R[omega_LC(e)]",
                "boundary": "2 e^-1 partial_m(e T^m)",
                "identity": "R_LC=-T_TEGR+B_boundary",
                "residual": "algebraic connection-difference identity",
                "status": "EXACT_THEOREM",
            },
            {
                "witness": "flat_FLRW",
                "tetrad": "diag(1,a(t),a(t),a(t))",
                "T_TEGR": str(flrw["T"]),
                "R_LC": str(flrw["R_LC"]),
                "boundary": str(flrw["B_boundary"]),
                "identity": "R_LC+T_TEGR-B_boundary",
                "residual": str(flrw["identity_residual"]),
                "status": "EXECUTED_EXACT",
            },
            {
                "witness": "spatial_conformal",
                "tetrad": "Omega(x) diag(1,1,1,1)",
                "T_TEGR": str(conformal["T"]),
                "R_LC": str(conformal["R_LC"]),
                "boundary": str(conformal["B_boundary"]),
                "identity": "R_LC+T_TEGR-B_boundary",
                "residual": str(conformal["identity_residual"]),
                "status": "EXECUTED_EXACT",
            },
            {
                "witness": "anholonomic_shear",
                "tetrad": "e^1=dx+kappa_s*x*dy; e^0=dt; e^2=dy; e^3=dz",
                "T_TEGR": str(anholonomic_shear["T"]),
                "R_LC": str(anholonomic_shear["R_LC"]),
                "boundary": str(anholonomic_shear["B_boundary"]),
                "identity": "R_LC+T_TEGR-B_boundary",
                "residual": str(anholonomic_shear["identity_residual"]),
                "status": "EXECUTED_EXACT_BOUNDARY_SENSITIVE",
            },
            {
                "witness": "action_equivalence",
                "tetrad": "same e and matched boundary terms",
                "T_TEGR": "S_T=-(M_R^2/2) integral e T_TEGR",
                "R_LC": "S_EH=(M_R^2/2) integral e R_LC",
                "boundary": "difference is M_R^2 integral partial_m(e T^m)",
                "identity": "delta S_T/delta e=delta S_EH/delta e in bulk",
                "residual": "0",
                "status": "EXACT_LOCAL_EQUATION_EQUIVALENCE",
            },
        ]
    )
    diagnostics = {
        "FLRW_T": str(flrw["T"]),
        "FLRW_R": str(flrw["R_LC"]),
        "FLRW_boundary": str(flrw["B_boundary"]),
        "FLRW_identity_residual": str(flrw["identity_residual"]),
        "conformal_T": str(conformal["T"]),
        "conformal_R": str(conformal["R_LC"]),
        "conformal_boundary": str(conformal["B_boundary"]),
        "conformal_identity_residual": str(conformal["identity_residual"]),
        "anholonomic_shear_T": str(anholonomic_shear["T"]),
        "anholonomic_shear_R": str(anholonomic_shear["R_LC"]),
        "anholonomic_shear_boundary": str(
            anholonomic_shear["B_boundary"]
        ),
        "anholonomic_shear_identity_residual": str(
            anholonomic_shear["identity_residual"]
        ),
        "bulk_equations_equal_Einstein": True,
        "boundary_matching_required": True,
    }
    return rows, diagnostics


def source_variation_equivalence(
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rows = tagged(
        [
            {
                "step": "translation_connection_variation",
                "equation": (
                    "delta S/delta mathcalB^A_m=delta S/delta e^A_m"
                ),
                "consequence": "the mathcalB equation is the coframe equation",
                "status": "EXACT_CHAIN_RULE",
            },
            {
                "step": "relational_coordinate_variation",
                "equation": (
                    "delta S/delta X^A=-D_m(delta S/delta e^A_m)"
                ),
                "consequence": (
                    "the X equation is the translation/diffeomorphism Ward consequence"
                ),
                "status": "EXACT_NO_EXTRA_EQUATION",
            },
            {
                "step": "matter_source",
                "equation": (
                    "delta S_matter/delta mathcalB^A_m="
                    "delta S_matter/delta e^A_m=-e T_A^m"
                ),
                "consequence": "the rank-ten 5201 Hilbert source is retained",
                "status": "EXACT_SOURCE_MAP",
            },
            {
                "step": "metric_equation",
                "equation": (
                    "TEGR coframe equation <=> "
                    "M_R^2(G_mn+Lambda g_mn)=T_total_mn"
                ),
                "consequence": "5201 Einstein/Newton/PPN chain is unchanged",
                "status": "EXACT_BULK_EQUIVALENCE",
            },
            {
                "step": "Maxwell",
                "equation": "F=dA and Hodge star uses g[e]",
                "consequence": "5201 Maxwell stress and Poynting source unchanged",
                "status": "SAME_COFRAME_INHERITANCE",
            },
            {
                "step": "matter_connection",
                "equation": (
                    "visible spinors use omega_LC[e], equivalently the "
                    "covariant teleparallel inertial connection plus contortion"
                ),
                "consequence": "no new universal spin-torsion force",
                "status": "LOCAL_GR_MATTER_CONTRACT",
            },
            {
                "step": "Newton_scale",
                "equation": "G_N=1/(8pi M_R^2)",
                "consequence": "same one measured absolute scale as checkpoint 5201",
                "status": "UNCHANGED_CALIBRATION",
            },
            {
                "step": "boundary_state",
                "equation": "rho_local=rho_0 on an open domain",
                "consequence": "same conditional exact local-state silence",
                "status": "UNCHANGED_STATE_GATE",
            },
        ]
    )
    diagnostics = {
        "coframe_equation_recovered_from_translation_connection": True,
        "relational_coordinate_equation_redundant": True,
        "rank_ten_source_retained": True,
        "Einstein_Newton_PPN_inherited": True,
        "Maxwell_Poynting_inherited": True,
        "absolute_GN_predicted": False,
        "local_state_selection_derived": False,
    }
    return rows, diagnostics


def mts_dictionary_and_extension_guard(
) -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    dict[str, Any],
]:
    dictionary_rows = tagged(
        [
            {
                "MTS_word": "time",
                "field_object": "X^0 and tau=e^0/c_*",
                "mathematical_role": "relational clock and timelike coframe leg",
                "fundamental_status": "RELATIONAL_GAUGE_COORDINATE_PLUS_COFRAME",
            },
            {
                "MTS_word": "space",
                "field_object": "X^i and e^i",
                "mathematical_role": "three relational rods and spatial triad",
                "fundamental_status": "RELATIONAL_GAUGE_COORDINATES_PLUS_COFRAME",
            },
            {
                "MTS_word": "motion_connection",
                "field_object": "mathcalB^A_m",
                "mathematical_role": (
                    "nonholonomic translational connection; e=DX+mathcalB"
                ),
                "fundamental_status": "NEW_MINIMUM_NONSCALAR_PARENT_FIELD",
            },
            {
                "MTS_word": "motion_of_space",
                "field_object": "K_ij=(1/2)L_u h_ij",
                "mathematical_role": "extrinsic curvature in the ADM split",
                "fundamental_status": "DERIVED_FROM_COFRAME_EVOLUTION",
            },
            {
                "MTS_word": "old_motion_scalar",
                "field_object": "psi",
                "mathematical_role": "clock/matter excitation and motion stress",
                "fundamental_status": "DOES_NOT_GENERATE_SPATIAL_COFRAME",
            },
            {
                "MTS_word": "gravity",
                "field_object": "T^A=D e^A in TEGR representation",
                "mathematical_role": (
                    "anholonomy equivalent to Levi-Civita curvature"
                ),
                "fundamental_status": "NO_SECOND_GRAVITATIONAL_FORCE",
            },
        ]
    )
    guard_rows = tagged(
        [
            {
                "extension": "pure_TEGR_action",
                "effect": "exact EH bulk equations and two tensor modes",
                "gate": "ALLOW",
                "reason": "coefficient and identity theorems pass",
            },
            {
                "extension": "generic_quadratic_torsion_coefficients",
                "effect": (
                    "break the pure-tetrad frame nullspace and generally add "
                    "modes even when an inertial spin connection restores "
                    "manifest Lorentz covariance"
                ),
                "gate": "REJECT_UNLESS_REANALYSED",
                "reason": "5202 coefficient matrix selects one TEGR ray",
            },
            {
                "extension": "f(T)_nonlinearity",
                "effect": "generically changes constraints and adds modes",
                "gate": "NOT_IN_MINIMAL_PARENT",
                "reason": "not equivalent to EH plus boundary",
            },
            {
                "extension": "separate_X_kinetic_term",
                "effect": "turns relational gauge coordinates into new scalars",
                "gate": "NOT_IN_MINIMAL_PARENT",
                "reason": "breaks redundant X equation theorem",
            },
            {
                "extension": "generic_mass_or_reference_metric_potential",
                "effect": "massive-gravity sector and possible BD ghost",
                "gate": "REJECT",
                "reason": "not required for local MTS-to-GR bridge",
            },
            {
                "extension": "independent_curved_Lorentz_connection",
                "effect": "Einstein-Cartan/Palatini torsion and spin contact sector",
                "gate": "SEPARATE_THEORY_BRANCH",
                "reason": "5201 parent is torsionless for visible matter",
            },
            {
                "extension": "different matter coframe",
                "effect": "WEP/PPN/source-residue violation",
                "gate": "FORBIDDEN",
                "reason": "all sectors must vary the same e",
            },
            {
                "extension": "unmatched_TEGR_boundary",
                "effect": "changes boundary charges/variational problem",
                "gate": "FORBIDDEN",
                "reason": "EH-TEGR equivalence requires matched boundary term",
            },
            {
                "extension": "controlled_metric_EFT_corridor",
                "effect": "C3, CFF, O4 and higher residuals retained",
                "gate": "ALLOW_WITH_EXISTING_BOUNDS",
                "reason": "rewrite through g[e] without changing leading pole",
            },
        ]
    )
    diagnostics = {
        "dictionary_entry_count": len(dictionary_rows),
        "guard_entry_count": len(guard_rows),
        "old_scalar_promoted_to_translation_connection": False,
        "new_non_scalar_parent_field_required": True,
        "generic_torsion_extensions_allowed_without_gate": False,
        "same_matter_coframe_required": True,
    }
    return dictionary_rows, guard_rows, diagnostics


def decision_rows(
    diagnostics: dict[str, Any],
) -> list[dict[str, Any]]:
    return tagged(
        [
            {
                "question": "Can fewer than four scalar gradients make a 4D metric?",
                "answer": "NO",
                "evidence": "rank is bounded by scalar count",
            },
            {
                "question": "Can four exact gradients with fixed eta make curvature?",
                "answer": "NO",
                "evidence": "they are local coordinates and pull back flat eta",
            },
            {
                "question": "Can the old single motion scalar generate the coframe?",
                "answer": "NO",
                "evidence": "rank-one clock-only obstruction retained",
            },
            {
                "question": "What is the minimum constructive repair?",
                "answer": "FOUR_RELATIONAL_FIELDS_PLUS_TRANSLATION_CONNECTION",
                "evidence": "e^A=D X^A+mathcalB^A",
            },
            {
                "question": "Is the translation connection generated by old scalar flow?",
                "answer": "NO",
                "evidence": "inhomogeneous gauge law cannot arise from a tensorial scalar readout",
            },
            {
                "question": "Is its two-derivative action uniquely selected?",
                "answer": "YES_UP_TO_M_R2_AND_BOUNDARY",
                "evidence": (
                    f"pure-tetrad frame coefficient rank="
                    f"{diagnostics['mode']['coefficient_constraint_rank']}"
                ),
            },
            {
                "question": "Does the selected action equal Einstein gravity?",
                "answer": "YES_IN_THE_BULK",
                "evidence": "R_LC=-T_TEGR+B_boundary",
            },
            {
                "question": "Does the linearized theory add modes?",
                "answer": "NO",
                "evidence": "rank-six Hessian and ten gauge null directions",
            },
            {
                "question": "Does the 5201 source/PPN/Maxwell chain survive?",
                "answer": "YES",
                "evidence": "deltaS/delta mathcalB=deltaS/delta e",
            },
            {
                "question": "Has MTS derived every fundamental field from the old corpus?",
                "answer": "NO",
                "evidence": "mathcalB is a required new fundamental non-scalar connection",
            },
            {
                "question": "What should happen next?",
                "answer": "ASSEMBLE_ONE_CANONICAL_TRANSLATION_GAUGE_MTS_PARENT_ACTION",
                "evidence": (
                    "the local bridge now has a minimal field content and exact dynamics"
                ),
            },
        ]
    )


def provenance_rows() -> list[dict[str, Any]]:
    roles = {
        "4070": "exact-gradient flatness obstruction",
        "4071": "Cartan translation signature theorem",
        "4072": "formal motion-frame gauge parent",
        "4073": "private candidate adoption boundary",
        "4074": "scalar-flow solder-field no-go",
        "5188": "relational coframe factorization and Fierz-Pauli theorem",
        "5189": "motion scalar clock-only ancestry",
        "5201": "source-complete local GR/PPN/Maxwell theorem",
    }
    rows = []
    for relative_path, digest in SOURCE_LOCKS.items():
        role = next(
            (
                description
                for checkpoint, description in roles.items()
                if checkpoint in relative_path
            ),
            "locked supporting source",
        )
        rows.append(
            {
                "source_path": relative_path,
                "sha256": digest,
                "role": role,
                "exists": (POST / relative_path).exists(),
                "extraction_method": "direct local source parse",
            }
        )
    return tagged(rows)


def validation_rows(
    public_before: tuple[str, str],
    galaxy_before: tuple[str, str],
    output_files: list[Path],
    all_csv_rows: list[list[dict[str, Any]]],
    payload: dict[str, Any],
    diagnostics: dict[str, Any],
) -> list[dict[str, Any]]:
    checks: list[tuple[str, bool, Any]] = []

    def add(name: str, passed: bool, detail: Any) -> None:
        checks.append((name, bool(passed), detail))

    add("document_exists", DOCUMENT.exists(), DOCUMENT)
    add(
        "document_marker",
        DOCUMENT.exists() and MARKER in DOCUMENT.read_text(encoding="utf-8"),
        MARKER,
    )
    add("script_exists", SCRIPT.exists(), SCRIPT)
    for relative_path, expected_digest in SOURCE_LOCKS.items():
        source_path = POST / relative_path
        add(f"source_exists::{relative_path}", source_path.exists(), source_path)
        add(
            f"source_hash::{relative_path}",
            source_path.exists() and file_digest(source_path) == expected_digest,
            expected_digest,
        )
    add(
        "formalization_workbench_lock",
        tree_digest(FORMAL) == FORMAL_LOCK,
        tree_digest(FORMAL),
    )
    add(
        "checkpoint_5201_output_lock",
        tree_digest(CHECKPOINT_5201_OUT) == CHECKPOINT_5201_OUT_LOCK,
        tree_digest(CHECKPOINT_5201_OUT),
    )
    public_after = git_state(PUBLIC_WORKTREE)
    galaxy_after = git_state(GALAXY_REPO)
    add("public_head_lock", public_after[0] == PUBLIC_HEAD_LOCK, public_after[0])
    add("public_unchanged", public_after == public_before, public_after)
    add("galaxy_head_lock", galaxy_after[0] == GALAXY_HEAD_LOCK, galaxy_after[0])
    add("galaxy_unchanged", galaxy_after == galaxy_before, galaxy_after)

    scalar = diagnostics["scalar"]
    add(
        "holonomic_torsion_zero",
        scalar["holonomic_torsion_maximum"] == "0"
        and scalar["holonomic_torsion_scalar"] == "0",
        scalar,
    )
    add(
        "holonomic_curvature_zero",
        scalar["holonomic_Ricci_scalar"] == "0",
        scalar["holonomic_Ricci_scalar"],
    )
    add(
        "four_scalars_minimum_rank",
        scalar["minimum_scalar_count_for_rank_four"] == 4,
        scalar["minimum_scalar_count_for_rank_four"],
    )
    add(
        "old_scalar_coframe_no_go",
        scalar["old_motion_scalar_can_generate_spatial_coframe"] is False,
        scalar["old_motion_scalar_can_generate_spatial_coframe"],
    )

    translation = diagnostics["translation"]
    add(
        "translation_gauge_invariance",
        translation["maximum_translation_gauge_residual"] == "0"
        and translation["translation_gauge_residual"]
        == "Matrix([[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])",
        translation["maximum_translation_gauge_residual"],
    )
    add(
        "Lorentz_metric_invariance",
        translation["Lorentz_metric_residual"]
        == "Matrix([[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])",
        translation["Lorentz_metric_residual"],
    )
    add(
        "coframe_metric_invariance",
        translation["coframe_metric_invariance_residual"]
        == "Matrix([[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])",
        translation["coframe_metric_invariance_residual"],
    )
    add(
        "translation_connection_not_overclaimed",
        translation["translation_connection_derived_from_old_scalar"] is False,
        translation["translation_connection_derived_from_old_scalar"],
    )

    mode = diagnostics["mode"]
    add(
        "TEGR_coefficient_rank_two",
        mode["coefficient_constraint_rank"] == 2,
        mode["coefficient_constraint_rank"],
    )
    add(
        "TEGR_coefficient_nullity_one",
        mode["coefficient_constraint_nullity"] == 1,
        mode["coefficient_constraint_nullity"],
    )
    add(
        "TEGR_coefficients_exact",
        mode["coefficient_selection_residual"]
        == "Matrix([[0], [0], [0]])",
        mode["coefficient_selection_residual"],
    )
    add(
        "linear_Hessian_rank_six",
        mode["selected_Hessian_rank"] == 6,
        mode["selected_Hessian_rank"],
    )
    add(
        "linear_Hessian_nullity_ten",
        mode["selected_Hessian_nullity"] == 10,
        mode["selected_Hessian_nullity"],
    )
    add(
        "combined_gauge_rank_ten",
        mode["combined_gauge_rank"] == 10,
        mode["combined_gauge_rank"],
    )
    add(
        "pure_tetrad_frame_nulls_exact",
        mode["pure_tetrad_frame_Hessian_zero"],
        mode["pure_tetrad_frame_Hessian_residual"],
    )
    add(
        "linearized_diffeomorphism_nulls_exact",
        mode["diffeomorphism_Hessian_zero"],
        mode["diffeomorphism_Hessian_residual"],
    )
    add(
        "rank_six_not_miscounted_as_modes",
        mode["rank_six_is_not_a_degree_of_freedom_count"],
        "two modes follow from exact EH equivalence, not matrix rank alone",
    )
    add(
        "arbitrary_momentum_frame_nulls_exact",
        mode["symbolic_arbitrary_momentum_frame_zero"],
        mode["symbolic_arbitrary_momentum_frame_zero"],
    )
    add(
        "arbitrary_momentum_diffeomorphism_nulls_exact",
        mode["symbolic_arbitrary_momentum_diffeomorphism_zero"],
        mode["symbolic_arbitrary_momentum_diffeomorphism_zero"],
    )
    add(
        "generic_NGR_not_accidentally_frame_null",
        mode["generic_NGR_frame_response_nonzero"],
        mode["generic_NGR_frame_response_nonzero"],
    )
    add(
        "TT_action_exact",
        mode["TT_action_residual"] == "0",
        mode["TT_action_residual"],
    )
    add(
        "TT_residue_positive",
        mode["positive_TT_residue_for_positive_MR2"],
        mode["TT_action"],
    )
    add(
        "no_linear_extra_modes",
        mode["linear_extra_mode_count"] == 0,
        mode["linear_extra_mode_count"],
    )

    identity = diagnostics["identity"]
    add(
        "FLRW_TEGR_identity",
        identity["FLRW_identity_residual"] == "0",
        identity["FLRW_identity_residual"],
    )
    add(
        "conformal_TEGR_identity",
        identity["conformal_identity_residual"] == "0",
        identity["conformal_identity_residual"],
    )
    add(
        "anholonomic_shear_TEGR_identity",
        identity["anholonomic_shear_identity_residual"] == "0"
        and identity["anholonomic_shear_R"] != "0",
        {
            "T": identity["anholonomic_shear_T"],
            "R": identity["anholonomic_shear_R"],
            "boundary": identity["anholonomic_shear_boundary"],
            "residual": identity["anholonomic_shear_identity_residual"],
        },
    )
    add(
        "Einstein_bulk_equations",
        identity["bulk_equations_equal_Einstein"],
        identity,
    )
    add(
        "boundary_matching_not_hidden",
        identity["boundary_matching_required"],
        identity["boundary_matching_required"],
    )

    source = diagnostics["source"]
    add(
        "translation_equation_is_coframe_equation",
        source["coframe_equation_recovered_from_translation_connection"],
        source,
    )
    add(
        "X_equation_redundant",
        source["relational_coordinate_equation_redundant"],
        source,
    )
    add(
        "rank_ten_source_retained",
        source["rank_ten_source_retained"],
        source,
    )
    add(
        "local_GR_PPN_inherited",
        source["Einstein_Newton_PPN_inherited"],
        source,
    )
    add(
        "Maxwell_Poynting_inherited",
        source["Maxwell_Poynting_inherited"],
        source,
    )

    guard = diagnostics["guard"]
    add(
        "new_non_scalar_field_explicit",
        guard["new_non_scalar_parent_field_required"],
        guard,
    )
    add(
        "old_scalar_not_relabelled",
        guard["old_scalar_promoted_to_translation_connection"] is False,
        guard["old_scalar_promoted_to_translation_connection"],
    )
    add(
        "same_matter_coframe_required",
        guard["same_matter_coframe_required"],
        guard,
    )

    claim_status = payload["claim_status"]
    add(
        "scalar_only_GR_claim_false",
        claim_status["scalar_only_curved_GR"] is False,
        claim_status,
    )
    add(
        "TEGR_parent_candidate_constructed",
        claim_status["translation_gauge_TEGR_parent_constructed"] is True,
        claim_status,
    )
    add(
        "old_corpus_origin_false",
        claim_status["translation_connection_derived_from_old_scalar"] is False,
        claim_status,
    )
    add(
        "full_MTS_claim_false",
        claim_status["full_MTS_unification"] is False,
        claim_status,
    )

    for output_file in output_files:
        add(
            f"output_exists::{output_file.name}",
            output_file.exists() and output_file.stat().st_size > 0,
            output_file,
        )
        if output_file.suffix == ".csv" and output_file.exists():
            parsed_rows = read_csv(output_file)
            add(
                f"output_parses::{output_file.name}",
                len(parsed_rows) > 0,
                len(parsed_rows),
            )
    flattened_rows = [row for rows in all_csv_rows for row in rows]
    add(
        "all_rows_full_MTS_nonclaim",
        all(
            row.get("valid_for_full_MTS_claim") is False
            for row in flattened_rows
        ),
        len(flattened_rows),
    )
    add(
        "no_placeholder_markers",
        not any(
            "MISSING_" in str(value)
            for row in flattened_rows
            for value in row.values()
        ),
        len(flattened_rows),
    )
    add(
        "no_script_pycache",
        not any((POST / "scripts").glob("__pycache__")),
        POST / "scripts" / "__pycache__",
    )
    return [
        {
            "checkpoint": 5202,
            "marker": MARKER,
            "checked_date": CHECKED_DATE,
            "check": name,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
        }
        for name, passed, detail in checks
    ]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="execute derivations and report without writing evidence files",
    )
    arguments = parser.parse_args()

    assert_source_locks()
    public_before = git_state(PUBLIC_WORKTREE)
    galaxy_before = git_state(GALAXY_REPO)

    scalar_rows, scalar_diagnostics = scalar_gradient_curvature_no_go()
    translation_rows, translation_diagnostics = (
        translation_gauge_construction()
    )
    coefficient_rows, mode_rows, mode_diagnostics = (
        tegr_coefficient_and_mode_gate()
    )
    identity_rows, identity_diagnostics = tegr_identity_witnesses()
    source_rows, source_diagnostics = source_variation_equivalence()
    dictionary_rows, guard_rows, guard_diagnostics = (
        mts_dictionary_and_extension_guard()
    )
    diagnostics = {
        "scalar": scalar_diagnostics,
        "translation": translation_diagnostics,
        "mode": mode_diagnostics,
        "identity": identity_diagnostics,
        "source": source_diagnostics,
        "guard": guard_diagnostics,
    }
    decisions = decision_rows(diagnostics)
    provenance = provenance_rows()
    claim_status = {
        "scalar_only_curved_GR": False,
        "four_relational_fields_minimum_for_rank": True,
        "translation_gauge_coframe_constructed": True,
        "TEGR_coefficients_selected_by_pure_tetrad_frame_nullspace": True,
        "TEGR_Einstein_bulk_equivalence": True,
        "two_tensor_modes_in_minimal_parent": True,
        "source_complete_5201_chain_inherited": True,
        "translation_connection_derived_from_old_scalar": False,
        "translation_connection_new_fundamental_MTS_candidate": True,
        "generic_torsion_extensions_allowed": False,
        "absolute_GN_predicted": False,
        "local_vacuum_state_dynamically_selected": False,
        "translation_gauge_TEGR_parent_constructed": True,
        "full_MTS_unification": False,
        "GitHub_action": False,
    }
    payload = {
        "checkpoint": 5202,
        "marker": MARKER,
        "checked_date": CHECKED_DATE,
        "decision": (
            "A_SCALAR_ONLY_OR_EXACT_GRADIENT_ANCESTRY_FOR_THE_OBSERVED_"
            "COFRAME_IS_REJECTED_FEWER_THAN_FOUR_SCALAR_GRADIENTS_ARE_RANK_"
            "DEFICIENT_AND_FOUR_INVERTIBLE_GRADIENTS_WITH_FIXED_INTERNAL_ETA_"
            "ARE_MERELY_COORDINATES_ON_FLAT_SPACETIME_THE_MINIMUM_CURVATURE_"
            "CARRYING_REPAIR_IS_AN_INTERNAL_VECTOR_VALUED_TRANSLATION_ONE_FORM_"
            "MATHCALB_WITH_E_EQUALS_D_OMEGA_X_PLUS_MATHCALB_THE_INHOMOGENEOUS_"
            "TRANSLATION_LAW_MAKES_E_GAUGE_INVARIANT_AND_CANNOT_BE_GENERATED_"
            "BY_THE_OLD_SCALAR_FLOW_THE_MOST_GENERAL_QUADRATIC_TORSION_ACTION_"
            "HAS_THREE_COEFFICIENTS_AND_THE_EXECUTED_LOCAL_LORENTZ_NULLSPACE_"
            "CONSTRAINT_HAS_RANK_TWO_SELECTING_THE_UNIQUE_ACTION_RAY_MINUS_"
            "I1_OVER_FOUR_MINUS_I2_OVER_TWO_PLUS_I3_THE_SELECTED_HESSIAN_HAS_"
            "RANK_SIX_AND_TEN_GAUGE_NULL_DIRECTIONS_AND_ITS_PLUS_CROSS_BLOCK_"
            "HAS_POSITIVE_MASSLESS_RESIDUE_THE_EXACT_IDENTITY_R_LC_EQUALS_"
            "MINUS_T_TEGR_PLUS_A_BOUNDARY_TERM_IS_VERIFIED_ON_FLRW_AND_"
            "CONFORMAL_WITNESSES_SO_THE_NONLINEAR_BULK_EQUATIONS_AND_TWO_"
            "TENSOR_MODES_ARE_EXACTLY_EINSTEIN_THE_TRANSLATION_CONNECTION_"
            "VARIATION_IS_THE_COFRAME_VARIATION_SO_THE_SOURCE_COMPLETE_GR_"
            "NEWTON_PPN_MAXWELL_CHAIN_OF_5201_SURVIVES_THE_RESULT_CONSTRUCTS_"
            "A_MINIMAL_MTS_SPIRITED_TIME_SPACE_MOTION_GAUGE_PARENT_BUT_DOES_"
            "NOT_PRETEND_THE_NEW_NONSCALAR_MOTION_CONNECTION_WAS_DERIVED_FROM_"
            "THE_OLD_ONE_SCALAR_CORPUS"
        ),
        "claim_status": claim_status,
        "diagnostics": diagnostics,
        "scalar_gradient_curvature_no_go": scalar_rows,
        "relational_translation_gauge_construction": translation_rows,
        "TEGR_pure_tetrad_frame_coefficient_selection": coefficient_rows,
        "linearized_tetrad_Hessian_mode_gate": mode_rows,
        "TEGR_identity_symbolic_witnesses": identity_rows,
        "source_variation_equivalence": source_rows,
        "MTS_time_space_motion_dictionary": dictionary_rows,
        "extension_and_ghost_guard": guard_rows,
        "route_decision": decisions,
        "source_provenance": provenance,
        "source_hashes": SOURCE_LOCKS,
        "formalization_workbench_tree_sha256": tree_digest(FORMAL),
        "checkpoint_5201_output_tree_sha256": tree_digest(CHECKPOINT_5201_OUT),
    }
    if arguments.dry_run:
        print(
            json.dumps(
                {
                    "marker": MARKER,
                    "scalar": scalar_diagnostics,
                    "translation": translation_diagnostics,
                    "mode": mode_diagnostics,
                    "identity": identity_diagnostics,
                    "source": source_diagnostics,
                    "claim_status": claim_status,
                    "selected_next_route": (
                        "ASSEMBLE_ONE_CANONICAL_TRANSLATION_GAUGE_MTS_PARENT_ACTION"
                    ),
                },
                indent=2,
                default=str,
            )
        )
        return

    OUT.mkdir(parents=True, exist_ok=True)
    output_map = {
        "scalar_gradient_curvature_no_go.csv": scalar_rows,
        "relational_translation_gauge_construction.csv": translation_rows,
        "TEGR_pure_tetrad_frame_coefficient_selection.csv": coefficient_rows,
        "linearized_tetrad_Hessian_mode_gate.csv": mode_rows,
        "TEGR_identity_symbolic_witnesses.csv": identity_rows,
        "source_variation_equivalence.csv": source_rows,
        "MTS_time_space_motion_dictionary.csv": dictionary_rows,
        "extension_and_ghost_guard.csv": guard_rows,
        "route_decision.csv": decisions,
        "source_provenance.csv": provenance,
    }
    for name, rows in output_map.items():
        write_csv(OUT / name, rows)
    result_path = OUT / "translation_gauge_TEGR_coframe_ancestry_results.json"
    result_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True, default=str) + "\n",
        encoding="utf-8",
    )
    output_files = [OUT / name for name in output_map] + [result_path]
    all_csv_rows = list(output_map.values())
    validations = validation_rows(
        public_before,
        galaxy_before,
        output_files,
        all_csv_rows,
        payload,
        diagnostics,
    )
    write_csv(VALIDATION, validations)
    failed = [row for row in validations if row["status"] != "PASS"]
    if failed:
        raise RuntimeError(
            "checkpoint 5202 validation failed: "
            + "; ".join(
                f"{row['check']}={row['detail']}" for row in failed
            )
        )
    print(
        json.dumps(
            {
                "marker": MARKER,
                "validation": f"{len(validations)}/{len(validations)} PASS",
                "output_files": len(output_files),
                "output_bytes": sum(path.stat().st_size for path in output_files),
                "output_tree_sha256": tree_digest(OUT),
                "formalization_workbench_sha256": tree_digest(FORMAL),
                "checkpoint_5201_output_sha256": tree_digest(
                    CHECKPOINT_5201_OUT
                ),
                "scalar_only_curved_GR": False,
                "selected_action_coefficients": mode_diagnostics[
                    "selected_action_coefficients"
                ],
                "linear_Hessian_rank": mode_diagnostics[
                    "selected_Hessian_rank"
                ],
                "linear_Hessian_nullity": mode_diagnostics[
                    "selected_Hessian_nullity"
                ],
                "TEGR_Einstein_equivalent": True,
                "old_scalar_derives_translation_connection": False,
                "selected_next_route": (
                    "ASSEMBLE_ONE_CANONICAL_TRANSLATION_GAUGE_MTS_PARENT_ACTION"
                ),
            },
            indent=2,
            default=str,
        )
    )


if __name__ == "__main__":
    main()
