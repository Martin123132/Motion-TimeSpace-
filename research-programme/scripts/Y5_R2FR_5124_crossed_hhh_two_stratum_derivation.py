from __future__ import annotations

import argparse
import cmath
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


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE = POST / "source-intake" / "functional_rg" / "5124"
RESIDUALS = POST / "source-intake" / "mts_residuals"

HIGH_RUN = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5079"
    / "runs"
    / "bounded_central_anchor_pilot_v12"
)
CONTROL_RUN = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5111"
    / "runs"
    / "E020_primary_complex_control_extension_v1"
)
RESULT_5123 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5123"
    / "physical_hhh_angular_first_and_crossed_remainder_results.json"
)
ROWS_5123 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5123"
    / "physical_replacement_crossed_remainder_rows.csv"
)
SCRIPT_5034 = (
    POST / "scripts" / "Y5_R2FR_5034_bounded_adaptive_outer_phase_space_smoke.py"
)
SCRIPT_5077 = POST / "scripts" / "Y5_R2FR_5077_central_anchor_pilot_runner.py"
SOURCE_GRAVITY = (
    POST
    / "source-intake"
    / "functional_rg"
    / "4985"
    / "sources"
    / "bern"
    / "gr_simp.tex"
)
CHECKPOINT_4987 = (
    POST
    / "4987-Y5-R2FR-full-finite-scheme-orbit-and-irreducible-two-loop-cut-reduction.md"
)
CHECKPOINT_5123 = (
    POST / "5123-Y5-R2FR-physical-hhh-angular-first-and-crossed-remainder-audit.md"
)

CYCLIC_CSV = SOURCE / "crossed_hhh_component_cyclic_rows.csv"
LOCAL_CSV = SOURCE / "crossed_hhh_local_stratum_rows.csv"
SUMMARY_CSV = SOURCE / "crossed_hhh_component_summary.csv"
RECIPROCAL_CSV = SOURCE / "reciprocal_residue_pair_audit.csv"
PLAIN_BENCHMARK_JSON = SOURCE / "topological_only_production_gate_benchmark.json"
BENCHMARK_JSON = SOURCE / "reciprocal_reduced_topological_benchmark.json"
RESULT_JSON = SOURCE / "crossed_hhh_two_stratum_derivation.json"
PROVENANCE = SOURCE / "PROVENANCE.md"
DOCUMENT = POST / "5124-Y5-R2FR-crossed-hhh-two-stratum-derivation.md"
VALIDATION_CSV = RESIDUALS / "P8_Y5_BRR545_5124_VALIDATION.csv"

MARKER = "MTS_5124_CROSSED_HHH_TWO_STRATUM_DERIVATION"
CHECKED_DATE = "2026-07-19"
FORMAL_BASELINE = "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
KERNEL_MULTIPLIER = -2.0 / math.pi
PHYSICAL_COSINES = np.asarray((-0.6, -0.3, 0.0, 0.3, 0.6), dtype=float)
PRODUCTION_SEEDS = (507601, 507602, 507603, 507604)
DESIGN_SEEDS = (
    507601,
    507602,
    507603,
    507604,
    507611,
    507612,
    507613,
    507614,
    507615,
    507616,
    507617,
    507618,
    507619,
    507620,
    507621,
    507622,
)
COMPONENTS = ("topological", "pole_model", "smooth", "naive", "total")


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


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True, default=json_default),
        encoding="utf-8",
    )


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


def json_default(value: Any) -> Any:
    if isinstance(value, np.generic):
        return value.item()
    if isinstance(value, complex):
        return complex_row(value)
    raise TypeError(type(value).__name__)


def complex_row(value: complex) -> dict[str, float]:
    return {"real": float(value.real), "imaginary": float(value.imag)}


def tagged(row: dict[str, Any]) -> dict[str, Any]:
    return {
        **row,
        "checkpoint_marker": MARKER,
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
        "source_checked_date": CHECKED_DATE,
    }


def continuous_log_difference(start: complex, end: complex, pole: complex) -> complex:
    start_vector = start - pole
    end_vector = end - pole
    phase_difference = cmath.phase(end_vector) - cmath.phase(start_vector)
    phase_difference = math.atan2(
        math.sin(phase_difference), math.cos(phase_difference)
    )
    return complex(
        math.log(abs(end_vector) / abs(start_vector)), phase_difference
    )


def split_kernel(path: Path) -> tuple[dict[str, complex], float]:
    gate = read_json(path)["fixed_event_integral_gate"]
    order = gate["order_rows"][-1]
    naive = complex(order["regularized_naive_value"])
    topological = complex(order["topological_correction"])
    pole_model = 0.0j
    for chamber in gate["chambers"]:
        start = complex(chamber["start_log"])
        end = complex(chamber["end_log"])
        for row in chamber["residue_catalog"]:
            if not row["included_as_pole_model"]:
                continue
            pole_model += (
                complex(row["residue"])
                * continuous_log_difference(
                    start, end, complex(row["log_point"])
                )
                / (2.0j * math.pi)
            )
    smooth = naive - pole_model
    total = naive + topological
    closure = abs(topological + pole_model + smooth - total)
    raw = {
        "topological": topological,
        "pole_model": pole_model,
        "smooth": smooth,
        "naive": naive,
        "total": total,
    }
    return {key: KERNEL_MULTIPLIER * value for key, value in raw.items()}, closure


def input_paths(
    seed: int, epsilon_id: str, argument_id: str, e040_profile: str
) -> tuple[Path, Path]:
    if epsilon_id == "E020":
        run = HIGH_RUN if seed in PRODUCTION_SEEDS else CONTROL_RUN
        profile = "primary24"
    else:
        run = HIGH_RUN
        profile = e040_profile
    stem = f"{epsilon_id}__S{seed}_N0000__{argument_id}__{profile}.json"
    return run / "kernels" / stem, run / "jobs" / stem


def checked_components(
    seed: int,
    epsilon_id: str,
    argument_id: str,
    e040_profile: str,
) -> tuple[dict[str, complex], float, tuple[Path, Path]]:
    kernel, job = input_paths(seed, epsilon_id, argument_id, e040_profile)
    job_row = read_json(job)
    if job_row["status"] != "COMPLETED_CONVERGED":
        raise RuntimeError(f"non-converged source row: {job}")
    values, closure = split_kernel(kernel)
    return values, closure, (kernel, job)


def matrix_rows(
    matrix_id: str,
    seeds: tuple[int, ...],
    e040_profile: str,
    config: dict[str, Any],
) -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    dict[str, np.ndarray],
    float,
    set[Path],
]:
    argument_lookup = {
        round(float(row["argument"]), 12): row["argument_id"]
        for row in config["base_arguments"]
    }
    event_lookup = {int(row["seed"]): row for row in config["events"]}
    shape = 1.0 - PHYSICAL_COSINES**2
    local_weights = shape / float(shape @ shape)
    cyclic_rows: list[dict[str, Any]] = []
    local_rows: list[dict[str, Any]] = []
    local_values: dict[str, list[complex]] = {key: [] for key in COMPONENTS}
    maximum_closure = 0.0
    used_paths: set[Path] = set()

    def extrapolated(seed: int, argument: float) -> dict[str, complex]:
        nonlocal maximum_closure
        argument_id = argument_lookup[round(float(argument), 12)]
        e020, closure_020, paths_020 = checked_components(
            seed, "E020", argument_id, e040_profile
        )
        e040, closure_040, paths_040 = checked_components(
            seed, "E040", argument_id, e040_profile
        )
        maximum_closure = max(maximum_closure, closure_020, closure_040)
        used_paths.update(paths_020)
        used_paths.update(paths_040)
        return {key: 2.0 * e020[key] - e040[key] for key in COMPONENTS}

    for seed in seeds:
        cyclic: dict[str, list[complex]] = {key: [] for key in COMPONENTS}
        for cosine in PHYSICAL_COSINES:
            t_ratio = -(1.0 - cosine) / 2.0
            u_ratio = -(1.0 + cosine) / 2.0
            z_t = (3.0 + cosine) / (1.0 - cosine)
            z_u = -(3.0 - cosine) / (1.0 + cosine)
            t_value = extrapolated(seed, z_t)
            u_value = extrapolated(seed, z_u)
            values = {
                key: t_ratio**3 * t_value[key] + u_ratio**3 * u_value[key]
                for key in COMPONENTS
            }
            for key, value in values.items():
                cyclic[key].append(value)
            cyclic_closure = abs(
                values["topological"]
                + values["pole_model"]
                + values["smooth"]
                - values["total"]
            )
            maximum_closure = max(maximum_closure, cyclic_closure)
            cyclic_rows.append(
                tagged(
                    {
                        "matrix_id": matrix_id,
                        "seed": seed,
                        "physical_cosine": cosine,
                        "e040_profile": e040_profile,
                        **{
                            f"{key}_real": values[key].real
                            for key in COMPONENTS
                        },
                        **{
                            f"{key}_imaginary": values[key].imag
                            for key in COMPONENTS
                        },
                        "component_closure": cyclic_closure,
                        "status": "EXACT_LINEAR_DECOMPOSITION",
                    }
                )
            )

        coefficients = {
            key: complex(np.asarray(values, dtype=np.complex128) @ local_weights)
            for key, values in cyclic.items()
        }
        residuals = {
            key: float(
                np.linalg.norm(
                    np.asarray(cyclic[key], dtype=np.complex128)
                    - coefficients[key] * shape
                )
            )
            for key in COMPONENTS
        }
        local_closure = abs(
            coefficients["topological"]
            + coefficients["pole_model"]
            + coefficients["smooth"]
            - coefficients["total"]
        )
        maximum_closure = max(maximum_closure, local_closure)
        for key, value in coefficients.items():
            local_values[key].append(value)
        event = event_lookup[seed]
        local_rows.append(
            tagged(
                {
                    "matrix_id": matrix_id,
                    "seed": seed,
                    "soft_energy": event["soft_energy"],
                    "soft_cosine": event["soft_cosine"],
                    "decay_cosine": event["decay_cosine"],
                    "e040_profile": e040_profile,
                    **{
                        f"{key}_local_real": coefficients[key].real
                        for key in COMPONENTS
                    },
                    **{
                        f"{key}_local_imaginary": coefficients[key].imag
                        for key in COMPONENTS
                    },
                    **{
                        f"{key}_nonlocal_norm": residuals[key]
                        for key in COMPONENTS
                    },
                    "component_closure": local_closure,
                    "status": "DESIGN_DIAGNOSTIC_NOT_COEFFICIENT_CLAIM",
                }
            )
        )

    return (
        cyclic_rows,
        local_rows,
        {
            key: np.asarray(value, dtype=np.complex128)
            for key, value in local_values.items()
        },
        maximum_closure,
        used_paths,
    )


def component_summary(
    matrix_id: str, values: dict[str, np.ndarray]
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    count = len(next(iter(values.values())))
    for component, array in values.items():
        rows.append(
            tagged(
                {
                    "matrix_id": matrix_id,
                    "component": component,
                    "sample_count": count,
                    "mean_real": float(np.mean(array.real)),
                    "mean_imaginary": float(np.mean(array.imag)),
                    "sample_sd_real": float(np.std(array.real, ddof=1)),
                    "sample_sd_imaginary": float(np.std(array.imag, ddof=1)),
                    "standard_error_real": float(
                        np.std(array.real, ddof=1) / math.sqrt(count)
                    ),
                    "standard_error_imaginary": float(
                        np.std(array.imag, ddof=1) / math.sqrt(count)
                    ),
                    "status": "DESIGN_VARIANCE_ONLY",
                }
            )
        )
    return rows


def correlation(first: np.ndarray, second: np.ndarray, part: str) -> float:
    left = first.real if part == "real" else first.imag
    right = second.real if part == "real" else second.imag
    return float(np.corrcoef(left, right)[0, 1])


def load_module(path: Path, name: str) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def reciprocal_unsafe_pairs(pairs: list[list[str]]) -> bool:
    if len(pairs) != 1:
        return True
    labels = set(pairs[0])
    return any(label.startswith("direct:g2:") for label in labels) and any(
        label.startswith("subtraction:decay:") for label in labels
    )


def pair_reciprocal_entries(entries: list[dict[str, Any]]) -> list[tuple[dict[str, Any], dict[str, Any], float]]:
    used: set[int] = set()
    pairs: list[tuple[dict[str, Any], dict[str, Any], float]] = []
    for index, first in enumerate(entries):
        if index in used:
            continue
        root = complex(first["target_root"])
        inverse = 1.0 / root
        candidates = [
            (
                abs(complex(second["target_root"]) - inverse)
                / max(1.0, abs(inverse), abs(complex(second["target_root"]))),
                second_index,
                second,
            )
            for second_index, second in enumerate(entries)
            if second_index != index and second_index not in used
        ]
        if not candidates:
            raise RuntimeError("reciprocal crossing partner is absent")
        residual, partner_index, partner = min(candidates, key=lambda row: row[0])
        if residual > 2.0e-8:
            raise RuntimeError(
                f"reciprocal crossing partner fails: {root}, {inverse}, {residual}"
            )
        used.update((index, partner_index))
        pairs.append((first, partner, residual))
    if len(used) != len(entries):
        raise RuntimeError("reciprocal pairing did not consume all crossings")
    return pairs


def reciprocal_matrix_audit() -> tuple[list[dict[str, Any]], dict[str, Any], set[Path]]:
    rows: list[dict[str, Any]] = []
    paths: set[Path] = set()
    safe_pairs = 0
    unsafe_pairs = 0
    safe_failures = 0
    maximum_root_residual = 0.0
    maximum_safe_residue_residual = 0.0
    maximum_reconstruction_residual = 0.0
    file_count = 0
    correction_row_count = 0
    for directory in (HIGH_RUN / "kernels", CONTROL_RUN / "kernels"):
        for path in sorted(directory.glob("*.json")):
            file_count += 1
            paths.add(path)
            gate = read_json(path)["fixed_event_integral_gate"]
            entries: list[dict[str, Any]] = []
            for chamber in gate["chambers"]:
                for correction in chamber["correction_rows"]:
                    root = complex(correction["target_root"])
                    catalog = min(
                        chamber["residue_catalog"],
                        key=lambda row: abs(complex(row["root"]) - root),
                    )
                    entries.append(
                        {
                            **correction,
                            "chamber_index": chamber["chamber_index"],
                            "pairs": catalog["pairs"],
                        }
                    )
            correction_row_count += len(entries)
            actual = sum((complex(row["contribution"]) for row in entries), 0.0j)
            reconstructed = 0.0j
            for pair_index, (first, second, root_residual) in enumerate(
                pair_reciprocal_entries(entries)
            ):
                first_residue = complex(first["residue"])
                second_residue = complex(second["residue"])
                residue_scale = max(1.0, abs(first_residue), abs(second_residue))
                residue_residual = abs(first_residue + second_residue) / residue_scale
                unsafe = reciprocal_unsafe_pairs(first["pairs"]) or reciprocal_unsafe_pairs(
                    second["pairs"]
                )
                if unsafe:
                    unsafe_pairs += 1
                    pair_value = (
                        int(first["winding_correction"]) * first_residue
                        + int(second["winding_correction"]) * second_residue
                    )
                else:
                    safe_pairs += 1
                    maximum_safe_residue_residual = max(
                        maximum_safe_residue_residual, residue_residual
                    )
                    if residue_residual > 2.0e-6:
                        safe_failures += 1
                    pair_value = (
                        int(first["winding_correction"])
                        - int(second["winding_correction"])
                    ) * first_residue
                reconstructed += pair_value
                maximum_root_residual = max(maximum_root_residual, root_residual)
                rows.append(
                    tagged(
                        {
                            "kernel_path": relative(path),
                            "pair_index": pair_index,
                            "first_root": first["target_root"],
                            "second_root": second["target_root"],
                            "reciprocal_root_residual": root_residual,
                            "first_pairs": json.dumps(first["pairs"]),
                            "second_pairs": json.dumps(second["pairs"]),
                            "first_winding": first["winding_correction"],
                            "second_winding": second["winding_correction"],
                            "residue_antisymmetry_residual": residue_residual,
                            "safe_for_reciprocal_reduction": not unsafe,
                            "pair_reconstructed_real": pair_value.real,
                            "pair_reconstructed_imaginary": pair_value.imag,
                            "status": (
                                "RECIPROCAL_REDUCED"
                                if not unsafe
                                else "FAIL_CLOSED_EVALUATE_BOTH"
                            ),
                        }
                    )
                )
            reconstruction_residual = abs(reconstructed - actual) / max(
                1.0, abs(actual)
            )
            maximum_reconstruction_residual = max(
                maximum_reconstruction_residual, reconstruction_residual
            )
    return rows, {
        "kernel_file_count": file_count,
        "correction_row_count": correction_row_count,
        "reciprocal_pair_count": safe_pairs + unsafe_pairs,
        "safe_pair_count": safe_pairs,
        "unsafe_pair_count": unsafe_pairs,
        "safe_pair_fraction": safe_pairs / (safe_pairs + unsafe_pairs),
        "safe_pair_failures": safe_failures,
        "maximum_reciprocal_root_residual": maximum_root_residual,
        "maximum_safe_residue_antisymmetry_residual": maximum_safe_residue_residual,
        "maximum_topological_reconstruction_relative_residual": maximum_reconstruction_residual,
        "safe_theorem": "for isolated non-g2/decay reciprocal pairs, Res(1/r)=-Res(r); use both stored windings",
        "unsafe_policy": "multi-root clusters and direct:g2/subtraction:decay pairs evaluate both fail-closed",
    }, paths


def topological_only_value(
    module: Any,
    topology: dict[str, Any],
    profile: dict[str, Any],
) -> tuple[complex, bool, int]:
    _, ownerships = module.physical_chambers()
    total = 0.0j
    all_stable = True
    catalog_rows = 0
    for chamber_index, ownership in enumerate(ownerships):
        chamber = topology["chambers"][chamber_index]
        start = complex(chamber["target_start_log"])
        end = complex(chamber["target_end_log"])
        crossings = chamber["surface_crossings"]
        catalog, stable = module.chamber_residue_catalog(
            ownership,
            start,
            end,
            [complex(row["target_root"]) for row in crossings],
            int(profile["global_nodes"]),
            int(profile["global_residue_nodes"]),
            int(profile["relative_residue_nodes"]),
            float(profile["model_distance"]),
        )
        all_stable = all_stable and stable
        catalog_rows += len(catalog)
        for crossing in crossings:
            root = complex(crossing["target_root"])
            match = min(catalog, key=lambda row: abs(row["root"] - root))
            matching_residual = abs(match["root"] - root) / max(
                1.0, abs(root), abs(match["root"])
            )
            if matching_residual > 2.0e-5:
                raise RuntimeError("topological-only crossing root mismatch")
            total += crossing["winding_correction"] * match["residue"]
    return total, all_stable, catalog_rows


def reciprocal_reduced_topological_value(
    module: Any,
    topology: dict[str, Any],
    profile: dict[str, Any],
) -> tuple[complex, bool, int, int, int]:
    entries: list[dict[str, Any]] = []
    for chamber_index, chamber in enumerate(topology["chambers"]):
        for crossing in chamber["surface_crossings"]:
            entries.append({**crossing, "chamber_index": chamber_index})
    reciprocal_pairs = pair_reciprocal_entries(entries)

    selected: dict[int, list[complex]] = {
        index: [] for index in range(len(topology["chambers"]))
    }
    contracts: list[dict[str, Any]] = []
    safe_pair_count = 0
    unsafe_pair_count = 0
    for first, second, _ in reciprocal_pairs:
        unsafe = reciprocal_unsafe_pairs(first["representing_pairs"]) or reciprocal_unsafe_pairs(
            second["representing_pairs"]
        )
        if unsafe:
            unsafe_pair_count += 1
            selected[first["chamber_index"]].append(complex(first["target_root"]))
            selected[second["chamber_index"]].append(complex(second["target_root"]))
            contracts.append(
                {"safe": False, "first": first, "second": second}
            )
            continue
        safe_pair_count += 1
        representative, partner = (
            (first, second)
            if abs(complex(first["target_root"])) >= 1.0
            else (second, first)
        )
        selected[representative["chamber_index"]].append(
            complex(representative["target_root"])
        )
        contracts.append(
            {
                "safe": True,
                "representative": representative,
                "partner": partner,
            }
        )

    _, ownerships = module.physical_chambers()
    residues: dict[tuple[int, complex], complex] = {}
    all_stable = True
    catalog_rows = 0
    for chamber_index, ownership in enumerate(ownerships):
        required_roots = selected[chamber_index]
        if not required_roots:
            continue
        chamber = topology["chambers"][chamber_index]
        catalog, stable = module.chamber_residue_catalog(
            ownership,
            complex(chamber["target_start_log"]),
            complex(chamber["target_end_log"]),
            required_roots,
            int(profile["global_nodes"]),
            int(profile["global_residue_nodes"]),
            int(profile["relative_residue_nodes"]),
            -1.0,
        )
        all_stable = all_stable and stable
        catalog_rows += len(catalog)
        for root in required_roots:
            match = min(catalog, key=lambda row: abs(complex(row["root"]) - root))
            matching_residual = abs(complex(match["root"]) - root) / max(
                1.0, abs(root), abs(complex(match["root"]))
            )
            if matching_residual > 2.0e-5:
                raise RuntimeError("reciprocal-reduced residue root mismatch")
            residues[(chamber_index, root)] = complex(match["residue"])

    total = 0.0j
    for contract in contracts:
        if contract["safe"]:
            representative = contract["representative"]
            partner = contract["partner"]
            residue = residues[
                (
                    representative["chamber_index"],
                    complex(representative["target_root"]),
                )
            ]
            total += (
                int(representative["winding_correction"])
                - int(partner["winding_correction"])
            ) * residue
        else:
            first = contract["first"]
            second = contract["second"]
            total += int(first["winding_correction"]) * residues[
                (first["chamber_index"], complex(first["target_root"]))
            ]
            total += int(second["winding_correction"]) * residues[
                (second["chamber_index"], complex(second["target_root"]))
            ]
    return (
        total,
        all_stable,
        catalog_rows,
        safe_pair_count,
        unsafe_pair_count,
    )


def production_benchmark() -> dict[str, Any]:
    runner = load_module(SCRIPT_5077, "mts_5077_for_5124")
    runner.install_history_invariant_breakpoints(runner.M5036.N5030)
    config = read_json(HIGH_RUN / "config.json")
    event = next(row for row in config["events"] if row["seed"] == 507602)
    argument = next(
        row for row in config["arguments"] if row["argument_id"] == "E020_A00"
    )
    topology_path = HIGH_RUN / "topologies" / "S507602_N0000__E020_A00.json"
    topology = read_json(topology_path)
    job_key = "E020__S507602_N0000__A00__primary24"
    kernel_path = HIGH_RUN / "kernels" / f"{job_key}.json"
    stored_gate = read_json(kernel_path)["fixed_event_integral_gate"]
    target = complex(
        argument["target_cosine"]["real"], argument["target_cosine"]["imaginary"]
    )
    runner.CURRENT_EVENT = event
    runner.CURRENT_ARGUMENT = argument
    module = runner.M5036.N5030
    runner.M5036.M5035.M5034.configure(event, target)
    profile = config["tiers"]["primary24"]
    previous_catalog = module.chamber_residue_catalog
    previous_global_value = module.global_chamber_value
    module.chamber_residue_catalog = runner.certified_primary_catalog
    runner.M5036.MREPAIR.CURRENT_JOB = job_key
    runner.M5036.MREPAIR.RADIUS_AUDIT.clear()
    runner.LOCAL_RESIDUE_RESOLUTION_AUDIT.clear()
    runner.OUTWARD_CONTOUR_AUDIT.clear()
    runner.PROJECTIVE_CLUSTER_ZERO_AUDIT.clear()
    runner.removable_extension_gate()
    module.global_chamber_value = runner.M5085.CertifiedRemovableGlobalExtension(
        previous_global_value
    )
    try:
        warm_started = time.perf_counter()
        (
            warm_value,
            warm_stable,
            _,
            _,
            _,
        ) = reciprocal_reduced_topological_value(
            module, topology, profile
        )
        warm_seconds = time.perf_counter() - warm_started

        top_started = time.perf_counter()
        (
            topological,
            all_stable,
            catalog_rows,
            safe_pair_count,
            unsafe_pair_count,
        ) = reciprocal_reduced_topological_value(module, topology, profile)
        topological_seconds = time.perf_counter() - top_started

        full_started = time.perf_counter()
        full_gate = module.fixed_event_integral_gate(
            topology,
            tuple(int(value) for value in profile["relative_orders"]),
            int(profile["global_nodes"]),
            int(profile["global_residue_nodes"]),
            int(profile["relative_residue_nodes"]),
            float(profile["model_distance"]),
            int(config["topology"]["boundary_tracking_steps"]),
            str(profile["relative_quadrature_mode"]),
            float(profile["relative_adaptive_tolerance"]),
            int(profile["relative_adaptive_maximum_intervals"]),
        )
        full_seconds = time.perf_counter() - full_started
    finally:
        module.chamber_residue_catalog = previous_catalog
        module.global_chamber_value = previous_global_value

    stored_topological = complex(stored_gate["topological_correction"])
    reproduction_residual = abs(topological - stored_topological)
    return tagged(
        {
            "job_key": job_key,
            "topology_path": relative(topology_path),
            "kernel_path": relative(kernel_path),
            "warm_value": complex_row(warm_value),
            "warm_residues_stable": warm_stable,
            "warm_seconds": warm_seconds,
            "topological_only_value": complex_row(topological),
            "stored_topological_value": complex_row(stored_topological),
            "topological_reproduction_residual": reproduction_residual,
            "topological_reproduction_relative_residual": (
                reproduction_residual / max(1.0, abs(stored_topological))
            ),
            "topological_residues_stable": all_stable,
            "selected_catalog_rows": catalog_rows,
            "full_catalog_crossing_rows": sum(
                len(chamber["surface_crossings"])
                for chamber in topology["chambers"]
            ),
            "safe_reciprocal_pair_count": safe_pair_count,
            "unsafe_fail_closed_pair_count": unsafe_pair_count,
            "reciprocal_reduced_seconds": topological_seconds,
            "full_gate_seconds": full_seconds,
            "reciprocal_reduced_cost_fraction": topological_seconds
            / full_seconds,
            "full_gate_topological_residual": abs(
                complex(full_gate["topological_correction"]) - topological
            ),
            "full_gate_converged": full_gate[
                "fixed_event_crossed_integral_converged"
            ],
            "status": "RECIPROCAL_REDUCED_PRODUCTION_GATE_REPRODUCTION",
        }
    )


def design_projection(
    values: dict[str, np.ndarray], benchmark: dict[str, Any]
) -> dict[str, Any]:
    topological = values["topological"]
    naive = values["naive"]
    total = values["total"]
    topological_cost = float(benchmark["reciprocal_reduced_seconds"])
    full_cost = float(benchmark["full_gate_seconds"])
    channels: dict[str, Any] = {}
    for part in ("real", "imaginary"):
        top_array = topological.real if part == "real" else topological.imag
        naive_array = naive.real if part == "real" else naive.imag
        total_array = total.real if part == "real" else total.imag
        sigma_topological = float(np.std(top_array, ddof=1))
        sigma_naive = float(np.std(naive_array, ddof=1))
        sigma_total = float(np.std(total_array, ddof=1))
        optimal_ratio = (
            sigma_topological
            / max(sigma_naive, 1.0e-30)
            * math.sqrt(full_cost / topological_cost)
        )
        stratified_cost_variance = (
            full_cost + topological_cost * optimal_ratio
        ) * (
            sigma_naive**2 + sigma_topological**2 / optimal_ratio
        )
        paired_cost_variance = full_cost * sigma_total**2
        channels[part] = {
            "sigma_topological": sigma_topological,
            "sigma_naive": sigma_naive,
            "sigma_total": sigma_total,
            "topological_naive_correlation": float(
                np.corrcoef(top_array, naive_array)[0, 1]
            ),
            "optimal_topological_per_full_ratio": optimal_ratio,
            "stratified_to_paired_cost_variance": (
                stratified_cost_variance / paired_cost_variance
            ),
            "projected_speedup": paired_cost_variance
            / stratified_cost_variance,
        }
    return {
        "identity": "E[H]=E[H_topological]+E[H_naive]",
        "sampling_contract": "keep pole_model+smooth paired inside H_naive; oversample only H_topological on independent outer events",
        "derivation": "linearity of epsilon Richardson, cyclic crossing, and local projection",
        "reciprocal_reduced_cost_fraction": topological_cost / full_cost,
        "channels": channels,
        "design_conditioned": True,
        "independent_pilot_required": True,
        "valid_for_numeric_UV_claim": False,
    }


def reproduction_residual(cyclic_rows: list[dict[str, Any]]) -> float:
    reference = {
        (int(row["seed"]), round(float(row["physical_cosine"]), 12)): complex(
            float(row["crossed_only_real"]), float(row["crossed_only_imaginary"])
        )
        for row in read_csv(ROWS_5123)
        if row["row_type"] == "high_seed"
    }
    maximum = 0.0
    for row in cyclic_rows:
        if row["matrix_id"] != "production4_primary_E040":
            continue
        key = (int(row["seed"]), round(float(row["physical_cosine"]), 12))
        value = complex(float(row["total_real"]), float(row["total_imaginary"]))
        maximum = max(maximum, abs(value - reference[key]))
    return maximum


def validation_rows(
    required_paths: set[Path],
    maximum_closure: float,
    reproduction: float,
    correlations: dict[str, float],
    benchmark: dict[str, Any],
    reciprocal_summary: dict[str, Any],
    projection: dict[str, Any],
    plain_projection: dict[str, Any],
    precombination_already_present: bool,
    pure_gravity_scope_separated: bool,
) -> list[dict[str, Any]]:
    checks = [
        (
            "all_used_source_paths_exist",
            all(path.exists() for path in required_paths),
            str(len(required_paths)),
        ),
        (
            "component_closure_machine_precision",
            maximum_closure < 1.0e-8,
            str(maximum_closure),
        ),
        (
            "production4_reproduces_5123_crossed_rows",
            reproduction < 1.0e-10,
            str(reproduction),
        ),
        (
            "existing_runner_precombines_cyclic_targets_per_event",
            precombination_already_present,
            relative(SCRIPT_5034),
        ),
        (
            "pure_gravity_R3_not_substituted_for_four_scalar_Kmu",
            pure_gravity_scope_separated,
            f"{relative(SOURCE_GRAVITY)} versus {relative(CHECKPOINT_4987)}",
        ),
        (
            "pole_model_and_smooth_remain_paired_real",
            correlations["pole_smooth_real"] < -0.95,
            str(correlations["pole_smooth_real"]),
        ),
        (
            "pole_model_and_smooth_remain_paired_imaginary",
            correlations["pole_smooth_imaginary"] < -0.95,
            str(correlations["pole_smooth_imaginary"]),
        ),
        (
            "all_crossing_roots_have_reciprocal_partners",
            int(reciprocal_summary["correction_row_count"])
            == 2 * int(reciprocal_summary["reciprocal_pair_count"])
            and float(reciprocal_summary["maximum_reciprocal_root_residual"])
            < 2.0e-8,
            json.dumps(
                {
                    "rows": reciprocal_summary["correction_row_count"],
                    "pairs": reciprocal_summary["reciprocal_pair_count"],
                    "maximum_residual": reciprocal_summary[
                        "maximum_reciprocal_root_residual"
                    ],
                }
            ),
        ),
        (
            "safe_reciprocal_residue_antisymmetry_closes",
            int(reciprocal_summary["safe_pair_failures"]) == 0
            and float(
                reciprocal_summary[
                    "maximum_safe_residue_antisymmetry_residual"
                ]
            )
            < 2.0e-6,
            str(
                reciprocal_summary[
                    "maximum_safe_residue_antisymmetry_residual"
                ]
            ),
        ),
        (
            "ambiguous_reciprocal_families_remain_fail_closed",
            int(reciprocal_summary["unsafe_pair_count"]) > 0,
            str(reciprocal_summary["unsafe_pair_count"]),
        ),
        (
            "reciprocal_reconstruction_reproduces_topological_sum",
            float(
                reciprocal_summary[
                    "maximum_topological_reconstruction_relative_residual"
                ]
            )
            < 2.0e-6,
            str(
                reciprocal_summary[
                    "maximum_topological_reconstruction_relative_residual"
                ]
            ),
        ),
        (
            "reciprocal_reduced_gate_reproduces_stored_value",
            float(benchmark["topological_reproduction_relative_residual"])
            < 1.0e-10,
            json.dumps(
                {
                    "absolute": benchmark["topological_reproduction_residual"],
                    "relative": benchmark[
                        "topological_reproduction_relative_residual"
                    ],
                }
            ),
        ),
        (
            "reciprocal_reduced_gate_residues_stable",
            bool(benchmark["topological_residues_stable"]),
            str(benchmark["selected_catalog_rows"]),
        ),
        (
            "full_gate_replay_converged",
            bool(benchmark["full_gate_converged"]),
            str(benchmark["full_gate_topological_residual"]),
        ),
        (
            "reciprocal_reduction_uses_fewer_catalog_rows",
            int(benchmark["selected_catalog_rows"])
            < int(benchmark["full_catalog_crossing_rows"]),
            f"{benchmark['selected_catalog_rows']}/{benchmark['full_catalog_crossing_rows']}",
        ),
        (
            "plain_topological_split_is_recorded_as_rejected",
            float(plain_projection["reciprocal_reduced_cost_fraction"]) > 0.6
            and float(plain_projection["channels"]["real"]["projected_speedup"])
            < 1.0
            and float(
                plain_projection["channels"]["imaginary"]["projected_speedup"]
            )
            < 1.0,
            json.dumps(
                {
                    "cost_fraction": plain_projection[
                        "reciprocal_reduced_cost_fraction"
                    ],
                    "real_speedup": plain_projection["channels"]["real"][
                        "projected_speedup"
                    ],
                    "imaginary_speedup": plain_projection["channels"][
                        "imaginary"
                    ]["projected_speedup"],
                }
            ),
        ),
        (
            "reciprocal_reduced_stratum_is_cheaper_in_benchmark",
            float(benchmark["reciprocal_reduced_cost_fraction"]) < 0.6,
            str(benchmark["reciprocal_reduced_cost_fraction"]),
        ),
        (
            "stratification_projects_real_efficiency_gain",
            float(projection["channels"]["real"]["projected_speedup"]) > 1.0,
            str(projection["channels"]["real"]["projected_speedup"]),
        ),
        (
            "stratification_projects_imaginary_efficiency_gain",
            float(projection["channels"]["imaginary"]["projected_speedup"])
            > 1.0,
            str(projection["channels"]["imaginary"]["projected_speedup"]),
        ),
        (
            "design_remains_nonclaim",
            projection["independent_pilot_required"]
            and not projection["valid_for_numeric_UV_claim"],
            "independent fresh topological events required",
        ),
        (
            "formalization_workbench_unchanged",
            tree_digest(FORMAL) == FORMAL_BASELINE,
            tree_digest(FORMAL),
        ),
    ]
    return [
        tagged(
            {
                "check_id": check_id,
                "passed": passed,
                "detail": detail,
            }
        )
        for check_id, passed, detail in checks
    ]


def write_provenance(required_paths: set[Path], result: dict[str, Any]) -> None:
    selected = (
        SCRIPT_5034,
        SCRIPT_5077,
        SOURCE_GRAVITY,
        CHECKPOINT_4987,
        CHECKPOINT_5123,
        HIGH_RUN / "config.json",
        HIGH_RUN / "COMPLETED.json",
        CONTROL_RUN / "config.json",
        CONTROL_RUN / "COMPLETED.json",
        RESULT_5123,
        ROWS_5123,
        PLAIN_BENCHMARK_JSON,
    )
    lines = [
        "# 5124 provenance",
        "",
        "This checkpoint is a private numerical/analytic design result. It does not alter the parent equations and makes no UV, local-GR, galaxy, or full-MTS claim.",
        "",
        "## Locked sources",
        "",
    ]
    for path in selected:
        lines.append(f"- `{relative(path)}` — `{digest(path)}`")
    lines.extend(
        [
            "",
            "## Matrix coverage",
            "",
            f"- Exact source files consumed: `{len(required_paths)}`.",
            f"- Production matrix: `{len(PRODUCTION_SEEDS)}` outer events with primary E020/E040.",
            f"- Design matrix: `{len(DESIGN_SEEDS)}` outer events with primary E020 and converged coarse E040.",
            "- The 16-event matrix is used only to design the stratum allocation; it is not substituted for the locked production estimator.",
            "- No target hhh values, locality residuals, or desired UV coefficient enter the split.",
            "",
            "## Governing cog condition",
            "",
            "Any eventual coefficient must feed one parent theory that leaves the tested GR/Newton local regime intact while deriving, rather than manually switching on, any galactic-scale departure.",
            "",
            f"Result digest before provenance: `{hashlib.sha256(json.dumps(result, sort_keys=True).encode()).hexdigest()}`.",
        ]
    )
    PROVENANCE.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_document(result: dict[str, Any]) -> None:
    design = result["stratified_design"]
    real = design["channels"]["real"]
    imaginary = design["channels"]["imaginary"]
    correlations = result["correlations"]
    benchmark = result["benchmark"]
    reciprocal = result["reciprocal_audit"]
    plain = result["plain_stratified_design"]
    text = f"""# 5124 - crossed hhh two-stratum derivation

## Result

This checkpoint takes a forward step on the crossed `hhh` bottleneck. The
existing runner already forms the `s/t/u` cyclic sum at each outer event, so
wrapping the three completed target integrals in another sum cannot change
the random variable or its variance.

The fixed-event contour instead admits the exact split

```text
R = R_naive + R_topological,
R_naive = R_pole_model + R_smooth.
```

Richardson extrapolation, cyclic crossing and the local-shape projection are
all linear, hence the same split survives exactly in the final event-level
coefficient. The maximum numerical closure residual is
`{result['maximum_component_closure']:.3e}`.

## What cancels and what can be sampled separately

The analytic pole model and regularized smooth remainder have design-matrix
correlations `{correlations['pole_smooth_real']:.9f}` (real) and
`{correlations['pole_smooth_imaginary']:.9f}` (imaginary). They are large
opposite pieces and **must remain paired**. Separating them would manufacture
variance.

By contrast, `R_topological` and the already-paired `R_naive` have
correlations `{correlations['top_naive_real']:.6f}` and
`{correlations['top_naive_imaginary']:.6f}`. The topological term carries the
dominant event variance and is an exact independent stratum.

Across `{reciprocal['kernel_file_count']}` completed kernels, all
`{reciprocal['correction_row_count']}` crossings form
`{reciprocal['reciprocal_pair_count']}` reciprocal-root pairs. For the
`{reciprocal['safe_pair_count']}` isolated safe pairs, reflection of the
relative circle gives `Res(1/r)=-Res(r)`; the largest measured antisymmetry
residual is
`{reciprocal['maximum_safe_residue_antisymmetry_residual']:.3e}`. The
`{reciprocal['unsafe_pair_count']}` clustered or mixed `g2/decay` pairs remain
fail-closed and evaluate both residues.

The reciprocal-reduced production replay reproduces the stored topological
correction with relative residual
`{benchmark['topological_reproduction_relative_residual']:.3e}` and all
residues stable. It evaluates `{benchmark['selected_catalog_rows']}` instead
of `{benchmark['full_catalog_crossing_rows']}` crossing rows and costs
`{benchmark['reciprocal_reduced_cost_fraction']:.3f}` of the full fixed-event
gate in the recorded benchmark.

The simpler unreduced split was tested first and rejected: its measured cost
fraction was `{plain['reciprocal_reduced_cost_fraction']:.3f}`, producing
projected speedups `{plain['channels']['real']['projected_speedup']:.3f}`
(real) and `{plain['channels']['imaginary']['projected_speedup']:.3f}`
(imaginary), both below unity. The reciprocal theorem—not relabelling the old
estimator—is what makes the revised stratum useful.

## Conditional reciprocal proof

The relative azimuth is represented by `xi` through

```text
c(xi) = (xi + xi^-1)/2,
s(xi) = (xi - xi^-1)/(2 i).
```

Under `I: xi -> xi^-1`, `c` is fixed and `s` changes sign. This is reflection
through the external scattering plane. On an isolated ownership branch the
helicity-summed KLT-plus scalar kernel is reflection-even, so
`F(I xi)=F(xi)`. For the relative contour one-form

```text
omega = F(xi) dxi/xi,
I*omega = F(I xi) d(xi^-1)/(xi^-1) = -omega.
```

Residues of a one-form are invariant under coordinate pullback; therefore
`Res_(1/r)(omega)=-Res_r(omega)`. This proof is deliberately restricted to
one-to-one isolated reciprocal ownership families. Multi-root groups and the
mixed direct-`g2`/subtraction-`decay` family do not yet satisfy that mapping
contract and are the 797 pairs retained fail-closed.

## Derived allocation

For independent topological and full/naive event banks,

```text
Var = sigma_naive^2/N_naive + sigma_top^2/N_top,
Cost = c_full N_naive + c_top N_top,
N_top/N_naive = (sigma_top/sigma_naive) sqrt(c_full/c_top).
```

The 16-event design matrix gives optimal ratios
`{real['optimal_topological_per_full_ratio']:.3f}` (real) and
`{imaginary['optimal_topological_per_full_ratio']:.3f}` (imaginary), with
projected cost-normalized speedups `{real['projected_speedup']:.3f}` and
`{imaginary['projected_speedup']:.3f}`. These are design estimates, not an
independent efficiency result; a fresh pilot must confirm them before the UV
coefficient is reconsidered.

## Source-scope correction

The Bern gravity source supplies the exact pure-gravity four-graviton `R^3`
running. It does not supply the two-loop four-scalar `K_mu` coefficient and is
therefore not substituted for this calculation.

## Physics discipline

- No exterior event is deleted or downweighted after inspection.
- No hhh target, locality residual, or desired coefficient is fitted.
- No field equation or coupling is retuned.
- No numeric UV coefficient, local GR/Newton limit, galaxy law, or full MTS is claimed.
- The governing cog condition remains: one parent mechanism must preserve the successful local GR/Newton regime while deriving any large-scale activation without a manual switch.

## Next calculation

Build the restartable reciprocal-reduced topological outer-event runner from
the exact gate proved here, lock fresh seeds and an allocation before seeing
outcomes, then compare its realized cost-variance against the paired high
estimator. The `pole_model+smooth` contour must remain a single full-event
stratum, and unsafe reciprocal families must continue to evaluate both roots.
"""
    DOCUMENT.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--reuse-benchmark", action="store_true")
    arguments = parser.parse_args()

    required = {
        HIGH_RUN / "config.json",
        HIGH_RUN / "COMPLETED.json",
        CONTROL_RUN / "config.json",
        CONTROL_RUN / "COMPLETED.json",
        RESULT_5123,
        ROWS_5123,
        SCRIPT_5034,
        SCRIPT_5077,
        SOURCE_GRAVITY,
        CHECKPOINT_4987,
        CHECKPOINT_5123,
        PLAIN_BENCHMARK_JSON,
    }
    if not all(path.exists() for path in required):
        missing = [str(path) for path in required if not path.exists()]
        raise FileNotFoundError(missing)
    config = read_json(HIGH_RUN / "config.json")
    plain_benchmark = read_json(PLAIN_BENCHMARK_JSON)

    (
        production_cyclic,
        production_local,
        production_values,
        production_closure,
        production_paths,
    ) = matrix_rows(
        "production4_primary_E040",
        PRODUCTION_SEEDS,
        "primary24",
        config,
    )
    (
        design_cyclic,
        design_local,
        design_values,
        design_closure,
        design_paths,
    ) = matrix_rows(
        "design16_coarse_E040",
        DESIGN_SEEDS,
        "coarse12",
        config,
    )
    required.update(production_paths)
    required.update(design_paths)
    maximum_closure = max(production_closure, design_closure)
    reproduction = reproduction_residual(production_cyclic)

    correlations = {
        "pole_smooth_real": correlation(
            design_values["pole_model"], design_values["smooth"], "real"
        ),
        "pole_smooth_imaginary": correlation(
            design_values["pole_model"], design_values["smooth"], "imaginary"
        ),
        "top_naive_real": correlation(
            design_values["topological"], design_values["naive"], "real"
        ),
        "top_naive_imaginary": correlation(
            design_values["topological"], design_values["naive"], "imaginary"
        ),
    }

    reciprocal_rows, reciprocal_summary, reciprocal_paths = reciprocal_matrix_audit()
    required.update(reciprocal_paths)

    if arguments.reuse_benchmark:
        benchmark = read_json(BENCHMARK_JSON)
    else:
        benchmark = production_benchmark()
        write_json(BENCHMARK_JSON, benchmark)
    projection = design_projection(design_values, benchmark)
    plain_projection = design_projection(
        design_values,
        {
            "reciprocal_reduced_seconds": plain_benchmark[
                "topological_only_seconds"
            ],
            "full_gate_seconds": plain_benchmark["full_gate_seconds"],
        },
    )

    source_5034 = SCRIPT_5034.read_text(encoding="utf-8")
    precombination_already_present = all(
        fragment in source_5034
        for fragment in (
            "value_lookup[keys[0]]",
            "crossing[\"t_ratio\"] ** 3 * value_lookup[keys[1]]",
            "crossing[\"u_ratio\"] ** 3 * value_lookup[keys[2]]",
            "sample_values.append(value)",
        )
    )
    gravity_text = SOURCE_GRAVITY.read_text(encoding="utf-8")
    checkpoint_text = CHECKPOINT_4987.read_text(encoding="utf-8")
    pure_gravity_scope_separated = (
        "four-graviton scattering" in gravity_text
        and "c_{R^3}" in gravity_text
        and "four-scalar" in checkpoint_text
        and "K_mu" in checkpoint_text
    )

    cyclic_rows = [*production_cyclic, *design_cyclic]
    local_rows = [*production_local, *design_local]
    summaries = [
        *component_summary("production4_primary_E040", production_values),
        *component_summary("design16_coarse_E040", design_values),
    ]
    write_csv(CYCLIC_CSV, cyclic_rows)
    write_csv(LOCAL_CSV, local_rows)
    write_csv(SUMMARY_CSV, summaries)
    write_csv(RECIPROCAL_CSV, reciprocal_rows)

    validations = validation_rows(
        required,
        maximum_closure,
        reproduction,
        correlations,
        benchmark,
        reciprocal_summary,
        projection,
        plain_projection,
        precombination_already_present,
        pure_gravity_scope_separated,
    )
    write_csv(VALIDATION_CSV, validations)
    if not all(row["passed"] for row in validations):
        failures = [row for row in validations if not row["passed"]]
        raise RuntimeError(f"validation failed: {failures}")

    result = tagged(
        {
            "production_matrix": {
                "seeds": list(PRODUCTION_SEEDS),
                "e020_profile": "primary24",
                "e040_profile": "primary24",
                "purpose": "reproduce checkpoint-5123 crossed production rows",
            },
            "design_matrix": {
                "seeds": list(DESIGN_SEEDS),
                "e020_profile": "primary24",
                "e040_profile": "coarse12",
                "purpose": "variance/allocation design only",
            },
            "identity": {
                "fixed_event": "R=R_topological+R_pole_model+R_smooth",
                "paired_remainder": "R_naive=R_pole_model+R_smooth",
                "cyclic_precombination_already_present": precombination_already_present,
                "maximum_component_closure": maximum_closure,
                "checkpoint_5123_reproduction_residual": reproduction,
            },
            "correlations": correlations,
            "reciprocal_audit": reciprocal_summary,
            "reciprocal_proof": {
                "involution": "I(xi)=xi^-1",
                "coordinate_action": "c(I xi)=c(xi), s(I xi)=-s(xi)",
                "one_form": "omega=F(xi) dxi/xi",
                "pullback": "I*omega=-omega on an isolated reflection-even ownership branch",
                "residue_law": "Res_(1/r)(omega)=-Res_r(omega)",
                "excluded_scope": "multi-root groups and mixed direct:g2/subtraction:decay families evaluate both roots",
            },
            "benchmark": benchmark,
            "stratified_design": projection,
            "plain_stratified_design": plain_projection,
            "pure_gravity_R3_source_is_not_four_scalar_Kmu": pure_gravity_scope_separated,
            "governing_cog_condition": "preserve local GR/Newton while deriving any galactic activation from the same parent mechanism",
            "numeric_UV_coefficient_complete": False,
            "local_GR_Newton_complete": False,
            "full_MTS_complete": False,
        }
    )
    result["maximum_component_closure"] = maximum_closure
    write_json(RESULT_JSON, result)
    write_provenance(required, result)
    write_document(result)

    print(
        json.dumps(
            {
                "checkpoint": 5124,
                "validation": f"{sum(row['passed'] for row in validations)}/{len(validations)}",
                "maximum_component_closure": maximum_closure,
                "checkpoint_5123_reproduction_residual": reproduction,
                "reciprocal_reduced_cost_fraction": benchmark[
                    "reciprocal_reduced_cost_fraction"
                ],
                "real_projected_speedup": projection["channels"]["real"][
                    "projected_speedup"
                ],
                "imaginary_projected_speedup": projection["channels"][
                    "imaginary"
                ]["projected_speedup"],
                "numeric_UV_claim": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
