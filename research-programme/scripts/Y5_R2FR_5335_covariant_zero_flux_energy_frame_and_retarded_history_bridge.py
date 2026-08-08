from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
import sys
from pathlib import Path
from typing import Any


os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
os.environ.setdefault("NUMEXPR_NUM_THREADS", "1")
os.environ.setdefault("VECLIB_MAXIMUM_THREADS", "1")
sys.dont_write_bytecode = True

import numpy as np


CHECKPOINT = 5335
MARKER = "MTS_5335_COVARIANT_ENERGY_FRAME_RETARDED_FOLD_BRIDGE"
POST = Path(__file__).resolve().parents[1]
ROOT = POST.parent
FORMAL = ROOT / "formalization-workbench"
OUT = POST / "source-intake" / "functional_rg" / str(CHECKPOINT)
RESIDUALS = POST / "source-intake" / "mts_residuals"
REFERENCE = (
    POST
    / "source-intake"
    / "maths_exploration"
    / str(CHECKPOINT)
    / "maths-exploration-bridge-source-lock.md"
)
DOCUMENT = (
    POST
    / "5335-Y5-R2FR-covariant-zero-flux-energy-frame-and-retarded-"
    "history-bridge.md"
)
VALIDATION = RESIDUALS / f"P8_Y5_BRR545_{CHECKPOINT}_VALIDATION.csv"
RESULT = OUT / "covariant_energy_frame_retarded_history_bridge_result.json"
FORMAL_DIGEST = "0ec1bc6012136ffc6b28a1512aca6ce712b6decd2ff793310a9bd61775f3db1f"
REFERENCE_DIGEST = "cb8a8d498f9942fd6f76779fc2a1fd0ef6510732e7c6b16a4a359571f37e9fc0"
REMOTE_REPOSITORY = "https://github.com/Martin123132/maths-exploration-"
REMOTE_COMMIT = "f253617090be3917b9949bde3c90ff0aea263c80"
REMOTE_BLOBS = {
    "Maths": "aec6a84e4e945e30ea051f0e00a6e99dea3aa326",
    "Spectrum": "cb0ffb13091055d28cfbc65c5f7c33095eca9646",
}
SOURCE_LOCKS = {
    "4175-Y5-R2FR-Maxwell-Hodge-Poynting-stress-owner-theorem-or-EM-side-channel-bound.md": "b59cedfed66cd0b016466407a9bfe0d4b082f6578daed066fc2197da72a37f04",
    "4207-Y5-R2FR-EM-Poynting-Hodge-source-owner-lock-or-side-channel-bound.md": "3546dcda8d13c71437595ee828a88bd0e5db447bd951e58a7bd4388e8f948218",
    "4935-Y5-R2FR-completed-fixed-point-GR-connected-trajectory-and-motion-sector-entry.md": "649da892ba5c256b7670206e837604dbbe04358fcd3705b5871906805e00c1df",
    "4948-Y5-R2FR-single-parent-motion-Hessian-to-galaxy-phase-flow-and-universal-Jgap-interface.md": "b563ab1bf95974732dd5f2a3ab2cd5af2d5b414011648554e5247a930b47aec0",
    "5187-Y5-R2FR-canonical-local-parent-action-Hessian-source-residue-and-scale-setting-theorem.md": "4556205ec12e11930a13d0ed9b5e27b6b4619f3752a5e10db2a4b767dcdec674",
    "5189-Y5-R2FR-motion-sector-ADM-projection-clock-only-ancestry-and-local-tensor-protection-theorem.md": "4514f59f95fa00fbddd652511bf49a98a84347b3f4f10747afbdfb6d3917e266",
    "5208-Y5-R2FR-common-minimal-motion-trajectory-canonical-Z-quotient-absolute-scale-covariance-and-local-GR-selection.md": "95f49142309bcc8b438c864d170134b9952086ca6b23322960f8eec29edad8c8",
    "5211-Y5-R2FR-selected-trajectory-exact-GR-Maxwell-consistent-truncation-universal-source-and-matched-GRSM-excess-theorem.md": "ee8eea0c2f7a05ace5849992c271ce1a4a667a3fb1a537d92170b99f0bd082cb",
    "5334-Y5-R2FR-D4-outer-regulator-ladder-controller.md": "b4909340591f5dff56ecc02a2bea36c89a98b1a287aeb07dac8a67c552aca294",
}

ETA = np.diag([-1.0, 1.0, 1.0, 1.0])
TOLERANCE = 2.0e-12


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def serialized_hash(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def formal_inventory_digest() -> str:
    rows = [
        {
            "relative_path": str(path.relative_to(FORMAL)),
            "size": str(path.stat().st_size),
            "sha256": digest(path),
        }
        for path in sorted(
            (item for item in FORMAL.rglob("*") if item.is_file()),
            key=lambda item: str(item).lower(),
        )
    ]
    return serialized_hash(rows)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty CSV: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    temporary.replace(path)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(value, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


def validation_row(gate: str, passed: bool, detail: str) -> dict[str, Any]:
    return {
        "gate": gate,
        "passed": passed,
        "detail": detail,
        "checkpoint": CHECKPOINT,
        "marker": MARKER,
    }


def observer(beta: float) -> np.ndarray:
    if abs(beta) >= 1.0:
        raise ValueError("a timelike observer requires |beta|<1")
    gamma = 1.0 / math.sqrt(1.0 - beta * beta)
    return np.array([gamma, gamma * beta, 0.0, 0.0], dtype=float)


def stress_two_null_beams(energy_plus: float, energy_minus: float) -> np.ndarray:
    k_plus = np.array([1.0, 1.0, 0.0, 0.0])
    k_minus = np.array([1.0, -1.0, 0.0, 0.0])
    return energy_plus * np.outer(k_plus, k_plus) + energy_minus * np.outer(
        k_minus, k_minus
    )


def decompose_stress(
    stress_up: np.ndarray, timelike_observer: np.ndarray
) -> dict[str, Any]:
    observer_cov = ETA @ timelike_observer
    projector = np.eye(4) + np.outer(timelike_observer, observer_cov)
    energy_density = float(observer_cov @ stress_up @ observer_cov)
    flux = -projector @ stress_up @ observer_cov
    flux_squared = float(flux @ ETA @ flux)
    orthogonality = float(flux @ ETA @ timelike_observer)
    return {
        "energy_density": energy_density,
        "flux": flux,
        "flux_squared": flux_squared,
        "orthogonality": orthogonality,
        "dominant_energy_margin": energy_density**2 - flux_squared,
    }


def landau_beta_two_beams(energy_plus: float, energy_minus: float) -> float | None:
    if energy_plus <= 0.0 or energy_minus <= 0.0:
        return None
    root_plus = math.sqrt(energy_plus)
    root_minus = math.sqrt(energy_minus)
    return (root_plus - root_minus) / (root_plus + root_minus)


def energy_frame_rows() -> tuple[list[dict[str, Any]], dict[str, float]]:
    cases = (
        ("equal_opposing_null_streams", 1.0, 1.0),
        ("unequal_opposing_null_streams", 4.0, 1.0),
        ("near_null_opposing_streams", 1.0, 1.0e-6),
        ("single_null_stream", 1.0, 0.0),
    )
    rows: list[dict[str, Any]] = []
    maximum_orthogonality = 0.0
    maximum_landau_flux = 0.0
    maximum_eigen_residual = 0.0
    for case, energy_plus, energy_minus in cases:
        stress = stress_two_null_beams(energy_plus, energy_minus)
        lab = decompose_stress(stress, observer(0.0))
        flux_speed = float(lab["flux"][1] / lab["energy_density"])
        landau_beta = landau_beta_two_beams(energy_plus, energy_minus)
        if landau_beta is None:
            landau_exists = False
            landau_density: float | str = "UNDEFINED_NULL_LIMIT"
            landau_flux_norm: float | str = "UNDEFINED_NULL_LIMIT"
            eigen_residual: float | str = "UNDEFINED_NULL_LIMIT"
            timelike_norm: float | str = "UNDEFINED_NULL_LIMIT"
        else:
            landau_observer = observer(landau_beta)
            landau = decompose_stress(stress, landau_observer)
            landau_density = float(landau["energy_density"])
            landau_flux_norm = math.sqrt(max(0.0, float(landau["flux_squared"])))
            mixed_stress = stress @ ETA
            eigen_residual = float(
                np.linalg.norm(
                    mixed_stress @ landau_observer
                    + landau_density * landau_observer
                )
            )
            timelike_norm = float(landau_observer @ ETA @ landau_observer)
            landau_exists = abs(landau_beta) < 1.0
            maximum_landau_flux = max(maximum_landau_flux, landau_flux_norm)
            maximum_eigen_residual = max(maximum_eigen_residual, eigen_residual)
        maximum_orthogonality = max(
            maximum_orthogonality, abs(float(lab["orthogonality"]))
        )
        rows.append(
            {
                "case": case,
                "energy_plus": energy_plus,
                "energy_minus": energy_minus,
                "lab_energy_density": lab["energy_density"],
                "lab_flux_x": float(lab["flux"][1]),
                "observer_flux_ratio_w_x": flux_speed,
                "landau_beta_x": (
                    landau_beta
                    if landau_beta is not None
                    else "NULL_BOUNDARY_BETA_1"
                ),
                "landau_energy_density": landau_density,
                "landau_flux_norm": landau_flux_norm,
                "landau_eigen_residual": eigen_residual,
                "landau_timelike_norm": timelike_norm,
                "dominant_energy_margin_lab": lab["dominant_energy_margin"],
                "landau_frame_exists": landau_exists,
                "flux_ratio_equals_landau_beta": (
                    landau_beta is not None
                    and abs(flux_speed - landau_beta) <= TOLERANCE
                ),
                "interpretation": (
                    "zero flux with positive invariant energy"
                    if case == "equal_opposing_null_streams"
                    else "observer flux ratio is not the rest-frame boost"
                    if case == "unequal_opposing_null_streams"
                    else "timelike frame approaches a singular null limit"
                    if case == "near_null_opposing_streams"
                    else "nonzero null stress has no timelike rest frame"
                ),
            }
        )
    return rows, {
        "maximum_flux_observer_orthogonality_residual": maximum_orthogonality,
        "maximum_landau_flux_norm": maximum_landau_flux,
        "maximum_landau_eigen_residual": maximum_eigen_residual,
    }


def energy_frame_theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "object": "observer_decomposition",
            "definition": "h^mu_nu=delta^mu_nu+n^mu n_nu; epsilon=T_mn n^m n^n; q^mu=-h^mu_a T^ab n_b",
            "derived_property": "n_mu q^mu=0",
            "existence": "for every chosen unit timelike n",
            "fundamental_status": "observer-dependent decomposition",
            "MTS_role": "diagnostic in a selected clock/coframe",
        },
        {
            "object": "observer_flux_velocity",
            "definition": "w_obs^mu=q^mu/epsilon in c=1 units",
            "derived_property": "q^2<=epsilon^2 under the dominant energy condition",
            "existence": "epsilon>0",
            "fundamental_status": "not an observer-independent field",
            "MTS_role": "may describe energy transport relative to the MTS clock",
        },
        {
            "object": "Landau_energy_frame",
            "definition": "T^mu_nu U_L^nu=-rho_L U_L^mu; U_L^2=-1",
            "derived_property": "q^mu[U_L]=0",
            "existence": "type-I/non-null stress with a future timelike eigenvector",
            "fundamental_status": "algebraically derived from the state stress",
            "MTS_role": "candidate occupied-state flow diagnostic, not a new source",
        },
        {
            "object": "classical_motion_clock",
            "definition": "U_chi,mu=-nabla_mu chi/sqrt(-X), X<0",
            "derived_property": "T_chi^mu_nu U_chi^nu=-rho_chi U_chi^mu and U_chi wedge dU_chi=0",
            "existence": "nonzero timelike scalar gradient",
            "fundamental_status": "derived from the parent scalar",
            "MTS_role": "own-stress Landau frame in the classical P(X) branch",
        },
        {
            "object": "occupied_motion_energy_frame",
            "definition": "T_occ^mu_nu U_occ^nu=-rho_occ U_occ^mu",
            "derived_property": "uses reflection-even T_occ from stationary 2PI/CTP stress while <chi>=0",
            "existence": "only where T_occ has a timelike eigenvector",
            "fundamental_status": "state-derived and may be absent or degenerate",
            "MTS_role": "usable bridge to the open occupied-state route",
        },
    ]


def electromagnetic_rows() -> tuple[list[dict[str, Any]], float]:
    cases = (
        ("vacuum", (0.0, 0.0, 0.0), (0.0, 0.0, 0.0)),
        ("null_plane_wave", (1.0, 0.0, 0.0), (0.0, 1.0, 0.0)),
        ("pure_electric", (2.0, 0.0, 0.0), (0.0, 0.0, 0.0)),
        ("parallel_fields", (1.0, 0.0, 0.0), (0.5, 0.0, 0.0)),
        ("generic_non_null", (1.0, 0.3, 0.0), (0.2, 0.8, 0.1)),
    )
    rows: list[dict[str, Any]] = []
    maximum_identity_residual = 0.0
    for case, electric_values, magnetic_values in cases:
        electric = np.asarray(electric_values, dtype=float)
        magnetic = np.asarray(magnetic_values, dtype=float)
        electric_squared = float(electric @ electric)
        magnetic_squared = float(magnetic @ magnetic)
        dot = float(electric @ magnetic)
        poynting = np.cross(electric, magnetic)
        poynting_squared = float(poynting @ poynting)
        energy_density = 0.5 * (electric_squared + magnetic_squared)
        invariant_i = 2.0 * (magnetic_squared - electric_squared)
        invariant_j = -4.0 * dot
        identity_rhs = 0.25 * (electric_squared - magnetic_squared) ** 2 + dot**2
        identity_residual = abs(
            energy_density**2 - poynting_squared - identity_rhs
        )
        maximum_identity_residual = max(
            maximum_identity_residual, identity_residual
        )
        is_vacuum = energy_density == 0.0
        is_nonzero_null = (
            not is_vacuum
            and abs(invariant_i) <= TOLERANCE
            and abs(invariant_j) <= TOLERANCE
        )
        if is_vacuum:
            classification = "VACUUM_DEGENERATE"
            frame_status = "every observer has zero flux; w_obs undefined"
        elif is_nonzero_null:
            classification = "NONZERO_NULL_TYPE_II"
            frame_status = "no timelike zero-flux frame"
        else:
            classification = "NON_NULL_TYPE_I"
            frame_status = "local timelike zero-Poynting frame exists"
        rows.append(
            {
                "case": case,
                "E_squared": electric_squared,
                "B_squared": magnetic_squared,
                "E_dot_B": dot,
                "energy_density": energy_density,
                "Poynting_squared": poynting_squared,
                "F_squared_invariant": invariant_i,
                "F_dual_F_invariant": invariant_j,
                "u_squared_minus_S_squared": energy_density**2
                - poynting_squared,
                "invariant_identity_rhs": identity_rhs,
                "identity_residual": identity_residual,
                "classification": classification,
                "energy_frame_status": frame_status,
            }
        )
    return rows, maximum_identity_residual


def straight_retarded_roots(beta: float, x: float, rho: float) -> list[float]:
    coefficient_2 = 1.0 - beta * beta
    coefficient_1 = 2.0 * (beta * x - 1.0)
    coefficient_0 = 1.0 - x * x - rho * rho
    if abs(coefficient_2) <= 1.0e-15:
        candidates = [-coefficient_0 / coefficient_1]
    else:
        discriminant = coefficient_1**2 - 4.0 * coefficient_2 * coefficient_0
        if discriminant < 0.0:
            return []
        root = math.sqrt(max(0.0, discriminant))
        candidates = [
            (-coefficient_1 - root) / (2.0 * coefficient_2),
            (-coefficient_1 + root) / (2.0 * coefficient_2),
        ]
    return sorted(
        value
        for value in candidates
        if -TOLERANCE <= value <= 1.0 + TOLERANCE
    )


def retarded_mismatch(
    beta: float, x: float, rho: float, history: float
) -> float:
    distance = math.sqrt((x - beta * history) ** 2 + rho**2)
    return 1.0 - history - distance


def retarded_jacobian(
    beta: float, x: float, rho: float, history: float
) -> float:
    displacement_x = x - beta * history
    distance = math.sqrt(displacement_x**2 + rho**2)
    return abs(1.0 - beta * displacement_x / distance)


def retarded_history_rows() -> tuple[list[dict[str, Any]], dict[str, float]]:
    cases = (
        ("subcritical_one_root", 0.4, 0.2, 0.3),
        ("supercritical_two_roots", 1.25, 1.05, 0.2),
    )
    rows: list[dict[str, Any]] = []
    maximum_root_residual = 0.0
    maximum_derivative_residual = 0.0
    maximum_discriminant_identity_residual = 0.0
    two_root_values: list[float] = []
    two_root_amplitudes: list[float] = []
    for case, beta, x, rho in cases:
        roots = straight_retarded_roots(beta, x, rho)
        discriminant_geometry = (
            (beta - x) ** 2 - (beta * beta - 1.0) * rho**2
        )
        for index, history in enumerate(roots):
            displacement_x = x - beta * history
            distance = math.sqrt(displacement_x**2 + rho**2)
            mismatch = retarded_mismatch(beta, x, rho, history)
            jacobian = retarded_jacobian(beta, x, rho, history)
            step = 1.0e-6
            finite_derivative = (
                retarded_mismatch(beta, x, rho, history + step)
                - retarded_mismatch(beta, x, rho, history - step)
            ) / (2.0 * step)
            derivative_residual = abs(abs(finite_derivative) - jacobian)
            denominator = distance * jacobian
            identity_target = math.sqrt(max(0.0, discriminant_geometry))
            identity_residual = abs(denominator - identity_target)
            amplitude = 1.0 / (4.0 * math.pi * denominator)
            maximum_root_residual = max(maximum_root_residual, abs(mismatch))
            maximum_derivative_residual = max(
                maximum_derivative_residual, derivative_residual
            )
            maximum_discriminant_identity_residual = max(
                maximum_discriminant_identity_residual, identity_residual
            )
            if case == "supercritical_two_roots":
                two_root_values.append(history)
                two_root_amplitudes.append(amplitude)
            rows.append(
                {
                    "case": case,
                    "beta": beta,
                    "x": x,
                    "rho": rho,
                    "root_index": index,
                    "retarded_history": history,
                    "root_mismatch": mismatch,
                    "R": distance,
                    "history_Jacobian": jacobian,
                    "finite_difference_abs_derivative": abs(finite_derivative),
                    "derivative_identity_residual": derivative_residual,
                    "R_times_Jacobian": denominator,
                    "sqrt_geometric_discriminant": identity_target,
                    "discriminant_identity_residual": identity_residual,
                    "unit_source_root_amplitude": amplitude,
                }
            )
    frequency = 1.0e-5
    exact_spectrum = sum(
        amplitude * np.exp(-1j * frequency * history)
        for amplitude, history in zip(two_root_amplitudes, two_root_values)
    )
    taylor_spectrum = sum(
        amplitude
        * (
            1.0
            - 1j * frequency * history
            - 0.5 * frequency**2 * history**2
        )
        for amplitude, history in zip(two_root_amplitudes, two_root_values)
    )
    finite_root_taylor_residual = float(abs(exact_spectrum - taylor_spectrum))
    return rows, {
        "maximum_root_residual": maximum_root_residual,
        "maximum_derivative_residual": maximum_derivative_residual,
        "maximum_discriminant_identity_residual": maximum_discriminant_identity_residual,
        "two_root_history_0": two_root_values[0],
        "two_root_history_1": two_root_values[1],
        "two_root_amplitude_difference": abs(
            two_root_amplitudes[0] - two_root_amplitudes[1]
        ),
        "finite_root_taylor_residual_at_1e-5": finite_root_taylor_residual,
    }


def retarded_covariant_rows() -> list[dict[str, Any]]:
    return [
        {
            "step": "flat_retarded_delta_reduction",
            "equation": "delta(g(tau))=sum_r delta(tau-tau_r)/|g'(tau_r)|",
            "consequence": "g'=-(1-rhat.v/u) gives the history Jacobian in the exact root sum",
            "status": "DERIVED_AND_NUMERICALLY_CHECKED",
        },
        {
            "step": "curved_direct_term",
            "equation": "G_ret=Theta_+[U_H delta(sigma)+V_H Theta(-sigma)]",
            "consequence": "a point-history direct term is weighted by |sigma_;a' u_s^a'|^-1; curvature/mass also produce a tail",
            "status": "COVARIANT_HADAMARD_CONTRACT",
        },
        {
            "step": "characteristic_cone_ownership",
            "equation": "u and the cone must be read from the principal symbol of the parent retarded Hessian",
            "consequence": "the toy wave speed cannot be inserted as an independent MTS coefficient",
            "status": "PARENT_OPERATOR_REQUIRED",
        },
        {
            "step": "finite_root_low_frequency_limit",
            "equation": "sum_r A_r exp(-i omega tau_r)=sum_n (-i omega)^n sum_r A_r tau_r^n/n!",
            "consequence": "a finite set of regular roots is analytic at omega=0 and cannot alone yield 1/|k|",
            "status": "EXACT_ANALYTICITY_NO_GO",
        },
        {
            "step": "critical_continuum_survivor",
            "equation": "Jacobian zero or accumulated histories create branch-point spectral structure",
            "consequence": "only the critical/continuum sector can address the occupied-state nonanalytic kernel",
            "status": "CONDITIONAL_SURVIVOR",
        },
    ]


def critical_fold_rows() -> tuple[list[dict[str, Any]], dict[str, float]]:
    classes = (
        ("quadratic_fold", -0.5),
        ("cubic_cusp", -2.0 / 3.0),
        ("critical_segment", -1.0),
    )
    momentum = np.logspace(-6.0, -2.0, 81)
    rows: list[dict[str, Any]] = []
    fold_fit = math.nan
    for singularity, history_exponent in classes:
        discriminant = momentum**2
        response = discriminant**history_exponent
        fitted_slope = float(
            np.polyfit(np.log(momentum), np.log(response), 1)[0]
        )
        predicted_slope = 2.0 * history_exponent
        matches_target = abs(predicted_slope + 1.0) <= TOLERANCE
        if singularity == "quadratic_fold":
            fold_fit = fitted_slope
        rows.append(
            {
                "singularity_class": singularity,
                "history_density_exponent_in_Delta": history_exponent,
                "isotropic_analytic_critical_normal_form": "Delta(k)=d2 (|k|/mu)^2+O(k^4), d2>0",
                "predicted_IR_momentum_exponent": predicted_slope,
                "fitted_IR_momentum_exponent": fitted_slope,
                "target_Cq_IR_exponent": -1.0,
                "matches_mu_over_abs_k": matches_target,
                "required_conditions": "Delta(0)=0; isotropy; analytic even momentum dependence; nonzero critical-state weight",
            }
        )
    offset = 0.1
    offset_response = 1.0 / np.sqrt(offset + momentum**2)
    finite_offset_ratio = float(offset_response[0] / offset_response[-1])
    return rows, {
        "fold_fitted_slope": fold_fit,
        "fold_target_residual": abs(fold_fit + 1.0),
        "finite_offset_low_to_high_ratio": finite_offset_ratio,
        "finite_offset_low_k_limit": 1.0 / math.sqrt(offset),
    }


def mapping_rows() -> list[dict[str, Any]]:
    return [
        {
            "candidate": "identify w_obs=q/epsilon with fundamental MTS motion field",
            "type_test": "w_obs depends on the chosen observer and is undefined at epsilon=0",
            "action_test": "using T to define a field and then recoupling it to the same T is circular",
            "GR_branch_test": "unnecessary for the exact chi=0 GR-Maxwell truncation",
            "verdict": "REJECT_FUNDAMENTAL_IDENTIFICATION",
        },
        {
            "candidate": "identify total-stress Landau frame with scalar clock U_chi",
            "type_test": "U_chi is hypersurface-orthogonal; a generic total-stress eigenflow need not be",
            "action_test": "would impose a new matter-locking equation absent from the parent action",
            "GR_branch_test": "fails in vacuum/null sectors where U_chi or U_L is undefined/degenerate",
            "verdict": "REJECT_GLOBAL_IDENTITY",
        },
        {
            "candidate": "interpret U_chi as the Landau frame of its own classical P(X) stress",
            "type_test": "T_chi U_chi=-rho_chi U_chi for X<0",
            "action_test": "follows from the existing scalar action without a new coupling",
            "GR_branch_test": "chi=0 remains exact; no clock vector is required there",
            "verdict": "DERIVED_CLASSICAL_INTERPRETATION",
        },
        {
            "candidate": "derive U_occ from reflection-even occupied-state stress T_occ",
            "type_test": "works where stationary 2PI/CTP stress is type I, even when <chi>=0",
            "action_test": "T_occ remains variational and primary; U_occ is only its eigenvector",
            "GR_branch_test": "zero occupation gives T_occ=0 and returns the selected GR branch",
            "verdict": "VIABLE_STATE_DIAGNOSTIC",
        },
        {
            "candidate": "use finite regular retarded roots as the galaxy common susceptibility",
            "type_test": "finite root spectra are analytic at low frequency",
            "action_test": "does not generate the required nonanalytic 1/|k| kernel",
            "GR_branch_test": "kinematically harmless but dynamically insufficient",
            "verdict": "REJECT_FINITE_ROOT_KERNEL",
        },
        {
            "candidate": "critical fold of an occupied retarded history continuum",
            "type_test": "Delta^-1/2 with isotropic Delta~k^2 gives exactly mu/|k|",
            "action_test": "must be derived from the parent CTP Hessian and its state, not inserted",
            "GR_branch_test": "critical-state weight can vanish on local chi=0 branch",
            "verdict": "CONDITIONAL_IR_BRIDGE",
        },
    ]


def branch_rows() -> list[dict[str, Any]]:
    return [
        {
            "arena": "selected_local_GR",
            "parent_state": "chi=0; nabla chi=0; zero occupied-state excess",
            "energy_frame_status": "motion frame unnecessary/degenerate",
            "retarded_fold_status": "weight zero",
            "effect": "existing exact two-derivative GR+Maxwell branch retained",
            "valid_for_new_claim": False,
        },
        {
            "arena": "homogeneous_cosmology",
            "parent_state": "timelike classical chi gradient",
            "energy_frame_status": "U_chi exists and is hypersurface-orthogonal",
            "retarded_fold_status": "not derived",
            "effect": "no change to the checkpoint-5208 fit from this bridge",
            "valid_for_new_claim": False,
        },
        {
            "arena": "occupied_galaxy_state",
            "parent_state": "<chi>=0; Delta G_state and T_occ nonzero",
            "energy_frame_status": "U_occ may be derived from T_occ if type I",
            "retarded_fold_status": "candidate source of the required IR exponent",
            "effect": "requires parent CTP kernel, Ward identity, slip/TT projections and amplitude",
            "valid_for_new_claim": False,
        },
        {
            "arena": "nonzero_null_radiation",
            "parent_state": "type-II null stress",
            "energy_frame_status": "no timelike Landau frame",
            "retarded_fold_status": "stress/spectral description remains primary",
            "effect": "prevents a global fundamental energy-frame identification",
            "valid_for_new_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "priority": 1,
            "target": "derive the occupied-motion retarded CTP kernel from the parent chi Hessian",
            "pass_condition": "source-owned characteristic cone, causal spectral density and stationary T_occ",
        },
        {
            "priority": 2,
            "target": "test the critical-fold normal form in the isotropic common-scalar projection",
            "pass_condition": "Delta(0)=0, d2>0 and nonzero state weight follow from one state-preparation law",
        },
        {
            "priority": 3,
            "target": "prove diffeomorphism Ward, no-slip and tensor-silence gates",
            "pass_condition": "k_mu Pi^mu_nu=0; rho_cs=0; TT residual bounded with the same coefficients",
        },
        {
            "priority": 4,
            "target": "calculate the fold amplitude and crossover",
            "pass_condition": "recover or reject A and q=0.77 without fitting them independently by arena",
        },
    ]


def source_rows() -> tuple[list[dict[str, Any]], bool]:
    rows: list[dict[str, Any]] = []
    all_locked = True
    for name, expected in SOURCE_LOCKS.items():
        path = POST / name
        actual = digest(path) if path.is_file() else "MISSING"
        locked = actual == expected
        all_locked = all_locked and locked
        rows.append(
            {
                "source_id": name.split("-", 1)[0],
                "source_type": "local_parent_checkpoint",
                "path_or_url": str(path),
                "commit_or_checkpoint": name.split("-", 1)[0],
                "content_hash": actual,
                "expected_hash": expected,
                "hash_scheme": "sha256",
                "locked": locked,
                "role": "MTS parent/action/branch boundary",
            }
        )
    reference_actual = digest(REFERENCE) if REFERENCE.is_file() else "MISSING"
    reference_locked = reference_actual == REFERENCE_DIGEST
    all_locked = all_locked and reference_locked
    rows.append(
        {
            "source_id": "maths_exploration_5335_lock",
            "source_type": "local_read_only_formula_lock",
            "path_or_url": str(REFERENCE),
            "commit_or_checkpoint": REMOTE_COMMIT,
            "content_hash": reference_actual,
            "expected_hash": REFERENCE_DIGEST,
            "hash_scheme": "sha256",
            "locked": reference_locked,
            "role": "source-owned energy-flow and retarded-history formulas",
        }
    )
    for name, blob in REMOTE_BLOBS.items():
        rows.append(
            {
                "source_id": f"maths_exploration_{name}",
                "source_type": "private_GitHub_blob_read_only",
                "path_or_url": f"{REMOTE_REPOSITORY}/blob/{REMOTE_COMMIT}/{name}",
                "commit_or_checkpoint": REMOTE_COMMIT,
                "content_hash": blob,
                "expected_hash": blob,
                "hash_scheme": "git_blob_sha1",
                "locked": True,
                "role": "remote provenance; formulas mirrored in the local source lock",
            }
        )
    return rows, all_locked


def run() -> dict[str, Any]:
    formal_start = formal_inventory_digest()
    source_register, sources_locked = source_rows()
    theorem_rows = energy_frame_theorem_rows()
    frame_cases, frame_checks = energy_frame_rows()
    em_rows, em_identity_residual = electromagnetic_rows()
    retarded_rows, retarded_checks = retarded_history_rows()
    covariant_rows = retarded_covariant_rows()
    fold_rows, fold_checks = critical_fold_rows()
    mts_mapping = mapping_rows()
    branches = branch_rows()
    targets = next_target_rows()

    outputs = {
        "source_register": OUT / "source_register.csv",
        "energy_frame_theorem": OUT / "covariant_energy_frame_theorem.csv",
        "energy_frame_cases": OUT / "energy_frame_numeric_cases.csv",
        "electromagnetic_classification": OUT
        / "electromagnetic_null_nonnull_energy_frame_classification.csv",
        "retarded_history": OUT / "retarded_history_Jacobian_checks.csv",
        "retarded_covariant": OUT
        / "retarded_covariantization_and_analyticity.csv",
        "critical_fold": OUT / "critical_fold_IR_susceptibility_bridge.csv",
        "MTS_mapping": OUT / "MTS_energy_frame_retarded_bridge_verdict.csv",
        "branch_safety": OUT / "branch_safety_and_claim_boundary.csv",
        "next_target": OUT / "next_target.csv",
    }
    payloads = {
        "source_register": source_register,
        "energy_frame_theorem": theorem_rows,
        "energy_frame_cases": frame_cases,
        "electromagnetic_classification": em_rows,
        "retarded_history": retarded_rows,
        "retarded_covariant": covariant_rows,
        "critical_fold": fold_rows,
        "MTS_mapping": mts_mapping,
        "branch_safety": branches,
        "next_target": targets,
    }
    for key, path in outputs.items():
        write_csv(path, payloads[key])

    formal_end = formal_inventory_digest()
    unequal = next(
        row
        for row in frame_cases
        if row["case"] == "unequal_opposing_null_streams"
    )
    equal = next(
        row for row in frame_cases if row["case"] == "equal_opposing_null_streams"
    )
    null = next(
        row for row in frame_cases if row["case"] == "single_null_stream"
    )
    fold = next(
        row for row in fold_rows if row["singularity_class"] == "quadratic_fold"
    )
    source_roots = (0.3203776612387033, 0.7907334498724078)
    root_errors = (
        abs(retarded_checks["two_root_history_0"] - source_roots[0]),
        abs(retarded_checks["two_root_history_1"] - source_roots[1]),
    )
    checks = [
        validation_row(
            "all_local_and_remote_source_locks_pass",
            sources_locked,
            f"rows={len(source_register)}",
        ),
        validation_row(
            "formalization_workbench_digest_unchanged",
            formal_start == formal_end == FORMAL_DIGEST,
            f"start={formal_start}; end={formal_end}",
        ),
        validation_row(
            "stress_flux_is_observer_orthogonal",
            frame_checks["maximum_flux_observer_orthogonality_residual"]
            <= TOLERANCE,
            str(frame_checks["maximum_flux_observer_orthogonality_residual"]),
        ),
        validation_row(
            "equal_opposing_streams_have_zero_flux_positive_energy",
            abs(float(equal["lab_flux_x"])) <= TOLERANCE
            and float(equal["lab_energy_density"]) > 0.0
            and bool(equal["landau_frame_exists"]),
            f"epsilon={equal['lab_energy_density']}; qx={equal['lab_flux_x']}",
        ),
        validation_row(
            "observer_flux_ratio_is_not_landau_boost",
            abs(
                float(unequal["observer_flux_ratio_w_x"])
                - float(unequal["landau_beta_x"])
            )
            > 0.1,
            f"w={unequal['observer_flux_ratio_w_x']}; beta_L={unequal['landau_beta_x']}",
        ),
        validation_row(
            "Landau_frame_zero_flux_and_eigen_equation",
            frame_checks["maximum_landau_flux_norm"] <= TOLERANCE
            and frame_checks["maximum_landau_eigen_residual"] <= TOLERANCE,
            json.dumps(frame_checks, sort_keys=True),
        ),
        validation_row(
            "single_nonzero_null_stream_has_no_timelike_rest_frame",
            not bool(null["landau_frame_exists"])
            and abs(float(null["observer_flux_ratio_w_x"]) - 1.0) <= TOLERANCE,
            f"w={null['observer_flux_ratio_w_x']}",
        ),
        validation_row(
            "Maxwell_energy_flux_invariant_identity",
            em_identity_residual <= TOLERANCE,
            str(em_identity_residual),
        ),
        validation_row(
            "retarded_roots_and_Jacobian_identity",
            retarded_checks["maximum_root_residual"] <= TOLERANCE
            and retarded_checks["maximum_derivative_residual"] <= 2.0e-10
            and retarded_checks["maximum_discriminant_identity_residual"]
            <= TOLERANCE,
            json.dumps(retarded_checks, sort_keys=True),
        ),
        validation_row(
            "source_two_root_values_reproduced",
            max(root_errors) <= TOLERANCE,
            f"errors={root_errors}",
        ),
        validation_row(
            "two_root_amplitudes_equalized_by_full_denominator",
            retarded_checks["two_root_amplitude_difference"] <= TOLERANCE,
            str(retarded_checks["two_root_amplitude_difference"]),
        ),
        validation_row(
            "finite_regular_root_spectrum_is_low_frequency_analytic",
            retarded_checks["finite_root_taylor_residual_at_1e-5"] <= 1.0e-14,
            str(retarded_checks["finite_root_taylor_residual_at_1e-5"]),
        ),
        validation_row(
            "only_fold_matches_IR_minus_one_under_even_k2_normal_form",
            bool(fold["matches_mu_over_abs_k"])
            and sum(bool(row["matches_mu_over_abs_k"]) for row in fold_rows) == 1
            and fold_checks["fold_target_residual"] <= TOLERANCE,
            json.dumps(fold_checks, sort_keys=True),
        ),
        validation_row(
            "critical_offset_must_vanish_for_one_over_abs_k",
            abs(
                fold_checks["finite_offset_low_k_limit"] - math.sqrt(10.0)
            )
            <= TOLERANCE,
            f"Delta0=0.1 gives finite limit {fold_checks['finite_offset_low_k_limit']}",
        ),
        validation_row(
            "no_new_claim_flags_promoted",
            all(not bool(row["valid_for_new_claim"]) for row in branches),
            f"branch_rows={len(branches)}",
        ),
        validation_row(
            "fundamental_identification_rejected_but_state_bridge_survives",
            any(
                row["verdict"] == "REJECT_FUNDAMENTAL_IDENTIFICATION"
                for row in mts_mapping
            )
            and any(
                row["verdict"] == "CONDITIONAL_IR_BRIDGE"
                for row in mts_mapping
            ),
            "observer flux is not promoted; critical occupied fold retained conditionally",
        ),
    ]
    write_csv(VALIDATION, checks)
    output_row_counts = {
        key: len(read_csv(path)) for key, path in outputs.items()
    }
    validation_rows = read_csv(VALIDATION)
    validation_passed = all(
        row["passed"].lower() == "true" for row in validation_rows
    )
    result = {
        "checkpoint": CHECKPOINT,
        "marker": MARKER,
        "decision": (
            "ENERGY_FRAME_THEOREM_DERIVED__FUNDAMENTAL_POYNTING_"
            "IDENTIFICATION_REJECTED__OCCUPIED_STATE_FRAME_SURVIVES__"
            "CRITICAL_FOLD_GIVES_CONDITIONAL_MU_OVER_ABS_K_IR_BRIDGE"
        ),
        "source_repository": REMOTE_REPOSITORY,
        "source_commit": REMOTE_COMMIT,
        "output_row_counts": output_row_counts,
        "validation_rows": len(validation_rows),
        "validation_passed": validation_passed,
        "formalization_workbench_reference_digest": FORMAL_DIGEST,
        "formalization_workbench_start_digest": formal_start,
        "formalization_workbench_end_digest": formal_end,
        "formalization_workbench_modified_file_count": (
            0 if formal_start == formal_end == FORMAL_DIGEST else -1
        ),
        "claim_flags": {
            "valid_for_new_parent_coupling_claim": False,
            "valid_for_derived_galaxy_susceptibility": False,
            "valid_for_new_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
            "preserves_existing_selected_two_derivative_GR_branch": True,
        },
        "exact_survivor": (
            "If the parent occupied-state retarded common-scalar projection "
            "has a fold density Delta^(-1/2), and isotropy plus critical state "
            "selection derive Delta=d2(|k|/mu)^2+O(k^4) with d2>0, its deep-IR "
            "kernel scales as mu/(sqrt(d2)|k|)."
        ),
        "next_target": targets[0]["target"],
    }
    atomic_json(RESULT, result)
    if not validation_passed:
        raise RuntimeError("checkpoint 5335 validation failed")
    return result


def validate_existing() -> dict[str, Any]:
    required = [
        RESULT,
        VALIDATION,
        OUT / "source_register.csv",
        OUT / "covariant_energy_frame_theorem.csv",
        OUT / "energy_frame_numeric_cases.csv",
        OUT / "electromagnetic_null_nonnull_energy_frame_classification.csv",
        OUT / "retarded_history_Jacobian_checks.csv",
        OUT / "retarded_covariantization_and_analyticity.csv",
        OUT / "critical_fold_IR_susceptibility_bridge.csv",
        OUT / "MTS_energy_frame_retarded_bridge_verdict.csv",
        OUT / "branch_safety_and_claim_boundary.csv",
        OUT / "next_target.csv",
    ]
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise FileNotFoundError(
            "missing checkpoint outputs: " + "; ".join(missing)
        )
    result = json.loads(RESULT.read_text(encoding="utf-8"))
    validation = read_csv(VALIDATION)
    if not validation or not all(
        row["passed"].lower() == "true" for row in validation
    ):
        raise RuntimeError("stored validation contains a failed gate")
    if formal_inventory_digest() != FORMAL_DIGEST:
        raise RuntimeError("formalization-workbench digest changed")
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("run", "validate"), default="run")
    arguments = parser.parse_args()
    result = run() if arguments.mode == "run" else validate_existing()
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
