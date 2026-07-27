from __future__ import annotations

import argparse
import ast
import csv
import hashlib
import json
import math
import subprocess
import sys
from pathlib import Path
from typing import Any

sys.dont_write_bytecode = True

import numpy as np
import sympy as sp

import Y5_R2FR_4956_functional_PX_fixed_function_gate as functional_px
import Y5_R2FR_5208_common_motion_trajectory_scale_covariance as checkpoint_5208


CHECKPOINT = 5209
MARKER = "MTS_5209_FINITE_MASS_ESSENTIAL_PX_VACUUM_BRANCH_GATE"
CHECKED_DATE = "2026-07-24"
POST = Path(__file__).resolve().parents[1]
ROOT = POST.parent
FORMAL = ROOT / "formalization-workbench"
OUT = POST / "source-intake" / "functional_rg" / str(CHECKPOINT)
VALIDATION = (
    POST
    / "source-intake"
    / "mts_residuals"
    / f"P8_Y5_BRR545_{CHECKPOINT}_VALIDATION.csv"
)
DOCUMENT = (
    POST
    / "5209-Y5-R2FR-finite-mass-essential-PX-threshold-backreaction-"
    "vacuum-rank-and-local-GR-Maxwell-gate.md"
)
PUBLIC = checkpoint_5208.PUBLIC
GALAXY = checkpoint_5208.GALAXY
PUBLIC_HEAD = checkpoint_5208.PUBLIC_HEAD
GALAXY_HEAD = checkpoint_5208.GALAXY_HEAD
GALAXY_DIRTY = checkpoint_5208.GALAXY_DIRTY
FORMAL_LOCK = checkpoint_5208.FORMAL_LOCK
X_CONTROL = 0.1
QUADRATURE_ORDER = 21
SOURCE_LOCKS = {
    POST
    / "4958-Y5-R2FR-six-derivative-essential-X2-X3-quotient-and-invariant-"
    "2to4-amplitude-or-rate-route-rejection.md": (
        "d08b8a0ab6a5317c77a23accd34dc46c5ad6a0bc5aa73e0767c8e0aa0edd5f1c"
    ),
    POST / "scripts" / "Y5_R2FR_4956_functional_PX_fixed_function_gate.py": (
        "b72f494961a83171520098dedd166c0af66f187060f9be52aafde3befb126333"
    ),
    POST / "scripts" / "Y5_R2FR_4958_essential_PX_sixpoint_trajectory.py": (
        "521ffed6f208cf4c0db3fd596643fc0970f34e1050de71ab65e37c44906ff77f"
    ),
    POST
    / "source-intake"
    / "functional_rg"
    / "4958"
    / "essential_PX_sixpoint_trajectory_results.json": (
        "383e13cd13c3e90be22dbf8ad589c756a26cad002f01da4ce151ad262e48ae67"
    ),
    POST
    / "source-intake"
    / "functional_rg"
    / "4958"
    / "essential_functional_GR_trajectory.csv": (
        "b4317dcc01084a61a6b282bd331d2ce111b835e499c86e65077d0fb98a549081"
    ),
    POST
    / "source-intake"
    / "functional_rg"
    / "4937"
    / "src-2110.09566v1"
    / "SSTwAS.tex": (
        "09e4775df76bf3e2024be7f2ec655a125436dbb6042779bc71fe03f6f7e5d778"
    ),
    POST
    / "5205-Y5-R2FR-normalized-CTP-regular-mode-ensemble-Hamiltonian-"
    "constraint-and-zero-Lambda-second-moment-selection-theorem.md": (
        "2563092d1eb5ede72275042bec70d70f79f7f98db371d5a710f681d59a38af50"
    ),
    POST / "scripts" / "Y5_R2FR_5205_normalized_CTP_regular_mode_state_gate.py": (
        "819a01a287e2a89b0582789927dd8da28178b97a7650245416025f36f20a2c55"
    ),
    POST
    / "source-intake"
    / "functional_rg"
    / "5205"
    / "normalized_CTP_regular_mode_state_results.json": (
        "08bc87ff2feefdf05d35a4df4836e55c9a4dd9eeeb3b7eff72c0960112400537"
    ),
    POST
    / "source-intake"
    / "functional_rg"
    / "5205"
    / "Hamiltonian_constraint_state_normalization.csv": (
        "62de68f47537b056c4c36b3eb06541a80920863fb444b75c3c87345e6cf3d134"
    ),
    POST
    / "5208-Y5-R2FR-common-minimal-motion-trajectory-canonical-Z-quotient-"
    "absolute-scale-covariance-and-local-GR-selection.md": (
        "95f49142309bcc8b438c864d170134b9952086ca6b23322960f8eec29edad8c8"
    ),
    POST
    / "scripts"
    / "Y5_R2FR_5208_common_motion_trajectory_scale_covariance.py": (
        "e7a64067eb5ae71db6064c814f195a96a7ff25243827aa02ac719bc4adf07107"
    ),
    POST
    / "source-intake"
    / "functional_rg"
    / "5208"
    / "common_minimal_motion_trajectory_results.json": (
        "fbda1e61e5eec0aed77f411fa6309b4e97c87b61e06b007684e9065af2ca70df"
    ),
    POST
    / "source-intake"
    / "functional_rg"
    / "5208"
    / "X2_FLRW_suppression.csv": (
        "29bdfaf41ad3396085a0c694e4f233a3d5e57b0c60516fcd337127e084d462c7"
    ),
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5208_VALIDATION.csv": (
        "78c9139c0dc4ac3b4bd58c80fceebcc01cc8b9a27a04836c41df24f81bc39015"
    ),
}


def file_digest(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def selected_digest(paths: list[Path], base: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(paths):
        digest.update(path.relative_to(base).as_posix().encode("utf-8"))
        digest.update(file_digest(path).encode("ascii"))
    return digest.hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty CSV: {path}")
    fieldnames: list[str] = []
    for row in rows:
        fieldnames.extend(key for key in row if key not in fieldnames)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def tagged(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            **row,
            "checkpoint": CHECKPOINT,
            "checkpoint_marker": MARKER,
            "valid_for_full_MTS_claim": False,
            "source_checked_date": CHECKED_DATE,
        }
        for row in rows
    ]


def assert_source_locks() -> dict[str, str]:
    hashes: dict[str, str] = {}
    for path, expected in SOURCE_LOCKS.items():
        if not path.is_file():
            raise FileNotFoundError(path)
        actual = file_digest(path)
        if actual != expected:
            raise RuntimeError(
                f"source lock mismatch for {path}: expected {expected}, got {actual}"
            )
        hashes[path.relative_to(POST).as_posix()] = actual
    return hashes


def threshold_q(
    eta: float,
    order: int,
    scalar_propagators: int,
    graviton_propagators: int,
    scalar_mass: float,
    graviton_mass: float = 0.0,
) -> float:
    numerator = 1.0 / math.factorial(order) - eta / (
        2.0 * math.factorial(order + 1)
    )
    return numerator / (
        (1.0 + scalar_mass) ** scalar_propagators
        * (1.0 + graviton_mass) ** graviton_propagators
    )


def redundant_sources(
    gravity: float,
    c_essential: float,
    eta_newton: float,
    eta_scalar: float,
    scalar_mass: float,
) -> tuple[float, float]:
    qn_2_12 = threshold_q(eta_newton, 2, 1, 2, scalar_mass)
    qn_3_13 = threshold_q(eta_newton, 3, 1, 3, scalar_mass)
    qs_2_20 = threshold_q(eta_scalar, 2, 2, 0, scalar_mass)
    qs_2_21 = threshold_q(eta_scalar, 2, 2, 1, scalar_mass)
    qs_3_22 = threshold_q(eta_scalar, 3, 2, 2, scalar_mass)
    beta_ctilde = (
        -gravity * qn_2_12 / (3.0 * math.pi)
        + c_essential * qs_2_20 / (12.0 * math.pi**2)
    )
    beta_d = (
        gravity
        * (4.0 * qn_2_12 - 18.0 * qn_3_13 + qs_2_21 - 9.0 * qs_3_22)
        / (6.0 * math.pi)
        - c_essential * qs_2_20 / (12.0 * math.pi**2)
    )
    return beta_ctilde, beta_d


def massive_quantum_coefficients(
    projector: functional_px.FunctionalPXProjector,
    coefficients: np.ndarray,
    newton: float,
    eta_newton: float,
    scalar_mass: float,
) -> tuple[np.ndarray, np.ndarray]:
    order = len(coefficients) - 1
    maximum_power = 2 * order
    hessian = [
        np.zeros((projector.node_count, 11, 11), dtype=float)
        for _ in range(maximum_power + 1)
    ]
    hessian[0][:] = np.eye(11)
    hessian[0][:, 10, 10] = 1.0 + scalar_mass
    gravity_coordinate = 32.0 * math.pi * newton
    gravity_root = math.sqrt(max(gravity_coordinate, 0.0))
    for power in range(1, order + 1):
        coefficient = coefficients[power]
        metric_vertex = coefficient * (
            projector.metric_measure
            + power * projector.metric_gradient
            + power * (power - 1) * projector.metric_second
        )
        hessian[2 * power][:, :10, :10] += gravity_coordinate * (
            projector.dewitt @ metric_vertex
        )[None, :, :]
        mixed_vertex = coefficient * (
            power * projector.mixed_first
            + power * (power - 1) * projector.mixed_second
        )
        hessian[2 * power - 1][:, :10, 10] += (
            gravity_root
            * projector.radial[:, None]
            * (mixed_vertex @ projector.dewitt.T)
        )
        hessian[2 * power - 1][:, 10, :10] += (
            gravity_root * projector.radial[:, None] * mixed_vertex
        )
        if power >= 2:
            hessian[2 * (power - 1)][:, 10, 10] += (
                projector.radial**2
                * coefficient
                * (
                    2.0 * power
                    + 4.0 * power * (power - 1) * projector.angular**2
                )
            )
    inverse = [np.zeros_like(hessian[0]) for _ in hessian]
    inverse[0][:] = np.eye(11)
    inverse[0][:, 10, 10] = 1.0 / (1.0 + scalar_mass)
    for power in range(1, maximum_power + 1):
        accumulator = np.zeros_like(hessian[0])
        for partition in range(1, power + 1):
            accumulator += hessian[partition] @ inverse[power - partition]
        inverse[power] = -inverse[0] @ accumulator
    fixed_eta = np.zeros(order + 1)
    scalar_eta = np.zeros(order + 1)
    graviton_weight = 1.0 - 0.5 * eta_newton * (
        1.0 - projector.radial**2
    )
    for power in range(1, order + 1):
        diagonal = np.diagonal(inverse[2 * power], axis1=1, axis2=2)
        fixed_trace = (
            graviton_weight * np.sum(diagonal[:, :10], axis=1)
            + diagonal[:, 10]
        )
        scalar_eta_trace = (
            -0.5 * (1.0 - projector.radial**2) * diagonal[:, 10]
        )
        fixed_eta[power] = (
            np.sum(projector.weights * fixed_trace) / (8.0 * math.pi**2)
        )
        scalar_eta[power] = (
            np.sum(projector.weights * scalar_eta_trace)
            / (8.0 * math.pi**2)
        )
    return fixed_eta, scalar_eta


def analytic_s2(scalar_mass: float) -> float:
    inverse = 1.0 / (1.0 + scalar_mass)
    return (
        24.0
        - (32.0 / 3.0) * inverse
        - (4.0 / 3.0) * inverse**2
        + 4.0 * inverse**3
    )


def analytic_s3(scalar_mass: float) -> float:
    inverse = 1.0 / (1.0 + scalar_mass)
    return math.pi * (
        -96.0
        + 144.0 * inverse
        - 96.0 * inverse**2
        - (224.0 / 5.0) * inverse**3
        + (256.0 / 5.0) * inverse**4
    )


def a2_mass_correction(scalar_mass: float) -> float:
    if scalar_mass < 1.0e-4:
        return (
            -(2.0 / 3.0) * scalar_mass
            - (7.0 / 3.0) * scalar_mass**2
            + 4.0 * scalar_mass**3
            - (16.0 / 3.0) * scalar_mass**4
        )
    return (
        -4.0 * math.log1p(scalar_mass)
        - (4.0 * scalar_mass + 7.0)
        / (3.0 * (1.0 + scalar_mass) ** 2)
        + 7.0 / 3.0
    )


def symbolic_threshold_theorem() -> tuple[list[dict[str, Any]], dict[str, str]]:
    w = sp.symbols("w", positive=True)
    kinetic, c2 = sp.symbols("Y c2", positive=True)
    inverse = 1 / (1 + w)
    source_2 = (
        24
        - sp.Rational(32, 3) * inverse
        - sp.Rational(4, 3) * inverse**2
        + 4 * inverse**3
    )
    primitive = (
        -8 * sp.log(w)
        - 4 * sp.log(1 + w)
        - (4 * w + 7) / (3 * (1 + w) ** 2)
    )
    source_3 = sp.pi * (
        -96
        + 144 * inverse
        - 96 * inverse**2
        - sp.Rational(224, 5) * inverse**3
        + sp.Rational(256, 5) * inverse**4
    )
    pressure = kinetic / 2 + c2 * kinetic**2
    energy = sp.simplify(2 * kinetic * sp.diff(pressure, kinetic) - pressure)
    kinetic_ratio = sp.simplify(
        (energy - kinetic / 2) / (kinetic / 2)
    )
    sound_speed = sp.simplify(
        sp.diff(pressure, kinetic)
        / (
            sp.diff(pressure, kinetic)
            + 2 * kinetic * sp.diff(pressure, kinetic, 2)
        )
    )
    residual = sp.simplify(-2 * w * sp.diff(primitive, w) - source_2)
    checks = {
        "S2_massless": str(sp.simplify(source_2.subs(w, 0) - 16)),
        "S2_primitive": str(residual),
        "S2_large_mass": str(sp.limit(source_2, w, sp.oo)),
        "S3_massless": str(
            sp.simplify(source_3.subs(w, 0) + sp.Rational(208, 5) * sp.pi)
        ),
        "S3_large_mass_over_pi": str(
            sp.simplify(sp.limit(source_3 / sp.pi, w, sp.oo))
        ),
        "X2_energy_ratio": str(sp.simplify(kinetic_ratio - 6 * c2 * kinetic)),
        "X2_sound_shift": str(
            sp.simplify(
                sound_speed - 1
                + 8 * c2 * kinetic / (1 + 12 * c2 * kinetic)
            )
        ),
    }
    rows = tagged(
        [
            {
                "theorem": "two-mass_Litim_threshold",
                "equation": (
                    "q_i,n^(ps,pg)(ws,wg)=[1/n!-eta_i/(2(n+1)!)]"
                    "/[(1+ws)^ps(1+wg)^pg]"
                ),
                "result": "exact optimized-regulator threshold",
                "status": "DERIVED",
            },
            {
                "theorem": "essential_X2_source",
                "equation": str(sp.factor(source_2)),
                "result": "S2(0)=16 and S2(infinity)=24",
                "status": "DERIVED",
            },
            {
                "theorem": "essential_X2_trajectory",
                "equation": str(primitive),
                "result": "-2w dF/dw=S2(w)",
                "status": "DERIVED",
            },
            {
                "theorem": "essential_X3_source",
                "equation": str(sp.expand(source_3)),
                "result": "S3(0)=-208*pi/5 and S3(infinity)=-96*pi",
                "status": "DERIVED",
            },
            {
                "theorem": "Lorentzian_X2_stress_and_sound_cone",
                "equation": (
                    "rho=2Y P_Y-P=Y/2+3c2Y^2; "
                    "c_s^2=(1+4c2Y)/(1+12c2Y)"
                ),
                "result": "rho_X2/rho_kinetic=6c2Y",
                "status": "DERIVED",
            },
        ]
    )
    return rows, checks


def projector_calibration_rows() -> list[dict[str, Any]]:
    projector = functional_px.FunctionalPXProjector(3, QUADRATURE_ORDER)
    gravity = 1.0e-3
    coefficients = np.zeros(4)
    coefficients[1] = 0.5
    rows: list[dict[str, Any]] = []
    comparison_coefficients = np.asarray([0.0, 0.5, -0.013, 0.002])
    original_fixed, original_eta = projector.quantum_coefficients(
        comparison_coefficients,
        0.031,
        -0.27,
    )
    massive_fixed, massive_eta = massive_quantum_coefficients(
        projector,
        comparison_coefficients,
        0.031,
        -0.27,
        0.0,
    )
    massless_equivalence = max(
        float(np.max(np.abs(original_fixed - massive_fixed))),
        float(np.max(np.abs(original_eta - massive_eta))),
    )
    rows.append(
        {
            "coordinate": "full_Hessian",
            "w_mass": 0.0,
            "numerical_source": "",
            "analytic_source": "",
            "absolute_residual": massless_equivalence,
            "relative_residual": massless_equivalence,
            "passed": massless_equivalence == 0.0,
            "status": "EXACT_MASSLESS_PROJECTOR_EQUIVALENCE",
        }
    )
    for scalar_mass in (0.0, 1.0e-6, 0.01, 0.1, 0.585, 1.0, 10.0, 100.0):
        fixed_eta, _ = massive_quantum_coefficients(
            projector,
            coefficients,
            gravity,
            0.0,
            scalar_mass,
        )
        beta_ctilde, beta_d = redundant_sources(
            gravity,
            0.0,
            0.0,
            0.0,
            scalar_mass,
        )
        essential_correction = 8.0 * math.pi * gravity * (
            beta_ctilde + beta_d
        )
        numerical_s2 = (fixed_eta[2] + essential_correction) / gravity**2
        numerical_s3 = fixed_eta[3] / gravity**3
        target_s2 = analytic_s2(scalar_mass)
        target_s3 = analytic_s3(scalar_mass)
        rows.extend(
            [
                {
                    "coordinate": "A2",
                    "w_mass": scalar_mass,
                    "numerical_source": numerical_s2,
                    "analytic_source": target_s2,
                    "absolute_residual": abs(numerical_s2 - target_s2),
                    "relative_residual": abs(numerical_s2 - target_s2)
                    / max(abs(target_s2), 1.0e-300),
                    "passed": math.isclose(
                        numerical_s2,
                        target_s2,
                        rel_tol=3.0e-13,
                        abs_tol=3.0e-13,
                    ),
                    "status": "MASS_DEFORMED_ESSENTIAL_PROJECTOR_CALIBRATION",
                },
                {
                    "coordinate": "A3",
                    "w_mass": scalar_mass,
                    "numerical_source": numerical_s3,
                    "analytic_source": target_s3,
                    "absolute_residual": abs(numerical_s3 - target_s3),
                    "relative_residual": abs(numerical_s3 - target_s3)
                    / max(abs(target_s3), 1.0e-300),
                    "passed": math.isclose(
                        numerical_s3,
                        target_s3,
                        rel_tol=3.0e-13,
                        abs_tol=3.0e-13,
                    ),
                    "status": "MASS_DEFORMED_RAW_PROJECTOR_CALIBRATION",
                },
            ]
        )
    return tagged(rows)


def load_exact_background() -> tuple[Any, dict[str, Any], dict[str, Any]]:
    result = json.loads(
        (
            POST
            / "source-intake"
            / "functional_rg"
            / "5208"
            / "common_minimal_motion_trajectory_results.json"
        ).read_text(encoding="utf-8")
    )
    params = result["fit"]["params"]
    data = (
        checkpoint_5208.checkpoint_5207.checkpoint_5206.checkpoint_5195
        .load_joint_data()
    )
    score = checkpoint_5208.checkpoint_5207.score_calibrated(
        params,
        0.0,
        data,
        accuracy="exact",
        detail=True,
    )
    return score["solution"], score, result


def endpoint_rows() -> dict[str, dict[str, str]]:
    rows = read_csv(
        POST
        / "source-intake"
        / "functional_rg"
        / "4958"
        / "essential_functional_GR_trajectory.csv"
    )
    endpoints: dict[str, dict[str, str]] = {}
    for scheme in ("dynamic_etaN", "reference_etaN0"):
        selected = [
            row
            for row in rows
            if row["scheme"] == scheme and row["polynomial_order"] == "8"
        ]
        selected.sort(key=lambda row: int(row["sample_index"]))
        endpoints[scheme] = selected[-1]
    return endpoints


def log10_sum(log_values: list[float]) -> float:
    finite = [value for value in log_values if math.isfinite(value)]
    if not finite:
        return -math.inf
    maximum = max(finite)
    return maximum + math.log10(
        sum(10.0 ** (value - maximum) for value in finite)
    )


def controlled_background_rows(
    solution: Any,
    result_5208: dict[str, Any],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, float]]:
    physical = result_5208["physical"]
    g_newton = float(physical["G_N_eV_minus2"])
    h0 = float(physical["H0_eV"])
    mass = float(physical["m_gap_eV"])
    j_gap = float(physical["J_gap"])
    reduced_planck = float(physical["M_N_eV"])
    endpoints = endpoint_rows()
    scan_rows: list[dict[str, Any]] = []
    formal_rows: list[dict[str, Any]] = []
    metrics = {
        "maximum_controlled_w": 0.0,
        "minimum_x_at_w_equal_one": math.inf,
        "maximum_relative_A2_mass_correction": 0.0,
        "maximum_abs_X2_kinetic_ratio": 0.0,
        "maximum_abs_Omega_X2": 0.0,
        "maximum_abs_sound_speed_shift": 0.0,
        "maximum_log10_N3_to_N8_kinetic_ratio": -math.inf,
        "minimum_log10_A3_margin_to_X2": math.inf,
        "maximum_g_control": 0.0,
        "maximum_no_overlap_identity_relative_residual": 0.0,
    }
    for scheme, endpoint in endpoints.items():
        g_reference = float(endpoint["g"])
        a2_reference = float(endpoint["A2_a_over_g_power"])
        w_reference = j_gap / g_reference
        higher = {
            order: float(endpoint[f"A{order}_a_over_g_power"])
            for order in range(3, 9)
        }
        for n_value, e_value, q_value in zip(
            solution.background.n_grid,
            solution.background.e_grid,
            solution.q_grid,
            strict=True,
        ):
            n_float = float(n_value)
            e_float = float(e_value)
            q_float = float(q_value)
            q_abs = abs(q_float)
            hubble = h0 * e_float
            kinetic_invariant = (
                reduced_planck**2 * hubble**2 * q_abs**2
            )
            k_control = (kinetic_invariant / X_CONTROL) ** 0.25
            g_control = g_newton * k_control**2
            w_control = (mass / k_control) ** 2
            x_at_threshold = kinetic_invariant / mass**4
            no_overlap_identity = abs(
                x_at_threshold - X_CONTROL / w_control**2
            ) / x_at_threshold
            a2_massless = a2_reference + 8.0 * math.log(
                g_control / g_reference
            )
            mass_delta = (
                a2_mass_correction(w_control)
                - a2_mass_correction(w_reference)
            )
            a2_finite = a2_massless + mass_delta
            g_hubble = g_newton * hubble**2
            c2_y = (
                a2_finite * g_hubble * q_float**2 / (8.0 * math.pi)
            )
            kinetic_ratio = 6.0 * c2_y
            omega_x2 = c2_y * q_float**2
            sound_shift = -8.0 * c2_y / (1.0 + 12.0 * c2_y)
            tail_logs: list[float] = []
            for order, ratio in higher.items():
                if ratio == 0.0 or g_control == 0.0:
                    continue
                tail_logs.append(
                    math.log10(2.0 * (2.0 * order - 1.0) * abs(ratio))
                    + order * math.log10(g_control)
                    + (order - 1.0) * math.log10(X_CONTROL)
                )
            tail_log = log10_sum(tail_logs)
            if abs(kinetic_ratio) > 0.0:
                log_a3_critical = (
                    math.log10(abs(kinetic_ratio))
                    - math.log10(10.0)
                    - 3.0 * math.log10(g_control)
                    - 2.0 * math.log10(X_CONTROL)
                )
                a3_margin = log_a3_critical - math.log10(abs(higher[3]))
            else:
                a3_margin = math.inf
            relative_mass = abs(mass_delta) / max(abs(a2_massless), 1.0)
            scan_rows.append(
                {
                    "scheme": scheme,
                    "N": n_float,
                    "E": e_float,
                    "q_dphi_dN": q_float,
                    "x_control": X_CONTROL,
                    "k_control_eV": k_control,
                    "g_control": g_control,
                    "w_mass_control": w_control,
                    "x_if_w_mass_equals_one": x_at_threshold,
                    "A2_massless": a2_massless,
                    "A2_finite_mass": a2_finite,
                    "A2_mass_delta": mass_delta,
                    "relative_A2_mass_delta": relative_mass,
                    "rho_X2_over_rho_kinetic": kinetic_ratio,
                    "Omega_X2": omega_x2,
                    "sound_speed_squared_minus_one": sound_shift,
                    "log10_abs_N3_to_N8_kinetic_ratio": tail_log,
                    "log10_A3_margin_to_equal_X2": a3_margin,
                    "status": "CONTROLLED_LOCAL_PX_DOMAIN",
                }
            )
            metrics["maximum_controlled_w"] = max(
                metrics["maximum_controlled_w"], w_control
            )
            metrics["minimum_x_at_w_equal_one"] = min(
                metrics["minimum_x_at_w_equal_one"], x_at_threshold
            )
            metrics["maximum_relative_A2_mass_correction"] = max(
                metrics["maximum_relative_A2_mass_correction"], relative_mass
            )
            metrics["maximum_abs_X2_kinetic_ratio"] = max(
                metrics["maximum_abs_X2_kinetic_ratio"], abs(kinetic_ratio)
            )
            metrics["maximum_abs_Omega_X2"] = max(
                metrics["maximum_abs_Omega_X2"], abs(omega_x2)
            )
            metrics["maximum_abs_sound_speed_shift"] = max(
                metrics["maximum_abs_sound_speed_shift"], abs(sound_shift)
            )
            metrics["maximum_log10_N3_to_N8_kinetic_ratio"] = max(
                metrics["maximum_log10_N3_to_N8_kinetic_ratio"], tail_log
            )
            metrics["minimum_log10_A3_margin_to_X2"] = min(
                metrics["minimum_log10_A3_margin_to_X2"], a3_margin
            )
            metrics["maximum_g_control"] = max(
                metrics["maximum_g_control"], g_control
            )
            metrics["maximum_no_overlap_identity_relative_residual"] = max(
                metrics["maximum_no_overlap_identity_relative_residual"],
                no_overlap_identity,
            )
        present = scan_rows[-1]
        for k_over_hubble in (0.01, 1.0, 100.0):
            w_formal = (
                mass
                / (h0 * k_over_hubble)
            ) ** 2
            g_formal = g_newton * (h0 * k_over_hubble) ** 2
            a2_massless = a2_reference + 8.0 * math.log(
                g_formal / g_reference
            )
            mass_delta = (
                a2_mass_correction(w_formal)
                - a2_mass_correction(w_reference)
            )
            formal_rows.append(
                {
                    "scheme": scheme,
                    "k_over_H0": k_over_hubble,
                    "w_mass": w_formal,
                    "A2_massless": a2_massless,
                    "A2_finite_mass": a2_massless + mass_delta,
                    "A2_mass_delta": mass_delta,
                    "controlled_x": X_CONTROL,
                    "present_controlled_w": present["w_mass_control"],
                    "status": "FORMAL_X2_ONLY_NOT_A_FUNCTIONAL_PX_CLAIM",
                }
            )
    return tagged(scan_rows), tagged(formal_rows), metrics


def vacuum_rank_rows(
    metrics: dict[str, float],
    result_5208: dict[str, Any],
) -> tuple[list[dict[str, Any]], dict[str, float]]:
    source_rows = read_csv(
        POST
        / "source-intake"
        / "functional_rg"
        / "5205"
        / "Hamiltonian_constraint_state_normalization.csv"
    )
    k0 = float(
        next(
            row["value"]
            for row in source_rows
            if row["model"] == "ParentScalar_Lambda_zero"
            and row["quantity"] == "unit_regular_energy_kernel_K0"
        )
    )
    sigma_zero = float(
        next(
            row["value"]
            for row in source_rows
            if row["model"] == "ParentScalar_Lambda_zero"
            and row["quantity"] == "sigma_A_squared_from_constraint"
        )
    )
    remainder = k0 * sigma_zero
    alternatives = (0.0, 0.1, 0.5)
    symbolic_k2, symbolic_k4, symbolic_c2, symbolic_sigma2 = sp.symbols(
        "K2 K4 c2 sigma2"
    )
    quadratic_rank = sp.Matrix([[1, symbolic_k2]]).rank()
    nonlinear_rank = sp.Matrix([[1, symbolic_k2, symbolic_c2 * symbolic_k4]]).rank()
    gaussian_rank = sp.Matrix(
        [[1, symbolic_k2 + 6 * symbolic_c2 * symbolic_k4 * symbolic_sigma2]]
    ).rank()
    rows: list[dict[str, Any]] = [
        {
            "case": "quadratic_state",
            "coordinates": "Omega_Lambda,sigma2",
            "constraint": "Omega_Lambda+K2 sigma2=R",
            "jacobian": "[1,K2]",
            "rank": quadratic_rank,
            "nullity": 2 - quadratic_rank,
            "result": "vacuum-state split not selected",
            "status": "EXACT_RANK_THEOREM",
        },
        {
            "case": "nonlinear_PX_even_state",
            "coordinates": "Omega_Lambda,sigma2,sigma4,...",
            "constraint": (
                "Omega_Lambda+K2 sigma2+c2 K4 sigma4+...=R"
            ),
            "jacobian": "[1,K2,c2 K4,...]",
            "rank": nonlinear_rank,
            "nullity": 3 - nonlinear_rank,
            "result": "nonlinear moments increase rather than remove nullity",
            "status": "EXACT_RANK_THEOREM",
        },
        {
            "case": "Gaussian_moment_closure",
            "coordinates": "Omega_Lambda,sigma2",
            "constraint": (
                "Omega_Lambda+K2 sigma2+3c2 K4 sigma2^2+...=R"
            ),
            "jacobian": "[1,K2+6c2 K4 sigma2+...]",
            "rank": gaussian_rank,
            "nullity": 2 - gaussian_rank,
            "result": "even an imposed Gaussian closure does not select Lambda",
            "status": "EXACT_RANK_THEOREM",
        },
    ]
    for omega_lambda in alternatives:
        sigma = (remainder - omega_lambda) / k0
        rows.append(
            {
                "case": f"explicit_positive_solution_OmegaLambda_{omega_lambda:g}",
                "coordinates": "Omega_Lambda,sigma2",
                "constraint": "Omega_Lambda+K2 sigma2=R",
                "jacobian": f"[1,{k0:.16g}]",
                "rank": 1,
                "nullity": 1,
                "Omega_Lambda": omega_lambda,
                "sigma2": sigma,
                "constraint_residual": omega_lambda + k0 * sigma - remainder,
                "result": "positive distinct solution",
                "status": "CONSTRUCTIVE_DEGENERACY_WITNESS",
            }
        )
    physical = result_5208["physical"]
    mass = float(physical["m_gap_eV"])
    reduced_planck = float(physical["M_N_eV"])
    h0 = float(physical["H0_eV"])
    logarithm = float(physical["log_MN_over_H0"])
    vacuum_density_bound = mass**4 * (logarithm + 1.5) / (
        64.0 * math.pi**2
    )
    critical_density = 3.0 * reduced_planck**2 * h0**2
    vacuum_fraction_bound = vacuum_density_bound / critical_density
    rows.append(
        {
            "case": "finite_mass_one_loop_threshold",
            "coordinates": "renormalized_vacuum_coordinate",
            "constraint": (
                "|Delta rho_vac,mass|<=m^4[ln(M_N/H0)+3/2]/(64pi^2)"
            ),
            "rank": "",
            "nullity": "",
            "Omega_Lambda": "",
            "sigma2": "",
            "constraint_residual": "",
            "result": vacuum_fraction_bound,
            "status": "FINITE_MASS_THRESHOLD_BOUND_NOT_ZERO_SELECTION",
        }
    )
    summary = {
        "K0": k0,
        "flatness_remainder": remainder,
        "sigma2_zero_Lambda": sigma_zero,
        "finite_mass_vacuum_density_bound_eV4": vacuum_density_bound,
        "finite_mass_vacuum_fraction_bound": vacuum_fraction_bound,
        "nonlinear_background_fraction_bound": metrics[
            "maximum_abs_Omega_X2"
        ],
    }
    return tagged(rows), summary


def local_maxwell_rows(
    metrics: dict[str, float],
    result_5208: dict[str, Any],
) -> list[dict[str, Any]]:
    physical = result_5208["physical"]
    response = float(physical["maximum_metric_induced_scalar_fraction"])
    tide = float(physical["maximum_local_cosmological_tide_ratio"])
    px_relative = metrics["maximum_abs_X2_kinetic_ratio"]
    sound = metrics["maximum_abs_sound_speed_shift"]
    return tagged(
        [
            {
                "arena": "visible_matter_scalar_charge",
                "equation": "delta S_m[g,Psi]/delta chi=0",
                "residual_bound": 0.0,
                "derivation": "constant F_R and no direct motion portal",
                "status": "EXACT_ZERO",
            },
            {
                "arena": "Maxwell_motion_portal",
                "equation": "delta S_EM[g,A]/delta chi=0",
                "residual_bound": 0.0,
                "derivation": "minimal Maxwell action has no chi dependence",
                "status": "EXACT_ZERO",
            },
            {
                "arena": "Maxwell_stress",
                "equation": (
                    "T_EM_mn=F_ma F_n^a-g_mn F_ab F^ab/4;"
                    " nabla_m T_EM^mn=0 on Maxwell equations"
                ),
                "residual_bound": 0.0,
                "derivation": "metric variation and gauge equation",
                "status": "STANDARD_EXACT_FORM_RETAINED",
            },
            {
                "arena": "Newton_calibration",
                "equation": "M_R^2=(8pi G_N)^-1",
                "residual_bound": 0.0,
                "derivation": "constant-F_R common branch",
                "status": "UNCHANGED_BY_PX",
            },
            {
                "arena": "metric_induced_scalar_response",
                "equation": "relative denominator shift from P_X",
                "residual_bound": response * sound,
                "derivation": (
                    "checkpoint-5208 response times the derived sound-cone shift"
                ),
                "status": "FINITE_PX_CORRECTION_BOUNDED",
            },
            {
                "arena": "homogeneous_scalar_Newtonian_tide",
                "equation": "checkpoint-5208 tide times nonlinear stress fraction",
                "residual_bound": tide * px_relative,
                "derivation": "conservative multiplicative envelope",
                "status": "FINITE_PX_CORRECTION_BOUNDED",
            },
        ]
    )


def decision_rows(
    metrics: dict[str, float],
    vacuum: dict[str, float],
) -> list[dict[str, Any]]:
    return tagged(
        [
            {
                "gate": "finite_mass_essential_PX_threshold",
                "result": (
                    "exact X2/X3 mass-deformed optimized-regulator sources derived"
                ),
                "claim": "DERIVED_IN_DECLARED_ONE_LOOP_ESSENTIAL_QUOTIENT",
                "next_action": "use only in its controlled derivative domain",
            },
            {
                "gate": "threshold_control_overlap",
                "result": (
                    f"max controlled w={metrics['maximum_controlled_w']:.6e}; "
                    f"min x at w=1={metrics['minimum_x_at_w_equal_one']:.6e}"
                ),
                "claim": "NO_OVERLAP_ON_FITTED_BACKGROUND",
                "next_action": "do not evaluate the local polynomial at k~m",
            },
            {
                "gate": "finite_mass_backreaction",
                "result": (
                    "relative A2 threshold change "
                    f"<={metrics['maximum_relative_A2_mass_correction']:.6e}; "
                    "Omega_X2 "
                    f"<={metrics['maximum_abs_Omega_X2']:.6e}"
                ),
                "claim": "BOUNDED_NEGLIGIBLE_IN_CONTROLLED_DOMAIN",
                "next_action": "retain X2 but do not fit it",
            },
            {
                "gate": "vacuum_branch_selection",
                "result": (
                    "Hamiltonian constraint rank remains one and nonlinear "
                    "state moments add null directions"
                ),
                "claim": "PX_CANNOT_DERIVE_LAMBDA_CAL_ZERO",
                "next_action": (
                    "seek a parent vacuum symmetry/renormalization condition or "
                    "retain Lambda_cal=0 as an explicit branch"
                ),
            },
            {
                "gate": "finite_mass_vacuum_loop",
                "result": (
                    f"|Delta Omega_vac|<={vacuum['finite_mass_vacuum_fraction_bound']:.6e}"
                ),
                "claim": "TOO_SMALL_AND_SCHEME_DEPENDENT_TO_SELECT_VACUUM",
                "next_action": "do not identify the finite threshold with dark energy",
            },
            {
                "gate": "local_GR_Newton_Maxwell",
                "result": (
                    "direct matter and Maxwell portals remain exact zero; "
                    "nonlinear propagation and stress corrections are bounded"
                ),
                "claim": "RETAINED_AT_RESOLVED_ORDER",
                "next_action": "move to parent vacuum-coordinate ownership",
            },
            {
                "gate": "full_MTS",
                "result": (
                    "finite-mass local P(X) issue is bounded; absolute vacuum "
                    "selection and all-order nonlocal completion remain open"
                ),
                "claim": "NOT_CLAIMED",
                "next_action": (
                    "DERIVE_PARENT_VACUUM_COORDINATE_OWNERSHIP_OR_PROVE_"
                    "RENORMALIZATION_CONDITION_BOUNDARY"
                ),
            },
        ]
    )


def provenance_rows() -> list[dict[str, Any]]:
    rows = []
    for path, expected in SOURCE_LOCKS.items():
        rows.append(
            {
                "source": path.relative_to(POST).as_posix(),
                "sha256": expected,
                "role": "locked parent evidence",
                "status": "SOURCE_LOCKED",
            }
        )
    rows.extend(
        [
            {
                "source": "SSTwAS.tex equations 684-730 and 1305-1349",
                "sha256": SOURCE_LOCKS[
                    POST
                    / "source-intake"
                    / "functional_rg"
                    / "4937"
                    / "src-2110.09566v1"
                    / "SSTwAS.tex"
                ],
                "role": (
                    "propagator-counted Litim thresholds and c,ctilde,d flows"
                ),
                "status": "PRIMARY_SOURCE_EQUATIONS_USED",
            },
            {
                "source": "checkpoint-5209 symbolic derivation",
                "sha256": "",
                "role": (
                    "two-scale threshold, exact S2 primitive, no-overlap and "
                    "constraint-rank theorems"
                ),
                "status": "NEW_DERIVATION",
            },
        ]
    )
    return tagged(rows)


def build_document(
    symbolic_checks: dict[str, str],
    metrics: dict[str, float],
    vacuum: dict[str, float],
    score: dict[str, Any],
    evidence_digest: str,
) -> str:
    return f"""# 5209 - Finite-Mass Essential `P(X)` Threshold, Backreaction, Vacuum Rank and Local-GR/Maxwell Gate

Private derivation and robustness checkpoint. No GitHub action and no
full-MTS, vacuum-selection or public cosmology claim.

Marker: `{MARKER}`.

## Executive result

The finite motion mass can be inserted into the locked optimized functional
trace without inventing a closure. For scalar and graviton propagator counts
`p_s,p_g`,

```text
q_i,n^(p_s,p_g)(w_s,w_g)
 =[1/n!-eta_i/(2(n+1)!)]
  /[(1+w_s)^p_s(1+w_g)^p_g].
```

After the checkpoint-4958 essential metric quotient, the weak sources are

```text
y=1/(1+w);

S2(w)
 =24-(32/3)y-(4/3)y^2+4y^3;

S3(w)/pi
 =-96+144y-96y^2-(224/5)y^3+(256/5)y^4.
```

Thus `S2(0)=16` and `S3(0)=-208 pi/5`, exactly reproducing the locked
massless coefficients. The mass-deformed numerical Hessian reproduces both
formulae at every calibration point.

## 1. Exact `A2` trajectory

With `w=m_gap^2/k^2`, `dw/d ln k=-2w`, and
`A2=a2/g^2`, the leading essential weak flow is

```text
dA2/d ln k=S2(w).
```

An exact primitive is

```text
F2(w)
 =-8 ln w-4 ln(1+w)-(4w+7)/[3(1+w)^2],

-2w dF2/dw=S2(w).
```

The symbolic residual is `{symbolic_checks['S2_primitive']}`. Relative to
the massless logarithm, the finite-mass correction starts as

```text
Delta A2_mass=-(2/3)w-(7/3)w^2+4w^3+O(w^4).
```

## 2. Scale-consistency/no-overlap theorem

The locked local polynomial projector is controlled for

```text
x=Y/k^4<={X_CONTROL},
Y=M_R^2 H^2 q^2.
```

A finite-mass threshold requires `w=m_gap^2/k^2` of order one. At `w=1`,

```text
x=Y/m_gap^4.
```

The exact fitted checkpoint-5208 background gives

```text
max w inside x<={X_CONTROL}
 ={metrics['maximum_controlled_w']:.12e};

min x when w=1
 ={metrics['minimum_x_at_w_equal_one']:.12e}.
```

Therefore the finite-mass threshold region and the controlled local `P(X)`
polynomial region do not overlap anywhere on `-18<=N<=0`. Evaluating the
whole finite polynomial at `k~m_gap~H0` would place it at an enormous
dimensionless gradient and is not a controlled functional calculation.

Inside the controlled region the maximum relative mass change in `A2` is

```text
{metrics['maximum_relative_A2_mass_correction']:.12e}.
```

This closes the finite-mass question at the resolved local-functional order:
the massless essential trajectory is valid where the local expansion is
valid. The `k~H` rows are retained only as formal `X2`-coefficient
extrapolations, not as a full-`P(X)` claim.

## 3. Cosmological nonlinear-stress bound

For the Lorentzian convention

```text
P(Y)=Y/2+sum_(n>=2) c_n Y^n,
rho_n=(2n-1)c_n Y^n,
M_R^2=(8 pi G_N)^-1,
```

the exact `X2` ratios are

```text
rho_X2/rho_kinetic
 =6 A2 G_N H^2 q^2/(8 pi);

Omega_X2
 =A2 G_N H^2 q^4/(8 pi).
```

Scanning the exact refitted background gives

```text
max |rho_X2/rho_kinetic|
 ={metrics['maximum_abs_X2_kinetic_ratio']:.12e};

max |Omega_X2|
 ={metrics['maximum_abs_Omega_X2']:.12e};

max |c_s^2-1|
 ={metrics['maximum_abs_sound_speed_shift']:.12e}.
```

The resolved `N=3..8` local-polynomial partial sum is at most
`10^({metrics['maximum_log10_N3_to_N8_kinetic_ratio']:.6f})` relative to
the canonical kinetic density. The actual checkpoint-4958 `A3` would need
at least `{metrics['minimum_log10_A3_margin_to_X2']:.6f}` additional orders
of magnitude to equal the already negligible `X2` term.

The exact baseline likelihood replay remains

```text
chi2_joint={float(score['chi2_joint']):.12f}.
```

The derived nonlinear background fraction is far below numerical and
observational resolution, so a refit cannot produce a meaningful parameter
shift.

## 4. Vacuum-rank theorem

For a normalized even regular-mode state, adding nonlinear `P(X)` terms
changes the homogeneous constraint from

```text
Omega_Lambda+K2 sigma2=R
```

to

```text
Omega_Lambda+K2 sigma2+c2 K4 sigma4+...=R.
```

The first Jacobian is `[1,K2]`, with rank one and nullity one. The nonlinear
Jacobian is `[1,K2,c2 K4,...]`, still rank one but with at least two null
directions. Even imposing the un-derived Gaussian closure
`sigma4=3 sigma2^2` leaves one equation for
`{{Omega_Lambda,sigma2}}`.

Three explicit positive witnesses are generated from the locked
checkpoint-5205 row. Therefore essential `P(X)` cannot select
`Lambda_cal=0`; it makes the state-moment degeneracy larger unless an
independent parent state law fixes every required moment.

The conservative finite mass-dependent one-loop vacuum piece obeys

```text
|Delta Omega_vac,mass|
 <={vacuum['finite_mass_vacuum_fraction_bound']:.12e}.
```

It is both renormalization-condition dependent and far too small to select
the observed vacuum split.

## 5. Local GR, Newton and Maxwell

On the selected constant-`F_R` branch,

```text
delta S_m/delta chi =0;
delta S_EM/delta chi=0.
```

The standard Maxwell stress tensor and its on-shell conservation law remain
unchanged. `P(X)` changes only the motion stress and scalar principal
operator. Its sound-cone and stress corrections are bounded above, so the
checkpoint-5208 local response and cosmological-tide bounds are unchanged
to the displayed accuracy. Newton calibration remains
`M_R^2=(8 pi G_N)^-1`.

## 6. Decision

```text
mass-deformed optimized threshold              = derived;
essential X2 and X3 weak sources               = derived and calibrated;
exact finite-mass A2 primitive                 = derived;
controlled-PX / finite-mass overlap            = excluded on fitted history;
finite-mass nonlinear cosmology backreaction   = bounded negligible;
direct material scalar charge                  = exact zero;
direct Maxwell-motion portal                   = exact zero;
Newton calibration                             = unchanged;
Lambda_cal=0 from P(X)                         = rejected by rank theorem;
parent vacuum-coordinate selection             = still open;
all-order nonlocal effective action             = still open;
full MTS unification                           = not claimed.
```

The next target is not another finite-polynomial scan. It is

```text
DERIVE_PARENT_VACUUM_COORDINATE_OWNERSHIP_OR_PROVE_THAT_LAMBDA_CAL_IS_
AN_INDEPENDENT_RENORMALIZATION_CONDITION.
```

## 7. Evidence

Generator:

`scripts/Y5_R2FR_5209_finite_mass_PX_vacuum_branch_gate.py`

Evidence directory:

`source-intake/functional_rg/5209/`

Evidence CSV digest:

`{evidence_digest}`

Validation:

`source-intake/mts_residuals/P8_Y5_BRR545_5209_VALIDATION.csv`
"""


def validation_rows(
    symbolic_checks: dict[str, str],
    calibrations: list[dict[str, Any]],
    metrics: dict[str, float],
    vacuum_rows: list[dict[str, Any]],
    vacuum: dict[str, float],
    local_rows: list[dict[str, Any]],
    score: dict[str, Any],
    result_5208: dict[str, Any],
    evidence_digest: str,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check: str, passed: bool, value: Any) -> None:
        rows.append(
            {
                "check": check,
                "status": "PASS" if passed else "FAIL",
                "value": value,
                "checkpoint": CHECKPOINT,
                "marker": MARKER,
                "valid_for_full_MTS_claim": False,
            }
        )

    for path, expected in SOURCE_LOCKS.items():
        add(
            f"source_lock::{path.relative_to(POST).as_posix()}",
            path.is_file() and file_digest(path) == expected,
            expected,
        )
    for name, value in symbolic_checks.items():
        expected = {
            "S2_massless": "0",
            "S2_primitive": "0",
            "S2_large_mass": "24",
            "S3_massless": "0",
            "S3_large_mass_over_pi": "-96",
            "X2_energy_ratio": "0",
            "X2_sound_shift": "0",
        }[name]
        add(f"symbolic::{name}", value == expected, value)
    add(
        "projector_calibration_all_pass",
        all(bool(row["passed"]) for row in calibrations),
        max(float(row["relative_residual"]) for row in calibrations),
    )
    add(
        "controlled_mass_threshold_small",
        metrics["maximum_controlled_w"] < 1.0e-40,
        metrics["maximum_controlled_w"],
    )
    add(
        "threshold_region_outside_polynomial_control",
        metrics["minimum_x_at_w_equal_one"] > 1.0e80,
        metrics["minimum_x_at_w_equal_one"],
    )
    add(
        "no_overlap_identity",
        metrics["maximum_no_overlap_identity_relative_residual"] < 1.0e-12,
        metrics["maximum_no_overlap_identity_relative_residual"],
    )
    add(
        "finite_mass_A2_correction_negligible",
        metrics["maximum_relative_A2_mass_correction"] < 1.0e-40,
        metrics["maximum_relative_A2_mass_correction"],
    )
    add(
        "X2_kinetic_backreaction_negligible",
        metrics["maximum_abs_X2_kinetic_ratio"] < 1.0e-100,
        metrics["maximum_abs_X2_kinetic_ratio"],
    )
    add(
        "X2_total_backreaction_negligible",
        metrics["maximum_abs_Omega_X2"] < 1.0e-100,
        metrics["maximum_abs_Omega_X2"],
    )
    add(
        "sound_cone_shift_negligible",
        metrics["maximum_abs_sound_speed_shift"] < 1.0e-100,
        metrics["maximum_abs_sound_speed_shift"],
    )
    add(
        "resolved_N3_N8_tail_below_X2",
        metrics["maximum_log10_N3_to_N8_kinetic_ratio"]
        < math.log10(metrics["maximum_abs_X2_kinetic_ratio"]) - 40.0,
        metrics["maximum_log10_N3_to_N8_kinetic_ratio"],
    )
    add(
        "A3_margin_over_forty_orders",
        metrics["minimum_log10_A3_margin_to_X2"] > 40.0,
        metrics["minimum_log10_A3_margin_to_X2"],
    )
    rank_rows = [
        row for row in vacuum_rows if row["status"] == "EXACT_RANK_THEOREM"
    ]
    add(
        "vacuum_rank_rows",
        [int(row["rank"]) for row in rank_rows] == [1, 1, 1],
        [row["rank"] for row in rank_rows],
    )
    witnesses = [
        row
        for row in vacuum_rows
        if row["status"] == "CONSTRUCTIVE_DEGENERACY_WITNESS"
    ]
    add(
        "vacuum_distinct_positive_witnesses",
        len(witnesses) == 3
        and all(float(row["sigma2"]) > 0.0 for row in witnesses)
        and max(abs(float(row["constraint_residual"])) for row in witnesses)
        < 1.0e-14,
        [row["sigma2"] for row in witnesses],
    )
    add(
        "finite_mass_vacuum_piece_negligible",
        vacuum["finite_mass_vacuum_fraction_bound"] < 1.0e-100,
        vacuum["finite_mass_vacuum_fraction_bound"],
    )
    exact_local = [
        row
        for row in local_rows
        if row["status"]
        in {"EXACT_ZERO", "STANDARD_EXACT_FORM_RETAINED", "UNCHANGED_BY_PX"}
    ]
    add(
        "local_exact_zero_and_standard_rows",
        len(exact_local) == 4
        and all(float(row["residual_bound"]) == 0.0 for row in exact_local),
        len(exact_local),
    )
    add(
        "baseline_exact_likelihood_replay",
        abs(
            float(score["chi2_joint"])
            - float(result_5208["fit"]["chi2_joint"])
        )
        < 1.0e-8,
        float(score["chi2_joint"]),
    )
    output_csvs = sorted(OUT.glob("*.csv"))
    add(
        "evidence_csv_digest",
        selected_digest(output_csvs, OUT) == evidence_digest,
        evidence_digest,
    )
    for path in output_csvs:
        parsed = read_csv(path)
        add(
            f"csv_parse::{path.name}",
            bool(parsed),
            len(parsed),
        )
    source_text = Path(__file__).read_text(encoding="utf-8")
    try:
        ast.parse(source_text)
        ast_ok = True
    except SyntaxError:
        ast_ok = False
    add("script_AST", ast_ok, len(source_text))
    add("document_exists", DOCUMENT.is_file(), DOCUMENT)
    add(
        "formal_tree_unchanged",
        checkpoint_5208.tree_digest(FORMAL) == FORMAL_LOCK,
        checkpoint_5208.tree_digest(FORMAL),
    )
    public_head, public_status = checkpoint_5208.git_state(PUBLIC)
    galaxy_head, galaxy_status = checkpoint_5208.git_state(GALAXY)
    add(
        "public_head_unchanged",
        public_head == PUBLIC_HEAD,
        public_head,
    )
    add(
        "public_worktree_clean",
        public_status == [],
        public_status,
    )
    add(
        "galaxy_head_unchanged",
        galaxy_head == GALAXY_HEAD,
        galaxy_head,
    )
    add(
        "galaxy_dirty_paths_unchanged",
        galaxy_status == GALAXY_DIRTY,
        galaxy_status,
    )
    add(
        "no_script_pycache",
        not (POST / "scripts" / "__pycache__").exists(),
        POST / "scripts" / "__pycache__",
    )
    return rows


def run_checkpoint() -> None:
    source_hashes = assert_source_locks()
    threshold_rows, symbolic_checks = symbolic_threshold_theorem()
    if any(
        symbolic_checks[name] != expected
        for name, expected in {
            "S2_massless": "0",
            "S2_primitive": "0",
            "S2_large_mass": "24",
            "S3_massless": "0",
            "S3_large_mass_over_pi": "-96",
            "X2_energy_ratio": "0",
            "X2_sound_shift": "0",
        }.items()
    ):
        raise RuntimeError(f"symbolic threshold failure: {symbolic_checks}")
    calibrations = projector_calibration_rows()
    if not all(bool(row["passed"]) for row in calibrations):
        raise RuntimeError("mass-deformed projector calibration failed")
    solution, score, result_5208 = load_exact_background()
    scan_rows, formal_rows, metrics = controlled_background_rows(
        solution,
        result_5208,
    )
    vacuum_rows, vacuum = vacuum_rank_rows(metrics, result_5208)
    local_rows = local_maxwell_rows(metrics, result_5208)
    decisions = decision_rows(metrics, vacuum)
    provenance = provenance_rows()
    datasets = {
        "finite_mass_threshold_theorem.csv": threshold_rows,
        "mass_deformed_projector_calibration.csv": calibrations,
        "controlled_PX_background_scan.csv": scan_rows,
        "formal_X2_mass_threshold_extrapolation.csv": formal_rows,
        "vacuum_constraint_rank_and_threshold.csv": vacuum_rows,
        "local_GR_Newton_Maxwell_residuals.csv": local_rows,
        "route_decision.csv": decisions,
        "source_provenance.csv": provenance,
    }
    OUT.mkdir(parents=True, exist_ok=True)
    for name, rows in datasets.items():
        write_csv(OUT / name, rows)
    evidence_digest = selected_digest(
        [OUT / name for name in datasets],
        OUT,
    )
    result = {
        "checkpoint": CHECKPOINT,
        "marker": MARKER,
        "checked_date": CHECKED_DATE,
        "claim_status": "PRIVATE_RESOLVED_ORDER_NO_FULL_MTS_CLAIM",
        "source_hashes": source_hashes,
        "symbolic_checks": symbolic_checks,
        "metrics": metrics,
        "vacuum": vacuum,
        "baseline_chi2_joint": float(score["chi2_joint"]),
        "evidence_csv_sha256": evidence_digest,
        "formal_tree_sha256": checkpoint_5208.tree_digest(FORMAL),
        "selected_next_route": (
            "DERIVE_PARENT_VACUUM_COORDINATE_OWNERSHIP_OR_PROVE_"
            "RENORMALIZATION_CONDITION_BOUNDARY"
        ),
    }
    write_json(OUT / "finite_mass_PX_vacuum_branch_results.json", result)
    DOCUMENT.write_text(
        build_document(
            symbolic_checks,
            metrics,
            vacuum,
            score,
            evidence_digest,
        ),
        encoding="utf-8",
    )
    validation = validation_rows(
        symbolic_checks,
        calibrations,
        metrics,
        vacuum_rows,
        vacuum,
        local_rows,
        score,
        result_5208,
        evidence_digest,
    )
    write_csv(VALIDATION, validation)
    failures = [row for row in validation if row["status"] != "PASS"]
    if failures:
        raise RuntimeError(f"validation failures: {failures}")
    print(
        json.dumps(
            {
                "checkpoint": CHECKPOINT,
                "validation": f"{len(validation)}/{len(validation)} PASS",
                "maximum_controlled_w": metrics["maximum_controlled_w"],
                "minimum_x_at_w_equal_one": metrics[
                    "minimum_x_at_w_equal_one"
                ],
                "maximum_abs_Omega_X2": metrics["maximum_abs_Omega_X2"],
                "finite_mass_vacuum_fraction_bound": vacuum[
                    "finite_mass_vacuum_fraction_bound"
                ],
                "selected_next_route": result["selected_next_route"],
                "evidence_csv_sha256": evidence_digest,
                "formal_tree_sha256": result["formal_tree_sha256"],
            },
            indent=2,
        )
    )


def validate_saved() -> None:
    assert_source_locks()
    result_path = OUT / "finite_mass_PX_vacuum_branch_results.json"
    if not result_path.is_file() or not VALIDATION.is_file() or not DOCUMENT.is_file():
        raise RuntimeError("checkpoint-5209 saved products are incomplete")
    result = json.loads(result_path.read_text(encoding="utf-8"))
    validation = read_csv(VALIDATION)
    failures = [row for row in validation if row["status"] != "PASS"]
    if failures:
        raise RuntimeError(f"saved validation failures: {failures}")
    csv_paths = sorted(OUT.glob("*.csv"))
    actual_digest = selected_digest(csv_paths, OUT)
    if actual_digest != result["evidence_csv_sha256"]:
        raise RuntimeError("checkpoint-5209 evidence digest changed")
    if checkpoint_5208.tree_digest(FORMAL) != FORMAL_LOCK:
        raise RuntimeError("formalization-workbench changed")
    public_head, public_status = checkpoint_5208.git_state(PUBLIC)
    galaxy_head, galaxy_status = checkpoint_5208.git_state(GALAXY)
    if public_head != PUBLIC_HEAD or public_status:
        raise RuntimeError("public worktree changed")
    if galaxy_head != GALAXY_HEAD or galaxy_status != GALAXY_DIRTY:
        raise RuntimeError("galaxy repository changed")
    if (POST / "scripts" / "__pycache__").exists():
        raise RuntimeError("script __pycache__ exists")
    print(
        json.dumps(
            {
                "saved_validation": f"{len(validation)}/{len(validation)} PASS",
                "evidence_csv_sha256": actual_digest,
                "formal_tree_sha256": checkpoint_5208.tree_digest(FORMAL),
            },
            indent=2,
        )
    )


def dry_run() -> None:
    assert_source_locks()
    _, symbolic_checks = symbolic_threshold_theorem()
    calibrations = projector_calibration_rows()
    print(
        json.dumps(
            {
                "dry_run": "PASS",
                "symbolic_checks": symbolic_checks,
                "projector_rows": len(calibrations),
                "projector_all_pass": all(
                    bool(row["passed"]) for row in calibrations
                ),
                "formal_tree_sha256": checkpoint_5208.tree_digest(FORMAL),
            },
            indent=2,
        )
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--validate-saved", action="store_true")
    arguments = parser.parse_args()
    if arguments.dry_run:
        dry_run()
    elif arguments.validate_saved:
        validate_saved()
    else:
        run_checkpoint()


if __name__ == "__main__":
    main()
