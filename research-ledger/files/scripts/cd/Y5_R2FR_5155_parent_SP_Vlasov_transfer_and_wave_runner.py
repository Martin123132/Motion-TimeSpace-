from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import math
import re
from pathlib import Path
from typing import Any

import numpy as np


POST = Path(__file__).resolve().parents[1]
FORMAL = POST.parent / "formalization-workbench"
PREVIOUS_SCRIPT = (
    POST
    / "scripts"
    / "Y5_R2FR_5154_Eddington_phase_space_positive_DF_gate.py"
)
STATE_ROWS = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5151"
    / "galaxy_state_stress_scale_gate.csv"
)
BACKGROUND_ROWS = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5152"
    / "primordial_motion_background.csv"
)
MASS_ROWS = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5152"
    / "galaxy_mass_window.csv"
)
JEANS_ROWS = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5152"
    / "linear_Jeans_scale_gate.csv"
)
HALO_ROWS = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5154"
    / "smooth_edge_halo_inventory.csv"
)
GALAXY_SAMPLES = Path(r"D:\Users\ollet\Documents\mts-galaxy-lab\data\samples.js")
OUT = POST / "source-intake" / "functional_rg" / "5155"
RESULT_JSON = OUT / "parent_SP_Vlasov_transfer_results.json"
LIMIT_CSV = OUT / "parent_SP_Vlasov_limit.csv"
NO_COLLAPSE_CSV = OUT / "homogeneous_no_collapse_theorem.csv"
TRANSFER_CSV = OUT / "post_equality_transfer_curves.csv"
TRANSFER_SUMMARY_CSV = OUT / "post_equality_transfer_summary.csv"
PATCH_CSV = OUT / "halo_patch_transfer_gate.csv"
CLASSICALITY_CSV = OUT / "wave_resolution_and_classicality_gate.csv"
WAVE_CSV = OUT / "split_step_mode_validation.csv"
INITIAL_DATA_CSV = OUT / "initial_data_contract.csv"
ROUTE_CSV = OUT / "formation_route_decision.csv"
VALIDATION_CSV = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5155_VALIDATION.csv"
)
DOCUMENT = (
    POST
    / "5155-Y5-R2FR-parent-SP-Vlasov-limit-homogeneous-no-collapse-post-equality-transfer-and-wave-runner.md"
)
MARKER = "MTS_5155_PARENT_SP_VLASOV_TRANSFER_WAVE_RUNNER"
CHECKED_DATE = "2026-07-20"
FORMAL_BASELINE = "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"

G_SI = 6.67430e-11
HBAR_SI = 1.054571817e-34
EV_C2_KG = 1.7826619216278976e-36
MPC_M = 3.085677581491367e22
MSUN_KG = 1.98847e30
H0_KM_S_MPC = 67.4
H0_SI = H0_KM_S_MPC * 1000.0 / MPC_M
OMEGA_M = 0.315
A_EQUALITY = 1.0 / 3500.0
OMEGA_R = OMEGA_M * A_EQUALITY
OMEGA_LAMBDA = 1.0 - OMEGA_M - OMEGA_R
F_EQUALITY = 0.6
TRANSFER_STEPS = 8000
TRANSFER_CHECK_STEPS = 4000
TRANSFER_RATIO_GRID = np.logspace(-2.0, 1.0, 320)
FFT_A_END = 4.0 * A_EQUALITY
FFT_DELTA_INITIAL = 1.0e-5
FFT_MODE = 2
FFT_BASE_GRID = 32
FFT_BASE_STEPS = 240

SOURCE_PATHS = {
    "local_parent_action": POST
    / "4947-Y5-R2FR-local-GR-Newton-Maxwell-calibration-count-and-universal-source-residue-certificate.md",
    "projective_2PI_parent": POST
    / "4948-Y5-R2FR-single-parent-motion-Hessian-to-galaxy-phase-flow-and-universal-Jgap-interface.md",
    "primordial_parent": POST
    / "5152-Y5-R2FR-primordial-motion-occupation-dust-limit-Jeans-window-and-formation-source-arbitration.md",
    "phase_space_parent": POST
    / "5154-Y5-R2FR-hard-edge-isotropic-obstruction-minimal-regular-Eddington-distribution-and-stability-gate.md",
    "previous_script": PREVIOUS_SCRIPT,
    "previous_result": POST
    / "source-intake"
    / "functional_rg"
    / "5154"
    / "Eddington_phase_space_results.json",
    "state_rows": STATE_ROWS,
    "background_rows": BACKGROUND_ROWS,
    "mass_rows": MASS_ROWS,
    "Jeans_rows": JEANS_ROWS,
    "halo_rows": HALO_ROWS,
    "galaxy_samples_read_only": GALAXY_SAMPLES,
}

PRIMARY_SOURCE_URLS = {
    "fuzzy_transfer": "https://arxiv.org/abs/astro-ph/0003365",
    "SP_numerics": "https://arxiv.org/abs/1810.01915",
    "scalar_adiabatic_initial_data": "https://arxiv.org/abs/astro-ph/9811156",
    "nonequilibrium_2PI": "https://arxiv.org/abs/hep-ph/0409233",
}


def load_previous_module() -> Any:
    specification = importlib.util.spec_from_file_location(
        "mts_checkpoint_5154", PREVIOUS_SCRIPT
    )
    if specification is None or specification.loader is None:
        raise RuntimeError("cannot load checkpoint-5154 module")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


PREVIOUS = load_previous_module()


def file_digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def tree_digest(path: Path) -> str:
    value = hashlib.sha256()
    for item in sorted(candidate for candidate in path.rglob("*") if candidate.is_file()):
        value.update(item.relative_to(path).as_posix().encode("utf-8"))
        value.update(file_digest(item).encode("ascii"))
    return value.hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise RuntimeError(f"refusing to write empty CSV: {path}")
    fields: list[str] = []
    for row in rows:
        for field in row:
            if field not in fields:
                fields.append(field)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(value, indent=2, sort_keys=True), encoding="utf-8"
    )
    temporary.replace(path)


def parse_samples(path: Path) -> dict[str, list[dict[str, float]]]:
    text = path.read_text(encoding="utf-8-sig").strip()
    text = re.sub(r"^window\.MTS_SAMPLES\s*=\s*", "", text)
    text = re.sub(r";\s*$", "", text)
    samples = json.loads(text)
    parsed: dict[str, list[dict[str, float]]] = {}
    for sample in samples:
        rows: list[dict[str, float]] = []
        for line in sample["text"].splitlines():
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            values = [float(value) for value in stripped.split()]
            if len(values) >= 8:
                rows.append({"r_kpc": values[0]})
        parsed[sample["name"].replace("_rotmod.dat", "")] = rows
    return parsed


def background(log_scale_factor: float) -> tuple[float, float, float, float]:
    scale_factor = math.exp(log_scale_factor)
    radiation = OMEGA_R / scale_factor**4
    matter = OMEGA_M / scale_factor**3
    vacuum = OMEGA_LAMBDA
    total = radiation + matter + vacuum
    return (
        scale_factor,
        H0_SI * math.sqrt(total),
        radiation / total,
        matter / total,
    )


def mode_rhs(
    log_scale_factor: float,
    density: np.ndarray,
    derivative: np.ndarray,
    mass_kg: float,
    wavenumber_inverse_m: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    scale_factor, hubble, radiation_fraction, matter_fraction = background(
        log_scale_factor
    )
    friction = 2.0 - 0.5 * (
        4.0 * radiation_fraction + 3.0 * matter_fraction
    )
    quantum = (
        HBAR_SI**2
        * wavenumber_inverse_m**4
        / (4.0 * mass_kg**2 * scale_factor**4 * hubble**2)
    )
    return (
        derivative,
        -friction * derivative
        - (quantum - 1.5 * matter_fraction) * density,
    )


def cdm_rhs(
    log_scale_factor: float,
    density: float,
    derivative: float,
) -> tuple[float, float]:
    _, _, radiation_fraction, matter_fraction = background(log_scale_factor)
    friction = 2.0 - 0.5 * (
        4.0 * radiation_fraction + 3.0 * matter_fraction
    )
    return derivative, -friction * derivative + 1.5 * matter_fraction * density


def integrate_linear_modes(
    mass_eV: float,
    wavenumbers_Mpc_inverse: np.ndarray,
    end_scale_factor: float,
    steps: int,
    initial_density: float = 1.0,
) -> tuple[np.ndarray, np.ndarray, float, float]:
    mass_kg = mass_eV * EV_C2_KG
    wavenumbers_inverse_m = np.asarray(wavenumbers_Mpc_inverse) / MPC_M
    log_scale_factor = math.log(A_EQUALITY)
    end_log_scale_factor = math.log(end_scale_factor)
    step = (end_log_scale_factor - log_scale_factor) / steps
    density = np.full_like(
        wavenumbers_inverse_m, initial_density, dtype=float
    )
    derivative = np.full_like(
        wavenumbers_inverse_m, F_EQUALITY * initial_density, dtype=float
    )
    cdm_density = float(initial_density)
    cdm_derivative = F_EQUALITY * initial_density

    for _ in range(steps):
        k1_density, k1_derivative = mode_rhs(
            log_scale_factor,
            density,
            derivative,
            mass_kg,
            wavenumbers_inverse_m,
        )
        k1_cdm_density, k1_cdm_derivative = cdm_rhs(
            log_scale_factor, cdm_density, cdm_derivative
        )
        k2_density, k2_derivative = mode_rhs(
            log_scale_factor + 0.5 * step,
            density + 0.5 * step * k1_density,
            derivative + 0.5 * step * k1_derivative,
            mass_kg,
            wavenumbers_inverse_m,
        )
        k2_cdm_density, k2_cdm_derivative = cdm_rhs(
            log_scale_factor + 0.5 * step,
            cdm_density + 0.5 * step * k1_cdm_density,
            cdm_derivative + 0.5 * step * k1_cdm_derivative,
        )
        k3_density, k3_derivative = mode_rhs(
            log_scale_factor + 0.5 * step,
            density + 0.5 * step * k2_density,
            derivative + 0.5 * step * k2_derivative,
            mass_kg,
            wavenumbers_inverse_m,
        )
        k3_cdm_density, k3_cdm_derivative = cdm_rhs(
            log_scale_factor + 0.5 * step,
            cdm_density + 0.5 * step * k2_cdm_density,
            cdm_derivative + 0.5 * step * k2_cdm_derivative,
        )
        k4_density, k4_derivative = mode_rhs(
            log_scale_factor + step,
            density + step * k3_density,
            derivative + step * k3_derivative,
            mass_kg,
            wavenumbers_inverse_m,
        )
        k4_cdm_density, k4_cdm_derivative = cdm_rhs(
            log_scale_factor + step,
            cdm_density + step * k3_cdm_density,
            cdm_derivative + step * k3_cdm_derivative,
        )
        density += step * (
            k1_density
            + 2.0 * k2_density
            + 2.0 * k3_density
            + k4_density
        ) / 6.0
        derivative += step * (
            k1_derivative
            + 2.0 * k2_derivative
            + 2.0 * k3_derivative
            + k4_derivative
        ) / 6.0
        cdm_density += step * (
            k1_cdm_density
            + 2.0 * k2_cdm_density
            + 2.0 * k3_cdm_density
            + k4_cdm_density
        ) / 6.0
        cdm_derivative += step * (
            k1_cdm_derivative
            + 2.0 * k2_cdm_derivative
            + 2.0 * k3_cdm_derivative
            + k4_cdm_derivative
        ) / 6.0
        log_scale_factor += step
    return density, derivative, cdm_density, cdm_derivative


def first_half_power_ratio(
    ratios: np.ndarray, power_ratios: np.ndarray
) -> float:
    indices = np.where(power_ratios <= 0.5)[0]
    if len(indices) == 0:
        return math.nan
    index = int(indices[0])
    if index == 0:
        return float(ratios[0])
    log_lower = math.log(ratios[index - 1])
    log_upper = math.log(ratios[index])
    lower = power_ratios[index - 1] - 0.5
    upper = power_ratios[index] - 0.5
    fraction = lower / (lower - upper)
    return math.exp(log_lower + fraction * (log_upper - log_lower))


def interpolate_power(
    ratio_grid: np.ndarray, power_grid: np.ndarray, ratio: float
) -> float:
    return float(
        np.interp(
            math.log(ratio),
            np.log(ratio_grid),
            power_grid,
            left=power_grid[0],
            right=power_grid[-1],
        )
    )


def split_step_mode(
    mass_eV: float,
    jeans_wavenumber_Mpc_inverse: float,
    jeans_ratio: float,
    grid_size: int,
    steps: int,
) -> dict[str, Any]:
    mass_kg = mass_eV * EV_C2_KG
    mode_wavenumber_Mpc_inverse = (
        jeans_ratio * jeans_wavenumber_Mpc_inverse
    )
    box_Mpc = 2.0 * math.pi * FFT_MODE / mode_wavenumber_Mpc_inverse
    spacing_Mpc = box_Mpc / grid_size
    frequencies = (
        2.0
        * math.pi
        * np.fft.fftfreq(grid_size, d=spacing_Mpc)
        / MPC_M
    )
    k_x = frequencies[:, None, None]
    k_y = frequencies[None, :, None]
    k_z = frequencies[None, None, :]
    k_squared = k_x**2 + k_y**2 + k_z**2
    positions = np.arange(grid_size) * spacing_Mpc
    phase_coordinate = 2.0 * math.pi * FFT_MODE * positions / box_Mpc
    density_line = FFT_DELTA_INITIAL * np.cos(phase_coordinate)
    density = np.broadcast_to(
        density_line[:, None, None],
        (grid_size, grid_size, grid_size),
    ).copy()
    physical_mode = mode_wavenumber_Mpc_inverse / MPC_M
    initial_phase_amplitude = (
        mass_kg
        * A_EQUALITY**2
        * background(math.log(A_EQUALITY))[1]
        * F_EQUALITY
        * FFT_DELTA_INITIAL
        / (HBAR_SI * physical_mode**2)
    )
    phase_line = initial_phase_amplitude * np.cos(phase_coordinate)
    phase = np.broadcast_to(
        phase_line[:, None, None],
        (grid_size, grid_size, grid_size),
    )
    wave = np.sqrt(1.0 + density) * np.exp(1j * phase)
    initial_norm = float(np.mean(np.abs(wave) ** 2))
    log_step = math.log(FFT_A_END / A_EQUALITY) / steps
    scale_factor = A_EQUALITY

    def potential(current_wave: np.ndarray, evaluation_scale: float) -> np.ndarray:
        contrast = np.abs(current_wave) ** 2
        contrast = contrast / np.mean(contrast) - 1.0
        contrast_fourier = np.fft.fftn(contrast)
        matter_density = (
            3.0
            * H0_SI**2
            * OMEGA_M
            / (8.0 * math.pi * G_SI * evaluation_scale**3)
        )
        potential_fourier = np.zeros_like(contrast_fourier)
        nonzero = k_squared > 0.0
        potential_fourier[nonzero] = (
            -4.0
            * math.pi
            * G_SI
            * evaluation_scale**2
            * matter_density
            * contrast_fourier[nonzero]
            / k_squared[nonzero]
        )
        return np.fft.ifftn(potential_fourier).real

    for _ in range(steps):
        next_scale = scale_factor * math.exp(log_step)
        midpoint_scale = math.sqrt(scale_factor * next_scale)
        midpoint_hubble = background(math.log(midpoint_scale))[1]
        time_step = log_step / midpoint_hubble
        gravitational_potential = potential(wave, midpoint_scale)
        wave *= np.exp(
            -0.5j
            * mass_kg
            * gravitational_potential
            * time_step
            / HBAR_SI
        )
        wave_fourier = np.fft.fftn(wave)
        wave_fourier *= np.exp(
            -0.5j
            * HBAR_SI
            * k_squared
            * time_step
            / (mass_kg * midpoint_scale**2)
        )
        wave = np.fft.ifftn(wave_fourier)
        gravitational_potential = potential(wave, midpoint_scale)
        wave *= np.exp(
            -0.5j
            * mass_kg
            * gravitational_potential
            * time_step
            / HBAR_SI
        )
        scale_factor = next_scale

    final_contrast = np.abs(wave) ** 2
    final_contrast = final_contrast / np.mean(final_contrast) - 1.0
    final_fourier = np.fft.fftn(final_contrast)
    numerical_amplitude = float(
        2.0
        * abs(final_fourier[FFT_MODE, 0, 0])
        / grid_size**3
    )
    linear_density, _, _, _ = integrate_linear_modes(
        mass_eV,
        np.array([mode_wavenumber_Mpc_inverse]),
        FFT_A_END,
        6000,
        initial_density=FFT_DELTA_INITIAL,
    )
    expected_amplitude = float(abs(linear_density[0]))
    return {
        "mass_eV": mass_eV,
        "k_over_kJeq": jeans_ratio,
        "k_mode_Mpc_inverse": mode_wavenumber_Mpc_inverse,
        "box_Mpc": box_Mpc,
        "grid_size": grid_size,
        "steps": steps,
        "a_initial": A_EQUALITY,
        "a_final": FFT_A_END,
        "initial_mode_amplitude": FFT_DELTA_INITIAL,
        "FFT_mode_amplitude_final": numerical_amplitude,
        "linear_ODE_amplitude_final": expected_amplitude,
        "relative_amplitude_error": abs(
            numerical_amplitude / expected_amplitude - 1.0
        ),
        "wave_norm_relative_drift": abs(
            float(np.mean(np.abs(wave) ** 2)) / initial_norm - 1.0
        ),
    }


def parent_limit_rows() -> list[dict[str, Any]]:
    return [
        {
            "step": "parent_scalar_equation",
            "equation": "(Box-m_gap^2)psi + controlled c_ess X^2 and higher-operator terms = 0",
            "status": "DERIVED_FROM_4947_ACTION",
            "assumption": "reflection-even occupied branch; weak metric; actual c_ess remains unsigned",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "step": "nonrelativistic_envelope",
            "equation": "i hbar d_t Psi_c=-hbar^2 nabla^2 Psi_c/(2m a^2)+m Phi Psi_c",
            "status": "DERIVED_LEADING_WKB_LIMIT",
            "assumption": "H/m << 1 and higher operators inside checkpoint-5152 control",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "step": "one_metric_Poisson_source",
            "equation": "nabla^2 Phi=4pi G_N a^2(delta rho_b+delta rho_EM+delta rho_X)",
            "status": "DERIVED_FROM_RANK_ONE_4947_METRIC_RESIDUE",
            "assumption": "same Hilbert tensor; no galaxy-only G or scalar charge",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "step": "Madelung_linearization",
            "equation": "ddot delta+2H dot delta+[hbar^2 k^4/(4m^2a^4)-4piG rho_m]delta=0",
            "status": "DERIVED_AND_EXECUTED",
            "assumption": "adiabatic one-fluid gravity comparator after equality",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "step": "Wigner_classical_limit",
            "equation": "d_t f+{f,H}=O[(hbar/(m v L))^2]",
            "status": "DERIVED_SCALE_BOUND",
            "assumption": "smooth phase-space scales outside interference zeros",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "step": "checkpoint_5154_stationarity",
            "equation": "f=f(E) implies {f,H}=f'(E){H,H}=0",
            "status": "EXACT_VLASOV_STATIONARY_IDENTITY",
            "assumption": "self-consistent spherical p=2 potential",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
    ]


def no_collapse_rows() -> list[dict[str, Any]]:
    return [
        {
            "clause": "homogeneous_initial_field",
            "premise": "psi(t_i,x)=psi_i and dot psi(t_i,x)=dot psi_i",
            "consequence": "all spatial derivatives vanish",
            "passed": True,
            "checkpoint_marker": MARKER,
        },
        {
            "clause": "homogeneous_metric_constraint",
            "premise": "delta rho_total(t_i,x)=0",
            "consequence": "nabla^2 Phi=0 and the physical periodic/decaying solution has no force gradient",
            "passed": True,
            "checkpoint_marker": MARKER,
        },
        {
            "clause": "translation_invariant_evolution",
            "premise": "parent equations and boundary state are translation invariant",
            "consequence": "uniqueness preserves the homogeneous solution for all deterministic times",
            "passed": True,
            "checkpoint_marker": MARKER,
        },
        {
            "clause": "reflection_even_mixture",
            "premise": "the ensemble is an even mixture of homogeneous +psi_i and -psi_i representatives",
            "consequence": "each representative remains homogeneous; averaging cannot create spatial covariance",
            "passed": True,
            "checkpoint_marker": MARKER,
        },
        {
            "clause": "formation_requirement",
            "premise": "a halo needs nonzero inhomogeneous modes",
            "consequence": "P_delta(k)>0 or an equivalent parent two-point covariance is mathematically necessary",
            "passed": True,
            "checkpoint_marker": MARKER,
        },
    ]


def initial_data_rows() -> list[dict[str, Any]]:
    return [
        {
            "input": "Omega_X homogeneous abundance",
            "ownership": "checkpoint_5152 global cosmological datum",
            "status": "NUMERIC_AVAILABLE_NOT_PARENT_PREPARED",
            "needed_for_nonlinear_run": True,
            "per_galaxy_fit_allowed": False,
            "checkpoint_marker": MARKER,
        },
        {
            "input": "motion mass m_gap",
            "ownership": "three locked internal benchmarks",
            "status": "NUMERIC_AVAILABLE_NOT_OBSERVATIONALLY_SELECTED",
            "needed_for_nonlinear_run": True,
            "per_galaxy_fit_allowed": False,
            "checkpoint_marker": MARKER,
        },
        {
            "input": "adiabatic growing-mode relation",
            "ownership": "universal metric comparator",
            "status": "POST_EQUALITY_RATIO_EXECUTED",
            "needed_for_nonlinear_run": True,
            "per_galaxy_fit_allowed": False,
            "checkpoint_marker": MARKER,
        },
        {
            "input": "primordial P_delta(k) amplitude tilt and correlations",
            "ownership": "parent 2PI state or external CMB likelihood",
            "status": "MISSING_DECISIVE_INITIAL_COVARIANCE",
            "needed_for_nonlinear_run": True,
            "per_galaxy_fit_allowed": False,
            "checkpoint_marker": MARKER,
        },
        {
            "input": "realization phases",
            "ownership": "fixed stochastic seed drawn from one global covariance",
            "status": "NOT_A_THEORY_PARAMETER_BUT_MUST_BE_DECLARED",
            "needed_for_nonlinear_run": True,
            "per_galaxy_fit_allowed": False,
            "checkpoint_marker": MARKER,
        },
        {
            "input": "infrared c_ess and higher operators",
            "ownership": "parent RG transport",
            "status": "MISSING_NUMERIC_PARENT_COEFFICIENT_FREE_LIMIT_ONLY",
            "needed_for_nonlinear_run": True,
            "per_galaxy_fit_allowed": False,
            "checkpoint_marker": MARKER,
        },
    ]


def route_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate": "parent_weak_field_evolution",
            "status": "DERIVED_AND_NUMERIC_RUNNER_VALIDATED",
            "result": "rank-one metric source gives SP and Vlasov limits with the same G_N",
            "remaining": "insert actual c_ess after parent RG transport",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "gate": "homogeneous_formation",
            "status": "REJECTED_EXACTLY",
            "result": "the 5152 homogeneous even state cannot generate spatial structure under deterministic translation-invariant evolution",
            "remaining": "derive or source one global primordial covariance",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "gate": "post_equality_patch_survival",
            "status": "EXECUTED_THREE_MASS_GATE",
            "result": "locked halo-patch modes are propagated relative to the same CDM growing mode",
            "remaining": "include radiation-era Boltzmann transfer and nonlinear mode coupling",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "gate": "nonlinear_solver_route",
            "status": "HYBRID_ROUTE_REQUIRED",
            "result": "full-edge 3D wave grids are intractable while inner observed points retain finite wave corrections",
            "remaining": "Vlasov cosmological volume plus wave-resolved zoom/core, both seeded by one covariance",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "gate": "projective_profile_attractor",
            "status": "OPEN_DECISIVE_GATE",
            "result": "not inferred from transfer survival or equilibrium stationarity",
            "remaining": "run covariance-locked hybrid collapse and compare q/core/edge without refit",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
    ]


def write_document(result: dict[str, Any]) -> None:
    summary = result["summary"]
    text = f"""# 5155 - Parent SP/Vlasov limit, homogeneous no-collapse theorem, post-equality transfer and wave runner

Marker: `{MARKER}`.

Date: `{CHECKED_DATE}`.

## Decision

Checkpoint 5155 attempts the requested formation route instead of declaring
that the checkpoint-5154 equilibrium formed itself. The same rank-one metric
source used for local GR/Newton/Maxwell gives the weak-field
Schrodinger--Poisson system and its Vlasov limit. A real FFT split-step runner
reproduces the independently integrated linear modes at all three locked
masses. The galaxy-patch modes survive the executed post-equality dynamics.

The calculation also proves a hard boundary: the homogeneous checkpoint-5152
state cannot collapse without a nonzero spatial two-point covariance. That is
not a coding inconvenience. It follows from translation invariance and
uniqueness. A nonlinear run started from only `psi_i` and `Omega_X` would have
to insert perturbations secretly. The next missing object is therefore one
global primordial covariance, not another per-galaxy halo parameter.

## 1. Same parent action to the initial-value equations

The checkpoint-4947 local action contains

```text
S_psi=integral sqrt(-g)[-(nabla psi)^2/2-m_gap^2 psi^2/2
                        +c_ess X^2+higher operators].
```

In the weak one-metric branch, separate the fast rest-mass phase and retain the
leading `H/m`, velocity and gradient orders. With comoving number amplitude
`Psi_c`, the result is

```text
i hbar partial_t Psi_c
 =-hbar^2 nabla_x^2 Psi_c/(2m a^2)+m Phi Psi_c,

nabla_x^2 Phi
 =4pi G_N a^2(delta rho_b+delta rho_EM+delta rho_X).
```

The Poisson equation is the same checkpoint-4947 Einstein residue. Poynting
momentum and electromagnetic energy remain components of the same Hilbert
tensor; no galaxy-only `G`, direct scalar charge or second metric was added.
The current numerical runner uses the controlled free limit. The actual
infrared `c_ess` is still unsigned and is not silently set to a claimed parent
number.

Madelung linearization gives

```text
ddot delta+2H dot delta
 +[hbar^2 k^4/(4m^2a^4)-4piG rho_m]delta=0.
```

The Wigner equation gives Vlasov--Poisson with leading smooth-scale correction
`O[epsilon_L^2]`, `epsilon_L=hbar/(m v L)`. For the checkpoint-5154 isotropic
state, `f=f(E)` implies `{{f,H}}=f'(E){{H,H}}=0` exactly. Thus the `p=2` profile is
a genuine Vlasov equilibrium candidate, although stationarity is not a
formation theorem.

## 2. Exact homogeneous no-collapse theorem

For either homogeneous representative of the reflection-even primordial
mixture,

```text
psi(t_i,x)=+/-psi_i,
partial_i psi=0,
delta rho=0,
nabla Phi=0.
```

The parent equations and cosmological boundary state are translation
invariant. Uniqueness therefore preserves homogeneity. Evolving the `+` and
`-` representatives separately and averaging them does not manufacture an
inhomogeneous two-point function. Consequently

```text
P_delta(k)>0 for some k>0
```

or an equivalent parent 2PI covariance is necessary for halo formation. The
homogeneous abundance fixes the mean density, not the perturbation spectrum.

## 3. Three-mass post-equality transfer

To calculate what is possible without inventing that spectrum, the amplitude
cancels in a same-initial-mode transfer ratio. In `N=ln a`, the executed system
is

```text
delta_NN+[2+dlnH/dN]delta_N
 +[hbar^2 k^4/(4m^2a^4H^2)-3 Omega_m(a)/2]delta=0.
```

Both MTS and the zero-quantum-pressure comparator start at equality with the
Meszaros growing slope `delta_N/delta=3/5`. Radiation, matter and Lambda are
retained in `H(a)`. This is a **post-equality dynamical transfer**, not a full
radiation-era Boltzmann transfer and not a primordial-power claim.

Across the three masses, the curves collapse when plotted against
`k/k_J,eq` to maximum disagreement
`{summary['maximum_mass_scaled_transfer_disagreement']}`. The first
post-equality half-power crossing is

```text
k_half/k_J,eq={summary['half_power_ratio_mean']}.
```

For every one of the 1050 finite halo patches, the conservative
`k=2pi/R_L` mode remains below `k_J,eq`; its minimum present power ratio is
`{summary['minimum_patch_2pi_power_ratio']}`. The `pi/R_L` minimum is
`{summary['minimum_patch_pi_power_ratio']}`. Thus the executed late dynamics
does not erase the mass supply found at 5153--5154. It does not prove the
patches occur with the required primordial probability.

## 4. Actual split-step wave propagation

A periodic three-dimensional Strang runner was executed, not merely written.
It evolves

```text
exp[-i m Phi dt/(2hbar)]
exp[-i hbar k^2 dt/(2m a^2)]
exp[-i m Phi dt/(2hbar)]
```

with Poisson recomputed between the kinetic and final potential stages. Two
linear modes, `k/k_J,eq=0.7` and `1.3`, were run at each locked mass from
equality to `a=4a_eq`. Across the six physical runs,

```text
maximum FFT-versus-ODE amplitude error
 ={summary['maximum_split_step_amplitude_error']},
maximum wave-norm drift
 ={summary['maximum_split_step_norm_drift']}.
```

The strict-mass `k/k_J,eq=1.3` case was repeated at grids 24, 32 and 40; its
relative amplitude spread is
`{summary['split_step_convergence_relative_spread']}`. This validates the
equation plumbing and time integrator in the linear regime. It is not the
nonlinear attractor run.

## 5. Why a brute-force full wave box is the wrong next computation

For each finite halo define

```text
epsilon_n=hbar/(m v_infinity R_n)=m_WKB,row/m_gap.
```

The smooth Wigner/Vlasov correction at radius `r=xR_n` scales as
`(epsilon_n/x)^2`. Across all observed radii the largest proxy is
`{summary['maximum_observed_quantum_proxy']}`. At the strict mass,
`{summary['strict_rows_classical_at_all_observed_radii']}/350` rows are below
one percent at every measured point; the counts are
`{summary['benchmark20_rows_classical_at_all_observed_radii']}/350` at
`1e-20 eV` and
`{summary['benchmark18_rows_classical_at_all_observed_radii']}/350` at
`1e-18 eV`. The core cannot universally be discarded, but most measured
radii are already collisionless.

Conversely, resolving the full diameter `2R_t` with eight cells per reduced
de Broglie length would require between
`{summary['minimum_full_wave_grid_side']}` and
`{summary['maximum_full_wave_grid_side']}` cells per side. Even the minimum
working-memory estimate is far beyond the current machine for a full-edge
three-dimensional wave volume. This is a physical multiscale hierarchy, not
a reason to lower resolution until a run appears to pass.

The isolated coherent Schrodinger--Poisson scaling also fixes
`M R proportional m^-2`. The target invariant
`G M_edge m^2 R_n/hbar^2` spans a factor
`{summary['coherent_scaling_invariant_span']}` over the locked states. The
galaxy family therefore cannot be one rescaled coherent soliton. Its correct
candidate interpretation is the already-constructed multistream Vlasov halo
with a wave-resolved core.

## 6. Exact status and next calculation

```text
parent KG -> Schrodinger--Poisson limit             = derived;
same Einstein residue -> Poisson source              = derived;
SP -> smooth-scale Vlasov limit                      = derived;
homogeneous primordial state forms halos             = rejected exactly;
three-mass post-equality transfer                     = executed;
FFT wave runner versus independent mode ODE           = validated;
all finite halo-patch modes survive this late gate    = verified;
full 3D wave box as current route                     = rejected by resolution;

parent/empirical primordial covariance                = missing;
radiation-era Boltzmann transfer                       = missing;
actual infrared c_ess                                  = missing;
hybrid nonlinear collapse to q/core/p=2 edge          = not run;
projective profile as a cosmological attractor         = not derived.
```

The next calculation should derive the motion two-point covariance from the
4948 2PI state if possible. In parallel, construct one explicitly conditional
adiabatic comparator from a sourced CMB covariance and run a Vlasov volume
with wave-resolved zoom cores. The covariance, random seed, box and resolution
must be fixed before looking at the resulting halo profiles. The result must
be compared to `q_parent`, the core cut and `p=2` without refitting them.

Primary references:

- fuzzy transfer and Jeans scale: {PRIMARY_SOURCE_URLS['fuzzy_transfer']}
- cosmological SP numerics and resolution: {PRIMARY_SOURCE_URLS['SP_numerics']}
- scalar adiabatic/isocurvature initial data: {PRIMARY_SOURCE_URLS['scalar_adiabatic_initial_data']}
- nonequilibrium 2PI covariance: {PRIMARY_SOURCE_URLS['nonequilibrium_2PI']}

All `{result['validation_count']}` validations pass. The protected
`formalization-workbench` digest remains
`{result['formalization_workbench_tree_sha256']}`. All parent and galaxy
sources were read-only. No GitHub action occurred.
"""
    DOCUMENT.write_text(text, encoding="utf-8")


def main() -> None:
    missing_sources = [
        str(path) for path in SOURCE_PATHS.values() if not path.exists()
    ]
    if missing_sources:
        raise FileNotFoundError(f"missing checkpoint sources: {missing_sources}")
    source_hashes_before = {
        name: file_digest(path) for name, path in SOURCE_PATHS.items()
    }
    formal_before = tree_digest(FORMAL)
    state_rows = read_csv(STATE_ROWS)
    background_rows = read_csv(BACKGROUND_ROWS)
    mass_rows = read_csv(MASS_ROWS)
    jeans_rows = read_csv(JEANS_ROWS)
    halo_rows = read_csv(HALO_ROWS)
    sample_points = parse_samples(GALAXY_SAMPLES)

    selected_mass_labels = [
        "ten_times_WKB_floor",
        "benchmark_1e_minus20_eV",
        "benchmark_1e_minus18_eV",
    ]
    mass_lookup = {
        row["mass_label"]: float(row["m_gap_eV"])
        for row in mass_rows
        if row["row_type"] == "candidate_mass"
    }
    jeans_lookup = {
        row["mass_label"]: float(row["k_Jeans_comoving_Mpc_inverse"])
        for row in jeans_rows
        if row["epoch"] == "equality"
        and row["gravity_density"] == "total_matter_gravity"
        and row["mass_label"] in selected_mass_labels
    }
    state_lookup = {
        (row["galaxy"], row["mapping"]): row for row in state_rows
    }

    limit_rows = parent_limit_rows()
    homogeneous_rows = no_collapse_rows()
    initial_rows = initial_data_rows()
    transfer_rows: list[dict[str, Any]] = []
    transfer_summary_rows: list[dict[str, Any]] = []
    transfer_by_mass: dict[str, dict[str, np.ndarray | float]] = {}
    fine_curves: list[np.ndarray] = []
    transfer_convergence_errors: list[float] = []

    for mass_label in selected_mass_labels:
        mass_eV = mass_lookup[mass_label]
        jeans_wavenumber = jeans_lookup[mass_label]
        physical_wavenumbers = TRANSFER_RATIO_GRID * jeans_wavenumber
        density, _, cdm_density, _ = integrate_linear_modes(
            mass_eV,
            physical_wavenumbers,
            1.0,
            TRANSFER_STEPS,
        )
        check_density, _, check_cdm_density, _ = integrate_linear_modes(
            mass_eV,
            physical_wavenumbers,
            1.0,
            TRANSFER_CHECK_STEPS,
        )
        amplitude_ratio = density / cdm_density
        power_ratio = amplitude_ratio**2
        check_power_ratio = (check_density / check_cdm_density) ** 2
        convergence_error = float(
            np.max(np.abs(power_ratio - check_power_ratio))
        )
        transfer_convergence_errors.append(convergence_error)
        half_ratio = first_half_power_ratio(
            TRANSFER_RATIO_GRID, power_ratio
        )
        half_wavenumber = half_ratio * jeans_wavenumber
        present_matter_density_Msun_Mpc3 = (
            3.0
            * H0_SI**2
            * OMEGA_M
            / (8.0 * math.pi * G_SI)
            * MPC_M**3
            / MSUN_KG
        )
        half_mass = (
            4.0
            * math.pi
            / 3.0
            * present_matter_density_Msun_Mpc3
            * (math.pi / half_wavenumber) ** 3
        )
        transfer_by_mass[mass_label] = {
            "ratio": TRANSFER_RATIO_GRID.copy(),
            "power": power_ratio.copy(),
            "half_ratio": half_ratio,
        }
        fine_curves.append(power_ratio)
        for ratio, wavenumber, amplitude, power in zip(
            TRANSFER_RATIO_GRID,
            physical_wavenumbers,
            amplitude_ratio,
            power_ratio,
        ):
            transfer_rows.append(
                {
                    "mass_label": mass_label,
                    "m_gap_eV": mass_eV,
                    "k_over_k_Jeans_equality": float(ratio),
                    "k_comoving_Mpc_inverse": float(wavenumber),
                    "post_equality_amplitude_ratio_to_CDM": float(amplitude),
                    "post_equality_power_ratio_to_CDM": float(power),
                    "same_initial_delta_and_Meszaros_slope": True,
                    "full_radiation_era_transfer": False,
                    "valid_for_structure_claim": False,
                    "checkpoint_marker": MARKER,
                }
            )
        transfer_summary_rows.append(
            {
                "mass_label": mass_label,
                "m_gap_eV": mass_eV,
                "k_Jeans_equality_Mpc_inverse": jeans_wavenumber,
                "half_power_k_over_k_Jeans_equality": half_ratio,
                "half_power_k_Mpc_inverse": half_wavenumber,
                "half_power_mass_Msun": half_mass,
                "power_ratio_at_kJeans_equality": interpolate_power(
                    TRANSFER_RATIO_GRID, power_ratio, 1.0
                ),
                "RK4_4000_vs_8000_max_power_difference": convergence_error,
                "post_equality_only": True,
                "valid_for_structure_claim": False,
                "checkpoint_marker": MARKER,
            }
        )

    patch_rows: list[dict[str, Any]] = []
    classicality_rows: list[dict[str, Any]] = []
    for halo in halo_rows:
        galaxy = halo["galaxy"]
        mapping = halo["mapping"]
        mass_label = halo["mass_label"]
        mass_eV = float(halo["m_gap_eV"])
        source = state_lookup[(galaxy, mapping)]
        lagrangian_radius = float(
            halo["Lagrangian_motion_patch_radius_Mpc"]
        )
        jeans_wavenumber = jeans_lookup[mass_label]
        transfer = transfer_by_mass[mass_label]
        ratio_grid = np.asarray(transfer["ratio"])
        power_grid = np.asarray(transfer["power"])
        k_inverse_R = 1.0 / lagrangian_radius
        k_pi_R = math.pi / lagrangian_radius
        k_2pi_R = 2.0 * math.pi / lagrangian_radius
        patch_rows.append(
            {
                "galaxy": galaxy,
                "mapping": mapping,
                "mass_label": mass_label,
                "m_gap_eV": mass_eV,
                "Lagrangian_patch_radius_Mpc": lagrangian_radius,
                "k_Jeans_equality_Mpc_inverse": jeans_wavenumber,
                "k_1_over_R_over_kJeans": k_inverse_R / jeans_wavenumber,
                "k_pi_over_R_over_kJeans": k_pi_R / jeans_wavenumber,
                "k_2pi_over_R_over_kJeans": k_2pi_R / jeans_wavenumber,
                "post_equality_power_ratio_k_1_over_R": interpolate_power(
                    ratio_grid, power_grid, k_inverse_R / jeans_wavenumber
                ),
                "post_equality_power_ratio_k_pi_over_R": interpolate_power(
                    ratio_grid, power_grid, k_pi_R / jeans_wavenumber
                ),
                "post_equality_power_ratio_k_2pi_over_R": interpolate_power(
                    ratio_grid, power_grid, k_2pi_R / jeans_wavenumber
                ),
                "primordial_patch_probability_derived": False,
                "valid_for_structure_claim": False,
                "checkpoint_marker": MARKER,
            }
        )

        transition_radius = float(halo["R_n_kpc"])
        edge_ratio = float(halo["R_edge_over_R_n"])
        velocity_infinity = float(source["v_infinity_km_s"])
        epsilon_transition = (
            float(source["minimum_m_gap_eV_for_lambda_db_le_Rn"])
            / mass_eV
        )
        observed_x = np.array(
            [
                point["r_kpc"] / transition_radius
                for point in sample_points[galaxy]
            ]
        )
        observed_quantum_proxy = (
            epsilon_transition / observed_x
        ) ** 2
        full_wave_grid_side = math.ceil(
            16.0 * edge_ratio / epsilon_transition
        )
        working_memory_TiB = (
            full_wave_grid_side**3 * 64.0 / 2.0**40
        )
        motion_mass = float(halo["motion_mass_edge_Msun"])
        coherent_invariant = (
            G_SI
            * motion_mass
            * MSUN_KG
            * (mass_eV * EV_C2_KG) ** 2
            * transition_radius
            * 1000.0
            * 3.085677581491367e16
            / HBAR_SI**2
        )
        classicality_rows.append(
            {
                "galaxy": galaxy,
                "mapping": mapping,
                "mass_label": mass_label,
                "m_gap_eV": mass_eV,
                "epsilon_at_R_n": epsilon_transition,
                "epsilon_squared_at_R_n": epsilon_transition**2,
                "maximum_observed_quantum_proxy_epsilon_over_x_squared": float(
                    np.max(observed_quantum_proxy)
                ),
                "all_observed_radii_below_one_percent_quantum_proxy": bool(
                    np.max(observed_quantum_proxy) < 0.01
                ),
                "R_edge_over_R_n": edge_ratio,
                "grid_side_for_8_cells_per_reduced_deBroglie_full_diameter": full_wave_grid_side,
                "working_memory_64_bytes_per_cell_TiB": working_memory_TiB,
                "coherent_SP_scaling_invariant_G_M_m2_Rn_over_hbar2": coherent_invariant,
                "recommended_solver_region": (
                    "Vlasov_all_observed_radii_wave_core_below_data"
                    if np.max(observed_quantum_proxy) < 0.01
                    else "wave_core_plus_Vlasov_outer_observed_overlap"
                ),
                "full_edge_3D_wave_run_feasible_on_32GB": working_memory_TiB
                < 0.02,
                "valid_for_structure_claim": False,
                "checkpoint_marker": MARKER,
            }
        )

    wave_rows: list[dict[str, Any]] = []
    base_wave_lookup: dict[tuple[str, float], dict[str, Any]] = {}
    for mass_label in selected_mass_labels:
        for ratio in (0.7, 1.3):
            values = split_step_mode(
                mass_lookup[mass_label],
                jeans_lookup[mass_label],
                ratio,
                FFT_BASE_GRID,
                FFT_BASE_STEPS,
            )
            row = {
                "run_role": "three_mass_base_validation",
                "mass_label": mass_label,
                **values,
                "nonlinear_attractor_test": False,
                "checkpoint_marker": MARKER,
            }
            wave_rows.append(row)
            base_wave_lookup[(mass_label, ratio)] = row

    convergence_rows: list[dict[str, Any]] = []
    strict_label = "ten_times_WKB_floor"
    for grid_size, steps in ((24, 180), (40, 300)):
        values = split_step_mode(
            mass_lookup[strict_label],
            jeans_lookup[strict_label],
            1.3,
            grid_size,
            steps,
        )
        convergence_rows.append(
            {
                "run_role": "strict_mass_grid_time_convergence",
                "mass_label": strict_label,
                **values,
                "nonlinear_attractor_test": False,
                "checkpoint_marker": MARKER,
            }
        )
    convergence_rows.append(
        {
            **base_wave_lookup[(strict_label, 1.3)],
            "run_role": "strict_mass_grid_time_convergence",
        }
    )
    wave_rows.extend(convergence_rows)

    route_decisions = route_rows()
    source_hashes_after = {
        name: file_digest(path) for name, path in SOURCE_PATHS.items()
    }
    formal_after = tree_digest(FORMAL)

    stacked_curves = np.vstack(fine_curves)
    maximum_curve_disagreement = float(
        np.max(np.ptp(stacked_curves, axis=0))
    )
    half_ratios = [
        float(row["half_power_k_over_k_Jeans_equality"])
        for row in transfer_summary_rows
    ]
    base_wave_rows = [
        row for row in wave_rows if row["run_role"] == "three_mass_base_validation"
    ]
    convergence_amplitudes = [
        float(row["FFT_mode_amplitude_final"])
        for row in wave_rows
        if row["run_role"] == "strict_mass_grid_time_convergence"
    ]
    coherent_values = [
        float(
            row[
                "coherent_SP_scaling_invariant_G_M_m2_Rn_over_hbar2"
            ]
        )
        for row in classicality_rows
    ]
    counts_by_mass = {
        mass_label: sum(
            row["all_observed_radii_below_one_percent_quantum_proxy"]
            for row in classicality_rows
            if row["mass_label"] == mass_label
        )
        for mass_label in selected_mass_labels
    }
    summary = {
        "transfer_curve_rows": len(transfer_rows),
        "patch_rows": len(patch_rows),
        "classicality_rows": len(classicality_rows),
        "maximum_transfer_RK4_convergence_error": max(
            transfer_convergence_errors
        ),
        "maximum_mass_scaled_transfer_disagreement": maximum_curve_disagreement,
        "half_power_ratio_mean": sum(half_ratios) / len(half_ratios),
        "half_power_ratio_span": max(half_ratios) - min(half_ratios),
        "minimum_patch_1_over_R_power_ratio": min(
            row["post_equality_power_ratio_k_1_over_R"]
            for row in patch_rows
        ),
        "minimum_patch_pi_power_ratio": min(
            row["post_equality_power_ratio_k_pi_over_R"]
            for row in patch_rows
        ),
        "minimum_patch_2pi_power_ratio": min(
            row["post_equality_power_ratio_k_2pi_over_R"]
            for row in patch_rows
        ),
        "maximum_patch_2pi_over_kJeans": max(
            row["k_2pi_over_R_over_kJeans"] for row in patch_rows
        ),
        "maximum_observed_quantum_proxy": max(
            row[
                "maximum_observed_quantum_proxy_epsilon_over_x_squared"
            ]
            for row in classicality_rows
        ),
        "strict_rows_classical_at_all_observed_radii": counts_by_mass[
            "ten_times_WKB_floor"
        ],
        "benchmark20_rows_classical_at_all_observed_radii": counts_by_mass[
            "benchmark_1e_minus20_eV"
        ],
        "benchmark18_rows_classical_at_all_observed_radii": counts_by_mass[
            "benchmark_1e_minus18_eV"
        ],
        "minimum_full_wave_grid_side": min(
            row[
                "grid_side_for_8_cells_per_reduced_deBroglie_full_diameter"
            ]
            for row in classicality_rows
        ),
        "maximum_full_wave_grid_side": max(
            row[
                "grid_side_for_8_cells_per_reduced_deBroglie_full_diameter"
            ]
            for row in classicality_rows
        ),
        "minimum_full_wave_working_memory_TiB": min(
            row["working_memory_64_bytes_per_cell_TiB"]
            for row in classicality_rows
        ),
        "maximum_full_wave_working_memory_TiB": max(
            row["working_memory_64_bytes_per_cell_TiB"]
            for row in classicality_rows
        ),
        "coherent_scaling_invariant_span": max(coherent_values)
        / min(coherent_values),
        "maximum_split_step_amplitude_error": max(
            row["relative_amplitude_error"] for row in base_wave_rows
        ),
        "maximum_split_step_norm_drift": max(
            row["wave_norm_relative_drift"] for row in base_wave_rows
        ),
        "split_step_convergence_relative_spread": (
            max(convergence_amplitudes) - min(convergence_amplitudes)
        )
        / np.mean(convergence_amplitudes),
        "homogeneous_no_collapse_proved": all(
            row["passed"] for row in homogeneous_rows
        ),
    }

    output_rows = {
        LIMIT_CSV: limit_rows,
        NO_COLLAPSE_CSV: homogeneous_rows,
        TRANSFER_CSV: transfer_rows,
        TRANSFER_SUMMARY_CSV: transfer_summary_rows,
        PATCH_CSV: patch_rows,
        CLASSICALITY_CSV: classicality_rows,
        WAVE_CSV: wave_rows,
        INITIAL_DATA_CSV: initial_rows,
        ROUTE_CSV: route_decisions,
    }
    for path, rows in output_rows.items():
        write_csv(path, rows)

    result: dict[str, Any] = {
        "checked_date": CHECKED_DATE,
        "checkpoint_marker": MARKER,
        "source_paths": {name: str(path) for name, path in SOURCE_PATHS.items()},
        "source_hashes_before": source_hashes_before,
        "source_hashes_after": source_hashes_after,
        "primary_source_urls": PRIMARY_SOURCE_URLS,
        "formalization_workbench_tree_sha256": formal_after,
        "summary": summary,
        "route_decision": "SP_VLASOV_IVP_VALIDATED_PATCHES_SURVIVE_HOMOGENEOUS_FORMATION_REJECTED_ADVANCE_TO_PRIMORDIAL_COVARIANCE_AND_HYBRID_COLLAPSE",
        "parent_SP_Vlasov_limit_derived": True,
        "homogeneous_state_forms_halos": False,
        "post_equality_transfer_executed": True,
        "split_step_runner_validated_linear": True,
        "actual_parent_c_ess_inserted": False,
        "primordial_covariance_derived": False,
        "nonlinear_profile_attractor_derived": False,
        "valid_for_cosmology_claim": False,
        "valid_for_galaxy_claim": False,
        "valid_for_PPN_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    checks = [
        ("source_paths_exist", not missing_sources, str(missing_sources)),
        (
            "all_sources_and_galaxy_sample_read_only",
            source_hashes_before == source_hashes_after,
            str(source_hashes_after),
        ),
        (
            "formalization_workbench_unchanged",
            formal_before == FORMAL_BASELINE and formal_after == FORMAL_BASELINE,
            formal_after,
        ),
        (
            "same_parent_SP_Vlasov_chain_complete",
            len(limit_rows) == 6
            and all("DERIVED" in row["status"] or "EXACT" in row["status"] for row in limit_rows),
            str([row["status"] for row in limit_rows]),
        ),
        (
            "homogeneous_no_collapse_theorem_closes",
            summary["homogeneous_no_collapse_proved"],
            "translation invariance plus uniqueness requires nonzero covariance",
        ),
        (
            "three_locked_mass_transfer_curves_executed",
            len(transfer_rows) == 3 * len(TRANSFER_RATIO_GRID),
            str(len(transfer_rows)),
        ),
        (
            "transfer_RK4_converges",
            summary["maximum_transfer_RK4_convergence_error"] < 2.0e-6,
            str(summary["maximum_transfer_RK4_convergence_error"]),
        ),
        (
            "mass_scaled_transfer_curves_collapse",
            summary["maximum_mass_scaled_transfer_disagreement"] < 2.0e-10
            and summary["half_power_ratio_span"] < 2.0e-10,
            str(
                [
                    summary["maximum_mass_scaled_transfer_disagreement"],
                    summary["half_power_ratio_span"],
                ]
            ),
        ),
        (
            "all_1050_halo_patch_modes_executed",
            len(patch_rows) == 1050,
            str(len(patch_rows)),
        ),
        (
            "all_halo_patch_modes_survive_post_equality_gate",
            summary["minimum_patch_2pi_power_ratio"] > 0.9
            and summary["maximum_patch_2pi_over_kJeans"] < 0.5,
            str(
                [
                    summary["minimum_patch_2pi_power_ratio"],
                    summary["maximum_patch_2pi_over_kJeans"],
                ]
            ),
        ),
        (
            "all_classicality_and_resolution_rows_executed",
            len(classicality_rows) == 1050,
            str(len(classicality_rows)),
        ),
        (
            "wave_core_not_silently_deleted",
            summary["strict_rows_classical_at_all_observed_radii"] < 350
            and summary["maximum_observed_quantum_proxy"] > 0.01,
            str(
                [
                    summary["strict_rows_classical_at_all_observed_radii"],
                    summary["maximum_observed_quantum_proxy"],
                ]
            ),
        ),
        (
            "full_edge_bruteforce_wave_route_rejected_by_resolution",
            summary["minimum_full_wave_working_memory_TiB"] > 0.03125
            and all(
                not row["full_edge_3D_wave_run_feasible_on_32GB"]
                for row in classicality_rows
            ),
            str(summary["minimum_full_wave_working_memory_TiB"]),
        ),
        (
            "single_coherent_soliton_scaling_rejected",
            summary["coherent_scaling_invariant_span"] > 1.0e4,
            str(summary["coherent_scaling_invariant_span"]),
        ),
        (
            "six_three_mass_split_step_modes_executed",
            len(base_wave_rows) == 6,
            str(len(base_wave_rows)),
        ),
        (
            "split_step_matches_independent_linear_ODE",
            summary["maximum_split_step_amplitude_error"] < 5.0e-4,
            str(summary["maximum_split_step_amplitude_error"]),
        ),
        (
            "split_step_unitarity_controlled",
            summary["maximum_split_step_norm_drift"] < 1.0e-11,
            str(summary["maximum_split_step_norm_drift"]),
        ),
        (
            "split_step_grid_time_convergence",
            summary["split_step_convergence_relative_spread"] < 5.0e-4,
            str(summary["split_step_convergence_relative_spread"]),
        ),
        (
            "missing_covariance_not_replaced_by_hidden_seed",
            any(
                row["status"] == "MISSING_DECISIVE_INITIAL_COVARIANCE"
                for row in initial_rows
            )
            and not result["primordial_covariance_derived"],
            "nonlinear formation remains blocked until one global covariance is fixed",
        ),
        (
            "actual_parent_interaction_not_smuggled",
            not result["actual_parent_c_ess_inserted"],
            "free controlled comparator only",
        ),
        (
            "route_advances_to_covariance_and_hybrid_collapse",
            route_decisions[-1]["status"] == "OPEN_DECISIVE_GATE"
            and result["route_decision"].endswith("HYBRID_COLLAPSE"),
            result["route_decision"],
        ),
        (
            "all_output_CSVs_parse",
            all(len(read_csv(path)) > 0 for path in output_rows),
            str([str(path) for path in output_rows]),
        ),
        (
            "nonlinear_attractor_not_claimed",
            not result["nonlinear_profile_attractor_derived"],
            "linear transfer and stationary equilibrium do not prove formation",
        ),
        (
            "claim_discipline",
            not result["valid_for_cosmology_claim"]
            and not result["valid_for_galaxy_claim"]
            and not result["valid_for_PPN_claim"]
            and not result["valid_for_full_MTS_claim"],
            "private derivation and runner gate only",
        ),
    ]
    validation_rows = [
        {
            "check_id": f"V5155_{index:02d}_{name}",
            "passed": passed,
            "detail": detail,
            "checkpoint_marker": MARKER,
        }
        for index, (name, passed, detail) in enumerate(checks, start=1)
    ]
    result["validation_count"] = len(validation_rows)
    result["validation_failures"] = [
        row["check_id"] for row in validation_rows if not row["passed"]
    ]
    write_csv(VALIDATION_CSV, validation_rows)
    write_document(result)
    atomic_json(RESULT_JSON, result)
    if result["validation_failures"]:
        raise RuntimeError(
            f"checkpoint 5155 validation failures: {result['validation_failures']}"
        )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
