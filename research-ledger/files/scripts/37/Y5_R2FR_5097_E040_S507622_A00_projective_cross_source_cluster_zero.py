from __future__ import annotations

import cmath
import csv
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
from typing import Any


POST = Path(__file__).resolve().parents[1]
ROOT = POST.parent
FORMAL = ROOT / "formalization-workbench"
SCRIPT_5043 = (
    POST
    / "scripts"
    / "Y5_R2FR_5043_theorem_first_coarse_E040_multilevel_gate.py"
)
RUN = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5079"
    / "runs"
    / "bounded_central_anchor_pilot_v9"
)
SOURCE = POST / "source-intake" / "functional_rg" / "5097"
RESULT_JSON = SOURCE / "E040_S507622_A00_projective_cross_source_cluster_zero.json"
VALIDATION_CSV = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5097_VALIDATION.csv"
)
MARKER = "MTS_5097_E040_S507622_A00_PROJECTIVE_CROSS_SOURCE_CLUSTER_ZERO"
REVISION = "projective-additive-cross-source-cluster-cauchy-zero-v1"
FORMAL_BASELINE = "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
EVENT_ID = "S507622_N0000"
ARGUMENT_ID = "E040_A00"
JOB_KEY = "E040__S507622_N0000__A00__coarse12"
PROFILE = "coarse12"
DIRECT_SOURCE = "direct:g2"
SUBTRACTION_SOURCE = "subtraction:decay"
FACTOR_SUFFIXES = ("plus_u", "plus_v", "minus_u", "minus_v")
ROOT_MATCH_TOLERANCE = 2.0e-9
PROJECTIVE_RESIDUAL_TOLERANCE = 2.0e-12
MINIMUM_SAME_SOURCE_FACTOR_SEPARATION = 1.0e-6


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


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


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True), encoding="utf-8")
    os.replace(temporary, path)


def complex_row(value: complex) -> dict[str, float]:
    return {"real": float(value.real), "imaginary": float(value.imag)}


def complex_from_row(value: dict[str, float]) -> complex:
    return complex(float(value["real"]), float(value["imaginary"]))


def normalized_residual(first: complex, second: complex) -> float:
    return float(abs(first - second) / max(1.0, abs(first), abs(second)))


def laurent_value(polynomial: dict[int, complex], value: complex) -> complex:
    return complex(
        sum(coefficient * value**exponent for exponent, coefficient in polynomial.items())
    )


def momentum_value(
    momentum: tuple[dict[int, complex], ...], value: complex
) -> tuple[complex, ...]:
    return tuple(laurent_value(component, value) for component in momentum)


def source_and_suffix(label: str) -> tuple[str, str]:
    source, suffix = label.rsplit(":", 1)
    return source, suffix


def projective_cluster_certificate(
    row: dict[str, Any],
    ownership: dict[str, bool],
    gate: dict[str, Any],
) -> dict[str, Any]:
    root = complex(row["root"])
    roots = [complex_from_row(value) for value in gate["relative_roots"]]
    closest_root = min(roots, key=lambda value: abs(value - root))
    root_residual = normalized_residual(root, closest_root)
    pairs = [tuple(str(label) for label in pair) for pair in row["pairs"]]
    pair_guards: list[dict[str, Any]] = []
    labels: list[str] = []
    for pair in pairs:
        pair_labels = list(pair)
        labels.extend(pair_labels)
        parsed = [source_and_suffix(label) for label in pair_labels]
        sources = {source for source, _ in parsed}
        suffixes = {suffix for _, suffix in parsed}
        pair_guards.append(
            {
                "pair": pair_labels,
                "direct_g2_vs_subtraction_decay": sources
                == {DIRECT_SOURCE, SUBTRACTION_SOURCE},
                "matching_factor_suffix": len(suffixes) == 1,
                "exactly_one_owned_label": sum(bool(ownership[label]) for label in pair_labels)
                == 1,
            }
        )
    guards = {
        "parent_gate_passed": bool(gate["projective_cluster_zero_certificate_passed"]),
        "relative_root_matched": root_residual < ROOT_MATCH_TOLERANCE,
        "nonzero_relative_root": abs(root) > 1.0e-8,
        "pairs_present": bool(pairs),
        "all_pairs_cross_additive_sources": all(
            value["direct_g2_vs_subtraction_decay"] for value in pair_guards
        ),
        "all_pairs_match_factor_suffix": all(
            value["matching_factor_suffix"] for value in pair_guards
        ),
        "all_pairs_have_opposite_ownership": all(
            value["exactly_one_owned_label"] for value in pair_guards
        ),
        "labels_do_not_repeat": len(labels) == len(set(labels)),
    }
    return {
        "passed": all(guards.values()),
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "root": complex_row(root),
        "matched_certified_root": complex_row(closest_root),
        "root_relative_residual": root_residual,
        "pairs": [list(pair) for pair in pairs],
        "pair_guards": pair_guards,
        "guards": guards,
        "analytic_identity": (
            "At u*=-(1+gamma)/(gamma beta), boosted g2 obeys "
            "p_g2=-sqrt(1-x) p_decay projectively. Corresponding g2 and decay "
            "factor roots therefore cross only between the two additive summands "
            "I_direct and -I_subtraction. Each selected same-summand simple-pole "
            "residue is holomorphic in q through the isolated cross-source cluster; "
            "q0 is nonzero, so Res_q[(sum Res_z I)/q]=0."
        ),
        "valid_for_full_MTS_claim": False,
    }


def main() -> None:
    source_paths = [SCRIPT_5043, RUN / "config.json", FORMAL]
    missing = [str(path) for path in source_paths if not path.exists()]
    if missing:
        raise FileNotFoundError(missing)
    module_5043 = load_module("mts_5043_for_5097", SCRIPT_5043)
    config = json.loads((RUN / "config.json").read_text(encoding="utf-8"))
    event = next(row for row in config["events"] if row["event_id"] == EVENT_ID)
    argument = next(
        row for row in config["arguments"] if row["argument_id"] == ARGUMENT_ID
    )
    target = complex_from_row(argument["target_cosine"])
    module_5043.M5034.configure(event, target)
    numerical = module_5043.N5030
    job_path = RUN / "jobs" / f"{JOB_KEY}.json"
    if not job_path.exists():
        raise FileNotFoundError(job_path)
    failed_job = json.loads(job_path.read_text(encoding="utf-8"))
    kernel_path = Path(failed_job["kernel_file"])
    if not kernel_path.exists():
        raise FileNotFoundError(kernel_path)
    kernel = json.loads(kernel_path.read_text(encoding="utf-8"))
    integral_gate = kernel["fixed_event_integral_gate"]

    soft_energy = float(event["soft_energy"])
    soft_cosine = float(event["soft_cosine"])
    decay_cosine = float(event["decay_cosine"])
    recoil_root = math.sqrt(1.0 - soft_energy)
    gamma = (2.0 - soft_energy) / (2.0 * recoil_root)
    beta = soft_energy / (2.0 - soft_energy)
    gamma_beta = gamma * beta
    u_from_energy = -(1.0 + gamma) / gamma_beta
    u_from_spatial = -gamma_beta / (gamma - 1.0)
    transverse_product = math.sqrt(1.0 - soft_cosine**2) * math.sqrt(
        1.0 - decay_cosine**2
    )
    quadratic_a = 0.5 * transverse_product
    quadratic_b = soft_cosine * decay_cosine - u_from_energy
    discriminant = quadratic_b * quadratic_b - 4.0 * quadratic_a * quadratic_a
    relative_roots = sorted(
        (
            (-quadratic_b + cmath.sqrt(discriminant)) / (2.0 * quadratic_a),
            (-quadratic_b - cmath.sqrt(discriminant)) / (2.0 * quadratic_a),
        ),
        key=abs,
    )

    rationals = numerical.M5029.root_rationals(
        soft_energy, soft_cosine, decay_cosine, target
    )
    momenta = numerical.M5029.source_momenta(
        soft_energy, soft_cosine, decay_cosine
    )
    root_certificates: list[dict[str, Any]] = []
    for relative_root in relative_roots:
        direct_momentum = momentum_value(momenta[DIRECT_SOURCE], relative_root)
        subtraction_momentum = momentum_value(
            momenta[SUBTRACTION_SOURCE], relative_root
        )
        component_residuals = [
            normalized_residual(direct, -recoil_root * subtraction)
            for direct, subtraction in zip(direct_momentum, subtraction_momentum)
        ]
        factor_values: dict[str, dict[str, Any]] = {}
        direct_factors: list[complex] = []
        subtraction_factors: list[complex] = []
        for suffix in FACTOR_SUFFIXES:
            direct_label = f"{DIRECT_SOURCE}:{suffix}"
            subtraction_label = f"{SUBTRACTION_SOURCE}:{suffix}"
            direct_factor = numerical.M5029.rational_value(
                rationals[direct_label], relative_root
            )
            subtraction_factor = numerical.M5029.rational_value(
                rationals[subtraction_label], relative_root
            )
            direct_factors.append(direct_factor)
            subtraction_factors.append(subtraction_factor)
            factor_values[suffix] = {
                "direct": complex_row(direct_factor),
                "subtraction": complex_row(subtraction_factor),
                "relative_residual": normalized_residual(
                    direct_factor, subtraction_factor
                ),
            }
        direct_minimum_separation = min(
            abs(direct_factors[first] - direct_factors[second])
            for first in range(len(direct_factors))
            for second in range(first + 1, len(direct_factors))
        )
        subtraction_minimum_separation = min(
            abs(subtraction_factors[first] - subtraction_factors[second])
            for first in range(len(subtraction_factors))
            for second in range(first + 1, len(subtraction_factors))
        )
        relative_cosine = (
            soft_cosine * decay_cosine
            + 0.5
            * transverse_product
            * (relative_root + 1.0 / relative_root)
        )
        root_certificates.append(
            {
                "relative_root": complex_row(relative_root),
                "relative_cosine": complex_row(relative_cosine),
                "relative_cosine_residual": normalized_residual(
                    relative_cosine, complex(u_from_energy, 0.0)
                ),
                "direct_momentum": [complex_row(value) for value in direct_momentum],
                "subtraction_momentum": [
                    complex_row(value) for value in subtraction_momentum
                ],
                "projective_scale": -recoil_root,
                "projective_component_residuals": component_residuals,
                "maximum_projective_component_residual": max(component_residuals),
                "factor_values": factor_values,
                "maximum_factor_root_residual": max(
                    value["relative_residual"] for value in factor_values.values()
                ),
                "minimum_direct_same_source_factor_separation": float(
                    direct_minimum_separation
                ),
                "minimum_subtraction_same_source_factor_separation": float(
                    subtraction_minimum_separation
                ),
            }
        )

    formal_digest = tree_digest(FORMAL)
    preliminary_guards = {
        "lorentz_identity": abs(gamma * gamma - gamma_beta * gamma_beta - 1.0)
        < 2.0e-14,
        "two_u_forms_agree": abs(u_from_energy - u_from_spatial) < 2.0e-13,
        "boosted_energy_ratio_is_minus_one": abs(
            gamma * (1.0 + beta * u_from_energy) + 1.0
        )
        < 2.0e-13,
        "boosted_spatial_n_coefficient_vanishes": abs(
            (gamma - 1.0) * u_from_energy + gamma_beta
        )
        < 2.0e-13,
        "relative_roots_nonzero_and_reciprocal": min(map(abs, relative_roots)) > 1.0e-8
        and abs(relative_roots[0] * relative_roots[1] - 1.0) < 2.0e-13,
        "projective_momenta_close": all(
            row["maximum_projective_component_residual"]
            < PROJECTIVE_RESIDUAL_TOLERANCE
            for row in root_certificates
        ),
        "all_four_factor_roots_match": all(
            row["maximum_factor_root_residual"] < PROJECTIVE_RESIDUAL_TOLERANCE
            for row in root_certificates
        ),
        "same_source_factor_poles_remain_separate": all(
            min(
                row["minimum_direct_same_source_factor_separation"],
                row["minimum_subtraction_same_source_factor_separation"],
            )
            > MINIMUM_SAME_SOURCE_FACTOR_SEPARATION
            for row in root_certificates
        ),
        "adaptive_quadrature_already_converged": all(
            bool(row["adaptive_quadrature_converged"])
            for row in integral_gate["order_rows"]
        )
        and float(integral_gate["highest_two_order_relative_residual"])
        < float(integral_gate["relative_adaptive_tolerance"]),
        "failure_is_residue_only": not bool(integral_gate["all_residues_stable"]),
        "formalization_unchanged": formal_digest == FORMAL_BASELINE,
    }
    preliminary_passed = all(preliminary_guards.values())
    provisional_gate = {
        "projective_cluster_zero_certificate_passed": preliminary_passed,
        "relative_roots": [complex_row(value) for value in relative_roots],
    }
    boundaries, ownerships = numerical.physical_chambers()
    unstable_rows: list[dict[str, Any]] = []
    for chamber_index, chamber in enumerate(integral_gate["chambers"]):
        for residue in chamber["residue_catalog"]:
            if bool(residue["stable"]):
                continue
            certificate = projective_cluster_certificate(
                residue, ownerships[chamber_index], provisional_gate
            )
            unstable_rows.append(
                {
                    "chamber_index": chamber_index,
                    "original_numeric_probe": {
                        "root": residue["root"],
                        "pairs": residue["pairs"],
                        "outer_residue": residue["outer_residue"],
                        "inner_residue": residue["inner_residue"],
                        "residue_stability": residue["residue_stability"],
                        "selected_fraction": residue["residue_contour_fraction"],
                    },
                    "certificate": certificate,
                }
            )
    unstable_rows_complete = len(unstable_rows) == 2 and all(
        row["certificate"]["passed"] for row in unstable_rows
    )
    guards = {**preliminary_guards, "all_unstable_rows_certified": unstable_rows_complete}
    certificate_passed = all(guards.values())
    result = {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "event_id": EVENT_ID,
        "argument_id": ARGUMENT_ID,
        "job_key": JOB_KEY,
        "profile": PROFILE,
        "source_config": str(RUN / "config.json"),
        "source_config_sha256": digest(RUN / "config.json"),
        "source_failed_job": str(job_path),
        "source_failed_job_sha256_before_repair": digest(job_path),
        "source_kernel": str(kernel_path),
        "source_kernel_sha256_before_repair": digest(kernel_path),
        "source_theorem_module": str(SCRIPT_5043),
        "source_theorem_module_sha256": digest(SCRIPT_5043),
        "soft_energy": soft_energy,
        "recoil_root": recoil_root,
        "gamma": gamma,
        "beta": beta,
        "gamma_beta": gamma_beta,
        "projective_relative_cosine": u_from_energy,
        "projective_relative_cosine_second_form": u_from_spatial,
        "relative_roots": [complex_row(value) for value in relative_roots],
        "root_certificates": root_certificates,
        "unstable_residue_rows": unstable_rows,
        "theorem": (
            "The simultaneous direct:g2/subtraction:decay factor collisions are "
            "crossings between additive summands. At each certified q root, "
            "p_g2=-sqrt(1-x) p_decay and the four same-source factor poles remain "
            "simple and mutually separated. Their local z residues are therefore "
            "holomorphic functions of q. Because q0 is nonzero, the enclosing "
            "relative Cauchy residue vanishes exactly."
        ),
        "guards": guards,
        "projective_cluster_zero_certificate_passed": certificate_passed,
        "runner_integration_authorized": certificate_passed,
        "formalization_workbench_tree_sha256": formal_digest,
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(RESULT_JSON, result)
    checks = [
        ("source_paths_exist", not missing, "all 5097 sources exist"),
        ("lorentz_identity", guards["lorentz_identity"], str(gamma)),
        ("projective_u_identity", guards["two_u_forms_agree"], str(u_from_energy)),
        (
            "boosted_momentum_identity",
            guards["boosted_energy_ratio_is_minus_one"]
            and guards["boosted_spatial_n_coefficient_vanishes"],
            "E_g2/recoil_root=-1 and the soft-direction coefficient vanishes",
        ),
        (
            "relative_root_pair",
            guards["relative_roots_nonzero_and_reciprocal"],
            str([complex_row(value) for value in relative_roots]),
        ),
        (
            "projective_momenta",
            guards["projective_momenta_close"],
            str(
                [
                    row["maximum_projective_component_residual"]
                    for row in root_certificates
                ]
            ),
        ),
        (
            "factor_roots_match",
            guards["all_four_factor_roots_match"],
            str([row["maximum_factor_root_residual"] for row in root_certificates]),
        ),
        (
            "same_source_poles_separate",
            guards["same_source_factor_poles_remain_separate"],
            "same-source global poles remain simple and separated",
        ),
        (
            "quadrature_was_already_converged",
            guards["adaptive_quadrature_already_converged"],
            str(integral_gate["highest_two_order_relative_residual"]),
        ),
        (
            "all_unstable_rows_certified",
            guards["all_unstable_rows_certified"],
            str(len(unstable_rows)),
        ),
        ("certificate_passed", certificate_passed, str(certificate_passed)),
        ("formalization_unchanged", formal_digest == FORMAL_BASELINE, formal_digest),
        (
            "claim_discipline",
            not result["valid_for_full_MTS_claim"],
            "local numerical/theorem repair is not a full MTS claim",
        ),
    ]
    VALIDATION_CSV.parent.mkdir(parents=True, exist_ok=True)
    with VALIDATION_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=("check_id", "passed", "detail", "checkpoint_marker"),
        )
        writer.writeheader()
        for index, (name, passed, detail) in enumerate(checks, start=1):
            writer.writerow(
                {
                    "check_id": f"V5097_{index:02d}_{name}",
                    "passed": passed,
                    "detail": detail,
                    "checkpoint_marker": MARKER,
                }
            )
    failed = [name for name, passed, _ in checks if not passed]
    if failed:
        raise RuntimeError(f"checkpoint 5097 validation failed: {failed}")


if __name__ == "__main__":
    main()
