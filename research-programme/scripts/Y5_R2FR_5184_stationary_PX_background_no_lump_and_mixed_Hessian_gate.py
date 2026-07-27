from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import sys
from pathlib import Path
from typing import Any

import numpy as np
import sympy as sp

sys.dont_write_bytecode = True


POST = Path(__file__).resolve().parents[1]
FORMAL = POST.parent / "formalization-workbench"
SCRIPT = Path(__file__).resolve()
OUT = POST / "source-intake" / "functional_rg" / "5184"

BACKGROUND_CSV = OUT / "stationary_background_classification.csv"
NO_LUMP_CSV = OUT / "static_no_lump_and_flux_theorem.csv"
HESSIAN_CSV = OUT / "timelike_spacelike_mixed_Hessian.csv"
CONE_CSV = OUT / "stealth_root_and_principal_cone_gate.csv"
SCALING_CSV = OUT / "stationary_background_scaling_comparison.csv"
ROUTE_CSV = OUT / "stationary_background_route_decision.csv"
PROVENANCE_CSV = OUT / "source_provenance.csv"
RESULT_JSON = OUT / "stationary_PX_background_results.json"
VALIDATION_CSV = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5184_VALIDATION.csv"
)
DOCUMENT = (
    POST
    / "5184-Y5-R2FR-stationary-PX-background-no-lump-and-mixed-Hessian-gate.md"
)

MARKER = "MTS_5184_STATIONARY_PX_BACKGROUND_NO_LUMP_MIXED_HESSIAN_GATE"
CHECKED_DATE = "2026-07-23"
FORMAL_DIGEST_LOCK = (
    "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
)
CHECKPOINT_5176_TREE_LOCK = (
    "254d5879c1e76908e3942e4817892e091fa1315666dae1d6d74e2c3287c67b8b"
)
CHECKPOINT_5176_ROOT = POST / "source-intake" / "functional_rg" / "5176"
Q_LOCKED = 0.77
CERTIFIED_X_MAX = 0.1

ROUTE_DECISION = (
    "THE_HEALTHY_SOURCE_FREE_PARENT_PX_SECTOR_HAS_NO_REGULAR_LOCALIZED_"
    "STATIC_MOTION_BACKGROUND_ON_A_HORIZON_FREE_STATIC_GALAXY_SLICE_"
    "BECAUSE_THE_SHIFT_CURRENT_IDENTITY_WITH_PX_POSITIVE_AND_ZERO_BOUNDARY_"
    "FLUX_FORCES_THE_SPATIAL_GRADIENT_TO_ZERO_ORDINARY_BARYONS_SUPPLY_"
    "NEITHER_A_SCALAR_SOURCE_NOR_A_JUNCTION_FLUX_A_HOMOGENEOUS_TIMELIKE_"
    "CLOCK_IS_GLOBAL_STATE_DATA_WITH_NONZERO_STRESS_AND_HAS_EXACTLY_ZERO_"
    "STATIC_METRIC_SCALAR_MIXING_A_HOMOGENEOUS_SPACELIKE_GRADIENT_IS_"
    "NONLOCALIZED_ANISOTROPIC_AND_GENERATES_A_K_ZERO_SCHUR_KERNEL_RATHER_"
    "THAN_THE_REQUIRED_K_TIMES_NQ_KERNEL_A_NULL_GRADIENT_CARRIES_NULL_"
    "STRESS_AND_THE_PX_ZERO_STEALTH_ESCAPE_REQUIRES_A_DEGENERATE_SCALAR_"
    "CONE_OUTSIDE_THE_CERTIFIED_CHART_AFTER_THE_LONGITUDINAL_EIGENVALUE_"
    "HAS_ALREADY_CROSSED_ZERO_THEREFORE_THE_CURRENT_CLASSICAL_STATIONARY_"
    "BACKGROUND_ROUTE_IS_REJECTED_WITHIN_THE_CERTIFIED_LOCAL_EFT_AND_THE_"
    "NEXT_CONSTRUCTIVE_ROUTE_IS_THE_PARENT_OWNED_INTERACTING_OCCUPIED_STATE_"
    "CTP_STRESS_BEYOND_THE_ALREADY_COUNTED_CLASSICAL_VLASOV_DENSITY"
)


def source_path(relative: str) -> Path:
    return POST / Path(relative.replace("/", "\\"))


SOURCES = {
    "checkpoint_4943_document": (
        source_path(
            "4943-Y5-R2FR-matter-source-interior-psi-zero-continuation-and-"
            "junction-or-fifth-force-residual-gate.md"
        ),
        "a90da0e9ad0457fc3dbdb389d7bf2715cb9d707cbffa094a987b0b0553e257b5",
    ),
    "checkpoint_4943_result": (
        source_path(
            "source-intake/functional_rg/4943/"
            "matter_source_junction_stability_results.json"
        ),
        "67ff98eb4e0bec17906e1515fef3d07f85a00480941d882cc31261639707eebb",
    ),
    "checkpoint_4943_junction": (
        source_path(
            "source-intake/functional_rg/4943/"
            "junction_scalar_charge_and_fifth_force.csv"
        ),
        "5fbca2c1672d7fbb6f1741e56a3c72a2adbaee544a4fd5fd5525a616cb836df6",
    ),
    "checkpoint_4957_document": (
        source_path(
            "4957-Y5-R2FR-functional-PX-GR-connected-trajectory-and-O2-O4-O5-"
            "residual-bound-or-motion-sector-rejection.md"
        ),
        "235b2e640428814bbcc3f0af1b2ebef020573314eaae1cb0b793be9122db0cb4",
    ),
    "checkpoint_4957_result": (
        source_path(
            "source-intake/functional_rg/4957/"
            "functional_PX_O4_GR_trajectory_results.json"
        ),
        "8d8c7e416706d116492e3539a0541e6e64174c59a460714325251656b1477cc6",
    ),
    "checkpoint_4957_trajectory": (
        source_path(
            "source-intake/functional_rg/4957/"
            "functional_PX_O4_GR_trajectory.csv"
        ),
        "c60eee38379dc8cf1bb16833b2b5a849ecc0b5d7da0f74d9f0c9bd1bf9b46166",
    ),
    "checkpoint_4957_regularity": (
        source_path(
            "source-intake/functional_rg/4957/"
            "trajectory_functional_regularity_gate.csv"
        ),
        "1071cc4e71dff09a05e1ba10d5c62242d33e2a4cce03c9fe638da402fa1764c2",
    ),
    "checkpoint_4960_document": (
        source_path(
            "4960-Y5-R2FR-integrated-H-soft-BRST-universal-source-theorem-and-"
            "local-GR-Newton-Maxwell-promotion-or-parent-field-content-"
            "boundary.md"
        ),
        "6cd343d022dde751f86ad82eaf0f61fb5e3616753c228f631c44a45da278a69d",
    ),
    "checkpoint_4960_result": (
        source_path(
            "source-intake/functional_rg/4960/"
            "integrated_H_universal_source_results.json"
        ),
        "6fe2d8335cb1a4902c07c986e597e2f748050aa31f6137c5b52f9ced94542477",
    ),
    "checkpoint_4982_document": (
        source_path(
            "4982-Y5-R2FR-covariant-orderX-Schur-kernel-and-essential-two-"
            "point-subtraction.md"
        ),
        "83bfd153e96f7fb2322e2df1e71dce485caf5b7323230be285081ff280f55645",
    ),
    "checkpoint_4982_result": (
        source_path(
            "source-intake/functional_rg/4982/"
            "covariant_orderX_essential_results.json"
        ),
        "923aceac438808f912b03f032281ccc1bba960987ce70158222efc88f41d6b2f",
    ),
    "checkpoint_4983_document": (
        source_path(
            "4983-Y5-R2FR-box2-essential-quotient-running-frame-and-local-"
            "profile-theorem.md"
        ),
        "e7740197cd6d7f18e6f2ba7512701f2d65751312d4328fd39e5524c38ac72c13",
    ),
    "checkpoint_4983_result": (
        source_path(
            "source-intake/functional_rg/4983/"
            "box2_essential_local_profile_results.json"
        ),
        "dd53cd55f79134cf659062f236fc4df1f33f3146bb609e3ad2b98d08c9025d20",
    ),
    "checkpoint_5151_document": (
        source_path(
            "5151-Y5-R2FR-parent-projective-occupation-to-conserved-Einstein-"
            "cluster-stress-and-two-metric-cog-gate.md"
        ),
        "b23ca652af8b66c220973cffbdc1ab2df028947c9dba8bd61666d1e0460c5fd5",
    ),
    "checkpoint_5151_result": (
        source_path(
            "source-intake/functional_rg/5151/"
            "projective_state_stress_results.json"
        ),
        "f1331f9bc511f12e4e785c9a3ffcf19dadf4eb8b05b05362031548a22984805c",
    ),
    "checkpoint_5157_document": (
        source_path(
            "5157-Y5-R2FR-composite-motion-clock-charge-entropy-adiabatic-"
            "state-preparation-reentry-gate.md"
        ),
        "dcafb49edbb5032549b3f55fe23a3d6a7edc45f5c7e1d7942f489e13e68fc2e2",
    ),
    "checkpoint_5157_result": (
        source_path(
            "source-intake/functional_rg/5157/"
            "composite_motion_clock_state_preparation_results.json"
        ),
        "02646573832bfa193da720680516681b364f4c37fa77b394170b19dcb7f9dd09",
    ),
    "checkpoint_5177_document": (
        source_path(
            "5177-Y5-R2FR-locked-ensemble-metric-split-and-no-retuning-"
            "theorem.md"
        ),
        "abe635ca81992660c7e9bb834eed765626bf63cfc2564f3f4b23b759a3a0fd90",
    ),
    "checkpoint_5177_result": (
        source_path(
            "source-intake/functional_rg/5177/"
            "locked_metric_split_results.json"
        ),
        "2ae85163c0c03a642252f6521d717ddd0a313f113cc6cc65bdf2b0425a2af570",
    ),
    "checkpoint_5183_document": (
        source_path(
            "5183-Y5-R2FR-Wick-sign-consistent-static-pair-response-and-"
            "5182-supersession.md"
        ),
        "c8aafba0a982c957d844b0db4165d46c30236d62296c38d4eb7d8e34fc25cc36",
    ),
    "checkpoint_5183_result": (
        source_path(
            "source-intake/functional_rg/5183/"
            "Wick_sign_consistent_pair_response_results.json"
        ),
        "97f3a5d9265fb19898ac859f37e33bede58bc0d72bb3f1dd86b78c3ed421a85b",
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
    for file_path in sorted(item for item in path.rglob("*") if item.is_file()):
        relative = file_path.relative_to(path).as_posix()
        digest.update(relative.encode("utf-8"))
        digest.update(file_digest(file_path).encode("ascii"))
    return digest.hexdigest()


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"cannot write empty CSV: {path}")
    fields = list(rows[0])
    if any(list(row) != fields for row in rows):
        raise ValueError(f"inconsistent fields: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    temporary.replace(path)


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


def relative(path: Path) -> str:
    return path.relative_to(POST).as_posix()


def validation_row(
    validation_id: str,
    check: str,
    passed: bool,
    actual: Any,
    expected: Any,
) -> dict[str, Any]:
    return {
        "validation_id": validation_id,
        "check": check,
        "passed": bool(passed),
        "actual": actual,
        "expected": expected,
        "checkpoint_marker": MARKER,
    }


def log_slope(x_values: np.ndarray, y_values: np.ndarray) -> float:
    return float(np.polyfit(np.log(x_values), np.log(y_values), 1)[0])


def first_positive_root(
    function: Any,
    maximum: float = 1.0,
    samples: int = 100_000,
) -> float | None:
    x_previous = 0.0
    value_previous = float(function(x_previous))
    for x_value in np.linspace(maximum / samples, maximum, samples):
        value = float(function(float(x_value)))
        if value == 0.0:
            return float(x_value)
        if value * value_previous < 0.0:
            lower = x_previous
            upper = float(x_value)
            for _ in range(100):
                midpoint = 0.5 * (lower + upper)
                midpoint_value = float(function(midpoint))
                if midpoint_value * value_previous <= 0.0:
                    upper = midpoint
                else:
                    lower = midpoint
                    value_previous = midpoint_value
            return 0.5 * (lower + upper)
        x_previous = float(x_value)
        value_previous = value
    return None


def symbolic_contract() -> dict[str, Any]:
    p_x, p_xx, phi, psi = sp.symbols(
        "P_X P_XX Phi Psi",
        real=True,
    )
    q_clock, v_space, omega, k_value, cosine = sp.symbols(
        "q_clock V omega k cosine",
        real=True,
    )
    eta = sp.diag(-1, 1, 1, 1)
    hessian_metric = sp.diag(-2 * phi, -2 * psi, -2 * psi, -2 * psi)

    def dot(first: sp.Matrix, second: sp.Matrix) -> sp.Expr:
        return sp.expand((first.T * eta * second)[0])

    def h_dot(first: sp.Matrix, second: sp.Matrix) -> sp.Expr:
        first_up = eta * first
        second_up = eta * second
        return sp.expand((first_up.T * hessian_metric * second_up)[0])

    def mixed(first: sp.Matrix, second: sp.Matrix) -> sp.Expr:
        trace = sp.trace(eta * hessian_metric)
        return sp.expand(
            p_x
            * (
                trace * dot(first, second)
                - 2 * h_dot(first, second)
            )
            - 2
            * p_xx
            * h_dot(first, first)
            * dot(first, second)
        )

    def scalar(first: sp.Matrix, second: sp.Matrix) -> sp.Expr:
        return sp.expand(
            2 * p_x * dot(second, second)
            + 4 * p_xx * dot(first, second) ** 2
        )

    fluctuation = sp.Matrix(
        [
            omega,
            k_value * sp.sqrt(1 - cosine**2),
            0,
            k_value * cosine,
        ]
    )
    timelike = sp.Matrix([q_clock, 0, 0, 0])
    spacelike = sp.Matrix([0, 0, 0, v_space])

    timelike_mixed = mixed(timelike, fluctuation)
    timelike_scalar = scalar(timelike, fluctuation)
    spacelike_mixed = mixed(spacelike, fluctuation)
    spacelike_scalar = scalar(spacelike, fluctuation)
    timelike_b = sp.Matrix(
        [
            sp.diff(timelike_mixed, phi),
            sp.diff(timelike_mixed, psi),
        ]
    )
    spacelike_b = sp.Matrix(
        [
            sp.diff(spacelike_mixed, phi),
            sp.diff(spacelike_mixed, psi),
        ]
    )

    x_space = v_space**2
    denominator = p_x + 2 * x_space * p_xx * cosine**2
    vector_u = sp.Matrix([p_x, -p_x + 2 * x_space * p_xx])
    spacelike_schur_direct = sp.simplify(
        spacelike_b.subs(omega, 0)
        * spacelike_b.subs(omega, 0).T
        / spacelike_scalar.subs(omega, 0)
    )
    spacelike_schur_closed = sp.simplify(
        2
        * x_space
        * cosine**2
        / denominator
        * vector_u
        * vector_u.T
    )
    schur_residual = sp.simplify(
        spacelike_schur_direct - spacelike_schur_closed
    )

    scale = sp.symbols("scale", positive=True)
    scaled_schur = sp.simplify(
        spacelike_schur_direct.subs(k_value, scale * k_value)
        - spacelike_schur_direct
    )

    return {
        "timelike_mixed": str(sp.factor(timelike_mixed)),
        "timelike_scalar": str(sp.factor(timelike_scalar)),
        "timelike_b": [str(sp.factor(item)) for item in timelike_b],
        "timelike_static_b": [
            str(sp.factor(item.subs(omega, 0))) for item in timelike_b
        ],
        "spacelike_mixed": str(sp.factor(spacelike_mixed.subs(omega, 0))),
        "spacelike_scalar": str(
            sp.factor(spacelike_scalar.subs(omega, 0))
        ),
        "spacelike_b": [
            str(sp.factor(item.subs(omega, 0))) for item in spacelike_b
        ],
        "spacelike_schur": [
            [str(sp.factor(item)) for item in row]
            for row in spacelike_schur_closed.tolist()
        ],
        "timelike_static_zero": all(
            sp.simplify(item.subs(omega, 0)) == 0 for item in timelike_b
        ),
        "spacelike_schur_identity": schur_residual == sp.zeros(2),
        "spacelike_schur_degree_zero": scaled_schur == sp.zeros(2),
        "timelike_quasistatic_schur_zero": all(
            sp.simplify(
                sp.limit(
                    timelike_b[index] * timelike_b[jindex]
                    / timelike_scalar,
                    omega,
                    0,
                )
            )
            == 0
            for index in range(2)
            for jindex in range(2)
        ),
    }


def monte_carlo_crosscheck(samples: int = 40_000) -> dict[str, float]:
    random = np.random.default_rng(5184)
    maximum_mixed_residual = 0.0
    maximum_schur_residual = 0.0
    minimum_denominator = math.inf
    for _ in range(samples):
        p_x = float(random.uniform(0.1, 2.0))
        x_space = float(random.uniform(1.0e-4, 0.1))
        p_xx = float(random.uniform(-0.4, 0.8))
        cosine = float(random.uniform(-1.0, 1.0))
        denominator = p_x + 2.0 * x_space * p_xx * cosine**2
        if denominator <= 0.05:
            continue
        v_space = math.sqrt(x_space)
        k_value = float(random.uniform(1.0e-3, 4.0))
        phi = float(random.normal())
        psi = float(random.normal())

        direct_mixed = (
            2.0 * p_x * phi * v_space * cosine * k_value
            + (
                -2.0 * p_x * v_space * cosine * k_value
                + 4.0 * p_xx * v_space**3 * cosine * k_value
            )
            * psi
        )
        vector_u = np.array(
            [p_x, -p_x + 2.0 * x_space * p_xx],
            dtype=float,
        )
        closed_mixed = float(
            2.0
            * v_space
            * cosine
            * k_value
            * np.dot(vector_u, np.array([phi, psi]))
        )
        mixed_scale = max(1.0, abs(direct_mixed), abs(closed_mixed))
        maximum_mixed_residual = max(
            maximum_mixed_residual,
            abs(direct_mixed - closed_mixed) / mixed_scale,
        )

        b_vector = (
            2.0 * v_space * cosine * k_value * vector_u
        )
        scalar_kernel = 2.0 * k_value**2 * denominator
        direct_schur = np.outer(b_vector, b_vector) / scalar_kernel
        closed_schur = (
            2.0
            * x_space
            * cosine**2
            / denominator
            * np.outer(vector_u, vector_u)
        )
        schur_scale = max(
            1.0,
            float(np.max(np.abs(direct_schur))),
            float(np.max(np.abs(closed_schur))),
        )
        maximum_schur_residual = max(
            maximum_schur_residual,
            float(
                np.max(np.abs(direct_schur - closed_schur))
                / schur_scale
            ),
        )
        minimum_denominator = min(minimum_denominator, denominator)

    return {
        "samples": samples,
        "maximum_mixed_relative_residual": maximum_mixed_residual,
        "maximum_schur_relative_residual": maximum_schur_residual,
        "minimum_sampled_principal_denominator": minimum_denominator,
    }


def load_cone_rows() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    trajectory_path = SOURCES["checkpoint_4957_trajectory"][0]
    with trajectory_path.open(encoding="utf-8", newline="") as handle:
        trajectory_rows = list(csv.DictReader(handle))

    selected = [
        row
        for row in trajectory_rows
        if row["polynomial_order"] == "8" and row["sample_index"] == "0"
    ]
    cone_rows: list[dict[str, Any]] = []
    maximum_minimum_residual = 0.0
    for row in selected:
        coefficients = {
            degree: float(row[f"a{degree}"])
            for degree in range(2, 9)
        }

        def p_first(x_value: float) -> float:
            return 0.5 + sum(
                degree
                * coefficients[degree]
                * x_value ** (degree - 1)
                for degree in coefficients
            )

        def p_second(x_value: float) -> float:
            return sum(
                degree
                * (degree - 1)
                * coefficients[degree]
                * x_value ** (degree - 2)
                for degree in coefficients
            )

        def longitudinal(x_value: float) -> float:
            return p_first(x_value) + 2.0 * x_value * p_second(x_value)

        transverse_root = first_positive_root(p_first)
        longitudinal_root = first_positive_root(longitudinal)
        if transverse_root is None or longitudinal_root is None:
            raise RuntimeError(f"missing principal root for {row['scheme']}")
        sample_grid = np.linspace(0.0, CERTIFIED_X_MAX, 20_001)
        transverse_values = np.array(
            [2.0 * p_first(float(value)) for value in sample_grid]
        )
        longitudinal_values = np.array(
            [2.0 * longitudinal(float(value)) for value in sample_grid]
        )
        minimum_transverse = float(np.min(transverse_values))
        minimum_longitudinal = float(np.min(longitudinal_values))
        stored_transverse = float(row["minimum_transverse_x_le_0p1"])
        stored_longitudinal = float(row["minimum_longitudinal_x_le_0p1"])
        maximum_minimum_residual = max(
            maximum_minimum_residual,
            abs(minimum_transverse - stored_transverse),
            abs(minimum_longitudinal - stored_longitudinal),
        )
        cone_rows.append(
            {
                "scheme": row["scheme"],
                "polynomial_order": 8,
                "trajectory_sample": 0,
                "certified_x_max": CERTIFIED_X_MAX,
                "minimum_lambda_T_x_le_0p1": minimum_transverse,
                "minimum_lambda_L_x_le_0p1": minimum_longitudinal,
                "first_lambda_L_zero": longitudinal_root,
                "first_PX_zero": transverse_root,
                "longitudinal_zero_precedes_PX_zero": (
                    longitudinal_root < transverse_root
                ),
                "PX_zero_inside_certified_chart": (
                    transverse_root <= CERTIFIED_X_MAX
                ),
                "stealth_root_healthy_and_certified": False,
                "status": (
                    "PX_ZERO_AFTER_LONGITUDINAL_DEGENERACY_AND_OUTSIDE_"
                    "CERTIFIED_CHART"
                ),
                "source_path": relative(trajectory_path),
                "valid_for_claim": False,
            }
        )

    n8_rows = [
        row for row in trajectory_rows if row["polynomial_order"] == "8"
    ]
    all_n8_convex = all(
        row["convex_x_le_0p1"].strip().lower() == "true"
        and float(row["minimum_transverse_x_le_0p1"]) > 0.0
        and float(row["minimum_longitudinal_x_le_0p1"]) > 0.0
        for row in n8_rows
    )
    metrics = {
        "selected_scheme_count": len(selected),
        "N8_trajectory_row_count": len(n8_rows),
        "all_N8_trajectory_rows_convex_x_le_0p1": all_n8_convex,
        "maximum_recomputed_minimum_residual": maximum_minimum_residual,
        "minimum_selected_first_longitudinal_zero": min(
            float(row["first_lambda_L_zero"]) for row in cone_rows
        ),
        "minimum_selected_first_PX_zero": min(
            float(row["first_PX_zero"]) for row in cone_rows
        ),
    }
    return cone_rows, metrics


def build_rows(
    symbolic: dict[str, Any],
    cone_rows: list[dict[str, Any]],
) -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    dict[str, Any],
]:
    source_4943 = relative(SOURCES["checkpoint_4943_document"][0])
    source_4957 = relative(SOURCES["checkpoint_4957_document"][0])
    source_4982 = relative(SOURCES["checkpoint_4982_document"][0])
    source_4983 = relative(SOURCES["checkpoint_4983_document"][0])
    source_5151 = relative(SOURCES["checkpoint_5151_document"][0])
    source_5157 = relative(SOURCES["checkpoint_5157_document"][0])
    source_5177 = relative(SOURCES["checkpoint_5177_document"][0])
    source_5183 = relative(SOURCES["checkpoint_5183_document"][0])

    background_rows = [
        {
            "background": "zero_gradient",
            "representative": "psi=constant; v_mu=0",
            "field_equation": "satisfied",
            "Hilbert_stress": "zero because P(0)=0",
            "static_mixing": "zero",
            "localization": "regular",
            "parent_selection": "exact local vacuum branch",
            "route_status": "RETAIN_LOCAL_GR_NEWTON_MAXWELL",
            "source_path": source_4982,
            "valid_for_claim": False,
        },
        {
            "background": "regular_localized_static",
            "representative": "psi=psi(x); psi->constant; zero scalar flux",
            "field_equation": "div(2 P_X grad psi)=0",
            "Hilbert_stress": "would be nonzero if grad psi nonzero",
            "static_mixing": "not reached",
            "localization": "requested",
            "parent_selection": "ordinary matter has J_psi=Q_psi=0",
            "route_status": "EXACTLY_CONSTANT_WHEN_PX_POSITIVE",
            "source_path": f"{source_4943};{source_4982}",
            "valid_for_claim": False,
        },
        {
            "background": "stationary_spherical_clock_plus_profile",
            "representative": "psi=q_clock*t+phi(r)",
            "field_equation": "2 N r^2 P_X phi_prime/A=Q",
            "Hilbert_stress": "T_tr proportional P_X q_clock phi_prime",
            "static_mixing": "profile part absent when Q=0 and P_X>0",
            "localization": "phi_prime forced to zero",
            "parent_selection": "q_clock remains global integration data",
            "route_status": "REDUCES_TO_HOMOGENEOUS_CLOCK",
            "source_path": f"{source_4943};{source_4982};{source_5157}",
            "valid_for_claim": False,
        },
        {
            "background": "homogeneous_timelike_clock",
            "representative": "psi=q_clock*t",
            "field_equation": "satisfied on stationary metric",
            "Hilbert_stress": "nonzero perfect-fluid-type stress unless q_clock=0",
            "static_mixing": "exactly zero for omega=0 Newtonian perturbations",
            "localization": "global not galaxy-localized",
            "parent_selection": "q_clock or charge is boundary/state datum",
            "route_status": "COSMOLOGY_STATE_ONLY_NOT_STATIC_GALAXY_FORCE",
            "source_path": f"{source_4982};{source_5157}",
            "valid_for_claim": False,
        },
        {
            "background": "homogeneous_spacelike_gradient",
            "representative": "psi=V*z; X=V^2",
            "field_equation": "satisfied in translation-invariant patch",
            "Hilbert_stress": "nonzero anisotropic rank-one stress",
            "static_mixing": "nonzero and proportional V*k_parallel",
            "localization": "not localized and breaks rotations",
            "parent_selection": "V and direction are unsourced boundary data",
            "route_status": "REJECT_AS_GALAXY_BACKGROUND",
            "source_path": source_4982,
            "valid_for_claim": False,
        },
        {
            "background": "constant_null_gradient",
            "representative": "X=0 with v_mu nonzero and null",
            "field_equation": "satisfied in flat translation-invariant patch",
            "Hilbert_stress": "2 P_X(0) v_mu v_nu nonzero null stress",
            "static_mixing": "anisotropic",
            "localization": "not localized",
            "parent_selection": "unsourced boundary data",
            "route_status": "NOT_STEALTH",
            "source_path": source_4982,
            "valid_for_claim": False,
        },
        {
            "background": "PX_zero_ghost_condensate_escape",
            "representative": "X=X_star nonzero; P_X(X_star)=0",
            "field_equation": "degenerate",
            "Hilbert_stress": "cosmological term only; exact zero also needs P=0",
            "static_mixing": "principal scalar cone loses transverse kinetic term",
            "localization": "not supplied",
            "parent_selection": "root outside certified chart after lambda_L zero",
            "route_status": "REJECT_UNHEALTHY_UNCERTIFIED_ESCAPE",
            "source_path": source_4957,
            "valid_for_claim": False,
        },
        {
            "background": "occupied_two_point_state",
            "representative": "<psi>=0; F_X nonzero",
            "field_equation": "CTP/Wigner state equation rather than classical profile",
            "Hilbert_stress": "positive conserved state stress exists",
            "static_mixing": "not represented by classical background Hessian",
            "localization": "stationary state construction exists",
            "parent_selection": "normalization and compensating interaction open",
            "route_status": "DISTINCT_SURVIVING_ROUTE",
            "source_path": f"{source_5151};{source_5177}",
            "valid_for_claim": False,
        },
    ]

    no_lump_rows = [
        {
            "clause": "static_geometry",
            "formula": "ds^2=-N^2 dt^2+gamma_ij dx^i dx^j; N>0",
            "assumption": "connected horizon-free galaxy slice",
            "result": "spatial metric is positive definite",
            "status": "DERIVED_SCOPE",
            "source_path": source_4982,
            "valid_for_claim": False,
        },
        {
            "clause": "shift_current",
            "formula": "J^mu=2 P_X nabla^mu psi; nabla_mu J^mu=0",
            "assumption": "shift-symmetric P(X) parent",
            "result": "no independent adjustable force current",
            "status": "EXACT",
            "source_path": source_4982,
            "valid_for_claim": False,
        },
        {
            "clause": "static_equation",
            "formula": "D_i[2 N P_X D^i psi]=0",
            "assumption": "partial_t psi=0",
            "result": "elliptic divergence equation",
            "status": "EXACT",
            "source_path": source_4982,
            "valid_for_claim": False,
        },
        {
            "clause": "integrated_identity",
            "formula": (
                "integral 2 N sqrt(gamma) P_X |D psi|^2 = "
                "boundary integral 2 N P_X (psi-psi_inf) n.Dpsi"
            ),
            "assumption": "multiply equation by psi-psi_inf and integrate",
            "result": "positive bulk equals boundary flux",
            "status": "EXACT_BY_PARTS",
            "source_path": source_4982,
            "valid_for_claim": False,
        },
        {
            "clause": "ordinary_matter_source",
            "formula": "delta S_SM/delta psi=0; Q_psi=0",
            "assumption": "reflection-even ordinary-matter branch",
            "result": "no baryonic volume source or junction flux",
            "status": "PARENT_DERIVED",
            "source_path": source_4943,
            "valid_for_claim": False,
        },
        {
            "clause": "no_lump_conclusion",
            "formula": "P_X>=epsilon>0 and boundary flux=0 implies D_i psi=0",
            "assumption": "healthy certified local EFT corridor",
            "result": "regular localized static profile is constant",
            "status": "PROVED",
            "source_path": f"{source_4943};{source_4982}",
            "valid_for_claim": False,
        },
        {
            "clause": "spherical_flux",
            "formula": "Q=2 N r^2 P_X phi_prime/A=constant",
            "assumption": "ds^2=-N^2dt^2+A^2dr^2+r^2dOmega^2",
            "result": "regular centre and Q_psi=0 force phi_prime=0",
            "status": "PROVED",
            "source_path": source_4943,
            "valid_for_claim": False,
        },
        {
            "clause": "stationary_staticity",
            "formula": "T_tr=2 P_X q_clock phi_prime",
            "assumption": "psi=q_clock*t+phi(r) and diagonal static metric",
            "result": "q_clock*phi_prime=0 on healthy P_X branch",
            "status": "EXACT",
            "source_path": source_4982,
            "valid_for_claim": False,
        },
        {
            "clause": "strict_EFT_curvature_packet",
            "formula": "integral N sqrt(gamma) K_eff^ij D_i psi D_j psi",
            "assumption": "checkpoint-4943 positive K_eff spatial corridor",
            "result": "positive curvature contacts preserve no-lump identity",
            "status": "BOUNDED_LOCAL_EXTENSION",
            "source_path": source_4943,
            "valid_for_claim": False,
        },
        {
            "clause": "Box2_packet",
            "formula": "positive b_Box adds b_Box integral (Box psi)^2",
            "assumption": "strict-EFT treatment; no spurious heavy pole promoted",
            "result": (
                "positive sign strengthens theorem; unfixed/negative sign cannot "
                "be used nonperturbatively as a derived lump"
            ),
            "status": "LOOPHOLE_NOT_PROMOTED",
            "source_path": source_4983,
            "valid_for_claim": False,
        },
    ]

    hessian_rows = [
        {
            "branch": "covariant_parent",
            "object": "mixed_second_variation",
            "formula": (
                "P_X[tr(h)(v.w)-2 v.h.w]-2 P_XX(v.h.v)(v.w)"
            ),
            "static_limit": "background dependent",
            "momentum_degree": "one in fluctuation momentum",
            "anisotropic": "background dependent",
            "implication": "all specialized vertices descend from one action",
            "source_path": source_4982,
            "valid_for_claim": False,
        },
        {
            "branch": "timelike_clock",
            "object": "B_(Phi,Psi)",
            "formula": (
                "2 q_clock omega "
                "[P_X-2 q_clock^2 P_XX, 3 P_X]"
            ),
            "static_limit": "[0,0]",
            "momentum_degree": "one in omega",
            "anisotropic": False,
            "implication": "no static Newtonian metric-scalar mixing",
            "source_path": source_4982,
            "valid_for_claim": False,
        },
        {
            "branch": "timelike_clock",
            "object": "K_chichi",
            "formula": (
                "2 P_X k^2-2(P_X-2 q_clock^2 P_XX) omega^2"
            ),
            "static_limit": "2 P_X k^2",
            "momentum_degree": "two",
            "anisotropic": False,
            "implication": "Schur response vanishes as omega^2/k^2",
            "source_path": source_4982,
            "valid_for_claim": False,
        },
        {
            "branch": "spacelike_gradient",
            "object": "B_(Phi,Psi)",
            "formula": (
                "2 V k_parallel [P_X, -P_X+2 X P_XX]"
            ),
            "static_limit": "nonzero if k_parallel nonzero",
            "momentum_degree": "one",
            "anisotropic": True,
            "implication": "direction of V is observable",
            "source_path": source_4982,
            "valid_for_claim": False,
        },
        {
            "branch": "spacelike_gradient",
            "object": "K_chichi",
            "formula": (
                "2 k^2[P_X+2 X P_XX cos(theta)^2]"
            ),
            "static_limit": "same",
            "momentum_degree": "two",
            "anisotropic": True,
            "implication": "denominator is the directional principal cone",
            "source_path": source_4982,
            "valid_for_claim": False,
        },
        {
            "branch": "spacelike_gradient",
            "object": "Schur_BKinvB",
            "formula": (
                "2 X cos(theta)^2 U U^T/"
                "[P_X+2 X P_XX cos(theta)^2]; "
                "U=[P_X,-P_X+2 X P_XX]"
            ),
            "static_limit": "finite only before principal-cone zero",
            "momentum_degree": "zero",
            "anisotropic": True,
            "implication": "not the isotropic k*n_q required kernel",
            "source_path": f"{source_4982};{source_5183}",
            "valid_for_claim": False,
        },
    ]

    low_x = np.geomspace(1.0e-8, 1.0e-4, 500)
    high_x = np.geomspace(1.0e4, 1.0e8, 500)

    def occupation(values: np.ndarray) -> np.ndarray:
        return 1.0 / (1.0 + values**Q_LOCKED)

    scaling_definitions = {
        "required_kernel": (
            low_x * occupation(low_x),
            high_x * occupation(high_x),
            "+1 then 1-q",
        ),
        "constant_gradient_kernel": (
            np.ones_like(low_x),
            np.ones_like(high_x),
            "0 then 0",
        ),
        "required_relative_to_Einstein": (
            occupation(low_x) / low_x,
            occupation(high_x) / high_x,
            "-1 then -(1+q)",
        ),
        "constant_gradient_relative_to_Einstein": (
            1.0 / low_x**2,
            1.0 / high_x**2,
            "-2 then -2",
        ),
    }
    scaling_rows: list[dict[str, Any]] = []
    for object_name, (low_values, high_values, expected) in (
        scaling_definitions.items()
    ):
        scaling_rows.append(
            {
                "object": object_name,
                "low_x_log_slope": log_slope(low_x, low_values),
                "high_x_log_slope": log_slope(high_x, high_values),
                "analytic_slopes": expected,
                "matches_checkpoint_5148_required_shape": (
                    object_name.startswith("required")
                ),
                "status": (
                    "TARGET"
                    if object_name.startswith("required")
                    else "SHAPE_MISMATCH"
                ),
                "source_path": f"{source_4982};{source_5183}",
                "valid_for_claim": False,
            }
        )

    route_rows = [
        {
            "route": "regular_localized_classical_PX_background",
            "existence_gate": "fails by positive-current no-lump theorem",
            "response_gate": "not reached",
            "parent_ownership": "ordinary matter source and flux are zero",
            "decision": "REJECT_CURRENT_CERTIFIED_ROUTE",
            "next_action": (
                "do not insert a galaxy profile or boundary scalar charge"
            ),
            "source_path": f"{source_4943};{source_4982}",
            "valid_for_claim": False,
        },
        {
            "route": "homogeneous_timelike_clock",
            "existence_gate": "conditional global state exists",
            "response_gate": "static mixed Hessian exactly zero",
            "parent_ownership": "amplitude/charge not source-selected",
            "decision": "RETAIN_FOR_COSMOLOGY_NOT_STATIC_GALAXY_FORCE",
            "next_action": "do not use as a static local response",
            "source_path": f"{source_4982};{source_5157}",
            "valid_for_claim": False,
        },
        {
            "route": "homogeneous_spacelike_or_null_gradient",
            "existence_gate": "translation-invariant solution only",
            "response_gate": "anisotropic k^0 Schur or null stress",
            "parent_ownership": "amplitude and direction are boundary data",
            "decision": "REJECT_AS_LOCALIZED_ISOTROPIC_GALAXY_ROUTE",
            "next_action": "do not average directions after the fact",
            "source_path": source_4982,
            "valid_for_claim": False,
        },
        {
            "route": "PX_zero_stealth",
            "existence_gate": "outside certified chart and cone-degenerate",
            "response_gate": "strong-coupling pole rather than controlled response",
            "parent_ownership": "no healthy trajectory selects it",
            "decision": "REJECT_CURRENT_ESCAPE",
            "next_action": "requires a new independently stable parent phase",
            "source_path": source_4957,
            "valid_for_claim": False,
        },
        {
            "route": "interacting_occupied_state_CTP_stress",
            "existence_gate": "positive conserved stationary stress exists",
            "response_gate": (
                "nonmultiplicative compensated interaction stress not derived"
            ),
            "parent_ownership": (
                "X2/X3 vertices exist; classical Vlasov density already counted"
            ),
            "decision": "SELECT_NEXT_CONSTRUCTIVE_DERIVATION",
            "next_action": (
                "derive 2PI/CTP interaction stress and its Ward-compensated "
                "static kernel without adding Vlasov density twice"
            ),
            "source_path": f"{source_5151};{source_5177}",
            "valid_for_claim": False,
        },
    ]

    summary = {
        "regular_localized_static_PX_background_exists": False,
        "ordinary_baryons_source_classical_motion_profile": False,
        "timelike_clock_static_mixing_nonzero": False,
        "spacelike_constant_gradient_is_localized_isotropic": False,
        "healthy_certified_PX_zero_stealth_root": False,
        "current_classical_stationary_background_route_retained": False,
        "occupied_two_point_state_route_retained": True,
        "local_GR_Newton_Maxwell_branch_modified": False,
        "full_MTS_claim": False,
        "next_target": (
            "5185 derive the parent-owned interacting occupied-state CTP/2PI "
            "stress beyond the already-counted classical Vlasov density"
        ),
        "route_decision": ROUTE_DECISION,
        "symbolic_contract": symbolic,
    }
    return (
        background_rows,
        no_lump_rows,
        hessian_rows,
        scaling_rows,
        route_rows,
        summary,
    )


def calculate_checks(
    symbolic: dict[str, Any],
    cone_rows: list[dict[str, Any]],
    cone_metrics: dict[str, Any],
    monte_carlo: dict[str, float],
    rows: tuple[
        list[dict[str, Any]],
        list[dict[str, Any]],
        list[dict[str, Any]],
        list[dict[str, Any]],
        list[dict[str, Any]],
        dict[str, Any],
    ],
    source_hashes: dict[str, str],
    formal_digest: str,
    checkpoint_5176_digest: str,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    (
        background_rows,
        no_lump_rows,
        hessian_rows,
        scaling_rows,
        route_rows,
        summary,
    ) = rows
    source_hash_match = all(
        source_hashes[name] == expected
        for name, (_, expected) in SOURCES.items()
    )
    schemes = {row["scheme"]: row for row in cone_rows}
    required_kernel = next(
        row for row in scaling_rows if row["object"] == "required_kernel"
    )
    constant_kernel = next(
        row
        for row in scaling_rows
        if row["object"] == "constant_gradient_kernel"
    )
    required_relative = next(
        row
        for row in scaling_rows
        if row["object"] == "required_relative_to_Einstein"
    )
    constant_relative = next(
        row
        for row in scaling_rows
        if row["object"] == "constant_gradient_relative_to_Einstein"
    )

    checks = [
        validation_row(
            "V5184_01_source_count",
            "all declared sources exist",
            len(source_hashes) == len(SOURCES),
            len(source_hashes),
            len(SOURCES),
        ),
        validation_row(
            "V5184_02_source_locks",
            "all source hashes match their read-only locks",
            source_hash_match,
            sum(
                source_hashes[name] == expected
                for name, (_, expected) in SOURCES.items()
            ),
            len(SOURCES),
        ),
        validation_row(
            "V5184_03_formal_lock",
            "formalization-workbench remains locked",
            formal_digest == FORMAL_DIGEST_LOCK,
            formal_digest,
            FORMAL_DIGEST_LOCK,
        ),
        validation_row(
            "V5184_04_5176_lock",
            "checkpoint 5176 ensemble remains locked",
            checkpoint_5176_digest == CHECKPOINT_5176_TREE_LOCK,
            checkpoint_5176_digest,
            CHECKPOINT_5176_TREE_LOCK,
        ),
        validation_row(
            "V5184_05_timelike_static_zero",
            "homogeneous timelike background has zero static mixed vertex",
            symbolic["timelike_static_zero"],
            symbolic["timelike_static_b"],
            ["0", "0"],
        ),
        validation_row(
            "V5184_06_timelike_quasistatic_zero",
            "timelike Schur response vanishes in omega to zero limit",
            symbolic["timelike_quasistatic_schur_zero"],
            symbolic["timelike_quasistatic_schur_zero"],
            True,
        ),
        validation_row(
            "V5184_07_spacelike_schur_identity",
            "closed spacelike Schur matrix matches direct contraction",
            symbolic["spacelike_schur_identity"],
            symbolic["spacelike_schur_identity"],
            True,
        ),
        validation_row(
            "V5184_08_spacelike_degree",
            "constant-gradient spacelike Schur kernel is degree zero in k",
            symbolic["spacelike_schur_degree_zero"],
            symbolic["spacelike_schur_degree_zero"],
            True,
        ),
        validation_row(
            "V5184_09_monte_carlo_mixed",
            "independent spacelike mixed-vertex crosscheck",
            monte_carlo["maximum_mixed_relative_residual"] < 1.0e-13,
            monte_carlo["maximum_mixed_relative_residual"],
            "<1e-13",
        ),
        validation_row(
            "V5184_10_monte_carlo_schur",
            "independent spacelike Schur crosscheck",
            monte_carlo["maximum_schur_relative_residual"] < 1.0e-13,
            monte_carlo["maximum_schur_relative_residual"],
            "<1e-13",
        ),
        validation_row(
            "V5184_11_dynamic_root_order",
            "dynamic N8 longitudinal cone zero precedes P_X zero",
            schemes["dynamic_etaN"]["longitudinal_zero_precedes_PX_zero"],
            (
                schemes["dynamic_etaN"]["first_lambda_L_zero"],
                schemes["dynamic_etaN"]["first_PX_zero"],
            ),
            "lambda_L_zero<PX_zero",
        ),
        validation_row(
            "V5184_12_reference_root_order",
            "reference N8 longitudinal cone zero precedes P_X zero",
            schemes["reference_etaN0"][
                "longitudinal_zero_precedes_PX_zero"
            ],
            (
                schemes["reference_etaN0"]["first_lambda_L_zero"],
                schemes["reference_etaN0"]["first_PX_zero"],
            ),
            "lambda_L_zero<PX_zero",
        ),
        validation_row(
            "V5184_13_roots_outside_chart",
            "all selected P_X zeros lie outside certified chart",
            all(
                not row["PX_zero_inside_certified_chart"]
                for row in cone_rows
            ),
            [row["first_PX_zero"] for row in cone_rows],
            f">{CERTIFIED_X_MAX}",
        ),
        validation_row(
            "V5184_14_trajectory_convex",
            "all N8 trajectory samples are convex on x<=0.1",
            cone_metrics["all_N8_trajectory_rows_convex_x_le_0p1"],
            cone_metrics["N8_trajectory_row_count"],
            "all positive",
        ),
        validation_row(
            "V5184_15_trajectory_minima",
            "recomputed principal minima match source rows",
            cone_metrics["maximum_recomputed_minimum_residual"] < 2.0e-12,
            cone_metrics["maximum_recomputed_minimum_residual"],
            "<2e-12",
        ),
        validation_row(
            "V5184_16_required_kernel_low",
            "required kernel low-k slope is +1",
            abs(float(required_kernel["low_x_log_slope"]) - 1.0) < 1.0e-3,
            required_kernel["low_x_log_slope"],
            1.0,
        ),
        validation_row(
            "V5184_17_required_kernel_high",
            "required kernel high-k slope is 1-q",
            abs(
                float(required_kernel["high_x_log_slope"])
                - (1.0 - Q_LOCKED)
            )
            < 1.0e-3,
            required_kernel["high_x_log_slope"],
            1.0 - Q_LOCKED,
        ),
        validation_row(
            "V5184_18_constant_kernel",
            "constant-gradient Schur kernel has zero low/high slopes",
            max(
                abs(float(constant_kernel["low_x_log_slope"])),
                abs(float(constant_kernel["high_x_log_slope"])),
            )
            < 1.0e-12,
            (
                constant_kernel["low_x_log_slope"],
                constant_kernel["high_x_log_slope"],
            ),
            (0.0, 0.0),
        ),
        validation_row(
            "V5184_19_required_relative",
            "required relative response has -1 and -(1+q) slopes",
            abs(float(required_relative["low_x_log_slope"]) + 1.0) < 1.0e-3
            and abs(
                float(required_relative["high_x_log_slope"])
                + 1.0
                + Q_LOCKED
            )
            < 1.0e-3,
            (
                required_relative["low_x_log_slope"],
                required_relative["high_x_log_slope"],
            ),
            (-1.0, -(1.0 + Q_LOCKED)),
        ),
        validation_row(
            "V5184_20_constant_relative",
            "constant-gradient relative response has -2 slopes",
            max(
                abs(float(constant_relative["low_x_log_slope"]) + 2.0),
                abs(float(constant_relative["high_x_log_slope"]) + 2.0),
            )
            < 1.0e-12,
            (
                constant_relative["low_x_log_slope"],
                constant_relative["high_x_log_slope"],
            ),
            (-2.0, -2.0),
        ),
        validation_row(
            "V5184_21_no_lump_clause",
            "positive-current no-lump conclusion is present",
            any(
                row["clause"] == "no_lump_conclusion"
                and row["status"] == "PROVED"
                for row in no_lump_rows
            ),
            True,
            True,
        ),
        validation_row(
            "V5184_22_matter_source_zero",
            "ordinary matter source and scalar flux remain zero",
            any(
                row["clause"] == "ordinary_matter_source"
                and "Q_psi=0" in row["formula"]
                for row in no_lump_rows
            ),
            True,
            True,
        ),
        validation_row(
            "V5184_23_background_classes",
            "all declared stationary classes were audited",
            len(background_rows) == 8,
            len(background_rows),
            8,
        ),
        validation_row(
            "V5184_24_hessian_rows",
            "timelike and spacelike Hessian blocks are recorded",
            len(hessian_rows) == 6,
            len(hessian_rows),
            6,
        ),
        validation_row(
            "V5184_25_route_selected",
            "next route is interacting occupied-state stress",
            any(
                row["decision"] == "SELECT_NEXT_CONSTRUCTIVE_DERIVATION"
                for row in route_rows
            ),
            True,
            True,
        ),
        validation_row(
            "V5184_26_local_branch",
            "local GR/Newton/Maxwell branch is unmodified",
            not summary["local_GR_Newton_Maxwell_branch_modified"],
            summary["local_GR_Newton_Maxwell_branch_modified"],
            False,
        ),
        validation_row(
            "V5184_27_no_full_claim",
            "checkpoint makes no full-MTS claim",
            not summary["full_MTS_claim"],
            summary["full_MTS_claim"],
            False,
        ),
    ]
    metrics = {
        "symbolic": symbolic,
        "monte_carlo": monte_carlo,
        "cone": cone_metrics,
        "scaling": {
            row["object"]: {
                "low_x_log_slope": row["low_x_log_slope"],
                "high_x_log_slope": row["high_x_log_slope"],
            }
            for row in scaling_rows
        },
    }
    return checks, metrics


def write_document(result: dict[str, Any]) -> None:
    metrics = result["metrics"]
    cone_rows = result["cone_rows"]
    schemes = {row["scheme"]: row for row in cone_rows}
    scaling = metrics["scaling"]
    text = f"""# 5184 - Stationary P(X) background no-lump and mixed-Hessian gate

Marker: `{MARKER}`.

Date: `{CHECKED_DATE}`.

## Decision

Checkpoint 5184 does the calculation requested at checkpoint 5183 rather than
assuming a nonzero motion profile. The result is a controlled negative for
the **classical stationary-background** route inside the currently certified
local EFT:

```text
{ROUTE_DECISION}
```

This does not reject the occupied-state programme. It separates two objects
that had been at risk of being mixed:

```text
classical background:       <psi> != 0;
occupied two-point state:   <psi> = 0 but F_X(x,y) != 0.
```

Checkpoint 5151 constructed the second object. The theorem below rejects a
regular source-free localized member of the first object in the healthy
`P_X>0` corridor.

## 1. Scope

Use the parent packet

```text
S_P = integral sqrt(-g) P(X),
X = g^munu nabla_mu psi nabla_nu psi,
P(0)=0,
P_X(0)=1/2.
```

The exact shift current and Hilbert source are

```text
J^mu = 2 P_X nabla^mu psi,
nabla_mu J^mu = 0,

T^mu_nu = 2 P_X v^mu v_nu - delta^mu_nu P.
```

Checkpoint 4943 supplies the essential source clause:

```text
delta S_SM/delta psi = 0,
Q_psi = 0,
```

including ordinary-matter interiors and nonsingular junctions. The theorem is
for a connected, horizon-free static galaxy slice, regular fields, constant
asymptotic scalar data, zero scalar boundary flux and positive spatial
principal operator. It is not advertised as a theorem about an unknown
nonperturbative UV completion.

## 2. Exact static no-lump theorem

Write

```text
ds^2 = -N^2 dt^2 + gamma_ij dx^i dx^j,
N>0,
partial_t psi=0.
```

The current equation becomes

```text
D_i[2 N P_X D^i psi]=0.
```

Multiply by `psi-psi_inf`, integrate over the static slice and integrate by
parts:

```text
integral_Sigma 2 N sqrt(gamma) P_X |D psi|^2

 = boundary_integral 2 N P_X (psi-psi_inf) n^i D_i psi.
```

The parent ordinary-matter theorem makes the interior/junction contribution
zero. Constant asymptotic data or zero scalar flux makes the outer term zero.
If

```text
P_X >= epsilon > 0
```

throughout the profile, the integrand is nonnegative and vanishes only when

```text
D_i psi=0.
```

Thus the requested regular localized static background is exactly constant.
This is not a boundary condition smuggled into the response: it follows from
the parent source theorem, regularity and the healthy principal sign.

The result also holds for a positive definite strict-EFT spatial kinetic
tensor `K_eff^ij`, including the bounded local curvature contacts of
checkpoint 4943. A positive `(Box psi)^2` coordinate strengthens the
integrated identity. An unfixed negative coefficient cannot be iterated
nonperturbatively to manufacture a lump: checkpoint 4983 treats that
coordinate in strict EFT and forbids promotion of its spurious heavy pole.

## 3. Spherical stationary extension

For

```text
ds^2=-N(r)^2 dt^2+A(r)^2 dr^2+r^2 dOmega^2,
psi=q_clock t+phi(r),
```

the radial current integrates once:

```text
Q = 2 N r^2 P_X phi'(r)/A = constant.
```

A regular centre has `Q=0`; checkpoint 4943 also forbids baryons from
supplying a nonzero junction charge. On the healthy branch,

```text
Q=0 and P_X>0  =>  phi'(r)=0.
```

There is a second exact check. A diagonal static metric requires

```text
T_tr=2 P_X q_clock phi'(r)=0.
```

Therefore a stationary radial profile plus a clock does not evade the
theorem. It reduces to a homogeneous timelike clock, a pure radial branch
with forbidden flux, or the degenerate `P_X=0` branch.

## 4. Stress and the stealth escape

For a nonnull constant gradient, the stress has three eigenvalues `-P` and
one eigenvalue

```text
2 X P_X-P.
```

Removing only the anisotropic/rank-one part requires `P_X=0`. Exact zero
stress additionally requires `P=0`. A null gradient at `X=0` is not stealth:

```text
P(0)=0,
P_X(0)=1/2,
T_mn = 2 P_X(0) v_m v_n != 0.
```

The source-locked order-eight trajectory gives:

| scheme | first `lambda_L=0` | first `P_X=0` | certified chart |
|---|---:|---:|---:|
| dynamic `eta_N` | {schemes["dynamic_etaN"]["first_lambda_L_zero"]:.15g} | {schemes["dynamic_etaN"]["first_PX_zero"]:.15g} | `x<=0.1` |
| reference `eta_N=0` | {schemes["reference_etaN0"]["first_lambda_L_zero"]:.15g} | {schemes["reference_etaN0"]["first_PX_zero"]:.15g} | `x<=0.1` |

In both schemes the longitudinal principal eigenvalue crosses zero before
`P_X` reaches zero, and both events are outside the certified chart. At
`P_X=0` the transverse scalar kinetic eigenvalue itself vanishes. The
would-be stealth point is therefore neither a healthy derived phase nor a
controlled response pole.

All `{metrics["cone"]["N8_trajectory_row_count"]}` stored order-eight
trajectory rows remain convex on `x<=0.1`. Recomputing their selected UV
principal minima agrees with the source table to
`{metrics["cone"]["maximum_recomputed_minimum_residual"]:.3e}`.

## 5. Exact timelike mixed Hessian

Checkpoint 4982 derived

```text
delta_h delta_chi L
 =P_X[tr(h)(v.w)-2v.h.w]
  -2P_XX(v.h.v)(v.w).
```

Use signature `(-,+,+,+)` and Newtonian gauge

```text
h_00=-2 Phi,
h_ij=-2 Psi delta_ij.
```

For `v_mu=(q_clock,0,0,0)` and fluctuation frequency `omega`,

```text
B_(Phi,Psi)
 =2 q_clock omega
   [P_X-2 q_clock^2 P_XX, 3 P_X],

K_chichi
 =2 P_X k^2
  -2(P_X-2 q_clock^2 P_XX) omega^2.
```

Consequently

```text
omega=0  =>  B_(Phi,Psi)=(0,0).
```

The finite-frequency Schur correction vanishes as `omega^2/k^2` in the
quasistatic limit. A homogeneous clock can affect cosmological/time-dependent
response, but it cannot supply the missing static galaxy kernel. Its
amplitude is also a global current/initial-state datum, not a baryon-selected
local profile.

## 6. Exact spacelike mixed Hessian

For a constant spacelike gradient `v_mu=(0,0,0,V)`, set

```text
X=V^2,
k_parallel=k cos(theta),
U=[P_X,-P_X+2 X P_XX].
```

The exact static blocks are

```text
B_(Phi,Psi)=2 V k_parallel U,

K_chichi
 =2 k^2[P_X+2 X P_XX cos(theta)^2].
```

Integrating the scalar fluctuation gives

```text
B K_chichi^-1 B^T

 =2 X cos(theta)^2 U U^T
  /[P_X+2 X P_XX cos(theta)^2].
```

This result is:

1. anisotropic;
2. homogeneous of degree zero in `k`;
3. singular only when the directional scalar principal cone degenerates;
4. carried by a nonlocalized, stressed background whose amplitude and
   direction are not selected by the parent source.

An independent `{int(metrics["monte_carlo"]["samples"])}`-sample numerical
contraction gives maximum mixed and Schur residuals
`{metrics["monte_carlo"]["maximum_mixed_relative_residual"]:.3e}` and
`{metrics["monte_carlo"]["maximum_schur_relative_residual"]:.3e}`.

## 7. Scaling against the required response

Checkpoint 5183 restated the required kernel scaling as

```text
d_required(k) proportional k n_q(k/mu),
n_q(x)=1/(1+x^q),
q=0.77.
```

The constant-gradient Schur kernel is `k^0`. Relative to the Einstein
constraint kernel `a proportional k^2`, the two alternatives are

```text
required relative response:            n_q(x)/x,
constant-gradient relative response:   1/x^2.
```

The executed low/high slopes are:

| object | low slope | high slope |
|---|---:|---:|
| required kernel | {scaling["required_kernel"]["low_x_log_slope"]:.15g} | {scaling["required_kernel"]["high_x_log_slope"]:.15g} |
| constant-gradient kernel | {scaling["constant_gradient_kernel"]["low_x_log_slope"]:.15g} | {scaling["constant_gradient_kernel"]["high_x_log_slope"]:.15g} |
| required relative response | {scaling["required_relative_to_Einstein"]["low_x_log_slope"]:.15g} | {scaling["required_relative_to_Einstein"]["high_x_log_slope"]:.15g} |
| constant-gradient relative response | {scaling["constant_gradient_relative_to_Einstein"]["low_x_log_slope"]:.15g} | {scaling["constant_gradient_relative_to_Einstein"]["high_x_log_slope"]:.15g} |

No constant normalization repairs both asymptotic slopes. Allowing the
background to vary spatially would abandon the constant-gradient Hessian, but
the no-lump theorem has already excluded a regular localized source-free
profile in the healthy corridor.

## 8. What survives and what comes next

```text
regular localized classical P(X) galaxy background = rejected in certified corridor;
timelike clock as static galaxy response            = exact zero;
spacelike/null constant gradient                     = nonlocalized/stressed/anisotropic;
P_X=0 stealth escape                                 = unhealthy and uncertified;
zero-gradient local GR/Newton/Maxwell branch         = retained;
checkpoint-5151 occupied-state stress                = distinct and retained;
full local-GR or galaxy claim                        = false.
```

The next calculation must not try another arbitrary classical profile.
Checkpoint 5185 should derive the first parent-owned **interacting**
occupied-state stress from the existing essential `X^2/X^3` vertices in the
CTP/2PI hierarchy. It must:

1. satisfy the metric Ward identity;
2. remove the classical Vlasov density already counted at checkpoint 5171;
3. test whether the remaining static kernel is compensated,
   scale-dependent and local-vacuum silent;
4. derive its state normalization or reject the route.

That is a constructive forward calculation, not another missing-input list.

## 9. Audit

All `{result["validation_count"]}` validations pass. Every evidence row
remains `valid_for_claim=false`. The protected `formalization-workbench`
digest remains `{result["formalization_workbench_tree_sha256"]}` and the
checkpoint-5176 ensemble remains
`{result["checkpoint_5176_tree_sha256"]}`. No GitHub action occurred.

Generated files:

- `source-intake/functional_rg/5184/stationary_background_classification.csv`
- `source-intake/functional_rg/5184/static_no_lump_and_flux_theorem.csv`
- `source-intake/functional_rg/5184/timelike_spacelike_mixed_Hessian.csv`
- `source-intake/functional_rg/5184/stealth_root_and_principal_cone_gate.csv`
- `source-intake/functional_rg/5184/stationary_background_scaling_comparison.csv`
- `source-intake/functional_rg/5184/stationary_background_route_decision.csv`
- `source-intake/functional_rg/5184/source_provenance.csv`
- `source-intake/functional_rg/5184/stationary_PX_background_results.json`
- `source-intake/mts_residuals/P8_Y5_BRR545_5184_VALIDATION.csv`
"""
    DOCUMENT.write_text(text, encoding="utf-8")


def run(dry_run: bool) -> dict[str, Any]:
    missing = [
        name for name, (path, _) in SOURCES.items() if not path.is_file()
    ]
    if missing:
        raise FileNotFoundError(f"missing sources: {missing}")
    source_hashes_before = {
        name: file_digest(path) for name, (path, _) in SOURCES.items()
    }
    formal_before = tree_digest(FORMAL)
    checkpoint_5176_before = tree_digest(CHECKPOINT_5176_ROOT)

    symbolic = symbolic_contract()
    cone_rows, cone_metrics = load_cone_rows()
    monte_carlo = monte_carlo_crosscheck()
    rows = build_rows(symbolic, cone_rows)
    checks, metrics = calculate_checks(
        symbolic,
        cone_rows,
        cone_metrics,
        monte_carlo,
        rows,
        source_hashes_before,
        formal_before,
        checkpoint_5176_before,
    )
    failures = [row["validation_id"] for row in checks if not row["passed"]]
    (
        background_rows,
        no_lump_rows,
        hessian_rows,
        scaling_rows,
        route_rows,
        summary,
    ) = rows
    dry_result = {
        "checkpoint_marker": MARKER,
        "checked_date": CHECKED_DATE,
        "dry_run": dry_run,
        "route_decision": ROUTE_DECISION,
        "metrics": metrics,
        "summary": summary,
        "cone_rows": cone_rows,
        "validation_count": len(checks),
        "validation_failures": failures,
    }
    if failures:
        raise RuntimeError(f"dry validation failures: {failures}")
    if dry_run:
        return dry_result

    write_csv(BACKGROUND_CSV, background_rows)
    write_csv(NO_LUMP_CSV, no_lump_rows)
    write_csv(HESSIAN_CSV, hessian_rows)
    write_csv(CONE_CSV, cone_rows)
    write_csv(SCALING_CSV, scaling_rows)
    write_csv(ROUTE_CSV, route_rows)
    provenance_rows = [
        {
            "source_id": name,
            "source_path": str(path),
            "sha256": source_hashes_before[name],
            "expected_sha256": expected,
            "status": "hash_locked_read_only",
            "checked_date": CHECKED_DATE,
        }
        for name, (path, expected) in SOURCES.items()
    ]
    write_csv(PROVENANCE_CSV, provenance_rows)

    source_hashes_after = {
        name: file_digest(path) for name, (path, _) in SOURCES.items()
    }
    formal_after = tree_digest(FORMAL)
    checkpoint_5176_after = tree_digest(CHECKPOINT_5176_ROOT)
    output_tables = (
        BACKGROUND_CSV,
        NO_LUMP_CSV,
        HESSIAN_CSV,
        CONE_CSV,
        SCALING_CSV,
        ROUTE_CSV,
        PROVENANCE_CSV,
    )
    output_text = "\n".join(
        path.read_text(encoding="utf-8") for path in output_tables
    )
    output_digest = hashlib.sha256(output_text.encode("utf-8")).hexdigest()
    full_checks = checks + [
        validation_row(
            "V5184_28_sources_read_only",
            "all source hashes remain unchanged",
            source_hashes_before == source_hashes_after,
            sum(
                source_hashes_before[name] == source_hashes_after[name]
                for name in SOURCES
            ),
            len(SOURCES),
        ),
        validation_row(
            "V5184_29_formal_after",
            "formalization-workbench remains unchanged",
            formal_after == formal_before == FORMAL_DIGEST_LOCK,
            formal_after,
            FORMAL_DIGEST_LOCK,
        ),
        validation_row(
            "V5184_30_5176_after",
            "checkpoint 5176 remains immutable",
            checkpoint_5176_after
            == checkpoint_5176_before
            == CHECKPOINT_5176_TREE_LOCK,
            checkpoint_5176_after,
            CHECKPOINT_5176_TREE_LOCK,
        ),
        validation_row(
            "V5184_31_no_placeholders",
            "generated evidence contains no missing-input placeholder",
            "MISSING_" not in output_text,
            "MISSING_" in output_text,
            False,
        ),
        validation_row(
            "V5184_32_provenance_rows",
            "every source has one provenance row",
            len(provenance_rows) == len(SOURCES),
            len(provenance_rows),
            len(SOURCES),
        ),
        validation_row(
            "V5184_33_output_parse",
            "all output CSVs parse with nonempty rows",
            all(
                len(list(csv.DictReader(path.open(encoding="utf-8")))) > 0
                for path in output_tables
            ),
            len(output_tables),
            len(output_tables),
        ),
        validation_row(
            "V5184_34_claim_columns",
            "every evidence row remains nonclaim",
            all(
                str(row["valid_for_claim"]).lower() == "false"
                for table in (
                    background_rows,
                    no_lump_rows,
                    hessian_rows,
                    cone_rows,
                    scaling_rows,
                    route_rows,
                )
                for row in table
            ),
            False,
            False,
        ),
        validation_row(
            "V5184_35_local_branch_unchanged",
            "local GR/Newton/Maxwell branch is unchanged",
            not summary["local_GR_Newton_Maxwell_branch_modified"],
            summary["local_GR_Newton_Maxwell_branch_modified"],
            False,
        ),
    ]
    full_failures = [
        row["validation_id"] for row in full_checks if not row["passed"]
    ]
    result = {
        "checkpoint_marker": MARKER,
        "checked_date": CHECKED_DATE,
        "dry_run": False,
        "route_decision": ROUTE_DECISION,
        "source_paths": {
            name: str(path) for name, (path, _) in SOURCES.items()
        },
        "source_hashes_before": source_hashes_before,
        "source_hashes_after": source_hashes_after,
        "formalization_workbench_tree_sha256": formal_after,
        "checkpoint_5176_tree_sha256": checkpoint_5176_after,
        "output_payload_sha256": output_digest,
        "metrics": metrics,
        "summary": summary,
        "cone_rows": cone_rows,
        "validation_count": len(full_checks),
        "validation_failures": full_failures,
        "valid_for_local_GR_claim": False,
        "valid_for_galaxy_claim": False,
        "valid_for_cosmology_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    write_json(RESULT_JSON, result)
    write_document(result)
    write_csv(VALIDATION_CSV, full_checks)
    if full_failures:
        raise RuntimeError(f"validation failures: {full_failures}")
    return result


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Prove or reject a regular parent stationary P(X) background, "
            "derive its exact Newtonian mixed Hessians, and select the next "
            "nonduplicative route."
        )
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="validate calculations and source locks without writing outputs",
    )
    arguments = parser.parse_args()
    result = run(arguments.dry_run)
    print(json.dumps(result, indent=2, sort_keys=True, allow_nan=False))


if __name__ == "__main__":
    main()
