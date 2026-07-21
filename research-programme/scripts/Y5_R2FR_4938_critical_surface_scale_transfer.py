from __future__ import annotations

import csv
import hashlib
import json
import math
import sys
from pathlib import Path
from typing import Any

import numpy as np
from scipy.integrate import solve_ivp

import Y5_R2FR_4934_completed_combined_flow as completed_flow


sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "functional_rg" / "4938"
OUTPUT = SOURCE_DIR / "critical_surface_scale_lock_results.json"
SPECTRUM_OUTPUT = SOURCE_DIR / "augmented_motion_stability_spectrum.csv"
TRANSFER_OUTPUT = SOURCE_DIR / "motion_scale_GR_transfer.csv"
BOUND_OUTPUT = SOURCE_DIR / "UV_scale_label_bound_translation.csv"

C3_SOLVER = POST / "scripts" / "Y5_R2FR_4933_c3_direct_threshold_solver.py"
COMBINED_4933 = POST / "scripts" / "Y5_R2FR_4933_combined_c3_photon_stability.py"
PHOTON_4933 = POST / "scripts" / "Y5_R2FR_4933_photon_flow_reproduction.py"
DIRECT_4934 = POST / "scripts" / "Y5_R2FR_4934_direct_c3_cff_principal.py"
COMPLETED_4934_SCRIPT = POST / "scripts" / "Y5_R2FR_4934_completed_combined_flow.py"
COMPLETED_4934 = POST / "source-intake" / "functional_rg" / "4934" / "completed_combined_flow_results.json"
TRAJECTORY_4935 = POST / "source-intake" / "functional_rg" / "4935" / "completed_fixed_point_trajectory_results.json"
FIXED_GATE_4937 = POST / "source-intake" / "functional_rg" / "4937" / "functional_potential_fixed_gate_results.json"
IDENTITY_4938 = SOURCE_DIR / "parent_scale_identity_audit_results.json"
MOTION_BOUNDS_4938 = SOURCE_DIR / "motion_scale_bound_translation.csv"

MARKER = "MTS_4938_CRITICAL_SURFACE_SCALE_TRANSFER"
EXPECTED_HASHES = {
    C3_SOLVER: "b0ff49318368f6b0b4f270603b364d14012462f2229e7bbb7858fe3b592f568a",
    COMBINED_4933: "5c80446a719d3820b5d08505c9c2d8b2e1389ec81266df2cdde60ca450a31df7",
    PHOTON_4933: "2858b5ea16085f2f5309ea7301d3a23b4868dd522905369e9ac3d95f2c9599d8",
    DIRECT_4934: "8299e6a2e6f53fc5da87ce8691602d7a3f7c77b08e8b7a48bd0c42f26a360fee",
    COMPLETED_4934_SCRIPT: "c5fded8ca210607972c5d12640cdfd3e88ea3de48f84d1b699a3b2a7e342e230",
    COMPLETED_4934: "c70583d03ec773fb31aca0cb0ac73e662c66c6146ee8bfcdeb07598ddfe43978",
    TRAJECTORY_4935: "8793e369ba0a9726c43dc64fe454ba87f88876832eca0ba9b79f07b171d1e222",
    FIXED_GATE_4937: "a965b75e5b5576e579bb4812b14a0e220a1b18b4e9653f4e83d714c4caf8a361",
    IDENTITY_4938: "24140234550056d98de373742073190154e432012451fec7a02b962e3a4dcb48",
    MOTION_BOUNDS_4938: "e62cabda4191eeae491d5f6849e8a5992eff1278b9b5286468dbfe15ff56e4bc",
}

SEED_AMPLITUDES = (1.0e-4, 3.0e-5, 1.0e-5, 3.0e-6, 1.0e-6)
IR_G_TARGET = 1.0e-10
T_IR_LIMIT = -40.0
R_UV_PROBE = 1.0e-12


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty table {path.name}")
    fieldnames: list[str] = []
    for row in rows:
        fieldnames.extend(key for key in row if key not in fieldnames)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def complex_rows(values: np.ndarray) -> list[dict[str, float]]:
    return [
        {"real": float(value.real), "imag": float(value.imag)} for value in values
    ]


def main() -> int:
    print(f"{MARKER}_START", flush=True)
    hash_failures = {
        path.as_posix(): {"expected": expected, "actual": digest(path) if path.exists() else "MISSING"}
        for path, expected in EXPECTED_HASHES.items()
        if not path.exists() or digest(path) != expected
    }
    if hash_failures:
        raise RuntimeError(f"critical-surface source hash mismatch: {hash_failures}")

    completed = json.loads(COMPLETED_4934.read_text(encoding="utf-8"))
    fixed = completed["source_complete_selected_row_fixed_point"]
    fixed_point = np.asarray(fixed["coordinates_g_gplus_gminus_gCFF_h"], dtype=float)
    gravity_stability = np.asarray(fixed["stability_matrix"], dtype=float)
    gravity_eigenvalues, gravity_eigenvectors = np.linalg.eig(gravity_stability)
    gravity_relevant_indices = [
        index for index, value in enumerate(gravity_eigenvalues) if value.real < 0.0
    ]
    if len(gravity_relevant_indices) != 1:
        raise RuntimeError(
            f"expected one minimal gravity relevant direction, found {gravity_relevant_indices}"
        )
    gravity_relevant_index = gravity_relevant_indices[0]
    theta_gravity = -float(gravity_eigenvalues[gravity_relevant_index].real)
    gravity_vector = np.real(gravity_eigenvectors[:, gravity_relevant_index])
    if gravity_vector[0] < 0.0:
        gravity_vector *= -1.0
    gravity_vector /= float(np.max(np.abs(gravity_vector / fixed_point)))

    fixed_gate = json.loads(FIXED_GATE_4937.read_text(encoding="utf-8"))
    low_source_root = next(
        row
        for row in fixed_gate["constant_root_decision"]["roots"][
            "source_diagonal_calibrated"
        ]
        if row["branch"] == "low"
    )
    mes_rows = fixed_gate["minimal_essential_sign_robustness"]
    mass_variants = {
        "source_calibrated_low_root": float(low_source_root["theta_mass_n2"]),
        **{
            row["mapping"]: float(row["theta_mass_n2"]) for row in mes_rows
        },
    }

    g_fixed = float(fixed_point[0])
    known_newton_threshold_column = np.zeros(5, dtype=float)
    known_newton_threshold_column[0] = -g_fixed**2 / (6.0 * math.pi)
    spectrum_rows: list[dict[str, Any]] = []
    augmented_summaries: dict[str, Any] = {}
    for variant, theta_mass in mass_variants.items():
        lambda_mass = -theta_mass
        augmented = np.zeros((6, 6), dtype=float)
        augmented[:5, :5] = gravity_stability
        augmented[:5, 5] = known_newton_threshold_column
        augmented[5, 5] = lambda_mass
        augmented_values = np.linalg.eigvals(augmented)
        expected_values = np.concatenate(
            [gravity_eigenvalues, np.array([lambda_mass], dtype=complex)]
        )
        unmatched = list(augmented_values)
        union_errors = []
        for expected in expected_values:
            closest_index = min(
                range(len(unmatched)), key=lambda index: abs(unmatched[index] - expected)
            )
            union_errors.append(abs(unmatched.pop(closest_index) - expected))
        gravity_response = -np.linalg.solve(
            gravity_stability - lambda_mass * np.eye(5),
            known_newton_threshold_column,
        )
        response_residual = np.linalg.norm(
            (gravity_stability - lambda_mass * np.eye(5)) @ gravity_response
            + known_newton_threshold_column,
            ord=np.inf,
        )
        sorted_values = sorted(
            augmented_values, key=lambda value: (value.real, value.imag)
        )
        for mode_index, value in enumerate(sorted_values):
            spectrum_rows.append(
                {
                    "mass_variant": variant,
                    "mode_index": mode_index,
                    "beta_eigenvalue_real": float(value.real),
                    "beta_eigenvalue_imag": float(value.imag),
                    "critical_exponent_real": float(-value.real),
                    "critical_exponent_imag": float(-value.imag),
                    "relevant": bool(value.real < 0.0),
                    "motion_mass_mode": abs(value - lambda_mass) < 1.0e-8,
                    "known_threshold_column_scope": "Newton component only; arbitrary upper-right columns leave the block-triangular eigenvalue union unchanged",
                    "valid_for_full_MTS_claim": False,
                    "checkpoint_marker": MARKER,
                }
            )
        augmented_summaries[variant] = {
            "theta_mass": theta_mass,
            "lambda_mass": lambda_mass,
            "theta_mass_over_theta_gravity": theta_mass / theta_gravity,
            "known_d_beta_g_d_w_at_zero": float(
                known_newton_threshold_column[0]
            ),
            "gravity_response_to_unit_mass_mode_known_column": gravity_response.tolist(),
            "response_solve_condition_number": float(
                np.linalg.cond(gravity_stability - lambda_mass * np.eye(5))
            ),
            "response_residual_infinity_norm": float(response_residual),
            "augmented_eigenvalues": complex_rows(augmented_values),
            "relevant_directions": int(
                sum(value.real < 0.0 for value in augmented_values)
            ),
            "eigenvalue_union_max_error": float(max(union_errors)),
        }

    _, _, beta, _, _, _ = completed_flow.build_completed_solver()

    mes_transfer_variants = {
        row["mapping"]: {
            "theta_mass": float(row["theta_mass_n2"]),
            "v_sign": 1.0 if row["v_value"] > 0.0 else -1.0,
        }
        for row in mes_rows
    }

    def gravity_anomalous_dimension(g_value: float, v_sign: float) -> float:
        dimensionless_planck = 1.0 / (16.0 * math.pi * g_value)
        v_value = v_sign * 3.0 * g_value / (8.0 * math.pi)
        return 1.0 / (96.0 * math.pi**2 * dimensionless_planck) * (
            20.0 / (1.0 - v_value) ** 2
            + 1.0 / (1.0 - v_value / 4.0) ** 2
        )

    transfer_rows: list[dict[str, Any]] = []
    for relative_amplitude in SEED_AMPLITUDES:
        initial_gravity = fixed_point - relative_amplitude * gravity_vector

        def right_hand_side(_time: float, state: np.ndarray) -> np.ndarray:
            gravity_point = state[:5]
            gravity_beta = beta(gravity_point)
            if not np.all(np.isfinite(gravity_beta)):
                raise FloatingPointError("nonfinite completed gravity beta")
            g_value = float(gravity_point[0])
            log_derivatives = [
                -2.0
                + gravity_anomalous_dimension(g_value, variant["v_sign"])
                for variant in mes_transfer_variants.values()
            ]
            return np.concatenate([gravity_beta, np.asarray(log_derivatives)])

        def infrared_event(_time: float, state: np.ndarray) -> float:
            return float(state[0] - IR_G_TARGET)

        infrared_event.terminal = True
        infrared_event.direction = -1

        initial_state = np.concatenate(
            [initial_gravity, np.zeros(len(mes_transfer_variants), dtype=float)]
        )
        solution = solve_ivp(
            right_hand_side,
            (0.0, T_IR_LIMIT),
            initial_state,
            method="DOP853",
            rtol=2.0e-9,
            atol=np.array(
                [1.0e-13, 1.0e-15, 1.0e-15, 1.0e-16, 1.0e-19, 1.0e-11, 1.0e-11]
            ),
            max_step=0.08,
            events=infrared_event,
        )
        termination = (
            "IR_G_TARGET" if len(solution.t_events[0]) else "INTEGRATOR_FAILURE"
        )
        if not solution.success or termination != "IR_G_TARGET":
            raise RuntimeError(
                f"scale transfer failed for seed {relative_amplitude}: {solution.message}"
            )
        endpoint_g = float(solution.y[0, -1])
        for transfer_index, (mapping, variant) in enumerate(
            mes_transfer_variants.items()
        ):
            theta_mass = variant["theta_mass"]
            uv_power = theta_mass / theta_gravity
            log_transfer = float(solution.y[5 + transfer_index, -1])
            w_seed = R_UV_PROBE * relative_amplitude**uv_power
            w_endpoint = w_seed * math.exp(log_transfer)
            j_endpoint = w_endpoint * endpoint_g
            transfer_jacobian = j_endpoint / R_UV_PROBE
            transfer_rows.append(
                {
                    "mapping": mapping,
                    "relative_gravity_seed": relative_amplitude,
                    "theta_gravity": theta_gravity,
                    "theta_mass": theta_mass,
                    "uv_power_theta_mass_over_theta_gravity": uv_power,
                    "R_UV_probe": R_UV_PROBE,
                    "w_seed": w_seed,
                    "t_endpoint": float(solution.t[-1]),
                    "g_endpoint": endpoint_g,
                    "log_linear_mass_transfer": log_transfer,
                    "w_endpoint_linear_probe": w_endpoint,
                    "D_psi_endpoint": 1.0 / (1.0 + w_endpoint),
                    "J_gap_endpoint": j_endpoint,
                    "K_J_equals_J_endpoint_over_R_UV": transfer_jacobian,
                    "termination": termination,
                    "interpretation": "infinitesimal spectator derivative on the 4935 separatrix; K depends on the declared relevant-vector normalization and is not a scale prediction",
                    "valid_for_full_MTS_claim": False,
                    "checkpoint_marker": MARKER,
                }
            )

    transfer_summaries: dict[str, Any] = {}
    for mapping in mes_transfer_variants:
        rows = [row for row in transfer_rows if row["mapping"] == mapping]
        values = np.asarray(
            [row["K_J_equals_J_endpoint_over_R_UV"] for row in rows], dtype=float
        )
        reference = float(values[-1])
        transfer_summaries[mapping] = {
            "K_values": values.tolist(),
            "smallest_seed_reference": reference,
            "max_relative_difference": float(
                np.max(np.abs(values - reference)) / abs(reference)
            ),
            "sqrt_K_reference": math.sqrt(reference),
            "interpretation": "J_gap_IR=K R_UV to first order in the convention-normalized independent motion amplitude",
        }

    bound_rows = read_csv(MOTION_BOUNDS_4938)
    uv_bound_rows: list[dict[str, Any]] = []
    for mapping, summary in transfer_summaries.items():
        transfer_reference = float(summary["smallest_seed_reference"])
        for bound in bound_rows:
            j_floor = float(bound["J_gap_floor"])
            uv_bound_rows.append(
                {
                    "mapping": mapping,
                    "mass_profile": bound["profile"],
                    "J_gap_floor": j_floor,
                    "K_reference": transfer_reference,
                    "R_UV_floor_in_declared_eigenvector_normalization": j_floor
                    / transfer_reference,
                    "log10_R_UV_floor": math.log10(
                        j_floor / transfer_reference
                    ),
                    "status": "CONDITIONAL_COMPACT_FLOOR_TRANSFER_NONCLAIM",
                    "valid_for_full_MTS_claim": False,
                    "checkpoint_marker": MARKER,
                }
            )

    identity = json.loads(IDENTITY_4938.read_text(encoding="utf-8"))
    checks = {
        "one_minimal_gravity_relevant_direction": len(gravity_relevant_indices) == 1,
        "known_Newton_threshold_derivative_nonzero": known_newton_threshold_column[0]
        < 0.0,
        "all_augmented_spectra_have_two_relevant_directions": all(
            row["relevant_directions"] == 2
            for row in augmented_summaries.values()
        ),
        "block_triangular_eigenvalue_union_numeric": all(
            row["eigenvalue_union_max_error"] < 1.0e-10
            for row in augmented_summaries.values()
        ),
        "motion_gravity_response_solve_is_accurate": all(
            row["response_residual_infinity_norm"] < 1.0e-12
            for row in augmented_summaries.values()
        ),
        "all_transfer_runs_reach_IR": all(
            row["termination"] == "IR_G_TARGET" for row in transfer_rows
        ),
        "linear_probe_remains_small": max(
            row["w_endpoint_linear_probe"] for row in transfer_rows
        )
        < 0.01,
        "both_sign_transfer_jacobians_seed_converge": all(
            row["max_relative_difference"] < 1.0e-4
            for row in transfer_summaries.values()
        ),
        "UV_bound_translation_positive": all(
            row["R_UV_floor_in_declared_eigenvector_normalization"] > 0.0
            for row in uv_bound_rows
        ),
        "parent_identity_audit_selected_two_scale": identity[
            "candidate_decision"
        ]["selected"]
        == "explicit_two_scale_parent",
    }
    checks = {name: bool(value) for name, value in checks.items()}
    if not all(checks.values()):
        raise RuntimeError(f"critical-surface scale transfer checks failed: {checks}")

    result = {
        "marker": MARKER,
        "source_hashes": {
            path.relative_to(ROOT).as_posix(): expected
            for path, expected in EXPECTED_HASHES.items()
        },
        "physical_scale_beta": {
            "J_gap": "w_psi g=m_gap^2 G_N=c_m^2 I_M^(3/4)",
            "exact_log_beta": "beta_J/J=beta_w/w+beta_g/g",
            "Gaussian_limit": "beta_w/w=-2 and beta_g/g=+2 imply beta_J=0",
            "UV_regular_mass_linearization": "beta_delta_w=-theta_mass delta_w",
            "fractional_warning": "beta_I cannot be represented by a single fractional coupling at the interacting point because checkpoint 4936 proved that family is not RG closed",
        },
        "block_triangular_theorem": {
            "matrix": "B_aug=[[B_gravity,c],[0,-theta_mass]]",
            "determinant": "det(zI-B_aug)=det(zI-B_gravity)(z+theta_mass) for arbitrary upper-right c",
            "reason_for_lower_left_zero": "about the constant motion fixed point the mass beta is proportional to the mass perturbation; changing a field-independent gravity coordinate does not add a phi^2 operator at zero mass",
            "known_threshold_column": known_newton_threshold_column.tolist(),
            "known_Newton_component": "d[g^2/(6pi(1+w))]/dw|w=0=-g_*^2/(6pi)",
            "gravity_critical_exponent": theta_gravity,
            "variants": augmented_summaries,
            "decision": "threshold backreaction can rotate the motion eigenvector into gravity but cannot remove its independent relevant eigenvalue in the unchanged minimal block",
        },
        "UV_trajectory_label": {
            "gravity_amplitude": "epsilon in the 4935 relative-unit eigenvector convention",
            "motion_amplitude": "delta w_seed",
            "invariant_label": "R_UV=delta w_seed/epsilon^(theta_mass/theta_gravity)",
            "status": "independent arbitrary critical-surface coordinate",
            "one_scale_requirement": "a parent boundary condition must select one R_UV; no current owner does",
        },
        "GR_separatrix_transfer": {
            "probe": R_UV_PROBE,
            "seed_amplitudes": list(SEED_AMPLITUDES),
            "summaries": transfer_summaries,
            "boundary": "spectator linear response on the unchanged 4935 gravity branch; it is not the fully backreacted motion trajectory",
        },
        "compact_floor_transfer": uv_bound_rows,
        "decision": {
            "critical_surface_fixes_motion_scale": False,
            "two_relevant_directions": True,
            "GR_transfer_function_derived": True,
            "GR_transfer_selects_value": False,
            "explicit_two_scale_parent_required": True,
        },
        "checks": checks,
        "claim_boundary": {
            "coupled_scale_ratio_beta_derived": True,
            "block_triangular_relevance_theorem_derived": True,
            "known_threshold_rotation_calculated": True,
            "linear_GR_transfer_calculated": True,
            "motion_scale_selected": False,
            "fully_backreacted_motion_trajectory": False,
            "full_MTS_fixed_point": False,
            "local_GR_Newton_Maxwell_promoted": False,
        },
    }

    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    write_csv(SPECTRUM_OUTPUT, spectrum_rows)
    write_csv(TRANSFER_OUTPUT, transfer_rows)
    write_csv(BOUND_OUTPUT, uv_bound_rows)
    print(f"{MARKER}_OUTPUT_SHA256={digest(OUTPUT)}", flush=True)
    print(f"{MARKER}_SPECTRUM_SHA256={digest(SPECTRUM_OUTPUT)}", flush=True)
    print(f"{MARKER}_TRANSFER_SHA256={digest(TRANSFER_OUTPUT)}", flush=True)
    print(f"{MARKER}_BOUNDS_SHA256={digest(BOUND_OUTPUT)}", flush=True)
    for mapping, summary in transfer_summaries.items():
        print(
            f"{MARKER}_K_{mapping}={summary['smallest_seed_reference']:.12g}",
            flush=True,
        )
    print(f"{MARKER}_RELEVANT_DIRECTIONS=2", flush=True)
    print(f"{MARKER}_PASS", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
