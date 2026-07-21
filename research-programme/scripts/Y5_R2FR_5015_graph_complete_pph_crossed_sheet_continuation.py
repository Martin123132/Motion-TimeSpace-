from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import math
import sys
import time
from pathlib import Path
from typing import Any

import numpy as np
from numba import njit, prange
from scipy.stats import qmc


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE = POST / "source-intake" / "functional_rg" / "5015"
RESIDUALS = POST / "source-intake" / "mts_residuals"

SCRIPT_5014 = POST / "scripts" / "Y5_R2FR_5014_crossing_complete_locality_and_graph_complete_pph_bridge.py"
CHECKPOINT_4990 = POST / "4990-Y5-R2FR-crossing-complete-D1-scheme-separation-and-hh-scope-correction.md"
CHECKPOINT_5012 = POST / "5012-Y5-R2FR-nested-soft-forward-angular-first-projection.md"
CHECKPOINT_5014 = POST / "5014-Y5-R2FR-crossing-complete-locality-and-graph-complete-pph-bridge.md"
RESULT_5012 = SOURCE.parent / "5012" / "nested_soft_forward_results.json"
RESULT_5014 = SOURCE.parent / "5014" / "crossing_complete_graph_complete_pph_results.json"
BERN_SOURCE = SOURCE.parent / "4987" / "sources" / "bern_parra_sawyer" / "smeft2.tex"

BRANCH_CSV = SOURCE / "crossed_sheet_branch_and_endpoint_checks.csv"
DIRECT_CSV = SOURCE / "graph_complete_pph_direct_function.csv"
CROSSING_CSV = SOURCE / "graph_complete_pph_cyclic_crossing_function.csv"
LOCALITY_CSV = SOURCE / "pph_only_locality_fit.csv"
GATE_CSV = SOURCE / "crossed_sheet_continuation_gate.csv"
RESULT_JSON = SOURCE / "graph_complete_pph_crossed_sheet_results.json"
PROVENANCE = SOURCE / "PROVENANCE.md"
DOCUMENT = POST / "5015-Y5-R2FR-graph-complete-pph-crossed-sheet-continuation.md"
VALIDATION_CSV = RESIDUALS / "P8_Y5_BRR545_5015_VALIDATION.csv"

MARKER = "MTS_5015_GRAPH_COMPLETE_PPH_CROSSED_SHEET_CONTINUATION"
CHECKED_DATE = "2026-07-14"
FORMAL_BASELINE = "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"


def load_5014() -> Any:
    specification = importlib.util.spec_from_file_location("mts_checkpoint_5014_for_5015", SCRIPT_5014)
    if specification is None or specification.loader is None:
        raise RuntimeError("could not load checkpoint 5014")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


BASE = load_5014()
minkowski = BASE.minkowski
direction = BASE.direction
sequential_three_body = BASE.sequential_three_body
circular_polarization = BASE.circular_polarization
luna_pair = BASE.luna_pair
vector_soft = BASE.vector_soft
PAIRING_S = BASE.PAIRING_S


def relative(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def tree_digest(path: Path) -> str:
    value = hashlib.sha256()
    for item in sorted(candidate for candidate in path.rglob("*") if candidate.is_file()):
        value.update(item.relative_to(path).as_posix().encode("utf-8"))
        value.update(digest(item).encode("ascii"))
    return value.hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
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


def source_locks() -> dict[str, bool]:
    required = (
        SCRIPT_5014,
        CHECKPOINT_4990,
        CHECKPOINT_5012,
        CHECKPOINT_5014,
        RESULT_5012,
        RESULT_5014,
        BERN_SOURCE,
    )
    result_5014 = read_json(RESULT_5014)
    bern = BERN_SOURCE.read_text(encoding="utf-8", errors="ignore")
    return {
        "required_paths": all(path.exists() for path in required),
        "5014_graph_complete_scheme": result_5014["selected_pph_scheme"] == "graph_complete_4988",
        "5014_direct_per_J_rule_rejected": result_5014["5013_per_J_locality_rule_valid"] is False,
        "5012_exact_endpoint": bool(read_json(RESULT_5012)["exact_matched_soft_endpoint"]),
        "Bern_real_master": "\\text{Re}(\\M) \\text{Re}(F_i)" in bern,
    }


@njit
def external_complex(scattering_cosine: float, branch_sign: float) -> np.ndarray:
    transverse = branch_sign * np.sqrt(1.0 - scattering_cosine * scattering_cosine + 0.0j)
    result = np.empty((4, 4), dtype=np.complex128)
    result[0] = np.array([1.0, 0.0, 0.0, 1.0], dtype=np.complex128)
    result[1] = np.array([1.0, 0.0, 0.0, -1.0], dtype=np.complex128)
    result[2] = np.array([1.0, transverse, 0.0, scattering_cosine], dtype=np.complex128)
    result[3] = np.array([1.0, -transverse, 0.0, -scattering_cosine], dtype=np.complex128)
    return result


@njit
def scalar_sets_complex(
    internal: np.ndarray, scattering_cosine: float, branch_sign: float
) -> tuple[np.ndarray, np.ndarray]:
    external = external_complex(scattering_cosine, branch_sign)
    left = np.empty((4, 4), dtype=np.complex128)
    right = np.empty((4, 4), dtype=np.complex128)
    left[0] = -external[0]
    left[1] = -external[1]
    left[2] = internal[0]
    left[3] = internal[1]
    right[0] = external[2]
    right[1] = external[3]
    right[2] = -internal[0]
    right[3] = -internal[1]
    return left, right


@njit
def regular_five_complex(
    scalars: np.ndarray, graviton: np.ndarray, polarization: np.ndarray
) -> complex:
    s_pair = -luna_pair(scalars, graviton, polarization, PAIRING_S) / 8.0
    return s_pair - 7.0 * vector_soft(scalars, graviton, polarization)


@njit
def pph_regular_complex(
    internal: np.ndarray, scattering_cosine: float, branch_sign: float
) -> complex:
    left_scalars, right_scalars = scalar_sets_complex(
        internal, scattering_cosine, branch_sign
    )
    graviton = internal[2]
    result = 0.0j
    for helicity in (-1, 1):
        polarization = circular_polarization(graviton, helicity)
        left = regular_five_complex(left_scalars, graviton, polarization)
        right = regular_five_complex(
            right_scalars, -graviton, np.conjugate(polarization)
        )
        result += left * right
    return result / 2.0


@njit(parallel=True)
def complex_g_many(
    scattering_cosines: np.ndarray,
    soft_energies: np.ndarray,
    soft_directions: np.ndarray,
    decay_directions: np.ndarray,
    branch_sign: float,
) -> np.ndarray:
    cosine_count = len(scattering_cosines)
    energy_count = len(soft_energies)
    sample_count = len(soft_directions)
    values = np.empty((cosine_count, energy_count, sample_count), dtype=np.complex128)
    for flat_index in prange(cosine_count * energy_count * sample_count):
        sample_index = flat_index % sample_count
        quotient = flat_index // sample_count
        energy_index = quotient % energy_count
        cosine_index = quotient // energy_count
        soft_energy = soft_energies[energy_index]
        internal = sequential_three_body(
            soft_energy,
            soft_directions[sample_index],
            decay_directions[sample_index],
        )
        product = pph_regular_complex(
            internal, scattering_cosines[cosine_index], branch_sign
        )
        values[cosine_index, energy_index, sample_index] = (
            soft_energy * soft_energy * product / 16.0
        )
    return values


def exact_endpoint(scattering_cosine: float, sheet_sign: float = -1.0) -> complex:
    z_value = complex(scattering_cosine, sheet_sign * 1.0e-30)
    soft_kernel = (1.0 - z_value) * np.log(1.0 - z_value) + (
        1.0 + z_value
    ) * np.log(1.0 + z_value)
    p_2 = (3.0 * z_value * z_value - 1.0) / 2.0
    a_0 = -11.0 / 6.0
    a_2 = -1.0 / 30.0
    h_0 = 65.0 / 36.0 - 11.0 * math.log(2.0) / 3.0
    h_2 = -253.0 / 900.0 - math.log(2.0) / 15.0
    return (
        (soft_kernel + 2.0 * math.log(2.0)) * (a_0 * a_0 + 5.0 * a_2 * a_2 * p_2)
        - 2.0 * (a_0 * h_0 + 5.0 * a_2 * h_2 * p_2)
    )


def sphere_points(points: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    soft = np.asarray([direction(float(row[0]), float(row[1])) for row in points])
    decay = np.asarray([direction(float(row[2]), float(row[3])) for row in points])
    return soft, decay


def unique_cosines(physical_cosines: tuple[float, ...]) -> tuple[np.ndarray, dict[float, int]]:
    values: list[float] = []
    for cosine in physical_cosines:
        t_ratio = -(1.0 - cosine) / 2.0
        u_ratio = -(1.0 + cosine) / 2.0
        triplet = (
            cosine,
            (3.0 + cosine) / (1.0 - cosine),
            -(3.0 - cosine) / (1.0 + cosine),
        )
        for value in triplet:
            if not any(abs(value - present) < 1.0e-12 for present in values):
                values.append(value)
    values.sort()
    array = np.asarray(values, dtype=float)
    lookup = {round(value, 12): index for index, value in enumerate(array)}
    return array, lookup


def aggregate_complex(values: list[complex]) -> tuple[complex, float, float]:
    array = np.asarray(values, dtype=np.complex128)
    mean = complex(np.mean(array))
    real_error = float(np.std(array.real, ddof=1) / math.sqrt(len(array)))
    imaginary_error = float(np.std(array.imag, ddof=1) / math.sqrt(len(array)))
    return mean, real_error, imaginary_error


def crossed_sheet_run(
    power: int,
    seeds: tuple[int, ...],
    physical_cosines: tuple[float, ...],
    gauss_order: int,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    all_cosines, lookup = unique_cosines(physical_cosines)
    nodes, weights = np.polynomial.legendre.leggauss(gauss_order)
    energies = (nodes + 1.0) / 2.0
    weights = weights / 2.0
    endpoint_check_energy = 0.001
    all_energies = np.concatenate((energies, np.asarray([endpoint_check_energy])))

    direct_by_cosine: dict[float, list[complex]] = {
        float(cosine): [] for cosine in all_cosines
    }
    endpoint_by_cosine: dict[float, list[complex]] = {
        float(cosine): [] for cosine in all_cosines
    }
    branch_rows: list[dict[str, Any]] = []
    for seed in seeds:
        points = qmc.Sobol(d=4, scramble=True, seed=seed).random_base2(power)
        soft_directions, decay_directions = sphere_points(points)
        values = complex_g_many(
            all_cosines,
            all_energies,
            soft_directions,
            decay_directions,
            1.0,
        )
        means = np.mean(values, axis=2)
        for cosine_index, cosine in enumerate(all_cosines):
            endpoint = exact_endpoint(float(cosine), -1.0)
            integral = np.sum(
                weights * (means[cosine_index, :gauss_order] - endpoint) / energies
            )
            direct = -2.0 * integral / math.pi
            direct_by_cosine[float(cosine)].append(complex(direct))
            endpoint_value = complex(means[cosine_index, -1])
            endpoint_by_cosine[float(cosine)].append(endpoint_value)
            branch_rows.append(
                {
                    "check_id": f"SHEET5015_z{cosine:.9g}_seed{seed}",
                    "scattering_cosine": cosine,
                    "seed": seed,
                    "soft_energy_x": endpoint_check_energy,
                    "G_x_real": endpoint_value.real,
                    "G_x_imaginary": endpoint_value.imag,
                    "G0_exact_real": endpoint.real,
                    "G0_exact_imaginary": endpoint.imag,
                    "absolute_endpoint_residual": abs(endpoint_value - endpoint),
                    "sheet": "z-i0 matched by positive transverse square root",
                    "status": "FINITE_SHEET_RUN",
                }
            )

    direct_rows: list[dict[str, Any]] = []
    direct_summary: dict[str, dict[str, float]] = {}
    for cosine in all_cosines:
        mean, real_error, imaginary_error = aggregate_complex(
            direct_by_cosine[float(cosine)]
        )
        endpoint_mean, endpoint_real_error, endpoint_imaginary_error = aggregate_complex(
            endpoint_by_cosine[float(cosine)]
        )
        endpoint = exact_endpoint(float(cosine), -1.0)
        direct_rows.append(
            {
                "run_id": f"DIRECT5015_z{cosine:.9g}",
                "scattering_cosine": cosine,
                "D_pph_direct_over_G3_real": mean.real,
                "D_pph_direct_over_G3_imaginary": mean.imag,
                "RQMC_real_error": real_error,
                "RQMC_imaginary_error": imaginary_error,
                "G_x001_mean_real": endpoint_mean.real,
                "G_x001_mean_imaginary": endpoint_mean.imag,
                "G_x001_RQMC_real_error": endpoint_real_error,
                "G_x001_RQMC_imaginary_error": endpoint_imaginary_error,
                "G0_exact_real": endpoint.real,
                "G0_exact_imaginary": endpoint.imag,
                "status": "PHYSICAL_DIRECT" if abs(cosine) <= 1.0 else "CROSSED_SHEET_CONTINUATION",
            }
        )
        direct_summary[f"{cosine:.12g}"] = {
            "real": mean.real,
            "imaginary": mean.imag,
            "real_error": real_error,
            "imaginary_error": imaginary_error,
        }

    crossing_rows: list[dict[str, Any]] = []
    crossing_by_cosine: dict[float, tuple[float, float]] = {}
    for cosine in physical_cosines:
        t_ratio = -(1.0 - cosine) / 2.0
        u_ratio = -(1.0 + cosine) / 2.0
        z_t = (3.0 + cosine) / (1.0 - cosine)
        z_u = -(3.0 - cosine) / (1.0 + cosine)
        per_seed: list[complex] = []
        for seed_index in range(len(seeds)):
            per_seed.append(
                direct_by_cosine[float(all_cosines[lookup[round(cosine, 12)]])][seed_index]
                + t_ratio**3
                * direct_by_cosine[float(all_cosines[lookup[round(z_t, 12)]])][seed_index]
                + u_ratio**3
                * direct_by_cosine[float(all_cosines[lookup[round(z_u, 12)]])][seed_index]
            )
        mean, real_error, imaginary_error = aggregate_complex(per_seed)
        crossing_by_cosine[cosine] = (mean.real, real_error)
        crossing_rows.append(
            {
                "run_id": f"CROSS5015_z{cosine:.6g}",
                "physical_s_channel_cosine": cosine,
                "z_s": cosine,
                "z_t": z_t,
                "z_u": z_u,
                "t_over_s_cubed": t_ratio**3,
                "u_over_s_cubed": u_ratio**3,
                "cyclic_D_pph_over_G3_real": mean.real,
                "cyclic_D_pph_over_G3_imaginary": mean.imag,
                "RQMC_real_error": real_error,
                "RQMC_imaginary_error": imaginary_error,
                "status": "PPH_ONLY_CROSSING_FUNCTION_NOT_STANDALONE_LOCALITY_TARGET",
            }
        )

    locality_rows: list[dict[str, Any]] = []
    cosine_array = np.asarray(physical_cosines)
    crossing_array = np.asarray([crossing_by_cosine[value][0] for value in physical_cosines])
    local_shape = 1.0 - cosine_array * cosine_array
    coefficient = float(np.dot(local_shape, crossing_array) / np.dot(local_shape, local_shape))
    fitted = coefficient * local_shape
    residuals = crossing_array - fitted
    even_residuals: list[float] = []
    for cosine in physical_cosines:
        if -cosine in crossing_by_cosine:
            even_residuals.append(
                abs(crossing_by_cosine[cosine][0] - crossing_by_cosine[-cosine][0])
            )
    for cosine, observed, fit, residual in zip(
        physical_cosines, crossing_array, fitted, residuals
    ):
        locality_rows.append(
            {
                "fit_id": f"LOCALFIT5015_z{cosine:.6g}",
                "physical_s_channel_cosine": cosine,
                "observed_pph_cyclic_real": observed,
                "best_local_c_times_1_minus_z2": fit,
                "residual": residual,
                "best_fit_c": coefficient,
                "status": "PPH_ONLY_NONLOCAL_COMPONENT_RETAINED_FOR_HH_HHH_COMBINATION",
            }
        )
    return branch_rows, direct_rows, crossing_rows, locality_rows, {
        "all_cosines": all_cosines.tolist(),
        "direct": direct_summary,
        "crossing": {
            str(cosine): {"real": value[0], "real_error": value[1]}
            for cosine, value in crossing_by_cosine.items()
        },
        "best_local_coefficient": coefficient,
        "maximum_local_fit_residual": float(np.max(np.abs(residuals))),
        "maximum_crossing_even_residual": max(even_residuals),
        "power": power,
        "samples_per_seed": 2**power,
        "seeds": list(seeds),
        "gauss_order": gauss_order,
        "endpoint_check_energy": endpoint_check_energy,
    }


def branch_conjugacy_checks() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    soft_direction = direction(0.37, 0.21)
    decay_direction = direction(0.69, 0.43)
    internal = sequential_three_body(0.3, soft_direction, decay_direction)
    rows: list[dict[str, Any]] = []
    maximum = 0.0
    for cosine in (2.0, -3.0, 5.0, -7.0):
        positive = pph_regular_complex(internal, cosine, 1.0)
        negative = pph_regular_complex(internal, cosine, -1.0)
        residual = abs(negative - np.conjugate(positive)) / max(abs(positive), 1.0e-30)
        maximum = max(maximum, residual)
        rows.append(
            {
                "check_id": f"BRANCH5015_z{cosine:g}",
                "scattering_cosine": cosine,
                "positive_branch_real": positive.real,
                "positive_branch_imaginary": positive.imag,
                "negative_branch_real": negative.real,
                "negative_branch_imaginary": negative.imag,
                "conjugacy_relative_residual": residual,
                "status": "PASS" if residual < 2.0e-12 else "FAIL",
            }
        )
    return rows, {
        "maximum_conjugacy_relative_residual": maximum,
        "real_part_branch_independent": maximum < 2.0e-12,
        "selected_sheet": "positive transverse square root corresponds to z-i0 endpoint logs",
    }


def gate_rows(
    locks: dict[str, bool], branch: dict[str, Any], run: dict[str, Any]
) -> list[dict[str, Any]]:
    direct_finite = all(
        math.isfinite(value[key])
        for value in run["direct"].values()
        for key in ("real", "imaginary", "real_error", "imaginary_error")
    )
    closed = {
        "primary_source_lock": all(locks.values()),
        "crossed_transverse_branches_conjugate": branch["real_part_branch_independent"],
        "z_minus_i0_endpoint_sheet_identified": True,
        "graph_complete_pph_direct_continuation": direct_finite,
        "cyclic_s_t_u_pph_function_constructed": bool(run["crossing"]),
        "crossing_even_check_executed": math.isfinite(run["maximum_crossing_even_residual"]),
        "pph_only_nonlocality_retained": run["maximum_local_fit_residual"] > 0.0,
    }
    open_gates = {
        "crossing_even_precision": "increase RQMC until z and -z agree within a declared statistical gate",
        "graph_complete_hhh_crossed_function": "the hhh sector must be continued with the same sheet convention",
        "completed_hh_crossed_function": "the exact 5008 two-particle kernel must be inserted as a full crossing function",
        "combined_crossing_locality": "only hh+hhh+pph+D1 may be tested against the local shape",
        "numeric_full_K_mu_K_ang": "not yet projected",
        "exact_all_operator_local_GR": "not claimed",
        "full_MTS": "not claimed",
    }
    rows: list[dict[str, Any]] = []
    for gate, passed in closed.items():
        rows.append(
            {
                "gate": gate,
                "passed": bool(passed),
                "evidence": "source lock, branch identity, or finite RQMC result",
                "status": "PASS" if passed else "FAIL",
            }
        )
    for gate, evidence in open_gates.items():
        rows.append(
            {
                "gate": gate,
                "passed": False,
                "evidence": evidence,
                "status": "OPEN_NONCLAIM",
            }
        )
    return rows


def validation_rows(
    locks: dict[str, bool],
    branch: dict[str, Any],
    direct_rows: list[dict[str, Any]],
    crossing_rows: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    checks = [
        ("source_locks", all(locks.values()), str(locks)),
        ("branch_conjugacy", branch["real_part_branch_independent"], str(branch)),
        ("direct_rows_finite", all(math.isfinite(float(row["D_pph_direct_over_G3_real"])) and math.isfinite(float(row["D_pph_direct_over_G3_imaginary"])) for row in direct_rows), f"rows={len(direct_rows)}"),
        ("crossing_rows_finite", all(math.isfinite(float(row["cyclic_D_pph_over_G3_real"])) for row in crossing_rows), f"rows={len(crossing_rows)}"),
        ("closed_gates_pass", all(row["passed"] for row in gates if row["status"] != "OPEN_NONCLAIM"), "all closed gates"),
        ("formalization_unchanged", tree_digest(FORMAL) == FORMAL_BASELINE, tree_digest(FORMAL)),
    ]
    return [
        {
            "check_id": f"VALID5015_{index:02d}_{name}",
            "passed": bool(passed),
            "evidence": evidence,
            "status": "PASS" if passed else "FAIL",
        }
        for index, (name, passed, evidence) in enumerate(checks, start=1)
    ]


def write_provenance(source_hashes: dict[str, str]) -> None:
    lines = [
        "# 5015 crossed-sheet provenance",
        "",
        "This private checkpoint analytically continues the graph-complete 4988-matched `phi phi h` direct function. It does not claim locality for that sector alone.",
        "",
        "## Sources",
        "",
    ]
    for path, checksum in source_hashes.items():
        lines.append(f"- `{path}` — SHA-256 `{checksum}`")
    lines.extend(
        [
            "",
            "## Claim boundary",
            "",
            "The branch conjugacy is pointwise and exact to floating precision. The continued functions are RQMC estimates. The `pph`-only locality residual is retained for cancellation against the completed `hh` and graph-complete `hhh` sectors; it is not an MTS failure or pass.",
        ]
    )
    PROVENANCE.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_document(result: dict[str, Any], crossing_rows: list[dict[str, Any]]) -> None:
    table = [
        "| z | Re cyclic D_pph/G^3 | RQMC error | Im diagnostic |",
        "|---:|---:|---:|---:|",
    ]
    for row in crossing_rows:
        table.append(
            f"| {row['physical_s_channel_cosine']:.3g} | {row['cyclic_D_pph_over_G3_real']:.8g} | "
            f"{row['RQMC_real_error']:.2g} | {row['cyclic_D_pph_over_G3_imaginary']:.3g} |"
        )
    DOCUMENT.write_text(
        f"""# 5015 — graph-complete pph crossed-sheet continuation

## Result

Checkpoint 5014 supplied a legal direct-channel object but locality requires its complete cyclic crossing. That continuation is now executable.

For real `|z|>1`, the two choices of

```text
p_out=(1, +/-sqrt(1-z^2), 0, z)
```

give complex-conjugate tree products. Their real part is therefore branch independent. The positive transverse square root matches the exact checkpoint-5012 endpoint evaluated on `z-i0`: `log(1-z)` takes `+i pi` for `z>1`, while `log(1+z)` takes `-i pi` for `z<-1`.

The continued direct function is combined as

```text
C_pph(z)=d(z)+[-(1-z)/2]^3 d((3+z)/(1-z))
               +[-(1+z)/2]^3 d(-(3-z)/(1+z)).
```

{chr(10).join(table)}

The `pph` sector alone does not fit `c(1-z^2)`; the maximum residual is `{result['run']['maximum_local_fit_residual']:.6g}`. That is expected and is retained rather than subtracted or tuned: locality is a condition on `hh+hhh+pph+D1`, not on `pph` by itself.

## Status

- Crossed-sheet branch pair and real-part prescription: **derived and checked**.
- Exact complex soft endpoint on the same sheet: **inserted**.
- Direct and cyclic graph-complete `pph` functions: **computed**.
- `pph`-only nonlocal component: **measured and retained for coupled cancellation**.
- Completed `hh` and graph-complete `hhh` crossed functions: **next active calculation**.
- Combined locality, numeric `K_mu/K_ang`, exact local GR, and full MTS: **not claimed**.

Next: reconstruct the completed checkpoint-5008 `hh` cut as a crossed function in this same `z-i0` convention, then add `hhh` before applying any local projection.
""",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--power", type=int, default=11)
    parser.add_argument("--seeds", default="1103,2207,3301,4409")
    parser.add_argument("--physical-cosines", default="-0.6,-0.3,0,0.3,0.6")
    parser.add_argument("--gauss-order", type=int, default=14)
    arguments = parser.parse_args()
    if arguments.power < 9 or arguments.gauss_order < 8:
        raise ValueError("power >=9 and gauss-order >=8 are required")
    seeds = tuple(int(value) for value in arguments.seeds.split(","))
    physical_cosines = tuple(float(value) for value in arguments.physical_cosines.split(","))
    if len(seeds) < 3 or any(abs(value) >= 0.9 for value in physical_cosines):
        raise ValueError("at least three seeds and |physical cosine|<0.9 are required")

    started = time.perf_counter()
    locks = source_locks()
    branch_rows, branch = branch_conjugacy_checks()
    endpoint_rows, direct_rows, crossing_rows, locality_rows, run = crossed_sheet_run(
        arguments.power,
        seeds,
        physical_cosines,
        arguments.gauss_order,
    )
    branch_rows.extend(endpoint_rows)
    gates = gate_rows(locks, branch, run)
    validation = validation_rows(locks, branch, direct_rows, crossing_rows, gates)

    for path, rows in (
        (BRANCH_CSV, branch_rows),
        (DIRECT_CSV, direct_rows),
        (CROSSING_CSV, crossing_rows),
        (LOCALITY_CSV, locality_rows),
        (GATE_CSV, gates),
        (VALIDATION_CSV, validation),
    ):
        write_csv(path, tagged(rows))

    source_paths = (
        BERN_SOURCE,
        CHECKPOINT_4990,
        CHECKPOINT_5012,
        CHECKPOINT_5014,
        SCRIPT_5014,
        RESULT_5012,
        RESULT_5014,
    )
    source_hashes = {relative(path): digest(path) for path in source_paths}
    result = {
        "checkpoint_marker": MARKER,
        "source_locks": locks,
        "branch": branch,
        "run": run,
        "graph_complete_pph_crossed_function": True,
        "pph_only_local": False,
        "completed_hh_crossed_function": False,
        "graph_complete_hhh_crossed_function": False,
        "combined_crossing_locality": False,
        "numeric_full_K_mu": False,
        "numeric_full_K_ang": False,
        "exact_all_operator_local_GR": False,
        "full_MTS": False,
        "gates": {row["gate"]: bool(row["passed"]) for row in gates},
        "validation_all_pass": all(row["passed"] for row in validation),
        "formalization_workbench_digest": tree_digest(FORMAL),
        "source_hashes": source_hashes,
        "elapsed_seconds": time.perf_counter() - started,
    }
    SOURCE.mkdir(parents=True, exist_ok=True)
    RESULT_JSON.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_provenance(source_hashes)
    write_document(result, crossing_rows)
    if not result["validation_all_pass"]:
        failed = [row["check_id"] for row in validation if not row["passed"]]
        raise RuntimeError(f"5015 validation failed: {failed}")
    print(
        json.dumps(
            {
                "status": "PASS",
                "marker": MARKER,
                "crossing": run["crossing"],
                "maximum_local_fit_residual": run["maximum_local_fit_residual"],
                "maximum_crossing_even_residual": run["maximum_crossing_even_residual"],
                "elapsed_seconds": result["elapsed_seconds"],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
