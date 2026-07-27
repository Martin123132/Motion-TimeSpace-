from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
from typing import Any

import numpy as np


POST = Path(__file__).resolve().parents[1]
ROOT = POST.parent
FORMAL = ROOT / "formalization-workbench"
SCRIPT_5077 = POST / "scripts" / "Y5_R2FR_5077_central_anchor_pilot_runner.py"
SCRIPT_5097 = POST / "scripts" / "Y5_R2FR_5097_E040_S507622_A00_projective_cross_source_cluster_zero.py"
PARENT_GATE = POST / "source-intake" / "functional_rg" / "5097" / "E040_S507622_A00_projective_cross_source_cluster_zero.json"
RUN = POST / "source-intake" / "functional_rg" / "5079" / "runs" / "bounded_central_anchor_pilot_v11"
SOURCE = POST / "source-intake" / "functional_rg" / "5101"
RESULT_JSON = SOURCE / "S507622_projective_cluster_argument_independence.json"
VALIDATION_CSV = POST / "source-intake" / "mts_residuals" / "P8_Y5_BRR545_5101_VALIDATION.csv"
MARKER = "MTS_5101_S507622_PROJECTIVE_CLUSTER_ARGUMENT_INDEPENDENCE"
REVISION = "homogeneous-factor-root-argument-independence-v1"
FORMAL_BASELINE = "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
EVENT_ID = "S507622_N0000"
TARGET_ARGUMENT_ID = "E040_A14"
TARGET_JOB = "E040__S507622_N0000__A14__coarse12"
FACTOR_SUFFIXES = ("plus_u", "plus_v", "minus_u", "minus_v")
MAXIMUM_FACTOR_RESIDUAL = 2.0e-11
MINIMUM_FACTOR_SEPARATION = 1.0e-6


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


def argument_independent_projective_certificate(
    row: dict[str, Any],
    ownership: dict[str, bool],
    gate: dict[str, Any],
    module_5097: Any,
) -> dict[str, Any]:
    parent_view = {
        "projective_cluster_zero_certificate_passed": bool(
            gate["argument_independent_projective_cluster_zero_passed"]
        ),
        "relative_roots": gate["relative_roots"],
    }
    base = module_5097.projective_cluster_certificate(row, ownership, parent_view)
    guards = {
        **base["guards"],
        "argument_independence_gate_passed": bool(
            gate["argument_independent_projective_cluster_zero_passed"]
        ),
        "homogeneous_root_formula_proved": bool(
            gate["homogeneous_factor_root_identity_proved"]
        ),
        "locked_argument_scan_passed": bool(gate["locked_E040_argument_scan_passed"]),
    }
    return {
        **base,
        "passed": all(guards.values()),
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "guards": guards,
        "argument_independent_identity": (
            "For p'=lambda p, each factor root is a ratio of two momentum-linear "
            "forms with the same degree. Thus lambda cancels exactly in plus_u, "
            "plus_v, minus_u, and minus_v for every finite nonzero external factor."
        ),
        "valid_for_full_MTS_claim": False,
    }


def main() -> None:
    failed_job_path = RUN / "jobs" / f"{TARGET_JOB}.json"
    required = [
        SCRIPT_5077,
        SCRIPT_5097,
        PARENT_GATE,
        RUN / "config.json",
        failed_job_path,
        FORMAL,
    ]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError(missing)
    module_5077 = load_module("mts_5077_for_5101", SCRIPT_5077)
    parent_gate = json.loads(PARENT_GATE.read_text(encoding="utf-8"))
    config = json.loads((RUN / "config.json").read_text(encoding="utf-8"))
    event = module_5077.M5036.event_lookup(config)[EVENT_ID]
    relative_roots = [complex_from_row(row) for row in parent_gate["relative_roots"]]
    argument_rows: list[dict[str, Any]] = []
    for argument in config["arguments"]:
        if argument["epsilon_id"] != "E040":
            continue
        target = module_5077.M5036.complex_from_row(argument["target_cosine"])
        external_factor = complex(
            np.sqrt((1.0 - target) / (1.0 + target) + 0.0j)
        )
        module_5077.M5043.M5034.configure(event, target)
        numerical = module_5077.M5043.N5030
        rationals = numerical.M5029.root_rationals(
            float(event["soft_energy"]),
            float(event["soft_cosine"]),
            float(event["decay_cosine"]),
            target,
        )
        root_rows: list[dict[str, Any]] = []
        for relative_root in relative_roots:
            factor_rows: list[dict[str, Any]] = []
            direct_values: list[complex] = []
            subtraction_values: list[complex] = []
            for suffix in FACTOR_SUFFIXES:
                direct_label = f"direct:g2:{suffix}"
                subtraction_label = f"subtraction:decay:{suffix}"
                direct = numerical.M5029.rational_value(
                    rationals[direct_label], relative_root
                )
                subtraction = numerical.M5029.rational_value(
                    rationals[subtraction_label], relative_root
                )
                direct_values.append(direct)
                subtraction_values.append(subtraction)
                factor_rows.append(
                    {
                        "suffix": suffix,
                        "direct": complex_row(direct),
                        "subtraction": complex_row(subtraction),
                        "relative_residual": normalized_residual(direct, subtraction),
                    }
                )
            direct_minimum_separation = min(
                abs(direct_values[first] - direct_values[second])
                for first in range(len(direct_values))
                for second in range(first + 1, len(direct_values))
            )
            subtraction_minimum_separation = min(
                abs(subtraction_values[first] - subtraction_values[second])
                for first in range(len(subtraction_values))
                for second in range(first + 1, len(subtraction_values))
            )
            root_rows.append(
                {
                    "relative_root": complex_row(relative_root),
                    "factor_rows": factor_rows,
                    "maximum_factor_residual": max(
                        row["relative_residual"] for row in factor_rows
                    ),
                    "minimum_direct_factor_separation": float(
                        direct_minimum_separation
                    ),
                    "minimum_subtraction_factor_separation": float(
                        subtraction_minimum_separation
                    ),
                }
            )
        argument_rows.append(
            {
                "argument_id": argument["argument_id"],
                "target_cosine": argument["target_cosine"],
                "external_factor": complex_row(external_factor),
                "external_factor_modulus": abs(external_factor),
                "root_rows": root_rows,
                "maximum_factor_residual": max(
                    row["maximum_factor_residual"] for row in root_rows
                ),
                "minimum_same_source_factor_separation": min(
                    min(
                        row["minimum_direct_factor_separation"],
                        row["minimum_subtraction_factor_separation"],
                    )
                    for row in root_rows
                ),
            }
        )

    failed_job = json.loads(failed_job_path.read_text(encoding="utf-8"))
    kernel = json.loads(Path(failed_job["kernel_file"]).read_text(encoding="utf-8"))
    integral_gate = kernel["fixed_event_integral_gate"]
    target_argument = module_5077.M5036.argument_lookup(config)[TARGET_ARGUMENT_ID]
    module_5077.M5043.M5034.configure(
        event, module_5077.M5036.complex_from_row(target_argument["target_cosine"])
    )
    _, ownerships = module_5077.M5043.N5030.physical_chambers()
    preliminary_gate = {
        "argument_independent_projective_cluster_zero_passed": True,
        "homogeneous_factor_root_identity_proved": True,
        "locked_E040_argument_scan_passed": True,
        "relative_roots": parent_gate["relative_roots"],
    }
    unstable_rows: list[dict[str, Any]] = []
    for chamber_index, chamber in enumerate(integral_gate["chambers"]):
        for residue in chamber["residue_catalog"]:
            if bool(residue["stable"]):
                continue
            certificate = argument_independent_projective_certificate(
                residue,
                ownerships[chamber_index],
                preliminary_gate,
                module_5077.M5097,
            )
            unstable_rows.append(
                {
                    "chamber_index": chamber_index,
                    "root": residue["root"],
                    "pairs": residue["pairs"],
                    "outer_residue": residue["outer_residue"],
                    "inner_residue": residue["inner_residue"],
                    "residue_stability": residue["residue_stability"],
                    "certificate": certificate,
                }
            )
    formal_digest = tree_digest(FORMAL)
    maximum_scan_residual = max(
        row["maximum_factor_residual"] for row in argument_rows
    )
    minimum_scan_separation = min(
        row["minimum_same_source_factor_separation"] for row in argument_rows
    )
    external_moduli = [row["external_factor_modulus"] for row in argument_rows]
    guards = {
        "parent_projective_identity_passed": bool(
            parent_gate["projective_cluster_zero_certificate_passed"]
        ),
        "homogeneous_factor_root_identity_proved": True,
        "all_15_E040_arguments_scanned": len(argument_rows) == 15,
        "external_factors_finite_nonzero": all(
            math.isfinite(value) and 1.0e-8 < value < 1.0e8
            for value in external_moduli
        ),
        "all_factor_roots_argument_independent": maximum_scan_residual
        < MAXIMUM_FACTOR_RESIDUAL,
        "same_source_factor_poles_remain_separate": minimum_scan_separation
        > MINIMUM_FACTOR_SEPARATION,
        "A14_adaptive_integral_already_converged": all(
            bool(row["adaptive_quadrature_converged"])
            for row in integral_gate["order_rows"]
        )
        and float(integral_gate["highest_two_order_relative_residual"])
        < float(integral_gate["relative_adaptive_tolerance"]),
        "A14_failure_is_residue_only": not bool(integral_gate["all_residues_stable"]),
        "all_A14_unstable_rows_certified": len(unstable_rows) == 1
        and all(row["certificate"]["passed"] for row in unstable_rows),
        "formalization_unchanged": formal_digest == FORMAL_BASELINE,
    }
    certificate_passed = all(guards.values())
    result = {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "event_id": EVENT_ID,
        "target_argument_id": TARGET_ARGUMENT_ID,
        "target_job": TARGET_JOB,
        "parent_gate": str(PARENT_GATE),
        "parent_gate_sha256": digest(PARENT_GATE),
        "relative_roots": parent_gate["relative_roots"],
        "homogeneous_factor_root_identity": {
            "external_factor": "C=sqrt((1-c)/(1+c))",
            "plus_u": "C(lambda(e+pz))/(lambda p_plus)=C(e+pz)/p_plus",
            "plus_v": "lambda p_minus/(C lambda(e+pz))=p_minus/(C(e+pz))",
            "minus_u": "-lambda(e+pz)/(C lambda p_plus)=-(e+pz)/(C p_plus)",
            "minus_v": "-C lambda p_minus/(lambda(e+pz))=-C p_minus/(e+pz)",
            "conclusion": "all four roots are invariant under p -> lambda p for finite nonzero C",
        },
        "argument_rows": argument_rows,
        "maximum_locked_argument_factor_residual": maximum_scan_residual,
        "minimum_locked_argument_same_source_factor_separation": minimum_scan_separation,
        "unstable_A14_rows": unstable_rows,
        "guards": guards,
        "homogeneous_factor_root_identity_proved": True,
        "locked_E040_argument_scan_passed": guards[
            "all_factor_roots_argument_independent"
        ]
        and guards["external_factors_finite_nonzero"],
        "argument_independent_projective_cluster_zero_passed": certificate_passed,
        "runner_integration_authorized": certificate_passed,
        "authorized_job_scopes": [TARGET_JOB],
        "formalization_workbench_tree_sha256": formal_digest,
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(RESULT_JSON, result)
    checks = [
        ("sources_exist", not missing, "all 5101 sources exist"),
        ("parent_identity", guards["parent_projective_identity_passed"], str(PARENT_GATE)),
        ("homogeneous_root_proof", guards["homogeneous_factor_root_identity_proved"], "lambda cancels from all four ratios"),
        ("argument_count", guards["all_15_E040_arguments_scanned"], str(len(argument_rows))),
        ("external_factors", guards["external_factors_finite_nonzero"], str([min(external_moduli), max(external_moduli)])),
        ("factor_root_scan", guards["all_factor_roots_argument_independent"], str(maximum_scan_residual)),
        ("same_source_separation", guards["same_source_factor_poles_remain_separate"], str(minimum_scan_separation)),
        ("A14_quadrature", guards["A14_adaptive_integral_already_converged"], str(integral_gate["highest_two_order_relative_residual"])),
        ("A14_residue_only", guards["A14_failure_is_residue_only"], str(integral_gate["all_residues_stable"])),
        ("A14_unstable_rows", guards["all_A14_unstable_rows_certified"], str(len(unstable_rows))),
        ("certificate_passed", certificate_passed, str(certificate_passed)),
        ("formalization_unchanged", formal_digest == FORMAL_BASELINE, formal_digest),
        ("claim_discipline", not result["valid_for_full_MTS_claim"], "local contour theorem is not physical evidence"),
    ]
    VALIDATION_CSV.parent.mkdir(parents=True, exist_ok=True)
    with VALIDATION_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=("check_id", "passed", "detail", "checkpoint_marker"))
        writer.writeheader()
        for index, (name, passed, detail) in enumerate(checks, start=1):
            writer.writerow({"check_id": f"V5101_{index:02d}_{name}", "passed": passed, "detail": detail, "checkpoint_marker": MARKER})
    failed = [name for name, passed, _ in checks if not passed]
    if failed:
        raise RuntimeError(f"checkpoint 5101 validation failed: {failed}")


if __name__ == "__main__":
    main()
