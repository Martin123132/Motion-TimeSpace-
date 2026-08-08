from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import sys
import time
from pathlib import Path
from typing import Any

import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq

import Y5_R2FR_4911_full_offshell_a6_template_projector as checkpoint_4911
import Y5_R2FR_4912_free_lattice_multigeometry_continuum_projector as checkpoint_4912


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
SOURCE = POST / "source-intake" / "functional_rg" / "4975"
RESIDUALS = POST / "source-intake" / "mts_residuals"

SOURCE_4911_SCRIPT = POST / "scripts" / "Y5_R2FR_4911_full_offshell_a6_template_projector.py"
SOURCE_4912_SCRIPT = POST / "scripts" / "Y5_R2FR_4912_free_lattice_multigeometry_continuum_projector.py"
SOURCE_4974_DOC = POST / "4974-Y5-R2FR-C3-third-response-topology-correction-and-free-scalar-proper-time-kernel.md"
SOURCE_4974_RESULT = SOURCE.parent / "4974" / "C3_three_response_topology_and_scalar_PT_kernel_results.json"
SOURCE_4974_VALIDATION = RESIDUALS / "P8_Y5_BRR545_4974_VALIDATION.csv"

RESPONSES_CSV = SOURCE / "C3_scalar_q6_q8_Taylor_responses.csv"
PROJECTION_CSV = SOURCE / "C3_scalar_q6_q8_quotient_projection.csv"
LEAVE_ONE_CSV = SOURCE / "C3_scalar_q8_leave_one_geometry.csv"
MASS_SCALING_CSV = SOURCE / "C3_scalar_mass_homogeneity.csv"
KERNEL_CSV = SOURCE / "C3_scalar_PT_m3_q6_q8_kernel.csv"
GATE_CSV = SOURCE / "C3_scalar_finite_momentum_germ_gate.csv"
RESULT_JSON = SOURCE / "C3_scalar_finite_momentum_germ_and_PT_kernel_results.json"
PROVENANCE = SOURCE / "PROVENANCE.md"

MARKER = "MTS_4975_SCALAR_FINITE_MOMENTUM_GERM_AND_PT_KERNEL"
CHECKED_DATE = "2026-07-13"
TARGET_C3 = 1.0 / (30240.0 * (4.0 * math.pi) ** 2)

EXPECTED_HASHES = {
    SOURCE_4911_SCRIPT: "a99e64b66812fb6e17e1c89fc7acd7c7cb8e750799f629f0c1e07f16796e694f",
    SOURCE_4912_SCRIPT: "8edae30d1df642d711a67add28ca07527f8502f4e317d27ab2292f7c27518c28",
    SOURCE_4974_DOC: "deaa72583f38071b6b2872e8d1d88d27a226246ffae6f1daa722d8ee54ca7454",
    SOURCE_4974_RESULT: "304a653025489903121d7f640f57cf5330c7b43dec8b01087193d65698a44990",
    SOURCE_4974_VALIDATION: "7b612b3cbf282c092060cc47f51c42bfcfc6524c6c2e0954ed552c4cd318064f",
}


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty CSV: {path}")
    fields: list[str] = []
    for row in rows:
        fields.extend(key for key in row if key not in fields)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def tagged(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            **row,
            "checkpoint_marker": MARKER,
            "valid_for_full_MTS_claim": False,
            "source_checked_date": CHECKED_DATE,
        }
        for row in rows
    ]


def cosine_coefficient(series: np.ndarray, phases: np.ndarray, order: int) -> float:
    phase = np.exp(1j * float(np.sum(phases)))
    return 0.25 * float(np.real(phase * series[order]))


def sigma_one(source: dict[str, Any]) -> float:
    return float(sum(momentum @ momentum for momentum in source["momenta"]))


def run_response_config(
    label: str,
    radial_order: int,
    angular_order: int,
    mass: float,
    ensemble: list[dict[str, Any]],
    matrix: np.ndarray,
) -> dict[str, Any]:
    q6 = np.zeros(len(ensemble), dtype=float)
    q8 = np.zeros(len(ensemble), dtype=float)
    inverse_residual = 0.0
    elapsed_rows: list[float] = []
    for index, source in enumerate(ensemble):
        started = time.perf_counter()
        series, residual = checkpoint_4912.complex_TTT_continuum_series_density(
            source["momenta"],
            source["polarizations"],
            mass,
            radial_order,
            angular_order,
        )
        q6[index] = cosine_coefficient(series, source["phases"], 6)
        q8[index] = cosine_coefficient(series, source["phases"], 8)
        inverse_residual = max(inverse_residual, residual)
        elapsed_rows.append(time.perf_counter() - started)
        print(
            f"4975 {label} {source['geometry_id']} {index + 1}/{len(ensemble)}",
            flush=True,
        )

    sigma = np.asarray([sigma_one(source) for source in ensemble])
    q8_matrix = sigma[:, np.newaxis] * matrix
    q6_recovery = checkpoint_4912.quotient_recovery(matrix, q6)
    q8_recovery = checkpoint_4912.quotient_recovery(q8_matrix, q8)
    return {
        "label": label,
        "radial_order": radial_order,
        "angular_order": angular_order,
        "mass": mass,
        "sigma1": sigma,
        "q6": q6,
        "q8": q8,
        "q8_matrix": q8_matrix,
        "q6_recovery": q6_recovery,
        "q8_recovery": q8_recovery,
        "maximum_inverse_residual": inverse_residual,
        "elapsed_rows": elapsed_rows,
    }


def response_rows(
    results: list[dict[str, Any]], ensemble: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for result in results:
        q6_reconstructed = result["q6_recovery"]["reconstructed"]
        q8_reconstructed = result["q8_recovery"]["reconstructed"]
        for index, source in enumerate(ensemble):
            rows.append(
                {
                    "config": result["label"],
                    "geometry_id": source["geometry_id"],
                    "mass": result["mass"],
                    "radial_order": result["radial_order"],
                    "angular_order": result["angular_order"],
                    "sigma1_external": result["sigma1"][index],
                    "q6_response": result["q6"][index],
                    "q6_rank8_reconstructed": q6_reconstructed[index],
                    "q6_absolute_residual": result["q6"][index] - q6_reconstructed[index],
                    "q8_response": result["q8"][index],
                    "q8_sigma1_rank8_reconstructed": q8_reconstructed[index],
                    "q8_leakage": result["q8"][index] - q8_reconstructed[index],
                    "elapsed_seconds": result["elapsed_rows"][index],
                    "status": "Q6_EXACT_LOCAL_IMAGE_Q8_TESTED_AGAINST_FIRST_SYMMETRIC_DRESSING",
                }
            )
    return tagged(rows)


def projection_rows(results: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for result in results:
        q6 = result["q6_recovery"]
        q8 = result["q8_recovery"]
        rows.append(
            {
                "config": result["label"],
                "mass": result["mass"],
                "radial_order": result["radial_order"],
                "angular_order": result["angular_order"],
                "q6_relative_image_residual": q6["response_residual"],
                "q6_zeta": q6["zeta"],
                "q6_m2_zeta_over_exact_C3": q6["zeta"] * result["mass"] ** 2 / TARGET_C3,
                "q8_relative_sigma1_image_residual": q8["response_residual"],
                "q8_projected_channel_estimator": q8["zeta"],
                "q8_m4_projected_channel_estimator": q8["zeta"] * result["mass"] ** 4,
                "maximum_propagator_inverse_residual": result["maximum_inverse_residual"],
                "q8_interpretation": "least_squares_first_symmetric_C3_form_factor_channel_only_not_unique_full_dimension8_operator_coefficient",
                "pure_C3_form_factor_derivative_identified": False,
                "status": "Q6_PASS_Q8_PURE_C3_DERIVATIVE_REJECTED_IF_LEAKAGE_NONZERO",
            }
        )
    return tagged(rows)


def leave_one_rows(
    selected: dict[str, Any], geometry_ids: list[str]
) -> tuple[list[dict[str, Any]], dict[str, float]]:
    matrix = selected["q8_matrix"]
    response = selected["q8"]
    full_zeta = float(selected["q8_recovery"]["zeta"])
    rows: list[dict[str, Any]] = []
    zetas: list[float] = []
    heldout_relative: list[float] = []
    response_scale = max(float(np.linalg.norm(response)), 1.0e-30)
    for omitted, geometry_id in enumerate(geometry_ids):
        reduced = checkpoint_4912.quotient_recovery(
            np.delete(matrix, omitted, axis=0),
            np.delete(response, omitted),
        )
        predicted = float(matrix[omitted] @ reduced["coefficients"])
        heldout = abs(predicted - response[omitted]) / response_scale
        zetas.append(float(reduced["zeta"]))
        heldout_relative.append(heldout)
        rows.append(
            {
                "config": selected["label"],
                "omitted_geometry_id": geometry_id,
                "fit_relative_residual": reduced["response_residual"],
                "heldout_observed": response[omitted],
                "heldout_predicted": predicted,
                "heldout_residual_over_full_response_norm": heldout,
                "q8_projected_channel_estimator": reduced["zeta"],
                "relative_shift_from_full_estimator": abs(reduced["zeta"] - full_zeta) / max(abs(full_zeta), 1.0e-30),
                "pure_C3_form_factor_derivative_identified": False,
                "status": "ENSEMBLE_STABILITY_DIAGNOSTIC_NOT_A_CLAIM",
            }
        )
    return tagged(rows), {
        "minimum_zeta": min(zetas),
        "maximum_zeta": max(zetas),
        "maximum_relative_zeta_shift": max(
            abs(value - full_zeta) / max(abs(full_zeta), 1.0e-30) for value in zetas
        ),
        "maximum_heldout_residual_over_full_norm": max(heldout_relative),
    }


def mass_homogeneity_rows(
    ensemble: list[dict[str, Any]], radial_order: int, angular_order: int
) -> tuple[list[dict[str, Any]], float]:
    rows: list[dict[str, Any]] = []
    maximum_residual = 0.0
    for source in ensemble[:3]:
        values: dict[float, dict[int, float]] = {}
        for mass in (1.0, 2.0):
            series, _ = checkpoint_4912.complex_TTT_continuum_series_density(
                source["momenta"],
                source["polarizations"],
                mass,
                radial_order,
                angular_order,
            )
            values[mass] = {
                order: cosine_coefficient(series, source["phases"], order)
                for order in (6, 8)
            }
        for order in (6, 8):
            expected_power = 4 - order
            scaled_ratio = values[2.0][order] / values[1.0][order] / (2.0 ** expected_power)
            residual = abs(scaled_ratio - 1.0)
            maximum_residual = max(maximum_residual, residual)
            rows.append(
                {
                    "geometry_id": source["geometry_id"],
                    "Taylor_order": order,
                    "dimension_power_of_mass": expected_power,
                    "coefficient_m1": values[1.0][order],
                    "coefficient_m2": values[2.0][order],
                    "observed_over_expected_scaling": scaled_ratio,
                    "absolute_scaling_residual": residual,
                    "analytic_change_of_variables": "p=m*l implies a_n(m)=m^(4-n)a_n(1)",
                    "status": "ANALYTIC_DIMENSIONAL_SCALING_NUMERICALLY_SPOTCHECKED",
                }
            )
    return tagged(rows), maximum_residual


def normalized_kernel(order: int, x_value: float) -> float:
    power = 2.0 - order / 2.0
    falling = power * (power - 1.0) * (power - 2.0)
    return falling * x_value**3 / (1.0 + x_value) ** (3.0 - power)


def cumulative_kernel(order: int, x_value: float) -> float:
    if order == 6:
        return (x_value / (1.0 + x_value)) ** 3
    if order == 8:
        return x_value**3 * (x_value + 4.0) / (1.0 + x_value) ** 4
    raise ValueError(f"unsupported order: {order}")


def kernel_rows(q6_coefficient: float, q8_estimator: float) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    x_values = (1.0e-8, 1.0e-6, 1.0e-4, 1.0e-2, 0.1, 0.3, 1.0, 1.5, 3.0, 10.0, 100.0, 1.0e4, 1.0e8)
    for x_value in x_values:
        q6_kernel = normalized_kernel(6, x_value)
        q8_kernel = normalized_kernel(8, x_value)
        rows.append(
            {
                "x_equals_3k2_over_m2": x_value,
                "k_over_m": math.sqrt(x_value / 3.0),
                "q6_normalized_dcoefficient_dlnk": q6_kernel,
                "q6_actual_dcoefficient_dlnk_m1": q6_coefficient * q6_kernel,
                "q6_cumulative_UV_to_IR_fraction": cumulative_kernel(6, x_value),
                "q8_normalized_dchannel_dlnk": q8_kernel,
                "q8_projected_channel_dlnk_m1": q8_estimator * q8_kernel,
                "q8_cumulative_UV_to_IR_fraction": cumulative_kernel(8, x_value),
                "q8_scope": "projected_first_symmetric_channel_with_nonzero_dimension8_leakage",
                "status": "EXACT_PT_M3_KERNEL_FOR_EACH_HOMOGENEOUS_TAYLOR_COMPONENT",
            }
        )

    integrals: dict[int, float] = {}
    half_points: dict[int, float] = {}
    for order in (6, 8):
        integrals[order] = quad(
            lambda value: -normalized_kernel(order, value) / (2.0 * value),
            0.0,
            np.inf,
            epsabs=1.0e-13,
            epsrel=1.0e-13,
            limit=300,
        )[0]
        half_points[order] = brentq(
            lambda value: cumulative_kernel(order, value) - 0.5,
            1.0e-12,
            1.0e4,
        )
    summary = {
        "q6_normalized_kernel": "-6*x^3/(1+x)^4",
        "q8_normalized_kernel": "-24*x^3/(1+x)^5",
        "q6_cumulative": "x^3/(1+x)^3",
        "q8_cumulative": "x^3*(x+4)/(1+x)^4",
        "q6_integral": integrals[6],
        "q8_integral": integrals[8],
        "q6_half_x": half_points[6],
        "q8_half_x": half_points[8],
        "q6_peak_x": 3.0,
        "q6_peak_value": -81.0 / 128.0,
        "q8_peak_x": 1.5,
        "q8_peak_value": -2592.0 / 3125.0,
        "operator_identity": "K_n=(3k^2)^3 partial_(M^2)^3[A_n(M^2)^(2-n/2)] at M^2=m^2+3k^2",
    }
    return tagged(rows), summary


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", choices=("smoke", "checkpoint"), default="checkpoint")
    arguments = parser.parse_args()
    started = time.perf_counter()
    print(f"{MARKER}_START profile={arguments.profile}", flush=True)
    SOURCE.mkdir(parents=True, exist_ok=True)

    observed_hashes = {path: digest(path) for path in EXPECTED_HASHES}
    source_hash_pass = all(observed_hashes[path] == expected for path, expected in EXPECTED_HASHES.items())

    checkpoint_4912.SERIES_ORDER = 8
    geometry_ids, matrix = checkpoint_4912.load_geometric_matrix()
    ensemble = checkpoint_4911.random_source_ensemble(len(geometry_ids))
    if [source["geometry_id"] for source in ensemble] != geometry_ids:
        raise RuntimeError("4911 ensemble order no longer matches the persisted template matrix")

    radial_order = 12 if arguments.profile == "smoke" else 24
    angular_orders = (8, 10)
    results = [
        run_response_config(
            f"R{radial_order}_A{angular_order}_m1",
            radial_order,
            angular_order,
            1.0,
            ensemble,
            matrix,
        )
        for angular_order in angular_orders
    ]
    selected = results[-1]

    q6_analysis = checkpoint_4911.matrix_analysis(matrix)
    q8_analysis = checkpoint_4911.matrix_analysis(selected["q8_matrix"])
    q6_null_map = float(np.max(np.abs(q6_analysis["nullspace"] @ checkpoint_4911.RICCI_FLAT_C3_MAP)))
    q8_null_map = float(np.max(np.abs(q8_analysis["nullspace"] @ checkpoint_4911.RICCI_FLAT_C3_MAP)))

    responses = response_rows(results, ensemble)
    projections = projection_rows(results)
    leave_one, leave_one_summary = leave_one_rows(selected, geometry_ids)
    mass_rows, mass_scaling_residual = mass_homogeneity_rows(ensemble, 12, 6)
    kernel, kernel_summary = kernel_rows(
        float(selected["q6_recovery"]["zeta"]),
        float(selected["q8_recovery"]["zeta"]),
    )

    q8_vector_convergence = float(
        np.linalg.norm(results[0]["q8"] - results[1]["q8"])
        / max(np.linalg.norm(results[1]["q8"]), 1.0e-30)
    )
    q8_estimator_convergence = abs(
        results[0]["q8_recovery"]["zeta"] - results[1]["q8_recovery"]["zeta"]
    ) / max(abs(results[1]["q8_recovery"]["zeta"]), 1.0e-30)
    q8_leakage = float(selected["q8_recovery"]["response_residual"])
    q6_target_residual = abs(
        selected["q6_recovery"]["zeta"] / TARGET_C3 - 1.0
    )

    gates = [
        {
            "gate": "source_hash_lock",
            "observed": source_hash_pass,
            "required": True,
            "passed": source_hash_pass,
            "interpretation": "all predecessor scripts documents results and validation remain hash locked",
        },
        {
            "gate": "q6_exact_recovery_control",
            "observed": f"image_residual={selected['q6_recovery']['response_residual']:.17g};target_residual={q6_target_residual:.17g}",
            "required": "both <1e-8",
            "passed": selected["q6_recovery"]["response_residual"] < 1.0e-8 and q6_target_residual < 1.0e-8,
            "interpretation": "the known local C3 coefficient is independently recovered before reading q8",
        },
        {
            "gate": "q8_quadrature_convergence",
            "observed": f"vector={q8_vector_convergence:.17g};estimator={q8_estimator_convergence:.17g}",
            "required": "both <1e-8",
            "passed": q8_vector_convergence < 1.0e-8 and q8_estimator_convergence < 1.0e-8,
            "interpretation": "q8 leakage is not an angular quadrature artifact",
        },
        {
            "gate": "q8_extra_operator_detection",
            "observed": q8_leakage,
            "required": "finite and >1e-6",
            "passed": math.isfinite(q8_leakage) and q8_leakage > 1.0e-6,
            "interpretation": "the first sigma1-dressed local quotient does not span the full dimension-eight response",
        },
        {
            "gate": "quotient_rank_and_C3_null_invariance",
            "observed": f"rank6={q6_analysis['rank']};rank8={q8_analysis['rank']};null6={q6_null_map:.17g};null8={q8_null_map:.17g}",
            "required": "rank6=rank8=8 and null residuals <1e-10",
            "passed": q6_analysis["rank"] == 8 and q8_analysis["rank"] == 8 and q6_null_map < 1.0e-10 and q8_null_map < 1.0e-10,
            "interpretation": "the projected C3-channel estimator is quotient invariant within the tested dressed image",
        },
        {
            "gate": "mass_homogeneity",
            "observed": mass_scaling_residual,
            "required": "<1e-12",
            "passed": mass_scaling_residual < 1.0e-12,
            "interpretation": "q6 scales as m^-2 and q8 as m^-4 exactly under the continuum change of variables",
        },
        {
            "gate": "proper_time_component_integrals",
            "observed": f"q6={kernel_summary['q6_integral']:.17g};q8={kernel_summary['q8_integral']:.17g}",
            "required": "both equal one within 1e-12",
            "passed": abs(kernel_summary["q6_integral"] - 1.0) < 1.0e-12 and abs(kernel_summary["q8_integral"] - 1.0) < 1.0e-12,
            "interpretation": "the PT-m3 operator reconstructs each homogeneous Taylor coefficient from UV to IR",
        },
        {
            "gate": "pure_C3_derivative_claim_ceiling",
            "observed": False,
            "required": False,
            "passed": q8_leakage > 1.0e-6,
            "interpretation": "nonzero converged q8 leakage forbids promotion of the estimator to a unique C3 form-factor derivative",
        },
    ]
    gates = tagged(gates)
    all_gates_pass = all(bool(row["passed"]) for row in gates)

    result = {
        "marker": MARKER,
        "profile": arguments.profile,
        "source_hash_pass": source_hash_pass,
        "series_order": checkpoint_4912.SERIES_ORDER,
        "geometry_count": len(ensemble),
        "q6_rank": q6_analysis["rank"],
        "q8_sigma1_dressed_rank": q8_analysis["rank"],
        "q6_C3_null_map_residual": q6_null_map,
        "q8_C3_null_map_residual": q8_null_map,
        "q6_zeta": float(selected["q6_recovery"]["zeta"]),
        "q6_exact_target": TARGET_C3,
        "q6_relative_image_residual": float(selected["q6_recovery"]["response_residual"]),
        "q6_target_relative_residual": q6_target_residual,
        "q8_projected_channel_estimator": float(selected["q8_recovery"]["zeta"]),
        "q8_relative_sigma1_image_leakage": q8_leakage,
        "q8_vector_quadrature_convergence": q8_vector_convergence,
        "q8_estimator_quadrature_convergence": q8_estimator_convergence,
        "q8_leave_one": leave_one_summary,
        "mass_scaling_maximum_residual": mass_scaling_residual,
        "proper_time": kernel_summary,
        "pure_C3_form_factor_derivative_identified": False,
        "finite_momentum_germ_status": "Q6_EXACT_Q8_CONVERGED_BUT_REQUIRES_ENLARGED_DIMENSION8_BASIS",
        "massless_limit_status": "NONUNIFORM_NOT_TAKEN_FROM_LOCAL_TAYLOR_GERM",
        "valid_for_full_MTS_claim": False,
        "all_internal_gates_pass": all_gates_pass,
        "elapsed_seconds": time.perf_counter() - started,
    }

    write_csv(RESPONSES_CSV, responses)
    write_csv(PROJECTION_CSV, projections)
    write_csv(LEAVE_ONE_CSV, leave_one)
    write_csv(MASS_SCALING_CSV, mass_rows)
    write_csv(KERNEL_CSV, kernel)
    write_csv(GATE_CSV, gates)
    RESULT_JSON.write_text(json.dumps(result, indent=2), encoding="utf-8")

    generated = (RESPONSES_CSV, PROJECTION_CSV, LEAVE_ONE_CSV, MASS_SCALING_CSV, KERNEL_CSV, GATE_CSV, RESULT_JSON)
    provenance_lines = [
        "# Checkpoint 4975 provenance",
        "",
        f"Marker: `{MARKER}`",
        "",
        "## Locked inputs",
        "",
    ]
    for path, expected in EXPECTED_HASHES.items():
        provenance_lines.append(f"- `{relative(path)}` — `{observed_hashes[path]}` — expected `{expected}`")
    provenance_lines.extend(["", "## Generated outputs", ""])
    for path in generated:
        provenance_lines.append(f"- `{relative(path)}` — `{digest(path)}`")
    provenance_lines.extend(
        [
            "",
            "All scientific rows are private nonclaim rows. No GitHub action was performed.",
        ]
    )
    PROVENANCE.write_text("\n".join(provenance_lines) + "\n", encoding="utf-8")

    print(
        f"{MARKER}_COMPLETE gates={sum(bool(row['passed']) for row in gates)}/{len(gates)} "
        f"q6_residual={selected['q6_recovery']['response_residual']:.3e} "
        f"q8_leakage={q8_leakage:.12g} q8_estimator={selected['q8_recovery']['zeta']:.12g} "
        f"elapsed={result['elapsed_seconds']:.3f}s",
        flush=True,
    )
    return 0 if all_gates_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
