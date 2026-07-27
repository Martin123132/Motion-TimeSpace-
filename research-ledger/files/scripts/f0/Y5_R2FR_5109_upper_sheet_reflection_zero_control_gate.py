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

import numpy as np


POST = Path(__file__).resolve().parents[1]
ROOT = POST.parent
FORMAL = ROOT / "formalization-workbench"
SCRIPT_5028 = (
    POST
    / "scripts"
    / "Y5_R2FR_5028_finite_x_relative_chamber_transport_event.py"
)
SCRIPT_5043 = (
    POST
    / "scripts"
    / "Y5_R2FR_5043_theorem_first_coarse_E040_multilevel_gate.py"
)
CONFIG = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5079"
    / "runs"
    / "bounded_central_anchor_pilot_v12"
    / "config.json"
)
PILOT_STATUS = CONFIG.parent / "status.json"
REFLECTION_5037 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5037"
    / "reflection_control.csv"
)
FAILURE_5108 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5108"
    / "locked_pilot_failure_mechanism.json"
)
SOURCE = POST / "source-intake" / "functional_rg" / "5109"
RESULT_JSON = SOURCE / "upper_sheet_reflection_zero_control_gate.json"
VALIDATION_CSV = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5109_VALIDATION.csv"
)
MARKER = "MTS_5109_UPPER_SHEET_REFLECTION_ZERO_CONTROL_GATE"
REVISION = "target-anchor-permutation-obstruction-v1"
FORMAL_BASELINE = (
    "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
)
REFERENCE = complex(0.3, 0.0)
EPSILON = 0.04
RELATIVE_PHASES = (0.071, 0.271, 0.571, 0.871)
GLOBAL_PHASES = (0.113, 0.413, 0.713)
TARGET_PERMUTATION = {
    "plus_u": "plus_v",
    "plus_v": "plus_u",
    "minus_u": "minus_v",
    "minus_v": "minus_u",
}
ANCHOR_PERMUTATION = {
    "plus_u": "minus_v",
    "plus_v": "minus_u",
    "minus_u": "plus_v",
    "minus_v": "plus_u",
}


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5028 = load_module("mts_5028_for_5109", SCRIPT_5028)
M5043 = load_module("mts_5043_for_5109", SCRIPT_5043)


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


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True), encoding="utf-8")
    os.replace(temporary, path)


def normalized_residual(first: complex, second: complex) -> float:
    return abs(first - second) / max(1.0, abs(first), abs(second))


def transformed_vector(vector: np.ndarray) -> np.ndarray:
    return np.asarray(
        [
            np.conjugate(vector[0]),
            -np.conjugate(vector[1]),
            -np.conjugate(vector[2]),
        ],
        dtype=np.complex128,
    )


def transformed_internal(internal: np.ndarray) -> np.ndarray:
    result = np.conjugate(internal)
    result[:, 2:] *= -1.0
    return result


def ownership_at(
    directions: dict[str, np.ndarray], anchor: complex
) -> dict[str, bool]:
    ownership: dict[str, bool] = {}
    for source, direction in directions.items():
        roots = M5028.M5024.all_factor_roots(direction, anchor)
        for label in M5028.ROOT_LABELS:
            ownership[f"{source}:{label}"] = abs(roots[label]) < 1.0
    return ownership


def permuted_ownership(
    ownership: dict[str, bool],
    sources: tuple[str, ...],
    permutation: dict[str, str],
) -> dict[str, bool]:
    return {
        f"{source}:{label}": ownership[
            f"{source}:{permutation[label]}"
        ]
        for source in sources
        for label in M5028.ROOT_LABELS
    }


def complex_strings(values: np.ndarray) -> list[str]:
    return [str(complex(value)) for value in values]


def main() -> None:
    required = [
        SCRIPT_5028,
        SCRIPT_5043,
        CONFIG,
        PILOT_STATUS,
        REFLECTION_5037,
        FAILURE_5108,
        FORMAL,
    ]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError(missing)
    config = read_json(CONFIG)
    status = read_json(PILOT_STATUS)
    failure = read_json(FAILURE_5108)
    with REFLECTION_5037.open(newline="", encoding="utf-8") as handle:
        reflection_rows = list(csv.DictReader(handle))

    maximum_direction_residual = 0.0
    maximum_internal_residual = 0.0
    maximum_integrand_residual = 0.0
    maximum_target_root_residual = 0.0
    same_anchor_mismatches = 0
    reflected_anchor_mismatches = 0
    current_sheet_target_mismatches = 0
    ownership_comparisons = 0
    integrand_comparisons = 0
    root_comparisons = 0

    for event in config["events"]:
        soft_energy = float(event["soft_energy"])
        soft_cosine = complex(float(event["soft_cosine"]), 0.0)
        decay_cosine = complex(float(event["decay_cosine"]), 0.0)
        for phase in RELATIVE_PHASES:
            relative = cmath.exp(2.0j * math.pi * phase)
            transformed_relative = np.conjugate(relative)
            soft, decay, internal = M5028.event_geometry(
                soft_energy, soft_cosine, decay_cosine, relative
            )
            transformed_soft, transformed_decay, transformed_momenta = (
                M5028.event_geometry(
                    soft_energy,
                    -soft_cosine,
                    -decay_cosine,
                    transformed_relative,
                )
            )
            maximum_direction_residual = max(
                maximum_direction_residual,
                float(
                    np.max(
                        np.abs(transformed_soft - transformed_vector(soft))
                    )
                ),
                float(
                    np.max(
                        np.abs(transformed_decay - transformed_vector(decay))
                    )
                ),
            )
            maximum_internal_residual = max(
                maximum_internal_residual,
                float(
                    np.max(
                        np.abs(
                            transformed_momenta
                            - transformed_internal(internal)
                        )
                    )
                ),
            )
            directions = M5028.source_directions(internal, soft, decay)
            transformed_directions = M5028.source_directions(
                transformed_momenta, transformed_soft, transformed_decay
            )
            sources = tuple(directions)
            physical_ownership = ownership_at(directions, REFERENCE)
            transformed_physical_ownership = ownership_at(
                transformed_directions, REFERENCE
            )
            transformed_reflected_anchor_ownership = ownership_at(
                transformed_directions, -REFERENCE
            )
            image_ownership = permuted_ownership(
                physical_ownership, sources, TARGET_PERMUTATION
            )
            same_anchor_image = permuted_ownership(
                physical_ownership, sources, ANCHOR_PERMUTATION
            )
            for key in transformed_physical_ownership:
                ownership_comparisons += 1
                if transformed_physical_ownership[key] != same_anchor_image[key]:
                    same_anchor_mismatches += 1
                if (
                    transformed_reflected_anchor_ownership[key]
                    != image_ownership[key]
                ):
                    reflected_anchor_mismatches += 1
                if transformed_physical_ownership[key] != image_ownership[key]:
                    current_sheet_target_mismatches += 1

            for base_argument in config["base_arguments"]:
                target = complex(float(base_argument["argument"]), EPSILON)
                transformed_target = -np.conjugate(target)
                for source in sources:
                    roots = M5028.M5024.all_factor_roots(
                        directions[source], target
                    )
                    transformed_roots = M5028.M5024.all_factor_roots(
                        transformed_directions[source], transformed_target
                    )
                    for label in M5028.ROOT_LABELS:
                        root_comparisons += 1
                        maximum_target_root_residual = max(
                            maximum_target_root_residual,
                            normalized_residual(
                                transformed_roots[label],
                                np.conjugate(
                                    roots[TARGET_PERMUTATION[label]]
                                ),
                            ),
                        )
                for global_phase in GLOBAL_PHASES:
                    global_circle = cmath.exp(
                        2.0j * math.pi * global_phase
                    )
                    original_value = M5028.M5026.finite_plus_integrand(
                        internal,
                        soft_energy,
                        soft,
                        decay,
                        target,
                        global_circle,
                    )
                    transformed_value = M5028.M5026.finite_plus_integrand(
                        transformed_momenta,
                        soft_energy,
                        transformed_soft,
                        transformed_decay,
                        transformed_target,
                        np.conjugate(global_circle),
                    )
                    integrand_comparisons += 1
                    maximum_integrand_residual = max(
                        maximum_integrand_residual,
                        normalized_residual(
                            transformed_value, np.conjugate(original_value)
                        ),
                    )

    probe_event = config["events"][0]
    probe_relative = cmath.exp(2.0j * math.pi * 0.271 / 8.0)
    probe_soft_energy = float(probe_event["soft_energy"])
    probe_soft_cosine = complex(float(probe_event["soft_cosine"]), 0.0)
    probe_decay_cosine = complex(float(probe_event["decay_cosine"]), 0.0)
    probe_soft, probe_decay, probe_internal = M5028.event_geometry(
        probe_soft_energy,
        probe_soft_cosine,
        probe_decay_cosine,
        probe_relative,
    )
    transformed_probe_soft, transformed_probe_decay, transformed_probe_internal = (
        M5028.event_geometry(
            probe_soft_energy,
            -probe_soft_cosine,
            -probe_decay_cosine,
            np.conjugate(probe_relative),
        )
    )
    probe_sources = tuple(
        M5028.source_directions(
            probe_internal, probe_soft, probe_decay
        )
    )
    probe_ownership = M5028.chamber_ownership(
        probe_soft_energy,
        probe_soft_cosine,
        probe_decay_cosine,
        probe_relative,
    )
    transformed_probe_ownership = M5028.chamber_ownership(
        probe_soft_energy,
        -probe_soft_cosine,
        -probe_decay_cosine,
        np.conjugate(probe_relative),
    )
    probe_image_ownership = permuted_ownership(
        probe_ownership, probe_sources, TARGET_PERMUTATION
    )
    original_arguments: dict[tuple[str, str], complex] = {}
    image_arguments: dict[tuple[str, str], complex] = {}
    physical_arguments: dict[tuple[str, str], complex] = {}
    base_arguments = list(config["base_arguments"])
    for base_argument in base_arguments:
        argument = float(base_argument["argument"])
        argument_id = str(base_argument["argument_id"])
        reflected_argument = min(
            base_arguments,
            key=lambda row: abs(float(row["argument"]) + argument),
        )
        if abs(float(reflected_argument["argument"]) + argument) > 1.0e-12:
            raise RuntimeError(f"locked argument set lacks reflection of {argument}")
        reflected_argument_id = str(reflected_argument["argument_id"])
        target = complex(argument, EPSILON)
        transformed_target = -np.conjugate(target)
        original_arguments[(argument_id, "value")] = (
            M5028.fixed_ownership_global_cycle(
                probe_soft_energy,
                probe_soft,
                probe_decay,
                probe_internal,
                target,
                probe_ownership,
                128,
                96,
            )[0]
        )
        image_arguments[(reflected_argument_id, "value")] = (
            M5028.fixed_ownership_global_cycle(
                probe_soft_energy,
                transformed_probe_soft,
                transformed_probe_decay,
                transformed_probe_internal,
                transformed_target,
                probe_image_ownership,
                128,
                96,
            )[0]
        )
        physical_arguments[(reflected_argument_id, "value")] = (
            M5028.fixed_ownership_global_cycle(
                probe_soft_energy,
                transformed_probe_soft,
                transformed_probe_decay,
                transformed_probe_internal,
                transformed_target,
                transformed_probe_ownership,
                128,
                96,
            )[0]
        )
    original_cyclic = M5043.cyclic_nonlocal(config, original_arguments)
    image_cyclic = M5043.cyclic_nonlocal(config, image_arguments)
    physical_cyclic = M5043.cyclic_nonlocal(config, physical_arguments)
    expected_cyclic = np.conjugate(original_cyclic[::-1])
    cyclic_scale = max(
        1.0,
        float(np.max(np.abs(original_cyclic))),
        float(np.max(np.abs(image_cyclic))),
        float(np.max(np.abs(physical_cyclic))),
    )
    image_cyclic_residual = float(
        np.max(np.abs(image_cyclic - expected_cyclic)) / cyclic_scale
    )
    physical_cyclic_residual = float(
        np.max(np.abs(physical_cyclic - expected_cyclic)) / cyclic_scale
    )
    physical_image_difference = float(
        np.max(np.abs(physical_cyclic - image_cyclic)) / cyclic_scale
    )

    formal_digest = tree_digest(FORMAL)
    prior_reflection_was_diagnostic_only = all(
        str(row["symmetry_imposed"]).lower() == "false"
        for row in reflection_rows
    )
    locked_matrix_complete = (
        int(status["completed_converged"]) == 360
        and bool(status["pilot_numerical_matrix_complete"])
        and status["state"] == "COMPLETE"
    )
    zero_control_rejected = (
        maximum_direction_residual < 1.0e-12
        and maximum_internal_residual < 1.0e-12
        and maximum_integrand_residual < 1.0e-10
        and maximum_target_root_residual < 1.0e-10
        and same_anchor_mismatches == 0
        and reflected_anchor_mismatches == 0
        and current_sheet_target_mismatches > 0
        and image_cyclic_residual < 1.0e-6
        and physical_cyclic_residual > 1.0e-3
        and physical_image_difference > 1.0e-3
    )
    result = {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "verdict": (
            "REFLECTION_ZERO_CONTROL_REJECTED_FOR_LOCKED_UPPER_SHEET"
            if zero_control_rejected
            else "REFLECTION_GATE_INCONCLUSIVE"
        ),
        "locked_matrix_complete": locked_matrix_complete,
        "locked_bottleneck": failure["bottleneck_channel"],
        "event_map": {
            "variables": "(x,s,d,r,w,c)->(x,-s,-d,conj(r),conj(w),-conj(c))",
            "direction": "n_R=diag(1,-1,-1) conj(n)",
            "internal_momentum": "p_R^0=conj(p^0), p_R^space=diag(1,-1,-1) conj(p^space)",
            "maximum_direction_residual": maximum_direction_residual,
            "maximum_internal_residual": maximum_internal_residual,
        },
        "integrand_identity": {
            "equation": "F_R(-conj(c),conj(r),conj(w))=conj(F(c,r,w))",
            "comparisons": integrand_comparisons,
            "maximum_normalized_residual": maximum_integrand_residual,
        },
        "target_root_identity": {
            "stereographic_map": "h_R=1/conj(a), a_R=1/conj(h), C_R=1/conj(C)",
            "permutation": TARGET_PERMUTATION,
            "comparisons": root_comparisons,
            "maximum_normalized_residual": maximum_target_root_residual,
        },
        "anchor_ownership_identity": {
            "fixed_anchor": str(REFERENCE),
            "same_anchor_permutation": ANCHOR_PERMUTATION,
            "same_anchor_mismatches": same_anchor_mismatches,
            "reflected_anchor": str(-REFERENCE),
            "reflected_anchor_permutation": TARGET_PERMUTATION,
            "reflected_anchor_mismatches": reflected_anchor_mismatches,
            "current_sheet_target_permutation_mismatches": current_sheet_target_mismatches,
            "ownership_comparisons": ownership_comparisons,
        },
        "cyclic_counterexample": {
            "event_id": probe_event["event_id"],
            "relative_circle": str(probe_relative),
            "epsilon": EPSILON,
            "global_nodes": 128,
            "global_residue_nodes": 96,
            "original_vector": complex_strings(original_cyclic),
            "reflection_image_vector": complex_strings(image_cyclic),
            "prescribed_upper_sheet_reflected_vector": complex_strings(
                physical_cyclic
            ),
            "expected_reflection_vector": complex_strings(expected_cyclic),
            "image_relation_normalized_residual": image_cyclic_residual,
            "prescribed_sheet_relation_normalized_residual": physical_cyclic_residual,
            "prescribed_minus_image_normalized_difference": physical_image_difference,
        },
        "proof_scope": (
            "The algebra is tested over all 16 locked events, all 15 locked "
            "arguments, four relative phases, and three global phases. The "
            "owned-cycle failure is exhibited by a converged fixed-relative "
            "cyclic counterexample; no fresh adaptive outer kernel is claimed."
        ),
        "why_zero_control_fails": (
            "The target reflection maps the +0.3 anchor to -0.3 and swaps u/v "
            "within each sign. The implemented upper-sheet prescription reanchors "
            "every reflected event at +0.3, whose ownership instead swaps both "
            "sign and u/v. The resulting residue-carrying contour is not the "
            "reflection image, so an upper-sheet imaginary component is an "
            "absorptive discontinuity rather than a symmetry-forced zero."
        ),
        "zero_mean_imaginary_control_proven": False,
        "prior_5037_reflection_was_diagnostic_only": prior_reflection_was_diagnostic_only,
        "next_derivation": (
            "derive the upper-minus-lower-sheet discontinuity from the existing "
            "global and relative residue catalogues and test it as a nonzero, "
            "predeclared imaginary control; do not spend more kernels on the "
            "rejected zero-control route"
        ),
        "formalization_workbench_tree_sha256": formal_digest,
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(RESULT_JSON, result)
    checks = [
        ("sources_exist", not missing, "all 5109 source paths exist"),
        ("locked_matrix_complete", locked_matrix_complete, "360/360 converged"),
        (
            "direction_map_exact",
            maximum_direction_residual < 1.0e-12
            and maximum_internal_residual < 1.0e-12,
            f"direction={maximum_direction_residual}; internal={maximum_internal_residual}",
        ),
        (
            "integrand_identity",
            maximum_integrand_residual < 1.0e-10,
            str(maximum_integrand_residual),
        ),
        (
            "target_root_identity",
            maximum_target_root_residual < 1.0e-10,
            str(maximum_target_root_residual),
        ),
        ("same_anchor_permutation", same_anchor_mismatches == 0, str(same_anchor_mismatches)),
        (
            "reflected_anchor_permutation",
            reflected_anchor_mismatches == 0,
            str(reflected_anchor_mismatches),
        ),
        (
            "current_sheet_obstruction_present",
            current_sheet_target_mismatches > 0,
            str(current_sheet_target_mismatches),
        ),
        (
            "image_cycle_obeys_reflection",
            image_cyclic_residual < 1.0e-6,
            str(image_cyclic_residual),
        ),
        (
            "prescribed_cycle_rejects_reflection",
            physical_cyclic_residual > 1.0e-3
            and physical_image_difference > 1.0e-3,
            f"relation={physical_cyclic_residual}; image_difference={physical_image_difference}",
        ),
        (
            "prior_reflection_not_imposed",
            prior_reflection_was_diagnostic_only,
            "5037 symmetry_imposed=false",
        ),
        ("zero_control_rejected", zero_control_rejected, result["verdict"]),
        (
            "formalization_unchanged",
            formal_digest == FORMAL_BASELINE,
            formal_digest,
        ),
        (
            "claim_discipline",
            not result["valid_for_full_MTS_claim"],
            "estimator theorem only; no MTS physics claim",
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
                    "check_id": f"V5109_{index:02d}_{name}",
                    "passed": passed,
                    "detail": detail,
                    "checkpoint_marker": MARKER,
                }
            )
    failed = [name for name, passed, _ in checks if not passed]
    if failed:
        raise RuntimeError(f"checkpoint 5109 validation failed: {failed}")


if __name__ == "__main__":
    main()
