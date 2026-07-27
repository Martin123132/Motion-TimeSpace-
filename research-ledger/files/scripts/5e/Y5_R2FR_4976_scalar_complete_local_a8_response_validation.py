from __future__ import annotations

import argparse
import csv
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
import Y5_R2FR_4976_scalar_complete_local_a8_response as checkpoint_4976


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE = POST / "source-intake" / "functional_rg" / "4976"
VALIDATION = POST / "source-intake" / "mts_residuals" / "P8_Y5_BRR545_4976_VALIDATION.csv"
OUT_OF_SAMPLE = SOURCE / "C3_scalar_local_a8_out_of_sample.csv"
QUOTIENT = SOURCE / "C3_scalar_local_a8_quotient.csv"
VALIDATION_PROVENANCE = SOURCE / "VALIDATION_PROVENANCE.md"

CHECKPOINT_DOC = POST / "4976-Y5-R2FR-source-complete-local-a8-third-response-quotient-and-scalar-q8-recovery.md"
FORMAL_NOTE = FORMAL / "992-PPC4161-source-complete-local-a8-third-response-and-scalar-q8-recovery.md"
CURRENT_RESUME = POST / "CURRENT_LOCAL_RESUME.md"
CURRENT_SPINE = POST / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"
VARIABLE_AUDIT = FORMAL / "04-variable-audit.csv"
CLAIMS_REGISTER = FORMAL / "02-claims-register.csv"
EQUATION_REGISTER = FORMAL / "05-equation-register.md"
RED_TEAM = FORMAL / "06-consistency-red-team.md"
UNIFICATION_SPINE = FORMAL / "07-unification-spine.md"

MARKER = "MTS_4976_SCALAR_COMPLETE_LOCAL_A8_RESPONSE_VALIDATION"
CHECKED_DATE = "2026-07-13"

EXPECTED_QUADRATIC = {
    "Q1_boxR_squared": Fraction(11, 30240),
    "Q2_boxRicci_squared": Fraction(1, 15120),
}
EXPECTED_CUBIC = {
    "C1_R2_boxR": Fraction(211, 907200),
    "C2_R_Ricci_HessR": Fraction(1, 6480),
    "C3_Ricci_gradR_gradR": -Fraction(11, 453600),
    "C4_R_cross_gradRicci": -Fraction(1, 5400),
    "C5_R_Ricci_boxRicci": -Fraction(13, 75600),
    "C6_boxR_Ricci2": -Fraction(1, 21600),
    "C7_boxR_Riemann2": Fraction(17, 100800),
    "C8_R_Riemann_HessRicci": Fraction(1, 2700),
    "C9_boxRicci_Riemann_Riemann": Fraction(1, 6300),
    "C10_Ricci_gradRiemann_gradRiemann": -Fraction(1, 25200),
    "C11_Riemann_gradRicci_gradRicci_A": -Fraction(1, 6300),
    "C12_Riemann_gradRicci_gradRicci_B": -Fraction(2, 4725),
    "C13_Ricci_gradRicci_gradRicci_cross": Fraction(1, 37800),
    "C14_Ricci_gradRicci_gradRicci_direct": -Fraction(1, 9450),
    "C15_boxRicci_Ricci_Ricci": -Fraction(1, 7560),
}


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty CSV: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def coefficient_vector(names: list[str]) -> np.ndarray:
    expected = {**EXPECTED_QUADRATIC, **EXPECTED_CUBIC}
    return np.asarray([float(expected[name]) for name in names], dtype=float)


def generate_out_of_sample() -> list[dict[str, Any]]:
    checkpoint_4912.SERIES_ORDER = 8
    names = list(checkpoint_4976.QUADRATIC_NAMES + checkpoint_4976.CUBIC_NAMES)
    coefficients = coefficient_vector(names)
    ensemble = checkpoint_4911.random_source_ensemble(20)
    rows: list[dict[str, Any]] = []
    for index, source in enumerate(ensemble[12:], start=12):
        started = time.perf_counter()
        geometry = checkpoint_4976.local_a8_geometry(
            6,
            source["momenta"],
            source["polarizations"],
            source["phases"],
        )
        series, inverse_residual = checkpoint_4912.complex_TTT_continuum_series_density(
            source["momenta"],
            source["polarizations"],
            1.0,
            24,
            10,
        )
        phase = np.exp(1j * float(np.sum(source["phases"])))
        q8 = 0.25 * float(np.real(phase * series[8]))
        target = -2.0 * (4.0 * math.pi) ** 2 * q8
        operator_values = np.asarray(
            [geometry["values"][name] for name in names], dtype=float
        )
        prediction = float(operator_values @ coefficients)
        row: dict[str, Any] = {
            "geometry_index": index,
            "geometry_id": source["geometry_id"],
            "grid_size": 6,
            "determinant_radial_order": 24,
            "determinant_angular_order": 10,
            "a8_target": target,
            "a8_source_fixed_prediction": prediction,
            "absolute_residual": prediction - target,
            "propagator_inverse_residual": inverse_residual,
            "metric_inverse_residual": geometry["metric_inverse_residual"],
            "maximum_imaginary_residual": geometry["maximum_imaginary_residual"],
            "elapsed_seconds": time.perf_counter() - started,
            "checkpoint_marker": MARKER,
            "valid_for_full_MTS_claim": False,
            "source_checked_date": CHECKED_DATE,
        }
        for name, value in zip(names, operator_values):
            row[name] = value
        rows.append(row)
        print(
            f"4976 validation {source['geometry_id']} {index - 11}/8 residual={prediction - target:.3e}",
            flush=True,
        )
    write_csv(OUT_OF_SAMPLE, rows)
    return rows


def matrix_from_runner(names: list[str]) -> tuple[list[str], np.ndarray]:
    rows = [
        row
        for row in read_csv(checkpoint_4976.MATRIX_CSV)
        if int(row["grid_size"]) == 8
    ]
    geometry_ids = sorted({row["geometry_id"] for row in rows})
    matrix = np.zeros((len(geometry_ids), len(names)), dtype=float)
    for row in rows:
        matrix[
            geometry_ids.index(row["geometry_id"]),
            names.index(row["operator"]),
        ] = float(row["mixed_third_response_density"])
    return geometry_ids, matrix


def normalized_svd(matrix: np.ndarray) -> dict[str, Any]:
    norms = np.linalg.norm(matrix, axis=0)
    if np.any(norms < 1.0e-14):
        raise RuntimeError("zero operator column in extended quotient")
    normalized = matrix / norms
    _, singular_values, right_vectors = np.linalg.svd(
        normalized, full_matrices=True
    )
    tolerance = singular_values[0] * 1.0e-10
    rank = int(np.sum(singular_values > tolerance))
    null_original = np.asarray(
        [vector / norms for vector in right_vectors[rank:]], dtype=float
    )
    for index in range(len(null_original)):
        null_original[index] /= np.linalg.norm(null_original[index])
    return {
        "norms": norms,
        "singular_values": singular_values,
        "rank": rank,
        "nullspace": null_original,
    }


def csv_width_valid(path: Path) -> bool:
    with path.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.reader(handle))
    return bool(rows) and all(len(row) == len(rows[0]) for row in rows)


def contains(path: Path, marker: str) -> bool:
    return path.exists() and marker in path.read_text(
        encoding="utf-8", errors="replace"
    )


def compiles(path: Path) -> bool:
    try:
        compile(path.read_text(encoding="utf-8"), str(path), "exec")
    except (OSError, SyntaxError):
        return False
    return True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--recompute-out-of-sample", action="store_true")
    arguments = parser.parse_args()
    started = time.perf_counter()
    print(f"{MARKER}_START", flush=True)

    names = list(checkpoint_4976.QUADRATIC_NAMES + checkpoint_4976.CUBIC_NAMES)
    expected = {**EXPECTED_QUADRATIC, **EXPECTED_CUBIC}
    source_coefficients_match = all(
        checkpoint_4976.QUADRATIC_COEFFICIENTS.get(name, checkpoint_4976.CUBIC_COEFFICIENTS.get(name))
        == expected[name]
        for name in names
    )

    if arguments.recompute_out_of_sample or not OUT_OF_SAMPLE.exists():
        out_rows = generate_out_of_sample()
    else:
        out_rows = read_csv(OUT_OF_SAMPLE)

    base_ids, base_matrix = matrix_from_runner(names)
    extra_ids = [row["geometry_id"] for row in out_rows]
    extra_matrix = np.asarray(
        [[float(row[name]) for name in names] for row in out_rows], dtype=float
    )
    extended_matrix = np.vstack((base_matrix, extra_matrix))
    analysis = normalized_svd(extended_matrix)
    coefficients = coefficient_vector(names)

    extra_target = np.asarray([float(row["a8_target"]) for row in out_rows])
    extra_prediction = extra_matrix @ coefficients
    extra_residual = float(
        np.linalg.norm(extra_prediction - extra_target)
        / max(float(np.linalg.norm(extra_target)), 1.0e-30)
    )

    recovery_rows = read_csv(checkpoint_4976.RECOVERY_CSV)
    base_target = np.asarray(
        [float(row["a8_target_from_exact_determinant_q8"]) for row in recovery_rows]
    )
    base_prediction = base_matrix @ coefficients
    base_residual = float(
        np.linalg.norm(base_prediction - base_target)
        / max(float(np.linalg.norm(base_target)), 1.0e-30)
    )

    # Exact closed-manifold integration-by-parts/Bianchi identity:
    # C2 + C3 - C1/4 = 0.
    identity_one = np.zeros(len(names), dtype=float)
    identity_one[names.index("C1_R2_boxR")] = -0.25
    identity_one[names.index("C2_R_Ricci_HessR")] = 1.0
    identity_one[names.index("C3_Ricci_gradR_gradR")] = 1.0
    identity_one_residual = float(
        np.linalg.norm(extended_matrix @ identity_one)
        / max(float(np.linalg.norm(extended_matrix)), 1.0e-30)
    )

    # The second null direction is the four-dimensional Gauss--Bonnet/
    # five-index-antisymmetrization descendant identified by the BV Appendix
    # A.35--A.39, reduced here to this integrated third-response basis.
    identity_two_coefficients = {
        "C3_Ricci_gradR_gradR": 4.0,
        "C4_R_cross_gradRicci": -8.0,
        "C5_R_Ricci_boxRicci": -8.0,
        "C6_boxR_Ricci2": 4.0,
        "C7_boxR_Riemann2": -1.0,
        "C8_R_Riemann_HessRicci": 8.0,
        "C9_boxRicci_Riemann_Riemann": 4.0,
        "C11_Riemann_gradRicci_gradRicci_A": 16.0,
        "C12_Riemann_gradRicci_gradRicci_B": 16.0,
        "C13_Ricci_gradRicci_gradRicci_cross": -16.0,
    }
    identity_two = np.zeros(len(names), dtype=float)
    for operator, value in identity_two_coefficients.items():
        identity_two[names.index(operator)] = value
    identity_two_residual = float(
        np.linalg.norm(extended_matrix @ identity_two)
        / max(float(np.linalg.norm(extended_matrix)), 1.0e-30)
    )

    quotient_rows: list[dict[str, Any]] = []
    for index, value in enumerate(analysis["singular_values"], start=1):
        quotient_rows.append(
            {
                "row_type": "singular_value",
                "row_index": index,
                "operator": "not_applicable",
                "value": value,
                "extended_geometry_count": len(base_ids) + len(extra_ids),
                "operator_count": len(names),
                "rank": analysis["rank"],
                "nullity": len(names) - analysis["rank"],
                "status": "EXTENDED_RESPONSE_QUOTIENT",
            }
        )
    for null_index, vector in enumerate(analysis["nullspace"], start=1):
        for operator, value in zip(names, vector):
            quotient_rows.append(
                {
                    "row_type": "numerical_null_vector",
                    "row_index": null_index,
                    "operator": operator,
                    "value": value,
                    "extended_geometry_count": len(base_ids) + len(extra_ids),
                    "operator_count": len(names),
                    "rank": analysis["rank"],
                    "nullity": len(names) - analysis["rank"],
                    "status": "NULL_DIRECTIONS_ARE_INTEGRATED_IDENTITIES_NOT_FIT_FREEDOMS",
                }
            )
    for relation_index, vector in enumerate((identity_one, identity_two), start=1):
        for operator, value in zip(names, vector):
            if value == 0.0:
                continue
            quotient_rows.append(
                {
                    "row_type": "exact_rational_identity",
                    "row_index": relation_index,
                    "operator": operator,
                    "value": value,
                    "extended_geometry_count": len(base_ids) + len(extra_ids),
                    "operator_count": len(names),
                    "rank": analysis["rank"],
                    "nullity": len(names) - analysis["rank"],
                    "status": (
                        "CLOSED_T4_IBP_AND_CONTRACTED_BIANCHI"
                        if relation_index == 1
                        else "FOUR_DIMENSIONAL_GAUSS_BONNET_A35_A39_DESCENDANT"
                    ),
                }
            )
    write_csv(
        QUOTIENT,
        [
            {
                **row,
                "checkpoint_marker": MARKER,
                "valid_for_full_MTS_claim": False,
                "source_checked_date": CHECKED_DATE,
            }
            for row in quotient_rows
        ],
    )

    runner_result = json.loads(checkpoint_4976.RESULT_JSON.read_text(encoding="utf-8"))
    output_paths = (
        checkpoint_4976.BASIS_CSV,
        checkpoint_4976.TERM_LEDGER_CSV,
        checkpoint_4976.MATRIX_CSV,
        checkpoint_4976.RECOVERY_CSV,
        checkpoint_4976.GATE_CSV,
        checkpoint_4976.RESULT_JSON,
        OUT_OF_SAMPLE,
        QUOTIENT,
    )
    no_missing_sentinels = all(
        "MISSING_" not in path.read_text(encoding="utf-8", errors="replace")
        for path in output_paths
    )
    csv_widths = all(
        csv_width_valid(path) for path in output_paths if path.suffix == ".csv"
    )
    maximum_extra_absolute = max(abs(float(row["absolute_residual"])) for row in out_rows)
    maximum_extra_metric = max(float(row["metric_inverse_residual"]) for row in out_rows)
    maximum_extra_imaginary = max(float(row["maximum_imaginary_residual"]) for row in out_rows)
    formal_marker = "PPC4161_SCALAR_COMPLETE_LOCAL_A8_RESPONSE_4976"
    register_paths = (EQUATION_REGISTER, RED_TEAM, UNIFICATION_SPINE)
    expected_variables = (
        "ScalarA8Quadratic4976_MTS",
        "ScalarA8CubicVector4976_MTS",
        "A8ResponseMatrix4976_MTS",
        "A8QuotientRank4976_MTS",
        "A8NullIdentities4976_MTS",
        "PredictivityStatus4976_MTS",
    )
    variable_text = VARIABLE_AUDIT.read_text(encoding="utf-8", errors="replace")
    scientific_csvs = tuple(path for path in output_paths if path.suffix == ".csv")
    all_scientific_rows_nonclaim = all(
        all(
            str(row.get("valid_for_full_MTS_claim", "False")).lower() == "false"
            for row in read_csv(path)
        )
        for path in scientific_csvs
    )
    cache_directories = list((POST / "scripts").rglob("__pycache__"))

    checks = [
        ("VAL4976_01_runner_result_exists", checkpoint_4976.RESULT_JSON.exists(), "runner JSON exists"),
        ("VAL4976_02_runner_all_gates", bool(runner_result["all_internal_gates_pass"]), "runner reports all internal gates"),
        ("VAL4976_03_runner_q8_recovery", float(runner_result["complete_local_a8_relative_residual"]) < 1.0e-10, "twelve-row recovery is machine precision"),
        ("VAL4976_04_runner_grid_control", float(runner_result["grid_relative_residual"]) < 1.0e-10, "N6/N8 response matrices agree"),
        ("VAL4976_05_runner_ibp_control", float(runner_result["covariant_integration_by_parts_relative_residual"]) < 1.0e-10, "covariant integration by parts closes"),
        ("VAL4976_06_operator_counts", len(names) == 17 and len(EXPECTED_QUADRATIC) == 2 and len(EXPECTED_CUBIC) == 15, "two quadratic plus fifteen cubic operators"),
        ("VAL4976_07_source_coefficients", source_coefficients_match, "runner coefficients equal independent exact fractions"),
        ("VAL4976_08_base_independent_arithmetic", base_residual < 1.0e-10, "independent matrix multiplication reproduces base targets"),
        ("VAL4976_09_out_of_sample_count", len(out_rows) == 8 and extra_ids == [f"G{i:02d}" for i in range(12, 20)], "eight fresh geometries are present"),
        ("VAL4976_10_out_of_sample_recovery", extra_residual < 1.0e-10, "source-fixed vector reproduces fresh determinant responses"),
        ("VAL4976_11_out_of_sample_absolute", maximum_extra_absolute < 1.0e-12, "each fresh absolute residual is below tolerance"),
        ("VAL4976_12_out_of_sample_geometry", maximum_extra_metric < 1.0e-10 and maximum_extra_imaginary < 1.0e-10, "fresh geometry numerics are controlled"),
        ("VAL4976_13_extended_rank", analysis["rank"] == 15, "twenty-geometry 17-column quotient has rank fifteen"),
        ("VAL4976_14_extended_nullity", len(names) - analysis["rank"] == 2, "exact integrated nullity is two"),
        ("VAL4976_15_identity_one", identity_one_residual < 1.0e-12, "C2+C3-C1/4 identity is numerically exact"),
        ("VAL4976_16_identity_two", identity_two_residual < 1.0e-12, "four-dimensional Gauss-Bonnet descendant is numerically exact"),
        ("VAL4976_17_output_paths", all(path.exists() for path in output_paths), "all scientific outputs exist"),
        ("VAL4976_18_csv_widths", csv_widths, "all CSV widths are canonical"),
        ("VAL4976_19_no_missing", no_missing_sentinels, "no MISSING_ sentinel occurs"),
        ("VAL4976_20_nonclaim", all(str(row.get("valid_for_full_MTS_claim", "False")).lower() == "false" for row in out_rows), "fresh rows remain nonclaim"),
        ("VAL4976_21_source_exists", checkpoint_4976.BV_SOURCE.exists(), "primary local a4 source exists"),
        ("VAL4976_22_checkpoint_marker", contains(CHECKPOINT_DOC, formal_marker), "checkpoint document contains the formal marker"),
        ("VAL4976_23_formal_note", contains(FORMAL_NOTE, formal_marker), "formal note contains the formal marker"),
        ("VAL4976_24_current_resume", contains(CURRENT_RESUME, formal_marker), "current resume points to 4976"),
        ("VAL4976_25_current_spine", contains(CURRENT_SPINE, formal_marker), "current local-GR spine points to 4976"),
        ("VAL4976_26_variable_audit", all(symbol in variable_text for symbol in expected_variables), "all six 4976 audit symbols exist"),
        ("VAL4976_27_claim_register", contains(CLAIMS_REGISTER, '"L-818"'), "claim L-818 exists"),
        ("VAL4976_28_formal_registers", all(contains(path, formal_marker) for path in register_paths), "equation red-team and unification registers contain 4976"),
        ("VAL4976_29_scripts_compile", compiles(Path(__file__)) and compiles(POST / "scripts" / "Y5_R2FR_4976_scalar_complete_local_a8_response.py"), "runner and validator compile in memory"),
        ("VAL4976_30_all_rows_nonclaim", all_scientific_rows_nonclaim, "every scientific CSV row remains nonclaim"),
        ("VAL4976_31_no_pycache", not cache_directories, "scripts tree contains no __pycache__ directory"),
    ]
    validation_rows = [
        {
            "validation_id": validation_id,
            "status": "PASS" if passed else "FAIL",
            "observed": detail,
            "checkpoint_marker": MARKER,
            "valid_for_full_MTS_claim": False,
            "source_checked_date": CHECKED_DATE,
        }
        for validation_id, passed, detail in checks
    ]
    write_csv(VALIDATION, validation_rows)
    passed = sum(row["status"] == "PASS" for row in validation_rows)
    provenance_paths = (
        checkpoint_4976.BV_SOURCE,
        POST / "scripts" / "Y5_R2FR_4976_scalar_complete_local_a8_response.py",
        Path(__file__),
        CHECKPOINT_DOC,
        FORMAL_NOTE,
        *output_paths,
        VALIDATION,
    )
    provenance_lines = [
        "# Checkpoint 4976 validation provenance",
        "",
        f"Marker: `{MARKER}`",
        "",
    ]
    for path in provenance_paths:
        provenance_lines.append(
            f"- `{path.relative_to(ROOT).as_posix()}` - `{digest(path)}`"
        )
    provenance_lines.extend(
        [
            "",
            "All scientific rows are private nonclaim rows. No GitHub action was performed.",
        ]
    )
    VALIDATION_PROVENANCE.write_text(
        "\n".join(provenance_lines) + "\n", encoding="utf-8"
    )
    print(
        f"{MARKER}_COMPLETE checks={passed}/{len(validation_rows)} rank={analysis['rank']} "
        f"base={base_residual:.3e} out={extra_residual:.3e} "
        f"validation_sha256={digest(VALIDATION)} elapsed={time.perf_counter() - started:.3f}s",
        flush=True,
    )
    return 0 if passed == len(validation_rows) else 1


if __name__ == "__main__":
    raise SystemExit(main())
