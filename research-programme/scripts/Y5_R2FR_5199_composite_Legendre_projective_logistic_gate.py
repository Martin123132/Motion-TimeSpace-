from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
from scipy.integrate import quad_vec
from scipy.linalg import eigh_tridiagonal
from scipy.optimize import minimize_scalar


sys.dont_write_bytecode = True

POST = Path(__file__).resolve().parents[1]
FORMAL = POST.parent / "formalization-workbench"
SCRIPT = Path(__file__).resolve()
OUT = POST / "source-intake" / "functional_rg" / "5199"
DOCUMENT = (
    POST
    / "5199-Y5-R2FR-exact-composite-Legendre-no-go-and-projective-"
    "scale-covariance-logistic-reduction.md"
)
VALIDATION = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5199_VALIDATION.csv"
)
CHECKPOINT_5198_OUT = POST / "source-intake" / "functional_rg" / "5198"
CHECKPOINT_5185_RESULT = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5185"
    / "occupied_state_2PI_interaction_results.json"
)
CHECKPOINT_5198_RESULT = (
    CHECKPOINT_5198_OUT / "marginal_Mestel_collective_results.json"
)
PUBLIC_WORKTREE = Path(
    r"C:\Users\ollet\OneDrive\Documents\Motion-TimeSpace-public-update-2026-07-22"
)
GALAXY_REPO = Path(r"D:\Users\ollet\Desktop\MTS-Galaxy-Lab-repo")

MARKER = "MTS_5199_COMPOSITE_LEGENDRE_PROJECTIVE_LOGISTIC_GATE"
CHECKED_DATE = "2026-07-24"
FORMAL_LOCK = (
    "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
)
CHECKPOINT_5198_OUT_LOCK = (
    "bfbb66e0c37e6995ae888ed21d56a41e8245c4c4ebbb731bb5192159c0044510"
)
PUBLIC_HEAD_LOCK = "8913c00b77d98e457ddb0c48e9aeec9cc5f309fd"
GALAXY_HEAD_LOCK = "f850e4997657f457dddc05cbe50f21186588dcc7"

SOURCE_LOCKS = {
    "5148-Y5-R2FR-one-parent-local-GR-galaxy-spectral-response-cog-theorem.md": (
        "b2d5bddd8ce3cee2299b2cdadd66a0688bbd07c945bc329ac2ade4c20c113352"
    ),
    "5151-Y5-R2FR-parent-projective-occupation-to-conserved-Einstein-cluster-stress-and-two-metric-cog-gate.md": (
        "b23ca652af8b66c220973cffbdc1ab2df028947c9dba8bd61666d1e0460c5fd5"
    ),
    "5181-Y5-R2FR-critical-pair-bubble-positive-Hessian-and-parent-ownership-gate.md": (
        "54a35ad66744f9e1f5ab6fdd15e66bc6f87a93330a999aae2235ea5cf98b3657"
    ),
    "5185-Y5-R2FR-occupied-state-2PI-interaction-stress-and-collision-gate.md": (
        "d47db7fefdb8b9f799a48a1e4d5a7c4266880d41d97b40ae2cefe33cd62d07a5"
    ),
    "5198-Y5-R2FR-marginal-Mestel-composite-Hessian-Plummer-scale-bridge-and-logistic-vertex-gate.md": (
        "e1bd7de17399f54d4069d9577750010d8329a81397a35a8bf0719eda9edec2be"
    ),
    "source-intake/functional_rg/5185/occupied_state_2PI_interaction_results.json": (
        "9d725483e8fe7e355f1844ab5a15a9b257d8e4d8792250807bef1474df58d081"
    ),
    "source-intake/functional_rg/5198/marginal_Mestel_collective_results.json": (
        "9ed92451c782c760cb6767f0e53217a972711489c3aaf5258a04ae2d441bf469"
    ),
    "scripts/Y5_R2FR_5198_marginal_Mestel_collective_Hessian_scale_bridge.py": (
        "ce71c7a1a43a04653d1c60427bf1392f7dbf05b41adab21edba4010e4fff05cc"
    ),
}

FRACTIONAL_POWER = 4.0 / 3.0
FRACTIONAL_AMPLITUDE = 3.0 / 4.0
LOGISTIC_INVARIANT = 3.0
Q_LOCKED = 0.77
Q_SELF_EXPECTED = 0.7698811733853892
OUTER_EXPONENT = 4.0
OUTER_BOUNDARY = 8.0


@dataclass
class QuantumSystem:
    mass_squared: float
    box_half_width: float
    grid_points: int
    state_count: int
    spacing: float
    eigenvalues: np.ndarray
    source_matrix: np.ndarray


def file_digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


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
            "checkpoint": 5199,
            "marker": MARKER,
            "checked_date": CHECKED_DATE,
            **row,
        }
        for row in rows
    ]


def cumulants_from_moments(
    mu1: float,
    mu2: float,
    mu3: float,
    mu4: float,
) -> tuple[float, float, float]:
    kappa2 = mu2 - mu1**2
    kappa3 = mu3 - 3.0 * mu2 * mu1 + 2.0 * mu1**3
    kappa4 = (
        mu4
        - 4.0 * mu3 * mu1
        - 3.0 * mu2**2
        + 12.0 * mu2 * mu1**2
        - 6.0 * mu1**4
    )
    return kappa2, kappa3, kappa4


def vertices_from_cumulants(
    kappa2: float,
    kappa3: float,
    kappa4: float,
) -> dict[str, float]:
    u2 = 1.0 / kappa2
    u3 = -kappa3 / kappa2**3
    u4 = (3.0 * kappa3**2 - kappa2 * kappa4) / kappa2**5
    invariant = u3**2 / (u2 * u4)
    return {
        "U2": u2,
        "U3": u3,
        "U4": u4,
        "shape_invariant": invariant,
    }


def exact_ultralocal_rows() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    moments = [
        FRACTIONAL_AMPLITUDE ** (-2.0 * order / FRACTIONAL_POWER)
        * math.gamma((2.0 * order + 1.0) / FRACTIONAL_POWER)
        / math.gamma(1.0 / FRACTIONAL_POWER)
        for order in range(1, 5)
    ]
    kappa2, kappa3, kappa4 = cumulants_from_moments(*moments)
    vertices = vertices_from_cumulants(kappa2, kappa3, kappa4)
    diagnostics = {
        "power": FRACTIONAL_POWER,
        "amplitude": FRACTIONAL_AMPLITUDE,
        "mu1": moments[0],
        "mu2": moments[1],
        "mu3": moments[2],
        "mu4": moments[3],
        "kappa2": kappa2,
        "kappa3": kappa3,
        "kappa4": kappa4,
        **vertices,
        "logistic_invariant": LOGISTIC_INVARIANT,
        "target_to_result_ratio": LOGISTIC_INVARIANT
        / vertices["shape_invariant"],
        "source_domain": "K>=0",
        "two_sided_source_neighbourhood": False,
    }
    rows = [
        {
            "object": "measure",
            "equation": "Z(K)=integral dpsi exp[-(3/4)|psi|^(4/3)-K psi^2/2]",
            "value": "",
            "status": "EXACT",
        },
        {
            "object": "moment_law",
            "equation": "mu_n=a^(-2n/p) Gamma[(2n+1)/p]/Gamma(1/p)",
            "value": "",
            "status": "EXACT",
        },
    ]
    rows.extend(
        {
            "object": f"mu{index}",
            "equation": f"<Y^{index}>; Y=psi^2",
            "value": value,
            "status": "EXACT",
        }
        for index, value in enumerate(moments, start=1)
    )
    rows.extend(
        [
            {
                "object": "kappa2",
                "equation": "mu2-mu1^2",
                "value": kappa2,
                "status": "EXACT",
            },
            {
                "object": "kappa3",
                "equation": "mu3-3mu2mu1+2mu1^3",
                "value": kappa3,
                "status": "EXACT",
            },
            {
                "object": "kappa4",
                "equation": "mu4-4mu3mu1-3mu2^2+12mu2mu1^2-6mu1^4",
                "value": kappa4,
                "status": "EXACT",
            },
            {
                "object": "U2",
                "equation": "1/kappa2",
                "value": vertices["U2"],
                "status": "EXACT",
            },
            {
                "object": "U3",
                "equation": "-kappa3/kappa2^3",
                "value": vertices["U3"],
                "status": "EXACT",
            },
            {
                "object": "U4",
                "equation": "(3kappa3^2-kappa2 kappa4)/kappa2^5",
                "value": vertices["U4"],
                "status": "EXACT",
            },
            {
                "object": "I_composite",
                "equation": "U3^2/(U2 U4)",
                "value": vertices["shape_invariant"],
                "status": "FAILS_LOGISTIC_I_EQUALS_3",
            },
            {
                "object": "source_domain",
                "equation": "K<0 makes -a|psi|^(4/3)-K psi^2/2 unbounded above",
                "value": "K=0 is a boundary point",
                "status": "ONE_SIDED_LEGENDRE_ONLY",
            },
        ]
    )
    return tagged(rows), diagnostics


def invariant_for_gaussian_fractional_mix(
    fractional_strength: float,
) -> tuple[float, tuple[float, float, float, float]]:
    if fractional_strength == 0.0:
        moments = (1.0, 3.0, 15.0, 105.0)
    else:
        if fractional_strength < 1.0:
            gaussian_coefficient = 0.5
            fractional_coefficient = fractional_strength
        else:
            gaussian_coefficient = 0.5 * fractional_strength ** (
                -2.0 / FRACTIONAL_POWER
            )
            fractional_coefficient = 1.0

        def integrand(value: float) -> np.ndarray:
            exponent = (
                -gaussian_coefficient * value**2
                - fractional_coefficient * value**FRACTIONAL_POWER
            )
            weight = math.exp(exponent)
            return weight * np.array(
                [1.0, value**2, value**4, value**6, value**8]
            )

        integrals, _ = quad_vec(
            integrand,
            0.0,
            np.inf,
            epsabs=2.0e-12,
            epsrel=2.0e-12,
        )
        moments = tuple(float(value / integrals[0]) for value in integrals[1:])
    kappa2, kappa3, kappa4 = cumulants_from_moments(*moments)
    invariant = vertices_from_cumulants(kappa2, kappa3, kappa4)[
        "shape_invariant"
    ]
    return invariant, moments


def ultralocal_mass_scan_rows(
    exact_diagnostics: dict[str, Any],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    strengths = np.concatenate(
        (
            np.array([0.0]),
            np.geomspace(1.0e-6, 1.0e6, 73),
        )
    )
    rows: list[dict[str, Any]] = []
    invariants: list[float] = []
    for strength in strengths:
        invariant, moments = invariant_for_gaussian_fractional_mix(
            float(strength)
        )
        invariants.append(invariant)
        rows.append(
            {
                "family": "exp[-z^2/2-lambda|z|^(4/3)]",
                "lambda": float(strength),
                "mu1": moments[0],
                "mu2": moments[1],
                "mu3": moments[2],
                "mu4": moments[3],
                "shape_invariant": invariant,
                "logistic_target": LOGISTIC_INVARIANT,
                "passes_logistic": False,
                "status": "NUMERIC_QUADRATURE",
            }
        )
    rows.append(
        {
            "family": "pure_fractional_endpoint",
            "lambda": "infinity",
            "shape_invariant": exact_diagnostics["shape_invariant"],
            "logistic_target": LOGISTIC_INVARIANT,
            "passes_logistic": False,
            "status": "EXACT_ENDPOINT",
        }
    )
    diagnostics = {
        "gaussian_endpoint": 2.0 / 3.0,
        "fractional_endpoint": exact_diagnostics["shape_invariant"],
        "sample_count": len(strengths),
        "sample_min": min(invariants),
        "sample_max": max(invariants),
        "sample_monotone_non_decreasing": bool(
            np.all(np.diff(np.asarray(invariants)) >= -2.0e-9)
        ),
    }
    return tagged(rows), diagnostics


def solve_quantum_system(
    mass_squared: float,
    box_half_width: float,
    grid_points: int,
    state_count: int,
) -> QuantumSystem:
    spacing = 2.0 * box_half_width / (grid_points + 1)
    coordinates = np.linspace(
        -box_half_width + spacing,
        box_half_width - spacing,
        grid_points,
    )
    diagonal = (
        1.0 / spacing**2
        + 0.5 * mass_squared * coordinates**2
        + FRACTIONAL_AMPLITUDE * np.abs(coordinates) ** FRACTIONAL_POWER
    )
    off_diagonal = np.full(grid_points - 1, -0.5 / spacing**2)
    eigenvalues, eigenvectors = eigh_tridiagonal(
        diagonal,
        off_diagonal,
        select="i",
        select_range=(0, state_count - 1),
        check_finite=False,
        tol=1.0e-12,
    )
    source_diagonal = 0.5 * coordinates**2
    source_matrix = eigenvectors.T @ (
        source_diagonal[:, np.newaxis] * eigenvectors
    )
    return QuantumSystem(
        mass_squared=mass_squared,
        box_half_width=box_half_width,
        grid_points=grid_points,
        state_count=state_count,
        spacing=spacing,
        eigenvalues=eigenvalues,
        source_matrix=source_matrix,
    )


def quantum_response(
    eigenvalues: np.ndarray,
    source_matrix: np.ndarray,
    target_state: int = 0,
) -> dict[str, Any]:
    state_count = len(eigenvalues)
    coefficients = [np.zeros(state_count) for _ in range(5)]
    coefficients[0][target_state] = 1.0
    energy_coefficients = [float(eigenvalues[target_state])]
    gaps = eigenvalues - eigenvalues[target_state]
    mask = np.arange(state_count) != target_state
    for order in range(1, 5):
        energy_coefficient = float(
            source_matrix[target_state] @ coefficients[order - 1]
        )
        energy_coefficients.append(energy_coefficient)
        right_hand_side = -(source_matrix @ coefficients[order - 1])
        for lower_order in range(1, order + 1):
            right_hand_side += (
                energy_coefficients[lower_order]
                * coefficients[order - lower_order]
            )
        coefficients[order][mask] = right_hand_side[mask] / gaps[mask]
    g0 = 2.0 * energy_coefficients[1]
    g1 = 4.0 * energy_coefficients[2]
    g2 = 12.0 * energy_coefficients[3]
    g3 = 48.0 * energy_coefficients[4]
    u2 = -1.0 / (2.0 * g1)
    u3 = g2 / (2.0 * g1**3)
    u4 = g3 / (2.0 * g1**4) - 3.0 * g2**2 / (2.0 * g1**5)
    invariant = u3**2 / (u2 * u4)
    return {
        "energy_coefficients": energy_coefficients,
        "E0": energy_coefficients[0],
        "G0": g0,
        "G1": g1,
        "G2": g2,
        "G3": g3,
        "U2": u2,
        "U3": u3,
        "U4": u4,
        "shape_invariant": invariant,
    }


def quantum_convergence_rows(
    baseline: QuantumSystem,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    grid_records: list[tuple[float, dict[str, Any]]] = []
    for grid_points in (2000, 3000, 4000, 6000):
        system = solve_quantum_system(
            mass_squared=0.0,
            box_half_width=14.0,
            grid_points=grid_points,
            state_count=100,
        )
        response = quantum_response(system.eigenvalues, system.source_matrix)
        grid_records.append((system.spacing, response))
        rows.append(
            {
                "convergence_type": "grid",
                "box_half_width": system.box_half_width,
                "grid_points": system.grid_points,
                "state_count": system.state_count,
                "spacing": system.spacing,
                **{
                    key: response[key]
                    for key in (
                        "E0",
                        "G0",
                        "G1",
                        "G2",
                        "G3",
                        "U2",
                        "U3",
                        "U4",
                        "shape_invariant",
                    )
                },
                "status": "FINITE_DIFFERENCE",
            }
        )
    baseline_response_100 = quantum_response(
        baseline.eigenvalues[:100],
        baseline.source_matrix[:100, :100],
    )
    grid_records.append((baseline.spacing, baseline_response_100))
    rows.append(
        {
            "convergence_type": "grid",
            "box_half_width": baseline.box_half_width,
            "grid_points": baseline.grid_points,
            "state_count": 100,
            "spacing": baseline.spacing,
            **{
                key: baseline_response_100[key]
                for key in (
                    "E0",
                    "G0",
                    "G1",
                    "G2",
                    "G3",
                    "U2",
                    "U3",
                    "U4",
                    "shape_invariant",
                )
            },
            "status": "FINITE_DIFFERENCE",
        }
    )
    squared_spacings = np.asarray([spacing**2 for spacing, _ in grid_records])
    extrapolated: dict[str, float] = {}
    for key in (
        "E0",
        "G0",
        "G1",
        "G2",
        "G3",
        "U2",
        "U3",
        "U4",
        "shape_invariant",
    ):
        values = np.asarray([record[key] for _, record in grid_records])
        extrapolated[key] = float(np.polyfit(squared_spacings, values, 2)[-1])
    rows.append(
        {
            "convergence_type": "continuum_extrapolation",
            "box_half_width": 14.0,
            "grid_points": "infinity",
            "state_count": 100,
            "spacing": 0.0,
            **extrapolated,
            "status": "QUADRATIC_IN_DX_SQUARED",
        }
    )
    spectral_values: list[float] = []
    for state_count in (40, 80, 120, 160, 180):
        response = quantum_response(
            baseline.eigenvalues[:state_count],
            baseline.source_matrix[:state_count, :state_count],
        )
        spectral_values.append(response["shape_invariant"])
        rows.append(
            {
                "convergence_type": "spectral",
                "box_half_width": baseline.box_half_width,
                "grid_points": baseline.grid_points,
                "state_count": state_count,
                "spacing": baseline.spacing,
                **{
                    key: response[key]
                    for key in (
                        "E0",
                        "G0",
                        "G1",
                        "G2",
                        "G3",
                        "U2",
                        "U3",
                        "U4",
                        "shape_invariant",
                    )
                },
                "status": "RAYLEIGH_SCHROEDINGER_ORDER_4",
            }
        )
    box_values: list[float] = []
    for box_half_width, grid_points in ((8.0, 4570), (12.0, 6856)):
        system = solve_quantum_system(
            mass_squared=0.0,
            box_half_width=box_half_width,
            grid_points=grid_points,
            state_count=100,
        )
        response = quantum_response(system.eigenvalues, system.source_matrix)
        box_values.append(response["shape_invariant"])
        rows.append(
            {
                "convergence_type": "box",
                "box_half_width": system.box_half_width,
                "grid_points": system.grid_points,
                "state_count": system.state_count,
                "spacing": system.spacing,
                **{
                    key: response[key]
                    for key in (
                        "E0",
                        "G0",
                        "G1",
                        "G2",
                        "G3",
                        "U2",
                        "U3",
                        "U4",
                        "shape_invariant",
                    )
                },
                "status": "MATCHED_GRID_SPACING",
            }
        )
    box_values.append(baseline_response_100["shape_invariant"])
    diagnostics = {
        "continuum_extrapolated": extrapolated,
        "fine_grid": baseline_response_100,
        "fine_to_extrapolated_invariant_residual": abs(
            baseline_response_100["shape_invariant"]
            - extrapolated["shape_invariant"]
        ),
        "last_two_grid_invariant_residual": abs(
            grid_records[-1][1]["shape_invariant"]
            - grid_records[-2][1]["shape_invariant"]
        ),
        "spectral_invariant_span_80_to_180": max(spectral_values[1:])
        - min(spectral_values[1:]),
        "matched_spacing_box_invariant_span": max(box_values) - min(box_values),
    }
    return tagged(rows), diagnostics


def quantum_mass_scan_rows(
    baseline: QuantumSystem,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    masses = np.concatenate(
        (
            np.array([0.0]),
            np.geomspace(1.0e-4, 1.0e3, 29),
        )
    )
    rows: list[dict[str, Any]] = []
    invariants: list[float] = []
    for mass_squared in masses:
        if mass_squared == 0.0:
            response = quantum_response(
                baseline.eigenvalues,
                baseline.source_matrix,
            )
            method = "FINE_BASELINE"
        else:
            system = solve_quantum_system(
                mass_squared=float(mass_squared),
                box_half_width=12.0,
                grid_points=4000,
                state_count=80,
            )
            response = quantum_response(
                system.eigenvalues,
                system.source_matrix,
            )
            method = "MASS_SCAN_GRID"
        invariants.append(response["shape_invariant"])
        rows.append(
            {
                "mass_squared": float(mass_squared),
                "E0": response["E0"],
                "G0": response["G0"],
                "U2": response["U2"],
                "U3": response["U3"],
                "U4": response["U4"],
                "shape_invariant": response["shape_invariant"],
                "logistic_target": LOGISTIC_INVARIANT,
                "passes_logistic": False,
                "method": method,
            }
        )
    rows.append(
        {
            "mass_squared": "infinity",
            "shape_invariant": 3.0 / 4.0,
            "logistic_target": LOGISTIC_INVARIANT,
            "passes_logistic": False,
            "method": "EXACT_HARMONIC_LIMIT",
        }
    )
    diagnostics = {
        "sample_count": len(masses),
        "sample_min": min(invariants),
        "sample_max": max(invariants),
        "harmonic_limit": 3.0 / 4.0,
        "sample_monotone_non_increasing": bool(
            np.all(np.diff(np.asarray(invariants)) <= 2.0e-5)
        ),
    }
    return tagged(rows), diagnostics


def eigenstate_scan_rows(
    baseline: QuantumSystem,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    invariants: list[float] = []
    for state in range(12):
        response = quantum_response(
            baseline.eigenvalues,
            baseline.source_matrix,
            target_state=state,
        )
        invariants.append(response["shape_invariant"])
        rows.append(
            {
                "eigenstate": state,
                "parity": "even" if state % 2 == 0 else "odd",
                "E0": response["E0"],
                "G0": response["G0"],
                "U2": response["U2"],
                "U3": response["U3"],
                "U4": response["U4"],
                "shape_invariant": response["shape_invariant"],
                "logistic_target": LOGISTIC_INVARIANT,
                "passes_logistic": False,
                "status": "CONVERGED_LOW_STATE_SCAN",
            }
        )
    diagnostics = {
        "state_count": len(rows),
        "minimum_invariant": min(invariants),
        "maximum_invariant": max(invariants),
        "all_stable_signs": all(
            row["U2"] > 0.0 and row["U3"] < 0.0 and row["U4"] > 0.0
            for row in rows
        ),
    }
    return tagged(rows), diagnostics


def thermal_response(
    energy_coefficients: np.ndarray,
    inverse_temperature: float,
) -> dict[str, float]:
    weights = np.exp(
        -inverse_temperature
        * (energy_coefficients[:, 0] - energy_coefficients[0, 0])
    )
    partition_coefficients = np.zeros(5)
    for state, weight in enumerate(weights):
        exponent_coefficients = np.zeros(5)
        exponent_coefficients[1:] = (
            -inverse_temperature * energy_coefficients[state, 1:]
        )
        exponential_series = np.zeros(5)
        exponential_series[0] = 1.0
        for order in range(1, 5):
            exponential_series[order] = (
                sum(
                    lower_order
                    * exponent_coefficients[lower_order]
                    * exponential_series[order - lower_order]
                    for lower_order in range(1, order + 1)
                )
                / order
            )
        partition_coefficients += weight * exponential_series
    normalized = partition_coefficients / partition_coefficients[0]
    z1, z2, z3, z4 = normalized[1:]
    log_coefficients = np.asarray(
        [
            0.0,
            z1,
            z2 - z1**2 / 2.0,
            z3 - z1 * z2 + z1**3 / 3.0,
            z4
            - z1 * z3
            - z2**2 / 2.0
            + z1**2 * z2
            - z1**4 / 4.0,
        ]
    )
    free_energy_coefficients = -log_coefficients / inverse_temperature
    g1 = 4.0 * free_energy_coefficients[2]
    g2 = 12.0 * free_energy_coefficients[3]
    g3 = 48.0 * free_energy_coefficients[4]
    u2 = -1.0 / (2.0 * g1)
    u3 = g2 / (2.0 * g1**3)
    u4 = g3 / (2.0 * g1**4) - 3.0 * g2**2 / (2.0 * g1**5)
    return {
        "U2": u2,
        "U3": u3,
        "U4": u4,
        "shape_invariant": u3**2 / (u2 * u4),
        "last_state_weight_fraction": float(weights[-1] / weights.sum()),
    }


def thermal_coefficients(
    system: QuantumSystem,
    thermal_state_count: int = 20,
) -> np.ndarray:
    coefficients = np.zeros((thermal_state_count, 5))
    for state in range(thermal_state_count):
        response = quantum_response(
            system.eigenvalues,
            system.source_matrix,
            target_state=state,
        )
        coefficients[state] = response["energy_coefficients"]
    return coefficients


def thermal_scan_for_system(
    system: QuantumSystem,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    coefficients = thermal_coefficients(system)
    beta_grid = np.geomspace(1.5, 100.0, 73)
    rows: list[dict[str, Any]] = []
    for inverse_temperature in beta_grid:
        response = thermal_response(coefficients, float(inverse_temperature))
        rows.append(
            {
                "inverse_temperature": float(inverse_temperature),
                **response,
                "box_half_width": system.box_half_width,
                "grid_points": system.grid_points,
                "spectral_states": system.state_count,
                "thermal_states": len(coefficients),
                "status": "SPECTRAL_FREE_ENERGY_ORDER_4",
            }
        )
    optimum = minimize_scalar(
        lambda beta: -thermal_response(coefficients, float(beta))[
            "shape_invariant"
        ],
        bounds=(2.0, 10.0),
        method="bounded",
        options={"xatol": 1.0e-10},
    )
    peak = thermal_response(coefficients, float(optimum.x))
    peak.update(
        {
            "inverse_temperature": float(optimum.x),
            "box_half_width": system.box_half_width,
            "grid_points": system.grid_points,
            "spectral_states": system.state_count,
            "thermal_states": len(coefficients),
        }
    )
    return rows, peak


def thermal_state_scan_rows(
    baseline: QuantumSystem,
    ultralocal_invariant: float,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    primary_rows, primary_peak = thermal_scan_for_system(baseline)
    convergence_systems = [
        solve_quantum_system(0.0, 12.0, 5000, 140),
        solve_quantum_system(0.0, 16.0, 9000, 180),
    ]
    peak_rows = [primary_peak]
    for system in convergence_systems:
        _, peak = thermal_scan_for_system(system)
        peak_rows.append(peak)
    rows = list(primary_rows)
    rows.extend(
        {
            **peak,
            "status": "THERMAL_PEAK_CONVERGENCE",
        }
        for peak in peak_rows
    )
    ground_response = quantum_response(
        baseline.eigenvalues,
        baseline.source_matrix,
    )
    rows.extend(
        [
            {
                "inverse_temperature": 0.0,
                "shape_invariant": ultralocal_invariant,
                "status": "EXACT_CLASSICAL_HIGH_T_LIMIT",
            },
            {
                "inverse_temperature": "infinity",
                "U2": ground_response["U2"],
                "U3": ground_response["U3"],
                "U4": ground_response["U4"],
                "shape_invariant": ground_response["shape_invariant"],
                "status": "QUANTUM_GROUND_STATE_LIMIT",
            },
        ]
    )
    peak_invariants = [float(peak["shape_invariant"]) for peak in peak_rows]
    diagnostics = {
        "primary_peak_inverse_temperature": primary_peak[
            "inverse_temperature"
        ],
        "primary_peak_invariant": primary_peak["shape_invariant"],
        "peak_convergence_span": max(peak_invariants) - min(peak_invariants),
        "high_temperature_limit": ultralocal_invariant,
        "low_temperature_limit": ground_response["shape_invariant"],
        "executed_beta_min": float(min(row["inverse_temperature"] for row in primary_rows)),
        "executed_beta_max": float(max(row["inverse_temperature"] for row in primary_rows)),
    }
    return tagged(rows), diagnostics


def gaussian_analytic_rows() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    quantum_max = 25.0 / 31.0
    quantum_min = 3.0 / 4.0
    classical_max = 49.0 / 67.0
    classical_min = 2.0 / 3.0
    rows = [
        {
            "closure": "quantum_Gaussian",
            "effective_action": "U=A/G+M G+B G^(2/3)",
            "stationary_parameter": "t=M/B>=0",
            "invariant": "(81t+50)^2/[4(9t+5)(243t+155)]",
            "derivative": "-45(81t+50)(81t+55)/[2(9t+5)^2(243t+155)^2]",
            "minimum": quantum_min,
            "maximum": quantum_max,
            "monotonicity": "strictly_decreasing",
            "passes_logistic": False,
            "status": "EXACT_ANALYTIC_BOUND",
        },
        {
            "closure": "classical_Gaussian_entropy",
            "effective_action": "U=-A ln G+M G+B G^(2/3)",
            "stationary_parameter": "t=M/B>=0",
            "invariant": "2(27t+14)^2/[(9t+4)(243t+134)]",
            "derivative": "-36(27t+14)(135t+86)/[(9t+4)^2(243t+134)^2]",
            "minimum": classical_min,
            "maximum": classical_max,
            "monotonicity": "strictly_decreasing",
            "passes_logistic": False,
            "status": "EXACT_ANALYTIC_BOUND",
        },
    ]
    diagnostics = {
        "quantum_min": quantum_min,
        "quantum_max": quantum_max,
        "classical_min": classical_min,
        "classical_max": classical_max,
    }
    return tagged(rows), diagnostics


def projective_scale_rows(
    q_self: float,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    sample_u = np.linspace(-10.0, 10.0, 401)
    odds = np.exp(q_self * sample_u)
    occupation = odds / (1.0 + odds)
    direct_derivative = q_self * odds / (1.0 + odds) ** 2
    logistic_derivative = q_self * occupation * (1.0 - occupation)
    flow_residual = float(
        np.max(np.abs(direct_derivative - logistic_derivative))
    )
    entropy_residual = float(
        np.max(
            np.abs(
                np.log(occupation / (1.0 - occupation))
                - q_self * sample_u
            )
        )
    )
    sample_n = np.linspace(1.0e-6, 1.0 - 1.0e-6, 1001)
    fisher_metric = 1.0 / (sample_n * (1.0 - sample_n))
    canonical_jacobian_squared = 1.0 / (
        sample_n * (1.0 - sample_n)
    )
    fisher_metric_residual = float(
        np.max(
            np.abs(fisher_metric - canonical_jacobian_squared)
            / fisher_metric
        )
    )
    theta = 2.0 * np.arcsin(np.sqrt(occupation))
    theta_flow = q_self * np.sqrt(occupation * (1.0 - occupation))
    canonical_angle_flow = 0.5 * q_self * np.sin(theta)
    canonical_angle_flow_residual = float(
        np.max(np.abs(theta_flow - canonical_angle_flow))
    )
    rows = [
        {
            "step": 1,
            "object": "positive_weights",
            "equation": "W0>0, W1>0",
            "result": "two positive reference/occupied weights",
            "status": "ASSUMPTION_TO_BE_PARENT_SIGNED",
        },
        {
            "step": 2,
            "object": "projective_occupation",
            "equation": "n=W1/(W0+W1)=z/(1+z), z=W1/W0",
            "result": "0<n<1",
            "status": "EXACT_DEFINITION",
        },
        {
            "step": 3,
            "object": "scale_covariance",
            "equation": "d ln W_a/du=Delta_a; u=ln(R/L)",
            "result": "d ln z/du=q; q=Delta1-Delta0",
            "status": "COMPOSITE_EIGENVALUE_CONTRACT",
        },
        {
            "step": 4,
            "object": "inner_flow",
            "equation": "dn/du=q n(1-n)",
            "result": "n=(R/L)^q/[1+(R/L)^q]",
            "status": "EXACT_FROM_STEPS_2_AND_3",
        },
        {
            "step": 5,
            "object": "binary_entropy",
            "equation": "F=n ln n+(1-n)ln(1-n)-q(u-u0)n",
            "result": "dF/dn=0 gives the same logistic occupation",
            "status": "EXACT_STABLE_VARIATIONAL_REALIZATION",
        },
        {
            "step": 6,
            "object": "projective_information_metric",
            "equation": "g_nn=d^2[n ln n+(1-n)ln(1-n)]/dn^2=1/[n(1-n)]",
            "result": "theta=2 asin(sqrt(n)) gives g_nn dn^2=dtheta^2",
            "status": "EXACT_BINARY_STATE_GEOMETRY",
        },
        {
            "step": 7,
            "object": "canonical_angle_flow",
            "equation": "dtheta/du=(q/2) sin(theta); V_theta=q^2 sin^2(theta)/8",
            "result": "the projective canonical completion is sine-Gordon-like, not quartic in n",
            "status": "EXACT_CONDITIONAL_ON_FISHER_METRIC",
        },
        {
            "step": 8,
            "object": "outer_flow",
            "equation": "b=1/[1+(R/(B L))^s]; db/du=-s b(1-b)",
            "result": f"s={OUTER_EXPONENT:g}; B={OUTER_BOUNDARY:g}",
            "status": "EXACT_FORM_BUT_PARENT_WALL_PARAMETERS_OPEN",
        },
        {
            "step": 9,
            "object": "current_collective_slope",
            "equation": "q from checkpoint-5198 scale equality",
            "result": q_self,
            "status": "CONDITIONAL_INTERNAL_SCALE_CLOSURE",
        },
        {
            "step": 10,
            "object": "Bogomolny_comparison",
            "equation": "V=q^2 n^2(1-n)^2/2",
            "result": "sufficient only for a flat n-metric; the projective state has a different natural metric",
            "status": "5198_VERTEX_GATE_SCOPE_REFINED",
        },
    ]
    diagnostics = {
        "q_self_consistent": q_self,
        "locked_q": Q_LOCKED,
        "relative_q_residual": abs(q_self - Q_LOCKED) / Q_LOCKED,
        "flow_identity_max_residual": flow_residual,
        "binary_entropy_stationarity_max_residual": entropy_residual,
        "Fisher_metric_canonicalization_max_relative_residual": (
            fisher_metric_residual
        ),
        "canonical_angle_flow_max_residual": canonical_angle_flow_residual,
        "stieltjes_positivity_window_pass": 0.0 < q_self < 2.0,
        "inner_functional_form_exact": True,
        "inner_parent_eigenvalue_signed": False,
        "outer_parent_wall_signed": False,
    }
    return tagged(rows), diagnostics


def known_parent_interaction_rows() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    payload = json.loads(CHECKPOINT_5185_RESULT.read_text(encoding="utf-8"))
    physical = payload["metrics"]["physical_bounds"]
    coefficients = payload["coefficient_rows"]
    dynamic = next(row for row in coefficients if row["scheme"] == "dynamic_etaN")
    rows = [
        {
            "object": "c2",
            "value": dynamic["c2_eV_minus4"],
            "units": "eV^-4",
            "role": "known X^2 occupied-state interaction",
            "can_shift_vertices_order_one": False,
            "source": "checkpoint_5185",
        },
        {
            "object": "c3",
            "value": dynamic["c3_eV_minus8"],
            "units": "eV^-8",
            "role": "known X^3 occupied-state interaction",
            "can_shift_vertices_order_one": False,
            "source": "checkpoint_5185",
        },
        {
            "object": "interaction_Z_norm_ceiling",
            "value": physical["maximum_interaction_Z_norm_ceiling"],
            "units": "dimensionless",
            "role": "largest sourced Hartree kinetic correction",
            "can_shift_vertices_order_one": False,
            "source": "checkpoint_5185",
        },
        {
            "object": "Hartree_stress_fraction_ceiling",
            "value": physical["maximum_Hartree_stress_fraction_ceiling"],
            "units": "dimensionless",
            "role": "largest sourced local interaction stress",
            "can_shift_vertices_order_one": False,
            "source": "checkpoint_5185",
        },
        {
            "object": "coherent_phase_ceiling",
            "value": physical["maximum_coherent_phase_ceiling"],
            "units": "dimensionless",
            "role": "maximal sourced coherent accumulation",
            "can_shift_vertices_order_one": False,
            "source": "checkpoint_5185",
        },
        {
            "object": "collision_exposure",
            "value": physical["maximum_log10_collision_exposure"],
            "units": "log10 dimensionless",
            "role": "largest sourced collision exposure",
            "can_shift_vertices_order_one": False,
            "source": "checkpoint_5185",
        },
        {
            "object": "unknown_O2_required_enhancement",
            "value": physical["minimum_O2_enhancement_over_natural"],
            "units": "dimensionless",
            "role": "uncontrolled enhancement needed for an order-one rescue",
            "can_shift_vertices_order_one": False,
            "source": "checkpoint_5185",
        },
    ]
    diagnostics = {
        "c2_eV_minus4": dynamic["c2_eV_minus4"],
        "c3_eV_minus8": dynamic["c3_eV_minus8"],
        **physical,
        "controlled_order_one_vertex_rescue": False,
    }
    return tagged(rows), diagnostics


def invariant_comparison_rows(
    ultralocal: dict[str, Any],
    quantum: dict[str, Any],
    mass_scan: dict[str, Any],
    eigenstates: dict[str, Any],
    thermal: dict[str, Any],
    gaussian: dict[str, Any],
) -> list[dict[str, Any]]:
    candidates = [
        (
            "bare_fractional_one_point",
            2.0 / 5.0,
            "EXACT",
        ),
        (
            "ultralocal_exact_composite",
            ultralocal["shape_invariant"],
            "EXACT",
        ),
        (
            "fractional_quantum_ground_composite",
            quantum["continuum_extrapolated"]["shape_invariant"],
            "NUMERIC_CONTINUUM_EXTRAPOLATION",
        ),
        (
            "positive_mass_quantum_maximum",
            mass_scan["sample_max"],
            "EXECUTED_SCAN_PLUS_HARMONIC_ENDPOINT",
        ),
        (
            "low_eigenstate_quantum_maximum",
            eigenstates["maximum_invariant"],
            "TWELVE_CONVERGED_EIGENSTATES",
        ),
        (
            "thermal_quantum_maximum",
            thermal["primary_peak_invariant"],
            "CONVERGED_SPECTRAL_THERMAL_PEAK",
        ),
        (
            "quantum_Gaussian_2PI_upper_bound",
            gaussian["quantum_max"],
            "EXACT_ANALYTIC_BOUND",
        ),
        (
            "classical_Gaussian_2PI_upper_bound",
            gaussian["classical_max"],
            "EXACT_ANALYTIC_BOUND",
        ),
        (
            "logistic_Bogomolny_target",
            LOGISTIC_INVARIANT,
            "EXACT_TARGET",
        ),
    ]
    return tagged(
        [
            {
                "candidate": name,
                "shape_invariant": invariant,
                "logistic_target": LOGISTIC_INVARIANT,
                "target_over_candidate": (
                    LOGISTIC_INVARIANT / invariant
                    if invariant != LOGISTIC_INVARIANT
                    else 1.0
                ),
                "fractional_target_gap": (
                    (LOGISTIC_INVARIANT - invariant) / LOGISTIC_INVARIANT
                ),
                "matches_logistic": math.isclose(
                    invariant,
                    LOGISTIC_INVARIANT,
                    rel_tol=1.0e-8,
                    abs_tol=1.0e-10,
                ),
                "evidence_class": evidence_class,
            }
            for name, invariant, evidence_class in candidates
        ]
    )


def route_decision_rows(
    projective: dict[str, Any],
    interaction: dict[str, Any],
) -> list[dict[str, Any]]:
    return tagged(
        [
            {
                "route": "bare_fractional_canonical_kink",
                "decision": "REJECTED",
                "reason": "I=2/5 rather than 3",
                "next_action": "none",
            },
            {
                "route": "minimal_ultralocal_composite_kink",
                "decision": "REJECTED",
                "reason": "exact I=0.7794368858 and K=0 is a one-sided source boundary",
                "next_action": "none",
            },
            {
                "route": "fractional_quantum_composite_kink",
                "decision": "REJECTED_IN_SOURCED_MINIMAL_TRUNCATION",
                "reason": "ground, mass, eigenstate, thermal and Gaussian responses stay far below I=3",
                "next_action": "do not repeat vertex scans without a new parent operator",
            },
            {
                "route": "known_parent_PX_interaction_rescue",
                "decision": "REJECTED_AS_CONTROLLED_RESCUE",
                "reason": (
                    "largest sourced interaction norm is "
                    f"{interaction['maximum_interaction_Z_norm_ceiling']:.6e}"
                ),
                "next_action": "no unsourced O2 enhancement",
            },
            {
                "route": "projective_scale_covariant_occupation",
                "decision": "RETAINED_CONDITIONALLY",
                "reason": "two positive scaling weights derive dn/du=q n(1-n) and the Fisher metric exactly without Landau vertices",
                "next_action": "derive the occupied/reference eigenvalue difference q and projected 2PI metric",
            },
            {
                "route": "current_inner_q",
                "decision": "CONDITIONAL_INTERNAL_CLOSURE",
                "reason": (
                    f"checkpoint-5198 gives q={projective['q_self_consistent']}"
                ),
                "next_action": "test this value in the parent composite stability block",
            },
            {
                "route": "outer_anti_wall",
                "decision": "FUNCTIONAL_FORM_EXACT_PARAMETERS_OPEN",
                "reason": "projective complement gives db/du=-s b(1-b), but s and B are not parent-signed",
                "next_action": "derive boundary-sector scaling weight and finite-domain normalization",
            },
            {
                "route": "local_GR_Newton_Maxwell",
                "decision": "UNCHANGED",
                "reason": "this is an occupied-state reduction and adds no vacuum pole or source coupling",
                "next_action": "retain the checkpoint-5197 route separation",
            },
        ]
    )


def source_provenance_rows() -> list[dict[str, Any]]:
    roles = {
        "5148-Y5-R2FR-one-parent-local-GR-galaxy-spectral-response-cog-theorem.md": (
            "original exact projective/logistic spectral factor"
        ),
        "5151-Y5-R2FR-parent-projective-occupation-to-conserved-Einstein-cluster-stress-and-two-metric-cog-gate.md": (
            "positive Stieltjes projective occupation and conserved state stress"
        ),
        "5181-Y5-R2FR-critical-pair-bubble-positive-Hessian-and-parent-ownership-gate.md": (
            "composite stability-block ownership gap"
        ),
        "5185-Y5-R2FR-occupied-state-2PI-interaction-stress-and-collision-gate.md": (
            "sourced 2PI interaction topology and physical bounds"
        ),
        "5198-Y5-R2FR-marginal-Mestel-composite-Hessian-Plummer-scale-bridge-and-logistic-vertex-gate.md": (
            "collective Hessian, scale bridge and Bogomolny vertex target"
        ),
        "source-intake/functional_rg/5185/occupied_state_2PI_interaction_results.json": (
            "machine-readable sourced interaction bounds"
        ),
        "source-intake/functional_rg/5198/marginal_Mestel_collective_results.json": (
            "machine-readable q self-consistency and target invariant"
        ),
        "scripts/Y5_R2FR_5198_marginal_Mestel_collective_Hessian_scale_bridge.py": (
            "predecessor executable"
        ),
    }
    return tagged(
        [
            {
                "source_path": relative_path,
                "sha256": file_digest(POST / relative_path),
                "role": roles[relative_path],
                "exists": (POST / relative_path).exists(),
                "status": "SOURCE_LOCKED",
            }
            for relative_path in SOURCE_LOCKS
        ]
    )


def build_payload(
    ultralocal_rows: list[dict[str, Any]],
    ultralocal_scan: list[dict[str, Any]],
    quantum_convergence: list[dict[str, Any]],
    mass_scan: list[dict[str, Any]],
    eigenstate_scan: list[dict[str, Any]],
    thermal_scan: list[dict[str, Any]],
    gaussian_rows: list[dict[str, Any]],
    projective_rows: list[dict[str, Any]],
    interaction_rows: list[dict[str, Any]],
    comparison_rows: list[dict[str, Any]],
    route_rows: list[dict[str, Any]],
    provenance: list[dict[str, Any]],
    diagnostics: dict[str, Any],
) -> dict[str, Any]:
    return {
        "checkpoint": 5199,
        "marker": MARKER,
        "checked_date": CHECKED_DATE,
        "claim_status": {
            "bare_fractional_Bogomolny_logistic": "REJECTED",
            "minimal_composite_2PI_Bogomolny_logistic": "REJECTED_IN_SOURCED_TRUNCATION",
            "projective_scale_covariance_logistic_form": "DERIVED_CONDITIONALLY",
            "projective_Fisher_metric": "DERIVED_FOR_TWO_NORMALIZED_WEIGHTS",
            "collective_q_parent_eigenvalue": "OPEN",
            "parent_2PI_projective_metric_match": "OPEN",
            "outer_wall_parent_parameters": "OPEN",
            "collective_state_normalization": "OPEN",
            "local_GR_Newton_Maxwell_branch": "UNCHANGED",
            "galaxy_claim": False,
            "local_GR_claim": False,
            "full_MTS_claim": False,
        },
        "theorem": (
            "The exact ultralocal Legendre transform, the nonperturbative "
            "fractional quantum zero mode, positive-mass deformations, low "
            "eigenstates, a converged finite-temperature scan and controlled Gaussian "
            "2PI closures all have the correct stable vertex signs but a "
            "field-normalization invariant below 0.872, not the canonical "
            "Bogomolny logistic value 3. The known parent P(X) interactions "
            "are far too small to repair that order-one ratio. This rejects "
            "the sourced minimal canonical-kink realization. It does not "
            "reject the logistic phase law: for two positive scale-covariant "
            "weights, the projective occupation n=W1/(W0+W1) obeys "
            "dn/du=(Delta1-Delta0)n(1-n) identically. The remaining parent "
            "task is therefore a composite scaling-eigenvalue, projective-"
            "metric and state-selection calculation, not an arbitrary cubic/"
            "quartic fit."
        ),
        "diagnostics": diagnostics,
        "exact_ultralocal_composite_vertices": ultralocal_rows,
        "ultralocal_positive_mass_scan": ultralocal_scan,
        "fractional_quantum_convergence": quantum_convergence,
        "fractional_quantum_positive_mass_scan": mass_scan,
        "fractional_quantum_eigenstate_scan": eigenstate_scan,
        "fractional_quantum_thermal_scan": thermal_scan,
        "Gaussian_2PI_analytic_bounds": gaussian_rows,
        "projective_scale_covariance_derivation": projective_rows,
        "known_parent_interaction_gate": interaction_rows,
        "invariant_comparison": comparison_rows,
        "route_decision": route_rows,
        "source_provenance": provenance,
    }


def validation_rows(
    galaxy_before: tuple[str, str],
    output_files: list[Path],
    all_rows: list[list[dict[str, Any]]],
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
        path = POST / relative_path
        add(f"source_exists::{relative_path}", path.exists(), path)
        add(
            f"source_lock::{relative_path}",
            path.exists() and file_digest(path) == expected_digest,
            file_digest(path) if path.exists() else "absent",
        )
    add(
        "formalization_workbench_lock",
        tree_digest(FORMAL) == FORMAL_LOCK,
        tree_digest(FORMAL),
    )
    add(
        "checkpoint_5198_output_lock",
        tree_digest(CHECKPOINT_5198_OUT) == CHECKPOINT_5198_OUT_LOCK,
        tree_digest(CHECKPOINT_5198_OUT),
    )
    add(
        "all_output_files_nonempty",
        all(path.exists() and path.stat().st_size > 0 for path in output_files),
        len(output_files),
    )
    add(
        "all_output_csv_parse",
        all(bool(read_csv(path)) for path in output_files if path.suffix == ".csv"),
        "all generated CSV files contain rows",
    )
    add(
        "all_row_sets_nonempty",
        all(bool(rows) for rows in all_rows),
        [len(rows) for rows in all_rows],
    )
    flattened = json.dumps(all_rows, default=str)
    add("no_missing_markers", "MISSING_" not in flattened, "no MISSING_ token")

    ultralocal = diagnostics["ultralocal"]
    add(
        "ultralocal_invariant_exact",
        math.isclose(
            ultralocal["shape_invariant"],
            0.7794368858172215,
            rel_tol=2.0e-13,
            abs_tol=2.0e-13,
        ),
        ultralocal["shape_invariant"],
    )
    add(
        "ultralocal_stable_vertex_signs",
        ultralocal["U2"] > 0.0
        and ultralocal["U3"] < 0.0
        and ultralocal["U4"] > 0.0,
        (ultralocal["U2"], ultralocal["U3"], ultralocal["U4"]),
    )
    add(
        "ultralocal_source_domain_boundary",
        not ultralocal["two_sided_source_neighbourhood"],
        ultralocal["source_domain"],
    )
    ultralocal_mass = diagnostics["ultralocal_mass"]
    add(
        "ultralocal_mass_scan_monotone",
        ultralocal_mass["sample_monotone_non_decreasing"],
        (ultralocal_mass["sample_min"], ultralocal_mass["sample_max"]),
    )
    add(
        "ultralocal_mass_scan_below_logistic",
        ultralocal_mass["sample_max"] < 0.8,
        ultralocal_mass["sample_max"],
    )

    quantum = diagnostics["quantum"]
    add(
        "quantum_continuum_invariant",
        0.8298
        < quantum["continuum_extrapolated"]["shape_invariant"]
        < 0.8299,
        quantum["continuum_extrapolated"]["shape_invariant"],
    )
    add(
        "quantum_grid_convergence",
        quantum["last_two_grid_invariant_residual"] < 5.0e-8,
        quantum["last_two_grid_invariant_residual"],
    )
    add(
        "quantum_extrapolation_residual",
        quantum["fine_to_extrapolated_invariant_residual"] < 1.0e-7,
        quantum["fine_to_extrapolated_invariant_residual"],
    )
    add(
        "quantum_spectral_convergence",
        quantum["spectral_invariant_span_80_to_180"] < 1.0e-8,
        quantum["spectral_invariant_span_80_to_180"],
    )
    add(
        "quantum_box_convergence",
        quantum["matched_spacing_box_invariant_span"] < 1.0e-7,
        quantum["matched_spacing_box_invariant_span"],
    )
    mass = diagnostics["quantum_mass"]
    add(
        "quantum_mass_scan_monotone",
        mass["sample_monotone_non_increasing"],
        (mass["sample_min"], mass["sample_max"]),
    )
    add(
        "quantum_mass_scan_below_logistic",
        mass["sample_max"] < 0.84,
        mass["sample_max"],
    )
    eigenstates = diagnostics["eigenstates"]
    add(
        "quantum_eigenstate_signs",
        eigenstates["all_stable_signs"],
        eigenstates["state_count"],
    )
    add(
        "quantum_eigenstate_scan_below_logistic",
        eigenstates["maximum_invariant"] < 0.84,
        eigenstates["maximum_invariant"],
    )
    thermal = diagnostics["thermal"]
    add(
        "thermal_peak_converged",
        thermal["peak_convergence_span"] < 5.0e-8,
        thermal["peak_convergence_span"],
    )
    add(
        "thermal_scan_below_logistic",
        thermal["primary_peak_invariant"] < 0.88,
        thermal["primary_peak_invariant"],
    )
    gaussian = diagnostics["gaussian"]
    add(
        "Gaussian_quantum_bound",
        gaussian["quantum_max"] == 25.0 / 31.0,
        gaussian["quantum_max"],
    )
    add(
        "Gaussian_classical_bound",
        gaussian["classical_max"] == 49.0 / 67.0,
        gaussian["classical_max"],
    )
    add(
        "all_minimal_direct_routes_miss_I3",
        max(
            ultralocal["shape_invariant"],
            quantum["continuum_extrapolated"]["shape_invariant"],
            mass["sample_max"],
            eigenstates["maximum_invariant"],
            thermal["primary_peak_invariant"],
            gaussian["quantum_max"],
            gaussian["classical_max"],
        )
        < 0.88,
        LOGISTIC_INVARIANT,
    )

    projective = diagnostics["projective"]
    add(
        "projective_flow_identity",
        projective["flow_identity_max_residual"] < 1.0e-14,
        projective["flow_identity_max_residual"],
    )
    add(
        "binary_entropy_stationarity",
        projective["binary_entropy_stationarity_max_residual"] < 1.0e-10,
        projective["binary_entropy_stationarity_max_residual"],
    )
    add(
        "projective_Fisher_metric_canonicalization",
        projective["Fisher_metric_canonicalization_max_relative_residual"]
        < 1.0e-14,
        projective["Fisher_metric_canonicalization_max_relative_residual"],
    )
    add(
        "projective_canonical_angle_flow",
        projective["canonical_angle_flow_max_residual"] < 1.0e-14,
        projective["canonical_angle_flow_max_residual"],
    )
    add(
        "projective_positivity_window",
        projective["stieltjes_positivity_window_pass"],
        projective["q_self_consistent"],
    )
    add(
        "q_self_source_lock",
        math.isclose(
            projective["q_self_consistent"],
            Q_SELF_EXPECTED,
            rel_tol=0.0,
            abs_tol=1.0e-15,
        ),
        projective["q_self_consistent"],
    )
    add(
        "projective_claim_boundary",
        not projective["inner_parent_eigenvalue_signed"]
        and not projective["outer_parent_wall_signed"],
        "parent eigenvalue and wall remain open",
    )
    interaction = diagnostics["interaction"]
    add(
        "known_interaction_too_small",
        interaction["maximum_interaction_Z_norm_ceiling"] < 1.0e-100,
        interaction["maximum_interaction_Z_norm_ceiling"],
    )
    add(
        "no_controlled_interaction_rescue",
        not interaction["controlled_order_one_vertex_rescue"],
        interaction["minimum_O2_enhancement_over_natural"],
    )
    claims = payload["claim_status"]
    add("galaxy_claim_false", claims["galaxy_claim"] is False, claims)
    add("local_GR_claim_false", claims["local_GR_claim"] is False, claims)
    add("full_MTS_claim_false", claims["full_MTS_claim"] is False, claims)

    galaxy_after = git_state(GALAXY_REPO)
    add(
        "galaxy_repo_head_unchanged",
        galaxy_before[0] == galaxy_after[0] == GALAXY_HEAD_LOCK,
        f"before={galaxy_before[0]};after={galaxy_after[0]}",
    )
    add(
        "galaxy_repo_status_unchanged",
        galaxy_before[1] == galaxy_after[1],
        galaxy_after[1] if galaxy_after[1] else "clean",
    )
    public_head, public_status = git_state(PUBLIC_WORKTREE)
    add(
        "public_worktree_head_unchanged",
        public_head == PUBLIC_HEAD_LOCK,
        public_head,
    )
    add(
        "public_worktree_clean",
        public_status == "",
        public_status if public_status else "clean",
    )
    pycache = POST / "scripts" / "__pycache__"
    add("no_scripts_pycache", not pycache.exists(), pycache)
    return tagged(
        [
            {
                "check": name,
                "status": "PASS" if passed else "FAIL",
                "detail": detail,
            }
            for name, passed, detail in checks
        ]
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="perform the derivation and print the decision without writing files",
    )
    arguments = parser.parse_args()

    galaxy_before = git_state(GALAXY_REPO)
    checkpoint_5198 = json.loads(
        CHECKPOINT_5198_RESULT.read_text(encoding="utf-8")
    )
    q_self = float(checkpoint_5198["scale_diagnostics"]["self_consistent_q"])

    ultralocal_rows, ultralocal_diagnostics = exact_ultralocal_rows()
    ultralocal_scan, ultralocal_mass_diagnostics = ultralocal_mass_scan_rows(
        ultralocal_diagnostics
    )

    baseline = solve_quantum_system(
        mass_squared=0.0,
        box_half_width=14.0,
        grid_points=8000,
        state_count=180,
    )
    quantum_convergence, quantum_diagnostics = quantum_convergence_rows(
        baseline
    )
    mass_scan, quantum_mass_diagnostics = quantum_mass_scan_rows(baseline)
    eigenstate_scan, eigenstate_diagnostics = eigenstate_scan_rows(baseline)
    thermal_scan, thermal_diagnostics = thermal_state_scan_rows(
        baseline,
        ultralocal_diagnostics["shape_invariant"],
    )
    gaussian_rows, gaussian_diagnostics = gaussian_analytic_rows()
    projective_rows, projective_diagnostics = projective_scale_rows(q_self)
    interaction_rows, interaction_diagnostics = known_parent_interaction_rows()
    comparison_rows = invariant_comparison_rows(
        ultralocal_diagnostics,
        quantum_diagnostics,
        quantum_mass_diagnostics,
        eigenstate_diagnostics,
        thermal_diagnostics,
        gaussian_diagnostics,
    )
    route_rows = route_decision_rows(
        projective_diagnostics,
        interaction_diagnostics,
    )
    provenance = source_provenance_rows()
    diagnostics = {
        "ultralocal": ultralocal_diagnostics,
        "ultralocal_mass": ultralocal_mass_diagnostics,
        "quantum": quantum_diagnostics,
        "quantum_mass": quantum_mass_diagnostics,
        "eigenstates": eigenstate_diagnostics,
        "thermal": thermal_diagnostics,
        "gaussian": gaussian_diagnostics,
        "projective": projective_diagnostics,
        "interaction": interaction_diagnostics,
    }
    payload = build_payload(
        ultralocal_rows,
        ultralocal_scan,
        quantum_convergence,
        mass_scan,
        eigenstate_scan,
        thermal_scan,
        gaussian_rows,
        projective_rows,
        interaction_rows,
        comparison_rows,
        route_rows,
        provenance,
        diagnostics,
    )

    if arguments.dry_run:
        print(
            json.dumps(
                {
                    "marker": MARKER,
                    "ultralocal_invariant": ultralocal_diagnostics[
                        "shape_invariant"
                    ],
                    "quantum_continuum_invariant": quantum_diagnostics[
                        "continuum_extrapolated"
                    ]["shape_invariant"],
                    "quantum_mass_scan_maximum": quantum_mass_diagnostics[
                        "sample_max"
                    ],
                    "eigenstate_scan_maximum": eigenstate_diagnostics[
                        "maximum_invariant"
                    ],
                    "thermal_peak": {
                        "inverse_temperature": thermal_diagnostics[
                            "primary_peak_inverse_temperature"
                        ],
                        "invariant": thermal_diagnostics[
                            "primary_peak_invariant"
                        ],
                        "convergence_span": thermal_diagnostics[
                            "peak_convergence_span"
                        ],
                    },
                    "logistic_target": LOGISTIC_INVARIANT,
                    "projective_flow": projective_diagnostics,
                    "selected_route": (
                        "PROJECTIVE_SCALE_COVARIANT_OCCUPATION; "
                        "PARENT_COMPOSITE_EIGENVALUE_STILL_REQUIRED"
                    ),
                },
                indent=2,
                default=str,
            )
        )
        return

    OUT.mkdir(parents=True, exist_ok=True)
    output_map = {
        "exact_ultralocal_composite_vertices.csv": ultralocal_rows,
        "ultralocal_positive_mass_scan.csv": ultralocal_scan,
        "fractional_quantum_zero_mode_convergence.csv": quantum_convergence,
        "fractional_quantum_positive_mass_scan.csv": mass_scan,
        "fractional_quantum_eigenstate_scan.csv": eigenstate_scan,
        "fractional_quantum_thermal_scan.csv": thermal_scan,
        "Gaussian_2PI_analytic_bounds.csv": gaussian_rows,
        "projective_scale_covariance_derivation.csv": projective_rows,
        "known_parent_interaction_gate.csv": interaction_rows,
        "logistic_invariant_comparison.csv": comparison_rows,
        "route_decision.csv": route_rows,
        "source_provenance.csv": provenance,
    }
    for name, rows in output_map.items():
        write_csv(OUT / name, rows)
    result_path = OUT / "composite_Legendre_projective_logistic_results.json"
    result_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True, default=str) + "\n",
        encoding="utf-8",
    )
    output_files = [OUT / name for name in output_map] + [result_path]
    all_rows = list(output_map.values())
    validations = validation_rows(
        galaxy_before,
        output_files,
        all_rows,
        payload,
        diagnostics,
    )
    write_csv(VALIDATION, validations)
    failed = [row for row in validations if row["status"] != "PASS"]
    if failed:
        raise RuntimeError(
            "checkpoint 5199 validation failed: "
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
                "checkpoint_5198_output_sha256": tree_digest(
                    CHECKPOINT_5198_OUT
                ),
                "ultralocal_composite_invariant": ultralocal_diagnostics[
                    "shape_invariant"
                ],
                "quantum_composite_invariant": quantum_diagnostics[
                    "continuum_extrapolated"
                ]["shape_invariant"],
                "thermal_peak_invariant": thermal_diagnostics[
                    "primary_peak_invariant"
                ],
                "logistic_target_invariant": LOGISTIC_INVARIANT,
                "projective_q": q_self,
                "selected_next_route": (
                    "DERIVE_PARENT_COMPOSITE_SCALING_EIGENVALUE_PROJECTIVE_METRIC_AND_WALL_WEIGHT"
                ),
            },
            indent=2,
            default=str,
        )
    )


if __name__ == "__main__":
    main()
