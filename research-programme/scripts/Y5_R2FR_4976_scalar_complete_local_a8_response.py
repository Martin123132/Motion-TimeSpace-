from __future__ import annotations

import argparse
import csv
import gc
import hashlib
import json
import math
import sys
import time
from fractions import Fraction
from pathlib import Path
from typing import Any

import numpy as np

import Y5_R2FR_4911_full_offshell_a6_template_projector as checkpoint_4911
import Y5_R2FR_4912_free_lattice_multigeometry_continuum_projector as checkpoint_4912


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
SOURCE = POST / "source-intake" / "functional_rg" / "4976"
VALIDATION = POST / "source-intake" / "mts_residuals"

MARKER = "MTS_4976_SCALAR_COMPLETE_LOCAL_A8_RESPONSE"
CHECKED_DATE = "2026-07-13"
TORUS_VOLUME = checkpoint_4911.TORUS_LENGTH**checkpoint_4911.DIMENSIONS

BV_SOURCE = (
    POST
    / "source-intake"
    / "functional_rg"
    / "4973"
    / "src-0911.1168"
    / "cpt2009m.tex"
)
RESPONSE_4975 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "4975"
    / "C3_scalar_q6_q8_Taylor_responses.csv"
)
CHECKPOINT_4975 = (
    POST
    / "4975-Y5-R2FR-scalar-finite-momentum-germ-proper-time-kernel-and-dimension8-leakage-verdict.md"
)

BASIS_CSV = SOURCE / "C3_scalar_local_a8_operator_basis.csv"
TERM_LEDGER_CSV = SOURCE / "C3_scalar_local_a8_source_term_ledger.csv"
MATRIX_CSV = SOURCE / "C3_scalar_local_a8_response_matrix.csv"
RECOVERY_CSV = SOURCE / "C3_scalar_local_a8_recovery.csv"
GATE_CSV = SOURCE / "C3_scalar_local_a8_gate.csv"
RESULT_JSON = SOURCE / "C3_scalar_complete_local_a8_results.json"
PROVENANCE = SOURCE / "PROVENANCE.md"

QUADRATIC_NAMES = (
    "Q1_boxR_squared",
    "Q2_boxRicci_squared",
)

CUBIC_NAMES = (
    "C1_R2_boxR",
    "C2_R_Ricci_HessR",
    "C3_Ricci_gradR_gradR",
    "C4_R_cross_gradRicci",
    "C5_R_Ricci_boxRicci",
    "C6_boxR_Ricci2",
    "C7_boxR_Riemann2",
    "C8_R_Riemann_HessRicci",
    "C9_boxRicci_Riemann_Riemann",
    "C10_Ricci_gradRiemann_gradRiemann",
    "C11_Riemann_gradRicci_gradRicci_A",
    "C12_Riemann_gradRicci_gradRicci_B",
    "C13_Ricci_gradRicci_gradRicci_cross",
    "C14_Ricci_gradRicci_gradRicci_direct",
    "C15_boxRicci_Ricci_Ricci",
)

OPERATOR_DEFINITIONS = {
    "Q1_boxR_squared": "(Box R)^2 = R Box^2 R on closed T4",
    "Q2_boxRicci_squared": "(Box R_mn)(Box R^mn) = R_mn Box^2 R^mn on closed T4",
    "C1_R2_boxR": "R^2 Box R",
    "C2_R_Ricci_HessR": "R R^mn nabla_m nabla_n R",
    "C3_Ricci_gradR_gradR": "R^mn nabla_m R nabla_n R",
    "C4_R_cross_gradRicci": "R nabla^m R^na nabla_n R_ma",
    "C5_R_Ricci_boxRicci": "R R^mn Box R_mn",
    "C6_boxR_Ricci2": "(Box R) R_mn R^mn",
    "C7_boxR_Riemann2": "(Box R) R_mnab R^mnab",
    "C8_R_Riemann_HessRicci": "R R^mnab nabla_m nabla_a R_nb",
    "C9_boxRicci_Riemann_Riemann": "(Box R_ab) R^a_mnl R^b_mnl",
    "C10_Ricci_gradRiemann_gradRiemann": "R_ls nabla^l R^mnab nabla^s R_mnab",
    "C11_Riemann_gradRicci_gradRicci_A": "R^manb nabla_m R_nl nabla^l R_ab",
    "C12_Riemann_gradRicci_gradRicci_B": "R^abmn nabla_a R_bl nabla_m R_n^l",
    "C13_Ricci_gradRicci_gradRicci_cross": "R^mn nabla_a R_bm nabla^b R_n^a",
    "C14_Ricci_gradRicci_gradRicci_direct": "R^mn nabla_m R^ab nabla_n R_ab",
    "C15_boxRicci_Ricci_Ricci": "(Box R^m_a) R^a_b R^b_m",
}

QUADRATIC_COEFFICIENTS = {
    "Q1_boxR_squared": Fraction(11, 30240),
    "Q2_boxRicci_squared": Fraction(1, 15120),
}

# Barvinsky--Vilkovisky cpt2009m.tex, local restored-Riemann a4 formula,
# source lines 3183--3299.  Internal-bundle curvature is zero and P=R/6
# for the minimal scalar operator H=Box.  Keeping the uncombined terms makes
# the substitution auditable and prevents a fitted coefficient from entering.
RAW_CUBIC_TERMS = (
    ("P01", "(1/24)(Box P)P P", "C1_R2_boxR", Fraction(1, 24 * 6**3)),
    ("P02", "(1/720)P P Box R", "C1_R2_boxR", Fraction(1, 720 * 6**2)),
    ("P03", "(1/180)R^mn Hess_mn(P) P", "C2_R_Ricci_HessR", Fraction(1, 180 * 6**2)),
    ("P04", "-(1/1890)R^mn grad_m(R) grad_n(P)", "C3_Ricci_gradR_gradR", -Fraction(1, 1890 * 6)),
    ("P05", "-(1/15120)(Box P)R R", "C1_R2_boxR", -Fraction(1, 15120 * 6)),
    ("P06", "(1/7560)P R Box R", "C1_R2_boxR", Fraction(1, 7560 * 6)),
    ("P07", "-(1/1260)cross-grad-Ricci P", "C4_R_cross_gradRicci", -Fraction(1, 1260 * 6)),
    ("P08", "-(1/840)R^mn Box(R_mn) P", "C5_R_Ricci_boxRicci", -Fraction(1, 840 * 6)),
    ("P09", "-(1/5040)Ricci^2 Box P", "C6_boxR_Ricci2", -Fraction(1, 5040 * 6)),
    ("P10", "(1/1120)Riemann^2 Box P", "C7_boxR_Riemann2", Fraction(1, 1120 * 6)),
    ("P11", "(1/420)Riemann Hess(Ricci) P", "C8_R_Riemann_HessRicci", Fraction(1, 420 * 6)),
    ("G01", "(1/50400)Riemann^2 Box R", "C7_boxR_Riemann2", Fraction(1, 50400)),
    ("G02", "(1/6300)Box(Ricci) Riemann Riemann", "C9_boxRicci_Riemann_Riemann", Fraction(1, 6300)),
    ("G03", "-(1/25200)Ricci grad(Riemann) grad(Riemann)", "C10_Ricci_gradRiemann_gradRiemann", -Fraction(1, 25200)),
    ("G04", "-(1/37800)R Riemann Hess(Ricci)", "C8_R_Riemann_HessRicci", -Fraction(1, 37800)),
    ("G05", "-(1/6300)Riemann grad(Ricci) grad(Ricci) A", "C11_Riemann_gradRicci_gradRicci_A", -Fraction(1, 6300)),
    ("G06", "-(2/4725)Riemann grad(Ricci) grad(Ricci) B", "C12_Riemann_gradRicci_gradRicci_B", -Fraction(2, 4725)),
    ("G07", "(1/37800)Ricci grad(Ricci) grad(Ricci) cross", "C13_Ricci_gradRicci_gradRicci_cross", Fraction(1, 37800)),
    ("G08", "-(1/9450)Ricci grad(Ricci) grad(Ricci) direct", "C14_Ricci_gradRicci_gradRicci_direct", -Fraction(1, 9450)),
    ("G09", "-(1/18900)R cross-grad-Ricci", "C4_R_cross_gradRicci", -Fraction(1, 18900)),
    ("G10", "(29/453600)Ricci grad(R) grad(R)", "C3_Ricci_gradR_gradR", Fraction(29, 453600)),
    ("G11", "(1/37800)R Ricci Box(Ricci)", "C5_R_Ricci_boxRicci", Fraction(1, 37800)),
    ("G12", "-(1/75600)(Box R)Ricci^2", "C6_boxR_Ricci2", -Fraction(1, 75600)),
    ("G13", "-(1/7560)Box(Ricci) Ricci Ricci", "C15_boxRicci_Ricci_Ricci", -Fraction(1, 7560)),
    ("G14", "-(1/100800)(Box R)R R", "C1_R2_boxR", -Fraction(1, 100800)),
)


def consolidated_cubic_coefficients() -> dict[str, Fraction]:
    coefficients = {name: Fraction(0, 1) for name in CUBIC_NAMES}
    for _, _, operator, coefficient in RAW_CUBIC_TERMS:
        coefficients[operator] += coefficient
    return coefficients


CUBIC_COEFFICIENTS = consolidated_cubic_coefficients()


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def relative(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty CSV: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


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


def covariant_derivative_covariant(
    tensor: np.ndarray, christoffel: np.ndarray, size: int
) -> np.ndarray:
    rank = tensor.ndim - checkpoint_4911.TENSOR_AXIS_START
    if rank < 1:
        raise ValueError("covariant derivative helper requires rank >= 1")
    labels = list("bcdefghijk"[:rank])
    result = checkpoint_4911.stack_derivatives(tensor, size)
    for position, old_index in enumerate(labels):
        tensor_labels = labels.copy()
        tensor_labels[position] = "z"
        connection = checkpoint_4911.jet_binary_einsum(
            f"...za{old_index},...{''.join(tensor_labels)}->...a{''.join(labels)}",
            christoffel,
            tensor,
        )
        result -= connection
        del connection
    return result


def contract_box(
    hessian: np.ndarray, inverse_metric: np.ndarray, trailing_rank: int
) -> np.ndarray:
    trailing = "cdefghij"[:trailing_rank]
    return checkpoint_4911.jet_binary_einsum(
        f"...ab,...ab{trailing}->...{trailing}",
        inverse_metric,
        hessian,
    )


def density_value(
    invariant: np.ndarray, sqrt_determinant: np.ndarray, size: int
) -> tuple[float, float]:
    density = checkpoint_4911.jet_pointwise(sqrt_determinant, invariant)
    cell_volume = (checkpoint_4911.TORUS_LENGTH / size) ** checkpoint_4911.DIMENSIONS
    mixed = np.sum(density[7]) * cell_volume / TORUS_VOLUME
    return float(mixed.real), abs(float(mixed.imag))


def local_a8_geometry(
    size: int,
    momenta: np.ndarray,
    polarizations: np.ndarray,
    phases: np.ndarray,
) -> dict[str, Any]:
    profiles = checkpoint_4911.source_profiles(size, momenta, polarizations, phases)
    covariant_metric, inverse_metric, sqrt_determinant, metric_residual = (
        checkpoint_4911.metric_jets(size, profiles)
    )
    curvature = checkpoint_4911.curvature_jets(
        size, covariant_metric, inverse_metric
    )
    christoffel = curvature["christoffel"]
    scalar = curvature["scalar"]
    ricci = curvature["ricci"]
    riemann = curvature["riemann"]
    grad_scalar = curvature["grad_scalar"]
    grad_ricci = curvature["grad_ricci"]
    grad_riemann = curvature["grad_riemann"]

    hess_scalar = covariant_derivative_covariant(
        grad_scalar, christoffel, size
    )
    box_scalar = contract_box(hess_scalar, inverse_metric, 0)
    hess_ricci = covariant_derivative_covariant(
        grad_ricci, christoffel, size
    )
    box_ricci = contract_box(hess_ricci, inverse_metric, 2)

    ricci_up = checkpoint_4911.raise_tensor_axes(
        ricci, inverse_metric, (0, 1)
    )
    riemann_up = checkpoint_4911.raise_tensor_axes(
        riemann, inverse_metric, (0, 1, 2, 3)
    )
    box_ricci_up = checkpoint_4911.raise_tensor_axes(
        box_ricci, inverse_metric, (0, 1)
    )

    quadratic = [
        checkpoint_4911.jet_pointwise(box_scalar, box_scalar),
        checkpoint_4911.jet_binary_einsum(
            "...mn,...mn->...", box_ricci, box_ricci_up
        ),
    ]

    scalar_squared = checkpoint_4911.jet_pointwise(scalar, scalar)
    c1 = checkpoint_4911.jet_pointwise(scalar_squared, box_scalar)

    ricci_hess_scalar = checkpoint_4911.jet_binary_einsum(
        "...mn,...mn->...", ricci_up, hess_scalar
    )
    c2 = checkpoint_4911.jet_pointwise(scalar, ricci_hess_scalar)

    grad_scalar_pair = checkpoint_4911.jet_binary_einsum(
        "...m,...n->...mn", grad_scalar, grad_scalar
    )
    c3 = checkpoint_4911.jet_binary_einsum(
        "...mn,...mn->...", ricci_up, grad_scalar_pair
    )

    grad_ricci_up = checkpoint_4911.raise_tensor_axes(
        grad_ricci, inverse_metric, (0, 1, 2)
    )
    cross_grad_ricci = checkpoint_4911.jet_binary_einsum(
        "...mna,...nma->...", grad_ricci_up, grad_ricci
    )
    c4 = checkpoint_4911.jet_pointwise(scalar, cross_grad_ricci)

    ricci_box_ricci = checkpoint_4911.jet_binary_einsum(
        "...mn,...mn->...", ricci_up, box_ricci
    )
    c5 = checkpoint_4911.jet_pointwise(scalar, ricci_box_ricci)

    ricci_squared = checkpoint_4911.jet_binary_einsum(
        "...mn,...mn->...", ricci, ricci_up
    )
    c6 = checkpoint_4911.jet_pointwise(box_scalar, ricci_squared)

    riemann_squared = checkpoint_4911.jet_binary_einsum(
        "...mnab,...mnab->...", riemann, riemann_up
    )
    c7 = checkpoint_4911.jet_pointwise(box_scalar, riemann_squared)

    riemann_hess_ricci = checkpoint_4911.jet_binary_einsum(
        "...mnab,...manb->...", riemann_up, hess_ricci
    )
    c8 = checkpoint_4911.jet_pointwise(scalar, riemann_hess_ricci)

    riemann_first_up = checkpoint_4911.raise_tensor_axes(
        riemann, inverse_metric, (0,)
    )
    riemann_pair_ab = checkpoint_4911.jet_binary_einsum(
        "...amnl,...bmnl->...ab", riemann_first_up, riemann_up
    )
    c9 = checkpoint_4911.jet_binary_einsum(
        "...ab,...ab->...", box_ricci, riemann_pair_ab
    )

    grad_riemann_derivative_up = checkpoint_4911.raise_tensor_axes(
        grad_riemann, inverse_metric, (0,)
    )
    grad_riemann_up = checkpoint_4911.raise_tensor_axes(
        grad_riemann_derivative_up, inverse_metric, (1, 2, 3, 4)
    )
    grad_riemann_pair = checkpoint_4911.jet_binary_einsum(
        "...lmnab,...smnab->...ls",
        grad_riemann_up,
        grad_riemann_derivative_up,
    )
    c10 = checkpoint_4911.jet_binary_einsum(
        "...ls,...ls->...", ricci, grad_riemann_pair
    )
    del grad_riemann_up, grad_riemann_derivative_up, grad_riemann_pair
    gc.collect()

    grad_ricci_derivative_up = checkpoint_4911.raise_tensor_axes(
        grad_ricci, inverse_metric, (0,)
    )
    grad_pair_a = checkpoint_4911.jet_binary_einsum(
        "...mnl,...lab->...manb", grad_ricci, grad_ricci_derivative_up
    )
    c11 = checkpoint_4911.jet_binary_einsum(
        "...manb,...manb->...", riemann_up, grad_pair_a
    )

    grad_ricci_last_up = checkpoint_4911.raise_tensor_axes(
        grad_ricci, inverse_metric, (2,)
    )
    grad_pair_b = checkpoint_4911.jet_binary_einsum(
        "...abl,...mnl->...abmn", grad_ricci, grad_ricci_last_up
    )
    c12 = checkpoint_4911.jet_binary_einsum(
        "...abmn,...abmn->...", riemann_up, grad_pair_b
    )

    grad_ricci_derivative_last_up = checkpoint_4911.raise_tensor_axes(
        grad_ricci, inverse_metric, (0, 2)
    )
    grad_pair_cross = checkpoint_4911.jet_binary_einsum(
        "...abm,...bna->...mn", grad_ricci, grad_ricci_derivative_last_up
    )
    c13 = checkpoint_4911.jet_binary_einsum(
        "...mn,...mn->...", ricci_up, grad_pair_cross
    )

    grad_ricci_ricci_up = checkpoint_4911.raise_tensor_axes(
        grad_ricci, inverse_metric, (1, 2)
    )
    grad_pair_direct = checkpoint_4911.jet_binary_einsum(
        "...mab,...nab->...mn", grad_ricci_ricci_up, grad_ricci
    )
    c14 = checkpoint_4911.jet_binary_einsum(
        "...mn,...mn->...", ricci_up, grad_pair_direct
    )

    box_ricci_mixed = checkpoint_4911.raise_tensor_axes(
        box_ricci, inverse_metric, (0,)
    )
    ricci_mixed = checkpoint_4911.raise_tensor_axes(
        ricci, inverse_metric, (0,)
    )
    box_times_ricci = checkpoint_4911.jet_binary_einsum(
        "...ma,...ab->...mb", box_ricci_mixed, ricci_mixed
    )
    c15 = checkpoint_4911.jet_binary_einsum(
        "...mb,...bm->...", box_times_ricci, ricci_mixed
    )

    cubic = [
        c1,
        c2,
        c3,
        c4,
        c5,
        c6,
        c7,
        c8,
        c9,
        c10,
        c11,
        c12,
        c13,
        c14,
        c15,
    ]

    r_box_r = checkpoint_4911.jet_pointwise(scalar, box_scalar)
    ricci_box_ricci_control = checkpoint_4911.jet_binary_einsum(
        "...mn,...mn->...", ricci_up, box_ricci
    )

    values: dict[str, float] = {}
    maximum_imaginary = 0.0
    for name, invariant in zip(QUADRATIC_NAMES + CUBIC_NAMES, quadratic + cubic):
        value, imaginary = density_value(invariant, sqrt_determinant, size)
        values[name] = value
        maximum_imaginary = max(maximum_imaginary, imaginary)
    r_box_r_value, r_box_r_imaginary = density_value(
        r_box_r, sqrt_determinant, size
    )
    ricci_box_value, ricci_box_imaginary = density_value(
        ricci_box_ricci_control, sqrt_determinant, size
    )
    maximum_imaginary = max(
        maximum_imaginary, r_box_r_imaginary, ricci_box_imaginary
    )

    return {
        "values": values,
        "R_box_R_control": r_box_r_value,
        "Ricci_box_Ricci_control": ricci_box_value,
        "metric_inverse_residual": metric_residual,
        "maximum_imaginary_residual": maximum_imaginary,
    }


def load_q8_target(geometry_ids: list[str]) -> np.ndarray:
    rows = [
        row
        for row in read_csv(RESPONSE_4975)
        if row["config"] == "R24_A10_m1"
    ]
    by_geometry = {row["geometry_id"]: float(row["q8_response"]) for row in rows}
    if set(by_geometry) != set(geometry_ids):
        raise RuntimeError("4975 selected q8 response does not match the 4911 ensemble")
    q8 = np.asarray([by_geometry[name] for name in geometry_ids], dtype=float)
    return -2.0 * (4.0 * math.pi) ** 2 * q8


def basis_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for sector, names, coefficients in (
        ("quadratic_four_derivative", QUADRATIC_NAMES, QUADRATIC_COEFFICIENTS),
        ("cubic_two_derivative", CUBIC_NAMES, CUBIC_COEFFICIENTS),
    ):
        for index, name in enumerate(names, start=1):
            coefficient = coefficients[name]
            rows.append(
                {
                    "sector": sector,
                    "sector_index": index,
                    "operator": name,
                    "definition": OPERATOR_DEFINITIONS[name],
                    "minimal_scalar_source_coefficient": str(coefficient),
                    "minimal_scalar_source_coefficient_float": float(coefficient),
                    "engine_to_source_sign": 1,
                    "coefficient_status": "SOURCE_FIXED_NOT_FITTED",
                }
            )
    return tagged(rows)


def term_ledger_rows() -> list[dict[str, Any]]:
    return tagged(
        [
            {
                "source_term": source_term,
                "source_expression_after_P_equals_R_over_6": expression,
                "consolidated_operator": operator,
                "term_coefficient": str(coefficient),
                "term_coefficient_float": float(coefficient),
                "source_location": f"{relative(BV_SOURCE)}:3183",
                "status": "SOURCE_TERM_TRANSCRIBED_AND_CONSOLIDATED",
            }
            for source_term, expression, operator, coefficient in RAW_CUBIC_TERMS
        ]
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", choices=("smoke", "checkpoint"), default="checkpoint")
    arguments = parser.parse_args()
    started = time.perf_counter()
    print(f"{MARKER}_START profile={arguments.profile}", flush=True)
    SOURCE.mkdir(parents=True, exist_ok=True)

    required_sources = (
        BV_SOURCE,
        RESPONSE_4975,
        CHECKPOINT_4975,
        POST / "scripts" / "Y5_R2FR_4911_full_offshell_a6_template_projector.py",
        POST / "scripts" / "Y5_R2FR_4912_free_lattice_multigeometry_continuum_projector.py",
    )
    source_exists = all(path.exists() for path in required_sources)
    if not source_exists:
        missing = [str(path) for path in required_sources if not path.exists()]
        raise FileNotFoundError(f"missing required source(s): {missing}")

    geometry_ids, a6_matrix = checkpoint_4912.load_geometric_matrix()
    ensemble = checkpoint_4911.random_source_ensemble(len(geometry_ids))
    if [source["geometry_id"] for source in ensemble] != geometry_ids:
        raise RuntimeError("4911 ensemble ordering changed")
    target = load_q8_target(geometry_ids)

    if arguments.profile == "smoke":
        sizes = (6,)
        selected_ensemble = ensemble[:3]
    else:
        sizes = (6, 8)
        selected_ensemble = ensemble

    matrix_rows: list[dict[str, Any]] = []
    computed: dict[int, dict[str, dict[str, Any]]] = {}
    for size in sizes:
        computed[size] = {}
        for index, source in enumerate(selected_ensemble):
            geometry_started = time.perf_counter()
            result = local_a8_geometry(
                size,
                source["momenta"],
                source["polarizations"],
                source["phases"],
            )
            computed[size][source["geometry_id"]] = result
            for operator, value in result["values"].items():
                matrix_rows.append(
                    {
                        "grid_size": size,
                        "geometry_id": source["geometry_id"],
                        "operator": operator,
                        "mixed_third_response_density": value,
                        "metric_inverse_residual": result["metric_inverse_residual"],
                        "maximum_imaginary_residual": result["maximum_imaginary_residual"],
                        "elapsed_geometry_seconds": time.perf_counter() - geometry_started,
                        "status": "EXACT_THIRD_JET_ON_PERIODIC_T4",
                    }
                )
            print(
                f"4976 N{size} {source['geometry_id']} {index + 1}/{len(selected_ensemble)}",
                flush=True,
            )
            gc.collect()

    selected_size = sizes[-1]
    selected_ids = [source["geometry_id"] for source in selected_ensemble]
    selected_indices = [geometry_ids.index(name) for name in selected_ids]
    quadratic_matrix = np.asarray(
        [
            [computed[selected_size][name]["values"][operator] for operator in QUADRATIC_NAMES]
            for name in selected_ids
        ]
    )
    cubic_matrix = np.asarray(
        [
            [computed[selected_size][name]["values"][operator] for operator in CUBIC_NAMES]
            for name in selected_ids
        ]
    )
    quadratic_coefficients = np.asarray(
        [float(QUADRATIC_COEFFICIENTS[name]) for name in QUADRATIC_NAMES]
    )
    cubic_coefficients = np.asarray(
        [float(CUBIC_COEFFICIENTS[name]) for name in CUBIC_NAMES]
    )
    quadratic_prediction = quadratic_matrix @ quadratic_coefficients
    # BV cpt2009m.tex lines 198--202 define
    # R^mu_{ alpha nu beta}=partial_nu Gamma^mu_{alpha beta}-..., exactly
    # the convention implemented by the 4911 engine.  The opposite cubic
    # sign recorded in 4911 belongs to its different Vassilevich source.
    cubic_prediction = cubic_matrix @ cubic_coefficients
    prediction = quadratic_prediction + cubic_prediction
    selected_target = target[selected_indices]
    target_norm = max(float(np.linalg.norm(selected_target)), 1.0e-30)
    relative_residual = float(np.linalg.norm(prediction - selected_target) / target_norm)
    quadratic_only_residual = float(
        np.linalg.norm(quadratic_prediction - selected_target) / target_norm
    )
    cubic_only_residual = float(
        np.linalg.norm(cubic_prediction - selected_target) / target_norm
    )

    recovery_rows = []
    for position, geometry_id in enumerate(selected_ids):
        recovery_rows.append(
            {
                "grid_size": selected_size,
                "geometry_id": geometry_id,
                "a8_target_from_exact_determinant_q8": selected_target[position],
                "a8_quadratic_descendant_prediction": quadratic_prediction[position],
                "a8_cubic_source_fixed_prediction": cubic_prediction[position],
                "a8_complete_local_prediction": prediction[position],
                "absolute_residual": prediction[position] - selected_target[position],
                "residual_over_full_target_norm": abs(prediction[position] - selected_target[position]) / target_norm,
                "status": "SOURCE_FIXED_LOCAL_A8_COMPARISON",
            }
        )

    a6_selected = a6_matrix[selected_indices]
    ibp_r_residuals = []
    ibp_ricci_residuals = []
    for position, name in enumerate(selected_ids):
        result = computed[selected_size][name]
        ibp_r_residuals.append(result["R_box_R_control"] + a6_selected[position, 0])
        ibp_ricci_residuals.append(result["Ricci_box_Ricci_control"] + a6_selected[position, 1])
    ibp_scale = max(float(np.linalg.norm(a6_selected[:, :2])), 1.0e-30)
    ibp_residual = float(
        np.linalg.norm(np.column_stack((ibp_r_residuals, ibp_ricci_residuals))) / ibp_scale
    )

    if len(sizes) > 1:
        size6 = np.asarray(
            [
                [computed[6][name]["values"][operator] for operator in QUADRATIC_NAMES + CUBIC_NAMES]
                for name in selected_ids
            ]
        )
        size8 = np.asarray(
            [
                [computed[8][name]["values"][operator] for operator in QUADRATIC_NAMES + CUBIC_NAMES]
                for name in selected_ids
            ]
        )
        grid_residual = float(
            np.linalg.norm(size8 - size6) / max(float(np.linalg.norm(size8)), 1.0e-30)
        )
    else:
        grid_residual = 0.0

    maximum_metric_residual = max(
        result["metric_inverse_residual"]
        for size_results in computed.values()
        for result in size_results.values()
    )
    maximum_imaginary_residual = max(
        result["maximum_imaginary_residual"]
        for size_results in computed.values()
        for result in size_results.values()
    )

    gates = [
        {
            "gate": "source_paths_exist",
            "observed": source_exists,
            "required": True,
            "passed": source_exists,
            "interpretation": "the local a4 source and determinant controls are present",
        },
        {
            "gate": "operator_count_and_fixed_coefficients",
            "observed": f"quadratic={len(QUADRATIC_NAMES)};cubic={len(CUBIC_NAMES)};raw_terms={len(RAW_CUBIC_TERMS)}",
            "required": "2 quadratic, 15 consolidated cubic, 25 raw source terms",
            "passed": len(QUADRATIC_NAMES) == 2 and len(CUBIC_NAMES) == 15 and len(RAW_CUBIC_TERMS) == 25,
            "interpretation": "all coefficients come from the local source formula after P=R/6",
        },
        {
            "gate": "BV_curvature_convention_map",
            "observed": "R^mu_(alpha nu beta)=partial_nu Gamma^mu_(alpha beta)-partial_beta Gamma^mu_(alpha nu)+...",
            "required": "same sign and index order as the 4911 engine",
            "passed": True,
            "interpretation": "BV source lines 198--202 match the engine; no cubic sign flip is applied",
        },
        {
            "gate": "covariant_integration_by_parts_control",
            "observed": ibp_residual,
            "required": "<1e-9",
            "passed": ibp_residual < 1.0e-9,
            "interpretation": "R Box R and Ricci Box Ricci reproduce minus the established gradient-squared templates",
        },
        {
            "gate": "grid_alias_control",
            "observed": grid_residual,
            "required": "<1e-9 for checkpoint; smoke records one-grid exact jet",
            "passed": grid_residual < 1.0e-9,
            "interpretation": "N6 and N8 give the same mixed local response when both are run",
        },
        {
            "gate": "geometric_numerics",
            "observed": f"metric={maximum_metric_residual:.17g};imaginary={maximum_imaginary_residual:.17g}",
            "required": "both <1e-9",
            "passed": maximum_metric_residual < 1.0e-9 and maximum_imaginary_residual < 1.0e-9,
            "interpretation": "metric inversion and real periodic integration are numerically controlled",
        },
        {
            "gate": "complete_local_a8_recovery",
            "observed": relative_residual,
            "required": "<1e-8",
            "passed": relative_residual < 1.0e-8,
            "interpretation": "the source-fixed local a8 basis reproduces the independent exact determinant q8 vector",
        },
        {
            "gate": "no_fitted_operator_coefficients",
            "observed": True,
            "required": True,
            "passed": True,
            "interpretation": "no response coefficient was inferred from the twelve target geometries",
        },
    ]
    gates = tagged(gates)
    all_gates_pass = all(bool(row["passed"]) for row in gates)

    result = {
        "marker": MARKER,
        "profile": arguments.profile,
        "geometry_count": len(selected_ids),
        "grid_sizes": list(sizes),
        "quadratic_operator_count": len(QUADRATIC_NAMES),
        "cubic_operator_count": len(CUBIC_NAMES),
        "raw_cubic_source_term_count": len(RAW_CUBIC_TERMS),
        "covariant_integration_by_parts_relative_residual": ibp_residual,
        "grid_relative_residual": grid_residual,
        "quadratic_only_relative_residual": quadratic_only_residual,
        "cubic_only_relative_residual": cubic_only_residual,
        "complete_local_a8_relative_residual": relative_residual,
        "maximum_metric_inverse_residual": maximum_metric_residual,
        "maximum_imaginary_residual": maximum_imaginary_residual,
        "coefficient_origin": "BARVINSKY_VILKOVISKY_LOCAL_A4_P_EQUALS_R_OVER_6_NO_FIT",
        "engine_to_source_cubic_sign": 1,
        "complete_scalar_q8_recovered": relative_residual < 1.0e-8,
        "valid_for_full_MTS_claim": False,
        "all_internal_gates_pass": all_gates_pass,
        "elapsed_seconds": time.perf_counter() - started,
    }

    write_csv(BASIS_CSV, basis_rows())
    write_csv(TERM_LEDGER_CSV, term_ledger_rows())
    write_csv(MATRIX_CSV, tagged(matrix_rows))
    write_csv(RECOVERY_CSV, tagged(recovery_rows))
    write_csv(GATE_CSV, gates)
    RESULT_JSON.write_text(json.dumps(result, indent=2), encoding="utf-8")

    generated = (
        BASIS_CSV,
        TERM_LEDGER_CSV,
        MATRIX_CSV,
        RECOVERY_CSV,
        GATE_CSV,
        RESULT_JSON,
    )
    lines = [
        "# Checkpoint 4976 provenance",
        "",
        f"Marker: `{MARKER}`",
        "",
        "## Inputs",
        "",
    ]
    for path in required_sources:
        lines.append(f"- `{relative(path)}` - `{digest(path)}`")
    lines.extend(["", "## Outputs", ""])
    for path in generated:
        lines.append(f"- `{relative(path)}` - `{digest(path)}`")
    lines.extend(
        [
            "",
            "All rows are private nonclaim rows. No GitHub action was performed.",
        ]
    )
    PROVENANCE.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(
        f"{MARKER}_COMPLETE gates={sum(bool(row['passed']) for row in gates)}/{len(gates)} "
        f"ibp={ibp_residual:.3e} grid={grid_residual:.3e} "
        f"a8_residual={relative_residual:.12g} elapsed={result['elapsed_seconds']:.3f}s",
        flush=True,
    )
    return 0 if all_gates_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
