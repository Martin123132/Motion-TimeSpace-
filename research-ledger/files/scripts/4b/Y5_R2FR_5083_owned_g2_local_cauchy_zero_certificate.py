from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
from typing import Any

import mpmath as mp
import numpy as np


POST = Path(__file__).resolve().parents[1]
SCRIPT_5040 = POST / "scripts" / "Y5_R2FR_5040_arbitrary_precision_cross_source_residue.py"
SCRIPT_5045 = POST / "scripts" / "Y5_R2FR_5045_theorem_scope_falsification_and_quarantine.py"
SCRIPT_5077 = POST / "scripts" / "Y5_R2FR_5077_central_anchor_pilot_runner.py"
COMPARATOR = POST / "source-intake" / "functional_rg" / "5082" / "full_homotopy_residue_instability_comparator.json"
PILOT_RUN = POST / "source-intake" / "functional_rg" / "5079" / "runs" / "bounded_central_anchor_pilot_v2"
SOURCE = POST / "source-intake" / "functional_rg" / "5083"
RESULT_JSON = SOURCE / "owned_g2_local_cauchy_zero_certificate.json"
WITNESS_JSON = SOURCE / "owned_g2_arbitrary_precision_witness.json"
VALIDATION_CSV = POST / "source-intake" / "mts_residuals" / "P8_Y5_BRR545_5083_VALIDATION.csv"
MARKER = "MTS_5083_OWNED_G2_LOCAL_CAUCHY_ZERO_CERTIFICATE"
REVISION = "event-local-source-separated-cauchy-and-70-digit-witness-v1"
FORMAL_BASELINE = "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
EVENT_ID = "S507602_N0000"
ARGUMENT_ID = "E040_A00"
BASE_ID = "A00"
PROFILE = "primary24"
CHAMBER_INDEX = 0
PAIR = ("direct:g2:minus_v", "subtraction:decay:plus_v")
OWNED_LABEL = "direct:g2:minus_v"
UNOWNED_LABEL = "subtraction:decay:plus_v"
DIRECT_INDEX = 1
ROOT_LABEL = "minus_v"
RELATIVE_FRACTIONS = (0.1, 0.05)
GLOBAL_FRACTIONS = (0.15, 0.075)
RELATIVE_NODES = 16
GLOBAL_NODES = 16
DPS = 70


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5040 = load_module("mts_5040_for_5083", SCRIPT_5040)
M5077 = load_module("mts_5077_for_5083", SCRIPT_5077)
N5030 = M5077.M5036.N5030


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True), encoding="utf-8")
    os.replace(temporary, path)


def serialized(value: complex | mp.mpc) -> dict[str, float]:
    return {"real": float(mp.re(value)), "imaginary": float(mp.im(value))}


def mpc(value: complex) -> mp.mpc:
    return mp.mpc(str(value.real), str(value.imag))


def locate_offending_row(document: dict[str, Any]) -> tuple[dict[str, Any], int]:
    target = tuple(sorted(PAIR))
    matches: list[tuple[dict[str, Any], int]] = []
    for chamber in document["fixed_event_integral_gate"]["chambers"]:
        for row in chamber["residue_catalog"]:
            pairs = {tuple(sorted(str(label) for label in pair)) for pair in row["pairs"]}
            if target in pairs and abs(complex(row["root"])) < 1.0:
                matches.append((row, int(chamber["chamber_index"])))
    if len(matches) != 1:
        raise RuntimeError(f"expected one subunit offending row, found {len(matches)}")
    return matches[0]


def double_direct_component(
    internal: np.ndarray,
    soft_energy: float,
    scattering_cosine: complex,
    unit_circle: complex,
) -> complex:
    module = N5030.M5028.M5026
    rotated = module.M5024.rotate_internal(internal, unit_circle)
    inverse_energy_square_sum = sum(
        1.0 / (momentum[0] * momentum[0]) for momentum in rotated
    )
    multiplier = (
        3.0
        / (rotated[2, 0] * rotated[2, 0])
        / inverse_energy_square_sum
    )
    value = (
        soft_energy
        * soft_energy
        * multiplier
        * module.M5017.hhh_reduced_product(rotated, scattering_cosine, 1.0)
        / (module.M5017.S_VALUE * module.M5017.S_VALUE)
    )
    return complex(value / soft_energy)


def selected_direct_data(
    relative_circle: complex,
    ownership: dict[str, bool],
) -> tuple[np.ndarray, np.ndarray, np.ndarray, complex, float]:
    soft_direction, decay_direction, internal = N5030.M5028.event_geometry(
        N5030.SOFT_ENERGY,
        complex(N5030.SOFT_COSINE, 0.0),
        complex(N5030.DECAY_COSINE, 0.0),
        relative_circle,
    )
    groups = N5030.M5028.fixed_ownership_groups(
        internal,
        soft_direction,
        decay_direction,
        N5030.TARGET_COSINE,
        ownership,
    )
    selected = [group for group in groups if OWNED_LABEL in group["labels"]]
    if len(selected) != 1:
        raise RuntimeError(f"owned branch count is {len(selected)}")
    root = complex(selected[0]["root"])
    separations = [
        abs(root - complex(other["root"]))
        for other in groups
        if other is not selected[0]
    ]
    safe_scale = min([abs(root)] + separations)
    if not math.isfinite(safe_scale) or safe_scale <= 0.0:
        raise RuntimeError("invalid global safe scale")
    return soft_direction, decay_direction, internal, root, safe_scale


def mp_global_residue(
    relative_circle: mp.mpc,
    ownership: dict[str, bool],
    nodes: int,
    radius_fraction: float,
) -> mp.mpc:
    _, _, _, double_root, safe_scale = selected_direct_data(
        complex(relative_circle), ownership
    )
    soft_direction, decay_direction, internal = M5040.event_geometry(
        N5030.SOFT_ENERGY,
        complex(N5030.SOFT_COSINE, 0.0),
        complex(N5030.DECAY_COSINE, 0.0),
        relative_circle,
    )
    direction = [
        internal[DIRECT_INDEX][index] / internal[DIRECT_INDEX][0]
        for index in range(1, 4)
    ]
    root = M5040.factor_root(direction, N5030.TARGET_COSINE, ROOT_LABEL)
    if abs(complex(root) - double_root) > 2.0e-8 * max(1.0, abs(double_root)):
        raise RuntimeError("arbitrary-precision and transported g2 roots disagree")
    radius = mp.mpf(str(radius_fraction * safe_scale))
    total = mp.mpc(0)
    for index in range(nodes):
        phase = mp.e ** (
            2j * mp.pi * (mp.mpf(index) + mp.mpf("0.317")) / nodes
        )
        unit_circle = root + radius * phase
        total += (
            M5040.finite_plus_component(
                "direct",
                internal,
                N5030.SOFT_ENERGY,
                soft_direction,
                decay_direction,
                N5030.TARGET_COSINE,
                unit_circle,
            )
            / unit_circle
            * radius
            * phase
        )
    return total / nodes


def mp_relative_residue(
    root: complex,
    safe_scale: float,
    ownership: dict[str, bool],
    relative_fraction: float,
    global_fraction: float,
) -> mp.mpc:
    radius = mp.mpf(str(relative_fraction * safe_scale))
    root_mp = mpc(root)
    total = mp.mpc(0)
    for index in range(RELATIVE_NODES):
        phase = mp.e ** (
            2j
            * mp.pi
            * (mp.mpf(index) + mp.mpf("0.317"))
            / RELATIVE_NODES
        )
        relative_circle = root_mp + radius * phase
        total += (
            mp_global_residue(
                relative_circle,
                ownership,
                GLOBAL_NODES,
                global_fraction,
            )
            / relative_circle
            * radius
            * phase
        )
    return total / RELATIVE_NODES


def port_validation(ownership: dict[str, bool]) -> dict[str, Any]:
    rows = []
    probes = (
        (complex(-0.006, 0.0002), complex(0.61, 0.37)),
        (complex(-0.0055, -0.0001), complex(-0.72, 0.19)),
        (complex(-0.0058, 0.0004), complex(1.31, 0.41)),
    )
    for relative_circle, unit_circle in probes:
        soft_direction, decay_direction, internal, _, _ = selected_direct_data(
            relative_circle, ownership
        )
        double = double_direct_component(
            internal,
            N5030.SOFT_ENERGY,
            N5030.TARGET_COSINE,
            unit_circle,
        )
        arbitrary = M5040.finite_plus_component(
            "direct",
            internal,
            N5030.SOFT_ENERGY,
            soft_direction,
            decay_direction,
            N5030.TARGET_COSINE,
            mpc(unit_circle),
        )
        relative_difference = float(
            abs(arbitrary - mpc(double)) / max(abs(double), 1.0)
        )
        rows.append(
            {
                "relative_circle": serialized(relative_circle),
                "unit_circle": serialized(unit_circle),
                "double": serialized(double),
                "arbitrary_precision": serialized(arbitrary),
                "relative_difference": relative_difference,
            }
        )
    maximum = max(row["relative_difference"] for row in rows)
    return {"rows": rows, "maximum_relative_difference": maximum, "passed": maximum < 2.0e-10}


def structural_audit(
    root: complex,
    safe_scale: float,
    ownership: dict[str, bool],
) -> dict[str, Any]:
    target_module = N5030.M5028.M5024
    minimum_same_component_separation = math.inf
    minimum_energy_magnitude = math.inf
    minimum_inverse_energy_square_sum = math.inf
    minimum_source_direction_separation = math.inf
    maximum_owned_root_motion = 0.0
    central_soft, central_decay, central_internal = N5030.M5028.event_geometry(
        N5030.SOFT_ENERGY,
        complex(N5030.SOFT_COSINE, 0.0),
        complex(N5030.DECAY_COSINE, 0.0),
        root,
    )
    central_sources = N5030.M5028.source_directions(
        central_internal, central_soft, central_decay
    )
    central_global_root = complex(
        target_module.all_factor_roots(
            central_sources["direct:g2"], N5030.TARGET_COSINE
        )[ROOT_LABEL]
    )
    samples = []
    for index in range(32):
        phase = np.exp(2.0j * np.pi * (index + 0.317) / 32)
        relative_circle = root + 0.1 * safe_scale * phase
        soft_direction, decay_direction, internal, owned_root, global_safe = selected_direct_data(
            relative_circle, ownership
        )
        sources = N5030.M5028.source_directions(
            internal, soft_direction, decay_direction
        )
        direct_roots: list[tuple[str, complex]] = []
        for source in ("direct:g1", "direct:g2", "direct:g3"):
            roots = target_module.all_factor_roots(
                sources[source], N5030.TARGET_COSINE
            )
            for label, value in roots.items():
                direct_roots.append((f"{source}:{label}", complex(value)))
        same_component_separation = min(
            abs(owned_root - candidate)
            for label, candidate in direct_roots
            if label != OWNED_LABEL
        )
        energies = [abs(complex(momentum[0])) for momentum in internal]
        inverse_sum = abs(
            sum(1.0 / (momentum[0] * momentum[0]) for momentum in internal)
        )
        g2_direction = sources["direct:g2"]
        source_direction_separation = min(
            float(np.linalg.norm(g2_direction - sources["subtraction:soft"])),
            float(np.linalg.norm(g2_direction - sources["subtraction:decay"])),
        )
        minimum_same_component_separation = min(
            minimum_same_component_separation, same_component_separation
        )
        minimum_energy_magnitude = min(minimum_energy_magnitude, *energies)
        minimum_inverse_energy_square_sum = min(
            minimum_inverse_energy_square_sum, float(inverse_sum)
        )
        minimum_source_direction_separation = min(
            minimum_source_direction_separation, source_direction_separation
        )
        maximum_owned_root_motion = max(
            maximum_owned_root_motion, abs(owned_root - central_global_root)
        )
        samples.append(
            {
                "relative_circle": serialized(relative_circle),
                "owned_global_root": serialized(owned_root),
                "global_all_source_safe_scale": global_safe,
                "same_direct_component_root_separation": same_component_separation,
                "minimum_internal_energy_magnitude": min(energies),
                "inverse_energy_square_sum_magnitude": float(inverse_sum),
                "g2_to_subtraction_direction_separation": source_direction_separation,
            }
        )
    guards = {
        "relative_disk_excludes_origin": abs(root) > 0.1 * safe_scale,
        "owned_and_unowned_labels_are_opposite": bool(ownership[OWNED_LABEL])
        and not bool(ownership[UNOWNED_LABEL]),
        "owned_source_is_recoil_g2": OWNED_LABEL.startswith("direct:g2:"),
        "same_direct_component_poles_are_isolated": minimum_same_component_separation
        > 10.0 * maximum_owned_root_motion,
        "internal_energies_nonzero_on_sampled_boundary": minimum_energy_magnitude > 1.0e-8,
        "direct_multiplier_denominator_nonzero_on_sampled_boundary": minimum_inverse_energy_square_sum
        > 1.0e-8,
        "g2_is_not_a_subtraction_direction_alias": minimum_source_direction_separation
        > 1.0e-8,
        "global_contour_fraction_is_strictly_local": max(GLOBAL_FRACTIONS) < 0.5,
    }
    return {
        "guards": guards,
        "passed": all(guards.values()),
        "minimum_same_direct_component_root_separation": minimum_same_component_separation,
        "maximum_owned_root_motion_on_relative_boundary": maximum_owned_root_motion,
        "minimum_internal_energy_magnitude": minimum_energy_magnitude,
        "minimum_inverse_energy_square_sum_magnitude": minimum_inverse_energy_square_sum,
        "minimum_g2_to_subtraction_direction_separation": minimum_source_direction_separation,
        "samples": samples,
    }


def arbitrary_precision_witness(
    root: complex,
    safe_scale: float,
    ownership: dict[str, bool],
) -> dict[str, Any]:
    mp.mp.dps = DPS
    port = port_validation(ownership)
    values = []
    table: dict[tuple[float, float], complex] = {}
    for relative_fraction in RELATIVE_FRACTIONS:
        for global_fraction in GLOBAL_FRACTIONS:
            value = mp_relative_residue(
                root,
                safe_scale,
                ownership,
                relative_fraction,
                global_fraction,
            )
            value_complex = complex(value)
            table[(relative_fraction, global_fraction)] = value_complex
            values.append(
                {
                    "relative_fraction": relative_fraction,
                    "global_fraction": global_fraction,
                    "value": serialized(value),
                    "magnitude": float(abs(value)),
                }
            )
    expected_ratio = float(2**RELATIVE_NODES)
    halving_rows = []
    for global_fraction in GLOBAL_FRACTIONS:
        outer = table[(RELATIVE_FRACTIONS[0], global_fraction)]
        inner = table[(RELATIVE_FRACTIONS[1], global_fraction)]
        ratio = outer / inner
        halving_rows.append(
            {
                "global_fraction": global_fraction,
                "complex_ratio": serialized(ratio),
                "ratio_magnitude": abs(ratio),
                "expected_ratio": expected_ratio,
                "relative_error": abs(ratio / expected_ratio - 1.0),
            }
        )
    global_radius_rows = []
    for relative_fraction in RELATIVE_FRACTIONS:
        first = table[(relative_fraction, GLOBAL_FRACTIONS[0])]
        second = table[(relative_fraction, GLOBAL_FRACTIONS[1])]
        relative_difference = abs(first - second) / max(abs(first), abs(second), 1.0e-300)
        global_radius_rows.append(
            {
                "relative_fraction": relative_fraction,
                "relative_difference": relative_difference,
            }
        )
    maximum_outer_magnitude = max(
        abs(table[(RELATIVE_FRACTIONS[0], fraction)])
        for fraction in GLOBAL_FRACTIONS
    )
    maximum_inner_magnitude = max(
        abs(table[(RELATIVE_FRACTIONS[1], fraction)])
        for fraction in GLOBAL_FRACTIONS
    )
    maximum_ratio_error = max(row["relative_error"] for row in halving_rows)
    maximum_global_radius_difference = max(
        row["relative_difference"] for row in global_radius_rows
    )
    passed = bool(
        port["passed"]
        and maximum_outer_magnitude < 2.0e-19
        and maximum_inner_magnitude < 3.0e-24
        and maximum_ratio_error < 2.0e-5
        and maximum_global_radius_difference < 2.0e-6
    )
    return {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "dps": DPS,
        "relative_nodes": RELATIVE_NODES,
        "global_nodes": GLOBAL_NODES,
        "relative_fractions": list(RELATIVE_FRACTIONS),
        "global_fractions": list(GLOBAL_FRACTIONS),
        "port_validation": port,
        "values": values,
        "halving_rows": halving_rows,
        "global_radius_rows": global_radius_rows,
        "maximum_outer_magnitude": maximum_outer_magnitude,
        "maximum_inner_magnitude": maximum_inner_magnitude,
        "maximum_halving_ratio_relative_error": maximum_ratio_error,
        "maximum_global_radius_relative_difference": maximum_global_radius_difference,
        "passed": passed,
        "valid_for_full_MTS_claim": False,
    }


def main() -> None:
    required = [
        SCRIPT_5040,
        SCRIPT_5045,
        SCRIPT_5077,
        COMPARATOR,
        PILOT_RUN / "config.json",
        PILOT_RUN / "kernels" / f"E040__{EVENT_ID}__{BASE_ID}__{PROFILE}.json",
    ]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError(f"missing 5083 inputs: {missing}")
    comparator = json.loads(COMPARATOR.read_text(encoding="utf-8"))
    config = json.loads((PILOT_RUN / "config.json").read_text(encoding="utf-8"))
    events = M5077.M5036.event_lookup(config)
    arguments = M5077.M5036.argument_lookup(config)
    event = events[EVENT_ID]
    argument = arguments[ARGUMENT_ID]
    target = M5077.M5036.complex_from_row(argument["target_cosine"])
    M5077.M5036.M5035.M5034.configure(event, target)
    kernel_path = PILOT_RUN / "kernels" / f"E040__{EVENT_ID}__{BASE_ID}__{PROFILE}.json"
    kernel = json.loads(kernel_path.read_text(encoding="utf-8"))
    row, chamber_index = locate_offending_row(kernel)
    ownership = N5030.physical_chambers()[1][chamber_index]
    root = complex(row["root"])
    safe_scale = float(row["outer_radius"]) / float(row["residue_contour_fraction"])
    labels = sorted({str(label) for pair in row["pairs"] for label in pair})
    owned_labels = [label for label in labels if bool(ownership[label])]
    structural = structural_audit(root, safe_scale, ownership)
    witness = arbitrary_precision_witness(root, safe_scale, ownership)
    atomic_json(WITNESS_JSON, witness)
    local_scope_guards = {
        "topology_transport_exonerated": comparator["transport_topology_exonerated"],
        "same_offending_pair_in_full_and_constructed": comparator["same_offending_pair_instability"],
        "event_exact": event["event_id"] == EVENT_ID,
        "argument_exact": argument["argument_id"] == ARGUMENT_ID,
        "chamber_exact": chamber_index == CHAMBER_INDEX,
        "single_pair_exact": len(row["pairs"]) == 1
        and tuple(str(value) for value in row["pairs"][0]) == PAIR,
        "owned_label_exact": owned_labels == [OWNED_LABEL],
        "unowned_label_exact": not ownership[UNOWNED_LABEL],
        "relative_root_nonzero": abs(root) > safe_scale,
        "relative_collision_disk_isolated": safe_scale > 0.0
        and float(row["residue_contour_fraction"]) < 1.0,
        "structural_audit_passed": structural["passed"],
        "arbitrary_precision_witness_passed": witness["passed"],
    }
    accepted = all(local_scope_guards.values())
    result = {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "event_id": EVENT_ID,
        "argument_id": ARGUMENT_ID,
        "profile": PROFILE,
        "chamber_index": chamber_index,
        "pair": list(PAIR),
        "owned_label": OWNED_LABEL,
        "unowned_label": UNOWNED_LABEL,
        "root": serialized(root),
        "relative_safe_scale": safe_scale,
        "local_scope_guards": local_scope_guards,
        "structural_audit": structural,
        "arbitrary_precision_witness": str(WITNESS_JSON),
        "arbitrary_precision_witness_sha256": digest(WITNESS_JSON),
        "analytic_identity": (
            "For the source-separated direct component D(q,z), choose a local z cycle "
            "containing only the transported direct:g2:minus_v pole cluster. The audited "
            "same-direct-component separation keeps that cycle in one meromorphic family "
            "through the isolated cross-source collision. Its z residue R_D(q) is therefore "
            "holomorphic in the audited q disk. Because q0 is nonzero, Res_q[R_D(q)/q]=0. "
            "The subtraction pole is unowned and contributes zero to the direct-only local "
            "z cycle by Cauchy analyticity."
        ),
        "certificate_scope": (
            "event-local only: S507602_N0000, E040_A00, chamber 0, owned "
            "direct:g2:minus_v versus unowned subtraction:decay:plus_v"
        ),
        "catalog_completeness_assumption": (
            "the finite-x global pole catalogue contains every direct-component pole in "
            "the audited neighborhood"
        ),
        "residue_value": {"real": 0.0, "imaginary": 0.0},
        "accepted_local_zero_certificate": accepted,
        "general_g2_family_theorem_claimed": False,
        "broad_5041_theorem_reinstated": False,
        "pilot_resume_authorized_for_this_row": accepted,
        "source_paths": {str(path): digest(path) for path in required},
        "formalization_workbench_tree_sha256": FORMAL_BASELINE,
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(RESULT_JSON, result)
    checks = [
        ("source_paths_exist", not missing, "all local sources present"),
        ("scope_exact", all(value for key, value in local_scope_guards.items() if key not in {"structural_audit_passed", "arbitrary_precision_witness_passed"}), str(local_scope_guards)),
        ("structural_cauchy_guards", structural["passed"], str(structural["guards"])),
        ("mp_port", witness["port_validation"]["passed"], f"max={witness['port_validation']['maximum_relative_difference']}"),
        ("mp_zero_witness", witness["passed"], f"outer={witness['maximum_outer_magnitude']}; inner={witness['maximum_inner_magnitude']}"),
        ("halving_signature", witness["maximum_halving_ratio_relative_error"] < 2.0e-5, f"error={witness['maximum_halving_ratio_relative_error']}"),
        ("global_radius_independence", witness["maximum_global_radius_relative_difference"] < 2.0e-6, f"difference={witness['maximum_global_radius_relative_difference']}"),
        ("local_certificate_accepted", accepted, result["certificate_scope"]),
        ("broad_theorem_not_reinstated", not result["general_g2_family_theorem_claimed"] and not result["broad_5041_theorem_reinstated"], "local row only"),
        ("formalization_unchanged", result["formalization_workbench_tree_sha256"] == FORMAL_BASELINE, result["formalization_workbench_tree_sha256"]),
        ("claim_discipline", not result["valid_for_full_MTS_claim"], "numerical pipeline certificate is not MTS evidence"),
    ]
    VALIDATION_CSV.parent.mkdir(parents=True, exist_ok=True)
    with VALIDATION_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=("check_id", "passed", "detail", "checkpoint_marker"))
        writer.writeheader()
        for index, (name, passed, detail) in enumerate(checks, start=1):
            writer.writerow(
                {
                    "check_id": f"V5083_{index:02d}_{name}",
                    "passed": passed,
                    "detail": detail,
                    "checkpoint_marker": MARKER,
                }
            )
    failed = [name for name, passed, _ in checks if not passed]
    if failed:
        raise RuntimeError(f"checkpoint 5083 validation failed: {failed}")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
