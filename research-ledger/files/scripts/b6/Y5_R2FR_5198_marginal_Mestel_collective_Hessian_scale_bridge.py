from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import math
import subprocess
import sys
from functools import lru_cache
from pathlib import Path
from types import ModuleType
from typing import Any

import numpy as np
from scipy.integrate import quad
from scipy.interpolate import PchipInterpolator
from scipy.optimize import brentq, minimize_scalar
from scipy.special import gamma


sys.dont_write_bytecode = True

POST = Path(__file__).resolve().parents[1]
FORMAL = POST.parent / "formalization-workbench"
SCRIPT = Path(__file__).resolve()
OUT = POST / "source-intake" / "functional_rg" / "5198"
DOCUMENT = (
    POST
    / "5198-Y5-R2FR-marginal-Mestel-composite-Hessian-Plummer-scale-"
    "bridge-and-logistic-vertex-gate.md"
)
VALIDATION = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5198_VALIDATION.csv"
)
CHECKPOINT_5197_OUT = POST / "source-intake" / "functional_rg" / "5197"
PUBLIC_WORKTREE = Path(
    r"C:\Users\ollet\OneDrive\Documents\Motion-TimeSpace-public-update-2026-07-22"
)
GALAXY_REPO = Path(r"D:\Users\ollet\Desktop\MTS-Galaxy-Lab-repo")
GALAXY_PACKS = Path(r"D:\Users\ollet\Desktop\Galaxy Work\mts-output-packs")

MARKER = "MTS_5198_MARGINAL_MESTEL_COLLECTIVE_HESSIAN_SCALE_BRIDGE"
CHECKED_DATE = "2026-07-24"
FORMAL_LOCK = (
    "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
)
CHECKPOINT_5197_OUT_LOCK = (
    "6c6f76b0fe366fe5b5435d2d6bcfe4b982212bf1606769928cf1559ccb2692e9"
)
PUBLIC_HEAD_LOCK = "8913c00b77d98e457ddb0c48e9aeec9cc5f309fd"
GALAXY_HEAD_LOCK = "f850e4997657f457dddc05cbe50f21186588dcc7"

Q_LOCKED = 0.77
C_Q_LOCKED = 4.640081689829917
BOUNDARY_OVER_L = 8.0
WALL_EXPONENT = 4.0
THICKNESS_OVER_L = 0.02
RADIAL_DISPERSION_COEFFICIENT = 1.0 / 8.0
GAMMA0_EXPECTED = 809.956
G_KPC_EXPECTED = 4.30091e-6
SPECTRAL_INTEGRATION_LIMIT = 400.0
SPECTRAL_SCALE_5148 = 2.921396974200681

POST_SOURCE_LOCKS = {
    "4935-Y5-R2FR-completed-fixed-point-GR-connected-trajectory-and-motion-sector-entry.md": (
        "649da892ba5c256b7670206e837604dbbe04358fcd3705b5871906805e00c1df"
    ),
    "5148-Y5-R2FR-one-parent-local-GR-galaxy-spectral-response-cog-theorem.md": (
        "b2d5bddd8ce3cee2299b2cdadd66a0688bbd07c945bc329ac2ade4c20c113352"
    ),
    "5171-Y5-R2FR-action-angle-retarded-vlasov-polarization-static-response-and-double-counting-gate.md": (
        "e66c543db2154ac061a5930edad50585b5835bbc53e1d2774a0c87d7e19cbade"
    ),
    "5178-Y5-R2FR-exact-2PI-Schur-Ward-Vlasov-subtraction-and-Gaussian-residual-stress-no-go.md": (
        "7bce528f8654373353304bf904316ddc15e2923dda3064bc7e9684e92a468ac9"
    ),
    "5181-Y5-R2FR-critical-pair-bubble-positive-Hessian-and-parent-ownership-gate.md": (
        "54a35ad66744f9e1f5ab6fdd15e66bc6f87a93330a999aae2235ea5cf98b3657"
    ),
    "5187-Y5-R2FR-canonical-local-parent-action-Hessian-source-residue-and-scale-setting-theorem.md": (
        "4556205ec12e11930a13d0ed9b5e27b6b4619f3752a5e10db2a4b767dcdec674"
    ),
    "5197-Y5-R2FR-universal-gap-cross-arena-compatibility-and-route-separation-theorem.md": (
        "f01f94465168758886800556f345e370910f6913e80f1a4a0c646bbe7abe0c0a"
    ),
    "source-intake/functional_rg/5148/regime_selective_motion_response_results.json": (
        "a9f48dd11d6c7f3bdd79436ade9d467c8b870b50c5fb2c5c760abae8dc3f05aa"
    ),
    "scripts/Y5_R2FR_5148_regime_selective_motion_response_cog_theorem.py": (
        "bec2ec345e31446c2812dcf79951452f8f0276fde7f42a0d9601322b9ec5e4a4"
    ),
}

EXTERNAL_SOURCE_LOCKS = {
    GALAXY_REPO / "scripts" / "mts-failure-lab.py": (
        "26edca131ece162c29ad2d263a9c27121b0bf2578b9f10e8641c5c09a517b88b"
    ),
    GALAXY_PACKS
    / "mts-v19-phase-flow-closure-v1"
    / "mts_v19_phase_flow_closure_formula.json": (
        "b12b599d657ee3ab3ce3ea315c1ba9ab3a8caacbd8ab2b68dd60706c823a812f"
    ),
    GALAXY_PACKS
    / "mts-v19-phase-flow-closure-v1"
    / "mts_v19_phase_flow_closure_kernel_profiles.csv": (
        "785131cc5b05636968fe82d6b88e03a1ca028a5d8e8b2738cb11ae8c5f751e54"
    ),
    GALAXY_PACKS
    / "mts-v19-self-similar-phase-disk-v1"
    / "mts_v19_self_similar_phase_disk_formula.json": (
        "33888dcffd4740a4a1e1043363e66cd41dd96807c34e21bd90892f37a3ae27a1"
    ),
    GALAXY_PACKS
    / "mts-v19-self-similar-phase-disk-v1"
    / "mts_v19_self_similar_phase_disk_variant_replay.csv": (
        "ea1446336e0589c26069828985becbbf3f592210ae7c953a2be006efcef99069"
    ),
    GALAXY_PACKS
    / "mts-v19-nonanalytic-phase-pilot-v1"
    / "mts_v19_nonanalytic_phase_formula.json": (
        "e9b3b8ed7344f6b02fb0097f1d771bf17ee4a7853e6d2557d9a46333724c628a"
    ),
    GALAXY_PACKS
    / "mts-v19-nonanalytic-phase-pilot-v1"
    / "mts_v19_nonanalytic_phase_eos_reconstruction.csv": (
        "b7b16733764440e7c9ad743e886181a43dea9acd2857f042b59497eb768a975d"
    ),
}


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
            **row,
            "checkpoint_marker": MARKER,
            "valid_for_local_GR_claim": False,
            "valid_for_galaxy_claim": False,
            "valid_for_full_MTS_claim": False,
            "source_checked_date": CHECKED_DATE,
        }
        for row in rows
    ]


def finite_quantiles(values: list[float] | np.ndarray) -> dict[str, float | int]:
    finite = np.asarray(values, dtype=float)
    finite = finite[np.isfinite(finite)]
    if finite.size == 0:
        return {
            "count": 0,
            "minimum": math.nan,
            "p05": math.nan,
            "p16": math.nan,
            "median": math.nan,
            "p84": math.nan,
            "p95": math.nan,
            "maximum": math.nan,
        }
    return {
        "count": int(finite.size),
        "minimum": float(np.min(finite)),
        "p05": float(np.quantile(finite, 0.05)),
        "p16": float(np.quantile(finite, 0.16)),
        "median": float(np.median(finite)),
        "p84": float(np.quantile(finite, 0.84)),
        "p95": float(np.quantile(finite, 0.95)),
        "maximum": float(np.max(finite)),
    }


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def load_galaxy_lab() -> ModuleType:
    source = GALAXY_REPO / "scripts" / "mts-failure-lab.py"
    module_name = "mts_failure_lab_read_only_5198"
    specification = importlib.util.spec_from_file_location(module_name, source)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import galaxy lab from {source}")
    module = importlib.util.module_from_spec(specification)
    sys.modules[module_name] = module
    specification.loader.exec_module(module)
    return module


def response_support(q_value: float, argument: float) -> float:
    def integrand(integration_variable: float) -> float:
        if integration_variable == 0.0:
            return 0.0
        ratio = argument / integration_variable
        return (
            math.sin(integration_variable)
            / integration_variable
            * ratio ** (1.0 + q_value)
            / (1.0 + ratio**q_value) ** 2
        )

    integral = quad(
        integrand,
        0.0,
        1.0,
        epsabs=3.0e-10,
        epsrel=3.0e-9,
        limit=400,
    )[0]
    left_edge = 1.0
    while left_edge < SPECTRAL_INTEGRATION_LIMIT:
        right_edge = min(left_edge + math.pi, SPECTRAL_INTEGRATION_LIMIT)
        integral += quad(
            integrand,
            left_edge,
            right_edge,
            epsabs=2.0e-10,
            epsrel=2.0e-8,
            limit=80,
        )[0]
        left_edge = right_edge
    return 1.0 - q_value * integral / argument


@lru_cache(maxsize=64)
def spectral_scale(q_value: float) -> tuple[float, float, float, float]:
    kernel_arguments = np.logspace(-4.0, math.log10(200.0), 120)
    kernel_support = np.asarray(
        [response_support(q_value, float(argument)) for argument in kernel_arguments]
    )
    interpolation = PchipInterpolator(np.log(kernel_arguments), kernel_support)
    comparison_radius = np.logspace(-3.0, 1.5, 80)
    canonical_support = 1.0 - np.exp(-(comparison_radius**q_value))

    def loss(log_scale: float) -> float:
        prediction = interpolation(np.log(comparison_radius) + log_scale)
        return float(np.mean((prediction - canonical_support) ** 2))

    optimization = minimize_scalar(
        loss,
        bounds=(math.log(0.5), math.log(5.0)),
        method="bounded",
        options={"xatol": 1.0e-9},
    )
    best_scale = math.exp(float(optimization.x))
    best_loss = loss(math.log(best_scale))
    scale_grid = np.linspace(2.0, 4.0, 20001)
    losses = np.asarray([loss(math.log(float(scale))) for scale in scale_grid])
    width_mask_0p1 = losses <= best_loss * 1.001
    width_mask_1 = losses <= best_loss * 1.01
    width_0p1 = float(scale_grid[width_mask_0p1][-1] - scale_grid[width_mask_0p1][0])
    width_1 = float(scale_grid[width_mask_1][-1] - scale_grid[width_mask_1][0])
    return best_scale, math.sqrt(best_loss), width_0p1, width_1


def self_similar_cq(q_value: float) -> float:
    density_power = 1.0 - q_value
    force_coefficient = (
        gamma(1.0 - density_power / 2.0)
        * gamma((1.0 + density_power) / 2.0)
        / (
            gamma((3.0 - density_power) / 2.0)
            * gamma(density_power / 2.0)
        )
    )
    return float(1.0 / force_coefficient)


def phase_values(
    radius_over_l: float,
    q_value: float = Q_LOCKED,
    boundary_over_l: float = BOUNDARY_OVER_L,
    wall_exponent: float = WALL_EXPONENT,
) -> tuple[float, float, float]:
    transition_coefficient = self_similar_cq(q_value)
    occupation = (
        transition_coefficient
        * radius_over_l**q_value
        / (1.0 + transition_coefficient * radius_over_l**q_value)
    )
    boundary = 1.0 / (
        1.0 + (radius_over_l / boundary_over_l) ** wall_exponent
    )
    dimensionless_surface_load = occupation * boundary / (2.0 * radius_over_l)
    return occupation, boundary, dimensionless_surface_load


def plummer_soft_wavenumber(
    dimensionless_surface_load: float,
    radial_coefficient: float = RADIAL_DISPERSION_COEFFICIENT,
    thickness_over_l: float = THICKNESS_OVER_L,
) -> float:
    thin_value = dimensionless_surface_load / radial_coefficient
    if thickness_over_l == 0.0:
        return thin_value
    upper = min(thin_value, 0.999999 / thickness_over_l)
    return float(
        brentq(
            lambda wavenumber: (
                radial_coefficient * wavenumber
                - dimensionless_surface_load
                * math.exp(-thickness_over_l * wavenumber)
                * (1.0 - thickness_over_l * wavenumber)
            ),
            0.0,
            upper,
        )
    )


def locked_soft_wavenumber(
    q_value: float,
    thickness_over_l: float = THICKNESS_OVER_L,
    boundary_over_l: float = BOUNDARY_OVER_L,
    wall_exponent: float = WALL_EXPONENT,
    radial_coefficient: float = RADIAL_DISPERSION_COEFFICIENT,
) -> float:
    _, _, surface_load = phase_values(
        1.0,
        q_value=q_value,
        boundary_over_l=boundary_over_l,
        wall_exponent=wall_exponent,
    )
    return plummer_soft_wavenumber(
        surface_load,
        radial_coefficient=radial_coefficient,
        thickness_over_l=thickness_over_l,
    )


def load_selected_kernel() -> tuple[np.ndarray, np.ndarray]:
    rows = read_csv(
        GALAXY_PACKS
        / "mts-v19-phase-flow-closure-v1"
        / "mts_v19_phase_flow_closure_kernel_profiles.csv"
    )
    selected = sorted(
        (row for row in rows if row["variantId"] == "B8-s4"),
        key=lambda row: float(row["radiusOverL"]),
    )
    return (
        np.asarray([float(row["radiusOverL"]) for row in selected]),
        np.asarray([float(row["smoothPhaseKernel"]) for row in selected]),
    )


def derivation_rows() -> list[dict[str, Any]]:
    return tagged(
        [
            {
                "step": "CH5198_00_thin_disk_constraint",
                "premise": "delta Sigma proportional to exp[i(kR-omega t)]",
                "equation": "delta Phi_k=-2 pi G delta Sigma_k exp(-|k|H)/|k|",
                "result": "Plummer-softened metric constraint",
                "status": "DERIVED_FROM_3D_POISSON_GREEN_FUNCTION",
            },
            {
                "step": "CH5198_01_conservation",
                "premise": "conserved axisymmetric barotropic surface stress",
                "equation": (
                    "-i omega delta Sigma+i k Sigma delta u_R=0; "
                    "-i omega delta u_R-2 Omega delta u_phi=-ik(delta h+delta Phi); "
                    "-i omega delta u_phi+kappa^2 delta u_R/(2 Omega)=0"
                ),
                "result": "continuity plus radial and azimuthal Euler equations",
                "status": "EXACT_WKB_LINEAR_SYSTEM",
            },
            {
                "step": "CH5198_02_collective_Hessian",
                "premise": "delta h=c_R^2 delta Sigma/Sigma",
                "equation": (
                    "omega^2=lambda(k)=kappa^2+c_R^2 k^2-"
                    "2 pi G Sigma |k| exp(-|k|H)"
                ),
                "result": "metric-dressed collective eigenvalue",
                "status": "DERIVED_BY_ELIMINATION",
            },
            {
                "step": "CH5198_03_thin_limit",
                "premise": "H=0",
                "equation": (
                    "k_star=pi G Sigma/c_R^2; "
                    "lambda_min=kappa^2-(pi G Sigma)^2/c_R^2; "
                    "Q=kappa c_R/(pi G Sigma)"
                ),
                "result": "lambda_min=kappa^2(1-Q^-2)",
                "status": "EXACT",
            },
            {
                "step": "CH5198_04_outer_phase",
                "premise": (
                    "Sigma_chi=Gamma0/(2 pi G y), "
                    "V_chi^2=Gamma0 L, kappa_chi^2=2 Gamma0/(L y^2)"
                ),
                "equation": "Q_chi=1",
                "result": "c_R^2=Gamma0 L/8",
                "status": "DERIVED_MARGINAL_MESTEL_AMPLITUDE_LAW",
            },
            {
                "step": "CH5198_05_local_vacuum",
                "premise": "Sigma_chi=0 and no occupied phase worldvolume",
                "equation": "delta Sigma_chi is absent; B_hchi=0",
                "result": "no new vacuum pole and checkpoint-5187 local Hessian is unchanged",
                "status": "EXACT_STATE_ABSENCE_LIMIT",
            },
            {
                "step": "CH5198_06_no_double_count",
                "premise": "use lambda(k) only to form and test the phase state",
                "equation": "T_total=T_b+T_phase; do not add a second polarization source",
                "result": "collective response is not replayed on top of its own background stress",
                "status": "COUNTING_CONTRACT",
            },
        ]
    )


def universal_profile_rows() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    radius_grid, support_grid = load_selected_kernel()
    support_interpolation = PchipInterpolator(radius_grid, support_grid)
    support_derivative = support_interpolation.derivative()
    rows: list[dict[str, Any]] = []
    active_q: list[float] = []
    active_lambda: list[float] = []
    active_enhancement: list[float] = []
    for point_index, (radius_over_l, support) in enumerate(
        zip(radius_grid, support_grid)
    ):
        support_prime = float(support_derivative(radius_over_l))
        occupation, boundary, surface_load = phase_values(float(radius_over_l))
        phase_kappa_dimensionless = (
            support_prime / radius_over_l + 2.0 * support / radius_over_l**2
        )
        thin_q = (
            math.sqrt(
                phase_kappa_dimensionless * RADIAL_DISPERSION_COEFFICIENT
            )
            / surface_load
        )
        soft_wavenumber = plummer_soft_wavenumber(surface_load)
        minimum_eigenvalue = (
            phase_kappa_dimensionless
            + RADIAL_DISPERSION_COEFFICIENT * soft_wavenumber**2
            - 2.0
            * surface_load
            * soft_wavenumber
            * math.exp(-THICKNESS_OVER_L * soft_wavenumber)
        )
        enhancement = phase_kappa_dimensionless / minimum_eigenvalue
        surface_log_slope = (
            Q_LOCKED * (1.0 - occupation)
            - WALL_EXPONENT * (1.0 - boundary)
            - 1.0
        )
        streaming_speed_squared_norm = (
            support
            + RADIAL_DISPERSION_COEFFICIENT * surface_log_slope
        )
        active = 0.5 <= radius_over_l <= 2.0
        if active:
            active_q.append(thin_q)
            active_lambda.append(minimum_eigenvalue)
            active_enhancement.append(enhancement)
        rows.append(
            {
                "point_index": point_index,
                "radius_over_L": radius_over_l,
                "smooth_phase_support_F": support,
                "dF_dy": support_prime,
                "occupation_n": occupation,
                "boundary_b": boundary,
                "surface_load_piG_Sigma_over_Gamma0": surface_load,
                "phase_kappa2_L_over_Gamma0": phase_kappa_dimensionless,
                "radial_dispersion_over_Gamma0L": (
                    RADIAL_DISPERSION_COEFFICIENT
                ),
                "thin_Toomre_Q_phase": thin_q,
                "Plummer_kstar_L": soft_wavenumber,
                "Plummer_wavelength_over_L": 2.0 * math.pi / soft_wavenumber,
                "Plummer_lambda_min_L_over_Gamma0": minimum_eigenvalue,
                "static_collective_enhancement": enhancement,
                "surface_log_slope": surface_log_slope,
                "streaming_speed_squared_over_Gamma0L": (
                    streaming_speed_squared_norm
                ),
                "active_annulus": active,
            }
        )
    dense_radius = np.geomspace(
        float(radius_grid[0]),
        float(radius_grid[-1]),
        10000,
    )

    def streaming_speed_squared_norm(radius_over_l: float) -> float:
        occupation, boundary, _ = phase_values(radius_over_l)
        surface_log_slope = (
            Q_LOCKED * (1.0 - occupation)
            - WALL_EXPONENT * (1.0 - boundary)
            - 1.0
        )
        return float(
            support_interpolation(radius_over_l)
            + RADIAL_DISPERSION_COEFFICIENT * surface_log_slope
        )

    dense_streaming = np.asarray(
        [
            streaming_speed_squared_norm(float(radius_over_l))
            for radius_over_l in dense_radius
        ]
    )
    streaming_roots: list[float] = []
    for left_index in np.where(np.diff(np.signbit(dense_streaming)))[0]:
        streaming_roots.append(
            float(
                brentq(
                    streaming_speed_squared_norm,
                    float(dense_radius[left_index]),
                    float(dense_radius[left_index + 1]),
                )
            )
        )
    diagnostics = {
        "active_Q": finite_quantiles(active_q),
        "active_lambda": finite_quantiles(active_lambda),
        "active_enhancement": finite_quantiles(active_enhancement),
        "active_maximum_abs_Q_minus_one": float(
            np.max(np.abs(np.asarray(active_q) - 1.0))
        ),
        "full_minimum_lambda": min(
            float(row["Plummer_lambda_min_L_over_Gamma0"]) for row in rows
        ),
        "full_minimum_streaming_speed_squared_norm": min(
            float(row["streaming_speed_squared_over_Gamma0L"]) for row in rows
        ),
        "streaming_speed_squared_zeroes_radius_over_L": streaming_roots,
    }
    return tagged(rows), diagnostics


def scale_bridge_rows() -> tuple[
    list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]
]:
    locked_scale, locked_rmse, width_0p1, width_1 = spectral_scale(Q_LOCKED)
    locked_wavenumber = locked_soft_wavenumber(Q_LOCKED)
    locked_relative_residual = abs(locked_wavenumber / locked_scale - 1.0)

    q_root = brentq(
        lambda q_value: locked_soft_wavenumber(q_value)
        - spectral_scale(q_value)[0],
        0.76,
        0.78,
        xtol=2.0e-10,
    )
    root_scale = spectral_scale(q_root)[0]
    root_wavenumber = locked_soft_wavenumber(q_root)

    _, _, surface_load_at_one = phase_values(1.0)
    required_thickness = brentq(
        lambda thickness: (
            RADIAL_DISPERSION_COEFFICIENT * locked_scale
            - surface_load_at_one
            * math.exp(-thickness * locked_scale)
            * (1.0 - thickness * locked_scale)
        ),
        0.0,
        0.1,
    )
    thin_wavenumber = locked_soft_wavenumber(Q_LOCKED, thickness_over_l=0.0)
    scale_rows = tagged(
        [
            {
                "bridge_id": "SB5198_00_locked_spectral_scale",
                "quantity": "mu_spectral L_eff",
                "value": locked_scale,
                "comparison": SPECTRAL_SCALE_5148,
                "relative_residual": abs(locked_scale / SPECTRAL_SCALE_5148 - 1.0),
                "status": "CHECKPOINT_5148_REPRODUCED",
            },
            {
                "bridge_id": "SB5198_01_Plummer_soft_mode",
                "quantity": "k_star L_eff at y=1",
                "value": locked_wavenumber,
                "comparison": locked_scale,
                "relative_residual": locked_relative_residual,
                "status": "CONDITIONAL_SCALE_BRIDGE_DERIVED",
            },
            {
                "bridge_id": "SB5198_02_soft_wavelength",
                "quantity": "2 pi/(k_star L_eff)",
                "value": 2.0 * math.pi / locked_wavenumber,
                "comparison": math.nan,
                "relative_residual": math.nan,
                "status": "ORDER_L_COLLECTIVE_WAVELENGTH",
            },
            {
                "bridge_id": "SB5198_03_self_consistent_q",
                "quantity": "q solving k_star(q)L=mu_spectral(q)L",
                "value": q_root,
                "comparison": Q_LOCKED,
                "relative_residual": abs(q_root / Q_LOCKED - 1.0),
                "status": "CONDITIONAL_Q_CLOSURE",
            },
            {
                "bridge_id": "SB5198_04_required_thickness",
                "quantity": "eta solving k_star L=locked spectral scale",
                "value": required_thickness,
                "comparison": THICKNESS_OVER_L,
                "relative_residual": abs(
                    required_thickness / THICKNESS_OVER_L - 1.0
                ),
                "status": "CONDITIONAL_THICKNESS_CLOSURE",
            },
            {
                "bridge_id": "SB5198_05_zero_thickness_control",
                "quantity": "thin k_star L at y=1",
                "value": thin_wavenumber,
                "comparison": locked_scale,
                "relative_residual": abs(thin_wavenumber / locked_scale - 1.0),
                "status": "CONTROL_DOES_NOT_CLOSE",
            },
            {
                "bridge_id": "SB5198_06_scale_width_0p1_percent_loss",
                "quantity": "full width in mu L",
                "value": width_0p1,
                "comparison": locked_scale,
                "relative_residual": width_0p1 / locked_scale,
                "status": "MATCH_NOT_STATISTICALLY_INDEPENDENT",
            },
            {
                "bridge_id": "SB5198_07_scale_width_1_percent_loss",
                "quantity": "full width in mu L",
                "value": width_1,
                "comparison": locked_scale,
                "relative_residual": width_1 / locked_scale,
                "status": "SHARED_PROFILE_CAVEAT",
            },
        ]
    )

    sweep_values = [
        0.55,
        0.60,
        0.65,
        0.70,
        0.72,
        0.74,
        0.75,
        0.76,
        0.77,
        0.78,
        0.79,
        0.80,
        0.82,
        0.85,
        0.88,
        0.90,
    ]
    sweep_rows = tagged(
        [
            {
                "q": q_value,
                "c_q": self_similar_cq(q_value),
                "spectral_mu_L": spectral_scale(q_value)[0],
                "Plummer_kstar_L": locked_soft_wavenumber(q_value),
                "fractional_scale_difference": (
                    locked_soft_wavenumber(q_value) / spectral_scale(q_value)[0]
                    - 1.0
                ),
                "spectral_shape_RMSE": spectral_scale(q_value)[1],
            }
            for q_value in sweep_values
        ]
    )
    diagnostics = {
        "locked_spectral_scale": locked_scale,
        "locked_spectral_rmse": locked_rmse,
        "locked_Plummer_wavenumber": locked_wavenumber,
        "locked_relative_residual": locked_relative_residual,
        "self_consistent_q": q_root,
        "self_consistent_q_relative_residual": abs(q_root / Q_LOCKED - 1.0),
        "self_consistent_scale": root_scale,
        "self_consistent_wavenumber": root_wavenumber,
        "required_thickness": required_thickness,
        "required_thickness_relative_residual": abs(
            required_thickness / THICKNESS_OVER_L - 1.0
        ),
        "thin_control_wavenumber": thin_wavenumber,
        "scale_loss_width_0p1_percent": width_0p1,
        "scale_loss_width_1_percent": width_1,
    }
    return scale_rows, sweep_rows, diagnostics


def clean_galaxy_replay(
    galaxy_lab: ModuleType,
) -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    dict[str, Any],
]:
    curves = {
        curve["name"]: curve
        for curve in (
            galaxy_lab.build_curve(sample) for sample in galaxy_lab.load_samples()
        )
    }
    eos_rows = read_csv(
        GALAXY_PACKS
        / "mts-v19-nonanalytic-phase-pilot-v1"
        / "mts_v19_nonanalytic_phase_eos_reconstruction.csv"
    )
    grouped_rows: dict[str, list[dict[str, str]]] = {}
    for row in eos_rows:
        if (
            row["supportModel"] == "canonical MTS"
            and row["fitEligible"].strip().lower() == "true"
        ):
            grouped_rows.setdefault(row["galaxy"], []).append(row)

    radius_grid, support_grid = load_selected_kernel()
    support_interpolation = PchipInterpolator(radius_grid, support_grid)
    gamma0 = float(galaxy_lab.GAMMA0)
    gravitational_constant = float(galaxy_lab.TNG_G)
    point_rows: list[dict[str, Any]] = []
    case_rows: list[dict[str, Any]] = []

    for galaxy_name, rows in sorted(grouped_rows.items()):
        curve = curves[galaxy_name]
        ordered = sorted(rows, key=lambda row: float(row["radiusKpc"]))
        radius_kpc = np.asarray([float(row["radiusKpc"]) for row in ordered])
        radius_over_l = radius_kpc / float(curve["leff"])
        eos_sound_speed_squared = np.asarray(
            [float(row["soundSpeedSquaredNorm"]) for row in ordered]
        ) * float(curve["points"][-1]["bar2"])
        baryon_radius = np.asarray([point["r"] for point in curve["points"]])
        baryon_speed_squared_source = np.asarray(
            [point["bar2"] for point in curve["points"]]
        )
        baryon_speed_squared = np.interp(
            radius_kpc,
            baryon_radius,
            baryon_speed_squared_source,
        )
        phase_speed_squared = (
            gamma0 * float(curve["leff"]) * support_interpolation(radius_over_l)
        )
        total_speed_squared = baryon_speed_squared + phase_speed_squared
        total_speed_derivative = np.gradient(
            total_speed_squared,
            radius_kpc,
            edge_order=2,
        )
        kappa_squared = (
            total_speed_derivative / radius_kpc
            + 2.0 * total_speed_squared / radius_kpc**2
        )
        collective_sound_speed_squared = (
            RADIAL_DISPERSION_COEFFICIENT
            * gamma0
            * float(curve["leff"])
        )
        phase_fraction = phase_speed_squared / total_speed_squared

        galaxy_point_rows: list[dict[str, Any]] = []
        for point_index, (
            radius,
            scaled_radius,
            phase_fraction_value,
            kappa_squared_value,
            eos_speed_squared_value,
        ) in enumerate(
            zip(
                radius_kpc,
                radius_over_l,
                phase_fraction,
                kappa_squared,
                eos_sound_speed_squared,
            )
        ):
            occupation, boundary, dimensionless_surface_load = phase_values(
                float(scaled_radius)
            )
            surface_density = (
                gamma0
                / gravitational_constant
                * occupation
                * boundary
                / (2.0 * math.pi * scaled_radius)
            )
            gravity_surface_scale = gamma0 * dimensionless_surface_load
            collective_q = (
                math.sqrt(
                    kappa_squared_value * collective_sound_speed_squared
                )
                / gravity_surface_scale
            )
            eos_q = (
                math.sqrt(kappa_squared_value * eos_speed_squared_value)
                / gravity_surface_scale
            )
            soft_wavenumber = plummer_soft_wavenumber(
                dimensionless_surface_load
            )
            kappa_dimensionless = (
                kappa_squared_value * float(curve["leff"]) / gamma0
            )
            minimum_eigenvalue_dimensionless = (
                kappa_dimensionless
                + RADIAL_DISPERSION_COEFFICIENT * soft_wavenumber**2
                - 2.0
                * dimensionless_surface_load
                * soft_wavenumber
                * math.exp(-THICKNESS_OVER_L * soft_wavenumber)
            )
            enhancement = (
                kappa_dimensionless / minimum_eigenvalue_dimensionless
                if minimum_eigenvalue_dimensionless > 0.0
                else math.nan
            )
            active = 0.5 <= scaled_radius <= 2.0
            point_row = {
                "galaxy": galaxy_name,
                "set": ordered[point_index]["set"],
                "fold": ordered[point_index]["fold"],
                "locked_route": ordered[point_index]["lockedRoute"],
                "point_index": point_index,
                "radius_kpc": radius,
                "radius_over_L": scaled_radius,
                "L_eff_kpc": float(curve["leff"]),
                "f_gas_out": float(curve["fGasOut"]),
                "phase_fraction": phase_fraction_value,
                "kappa_squared_km2_s2_kpc2": kappa_squared_value,
                "surface_density_Msun_kpc2": surface_density,
                "collective_cR2_km2_s2": collective_sound_speed_squared,
                "spherical_EOS_c2_km2_s2": eos_speed_squared_value,
                "spherical_EOS_over_collective_cR2": (
                    eos_speed_squared_value / collective_sound_speed_squared
                ),
                "collective_Q": collective_q,
                "spherical_EOS_Q": eos_q,
                "Plummer_kstar_L": soft_wavenumber,
                "Plummer_lambda_min_L_over_Gamma0": (
                    minimum_eigenvalue_dimensionless
                ),
                "static_collective_enhancement": enhancement,
                "active_annulus": active,
                "unstable_flag": minimum_eigenvalue_dimensionless <= 0.0,
            }
            galaxy_point_rows.append(point_row)
            point_rows.append(point_row)

        active_rows = [
            row for row in galaxy_point_rows if bool(row["active_annulus"])
        ]
        if not active_rows:
            continue
        positive_active = [
            row
            for row in active_rows
            if float(row["Plummer_lambda_min_L_over_Gamma0"]) > 0.0
        ]
        unstable_active = [
            row
            for row in active_rows
            if bool(row["unstable_flag"])
        ]
        case_rows.append(
            {
                "galaxy": galaxy_name,
                "set": active_rows[0]["set"],
                "fold": active_rows[0]["fold"],
                "locked_route": active_rows[0]["locked_route"],
                "L_eff_kpc": float(curve["leff"]),
                "f_gas_out": float(curve["fGasOut"]),
                "active_point_count": len(active_rows),
                "median_collective_Q": float(
                    np.median([float(row["collective_Q"]) for row in active_rows])
                ),
                "minimum_collective_Q": min(
                    float(row["collective_Q"]) for row in active_rows
                ),
                "median_spherical_EOS_Q": float(
                    np.median(
                        [float(row["spherical_EOS_Q"]) for row in active_rows]
                    )
                ),
                "median_spherical_EOS_over_collective_cR2": float(
                    np.median(
                        [
                            float(row["spherical_EOS_over_collective_cR2"])
                            for row in active_rows
                        ]
                    )
                ),
                "median_phase_fraction": float(
                    np.median([float(row["phase_fraction"]) for row in active_rows])
                ),
                "median_static_collective_enhancement": (
                    float(
                        np.median(
                            [
                                float(row["static_collective_enhancement"])
                                for row in positive_active
                            ]
                        )
                    )
                    if positive_active
                    else math.nan
                ),
                "median_Plummer_kstar_L": float(
                    np.median(
                        [float(row["Plummer_kstar_L"]) for row in active_rows]
                    )
                ),
                "active_unstable_point_count": len(unstable_active),
                "active_unstable_radii_kpc": ";".join(
                    f"{float(row['radius_kpc']):.12g}" for row in unstable_active
                ),
                "case_status": (
                    "COUNTERCASE_REQUIRES_2D_STABILITY_REPLAY"
                    if unstable_active
                    else "STABLE_IN_EXECUTED_AXISYMMETRIC_WKB_REPLAY"
                ),
            }
        )

    band_definitions = [
        ("inner_core", 0.0, 0.25),
        ("inner_transition", 0.25, 0.5),
        ("active_inner", 0.5, 1.0),
        ("active_outer", 1.0, 2.0),
        ("outer_transition", 2.0, 4.0),
        ("boundary", 4.0, 8.0),
        ("active_total", 0.5, 2.0),
    ]
    band_rows: list[dict[str, Any]] = []
    for band_name, lower, upper in band_definitions:
        selected = [
            row
            for row in point_rows
            if lower <= float(row["radius_over_L"]) < upper
        ]
        positive = [
            row
            for row in selected
            if float(row["Plummer_lambda_min_L_over_Gamma0"]) > 0.0
        ]
        collective_q_values = np.asarray(
            [float(row["collective_Q"]) for row in selected]
        )
        eos_q_values = np.asarray(
            [float(row["spherical_EOS_Q"]) for row in selected]
        )
        collective_stats = finite_quantiles(collective_q_values)
        eos_stats = finite_quantiles(eos_q_values)
        phase_stats = finite_quantiles(
            [float(row["phase_fraction"]) for row in selected]
        )
        enhancement_stats = finite_quantiles(
            [float(row["static_collective_enhancement"]) for row in positive]
        )
        wavenumber_stats = finite_quantiles(
            [float(row["Plummer_kstar_L"]) for row in selected]
        )
        eos_ratio_stats = finite_quantiles(
            [
                float(row["spherical_EOS_over_collective_cR2"])
                for row in selected
            ]
        )
        band_rows.append(
            {
                "band": band_name,
                "lower_radius_over_L": lower,
                "upper_radius_over_L": upper,
                "point_count": len(selected),
                "galaxy_count": len({str(row["galaxy"]) for row in selected}),
                "collective_Q_minimum": collective_stats["minimum"],
                "collective_Q_p16": collective_stats["p16"],
                "collective_Q_median": collective_stats["median"],
                "collective_Q_p84": collective_stats["p84"],
                "spherical_EOS_Q_median": eos_stats["median"],
                "phase_fraction_median": phase_stats["median"],
                "enhancement_median_positive": enhancement_stats["median"],
                "Plummer_kstar_L_median": wavenumber_stats["median"],
                "spherical_EOS_over_collective_cR2_median": eos_ratio_stats[
                    "median"
                ],
                "fraction_collective_Q_0p8_to_1p25": float(
                    np.mean(
                        (collective_q_values >= 0.8)
                        & (collective_q_values <= 1.25)
                    )
                ),
                "fraction_spherical_EOS_Q_0p8_to_1p25": float(
                    np.mean((eos_q_values >= 0.8) & (eos_q_values <= 1.25))
                ),
                "unstable_point_count": sum(
                    bool(row["unstable_flag"]) for row in selected
                ),
                "unstable_fraction": float(
                    np.mean([bool(row["unstable_flag"]) for row in selected])
                ),
            }
        )

    active_points = [
        row for row in point_rows if bool(row["active_annulus"])
    ]
    positive_active = [
        row
        for row in active_points
        if float(row["Plummer_lambda_min_L_over_Gamma0"]) > 0.0
    ]
    correlation_matrix = np.corrcoef(
        np.asarray(
            [
                [
                    float(row["phase_fraction"]),
                    math.log(float(row["static_collective_enhancement"])),
                ]
                for row in positive_active
            ]
        ).T
    )
    active_case_q = finite_quantiles(
        [float(row["median_collective_Q"]) for row in case_rows]
    )
    active_case_eos_q = finite_quantiles(
        [float(row["median_spherical_EOS_Q"]) for row in case_rows]
    )
    active_case_enhancement = finite_quantiles(
        [
            float(row["median_static_collective_enhancement"])
            for row in case_rows
        ]
    )
    diagnostics = {
        "loaded_curve_count": len(curves),
        "clean_eos_galaxy_count": len(grouped_rows),
        "case_summary_count": len(case_rows),
        "point_count": len(point_rows),
        "active_point_count": len(active_points),
        "active_unstable_point_count": sum(
            bool(row["unstable_flag"]) for row in active_points
        ),
        "active_unstable_galaxies": sorted(
            {
                str(row["galaxy"])
                for row in active_points
                if bool(row["unstable_flag"])
            }
        ),
        "all_kappa_squared_positive": all(
            float(row["kappa_squared_km2_s2_kpc2"]) > 0.0 for row in point_rows
        ),
        "active_case_collective_Q": active_case_q,
        "active_case_spherical_EOS_Q": active_case_eos_q,
        "active_case_enhancement": active_case_enhancement,
        "active_phase_fraction_log_enhancement_correlation": float(
            correlation_matrix[0, 1]
        ),
    }
    return tagged(case_rows), tagged(band_rows), point_rows, diagnostics


def stress_selection_rows(
    band_rows: list[dict[str, Any]],
    replay_diagnostics: dict[str, Any],
) -> list[dict[str, Any]]:
    active = next(row for row in band_rows if row["band"] == "active_total")
    return tagged(
        [
            {
                "candidate": "spherical reconstructed EOS as disk radial pressure",
                "executed_value": active["spherical_EOS_Q_median"],
                "comparison": active[
                    "spherical_EOS_over_collective_cR2_median"
                ],
                "diagnostic": (
                    "median Q and median c_EOS^2/(Gamma0 L/8), respectively"
                ),
                "decision": "REJECT_DIRECT_IDENTIFICATION",
                "reason": (
                    "the spherical diagnostic is too stiff for the collective "
                    "soft branch and its own source file already requires an "
                    "axisymmetric anisotropic completion"
                ),
            },
            {
                "candidate": "marginal Mestel radial dispersion",
                "executed_value": active["collective_Q_median"],
                "comparison": active["fraction_collective_Q_0p8_to_1p25"],
                "diagnostic": (
                    "active-point median Q and fraction in 0.8<=Q<=1.25"
                ),
                "decision": "RETAIN_AS_DERIVED_ASYMPTOTIC_RADIAL_STRESS_LAW",
                "reason": (
                    "c_R^2=Gamma0 L/8 follows from the phase outer normalization "
                    "and Q=1, with no per-galaxy coefficient"
                ),
            },
            {
                "candidate": "finite-thickness total-background stability",
                "executed_value": replay_diagnostics[
                    "active_unstable_point_count"
                ],
                "comparison": ";".join(
                    replay_diagnostics["active_unstable_galaxies"]
                ),
                "diagnostic": "unstable active points and galaxies",
                "decision": "RETAIN_WITH_EXPLICIT_COUNTERCASES",
                "reason": (
                    "the small countercase set is not erased; it requires a "
                    "native 2D derivative and stability replay"
                ),
            },
            {
                "candidate": "local vacuum continuation",
                "executed_value": 0.0,
                "comparison": 0.0,
                "diagnostic": "Sigma_chi and occupied-state residue",
                "decision": "EXACTLY_SILENT_WHEN_STATE_ABSENT",
                "reason": (
                    "the collective coordinate is a state fluctuation, not a "
                    "second vacuum propagator"
                ),
            },
        ]
    )


def logistic_vertex_rows() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    q_squared = Q_LOCKED**2
    wall_squared = WALL_EXPONENT**2
    bare_fractional_invariant = 0.4
    required_logistic_invariant = 3.0
    rows = tagged(
        [
            {
                "vertex_id": "LV5198_00_inner_BPS_action",
                "field": "n",
                "effective_potential": "V_n=q^2 n^2(1-n)^2/2",
                "m2": q_squared,
                "g3_factorial_convention": -6.0 * q_squared,
                "g4_factorial_convention": 12.0 * q_squared,
                "first_order_flow": "dn/du=q n(1-n)",
                "status": "EXACT_REDUCED_ACTION_CONTRACT",
            },
            {
                "vertex_id": "LV5198_01_outer_BPS_action",
                "field": "b",
                "effective_potential": "V_b=s^2 b^2(1-b)^2/2",
                "m2": wall_squared,
                "g3_factorial_convention": -6.0 * wall_squared,
                "g4_factorial_convention": 12.0 * wall_squared,
                "first_order_flow": "db/du=-s b(1-b)",
                "status": "EXACT_REDUCED_ACTION_CONTRACT",
            },
            {
                "vertex_id": "LV5198_02_reflection_even_composite",
                "field": "n=psi^2/v^2 or normalized two-point occupation",
                "effective_potential": (
                    "q^2[psi^4/v^4-2psi^6/v^6+psi^8/v^8]/2"
                ),
                "m2": 0.0,
                "g3_factorial_convention": math.nan,
                "g4_factorial_convention": math.nan,
                "first_order_flow": "composite rather than one-particle vacuum flow",
                "status": "REFLECTION_SYMMETRY_COMPATIBLE_COMPOSITE_COMPLETION",
            },
            {
                "vertex_id": "LV5198_03_parent_fractional_vertices",
                "field": "canonical psi about psi0!=0",
                "effective_potential": "V=(3/4)g_psi |psi|^(4/3)",
                "m2": "g_psi/(3|psi0|^(2/3))",
                "g3_factorial_convention": "-2g_psi/(9|psi0|^(5/3))",
                "g4_factorial_convention": "10g_psi/(27|psi0|^(8/3))",
                "first_order_flow": "none",
                "status": "DIRECT_BARE_LOGISTIC_MAP_REJECTED",
            },
            {
                "vertex_id": "LV5198_04_shape_invariant",
                "field": "canonical linear field identification",
                "effective_potential": "I=g3^2/(m2 g4)",
                "m2": required_logistic_invariant,
                "g3_factorial_convention": bare_fractional_invariant,
                "g4_factorial_convention": (
                    required_logistic_invariant / bare_fractional_invariant
                ),
                "first_order_flow": "I_logistic=3 versus I_fractional=2/5",
                "status": "NO_CANONICAL_LINEAR_IDENTIFICATION",
            },
            {
                "vertex_id": "LV5198_05_surviving_route",
                "field": "2PI occupation/covariance composite",
                "effective_potential": (
                    "Gamma_2PI[n] must generate m2:g3:g4=q^2:-6q^2:12q^2"
                ),
                "m2": q_squared,
                "g3_factorial_convention": -6.0 * q_squared,
                "g4_factorial_convention": 12.0 * q_squared,
                "first_order_flow": "Bogomolny reduction after state formation",
                "status": "OPEN_PARENT_VERTEX_CALCULATION_NOT_ASSUMED",
            },
        ]
    )
    diagnostics = {
        "q_squared": q_squared,
        "inner_g3": -6.0 * q_squared,
        "inner_g4": 12.0 * q_squared,
        "logistic_shape_invariant": required_logistic_invariant,
        "fractional_parent_shape_invariant": bare_fractional_invariant,
        "invariant_ratio": (
            required_logistic_invariant / bare_fractional_invariant
        ),
    }
    return rows, diagnostics


def route_decision_rows(
    scale_diagnostics: dict[str, Any],
    profile_diagnostics: dict[str, Any],
    replay_diagnostics: dict[str, Any],
) -> list[dict[str, Any]]:
    return tagged(
        [
            {
                "route": "elementary pole owns galaxy scale",
                "decision": "REJECTED_BY_5197_UNCHANGED",
                "derived_support": "none",
                "remaining_condition": "none",
            },
            {
                "route": "occupied phase disk collective Hessian",
                "decision": "RETAIN_AS_QUADRATIC_CARRIER",
                "derived_support": (
                    "metric constraint plus conserved surface stress gives "
                    "the Plummer-softened eigenvalue"
                ),
                "remaining_condition": (
                    "derive state formation and complete covariant stress"
                ),
            },
            {
                "route": "marginal Mestel radial amplitude",
                "decision": "DERIVED_ASYMPTOTICALLY",
                "derived_support": "c_R^2=Gamma0 L_eff/8",
                "remaining_condition": (
                    "derive why the occupied state self-regulates to this branch"
                ),
            },
            {
                "route": "spectral-to-collective scale identification",
                "decision": "CONDITIONAL_INTERNAL_CLOSURE",
                "derived_support": (
                    f"relative scale residual={scale_diagnostics['locked_relative_residual']}"
                ),
                "remaining_condition": (
                    "shared-profile origin and broad spectral conversion width "
                    "prevent an independent evidence claim"
                ),
            },
            {
                "route": "spherical EOS supplies disk radial pressure",
                "decision": "REJECTED",
                "derived_support": (
                    "executed clean-sample Q is materially above the soft branch"
                ),
                "remaining_condition": "replace with axisymmetric anisotropic stress",
            },
            {
                "route": "bare fractional scalar directly supplies logistic flow",
                "decision": "REJECTED_FOR_CANONICAL_LINEAR_MAP",
                "derived_support": "vertex-shape invariant 2/5 differs from 3",
                "remaining_condition": "calculate the composite 2PI vertices",
            },
            {
                "route": "local GR/Newton/Maxwell branch",
                "decision": "UNCHANGED_AND_NOT_PROMOTED_BY_5198",
                "derived_support": "state-absence limit preserves block-diagonal vacuum",
                "remaining_condition": (
                    "full source coupling and higher-operator bounds remain separate"
                ),
            },
            {
                "route": "next checkpoint",
                "decision": "CALCULATE_COMPOSITE_2PI_NONLINEAR_VERTICES",
                "derived_support": (
                    f"active phase Q deviation<="
                    f"{profile_diagnostics['active_maximum_abs_Q_minus_one']}; "
                    f"clean countercase galaxies="
                    f"{','.join(replay_diagnostics['active_unstable_galaxies'])}"
                ),
                "remaining_condition": (
                    "obtain or reject the exact logistic vertex ratios without "
                    "inserting them as closure"
                ),
            },
        ]
    )


def source_provenance_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for relative_path, digest in POST_SOURCE_LOCKS.items():
        rows.append(
            {
                "source_path": f"post-checkpoint-work/{relative_path}",
                "sha256": digest,
                "source_role": "parent derivation or predecessor result",
                "access_mode": "read_only",
            }
        )
    for path, digest in EXTERNAL_SOURCE_LOCKS.items():
        rows.append(
            {
                "source_path": str(path),
                "sha256": digest,
                "source_role": (
                    "read-only galaxy formula, kernel, EOS diagnostic or curve loader"
                ),
                "access_mode": "read_only",
            }
        )
    return tagged(rows)


def validation_rows(
    galaxy_before: tuple[str, str],
    output_files: list[Path],
    scale_diagnostics: dict[str, Any],
    profile_diagnostics: dict[str, Any],
    replay_diagnostics: dict[str, Any],
    vertex_diagnostics: dict[str, Any],
    case_rows: list[dict[str, Any]],
    band_rows: list[dict[str, Any]],
    all_output_rows: list[list[dict[str, Any]]],
    galaxy_lab: ModuleType,
) -> list[dict[str, Any]]:
    checks: list[tuple[str, bool, Any]] = []

    def add(name: str, passed: bool, detail: Any) -> None:
        checks.append((name, bool(passed), detail))

    for relative_path, expected in POST_SOURCE_LOCKS.items():
        source = POST / relative_path
        add(
            f"source_lock_{Path(relative_path).name}",
            source.exists() and file_digest(source) == expected,
            source,
        )
    for source, expected in EXTERNAL_SOURCE_LOCKS.items():
        add(
            f"external_source_lock_{source.name}",
            source.exists() and file_digest(source) == expected,
            source,
        )

    phase_formula = load_json(
        GALAXY_PACKS
        / "mts-v19-phase-flow-closure-v1"
        / "mts_v19_phase_flow_closure_formula.json"
    )
    disk_formula = load_json(
        GALAXY_PACKS
        / "mts-v19-self-similar-phase-disk-v1"
        / "mts_v19_self_similar_phase_disk_formula.json"
    )
    add(
        "locked_q_and_cq_loaded",
        abs(float(disk_formula["q"]) - Q_LOCKED) < 1.0e-15
        and abs(float(disk_formula["c_q"]) - C_Q_LOCKED) < 1.0e-14,
        f"q={disk_formula['q']};c_q={disk_formula['c_q']}",
    )
    selected_geometry = phase_formula["selectedGeometry"]
    add(
        "locked_boundary_geometry_loaded",
        abs(float(selected_geometry["boundaryOverL"]) - BOUNDARY_OVER_L)
        < 1.0e-15
        and abs(float(selected_geometry["wallExponent"]) - WALL_EXPONENT)
        < 1.0e-15
        and abs(float(selected_geometry["thicknessOverL"]) - THICKNESS_OVER_L)
        < 1.0e-15,
        selected_geometry,
    )
    add(
        "galaxy_constants_loaded",
        abs(float(galaxy_lab.GAMMA0) - GAMMA0_EXPECTED) < 1.0e-12
        and abs(float(galaxy_lab.TNG_G) - G_KPC_EXPECTED) < 1.0e-18,
        f"Gamma0={galaxy_lab.GAMMA0};G={galaxy_lab.TNG_G}",
    )
    add(
        "checkpoint_5148_scale_reproduced",
        abs(
            scale_diagnostics["locked_spectral_scale"] / SPECTRAL_SCALE_5148
            - 1.0
        )
        < 1.0e-12,
        scale_diagnostics["locked_spectral_scale"],
    )
    add(
        "Plummer_collective_scale_bridge",
        scale_diagnostics["locked_relative_residual"] < 5.0e-4,
        scale_diagnostics["locked_relative_residual"],
    )
    add(
        "self_consistent_q_closes",
        scale_diagnostics["self_consistent_q_relative_residual"] < 5.0e-4,
        scale_diagnostics["self_consistent_q"],
    )
    add(
        "selected_thickness_closes",
        scale_diagnostics["required_thickness_relative_residual"] < 5.0e-3,
        scale_diagnostics["required_thickness"],
    )
    add(
        "active_phase_profile_near_marginal",
        profile_diagnostics["active_maximum_abs_Q_minus_one"] < 0.06,
        profile_diagnostics["active_maximum_abs_Q_minus_one"],
    )
    add(
        "universal_Plummer_profile_stable",
        profile_diagnostics["full_minimum_lambda"] > 0.0,
        profile_diagnostics["full_minimum_lambda"],
    )
    add(
        "clean_curve_and_case_counts",
        replay_diagnostics["loaded_curve_count"] == 175
        and replay_diagnostics["clean_eos_galaxy_count"] == 160
        and replay_diagnostics["case_summary_count"] == 160,
        (
            replay_diagnostics["loaded_curve_count"],
            replay_diagnostics["clean_eos_galaxy_count"],
            replay_diagnostics["case_summary_count"],
        ),
    )
    add(
        "clean_replay_kappa_positive",
        replay_diagnostics["all_kappa_squared_positive"],
        replay_diagnostics["point_count"],
    )
    active_band = next(row for row in band_rows if row["band"] == "active_total")
    add(
        "collective_law_beats_spherical_EOS_proximity",
        float(active_band["collective_Q_median"])
        < float(active_band["spherical_EOS_Q_median"]),
        (
            active_band["collective_Q_median"],
            active_band["spherical_EOS_Q_median"],
        ),
    )
    add(
        "collective_active_median_near_unity",
        1.0 <= float(active_band["collective_Q_median"]) <= 1.5,
        active_band["collective_Q_median"],
    )
    add(
        "spherical_EOS_is_too_stiff",
        float(active_band["spherical_EOS_Q_median"]) > 2.0
        and float(active_band["spherical_EOS_over_collective_cR2_median"]) > 3.0,
        (
            active_band["spherical_EOS_Q_median"],
            active_band["spherical_EOS_over_collective_cR2_median"],
        ),
    )
    add(
        "countercases_explicit_not_erased",
        replay_diagnostics["active_unstable_point_count"] > 0
        and len(replay_diagnostics["active_unstable_galaxies"]) > 0
        and any(
            int(row["active_unstable_point_count"]) > 0 for row in case_rows
        ),
        (
            replay_diagnostics["active_unstable_point_count"],
            replay_diagnostics["active_unstable_galaxies"],
        ),
    )
    add(
        "environmental_enhancement_correlation",
        replay_diagnostics[
            "active_phase_fraction_log_enhancement_correlation"
        ]
        > 0.7,
        replay_diagnostics[
            "active_phase_fraction_log_enhancement_correlation"
        ],
    )
    add(
        "fractional_bare_vertex_mismatch",
        abs(vertex_diagnostics["fractional_parent_shape_invariant"] - 0.4)
        < 1.0e-15
        and abs(vertex_diagnostics["logistic_shape_invariant"] - 3.0)
        < 1.0e-15
        and abs(vertex_diagnostics["invariant_ratio"] - 7.5) < 1.0e-15,
        vertex_diagnostics,
    )
    add(
        "all_claim_flags_false",
        all(
            row.get("valid_for_local_GR_claim") is False
            and row.get("valid_for_galaxy_claim") is False
            and row.get("valid_for_full_MTS_claim") is False
            for rows in all_output_rows
            for row in rows
        ),
        "no checkpoint-5198 row is claim-valid",
    )
    add(
        "document_present_and_marked",
        DOCUMENT.exists() and MARKER in DOCUMENT.read_text(encoding="utf-8"),
        DOCUMENT,
    )
    add(
        "script_compiles_without_bytecode",
        bool(compile(SCRIPT.read_text(encoding="utf-8"), str(SCRIPT), "exec")),
        SCRIPT,
    )
    add(
        "all_output_files_exist_nonempty",
        all(path.exists() and path.stat().st_size > 0 for path in output_files),
        len(output_files),
    )
    add(
        "all_csv_outputs_parse",
        all(
            bool(read_csv(path))
            for path in output_files
            if path.suffix.lower() == ".csv"
        ),
        "all generated CSV files contain rows",
    )
    add(
        "formalization_workbench_lock",
        tree_digest(FORMAL) == FORMAL_LOCK,
        tree_digest(FORMAL),
    )
    add(
        "checkpoint_5197_output_lock",
        tree_digest(CHECKPOINT_5197_OUT) == CHECKPOINT_5197_OUT_LOCK,
        tree_digest(CHECKPOINT_5197_OUT),
    )
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


def build_payload(
    derivations: list[dict[str, Any]],
    universal_profile: list[dict[str, Any]],
    scale_bridge: list[dict[str, Any]],
    q_sweep: list[dict[str, Any]],
    case_rows: list[dict[str, Any]],
    band_rows: list[dict[str, Any]],
    stress_rows: list[dict[str, Any]],
    vertex_rows: list[dict[str, Any]],
    route_rows: list[dict[str, Any]],
    provenance: list[dict[str, Any]],
    scale_diagnostics: dict[str, Any],
    profile_diagnostics: dict[str, Any],
    replay_diagnostics: dict[str, Any],
    vertex_diagnostics: dict[str, Any],
) -> dict[str, Any]:
    return {
        "checkpoint": 5198,
        "marker": MARKER,
        "claim_status": {
            "metric_dressed_collective_Hessian": "DERIVED_CONDITIONALLY_ON_CONSERVED_PHASE_SURFACE_STRESS",
            "marginal_Mestel_radial_amplitude": "DERIVED_ASYMPTOTICALLY",
            "spectral_collective_scale_bridge": "CONDITIONAL_INTERNAL_CLOSURE",
            "direct_spherical_EOS_radial_map": "REJECTED",
            "direct_bare_fractional_logistic_map": "REJECTED",
            "composite_2PI_logistic_vertices": "OPEN",
            "local_GR_Newton_Maxwell_branch": "UNCHANGED",
            "galaxy_claim": False,
            "local_GR_claim": False,
            "full_MTS_claim": False,
        },
        "theorem": (
            "A conserved occupied MTS phase surface stress has a universal "
            "metric-dressed WKB Hessian. Its outer finite-Mestel limit fixes "
            "c_R^2=Gamma0 L_eff/8. With the already selected Plummer thickness, "
            "the soft wavenumber at R=L_eff matches the independently constructed "
            "checkpoint-5148 spectral-to-real scale map internally. The route "
            "is locally silent because the collective coordinate is absent when "
            "the state is absent. The quadratic carrier and radial amplitude "
            "therefore survive, but the exact logistic flow still requires "
            "composite 2PI nonlinear vertices; the bare fractional one-field "
            "potential cannot supply their canonical vertex ratios."
        ),
        "scale_diagnostics": scale_diagnostics,
        "universal_profile_diagnostics": profile_diagnostics,
        "clean_replay_diagnostics": replay_diagnostics,
        "vertex_diagnostics": vertex_diagnostics,
        "collective_Hessian_derivation": derivations,
        "universal_phase_soft_mode_profile": universal_profile,
        "spectral_collective_scale_bridge": scale_bridge,
        "q_scale_self_consistency_sweep": q_sweep,
        "clean_galaxy_collective_case_summary": case_rows,
        "radial_band_collective_summary": band_rows,
        "stress_selection": stress_rows,
        "logistic_vertex_contract": vertex_rows,
        "route_decision": route_rows,
        "source_provenance": provenance,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="derive and print the checkpoint decision without writing files",
    )
    arguments = parser.parse_args()

    galaxy_before = git_state(GALAXY_REPO)
    galaxy_lab = load_galaxy_lab()
    derivations = derivation_rows()
    universal_profile, profile_diagnostics = universal_profile_rows()
    scale_bridge, q_sweep, scale_diagnostics = scale_bridge_rows()
    case_rows, band_rows, point_rows, replay_diagnostics = clean_galaxy_replay(
        galaxy_lab
    )
    stress_rows = stress_selection_rows(band_rows, replay_diagnostics)
    vertex_rows, vertex_diagnostics = logistic_vertex_rows()
    route_rows = route_decision_rows(
        scale_diagnostics,
        profile_diagnostics,
        replay_diagnostics,
    )
    provenance = source_provenance_rows()
    payload = build_payload(
        derivations,
        universal_profile,
        scale_bridge,
        q_sweep,
        case_rows,
        band_rows,
        stress_rows,
        vertex_rows,
        route_rows,
        provenance,
        scale_diagnostics,
        profile_diagnostics,
        replay_diagnostics,
        vertex_diagnostics,
    )

    if arguments.dry_run:
        print(
            json.dumps(
                {
                    "marker": MARKER,
                    "scale_diagnostics": scale_diagnostics,
                    "universal_profile_diagnostics": profile_diagnostics,
                    "clean_replay_diagnostics": replay_diagnostics,
                    "vertex_diagnostics": vertex_diagnostics,
                    "route_decision": route_rows,
                },
                indent=2,
                default=str,
            )
        )
        return

    OUT.mkdir(parents=True, exist_ok=True)
    output_map = {
        "collective_Hessian_derivation.csv": derivations,
        "universal_phase_soft_mode_profile.csv": universal_profile,
        "spectral_collective_scale_bridge.csv": scale_bridge,
        "q_scale_self_consistency_sweep.csv": q_sweep,
        "clean_galaxy_collective_case_summary.csv": case_rows,
        "radial_band_collective_summary.csv": band_rows,
        "spherical_EOS_rejection_and_radial_stress_selection.csv": stress_rows,
        "logistic_composite_vertex_contract.csv": vertex_rows,
        "route_decision.csv": route_rows,
        "source_provenance.csv": provenance,
    }
    for name, rows in output_map.items():
        write_csv(OUT / name, rows)
    result_path = OUT / "marginal_Mestel_collective_results.json"
    result_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True, default=str) + "\n",
        encoding="utf-8",
    )
    output_files = [OUT / name for name in output_map] + [result_path]
    all_output_rows = list(output_map.values())
    validations = validation_rows(
        galaxy_before,
        output_files,
        scale_diagnostics,
        profile_diagnostics,
        replay_diagnostics,
        vertex_diagnostics,
        case_rows,
        band_rows,
        all_output_rows,
        galaxy_lab,
    )
    write_csv(VALIDATION, validations)
    failed = [row for row in validations if row["status"] != "PASS"]
    if failed:
        raise RuntimeError(
            "checkpoint 5198 validation failed: "
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
                "checkpoint_5197_output_sha256": tree_digest(
                    CHECKPOINT_5197_OUT
                ),
                "locked_spectral_mu_L": scale_diagnostics[
                    "locked_spectral_scale"
                ],
                "Plummer_collective_kstar_L": scale_diagnostics[
                    "locked_Plummer_wavenumber"
                ],
                "relative_scale_residual": scale_diagnostics[
                    "locked_relative_residual"
                ],
                "self_consistent_q": scale_diagnostics[
                    "self_consistent_q"
                ],
                "active_case_median_Q": replay_diagnostics[
                    "active_case_collective_Q"
                ]["median"],
                "active_case_median_spherical_EOS_Q": replay_diagnostics[
                    "active_case_spherical_EOS_Q"
                ]["median"],
                "active_unstable_galaxies": replay_diagnostics[
                    "active_unstable_galaxies"
                ],
                "selected_next_route": (
                    "CALCULATE_COMPOSITE_2PI_NONLINEAR_VERTICES"
                ),
            },
            indent=2,
            default=str,
        )
    )


if __name__ == "__main__":
    main()
